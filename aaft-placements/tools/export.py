"""Deliverables for the edit, all from content/timeline.json + assets/audio/clips.json (the same timing the film uses).

  python3 tools/export.py      -> deliverables/voices_master.wav, captions.srt, music-cue-sheet.md

voices_master.wav starts exactly at film time 0:00 (the white flash frame). No sync beep in the file.
"""
import json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'deliverables'
TL = json.loads((ROOT / 'content/timeline.json').read_text())
CLIPS = json.loads((ROOT / 'assets/audio/clips.json').read_text())


def layout():
    """Absolute start of every clip, exactly as index.html lays them out."""
    out = []
    for b in TL['beats']:
        t = b['start'] + TL['lead']
        for cid in b['clips']:
            out.append({'id': cid, 't': t, 'dur': CLIPS[cid]['duration'], 'beat': b['id'], 'speaker': CLIPS[cid]['speaker']})
            t += CLIPS[cid]['duration'] + TL['gap']
    return out


# ---------------------------------------------------------------- voices_master.wav
def voices_master(V):
    inputs, filt, labels = [], [], []
    for i, v in enumerate(V):
        inputs += ['-i', str(ROOT / CLIPS[v['id']]['file'])]
        ms = round(v['t'] * 1000)
        filt.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}]')
        labels.append(f'[v{i}]')
    filt.append(f'{"".join(labels)}amix=inputs={len(V)}:normalize=0,apad=whole_dur={TL["end"]},atrim=0:{TL["end"]}[out]')
    f = OUT / 'voices_master.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(filt), '-map', '[out]',
                    '-ar', '48000', '-c:a', 'pcm_s24le', str(f)], check=True)
    o = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(f), '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    lufs = re.findall(r'I:\s+(-?[\d.]+) LUFS', o)[-1]; peak = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', o)[-1]
    return f, lufs, peak


# ---------------------------------------------------------------- captions.srt
# On-screen wording (₹, digits, AAFT, TwinCafe), anchored to the spoken word where each caption starts.
# (caption text, index of its first spoken word, expected spoken word)   \n = line break (max ~42 chars a line)
CAPS = {
 'narr_01':   [('Placement season, reimagined.', 0, 'Placement'), ('Meet AAFT Placements,\na Space on TwinCafe.', 3, 'Meet')],
 'narr_02':   [('A Space gives a community its own Twin,', 0, 'A'), ('private to its members,\ntrained on its documents,', 8, 'private'), ('with agents built in.', 16, 'with')],
 'narr_03a':  [('One Space for the whole batch\nand the placement cell.', 0, 'One')],
 'narr_03b':  [('A student asks which companies\nare coming in December.', 0, 'A'), ("The Space answers from the\nplacement cell's own drive calendar.", 9, 'The')],
 'narr_03d':  [('Another asks what Meridian Analytics\nwill ask, and how to prepare.', 0, 'Another'), ("The answer draws on seniors' debriefs\nfrom past Meridian interviews.", 11, 'The')],
 'narr_04':   [('Every recruiter comes with\nits own mock interview.', 0, 'Every'), ('Students pick a company\nand start practising.', 8, 'Students')],
 'narr_05a':  [('Students upload their CV, and get asked\nabout their experience', 0, 'Students'), ("for the role they're applying to.", 10, 'for')],
 'int_05b_q': [('You cut cost per install\nfrom ₹38 to ₹24.', 0, 'You'), ('Were those listeners worth keeping?', 10, 'Were')],
 'riya_05b_a':[('Not at first. So I started judging\ncreatives on day-seven retention.', None, None)],
 'narr_05t':  [('They can practise all types of interviews,', 0, 'They'), ('like case interviews, technical rounds,\nHR discussions and more.', 7, 'like')],
 'int_05c_q': [('Week one. Option A costs ₹20 an install,', 0, 'Week'), ('and 4% reach a paid episode.', 9, 'and'),
               ('Option B costs ₹32, and 14% do.', 16, 'Option'), ('Which do you scale?', 24, 'Which')],
 'riya_05d_a':[('B. ₹229 per paying listener,\nagainst ₹500 for A.', 0, 'B.')],
 'narr_06':   [('From marketing to cinema,', 0, 'From'), ('every school practises\nfor its own roles.', 4, 'every')],
 'int_06_q':  [('Your lead actor is 90 minutes late,', 0, 'Your'), ('and you lose the light at 5:30.', 7, 'and'), ('What do you do?', 15, 'What')],
 'arjun_06_a':[('First, I tell the first AD to reshuffle\nto the scenes we can shoot without him,', 0, 'First,'), ("so we don't lose the light.", 16, 'so')],
 'narr_07':   [('Every attempt ends with a scorecard,', 0, 'Every'), ('a recording and what to practise next.', 6, 'a'), ('Students practise again\nas often as they like.', 13, 'Students')],
 'narr_08':   [('Every question answered.\nEvery interview practised.', 0, 'Every'), ('Placement-ready, around the clock.', 6, 'Placement-ready,')],
}


