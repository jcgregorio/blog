---
title: "Fixing false positives in the HomeBrain"
date: 2026-06-05T16:52:18-04:00
tags:
  - HomeAssistant
  - LLM
  - HomeBrain
---

So one the most pressing issues with the HomeBrain has been false positives, not that this is an issue solely with the HomeBrain, as
both the Google and Alexa devices frequently get erroneously triggered and start yappingg about nothing nobody asked for.
The issue was pressing because the HomeBrain was bad enough that it bothering my wife, so it moved to the top of the "fix" list.

To understand the solution, first let's look at the current system at a high level:

```
      User speaks
           │
           ▼
  ┌─────────────────┐
  │   Microphone    │
  │  XMOS XU316 DSP │
  │  AEC · NS · AGC │
  └────────┬────────┘
           │ 32-bit stereo
           │ PCM · 16 kHz
           ▼
  ┌─────────────────┐
  │    ESP32-S3     │
  │  microWakeWord  │
  │  (on-device     │
  │    TFLite)      │
  └────────┬────────┘
           │ wake + 1.5s
           │ prebuffer
           ▼
  ┌─────────────────┐
  │      MQTT       │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │    myjarvis     │
  │   Silero VAD    │
  └────────┬────────┘
           │ speech end
           ▼
  ┌─────────────────┐
  │ faster-whisper  │
  │      STT        │
  └────────┬────────┘
           │ transcript
           ▼
  ┌─────────────────┐
  │ **wake-word**   │
  │    **filter**   │
  └────────┬────────┘
           │ real command
           ▼
  ┌─────────────────┐  tool  ┌──────────┐
  │   Ollama LLM    │ calls  │    HA    │
  │   granite4      │───────▶│ REST API │
  └────────┬────────┘        └──────────┘
           │ reply
           ▼
  ┌─────────────────┐
  │   Piper TTS     │
  └────────┬────────┘
           │ WAV URL
           │ via MQTT
           ▼
  ┌─────────────────┐
  │    ESP32-S3     │
  │  AIC3204 DAC    │
  └────────┬────────┘
           │
           ▼
        Speaker
```

The `wake-word filter` is the new component that was added in the fix.

[microWakeWord](https://github.com/kahrendt/microWakeWord) (the on-device
[TFLite](https://ai.google.dev/edge/litert) model) occasionally fires on ambient
speech that phonetically resembles "Hey Jarvis". When this happened,
[myjarvis](https://github.com/jcgregorio/myjarvis) would receive the audio,
transcribe it, and pass it to the LLM — which would respond with a generic
greeting or attempt to act on whatever was said in the background conversation.

This failed in two different way:

1. **No wake word in transcript** — The STT transcript contains real speech but
   no "Hey Jarvis" at the beginning. For example, just some background chatter
   on the TV.

2. **Only wake word in transcript** — The STT transcript only contains one or
   more wakewords but no actual command follows. Example: _"Hey Jarvis. Hey
   Jarvis. Hey Jarvis."_ — previously this passed the wake-word check and
   reached the LLM, which responded with a generic greeting.

Now the microWakeWord detection is great because it runs on the device itself,
which is efficent so that none of the other parts of the system start running
until "Hey, Jarvis" is detected, so we'll keep that in place, but the first part
of the fix is to keep a ring buffer of all the data that the wake word detection
has heard. This doesn't have to be a huge amount of memory, just enough to fully
capture the actual audio that got detected as "Hey, Jarvis", so 192 KB, which is
~1.5 seconds of audio at 16 kHz / 32-bit / stereo.

That ring buffer was a big missing piece, without it the wake word detection
would only start streaming the audio _after_ it detected "Hey, Jarvis", which
means the actualy "Hey, Jarvis" audio was lost. Now with the ring buffer we can
include the triggering audio that we send through the Speech to Text (STT)
sysem.

Now to fix the first issue I just look to see if the text starts with something
that looks like "Hey, Jarvis", which we can handle via regexp now that we are in
the text phase of processing the input:

    `(?i)^(h(?:ey|i),?\sjarvis)[\p{P}+\s]*`

Note we use the regexp to also slurp up trailing punctuation, because we use the
regexp to not only find the "Hey, Jarvis", but to also snip it from the front of
the text we pass to the LLM. This also leads to the fix for issue #2 where all
we get in the wake word, we just repeatedly remove a found "Hey, Jarvis" from
the front of the prompt until we either have nothing left, in which case we stop
processing, or we have non-wake word text, in which case we pass it on to the
LLM.

```Go
func StartsWithWakeWord(transcript string) (string, bool) {
	match := heyJarvisRE.FindString(transcript)
	if match != "" {
		// We now know it starts with a wake word, but what if it was only the
		// wake word, or multiple wake words repeated. So let's repeatedly look
		// for "hey, jarvis" at the beginning and remove until no more appear.
		for match != "" {
			transcript = transcript[len(match):]
			match = heyJarvisRE.FindString(transcript)
		}
		return transcript, true
	}
	return transcript, false
}
```

I still haven't figured out what is triggering the system with _"Hey Jarvis. Hey
Jarvis. Hey Jarvis."_, I presume a TV jingle of some sort? Anyway, this is live
and has stopped five inappropriate responses in the first 24 hours after
deployment, there were **zero** false positives! Even better, Alexa falsely
triggered at least once in that timeframe, so I'm currently doing better than
the competition `;-)`.
