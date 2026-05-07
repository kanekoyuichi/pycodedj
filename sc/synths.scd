// PyCodeDJ — SuperCollider synth definitions
// Run this file in the SuperCollider IDE before using pycodedj eval.

s.waitForBoot({
    // Shared controls:
    // cutoff = tone/brightness, lfoRate = pattern/modulation speed,
    // reverbMix = space, gate = fade out when a loop is restarted/stopped.
    SynthDef(\pycodedj_sub_bass, {
        arg cutoff = 900, lfoRate = 1.0, reverbMix = 0.05, amp = 0.38, gate = 1;
        var trig, freq, env, click, sig;
        trig = Impulse.kr(lfoRate.clip(0.25, 4.0));
        freq = Demand.kr(trig, 0, Dseq([36, 36, 43, 34, 36, 48, 43, 34].midicps, inf));
        env = Decay2.kr(trig, 0.004, 0.32);
        click = Decay2.kr(trig, 0.001, 0.018) * WhiteNoise.ar(0.08);
        sig = (SinOsc.ar(freq) + (Saw.ar(freq * 0.5) * 0.28) + click) * env;
        sig = RLPF.ar(sig.tanh, cutoff.clip(90, 1800), 0.28);
        env = EnvGen.kr(Env.asr(0.1, 1, 0.2), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.8)) * env * amp;
        Out.ar(0, sig ! 2);
    }).add;

    SynthDef(\pycodedj_hat_engine, {
        arg cutoff = 6500, lfoRate = 1.5, reverbMix = 0.08, amp = 0.18, gate = 1;
        var trig, openTrig, closedEnv, openEnv, tone, sig, env;
        trig = Impulse.kr((lfoRate * 4).clip(3, 18));
        openTrig = PulseDivider.kr(trig, 4);
        closedEnv = Decay2.kr(trig, 0.001, 0.045);
        openEnv = Decay2.kr(openTrig, 0.002, 0.18);
        tone = cutoff.linlin(200, 4000, 5000, 14000).clip(5000, 14000);
        sig = HPF.ar(WhiteNoise.ar, tone * 0.7);
        sig = BPF.ar(sig, tone, 0.45) * (closedEnv + (openEnv * 0.75));
        env = EnvGen.kr(Env.asr(0.01, 1, 0.08), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.45), 0.25, 0.15) * env * amp;
        Out.ar(0, Pan2.ar(sig, SinOsc.kr(0.13).range(-0.25, 0.25)));
    }).add;

    SynthDef(\pycodedj_neon_stab, {
        arg cutoff = 1200, lfoRate = 0.25, reverbMix = 0.25, amp = 0.22, gate = 1;
        var trig, root, freqs, env, sig, gateEnv;
        trig = Impulse.kr((lfoRate * 0.75).clip(0.08, 1.5));
        root = Demand.kr(trig, 0, Dseq([48, 43, 46, 41], inf));
        freqs = (root + [0, 3, 7, 10]).midicps;
        env = Decay2.kr(trig, 0.01, 0.42);
        sig = Splay.ar(VarSaw.ar(freqs * [1, 1.004, 0.997, 1.006], 0, 0.42)) * 0.2;
        sig = RLPF.ar(sig, cutoff.clip(600, 4500), 0.32) * env;
        gateEnv = EnvGen.kr(Env.asr(0.05, 1, 0.25), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.8), 0.55, 0.35) * gateEnv * amp;
        Out.ar(0, sig);
    }).add;

    SynthDef(\pycodedj_acid_lead, {
        arg cutoff = 2100, lfoRate = 2.0, reverbMix = 0.12, amp = 0.22, gate = 1;
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
        Out.ar(0, Pan2.ar(sig, SinOsc.kr(0.21).range(-0.35, 0.35)));
    }).add;

    SynthDef(\pycodedj_warehouse_air, {
        arg cutoff = 700, lfoRate = 0.1, reverbMix = 0.6, amp = 0.24, gate = 1;
        var sweep, dust, tail, sig, env;
        sweep = LFNoise1.kr(lfoRate.clip(0.03, 0.8)).range(0, 1).exprange(180, cutoff.clip(350, 3600));
        dust = Decay2.kr(Dust.kr((lfoRate * 5).clip(0.5, 7)), 0.02, 1.2) * PinkNoise.ar(0.08);
        tail = BPF.ar(PinkNoise.ar(0.22), sweep, 0.2);
        sig = HPF.ar(tail + dust, 140);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.25, 0.9), 0.92, 0.65);
        env = EnvGen.kr(Env.asr(1.5, 1, 2.0), gate, doneAction: 2);
        Out.ar(0, Pan2.ar(sig * env * amp, LFNoise1.kr(0.08)));
    }).add;

    SynthDef(\pycodedj_kick_pulse, {
        arg cutoff = 900, lfoRate = 1.0, reverbMix = 0.02, amp = 0.42, gate = 1;
        var trig, env, pitch, sig, gateEnv;
        trig = Impulse.kr(lfoRate.clip(0.5, 4.0));
        env = Decay2.kr(trig, 0.001, 0.22);
        pitch = EnvGen.kr(Env([72, 38, 34], [0.025, 0.16], \exp), trig).midicps;
        sig = SinOsc.ar(pitch) * env;
        sig = (sig + (BPF.ar(WhiteNoise.ar(0.08), cutoff.clip(500, 4500), 0.5) * Decay2.kr(trig, 0.001, 0.02))).tanh;
        gateEnv = EnvGen.kr(Env.asr(0.01, 1, 0.08), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.25), 0.2, 0.1) * gateEnv * amp;
        Out.ar(0, sig ! 2);
    }).add;

    SynthDef(\pycodedj_floor_kick, {
        arg cutoff = 1100, lfoRate = 1.0, reverbMix = 0.08, amp = 0.52, gate = 1;
        var trig, bodyEnv, punchEnv, tailEnv, pitch, body, punch, tail, room, sig, gateEnv;
        trig = Impulse.kr(lfoRate.clip(0.8, 3.0));
        bodyEnv = Decay2.kr(trig, 0.001, 0.34);
        punchEnv = Decay2.kr(trig, 0.001, 0.035);
        tailEnv = Decay2.kr(trig, 0.02, 0.7);
        pitch = EnvGen.kr(Env([88, 43, 35], [0.018, 0.22], \exp), trig).midicps;
        body = SinOsc.ar(pitch) * bodyEnv;
        punch = BPF.ar(WhiteNoise.ar(0.32), cutoff.clip(700, 5200), 0.35) * punchEnv;
        tail = LPF.ar(SinOsc.ar(46) + Saw.ar(23, 0.12), 160) * tailEnv * 0.34;
        room = FreeVerb.ar((body + tail) * 0.5, reverbMix.clip(0, 0.3), 0.62, 0.25);
        sig = (body + punch + tail + room).tanh;
        gateEnv = EnvGen.kr(Env.asr(0.005, 1, 0.12), gate, doneAction: 2);
        sig = Compander.ar(sig, sig, 0.45, 1, 0.35, 0.003, 0.08) * gateEnv * amp;
        Out.ar(0, sig ! 2);
    }).add;

    SynthDef(\pycodedj_glitch_ticks, {
        arg cutoff = 5000, lfoRate = 2.0, reverbMix = 0.08, amp = 0.16, gate = 1;
        var trig, rate, env, sig, gateEnv;
        rate = (lfoRate * 8).clip(4, 28);
        trig = Dust.kr(rate);
        env = Decay2.kr(trig, 0.0005, 0.035);
        sig = HPF.ar(Hasher.ar(Sweep.ar(trig)), cutoff.clip(1200, 12000) * 0.5) * env;
        sig = Pan2.ar(sig, LFNoise1.kr(rate * 0.25).range(-0.8, 0.8));
        gateEnv = EnvGen.kr(Env.asr(0.005, 1, 0.05), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.5), 0.35, 0.2) * gateEnv * amp;
        Out.ar(0, sig);
    }).add;

    SynthDef(\pycodedj_soft_pluck, {
        arg cutoff = 1600, lfoRate = 1.0, reverbMix = 0.18, amp = 0.22, gate = 1;
        var trig, note, freq, env, sig, gateEnv;
        trig = Impulse.kr(lfoRate.clip(0.2, 6.0));
        note = Demand.kr(trig, 0, Dseq([60, 64, 67, 72, 67, 64], inf));
        freq = note.midicps;
        env = Decay2.kr(trig, 0.004, 0.28);
        sig = Mix.ar(Pulse.ar(freq * [1, 2.01], [0.42, 0.35], [0.55, 0.12])) * env;
        sig = RLPF.ar(sig, cutoff.clip(350, 7000), 0.38);
        gateEnv = EnvGen.kr(Env.asr(0.02, 1, 0.16), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.75), 0.45, 0.28) * gateEnv * amp;
        Out.ar(0, sig ! 2);
    }).add;

    SynthDef(\pycodedj_dub_chord, {
        arg cutoff = 1200, lfoRate = 0.5, reverbMix = 0.35, amp = 0.2, gate = 1;
        var trig, root, freqs, env, sig, gateEnv;
        trig = Impulse.kr(lfoRate.clip(0.08, 2.0));
        root = Demand.kr(trig, 0, Dseq([43, 46, 41, 48], inf));
        freqs = (root + [0, 7, 10, 14]).midicps;
        env = Decay2.kr(trig, 0.015, 0.55);
        sig = Splay.ar(Pulse.ar(freqs, 0.48)) * 0.16;
        sig = RLPF.ar(sig, cutoff.clip(500, 5000), 0.24) * env;
        gateEnv = EnvGen.kr(Env.asr(0.05, 1, 0.3), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.1, 0.85), 0.75, 0.45) * gateEnv * amp;
        Out.ar(0, sig);
    }).add;

    SynthDef(\pycodedj_shimmer_pad, {
        arg cutoff = 1400, lfoRate = 0.15, reverbMix = 0.55, amp = 0.2, gate = 1;
        var drift, freqs, sig, gateEnv;
        drift = LFNoise1.kr(lfoRate.clip(0.03, 0.7)).range(-0.08, 0.08);
        freqs = ([55, 62, 67, 74] + drift).midicps;
        sig = Splay.ar(SinOsc.ar(freqs * [1, 1.002, 0.998, 1.004])) * 0.18;
        sig = RLPF.ar(sig, cutoff.clip(500, 5200), 0.42);
        gateEnv = EnvGen.kr(Env.asr(1.2, 1, 1.8), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0.25, 0.95), 0.9, 0.55) * gateEnv * amp;
        Out.ar(0, sig);
    }).add;

    SynthDef(\pycodedj_base, {
        arg cutoff = 800, lfoRate = 0.5, reverbMix = 0.2, amp = 0.3, gate = 1;
        var sig, env, lfo;
        lfo = SinOsc.kr(lfoRate, 0, 0.3, 1);
        sig = Saw.ar(220 * lfo);
        sig = RLPF.ar(sig, cutoff.clip(200, 4000), 0.5);
        env = EnvGen.kr(Env.asr(0.1, 1, 0.2), gate, doneAction: 2);
        sig = FreeVerb.ar(sig, reverbMix.clip(0, 0.8)) * env * amp;
        Out.ar(0, sig ! 2);
    }).add;

    s.sync;

    // Registry: loop name -> array of running Synth instances
    ~loops = Dictionary.new;
    ~loopParams = Dictionary.new;

    ~synthForLoop = { |name|
        switch (name,
            "sub_bass", { \pycodedj_sub_bass },
            "hat_engine", { \pycodedj_hat_engine },
            "neon_stab", { \pycodedj_neon_stab },
            "acid_lead", { \pycodedj_acid_lead },
            "warehouse_air", { \pycodedj_warehouse_air },
            "kick_pulse", { \pycodedj_kick_pulse },
            "floor_kick", { \pycodedj_floor_kick },
            "glitch_ticks", { \pycodedj_glitch_ticks },
            "soft_pluck", { \pycodedj_soft_pluck },
            "dub_chord", { \pycodedj_dub_chord },
            "shimmer_pad", { \pycodedj_shimmer_pad },
            { \pycodedj_base }
        );
    };

    // Helper: start or restart a loop with given voice count
    ~startLoop = { |name, voiceCount = 1|
        var synthName, synths, params;
        if (~loops[name].notNil) {
            ~loops[name].do({ |synth| synth.set(\gate, 0) });
        };
        params = ~loopParams[name] ?? {
            (cutoff: 800, lfoRate: 0.5, reverbMix: 0.2)
        };
        ~loopParams[name] = params;
        synthName = ~synthForLoop.value(name);
        synths = voiceCount.collect({
            Synth(synthName, [
                \cutoff, params[\cutoff],
                \lfoRate, params[\lfoRate],
                \reverbMix, params[\reverbMix]
            ])
        });
        ~loops[name] = synths;
    };

    ~setLoopParam = { |name, key, val|
        var params;
        params = ~loopParams[name] ?? {
            (cutoff: 800, lfoRate: 0.5, reverbMix: 0.2)
        };
        params[key] = val;
        ~loopParams[name] = params;
        if (~loops[name].notNil) {
            ~loops[name].do({ |synth| synth.set(key, val) });
        };
    };

    ~applyLoopParams = { |name, voiceCount, cutoff, lfoRate, reverbMix|
        var params;
        params = (cutoff: cutoff, lfoRate: lfoRate, reverbMix: reverbMix);
        ~loopParams[name] = params;
        if (voiceCount.asInteger <= 0) {
            if (~loops[name].notNil) {
                ~loops[name].do({ |synth| synth.set(\gate, 0) });
                ~loops[name] = nil;
            };
        } {
            ~startLoop.value(name, voiceCount.asInteger);
        };
    };

    // Single handler for all /pycodedj/loop/<name>/<param> addresses.
    // OSCdef does not interpret "*" as a wildcard — it registers the path literally.
    // OSCFunc with nil path receives every incoming OSC message and we filter by prefix.
    // var は SC では実行文より前に宣言しなければならないため、
    // すべての var をクロージャ先頭にまとめる。
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
                    } {
                        ~startLoop.value(name, val.asInteger);
                    };
                },
                "cutoff",    { ~setLoopParam.value(name, \cutoff,    val.asFloat) },
                "lfo_rate",  { ~setLoopParam.value(name, \lfoRate,   val.asFloat) },
                "reverb",    { ~setLoopParam.value(name, \reverbMix, val.asFloat) },
                "params",    {
                    if (msg.size >= 5) {
                        ~applyLoopParams.value(name, msg[1], msg[2].asFloat, msg[3].asFloat, msg[4].asFloat);
                    };
                }
            );
        };
    };
    thisProcess.addOSCRecvFunc(~pycodedjOSC);

    ("PyCodeDJ synths loaded. Ready. OSC port: " ++ NetAddr.langPort).postln;
});
