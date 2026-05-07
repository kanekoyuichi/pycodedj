# PyCodeDJ club groove.
#
# Load sc/synths.scd in SuperCollider, then run:
#   pycodedj watch examples/club_set.py
#
# Design notes:
# - kick_hard and bass_rumble make a physical four-on-the-floor foundation
# - bass_reese adds moving low-mid pressure instead of a static bass tone
# - hat_offbeat, hat_ride, clap_backbeat, and clap_snare create the body groove
# - chord_rave, lead_hoover, fx_air, and fx_impact add club-scale space and release


# @loop kick_hard interval=1.0
def hard_floor_kick():
    # Four on the floor, with bar accents so the loop breathes.
    for bar in range(8):
        for beat in range(4):
            if beat == 0:
                hit = "downbeat_weight"
            else:
                hit = "steady_drive"
            if bar in (3, 7) and beat == 3:
                hit = "pickup_push"
            _ = hit


# @loop bass_rumble interval=1.0
def kick_rumble():
    # A low tail that follows the kick and fills the room between beats.
    for bar in range(4):
        for beat in range(4):
            if beat in (0, 1, 2, 3):
                for tail in range(3):
                    if tail == 0:
                        pressure = "thump"
                    elif tail == 1:
                        pressure = "sub_tail"
                    else:
                        pressure = "room_rumble"
                    _ = pressure


# @loop bass_reese interval=0.5
def reese_bassline():
    # Syncopated low-mid movement, leaving holes for the kick.
    groove = [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0]
    accents = {0: "root", 5: "push", 10: "answer", 13: "turnaround"}
    for cycle in range(2):
        for step, active in enumerate(groove):
            if active:
                phrase = accents.get(step, "ghost")
                if step in (5, 13):
                    for slide in range(2):
                        phrase = f"{phrase}_slide_{slide}"
                        _ = phrase
                else:
                    _ = phrase


# @loop hat_offbeat interval=0.25
def offbeat_hats():
    # Offbeat hats keep the body waiting for the next kick.
    for tick in range(16):
        if tick in (2, 6, 10, 14):
            hat = "open_offbeat"
            _ = hat
        if tick % 2 == 0:
            hat = "closed_drive"
            _ = hat
        if tick in (7, 15):
            hat = "late_shuffle"
            _ = hat


# @loop hat_ride interval=0.5
def ride_layer():
    # A longer metallic layer for lift without turning into a melody.
    pattern = [0, 1, 0, 1, 1, 0, 1, 0]
    for bar in range(4):
        for step, active in enumerate(pattern):
            if active:
                if bar >= 2 and step in (4, 6):
                    ride = "wide_open"
                else:
                    ride = "tight"
                _ = ride


# @loop clap_backbeat interval=1.0
def backbeat_clap():
    # Simple social backbeat: this stays readable.
    for bar in range(8):
        for beat in range(4):
            if beat == 2:
                clap = "backbeat"
                _ = clap
            if bar in (3, 7) and beat == 3:
                clap = "pre_drop_flam"
                _ = clap


# @loop clap_snare interval=1.0
def snare_accent():
    # Adds harder punctuation on phrase endings.
    for bar in range(8):
        for beat in range(4):
            if bar in (1, 3, 5, 7) and beat == 2:
                snare = "hard_two"
                _ = snare
            if bar == 7 and beat in (2, 3):
                snare = "fill"
                _ = snare


# @loop chord_rave interval=2.0
def rave_stabs():
    # Short harmonic hits: repetition first, melody second.
    def minor_root():
        return "root"

    def pressure_fifth():
        return "fifth"

    def club_seventh():
        return "seventh"

    for phrase in range(4):
        if phrase in (0, 2):
            color = minor_root()
        elif phrase == 1:
            color = pressure_fifth()
        else:
            color = club_seventh()
        _ = color


# @loop lead_hoover interval=4.0
def hoover_answer():
    # Sparse lead answer, not a constant siren.
    for phrase in range(4):
        if phrase == 0:
            motion = "rise"
        elif phrase == 2:
            motion = "fall"
        else:
            motion = "hold_back"
        if phrase in (0, 2):
            for bend in range(2):
                motion = f"{motion}_{bend}"
                _ = motion


# @loop fx_impact interval=8.0
# pressure drop
# room inhale
# hands up
def impact_drop():
    # One impact per larger phrase.
    pass


# @loop fx_air interval=4.0
# dark room
# low ceiling
# smoke
# crowd heat
# concrete reflections
# blue strobes
def warehouse_air():
    pass
