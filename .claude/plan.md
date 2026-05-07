# PyCodeDJ 実装計画

仕様: `.claude/spec.md`

---

## ディレクトリ構成（目標形)

```
pycodedj/
├── pyproject.toml
├── README.md
├── src/
│   └── pycodedj/
│       ├── __init__.py
│       ├── __main__.py          # CLI エントリポイント（eval サブコマンド含む）
│       ├── engine.py            # メインエンジン（ループ管理・ブロック評価）
│       ├── block_parser.py      # # @loop ブロック分割・パース
│       ├── analyzer.py          # AST解析・特徴量抽出
│       ├── mapper.py            # コード特徴量→音楽パラメーター変換
│       ├── osc_bridge.py        # OSC送受信
│       └── watcher.py           # ファイル監視（watchdog、オプション）
├── sc/
│   └── synths.scd               # SuperCollider シンセ定義
├── examples/
│   └── demo.py                  # デモ用ライブコーディングファイル
└── tests/
    ├── test_block_parser.py
    ├── test_analyzer.py
    ├── test_mapper.py
    └── test_osc_bridge.py
```

---

## フェーズ0：マッピング設計の検証

**目標:** ASTマッピング仮説が「音楽として聴こえる」かを人の耳で検証する。コードを書く前に完了する。

**合格条件:** 演奏者が「どのコード変更がどの音楽変化を起こすか」をおおまかに予測できること。

### タスク

#### F0-1: SuperCollider シンセ準備

`sc/synths.scd` に以下のシンセを定義する。

```supercollider
// 基本シンセ（Cutoff・LFOレート・Reverb・Voice数を外部制御可能にする）
// Voice数はシンセを複数起動する方式で制御する（F1で確認後に確定）
SynthDef(\pycodedj_base, {
    arg cutoff=800, lfoRate=0.5, reverbMix=0.2, amp=0.5, gate=1;
    var sig, env, lfo;
    lfo = SinOsc.kr(lfoRate, 0, 0.3, 1);
    sig = Saw.ar(220 * lfo);
    sig = RLPF.ar(sig, cutoff, 0.5);
    env = EnvGen.kr(Env.asr(0.1, 1, 0.2), gate, doneAction: 2);
    sig = FreeVerb.ar(sig, reverbMix) * env * amp;
    Out.ar(0, sig ! 2);
}).add;
```

**OSCアドレス契約（Python→SC）：**

複数ループが同じアドレスを上書きしないよう、ループ名をアドレスに含める。

| MusicParams フィールド | OSC アドレス | 型 | 備考 |
| :--- | :--- | :--- | :--- |
| `cutoff` | `/pycodedj/loop/<name>/cutoff` | float | Hz, 200–4000 |
| `lfo_rate` | `/pycodedj/loop/<name>/lfo_rate` | float | Hz, 0.1–5.0 |
| `reverb_mix` | `/pycodedj/loop/<name>/reverb` | float | 0.0–0.8 |
| `voice_count` | `/pycodedj/loop/<name>/voice_count` | int | 1–4。SCがシンセ起動数を管理 |

SC側はループ名ごとに独立したシンせを持ち、`OSCdef` で受信したアドレスの `<name>` に対応するシンセのパラメーターだけを更新する。このアドレス契約はフェーズ1で実機確認し、変更があれば本表を更新する。

#### F0-2: 手動パラメーター変化の聴取

SC IDE から手動でパラメーターを変化させ、以下を確認する。

| パラメーター | 変化範囲 | 聴取結果の記録先 |
| :--- | :--- | :--- |
| Cutoff | 200〜4000 Hz | `.claude/notes/mapping-validation.md` |
| LFOレート | 0.1〜5.0 Hz | 同上 |
| Reverb Mix | 0.0〜0.8 | 同上 |
| Voice数 | 1〜4 | 同上 |

#### F0-3: マッピング仮説の確定

仕様書のマッピングテーブルを実測値で更新する。廃止・変更したマッピングは理由とともに `spec.md` に記録する。

---

## フェーズ1：プロトタイプ開発

**目標:** PythonからOSC経由でSuperColliderを鳴らし、パラメーターを変更できる最小構成を作る。

### タスク

#### F1-1: プロジェクト初期化

