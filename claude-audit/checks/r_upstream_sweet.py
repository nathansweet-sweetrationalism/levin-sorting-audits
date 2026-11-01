#!/usr/bin/env python3
"""Sweet's Oct 31 endpoint tests, re-run on the ORIGINAL threaded implementation
(Zhangtaining/cell_research @ 1fd2bd5) instead of Dietz's sequential surrogate.

For n=80 (40 Bubble, 40 Selection), copies per key C in {1, 2, 10}, 15 runs each:
  - equal-key identity reversals (global stability) for C >= 2
  - quiet-endpoint persistence: runs that stopped because no swap occurred for `quiet_s` s
  - C=2 exact within-block conditional test (same null as Sweet), C=10 conditional mean
  - matched label-permutation control for the transient PEAK: on the same trajectory,
    a random 40/40 passive label independent of algotype, max over time (removes peak-selection bias)
Writes results/r_upstream_sweet.json."""
import json, os, sys, random, statistics as st
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
import upstream_driver as U

def H(t): return sum(1 for i in range(len(t) - 1) if t[i] == t[i + 1])
def blocks(vals, types):
    out, cur, last = [], [], None
    for v, t in zip(vals, types):
        if cur and v != last: out.append(cur); cur = []
        cur.append(t); last = v
    out.append(cur); return out
def cond_mean(bl):
    E = F(0)
    for b in bl:
        m = len(b); nb = b.count("B"); ns = m - nb
        if m > 1: E += F(nb * (nb - 1) + ns * (ns - 1), m)
    for b1, b2 in zip(bl, bl[1:]):
        E += F(b1.count("B"), len(b1)) * F(b2.count("B"), len(b2)) + F(b1.count("S"), len(b1)) * F(b2.count("S"), len(b2))
    return E
def run_dist(bl):
    from itertools import permutations
    dist, first = {}, True
    for b in bl:
        perms = list(permutations(range(len(b)))); cnt = {}
        for p in perms:
            s = tuple(b[i] for i in p); cnt[s] = cnt.get(s, 0) + 1
        new = {}
        for seq, c in cnt.items():
            ps = F(c, len(perms)); hin = H(list(seq))
            if first:
                k = (seq[-1], hin); new[k] = new.get(k, 0) + ps
            else:
                for (lt, h), p in dist.items():
                    k = (seq[-1], h + hin + (lt == seq[0])); new[k] = new.get(k, 0) + p * ps
        dist, first = new, False
    tot = {}
    for (_, h), p in dist.items(): tot[h] = tot.get(h, 0) + p
    return tot

REPS = int(os.environ.get("REPS", "15")); n = 80
out = {}
for C in [int(c) for c in os.environ.get("CS", "1,2,10").split(",")]:
    rows = []
    for r in range(REPS):
        rng = random.Random(int(os.environ.get("SEEDBASE", "7000")) + 100 * C + r)
        if C == 1: vals = rng.sample(range(1, n + 1), n)
        else:
            vals = [(i % (n // C)) + 1 for i in range(n)]; rng.shuffle(vals)
        types = ["B"] * 40 + ["S"] * 40; rng.shuffle(types)
        passive = ["B"] * 40 + ["S"] * 40; rng.shuffle(passive)   # label-permutation control
        res = U.run(vals, types, (), quiet_s=1.5, max_s=90, seed=r, track_ids=True)
        idtype = {i + 1: types[i] for i in range(n)}; idpas = {i + 1: passive[i] for i in range(n)}
        traj = [[i + 1 for i in range(n)]] + res["id_snapshots"]
        peak = max(H([idtype[x] for x in s]) for s in traj) / n
        peak_ctrl = max(H([idpas[x] for x in s]) for s in traj) / n
        fids = res["final_ids"]; fv = res["final_values"]; ft = [idtype[x] for x in fids]
        rev = False
        if C >= 2:
            pos = {x: k for k, x in enumerate(fids)}
            byv = {}
            for i in range(n): byv.setdefault(vals[i], []).append(pos[i + 1])
            rev = any(p[k] > p[k + 1] for p in byv.values() for k in range(len(p) - 1))
        rows.append({"final_A": H(ft) / n, "peak_A": peak, "peak_ctrl": peak_ctrl,
                     "final_ctrl": H([idpas[x] for x in fids]) / n, "sorted": fv == sorted(vals),
                     "quiet_stop": not res["hit_max_time"], "equal_key_reversal": rev,
                     "blocks": blocks(fv, ft), "H": H(ft), "swaps": res["swaps"],
                     "blocks_ctrl": blocks(fv, [idpas[x] for x in fids]), "H_ctrl": H([idpas[x] for x in fids])})
        print(C, r, round(rows[-1]["final_A"], 4), round(peak, 4), round(peak_ctrl, 4), flush=True)
    d = {"runs": REPS, "final_mean": st.mean(x["final_A"] for x in rows),
         "final_sem": st.pstdev(x["final_A"] for x in rows) / REPS ** 0.5,
         "final_ctrl_mean": st.mean(x["final_ctrl"] for x in rows),
         "peak_mean": st.mean(x["peak_A"] for x in rows), "peak_ctrl_mean": st.mean(x["peak_ctrl"] for x in rows),
         "peak_excess_mean": st.mean(x["peak_A"] - x["peak_ctrl"] for x in rows),
         "peak_excess_runs_positive": sum(x["peak_A"] > x["peak_ctrl"] for x in rows),
         "all_sorted": all(x["sorted"] for x in rows), "quiet_stops": sum(x["quiet_stop"] for x in rows),
         "runs_with_equal_key_reversal": sum(x["equal_key_reversal"] for x in rows) if C >= 2 else None}
    if C >= 2:
        obs = sum(x["H"] for x in rows); mu = sum(cond_mean(x["blocks"]) for x in rows)
        d["observed_total_H"] = obs; d["conditional_expected_total_H"] = float(mu)
        d["conditional_mean_A"] = float(mu / (REPS * n))
        if C == 2:
            tot = {0: F(1)}
            for x in rows:
                dd = run_dist(x["blocks"]); new = {}
                for a, p in tot.items():
                    for b, q in dd.items(): new[a + b] = new.get(a + b, 0) + p * q
                tot = new
            d["exact_two_sided_distance_tail_p"] = float(sum(p for h, p in tot.items() if abs(h - mu) >= abs(obs - mu)))
            # negative control: identical test on passive labels that cannot influence movement
            obs_c = sum(x["H_ctrl"] for x in rows); mu_c = sum(cond_mean(x["blocks_ctrl"]) for x in rows)
            tot = {0: F(1)}
            for x in rows:
                dd = run_dist(x["blocks_ctrl"]); new = {}
                for a, p in tot.items():
                    for b, q in dd.items(): new[a + b] = new.get(a + b, 0) + p * q
                tot = new
            d["negative_control_observed_H"] = obs_c; d["negative_control_expected_H"] = float(mu_c)
            d["negative_control_exact_p"] = float(sum(p for h, p in tot.items() if abs(h - mu_c) >= abs(obs_c - mu_c)))
    out[f"C{C}"] = d
    print(C, {k: v for k, v in d.items()}, flush=True)
os.makedirs("results", exist_ok=True)
json.dump(out, open(os.environ.get("OUT", "results/r_upstream_sweet.json"), "w"), indent=1)
