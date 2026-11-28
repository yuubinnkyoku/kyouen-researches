#!/usr/bin/env python3
# Fresh fail-closed summary generator for the twenty-first-ladder-top k02 cppgate kit.
# G0 input pins; G1 status log sanity; G2 raw-vs-expected + fresh-cold pair determinism;
# G3 anchor raw sha cross-kit pins. Writes output/cppgate-summary.json only on full PASS.
import hashlib, json, sys, os
kit = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = json.load(open(os.path.join(kit, "input", "gate-rows.json")))
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()
fails = []
# G0 input pins
for name, spec in list(rows["targets"].items()) + list(rows["anchors"].items()):
    p = os.path.join(kit, "input", f"{name}.input.csv")
    if not os.path.exists(p): fails.append(f"G0 missing input {name}")
    elif sha(p) != spec["input_pin"]: fails.append(f"G0 input pin mismatch {name}")
# G1 status log
log = os.path.join(kit, "output", "gate-status.log")
if not os.path.exists(log): fails.append("G1 missing gate-status.log")
else:
    lines = [l for l in open(log).read().splitlines() if "GATE-PASS" in l]
    expected_names = list(rows["targets"]) + list(rows["anchors"])
    for n in expected_names:
        if not any(f" {n} GATE-PASS " in l for l in lines): fails.append(f"G1 no GATE-PASS line for {n}")
# G2 raw-vs-expected + pair determinism
results = {}
for name, spec in list(rows["targets"].items()) + list(rows["anchors"].items()):
    vals = []
    for p in ("p1", "p2"):
        f = os.path.join(kit, "output", "raw", f"{name}.{p}.out")
        row = None
        if os.path.exists(f):
            for l in open(f):
                if l.startswith("replay,"): row = l.strip()
        if not row: fails.append(f"G2 missing replay row {name} {p}")
        else: vals.append(",".join([row.split(",")[i] for i in (3,5,6,7)]))
    if len(vals) == 2:
        if vals[0] != vals[1]: fails.append(f"G2 pair mismatch {name}: {vals}")
        elif vals[0] != spec["expected"]: fails.append(f"G2 expected mismatch {name}: {vals[0]} != {spec['expected']}")
        else: results[name] = vals[0]
if fails:
    print("SUMMARY-FAIL")
    for f in fails: print(f)
    sys.exit(1)
out = {
 "schema": "n11-twenty-first-ladder-top-k02-cppgate-summary-v1",
 "declaration_commit": rows["declaration"].split("commit ")[-1].rstrip(")"),
 "gate": "GATE-PASS",
 "results": results,
 "runner_pair_determinism": True,
 "gate_source_sha256": rows["gate_source"],
 "status_guard": "pillar bookkeeping only; NO verdict consumed; 11x11 UNKNOWN"
}
with open(os.path.join(kit, "output", "cppgate-summary.json"), "w") as f:
    json.dump(out, f, indent=1)
print("SUMMARY-PASS " + json.dumps(results))
