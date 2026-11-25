#!/usr/bin/env python3
"""Aggregate q6camp/q5campaign outputs into records.jsonl + class_consistency.txt.

Deterministic; reads only output/q6camp/*.jsonl and output/q5camp/*.jsonl.
"""
import json, os, sys

exp = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.join(exp, "output")

INV = ["nP", "nPpruned", "nRmLeaves", "nSafe", "nMaximal", "nWitness", "nEmpty", "nTprime"]

def last(path):
    with open(path) as f:
        lines = [l for l in f if l.strip()]
    return json.loads(lines[-1])

def parse(fname):
    # <species>_<img>_t<offX>[_run2]
    base = fname[:-6]
    double = base.endswith("_run2")
    if double:
        base = base[:-5]
    parts = base.split("_")
    off = int(parts[-1][1:])
    img = parts[-2]
    species = "_".join(parts[:-2])
    return species, img, off, double

records = []
for camp, subdir, w, q, m, tmax in (
    ("5x23q6-species", "q6camp", 5, 6, 23, 24),
    ("5x27q5-species", "q5camp", 5, 5, 27, 19),
):
    d = os.path.join(O, subdir)
    for fname in sorted(os.listdir(d)):
        if not fname.endswith(".jsonl"):
            continue
        species, img, off, double = parse(fname)
        s = last(os.path.join(d, fname))
        records.append({
            "campaign": camp, "species": species, "image": img, "offX": off,
            "double": double, "nRmLeaves": s["nRmLeaves"], "nSafe": s["nSafe"],
            "nMaximal": s["nMaximal"], "nWitness": s["nWitness"],
            "nP": s["nP"], "nPpruned": s["nPpruned"], "nEmpty": s["nEmpty"],
            "nTprime": s["nTprime"], "elapsedMs": s["elapsedMs"],
            "seedFile": s["seedFile"], "targetMax": s["targetMax"],
            "maxP": s["maxP"], "maxRm": s["maxRm"],
            "file": "output/%s/%s" % (subdir, fname),
        })

with open(os.path.join(O, "records.jsonl"), "w") as f:
    for r in records:
        f.write(json.dumps(r) + "\n")

# class consistency: full 4-member cross-check classes (t=0 both campaigns)
uniq = {(r["campaign"], r["species"], r["image"], r["offX"]): r for r in records if not r["double"]}
lines = []
def invof(r):
    return {k: r[k] for k in INV}

def check_class(camp, species, t, members):
    got = {}
    for img, off in members:
        r = uniq.get((camp, species, img, off))
        if r is None:
            lines.append(f"{camp} {species} class t={t}: MISSING {img}@{off}")
            return False
        got[(img, off)] = r
    vals = list(got.values())
    ok = all(invof(v) == invof(vals[0]) for v in vals[1:])
    mem = ",".join(f"{img}@{off}" for img, off in members)
    if ok:
        lines.append(f"{camp} {species} class t={t} ({mem}): consistent=True "
                     f"nRmLeaves={vals[0]['nRmLeaves']} nSafe={vals[0]['nSafe']} "
                     f"nMaximal={vals[0]['nMaximal']} nWitness={vals[0]['nWitness']}")
    else:
        for k, r in got.items():
            lines.append(f"  {k}: {invof(r)}")
        lines.append(f"{camp} {species} class t={t} ({mem}): CONSISTENCY FAIL")
    return ok

all_ok = True
# q6: m=23, span s=18 -> m-s=5; class t = {id@t, H@t, V@(5-t), HV@(5-t)}
all_ok &= check_class("5x23q6-species", "m21_m21", 0, [("id", 0), ("H", 0), ("V", 5), ("HV", 5)])
# q5: m=27, span s=20 -> m-s=7; class t = {id@t, H@t, V@(7-t), HV@(7-t)}
all_ok &= check_class("5x27q5-species", "m25", 0, [("id", 0), ("H", 0), ("V", 7), ("HV", 7)])

# determinism doubles
for camp, species, img, off in (("5x23q6-species", "m21_m21", "id", 0),
                                 ("5x27q5-species", "m25", "id", 0)):
    runs = [r for r in records if r["campaign"] == camp and r["species"] == species
            and r["image"] == img and r["offX"] == off]
    core = [{k: r[k] for k in INV} for r in runs]
    ok = all(c == core[0] for c in core[1:])
    all_ok &= ok
    lines.append(f"{camp} {species} {img}@{off}: {len(runs)} runs (1 pre-interrupt + reruns), "
                 f"unlock-invariants identical={ok} nRmLeaves={core[0]['nRmLeaves']}")

# full-grid coverage assertion per species
for camp, m, species_list, noff, tmax in (
    ("5x23q6-species", 23, ["m21_m21", "m21_varA", "m21_varB"], 6, 24),
    ("5x27q5-species", 27, ["m25"], 8, 19),
):
    for sp in species_list:
        offs = sorted(r["offX"] for r in records
                      if r["campaign"] == camp and r["species"] == sp and r["image"] == "id" and not r["double"])
        want = list(range(noff))
        lines.append(f"{camp} {sp}: rep offsets {offs} complete={offs == want}")
        all_ok &= offs == want

# totals over unique configs
tot = {}
for r in records:
    if r["double"]:
        continue
    k = (r["campaign"], r["species"], r["image"], r["offX"])
    if k in tot:
        all_ok = False
        lines.append(f"DUPLICATE CONFIG {k}")
    tot[k] = r
T = sum(r["nRmLeaves"] for r in tot.values())
W = sum(r["nWitness"] for r in tot.values())
MX = sum(r["nMaximal"] for r in tot.values())
SF = sum(r["nSafe"] for r in tot.values())
q6 = sum(r["nRmLeaves"] for r in tot.values() if r["campaign"] == "5x23q6-species")
q5 = sum(r["nRmLeaves"] for r in tot.values() if r["campaign"] == "5x27q5-species")
n6 = sum(1 for r in tot.values() if r["campaign"] == "5x23q6-species")
n5 = sum(1 for r in tot.values() if r["campaign"] == "5x27q5-species")
lines.append(f"total unique-config runs: {len(tot)} (q6 {n6} / q5 {n5})")
lines.append(f"total nRmLeaves over unique configs: {T} (q6 {q6} / q5 {q5})")
lines.append(f"total nSafe: {SF}  nMaximal: {MX}  nWitness: {W}")
lines.append("records.jsonl: %d runs (incl. determinism doubles)" % len(records))
lines.append("ALL CHECKS PASS" if all_ok else "CHECK FAILURE - HALT (fail-closed)")

out = "\n".join(lines) + "\n"
with open(os.path.join(O, "class_consistency.txt"), "w") as f:
    f.write(out)
print(out)
sys.exit(0 if all_ok else 1)
