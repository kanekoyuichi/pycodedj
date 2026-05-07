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
2. [Getting set up](#2-getting-set-up)
3. [Setting up SuperCollider](#3-setting-up-supercollider)
4. [Making your first sound](#4-making-your-first-sound)
5. [Save to reload — watch mode](#5-save-to-reload--watch-mode)
6. [How code maps to sound](#6-how-code-maps-to-sound)
7. [Running multiple loops at once](#7-running-multiple-loops-at-once)
8. [Club set example — running club_set.py](#8-club-set-example--running-club_setpy)
9. [Performance ideas](#9-performance-ideas)
10. [Troubleshooting](#10-troubleshooting)
11. [Full command and option reference](#11-full-command-and-option-reference)
12. [Under the hood](#12-under-the-hood)

---

## 1. What is PyCodeDJ?

### In one sentence

**PyCodeDJ is an instrument where writing Python code changes the music in real time.**

Add more `for` loops and the modulation speeds up. Write three functions and you get three-voice polyphony. Fill the file with comments and the reverb deepens, widening the sonic space.

```python
# @loop main interval=1.0

# more comments = more space
# another line
# one more

def melody():
    for i in range(4):   # more for = faster modulation
        if i > 2:        # more if = even faster
            pass
```

Evaluate that code and the terminal prints:

```
[pycodedj] main  cutoff=560Hz  lfo=1.08Hz  reverb=0.43  voices=1
```

SuperCollider switches to that sound immediately. Other loops keep playing.

### What can I use it for?

- Live-coding performance (playing music while writing code on stage)
- Feeling the structure of your code through sound as you develop
- Adding sonic feedback to programming practice

### Where does the sound come from?

PyCodeDJ itself does not produce sound. **SuperCollider** (a free software audio synthesiser) does. PyCodeDJ is the bridge that analyses your Python code and tells SuperCollider what parameters to use.

```
Python code you write
        |
        | pycodedj eval / watch
        v
  PyCodeDJ analyses the code
  (how deeply is it nested?
   how many functions? etc.)
        |
        | OSC protocol
        v
  SuperCollider produces sound
        |
        v
     speakers
```

You only need a minimal amount of SuperCollider interaction. Nothing complicated is required.

---

## 2. Getting set up

### What you need

- Python 3.10 or later (`python --version` to check)
- SuperCollider 3.12 or later (installation covered in the next section)
- A terminal

### Installing PyCodeDJ

```bash
pip install 'pycodedj[watch]'
```

The `[watch]` extra installs watchdog, which enables the `watch` command. Including it from the start makes live performance much smoother.

Verify the installation:

```bash
pycodedj --help
```

If you see this, you're good:

```
usage: pycodedj [-h] {eval,watch} ...
```

### Installing SuperCollider

Download an installer from the official SuperCollider site (supercollider.github.io).

- macOS: download the `.dmg` and install
- Linux: use your package manager or the official site
- Windows: download the `.exe` installer

After installation, launch the SuperCollider IDE. If the window opens, the installation succeeded.

---

## 3. Setting up SuperCollider

SuperCollider is the audio engine. You set it up once and it stays ready.

### What does SuperCollider do here?

In PyCodeDJ, Python does not generate audio directly. Python analyses your code and sends short OSC messages to SuperCollider.

On the SuperCollider side, you do three things:

1. Boot the audio server
2. Load `sc/synths.scd` to register PyCodeDJ's synths
3. Receive OSC messages from Python and turn them into sound

The SuperCollider IDE has two important areas:

- Code documents: where you type and evaluate code such as `s.boot;` or `{ SinOsc... }.play;`
- Post window: where SuperCollider prints logs, errors, and messages such as `PyCodeDJ synths loaded...`

When this manual says to "evaluate this in SuperCollider", run it in a SuperCollider code document, not in your terminal.

### Step 1: Boot the server

Open the SuperCollider IDE and choose **Server > Boot Server** from the menu.

Or type the following in the code editor and press **Ctrl+Enter** (Cmd+Enter on Mac):

```supercollider
s.boot;
```

When the status bar at the bottom turns green showing `localhost`, the server is running.

If this audio server is not running, Python commands may still succeed, but no sound will come out.

### Step 2: Load the synths

Open `sc/synths.scd` from the PyCodeDJ project folder using **File > Open**. Select everything with **Ctrl+A** (Cmd+A on Mac), then evaluate with **Ctrl+Enter** (Cmd+Enter on Mac).

The Post window on the right should show:

```
PyCodeDJ synths loaded. Ready. OSC port: 57120
```

If this message does not appear, see [Troubleshooting](#10-troubleshooting).

`sc/synths.scd` registers the PyCodeDJ synth definitions and OSC receiver in SuperCollider. Run this file again after restarting SuperCollider.

### Step 3: If you change the audio output

SuperCollider uses the audio output device that is active when the audio server boots. If you change the system output to speakers, headphones, or an audio interface, restart the SuperCollider audio server.

First list the available device names in a SuperCollider IDE code document. Run this in SuperCollider, not in your terminal:

```supercollider
ServerOptions.devices;
```

The device names appear in the Post window. After choosing the output device name, set it explicitly in the same kind of SuperCollider code document:

```supercollider
s.quit;
s.options.outDevice = "output device name here";
s.options.numInputBusChannels = 0;
s.boot;
```

If you do not need audio input, keeping `numInputBusChannels = 0` helps avoid sample-rate mismatches with the input device.

After booting, confirm that SuperCollider itself can make sound:

```supercollider
{ SinOsc.ar(110, 0, 0.03) ! 2 }.play;
```

If you hear sound, re-evaluate `sc/synths.scd` (Ctrl+A → Ctrl+Enter, or Cmd+A → Cmd+Enter on Mac).

### Step 4: Confirm the connection

Back in your terminal, run:

```bash
pycodedj eval examples/demo.py::bass
```

If the terminal prints `[pycodedj] bass ...` and a sound comes from SuperCollider, the connection is working.

Leave SuperCollider running while you work.

---

## 4. Making your first sound

### Step 1: Look at the demo file

Open `examples/demo.py`:

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
# leave space here
# a little more
# silence is music
def pad():
    pass
```

Everything from `# @loop bass` up to (but not including) `# @loop melody` is the **bass block**.

### Step 2: Make a sound

Run this in the terminal:

```bash
pycodedj eval examples/demo.py::bass
```

`eval` is short for evaluate. This command reads the `bass` loop in `examples/demo.py` right now, analyses its code structure, and sends sound parameters to SuperCollider.

On success:

```
[pycodedj] bass  cutoff=418Hz  lfo=1.08Hz  reverb=0.00  voices=1
```

This is your first live-coded sound. The feedback line tells you exactly what sound shape is active right now.

Evaluate melody and pad too:

```bash
pycodedj eval examples/demo.py::melody
pycodedj eval examples/demo.py::pad
```

All three loops are now running independently.

### Step 3: Change the code, change the sound

Open `examples/demo.py` in a text editor and modify the bass block:

**Before:**

```python
# @loop bass interval=2.0
def bass():
    for i in range(8):
        if i % 2 == 0:
            pass
```

**After (deeper nesting):**

```python
# @loop bass interval=2.0
def bass():
    for i in range(8):
        for j in range(4):      # added
            if i % 2 == 0:
                if j > 2:       # added
                    pass
```

Save and evaluate again:

```bash
pycodedj eval examples/demo.py::bass
```

```
[pycodedj] bass  cutoff=1200Hz  lfo=2.16Hz  reverb=0.00  voices=1
```

The cutoff went up and the LFO sped up. Deeper nesting opens the filter; more control flow speeds up the modulation.

---

## 5. Save to reload — watch mode

Running `pycodedj eval` by hand every time gets old fast. The `watch` command evaluates all loops once when it starts, then **automatically re-evaluates all loops every time you save the file**.

### Starting watch

```bash
pycodedj watch examples/demo.py
```

```
[pycodedj] watching demo.py — save to reload (Ctrl+C to stop)
[pycodedj] reloaded demo.py (3 loop(s))
```

You should hear sound immediately after watch starts. From here, just write and save. On every save:

```
[pycodedj] reloaded demo.py (3 loop(s))
```

This is the real live-coding workflow: write → save → hear. Repeat.

### Stopping

Press **Ctrl+C** in the terminal. SuperCollider keeps playing.

### About debounce

Some editors (vim, Emacs, etc.) save by writing a temporary file and then renaming it over the target. PyCodeDJ handles these atomic saves correctly, and also collapses rapid successive events so evaluation only fires once per save action. Use `--debounce` to adjust the wait window (default 0.3 s):

```bash
pycodedj watch demo.py --debounce 0.5
```

---

## 6. How code maps to sound

PyCodeDJ converts the **structure** of your Python code into four musical parameters.

### Mapping table

| What the code sees | Musical parameter | How it sounds |
| :--- | :--- | :--- |
| Block structure depth (`if`/`for` nesting) | Filter brightness (Cutoff) | Deeper = brighter, more open |
| Control-flow count (`if`/`for`/`while` total) | Modulation speed (LFO rate) | More = faster wobble |
| Function count (`def` count) | Polyphony voice count | More = more voices (max 4) |
| Comment ratio (comment lines ÷ total lines) | Spatial width (Reverb depth) | More = more reverb |

### Examples

#### Filter brightness (nesting depth)

```python
# @loop test interval=1.0
# depth 1 → filter minimum (muffled)
def f(): pass
```

```python
# @loop test interval=1.0
# depth 4 → filter maximum (bright)
def f():
    for i in range(4):
        for j in range(4):
            if i == j:
                pass
```

> Arithmetic expressions like `x = 1 + 2 * (3 + 4)` do **not** count toward nesting depth. Only block structures (`if`, `for`, `while`, `with`, `try`, `def`, etc.) are counted.

#### Modulation speed (control-flow count)

```python
# @loop test interval=1.0
# 0 control flows → minimum LFO (slow drift)
def f(): pass
```

```python
# @loop test interval=1.0
# 3 control flows → medium LFO
def f():
    for i in range(4):   # 1
        if i > 2:        # 2
            while False: # 3
                pass
```

#### Polyphony (function count)

```python
# @loop test interval=1.0
# 1 function → mono
def solo(): pass
```

```python
# @loop test interval=1.0
# 4 functions → max polyphony
def voice_a(): pass
def voice_b(): pass
def voice_c(): pass
def voice_d(): pass
```

#### Reverb depth (comment ratio)

```python
# @loop test interval=1.0
# no comments → dry sound
def f():
    x = 1
    return x
```

```python
# @loop test interval=1.0
# lots of comments → deep reverb
# space
# space
# space
def f(): pass
```

---

## 7. Running multiple loops at once

The defining feature of PyCodeDJ is that **multiple loops run independently and simultaneously**.

### The basics

Add `# @loop name` anywhere in the file to create a new loop:

```python
# @loop bass interval=2.0
def bass():
    for i in range(8):
        pass

# @loop chord interval=1.0
def chord_a(): pass
def chord_b(): pass

# @loop texture interval=4.0
# background
# air
def bg(): pass
```

Evaluate each independently:

```bash
pycodedj eval myfile.py::bass
pycodedj eval myfile.py::chord
pycodedj eval myfile.py::texture
```

Or use `watch` and all loops update on every save.

### Stopping a loop

To stop a loop, empty its block (remove the `def`) and re-evaluate:

```python
# @loop bass interval=2.0
# (empty)
```

```bash
pycodedj eval myfile.py::bass
```

---

## 8. Club set example — running club_set.py

`examples/club_set.py` is a focused six-part dancefloor groove. It is not a synth catalogue: it combines kick, sub bass, hats, clap, chord hits, and room ambience.

Loop names such as `# @loop kick_floor interval=1.0` are interpreted as role names on the SuperCollider side. For example, `kick_...` maps to a kick synth, `bass_...` maps to a bass synth, and `hat_...` maps to a hat synth. If you are only changing the Python groove or arrangement, you usually do not need to edit `sc/synths.scd`. Edit SuperCollider only when you want to add a genuinely new sound engine.

### Block overview

| Loop name | Character | Code features |
| :--- | :--- | :--- |
| `kick_floor` | Big four-on-the-floor kick | Low body and a short attack |
| `bass_sub` | Heavy sub bass | Deep `if` nesting, filter wide open |
| `hat_offbeat` | Hi-hat grid | Many `for` + `if`, fast LFO |
| `clap_backbeat` | Clap / snare accent | Backbeat energy |
| `chord_dub` | Dub chord | Reverb-heavy chord hits |
| `fx_air` | Warehouse ambience | Comment-heavy = deep reverb |

### Getting it running

Start watch and edit the file while it plays. Watch evaluates all loops once at startup, so it should make sound before you save:

```bash
pycodedj watch examples/club_set.py
```

You can also evaluate individual loops:

```bash
pycodedj eval examples/club_set.py::kick_floor
pycodedj eval examples/club_set.py::bass_sub
pycodedj eval examples/club_set.py::hat_offbeat
pycodedj eval examples/club_set.py::clap_backbeat
pycodedj eval examples/club_set.py::chord_dub
pycodedj eval examples/club_set.py::fx_air
```

### Performing with it

`fx_air` is a comment-only block. Adding or removing comments changes the reverb depth. The function can still be named `warehouse_air`; the OSC loop name comes from `# @loop fx_air ...`.

```python
# @loop fx_air interval=4.0
# smoke above the kick
# late reflections
# concrete room tail
# crowd heat
# blue strobes
def warehouse_air():
    pass
```

Try leaving only two comment lines and saving. The space dries out immediately.

Remove one function from `chord_dub` and the chord drops from three voices to two:

```python
# @loop chord_dub interval=2.0
def chord_root():
    return "minor"

def chord_fifth():
    return "pressure"

# chord_seventh removed
```

Remove the inner `for pressure in range(3)` loop from `bass_sub`. The filter drops and the bass loses some forward pressure.

Changing code structure *is* the performance.

---

## 9. Performance ideas

### Idea A: Grow from simple to complex

Start with empty code and add elements one by one. With watch running, each save is a new sound.

```python
# stage 1: near silence (minimum filter, 1 voice)
# @loop main interval=1.0
def f(): pass
```

```python
# stage 2: add some movement
# @loop main interval=1.0
def f():
    for i in range(4):
        pass
```

```python
# stage 3: go deeper
# @loop main interval=1.0
def f():
    for i in range(4):
        for j in range(2):
            if i > j:
                pass
```

```python
# stage 4: add voices for the climax
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

### Idea B: Play with contrast

Use two loops to set a busy part against a quiet one.

**Busy bass:**

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

**Quiet pad:**

```python
# @loop pad interval=4.0
# silence
# more silence
# just space
def space(): pass
```

### Idea C: Perform with comments alone

Keep a single function and vary only the comment count. More comments = deeper reverb. With watch running, each save shifts the space.

```python
# @loop ambient interval=4.0
# add and remove lines here to perform
def f(): pass
```

### Idea D: Write code as a story

Sound is determined by code structure, not function names. Name things anything you like — your code can tell a story as it performs.

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

## 10. Troubleshooting

### No sound

First check that SuperCollider can make sound on its own. Open a new empty SuperCollider document and evaluate this one line:

```supercollider
{ SinOsc.ar(440, 0, 0.1) ! 2 }.play;
```

Evaluate with **Ctrl+Enter** (Cmd+Enter on Mac). Stop the sound with **Ctrl+.** (Cmd+. on Mac).

If this does not make sound, the problem is not PyCodeDJ yet. Check the SuperCollider server, system volume, and audio output device.

Next, check that the SuperCollider server is running:

```supercollider
s.boot;
```

Then re-run `sc/synths.scd` (Ctrl+A → Ctrl+Enter, or Cmd+A → Cmd+Enter on Mac). The Post window should show:

```text
PyCodeDJ synths loaded. Ready. OSC port: 57120
```

To confirm the OSC port, evaluate this in SuperCollider:

```supercollider
NetAddr.langPort.postln;
```

If it prints anything other than `57120`, pass that port from Python:

```bash
pycodedj eval examples/demo.py::bass --sc-port printed-port
```

To confirm that the synth definitions are loaded, evaluate this in SuperCollider:

```supercollider
~startLoop.value("bass", 1);
```

If this makes sound, the synth definitions are loaded. Stop the sound with **Ctrl+.** (Cmd+. on Mac).

To confirm OSC receiving inside SuperCollider, evaluate:

```supercollider
NetAddr("127.0.0.1", NetAddr.langPort).sendMsg("/pycodedj/loop/bass/voice_count", 1);
```

If this makes sound, SuperCollider's OSC receiver is working.

Still nothing? Check the connection:

```bash
pycodedj eval examples/demo.py::bass
```

If needed, trace incoming OSC messages in SuperCollider:

```supercollider
OSCFunc.trace(true);
```

Stop tracing with:

```supercollider
OSCFunc.trace(false);
```

### `[pycodedj] OSC error`

SuperCollider is not running or the port is wrong.

1. Confirm the SuperCollider IDE is open and the server is booted
2. Re-evaluate `sc/synths.scd` and confirm the `Ready.` message
3. If the port has been changed from the default (57120), pass `--sc-port`:

```bash
pycodedj eval demo.py::bass --sc-port 57200
```

### eval ran but no feedback appeared

A successful eval always prints `[pycodedj] loop-name  cutoff=...Hz ...`. If nothing appears, check stderr — there may be a syntax error.

### `loop 'xxx' not found`

The loop name after `::` does not match the `# @loop` marker in the file. Names are case-sensitive.

```bash
# if the file contains `# @loop bass`
pycodedj eval demo.py::bass   # OK
pycodedj eval demo.py::Bass   # wrong case
```

### `file not found`

The file path is wrong. Check your current directory or use an absolute path:

```bash
pwd
ls

pycodedj eval /home/user/projects/myfile.py::bass
```

### `pycodedj watch` says watchdog is not installed

```bash
pip install 'pycodedj[watch]'
```

Run this if you installed without the `[watch]` extra the first time.

### Syntax error in a block

```
[pycodedj] syntax error (bass): invalid syntax ...
```

The block with the error keeps its previous sound. Other loops are unaffected. Fix the syntax and evaluate again.

---

## 11. Full command and option reference

### `pycodedj eval`

Evaluates a single loop once and sends parameters to SuperCollider.
`eval` is short for evaluate: it means "apply this loop to the sound now."

```
pycodedj eval FILE::LOOP [--sc-host HOST] [--sc-port PORT]
```

| Argument / option | Description | Default |
| :--- | :--- | :--- |
| `FILE::LOOP` | File path and loop name separated by `::` | — |
| `--sc-host` | SuperCollider host | `127.0.0.1` |
| `--sc-port` | SuperCollider receive port | `57120` |

`FILE::LOOP` selects the `# @loop LOOP` block inside `FILE`. For example, `examples/demo.py::bass` evaluates the `# @loop bass` block in `examples/demo.py`.

`eval` runs once. Use `pycodedj watch` when you want all loops to update automatically every time you save the file.

On success, feedback is written to stdout:

```
[pycodedj] bass  cutoff=418Hz  lfo=1.08Hz  reverb=0.00  voices=1
```

On failure (syntax error or OSC send failure), an error is written to stderr and the exit code is 1.

**Examples:**

```bash
pycodedj eval examples/demo.py::bass
pycodedj eval demo.py::melody --sc-host 192.168.1.10
pycodedj eval demo.py::pad --sc-port 57200
```

### `pycodedj watch`

Watches a file and re-evaluates all loops at startup and on every save. Stop with Ctrl+C.

```
pycodedj watch FILE [--sc-host HOST] [--sc-port PORT] [--debounce SECS]
```

| Argument / option | Description | Default |
| :--- | :--- | :--- |
| `FILE` | File to watch | — |
| `--sc-host` | SuperCollider host | `127.0.0.1` |
| `--sc-port` | SuperCollider receive port | `57120` |
| `--debounce` | Window to collapse rapid save events (seconds) | `0.3` |

**Examples:**

```bash
pycodedj watch examples/demo.py
pycodedj watch club_set.py --debounce 0.5
pycodedj watch myfile.py --sc-host 192.168.1.10
```

### Block marker syntax

```
# @loop <name> [interval=seconds]
```

| Element | Description |
| :--- | :--- |
| `<name>` | Alphanumeric characters and underscores. e.g. `bass`, `my_loop_1` |
| `interval=seconds` | Optional. Parsed and stored; not yet sent over OSC (reserved for future use) |

---

## 12. Under the hood

### Mapping values

| Parameter | Input | Output range | Scale |
| :--- | :--- | :--- | :--- |
| Cutoff | Block depth 0–10 | 200–4000 Hz | Linear |
| LFO rate | Control-flow count 0–10 | 0.1–5.0 Hz | Linear |
| Reverb | Comment ratio 0.0–1.0 | 0.0–0.8 | Linear |
| Voice count | Function count (clamped) | 1–4 | Clamp |

### OSC addresses

Address format used to communicate with SuperCollider. Reference these when connecting an external visualiser such as Hydra.

| Address | Type | Range |
| :--- | :--- | :--- |
| `/pycodedj/loop/<name>/params` | int, float, float, float | `voice_count`, `cutoff`, `lfo_rate`, `reverb` |
| `/pycodedj/loop/<name>/voice_count` | int | 1–4 (compatibility) |
| `/pycodedj/loop/<name>/cutoff` | float | 200–4000 (compatibility) |
| `/pycodedj/loop/<name>/lfo_rate` | float | 0.1–5.0 (compatibility) |
| `/pycodedj/loop/<name>/reverb` | float | 0.0–0.8 (compatibility) |

### Using the Python API directly

You can drive PyCodeDJ from code without the CLI:

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

`eval_block` returns a `MusicParams` on success, or `None` if there was a syntax error or OSC failure.

### Module layout

```
pycodedj/
├── block_parser.py   # splits source into @loop blocks
├── analyzer.py       # extracts structural features (depth, counts, ratio)
├── mapper.py         # maps features to musical parameters
├── engine.py         # orchestrates the full eval pipeline
├── osc_bridge.py     # sends parameters to SuperCollider over OSC
├── watcher.py        # file watcher (watchdog-based)
└── __main__.py       # CLI entry point
```
