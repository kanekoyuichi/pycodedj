# PyCodeDJ

[English README](https://github.com/kanekoyuichi/pycodedj/blob/main/README.md) · [マニュアル (JA)](https://github.com/kanekoyuichi/pycodedj/blob/main/docs/manual.ja.md) · [Full Manual (EN)](https://github.com/kanekoyuichi/pycodedj/blob/main/docs/manual.md)

Python のコードを書くと、リアルタイムに音が変わるライブコーディング環境。ファイルを保存するたびに演奏が変わる。

---

## コンセプト

PyCodeDJ は「コードを書くこと」と「音を鳴らすこと」を直結させます。

`for` ループを増やすと音の揺らぎが速くなり、ネストを深くするとフィルターが開き、コメントを書き込むと空間が広がります。`pattern("x . x .")` と書けばそのリズムで音が鳴り、`pattern("0 . 3 . 5 .")` と書けば指定した音程で演奏されます。

既存の Python ↔ SuperCollider ブリッジ（sc3nb・supriya）との違いは 2 点です。

- **ホットリロード演奏** — ループを止めずにファイルを差し替える。保存が即座に音の変化になる
- **2 つの演奏スタイル** — コードの構造から自動生成するモードと、`pattern()` で音程とリズムを明示指定するモードを自由に混在させられる

---

## アーキテクチャ

```
[Python エンジン]  →OSC→  [SuperCollider]  →音響出力→  スピーカー
      ↓ OSC
  [Hydra 等]  →映像出力→  スクリーン
```

| 層 | 役割 | 技術 |
| :--- | :--- | :--- |
| 制御層 | コード解析・スケジューリング・OSC 送出 | Python 3.10+, python-osc, watchdog |
| 音響層 | リアルタイム音響合成 | SuperCollider (scsynth) |
| 視覚層 | 音楽データに同期した映像生成 | Hydra または Pyxel |

BPM クロックは SuperCollider 側の `TempoClock` が保持します。Python は「次のループで使う設定の更新」を OSC で送るだけで、タイミング精度は SuperCollider に委ねます。

---

## コード構造 → 音楽パラメーターのマッピング

| コード特徴量 | 音楽パラメーター |
| :--- | :--- |
| ネストの深さ（最大） | フィルター Cutoff (200–4000 Hz) |
| 制御フロー数（if/for/while） | LFO レート (0.1–5.0 Hz) |
| 関数定義数 | ポリフォニー声部数 (1–4) |
| コメント率 | リバーブ Depth (0.0–0.8) |
| `volume=` 引数 | Amplitude (0.0–1.0) |
| `eq=` / `low=` / `mid=` / `high=` 引数 | 簡易 3 バンド EQ |

---

## インストール

**必要なもの**

- Python 3.10 以上
- SuperCollider（scsynth が起動できる環境）

```bash
pip install 'pycodedj[watch]'
```

`[watch]` を付けると `pycodedj watch` コマンドも使えます。

開発用:

```bash
git clone https://github.com/kanekoyuichi/pycodedj
cd pycodedj
pip install -e ".[dev]"
```

---

## クイックスタート

**1. SuperCollider を起動してシンセを読み込む**

SuperCollider IDE で `sc/synths.scd` を開き、Ctrl+A（Mac は Cmd+A）→ Ctrl+Enter（Mac は Cmd+Enter）で実行します。Post window に次が出れば準備完了です。

```
PyCodeDJ synths loaded. Ready. OSC port: 57120
```

**2. ライブコーディングファイルを用意する**

```python
from pycodedj import loop, pattern

# コードの「構造」が音楽パラメーターになるモード
@loop("bass", interval=2.0)
def bass(volume=0.4):
    for i in range(8):
        if i % 2 == 0:
            pass

# pattern() でリズムと音程を明示指定するモード
@loop("kick", synth="floor_kick", dur=0.25)
def kick():
    pattern("x . x .")

@loop("melody", synth="acid_lead", root="A3", scale="minor", dur=0.25)
def melody():
    pattern("0 . 3 . 5 .")

# コメントで空間を作るモード
@loop("pad", interval=4.0)
def pad(volume=0.1):
    # 背景の空気
    # 余白
    pass
```

**3. watch モードで起動する**

```bash
pycodedj watch demo.py
```

あとはエディタでコードを書いて保存するだけです。保存のたびに全ループが再評価されます。

**4. 緊急停止**

```bash
pycodedj panic
```

**5. ミュート / アンミュート**

```bash
pycodedj mute bass
pycodedj unmute bass
```

---

## pattern() の使い方

`pattern()` を使うと、リズムと音程を明示的に指定できます。

```python
from pycodedj import loop, pattern

# トリガーパターン（x=鳴らす、.=休符）
@loop("kick", synth="floor_kick", dur=0.25)
def kick():
    pattern("x . x .")

# 音程パターン（数字=スケール度数）
@loop("bass", synth="bass_acid", root="A1", scale="minor", dur=0.25)
def bass():
    pattern("0 . 3 . 5 .")
```

`@loop` に渡す引数:

| 引数 | 説明 |
| :--- | :--- |
| `synth=` | 使うシンセ名 |
| `root=` | ルートノート（例: `"A3"`, `"C4"`） |
| `scale=` | スケール（例: `"minor"`, `"major"`, `"pentatonicMinor"`） |
| `dur=` | 1 ステップの長さ（秒）。`0.25` で 16 分音符相当 |

---

## サンプルファイル

| ファイル | 内容 |
| :--- | :--- |
| `examples/demo.py` | bass / melody / pad の 3 ループ入門デモ |
| `examples/club_set.py` | EDM クラブグルーヴ（キック・ベース・ハット・コード・パッドを含む 8 ループ） |
| `examples/sound_showcase.py` | 全 30 音色 — 1 音ずつ eval して確認できる |

---

## OSC アドレス仕様

| アドレス | 型 | 対応パラメーター |
| :--- | :--- | :--- |
| `/pycodedj/loop/<name>/params` | int, float, float, float, float | `voice_count`, `cutoff`, `lfo_rate`, `reverb`, `amp` |
| `/pycodedj/loop/<name>/pattern` | int, str, float, str, int… | パターンデータ |
| `/pycodedj/loop/<name>/pattern_stop` | — | パターン停止 |
| `/pycodedj/loop/<name>/amp` | float | 音量（互換用） |

---

## 動作環境

- **推奨 OS:** macOS（Core Audio の低遅延性を活用）または Linux（Raspberry Pi 5 等）
- **Python:** 3.10 以上
- **SuperCollider:** 3.12 以上

---

## ロードマップ

- [x] Python → SuperCollider OSC プロトタイプ
- [x] ホットリロード・ライブループ実装（`pycodedj watch`）
- [x] Sprint 1: ライブ安定性（`panic`, SyntaxError 維持, `mute`/`solo`, `status`）
- [x] Sprint 2: 音楽 DSL（`pattern()`, `@loop` パラメータ拡張: `synth`, `root`, `scale`, `dur`）
- [ ] Sprint 3: 音色・演奏性（SynthDef 整理, `bpm`, `list-synths`, `sample()`）
- [ ] Sprint 4: Hydra ビジュアライザー統合

---

## ライセンス

MIT + Commons Clause — 個人利用・改変・ライブパフォーマンス（有料公演含む）は自由です。ソフトウェアそのものの販売・有償サービス化は禁止しています。詳細は [LICENSE](LICENSE) を参照してください。
