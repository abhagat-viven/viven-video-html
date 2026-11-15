"""Render a rough 2:00 soundtrack preview: every voice clip at its planned time, music bed ducked underneath.

  python3 tools/mix_preview.py            -> assets/music/preview_bed_b.mp3, bed at the per-beat levels in content/timeline.json
                                             (the same levels index.html?music=1 plays)
  python3 tools/mix_preview.py bed_a      -> assets/music/preview_bed_a.mp3, flat -14 dB
  python3 tools/mix_preview.py none       -> voices only

Start times here are the planned TIMELINE (seconds). The HTML build reads the same clip files.
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# timing lives in content/timeline.json (shared with index.html and prototypes/soundtrack.html)
TL = json.loads((ROOT / 'content/timeline.json').read_text())
GAP, LEAD, END = TL['gap'], TL['lead'], TL['end']
PLAN = [(b['start'], b['clips']) for b in TL['beats']]


def music_gain_expr():
    """Piecewise-linear gain over film time, built exactly like scheduleMusic() in index.html."""
    M, beats = TL['music'], TL['beats']
    lv = lambda bid: 10 ** (M['db'][bid] / 20)
    ev = [(0.0, 0.0001), (M['fade_in'], lv(beats[0]['id']))]
    for prev, b in zip(beats, beats[1:]):
        a, z = b['start'] - M['ramp'] / 2, b['start'] + M['ramp'] / 2
        if a > ev[-1][0] + 0.01:
            ev += [(a, lv(prev['id'])), (z, lv(b['id']))]
    fo = END - M['fade_out']
    if fo > ev[-1][0]:
        ev.append((fo, lv(beats[-1]['id'])))
    ev.append((END, 0.0001))
    expr = f'{ev[-1][1]:.5f}'
    for (a, va), (b, vb) in reversed(list(zip(ev, ev[1:]))):
        expr = f"if(lt(t,{b:.3f}),{va:.5f}+({vb - va:.5f})*(t-{a:.3f})/{max(b - a, 1e-3):.3f},{expr})"
    return expr


def main(bed, music_file=None):
    clips = json.loads((ROOT / 'assets/audio/clips.json').read_text())
    inputs, filters, labels, t_list = [], [], [], []
    for start, ids in PLAN:
        t = start + LEAD
        for cid in ids:
            inputs += ['-i', str(ROOT / clips[cid]['file'])]
            t_list.append((cid, round(t, 2)))
            i = len(inputs) // 2 - 1
            ms = int(t * 1000)
            filters.append(f'[{i}:a]aresample=44100,aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}]')
            labels.append(f'[v{i}]')
            t += clips[cid]['duration'] + GAP
    n = len(labels)
    filters.append(f'{"".join(labels)}amix=inputs={n}:normalize=0,apad=whole_dur={END}[vox]')
    out_name = 'preview_voices_only' if bed == 'none' else 'preview_' + Path(TL['music']['file']).stem.replace('_fit', '') if bed == 'timeline' else f'preview_{bed}'
    if music_file:                     # same per-beat levels, another bed: python3 tools/mix_preview.py bed_c assets/music/bed_c_fit.mp3
        out_name, bed = f'preview_{bed}', 'timeline'
    if bed == 'timeline':
        inputs += ['-i', str(ROOT / (music_file or TL['music']['file']))]
        filters.append(f"[{n}:a]aresample=44100,aformat=channel_layouts=stereo,atrim=0:{END},volume='{music_gain_expr()}':eval=frame[bed]")
        filters.append(f'[vox][bed]amix=inputs=2:normalize=0,atrim=0:{END}[out]')
    elif bed != 'none':
        inputs += ['-i', str(ROOT / f'assets/music/{bed}.mp3')]
        m = n
        # music at -14 dB under voice, 2s fade-in, 3s fade-out ending at 2:00
        filters.append(f'[{m}:a]aresample=44100,aformat=channel_layouts=stereo,atrim=0:{END},volume=-14dB,'
                       f'afade=t=in:d=2,afade=t=out:st={END-3}:d=3[bed]')
        filters.append(f'[vox][bed]amix=inputs=2:normalize=0,atrim=0:{END}[out]')
    else:
        filters.append(f'[vox]atrim=0:{END}[out]')
    out = ROOT / 'assets/music' / f'{out_name}.mp3'
    cmd = ['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(filters), '-map', '[out]',
           '-b:a', '192k', str(out)]
    subprocess.run(cmd, check=True)
    print('wrote', out.relative_to(ROOT))
    for cid, t in t_list:
        print(f'  {int(t//60)}:{t%60:05.2f}  {cid}  ({clips[cid]["duration"]:.2f}s)')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'timeline', sys.argv[2] if len(sys.argv) > 2 else None)
