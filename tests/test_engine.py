from unittest.mock import MagicMock, patch

from pycodedj.block_parser import LoopBlock
from pycodedj.engine import Engine
from pycodedj.mapper import MusicParams
from pycodedj.osc_bridge import OscBridge, OscEndpoint


def _make_engine() -> Engine:
    with patch("pycodedj.osc_bridge.udp_client.SimpleUDPClient"):
        ep = OscEndpoint(host="127.0.0.1", port=57120)
    ep._client = MagicMock()
    bridge = OscBridge(audio=ep)
    return Engine(bridge=bridge)


def _block(source: str, name: str = "test") -> LoopBlock:
    return LoopBlock(name=name, interval=1.0, source=source)


def test_eval_block_returns_params_on_success() -> None:
    engine = _make_engine()
    result = engine.eval_block(_block("def f(): pass"))
    assert isinstance(result, MusicParams)


def test_eval_block_returns_none_on_syntax_error() -> None:
    engine = _make_engine()
    result = engine.eval_block(_block("def f(:"))
    assert result is None


def test_eval_block_returns_none_on_osc_error() -> None:
    engine = _make_engine()
    from typing import cast
    cast(MagicMock, engine.bridge.audio._client).send_message.side_effect = OSError("fail")
    result = engine.eval_block(_block("def f(): pass"))
    assert result is None


def test_eval_block_stores_params_on_success() -> None:
    engine = _make_engine()
    engine.eval_block(_block("def f(): pass", name="bass"))
    assert "bass" in engine.list_loops()


def test_eval_block_does_not_store_on_error() -> None:
    engine = _make_engine()
    engine.eval_block(_block("def f(:", name="bass"))
    assert "bass" not in engine.list_loops()


# --- mute / unmute ---

def test_mute_sends_amp_zero() -> None:
    engine = _make_engine()
    engine.eval_block(_block("def f(): pass", name="bass"))

    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.mute("bass")

    calls = mock_send.call_args_list
    assert len(calls) == 1
    args = calls[0].args[1]  # second positional arg is the value list
    amp_index = 4  # voice_count, cutoff, lfo_rate, reverb_mix, amp, low, mid, high
    assert args[amp_index] == 0.0


def test_mute_nonexistent_is_noop() -> None:
    engine = _make_engine()
    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.mute("nonexistent")

    mock_send.assert_not_called()


def test_unmute_restores_amp() -> None:
    engine = _make_engine()
    engine.eval_block(_block("def f(): pass", name="bass"))
    original_amp = engine._states["bass"].params.amp

    engine.mute("bass")
    engine.unmute("bass")

    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    last_call_values = mock_send.call_args_list[-1].args[1]
    amp_index = 4
    assert last_call_values[amp_index] == original_amp


def test_eval_while_muted_keeps_amp_zero() -> None:
    engine = _make_engine()
    engine.eval_block(_block("def f(): pass", name="bass"))
    engine.mute("bass")

    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.eval_block(_block("def f(): pass\nx = 1", name="bass"))

    amp_index = 4
    sent_amp = mock_send.call_args_list[-1].args[1][amp_index]
    assert sent_amp == 0.0
    assert engine._states["bass"].muted is True


# --- solo / unsolo ---

def test_solo_unknown_name_is_noop() -> None:
    engine = _make_engine()
    engine.eval_block(_block("def f(): pass", name="bass"))
    engine.eval_block(_block("def f(): pass", name="pad"))

    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.solo("nonexistent")

    assert engine._states["bass"].muted is False
    assert engine._states["pad"].muted is False
    mock_send.assert_not_called()


def test_solo_mutes_others() -> None:
    engine = _make_engine()
    engine.eval_block(_block("def f(): pass", name="bass"))
    engine.eval_block(_block("def f(): pass", name="pad"))

    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.solo("bass")

    assert engine._states["bass"].muted is False
    assert engine._states["pad"].muted is True


def test_solo_saves_muted_before_solo() -> None:
    engine = _make_engine()
    engine.eval_block(_block("def f(): pass", name="bass"))
    engine.eval_block(_block("def f(): pass", name="pad"))
    engine.mute("pad")

    engine.solo("bass")

    assert engine._states["pad"].muted_before_solo is True
    assert engine._states["bass"].muted_before_solo is False


def test_unsolo_restores_muted_state() -> None:
    engine = _make_engine()
    engine.eval_block(_block("def f(): pass", name="bass"))
    engine.eval_block(_block("def f(): pass", name="pad"))
    engine.mute("pad")

    engine.solo("bass")
    engine.unsolo()

    assert engine._states["pad"].muted is True
    assert engine._states["bass"].muted is False


# --- panic ---

def test_panic_stops_all_loops() -> None:
    engine = _make_engine()
    engine.eval_block(_block("def f(): pass", name="bass"))
    engine.eval_block(_block("def f(): pass", name="pad"))

    engine.panic()

    assert engine.list_loops() == []


