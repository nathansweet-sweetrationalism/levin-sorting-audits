#!/usr/bin/env python3
"""Calibration of Sweet's within-block conditional test under its own null.
Labels: uniform random 40/40 arrangement on a sorted C=2 array (labels independent of movement).
Repeats the 15-run aggregate test many times; under a calibrated test P(p <= a) <= a."""
import random, json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from fractions import Fraction as F
import importlib.util
spec = importlib.util.spec_from_file_location("rs", os.path.join(os.path.dirname(__file__), "r_upstream_sweet.py"))
src = open(spec.origin).read().split("REPS = int")[0]           # reuse helper functions only
ns = {"__file__": spec.origin}; exec(src.replace("import upstream_driver as U", ""), ns)
H, blocks, cond_mean, run_dist = ns["H"], ns["blocks"], ns["cond_mean"], ns["run_dist"]
rng = random.Random(20261101); n = 80; D = int(os.environ.get("DRAWS", "300")); ps = []
vals = sorted([(i % 40) + 1 for i in range(n)])
for d in range(D):
    obs = 0; mu = F(0); tot = {0: F(1)}
    for r in range(15):
        lab = ["B"] * 40 + ["S"] * 40; rng.shuffle(lab)
        bl = blocks(vals, lab); obs += H(lab); mu += cond_mean(bl)
        dd = run_dist(bl); new = {}
        for a, p in tot.items():
            for b, q in dd.items(): new[a + b] = new.get(a + b, 0) + p * q
        tot = new
    ps.append(float(sum(p for h, p in tot.items() if abs(h - mu) >= abs(obs - mu))))
out = {"draws": D, "frac_p_le_0.05": sum(p <= 0.05 for p in ps) / D, "frac_p_le_0.013": sum(p <= 0.0129 for p in ps) / D,
       "frac_p_le_0.01": sum(p <= 0.01 for p in ps) / D, "median_p": sorted(ps)[D // 2]}
print(out); json.dump(out, open("results/r_conditional_test_calibration.json", "w"), indent=1)
