from pathlib import Path
import subprocess,json,time
ROOT=Path(__file__).resolve().parents[1];py=ROOT/'.venv/Scripts/python.exe';repo=ROOT/'external/morpholib'
tasks=[('pietak_selftest',[str(py),'-X','utf8',str(repo/'models/2017-pietak-bioelectric-morphogen-coupling.py'),'--self-test']),('tadpole_selftest',[str(py),'-X','utf8',str(repo/'models/2019-bischof-xenopus-craniofacial-remap.py'),'--self-test']),('xenobot_selftest',[str(py),'-X','utf8',str(repo/'models/2020-kriegman-xenobot-evolutionary-biobots.py'),'--self-test']),('node_port',['C:/Program Files/nodejs/node.exe',str(ROOT/'sources/primary/port_js.mjs'),'--n','100','--reps','15','--seed','42'])]
out=[]
for name,cmd in tasks:
 start=time.perf_counter()
 try:
  p=subprocess.run(cmd,cwd=str(repo),capture_output=True,text=True,encoding='utf8',errors='replace',timeout=70);rec={'name':name,'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'seconds':time.perf_counter()-start}
 except subprocess.TimeoutExpired as e:rec={'name':name,'command':cmd,'status':'timeout','seconds':time.perf_counter()-start}
 (ROOT/'results'/f'{name}.json').write_text(json.dumps(rec,indent=2),encoding='utf8');out.append(rec);print(name,rec.get('exit_code',rec.get('status')),rec.get('stderr','')[-700:],flush=True)
(ROOT/'results/upstream_execution_checks.json').write_text(json.dumps(out,indent=2),encoding='utf8')
