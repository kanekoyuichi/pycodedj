# PyCodeDJ

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

テンポ（BPM）と基音（Pitch）は演奏者が明示的に制御します。保存のたびに楽曲全体の土台が変わることを防ぐためです。

---

## インストール

**必要なもの**

- Python 3.10 以上
- SuperCollider（scsynth が起動できる環境）

```bash
pip install pycodedj
```

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
# @loop bass interval=2.0
def bass():
    for i in range(8):
        if i % 2 == 0:
            pass

# @loop melody interval=0.5
def melody():
    x = 1
    y = 2
    return x + y

# @loop pad interval=4.0
def pad():
    # 空間を作る
    # もう少し余白
    pass
```

**3. ブロックを評価する**

```bash
pycodedj eval demo.py::bass
pycodedj eval demo.py::melody
pycodedj eval demo.py::pad
```

コマンドを実行した瞬間に、そのブロックのコード構造が解析されて音色が変わります。他のループはそのまま鳴り続けます。ファイルを保存する必要はありません。

---

## ライブコーディング例

### ネストを深くするとフィルターが開く

```python
# @loop bass interval=2.0
def bass():
    for i in range(4):       # 制御フロー +1
        for j in range(4):   # ネスト深さ +1、制御フロー +1
            if i == j:       # ネスト深さ +1、制御フロー +1
                pass
```

### 関数を増やすとポリフォニーが広がる

```python
# @loop chord interval=1.0
def voice_a(): pass
def voice_b(): pass
def voice_c(): pass
def voice_d(): pass
```

### コメントを増やすと空間（リバーブ）が広がる

```python
# @loop pad interval=4.0
# ここに余白を置く
# もう少し置く
# 静寂も音楽
def pad(): pass
```

---

## OSC アドレス仕様

SuperCollider との通信に使うアドレスです。

| アドレス | 型 | 値域 | 対応パラメーター |
| :--- | :--- | :--- | :--- |
| `/pycodedj/cutoff` | float | 200–4000 Hz | フィルター Cutoff |
| `/pycodedj/lfo_rate` | float | 0.1–5.0 Hz | LFO レート |
| `/pycodedj/reverb` | float | 0.0–0.8 | リバーブ Depth |
| `/pycodedj/voice_count` | int | 1–4 | ポリフォニー声部数 |

Hydra 等の外部ビジュアライザーへは同じパラメーターを別ポートに送信します。

---

## 動作環境

- **推奨OS:** macOS（Core Audio の低遅延性を活用）または Linux（Raspberry Pi 5 等）
- **Python:** 3.10 以上
- **SuperCollider:** 3.12 以上

---

## ロードマップ

- [x] 仕様設計・マッピング設計
- [ ] フェーズ0: マッピング仮説の聴取検証
- [ ] フェーズ1: Python → SuperCollider OSC プロトタイプ
- [ ] フェーズ2: ホットリロード・ライブループ実装
- [ ] フェーズ3: Hydra ビジュアライザー統合

---

## ライセンス

MIT
