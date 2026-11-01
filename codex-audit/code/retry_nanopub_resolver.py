from pathlib import Path
import json,urllib.request,concurrent.futures,hashlib
ROOT=Path(__file__).resolve().parents[1];records=json.loads((ROOT/'results/nanopub_identifier_checks.json').read_text(encoding='utf8'))
u='https://raw.githubusercontent.com/fractastical/morpholib/35d30f4cfd5397ee1ed769f96494e018603e293d/nanopubs/thompson_predictions/published_manifest_prod.txt'
with urllib.request.urlopen(u,timeout=25) as r:b=r.read()
(ROOT/'sources/primary/nanopub_published_manifest_prod.txt').write_bytes(b);print(b.decode()[-3500:])
def one(rec):
 ident=rec['artifact_code'];url='https://w3id.org/np/'+ident
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'Accept':'application/trig','User-Agent':'RCF-audit/1.0'}),timeout=25) as f:b=f.read();last=f.url;ct=f.headers.get('Content-Type')
  p=ROOT/'sources/nanopub_registry'/f'{ident}.trig';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);rec['resolver_retry']={'url':url,'status':200,'final_url':last,'content_type':ct,'sha256':hashlib.sha256(b).hexdigest(),'contains_artifact_code':ident.encode() in b}
 except Exception as e:rec['resolver_retry']={'url':url,'status':'unavailable','error':str(e)}
 return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:out=list(ex.map(one,records))
(ROOT/'results/nanopub_identifier_checks.json').write_text(json.dumps(out,indent=2),encoding='utf8');print([(x['artifact_code'],x['resolver_retry']) for x in out])
