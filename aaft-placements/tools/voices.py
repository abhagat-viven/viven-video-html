"""ElevenLabs helper for the AAFT Placements film.

Reads ELEVENLABS_API_KEY from aaft-placements/.env (git-ignored). Never prints the key.

  python3 tools/voices.py quota               # characters used / left this period
  python3 tools/voices.py list [--indian]     # voices available to this account
  python3 tools/voices.py sample ROLE VOICE_ID [VOICE_ID ...]
                                              # one sample line per voice, saved to prototypes/voice-samples/
  python3 tools/voices.py generate [LINE_ID ...]
                                              # final clips -> assets/audio/*.mp3 + clips.json (durations, word timings)
  python3 tools/voices.py music NAME "PROMPT" LENGTH_MS
                                              # background music -> assets/music/NAME.mp3
"""
import json, sys, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = 'https://api.elevenlabs.io'

# Samples use real script lines, so a chosen sample doubles as the final clip.
SAMPLE_LINES = {
    'NARR':   ('narr_08',    'Ask anything. Practise anything. Placement-ready, around the clock.'),
    'INT_KA': ('int_05d_f',  "Good. Your CFO only sees B's higher cost. Convince her in one line."),
    'RIYA':   ('riya_05b_a', 'Not at first. So I started judging creatives on day-seven retention.'),
    'INT_SF': ('int_06_q',   'Your lead actor is ninety minutes late, and you lose the light at five thirty. What do you do?'),
    'ARJUN':  ('arjun_06_a', 'First, I call the first AD, and—'),
}
SETTINGS = {'stability': .5, 'similarity_boost': .75, 'style': .1, 'use_speaker_boost': True}
MODEL = 'eleven_multilingual_v2'


def _key_values():
    vals = []
    for line in (ROOT / '.env').read_text().splitlines():
        line = line.strip()
        if line.startswith('ELEVENLABS_API_KEY='):
            vals.append(line.split('=', 1)[1].strip().strip('"\''))
    return vals


def key():
    vals = _key_values()
    for v in reversed(vals):            # prefer the newest real key (sk_...)
        if v.startswith('sk_'):
            return v
    if vals:
        return vals[-1]
    sys.exit('ELEVENLABS_API_KEY missing from aaft-placements/.env')


def check():
    import time
    for p in [ROOT / '.env', ROOT.parent / '.env', ROOT / '.env.local', ROOT / 'tools' / '.env']:
        if p.exists():
            has = 'ELEVENLABS_API_KEY' in p.read_text()
            print(f'{p}: modified {time.strftime("%H:%M:%S", time.localtime(p.stat().st_mtime))}, has key line={has}')
    vals = _key_values()
    print(f'{len(vals)} ELEVENLABS_API_KEY line(s): ' +
          ', '.join(f"#{i+1} starts with sk_={v.startswith('sk_')} length={len(v)}" for i, v in enumerate(vals)))


