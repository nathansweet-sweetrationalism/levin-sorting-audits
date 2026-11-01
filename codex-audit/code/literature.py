from pathlib import Path
import json,urllib.request,urllib.parse,concurrent.futures,hashlib,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
def fetch(url,p):
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'RCF-scholarly-audit/1.0'}),timeout=25) as f:b=f.read();u=f.url;ctype=f.headers.get('Content-Type')
  p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);return {'status':200,'url':url,'final_url':u,'local_path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(b).hexdigest(),'content_type':ctype}
 except Exception as e:return {'status':'unavailable','url':url,'error':str(e)}
meta=json.loads((ROOT/'results/doi_metadata_summary.json').read_text())
correct=['10.1371/journal.pone.0112732','10.1098/rspb.2020.1053','10.1242/dev.175893','10.3389/fbioe.2016.00055','10.1002/reg2.72']
add=['10.1371/journal.pcbi.1001122','10.1371/journal.pcbi.1003285','10.1371/journal.pcbi.1009917','10.1038/sdata.2016.18','10.1111/ecog.02881','10.1098/rsif.2007.0231','10.1093/bib/bbn034','10.3233/DS-2014-0001','10.1038/s41597-022-01732-4']
do=['10.1016/j.biosystems.2021.104511','10.1016/j.chembiol.2010.11.012','10.1016/j.ydbio.2009.12.012','10.1002/dvdy.23770','10.1073/pnas.2112672118','10.1073/pnas.1910837117','10.1098/rsif.2017.0425','10.1073/pnas.1314922110','10.1016/j.patter.2025.101472']+correct+add
results=[]
def work(d):
 h=hashlib.sha256(d.encode()).hexdigest()[:16];p=ROOT/'sources/europepmc'/f'{h}.json';u='https://www.ebi.ac.uk/europepmc/webservices/rest/search?query='+urllib.parse.quote('DOI:'+d)+'&format=json&resultType=core';r=fetch(u,p);r['doi']=d
 if r['status']==200:
  z=json.loads(p.read_text()).get('resultList',{}).get('result',[])
  r['records']=len(z)
  if z:
   r['title']=z[0].get('title');r['pmcid']=z[0].get('pmcid');r['retracted']=z[0].get('isRetracted');r['open_access']=z[0].get('isOpenAccess')
   if r['pmcid']:
    pp=ROOT/'sources/europepmc'/f"{r['pmcid']}.xml";r['fulltext']=fetch('https://www.ebi.ac.uk/europepmc/webservices/rest/'+r['pmcid']+'/fullTextXML',pp)
    if r['fulltext']['status']==200:
     doc=ET.parse(pp).getroot(); txt='\n'.join(''.join(e.itertext()) for e in doc.iter() if e.tag in ['article-title','title','p','label','caption','table-wrap','disp-formula']);pp.with_suffix('.txt').write_text(txt,encoding='utf8')
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(work,do))
(ROOT/'results/primary_literature_access.json').write_text(json.dumps(results,indent=2),encoding='utf8')
for x in results:print(x['doi'],x.get('title'),x.get('pmcid'),x.get('fulltext',{}).get('status'),flush=True)
# Corrected and methodology DOI metadata, separate from the input DOI audit.
extra=[]
for d in correct+add:
 p=ROOT/'sources/additional_metadata'/(hashlib.sha256(d.encode()).hexdigest()[:16]+'.json');r=fetch('https://api.crossref.org/works/'+d,p);r['doi']=d;extra.append(r)
(ROOT/'sources/additional_metadata_downloads.json').write_text(json.dumps(extra,indent=2),encoding='utf8')
# Official publisher PDF listed by Crossref, plus MDPI's official asset server.
mdpi=fetch('https://mdpi-res.com/d_attachment/philosophies/philosophies-11-00161/article_deploy/philosophies-11-00161.pdf',ROOT/'sources/primary/ingressing.pdf')
(ROOT/'sources/mdpi_download.json').write_text(json.dumps(mdpi,indent=2),encoding='utf8');print('ingressing',mdpi['status'])
