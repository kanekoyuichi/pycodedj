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
    assert blocks[0].volume == 0.8


def test_eq_defaults_extracted() -> None:
    blocks = parse_blocks(_WITH_EQ).blocks
    assert len(blocks) == 1
    assert blocks[0].eq == "edm"
    assert blocks[0].low == 1.5
    assert blocks[0].mid is None
    assert blocks[0].high == 0.8


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
    assert blocks[0].volume == 0.6
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
