from pathlib import Path
import urllib.request,urllib.parse,json,re,hashlib,concurrent.futures
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
class Plain(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.links=[];self.href=None;self.label=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ['script','style']:self.skip+=1
  if tag=='a':self.href=dict(attrs).get('href');self.label=[]
 def handle_endtag(self,tag):
  if tag in ['script','style']:self.skip=max(0,self.skip-1)
  if tag=='a' and self.href:self.links.append({'text':' '.join(self.label),'url':self.href});self.href=None
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
  if self.href:self.label.append(d)
def fetch(u,name):
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'RCF-audit/1.0'}),timeout=25) as f:b=f.read();ct=f.headers.get('Content-Type','');url=f.url
  p=ROOT/'sources/primary'/name;p.write_bytes(b);r={'url':u,'final_url':url,'path':str(p.relative_to(ROOT)),'status':200,'sha256':hashlib.sha256(b).hexdigest()}
  if 'html' in ct or name.endswith('.html'):
   z=Plain();z.feed(b.decode('utf8',errors='replace'));p.with_suffix('.text.txt').write_text(' '.join(z.parts),encoding='utf8');p.with_suffix('.links.json').write_text(json.dumps(z.links,indent=2),encoding='utf8')
  return r
 except Exception as e:return {'url':u,'status':'unavailable','error':str(e)}
cor=json.loads((ROOT/'sources/primary/sweet_corpus.json').read_text(encoding='utf8'));u=next(x['url'] for x in cor['items'] if 'bubble' in x.get('title','').lower())
tasks=[(u,'sweet_live.html'),('https://calteches.library.caltech.edu/51/02/CargoCult.htm','feynman.html'),('https://arxiv.org/abs/2005.08363','compiler_brown.html'),('https://arxiv.org/abs/1711.03050','compiler_fluckiger.html'),('https://arxiv.org/abs/1802.09845','compiler_georgiou.html'),('https://arxiv.org/pdf/2405.07987','platonic_representation.pdf'),('https://arxiv.org/pdf/2510.22954','hivemind.pdf'),('https://x.com/drmichaellevin/status/2114794440896487530','levin_post.html'),('https://teapaw.org/drmichaellevin/status/2114794440896487530','levin_post_mirror.html'),('https://www.gutenberg.org/ebooks/55264','thompson1917_catalog.html'),('https://plato.stanford.edu/entries/scientific-reduction/','sep_reduction.html'),('https://plato.stanford.edu/entries/reduction-biology/','sep_biology.html')]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rr=list(ex.map(lambda z:fetch(*z),tasks))
(ROOT/'sources/quote_source_downloads.json').write_text(json.dumps(rr,indent=2),encoding='utf8')
for x in rr:print(x['url'],x['status'],flush=True)
for k in ['compiler_brown','compiler_fluckiger','compiler_georgiou']:
 p=ROOT/'sources/primary'/f'{k}.html'
 if p.exists():
  s=p.read_text(encoding='utf8');print(k,re.findall(r'<title>(.*?)</title>',s,re.S))
