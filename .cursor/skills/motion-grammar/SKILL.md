---
name: motion-grammar
description: Applies Viven motion grammar (structures S1–S3, registers R1–R2, patterns P1–P17) when building or retiming HTML video scenes for Screen Studio. Use when authoring viven_*.html scenes, syncing beats to voiceover, choosing title-card vs demo choreography, or when the user mentions motion grammar, motion patterns, or MOTION-GRAMMAR.md.
---

# Viven Motion Grammar

Reference-derived motion vocabulary for Viven/AskSila Screen Studio HTML videos.

**Full pattern catalog:** [reference.md](reference.md) (source: `MOTION-GRAMMAR.md` in repo root)

**Companion:** design system + Screen Studio rules live in `viven-video-production` skill and `CLAUDE.md` — always apply those alongside this grammar.

---

## Before building any scene

1. **Pick STRUCTURE** (S1, S2, or S3) — one per video
2. **Pick REGISTER** (R1 hot or R2 calm) — sets all timing
3. **Assemble scenes from named PATTERNS** — cite by ID in prompts and code comments
4. **Ask:** what should this motion *mean*? Metaphor first; parameters follow.

In Cursor prompts, reference patterns by name: *"Use spoken-word reveal (P1) on the opening card, calm register timings."*

---

## Structures (pick one)

| ID | Name | Use for |
|----|------|---------|
| **S1** | Rhetoric arc | Launches, category creation, AskSila/TwinUp — indict → reveal → prove → objections → close |
| **S2** | Escalating demo | Capability showcases — prompt → agent works → output, repeat 2–3×, verb montage close |
| **S3** | Claim/proof alternation | Skeptical executives, **Prodapt/Sysco CIO default** — bold claim ~2s → demo proof → repeat |

---

## Registers (sets tempo)

| ID | Tempo | Word reveal | Scene hold | Use for |
|----|-------|-------------|------------|---------|
| **R1** Hot | Fast | 300–350ms/word | 1.2–1.5s | Launches, AskSila, TwinUp |
| **R2** Calm | Slow | 400–500ms/word | 1.5–2.5s | Enterprise, CIO, Viven EA, feature walkthroughs |

**Rules:**
- Same easing curves in both registers (ease-out entries, dim/emphasis text)
- Enterprise = **R2** unless deliberately arguing otherwise
- **180ms/word** = labels/title cards only; **400ms+** = rhetoric/argument copy (P1)

---

## Pattern quick index

| ID | Name | When to use |
|----|------|-------------|
| P1 | Spoken-word reveal | Opener rhetoric; opacity-only word stagger |
| P2 | Environment as evidence | Background density crescendo to copy climax |
| P3 | Zoom-through transition | Push through text into product UI |
| P4 | Constant composition, swapped theme | Channel-flip montage; sync sub-elements |
| P5 | Checklist rhythm | Objection handling: Q → evidence → tick ×3 |
| P6 | Demo as narrative | Real-speed typing, first-person captions |
| P7 | Agent work as theater | Twin thinking: checklist lines, state grammar |
| P8 | Speed made visible | Timer counter as rows fill |
| P9 | Verb montage with dim-trail | Close: constant noun, swapping verbs |
| P10 | Motion-blur settle | Logo close, ~600ms blur → sharp |
| P11 | Claim card | S3 interstitial: bold sentence, empty ground, ~2s |
| P12 | Inline entity pills | Tool/person chips inside sentences |
| P13 | Cross-app work log | P7 + surface header (Gmail → Slack → Github) |
| P14 | Artifact chain of evidence | Proof escalates to delivered artifact in destination UI |
| P15 | Notification cold-open | Single OS toast as hook |
| P16 | Continuous cursor journey | Every transition caused by cursor click |
| P17 | Pain marquee | Scrolling failure pills → dissolve to logo |

See [reference.md](reference.md) for implementation notes, CSS hints, and Viven copy mappings.

---

## Project defaults (current work)

| Project | Structure | Register | Key patterns |
|---------|-----------|----------|--------------|
| **Prodapt/Sysco CIO** (`viven_ea.html`) | S3 | R2 | P11 claim cards, P7/P13 thinking, P14 Paul Miller demo, P17 opener |
| **Video 4 — Meetings** | S2 or S3 | R2 | P15 cold-open, P16 cursor journey, P7/P13, P14, P1 calm |
| **Hero v8_11** | Locked | — | P2 Scene 1, P4 Scene 3, P14+P8 Scene 4 |
| **AskSila/TwinUp** | S1 | R1 | P1 hot, P17 student pain, P5 objection ticks |

---

## Implementation in this repo

HTML video files (`viven_*.html`, `video2_*.html`) use:

- `playTitleCard()` — P1 at label speed (~180ms/word stagger via `st()`)
- `st()` / `sleep()` — all timed beats; must respect pause/resume
- `streamHTML()` — response streaming; tune `streamSpeed` per register
- Scene pattern: `reset[N]()` → `run[N]Inner()` with `s[N]Resetting` guards

When retiming to voiceover: change **intra-scene delays only** unless user switches scenes manually during recording.

---

## Physics defaults (all patterns)

- Entries: ease-out (fast start, soft landing)
- Exits: ease-in
- Linear motion: continuous marquees/filmstrips only
- Stagger siblings: 60–100ms (UI) or per-register word timing (copy)
- Anticipation before large moves
- **Hold ≥ movement** — stillness is where meaning lands

---

## Do not copy

- Chronicle pace for enterprise audiences
- Lovable saturated gradients (Viven warmth = off-white, not saturation)
- 3D spectacle beats (Rubik's-cube-style) — wrong pipeline, wrong aesthetic

---

## Workflow checklist

```
- [ ] Structure (S1/S2/S3) chosen for this video
- [ ] Register (R1/R2) chosen — enterprise defaults to R2
- [ ] Each scene mapped to 1–2 patterns by ID
- [ ] Motion meaning stated before coding timings
- [ ] Title cards use label speed; rhetoric uses register speed
- [ ] Holds long enough for VO; background drift during holds (R2)
- [ ] Pattern names cited in commit/PR description
```

For full pattern specs, copy banks, and gap notes, read [reference.md](reference.md).
