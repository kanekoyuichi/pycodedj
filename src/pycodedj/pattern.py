from __future__ import annotations

# Pattern sentinel values:
# REST means a silent step, TIE extends the previous degree/chord, TRIGGER fires
# the loop/root synth without a scale degree.
REST = -2
TIE = -3
TRIGGER = -1
PatternStep = int | list[int]

_NOTE_MAP = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
_ACCIDENTAL = {"#": 1, "s": 1, "b": -1}


def _tokenize_pattern(pattern_str: str) -> list[str]:
    tokens: list[str] = []
    i = 0
    while i < len(pattern_str):
        char = pattern_str[i]
        if char.isspace():
            i += 1
            continue
        if char == "[":
            end = pattern_str.find("]", i + 1)
            if end == -1:
                raise ValueError("unterminated chord")
            tokens.append(pattern_str[i : end + 1])
            i = end + 1
            continue
        if char == "]":
            raise ValueError("unexpected chord close")
        start = i
        while i < len(pattern_str) and not pattern_str[i].isspace():
            if pattern_str[i] in "[]":
                break
            i += 1
        tokens.append(pattern_str[start:i])
    return tokens


def _parse_degree(token: str) -> int:
    if token.lstrip("-").isdigit():
        degree = int(token)
        if degree < 0:
            raise ValueError(f"negative degree not allowed: {token!r}")
        return degree
    raise ValueError(f"unknown pattern token: {token!r}")


def _parse_chord(token: str) -> list[int]:
    body = token[1:-1].strip()
    if not body:
        raise ValueError("empty chord not allowed")
    chord: list[int] = []
    for part in body.split():
        if part in {".", "x", "~"}:
            raise ValueError(f"invalid chord token: {part!r}")
        if not part.lstrip("-").isdigit():
            raise ValueError(f"invalid chord token: {part!r}")
        degree = int(part)
        if degree < 0:
            raise ValueError(f"negative degree not allowed in chord: {part!r}")
        chord.append(degree)
    return chord


def parse_pattern(pattern_str: str) -> list[PatternStep]:
    """
    "x . x ."  -> [-1, -2, -1, -2]
    "0 . 3 ."  -> [0, -2, 3, -2]
    "0 . [0 3] ~" -> [0, -2, [0, 3], -3]
    """
    steps: list[PatternStep] = []
    for token in _tokenize_pattern(pattern_str):
        if token == ".":
            steps.append(REST)
        elif token == "x":
            steps.append(TRIGGER)
        elif token == "~":
            if not steps or not (
                isinstance(steps[-1], list) or steps[-1] not in {REST, TRIGGER, TIE}
            ):
                raise ValueError("tie must follow a degree or chord")
            steps.append(TIE)
        elif token.startswith("[") and token.endswith("]"):
            steps.append(_parse_chord(token))
        else:
            steps.append(_parse_degree(token))
    return steps


def encode_steps(steps: list[PatternStep]) -> list[int | float | str]:
    encoded: list[int | float | str] = []
    for step in steps:
        if isinstance(step, list):
            encoded.append(len(step))
            encoded.extend(step)
        elif step == REST:
            encoded.append(0)
        elif step == TIE:
            encoded.append(TIE)
        else:
            encoded.extend((1, step))
    return encoded


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
