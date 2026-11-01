from pathlib import Path
import json,urllib.request,hashlib,csv,importlib.util,sys,numpy as np
ROOT=Path(__file__).resolve().parents[1];repo=ROOT/'external/morpholib';tree=json.loads((ROOT/'sources/morpholib_tree.json').read_text(encoding='utf8'))['tree']
paths=[x['path'] for x in tree if x['type']=='blob' and x['path'] in ['datasets/thompson/trimmed_tps_Claverie2014.csv','datasets/thompson/thompson_1917_exact_species_landmarks.json']]
for p in paths:
 dst=repo/p;dst.parent.mkdir(parents=True,exist_ok=True)
 with urllib.request.urlopen('https://raw.githubusercontent.com/fractastical/morpholib/35d30f4cfd5397ee1ed769f96494e018603e293d/'+p,timeout=30) as f:dst.write_bytes(f.read())
p=repo/'datasets/thompson/trimmed_tps_Claverie2014.csv';assert hashlib.sha256(p.read_bytes()).hexdigest()=='ab5315f3be273285c101299457093199e98ff0b1d0fcf08331cc303b2f07e6bd'
# Re-estimate the calibration from original specimen data and landmark methods, without rebuilding all tree predictions.
def mod(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
at=mod('audit_atlas',repo/'thompson/1917-thompson-four-families-atlas.py');eng=mod('audit_engine',repo/'thompson/run_phylogenetic_prediction_engine.py');names,fams,X=at.load_landmarks();Y=at.gpa(X);M0=at.centre_scale(Y.mean(0));Yopa=np.array([at.opa(y,M0) for y in Y]);B,Rg=eng.thompson_mode_basis(M0);D=(Yopa-M0).reshape(len(names),-1);Z=np.linalg.lstsq(B,D.T,rcond=None)[0].T
from scipy import stats
from collections import defaultdict
raw=defaultdict(lambda:defaultdict(list))
for r in csv.DictReader((ROOT/'sources/primary/FishShapes_specimensv1.csv').open(encoding='utf-8-sig')):
 try:sl=float(r['Standard_length'])
 except ValueError:continue
 if sl<=0:continue
 z=[x for x in r['Tree_name'].strip().replace(' ','_').split('_') if x]
 if len(z)<2:continue
 nm=z[0].capitalize()+'_'+z[1].lower()
 for k,c in [('BDmax_over_SL','Max_body_depth'),('CPD_over_SL','Min_caudalpeduncle_depth')]:
  try:v=float(r[c])
  except ValueError:continue
  if v>0:raw[nm][k].append(v/sl)
# Ratios exactly specified at registration.
pre=mod('audit_registration',repo/'thompson/preregister_blind_predictions.py');ratios=pre.ratios_vec(Yopa);stored=json.loads((repo/'thompson_blind_test_results.json').read_text(encoding='utf8'))['calibration'];cal={}
for k in ['BDmax_over_SL','CPD_over_SL']:
 xs=[];ys=[]
 for i,n in enumerate(names):
  if k in raw.get(n,{}):xs.append(float(ratios[k][i]));ys.append(float(np.median(raw[n][k])))
 fit=stats.linregress(xs,ys);cal[k]={'n':len(xs),'alpha':fit.intercept,'beta':fit.slope,'max_abs_coefficient_difference':max(abs(fit.intercept-stored[k]['alpha']),abs(fit.slope-stored[k]['beta']))};assert cal[k]['max_abs_coefficient_difference']<1e-12
out={'original_landmark_sha256_verified':True,'n_landmark_species':len(names),'calibration_reestimated':cal,'interpretive_rate_ratio_check':{'791_species_loading_ratio':47/14.41,'10303_species_loading_ratio':85.40891046529265/9.218072912214746,'units':'ratio of variance-loading percentages; not change per unit time'},'GPA_implementation_boundary':'Uses source GPA and registered proxy definitions, so this verifies recomputation but is not a fully independent morphometrics implementation.'}
(ROOT/'results/morphometrics_calibration_check.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
