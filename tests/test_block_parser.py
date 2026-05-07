from pycodedj.block_parser import parse_blocks


_MULTI = """\
# @loop bass interval=2.0
def bass():
    pass

# @loop melody interval=0.5
def melody():
    return 1
"""

_NO_INTERVAL = """\
# @loop pad
def pad():
    pass
"""

_NO_MARKER = """\
x = 1
y = 2
"""

_MARKER_THEN_BARE = """\
# @loop solo
def solo(): pass
"""


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


def test_source_excludes_marker_line() -> None:
    blocks = parse_blocks(_MARKER_THEN_BARE)
    assert "# @loop" not in blocks[0].source


def test_block_source_content() -> None:
    blocks = parse_blocks(_MULTI)
    assert "def bass" in blocks[0].source
    assert "def melody" not in blocks[0].source
