#!/usr/bin/env python3
"""Eighth-cost k01 WIN row (1297036692750860288:64) C++ scrutiny gate kit
maker (2026-11-27).

Assembles the fail-closed kit for the delegated pinned C++
second-implementation scrutiny gate on the SINGLE eighth-cost WIN row k01
(key 1297036692750860288:64, published resolution 84,15000000,1,8514427,
at15m cold pair both sha256 3be9db9b76f5dbd2756ffe51a2eb4e2c62c09f12d
6999f7bc9a0376075479062). Part SX (seventh-cost k05 L50M WIN row)
precedent: single target + 3 calibration anchors, fresh single-row audit
(disclosed), publish-then-execute under the wave-A declaration
(research/log/2026-11-27-n11-eighthcost-k01-win-cppgate-declaration.md).

Structural-clone disclosure vs the published Part SX maker: deltas are
(1) part/schema strings; (2) the target set is the single k01 row with
pins machine-read from the published eighth-cost kit (input manifest pin)
and the published at15m raw pair (sha-verified 3be9db9b x2), plus the
published at2m UNKNOWN stage raws (stage policy: the 15M escalation was
declared after the published 2M UNKNOWN raws); (3) the runner transform
is the published SX runner with the comment block only (machine-verified
diff = 2 comment lines); the audit is a FRESH single-row implementation
(the Part SS/SX precedent, disclosed); (4) the expected quadruple has
result=1 (WIN), the second WIN-side row of the C++ gate lineage after
SX. No gate added, removed, or weakened. The third-implementation
corroboration of this row is ALREADY PUBLISHED (CORROBORATION-PASS,
third_impl 08ea958f), so a GATE-PASS here brings k01 to implementation-
pillar parity with the k05 precedent (adoption stays a separate Part).

Gates (all must PASS; any failure -> rc=1, no emit):
  G0  gate source pins (kyouen_dfpn_root.cpp 9193f5b6... @ 154f3b7a...,
      headers 5976935d... / 2e36d694...); SW kit gate-rows.json read
      (anchors authority).
  G1  k01 SSOT: kit input sha == published eighth-cost kit
      MANIFEST-sha256.txt pin; published at15m raw pair sha-verified
      (3be9db9b x2); cold-pair identity on every replay field except
      wall_s; expected quadruple derived from raw run1 == 84,15000000,
      1,8514427; budget 15000000; result 1 (WIN); the 2M UNKNOWN stage
      raws are also pinned.
  G2  cross-SSOT: canonical head 5b6e77f7 sha-verified (6,874 s5verdict
      rows WIN202/LOSS6672) with the k01 [lo,hi] pair ABSENT
      (verdict-unconsumed); anchors quadruples == the published SW kit
      anchors block; anchor inputs byte-clones of the published SW kit
      inputs.
  G3  runner == published SX runner transform (comment block only,
      machine-verified).

No verdict is consumed. The k01 WIN row stays a gate-verified UNCONSUMED
label. The standard 11x11 empty board, every root, S2, class 1/2/4 and
all closure classes stay UNKNOWN. Nodes are bookkeeping, never verdicts.
"""
import hashlib, json, os, pathlib, subprocess, sys

KIT = pathlib.Path(__file__).resolve().parent.parent
SSOT = pathlib.Path(os.environ.get("K01_SSOT", str(KIT.parent / "ssot")))

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
    "label": "5b6e77f7",
    "sha256": "5b6e77f7d7832d4ce84cb1f080a93e066eb052dcf8b817e5d560f95499fcdde2",
    "rows": 6874, "WIN": 202, "LOSS": 6672,
}
SW_KIT_SCHEMA = "n11-seventhcost-41loss-cppgate-rows-v1"
E8_KIT = "research/experiments/n11-eighthcost-class-s5-exclusive-probe-1297036692750860288-20261127"
K01 = {"key": "1297036692750860288:64", "lo": "1297036692750860288", "hi": "64",
       "input_pin": "a5a18d5e057d7ad87dca39dd17a28057c68554ebb16e40b02d080e50580f923b",
       "raw_pair_sha": "3be9db9b76f5dbd2756ffe51a2eb4e2c62c09f12d6999f7bc9a0376075479062",
       "budget": "15000000"}
EXPECT = "84,15000000,1,8514427"
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

# G1: k01 SSOT
kin = KIT / "input" / "k01.input.csv"
ok &= gate("G1:k01-input-present", kin.is_file())
ok &= gate("G1:k01-input-sha==published-manifest-pin", kin.is_file() and sha256(kin) == K01["input_pin"], sha256(kin) if kin.exists() else "")
spec = kin.read_text().strip() if kin.exists() else ""
ok &= gate("G1:k01-input-row-spec-shape", spec == "target,0,5,1297036692750860288,64,84,0,0,0,0,0", spec)
r1 = SSOT / "e8" / "at15m-run1.k01.out.csv"
r2 = SSOT / "e8" / "at15m-run2.k01.out.csv"
ok &= gate("G1:k01-raw-run1-sha==3be9db9b", r1.is_file() and sha256(r1) == K01["raw_pair_sha"], sha256(r1) if r1.exists() else "missing")
ok &= gate("G1:k01-raw-run2-sha==3be9db9b", r2.is_file() and sha256(r2) == K01["raw_pair_sha"], sha256(r2) if r2.exists() else "missing")
f1, f2 = replay_fields(r1), replay_fields(r2)
ok &= gate("G1:k01-cold-pair-identity-except-wall", f1 and f2 and f1[:8] == f2[:8] and f1[8:] == f2[8:], "%s vs %s" % (",".join(f1 or []), ",".join(f2 or [])))
quad = ",".join([f1[3], f1[5], f1[6], f1[7]]) if f1 else ""
ok &= gate("G1:k01-expected-quadruple-from-raw", quad == EXPECT, "%s expected %s" % (quad, EXPECT))
ok &= gate("G1:k01-win-inside-budget", f1 and f1[6] == "1" and int(f1[7]) <= int(K01["budget"]), "")
s1 = SSOT / "e8" / "at2m-run1.k01.out.csv"
s2 = SSOT / "e8" / "at2m-run2.k01.out.csv"
fs1, fs2 = replay_fields(s1), replay_fields(s2)
ok &= gate("G1:k01-stage-policy-2m-unknown", fs1 and fs1[6] == "0" and fs1[7] == "2000000" and fs2 and fs2[6] == "0" and fs2[7] == "2000000", "%s" % (",".join(fs1 or []) if fs1 else "missing"))

