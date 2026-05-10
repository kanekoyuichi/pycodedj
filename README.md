# PyCodeDJ

[日本語版 README はこちら](https://github.com/kanekoyuichi/pycodedj/blob/main/README.ja.md) · [Full Manual (EN)](https://github.com/kanekoyuichi/pycodedj/blob/main/docs/manual.md) · [マニュアル (JA)](https://github.com/kanekoyuichi/pycodedj/blob/main/docs/manual.ja.md)

A live-coding environment that translates Python code structure into music in real time. Every save changes the performance.

---

## Concept

PyCodeDJ connects "writing code" directly to "making sound."

Add more `for` loops and the modulation speeds up. Deepen nesting and the filter opens up. Fill in comments and the space grows. Write `dj.pattern = "x . x ."` and that rhythm plays. Write `dj.pattern = "0 . 3 . 5 ."` and those pitches ring out.

Two things set it apart from existing Python ↔ SuperCollider bridges (sc3nb, supriya):

- **Hot-reload performance** — swap out a loop without stopping it. Saving a file is an immediate sound change.
- **Two performance styles** — auto-generation from code structure, and explicit `dj.pattern` notation for rhythm and pitch. Mix them freely in the same file.

---

## Architecture

```
[Python engine]  →OSC→  [SuperCollider]  →audio out→  speakers
      ↓ OSC
  [Hydra etc.]  →video out→  screen
```

| Layer | Role | Technology |
| :--- | :--- | :--- |
| Control | Code analysis, scheduling, OSC dispatch | Python 3.10+, python-osc, watchdog |
| Audio | Real-time sound synthesis | SuperCollider (scsynth) |
| Visual | Music-synced visuals | Hydra or Pyxel |

BPM clock is held by SuperCollider's `TempoClock`. Python only sends parameter updates over OSC; timing accuracy is delegated to SuperCollider.

---

## Code Structure → Music Parameter Mapping

| Code feature | Music parameter |
| :--- | :--- |
| Max nesting depth | Filter Cutoff (200–4000 Hz) |
| Control-flow count (if/for/while) | LFO rate (0.1–5.0 Hz) |
| Function definition count | Polyphony voice count (1–4) |
| Comment ratio | Reverb depth (0.0–0.8) |
| `dj.volume` | Amplitude (0.0–1.0) |
| `dj.cutoff` / `dj.reverb` | Direct filter/reverb override |
| `dj.eq` / `dj.low` / `dj.mid` / `dj.high` | Simple 3-band EQ |

---

## Installation

**Requirements**

- Python 3.10 or later
- SuperCollider (with scsynth available)

```bash
pip install 'pycodedj[watch]'
```

The `[watch]` extra enables the `pycodedj watch` command.

Development install:

```bash
git clone https://github.com/kanekoyuichi/pycodedj
cd pycodedj
pip install -e ".[dev]"
```

---

## Quick Start

**1. Boot SuperCollider and load the synths**

Open `sc/synths.scd` in the SuperCollider IDE. Press Ctrl+A (Cmd+A on Mac) to select all, then Ctrl+Enter (Cmd+Enter on Mac) to run. When the Post window shows this, you're ready:

```
PyCodeDJ synths loaded. Ready. OSC port: 57120
```

**2. Write a live-coding file**

```python
from pycodedj import dj, loop

# Code-structure mode: the shape of your code maps to sound
@loop(interval=2.0)
def bass():
    dj.volume = 0.4
    for i in range(8):
        if i % 2 == 0:
            pass

# Pattern mode: specify rhythm and pitch explicitly
@loop(synth="kick_floor", beat=0.25)
def kick():
    dj.volume = 0.8
    dj.pattern = "x . x ."

@loop(synth="lead_acid", root="A3", scale="minor", beat=0.25)
def melody():
    dj.volume = 0.3
    dj.pattern = "0 . 3 . 5 ."

# Comments create space (reverb)
@loop(interval=4.0)
def pad():
    dj.volume = 0.1
    # ambient space
    # silence is music
    pass
```

**3. Start watch mode**

```bash
pycodedj watch demo.py
```

From here, just write code and save. Every save re-evaluates all loops.

**4. Emergency stop**

```bash
pycodedj panic
```

**5. Stop one loop**

```bash
pycodedj stop bass
```

**6. Mute / unmute**

```bash
pycodedj mute bass
pycodedj unmute bass
```

---

## Using dj.pattern

`dj.pattern` lets you specify rhythm and pitch explicitly.

```python
from pycodedj import dj, loop

# Trigger pattern (x = hit, . = rest)
@loop(synth="kick_floor", beat=0.25)
def kick():
    dj.volume = 0.8
    dj.pattern = "x . x ."

# Pitch pattern (integer = scale degree)
@loop(synth="bass_acid", root="A1", scale="minor", beat=0.25)
def bass():
    dj.volume = 0.35
    dj.pattern = "0 . 3 . 5 ."

# Chords and ties
@loop(synth="note", root="A1", scale="minor", beat=0.25)
def chord():
    dj.volume = 0.25
    dj.pattern = "0 . [0 3] ~ 5 . 3 ."
    # [0 3] = two-note chord, ~ = sustain the previous note one more step
```

Token reference:

| Token | Meaning |
| :--- | :--- |
| `x` | Trigger (plays root note) |
| `.` | Rest (silence) |
| `0`, `1`, `2` … | Scale degree (pitch) |
| `[0 3]` | Chord (multiple degrees simultaneously) |
| `~` | Tie (extends the previous note/chord by one step) |

`@loop` arguments for pattern mode:

| Argument | Description |
| :--- | :--- |
| `synth=` | Synth name to use |
| `root=` | Root note (e.g. `"A3"`, `"C4"`) |
| `scale=` | Scale name (e.g. `"minor"`, `"major"`, `"pentatonicMinor"`) |
| `beat=` | Step length in seconds. `0.25` = sixteenth note at 60 BPM |

---

## Example Files

| File | Contents |
| :--- | :--- |
| `examples/demo.py` | Intro demo: bass / melody / pad |
| `examples/club_set.py` | Sub-heavy club set: 11 loops with kick, rumble, sub, acid, hats, and room noise |
| `examples/sound_showcase.py` | All 60 synths — evaluate one at a time to audition |

---

## OSC Address Reference

| Address | Type | Parameter |
| :--- | :--- | :--- |
| `/pycodedj/loop/<name>/params` | int, float, float, float, float | `voice_count`, `cutoff`, `lfo_rate`, `reverb`, `amp` |
| `/pycodedj/loop/<name>/pattern` | int, str, float, str, int… | Pattern data |
| `/pycodedj/loop/<name>/pattern_stop` | — | Stop pattern |
| `/pycodedj/loop/<name>/amp` | float | Amplitude (compatibility) |

---

## Requirements

- **Recommended OS:** macOS (low-latency Core Audio) or Linux (Raspberry Pi 5, etc.)
- **Python:** 3.10 or later
- **SuperCollider:** 3.12 or later

---

## Roadmap

- [x] Python → SuperCollider OSC prototype
- [x] Hot-reload live loop implementation (`pycodedj watch`)
- [x] Sprint 1: Live stability (`panic`, SyntaxError recovery, `mute`/`solo`, `status`)
- [x] Sprint 2: Music DSL (`dj.pattern`, `@loop` parameter expansion: `synth`, `root`, `scale`, `beat`)
- [ ] Sprint 3: Sound design and playability (SynthDef cleanup, `bpm`, `list-synths`, `sample()`)
- [ ] Sprint 4: Hydra visualiser integration

---

## License

MIT + Commons Clause — free to use, modify, and perform (including paid live performances). Selling or commercially distributing the software itself is not permitted. See [LICENSE](LICENSE) for details.

---

## Support

This project is maintained on a best-effort basis.

Bug reports and suggestions may be submitted through GitHub Issues, but responses and fixes are not guaranteed.
