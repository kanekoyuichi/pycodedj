# PyCodeDJ マニュアル

[English manual](https://github.com/kanekoyuichi/pycodedj/blob/main/docs/manual.md)

> Python コードを書く。保存する。音が変わる。

## 目次

1. [PyCodeDJ とは](#1-pycodedj-とは)
2. [インストールと起動](#2-インストールと起動)
3. [ループの基本構文](#3-ループの基本構文)
4. [コード構造マッピング](#4-コード構造マッピング)
5. [dj.pattern でリズムと音程を指定する](#5-djpattern-でリズムと音程を指定する)
6. [複数ループ](#6-複数ループ)
7. [音色リファレンス](#7-音色リファレンス)
8. [CLI リファレンス](#8-cli-リファレンス)
9. [トラブルシューティング](#9-トラブルシューティング)
10. [内部構成](#10-内部構成)

## 1. PyCodeDJ とは

PyCodeDJ は Python のソースコードをライブ演奏に変換するツールです。業務コードを実行して音を出すのではなく、ファイルを AST 解析し、`@loop` が付いた関数の構造と `dj.*` のメタ情報を読み取って SuperCollider に OSC を送ります。

`for` や `if` が増えるとモジュレーションが変わります。コメントが増えるとリバーブが深くなります。`dj.pattern = "x . x ."` と書くと、そのリズムで鳴ります。

```python
from pycodedj import dj, loop

@loop(interval=2.0)
def bass():
    dj.volume = 0.4
    for i in range(8):
        if i % 2 == 0:
            pass

@loop(synth="kick_floor", beat=0.25)
def kick():
    dj.volume = 0.8
    dj.pattern = "x . x ."
```

関数名がループ名になります。`pycodedj eval demo.py::bass`、`pycodedj mute bass`、`pycodedj stop bass` のように指定します。

## 2. インストールと起動

必要なもの:

- Python 3.10 以上
- SuperCollider 3.12 以上

インストール:

```bash
pip install 'pycodedj[watch]'
```

SuperCollider 側の準備:

1. SuperCollider IDE で `sc/synths.scd` を開く。
2. 全選択する。
3. Ctrl+Enter、macOS では Cmd+Enter で実行する。
4. Post window に次が出れば準備完了。

```text
PyCodeDJ synths loaded. Ready. OSC port: 57120
```

確認:

```bash
pycodedj eval examples/demo.py::bass
```

## 3. ループの基本構文

```python
from pycodedj import dj, loop

@loop(interval=1.0)
def loop_name():
    dj.volume = 0.3
    dj.eq = "flat"
    # 通常の Python コードを書く
    pass
```

`@loop(...)` を付けた関数が PyCodeDJ の 1 ループです。デコレータに名前を書かない場合、関数名がそのままループ名になります。

ループの音楽メタ情報は `dj` 名前空間に書きます。

| 設定 | 意味 | デフォルト |
| :--- | :--- | :--- |
| `dj.volume` | 音量。0.0〜1.0 | `0.3` |
| `dj.eq` | EQ プリセット | `"flat"` |
| `dj.low` | 低域倍率。0.0〜2.0 | プリセット値 |
| `dj.mid` | 中域倍率。0.0〜2.0 | プリセット値 |
| `dj.high` | 高域倍率。0.0〜2.0 | プリセット値 |
| `dj.pattern` | リズムと音程のパターン文字列 | なし |

`dj.low`, `dj.mid`, `dj.high` を書くと、`dj.eq` の該当帯域だけ上書きします。

```python
@loop(interval=0.5)
def bass():
    dj.volume = 0.45
    dj.eq = "edm"

@loop(interval=0.25)
def hats():
    dj.volume = 0.08
    dj.eq = "edm"
    dj.low = 0.5
    dj.high = 1.25
```

EQ プリセット:

| プリセット | 傾向 |
| :--- | :--- |
| `"flat"` | 補正なし |
| `"classic"` / `"classical"` | 低域と高域を控えめにして中域を少し出す |
| `"jazz"` | 暖かい低域、中域の存在感、少し柔らかい高域 |
| `"rock"` / `"pop"` | 低域と高域を少し上げる |
| `"edm"` / `"hiphop"` / `"hip-hop"` | 低域を強める |
| `"acoustic"` | 低域を控えめにして中高域を少し上げる |

## 4. コード構造マッピング

`dj.pattern` がないループでは、関数本体の「形」が音になります。

| 読み取るもの | 音楽パラメーター | 効果 |
| :--- | :--- | :--- |
| ブロックの最大ネスト深度 | フィルター cutoff | 深いほど明るい |
| `if` / `for` / `while` の数 | LFO レート | 多いほど速い |
| ネストした `def` の数 | 声部数 | 多いほど厚い。最大 4 |
| コメント率 | リバーブ | コメントが多いほど空間が広い |
| `dj.volume` | 音量 | 直接指定 |
| `dj.eq` + `dj.low/mid/high` | EQ | ループごとの音質補正 |

例:

```python
@loop(interval=2.0)
def bass():
    dj.volume = 0.4
    for i in range(8):
        for j in range(4):
            if i == j:
                pass
```

## 5. dj.pattern でリズムと音程を指定する

明示的にリズムやメロディを書きたい場合は `dj.pattern` を使います。

```python
from pycodedj import dj, loop

@loop(synth="kick_floor", beat=0.25)
def kick():
    dj.volume = 0.8
    dj.pattern = "x . x ."

@loop(synth="bass_acid", root="A1", scale="minor", beat=0.25)
def bass():
    dj.volume = 0.35
    dj.pattern = "0 . [0 3] ~ 5 . 3 ."
```

パターン用の `@loop` 引数:

| 引数 | 意味 | デフォルト |
| :--- | :--- | :--- |
| `synth=` | SuperCollider の音色名 | 空 / 構造ループでは推定 |
| `root=` | ルート音 | `"C4"` |
| `scale=` | スケール名 | `"chromatic"` |
| `beat=` | 1 ステップの長さ（秒） | `0.25` |
| `interval=` | 構造ループの更新間隔 | `1.0` |

パターンのトークン:

| トークン | 意味 |
| :--- | :--- |
| `x` | ルート音で鳴らす |
| `.` | 休符 |
| `0`, `1`, `2` ... | スケール度数 |
| `[0 3]` | コード |
| `~` | 直前の音やコードを伸ばす |

例:

```python
@loop(synth="hat_engine", beat=0.25)
def hat():
    dj.pattern = "x x x x x x x x"

@loop(synth="lead_acid", root="A3", scale="minor", beat=0.25)
def melody():
    dj.pattern = "0 . 3 . 5 . 7 ."

@loop(synth="note", root="C3", scale="minor", beat=0.5)
def chord():
    dj.pattern = "[0 2 4] . [0 3] ."
```

`dj.pattern = p1` のような変数参照は読み取りません。パターン文字列はループ本体に直接書いてください。

## 6. 複数ループ

複数のループは独立して動きます。1 つを編集しても他のループは止まりません。

```python
from pycodedj import dj, loop

@loop(synth="kick_floor", beat=0.25)
def kick():
    dj.volume = 0.8
    dj.pattern = "x . x ."

@loop(interval=2.0)
def bass():
    dj.volume = 0.4
    for i in range(8):
        if i % 2 == 0:
            pass

@loop(interval=4.0)
def pad():
    dj.volume = 0.08
    # 広い空間
    # 長い残響
    pass
```

実行:

```bash
pycodedj watch examples/demo.py
```

## 7. 音色リファレンス

`synth=` に SuperCollider の音色名を指定します。関数名はループ名のままで、`synth=` は鳴らす音色だけを選びます。

```python
@loop(synth="bass_acid", root="A1", scale="minor", beat=0.25)
def acid():
    dj.volume = 0.25
    dj.pattern = "0 . 3 . 5 ."
```

全音色を 1 つずつ試聴:

```bash
pycodedj eval examples/sound_showcase.py::kick_floor
pycodedj eval examples/sound_showcase.py::bass_acid
pycodedj eval examples/sound_showcase.py::lead_acid
```

### Kick

| 音色 | キャラクター | 向いている用途 |
| :--- | :--- | :--- |
| `kick_hard` | タイトでパンチのある短いキック | 強い頭拍、ミニマルなパターン |
| `kick_floor` | 太い four-on-the-floor キック | ダンス/テクノ系の主キック |
| `kick_pulse` | 軽めのパルスキック | 補助的な拍、柔らかいリズム支え |
| `kick_soft` | クリックを抑えた丸いキック | 柔らかいグルーヴ、静かな展開 |
| `kick_909` | 長めの電子的なキックテール | ハウス/テクノの土台 |
| `kick_click` | 立ち上がりが明確な短いキック | 速いパターン、輪郭が欲しい場面 |

### Bass

| 音色 | キャラクター | 向いている用途 |
| :--- | :--- | :--- |
| `bass_rumble` | 深くゆるい低域の圧力 | キック下のランブル層 |
| `bass_reese` | 横に広がる Reese 系ベース | 暗いベースライン、持続する動き |
| `bass_sub` | クリーンなサブ低域 | ルート低音、床を支える音 |
| `bass_acid` | レゾナンスのある 303 風ベース | アシッドベースライン、細かいシーケンス |
| `bass_pluck` | 短いプラック系ベース | シンコペーションのある低域フック |
| `bass_fm` | 金属感のある FM ベース | 打楽器的なベースライン |
| `bass_mono` | 素直なモノシンセベース | 安定したベースフレーズ |
| `bass_wobble` | フィルターが揺れるベース | ダブステップ風の動き、ブレイク |

### Percussion

| 音色 | キャラクター | 向いている用途 |
| :--- | :--- | :--- |
| `hat_engine` | 短いクローズ/オープンハット感 | 16分グリッド、前に進むノリ |
| `hat_ride` | 長めのオープンハット/ライド感 | 裏拍、持続する高域エネルギー |
| `clap_snap` | 鋭く乾いたクラップ | 短いアクセント |
| `clap_snare` | スネア寄りの広いクラップ | 2拍4拍のバックビート |
| `tom_drum` | ピッチが動くタム | フィル、展開、低めの打楽器 |
| `snare_roll` | 連打系スネア | ロール、ビルドアップ |
| `crash_noise` | 長いノイズクラッシュ | セクション切替、インパクト |
| `rim_shot` | 乾いたリムのアタック | 隙間のあるシンコペーション |
| `cowbell` | 金属的な2音のヒット | クラシックなマシンパーカッション |
| `perc_blip` | 小さな音程付きブリップ | ミニマルな打楽器、細かい返し |
| `shaker_loop` | 連続するシェイカー感 | 高域のグルーヴ、前に進む動き |
| `tick_metal` | 小さな金属クリック | グリッチグリッド、高域アクセント |
| `wood_block` | 木質のノック音 | 乾いたパーカッションパターン |

### Chords / Stabs

| 音色 | キャラクター | 向いている用途 |
| :--- | :--- | :--- |
| `chord_rave` | 明るいレイヴスタブ | 短いコードヒット、フック |
| `stab_neon` | 艶のあるシンセスタブ | メロディックなアクセント |
| `chord_dub` | 柔らかい dub techno 風コード | 空間のあるコードパルス |
| `stab_saw` | デチューンした saw スタブ | 強めの和声アクセント |
| `chord_organ` | オルガン風コード | 暖かい和声の土台 |
| `bell_rave` | 金属的な FM ベル | 明るいメロディックスタブ |
| `pad_minor` | 暗いマイナーパッド | 不穏さ、暗めの和声ベッド |
| `chord_deep` | 低くフィルターされたコード | ディープハウス/dub techno のパルス |
| `chord_glass` | 透明感のあるコード | 明るくきれいな和声アクセント |
| `pad_warm` | なめらかなアナログ風パッド | 柔らかい背景の和声 |
| `pad_string` | ストリングス風シンセパッド | 長く伸びる情緒的なレイヤー |
| `pad_choir` | 声のフォルマントを持つパッド | リードボーカルなしの合唱感 |

### Leads / Notes

| 音色 | キャラクター | 向いている用途 |
| :--- | :--- | :--- |
| `lead_acid` | アシッド風リード | メロディックなシーケンス |
| `lead_hoover` | Hoover 系リード | 大きく伸びるフレーズ |
| `pluck_soft` | 柔らかいプラック | 隙間のあるメロディ |
| `arp_synth` | アルペジオ向きシンセ | 速いメロディの動き |
| `lead_square` | 空洞感のある矩形波リード | レトロなメロディックフック |
| `lead_fm` | ベル寄りの FM リード | 明るいデジタルメロディ |
| `lead_chip` | 短いチップチューン風リード | 速いゲーム音楽風フレーズ |
| `lead_saw` | デチューンした saw リード | 大きめのメロディライン |
| `lead_whistle` | 細いサイン波風ホイッスル | 高域の対旋律 |
| `note` | ニュートラルな音程シンセ | `dj.pattern` の音程確認、コード確認 |

### Atmosphere / FX

| 音色 | キャラクター | 向いている用途 |
| :--- | :--- | :--- |
| `pad_shimmer` | 広くゆっくりしたシマーパッド | 背景のパッド |
| `air_warehouse` | 工業的な部屋鳴り | 空気感、ノイズベッド |
| `vox_ahh` | 声のフォルマント風パッド | ブレス、合唱風レイヤー |
| `fx_drop` | 低いインパクト音 | ドロップ、展開 |
| `fx_riser` | 上昇するノイズ | ビルドアップ |
| `fx_glitch` | 小さなグリッチクリック | 細かい打楽器テクスチャ |
| `drone_space` | 低く変化するドローン | 長いアンビエントの土台 |
| `fx_down` | 下降するノイズスイープ | ドロップ、セクション終わり |
| `fx_zap` | 短く落ちるレーザー風ヒット | 小さな FX の句読点 |
| `fx_noise` | フィルターされたノイズバースト | インパクト、展開 |
| `fx_laser` | ピッチが曲がるレーザー FX | SF 風アクセント |
| `fx_vinyl` | クラックルとヒスの背景 | 質感、ローファイな背景 |

## 8. CLI リファレンス

1 つのループを評価:

```bash
pycodedj eval FILE::LOOP
pycodedj eval examples/demo.py::bass
```

ファイルを監視して保存ごとに更新:

```bash
pycodedj watch examples/demo.py
```

全停止:

```bash
pycodedj panic
```

1 つのループを停止:

```bash
pycodedj stop bass
```

ミュート / 解除:

```bash
pycodedj mute bass
pycodedj unmute bass
```

主なオプション:

| オプション | 意味 | デフォルト |
| :--- | :--- | :--- |
| `--sc-host` | SuperCollider のホスト | `127.0.0.1` |
| `--sc-port` | SuperCollider の OSC 受信ポート | `57120` |
| `--debounce` | watch モードの debounce 秒数 | `0.3` |

## 9. トラブルシューティング

音が出ない:

1. SuperCollider のサーバーを boot する。
2. `sc/synths.scd` を実行する。
3. Post window に `Ready. OSC port: 57120` が出ているか確認する。
4. `pycodedj eval examples/demo.py::bass` を実行する。

OSC error:

- SuperCollider が起動していないか、ポートが違います。
- ポートが違う場合は `--sc-port` を指定してください。

loop not found:

- `::` の後ろは Python の関数名と一致させます。
- `def bass():` は `demo.py::bass` で指定します。

SyntaxError:

- ファイルを修正して保存してください。watch モードでは直前の正常なループが鳴り続けます。

## 10. 内部構成

PyCodeDJ は Python ソースを `ast` で解析します。`loop`, `dj`, `pattern` は実行時には no-op に近いヘルパーで、通常の Python ファイルとして import できます。

主なモジュール:

```text
pycodedj/
├── _loop.py          # loop デコレータと dj 名前空間
├── block_parser.py   # @loop ブロックと dj メタ情報の抽出
├── analyzer.py       # コード特徴量抽出
├── mapper.py         # 特徴量から音楽パラメーターへの変換
├── pattern.py        # pattern 文字列パーサー
├── engine.py         # 評価パイプライン
├── osc_bridge.py     # OSC 通信
├── watcher.py        # ファイル監視
└── __main__.py       # CLI
```
