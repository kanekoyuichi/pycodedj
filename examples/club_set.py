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

from pycodedj import dj, loop


# --- Drum engine: stable pulse first, variations second ---

@loop(synth="kick_floor", beat=0.117)
def kick():
    dj.volume = 1.0
    dj.eq = "edm"
    dj.low = 1.7
    dj.mid = 0.78
    dj.high = 0.82
    dj.pattern = (
        "x . . . x . . . x . . . x . . . "
        "x . . . x . . x x . . . x . . x"
    )


@loop(synth="clap_snare", beat=0.117)
def clap():
    dj.volume = 0.18
    dj.eq = "pop"
    dj.low = 0.62
    dj.mid = 0.85
    dj.high = 0.98
    dj.pattern = (
        ". . . . x . . . . . . . x . . . "
        ". . . . x . . . . . . x x . x ."
    )


@loop(synth="hat_ride", beat=0.117)
def offhat():
    dj.volume = 0.065
    dj.eq = "edm"
    dj.low = 0.28
    dj.mid = 0.78
    dj.high = 1.0
    dj.pattern = (
        ". . x . . . x . . . x . . . x . "
        ". . x . . x x . . . x . . x x ."
    )


@loop(synth="hat_engine", beat=0.0585)
def hats():
    dj.volume = 0.075
    dj.eq = "edm"
    dj.low = 0.3
    dj.mid = 0.82
    dj.high = 1.02
    dj.pattern = (
        "x . x . x x x . x . x . x x x . "
        "x x x . x . x x x . x x x . x ."
    )


# --- Low end: kick-locked weight with room-shaking sustain ---

@loop(synth="bass_rumble", root="A1", scale="minor", beat=0.117)
def rumble():
    dj.volume = 0.42
    dj.eq = "edm"
    dj.low = 1.75
    dj.mid = 0.58
    dj.high = 0.32
    dj.pattern = (
        "0 ~ . . 0 ~ . . 0 ~ . . 0 ~ . . "
        "0 ~ . . 3 ~ . . 0 ~ . . 5 3 0 ."
    )


@loop(synth="bass_sub", root="A1", scale="minor", beat=0.117)
def sub():
    dj.volume = 0.58
    dj.eq = "edm"
    dj.low = 1.85
    dj.mid = 0.58
    dj.high = 0.25
    dj.pattern = (
        "0 ~ . 0 0 ~ . 0 0 ~ 3 . 0 ~ . 0 "
        "0 ~ 0 . 3 ~ . 0 0 ~ 5 . 3 ~ 0 ."
    )


@loop(synth="bass_sub", root="A1", scale="minor", beat=0.468)
def floor():
    dj.volume = 0.22
    dj.eq = "edm"
    dj.low = 1.9
    dj.mid = 0.45
    dj.high = 0.2
    dj.pattern = "0 ~ 0 ~ 0 ~ 0 ~"


@loop(synth="bass_acid", root="A1", scale="minor", beat=0.0585)
def acid():
    dj.volume = 0.15
    dj.eq = "edm"
    dj.low = 1.15
    dj.mid = 0.88
    dj.high = 0.72
    dj.pattern = (
        "0 . 0 . 3 . 0 0 0 . 5 . 3 . 0 . "
        "0 . 0 3 . 5 . 3 0 . 7 . 5 . 3 . "
        "0 3 0 . 5 . 7 . 0 . 5 3 0 . 10 . "
        "0 . 0 . 3 . 0 0 5 . 3 . 0 . 0 ."
    )


# --- Hooks and fills: sparse enough to leave room for the bass ---

@loop(synth="chord_rave", root="A2", scale="minor", beat=0.117)
def stabs():
    dj.volume = 0.095
    dj.eq = "edm"
    dj.low = 0.55
    dj.mid = 0.72
    dj.high = 0.78
    dj.pattern = (
        ". . . . [0 2 4] . . . . . . . [3 5 7] . . . "
        ". . [5 7 9] . . . . . [0 2 4] . . . [3 5 7] . . ."
    )


@loop(synth="tom_drum", root="A1", scale="minor", beat=0.0585)
def fill():
    dj.volume = 0.09
    dj.eq = "edm"
    dj.low = 1.15
    dj.mid = 0.72
    dj.high = 0.5
    dj.pattern = (
        ". . . . . . . . . . . . . . . . "
        ". . . . . . . . . . 0 . 3 5 7 10"
    )


@loop(synth="air_warehouse", root="A1", scale="minor", beat=0.468)
def room():
    dj.volume = 0.08
    dj.eq = "edm"
    dj.low = 1.2
    dj.mid = 0.55
    dj.high = 0.45
    # dark concrete reflections
    # low frequency pressure
    # distant system noise
    dj.pattern = "0 . . . 0 . 3 . 0 . . . 5 . 3 ."
