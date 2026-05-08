from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .block_parser import parse_blocks
from .engine import Engine
from .osc_bridge import OscBridge, OscEndpoint, OscError


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pycodedj")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command")

    eval_p = sub.add_parser("eval", help="Evaluate a loop block and send OSC parameters")
    eval_p.add_argument(
        "target",
        metavar="FILE::LOOP",
        help="Path to source file and loop name, separated by ::",
    )
    eval_p.add_argument("--sc-host", default="127.0.0.1", help="SuperCollider host")
    eval_p.add_argument("--sc-port", default=57120, type=int, help="SuperCollider port")

    watch_p = sub.add_parser("watch", help="Watch a file and re-eval all loops on save")
    watch_p.add_argument("file", metavar="FILE", help="Source file to watch")
    watch_p.add_argument("--sc-host", default="127.0.0.1", help="SuperCollider host")
    watch_p.add_argument("--sc-port", default=57120, type=int, help="SuperCollider port")
    watch_p.add_argument(
        "--debounce", default=0.3, type=float,
        metavar="SECS", help="Debounce interval in seconds (default: 0.3)",
    )

    panic_p = sub.add_parser("panic", help="Stop all loops immediately")
    panic_p.add_argument("--sc-host", default="127.0.0.1", help="SuperCollider host")
    panic_p.add_argument("--sc-port", default=57120, type=int, help="SuperCollider port")

    stop_p = sub.add_parser("stop", help="Stop one loop immediately")
    stop_p.add_argument("name", help="Loop name")
    stop_p.add_argument("--sc-host", default="127.0.0.1", help="SuperCollider host")
    stop_p.add_argument("--sc-port", default=57120, type=int, help="SuperCollider port")

    # NOTE: mute/unmute/solo/unsolo は watch プロセスとは別プロセスで実行されるため
    # Engine._states を共有できない。CLI では OSC を直接送信する簡易実装とする。
    mute_p = sub.add_parser("mute", help="Mute a loop (sends amp=0 via OSC)")
    mute_p.add_argument("name", help="Loop name")
    mute_p.add_argument("--sc-host", default="127.0.0.1", help="SuperCollider host")
    mute_p.add_argument("--sc-port", default=57120, type=int, help="SuperCollider port")

    unmute_p = sub.add_parser("unmute", help="Unmute a loop (sends amp restore via OSC)")
    unmute_p.add_argument("name", help="Loop name")
    unmute_p.add_argument("--sc-host", default="127.0.0.1", help="SuperCollider host")
    unmute_p.add_argument("--sc-port", default=57120, type=int, help="SuperCollider port")

    solo_p = sub.add_parser("solo", help="Solo a loop (mutes all others via OSC)")
    solo_p.add_argument("name", help="Loop name to solo")
    solo_p.add_argument("--sc-host", default="127.0.0.1", help="SuperCollider host")
    solo_p.add_argument("--sc-port", default=57120, type=int, help="SuperCollider port")

    unsolo_p = sub.add_parser("unsolo", help="Release solo")
    unsolo_p.add_argument("--sc-host", default="127.0.0.1", help="SuperCollider host")
    unsolo_p.add_argument("--sc-port", default=57120, type=int, help="SuperCollider port")

    status_p = sub.add_parser("status", help="Show active loop status")
    status_p.add_argument("--sc-host", default="127.0.0.1", help="SuperCollider host")
    status_p.add_argument("--sc-port", default=57120, type=int, help="SuperCollider port")

    return parser


def _print_params(loop_name: str, params: object) -> None:
    from .mapper import MusicParams
    if not isinstance(params, MusicParams):
        return
    print(
        f"[pycodedj] {loop_name}"
        f"  cutoff={params.cutoff:.0f}Hz"
        f"  lfo={params.lfo_rate:.2f}Hz"
        f"  reverb={params.reverb_mix:.2f}"
        f"  voices={params.voice_count}"
        f"  eq={params.low:.2f}/{params.mid:.2f}/{params.high:.2f}"
    )


def _make_bridge(args: argparse.Namespace) -> OscBridge | None:
    try:
        return OscBridge(audio=OscEndpoint(host=args.sc_host, port=args.sc_port))
    except OscError as e:
        sys.stderr.write(f"[pycodedj] OSC error: {e}\n")
        return None


def _cmd_eval(args: argparse.Namespace) -> int:
    if "::" not in args.target:
        sys.stderr.write(f"[pycodedj] invalid target format (expected FILE::LOOP): {args.target}\n")
        return 1

    file_path, loop_name = args.target.split("::", 1)
    path = Path(file_path)

    if not path.exists():
        sys.stderr.write(f"[pycodedj] file not found: {file_path}\n")
        return 1

    source = path.read_text(encoding="utf-8")
    result = parse_blocks(source)
    if not result.ok:
        sys.stderr.write(f"[pycodedj] syntax error in {file_path}: {result.error}\n")
        return 1
    block_map = {b.name: b for b in result.blocks}

    if loop_name not in block_map:
        available = ", ".join(block_map.keys()) or "(none)"
        sys.stderr.write(
            f"[pycodedj] loop '{loop_name}' not found in {file_path}. "
            f"Available: {available}\n"
        )
        return 1

    bridge = _make_bridge(args)
    if bridge is None:
        return 1

    try:
        engine = Engine(bridge=bridge)
        params = engine.eval_block(block_map[loop_name])
    except OscError as e:
        sys.stderr.write(f"[pycodedj] OSC error: {e}\n")
        return 1

    if params is not None:
        _print_params(loop_name, params)
        return 0
    return 1


