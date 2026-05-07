# PyCodeDJ club-style demo.
#
# Load sc/synths.scd in SuperCollider, then bring parts in and out:
#   pycodedj eval examples/club_set.py::sub_bass
#   pycodedj eval examples/club_set.py::hat_engine
#   pycodedj eval examples/club_set.py::neon_stab
#   pycodedj eval examples/club_set.py::acid_lead
#   pycodedj eval examples/club_set.py::warehouse_air
#   pycodedj eval examples/club_set.py::kick_pulse
#   pycodedj eval examples/club_set.py::glitch_ticks
#   pycodedj eval examples/club_set.py::soft_pluck
#   pycodedj eval examples/club_set.py::dub_chord
#   pycodedj eval examples/club_set.py::shimmer_pad
#
# These blocks are meant as code-structure performance material. Edit and save
# them live, then re-run eval for a loop to push a new sound shape.


# @loop sub_bass interval=1.0
def sub_bass():
    pulse = [1, 0, 0, 1, 0, 1, 0, 0]
    for step in range(8):
        if pulse[step]:
            if step in (0, 5):
                drive = "heavy"
            else:
                drive = "tight"
            _ = drive


# @loop hat_engine interval=0.25
def hat_engine():
    grid = range(16)
    for tick in grid:
        if tick % 2 == 0:
            accent = "closed"
        if tick in (3, 7, 11, 15):
            accent = "open"
        _ = accent


# @loop neon_stab interval=2.0
def neon_stab():
    def chord_root():
        return "minor"

    def chord_fifth():
        return "pressure"

    def chord_seventh():
        return "glow"

    return chord_root(), chord_fifth(), chord_seventh()


# @loop acid_lead interval=0.5
def acid_lead():
    pattern = [0, 3, 7, 10, 12, 10, 7, 3]
    for note in pattern:
        if note > 9:
            for slide in range(2):
                if slide == 1:
                    bend = "up"
                else:
                    bend = "down"
                _ = bend


# @loop warehouse_air interval=4.0
# smoke above the kick
# late reflections
# concrete room tail
# crowd heat
# blue strobes
def warehouse_air():
    pass


# @loop kick_pulse interval=1.0
def kick_pulse():
    for beat in range(4):
        if beat == 0:
            weight = "downbeat"
        else:
            weight = "ghost"
        _ = weight


# @loop glitch_ticks interval=0.25
def glitch_ticks():
    for grain in range(12):
        if grain % 3 == 0:
            cut = "sharp"
        if grain in (5, 9):
            cut = "scatter"
        _ = cut


# @loop soft_pluck interval=0.5
def soft_pluck():
    notes = ["root", "third", "fifth", "octave"]
    for note in notes:
        if note in ("fifth", "octave"):
            color = "bright"
        else:
            color = "round"
        _ = color


# @loop dub_chord interval=2.0
def dub_chord():
    def root():
        return "low"

    def fifth():
        return "wide"

    return root(), fifth()


# @loop shimmer_pad interval=4.0
# high ceiling
# silver trail
# slow light
# suspended air
def shimmer_pad():
    pass
