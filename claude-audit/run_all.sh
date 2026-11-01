#!/usr/bin/env bash
# Re-run every check in this bundle from scratch. Deterministic checks first, stochastic last.
# Requirements: git; python3 with requirements-audit.txt; node (>=18); Lean 4.35.0 via elan (lean-toolchain).
# MODE=deterministic runs only the exact, seeded and network checks (used by CI).
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1  # never add bytecode to the upstream clone (f_code_forensics reads it)
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE"
WORK="${WORK:-$HERE/_work}"; mkdir -p "$WORK" results
# 1. Pinned upstream sources
[ -d "$WORK/cell_research" ] || git clone -q https://github.com/Zhangtaining/cell_research.git "$WORK/cell_research"
git -C "$WORK/cell_research" checkout -q 1fd2bd5921c1f6b423a71f691d5189106a8a1020
sparse_clone () {  # $1 dest, $2 commit: partial, sparse clone (the full morpholib history is ~3 GB)
  if [ ! -d "$1" ]; then
    git clone -q --filter=blob:none --no-checkout https://github.com/fractastical/morpholib.git "$1"
    git -C "$1" sparse-checkout set sorting-morphogenesis thompson datasets/thompson morphoeval/lean
  fi
  git -C "$1" checkout -q "$2"
  mkdir -p "$1/docs/media"
}
sparse_clone "$WORK/morpholib" 35d30f4cfd5397ee1ed769f96494e018603e293d
sparse_clone "$WORK/morpholib_bfe377c" bfe377c2f9d5bfc35e0083df1c04eb9fe6ca739e
export CELL_RESEARCH="$WORK/cell_research" MORPHOLIB="$WORK/morpholib" MORPHOLIB_PIN="$WORK/morpholib_bfe377c" AUDIT="$HERE"
# 2. Deterministic: exact math (Python + independent Node), Lean, code forensics, isolated prefix test
python3 -I checks/m_exact_math.py
node checks/m_crosscheck.mjs
lean lean/AdjacentSwap.lean
lean "$MORPHOLIB/morphoeval/lean/loops/Loop_zhang_sorting_morphogenesis.lean"
python3 checks/f_code_forensics.py
python3 checks/u_isolated_prefix.py
# 3. Deterministic replays of Dietz's model (seeded)
python3 checks/n_replay_bfe377c.py          # Sweet's Oct 31 numbers at bfe377c
python3 checks/t_alignment_null.py          # Claim 4 alignment vs random/PCA subspaces
(cd "$MORPHOLIB/sorting-morphogenesis" && python3 audit_platonic_space_claims.py >/dev/null && \
  python3 -m json.tool figures/platonic_claims_ablation_metrics.json > "$HERE/results/dietz_ablation_rerun.json")
# 4. Network: DOI metadata
python3 checks/d_references.py
python3 checks/d_method_refs.py
# 5. Stochastic (threaded upstream code; results are distributions, compare within SE)
if [ "${MODE:-full}" = "deterministic" ]; then echo "Deterministic checks completed."; exit 0; fi
REPS=20 python3 checks/r_upstream.py
REPS=15 python3 checks/r_upstream_agg.py
# Sweet's Oct 31 endpoint tests on the original threaded code (held-out inputs), plus calibration
REPS=15 OUT=results/r_upstream_sweet_main.json python3 checks/r_upstream_sweet.py
CS=2 REPS=15 OUT=results/r_upstream_sweet_C2_negctrl.json python3 checks/r_upstream_sweet.py
CS=2 REPS=15 SEEDBASE=8000 OUT=results/r_upstream_sweet_C2_seed8000.json python3 checks/r_upstream_sweet.py
DRAWS=300 python3 checks/r_conditional_test_calibration.py
sha256sum results/*.json > results/SHA256SUMS
echo "All checks completed."
