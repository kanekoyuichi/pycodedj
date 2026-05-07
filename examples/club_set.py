# PyCodeDJ club groove — EDM edition
#
# 8 loops, each with a distinct code structure and sonic role.
# Load sc/synths.scd in SuperCollider, then run:
#   pycodedj watch examples/club_set.py
#
# Code structure → sound (by design):
#
#   kick_hard    depth=1, cf=0  →  580 Hz,  0.10 Hz LFO  (dark, static)
#   sub_bass     depth=2, cf=1  →  960 Hz,  0.59 Hz LFO  (dark sub pulse)
#   bass_acid    depth=5, cf=4  → 2100 Hz,  2.06 Hz LFO  (acid squelch)
#   hat_engine   depth=7, cf=9  → 2860 Hz,  4.51 Hz LFO  (brightest, fastest)
#   clap_snare   depth=6, cf=5  → 2480 Hz,  2.55 Hz LFO  (bright backbeat)
#   chord_rave   depth=7, cf=7  → 2860 Hz,  3.53 Hz LFO  (rave stabs)
#   lead_hoover  depth=5, cf=4  → 2100 Hz,  2.06 Hz LFO  reverb=0.15
#   shimmer_pad  depth=1, cf=0  →  580 Hz,  0.10 Hz LFO  reverb=0.60

from pycodedj import loop


# --- Foundation: dead simple, bone-dry ---

@loop("kick_hard", interval=1.0)
def four_on_floor(volume=0.9, eq="edm", low=1.25):
    hit = "down"
    _ = hit


# --- Sub: minimal pulse, barely more than the kick ---

@loop("sub_bass", interval=1.0)
def sub_layer(volume=0.4, eq="edm", low=1.45, high=0.7):
    for beat in range(4):
        sub = "low"
        _ = sub


# --- Groove: syncopated acid sequence with accents ---

@loop("bass_acid", interval=0.5)
def acid_line(volume=0.22, eq="edm", low=1.2, mid=1.05):
    pattern = [
        ("hit", True), ("skip", False), ("slide", True),
        ("hit", True), ("skip", False), ("accent", True),
        ("skip", False), ("slide", True),
    ]
    for step, (note, active) in enumerate(pattern):
        if active:
            for layer in range(2):
                if layer == 0:
                    out = note
                else:
                    out = f"{note}_tail"
                _ = out


# --- Hats: mechanical 16th-note grid ---

@loop("hat_engine", interval=0.25)
def closed_hats(volume=0.13, eq="edm", low=0.45, high=1.25):
    for bar in range(2):
        for tick in range(16):
            if tick % 4 == 0:
                if tick == 0:
                    if bar == 0:
                        hat = "anchor_a"
                    else:
                        hat = "anchor_b"
                else:
                    hat = "beat"
            elif tick % 2 == 0:
                hat = "up"
            elif tick in (3, 7, 11, 15):
                if bar == 0:
                    hat = "ghost_a"
                else:
                    hat = "ghost_b"
            else:
                hat = "skip"
            if tick in (6, 14):
                hat = "open"
            _ = hat


# --- Backbeat: decisive 2 & 4 with fill on bar 4 ---

@loop("clap_snare", interval=1.0)
def backbeat(volume=0.26, eq="pop", low=0.75, high=1.15):
    for bar in range(4):
        for beat in range(4):
            if beat == 1:
                hit = "snap"
            elif beat == 3:
                if bar == 3:
                    hit = "fill"
                else:
                    hit = "heavy"
            else:
                hit = "off"
            _ = hit


# --- Harmonic: stacked chord voices across phrases ---

@loop("chord_rave", interval=2.0)
def rave_stabs(volume=0.14, eq="edm", mid=0.9):
    for phrase in range(4):
        for voice in range(3):
            for harmonic in range(2):
                if phrase == 0:
                    if voice == 0:
                        chord = "root"
                    elif voice == 1:
                        chord = "fifth"
                    else:
                        chord = "octave"
                elif phrase == 2:
                    chord = "resolve"
                else:
                    chord = "hit"
                _ = chord


# --- Lead: phrase-based, slight air ---

@loop("lead_hoover", interval=4.0)
def hoover(volume=0.11, eq="edm", high=1.25):
    # classic rave swell
    # builds and drops
    for phrase in range(4):
        for step in range(3):
            if phrase in (0, 2):
                if step == 0:
                    motion = "attack"
                else:
                    motion = "hold"
                _ = motion


# --- Space: pure atmosphere, no code at all ---

@loop("shimmer_pad", interval=8.0)
def shimmer(volume=0.06, eq="acoustic", low=0.65):
    # wide hall reverb
    # slow harmonic drift
    # always underneath everything
    # never noticed until it stops
    # consonance without definition
    # air between the notes
    pass
