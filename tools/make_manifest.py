#!/usr/bin/env python3
"""Regenerate MANIFEST.sha256 for every file in the release (excluding .git and local work dirs)."""
import os, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lines = []
for r, ds, fs in os.walk(ROOT):
    ds[:] = [d for d in ds if d not in (".git", "_work", "__pycache__", ".venv")]
    for f in fs:
        p = os.path.relpath(os.path.join(r, f), ROOT).replace(os.sep, "/")
        if p != "MANIFEST.sha256":
            lines.append(f"{hashlib.sha256(open(os.path.join(ROOT, p), 'rb').read()).hexdigest()}  {p}")
open(os.path.join(ROOT, "MANIFEST.sha256"), "w").write("\n".join(sorted(lines, key=lambda l: l.split("  ", 1)[1])) + "\n")
print(len(lines), "files")
