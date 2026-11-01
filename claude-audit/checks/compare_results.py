#!/usr/bin/env python3
"""Compare freshly regenerated results with the published ones.

Deterministic files must match exactly, except that floating-point numbers may differ by at most
1e-9 relative (LAPACK/BLAS results can differ in the last bits across CPUs); every difference is printed.
d_references.json / d_method_refs.json depend on live registry metadata, so only the
per-DOI verdict (MATCH / MISMATCH / UNRESOLVED or resolved title) is compared.
Usage: python3 checks/compare_results.py EXPECTED_DIR ACTUAL_DIR
Exit status 0 iff every comparison passes."""
import json, sys, os
EXP, ACT = sys.argv[1:3]
EXACT = ["m_exact_math.json", "m_crosscheck_node.json", "n_replay_bfe377c.json", "t_alignment_null.json",
         "f_code_forensics.json", "u_isolated_prefix.json", "dietz_ablation_rerun.json"]
ok = True
def load(d, f):
    return json.load(open(os.path.join(d, f), encoding="utf-8"))
def diff(a, b, path, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b: out.append((path + "/" + k, a.get(k), b.get(k), False))
            else: diff(a[k], b[k], path + "/" + k, out)
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)): diff(x, y, f"{path}[{i}]", out)
    elif isinstance(a, float) and isinstance(b, (int, float)) and not isinstance(b, bool):
        if a != b: out.append((path, a, b, abs(a - b) <= 1e-9 * max(1.0, abs(a), abs(b))))
    elif a != b:
        out.append((path, a, b, False))
for f in EXACT:
    d = []; diff(load(EXP, f), load(ACT, f), "", d)
    hard = [x for x in d if not x[3]]
    print(("PASS " if not hard else "FAIL ") + f + (f" ({len(d)} float differences within 1e-9)" if d and not hard else ""))
    for p_, a, b, _ in hard[:20]: print("   ", p_, a, "->", b)
    ok &= not hard
e = {r["doi"]: r["status"] for r in load(EXP, "d_references.json")}
a = {r["doi"]: r["status"] for r in load(ACT, "d_references.json")}
same = e == a
print(("PASS " if same else "FAIL ") + "d_references.json (per-DOI verdicts)"); ok &= same
if not same:
    for k in sorted(set(e) | set(a)):
        if e.get(k) != a.get(k): print("   ", k, e.get(k), "->", a.get(k))
if os.path.exists(os.path.join(ACT, "d_method_refs.json")):
    e = {k: v.get("title") for k, v in load(EXP, "d_method_refs.json").items()}
    a = {k: v.get("title") for k, v in load(ACT, "d_method_refs.json").items()}
    same = e == a
    print(("PASS " if same else "FAIL ") + "d_method_refs.json (resolved titles)"); ok &= same
sys.exit(0 if ok else 1)
