from pathlib import Path
import re,json,hashlib,datetime,urllib.request,urllib.error,concurrent.futures,sys
ROOT=Path(__file__).resolve().parents[1]
UA={'User-Agent':'RCF-ScholarlyAudit/1.0 (source verification; local reproducibility)'}
def dump(p,x):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False),encoding='utf8')
def get(url,dest):
 rec={'url':url,'accessed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'local_path':str(dest)}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=22) as r:
   b=r.read();rec.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  p=ROOT/dest;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 except Exception as e:rec.update(status='unavailable',error=str(e))
 return rec
texts={p.stem:p.read_text(encoding='utf-8-sig') for p in (ROOT/'inputs').glob('*.txt')}
refs=[];quotes=[];urls=set();dois=set()
for name,t in texts.items():
 for no,line in enumerate(t.splitlines(),1):
  ds=re.findall(r'10\.\d{4,9}/[^\s<>·]+',line)
  us=re.findall(r'https?://[^\s<>]+',line)
  for d in ds:
   d=d.rstrip('.,;:)”’');dois.add(d);refs.append({'article':name,'line':no,'doi':d,'context':line})
  for u in us:urls.add(u.rstrip('.,;:)”’'))
  for q in re.findall(r'“([^”]+)”',line):quotes.append({'article':name,'line':no,'quote':q,'context':line,'status':'not_yet_adjudicated'})
dump('results/doi_occurrences.json',refs);dump('results/quote_inventory.json',quotes);dump('results/url_inventory.json',sorted(urls));dump('results/input_hashes.json',{k:hashlib.sha256((ROOT/'inputs'/f'{k}.txt').read_bytes()).hexdigest() for k in texts})
tree=json.loads((ROOT/'sources/morpholib_tree.json').read_text())['tree']
selected=[]
for x in tree:
 p=x['path']
 if x['type']!='blob' or '/.lake/' in p:continue
 if (p.startswith('sorting-morphogenesis/') and Path(p).suffix in ('.py','.json','.md','.cpp','.js','.mjs','.lean','.toml','.txt','.csv')) or (p.startswith('morphoeval/lean/') and Path(p).suffix in ('.lean','.json','.toml','')) or (p.startswith('models/') and Path(p).suffix=='.py' and any(s in p for s in ['Cervera','pietak','bischof','kriegman'])) or (p.startswith('thompson/') and Path(p).suffix=='.py') or (p.startswith('thompson_') and Path(p).suffix in ('.json','.csv')) or p in ['AGENTS.md','requirements.lock.txt','requirements.txt','docs/ERRATA_AND_REFEREE_AUDIT_LOG.md','docs/CAUSAL_EMERGENCE_PRACTITIONERS_GUIDE.md','docs/THOMPSON_METHODS_AND_PROVENANCE.md','docs/KEY_DISCOVERIES.md','docs/LEV IN_LATENT_SPACE_METHODS_AND_PROVENANCE.md'.replace('LEV IN','LEVIN')]:
  if x.get('size',0)<4000000:selected.append(p)
dump('sources/selected_repository_files.json',selected)
print('inventory',len(dois),'DOIs',len(urls),'URLs',len(quotes),'quote candidates;',len(selected),'source files',flush=True)
mode=(sys.argv[1] if len(sys.argv)>1 else 'all') if __name__=='__main__' else 'inventory'
if mode in ('all','repo'):
 tasks=[('https://raw.githubusercontent.com/fractastical/morpholib/35d30f4cfd5397ee1ed769f96494e018603e293d/'+urllib.parse.quote(p),Path('external/morpholib')/p) for p in selected]
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex: recs=list(ex.map(lambda a:get(*a),tasks))
 dump('sources/repository_downloads.json',recs);print('repository',len(recs),'success',sum(r['status']==200 for r in recs),flush=True)
if mode in ('all','refs'):
 tasks=[]
 for d in sorted(dois):
  provider='datacite' if d.startswith(('10.5281/','10.31234/')) else 'crossref'
  u=('https://api.datacite.org/dois/' if provider=='datacite' else 'https://api.crossref.org/works/')+urllib.parse.quote(d,safe='')
  tasks.append((u,Path('sources/metadata')/(hashlib.sha256(d.encode()).hexdigest()[:16]+'.json'),d,provider))
 def meta(a):
  r=get(a[0],a[1]);r.update(doi=a[2],provider=a[3]);return r
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex: recs=list(ex.map(meta,tasks))
 dump('results/doi_resolution.json',recs);print('DOI registry records',sum(r['status']==200 for r in recs),'/',len(recs),flush=True)
if mode in ('all','urls'):
 tasks=[(u,Path('sources/urls')/(hashlib.sha256(u.encode()).hexdigest()[:16]+'.bin')) for u in sorted(urls)]
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex: recs=list(ex.map(lambda a:get(*a),tasks))
 dump('results/url_resolution.json',recs);print('URL responses',sum(r['status']==200 for r in recs),'/',len(recs),flush=True)