```toml
# pyproject.toml
[project]
name = "pycodedj"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "python-osc>=1.8",
]

[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy"]
watch = ["watchdog>=3.0"]   # ファイル保存トリガー（MVP外）

[project.scripts]
pycodedj = "pycodedj.__main__:main"
```

#### F1-2: OSCブリッジ実装（`osc_bridge.py`）

SC（57120番）とHydra（別ポート）へ別々に送信できるよう、`OscEndpoint` を複数持てる設計にする。

```python
from dataclasses import dataclass, field
from pythonosc import udp_client

@dataclass
class OscEndpoint:
    host: str
    port: int
    _client: udp_client.SimpleUDPClient = field(init=False)

    def __post_init__(self) -> None:
        self._client = udp_client.SimpleUDPClient(self.host, self.port)

    def send(self, address: str, *args) -> None:
        self._client.send_message(address, list(args))

@dataclass
class OscBridge:
    audio: OscEndpoint    # SuperCollider (default: 127.0.0.1:57120)
    visual: OscEndpoint | None = None  # Hydra 等（フェーズ3で使用）

    def send_params(self, name: str, params: "MusicParams") -> None:
        base = f"/pycodedj/loop/{name}"
        self.audio.send(f"{base}/cutoff", params.cutoff)
        self.audio.send(f"{base}/lfo_rate", params.lfo_rate)
        self.audio.send(f"{base}/reverb", params.reverb_mix)
        self.audio.send(f"{base}/voice_count", params.voice_count)
        if self.visual is not None:
            self.visual.send(f"{base}/cutoff", params.cutoff)
            self.visual.send(f"{base}/lfo_rate", params.lfo_rate)
            self.visual.send(f"{base}/reverb", params.reverb_mix)
```

テスト: `test_osc_bridge.py` でSC起動不要なモック送信テスト。`visual=None` のとき visual 側に送らないことを確認。

#### F1-3: SuperCollider 接続確認スクリプト

`examples/hello_sc.py` として単発音を鳴らすスクリプトを作成し、動作を手動確認する。

#### F1-4: SuperCollider TempoClock 構成確認

SC側で `TempoClock` を動かし、Pythonからのパラメーター変更がビートを壊さないことを確認する。

---

## フェーズ2：ブロック評価エンジンの実装

**目標:** `pycodedj eval <file>::<loop名>` を実行したとき、AST解析→マッピング→OSC送出が即時に動き、複数ループを独立して管理できる状態を作る。

### タスク

#### F2-1: ブロックパーサー（`block_parser.py`）

`# @loop <名前> [interval=秒]` から次の `# @loop` までを1ブロックとして分割する。

```python
from dataclasses import dataclass

@dataclass
class LoopBlock:
    name: str
    interval: float      # 秒。未指定時は 1.0
    source: str          # ブロックのソースコード

def parse_blocks(source: str) -> list[LoopBlock]:
    ...
```

テスト: `tests/test_block_parser.py` で以下を確認する。
- 複数ブロックが正しく分割される。
- `interval` の省略時はデフォルト値が入る。
- マーカーのない行はどのブロックにも属さない（無視する）。
- ブロックが0件のときは空リストを返す。

#### F2-2: CLIコマンド `eval`（`__main__.py`）

```bash
pycodedj eval demo.py::bass
```

- ファイルを読んで `parse_blocks` でブロックを取り出す。
- 指定した名前のブロックを `Engine.eval_block(block)` に渡す。
- ブロック名が存在しない場合はエラーメッセージを stderr に出力して終了コード 1 を返す。

#### F2-3: AST解析（`analyzer.py`）

```python
import ast
import tokenize
import io
from dataclasses import dataclass

@dataclass
class CodeFeatures:
    max_depth: int
    control_flow_count: int
    function_count: int
    comment_ratio: float   # コメント行数 / 全行数（空行を除く）

def analyze(source: str) -> CodeFeatures:
    ...
```

`comment_ratio` の実装方針：
- コメントは AST に残らないため、`tokenize.generate_tokens` で `COMMENT` トークンを数える。
- 分母は「空行を除いた実効行数」とする。分母が 0 のときは `0.0` を返す。

テスト: `tests/test_analyzer.py` に複数のコード断片を入力し、期待する特徴量が返ることを確認。コメントなし・コメントのみ・混在の3パターンを含める。

#### F2-4: マッピング変換（`mapper.py`）

