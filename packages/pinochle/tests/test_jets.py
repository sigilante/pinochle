"""Jets: a %fast hint [11 [%fast name] core-formula] warms the produced
core's battery; a later Nock 9 into that battery dispatches the native.
Everything stays transparent -- jet(core) == the arm formula."""

import pytest
from pinochle import nock, parse, to_noun, jets, Cell


# A minimal "inc" gate: core = [battery [sample context]] with the $ arm at
# axis 2 computing +sample (+/[6 core]); battery is [4 0 6].
def _inc_gate(sample):
    return to_noun(((4, 0, 6), (sample, 0)))


def _fast(name_cord, core_formula):
    """Build [11 [%fast name] core-formula]."""
    return Cell(11, Cell(Cell(jets.cord("fast"), name_cord), core_formula))


@pytest.fixture(autouse=True)
def _clean_warm():
    jets.reset_warm()
    yield
    jets.reset_warm()


def test_fast_registers_and_dispatches():
    calls = []

    def inc(core):
        calls.append(core)
        return int(core.tail.head) + 1        # sample at +6

    jets.register("inc", inc)
    try:
        core = _inc_gate(5)
        # %fast is transparent: it produces the core...
        assert nock(0, _fast(jets.cord("inc"), Cell(1, core))) == core
        # ...and warms the battery, so invoking arm 2 dispatches the native.
        assert nock(core, parse("[9 2 0 1]")) == 6
        assert calls, "native was not dispatched"
    finally:
        del jets.REGISTRY[jets.cord("inc")]


def test_core_clue_head_is_the_name():
    calls = []
    jets.register("inc", lambda core: calls.append(1) or int(core.tail.head) + 1)
    try:
        core = _inc_gate(5)
        clue = to_noun((jets.cord("inc"), 0, 0))   # [name parent hooks]
        nock(0, _fast(clue, Cell(1, core)))
        assert nock(core, parse("[9 2 0 1]")) == 6
        assert calls
    finally:
        del jets.REGISTRY[jets.cord("inc")]


def test_unwarmed_battery_runs_the_arm_formula():
    # Never %fast-registered: plain Nock 9 arm evaluation, +sample = 6.
    assert nock(_inc_gate(5), parse("[9 2 0 1]")) == 6
    assert not jets.WARM


def test_fast_with_unregistered_name_is_a_pure_hint():
    core = _inc_gate(5)
    assert nock(0, _fast(jets.cord("nonesuch"), Cell(1, core))) == core
    assert not jets.WARM                       # nothing warmed
    assert nock(core, parse("[9 2 0 1]")) == 6 # formula path


def test_disabled_never_dispatches():
    calls = []
    jets.register("inc", lambda core: calls.append(1) or int(core.tail.head) + 1)
    try:
        core = _inc_gate(5)
        jets.ENABLED = False
        try:
            assert nock(0, _fast(jets.cord("inc"), Cell(1, core))) == core
            assert not jets.WARM               # warming is gated too
            assert nock(core, parse("[9 2 0 1]")) == 6
            assert not calls, "native ran while jets disabled"
        finally:
            jets.ENABLED = True
    finally:
        del jets.REGISTRY[jets.cord("inc")]


def test_validate_agreement():
    jets.register("inc", lambda core: int(core.tail.head) + 1)   # honest
    try:
        core = _inc_gate(5)
        nock(0, _fast(jets.cord("inc"), Cell(1, core)))
        jets.VALIDATE = True
        try:
            assert nock(core, parse("[9 2 0 1]")) == 6
        finally:
            jets.VALIDATE = False
    finally:
        del jets.REGISTRY[jets.cord("inc")]


def test_validate_catches_a_lying_jet():
    jets.register("inc", lambda core: int(core.tail.head) + 100)  # wrong
    try:
        core = _inc_gate(5)
        nock(0, _fast(jets.cord("inc"), Cell(1, core)))
        jets.VALIDATE = True
        try:
            with pytest.raises(Exception):
                nock(core, parse("[9 2 0 1]"))
        finally:
            jets.VALIDATE = False
    finally:
        del jets.REGISTRY[jets.cord("inc")]


# --- built-in natives read the sample at +6 -----------------------------

def test_builtin_dec_reads_sample():
    core = to_noun(((0, 0), (9, 0)))            # [battery [sample=9 ctx=0]]
    assert jets.REGISTRY[jets.cord("dec")](core) == 8

def test_builtin_dec_zero_crashes():
    core = to_noun(((0, 0), (0, 0)))
    with pytest.raises(Exception):
        jets.REGISTRY[jets.cord("dec")](core)

def test_builtin_add_reads_sample():
    core = to_noun(((0, 0), ((3, 4), 0)))       # sample = [3 4]
    assert jets.REGISTRY[jets.cord("add")](core) == 7


# --- %slog (unchanged dynamic hint) -------------------------------------

def test_slog_emits_clue_and_stays_transparent():
    # [11 [%slog c] d]: clue *[a c] = [priority tank], body *[a d] = 99.
    formula = "[11 [%slog [1 1 42]] [1 99]]"     # clue [1 42], body 99
    captured = []
    old = jets.SLOG
    jets.SLOG = captured.append
    try:
        assert nock(0, parse(formula)) == 99
        assert captured == [to_noun((1, 42))]
    finally:
        jets.SLOG = old

def test_slog_default_sink_writes_stderr(capsys):
    assert nock(0, parse("[11 [%slog [1 1 42]] [1 99]]")) == 99
    assert "42" in capsys.readouterr().err

def test_other_dynamic_hint_is_silent_noop():
    captured = []
    old = jets.SLOG
    jets.SLOG = captured.append
    try:
        assert nock(0, parse("[11 [%memo [1 1 42]] [1 99]]")) == 99
        assert captured == []
    finally:
        jets.SLOG = old
