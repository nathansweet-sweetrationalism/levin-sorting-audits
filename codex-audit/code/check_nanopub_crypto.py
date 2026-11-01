from pathlib import Path
import json,importlib.metadata
from nanopub import Nanopub
ROOT=Path(__file__).resolve().parents[1];out=[]
for p in (ROOT/'sources/nanopub_registry').glob('*.trig'):
 rec={'artifact_code':p.stem,'client_version':importlib.metadata.version('nanopub'),'local_path':str(p.relative_to(ROOT))}
 try:
  np=Nanopub(rdf=p);rec.update(source_uri=np.source_uri,trusty_hash_valid=bool(np.has_valid_trusty),rsa_signature_valid=bool(np.has_valid_signature),rdf_structure_valid=bool(np.is_valid))
 except Exception as e:rec.update(error=type(e).__name__+': '+str(e))
 out.append(rec);print(rec,flush=True)
(ROOT/'results/nanopub_crypto_checks.json').write_text(json.dumps(out,indent=2),encoding='utf8')
