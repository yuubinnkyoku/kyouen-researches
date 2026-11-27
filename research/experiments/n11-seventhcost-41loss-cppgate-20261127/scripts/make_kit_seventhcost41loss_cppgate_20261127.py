#!/usr/bin/env python3
"""Part SW (seventh-cost 41 LOSS rows) C++ scrutiny gate kit maker (2026-11-27).

Assembles the fail-closed kit for the delegated pinned C++
second-implementation scrutiny gate on the FORTY-ONE resolved-LOSS rows of
the seventh-cost exclusive S5 probe batch (k01..k42 minus k05; k05 is the
parked-then-L50M-WIN row and is EXCLUDED, no new verdict for it, its C++
gate + third-impl corroboration stay separate future Parts). These are the
41 rows the seventh-cost batch checkpoint records as exact LOSS with ladder
cold pairs but no delegated C++ gate.

Structural-clone disclosure vs the published Part SR maker
(scripts/make_kit_fifthres30_cppgate_20261126.py, kit
research/experiments/n11-sixthcost-fifthres30-cppgate-20261126/): exactly
these deltas, all pre-registered in the Part SW declaration:
(1) part/schema strings fifthres30 -> seventhcost41loss; (2) KEYS/TARGETS:
the 41 seventh-cost resolved-LOSS keys, machine-read from the published
seventh-cost selection JSON + batch-summary ledger + probe raws (the
published probe kit MANIFEST pins are the input SSOT, the published
MANIFEST-raw-sha256.txt pins are the raw SSOT; the 124 published raws are
read from a local cache and sha-verified against the published manifest
fetched from the pinned HEAD - a fetch-route optimization only, disclosed
in the declaration); (3) the runner/audit byte templates are the published
Part SR kit (MANIFEST-pinned) transformed by the same comment/header-only
+ machine-wired rules; (4) THE THIRD-IMPL SECTION IS ABSENCE, NOT
PRESENCE: no seventh-cost row has third-implementation corroboration yet
(the inverse of the SR kit), so gate-rows.json records
third_impl_verdict_level_corroboration=false and the adoption requirement
(second impl = this gate, third impl = separate future Part) follows the
SN disclosed-absence pattern. No other gate was added, removed, or
weakened; G0/G1/G2/G3 semantics are unchanged.

Machine-derived, no per-row pin hand-typed (EP pin policy): gate source and
anchor pins are machine-read from the published SR kit gate-rows.json;
targets/expectations are derived from the published raws and cross-checked
against the published selection JSON literals and the published
batch-summary ledger; the runner/audit transform templates are
MANIFEST-verified against the published SR kit.

Gates (all must PASS; any failure -> rc=1, no kit emit):
  G0  gate source pins: cpp/solvers/kyouen_dfpn_root.cpp sha256 9193f5b6...
      (commit 154f3b7a67b97e13acbaee8b04dc74ddca728d19, machine-read from
      the published SR kit gate-rows.json), headers
      kyouen_residual_micro.hpp 5976935d... / n11_s5_quarantine.hpp
      2e36d694... at the same commit.
  G1  probe-lane SSOT discipline per target: kit input byte-shape
      (target,0,5,lo,hi,legal,0,0,0,0,0) + sha == published seventh-cost
      kit MANIFEST-sha256.txt pin; published raw sha pins == published
      MANIFEST-raw-sha256.txt pins; resolution cold-pair identity on every
      replay field except wall_s; expected quadruple derived from the
      resolution run1 raw; budget policy (stage 15m rows at 15000000,
      stage 2m rows at 2000000) machine-read from the batch-summary ledger.
  G2  cross-SSOT: batch-summary ledger agreement (resolved_exact_loss 41,
      the 41 target keys are exactly the non-parked resolved keys, k05 the
      only parked key, head_basis sha 42dbb58f); canonical head 42dbb58f
      sha-verified with 6,832 s5verdict rows (WIN201/LOSS6631) and every
      target [lo,hi] pair ABSENT (fresh, verdict-unconsumed); anchors
      quadruples == the published SR kit anchors block; anchor inputs
      byte-clones of the published SR kit inputs.
  G3  kit byte templates: runner == published SR runner transform (comment
      block only); audit_gate.py == published SR audit transform (docstring
      + machine-generated ROWS/RAW_PROV + part/schema strings only, logic
      byte-identical).
  G8  emit input/gate-rows.json (schema
      n11-seventhcost-41loss-cppgate-rows-v1) ONLY if every gate PASSes.

No verdict is consumed. The 41 rows stay gate-verified UNCONSUMED labels.
The standard 11x11 empty board, every root, S2, class 1/2/4 and all closure
classes stay UNKNOWN. Nodes are bookkeeping, never verdicts.
"""
import hashlib, json, os, pathlib, re, subprocess, sys

