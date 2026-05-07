"""Single OSC ping to verify SuperCollider connectivity.

Usage:
    python examples/hello_sc.py
    python examples/hello_sc.py --host 127.0.0.1 --port 57120
"""

from __future__ import annotations

import argparse

from pycodedj.mapper import MusicParams
from pycodedj.osc_bridge import OscBridge, OscEndpoint


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=57120, type=int)
    args = parser.parse_args()

    bridge = OscBridge(audio=OscEndpoint(host=args.host, port=args.port))
    params = MusicParams(cutoff=1000.0, lfo_rate=0.5, reverb_mix=0.2, voice_count=1, amp=0.3)
    bridge.send_params("hello", params)
    print(f"Sent OSC to {args.host}:{args.port} — loop 'hello'")


if __name__ == "__main__":
    main()
