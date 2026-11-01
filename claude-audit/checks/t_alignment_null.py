#!/usr/bin/env python3
"""Null model for Dietz Claim 4's "93.5% alignment" (cos of within-genus g_max vs
between-genus r_max, Schluter 1996) on the 791-species, 17-landmark dataset.

Dietz computes the cosine after projecting every species onto Thompson's 8-parameter
grids (cos 0.935) and compares it with raw 34-D space (cos 0.429). Any projection onto a
low-dimensional subspace can raise this cosine. We recompute it with Dietz's own loaders
and GPA/OPA, replacing the Thompson projection by (a) the top-k PCA subspace of the data,
(b) random k-dim subspaces, k in {4, 7, 8}. If those also give ~0.93, the alignment is not
evidence for Thompson's grids specifically.
Env MORPHOLIB must point at the morpholib checkout (HEAD 35d30f4)."""
import os, sys, json, importlib.util
from collections import defaultdict
import numpy as np
ROOT = os.environ["MORPHOLIB"]
os.chdir(ROOT); sys.path.insert(0, ROOT)
spec = importlib.util.spec_from_file_location("sil", os.path.join(ROOT, "thompson/1917-thompson-silhouette-area-paradox.py"))
sil = importlib.util.module_from_spec(spec); spec.loader.exec_module(sil)
at, _ = sil.load_modules()
names, families, X = at.load_landmarks()
Y = at.gpa(X); M0 = at.centre_scale(Y.mean(0))
Yo = np.array([at.opa(y, M0) for y in Y])
Z = (Yo - M0).reshape(len(Yo), -1)

gen = defaultdict(list)
for i, n in enumerate(names):
    gen[n.split("_")[0]].append(i)
glist = sorted(g for g, ix in gen.items() if len(ix) >= 3)

def gmax_rmax_cos(Zp):
    W, B = [], []
    for g in glist:
        ix = gen[g]; m = Zp[ix].mean(0)
        B.append(m)  # Z already centred on M0
        W.extend(Zp[i] - m for i in ix)
    W, B = np.array(W), np.array(B)
    vw = np.linalg.svd(W, full_matrices=False)[2][0]
    vb = np.linalg.svd(B, full_matrices=False)[2][0]
    return float(abs(vw @ vb))

out = {"n_species": len(names), "n_genera_ge3": len(glist), "raw_cos": gmax_rmax_cos(Z)}
U = np.linalg.svd(Z - Z.mean(0), full_matrices=False)[2]
rng = np.random.default_rng(20261101)
for k in (4, 7, 8):
    P = U[:k].T @ U[:k]
    out[f"pca{k}_cos"] = gmax_rmax_cos(Z @ P)
    rs = []
    for _ in range(200):
        Q = np.linalg.qr(rng.standard_normal((Z.shape[1], k)))[0]
        rs.append(gmax_rmax_cos(Z @ Q @ Q.T))
    out[f"random{k}_cos_median"] = float(np.median(rs))
    out[f"random{k}_cos_p95"] = float(np.quantile(rs, 0.95))
    out[f"random{k}_frac_ge_0.935"] = float(np.mean(np.array(rs) >= 0.935))
out["dietz_thompson8_cos_reported"] = 0.9352
print(json.dumps(out, indent=1))
os.makedirs(os.path.join(os.environ["AUDIT"], "results"), exist_ok=True)
json.dump(out, open(os.path.join(os.environ["AUDIT"], "results", "t_alignment_null.json"), "w"), indent=1)
