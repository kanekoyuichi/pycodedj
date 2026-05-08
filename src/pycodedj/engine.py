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
    has_pattern: bool = False


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
            # Validate and pre-compute pattern args before any state mutation.
            pattern_args = self._make_pattern_args(block) if block.pattern_str is not None else None
            # Pattern blocks own their own timing via Pdef — suppress the legacy loop.
            if pattern_args is not None:
                send = dataclasses.replace(send, voice_count=0)
            else:
                # Always clear any stale Pdef before starting the legacy loop,
                # even when called from a fresh stateless Engine (SC treats it as no-op if none running).
                self.bridge.send_pattern_stop(block.name)
            if pattern_args is None:
                self.bridge.send_synth(block.name, block.synth or "")
            self.bridge.send_params(block.name, send)
            if pattern_args is not None:
                self.bridge.send_pattern(block.name, *pattern_args)
            # Commit state only after all OSC sends succeed.
            # For pattern states, store voice_count=0 so mute/solo never restart the legacy loop.
            stored_params = dataclasses.replace(params, voice_count=0) if pattern_args is not None else params
            self._states[block.name] = LoopState(
                params=stored_params, muted=muted, has_pattern=pattern_args is not None
            )
            return params
        except SyntaxError as e:
            sys.stderr.write(f"[pycodedj] syntax error ({block.name}): {e}\n")
        except OscError as e:
            sys.stderr.write(f"[pycodedj] OSC send failed ({block.name}): {e}\n")
        except ValueError as e:
            sys.stderr.write(f"[pycodedj] pattern error ({block.name}): {e}\n")
        return None

    def _make_pattern_args(
        self, block: LoopBlock
    ) -> tuple[int, str, float, list[int], str]:
        from .pattern import parse_pattern, root_to_midi
        steps = parse_pattern(block.pattern_str or "")
        midi = root_to_midi(block.root or "C4")
        scale = block.scale or "chromatic"
        dur = block.dur or 0.25
        synth = block.synth or ""
        return midi, scale, dur, steps, synth

    def stop_loop(self, name: str) -> None:
        state = self._states.pop(name, None)
        stop_params = MusicParams(cutoff=200.0, lfo_rate=0.1, reverb_mix=0.0, voice_count=0)
        self.bridge.send_params(name, stop_params)
        if state is not None and state.has_pattern:
            self.bridge.send_pattern_stop(name)

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
