#!/usr/bin/env python3
"""Exact / exhaustive checks of the mathematical claims in both articles.

Every check is an assertion. Results are written to results/m_exact_math.json.
Run: python3 -I checks/m_exact_math.py   (no network, deterministic)
"""
import itertools, json, math, sys, os
from fractions import Fraction as F
from collections import Counter

import sympy as sp

OUT = {}
def record(cid, claim, source, ok, detail):
    OUT[cid] = {"claim": claim, "source": source, "pass": bool(ok), "detail": detail}
    print(("PASS " if ok else "FAIL ") + cid + ": " + claim)

def inv(v):  # I(v): all inverted pairs
    return sum(1 for i in range(len(v)) for j in range(i + 1, len(v)) if v[i] > v[j])
def desc(v):  # E(v): adjacent descents (= upstream monotonicity error)
    return sum(1 for i in range(1, len(v)) if v[i] < v[i - 1])

# M1 worked example ---------------------------------------------------------
a, b = [2, 4, 1, 3], [2, 1, 4, 3]
record("M1", "[2,4,1,3]->[2,1,4,3]: I 3->2, E 1->2", "Dietz Claim 2; Sweet 'A rising score'",
       (inv(a), desc(a), inv(b), desc(b)) == (3, 1, 2, 2),
       {"I": [inv(a), inv(b)], "E": [desc(a), desc(b)]})

# M2 adjacent strict-inversion swap: dI = -1 exactly; dE distribution -----------
dI, dE = Counter(), Counter()
for n in range(2, 9):
    for p in itertools.permutations(range(n)):
        for i in range(n - 1):
            if p[i] > p[i + 1]:
                q = list(p); q[i], q[i + 1] = q[i + 1], q[i]
                dI[inv(q) - inv(p)] += 1
                dE[desc(q) - desc(p)] += 1
record("M2", "Every adjacent strict-inversion swap lowers I by exactly 1 (exhaustive, n<=8 distinct keys)",
       "Dietz Claim 2; Sweet (checked through 8 keys)", set(dI) == {-1},
       {"dI_counts": dict(dI), "dE_counts": dict(dE),
        "fraction_of_downhill_swaps_where_E_rises": float(F(dE[1], sum(dE.values())))})

# M2b with duplicate keys: still -1 (strict comparison) ---------------------------
dIdup = Counter()
for n in range(2, 8):
    for p in itertools.product(range(3), repeat=n):
        for i in range(n - 1):
            if p[i] > p[i + 1]:
                q = list(p); q[i], q[i + 1] = q[i + 1], q[i]
                dIdup[inv(q) - inv(p)] += 1
record("M2b", "Same with duplicate keys (strict inversions, alphabet 3, n<=7)", "extension",
       set(dIdup) == {-1}, dict(dIdup))

# M3 long-range swaps: dI = -(1+2k) for an inverted pair, +(1+2k) otherwise -------
okM3 = True; seen = Counter()
for n in range(2, 8):
    for p in itertools.permutations(range(n)):
        for i in range(n):
            for j in range(i + 1, n):
                q = list(p); q[i], q[j] = q[j], q[i]
                lo, hi = min(p[i], p[j]), max(p[i], p[j])
                k = sum(1 for m in range(i + 1, j) if lo < p[m] < hi)
                expect = -(1 + 2 * k) if p[i] > p[j] else (1 + 2 * k)
                d = inv(q) - inv(p)
                okM3 &= (d == expect); seen[d] += 1
record("M3", "Non-adjacent swap of an inverted pair lowers I by 1+2k (odd, can exceed 1); "
       "swapping a non-inverted pair raises I. So 'dI=-1 on every single swap' holds only for adjacent swaps",
       "Dietz Claim 2 verdict vs. Selection long-range swaps", okM3,
       {"observed_dI_values": sorted(seen)})

# M4 no local minima: every unsorted permutation has an adjacent descent ----------
okM4 = all(desc(p) > 0 for n in range(2, 9) for p in itertools.permutations(range(n)) if list(p) != sorted(p))
record("M4", "I has no non-global local minimum under adjacent transpositions (n<=8)",
       "Dietz Conclusion 'permutations have no local minima'", okM4, "standard (Knuth TAOCP 3, 5.1.1)")