def call(path, body=None, raw=False, timeout=60):
    req = urllib.request.Request(API + path, method='POST' if body else 'GET',
                                 data=json.dumps(body).encode() if body else None,
                                 headers={'xi-api-key': key(), 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f'HTTP {e.code} on {path}: {e.read().decode()[:300]}')
    return data if raw else json.loads(data)


def quota():
    s = call('/v1/user/subscription')
    used, limit = s.get('character_count', 0), s.get('character_limit', 0)
    print(f"tier={s.get('tier')}  characters used {used:,} of {limit:,}  ({limit-used:,} left)")


def list_voices(indian_only):
    vs = call('/v2/voices?page_size=100').get('voices', [])
    rows = []
    for v in vs:
        lab = v.get('labels') or {}
        acc = (lab.get('accent') or '').lower()
        if indian_only and 'indian' not in acc and 'hindi' not in (v.get('name', '') + acc).lower():
            continue
        rows.append((v['name'], v['voice_id'], lab.get('gender', ''), lab.get('age', ''), lab.get('accent', ''),
                     lab.get('use_case', lab.get('descriptive', '')), v.get('category', '')))
    for r in sorted(rows):
        print(' | '.join(str(x) for x in r))
    print(f'{len(rows)} voices')


def library(gender, age):
    q = f'/v1/shared-voices?page_size=40&language=en&accent=indian&gender={gender}&age={age}&sort=usage_character_count_1y'
    for v in call(q).get('voices', []):
        print(' | '.join(str(v.get(k, '')) for k in
              ('name', 'voice_id', 'public_owner_id', 'gender', 'age', 'accent', 'use_case', 'descriptive', 'cloned_by_count')),
              '|', (v.get('description') or '')[:90].replace('\n', ' '))


def similar(audio_path, top_k=10):
    """Find library voices that sound like a reference clip (POST /v1/similar-voices)."""
    import uuid
    boundary = uuid.uuid4().hex
    data = Path(audio_path).read_bytes()
    body = (f'--{boundary}\r\nContent-Disposition: form-data; name="top_k"\r\n\r\n{top_k}\r\n'
            f'--{boundary}\r\nContent-Disposition: form-data; name="audio_file"; filename="ref.mp3"\r\n'
            f'Content-Type: audio/mpeg\r\n\r\n').encode() + data + f'\r\n--{boundary}--\r\n'.encode()
    req = urllib.request.Request(API + '/v1/similar-voices', data=body, method='POST',
                                 headers={'xi-api-key': key(), 'Content-Type': f'multipart/form-data; boundary={boundary}'})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            res = json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f'HTTP {e.code} on similar-voices: {e.read().decode()[:300]}')
    for v in res.get('voices', []):
        print(' | '.join(str(v.get(k, '')) for k in ('name', 'voice_id', 'gender', 'age', 'accent', 'use_case', 'descriptive')),
              '|', (v.get('description') or '')[:80].replace('\n', ' '))


def sample(role, ids):
    line_id, text = SAMPLE_LINES[role]
    out = ROOT / 'prototypes' / 'voice-samples'
    out.mkdir(parents=True, exist_ok=True)
    for vid in ids:
        name = vid.split('=')[0] if '=' in vid else vid
        vid = vid.split('=')[-1]
        audio = call(f'/v1/text-to-speech/{vid}?output_format=mp3_44100_128',
                     {'text': text, 'model_id': MODEL, 'voice_settings': SETTINGS}, raw=True)
        f = out / f'{role}__{name}__{line_id}.mp3'
        f.write_bytes(audio)
        print('saved', f.relative_to(ROOT), len(text), 'chars')

