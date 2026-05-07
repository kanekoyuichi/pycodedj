from pycodedj.block_parser import parse_blocks

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
    blocks = parse_blocks(_MULTI)
    assert len(blocks) == 2
    assert blocks[0].name == "bass"
    assert blocks[1].name == "melody"


def test_interval_parsed() -> None:
    blocks = parse_blocks(_MULTI)
    assert blocks[0].interval == 2.0
    assert blocks[1].interval == 0.5


def test_interval_default() -> None:
    blocks = parse_blocks(_NO_INTERVAL)
    assert len(blocks) == 1
    assert blocks[0].interval == 1.0


def test_no_marker_returns_empty() -> None:
    assert parse_blocks(_NO_MARKER) == []


def test_empty_source_returns_empty() -> None:
    assert parse_blocks("") == []


def test_syntax_error_returns_empty() -> None:
    assert parse_blocks(_SYNTAX_ERROR) == []


def test_volume_extracted() -> None:
    blocks = parse_blocks(_WITH_VOLUME)
    assert len(blocks) == 1
    assert blocks[0].volume == 0.8


def test_eq_defaults_extracted() -> None:
    blocks = parse_blocks(_WITH_EQ)
    assert len(blocks) == 1
    assert blocks[0].eq == "edm"
    assert blocks[0].low == 1.5
    assert blocks[0].mid is None
    assert blocks[0].high == 0.8


def test_volume_default() -> None:
    blocks = parse_blocks(_NO_VOLUME)
    assert len(blocks) == 1
    assert blocks[0].volume == 0.3
    assert blocks[0].eq == "flat"
    assert blocks[0].low is None
    assert blocks[0].mid is None
    assert blocks[0].high is None


def test_non_loop_functions_ignored() -> None:
    blocks = parse_blocks(_MIXED)
    assert len(blocks) == 2
    assert blocks[0].name == "bass"
    assert blocks[1].name == "lead"


def test_source_contains_function() -> None:
    blocks = parse_blocks(_MULTI)
    assert "def my_bass" in blocks[0].source
    assert "def my_bass" not in blocks[1].source


def test_block_volume_and_interval() -> None:
    blocks = parse_blocks(_MIXED)
    assert blocks[0].volume == 0.6
    assert blocks[0].interval == 2.0
    assert blocks[1].volume == 0.3
    assert blocks[1].interval == 1.0
