"""brands.py: finds each brand folder and picks one by the name the person says.
Run: python3 tests/test_brands.py   (no dependencies, no network)"""
import json, os, subprocess, sys, tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills/perlili-video-editor/scripts/brands.py"


def run(root, *args):
    r = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, env={**os.environ, "REELS_ROOT": str(root)})
    return r.returncode, r.stdout.strip()


with tempfile.TemporaryDirectory() as d:
    root = Path(d) / "reels"; root.mkdir()
    assert run(root)[0] == 4 and run(root, "anything")[0] == 4, "no brands should exit 4"

    # the original setup: brand.json directly in ~/reels, plus reel folders without one
    (root / "brand.json").write_text(json.dumps({"name": "Trust In Gus"}))
    (root / "2026-11-24-storm-claim").mkdir()
    assert run(root, "trust in gus") == (0, str(root)), run(root, "trust in gus")
    assert run(root, "TRUST-IN-GUS")[1] == str(root)

    # more brands as folders: inside ~/reels and inside ~/reels/brands
    (root / "leru").mkdir(); (root / "leru" / "brand.json").write_text(json.dumps({"name": "Latinos En Roofing University"}))
    (root / "brands" / "perlili").mkdir(parents=True); (root / "brands" / "perlili" / "brand.json").write_text(json.dumps({"name": "Perlili Developers Studio"}))
    (root / "chispa").mkdir(); (root / "chispa" / "brand.json").write_text("not json")   # unreadable: falls back to the folder name

    code, out = run(root)
    assert code == 0 and len(out.splitlines()) == 4, out
    assert run(root, "leru") == (0, str(root / "leru"))                          # folder name
    assert run(root, "latinos en roofing") == (0, str(root / "leru"))            # unique partial name
    assert run(root, "Perlili") == (0, str(root / "brands" / "perlili"))
    assert run(root, "chispa") == (0, str(root / "chispa"))
    assert run(root, "Látinos En Roofing University")[1] == str(root / "leru")   # accents ignored

    code, out = run(root, "nobody")
    assert code == 2 and len(out.splitlines()) == 4, (code, out)                 # no match: lists every brand

    (root / "trust-in-gus-es").mkdir(); (root / "trust-in-gus-es" / "brand.json").write_text(json.dumps({"name": "Trust In Gus (Español)"}))
    assert run(root, "trust in gus") == (0, str(root)), "an exact name beats a longer partial match"
    code, out = run(root, "gus")
    assert code == 3 and len(out.splitlines()) == 2, (code, out)                 # ambiguous: lists the candidates

print("PASS: brands (list, pick by name or folder, accents, no match, ambiguous)")
