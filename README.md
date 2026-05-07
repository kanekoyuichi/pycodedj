# PyCodeDJ

[日本語版 README はこちら](https://github.com/kanekoyuichi/pycodedj/blob/main/README.ja.md) · [Full Manual (EN)](https://github.com/kanekoyuichi/pycodedj/blob/main/docs/manual.md) · [マニュアル (JA)](https://github.com/kanekoyuichi/pycodedj/blob/main/docs/manual.ja.md)

A live-coding environment that translates Python code structure into music in real time. Every save changes the performance.

---

## Concept

PyCodeDJ connects "writing code" directly to "making sound."

Add more functions and the polyphony widens. Deepen nesting and the filter opens up. Fill in comments and the space grows. The structure of your code is the instrument.

Two things set it apart from existing Python ↔ SuperCollider bridges (sc3nb, supriya):

- **Hot-reload performance** — swap out a loop without stopping it. Saving a file becomes an immediate sound change.
- **Audible code structure** — structural features extracted via AST analysis (depth, branch count, function count, etc.) are automatically mapped to musical parameters.

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

| Code feature | Music parameter | Musical rationale |
| :--- | :--- | :--- |
| Max nesting depth | Filter Cutoff (200–4000 Hz) | Deep structure = complexity = brightness |
| Control-flow count (if/for/while) | LFO rate (0.1–5.0 Hz) | More branches = faster modulation |
| Function definition count | Polyphony voice count (1–4) | Functions = independent voices |
| Comment ratio | Reverb depth (0.0–0.8) | More whitespace = more space |
| `volume=` argument | Amplitude (0.0–1.0) | Direct performer control over loudness |

Tempo (BPM) and root pitch are controlled explicitly by the performer, to prevent the foundation of the piece from shifting on every save.

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
git clone https://github.com/yourname/pycodedj
cd pycodedj
pip install -e ".[dev]"
```

---

## Quick Start

**1. Boot SuperCollider and load the synths**

Open `sc/synths.scd` in the SuperCollider IDE and evaluate it.

**2. Write a live-coding file**

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
    # make space
    # a little more
    pass
```

**3. Evaluate a block**

```bash
pycodedj eval demo.py::bass
```

On success, feedback is printed immediately:

```
[pycodedj] bass  cutoff=418Hz  lfo=1.08Hz  reverb=0.00  voices=1  amp=0.40
```

Other loops keep playing without interruption.

**4. Live-code with watch mode**

Instead of running eval manually, use watch to re-evaluate all loops on every save:

```bash
pycodedj watch demo.py
```

From here, just write code and save.

---

## Example Files

| File | Contents |
| :--- | :--- |
| `examples/demo.py` | Intro demo with bass / melody / pad |
| `examples/club_set.py` | EDM groove (8 loops, kick → acid bass → rave stabs → hoover → shimmer) |
| `examples/sound_showcase.py` | All 30 synths — evaluate one at a time to audition each sound |

---

## Live-Coding Examples

### Deeper nesting opens the filter

```python
from pycodedj import loop

@loop("bass", interval=2.0)
def bass(volume=0.4):
    for i in range(4):       # control flow +1
        for j in range(4):   # depth +1, control flow +1
            if i == j:       # depth +1, control flow +1
                pass
```

### More functions = more polyphony

```python
from pycodedj import loop

@loop("chord", interval=1.0)
def chord(volume=0.2):
    def voice_a(): pass
    def voice_b(): pass
    def voice_c(): pass
    def voice_d(): pass
```

### More comments = more space (reverb)

```python
from pycodedj import loop

@loop("pad", interval=4.0)
def pad(volume=0.15):
    # leave space here
    # a little more
    # silence is music
    pass
```

---

## OSC Address Reference

Addresses used to communicate with SuperCollider.

| Address | Type | Range | Parameter |
| :--- | :--- | :--- | :--- |
| `/pycodedj/loop/<name>/params` | int, float, float, float, float | see parameter order | `voice_count`, `cutoff`, `lfo_rate`, `reverb`, `amp` |
| `/pycodedj/loop/<name>/cutoff` | float | 200–4000 Hz | Filter Cutoff (compatibility) |
| `/pycodedj/loop/<name>/lfo_rate` | float | 0.1–5.0 Hz | LFO rate (compatibility) |
| `/pycodedj/loop/<name>/reverb` | float | 0.0–0.8 | Reverb depth (compatibility) |
| `/pycodedj/loop/<name>/voice_count` | int | 1–4 | Polyphony voice count (compatibility) |
| `/pycodedj/loop/<name>/amp` | float | 0.0–1.0 | Amplitude (compatibility) |

`<name>` is the loop name (e.g. `bass`, `melody`). Each loop has its own address namespace, so multiple loops never overwrite each other's parameters.

External visualisers such as Hydra can receive the same parameters on a separate port.

---

## Requirements

- **Recommended OS:** macOS (low-latency Core Audio) or Linux (Raspberry Pi 5, etc.)
- **Python:** 3.10 or later
- **SuperCollider:** 3.12 or later

---

## Roadmap

- [x] Spec design and mapping design
- [ ] Phase 0: Listening validation of mapping hypotheses
- [x] Phase 1: Python → SuperCollider OSC prototype
- [x] Phase 2: Hot-reload live loop implementation (`pycodedj watch`)
- [ ] Phase 3: Hydra visualiser integration

---

## License

MIT + Commons Clause — free to use, modify, and perform (including paid live performances). Selling or commercially distributing the software itself is not permitted. See [LICENSE](LICENSE) for details.