def _cmd_watch(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.exists():
        sys.stderr.write(f"[pycodedj] file not found: {args.file}\n")
        return 1

    try:
        from .watcher import watch
    except ImportError as e:
        sys.stderr.write(f"[pycodedj] {e}\n")
        return 1

    bridge = _make_bridge(args)
    if bridge is None:
        return 1

    engine = Engine(bridge=bridge)

    def _on_eval(file_path: str, loop_count: int) -> None:
        print(f"[pycodedj] reloaded {Path(file_path).name} ({loop_count} loop(s))")

    print(f"[pycodedj] watching {path} — save to reload (Ctrl+C to stop)")
    watch(str(path), engine, debounce=args.debounce, on_eval=_on_eval)
    return 0


def _cmd_panic(args: argparse.Namespace) -> int:
    bridge = _make_bridge(args)
    if bridge is None:
        return 1
    Engine(bridge=bridge).panic()
    print("[pycodedj] panic: all loops stopped")
    return 0


def _cmd_stop(args: argparse.Namespace) -> int:
    bridge = _make_bridge(args)
    if bridge is None:
        return 1
    try:
        bridge.send_loop_stop(args.name)
    except OscError as e:
        sys.stderr.write(f"[pycodedj] OSC error: {e}\n")
        return 1
    print(f"[pycodedj] stopped {args.name}")
    return 0


def _cmd_mute(args: argparse.Namespace) -> int:
    bridge = _make_bridge(args)
    if bridge is None:
        return 1
    try:
        bridge.audio.send(f"/pycodedj/loop/{args.name}/amp", 0.0)
    except OscError as e:
        sys.stderr.write(f"[pycodedj] OSC error: {e}\n")
        return 1
    print(f"[pycodedj] muted {args.name}")
    return 0


def _cmd_unmute(args: argparse.Namespace) -> int:
    bridge = _make_bridge(args)
    if bridge is None:
        return 1
    try:
        # CLI mute は SC ~loopParams に amp=0 を永続化するため、unmute では
        # 先に amp をデフォルト値に戻し、その後 voice_count=1 で再起動する。
        from .mapper import _AMP_DEFAULT
        bridge.audio.send(f"/pycodedj/loop/{args.name}/amp", _AMP_DEFAULT)
        bridge.audio.send(f"/pycodedj/loop/{args.name}/voice_count", 1)
    except OscError as e:
        sys.stderr.write(f"[pycodedj] OSC error: {e}\n")
        return 1
    print(f"[pycodedj] unmuted {args.name}")
    return 0


def _cmd_solo(args: argparse.Namespace) -> int:
    sys.stderr.write(
        "[pycodedj] solo is not supported from CLI (requires watch process state). "
        "Use Engine.solo() directly in watch mode.\n"
    )
    return 1


def _cmd_unsolo(args: argparse.Namespace) -> int:
    sys.stderr.write(
        "[pycodedj] unsolo is not supported from CLI (requires watch process state). "
        "Use Engine.unsolo() directly in watch mode.\n"
    )
    return 1


def _cmd_status(args: argparse.Namespace) -> int:
    # NOTE: watch プロセスとは別プロセスのため Engine._states は常に空になる。
    # status は将来の IPC 対応後に実用的になる。現状は Engine API の確認用。
    bridge = _make_bridge(args)
    if bridge is None:
        return 1
    entries = Engine(bridge=bridge).status()
    if not entries:
        print("[pycodedj] no active loops")
        return 0
    print(f"{'Loop':<12} {'State':<8} {'Amp':<6} {'Cutoff'}")
    for e in entries:
        state_str = "muted" if e.muted else "playing"
        print(f"{e.name:<12} {state_str:<8} {e.amp:<6.2f} {e.cutoff:.0f}Hz")
    return 0


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "eval":
        sys.exit(_cmd_eval(args))
    elif args.command == "watch":
        sys.exit(_cmd_watch(args))
    elif args.command == "panic":
        sys.exit(_cmd_panic(args))
    elif args.command == "stop":
        sys.exit(_cmd_stop(args))
    elif args.command == "mute":
        sys.exit(_cmd_mute(args))
    elif args.command == "unmute":
        sys.exit(_cmd_unmute(args))
    elif args.command == "solo":
        sys.exit(_cmd_solo(args))
    elif args.command == "unsolo":
        sys.exit(_cmd_unsolo(args))
    elif args.command == "status":
        sys.exit(_cmd_status(args))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
