from collect import *
import time
# Explicit primary URLs and code versions. Downloads are read-only; no upstream code is executed here.
tasks={
 'sorting_arxiv.pdf':'https://arxiv.org/pdf/2401.05375',
 'ingressing.pdf':'https://www.mdpi.com/2409-9287/11/5/161/pdf',
 'lex_transcript.html':'https://lexfridman.com/michael-levin-2-transcript/',
 'sweet_corpus.json':'https://sweetrationalism.com/ai-corpus.json/',
 'dietz_methods.pdf':'https://fractastical.github.io/morpholib/levin_latent_space_methods_and_provenance.pdf',
 'dietz_sorting.pdf':'https://fractastical.github.io/morpholib/zhang_levin_sorting_morphogenesis_manuscript.pdf',
 'dietz_fish.pdf':'https://fractastical.github.io/morpholib/thompson_1917_fish_transformations_manuscript.pdf',
 'upstream_commit.json':'https://api.github.com/repos/Zhangtaining/cell_research/commits/1fd2bd5921c1f6b423a71f691d5189106a8a1020',
 'lean_sorting.lean':'https://raw.githubusercontent.com/fractastical/morpholib/35d30f4cfd5397ee1ed769f96494e018603e293d/morphoeval/lean/loops/Loop_zhang_sorting_morphogenesis.lean',
 'old_model.py':'https://raw.githubusercontent.com/fractastical/morpholib/bfe377c2f9d5bfc35e0083df1c04eb9fe6ca739e/sorting-morphogenesis/sorting_morphogenesis.py',
 'old_ablation.py':'https://raw.githubusercontent.com/fractastical/morpholib/bfe377c2f9d5bfc35e0083df1c04eb9fe6ca739e/sorting-morphogenesis/audit_platonic_space_claims.py',
 'old_metrics.json':'https://raw.githubusercontent.com/fractastical/morpholib/bfe377c2f9d5bfc35e0083df1c04eb9fe6ca739e/sorting-morphogenesis/figures/platonic_claims_ablation_metrics.json',
 'old_commit.json':'https://api.github.com/repos/fractastical/morpholib/commits/bfe377c2f9d5bfc35e0083df1c04eb9fe6ca739e',
 'upstream_tree.json':'https://api.github.com/repos/Zhangtaining/cell_research/git/trees/1fd2bd5921c1f6b423a71f691d5189106a8a1020?recursive=1',
 'port_js.mjs':'https://raw.githubusercontent.com/fractastical/morpholib/35d30f4cfd5397ee1ed769f96494e018603e293d/sorting-morphogenesis/js/zhang_sorting_morphogenesis.mjs',
}
for fn in ['BubbleSortCell.py','InsertionSortCell.py','SelectionSortCell.py','MultiThreadCell.py']:
 tasks['upstream_'+fn]='https://raw.githubusercontent.com/Zhangtaining/cell_research/1fd2bd5921c1f6b423a71f691d5189106a8a1020/modules/multithread/'+fn
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: recs=list(ex.map(lambda kv:get(kv[1],Path('sources/primary')/kv[0]),tasks.items()))
dump('sources/primary_downloads.json',recs)
print('\n'.join(str((Path(x['local_path']).name,x['status'],x.get('bytes'),x.get('error',''))) for x in recs),flush=True)
# Retry rate-limited registry requests sequentially with explicit backoff; do not turn unavailable into invalid.
old=json.loads((ROOT/'results/doi_resolution.json').read_text())
for rec in old:
 if rec['status']==200:continue
 d=rec['doi'];url='https://api.crossref.org/works/'+urllib.parse.quote(d,safe='/()')
 rr=get(url,Path(rec['local_path']));rr.update(doi=d,provider='crossref-retry');
 if rr['status']!=200:
  rr=get('https://doi.org/'+d,Path('sources/doi_landing')/(hashlib.sha256(d.encode()).hexdigest()[:16]+'.html'));rr.update(doi=d,provider='doi-resolution-fallback')
 rec['retry']=rr
 print(d,rr['status'],flush=True);time.sleep(0.9)
dump('results/doi_resolution.json',old)