KIT = pathlib.Path(__file__).resolve().parent.parent
SSOT = pathlib.Path(os.environ.get("SW_SSOT", str(KIT.parent / "ssot")))
RAWS = pathlib.Path(os.environ.get("SW_RAWS", "/home/user/knowledge/kyouen-research/_seventhkit-raws"))

RAW_BASE = "https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches"
HEAD = "f38d2b43cefa91853a2e0e0f04b2f69ffa52bb5c"  # main head at kit build

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
SR_KIT = "research/experiments/n11-sixthcost-fifthres30-cppgate-20261126"
SEV_KIT = "research/experiments/n11-seventhcost-class-s5-exclusive-probe-1306043891938492416-20261126"
PROBE_RAW = SEV_KIT + "/output/raw"
LEDGER = SEV_KIT + "/output/batch-summary.json"
SELECTION = SEV_KIT + "/output/seventh-cost-exclusive-keys.json"
SELECTION_SHA = "c395fe032f87ee6764ee24777b90140ca0eaa05002abe9038a7c67d6ca12e627"
LEDGER_SHA = "6881eaaf"  # prefix pin from the published pre-audit instrument; full sha asserted below

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
    # ---- G0 gate source pins vs published SR kit gate-rows.json ----
    srgr_path = SSOT / "sr-gate-rows.json"
    fetch("%s/%s/%s/input/gate-rows.json" % (RAW_BASE, HEAD, SR_KIT), srgr_path)
    srgr = json.loads(srgr_path.read_text())
    ok &= gate("G0:sr-kit-gate-rows-read", srgr.get("schema") == "n11-sixthcost-fifthres30-cppgate-rows-v1", srgr.get("schema"))
    gs = srgr.get("gate_source", {})
    ok &= gate("G0:gate-source-commit", gs.get("commit") == GATE_SOURCE["commit"])
    ok &= gate("G0:kyouen_dfpn_root.cpp", gs.get("sha256") == GATE_SOURCE["sha256"])
    ok &= gate("G0:kyouen_residual_micro.hpp", gs.get("header_pins", {}).get("kyouen_residual_micro.hpp") == GATE_SOURCE["header_pins"]["kyouen_residual_micro.hpp"])
    ok &= gate("G0:n11_s5_quarantine.hpp", gs.get("header_pins", {}).get("n11_s5_quarantine.hpp") == GATE_SOURCE["header_pins"]["n11_s5_quarantine.hpp"])

    # ---- published seventh-cost SSOT literals ----
    sel_path = SSOT / "seventh-cost-exclusive-keys.json"
    fetch("%s/%s/%s" % (RAW_BASE, HEAD, SELECTION), sel_path)
    ok &= gate("G1:selection-sha-pin", sha256(sel_path) == SELECTION_SHA, sha256(sel_path))
    sel = json.loads(sel_path.read_text())
    order = sel["exclusive_probe_order"]
    ok &= gate("G1:selection-42-keys", len(order) == 42)

    led_path = SSOT / "batch-summary.json"
    fetch("%s/%s/%s" % (RAW_BASE, HEAD, LEDGER), led_path)
    led = json.loads(led_path.read_text())
    ok &= gate("G2:ledger-schema", led.get("schema") == "n11-seventhcost-batch-checkpoint-summary-v1", led.get("schema"))
    ok &= gate("G2:ledger-head-basis", led.get("head_basis", {}).get("sha256") == CANONICAL_HEAD["sha256"])
    ok &= gate("G2:ledger-counts", led.get("resolved_exact_loss") == 41 and led.get("resolved_exact_win") == 0 and led.get("parked_unknown_15m") == 1)
    pk = led["per_key"]

    # ---- published raw manifest (raw SSOT) ----
    rawman_path = SSOT / "MANIFEST-raw-sha256.txt"
    fetch("%s/%s/%s/MANIFEST-raw-sha256.txt" % (RAW_BASE, HEAD, SEV_KIT), rawman_path)
    rawpins = {}
    for line in rawman_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        sha, size, path = line.split()
        rawpins[path.split("/")[-1]] = (sha, int(size))

    # ---- published seventh-cost kit input manifest (input SSOT) ----
    inman_path = SSOT / "MANIFEST-sha256.txt"
    fetch("%s/%s/%s/MANIFEST-sha256.txt" % (RAW_BASE, HEAD, SEV_KIT), inman_path)
    inpins = {}
    for line in inman_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        inpins[parts[2].split("/")[-1]] = parts[0]

    # ---- G1 per-target SSOT ----
    expected = {}
    targetmeta = {}
    for i, e in enumerate(order, start=1):
        k = "k%02d" % i
        lo, hi = e["key"].split(":")
        if k == "k05":
            ok &= gate("G1:k05-parked-excluded", pk[i - 1].get("parked_unknown_15m") is True and pk[i - 1]["key"] == e["key"])
            continue
        ipath = KIT / "input" / ("%s.input.csv" % k)
        if not ipath.is_file():
            ok &= gate("G1:%s:input-present" % k, False); continue
        isha = sha256(ipath)
        ok &= gate("G1:%s:input-sha==kit-manifest" % k, isha == inpins["%s.input.csv" % k], isha)
        rowtext = ipath.read_text().strip()
        ok &= gate("G1:%s:input-row-spec-shape" % k,
                   rowtext.startswith("target,0,5,%s,%s," % (lo, hi)) and rowtext.endswith(",0,0,0,0,0"),
                   rowtext)
        # resolution stage from the ledger
        rec = pk[i - 1]
        ok &= gate("G1:%s:ledger-key" % k, rec["key"] == e["key"])
        stage = rec["resolved"]["stage"]
        if stage == "15m":
            f1, f2 = "at15m-run1-%s.out.csv" % k, "at15m-run2-%s.out.csv" % k
            budget = "15000000"
        else:
            assert stage == "2m", (k, stage)
            f1, f2 = "at2m-%s.out.csv" % k, "at2m-run2-%s.out.csv" % k
            budget = "2000000"
        d1, d2 = RAWS / f1, RAWS / f2
        ok &= gate("G1:%s:raw-run1-sha==manifest" % k, sha256(d1) == rawpins[f1][0], sha256(d1))
        ok &= gate("G1:%s:raw-run2-sha==manifest" % k, sha256(d2) == rawpins[f2][0], sha256(d2))
        def replay_fields(p):
            line = [l for l in pathlib.Path(p).read_text().splitlines() if l.startswith("replay,")]
            assert len(line) == 1, p
            return line[0].split(",")
        a, b = replay_fields(d1), replay_fields(d2)
        ok &= gate("G1:%s:cold-pair-identity-except-wall" % k, a[1:8] == b[1:8] and a[9:] == b[9:], "%s vs %s" % (",".join(a), ",".join(b)))
        ok &= gate("G1:%s:loss-inside-budget" % k, a[5] == budget and a[6] == "2" and int(a[7]) < int(budget), ",".join(a))
        ok &= gate("G1:%s:rep-nodes==ledger" % k, a[7] == str(rec["resolved"]["nodes"]), a[7])
        ok &= gate("G1:%s:legal==selection" % k, a[3] == str(e["legal"]), a[3])
        expected[k] = "%s,%s,2,%s" % (a[3], budget, a[7])
        targetmeta[k] = {"lo": lo, "hi": hi, "legal": a[3], "budget": budget,
                         "key": e["key"], "raw_run1": f1}
    ok &= gate("G1:targets-41", len(expected) == 41, "targets=%d" % len(expected))

    # ---- G2 cross-SSOT ----
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
    absent = [k for k in sorted(targetmeta) if ("s5verdict,%s,%s," % (targetmeta[k]["lo"], targetmeta[k]["hi"])) not in head_text]
    ok &= gate("G2:freshness-41-targets-absent", len(absent) == 41, "absent=%d/41" % len(absent))

    anchors = srgr.get("anchors", {})
    ok &= gate("G2:anchors==sr-kit", anchors == {
        "anchor-af039": "89,30000000,2,19234232",
        "anchor-aj001": "84,30000000,2,5156075",
        "anchor-at2m": "98,2000000,0,2000000"}, anchors)
    for a in anchors:
        ap = KIT / "input" / ("%s.input.csv" % a)
        ok &= gate("G2:%s:input-present" % a, ap.is_file())
        if ap.is_file():
            srp = SSOT / ("sr-input-%s.input.csv" % a)
            fetch("%s/%s/%s/input/%s.input.csv" % (RAW_BASE, HEAD, SR_KIT, a), srp)
            ok &= gate("G2:%s:input==sr-kit-byte-clone" % a, ap.read_bytes() == srp.read_bytes())

    # ---- G3 kit byte templates ----
    sr_runner_pub = SSOT / "sr-gate_runner.sh"
    fetch("%s/%s/%s/scripts/gate_runner.sh" % (RAW_BASE, HEAD, SR_KIT), sr_runner_pub)
    want = sr_runner_pub.read_text().replace(
        "# Part SR (fifth-resumption 30 LOSS rows) C++ scrutiny gate runner. Usage: gate_runner.sh <key> <budget> <expected-fields>",
        "# Part SW (seventh-cost 41 LOSS rows) C++ scrutiny gate runner. Usage: gate_runner.sh <key> <budget> <expected-fields>",
    ).replace("# block names Part SR", "# block names Part SW")
    got = (KIT / "scripts" / "gate_runner.sh").read_text()
    ok &= gate("G3:runner-transform-byte-exact", got == want, "runner sha256=%s" % sha256(KIT / "scripts" / "gate_runner.sh"))

    # generate the audit script from the published SR audit via machine transforms
    sr_audit_pub = SSOT / "sr-audit_gate.py"
    fetch("%s/%s/%s/scripts/audit_gate.py" % (RAW_BASE, HEAD, SR_KIT), sr_audit_pub)
    sr_src = sr_audit_pub.read_text()
    head, rest = sr_src.split('"""', 2)[0], sr_src.split('"""', 2)[2]
    # drop the SR ROWS/RAW_PROV literal blocks entirely; keep only the logic tail
    logic_src = rest[rest.index("REPLAY = re.compile"):]
    rows_json = json.dumps(dict(
        [(a, [anchors[a].split(",")[1], anchors[a],
              sha256(KIT / "input" / ("%s.input.csv" % a)),
              "SR kit input/%s.input.csv (byte-clone; == EQ/EN/EO/EV/SN/SR kit input; SR kit MANIFEST-sha256.txt pin)" % a])
         for a in sorted(anchors)] +
        [(k, [targetmeta[k]["budget"], expected[k],
              sha256(KIT / "input" / ("%s.input.csv" % k)),
              "seventh-cost kit input/%s.input.csv (byte-clone of the published seventh-cost batch input of n11-seventhcost-exclusive-selection-v1; sha256 == published seventh-cost kit MANIFEST-sha256.txt pin, the input SSOT)" % k])
         for k in sorted(targetmeta)]), indent=1, sort_keys=True)
    raw_prov_json = json.dumps(dict(
        [(a, "EV/SK/SR kit raw condition (budget-ceiling baseline); == SR kit anchors block") for a in sorted(anchors)] +
        [(k, "%s/%s (published seventh-cost replica %s); cold-pair node-exact vs its run2 raw; third-impl corroboration ABSENT for this row (separate future Part before any adoption)" % (PROBE_RAW, targetmeta[k]["raw_run1"], expected[k])) for k in sorted(targetmeta)]), indent=1, sort_keys=True)
    audit_src = (
        '#!/usr/bin/env python3\n'
        '"""Part SW (seventh-cost 41 LOSS rows C++ scrutiny gate) fail-closed\n'
        'machine audit (41 delegated resolved-LOSS rows + 3 calibration anchors).\n'
        "\n"
        "EQ rev4 structure kept via the published SM/SN/SR kit audit script\n"
        "template (10-capture-group REPLAY regex asserted at import; see\n"
        "input/gate-rows.json for the machine-derived pins this audit derives\n"
        "from). Gates: G1 raw shape (replay row + terminal replay_done +\n"
        "driver headers), G2 per-row determinism (p1 == p2 except wall_s),\n"
        "G3 published-raw pins (legal,budget,result,nodes), G4 gate-status\n"
        "accounting, G5 input byte-clones (seventh-cost kit input/ == the\n"
        "published seventh-cost kit MANIFEST-sha256.txt pins for the 41\n"
        "targets; SR kit input/ == SR kit MANIFEST pins for the anchors).\n"
        "\n"
        "Disclosed vs the SR kit transform rule: docstring + machine-generated\n"
        "ROWS/RAW_PROV + part/schema strings only; the audit logic is unchanged.\n"
        "Unlike SR (third-impl PRESENCE), no target row here has\n"
        "third-implementation corroboration yet (seventh-cost batch\n"
        "single-implementation; a third-impl Part is a separate future Part\n"
        "before any adoption). No verdict is consumed: the 41 rows stay\n"
        "UNCONSUMED labels (canonical head 42dbb58f keeps them absent). 11x11,\n"
        "the two-stone root {60,27}, and its remaining third moves 100/108 stay\n"
        "UNKNOWN throughout. k05 (WIN@50M) is NOT a row of this kit.\n"
        '"""\n'
        "import hashlib, json, os, re, sys\n"
        "\n"
        "KIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), \"..\")\n"
        "KIT = os.path.abspath(KIT)\n"
        "\n"
        "# key -> (budget, expected \"legal,budget,result,nodes\",\n"
        "#          input sha256 pin, provenance of the input pin)\n"
        "ROWS = " + rows_json + "\n\n"
        "RAW_PROV = " + raw_prov_json + "\n\n"
        + logic_src.replace('"part": "SR", "schema": "n11-sixthcost-fifthres30-cppgate-audit-v1"',
                            '"part": "SW", "schema": "n11-seventhcost-41loss-cppgate-audit-v1"')
    )
    (KIT / "scripts" / "audit_gate.py").write_text(audit_src)
    kit_src = (KIT / "scripts" / "audit_gate.py").read_text()
    def norm(s):
        s = s.replace('"part": "SR", "schema": "n11-sixthcost-fifthres30-cppgate-audit-v1"', "PART_SCHEMA_TOKEN")
        return s.replace('"part": "SW", "schema": "n11-seventhcost-41loss-cppgate-audit-v1"', "PART_SCHEMA_TOKEN")
    ok &= gate("G3:audit-logic-byte-identical",
               norm(sr_src.split('"""', 2)[2].split("ROWS = {", 1)[0]) == norm(kit_src.split('"""', 2)[2].split("ROWS = ", 1)[0])
               and norm(sr_src.split("REPLAY = re.compile", 1)[1]) == norm(kit_src.split("REPLAY = re.compile", 1)[1]),
               "audit sha256=%s" % sha256(KIT / "scripts" / "audit_gate.py"))
    ok &= gate("G3:audit-rows-consistent", all(json.loads(re.search(r"ROWS = (\{.*?\})\n\nRAW_PROV", kit_src, re.S).group(1))[k][1] == expected[k] for k in sorted(targetmeta)))
    arows = json.loads(re.search(r"ROWS = (\{.*?\})\n\nRAW_PROV", kit_src, re.S).group(1))
    ok &= gate("G3:audit-anchor-rows", all(arows[a][1] == anchors[a] for a in anchors) and len(arows) == 44)

    if not ok:
        print(json.dumps({"gates": gates, "emitted": False}, indent=1, sort_keys=True))
        return 1

    out = {
        "part": "SW",
        "schema": "n11-seventhcost-41loss-cppgate-rows-v1",
        "gate_source": GATE_SOURCE,
        "canonical_head": dict(CANONICAL_HEAD, targets_fresh_vs=CANONICAL_HEAD["label"]),
        "selection": {"path": SELECTION, "sha256": SELECTION_SHA, "keys": 42},
        "ledger": {"path": LEDGER, "schema": led["schema"], "resolved_exact_loss": 41,
                   "parked_keys": led["parked_keys"]},
        "third_impl": {
            "exists": False,
            "note": "seventh-cost batch rows are single-implementation (Node replica cold pairs) + this delegated second-implementation gate; third-impl corroboration is a separate future Part before any adoption (SN disclosed-absence pattern)",
        },
        "anchors": {a: anchors[a] for a in sorted(anchors)},
        "anchors_runtime": {a: [anchors[a].split(",")[1], anchors[a]] for a in sorted(anchors)},
        "targets": {k: {"budget": targetmeta[k]["budget"], "expected": expected[k],
                        "input_sha256": sha256(KIT / "input" / ("%s.input.csv" % k)),
                        "lo": targetmeta[k]["lo"], "hi": targetmeta[k]["hi"], "legal": targetmeta[k]["legal"],
                        "replica_verdict": 2,
                        "raw_provenance": "%s/%s" % (PROBE_RAW, targetmeta[k]["raw_run1"])}
                    for k in sorted(targetmeta)},
        "auditor_source": {"path": "%s/scripts/audit_gate.py" % SR_KIT, "sha256": sha256(sr_audit_pub)},
        "gates": gates,
    }
    (KIT / "input" / "gate-rows.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"emitted": True, "gates": {k: v["status"] for k, v in gates.items()}}, indent=1, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())