# ---------------------------------------------------------------- final lines
# Picked 14 Nov 2026. One interviewer voice covers both interviews.
# 14 Nov: CFO follow-up (int_05d_f) retired; bridge narr_06 added; Arjun's answer completed.
# 14 Nov (pass 3g): narrator in third person throughout; 03b/03d now say the typed question AND where the answer comes from (film plays on an event screen, text is hard to read).
# 14 Nov (3rd pass): 5a now about uploading the CV for the role; narr_05t (interview types) added; ("school" kept — AAFT calls them schools).
VOICES = {
    'NARR':  '9PvnT6XRzlljoaDG6Knu',   # Ranbir – Warm and Friendly (closest to the Dr Marwah narrator)
    'INT':   'uhfmGpskiOe0s3pNnkP6',   # Briggs (closest to the SPJIMR interviewer)
    'RIYA':  'pPd9oF6dS3IEotr2Fmhq',   # Zara
    'ARJUN': 'RpiHVNPKGBg7UmgmrKrN',   # Aashish
}
# (file id, speaker, TTS text) — source of truth mirrors content/voice-script.md
LINES = [
    ('narr_01',    'NARR',  'Placement season, reimagined. Meet A-A-F-T Placements, a Space on Twin Cafe.'),
    ('narr_02',    'NARR',  'A Space gives a community its own Twin, private to its members, trained on its documents, with agents built in.'),
    ('narr_03a',   'NARR',  'One Space for the whole batch and the placement cell.'),
    ('narr_03b',   'NARR',  'A student asks which companies are coming in December. The Space answers from the placement cell\'s own drive calendar.'),
    ('narr_03d',   'NARR',  'Another asks what Meridian Analytics will ask, and how to prepare. The answer draws on seniors\' debriefs from past Meridian interviews.'),
    ('narr_04',    'NARR',  'Every recruiter comes with its own mock interview. Students pick a company and start practising.'),
    ('narr_05a',   'NARR',  "Students upload their CV, and get asked about their experience for the role they're applying to."),
    ('narr_05t',   'NARR',  'They can practise all types of interviews, like case interviews, technical rounds, HR discussions and more.'),   # director's wording, 14 Nov
    ('narr_06',    'NARR',  'From marketing to cinema, every school practises for its own roles.'),   # AAFT's own term: "schools"
    ('narr_07',    'NARR',  'Every attempt ends with a scorecard, a recording and what to practise next. Students practise again as often as they like.'),
    ('narr_08',    'NARR',  'Every question answered. Every interview practised. Placement-ready, around the clock.'),
    ('int_05b_q',  'INT',   'You cut cost per install from thirty-eight rupees to twenty-four. Were those listeners worth keeping?'),
    ('riya_05b_a', 'RIYA',  'Not at first. So I started judging creatives on day-seven retention.'),
    ('int_05c_q',  'INT',   'Week one. Option A costs twenty rupees an install, and four percent reach a paid episode. Option B costs thirty-two, and fourteen percent do. Which do you scale?'),
    ('riya_05d_a', 'RIYA',  'B. Two hundred and twenty-nine rupees per paying listener, against five hundred for A.'),
    ('int_06_q',   'INT',   'Your lead actor is ninety minutes late, and you lose the light at five thirty. What do you do?'),
    ('arjun_06_a', 'ARJUN', "First, I tell the first AD to reshuffle to the scenes we can shoot without him, so we don't lose the light."),
]
# Approved sample takes reused as final clips (same text, same voice, same settings).
REUSE = {
    'riya_05b_a': 'RIYA__Zara__riya_05b_a.mp3',
}


def duration(path):
    import subprocess
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)],
                         capture_output=True, text=True).stdout.strip()
    return round(float(out), 3)


def normalize(f, target=-16):
    """Loudness-normalise a clip in place to `target` LUFS; the untouched take is kept in raw/."""
    import shutil, subprocess
    raw = f.parent / 'raw'
    raw.mkdir(exist_ok=True)
    src = raw / f.name
    if not src.exists() or src.stat().st_mtime < f.stat().st_mtime:
        shutil.copy(f, src)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-af', f'loudnorm=I={target}:TP=-1.5:LRA=11',
                    '-ar', '44100', '-b:a', '192k', str(f)], check=True)


def generate(only=None):
    """Generate every line (skipping unchanged ones), then write assets/audio/clips.json."""
    import base64, hashlib, shutil
    out = ROOT / 'assets' / 'audio'
    out.mkdir(parents=True, exist_ok=True)
    manifest_path = out / 'clips.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    for lid, spk, text in LINES:
        if only and lid not in only:
            continue
        h = hashlib.sha1(f'{VOICES[spk]}|{MODEL}|{json.dumps(SETTINGS)}|{text}'.encode()).hexdigest()[:12]
        f = out / f'{lid}.mp3'
        if f.exists() and manifest.get(lid, {}).get('hash') == h and not only:
            print('unchanged', lid); continue
        words = None
        if lid in REUSE and not f.exists():
            shutil.copy(ROOT / 'prototypes' / 'voice-samples' / REUSE[lid], f)
            print('reused sample', lid)
        else:
            res = call(f'/v1/text-to-speech/{VOICES[spk]}/with-timestamps?output_format=mp3_44100_128',
                       {'text': text, 'model_id': MODEL, 'voice_settings': SETTINGS})
            f.write_bytes(base64.b64decode(res['audio_base64']))
            al = res.get('alignment') or {}
            words = _words(al.get('characters', []), al.get('character_start_times_seconds', []),
                           al.get('character_end_times_seconds', []))
            print('generated', lid, len(text), 'chars')
        normalize(f)
        manifest[lid] = {'speaker': spk, 'text': text, 'file': f'assets/audio/{lid}.mp3',
                         'duration': duration(f), 'hash': h, 'words': words}
    manifest_path.write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
    print('wrote', manifest_path.relative_to(ROOT))


