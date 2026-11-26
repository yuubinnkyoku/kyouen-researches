#!/usr/bin/env python3
"""Part SM (parked4 L50M WIN rows) C++ scrutiny gate kit maker (2026-11-26).

Assembles the fail-closed kit for the delegated pinned C++ second-implementation
scrutiny gate on the two sixth-cost parked-4-keys S5 L50M ladder WIN rows:

  k13 1152921573327376384:536870912  (legal 95)  expected 95,50000000,1,16402480
  k19 10376293541461626880:65664     (legal 95)  expected 95,50000000,1,15379062

These are the halt-audit's "win_raws_needing_scrutiny" / "delegated_cpp_gate_
targets" rows (the ladder lane had no C++ toolchain and delegated the gate to a
scrutiny owner). Part SL published the third-implementation verdict-level
batch scrutiny (32/32, k13/k19 WIN x3 runs); the pinned C++ gate recorded in
the halt-audit remains unexecuted. This Part executes it, following the
Part SK lineage (same runner rev2 bytes, same EQ rev4 audit structure,
same zig 0.13.0 build route for the pinned gate source).

Machine-derived, no per-row pin hand-typed (EP pin policy): gate source and
anchor pins are extracted from the published Part SK kit (gate-rows.json +
MANIFEST-sha256.txt), target expectations are derived from the published
parked4 ladder kit raws and cross-checked against the halt-audit, the kit
README, the session status.log, and the published third-impl batch summary.

Gates (all must PASS; any failure -> rc=1, no kit emit):
  G0  gate source pins: cpp/solvers/kyouen_dfpn_root.cpp sha256 9193f5b6...
      (commit 154f3b7a67b97e13acbaee8b04dc74ddca728d19, machine-read from the
      published SK kit gate-rows.json), headers kyouen_residual_micro.hpp
      5976935d... / n11_s5_quarantine.hpp 2e36d694... at the same commit.
  G1  parked4-kit SSOT discipline for k13/k19: input row-spec shape; base15m
      park raws (result 0, nodes 15,000,000 @15M); l50m-run1/run2 pair identity
      on every replay field except wall_s; the 32M margin reproof raw; the
      voluntary run3-verify raw identical (except wall_s); the published
      two-target validation rows (val-at2m x2 result 0 ceiling, val-15m x2
      result 2 at nodes 3,651,923 / 5,040,200, distinct keys); status.log
      accounting lines; expected quadruple derived from l50m-run1.
  G2  cross-SSOT: the machine-extracted (legal,budget,result,nodes) quadruple
      per key agrees with (a) halt-audit.json delegated_cpp_gate_targets +
      per_key stages + halted_on_win_keys + title, (b) the parked4 kit README
      result lines + delegated solver pin, (c) the published third-impl batch
      audit summary (all_pass, verdict-level agreement, 3 runs, replica
      resolution nodes).
  G3  anchors: byte pins from the published Part SK kit MANIFEST-sha256.txt +
      expected anchor quadruples machine-extracted from the published SK kit
      gate-rows.json anchors block.
  G4  freshness: canonical merged head sha256 16a12390... (Part EW close-out
      head of record, 6,797 s5verdict rows WIN197/LOSS6600); every target
      (lo,hi) pair absent from it (verdict-unconsumed rows).
  G8  emit kit bytes (inputs byte-clone + gate-rows.json + audit_gate.py +
      gate_runner.sh + tamper_battery.sh, every emitted byte sha-recorded).

No verdict is consumed by anything in this kit. The 2 rows stay UNCONSUMED
labels; the gate only makes them adoption-eligible for a separately declared
adoption Part (if-adopted scenario recorded NOT-ADOPTED in the halt-audit).
The standard 11x11 empty board, the two-stone root {60,27}, and its remaining
third moves 100/108 stay UNKNOWN throughout. nodes are bookkeeping, never
verdicts.
"""
import hashlib
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, ".."))
SSOT = os.environ.get(
    "SM_SSOT_ROOT",
    os.path.abspath(os.path.join(HERE, "..", "..", "..", "ssot")))

CANON_HEAD_SHA256 = \
    "16a12390c0c3f046f0ae537b2a9940e15661263fc5034ce1b155c138bb9043cd"
CANON_HEAD_LABEL = "16a12390"
CANON_HEAD_PATH = ("research/experiments/"
                   "n11-centralreply-sixthwin5-adoption-predecl-20261126/"
                   "output/merged-exact-s5-chain-plus-sixthwin5-20261126.cache")

