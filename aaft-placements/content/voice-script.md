# Voice script — every voice AI-generated (ElevenLabs)

Updated 14 Nov 2026. This file replaces `interview-script.md`.

Every voice in the film is generated: the narrator, both interviewers, Riya and Arjun. Nothing is recorded live from the product, so the interviewer's lines are now **a fixed script**, not targets.

- **TTS text** is exactly what goes into ElevenLabs: numbers spelled out, acronyms spaced where needed.
- **On-screen text** is what the call window or cards show, in ₹ and digits.
- **Est.** assumes ~150 wpm. ElevenLabs usually runs a little faster, which gives some slack. Final timing comes from the real clip lengths (see *How the HTML uses the clips*).

---

## Status — pass 3 (14 Nov 2026)

- **New or changed lines** (Ranbir):
  - `narr_05a`: "Students upload their CV, and get asked about their experience for the role they're applying to." (6.1s)
  - `narr_05t` (new beat between 5b and 5c, director's wording): "They can practise all types of interviews, like case interviews, technical rounds, HR discussions and more." (7.3s). Visual: the real New interview page (Interview type chips + More dropdown).
  - `narr_06`: "From marketing to cinema, every school practises for its own roles." (4.3s). "School" is kept because that's AAFT's own term.
- **Pass 3g — third person throughout.** The film plays on an event screen with no live demo, so the narrator carries what small on-screen text can't. The narrator never says "I" or "you"; the on-screen headlines don't either (product UI and dialogue keep their own wording).
  - `narr_03b`: "A student asks which companies are coming in December. The Space answers from the placement cell's own drive calendar." (8.1s)
  - `narr_03d`: "Another asks what Meridian Analytics will ask, and how to prepare. The answer draws on seniors' debriefs from past Meridian interviews." (9.5s)
  - `narr_04`: "Every recruiter comes with its own mock interview. Students pick a company and start practising." (7.1s)
  - `narr_08`: "Every question answered. Every interview practised. Placement-ready, around the clock." (6.5s). The end card shows the same line.
  - Headlines: "Practise with *their own CV*", "Pushed on *their own numbers*", "Answers from *AAFT's own documents*".
- **One-take voices (14 Nov):** narrator = Ranbir take 1, interviewer = Briggs take 1 (re-recorded with "Option A / Option B" so "A" isn't read as the article). Each speaker is one continuous read, cut into the usual clips by `tools/voices.py cut`; old clips in `assets/audio/raw/pre-onetake/`.
- **Runtime: 2:15** (14 Nov: ~1s pauses added at scene changes). Timing lives in `content/timeline.json`.
- **Speaker clarity:** the interviewer lives in the call window (orb and prompt). Only the student gets a card on the left (face, name, pink "Speaking" pill), and only while they answer. No side borders, no context pills.
- `tools/voices.py` LINES and `tools/mix_preview.py` PLAN are the source of truth; the older sections below predate this pass.

## Status (14 Nov 2026)

- **All 16 lines are generated** in `assets/audio/*.mp3`, loudness-normalised to -16 LUFS. Untouched takes are in `assets/audio/raw/`.
- `assets/audio/clips.json` holds each clip's speaker, text, measured duration and word timings. The HTML build reads it.
- **Two music beds** are in `assets/music/` (`bed_a`: felt piano and arpeggios; `bed_b`: Rhodes and mallets), each with a 2:00 soundtrack preview (`preview_bed_a.mp3`, `preview_bed_b.mp3`).
- **Approved order (14 Nov, second pass):** Riya's interview ends on her ₹229 answer (the **CFO follow-up `int_05d_f` is cut**). A **bridge** (`narr_06`: "From marketing to cinema, every school practises for its own roles.") returns to the Placement prep list. **Arjun's interview** follows with a full answer (`arjun_06_a` regenerated), then **Arjun's scorecard** replaces Riya's.
- **Timing (from the measured clips):** 5c 1:08–1:19.5 · 5d 1:19.5–1:25.3 · bridge 1:25.3–1:31 · 6 1:31–1:43 · 7 1:43–1:52 · 8 1:52–2:00.
- **Music: bed D** (modern tech plucks, ~112 BPM, C major; picked 14 Nov over B, C and E on `prototypes/music.html`). Preview: `assets/music/preview_bed_d.mp3`. The tables below predate this pass; `tools/voices.py` LINES is the source of truth.
- File names are `.mp3`; the table below still says `.wav`.
- Regenerate one line: `python3 tools/voices.py generate int_05c_q`. Re-render the previews: `python3 tools/mix_preview.py bed_a`.

## Voices

| ID | Who | Voice (ElevenLabs) |
|---|---|---|
| `NARR` | Narrator | **Ranbir – Warm and Friendly** (`9PvnT6XRzlljoaDG6Knu`), picked 14 Nov. Closest match to the Dr Marwah narrator. |
| `INT` | AI interviewer, **one voice for both interviews** (Kissa Audio and Saffron Frame) | **Briggs** (`uhfmGpskiOe0s3pNnkP6`), picked 14 Nov. Closest match to the SPJIMR interviewer. |
| `RIYA` | Riya Malhotra | **Zara** (`pPd9oF6dS3IEotr2Fmhq`), picked 14 Nov |
| `ARJUN` | Arjun Sethi | **Aashish** (`RpiHVNPKGBg7UmgmrKrN`), picked 14 Nov |

The narrator and interviewer candidates come from ElevenLabs voice-similarity search, run on clips of the Dr Marwah narrator and the SPJIMR interviewer. The interviewer clip was cut to leave out the user's name. `INT_KA` and `INT_SF` below both mean `INT`.

**Settings (starting point):** Multilingual v2 (or v3), stability 0.45–0.55, similarity 0.75, style 0–0.2, speaker boost on. Generate 3 takes per line and pick one. Export WAV, or MP3 at 44.1 kHz / 192 kbps.

**Pronunciation:** AAFT → "A-A-F-T" · TwinCafe → "Twin Cafe" · Kahaani → "Ka-haa-nee" · ₹ amounts as words ("twenty-four rupees") · CPI and CFO letter by letter, if the voice runs them together.

---

## Timeline and lines (2:00)

Changes from the brief's timings are marked **↻**. Interview time grew because the spoken lines run longer than the original windows. Scene 4 gives up 3s to make room.

### Narrator (added in Descript, not played by the HTML)

| File | Scene | Window | TTS text | Est. |
|---|---|---|---|---|
| `narr_01.wav` | 1 | 0:00–0:08 | Placement season, reimagined. Meet A-A-F-T Placements, a Space on Twin Cafe. | 5.6s |
| `narr_02.wav` | 2 | 0:08–0:18 | A Space gives a community its own Twin, private to its members, trained on its documents, with agents built in. | 8.0s |
| `narr_03a.wav` | 3a | 0:18–0:22 | ↻ One Space for the whole batch and the placement cell. | 4.0s |
| `narr_03b.wav` | 3b | 0:22–0:25 | Which companies are coming in December? | 2.4s |
| `narr_03d.wav` | 3d | ↻ 0:34–0:38 | Meridian Analytics is coming. How do I prepare? | 3.2s |
| `narr_04.wav` | 4 | ↻ 0:46–0:53 | Every recruiter comes with its own mock interview. Pick a company. Start practising. | 5.2s |
| `narr_05a.wav` | 5a | ↻ 0:53–0:56 | Students practise with their own CV. | 2.4s |
| `narr_07.wav` | 7 | ↻ 1:41–1:52 | Every attempt ends with a scorecard, a recording and what to practise next. Students practise again as often as they like. | 8.4s |
| `narr_08.wav` | 8 | 1:52–2:00 | *(warmer, slower)* Ask anything. Practise anything. Placement-ready, around the clock. | 4.0s |

Notes:
- **3a ↻:** the brief's line ("For AAFT, it's one Space…") runs ~6.4s in a 4s window, so it's trimmed.
- **3d ↻:** the typed question on screen stays full ("…What do they ask, and how do I prepare?"); the narrator reads the short version. The window grows to 4s, and 3e runs 0:38–0:46.
- **7:** "Students retry" becomes "practise again", to match the **Practice again** button.
- **Space name:** "A-A-F-T Placements" assumes the script name wins over stage's "AAFT Placement Prep" (still open).

### Interview (played by the HTML, so the orb and mic react)

| File | Scene | Window | Speaker | TTS text | On-screen text | Est. |
|---|---|---|---|---|---|---|
| `int_05b_q.wav` | 5b | ↻ 0:56–1:08 | `INT_KA` | You cut cost per install from thirty-eight rupees to twenty-four. Were those listeners worth keeping? | You cut cost per install from ₹38 to ₹24. Were those listeners worth keeping? | 6.0s |
| `riya_05b_a.wav` | 5b | | `RIYA` | Not at first. So I started judging creatives on day-seven retention. | | 4.4s |
| `int_05c_q.wav` | 5c | ↻ 1:08–1:19 | `INT_KA` | Week one. A costs twenty rupees an install, and four percent reach a paid episode. B costs thirty-two, and fourteen percent do. Which do you scale? | Week one. A costs ₹20 an install, and 4% reach a paid episode. B costs ₹32, and 14% do. Which do you scale? | 10.4s |
| `riya_05d_a.wav` | 5d | 1:19–1:30 | `RIYA` | B. Two hundred and twenty-nine rupees per paying listener, against five hundred for A. | "B. ₹229 per paying listener, against ₹500 for A." | 5.6s |
| `int_05d_f.wav` | 5d | | `INT_KA` | Good. Your CFO only sees B's higher cost. Convince her in one line. | Good. Your CFO only sees B's higher cost. Convince her in one line. | 5.2s |
| `int_06_q.wav` | 6 | ↻ 1:30–1:41 | `INT_SF` | Your lead actor is ninety minutes late, and you lose the light at five thirty. What do you do? | Your lead actor is 90 minutes late, and you lose the light at 5:30. What do you do? | 7.6s |
| `arjun_06_a.wav` | 6 | | `ARJUN` | First, I call the first AD, and— | | 2.4s |

Maths: A = ₹20 ÷ 4% = ₹500. B = ₹32 ÷ 14% = ₹228.57 ≈ ₹229.

Gaps: ~0.5s between speakers, ~0.5s hold after the last line in each scene. Arjun's line is cut mid-sentence on purpose; the scene moves on while he's answering.

---

## How the HTML uses the clips

1. Clips go in `assets/audio/` with the file names above.
2. `TIMELINE` lists each scene's clips in order, with gaps. At load, the HTML reads each clip's real duration and lays the scene out from it, so regenerating a line never needs hand retiming.
3. **Interview clips play in the HTML** through Web Audio, and Screen Studio records the system audio. The orb copies the SPJIMR recording (see *Speaking orb* below), and the mic button pulses softly while Riya or Arjun speaks.
4. **Narrator clips are not played** during recording; they go in Descript. Add `?vo=1` to hear them in the HTML, for rehearsing timing.
5. `?debug=1` shows the running timecode and the current clip ID, for lining things up in Descript.
6. **Captions are added in post** (Descript can generate them from the clips).
7. Until the ElevenLabs clips exist, scenes run on **placeholder voices** generated with the macOS voices Rishi (interviewer) and Tara (Riya), under the same file names. Swapping in the real clips is a file drop.


### Speaking orb (from the SPJIMR recording)

Prototype: `prototypes/orb.html` (click or press Space; add `?debug=1` for the level readout).

- A dark plum wedge sweeps **clockwise** around a soft blurred ring, with a sharp leading edge and a tail fading to lavender.
- **While the interviewer speaks:** about 46°/s (one turn every ~8 seconds, as in the recording), plus up to 90°/s more at peak level. The ring grows up to 7% and brightens with the voice, and the faint outer halo breathes with it.
- **While the candidate speaks, or in silence:** the wedge slows to 18°/s at resting size.
- Levels come from a Web Audio AnalyserNode on the clip that's playing, so the motion matches the voice exactly. All values sit in one `ORB` config.
- Not yet checked against the product: whether the real orb reacts while the *candidate* speaks. The recording only shows it while the interviewer speaks.

---

## Generating the voices (no manual export)

**I can generate every clip and set the timings myself through the ElevenLabs API.** You set up access once:

1. Create an API key in ElevenLabs (Profile → API keys) with text-to-speech access.
2. Put it in `aaft-placements/.env` as `ELEVENLABS_API_KEY=…`. Type it into that file yourself; don't paste it into chat. The file is git-ignored.
3. I add `tools/voices.py`, which reads the line table in this file and:
   - **lists your voices** and generates a 1-line sample per role, for you to pick from;
   - **generates each line** with the chosen voice IDs (`/v1/text-to-speech/{voice}/with-timestamps`), saving the MP3 plus word-level timestamps;
   - **measures each clip** and writes `assets/audio/clips.json` (ID, duration, word timings), which the HTML reads to lay out `TIMELINE`;
   - **only regenerates lines whose text changed**, to save credits.
4. Cost: the whole script is about 1,300 characters per full pass, a small fraction of even the starter plan.

Alternative: the official ElevenLabs MCP server (`uvx elevenlabs-mcp`, configured with the same key) lets me call ElevenLabs as a tool. The API script is simpler and repeatable, so I'd use that.

Word timestamps are also free caption data, if you ever want captions burned in rather than added in Descript.

---

## Background music

- **Generate it with ElevenLabs Music** (`/v1/music`) in the same pipeline: a 2:00 instrumental, so there's no stock licence to clear.
- **Brief:** calm, premium, warm; soft piano or felt keys over light pulses and airy pads. ~90 BPM, no vocals, no big drops. It lifts gently into the interview (0:56) and resolves for the end card (1:52).
- **It goes in Descript, not the HTML,** so the dialogue recorded from the HTML stays clean. Duck it about 12 dB under the narrator and the interview.
- Generate 2–3 variations and pick one. If the key lacks the music permission, enable it the same way as Voices.

---

## Recommended (decide)

- **Disclosure line — decided (14 Nov):** a small "Dramatisation · AI-generated voices" line sits at the bottom of the end card.
- **One validation run on stage.** Play Riya's clips into a real Pocket FM case interview on stage. That checks that the product's interviewer really probes CV claims and follows up, which is what the film shows, and it can produce a real scored attempt for scene 7's text.
