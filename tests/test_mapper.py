from pycodedj.analyzer import CodeFeatures
from pycodedj.mapper import map_features


def _features(
    max_depth: int = 0,
    control_flow_count: int = 0,
    function_count: int = 1,
    comment_ratio: float = 0.0,
) -> CodeFeatures:
    return CodeFeatures(
        max_depth=max_depth,
        control_flow_count=control_flow_count,
        function_count=function_count,
        comment_ratio=comment_ratio,
    )


def test_cutoff_min() -> None:
    p = map_features(_features(max_depth=0))
    assert p.cutoff == 200.0


def test_cutoff_max() -> None:
    p = map_features(_features(max_depth=10))
    assert p.cutoff == 4000.0


def test_cutoff_over_max_clamped() -> None:
    p = map_features(_features(max_depth=100))
    assert p.cutoff == 4000.0


def test_lfo_rate_min() -> None:
    p = map_features(_features(control_flow_count=0))
    assert abs(p.lfo_rate - 0.1) < 1e-9


def test_lfo_rate_max() -> None:
    p = map_features(_features(control_flow_count=10))
    assert abs(p.lfo_rate - 5.0) < 1e-9


def test_lfo_rate_over_max_clamped() -> None:
    p = map_features(_features(control_flow_count=999))
    assert p.lfo_rate == 5.0


def test_reverb_no_comments() -> None:
    p = map_features(_features(comment_ratio=0.0))
    assert p.reverb_mix == 0.0


def test_reverb_full_comments() -> None:
    p = map_features(_features(comment_ratio=1.0))
    assert p.reverb_mix == 0.8


def test_voice_count_clamp_min() -> None:
    p = map_features(_features(function_count=0))
    assert p.voice_count == 1


def test_voice_count_clamp_max() -> None:
    p = map_features(_features(function_count=100))
    assert p.voice_count == 4


def test_all_params_in_range() -> None:
    for depth in [0, 5, 10, 20]:
        for cf in [0, 3, 10, 50]:
            for fc in [0, 1, 4, 10]:
                for cr in [0.0, 0.5, 1.0]:
                    p = map_features(_features(depth, cf, fc, cr))
                    assert 200.0 <= p.cutoff <= 4000.0
                    assert 0.1 <= p.lfo_rate <= 5.0
                    assert 0.0 <= p.reverb_mix <= 0.8
                    assert 1 <= p.voice_count <= 4
