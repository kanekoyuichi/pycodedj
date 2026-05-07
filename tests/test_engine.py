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
