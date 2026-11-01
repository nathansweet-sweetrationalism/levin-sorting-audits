#!/usr/bin/env python3
"""Does the UPSTREAM threaded code reproduce Dietz's Claim 3 aggregation numbers?
n=80, 40 Bubble + 40 Selection, copies per key C in {1, 2, 10}, 15 runs each.
Aggregation A = H/N as in upstream analysis/cell_type_aggregation_analysis.py.
Writes results/r_upstream_agg.json."""
import json, os, sys, random, statistics as st
sys.path.insert(0, os.path.dirname(__file__))
import upstream_driver as U

def A(types): return sum(1 for i in range(len(types) - 1) if types[i] == types[i + 1]) / len(types)
REPS = int(os.environ.get("REPS", "15")); n = 80
out = {}
for C in (1, 2, 10):
    finals, peaks, sorted_ok = [], [], 0
    for r in range(REPS):
        rng = random.Random(5000 + 100 * C + r)
        keys = n // C
        vals = [(i % keys) + 1 for i in range(n)]; rng.shuffle(vals)
        if C == 1: vals = rng.sample(range(1, n + 1), n)
        types = ["B"] * 40 + ["S"] * 40; rng.shuffle(types)
        res = U.run(vals, types, (), quiet_s=1.2, max_s=60, seed=r)
        code = {0: "B", 1: "S", 2: "I"}
        traj = [A(types)] + [A([code[x] for x in s]) for s in res["type_snapshots"]]
        finals.append(A(res["final_types"])); peaks.append(max(traj))
        sorted_ok += res["final_values"] == sorted(vals)
    out[f"C{C}"] = {"final_mean": st.mean(finals), "final_sem": st.pstdev(finals) / len(finals) ** 0.5,
                    "peak_mean": st.mean(peaks), "runs": REPS, "runs_fully_sorted": sorted_ok,
                    "null_expectation": (40 * 39 * 2) / n ** 2}
    print(C, out[f"C{C}"], flush=True)
os.makedirs("results", exist_ok=True)
json.dump(out, open("results/r_upstream_agg.json", "w"), indent=1)
