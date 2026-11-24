#!/usr/bin/env python3
"""Tighten an approved rough cut: remove fillers and shorten pauses inside the kept spans, as hard as brand.json "pacing" says (scripts/pacing.py).
Run after the person approves edl.json, before cut.py. Rewrites edl.json (the original is kept as edl_rough.json).
Usage: python3 tighten.py <reel-folder>
       python3 tighten.py <reel-folder> --detect   only find the fillers (writes fillers.json); run before the review page

How: Whisper normally hides fillers inside neighbouring words, so it is re-run with a prompt full of fillers in the
reel's language ("um, uh" / "eh, este, mmm"), which makes it write them down. It runs in that language (whisper-cli
assumes English unless told, which turns Spanish into English) with the multilingual model. Pauses come from silencedetect
on the cleaned voice. Every cut edge keeps the preset's air (50-150 ms) so words never clip.
Spanish "este" is cut only when a pause follows it ("este..."), never in "este mes". "pues", "bueno", "o sea" are never cut here."""
import json, re, shutil, subprocess, sys, unicodedata
from pathlib import Path

reel = Path(sys.argv[1]).expanduser()
DETECT = "--detect" in sys.argv[2:]
edl = {} if DETECT else json.load(open(reel / "edl.json"))
voice = reel / edl.get("audio", "voice.wav")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import perlili_env as pe
from pacing import pacing
B = pe.brand()
LANG = pe.reel_language(reel, B) or "en"
P_ = pacing(B, LANG)
PAD, MIN_PAUSE = P_["air"], P_["pause_min"]
FILLERS, HESIT = set(P_["fillers"]), set(P_["hesitations"])
PROMPT = {"en": "Um, uh, so, like, um, I mean, uh, you know.",
          "es": "Eh, este, mmm, o sea, eh, pues, em, este... bueno, eh."}[LANG]
norm = lambda s: re.sub(r"[^\w]", "", unicodedata.normalize("NFC", s.lower()))

# 1. fillers, via Whisper with a filler-heavy prompt
cuts = []
cli = next((p for p in ("/opt/homebrew/bin/whisper-cli", "/usr/local/bin/whisper-cli") if Path(p).exists()), None)
mdir = Path("~/.cache/hyperframes/whisper/models").expanduser()
model = mdir / f"ggml-{pe.whisper_model(B)}.bin"
if not model.exists():   # fall back to any multilingual model; ".en" models only for English reels
    model = next((m for m in sorted(mdir.glob("ggml-*.bin"), reverse=True) if LANG == "en" or ".en." not in m.name), None)
found = False
if not (cli and model):
    print("PV-WHISPER: whisper-cli or its model is missing. Run scripts/doctor.sh (this script never installs anything).")
else:
    wav16 = reel / "v16.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(voice), "-ar", "16000", "-ac", "1", str(wav16)], check=True)
    r = subprocess.run([cli, "-m", str(model), "-f", str(wav16), "-l", LANG, "--prompt", PROMPT,
                        "-ml", "1", "-sow", "-oj", "-of", str(reel / "fillers")], capture_output=True, text=True)
    if r.returncode == 0 and (reel / "fillers.json").exists():
        found = True
        toks = [(t["text"].strip(), t["offsets"]["from"] / 1000, t["offsets"]["to"] / 1000)
                for t in json.load(open(reel / "fillers.json"))["transcription"] if t["text"].strip()]
        for k, (txt, a, b) in enumerate(toks):
            w = norm(txt)
            nxt = toks[k + 1][1] if k + 1 < len(toks) else b + 1
            if w in FILLERS or (w in HESIT and nxt - b >= 0.25):
                cuts.append((a - 0.02, max(b, min(nxt, a + 0.7)) - 0.02))
        print(f"fillers found ({LANG}): {len(cuts)}", [round(a, 1) for a, _ in cuts])
    else:
        (reel / "fillers.json").unlink(missing_ok=True)   # never leave a stale or half-written file behind
        print("whisper-cli failed:", (r.stderr or "").strip()[-300:])
if not found:
    print("FILLERS NOT DETECTED: fillers won't be cut automatically. Tell the person, and offer to cut them by hand on the review.")
if DETECT: sys.exit(0 if found else 3)

# 2. pauses, via silencedetect on the cleaned voice. The threshold sits just above THIS clip's background noise
#    (outdoor or noisy rooms never reach a fixed -40 dB, so a fixed threshold finds nothing).
import array, math, wave
wf = wave.open(str(voice)); sr = wf.getframerate(); pcm = array.array("h"); pcm.frombytes(wf.readframes(wf.getnframes()))
hop = int(sr * 0.05)
lev = sorted(20 * math.log10(max(1.0, math.sqrt(sum(x * x for x in pcm[i:i + hop:4]) / (hop / 4))) / 32768)
             for i in range(0, len(pcm) - hop, hop))
floor = lev[len(lev) // 10]
thresh = min(floor + 5, -20)
print(f"background noise {floor:.0f} dB -> pause threshold {thresh:.0f} dB")
out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(voice), "-af", f"silencedetect=noise={thresh:.1f}dB:d={MIN_PAUSE}", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
pauses = [(a + PAD, b - PAD) for a, b in zip(starts, ends) if b - a > MIN_PAUSE]
cuts += pauses
cuts.sort()

# 3. subtract the cuts from each approved span (span order is preserved, so a moved CTA stays moved)
def subtract(span, cuts):
    a, b = span; parts, cur = [], a
    for ca, cb in cuts:
        if cb <= cur or ca >= b: continue
        if ca > cur + 0.05: parts.append([round(cur, 3), round(ca, 3)])
        cur = max(cur, cb)
    if b > cur + 0.05: parts.append([round(cur, 3), round(b, 3)])
    return parts
before = sum(b - a for a, b in edl["keep"])
shutil.copy(reel / "edl.json", reel / "edl_rough.json")
edl["keep"] = [p for span in edl["keep"] for p in subtract(span, cuts)]
after = sum(b - a for a, b in edl["keep"])
json.dump(edl, open(reel / "edl.json", "w"))
print(f"{len(pauses)} pauses + fillers removed: {before:.1f}s -> {after:.1f}s kept ({len(edl['keep'])} pieces)")
