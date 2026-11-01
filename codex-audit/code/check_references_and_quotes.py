from pathlib import Path
import json,re,html,unicodedata,urllib.request,hashlib,time
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
class Text(HTMLParser):
 def __init__(self):super().__init__();self.out=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,s):
  if not self.skip:self.out.append(s)
def plain(s):
 h=Text();h.feed(s);return ' '.join(h.out)
for p in (ROOT/'sources/primary').glob('*.html'):p.with_suffix('.plain.txt').write_text(plain(p.read_text(encoding='utf8',errors='replace')),encoding='utf8')
# Match every exact attributed phrase while retaining unresolved/scare-quote cases as such.
def norm(s):
 s=unicodedata.normalize('NFKC',html.unescape(s)).replace('\xad','');return ' '.join(re.findall(r"[a-z0-9]+",s.lower()))
corpus=[]
for base in [ROOT/'sources/primary',ROOT/'sources/europepmc']:
 for p in base.glob('*.txt'):
  if any(x in p.name for x in ['sweet_live','sweet_original']):continue
  corpus.append((str(p.relative_to(ROOT)),norm(p.read_text(encoding='utf8',errors='replace'))))
# Third-party pages explicitly linked in input, retained separately from the target articles.
for x in json.loads((ROOT/'results/url_resolution.json').read_text(encoding='utf8')):
 if x['status']==200 and any(s in x['url'] for s in ['scienceandculture.com','lexfridman.com']):
  p=ROOT/x['local_path'];corpus.append((str(p.relative_to(ROOT)),norm(plain(p.read_text(encoding='utf8',errors='replace')))))
quotes=json.loads((ROOT/'results/quote_inventory.json').read_text(encoding='utf8'))
for q in quotes:
 n=norm(q['quote']);matches=[p for p,t in corpus if n and n in t]
 q['exact_normalized_matches']=matches
 q['status']='normalized_word_match_requires_context_check' if matches else ('short_term_or_label_not_external_quotation' if len(q['quote'].split())<5 else 'not_matched_to_preserved_primary_source')
 q['normalization']='case, punctuation, whitespace, Unicode compatibility and soft hyphens normalized; word order retained'
# Explicit source adjudications for substantive quotations. The inventory keeps raw text and locators.
for q in quotes:
 if q['article']=='sweet' and q['line']==19:q.update(status='verified_words_minor_punctuation_difference',evidence='sources/primary/feynman.plain.txt')
 if q['article']=='sweet' and q['line']==68:q.update(status='private_exchange_not_independently_verified',evidence='only author report in supplied target')
 if q['article']=='sweet' and q['line']==165:q.update(status='explicit_hypothetical_question_not_historical_quote')
 if q['article']=='dietz' and q['line']==12:q.update(status='authors_own_reported_explanation_no_external_transcript')
 if q['article']=='dietz' and q['line']==65:q.update(status='verified_published_wording_locator_version_drift',evidence='sources/primary/ingressing.pdf PDF/printed page 29, section 6.3; article says page 22')
 if q['article']=='dietz' and q['line']==92:q.update(status='not_verbatim_in_cited_published_version',evidence='Published page 29 uses different wording about moving away from the goal; label paraphrase or supply another exact version.')
 if q['article']=='dietz' and q['line']==261:q.update(status='matches_preserved_mirror_with_ellipsis_primary_post_needs_rendered_validation',evidence='sources/primary/levin_post_mirror.plain.txt; HTTP 200 from x.com alone is insufficient')
 if q['article']=='dietz' and q['line']==278:q.update(status='verified_paper_abstract_wording',evidence='sources/primary/platonic_representation.pdf page 1; conclusion remains a hypothesis')
 if q['article']=='dietz' and q['line']==286:q.update(status='not_verified_against_original_recording',evidence='Related public quotations found; symposium slide/recording not supplied. Do not certify exact wording.')
(ROOT/'results/quote_checks.json').write_text(json.dumps(quotes,indent=2,ensure_ascii=False),encoding='utf8')
# Preserve exact comment boundaries for public correspondence verification.
s=(ROOT/'sources/primary/symposium.html').read_text(encoding='utf8');comments={}
for k in ['4345','4350','4449']:
 pos=s.find('id="comment-'+k+'"');end=s.find('<li',pos+20);end=end if end>pos else pos+15000;comments[k]={'found':pos>=0,'text':plain(s[pos:end]),'raw_offset':pos}
