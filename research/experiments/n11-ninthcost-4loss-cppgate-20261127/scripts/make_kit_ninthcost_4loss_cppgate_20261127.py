#!/usr/bin/env python3
"""Ninth-cost 4 LOSS row (k01/k03/k05/k06) C++ scrutiny gate maker (2026-11-27).

Machine-derives the gate rows for the four published ninth-cost at15m
LOSS rows of the exclusive S5 probe class 1297036692683751424:134217728
(kit research/experiments/n11-ninthcost-class-s5-exclusive-probe-
1297036692683751424-20261127, wave C6 commit 95883e09) and emits
input/gate-rows.json (schema n11-ninthcost-4loss-cppgate-rows-v1).

Adaptation of the eighth-cost single-row maker (10549-byte kit script,
disclosed as a structural adaptation; the batch form follows the SW
precedent). Disclosed: expected quadruples are machine-derived from the
published at15m run1 raws, cold-pair identity is re-verified on every
replay field except wall_s, and the 2M UNKNOWN stage raws of all four
keys are pinned (stage policy: the 15M escalations were published after
the wave C5 2M UNKNOWN sweep).

No verdict is consumed. The four LOSS rows stay gate-verified UNCONSUMED
labels. The standard 11x11 empty board, every central-reply root, the
two-stone root {60,27}, its remaining third moves {100,108}, S2, class
1/2/4 and all closure classes stay UNKNOWN. Nodes are bookkeeping, never
verdicts.

Gates (all must PASS; any failure -> rc=1, no emit):
  G0  gate source pins (kyouen_dfpn_root.cpp 9193f5b6... @ 154f3b7a...,
      headers 5976935d... / 2e36d694...); SW kit gate-rows.json read
      (anchors authority).
  G1  per-target SSOT: kit input sha == published ninth-cost kit
      MANIFEST-sha256.txt pin; published at15m raw pair quad-identical
      (every replay field except wall_s); expected quadruple derived
      from the run1 raw; budget 15000000; result 2 (LOSS); the 2M
      UNKNOWN stage raw pair pinned byte-identical per key.
  G2  canonical head 0935c94c sha-verified (6,875 s5verdict rows
      WIN203/LOSS6672) with all four [lo,hi] pairs ABSENT
      (verdict-unconsumed); anchors quadruples == the published SW kit
      anchors block; anchor inputs byte-clones of the published SW kit
      inputs.
  G3  kit runner == published SX runner transform (comment block only,
      machine-verified: code lines identical).
"""
import hashlib, json, os, pathlib, subprocess, sys

KIT = pathlib.Path(__file__).resolve().parent.parent
SSOT = pathlib.Path(os.environ.get("N9_SSOT", str(KIT.parent / "ssot")))

GATE_SOURCE = {
    "commit": "154f3b7a67b97e13acbaee8b04dc74ddca728d19",
    "path": "cpp/solvers/kyouen_dfpn_root.cpp",
    "sha256": "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e",
    "header_pins": {
        "kyouen_residual_micro.hpp": "5976935dcfccb9b5a26fa68f8de20868ce45363dd8c372dcd67d9b841167e7f5",
        "n11_s5_quarantine.hpp": "2e36d69481fafcde7aede8ae4fedf3d5477f91ee9846bcd4ae2975f32a4ba1a5",
    },
}
CANONICAL_HEAD = {
    "label": "0935c94c",
    "sha256": "0935c94c03a9a3fbdf2a55aca90bb986a019dfd26c0097ab2c75709d590e9ca4",
    "rows": 6875, "WIN": 203, "LOSS": 6672,
    "path": "research/experiments/n11-eighthcost-k01-win-adoption-20261127/output/merged-exact-s5-chain-plus-eighthcost-k01-20261127.cache",
}
SW_KIT_SCHEMA = "n11-seventhcost-41loss-cppgate-rows-v1"
N9_KIT = "research/experiments/n11-ninthcost-class-s5-exclusive-probe-1297036692683751424-20261127"
BUDGET = "15000000"
TARGETS = {
    "k01": {"lo": "1297036692683751424", "hi": "134283264",
            "input_pin": "5768229a7bc3b5e719b57456e710b4250990f42f75336018eacb4fe3484400c7"},
    "k03": {"lo": "1297036761403228160", "hi": "134217728",
            "input_pin": "3b33982dea100bcb4f17229b35526052b3a349b4e1a2981701a087c8234385cc"},
    "k05": {"lo": "1152921504624672768", "hi": "536903680",
            "input_pin": "ed29fa0fe1fcebad260474c42ff473f7b95be1b4a5b1c77a60222e813e72fd67"},
    "k06": {"lo": "1152923703764321280", "hi": "68719476736",
            "input_pin": "ed853a05bbee7734d30abe89dfaae1b6f4d0329904741ec4b964c060d0c53cac"},
}
ANCHOR_PINS = {
    "anchor-af039": "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691",
    "anchor-aj001": "2f6daea5ca3b3fe6b7713c8d450af3f3c9f203acacb8a1340255d8e8f656496c",
    "anchor-at2m": "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
}
ANCHORS = {
    "anchor-at2m": "98,2000000,0,2000000",
    "anchor-aj001": "84,30000000,2,5156075",
    "anchor-af039": "89,30000000,2,19234232",
}

def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def replay_fields(path):
    for line in pathlib.Path(path).read_text().splitlines():
        if line.startswith("replay,"):
            return line.split(",")
    return None

gates = {}
def gate(name, ok, detail=""):
    gates[name] = {"status": "PASS" if ok else "FAIL", "detail": str(detail)}
    return bool(ok)

ok = True

