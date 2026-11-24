#!/usr/bin/env python3
"""Word-timed transcript for a clip, in Spanish or English (Spanglish too). Writes a flat word list:
[{"text","start","end"}, ...] and, next to it, language.json ({"language": "es"|"en", "source", "model"}).
Usage: python3 transcribe.py <video-or-audio> <out.json> [--language es|en|auto]

Language: --language wins; else brand.json "language" ("es" / "en"; "auto" or missing = detect); else the language
already detected for this reel folder (so master.mp4 is transcribed like raw.*); else Whisper detects it.
Never default to English: an English-only model turns Spanish into invented English, and forcing the wrong language
turns English into invented Spanish (caption test, Nov 2026).

Engine: the pinned HyperFrames' local Whisper (free, on this Mac), model brand.json "whisper_model" (default large-v3).
ElevenLabs Scribe only if brand.json has "elevenlabs": true AND a key is set: then the clip's audio is uploaded
and billed to the person's ElevenLabs account. Key: ELEVENLABS_API_KEY in the environment or ~/.config/reels/.env
(never pasted into chat).

Fixes for names Whisper mishears: brand.json "corrections", e.g. {"trusting gus": "Trust In Gus"}. Matching ignores case and
punctuation; the corrected words keep the original timing."""
import argparse, json, os, re, subprocess, sys, tempfile, unicodedata, urllib.error, urllib.request, uuid
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import reel_env as pe

ap =argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--language", choices=["es", "en", "auto"])
A = ap.parse_args()
lang_arg = A.language
src, out = Path(A.src).expanduser(), Path(A.out).expanduser()
folder = out.parent
B = pe.brand()
MODEL = pe.whisper_model(B)

if lang_arg in pe.LANGS: lang, source = lang_arg, "arg"
elif lang_arg == "auto": lang, source = None, "auto"
elif B.get("language") in pe.LANGS: lang, source = B["language"], "brand"
else:
    lang = pe.reel_language(folder, B)
    source = "folder" if lang else "auto"


def key():
    if os.environ.get("ELEVENLABS_API_KEY"): return os.environ["ELEVENLABS_API_KEY"]
    env = Path("~/.config/reels/.env").expanduser()
    for line in (env.read_text().splitlines() if env.exists() else []):
        if line.startswith("ELEVENLABS_API_KEY="): return line.split("=", 1)[1].strip()


def scribe(k):
    with tempfile.TemporaryDirectory() as tmp:
        audio = Path(tmp) / "a.mp3"   # mono 64 kbps: ~0.5 MB a minute, only the audio leaves the machine
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000", "-b:a", "64k", str(audio)], check=True)
        data = audio.read_bytes()
    for model in ("scribe_v2", "scribe_v1"):
        b = uuid.uuid4().hex
        fields = [("model_id", model), ("timestamps_granularity", "word"), ("tag_audio_events", "false")]
        if lang: fields.append(("language_code", {"es": "spa", "en": "eng"}[lang]))
        body = b"".join([f"--{b}\r\nContent-Disposition: form-data; name=\"{n}\"\r\n\r\n{v}\r\n".encode() for n, v in fields] + [
            f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"a.mp3\"\r\nContent-Type: audio/mpeg\r\n\r\n".encode(),
            data, f"\r\n--{b}--\r\n".encode()])
        req = urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text", data=body, method="POST",
                                     headers={"xi-api-key": k, "Content-Type": f"multipart/form-data; boundary={b}"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                res = json.load(r)
            det = (res.get("language_code") or "")[:2]
            det = {"sp": "es", "en": "en"}.get(det, det)
            return model, det, [{"text": w["text"], "start": round(w["start"], 3), "end": round(w["end"], 3)}
                                for w in res.get("words", []) if w.get("type") == "word" and w["text"].strip()]
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:200]
            if e.code in (400, 422) and "model" in msg.lower(): continue      # model id not offered: try the older one
            sys.exit(f"ElevenLabs error {e.code}: {msg}")
    sys.exit("ElevenLabs: no usable Scribe model")


