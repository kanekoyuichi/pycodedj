from __future__ import annotations

from typing import Any, Callable


def loop(
    name: str,
    interval: float = 1.0,
    synth: str | None = None,
    root: str | None = None,
    scale: str | None = None,
    dur: float | None = None,
) -> Callable[..., Any]:
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        return fn
    return decorator


def pattern(pattern_str: str) -> None:
    """実行時 no-op。AST 解析で抽出される。"""
