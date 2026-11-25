#!/usr/bin/env python3
"""Send a finished reel to a WoopSocial upload session (standard library only).

WoopSocial takes a file in three steps (see references/woopsocial.md):
  1. Claude calls the WoopSocial tool media_uploads_create_session with the project and the file's exact size in
     bytes, and saves the answer as <reel>/woopsocial/session.json.
  2. This script sends the file's bytes to each upload address in that answer.
  3. Claude calls media_uploads_complete_session; when it says READY it gives the mediaId.

Usage: python3 woop_upload.py <session.json> <file>
Needs network access to *.r2.cloudflarestorage.com (where WoopSocial stores uploads)."""
import json, os, sys, urllib.error, urllib.request


def main():
    if len(sys.argv) != 3: sys.exit(__doc__)
    session = json.load(open(sys.argv[1], encoding="utf-8"))
    path = sys.argv[2]
    try:
        part_size = int(session["partSizeInBytes"])
        parts = sorted(session["parts"], key=lambda p: int(p["partNumber"]))
    except (KeyError, TypeError, ValueError):
        sys.exit("session.json isn't an upload session (needs partSizeInBytes and parts)")
    count = int(session.get("partCount", len(parts)))
    size = os.path.getsize(path)
    if -(-size // part_size) != count or len(parts) != count:
        sys.exit(f"the session was made for a different size: create it again with fileSizeInBytes={size}")
    with open(path, "rb") as f:
        for p in parts:
            chunk = f.read(part_size)
            req = urllib.request.Request(p["uploadUrl"], data=chunk, method="PUT",
                                         headers={"Content-Type": "application/octet-stream"})
            try:
                with urllib.request.urlopen(req, timeout=300) as r: status = r.status
            except urllib.error.HTTPError as e:
                sys.exit(f"part {p['partNumber']} was refused (HTTP {e.code}): create a new session and try again")
            except urllib.error.URLError as e:
                sys.exit(f"part {p['partNumber']} couldn't connect ({e.reason}). "
                         "If a network allowlist is on, allow *.r2.cloudflarestorage.com")
            print(f"part {p['partNumber']}/{count} sent (HTTP {status})")
    print("upload sent: now call media_uploads_complete_session")


if __name__ == "__main__":
    main()
