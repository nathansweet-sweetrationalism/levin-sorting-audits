from pathlib import Path
import json,urllib.request,urllib.parse,concurrent.futures,hashlib
ROOT=Path(__file__).resolve().parents[1]
def get(url,p):
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'RCF-audit/1.0'}),timeout=25) as f:b=f.read()
  p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);return {'url':url,'path':str(p.relative_to(ROOT)),'status':200,'sha256':hashlib.sha256(b).hexdigest()}
 except Exception as e:return {'url':url,'path':str(p),'status':'unavailable','error':str(e)}
tree=json.loads((ROOT/'sources/morpholib_tree.json').read_text(encoding='utf8'))['tree'];paths=[]
for x in tree:
 p=x['path']
 if x['type']!='blob':continue
 if p in ['thompson_blind_predictions_registered.json','thompson_blind_test_results.json','models/2021-Cervera–Levin–Mafe.py','docs/CAUSAL_EMERGENCE_PRACTITIONERS_GUIDE.md','docs/THOMPSON_BLIND_TEST_RESULTS.md','docs/THOMPSON_BLIND_PREREGISTRATION.md'] or (p.startswith('datasets/') and any(z in p for z in ['xenopus_craniofacial','xenobot_evolutionary','bioelectric_morphogen','planarian_hk','causal_emergence']) and Path(p).suffix in ['.json','.csv','.bib','.md','.jpg']) or (p.startswith('nanopubs/') and any(z in p for z in ['blind','fishshape','sorting','thompson-prereg'])):paths.append(p)
tasks=[('https://raw.githubusercontent.com/fractastical/morpholib/35d30f4cfd5397ee1ed769f96494e018603e293d/'+urllib.parse.quote(p),Path('external/morpholib')/p) for p in paths]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:rr=list(ex.map(lambda z:get(*z),tasks))
(ROOT/'sources/additional_repository_downloads.json').write_text(json.dumps(rr,indent=2),encoding='utf8');print('additional sources',len(rr),'success',sum(r['status']==200 for r in rr))
for u,p in [('https://zenodo.org/api/records/6642650','sources/fishshapes_zenodo.json'),('https://api.github.com/repos/leanprover/lean4/releases/latest','sources/lean_release.json')]:
 r=get(u,Path(p));print(r)
 if r['status']==200:
  j=json.loads((ROOT/p).read_text(encoding='utf8'))
  if 'assets' in j:print('lean assets',[(x['name'],x['size'],x['browser_download_url']) for x in j['assets'] if 'windows' in x['name']])
  if 'files' in j:print('Fish files',[(x['key'],x['size'],x['links']) for x in j['files']])
