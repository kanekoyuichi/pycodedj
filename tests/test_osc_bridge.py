from typing import Any, cast
from unittest.mock import MagicMock, patch

import pytest

from pycodedj.mapper import MusicParams
from pycodedj.osc_bridge import OscBridge, OscEndpoint, OscError


def _make_mock_endpoint(port: int) -> OscEndpoint:
    with patch("pycodedj.osc_bridge.udp_client.SimpleUDPClient"):
        ep = OscEndpoint(host="127.0.0.1", port=port)
    ep._client = MagicMock()
    return ep


@pytest.fixture()
def mock_endpoint() -> OscEndpoint:
    return _make_mock_endpoint(57120)


@pytest.fixture()
def mock_visual() -> OscEndpoint:
    return _make_mock_endpoint(57200)


def _send_mock(ep: OscEndpoint) -> Any:
    return cast(MagicMock, ep._client).send_message


def _make_params() -> MusicParams:
    return MusicParams(
        cutoff=800.0,
        lfo_rate=1.0,
        reverb_mix=0.3,
        voice_count=2,
        amp=0.5,
        low=1.2,
        mid=0.9,
        high=1.1,
    )


def test_send_params_addresses(mock_endpoint: OscEndpoint) -> None:
    bridge = OscBridge(audio=mock_endpoint)
    bridge.send_params("bass", _make_params())

    calls = [c.args[0] for c in _send_mock(mock_endpoint).call_args_list]
    assert calls == ["/pycodedj/loop/bass/params"]


def test_send_params_values(mock_endpoint: OscEndpoint) -> None:
    bridge = OscBridge(audio=mock_endpoint)
    bridge.send_params("bass", _make_params())

    call_map = {c.args[0]: c.args[1] for c in _send_mock(mock_endpoint).call_args_list}
    assert call_map["/pycodedj/loop/bass/params"] == [2, 800.0, 1.0, 0.3, 0.5, 1.2, 0.9, 1.1]


def test_no_visual_sends_only_audio(mock_endpoint: OscEndpoint) -> None:
    bridge = OscBridge(audio=mock_endpoint, visual=None)
    bridge.send_params("bass", _make_params())
    assert _send_mock(mock_endpoint).call_count == 1


def test_visual_receives_params(mock_endpoint: OscEndpoint, mock_visual: OscEndpoint) -> None:
    bridge = OscBridge(audio=mock_endpoint, visual=mock_visual)
    bridge.send_params("bass", _make_params())
    assert _send_mock(mock_visual).call_count == 1


def test_osc_error_on_init_failure() -> None:
    with patch(
        "pycodedj.osc_bridge.udp_client.SimpleUDPClient",
        side_effect=OSError("socket error"),
    ):
        with pytest.raises(OscError):
            OscEndpoint(host="127.0.0.1", port=57120)


def test_osc_error_on_send_failure(mock_endpoint: OscEndpoint) -> None:
    _send_mock(mock_endpoint).side_effect = OSError("network unreachable")
    bridge = OscBridge(audio=mock_endpoint)
    with pytest.raises(OscError):
        bridge.send_params("bass", _make_params())


def test_osc_error_on_attribute_error() -> None:
    with patch(
        "pycodedj.osc_bridge.udp_client.SimpleUDPClient",
        side_effect=AttributeError("_sock"),
    ):
        with pytest.raises(OscError):
            OscEndpoint(host="127.0.0.1", port=57120)


# --- send_panic ---

def test_send_panic_sends_to_audio(mock_endpoint: OscEndpoint) -> None:
    bridge = OscBridge(audio=mock_endpoint)
    bridge.send_panic()

    calls = [c.args[0] for c in _send_mock(mock_endpoint).call_args_list]
    assert "/pycodedj/panic" in calls


def test_send_panic_sends_to_visual_when_set(
    mock_endpoint: OscEndpoint, mock_visual: OscEndpoint
) -> None:
    bridge = OscBridge(audio=mock_endpoint, visual=mock_visual)
    bridge.send_panic()

    visual_calls = [c.args[0] for c in _send_mock(mock_visual).call_args_list]
    assert "/pycodedj/panic" in visual_calls


def test_send_panic_skips_visual_when_none(mock_endpoint: OscEndpoint) -> None:
    bridge = OscBridge(audio=mock_endpoint, visual=None)
    bridge.send_panic()

    assert _send_mock(mock_endpoint).call_count == 1


# --- send_pattern ---

def test_send_pattern_address(mock_endpoint: OscEndpoint) -> None:
    bridge = OscBridge(audio=mock_endpoint)
    bridge.send_pattern("kick", 48, "chromatic", 0.25, [-1, -2, -1, -2])

    calls = [c.args[0] for c in _send_mock(mock_endpoint).call_args_list]
    assert calls == ["/pycodedj/loop/kick/pattern"]


def test_send_pattern_values(mock_endpoint: OscEndpoint) -> None:
    bridge = OscBridge(audio=mock_endpoint)
    bridge.send_pattern("kick", 48, "chromatic", 0.25, [-1, -2, -1, -2])

    call_map = {c.args[0]: c.args[1] for c in _send_mock(mock_endpoint).call_args_list}
    # order: root_midi, scale, dur, synth(""), steps...
    assert call_map["/pycodedj/loop/kick/pattern"] == [48, "chromatic", 0.25, "", -1, -2, -1, -2]


def test_send_pattern_with_synth(mock_endpoint: OscEndpoint) -> None:
    bridge = OscBridge(audio=mock_endpoint)
    bridge.send_pattern("bass", 33, "minor", 0.5, [0, -2], synth="bass_acid")

    call_map = {c.args[0]: c.args[1] for c in _send_mock(mock_endpoint).call_args_list}
    assert call_map["/pycodedj/loop/bass/pattern"] == [33, "minor", 0.5, "bass_acid", 0, -2]


def test_send_pattern_empty_steps(mock_endpoint: OscEndpoint) -> None:
    bridge = OscBridge(audio=mock_endpoint)
    bridge.send_pattern("bass", 33, "minor", 0.5, [])

    call_map = {c.args[0]: c.args[1] for c in _send_mock(mock_endpoint).call_args_list}
    assert call_map["/pycodedj/loop/bass/pattern"] == [33, "minor", 0.5, ""]


def test_send_pattern_stop(mock_endpoint: OscEndpoint) -> None:
    bridge = OscBridge(audio=mock_endpoint)
    bridge.send_pattern_stop("kick")

    calls = [c.args[0] for c in _send_mock(mock_endpoint).call_args_list]
    assert calls == ["/pycodedj/loop/kick/pattern_stop"]
