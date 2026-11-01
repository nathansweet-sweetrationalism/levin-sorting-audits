#!/usr/bin/env python3
"""Resolve the methodological references recommended in REPORT.md (same resolver as d_references.py)."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from d_references import fetch  # noqa
REFS = {
 "10.1126/science.1213847": "Peng 2011", "10.1371/journal.pcbi.1003285": "Sandve 2013",
 "10.1038/sdata.2016.18": "Wilkinson 2016 FAIR", "10.17226/25303": "NASEM 2019",
 "10.1080/00031305.2016.1154108": "Wasserstein & Lazar 2016", "10.1073/pnas.1708274114": "Nosek 2018",
 "10.1177/0956797611417632": "Simmons 2011", "10.1037/h0040957": "Cronbach & Meehl 1955",
 "10.1037/0003-066X.50.9.741": "Messick 1995", "10.1787/9789264043466-en": "OECD/JRC 2008",
 "10.1214/aoms/1177731909": "Wald & Wolfowitz 1940", "10.1111/j.1558-5646.1996.tb03563.x": "Schluter 1996",
 "10.1086/284325": "Felsenstein 1985", "10.1093/sysbio/syy031": "Uyeda 2018",
 "10.2307/2992207": "Rohlf & Slice 1990", "10.1145/48529.48530": "Fetzer 1988",
 "10.1007/978-3-319-07443-6_27": "Kuhn & Dumontier 2014", "10.7717/peerj-cs.78": "Kuhn 2016",
 "10.1038/s41598-023-41032-5": "Walters & Wilder 2023", "10.1017/9781107286184": "Mayo 2018",
 "10.1016/S0025-5564(96)00186-1": "Stone 1997", "10.1007/978-3-030-79876-5_37": "de Moura & Ullrich 2021",
 "10.1145/2812803": "Collberg & Proebsting 2016", "10.1145/3186266": "Ivie & Thain 2018",
}
out = {}
for doi, lab in REFS.items():
    r = fetch(doi)
    if "_error" in r:
        out[doi] = {"label": lab, "status": "UNRESOLVED"}; print("UNRESOLVED", doi, lab); continue
    t = r.get("title", ""); t = t[0] if isinstance(t, list) and t else t
    a = r.get("author", [{}]); fa = (a[0].get("family") or a[0].get("literal", "")) if a else ""
    y = (r.get("issued", {}).get("date-parts") or [[None]])[0][0]
    out[doi] = {"label": lab, "first_author": fa, "year": y, "title": t}
    print(lab, "|", fa, y, "|", t[:90])
json.dump(out, open("results/d_method_refs.json", "w"), indent=1, ensure_ascii=False)
