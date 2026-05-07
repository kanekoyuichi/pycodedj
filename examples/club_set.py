# PyCodeDJ club groove.
#
# Load sc/synths.scd in SuperCollider, then run:
#   pycodedj watch examples/club_set.py
#
# Design notes:
# - floor_kick is fixed near 128 BPM four-on-the-floor
# - sub_bass carries physical low-end pressure and pumps against the kick
# - hat_engine and clap_snap create the offbeat/backbeat groove
# - dub_chord, warehouse_air, and build_riser add repetition, space, and tension


# @loop floor_kick interval=1.0
def floor_kick():
    # Four on the floor: predictable, physical, collective.
    steps = [1, 1, 1, 1]
    for bar in range(4):
        for beat in range(4):
            if steps[beat]:
                if beat == 0:
                    body = "big"
                else:
                    body = "steady"
                _ = body


# @loop sub_bass interval=0.5
def sub_bass():
    # Low pressure, sparse notes, repeated until the body locks in.
    groove = [1, 0, 0, 1, 0, 1, 0, 0]
    for cycle in range(2):
        for step in range(8):
            if groove[step]:
                if step in (0, 5):
                    for pressure in range(3):
                        if pressure:
                            weight = "heavy"
                        else:
                            weight = "held"
                        _ = weight


# @loop hat_engine interval=0.25
def hat_engine():
    # Offbeat motion: the body waits for the next kick.
    for tick in range(16):
        if tick in (2, 6, 10, 14):
            hat = "open_offbeat"
            _ = hat
        if tick % 2 == 0:
            hat = "closed_drive"
            _ = hat


# @loop clap_snap interval=1.0
def clap_snap():
    # Backbeat accent: simple, repeated, social.
    for bar in range(4):
        for beat in range(4):
            if beat == 2:
                clap = "backbeat"
                _ = clap


# @loop dub_chord interval=2.0
def dub_chord():
    # Repeated harmonic cue, not a melody.
    def root():
        return "low"

    def fifth():
        return "wide"

    return root(), fifth()


# @loop build_riser interval=4.0
# filter opens
# pressure rises
# crowd waits
# kick returns
def build_riser():
    pass


# @loop warehouse_air interval=4.0
# dark room
# low ceiling
# smoke
# crowd heat
def warehouse_air():
    pass
