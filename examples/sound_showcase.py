# PyCodeDJ — Sound Showcase
#
# Demonstrates every available synth name (60 total).
# Evaluate one loop at a time to hear each sound in isolation:
#
#   pycodedj eval examples/sound_showcase.py::kick_hard
#   pycodedj eval examples/sound_showcase.py::bass_acid
#   pycodedj eval examples/sound_showcase.py::fx_riser
#
# Or layer everything at once (heavy but instructive):
#
#   pycodedj watch examples/sound_showcase.py
#
# ─── Index ──────────────────────────────────────────────────────────────────
#
#   Kicks        kick_hard  kick_floor  kick_pulse  kick_soft
#                kick_909  kick_click
#   Basses       bass_rumble  bass_reese  bass_sub  bass_acid
#                bass_pluck  bass_fm  bass_mono  bass_wobble
#   Percussion   hat_engine  hat_ride  clap_snap  clap_snare
#                tom_drum  snare_roll  crash_noise  rim_shot
#                cowbell  perc_blip  shaker_loop  tick_metal  wood_block
#   Chords       chord_rave  stab_neon  chord_dub
#                stab_saw  chord_organ  bell_rave  pad_minor
#                chord_deep  chord_glass  pad_warm  pad_string  pad_choir
#   Leads        lead_acid  lead_hoover  pluck_soft  arp_synth
#                lead_square  lead_fm  lead_chip  lead_saw  lead_whistle
#   Atmospheric  pad_shimmer  air_warehouse  vox_ahh  drone_space
#   FX           fx_drop  fx_riser  fx_glitch  fx_down
#                fx_zap  fx_noise  fx_laser  fx_vinyl

from pycodedj import dj, loop


# ─── Kicks (depth=1: dark, punchy) ──────────────────────────────────────────

@loop(synth="kick_hard", interval=1.0)
def kick_hard():
    dj.volume = 0.85
    hit = "down"
    _ = hit


@loop(synth="kick_floor", interval=1.0)
def kick_floor():
    dj.volume = 0.75
    hit = "floor"
    _ = hit


@loop(synth="kick_pulse", interval=1.0)
def kick_pulse():
    dj.volume = 0.6
    for beat in range(2):
        hit = "pulse"
        _ = hit


@loop(synth="kick_soft", interval=1.0)
def kick_soft():
    dj.volume = 0.5
    hit = "soft"
    _ = hit


@loop(synth="kick_909", interval=1.0)
def kick_909():
    dj.volume = 0.7
    hit = "long"
    _ = hit


@loop(synth="kick_click", interval=1.0)
def kick_click():
    dj.volume = 0.55
    hit = "click"
    _ = hit


# ─── Basses (depth=2-3: mid-dark) ───────────────────────────────────────────

@loop(synth="bass_rumble", interval=1.0)
def bass_rumble():
    dj.volume = 0.35
    sub = "rumble"
    _ = sub


@loop(synth="bass_reese", interval=0.5)
def bass_reese():
    dj.volume = 0.3
    for step in range(4):
        if step % 2 == 0:
            note = "on"
            _ = note


@loop(synth="bass_sub", interval=1.0)
def bass_sub():
    dj.volume = 0.3
    for step in range(4):
        note = "sub"
        _ = note


@loop(synth="bass_acid", interval=0.5)
def bass_acid():
    dj.volume = 0.25
    for step in range(8):
        if step in (0, 3, 5):
            for bend in range(2):
                note = f"acid_{bend}"
                _ = note


@loop(synth="bass_pluck", interval=0.5)
def bass_pluck():
    dj.volume = 0.25
    for step in range(8):
        if step % 2 == 0:
            note = "pluck"
            _ = note


@loop(synth="bass_fm", interval=0.5)
def bass_fm():
    dj.volume = 0.24
    for step in range(8):
        if step in (0, 2, 5):
            note = "fm"
            _ = note


@loop(synth="bass_mono", interval=1.0)
def bass_mono():
    dj.volume = 0.28
    for step in range(4):
        note = "mono"
        _ = note


@loop(synth="bass_wobble", interval=1.0)
def bass_wobble():
    dj.volume = 0.24
    for step in range(4):
        if step in (0, 2):
            note = "wobble"
            _ = note


# ─── Percussion (depth=1-2: crisp and dry) ──────────────────────────────────

@loop(synth="hat_engine", interval=0.25)
def hat_engine():
    dj.volume = 0.12
    for tick in range(8):
        if tick % 2 == 0:
            hat = "closed"
            _ = hat


@loop(synth="hat_ride", interval=0.5)
def hat_ride():
    dj.volume = 0.1
    for step in range(4):
        if step % 2 == 1:
            ride = "on"
            _ = ride


