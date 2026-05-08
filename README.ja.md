# PyCodeDJ

[English README](https://github.com/kanekoyuichi/pycodedj/blob/main/README.md) · [マニュアル (JA)](https://github.com/kanekoyuichi/pycodedj/blob/main/docs/manual.ja.md) · [Full Manual (EN)](https://github.com/kanekoyuichi/pycodedj/blob/main/docs/manual.md)

Pythonコードの構造をリアルタイムに音楽へ変換するライブコーディング環境。ファイルを保存するたびに演奏が変わる。

---

## コンセプト

PyCodeDJ は「コードを書くこと」と「音を鳴らすこと」を直結させます。

関数を増やせばポリフォニーが広がり、ネストを深くすればフィルターが開き、コメントを書き込めば空間が広がる。コードの構造そのものが楽器です。

既存の Python ↔ SuperCollider ブリッジ（sc3nb・supriya）との違いは2点です。

- **ホットリロード演奏** — ループを止めずにファイルを差し替える。保存が即座に音の変化になる。
- **コード構造の可聴化** — AST解析で抽出した構造的特徴量（深さ・分岐数・関数数など）を音楽パラメーターへ自動変換する。

---

## アーキテクチャ

```
[Python エンジン]  →OSC→  [SuperCollider]  →音響出力→  スピーカー
      ↓ OSC
  [Hydra 等]  →映像出力→  スクリーン
```

| 層 | 役割 | 技術 |
| :--- | :--- | :--- |
| 制御層 | コード解析・スケジューリング・OSC送出 | Python 3.10+, python-osc, watchdog |
| 音響層 | リアルタイム音響合成 | SuperCollider (scsynth) |
| 視覚層 | 音楽データに同期した映像生成 | Hydra または Pyxel |

BPMクロックは SuperCollider 側の `TempoClock` が保持します。Python は「次のループで使う設定の更新」をOSCで送るだけに徹し、タイミング精度は SuperCollider に委ねます。

---

## コード構造 → 音楽パラメーターのマッピング

| コード特徴量 | 音楽パラメーター | 音楽的根拠 |
| :--- | :--- | :--- |
| ネストの深さ（最大） | フィルター Cutoff (200–4000 Hz) | 深い構造＝複雑さ＝音色の明るさ |
| 制御フロー数（if/for/while） | LFO レート (0.1–5.0 Hz) | 分岐の多さ＝揺らぎの速さ |
| 関数定義数 | ポリフォニー声部数 (1–4) | 関数＝独立した声部 |
| コメント率 | リバーブ Depth (0.0–0.8) | 余白の多さ＝空間の広さ |
| `volume=` 引数 | Amplitude (0.0–1.0) | 演奏者が直接音量を制御する |
| `eq=` / `low=` / `mid=` / `high=` 引数 | 簡易 3 バンド EQ | ループごとの音質補正 |

テンポ（BPM）と基音（Pitch）は演奏者が明示的に制御します。保存のたびに楽曲全体の土台が変わることを防ぐためです。

---

## インストール

**必要なもの**

- Python 3.10 以上
- SuperCollider（scsynth が起動できる環境）

```bash
pip install 'pycodedj[watch]'
```

`[watch]` を付けると `pycodedj watch` コマンドも使えるようになります。

開発用:

```bash
git clone https://github.com/yourname/pycodedj
cd pycodedj
pip install -e ".[dev]"
```

---

## クイックスタート

**1. SuperCollider を起動し、シンセを読み込む**

SuperCollider IDE で `sc/synths.scd` を開いて実行します。

**2. ライブコーディングファイルを用意する**

```python
from pycodedj import loop

@loop("bass", interval=2.0)
def bass(volume=0.4):
    for i in range(8):
        if i % 2 == 0:
            pass

@loop("melody", interval=0.5)
def melody(volume=0.3):
    x = 1
    y = 2
    return x + y

@loop("pad", interval=4.0)
def pad(volume=0.15):
    # 空間を作る
    # もう少し余白
    pass
```

**3. ブロックを評価する**

```bash
pycodedj eval demo.py::bass
```

成功すると次のフィードバックが表示されます。

```
[pycodedj] bass  cutoff=418Hz  lfo=1.08Hz  reverb=0.00  voices=1  amp=0.40
```

他のループはそのまま鳴り続けます。

**4. watch モードでライブコーディング**

毎回 eval を打つ代わりに、ファイル保存で全ループを自動再評価できます。

```bash
pycodedj watch demo.py
```

あとはエディタでコードを書いて保存するだけです。

**5. 緊急停止**

```bash
pycodedj panic
```

全アクティブループに停止信号を即時送信します。演奏中に問題が起きたときに使います。

**6. ミュート / ソロ**

```bash
pycodedj mute bass        # ループを消音（停止はしない）
pycodedj unmute bass      # 音量を元に戻す
pycodedj solo pad         # pad 以外を全ミュート
pycodedj unsolo           # ソロ解除、ミュート状態を元に戻す
```

注意: `mute` / `unmute` / `solo` / `unsolo` は OSC を直接 SuperCollider に送信します。完全な状態管理が必要な場合は watch セッション内で `Engine.mute()` / `Engine.solo()` を呼び出してください。

**7. ループのステータス確認**

```bash
pycodedj status
```

アクティブなループの名前・ミュート状態・音量・フィルターカットオフを表示します。

---

## サンプルファイル

| ファイル | 内容 |
| :--- | :--- |
| `examples/demo.py` | bass / melody / pad の 3 ループ入門デモ |
| `examples/club_set.py` | EDM クラブグルーヴ（8 ループ、キック → アシッドベース → レイブスタブ → Hoover → シマー） |
| `examples/sound_showcase.py` | 全 30 音色を収録 — 1 音ずつ eval して確認できる |

---

## ライブコーディング例

### ネストを深くするとフィルターが開く

```python
from pycodedj import loop

@loop("bass", interval=2.0)
def bass(volume=0.4):
    for i in range(4):       # 制御フロー +1
        for j in range(4):   # ネスト深さ +1、制御フロー +1
            if i == j:       # ネスト深さ +1、制御フロー +1
                pass
```

### 関数を増やすとポリフォニーが広がる

```python
from pycodedj import loop

@loop("chord", interval=1.0)
def chord(volume=0.2):
    def voice_a(): pass
    def voice_b(): pass
    def voice_c(): pass
    def voice_d(): pass
```

### コメントを増やすと空間（リバーブ）が広がる

```python
from pycodedj import loop

@loop("pad", interval=4.0)
def pad(volume=0.15):
    # ここに余白を置く
    # もう少し置く
    # 静寂も音楽
    pass
```

---

## OSC アドレス仕様

SuperCollider との通信に使うアドレスです。

| アドレス | 型 | 値域 | 対応パラメーター |
| :--- | :--- | :--- | :--- |
| `/pycodedj/loop/<name>/params` | int, float, float, float, float | パラメーター順を参照 | `voice_count`, `cutoff`, `lfo_rate`, `reverb`, `amp` |
| `/pycodedj/loop/<name>/cutoff` | float | 200–4000 Hz | フィルター Cutoff（互換用） |
| `/pycodedj/loop/<name>/lfo_rate` | float | 0.1–5.0 Hz | LFO レート（互換用） |
| `/pycodedj/loop/<name>/reverb` | float | 0.0–0.8 | リバーブ Depth（互換用） |
| `/pycodedj/loop/<name>/voice_count` | int | 1–4 | ポリフォニー声部数（互換用） |
| `/pycodedj/loop/<name>/amp` | float | 0.0–1.0 | Amplitude（互換用） |

`<name>` はブロック名（`bass`、`melody` など）です。ループごとに独立したアドレスを持つため、複数ループが同じパラメーターを上書きしません。

Hydra 等の外部ビジュアライザーへは同じパラメーターを別ポートに送信します。

---

## 動作環境

- **推奨OS:** macOS（Core Audio の低遅延性を活用）または Linux（Raspberry Pi 5 等）
- **Python:** 3.10 以上
- **SuperCollider:** 3.12 以上

---

## ロードマップ

- [x] Python → SuperCollider OSC プロトタイプ
- [x] ホットリロード・ライブループ実装（`pycodedj watch`）
- [x] Sprint 1: ライブ安定性（`panic`, SyntaxError維持, `mute`/`solo`, `status`）
- [ ] Sprint 2: 音楽DSL（`pattern()`, `sample()`, `@loop` パラメータ拡張, mapping モード）
- [ ] Sprint 3: 音色・演奏性（SynthDef整理, `bpm`, `list-synths`）
- [ ] Sprint 4: README・マニュアル刷新、Hydra ビジュアライザー統合

---

## ライセンス

MIT + Commons Clause — 個人利用・改変・ライブパフォーマンス（有料公演含む）は自由です。ソフトウェアそのものの販売・有償サービス化は禁止しています。詳細は [LICENSE](LICENSE) を参照してください。
