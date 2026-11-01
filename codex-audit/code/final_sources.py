from pathlib import Path
import json,urllib.request,concurrent.futures,hashlib
ROOT=Path(__file__).resolve().parents[1]
tasks={
 'symposium.html':'https://thoughtforms.life/symposium-on-the-platonic-space/',
 'sweet_original.html':'https://sweetrationalism.com/articles/biology/why-michael-levins-bubble-sort-revelation-is-misunderstood-1960s-algorithm-theory-meets-god-of-the-gaps-argument-original-text/',
 'film_clips.html':'https://unlockingthemysteryoflife.film/clips/',
 'discovery_2004.html':'https://www.discovery.org/a/2116/',
 'durant_2017.pdf':'https://chrisfieldsresearch.com/bioelectric-epigenetics-BJ-2017.pdf',
 'morpholib_LICENSE':'https://raw.githubusercontent.com/fractastical/morpholib/35d30f4cfd5397ee1ed769f96494e018603e293d/LICENSE',
 'planarian_oviedo.html':'https://pmc.ncbi.nlm.nih.gov/articles/PMC2823934/',
 'planarian_beane.html':'https://pmc.ncbi.nlm.nih.gov/articles/PMC3278711/',
 'tadpole_vandenberg.html':'https://pmc.ncbi.nlm.nih.gov/articles/PMC3428595/',
 'tadpole_pinet.pdf':'https://journals.biologists.com/dev/article-pdf/146/14/dev175893/1738124/dev175893.pdf',
 'causal_hoel2013.html':'https://pmc.ncbi.nlm.nih.gov/articles/PMC3856819/',
}
def one(kv):
 name,url=kv;rec={'url':url,'path':'sources/primary/'+name}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'RCF-audit/1.0'}),timeout=25) as r:b=r.read();rec.update(status=r.status,final_url=r.url)
  (ROOT/rec['path']).write_bytes(b);rec['sha256']=hashlib.sha256(b).hexdigest()
 except Exception as e:rec.update(status='unavailable',error=str(e))
 return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rr=list(ex.map(one,tasks.items()))
(ROOT/'sources/final_primary_downloads.json').write_text(json.dumps(rr,indent=2),encoding='utf8')
for r in rr:print(r['path'],r['status'])
