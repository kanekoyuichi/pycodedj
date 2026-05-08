# PyCodeDJ club set — sub-heavy warehouse floor
#
# Load sc/synths.scd in SuperCollider, then run:
#   pycodedj watch examples/club_set.py
#
# Club-focused design:
# - steady four-on-the-floor kick for dancers
# - clap on 2 and 4
# - offbeat hats plus 16th-note motion
# - bass notes locked to the kick with syncopated replies
# - sustained sub and rumble layers for floor pressure
# - sparse stabs and fills so the bass has room

from pycodedj import loop, pattern


# --- Drum engine: stable pulse first, variations second ---

@loop("kick", synth="floor_kick", dur=0.117)
def kick(volume=1.0, eq="edm", low=1.7, mid=0.78, high=0.82):
    pattern(
        "x . . . x . . . x . . . x . . . "
        "x . . . x . . x x . . . x . . x"
    )


@loop("clap", synth="clap_snare", dur=0.117)
def clap(volume=0.18, eq="pop", low=0.62, mid=0.85, high=0.98):
    pattern(
        ". . . . x . . . . . . . x . . . "
        ". . . . x . . . . . . x x . x ."
    )


@loop("offhat", synth="hat_ride", dur=0.117)
def offhat(volume=0.065, eq="edm", low=0.28, mid=0.78, high=1.0):
    pattern(
        ". . x . . . x . . . x . . . x . "
        ". . x . . x x . . . x . . x x ."
    )


@loop("hats", synth="hat_engine", dur=0.0585)
def hats(volume=0.075, eq="edm", low=0.3, mid=0.82, high=1.02):
    pattern(
        "x . x . x x x . x . x . x x x . "
        "x x x . x . x x x . x x x . x ."
    )


# --- Low end: kick-locked weight with room-shaking sustain ---

@loop("rumble", synth="bass_rumble", root="A1", scale="minor", dur=0.117)
def rumble(volume=0.42, eq="edm", low=1.75, mid=0.58, high=0.32):
    pattern(
        "0 ~ . . 0 ~ . . 0 ~ . . 0 ~ . . "
        "0 ~ . . 3 ~ . . 0 ~ . . 5 3 0 ."
    )


@loop("sub", synth="sub_bass", root="A1", scale="minor", dur=0.117)
def sub(volume=0.58, eq="edm", low=1.85, mid=0.58, high=0.25):
    pattern(
        "0 ~ . 0 0 ~ . 0 0 ~ 3 . 0 ~ . 0 "
        "0 ~ 0 . 3 ~ . 0 0 ~ 5 . 3 ~ 0 ."
    )


@loop("floor", synth="sub_bass", root="A1", scale="minor", dur=0.468)
def floor(volume=0.22, eq="edm", low=1.9, mid=0.45, high=0.2):
    pattern("0 ~ 0 ~ 0 ~ 0 ~")


@loop("acid", synth="bass_acid", root="A1", scale="minor", dur=0.0585)
def acid(volume=0.15, eq="edm", low=1.15, mid=0.88, high=0.72):
    pattern(
        "0 . 0 . 3 . 0 0 0 . 5 . 3 . 0 . "
        "0 . 0 3 . 5 . 3 0 . 7 . 5 . 3 . "
        "0 3 0 . 5 . 7 . 0 . 5 3 0 . 10 . "
        "0 . 0 . 3 . 0 0 5 . 3 . 0 . 0 ."
    )


# --- Hooks and fills: sparse enough to leave room for the bass ---

@loop("stabs", synth="chord_rave", root="A2", scale="minor", dur=0.117)
def stabs(volume=0.095, eq="edm", low=0.55, mid=0.72, high=0.78):
    pattern(
        ". . . . [0 2 4] . . . . . . . [3 5 7] . . . "
        ". . [5 7 9] . . . . . [0 2 4] . . . [3 5 7] . . ."
    )


@loop("fill", synth="tom_drum", root="A1", scale="minor", dur=0.0585)
def fill(volume=0.09, eq="edm", low=1.15, mid=0.72, high=0.5):
    pattern(
        ". . . . . . . . . . . . . . . . "
        ". . . . . . . . . . 0 . 3 5 7 10"
    )


@loop("room", synth="warehouse_air", root="A1", scale="minor", dur=0.468)
def room(volume=0.08, eq="edm", low=1.2, mid=0.55, high=0.45):
    # dark concrete reflections
    # low frequency pressure
    # distant system noise
    pattern("0 . . . 0 . 3 . 0 . . . 5 . 3 .")
