#!/usr/bin/env python3
"""Replication on the UNMODIFIED upstream threaded code (see upstream_driver.py).

R1  Frozen-cell semantics actually implemented upstream (movable vs wall), barrier crossing.
R2  Insertion FREEZE-reset ablation under upstream (movable) semantics, n=60, f=1..3.
R3  Mixed Bubble+Selection: sign of dI per swap (is 'never uphill on I' true?).
R4  Determinism: same input, same seed, two runs -> identical swap traces?
Writes results/r_upstream.json. Wall-clock dependent (threads); numbers are distributions.
"""
import json, os, sys, random, statistics as st
sys.path.insert(0, os.path.dirname(__file__))
import upstream_driver as U

def inv(v): return sum(1 for i in range(len(v)) for j in range(i + 1, len(v)) if v[i] > v[j])
def desc(v): return sum(1 for i in range(1, len(v)) if v[i] < v[i - 1])
OUT = {}
REPS = int(os.environ.get("REPS", "20"))

# R1 ----------------------------------------------------------------------------
r1 = []
for f in (1, 2, 3):
    for r in range(REPS // 2):
        rng = random.Random(1000 + 10 * f + r)
        n = 60
        v = rng.sample(range(1, n + 1), n)
        fi = rng.sample(range(5, n - 5), f)
        res = U.run(v, ["B"] * n, fi, quiet_s=1.2, max_s=40, seed=r)
        snaps = [v] + res["value_snapshots"]
        dI = [inv(snaps[t]) - inv(snaps[t - 1]) for t in range(1, len(snaps))]
        d0 = min(fi)
        crossed = len(set(v[:d0]) ^ set(res["final_values"][:d0]))
        r1.append({"f": f, "frozen_moved": sum(a != b for a, b in zip(res["frozen_init"], res["frozen_final"])),
                   "values_crossing_first_frozen_index": crossed, "dI_set": sorted(set(dI)),
                   "final_E": desc(res["final_values"]), "swaps": res["swaps"]})
OUT["R1_bubble_movable_frozen"] = {
    "runs": len(r1),
    "runs_where_a_frozen_cell_was_displaced": sum(1 for x in r1 if x["frozen_moved"] > 0),
    "runs_with_values_crossing_the_initial_frozen_index": sum(1 for x in r1 if x["values_crossing_first_frozen_index"] > 0),
    "all_bubble_swaps_dI_minus1": all(x["dI_set"] == [-1] for x in r1),
    "mean_final_E_by_f": {f: st.mean(x["final_E"] for x in r1 if x["f"] == f) for f in (1, 2, 3)},
    "detail": r1}
print("R1", {k: v for k, v in OUT["R1_bubble_movable_frozen"].items() if k != "detail"}, flush=True)

# R2 ----------------------------------------------------------------------------
r2 = {"with_reset": {1: [], 2: [], 3: []}, "strict_no_reset": {1: [], 2: [], 3: []}}
for f in (1, 2, 3):
    for r in range(REPS):
        rng = random.Random(2000 + 10 * f + r)
        n = 60
        v = rng.sample(range(1, n + 1), n)
        fi = rng.sample(range(5, n - 5), f)
        for arm, strict in (("with_reset", False), ("strict_no_reset", True)):
            res = U.run(v, ["I"] * n, fi, strict_insertion=strict, quiet_s=1.2, max_s=40, seed=r)
            r2[arm][f].append(desc(res["final_values"]))
OUT["R2_insertion_ablation_upstream_movable"] = {
    arm: {f: {"mean_final_E": st.mean(x), "sd": st.pstdev(x), "n": len(x)} for f, x in d.items()} for arm, d in r2.items()}
print("R2", OUT["R2_insertion_ablation_upstream_movable"], flush=True)

# R3 ----------------------------------------------------------------------------
r3 = []
for r in range(REPS // 2):
    rng = random.Random(3000 + r)
    n = 60
    v = rng.sample(range(1, n + 1), n)
    types = ["B"] * (n // 2) + ["S"] * (n // 2); rng.shuffle(types)
    res = U.run(v, types, (), quiet_s=1.2, max_s=40, seed=r)
    snaps = [v] + res["value_snapshots"]
    dI = [inv(snaps[t]) - inv(snaps[t - 1]) for t in range(1, len(snaps))]
    r3.append({"swaps": len(dI), "uphill_I": sum(d > 0 for d in dI), "zero_I": sum(d == 0 for d in dI),
               "max_dI": max(dI), "min_dI": min(dI), "sorted": res["final_values"] == sorted(v)})
OUT["R3_mixed_BS_dI"] = {"runs": len(r3), "runs_with_uphill_I_swap": sum(x["uphill_I"] > 0 for x in r3),
                         "total_uphill": sum(x["uphill_I"] for x in r3), "total_swaps": sum(x["swaps"] for x in r3),
                         "detail": r3}
print("R3", {k: v for k, v in OUT["R3_mixed_BS_dI"].items() if k != "detail"}, flush=True)

# R4 ----------------------------------------------------------------------------
rng = random.Random(4000); n = 40
v = rng.sample(range(1, n + 1), n)
traces = [U.run(v, ["B"] * n, (), quiet_s=1.0, max_s=30, seed=7)["value_snapshots"] for _ in range(3)]
OUT["R4_determinism"] = {"identical_traces_run1_run2": traces[0] == traces[1],
                         "identical_traces_run1_run3": traces[0] == traces[2],
                         "trace_lengths": [len(t) for t in traces]}
print("R4", OUT["R4_determinism"], flush=True)
os.makedirs("results", exist_ok=True)
json.dump(OUT, open("results/r_upstream.json", "w"), indent=1)
