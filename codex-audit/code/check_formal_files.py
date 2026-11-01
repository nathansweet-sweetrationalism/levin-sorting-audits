from pathlib import Path
import re,json,subprocess
ROOT=Path(__file__).resolve().parents[1];rep=ROOT/'external/morpholib/morphoeval/lean';lean=ROOT/'tools/lean-4.35.0-windows/bin/lean.exe';files=[rep/'MathOfBiology.lean',rep/'loops/Loop_082_bioelectric_morphogen_coupling.lean',rep/'loops/Loop_083_xenobot_evolutionary_biobots.lean',rep/'loops/Loop_085_xenopus_craniofacial_remap.lean'];out=[]
for p in files:
 text=p.read_text(encoding='utf8');stack=[];decl=[]
 for line in text.splitlines():
  if m:=re.match(r'^namespace\s+(\S+)',line):stack.append(m[1])
  elif m:=re.match(r'^end(?:\s+(\S+))?\s*$',line):
   if stack:stack.pop()
  elif m:=re.match(r'^theorem\s+(\S+)',line):decl.append('.'.join(stack+[m[1]]))
 q=ROOT/'results'/('axiom_audit_'+p.name);q.write_text(text+'\n'+'\n'.join('#print axioms '+x for x in decl)+'\n',encoding='utf8');r=subprocess.run([str(lean),str(q)],capture_output=True,text=True,encoding='utf8',errors='replace',timeout=45);log=ROOT/'results'/('lean_'+p.stem+'.txt');log.write_text(r.stdout+r.stderr,encoding='utf8');bad='sorryAx' in (r.stdout+r.stderr) or r.returncode!=0
 out.append({'source':str(p.relative_to(ROOT)),'checked_file':str(q.relative_to(ROOT)),'declarations':decl,'exit_code':r.returncode,'sorryAx_or_error':bad,'output':str(log.relative_to(ROOT))});print(p.name,len(decl),'declarations','exit',r.returncode,'bad',bad,flush=True)
(ROOT/'results/lean_additional_kernel_checks.json').write_text(json.dumps(out,indent=2),encoding='utf8')
