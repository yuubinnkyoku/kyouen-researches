#!/usr/bin/env python3
"""Part EV fail-closed kit maker: C++ scrutiny gate for the FOUR unconsumed
closure-batch WIN rows b018 / d002 / e002 / f017 (classes 16757 / 20421 /
16371 / 12264 batches 1/3/4/5; probe-level WIN, third-implementation
corroborated 2026-11-22, C++ gate pending since - "scrutiny owner pending").

Every gate must PASS before any kit file is emitted (fail-closed; rc=1 on ANY
drift). No per-file sha is hand-typed into the emitted kit: every pin is
machine-extracted at emit time (Part EP pin policy).

Sources (all fetched from published bytes on main and recorded by sha256 in
the emitted registry):
  W4  batch kits  research/experiments/n11-centralreply-closure-class{16757,
      20421,16371-batch4,12264-batch5}-20261122/ - the published jsreplay
      replica probe raws of the four targets (2-pass node-exact @15M) plus
      batch-keys.json SSOT and status.log.
  T   third-impl reverify kit n11-centralreply-closure-wins-thirdimpl-reverify-20261122
      (rows.json + output/targets/<key>.{a,b}.out) - the independent
      third-implementation verdict-level corroboration of the same four rows.
  EQ  EQ kit subset  research/experiments/n11-centralreply-closure-class30345-cppgate-20261125/
      (MANIFEST-pinned runner/audit bytes lineage + the 3 calibration anchors
      of the same EN/EO/EQ lineage).
  ER  canonical merged head merged-exact-s5-chain-plus-erwin18-20261125.cache
      9c4dd94e... (6,765 rows WIN186/LOSS6579) - freshness reference.
  S0  gate source  cpp/solvers/kyouen_dfpn_root.cpp at commit
      154f3b7a67b97e13acbaee8b04dc74ddca728d19 with headers (pins asserted).

Gates:
  G0  gate-source pins.
  G1  per-target batch-kit verification: 10-group replay rows p1/p2 identical
      except wall_s; forbidden-quadruples telemetry; input CSV == SSOT row;
      batch-keys.json lo/hi/legal match; status.log PASS triple == raw
      (budget,result,nodes) and the WIN-HALT line marks result==1.
  G2  third-impl cross-SSOT: rows.json replica quadruples == batch raws, and
      the two third-implementation passes (a/b) of each target agree on
      verdict WIN (result 1) with identical expansion counts.
  G3  EQ subset byte verification vs the EQ MANIFEST pins + anchor
      quadruples regenerated from the EQ raws.
  G4  freshness: the four (lo,hi) keys absent from the canonical merged head
      9c4dd94e (6,765/186/6579).
  G8  emit: input CSVs byte-cloned (batch + EQ anchor bytes), runner (EQ
      bytes, comment block names Part EV - disclosed), audit (EQ rev4 gate
      structure, ROWS/RAW_PROV regenerated, EV provenance), registry
      gate-rows-ev.json.
"""
import hashlib, json, os, re, shutil, sys

KIT = os.path.dirname(os.path.abspath(__file__)) + "/.."
KIT = os.path.abspath(KIT)
S = os.path.join(KIT, "sources")
W4 = os.path.join(S, "win4")
THIRD = os.path.join(S, "thirdimpl")
EQK = os.path.join(S, "eqkit")
ER = os.path.join(S, "erchain")
GSRC = os.path.join(S, "gatesrc")

TARGETS = [
    ("b018", "b1", 16757),
    ("d002", "b3", 20421),
    ("e002", "b4", 16371),
    ("f017", "b5", 12264),
]

def die(msg):
    sys.stderr.write("FAIL: %s\n" % msg)
    sys.exit(1)

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def parse_manifest(path):
    pins = {}
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) != 3:
            die("MANIFEST parse: %r" % line)
        sh, size, rel = parts
        pins[rel] = (sh, int(size))
    return pins

REPLAY = re.compile(r"^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),([0-9.]+),(\d+),(\d+)$")
assert REPLAY.groups == 10, "rev4 lesson: exactly 10 capture groups"