def test_panic_sends_osc_panic() -> None:
    engine = _make_engine()
    engine.eval_block(_block("def f(): pass", name="bass"))

    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.panic()

    addresses = [c.args[0] for c in mock_send.call_args_list]
    assert "/pycodedj/panic" in addresses


def test_panic_on_empty_engine_is_noop() -> None:
    engine = _make_engine()

    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.panic()

    addresses = [c.args[0] for c in mock_send.call_args_list]
    assert "/pycodedj/panic" in addresses
    assert engine.list_loops() == []


# --- status ---

def test_status_returns_loop_info() -> None:
    engine = _make_engine()
    engine.eval_block(_block("def f(): pass", name="bass"))

    entries = engine.status()

    assert len(entries) == 1
    assert entries[0].name == "bass"
    assert isinstance(entries[0].amp, float)
    assert isinstance(entries[0].cutoff, float)


def test_status_reflects_muted_state() -> None:
    engine = _make_engine()
    engine.eval_block(_block("def f(): pass", name="bass"))
    engine.mute("bass")

    entries = engine.status()

    assert entries[0].muted is True


def test_status_empty_on_init() -> None:
    engine = _make_engine()
    assert engine.status() == []


# --- pattern ---

def _pattern_block(
    pattern_str: str | None = "x . x .",
    root: str | None = "C4",
    scale: str | None = "chromatic",
    dur: float | None = 0.25,
) -> LoopBlock:
    return LoopBlock(
        name="kick",
        interval=1.0,
        source="def f(): pass",
        synth="kick_pulse",
        root=root,
        scale=scale,
        dur=dur,
        pattern_str=pattern_str,
    )


def test_mute_pattern_loop_keeps_voice_count_zero() -> None:
    engine = _make_engine()
    engine.eval_block(_pattern_block())
    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.mute("kick")

    params_calls = [c for c in mock_send.call_args_list if "/params" in c.args[0]]
    assert len(params_calls) == 1
    assert params_calls[0].args[1][0] == 0  # voice_count still 0


def test_mute_pattern_loop_does_not_send_pattern_stop() -> None:
    engine = _make_engine()
    engine.eval_block(_pattern_block())
    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.mute("kick")

    addresses = [c.args[0] for c in mock_send.call_args_list]
    assert "/pycodedj/loop/kick/pattern_stop" not in addresses


def test_stop_loop_sends_pattern_stop_when_had_pattern() -> None:
    engine = _make_engine()
    engine.eval_block(_pattern_block())
    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.stop_loop("kick")

    addresses = [c.args[0] for c in mock_send.call_args_list]
    assert "/pycodedj/loop/kick/pattern_stop" in addresses


def test_stop_loop_does_not_send_pattern_stop_for_non_pattern_loop() -> None:
    engine = _make_engine()
    engine.eval_block(_block("def f(): pass", name="kick"))
    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.stop_loop("kick")

    addresses = [c.args[0] for c in mock_send.call_args_list]
    assert "/pycodedj/loop/kick/pattern_stop" not in addresses


def test_eval_block_pattern_suppresses_legacy_loop() -> None:
    engine = _make_engine()
    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.eval_block(_pattern_block())

    # /params should have voice_count=0 when pattern is active
    params_calls = [c for c in mock_send.call_args_list if "/params" in c.args[0]]
    assert len(params_calls) == 1
    assert params_calls[0].args[1][0] == 0  # voice_count at index 0


def test_eval_block_pattern_osc_fail_does_not_update_state() -> None:
    engine = _make_engine()
    # Make send_pattern fail (second call fails)
    call_count = 0
    original_send = engine.bridge.audio.send

    def failing_send(address: str, *args: object) -> None:
        nonlocal call_count
        call_count += 1
        if "pattern" in address and "stop" not in address:
            from pycodedj.osc_bridge import OscError
            raise OscError("pattern send failed")
        original_send(address, *args)

    engine.bridge.audio.send = failing_send  # type: ignore[method-assign]

    result = engine.eval_block(_pattern_block())
    assert result is None
    assert "kick" not in engine.list_loops()


def test_eval_block_calls_send_pattern_when_pattern_str_set() -> None:
    engine = _make_engine()
    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.eval_block(_pattern_block())

    addresses = [c.args[0] for c in mock_send.call_args_list]
    assert "/pycodedj/loop/kick/pattern" in addresses


def test_eval_block_does_not_call_send_pattern_when_pattern_str_none() -> None:
    engine = _make_engine()
    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.eval_block(_pattern_block(pattern_str=None))

    addresses = [c.args[0] for c in mock_send.call_args_list]
    assert "/pycodedj/loop/kick/pattern" not in addresses


