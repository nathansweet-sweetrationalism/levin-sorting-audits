#!/usr/bin/env python3
"""Re-derive the numbers in Sweet's Oct 31 revision from Dietz's model pinned at bfe377c.

Replays quantify_emergence_ce2.analyze_duplicate_multiplicity_law exactly (same RNG calls),
keeping the final Cell objects so equal-key order and continuation can be checked.
Then computes: stable-sort benchmark, exact within-block conditional means, and the exact
C=2 conditional tail probability by dynamic programming (plus a seeded Monte Carlo).
Env MORPHOLIB_PIN must point at a checkout of bfe377c.
"""
import os, sys, json, random
from fractions import Fraction as F
import numpy as np
PIN = os.environ["MORPHOLIB_PIN"]
sys.path.insert(0, os.path.join(PIN, "sorting-morphogenesis"))
import sorting_morphogenesis as SM  # noqa: E402

def H(types): return sum(1 for i in range(len(types) - 1) if types[i] == types[i + 1])

n, reps, seed = 80, 15, 42
rng = np.random.default_rng(seed)
mult = [1, 2, 4, 8, 10, 20, 40]
runs = []
for C in mult:
    n_keys = n // C
    for r in range(reps):
        vals = list(rng.permutation([(i % n_keys) + 1 for i in range(n)]))
        at = ["B"] * (n // 2) + ["S"] * (n // 2)
        rng.shuffle(at)
        cells = SM.make_cells(vals, at)
        init = [(c.value, c.algotype, c.uid) for c in cells]
        res = SM.simulate(cells, seed=seed * 500 + C * 31 + r)
        final = [(c.value, c.algotype, c.uid) for c in cells]
        assert [x[0] for x in final] == res.final_values
        # continuation: run again from the final state with existing internal state
        k_before = res.swaps
        res2 = SM.simulate(cells, seed=12345 + r, stop_when_sorted=False)
        runs.append({"C": C, "r": r, "init": init, "final": final, "agg_final": res.aggregation_trace[-1],
                     "continuation_swaps": res2.swaps})

out = {}
by_C = {C: [x for x in runs if x["C"] == C] for C in mult}
out["final_agg_mean_by_C"] = {C: round(float(np.mean([x["agg_final"] for x in rs])), 4) for C, rs in by_C.items()}
out["final_agg_sem_by_C"] = {C: round(float(np.std([x["agg_final"] for x in rs]) / np.sqrt(reps)), 4) for C, rs in by_C.items()}

# equal-key reversals (global stability) ------------------------------------------
def reversed_equal_pair(init, final):
    pos = {u: i for i, (_, _, u) in enumerate(final)}
    groups = {}
    for i, (v, _, u) in enumerate(init):
        groups.setdefault(v, []).append(u)
    for v, us in groups.items():
        p = [pos[u] for u in us]
        if any(p[i] > p[i + 1] for i in range(len(p) - 1)):
            return True
    return False
dup = [x for x in runs if x["C"] >= 2]
out["duplicate_runs"] = len(dup)
out["duplicate_runs_with_equal_key_reversal"] = sum(reversed_equal_pair(x["init"], x["final"]) for x in dup)
out["runs_total"] = len(runs)
out["runs_with_zero_continuation_swaps"] = sum(x["continuation_swaps"] == 0 for x in runs)

# stable-sort benchmark and within-block conditional mean at C = 10 ------------------
def stable_types(init):
    return [t for (_, t, _) in sorted(init, key=lambda z: z[0])]  # Python sort is stable
def blocks(final):
    out_, cur = [], []
    for v, t, _ in final:
        if cur and cur[-1][0] != v:
            out_.append(cur); cur = []
        cur.append((v, t))
    out_.append(cur)
    return [[t for _, t in b] for b in out_]
def cond_mean_H(final):
    E = F(0); bl = blocks(final)
    for b in bl:
        m = len(b); nb = b.count("B"); ns = m - nb
        if m > 1:
            E += F(nb * (nb - 1) + ns * (ns - 1), m)  # (m-1) * P(match) ; P = [..]/(m(m-1))
    for b1, b2 in zip(bl, bl[1:]):
        E += F(b1.count("B"), len(b1)) * F(b2.count("B"), len(b2)) + F(b1.count("S"), len(b1)) * F(b2.count("S"), len(b2))
    return E
for C in (2, 10):
    rs = by_C[C]
    out[f"C{C}_stable_sort_benchmark_mean_A"] = float(np.mean([H(stable_types(x["init"])) / n for x in rs]))
    out[f"C{C}_within_block_conditional_mean_A_exact"] = float(sum(cond_mean_H(x["final"]) for x in rs) / (len(rs) * n))
    out[f"C{C}_observed_total_H"] = sum(H([t for _, t, _ in x["final"]]) for x in rs)
    out[f"C{C}_conditional_expected_total_H"] = float(sum(cond_mean_H(x["final"]) for x in rs))

# exact distribution of total H at C=2 under within-block permutation -----------------
def run_H_distribution(final):
    """DP over blocks: state = type of last cell; returns dict H -> probability (Fraction)."""
    bl = blocks(final)
    dist = {}  # (last_type, H) -> prob
    def orders(b):
        # distinct internal orders of a block, uniformly over permutations
        from itertools import permutations
        perms = list(permutations(range(len(b))))
        cnt = {}
        for p in perms:
            seq = tuple(b[i] for i in p); cnt[seq] = cnt.get(seq, 0) + 1
        return {s: F(c, len(perms)) for s, c in cnt.items()}
    first = True
    for b in bl:
        new = {}
        for seq, ps in orders(b).items():
            hin = H(list(seq))
            if first:
                key = (seq[-1], hin); new[key] = new.get(key, 0) + ps
            else:
                for (lt, h), p in dist.items():
                    key = (seq[-1], h + hin + (1 if lt == seq[0] else 0))
                    new[key] = new.get(key, 0) + p * ps
        dist, first = new, False
    tot = {}
    for (_, h), p in dist.items():
        tot[h] = tot.get(h, 0) + p
    return tot
def convolve(a, b):
    c = {}
    for x, p in a.items():
        for y, q in b.items():
            c[x + y] = c.get(x + y, 0) + p * q
    return c
total = {0: F(1)}
for x in by_C[2]:
    total = convolve(total, run_H_distribution(x["final"]))
mu = sum(h * p for h, p in total.items())
obs = out["C2_observed_total_H"]
p_two = sum(p for h, p in total.items() if abs(h - mu) >= abs(obs - mu))
out["C2_exact_mean_total_H"] = float(mu)
out["C2_exact_two_sided_distance_tail_p"] = float(p_two)
# Monte Carlo, 100,000 draws, seeded
mc = random.Random(20261031); hits = 0; D = 100000
bls = [blocks(x["final"]) for x in by_C[2]]
for _ in range(D):
    s = 0
    for bl in bls:
        seq = []
        for b in bl:
            b2 = b[:]; mc.shuffle(b2); seq += b2
        s += H(seq)
    hits += abs(s - mu) >= abs(obs - mu)
out["C2_monte_carlo_p_100k"] = hits / D
json.dump(out, open("results/n_replay_bfe377c.json", "w"), indent=1)
print(json.dumps(out, indent=1))
