from pathlib import Path
import ast,json,types,math,importlib.util,sys
ROOT=Path(__file__).resolve().parents[1];out={}
p=ROOT/'sources/primary/upstream_InsertionSortCell.py';tree=ast.parse(p.read_text(encoding='utf8'));cl=next(x for x in tree.body if isinstance(x,ast.ClassDef));fn=next(x for x in cl.body if isinstance(x,ast.FunctionDef) and x.name=='is_enable_to_move');mod=ast.Module(body=[fn],type_ignores=[])
class Status:FREEZE='freeze';ACTIVE='active'
ns={'CellStatus':Status};exec(compile(mod,str(p),'exec'),ns);enable=ns['is_enable_to_move']
cells=[types.SimpleNamespace(value=3,status=Status.ACTIVE),types.SimpleNamespace(value=1,status=Status.FREEZE)]
obj=types.SimpleNamespace(reverse_direction=False,left_boundary=(0,1),current_position=(2,1),cells=cells)
with_branch=enable(obj);fn2=ast.parse(ast.unparse(fn)).body[0];loop=next(z for z in fn2.body if isinstance(z,ast.For));loop.body=[z for z in loop.body if not (isinstance(z,ast.If) and 'CellStatus.FREEZE' in ast.unparse(z.test))];exec(compile(ast.fix_missing_locations(ast.Module(body=[fn2],type_ignores=[])),'ablation','exec'),ns);without_branch=ns['is_enable_to_move'](obj)
out['exact_upstream_insertion_isolated']={'prefix_values':[3,1],'frozen_index':1,'with_FREEZE_branch':with_branch,'without_FREEZE_branch':without_branch};assert with_branch and not without_branch
# Static call targets: primary source does not reset on every swap.
t=ast.parse((ROOT/'sources/primary/upstream_MultiThreadCell.py').read_text());c=next(z for z in t.body if isinstance(z,ast.ClassDef) and z.name=='MultiThreadCell');f=next(z for z in c.body if isinstance(z,ast.FunctionDef) and z.name=='swap');calls=[ast.unparse(z.func) for z in ast.walk(f) if isinstance(z,ast.Call)];out['upstream_swap_calls']=calls;out['swap_calls_update']=any(z.endswith('.update') for z in calls);assert not out['swap_calls_update']
# Freeze-reset in reverse direction is -1 in primary, +infinity in surrogate.
obj=types.SimpleNamespace(reverse_direction=True,left_boundary=(0,1),current_position=(2,1),cells=[types.SimpleNamespace(value=50,status=Status.FREEZE),types.SimpleNamespace(value=3,status=Status.ACTIVE)])
out['reverse_freeze_prefix']={'source_returns':enable(obj),'surrogate_returns':True,'prefix':[50,3],'frozen_index':0,'meaning':'Primary resets to -1 even in decreasing direction; surrogate resets to +infinity.'}
# A coarse-graining needs lumpability before treating aggregate dynamics as a closed Markov chain.
from itertools import permutations
ps=list(permutations(range(1,5)));d=lambda x:sum(a>b for a,b in zip(x,x[1:]));i=lambda x:sum(a>b for j,a in enumerate(x) for b in x[j+1:])
examples={}
for v in ps:
 act=[j for j in range(len(v)) if (j and v[j]<v[j-1]) or (j+1<len(v) and v[j]>v[j+1])];weights={}
 if not act:continue
 for j in act:
  for step in [-1,1]:
   k=j+step
   if 0<=k<len(v) and ((step==-1 and v[j]<v[k]) or(step==1 and v[j]>v[k])):
    w=list(v);w[j],w[k]=w[k],w[j];weights[tuple(w)]=weights.get(tuple(w),0)+.5/len(act)
 total=sum(weights.values());agg={}
 for w,prob in weights.items():agg[d(w)]=agg.get(d(w),0)+prob/total
 key=d(v)
 if key in examples and examples[key]['macro_probs']!=agg:
  out['E_non_lumpability_witness']={'same_E':key,'first':examples[key],'second':{'state':v,'macro_probs':agg}};break
 examples[key]={'state':v,'macro_probs':agg}
# Check author text's transport ratio with stated thermal voltage, plus dimensional assumptions.
out['thermal_voltage']={'at_298K_mV':8.314462618*298/96485.33212*1000,'article_model_claim_mV':25.85,'exp40_over_25_85':math.exp(40/25.85),'model_claim_ratio':4.7002,'interpretation':'Approximation 4.7 reasonable, but thermal voltage 25.85mV is about 300K, not 298K. Conductance cancellation requires positive coupling and zero-flux assumptions.'}
(ROOT/'results/source_semantics_checks.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))

