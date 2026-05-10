from __future__ import annotations

from typing import Any, Callable


class _Dj:
    """Runtime no-op namespace for AST-readable music metadata."""

    volume: float | None = None
    eq: str | None = None
    low: float | None = None
    mid: float | None = None
    high: float | None = None
    pattern: str | None = None
    cutoff: float | None = None
    reverb: float | None = None


dj = _Dj()


def loop(
    name: str | None = None,
    interval: float = 1.0,
    synth: str | None = None,
    root: str | None = None,
    scale: str | None = None,
    dur: float | None = None,
    beat: float | None = None,
) -> Callable[..., Any]:
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        return fn
    return decorator


def pattern(pattern_str: str) -> None:
    """実行時 no-op。AST 解析で抽出される。"""
