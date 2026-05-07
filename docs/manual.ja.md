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
9. [音色リファレンス](#9-音色リファレンス)
10. [演奏のアイデア](#10-演奏のアイデア)
11. [うまくいかないとき](#11-うまくいかないとき)
12. [コマンドと設定の全リスト](#12-コマンドと設定の全リスト)
13. [仕組みをもっと知りたい人へ](#13-仕組みをもっと知りたい人へ)

---

## 1. PyCodeDJ って何？

### ひとことで言うと

**Python のコードを書くと、リアルタイムに音が変わる楽器です。**

`for` ループを増やすと音の揺らぎが速くなります。関数を 3 つ書くと 3 声のポリフォニーになります。コメントをたくさん書くと、リバーブが深くかかって空間が広がります。`volume=` で音量を直接指定できます。

```python
from pycodedj import loop

@loop("main", interval=1.0)
def my_sound(volume=0.4):
    # コメントを増やすほど空間が広がる
    # もう一行
    # さらにもう一行
    for i in range(4):   # for を増やすと揺らぎが速くなる
        if i > 2:        # if を増やすとさらに速くなる
            pass
```

このコードを評価すると、ターミナルに次のように表示されます。

```
[pycodedj] main  cutoff=560Hz  lfo=1.08Hz  reverb=0.43  voices=1  amp=0.40
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

### SuperCollider で何をするの？

PyCodeDJ では、Python は音を直接鳴らしません。Python 側はコードを分析して、OSC という短いメッセージを SuperCollider に送ります。

SuperCollider 側では、次の 3 つを行います。

1. audio server を起動する
2. `sc/synths.scd` を読み込んで、PyCodeDJ 用のシンセを登録する
3. Python から届く OSC メッセージを受け取り、音を鳴らす

SuperCollider IDE には主に 2 つの場所があります。

- コードを書くドキュメント: `s.boot;` や `{ SinOsc... }.play;` などを入力して実行する場所
- Post window: 実行結果、エラー、`PyCodeDJ synths loaded...` などのログが表示される場所

このマニュアルで「SuperCollider で実行する」と書いてあるコードは、ターミナルではなく SuperCollider IDE のコードを書くドキュメントで実行します。

### ステップ 1: サーバーを起動する

SuperCollider IDE を開き、メニューから **Server > Boot Server** を選びます。

または、コード入力欄に次を書いて **Ctrl+Enter**（Mac は Cmd+Enter）で実行します。

```supercollider
s.boot;
```

画面下部に `localhost` が緑色に変わったら起動成功です。

この audio server が起動していないと、Python 側のコマンドが成功しても音は出ません。

### ステップ 2: シンセを読み込む

PyCodeDJ のプロジェクトフォルダにある `sc/synths.scd` を SuperCollider IDE で開きます。

**File > Open** で `sc/synths.scd` を開いたら、**Ctrl+A**（Mac は Cmd+A）で全選択し、**Ctrl+Enter**（Mac は Cmd+Enter）で実行します。

右側の Post window に次のメッセージが出れば準備完了です。

```
PyCodeDJ synths loaded. Ready. OSC port: 57120
```

このメッセージが出ない場合は [うまくいかないとき](#10-うまくいかないとき) を参照してください。

`sc/synths.scd` は、PyCodeDJ 用の音色と OSC 受信処理を SuperCollider に登録するファイルです。SuperCollider を再起動した後は、もう一度このファイルを実行してください。

### ステップ 3: 出力先を変更した場合

SuperCollider は audio server を起動した時点の出力先を使います。Mac/PC 側でスピーカー、イヤホン、オーディオインターフェースなどの出力先を変更した場合は、SuperCollider の audio server を起動し直してください。

まず SuperCollider IDE のコードを書くドキュメントで、使えるデバイス名を確認します。これはターミナルではなく SuperCollider で実行します。

```supercollider
ServerOptions.devices;
```

Post window にデバイス名の一覧が表示されます。使いたい出力先の名前を確認したら、同じく SuperCollider IDE のコードを書くドキュメントで次のように指定します。

```supercollider
s.quit;
s.options.outDevice = "ここに出力デバイス名を書く";
s.options.numInputBusChannels = 0;
s.boot;
```

入力を使わない場合は `numInputBusChannels = 0` にしておくと、入力デバイスとのサンプルレート不一致を避けやすくなります。

boot 後、SuperCollider 単体で音が出るか確認します。

```supercollider
{ SinOsc.ar(110, 0, 0.03) ! 2 }.play;
```

音が出たら、`sc/synths.scd` をもう一度実行します（Ctrl+A → Ctrl+Enter、Mac は Cmd+A → Cmd+Enter）。

### ステップ 4: 接続を確認する

ターミナルに戻り、次を実行します。

```bash
pycodedj eval examples/demo.py::bass
```

ターミナルに `[pycodedj] bass ...` と表示され、SuperCollider から音が出れば接続成功です。

SuperCollider はこのまま起動したままにしておいてください。

---

## 4. はじめての音を出す

### ステップ 1: デモファイルを確認する

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

`@loop("bass", ...)` が付いた関数が「bass ループ」です。関数名（`bass`, `melody`, `pad`）は自由につけられます。OSC に送られる名前は `@loop(...)` の第一引数です。

### ステップ 2: 音を出す

ターミナルで次を実行します。

```bash
pycodedj eval examples/demo.py::bass
```

`eval` は evaluate（評価する）の略です。このコマンドは `examples/demo.py` の `bass` ループを今すぐ読み取り、コード構造を分析して SuperCollider に音のパラメーターを送ります。

成功すると次のように表示されます。

```
[pycodedj] bass  cutoff=418Hz  lfo=1.08Hz  reverb=0.00  voices=1  amp=0.40
```

これがあなたの最初のライブコーディングです。続けて melody と pad も評価してみましょう。

```bash
pycodedj eval examples/demo.py::melody
pycodedj eval examples/demo.py::pad
```

3 つのループが同時に鳴っています。それぞれが独立して動いているのがわかるでしょうか。

### ステップ 3: コードを変えて音を変える

`examples/demo.py` をテキストエディタで開いて、bass ブロックを変えてみます。

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
[pycodedj] bass  cutoff=1200Hz  lfo=2.16Hz  reverb=0.00  voices=1  amp=0.40
```

cutoff が上がって音が明るくなり、lfo も速くなりました。音量を変えたいときは `volume=` の値を変えます。

```python
@loop("bass", interval=2.0)
def bass(volume=0.7):   # ← 大きくする
    ...
```

---

## 5. 保存するだけで音が変わる — watch モード

毎回 `pycodedj eval` を打つのは面倒です。`watch` コマンドを使うと、起動時に一度すべてのループを評価し、その後は**ファイルを保存するだけで自動的に全ループが再評価されます**。

### 起動方法

```bash
pycodedj watch examples/demo.py
```

```
[pycodedj] watching demo.py — save to reload (Ctrl+C to stop)
[pycodedj] reloaded demo.py (3 loop(s))
```

起動直後に一度音が鳴ります。あとはエディタでコードを書いて保存するだけです。保存のたびに次のように出力されます。

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

PyCodeDJ は Python コードの「構造」を 5 つの音楽パラメーターに変換します。

### 対応表

| コードのどこを見るか | 変わる音のパラメーター | 変化のイメージ |
| :--- | :--- | :--- |
| ブロック構造の深さ（`if` や `for` のネスト） | フィルターの明るさ（Cutoff） | 深くなるほど音が明るく開く |
| 制御フローの数（`if` / `for` / `while` の合計） | 音の揺らぎの速さ（LFO レート） | 多いほど揺らぎが速くなる |
| 関数の数（`def` の数） | 音の重なり（ポリフォニー声部数） | 多いほど音が重なる（最大 4） |
| コメントの割合（コメント行 ÷ 全行） | 空間の広さ（リバーブの深さ） | 多いほど残響が増える |
| `volume=` 引数のデフォルト値 | 音量（Amplitude） | 直接指定。0.0〜1.0 |

### 実例で見る

#### フィルターの明るさ（ネストの深さ）

```python
@loop("test", interval=1.0)
def f(volume=0.3):
    # ネスト深さ 1 → フィルター最小（こもった音）
    pass
```

```python
@loop("test", interval=1.0)
def f(volume=0.3):
    # ネスト深さ 4 → フィルター最大（明るい音）
    for i in range(4):
        for j in range(4):
            if i == j:
                pass
```

> `x = 1 + 2 * (3 + 4)` のような演算式はネストの深さにカウントされません。`if` や `for` などのブロック構造だけを数えます。

#### 揺らぎの速さ（制御フローの数）

```python
@loop("test", interval=1.0)
def f(volume=0.3):
    # 制御フロー 0 個 → 揺らぎ最小（ゆったり）
    pass
```

```python
@loop("test", interval=1.0)
def f(volume=0.3):
    for i in range(4):   # 1 つ目
        if i > 2:        # 2 つ目
            while False: # 3 つ目
                pass
```

#### 音の重なり（関数の数）

```python
@loop("test", interval=1.0)
def solo(volume=0.3):
    # 関数 1 個 → 1 声（ソロ）
    pass
```

```python
@loop("test", interval=1.0)
def f(volume=0.3):
    # 関数 4 個 → 4 声（最大ポリフォニー）
    def voice_a(): pass
    def voice_b(): pass
    def voice_c(): pass
    def voice_d(): pass
```

#### 空間の広さ（コメント率）

```python
@loop("test", interval=1.0)
def f(volume=0.3):
    # コメントなし → ドライな音
    x = 1
    return x
```

```python
@loop("test", interval=1.0)
def f(volume=0.3):
    # コメントが多い → 深い残響
    # 余白
    # 余白
    # 余白
    pass
```

#### 音量（volume 引数）

```python
@loop("kick", interval=1.0)
def my_kick(volume=0.9):   # 大きい
    ...

@loop("shimmer", interval=4.0)
def bg_shimmer(volume=0.05):  # 奥で小さく
    ...
```

---

## 7. 複数のループを同時に動かす

PyCodeDJ の最大の特徴は、**複数のループが独立して動き続ける**ことです。

### 基本の使い方

`@loop("名前", ...)` デコレータを付けた関数を並べるだけで、複数のループを作れます。

```python
from pycodedj import loop

@loop("bass", interval=2.0)
def my_bass(volume=0.4):
    for i in range(8):
        pass

@loop("chord", interval=1.0)
def my_chord(volume=0.2):
    def chord_a(): pass
    def chord_b(): pass

@loop("texture", interval=4.0)
def bg(volume=0.06):
    # 背景
    # 空気
    pass
```

それぞれを別々に評価できます。

```bash
pycodedj eval myfile.py::bass
pycodedj eval myfile.py::chord
pycodedj eval myfile.py::texture
```

または `watch` を使えばファイルを保存するだけで全ループが一斉に更新されます。

### ループを止めるには

ループを止めたいときは、その `@loop` デコレータごと関数を削除して保存します。watch モードなら保存時に自動で止まります。

eval で止めたい場合は、関数名の `def` だけを残して本体を空にし、ファイルからブロックが消えたと判定されるよう `@loop` を削除します。

---

## 8. クラブセット例 — club_set.py を動かす

`examples/club_set.py` は、クラブのグルーヴとして成立しやすい多層デモファイルです。foundation / movement / body / harmonic / lead / hats / space / texture の 8 層 14 ループ構成で、各ループのコード構造が音域・変調速度・リバーブを決定します。

全 30 音色を 1 音ずつ確認したい場合は `examples/sound_showcase.py` を使います。

```bash
pycodedj eval examples/sound_showcase.py::bass_acid
pycodedj eval examples/sound_showcase.py::riser_noise
pycodedj eval examples/sound_showcase.py::bell_rave
```

`@loop("kick_hard", ...)` のようなループ名は、SuperCollider 側では音色名として解釈されます。たとえば `kick_hard` はキック系、`bass_reese` はベース系のシンセに割り当てられます。Python 側でグルーヴや構成を変えるだけなら、通常は `sc/synths.scd` を編集する必要はありません。まったく新しい音色エンジンを増やしたいときだけ、SuperCollider 側に SynthDef を追加します。

### club_set.py のループ構成

| ループ名 | レイヤー | キャラクター |
| :--- | :--- | :--- |
| `kick_hard` | foundation | 硬い四つ打ちキック（depth=1、ドライ） |
| `bass_rumble` | foundation | キック下のランブル（depth=1、ドライ） |
| `bass_reese` | movement | 揺れる Reese ベース（depth=4、中域） |
| `hat_ride` | movement | ライド/オープンハット（depth=4） |
| `clap_snap` | body | スナップクラップ（depth=4、速い LFO） |
| `clap_snare` | body | スネア寄りのアクセント（depth=4） |
| `chord_rave` | harmonic | レイブスタブ（depth=6、明るい） |
| `neon_stab` | harmonic | アンサースタブ（depth=5） |
| `lead_hoover` | lead | Hoover 風リード（depth=5、微リバーブ） |
| `hat_engine` | hats | ハットグリッド（depth=6、最速 LFO） |
| `shimmer_pad` | space | シマーパッド（コメント多め、高リバーブ） |
| `warehouse_air` | space | 倉庫の空気感（コメントのみ、最大リバーブ） |
| `glitch_ticks` | texture | グリッチテクスチャ（depth=4、速い LFO） |
| `fx_impact` | texture | ドロップのインパクト（depth=5） |

### 動かしてみる

watch で起動して、エディタで各ブロックを編集しながら音を変えていきます。起動直後に全ループが一度評価されるので、保存しなくてもまず音が鳴ります。

```bash
pycodedj watch examples/club_set.py
```

個別にループを評価したい場合は eval を使います。

```bash
pycodedj eval examples/club_set.py::kick_hard
pycodedj eval examples/club_set.py::bass_reese
pycodedj eval examples/club_set.py::chord_rave
```

### 演奏してみる

**音量を変える:** `volume=` の値を変えて保存するだけで、そのループの音量が即座に変わります。

```python
@loop("lead_hoover", interval=4.0)
def hoover(volume=0.4):   # ← 前に出したいとき
    ...
```

**空間を変える:** `warehouse_air` や `shimmer_pad` のコメントを増やしたり減らしたりすると、リバーブの深さが変わります。

```python
@loop("warehouse_air", interval=4.0)
def room_tone(volume=0.06):
    # concrete walls
    # low ceiling pressing down
    # crowd warmth
    pass
```

コメントを 1 行だけ残して保存してみてください。空間が一気に乾いた音になります。

**声部を変える:** `chord_rave` の内部関数を 1 つ減らすと、3 声から 2 声になって音が薄くなります。

---

## 9. 音色リファレンス

`@loop` の第一引数（ループ名）を変えると、SuperCollider 側で使う音色を選べます。全 30 音色を 1 音ずつ確認したい場合は `examples/sound_showcase.py` を使います。

```bash
pycodedj eval examples/sound_showcase.py::bass_acid
pycodedj eval examples/sound_showcase.py::riser_noise
pycodedj eval examples/sound_showcase.py::bell_rave
```

**キック**

| ループ名 | 音 |
| :--- | :--- |
| `kick_hard` | 硬めでアタックの強いキック |
| `floor_kick` | 太い四つ打ちキック |
| `kick_pulse` | 軽めのパルスキック |

**ベース**

| ループ名 | 音 |
| :--- | :--- |
| `bass_rumble` | キック由来の低いランブル |
| `bass_reese` | 揺れる Reese 系ベース |
| `sub_bass` | サブベース |
| `bass_acid` | 303スタイルのアシッドベース（スクウェルチ付き） |

**パーカッション**

| ループ名 | 音 |
| :--- | :--- |
| `hat_engine` | クローズ/オープンのハットグリッド |
| `hat_ride` | 長めのライド/オープンハット |
| `clap_snap` | 鋭いクラップ |
| `clap_snare` | スネア寄りのクラップ |
| `tom_drum` | フロアタム（ピッチスイープあり） |
| `snare_roll` | スネアロール（lfoRate で速度制御） |
| `noise_crash` | クラッシュシンバル（長いテール） |

**コード・スタブ**

| ループ名 | 音 |
| :--- | :--- |
| `chord_rave` | 明るいレイブスタブ |
| `neon_stab` | ネオン系スタブコード |
| `dub_chord` | ダブコード |
| `stab_saw` | デチューンソーコードスタブ |
| `organ_chord` | ハモンドオルガン風コード |
| `bell_rave` | インハーモニクスFMレイブベル |

**リード**

| ループ名 | 音 |
| :--- | :--- |
| `acid_lead` | アシッド系リード |
| `lead_hoover` | Hoover 風リード |
| `soft_pluck` | やわらかいプラック |
| `synth_arp` | アルペジオシンセ（高速ノートシーケンス） |

**アトモスフィア**

| ループ名 | 音 |
| :--- | :--- |
| `shimmer_pad` | 深いシマーパッド |
| `warehouse_air` | 倉庫っぽい空気感 |
| `vox_ahh` | フォルマントボーカルパッド |

**FX**

| ループ名 | 音 |
| :--- | :--- |
| `fx_impact` | 低いインパクト |
| `riser_noise` | ノイズライザー（8秒でスイープ上昇） |
| `glitch_ticks` | 細かいグリッチ音 |

---

## 10. 演奏のアイデア

### アイデア A: シンプルから複雑へ育てる

最初は空のコードから始めて、少しずつ要素を加えていきます。watch を起動した状態で保存するたびに音が変わっていく様子を楽しめます。

```python
# 段階 1: ほぼ無音（フィルター最小、ポリフォニー 1）
@loop("main", interval=1.0)
def f(volume=0.3):
    pass
```

```python
# 段階 2: 揺らぎを加える
@loop("main", interval=1.0)
def f(volume=0.3):
    for i in range(4):
        pass
```

```python
# 段階 3: さらに深く
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

### アイデア B: コントラストをつける

2 つのループを使って、にぎやかなパートと静かなパートを対比させます。

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
```

```python
@loop("pad", interval=4.0)
def space(volume=0.08):
    # 静寂
    # もっと静寂
    # ただの余白
    pass
```

### アイデア C: コメントだけで演奏する

関数は 1 つだけ残して、コメントの量だけで演奏します。コメントが増えるほど残響が深くなり、音の空間が変化します。

```python
@loop("ambient", interval=4.0)
def f(volume=0.15):
    # ここからコメントを増やしたり減らしたりするだけ
    pass
```

### アイデア D: 関数名をストーリーとして書く

音は関数の中身の構造で決まります。関数名はどんな名前でも構いません。演奏しながらコードがストーリーになるような書き方もできます。

```python
@loop("narrative", interval=2.0)
def the_city_wakes_up(volume=0.3):
    for hour in range(6):
        if hour > 4:
            pass

@loop("texture", interval=1.0)
def rush_hour(volume=0.2):
    for commuter in range(8):
        for train in range(3):
            if commuter % 2 == 0:
                pass
```

---

## 11. うまくいかないとき

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

ループ名の綴りが `@loop(...)` の第一引数と一致していません。`::` の後ろの名前を確認してください。

```bash
# ファイルの中に @loop("bass", ...) と書いてあれば
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

## 12. コマンドと設定の全リスト

### `pycodedj eval`

指定したループを一度だけ評価して SuperCollider にパラメーターを送ります。
`eval` は evaluate（評価する）の略で、「このループを今すぐ音に反映する」という意味です。

```
pycodedj eval FILE::LOOP [--sc-host HOST] [--sc-port PORT]
```

| 引数・オプション | 説明 | デフォルト |
| :--- | :--- | :--- |
| `FILE::LOOP` | ファイルパスとループ名を `::` で区切る | — |
| `--sc-host` | SuperCollider のホスト | `127.0.0.1` |
| `--sc-port` | SuperCollider の受信ポート番号 | `57120` |

`FILE::LOOP` は、`FILE` の中にある `@loop("LOOP", ...)` のブロックを指定します。たとえば `examples/demo.py::bass` は、`@loop("bass", ...)` デコレータが付いた関数を評価します。

成功すると stdout にフィードバックが出ます。

```
[pycodedj] bass  cutoff=418Hz  lfo=1.08Hz  reverb=0.00  voices=1  amp=0.40
```

評価に失敗した場合（構文エラー / OSC 送信失敗）は stderr にエラーが出て終了コード 1 で終了します。

**使用例:**

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

### ループの書き方

```python
from pycodedj import loop

@loop("ループ名", interval=秒)
def 関数名(volume=音量):
    # 関数の中身が音楽パラメーターに変換される
    ...
```

| 要素 | 説明 |
| :--- | :--- |
| `"ループ名"` | SuperCollider に送られる名前。英数字とアンダースコア。例: `bass`, `kick_hard` |
| `interval=秒` | ループの更新間隔（秒）。省略時は 1.0 |
| `volume=音量` | 音量。0.0〜1.0 の浮動小数点数。省略時は 0.3 |
| 関数名 | 自由につけられる。ループ名とは独立している |

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

SuperCollider と通信するアドレスの形式です。Hydra などのビジュアルツールを繋ぐときに参照してください。

| アドレス | 型 | 値 |
| :--- | :--- | :--- |
| `/pycodedj/loop/<name>/params` | int, float, float, float, float | `voice_count`, `cutoff`, `lfo_rate`, `reverb`, `amp` の順 |
| `/pycodedj/loop/<name>/voice_count` | int | 1–4（互換用） |
| `/pycodedj/loop/<name>/cutoff` | float | 200–4000（互換用） |
| `/pycodedj/loop/<name>/lfo_rate` | float | 0.1–5.0（互換用） |
| `/pycodedj/loop/<name>/reverb` | float | 0.0–0.8（互換用） |
| `/pycodedj/loop/<name>/amp` | float | 0.0–1.0（互換用） |

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
├── engine.py         # ブロック評価のパイプライン全体を管理する
├── osc_bridge.py     # SuperCollider へ OSC で送信する
├── watcher.py        # ファイル監視（watchdog ベース）
└── __main__.py       # CLI コマンドのエントリポイント
```
