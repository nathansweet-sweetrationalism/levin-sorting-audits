from pathlib import Path
import urllib.request,json,hashlib,concurrent.futures
ROOT=Path(__file__).resolve().parents[1]
ids=['RAH6FDLaacsq28cjx2NVRYRANqOThwHaHwE58ByxqIWI8','RA_mMJXveSMNlxIjYu_oTtIY233QfJnNCf47yRLfInMuE','RAdFmYq_oVoHbK2eclzYgRWXJVhSNdiEQBfxp4nhvkzJk','RAilN4nbRHp3e3ZHqlbIgeL3UGPRV_KtQHtJD3gzVVdqw','RAJancwGOPEkHzBoZXGv_vu_snW0Lff2FktE85Me1P-fI']
def fetch(ident):
 url='https://np.knowledgepixels.com/'+ident;rec={'artifact_code':ident,'url':url}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'Accept':'application/trig','User-Agent':'RCF-audit/1.0'}),timeout=25) as f:b=f.read();rec.update(status=r.status if False else f.status,final_url=f.url,content_type=f.headers.get('Content-Type'))
  p=ROOT/'sources/nanopub_registry'/f'{ident}.trig';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);rec.update(local_path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(b).hexdigest(),contains_artifact_code=ident.encode() in b)
 except Exception as e:rec.update(status='unavailable',error=str(e))
 rec.update(cryptographic_trusty_hash_validated=False,signature_validated=False,interpretation='Retrieval and syntactic RDF checks do not verify the standardized trusty hash or RSA signature, author identity, timestamp, blinding or scientific truth.')
 return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:r=list(ex.map(fetch,ids))
(ROOT/'results/nanopub_identifier_checks.json').write_text(json.dumps(r,indent=2),encoding='utf8');print(json.dumps(r,indent=2))