# G2: cross-SSOT
head = SSOT / "head5b6e.cache"
ok &= gate("G2:canonical-head-sha", head.is_file() and sha256(head) == CANONICAL_HEAD["sha256"], sha256(head) if head.exists() else "missing")
lines = head.read_text().splitlines()
data = [l for l in lines if l.startswith("s5verdict,")]
wins = sum(1 for l in data if l.split(",")[4] == "1")
losses = sum(1 for l in data if l.split(",")[4] == "2")
ok &= gate("G2:canonical-head-census", len(data) == CANONICAL_HEAD["rows"] and wins == CANONICAL_HEAD["WIN"] and losses == CANONICAL_HEAD["LOSS"],
           "rows=%d WIN=%d LOSS=%d" % (len(data), wins, losses))
absent = not any(l.split(",")[1] == K01["lo"] and l.split(",")[2] == K01["hi"] for l in data)
ok &= gate("G2:freshness-k01-absent", absent, "k01 must be absent from 5b6e77f7")
ok &= gate("G2:anchors==sw-kit", sw_rows.get("anchors") == ANCHORS, sw_rows.get("anchors"))
for a, pin in ANCHOR_PINS.items():
    p = KIT / "input" / (a + ".input.csv")
    ok &= gate("G2:%s:input==sw-kit-byte-clone" % a, p.is_file() and sha256(p) == pin, sha256(p) if p.exists() else "missing")

# G3: runner transform (comment block only) vs published SX runner
runner = (KIT / "scripts" / "gate_runner.sh").read_text()
sx_runner = (SSOT / "sx" / "gate_runner.sh").read_text()
r_lines, s_lines = runner.splitlines(), sx_runner.splitlines()
body_r = [l for l in r_lines if not l.startswith("#") and l.strip()]
body_s = [l for l in s_lines if not l.startswith("#") and l.strip()]
ok &= gate("G3:runner-transform-comment-only", body_r == body_s, "noncomment bodies identical")

print(json.dumps({"gates": gates, "overall": "PASS" if ok else "FAIL"}, indent=1, sort_keys=True))
if not ok:
    for k, v in sorted(gates.items()):
        if v["status"] == "FAIL":
            print("FAIL", k, v["detail"])
    sys.exit(1)

# emit gate-rows.json
rows = {
    "part": "eighth-cost k01 WIN row C++ scrutiny gate",
    "schema": "n11-eighthcost-k01-win-cppgate-rows-v1",
    "gate_source": GATE_SOURCE,
    "canonical_head": {
        "label": CANONICAL_HEAD["label"],
        "sha256": CANONICAL_HEAD["sha256"],
        "rows": CANONICAL_HEAD["rows"], "WIN": CANONICAL_HEAD["WIN"], "LOSS": CANONICAL_HEAD["LOSS"],
        "targets_fresh_vs": CANONICAL_HEAD["label"],
        "path": "research/experiments/n11-seventhcost-sz-adoption-20261127/output/merged/merged-exact-s5-chain-plus-seventhcost42-20261127.cache",
    },
    "anchors": ANCHORS,
    "anchors_runtime": {a: [ANCHORS[a].split(",")[1], ANCHORS[a]] for a in ANCHORS},
    "target": {"k01": {
        "budget": K01["budget"], "expected": EXPECT,
        "lo": K01["lo"], "hi": K01["hi"], "legal": "84",
        "input_sha256": K01["input_pin"], "raw_pair_sha256": K01["raw_pair_sha"],
        "raw_provenance": E8_KIT + "/output/raw/at15m-run1/k01.out.csv",
        "replica_verdict": 1,
    }},
    "third_impl": {
        "exists": True,
        "note": "published CORROBORATION-PASS (third_impl 08ea958f, WIN(1) expansions 9987963 x2 identical cold passes) precedes this gate; a GATE-PASS brings k01 to replica+C+++third-impl pillar parity",
    },
    "gates": gates,
}
(KIT / "input" / "gate-rows.json").write_text(json.dumps(rows, indent=1, sort_keys=True) + "\n")

# emit MANIFEST-sha256.txt over kit files present now
man = []
for p in sorted(KIT.rglob("*")):
    if p.is_file() and p.name not in ("MANIFEST-sha256.txt",):
        man.append("%s %d %s" % (sha256(p), p.stat().st_size, str(p.relative_to(KIT))))
(KIT / "MANIFEST-sha256.txt").write_text("\n".join(man) + "\n")
print("EMIT input/gate-rows.json MANIFEST-sha256.txt")
