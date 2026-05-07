# PyCodeDJ club groove.
#
# Load sc/synths.scd in SuperCollider, then run:
#   pycodedj watch examples/club_set.py
#
# Layers:
#   foundation  — kick_hard + bass_rumble hold the floor
#   movement    — bass_reese + hat_engine + hat_ride carry the groove
#   body        — clap_snap + clap_snare mark the phrase
#   harmonic    — chord_rave + neon_stab build the energy
#   space       — lead_hoover + shimmer_pad open the room
#   texture     — glitch_ticks + fx_impact + warehouse_air fill the edges

from pycodedj import loop


# --- Foundation ---

@loop("kick_hard", interval=1.0)
def floor_kick(volume=0.9):
    for bar in range(8):
        for beat in range(4):
            if beat == 0:
                weight = "anchor"
            elif beat == 2:
                weight = "lift"
            else:
                weight = "steady"
            if bar in (3, 7) and beat == 3:
                weight = "push"
            _ = weight


@loop("bass_rumble", interval=1.0)
def sub_pulse(volume=0.36):
    for bar in range(4):
        for beat in range(4):
            if beat == 0:
                layer = "punch"
            else:
                layer = "tail"
            for harmonic in range(2):
                sub = f"{layer}_{harmonic}"
                _ = sub


# --- Movement ---

@loop("bass_reese", interval=0.5)
def reese_groove(volume=0.3):
    groove = [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0]
    accent = {0: "root", 3: "ghost", 5: "fifth", 9: "push", 13: "turn"}
    for step, active in enumerate(groove):
        if active:
            phrase = accent.get(step, "mid")
            if step in (5, 9):
                for bend in range(2):
                    phrase = f"{phrase}_{bend}"
                    _ = phrase
            else:
                _ = phrase


@loop("hat_engine", interval=0.25)
def closed_hats(volume=0.12):
    for bar in range(2):
        for tick in range(16):
            if tick % 4 == 0:
                hat = "downbeat"
            elif tick % 2 == 0:
                hat = "upbeat"
            elif tick in (3, 7, 11, 15):
                hat = "ghost"
            else:
                hat = "skip"
            if tick in (6, 14):
                hat = "open"
            _ = hat


@loop("hat_ride", interval=0.5)
def ride_layer(volume=0.09):
    offbeat = [0, 1, 0, 1, 1, 0, 1, 0]
    for bar in range(4):
        for step, on in enumerate(offbeat):
            if on:
                ride = "wide" if bar >= 2 and step in (4, 6) else "tight"
                _ = ride


# --- Body ---

@loop("clap_snap", interval=1.0)
def snap_back(volume=0.2):
    for bar in range(8):
        for beat in range(4):
            if beat in (1, 3):
                snap = "crack"
                _ = snap
            if bar in (3, 7) and beat == 3:
                snap = "flam"
                _ = snap


@loop("clap_snare", interval=1.0)
def heavy_two(volume=0.22):
    for bar in range(8):
        for beat in range(4):
            if bar % 2 == 1 and beat == 2:
                hit = "heavy"
                _ = hit
            if bar == 7 and beat in (2, 3):
                hit = "fill"
                _ = hit


# --- Harmonic ---

@loop("chord_rave", interval=2.0)
def rave_stabs(volume=0.14):
    def root():
        return "minor_root"

    def fifth():
        return "power_fifth"

    def seventh():
        return "flat_seventh"

    def resolve():
        return "octave_drop"

    for phrase in range(4):
        if phrase == 0:
            chord = root()
        elif phrase == 1:
            chord = fifth()
        elif phrase == 2:
            chord = seventh()
        else:
            chord = resolve()
        _ = chord


@loop("neon_stab", interval=2.0)
def stab_layer(volume=0.1):
    # darker stab answers the rave chord
    # one bar behind, shifted a fifth below
    for phrase in range(4):
        if phrase in (1, 3):
            stab = "answer"
            _ = stab


# --- Space ---

@loop("lead_hoover", interval=4.0)
def hoover(volume=0.12):
    for phrase in range(4):
        if phrase in (0, 2):
            for step in range(3):
                if step == 0:
                    motion = "attack"
                elif step == 1:
                    motion = "hold"
                else:
                    motion = "fade"
                _ = motion
        else:
            _ = "rest"


@loop("shimmer_pad", interval=8.0)
def shimmer(volume=0.07):
    # wide hall reverb
    # slow harmonic drift across the stereo field
    # always underneath everything
    # never noticed until it stops
    pass


# --- Texture ---

@loop("glitch_ticks", interval=0.5)
def digital_noise(volume=0.05):
    for tick in range(8):
        if tick in (2, 5, 7):
            glitch = "tick"
            _ = glitch
        elif tick == 4:
            glitch = "stutter"
            _ = glitch


@loop("fx_impact", interval=8.0)
def drop_hit(volume=0.18):
    # pressure builds to the drop
    # room holds its breath
    # release
    for layer in range(3):
        if layer == 0:
            hit = "thump"
        elif layer == 1:
            hit = "noise"
        else:
            hit = "tail"
        _ = hit


@loop("warehouse_air", interval=4.0)
def room_tone(volume=0.06):
    # concrete walls
    # low ceiling pressing down
    # crowd warmth from two hundred bodies
    # sub frequencies bleeding through from the main room
    # smoke machine haze diffusing the strobes
    # the room is the instrument
    pass
