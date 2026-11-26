"""WoopSocial helpers: woop_posts.py builds draft-by-default requests from a checked post.md (and refuses an unchecked
one); woop_upload.py sends every part of the file to the session's upload addresses.
Run: python3 tests/test_woopsocial.py   (no network: the upload goes to a local test server)"""
import http.server, json, os, subprocess, sys, tempfile, threading
from datetime import datetime, timedelta, timezone
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / "skills/jackieg-reel-editor"
POSTS, UPLOAD = SKILL / "scripts/woop_posts.py", SKILL / "scripts/woop_upload.py"
GOOD = """# How a roof claim works
Language: en

## Caption
It starts with a free roof inspection.
Follow for more tips
trustingus.co

## Hashtags
#RoofReplacement #InsuranceClaim #DFWRoofing

## Title (YouTube Shorts)
How a roof insurance claim works
"""

with tempfile.TemporaryDirectory() as d:
    home = Path(d) / "reels"; reel = home / "2026-01-01-claim"; reel.mkdir(parents=True)
    (home / "brand.md").write_text("Website trustingus.co\n"); (home / "brand.json").write_text(json.dumps({"cta": "Follow for more tips"}))
    (reel / "master_transcript.json").write_text(json.dumps([{"text": w} for w in "it starts with a free roof inspection".split()]))
    (reel / "post.md").write_text(GOOD)
    env = {**os.environ, "REELS_HOME": str(home)}
    def run(*args): return subprocess.run([sys.executable, str(POSTS), str(reel), *args], capture_output=True, text=True, env=env)

    # 1. default is a draft, one request per account, caption = caption + hashtags, Instagram gets REEL
    r = run("--media", "m1", "--account", "INSTAGRAM:ig1", "--account", "youtube:yt1")
    assert r.returncode == 0, r.stdout + r.stderr
    ig = json.loads((reel / "woopsocial/instagram-ig1.json").read_text())
    yt = json.loads((reel / "woopsocial/youtube-yt1.json").read_text())
    assert ig["schedule"] == {"type": "DRAFT"} and yt["schedule"] == {"type": "DRAFT"}
    assert ig["socialAccounts"] == [{"platform": "INSTAGRAM", "socialAccountId": "ig1", "postType": "REEL"}]
    assert "postType" not in yt["socialAccounts"][0], "don't guess other networks' post types"
    assert ig["content"][0]["text"].endswith("trustingus.co\n\n#RoofReplacement #InsuranceClaim #DFWRoofing")
    assert ig["content"][0]["media"] == [{"type": "MEDIA_LIBRARY", "mediaId": "m1"}] and ig["autoDeleteMediaAfterPublish"] is True
    assert (reel / "woopsocial/youtube-yt1.title.txt").read_text() == "How a roof insurance claim works"
    assert "not sent yet" in r.stdout

    # 2. schedule: future time with timezone -> UTC; no timezone, past or junk -> refused; now; keep media
    future = (datetime.now(timezone(timedelta(hours=-6))) + timedelta(days=2)).replace(microsecond=0)
    assert run("--media", "m1", "--account", "TIKTOK:tt1", "--schedule", future.isoformat()).returncode == 0
    tt = json.loads((reel / "woopsocial/tiktok-tt1.json").read_text())
    assert tt["schedule"] == {"type": "SCHEDULE_FOR_LATER", "scheduledFor": future.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    assert "timezone" in run("--media", "m1", "--account", "TIKTOK:tt1", "--schedule", "2030-01-01T09:00").stderr
    assert "past" in run("--media", "m1", "--account", "TIKTOK:tt1", "--schedule", "2020-01-01T09:00-06:00").stderr
    assert run("--media", "m1", "--account", "TIKTOK:tt1", "--schedule", "tomorrow").returncode != 0
    assert run("--media", "m1", "--account", "FACEBOOK:fb1", "--schedule", "now", "--keep-media").returncode == 0
    fb = json.loads((reel / "woopsocial/facebook-fb1.json").read_text())
    assert fb["schedule"] == {"type": "PUBLISH_NOW"} and "autoDeleteMediaAfterPublish" not in fb
    assert run("--media", "m1", "--account", "INSTAGRAM").returncode != 0

    # 3. a draft that fails check_post.py (invented number) is refused
    (reel / "post.md").write_text(GOOD.replace("Follow for more tips", "500+ roofs done. Follow for more tips"))
    r = run("--media", "m1", "--account", "INSTAGRAM:ig1")
    assert r.returncode != 0 and "500" in r.stdout + r.stderr

    # 4. woop_upload.py sends each part in order to its address
    got = {}
    class H(http.server.BaseHTTPRequestHandler):
        def do_PUT(self):
            got[self.path] = self.rfile.read(int(self.headers["Content-Length"])); self.send_response(200); self.end_headers()
        def log_message(self, *a): pass
    srv = http.server.HTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_port}"
    data = os.urandom(2500); f = Path(d) / "final.mp4"; f.write_bytes(data)
    session = {"partSizeInBytes": 1000, "partCount": 3, "parts": [{"partNumber": n, "uploadUrl": f"{base}/p{n}"} for n in (3, 1, 2)]}
    (Path(d) / "session.json").write_text(json.dumps(session))
    env_np = {k: v for k, v in os.environ.items() if k.lower() not in ("http_proxy", "https_proxy", "all_proxy")}
    r = subprocess.run([sys.executable, str(UPLOAD), str(Path(d) / "session.json"), str(f)], capture_output=True, text=True, env=env_np)
    assert r.returncode == 0, r.stdout + r.stderr
    assert got["/p1"] + got["/p2"] + got["/p3"] == data and len(got["/p3"]) == 500
    session["partCount"] = 2; session["parts"] = session["parts"][:2]; (Path(d) / "session.json").write_text(json.dumps(session))
    r = subprocess.run([sys.executable, str(UPLOAD), str(Path(d) / "session.json"), str(f)], capture_output=True, text=True, env=env_np)
    assert r.returncode != 0 and "fileSizeInBytes=2500" in r.stdout + r.stderr
    srv.shutdown()

print("PASS: WoopSocial (draft by default, per-account requests, schedule rules, refuses unchecked drafts, upload parts)")