def srt_time(t):
    ms = max(0, round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'


def captions(V):
    rows = []
    for v in V:
        words, caps = CLIPS[v['id']].get('words'), CAPS[v['id']]
        for k, (text, i0, expect) in enumerate(caps):
            if i0 is None or not words:
                a, b = v['t'] + 0.05, v['t'] + v['dur'] - 0.1
            else:
                assert words[i0][0] == expect, f'{v["id"]}: caption {k} expects "{expect}", word {i0} is "{words[i0][0]}"'
                i1 = (caps[k + 1][1] - 1) if k + 1 < len(caps) else len(words) - 1
                a, b = v['t'] + words[i0][1] - 0.05, v['t'] + words[i1][2] + 0.25
            rows.append([a, b, text])
    rows.sort()
    for i in range(len(rows)):                       # no overlaps; at least 1s on screen where there's room
        nxt = rows[i + 1][0] - 0.04 if i + 1 < len(rows) else TL['end']
        rows[i][1] = min(max(rows[i][1], rows[i][0] + 1.0), nxt)
    f = OUT / 'captions.srt'
    f.write_text(''.join(f'{i}\n{srt_time(a)} --> {srt_time(b)}\n{t}\n\n' for i, (a, b, t) in enumerate(rows, 1)))
    return f, len(rows)


# ---------------------------------------------------------------- music cue sheet
LEVELS = {   # beat id -> (music level, why)
 '1':      ('**Full**, fade in over 1s', 'Title; no dialogue yet, sets the tone'),
 '2':      ('Medium-low under the narrator', 'Explains a Space; small lift as the card pushes into the window'),
 '3a':     ('Low', 'The Space opens; typing and answers need room'),
 '3b':     ('Low', 'Narrator over the December question and answer'),
 '3d':     ('Low', 'Narrator over the Meridian question and answer'),
 '4':      ('Medium', 'Cursor journey: Agents → Placement prep → list'),
 '5a':     ('Medium-low', 'CV upload; Start interview'),
 '5b':     ('**Lowest** (or very soft)', 'Interviewer and Riya speak'),
 '5t':     ('Medium-low lift', 'Narrator only, over the New interview page'),
 '5c':     ('**Lowest**', 'The case question (13s of interviewer)'),
 '5d':     ('**Lowest**', 'Riya answers'),
 'bridge': ('**Swell to medium** under the narrator', 'Marks the change of context: every school'),
 '6':      ('**Lowest**', 'Interviewer and Arjun speak'),
 '7':      ('Medium-low', 'Scorecard; lift slightly from the end-call click'),
 '8':      ('**Full**, resolving; fade out over the last 3s', 'The payoff'),
}
HITS = [   # (beat id, offset from beat start or word anchor, what happens) — optional accents for the editor
 ('2',  'B3a-0.45', 'Push through the Space card into the browser window'),
 ('4',  'B4',       'Scene 4 starts: cursor heads for Agents'),
 ('5b', 'B5b-0.45', 'Window slides right into the call layout'),
 ('5t', 'B5t',      'Back out to the New interview page'),
 ('5c', 'B5c-0.35', 'Into a fresh case call'),
 ('bridge', 'Bbridge', 'Back to the list: every school'),
 ('7',  'W:narr_07:2', 'End-call click ("Every attempt ends…")'),
 ('8',  'B8',       'Window shrinks into the AAFT tile: end card'),
]


def fmt(t):
    return f'{int(t // 60)}:{t % 60:04.1f}'


def cue_sheet(V):
    beats = TL['beats']
    B = {b['id']: b['start'] for b in beats}
    starts = {v['id']: v['t'] for v in V}
    lines = ['# Music cue sheet: AAFT Placements film', '',
             f'Generated by `tools/export.py` from `content/timeline.json`. Runtime **{fmt(TL["end"])}**. '
             'Music is bed D (`assets/music/bed_d.mp3`: modern tech plucks, ~112 BPM, C major), added in Canva. Film time 0:00 = the white flash frame '
             '(line `voices_master.wav` and the music up to it).', '',
             '## Levels by beat', '', '| Time | Beat | Music level | Why |', '|---|---|---|---|']
    for i, b in enumerate(beats):
        end = beats[i + 1]['start'] if i + 1 < len(beats) else TL['end']
        lv, why = LEVELS[b['id']]
        lines.append(f'| {fmt(b["start"])}–{fmt(end)} | {b["id"]} · {b["name"]} | {lv} | {why} |')
    lines += ['', '## Hit points (optional accents)', '', '| Time | Moment |', '|---|---|']
    for _, spec, what in HITS:
        if spec.startswith('W:'):
            _, cid, n = spec.split(':'); t = starts[cid] + CLIPS[cid]['words'][int(n)][1]
        else:
            m = re.match(r'B([0-9a-z]+)([+-][\d.]+)?$', spec); t = B[m.group(1)] + float(m.group(2) or 0)
        lines.append(f'| {fmt(t)} | {what} |')
    lines += ['', '## Voice regions (duck the music here)', '', '| From | To | Speaker | Line |', '|---|---|---|---|']
    names = {'NARR': 'Narrator', 'INT': 'Interviewer', 'RIYA': 'Riya', 'ARJUN': 'Arjun'}
    for v in V:
        lines.append(f'| {fmt(v["t"])} | {fmt(v["t"] + v["dur"])} | {names[v["speaker"]]} | {CLIPS[v["id"]]["text"]} |')
    f = OUT / 'music-cue-sheet.md'
    f.write_text('\n'.join(lines) + '\n')
    return f


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    V = layout()
    f, lufs, peak = voices_master(V); print(f'wrote {f.relative_to(ROOT)}  ({TL["end"]}s, {lufs} LUFS, peak {peak} dBFS)')
    f, n = captions(V); print(f'wrote {f.relative_to(ROOT)}  ({n} captions)')
    f = cue_sheet(V); print(f'wrote {f.relative_to(ROOT)}')
