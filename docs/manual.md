# PyCodeDJ Manual

[日本語版マニュアルはこちら](https://github.com/kanekoyuichi/pycodedj/blob/main/docs/manual.ja.md)

> Write Python code. Hear it change in real time.

---

## Before you start

Anyone who has written a program can try this. No music theory required. It's fine if you've never heard of SuperCollider. Follow this manual from the top and you'll end up with **sound coming out of Python code you wrote yourself**.

Estimated time: 20–30 minutes including setup.

---

## Table of contents

1. [What is PyCodeDJ?](#1-what-is-pycodedj)
2. [Installation](#2-installation)
3. [Setting up SuperCollider](#3-setting-up-supercollider)
4. [Making your first sound](#4-making-your-first-sound)
5. [Watch mode — save to reload](#5-watch-mode--save-to-reload)
6. [How code structure maps to sound](#6-how-code-structure-maps-to-sound)
7. [pattern() — specify rhythm and pitch](#7-pattern--specify-rhythm-and-pitch)
8. [Running multiple loops](#8-running-multiple-loops)
9. [Sound Reference](#9-sound-reference)
10. [Performance ideas](#10-performance-ideas)
11. [Troubleshooting](#11-troubleshooting)
12. [Full command and option reference](#12-full-command-and-option-reference)
13. [Under the hood](#13-under-the-hood)

---

## 1. What is PyCodeDJ?

### In one sentence

**PyCodeDJ is an instrument where writing Python code changes the music in real time.**

Add more `for` loops and the modulation speeds up. Write three functions and you get three-voice polyphony. Fill the file with comments and the reverb deepens. Write `pattern("x . x .")` and that rhythm plays. Write `pattern("0 . 3 . 5 .")` and those pitches ring out.

```python
from pycodedj import loop, pattern

# Code structure controls the sound
@loop("bass", interval=2.0)
def bass_line(volume=0.4):
    for i in range(8):
        if i % 2 == 0:
            pass

# pattern() specifies rhythm and pitch explicitly
@loop("kick", synth="floor_kick", dur=0.25)
def kick_drum():
    pattern("x . x .")

@loop("melody", synth="acid_lead", root="A3", scale="minor", dur=0.25)
def melody_line():
    pattern("0 . 3 . 5 . 7 .")
```

Save this file and the sound changes instantly. No extra configuration needed.

### What can you do with it?

- **Live-coding performance** — perform music in front of an audience by writing code
- **Sonic feedback while coding** — feel the structure of what you write, in real time
- **Programming education** — immediate auditory feedback for every code change

### Where does the sound come from?

PyCodeDJ itself does not produce sound. **SuperCollider** (a free software audio synthesizer) does. PyCodeDJ is the bridge — it analyzes your Python code and sends parameters to SuperCollider over OSC.

```
You write Python code and save
         |
         v
   PyCodeDJ analyzes the code
   (nesting depth, function count,
     comment ratio, pattern() content…)
         |
         | OSC messages
         v
   SuperCollider plays the sound
         |
         v
      Speakers
```

You only interact with SuperCollider once at the start. After that, it stays in the background.

---

## 2. Installation

### Requirements

- **Python 3.10 or later** — check with `python --version` or `python3 --version`
- **SuperCollider 3.12 or later** — instructions in the next section

### Install PyCodeDJ

```bash
pip install 'pycodedj[watch]'
```

The `[watch]` extra enables file watching so you can use the `watch` command. Install it from the start — it makes live-coding much smoother.

Verify the installation:

```bash
pycodedj --help
```

You should see:

```
usage: pycodedj [-h] {eval,watch,panic,mute,unmute,solo,unsolo,status} ...
```

### Development install

```bash
git clone https://github.com/kanekoyuichi/pycodedj
cd pycodedj
pip install -e ".[dev]"
```

---

## 3. Setting up SuperCollider

SuperCollider handles all audio output. You only need to configure it once.

### Install SuperCollider

Download from the official site ([supercollider.github.io](https://supercollider.github.io)):

- **macOS:** Download the `.dmg` and install
- **Linux:** Use your package manager or the official site (`sudo apt install supercollider` on Ubuntu)
- **Windows:** Download the `.exe` installer

After installation, launch **SuperCollider IDE**. If the window opens, you're good.

### The SuperCollider IDE

There are two main areas:

- **Code area (top):** Where you type and run SuperCollider code like `s.boot;`
- **Post window (right or bottom):** Where output, logs, and errors appear

When this manual says "run in SuperCollider," it means the code area in SuperCollider IDE — not your terminal.

### Step 1: Boot the server

In the SuperCollider code area, type this and press **Ctrl+Enter** (Mac: **Cmd+Enter**):

```supercollider
s.boot;
```

The indicator at the bottom turns green when the server is running.

> **Tip:** You can also use the menu: **Server > Boot Server**.

### Step 2: Load the synths

Open `sc/synths.scd` from the PyCodeDJ project folder using **File > Open**.

Press **Ctrl+A** (Mac: **Cmd+A**) to select all, then **Ctrl+Enter** (Mac: **Cmd+Enter**) to run.

When the Post window shows this, you're ready:

```
PyCodeDJ synths loaded. Ready. OSC port: 57120
```

If this doesn't appear, see [Troubleshooting](#11-troubleshooting).

> **Note:** After restarting SuperCollider, run `sc/synths.scd` again.

### Step 3: Verify the connection

Back in your terminal, run:

```bash
pycodedj eval examples/demo.py::bass
```

If the terminal shows `[pycodedj] bass ...` and SuperCollider plays a sound, the connection works.

---

## 4. Making your first sound

### Loop file basics

A PyCodeDJ file looks like this:

```python
from pycodedj import loop

@loop("name", interval=seconds)
def function_name(volume=level):
    # The structure of this code maps to sound
    ...
```

The `@loop("name", interval=seconds)` decorator makes a function a "loop":

- `"name"` — the name sent to SuperCollider (letters, numbers, underscores)
- `interval=seconds` — update interval in seconds (default: 1.0)
- `volume=level` — volume from 0.0 to 1.0 (default: 0.3)

### Try the demo file

Open `examples/demo.py`:

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
    # leave space here
    # a little more
    # silence is music
    pass
```

Evaluate the `bass` loop:

```bash
pycodedj eval examples/demo.py::bass
```

On success:

```
[pycodedj] bass  cutoff=418Hz  lfo=1.08Hz  reverb=0.00  voices=1  amp=0.40
```

Now evaluate `melody` and `pad`:

```bash
pycodedj eval examples/demo.py::melody
pycodedj eval examples/demo.py::pad
```

All three loops are playing simultaneously, independently.

### Change the code, change the sound

Open `examples/demo.py` in an editor and deepen the nesting in the `bass` block:

**Before:**
```python
@loop("bass", interval=2.0)
def bass(volume=0.4):
    for i in range(8):
        if i % 2 == 0:
            pass
```

**After:**
```python
@loop("bass", interval=2.0)
def bass(volume=0.4):
    for i in range(8):
        for j in range(4):      # added
            if i % 2 == 0:
                if j > 2:       # added
                    pass
```

Save, then re-evaluate:

```bash
pycodedj eval examples/demo.py::bass
```

```
[pycodedj] bass  cutoff=1200Hz  lfo=2.16Hz  reverb=0.00  voices=1  amp=0.40
```

The filter opened up and the modulation got faster. Deeper nesting = brighter sound.

---

## 5. Watch mode — save to reload

Running `pycodedj eval` manually each time gets tedious. The `watch` command evaluates all loops at startup and then **re-evaluates automatically on every save**.

### Start watching

```bash
pycodedj watch examples/demo.py
```

```
[pycodedj] watching demo.py — save to reload (Ctrl+C to stop)
[pycodedj] reloaded demo.py (3 loop(s))
```

All loops play immediately. From here, just write code and save. Every save shows:

```
[pycodedj] reloaded demo.py (3 loop(s))
```

**Write code → Save → Sound changes.** That's the live-coding workflow.

### Stop watching

Press **Ctrl+C**. The SuperCollider sound keeps playing. Use `pycodedj panic` to stop all sound.

### Syntax errors

If you save with a syntax error, **only that loop stays unchanged**. The rest keep playing. The error appears in the terminal:

```
[pycodedj] syntax error (bass): invalid syntax (demo.py, line 7)
```

Fix the syntax and save to recover automatically.

---

## 6. How code structure maps to sound

PyCodeDJ reads the **shape** of your code — not what it computes — and maps it to five musical parameters.

### Mapping table

| What PyCodeDJ reads | Musical parameter | Effect |
| :--- | :--- | :--- |
| Block nesting depth (`if` / `for` nesting) | Filter Cutoff (200–4000 Hz) | Deeper = brighter |
| Control-flow count (`if` / `for` / `while`) | LFO rate (0.1–5.0 Hz) | More = faster modulation |
| Function count (`def`) | Polyphony voices (1–4) | More = richer sound |
| Comment ratio (comment lines ÷ total lines) | Reverb depth (0.0–0.8) | More = more space |
| `volume=` default value | Amplitude (0.0–1.0) | Direct control |
| `eq=` / `low=` / `mid=` / `high=` arguments | 3-band EQ | Per-loop tone shaping |

> **Note:** Arithmetic expressions like `x = 1 + 2 * (3 + 4)` are not counted. Only block-level structure (`if`, `for`, `while`, `def`) matters.

### Examples

#### Filter brightness (nesting depth)

```python
# Nesting depth 0 → filter minimum (dark, muffled sound)
@loop("dark", interval=1.0)
def f(volume=0.3):
    pass
```

```python
# Nesting depth 4 → filter maximum (bright, open sound)
@loop("bright", interval=1.0)
def f(volume=0.3):
    for i in range(4):
        for j in range(4):
            if i == j:
                pass
```

#### Modulation speed (control-flow count)

```python
# 0 control-flow statements → minimal modulation (steady)
@loop("still", interval=1.0)
def f(volume=0.3):
    pass
```

```python
# 3 control-flow statements → fast modulation
@loop("busy", interval=1.0)
def f(volume=0.3):
    for i in range(4):     # 1
        if i > 2:          # 2
            while False:   # 3
                pass
```

#### Polyphony (function count)

```python
# 1 function → mono (solo)
@loop("solo", interval=1.0)
def f(volume=0.3):
    pass
```

```python
# 4 functions → 4-voice polyphony (maximum)
@loop("choir", interval=1.0)
def f(volume=0.3):
    def voice_a(): pass
    def voice_b(): pass
    def voice_c(): pass
    def voice_d(): pass
```

#### Space / reverb (comment ratio)

```python
# No comments → dry sound
@loop("dry", interval=1.0)
def f(volume=0.3):
    x = 1
    return x
```

```python
# Many comments → deep reverb
@loop("spacious", interval=1.0)
def f(volume=0.3):
    # space
    # more space
    # silence is music
    pass
```

#### EQ

```python
@loop("bass_reese", interval=0.5)
def bass(volume=0.45, eq="edm"):
    ...

@loop("hat_engine", interval=0.25)
def hats(volume=0.08, eq="edm", low=0.5, high=1.25):
    ...
```

| `eq=` preset | Character |
| :--- | :--- |
| `"flat"` | No adjustment (default) |
| `"rock"` / `"pop"` | Slight boost in lows and highs, slight dip in mids |
| `"edm"` / `"hiphop"` | Strong low boost, slight high boost |
| `"classic"` / `"jazz"` | Flat-leaning |
| `"acoustic"` | Restrained lows, slight mid-high lift |

---

## 7. pattern() — specify rhythm and pitch

Beyond code-structure mapping, you can specify rhythm and pitch **explicitly** using `pattern()`.

### The basics

```python
from pycodedj import loop, pattern

@loop("kick", synth="floor_kick", dur=0.25)
def kick_drum():
    pattern("x . x .")
```

The string passed to `pattern()` describes a sequence of steps:

| Token | Meaning |
| :--- | :--- |
| `x` | Trigger: play the sound here |
| `.` | Rest: silence |
| `0`, `1`, `2` … | Play the sound at this scale degree |

Tokens are separated by spaces. `"x . x ."` is a 4-step pattern.

### @loop arguments for pattern mode

| Argument | Description | Example |
| :--- | :--- | :--- |
| `synth=` | Synth name | `synth="floor_kick"` |
| `root=` | Root note | `root="A3"`, `root="C4"` |
| `scale=` | Scale name | `scale="minor"`, `scale="major"` |
| `dur=` | Step length in seconds | `dur=0.25` (sixteenth note) |

> `volume=`, `eq=`, and `interval=` still work alongside pattern arguments.

### Trigger patterns — x and . only

When you only want **rhythm** without specific pitches, use `x` and `.`:

```python
from pycodedj import loop, pattern

@loop("kick", synth="floor_kick", dur=0.25)
def kick():
    pattern("x . x .")           # 4 steps

@loop("hat", synth="hat_engine", dur=0.25)
def hat():
    pattern("x x x x x x x x")  # 8 steps (16th-note grid)

@loop("snare", synth="clap_snare", dur=0.25)
def snare():
    pattern(". . x . . . x .")   # backbeat (beats 2 and 4)
```

### Pitch patterns — scale degrees

Use non-negative integers to specify **pitch** as a scale degree:

```python
@loop("melody", synth="acid_lead", root="A3", scale="minor", dur=0.25)
def melody():
    pattern("0 . 3 . 5 . 7 .")
```

With `scale="minor"` and `root="A3"`, the degrees map like this:

| Degree | A natural minor |
| :--- | :--- |
| 0 | A3 |
| 1 | B3 |
| 2 | C4 |
| 3 | D4 |
| 4 | E4 |
| 5 | F4 |
| 6 | G4 |
| 7 | A4 (one octave up) |

> Degrees above 6 automatically wrap up by an octave. `7` = one octave above `0`, `14` = two octaves above `0`.

### Available scales

Any scale from SuperCollider's Scale library works. Common ones:

| `scale=` value | Scale |
| :--- | :--- |
| `"major"` | Major |
| `"minor"` | Natural minor |
| `"chromatic"` | Chromatic |
| `"dorian"` | Dorian |
| `"phrygian"` | Phrygian |
| `"lydian"` | Lydian |
| `"mixolydian"` | Mixolydian |
| `"pentatonicMajor"` | Major pentatonic |
| `"pentatonicMinor"` | Minor pentatonic |

### Mixing x and degrees

You can mix trigger tokens and degrees in the same pattern. `x` plays at the root note.

```python
@loop("bass", synth="acid_lead", root="C3", scale="minor", dur=0.25)
def bass():
    pattern("0 . x . 3 . x .")
    # 0→C3, rest, x→C3, rest, 3→Eb3, rest, x→C3, rest
```

### Root note notation

| Notation | Note |
| :--- | :--- |
| `"C4"` | Middle C |
| `"A3"` | A3 |
| `"Bb2"` | B♭2 |
| `"F#3"` | F♯3 (also writable as `"Fs3"`) |
| `"C1"` | Low C |

### Full example: kick, bass, and melody

```python
from pycodedj import loop, pattern

@loop("kick", synth="floor_kick", dur=0.25)
def kick():
    pattern("x . . . x . . .")

@loop("bass", synth="bass_acid", root="A1", scale="minor", dur=0.25)
def bass():
    pattern("0 . 0 . 3 . 5 .")

@loop("melody", synth="acid_lead", root="A3", scale="minor", dur=0.5)
def melody():
    pattern("0 3 5 7")

@loop("pad", interval=4.0)
def pad(volume=0.06):
    # ambient background
    # let the code breathe
    pass
```

### pattern() vs code-structure mapping

| | Code-structure mapping | pattern() |
| :--- | :--- | :--- |
| Rhythm | Generated from code structure | You specify |
| Pitch | Generated from code structure | You specify (or omit) |
| Use when | You want the sound to reflect the code's shape | You want precise rhythm and melody |

Both styles can coexist in the same file.

---

## 8. Running multiple loops

The key feature of PyCodeDJ is that **multiple loops run independently**. Updating one loop doesn't interrupt the others.

### Basic setup

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
    # ambient space
    # breathe
    pass
```

Start watching and each save updates only the changed loops:

```bash
pycodedj watch myfile.py
```

### Live controls

**Mute and unmute**

```bash
pycodedj mute bass        # silence without stopping
pycodedj unmute bass      # restore volume
```

**Emergency stop**

```bash
pycodedj panic            # stop everything immediately
```

**Check loop status**

```bash
pycodedj status
```

```
Loop         State    Amp    Cutoff
kick         playing  0.30   —
bass         playing  0.40   1340Hz
pad          muted    0.08   200Hz
```

### Removing a loop

Delete the `@loop` block (decorator + function) and save. In watch mode, the loop stops automatically.

---

## 9. Sound Reference

The first argument to `@loop` (the loop name) selects the synth on the SuperCollider side.

To audition all 30 synths one at a time, use `examples/sound_showcase.py`:

```bash
pycodedj eval examples/sound_showcase.py::floor_kick
pycodedj eval examples/sound_showcase.py::bass_acid
pycodedj eval examples/sound_showcase.py::acid_lead
```

The same names work with the `synth=` argument in pattern mode.

### Kick

| Name | Sound |
| :--- | :--- |
| `kick_hard` | Hard, punchy kick |
| `floor_kick` | Full four-on-the-floor kick |
| `kick_pulse` | Light pulse kick |

### Bass

| Name | Sound |
| :--- | :--- |
| `bass_rumble` | Deep low rumble |
| `bass_reese` | Reese-style wobble bass |
| `sub_bass` | Sub bass |
| `bass_acid` | 303-style acid bass |

### Percussion

| Name | Sound |
| :--- | :--- |
| `hat_engine` | Closed/open hi-hat grid |
| `hat_ride` | Long ride/open hat |
| `clap_snap` | Sharp clap |
| `clap_snare` | Snare-like clap |
| `tom_drum` | Floor tom (pitch sweep) |
| `snare_roll` | Snare roll |
| `noise_crash` | Crash cymbal (long tail) |

### Chords / Stabs

| Name | Sound |
| :--- | :--- |
| `chord_rave` | Bright rave stab |
| `neon_stab` | Neon-style stab chord |
| `dub_chord` | Dub chord |
| `stab_saw` | Detuned saw chord stab |
| `organ_chord` | Hammond-style organ chord |
| `bell_rave` | FM rave bell |

### Lead / Melody

| Name | Sound |
| :--- | :--- |
| `acid_lead` | Acid-style lead |
| `lead_hoover` | Hoover-style lead |
| `soft_pluck` | Soft pluck |
| `synth_arp` | Arpeggio synth |
| `note` | General-purpose note synth (for pitch patterns) |

### Atmosphere

| Name | Sound |
| :--- | :--- |
| `shimmer_pad` | Deep shimmer pad |
| `warehouse_air` | Industrial air texture |
| `vox_ahh` | Formant vocal pad |

### FX

| Name | Sound |
| :--- | :--- |
| `fx_impact` | Low impact hit |
| `riser_noise` | Noise riser (8-second upward sweep) |
| `glitch_ticks` | Fine glitch ticks |

---

## 10. Performance ideas

### Idea A: Grow from silence

Start with empty code and add elements one save at a time. Each save is an audible step.

```python
# Stage 1: minimum (dark filter, mono)
@loop("main", interval=1.0)
def f(volume=0.3):
    pass
```

```python
# Stage 2: add movement
@loop("main", interval=1.0)
def f(volume=0.3):
    for i in range(4):
        pass
```

```python
# Stage 3: open the filter with deeper nesting
@loop("main", interval=1.0)
def f(volume=0.3):
    for i in range(4):
        for j in range(2):
            if i > j:
                pass
```

```python
# Stage 4: climax — maximum polyphony
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

### Idea B: Live sequence with pattern()

Change the pattern string on each save.

```python
from pycodedj import loop, pattern

@loop("kick", synth="floor_kick", dur=0.25)
def kick():
    pattern("x . x .")     # ← change this and save to change the rhythm

@loop("bass", synth="bass_acid", root="A1", scale="minor", dur=0.25)
def bass():
    pattern("0 . 0 . 3 .") # ← change degrees to change the harmony
```

### Idea C: Contrast quiet and loud

Pair a busy loop with a spacious one.

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
    # silence
    # more silence
    # just space
    pass
```

### Idea D: Perform with comments only

Leave one function and change only the comment count. More comments = more reverb.

```python
@loop("ambient", interval=4.0)
def f(volume=0.15):
    # add or remove lines here to change the space
    pass
```

### Idea E: Write a story with function names

Sound comes from code structure, not function names. Name things whatever you like.

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

## 11. Troubleshooting

### No sound

First, check that SuperCollider works on its own. In the SuperCollider code area:

```supercollider
{ SinOsc.ar(440, 0, 0.1) ! 2 }.play;
```

**Ctrl+Enter** to run, **Ctrl+.** (Mac: **Cmd+.**) to stop.

If this produces no sound, the issue is with SuperCollider, not PyCodeDJ. Check your system volume, output device, and audio server.

If it does produce sound, work through these checks:

**1. Is the server booted?**

```supercollider
s.boot;
```

**2. Is `sc/synths.scd` loaded?**

Select all (Ctrl+A) and run (Ctrl+Enter). The Post window should show:

```
PyCodeDJ synths loaded. Ready. OSC port: 57120
```

**3. Is the port number correct?**

Run this in SuperCollider:

```supercollider
NetAddr.langPort.postln;
```

If it shows something other than `57120`, specify it:

```bash
pycodedj eval examples/demo.py::bass --sc-port PORT_NUMBER
```

**4. Trace OSC messages**

```supercollider
OSCFunc.trace(true);
```

Run `pycodedj eval` and check whether messages appear in the Post window. Disable tracing when done:

```supercollider
OSCFunc.trace(false);
```

### `[pycodedj] OSC error`

SuperCollider isn't running or the port number is wrong.

1. Check that SuperCollider IDE is open and the server is booted
2. Run `sc/synths.scd` and confirm `Ready.` in the Post window
3. If the port differs from 57120, use `--sc-port`

### `loop 'xxx' not found`

The loop name after `::` doesn't match the first argument of `@loop(...)`.

```bash
# If the file contains @loop("bass", ...)
pycodedj eval demo.py::bass   # correct
pycodedj eval demo.py::Bass   # wrong (case sensitive)
```

### `file not found`

Check your current directory and use an absolute path if needed.

```bash
pwd    # show current directory
ls     # list files

pycodedj eval /home/user/projects/myfile.py::bass
```

### `pycodedj watch` asks you to install watchdog

```bash
pip install 'pycodedj[watch]'
```

### Output device changed and now there's no sound

SuperCollider uses the output device that was active when the server booted. After changing the device:

```supercollider
ServerOptions.devices;  // list available devices

s.quit;
s.options.outDevice = "Your Device Name";
s.options.numInputBusChannels = 0;
s.boot;
```

Then run `sc/synths.scd` again.

---

## 12. Full command and option reference

### `pycodedj eval`

Evaluate one loop and send parameters to SuperCollider.

```
pycodedj eval FILE::LOOP [--sc-host HOST] [--sc-port PORT]
```

| Argument / option | Description | Default |
| :--- | :--- | :--- |
| `FILE::LOOP` | File path and loop name separated by `::` | — |
| `--sc-host` | SuperCollider host | `127.0.0.1` |
| `--sc-port` | SuperCollider receive port | `57120` |

On success, stdout shows:

```
[pycodedj] bass  cutoff=418Hz  lfo=1.08Hz  reverb=0.00  voices=1  amp=0.40
```

On failure, stderr shows an error and exit code is 1.

```bash
pycodedj eval examples/demo.py::bass
pycodedj eval demo.py::melody --sc-host 192.168.1.10
pycodedj eval demo.py::pad --sc-port 57200
```

### `pycodedj watch`

Watch a file and re-evaluate all loops at startup and on every save. Stop with Ctrl+C.

```
pycodedj watch FILE [--sc-host HOST] [--sc-port PORT] [--debounce SECS]
```

| Argument / option | Description | Default |
| :--- | :--- | :--- |
| `FILE` | File to watch | — |
| `--sc-host` | SuperCollider host | `127.0.0.1` |
| `--sc-port` | SuperCollider receive port | `57120` |
| `--debounce` | Seconds to wait before re-evaluating on rapid saves | `0.3` |

```bash
pycodedj watch examples/demo.py
pycodedj watch club_set.py --debounce 0.5
```

### `pycodedj panic`

Send an immediate stop signal to all active loops.

```
pycodedj panic [--sc-host HOST] [--sc-port PORT]
```

```bash
pycodedj panic
```

### `pycodedj mute`

Silence a loop without stopping it.

```
pycodedj mute NAME [--sc-host HOST] [--sc-port PORT]
```

```bash
pycodedj mute bass
```

### `pycodedj unmute`

Restore a muted loop's volume.

```
pycodedj unmute NAME [--sc-host HOST] [--sc-port PORT]
```

```bash
pycodedj unmute bass
```

### `pycodedj status`

Show the state of all active loops.

```
pycodedj status [--sc-host HOST] [--sc-port PORT]
```

```
Loop         State    Amp    Cutoff
bass         playing  0.40   1340Hz
pad          muted    0.15   200Hz
```

> **Note:** `status` runs in a separate process from `watch` and can only see loops that watch is currently managing.

### Loop syntax summary

```python
from pycodedj import loop, pattern

# Code-structure mode
@loop("name", interval=seconds)
def function_name(volume=level, eq="preset"):
    # code structure maps to sound
    ...

# pattern() mode
@loop("name", synth="synth_name", root="note", scale="scale_name", dur=seconds)
def function_name(volume=level):
    pattern("x . x . 0 . 3 .")
```

| Argument | Description | Default |
| :--- | :--- | :--- |
| `"name"` | Loop name (letters, numbers, underscores) | — |
| `interval=` | Update interval in seconds | `1.0` |
| `volume=` | Volume (0.0–1.0) | `0.3` |
| `eq=` | EQ preset | `"flat"` |
| `low=`, `mid=`, `high=` | Per-band EQ multiplier (0.0–2.0) | preset values |
| `synth=` | Synth name for pattern mode | — |
| `root=` | Root note for pattern mode | `"C4"` |
| `scale=` | Scale name for pattern mode | `"chromatic"` |
| `dur=` | Step length in seconds for pattern mode | `0.25` |

---

## 13. Under the hood

### Mapping numbers

| Parameter | Input | Output range | Scale |
| :--- | :--- | :--- | :--- |
| Cutoff | Block depth 0–10 | 200–4000 Hz | Linear |
| LFO rate | Control-flow count 0–10 | 0.1–5.0 Hz | Linear |
| Reverb | Comment ratio 0.0–1.0 | 0.0–0.8 | Linear |
| Voice count | Function count (clamped) | 1–4 | Clamp |
| Amplitude | `volume=` argument | pass-through | Pass-through |

### OSC address reference

Use these addresses to connect external tools like Hydra.

| Address | Type | Value |
| :--- | :--- | :--- |
| `/pycodedj/loop/<name>/params` | int, float, float, float, float | `voice_count`, `cutoff`, `lfo_rate`, `reverb`, `amp` (in order) |
| `/pycodedj/loop/<name>/pattern` | int, str, float, str, int… | `root_midi`, `scale`, `dur`, `synth`, `step…` |
| `/pycodedj/loop/<name>/pattern_stop` | — | Stop pattern |
| `/pycodedj/loop/<name>/synth` | str | Synth name (empty string to clear) |
| `/pycodedj/loop/<name>/amp` | float | Amplitude (compatibility) |

### Using the Python API directly

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

`eval_block` returns `MusicParams` on success, or `None` on syntax error or OSC failure.

### Module overview

```
pycodedj/
├── _loop.py          # @loop decorator (no-op at runtime)
├── block_parser.py   # AST parser: extracts @loop blocks from source
├── analyzer.py       # Feature extraction: depth, counts, ratios
├── mapper.py         # Maps features to MusicParams
├── pattern.py        # Parses pattern() strings to step lists
├── engine.py         # Evaluation pipeline
├── osc_bridge.py     # OSC communication with SuperCollider
├── watcher.py        # File watcher (watchdog-based)
└── __main__.py       # CLI entry point
```
