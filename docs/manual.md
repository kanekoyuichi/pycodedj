# PyCodeDJ Manual

[日本語版マニュアルはこちら](https://github.com/kanekoyuichi/pycodedj/blob/main/docs/manual.ja.md)

> Write Python code. Hear it change in real time.

## Table of Contents

1. [What PyCodeDJ Does](#1-what-pycodedj-does)
2. [Install and Start](#2-install-and-start)
3. [Basic Loop Syntax](#3-basic-loop-syntax)
4. [Code Structure Mapping](#4-code-structure-mapping)
5. [Rhythm and Pitch with dj.pattern](#5-rhythm-and-pitch-with-djpattern)
6. [Multiple Loops](#6-multiple-loops)
7. [Sound Reference](#7-sound-reference)
8. [CLI Reference](#8-cli-reference)
9. [Troubleshooting](#9-troubleshooting)
10. [Under the Hood](#10-under-the-hood)

## 1. What PyCodeDJ Does

PyCodeDJ turns Python source code into live music. It does not execute your business logic to make sound. It parses your file, reads `@loop` blocks, maps code structure to musical parameters, and sends OSC messages to SuperCollider.

Add more `for` and `if` blocks and the modulation changes. Add comments and the reverb grows. Add `dj.pattern = "x . x ."` and that exact rhythm plays.

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

The function name is the loop name. Use it with commands such as `pycodedj eval demo.py::bass`, `pycodedj mute bass`, and `pycodedj stop bass`.

## 2. Install and Start

Requirements:

- Python 3.10 or later
- SuperCollider 3.12 or later

Install:

```bash
pip install 'pycodedj[watch]'
```

Load the SuperCollider synths:

1. Open `sc/synths.scd` in SuperCollider IDE.
2. Select all.
3. Run it with Ctrl+Enter, or Cmd+Enter on macOS.
4. Confirm the Post window says:

```text
PyCodeDJ synths loaded. Ready. OSC port: 57120
```

Verify:

```bash
pycodedj eval examples/demo.py::bass
```

## 3. Basic Loop Syntax

```python
from pycodedj import dj, loop

@loop(interval=1.0)
def loop_name():
    dj.volume = 0.3
    dj.eq = "flat"
    # Your normal Python code goes here.
    pass
```

`@loop(...)` marks a function as a PyCodeDJ loop. If the decorator has no name argument, the function name becomes the loop name.

Loop metadata lives in the `dj` namespace:

| Setting | Meaning | Default |
| :--- | :--- | :--- |
| `dj.volume` | Amplitude, 0.0 to 1.0 | `0.3` |
| `dj.eq` | EQ preset | `"flat"` |
| `dj.low` | Low-band multiplier, 0.0 to 2.0 | preset value |
| `dj.mid` | Mid-band multiplier, 0.0 to 2.0 | preset value |
| `dj.high` | High-band multiplier, 0.0 to 2.0 | preset value |
| `dj.pattern` | Rhythm and pitch pattern string | none |

`dj.low`, `dj.mid`, and `dj.high` override the selected `dj.eq` preset per band.

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

EQ presets:

| Preset | Character |
| :--- | :--- |
| `"flat"` | No adjustment |
| `"classic"` / `"classical"` | Restrained lows and highs, slightly forward mids |
| `"jazz"` | Warm lows, forward mids, slightly soft highs |
| `"rock"` / `"pop"` | Slight lows and highs boost |
| `"edm"` / `"hiphop"` / `"hip-hop"` | Stronger low end |
| `"acoustic"` | Restrained lows, slight mid-high lift |

## 4. Code Structure Mapping

When `dj.pattern` is absent, PyCodeDJ maps the shape of the function body to sound.

| Code feature | Music parameter | Effect |
| :--- | :--- | :--- |
| Max block depth | Filter cutoff | Deeper code sounds brighter |
| `if` / `for` / `while` count | LFO rate | More control flow moves faster |
| Nested `def` count | Voice count | More functions add voices, up to 4 |
| Comment ratio | Reverb mix | More comments add space |
| `dj.volume` | Amplitude | Direct level control |
| `dj.eq` + `dj.low/mid/high` | EQ | Per-loop tone shaping |

Example:

```python
@loop(interval=2.0)
def bass():
    dj.volume = 0.4
    for i in range(8):
        for j in range(4):
            if i == j:
                pass
```

## 5. Rhythm and Pitch with dj.pattern

Use `dj.pattern` when you want explicit rhythm or melody.

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

Pattern loop decorator arguments:

| Argument | Meaning | Default |
| :--- | :--- | :--- |
| `synth=` | SuperCollider synth name | empty / inferred for structure loops |
| `root=` | Root note | `"C4"` |
| `scale=` | Scale name | `"chromatic"` |
| `beat=` | Step length in seconds | `0.25` |
| `interval=` | Structure-loop update interval | `1.0` |

Pattern tokens:

| Token | Meaning |
| :--- | :--- |
| `x` | Trigger at the root note |
| `.` | Rest |
| `0`, `1`, `2` ... | Scale degree |
| `[0 3]` | Chord |
| `~` | Tie, extending the previous note/chord |

Examples:

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

`dj.pattern = p1` is intentionally not supported. Keep pattern strings visible in the loop body.

## 6. Multiple Loops

Multiple loops run independently. Editing one loop does not restart the others.

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
    # wide space
    # long tail
    pass
```

Run:

```bash
pycodedj watch examples/demo.py
```

## 7. Sound Reference

Use `synth=` to choose a SuperCollider synth for pattern loops or structure loops. The function name is still the loop name; `synth=` only chooses the sound.

```python
@loop(synth="bass_acid", root="A1", scale="minor", beat=0.25)
def acid():
    dj.volume = 0.25
    dj.pattern = "0 . 3 . 5 ."
```

Audition all sounds one at a time:

```bash
pycodedj eval examples/sound_showcase.py::kick_floor
pycodedj eval examples/sound_showcase.py::bass_acid
pycodedj eval examples/sound_showcase.py::lead_acid
```

### Kicks

| Synth | Character | Good for |
| :--- | :--- | :--- |
| `kick_hard` | Tight, punchy, short attack | Strong downbeats and minimal patterns |
| `kick_floor` | Full four-on-the-floor club kick | Main kick in dance/techno loops |
| `kick_pulse` | Lighter pulse kick | Secondary pulse, softer rhythmic support |
| `kick_soft` | Rounder kick with less click | Warm grooves and quieter sections |
| `kick_909` | Long electronic kick tail | House and techno foundations |
| `kick_click` | Short kick with a clear transient | Fast patterns that need definition |

### Bass

| Synth | Character | Good for |
| :--- | :--- | :--- |
| `bass_rumble` | Deep, loose low-end pressure | Rumble layers under a kick |
| `bass_reese` | Wide, moving Reese-style bass | Dark basslines and sustained movement |
| `bass_sub` | Clean sine-like sub weight | Fundamental low notes and floor pressure |
| `bass_acid` | Resonant 303-like acid tone | Patterned basslines and squelchy sequences |
| `bass_pluck` | Short plucked bass | Syncopated low-end hooks |
| `bass_fm` | Metallic FM low tone | Percussive basslines |
| `bass_mono` | Simple mono synth bass | Stable bass phrases |
| `bass_wobble` | Filter-modulated bass | Dubstep-style movement and breakdowns |

### Percussion

| Synth | Character | Good for |
| :--- | :--- | :--- |
| `hat_engine` | Short closed/open hat texture | 16th-note grids and forward motion |
| `hat_ride` | Longer open hat / ride color | Offbeats and sustained top-end energy |
| `clap_snap` | Sharp, dry clap | Snappy accents |
| `clap_snare` | Broader snare-like clap | Backbeats on beats 2 and 4 |
| `tom_drum` | Pitch-swept tom | Fills, transitions, low percussion |
| `snare_roll` | Repeated snare texture | Rolls and build-ups |
| `crash_noise` | Long noisy crash | Section changes and impacts |
| `rim_shot` | Dry rim transient | Sparse syncopation |
| `cowbell` | Metallic two-tone hit | Classic machine percussion |
| `perc_blip` | Small pitched blip | Minimal percussion and call-response details |
| `shaker_loop` | Continuous shaker texture | Top-end groove and motion |
| `tick_metal` | Tiny metallic tick | Glitch grids and high-frequency accents |
| `wood_block` | Woody resonant knock | Dry percussion patterns |

### Chords and Stabs

| Synth | Character | Good for |
| :--- | :--- | :--- |
| `chord_rave` | Bright rave stab | Short chord hits and hooks |
| `stab_neon` | Glossy synthetic stab | Melodic accents |
| `chord_dub` | Soft dub-techno chord | Spacious chord pulses |
| `stab_saw` | Detuned saw stab | Aggressive harmonic accents |
| `chord_organ` | Organ-like sustained chord | Warm harmonic beds |
| `bell_rave` | Metallic FM bell | Bright melodic stabs |
| `pad_minor` | Dark minor pad | Suspense and darker harmonic beds |
| `chord_deep` | Low filtered chord | Deep house / dub-techno pulses |
| `chord_glass` | Clear glassy chord | Clean bright harmonic accents |
| `pad_warm` | Smooth analog-style pad | Soft background harmony |
| `pad_string` | Bowed string-like synth pad | Long sustained emotional layers |
| `pad_choir` | Vocal-formant pad | Choral beds without a lead vocal |

### Leads and Notes

| Synth | Character | Good for |
| :--- | :--- | :--- |
| `lead_acid` | Acid-style lead | Melodic sequences |
| `lead_hoover` | Hoover-like lead | Big sustained gestures |
| `pluck_soft` | Gentle plucked tone | Sparse melodies |
| `arp_synth` | Arpeggiated synth tone | Fast melodic motion |
| `lead_square` | Hollow square-wave lead | Retro melodic hooks |
| `lead_fm` | Bell-like FM lead | Bright digital melodies |
| `lead_chip` | Short chiptune lead | Fast arcade-like phrases |
| `lead_saw` | Detuned saw lead | Larger melodic lines |
| `lead_whistle` | Thin sine-like whistle | High counter-melodies |
| `note` | Neutral note synth | General `dj.pattern` pitch tests and chords |

### Atmosphere and FX

| Synth | Character | Good for |
| :--- | :--- | :--- |
| `pad_shimmer` | Wide, slow shimmer | Background pads |
| `air_warehouse` | Industrial room tone | Space, air, and noise bed |
| `vox_ahh` | Vocal-like formant pad | Breath and choir-like layers |
| `fx_drop` | Low impact hit | Drops and transitions |
| `fx_riser` | Rising noise sweep | Build-ups |
| `fx_glitch` | Small glitch clicks | Detailed percussive texture |
| `drone_space` | Low evolving drone | Long ambient beds |
| `fx_down` | Descending noise sweep | Drops and section endings |
| `fx_zap` | Short falling laser-like hit | Small FX punctuation |
| `fx_noise` | Filtered noise burst | Impacts and transitions |
| `fx_laser` | Pitch-bending laser FX | Sci-fi accents |
| `fx_vinyl` | Crackle and hiss bed | Texture and lo-fi background |

## 8. CLI Reference

Evaluate one loop:

```bash
pycodedj eval FILE::LOOP
pycodedj eval examples/demo.py::bass
```

Watch a file and reload on save:

```bash
pycodedj watch examples/demo.py
```

Stop everything:

```bash
pycodedj panic
```

Stop one loop:

```bash
pycodedj stop bass
```

Mute and unmute:

```bash
pycodedj mute bass
pycodedj unmute bass
```

Common options:

| Option | Meaning | Default |
| :--- | :--- | :--- |
| `--sc-host` | SuperCollider host | `127.0.0.1` |
| `--sc-port` | SuperCollider OSC receive port | `57120` |
| `--debounce` | Watch-mode debounce seconds | `0.3` |

## 9. Troubleshooting

No sound:

1. Boot the SuperCollider server.
2. Run `sc/synths.scd`.
3. Confirm the Post window says `Ready. OSC port: 57120`.
4. Run `pycodedj eval examples/demo.py::bass`.

OSC error:

- SuperCollider is not running, or the port is wrong.
- If SuperCollider uses a different port, pass `--sc-port`.

Loop not found:

- The name after `::` must match the Python function name.
- `def bass():` is addressed as `demo.py::bass`.

Syntax error:

- Fix the file and save again. In watch mode, the previous good version keeps playing.

## 10. Under the Hood

PyCodeDJ parses Python source with `ast`. The runtime functions `loop`, `dj`, and `pattern` are intentionally no-op helpers so files can still be imported as Python.

Main modules:

```text
pycodedj/
├── _loop.py          # loop decorator and dj namespace
├── block_parser.py   # extracts @loop blocks and dj metadata
├── analyzer.py       # code feature extraction
├── mapper.py         # feature-to-music mapping
├── pattern.py        # pattern string parser
├── engine.py         # evaluation pipeline
├── osc_bridge.py     # OSC communication
├── watcher.py        # file watching
└── __main__.py       # CLI
```