# G0: gate source pins
for name, pin in [("kyouen_dfpn_root.cpp", GATE_SOURCE["sha256"])] + list(GATE_SOURCE["header_pins"].items()):
    p = SSOT / "gsrc" / name
    ok &= gate("G0:" + name, p.is_file() and sha256(p) == pin, sha256(p) if p.is_file() else "missing")
sw_rows = json.loads((SSOT / "sw" / "gate-rows.json").read_text())
ok &= gate("G0:sw-kit-gate-rows-read", sw_rows.get("schema") == SW_KIT_SCHEMA, sw_rows.get("schema"))
ok &= gate("G0:sw-anchors", sw_rows.get("anchors") == ANCHORS, sw_rows.get("anchors"))

# G1: per-target SSOT from the published ninth-cost kit raws
n9 = SSOT / "n9"
targets = {}
for key, meta in TARGETS.items():
    inp = KIT / "input" / (key + ".input.csv")
    isha = sha256(inp) if inp.is_file() else "missing"
    ok &= gate("G1:%s:input-pin" % key, isha == meta["input_pin"], isha)
    r1 = replay_fields(n9 / (key + ".at15m-run1.out.csv"))
    r2 = replay_fields(n9 / (key + ".at15m-run2.out.csv"))
    ok &= gate("G1:%s:at15m-pair" % key, r1 is not None and r2 is not None and r1[:8] == r2[:8] and r1[9:] == r2[9:],
               "run1=%s run2=%s" % (r1, r2))
    quad = ",".join([r1[3], r1[5], r1[6], r1[7]])
    ok &= gate("G1:%s:expected" % key,
               r1[5] == BUDGET and r1[6] == "2" and r1[9] == meta["lo"] and r1[10] == meta["hi"],
               "budget=%s result=%s key=%s:%s" % (r1[5], r1[6], r1[9], r1[10]))
    ok &= gate("G1:%s:at2m-stage" % key,
               sha256(n9 / (key + ".at2m-run1.out.csv")) == sha256(n9 / (key + ".at2m-run2.out.csv")),
               "2M stage raw pair not byte-identical")
    s1 = replay_fields(n9 / (key + ".at2m-run1.out.csv"))
    ok &= gate("G1:%s:at2m-unknown" % key, s1[5] == "2000000" and s1[6] == "0" and s1[7] == "2000000", "stage raw %s" % s1)
    targets[key] = {
        "expected": quad, "budget": BUDGET, "lo": meta["lo"], "hi": meta["hi"],
        "input_sha256": isha,
        "at15m_run1_sha256": sha256(n9 / (key + ".at15m-run1.out.csv")),
        "at15m_run2_sha256": sha256(n9 / (key + ".at15m-run2.out.csv")),
        "at2m_run1_sha256": sha256(n9 / (key + ".at2m-run1.out.csv")),
        "raws_path": N9_KIT + "/output/raw",
    }

# G2: canonical head freshness (all four absent) + anchor clones
head = SSOT / "head" / "merged.cache"
ok &= gate("G2:head-sha", head.is_file() and sha256(head) == CANONICAL_HEAD["sha256"], sha256(head) if head.is_file() else "missing")
data = [l for l in head.read_text().splitlines() if l.startswith("s5verdict,")]
wins = sum(1 for l in data if l.split(",")[4] == "1")
losses = sum(1 for l in data if l.split(",")[4] == "2")
ok &= gate("G2:head-census", len(data) == CANONICAL_HEAD["rows"] and wins == CANONICAL_HEAD["WIN"] and losses == CANONICAL_HEAD["LOSS"],
           "rows=%d WIN=%d LOSS=%d" % (len(data), wins, losses))
present = [k for k, m in TARGETS.items() if any(l.split(",")[1] == m["lo"] and l.split(",")[2] == m["hi"] for l in data)]
ok &= gate("G2:freshness-absent", not present, "present=%s" % present)
for a, pin in ANCHOR_PINS.items():
    p = KIT / "input" / (a + ".input.csv")
    ok &= gate("G2:%s:clone" % a, p.is_file() and sha256(p) == pin, sha256(p) if p.is_file() else "missing")

# G3: kit runner code-identical to the published SX runner (comment block only)
pub = (SSOT / "sx_runner.sh").read_text().splitlines()
mine = (KIT / "scripts" / "gate_runner.sh").read_text().splitlines()
code_pub = [l for l in pub if not l.lstrip().startswith("#")]
code_mine = [l for l in mine if not l.lstrip().startswith("#")]
ok &= gate("G3:runner-code-identical", code_pub == code_mine, "sx=%d lines, kit=%d lines" % (len(code_pub), len(code_mine)))

out = {
    "schema": "n11-ninthcost-4loss-cppgate-rows-v1",
    "part": "ninth-cost 4 LOSS row C++ scrutiny gate (k01/k03/k05/k06 of class 1297036692683751424:134217728)",
    "gate_source": GATE_SOURCE,
    "canonical_head": CANONICAL_HEAD,
    "anchors": ANCHORS,
    "anchors_runtime": {a: [ANCHORS[a].split(",")[1], ANCHORS[a]] for a in ANCHORS},
    "targets": targets,
    "target_runtime": {k: [v["budget"], v["expected"]] for k, v in targets.items()},
    "rows": len(ANCHORS) + len(TARGETS),
    "gates": gates,
    "overall": "PASS" if ok else "FAIL",
}
if ok:
    with open(KIT / "input" / "gate-rows.json", "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    print("maker: PASS (%d gates, %d rows)" % (len(gates), out["rows"]))
else:
    print("maker: FAIL")
    for k, v in sorted(gates.items()):
        if v["status"] == "FAIL":
            print("FAIL", k, v["detail"])
sys.exit(0 if ok else 1)
