"""Generate the AI portraits listed in content/people.md with Nano Banana Pro (gemini-3-pro-image).

Default backend: Gemini API with GEMINI_API_KEY from aaft-placements/.env (billing enabled 14 Nov).
Alternative: PEOPLE_BACKEND=elevenlabs uses ElevenLabs /v1/flows/image (needs ElevenLabs Pro plan).
Never prints keys.

  python3 tools/people.py            # all people
  python3 tools/people.py riya arjun # just these
  PEOPLE_MODEL=gpt-image-2 python3 tools/people.py riya   # try another model
"""
import json, os, re, sys, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from voices import key as eleven_key  # noqa: E402

API = 'https://api.elevenlabs.io'
MODEL = os.environ.get('PEOPLE_MODEL', 'gemini-3-pro-image')
BACKEND = os.environ.get('PEOPLE_BACKEND', 'gemini')   # 'gemini' (AI Studio key, billed) or 'elevenlabs' (needs Pro plan)


def gemini_key():
    for line in (ROOT / '.env').read_text().splitlines():
        if line.strip().startswith('GEMINI_API_KEY='):
            return line.split('=', 1)[1].strip().strip('"\'')
    sys.exit('GEMINI_API_KEY missing from aaft-placements/.env')


def generate_gemini(prompt):
    import base64
    body = {'contents': [{'parts': [{'text': prompt}]}],
            'generationConfig': {'responseModalities': ['IMAGE'],
                                 'imageConfig': {'aspectRatio': '1:1'} if '2.5' in MODEL else {'aspectRatio': '1:1', 'imageSize': '1K'}}}
    req = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent',
                                 data=json.dumps(body).encode(), method='POST',
                                 headers={'x-goog-api-key': gemini_key(), 'Content-Type': 'application/json'})
    try:
        res = json.loads(urllib.request.urlopen(req, timeout=240).read())
    except urllib.error.HTTPError as e:
        sys.exit(f'HTTP {e.code}: {e.read().decode()[:400]}')
    for part in res['candidates'][0]['content']['parts']:
        d = part.get('inlineData') or part.get('inline_data')
        if d:
            return base64.b64decode(d['data']), d.get('mimeType', d.get('mime_type', 'image/png'))
    sys.exit('no image in response: ' + json.dumps(res)[:400])


def people():
    md = (ROOT / 'content' / 'people.md').read_text()
    style = re.search(r'## Shared style.*?\n> (.+?)\n', md, re.S).group(1).strip()
    rows = re.findall(r'^\| `(\w+)` \| (.+?) \| (.+?) \|$', md, re.M)
    return style, rows


def _req(path, body=None):
    req = urllib.request.Request(API + path, method='POST' if body else 'GET',
                                 data=json.dumps(body).encode() if body else None,
                                 headers={'xi-api-key': eleven_key(), 'Content-Type': 'application/json'})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=120).read())
    except urllib.error.HTTPError as e:
        sys.exit(f'HTTP {e.code} on {path}: {e.read().decode()[:400]}')


def generate_image(prompt):
    body = {'model_id': MODEL, 'prompt': prompt, 'aspect_ratio': '1:1'}
    if MODEL in ('gemini-3-pro-image', 'gemini-3.1-flash-image', 'gpt-image-2'):
        body['resolution'] = '1K'
    gen = _req('/v1/flows/image', body)
    gid = gen['id']
    for _ in range(120):                       # up to ~6 minutes
        st = _req(f'/v1/flows/image/{gid}')
        if st['status'] == 'completed':
            with urllib.request.urlopen(st['content_url'], timeout=120) as r:
                return r.read(), st.get('content_mime_type', 'image/png')
        if st['status'] == 'failed':
            sys.exit(f"generation failed: {st.get('failure_reason')} {st.get('error_message', '')}")
        time.sleep(3)
    sys.exit('timed out waiting for generation ' + gid)


def main(only):
    style, rows = people()
    out = ROOT / 'assets' / 'people'
    out.mkdir(parents=True, exist_ok=True)
    for pid, who, prompt in rows:
        if only and pid not in only:
            continue
        print('generating', pid, f'({MODEL}) …', flush=True)
        full = f'{style} Person: {prompt}'
        data, mime = generate_gemini(full) if BACKEND == 'gemini' else generate_image(full)
        ext = {'image/png': 'png', 'image/jpeg': 'jpg', 'image/webp': 'webp'}.get(mime, 'png')
        f = out / f'{pid}.{ext}'
        f.write_bytes(data)
        print('saved', f.relative_to(ROOT), len(data) // 1024, 'KB')


if __name__ == '__main__':
    main(sys.argv[1:])
