"""Create and verify an immutable private zip, then preserve it in the workspace.

This is a new output directory only. Existing files are not deleted or replaced.
"""
from pathlib import Path
import zipfile,hashlib,json,shutil,sys
ROOT=Path(__file__).resolve().parents[1]
assert json.loads((ROOT/'results/package_validation.json').read_text())['passed']
def unique(p):
 if not p.exists():return p
 for i in range(2,1000):
  q=p.with_name(p.stem+f'_v{i}'+p.suffix)
  if not q.exists():return q
 raise RuntimeError('No unused output name')
archive=unique(ROOT.parent/'Levin_Dietz_Sweet_Audit_2026-11-01.zip')
excluded={'.venv','tools','__pycache__','.pytest_cache'}
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and not any(x in excluded for x in p.relative_to(ROOT).parts))
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:z.write(p,ROOT.name+'/'+p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for line in (ROOT/'SHA256SUMS.txt').read_text(encoding='utf8').splitlines():
  sha,name=line.split('  ',1)
  assert hashlib.sha256(z.read(ROOT.name+'/'+name)).hexdigest()==sha,name
digest=hashlib.sha256(archive.read_bytes()).hexdigest();receipt={'archive':str(archive),'archive_sha256':digest,'archive_bytes':archive.stat().st_size,'files':len(files),'crc_and_all_manifest_entries_verified':True,'publicly_published':False}
checksum=archive.with_suffix('.zip.sha256');checksum.write_text(digest+'  '+archive.name+'\n',encoding='utf8')
if '--mirror' in sys.argv:
 base=Path(r'\\OMV\nexus\Projects\AI\Recursive Constraint Falsification (RCF)\Research_Audits')
 if not base.parent.is_dir():raise RuntimeError('Named workspace is unavailable; local archive is retained')
 base.mkdir(exist_ok=True);dest=unique(base/'2026-11-01_Levin_Dietz_Sweet_audit_01');dest.mkdir()
 # The complete evidence is in the zip; immediate review and continuation files
 # are also copied separately for convenient browsing without extraction.
 for p in [archive,checksum]:shutil.copy2(p,dest/p.name)
 for name in ['AUDIT_REPORT.md','AUDIT_REPORT.html','README.md','RESUME.md','REFERENCES.md','references-recommended.bib','SHA256SUMS.txt']:shutil.copy2(ROOT/name,dest/name)
 (dest/'results').mkdir()
 for name in ['claims.json','claims.csv','claims.schema.json','package_validation.json','audit_summary.png']:shutil.copy2(ROOT/'results'/name,dest/'results'/name)
 assert hashlib.sha256((dest/archive.name).read_bytes()).hexdigest()==digest
 (dest/'MIRROR_README.txt').write_text('The zip contains the complete frozen research evidence. Standalone report and ledger files are also provided for immediate review. Extract the zip before following relative source paths or running validation. The original working audit is at '+str(ROOT)+'. No public repository or Library upload is claimed.\n',encoding='utf8')
 receipt['workspace_mirror']=str(dest);receipt['mirrored_archive_hash_verified']=True
receipt_path=archive.with_suffix('.delivery.json');receipt_path.write_text(json.dumps(receipt,indent=2),encoding='utf8')
print(json.dumps(receipt,indent=2))
