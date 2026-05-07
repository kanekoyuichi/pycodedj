from __future__ import annotations

from typing import Any, Callable


def loop(name: str, interval: float = 1.0) -> Callable[..., Any]:
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        return fn
    return decorator
