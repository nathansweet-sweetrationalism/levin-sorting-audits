from pathlib import Path
import json,re,time,urllib.request,hashlib,concurrent.futures
ROOT=Path(__file__).resolve().parents[1]
def fetch(u,p):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True)
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'RCF-audit/1.0'}),timeout=25) as f:b=f.read();last=f.url
  p.write_bytes(b);return {'url':u,'path':str(p.relative_to(ROOT)),'status':200,'final_url':last,'sha256':hashlib.sha256(b).hexdigest()}
 except Exception as e:return {'url':u,'path':str(p.relative_to(ROOT)),'status':'unavailable','error':str(e)}
# Keep a complete compact table of canonical DOI metadata and source-text citation contexts.
a=json.loads((ROOT/'results/doi_resolution.json').read_text());out=[]
for x in a:
 r=x.get('retry',x) if x['status']!=200 else x
 p=ROOT/r['local_path']; rec={'doi':x['doi'],'status':r['status'],'provider':r['provider']}
 try:
  j=json.loads(p.read_text()); m=j.get('message',j.get('data',{}).get('attributes',{}))
  rec.update(title=m.get('title',m.get('titles')),authors=m.get('author',m.get('creators')),container=m.get('container-title'),volume=m.get('volume'),issue=m.get('issue'),page=m.get('page'),published=m.get('published',m.get('publicationYear')),type=m.get('type',m.get('types')),update_to=m.get('update-to'),url=m.get('URL',m.get('url')),links=m.get('link'),license=m.get('license'))
 except Exception as e:rec.update(parse_error=str(e))
 out.append(rec)
(ROOT/'results/doi_metadata_summary.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf8')
for x in out:print(x['doi'],x.get('title'),x.get('published'),x.get('page'),x.get('parse_error',''))
# Fetch all small upstream Python files so callers of update() and configuration can be inspected.
tree=json.loads((ROOT/'sources/primary/upstream_tree.json').read_text())['tree']
tasks=[('https://raw.githubusercontent.com/Zhangtaining/cell_research/1fd2bd5921c1f6b423a71f691d5189106a8a1020/'+x['path'],Path('external/cell_research')/x['path']) for x in tree if x['type']=='blob' and x['path'].endswith('.py')]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: rr=list(ex.map(lambda z:fetch(*z),tasks))
(ROOT/'sources/upstream_downloads.json').write_text(json.dumps(rr,indent=2),encoding='utf8')
# Correctly gated collector import.
p=ROOT/'code/collect.py'; s=p.read_text(encoding='utf-8-sig'); s=s.replace("mode=sys.argv[1] if len(sys.argv)>1 else 'all'","mode=(sys.argv[1] if len(sys.argv)>1 else 'all') if __name__=='__main__' else 'inventory'");p.write_text(s,encoding='utf8')
print('upstream files',len(rr),'success',sum(x['status']==200 for x in rr))
