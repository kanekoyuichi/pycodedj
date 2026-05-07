# PyCodeDJ club-style demo.
#
# Load sc/synths.scd in SuperCollider, then bring parts in and out:
#   pycodedj eval examples/club_set.py::sub_bass
#   pycodedj eval examples/club_set.py::hat_engine
#   pycodedj eval examples/club_set.py::neon_stab
#   pycodedj eval examples/club_set.py::acid_lead
#   pycodedj eval examples/club_set.py::warehouse_air
#   pycodedj eval examples/club_set.py::kick_pulse
#   pycodedj eval examples/club_set.py::floor_kick
#   pycodedj eval examples/club_set.py::glitch_ticks
#   pycodedj eval examples/club_set.py::soft_pluck
#   pycodedj eval examples/club_set.py::dub_chord
#   pycodedj eval examples/club_set.py::shimmer_pad
#
# Start with floor_kick + sub_bass + hat_engine, then add chords, plucks,
# acid, and air. Edit and save while watch is running to reshape the groove.


# @loop floor_kick interval=1.0
def floor_kick():
    four_on_floor = [1, 1, 1, 1]
    for beat in range(4):
        if four_on_floor[beat]:
            if beat == 0:
                room = "boom"
            else:
                room = "thump"
            _ = room


# @loop sub_bass interval=0.5
def sub_bass():
    groove = [1, 0, 1, 1, 0, 1, 0, 1]
    for step in range(8):
        if groove[step]:
            if step in (0, 2, 5):
                for push in range(2):
                    if push == 1:
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
            _ = accent
        if tick in (3, 7, 11, 15):
            for lift in range(2):
                if lift == 1:
                    accent = "open"
                _ = accent


# @loop neon_stab interval=1.0
def neon_stab():
    def chord_root():
        return "minor"

    def chord_fifth():
        return "pressure"

    def chord_seventh():
        return "glow"

    return chord_root(), chord_fifth(), chord_seventh()


# @loop acid_lead interval=0.25
def acid_lead():
    pattern = [0, 3, 7, 10, 12, 10, 15, 7, 3, 10, 12, 17]
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
# hands up
# pressure wave
def warehouse_air():
    pass


# @loop kick_pulse interval=0.5
def kick_pulse():
    hits = [1, 0, 0, 1, 0, 0, 1, 0]
    for beat in range(8):
        if hits[beat]:
            if beat in (0, 6):
                weight = "downbeat"
            else:
                weight = "bounce"
            _ = weight


# @loop glitch_ticks interval=0.25
def glitch_ticks():
    for grain in range(16):
        if grain % 3 == 0:
            cut = "sharp"
            _ = cut
        if grain in (5, 9, 13):
            for scatter in range(2):
                if scatter:
                    cut = "scatter"
                _ = cut


# @loop soft_pluck interval=0.5
def soft_pluck():
    notes = ["root", "third", "fifth", "octave", "fifth", "third"]
    for note in notes:
        if note in ("fifth", "octave"):
            color = "bright"
        else:
            color = "round"
        _ = color


# @loop dub_chord interval=1.0
def dub_chord():
    def root():
        return "low"

    def fifth():
        return "wide"

    def seventh():
        return "push"

    return root(), fifth(), seventh()


# @loop shimmer_pad interval=4.0
# high ceiling
# silver trail
# slow light
# suspended air
# ceiling shimmer
# late-night lift
def shimmer_pad():
    pass
