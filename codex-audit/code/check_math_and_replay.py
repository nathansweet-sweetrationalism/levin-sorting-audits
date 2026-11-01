from pathlib import Path
import json,itertools,collections,math,random,time,importlib.util,sys,ast
from fractions import Fraction as Q
ROOT=Path(__file__).resolve().parents[1]
def save(name,x): (ROOT/'results'/name).write_text(json.dumps(x,indent=2),encoding='utf8')
def inv(v): return sum(a>b for i,a in enumerate(v) for b in v[i+1:])
def desc(v):return sum(a>b for a,b in zip(v,v[1:]))
def matches(a):return sum(x==y for x,y in zip(a,a[1:]))
def ag(a):return Q(matches(a),len(a))
start=time.perf_counter(); counts={'adjacent_distinct':0,'adjacent_duplicate':0,'nonadjacent_duplicate':0,'fixed_count_arrangements':0}
for n in range(2,9):
 for v in itertools.permutations(range(n)):
  before=inv(v)
  for i in range(n-1):
   if v[i]>v[i+1]:
    w=list(v);w[i],w[i+1]=w[i+1],w[i]; assert inv(w)==before-1;counts['adjacent_distinct']+=1
for n in range(2,8):
 for v in itertools.product(range(3),repeat=n):
  before=inv(v)
  for i in range(n-1):
   if v[i]>v[i+1]:
    w=list(v);w[i],w[i+1]=w[i+1],w[i];assert inv(w)==before-1;counts['adjacent_duplicate']+=1
  for i in range(n):
   for j in range(i+1,n):
    if v[i]>v[j]:
     w=list(v);a,b=w[i],w[j];w[i],w[j]=b,a
     predicted=1+sum(int(b<=x<a)+int(b<x<=a) for x in v[i+1:j])
     assert before-inv(w)==predicted;counts['nonadjacent_duplicate']+=1
for n in range(2,13):
 for b in range(n+1):
  vals=[]
  for idx in itertools.combinations(range(n),b):
   a=[0]*n
   for i in idx:a[i]=1
   vals.append(matches(a));counts['fixed_count_arrangements']+=1
  got=Q(sum(vals),len(vals)*n);expected=Q(b*(b-1)+(n-b)*(n-b-1),n*n);assert got==expected
exact={'counts':counts,'balanced_N80':str(Q(39,80)),'balanced_N80_float':float(Q(39,80)),'rulers':{'before':[2,4,1,3],'after':[2,1,4,3],'I':[3,2],'E':[1,2]},'nonlocal_counterexample':{'before':[3,2,1],'after':[1,2,3],'delta_I':-3},'local_minimum_with_barrier':{'values':[2,1,0],'frozen_index':1,'adjacent_swaps_legal':0,'inversions':3},'score_average':sum([66.7,13.5,86.5,96.1,95.0,95.0,90.1])/7,'structural_average':sum([100,40.5,100,96.1,95,95,90.1])/7,'nernst_ratio_298_15K_40mV':math.exp(96485.33212*.040/(8.314462618*298.15)),'elapsed_seconds':time.perf_counter()-start}
save('independent_math.json',exact);print(json.dumps(exact),flush=True)
# Independent AST check: reporting labels are literals, not acceptance decisions.
p=ROOT/'external/morpholib/sorting-morphogenesis/validate_kymograph_and_paper.py';t=ast.parse(p.read_text(encoding='utf-8-sig'))
labels=[]
for x in ast.walk(t):
 if isinstance(x,ast.Dict):
  d={k.value:v for k,v in zip(x.keys,x.values) if isinstance(k,ast.Constant)}
  if 'benchmark_id' in d and 'status' in d:labels.append({'benchmark':ast.literal_eval(d['benchmark_id']),'status_expr':ast.unparse(d['status']),'line':x.lineno})
save('benchmark_label_audit.json',labels);assert len(labels)==14 and all(x['status_expr']=="'VERIFIED'" for x in labels)
(ROOT/'checkpoints/02_exact_math.md').write_text('# Checkpoint 02: exact mathematics\nIndependent enumeration passed. See results/independent_math.json and code/check_math_and_replay.py. The benchmark script contains 14 literal VERIFIED labels; these are not calculated acceptance tests. Replay follows and saves every initial/final state.\n',encoding='utf8')
# Replay Sweet's explicitly cited historical implementation, without changing source.
import numpy as np
p=ROOT/'sources/primary/old_model.py';sp=importlib.util.spec_from_file_location('audited_old_model',p);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
rng=np.random.default_rng(42);runs=[];c2_dists=[]
def conditional_mean(v,a):
 groups=[list(g) for k,g in itertools.groupby(zip(v,a),lambda x:x[0])];mean=Q(0)
 for g in groups:
  n=len(g);b=sum(a=='B' for _,a in g);s=n-b
  if n>1:mean+=Q(b*(b-1)+s*(s-1),n)
 for g,h in zip(groups,groups[1:]):
  n,k=len(g),len(h);b=sum(a=='B' for _,a in g);c=sum(a=='B' for _,a in h);mean+=Q(b*c+(n-b)*(k-c),n*k)
 return mean
