"""Render local review artifacts and build a SHA-256 evidence manifest.

No publication, messaging, signing, or third-party synchronization is performed.
Run after rebuilding the ledger and before final package validation.
"""
from pathlib import Path
import json,re,html,base64,hashlib,subprocess,sys,urllib.parse,datetime
import markdown
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf8'))
def write(p,t):(ROOT/p).write_text(t,encoding='utf8')
def clean(t):return re.sub(r'\s+',' ',re.sub('<[^>]+>','',str(t))).strip()
def title(v):
 if isinstance(v,list):return title(v[0]) if v else ''
 if isinstance(v,dict):return title(v.get('title',v.get('name','')))
 return clean(v)
def year(v):
 if isinstance(v,dict):return str(v.get('date-parts',[['unknown']])[0][0])
 return str(v or 'unknown')
def authors(v):
 return '; '.join((x.get('family') or x.get('name') or '')+(', '+x['given'] if x.get('given') else '') for x in (v or []))
lit=read('results/recommended_literature.json');refs=read('results/reference_checks.json')
md=['# Source and literature register','','DOI identity and reading status are different checks. This is not a claim that all cited papers were read completely or that no retraction exists. See the full access and rejection logs.','','## Focused methodological reading order','']
bib=[]
for i,r in enumerate(lit,1):
 t=title(r['title']);a=authors(r.get('author'));y=year(r.get('published'));doi=r['doi'];j=title(r.get('container'))
 md.extend([f'{i}. **{a} ({y}). [{t}](https://doi.org/{doi}).** {j}.',f'   Purpose: {r["purpose"]}. Access: {r["reading_scope"]}.',''])
 esc=lambda s: str(s).replace('&',r'\&').replace('%',r'\%').replace('_',r'\_')
 fields={'title':t,'author':' and '.join((x.get('family') or x.get('name') or '')+(', '+x['given'] if x.get('given') else '') for x in (r.get('author') or [])),'year':y,'doi':doi,'url':'https://doi.org/'+doi,'note':r['purpose']}
 if j:fields['journal']=j
 bib.append('@misc{audit_reading_'+str(i)+',\n'+',\n'.join('  '+k+' = {'+esc(v)+'}' for k,v in fields.items())+'\n}')
md.extend(['## Every input DOI identity','','The four erroneous pairings below are retained for correction, not recommended for citation under their original descriptions.','','| DOI | Registered title | Outcome |','|---|---|---|'])
for r in refs:
 v=r['verification'];c=r.get('correction');msg=v.replace('_',' ')
 if c:msg+='; correct DOI: ['+c['correct_doi']+'](https://doi.org/'+c['correct_doi']+')'
 md.append(f"| [{r['doi']}](https://doi.org/{r['doi']}) | {title(r['title']).replace('|','/')} | {msg} |")
md.extend(['','## Non-DOI background identities','','Publisher/author/archive records were checked for the following background references. These identities do not derive the mixed-sort aggregation curve. Full textbook content was not reread.','',
 '- Schelling (1969), *Models of segregation*, AER59(2):488-493: original article copy at [Utrecht University](https://www.uu.nl/sites/default/files/c4_schelling1969_models_segregation.pdf), stable JSTOR1823701.',
 '- Gardner (1970), *Mathematical Games*, Scientific American223(4):120-123: [publisher record](https://www.scientificamerican.com/article/mathematical-games-1970-10/), DOI10.1038/scientificamerican1070-120. Popular exposition, not a peer-reviewed derivation of algotype clustering.',
 '- Knuth (1973), *Sorting and Searching*, TAOCP3: [author publication record](https://cs.stanford.edu/~knuth/vita.pdf).',
 '- Cormen, Leiserson and Rivest (1990), *Introduction to Algorithms*: [first-edition publisher record](https://mitpress.mit.edu/9780262530910/introduction-to-algorithms/). Three authors is correct for that edition.',
 '- Wolfram (2002), *A New Kind of Science*: [publisher facts](https://www.wolframscience.com/media/facts.html). Book, not a journal replication study.',
 '- Brown, Flueckiger and Georgiou preprint identities were checked against arXiv records; the published Flueckiger DOI is in the input DOI table. Their compiler results are not a demonstrated explanation of this logical aggregation metric.',
 '- Aristotle, Thompson and the Seventh Letter: primary passages and translation/authenticity limits are recorded in results/historical_text_checks.json.',
 '- Interview clips, public comments, film-promotion claims and private speech have their own quotation/URL registers; they are not all authenticated merely because the corresponding work exists.',''])
