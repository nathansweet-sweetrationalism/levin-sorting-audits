#!/usr/bin/env python3
"""Build claims_ledger.json from the tables in REPORT.md, attaching SHA-256 of every cited result file."""
import re, json, hashlib, os, glob
LABEL = {"D1a":"EXACT","D1b":"REPRODUCED-WITH-DESIGN-CAVEAT","D1c":"FALSE","D1d":"OVERSTATED","D2a":"EXACT","D2b":"TRUE",
 "D2c":"PARTLY-TRUE","D2d":"PARTLY-TRUE","D2e":"FALSE-FOR-PUBLIC-CODE","D2f":"TRUE","D3a":"REPRODUCED","D3b":"IMPRECISE",
 "D3c":"PRIOR-ART","D4a":"MISATTRIBUTED","D4b":"INCOMPLETE","D4c":"NOT-DISCRIMINATING","D4d":"CONSISTENT","D4e":"UNDEFINED",
 "D4f":"WRONG-CITATION","D4g":"SCOPE-MISMATCH","D5":"CORRECT","D6":"WRONG-CITATION","D7":"APPROXIMATE","D8a":"EXACT",
 "D8b":"ROUNDING-ERROR","D8c":"NO-DEFINED-CONSTRUCT","D9":"OVERSTATED","D10":"TRUE-WITH-SPECIFICATION-GAP","D11":"GLOSS-NOT-IN-SOURCE",
 "S1":"EXACT","S2":"EXACT","S3":"EXACT","S4":"EXACT","S5":"EXACT","S6":"EXACT","S7":"TRUE","S8":"EXACT",
 "S9":"MISLEADING-SCOPE","S10":"EXACT","S11":"CORRECT","S12":"EXACT","S13":"WITHDRAWN-COPY-ARTIFACT","S14":"NOT-CHECKED"}
rows = []
for line in open("REPORT.md", encoding="utf-8"):
    m = re.match(r"\| ([DS]\d+[a-z]?) \| (.*) \| (.*) \| (.*) \|\s*$", line)
    if m:
        cid, claim, verdict, ev = m.groups()
        files = [f for f in glob.glob("results/*.json") if os.path.basename(f).split(".")[0] in ev]
        rows.append({"id": cid, "author": "Dietz" if cid.startswith("D") else "Sweet", "claim": claim,
                     "verdict_label": LABEL[cid],
                     "verdict": verdict, "evidence": ev,
                     "result_files": {f: hashlib.sha256(open(f, "rb").read()).hexdigest() for f in files}})
json.dump({"generated": "2026-11-01", "rows": rows}, open("claims_ledger.json", "w"), indent=1, ensure_ascii=False)
print(len(rows), "rows")
