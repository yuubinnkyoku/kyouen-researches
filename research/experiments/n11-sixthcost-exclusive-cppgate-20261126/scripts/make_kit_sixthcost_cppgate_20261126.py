#!/usr/bin/env python3
"""Part SK (sixth-cost) C++ scrutiny gate kit maker (2026-11-26).

Assembles the fail-closed kit for the delegated C++ second-implementation
scrutiny gate on the sixth-cost exclusive-probe batch rows k01..k08 whose
expected C++ quadruples have been pinned and delegated since 2026-11-21
(probe README adoption-requirement lines; win-finding-ifadopted-k08.json
adoption_requirement). This executes the long-waiting delegated gate that
every sixth-cost lane session recorded as "no C++ toolchain in this sandbox;
delegated to the scrutiny owner / external C++ resource".

Follows the EN/EO/EQ/ET/EV kit lineage (same runner rev2 bytes, same
EQ rev4 audit structure). Machine-derived, no per-row pin hand-typed
(EP pin policy).

Gates (all must PASS; any failure -> rc=1, no kit emit):
  G0  gate source pins: cpp/solvers/kyouen_dfpn_root.cpp sha256 9193f5b6...
      (commit 154f3b7a67b97e13acbaee8b04dc74ddca728d19), headers
      kyouen_residual_micro.hpp 5976935d... / n11_s5_quarantine.hpp
      2e36d694... at the same commit.
  G1  probe-kit SSOT discipline for k01..k08: input row-spec shape;
      published at15m-run1/run2 raws with the 10-capture-group REPLAY
      line; pair identity on every replay field except wall_s; at2m raw
      present; k07 resolved at the 2M stage (at2m pair, res=2); the
      voluntary run3-verify raws (k02/k03/k04/k05/k08) identical to run1
      except wall_s; status.log per-key accounting lines present.
  G2  cross-SSOT: the machine-extracted (legal,budget,result,nodes)
      quadruple per key agrees with (a) win-finding-ifadopted-k08.json
      adoption_requirement text + unconsumed_batch_rows, (b) the probe
      README delegated-target lines (all 8 row specs + the 9193f5b6 solver
      pin present), (c) published third-implementation audit summaries
      (verdict-level agreement for k01/k03, k04, k05, k06/k07/k08; k02 has
      NO published third-impl reproduction yet - recorded honestly, the
      C++ gate is itself the second implementation for k02).
  G3  anchors: byte pins from the published EV kit MANIFEST-sha256.txt
      (== EQ/EN/EO kit inputs) + expected anchor quadruples from the
      published gate-rows-ev.json anchors block.
  G4  freshness: canonical merged head sha256 6e49dd84... (Part EM
      close-out head of record, 6,792 s5verdict rows WIN192/LOSS6600);
      every target (lo,hi) pair absent from it (verdict-unconsumed rows).
  G8  emit kit bytes (inputs byte-clone + gate-rows.json + audit_gate.py).

No verdict is consumed by anything in this kit. The 8 rows stay UNCONSUMED
labels; the gate only makes the 5 WIN rows (k02/k03/k04/k05/k08) adoptable
by a separately declared adoption Part. The standard 11x11 empty board, the
two-stone root {60,27}, and its remaining third moves {100,108} stay
UNKNOWN throughout. nodes are bookkeeping, never verdicts.
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
    "SK_SSOT_ROOT",
    os.path.abspath(os.path.join(HERE, "..", "..", "..", "ssot")))

GATE_SOURCE_COMMIT = "154f3b7a67b97e13acbaee8b04dc74ddca728d19"
GATE_SOURCE_PINS = {
    "kyouen_dfpn_root.cpp":
        "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e",
    "kyouen_residual_micro.hpp":
        "5976935dcfccb9b5a26fa68f8de20868ce45363dd8c372dcd67d9b841167e7f5",
    "n11_s5_quarantine.hpp":
        "2e36d69481fafcde7aede8ae4fedf3d5477f91ee9846bcd4ae2975f32a4ba1a5",
}

CANON_HEAD_SHA256 = \
    "6e49dd841b7bfcb335d86ef2479c95f47ab7acbcf41ace389a8b8eb95c778c9d"
CANON_HEAD_LABEL = "6e49dd84"
CANON_HEAD_PATH = ("research/experiments/"
                   "n11-centralreply-emloss21-adoption-predecl-20261126/"
                   "output/merged-exact-s5-chain-plus-emloss21-20261126.cache")

KEYS = ["k%02d" % i for i in range(1, 9)]
TARGETS = {
    "k01": ("1297036692683751424", "1114112"),
    "k02": ("1297036692683751424", "68157440"),
    "k03": ("10376293541461626880", "65792"),
    "k04": ("10376293541461626888", "65536"),
    "k05": ("10376293541461757952", "65536"),
    "k06": ("10376293541462675456", "65536"),
    "k07": ("10376293542535368704", "65536"),
    "k08": ("10376293610182148096", "68719476736"),
}
BUDGET = {k: ("2000000" if k == "k07" else "15000000") for k in KEYS}

ANCHORS_EXP = {
    "anchor-at2m": "98,2000000,0,2000000",
    "anchor-aj001": "84,30000000,2,5156075",
    "anchor-af039": "89,30000000,2,19234232",
}
ANCHOR_BUDGET = {
    "anchor-at2m": "2000000",
    "anchor-aj001": "30000000",
    "anchor-af039": "30000000",
}
ANCHOR_EV_MANIFEST_PINS = None  # machine-extracted from the fetched EV kit
# MANIFEST-sha256.txt at maker time (no hand-typed pins: EP pin policy;
# a first draft hand-transcribed the aj001 pin with one wrong hex pair and
# the fail-closed byte-pin gate caught it - lesson enforced structurally)


def load_anchor_pins():
    pins = {}
    mp = rd(os.path.join("ev", "MANIFEST-sha256.txt"))
    for line in open(mp):
        parts = line.split()
        if len(parts) == 2 and parts[1].startswith("input/anchor-"):
            a = parts[1][len("input/"):-len(".input.csv")]
            pins[a] = parts[0]
    return pins
ANCHOR_PROV = ("EQ kit input/%(a)s.input.csv (byte-clone; == EN/EO/EV kit "
               "input; EV kit MANIFEST-sha256.txt pin)")

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
    global ANCHOR_EV_MANIFEST_PINS
    ANCHOR_EV_MANIFEST_PINS = load_anchor_pins()
    assert sorted(ANCHOR_EV_MANIFEST_PINS) == sorted(ANCHORS_EXP), \
        "EV kit MANIFEST must pin exactly the 3 anchor inputs: %r" % \
        sorted(ANCHOR_EV_MANIFEST_PINS)

    def g(name, ok, detail=""):
        gates[name] = {"status": "PASS" if ok else "FAIL", "detail": detail}
        if not ok:
            fail("gate %s FAIL: %s" % (name, detail))
        return ok

    # ---- G0 gate source pins
    for fn, pin in sorted(GATE_SOURCE_PINS.items()):
        p = rd(os.path.join("pinned", fn))
        got = sha256(p)
        g("G0:" + fn, got == pin,
          "sha256 %s %s" % (got, "==" if got == pin else "!= " + pin))

    # ---- G1 probe-kit SSOT discipline
    rows = {}
    raw_dir = rd(os.path.join("probe", "raw"))
    for k in KEYS:
        lo, hi = TARGETS[k]
        ipath = rd(os.path.join("probe", "input", k + ".input.csv"))
        icont = open(ipath).read().strip()
        fields = icont.split(",")
        ok = (fields[0] == "target" and fields[1] == "0"
              and fields[2] == "5" and fields[3] == lo and fields[4] == hi
              and fields[5].isdigit() and int(fields[5]) > 0
              and fields[6:] == ["0", "0", "0", "0", "0"])
        g("G1:%s:input-row-spec-shape" % k, ok,
          "spec=%s" % icont if ok else "bad row spec %r" % icont)
        legal = fields[5]
        r1 = parse_replay(os.path.join(raw_dir, "at15m-run1-%s.out.csv" % k))
        r2 = parse_replay(os.path.join(raw_dir, "at15m-run2-%s.out.csv" % k))
        g("G1:%s:15m-pair-identity-except-wall_s" % k,
          nowall(r1) == nowall(r2),
          "run1=%s run2=%s" % (",".join(r1), ",".join(r2)))
        g("G1:%s:key-fields-in-raws" % k,
          r1[8] == lo and r1[9] == hi and r2[8] == lo and r2[9] == hi,
          "lo,hi in raws %s,%s" % (r1[8], r1[9]))
        g("G1:%s:input-legal==raw-legal" % k, legal == r1[2],
          "input=%s raw=%s" % (legal, r1[2]))
        g("G1:%s:15m-budget-field" % k, r1[4] == "15000000", r1[4])
        g("G1:%s:15m-run1==15m-run2-nodes" % k, r1[6] == r2[6],
          "run1 nodes=%s run2 nodes=%s" % (r1[6], r2[6]))
        g("G1:%s:15m-run1==15m-run2-result" % k, r1[5] == r2[5],
          "run1 result=%s run2 result=%s" % (r1[5], r2[5]))
        t2 = parse_replay(os.path.join(raw_dir, "at2m-%s.out.csv" % k))
        g("G1:%s:at2m-present-key" % k, t2[8] == lo and t2[9] == hi,
          "at2m key %s,%s" % (t2[8], t2[9]))
        g("G1:%s:at2m-budget-field" % k, t2[4] == "2000000", t2[4])
        if k == "k07":
            t2b = parse_replay(os.path.join(raw_dir,
                                            "at2m-run2-%s.out.csv" % k))
            g("G1:%s:at2m-pair-identity" % k, nowall(t2) == nowall(t2b),
              "k07 resolved at the 2M stage; determinism pair identical")
            g("G1:%s:res2m==2-nodes-1419823" % k,
              t2[5] == "2" and t2[6] == "1419823",
              "at2m result=%s nodes=%s" % (t2[5], t2[6]))
            g("G1:%s:at2m-vs-15m-agreement" % k,
              t2[5] == r1[5] and t2[6] == r1[6],
              "2M resolution == 15M cold pair (result %s, nodes %s)"
              % (r1[5], r1[6]))
            exp_quad = ",".join([t2[2], "2000000", t2[5], t2[6]])
        else:
            g("G1:%s:res2m-unknown-2M-ceiling" % k,
              t2[5] == "0" and t2[6] == "2000000",
              "at2m result=%s nodes=%s (unresolved at 2M, res2m=0)"
              % (t2[5], t2[6]))
            exp_quad = ",".join([r1[2], "15000000", r1[5], r1[6]])
        vpath = os.path.join(raw_dir, "at15m-run3-verify-%s.out.csv" % k)
        if os.path.isfile(vpath):
            rv = parse_replay(vpath)
            g("G1:%s:run3-verify-identity" % k,
              nowall(rv) == nowall(r1),
              "voluntary third cold run identical (except wall_s)")
            rows[k] = {"has_run3_verify": True}
        else:
            rows[k] = {"has_run3_verify": False}
        result1 = exp_quad.split(",")[2]
        g("G1:%s:expected-quadruple-derived" % k,
          exp_quad.split(",")[0] == legal
          and exp_quad.split(",")[1] == BUDGET[k]
          and result1 in ("1", "2"),
          "expected=%s (from published raws, %s stage)"
          % (exp_quad, "2M" if k == "k07" else "15M"))
        rows[k].update({
            "input_sha256": sha256(ipath),
            "row_spec": icont,
            "legal": legal,
            "budget": BUDGET[k],
            "expected": exp_quad,
            "raw_p1_sha256": sha256(os.path.join(
                raw_dir, "at15m-run1-%s.out.csv" % k)),
            "raw_p2_sha256": sha256(os.path.join(
                raw_dir, "at15m-run2-%s.out.csv" % k)),
        })

    # status.log accounting lines
    st = open(rd(os.path.join("probe", "raw", "status.log"))).read()
    for k in KEYS:
        nn = k[1:]
        nm = nn.lstrip("0") or nn  # the parent-batch keys 01/02 use "1"/"2"
        def has_any(*pats):
            return any(p in st for p in pats)
        ok = (has_any("done %s 2m rc=0" % nn,
                      "done %s 2m rc=0" % nm)
              and has_any("done %s 15m-run1 rc=0" % nn,
                          "done %s 15m-run1 rc=0" % nm)
              and has_any("done %s 15m-run2 rc=0" % nn,
                          "done %s 15m-run2 rc=0" % nm)
              and has_any("key %s status=" % nn, "key %s status=" % nm))
        # the parent-batch rows k01/k02 predate the start-line convention;
        # k03..k08 (first..fourth resumption rows) must carry their start line
        if k not in ("k01", "k02"):
            ok = ok and has_any("start %s " % nn, "start %s " % nm)
        g("G1:%s:status-log-lines" % k, ok, "key %s accounting lines" % nn)
    g("G1:status-log-k07-2m-run2",
      ("done 07 2m-run2 rc=0 res=2" in st), "k07 2M determinism pair line")
    for k in ("06", "07", "08"):
        keylines = " ".join(l for l in st.splitlines()
                            if (("key %s status=" % k) in l))
        mode = "WIN-halt" if k == "08" else "done"
        g("G1:status-log-k%s-mode" % k, mode in keylines,
          "key %s batch line mode (%s)" % (k, mode))

    # ---- G2 cross-SSOT
    wit = json.load(open(rd(os.path.join(
        "probe", "out", "win-finding-ifadopted-k08.json"))))
    req = wit["finding"]["adoption_requirement"]
    for k in KEYS:
        lo, hi = TARGETS[k]
        exp = rows[k]["expected"]
        result = exp.split(",")[2]
        nodes = exp.split(",")[3]
        nodes_g = "{:,}".format(int(nodes))
        if k in ("k06", "k07", "k08"):
            spec = "target,0,5,%s,%s," % (lo, hi)
            g("G2:%s:witness-target-text" % k, spec in req,
              "adoption_requirement pins the full row spec (fresh k06..k08 "
              "rows)")
            g("G2:%s:witness-expected-text" % k,
              ("result %s, nodes %s" % (result, nodes_g)) in req,
              "adoption_requirement pins 'result %s, nodes %s'"
              % (result, nodes_g))
        else:
            g("G2:%s:witness-expected-text-short" % k,
              ("k%s expected %s / %s" % (k[1:], result, nodes_g)) in req,
              "adoption_requirement pins 'k%s expected %s / %s'"
              % (k[1:], result, nodes_g))
        ubr = [r for r in wit["unconsumed_batch_rows"]
               if r["key"] == "%s:%s" % (lo, hi)]
        ok = (len(ubr) == 1 and str(ubr[0]["verdict"]) == result
              and str(ubr[0]["nodes"]) == nodes)
        g("G2:%s:witness-unconsumed-row" % k, ok,
          "unconsumed_batch_rows verdict=%s nodes=%s" % (result, nodes))
        readme = open(rd(os.path.join("probe", "README.md"))).read()
        spec_an = "target,0,5,%s,%s" % (lo, hi)
        g("G2:%s:probe-readme-delegated-target" % k, spec_an in readme,
          "probe README delegated-target line present")
    readme = open(rd(os.path.join("probe", "README.md"))).read()
    g("G2:probe-readme-solver-pin", "9193f5b6" in readme,
      "probe README pins the delegated solver sha prefix")
    g("G2:witness-solver-pin", "9193f5b6" in req,
      "witness adoption_requirement pins the delegated solver sha prefix")
    # third-impl cross-SSOT
    ti_summaries = {
        "k01": rd(os.path.join("ti", "audit-summary.json")),
        "k03": rd(os.path.join("ti", "audit-summary.json")),
        "k04": rd(os.path.join("ti", "audit-k04-summary.json")),
        "k05": rd(os.path.join("ti", "audit-k05-summary.json")),
        "k06": rd(os.path.join("ti", "audit-k06k07k08-summary.json")),
        "k07": rd(os.path.join("ti", "audit-k06k07k08-summary.json")),
        "k08": rd(os.path.join("ti", "audit-k06k07k08-summary.json")),
    }
    for k, p in sorted(ti_summaries.items()):
        d = json.load(open(p))
        covered = any(k in str(row) for row in d.get("row_results", []))
        g("G2:%s:third-impl-verdict-level" % k,
          bool(d.get("all_pass")) and covered,
          "third-impl audit all_pass=%s covers %s" % (d.get("all_pass"), k))
    d01 = json.dumps(json.load(open(rd(os.path.join(
        "ti", "audit-summary.json")))))
    g("G2:k02-no-third-impl-honest-disclosure", '"k02' not in d01,
      "k02 has no published third-impl reproduction; the C++ gate (this "
      "Part) is the second implementation for k02; recorded, not blocked")
    for k in KEYS:
        rows[k]["third_impl_verdict_level_corroboration"] = (k != "k02")

    # ---- G3 anchors
    ev_rows = json.load(open(rd(os.path.join(
        "ev", "input", "gate-rows-ev.json"))))
    for a in sorted(ANCHORS_EXP):
        p = rd(os.path.join("ev", "input", a + ".input.csv"))
        got = sha256(p)
        g("G3:%s:byte-pin-vs-EV-kit-MANIFEST" % a,
          got == ANCHOR_EV_MANIFEST_PINS[a],
          "sha256 == published EV kit MANIFEST pin")
        g("G3:%s:expected-vs-gate-rows-ev" % a,
          ev_rows["anchors"][a] == ANCHORS_EXP[a],
          "EV kit anchors block == %s" % ev_rows["anchors"][a])
        ac = open(p).read().strip().split(",")
        g("G3:%s:input-row-spec-shape" % a,
          ac[0] == "target" and ac[2] == "5" and len(ac) == 11,
          "anchor row spec %s" % ",".join(ac[:5]))

    # ---- G4 freshness vs canonical head
    canon = rd("canon.cache")
    got = sha256(canon)
    g("G4:canonical-head-sha256", got == CANON_HEAD_SHA256,
      "Part EM head of record %s (%s)" % (CANON_HEAD_LABEL, CANON_HEAD_PATH))
    data_lines = [l for l in open(canon).read().splitlines()
                  if l.startswith("s5verdict,")]
    g("G4:canonical-row-count", len(data_lines) == 6792,
      "s5verdict rows=%d (Part EM close-out: 6,792)" % len(data_lines))
    verdicts = {}
    for l in data_lines:
        parts = l.split(",")
        verdicts[parts[4]] = verdicts.get(parts[4], 0) + 1
    g("G4:canonical-census-WIN192-LOSS6600",
      verdicts.get("1") == 192 and verdicts.get("2") == 6600,
      "WIN(1)=%d LOSS(2)=%d" % (verdicts.get("1", 0),
                                verdicts.get("2", 0)))
    canon_pairs = set()
    for l in data_lines:
        parts = l.split(",")
        canon_pairs.add((parts[1], parts[2]))
    for k in KEYS:
        lo, hi = TARGETS[k]
        g("G4:%s:fresh-not-in-canonical-head" % k,
          (lo, hi) not in canon_pairs,
          "row (%s,%s) absent from %s" % (lo, hi, CANON_HEAD_LABEL))

    # ---- G8 emit
    in_dir = os.path.join(KIT, "input")
    if os.path.isdir(in_dir):
        shutil.rmtree(in_dir)
    os.makedirs(in_dir)
    for k in KEYS:
        shutil.copyfile(rd(os.path.join("probe", "input", k + ".input.csv")),
                        os.path.join(in_dir, k + ".input.csv"))
        got = sha256(os.path.join(in_dir, k + ".input.csv"))
        g("G8:%s:input-clone-byte-verified" % k,
          got == rows[k]["input_sha256"], "sha256 %s" % got)
    for a in sorted(ANCHORS_EXP):
        shutil.copyfile(rd(os.path.join("ev", "input", a + ".input.csv")),
                        os.path.join(in_dir, a + ".input.csv"))
        got = sha256(os.path.join(in_dir, a + ".input.csv"))
        g("G8:%s:input-clone-byte-verified" % a,
          got == ANCHOR_EV_MANIFEST_PINS[a], "sha256 %s" % got)
    gate_rows = {
        "part": "SK",
        "schema": "n11-sixthcost-exclusive-cppgate-rows-v1",
        "gate_source": {
            "commit": GATE_SOURCE_COMMIT,
            "path": "cpp/solvers/kyouen_dfpn_root.cpp",
            "sha256": GATE_SOURCE_PINS["kyouen_dfpn_root.cpp"],
            "header_pins": {
                "kyouen_residual_micro.hpp":
                    GATE_SOURCE_PINS["kyouen_residual_micro.hpp"],
                "n11_s5_quarantine.hpp":
                    GATE_SOURCE_PINS["n11_s5_quarantine.hpp"],
            },
        },
        "anchors": dict(ANCHORS_EXP),
        "anchors_runtime": {
            a: [ANCHOR_BUDGET[a], ANCHORS_EXP[a]] for a in sorted(ANCHORS_EXP)
        },
        "targets": {
            k: {
                "key_lo": TARGETS[k][0],
                "key_hi": TARGETS[k][1],
                "budget": rows[k]["budget"],
                "expected": rows[k]["expected"],
                "row_spec": rows[k]["row_spec"],
                "input_sha256": rows[k]["input_sha256"],
                "raw_p1_sha256": rows[k]["raw_p1_sha256"],
                "raw_p2_sha256": rows[k]["raw_p2_sha256"],
                "has_run3_verify": rows[k]["has_run3_verify"],
                "third_impl_verdict_level_corroboration":
                    rows[k]["third_impl_verdict_level_corroboration"],
            } for k in KEYS
        },
        "canonical_head": {
            "label": CANON_HEAD_LABEL,
            "sha256": CANON_HEAD_SHA256,
            "path": CANON_HEAD_PATH,
            "rows": 6792,
            "census": {"WIN": 192, "LOSS": 6600},
            "targets_fresh_vs": CANON_HEAD_LABEL,
        },
        "gates": {name: {"status": "PASS"} for name in sorted(gates)},
    }
    with open(os.path.join(in_dir, "gate-rows.json"), "w") as f:
        json.dump(gate_rows, f, indent=1, sort_keys=True)
        f.write("\n")
    audit = make_audit_text(gate_rows)
    apath = os.path.join(KIT, "scripts", "audit_gate.py")
    with open(apath, "w") as f:
        f.write(audit)
    out = {
        "part": "SK",
        "gates_total": len(gates),
        "gates": gates,
        "targets": {k: rows[k]["expected"] for k in KEYS},
        "anchors": ANCHORS_EXP,
    }
    print("maker: ALL %d gates PASS" % len(gates))
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


def make_audit_text(gate_rows):
    rows_py = {}
    prov = {}
    for k, v in sorted(gate_rows["targets"].items()):
        rows_py[k] = [
            v["budget"], v["expected"], v["input_sha256"],
            "probe kit input/%s.input.csv (sixth-cost exclusive probe "
            "batch; input byte-pin registry SSOT)" % k]
        prov[k] = (
            "probe kit output/raw/at15m-run1-%s.out.csv (published replica "
            "%s); two-pass node-exact vs at15m-run2-%s.out.csv%s" % (
                k, v["expected"], k,
                "; third-impl verdict-level agreement published"
                if v["third_impl_verdict_level_corroboration"]
                else "; NO published third-impl reproduction (k02): the C++ "
                     "gate IS the second implementation for this row"))
    for a in sorted(gate_rows["anchors_runtime"]):
        budget, exp = gate_rows["anchors_runtime"][a]
        rows_py[a] = [
            budget, exp, ANCHOR_EV_MANIFEST_PINS[a], ANCHOR_PROV % {"a": a}]
        prov[a] = ("EQ kit raw condition (budget-ceiling baseline); == EV "
                   "kit anchors block")
    template = open(rd(os.path.join("ev", "scripts", "audit_gate.py"))).read()
    lines = template.splitlines(True)
    out_lines = []
    state = 0  # 0: copy until ROWS=; 1: skip until RAW_PROV=; 2: skip until
    # the `# published raw provenance...`/`REPLAY` block end, i.e. until the
    # line `def sha256(path):`; 3: copy the rest verbatim
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
                out_lines.append("RAW_PROV = %s\n" % json.dumps(prov, indent=1))
                state = 2
        elif state == 2:
            if ln.startswith("REPLAY = re.compile"):
                out_lines.append(ln)
                state = 3
        else:
            out_lines.append(ln)
    if state != 3:
        fail("audit template transform did not reach the tail "
             "(state=%d)" % state)
    text = "".join(out_lines)
    # docstring header: replaced below by SK-specific text (disclosed diff
    # vs the EV audit template: module docstring + ROWS/RAW_PROV only)
    new_doc = '"""Part SK (sixth-cost exclusive C++ scrutiny gate) '
    doc_start = text.index('"""')
    doc_end = text.index('"""', doc_start + 3) + 3
    old_block = text[:doc_end]
    sk_doc = '''"""Part SK (sixth-cost exclusive C++ scrutiny gate) fail-closed machine
audit (k01..k08 delegated rows + 3 calibration anchors).

EQ rev4 structure kept (10-capture-group REPLAY regex asserted at import;
see input/gate-rows.json for the machine-derived pins this audit derives
from). Gates: G1 raw shape (replay row + terminal replay_done + driver
headers), G2 per-row determinism (p1 == p2 except wall_s), G3 published-raw
pins (legal,budget,result,nodes), G4 gate-status accounting, G5 input
byte-clones (probe kit input/ for k01..k08; EQ kit input/ == EV kit
MANIFEST pins for the anchors).

No verdict is consumed: the 8 rows stay UNCONSUMED labels; the 5 WIN rows
only BECOME adoptable. 11x11, the two-stone root {60,27}, and its
remaining third moves {100,108} stay UNKNOWN throughout.
"""'''
    text = text[:doc_start] + sk_doc + text[doc_end:]
    text = text.replace('"part": "EV", "schema": '
                        '"n11-centralreply-cppgate-wins41164-audit-v1"',
                        '"part": "SK", "schema": '
                        '"n11-sixthcost-exclusive-cppgate-audit-v1"')
    assert "ROWS = " in text and "RAW_PROV = " in text
    assert '"part": "SK"' in text
    return text


if __name__ == "__main__":
    sys.exit(main())
