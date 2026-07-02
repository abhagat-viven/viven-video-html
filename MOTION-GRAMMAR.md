# Viven Motion Grammar

Reference-derived motion vocabulary for all Viven/AskSila video production.
Derived from frame-level analysis of four films: Chronicle (launch), Perplexity Computer (launch), OpenAI GPT-5.5 (launch), Lovable (feature video).

**How to use this file:** Before building any video — (1) pick a STRUCTURE, (2) pick a REGISTER, (3) assemble scenes from named PATTERNS. In Cursor prompts, reference patterns by name: "Use spoken-word reveal (P1) on the opening card, calm register timings."

This file extends the viven-video-production skill. Design system (colors, fonts, Screen Studio rules) lives there and always applies.

---

## 1. STRUCTURES — pick one per video

### S1 — Rhetoric arc (Chronicle)
Indict status quo → Reveal product → Prove (demo) → Objection handling → Social proof → Close.
Use for: launches, category-creation stories, AskSila/TwinUp energy.
Signature: the video makes an argument; motion serves persuasion.

### S2 — Escalating demo (Perplexity)
Prompt → agent works → output. Repeat 2–3x, each use case more agentic than the last. Verb montage close.
Use for: capability showcases, feature videos where the product is the story.
Signature: no title-card theatrics for long stretches; the demo IS the narrative. Quiet serif captions narrate in the product's first-person voice.

### S3 — Claim/proof alternation (OpenAI)
Short bold claim card on empty ground (~2s, plain, centered) → demo proving it → next claim → next proof.
Use for: skeptical-executive audiences. **Default for Prodapt/Sysco CIO video.**
Signature: every assertion immediately pays its debt with evidence. Claims are section labels, not rhetoric.

---

## 2. REGISTERS — pick one per video (sets all timing)

### R1 — Hot (Chronicle)
- Word reveals: 300–350ms/word
- Scene holds: 1.2–1.5s
- Density crescendos, montage rhythm, punchline timing
- Use for: launch films, AskSila consumer content, TwinUp

### R2 — Calm (Perplexity / OpenAI)
- Word reveals: 400–500ms/word
- Scene holds: 1.5–2.5s
- Continuous gentle background motion so holds never freeze
- Use for: Viven Enterprise, CIO-facing, Reading Room follow-ups, feature walkthroughs

Rule: same curves in both registers (ease-out entries, dim/emphasis text). Only tempo and assertion-to-evidence ratio change. Enterprise = R2 unless deliberately arguing otherwise.

---

## 3. PATTERNS

### Text & rhetoric

**P1 — Spoken-word reveal** (Chronicle opener)
Words arrive one at a time at speech pace. Each word enters at ~40% opacity gray, darkens to full black over ~170ms. No movement — pure opacity. Payoff words land last after a slightly longer beat; emphasis words get bold/full-opacity vs dim ~0.6 for connectives.
- Hot: 330ms/word. Calm: 450ms/word. Label/title-card use (existing skill pattern): 180ms/word.
- Rule: 180ms is for labels; 400ms+ is for rhetoric/argument copy.
- CSS: opacity + color transition per word span, staggered setTimeout (existing `playTitleCard` pattern, retimed).

**P9 — Verb montage with dim-trail** (Perplexity close)
Constant noun, swapping verb: "Computer researches → builds → codes → works." Outgoing verb fades to gray FIRST, then new verb arrives dark. ~1.5–2s per beat. Screenshots scroll continuously beside text like a slow filmstrip. Ends collapsing into one summary verb.
- Viven mapping: "Your Twin answers → reviews → drafts → decides → works."

**P11 — Claim card** (OpenAI interstitials)
Bold sans sentence, centered, empty ground, ~2s hold, minimal entrance (fade or P1 at label speed). Connective tissue between proofs. Never decorated.

### Environment & problem-setting

**P2 — Environment as evidence** (Chronicle slide wall)
Background elements accumulate from screen edges in sync with copy, density crescendoing to peak exactly as the sentence completes; at peak the wall may briefly swallow the text. Background is the prosecution's exhibit, not decoration.
- Viven mapping: Scene 1 notification chaos — push density further, time peak to copy climax.

**P17 — Pain marquee** (Lovable close)
Rows of small pills, each naming one specific relatable failure, scrolling horizontally (alternate row directions), then dissolving to logo/product. Pain enumeration as texture; every viewer finds their own wound.
- Viven copy bank: "Waiting two days for a Slack reply" / "The one architect who knows is on leave" / "Answered this same question forty times."
- CSS: two marquee keyframe tracks, pill component, staggered fade-out.

**P15 — Notification cold-open** (Lovable)
Film opens on a single OS-level toast on empty/dark ground. No logo, no product. Cursor clicks it → door into the story. Inverse of chaos-opener: one notification as hook.
- Video 4 candidate: "Your Twin has notes from today's meeting."

### Transitions & camera

**P3 — Zoom-through transition** (Chronicle)
Outgoing text scales up massively — camera pushes THROUGH the letterforms — product UI emerges small on the far side, settles center, push continues into the input box until it fills frame, typing begins. Sections connected by one continuous camera move, not cuts.
- Implementation: scale transforms in HTML; partially achievable via Screen Studio zoom alone. Combine: HTML handles the text blow-up, Screen Studio handles the push-in.

