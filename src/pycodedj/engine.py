from __future__ import annotations

import dataclasses
import sys
from dataclasses import dataclass, field

from .analyzer import analyze
from .block_parser import LoopBlock
from .mapper import MusicParams, map_features
from .osc_bridge import OscBridge, OscError


@dataclass
class LoopState:
    params: MusicParams
    muted: bool = False
    muted_before_solo: bool = False  # solo 解除時に solo 前の mute 状態を復元するために使用


@dataclass
class LoopStatus:
    name: str
    muted: bool
    amp: float
    cutoff: float


@dataclass
class Engine:
    bridge: OscBridge
    _states: dict[str, LoopState] = field(default_factory=dict, init=False, repr=False)

    def eval_block(self, block: LoopBlock) -> MusicParams | None:
        try:
            features = analyze(block.source)
            params = map_features(
                features,
                volume=block.volume,
                eq=block.eq,
                low=block.low,
                mid=block.mid,
                high=block.high,
            )
            existing = self._states.get(block.name)
            muted = existing.muted if existing is not None else False
            send = dataclasses.replace(params, amp=0.0) if muted else params
            self.bridge.send_params(block.name, send)
            self._states[block.name] = LoopState(params=params, muted=muted)
            return params
        except SyntaxError as e:
            sys.stderr.write(f"[pycodedj] syntax error ({block.name}): {e}\n")
        except OscError as e:
            sys.stderr.write(f"[pycodedj] OSC send failed ({block.name}): {e}\n")
        return None

    def stop_loop(self, name: str) -> None:
        self._states.pop(name, None)
        stop_params = MusicParams(cutoff=200.0, lfo_rate=0.1, reverb_mix=0.0, voice_count=0)
        self.bridge.send_params(name, stop_params)

    def list_loops(self) -> list[str]:
        return list(self._states.keys())

    def mute(self, name: str) -> None:
        if name not in self._states:
            return
        self._states[name].muted = True
        self.bridge.send_params(name, dataclasses.replace(self._states[name].params, amp=0.0))

    def unmute(self, name: str) -> None:
        if name not in self._states:
            return
        self._states[name].muted = False
        self.bridge.send_params(name, self._states[name].params)

    def solo(self, name: str) -> None:
        if name not in self._states:
            return
        for n, state in self._states.items():
            state.muted_before_solo = state.muted
            if n != name:
                state.muted = True
                self.bridge.send_params(n, dataclasses.replace(state.params, amp=0.0))
            else:
                state.muted = False
                self.bridge.send_params(n, state.params)

    def unsolo(self) -> None:
        for n, state in self._states.items():
            state.muted = state.muted_before_solo
            amp = 0.0 if state.muted else state.params.amp
            self.bridge.send_params(n, dataclasses.replace(state.params, amp=amp))

    def panic(self) -> None:
        for name in list(self._states):
            self.stop_loop(name)
        self.bridge.send_panic()

    def status(self) -> list[LoopStatus]:
        return [
            LoopStatus(name=n, muted=s.muted, amp=s.params.amp, cutoff=s.params.cutoff)
            for n, s in self._states.items()
        ]
