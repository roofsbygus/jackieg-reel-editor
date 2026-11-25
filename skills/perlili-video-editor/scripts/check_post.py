#!/usr/bin/env python3
"""Check a reel's post draft (<reel>/post.md) before it's delivered.
Fails when the draft has a number, link, @handle or email that isn't in what the person said (master_transcript.json),
their brand file (brand.md / brand.json) or post_facts.txt (anything they told you for this post), or when it breaks
the format or platform limits. The point: a post never claims something they didn't say.
Usage: python3 check_post.py <reel folder>"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import perlili_env as pe

reel = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else sys.exit(__doc__)
post = reel / "post.md"
if not post.exists(): sys.exit(f"no post draft yet: write {post} (references/post-copy.md)")
text = post.read_text()

src = []
for name in ("master_transcript.json", "transcript.json"):
    f = reel / name
    if f.exists():
        src.append(" ".join(w.get("text", "") for w in json.load(open(f)))); break
for f in (pe.HOME / "brand.md", pe.HOME / "brand.json", reel / "post_facts.txt"):
    if f.exists(): src.append(f.read_text())
source = " ".join(src).lower()
digits_src = re.sub(r"[,\s]", "", source)

problems = []
sections = {m.group(1).strip().lower(): m.start() for m in re.finditer(r"^## (.+)$", text, re.M)}
def section(name):
    k = next((s for s in sections if s.startswith(name)), None)
    if k is None: return None
    start = sections[k]; ends = [v for v in sections.values() if v > start]
    return text[start:min(ends) if ends else len(text)].split("\n", 1)[1].strip()
caption, tags, title = section("caption"), section("hashtags"), section("title")
for n, v in (("Caption", caption), ("Hashtags", tags), ("Title", title)):
    if not v: problems.append(f"missing or empty '## {n}' section")

body = "\n".join(v for v in (caption, title) if v)
for num in sorted(set(re.findall(r"\d[\d,.:/-]*\d|\d", body))):
    if re.sub(r"[,\s]", "", num) not in digits_src:
        problems.append(f"number not in the reel or brand file: {num}")
for url in sorted(set(re.findall(r"(?:https?://)?(?:[\w-]+\.)+(?:com|co|net|org|io|dev|ai|us|biz|info|tv|me|app)\b(?:/\S*)?", body, re.I))):
    if re.sub(r"^https?://(www\.)?", "", url.lower()).rstrip("/") not in source:
        problems.append(f"link not in the reel or brand file: {url}")
for handle in sorted(set(re.findall(r"(?<![\w.])@[\w.]+", body))):
    if handle.lower() not in source: problems.append(f"@handle not in the reel or brand file: {handle}")
for mail in sorted(set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", body))):
    if mail.lower() not in source: problems.append(f"email not in the reel or brand file: {mail}")

if caption and len(caption) > 2200: problems.append(f"caption is {len(caption)} characters (Instagram's limit is 2200)")
if title and len(title) > 100: problems.append(f"title is {len(title)} characters (YouTube Shorts' limit is 100)")
if tags is not None:
    found = re.findall(r"#\w+", tags)
    if not 3 <= len(found) <= 8: problems.append(f"{len(found)} hashtags: use 3 to 8")
    if re.sub(r"#\w+|\s", "", tags): problems.append("hashtags line has other text: only #tags separated by spaces")

if problems:
    print("post draft needs fixing:"); [print(" -", p) for p in problems]; sys.exit(1)
print(f"post draft OK: {post}")
