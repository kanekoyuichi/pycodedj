import pytest

from pycodedj.pattern import REST, TIE, TRIGGER, encode_steps, parse_pattern, root_to_midi


# --- parse_pattern ---

def test_rest_dot() -> None:
    assert parse_pattern(".") == [REST]


def test_trigger_x() -> None:
    assert parse_pattern("x") == [TRIGGER]


def test_degree_zero() -> None:
    assert parse_pattern("0") == [0]


def test_degree_positive() -> None:
    assert parse_pattern("3") == [3]


def test_degree_negative_raises() -> None:
    with pytest.raises(ValueError, match="negative degree not allowed"):
        parse_pattern("-1")


def test_mixed_pattern() -> None:
    assert parse_pattern("x . x .") == [TRIGGER, REST, TRIGGER, REST]


def test_degree_pattern() -> None:
    assert parse_pattern("0 . 3 .") == [0, REST, 3, REST]


def test_chord_pattern() -> None:
    assert parse_pattern("[0 3]") == [[0, 3]]


def test_chord_mixed_pattern() -> None:
    assert parse_pattern("0 . [0 3] ~ 5 . 3 .") == [0, REST, [0, 3], TIE, 5, REST, 3, REST]


def test_tie_after_degree() -> None:
    assert parse_pattern("0 ~") == [0, TIE]


def test_tie_after_chord() -> None:
    assert parse_pattern("[0 3] ~") == [[0, 3], TIE]


def test_longer_pattern() -> None:
    result = parse_pattern("x x . x . . x .")
    assert result == [TRIGGER, TRIGGER, REST, TRIGGER, REST, REST, TRIGGER, REST]


def test_single_rest() -> None:
    assert parse_pattern(".") == [-2]


def test_rest_constant_value() -> None:
    assert REST == -2


def test_trigger_constant_value() -> None:
    assert TRIGGER == -1


def test_tie_constant_value() -> None:
    assert TIE == -3


def test_unknown_token_raises() -> None:
    with pytest.raises(ValueError, match="unknown pattern token"):
        parse_pattern("x y .")


def test_leading_tie_raises() -> None:
    with pytest.raises(ValueError, match="tie must follow"):
        parse_pattern("~")


def test_rest_then_tie_raises() -> None:
    with pytest.raises(ValueError, match="tie must follow"):
        parse_pattern(". ~")


def test_trigger_then_tie_raises() -> None:
    with pytest.raises(ValueError, match="tie must follow"):
        parse_pattern("x ~")


def test_empty_chord_raises() -> None:
    with pytest.raises(ValueError, match="empty chord"):
        parse_pattern("[]")


@pytest.mark.parametrize("token", ["x", ".", "~"])
def test_chord_special_token_raises(token: str) -> None:
    with pytest.raises(ValueError, match="invalid chord token"):
        parse_pattern(f"[0 {token}]")


def test_chord_negative_degree_raises() -> None:
    with pytest.raises(ValueError, match="negative degree not allowed in chord"):
        parse_pattern("[0 -3]")


def test_empty_string_returns_empty() -> None:
    assert parse_pattern("") == []


def test_whitespace_only_returns_empty() -> None:
    assert parse_pattern("   ") == []


# --- encode_steps ---

def test_encode_steps_rest() -> None:
    assert encode_steps([REST]) == [0]


def test_encode_steps_tie() -> None:
    assert encode_steps([TIE]) == [TIE]


def test_encode_steps_trigger() -> None:
    assert encode_steps([TRIGGER]) == [1, TRIGGER]


def test_encode_steps_note() -> None:
    assert encode_steps([3]) == [1, 3]


def test_encode_steps_chord() -> None:
    assert encode_steps([[0, 3]]) == [2, 0, 3]


def test_encode_steps_acceptance_pattern() -> None:
    steps = parse_pattern("0 . [0 3] ~ 5 . 3 .")
    assert encode_steps(steps) == [1, 0, 0, 2, 0, 3, TIE, 1, 5, 0, 1, 3, 0]


# --- root_to_midi ---

def test_c4() -> None:
    assert root_to_midi("C4") == 60


def test_a4() -> None:
    assert root_to_midi("A4") == 69


def test_c0() -> None:
    assert root_to_midi("C0") == 12


def test_c_minus1() -> None:
    assert root_to_midi("C-1") == 0


def test_a1() -> None:
    assert root_to_midi("A1") == 33


def test_c3() -> None:
    assert root_to_midi("C3") == 48


def test_sharp() -> None:
    assert root_to_midi("C#4") == 61


def test_flat_b() -> None:
    assert root_to_midi("Bb2") == 46


def test_sharp_s() -> None:
    assert root_to_midi("Cs4") == 61


def test_d4() -> None:
    assert root_to_midi("D4") == 62


def test_e4() -> None:
    assert root_to_midi("E4") == 64


def test_f4() -> None:
    assert root_to_midi("F4") == 65


def test_g4() -> None:
    assert root_to_midi("G4") == 67


def test_b4() -> None:
    assert root_to_midi("B4") == 71


def test_invalid_note_raises() -> None:
    with pytest.raises(ValueError, match="invalid root"):
        root_to_midi("X4")


def test_invalid_no_octave_raises() -> None:
    with pytest.raises(ValueError, match="invalid root"):
        root_to_midi("C")


def test_empty_raises() -> None:
    with pytest.raises(ValueError, match="invalid root"):
        root_to_midi("")