def _words(chars, starts, ends):
    words, cur, t0 = [], '', None
    for c, s, e in zip(chars, starts, ends):
        if c.isspace():
            if cur: words.append([cur, round(t0, 3), round(prev_e, 3)]); cur = ''
            continue
        if not cur: t0 = s
        cur += c; prev_e = e
    if cur: words.append([cur, round(t0, 3), round(prev_e, 3)])
    return words


def align(ids):
    """Word timings for clips that came from reused samples (no timestamps), via /v1/forced-alignment."""
    import uuid
    mpath = ROOT / 'assets' / 'audio' / 'clips.json'
    m = json.loads(mpath.read_text())
    for lid in ids or [k for k, v in m.items() if not v.get('words')]:
        audio = (ROOT / m[lid]['file']).read_bytes()
        b = uuid.uuid4().hex
        body = (f'--{b}\r\nContent-Disposition: form-data; name="text"\r\n\r\n{m[lid]["text"]}\r\n'
                f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="a.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n'
                ).encode() + audio + f'\r\n--{b}--\r\n'.encode()
        req = urllib.request.Request(API + '/v1/forced-alignment', data=body, method='POST',
                                     headers={'xi-api-key': key(), 'Content-Type': f'multipart/form-data; boundary={b}'})
        try:
            res = json.loads(urllib.request.urlopen(req, timeout=120).read())
        except urllib.error.HTTPError as e:
            sys.exit(f'HTTP {e.code} on forced-alignment: {e.read().decode()[:300]}')
        m[lid]['words'] = [[w['text'], round(w['start'], 3), round(w['end'], 3)]
                           for w in res.get('words', []) if w['text'].strip()]
        print('aligned', lid, len(m[lid]['words']), 'words')
    mpath.write_text(json.dumps(m, indent=1, ensure_ascii=False))


# ---------------------------------------------------------------- one-take recording
# One speaker's lines read as ONE continuous performance, so timbre, energy and pace match across the film.
# onetake SPK N  -> N full takes in assets/audio/takes/ (+ alignment json)
# cut SPK K      -> slices take K into the usual per-line clips (same ids), updates clips.json
ONETAKE_SETTINGS = {'stability': .6, 'similarity_boost': .75, 'style': .05, 'use_speaker_boost': True}
BREAK = ' <break time="1.0s" /> '


def _post(path, body, timeout=240):
    req = urllib.request.Request(API + path, method='POST', data=json.dumps(body).encode(),
                                 headers={'xi-api-key': key(), 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f'HTTP {e.code} on {path}: {e.read().decode()[:300]}')


def _loudnorm_2pass(src, dst, target=-16):
    """Accurate, linear (no dynamic pumping) loudness normalisation of a whole take."""
    import subprocess, re
    p1 = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(src), '-af',
                         f'loudnorm=I={target}:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                        capture_output=True, text=True).stderr
    m = json.loads(p1[p1.rindex('{'):p1.rindex('}') + 1])
    af = (f'loudnorm=I={target}:TP=-1.5:LRA=11:measured_I={m["input_i"]}:measured_TP={m["input_tp"]}:'
          f'measured_LRA={m["input_lra"]}:measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-af', af, '-ar', '44100', '-b:a', '192k', str(dst)], check=True)


