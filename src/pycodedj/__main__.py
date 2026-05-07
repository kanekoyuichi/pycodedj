from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .block_parser import parse_blocks
from .engine import Engine
from .osc_bridge import OscBridge, OscEndpoint, OscError


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pycodedj")
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
    blocks = parse_blocks(source)
    block_map = {b.name: b for b in blocks}

    if loop_name not in block_map:
        available = ", ".join(block_map.keys()) or "(none)"
        sys.stderr.write(
            f"[pycodedj] loop '{loop_name}' not found in {file_path}. "
            f"Available: {available}\n"
        )
        return 1

    try:
        bridge = OscBridge(audio=OscEndpoint(host=args.sc_host, port=args.sc_port))
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

    try:
        bridge = OscBridge(audio=OscEndpoint(host=args.sc_host, port=args.sc_port))
    except OscError as e:
        sys.stderr.write(f"[pycodedj] OSC error: {e}\n")
        return 1

    engine = Engine(bridge=bridge)

    def _on_eval(file_path: str, loop_count: int) -> None:
        print(f"[pycodedj] reloaded {Path(file_path).name} ({loop_count} loop(s))")

    print(f"[pycodedj] watching {path} — save to reload (Ctrl+C to stop)")
    watch(str(path), engine, debounce=args.debounce, on_eval=_on_eval)
    return 0


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "eval":
        sys.exit(_cmd_eval(args))
    elif args.command == "watch":
        sys.exit(_cmd_watch(args))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