write('REFERENCES.md','\n'.join(md));write('references-recommended.bib','\n\n'.join(bib)+'\n')
write('requirements-audit.lock.txt',subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True,encoding='utf8'))
write('results/pending_mirror_manifest.json',json.dumps({'scope':'Local preservation only. No authenticated ChatGPT Library upload surface was available and no upload is asserted.','status':'pending_destination_and_authenticated_upload','locally_preserved_primary_files':[p.relative_to(ROOT).as_posix() for p in sorted((ROOT/'sources/primary').glob('*.pdf'))],'required_before_any_public_mirror':['Confirm destination and access boundary','Check third-party license and applicable redistribution rights','Upload exact bytes and verify receipt/hash','Retain access/read status and version/supersession links']},indent=2))
claimdata=read('results/claims.json');claims=claimdata['claims'];report=(ROOT/'AUDIT_REPORT.md').read_text(encoding='utf8')
figure=base64.b64encode((ROOT/'results/audit_summary.png').read_bytes()).decode()
body=markdown.markdown(report,extensions=['tables','fenced_code','toc'])
e=html.escape
cards=[]
for c in claims:
 links='; '.join('<a href="'+urllib.parse.quote(x['path'])+'">'+e(x['path'])+'</a>' for x in c['evidence'])
 cards.append('<details class="claim" data-status="'+e(c['status'])+'"><summary><b>'+e(c['id'])+'</b> <span class="tag">'+e(c['status'].replace('_',' '))+'</span> '+e(c['claim'])+'</summary>'+''.join('<p><b>'+label+':</b> '+e(c[k])+'</p>' for label,k in [('Boundary','boundary'),('Check','check'),('Limit','limitations'),('Revision condition','revision_condition')])+'<p><b>Evidence:</b> '+links+'</p></details>')