def onetake(spk, n=3):
    import base64
    lines = [(lid, text) for lid, s, text in LINES if s == spk]
    script = BREAK.join(t for _, t in lines)
    out = ROOT / 'assets' / 'audio' / 'takes'
    out.mkdir(parents=True, exist_ok=True)
    for k in range(1, n + 1):
        res = _post(f'/v1/text-to-speech/{VOICES[spk]}/with-timestamps?output_format=mp3_44100_128',
                    {'text': script, 'model_id': MODEL, 'voice_settings': ONETAKE_SETTINGS, 'seed': 1000 + k})
        raw = out / f'{spk.lower()}_take{k}.raw.mp3'
        raw.write_bytes(base64.b64decode(res['audio_base64']))
        (out / f'{spk.lower()}_take{k}.json').write_text(json.dumps(
            {'lines': lines, 'alignment': res.get('alignment')}, ensure_ascii=False))
        _loudnorm_2pass(raw, out / f'{spk.lower()}_take{k}.mp3')
        print(f'take {k}: {duration(out / f"{spk.lower()}_take{k}.mp3")}s, {len(script)} chars')


def _line_spans(take_json):
    """(lid, text, t_start, t_end, words) for every line, located in the take's character alignment."""
    d = json.loads(take_json.read_text())
    al = d['alignment']; chars = al['characters']
    st, en = al['character_start_times_seconds'], al['character_end_times_seconds']
    joined = ''.join(chars)
    spans, pos = [], 0
    for lid, text in d['lines']:
        i = joined.find(text, pos)
        if i < 0:
            sys.exit(f'{lid}: text not found in alignment')
        j = i + len(text)
        spans.append((lid, text, st[i], en[j - 1], _words(chars[i:j], st[i:j], en[i:j])))
        pos = j
    return spans


def cut(spk, k):
    import subprocess, hashlib
    takes = ROOT / 'assets' / 'audio' / 'takes'
    src = takes / f'{spk.lower()}_take{k}.mp3'
    spans = _line_spans(takes / f'{spk.lower()}_take{k}.json')
    mpath = ROOT / 'assets' / 'audio' / 'clips.json'
    m = json.loads(mpath.read_text())
    for n, (lid, text, t0, t1, words) in enumerate(spans):
        a = max(0.0, t0 - 0.06)
        nxt = spans[n + 1][2] if n + 1 < len(spans) else t1 + 1
        b = min(t1 + 0.25, nxt - 0.1)
        f = ROOT / 'assets' / 'audio' / f'{lid}.mp3'
        d = b - a
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-t', f'{d:.3f}', '-i', str(src),
                        '-af', f'afade=t=in:d=0.01,afade=t=out:st={d - 0.03:.3f}:d=0.03', '-ar', '44100', '-b:a', '192k', str(f)],
                       check=True)
        m[lid] = {'speaker': spk, 'text': text, 'file': f'assets/audio/{lid}.mp3', 'duration': duration(f),
                  'hash': 'onetake-' + hashlib.sha1(f'{spk}{k}{text}'.encode()).hexdigest()[:8], 'take': f'{spk.lower()}_take{k}',
                  'words': [[w, round(s - a, 3), round(e - a, 3)] for w, s, e in words]}
        print(f'{lid:11} {m[lid]["duration"]:5.2f}s  {len(words)/(t1-t0):4.2f} w/s')
    mpath.write_text(json.dumps(m, indent=1, ensure_ascii=False))


def music(name, prompt, ms):
    out = ROOT / 'assets' / 'music'
    out.mkdir(parents=True, exist_ok=True)
    audio = call('/v1/music?output_format=mp3_44100_192',
                 {'prompt': prompt, 'music_length_ms': ms, 'model_id': 'music_v1'}, raw=True, timeout=300)
    f = out / f'{name}.mp3'
    f.write_bytes(audio)
    print('saved', f.relative_to(ROOT), duration(f), 's')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'generate': generate(sys.argv[2:] or None)
    elif cmd == 'music': music(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    elif cmd == 'align': align(sys.argv[2:])
    elif cmd == 'onetake': onetake(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 3)
    elif cmd == 'cut': cut(sys.argv[2], int(sys.argv[3]))
    elif cmd == 'check': check()
    elif cmd == 'quota': quota()
    elif cmd == 'list': list_voices('--indian' in sys.argv)
    elif cmd == 'library': library(sys.argv[2], sys.argv[3])
    elif cmd == 'similar': similar(sys.argv[2])
    elif cmd == 'sample': sample(sys.argv[2], sys.argv[3:])
    else: print(__doc__)
