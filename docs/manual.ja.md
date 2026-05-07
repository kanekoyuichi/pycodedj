# PyCodeDJ マニュアル

[English manual](https://github.com/kanekoyuichi/pycodedj/blob/main/docs/manual.md)

> Python コードを書くと、リアルタイムに音が変わる

---

## このマニュアルを読む前に

プログラムを書いたことがある人なら、誰でも試せます。音楽の知識は不要です。SuperCollider も「はじめて聞いた」で大丈夫です。

このマニュアルを順番に進めると、最終的に **自分が書いた Python コードから音が出る体験** ができます。所要時間の目安: セットアップ込みで 20〜30 分。

---

## 目次

1. [PyCodeDJ って何？](#1-pycodedj-って何)
2. [準備する](#2-準備する)
3. [SuperCollider をセットアップする](#3-supercollider-をセットアップする)
4. [はじめての音を出す](#4-はじめての音を出す)
5. [保存するだけで音が変わる — watch モード](#5-保存するだけで音が変わる--watch-モード)
6. [コードと音の関係を知る](#6-コードと音の関係を知る)
7. [複数のループを同時に動かす](#7-複数のループを同時に動かす)
8. [クラブセット例 — club_set.py を動かす](#8-クラブセット例--club_setpy-を動かす)
9. [演奏のアイデア](#9-演奏のアイデア)
10. [うまくいかないとき](#10-うまくいかないとき)
11. [コマンドと設定の全リスト](#11-コマンドと設定の全リスト)
12. [仕組みをもっと知りたい人へ](#12-仕組みをもっと知りたい人へ)

---

## 1. PyCodeDJ って何？

### ひとことで言うと

**Python のコードを書くと、リアルタイムに音が変わる楽器です。**

`for` ループを増やすと音の揺らぎが速くなります。関数を 3 つ書くと 3 声のポリフォニーになります。コメントをたくさん書くと、リバーブが深くかかって空間が広がります。

```python
# @loop main interval=1.0

# コメントを増やすほど空間が広がる
# もう一行
# さらにもう一行

def melody():
    for i in range(4):   # for を増やすと揺らぎが速くなる
        if i > 2:        # if を増やすとさらに速くなる
            pass
```

このコードを評価すると、ターミナルに次のように表示されます。

```
[pycodedj] main  cutoff=560Hz  lfo=1.08Hz  reverb=0.43  voices=1
```

SuperCollider がすぐにその音色に切り替わります。他のループは止まりません。

### 何に使えるの？

- ライブコーディングパフォーマンス（コードを書きながら音楽を演奏する）
- コードを書く「感触」を音で感じながら開発する
- プログラミングの学習に音のフィードバックを加える

### 音はどこから出るの？

PyCodeDJ 自体は音を出しません。**SuperCollider**（無料のソフトウェア音響シンセサイザー）が音を出します。PyCodeDJ は「Python コードを分析して、SuperCollider にパラメーターを伝える橋渡し役」です。

```
あなたが書く Python コード
        |
        | pycodedj eval / watch を実行
        v
  PyCodeDJ がコードを分析
  （どれだけネストしているか、
    関数がいくつあるか、など）
        |
        | OSC という通信プロトコルで指示
        v
  SuperCollider が音を出す
        |
        v
     スピーカー
```

SuperCollider の操作は最小限で済みます。難しいことはしなくて大丈夫です。

---

## 2. 準備する

### 必要なもの

- Python 3.10 以上（`python --version` で確認できます）
- SuperCollider 3.12 以上（次のセクションでインストール方法を説明します）
- ターミナル（コマンドを打てる環境）

### PyCodeDJ をインストールする

```bash
pip install 'pycodedj[watch]'
```

`[watch]` を付けることで、ファイル保存を検知する `watch` コマンドも使えるようになります。これがあると演奏がずっとスムーズになるので、最初からインストールするのをおすすめします。

インストールできたか確認します。

```bash
pycodedj --help
```

次のように表示されれば成功です。

```
usage: pycodedj [-h] {eval,watch} ...
```

### SuperCollider をインストールする

SuperCollider の公式サイト（supercollider.github.io）からインストーラーをダウンロードします。

- macOS: `.dmg` ファイルをダウンロードしてインストール
- Linux: パッケージマネージャーか公式サイトから
- Windows: `.exe` インストーラーをダウンロード

インストール後に SuperCollider IDE（アプリ）を起動してください。画面が開けばインストール成功です。

---

## 3. SuperCollider をセットアップする

SuperCollider は「音を出す担当」です。最初に一度だけ設定すれば、あとは自動的に動きます。

### ステップ 1: サーバーを起動する

SuperCollider IDE を開き、メニューから **Server > Boot Server** を選びます。

または、コード入力欄に次を書いて **Ctrl+Enter**（Mac は Cmd+Enter）で実行します。

```supercollider
s.boot;
```

画面下部に `localhost` が緑色に変わったら起動成功です。

### ステップ 2: シンセを読み込む

PyCodeDJ のプロジェクトフォルダにある `sc/synths.scd` を SuperCollider IDE で開きます。

**File > Open** で `sc/synths.scd` を開いたら、**Ctrl+A**（Mac は Cmd+A）で全選択し、**Ctrl+Enter**（Mac は Cmd+Enter）で実行します。

右側の Post window に次のメッセージが出れば準備完了です。

```
PyCodeDJ synths loaded. Ready. OSC port: 57120
```

このメッセージが出ない場合は [うまくいかないとき](#10-うまくいかないとき) を参照してください。

### ステップ 3: 接続を確認する

ターミナルに戻り、次を実行します。

```bash
python examples/hello_sc.py
```

ターミナルに `Sent OSC to 127.0.0.1:57120 — loop 'hello'` と表示され、SuperCollider から音が出れば接続成功です。

SuperCollider はこのまま起動したままにしておいてください。

---

## 4. はじめての音を出す

### ステップ 1: デモファイルを確認する

`examples/demo.py` を開いてみましょう。

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
# ここに余白を置く
# もう少し置く
# 静寂も音楽
def pad():
    pass
```

`# @loop bass` から `# @loop melody` の直前まで、これが「bass ブロック」です。

### ステップ 2: 音を出す

ターミナルで次を実行します。

```bash
pycodedj eval examples/demo.py::bass
```

成功すると次のように表示されます。

```
[pycodedj] bass  cutoff=418Hz  lfo=1.08Hz  reverb=0.00  voices=1
```

これがあなたの最初のライブコーディングです。このフィードバックで今どんな音色になっているかが一目でわかります。

続けて melody と pad も評価してみましょう。

```bash
pycodedj eval examples/demo.py::melody
pycodedj eval examples/demo.py::pad
```

3 つのループが同時に鳴っています。それぞれが独立して動いているのがわかるでしょうか。

### ステップ 3: コードを変えて音を変える

`examples/demo.py` をテキストエディタで開いて、bass ブロックを変えてみます。

**変更前:**

```python
# @loop bass interval=2.0
def bass():
    for i in range(8):
        if i % 2 == 0:
            pass
```

**変更後（ネストを深くする）:**

```python
# @loop bass interval=2.0
def bass():
    for i in range(8):
        for j in range(4):      # 1 行追加
            if i % 2 == 0:
                if j > 2:       # 1 行追加
                    pass
```

ファイルを保存したら、ターミナルで再度評価します。

```bash
pycodedj eval examples/demo.py::bass
```

```
[pycodedj] bass  cutoff=1200Hz  lfo=2.16Hz  reverb=0.00  voices=1
```

cutoff が上がって音が明るくなり、lfo も速くなりました。ネストが深くなるほどフィルターが開き、制御フローが増えるほど揺らぎが速くなります。

---

## 5. 保存するだけで音が変わる — watch モード

毎回 `pycodedj eval` を打つのは面倒です。`watch` コマンドを使うと、**ファイルを保存するだけで自動的に全ループが再評価されます**。

### 起動方法

```bash
pycodedj watch examples/demo.py
```

```
[pycodedj] watching demo.py — save to reload (Ctrl+C to stop)
```

あとはエディタでコードを書いて保存するだけです。保存のたびに次のように出力されます。

```
[pycodedj] reloaded demo.py (3 loop(s))
```

これがライブコーディングの本来のワークフローです。コードを書く → 保存する → 音が変わる、このサイクルを繰り返します。

### 止め方

ターミナルで **Ctrl+C** を押すと監視が止まります。SuperCollider の音はそのまま鳴り続けます。

### デバウンスについて

連続して保存したとき（vim のような一部のエディタは保存時にテンポラリファイルを経由する）でも、短時間に複数回評価されないよう自動的に間引きます。`--debounce` オプションでその待機時間を変更できます（デフォルト 0.3 秒）。

```bash
pycodedj watch demo.py --debounce 0.5
```

---

## 6. コードと音の関係を知る

PyCodeDJ は Python コードの「構造」を 4 つの音楽パラメーターに変換します。

### 対応表

| コードのどこを見るか | 変わる音のパラメーター | 変化のイメージ |
| :--- | :--- | :--- |
| ブロック構造の深さ（`if` や `for` のネスト） | フィルターの明るさ（Cutoff） | 深くなるほど音が明るく開く |
| 制御フローの数（`if` / `for` / `while` の合計） | 音の揺らぎの速さ（LFO レート） | 多いほど揺らぎが速くなる |
| 関数の数（`def` の数） | 音の重なり（ポリフォニー声部数） | 多いほど音が重なる（最大 4） |
| コメントの割合（コメント行 ÷ 全行） | 空間の広さ（リバーブの深さ） | 多いほど残響が増える |

### 実例で見る

#### フィルターの明るさ（ネストの深さ）

```python
# @loop test interval=1.0
# ネスト深さ 1 → フィルター最小（こもった音）
def f(): pass
```

```python
# @loop test interval=1.0
# ネスト深さ 4 → フィルター最大（明るい音）
def f():
    for i in range(4):
        for j in range(4):
            if i == j:
                pass
```

> `x = 1 + 2 * (3 + 4)` のような演算式はネストの深さにカウントされません。`if` や `for` などのブロック構造だけを数えます。

#### 揺らぎの速さ（制御フローの数）

```python
# @loop test interval=1.0
# 制御フロー 0 個 → 揺らぎ最小（ゆったり）
def f(): pass
```

```python
# @loop test interval=1.0
# 制御フロー 3 個 → 揺らぎ中程度
def f():
    for i in range(4):   # 1 つ目
        if i > 2:        # 2 つ目
            while False: # 3 つ目
                pass
```

#### 音の重なり（関数の数）

```python
# @loop test interval=1.0
# 関数 1 個 → 1 声（ソロ）
def solo(): pass
```

```python
# @loop test interval=1.0
# 関数 4 個 → 4 声（最大ポリフォニー）
def voice_a(): pass
def voice_b(): pass
def voice_c(): pass
def voice_d(): pass
```

#### 空間の広さ（コメント率）

```python
# @loop test interval=1.0
# コメントなし → ドライな音
def f():
    x = 1
    return x
```

```python
# @loop test interval=1.0
# コメントが多い → 深い残響
# 余白
# 余白
# 余白
def f(): pass
```

---

## 7. 複数のループを同時に動かす

PyCodeDJ の最大の特徴は、**複数のループが独立して動き続ける**ことです。

### 基本の使い方

ファイルに `# @loop 名前` を追加するだけで新しいループを作れます。

```python
# @loop bass interval=2.0
def bass():
    for i in range(8):
        pass

# @loop chord interval=1.0
def chord_a(): pass
def chord_b(): pass

# @loop texture interval=4.0
# 背景
# 空気
def bg(): pass
```

それぞれを別々に評価できます。

```bash
pycodedj eval myfile.py::bass
pycodedj eval myfile.py::chord
pycodedj eval myfile.py::texture
```

または `watch` を使えばファイルを保存するだけで全ループが一斉に更新されます。

### ループを止めるには

ループを止めたいときは、そのブロックの関数を削除して（`def` がなくなった状態にして）再評価します。

```python
# @loop bass interval=2.0
# （空にする）
```

```bash
pycodedj eval myfile.py::bass
```

---

## 8. クラブセット例 — club_set.py を動かす

`examples/club_set.py` は、クラブミュージック風のパートを 5 つ組み合わせたデモファイルです。それぞれのブロックがコードの構造で異なる音色を持っています。

### ブロック一覧

| ループ名 | キャラクター | コードの特徴 |
| :--- | :--- | :--- |
| `sub_bass` | 重いサブベース | `if` のネストが深く、フィルターが開いている |
| `hat_engine` | ハイハットのグリッド | `for` + `if` が多く、揺らぎが速い |
| `neon_stab` | 3 声のコードスタブ | 関数 3 つでポリフォニー |
| `acid_lead` | アシッドリード | 深いネストと多い制御フローで明るく速い |
| `warehouse_air` | 倉庫の空気感 | コメントだらけでリバーブが深い |

### 動かしてみる

watch で起動して、エディタで各ブロックを編集しながら音を変えていきます。

```bash
pycodedj watch examples/club_set.py
```

まず全ループを一度評価してみましょう。watch が起動した状態でファイルを保存すると全ループが評価されます。あるいは個別に eval することもできます。

```bash
pycodedj eval examples/club_set.py::sub_bass
pycodedj eval examples/club_set.py::hat_engine
pycodedj eval examples/club_set.py::neon_stab
pycodedj eval examples/club_set.py::acid_lead
pycodedj eval examples/club_set.py::warehouse_air
```

### 演奏してみる

`warehouse_air` はコメントだけのブロックです。コメントを増やしたり減らしたりすると、リバーブの深さが変わります。

```python
# @loop warehouse_air interval=4.0
# smoke above the kick
# late reflections
# concrete room tail
# crowd heat
# blue strobes
def warehouse_air():
    pass
```

コメントを 2 行だけ残して保存してみてください。空間が一気に乾いた音になります。

`neon_stab` の関数を 1 つ減らしてみましょう。3 声から 2 声になって音が薄くなります。

```python
# @loop neon_stab interval=2.0
def chord_root():
    return "minor"

def chord_fifth():
    return "pressure"

# chord_seventh を削除
```

`acid_lead` の `for slide in range(2)` のネストを削除して、フラットにしてみましょう。フィルターがグッと下がって音がこもります。

このように、コードの構造を変えることが演奏になります。

---

## 9. 演奏のアイデア

### アイデア A: シンプルから複雑へ育てる

最初は空のコードから始めて、少しずつ要素を加えていきます。watch を起動した状態で保存するたびに音が変わっていく様子を楽しめます。

```python
# 段階 1: ほぼ無音（フィルター最小、ポリフォニー 1）
# @loop main interval=1.0
def f(): pass
```

```python
# 段階 2: 揺らぎを加える
# @loop main interval=1.0
def f():
    for i in range(4):
        pass
```

```python
# 段階 3: さらに深く
# @loop main interval=1.0
def f():
    for i in range(4):
        for j in range(2):
            if i > j:
                pass
```

```python
# 段階 4: 声部を増やしてクライマックス
# @loop main interval=1.0
def voice_a():
    for i in range(4):
        for j in range(2):
            if i > j:
                pass

def voice_b():
    for k in range(8):
        pass
```

### アイデア B: コントラストをつける

2 つのループを使って、にぎやかなパートと静かなパートを対比させます。

**にぎやかな bass:**

```python
# @loop bass interval=2.0
def layer_a():
    for i in range(8):
        for j in range(4):
            if i == j:
                pass

def layer_b():
    for k in range(8):
        pass
```

**静かな pad:**

```python
# @loop pad interval=4.0
# 静寂
# もっと静寂
# ただの余白
def space(): pass
```

### アイデア C: コメントだけで演奏する

関数は 1 つだけ残して、コメントの量だけで演奏します。コメントが増えるほど残響が深くなり、音の空間が変化します。watch を使えば保存するたびに変化が聴こえます。

```python
# @loop ambient interval=4.0
# ここからコメントを増やしたり減らしたりするだけ
def f(): pass
```

### アイデア D: 関数名をストーリーとして書く

音は関数の中身の構造で決まります。関数名はどんな名前でも構いません。演奏しながらコードがストーリーになるような書き方もできます。

```python
# @loop narrative interval=2.0
def the_city_wakes_up():
    for hour in range(6):
        if hour > 4:
            pass

def rush_hour():
    for commuter in range(8):
        for train in range(3):
            if commuter % 2 == 0:
                pass
```

---

## 10. うまくいかないとき

### 音が鳴らない

まず SuperCollider 単体で音が出るか確認します。SuperCollider IDE で新しい空のドキュメントを開き、次の 1 行を実行します。

```supercollider
{ SinOsc.ar(440, 0, 0.1) ! 2 }.play;
```

実行は **Ctrl+Enter**（Mac は Cmd+Enter）です。音を止めるには **Ctrl+.**（Mac は Cmd+.）を押します。

ここで音が出ない場合は、PyCodeDJ ではなく SuperCollider のサーバー、Mac/PC の音量、出力先を確認してください。

次に SuperCollider のサーバーが起動しているか確認します。

```supercollider
s.boot;
```

次に `sc/synths.scd` を再実行します（Ctrl+A → Ctrl+Enter、Mac は Cmd+A → Cmd+Enter）。Post window に次が出るはずです。

```text
PyCodeDJ synths loaded. Ready. OSC port: 57120
```

OSC port が `57120` か確認するには、SuperCollider で次を実行します。

```supercollider
NetAddr.langPort.postln;
```

`57120` 以外が表示された場合は、Python 側でその番号を指定します。

```bash
pycodedj eval examples/demo.py::bass --sc-port 表示された番号
```

SuperCollider 側のシンセが読み込まれているか直接確認するには、SuperCollider で次を実行します。

```supercollider
~startLoop.value("bass", 1);
```

これで音が出れば、シンセ定義は読み込まれています。音を止めるには **Ctrl+.**（Mac は Cmd+.）です。

さらに OSC 受信を SuperCollider 内だけで確認するには、次を実行します。

```supercollider
NetAddr("127.0.0.1", NetAddr.langPort).sendMsg("/pycodedj/loop/bass/voice_count", 1);
```

これで音が出れば、SuperCollider 側の OSC 受信も動いています。

それでも音が鳴らない場合は、接続確認をします。

```bash
pycodedj eval examples/demo.py::bass
```

必要なら SuperCollider 側で OSC の受信ログを出せます。

```supercollider
OSCFunc.trace(true);
```

ログを止めるには次を実行します。

```supercollider
OSCFunc.trace(false);
```

### `[pycodedj] OSC error` というエラーが出る

SuperCollider が起動していないか、ポート番号が違います。

1. SuperCollider IDE が開いていて、サーバーが起動しているか確認する
2. `sc/synths.scd` を実行して `Ready.` メッセージを確認する
3. ポート番号がデフォルト（57120）から変わっていれば `--sc-port` で指定する

```bash
pycodedj eval demo.py::bass --sc-port 57200
```

### eval を実行したが何も出ない（フィードバックが出ない）

eval に成功すると `[pycodedj] ループ名  cutoff=...Hz ...` の行が出るはずです。何も出ない場合は stderr を確認してください。構文エラーが出ているかもしれません。

### `loop 'xxx' not found` というエラーが出る

ループ名の綴りが `# @loop` マーカーと一致していません。`::` の後ろの名前を確認してください。

```bash
# ファイルの中に `# @loop bass` と書いてあれば
pycodedj eval demo.py::bass   # OK
pycodedj eval demo.py::Bass   # NG（大文字小文字が違う）
```

### `file not found` というエラーが出る

ファイルのパスが正しくありません。カレントディレクトリを確認するか、フルパスで指定します。

```bash
pwd
ls

pycodedj eval /home/user/projects/myfile.py::bass
```

### `pycodedj watch` が watchdog をインストールしろと言う

```bash
pip install 'pycodedj[watch]'
```

最初のインストールで `[watch]` を付け忘れた場合はこれで追加できます。

### 構文エラーのあるコードを評価したとき

```
[pycodedj] syntax error (bass): invalid syntax ...
```

構文エラーがあったブロックは変化せず、直前の音を維持します。他のループは止まりません。コードの構文を修正してから再度評価してください。

---

## 11. コマンドと設定の全リスト

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
[pycodedj] bass  cutoff=418Hz  lfo=1.08Hz  reverb=0.00  voices=1
```

評価に失敗した場合（構文エラー / OSC 送信失敗）は stderr にエラーが出て終了コード 1 で終了します。

**使用例:**

```bash
pycodedj eval examples/demo.py::bass
pycodedj eval demo.py::melody --sc-host 192.168.1.10
pycodedj eval demo.py::pad --sc-port 57200
```

### `pycodedj watch`

ファイルを監視し、保存のたびに全ループを自動で再評価します。Ctrl+C で停止します。

```
pycodedj watch FILE [--sc-host HOST] [--sc-port PORT] [--debounce SECS]
```

| 引数・オプション | 説明 | デフォルト |
| :--- | :--- | :--- |
| `FILE` | 監視するファイルのパス | — |
| `--sc-host` | SuperCollider のホスト | `127.0.0.1` |
| `--sc-port` | SuperCollider の受信ポート番号 | `57120` |
| `--debounce` | 連続保存をまとめる待機時間（秒） | `0.3` |

**使用例:**

```bash
pycodedj watch examples/demo.py
pycodedj watch club_set.py --debounce 0.5
pycodedj watch myfile.py --sc-host 192.168.1.10
```

### ブロックマーカーの構文

```
# @loop <名前> [interval=秒]
```

| 要素 | 説明 |
| :--- | :--- |
| `<名前>` | 英数字とアンダースコアが使える。例: `bass`, `my_loop_1` |
| `interval=秒` | 省略可。現在は OSC で送信されず、将来の拡張用に記録される |

---

## 12. 仕組みをもっと知りたい人へ

### マッピングの数値

| パラメーター | 入力 | 出力範囲 | スケール |
| :--- | :--- | :--- | :--- |
| Cutoff | ブロック深さ 0–10 | 200–4000 Hz | リニア |
| LFO レート | 制御フロー数 0–10 | 0.1–5.0 Hz | リニア |
| リバーブ | コメント率 0.0–1.0 | 0.0–0.8 | リニア |
| 声部数 | 関数数（クランプ） | 1–4 | クランプ |

### OSC アドレス

SuperCollider と通信するアドレスの形式です。Hydra などのビジュアルツールを繋ぐときに参照してください。

| アドレス | 型 | 値域 |
| :--- | :--- | :--- |
| `/pycodedj/loop/<name>/voice_count` | int | 1–4（最初に送る） |
| `/pycodedj/loop/<name>/cutoff` | float | 200–4000 |
| `/pycodedj/loop/<name>/lfo_rate` | float | 0.1–5.0 |
| `/pycodedj/loop/<name>/reverb` | float | 0.0–0.8 |

### Python から直接使う

CLI を使わずにプログラムから操作することもできます。

```python
from pycodedj.block_parser import parse_blocks
from pycodedj.engine import Engine
from pycodedj.osc_bridge import OscBridge, OscEndpoint

bridge = OscBridge(audio=OscEndpoint("127.0.0.1", 57120))
engine = Engine(bridge=bridge)

source = open("demo.py").read()
blocks = {b.name: b for b in parse_blocks(source)}

params = engine.eval_block(blocks["bass"])
if params is not None:
    print(f"cutoff={params.cutoff:.0f}Hz")
```

`eval_block` は成功すると `MusicParams` を返します。構文エラーや OSC 送信失敗の場合は `None` を返します。

### モジュール構成

```
pycodedj/
├── block_parser.py   # @loop ブロックを分割する
├── analyzer.py       # コードの特徴量（深さ・数・比率）を抽出する
├── mapper.py         # 特徴量を音楽パラメーターに変換する
├── engine.py         # ブロック評価のパイプライン全体を管理する
├── osc_bridge.py     # SuperCollider へ OSC で送信する
├── watcher.py        # ファイル監視（watchdog ベース）
└── __main__.py       # CLI コマンドのエントリポイント
```
