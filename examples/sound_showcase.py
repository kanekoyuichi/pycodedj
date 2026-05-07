# PyCodeDJ — Sound Showcase
#
# Demonstrates every available synth name (31 total).
# Evaluate one loop at a time to hear each sound in isolation:
#
#   pycodedj eval examples/sound_showcase.py::kick_hard
#   pycodedj eval examples/sound_showcase.py::bass_acid
#   pycodedj eval examples/sound_showcase.py::riser_noise
#
# Or layer everything at once (heavy but instructive):
#
#   pycodedj watch examples/sound_showcase.py
#
# ─── Index ──────────────────────────────────────────────────────────────────
#
#   Kicks        kick_hard  floor_kick  kick_pulse
#   Basses       bass_rumble  bass_reese  sub_bass  bass_acid
#   Percussion   hat_engine  hat_ride  clap_snap  clap_snare
#                tom_drum  snare_roll  noise_crash
#   Chords       chord_rave  neon_stab  dub_chord
#                stab_saw  organ_chord  bell_rave
#   Leads        acid_lead  lead_hoover  soft_pluck  synth_arp
#   Atmospheric  shimmer_pad  warehouse_air  vox_ahh
#   FX           fx_impact  riser_noise  glitch_ticks

from pycodedj import loop


# ─── Kicks (depth=1: dark, punchy) ──────────────────────────────────────────

@loop("kick_hard", interval=1.0)
def demo_kick_hard(volume=0.85):
    hit = "down"
    _ = hit


@loop("floor_kick", interval=1.0)
def demo_floor_kick(volume=0.75):
    hit = "floor"
    _ = hit


@loop("kick_pulse", interval=1.0)
def demo_kick_pulse(volume=0.6):
    for beat in range(2):
        hit = "pulse"
        _ = hit


# ─── Basses (depth=2-3: mid-dark) ───────────────────────────────────────────

@loop("bass_rumble", interval=1.0)
def demo_bass_rumble(volume=0.35):
    sub = "rumble"
    _ = sub


@loop("bass_reese", interval=0.5)
def demo_bass_reese(volume=0.3):
    for step in range(4):
        if step % 2 == 0:
            note = "on"
            _ = note


@loop("sub_bass", interval=1.0)
def demo_sub_bass(volume=0.3):
    for step in range(4):
        note = "sub"
        _ = note


@loop("bass_acid", interval=0.5)
def demo_bass_acid(volume=0.25):
    for step in range(8):
        if step in (0, 3, 5):
            for bend in range(2):
                note = f"acid_{bend}"
                _ = note


# ─── Percussion (depth=1-2: crisp and dry) ──────────────────────────────────

@loop("hat_engine", interval=0.25)
def demo_hat_engine(volume=0.12):
    for tick in range(8):
        if tick % 2 == 0:
            hat = "closed"
            _ = hat


@loop("hat_ride", interval=0.5)
def demo_hat_ride(volume=0.1):
    for step in range(4):
        if step % 2 == 1:
            ride = "on"
            _ = ride


@loop("clap_snap", interval=1.0)
def demo_clap_snap(volume=0.2):
    for beat in range(4):
        if beat in (1, 3):
            snap = "crack"
            _ = snap


@loop("clap_snare", interval=1.0)
def demo_clap_snare(volume=0.22):
    for beat in range(4):
        if beat == 2:
            hit = "snare"
            _ = hit


@loop("tom_drum", interval=1.0)
def demo_tom_drum(volume=0.25):
    for beat in range(4):
        if beat in (2, 3):
            tom = "hit"
            _ = tom


@loop("snare_roll", interval=1.0)
def demo_snare_roll(volume=0.2):
    for tick in range(16):
        if tick % 2 == 0:
            for layer in range(2):
                roll = f"r{layer}"
                _ = roll


@loop("noise_crash", interval=4.0)
def demo_noise_crash(volume=0.2):
    for layer in range(3):
        crash = "hit"
        _ = crash


