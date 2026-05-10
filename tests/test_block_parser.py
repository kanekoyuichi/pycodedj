from pycodedj.block_parser import ParseResult, parse_blocks

_MULTI = """\
from pycodedj import loop

@loop("bass", interval=2.0)
def my_bass():
    pass

@loop("melody", interval=0.5)
def my_melody():
    return 1
"""

_NO_INTERVAL = """\
@loop("pad")
def my_pad():
    pass
"""

_NO_MARKER = """\
x = 1
y = 2
"""

_WITH_VOLUME = """\
@loop("kick", interval=1.0)
def my_kick(volume=0.8):
    pass
"""

_WITH_EQ = """\
@loop("bass", interval=0.5)
def my_bass(volume=0.5, eq="edm", low=1.5, high=0.8):
    pass
"""

_NO_VOLUME = """\
@loop("hat")
def my_hat():
    pass
"""

_MIXED = """\
@loop("bass", interval=2.0)
def the_bass(volume=0.6):
    for i in range(4):
        pass

def helper():
    pass

@loop("lead", interval=1.0)
def the_lead(volume=0.3):
    pass
"""

_SYNTAX_ERROR = "def foo(:"


def test_multiple_blocks() -> None:
    blocks = parse_blocks(_MULTI).blocks
    assert len(blocks) == 2
    assert blocks[0].name == "bass"
    assert blocks[1].name == "melody"


def test_interval_parsed() -> None:
    blocks = parse_blocks(_MULTI).blocks
    assert blocks[0].interval == 2.0
    assert blocks[1].interval == 0.5


def test_interval_default() -> None:
    blocks = parse_blocks(_NO_INTERVAL).blocks
    assert len(blocks) == 1
    assert blocks[0].interval == 1.0


def test_no_marker_returns_empty() -> None:
    assert parse_blocks(_NO_MARKER).blocks == []


def test_empty_source_returns_empty() -> None:
    assert parse_blocks("").blocks == []


def test_syntax_error_returns_empty() -> None:
    assert parse_blocks(_SYNTAX_ERROR).blocks == []


def test_volume_extracted() -> None:
    blocks = parse_blocks(_WITH_VOLUME).blocks
    assert len(blocks) == 1
    assert blocks[0].volume == 0.3


def test_eq_defaults_extracted() -> None:
    blocks = parse_blocks(_WITH_EQ).blocks
    assert len(blocks) == 1
    assert blocks[0].eq == "flat"
    assert blocks[0].low is None
    assert blocks[0].mid is None
    assert blocks[0].high is None


def test_volume_default() -> None:
    blocks = parse_blocks(_NO_VOLUME).blocks
    assert len(blocks) == 1
    assert blocks[0].volume == 0.3
    assert blocks[0].eq == "flat"
    assert blocks[0].low is None
    assert blocks[0].mid is None
    assert blocks[0].high is None


def test_non_loop_functions_ignored() -> None:
    blocks = parse_blocks(_MIXED).blocks
    assert len(blocks) == 2
    assert blocks[0].name == "bass"
    assert blocks[1].name == "lead"


def test_source_contains_function() -> None:
    blocks = parse_blocks(_MULTI).blocks
    assert "def my_bass" in blocks[0].source
    assert "def my_bass" not in blocks[1].source


def test_block_volume_and_interval() -> None:
    blocks = parse_blocks(_MIXED).blocks
    assert blocks[0].volume == 0.3
    assert blocks[0].interval == 2.0
    assert blocks[1].volume == 0.3
    assert blocks[1].interval == 1.0


def test_syntax_error_ok_is_false() -> None:
    assert parse_blocks(_SYNTAX_ERROR).ok is False


def test_syntax_error_has_error_field() -> None:
    assert isinstance(parse_blocks(_SYNTAX_ERROR).error, SyntaxError)


def test_valid_source_ok_is_true() -> None:
    assert parse_blocks("def f(): pass").ok is True


def test_valid_source_error_is_none() -> None:
    assert parse_blocks("def f(): pass").error is None


def test_parse_result_type() -> None:
    assert isinstance(parse_blocks(_MULTI), ParseResult)


# --- Sprint 2: @loop synth/root/scale/dur ---

_WITH_SYNTH_PARAMS = """\
from pycodedj import loop

@loop("kick", synth="kick_pulse", root="C2", scale="minor", dur=0.25)
def my_kick():
    pass
"""

_WITH_PARTIAL_PARAMS = """\
from pycodedj import loop

@loop("bass", synth="bass_reese", dur=0.5)
def my_bass():
    pass
"""

_WITH_FUNCTION_NAME_LOOP = """\
from pycodedj import loop

@loop(synth="bass_acid", root="A1", scale="minor", beat=0.25)
def bass():
    pass
"""


def test_synth_extracted() -> None:
    blocks = parse_blocks(_WITH_SYNTH_PARAMS).blocks
    assert len(blocks) == 1
    assert blocks[0].synth == "kick_pulse"


def test_root_extracted() -> None:
    blocks = parse_blocks(_WITH_SYNTH_PARAMS).blocks
    assert blocks[0].root == "C2"


def test_scale_extracted() -> None:
    blocks = parse_blocks(_WITH_SYNTH_PARAMS).blocks
    assert blocks[0].scale == "minor"


def test_dur_extracted() -> None:
    blocks = parse_blocks(_WITH_SYNTH_PARAMS).blocks
    assert blocks[0].dur == 0.25


