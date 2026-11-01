"""Explicit RSA PKCS#1 v1.5 verification with positive and assertion-tamper controls.

RDF normalization is shared with nanopub2.2.2. The cryptographic acceptance decision
uses the exception-based verifier directly, avoiding that client's ignored bool.
"""
from pathlib import Path
from base64 import decodebytes
import json,hashlib,shutil
from rdflib import URIRef,Literal
from nanopub import Nanopub
from nanopub.sign_utils import RdfUtils,RdfHasher
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15,PKCS1_v1_5
ROOT=Path(__file__).resolve().parents[1]
vocab='http://purl.org/nanopub/x/';out=[]
def verify(np):
 g=np._rdf
 target=next(g.quads((None,URIRef(vocab+'hasSignatureTarget'),URIRef(np.source_uri),None)))[0]
 def obj(predicate):return next(g.quads((target,URIRef(vocab+predicate),None,None)))[2]
 algo=str(obj('hasAlgorithm')).upper();assert algo=='RSA',algo
 key=RSA.import_key(decodebytes(str(obj('hasPublicKey')).encode()))
 signature=decodebytes(str(obj('hasSignature')).encode())
 # A signature cannot sign its own value. Nanopublication signing excludes the
 # npx:hasSignature triple as well as the self-referential trusty artifact code.
 quads=[q for q in RdfUtils.get_quads(g) if not (str(q[1])==str(target) and str(q[2])==vocab+'hasSignature')]
 normalized=RdfHasher.normalize_quads(quads,baseuri=str(np._metadata.namespace),hashstr=' ')
 digest=SHA256.new(normalized.encode())
 # Record both correct interfaces: one raises, the legacy interface returns bool.
 legacy_bool=bool(PKCS1_v1_5.new(key).verify(digest,signature))
 try:pkcs1_15.new(key).verify(digest,signature);valid=True
 except (ValueError,TypeError):valid=False
 assert valid==legacy_bool
 return valid,algo,hashlib.sha256(key.export_key(format='DER')).hexdigest()
for p in sorted((ROOT/'sources/nanopub_registry').glob('*.trig')):
 np=Nanopub(rdf=p);original,algo,keyhash=verify(np)
 q=next(np._rdf.quads((None,URIRef('http://www.nanopub.org/nschema#hasAssertion'),None,None)));g=np._rdf.graph(q[2]);s,pred,obj=next(iter(g));g.remove((s,pred,obj));g.add((s,pred,URIRef(str(obj)+'/audit-tamper') if isinstance(obj,URIRef) else Literal(str(obj)+' [audit tamper]')))
 tampered,_,_=verify(np)
 out.append({'artifact_code':p.stem,'algorithm':algo,'public_key_sha256':keyhash,'rsa_signature_valid_direct':original,'tampered_signature_valid_direct':tampered,'nanopub_client_tampered_signature_claim':bool(np.has_valid_signature),'normalization_boundary':'nanopub2.2.2 RDF normalization shared; cryptographic acceptance tested directly using two PyCryptodome interfaces'})
 print(out[-1],flush=True)
old=ROOT/'results/crypto_negative_controls.json'
if old.exists() and not (ROOT/'results/crypto_negative_controls_client_only.json').exists():shutil.copy2(old,ROOT/'results/crypto_negative_controls_client_only.json')
(ROOT/'results/rsa_direct_checks.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps({'original_signatures_valid_direct':sum(x['rsa_signature_valid_direct'] for x in out),'tampered_signatures_rejected_direct':sum(not x['tampered_signature_valid_direct'] for x in out),'client_false_positive_on_tampered_records':sum(x['nanopub_client_tampered_signature_claim'] for x in out)},indent=2))
