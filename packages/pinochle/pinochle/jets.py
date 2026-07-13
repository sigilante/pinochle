"""
Jet dispatch for the Nock interpreter.

A jet is a native implementation of a Nock arm, matched by the mug of a
core's battery -- the same register-then-match architecture Vere uses,
minus parents and hooks.

Two tables:

  * REGISTRY maps a jet *name* (a @tas cord, e.g. %dec) to a native
    `fn(core) -> result`.  These are the jet implementations, declared in
    the Python runtime ahead of time.
  * WARM maps a battery *mug* to one of those natives.  It is populated at
    run time: a %fast hint

        *[a 11 [%fast name] core-formula]

    is transparent (it just produces the core `*[a core-formula]`), but as
    a side effect it registers `mug(battery) -> REGISTRY[name]`, where the
    battery is the head of the produced core.

Dispatch then happens at arm invocation (Nock 9): computing `*[a 9 b c]`
first builds the core `*[a c]`; if `mug(head(core))` is warm, the native
runs against the core instead of the arm formula.  A native receives the
whole core `[battery payload]`; for a gate the sample sits at axis 6 and
the context at axis 7 (the standard Hoon calling convention).

Correctness contract: jet(core) == *[core 2 [0 1] 0 b] (the arm). VALIDATE
runs both on every dispatch and asserts they agree.  Registering a jet is a
promise about a formula, so only register natives you have certified.

Semantics vs disabled: with ENABLED False (or an unregistered name/battery)
nothing is warmed and nothing dispatches, so the interpreter runs the arm
formula and results are identical -- a jet only changes cost, never meaning.

Caveats (deliberate simplifications): dispatch keys on the battery mug
alone, so it assumes one jet per battery (true for gates, not multi-arm
cores); and mug is 31-bit, so distinct batteries could in principle collide
(astronomically unlikely).
"""

import time

from .noun import Cell, deep, pretty, mug


def _default_slog(clue):
    """Default %slog sink: `clue` is [priority tank]; print the tank to stderr."""
    import sys
    tank = clue.tail if deep(clue) else clue
    sys.stderr.write(pretty(tank, False) + "\n")


#: sink for %slog debug hints: fn(clue_noun) -> None. Reassign to redirect
#: (e.g. a Jupyter kernel routing slogs into cell output).
SLOG = _default_slog


def _default_bout(elapsed_ns):
    """Default %bout sink: print the elapsed time of the timed formula."""
    import sys
    sys.stderr.write(f"bout: {elapsed_ns / 1e6:.3f} ms\n")


#: sink for %bout timing hints: fn(elapsed_ns) -> None. Reassign to redirect
#: or silence (set to a no-op).
BOUT = _default_bout


def bout(thunk):
    """Time `thunk()`, report the elapsed nanoseconds via BOUT, return its
    result.  Reports even if the body crashes, matching Urbit's %bout."""
    start = time.perf_counter_ns()
    try:
        return thunk()
    finally:
        BOUT(time.perf_counter_ns() - start)

#: master switch: when False, nothing warms and nothing dispatches
ENABLED = True

#: run each dispatch through native *and* arm formula and assert equality
#: (slow; for certification runs)
VALIDATE = False

#: jet name cord -> native fn(core) -> result (noun or python int)
REGISTRY: dict[int, callable] = {}

#: battery mug -> native fn(core), populated by %fast hints at run time
WARM: dict[int, callable] = {}


def cord(name) -> int:
    """A @tas name as a little-endian atom (%dec -> 6514020). Ints pass through."""
    if isinstance(name, str):
        return int.from_bytes(name.encode(), "little")
    return name


def register(name, fn):
    """Register native `fn(core) -> result` under jet `name` (str or cord)."""
    REGISTRY[cord(name)] = fn
    return fn


def warm_register(name, battery):
    """A %fast hint fired: warm `mug(battery)` to the native named `name`.

    No-op if jets are disabled or `name` names no registered native.
    """
    if not ENABLED:
        return
    fn = REGISTRY.get(cord(name))
    if fn is not None:
        WARM[mug(battery)] = fn


def warm_lookup(battery):
    """Native warmed for this battery, or None if unjetted/disabled."""
    if not ENABLED:
        return None
    return WARM.get(mug(battery))


def reset_warm():
    """Clear the run-time warm table (does not touch REGISTRY)."""
    WARM.clear()


def _atom(n):
    if deep(n):
        raise ValueError("jet: expected atom")
    return int(n)


def _sample(core):
    """A jet receives the core [battery payload]; a gate's payload is
    [sample context], so the sample is at axis 6."""
    return core.tail.head


# --- built-in arithmetic jets -------------------------------------------
# Natives receive the core and read the sample at +6, reproducing the arm
# formula's crash behaviour so VALIDATE stays exact.

def _j_dec(core):
    n = _atom(_sample(core))
    if n == 0:
        raise Exception("fail: dec 0")
    return n - 1

def _j_add(core):
    s = _sample(core)
    return _atom(s.head) + _atom(s.tail)

def _j_sub(core):
    s = _sample(core)
    a, b = _atom(s.head), _atom(s.tail)
    if b > a:
        raise Exception("fail: sub underflow")
    return a - b

def _j_mul(core):
    s = _sample(core)
    return _atom(s.head) * _atom(s.tail)

def _j_lte(core):
    s = _sample(core)
    return 0 if _atom(s.head) <= _atom(s.tail) else 1


for _name, _fn in {
    "dec": _j_dec,
    "add": _j_add,
    "sub": _j_sub,
    "mul": _j_mul,
    "lte": _j_lte,
}.items():
    register(_name, _fn)
