#!/usr/bin/env python3
"""Part SX (seventh-cost k05 L50M WIN row) C++ scrutiny gate kit maker
(2026-11-27).

Assembles the fail-closed kit for the delegated pinned C++
second-implementation scrutiny gate on the SINGLE seventh-cost
parked-then-L50M WIN row k05 (key 1152921504607932416:536870912, published
resolution 90,50000000,1,15763505, cold pair both sha256 ff750cc6...).
Part SS (k38 L50M single WIN-side... LOSS row) precedent: single target +
3 calibration anchors, fresh single-row audit (disclosed), publish-then-
execute under the wave-A declaration.

Structural-clone disclosure vs the published Part SW maker: deltas are
(1) part/schema strings; (2) the target set is the single k05 row with
pins machine-read from the published seventh-cost kit (input manifest pin)
and the published at50m raw pair (sha-verified ff750cc6); (3) the
runner/audit templates are the published Part SW kit (runner transform =
comment block only; the audit is a FRESH single-row implementation, not a
byte transform - the Part SS precedent, disclosed); (4) the expected
quadruple has result=1 (WIN), the first WIN-side row of the C++ gate
lineage since EV/SN. No gate added, removed, or weakened.

Gates (all must PASS; any failure -> rc=1, no kit emit):
  G0  gate source pins machine-read from the published SW kit
      gate-rows.json (cpp/solvers/kyouen_dfpn_root.cpp 9193f5b6... @
      154f3b7a..., headers 5976935d... / 2e36d694...).
  G1  k05 SSOT: kit input sha == published seventh-cost kit
      MANIFEST-sha256.txt pin; published at50m raw pair sha-verified
      (ff750cc6 x2); cold-pair identity on every replay field except
      wall_s; expected quadruple derived from raw run1; budget 50000000;
      result 1 (WIN) - the 15M/2M UNKNOWN stage raws are also pinned
      (stage policy: the 50M escalation was declared after the published
      2M/15M UNKNOWN raws).
  G2  cross-SSOT: canonical head 42dbb58f sha-verified (6,832 s5verdict
      rows WIN201/LOSS6631) with the k05 [lo,hi] pair ABSENT
      (verdict-unconsumed); anchors quadruples == the published SW kit
      anchors block; anchor inputs byte-clones of the published SW kit
      inputs.
  G3  runner == published SW runner transform (comment block only).

No verdict is consumed. The k05 WIN row stays a gate-verified UNCONSUMED
label; third-impl corroboration remains vacant (future Part) before any
adoption under the parent batch's WIN/LOSS conflict policy. The standard
11x11 empty board, every root, S2, class 1/2/4 and all closure classes
stay UNKNOWN. Nodes are bookkeeping, never verdicts.
"""
import hashlib, json, os, pathlib, re, subprocess, sys

KIT = pathlib.Path(__file__).resolve().parent.parent
SSOT = pathlib.Path(os.environ.get("SX_SSOT", str(KIT.parent / "ssot")))

RAW_BASE = "https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches"
HEAD = "b05bf8b46f6335d6d819dbe966e473fd05885ed7"  # main head at kit build (set below at runtime check)

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
    "label": "42dbb58f",
    "path": "research/experiments/n11-centralreply-sixthlossk38-adoption-reaudit-20261126/output/merged-exact-s5-chain-plus-sixthlossk38-20261126.cache",
    "sha256": "42dbb58ffe8dd02a81f4a92993d08e3fbebdaeb4b4f7bf33e142120ff055bdc4",
    "rows": 6832, "WIN": 201, "LOSS": 6631,
}
SW_KIT = "research/experiments/n11-seventhcost-41loss-cppgate-20261127"
SEV_KIT = "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126"
PROBE_RAW = SEV_KIT + "/output/raw"
K05 = {"key": "1152921504607932416:536870912", "lo": "1152921504607932416", "hi": "536870912",
       "input_pin": "a73a6c70a221619b94ce29c188434d24a1f8af43653b37c1019a3286ba2ddb91",
       "raw_pair_sha": "ff750cc63e3ead314a5c5a22b09cca5588f284a34dc08c5c4d1cc5716eda342c",
       "budget": "50000000"}
EXPECT = "90,50000000,1,15763505"

gates = {}
def gate(name, ok, detail=""):
    gates[name] = {"status": "PASS" if ok else "FAIL", "detail": str(detail)[:400]}
    return bool(ok)

