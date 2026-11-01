"""Bounded additional source retrieval; exact URLs and response hashes retained."""
from pathlib import Path
import urllib.request,hashlib,json,concurrent.futures,re,html
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
targets={
 'wing_specimens.tab':'https://doi.pangaea.de/10.1594/PANGAEA.937635?format=textfile',
 'wing_landmarks.tab':'https://doi.pangaea.de/10.1594/PANGAEA.937651?format=textfile',
 'aristotle_de_anima2.html':'https://psychclassics.yorku.ca/Aristotle/De-anima/de-anima2.htm',
 'thompson1913_ocr.txt':'https://archive.org/download/onaristotleasbio00thomrich/onaristotleasbio00thomrich_djvu.txt',
 'plato_letter7.html':'https://classics.mit.edu/Plato/seventh_letter.html',
}
def get(kv):
 name,url=kv;p=ROOT/'sources/primary'/name
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ScholarlySourceAudit/1.0'}),timeout=40) as r:
   b=r.read();final=r.url;p.write_bytes(b)
  return {'url':url,'status':200,'final_url':final,'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 except Exception as e:return {'url':url,'status':'access_failed','error':str(e)}
out=list(concurrent.futures.ThreadPoolExecutor(max_workers=5).map(get,targets.items()))
(ROOT/'results/supplement_access.json').write_text(json.dumps(out,indent=2),encoding='utf8')
class P(HTMLParser):
 def __init__(self):super().__init__();self.a=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,s):
  if not self.skip:self.a.append(s)
for n in ['sweet_pipette','aristotle_de_anima2','plato_letter7']:
 p=ROOT/'sources/primary'/f'{n}.html'
 if p.exists():
  a=P();a.feed(p.read_text(encoding='utf8',errors='replace'));p.with_suffix('.plain.txt').write_text(' '.join(a.a),encoding='utf8')
print(json.dumps(out,indent=2))
