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
        # voice_count を先に送り SC 側でシンセを起動してから各パラメーターを適用させる
        self.audio.send(f"{base}/voice_count", params.voice_count)
        self.audio.send(f"{base}/cutoff", params.cutoff)
        self.audio.send(f"{base}/lfo_rate", params.lfo_rate)
        self.audio.send(f"{base}/reverb", params.reverb_mix)
        if self.visual is not None:
            self.visual.send(f"{base}/voice_count", params.voice_count)
            self.visual.send(f"{base}/cutoff", params.cutoff)
            self.visual.send(f"{base}/lfo_rate", params.lfo_rate)
            self.visual.send(f"{base}/reverb", params.reverb_mix)
