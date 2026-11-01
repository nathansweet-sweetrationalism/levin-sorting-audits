from pathlib import Path
import urllib.request,json,ast,numpy as np
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'sources/primary/old_renderer.py'
with urllib.request.urlopen('https://raw.githubusercontent.com/fractastical/morpholib/bfe377c2f9d5bfc35e0083df1c04eb9fe6ca739e/sorting-morphogenesis/render_13yo_illustrations.py',timeout=25) as r:p.write_bytes(r.read())
out=[]
for p in [p,ROOT/'external/morpholib/sorting-morphogenesis/render_13yo_illustrations.py']:
 t=ast.parse(p.read_text(encoding='utf-8-sig'));fun=next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name=='render_fig8_ai_vs_human_authorship_heatmap');matrix=next(x for x in ast.walk(fun) if isinstance(x,ast.Assign) and any(isinstance(z,ast.Name) and z.id=='ai_matrix' for z in x.targets));a=np.array(ast.literal_eval(matrix.value.args[0]));out.append({'file':str(p.relative_to(ROOT)),'rows':len(a),'hypothesis_human_pct':round(100-float(a[:,0].mean()),1),'prose_human_pct':round(100-float(a[:,1].mean()),1),'technical_ai_pct_all_rows':round(float(a[:,2:5].mean()),1),'data_origin':'author estimates; arithmetic check cannot verify actual contribution shares'})
(ROOT/'results/authorship_arithmetic.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
