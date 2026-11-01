from pathlib import Path
import sys,json,random,threading,types,itertools
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'external/cell_research'))
from modules.multithread.BubbleSortCell import BubbleSortCell
from modules.multithread.SelectionSortCell import SelectionSortCell
from modules.multithread.InsertionSortCell import InsertionSortCell
from modules.multithread.CellGroup import GroupStatus
from modules.multithread.StatusProbe import StatusProbe
from modules.multithread.MultiThreadCell import CellStatus
inv=lambda v:sum(a>b for i,a in enumerate(v) for b in v[i+1:])
out={'boundary':'Deterministic scheduler invokes unmodified source move() methods under their locks, with visualization disabled, one active group, no threads started. This tests the transition rules, not OS-thread timing.'}
# Directly demonstrate movable frozen target in upstream Bubble, versus the article's general wall wording.
cells=[];probe=StatusProbe();lock=threading.Lock()
for i,v in enumerate([2,1]):cells.append(BubbleSortCell(i,v,lock,(i,1),cells,(0,1),(1,1),probe,disable_visualization=True,swapping_count=[0],export_steps=[]))
for c in cells:c.group=types.SimpleNamespace(status=GroupStatus.ACTIVE,group_id=0)
cells[1].set_cell_to_freeze();permitted=cells[0].should_move_to((1,1),True);cells[0].swap((1,1));out['movable_frozen_primary_example']={'before':[2,1],'frozen_target_swap_permitted':bool(permitted),'after':[c.value for c in cells]}
# Search short actual-source trajectories for inversions rising due to nonlocal Selection and stale target state.
found=None;runs=0
for seed in range(120):
 random.seed(seed);n=6;values=list(range(n));random.shuffle(values);algs=['B']*3+['S']*3;random.shuffle(algs);cells=[];probe=StatusProbe();lock=threading.Lock();classes={'B':BubbleSortCell,'S':SelectionSortCell};history=[]
 for i,(v,a) in enumerate(zip(values,algs)):cells.append(classes[a](i,v,lock,(i,1),cells,(0,1),(n-1,1),probe,disable_visualization=True,swapping_count=[0],export_steps=[]))
 for c in cells:c.group=types.SimpleNamespace(status=GroupStatus.ACTIVE,group_id=0)
 for step in range(800):
  p=random.randrange(n);before=[c.value for c in cells];targets=[c.ideal_position for c in cells];who=cells[p].cell_type;cells[p].move();after=[c.value for c in cells]
  if before!=after:
   history.append({'step':step,'scheduled_position':p,'type':who,'before':before,'before_targets':targets,'after':after,'delta_I':inv(after)-inv(before)})
   if inv(after)>inv(before):found={'seed':seed,'initial_values':values,'initial_types':algs,'history':history};break
  if all(after[i]<=after[i+1] for i in range(n-1)):break
 runs+=1
 if found:break
out['searched_runs']=runs;out['source_uphill_witness']=found
(ROOT/'results/actual_source_transition_checks.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
