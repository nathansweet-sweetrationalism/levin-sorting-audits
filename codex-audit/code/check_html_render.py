"""Headless isolated-browser rendering of the local report; no user session is used."""
from pathlib import Path
import subprocess,json,re,os
ROOT=Path(__file__).resolve().parents[1]
browser=Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')
profile=ROOT/'tools/edge-review-profile';shot=ROOT/'results/report_preview.png'
cmd=[str(browser),'--headless','--disable-gpu','--no-first-run','--disable-extensions','--user-data-dir='+str(profile),'--window-size=1440,1100','--screenshot='+str(shot),'--dump-dom',(ROOT/'AUDIT_REPORT.html').as_uri()]
r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=55,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
dom=r.stdout
result={'browser':'Microsoft Edge isolated headless profile','exit_code':r.returncode,'screenshot_exists':shot.is_file(),'claim_details':len(re.findall(r'<details class="claim"',dom)),'script_count_text':'64 claims shown' in dom,'screenshot':'results/report_preview.png','dom_contains_report_title':'Mathematical and source audit' in dom,'limits':'Desktop initial viewport and script execution checked; not an exhaustive accessibility, print, mobile or cross-browser test.'}
(ROOT/'results/html_render_check.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result,indent=2));assert r.returncode==0 and result['screenshot_exists'] and result['claim_details']==64 and result['script_count_text'] and result['dom_contains_report_title']