# M5 global stability fails with non-adjacent swaps ----------------------------------
recs = [(2, "a"), (2, "b"), (1, "c")]
r2 = [recs[2], recs[1], recs[0]]
record("M5", "[2a,2b,1c] swap first/last -> [1c,2b,2a]: equal keys reversed without being compared",
       "Sweet, 'Clustering formation and persistence'", [x[1] for x in r2] == ["c", "b", "a"], r2)

# M6 null expectation of A = H/N under uniform arrangement with fixed counts ----------
B, S, N = sp.symbols("b s N", positive=True, integer=True)
EA = (B * (B - 1) + S * (S - 1)) / (B + S) ** 2
simp = sp.simplify(EA.subs(S, B).subs(B, N / 2))
def exact_EA(b, s):
    n = b + s; tot = F(0); cnt = 0
    for pos in itertools.combinations(range(n), b):
        lab = [0] * n
        for x in pos: lab[x] = 1
        tot += F(sum(1 for i in range(n - 1) if lab[i] == lab[i + 1]), n); cnt += 1
    return tot / cnt
enum_ok = all(exact_EA(b, s) == F(b * (b - 1) + s * (s - 1), (b + s) ** 2)
              for b in range(1, 8) for s in range(1, 8))
record("M6", "E[H/N] = [b(b-1)+s(s-1)]/N^2; equal counts -> 1/2 - 1/N; N=80 -> 0.4875, N=100 -> 0.49",
       "Sweet (0.4875); Dietz/paper ('0.50')",
       enum_ok and sp.simplify(simp - (sp.Rational(1, 2) - 1 / N)) == 0,
       {"symbolic_equal_counts": str(simp), "N80": float(F(40 * 39 * 2, 80 ** 2)),
        "N100": float(F(50 * 49 * 2, 100 ** 2)),
        "alt_denominator_N_minus_1_equal_counts_N80": float(F(2 * 40 * 39, 80 * 79)),
        "alt_iid_coinflip_labels_N80": float(F(79, 2 * 80))})

# M7 exchangeability: ANY label-independent permutation gives the same null ------------
# Enumerate small multiset of keys with duplicates and labels; compare final-label
# distributions for (a) stable sort, (b) reverse-stable (maximally unstable) sort,
# (c) an arbitrary fixed key-dependent permutation.
def final_A(keys, labels, order):
    idx = order(keys)
    lab = [labels[i] for i in idx]
    return F(sum(1 for i in range(len(lab) - 1) if lab[i] == lab[i + 1]), len(lab))
stable = lambda k: sorted(range(len(k)), key=lambda i: (k[i], i))
antistable = lambda k: sorted(range(len(k)), key=lambda i: (k[i], -i))
weird = lambda k: sorted(range(len(k)), key=lambda i: (k[i], (i * 7 + 3) % len(k)))
keys = [0, 0, 1, 1, 2, 2]
res = {}
for name, fn in [("stable", stable), ("antistable", antistable), ("arbitrary", weird)]:
    vals = [final_A(keys, [1 if j in pos else 0 for j in range(6)], fn)
            for pos in itertools.combinations(range(6), 3)]
    res[name] = str(sum(vals, F(0)) / len(vals))
record("M7", "Endpoint chance benchmark holds for EVERY sort whose permutation ignores labels "
       "(stable or not); a departure refutes label-independence of movement, not stability as such",
       "bears on Dietz 'critics predict flat 0.50' and Sweet's acceptance of it",
       len(set(res.values())) == 1, res)

# M8 Nernst/Boltzmann factor for a monovalent cation across 40 mV ---------------------
kB, e = 1.380649e-23, 1.602176634e-19   # exact SI (2019)
fac = {f"{T-273.15:.0f}C": math.exp(e * 0.040 / (kB * T)) for T in (293.15, 298.15, 310.15)}
record("M8", "Serotonin (z=+1) equilibrium ratio across -20 vs -60 mV is ~4.7",
       "Dietz Claim 5", 4.4 < fac["25C"] < 5.0, fac)

