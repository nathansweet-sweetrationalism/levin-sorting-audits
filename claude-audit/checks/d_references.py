#!/usr/bin/env python3
"""Resolve every DOI cited in both articles via doi.org content negotiation (CSL-JSON;
works for Crossref and DataCite), and compare against the claimed metadata.
Claimed fields: (article, first-author surname, year, container fragment, volume, title fragment).
Writes results/d_references.json (includes the raw CSL records for audit)."""
import json, os, urllib.request, time, sys

CLAIMS = [
 # Dietz
 ("Dietz", "10.5281/zenodo.20622878", "Dietz", "2026", "", "", "NeuroEval"),
 ("Dietz", "10.5281/zenodo.20567719", "Dietz", "2026", "", "", "BioEval"),
 ("Dietz", "10.5281/zenodo.23680705", "Dietz", "2026", "", "", "MorphoEval"),
 ("Dietz", "10.31234/osf.io/5g2xj_v3", "Levin", "2025", "", "", "Ingressing"),
 ("Dietz", "10.3390/philosophies11050161", "Levin", "2026", "Philosophies", "11", "Ingressing"),
 ("Dietz", "10.5962/bhl.title.11332", "Thompson", "1917", "", "", "growth and form"),
 ("Dietz", "10.5962/bhl.title.147382", "Aristotle", "1910", "", "", "Historia"),
 ("Both", "10.1177/10597123241269740", "Zhang", "2025", "Adaptive Behavior", "33", "sorting"),
 ("Dietz", "10.1111/evo.12502", "Claverie", "2014", "Evolution", "68", "morphospace"),
 ("Dietz", "10.1093/sysbio/syz029", "Friedman", "2019", "Systematic Biology", "69", "benthic"),
 ("Dietz", "10.1109/34.24792", "Bookstein", "1989", "Pattern Analysis", "11", "Principal warps"),
 ("Dietz", "10.1038/s41586-018-0273-1", "Rabosky", "2018", "Nature", "559", "latitudinal"),
 ("Dietz", "10.1016/j.ydbio.2009.12.012", "Oviedo", "2010", "Developmental Biology", "339", "polarity"),
 ("Dietz", "10.1016/j.chembiol.2010.11.012", "Beane", "2011", "Chemistry", "18", "H,K-ATPase"),
 ("Dietz", "10.3389/fphys.2016.00178", "Pietak", "2016", "Frontiers in Physiology", "7", "BETSE"),
 ("Dietz", "10.1098/rsif.2017.0425", "Pietak", "2017", "Interface", "14", "gene and reaction networks"),
 ("Dietz", "10.1016/j.biosystems.2021.104511", "Cervera", "2021", "BioSystems", "209", "gap junction"),
 ("Dietz-inline", "10.1016/j.ydbio.2012.01.027", "Vandenberg", "2012", "", "", "craniofacial"),
 ("Dietz", "10.1002/dvdy.23770", "Vandenberg", "2012", "Developmental Dynamics", "241", "craniofacial"),
 ("Dietz-inline", "10.1098/rsif.2015.0772", "Pezzulo", "2015", "", "", "Re-membering"),
 ("Dietz", "10.1039/c5ib00221d", "Pezzulo", "2015", "Integrative Biology", "7", "Re-membering"),
 ("Dietz", "10.1242/dev.175950", "Pinet", "2019", "Development", "146", "craniofacial"),
 ("Dietz", "10.1073/pnas.1910837117", "Kriegman", "2020", "Proceedings", "117", "reconfigurable"),
 ("Dietz", "10.1073/pnas.2112672118", "Kriegman", "2021", "Proceedings", "118", "self-replication"),
 ("Dietz", "10.3389/fnsys.2022.768201", "Levin", "2022", "Frontiers in Systems Neuroscience", "16", "Mind Everywhere"),
 ("Dietz", "10.1038/41557", "Simard", "1997", "Nature", "388", "carbon"),
 ("Both", "10.1073/pnas.1314922110", "Hoel", "2013", "Proceedings", "110", "causal emergence"),
 ("Dietz", "10.1016/j.patter.2025.101472", "Hoel", "2026", "Patterns", "7", "emergent complexity"),
 ("Dietz", "10.1093/bioinformatics/btt088", "Lobo", "2013", "Bioinformatics", "29", "Planform"),
 ("Dietz", "10.1242/bio.20123400", "Lobo", "2013", "Biology Open", "2", ""),
 ("Dietz", "10.1093/bioinformatics/btu582", "Lobo", "2014", "Bioinformatics", "30", "Limbform"),
 ("Dietz", "10.1098/rsif.2013.0918", "Lobo", "2014", "Interface", "11", "linear-encoding"),
 ("Dietz", "10.3897/JHR.32.4685", "Perrard", "2013", "Hymenoptera", "32", "hornets"),
 # Sweet
 ("Sweet", "10.1080/0022250X.1971.9989794", "Schelling", "1971", "Mathematical Sociology", "1", "segregation"),
 ("Sweet", "10.1016/j.jjimei.2021.100042", "Zutshi", "2021", "Data Insights", "1", "sorting"),
 ("Sweet", "10.1093/comjnl/bxab107", "Ganapathi", "2021", "Computer Journal", "", "bubble sort"),
 ("Sweet", "10.1155/2019/3027578", "Shabaz", "2019", "Networks and Communications", "2019", "SA Sorting"),
 ("Sweet", "10.1145/3158137", "Flückiger", "2018", "", "", "speculative"),
 ("Sweet", "10.1147/rd.53.0183", "Landauer", "1961", "IBM Journal", "5", "Irreversibility"),
 ("Sweet", "10.1016/S1355-2198(03)00039-X", "Bennett", "2003", "Studies in History", "34", "Landauer"),
 ("Sweet", "10.3390/e19050188", "Hoel", "2017", "Entropy", "19", "Map"),
 ("Sweet", "10.3390/philosophies7020030", "Eberhardt", "2022", "Philosophies", "7", "Causal Emergence"),
 ("Sweet", "10.1007/s00224-006-1311-1", "Franceschini", "2007", "Theory of Computing Systems", "40", "Stably"),
]

