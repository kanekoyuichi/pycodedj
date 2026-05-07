from __future__ import annotations

import sys
from dataclasses import dataclass, field

from .analyzer import analyze
from .block_parser import LoopBlock
from .mapper import MusicParams, map_features
from .osc_bridge import OscBridge, OscError


@dataclass
class Engine:
    bridge: OscBridge
    _loops: dict[str, MusicParams] = field(default_factory=dict, init=False, repr=False)

    def eval_block(self, block: LoopBlock) -> MusicParams | None:
        try:
            features = analyze(block.source)
            params = map_features(features)
            self.bridge.send_params(block.name, params)
            self._loops[block.name] = params
            return params
        except SyntaxError as e:
            sys.stderr.write(f"[pycodedj] syntax error ({block.name}): {e}\n")
        except OscError as e:
            sys.stderr.write(f"[pycodedj] OSC send failed ({block.name}): {e}\n")
        return None

    def stop_loop(self, name: str) -> None:
        self._loops.pop(name, None)
        stop_params = MusicParams(cutoff=200.0, lfo_rate=0.1, reverb_mix=0.0, voice_count=0)
        self.bridge.send_params(name, stop_params)

    def list_loops(self) -> list[str]:
        return list(self._loops.keys())
