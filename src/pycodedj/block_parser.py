from __future__ import annotations

import ast
from dataclasses import dataclass

_DEFAULT_INTERVAL = 1.0
_DEFAULT_VOLUME = 0.3


@dataclass
class LoopBlock:
    name: str
    interval: float
    source: str
    volume: float = _DEFAULT_VOLUME


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


def _extract_volume(node: ast.FunctionDef) -> float:
    args = node.args.args
    defaults = node.args.defaults
    offset = len(args) - len(defaults)
    for i, default in enumerate(defaults):
        if args[offset + i].arg == "volume" and isinstance(default, ast.Constant):
            return float(default.value)
    return _DEFAULT_VOLUME


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
        volume = _extract_volume(node)
        func_source = "".join(lines[node.lineno - 1 : node.end_lineno])
        blocks.append(LoopBlock(
            name=loop_name,
            interval=interval,
            source=func_source,
            volume=volume,
        ))

    return blocks
