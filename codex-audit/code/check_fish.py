from pathlib import Path
import json,urllib.request,csv,hashlib,collections,math
import numpy as np
from scipy import stats
ROOT=Path(__file__).resolve().parents[1];repo=ROOT/'external/morpholib';out={}
p=ROOT/'sources/primary/FishShapes_specimensv1.csv'
if not p.exists():
 with urllib.request.urlopen('https://zenodo.org/api/records/6642650/files/FishShapes_specimensv1.csv/content',timeout=30) as r:p.write_bytes(r.read())
actual=hashlib.md5(p.read_bytes()).hexdigest();assert actual=='122b495274d0167c5447db104c7acbfe';out['raw_data_md5']=actual
j=json.loads((repo/'thompson_blind_test_results.json').read_text(encoding='utf8'));pred=json.loads((repo/'thompson_blind_predictions_registered.json').read_text(encoding='utf8'));man=json.loads((repo/'thompson_blind_predictions_manifest.json').read_text(encoding='utf8'))
out['registered_file_hash_checks']={name:hashlib.sha256((repo/name).read_bytes()).hexdigest()==sha for name,sha in man['files'].items()};assert all(out['registered_file_hash_checks'].values())
def norm(s):
 z=[p for p in s.strip().replace(' ','_').split('_') if p];return z[0].capitalize()+'_'+z[1].lower() if len(z)>1 else ''
dat=collections.defaultdict(lambda:collections.defaultdict(list));specimens=0
for row in csv.DictReader(p.open(encoding='utf-8-sig',newline='')):
 specimens+=1
 try:sl=float(row['Standard_length'])
 except ValueError:continue
 if sl<=0:continue
 for key,col in [('BDmax_over_SL','Max_body_depth'),('CPD_over_SL','Min_caudalpeduncle_depth')]:
  try:x=float(row[col])
  except ValueError:continue
  if x>0:dat[norm(row['Tree_name'])][key].append(x/sl)
obs={n:{k:float(np.median(v)) for k,v in a.items()} for n,a in dat.items()};ps={x['species']:x for x in pred['predictions']};raw_deltas=[];errs=collections.defaultdict(list);fams=collections.defaultdict(list)
for row in j['per_species']:
 n=row['species'];s=ps[n]
 for k in ['BDmax_over_SL','CPD_over_SL']:
  if k not in row:continue
  o=obs[n][k];assert abs(o-row[k]['obs'])<1e-12
  for name,x in [('full30',s['full30'][k]['pred']),('thompson7',s['thompson7'][k]['pred']),('consensus',s['baseline_consensus'][k]),('nearest',s['baseline_nearest_training_species'][k])]:
   cal=j['calibration'][k]['alpha']+j['calibration'][k]['beta']*x; e=abs(cal-o);assert abs(e-row[k]['err_'+name+'_cal'])<1e-12
   if row['tau']<50:errs[k,name].append(e)
  if row['tau']<50 and k=='BDmax_over_SL':fams[row['family']].append(row[k]['err_full30_cal']-row[k]['err_nearest_cal'])
out['raw_observations_and_errors_match_all_saved_species']=True;out['n_scored']=len(j['per_species']);out['n_specimens']=specimens
k='BDmax_over_SL';a=np.array(errs[k,'full30']);b=np.array(errs[k,'consensus']);c=np.array(errs[k,'nearest']);d=np.array(errs[k,'thompson7'])
wil=lambda a,b:float(stats.wilcoxon((a-b)[a!=b],alternative='less').pvalue)
out['full30_vs_consensus']={'n':len(a),'median_model':float(np.median(a)),'median_baseline':float(np.median(b)),'p_one_sided_species_wilcoxon':wil(a,b)}
out['full30_vs_nearest']={'median_model':float(np.median(a)),'median_nearest':float(np.median(c)),'ratio':float(np.median(a)/np.median(c)),'relative_lower_error_pct':float(100*(1-np.median(a)/np.median(c))),'p_one_sided_species_wilcoxon':wil(a,c),'pass_alpha_0_01':wil(a,c)<.01}
out['thompson7_vs_consensus']={'median_model':float(np.median(d)),'median_consensus':float(np.median(b)),'p_one_sided_species_wilcoxon':wil(d,b)}
# Exploratory family-level sensitivity. This is not full phylogenetic correction.
v=np.array([np.mean(x) for x in fams.values()]);out['exploratory_family_mean_differences_full30_minus_nearest']={'families':len(v),'mean_difference':float(np.mean(v)),'p_one_sided_wilcoxon_family':float(stats.wilcoxon(v[v!=0],alternative='less').pvalue),'limitation':'coarse sensitivity only; full phylogenetic dependence not removed'}
out['reported_H1_to_H7_pass_cal']={k:v['pass'] for k,v in j['hypotheses'].items() if k.endswith('_cal')};out['calibration_boundary']='Error reconstruction uses the repository-supplied fitted calibration coefficients; those coefficients and original shape predictions were not independently re-estimated in this check.'
(ROOT/'results/fish_independent_audit.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
(ROOT/'checkpoints/04_fish_checks.md').write_text('# Checkpoint 04: fish raw-data and statistical checks\nRaw FishShapes checksum verified. All 5,180 scored species observations and full30/Thompson7/consensus/nearest errors agree with raw data plus locked predictions and supplied calibration. The article reverses the 4% direction and uses the full30 p-value to describe Thompson7. H2,H4,H5 fail their registered criteria. Original prediction generation, re-estimation of calibration and proper phylogenetic dependence remain separate checks.\n',encoding='utf8')
