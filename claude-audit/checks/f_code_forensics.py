#!/usr/bin/env python3
"""Code-provenance checks on Zhangtaining/cell_research (machine-checkable versions of F1-F3).
F1  committed source: who may swap with a FREEZE cell (movable vs immovable semantics).
F2  __pycache__ headers: source mtime and size recorded at compile time vs committed files;
    which bytecode generation contains is_enable_to_move and a FREEZE-target check in swap().
F3  does any version call update() inside swap()?
Needs: git, python3 -m pip install xdis. Env CELL_RESEARCH."""
import os, re, sys, json, glob, struct, subprocess, datetime
UP = os.environ["CELL_RESEARCH"]; MT = os.path.join(UP, "modules", "multithread")
out = {}
git = lambda *a: subprocess.run(["git", "-C", UP, *a], capture_output=True, text=True).stdout.strip()
out["head"] = git("rev-parse", "HEAD")
out["cell_file_last_commits"] = {f: git("log", "-1", "--format=%h %ad", "--date=short", "--", f"modules/multithread/{f}")
                                 for f in ("BubbleSortCell.py", "InsertionSortCell.py", "SelectionSortCell.py", "MultiThreadCell.py")}
src = {f: open(os.path.join(MT, f)).read() for f in ("BubbleSortCell.py", "InsertionSortCell.py", "SelectionSortCell.py", "MultiThreadCell.py")}
swap_body = src["MultiThreadCell.py"].split("def swap")[1].split("def update")[0]
out["F1"] = {
    "swap_blocks_only_frozen_initiator": "if self.status == CellStatus.FREEZE:" in swap_body and "# or current_cell_at_target.status == CellStatus.FREEZE" in swap_body,
    "bubble_should_move_to_accepts_FREEZE_target": "self.cells[int(target_position[0])].status == CellStatus.FREEZE" in src["BubbleSortCell.py"],
    "insertion_should_move_to_accepts_FREEZE_target": "self.cells[int(target_position[0])].status == CellStatus.FREEZE" in src["InsertionSortCell.py"],
    "selection_swaps_into_FREEZE_target": "self.swap(target_position) # in order to count frozen cell swap attempts" in src["SelectionSortCell.py"],
    "insertion_freeze_reset_line": [i + 1 for i, l in enumerate(src["InsertionSortCell.py"].splitlines()) if "CellStatus.FREEZE" in l and "self.cells[i]" in l],
}
pyc = {}
tracked = set(git("ls-files", "modules/multithread/__pycache__").split())  # only bytecode committed upstream
for f in sorted(glob.glob(os.path.join(MT, "__pycache__", "*.pyc"))):
    if os.path.relpath(f, UP).replace(os.sep, "/") not in tracked:
        continue
    b = open(f, "rb").read(16)
    mtime, size = struct.unpack("<I", b[8:12])[0], struct.unpack("<I", b[12:16])[0]
    s = os.path.join(MT, os.path.basename(f).split(".")[0] + ".py")
    dis = subprocess.run([sys.executable, "-m", "xdis", f], capture_output=True, text=True).stdout
    swap_dis = dis.split("Method Name:       swap")[1].split("# Method Name:")[0] if "Method Name:       swap" in dis else ""
    pyc[os.path.basename(f)] = {
        "source_mtime_utc": datetime.datetime.fromtimestamp(mtime, datetime.timezone.utc).isoformat(),
        "source_size_at_compile": size, "committed_size": os.path.getsize(s) if os.path.exists(s) else None,
        "has_is_enable_to_move": "is_enable_to_move" in dis,
        "swap_FREEZE_checks": swap_dis.count("(FREEZE)"),
        "swap_calls_update": "LOAD_METHOD          (update)" in swap_dis or "LOAD_ATTR            (update)" in swap_dis,
    }
out["F2_pyc"] = pyc
out["F3_any_swap_calls_update"] = any(v["swap_calls_update"] for v in pyc.values()) or "update()" in swap_body
os.makedirs("results", exist_ok=True); json.dump(out, open("results/f_code_forensics.json", "w"), indent=1)
print(json.dumps(out["F1"]), "\nF3:", out["F3_any_swap_calls_update"])
for k in ("InsertionSortCell.cpython-310.pyc", "InsertionSortCell.cpython-311.pyc", "MultiThreadCell.cpython-310.pyc", "MultiThreadCell.cpython-311.pyc"):
    print(k, pyc.get(k))
