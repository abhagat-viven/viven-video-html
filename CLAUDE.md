# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is
HTML scenes for Viven AI's product videos, built for recording with Screen Studio. Each file contains multiple scenes navigable via keyboard. Scenes are recorded as-is, with zooms/speed-ups/splits added in post.

## GitHub
- Remote: `https://github.com/abhagat-viven/viven-video-html`
- Push only when explicitly instructed

## Preview Server
The preview server runs from a worktree, not the main directory:
- Worktree: `/Users/akashbhagat/viven-video-html/.claude/worktrees/goofy-liskov/`
- After every edit, sync: `cp /Users/akashbhagat/viven-video-html/video2_260331_v10_1.html /Users/akashbhagat/viven-video-html/.claude/worktrees/goofy-liskov/video2_260331_v10_1.html`
- Preview URL: `http://localhost:3456/video2_260331_v10_1.html`
- **201 v1 (storylane):** sync `cp /Users/akashbhagat/viven-video-html/viven-video-html/video2_201_v1_020426.html /Users/akashbhagat/viven-video-html/.claude/worktrees/goofy-liskov/video2_201_v1_020426.html`
- **201 v1 preview:** `http://localhost:3456/video2_201_v1_020426.html`

---

## video2_201_v1_020426.html — Storylane WIP

Working copy for a **new storylane**, built scene-by-scene. Started as a clone of `video2_v3_020426.html` (same single-file pattern: inline CSS/HTML/JS, GSAP, keyboard `switchScene(1–4)`).

Architecture matches the v10 doc below unless this file diverges: `reset[N]` / `run[N]Inner` / `run[N]`, `st()` for timeouts, scene 3→4 push + drag ghost where applicable.

### Scene Map (update as the story is rebuilt)
| Key | Scene | Story Beat |
|-----|-------|------------|
| 1 | Calendar | TBD — revise from v3 clone |
| 2 | Chat + deck | TBD |
| 3 | AI analysis | TBD |
| 4 | Chart → deck | TBD |

---

## video2_260331_v10_1.html — Cinematic Product Overview Video

### Scene Map
| Key | Scene | Story Beat |
|-----|-------|------------|
| 1 | Calendar | QBR meeting block, colleagues accept, Slack arrives from Margaret Chen |
| 2 | Chat with PPT | Upload `Q3_Board_Review_v3.pptx` to Viven, Margaret answers go/delay decision |
| 3 | AI Analysis | Data Analytics Team agent runs retention analysis, draws chart live on canvas |
| 4 | Chart → PPT | Cursor grabs chart from scene 3, viewport pushes left (Mac Spaces style), PPT slides in from right, chart drops in, decision typed, saved |

### Architecture
Single HTML file, no build step. All CSS, HTML, and JS are inline.

**Global utilities** (top of `<script>` block):
- `$('id')` — shorthand for `getElementById`
- `sleep(ms)` — Promise-based delay
- `clearAllTimeouts()` — kills all pending `st()` timeouts on scene switch
- `st(fn, ms)` — tracked `setTimeout` wrapper

**Scene pattern** — every scene follows:
```
reset[N]()        → sync reset to initial state, sets s[N]Resetting=true
run[N]Inner()     → async choreography, checks s[N]Resetting after every await
run[N]()          → calls reset[N]() then run[N]Inner()
```

**`switchScene(num)`** — deactivates all scenes, cleans up scene1's fixed overlays (`#meetExpanded`, `#dimOverlay`), stops scene3 if running (when switching to 4), then calls `reset[N]()` + `run[N]()`.

**Canvas charts** — scene 3 uses `drawChart(progress)` targeting `#s3Canvas`. Scene 4 uses `drawChartOn(progress, canvasId)` generic version. Both use the same `WEEKS`, `APR`, `MAY` data arrays.

**Cursor pattern** — each scene that needs a cursor creates a `position:fixed` div appended to `body`, with `z-index:500`. Movement uses a custom quadratic ease-in-out rAF loop.

**Drag ghost** — `#s4DragGhost` is `position:fixed; z-index:500`, sits above both scene 3 and scene 4 panels during the viewport push transition.

### Key IDs to Know
- `#s3Canvas` — the retention chart canvas in scene 3
- `#s3ChartWrap` — container; needs `.visible` class to show
- `#s3Page` / `.s3-page` — the full scene 3 content column; receives `.s3-slide-out` during transition
- `#s4PptWindow` — the PPT window in scene 4; receives `.slide-in` to enter from right
- `#s4DragGhost` — floating chart thumbnail carried by cursor across both scenes
- `#s2Deck` — the PowerPoint panel in scene 2 (ribbon + thumbnail strip + slide)

### PPT Design (scenes 2 and 4 must match)
- Orange gradient title bar: `linear-gradient(90deg, #c55a11 0%, #e8711a 100%)`
- Left thumbnail strip: 4 slides, slide 3 active (orange border)
- Ribbon tabs: File · Home · Insert · Design · Review
- Main slide: eyebrow + headline "Horizon Module Launch — Go / Delay Decision" + callout + Options A/B + drop zone / chart + decision bullet

### Scene 3→4 Transition (cinematic push)
The intended flow (Option A — auto-chains):
1. Scene 3 runs fully (analysis steps → chart drawn → callout)
2. Cursor appears on chart, grabs it (ghost appears)
3. Full viewport push: `.s3-page` exits left at `-100vw`, `#s4PptWindow` enters from `+100vw` simultaneously — same speed/easing (Mac Spaces feel)
4. Ghost floats fixed above the push, moves to PPT drop zone after push completes
5. Chart drops in, draws, decision typed, "Saved ✓"
- Pressing `4` on the nav jumps directly to the PPT (skips analysis)
- GSAP is the intended animation library for the push (guarantees frame-perfect sync); CDN: `https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js`

---

## Hero Video Files (viven_hero_v*.html)

### Current File
`viven_hero_v8.html` — current working file with Courtney's second round of copy changes.

### Scene Structure (v8)
| Key | Scene | Purpose |
|-----|-------|---------|
| 1 | Bottleneck | Sarah offline, team stuck on Acme Q2 Discount Approval doc |
| 2 | Digital Twin | "What If Sarah's Expertise Was Available / Even When She's Not?" → Twin answers Josh's question |
| 3 | Channel-flip | CS, Engineering, Legal Twins — chunked answer reveal |
| 4 | Network | SVG knowledge network (under redesign) |

### Design Rules
- Accent: purple `#a196eb` — NO orange
- Background: `#f5f3f0`
- Title card font: Roboto, 48px (use scoped CSS override if a line wraps)
- Max-width of `.title-card-text-wrap`: 800px (tc2a overridden to 1000px)
- All timeouts via `st()` wrapper for cleanup

### Title Card Word Count (must match span count exactly)
- tc1: 8 words
- tc2a: 10 words — "What If Sarah's Expertise Was Available / Even When She's Not?"
- tc2b: 5 words — "Meet Sarah's Viven Digital Twin" (single line, no subtitle)
- tc3: 6 words
- tc4: 7 words

### Twin Voice
- Twin speaks AS the expert, not about them
- "we" for team/deal history, "I" for personal judgment
- Questions should sound like messaging the real person directly
