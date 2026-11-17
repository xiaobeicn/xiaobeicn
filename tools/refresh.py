#!/usr/bin/env python3
"""Weekly refresh for the profile README (see .github/workflows/refresh-profile.yml).

- Fetches the current starred-repo total from the public GitHub REST API
  (no token needed; with per_page=1 the last page number equals the total).
- Regenerates assets/header-*.svg with the new total and today's date.
- Updates the <!-- refreshed: ... --> marker in README.md.

Commits nothing itself; the workflow commits when files change.

Deliberately NOT automated here: the per-list counts in the README table
(needs GraphQL + a token with `user` scope) and the harness-learn
verification date (changes only when the notes are re-verified by hand).
"""
import json
import os
import re
import sys
import urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from gen_header import generate  # noqa: E402

USER = "xiaobeicn"
VERIFIED = "2026-09-07"  # harness-learn last verification; update by hand


def starred_total():
    req = urllib.request.Request(
        f"https://api.github.com/users/{USER}/starred?per_page=1",
        headers={"User-Agent": "profile-refresh", "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        link = resp.headers.get("Link", "")
        body = json.loads(resp.read() or b"[]")
    m = re.search(r'[?&]page=(\d+)>; rel="last"', link)
    return int(m.group(1)) if m else len(body)


def main():
    today = date.today().isoformat()
    total = starred_total()
    generate(os.path.join(ROOT, "assets"), starred=total, date=today, verified=VERIFIED)

    readme = os.path.join(ROOT, "README.md")
    text = open(readme, encoding="utf-8").read()
    new_text, n = re.subn(
        r"<!-- refreshed: \d{4}-\d{2}-\d{2} -->",
        f"<!-- refreshed: {today} -->",
        text,
    )
    if n:
        open(readme, "w", encoding="utf-8").write(new_text)
        print(f"README refreshed marker -> {today}")
    else:
        print("WARNING: refreshed marker not found in README.md; left untouched")
    print(f"starred total: {total}")


if __name__ == "__main__":
    main()