def fetch(doi):
    req = urllib.request.Request("https://doi.org/" + doi,
                                 headers={"Accept": "application/vnd.citationstyles.csl+json",
                                          "User-Agent": "audit-script" + (" (mailto:" + os.environ["CROSSREF_MAILTO"] + ")" if os.environ.get("CROSSREF_MAILTO") else "")})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            err = str(e); time.sleep(2)
    return {"_error": err}

def year_of(rec):
    for k in ("published-print", "issued", "published-online", "published"):
        dp = rec.get(k, {}).get("date-parts")
        if dp and dp[0] and dp[0][0]:
            return str(dp[0][0])
    return ""

def main():
  out = []
  for art, doi, au, yr, cont, vol, tfrag in CLAIMS:
      rec = fetch(doi)
      if "_error" in rec:
          out.append({"article": art, "doi": doi, "status": "UNRESOLVED", "error": rec["_error"]}); print("UNRESOLVED", doi); continue
      authors = rec.get("author", [])
      first = (authors[0].get("family") or authors[0].get("literal") or "") if authors else ""
      title = rec.get("title", "")
      if isinstance(title, list): title = title[0] if title else ""
      container = rec.get("container-title", "")
      if isinstance(container, list): container = container[0] if container else ""
      years = {year_of(rec)} | {str(rec.get(k, {}).get("date-parts", [[None]])[0][0]) for k in ("published-print", "published-online", "issued")}
      chk = {
          "first_author": au.lower() in first.lower() or au.lower() in json.dumps(authors, ensure_ascii=False).lower(),
          "year": yr in years,
          "container": (cont.lower() in container.lower()) if cont else None,
          "volume": (str(rec.get("volume", "")) == vol) if vol else None,
          "title": (tfrag.lower() in title.lower()) if tfrag else None,
      }
      status = "MATCH" if all(v is not False for v in chk.values()) else "MISMATCH"
      out.append({"article": art, "doi": doi, "status": status, "checks": chk, "resolved": {
          "first_author": first, "title": title, "container": container, "volume": rec.get("volume"),
          "issue": rec.get("issue"), "page": rec.get("page"), "years_seen": sorted(y for y in years if y and y != "None"),
          "type": rec.get("type")}})
      print(status, doi, "|", first, "|", title[:70], "|", container[:40], rec.get("volume"), sorted(years))
  json.dump(out, open("results/d_references.json", "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
