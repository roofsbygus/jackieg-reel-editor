#!/usr/bin/env python3
"""Turn a reel's checked post draft (post.md) into WoopSocial post requests, one per social account.
Nothing is sent: Claude validates each request with posts_validate, shows the person, and only then calls posts_create.

Usage:
  python3 woop_posts.py <reel> --media <mediaId> --account <PLATFORM>:<socialAccountId>[:<postType>] [--account ...]
                        [--schedule draft | now | <date-time with timezone, e.g. 2026-11-28T09:00-06:00>] [--keep-media]

- Default --schedule is draft: saved in WoopSocial only, nothing goes to the network.
- Caption = the "## Caption" section + a blank line + the "## Hashtags" line. The YouTube Shorts title is written to
  woopsocial/<file>.title.txt for Claude to put in the field the live schema names (it differs per network).
- postType: INSTAGRAM defaults to REEL; for other networks pass it (or leave it out) and let posts_validate say.
- The uploaded video is deleted from the WoopSocial library once every account has published
  (autoDeleteMediaAfterPublish, so the free plan's storage doesn't fill up), unless --keep-media.
Writes <reel>/woopsocial/<platform>-<id>.json and prints a summary."""
import argparse, json, re, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ap = argparse.ArgumentParser(usage=__doc__)
ap.add_argument("reel"); ap.add_argument("--media", required=True)
ap.add_argument("--account", action="append", required=True)
ap.add_argument("--schedule", default="draft"); ap.add_argument("--keep-media", action="store_true")
a = ap.parse_args()
reel = Path(a.reel).expanduser()

# the draft must pass its own check first: no invented numbers, links or handles
chk = subprocess.run([sys.executable, str(Path(__file__).with_name("check_post.py")), str(reel)], capture_output=True, text=True)
if chk.returncode != 0: sys.exit(chk.stdout + chk.stderr + "\nfix post.md first (references/post-copy.md)")
text = (reel / "post.md").read_text()

# the music must be approved and cleared for every network it's going to (e.g. Meta Sound Collection: no TikTok)
nets = sorted({acc.split(":")[0].upper() for acc in a.account if acc.split(":")[0]})
mus = subprocess.run([sys.executable, str(Path(__file__).with_name("music.py")), "check", str(reel), "--platforms", ",".join(nets)],
                     capture_output=True, text=True)
if mus.returncode != 0: sys.exit(mus.stdout + mus.stderr + "\nfix the music first (references/music.md)")

def section(name):
    m = re.search(rf"^## {name}[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S | re.I)
    return m.group(1).strip() if m else ""
caption = section("Caption") + "\n\n" + section("Hashtags")
title = section("Title")

s = a.schedule.strip().lower()
if s == "draft": schedule = {"type": "DRAFT"}
elif s == "now": schedule = {"type": "PUBLISH_NOW"}
else:
    try: when = datetime.fromisoformat(a.schedule.strip().replace("Z", "+00:00"))
    except ValueError: sys.exit(f"--schedule {a.schedule!r}: use draft, now, or a date-time like 2026-11-28T09:00-06:00")
    if when.tzinfo is None: sys.exit("--schedule needs a timezone (e.g. -06:00 for Central): '9am' alone is ambiguous")
    if when <= datetime.now(timezone.utc): sys.exit(f"--schedule {a.schedule} is in the past")
    schedule = {"type": "SCHEDULE_FOR_LATER", "scheduledFor": when.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}

out = reel / "woopsocial"; out.mkdir(exist_ok=True)
lines = []
for acc in a.account:
    bits = acc.split(":")
    if len(bits) not in (2, 3) or not bits[0] or not bits[1]:
        sys.exit(f"--account {acc!r}: use PLATFORM:socialAccountId[:postType], e.g. INSTAGRAM:abc123")
    platform, acc_id = bits[0].upper(), bits[1]
    post_type = (bits[2].upper() if len(bits) == 3 else ("REEL" if platform == "INSTAGRAM" else None))
    target = {"platform": platform, "socialAccountId": acc_id}
    if post_type: target["postType"] = post_type
    body = {"content": [{"text": caption, "media": [{"type": "MEDIA_LIBRARY", "mediaId": a.media}]}],
            "schedule": schedule, "socialAccounts": [target]}
    if not a.keep_media: body["autoDeleteMediaAfterPublish"] = True
    name = re.sub(r"[^a-z0-9]+", "-", f"{platform}-{acc_id}".lower())
    (out / f"{name}.json").write_text(json.dumps(body, indent=2, ensure_ascii=False))
    if platform == "YOUTUBE" and title: (out / f"{name}.title.txt").write_text(title)
    lines.append(f"{platform:<10} {post_type or '(postType from validate)':<26} {schedule['type']:<18} woopsocial/{name}.json")

print("post requests (not sent yet: validate, show the person, then create):")
print("\n".join(lines))
print(f"caption: {len(caption)} characters" + (f"; YouTube title: {title}" if title else ""))
