"""Parsing of %constants (@tas terms), alongside the existing number syntax."""

import pytest
from pinochle import parse, Cell, jets


def _cord(s):
    return int.from_bytes(s.encode(), "little")


def test_term_is_little_endian_cord():
    assert parse("%dec") == _cord("dec")
    assert parse("%fast") == _cord("fast")
    # agrees with the jet layer's own cord() helper
    assert parse("%dec") == jets.cord("dec")


def test_percent_number_is_that_number():
    assert parse("%42") == 42
    assert parse("%0") == 0


def test_term_allows_dot_and_dash_literally():
    assert parse("%foo-bar") == _cord("foo-bar")
    assert parse("%.y") == _cord(".y")          # dot is term text here, not a sep


def test_number_dot_is_still_a_separator():
    assert parse("1.024") == 1024               # unchanged number syntax


def test_term_inside_a_cell():
    x = parse("[%fast %dec]")
    assert x == Cell(_cord("fast"), _cord("dec"))
    y = parse("[1 %dec]")
    assert y == Cell(1, _cord("dec"))


def test_percent_requires_a_token_boundary():
    with pytest.raises(ValueError):
        parse("5%foo")                          # % mid-number is illegal