**P16 — Continuous cursor journey** (Lovable)
One unbroken user path: every scene transition is CAUSED by a visible cursor click. Cursor is protagonist stitching scenes; feature video feels like lived experience.
- Implementation: existing fake-cursor component + scene transitions triggered on its click arrival. Default for feature videos.

**P10 — Motion-blur settle** (Perplexity logo)
Wordmark arrives with horizontal motion blur, sharpens into place. ~600ms, once, at close only.
- CSS: filter: blur() on X-translate, animated to 0.

### Agent work & believability

**P7 — Agent work as theater** (Perplexity subagent checklist)
Header via left-to-right color wipe across characters. Task lines arrive one at a time, 400–700ms apart. Line anatomy: status icon + VERB in color (color-coded by action type) + description in dark + model/source tag pill. State grammar: pending = gray, active = colored verb + shimmer, complete = check retained. Variant: stacked pipeline cards with progress bars for sequential jobs.
- Viven mapping: Twin thinking states. Replaces single "Analyzing…" shimmer with a state vocabulary.

**P13 — Cross-app work log** (OpenAI)
P7 plus a surface header naming WHERE work happens: "Using Gmail → Using Slack → Using Github", flipping to past tense on completion ("Used Github"). Capped with micro-summary ("Exploring 4 files, 1 search, 1 list").
- Viven mapping: Twin working across customer stack — the "lives in your tools" claim. Reading Room Jira demo scenes.

**P8 — Speed made visible** (Perplexity stopwatch)
Output rows/items fill in against a running timer counter (0.5s → 1.5s → 2.5s). Turns "it's fast" from claim into observation. Cheap, high believability yield.

**P14 — Artifact chain of evidence** (OpenAI)
Proof escalates through increasingly concrete artifacts: instruction → work log → artifact card with real details (file diffs +69 −24 colored) → automation tag → the actual delivered message shown in the destination tool's own UI. End at the thing a human teammate would have produced.
- Viven mapping: Scene-4 magic moments — show the answer LANDING where work lives (Slack reply, Jira comment), not just the answer.

**P12 — Inline entity pills** (OpenAI)
Tool/app/person names render as colored chips INSIDE sentences — in prompts and in outputs. Integrations become first-class words, demonstrating breadth without a dedicated integrations scene.
- Viven mapping: Twin names, `Jira`, `Salesforce`, source + confidence pills, upstream into the ask itself.

### Product & montage

**P4 — Constant composition, swapped theme** (Chronicle brand montage)
One fixed layout; 3D vertical-axis card flip (~330ms) into the same layout re-skinned. Holds 1.2–1.5s each. EVERY sub-element (pills, swatches, chart bars) re-themes in sync — constancy isolates the one variable, teaching the message wordlessly.
- Maps to existing v8_11 Scene 3 channel-flip; upgrade = sync sub-element re-theming.

**P5 — Checklist rhythm** (Chronicle objections)
Question → evidence montage → accent-colored tick. Repeat 3x, accelerating. Builds "yes, yes, yes" cadence. Use for objection-handling beats in S1.

**P6 — Demo as narrative** (Perplexity)
Real-speed typing with cursor (bold key phrases inside prompt text). Product speaks first-person via quiet serif captions ("Here is the updated model with the biggest changes highlighted:"). Chromeless UI cards floating on warm canvas. Escalating use cases as the argument.
- Fits Viven design system natively (same warm off-white canvas philosophy).

---

## 4. PROJECT MAPPING (current work)

**Video 4 — Meetings Agent:** Structure S2 or S3, Register R2. Candidate assembly: P15 cold-open ("Your Twin has notes…") → P16 cursor journey → P7/P13 for Twin-attended-meeting work states → P14 for the answer landing → P1 (calm) title cards. The unresolved "But wait" midpoint card: consider replacing rhetoric with a P15-style moment instead.

**Prodapt/Sysco CIO video:** Structure S3, Register R2. Claim cards between sections; tacit-knowledge diagram + use cases as proofs; P14 for the Paul Miller hero demo; P17 pain marquee viable as opener texture (enterprise copy bank).

**Hero video (v8_11):** Keep locked structure. Upgrades: Scene 1 gets P2 density-crescendo timing; Scene 3 gets P4 sub-element sync; Scene 4 gets P14 artifact chain + P8 if speed is claimed.

**AskSila/TwinUp content:** Structure S1, Register R1. P1 hot reveals, P17 student-pain marquee, P5 objection ticks.

---

## 5. GAPS & RULES

- **Uncovered area:** diagram/data animation (maturity curve, knowledge-network builds). Next reference collected should be this; nothing else needed.
- **Do not copy:** Chronicle's pace for enterprise audiences; Lovable's saturated gradient identity (Viven warmth comes from off-white, not saturation); 3D spectacle beats (Rubik's-cube-style) — wrong pipeline, wrong aesthetic.
- **Physics defaults (all patterns):** entries ease-out (fast start, soft landing); exits ease-in; nothing linear except continuous marquees/filmstrips; stagger siblings 60–100ms (UI) or per-register word timing (copy); anticipation before large moves; hold ≥ movement — stillness is where meaning lands.
- **Before building any scene, ask:** what should this motion MEAN? Get the metaphor right first; parameters follow mechanically.
