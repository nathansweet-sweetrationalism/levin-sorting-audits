"""Validate the audit's provenance links and key consistency checks, offline.

This is not a scientific-truth classifier. Successful validation includes correctly
preserved negative results and known upstream execution failures.
"""
from pathlib import Path
from fractions import Fraction
import json,hashlib,math,sys,collections,csv
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf8'))
def check(name,condition,detail=None):
 checks.append({'check':name,'pass':bool(condition),'detail':detail})
def rel(p):return ROOT/str(p).replace('\\','/')
def close(a,b):return math.isclose(float(a),float(b),rel_tol=1e-11,abs_tol=1e-13)

data=read('results/claims.json');schema=read('results/claims.schema.json')
errs=list(Draft202012Validator(schema).iter_errors(data));check('claim_schema',not errs,[e.message for e in errs])
ids=[c['id'] for c in data['claims']];check('unique_claim_ids',len(ids)==len(set(ids)),len(ids))
missing=[(c['id'],e['path']) for c in data['claims'] for e in c['evidence'] if not rel(e['path']).is_file()];check('all_claim_evidence_files_exist',not missing,missing)
badloc=[]
for c in data['claims']:
 for x in c['target_locations']:
  lines=rel(x['path']).read_text(encoding='utf8').splitlines()
  if not (0<x['line']<=len(lines) and x['search_text'].casefold() in lines[x['line']-1].casefold()):badloc.append([c['id'],x])
check('input_line_locators',not badloc,badloc)
rows=list(csv.DictReader((ROOT/'results/claims.csv').open(encoding='utf-8-sig',newline='')));check('csv_json_claim_parity',[r['id'] for r in rows]==ids and [r['status'] for r in rows]==[r['status'] for r in data['claims']])
input_hashes=read('results/input_hashes.json');check('frozen_input_hashes',all(hashlib.sha256((ROOT/'inputs'/f'{name}.txt').read_bytes()).hexdigest()==sha for name,sha in input_hashes.items()))

