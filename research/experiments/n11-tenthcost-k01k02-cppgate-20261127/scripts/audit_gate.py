#!/usr/bin/env python3
# fresh batch audit for the n11 tenth-cost k01/k02 C++ scrutiny gate kit.
# fail-closed: any gate failure exits non-zero and names the gate.
# G0 input pins  G1 raw format  G2 pair equality  G3 expected equality
# G4 status log  G5 anchor block  G6 head freshness (head sha + absence)
import json, hashlib, os, re, sys

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(KIT, "output")
fail = []
def gate(name, ok, msg=""):
    if not ok:
        fail.append(f"{name}: {msg}")

rows = json.load(open(os.path.join(KIT, "input", "gate-rows.json")))
targets, anchors = rows["targets"], rows["anchors"]

# G0: input pins
for k, t in targets.items():
    p = os.path.join(KIT, "input", f"{k}.input.csv")
    gate("G0", os.path.exists(p), f"missing {k}.input.csv")
    sha = hashlib.sha256(open(p, "rb").read()).hexdigest()
    gate("G0", sha == t["input_pin"], f"{k} input_pin {sha}")

# G1/G2/G3: raws
def fields(p):
    txt = open(p).read()
    m = re.search(r"^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),\d+,(\d+),(\d+)$", txt, re.M)
    if not m: return None
    return m.groups()  # stones,legal,is_or,budget,result,nodes,wall,lo,hi

allrows = dict(targets)
allrows.update({k: {"key": None, "expected": a["expected"], "lo": None} for k, a in anchors.items()})
status = []
for k, t in allrows.items():
    p1 = os.path.join(OUT, "raw", f"{k}.p1.out")
    p2 = os.path.join(OUT, "raw", f"{k}.p2.out")
    gate("G1", os.path.exists(p1) and os.path.exists(p2), f"missing raws {k}")
    f1, f2 = fields(p1), fields(p2)
    gate("G1", f1 is not None and f2 is not None, f"bad raw format {k}")
    if not f1 or not f2: continue
    q1 = f"{f1[2]},{f1[4]},{f1[5]},{f1[6]}"   # legal,budget,result,nodes
    q2 = f"{f2[2]},{f2[4]},{f2[5]},{f2[6]}"
    gate("G2", q1 == q2, f"{k} pair {q1} vs {q2}")
    gate("G3", q1 == t["expected"], f"{k} expected {q1} vs {t['expected']}")
    status.append(k)

# G4: status log
log = open(os.path.join(OUT, "gate-status.log")).read()
passes = re.findall(r" (\S+) GATE-PASS ", log)
gate("G4", len(passes) == len(status) and sorted(passes) == sorted(status),
     f"passes {passes} vs rows {status}")
gate("G4", "GATE-FAIL" not in log and "MISMATCH" not in log and "CRASH" not in log, "failure tokens in log")

# G5: anchor expecteds equal the SW kit anchors block (hardcoded, machine-derived)
sw = {"anchor-at2m": "98,2000000,0,2000000",
      "anchor-aj001": "84,30000000,2,5156075",
      "anchor-af039": "89,30000000,2,19234232"}
for k, v in sw.items():
    gate("G5", anchors[k]["expected"] == v, f"{k} anchor expected {anchors[k]['expected']}")
    f1 = fields(os.path.join(OUT, "raw", f"{k}.p1.out"))
    gate("G5", f1 and f"{f1[2]},{f1[4]},{f1[5]},{f1[6]}" == v, f"{k} raw anchor mismatch")

# G6: head freshness
head = os.path.join(KIT, "head.cache")
if not os.path.exists(head):
    import glob
    cand = glob.glob(os.path.join(os.path.dirname(KIT), "..", "head.cache"))
    head = cand[0] if cand else os.path.join(KIT, "input", "head.cache")
h = open(head, "rb").read()
hsha = hashlib.sha256(h).hexdigest()
gate("G6", hsha.startswith(rows["head_basis"]["sha256_prefix"]), f"head sha {hsha}")
lines = h.decode().strip().split("\n")
gate("G6", len(lines) - 1 == rows["head_basis"]["rows"], f"head rows {len(lines)-1}")
for k, t in targets.items():
    lo, hi = t["key"].split(":")
    gate("G6", not any(l.startswith(f"s5verdict,{lo},{hi},") for l in lines),
         f"{k} present in head")

if fail:
    print("AUDIT-FAIL")
    for f in fail: print("  " + f)
    sys.exit(1)
print(json.dumps({"verdict": "AUDIT-PASS", "gates": "G0-G6", "rows": len(status),
                  "targets": sorted(targets), "head_sha256": hsha,
                  "target_keys": {k: t["key"] for k, t in targets.items()},
                  "expected": {k: t["expected"] for k, t in targets.items()}}))
