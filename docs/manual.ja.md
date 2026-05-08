# PyCodeDJ マニュアル

[English manual](https://github.com/kanekoyuichi/pycodedj/blob/main/docs/manual.md)

> Python のコードを書くと、音が変わる

---

## このマニュアルについて

プログラムを書いたことがあれば、誰でも試せます。音楽の知識は不要です。SuperCollider は「名前も聞いたことがない」で大丈夫です。

このマニュアルを順番に読んでいくと、最終的に **自分が書いた Python コードから音が鳴る体験** ができます。セットアップも含めて 20〜30 分が目安です。

---

## 目次

1. [PyCodeDJ って何？](#1-pycodedj-って何)
2. [インストールする](#2-インストールする)
3. [SuperCollider をセットアップする](#3-supercollider-をセットアップする)
4. [はじめての音を出す](#4-はじめての音を出す)
5. [watch モード — 保存するだけで音が変わる](#5-watch-モード--保存するだけで音が変わる)
6. [コードの構造が音を変える](#6-コードの構造が音を変える)
7. [pattern() で音程とリズムを指定する](#7-pattern-で音程とリズムを指定する)
8. [複数のループを同時に動かす](#8-複数のループを同時に動かす)
9. [音色リファレンス](#9-音色リファレンス)
10. [演奏のアイデア](#10-演奏のアイデア)
11. [うまくいかないとき](#11-うまくいかないとき)
12. [コマンドと設定の全リスト](#12-コマンドと設定の全リスト)
13. [仕組みをもっと知りたい人へ](#13-仕組みをもっと知りたい人へ)

---

## 1. PyCodeDJ って何？

### ひとことで言うと

**「コードを書くこと」が「音楽を演奏すること」になるツールです。**

`for` ループを増やすと音の揺らぎが速くなります。  
関数を 3 つ書くと 3 声のポリフォニーになります。  
コメントをたくさん書くと、リバーブが深くかかって空間が広がります。  
`pattern("x . x .")` と書けば、そのリズムで音が鳴ります。

```python
from pycodedj import loop, pattern

# コードの「構造」が音を決める
@loop("bass", interval=2.0)
def bass_line(volume=0.4):
    for i in range(8):
        if i % 2 == 0:
            pass

# pattern() でリズムと音程を明示的に指定する
@loop("kick", synth="floor_kick", dur=0.25)
def kick_drum():
    pattern("x . x .")

@loop("melody", synth="acid_lead", root="A3", scale="minor", dur=0.25)
def melody_line():
    pattern("0 . 3 . 5 . 7 .")
```

このコードをファイルに保存するだけで、音が変わります。  
追加説明もシンセの設定も必要ありません。ただ書いて、保存するだけです。

### 何に使えるの？

- **ライブコーディングパフォーマンス** — コードを書きながら観客の前で音楽を演奏する
- **コードを書く感触を音で感じる** — 構造が変わるたびに音も変わる即興制作
- **プログラミング学習** — 書いたコードが即座に音でフィードバックされる

### 音はどこから出るの？

PyCodeDJ 自体は音を出しません。**SuperCollider**（無料のソフトウェア音響シンセサイザー）が音を出します。PyCodeDJ は「Python コードを分析して SuperCollider にパラメーターを送る橋渡し役」です。

```
あなたが Python コードを書いて保存する
         |
         v
   PyCodeDJ がコードを分析
   （ネストの深さ、関数の数、
     コメントの量、pattern() の内容…）
         |
         | OSC という通信で指示
         v
   SuperCollider が音を出す
         |
         v
      スピーカー
```

SuperCollider の操作は最初の一度だけです。難しいことは何もありません。

---

## 2. インストールする

### 必要なもの

- **Python 3.10 以上** — `python --version` または `python3 --version` で確認できます
- **SuperCollider 3.12 以上** — 次のセクションでインストール方法を説明します

### PyCodeDJ をインストールする

```bash
pip install 'pycodedj[watch]'
```

`[watch]` を付けることで、ファイルの保存を検知して自動で再評価する `watch` コマンドが使えるようになります。これがあると演奏がずっとスムーズになるので、最初から付けてインストールするのをおすすめします。

インストールできたか確認します。

```bash
pycodedj --help
```

次のように表示されれば成功です。

```
usage: pycodedj [-h] [--version] {eval,watch,panic,stop,mute,unmute,solo,unsolo,status} ...
```

### 開発版をインストールする

ソースから使いたい場合は次のようにします。

```bash
git clone https://github.com/kanekoyuichi/pycodedj
cd pycodedj
pip install -e ".[dev]"
```

---

## 3. SuperCollider をセットアップする

SuperCollider は「音を出す担当」です。最初に一度だけ設定すれば、あとは自動で動きます。

### SuperCollider をインストールする

SuperCollider の公式サイト（[supercollider.github.io](https://supercollider.github.io)）からインストーラーをダウンロードします。

- **macOS:** `.dmg` ファイルをダウンロードしてインストール
- **Linux:** パッケージマネージャーか公式サイトから（Ubuntu なら `sudo apt install supercollider`）
- **Windows:** `.exe` インストーラーをダウンロード

インストール後に **SuperCollider IDE**（アプリ）を起動してください。画面が開けばインストール成功です。

### SuperCollider IDE の見方

SuperCollider IDE には大きく 2 つの場所があります。

- **コードを書く場所（上側）:** `s.boot;` のようなコードを入力して実行する
- **Post window（右側や下側）:** 実行結果やログが流れる場所

「SuperCollider で実行する」と書いてあるコードは、ターミナルではなく SuperCollider IDE のコードを書く場所で実行します。

### ステップ 1: サーバーを起動する

SuperCollider IDE を開いて、コードを書く場所に次を入力し **Ctrl+Enter**（Mac は **Cmd+Enter**）で実行します。

```supercollider
s.boot;
```

画面下部のインジケーターが緑色に変わったら起動成功です。

> **ヒント:** メニューから **Server > Boot Server** を選んでも同じことができます。

### ステップ 2: シンセを読み込む

PyCodeDJ の音色と OSC 受信処理を SuperCollider に登録します。

**File > Open** で PyCodeDJ プロジェクトフォルダの `sc/synths.scd` を開きます。  
開いたら **Ctrl+A**（Mac は **Cmd+A**）で全選択し、**Ctrl+Enter**（Mac は **Cmd+Enter**）で実行します。

Post window に次が出れば準備完了です。

```
PyCodeDJ synths loaded. Ready. OSC port: 57120
```

このメッセージが出なかった場合は [うまくいかないとき](#11-うまくいかないとき) を参照してください。

> **注意:** SuperCollider を再起動したら、もう一度 `sc/synths.scd` を実行してください。

### ステップ 3: 接続を確認する

SuperCollider の準備ができたら、ターミナルに戻って次を実行します。

```bash
pycodedj eval examples/demo.py::bass
```

ターミナルに `[pycodedj] bass ...` と表示されて SuperCollider から音が出れば、接続は完璧です。

---

## 4. はじめての音を出す

### ループファイルの基本形

PyCodeDJ のコードファイルは次の形で書きます。

```python
from pycodedj import loop

@loop("名前", interval=秒数)
def 関数名(volume=音量):
    # ここに書いたコードの「構造」が音を決める
    ...
```

`@loop("名前", interval=秒数)` は**デコレータ**です。これを付けた関数がひとつの「ループ」になります。

- `"名前"` — SuperCollider に送られる名前。英数字とアンダースコア（例: `bass`, `kick_hard`）
- `interval=秒数` — ループの更新間隔（省略時は 1.0 秒）
- `volume=音量` — 音量。0.0〜1.0 の数値（省略時は 0.3）

### サンプルファイルで試してみる

`examples/demo.py` を開いてみましょう。

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
    # ここに余白を置く
    # もう少し置く
    # 静寂も音楽
    pass
```

`bass`, `melody`, `pad` の 3 つのループが定義されています。それぞれを評価してみましょう。

```bash
pycodedj eval examples/demo.py::bass
```

成功すると次のように表示されます。

```
[pycodedj] bass  cutoff=418Hz  lfo=1.08Hz  reverb=0.00  voices=1  amp=0.40
```

続けて `melody` と `pad` も評価します。

```bash
pycodedj eval examples/demo.py::melody
pycodedj eval examples/demo.py::pad
```

3 つのループが同時に鳴っています。それぞれが独立して動いています。

### コードを変えて音を変える

`examples/demo.py` をエディタで開いて、`bass` ブロックを変えてみましょう。

**変更前:**
```python
@loop("bass", interval=2.0)
def bass(volume=0.4):
    for i in range(8):
        if i % 2 == 0:
            pass
```

**変更後（ネストを深くする）:**
```python
@loop("bass", interval=2.0)
def bass(volume=0.4):
    for i in range(8):
        for j in range(4):      # 追加
            if i % 2 == 0:
                if j > 2:       # 追加
                    pass
```

保存したら再度評価します。

```bash
pycodedj eval examples/demo.py::bass
```

```
[pycodedj] bass  cutoff=1200Hz  lfo=2.16Hz  reverb=0.00  voices=1  amp=0.40
```

cutoff が上がって音が明るくなり、lfo も速くなりました。ネストが深くなるほどフィルターが開きます。

### 音量を変える

`volume=` の値を変えるだけです。

```python
@loop("bass", interval=2.0)
def bass(volume=0.7):   # 大きくする
    ...
```

---

## 5. watch モード — 保存するだけで音が変わる

毎回 `pycodedj eval` を打つのは手間です。`watch` コマンドを使うと、起動時に全ループをまとめて評価し、その後は**ファイルを保存するだけで自動的に全ループが再評価**されます。

### 起動する

```bash
pycodedj watch examples/demo.py
```

```
[pycodedj] watching demo.py — save to reload (Ctrl+C to stop)
[pycodedj] reloaded demo.py (3 loop(s))
```

起動直後に一度すべてのループが評価されて音が鳴ります。あとはエディタでコードを書いて保存するだけです。

```
[pycodedj] reloaded demo.py (3 loop(s))
```

**コードを書く → 保存する → 音が変わる**、このサイクルがライブコーディングの本来の姿です。

### 止める

**Ctrl+C** を押すと監視が止まります。SuperCollider の音はそのまま鳴り続けます（止めたいときは `pycodedj panic`）。

### 構文エラーが出たときは

コードに構文エラーがある状態で保存しても、**そのループだけ変化せず、他のループは鳴り続けます**。エラーはターミナルに表示されます。

```
[pycodedj] syntax error (bass): invalid syntax (demo.py, line 7)
```

構文を直して保存すれば自動的に回復します。

---

## 6. コードの構造が音を変える

PyCodeDJ は Python コードの「構造」を 5 つの音楽パラメーターに変換します。コードの中身（計算の結果や変数の値）ではなく、**形** を見ています。

### 対応表

| コードのどこを見るか | 変わる音のパラメーター | 変化のイメージ |
| :--- | :--- | :--- |
| ブロックのネストの深さ（`if` や `for` の入れ子） | フィルターの明るさ（Cutoff 200〜4000 Hz） | 深くなるほど音が明るく開く |
| 制御フローの数（`if` / `for` / `while` の合計） | 音の揺らぎの速さ（LFO レート 0.1〜5.0 Hz） | 多いほど揺らぎが速くなる |
| 関数の数（`def` の数） | 音の重なり（ポリフォニー声部数 1〜4） | 多いほど音が重なる |
| コメントの割合（コメント行 ÷ 全行数） | 空間の広さ（リバーブ 0.0〜0.8） | 多いほど残響が増える |
| `volume=` 引数のデフォルト値 | 音量（0.0〜1.0） | そのまま反映される |
| `eq=` / `low=` / `mid=` / `high=` 引数 | 3 バンド EQ | ループごとの音質補正 |

> **ポイント:** `x = 1 + 2 * (3 + 4)` のような式はカウントされません。`if` / `for` などのブロック構造だけを見ています。

### 実例

#### フィルターの明るさ（ネストの深さ）

```python
# ネスト深さ 0 → フィルター最小（こもった音）
@loop("dark", interval=1.0)
def f(volume=0.3):
    pass
```

```python
# ネスト深さ 4 → フィルター全開（明るい音）
@loop("bright", interval=1.0)
def f(volume=0.3):
    for i in range(4):
        for j in range(4):
            if i == j:
                pass
```

#### 揺らぎの速さ（制御フローの数）

```python
# 制御フロー 0 個 → 揺らぎ最小（静かな音）
@loop("still", interval=1.0)
def f(volume=0.3):
    pass
```

```python
# 制御フロー 3 個 → 揺らぎ速い
@loop("busy", interval=1.0)
def f(volume=0.3):
    for i in range(4):    # 1 つ目
        if i > 2:          # 2 つ目
            while False:   # 3 つ目
                pass
```

#### 音の重なり（関数の数）

```python
# def 1 個 → 1 声（ソロ）
@loop("solo", interval=1.0)
def f(volume=0.3):
    pass
```

```python
# def 4 個 → 4 声（最大ポリフォニー）
@loop("choir", interval=1.0)
def f(volume=0.3):
    def voice_a(): pass
    def voice_b(): pass
    def voice_c(): pass
    def voice_d(): pass
```

#### 空間の広さ（コメント率）

```python
# コメントなし → ドライな音
@loop("dry", interval=1.0)
def f(volume=0.3):
    x = 1
    return x
```

```python
# コメントが多い → 深い残響
@loop("spacious", interval=1.0)
def f(volume=0.3):
    # 余白
    # もっと余白
    # 静寂も音楽
    pass
```

#### 簡易 EQ

`eq=` でジャンル寄りの EQ プリセットを選べます。`low=`, `mid=`, `high=` で個別に調整も可能です。

```python
@loop("bass_reese", interval=0.5)
def bass(volume=0.45, eq="edm"):
    ...

@loop("hat_engine", interval=0.25)
def hats(volume=0.08, eq="edm", low=0.5, high=1.25):
    ...
```

| `eq=` | 傾向 |
| :--- | :--- |
| `"flat"` | 補正なし（デフォルト） |
| `"rock"` / `"pop"` | 低音と高音を少し上げ、中域を少し下げる |
| `"edm"` / `"hiphop"` | 低音を強め、高音も少し上げる |
| `"classic"` / `"jazz"` | フラット志向 |
| `"acoustic"` | 低音を控えめにして中高域を少し上げる |

---

## 7. pattern() で音程とリズムを指定する

前章の「コード構造が音を変える」とは別に、**明示的にリズムと音程を指定する**方法があります。それが `pattern()` です。

### pattern() の基本

```python
from pycodedj import loop, pattern

@loop("kick", synth="floor_kick", dur=0.25)
def kick_drum():
    pattern("x . x .")
```

`pattern()` に渡す文字列に、鳴らすタイミングを書きます。

| トークン | 意味 |
| :--- | :--- |
| `x` | ここで音を鳴らす（トリガー） |
| `.` | 休符（無音） |
| `0`, `1`, `2` … | 音を鳴らす + 音程（スケール度数） |
| `[0 3]` | コード（複数の度数を同時に鳴らす） |
| `~` | タイ（直前の音を次のステップまで伸ばす） |

スペースで区切ると 1 ステップになります。`"x . x ."` なら 4 ステップのパターンです。

### @loop のパラメーター（pattern 用）

`pattern()` を使うループでは、`@loop` デコレータに次の引数を追加します。

**音色は `synth=` で指定します。** `@loop("bass", synth="floor_kick")` と書くと、ループ名は `bass` のまま、鳴る音色だけが `floor_kick` になります。

| 引数 | 説明 | 例 |
| :--- | :--- | :--- |
| `synth=` | 使うシンセ名 | `synth="floor_kick"` |
| `root=` | ルートノート | `root="A3"`, `root="C4"` |
| `scale=` | スケール名 | `scale="minor"`, `scale="major"` |
| `dur=` | 1 ステップの長さ（秒） | `dur=0.25`（16 分音符相当） |

> **ポイント:** `volume=` / `eq=` / `interval=` は pattern ループでも引き続き使えます。
> `@loop("kick", synth="floor_kick")` の `"kick"` はループ名、`"floor_kick"` は音色名です。`pycodedj eval demo.py::kick` や `pycodedj mute kick` ではループ名を使います。

### トリガーパターン — x と . だけで

音程なしで「リズムだけ」を指定したいときは `x` と `.` だけ使います。

```python
from pycodedj import loop, pattern

@loop("kick", synth="floor_kick", dur=0.25)
def kick():
    pattern("x . x .")      # 4 ステップ: 鳴る・休・鳴る・休

@loop("hat", synth="hat_engine", dur=0.25)
def hat():
    pattern("x x x x x x x x")  # 8 ステップ: 全部鳴る（16 分グリッド）

@loop("snare", synth="clap_snare", dur=0.25)
def snare():
    pattern(". . x . . . x .")   # 2・4 拍に鳴る
```

### 音程パターン — 数字でスケール度数を指定

音程を指定したいときは整数（0 以上）を使います。数字はスケールの**度数**（0 から数えるインデックス）です。

```python
@loop("melody", synth="acid_lead", root="A3", scale="minor", dur=0.25)
def melody():
    pattern("0 . 3 . 5 . 7 .")
```

`scale="minor"` で `root="A3"` のとき、度数と音程の対応はこうなります。

| 度数 | A ナチュラルマイナー |
| :--- | :--- |
| 0 | A3 |
| 1 | B3 |
| 2 | C4 |
| 3 | D4 |
| 4 | E4 |
| 5 | F4 |
| 6 | G4 |
| 7 | A4（1 オクターブ上） |

> **ヒント:** 度数が 7 以上になると自動的にオクターブが上がります。`7` は `0` の 1 オクターブ上、`14` は 2 オクターブ上です。

### 利用可能なスケール

SuperCollider の Scale ライブラリが使えます。主なものを挙げます。

| `scale=` に渡す名前 | スケール |
| :--- | :--- |
| `"major"` | メジャー（長調） |
| `"minor"` | ナチュラルマイナー（短調） |
| `"chromatic"` | クロマチック（半音階） |
| `"dorian"` | ドリアン |
| `"phrygian"` | フリジアン |
| `"lydian"` | リディアン |
| `"mixolydian"` | ミクソリディアン |
| `"pentatonicMajor"` | メジャーペンタトニック |
| `"pentatonicMinor"` | マイナーペンタトニック |

### x と数字を混ぜる

トリガー（`x`）と度数を混ぜても使えます。`x` は「ルートノートで鳴らす」という意味になります。

```python
@loop("bass", synth="acid_lead", root="C3", scale="minor", dur=0.25)
def bass():
    pattern("0 . x . 3 . x .")
    # 0→C3, 休, x→C3, 休, 3→Eb3, 休, x→C3, 休
```

### コード — 複数の音を同時に鳴らす

`[0 3]` のように角括弧で複数の度数を囲むと、1 ステップで複数の音を同時に鳴らせます。

```python
@loop("chord", synth="note", root="C3", scale="minor", dur=0.5)
def chord():
    pattern("[0 2 4] . [0 3] .")
    # [0 2 4]→C3+Eb3+G3（短三和音）, 休, [0 3]→C3+Eb3, 休
```

コード内に書けるのは **0 以上の整数のみ** です。`.`・`x`・`~` は書けません。

### タイ — 音を伸ばす

`~` を使うと、直前の音（または コード）を次のステップまで伸ばせます。

```python
@loop("bass", synth="note", root="A1", scale="minor", dur=0.25)
def bass():
    pattern("0 . [0 3] ~ 5 . 3 .")
    # 0→A1, 休, [0 3]→和音（2ステップ分 持続）, 5→F2, 休, 3→D2, 休
```

`~` は単音・コードの直後にのみ書けます。先頭・`.` や `x` の直後は書けません。

### ルートノートの書き方

`root=` にはノート名 + オクターブ番号を渡します。

| 書き方 | 音 |
| :--- | :--- |
| `"C4"` | 中央 C（ミドル C） |
| `"A3"` | A3 |
| `"Bb2"` | B♭2 |
| `"F#3"` | F♯3（`s` を使って `"Fs3"` とも書ける） |
| `"C1"` | 低い C |

### 実例: キックとベースとコード

```python
from pycodedj import loop, pattern

@loop("kick", synth="floor_kick", dur=0.25)
def kick():
    pattern("x . . . x . . .")

@loop("bass", synth="bass_acid", root="A1", scale="minor", dur=0.25)
def bass():
    pattern("0 . [0 3] ~ 5 . 3 .")
    # 0→A1, 休, [0 3]→2音コード（2ステップ持続）, 5→F2, 休, 3→D2, 休

@loop("melody", synth="acid_lead", root="A3", scale="minor", dur=0.5)
def melody():
    pattern("0 3 5 7")

@loop("pad", interval=4.0)
def pad(volume=0.06):
    # 背景の空気感
    # コード構造で鳴らす
    pass
```

### pattern() と構造マッピングの違い

| | コード構造マッピング（従来） | pattern() |
| :--- | :--- | :--- |
| リズム | SuperCollider 側で生成（コードの構造から） | 自分で指定 |
| 音程 | SuperCollider 側で生成 | 自分で指定（または任せる） |
| 使い方 | 構造の変化を楽しむ | リズム・音程を明示したいとき |

どちらを使っても構いません。同じファイルの中で混在させることもできます。

---

## 8. 複数のループを同時に動かす

PyCodeDJ の最大の特徴は、**複数のループが独立して動き続ける**ことです。1 つのループを変更しても、他のループは止まりません。

### 基本の使い方

```python
from pycodedj import loop, pattern

@loop("kick", synth="floor_kick", dur=0.25)
def kick():
    pattern("x . x .")

@loop("bass", interval=2.0)
def bass_line(volume=0.4):
    for i in range(8):
        if i % 2 == 0:
            pass

@loop("pad", interval=4.0)
def atmosphere(volume=0.08):
    # 背景の空気
    # 余白
    pass
```

watch で起動すれば、保存するたびに変更したループだけが更新されます。

```bash
pycodedj watch myfile.py
```

### 重低音クラブセットを試す

`examples/club_set.py` は、クラブのフロアで鳴る低域を意識したサンプルです。4つ打ちキック、2・4拍のクラップ、オフビートハット、16分ハット、ランブル、サブベース、アシッドベース、スタブ、フィル、空間ノイズを重ねています。

```bash
pycodedj watch examples/club_set.py
```

主なループ名は次の通りです。`mute` / `unmute` で足し引きすると、クラブトラックのレイヤー構造がわかりやすくなります。

| ループ名 | 役割 | 音色名 |
| :--- | :--- | :--- |
| `kick` | 4つ打ちの土台 | `floor_kick` |
| `rumble` | 床鳴りする低域 | `bass_rumble` |
| `sub` / `floor` | 持続する重低音 | `sub_bass` |
| `acid` | 動くベースライン | `bass_acid` |
| `offhat` / `hats` | グルーヴの推進力 | `hat_ride`, `hat_engine` |
| `room` | 倉庫のような空間感 | `warehouse_air` |

### 演奏中のコントロール

**停止 / ミュート / アンミュート**

```bash
pycodedj stop bass        # bass を停止する
pycodedj mute bass        # bass を消音（停止はしない）
pycodedj unmute bass      # bass の音量を元に戻す
```

**緊急停止**

```bash
pycodedj panic            # すべてのループを即時停止
```

**ループの状態を確認**

```bash
pycodedj status
```

```
Loop         State    Amp    Cutoff
kick         playing  0.30   —
bass         playing  0.40   1340Hz
pad          muted    0.08   200Hz
```

### ループを削除するには

ファイルからそのブロック（`@loop` デコレータごと関数）を削除して保存します。watch モードなら保存時に自動的に停止します。

---

## 9. 音色リファレンス

PyCodeDJ では **ループ名** と **音色名** を分けて考えます。

- ループ名: `@loop("kick", ...)` の第一引数。`pycodedj eval demo.py::kick`、`mute`、`solo` などで指定する名前
- 音色名: SuperCollider 側のシンセ名。pattern ループでは `synth="floor_kick"` のように指定する名前

音色を選ぶときは、下の表から音色名を選んで `synth=` に入れます。たとえば `@loop("bass", synth="floor_kick")` は、`bass` というループ名で `floor_kick` の音色を鳴らします。

`pattern()` を使う場合は、`@loop("kick", synth="floor_kick")` のように、短いループ名と具体的な音色名を分けて書けます。

`pattern()` を使わない構造マッピングのループでは、互換性のためにループ名と同じ名前の音色があればそれが使われます。たとえば `@loop("bass_acid", interval=0.5)` は `bass_acid` 音色で鳴ります。

全 30 音色を 1 音ずつ確認したい場合は `examples/sound_showcase.py` を使います。

```bash
pycodedj eval examples/sound_showcase.py::floor_kick
pycodedj eval examples/sound_showcase.py::bass_acid
pycodedj eval examples/sound_showcase.py::acid_lead
```

`examples/sound_showcase.py` では試聴しやすいように、ループ名を音色名と同じにしています。通常の pattern ループでは、次のように `synth=` にこの表の音色名を指定します。

```python
@loop("kick", synth="floor_kick", dur=0.25)
def kick():
    pattern("x . x .")
```

### キック

| 音色名 | 音の特徴 |
| :--- | :--- |
| `kick_hard` | 硬めでアタックの強いキック |
| `floor_kick` | 太い四つ打ちキック |
| `kick_pulse` | 軽めのパルスキック |

### ベース

| 音色名 | 音の特徴 |
| :--- | :--- |
| `bass_rumble` | 深い低音ランブル |
| `bass_reese` | 揺れる Reese 系ベース |
| `sub_bass` | サブベース |
| `bass_acid` | 303 スタイルのアシッドベース |

### パーカッション

| 音色名 | 音の特徴 |
| :--- | :--- |
| `hat_engine` | クローズ/オープンのハットグリッド |
| `hat_ride` | 長めのライド/オープンハット |
| `clap_snap` | 鋭いクラップ |
| `clap_snare` | スネア寄りのクラップ |
| `tom_drum` | フロアタム（ピッチスイープ付き） |
| `snare_roll` | スネアロール |
| `noise_crash` | クラッシュシンバル（長いテール） |

### コード・スタブ

| 音色名 | 音の特徴 |
| :--- | :--- |
| `chord_rave` | 明るいレイブスタブ |
| `neon_stab` | ネオン系スタブコード |
| `dub_chord` | ダブコード |
| `stab_saw` | デチューンソーコードスタブ |
| `organ_chord` | ハモンドオルガン風コード |
| `bell_rave` | FM ベル（レイブ系） |

### リード・メロディー

| 音色名 | 音の特徴 |
| :--- | :--- |
| `acid_lead` | アシッド系リード |
| `lead_hoover` | Hoover 風リード |
| `soft_pluck` | やわらかいプラック |
| `synth_arp` | アルペジオシンセ |
| `note` | 汎用ノートシンセ（音程パターン向け） |

### アトモスフィア

| 音色名 | 音の特徴 |
| :--- | :--- |
| `shimmer_pad` | 深いシマーパッド |
| `warehouse_air` | 倉庫っぽい空気感 |
| `vox_ahh` | フォルマントボーカルパッド |

### FX

| 音色名 | 音の特徴 |
| :--- | :--- |
| `fx_impact` | 低いインパクト |
| `riser_noise` | ノイズライザー（8 秒でスイープ上昇） |
| `glitch_ticks` | 細かいグリッチ音 |

---

## 10. 演奏のアイデア

### アイデア A: シンプルから育てていく

watch を起動した状態で、空のコードから少しずつ要素を足していきます。保存するたびに音が変わる様子を体験できます。

```python
# 段階 1: 最小（フィルター最小、ポリフォニー 1）
@loop("main", interval=1.0)
def f(volume=0.3):
    pass
```

```python
# 段階 2: 揺らぎを追加
@loop("main", interval=1.0)
def f(volume=0.3):
    for i in range(4):
        pass
```

```python
# 段階 3: ネストを深くしてフィルターを開く
@loop("main", interval=1.0)
def f(volume=0.3):
    for i in range(4):
        for j in range(2):
            if i > j:
                pass
```

```python
# 段階 4: 声部を増やしてクライマックス
@loop("main", interval=1.0)
def f(volume=0.5):
    def voice_a():
        for i in range(4):
            for j in range(2):
                if i > j:
                    pass
    def voice_b():
        for k in range(8):
            pass
```

### アイデア B: pattern() でライブシーケンス

pattern() を使って、保存するたびにリズムや音程を変えていきます。

```python
from pycodedj import loop, pattern

@loop("kick", synth="floor_kick", dur=0.25)
def kick():
    pattern("x . x .")   # ← ここを変えて保存するたびにリズムが変わる

@loop("bass", synth="bass_acid", root="A1", scale="minor", dur=0.25)
def bass():
    pattern("0 . 0 . 3 .")   # ← 度数を変えて和声を変える
```

### アイデア C: コントラストをつける

にぎやかなパートと静かなパートを対比させます。

```python
@loop("bass", interval=2.0)
def the_bass(volume=0.5):
    def layer_a():
        for i in range(8):
            for j in range(4):
                if i == j:
                    pass
    def layer_b():
        for k in range(8):
            pass

@loop("pad", interval=4.0)
def space(volume=0.08):
    # 静寂
    # もっと静寂
    # ただの余白
    pass
```

### アイデア D: コメントだけで演奏する

関数は 1 つだけ残して、コメントの量だけで演奏します。コメントが増えるほど残響が深くなります。

```python
@loop("ambient", interval=4.0)
def f(volume=0.15):
    # ここからコメントを増やしたり減らしたりするだけ
    pass
```

### アイデア E: 関数名でストーリーを書く

音は関数の中身の構造で決まります。関数名は何でも構いません。

```python
@loop("scene", interval=2.0)
def the_city_wakes_up(volume=0.3):
    for hour in range(6):
        if hour > 4:
            pass

@loop("rush", interval=1.0)
def rush_hour(volume=0.2):
    for commuter in range(8):
        for train in range(3):
            if commuter % 2 == 0:
                pass
```

---

## 11. うまくいかないとき

### 音が鳴らない

まず SuperCollider 単体で音が出るか確認します。SuperCollider IDE のコードを書く場所で次を実行します。

```supercollider
{ SinOsc.ar(440, 0, 0.1) ! 2 }.play;
```

**Ctrl+Enter**（Mac は **Cmd+Enter**）で実行、**Ctrl+.**（Mac は **Cmd+.**）で停止です。

ここで音が出なければ PyCodeDJ の問題ではありません。SuperCollider サーバーの状態、OS の音量設定、出力デバイスを確認してください。

音が出た場合は次を確認します。

**1. サーバーが起動しているか**

```supercollider
s.boot;
```

**2. `sc/synths.scd` が読み込まれているか**

`sc/synths.scd` を全選択して実行（Ctrl+A → Ctrl+Enter）し、Post window に次が出るか確認します。

```
PyCodeDJ synths loaded. Ready. OSC port: 57120
```

**3. ポート番号が合っているか**

SuperCollider で次を実行して確認します。

```supercollider
NetAddr.langPort.postln;
```

`57120` 以外が表示されたら、Python 側でポートを指定します。

```bash
pycodedj eval examples/demo.py::bass --sc-port 表示された番号
```

**4. OSC の受信確認**

SuperCollider で OSC トレースを有効にします。

```supercollider
OSCFunc.trace(true);
```

この状態で `pycodedj eval` を実行し、SuperCollider の Post window に OSC メッセージが流れるか確認します。確認が終わったらトレースを止めます。

```supercollider
OSCFunc.trace(false);
```

### `[pycodedj] OSC error` というエラーが出る

SuperCollider が起動していないか、ポート番号が違います。

1. SuperCollider IDE が開いていてサーバーが起動しているか確認する
2. `sc/synths.scd` を実行して `Ready.` メッセージを確認する
3. ポート番号が違う場合は `--sc-port` で指定する

```bash
pycodedj eval demo.py::bass --sc-port 57200
```

### `loop 'xxx' not found` というエラーが出る

`::` の後ろのループ名が `@loop(...)` の第一引数と一致していません。

```bash
# ファイルの中に @loop("bass", ...) と書いてあれば
pycodedj eval demo.py::bass   # OK
pycodedj eval demo.py::Bass   # NG（大文字小文字が違う）
```

### `file not found` というエラーが出る

ファイルのパスが正しくありません。現在のディレクトリを確認するか、フルパスで指定します。

```bash
pwd    # 現在のディレクトリを確認
ls     # ファイル一覧を確認
```

### `pycodedj watch` が watchdog のインストールを求める

```bash
pip install 'pycodedj[watch]'
```

最初のインストールで `[watch]` を付け忘れた場合はこれで追加できます。

### 出力先を変えたら音が出なくなった

SuperCollider は audio server を起動した時点の出力先を使います。出力先を変更したら次の手順を踏みます。

```supercollider
// 利用可能なデバイスを確認
ServerOptions.devices;

// 出力先を指定して再起動
s.quit;
s.options.outDevice = "ここに出力デバイス名";
s.options.numInputBusChannels = 0;
s.boot;
```

boot 後、`sc/synths.scd` をもう一度実行してください。

---

## 12. コマンドと設定の全リスト

### `pycodedj eval`

指定したループを一度だけ評価して SuperCollider にパラメーターを送ります。

```
pycodedj eval FILE::LOOP [--sc-host HOST] [--sc-port PORT]
```

| 引数・オプション | 説明 | デフォルト |
| :--- | :--- | :--- |
| `FILE::LOOP` | ファイルパスとループ名を `::` で区切る | — |
| `--sc-host` | SuperCollider のホスト | `127.0.0.1` |
| `--sc-port` | SuperCollider の受信ポート番号 | `57120` |

成功すると stdout にフィードバックが出ます。

```
[pycodedj] bass  cutoff=418Hz  lfo=1.08Hz  reverb=0.00  voices=1  amp=0.40
```

失敗した場合は stderr にエラーが出て終了コード 1 で終了します。

```bash
pycodedj eval examples/demo.py::bass
pycodedj eval demo.py::melody --sc-host 192.168.1.10
pycodedj eval demo.py::pad --sc-port 57200
```

### `pycodedj watch`

ファイルを監視し、起動時と保存のたびに全ループを自動で再評価します。Ctrl+C で停止します。

```
pycodedj watch FILE [--sc-host HOST] [--sc-port PORT] [--debounce SECS]
```

| 引数・オプション | 説明 | デフォルト |
| :--- | :--- | :--- |
| `FILE` | 監視するファイル | — |
| `--sc-host` | SuperCollider のホスト | `127.0.0.1` |
| `--sc-port` | SuperCollider の受信ポート番号 | `57120` |
| `--debounce` | 連続保存をまとめる待機時間（秒） | `0.3` |

```bash
pycodedj watch examples/demo.py
pycodedj watch examples/club_set.py --debounce 0.5
```

### `pycodedj panic`

全アクティブループに即時停止信号を送ります。演奏中に問題が起きたとき、すべての音をすぐ止めたい場合に使います。

```
pycodedj panic [--sc-host HOST] [--sc-port PORT]
```

```bash
pycodedj panic
```

### `pycodedj stop`

指定した 1 つのループを停止します。`mute` と違い、音量を 0 にするだけではなく、通常ループのシンセと `pattern()` ループの Pdef の両方を止めます。

```
pycodedj stop NAME [--sc-host HOST] [--sc-port PORT]
```

```bash
pycodedj stop kick_hard
```

### `pycodedj mute`

ループを消音します（停止はしません）。unmute で音量が復元します。

```
pycodedj mute NAME [--sc-host HOST] [--sc-port PORT]
```

```bash
pycodedj mute bass
```

### `pycodedj unmute`

ミュートしたループの音量を元に戻します。

```
pycodedj unmute NAME [--sc-host HOST] [--sc-port PORT]
```

```bash
pycodedj unmute bass
```

### `pycodedj status`

アクティブなループの状態を表示します。

```
pycodedj status [--sc-host HOST] [--sc-port PORT]
```

```
Loop         State    Amp    Cutoff
bass         playing  0.40   1340Hz
pad          muted    0.15   200Hz
```

> **注意:** `status` は watch プロセスとは別プロセスで動作するため、watch セッション外で実行すると「no active loops」と表示されます。

### ループの書き方（まとめ）

```python
from pycodedj import loop, pattern

# コード構造マッピング
@loop("名前", interval=秒数)
def 関数名(volume=音量, eq="プリセット"):
    # 中身の構造が音楽パラメーターになる
    ...

# pattern() を使う
@loop("名前", synth="音色名", root="ノート", scale="スケール", dur=秒数)
def 関数名(volume=音量):
    pattern("x . x . 0 . 3 .")
```

| 引数 | 説明 | デフォルト |
| :--- | :--- | :--- |
| `"名前"` | ループ名（英数字とアンダースコア） | — |
| `interval=` | 更新間隔（秒） | `1.0` |
| `volume=` | 音量（0.0〜1.0） | `0.3` |
| `eq=` | EQ プリセット | `"flat"` |
| `low=`, `mid=`, `high=` | EQ 個別調整（0.0〜2.0） | プリセット値 |
| `synth=` | pattern 用のシンセ名 | — |
| `root=` | pattern 用のルートノート | `"C4"` |
| `scale=` | pattern 用のスケール名 | `"chromatic"` |
| `dur=` | pattern の 1 ステップの長さ（秒） | `0.25` |

---

## 13. 仕組みをもっと知りたい人へ

### マッピングの数値

| パラメーター | 入力 | 出力範囲 | スケール |
| :--- | :--- | :--- | :--- |
| Cutoff | ブロック深さ 0–10 | 200–4000 Hz | リニア |
| LFO レート | 制御フロー数 0–10 | 0.1–5.0 Hz | リニア |
| リバーブ | コメント率 0.0–1.0 | 0.0–0.8 | リニア |
| 声部数 | 関数数（クランプ） | 1–4 | クランプ |
| 音量 | `volume=` 引数 | そのまま | パススルー |

### OSC アドレス

SuperCollider と通信するアドレスです。Hydra などのビジュアルツールを繋ぐときに参照してください。

| アドレス | 型 | 値 |
| :--- | :--- | :--- |
| `/pycodedj/loop/<name>/params` | int, float, float, float, float | `voice_count`, `cutoff`, `lfo_rate`, `reverb`, `amp` の順 |
| `/pycodedj/loop/<name>/pattern` | int, str, float, str, int… | `root_midi`, `scale`, `dur`, `synth`, `step…` |
| `/pycodedj/loop/<name>/pattern_stop` | — | パターン停止 |
| `/pycodedj/loop/<name>/synth` | str | シンセ名（空文字列でリセット） |
| `/pycodedj/loop/<name>/amp` | float | 音量（互換用） |

### Python API から直接使う

CLI を使わずにプログラムから操作することもできます。

```python
from pycodedj.block_parser import parse_blocks
from pycodedj.engine import Engine
from pycodedj.osc_bridge import OscBridge, OscEndpoint

bridge = OscBridge(audio=OscEndpoint("127.0.0.1", 57120))
engine = Engine(bridge=bridge)

source = open("demo.py").read()
blocks = {b.name: b for b in parse_blocks(source).blocks}

params = engine.eval_block(blocks["bass"])
if params is not None:
    print(f"cutoff={params.cutoff:.0f}Hz  amp={params.amp:.2f}")
```

`eval_block` は成功すると `MusicParams` を返します。構文エラーや OSC 送信失敗の場合は `None` を返します。

### モジュール構成

```
pycodedj/
├── _loop.py          # @loop デコレータ（実行時は no-op）
├── block_parser.py   # @loop デコレータを AST で解析してブロックを分割する
├── analyzer.py       # コードの特徴量（深さ・数・比率）を抽出する
├── mapper.py         # 特徴量を音楽パラメーターに変換する
├── pattern.py        # pattern() 文字列を解析する
├── engine.py         # ブロック評価のパイプライン全体を管理する
├── osc_bridge.py     # SuperCollider へ OSC で送信する
├── watcher.py        # ファイル監視（watchdog ベース）
└── __main__.py       # CLI コマンドのエントリポイント
```