GHOSTS = re.compile(r"thanks? (you )?for watching|subscribe|like and subscribe|gracias por (ver|su atenci)|suscr[ií]b|subt[ií]tulos (por|realizados)", re.I)
def invented(ws):
    """Whisper makes words up on clips with no talking ("Thank you for watching."), stretched over the silence.
    Real speech runs ~0.2 s a word; invented words run 1 s+. True = drop them."""
    if not ws: return False
    durs = sorted(w["end"] - w["start"] for w in ws)
    text = " ".join(w["text"] for w in ws)
    return durs[len(durs) // 2] > 0.8 or (len(ws) <= 8 and bool(GHOSTS.search(text)))


def whisper():
    """One clip: transcribe it. Several clips joined by join_clips.py (clips.json next to raw.*): transcribe each clip on
    its own and shift the times, so a word can't drift across a join into the next clip (Whisper did, by ~0.5 s)."""
    clips_f = folder / "clips.json"
    if not (clips_f.exists() and src.stem == "raw"):
        det, ws = whisper_one(src, folder / (out.stem + "_whisper"))
        if invented(ws):
            print(f"no real speech: dropped {len(ws)} words Whisper made up ({' '.join(w['text'] for w in ws)[:60]!r})")
            return det, []
        return det, ws
    dets, words = [], []
    with tempfile.TemporaryDirectory() as tmp:
        for c in json.load(open(clips_f)):
            seg = Path(tmp) / f"clip{c['n']}.wav"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(c["start"]), "-to", str(c["end"]), "-i", str(src),
                            "-vn", "-ac", "1", "-ar", "16000", str(seg)], check=True)
            det, ws = whisper_one(seg, folder / (out.stem + f"_whisper_clip{c['n']}"))
            if invented(ws):
                print(f"clip {c['n']} ({c['file']}): no talking, dropped {len(ws)} words Whisper made up "
                      f"({' '.join(w['text'] for w in ws)[:60]!r})")
                ws = []
            if ws: dets.append(det)
            for w in ws:
                a = round(c["start"] + w["start"], 3)
                if a >= c["end"]: continue
                words.append({**w, "start": a, "end": round(min(c["start"] + w["end"], c["end"]), 3)})
    return (max(set(dets), key=dets.count) if dets else None), words


def whisper_one(src, d):
    cmd = [pe.hyperframes(), "transcribe", str(src), "-d", str(d), "--json",
           "--engine", "whisper", "--no-runtime-install", "--model", MODEL]   # never "auto"/"heygen": no paid engine by accident
    if lang: cmd += ["--language", lang]
    r = subprocess.run(cmd, capture_output=True, text=True)
    summary = {}
    for line in r.stdout.splitlines()[::-1]:
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if "ok" in ev: summary = ev; break
    if r.returncode != 0 or not summary.get("ok"):
        tail = (r.stderr or r.stdout).strip()[-400:]
        sys.exit(f"JG-WHISPER: no se pudo transcribir / transcription failed (model {MODEL}). "
                 f"Run scripts/doctor.sh. Details: {tail}")
    return summary.get("detectedLanguage"), json.load(open(d / "transcript.json"))


def norm(s):
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFC", s.lower()))


def correct(words, fixes):
    """Replace misheard word runs (e.g. 'Trusting Gus' -> 'Trust In Gus'), keeping the run's start/end times."""
    rules = sorted(((k.split(), v.split()) for k, v in fixes.items()), key=lambda kv: -len(kv[0]))
    out, i, n = [], 0, 0
    while i < len(words):
        for wrong, right in rules:
            seq = [norm(w["text"]) for w in words[i:i + len(wrong)]]
            if seq == [norm(x) for x in wrong]:
                a, z = words[i]["start"], words[i + len(wrong) - 1]["end"]
                tail = re.sub(r"^[\w'’-]+", "", words[i + len(wrong) - 1]["text"].strip())   # keep trailing punctuation
                step = (z - a) / len(right)
                for j, t in enumerate(right):
                    out.append({"text": t + (tail if j == len(right) - 1 else ""),
                                "start": round(a + j * step, 3), "end": round(a + (j + 1) * step, 3)})
                i += len(wrong); n += 1
                break
        else:
            out.append(words[i]); i += 1
    return out, n


k = key() if B.get("elevenlabs") else None
if k:
    model, det, words = scribe(k)
    engine = f"ElevenLabs {model} (audio uploaded to ElevenLabs)"
else:
    det, words = whisper()
    model, engine = MODEL, f"local Whisper {MODEL} via HyperFrames"
words = [{"text": w["text"], "start": w["start"], "end": w["end"]} for w in words if w["text"].strip()]

final = lang or (det if det in pe.LANGS else None)
if final is None:
    print(f"WARNING: detected language {det!r} is not Spanish or English. Ask the person which they spoke, "
          "then re-run with --language es or --language en.")
    final = det or "unknown"
pe.save_language(folder, final, source if lang else "auto", model)

fixes = {kk.lower(): vv for kk, vv in (B.get("corrections") or {}).items()}
words, nfix = correct(words, fixes) if fixes else (words, 0)
json.dump(words, open(out, "w"), ensure_ascii=False)

label = {"es": "Spanish / español", "en": "English / inglés"}.get(final, final)
how = {"arg": "set for this run", "brand": "set in brand.json", "folder": "same as this reel's first transcript",
       "auto": "detected"}[source if lang else "auto"]
print(f"transcribed with {engine}: {len(words)} words · language: {label} ({how})" + (f" · {nfix} name fixes" if nfix else ""))
if not words:
    print("NO SPEECH FOUND: this clip may have no talking. Don't add captions for it.")
