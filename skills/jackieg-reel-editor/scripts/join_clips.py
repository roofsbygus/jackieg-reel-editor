#!/usr/bin/env python3
"""Several phone clips → one reel. Joins them, in order, into <reel>/raw.mov so every later step (transcribe, clean
audio, review, cut) works on one video, exactly as with a single clip. The originals are only read, never changed.

Usage: python3 join_clips.py <reel-folder> <clip> <clip> [...] [--keep-order]
  Default order: oldest first (the phone's recording time), then file name. --keep-order uses the order given.
Writes raw.mov (H.264 at the brand resolution, 30 fps, lossless PCM audio, so the voice clean-up starts from the
original sound) and clips.json [{n, file, start, end, landscape, no_audio}], which the review page uses to show
where each clip starts. Refuses to overwrite an existing raw.*.
Each clip fills the vertical frame (centered crop). A sideways (landscape) clip loses its sides: it's flagged so you
can tell the person before they approve."""
import json, os, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import reel_env  # noqa: F401  Homebrew tools on PATH (Code tab)

args = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(args) < 3: sys.exit(__doc__)
reel, clips = Path(args[0]).expanduser(), [Path(a).expanduser() for a in args[1:]]
for c in clips:
    if not c.is_file(): sys.exit(f"JG-CLIP: no encuentro el video {c} / can't find this clip")
if list(reel.glob("raw.*")): sys.exit(f"{reel} already has a raw clip: use a new reel folder (nothing was changed)")
reel.mkdir(parents=True, exist_ok=True)
HOME = Path(os.environ.get("REELS_HOME", "~/reels-jackieg")).expanduser()
brand = json.load(open(HOME / "brand.json")) if (HOME / "brand.json").exists() else {}
W, H = brand.get("resolution", [1080, 1920])

def probe(p):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(p)],
                                  capture_output=True, text=True, check=True).stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    w, h = int(v["width"]), int(v["height"])
    rot = 0
    for sd in v.get("side_data_list", []):
        if "rotation" in sd: rot = int(sd["rotation"])
    rot = int(v.get("tags", {}).get("rotate", rot))
    if abs(rot) % 180 == 90: w, h = h, w            # phones store portrait video as landscape + a rotation flag
    tags = {**j["format"].get("tags", {}), **v.get("tags", {})}
    when = tags.get("com.apple.quicktime.creationdate") or tags.get("creation_time") or ""
    return {"dur": float(j["format"]["duration"]), "w": w, "h": h, "when": when,
            "audio": any(s["codec_type"] == "audio" for s in j["streams"])}

info = [(c, probe(c)) for c in clips]
if "--keep-order" not in sys.argv:
    info.sort(key=lambda ci: (ci[1]["when"] or "9999", ci[0].name.lower()))

inputs, fc, cat, out, t = [], [], "", [], 0.0
for k, (c, p) in enumerate(info):
    inputs += ["-i", str(c)]
    fc.append(f"[{k}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,setsar=1,format=yuv420p[v{k}]")
    if p["audio"]:
        fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{p['dur']:.3f}[a{k}]")
    else:   # a clip with no sound gets silence, so the joins stay in sync
        fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{p['dur']:.3f}[a{k}]")
    cat += f"[v{k}][a{k}]"
    out.append({"n": k + 1, "file": c.name, "start": round(t, 3), "end": round(t + p["dur"], 3),
                "landscape": p["w"] > p["h"], "no_audio": not p["audio"]})
    t += p["dur"]
fc.append(f"{cat}concat=n={len(info)}:v=1:a=1[vout][aout]")
script = reel / "join_filter.txt"
script.write_text(";\n".join(fc))
print(f"Uniendo {len(info)} videos ({t:.1f} s) / joining {len(info)} clips:")
for o in out:
    print(f"  {o['n']}. {o['file']}  {o['start']:.1f}–{o['end']:.1f} s" + ("  ⚠️ horizontal: se recortan los lados" if o["landscape"] else "")
          + ("  (sin sonido)" if o["no_audio"] else ""))
subprocess.run(["nice", "-n", "15", "ffmpeg", "-y", "-v", "error", "-stats", *inputs, "-/filter_complex", str(script),
                "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14",
                "-c:a", "pcm_s16le", str(reel / "raw.mov")], check=True)
json.dump(out, open(reel / "clips.json", "w"), indent=1)
print(reel / "raw.mov")
