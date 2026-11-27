#!/usr/bin/env python3
# Part SS (k38 L50M follow-up LOSS row) C++ scrutiny gate audit.
# Fresh single-row implementation of the EN/EO/EQ/ET/SK/SM/SN/SR gate checks
# (NOT a byte-transform of the SR audit script; disclosed in README/declaration):
# G1 kit pins (inputs, gate-rows.json, runner), G2 raw presence/completeness,
# G3 p1==p2==expected per row, G4 phantom/status consistency,
# G5 target freshness vs the canonical head, G0 environment pins.
# Fail-closed: any gate failing exits rc=1 after writing audit_gate.json.
import hashlib, json, os, sys

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROWS = json.load(open(os.path.join(DIR, "input", "gate-rows.json")))

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def fields(rawpath):
    """Return (legal,budget,result,nodes) of the single replay row, or None."""
    for line in open(rawpath):
        if line.startswith("replay,"):
            p = line.strip().split(",")
            return ",".join([p[3], p[5], p[6], p[7]])
    return None

gates = {}

def gate(name, ok, detail=""):
    gates[name] = {"status": "PASS" if ok else "FAIL", "detail": detail}
    return ok

# G0: gate-rows schema and pin structure
ok = (ROWS["schema"] == "n11-sixthcost-k38-l50m-cppgate-rows-v1"
      and ROWS["part"] == "SS"
      and set(ROWS["targets"]) == {"k38"}
      and set(ROWS["anchors"]) == {"anchor-at2m", "anchor-aj001", "anchor-af039"})
gate("G0:schema-pins", ok)

# G1: kit input byte pins (k38 input = published sixth-cost probe kit input clone)
inpins = {
    "k38.input.csv": "b6ef9f439ee0b6c9a35af08ff065a9323d0bec627beabb4defb9426a11d6600e",
    "anchor-at2m.input.csv": "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
    "anchor-aj001.input.csv": "2f6daea5ca3b3fe6b7713c8d450af3f3c9f203acacb8a1340255d8e8f656496c",
    "anchor-af039.input.csv": "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691",
    "gate-rows.json": None,  # pin checked by presence only (this file is the SSOT)
    "../scripts/gate_runner.sh": None,
}
ok = True
detail = []
for name, pin in inpins.items():
    p = os.path.join(DIR, "input", name) if not name.startswith("..") else os.path.join(DIR, "scripts", "gate_runner.sh")
    if not os.path.isfile(p):
        ok = False; detail.append("missing " + name); continue
    if pin is not None and sha(p) != pin:
        ok = False; detail.append("sha-mismatch " + name)
gate("G1:input-pins", ok, "; ".join(detail))

# G2/G3: raws exist, complete, deterministic, node-exact vs expectations
allrows = dict(ROWS["anchors"]); allrows.update(ROWS["targets"])
ok = True; detail = []
for key, expected in sorted(allrows.items()):
    for p in ("p1", "p2"):
        raw = os.path.join(DIR, "output", "raw", key + "." + p + ".out")
        if not os.path.isfile(raw):
            ok = False; detail.append("missing raw " + key + "." + p); continue
        if "# replay_done" not in open(raw).read():
            ok = False; detail.append("truncated " + key + "." + p); continue
        f = fields(raw)
        if f is None:
            ok = False; detail.append("no replay row " + key + "." + p); continue
        if f != expected:
            ok = False; detail.append("quadruple %s.%s=%s expected=%s" % (key, p, f, expected))
gate("G2:raw-completeness", ok, "; ".join([d for d in detail if "missing" in d or "truncated" in d or "no replay" in d]))
gate("G3:quadruple-match", ok, "; ".join([d for d in detail if "quadruple" in d]))

# G4: no phantom raws; status log has exactly one GATE-PASS line per row, no FAIL/MISMATCH
rawdir = os.path.join(DIR, "output", "raw")
expected_names = sorted([k + "." + p + ".out" for k in allrows for p in ("p1", "p2")])
actual_names = sorted(os.listdir(rawdir))
phantoms = sorted(set(actual_names) - set(expected_names))
gate("G4:no-phantom-raws", not phantoms, "phantoms=" + ",".join(phantoms))
statusp = os.path.join(DIR, "output", "gate-status.log")
sl = open(statusp).read().splitlines() if os.path.isfile(statusp) else []
passes = [l for l in sl if "GATE-PASS" in l]
bad = [l for l in sl if ("GATE-FAIL" in l or "MISMATCH" in l or "GATE-CRASH" in l or "TRUNCATED" in l)]
ok = (len(passes) == len(allrows) and not bad
      and all((" " + k + " GATE-PASS ") in sl_text for k in allrows for sl_text in ["".join(l + "\n" for l in sl)]))
gate("G4:status-log", ok, "passes=%d expected=%d bad=%d" % (len(passes), len(allrows), len(bad)))

# G5: freshness - the k38 [lo,hi] pair absent from the canonical head of record
cache = os.path.join(DIR, "input", "canonical-head.cache")
if not os.path.isfile(cache):
    cache = None
    for cand in (os.path.join(DIR, "..", "canonical.cache"), "/home/user/k38/canonical.cache"):
        if os.path.isfile(cand):
            cache = cand; break
ok = cache is not None and sha(cache) == ROWS["canonical_head"]["sha256"]
detail = "cache=" + str(cache)
if ok:
    content = open(cache).read()
    pair = "10376293541461626880,66048"
    ok = pair not in content
    detail += " pair-absent=" + str(ok)
gate("G5:target-fresh-vs-02db5ab3", ok, detail)

result = {
    "schema": "n11-sixthcost-k38-l50m-cppgate-audit-v1",
    "part": "SS",
    "gates": gates,
    "rc": 0 if all(g["status"] == "PASS" for g in gates.values()) else 1,
}
out = os.path.join(DIR, "output", "audit_gate.json")
with open(out, "w") as f:
    json.dump(result, f, indent=1, sort_keys=True)
    f.write("\n")
print("audit rc=%d gates=%d" % (result["rc"], len(gates)))
for k, v in sorted(gates.items()):
    if v["status"] != "PASS":
        print("FAIL %s %s" % (k, v["detail"]))
sys.exit(result["rc"])
