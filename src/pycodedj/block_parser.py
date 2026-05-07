from __future__ import annotations

import re
from dataclasses import dataclass

_MARKER_RE = re.compile(r"^#\s*@loop\s+(\w+)(?:\s+interval=([\d.]+))?")
_DEFAULT_INTERVAL = 1.0


@dataclass
class LoopBlock:
    name: str
    interval: float
    source: str


def parse_blocks(source: str) -> list[LoopBlock]:
    blocks: list[LoopBlock] = []
    current_name: str | None = None
    current_interval: float = _DEFAULT_INTERVAL
    current_lines: list[str] = []

    for line in source.splitlines(keepends=True):
        m = _MARKER_RE.match(line)
        if m:
            if current_name is not None:
                blocks.append(LoopBlock(
                    name=current_name,
                    interval=current_interval,
                    source="".join(current_lines),
                ))
            current_name = m.group(1)
            current_interval = float(m.group(2)) if m.group(2) else _DEFAULT_INTERVAL
            current_lines = []
        elif current_name is not None:
            current_lines.append(line)

    if current_name is not None:
        blocks.append(LoopBlock(
            name=current_name,
            interval=current_interval,
            source="".join(current_lines),
        ))

    return blocks
