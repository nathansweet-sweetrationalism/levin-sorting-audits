#!/usr/bin/env python3
"""Compare freshly regenerated results with the published ones.

Deterministic files must match exactly after key-sorted JSON normalisation.
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
for f in EXACT:
    same = json.dumps(load(EXP, f), sort_keys=True) == json.dumps(load(ACT, f), sort_keys=True)
    print(("PASS " if same else "FAIL ") + f); ok &= same
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