options=''.join('<option value="'+s+'">'+s.replace('_',' ')+'</option>' for s in sorted({c['status'] for c in claims}))
style='''body{margin:0;background:#f4f6f8;color:#162430;font:17px/1.65 system-ui,sans-serif}main{max-width:1080px;margin:auto;background:white;padding:40px 52px}h1{font-size:2.15em;line-height:1.2}h2{margin-top:2em;line-height:1.3}h3{line-height:1.4}a{color:#075f8d}table{width:100%;border-collapse:collapse;font-size:.88em;display:block;overflow:auto}th,td{border:1px solid #ccd4db;padding:9px 11px;text-align:left;vertical-align:top}th{background:#eaf2f7}code{font-size:.9em;overflow-wrap:anywhere}img{max-width:100%}.note{padding:14px 20px;background:#eaf2f7;border-left:5px solid #1379a1}.claim{border:1px solid #c9d5de;border-radius:5px;padding:12px 16px;margin:12px 0}.claim summary{cursor:pointer}.claim p{font-size:.91em}.tag{display:inline-block;font-size:.76em;background:#eaf2f7;border-radius:4px;padding:1px 5px;margin-right:8px}input,select{font:inherit;padding:7px;margin:5px 8px 10px 0;border:1px solid #9fb0be;border-radius:4px}input{min-width:320px}nav{margin:1em 0}pre{overflow:auto}@media(max-width:700px){main{padding:22px 18px}h1{font-size:1.6em}input{min-width:0;max-width:90%}}@media print{body{background:white}main{padding:0;max-width:none}nav,.controls{display:none}a{color:inherit}details{break-inside:avoid}summary{list-style:none}table{font-size:10pt}}'''
script='''const q=document.querySelector('#query'),s=document.querySelector('#status'),c=[...document.querySelectorAll('.claim')];function filter(){let n=0;c.forEach(x=>{let yes=(!s.value||x.dataset.status===s.value)&&x.textContent.toLowerCase().includes(q.value.toLowerCase());x.hidden=!yes;if(yes)n++});document.querySelector('#count').textContent=n+' claims shown'}q.addEventListener('input',filter);s.addEventListener('change',filter);document.querySelector('#expand').onclick=()=>c.forEach(x=>x.open=!x.hidden);document.querySelector('#collapse').onclick=()=>c.forEach(x=>x.open=false);filter();'''
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dietz, Sweet and Levin: evidence audit</title><style>'+style+'</style><main><nav><a href="#report">Report</a> · <a href="#figure">Summary figure</a> · <a href="#claims">64 material claims</a> · <a href="REFERENCES.md">References</a> · <a href="README.md">Reproduce and resume</a></nav><p class="note">Private research review bundle. November 1, 2026. Verified findings, failed checks and unresolved claims are preserved separately. The package does not certify every sentence or philosophical conclusion.</p><section id="report">'+body+'</section><section id="figure"><h2>Reproduced numerical summaries</h2><img alt="Historical sequential model aggregation and fish prediction error comparison" src="data:image/png;base64,'+figure+'"><p>Historical replay means and the saved within-key randomization expectations; no uncertainty interval is implied by this plot. Fish bars are median absolute errors. See the report for sampling, model and test boundaries.</p></section><section id="claims"><h2>Material claim ledger</h2><p>These are curated audit restatements, not necessarily verbatim quotations. Counts by status are not a truth score. Structural validation is not scientific validation.</p><div class="controls"><input id="query" aria-label="Search claims" placeholder="Search claim, check or limitation"><select id="status" aria-label="Filter outcomes"><option value="">All outcomes</option>'+options+'</select><button id="expand">Expand shown</button> <button id="collapse">Collapse</button><p id="count"></p></div>'+''.join(cards)+'</section></main><script>'+script+'</script></html>'
write('AUDIT_REPORT.html',page)
excluded={'.venv','tools','__pycache__','.pytest_cache'}
def files():return sorted(p for p in ROOT.rglob('*') if p.is_file() and not any(x in excluded for x in p.relative_to(ROOT).parts) and p.name not in ['SHA256SUMS.txt','package_validation.json','ro-crate-metadata.json'])
allfiles=files();graph=[{'@id':'ro-crate-metadata.json','@type':'CreativeWork','conformsTo':{'@id':'https://w3id.org/ro/crate/1.1'},'about':{'@id':'./'}},{'@id':'./','@type':'Dataset','name':'Dietz-Sweet-Levin bounded mathematical and source audit','description':'Frozen inputs, selected sources, exact checks, bounded replays, preserved failures and a material-claim ledger. Private review bundle. No claim of complete independent replication or universal philosophical adjudication.','datePublished':'2026-11-01','license':{'@id':'#rights'},'hasPart':[{'@id':urllib.parse.quote(p.relative_to(ROOT).as_posix())} for p in allfiles]},{'@id':'#rights','@type':'CreativeWork','name':'Private research bundle; third-party rights retained','description':'No blanket public redistribution license granted. Check individual source rights before release; authors retain rights in their supplied articles and third parties in their sources.'}]
for p in allfiles:
 name=p.relative_to(ROOT).as_posix();item={'@id':urllib.parse.quote(name),'@type':['File','SoftwareSourceCode'] if p.suffix in ['.py','.mjs','.ps1'] else 'File','name':name,'contentSize':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 graph.append(item)
write('ro-crate-metadata.json',json.dumps({'@context':'https://w3id.org/ro/crate/1.1/context','@graph':graph},indent=2,ensure_ascii=False))
allfiles=files()+[ROOT/'ro-crate-metadata.json'];write('SHA256SUMS.txt','\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix() for p in sorted(allfiles))+'\n')
print(json.dumps({'html_bytes':(ROOT/'AUDIT_REPORT.html').stat().st_size,'claims':len(claims),'manifest_files':len(allfiles),'third_party_publication':False},indent=2))
