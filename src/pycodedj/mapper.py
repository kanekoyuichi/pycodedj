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

_AMP_DEFAULT = 0.3

EQ_PRESETS = {
    "flat": (1.0, 1.0, 1.0),
    "classic": (0.95, 1.08, 0.92),
    "classical": (0.95, 1.08, 0.92),
    "jazz": (1.05, 1.08, 0.95),
    "rock": (1.15, 0.9, 1.15),
    "pop": (1.12, 0.92, 1.12),
    "edm": (1.35, 0.95, 1.18),
    "hiphop": (1.4, 0.95, 1.08),
    "hip-hop": (1.4, 0.95, 1.08),
    "acoustic": (0.9, 1.05, 1.08),
}


@dataclass
class MusicParams:
    cutoff: float
    lfo_rate: float
    reverb_mix: float
    voice_count: int
    amp: float = _AMP_DEFAULT
    low: float = 1.0
    mid: float = 1.0
    high: float = 1.0


def _lerp(value: float, in_max: float, out_min: float, out_max: float) -> float:
    t = min(max(value / in_max, 0.0), 1.0)
    return out_min + t * (out_max - out_min)


def _clamp_eq(value: float) -> float:
    return min(max(value, 0.0), 2.0)


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return min(max(value, minimum), maximum)


def _resolve_eq(
    eq: str = "flat",
    low: float | None = None,
    mid: float | None = None,
    high: float | None = None,
) -> tuple[float, float, float]:
    preset_low, preset_mid, preset_high = EQ_PRESETS.get(eq.lower(), EQ_PRESETS["flat"])
    return (
        _clamp_eq(preset_low if low is None else low),
        _clamp_eq(preset_mid if mid is None else mid),
        _clamp_eq(preset_high if high is None else high),
    )


def map_features(
    features: CodeFeatures,
    volume: float = _AMP_DEFAULT,
    eq: str = "flat",
    low: float | None = None,
    mid: float | None = None,
    high: float | None = None,
    cutoff: float | None = None,
    reverb: float | None = None,
) -> MusicParams:
    mapped_cutoff = _lerp(features.max_depth, _CUTOFF_DEPTH_MAX, _CUTOFF_MIN, _CUTOFF_MAX)
    lfo_rate = _lerp(features.control_flow_count, _LFO_COUNT_MAX, _LFO_MIN, _LFO_MAX)
    mapped_reverb = _lerp(features.comment_ratio, 1.0, _REVERB_MIN, _REVERB_MAX)
    voice_count = min(max(features.function_count, _VOICE_MIN), _VOICE_MAX)
    eq_low, eq_mid, eq_high = _resolve_eq(eq, low, mid, high)

    return MusicParams(
        cutoff=mapped_cutoff if cutoff is None else _clamp(cutoff, _CUTOFF_MIN, _CUTOFF_MAX),
        lfo_rate=lfo_rate,
        reverb_mix=mapped_reverb if reverb is None else _clamp(reverb, _REVERB_MIN, _REVERB_MAX),
        voice_count=voice_count,
        amp=volume,
        low=eq_low,
        mid=eq_mid,
        high=eq_high,
    )