# ─── Chords & Stabs (depth=4-5: bright) ─────────────────────────────────────

@loop("chord_rave", interval=2.0)
def demo_chord_rave(volume=0.14):
    for phrase in range(4):
        for voice in range(3):
            if phrase == 0:
                chord = "root"
            else:
                chord = "alt"
            _ = chord


@loop("neon_stab", interval=2.0)
def demo_neon_stab(volume=0.12):
    for phrase in range(4):
        for voice in range(2):
            if phrase in (0, 2):
                stab = "hit"
                _ = stab


@loop("dub_chord", interval=2.0)
def demo_dub_chord(volume=0.13):
    for phrase in range(4):
        for voice in range(2):
            chord = "dub"
            _ = chord


@loop("stab_saw", interval=1.0)
def demo_stab_saw(volume=0.2):
    for phrase in range(4):
        for voice in range(3):
            if phrase % 2 == 0:
                stab = "hit"
                _ = stab


@loop("organ_chord", interval=2.0)
def demo_organ_chord(volume=0.14):
    for phrase in range(4):
        for voice in range(2):
            chord = "organ"
            _ = chord


@loop("bell_rave", interval=2.0)
def demo_bell_rave(volume=0.12):
    for phrase in range(4):
        for step in range(2):
            if phrase in (0, 2):
                bell = "ring"
                _ = bell


# ─── Leads (depth=4-5: bright, melodic) ─────────────────────────────────────

@loop("acid_lead", interval=0.5)
def demo_acid_lead(volume=0.15):
    for step in range(8):
        if step % 2 == 0:
            for note in range(2):
                lead = f"a{note}"
                _ = lead


@loop("lead_hoover", interval=4.0)
def demo_lead_hoover(volume=0.12):
    for phrase in range(4):
        for step in range(3):
            if phrase in (0, 2):
                motion = "on"
                _ = motion


@loop("soft_pluck", interval=1.0)
def demo_soft_pluck(volume=0.12):
    for step in range(6):
        for note in range(2):
            if step % 3 == 0:
                pluck = "hit"
                _ = pluck


@loop("synth_arp", interval=0.5)
def demo_synth_arp(volume=0.14):
    for step in range(8):
        for note in range(2):
            if step % 2 == 0:
                arp = f"n{note}"
                _ = arp


# ─── Atmospheric (comments = reverb) ────────────────────────────────────────

@loop("shimmer_pad", interval=8.0)
def demo_shimmer_pad(volume=0.08):
    # wide hall reverb
    # slow harmonic drift
    # always underneath
    # never noticed until it stops
    pass


@loop("warehouse_air", interval=4.0)
def demo_warehouse_air(volume=0.07):
    # concrete room texture
    # low ceiling
    # crowd warmth
    pass


@loop("vox_ahh", interval=4.0)
def demo_vox_ahh(volume=0.1):
    # formant vowel texture
    # breathy
    for phrase in range(4):
        if phrase in (0, 2):
            vox = "ahh"
            _ = vox


# ─── FX ─────────────────────────────────────────────────────────────────────

@loop("fx_impact", interval=8.0)
def demo_fx_impact(volume=0.18):
    for layer in range(3):
        if layer == 0:
            hit = "thump"
        elif layer == 1:
            hit = "noise"
        else:
            hit = "tail"
        _ = hit


@loop("riser_noise", interval=8.0)
def demo_riser_noise(volume=0.15):
    # sweeps upward over 8 seconds
    # retrigger by saving the file
    for step in range(4):
        if step == 3:
            peak = "top"
            _ = peak


@loop("glitch_ticks", interval=0.5)
def demo_glitch_ticks(volume=0.06):
    for tick in range(8):
        if tick in (2, 5, 7):
            glitch = "tick"
            _ = glitch
        elif tick == 4:
            glitch = "stutter"
            _ = glitch
