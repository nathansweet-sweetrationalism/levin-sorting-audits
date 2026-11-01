"""Thin driver for the UNMODIFIED upstream threaded implementation
(Zhangtaining/cell_research @ 1fd2bd5, cell files unchanged since 4a01069).

Only the experiment harness is ours: construction mirrors freezing_sorting_analysis.py
(one CellGroup, huge period, disable_visualization=True, set_cell_to_freeze()).
Termination: stop when no swap has been recorded for `quiet_s` seconds or `max_s` elapsed.
The optional `strict_insertion` flag monkeypatches is_enable_to_move with the textbook
prefix check (the three FREEZE lines removed) for the ablation; nothing else changes.
"""
import os, sys, threading, time, random
UP = os.environ.get("CELL_RESEARCH", os.path.join(os.path.dirname(__file__), "..", "..", "cell_research"))
sys.path.insert(0, os.path.abspath(UP))
from modules.multithread.StatusProbe import StatusProbe            # noqa: E402
from modules.multithread.SelectionSortCell import SelectionSortCell  # noqa: E402
from modules.multithread.BubbleSortCell import BubbleSortCell        # noqa: E402
from modules.multithread.InsertionSortCell import InsertionSortCell  # noqa: E402
from modules.multithread.CellGroup import CellGroup, GroupStatus     # noqa: E402
from modules.multithread.MultiThreadCell import CellStatus, MultiThreadCell  # noqa: E402
_ORIG_SWAP = MultiThreadCell.swap

_ORIG_ENABLE = InsertionSortCell.is_enable_to_move

def _strict_enable(self):
    prev = -1
    for i in range(int(self.left_boundary[0]), int(self.current_position[0])):
        if self.cells[i].value < prev:
            return False
        prev = self.cells[i].value
    return True

CLS = {"B": BubbleSortCell, "S": SelectionSortCell, "I": InsertionSortCell}

def run(values, types, frozen_idx=(), strict_insertion=False, quiet_s=1.0, max_s=60.0, seed=None, track_ids=False):
    if seed is not None:
        random.seed(seed)  # upstream Bubble uses module-level random; threads still interleave freely
    InsertionSortCell.is_enable_to_move = _strict_enable if strict_insertion else _ORIG_ENABLE
    lock = threading.Lock()
    probe = StatusProbe()
    n = len(values)
    lb, rb = (0, 1), (n - 1, 1)
    cells = []
    # fresh mutable defaults: upstream uses shared default lists (swapping_count=[0], export_steps=[])
    sc, ex = [0], []
    for i, (v, t) in enumerate(zip(values, types)):
        cells.append(CLS[t](i + 1, v, lock, (i, 1), cells, lb, rb, probe,
                            disable_visualization=True, swapping_count=sc, export_steps=ex))
    group = CellGroup(cells, cells, 0, lb, rb, GroupStatus.ACTIVE, lock, 10**9, 10**9)
    for c in cells:
        c.group = group
    frozen_cells = []
    for i in frozen_idx:
        cells[i].set_cell_to_freeze()
        frozen_cells.append(cells[i])
    init_frozen_pos = list(frozen_idx)
    id_snaps = []
    if track_ids:
        # Observation only: call the unmodified swap, then record the identity order (lock is already held).
        def _swap(self, target_position, skip_stats=False):
            _ORIG_SWAP(self, target_position, skip_stats)
            if not skip_stats and self.status != CellStatus.FREEZE:
                id_snaps.append([c.threadID for c in cells])
        MultiThreadCell.swap = _swap
    lock.acquire()
    for c in cells:
        c.daemon = True
        c.start()
    group.daemon = True
    group.start()
    lock.release()
    t0 = time.time(); last_n = -1; last_change = t0
    while True:
        time.sleep(0.05)
        k = probe.swap_count
        now = time.time()
        if k != last_n:
            last_n, last_change = k, now
        if now - last_change > quiet_s or now - t0 > max_s:
            break
    lock.acquire()
    for c in cells:
        c.status = CellStatus.INACTIVE
    group.status = GroupStatus.MERGED
    final_vals = [c.value for c in cells]
    final_types = [c.cell_type[0] for c in cells]
    final_frozen_pos = [cells.index(fc) for fc in frozen_cells]
    lock.release()
    InsertionSortCell.is_enable_to_move = _ORIG_ENABLE
    MultiThreadCell.swap = _ORIG_SWAP
    return {"id_snapshots": id_snaps, "final_ids": [c.threadID for c in cells],"final_values": final_vals, "final_types": final_types,
            "value_snapshots": [list(s) for s in probe.sorting_steps],
            "type_snapshots": [[r[1] for r in s] for s in probe.cell_types],
            "swaps": probe.swap_count, "frozen_init": init_frozen_pos,
            "frozen_final": final_frozen_pos, "elapsed_s": time.time() - t0,
            "hit_max_time": time.time() - t0 >= max_s}
