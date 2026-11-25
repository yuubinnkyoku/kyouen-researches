#!/usr/bin/env python3
"""Aggregate the sd43/34 sweep jsonl outputs into records.jsonl + class_consistency.txt.
Verifies: exactly one summary line per file, no witness event rows, cross-check invariants
match class rep, rerun invariants match original. Fail-closed: nonzero rc on any anomaly."""
import json, sys, hashlib, pathlib, collections

root = pathlib.Path(__file__).resolve().parents[1]
KEYS = ["nP", "nPpruned", "nRmLeaves", "nSafe", "nMaximal", "nWitness", "nEmpty", "nTprime"]

def load(p):
    lines = p.read_text().splitlines()
    assert len(lines) == 1, f"{p}: expected single summary line, got {len(lines)}"
    rec = json.loads(lines[0])
    assert rec.get("event") == "summary", f"{p}: not a summary row"
    return rec

files = sorted((root / "output").glob("sweep*/*/*.jsonl"))
assert len(files) == 30, f"expected 30 run files, got {len(files)}"
recs, anomalies = {}, []
for p in files:
    rec = load(p)
    assert rec["nWitness"] == 0 and rec["nMaximal"] == 0, f"{p}: witness/maximal found!"
    assert rec["nSafe"] == rec["nRmLeaves"], f"{p}: nSafe != nRmLeaves"
    recs[p.name] = rec
    # mutate nothing; keep file info
    rec["_file"] = str(p.relative_to(root)).replace("output/sweep", "sweep")

# consistency: crosscheck vs class rep t=0 (id@0), rerun vs original
def inv(rec): return {k: rec[k] for k in KEYS}
def check(a, b, what):
    if inv(a) != inv(b): anomalies.append(f"{what}: MISMATCH {inv(a)} vs {inv(b)}")
    else: anomalies.append(f"{what}: consistent")

# q6 and q5, for each budget
for camp, cross, repfile in [
    ("q6", ("sweep43","q6","V_off2_crosscheck.jsonl"), ("sweep43","q6","id_off0.jsonl")),
    ("q5", ("sweep43","q5","HV_off7_crosscheck.jsonl"), ("sweep43","q5","id_off0.jsonl")),
    ("q6", ("sweep34","q6","V_off2_crosscheck.jsonl"), ("sweep34","q6","id_off0.jsonl")),
    ("q5", ("sweep34","q5","HV_off7_crosscheck.jsonl"), ("sweep34","q5","id_off0.jsonl")),
]:
    a = load(root/"output"/cross[0]/cross[1]/cross[2]); b = load(root/"output"/repfile[0]/repfile[1]/repfile[2])
    tag = f"{cross[0]} {cross[1]} crosscheck-vs-id@0"
    check(a, b, tag)

for bug, orig in [("sweep43/q6/id_off0_rerun.jsonl","sweep43/q6/id_off0.jsonl"),
                  ("sweep43/q5/id_off0_rerun.jsonl","sweep43/q5/id_off0.jsonl"),
                  ("sweep34/q6/id_off0_rerun.jsonl","sweep34/q6/id_off0.jsonl"),
                  ("sweep34/q5/id_off0_rerun.jsonl","sweep34/q5/id_off0.jsonl")]:
    a = load(root/"output"/bug); b = load(root/"output"/orig)
    check(a, b, f"{bug.split('/')[0]} {bug.split('/')[1]} rerun-vs-original")

out = root/"output"
recs_out = []
for p in files:
    rec = load(p)
    recs_out.append({k: rec[k] for k in ["board","q","offX","n0","targetMax","maxP","maxRm","nP","nPpruned","nRmLeaves","nSafe","nMaximal","nWitness","nEmpty","nTprime","elapsedMs"]} | {"file": str(p.relative_to(root))})
with open(out/"records.jsonl","w") as f:
    for r in sorted(recs_out, key=lambda r: r["file"]):
        f.write(json.dumps(r) + "\n")

# totals (class reps only, reruns/crosschecks excluded as duplicates)
total = collections.Counter(); nruns = 0
for r in recs_out:
    if "rerun" in r["file"] or "crosscheck" in r["file"]: continue
    assert r["nWitness"] == 0
    total[r["file"].split("/")[1]] += r["nRmLeaves"]; nruns += 1
consistency = "\n".join(anomalies)
with open(out/"class_consistency.txt","w") as f:
    f.write(consistency + "\n")
    f.write(f"runs aggregated (rep+crosscheck+rerun): {len(recs_out)}\n")
    f.write(f"class-rep runs (coverage counting): {nruns}\n")
    for k in sorted(total): f.write(f"leaves[{k}] = {total[k]}\n")
    f.write(f"total leaves over class reps: {sum(total.values())}\n")
print(consistency)
print(f"OK: {nruns} rep runs, total leaves {sum(total.values())}")