KEYS = ["k13", "k19"]
TARGETS = {
    "k13": ("1152921573327376384", "536870912"),
    "k19": ("10376293541461626880", "65664"),
}
BUDGET = "50000000"
MARGIN_BUDGET = "32000000"

REPLAY = re.compile(
    r"^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),([0-9.]+),(\d+),(\d+)$")
assert REPLAY.groups == 10, "rev4 lesson: exactly 10 capture groups"


def fail(msg):
    sys.stderr.write("MAKER GATE FAIL: %s\n" % msg)
    sys.exit(1)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def rd(rel):
    return os.path.join(SSOT, rel)


def parse_replay(path):
    text = open(path).read()
    m = [REPLAY.match(l) for l in text.splitlines() if l.startswith("replay,")]
    done = "# replay_done rows=1" in text
    hdr = ("# exact replay: order=0 " in text
           and "# exact replay: id,stones,legal,is_or,budget,result,nodes,"
               "wall_s,key_lo,key_hi" in text)
    if len(m) != 1 or not done or not hdr:
        fail("raw shape %s (replay_rows=%d done=%s hdr=%s)"
             % (path, len(m), done, hdr))
    return list(m[0].groups())


def nowall(groups):
    """All replay fields except wall_s (index 7)."""
    return groups[:7] + groups[8:]


