#!/usr/bin/env python3
"""Sweet's isolated test: upstream InsertionSortCell.is_enable_to_move on prefix [3, frozen 1]
allows movement; removing the FREEZE branch blocks it. No threads are started."""
import os, sys, json, threading
sys.path.insert(0, os.path.dirname(__file__))
import upstream_driver as U
lock = threading.Lock(); probe = U.StatusProbe(); cells = []
vals = [3, 1, 2]
for i, v in enumerate(vals):
    cells.append(U.InsertionSortCell(i + 1, v, lock, (i, 1), cells, (0, 1), (2, 1), probe, disable_visualization=True))
cells[1].set_cell_to_freeze()
with_reset = U._ORIG_ENABLE(cells[2])
strict = U._strict_enable(cells[2])
ok = with_reset is True and strict is False
out = {"prefix": "[3, frozen 1]", "upstream_is_enable_to_move": with_reset, "freeze_branch_removed": strict, "pass": ok}
os.makedirs("results", exist_ok=True); json.dump(out, open("results/u_isolated_prefix.json", "w"), indent=1)
print(out); sys.exit(0 if ok else 1)