def test_synth_without_root_scale() -> None:
    blocks = parse_blocks(_WITH_PARTIAL_PARAMS).blocks
    assert blocks[0].synth == "bass_reese"
    assert blocks[0].root is None
    assert blocks[0].scale is None
    assert blocks[0].dur == 0.5


def test_loop_name_defaults_to_function_name() -> None:
    blocks = parse_blocks(_WITH_FUNCTION_NAME_LOOP).blocks
    assert len(blocks) == 1
    assert blocks[0].name == "bass"


def test_beat_alias_sets_dur() -> None:
    blocks = parse_blocks(_WITH_FUNCTION_NAME_LOOP).blocks
    assert blocks[0].dur == 0.25


def test_new_fields_default_to_none() -> None:
    blocks = parse_blocks(_NO_VOLUME).blocks
    assert blocks[0].synth is None
    assert blocks[0].root is None
    assert blocks[0].scale is None
    assert blocks[0].dur is None
    assert blocks[0].pattern_str is None
    assert blocks[0].cutoff is None
    assert blocks[0].reverb is None


# --- Sprint 2: pattern() extraction ---

_WITH_PATTERN = """\
from pycodedj import loop, pattern

@loop("kick", synth="kick_pulse", dur=0.25)
def my_kick():
    pattern("x . x .")
"""

_WITH_PATTERN_AND_DEGREE = """\
from pycodedj import loop, pattern

@loop("bass", synth="bass_acid", root="A1", scale="minor", dur=0.25)
def my_bass():
    pattern("0 . 3 .")
"""


def test_pattern_str_extracted() -> None:
    blocks = parse_blocks(_WITH_PATTERN).blocks
    assert blocks[0].pattern_str == "x . x ."


def test_pattern_str_with_degrees() -> None:
    blocks = parse_blocks(_WITH_PATTERN_AND_DEGREE).blocks
    assert blocks[0].pattern_str == "0 . 3 ."


def test_pattern_str_none_when_absent() -> None:
    blocks = parse_blocks(_WITH_SYNTH_PARAMS).blocks
    assert blocks[0].pattern_str is None


_WITH_NESTED_PATTERN = """\
from pycodedj import loop, pattern

@loop("bass", synth="bass_acid", dur=0.25)
def my_bass():
    def helper():
        pattern("x . x .")  # inside nested function — should be ignored
    helper()
"""


def test_pattern_str_ignores_nested_scope() -> None:
    blocks = parse_blocks(_WITH_NESTED_PATTERN).blocks
    assert blocks[0].pattern_str is None


_WITH_MULTIPLE_PATTERNS = """\
from pycodedj import loop, pattern

@loop("kick", dur=0.25)
def my_kick():
    pattern("x . x .")
    if True:
        pattern("x x . .")
"""


def test_pattern_str_takes_first_in_source_order() -> None:
    blocks = parse_blocks(_WITH_MULTIPLE_PATTERNS).blocks
    assert blocks[0].pattern_str == "x . x ."


# --- dj namespace metadata ---

_WITH_DJ_METADATA = """\
from pycodedj import dj, loop

@loop(synth="bass_acid", root="A1", scale="minor", beat=0.25)
def bass(volume=0.9):
    dj.volume = 0.35
    dj.eq = "edm"
    dj.low = 1.7
    dj.mid = 0.78
    dj.high = 0.82
    dj.cutoff = 1800
    dj.reverb = 0.35
    dj.pattern = "0 . [0 3] ~ 5 . 3 ."
"""

_WITH_DJ_PATTERN_NAME = """\
from pycodedj import dj, loop

p1 = "0 . 3 ."

@loop(synth="bass_acid")
def bass():
    dj.pattern = p1
"""

_WITH_NESTED_DJ_METADATA = """\
from pycodedj import dj, loop

@loop(synth="bass_acid")
def bass():
    def helper():
        dj.volume = 0.9
        dj.pattern = "x . x ."
    helper()
"""


def test_dj_volume_extracted() -> None:
    blocks = parse_blocks(_WITH_DJ_METADATA).blocks
    assert blocks[0].volume == 0.35


def test_dj_eq_extracted() -> None:
    blocks = parse_blocks(_WITH_DJ_METADATA).blocks
    assert blocks[0].eq == "edm"
    assert blocks[0].low == 1.7
    assert blocks[0].mid == 0.78
    assert blocks[0].high == 0.82


def test_dj_cutoff_reverb_extracted() -> None:
    blocks = parse_blocks(_WITH_DJ_METADATA).blocks
    assert blocks[0].cutoff == 1800.0
    assert blocks[0].reverb == 0.35


def test_dj_pattern_extracted() -> None:
    blocks = parse_blocks(_WITH_DJ_METADATA).blocks
    assert blocks[0].pattern_str == "0 . [0 3] ~ 5 . 3 ."


def test_dj_pattern_name_is_ignored() -> None:
    blocks = parse_blocks(_WITH_DJ_PATTERN_NAME).blocks
    assert blocks[0].pattern_str is None


def test_dj_metadata_ignores_nested_scope() -> None:
    blocks = parse_blocks(_WITH_NESTED_DJ_METADATA).blocks
    assert blocks[0].volume == 0.3
    assert blocks[0].pattern_str is None
    assert blocks[0].cutoff is None
    assert blocks[0].reverb is None


def test_dj_pattern_preferred_over_pattern_call() -> None:
    source = """\
from pycodedj import dj, loop, pattern

@loop(synth="bass_acid")
def bass():
    dj.pattern = "0 . 3 ."
    pattern("x . x .")
"""
    blocks = parse_blocks(source).blocks
    assert blocks[0].pattern_str == "0 . 3 ."
