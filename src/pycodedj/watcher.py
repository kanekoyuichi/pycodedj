from __future__ import annotations

import os
import threading
from pathlib import Path
from typing import Callable

from .block_parser import parse_blocks
from .engine import Engine
from .osc_bridge import OscError


class _LoopFileHandler:
    """ファイル変更イベントを受け取り、デバウンス後に全ループを再評価する。"""

    def __init__(
        self,
        path: str,
        engine: Engine,
        on_eval: Callable[[str, int], None] | None = None,
        debounce: float = 0.3,
    ) -> None:
        self._path = os.path.abspath(path)
        self._engine = engine
        self._on_eval = on_eval
        self._debounce = debounce
        self._timer: threading.Timer | None = None
        self._active_names: set[str] = set()

    def dispatch(self, src_path: str) -> None:
        """watchdog の on_modified から呼ぶ。対象ファイル以外は無視する。"""
        if os.path.abspath(src_path) != self._path:
            return
        if self._timer is not None:
            self._timer.cancel()
        self._timer = threading.Timer(self._debounce, self._eval_all)
        self._timer.start()

    def _eval_all(self) -> None:
        try:
            source = Path(self._path).read_text(encoding="utf-8")
        except OSError:
            return
        blocks = parse_blocks(source)
        current_names = {b.name for b in blocks}

        for name in self._active_names - current_names:
            try:
                self._engine.stop_loop(name)
            except OscError:
                pass
        self._active_names = current_names

        for block in blocks:
            self._engine.eval_block(block)
        if self._on_eval is not None:
            self._on_eval(self._path, len(blocks))


def watch(
    path: str,
    engine: Engine,
    debounce: float = 0.3,
    on_eval: Callable[[str, int], None] | None = None,
) -> None:
    """ファイルを監視し、変更のたびに全ループを再評価する。Ctrl+C で停止。

    Args:
        path: 監視するファイルのパス
        engine: eval_block を呼び出す Engine インスタンス
        debounce: 連続変更イベントをまとめる待機時間（秒）
        on_eval: 再評価後に呼ばれるコールバック (file_path, loop_count)
    """
    try:
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer
    except ImportError:
        raise ImportError(
            "watchdog が必要です: pip install 'pycodedj[watch]'"
        )

    handler_wrapper = _LoopFileHandler(path, engine, on_eval=on_eval, debounce=debounce)

    class _WatchdogAdapter(FileSystemEventHandler):
        def on_modified(self, event: object) -> None:
            src = getattr(event, "src_path", "")
            handler_wrapper.dispatch(str(src))

        # vim/emacs などのアトミックセーブは rename で完了するため on_moved も受ける
        def on_moved(self, event: object) -> None:
            src = getattr(event, "dest_path", "")
            handler_wrapper.dispatch(str(src))

        def on_created(self, event: object) -> None:
            src = getattr(event, "src_path", "")
            handler_wrapper.dispatch(str(src))

    abs_path = os.path.abspath(path)
    watch_dir = os.path.dirname(abs_path)

    observer = Observer()
    observer.schedule(_WatchdogAdapter(), watch_dir, recursive=False)
    observer.start()
    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
