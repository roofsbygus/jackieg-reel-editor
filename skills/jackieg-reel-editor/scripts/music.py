#!/usr/bin/env python3
"""Music bed for a reel: a licensed track under the voice, picked to fit the reel, checked against where it's posted.

Every track lives in one shared library for all their brands (~/reels/music/, or $REELS_ROOT/music; list in
music/library.json) with its license, so any brand can reuse it and a reel's music can always be traced back to where
it came from and what it's cleared for. Never in-app or trending
songs, never NonCommercial: references/music.md.

  add <file> --source <src> --license-url <url> --title "<t>" [--artist "<a>"] [--mood calm,upbeat]
             [--credit "<line for the caption>"]
      Copy a downloaded track into the library (the original is left untouched). <src>: meta (Meta Sound
      Collection: Instagram and Facebook only), pixabay, mixkit, cc0, cc-by (needs --credit), own (they made/own it).
  pick <reel> --mood <m1,m2> [--platforms INSTAGRAM,TIKTOK]
      Choose the best track for this reel: mood tags first, then long enough not to loop, then not used lately.
      Platforms default to brand.json "woopsocial.accounts", else every network. Writes <reel>/music.json
      (approved: false) with up to 3 alternatives. Exit 2: nothing in the library fits.
  swap <reel> <number|title>   use alternative 1/2/3 (or a library title) instead; approval resets.
  none <reel>                  this reel has no music.
  approve <reel>               they listened and said yes.
  check <reel> [--platforms INSTAGRAM,TIKTOK]
      Exit 1 if the track is missing, not approved, not cleared for a platform, or its credit line isn't in post.md.
  resolve <reel>               for mix_music.sh: "none", or path<TAB>gain_db<TAB>start<TAB>fade_out.
  list                         show the library."""
import json, os, re, shutil, subprocess, sys
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import reel_env as pe

ALL = ["INSTAGRAM", "FACEBOOK", "THREADS", "TIKTOK", "YOUTUBE", "LINKEDIN", "X", "PINTEREST", "BLUESKY"]
SOURCES = {   # what each source's license clears (references/music.md has the why and the links)
    "meta":    {"name": "Meta Sound Collection", "platforms": ["INSTAGRAM", "FACEBOOK"], "credit": False},
    "pixabay": {"name": "Pixabay Music", "platforms": ALL, "credit": False},
    "mixkit":  {"name": "Mixkit", "platforms": ALL, "credit": False},
    "cc0":     {"name": "Creative Commons CC0", "platforms": ALL, "credit": False},
    "cc-by":   {"name": "Creative Commons CC BY", "platforms": ALL, "credit": True},
    "own":     {"name": "Their own music", "platforms": ALL, "credit": False},
}
REFUSED = "in-app/trending songs, Spotify/YouTube rips and NonCommercial (NC) tracks aren't cleared for a business account"
GAIN_DB, FADE_OUT = -18, 1.5   # same bed level render.sh always used; fade out over the last 1.5 s
LIB_DIR = Path(os.environ.get("REELS_ROOT", "~/reels")).expanduser() / "music"   # shared by every brand (brands.py ROOT)
LIB = LIB_DIR / "library.json"


def load_lib(): return json.load(open(LIB)) if LIB.exists() else []
def save_lib(lib): LIB_DIR.mkdir(parents=True, exist_ok=True); LIB.write_text(json.dumps(lib, indent=2, ensure_ascii=False))
def tags(s): return [t.strip().lower() for t in (s or "").split(",") if t.strip()]
def plats(s): return [p.strip().upper() for p in s.split(",") if p.strip()] if s else None


def duration(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                       capture_output=True, text=True)
    try: return round(float(r.stdout.strip()), 2)
    except ValueError: sys.exit(f"can't read the length of {f}: is it an audio file?")


def opt(args, name, default=None):
    if name in args:
        i = args.index(name)
        if i + 1 >= len(args): sys.exit(f"{name} needs a value")
        return args[i + 1]
    return default


def reel_dir(args):
    if not args: sys.exit(__doc__)
    r = Path(args[0]).expanduser()
    if not r.is_dir(): sys.exit(f"no reel folder at {r}")
    return r


def reel_length(reel):
    for n in ("final_voice.mp4", "master.mp4", "final.mp4"):
        if (reel / n).exists(): return duration(reel / n)
    sys.exit(f"no master.mp4 in {reel} yet: cut the reel first (step 4)")


