# PyCodeDJ dancefloor demo.
#
# Load sc/synths.scd in SuperCollider, then run:
#   pycodedj watch examples/club_set.py
#
# This file is intentionally a compact club groove, not a synth catalogue.
# The main weight is floor_kick + sub_bass + hat_engine + clap_snap.


# @loop floor_kick interval=1.0
def floor_kick():
    # four-on-the-floor foundation
    steps = [1, 1, 1, 1, 1, 1, 1, 1]
    for beat in range(8):
        if steps[beat]:
            if beat in (0, 4):
                body = "big"
            else:
                body = "tight"
            _ = body


# @loop sub_bass interval=0.5
def sub_bass():
    # rolling low end between the kicks
    groove = [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0]
    for step in range(12):
        if groove[step]:
            if step in (0, 5, 8):
                for pressure in range(2):
                    if pressure:
                        weight = "heavy"
                    else:
                        weight = "held"
                    _ = weight


# @loop hat_engine interval=0.25
def hat_engine():
    # offbeat lift and steady high-end motion
    for tick in range(16):
        if tick % 2 == 0:
            hat = "closed"
            _ = hat
        if tick in (3, 7, 11, 15):
            hat = "open"
            _ = hat


# @loop clap_snap interval=1.0
def clap_snap():
    # backbeat energy
    for beat in range(8):
        if beat in (2, 6):
            clap = "backbeat"
            _ = clap


# @loop dub_chord interval=2.0
def dub_chord():
    # sparse chord hits, kept behind the drums
    def root():
        return "low"

    def fifth():
        return "wide"

    return root(), fifth()


# @loop warehouse_air interval=4.0
# dark room
# low ceiling
# smoke
# crowd heat
def warehouse_air():
    pass
