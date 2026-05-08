from __future__ import annotations

REST = -2
TRIGGER = -1

_NOTE_MAP = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
_ACCIDENTAL = {"#": 1, "s": 1, "b": -1}


def parse_pattern(pattern_str: str) -> list[int]:
    """
    "x . x ."  -> [-1, -2, -1, -2]
    "0 . 3 ."  -> [0, -2, 3, -2]
    """
    steps: list[int] = []
    for token in pattern_str.split():
        if token == ".":
            steps.append(REST)
        elif token == "x":
            steps.append(TRIGGER)
        elif token.lstrip("-").isdigit():
            val = int(token)
            if val < 0:
                raise ValueError(f"negative degree not allowed: {token!r}")
            steps.append(val)
        else:
            raise ValueError(f"unknown pattern token: {token!r}")
    return steps


def root_to_midi(root: str) -> int:
    """
    "C3" -> 48, "A1" -> 33, "Bb2" -> 46
    Convention: C-1=0, C0=12, C4=60 (General MIDI)
    """
    if not root or root[0] not in _NOTE_MAP:
        raise ValueError(f"invalid root: {root!r}")
    note = _NOTE_MAP[root[0]]
    pos = 1
    if pos < len(root) and root[pos] in _ACCIDENTAL:
        note += _ACCIDENTAL[root[pos]]
        pos += 1
    octave_str = root[pos:]
    if not octave_str or not (octave_str.lstrip("-").isdigit()):
        raise ValueError(f"invalid root: {root!r}")
    octave = int(octave_str)
    return (octave + 1) * 12 + note