def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def fetch(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["curl", "-sL", "--fail", url, "-o", str(dest)])
    if r.returncode != 0:
        raise SystemExit("fetch failed: %s" % url)

def main():
    ok = True
    # ---- G0 gate source pins vs published SW kit gate-rows.json ----
    swgr_path = SSOT / "sw-gate-rows.json"
    fetch("%s/%s/%s/input/gate-rows.json" % (RAW_BASE, HEAD, SW_KIT), swgr_path)
    swgr = json.loads(swgr_path.read_text())
    ok &= gate("G0:sw-kit-gate-rows-read", swgr.get("schema") == "n11-seventhcost-41loss-cppgate-rows-v1", swgr.get("schema"))
    gs = swgr.get("gate_source", {})
    ok &= gate("G0:gate-source-commit", gs.get("commit") == GATE_SOURCE["commit"])
    ok &= gate("G0:kyouen_dfpn_root.cpp", gs.get("sha256") == GATE_SOURCE["sha256"])
    ok &= gate("G0:kyouen_residual_micro.hpp", gs.get("header_pins", {}).get("kyouen_residual_micro.hpp") == GATE_SOURCE["header_pins"]["kyouen_residual_micro.hpp"])
    ok &= gate("G0:n11_s5_quarantine.hpp", gs.get("header_pins", {}).get("n11_s5_quarantine.hpp") == GATE_SOURCE["header_pins"]["n11_s5_quarantine.hpp"])

    # ---- G1 k05 SSOT ----
    ipath = KIT / "input" / "k05.input.csv"
    ok &= gate("G1:k05-input-present", ipath.is_file())
    ok &= gate("G1:k05-input-sha==published-manifest-pin", sha256(ipath) == K05["input_pin"], sha256(ipath))
    rowtext = ipath.read_text().strip()
    ok &= gate("G1:k05-input-row-spec-shape",
               rowtext.startswith("target,0,5,%s,%s,90" % (K05["lo"], K05["hi"])) and rowtext.endswith(",0,0,0,0,0"), rowtext)
    r1, r2 = SSOT / "k05-at50m-run1.out.csv", SSOT / "k05-at50m-run2.out.csv"
    fetch("%s/%s/%s/at50m-run1-k05.out.csv" % (RAW_BASE, HEAD, PROBE_RAW), r1)
    fetch("%s/%s/%s/at50m-run2-k05.out.csv" % (RAW_BASE, HEAD, PROBE_RAW), r2)
    ok &= gate("G1:k05-raw-run1-sha==ff750cc6", sha256(r1) == K05["raw_pair_sha"], sha256(r1))
    ok &= gate("G1:k05-raw-run2-sha==ff750cc6", sha256(r2) == K05["raw_pair_sha"], sha256(r2))
    def replay_fields(p):
        line = [l for l in pathlib.Path(p).read_text().splitlines() if l.startswith("replay,")]
        assert len(line) == 1, p
        return line[0].split(",")
    a, b = replay_fields(r1), replay_fields(r2)
    ok &= gate("G1:k05-cold-pair-identity-except-wall", a[1:8] == b[1:8] and a[9:] == b[9:], "%s vs %s" % (",".join(a), ",".join(b)))
    ok &= gate("G1:k05-win-inside-budget", a[5] == K05["budget"] and a[6] == "1" and int(a[7]) < int(K05["budget"]), ",".join(a))
    ok &= gate("G1:k05-expected-quadruple-from-raw", "%s,%s,%s,%s" % (a[3], a[5], a[6], a[7]) == EXPECT, ",".join(a))
    # stage policy: the published 2M/15M UNKNOWN raws of the same key
    u1 = SSOT / "k05-at2m.out.csv"
    fetch("%s/%s/%s/at2m-k05.out.csv" % (RAW_BASE, HEAD, PROBE_RAW), u1)
    ua = replay_fields(u1)
    ok &= gate("G1:k05-stage-policy-2m-unknown", ua[5] == "2000000" and ua[6] == "0" and ua[7] == "2000000", ",".join(ua))

    # ---- G2 cross-SSOT ----
    head_path = SSOT / "head-sx.cache"
    fetch("%s/%s/%s" % (RAW_BASE, HEAD, CANONICAL_HEAD["path"]), head_path)
    hsha = sha256(head_path)
    head_text = head_path.read_text()
    head_rows = [l for l in head_text.splitlines() if l.startswith("s5verdict,")]
    win = sum(1 for l in head_rows if l.split(",")[4] == "1")
    loss = sum(1 for l in head_rows if l.split(",")[4] == "2")
    ok &= gate("G2:canonical-head-sha", hsha == CANONICAL_HEAD["sha256"], hsha)
    ok &= gate("G2:canonical-head-census", len(head_rows) == CANONICAL_HEAD["rows"] and win == CANONICAL_HEAD["WIN"] and loss == CANONICAL_HEAD["LOSS"],
               "rows=%d WIN=%d LOSS=%d" % (len(head_rows), win, loss))
    ok &= gate("G2:freshness-k05-absent", ("s5verdict,%s,%s," % (K05["lo"], K05["hi"])) not in head_text, "k05 must be absent from 42dbb58f")

    anchors = swgr.get("anchors", {})
    ok &= gate("G2:anchors==sw-kit", anchors == {
        "anchor-af039": "89,30000000,2,19234232",
        "anchor-aj001": "84,30000000,2,5156075",
        "anchor-at2m": "98,2000000,0,2000000"}, anchors)
    for a in anchors:
        ap = KIT / "input" / ("%s.input.csv" % a)
        ok &= gate("G2:%s:input-present" % a, ap.is_file())
        if ap.is_file():
            swp = SSOT / ("sw-input-%s.input.csv" % a)
            fetch("%s/%s/%s/input/%s.input.csv" % (RAW_BASE, HEAD, SW_KIT, a), swp)
            ok &= gate("G2:%s:input==sw-kit-byte-clone" % a, ap.read_bytes() == swp.read_bytes())

    # ---- G3 runner == SW runner transform ----
    sw_runner_pub = SSOT / "sw-gate_runner.sh"
    fetch("%s/%s/%s/scripts/gate_runner.sh" % (RAW_BASE, HEAD, SW_KIT), sw_runner_pub)
    want = sw_runner_pub.read_text().replace(
        "# Part SW (seventh-cost 41 LOSS rows) C++ scrutiny gate runner. Usage: gate_runner.sh <key> <budget> <expected-fields>",
        "# Part SX (seventh-cost k05 L50M WIN row) C++ scrutiny gate runner. Usage: gate_runner.sh <key> <budget> <expected-fields>",
    ).replace("# block names Part SW", "# block names Part SX")
    got = (KIT / "scripts" / "gate_runner.sh").read_text()
    ok &= gate("G3:runner-transform-byte-exact", got == want, "runner sha256=%s" % sha256(KIT / "scripts" / "gate_runner.sh"))

    if not ok:
        print(json.dumps({"gates": gates, "emitted": False}, indent=1, sort_keys=True))
        return 1

    out = {
        "part": "SX",
        "schema": "n11-seventhcost-k05-l50m-cppgate-rows-v1",
        "gate_source": GATE_SOURCE,
        "canonical_head": dict(CANONICAL_HEAD, targets_fresh_vs=CANONICAL_HEAD["label"]),
        "target": {"k05": {"budget": K05["budget"], "expected": EXPECT,
                           "input_sha256": K05["input_pin"],
                           "lo": K05["lo"], "hi": K05["hi"], "legal": "90",
                           "replica_verdict": 1,
                           "raw_pair_sha256": K05["raw_pair_sha"],
                           "raw_provenance": "%s/at50m-run1-k05.out.csv" % PROBE_RAW}},
        "third_impl": {"exists": False,
                       "note": "k05 WIN row: single-implementation Node replica cold pair + this delegated second-implementation gate; third-impl corroboration is a separate future Part before any adoption (k20/k33 WIN precedent)"},
        "anchors": {a: anchors[a] for a in sorted(anchors)},
        "anchors_runtime": {a: [anchors[a].split(",")[1], anchors[a]] for a in sorted(anchors)},
        "auditor_source": {"path": "%s/scripts/audit_gate.py" % SW_KIT, "note": "the SX audit is a FRESH single-row implementation (Part SS precedent), not a byte transform; disclosed in the declaration and README"},
        "gates": gates,
    }
    (KIT / "input" / "gate-rows.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"emitted": True, "gates": {k: v["status"] for k, v in gates.items()}}, indent=1, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())
