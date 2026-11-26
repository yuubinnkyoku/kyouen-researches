#!/usr/bin/env python3
"""Part SR (fifth-resumption 30 LOSS rows) C++ scrutiny gate kit maker
(2026-11-26).

Assembles the fail-closed kit for the delegated pinned C++
second-implementation scrutiny gate on the THIRTY resolved-LOSS rows of the
fifth-resumption batch k09..k43 of the sixth-cost exclusive S5 probe (k09,
k10, k11, k12, k14, k15, k16, k17, k18, k21, k22, k23, k24, k25, k26, k27,
k28, k29, k30, k31, k32, k34, k35, k36, k37, k39, k40, k41, k42, k43 - the
parked keys k20/k33/k38 excluded, no new verdict for them). These are the
30 rows the Part SQ completion log records as standing unconsumed with "no
delegated C++ gate; coverage asymmetry disclosed"; the Part SL third-impl
batch (32/32 all-pass) already supplies third-implementation verdict-level
LOSS(2) corroboration for every one of them, so this Part supplies the
missing second-implementation gate.

Structural-clone disclosure vs the published Part SN maker
(scripts/make_kit_parked4rest2_cppgate_20261126.py, kit
research/experiments/n11-sixthcost-parked4rest2-l50m-cppgate-20261126/):
exactly these deltas, all pre-registered in the Part SR declaration:
(1) part/schema strings parked4rest2 -> fifthres30; (2) KEYS/TARGETS
k20/k33 -> the 30 fifth-resumption LOSS keys with the third-impl kit
input/ and the probe-lane output/raw/ pin locations (the per-row pins are
machine-read from the published audit_k09k43.py INPINS/ROWS literals,
fetched from main at the recorded HEAD and byte-pinned by the maker);
(3) the runner/audit/tamper byte templates are the published Part SN kit
(MANIFEST-pinned) instead of the Part SM kit, transformed by the same
comment/header-only + machine-wired rules; (4) THE THIRD-IMPL SECTION IS
PRESENCE, NOT ABSENCE: every target row has Part SL batch third-impl
verdict-level LOSS(2) corroboration (summary all_pass, 32 rows), so the G2
third-impl gates assert PRESENCE + per-row agreement, and gate-rows.json
records third_impl_verdict_level_corroboration=true (the inverse of the
SN disclosed-absence section). No other gate was added, removed, or
weakened; G0/G1/G3/G4 semantics are unchanged.

Machine-derived, no per-row pin hand-typed (EP pin policy): gate source and
anchor pins are machine-read from the published Part SN kit
(input/gate-rows.json), targets/expectations are derived from the
published probe-lane raws and cross-checked against the published
audit_k09k43.py literals and the Part SL summary; the runner/audit/tamper
transform templates are MANIFEST-verified against the published Part SN
kit.

Gates (all must PASS; any failure -> rc=1, no kit emit):
  G0  gate source pins: cpp/solvers/kyouen_dfpn_root.cpp sha256 9193f5b6...
      (commit 154f3b7a67b97e13acbaee8b04dc74ddca728d19, machine-read from
      the published SN kit gate-rows.json), headers
      kyouen_residual_micro.hpp 5976935d... / n11_s5_quarantine.hpp
      2e36d694... at the same commit.
  G1  probe-lane SSOT discipline per target: kit input byte-shape
      (target,0,5,lo,hi,legal,0,0,0,0,0) + sha == audit_k09k43.py INPINS
      pin; published raw sha pins == audit_k09k43.py ROWS pins; resolution
      cold-pair identity on every replay field except wall_s; expected
      quadruple derived from the resolution run1 raw; budget policy
      (loss15/loss2m15m rows at 15000000, loss2m rows at 2000000).
  G2  cross-SSOT: Part SL summary all_pass with rows_audited 32 and
      replica_verdict==third_impl_verdict==2 for every target;
      canonical head 02db5ab3 sha-verified with 6,801 s5verdict rows
      (WIN201/LOSS6600) and every target [lo,hi] pair ABSENT (fresh,
      verdict-unconsumed); anchors quadruples == the published SN kit
      anchors block.
  G3  kit byte templates: runner == published SN runner transform
      (comment block only); audit_gate.py == published SN audit transform
      (docstring + machine-generated ROWS/RAW_PROV + part/schema strings
      only, logic byte-identical).
  G8  emit input/gate-rows.json (schema
      n11-sixthcost-fifthres30-cppgate-rows-v1) ONLY if every gate PASSes.

No verdict is consumed. The 30 rows stay gate-verified UNCONSUMED labels.
The standard 11x11 empty board, every root, S2, class 1/2/4 and all closure
classes stay UNKNOWN. Nodes are bookkeeping, never verdicts.
"""
import hashlib, json, os, re, subprocess, sys, pathlib

