from argparse import Namespace
from unittest.mock import MagicMock, patch

from pycodedj.__main__ import _build_parser, _cmd_stop
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
