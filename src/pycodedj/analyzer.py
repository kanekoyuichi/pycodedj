from __future__ import annotations

import ast
import io
import tokenize
from dataclasses import dataclass


@dataclass
class CodeFeatures:
    max_depth: int
    control_flow_count: int
    function_count: int
    comment_ratio: float


# ブロック構造ノードだけをネスト深さとしてカウントする。
# BinOp・Call など式ノードは含めない（式の複雑さではなく制御構造の深さを測る）。
_BLOCK_NODES = (
    ast.If, ast.For, ast.While, ast.With,
    ast.Try, ast.FunctionDef, ast.AsyncFunctionDef,
    ast.ClassDef, ast.ExceptHandler,
)


def _ast_depth(node: ast.AST, current: int = 0) -> int:
    children = list(ast.iter_child_nodes(node))
    if not children:
        return current
    next_depth = current + 1 if isinstance(node, _BLOCK_NODES) else current
    return max(_ast_depth(child, next_depth) for child in children)


def _count_nodes(tree: ast.AST, *types: type) -> int:
    return sum(isinstance(node, types) for node in ast.walk(tree))


def _comment_ratio(source: str) -> float:
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    comment_count = 0
    try:
        for tok in tokens:
            if tok.type == tokenize.COMMENT:
                comment_count += 1
    except tokenize.TokenError:
        pass

    total_non_blank = sum(1 for line in source.splitlines() if line.strip())
    if total_non_blank == 0:
        return 0.0
    return comment_count / total_non_blank


def analyze(source: str) -> CodeFeatures:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        raise

    return CodeFeatures(
        max_depth=_ast_depth(tree),
        control_flow_count=_count_nodes(tree, ast.If, ast.For, ast.While),
        function_count=_count_nodes(tree, ast.FunctionDef, ast.AsyncFunctionDef),
        comment_ratio=_comment_ratio(source),
    )
