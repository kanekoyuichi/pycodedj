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
9. [Sound Reference](#9-sound-reference)
10. [Performance ideas](#10-performance-ideas)
11. [Troubleshooting](#11-troubleshooting)
12. [Full command and option reference](#12-full-command-and-option-reference)
13. [Under the hood](#13-under-the-hood)

---

## 1. What is PyCodeDJ?

### In one sentence

**PyCodeDJ is an instrument where writing Python code changes the music in real time.**

Add more `for` loops and the modulation speeds up. Write three functions and you get three-voice polyphony. Fill the file with comments and the reverb deepens. Set `volume=` to control how loud each loop is.

```python
from pycodedj import loop

@loop("main", interval=1.0)
def my_sound(volume=0.4):
    # more comments = more space
    # another line
    # one more
    for i in range(4):   # more for = faster modulation
        if i > 2:        # more if = even faster
            pass
```

Evaluate that code and the terminal prints:

```
[pycodedj] main  cutoff=560Hz  lfo=1.08Hz  reverb=0.43  voices=1  amp=0.40
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

A function decorated with `@loop("bass", ...)` is the **bass loop**. The function name (`bass`, `melody`, `pad`) can be anything — the name sent over OSC is the first argument to `@loop`.

### Step 2: Make a sound

Run this in the terminal:

```bash
pycodedj eval examples/demo.py::bass
```

`eval` is short for evaluate. This command reads the `bass` loop in `examples/demo.py` right now, analyses its code structure, and sends sound parameters to SuperCollider.

On success:

```
[pycodedj] bass  cutoff=418Hz  lfo=1.08Hz  reverb=0.00  voices=1  amp=0.40
```

This is your first live-coded sound. Evaluate melody and pad too:

```bash
pycodedj eval examples/demo.py::melody
pycodedj eval examples/demo.py::pad
```

All three loops are now running independently.

### Step 3: Change the code, change the sound

Open `examples/demo.py` in a text editor and modify the bass block:

**Before:**

```python
@loop("bass", interval=2.0)
def bass(volume=0.4):
    for i in range(8):
        if i % 2 == 0:
            pass
```

**After (deeper nesting):**

```python
@loop("bass", interval=2.0)
def bass(volume=0.4):
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
[pycodedj] bass  cutoff=1200Hz  lfo=2.16Hz  reverb=0.00  voices=1  amp=0.40
```

The cutoff went up and the LFO sped up. To change the volume, change `volume=`:

```python
@loop("bass", interval=2.0)
def bass(volume=0.7):   # louder
    ...
```

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

PyCodeDJ converts the **structure** of your Python code into five musical parameters.

### Mapping table

| What the code sees | Musical parameter | How it sounds |
| :--- | :--- | :--- |
| Block structure depth (`if`/`for` nesting) | Filter brightness (Cutoff) | Deeper = brighter, more open |
| Control-flow count (`if`/`for`/`while` total) | Modulation speed (LFO rate) | More = faster wobble |
| Function count (`def` count) | Polyphony voice count | More = more voices (max 4) |
| Comment ratio (comment lines ÷ total lines) | Spatial width (Reverb depth) | More = more reverb |
| `volume=` argument default value | Amplitude | Direct control. 0.0–1.0 |
| `eq=` / `low=` / `mid=` / `high=` arguments | Simple 3-band EQ | Per-loop tone shaping |

### Examples

#### Filter brightness (nesting depth)

```python
@loop("test", interval=1.0)
def f(volume=0.3):
    # depth 1 → filter minimum (muffled)
    pass
```

```python
@loop("test", interval=1.0)
def f(volume=0.3):
    # depth 4 → filter maximum (bright)
    for i in range(4):
        for j in range(4):
            if i == j:
                pass
```

> Arithmetic expressions like `x = 1 + 2 * (3 + 4)` do **not** count toward nesting depth. Only block structures (`if`, `for`, `while`, `with`, `try`, `def`, etc.) are counted.

#### Modulation speed (control-flow count)

```python
@loop("test", interval=1.0)
def f(volume=0.3):
    # 0 control flows → minimum LFO (slow drift)
    pass
```

```python
@loop("test", interval=1.0)
def f(volume=0.3):
    for i in range(4):   # 1
        if i > 2:        # 2
            while False: # 3
                pass
```

#### Polyphony (function count)

```python
@loop("test", interval=1.0)
def solo(volume=0.3):
    # 1 function → mono
    pass
```

```python
@loop("test", interval=1.0)
def f(volume=0.3):
    # 4 functions → max polyphony
    def voice_a(): pass
    def voice_b(): pass
    def voice_c(): pass
    def voice_d(): pass
```

#### Reverb depth (comment ratio)

```python
@loop("test", interval=1.0)
def f(volume=0.3):
    # no comments → dry sound
    x = 1
    return x
```

```python
@loop("test", interval=1.0)
def f(volume=0.3):
    # lots of comments → deep reverb
    # space
    # space
    # space
    pass
```

#### Volume (volume argument)

```python
@loop("kick", interval=1.0)
def my_kick(volume=0.9):   # loud, floor-shaking
    ...

@loop("shimmer", interval=4.0)
def bg_shimmer(volume=0.05):  # quiet, in the background
    ...
```

#### Simple EQ

Use `eq=` to choose a genre-like EQ preset. Override only the bands you need with `low=`, `mid=`, and `high=`.

```python
@loop("bass_reese", interval=0.5)
def bass(volume=0.45, eq="edm"):
    ...

@loop("hat_engine", interval=0.25)
def hats(volume=0.08, eq="edm", low=0.5, high=1.25):
    ...
```

| `eq` | Character |
| :--- | :--- |
| `"flat"` | No correction |
| `"rock"` / `"pop"` | Slight low/high boost with a small mid cut |
| `"edm"` / `"hiphop"` | Stronger low end and some high lift |
| `"classic"` / `"jazz"` | Flat-oriented |
| `"acoustic"` | Less low end, slightly more upper mids/highs |

---

## 7. Running multiple loops at once

The defining feature of PyCodeDJ is that **multiple loops run independently and simultaneously**.

### The basics

Add `@loop("name", ...)` to as many functions as you like:

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
    # background
    # air
    pass
```

Evaluate each independently:

```bash
pycodedj eval myfile.py::bass
pycodedj eval myfile.py::chord
pycodedj eval myfile.py::texture
```

Or use `watch` and all loops update on every save.

### Stopping a loop

To stop a loop, delete the entire `@loop`-decorated function from the file and save. In watch mode, the loop stops automatically. With `eval`, once the decorated function is gone, the loop is no longer found and SuperCollider fades it out.

---

## 8. Club set example — running club_set.py

`examples/club_set.py` is a four-on-the-floor EDM groove built from 8 loops, each with a deliberately distinct code structure and sonic role.

For the full list of available sounds, see [Chapter 9: Sound Reference](#9-sound-reference).

Loop names such as `@loop("kick_hard", ...)` are interpreted as sound names on the SuperCollider side. For example, `kick_hard` maps to a kick synth and `bass_reese` maps to a bass synth. If you are only changing the Python groove or arrangement, you usually do not need to edit `sc/synths.scd`. Edit SuperCollider only when you want to add a genuinely new sound engine.

### club_set.py loop overview

| Loop name | Role | Code style | Cutoff / LFO |
| :--- | :--- | :--- | :--- |
| `kick_hard` | Four-on-the-floor kick | Single assignment (minimal) | 580 Hz / 0.10 Hz |
| `sub_bass` | Deep sub bass | Simple for loop | 960 Hz / 0.59 Hz |
| `bass_acid` | Acid line | List pattern + double loop + if | 2100 Hz / 2.06 Hz |
| `hat_engine` | 16th-note hi-hat grid | Double for + multi-level if/elif (most complex) | 2860 Hz / 4.51 Hz |
| `clap_snare` | Backbeat 2 & 4 | Double for + if/elif + nested if | 2480 Hz / 2.55 Hz |
| `chord_rave` | Rave chord stabs | Triple for + multi-level if/elif | 2860 Hz / 3.53 Hz |
| `lead_hoover` | Classic hoover lead | Comments + double for + two-level if | 2100 Hz / 2.06 Hz, reverb 0.15 |
| `shimmer_pad` | Depth and atmosphere | Comments only, no code | 580 Hz / 0.10 Hz, reverb 0.60 |

### Getting it running

Start watch and edit the file while it plays. Watch evaluates all loops once at startup, so it should make sound before you save:

```bash
pycodedj watch examples/club_set.py
```

You can also evaluate individual loops:

```bash
pycodedj eval examples/club_set.py::kick_hard
pycodedj eval examples/club_set.py::bass_reese
pycodedj eval examples/club_set.py::chord_rave
```

### Performing with it

**Change the volume:** Change `volume=` and save. The loop's amplitude updates immediately.

```python
@loop("lead_hoover", interval=4.0)
def hoover(volume=0.4):   # push it forward
    ...
```

**Change EQ:** Choose a preset with `eq=`, then adjust only the bands you need with `low=`, `mid=`, and `high=`.

```python
@loop("bass_reese", interval=0.5)
def bass(volume=0.45, eq="edm", low=1.5):
    ...
```

**Change the space:** Add or remove comments in `warehouse_air` or `shimmer_pad` to shift the reverb depth.

```python
@loop("warehouse_air", interval=4.0)
def room_tone(volume=0.06):
    # concrete walls
    # low ceiling
    # crowd warmth
    pass
```

Leave only one comment line and save. The space dries out immediately.

**Change the groove:** Remove the `elif` block from `bass_acid` to flatten the acid squelch into a plain bass. Raise `snare_roll`'s `volume=` to push the build-up forward.

Changing code structure *is* the performance.

---

## 9. Sound Reference

Change the first argument of `@loop` to choose the SuperCollider sound. The Python function name can be anything. To audition sounds individually:

```bash
pycodedj eval examples/sound_showcase.py::bass_acid
pycodedj eval examples/sound_showcase.py::riser_noise
pycodedj eval examples/sound_showcase.py::bell_rave
```

**Kicks**

| Loop name | Sound |
| :--- | :--- |
| `kick_hard` | Hard kick with a strong attack |
| `floor_kick` | Big four-on-the-floor kick |
| `kick_pulse` | Lighter pulse kick |

**Basses**

| Loop name | Sound |
| :--- | :--- |
| `bass_rumble` | Low kick-derived rumble |
| `bass_reese` | Moving Reese-style bass |
| `sub_bass` | Sub bass |
| `bass_acid` | 303-style acid bass with squelch |

**Percussion**

| Loop name | Sound |
| :--- | :--- |
| `hat_engine` | Closed/open hi-hat grid |
| `hat_ride` | Longer ride/open hat |
| `clap_snap` | Sharp clap |
| `clap_snare` | Snare-like clap |
| `tom_drum` | Floor tom with pitch sweep |
| `snare_roll` | Snare roll (lfoRate controls speed) |
| `noise_crash` | Crash cymbal with long tail |

**Chords & Stabs**

| Loop name | Sound |
| :--- | :--- |
| `chord_rave` | Bright rave stab |
| `neon_stab` | Neon-style chord stab |
| `dub_chord` | Dub chord |
| `stab_saw` | Detuned saw chord stab |
| `organ_chord` | Hammond-style drawbar organ |
| `bell_rave` | Inharmonic FM rave bell |

**Leads**

| Loop name | Sound |
| :--- | :--- |
| `acid_lead` | Acid-style lead |
| `lead_hoover` | Hoover-style lead |
| `soft_pluck` | Soft pluck |
| `synth_arp` | Arpeggio synth (fast note sequence) |

**Atmospheric**

| Loop name | Sound |
| :--- | :--- |
| `shimmer_pad` | Deep shimmer pad |
| `warehouse_air` | Warehouse ambience |
| `vox_ahh` | Formant vocal pad |

**FX**

| Loop name | Sound |
| :--- | :--- |
| `fx_impact` | Low impact hit |
| `riser_noise` | Noise riser sweeping up over 8 seconds |
| `glitch_ticks` | Small glitch ticks |

---

## 10. Performance ideas

### Idea A: Grow from simple to complex

Start with empty code and add elements one by one. With watch running, each save is a new sound.

```python
# stage 1: near silence (minimum filter, 1 voice)
@loop("main", interval=1.0)
def f(volume=0.3):
    pass
```

```python
# stage 2: add some movement
@loop("main", interval=1.0)
def f(volume=0.3):
    for i in range(4):
        pass
```

```python
# stage 3: go deeper
@loop("main", interval=1.0)
def f(volume=0.3):
    for i in range(4):
        for j in range(2):
            if i > j:
                pass
```

```python
# stage 4: add voices for the climax
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

### Idea B: Play with contrast

Use two loops to set a busy part against a quiet one.

**Busy bass:**

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

**Quiet pad:**

```python
@loop("pad", interval=4.0)
def space(volume=0.08):
    # silence
    # more silence
    # just space
    pass
```

### Idea C: Perform with comments alone

Keep a single function and vary only the comment count. More comments = deeper reverb. With watch running, each save shifts the space.

```python
@loop("ambient", interval=4.0)
def f(volume=0.15):
    # add and remove lines here to perform
    pass
```

### Idea D: Write code as a story

Sound is determined by code structure, not function names. Name things anything you like — your code can tell a story as it performs.

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

## 11. Troubleshooting

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

The loop name after `::` does not match the first argument of `@loop(...)` in the file. Names are case-sensitive.

```bash
# if the file contains @loop("bass", ...)
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

## 12. Full command and option reference

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

`FILE::LOOP` selects the function decorated with `@loop("LOOP", ...)` inside `FILE`. For example, `examples/demo.py::bass` evaluates the function with `@loop("bass", ...)` in `examples/demo.py`.

`eval` runs once. Use `pycodedj watch` when you want all loops to update automatically every time you save the file.

On success, feedback is written to stdout:

```
[pycodedj] bass  cutoff=418Hz  lfo=1.08Hz  reverb=0.00  voices=1  amp=0.40
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

### Loop syntax

```python
from pycodedj import loop

@loop("loop-name", interval=seconds)
def function_name(volume=amplitude, eq="preset"):
    # function body maps to musical parameters
    ...
```

| Element | Description |
| :--- | :--- |
| `"loop-name"` | Name sent over OSC. Alphanumeric and underscores. e.g. `bass`, `kick_hard` |
| `interval=seconds` | Update interval in seconds. Default: `1.0` |
| `volume=amplitude` | Volume. Float from 0.0 to 1.0. Default: `0.3` |
| `eq="preset"` | Simple EQ. Default: `"flat"` |
| `low=multiplier`, `mid=multiplier`, `high=multiplier` | Manual EQ adjustment. 0.0–2.0. Overrides only the specified preset bands |
| function name | Free to choose. Independent from the loop name |

---

## 13. Under the hood

### Mapping values

| Parameter | Input | Output range | Scale |
| :--- | :--- | :--- | :--- |
| Cutoff | Block depth 0–10 | 200–4000 Hz | Linear |
| LFO rate | Control-flow count 0–10 | 0.1–5.0 Hz | Linear |
| Reverb | Comment ratio 0.0–1.0 | 0.0–0.8 | Linear |
| Voice count | Function count (clamped) | 1–4 | Clamp |
| Amplitude | `volume=` argument | pass-through | — |
| EQ | `eq=` preset + `low/mid/high` | 0.0–2.0 | Preset, manual values are clamped |

### OSC addresses

Address format used to communicate with SuperCollider. Reference these when connecting an external visualiser such as Hydra.

| Address | Type | Values |
| :--- | :--- | :--- |
| `/pycodedj/loop/<name>/params` | int, float, float, float, float | `voice_count`, `cutoff`, `lfo_rate`, `reverb`, `amp` |
| `/pycodedj/loop/<name>/voice_count` | int | 1–4 (compatibility) |
| `/pycodedj/loop/<name>/cutoff` | float | 200–4000 (compatibility) |
| `/pycodedj/loop/<name>/lfo_rate` | float | 0.1–5.0 (compatibility) |
| `/pycodedj/loop/<name>/reverb` | float | 0.0–0.8 (compatibility) |
| `/pycodedj/loop/<name>/amp` | float | 0.0–1.0 (compatibility) |

### Using the Python API directly

You can drive PyCodeDJ from code without the CLI:

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

`eval_block` returns a `MusicParams` on success, or `None` if there was a syntax error or OSC failure.

### Module layout

```
pycodedj/
├── _loop.py          # @loop decorator (no-op at runtime)
├── block_parser.py   # parses @loop decorators via AST to extract loop blocks
├── analyzer.py       # extracts structural features (depth, counts, ratio)
├── mapper.py         # maps features to musical parameters
├── engine.py         # orchestrates the full eval pipeline
├── osc_bridge.py     # sends parameters to SuperCollider over OSC
├── watcher.py        # file watcher (watchdog-based)
└── __main__.py       # CLI entry point
```
