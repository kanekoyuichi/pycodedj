from __future__ import annotations

from dataclasses import dataclass

from .analyzer import CodeFeatures

_CUTOFF_MIN = 200.0
_CUTOFF_MAX = 4000.0
_CUTOFF_DEPTH_MAX = 10

_LFO_MIN = 0.1
_LFO_MAX = 5.0
_LFO_COUNT_MAX = 10

_REVERB_MIN = 0.0
_REVERB_MAX = 0.8

_VOICE_MIN = 1
_VOICE_MAX = 4


@dataclass
class MusicParams:
    cutoff: float
    lfo_rate: float
    reverb_mix: float
    voice_count: int


def _lerp(value: float, in_max: float, out_min: float, out_max: float) -> float:
    t = min(max(value / in_max, 0.0), 1.0)
    return out_min + t * (out_max - out_min)


def map_features(features: CodeFeatures) -> MusicParams:
    cutoff = _lerp(features.max_depth, _CUTOFF_DEPTH_MAX, _CUTOFF_MIN, _CUTOFF_MAX)
    lfo_rate = _lerp(features.control_flow_count, _LFO_COUNT_MAX, _LFO_MIN, _LFO_MAX)
    reverb_mix = _lerp(features.comment_ratio, 1.0, _REVERB_MIN, _REVERB_MAX)
    voice_count = min(max(features.function_count, _VOICE_MIN), _VOICE_MAX)

    return MusicParams(
        cutoff=cutoff,
        lfo_rate=lfo_rate,
        reverb_mix=reverb_mix,
        voice_count=voice_count,
    )
