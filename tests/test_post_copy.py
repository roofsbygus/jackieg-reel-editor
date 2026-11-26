"""check_post.py: a post draft passes only with numbers, links, handles and emails the person actually said or has in
their brand file, and with the right format and lengths. deliver.sh copies it next to the video.
Run: python3 tests/test_post_copy.py   (needs ffmpeg for the deliver part; no network)"""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / "skills/jackieg-reel-editor"
CHECK = SKILL / "scripts/check_post.py"

GOOD = """# How a roof claim works
Language: en

## Caption
It starts with a free roof inspection.
Then we submit a claim and work with the insurance to get you approved.
Follow for more tips
trustingus.co

## Hashtags
#RoofReplacement #InsuranceClaim #DFWRoofing

## Title (YouTube Shorts)
How a roof insurance claim works
"""

with tempfile.TemporaryDirectory() as d:
    home = Path(d) / "reels"; reel = home / "2026-01-01-claim"; reel.mkdir(parents=True)
    (home / "brand.md").write_text("# Trust In Gus\nWebsite trustingus.co. Homeowners in North Texas (Dallas-Fort Worth).\n")
    (home / "brand.json").write_text(json.dumps({"cta": "Follow for more tips", "deliver_dir": str(Path(d) / "out")}))
    words = "it starts with a free roof inspection then we submit a claim we have done 2 roofs this week".split()
    (reel / "master_transcript.json").write_text(json.dumps([{"text": w} for w in words]))
    env = {**os.environ, "REELS_HOME": str(home)}

    def check(md):
        (reel / "post.md").write_text(md)
        r = subprocess.run([sys.executable, str(CHECK), str(reel)], capture_output=True, text=True, env=env)
        return r.returncode, r.stdout + r.stderr

    assert check(GOOD)[0] == 0, check(GOOD)
    # invented facts are caught
    for bad, why in [("We've replaced 500+ roofs since 2015.", "500"), ("Call 972-555-0100 today.", "972"),
                     ("Book at gusroofs.com", "gusroofs.com"), ("DM @trustingus_official", "@trustingus_official"),
                     ("Email gus@example.com", "gus@example.com")]:
        code, out = check(GOOD.replace("Follow for more tips", bad))
        assert code == 1 and why in out, (bad, out)
    # a number they said, or one they gave for this post, is fine
    assert check(GOOD.replace("Follow for more tips", "2 roofs this week. Follow for more tips"))[0] == 0
    (reel / "post_facts.txt").write_text("Offer ends December 15")
    assert check(GOOD.replace("Follow for more tips", "Offer ends December 15. Follow for more tips"))[0] == 0
    # format and limits
    assert "hashtags" in check(GOOD.replace("#RoofReplacement #InsuranceClaim #DFWRoofing", "#Roofing"))[1]
    assert "only #tags" in check(GOOD.replace("#DFWRoofing", "#DFWRoofing and more"))[1]
    assert "title is" in check(GOOD.replace("How a roof insurance claim works", "x" * 101))[1]
    assert "missing" in check(GOOD.split("## Title")[0])[1]
    (reel / "post.md").unlink()
    assert subprocess.run([sys.executable, str(CHECK), str(reel)], capture_output=True, env=env).returncode != 0

    # deliver.sh puts the draft next to the video
    if shutil.which("ffmpeg"):
        (reel / "post.md").write_text(GOOD)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=gray:s=320x568:r=30:d=1", "-f", "lavfi",
                        "-i", "anullsrc=r=48000:cl=stereo", "-t", "1", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
                        str(reel / "final.mp4")], check=True)
        subprocess.run(["bash", str(SKILL / "scripts/deliver.sh"), str(reel / "final.mp4"), "Claim test"], env=env, check=True,
                       capture_output=True)
        out = Path(d) / "out" / "Claim test"                                   # its own folder inside the delivery folder
        assert (out / "Claim test.mp4").exists() and (out / "Claim test - post.txt").read_text() == GOOD

print("PASS: post drafts (invented numbers, links, handles and emails caught; format; delivered next to the video in its own folder)")
