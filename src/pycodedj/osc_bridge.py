from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pythonosc import udp_client

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
