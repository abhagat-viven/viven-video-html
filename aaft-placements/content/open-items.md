# Open items before the final recording (14 Nov 2026)

The film runs end to end at 2:15 (pauses added between scenes, 14 Nov). Everything below is either placeholder content or a decision still open.

## Placeholder content (3c shows an orange PLACEHOLDER tag, `?ph=0` hides it; the scorecard has no tag, by request)

1. **3c · December drives answer** is sample text, not a real Space answer. Ask "@space Which companies are coming in December?" once in the staging Space and paste the reply into `TIMELINE.copy.a1` (trim only, swap names through `NAMES`). If the real answer doesn't cite a calendar document, reword `narr_03b` ("…from the placement cell's own drive calendar").
2. **3e · Meridian Analytics answer** is merged from two real answers (both trimmed). Better: ask the exact on-screen question once and use that single reply.
3. **Scene 7 · Arjun's scorecard**: the scores (3/4; criteria 4/3/3/3/4), the What went well / Areas of improvement text, the date and "Attempt 2 of 2" are all placeholders. Run one Situational interview in staging and copy its attempt page into `TIMELINE.copy.score`.

## To match the product

4. **"Selected" Interview type chip** (5t, Case interview): the dark outline is a guess. A screenshot of a selected chip on the New interview page fixes it.
5. **Space name**: staging says "AAFT Placement Prep"; the film says "AAFT Placements" (`SPACE_NAME`, one line; the Twin's name follows it, shown as "AAFT Placements' Twin". Check how the product writes the possessive for a name ending in s).

## Decisions

6. **Pacing**: ~1s pauses now sit where the film changes idea (2:05 → 2:15). Trim any of them in `content/timeline.json`; everything follows. Music: bed D, generated at 2:15 (no stretch).
7. **Interviewer take**: take 1 is in use; take 2 is on `prototypes/takes.html`.

## Housekeeping

8. A stray Attempt 4 on the staging Kissa Audio interview (from an earlier test) can be deleted.
9. Nothing in `aaft-placements/` is committed yet. `deliverables/voices_master.wav` is ~36 MB and is git-ignored (regenerate with `python3 tools/export.py`).
