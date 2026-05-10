from argparse import Namespace
from unittest.mock import MagicMock, patch

from pycodedj.__main__ import _build_parser, _cmd_bpm, _cmd_list_synths, _cmd_stop
from pycodedj.osc_bridge import OscError


def test_parser_accepts_stop_command() -> None:
    args = _build_parser().parse_args(["stop", "kick_hard"])

    assert args.command == "stop"
    assert args.name == "kick_hard"


def test_cmd_stop_sends_loop_stop() -> None:
    bridge = MagicMock()
    args = Namespace(name="kick_hard", sc_host="127.0.0.1", sc_port=57120)

    with patch("pycodedj.__main__._make_bridge", return_value=bridge):
        result = _cmd_stop(args)

    assert result == 0
    bridge.send_loop_stop.assert_called_once_with("kick_hard")


def test_cmd_stop_reports_osc_error() -> None:
    bridge = MagicMock()
    bridge.send_loop_stop.side_effect = OscError("socket error")
    args = Namespace(name="kick_hard", sc_host="127.0.0.1", sc_port=57120)

    with patch("pycodedj.__main__._make_bridge", return_value=bridge):
        result = _cmd_stop(args)

    assert result == 1


def test_parser_accepts_bpm_command() -> None:
    args = _build_parser().parse_args(["bpm", "128"])

    assert args.command == "bpm"
    assert args.value == 128.0


def test_cmd_bpm_sends_bpm() -> None:
    bridge = MagicMock()
    args = Namespace(value=128.0, sc_host="127.0.0.1", sc_port=57120)

    with patch("pycodedj.__main__._make_bridge", return_value=bridge):
        result = _cmd_bpm(args)

    assert result == 0
    bridge.send_bpm.assert_called_once_with(128.0)


def test_cmd_bpm_rejects_non_positive_value() -> None:
    bridge = MagicMock()
    args = Namespace(value=0.0, sc_host="127.0.0.1", sc_port=57120)

    with patch("pycodedj.__main__._make_bridge", return_value=bridge):
        result = _cmd_bpm(args)

    assert result == 1
    bridge.send_bpm.assert_not_called()


def test_parser_accepts_list_synths_command() -> None:
    args = _build_parser().parse_args(["list-synths"])

    assert args.command == "list-synths"


def test_cmd_list_synths_prints_known_synths(capsys) -> None:  # type: ignore[no-untyped-def]
    result = _cmd_list_synths(Namespace())

    assert result == 0
    out = capsys.readouterr().out
    assert "Kicks:" in out
    assert "kick_floor" in out
    assert "bass_acid" in out
    assert "fx_vinyl" in out
