# Changelog

## [0.5.1] - 2026-05-08

### Improvements

- `examples/club_set.py` を `pattern()` / `synth=` ベースの重低音クラブセットに刷新。4つ打ちキック、ランブル、サブ、アシッド、ハット、フィル、空間ノイズを含む 11 ループ構成に変更
- `pycodedj --version` を追加し、公開前チェックでパッケージバージョンを確認できるようにした

### Docs

- `docs/manual.ja.md` / `docs/manual.md` / `docs/manual.html` — ループ名と音色名の違いを明確化し、音色は `synth=` で指定することを追記
- `docs/manual.ja.md` / `docs/manual.md` / `docs/manual.html` — `examples/club_set.py` の重低音クラブセットの使い方と主要レイヤー一覧を追加
- `README.ja.md` / `README.md` — `examples/club_set.py` の説明を現在の 11 ループ構成に更新

## [0.5.0] - 2026-05-08

### Features

- `pattern()` にコード構文 `[0 3]` を追加。1 ステップで複数の度数を同時発音できる
- `pattern()` にタイ構文 `~` を追加。直前の音（または コード）を次のステップまで延長できる

### Improvements

- OSC パターン payload を v2 フォーマット（`"v2"` マーカー付き flat encoding）に統一
- SC 側 `~setupPattern` を v2 専用 decode に変更。`\sustain` を `Pseq` で制御し、chord/tie の発音長を正確に管理
- `encode_steps()` を `pattern.py` に追加。Python 内部の `list[PatternStep]` を OSC flat encoding に変換する

---

## [0.4.0] - 2026-05-08

### Features

- `pattern()` ヘルパー — `x`（トリガー）・`.`（休符）・整数（スケール度数）で構成したパターン文字列を SuperCollider に送信し `Pdef + Pbind` で再生する
- `@loop` デコレータに `synth=`, `root=`, `scale=`, `dur=` 引数を追加。`pattern()` ループでシンセ・ルートノート・スケール・ステップ長を指定できる
- `pycodedj_note` SynthDef を追加。音程パターン（度数を含む場合）は自動的にこのシンセで再生される
- `send_pattern` / `send_pattern_stop` / `send_synth` を `OscBridge` に追加
- SC 側: `~patterns` 辞書でアクティブな `Pdef` を追跡。`~startLoop` でパターン中のループに対して従来のシンセループが二重起動されないよう保護

### Improvements

- `block_parser._extract_pattern_call` を `ast.walk`（全ノード走査）から DFS preorder + ネストスコープ除外に変更。ネストされたヘルパー関数内の `pattern()` 呼び出しを誤検出しなくなった
- パターン引数の検証を OSC 送信より前に行い、検証失敗時に状態が更新されないよう修正（アトミック更新）
- パターンループは `voice_count=0` を送信し従来のシンセループを抑制。ミュート状態でも Pdef を停止しないよう `~applyLoopParams` を修正
- 度数トークンがある場合は `synth=` 指定の有無にかかわらず `pycodedj_note` を使用（既存シンセは `freq` を消費しないため）

### Docs

- `docs/manual.ja.md` / `docs/manual.md` / `docs/manual.html` — マニュアル全面改訂。`pattern()` の使い方（第 7 章）を新設し、初心者向けに丁寧に再構成
- `README.ja.md` / `README.md` — Sprint 2 機能（`pattern()`, `@loop` 拡張）の説明を追加、ロードマップの Sprint 2 を完了に更新

## [0.3.0] - 2026-05-08

### Features

- `pycodedj panic` — 全アクティブループを即時停止。SuperCollider 側でシンセを解放し `~loops` / `~loopParams` を初期化する
- `pycodedj mute <name>` — ループを消音（停止しない）。再評価時もミュート状態を維持
- `pycodedj unmute <name>` — ミュート解除、音量を復元
- `pycodedj solo <name>` — 対象ループ以外を全ミュート（CLI は OSC 直送、完全な状態管理は watch セッション内の `Engine.solo()` 推奨）
- `pycodedj unsolo` — ソロ解除、solo 前のミュート状態に戻す
- `pycodedj status` — アクティブループの名前・ミュート状態・音量・カットオフを表示

### Improvements

- `ParseResult` dataclass 導入 — `parse_blocks()` が SyntaxError 時に `ParseResult(ok=False, error=...)` を返すようになり、watch モードでコード編集中に構文エラーがあっても演奏中のループが止まらなくなった
- `Engine` 内部状態を `LoopState` dataclass で管理 — `muted` / `muted_before_solo` フラグを保持し、mute/solo/unsolo の状態を正確に追跡
- `eval_block` が OSC 送信成功後に内部状態を更新するよう修正（送信失敗時の状態不整合を解消）
- `Engine.solo()` に未知のループ名ガードを追加（存在しない名前を渡しても全ループがミュートされない）
- CLI `unmute` が SuperCollider に永続化された `amp=0` を上書きしてから voice_count を送るよう修正

