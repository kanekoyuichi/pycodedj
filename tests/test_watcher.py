import time
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pycodedj.watcher import _LoopFileHandler


def _make_handler(
    path: str = "/tmp/demo.py",
    debounce: float = 0.0,
) -> tuple[_LoopFileHandler, MagicMock]:
    engine = MagicMock()
    handler = _LoopFileHandler(path=path, engine=engine, debounce=debounce)
    return handler, engine


_BASS_BLOCK = '@loop("bass")\ndef f(): pass\n'
_BASS_PAD_BLOCK = '@loop("bass")\ndef bass(): pass\n@loop("pad")\ndef pad(): pass\n'
_BASS_MELODY_BLOCK = '@loop("bass")\ndef bass(): pass\n@loop("melody")\ndef melody(): pass\n'


def test_dispatch_calls_eval_for_target_file(tmp_path: Path) -> None:
    target = tmp_path / "demo.py"
    target.write_text(_BASS_BLOCK)
    handler, engine = _make_handler(path=str(target), debounce=0.0)

    handler.dispatch(str(target))
    time.sleep(0.05)

    assert engine.eval_block.call_count == 1


def test_dispatch_ignores_other_files(tmp_path: Path) -> None:
    target = tmp_path / "demo.py"
    target.write_text(_BASS_BLOCK)
    other = tmp_path / "other.py"
    handler, engine = _make_handler(path=str(target), debounce=0.0)

    handler.dispatch(str(other))
    time.sleep(0.05)

    engine.eval_block.assert_not_called()


def test_debounce_collapses_rapid_events(tmp_path: Path) -> None:
    target = tmp_path / "demo.py"
    target.write_text(_BASS_BLOCK)
    handler, engine = _make_handler(path=str(target), debounce=0.1)

    for _ in range(5):
        handler.dispatch(str(target))

    time.sleep(0.25)

    assert engine.eval_block.call_count == 1


def test_eval_all_loops_in_file(tmp_path: Path) -> None:
    target = tmp_path / "demo.py"
    target.write_text(_BASS_MELODY_BLOCK)
    handler, engine = _make_handler(path=str(target), debounce=0.0)

    handler.dispatch(str(target))
    time.sleep(0.05)

    assert engine.eval_block.call_count == 2


def test_eval_now_evaluates_without_file_event(tmp_path: Path) -> None:
    target = tmp_path / "demo.py"
    target.write_text(_BASS_BLOCK)
    handler, engine = _make_handler(path=str(target), debounce=0.0)

    handler.eval_now()

    assert engine.eval_block.call_count == 1


def test_on_eval_callback_called(tmp_path: Path) -> None:
    target = tmp_path / "demo.py"
    target.write_text(_BASS_BLOCK)
    engine = MagicMock()
    callback = MagicMock()
    handler = _LoopFileHandler(
        path=str(target), engine=engine, on_eval=callback, debounce=0.0
    )

    handler.dispatch(str(target))
    time.sleep(0.05)

    callback.assert_called_once_with(str(target), 1)


def test_eval_all_stops_removed_loop(tmp_path: Path) -> None:
    target = tmp_path / "demo.py"
    target.write_text(_BASS_PAD_BLOCK)
    handler, engine = _make_handler(path=str(target), debounce=0.0)

    # 1 回目: bass と pad を評価して _active_names を確立
    handler.dispatch(str(target))
    time.sleep(0.05)

    # pad を削除して 2 回目
    target.write_text(_BASS_BLOCK)
    handler.dispatch(str(target))
    time.sleep(0.05)

    engine.stop_loop.assert_called_once_with("pad")


def _make_watchdog_adapter(target_path: str, engine: MagicMock) -> Any:
    """watch() を mocked watchdog で起動し、schedule に渡された _WatchdogAdapter を返す。"""
    captured: list[Any] = []

    # _WatchdogAdapter が継承するための最小限のスタブクラス
    class _FakeHandler:
        pass

    mock_events = MagicMock()
    mock_events.FileSystemEventHandler = _FakeHandler

    mock_obs_cls = MagicMock()
    mock_obs_inst = mock_obs_cls.return_value
    mock_obs_inst.schedule.side_effect = lambda h, *a, **kw: captured.append(h)
    # 1回目の join で KeyboardInterrupt → except 内の 2回目は None で正常終了
    mock_obs_inst.join.side_effect = [KeyboardInterrupt, None]

    mock_observers = MagicMock()
    mock_observers.Observer = mock_obs_cls

    with patch.dict("sys.modules", {
        "watchdog": MagicMock(),
        "watchdog.events": mock_events,
        "watchdog.observers": mock_observers,
    }):
        from pycodedj.watcher import watch
        watch(target_path, engine, debounce=0.0)

    return captured[0]


def test_adapter_on_moved_fires_eval(tmp_path: Path) -> None:
    target = tmp_path / "demo.py"
    target.write_text(_BASS_BLOCK)
    engine = MagicMock()

    adapter = _make_watchdog_adapter(str(target), engine)
    engine.reset_mock()

    event = MagicMock()
    event.dest_path = str(target)
    adapter.on_moved(event)
    time.sleep(0.05)

    assert engine.eval_block.call_count == 1


def test_adapter_on_created_fires_eval(tmp_path: Path) -> None:
    target = tmp_path / "demo.py"
    target.write_text(_BASS_BLOCK)
    engine = MagicMock()

    adapter = _make_watchdog_adapter(str(target), engine)
    engine.reset_mock()

    event = MagicMock()
    event.src_path = str(target)
    adapter.on_created(event)
    time.sleep(0.05)

    assert engine.eval_block.call_count == 1


def test_adapter_on_moved_ignores_wrong_dest(tmp_path: Path) -> None:
    target = tmp_path / "demo.py"
    target.write_text(_BASS_BLOCK)
    other = tmp_path / "other.py"
    engine = MagicMock()

    adapter = _make_watchdog_adapter(str(target), engine)
    engine.reset_mock()

    event = MagicMock()
    event.dest_path = str(other)
    adapter.on_moved(event)
    time.sleep(0.05)

    engine.eval_block.assert_not_called()


def test_syntax_error_does_not_stop_loops(tmp_path: Path) -> None:
    target = tmp_path / "demo.py"
    target.write_text(_BASS_BLOCK)
    handler, engine = _make_handler(path=str(target), debounce=0.0)

    # 1回目: 正常評価で _active_names を確立
    handler.eval_now()

    # SyntaxError なファイルに書き換えて再評価
    target.write_text("def broken(:")
    handler.dispatch(str(target))
    time.sleep(0.05)

    # SyntaxError 時は stop_loop を呼ばない
    engine.stop_loop.assert_not_called()


def test_watch_raises_on_missing_watchdog() -> None:
    import builtins
    real_import = builtins.__import__

    def mock_import(name: str, *args: object, **kwargs: object) -> object:
        if name == "watchdog.observers" or name == "watchdog.events":
            raise ImportError("no module")
        return real_import(name, *args, **kwargs)  # type: ignore[arg-type]

    with patch("builtins.__import__", side_effect=mock_import):
        from pycodedj.watcher import watch
        with pytest.raises(ImportError, match="watchdog"):
            watch("/tmp/demo.py", MagicMock())