def c2_dist(a):
 dp={(None,0):1}
 for i in range(0,len(a),2):
  options=set(itertools.permutations(a[i:i+2]));nd=collections.Counter()
  for (last,h),num in dp.items():
   for z in options:nd[(z[-1],h+matches(z)+int(last is not None and last==z[0]))]+=num
  dp=nd
 out=collections.Counter()
 for (_,h),num in dp.items():out[h]+=num
 return out
for C in [1,2,4,8,10,20,40]:
 for r in range(15):
  n=80;k=n//C;values=list(map(int,rng.permutation([(i%k)+1 for i in range(n)])));types=['B']*40+['S']*40;rng.shuffle(types)
  cells=m.make_cells(values,types);res=m.simulate(cells,seed=42*500+C*31+r)
  final=[{'value':c.value,'algotype':c.algotype,'uid':c.uid,'target':c.target} for c in cells]
  unstable=False
  for key in set(values):
   init=[i for i,v in enumerate(values) if v==key];end=[c.uid for c in cells if c.value==key];unstable |= init!=end
  stable=[types[i] for i in sorted(range(n),key=lambda i:values[i])]
  expected=conditional_mean(res.final_values,res.final_algotypes)
  more=m.simulate(cells,stop_when_sorted=False,seed=918273+r+C*31)
  row={'C':C,'run':r,'initial_values':values,'initial_types':types,'final_cells':final,'final_H':matches(res.final_algotypes),'final_A':float(ag(res.final_algotypes)),'stable_A':float(ag(stable)),'conditional_expected_H':str(expected),'conditional_expected_A':float(expected/80),'equal_key_reversed':bool(unstable),'continued_swaps':more.swaps,'final_error':res.final_error,'seed':42*500+C*31+r}
  runs.append(row)
  if C==2:c2_dists.append(c2_dist(res.final_algotypes))
 save('historical_replay_runs.json',runs)
 print('completed C',C,'A',sum(x['final_A'] for x in runs if x['C']==C)/15,flush=True)
summary=[]
for C in [1,2,4,8,10,20,40]:
 z=[x for x in runs if x['C']==C];summary.append({'C':C,'runs':len(z),'mean_A':sum(x['final_A'] for x in z)/15,'mean_stable_A':sum(x['stable_A'] for x in z)/15,'mean_conditional_A':sum(x['conditional_expected_A'] for x in z)/15,'reversed':sum(x['equal_key_reversed'] for x in z),'continued_swaps':sum(x['continued_swaps'] for x in z),'final_errors':sum(x['final_error'] for x in z)})
dist=collections.Counter({0:1})
for d in c2_dists:
 new=collections.Counter()
 for h,a in dist.items():
  for k,b in d.items():new[h+k]+=a*b
 dist=new
total=sum(dist.values());mean=sum(Q(h*c,total) for h,c in dist.items());observed=sum(x['final_H'] for x in runs if x['C']==2);tail=sum(c for h,c in dist.items() if abs(Q(h)-mean)>=abs(Q(observed)-mean));pv=Q(tail,total)
save('historical_replay_summary.json',{'summary':summary,'C2_exact_conditional_test':{'observed_H':observed,'expected_H':str(mean),'tail_probability_fraction':str(pv),'tail_probability':float(pv),'tail_definition':'P(|H-EH|>=|observed-EH|); fixed observed per-key type counts, uniformly permuted within tied blocks independently per run','post_selection':'exploratory; no confirmatory label'},'runtime_seconds':time.perf_counter()-start})
save('C2_conditional_distribution.json',{str(k):str(v) for k,v in sorted(dist.items())});print('C2',observed,str(mean),float(pv),flush=True)
(ROOT/'checkpoints/03_historical_replay.md').write_text('# Checkpoint 03: historical replay completed\n105 historical model runs saved individually with initial/final states and targets. Exact conditional C=2 tail recomputed independently, with exploratory status. See historical_replay_summary.json. This is reproduction of a sequential surrogate, not replication of the original threaded paper experiment.\n',encoding='utf8')
