---
title: "Surprising things I learned putting together a Home Brain"
date: 2026-05-17T22:14:34-04:00
tags:
  - HomeAssistant
  - LLM
  - HomeBrain
---

So, I'm trying to put together something I call a "Home Brain", a conversational
system I can interact with that not only allows me to control
[IoT](https://en.wikipedia.org/wiki/Internet_of_things) devices in my home, but
also contains personal knowledge I can access, and also more general knowledge
(think wikipedia), and yet all this functionality should run locally, with no
cloud services required.

I initially started down this path with [Home
Assistant](https://www.home-assistant.io/), adding all of our IoT devices into
Home Assistant running on an [RPi](https://www.raspberrypi.com/), which worked
fine, but when I took the next step of buying a couple [Home Assistant Voice
Preview Edition](https://www.home-assistant.io/voice-pe/) devices I found the
performance of the RPi was painfully slow.

Moving the entire stack to my desktop off of the RPi made a huge difference, and
this is where the paid [Claude](https://claude.ai/new) account paid for itself,
with Claude planning and then scripting the entire migration process that went
super smoothly. After that migration the voice path ran much faster, but digging
into the HA implementation I saw that it was the equivalent of yelling at a bag
of regexes. This was the perfect place to use an LLM. Now, first world benefits,
I happened to have a computer laying around the house with an RTX 5000 (Turing)
GPU with 16GB of RAM. I wondered how far I could push that hardware to be the
House Brain I imagined.

Now full credit to the Home Assistant folks for creating a great basis for all
of this. For the device management and control Home Assistant is open source and
just works. The UI is fairly complex, verging on the byzantine, but HA also
supports a REST API that allows enumerating and controlling all of your devices.
With that as the foundation I embarked on building what I call "My Jarvis", the
Home Brain. Now the naming isn't incidental, the Home Assistant folks have done
training on various wake words, and then boiled those down into tiny models you
can run on as EPS32-S3 device, and one of those wake works is "Hey, Jarvis".

Getting Claude to spin up a Go program that coordinated the ESP32 Voice devices
and TTS, STT, and mapping that in a crude way to Home Assistant calls will be a
blog post for another day, but after that worked I pivoted to running LLMs on
the RTX 5000 machine to first handle the mapping from voice commands to Home
Assistant API calls. Once that worked I expanded the actions to answering
queries across two distinct datasets. The datasets are Wikipedia and an
[Obsidian](https://obsidian.md/) vault with personal information in it. The key
here was to index both datasets using [Qdrant](https://qdrant.tech/).

And this is where it got interesting, because there's a whole slew of models and
indexing strategies to try, particularly trying to run all of this on a five
year old GPU with only 16GB of RAM. I did look at a bunch of benchmarks, but in
the end nothing is a substitute for just testing the actual thing yourself.

## The setup

MyJarvis is a Go voice-assistant pipeline for Home Assistant: an ESP32
hears a wake word, audio goes to VAD → STT → an LLM, and the LLM either
calls a Home-Assistant tool or answers a question from RAG (Obsidian
notes or a 43-million-document Wikipedia index in Qdrant).

Every user interaction is dominated by **two LLM calls**, not the code:

1. **Routing** — pick the right tool (turn on a light? check a list?
   look something up in Wikipedia? in my notes?).
2. **Synthesis** — for a lookup, turn retrieved chunks into one spoken
   sentence.

Latency is the whole game for voice. A two-second answer feels like an
assistant; a fifteen-second one feels broken. So we want not only
to be correct, but fast, so the first test harness tested

- 33 prompts spanning home automation, personal-notes lookups, and
  general-knowledge lookups.
- Each asserts the model's _first tool call_ equals the expected tool.
- Synthetic Home-Assistant entities so it's reproducible.
- A machine-readable result line so a script can sweep it across models.

| #   | Prompt                                                     | Expected tool        |
| --- | ---------------------------------------------------------- | -------------------- |
| 1   | Turn on the kitchen light                                  | `set_state`          |
| 2   | Turn off the living room light                             | `set_state`          |
| 3   | Switch off the fan                                         | `set_state`          |
| 4   | Bedroom light on please                                    | `set_state`          |
| 5   | Can you turn the coffee maker on                           | `set_state`          |
| 6   | Shut off the office fan                                    | `set_state`          |
| 7   | Run the goodnight routine                                  | `trigger_automation` |
| 8   | Activate movie time                                        | `trigger_automation` |
| 9   | Set a timer for 10 minutes                                 | `set_timer`          |
| 10  | Start a 5 minute pasta timer                               | `set_timer`          |
| 11  | Add milk to the shopping list                              | `add_to_list`        |
| 12  | Put batteries on the todo list                             | `add_to_list`        |
| 13  | What's on my shopping list                                 | `check_list`         |
| 14  | Is bread on the shopping list                              | `check_list`         |
| 15  | Check off bread from the shopping list                     | `check_off_item`     |
| 16  | Clean up the lists                                         | `clean_lists`        |
| 17  | What did I write about Goldmine Prime                      | `search_notes`       |
| 18  | When did I buy the Hayes Run property                      | `search_notes`       |
| 19  | Summarize my notes on the Telluride trip                   | `search_notes`       |
| 20  | What are the specs of my Austin computer                   | `search_notes`       |
| 21  | Remind me what I wrote about the RAG setup                 | `search_notes`       |
| 22  | What did I write in my notes about the basement renovation | `search_notes`       |
| 23  | What did I note about my car's last oil change             | `search_notes`       |
| 24  | Who invented the transistor                                | `search_wikipedia`   |
| 25  | How far is the moon from the earth in light seconds        | `search_wikipedia`   |
| 26  | What is the capital of Mongolia                            | `search_wikipedia`   |
| 27  | When did World War 2 end                                   | `search_wikipedia`   |
| 28  | What is the speed of light                                 | `search_wikipedia`   |
| 29  | How tall is Mount Everest                                  | `search_wikipedia`   |
| 30  | Who wrote Pride and Prejudice                              | `search_wikipedia`   |
| 31  | Explain how photosynthesis works                           | `search_wikipedia`   |
| 32  | What year did the Berlin Wall fall                         | `search_wikipedia`   |
| 33  | What is the boiling point of water in Fahrenheit           | `search_wikipedia`   |

So I've got the time, and the tokens are free, so let's test this against
a large number of models; five families across sizes, context windows, and
quantizations, each run with _and_ without chain-of-thought where the
family supports the switch:

- **Qwen**: 3:4b, 3:8b, 3:8b-128k, 3:8b-q8_0, 3:14b-64k, 3:14b-q4_K_M,
  3.5:9b, 3.5:9b-64k, 3.6:latest
- **Gemma**: 4:latest, 4:16k, 3:4b, 3:12b, 4-26B (Q4 GGUF)
- **Nemotron**: 3-nano:4b, mini:latest
- **Granite**: 4:latest, 3.3:8b
- **Mistral / Phi**: mistral:7b, phi4-mini, phi4, phi4-reasoning, phi3

The results were interesting:

**Group 1 — 100% routing accuracy** (33 prompts, warm, chain-of-thought
on, ranked by mean latency):

| Model                      | Accuracy | Mean       | p95        |
| -------------------------- | -------- | ---------- | ---------- |
| **granite4:latest**        | **100%** | **0.54 s** | **0.65 s** |
| nemotron-3-nano:4b         | 100%     | 1.88 s     | 2.42 s     |
| gemma4:latest              | 100%     | 2.24 s     | 6.41 s     |
| gemma4:16k                 | 100%     | 2.26 s     | 6.24 s     |
| qwen3:8b                   | 100%     | 3.02 s     | 5.85 s     |
| qwen3:8b-128k              | 100%     | 3.04 s     | 4.42 s     |
| qwen3.5:9b                 | 100%     | 3.22 s     | 4.30 s     |
| qwen3.5:9b-64k             | 100%     | 3.24 s     | 4.11 s     |
| qwen3:14b-64k _(old prod)_ | 100%     | 4.58 s     | 7.81 s     |
| qwen3:14b-q4_K_M           | 100%     | 4.79 s     | 8.49 s     |
| qwen3:4b                   | 100%     | 4.81 s     | 9.09 s     |
| qwen3:8b-q8_0              | 100%     | 4.98 s     | 10.35 s    |
| qwen3.6:latest             | 100%     | 26.73 s    | 38.35 s    |

I absolutely did not expect IBM's Granite to top out the list here.

**Group 2 — ran but mis-routed** (unusable as routers):

| Model                | Accuracy | Mean   |
| -------------------- | -------- | ------ |
| nemotron-mini:latest | 21%      | 0.58 s |
| granite3.3:8b        | 0%       | 0.99 s |
| mistral:7b           | 0%       | 1.06 s |
| phi4-mini:latest     | 0%       | 1.61 s |

**Group 3 — no tool-calling support**: `gemma3:4b`, `gemma3:12b`, `phi4:latest`,
`phi4-reasoning:latest`, `phi3:latest`, and the 26B Gemma GGUF all return
Ollama's _"does not support tools"_ — no function-calling template.

**Chain-of-thought on vs off** was tested for every Qwen and Nemotron
config — the extra runs that take the sweep to 36. The deltas were small
_and inconsistent_ — granite4 0.54→0.55 s, qwen3:8b 3.02→3.06 s, but
qwen3:8b-q8*0 actually \_improved* 4.98→4.28 s while qwen3:4b _worsened_
4.81→5.99 s, and nemotron-3-nano slipped 100→97%. Disabling
"thinking" was _not_ a reliable latency reducer.

Now the above only tests if the LLM chooses the correct tool to call, we still
need to measure how well the LLM does as querying Wikipedia and the Obsidian
vault via Qdrant and organizing that into a coherent answer.

A separate suite ran real Wikipedia questions through the full
retrieve-then-answer path, scoring factual correctness, TTS-cleanliness,
source attribution, and latency. Synthesis turned out to be _easy_: 16
of 17 models were 100% factually correct (the answer is in the retrieved
text; the model just has to phrase it). The differentiators were latency
and cleanliness:

All 17 chat-capable models, 6 Wikipedia questions each, ranked by mean
latency (facts = answer contains the correct fact; clean = TTS-safe, no
markdown; attrib = cites the source article):

| Model                      | Facts    | Clean    | Attrib | Mean        |
| -------------------------- | -------- | -------- | ------ | ----------- |
| phi3:latest                | 100%     | 83%      | 50%    | 1.61 s      |
| **granite4:latest**        | **100%** | **100%** | 83%    | **1.64 s**  |
| gemma3:4b                  | 100%     | 100%     | 100%   | 1.65 s      |
| phi4-mini:latest           | 100%     | 100%     | 83%    | 2.22 s      |
| mistral:7b                 | 100%     | 100%     | 67%    | 2.29 s      |
| llama3.1:8b                | 100%     | 100%     | 100%   | 2.32 s      |
| granite3.3:8b              | 100%     | 100%     | 100%   | 3.18 s      |
| gemma3:12b                 | 100%     | 100%     | 100%   | 3.20 s      |
| phi4:latest                | 100%     | 100%     | 100%   | 4.17 s      |
| nemotron-3-nano:4b         | 67%      | 100%     | 67%    | 5.17 s      |
| qwen3:8b                   | 100%     | 83%      | 100%   | 6.91 s      |
| gemma4:16k                 | 100%     | 100%     | 100%   | 8.36 s      |
| gemma4:latest              | 100%     | 100%     | 100%   | 8.54 s      |
| qwen3:14b-64k _(old prod)_ | 100%     | 83%      | 100%   | 11.48 s     |
| qwen3:4b                   | 100%     | 100%     | 100%   | 13.48 s     |
| qwen3.5:9b                 | 100%     | 100%     | 100%   | **37.33 s** |
| qwen3.5:9b-64k             | 100%     | 100%     | 100%   | **44.47 s** |

Again, Granite being the winner here, fastest speed with 100% on facts and
cleanliness, was a total surprise.

So I thought I had a win here, but then a simple query blew the whole thing apart.

> "How big is the moon?"

That query produced a 600-character ramble stitched across several _unrelated_
articles including Phoebe — a moon of Saturn; a basin on Mars; an
orders-of-magnitude list, etc.

Probing the 43 M-doc index directly was the eye-opener: **no short query
surfaces canonical articles.** "Moon", "how big is the moon", and the
LLM's keyword expansion all return bands, people, and disambiguation
pages — never the _Moon_ article. It _is_ indexed (a long, content-rich
query finds it at rank 4–5), so this is a **ranking** problem, not a
data problem. The token "moon" is swamped across 43 million documents;
sparse hybrid search (SPLADE + BM25, DBSF fusion) can't promote the
canonical article from a two-word query.

Because retrieval is fast (~70 ms), I could afford to be clever:

**Use the question, not just the keywords.**

The router distills the user's question into keywords; sometimes that drops the
very term that finds the article. I probed 12 factual questions, retrieving
three ways and scoring whether the _expected canonical article_ landed in the
top 5:

| Retrieval input              | recall@5  | mean rank |
| ---------------------------- | --------- | --------- |
| keyword query (old behavior) | 8/12      | 1.62      |
| raw question                 | 10/12     | 1.70      |
| **keyword + question**       | **10/12** | **1.60**  |

So simply adding the original query in along with the keyword query made a
huge difference.

**Adversarial re-rank.**

Search results kept hitting Wikipedia disambiguation pages that aren't really
useful. A simple fix was to drop them outright; demote "List/Index/Outline of …"
pages below real articles.

**One conditional re-query.**

If the top hit was still junk (disambiguation/index), ask the model for a better
article title and retrieve _once_ more. Bounded, no loop, and it only fires on
the junk signal so clean queries pay nothing. This **rescued "What is the
capital of France?"** — which had missed the _Paris_ article in _every_
retrieval mode — by re-querying into "Paris".

After these, the synthesis suite (now including adversarial cases) was
8/8: the Eiffel Tower question cites the _Eiffel Tower_ article, not
"Eiffel Tower (disambiguation)".

This has been a fun project, and I'm continuing to work on it and improve
functionality and correctness, but the biggest lesson I learned along the way so
far has been to just simply measure things and not rely on rankings/ratings from
other parties. While they might give you a general idea of a model's
capabilities, you won't really know until you apply them to your specific
problem. I had originally just gone with qwen3.5:9b based off it's rankings
against the other models, but in actual measurments the Granite model is not
only more accurate on tool calling and synthesis, but also over 8x faster!

Now the moon query is faster, but it still ends up referencing the Wikipedia
article on [Habash al-Hasib](https://en.wikipedia.org/wiki/Habash_al-Hasib), so
clearly there's still work to do.