git_checks={}
for folder,treefile in [('morpholib','sources/morpholib_tree.json'),('cell_research','sources/primary/upstream_tree.json')]:
 tree=read(treefile);index={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'};count=0;bad=[];unindexed=[];base=ROOT/'external'/folder
 for p in base.rglob('*'):
  if not p.is_file() or '__pycache__' in p.parts:continue
  k=p.relative_to(base).as_posix()
  if k not in index:unindexed.append(k);continue
  b=p.read_bytes();sha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();count+=1
  if sha!=index[k]:bad.append(k)
 git_checks[folder]={'blob_files_checked':count,'mismatches':bad,'unindexed_files':unindexed,'tree_truncated':tree.get('truncated')}
 check(folder+'_git_blob_bytes_match',not bad and count>0,git_checks[folder])
(ROOT/'results/source_integrity_checks.json').write_text(json.dumps(git_checks,indent=2),encoding='utf8')

m=read('results/independent_math.json');check('finite_size_baseline',Fraction(m['balanced_N80'])==Fraction(39,80) and m['balanced_N80_float']==.4875)
check('adjacent_error_counterexample',m['rulers']['I']==[3,2] and m['rulers']['E']==[1,2])
check('nonlocal_equality_counterexample',m['nonlocal_counterexample']['delta_I']==-3)
runs=read('results/historical_replay_runs.json');summary=read('results/historical_replay_summary.json');check('historical_run_count',len(runs)==105)
bad=[]
for r in runs:
 a=r['final_cells'];h=sum(x['algotype']==y['algotype'] for x,y in zip(a,a[1:]));v=[x['value'] for x in a]
 if h!=r['final_H'] or not close(h/80,r['final_A']) or v!=sorted(v) or r['continued_swaps']!=0:bad.append([r['C'],r['run']])
check('saved_endpoint_records_and_persistence',not bad,bad)
check('historical_group_means',all(close(sum(x['final_A'] for x in runs if x['C']==r['C'])/15,r['mean_A']) for r in summary['summary']))
counts={int(k):int(v) for k,v in read('results/C2_conditional_distribution.json').items()};den=sum(counts.values());mean=Fraction(sum(k*v for k,v in counts.items()),den);obs=sum(x['final_H'] for x in runs if x['C']==2);tail=Fraction(sum(v for k,v in counts.items() if abs(k-mean)>=abs(obs-mean)),den)
check('exact_conditional_tail_from_integer_distribution',mean==Fraction(1207,2) and obs==572 and str(tail)==summary['C2_exact_conditional_test']['tail_probability_fraction'])
fresh=read('results/fresh_robustness.json')['runs'];check('fresh_sensitivity_120_runs',len(fresh)==120 and all(x['final_error']==0 and not x['step_cap_hit'] for x in fresh))
f=read('results/fish_independent_audit.json');g=f['full30_vs_nearest'];ratio=g['median_model']/g['median_nearest'];check('fish_direction_and_test_distinguished',close(ratio,g['ratio']) and ratio<1 and g['p_one_sided_species_wilcoxon']>.01 and not g['pass_alpha_0_01'])
check('all_fish_observations_and_locks',f['n_scored']==5180 and f['n_specimens']==16523 and f['raw_observations_and_errors_match_all_saved_species'] and all(f['registered_file_hash_checks'].values()))
check('fish_full_registered_decisions',f['reported_H1_to_H7_pass_cal']=={f'H{i}_cal':v for i,v in enumerate([True,False,True,False,False,True,True],1)})
w=read('results/wing_checks.json');check('wing_scope_and_failed_tests',w['retained_wings']==1027 and w['species']==30 and w['landmarks']==19 and not any(w['W1_to_W7_recorded_pass'].values()) and close(w['perimeter_fraction'],.6582121084811257))
labels=read('results/benchmark_label_audit.json');check('literal_verdicts_not_acceptance_rules',len(labels)==14 and all(x['status_expr']=="'VERIFIED'" for x in labels))
formal=read('results/lean_additional_kernel_checks.json');check('additional_kernel_runs_clean',sum(len(x['declarations']) for x in formal)==85 and all(x['exit_code']==0 and not x['sorryAx_or_error'] for x in formal))
log=(ROOT/'results/lean_kernel_output.txt').read_text(encoding='utf8');check('sorting_axiom_log_has_no_sorry','sorryAx' not in log and 'depends on axioms' in log)
crypto=read('results/nanopub_crypto_checks.json');check('five_crypto_checks_valid',len(crypto)==5 and all(all(x[k] for k in ['trusty_hash_valid','rsa_signature_valid','rdf_structure_valid']) for x in crypto))
negative=read('results/crypto_negative_controls.json');check('crypto_client_negative_control_exposes_false_positive',len(negative)==5 and all(r['checks']['has_valid_trusty']['tampered_record_rejected'] and not r['checks']['has_valid_signature']['tampered_record_rejected'] for r in negative))
direct=read('results/rsa_direct_checks.json');check('direct_rsa_positive_and_negative_controls',len(direct)==5 and all(r['rsa_signature_valid_direct'] and not r['tampered_signature_valid_direct'] for r in direct))
refs=read('results/reference_checks.json');badrefs=[x['doi'] for x in refs if x['verification']=='confirmed_mismatched_reference'];check('four_wrong_doi_pairings_preserved',len(refs)==41 and set(badrefs)=={'10.1093/sysbio/syz029','10.1111/evo.12502','10.1242/dev.175950','10.3389/fphys.2016.00178'})
check('upstream_failure_logs_retained',all(read('results/'+x+'_selftest.json')['exit_code']!=0 for x in ['pietak','tadpole','xenobot']))
crate=read('ro-crate-metadata.json') if (ROOT/'ro-crate-metadata.json').exists() else None
check('crate_minimal_graph_present',crate is not None and any(x.get('@id')=='./' for x in crate.get('@graph',[])))
manifest=ROOT/'SHA256SUMS.txt'
if manifest.exists():
 bad=[];n=0
 for line in manifest.read_text(encoding='utf8').splitlines():
  if not line:continue
  sha,p=line.split('  ',1);n+=1
  if not rel(p).is_file() or hashlib.sha256(rel(p).read_bytes()).hexdigest()!=sha:bad.append(p)
 check('sha256_manifest',not bad,{'files':n,'failures':bad})
else:check('sha256_manifest',False,'Not yet generated')
result={'scope':'Offline schema, provenance-byte and result-consistency validation; not universal scientific validation. RO-Crate graph checked minimally, not independently certified against an entire profile.','checks':checks,'passed':all(x['pass'] for x in checks)}
(ROOT/'results/package_validation.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps({'passed':result['passed'],'checks':len(checks),'claims':len(ids),'failures':[x for x in checks if not x['pass']]},indent=2));sys.exit(0 if result['passed'] else 1)
