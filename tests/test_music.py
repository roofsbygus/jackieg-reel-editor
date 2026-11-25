"""Music bed: music.py keeps one licensed library shared by every brand, picks a track that fits the reel and where it's posted,
refuses unlicensed sources, needs their approval and the CC BY credit; mix_music.sh puts it under the voice at -14 LUFS
without touching final_voice.mp4; woop_posts.py refuses music that isn't cleared for a network.
Run: python3 tests/test_music.py   (needs ffmpeg; no network)"""
import json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / "skills/perlili-video-editor"
MUSIC, MIX, POSTS = SKILL / "scripts/music.py", SKILL / "scripts/mix_music.sh", SKILL / "scripts/woop_posts.py"


def ff(*args): subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def lufs(f):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(f), "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    return float(json.loads(r.stderr[r.stderr.rindex("{"):])["input_i"])


with tempfile.TemporaryDirectory() as d:
    d = Path(d); root = d / "reels"; home = root / "tig"; reel = home / "2026-01-01-claim"; reel.mkdir(parents=True)
    (home / "brand.json").write_text(json.dumps({"woopsocial": {"accounts": ["INSTAGRAM"]}}))
    env = {**os.environ, "REELS_ROOT": str(root), "REELS_HOME": str(home)}
    def run(*args): return subprocess.run([sys.executable, str(MUSIC), *map(str, args)], capture_output=True, text=True, env=env)

    # a 6 s "rendered reel" (video + a voice tone) and three downloaded tracks
    ff("-f", "lavfi", "-i", "color=c=black:s=320x568:d=6", "-f", "lavfi", "-i", "sine=f=220:d=6", "-shortest",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(reel / "final_voice.mp4"))
    for name, sec in (("calm.mp3", 10), ("upbeat.mp3", 10), ("short.mp3", 3)):
        ff("-f", "lavfi", "-i", f"sine=f=440:d={sec}", str(d / name))
    calm_src = (d / "calm.mp3").read_bytes()

    # 1. add: unlicensed sources and NonCommercial licenses are refused; CC BY needs its credit line
    assert run("add", d / "calm.mp3", "--source", "instagram", "--license-url", "https://x.com", "--title", "x").returncode != 0
    assert run("add", d / "calm.mp3", "--source", "cc-by", "--title", "x",
               "--license-url", "https://creativecommons.org/licenses/by-nc/4.0/").returncode != 0
    assert run("add", d / "calm.mp3", "--source", "cc-by", "--title", "x", "--credit", "c",
               "--license-url", "https://creativecommons.org/licenses/by-nd/4.0/").returncode != 0
    assert run("add", d / "calm.mp3", "--source", "cc-by", "--title", "x",
               "--license-url", "https://creativecommons.org/licenses/by/4.0/").returncode != 0, "CC BY without --credit"
    r = run("add", d / "calm.mp3", "--source", "meta", "--license-url", "https://www.facebook.com/sound/collection",
            "--title", "Calm Roof", "--mood", "calm,warm"); assert r.returncode == 0, r.stdout + r.stderr
    r = run("add", d / "upbeat.mp3", "--source", "cc-by", "--license-url", "https://creativecommons.org/licenses/by/4.0/",
            "--title", "Upbeat Day", "--mood", "upbeat,calm", "--credit", "Music: Upbeat Day by Ana (CC BY 4.0)")
    assert r.returncode == 0, r.stdout + r.stderr
    assert run("add", d / "short.mp3", "--source", "pixabay", "--license-url", "https://pixabay.com/service/license-summary/",
               "--title", "Short Calm", "--mood", "calm").returncode == 0
    lib = json.loads((root / "music/library.json").read_text())   # shared, not inside the brand folder
    assert not (home / "music").exists()
    assert [t["id"] for t in lib] == ["calm-roof", "upbeat-day", "short-calm"]
    assert lib[0]["platforms"] == ["INSTAGRAM", "FACEBOOK"] and "TIKTOK" in lib[1]["platforms"]
    assert (d / "calm.mp3").read_bytes() == calm_src, "the original download is never changed"

    # 2. pick: mood first, long enough beats a loop; for TikTok the Meta-only track is skipped
    r = run("pick", reel, "--mood", "calm"); assert r.returncode == 0, r.stdout + r.stderr
    m = json.loads((reel / "music.json").read_text())
    assert m["id"] == "calm-roof" and m["approved"] is False and m["for_platforms"] == ["INSTAGRAM"]
    assert "short-calm" in m["alternatives"]
    r = run("pick", reel, "--mood", "calm", "--platforms", "INSTAGRAM,TIKTOK"); assert r.returncode == 0
    assert json.loads((reel / "music.json").read_text())["id"] == "upbeat-day", "Meta Sound Collection isn't cleared for TikTok"
    assert run("pick", reel, "--mood", "dramatic").returncode == 2, "nothing fits: say so, don't pick a random track"

    # another brand uses the same library, and use is recorded as brand/reel
    other = root / "chispa" / "2026-01-02-promo"; other.mkdir(parents=True); (root / "chispa/brand.json").write_text("{}")
    shutil.copy(reel / "final_voice.mp4", other / "final_voice.mp4")
    r = subprocess.run([sys.executable, str(MUSIC), "pick", str(other), "--mood", "calm"], capture_output=True, text=True,
                       env={**env, "REELS_HOME": str(root / "chispa")})
    assert r.returncode == 0, r.stdout + r.stderr
    used = [u for t in json.loads((root / "music/library.json").read_text()) for u in t.get("used", [])]
    assert "tig/2026-01-01-claim" in used and "chispa/2026-01-02-promo" in used, used

    # 3. check: needs their yes, and the CC BY credit in the caption
    (reel / "post.md").write_text("## Caption\nhi\n")
    r = run("check", reel); assert r.returncode == 1 and "approved" in r.stdout and "credit" in r.stdout, r.stdout
    assert run("approve", reel).returncode == 0
    (reel / "post.md").write_text("## Caption\nhi\nMusic: Upbeat Day by Ana (CC BY 4.0)\n")
    r = run("check", reel); assert r.returncode == 0, r.stdout
    # the credit line's own numbers ("4.0") don't trip the post check
    (home / "brand.md").write_text(""); (reel / "master_transcript.json").write_text(json.dumps([{"text": "hi"}]))
    (reel / "post.md").write_text("# x\nLanguage: en\n\n## Caption\nhi\nMusic: Upbeat Day by Ana (CC BY 4.0)\n\n"
                                  "## Hashtags\n#a #b #c\n\n## Title (YouTube Shorts)\nhi\n")
    r = subprocess.run([sys.executable, str(SKILL / "scripts/check_post.py"), str(reel)], capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stdout + r.stderr

    # 4. swap resets approval and won't take a track not cleared for where it's going
    r = run("swap", reel, "Calm Roof"); assert r.returncode != 0 and "only cleared" in r.stderr, r.stdout + r.stderr
    run("pick", reel, "--mood", "calm"); run("approve", reel)
    r = run("swap", reel, "1"); assert r.returncode == 0, r.stdout + r.stderr
    assert json.loads((reel / "music.json").read_text())["approved"] is False

    # 5. mix: music under the voice, fade out, -14 LUFS, final_voice.mp4 untouched; "none" = voice only
    voice_before = (reel / "final_voice.mp4").read_bytes()
    run("swap", reel, "Calm Roof")
    r = subprocess.run(["bash", str(MIX), str(reel)], capture_output=True, text=True, env=env)
    assert r.returncode == 0 and "calm-roof" in r.stdout, r.stdout + r.stderr
    assert (reel / "final_voice.mp4").read_bytes() == voice_before
    assert abs(lufs(reel / "final.mp4") - (-14)) < 1.5
    run("none", reel)
    r = subprocess.run(["bash", str(MIX), str(reel)], capture_output=True, text=True, env=env)
    assert r.returncode == 0 and "no music" in r.stdout
    assert run("resolve", reel).stdout.strip() == "none"

    # 6. older brands with one fixed track keep working when a reel has no music.json
    (reel / "music.json").unlink()
    (home / "brand.json").write_text(json.dumps({"music": str(d / "calm.mp3")}))
    assert re.match(rf"{re.escape(str(d / 'calm.mp3'))}\t-18\t0\t0$", run("resolve", reel).stdout.strip())

    # 7. woop_posts refuses a TikTok post whose music is Meta-only
    (home / "brand.json").write_text("{}"); (home / "brand.md").write_text("")
    (reel / "master_transcript.json").write_text(json.dumps([{"text": "hi"}]))
    (reel / "post.md").write_text("# x\nLanguage: en\n\n## Caption\nhi\n\n## Hashtags\n#a #b #c\n\n## Title (YouTube Shorts)\nhi\n")
    assert run("pick", reel, "--mood", "warm", "--platforms", "INSTAGRAM").returncode == 0; run("approve", reel)
    r = subprocess.run([sys.executable, str(POSTS), str(reel), "--media", "m1", "--account", "TIKTOK:t1"],
                       capture_output=True, text=True, env=env)
    assert r.returncode != 0 and "TIKTOK" in r.stdout + r.stderr, r.stdout + r.stderr
    r = subprocess.run([sys.executable, str(POSTS), str(reel), "--media", "m1", "--account", "INSTAGRAM:i1"],
                       capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stdout + r.stderr

print("music tests passed")
