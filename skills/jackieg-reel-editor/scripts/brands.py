#!/usr/bin/env python3
"""Which brand to edit for. Each brand is a folder with its own brand.json (+ brand.md, fonts/, assets/, reels):
~/reels itself (the original single-brand setup) and any folder directly inside ~/reels or ~/reels/brands/ that has a
brand.json. Every script uses the brand in REELS_HOME, so pick the folder here and pass it as REELS_HOME.

Usage: python3 brands.py                 list the brands: <folder><TAB><name>
       python3 brands.py "<brand name>"  print the folder for that brand (matches brand.json "name" or the folder name,
                                         ignoring case, accents and punctuation; a unique partial match counts)
Exit codes: 0 found, 2 no brand matches, 3 more than one matches (the candidates are listed), 4 no brands at all."""
import json, os, re, sys, unicodedata
from pathlib import Path

ROOT = Path(os.environ.get("REELS_ROOT", "~/reels")).expanduser()


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", s)


def brands():
    found, seen = [], set()
    cands = [ROOT] + sorted(p for p in ROOT.glob("*") if p.is_dir()) + sorted(p for p in (ROOT / "brands").glob("*") if p.is_dir())
    for d in cands:
        f = d / "brand.json"
        if not f.is_file() or d.resolve() in seen: continue
        seen.add(d.resolve())
        try: name = json.load(open(f)).get("name") or d.name
        except (OSError, ValueError): name = d.name
        found.append((d, str(name)))
    return found


all_ = brands()
args = [a for a in sys.argv[1:] if a.strip()]
if not args:
    for d, name in all_: print(f"{d}\t{name}")
    sys.exit(0 if all_ else 4)
if not all_:
    print(f"no brands yet in {ROOT}: run the setup interview first"); sys.exit(4)

want = norm(" ".join(args))
exact = [(d, n) for d, n in all_ if want in (norm(n), norm(d.name))]
part = [(d, n) for d, n in all_ if want and (want in norm(n) or want in norm(d.name))]
hits = exact or part
if len(hits) == 1:
    print(hits[0][0]); sys.exit(0)
for d, n in (hits or all_): print(f"{d}\t{n}")
sys.exit(3 if hits else 2)
