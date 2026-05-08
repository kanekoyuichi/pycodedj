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