def main():
    gates = {}

    def g(name, ok, detail=""):
        gates[name] = {"status": "PASS" if ok else "FAIL", "detail": detail}
        if not ok:
            fail("gate %s FAIL: %s" % (name, detail))
        return ok

    # ---- G0 gate source pins (machine-read from the published SK kit)
    sk_rows = json.load(open(rd(os.path.join("sk", "input", "gate-rows.json"))))
    g("G0:sk-kit-rows-read", sk_rows.get("part") == "SK"
      and sk_rows.get("schema") == "n11-sixthcost-exclusive-cppgate-rows-v1",
      "SK kit gate-rows.json schema anchor")
    gate_source = sk_rows["gate_source"]
    g("G0:gate-source-commit",
      gate_source["commit"] == "154f3b7a67b97e13acbaee8b04dc74ddca728d19",
      "commit %s" % gate_source["commit"])
    GATE_SOURCE_PIN_CPP = gate_source["sha256"]
    GATE_SOURCE_PIN_HPP = gate_source["header_pins"]["kyouen_residual_micro.hpp"]
    GATE_SOURCE_PIN_Q = gate_source["header_pins"]["n11_s5_quarantine.hpp"]
    for fn, pin in (("kyouen_dfpn_root.cpp", GATE_SOURCE_PIN_CPP),
                    ("kyouen_residual_micro.hpp", GATE_SOURCE_PIN_HPP),
                    ("n11_s5_quarantine.hpp", GATE_SOURCE_PIN_Q)):
        p = rd(os.path.join("pinned", fn))
        got = sha256(p)
        g("G0:" + fn, got == pin,
          "sha256 %s %s" % (got, "==" if got == pin else "!= " + pin))

    # ---- G1 parked4-kit SSOT discipline
    rows = {}
    for k in KEYS:
        lo, hi = TARGETS[k]
        ipath = rd(os.path.join("p4", "input", "batch-%s.input.csv" % k))
        icont = open(ipath).read().strip()
        fields = icont.split(",")
        ok = (fields[0] == "target" and fields[1] == "0"
              and fields[2] == "5" and fields[3] == lo and fields[4] == hi
              and fields[5].isdigit() and int(fields[5]) > 0
              and fields[6:] == ["0", "0", "0", "0", "0"])
        g("G1:%s:input-row-spec-shape" % k, ok,
          "spec=%s" % icont if ok else "bad row spec %r" % icont)
        legal = fields[5]
        raw_dir = os.path.join("p4", "output", "raw")

        def pkey(name):
            return rd(os.path.join(raw_dir, "%s-%s-%s.out.csv" % (name, lo, hi)))

        # base15m park baseline
        b = parse_replay(pkey("base15m"))
        g("G1:%s:base15m-park-baseline" % k,
          b[4] == "15000000" and b[5] == "0" and b[6] == "15000000"
          and b[8] == lo and b[9] == hi,
          "base15m result=%s nodes=%s (parked@15M)" % (b[5], b[6]))
        # 50M determinism pair
        r1 = parse_replay(pkey("l50m-run1"))
        r2 = parse_replay(pkey("l50m-run2"))
        g("G1:%s:50m-pair-identity-except-wall_s" % k,
          nowall(r1) == nowall(r2),
          "run1=%s run2=%s" % (",".join(r1), ",".join(r2)))
        g("G1:%s:key-fields-in-raws" % k,
          r1[8] == lo and r1[9] == hi and r2[8] == lo and r2[9] == hi,
          "lo,hi in raws %s,%s" % (r1[8], r1[9]))
        g("G1:%s:input-legal==raw-legal" % k, legal == r1[2],
          "input=%s raw=%s" % (legal, r1[2]))
        g("G1:%s:50m-budget-field" % k, r1[4] == BUDGET, r1[4])
        g("G1:%s:win-inside-budget" % k,
          r1[5] == "1" and int(r1[6]) < int(BUDGET),
          "result=%s nodes=%s < budget=%s (full df-pn proof, not a truncation)"
          % (r1[5], r1[6], BUDGET))
        # margin reproof + voluntary third verify
        m32 = parse_replay(pkey("l50m-margin"))
        g("G1:%s:margin-reproof" % k,
          m32[4] == MARGIN_BUDGET and m32[5] == "1" and m32[6] == r1[6],
          "margin budget=%s result=%s nodes=%s"
          % (m32[4], m32[5], m32[6]))
        rv = parse_replay(pkey("l50m-run3-verify"))
        g("G1:%s:run3-verify-identity" % k,
          nowall(rv) == nowall(r1),
          "voluntary third cold 50M run identical (except wall_s)")
        exp_quad = ",".join([r1[2], BUDGET, r1[5], r1[6]])
        g("G1:%s:expected-quadruple-derived" % k,
          exp_quad.split(",")[0] == legal and exp_quad.split(",")[1] == BUDGET
          and exp_quad.split(",")[2] == "1",
          "expected=%s (from published l50m-run1 raw)" % exp_quad)
        rows[k] = {
            "input_sha256": sha256(ipath),
            "row_spec": icont,
            "legal": legal,
            "budget": BUDGET,
            "expected": exp_quad,
            "raw_p1_sha256": sha256(pkey("l50m-run1")),
            "raw_p2_sha256": sha256(pkey("l50m-run2")),
            "margin_sha256": sha256(pkey("l50m-margin")),
            "run3_verify_sha256": sha256(pkey("l50m-run3-verify")),
        }

    # published validation rows (fresh-session two-target reproductions of
    # the parent batch's published validation rows; distinct keys, NOT a
    # determinism pair of one row - the ladder README wording "at2m x2")
    v1 = parse_replay(rd(os.path.join("p4", "output", "raw",
                                      "val-at2m-first.out.csv")))
    v2 = parse_replay(rd(os.path.join("p4", "output", "raw",
                                      "val-at2m-second.out.csv")))
    g("G1:val-at2m-two-target-rows",
      v1[2] == "98" and v2[2] == "99"
      and v1[4] == "2000000" and v2[4] == "2000000"
      and v1[5] == "0" and v1[6] == "2000000"
      and v2[5] == "0" and v2[6] == "2000000"
      and v1[9] != v2[9],
      "val-at2m rows legal=%s/%s result=%s nodes=%s (distinct keys)"
      % (v1[2], v2[2], v1[5], v1[6]))
    w1 = parse_replay(rd(os.path.join("p4", "output", "raw",
                                      "val-first-15m.out.csv")))
    w2 = parse_replay(rd(os.path.join("p4", "output", "raw",
                                      "val-second-15m.out.csv")))
    g("G1:val-15m-two-target-rows",
      w1[2] == "98" and w2[2] == "99"
      and w1[4] == "15000000" and w2[4] == "15000000"
      and w1[5] == "2" and w2[5] == "2"
      and w1[6] == "3651923" and w2[6] == "5040200"
      and w1[9] != w2[9],
      "val-15m rows legal=%s/%s result=2 nodes=%s/%s (distinct keys)"
      % (w1[2], w2[2], w1[6], w2[6]))

    # status.log accounting lines
    st = open(rd(os.path.join("p4", "output", "raw", "status.log"))).read()
    for k in KEYS:
        ok = (("start %s " % k) in st
              and ("done %s base15m rc=0 res=0 nodes=15000000" % k) in st
              and ("done %s l50m-run1 rc=0" % k) in st
              and ("done %s l50m-run2 rc=0" % k) in st
              and ("done %s margin32m rc=0" % k) in st
              and ("key %s status=WIN-halt res50m=1 nodes=%s"
                   % (k, rows[k]["expected"].split(",")[3])) in st
              and ("done %s run3-verify rc=0" % k) in st)
        g("G1:%s:status-log-lines" % k, ok, "key %s accounting lines" % k)
    g("G1:status-log-halt-rule",
      "lane halted on WIN stop rule 1" in st
      and "k20,k33 never started (remain parked@15M, claimable)" in st,
      "halt line + never-started keys on record")

    # ---- G2 cross-SSOT
    ha = json.load(open(rd(os.path.join("p4", "output", "halt-audit.json"))))
    g("G2:halt-audit-schema",
      ha.get("schema") == "n11-sixthcost-parked4-l50m-ladder-halt-audit-v1",
      ha.get("schema"))
    g("G2:halt-audit-gates-pass",
      ha.get("all_gates_pass_before_halt") is True
      and ha.get("halted_on_win_keys") == ["%s:%s" % TARGETS["k13"],
                                           "%s:%s" % TARGETS["k19"]],
      "halted_on_win_keys=%s" % ha.get("halted_on_win_keys"))
    prov = ha["probe"]
    per_key = prov["per_key"]
    delegated = {t["key"]: t for t in prov["delegated_cpp_gate_targets"]}
    g("G2:win-raws-list",
      prov.get("win_raws_needing_scrutiny") == ["%s:%s" % TARGETS["k13"],
                                                "%s:%s" % TARGETS["k19"]],
      "win_raws_needing_scrutiny=%s" % prov.get("win_raws_needing_scrutiny"))
    for k in KEYS:
        lo, hi = TARGETS[k]
        key = "%s:%s" % (lo, hi)
        exp = rows[k]["expected"]
        nodes = exp.split(",")[3]
        pk = per_key[k]
        g("G2:%s:halt-audit-per-key" % k,
          pk["key"] == key and pk["legal"] == int(rows[k]["legal"])
          and pk["verdict"] == "WIN"
          and pk["stages"]["at50m"]["result"] == 1
          and str(pk["stages"]["at50m"]["nodes"]) == nodes
          and pk["stages"]["at50m_run2"]["nodes"] == int(nodes)
          and pk["stages"]["margin_reproof"]["budget"] == 32000000
          and pk["stages"]["margin_reproof"]["nodes"] == int(nodes)
          and pk["stages"]["base15m"] == {"result": 0, "nodes": 15000000},
          "per_key stages agree with the published raws")
        dt = delegated[key]
        g("G2:%s:delegated-target-line" % k,
          dt["target"] == rows[k]["row_spec"],
          "delegated target == input row spec")
        g("G2:%s:delegated-expectation" % k,
          dt["budget"] == 50000000 and dt["expected_result"] == 1
          and str(dt["expected_nodes"]) == nodes,
          "delegated budget/result/nodes == %s" % exp)
    readme = open(rd(os.path.join("p4", "README.md"))).read()
    for k in KEYS:
        lo, hi = TARGETS[k]
        nodes = rows[k]["expected"].split(",")[3]
        nodes_g = "{:,}".format(int(nodes))
        g("G2:%s:kit-readme-result-line" % k,
          ("**%s `%s:%s` (legal %s): WIN(1) in nodes %s**"
           % (k, lo, hi, rows[k]["legal"], nodes_g)) in readme,
          "README result line for %s" % k)
    g("G2:kit-readme-solver-pin", "9193f5b6" in readme,
      "ladder kit README pins the delegated solver sha prefix")
    g("G2:kit-readme-jsreplay-pin",
      "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
      in readme,
      "ladder kit README pins the jsreplay replica sha")
    # third-impl batch cross-SSOT (Part SL, 32/32)
    ti = json.load(open(rd(os.path.join("ti", "audit-k09k43-summary.json"))))
    g("G2:third-impl-all-pass",
      ti.get("all_pass") is True and ti.get("rows_audited") == 32,
      "third-impl batch audit all_pass, 32 rows")
    for k in KEYS:
        lo, hi = TARGETS[k]
        key = "%s:%s" % (lo, hi)
        trow = ti["row_results"].get(k)
        nodes = rows[k]["expected"].split(",")[3]
        g("G2:%s:third-impl-verdict-level" % k,
          trow is not None and trow["key"] == key
          and trow["legal"] == int(rows[k]["legal"])
          and trow["third_impl_runs"] == 3
          and trow["third_impl_verdict"] == 1 == trow["replica_verdict"]
          and trow["verdict_level_agreement"] is True
          and trow["determinism_identical"] is True
          and str(trow["replica_resolution_nodes"]) == nodes,
          "third-impl verdict-level agreement, 3 runs, replica nodes %s"
          % nodes)
        rows[k]["third_impl_verdict_level_corroboration"] = True

    # ---- G3 anchors (byte pins + expectations machine-read from SK kit)
    ANCHOR_PINS = {}
    mp = rd(os.path.join("sk", "MANIFEST-sha256.txt"))
    for line in open(mp):
        parts = line.split()
        if len(parts) == 2 and parts[1].startswith("input/anchor-"):
            a = parts[1][len("input/"):-len(".input.csv")]
            ANCHOR_PINS[a] = parts[0]
    ANCHORS = dict(sk_rows["anchors"])
    ANCHOR_BUDGET = {a: sk_rows["anchors_runtime"][a][0]
                     for a in sorted(sk_rows["anchors_runtime"])}
    g("G3:anchor-inventory",
      sorted(ANCHOR_PINS) == sorted(ANCHORS) == sorted(ANCHOR_BUDGET)
      and sorted(ANCHORS) == ["anchor-af039", "anchor-aj001", "anchor-at2m"],
      "3 anchors pinned: %s" % ",".join(sorted(ANCHORS)))
    for a in sorted(ANCHORS):
        p = rd(os.path.join("sk", "input", "%s.input.csv" % a))
        got = sha256(p)
        g("G3:%s:byte-pin-vs-SK-kit-MANIFEST" % a, got == ANCHOR_PINS[a],
          "sha256 == published SK kit MANIFEST pin")
        ac = open(p).read().strip().split(",")
        g("G3:%s:input-row-spec-shape" % a,
          ac[0] == "target" and ac[1] == "0" and ac[2] == "5"
          and len(ac) == 11,
          "anchor row spec %s" % ",".join(ac[:5]))
        g("G3:%s:expected-vs-SK-kit-anchors" % a,
          sk_rows["anchors_runtime"][a][1] == ANCHORS[a],
          "SK kit anchors block == %s" % ANCHORS[a])

    # ---- G4 freshness vs canonical head (Part EW head of record)
    canon = rd("canon.cache")
    got = sha256(canon)
    g("G4:canonical-head-sha256", got == CANON_HEAD_SHA256,
      "Part EW head of record %s (%s)" % (CANON_HEAD_LABEL, CANON_HEAD_PATH))
    data_lines = [l for l in open(canon).read().splitlines()
                  if l.startswith("s5verdict,")]
    g("G4:canonical-row-count", len(data_lines) == 6797,
      "s5verdict rows=%d (Part EW close-out: 6,797)" % len(data_lines))
    verdicts = {}
    for l in data_lines:
        parts = l.split(",")
        verdicts[parts[4]] = verdicts.get(parts[4], 0) + 1
    g("G4:canonical-census-WIN197-LOSS6600",
      verdicts.get("1") == 197 and verdicts.get("2") == 6600,
      "WIN(1)=%d LOSS(2)=%d" % (verdicts.get("1", 0), verdicts.get("2", 0)))
    canon_pairs = set()
    for l in data_lines:
        parts = l.split(",")
        canon_pairs.add((parts[1], parts[2]))
    for k in KEYS:
        lo, hi = TARGETS[k]
        g("G4:%s:fresh-not-in-canonical-head" % k,
          (lo, hi) not in canon_pairs,
          "row (%s,%s) absent from %s" % (lo, hi, CANON_HEAD_LABEL))

    # ---- G8 emit kit bytes
    in_dir = os.path.join(KIT, "input")
    if os.path.isdir(in_dir):
        shutil.rmtree(in_dir)
    os.makedirs(in_dir)
    for k in KEYS:
        dst = os.path.join(in_dir, "%s.input.csv" % k)
        shutil.copyfile(rd(os.path.join("p4", "input",
                                       "batch-%s.input.csv" % k)), dst)
        g("G8:%s:input-clone-byte-verified" % k,
          sha256(dst) == rows[k]["input_sha256"], "sha256 %s" % sha256(dst))
    for a in sorted(ANCHORS):
        dst = os.path.join(in_dir, "%s.input.csv" % a)
        shutil.copyfile(rd(os.path.join("sk", "input", "%s.input.csv" % a)), dst)
        g("G8:%s:input-clone-byte-verified" % a,
          sha256(dst) == ANCHOR_PINS[a], "sha256 %s" % sha256(dst))

    gate_rows = {
        "part": "SM",
        "schema": "n11-sixthcost-parked4-cppgate-rows-v1",
        "gate_source": {
            "commit": gate_source["commit"],
            "path": gate_source["path"],
            "sha256": GATE_SOURCE_PIN_CPP,
            "header_pins": {
                "kyouen_residual_micro.hpp": GATE_SOURCE_PIN_HPP,
                "n11_s5_quarantine.hpp": GATE_SOURCE_PIN_Q,
            },
        },
        "anchors": dict(ANCHORS),
        "anchors_runtime": {a: [ANCHOR_BUDGET[a], ANCHORS[a]]
                            for a in sorted(ANCHORS)},
        "targets": {
            k: {
                "key_lo": TARGETS[k][0], "key_hi": TARGETS[k][1],
                "budget": rows[k]["budget"],
                "expected": rows[k]["expected"],
                "row_spec": rows[k]["row_spec"],
                "input_sha256": rows[k]["input_sha256"],
                "raw_p1_sha256": rows[k]["raw_p1_sha256"],
                "raw_p2_sha256": rows[k]["raw_p2_sha256"],
                "margin_sha256": rows[k]["margin_sha256"],
                "run3_verify_sha256": rows[k]["run3_verify_sha256"],
                "third_impl_verdict_level_corroboration": True,
            } for k in KEYS
        },
        "canonical_head": {
            "label": CANON_HEAD_LABEL,
            "sha256": CANON_HEAD_SHA256,
            "path": CANON_HEAD_PATH,
            "rows": 6797,
            "census": {"WIN": 197, "LOSS": 6600},
            "targets_fresh_vs": CANON_HEAD_LABEL,
        },
        "gates": {name: {"status": "PASS"} for name in sorted(gates)},
    }
    with open(os.path.join(in_dir, "gate-rows.json"), "w") as f:
        json.dump(gate_rows, f, indent=1, sort_keys=True)
        f.write("\n")

    # audit_gate.py: machine transform of the published SK kit audit script
    template_path = rd(os.path.join("sk", "scripts", "audit_gate.py"))
    SK_MANIFEST_AUDIT_PIN = None
    for line in open(mp):
        parts = line.split()
        if len(parts) == 2 and parts[1] == "scripts/audit_gate.py":
            SK_MANIFEST_AUDIT_PIN = parts[0]
    g("G8:audit-template-pin-vs-SK-MANIFEST",
      sha256(template_path) == SK_MANIFEST_AUDIT_PIN,
      "template == published SK kit audit script sha256 %s"
      % SK_MANIFEST_AUDIT_PIN)
    audit = make_audit_text(template_path, gate_rows, ANCHOR_PINS)
    with open(os.path.join(KIT, "scripts", "audit_gate.py"), "w") as f:
        f.write(audit)

    # gate_runner.sh: runner rev2 byte-clone, only the comment block names SM
    runner_path = rd(os.path.join("sk", "scripts", "gate_runner.sh"))
    SK_MANIFEST_RUNNER_PIN = None
    for line in open(mp):
        parts = line.split()
        if len(parts) == 2 and parts[1] == "scripts/gate_runner.sh":
            SK_MANIFEST_RUNNER_PIN = parts[0]
    g("G8:runner-template-pin-vs-SK-MANIFEST",
      sha256(runner_path) == SK_MANIFEST_RUNNER_PIN,
      "template == published SK kit runner sha256 %s"
      % SK_MANIFEST_RUNNER_PIN)
    src = open(runner_path, "r").read()
    src2 = src.replace(
        "# Part SK (sixth-cost) C++ scrutiny gate runner. Usage: "
        "gate_runner.sh <key> <budget> <expected-fields>",
        "# Part SM (parked4 L50M WIN rows) C++ scrutiny gate runner. "
        "Usage: gate_runner.sh <key> <budget> <expected-fields>")
    src2 = src2.replace("block names Part SK).",
                        "block names Part SM).")
    if src2.count("Part SM") != 2 or "Part SK" in src2:
        fail("runner transform: comment-block-only diff violated")
    if sum(1 for a, b in zip(src.splitlines(), src2.splitlines())
           if a != b) != 2 or len(src.splitlines()) != len(src2.splitlines()):
        fail("runner transform: diff must be exactly two comment lines")
    rpath = os.path.join(KIT, "scripts", "gate_runner.sh")
    with open(rpath, "w") as f:
        f.write(src2)
    os.chmod(rpath, 0o755)

    # tamper_battery.sh: machine transform of the published SK kit battery
    tb_path = rd(os.path.join("sk", "tamper_battery.sh"))
    SK_MANIFEST_TAMPER_PIN = None
    for line in open(mp):
        parts = line.split()
        if len(parts) == 2 and parts[1] == "tamper_battery.sh":
            SK_MANIFEST_TAMPER_PIN = parts[0]
    g("G8:tamper-template-pin-vs-SK-MANIFEST",
      sha256(tb_path) == SK_MANIFEST_TAMPER_PIN,
      "template == published SK kit tamper battery sha256 %s"
      % SK_MANIFEST_TAMPER_PIN)
    tsrc = open(tb_path, "r").read()
    t2 = tsrc.replace("# Part SK (sixth-cost) tamper battery.",
                      "# Part SM (parked4 L50M WIN rows) tamper battery.")
    t2 = t2.replace("/tmp/sk_", "/tmp/sm_")
    t2 = t2.replace(
        "T1-START break audit ROWS pin k01 nodes 10369650->10369651",
        "T1-START break audit ROWS pin k13 nodes 16402480->16402481")
    t2 = t2.replace("s/87,15000000,2,10369650/87,15000000,2,10369651/",
                    "s/95,50000000,1,16402480/95,50000000,1,16402481/")
    t2 = t2.replace("'\"G3:k01\": {\"status\": \"FAIL\"'",
                    "'\"G3:k13\": {\"status\": \"FAIL\"'")
    t2 = t2.replace("g3=d['gates']['G3:k01']; print(\"T1 G3:k01 status:\","
                    "g3.get('status'),\"| detail:\",g3.get('detail'))",
                    "g3=d['gates']['G3:k13']; print(\"T1 G3:k13 status:\","
                    "g3.get('status'),\"| detail:\",g3.get('detail'))")
    t2 = t2.replace("out={'t1':{'g3_k01':g3}}", "out={'t1':{'g3_k13':g3}}")
    t2 = t2.replace(
        "T2-START break raw k01.p1 nodes 10369650->10369651",
        "T2-START break raw k13.p1 nodes 16402480->16402481")
    t2 = t2.replace("R=output/raw/k01.p1.out", "R=output/raw/k13.p1.out")
    t2 = t2.replace("s/,15000000,2,10369650/,15000000,2,10369651/",
                    "s/,50000000,1,16402480/,50000000,1,16402481/")
    t2 = t2.replace("g2=d['gates']['G2:k01']; g3=d['gates']['G3:k01']\n"
                    "print(\"T2 G2:k01 status:\",g2.get('status'),"
                    "\"G3 status:\",g3.get('status'))",
                    "g2=d['gates']['G2:k13']; g3=d['gates']['G3:k13']\n"
                    "print(\"T2 G2:k13 status:\",g2.get('status'),"
                    "\"G3 status:\",g3.get('status'))")
    t2 = t2.replace(
        "echo \"2026-11-26T00:00:00Z PHANTOM-KEY GATE-PASS "
        "87,15000000,2,10369650 (fabricated)\" >> $S",
        "echo \"2026-11-26T00:00:00Z PHANTOM-KEY GATE-PASS "
        "95,50000000,1,16402480 (fabricated)\" >> $S")
    t2 = t2.replace(
        "# ---- T1: audit ROWS pin (expected nodes) tampered "
        "10369650 -> 10369651",
        "# ---- T1: audit ROWS pin (expected nodes) tampered "
        "16402480 -> 16402481")
    t2 = t2.replace("# ---- T2: raw k01.p1.out nodes 10369650 -> 10369651",
                    "# ---- T2: raw k13.p1.out nodes 16402480 -> 16402481")
    t2 = t2.replace('say "T2 pin-assert k01.p1.out sha256=$pin2"',
                    'say "T2 pin-assert k13.p1.out sha256=$pin2"')
    if "k01" in t2 or "10369650" in t2 or "15000000,2" in t2:
        fail("tamper transform: k01/SK quadruple residue in SM battery")
    if t2.count("k13") < 6:
        fail("tamper transform: k13 rows not wired")
    tpath = os.path.join(KIT, "tamper_battery.sh")
    with open(tpath, "w") as f:
        f.write(t2)
    os.chmod(tpath, 0o755)

    # ASCII-only assert on every emitted kit byte (push-transport lesson)
    for root, _, fs in os.walk(KIT):
        for fn in fs:
            p = os.path.join(root, fn)
            data = open(p, "rb").read()
            if re.search(rb"[^\x00-\x7F]", data):
                fail("non-ASCII byte in emitted kit file %s" % p)

    out = {
        "part": "SM",
        "gates_total": len(gates),
        "gates": gates,
        "targets": {k: rows[k]["expected"] for k in KEYS},
        "anchors": ANCHORS,
        "kit_pins": {
            "input/k13.input.csv": rows["k13"]["input_sha256"],
            "input/k19.input.csv": rows["k19"]["input_sha256"],
            "input/anchor-at2m.input.csv": ANCHOR_PINS["anchor-at2m"],
            "input/anchor-aj001.input.csv": ANCHOR_PINS["anchor-aj001"],
            "input/anchor-af039.input.csv": ANCHOR_PINS["anchor-af039"],
            "input/gate-rows.json": sha256(
                os.path.join(in_dir, "gate-rows.json")),
            "scripts/audit_gate.py": sha256(
                os.path.join(KIT, "scripts", "audit_gate.py")),
            "scripts/gate_runner.sh": sha256(rpath),
            "tamper_battery.sh": sha256(tpath),
        },
    }
    print("maker: ALL %d gates PASS" % len(gates))
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


