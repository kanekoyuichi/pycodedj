# PyCodeDJ club groove.
#
# Load sc/synths.scd in SuperCollider, then run:
#   pycodedj watch examples/club_set.py
#
# Code structure → sound (by design):
#
#   foundation  kick_hard + bass_rumble
#                 depth=1 → cutoff 580 Hz  (dark)
#                 cf=0    → lfo   0.10 Hz  (no movement)
#
#   movement    bass_reese + hat_ride
#                 depth=4 → cutoff 1720 Hz (mid)
#                 cf=3    → lfo   1.57 Hz
#
#   body        clap_snap + clap_snare
#                 depth=4 → cutoff 1720 Hz
#                 cf=5    → lfo   2.55 Hz  (snappier)
#
#   harmonic    chord_rave + neon_stab
#                 depth=6 → cutoff 2480 Hz (bright)
#                 cf=5-6  → lfo   2.55-3.04 Hz
#
#   lead        lead_hoover
#                 depth=5 → cutoff 2100 Hz
#                 reverb  → 0.12 (slight space)
#
#   hats        hat_engine
#                 depth=6 → cutoff 2480 Hz
#                 cf=8    → lfo   4.02 Hz  (fast)
#
#   space       shimmer_pad + warehouse_air
#                 depth=1 → cutoff 580 Hz
#                 reverb  → 0.57-0.60 (lots of room)
#
#   texture     glitch_ticks + fx_impact
#                 depth=4-5, cf=6-8 → fast LFO

from pycodedj import loop


# --- Foundation (depth=1: darkest, no movement, dry) ---

@loop("kick_hard", interval=1.0)
def floor_kick(volume=0.9):
    hit = "down"
    _ = hit


@loop("bass_rumble", interval=1.0)
def sub_pulse(volume=0.36):
    sub = "punch"
    _ = sub


# --- Movement (depth=4: mid-range, moderate LFO) ---

@loop("bass_reese", interval=0.5)
def reese_groove(volume=0.3):
    groove = [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0]
    for step, active in enumerate(groove):
        if active:
            for bend in range(2):
                phrase = f"b{step}_{bend}"
                _ = phrase


@loop("hat_ride", interval=0.5)
def ride_layer(volume=0.09):
    offbeat = [0, 1, 0, 1, 1, 0, 1, 0]
    for bar in range(4):
        for step, on in enumerate(offbeat):
            if on:
                ride = "swing" if bar >= 2 else "tight"
                _ = ride


# --- Body (depth=4: mid, faster LFO than movement) ---

@loop("clap_snap", interval=1.0)
def snap_back(volume=0.2):
    for bar in range(8):
        for beat in range(4):
            if beat in (1, 3):
                snap = "crack"
            elif beat == 0:
                snap = "ghost"
            else:
                snap = "skip"
            _ = snap
            if bar in (3, 7) and beat == 3:
                flam = "flam"
                _ = flam


@loop("clap_snare", interval=1.0)
def heavy_two(volume=0.22):
    for bar in range(8):
        for beat in range(4):
            if beat == 2:
                hit = "heavy"
                _ = hit
            if bar == 7 and beat in (2, 3):
                fill = "fill"
                _ = fill


# --- Harmonic (depth=6: brightest, medium-fast LFO) ---

@loop("chord_rave", interval=2.0)
def rave_stabs(volume=0.14):
    for phrase in range(4):
        for voice in range(3):
            for harmonic in range(2):
                if phrase == 0:
                    if voice == 0:
                        chord = "root"
                    elif voice == 1:
                        chord = "third"
                    else:
                        chord = "fifth"
                elif phrase == 1:
                    chord = "fifth"
                elif phrase == 2:
                    chord = "seventh"
                else:
                    chord = "resolve"
                _ = chord


@loop("neon_stab", interval=2.0)
def stab_layer(volume=0.1):
    for phrase in range(4):
        for beat in range(2):
            if phrase in (1, 3):
                if beat == 0:
                    stab = "hit"
                else:
                    stab = "tail"
                _ = stab


# --- Lead (depth=5: bright, slight reverb from comments) ---

@loop("lead_hoover", interval=4.0)
def hoover(volume=0.12):
    # attack into the drop
    # fade into nothing
    for phrase in range(4):
        for step in range(3):
            if phrase in (0, 2):
                if step == 0:
                    motion = "attack"
                elif step == 1:
                    motion = "hold"
                else:
                    motion = "fade"
                _ = motion


# --- Hats (depth=6: bright, fast LFO — sits above harmonic layer) ---

@loop("hat_engine", interval=0.25)
def closed_hats(volume=0.12):
    for bar in range(2):
        for tick in range(16):
            if tick % 4 == 0:
                if tick == 0:
                    if bar == 0:
                        hat = "anchor_a"
                    else:
                        hat = "anchor_b"
                else:
                    hat = "beat"
            elif tick % 2 == 0:
                hat = "up"
            elif tick in (3, 7, 11, 15):
                if bar == 0:
                    hat = "ghost_a"
                else:
                    hat = "ghost_b"
            else:
                hat = "skip"
            if tick in (6, 14):
                hat = "open"
            _ = hat


# --- Space (depth=1: dark, maximum reverb from comment ratio) ---

@loop("shimmer_pad", interval=8.0)
def shimmer(volume=0.07):
    # wide hall reverb
    # slow harmonic drift
    # always underneath everything
    # never noticed until it stops
    # consonance without definition
    # air between the notes
    pass


@loop("warehouse_air", interval=4.0)
def room_tone(volume=0.06):
    # concrete walls
    # low ceiling pressing down
    # crowd warmth from two hundred bodies
    # sub frequencies bleeding through
    # smoke machine haze
    pass


# --- Texture (depth=4-5, cf=6-8: fast LFO = glitchy modulation) ---

@loop("glitch_ticks", interval=0.5)
def digital_noise(volume=0.05):
    for tick in range(8):
        if tick % 3 == 0:
            if tick == 0:
                glitch = "trigger"
            else:
                glitch = "echo"
        elif tick % 2 == 0:
            if tick in (2, 4):
                glitch = "tick"
            else:
                glitch = "blip"
        elif tick == 5:
            glitch = "stutter"
        else:
            glitch = "skip"
        _ = glitch


@loop("fx_impact", interval=8.0)
def drop_hit(volume=0.18):
    for layer in range(3):
        for sub in range(2):
            if layer == 0:
                hit = "thump"
            elif layer == 1:
                if sub == 0:
                    hit = "noise"
                else:
                    hit = "crack"
            else:
                hit = "tail"
            _ = hit
