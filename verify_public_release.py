#!/usr/bin/env python3
"""Integrity check for this public release (standard library only).

1. MANIFEST.sha256 (repository root) lists every file in the release; each must match.
2. codex-audit/ is a rights-filtered copy of the private Codex bundle. Every entry of that
   bundle's own manifest (codex-audit/SHA256SUMS.txt) must be either present with the SAME
   SHA-256, or listed in codex-audit/PUBLIC_RELEASE_REMOVED_FILES.json with the same SHA-256.
   This shows that no kept file was edited and accounts for every removal.
3. claude-audit/results/SHA256SUMS must match the result files it lists.
Exit status 0 iff all checks pass.
Usage: python3 verify_public_release.py
"""
import hashlib, json, os, sys
ROOT = os.path.dirname(os.path.abspath(__file__))

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def read_manifest(path):
    out = {}
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line:
            h, p = line.split("  ", 1)
            out[p.replace("\\", "/")] = h
    return out

ok = True
def report(name, passed, detail=""):
    global ok
    ok &= passed
    print(("PASS " if passed else "FAIL ") + name + (": " + detail if detail else ""))

# 1. whole-release manifest
man = read_manifest(os.path.join(ROOT, "MANIFEST.sha256"))
bad = [p for p, h in man.items() if not os.path.isfile(os.path.join(ROOT, p)) or sha(os.path.join(ROOT, p)) != h]
listed = set(man)
present = set()
for r, ds, fs in os.walk(ROOT):
    ds[:] = [d for d in ds if d not in (".git", "_work", "__pycache__", ".venv")]
    for f in fs:
        rel = os.path.relpath(os.path.join(r, f), ROOT).replace("\\", "/")
        if rel != "MANIFEST.sha256":
            present.add(rel)
report("MANIFEST.sha256 hashes", not bad, f"{len(man)} files" if not bad else f"{len(bad)} mismatches, e.g. {bad[:3]}")
extra = sorted(present - listed)
report("MANIFEST.sha256 completeness", not extra, "every file listed" if not extra else f"unlisted: {extra[:5]}")

# 2. Codex bundle: kept files byte-identical to the private original, removals accounted for
C = os.path.join(ROOT, "codex-audit")
orig = read_manifest(os.path.join(C, "SHA256SUMS.txt"))
rem = {r["path"]: r for r in json.load(open(os.path.join(C, "PUBLIC_RELEASE_REMOVED_FILES.json")))["removed"]}
mism, unacc = [], []
for p, h in orig.items():
    fp = os.path.join(C, p)
    if os.path.isfile(fp):
        if sha(fp) != h: mism.append(p)
    elif p in rem:
        if rem[p]["sha256"] != h: mism.append(p)
    else:
        unacc.append(p)
kept = sum(1 for p in orig if os.path.isfile(os.path.join(C, p)))
report("codex-audit kept files identical to private original", not mism, f"{kept} kept, {len(rem)} removed" if not mism else f"{mism[:5]}")
report("codex-audit every original manifest entry accounted for", not unacc, "" if not unacc else f"{unacc[:5]}")

# 3. Claude results manifest
cr = read_manifest(os.path.join(ROOT, "claude-audit", "results", "SHA256SUMS"))
bad = [p for p, h in cr.items() if sha(os.path.join(ROOT, "claude-audit", p)) != h]
report("claude-audit/results/SHA256SUMS", not bad, f"{len(cr)} files" if not bad else f"{bad[:5]}")
sys.exit(0 if ok else 1)