### Docs

- README.md / README.ja.md — panic / mute / unmute / status のクイックリファレンスを追加、ロードマップの Sprint 1 を完了に更新
- `docs/manual.md` / `docs/manual.ja.md` / `docs/manual.html` — セクション 12 に新コマンド 6 つの全リファレンスを追加

## [0.2.1] - 2026-05-08

### Docs

- `docs/manual.html` — Python シンタックスハイライターのプレースホルダー衝突バグを修正。`PY_NUMBER` がプレースホルダーのインデックス数字にマッチしてコメント・文字列が正しく表示されない問題を解消

## [0.2.0] - 2026-05-08

### Breaking

- `# @loop <name> interval=<sec>` コメント構文を廃止。`@loop("name", interval=sec)` デコレータ構文に移行
- 既存のライブコーディングファイルはデコレータ構文への書き換えが必要

### Features

- `@loop("name", interval=sec)` デコレータ — ファイルをそのまま `python` で実行できる no-op デコレータとして `from pycodedj import loop` で提供
- `volume=` 引数 — ループ関数のデフォルト引数として音量を直接指定できる（例: `def my_loop(volume=0.4):`）
- Amplitude パラメーター（`amp`）を OSC で SuperCollider に送出。`/pycodedj/loop/<name>/params` は `voice_count, cutoff, lfo_rate, reverb, amp` の 5 値に拡張

### Improvements

- `sc/synths.scd` — `amp` パラメーターをすべての SynthDef と OSC ハンドラーに追加
- `examples/club_set.py` — 6 層 14 ループ構成のクラブセットに刷新（foundation / movement / body / harmonic / space / texture）
- `examples/demo.py` — 新デコレータ構文に更新

### Docs

- README.md / README.ja.md — 新デコレータ構文・`volume=` 引数・`amp` OSC パラメーターに全面更新
- `docs/manual.md` / `docs/manual.ja.md` — 同上
- `docs/index.html` — ライブデモアニメーションとコード例を新構文に更新

## [0.1.4] - 2026-05-07

### Fixes

- Fix editable installs so `pycodedj.__main__` resolves from `src/pycodedj`
- Fix SuperCollider OSC receiving and address parsing for `/pycodedj/loop/<name>/<param>` messages
- Keep the SuperCollider OSC receiver active across repeated `synths.scd` reloads

## [0.1.3] - 2026-05-07

### Fixes

- Add `readme = "README.md"` to `pyproject.toml` so PyPI shows the project description

## [0.1.2] - 2026-05-07

### Features

- License changed to MIT + Commons Clause — personal use, modification, and live performances (including paid shows) are permitted; selling or commercially distributing the software itself is not

### Docs

- Add project homepage at `docs/index.html` with live demo animation and accurate engine-computed parameter values
- Add visualizer concept page at `docs/visualizer-concept.html` showing Canvas 2D animation synced to music parameters

## [0.1.1] - 2026-05-07

### Docs

- Add cross-language links between English and Japanese README and manual using absolute GitHub URLs
- Rename publish workflow file to `workflow.yml`

## [0.1.0] - 2026-05-07

### Features

- `pycodedj eval FILE::LOOP` — evaluate a loop block and send OSC parameters to SuperCollider; prints feedback (`cutoff`, `lfo_rate`, `reverb_mix`, `voice_count`) on success and exits with code 1 on failure
- `pycodedj watch FILE` — watch a file and re-evaluate all loops on every save; handles atomic saves (vim/Emacs rename-based writes) via `on_moved` and `on_created` in addition to `on_modified`; stops loops that are removed from the file between reloads
- OSC bridge sends `voice_count` first so SuperCollider creates synths before receiving parameter updates
- AST-based code analysis maps block nesting depth → filter cutoff, control-flow count → LFO rate, function count → polyphony voices, comment ratio → reverb depth
- `sc/synths.scd` — SuperCollider synth definitions with a single `OSCFunc(nil path)` handler dispatching all `/pycodedj/loop/<name>/<param>` messages
- `examples/demo.py` and `examples/club_set.py` bundled in the wheel as package data

### Docs

- `README.ja.md` and `README.md` with architecture overview, quick start, and OSC address reference
- `docs/manual.ja.md` and `docs/manual.md` — beginner-friendly full manual covering setup, watch mode, code-to-sound mapping, club set example, and troubleshooting
