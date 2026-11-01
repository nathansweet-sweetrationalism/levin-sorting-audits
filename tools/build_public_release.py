#!/usr/bin/env python3
"""Build the rights-filtered public release from the two private audit bundles.

Inputs (private, not redistributed): the original Codex bundle directory and the original
Claude bundle directory. Output: a repository tree in which
  * every kept file from the Codex bundle is byte-identical to the private original
    (checked later against the original SHA256SUMS.txt by verify_public_release.py), and
  * every removed file is listed with its original SHA-256, size and the reason for removal.
Removal reasons: third-party copyright or no licence, or private correspondence metadata.
Usage: python3 build_public_release.py CODEX_DIR CLAUDE_DIR OUT_DIR
"""
import sys, os, shutil, hashlib, json, fnmatch

CODEX, CLAUDE, OUT = map(os.path.abspath, sys.argv[1:4])

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

# ---------------- Codex bundle ----------------
KEEP_PRIMARY = {  # sources/primary whitelist: licence or authorship verified
    "FishShapes_specimensv1.csv": "Price et al. 2022, Dryad doi:10.5061/dryad.vt4b8gtvf, CC0-1.0",
    "wing_landmarks.tab": "Abels & Wedmann, PANGAEA doi:10.1594/PANGAEA.937651, CC-BY-4.0",
    "wing_specimens.tab": "Abels & Wedmann, PANGAEA doi:10.1594/PANGAEA.937635, CC-BY-4.0",
    "lean_sorting.lean": "fractastical/morpholib, MIT",
    "morpholib_LICENSE": "fractastical/morpholib, MIT",
    "nanopub_published_manifest_prod.txt": "fractastical/morpholib, MIT",
    "old_ablation.py": "fractastical/morpholib @ bfe377c, MIT",
    "old_commit.json": "GitHub API metadata for fractastical/morpholib (factual record)",
    "old_metrics.json": "fractastical/morpholib @ bfe377c, MIT",
    "old_model.py": "fractastical/morpholib @ bfe377c, MIT",
    "old_renderer.py": "fractastical/morpholib @ bfe377c, MIT",
    "port_js.mjs": "fractastical/morpholib, MIT",
    "thompson_pcm_downstream_implications.json": "fractastical/morpholib, MIT",
    "thompson1913_ocr.txt": "D'Arcy Thompson, On Aristotle as a Biologist (1913), public domain",
    "upstream_commit.json": "GitHub API metadata for Zhangtaining/cell_research (factual record)",
    "upstream_tree.json": "GitHub API tree listing for Zhangtaining/cell_research (factual record)",
}
PRIVATE = {"results/private_chronology_check.json": "private correspondence metadata (mailbox message identifier)"}
RULES = [  # (glob, reason) applied in order; first match removes
    ("external/cell_research/*", "Zhangtaining/cell_research has no licence file; fetch it at commit 1fd2bd5 instead"),
    ("inputs/dietz.txt", "full text of Joel Dietz's article (third-party copyright); link and hash retained"),
    ("results/ingressing_quote_page.png", "page image from Levin's paper (third-party copyright)"),
    ("sources/urls/*", "captured third-party web pages"),
    ("sources/europepmc/*.xml", "full-text article XML (third-party copyright)"),
    ("sources/europepmc/*.txt", "full-text article extraction (third-party copyright)"),
]

orig = {}
for line in open(os.path.join(CODEX, "SHA256SUMS.txt"), encoding="utf-8"):
    h, p = line.rstrip("\n").split("  ", 1)
    orig[p.replace("\\", "/")] = h

removed, kept = [], 0
dst_root = os.path.join(OUT, "codex-audit")
for root, _, files in os.walk(CODEX):
    for fn in files:
        src = os.path.join(root, fn)
        rel = os.path.relpath(src, CODEX).replace("\\", "/")
        reason = PRIVATE.get(rel)
        if reason is None:
            for g, r in RULES:
                if fnmatch.fnmatch(rel, g):
                    reason = r; break
        if reason is None and rel.startswith("sources/primary/"):
            name = rel.split("/", 2)[2]
            if not (name in KEEP_PRIMARY or name.startswith("sweet_")):
                reason = "third-party document or page capture (copyright); identity retained by hash"
        if reason:
            removed.append({"path": rel, "sha256": sha(src), "bytes": os.path.getsize(src),
                            "in_original_manifest": rel in orig,
                            "original_manifest_sha256_matches": orig.get(rel) == sha(src) if rel in orig else None,
                            "reason": reason})
            continue
        d = os.path.join(dst_root, rel); os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(src, d); kept += 1

kept_primary = {k: v for k, v in KEEP_PRIMARY.items()}
kept_primary.update({"sweet_*": "Nathan Sweet's own articles (the release author)"})
json.dump({"source_bundle": "Levin_Dietz_Sweet_Audit_2026-11-01(Codex).zip (private original)",
           "kept_files": kept, "removed_files": len(removed),
           "kept_third_party_with_licence": kept_primary,
           "removed": sorted(removed, key=lambda r: r["path"])},
          open(os.path.join(OUT, "codex-audit", "PUBLIC_RELEASE_REMOVED_FILES.json"), "w"), indent=1)

# ---------------- Claude bundle ----------------
CL_REMOVE = {
    "sources/zhang.txt": "full-text extraction of Zhang, Goldstein & Levin arXiv:2401.05375 (third-party copyright)",
    "sources/ing3.txt": "full-text extraction of Levin, Ingressing Minds, PsyArXiv v3 (third-party copyright)",
    "ARTICLE_EDITS_2026-11-01.md": "private editing worksheet for the author's own article",
    "ARTICLE_two_audits_2026-11-01.md": "moved to repository root as CROSS_AUDIT.md",
}
cl_removed = []
for root, _, files in os.walk(CLAUDE):
    for fn in files:
        src = os.path.join(root, fn)
        rel = os.path.relpath(src, CLAUDE).replace("\\", "/")
        if "__pycache__" in rel:
            continue
        if rel in CL_REMOVE:
            cl_removed.append({"path": rel, "sha256": sha(src), "bytes": os.path.getsize(src), "reason": CL_REMOVE[rel]})
            continue
        d = os.path.join(OUT, "claude-audit", rel); os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(src, d)
json.dump({"source_bundle": "levin-sorting-audit (Claude, private original)", "removed": cl_removed},
          open(os.path.join(OUT, "claude-audit", "PUBLIC_RELEASE_REMOVED_FILES.json"), "w"), indent=1)
print("codex kept", kept, "removed", len(removed), "| claude removed", len(cl_removed))
