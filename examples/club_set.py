# PyCodeDJ club groove — EDM edition
#
# Four-on-the-floor kick · sub bass · acid squelch · rave stabs · hoover
#
# Load sc/synths.scd in SuperCollider, then run:
#   pycodedj watch examples/club_set.py
#
# Code structure → sound (by design):
#
#   foundation  kick_hard + floor_kick + sub_bass
#                 depth=1-2 → cutoff  580-960 Hz  (dark, locked to kick)
#                 cf=0-1    → lfo     0.10-0.59 Hz (static)
#
#   groove      bass_reese + bass_acid
#                 depth=3-4 → cutoff 1340-1720 Hz  (mid)
#                 cf=3-4    → lfo    1.57-2.06 Hz
#
#   rhythm      hat_engine + hat_ride + clap_snare
#                 depth=4-6 → cutoff 1720-2480 Hz  (bright to crisp)
#                 cf=3-9    → lfo    1.57-4.51 Hz
#
#   harmonic    chord_rave + stab_saw
#                 depth=4-6 → cutoff 1720-2480 Hz  (bright)
#                 cf=4-7    → lfo    2.06-3.53 Hz
#
#   lead        lead_hoover
#                 depth=5   → cutoff 2100 Hz
#                 2 comments → reverb 0.13 (air without washing out)
#
#   build       snare_roll
#                 depth=4   → cutoff 1720 Hz
#                 cf=3      → lfo    1.57 Hz  (lfoRate drives roll speed)
#
#   space       shimmer_pad + warehouse_air
#                 depth=1   → cutoff  580 Hz
#                 comments  → reverb 0.50-0.53

from pycodedj import loop


# --- Foundation (depth=1-2: darkest, static, bone-dry) ---

@loop("kick_hard", interval=1.0)
def four_on_floor(volume=0.9):
    hit = "down"
    _ = hit


@loop("floor_kick", interval=1.0)
def kick_body(volume=0.6):
    boom = "punch"
    _ = boom


@loop("sub_bass", interval=1.0)
def sub_layer(volume=0.42):
    for beat in range(4):
        sub = "low"
        _ = sub


# --- Groove (depth=3-4: mid-dark, bass movement and acid squelch) ---

@loop("bass_reese", interval=0.5)
def reese_groove(volume=0.28):
    for step in range(8):
        if step % 4 == 0:
            note = "root"
        elif step % 2 == 0:
            note = "fifth"
        else:
            note = "slide"
        _ = note


@loop("bass_acid", interval=0.5)
def acid_line(volume=0.2):
    for step in range(8):
        if step % 4 == 0:
            note = "root"
        elif step % 2 == 0:
            for accent in range(2):
                note = f"sq{accent}"
                _ = note
        else:
            note = "skip"
        _ = note


# --- Rhythm (depth=4-6: bright, driving grid above groove layer) ---

@loop("hat_engine", interval=0.25)
def closed_hats(volume=0.13):
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


@loop("hat_ride", interval=0.5)
def offbeat_ride(volume=0.08):
    for bar in range(4):
        for beat in range(2):
            if beat == 1:
                ride = "open"
                _ = ride


@loop("clap_snare", interval=1.0)
def backbeat(volume=0.26):
    for bar in range(4):
        for beat in range(4):
            if beat == 1:
                hit = "snap"
            elif beat == 3:
                if bar == 3:
                    hit = "fill"
                else:
                    hit = "heavy"
            else:
                hit = "off"
            _ = hit


# --- Harmonic (depth=4-6: brightest, energy and euphoria) ---

@loop("chord_rave", interval=2.0)
def rave_stabs(volume=0.15):
    for phrase in range(4):
        for voice in range(3):
            for harmonic in range(2):
                if phrase == 0:
                    if voice == 0:
                        chord = "root"
                    elif voice == 1:
                        chord = "fifth"
                    else:
                        chord = "octave"
                elif phrase == 2:
                    chord = "resolve"
                else:
                    chord = "hit"
                _ = chord


@loop("stab_saw", interval=1.0)
def saw_layer(volume=0.16):
    for phrase in range(8):
        for voice in range(3):
            if phrase % 4 == 0:
                stab = "down"
            elif phrase % 2 == 0:
                stab = "up"
            else:
                stab = "tail"
            _ = stab


# --- Lead (depth=5: bright, slight reverb from comments) ---

@loop("lead_hoover", interval=4.0)
def hoover(volume=0.12):
    # classic rave swell
    # builds and drops
    for phrase in range(4):
        for step in range(3):
            if phrase in (0, 2):
                if step == 0:
                    motion = "attack"
                else:
                    motion = "hold"
                _ = motion


# --- Build (snare_roll: lfoRate controls how fast the roll runs) ---

@loop("snare_roll", interval=1.0)
def roll_build(volume=0.18):
    for tick in range(16):
        if tick % 2 == 0:
            for layer in range(2):
                roll = f"r{layer}"
                _ = roll


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
