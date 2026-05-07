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

    ~synthForLoop = { |name|
        switch (name,
            "sub_bass", { \pycodedj_sub_bass },
            "hat_engine", { \pycodedj_hat_engine },
            "neon_stab", { \pycodedj_neon_stab },
            "acid_lead", { \pycodedj_acid_lead },
            "warehouse_air", { \pycodedj_warehouse_air },
            { \pycodedj_base }
        );
    };

    // Helper: start or restart a loop with given voice count
    ~startLoop = { |name, voiceCount = 1|
        var synthName, synths;
        if (~loops[name].notNil) {
            ~loops[name].do({ |synth| synth.set(\gate, 0) });
        };
        synthName = ~synthForLoop.value(name);
        synths = voiceCount.collect({ Synth(synthName) });
        ~loops[name] = synths;
    };

    // Single handler for all /pycodedj/loop/<name>/<param> addresses.
    // OSCdef does not interpret "*" as a wildcard — it registers the path literally.
    // OSCFunc with nil path receives every incoming OSC message and we filter by prefix.
    // var は SC では実行文より前に宣言しなければならないため、
    // すべての var をクロージャ先頭にまとめる。
    if (~pycodedjOSC.notNil) {
        ~pycodedjOSC.free;
    };

    ~pycodedjOSC = OSCFunc({ |msg, time, addr|
        var parts, name, param, val;
        parts = msg[0].asString.split($/);
        // parts: ["pycodedj", "loop", <name>, <param>]
        if (parts.size != 4) { ^nil };
        if (parts[0] != "pycodedj") { ^nil };
        if (parts[1] != "loop") { ^nil };

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
            "cutoff",    { ~loops[name].do({ |synth| synth.set(\cutoff,    val.asFloat) }) },
            "lfo_rate",  { ~loops[name].do({ |synth| synth.set(\lfoRate,   val.asFloat) }) },
            "reverb",    { ~loops[name].do({ |synth| synth.set(\reverbMix, val.asFloat) }) }
        );
    }, nil, nil, NetAddr.langPort);  // nil path = receive all OSC messages

    ("PyCodeDJ synths loaded. Ready. OSC port: " ++ NetAddr.langPort).postln;
});
