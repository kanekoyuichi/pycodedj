import pytest

from pycodedj.analyzer import analyze


_SIMPLE = """\
def foo():
    pass
"""

_NESTED = """\
def foo():
    for i in range(4):
        for j in range(4):
            if i == j:
                pass
"""

_COMMENTS_ONLY = """\
# first
# second
# third
"""

_MIXED = """\
# this is a comment
def foo():
    x = 1  # inline
    return x
"""

_MULTI_FUNC = """\
def a(): pass
def b(): pass
def c(): pass
"""

# 式が複雑でもブロック構造が同じなら max_depth は変わらない
_FLAT_SIMPLE = "def f(): pass\n"
_FLAT_EXPR = "def f(): x = 1 + 2 * (3 + (4 - 5))\n"


def test_no_control_flow() -> None:
    f = analyze(_SIMPLE)
    assert f.control_flow_count == 0
    assert f.function_count == 1


def test_nested_control_flow() -> None:
    f = analyze(_NESTED)
    assert f.control_flow_count == 3
    assert f.max_depth >= 4


def test_max_depth_counts_block_structure_only() -> None:
    # 式の複雑さ（BinOp 等）は max_depth に影響しない
    assert analyze(_FLAT_SIMPLE).max_depth == analyze(_FLAT_EXPR).max_depth


def test_max_depth_flat_function() -> None:
    # ブロック構造が FunctionDef だけなら深さは 1
    assert analyze(_FLAT_SIMPLE).max_depth == 1


def test_comment_ratio_comments_only() -> None:
    f = analyze(_COMMENTS_ONLY)
    assert f.comment_ratio == 1.0


def test_comment_ratio_no_comments() -> None:
    f = analyze(_SIMPLE)
    assert f.comment_ratio == 0.0


def test_comment_ratio_mixed() -> None:
    f = analyze(_MIXED)
    assert 0.0 < f.comment_ratio < 1.0


def test_multiple_functions() -> None:
    f = analyze(_MULTI_FUNC)
    assert f.function_count == 3


def test_syntax_error_raises() -> None:
    with pytest.raises(SyntaxError):
        analyze("def foo(:")


def test_empty_source() -> None:
    f = analyze("")
    assert f.max_depth >= 0
    assert f.control_flow_count == 0
    assert f.function_count == 0
    assert f.comment_ratio == 0.0
