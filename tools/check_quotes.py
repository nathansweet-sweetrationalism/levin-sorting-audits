#!/usr/bin/env python3
"""Check every quotation in CROSS_AUDIT.md against a pinned primary source.

Each quotation in curly double quotes in CROSS_AUDIT.md must either
  * appear (after normalising whitespace, quote marks, dashes and PDF line-break hyphens)
    in the source assigned to it below, or
  * be listed in NOT_QUOTATIONS (titles, scare quotes, section names, or the audit's own
    proposed wording), with the reason.
Remote sources are fetched at pinned versions; PDFs are checked against pinned SHA-256
and converted with `pdftotext` (poppler-utils). Local sources are files in this repository.
Writes tools/check_quotes_result.json. Exit 0 iff every quotation is accounted for and found.
"""
import hashlib, json, os, re, subprocess, sys, tempfile, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MORPH = "https://raw.githubusercontent.com/fractastical/morpholib/35d30f4cfd5397ee1ed769f96494e018603e293d/docs/"
SOURCES = {
    "dietz": {"urls": [MORPH + "SUBSTACK_LEVIN_LATENT_SPACE_ARTICLE.md", MORPH + "SUBSTACK_LEVIN_LATENT_SPACE_CLAIMS.md"],
              "desc": "Dietz public draft + claims companion, fractastical/morpholib @ 35d30f4 (MIT)"},
    "levin": {"pdf": "https://osf.io/download/67a6189f05e0091426af4497/",
              "sha256": "ed12ff38543e0e49ddc8504af26d577c3dd766795223d473d13a25b539e5fdd6",
              "desc": "Levin, Ingressing Minds, PsyArXiv v3, doi:10.31234/osf.io/5g2xj_v3"},
    "zhang": {"pdf": "https://arxiv.org/pdf/2401.05375v1",
              "sha256": "f4e78ddc8a83f7c983d088713c916adac01c4c90eebe28d1bc9018ddef0098ca",
              "desc": "Zhang, Goldstein & Levin, arXiv:2401.05375v1"},
    "sweet": {"file": "codex-audit/sources/primary/sweet_live.plain.txt",
              "desc": "Sweet, bubble-sort article, October 31, 2026 text as retrieved by the Codex audit"},
    "sweet_supplied": {"file": "codex-audit/inputs/sweet.txt",
                       "desc": "Sweet, bubble-sort article as pasted to both audits on November 1, 2026"},
    "pipette": {"file": "codex-audit/sources/primary/sweet_pipette.plain.txt",
                "desc": "Sweet, Religion with a Pipette (October 4, modified October 7, 2026)"},
}
QUOTES = {  # quotation (as printed, without trailing punctuation) -> source key
    "the frozen cell is a brick wall": "dietz",
    "formally proved in Lean 4 Theorem 2": "dietz",
    "no cell walks around the wall": "dietz",
    "Every single swap": "dietz",
    "ΔI = −1 on every single swap": "dietz",
    "the Thompson predictor beat the clade consensus": "dietz",
    "copying the single nearest relative won by 4%": "dietz",
    "all 14 of the empirical curves": "dietz",
    "gaps in our reduced equations": "dietz",
    "a sphere manages one": "dietz",
    "kinematic phase separation": "dietz",
    "3.3× to 9.3× faster": "dietz",
    "temporarily going against its gradient to recoup greater gains later": "dietz",
    "No error-handling code was added": "dietz",
    "Spontaneous algotype clustering": "dietz",
    "Delayed gratification": "dietz",
    "Validated": "dietz",
    "The critical thing is that we did not add steps to the algorithm to check whether a swap had been completed, or to do specific things if an operation failed": "levin",
    "do not have a known physical basis but they do have structure and information content": "levin",
    "temporarily go against their gradient to recoup gains later": "levin",
    "suggests that the efficiency hypothesis can be the explanation": "zhang",
    "confirmation requires predeclared or held-out tests": "sweet",
    "Joel quotes that question accurately elsewhere": "sweet",
    "Nor is replaying his sequential model an independent replication of the original threaded implementation": "sweet",
    "The inspected code version postdates the paper’s first online publication": "sweet",
    "Radical Platonism and Radical Empiricism": "pipette",
    "…missing evidence.petition does not supply…": "sweet_supplied",
}
NOT_QUOTATIONS = {
    "Revelation": "part of the title of Sweet's article",
    "Right": "word from the title of Dietz's article, contrasted with the repository draft title",
    "independent": "scare quotes in a section heading",
    "every swap between neighbours": "the audit's own proposed wording",
}

def norm(t):
    t = re.sub(r"-\s*\n\s*", "", t)               # PDF line-break hyphenation
    t = t.replace("`", "").replace("**", "")
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"), ("−", "-"), ("­", "")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t).strip().lower()

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "quote-check"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

texts = {}
for k, s in SOURCES.items():
    if "urls" in s:
        texts[k] = "\n".join(fetch(u).decode("utf-8") for u in s["urls"])
    elif "pdf" in s:
        b = fetch(s["pdf"]); h = hashlib.sha256(b).hexdigest()
        if h != s["sha256"]:
            sys.exit(f"{k}: PDF hash {h} != pinned {s['sha256']}")
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "f.pdf"); open(p, "wb").write(b)
            texts[k] = subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True, check=True).stdout
    else:
        texts[k] = open(os.path.join(ROOT, s["file"]), encoding="utf-8").read()
ntexts = {k: norm(v) for k, v in texts.items()}

article = open(os.path.join(ROOT, "CROSS_AUDIT.md"), encoding="utf-8").read()
found = [q.strip().rstrip(".,;:") for q in re.findall(r"“([^”]+)”", article)]
results, ok = [], True
for q in sorted(set(found)):
    if q in NOT_QUOTATIONS:
        results.append({"quote": q, "status": "not a quotation", "reason": NOT_QUOTATIONS[q]}); continue
    src = QUOTES.get(q)
    if src is None:
        results.append({"quote": q, "status": "UNASSIGNED"}); ok = False; continue
    hit = norm(q.strip("…")) in ntexts[src]
    ok &= hit
    results.append({"quote": q, "source": SOURCES[src]["desc"], "status": "FOUND" if hit else "NOT FOUND"})
for r in results:
    print(f"{r['status']:16s} {r['quote'][:80]}")
json.dump({"article": "CROSS_AUDIT.md", "results": results, "all_ok": ok},
          open(os.path.join(ROOT, "tools", "check_quotes_result.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
sys.exit(0 if ok else 1)
