"""Recompute bounded wing checks; uses source GPA/basis, independent raw loading/scoring."""
from pathlib import Path
import json,importlib.util,collections,sys
import numpy as np
from scipy import stats
ROOT=Path(__file__).resolve().parents[1];repo=ROOT/'external/morpholib'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
eng=load('audit_wing_engine',repo/'thompson/run_phylogenetic_prediction_engine.py');at=eng.at
def tab(p):
 s=p.read_text(encoding='utf8').splitlines();i=next(i for i,l in enumerate(s) if l.startswith('*/'));h=s[i+1].split('\t');return [dict(zip(h,l.split('\t'))) for l in s[i+2:] if l.strip()]
spec={r['Spec ID']:r for r in tab(ROOT/'sources/primary/wing_specimens.tab')};rows=tab(ROOT/'sources/primary/wing_landmarks.tab')
saved=json.loads((repo/'thompson/portfolio/results/vespinae_wings.json').read_text());spp=saved['species'];by=collections.defaultdict(list)
xs=[c for c in rows[0] if '(x' in c];ys=[c for c in rows[0] if '(y' in c];assert len(xs)==len(ys)==19
for r in rows:
 s=spec.get(r['Spec ID'])
 if s is None:continue
 n=s['Genus']+'_'+s['Species']
 if n not in spp:continue
 try:a=np.array([[float(r[x]),float(r[y])] for x,y in zip(xs,ys)])
 except ValueError:continue
 by[n].append(a)
allw=np.array([w for s in spp for w in by[s]]);lab=np.array([s for s in spp for w in by[s]]);assert len(allw)==1027
yw=at.gpa(allw);means=np.array([yw[lab==s].mean(0) for s in spp]);Y=at.gpa(means);M=at.centre_scale(Y.mean(0));Yopa=np.array([at.opa(y,M) for y in Y]);D=(Yopa-M).reshape(len(spp),-1)
B,R=eng.thompson_mode_basis(M);Z=np.linalg.lstsq(B,D.T,rcond=None)[0].T;E=D-Z@B.T
share=1-float(np.sum(E**2)/np.sum(D**2));err=float(np.max(np.abs(Yopa-np.array(saved['species_means']))));assert err<1e-10;assert abs(share-saved['variance']['thompson7'])<1e-10
per=np.array([i-1 for i in [1,2,3,11,12,13,15,16,17,18,19]]);inter=np.array([i-1 for i in [4,5,6,7,8,9,10,14]])
d=D.reshape(30,19,2);e=E.reshape(30,19,2);sub=lambda ix:1-float(np.sum(e[:,ix]**2)/np.sum(d[:,ix]**2))
later=json.loads((repo/'thompson/portfolio/results/vespinae_venation_mechanics.json').read_text());assert abs(sub(per)-later['variance']['t7_perimeter_11lm'])<1e-10 if 't7_perimeter_11lm' in later['variance'] else abs(sub(per)-later['hypotheses']['D3']['t7_variance_share_perimeter_11lm'])<1e-10
A={k:np.array([r[k] for r in saved['per_species']]) for k in saved['per_species'][0] if k.startswith('rms')}
med={k:float(np.median(v)) for k,v in A.items()};assert all(abs(v-saved['loo_medians'][k])<1e-12 for k,v in med.items())
h=saved['hypotheses'];assert not any(v['pass'] for v in h.values())
wi=lambda a,b:float(stats.wilcoxon(a-b,alternative='less').pvalue)
p3=wi(A['rms_full'],A['rms_consensus']);p4=wi(A['rms_full'],A['rms_nearest']);p6=wi(A['rms_pca7'],A['rms_thompson7']);assert abs(p3-h['W3']['p'])<1e-12 and abs(p4-h['W4']['p_full_less'])<1e-12
H=json.loads((repo/'thompson/portfolio/groups/vespinae_wings_hypotheses.json').read_text());brier=float(np.mean([(x['p']-float(h[x['id']]['pass']))**2 for x in H['hypotheses']]));assert abs(brier-saved['brier'])<1e-12
out={'raw_wings':len(rows),'retained_wings':len(allw),'species':len(spp),'landmarks':19,'species_means_max_absolute_difference':err,'t7_variance_share':share,'perimeter_fraction':sub(per),'interior_fraction':sub(inter),'loo_saved_prediction_error_medians_recomputed':med,'W1_to_W7_recorded_pass':{k:v['pass'] for k,v in h.items()},'wilcoxon_p_from_saved_predictions':{'W3':p3,'W4':p4,'W6':p6},'brier':brier,'scope':'Raw wing mean shapes and projection fractions recomputed using source GPA and basis. Prediction-error summaries and W decisions checked against saved prediction outputs. Full predictor and all noise/allometry alternatives not independently rebuilt. 1027 specimens are 30 species, not 1027 independent evolutionary replicates. Perimeter landmark split is later model selection and needs held-out confirmation.'}
(ROOT/'results/wing_checks.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