# M9 scoreboard arithmetic --------------------------------------------------------
cards = {"C1": (F("7.4"), F("11.1")), "C2": (F("1.5"), F("11.1")), "C3": (F("9.6"), F("11.1")),
         "C4": (F("32.0"), F("33.3")), "C5": (F("10.55"), F("11.1")), "C6": (F("10.55"), F("11.1")),
         "C7": (F("10.0"), F("11.1"))}
pct = {k: 100 * a / b for k, (a, b) in cards.items()}
mean7 = sum(pct.values()) / 7
mean7_rounded_inputs = sum(F(x) for x in ["66.7", "13.5", "86.5", "96.1", "95.0", "95.0", "90.1"]) / 7
pillar = (100 * F("18.5") / F("33.3") + pct["C4"] + 100 * F("31.1") / F("33.3")) / 3
four = (pct["C1"] + pct["C2"] + pct["C3"] + pct["C4"]) / 4
struct = (F(100) + F("40.5") + F(100) + F("96.1") + F("95.0") + F("95.0") + F("90.1")) / 7
implied_dualist = {"C1": F("11.1") - F("7.4"), "C2": F("11.1") - F("1.5") / F("0.405"), "C3": F("11.1") - F("9.6")}
record("M9", "Scoreboard arithmetic reproduces 77.6, 65.7, 88.1; the superseded pillar mean is 81.68 (81.7) from exact cards, "
       "81.6 only from rounded inputs with Thompson written as 96.0 instead of 96.1",
       "Dietz 'The Score'",
       round(float(mean7), 1) == 77.6 and round(float(four), 1) == 65.7
       and round(float(struct), 1) == 88.1 and round(float(pillar), 1) == 81.7,
       {"per_claim_pct": {k: round(float(v), 3) for k, v in pct.items()},
        "mean7_exact": float(mean7), "mean7_from_rounded": float(mean7_rounded_inputs),
        "pillar_mean": float(pillar), "four_claim_mean": float(four), "structural": float(struct),
        "thompson_stated_as_96.0_in_pillar_formula_but_32/33.3=": float(pct["C4"]),
        "implied_dualist_deductions_points": {k: float(v) for k, v in implied_dualist.items()},
        "share_of_sorting_deductions_that_are_dualist": float(sum(implied_dualist.values()) / (F("33.3") - F("18.5"))),
        "93.4_check_81.6_over_87.4": 81.6 / 87.4,
        "insertion_ablation_ratio_21.95_over_4.90": 21.95 / 4.90})

# M10 Thompson percentages that can be checked without data ---------------------------
record("M10", "57.9% (7 Thompson modes) <= 86.2% (7-PC PCA) is required by Eckart-Young; '+13% to +48%' over 2.4% "
       "are ratios 6.4x-21x, so '15x' needs a stated base",
       "Dietz Claim 4", 57.9 <= 86.2,
       {"ratio_low": (2.4 + 13) / 2.4, "ratio_high": (2.4 + 48) / 2.4,
        "if_points_are_relative_percent": [1.13, 1.48]})

# M11 Landauer bound ---------------------------------------------------------------
record("M11", "Landauer kT ln 2 at 300 K ~ 2.87e-21 J per erased unbiased bit", "Sweet",
       abs(kB * 300 * math.log(2) - 2.87e-21) < 1e-23, kB * 300 * math.log(2))

# M12 runs-test identity: H = N - R (R = number of runs); Wald-Wolfowitz E[R] = 1 + 2bs/N
okM12 = all(sp.simplify((B + S - (1 + 2 * B * S / (B + S))) / (B + S) - EA) == 0 for _ in [0])
record("M12", "A = H/N = (N - R)/N, so the chance benchmark is the Wald-Wolfowitz runs-test null: E[R] = 1 + 2bs/N",
       "classical anchor for Sweet's E[A]", okM12, "Wald & Wolfowitz 1940, doi:10.1214/aoms/1177731909")

os.makedirs("results", exist_ok=True)
json.dump(OUT, open("results/m_exact_math.json", "w"), indent=2, default=str)
sys.exit(0 if all(v["pass"] for v in OUT.values()) else 1)
