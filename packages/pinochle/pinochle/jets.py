"""
Jet dispatch for the Nock interpreter.

A jet is a native Python implementation of a Nock formula, selected by a
%fast opcode-11 hint:

    *[a 11 [%fast name] body]  ==  *[a body]

The hint is transparent -- it computes exactly what `body` would -- and its
clue `[%fast name]` is metadata, not a formula (it is never evaluated).
`name` is a @tas cord (e.g. %dec) identifying which arm is accelerated, or
an Urbit-style [name parent hooks] clue whose head is the name. When jets
are ENABLED and `name` names a registered jet, the interpreter runs the
native implementation against the subject `a` instead of interpreting
`body`. When jets are disabled, or `name` is unregistered, it interprets
`body` -- so the two paths return identical results; a jet only changes
cost, never meaning.

Correctness contract: jet(a) == *[a body]. VALIDATE mode runs both paths on
every dispatch and asserts they agree, for certification.

This is the acceleration architecture Vere uses for Hoon's dec/add, minus
core registration: dispatch is on the %fast name alone, with no battery-mug
warm table. Registering a jet is a promise about a formula, so only
register natives you have certified (see VALIDATE and the tests).
"""

import sys

from .noun import Cell, deep, pretty


def _default_slog(clue):
    """Default %slog sink: `clue` is [priority tank]; print the tank to stderr."""
    tank = clue.tail if deep(clue) else clue
    sys.stderr.write(pretty(tank, False) + "\n")


#: sink for %slog debug hints: fn(clue_noun) -> None. Reassign to redirect
#: (e.g. a Jupyter kernel routing slogs into cell output).
SLOG = _default_slog

#: master switch: when False, every hint falls through to its formula body
ENABLED = True

#: run each dispatch through native *and* formula and assert equality (slow;
#: intended for certification runs, not production)
VALIDATE = False

#: tag cord -> fn(subject_noun) -> result (noun or python int)
REGISTRY: dict[int, callable] = {}


def cord(name) -> int:
    """A @tas name as a little-endian atom (%dec -> 6513252). Ints pass through."""
    if isinstance(name, str):
        return int.from_bytes(name.encode(), "little")
    return name


def register(name, fn):
    """Register native `fn(subject) -> result` under jet `name` (str or cord)."""
    REGISTRY[cord(name)] = fn
    return fn


def lookup(tag):
    """Native fn for a static-hint tag atom, or None if unjetted/disabled."""
    if not ENABLED:
        return None
    return REGISTRY.get(int(tag))


def _atom(n):
    if deep(n):
        raise ValueError("jet: expected atom")
    return int(n)


# --- built-in arithmetic jets -------------------------------------------
# Convention (matching a standard Hoon-style arm core): the jet receives the
# arm subject [battery sample]; arguments live in the sample, i.e. `subj.tail`.
# Natives reproduce the formula's crash behaviour so VALIDATE stays exact.

def _j_dec(subj):
    n = _atom(subj.tail)
    if n == 0:
        raise Exception("fail: dec 0")
    return n - 1

def _j_add(subj):
    s = subj.tail
    return _atom(s.head) + _atom(s.tail)

def _j_sub(subj):
    s = subj.tail
    a, b = _atom(s.head), _atom(s.tail)
    if b > a:
        raise Exception("fail: sub underflow")
    return a - b

def _j_mul(subj):
    s = subj.tail
    return _atom(s.head) * _atom(s.tail)

def _j_lte(subj):
    s = subj.tail
    return 0 if _atom(s.head) <= _atom(s.tail) else 1


for _name, _fn in {
    "dec": _j_dec,
    "add": _j_add,
    "sub": _j_sub,
    "mul": _j_mul,
    "lte": _j_lte,
}.items():
    register(_name, _fn)
