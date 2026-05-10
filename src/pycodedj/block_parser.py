from __future__ import annotations

import ast
from collections.abc import Iterator
from dataclasses import dataclass

_DEFAULT_INTERVAL = 1.0
_DEFAULT_VOLUME = 0.3
_DEFAULT_EQ = "flat"


@dataclass
class LoopBlock:
    name: str
    interval: float
    source: str
    volume: float = _DEFAULT_VOLUME
    eq: str = _DEFAULT_EQ
    low: float | None = None
    mid: float | None = None
    high: float | None = None
    cutoff: float | None = None
    reverb: float | None = None
    # S2-1: @loop デコレータ拡張
    synth: str | None = None
    root: str | None = None
    scale: str | None = None
    dur: float | None = None
    # S2-2a: pattern() 呼び出し
    pattern_str: str | None = None


def _extract_loop_decorator(
    node: ast.FunctionDef,
) -> tuple[str, float, dict[str, object]] | None:
    """@loop デコレータを探し (name, interval, kwargs) を返す。なければ None。"""
    for dec in node.decorator_list:
        if not isinstance(dec, ast.Call):
            continue
        if not (isinstance(dec.func, ast.Name) and dec.func.id == "loop"):
            continue

        loop_name = node.name
        if dec.args:
            name_node = dec.args[0]
            if not isinstance(name_node, ast.Constant) or not isinstance(name_node.value, str):
                continue
            loop_name = name_node.value
        if len(dec.args) > 1:
            continue

        interval = _DEFAULT_INTERVAL
        kwargs: dict[str, object] = {}
        for kw in dec.keywords:
            if not isinstance(kw.value, ast.Constant):
                continue
            if kw.arg == "interval":
                interval = float(kw.value.value)
            elif kw.arg in ("synth", "root", "scale"):
                if isinstance(kw.value.value, str):
                    kwargs[kw.arg] = kw.value.value
            elif kw.arg == "dur":
                if isinstance(kw.value.value, (int, float)):
                    kwargs["dur"] = float(kw.value.value)
            elif kw.arg == "beat":
                if isinstance(kw.value.value, (int, float)):
                    kwargs["dur"] = float(kw.value.value)
        return loop_name, interval, kwargs
    return None


def _optional_float(value: object) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _optional_str(value: object) -> str | None:
    if isinstance(value, str):
        return value
    return None


def _walk_body(node: ast.FunctionDef) -> Iterator[ast.AST]:
    """関数本体をネストされたスコープを除き、DFS preorder（ソース順）で走査する。"""
    stack: list[ast.AST] = list(reversed(node.body))
    while stack:
        item = stack.pop()
        yield item
        if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            stack.extend(reversed(list(ast.iter_child_nodes(item))))


def _extract_pattern_call(node: ast.FunctionDef) -> str | None:
    """関数本体から最初の pattern("...") 呼び出しを探して文字列を返す。"""
    for child in _walk_body(node):
        if (
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Name)
            and child.func.id == "pattern"
            and child.args
            and isinstance(child.args[0], ast.Constant)
            and isinstance(child.args[0].value, str)
        ):
            return child.args[0].value
    return None


def _extract_dj_assignments(node: ast.FunctionDef) -> dict[str, object]:
    dj_attrs = {"volume", "eq", "low", "mid", "high", "pattern", "cutoff", "reverb"}
    values: dict[str, object] = {}
    for child in _walk_body(node):
        if not isinstance(child, ast.Assign):
            continue
        for target in child.targets:
            if (
                isinstance(target, ast.Attribute)
                and isinstance(target.value, ast.Name)
                and target.value.id == "dj"
                and target.attr in dj_attrs
                and target.attr not in values
                and isinstance(child.value, ast.Constant)
            ):
                values[target.attr] = child.value.value
    return values


@dataclass
class ParseResult:
    ok: bool
    blocks: list[LoopBlock]
    error: SyntaxError | None = None


def parse_blocks(source: str) -> ParseResult:
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return ParseResult(ok=False, blocks=[], error=e)

    lines = source.splitlines(keepends=True)
    blocks: list[LoopBlock] = []

    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        result = _extract_loop_decorator(node)
        if result is None:
            continue
        loop_name, interval, loop_kwargs = result
        dj_values = _extract_dj_assignments(node)
        volume = _optional_float(dj_values.get("volume"))
        eq = dj_values.get("eq")
        func_source = "".join(lines[node.lineno - 1 : node.end_lineno])
        blocks.append(LoopBlock(
            name=loop_name,
            interval=interval,
            source=func_source,
            volume=volume if volume is not None else _DEFAULT_VOLUME,
            eq=eq if isinstance(eq, str) else _DEFAULT_EQ,
            low=_optional_float(dj_values.get("low")),
            mid=_optional_float(dj_values.get("mid")),
            high=_optional_float(dj_values.get("high")),
            cutoff=_optional_float(dj_values.get("cutoff")),
            reverb=_optional_float(dj_values.get("reverb")),
            synth=_optional_str(loop_kwargs.get("synth")),
            root=_optional_str(loop_kwargs.get("root")),
            scale=_optional_str(loop_kwargs.get("scale")),
            dur=_optional_float(loop_kwargs.get("dur")),
            pattern_str=_optional_str(dj_values.get("pattern")) or _extract_pattern_call(node),
        ))

    return ParseResult(ok=True, blocks=blocks)
