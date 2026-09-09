#!/usr/bin/env python3
"""
Check that every local reference in this repo actually resolves.

Covers the Pages site under docs/ (href, src, stylesheet links) and the relative
links in the Markdown files. External http(s) links are reported but not fetched,
so this stays fast and works offline.

    python3 scripts/check-links.py
"""

import os
import re
import sys
from urllib.parse import unquote, urlparse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, "docs")

HTML_REF = re.compile(r'(?:href|src)\s*=\s*"([^"]+)"', re.I)
MD_REF = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def is_external(target: str) -> bool:
    return bool(urlparse(target).scheme) or target.startswith("//")


def collect(path: str, pattern: re.Pattern) -> list:
    with open(path, encoding="utf-8") as fh:
        return pattern.findall(fh.read())


def resolve(source_file: str, target: str) -> str:
    """Map a reference to the path on disk it should point at."""
    target = unquote(target.split("#")[0].split("?")[0])
    if not target:
        return ""
    if target.startswith("/"):
        # Root-relative inside the Pages site.
        return os.path.join(DOCS, target.lstrip("/"))
    return os.path.normpath(os.path.join(os.path.dirname(source_file), target))


def exists(path: str, from_html: bool) -> bool:
    if os.path.isfile(path):
        return True
    if not os.path.isdir(path):
        return False
    # GitHub renders a directory link as its file listing, so any existing
    # directory is a valid Markdown target. GitHub Pages needs something to
    # serve, so an HTML target must contain an index.
    if not from_html:
        return True
    return os.path.isfile(os.path.join(path, "index.html"))


def main() -> int:
    targets = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", ".venv"}]
        for name in files:
            full = os.path.join(root, name)
            if name.endswith((".html", ".htm")):
                targets.append((full, HTML_REF, True))
            elif name.endswith(".md"):
                targets.append((full, MD_REF, False))

    broken, checked, external = [], 0, 0

    for path, pattern, from_html in sorted(targets):
        for ref in collect(path, pattern):
            if ref.startswith(("mailto:", "data:", "tel:", "#")):
                continue
            if is_external(ref):
                external += 1
                continue
            checked += 1
            resolved = resolve(path, ref)
            if not resolved or not exists(resolved, from_html):
                broken.append((os.path.relpath(path, REPO), ref))

    for src, ref in broken:
        print(f"BROKEN  {src} -> {ref}")

    print(
        f"\n{checked} local reference(s) checked, "
        f"{len(broken)} broken, {external} external skipped"
    )
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