@loop(synth="clap_snap", interval=1.0)
def clap_snap():
    dj.volume = 0.2
    for beat in range(4):
        if beat in (1, 3):
            snap = "crack"
            _ = snap


@loop(synth="clap_snare", interval=1.0)
def clap_snare():
    dj.volume = 0.22
    for beat in range(4):
        if beat == 2:
            hit = "snare"
            _ = hit


@loop(synth="tom_drum", interval=1.0)
def tom_drum():
    dj.volume = 0.25
    for beat in range(4):
        if beat in (2, 3):
            tom = "hit"
            _ = tom


@loop(synth="snare_roll", interval=1.0)
def snare_roll():
    dj.volume = 0.2
    for tick in range(16):
        if tick % 2 == 0:
            for layer in range(2):
                roll = f"r{layer}"
                _ = roll


@loop(synth="crash_noise", interval=4.0)
def crash_noise():
    dj.volume = 0.2
    for layer in range(3):
        crash = "hit"
        _ = crash


@loop(synth="rim_shot", interval=1.0)
def rim_shot():
    dj.volume = 0.16
    for beat in range(4):
        if beat in (1, 3):
            hit = "rim"
            _ = hit


@loop(synth="cowbell", interval=1.0)
def cowbell():
    dj.volume = 0.14
    for beat in range(4):
        if beat in (0, 3):
            hit = "bell"
            _ = hit


@loop(synth="perc_blip", interval=0.5)
def perc_blip():
    dj.volume = 0.12
    for step in range(8):
        if step in (1, 4, 6):
            hit = "blip"
            _ = hit


@loop(synth="shaker_loop", interval=0.25)
def shaker_loop():
    dj.volume = 0.08
    for tick in range(8):
        shake = "grain"
        _ = shake


@loop(synth="tick_metal", interval=0.25)
def tick_metal():
    dj.volume = 0.08
    for tick in range(8):
        if tick % 3 == 0:
            hit = "metal"
            _ = hit


@loop(synth="wood_block", interval=0.5)
def wood_block():
    dj.volume = 0.12
    for step in range(8):
        if step in (0, 3, 7):
            hit = "wood"
            _ = hit


# ─── Chords & Stabs (depth=4-5: bright) ─────────────────────────────────────

@loop(synth="chord_rave", interval=2.0)
def chord_rave():
    dj.volume = 0.14
    for phrase in range(4):
        for voice in range(3):
            if phrase == 0:
                chord = "root"
            else:
                chord = "alt"
            _ = chord


@loop(synth="stab_neon", interval=2.0)
def stab_neon():
    dj.volume = 0.12
    for phrase in range(4):
        for voice in range(2):
            if phrase in (0, 2):
                stab = "hit"
                _ = stab


@loop(synth="chord_dub", interval=2.0)
def chord_dub():
    dj.volume = 0.13
    for phrase in range(4):
        for voice in range(2):
            chord = "dub"
            _ = chord


@loop(synth="stab_saw", interval=1.0)
def stab_saw():
    dj.volume = 0.2
    for phrase in range(4):
        for voice in range(3):
            if phrase % 2 == 0:
                stab = "hit"
                _ = stab


@loop(synth="chord_organ", interval=2.0)
def chord_organ():
    dj.volume = 0.14
    for phrase in range(4):
        for voice in range(2):
            chord = "organ"
            _ = chord


@loop(synth="bell_rave", interval=2.0)
def bell_rave():
    dj.volume = 0.12
    for phrase in range(4):
        for step in range(2):
            if phrase in (0, 2):
                bell = "ring"
                _ = bell


@loop(synth="pad_minor", interval=4.0)
def pad_minor():
    dj.volume = 0.08
    # darker suspended pad
    pass


@loop(synth="chord_deep", interval=2.0)
def chord_deep():
    dj.volume = 0.12
    for phrase in range(4):
        if phrase in (0, 2):
            chord = "deep"
            _ = chord


@loop(synth="chord_glass", interval=2.0)
def chord_glass():
    dj.volume = 0.1
    for phrase in range(4):
        if phrase in (1, 3):
            chord = "glass"
            _ = chord


@loop(synth="pad_warm", interval=8.0)
def pad_warm():
    dj.volume = 0.08
    # slow warm bed
    pass


@loop(synth="pad_string", interval=8.0)
def pad_string():
    dj.volume = 0.08
    # bowed synth layer
    pass


@loop(synth="pad_choir", interval=8.0)
def pad_choir():
    dj.volume = 0.08
    # vowel-like harmonic bed
    pass


