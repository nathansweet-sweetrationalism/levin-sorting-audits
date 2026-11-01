from pathlib import Path
import urllib.request,json,hashlib,zipfile,time
ROOT=Path(__file__).resolve().parents[1];meta=json.loads((ROOT/'sources/lean_release.json').read_text(encoding='utf8'));a=next(a for a in meta['assets'] if a['name'].endswith('windows.zip'));p=ROOT/'tools'/a['name'];p.parent.mkdir(exist_ok=True)
if not p.exists():
 with urllib.request.urlopen(a['browser_download_url'],timeout=35) as r,p.open('wb') as o:
  while b:=r.read(8*1024*1024):o.write(b)
h=hashlib.sha256(p.read_bytes()).hexdigest();digest=a.get('digest');assert not digest or digest=='sha256:'+h
with zipfile.ZipFile(p) as z:
 for m in z.infolist():
  rel=Path(m.filename)
  if rel.is_absolute() or '..' in rel.parts:raise ValueError('Unsafe archive path')
  if '/lib/lean/' in m.filename or '/bin/' in m.filename:z.extract(m,ROOT/'tools')
(ROOT/'results/lean_toolchain.json').write_text(json.dumps({'tag':meta['tag_name'],'url':a['browser_download_url'],'sha256':h,'official_digest':digest},indent=2),encoding='utf8');print('lean toolchain downloaded, verified, extracted',flush=True)