def replay_row(path, want_telemetry=True):
    txt = open(path).read()
    m = [REPLAY.match(l) for l in txt.splitlines() if l.startswith("replay,")]
    if len(m) != 1 or not m[0]:
        die("replay row parse: %s (%d rows)" % (path, len(m)))
    done = "# replay_done rows=1" in txt
    if not done:
        die("no replay_done marker: %s" % path)
    if want_telemetry and txt.count("# forbidden quadruples: 95670") != 1:
        die("jsreplay telemetry drift: %s" % path)
    return list(m[0].groups()), txt

def main():
    head = open(os.path.join(S, "HEAD.txt")).read().strip()
    gates = {}
    # G0: gate source pins
    pins0 = {
        "kyouen_dfpn_root.cpp":
            "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e",
        "kyouen_residual_micro.hpp":
            "5976935dcfccb9b5a26fa68f8de20868ce45363dd8c372dcd67d9b841167e7f5",
        "n11_s5_quarantine.hpp":
            "2e36d69481fafcde7aede8ae4fedf3d5477f91ee9846bcd4ae2975f32a4ba1a5",
    }
    for f, pin in pins0.items():
        got = sha256(os.path.join(GSRC, f))
        if got != pin:
            die("G0 gate source pin mismatch %s: %s != %s" % (f, got, pin))
    gates["G0"] = {"status": "PASS",
                   "gate_source_sha256": pins0["kyouen_dfpn_root.cpp"],
                   "commit": "154f3b7a67b97e13acbaee8b04dc74ddca728d19"}

    # G1: batch-kit verification per target
    expected = {}
    src_pins = {}
    cls_info = {}
    for key, tag, cls in TARGETS:
        d = os.path.join(W4, tag)
        r1, _ = replay_row(os.path.join(d, "raw", "%s.p1.out" % key))
        r2, _ = replay_row(os.path.join(d, "raw", "%s.p2.out" % key))
        if r1[:7] != r2[:7] or r1[8:] != r2[8:]:
            die("G1 %s: batch raw p1/p2 drift" % key)
        _, _, legal, _, budget, result, nodes = r1[0], r1[1], r1[2], r1[3], r1[4], r1[5], r1[6]
        if int(budget) != 15000000:
            die("G1 %s: budget %s != 15000000" % (key, budget))
        if int(result) != 1:
            die("G1 %s: published replica result %s != 1 (WIN)" % (key, result))
        # input CSV == SSOT shape
        ssot = json.load(open(os.path.join(d, "batch-keys.json")))
        ent = [k for k in ssot["keys"] if k["key_id"] == key]
        if len(ent) != 1:
            die("G1 %s: batch-keys entry count %d" % (key, len(ent)))
        ent = ent[0]
        if ssot["class_index"] != cls or ssot["budget"] != 15000000:
            die("G1 %s: batch-keys class/budget drift %r %r" % (key, ssot["class_index"], ssot["budget"]))
        if int(ent["legal"]) != int(legal) or str(ent["lo"]) != r1[8] or str(ent["hi"]) != r1[9]:
            die("G1 %s: batch-keys key drift" % key)
        icontent = open(os.path.join(d, "input", "%s.input.csv" % key)).read()
        want = "target,0,5,%d,%d,%d,0,0,0,0,0\n" % (ent["lo"], ent["hi"], int(legal))
        if icontent != want:
            die("G1 %s: input csv %r != %r" % (key, icontent, want))
        # status.log triple
        st = open(os.path.join(d, "status.log")).read()
        mt = re.search(r"^(\S+) (\S+) PASS 15000000,1,%s$" % nodes, st, re.M)
        mh = re.search(r"^(\S+) (\S+) WIN-HALT$", st, re.M)
        if not mt or mt.group(2) != key:
            die("G1 %s: status.log PASS triple missing" % key)
        if not mh or mh.group(2) != key:
            die("G1 %s: status.log WIN-HALT line missing" % key)
        expected[key] = "%s,15000000,1,%s" % (legal, nodes)
        src_pins[key] = {
            "input_sha256": sha256(os.path.join(d, "input", "%s.input.csv" % key)),
            "raw_p1_sha256": sha256(os.path.join(d, "raw", "%s.p1.out" % key)),
            "raw_p2_sha256": sha256(os.path.join(d, "raw", "%s.p2.out" % key)),
            "batch_keys_sha256": sha256(os.path.join(d, "batch-keys.json")),
            "status_log_sha256": sha256(os.path.join(d, "status.log")),
        }
        cls_info[key] = {"class_index": cls, "s5_index": ent["s5_index"],
                         "lo": ent["lo"], "hi": ent["hi"], "legal": int(legal)}
    gates["G1"] = {"status": "PASS", "targets": len(expected)}

    # G2: third-impl cross-SSOT
    t3 = json.load(open(os.path.join(THIRD, "rows.json")))
    t3map = {t["key_id"]: t for t in t3["targets"]}
    for key, tag, cls in TARGETS:
        t = t3map.get(key)
        if t is None:
            die("G2 %s: rows.json entry missing" % key)
        c = cls_info[key]
        if t["lo"] != c["lo"] or t["hi"] != c["hi"] or t["legal"] != c["legal"]:
            die("G2 %s: rows.json key drift" % key)
        if t["replica_result"] != 1 or t["replica_nodes"] != int(expected[key].split(",")[3]):
            die("G2 %s: rows.json replica quadruple drift" % key)
        if t["expect_third"] != 1:
            die("G2 %s: expect_third != 1" % key)
        for p in ("a", "b"):
            tp = os.path.join(THIRD, "targets", "%s.%s.out" % (key, p))
            line = open(tp).read().strip()
            m = re.match(r"^third,%s%s,5,(\d+),(\d+),1,(\d+),(\d+),([0-9.]+)," % (key, p), line)
            if not m:
                die("G2 %s: third-impl raw %s parse: %r" % (key, p, line[:80]))
            if int(m.group(1)) != cls_info[key]["legal"] or m.group(1) != m.group(2):
                die("G2 %s: third-impl raw %s legal drift" % (key, p))
        with open(os.path.join(THIRD, "targets", "%s.a.out" % key)) as fa, \
             open(os.path.join(THIRD, "targets", "%s.b.out" % key)) as fb:
            la = fa.read().strip().split(",")
            lb = fb.read().strip().split(",")
            if la[6] != lb[6] or la[7] != lb[7] or la[5] != lb[5] or la[5] != "1":
                die("G2 %s: third-impl a/b disagree or result != 1" % key)
    gates["G2"] = {"status": "PASS", "cross_ssot": "rows.json + a/b target raws agree verdict-level"}

    # G3: EQ subset byte verification + anchors
    eq_manifest = parse_manifest(os.path.join(EQK, "MANIFEST-sha256.txt"))
    eq_files = ["scripts/gate_runner.sh", "scripts/audit_gate.py",
                "MANIFEST-sha256.txt",
                "input/anchor-af039.input.csv", "input/anchor-aj001.input.csv",
                "input/anchor-at2m.input.csv"]
    for k in ["anchor-af039", "anchor-aj001", "anchor-at2m"]:
        for p in ("p1", "p2"):
            eq_files.append("output/raw/%s.%s.out" % (k, p))
    for rel in eq_files:
        p = os.path.join(EQK, rel)
        if not os.path.isfile(p):
            die("G3 missing EQ file: %s" % p)
        if rel == "MANIFEST-sha256.txt":
            continue
        if sha256(p) != eq_manifest[rel][0]:
            die("G3 EQ sha mismatch %s" % rel)
    A = {}
    for k, budget in [("anchor-at2m", 2000000), ("anchor-af039", 30000000), ("anchor-aj001", 30000000)]:
        r1, _ = replay_row(os.path.join(EQK, "output/raw/%s.p1.out" % k), want_telemetry=False)
        r2, _ = replay_row(os.path.join(EQK, "output/raw/%s.p2.out" % k), want_telemetry=False)
        if r1[:7] != r2[:7] or r1[8:] != r2[8:]:
            die("G3 anchor %s: p1/p2 drift" % k)
        legal, bud, result, nodes = r1[2], r1[4], r1[5], r1[6]
        if int(bud) != budget:
            die("G3 anchor %s: budget %s != %d" % (k, bud, budget))
        A[k] = "%s,%s,%s,%s" % (legal, bud, result, nodes)
    if A != {"anchor-af039": "89,30000000,2,19234232",
             "anchor-aj001": "84,30000000,2,5156075",
             "anchor-at2m": "98,2000000,0,2000000"}:
        die("G3 anchor expected set mismatch: %r" % A)
    gates["G3"] = {"status": "PASS", "files": len(eq_files), "anchors": A}

    # G4: freshness vs canonical head 9c4dd94e
    def cache_rows(path):
        rows = {}
        for l in open(path):
            l = l.strip()
            if not l or l.startswith("#"):
                continue
            parts = [x.strip() for x in l.split(",")]
            if parts[0] != "s5verdict" or len(parts) != 6:
                die("cache row parse: %r" % l)
            rows[(parts[1], parts[2])] = True
        return rows
    merged_path = os.path.join(ER, "merged-exact-s5-chain-plus-erwin18-20261125.cache")
    msha = sha256(merged_path)
    if msha != "9c4dd94e61b6ee724a966ecc9552e527ba5a7107de732f0e9c5ced33bdad4a5a":
        die("G4 merged head sha mismatch: %s (EU may have landed - re-fetch)" % msha)
    merged = cache_rows(merged_path)
    if len(merged) != 6765:
        die("G4 merged census %d != 6765" % len(merged))
    for key, tag, cls in TARGETS:
        if (str(cls_info[key]["lo"]), str(cls_info[key]["hi"])) in merged:
            die("G4 target %s present in canonical head 9c4dd94e" % key)
    gates["G4"] = {"status": "PASS", "merged_sha256": msha, "rows": len(merged),
                   "targets_fresh_vs": "9c4dd94e"}

    # G8: emit kit
    inp = os.path.join(KIT, "input")
    os.makedirs(inp, exist_ok=True)
    for key, tag, cls in TARGETS:
        shutil.copyfile(os.path.join(W4, tag, "input", "%s.input.csv" % key),
                        os.path.join(inp, "%s.input.csv" % key))
    for k in ["anchor-at2m", "anchor-af039", "anchor-aj001"]:
        shutil.copyfile(os.path.join(EQK, "input/%s.input.csv" % k),
                        os.path.join(inp, "%s.input.csv" % k))
    # runner: EQ bytes with the Part-EV comment block (disclosed diff)
    runner = open(os.path.join(EQK, "scripts/gate_runner.sh")).read()
    if runner.count("# Part EQ C++ scrutiny gate runner. Usage: gate_runner.sh <key> <budget> <expected-fields>") != 1:
        die("G8 runner EQ header not unique")
    runner = runner.replace("# Part EQ C++ scrutiny gate runner. Usage: gate_runner.sh <key> <budget> <expected-fields>",
                            "# Part EV C++ scrutiny gate runner. Usage: gate_runner.sh <key> <budget> <expected-fields>")
    runner = runner.replace("# Machine-identical to the EN/EO runner rev2 (3a8ee4fd bytes; only this comment\n# block names Part EQ). Two fresh-cold passes (one process per pass, like the\n# drive runners).",
                            "# Machine-identical to the EN/EO/EQ/ET runner rev2 (3a8ee4fd bytes; only this comment\n# block names Part EV). Two fresh-cold passes (one process per pass, like the\n# drive runners).")
    with open(os.path.join(KIT, "scripts/gate_runner.sh"), "w") as f:
        f.write(runner)
    # audit: EQ rev4 gate structure, EV rows/provenance
    ROWS = {}
    for key, tag, cls in TARGETS:
        ROWS[key] = ("15000000", expected[key], src_pins[key]["input_sha256"],
                     "batch kit input/%s.input.csv (class %d batch; batch-keys SSOT)" % (key, cls))
    for k in ["anchor-at2m", "anchor-af039", "anchor-aj001"]:
        ROWS[k] = (str(2000000 if k == "anchor-at2m" else 30000000), A[k],
                  eq_manifest["input/%s.input.csv" % k][0],
                  "EQ kit input/%s.input.csv (byte-clone; == EO/EN kit input)" % k)
    eq_audit = open(os.path.join(EQK, "scripts/audit_gate.py")).read()
    m0 = eq_audit.index("ROWS = {")
    mc = eq_audit.index("# published raw provenance")
    eq_audit = eq_audit[:m0] + "ROWS = " + json.dumps(ROWS, indent=4, sort_keys=True) + "\n\n" + eq_audit[mc:]
    m2 = eq_audit.index("RAW_PROV = {")
    m3 = eq_audit.index("REPLAY = re.compile(")
    RAW = {}
    for key, tag, cls in TARGETS:
        RAW[key] = ("batch kit output/raw/%s.p1.out (replay...,%s,...); two-pass node-exact vs %s.p2; "
                    "third-impl reverify a/b agree verdict-level" % (key, expected[key].split(",")[3], key))
    RAW["anchor-at2m"] = "EQ kit output/raw/anchor-at2m.p1.out (2000000,0,2000000); budget-ceiling baseline"
    RAW["anchor-af039"] = "EQ kit output/raw/anchor-af039.p1.out (30000000,2,19234232); budget-ceiling baseline"
    RAW["anchor-aj001"] = "EQ kit output/raw/anchor-aj001.p1.out (30000000,2,5156075); budget-ceiling baseline"
    eq_audit = eq_audit[:m2] + "RAW_PROV = " + json.dumps(RAW, indent=4, sort_keys=True) + "\n\n" + eq_audit[m3:]
    eq_audit = eq_audit.replace('"part": "EQ", "schema": "n11-centralreply-cppgate-30345win18-audit-v1"',
                                '"part": "EV", "schema": "n11-centralreply-cppgate-wins41164-audit-v1"')
    eq_audit = eq_audit.replace("Part EQ fail-closed machine audit for the C++ scrutiny gate run\n(closure class 30345, b38-win-18 rows).",
                                "Part EV fail-closed machine audit for the C++ scrutiny gate run\n(closure-batch WINs b018/d002/e002/f017 at the 15M condition).")
    eq_audit = eq_audit.replace("G3  per-row published-raw pins: (legal, budget, result, nodes) equal the\n      pinned expected values transcribed from the published source raws\n      (EG kit sources/b33-raw at 15M for af029/af047/af050/af053 and\n      sources/ea-raw at 30M for af023/af048; EN kit raws for the anchors).",
                                "G3  per-row published-raw pins: (legal, budget, result, nodes) equal the\n      pinned expected values transcribed from the published source raws\n      (closure batch kits class16757/20421/16371-batch4/12264-batch5 at\n      15M for the four WIN rows; EQ kit raws for the anchors).")
    if "b38-win-18 rows" in eq_audit:
        die("G8 audit EQ label residue")
    with open(os.path.join(KIT, "scripts/audit_gate.py"), "w") as f:
        f.write(eq_audit)
    # registry
    reg = {
        "schema": "n11-centralreply-cppgate-wins41164-rows-v1",
        "part": "EV",
        "main_head_at_maker": head,
        "gate_source": {"path": "cpp/solvers/kyouen_dfpn_root.cpp",
                        "commit": "154f3b7a67b97e13acbaee8b04dc74ddca728d19",
                        "sha256": pins0["kyouen_dfpn_root.cpp"],
                        "header_pins": {k: v for k, v in pins0.items() if k != "kyouen_dfpn_root.cpp"}},
        "targets": {key: {"budget": 15000000, "expected": expected[key],
                          "input_pin": src_pins[key]["input_sha256"],
                          "class_index": cls, "s5_index": cls_info[key]["s5_index"],
                          "lo": cls_info[key]["lo"], "hi": cls_info[key]["hi"],
                          "result_label": "WIN",
                          "batch_source_pins": src_pins[key]} for key, tag, cls in TARGETS},
        "anchors": A,
        "canonical_head_freshness": {"merged_sha256": msha, "rows": len(merged),
                                      "targets_fresh_vs": "9c4dd94e"},
        "out_of_scope": "k04 sixth-cost WIN (sixth-cost lane), all Part ES 30M rows (Part ET territory + EU adoption in flight), the 21 unconsumed LOSS rows (EM pattern), everything consumed",
        "gates": gates,
    }
    with open(os.path.join(inp, "gate-rows-ev.json"), "w") as f:
        json.dump(reg, f, indent=1, sort_keys=True)
        f.write("\n")
    print("maker: ALL PASS; targets=%d anchors=%d" % (len(TARGETS), len(A)))
    print("targets:", " ".join(k for k, _, _ in TARGETS))
    print("expected:", json.dumps(expected, sort_keys=True))
    for gname, g in sorted(gates.items()):
        print("  ", gname, g.get("status"), "->", json.dumps({k: v for k, v in g.items() if k != "status"}, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())