# ─── Leads (depth=4-5: bright, melodic) ─────────────────────────────────────

@loop(synth="lead_acid", interval=0.5)
def lead_acid():
    dj.volume = 0.15
    for step in range(8):
        if step % 2 == 0:
            for note in range(2):
                lead = f"a{note}"
                _ = lead


@loop(synth="lead_hoover", interval=4.0)
def lead_hoover():
    dj.volume = 0.12
    for phrase in range(4):
        for step in range(3):
            if phrase in (0, 2):
                motion = "on"
                _ = motion


@loop(synth="pluck_soft", interval=1.0)
def pluck_soft():
    dj.volume = 0.12
    for step in range(6):
        for note in range(2):
            if step % 3 == 0:
                pluck = "hit"
                _ = pluck


@loop(synth="arp_synth", interval=0.5)
def arp_synth():
    dj.volume = 0.14
    for step in range(8):
        for note in range(2):
            if step % 2 == 0:
                arp = f"n{note}"
                _ = arp


@loop(synth="lead_square", interval=0.5)
def lead_square():
    dj.volume = 0.12
    for step in range(8):
        if step in (0, 2, 5):
            lead = "square"
            _ = lead


@loop(synth="lead_fm", interval=0.5)
def lead_fm():
    dj.volume = 0.12
    for step in range(8):
        if step % 2 == 1:
            lead = "fm"
            _ = lead


@loop(synth="lead_chip", interval=0.25)
def lead_chip():
    dj.volume = 0.1
    for step in range(8):
        if step in (0, 3, 4, 7):
            lead = "chip"
            _ = lead


@loop(synth="lead_saw", interval=0.5)
def lead_saw():
    dj.volume = 0.13
    for step in range(8):
        if step in (0, 2, 4):
            lead = "saw"
            _ = lead


@loop(synth="lead_whistle", interval=1.0)
def lead_whistle():
    dj.volume = 0.09
    for phrase in range(4):
        if phrase in (0, 2):
            lead = "whistle"
            _ = lead


# ─── Atmospheric (comments = reverb) ────────────────────────────────────────

@loop(synth="pad_shimmer", interval=8.0)
def pad_shimmer():
    dj.volume = 0.08
    # wide hall reverb
    # slow harmonic drift
    # always underneath
    # never noticed until it stops
    pass


@loop(synth="air_warehouse", interval=4.0)
def air_warehouse():
    dj.volume = 0.07
    # concrete room texture
    # low ceiling
    # crowd warmth
    pass


@loop(synth="vox_ahh", interval=4.0)
def vox_ahh():
    dj.volume = 0.1
    # formant vowel texture
    # breathy
    for phrase in range(4):
        if phrase in (0, 2):
            vox = "ahh"
            _ = vox


@loop(synth="drone_space", interval=8.0)
def drone_space():
    dj.volume = 0.08
    # deep static drone
    # slow pitch drift
    pass


# ─── FX ─────────────────────────────────────────────────────────────────────

@loop(synth="fx_drop", interval=8.0)
def fx_drop():
    dj.volume = 0.18
    for layer in range(3):
        if layer == 0:
            hit = "thump"
        elif layer == 1:
            hit = "noise"
        else:
            hit = "tail"
        _ = hit


@loop(synth="fx_riser", interval=8.0)
def fx_riser():
    dj.volume = 0.15
    # sweeps upward over 8 seconds
    # retrigger by saving the file
    for step in range(4):
        if step == 3:
            peak = "top"
            _ = peak


@loop(synth="fx_glitch", interval=0.5)
def fx_glitch():
    dj.volume = 0.06
    for tick in range(8):
        if tick in (2, 5, 7):
            glitch = "tick"
            _ = glitch
        elif tick == 4:
            glitch = "stutter"
            _ = glitch


@loop(synth="fx_down", interval=8.0)
def fx_down():
    dj.volume = 0.13
    for step in range(4):
        if step == 0:
            fx = "drop"
            _ = fx


@loop(synth="fx_zap", interval=1.0)
def fx_zap():
    dj.volume = 0.12
    for step in range(4):
        if step in (0, 3):
            fx = "fx_zap"
            _ = fx


@loop(synth="fx_noise", interval=4.0)
def fx_noise():
    dj.volume = 0.14
    for layer in range(2):
        fx = "noise"
        _ = fx


@loop(synth="fx_laser", interval=1.0)
def fx_laser():
    dj.volume = 0.11
    for step in range(4):
        if step == 2:
            fx = "laser"
            _ = fx


@loop(synth="fx_vinyl", interval=8.0)
def fx_vinyl():
    dj.volume = 0.07
    # crackle and low background movement
    pass
