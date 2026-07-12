"""Jet dispatch: static opcode-11 hints select native implementations while
remaining semantically transparent (jet(a) == *[a body])."""

import pytest
from pinochle import nock, parse, to_noun, jets


def _run(subj, formula):
    return nock(parse(subj), parse(formula))


def test_unregistered_tag_is_transparent():
    # [11 tag [4 0 1]] with an unregistered tag == *[a 4 0 1] == a + 1.
    assert _run("5", "[11 999999 [4 0 1]]") == 6


def test_jet_dispatches_and_stays_transparent():
    calls = []

    def inc(a):
        calls.append(a)
        return int(a) + 1

    jets.register("inc", inc)
    tag = jets.cord("inc")
    formula = f"[11 {tag} [4 0 1]]"  # body is a genuine increment
    try:
        # ENABLED (default): native runs, agrees with the formula's a+1.
        assert _run("5", formula) == 6
        assert calls, "native jet was not invoked"

        # VALIDATE: both paths run and must agree on every dispatch.
        jets.VALIDATE = True
        try:
            assert _run("41", formula) == 42
        finally:
            jets.VALIDATE = False

        # Disabled: falls through to the formula body, native untouched.
        calls.clear()
        jets.ENABLED = False
        try:
            assert _run("7", formula) == 8
            assert not calls, "native ran while jets disabled"
        finally:
            jets.ENABLED = True
    finally:
        del jets.REGISTRY[tag]


def test_validate_catches_a_lying_jet():
    jets.register("wrong", lambda a: int(a) + 100)
    tag = jets.cord("wrong")
    jets.VALIDATE = True
    try:
        with pytest.raises(Exception):
            _run("5", f"[11 {tag} [4 0 1]]")  # native 105 != formula 6
    finally:
        jets.VALIDATE = False
        del jets.REGISTRY[tag]


def test_builtin_dec_reads_sample():
    # subject [battery sample]; %dec native reads the sample (tail).
    tag = jets.cord("dec")
    assert nock(to_noun((0, 5)), parse(f"[11 {tag} [0 1]]")) == 4


def test_builtin_dec_zero_crashes():
    tag = jets.cord("dec")
    with pytest.raises(Exception):
        nock(to_noun((0, 0)), parse(f"[11 {tag} [0 1]]"))


def test_builtin_add():
    tag = jets.cord("add")
    assert nock(to_noun((0, (3, 4))), parse(f"[11 {tag} [0 1]]")) == 7


def test_slog_emits_clue_and_stays_transparent():
    # [11 [%slog c] d]: clue *[a c] = [priority tank], body *[a d] = 99.
    tag = jets.cord("slog")
    formula = f"[11 [{tag} [1 1 42]] [1 99]]"  # clue [1 42], body 99
    captured = []
    old = jets.SLOG
    jets.SLOG = captured.append
    try:
        assert nock(0, parse(formula)) == 99            # transparent: body wins
        assert captured == [to_noun((1, 42))]           # sink saw [priority tank]
    finally:
        jets.SLOG = old


def test_slog_default_sink_writes_stderr(capsys):
    tag = jets.cord("slog")
    formula = f"[11 [{tag} [1 1 42]] [1 99]]"
    assert nock(0, parse(formula)) == 99
    assert "42" in capsys.readouterr().err


def test_slog_disabled_tag_is_ordinary_hint():
    # A non-slog dynamic hint just evaluates+discards its clue, no output.
    captured = []
    old = jets.SLOG
    jets.SLOG = captured.append
    try:
        assert nock(0, parse("[11 [999999 [1 1 42]] [1 99]]")) == 99
        assert captured == []
    finally:
        jets.SLOG = old
