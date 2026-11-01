from pathlib import Path
import numpy as np,itertools,json,importlib.util,sys
ROOT=Path(__file__).resolve().parents[1]
def inv(x):return sum(a>b for i,a in enumerate(x) for b in x[i+1:])
def measure(T):
 n=len(T);q=T[T>0];rows=-np.sum(np.where(T>0,T*np.log2(np.maximum(T,1e-300)),0),axis=1);u=T.mean(0);h=-sum(x*np.log2(x) for x in u if x>0);det=1-rows.mean()/np.log2(n);deg=1-h/np.log2(n);return {'determinism':det,'degeneracy':deg,'cp_eff':det-deg,'EI_bits':h-rows.mean()}
def lump(T,labels):
 lev=sorted(set(labels));G=np.array([[int(x==k) for k in lev] for x in labels]);return (G.T@T@G)/np.sum(G,axis=0)[:,None]
res={}
for n in [3,4,5,6]:
 ps=list(itertools.permutations(range(n)));idx={x:i for i,x in enumerate(ps)};T=np.zeros((len(ps),len(ps)));R=T.copy();I=[];E=[];M=[]
 for j,x in enumerate(ps):
  I.append(inv(x));E.append(sum(a>b for a,b in zip(x,x[1:])));M.append(inv(x)*2+int(x[0]>=n//2));active=[i for i in range(n) if (i>0 and x[i]<x[i-1]) or(i+1<n and x[i]>x[i+1])]
  if not active:T[j,j]=R[j,j]=1;continue
  for i in active:
   for side in [-1,1]:
    k=i+side;p=.5/len(active)
    if 0<=k<n and ((side==-1 and x[i]<x[k])or(side==1 and x[i]>x[k])):
     z=list(x);z[i],z[k]=z[k],z[i];R[j,idx[tuple(z)]]+=p
    else:R[j,j]+=p
  T[j]=R[j];T[j,j]=0;T[j]/=T[j].sum()
 assert np.max(abs(T.sum(1)-1))<1e-12 and np.max(abs(R.sum(1)-1))<1e-12
 micro=measure(T);ir=measure(lump(R,I));mr=measure(R);iv=measure(lump(T,I));ev=measure(lump(T,E));meso=measure(lump(T,M))
 res[n]={'micro_swap':micro,'macro_I_swap':iv,'macro_E_swap':ev,'meso_swap':meso,'micro_raw':mr,'macro_I_raw':ir,'delta_cp_swap':iv['cp_eff']-micro['cp_eff'],'delta_cp_raw_like_for_like':ir['cp_eff']-mr['cp_eff'],'zero_incoming_states_swap':int(np.sum(T.sum(0)==0))}
(ROOT/'results/causal_measures_independent.json').write_text(json.dumps(res,indent=2),encoding='utf8');print('n6',json.dumps(res[6],indent=2))
# Re-run Python's separately coded port and compare final arrays with freshly run Node and archived C++ output.
p=ROOT/'external/morpholib/sorting-morphogenesis/verify_multilang_ports.py';sp=importlib.util.spec_from_file_location('audit_ports',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);py=m.run_python_splitmix_kymograph(42);js=json.loads((ROOT/'results/node_port_output.json').read_text(encoding='utf8'));cpp=json.loads((ROOT/'external/morpholib/sorting-morphogenesis/cpp/cpp_validation_benchmarks.json').read_text(encoding='utf8'));checks={a:py[a]['final_values']==js['kymograph_n42'][a+'_final_values']==cpp['kymograph_n42'][a+'_final_values'] for a in ['bubble','insertion','selection']};assert all(checks.values())
(ROOT/'results/language_port_check.json').write_text(json.dumps({'fresh_python_vs_fresh_node_vs_archived_cpp_final_arrays':checks,'cells_checked':126,'cpp_node_benchmark_outputs_match':cpp['benchmarks']==js['benchmarks'],'full_time_traces_compared':False,'cpp_recompiled':False,'upstream_source_dynamics_equivalence_proved':False,'windows_cli_note':'The original ES-module direct-entry guard silently skipped work on Windows. A separate pathname-normalizing wrapper invoked the unmodified module.'},indent=2),encoding='utf8');print('port arrays',checks,'archived cpp benchmark match',cpp['benchmarks']==js['benchmarks'])
