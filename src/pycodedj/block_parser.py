from __future__ import annotations

import ast
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


def _extract_loop_decorator(node: ast.FunctionDef) -> tuple[str, float] | None:
    for dec in node.decorator_list:
        if not isinstance(dec, ast.Call):
            continue
        if not (isinstance(dec.func, ast.Name) and dec.func.id == "loop"):
            continue
        if not dec.args:
            continue
        name_node = dec.args[0]
        if not isinstance(name_node, ast.Constant) or not isinstance(name_node.value, str):
            continue
        interval = _DEFAULT_INTERVAL
        for kw in dec.keywords:
            if kw.arg == "interval" and isinstance(kw.value, ast.Constant):
                interval = float(kw.value.value)
        return name_node.value, interval
    return None


def _default_arg_map(node: ast.FunctionDef) -> dict[str, object]:
    args = node.args.args
    defaults = node.args.defaults
    offset = len(args) - len(defaults)
    values: dict[str, object] = {}
    for i, default in enumerate(defaults):
        if isinstance(default, ast.Constant):
            values[args[offset + i].arg] = default.value
    return values


def _optional_float(value: object) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    return None


def parse_blocks(source: str) -> list[LoopBlock]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    lines = source.splitlines(keepends=True)
    blocks: list[LoopBlock] = []

    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        result = _extract_loop_decorator(node)
        if result is None:
            continue
        loop_name, interval = result
        arg_defaults = _default_arg_map(node)
        volume = _optional_float(arg_defaults.get("volume"))
        eq = arg_defaults.get("eq")
        func_source = "".join(lines[node.lineno - 1 : node.end_lineno])
        blocks.append(LoopBlock(
            name=loop_name,
            interval=interval,
            source=func_source,
            volume=volume if volume is not None else _DEFAULT_VOLUME,
            eq=eq if isinstance(eq, str) else _DEFAULT_EQ,
            low=_optional_float(arg_defaults.get("low")),
            mid=_optional_float(arg_defaults.get("mid")),
            high=_optional_float(arg_defaults.get("high")),
        ))

    return blocks
