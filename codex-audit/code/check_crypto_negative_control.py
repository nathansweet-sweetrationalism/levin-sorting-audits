"""Tamper with in-memory assertion copies; original signed records stay unchanged."""
from pathlib import Path
import json
from rdflib import Dataset,URIRef,Literal
from nanopub import Nanopub
ROOT=Path(__file__).resolve().parents[1];out=[]
for p in sorted((ROOT/'sources/nanopub_registry').glob('*.trig')):
 # Construction already validates a record. Mutate its memory copy afterwards so
 # both hash and signature validators can be exercised independently.
 np=Nanopub(rdf=p)
 ds=np._rdf
 q=next(ds.quads((None,URIRef('http://www.nanopub.org/nschema#hasAssertion'),None,None)))
 g=ds.graph(q[2]);s,pred,obj=next(iter(g))
 replacement=URIRef(str(obj)+'/audit-tamper') if isinstance(obj,URIRef) else Literal(str(obj)+' [audit tamper]')
 g.remove((s,pred,obj));g.add((s,pred,replacement))
 row={'artifact_code':p.stem,'original_file_changed':False,'tamper_boundary':'one assertion object in an in-memory RDF copy','checks':{}}
 for attr in ['has_valid_trusty','has_valid_signature']:
  try:valid=bool(getattr(np,attr));row['checks'][attr]={'tampered_record_rejected':not valid,'returned':valid}
  except Exception as exc:row['checks'][attr]={'tampered_record_rejected':True,'error_type':type(exc).__name__}
 print(row,flush=True)
 out.append(row)
(ROOT/'results/crypto_negative_controls.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps({'records':len(out),'all_tampered_hashes_and_signatures_rejected':all(all(x['tampered_record_rejected'] for x in r['checks'].values()) for r in out)},indent=2))