KIT = pathlib.Path(__file__).resolve().parent.parent
SSOT = pathlib.Path(os.environ.get("SR_SSOT", str(KIT.parent / "ssot")))

RAW_BASE = "https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches"
HEAD = "277f91b2b06a5335b0896c2df0a2e53c140fb7c8"  # main head at kit build

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
    "label": "02db5ab3",
    "path": "research/experiments/n11-centralreply-sixthwin3-adoption-reaudit-20261126/output/merged-exact-s5-chain-plus-sixthwin3-20261126.cache",
    "sha256": "02db5ab35b8ad71dfd0699217756291c6bc896c78e9fd7c609b5e25177f6b25c",
    "rows": 6801, "WIN": 201, "LOSS": 6600,
}
SN_KIT = "research/experiments/n11-sixthcost-parked4rest2-l50m-cppgate-20261126"
TI_KIT = "research/experiments/n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122"
PROBE_RAW = "research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw"

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
    # ---- G0 gate source pins vs published SN kit gate-rows.json ----
    sngr_path = SSOT / "sn-gate-rows.json"
    fetch("%s/%s/%s/input/gate-rows.json" % (RAW_BASE, HEAD, SN_KIT), sngr_path)
    sngr = json.loads(sngr_path.read_text())
    ok &= gate("G0:sn-kit-gate-rows-read", sngr.get("schema") == "n11-sixthcost-parked4rest2-cppgate-rows-v1", sngr.get("schema"))
    gs = sngr.get("gate_source", {})
    ok &= gate("G0:gate-source-commit", gs.get("commit") == GATE_SOURCE["commit"])
    ok &= gate("G0:kyouen_dfpn_root.cpp", gs.get("sha256") == GATE_SOURCE["sha256"])
    ok &= gate("G0:kyouen_residual_micro.hpp", gs.get("header_pins", {}).get("kyouen_residual_micro.hpp") == GATE_SOURCE["header_pins"]["kyouen_residual_micro.hpp"])
    ok &= gate("G0:n11_s5_quarantine.hpp", gs.get("header_pins", {}).get("n11_s5_quarantine.hpp") == GATE_SOURCE["header_pins"]["n11_s5_quarantine.hpp"])

    # ---- machine-read the published third-impl auditor literals ----
    aud_path = SSOT / "audit_k09k43.py"
    fetch("%s/%s/%s/audit_k09k43.py" % (RAW_BASE, HEAD, TI_KIT), aud_path)
    aud_sha = sha256(aud_path)
    rows = json.loads(re.search(r'ROWS = json\.loads\(r"""(\{.*?\})"""\)', aud_path.read_text(), re.S).group(1))
    inpins = json.loads(re.search(r'INPINS = json\.loads\(r"""(\{.*?\})"""\)', aud_path.read_text(), re.S).group(1))
    targets = {k: v for k, v in rows.items() if not v.get("win")}
    ok &= gate("G1:auditor-fetched-pinned", len(targets) == 30 and len(inpins) == 32,
               "targets=%d inpins=%d auditor_sha256=%s" % (len(targets), len(inpins), aud_sha))

    # ---- G1 per-target SSOT ----
    order = sorted(targets, key=lambda x: int(x[1:]))
    expected = {}
    for k in order:
        v = targets[k]
        ipath = KIT / "input" / ("%s.input.csv" % k)
        if not ipath.is_file():
            ok &= gate("G1:%s:input-present" % k, False); continue
        isha = sha256(ipath)
        spec = inpins.get("%s.input.csv" % k)
        ok &= gate("G1:%s:input-sha==INPINS" % k, isha == spec[0], isha)
        ok &= gate("G1:%s:input-row-spec-shape" % k,
                   ipath.read_text().strip() == spec[1] and spec[1].startswith("target,0,5,") and spec[1].endswith(",0,0,0,0,0"), spec[1])
        # fetch + verify every published raw of this row
        stage = v["stage"]
        if stage in ("loss15", "loss2m15m"):
            f1, f2 = "at15m-run1-%s.out.csv" % k, "at15m-run2-%s.out.csv" % k
            budget = "15000000"
        else:
            assert stage == "loss2m", stage
            f1, f2 = "at2m-%s.out.csv" % k, "at2m-run2-%s.out.csv" % k
            budget = "2000000"
        d1, d2 = SSOT / "raws" / f1, SSOT / "raws" / f2
        fetch("%s/%s/%s/%s" % (RAW_BASE, HEAD, PROBE_RAW, f1), d1)
        fetch("%s/%s/%s/%s" % (RAW_BASE, HEAD, PROBE_RAW, f2), d2)
        ok &= gate("G1:%s:raw-run1-sha==ROWS-pin" % k, sha256(d1) == v["files"][f1][3], sha256(d1))
        ok &= gate("G1:%s:raw-run2-sha==ROWS-pin" % k, sha256(d2) == v["files"][f2][3], sha256(d2))
        def replay_fields(p):
            line = [l for l in pathlib.Path(p).read_text().splitlines() if l.startswith("replay,")]
            assert len(line) == 1, p
            return line[0].split(",")
        a, b = replay_fields(d1), replay_fields(d2)
        ok &= gate("G1:%s:cold-pair-identity-except-wall" % k, a[2:8] == b[2:8] and a[9:] == b[9:], "%s vs %s" % (",".join(a), ",".join(b)))
        ok &= gate("G1:%s:loss-inside-budget" % k, a[5] == budget and a[6] == "2" and int(a[7]) < int(budget), ",".join(a))
        ok &= gate("G1:%s:rep-nodes==auditor" % k, a[7] == v["rep_nodes"], a[7])
        expected[k] = "%s,%s,2,%s" % (v["legal"], budget, a[7])

    # ---- G2 cross-SSOT ----
    sl_path = SSOT / "audit-k09k43-summary.json"
    fetch("%s/%s/%s/out/audit-k09k43-summary.json" % (RAW_BASE, HEAD, TI_KIT), sl_path)
    sl = json.loads(sl_path.read_text())
    rr = sl.get("row_results", {})
    agree = all(rr.get(k, {}).get("replica_verdict") == 2 and rr.get(k, {}).get("third_impl_verdict") == 2 for k in order)
    ok &= gate("G2:sl-summary-all-pass-32", sl.get("all_pass") is True and sl.get("rows_audited") == 32 and sl.get("consumed") is False, sl.get("schema"))
    ok &= gate("G2:sl-third-impl-loss-agreement-30", agree and sum(1 for v in rr.values() if v.get("replica_verdict") == 2) == 30)

    head_path = SSOT / "head.cache"
    fetch("%s/%s/%s" % (RAW_BASE, HEAD, CANONICAL_HEAD["path"]), head_path)
    hsha = sha256(head_path)
    head_text = head_path.read_text()
    head_rows = [l for l in head_text.splitlines() if l.startswith("s5verdict,")]
    win = sum(1 for l in head_rows if l.split(",")[4] == "1")
    loss = sum(1 for l in head_rows if l.split(",")[4] == "2")
    ok &= gate("G2:canonical-head-sha", hsha == CANONICAL_HEAD["sha256"], hsha)
    ok &= gate("G2:canonical-head-census", len(head_rows) == CANONICAL_HEAD["rows"] and win == CANONICAL_HEAD["WIN"] and loss == CANONICAL_HEAD["LOSS"],
               "rows=%d WIN=%d LOSS=%d" % (len(head_rows), win, loss))
    absent = [k for k in order if ("s5verdict,%s,%s," % (targets[k]["lo"], targets[k]["hi"])) not in head_text]
    ok &= gate("G2:freshness-30-targets-absent", len(absent) == 30, "absent=%d/30" % len(absent))

    anchors = sngr.get("anchors", {})
    ok &= gate("G2:anchors==sn-kit", anchors == {
        "anchor-af039": "89,30000000,2,19234232",
        "anchor-aj001": "84,30000000,2,5156075",
        "anchor-at2m": "98,2000000,0,2000000"}, anchors)
    for a in anchors:
        ap = KIT / "input" / ("%s.input.csv" % a)
        ok &= gate("G2:%s:input-present" % a, ap.is_file())
        if ap.is_file():
            # byte-clone == published SN kit input
            snp = SSOT / ("sn-input-%s.input.csv" % a)
            fetch("%s/%s/%s/input/%s.input.csv" % (RAW_BASE, HEAD, SN_KIT, a), snp)
            ok &= gate("G2:%s:input==sn-kit-byte-clone" % a, ap.read_bytes() == snp.read_bytes())

    # ---- G3 kit byte templates ----
    sn_runner_pub = SSOT / "sn-gate_runner.sh"
    fetch("%s/%s/%s/scripts/gate_runner.sh" % (RAW_BASE, HEAD, SN_KIT), sn_runner_pub)
    want = sn_runner_pub.read_text().replace(
        "# Part SN (parked4rest2 L50M WIN rows) C++ scrutiny gate runner. Usage: gate_runner.sh <key> <budget> <expected-fields>",
        "# Part SR (fifth-resumption 30 LOSS rows) C++ scrutiny gate runner. Usage: gate_runner.sh <key> <budget> <expected-fields>",
    ).replace("# block names Part SN", "# block names Part SR")
    got = (KIT / "scripts" / "gate_runner.sh").read_text()
    ok &= gate("G3:runner-transform-byte-exact", got == want, "runner sha256=%s" % sha256(KIT / "scripts" / "gate_runner.sh"))

    sn_audit_pub = SSOT / "sn-audit_gate.py"
    fetch("%s/%s/%s/scripts/audit_gate.py" % (RAW_BASE, HEAD, SN_KIT), sn_audit_pub)
    sn_src = sn_audit_pub.read_text()
    kit_src = (KIT / "scripts" / "audit_gate.py").read_text()
    def norm(s):
        s = s.replace('"part": "SN", "schema": "n11-sixthcost-parked4rest2-cppgate-audit-v1"', "PART_SCHEMA_TOKEN")
        return s.replace('"part": "SR", "schema": "n11-sixthcost-fifthres30-cppgate-audit-v1"', "PART_SCHEMA_TOKEN")
    ok &= gate("G3:audit-logic-byte-identical",
               norm(sn_src.split('"""', 2)[2].split("ROWS = {")[0]) == norm(kit_src.split('"""', 2)[2].split("ROWS = {")[0])
               and norm(sn_src.split("RAW_PROV = {", 1)[1].split("REPLAY", 1)[1]) == norm(kit_src.split("RAW_PROV = {", 1)[1].split("REPLAY", 1)[1]),
               "audit sha256=%s" % sha256(KIT / "scripts" / "audit_gate.py"))
    ok &= gate("G3:audit-rows-consistent", all(json.loads(re.search(r'ROWS = (\{.*?\})\n', kit_src, re.S).group(1))[k][1] == expected[k] for k in order))

    if not ok:
        print(json.dumps({"gates": gates, "emitted": False}, indent=1, sort_keys=True))
        return 1

    out = {
        "part": "SR",
        "schema": "n11-sixthcost-fifthres30-cppgate-rows-v1",
        "gate_source": GATE_SOURCE,
        "canonical_head": dict(CANONICAL_HEAD, targets_fresh_vs=CANONICAL_HEAD["label"]),
        "third_impl": {
            "exists": True,
            "source": "%s/out/audit-k09k43-summary.json" % TI_KIT,
            "schema": sl["schema"], "all_pass": True, "rows_audited": 32,
            "verdict_level_corroboration": True,
        },
        "anchors": {a: anchors[a] for a in sorted(anchors)},
        "anchors_runtime": {a: [anchors[a].split(",")[1], anchors[a]] for a in sorted(anchors)},
        "targets": {k: {"budget": expected[k].split(",")[1], "expected": expected[k],
                        "input_sha256": sha256(KIT / "input" / ("%s.input.csv" % k)),
                        "lo": targets[k]["lo"], "hi": targets[k]["hi"], "legal": targets[k]["legal"],
                        "replica_verdict": 2, "third_impl_verdict": 2,
                        "raw_provenance": "%s/%s" % (PROBE_RAW, ("at15m-run1-%s.out.csv" % k) if targets[k]["stage"] in ("loss15", "loss2m15m") else ("at2m-%s.out.csv" % k))}
                      for k in order},
        "auditor_source": {"path": "%s/audit_k09k43.py" % TI_KIT, "sha256": aud_sha},
        "gates": gates,
    }
    (KIT / "input" / "gate-rows.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"emitted": True, "gates": {k: v["status"] for k, v in gates.items()}}, indent=1, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())