(ROOT/'results/symposium_comment_excerpts.json').write_text(json.dumps(comments,indent=2),encoding='utf8')
# Metadata verification is distinct from full-text support.
wrong={
 '10.1111/evo.12502':{'intended':'Claverie & Wainwright, A morphospace for reef fishes','correct_doi':'10.1371/journal.pone.0112732','correct_citation':'Claverie T, Wainwright PC (2014). PLoS ONE 9(11):e112732.'},
 '10.1093/sysbio/syz029':{'intended':'Friedman et al., Body shape diversification along the benthic-pelagic axis','correct_doi':'10.1098/rspb.2020.1053','correct_citation':'Friedman ST, Price SA, Corn KA, Larouche O, Martinez CM, Wainwright PC (2020). Proceedings of the Royal Society B 287:20201053.'},
 '10.1242/dev.175950':{'intended':'Pinet et al., Adaptive correction of craniofacial defects','correct_doi':'10.1242/dev.175893','correct_citation':'Pinet K, Deolankar M, Leung B, McLaughlin KA (2019). Development 146(14):dev175893.'},
 '10.3389/fphys.2016.00178':{'intended':'Pietak & Levin, Exploring instructive physiological signaling with BETSE','correct_doi':'10.3389/fbioe.2016.00055','correct_citation':'Pietak A, Levin M (2016). Frontiers in Bioengineering and Biotechnology 4:55.'}}
meta=json.loads((ROOT/'results/doi_metadata_summary.json').read_text(encoding='utf8'));occ=json.loads((ROOT/'results/doi_occurrences.json').read_text(encoding='utf8'));reg=[]
for x in meta:
 z={**x,'input_occurrences':[{'article':o['article'],'line':o['line'],'context':o['context']} for o in occ if o['doi']==x['doi']],'verification':'registry_record_retrieved_not_full_text_validation','retraction_check':'no exhaustive retraction assurance; registration metadata alone is insufficient'}
 if x['doi'] in wrong:z.update(verification='confirmed_mismatched_reference',correction=wrong[x['doi']])
 reg.append(z)
(ROOT/'results/reference_checks.json').write_text(json.dumps(reg,indent=2,ensure_ascii=False),encoding='utf8')
# Mark URL semantics rather than mistaking HTTP success for reference validity.
urls=json.loads((ROOT/'results/url_resolution.json').read_text(encoding='utf8'))
for u in urls:
 u['interpretation']='HTTP response only; content and referent require separate verification'
 if u['status']!=200:u['interpretation']='access failure in this route, not evidence of invalid URL or invalid publication'
 if 'youtube.com/watch?' in u['url']:
  ident=u['url'].split('v=')[-1].split('&')[0];u['video_id_shape_valid']=bool(re.fullmatch(r'[A-Za-z0-9_-]{11}',ident))
  if not u['video_id_shape_valid']:u['interpretation']='pasted text concatenates video URL with caption; use the live article anchor, not the concatenated string'
(ROOT/'results/url_checks.json').write_text(json.dumps(urls,indent=2),encoding='utf8')
# Methodology and critical sources: verify identity before recommendation.
recommended={
 '10.1371/journal.pcbi.1001122':'Full simulation experiment specification (MIASE)',
 '10.1371/journal.pcbi.1003285':'Versioning, provenance and reproducible computation',
 '10.1371/journal.pcbi.1009917':'Principled simulation and scheduling',
 '10.18564/jasss.4259':'ODD agent-based model protocol',
 '10.21105/joss.01891':'Property-based testing with Hypothesis',
 '10.1126/science.263.5147.641':'Limits of confirmation and model uniqueness',
 '10.1111/ecog.02881':'Structured and phylogenetic cross-validation',
 '10.1086/284325':'Phylogenies and comparative nonindependence',
 '10.1038/sdata.2016.18':'FAIR principles',
 '10.3233/DS-210053':'Research-object packaging (RO-Crate)',
 '10.1371/journal.pone.0309210':'Workflow execution provenance',
 '10.3233/SW-140160':'Trusty content-addressed identifiers',
 '10.1093/bjps/axs012':'Distinctively mathematical explanation',
 '10.1007/978-3-030-79876-5_37':'Lean 4 system description',
 '10.1002/ecy.3829':'Actual FishShapes dataset paper',
 '10.1016/j.bpj.2017.04.011':'Persistent bioelectric regeneration experiments',
}
records=[]
for d,purpose in recommended.items():
 p=ROOT/'sources/recommended_metadata'/(hashlib.sha256(d.encode()).hexdigest()[:16]+'.json');p.parent.mkdir(parents=True,exist_ok=True)
 try:
  with urllib.request.urlopen(urllib.request.Request('https://api.crossref.org/works/'+d,headers={'User-Agent':'RCF-audit/1.0'}),timeout=20) as r:b=r.read()
  p.write_bytes(b);m=json.loads(b)['message'];records.append({'doi':d,'purpose':purpose,'title':m.get('title'),'author':m.get('author'),'published':m.get('published'),'container':m.get('container-title'),'metadata_status':'verified','reading_scope':'registry metadata; separately saved full texts identified in access register'})
 except Exception as e:records.append({'doi':d,'purpose':purpose,'metadata_status':'unavailable','error':str(e)})
 time.sleep(.3)
(ROOT/'results/recommended_literature.json').write_text(json.dumps(records,indent=2),encoding='utf8')
print('references',len(reg),'mismatches',len(wrong),'quotes',len(quotes),'exact normalized candidates',sum(bool(x['exact_normalized_matches']) for x in quotes),'recommended metadata',sum(x['metadata_status']=='verified' for x in records),'/',len(records));[(print(k,v['found'],v['text'][:1900])) for k,v in comments.items()]
