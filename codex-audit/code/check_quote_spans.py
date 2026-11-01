"""Supplement initial line-based quote inventory with multiline and ASCII spans."""
from pathlib import Path
import json,re,html,unicodedata,urllib.request
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
class P(HTMLParser):
 def __init__(self):super().__init__();self.a=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,s):
  if not self.skip:self.a.append(s)
def norm(s):return ' '.join(re.findall(r'[a-z0-9]+',unicodedata.normalize('NFKC',html.unescape(s)).replace('\xad','').lower()))
# Prefer the independently hosted same translation after the first host's certificate failure.
url='https://classics.mit.edu/Aristotle/soul.2.ii.html';p=ROOT/'sources/primary/aristotle_soul_mit.html'
if not p.exists():p.write_bytes(urllib.request.urlopen(url,timeout=35).read())
h=P();h.feed(p.read_text(encoding='utf8'));p.with_suffix('.plain.txt').write_text(' '.join(h.a),encoding='utf8')
corpus=[]
for p in (ROOT/'sources/primary').glob('*.txt'):
 if p.name in ['sweet_live.plain.txt','sweet_original.plain.txt']:continue
 corpus.append((str(p.relative_to(ROOT)),norm(p.read_text(encoding='utf8',errors='replace'))))
old=json.loads((ROOT/'results/quote_checks.json').read_text(encoding='utf8'));lookup={(q['article'],q['line'],q['quote']):q for q in old};out=[]
for article in ['sweet','dietz']:
 s=(ROOT/'inputs'/f'{article}.txt').read_text(encoding='utf8')
 for pattern,label in [(r'“([^”]+)”','curly_multiline'),(r'"([^"\n]+)"','ascii_singleline')]:
  for m in re.finditer(pattern,s,re.S):
   line=s.count('\n',0,m.start())+1;q=m.group(1);n=norm(q);matches=[p for p,t in corpus if n and n in t]
   prior=lookup.get((article,line,q));status=prior['status'] if prior else ('normalized_word_match_requires_context_check' if matches else 'unresolved_or_constructed_wording_needs_classification')
   if article=='dietz' and 'Joel Dietz points in the right direction' in q:
    status='not_matched_to_retrieved_companion_version' if not matches else 'normalized_match_to_public_companion_article'
   out.append({'article':article,'line_start':line,'line_end':s.count('\n',0,m.end())+1,'delimiter':label,'quote':q,'status':status,'normalized_matches':matches,'note':'Extraction is not adjudication. Nested opening marks and scare quotes can affect spans; initial linewise inventory remains available.'})
(ROOT/'results/quote_span_supplement.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf8')
history={'aristotle_primary_url':url,'triangle_scope':'De Anima II.3,414b28-32; Smith translation expresses square containing triangle, so exact article words are translation-dependent.','causes_scope':'De Anima II.4,415b8-12: origin of movement,end,essence; supports the three-cause reading.','seventh_letter':'MIT J.Harward translation supports ineffability/non-writing passage; authorship disputed. Passage alone does not establish an Eleusinian/Delphic ritual prohibition or empirical reliability.','seventh_letter_authenticity_source':'https://plato.stanford.edu/entries/plato/','thompson1913':'Original OCR pp26-27 supports graded souls, triangle/square analogy, biology-philosophy linkage. OCR source also includes a reasoning-soul-from-afar discussion, so an exclusively simple modern materialist attribution would need qualification. OCR needs page-image check for exact Greek wording.','companion_quote_candidates':[x for x in out if 'Joel Dietz points in the right direction' in x['quote']]}
(ROOT/'results/historical_text_checks.json').write_text(json.dumps(history,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps({'additional_span_inventory':len(out),'multiline_spans':sum(x['line_end']>x['line_start'] for x in out),'companion_quote_status':[x['status'] for x in history['companion_quote_candidates']]},indent=2))
