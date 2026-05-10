// PyCodeDJ — SuperCollider synth definitions
// Run this file in the SuperCollider IDE before using pycodedj eval.

s.waitForBoot({
    // Shared controls:
    // cutoff = tone/brightness, lfoRate = pattern/modulation speed,
    // reverbMix = space, gate = fade out when a loop is restarted/stopped.
    // low/mid/high = simple per-loop 3-band EQ multipliers.
    ~applySimpleEQ = { |sig, eqLow = 1, eqMid = 1, eqHigh = 1|
        sig = BLowShelf.ar(sig, 120, 1, eqLow.clip(0.001, 2).ampdb);
        sig = BPeakEQ.ar(sig, 900, 1, eqMid.clip(0.001, 2).ampdb);
        sig = BHiShelf.ar(sig, 5000, 1, eqHigh.clip(0.001, 2).ampdb);
        Limiter.ar(sig, 0.98);
    };

    SynthDef(\pycodedj_bass_sub, {
        arg cutoff = 900, lfoRate = 1.0, reverbMix = 0.05, amp = 0.5, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, pumpTrig, freq, env, pump, click, sub, mid, sig;
        trig = Impulse.kr((lfoRate * 0.85).clip(1.2, 3.4));
        pumpTrig = Impulse.kr(2.133); // 128 BPM quarter-note pump
        freq = Demand.kr(trig, 0, Dseq([36, 36, 34, 36, 43, 36, 34, 31], inf)).midicps;
        env = Decay2.kr(trig, 0.002, 0.42);
        pump = 1 - (Decay2.kr(pumpTrig, 0.002, 0.18) * 0.55);
        click = Decay2.kr(trig, 0.001, 0.012) * WhiteNoise.ar(0.05);
        sub = SinOsc.ar(freq) * 0.95;
        mid = (Saw.ar(freq) * 0.12) + (Pulse.ar(freq * 0.5, 0.45) * 0.16);
        sig = (sub + mid + click) * env * pump;
        sig = RLPF.ar(sig.tanh, cutoff.clip(80, 1700), 0.22);
        env = EnvGen.kr(Env.asr(0.1, 1, 0.2), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.8)) * env * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_hat_engine, {
        arg cutoff = 6500, lfoRate = 1.5, reverbMix = 0.08, amp = 0.13, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, openTrig, closedEnv, openEnv, tone, sig, env;
        trig = Impulse.kr((lfoRate * 3.2).clip(6, 16));
        openTrig = PulseDivider.kr(trig, 4);
        closedEnv = Decay2.kr(trig, 0.001, 0.045);
        openEnv = Decay2.kr(openTrig, 0.002, 0.18);
        tone = cutoff.linlin(200, 4000, 5000, 14000).clip(5000, 14000);
        sig = HPF.ar(WhiteNoise.ar, tone * 0.7);
        sig = BPF.ar(sig, tone, 0.45) * (closedEnv + (openEnv * 0.75));
        env = EnvGen.kr(Env.asr(0.01, 1, 0.08), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.45), 0.25, 0.15) * env * amp;
        Out.ar(0, ~applySimpleEQ.value(Pan2.ar(sig, SinOsc.kr(0.13).range(-0.25, 0.25)), eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_clap_snap, {
        arg cutoff = 4200, lfoRate = 1.0, reverbMix = 0.18, amp = 0.18, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, flam, env, tone, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 0.65).clip(0.8, 1.4));
        flam = trig + DelayN.kr(trig, 0.04, 0.018) + DelayN.kr(trig, 0.06, 0.037);
        env = Decay2.kr(flam, 0.001, 0.13);
        tone = cutoff.clip(1800, 9000);
        sig = BPF.ar(WhiteNoise.ar(0.55), tone, 0.55) * env;
        sig = HPF.ar(sig, 900);
        gateEnv = EnvGen.kr(Env.asr(0.01, 1, 0.1), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.05, 0.5), 0.55, 0.25) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_stab_neon, {
        arg cutoff = 1200, lfoRate = 0.25, reverbMix = 0.25, amp = 0.14, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, root, freqs, env, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 0.75).clip(0.08, 1.5));
        root = Demand.kr(trig, 0, Dseq([48, 43, 46, 41], inf));
        freqs = (root + [0, 3, 7, 10]).midicps;
        env = Decay2.kr(trig, 0.01, 0.42);
        sig = Splay.ar(VarSaw.ar(freqs * [1, 1.004, 0.997, 1.006], 0, 0.42)) * 0.2;
        sig = RLPF.ar(sig, cutoff.clip(600, 4500), 0.32) * env;
        gateEnv = EnvGen.kr(Env.asr(0.05, 1, 0.25), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.8), 0.55, 0.35) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_lead_acid, {
        arg cutoff = 2100, lfoRate = 2.0, reverbMix = 0.12, amp = 0.15, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, note, freq, env, filterEnv, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 3).clip(2, 14));
        note = Demand.kr(trig, 0, Dseq([48, 51, 55, 58, 60, 58, 55, 51], inf));
        freq = Lag.kr(note.midicps, 0.045);
        env = Decay2.kr(trig, 0.003, 0.16);
        filterEnv = Decay2.kr(trig, 0.002, 0.12).range(0, 2600);
        sig = (Pulse.ar(freq, 0.48) * 0.65) + (Saw.ar(freq * 2) * 0.18);
        sig = RLPF.ar(sig, (cutoff + filterEnv).clip(500, 6200), 0.16).tanh * env;
        gateEnv = EnvGen.kr(Env.asr(0.02, 1, 0.12), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.55), 0.35, 0.22) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(Pan2.ar(sig, SinOsc.kr(0.21).range(-0.35, 0.35)), eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_air_warehouse, {
        arg cutoff = 700, lfoRate = 0.1, reverbMix = 0.6, amp = 0.08, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var sweep, dust, tail, sig, env;
        sweep = LFNoise1.kr(lfoRate.clip(0.03, 0.8)).range(0, 1).exprange(180, cutoff.clip(350, 3600));
        dust = Decay2.kr(Dust.kr((lfoRate * 5).clip(0.5, 7)), 0.02, 1.2) * PinkNoise.ar(0.08);
        tail = BPF.ar(PinkNoise.ar(0.22), sweep, 0.2);
        sig = HPF.ar(tail + dust, 140);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.25, 0.9), 0.92, 0.65);
        env = EnvGen.kr(Env.asr(1.5, 1, 2.0), gate, doneAction: 2);
        Out.ar(0, ~applySimpleEQ.value(Pan2.ar(sig * env * amp, LFNoise1.kr(0.08)), eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_kick_pulse, {
        arg cutoff = 900, lfoRate = 1.0, reverbMix = 0.02, amp = 0.28, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, env, pitch, sig, gateEnv;
        trig = Impulse.kr(lfoRate.clip(0.5, 4.0));
        env = Decay2.kr(trig, 0.001, 0.22);
        pitch = EnvGen.kr(Env([72, 38, 34], [0.025, 0.16], \exp), trig).midicps;
        sig = SinOsc.ar(pitch) * env;
        sig = (sig + (BPF.ar(WhiteNoise.ar(0.08), cutoff.clip(500, 4500), 0.5) * Decay2.kr(trig, 0.001, 0.02))).tanh;
        gateEnv = EnvGen.kr(Env.asr(0.01, 1, 0.08), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.25), 0.2, 0.1) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_kick_floor, {
        arg cutoff = 1100, lfoRate = 1.0, reverbMix = 0.08, amp = 0.72, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, bodyEnv, punchEnv, tailEnv, pitch, body, punch, tail, room, sig, gateEnv;
        trig = Impulse.kr(2.133); // 128 BPM four-on-the-floor
        bodyEnv = Decay2.kr(trig, 0.001, 0.28);
        punchEnv = Decay2.kr(trig, 0.001, 0.035);
        tailEnv = Decay2.kr(trig, 0.015, 0.62);
        pitch = EnvGen.kr(Env([92, 45, 34], [0.014, 0.18], \exp), trig).midicps;
        body = SinOsc.ar(pitch) * bodyEnv;
        punch = BPF.ar(WhiteNoise.ar(0.36), cutoff.clip(900, 7200), 0.24) * punchEnv;
        tail = LPF.ar(SinOsc.ar(45) + Saw.ar(22.5, 0.13), 145) * tailEnv * 0.36;
        room = FreeVerb.ar((body + tail) * 0.38, reverbMix.clip(0, 0.22), 0.48, 0.18);
        sig = (body + punch + tail + room).tanh;
        gateEnv = EnvGen.kr(Env.asr(0.005, 1, 0.12), gate, doneAction: 2);
        sig = Compander.ar(sig, sig, 0.5, 1, 0.28, 0.002, 0.06) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_fx_glitch, {
        arg cutoff = 5000, lfoRate = 2.0, reverbMix = 0.08, amp = 0.06, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, rate, env, sig, gateEnv;
        rate = (lfoRate * 8).clip(4, 28);
        trig = Dust.kr(rate);
        env = Decay2.kr(trig, 0.0005, 0.035);
        sig = HPF.ar(Hasher.ar(Sweep.ar(trig)), cutoff.clip(1200, 12000) * 0.5) * env;
        sig = Pan2.ar(sig, LFNoise1.kr(rate * 0.25).range(-0.8, 0.8));
        gateEnv = EnvGen.kr(Env.asr(0.005, 1, 0.05), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.5), 0.35, 0.2) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_pluck_soft, {
        arg cutoff = 1600, lfoRate = 1.0, reverbMix = 0.18, amp = 0.11, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, note, freq, env, sig, gateEnv;
        trig = Impulse.kr(lfoRate.clip(0.2, 6.0));
        note = Demand.kr(trig, 0, Dseq([60, 64, 67, 72, 67, 64], inf));
        freq = note.midicps;
        env = Decay2.kr(trig, 0.004, 0.28);
        sig = Mix.ar(Pulse.ar(freq * [1, 2.01], [0.42, 0.35], [0.55, 0.12])) * env;
        sig = RLPF.ar(sig, cutoff.clip(350, 7000), 0.38);
        gateEnv = EnvGen.kr(Env.asr(0.02, 1, 0.16), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.75), 0.45, 0.28) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_chord_dub, {
        arg cutoff = 1200, lfoRate = 0.5, reverbMix = 0.35, amp = 0.13, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, root, freqs, env, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 0.75).clip(0.08, 1.0));
        root = Demand.kr(trig, 0, Dseq([43, 46, 41, 48], inf));
        freqs = (root + [0, 7, 10, 14]).midicps;
        env = Decay2.kr(trig, 0.015, 0.55);
        sig = Splay.ar(Pulse.ar(freqs, 0.48)) * 0.16;
        sig = RLPF.ar(sig, cutoff.clip(500, 5000), 0.24) * env;
        gateEnv = EnvGen.kr(Env.asr(0.05, 1, 0.3), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.1, 0.85), 0.75, 0.45) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_pad_shimmer, {
        arg cutoff = 1400, lfoRate = 0.15, reverbMix = 0.55, amp = 0.08, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var drift, freqs, sig, gateEnv;
        drift = LFNoise1.kr(lfoRate.clip(0.03, 0.7)).range(-0.08, 0.08);
        freqs = ([55, 62, 67, 74] + drift).midicps;
        sig = Splay.ar(SinOsc.ar(freqs * [1, 1.002, 0.998, 1.004])) * 0.18;
        sig = RLPF.ar(sig, cutoff.clip(500, 5200), 0.42);
        gateEnv = EnvGen.kr(Env.asr(1.2, 1, 1.8), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.25, 0.95), 0.9, 0.55) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_kick_hard, {
        arg cutoff = 1300, lfoRate = 1.0, reverbMix = 0.04, amp = 0.76, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, bodyEnv, clickEnv, driveEnv, pitch, body, click, drive, sig, gateEnv;
        trig = Impulse.kr(2.133);
        bodyEnv = Decay2.kr(trig, 0.001, 0.34);
        clickEnv = Decay2.kr(trig, 0.001, 0.018);
        driveEnv = Decay2.kr(trig, 0.001, 0.09);
        pitch = EnvGen.kr(Env([105, 48, 36], [0.012, 0.13], \exp), trig).midicps;
        body = SinOsc.ar(pitch) * bodyEnv;
        click = HPF.ar(WhiteNoise.ar(0.42), cutoff.clip(1800, 9000)) * clickEnv;
        drive = (SinOsc.ar(54) + Pulse.ar(27, 0.42, 0.18)) * driveEnv;
        sig = (body + click + drive).tanh;
        sig = Compander.ar(sig, sig, 0.42, 1, 0.22, 0.001, 0.045);
        gateEnv = EnvGen.kr(Env.asr(0.005, 1, 0.1), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.18), 0.25, 0.12) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_bass_reese, {
        arg cutoff = 1100, lfoRate = 0.9, reverbMix = 0.08, amp = 0.28, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, note, freq, env, wobble, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 1.6).clip(0.8, 5.0));
        note = Demand.kr(trig, 0, Dseq([36, 36, 43, 34, 36, 31, 34, 36], inf));
        freq = Lag.kr(note.midicps, 0.055);
        env = Decay2.kr(trig, 0.008, 0.46);
        wobble = SinOsc.kr(lfoRate.clip(0.1, 4.5)).range(0.65, 1.2);
        sig = Splay.ar(Saw.ar(freq * [0.995, 1.004, 1.012], [0.26, 0.22, 0.18])) * 0.42;
        sig = RLPF.ar(sig, (cutoff * wobble).clip(120, 2600), 0.18);
        sig = (sig * 1.8).tanh * env;
        gateEnv = EnvGen.kr(Env.asr(0.06, 1, 0.18), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.38), 0.36, 0.2) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_bass_rumble, {
        arg cutoff = 500, lfoRate = 1.0, reverbMix = 0.28, amp = 0.34, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, kickEnv, rumbleEnv, pitch, kick, rumble, pump, sig, gateEnv;
        trig = Impulse.kr(2.133);
        kickEnv = Decay2.kr(trig, 0.001, 0.16);
        rumbleEnv = Decay2.kr(trig, 0.03, 0.82);
        pitch = EnvGen.kr(Env([75, 38, 32], [0.015, 0.14], \exp), trig).midicps;
        kick = SinOsc.ar(pitch) * kickEnv;
        rumble = LPF.ar((SinOsc.ar(45) + Saw.ar(22.5, 0.18)).tanh, cutoff.clip(90, 900)) * rumbleEnv;
        pump = 1 - (Decay2.kr(trig, 0.001, 0.22) * 0.45);
        sig = (kick + FreeVerb.ar(rumble, reverbMix.clip(0.15, 0.65), 0.9, 0.55)) * pump;
        gateEnv = EnvGen.kr(Env.asr(0.02, 1, 0.18), gate, doneAction: 2);
        Out.ar(0, ~applySimpleEQ.value((sig.tanh * gateEnv * amp) ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_hat_ride, {
        arg cutoff = 9000, lfoRate = 1.5, reverbMix = 0.18, amp = 0.1, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, env, tone, metal, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 1.6).clip(3, 12));
        env = Decay2.kr(trig, 0.002, 0.42);
        tone = cutoff.clip(5000, 14000);
        metal = Mix.ar(Pulse.ar([5300, 6110, 7240, 8110], 0.5)) * 0.08;
        sig = HPF.ar((WhiteNoise.ar(0.45) + metal), tone * 0.55);
        sig = BPF.ar(sig, tone, 0.34) * env;
        gateEnv = EnvGen.kr(Env.asr(0.01, 1, 0.12), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.55), 0.55, 0.24) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(Pan2.ar(sig, LFNoise1.kr(0.35).range(-0.45, 0.45)), eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_clap_snare, {
        arg cutoff = 3600, lfoRate = 1.0, reverbMix = 0.16, amp = 0.2, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, env, bodyEnv, noise, body, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 0.65).clip(0.8, 1.8));
        env = Decay2.kr(trig, 0.001, 0.18);
        bodyEnv = Decay2.kr(trig, 0.001, 0.08);
        noise = BPF.ar(WhiteNoise.ar(0.65), cutoff.clip(1400, 9000), 0.48) * env;
        body = SinOsc.ar(185) * bodyEnv * 0.45;
        sig = HPF.ar(noise + body, 120);
        gateEnv = EnvGen.kr(Env.asr(0.01, 1, 0.11), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.04, 0.55), 0.52, 0.24) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_chord_rave, {
        arg cutoff = 1800, lfoRate = 0.55, reverbMix = 0.28, amp = 0.15, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, root, freqs, env, detune, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 1.15).clip(0.15, 2.2));
        root = Demand.kr(trig, 0, Dseq([48, 51, 46, 43], inf));
        freqs = (root + [0, 7, 10, 15]).midicps;
        detune = [0.996, 1.003, 1.007, 0.992];
        env = Decay2.kr(trig, 0.004, 0.34);
        sig = Splay.ar(Saw.ar(freqs * detune)) * 0.18;
        sig = RLPF.ar((sig * 1.7).tanh, cutoff.clip(650, 6200), 0.2) * env;
        gateEnv = EnvGen.kr(Env.asr(0.03, 1, 0.22), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.08, 0.75), 0.62, 0.34) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_lead_hoover, {
        arg cutoff = 2400, lfoRate = 1.2, reverbMix = 0.18, amp = 0.13, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, note, freq, env, detune, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 1.8).clip(0.6, 7.0));
        note = Demand.kr(trig, 0, Dseq([60, 63, 58, 55, 60, 67, 65, 63], inf));
        freq = Lag.kr(note.midicps, 0.08);
        env = Decay2.kr(trig, 0.008, 0.34);
        detune = LFNoise1.kr(4 ! 4).range(0.986, 1.014);
        sig = Splay.ar(Saw.ar(freq * [0.5, 0.997, 1.006, 2.01] * detune)) * 0.2;
        sig = RLPF.ar((sig * 1.5).tanh, cutoff.clip(700, 7600), 0.24) * env;
        gateEnv = EnvGen.kr(Env.asr(0.04, 1, 0.2), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.04, 0.65), 0.48, 0.24) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_fx_drop, {
        arg cutoff = 1600, lfoRate = 0.25, reverbMix = 0.55, amp = 0.16, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, env, thump, noise, tail, sig, gateEnv;
        trig = Impulse.kr(lfoRate.clip(0.05, 1.0));
        env = Decay2.kr(trig, 0.001, 1.2);
        thump = SinOsc.ar(EnvGen.kr(Env([62, 32], [0.18], \exp), trig).midicps) * Decay2.kr(trig, 0.001, 0.45);
        noise = LPF.ar(PinkNoise.ar(0.34), cutoff.clip(400, 5000)) * env;
        tail = FreeVerb.ar(noise + thump, reverbMix.clip(0.25, 0.9), 0.92, 0.62);
        sig = (thump + tail).tanh;
        gateEnv = EnvGen.kr(Env.asr(0.02, 1, 0.35), gate, doneAction: 2);
        Out.ar(0, ~applySimpleEQ.value((sig ! 2) * gateEnv * amp, eqLow, eqMid, eqHigh));
    }).add;

    // ── New DJ sounds ──────────────────────────────────────────────────

    // tom_drum: floor tom, MIDI pitch sweep, noise transient
    SynthDef(\pycodedj_tom_drum, {
        arg cutoff = 1200, lfoRate = 1.0, reverbMix = 0.14, amp = 0.25, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, pitch, bodyEnv, transEnv, body, trans, sig, gateEnv;
        trig = Impulse.kr(lfoRate.clip(0.5, 4.0));
        pitch = EnvGen.kr(Env([65, 38, 32], [0.018, 0.22], \exp), trig).midicps;
        bodyEnv = Decay2.kr(trig, 0.001, 0.32);
        transEnv = Decay2.kr(trig, 0.001, 0.04);
        body = SinOsc.ar(pitch) * bodyEnv;
        trans = BPF.ar(WhiteNoise.ar(0.18), cutoff.clip(300, 4000), 0.5) * transEnv;
        sig = (body + trans).tanh;
        gateEnv = EnvGen.kr(Env.asr(0.01, 1, 0.1), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.55), 0.45, 0.22) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    // snare_roll: rapid triggered noise roll, rate driven by lfoRate
    SynthDef(\pycodedj_snare_roll, {
        arg cutoff = 4000, lfoRate = 2.0, reverbMix = 0.22, amp = 0.2, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var rate, trig, env, sig, gateEnv;
        rate = (lfoRate * 8).clip(8, 32);
        trig = Impulse.kr(rate);
        env = Decay2.kr(trig, 0.001, max(1 / rate * 0.7, 0.018));
        sig = BPF.ar(WhiteNoise.ar(0.7), cutoff.clip(1500, 8000), 0.5) * env;
        sig = HPF.ar(sig, 200);
        gateEnv = EnvGen.kr(Env.asr(0.01, 1, 0.08), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.5), 0.5, 0.22) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    // crash_noise: metallic crash cymbal with long tail
    SynthDef(\pycodedj_crash_noise, {
        arg cutoff = 8000, lfoRate = 0.5, reverbMix = 0.35, amp = 0.22, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, env, tone, metal, sig, gateEnv;
        trig = Impulse.kr(lfoRate.clip(0.1, 2.0));
        env = Decay2.kr(trig, 0.003, 1.4);
        tone = cutoff.clip(3000, 16000);
        metal = Mix.ar(Pulse.ar([4100, 5040, 6280, 8320], 0.5)) * 0.06;
        sig = HPF.ar(WhiteNoise.ar(0.6) + metal, 2500);
        sig = BPF.ar(sig, tone, 0.65) * env;
        gateEnv = EnvGen.kr(Env.asr(0.01, 1, 0.35), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.1, 0.8), 0.75, 0.45) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    // bass_acid: classic 303-style acid bass, low register, squelchy filter
    SynthDef(\pycodedj_bass_acid, {
        arg cutoff = 1200, lfoRate = 3.0, reverbMix = 0.05, amp = 0.22, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, note, freq, acc, env, filterEnv, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 2).clip(2, 16));
        note = Demand.kr(trig, 0, Dseq([36, 36, 43, 36, 38, 34, 36, 31], inf));
        freq = Lag.kr(note.midicps, 0.025);
        acc = Demand.kr(trig, 0, Dseq([1, 0, 0, 1, 0, 1, 0, 0], inf));
        env = Decay2.kr(trig, 0.002, 0.12 + (acc * 0.08));
        filterEnv = Decay2.kr(trig, 0.003, 0.08 + (acc * 0.14)).range(0, 4200);
        sig = Saw.ar(freq) + (Pulse.ar(freq, 0.5) * 0.22);
        sig = RLPF.ar(sig.tanh, (cutoff + filterEnv).clip(300, 6200), 0.13) * env;
        gateEnv = EnvGen.kr(Env.asr(0.008, 1, 0.1), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.3), 0.22, 0.12) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(Pan2.ar(sig, 0), eqLow, eqMid, eqHigh));
    }).add;

    // stab_saw: classic detuned saw chord stab, tight attack
    SynthDef(\pycodedj_stab_saw, {
        arg cutoff = 2400, lfoRate = 1.0, reverbMix = 0.18, amp = 0.2, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, root, freqs, env, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 0.5).clip(0.2, 2.0));
        root = Demand.kr(trig, 0, Dseq([48, 48, 55, 53], inf));
        freqs = (root + [0, 4, 7]).midicps;
        env = Decay2.kr(trig, 0.001, 0.16);
        sig = Splay.ar(Saw.ar(freqs * [0.997, 1.001, 1.005])) * 0.24;
        sig = RLPF.ar((sig * 2.2).tanh, cutoff.clip(800, 7200), 0.17) * env;
        gateEnv = EnvGen.kr(Env.asr(0.005, 1, 0.1), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.65), 0.55, 0.28) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig, eqLow, eqMid, eqHigh));
    }).add;

    // fx_riser: noise sweep that climbs over 8s — restart synth to retrigger
    SynthDef(\pycodedj_fx_riser, {
        arg cutoff = 1000, lfoRate = 0.5, reverbMix = 0.35, amp = 0.15, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var startPitch, endPitch, sweep, env, sig, gateEnv;
        startPitch = cutoff.clip(120, 2000) * 0.2;
        endPitch = cutoff.clip(120, 2000) * 5;
        sweep = XLine.kr(startPitch, endPitch, 8.0);
        env = Line.kr(0.0, 1.0, 7.5);
        sig = HPF.ar(PinkNoise.ar(0.55), sweep);
        sig = BPF.ar(sig + (SinOsc.ar(sweep * 0.5) * 0.22), sweep, 0.55) * env;
        gateEnv = EnvGen.kr(Env.asr(0.5, 1, 1.5), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.1, 0.85), 0.75, 0.45) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    // bell_rave: metallic FM bell with classic rave inharmonic ratios
    SynthDef(\pycodedj_bell_rave, {
        arg cutoff = 3000, lfoRate = 1.0, reverbMix = 0.38, amp = 0.12, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, note, freq, env, partials, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 0.75).clip(0.15, 3.0));
        note = Demand.kr(trig, 0, Dseq([72, 75, 79, 84], inf));
        freq = note.midicps;
        env = Decay2.kr(trig, 0.002, 1.2);
        // inharmonic FM bell partials: [ratio, amplitude]
        partials = Mix.ar([
            SinOsc.ar(freq * 1.0)     * 0.50,
            SinOsc.ar(freq * 2.756)   * 0.30,
            SinOsc.ar(freq * 5.404)   * 0.15,
            SinOsc.ar(freq * 8.933)   * 0.08,
            SinOsc.ar(freq * 13.876)  * 0.04
        ]);
        sig = RLPF.ar(partials * env, cutoff.clip(1000, 14000), 0.5);
        gateEnv = EnvGen.kr(Env.asr(0.01, 1, 0.3), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.1, 0.85), 0.72, 0.42) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    // chord_organ: Hammond-style drawbar organ with harmonic stack
    SynthDef(\pycodedj_chord_organ, {
        arg cutoff = 2200, lfoRate = 0.5, reverbMix = 0.22, amp = 0.14, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, root, freq, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 0.5).clip(0.1, 1.5));
        root = Demand.kr(trig, 0, Dseq([48, 51, 46, 43], inf));
        freq = Lag.kr(root.midicps, 0.08);
        // drawbar harmonics: 16' 8' 5-1/3' 4' 2-2/3' 2'
        sig = Mix.ar([
            SinOsc.ar(freq * 0.5)  * 0.60,
            SinOsc.ar(freq * 1.0)  * 0.90,
            SinOsc.ar(freq * 1.5)  * 0.50,
            SinOsc.ar(freq * 2.0)  * 0.40,
            SinOsc.ar(freq * 3.0)  * 0.25,
            SinOsc.ar(freq * 4.0)  * 0.15
        ]) * 0.12;
        sig = RLPF.ar(sig.tanh, cutoff.clip(600, 6000), 0.35);
        gateEnv = EnvGen.kr(Env.asr(0.04, 1, 0.25), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.7), 0.55, 0.32) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    // arp_synth: fast arpeggio, filter opens with each trigger
    SynthDef(\pycodedj_arp_synth, {
        arg cutoff = 2000, lfoRate = 2.0, reverbMix = 0.18, amp = 0.14, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, note, freq, env, filterEnv, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 4).clip(4, 20));
        note = Demand.kr(trig, 0, Dseq([60, 64, 67, 72, 74, 72, 67, 64], inf));
        freq = Lag.kr(note.midicps, 0.005);
        env = Decay2.kr(trig, 0.003, 0.12);
        filterEnv = Decay2.kr(trig, 0.003, 0.08).range(0, 2200);
        sig = (Saw.ar(freq) * 0.55) + (Pulse.ar(freq * 2, 0.3) * 0.18);
        sig = RLPF.ar(sig, (cutoff + filterEnv).clip(400, 8000), 0.22) * env;
        gateEnv = EnvGen.kr(Env.asr(0.02, 1, 0.12), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.65), 0.48, 0.28) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(Pan2.ar(sig, SinOsc.kr(0.15).range(-0.4, 0.4)), eqLow, eqMid, eqHigh));
    }).add;

    // vox_ahh: formant-based vocal pad, three formant filters
    SynthDef(\pycodedj_vox_ahh, {
        arg cutoff = 1200, lfoRate = 0.3, reverbMix = 0.28, amp = 0.1, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, note, freq, fScale, f1, f2, f3, env, raw, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 0.5).clip(0.08, 2.0));
        note = Demand.kr(trig, 0, Dseq([48, 51, 55, 58], inf));
        freq = Lag.kr(note.midicps, 0.15);
        fScale = cutoff.linlin(200, 4000, 0.5, 2.0);
        f1 = (800 * fScale).clip(200, 6000);
        f2 = (1200 * fScale).clip(400, 9000);
        f3 = (2500 * fScale).clip(800, 14000);
        env = Decay2.kr(trig, 0.05, 0.55);
        raw = Saw.ar(freq) + (Saw.ar(freq * 2) * 0.15);
        sig = BPF.ar(raw, f1, 0.08) + BPF.ar(raw, f2, 0.06) + BPF.ar(raw, f3, 0.04);
        sig = sig * env;
        gateEnv = EnvGen.kr(Env.asr(0.12, 1, 0.3), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.08, 0.75), 0.6, 0.35) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    // ── Extended sound bank: 60 named sounds total ─────────────────────

    SynthDef(\pycodedj_kick_soft, {
        arg cutoff = 1000, lfoRate = 1.0, reverbMix = 0.04, amp = 0.46, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, env, pitch, body, sig, gateEnv;
        trig = Impulse.kr(lfoRate.clip(0.4, 4.0));
        env = Decay2.kr(trig, 0.002, 0.34);
        pitch = EnvGen.kr(Env([70, 42, 35], [0.02, 0.18], \exp), trig).midicps;
        body = SinOsc.ar(pitch) * env;
        sig = LPF.ar(body + (PinkNoise.ar(0.03) * Decay2.kr(trig, 0.001, 0.018)), cutoff.clip(220, 3200)).tanh;
        gateEnv = EnvGen.kr(Env.asr(0.01, 1, 0.1), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.22), 0.22, 0.12) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_kick_909, {
        arg cutoff = 1400, lfoRate = 1.0, reverbMix = 0.05, amp = 0.62, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, bodyEnv, clickEnv, pitch, sig, gateEnv;
        trig = Impulse.kr(lfoRate.clip(0.4, 4.0));
        bodyEnv = Decay2.kr(trig, 0.001, 0.52);
        clickEnv = Decay2.kr(trig, 0.001, 0.012);
        pitch = EnvGen.kr(Env([82, 46, 37], [0.018, 0.22], \exp), trig).midicps;
        sig = (SinOsc.ar(pitch) * bodyEnv) + (HPF.ar(WhiteNoise.ar(0.22), cutoff.clip(1200, 9000)) * clickEnv);
        gateEnv = EnvGen.kr(Env.asr(0.005, 1, 0.12), gate, doneAction: 2);
        sig = Compander.ar(sig.tanh, sig, 0.45, 1, 0.25, 0.002, 0.06) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_kick_click, {
        arg cutoff = 3200, lfoRate = 1.0, reverbMix = 0.02, amp = 0.42, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, bodyEnv, clickEnv, pitch, sig, gateEnv;
        trig = Impulse.kr(lfoRate.clip(0.5, 6.0));
        bodyEnv = Decay2.kr(trig, 0.001, 0.2);
        clickEnv = Decay2.kr(trig, 0.0005, 0.02);
        pitch = EnvGen.kr(Env([98, 48, 39], [0.01, 0.12], \exp), trig).midicps;
        sig = (SinOsc.ar(pitch) * bodyEnv) + (BPF.ar(WhiteNoise.ar(0.5), cutoff.clip(1800, 10000), 0.32) * clickEnv);
        gateEnv = EnvGen.kr(Env.asr(0.005, 1, 0.08), gate, doneAction: 2);
        Out.ar(0, ~applySimpleEQ.value((sig.tanh * gateEnv * amp) ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_bass_pluck, {
        arg cutoff = 900, lfoRate = 1.0, reverbMix = 0.06, amp = 0.26, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, note, freq, env, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 2).clip(1, 10));
        note = Demand.kr(trig, 0, Dseq([36, 43, 34, 39, 36, 31, 34, 36], inf));
        freq = Lag.kr(note.midicps, 0.015);
        env = Decay2.kr(trig, 0.002, 0.18);
        sig = (Pulse.ar(freq, 0.38) + Saw.ar(freq * 0.5, 0.25)) * env;
        sig = RLPF.ar(sig.tanh, cutoff.clip(120, 2400), 0.2);
        gateEnv = EnvGen.kr(Env.asr(0.01, 1, 0.1), gate, doneAction: 2);
        Out.ar(0, ~applySimpleEQ.value((sig * gateEnv * amp) ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_bass_fm, {
        arg cutoff = 850, lfoRate = 1.0, reverbMix = 0.05, amp = 0.24, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, note, freq, env, mod, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 1.5).clip(0.8, 8));
        note = Demand.kr(trig, 0, Dseq([36, 36, 31, 34, 39, 36, 34, 31], inf));
        freq = Lag.kr(note.midicps, 0.03);
        env = Decay2.kr(trig, 0.003, 0.3);
        mod = SinOsc.ar(freq * 2.01) * (freq * 1.8) * env;
        sig = SinOsc.ar(freq + mod) * env;
        sig = RLPF.ar((sig * 2).tanh, cutoff.clip(160, 2400), 0.32);
        gateEnv = EnvGen.kr(Env.asr(0.02, 1, 0.12), gate, doneAction: 2);
        Out.ar(0, ~applySimpleEQ.value((sig * gateEnv * amp) ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_bass_mono, {
        arg cutoff = 700, lfoRate = 1.0, reverbMix = 0.03, amp = 0.28, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, note, freq, env, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 1.25).clip(0.5, 6));
        note = Demand.kr(trig, 0, Dseq([36, 38, 34, 31, 36, 43, 38, 34], inf));
        freq = Lag.kr(note.midicps, 0.06);
        env = Decay2.kr(trig, 0.008, 0.46);
        sig = (Saw.ar(freq) * 0.5) + (SinOsc.ar(freq * 0.5) * 0.7);
        sig = RLPF.ar(sig.tanh, cutoff.clip(90, 1800), 0.24) * env;
        gateEnv = EnvGen.kr(Env.asr(0.03, 1, 0.16), gate, doneAction: 2);
        Out.ar(0, ~applySimpleEQ.value((sig * gateEnv * amp) ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_bass_wobble, {
        arg cutoff = 1000, lfoRate = 1.0, reverbMix = 0.08, amp = 0.25, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, note, freq, env, wob, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 0.75).clip(0.3, 4));
        note = Demand.kr(trig, 0, Dseq([36, 31, 34, 36], inf));
        freq = Lag.kr(note.midicps, 0.08);
        env = Decay2.kr(trig, 0.01, 0.8);
        wob = SinOsc.kr((lfoRate * 2).clip(0.2, 8)).range(180, cutoff.clip(500, 2600));
        sig = Splay.ar(Saw.ar(freq * [0.997, 1.003])) * 0.5;
        sig = RLPF.ar((sig * 2.4).tanh, wob, 0.16) * env;
        gateEnv = EnvGen.kr(Env.asr(0.04, 1, 0.18), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.35), 0.35, 0.18) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_rim_shot, {
        arg cutoff = 3500, lfoRate = 1.0, reverbMix = 0.08, amp = 0.18, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, env, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 1.5).clip(0.8, 8));
        env = Decay2.kr(trig, 0.001, 0.055);
        sig = (SinOsc.ar(1800) * 0.45) + BPF.ar(WhiteNoise.ar(0.32), cutoff.clip(1800, 9000), 0.25);
        gateEnv = EnvGen.kr(Env.asr(0.005, 1, 0.06), gate, doneAction: 2);
        sig = FreeVerb.ar(sig * env, reverbMix.clip(0, 0.35), 0.35, 0.16) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_cowbell, {
        arg cutoff = 4600, lfoRate = 1.0, reverbMix = 0.12, amp = 0.16, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, env, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 1.25).clip(0.6, 7));
        env = Decay2.kr(trig, 0.001, 0.18);
        sig = Pulse.ar([540, 800], 0.45).sum * 0.26;
        sig = BPF.ar(sig, cutoff.clip(900, 7000), 0.45) * env;
        gateEnv = EnvGen.kr(Env.asr(0.005, 1, 0.08), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.45), 0.42, 0.22) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_perc_blip, {
        arg cutoff = 2200, lfoRate = 1.0, reverbMix = 0.12, amp = 0.13, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, note, freq, env, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 3).clip(2, 16));
        note = Demand.kr(trig, 0, Dseq([72, 75, 67, 79, 70, 74], inf));
        freq = note.midicps;
        env = Decay2.kr(trig, 0.001, 0.06);
        sig = SinOsc.ar(freq + (SinOsc.ar(freq * 3) * 80 * env)) * env;
        sig = HPF.ar(sig, cutoff.clip(500, 6000) * 0.3);
        gateEnv = EnvGen.kr(Env.asr(0.005, 1, 0.06), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.55), 0.38, 0.24) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(Pan2.ar(sig, LFNoise1.kr(2).range(-0.35, 0.35)), eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_shaker_loop, {
        arg cutoff = 7600, lfoRate = 1.5, reverbMix = 0.08, amp = 0.08, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, accent, env, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 4).clip(4, 20));
        accent = Demand.kr(trig, 0, Dseq([1.0, 0.45, 0.65, 0.4], inf));
        env = Decay2.kr(trig, 0.001, 0.05) * accent;
        sig = HPF.ar(WhiteNoise.ar(0.55), cutoff.clip(3000, 12000) * 0.6) * env;
        gateEnv = EnvGen.kr(Env.asr(0.01, 1, 0.08), gate, doneAction: 2);
        Out.ar(0, ~applySimpleEQ.value(Pan2.ar(sig * gateEnv * amp, SinOsc.kr(0.25).range(-0.25, 0.25)), eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_tick_metal, {
        arg cutoff = 6800, lfoRate = 2.0, reverbMix = 0.1, amp = 0.09, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, env, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 5).clip(3, 24));
        env = Decay2.kr(trig, 0.0005, 0.035);
        sig = Mix.ar(SinOsc.ar([3210, 4890, 7340])) * 0.09;
        sig = BPF.ar(sig + WhiteNoise.ar(0.08), cutoff.clip(3000, 12000), 0.22) * env;
        gateEnv = EnvGen.kr(Env.asr(0.005, 1, 0.05), gate, doneAction: 2);
        Out.ar(0, ~applySimpleEQ.value(Pan2.ar(sig * gateEnv * amp, LFNoise1.kr(3).range(-0.6, 0.6)), eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_wood_block, {
        arg cutoff = 1800, lfoRate = 1.0, reverbMix = 0.1, amp = 0.14, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, env, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 1.7).clip(0.8, 9));
        env = Decay2.kr(trig, 0.001, 0.09);
        sig = BPF.ar(WhiteNoise.ar(0.4), cutoff.clip(700, 4200), 0.16) + (SinOsc.ar(820) * 0.12);
        gateEnv = EnvGen.kr(Env.asr(0.005, 1, 0.07), gate, doneAction: 2);
        sig = FreeVerb.ar(sig * env, reverbMix.clip(0, 0.4), 0.35, 0.16) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_pad_minor, {
        arg cutoff = 1300, lfoRate = 0.2, reverbMix = 0.48, amp = 0.08, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var drift, freqs, sig, gateEnv;
        drift = LFNoise1.kr(lfoRate.clip(0.03, 0.8)).range(-0.06, 0.06);
        freqs = ([48, 51, 55, 62] + drift).midicps;
        sig = Splay.ar(VarSaw.ar(freqs * [0.998, 1.002, 1.005, 0.996], 0, 0.45)) * 0.18;
        sig = RLPF.ar(sig, cutoff.clip(400, 5200), 0.38);
        gateEnv = EnvGen.kr(Env.asr(1.0, 1, 1.5), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.2, 0.92), 0.85, 0.52) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_chord_deep, {
        arg cutoff = 900, lfoRate = 0.4, reverbMix = 0.35, amp = 0.12, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, root, freqs, env, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 0.5).clip(0.08, 1.2));
        root = Demand.kr(trig, 0, Dseq([43, 46, 41, 38], inf));
        freqs = (root + [0, 7, 10, 14]).midicps;
        env = Decay2.kr(trig, 0.03, 0.9);
        sig = Splay.ar(Pulse.ar(freqs, 0.48)) * 0.14;
        sig = RLPF.ar(sig.tanh, cutoff.clip(280, 3200), 0.2) * env;
        gateEnv = EnvGen.kr(Env.asr(0.08, 1, 0.35), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.12, 0.85), 0.78, 0.5) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_chord_glass, {
        arg cutoff = 3600, lfoRate = 0.5, reverbMix = 0.42, amp = 0.1, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, root, freqs, env, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 0.7).clip(0.1, 2.0));
        root = Demand.kr(trig, 0, Dseq([60, 64, 67, 55], inf));
        freqs = (root + [0, 4, 7, 11]).midicps;
        env = Decay2.kr(trig, 0.006, 1.1);
        sig = Splay.ar(SinOsc.ar(freqs * [1, 2.01, 3.01, 4.02])) * 0.13;
        sig = RLPF.ar(sig * env, cutoff.clip(1200, 11000), 0.48);
        gateEnv = EnvGen.kr(Env.asr(0.02, 1, 0.4), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.15, 0.9), 0.82, 0.55) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_pad_warm, {
        arg cutoff = 1200, lfoRate = 0.15, reverbMix = 0.5, amp = 0.08, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var freqs, sig, gateEnv;
        freqs = [48, 55, 60, 64].midicps;
        sig = Splay.ar(Saw.ar(freqs * LFNoise1.kr(0.2 ! 4).range(0.997, 1.003))) * 0.12;
        sig = RLPF.ar(sig, cutoff.clip(300, 4200), 0.45);
        gateEnv = EnvGen.kr(Env.asr(1.5, 1, 2.0), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.2, 0.95), 0.88, 0.6) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_pad_string, {
        arg cutoff = 1800, lfoRate = 0.2, reverbMix = 0.45, amp = 0.08, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var freqs, trem, sig, gateEnv;
        freqs = [55, 62, 67, 71].midicps;
        trem = SinOsc.kr(lfoRate.clip(0.05, 2.0)).range(0.75, 1.0);
        sig = Splay.ar(VarSaw.ar(freqs * [0.996, 1.002, 1.006, 0.999], 0, 0.28)) * 0.14 * trem;
        sig = BHiShelf.ar(RLPF.ar(sig, cutoff.clip(500, 6000), 0.5), 5000, 1, -4);
        gateEnv = EnvGen.kr(Env.asr(1.2, 1, 1.6), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.18, 0.9), 0.86, 0.55) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_pad_choir, {
        arg cutoff = 1400, lfoRate = 0.2, reverbMix = 0.5, amp = 0.08, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var freqs, raw, sig, gateEnv;
        freqs = [48, 55, 60].midicps;
        raw = Splay.ar(Saw.ar(freqs * [0.998, 1.002, 1.006])) * 0.16;
        sig = BPF.ar(raw, cutoff.clip(500, 4000) * 0.65, 0.08) + BPF.ar(raw, cutoff.clip(500, 4000), 0.06) + BPF.ar(raw, cutoff.clip(500, 4000) * 1.9, 0.05);
        gateEnv = EnvGen.kr(Env.asr(1.1, 1, 1.6), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.2, 0.95), 0.88, 0.58) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_lead_square, {
        arg cutoff = 2200, lfoRate = 1.5, reverbMix = 0.16, amp = 0.12, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, note, freq, env, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 2).clip(1, 12));
        note = Demand.kr(trig, 0, Dseq([60, 63, 67, 70, 72, 70, 67, 63], inf));
        freq = Lag.kr(note.midicps, 0.02);
        env = Decay2.kr(trig, 0.004, 0.22);
        sig = Pulse.ar(freq, 0.5) * env;
        sig = RLPF.ar(sig, cutoff.clip(500, 7600), 0.28);
        gateEnv = EnvGen.kr(Env.asr(0.01, 1, 0.12), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.6), 0.45, 0.28) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(Pan2.ar(sig, SinOsc.kr(0.2).range(-0.3, 0.3)), eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_lead_fm, {
        arg cutoff = 3000, lfoRate = 1.5, reverbMix = 0.18, amp = 0.12, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, note, freq, env, mod, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 2.2).clip(1, 14));
        note = Demand.kr(trig, 0, Dseq([72, 74, 75, 79, 82, 79, 75, 74], inf));
        freq = Lag.kr(note.midicps, 0.015);
        env = Decay2.kr(trig, 0.003, 0.2);
        mod = SinOsc.ar(freq * 2.5) * (freq * 0.8) * env;
        sig = SinOsc.ar(freq + mod) * env;
        sig = RLPF.ar(sig, cutoff.clip(800, 10000), 0.42);
        gateEnv = EnvGen.kr(Env.asr(0.01, 1, 0.12), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.65), 0.5, 0.3) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(Pan2.ar(sig, LFNoise1.kr(0.8).range(-0.35, 0.35)), eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_lead_chip, {
        arg cutoff = 4200, lfoRate = 2.0, reverbMix = 0.08, amp = 0.1, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, note, freq, env, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 4).clip(4, 22));
        note = Demand.kr(trig, 0, Dseq([72, 79, 76, 84, 79, 76, 74, 71], inf));
        freq = note.midicps;
        env = Decay2.kr(trig, 0.001, 0.08);
        sig = Pulse.ar(freq, 0.5) * env;
        sig = HPF.ar(RLPF.ar(sig, cutoff.clip(1200, 10000), 0.35), 300);
        gateEnv = EnvGen.kr(Env.asr(0.005, 1, 0.06), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.42), 0.32, 0.18) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(Pan2.ar(sig, LFNoise1.kr(3).range(-0.5, 0.5)), eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_lead_saw, {
        arg cutoff = 2600, lfoRate = 1.5, reverbMix = 0.16, amp = 0.13, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, note, freq, env, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 1.8).clip(0.8, 10));
        note = Demand.kr(trig, 0, Dseq([60, 62, 67, 70, 72, 70, 67, 62], inf));
        freq = Lag.kr(note.midicps, 0.04);
        env = Decay2.kr(trig, 0.006, 0.3);
        sig = Splay.ar(Saw.ar(freq * [0.996, 1.004, 2.002])) * 0.22;
        sig = RLPF.ar((sig * 1.8).tanh, cutoff.clip(700, 9000), 0.22) * env;
        gateEnv = EnvGen.kr(Env.asr(0.02, 1, 0.14), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.65), 0.46, 0.26) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_lead_whistle, {
        arg cutoff = 5200, lfoRate = 1.0, reverbMix = 0.22, amp = 0.09, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, note, freq, env, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 1.4).clip(0.4, 8));
        note = Demand.kr(trig, 0, Dseq([79, 82, 84, 86, 84, 82, 79, 74], inf));
        freq = Lag.kr(note.midicps, 0.08);
        env = Decay2.kr(trig, 0.02, 0.42);
        sig = SinOsc.ar(freq + (SinOsc.kr(5.2).range(-3, 3))) * env;
        sig = BPF.ar(sig, cutoff.clip(1800, 9000), 0.35);
        gateEnv = EnvGen.kr(Env.asr(0.03, 1, 0.18), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.05, 0.72), 0.58, 0.34) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(Pan2.ar(sig, SinOsc.kr(0.17).range(-0.4, 0.4)), eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_fx_down, {
        arg cutoff = 5200, lfoRate = 0.25, reverbMix = 0.42, amp = 0.14, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, env, sweep, sig, gateEnv;
        trig = Impulse.kr(lfoRate.clip(0.05, 1.0));
        env = Decay2.kr(trig, 0.003, 2.5);
        sweep = EnvGen.kr(Env([cutoff.clip(800, 9000), 140], [2.2], \exp), trig);
        sig = BPF.ar(PinkNoise.ar(0.55), sweep, 0.45) * env;
        gateEnv = EnvGen.kr(Env.asr(0.02, 1, 0.6), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.1, 0.9), 0.86, 0.55) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_fx_zap, {
        arg cutoff = 2400, lfoRate = 1.0, reverbMix = 0.18, amp = 0.14, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, env, pitch, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 1.2).clip(0.4, 6));
        env = Decay2.kr(trig, 0.001, 0.12);
        pitch = EnvGen.kr(Env([1800, 180], [0.09], \exp), trig);
        sig = SinOsc.ar(pitch) * env;
        sig = (sig + (BPF.ar(WhiteNoise.ar(0.12), cutoff.clip(700, 6000), 0.4) * env)).tanh;
        gateEnv = EnvGen.kr(Env.asr(0.005, 1, 0.08), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.55), 0.45, 0.25) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(Pan2.ar(sig, LFNoise1.kr(1).range(-0.45, 0.45)), eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_fx_noise, {
        arg cutoff = 1800, lfoRate = 0.5, reverbMix = 0.35, amp = 0.15, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, env, sig, gateEnv;
        trig = Impulse.kr(lfoRate.clip(0.1, 3.0));
        env = Decay2.kr(trig, 0.001, 0.55);
        sig = LPF.ar(PinkNoise.ar(0.7), cutoff.clip(300, 6000)) * env;
        sig = HPF.ar(sig, 80);
        gateEnv = EnvGen.kr(Env.asr(0.01, 1, 0.2), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.05, 0.8), 0.72, 0.42) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_fx_laser, {
        arg cutoff = 3600, lfoRate = 1.0, reverbMix = 0.14, amp = 0.12, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var trig, env, pitch, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 1.5).clip(0.6, 8));
        env = Decay2.kr(trig, 0.001, 0.16);
        pitch = EnvGen.kr(Env([360, 2200, 620], [0.03, 0.1], \exp), trig);
        sig = SinOsc.ar(pitch) * env;
        sig = BPF.ar(sig + (WhiteNoise.ar(0.08) * env), cutoff.clip(900, 9000), 0.45);
        gateEnv = EnvGen.kr(Env.asr(0.005, 1, 0.08), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.55), 0.4, 0.22) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(Pan2.ar(sig, LFNoise1.kr(2).range(-0.55, 0.55)), eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_fx_vinyl, {
        arg cutoff = 3000, lfoRate = 0.4, reverbMix = 0.18, amp = 0.07, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var crackle, dust, sig, gateEnv;
        crackle = Crackle.ar(1.92) * 0.08;
        dust = Decay2.kr(Dust.kr((lfoRate * 16).clip(2, 24)), 0.001, 0.03) * WhiteNoise.ar(0.25);
        sig = HPF.ar(LPF.ar(PinkNoise.ar(0.12) + crackle + dust, cutoff.clip(1000, 7000)), 180);
        gateEnv = EnvGen.kr(Env.asr(0.2, 1, 0.4), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.5), 0.45, 0.24) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_drone_space, {
        arg cutoff = 900, lfoRate = 0.08, reverbMix = 0.65, amp = 0.08, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var drift, freqs, sig, gateEnv;
        drift = LFNoise1.kr(lfoRate.clip(0.02, 0.4) ! 4).range(-0.12, 0.12);
        freqs = ([36, 43, 50, 55] + drift).midicps;
        sig = Splay.ar(SinOsc.ar(freqs) + (Saw.ar(freqs * 0.5) * 0.12)) * 0.13;
        sig = RLPF.ar(sig, cutoff.clip(160, 2600), 0.5);
        gateEnv = EnvGen.kr(Env.asr(2.0, 1, 2.5), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.3, 0.98), 0.95, 0.7) * gateEnv * amp;
        Out.ar(0, ~applySimpleEQ.value(sig, eqLow, eqMid, eqHigh));
    }).add;

    SynthDef(\pycodedj_base, {
        arg cutoff = 800, lfoRate = 0.5, reverbMix = 0.2, amp = 0.3, gate = 1, eqLow = 1, eqMid = 1, eqHigh = 1;
        var sig, env, lfo;
        lfo = SinOsc.kr(lfoRate, 0, 0.3, 1);
        sig = Saw.ar(220 * lfo);
        sig = RLPF.ar(sig, cutoff.clip(200, 4000), 0.5);
        env = EnvGen.kr(Env.asr(0.1, 1, 0.2), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.8)) * env * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    // Default melodic synth for pattern mode — supports \freq / \midinote and full mapped controls.
    SynthDef(\pycodedj_note, {
        arg freq = 440, amp = 0.3, gate = 1, cutoff = 2000, reverbMix = 0.15, eqLow = 1, eqMid = 1, eqHigh = 1;
        var sig, env;
        sig = Mix.ar(Saw.ar(freq * [1.0, 1.004, 0.996])) * 0.18;
        sig = RLPF.ar(sig, cutoff.clip(400, 12000), 0.45);
        env = EnvGen.kr(Env.asr(0.005, 1, 0.08), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.7), 0.45, 0.25) * env * amp;
        Out.ar(0, ~applySimpleEQ.value(sig ! 2, eqLow, eqMid, eqHigh));
    }).add;

    s.sync;

    // Registry: loop name -> array of running Synth instances
    ~loops = Dictionary.new;
    ~loopParams = Dictionary.new;
    ~patterns = Dictionary.new;
    ~loopSynths = Dictionary.new;

    ~synthForLoop = { |name|
        var nameString, parts, role, variant;
        nameString = name.asString;

        switch (nameString,
            "bass_sub",     { \pycodedj_bass_sub },
            "hat_engine",   { \pycodedj_hat_engine },
            "clap_snap",    { \pycodedj_clap_snap },
            "stab_neon",    { \pycodedj_stab_neon },
            "lead_acid",    { \pycodedj_lead_acid },
            "air_warehouse",{ \pycodedj_air_warehouse },
            "kick_pulse",   { \pycodedj_kick_pulse },
            "kick_floor",   { \pycodedj_kick_floor },
            "fx_glitch", { \pycodedj_fx_glitch },
            "pluck_soft",   { \pycodedj_pluck_soft },
            "chord_dub",    { \pycodedj_chord_dub },
            "pad_shimmer",  { \pycodedj_pad_shimmer },
            "kick_hard",    { \pycodedj_kick_hard },
            "bass_reese",   { \pycodedj_bass_reese },
            "bass_rumble",  { \pycodedj_bass_rumble },
            "hat_ride",     { \pycodedj_hat_ride },
            "clap_snare",   { \pycodedj_clap_snare },
            "chord_rave",   { \pycodedj_chord_rave },
            "lead_hoover",  { \pycodedj_lead_hoover },
            "fx_drop",    { \pycodedj_fx_drop },
            // common shorthands
            "acid",         { \pycodedj_bass_acid },
            "kick",         { \pycodedj_kick_floor },
            "note",         { \pycodedj_note },
            // new DJ sounds
            "tom_drum",     { \pycodedj_tom_drum },
            "snare_roll",   { \pycodedj_snare_roll },
            "crash_noise",  { \pycodedj_crash_noise },
            "bass_acid",    { \pycodedj_bass_acid },
            "stab_saw",     { \pycodedj_stab_saw },
            "fx_riser",  { \pycodedj_fx_riser },
            "bell_rave",    { \pycodedj_bell_rave },
            "chord_organ",  { \pycodedj_chord_organ },
            "arp_synth",    { \pycodedj_arp_synth },
            "vox_ahh",      { \pycodedj_vox_ahh },
            "kick_soft",    { \pycodedj_kick_soft },
            "kick_909",     { \pycodedj_kick_909 },
            "kick_click",   { \pycodedj_kick_click },
            "bass_pluck",   { \pycodedj_bass_pluck },
            "bass_fm",      { \pycodedj_bass_fm },
            "bass_mono",    { \pycodedj_bass_mono },
            "bass_wobble",  { \pycodedj_bass_wobble },
            "rim_shot",     { \pycodedj_rim_shot },
            "cowbell",      { \pycodedj_cowbell },
            "perc_blip",    { \pycodedj_perc_blip },
            "shaker_loop",  { \pycodedj_shaker_loop },
            "tick_metal",   { \pycodedj_tick_metal },
            "wood_block",   { \pycodedj_wood_block },
            "pad_minor",    { \pycodedj_pad_minor },
            "chord_deep",   { \pycodedj_chord_deep },
            "chord_glass",  { \pycodedj_chord_glass },
            "pad_warm",     { \pycodedj_pad_warm },
            "pad_string",   { \pycodedj_pad_string },
            "pad_choir",    { \pycodedj_pad_choir },
            "lead_square",  { \pycodedj_lead_square },
            "lead_fm",      { \pycodedj_lead_fm },
            "lead_chip",    { \pycodedj_lead_chip },
            "lead_saw",     { \pycodedj_lead_saw },
            "lead_whistle", { \pycodedj_lead_whistle },
            "fx_down",   { \pycodedj_fx_down },
            "fx_zap",          { \pycodedj_fx_zap },
            "fx_noise",    { \pycodedj_fx_noise },
            "fx_laser",    { \pycodedj_fx_laser },
            "fx_vinyl",  { \pycodedj_fx_vinyl },
            "drone_space",  { \pycodedj_drone_space },
            {
                parts = nameString.split($_);
                role = parts[0];
                variant = if (parts.size > 1) { parts[1] } { "" };

                switch (role,
                    "kick",  {
                        switch (variant,
                            "hard",   { \pycodedj_kick_hard },
                            "pulse",  { \pycodedj_kick_pulse },
                            "soft",   { \pycodedj_kick_soft },
                            "909",    { \pycodedj_kick_909 },
                            "click",  { \pycodedj_kick_click },
                            { \pycodedj_kick_floor }
                        )
                    },
                    "bass",  {
                        switch (variant,
                            "reese",  { \pycodedj_bass_reese },
                            "rumble", { \pycodedj_bass_rumble },
                            "acid",   { \pycodedj_bass_acid },
                            "pluck",  { \pycodedj_bass_pluck },
                            "fm",     { \pycodedj_bass_fm },
                            "mono",   { \pycodedj_bass_mono },
                            "wobble", { \pycodedj_bass_wobble },
                            { \pycodedj_bass_sub }
                        )
                    },
                    "hat",   {
                        switch (variant,
                            "ride",   { \pycodedj_hat_ride },
                            { \pycodedj_hat_engine }
                        )
                    },
                    "clap",  {
                        switch (variant,
                            "snare",  { \pycodedj_clap_snare },
                            "roll",   { \pycodedj_snare_roll },
                            { \pycodedj_clap_snap }
                        )
                    },
                    "snare", {
                        switch (variant,
                            "roll",   { \pycodedj_snare_roll },
                            { \pycodedj_clap_snare }
                        )
                    },
                    "chord", {
                        switch (variant,
                            "stab",   { \pycodedj_stab_neon },
                            "rave",   { \pycodedj_chord_rave },
                            "deep",   { \pycodedj_chord_deep },
                            { \pycodedj_chord_dub }
                        )
                    },
                    "lead",  {
                        switch (variant,
                            "acid",   { \pycodedj_lead_acid },
                            "hoover", { \pycodedj_lead_hoover },
                            "square", { \pycodedj_lead_square },
                            "fm",     { \pycodedj_lead_fm },
                            "chip",   { \pycodedj_lead_chip },
                            "saw",    { \pycodedj_lead_saw },
                            "whistle",{ \pycodedj_lead_whistle },
                            { \pycodedj_pluck_soft }
                        )
                    },
                    "fx",    {
                        switch (variant,
                            "ticks",  { \pycodedj_fx_glitch },
                            "pad",    { \pycodedj_pad_shimmer },
                            "impact", { \pycodedj_fx_drop },
                            "noise",  { \pycodedj_fx_noise },
                            "laser",  { \pycodedj_fx_laser },
                            { \pycodedj_air_warehouse }
                        )
                    },
                    "tom",   { \pycodedj_tom_drum },
                    "stab",  { \pycodedj_stab_saw },
                    "riser", { \pycodedj_fx_riser },
                    "bell",  { \pycodedj_bell_rave },
                    "organ", { \pycodedj_chord_organ },
                    "arp",   { \pycodedj_arp_synth },
                    "vox",   { \pycodedj_vox_ahh },
                    "crash", { \pycodedj_crash_noise },
                    "pluck", { \pycodedj_bass_pluck },
                    "fm",    { \pycodedj_lead_fm },
                    "mono",  { \pycodedj_bass_mono },
                    "wobble",{ \pycodedj_bass_wobble },
                    "rim",   { \pycodedj_rim_shot },
                    "perc",  { \pycodedj_perc_blip },
                    "shaker",{ \pycodedj_shaker_loop },
                    "metal", { \pycodedj_tick_metal },
                    "wood",  { \pycodedj_wood_block },
                    "minor", { \pycodedj_pad_minor },
                    "deep",  { \pycodedj_chord_deep },
                    "glass", { \pycodedj_chord_glass },
                    "warm",  { \pycodedj_pad_warm },
                    "string",{ \pycodedj_pad_string },
                    "choir", { \pycodedj_pad_choir },
                    "square",{ \pycodedj_lead_square },
                    "chip",  { \pycodedj_lead_chip },
                    "saw",   { \pycodedj_lead_saw },
                    "whistle",{ \pycodedj_lead_whistle },
                    "fx_down", { \pycodedj_fx_down },
                    "fx_zap",   { \pycodedj_fx_zap },
                    "noise", { \pycodedj_fx_noise },
                    "laser", { \pycodedj_fx_laser },
                    "vinyl", { \pycodedj_fx_vinyl },
                    "space", { \pycodedj_drone_space },
                    { \pycodedj_base }
                );
            }
        );
    };

    // Helper: start or restart a loop with given voice count
    ~startLoop = { |name, voiceCount = 1|
        // Do not start a legacy synth while a Pdef pattern is active for this name.
        if (~patterns[name].isNil) {
            var synthName, synths, params;
            if (~loops[name].notNil) {
                ~loops[name].do({ |synth| synth.set(\gate, 0) });
            };
            params = ~loopParams[name] ?? {
                (cutoff: 800, lfoRate: 0.5, reverbMix: 0.2, amp: 0.3, low: 1, mid: 1, high: 1)
            };
            ~loopParams[name] = params;
            // Honor synth= override when set; fall back to name-based selection.
            synthName = if (~loopSynths[name].notNil) {
                ~synthForLoop.value(~loopSynths[name])
            } {
                ~synthForLoop.value(name)
            };
            synths = voiceCount.collect({
                Synth(synthName, [
                    \cutoff, params[\cutoff],
                    \lfoRate, params[\lfoRate],
                    \reverbMix, params[\reverbMix],
                    \amp, params[\amp],
                    \eqLow, params[\low],
                    \eqMid, params[\mid],
                    \eqHigh, params[\high]
                ])
            });
            ~loops[name] = synths;
        };
    };

    ~setLoopParam = { |name, key, val|
        var params;
        params = ~loopParams[name] ?? {
            (cutoff: 800, lfoRate: 0.5, reverbMix: 0.2, amp: 0.3, low: 1, mid: 1, high: 1)
        };
        params[key] = val;
        ~loopParams[name] = params;
        if (~loops[name].notNil) {
            switch (key,
                \low,  { ~loops[name].do({ |synth| synth.set(\eqLow,  val) }) },
                \mid,  { ~loops[name].do({ |synth| synth.set(\eqMid,  val) }) },
                \high, { ~loops[name].do({ |synth| synth.set(\eqHigh, val) }) },
                { ~loops[name].do({ |synth| synth.set(key, val) }) }
            );
        };
    };

    ~stopPattern = { |name|
        if (~patterns[name].notNil) {
            Pdef(name.asSymbol).stop;
            ~patterns.removeAt(name);
        };
    };

    ~applyLoopParams = { |name, voiceCount, cutoff, lfoRate, reverbMix, amp, low = 1, mid = 1, high = 1|
        var params;
        params = (cutoff: cutoff, lfoRate: lfoRate, reverbMix: reverbMix, amp: amp, low: low, mid: mid, high: high);
        ~loopParams[name] = params;
        if (voiceCount.asInteger <= 0) {
            // Gate legacy synths; pattern Pdefs are stopped only via /pattern_stop.
            if (~loops[name].notNil) {
                ~loops[name].do({ |synth| synth.set(\gate, 0) });
                ~loops[name] = nil;
            };
        } {
            ~startLoop.value(name, voiceCount.asInteger);
        };
    };

    ~setupPattern = { |name, rootMidi, scaleName, dur, synthName, version, encoded|
        var scale, pitches, sustains, instrSym, i, hasDegree, decodeError, tieTargetIndex, degreeToMidi;
        scale = Scale.at(scaleName.asSymbol) ?? { Scale.chromatic };
        pitches = List.new;
        sustains = List.new;
        i = 0;
        hasDegree = false;
        decodeError = false;
        tieTargetIndex = nil;
        degreeToMidi = { |degree|
            (scale.degrees[degree % scale.size] + rootMidi + (degree.div(scale.size) * 12)).asInteger
        };
        if (version.asString != "v2") {
            ("PyCodeDJ pattern error: unsupported pattern payload version: " ++ version.asString).postln;
        } {
            while ({ (i < encoded.size) and: { decodeError.not } }, {
                var count = encoded[i].asInteger;
                if (count == 0) {
                    pitches.add(Rest());
                    sustains.add(dur);
                    tieTargetIndex = nil;
                    i = i + 1;
                } {
                    if (count == -3) {
                        if (tieTargetIndex.isNil) {
                            "PyCodeDJ pattern error: tie must follow a note or chord.".postln;
                            decodeError = true;
                        } {
                            sustains[tieTargetIndex] = sustains[tieTargetIndex] + dur;
                            pitches.add(Rest());
                            sustains.add(dur);
                            i = i + 1;
                        };
                    } {
                        if ((i + count) >= encoded.size) {
                            "PyCodeDJ pattern error: truncated v2 pattern payload.".postln;
                            decodeError = true;
                        } {
                            if (count == 1) {
                                var degree = encoded[i + 1].asInteger;
                                if (degree == -1) {
                                    pitches.add(rootMidi.asInteger);
                                    tieTargetIndex = nil;
                                } {
                                    pitches.add(degreeToMidi.value(degree));
                                    hasDegree = true;
                                    tieTargetIndex = sustains.size;
                                };
                                sustains.add(dur);
                                i = i + 2;
                            } {
                                if (count > 1) {
                                    pitches.add(Array.fill(count, { |j|
                                        degreeToMidi.value(encoded[i + 1 + j].asInteger)
                                    }));
                                    sustains.add(dur);
                                    hasDegree = true;
                                    tieTargetIndex = sustains.size - 1;
                                    i = i + 1 + count;
                                } {
                                    ("PyCodeDJ pattern error: invalid v2 pattern count: " ++ count).postln;
                                    decodeError = true;
                                };
                            };
                        };
                    };
                };
            });
            if (decodeError.not) {
                // Degree and chord tokens require a freq-aware synth; trigger-only patterns can use the
                // caller-specified synth= or fall back to the loop's default.
                instrSym = if (hasDegree) {
                    \pycodedj_note
                } {
                    if (synthName.size > 0) {
                        ~synthForLoop.value(synthName)
                    } {
                        ~synthForLoop.value(name)
                    }
                };
                Pdef(name.asSymbol,
                    Pbind(
                        \instrument, instrSym,
                        \midinote, Pseq(pitches.asArray, inf),
                        \dur, dur,
                        \sustain, Pseq(sustains.asArray, inf),
                        \amp,       Pfunc({ (~loopParams[name] ?? { (amp: 0.3) })[\amp] }),
                        \cutoff,    Pfunc({ (~loopParams[name] ?? { (cutoff: 800) })[\cutoff] }),
                        \lfoRate,   Pfunc({ (~loopParams[name] ?? { (lfoRate: 0.5) })[\lfoRate] }),
                        \reverbMix, Pfunc({ (~loopParams[name] ?? { (reverbMix: 0.2) })[\reverbMix] }),
                        \eqLow,     Pfunc({ (~loopParams[name] ?? { (low: 1) })[\low] }),
                        \eqMid,     Pfunc({ (~loopParams[name] ?? { (mid: 1) })[\mid] }),
                        \eqHigh,    Pfunc({ (~loopParams[name] ?? { (high: 1) })[\high] }),
                    )
                ).play(TempoClock.default);
                ~patterns[name] = true;
                ("PyCodeDJ pattern started: " ++ name).postln;
            };
        };
    };

    // Single handler for all /pycodedj/loop/<name>/<param> addresses.
    // OSCdef does not interpret "*" as a wildcard — it registers the path literally.
    // OSCFunc with nil path receives every incoming OSC message and we filter by prefix.
    // var は SC では実行文より前に宣言しなければならないため、
    // すべての var をクロージャ先頭にまとめる。
    // ── Panic handler ────────────────────────────────────────────────────────
    // /pycodedj/panic: すべての Synth を即停止し ~loops / ~loopParams を初期化する。
    // OSCFunc は再登録時に上書きされるため、スクリプト再実行時でも安全。
    if (~pycodedjPanic.notNil) { ~pycodedjPanic.free };
    ~pycodedjPanic = OSCFunc({ |msg, time, addr|
        ~loops.keysValuesDo({ |name, synths|
            if (synths.notNil) {
                synths.do({ |synth| synth.set(\gate, 0) });
            };
        });
        ~patterns.keys.do({ |name|
            Pdef(name.asSymbol).stop;
        });
        ~loops = Dictionary.new;
        ~loopParams = Dictionary.new;
        ~patterns = Dictionary.new;
        ~loopSynths = Dictionary.new;
        "PyCodeDJ panic: all loops stopped.".postln;
    }, '/pycodedj/panic');

    if (~pycodedjBpm.notNil) { ~pycodedjBpm.free };
    ~pycodedjBpm = OSCFunc({ |msg, time, addr|
        var bpm;
        bpm = msg[1].asFloat;
        if (bpm > 0) {
            TempoClock.default.tempo = bpm / 60;
            ("PyCodeDJ BPM set: " ++ bpm.asString).postln;
        };
    }, '/pycodedj/bpm');

    if (~pycodedjOSC.notNil) {
        thisProcess.removeOSCRecvFunc(~pycodedjOSC);
    };

    ~pycodedjOSC = { |msg, time, addr, recvPort|
        var parts, name, param, val;
        parts = msg[0].asString.split($/).reject({ |part| part.size == 0 });
        // parts: ["pycodedj", "loop", <name>, <param>]
        if ((parts.size == 4) and: { parts[0] == "pycodedj" } and: { parts[1] == "loop" }) {
            name  = parts[2];
            param = parts[3];
            val   = msg[1];

            switch (param,
                "voice_count", {
                    if (val.asInteger <= 0) {
                        if (~loops[name].notNil) {
                            ~loops[name].do({ |synth| synth.set(\gate, 0) });
                            ~loops[name] = nil;
                        };
                        // Pattern Pdefs are stopped only via /pattern_stop.
                    } {
                        ~startLoop.value(name, val.asInteger);
                    };
                },
                "cutoff",    { ~setLoopParam.value(name, \cutoff,    val.asFloat) },
                "lfo_rate",  { ~setLoopParam.value(name, \lfoRate,   val.asFloat) },
                "reverb",    { ~setLoopParam.value(name, \reverbMix, val.asFloat) },
                "amp",       { ~setLoopParam.value(name, \amp,       val.asFloat) },
                "low",       { ~setLoopParam.value(name, \low,       val.asFloat) },
                "mid",       { ~setLoopParam.value(name, \mid,       val.asFloat) },
                "high",      { ~setLoopParam.value(name, \high,      val.asFloat) },
                "params",    {
                    if (msg.size >= 6) {
                        ~applyLoopParams.value(
                            name,
                            msg[1],
                            msg[2].asFloat,
                            msg[3].asFloat,
                            msg[4].asFloat,
                            msg[5].asFloat,
                            if (msg.size >= 9) { msg[6].asFloat } { 1 },
                            if (msg.size >= 9) { msg[7].asFloat } { 1 },
                            if (msg.size >= 9) { msg[8].asFloat } { 1 }
                        );
                    };
                },
                "pattern",   {
                    // msg: [addr, rootMidi, scaleName, dur, synthName, "v2", encoded...]
                    if (msg.size >= 6) {
                        ~setupPattern.value(
                            name,
                            msg[1].asInteger,
                            msg[2].asString,
                            msg[3].asFloat,
                            msg[4].asString,
                            msg[5].asString,
                            msg[6..]
                        );
                    };
                },
                "pattern_stop", {
                    ~stopPattern.value(name);
                },
                "synth", {
                    var s = val.asString;
                    if (s.size > 0) {
                        ~loopSynths[name] = s;
                    } {
                        ~loopSynths.removeAt(name);
                    };
                }
            );
        };
    };
    thisProcess.addOSCRecvFunc(~pycodedjOSC);

    ("PyCodeDJ synths loaded. Ready. OSC port: " ++ NetAddr.langPort).postln;
});