def test_eval_block_pattern_values_correct() -> None:
    engine = _make_engine()
    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.eval_block(_pattern_block(pattern_str="x . x .", root="C4", scale="minor", dur=0.25))

    call_map = {c.args[0]: c.args[1] for c in mock_send.call_args_list}
    values = call_map["/pycodedj/loop/kick/pattern"]
    # order: root_midi=60, scale="minor", dur=0.25, synth="kick_pulse", steps...
    assert values[0] == 60
    assert values[1] == "minor"
    assert values[2] == 0.25
    assert values[3] == "kick_pulse"
    assert values[4:] == ["v2", 1, -1, 0, 1, -1, 0]


def test_eval_block_pattern_chord_and_tie_values_correct() -> None:
    engine = _make_engine()
    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.eval_block(_pattern_block(pattern_str="0 . [0 3] ~ 5 . 3 .", root="C4", scale="minor", dur=0.25))

    call_map = {c.args[0]: c.args[1] for c in mock_send.call_args_list}
    values = call_map["/pycodedj/loop/kick/pattern"]
    assert values == [
        60,
        "minor",
        0.25,
        "kick_pulse",
        "v2",
        1,
        0,
        0,
        2,
        0,
        3,
        -3,
        1,
        5,
        0,
        1,
        3,
        0,
    ]


def test_eval_block_pattern_uses_defaults_for_missing_root_scale_dur() -> None:
    engine = _make_engine()
    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.eval_block(_pattern_block(pattern_str="x .", root=None, scale=None, dur=None))

    call_map = {c.args[0]: c.args[1] for c in mock_send.call_args_list}
    values = call_map["/pycodedj/loop/kick/pattern"]
    assert values[0] == 60   # C4 default
    assert values[1] == "chromatic"
    assert values[2] == 0.25


def test_eval_block_invalid_pattern_does_not_update_state() -> None:
    engine = _make_engine()
    result = engine.eval_block(_pattern_block(pattern_str="x y ."))
    assert result is None
    assert "kick" not in engine.list_loops()


def test_eval_block_invalid_pattern_returns_none() -> None:
    engine = _make_engine()
    result = engine.eval_block(_pattern_block(pattern_str="x y ."))
    assert result is None


def test_eval_block_sends_synth_for_non_pattern_loop() -> None:
    engine = _make_engine()
    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    block = LoopBlock(name="beat", interval=1.0, source="def f(): pass", synth="kick_pulse")
    engine.eval_block(block)

    addresses = [c.args[0] for c in mock_send.call_args_list]
    assert "/pycodedj/loop/beat/synth" in addresses


def test_eval_block_sends_synth_clear_when_no_synth() -> None:
    engine = _make_engine()
    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.eval_block(_block("def f(): pass", name="beat"))

    call_map = {c.args[0]: c.args[1] for c in mock_send.call_args_list}
    assert "/pycodedj/loop/beat/synth" in call_map
    assert call_map["/pycodedj/loop/beat/synth"] == [""]


def test_eval_block_does_not_send_synth_for_pattern_loop() -> None:
    engine = _make_engine()
    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.eval_block(_pattern_block())

    addresses = [c.args[0] for c in mock_send.call_args_list]
    assert "/pycodedj/loop/kick/synth" not in addresses


def test_send_synth() -> None:
    with patch("pycodedj.osc_bridge.udp_client.SimpleUDPClient"):
        ep = OscEndpoint(host="127.0.0.1", port=57120)
    client = MagicMock()
    ep._client = client
    bridge = OscBridge(audio=ep)
    bridge.send_synth("beat", "kick_pulse")
    assert client.send_message.call_args.args[0] == "/pycodedj/loop/beat/synth"
    assert client.send_message.call_args.args[1] == ["kick_pulse"]


def test_eval_block_pattern_to_non_pattern_sends_stop_before_params() -> None:
    engine = _make_engine()
    engine.eval_block(_pattern_block(pattern_str="x . x ."))

    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    engine.eval_block(_pattern_block(pattern_str=None))

    addresses = [c.args[0] for c in mock_send.call_args_list]
    stop_idx = next(i for i, a in enumerate(addresses) if "pattern_stop" in a)
    params_idx = next(i for i, a in enumerate(addresses) if "/params" in a)
    assert stop_idx < params_idx


def test_eval_block_pattern_removed_sends_stop() -> None:
    engine = _make_engine()
    engine.eval_block(_pattern_block(pattern_str="x . x ."))

    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    # Re-eval without pattern_str — should send pattern_stop
    engine.eval_block(_pattern_block(pattern_str=None))

    addresses = [c.args[0] for c in mock_send.call_args_list]
    assert "/pycodedj/loop/kick/pattern_stop" in addresses


def test_eval_block_always_sends_pattern_stop_for_non_pattern_block() -> None:
    engine = _make_engine()
    from typing import cast
    mock_send = cast(MagicMock, engine.bridge.audio._client).send_message
    mock_send.reset_mock()

    # Eval without pattern — pattern_stop is always sent (SC no-ops when no Pdef is running)
    engine.eval_block(_pattern_block(pattern_str=None))

    addresses = [c.args[0] for c in mock_send.call_args_list]
    assert "/pycodedj/loop/kick/pattern_stop" in addresses
