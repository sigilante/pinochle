# Pinochle - Core Library

Python implementation of the Nock 4K Combinator Calculus.

## Components

* `noun.py`:  [`pynoun` from Urbit](https://github.com/urbit/tools/blob/master/pkg/pynoun/noun.py)
* `nock.py`:  Nock tree-walking interpreter

## Installation

```bash
pip install pinochle
```

Or from source:
```bash
git clone https://github.com/sigilante/pinochle.git
cd pinochle/packages/pinochle
pip install .
```

## Usage

```python
from pinochle import nock, parse_noun

# Parse and evaluate Nock expressions
result = nock(42, parse_noun("[0 1]"))
print(result)  # 42

# Increment
result = nock(41, parse_noun("[4 0 1]"))
print(result)  # 42
```

## Terms (`%tas`)

The parser accepts Hoon-style `%` constants alongside numbers.  `%` before a
number is that number (an atom is already a constant); `%` before a term
(`a-z`, `-`, `.`, …) is the term's bytes as a little-endian atom — the `@tas`
cord.  Number syntax (with `.` digit separators) is unchanged.

```python
from pinochle import parse

parse('%dec')        # 6514020   (little-endian cord for "dec")
parse('%42')         # 42
parse('[%fast %dec]')# Cell(1953718630, 6514020)
parse('1.024')       # 1024
```

## Jets and hints

A jet is a native Python implementation of a Nock arm, matched by the mug of
a core's battery — the register-then-match architecture Vere uses, minus
parents and hooks.

A `%fast` opcode-11 hint wraps a core-producing formula:

```
*[a 11 [%fast name] core-formula]  ==  *[a core-formula]
```

It is **transparent** — it just produces the core — but as a side effect it
*warms* the core's battery: it records `mug(battery) → native` in a run-time
table, where the native is looked up by `name` (a `@tas` cord such as `%dec`,
or an Urbit-style `[name parent hooks]` clue whose head is the name; the clue
is metadata, never evaluated as a formula).

Dispatch happens at arm invocation (Nock 9).  Evaluating `*[a 9 b c]` builds
the core `*[a c]`; if its battery is warm, the native runs against the core
instead of the arm formula.  A native receives the whole core
`[battery payload]`; for a gate the sample is at axis 6 and the context at
axis 7 (the standard Hoon calling convention).  With jets disabled, or an
unregistered name/battery, nothing warms and nothing dispatches — results are
identical, so a jet only changes cost, never meaning.

```python
from pinochle import nock, parse, to_noun, register_jet, jets, Cell

# A native reads the sample from the core at +6.  The built-ins
# (dec/add/sub/mul/lte) follow the same convention; register your own by name.
register_jet('inc', lambda core: int(core.tail.head) + 1)

# A minimal inc gate: core = [battery [sample context]], battery [4 0 6].
core = to_noun(((4, 0, 6), (5, 0)))

# %fast warms the battery and returns the core (transparent)...
nock(0, Cell(11, Cell(Cell(jets.cord('fast'), jets.cord('inc')), Cell(1, core))))
# ...so invoking arm 2 now dispatches the native instead of the formula:
nock(core, parse('[9 2 0 1]'))           # 6

# Certification: run BOTH native and arm formula on every dispatch, assert equal.
jets.VALIDATE = True
# Master switch (nothing warms, nothing dispatches — pure interpreter):
jets.ENABLED = False
jets.reset_warm()                        # clear the run-time warm table
```

`pinochle` is an interpreter, not a compiler: it emits no hints.  Jets fire
only on cores warmed by `[11 [%fast name] core]` hints present in the noun
(for example those produced by
[`nockasm`](https://github.com/sigilante/nockasm)'s `(%hintd 'fast' 'dec' …)`).
Dispatch keys on the battery mug alone, so it assumes one jet per battery
(true for gates, not multi-arm cores) and, being a 31-bit mug, could in
principle collide (astronomically unlikely).

## Debug output (`%slog`)

The dynamic hint `[11 [%slog clue] body]` prints its clue (`[priority tank]`)
before producing `body`, the Nock analogue of Hoon's `~&`.  It stays
transparent — `body`'s value is unchanged.  Output goes to stderr by default
through a redirectable sink:

```python
from pinochle import jets
# e.g. route ~& output into a Jupyter cell instead of the server's stderr
jets.SLOG = lambda clue: my_stream_writer(clue)
```

## API Reference

See full documentation in the repository.

## License

MIT License