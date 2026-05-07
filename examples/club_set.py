# PyCodeDJ club groove.
#
# Load sc/synths.scd in SuperCollider, then run:
#   pycodedj watch examples/club_set.py
#
# Design notes:
# - kick_floor is fixed near 128 BPM four-on-the-floor
# - bass_sub carries physical low-end pressure and pumps against the kick
# - hat_offbeat and clap_backbeat create the offbeat/backbeat groove
# - chord_dub and fx_air add repetition and space without taking over


# @loop kick_floor interval=1.0
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


# @loop bass_sub interval=0.5
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


# @loop hat_offbeat interval=0.25
def hat_engine():
    # Offbeat motion: the body waits for the next kick.
    for tick in range(16):
        if tick in (2, 6, 10, 14):
            hat = "open_offbeat"
            _ = hat
        if tick % 2 == 0:
            hat = "closed_drive"
            _ = hat


# @loop clap_backbeat interval=1.0
def clap_snap():
    # Backbeat accent: simple, repeated, social.
    for bar in range(4):
        for beat in range(4):
            if beat == 2:
                clap = "backbeat"
                _ = clap


# @loop chord_dub interval=2.0
def dub_chord():
    # Repeated harmonic cue, not a melody.
    def root():
        return "low"

    def fifth():
        return "wide"

    return root(), fifth()


# @loop fx_air interval=4.0
# dark room
# low ceiling
# smoke
# crowd heat
def warehouse_air():
    pass
