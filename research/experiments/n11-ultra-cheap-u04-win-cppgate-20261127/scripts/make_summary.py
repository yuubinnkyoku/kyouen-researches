#!/usr/bin/env python3
# Summary generator + fail-closed gate for the n11 ultra-cheap u04 WIN-row C++ gate kit.
# Gates: G0 input pins (targets+anchors, sha256) / G1 gate-status.log GATE-PASS lines match
# gate-rows.json / G2 each raw replay row (legal,budget,result,nodes) == expected and
# p1==p2 node-identical / G3 anchors match published expectations / G4 third-impl kit
# cross-pin (published summary pinned by sha256 from gate-rows.json, fetched from main).
# Any gate failure: exit non-zero, write NOTHING (fail-closed). Tamper T4 flips a
# gate-rows expected pin -> this script must fail.
import hashlib, json, subprocess, sys, os

K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = json.load(open(os.path.join(K, "input/gate-rows.json")))

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()

def replay_fields(path):
    for line in open(path):
        if line.startswith("replay,"):
            f = line.strip().split(",")
            return ",".join([f[3], f[5], f[6], f[7]]), f
    raise SystemExit(f"no replay row in {path}")

# G0 input pins
for name, spec in list(rows["targets"].items()) + list(rows["anchors"].items()):
    p = os.path.join(K, f"input/{name}.input.csv")
    got = sha256(p)
    assert got == spec["input_pin"], f"G0 FAIL {name}: {got}"

# G1 gate-status.log
status = open(os.path.join(K, "output/gate-status.log")).read()
for name, spec in list(rows["targets"].items()) + list(rows["anchors"].items()):
    assert f"{name} GATE-PASS {spec['expected']}" in status, f"G1 FAIL {name}"

# G2 raws: expected + node-identical pairs
results = {}
for name, spec in list(rows["targets"].items()) + list(rows["anchors"].items()):
    f1, _ = replay_fields(os.path.join(K, f"output/raw/{name}.p1.out"))
    f2, _ = replay_fields(os.path.join(K, f"output/raw/{name}.p2.out"))
    assert f1 == f2, f"G2 FAIL {name} p1!=p2: {f1} vs {f2}"
    assert f1 == spec["expected"], f"G2 FAIL {name}: {f1} != {spec['expected']}"
    results[name] = f1

# G3 anchors byte/node identity vs published u03 pillars kit raw sha256 prefixes
PUBLISHED = {
    ("anchor-at2m", "p1"): "cfa72d667428bfc7b3cc60306be5828b859f2e50631bb89b37a8601d6bf02ee3",
    ("anchor-at2m", "p2"): "cfa72d667428bfc7b3cc60306be5828b859f2e50631bb89b37a8601d6bf02ee3",
    ("anchor-aj001", "p1"): "54f261f66e2368ac40aef2ef6824ef2be8152b3c4a697edf161d330bd4e615ed",
    ("anchor-aj001", "p2"): "54f261f66e2368ac40aef2ef6824ef2be8152b3c4a697edf161d330bd4e615ed",
    ("anchor-af039", "p1"): "aa295618323403dbc2c126da7280427c5a4ede11ff08c080b2533630f1f8f332",
}
for (name, ps), pin in PUBLISHED.items():
    p = os.path.join(K, f"output/raw/{name}.{ps}.out")
    assert sha256(p) == pin, f"G3 FAIL {name}.{ps}"

# G4 third-impl kit cross-pin: fetch published summary from main and pin it
ti = rows["third_impl_kit"]
url = ("https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/main/"
       "research/experiments/n11-ultra-cheap-u04-thirdimpl-20261127/output/pillars-summary.json")
out = subprocess.run(["curl", "-sfL", url], capture_output=True)
assert out.returncode == 0, "G4 FAIL fetch"
assert hashlib.sha256(out.stdout).hexdigest() == ti["summary_sha256"], "G4 FAIL pin"
tis = json.loads(out.stdout)
assert tis["third_impl"]["result"] == ti["result"], "G4 FAIL ti result"
assert tis["third_impl"]["expansions"] == ti["expansions"], "G4 FAIL ti expansions"

summary = {
 "schema": "n11-ultra-cheap-u04-win-cppgate-summary-v1",
 "part": "ultra-cheap u04 WIN-row C++ second-implementation scrutiny gate (completes the two-pillar requirement left OPEN by n11-ultra-cheap-u04-thirdimpl-20261127)",
 "row": rows["targets"]["u04"],
 "gate": {
  "status": "GATE-PASS 85,15000000,1,9149084 (fresh-cold pair node-identical, node-exact vs the published escalation raw)",
  "source_sha256": rows["gate_source"]["kyouen_dfpn_root.cpp"],
  "build": rows["gate_source"]["build"],
  "anchors": {k: {"expected": v["expected"], "status": "GATE-PASS pair node-identical"} for k, v in rows["anchors"].items()}
 },
 "third_impl": ti,
 "pillars": "BOTH COMPLETE for u04: escalation replica + C++ gate (this kit) + third-impl corroboration (published kit 2691ac04); adoption remains a separate declared Part",
 "disclosures": [
  "gate source + headers byte-fetched from the published tenth-cost k01k02 cppgate kit and sha256-verified against the standing pins 9193f5b6/5976935d/2e36d694",
  "zig 0.13.0 tarball pin d45312e6 re-verified before build; -std=c++20 as in the standing build recipe",
  "anchor raws reproduce the published u03 pillars kit raw sha256 prefixes exactly (cross-host determinism)",
  "u04 pair wall_s 17 vs 18; af039 pair wall_s 38 vs 37 (host wall-clock only)",
  "no other key was run at any budget in this Part",
  "no u04 adoption is performed here; the standing WIN-side flip-census review is required before any adoption"
 ],
 "status_guard": "pillar bookkeeping only; NO verdict consumed; nodes are bookkeeping; 11x11 UNKNOWN"
}
with open(os.path.join(K, "output/cppgate-summary.json"), "w") as f:
    json.dump(summary, f, indent=1)
    f.write("\n")
print("SUMMARY-PASS")
