import pytest
from noun import *

# Test to_noun conversions
def test_to_noun_int():
    n = to_noun(5)
    assert n.value == 5
    assert isatom(n) == tru

def test_to_noun_negative_fails():
    with pytest.raises(ValueError):
        to_noun(-5)

def test_to_noun_pair():
    n = to_noun((3, 4))
    assert isatom(n) == bad
    assert head(n).value == 3
    assert tail(n).value == 4

def test_to_noun_right_branching():
    n = to_noun((3, 4, 5))
    assert head(n).value == 3
    assert head(tail(n)).value == 4
    assert tail(tail(n)).value == 5

def test_to_noun_long_right_branching():
    n = to_noun((1, 2, 3, 4, 5))
    # Should be (1, (2, (3, (4, 5))))
    assert head(n).value == 1
    assert head(tail(n)).value == 2
    assert head(tail(tail(n))).value == 3
    assert head(tail(tail(tail(n)))).value == 4
    assert tail(tail(tail(tail(n)))).value == 5

def test_to_noun_preserves_left_structure():
    n = to_noun(((3, 4), 5))
    left = head(n)
    assert head(left).value == 3
    assert tail(left).value == 4
    assert tail(n).value == 5

# Test isatom and iscell
def test_isatom_on_atom():
    assert isatom(5) == tru

def test_isatom_on_cell():
    assert isatom((3, 4)) == bad

def test_iscell_on_cell():
    assert iscell((3, 4)) == tru

def test_iscell_on_atom():
    assert iscell(5) == bad

# Test wut
def test_wut():
    assert wut((3, 4)) == tru
    assert wut(5) == bad

# Test head and tail
def test_head():
    assert head((10, 20)).value == 10

def test_head_on_atom_fails():
    with pytest.raises(Exception):
        head(5)

def test_tail():
    assert tail((10, 20)).value == 20

def test_tail_on_atom_fails():
    with pytest.raises(Exception):
        tail(5)

# Test lus (increment)
def test_lus():
    assert lus(5).value == 6
    assert lus(0).value == 1
    assert lus(99).value == 100

def test_lus_on_cell_fails():
    with pytest.raises(Exception):
        lus((3, 4))

# Test tis (equality)
def test_tis_equal_atoms():
    assert tis(5, 5) == tru

def test_tis_unequal_atoms():
    assert tis(5, 6) == bad

def test_tis_equal_cells():
    assert tis((3, 4), (3, 4)) == tru

def test_tis_unequal_cells():
    assert tis((3, 4), (3, 5)) == bad

# Test fas (tree navigation)
def test_fas_axis_1():
    assert fas(1, 42).value == 42
    assert fas(1, (10, 20)) == to_noun((10, 20))

def test_fas_axis_2():
    assert fas(2, (10, 20)).value == 10

def test_fas_axis_3():
    assert fas(3, (10, 20)).value == 20

def test_fas_axis_0_fails():
    with pytest.raises(Exception):
        fas(0, 42)

def test_fas_even_recursion():
    # /[4 [[1 2] [3 4]]] = /[2 /[2 [[1 2] [3 4]]]]
    #                     = /[2 [1 2]] = 1
    tree = to_noun(((1, 2), (3, 4)))
    assert fas(4, tree).value == 1

def test_fas_odd_recursion():
    # /[5 [[1 2] [3 4]]] = /[3 /[2 [[1 2] [3 4]]]]
    #                     = /[3 [1 2]] = 2
    tree = to_noun(((1, 2), (3, 4)))
    assert fas(5, tree).value == 2

def test_fas_complex_tree():
    # /[6 [[1 2] [3 4]]] = /[2 /[3 [[1 2] [3 4]]]]
    #                     = /[2 [3 4]] = 3
    tree = to_noun(((1, 2), (3, 4)))
    assert fas(6, tree).value == 3

def test_fas_axis_7():
    # /[7 [[1 2] [3 4]]] = /[3 /[3 [[1 2] [3 4]]]]
    #                     = /[3 [3 4]] = 4
    tree = to_noun(((1, 2), (3, 4)))
    assert fas(7, tree).value == 4

# Test hax (# operator)
def test_hax_axis_1():
    # #[1 a b] = a
    assert hax(1, 10, 20).value == 10

def test_hax_axis_2():
    # #[2 a b] = #[1 [a /[3 b]] b]
    # For simple case: #[2 a [b c]] should give [a c]
    result = hax(2, 5, (10, 20))
    assert head(result).value == 5
    assert tail(result).value == 20

def test_hax_axis_3():
    # #[3 a b] = #[1 [/[2 b] a] b]
    # For simple case: #[3 a [b c]] should give [b a]
    result = hax(3, 5, (10, 20))
    assert head(result).value == 10
    assert tail(result).value == 5

def test_hax_axis_4():
    # #[4 a [[b c] [d e]]]
    tree = to_noun(((1, 2), (3, 4)))
    result = hax(4, 100, tree)
    # Should navigate and reconstruct
    assert isatom(result) == bad

def test_hax_non_atom_axis_fails():
    with pytest.raises(Exception):
        hax((1, 2), 5, 10)

# Run all tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
