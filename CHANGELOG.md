# Changelog

## [0.1.3] - 2026-05-07

### Fixes

- Add `readme = "README.md"` to `pyproject.toml` so PyPI shows the project description

## [0.1.2] - 2026-05-07

### Features

- License changed to MIT + Commons Clause — personal use, modification, and live performances (including paid shows) are permitted; selling or commercially distributing the software itself is not

### Docs

- Add project homepage at `docs/index.html` with live demo animation and accurate engine-computed parameter values
- Add visualizer concept page at `docs/visualizer-concept.html` showing Canvas 2D animation synced to music parameters

## [0.1.1] - 2026-05-07

### Docs

- Add cross-language links between English and Japanese README and manual using absolute GitHub URLs
- Rename publish workflow file to `workflow.yml`

## [0.1.0] - 2026-05-07

### Features

- `pycodedj eval FILE::LOOP` — evaluate a loop block and send OSC parameters to SuperCollider; prints feedback (`cutoff`, `lfo_rate`, `reverb_mix`, `voice_count`) on success and exits with code 1 on failure
- `pycodedj watch FILE` — watch a file and re-evaluate all loops on every save; handles atomic saves (vim/Emacs rename-based writes) via `on_moved` and `on_created` in addition to `on_modified`; stops loops that are removed from the file between reloads
- OSC bridge sends `voice_count` first so SuperCollider creates synths before receiving parameter updates
- AST-based code analysis maps block nesting depth → filter cutoff, control-flow count → LFO rate, function count → polyphony voices, comment ratio → reverb depth
- `sc/synths.scd` — SuperCollider synth definitions with a single `OSCFunc(nil path)` handler dispatching all `/pycodedj/loop/<name>/<param>` messages
- `examples/demo.py` and `examples/club_set.py` bundled in the wheel as package data

### Docs

- `README.ja.md` and `README.md` with architecture overview, quick start, and OSC address reference
- `docs/manual.ja.md` and `docs/manual.md` — beginner-friendly full manual covering setup, watch mode, code-to-sound mapping, club set example, and troubleshooting