def make_audit_text(template_path, gate_rows, anchor_pins):
    rows_py = {}
    prov = {}
    for k, v in sorted(gate_rows["targets"].items()):
        rows_py[k] = [
            v["budget"], v["expected"], v["input_sha256"],
            "parked4 kit input/batch-%s.input.csv (sixth-cost parked-4-keys "
            "S5 L50M ladder kit; input SSOT)" % k]
        prov[k] = (
            "parked4 kit output/raw/l50m-run1-%s-%s.out.csv (published "
            "replica %s); two-pass node-exact vs l50m-run2-%s-%s.out.csv; "
            "third-impl verdict-level agreement published (batch 32/32, "
            "k-row x3 runs)" % (v["key_lo"], v["key_hi"], v["expected"],
                                v["key_lo"], v["key_hi"]))
    for a in sorted(gate_rows["anchors_runtime"]):
        budget, exp = gate_rows["anchors_runtime"][a]
        rows_py[a] = [
            budget, exp, anchor_pins[a],
            "SK kit input/%s.input.csv (byte-clone; == EQ/EN/EO/EV kit "
            "input; SK kit MANIFEST-sha256.txt pin)" % a]
        prov[a] = ("EV/SK kit raw condition (budget-ceiling baseline); == "
                   "SK kit anchors block")
    src = open(template_path, "r").read()
    lines = src.splitlines(True)
    out_lines = []
    state = 0  # 0: copy until ROWS=; 1: skip until RAW_PROV=; 2: skip until
    # the REPLAY block; 3: copy the rest verbatim
    for ln in lines:
        if state == 0:
            if ln.startswith("ROWS = {"):
                out_lines.append("ROWS = %s\n" % json.dumps(rows_py, indent=1))
                out_lines.append("\n")
                state = 1
            else:
                out_lines.append(ln)
        elif state == 1:
            if ln.startswith("RAW_PROV = {"):
                out_lines.append("RAW_PROV = %s\n"
                                 % json.dumps(prov, indent=1))
                state = 2
        elif state == 2:
            if ln.startswith("REPLAY = re.compile"):
                out_lines.append(ln)
                state = 3
        else:
            out_lines.append(ln)
    if state != 3:
        fail("audit template transform did not reach the tail (state=%d)"
             % state)
    text = "".join(out_lines)
    doc_start = text.index('"""')
    doc_end = text.index('"""', doc_start + 3) + 3
    sm_doc = '''"""Part SM (parked4 L50M WIN rows C++ scrutiny gate) fail-closed
machine audit (k13/k19 delegated rows + 3 calibration anchors).

EQ rev4 structure kept via the published SK kit audit script template
(10-capture-group REPLAY regex asserted at import; see input/gate-rows.json
for the machine-derived pins this audit derives from). Gates: G1 raw shape
(replay row + terminal replay_done + driver headers), G2 per-row determinism
(p1 == p2 except wall_s), G3 published-raw pins (legal,budget,result,nodes),
G4 gate-status accounting, G5 input byte-clones (parked4 ladder kit input/
for k13/k19; SK kit input/ == SK kit MANIFEST pins for the anchors).

No verdict is consumed: the 2 rows stay UNCONSUMED labels; they only BECOME
adoption-eligible for a separately declared adoption Part. 11x11, the
two-stone root {60,27}, and its remaining third moves 100/108 stay UNKNOWN
throughout.
"""'''
    text = text[:doc_start] + sm_doc + text[doc_end:]
    text = text.replace(
        '"part": "SK", "schema": '
        '"n11-sixthcost-exclusive-cppgate-audit-v1"',
        '"part": "SM", "schema": '
        '"n11-sixthcost-parked4-cppgate-audit-v1"')
    for residue in ("k01", "k02", "k03", "k04", "k05", "k06", "k07", "k08",
                    "Part SK", "sixth-cost exclusive"):
        if residue in text.split("RAW_PROV")[0] + text.split("RAW_PROV")[2].split("def main")[0]:
            fail("audit transform: SK residue %r outside RAW_PROV" % residue)
    assert "ROWS = " in text and "RAW_PROV = " in text
    assert '"part": "SM"' in text
    return text


if __name__ == "__main__":
    sys.exit(main())