```python
from dataclasses import dataclass
from .analyzer import CodeFeatures

@dataclass
class MusicParams:
    cutoff: float        # Hz, 200–4000
    lfo_rate: float      # Hz, 0.1–5.0
    reverb_mix: float    # 0.0–0.8
    voice_count: int     # 1–4

def map_features(features: CodeFeatures) -> MusicParams:
    ...
```

マッピング関数はフェーズ0で確定した値域・カーブを使う。線形スケールが不自然な場合は対数スケールを採用する。

テスト: 境界値・極端な入力でパラメーターが有効範囲外にならないことを確認。

#### F2-5: エンジン（`engine.py`）

ブロック評価パイプラインとループ状態管理を担う。Python は周期イベントを自ら刻まない。SuperCollider 側が TempoClock で刻む。

```python
@dataclass
class Engine:
    bridge: OscBridge
    # ループ名 → 最後に送ったパラメーター（状態管理のみ）
    _loops: dict[str, MusicParams] = field(default_factory=dict, init=False)

    def eval_block(self, block: LoopBlock) -> None:
        try:
            features = analyze(block.source)
            params = map_features(features)
            self.bridge.send_params(block.name, params)  # 評価時に一度だけ送出
            self._loops[block.name] = params             # 最後のパラメーターを記録
        except SyntaxError as e:
            sys.stderr.write(f"[pycodedj] syntax error ({block.name}): {e}\n")
            # 解析エラー時は既存パラメーターをそのまま維持。他ループへの影響なし。

    def stop_loop(self, name: str) -> None:
        self._loops.pop(name, None)
        # SC側に停止シグナルを送る（voice_count=0 等、F1で確定）

    def list_loops(self) -> list[str]:
        return list(self._loops.keys())
```

#### F2-6: 統合動作確認

`examples/demo.py` を用意し、以下を実機で確認する。

```bash
pycodedj eval examples/demo.py::bass
pycodedj eval examples/demo.py::melody
pycodedj eval examples/demo.py::pad
```

- 各コマンドが即時に音色を変える。
- `bass` を更新しても `melody` と `pad` は継続して鳴り続ける。
- 構文エラーのブロックを評価しても他のループが止まらない。

---

## フェーズ3：ビジュアライザー統合

**目標:** OSCで外部ビジュアライザー（Hydra）に音楽パラメーターを送り、音と映像が知覚上同期する状態を作る。

### タスク

#### F3-1: Hydra向けOSC送出

`OscBridge` の `visual` フィールドに Hydra のエンドポイントを設定する。F1-2 で実装済みの `send_params` が `visual` が `None` でなければ自動的に Hydra へも送出する。追加のコード変更は不要で、設定だけで切り替えられることを確認する。

#### F3-2: Hydra スケッチ作成

`examples/hydra_receiver.js` として、OSCを受け取ってパラメーターに応じた映像を描くスケッチを用意する。

#### F3-3: 同期確認

音と映像の変化が「知覚上同期している」と判断できることをデモ演奏で確認する。厳密なサンプル精度の同期は目標としない。

---

## 品質基準

- `pytest` を全フェーズのタスク完了時に実行し、全テストがパスすることを確認する。
- `ruff check src tests` が通ることを確認する。
- `mypy src` が通ることを確認する。
- 各フェーズ完了後に `codex review --uncommitted` を実行する。

---

## 未決定事項

| 項目 | 決定タイミング |
| :--- | :--- |
| LFOレートの対数スケール要否 | フェーズ0 聴取後 |
| Voice数の実装方式（シンせ複数起動 vs 内部ポリ）→ OSCアドレス契約に反映 | フェーズ1 SC確認時 |
| ループ停止シグナルの方式（voice_count=0 等） | フェーズ1 SC確認時 |
| Hydra の OSC 受信ポート番号 | フェーズ3 開始前 |
| Hydra以外のビジュアライザー採用可否 | フェーズ3 開始前 |

---

## 将来対応（MVP外）

- **ファイル保存トリガー（`watcher.py`）:** `watchdog` を使ってファイル変更を検知し、`eval_block` を自動呼び出しする。デバウンス時間は実機確認後に決定する。
- **VS Code 拡張:** カーソル位置のブロックを Cmd+Enter で評価する。`pycodedj eval` を内部で呼ぶだけなので拡張本体は薄い。
