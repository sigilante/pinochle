"""Runnable demo: a %fast jet accelerating a real Nock formula.

    python examples/jets_demo.py

We build a `dec` gate whose $ arm is the genuine O(n) Nock decrement loop
(atoms expose only increment and equality, so pure `dec` counts up from 0).
A %fast hint warms the gate's battery to the built-in O(1) `%dec` native.
The same call then goes two ways:

  * jets off  -> the interpreter walks the loop formula
  * jets on   -> the native runs instead, keyed on the battery's mug

Both yield the same value: a jet changes cost, never meaning.  VALIDATE
mode proves it, running the native AND the formula on every dispatch and
asserting they agree.
"""

import sys

from pinochle import nock, parse, jets, Cell, mug

# The canonical Nock decrement loop, subject = the atom m, result m - 1.
# (This is nockasm's benchmarks/dec.nasm expanded to flat Nock.)
DEC_LOOP = parse(
    "[8 [1 [8 [9 5 0 1] 9 2 10 [6 0 7] 0 2] 8 [1 0] "
    "[1 6 [5 [1 0] 0 6] [0 0] 8 [1 0] 8 [1 6 [5 [0 30] 4 0 6] "
    "[0 6] 9 2 10 [6 4 0 6] 0 1] 9 2 0 1] 0 1] 9 4 0 1]"
)

# A gate: core = [battery [sample context]].  The battery reads the sample at
# axis 6 (Hoon's gate convention) and runs the dec loop on it.
BATTERY = Cell(7, Cell(Cell(0, 6), DEC_LOOP))     # [7 [0 6] <dec loop>]
CALL = parse("[9 2 0 1]")                          # invoke arm 2 of the core


def gate(sample):
    return Cell(BATTERY, Cell(sample, 0))          # context = 0


def main():
    sys.setrecursionlimit(1_000_000)               # the pure loop recurses deep
    m = 7
    core = gate(m)

    jets.ENABLED = False
    off = nock(core, CALL)

    jets.ENABLED = True
    jets.reset_warm()
    # %fast hint: transparent (returns the core), warms mug(battery) -> %dec.
    nock(0, Cell(11, Cell(Cell(jets.cord("fast"), jets.cord("dec")), Cell(1, core))))
    on = nock(core, CALL)

    jets.VALIDATE = True
    checked = nock(core, CALL)
    jets.VALIDATE = False

    print(f"dec {m}")
    print(f"  battery mug        : {mug(BATTERY)}")
    print(f"  jets off (formula) : {off}")
    print(f"  jets on  (native)  : {on}")
    print(f"  VALIDATE (both=)   : {checked}")
    assert off == on == checked == m - 1
    print("  ok: native and formula agree")


if __name__ == "__main__":
    main()
