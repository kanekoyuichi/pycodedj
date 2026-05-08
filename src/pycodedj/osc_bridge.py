from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pythonosc import udp_client

from .pattern import PatternStep, encode_steps

if TYPE_CHECKING:
    from .mapper import MusicParams


class OscError(Exception):
    """OSC クライアントの初期化・送信失敗を表す例外。"""


@dataclass
class OscEndpoint:
    host: str
    port: int
    _client: udp_client.SimpleUDPClient = field(init=False, repr=False)

    def __post_init__(self) -> None:
        try:
            self._client = udp_client.SimpleUDPClient(self.host, self.port)
        except (OSError, AttributeError) as e:
            raise OscError(f"failed to create OSC client ({self.host}:{self.port}): {e}") from e

    def send(self, address: str, *args: object) -> None:
        try:
            self._client.send_message(address, list(args))
        except (OSError, AttributeError) as e:
            raise OscError(f"failed to send OSC message to {address}: {e}") from e


@dataclass
class OscBridge:
    audio: OscEndpoint
    visual: OscEndpoint | None = None

    def send_panic(self) -> None:
        self.audio.send("/pycodedj/panic")
        if self.visual is not None:
            self.visual.send("/pycodedj/panic")

    def send_pattern(
        self,
        name: str,
        root_midi: int,
        scale: str,
        dur: float,
        steps: list[PatternStep],
        synth: str = "",
    ) -> None:
        self.audio.send(
            f"/pycodedj/loop/{name}/pattern",
            root_midi,
            scale,
            dur,
            synth,
            "v2",
            *encode_steps(steps),
        )

    def send_synth(self, name: str, synth: str) -> None:
        self.audio.send(f"/pycodedj/loop/{name}/synth", synth)

    def send_pattern_stop(self, name: str) -> None:
        self.audio.send(f"/pycodedj/loop/{name}/pattern_stop")

    def send_loop_stop(self, name: str) -> None:
        self.audio.send(f"/pycodedj/loop/{name}/voice_count", 0)
        self.audio.send(f"/pycodedj/loop/{name}/pattern_stop")
        if self.visual is not None:
            self.visual.send(f"/pycodedj/loop/{name}/voice_count", 0)

    def send_params(self, name: str, params: "MusicParams") -> None:
        base = f"/pycodedj/loop/{name}"
        # Keep audio updates atomic so SuperCollider does not set params on stale nodes.
        self.audio.send(
            f"{base}/params",
            params.voice_count,
            params.cutoff,
            params.lfo_rate,
            params.reverb_mix,
            params.amp,
            params.low,
            params.mid,
            params.high,
        )
        if self.visual is not None:
            self.visual.send(
                f"{base}/params",
                params.voice_count,
                params.cutoff,
                params.lfo_rate,
                params.reverb_mix,
                params.amp,
                params.low,
                params.mid,
                params.high,
            )
