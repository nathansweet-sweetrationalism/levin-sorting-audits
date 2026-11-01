from pathlib import Path
import importlib.util,sys,random,itertools,json,numpy as np
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'sources/primary/old_model.py';sp=importlib.util.spec_from_file_location('robust_old',p);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
def agg(a):return sum(x==y for x,y in zip(a,a[1:]))/len(a)
def run(vals,tags,seed,reset=True,all_cells=False,null=False):
 cells=m.make_cells(vals,['B']*len(vals) if null else tags);rng=random.Random(seed);n=len(vals);peak=agg(tags);swaps=0;steps=0
 while steps<n*n*40:
  vals_now=[c.value for c in cells]
  if m.monotonicity_error(vals_now)==0:break
  act=m._compute_active_indices(cells)
  if not act:break
  p=rng.randrange(n) if all_cells else act[rng.randrange(len(act))];steps+=1;q,d=m._propose(cells,p,rng,selection_reset_on_swap=reset)
  if q:
   i,j=q;cells[i],cells[j]=cells[j],cells[i];swaps+=1
   if reset:
    m._reset_selection_target(cells[i],n);m._reset_selection_target(cells[j],n)
   else:
    for k in [i,j]:
     if cells[k].algotype=='S' and cells[k].target>k:cells[k].target=0
   peak=max(peak,agg([tags[c.uid] for c in cells]))
 return {'peak_A':peak,'final_A':agg([tags[c.uid] for c in cells]),'final_error':m.monotonicity_error([c.value for c in cells]),'swaps':swaps,'steps':steps,'step_cap_hit':steps==n*n*40}
rng=np.random.default_rng(20261101);rows=[]
for r in range(30):
 v=list(map(int,rng.permutation(range(40))));tags=['B']*20+['S']*20;rng.shuffle(tags);null=run(v,tags,772000+r,True,False,True)
 for reset,allc in itertools.product([True,False],[False,True]):
  z=run(v,tags,993000+r,reset,allc);rows.append({'run':r,'reset':reset,'scheduler':'all_cells' if allc else 'active_cells',**z,'control_peak_A':null['peak_A'],'peak_minus_control':z['peak_A']-null['peak_A']})
summary=[]
for reset,allc in itertools.product([True,False],[False,True]):
 z=[x for x in rows if x['reset']==reset and x['scheduler']==('all_cells' if allc else 'active_cells')];summary.append({'reset':reset,'scheduler':z[0]['scheduler'],'n_runs':len(z),'mean_peak_A':float(np.mean([x['peak_A'] for x in z])),'mean_peak_minus_control':float(np.mean([x['peak_minus_control'] for x in z])),'mean_final_A':float(np.mean([x['final_A'] for x in z])),'expected_final_A':.475,'not_sorted':sum(x['final_error']>0 for x in z),'caps':sum(x['step_cap_hit'] for x in z)})
(ROOT/'results/fresh_robustness.json').write_text(json.dumps({'protocol':'checkpoints/05_frozen_robustness_protocol.md','runs':rows,'summary':summary},indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