def default_platforms():
    accs = pe.brand().get("woopsocial", {}).get("accounts")
    return [a.upper() for a in accs] if accs else ALL


def write_choice(reel, t, alternatives, mood, platforms):
    rec = {"track": str(LIB_DIR / t["file"]), "id": t["id"], "title": t["title"], "artist": t.get("artist"),
           "source": t["source"], "source_name": SOURCES[t["source"]]["name"], "license_url": t["license_url"],
           "credit": t.get("credit"), "platforms": t["platforms"], "gain_db": GAIN_DB, "start": 0, "fade_out": FADE_OUT,
           "mood": mood, "for_platforms": platforms, "alternatives": [a["id"] for a in alternatives], "approved": False}
    (reel / "music.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False))
    lib = load_lib()
    for e in lib:
        if e["id"] == t["id"]: e.setdefault("used", []).append(f"{pe.HOME.name}/{reel.name}")   # brand/reel
    save_lib(lib)
    return rec


def cmd_add(args):
    if not args: sys.exit(__doc__)
    src_file = Path(args[0]).expanduser()
    if not src_file.is_file(): sys.exit(f"no file at {src_file}")
    source = (opt(args, "--source") or "").lower(); url = opt(args, "--license-url"); title = opt(args, "--title")
    if source not in SOURCES: sys.exit(f"--source must be one of {', '.join(SOURCES)} ({REFUSED})")
    if not url or not re.match(r"https?://", url): sys.exit("--license-url: the page that shows this track's license")
    if re.search(r"by-nc|[-_/]nc[-_/]|noncommercial", url, re.I): sys.exit(f"that license is NonCommercial: {REFUSED}")
    if re.search(r"by-nd|[-_/]nd[-_/]|noderivatives", url, re.I): sys.exit("that license is NoDerivatives: a track mixed into a reel can't be ND")
    if not title: sys.exit("--title is needed")
    credit = opt(args, "--credit")
    if SOURCES[source]["credit"] and not credit: sys.exit("a CC BY track needs --credit: the exact line its license asks for")
    lib = load_lib()
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "track"
    tid = slug; n = 2
    while any(e["id"] == tid for e in lib): tid = f"{slug}-{n}"; n += 1
    LIB_DIR.mkdir(parents=True, exist_ok=True)
    dest = LIB_DIR / f"{tid}{src_file.suffix.lower()}"
    shutil.copy2(src_file, dest)   # a copy: their download stays as it was
    e = {"id": tid, "file": dest.name, "title": title, "artist": opt(args, "--artist"), "source": source,
         "license_url": url, "credit": credit, "platforms": SOURCES[source]["platforms"],
         "mood": tags(opt(args, "--mood")), "seconds": duration(dest), "added": date.today().isoformat(), "used": []}
    lib.append(e); save_lib(lib)
    print(f"added '{title}' ({e['seconds']} s, {SOURCES[source]['name']}, cleared for {', '.join(e['platforms'])})")


def ranked(lib, mood, platforms, length):
    ok = [t for t in lib if set(platforms) <= set(t["platforms"]) and (LIB_DIR / t["file"]).exists()]
    def score(t):
        recent = len([u for u in t.get("used", [])[-5:]])
        return (len(set(mood) & set(t.get("mood", []))), t.get("seconds", 0) >= length, -recent)   # ties: library order
    return sorted(ok, key=score, reverse=True)


def cmd_pick(args):
    reel = reel_dir(args); mood = tags(opt(args, "--mood"))
    if not mood: sys.exit("--mood is needed: 1-3 words that fit what the reel says and how it feels (calm, upbeat, ...)")
    platforms = plats(opt(args, "--platforms")) or default_platforms()
    lib = load_lib()
    if not lib: print(f"the music library is empty ({LIB}): add tracks first (references/music.md)"); sys.exit(2)
    best = ranked(lib, mood, platforms, reel_length(reel))
    if not best or not set(mood) & set(best[0].get("mood", [])):
        print(f"nothing in the library fits mood {', '.join(mood)} for {', '.join(platforms)}: find a track (references/music.md)")
        sys.exit(2)
    rec = write_choice(reel, best[0], best[1:4], mood, platforms)
    print(f"music: '{rec['title']}' ({rec['source_name']}) - not approved yet, they listen first")
    for i, a in enumerate(best[1:4], 1): print(f"  alternative {i}: '{a['title']}' ({', '.join(a.get('mood', []))})")


def cmd_swap(args):
    reel = reel_dir(args); f = reel / "music.json"
    if len(args) < 2 or not f.exists(): sys.exit("usage: swap <reel> <number|title> (after pick)")
    cur, lib = json.load(open(f)), load_lib()
    want = args[1]
    if want.isdigit():
        i = int(want) - 1
        if not 0 <= i < len(cur["alternatives"]): sys.exit(f"there are {len(cur['alternatives'])} alternatives")
        t = next(e for e in lib if e["id"] == cur["alternatives"][i])
    else:
        t = next((e for e in lib if e["title"].lower() == want.lower() or e["id"] == want.lower()), None)
        if not t: sys.exit(f"no track called '{want}' in the library")
    if not set(cur["for_platforms"]) <= set(t["platforms"]):
        sys.exit(f"'{t['title']}' is only cleared for {', '.join(t['platforms'])}")
    others = [e for e in lib if e["id"] in cur["alternatives"] + [cur["id"]] and e["id"] != t["id"]]
    rec = write_choice(reel, t, others[:3], cur["mood"], cur["for_platforms"])
    print(f"music: '{rec['title']}' - not approved yet. Remix: bash scripts/mix_music.sh {reel}")


def cmd_none(args):
    reel = reel_dir(args)
    (reel / "music.json").write_text(json.dumps({"track": None, "approved": True}, indent=2))
    print("no music on this reel")


def cmd_approve(args):
    reel = reel_dir(args); f = reel / "music.json"
    if not f.exists(): sys.exit("no music chosen yet: run pick first")
    rec = json.load(open(f)); rec["approved"] = True; f.write_text(json.dumps(rec, indent=2, ensure_ascii=False))
    print("music approved" if rec.get("track") else "no music (approved)")


def cmd_check(args):
    reel = reel_dir(args); f = reel / "music.json"
    if not f.exists(): print("no music.json: no per-reel music"); return
    rec = json.load(open(f))
    if rec.get("track") is None: print("music: none"); return
    problems = []
    if not Path(rec["track"]).exists(): problems.append(f"the track file is missing: {rec['track']}")
    if not rec.get("approved"): problems.append("they haven't approved the music yet (listen, then music.py approve)")
    for p in plats(opt(args, "--platforms")) or rec.get("for_platforms", []):
        if p not in rec["platforms"]:
            problems.append(f"'{rec['title']}' ({rec['source_name']}) isn't cleared for {p}: swap it or post without {p}")
    if rec.get("credit"):
        post = reel / "post.md"
        if not post.exists() or rec["credit"] not in post.read_text():
            problems.append(f"the license needs this credit in the caption of post.md: {rec['credit']}")
    if problems:
        print("music needs fixing:"); [print(" -", p) for p in problems]; sys.exit(1)
    print(f"music OK: '{rec['title']}' ({rec['source_name']})")


def cmd_resolve(args):
    reel = reel_dir(args); f = reel / "music.json"
    if f.exists():
        rec = json.load(open(f))
        if rec.get("track") is None: print("none"); return
        print(f"{rec['track']}\t{rec.get('gain_db', GAIN_DB)}\t{rec.get('start', 0)}\t{rec.get('fade_out', FADE_OUT)}"); return
    m = pe.brand().get("music")   # older setup: one fixed track for the whole brand
    p = Path(m).expanduser() if isinstance(m, str) and m not in ("none", "auto") else None
    print(f"{p}\t{GAIN_DB}\t0\t0" if p and p.is_file() else "none")


def cmd_list(args):
    lib = load_lib()
    if not lib: print(f"no tracks yet ({LIB})"); return
    for t in lib:
        print(f"{t['title']:<32} {t.get('seconds', 0):>6.1f}s  {SOURCES[t['source']]['name']:<24} {', '.join(t.get('mood', []))}")


if __name__ == "__main__":
    cmds = {"add": cmd_add, "pick": cmd_pick, "swap": cmd_swap, "none": cmd_none, "approve": cmd_approve,
            "check": cmd_check, "resolve": cmd_resolve, "list": cmd_list}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds: sys.exit(__doc__)
    cmds[sys.argv[1]](sys.argv[2:])
