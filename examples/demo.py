# PyCodeDJ demo — run each loop independently:
#   pycodedj eval examples/demo.py::kick
#   pycodedj eval examples/demo.py::bass
#   pycodedj eval examples/demo.py::melody
#   pycodedj eval examples/demo.py::pad

from pycodedj import dj, loop


@loop(synth="kick_floor", beat=0.25)
def kick():
    dj.volume = 0.8
    dj.eq = "edm"
    dj.low = 1.5
    dj.pattern = "x . . . x . . ."


@loop(synth="bass_acid", root="A1", scale="minor", beat=0.25)
def bass():
    dj.volume = 0.35
    dj.eq = "edm"
    dj.low = 1.3
    dj.pattern = "0 . 3 . 5 . 3 ."


@loop(synth="lead_acid", root="A3", scale="minor", beat=0.25)
def melody():
    dj.volume = 0.18
    dj.pattern = ". 0 . 3 . 5 7 ."


@loop(synth="pad_shimmer", root="A2", scale="minor", beat=0.5)
def pad():
    dj.volume = 0.15
    dj.eq = "ambient"
    dj.pattern = "[0 2 4] . . . [5 7 9] . . ."
