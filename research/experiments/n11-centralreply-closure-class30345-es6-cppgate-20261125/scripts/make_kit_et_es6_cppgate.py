#!/usr/bin/env python3
"""Part ET fail-closed kit maker: C++ scrutiny gate for the 6 Part ES
re-probe-30M rows (closure class 30345; 2 WIN + 4 LOSS, all unconsumed).

Every gate must PASS before any kit file is emitted (fail-closed; rc=1 on
ANY drift).  No per-file sha is hand-typed: every pin is machine-extracted
from the published source-kit MANIFESTs and the published raws (Part EP
pin policy).

Source kits (all fetched from published bytes at the recorded main head and
verified file-by-file against their MANIFEST-sha256.txt):
  S1  ES kit  research/experiments/n11-centralreply-closure-class30345-reprobe30m-20261125
              (MANIFEST 38 entries incl. output raws; Part ES 30M re-probe,
              drive raws of the 6 targets this gate re-verifies)
  S2  EQ kit  research/experiments/n11-centralreply-closure-class30345-cppgate-20261125
              (MANIFEST 74 entries; Part EQ C++ gate - runner/audit bytes
              lineage + the 3 calibration anchors of the same lineage)
  S3  ER chain  increment-erwin18-20261125.cache (4f6b7797) and merged
              merged-exact-s5-chain-plus-erwin18-20261125.cache (9c4dd94e),
              fetched from the published Part ER kit at the recorded head of
              n11-centralreply-erwin18-adoption-reaudit-20261125.
  S0  gate source  cpp/solvers/kyouen_dfpn_root.cpp at commit
              154f3b7a67b97e13acbaee8b04dc74ddca728d19 (9193f5b6...) with
              headers kyouen_residual_micro.hpp / n11_s5_quarantine.hpp at
              the same commit (full pins asserted below).

Gates:
  G1  S1 byte verification: every fetched ES file matches its MANIFEST pin
      (6 inputs, targets-30m.json SSOT, status.log, 12 raws, 8 val-gate
      runs, jsreplay/runbatch30m scripts, 4 published baselines).
  G2  S2 byte verification: fetched EQ runner/audit bytes and
      anchor-inputs/anchor-raws match the EQ MANIFEST pins.
  G3  cross-SSOT: ES status.log PASS triples == targets-30m.json
      quadruples (lo,hi,legal per key) jointly with the raws; WIN lines
      carry the same triple as their PASS line; exactly 6 keys, 2 WIN.
  G4  target derivation: the 6 target ids are exactly the SSOT targets,
      every serving_class 30345, budget 30000000 for all.
  G5  per-target raw discipline: p1 == p2 on all replay fields except
      wall_s; (legal,budget,result,nodes) == status.log triple; legal ==
      SSOT legal; lo/hi == SSOT; raw carries the jsreplay
      '# forbidden quadruples' telemetry line; input CSV == SSOT row.
  G6  freshness: every target (lo,hi) absent from the ER merged canonical
      head 9c4dd94e (6,765 rows WIN186/LOSS6579; ER increment 4f6b7797
      rows verified to survive into it; union-merge chain property =>
      absent from all prior canonical heads as well).
  G7  anchors: EQ anchor raws p1 == p2 and expected quadruples regenerate
      from the raws; anchor input CSVs byte-match the EQ kit pins.
  G8  emit: input CSVs byte-cloned, runner (EQ bytes, comment block names
      Part ET - disclosed), audit script (EQ gates kept verbatim,
      ROWS/RAW_PROV regenerated), gate-rows-et.json registry.
"""
import hashlib, json, os, re, shutil, sys

KIT = os.path.dirname(os.path.abspath(__file__)) + "/.."
KIT = os.path.abspath(KIT)
S = os.path.join(KIT, "sources")
RES = os.path.join(S, "eskit")
EQK = os.path.join(S, "eqkit")
ER = os.path.join(S, "erchain")
GSRC = os.path.join(S, "gatesrc")

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

def verify_tree(root, manifest, subset=None):
    pins = parse_manifest(os.path.join(root, manifest))
    checked = 0
    for rel, (pin, size) in sorted(pins.items()):
        if subset is not None and rel not in subset:
            continue
        p = os.path.join(root, rel)
        if not os.path.isfile(p):
            die("G1 missing file: %s" % p)
        if os.path.getsize(p) != size:
            die("G1 size mismatch: %s (%d != %d)" % (p, os.path.getsize(p), size))
        got = sha256(p)
        if got != pin:
            die("G1 sha mismatch: %s (%s != %s)" % (p, got, pin))
        checked += 1
    return checked, pins

REPLAY = re.compile(r"^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),([0-9.]+),(\d+),(\d+)$")
assert REPLAY.groups == 10, "rev4 lesson: exactly 10 capture groups"

def replay_row(path):
    txt = open(path).read()
    m = [REPLAY.match(l) for l in txt.splitlines() if l.startswith("replay,")]
    if len(m) != 1 or not m[0]:
        die("replay row parse: %s (%d rows)" % (path, len(m)))
    done = "# replay_done rows=1" in txt
    if not done:
        die("no replay_done marker: %s" % path)
    return list(m[0].groups()), txt

def main():
    head = open(os.path.join(S, "HEAD.txt")).read().strip()
    gates = {}
    # G1: ES kit verification (ALL MANIFEST entries)
    n1, espins = verify_tree(RES, "MANIFEST-sha256.txt")
    gates["G1"] = {"status": "PASS", "files": n1}
    # G2: EQ kit verification (runner/audit bytes + anchors)
    eq_manifest = parse_manifest(os.path.join(EQK, "MANIFEST-sha256.txt"))
    eq_files = ["scripts/gate_runner.sh", "scripts/audit_gate.py",
                "scripts/make_kit_eq_win18_cppgate.py", "MANIFEST-sha256.txt",
                "input/anchor-af039.input.csv", "input/anchor-aj001.input.csv",
                "input/anchor-at2m.input.csv"]
    for k in ["anchor-af039", "anchor-aj001", "anchor-at2m"]:
        for p in ("p1", "p2"):
            eq_files.append("output/raw/%s.%s.out" % (k, p))
    for rel in eq_files:
        p = os.path.join(EQK, rel)
        if not os.path.isfile(p):
            die("G2 missing EQ file: %s" % p)
        got = sha256(p)
        if rel == "MANIFEST-sha256.txt":
            continue
        if got != eq_manifest[rel][0]:
            die("G2 EQ sha mismatch %s: %s != %s" % (rel, got, eq_manifest[rel][0]))
    gates["G2"] = {"status": "PASS", "files": len(eq_files)}
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
    # G3: cross-SSOT of ES targets
    ssot = json.load(open(os.path.join(RES, "input/targets-30m.json")))
    if ssot["schema"] != "class30345-reprobe30m-targets-v1":
        die("G3 SSOT schema drift: %r" % ssot["schema"])
    targets = [t["key_id"] for t in ssot["targets"]]
    want6 = ["ai007", "ai024", "ai030", "ai038", "ai040", "ai041"]
    if sorted(targets) != sorted(want6):
        die("G3 target id set drift: %r" % targets)
    tmap = {t["key_id"]: t for t in ssot["targets"]}
    pass_re = re.compile(r"^(\S+) (\S+) PASS (\d+),(\d+),(\d+)$")
    win_re = re.compile(r"^(\S+) (\S+) WIN (\d+),(\d+),(\d+)$")
    status_pass, status_win = {}, {}
    for line in open(os.path.join(RES, "output/status.log")):
        line = line.strip()
        if not line:
            continue
        m = pass_re.match(line)
        if m:
            status_pass[m.group(2)] = (int(m.group(3)), int(m.group(4)), int(m.group(5)))
            continue
        m = win_re.match(line)
        if m:
            status_win[m.group(2)] = (int(m.group(3)), int(m.group(4)), int(m.group(5)))
            continue
        die("G3 unparseable ES status.log line: %r" % line)
    if sorted(status_pass) != sorted(want6):
        die("G3 ES status PASS keys %r != 6 targets" % sorted(status_pass))
    if sorted(status_win) != ["ai007", "ai040"]:
        die("G3 ES status WIN keys %r != ai007/ai040" % sorted(status_win))
    for k, t in status_win.items():
        if t != status_pass[k]:
            die("G3 WIN line != PASS line for %s" % k)
    for k in want6:
        b, res, nodes = status_pass[k]
        if b != 30000000:
            die("G3 %s budget %d != 30000000" % (k, b))
        exp = 1 if k in status_win else 2
        if res != exp:
            die("G3 %s result %d != %d" % (k, res, exp))
        if nodes < 1 or nodes > 30000000:
            die("G3 %s nodes out of range: %d" % (k, nodes))
    gates["G3"] = {"status": "PASS", "keys": len(status_pass)}
    # G4: target quadruples vs SSOT
    for k in want6:
        t = tmap[k]
        if t["serving_class"] != 30345:
            die("G4 %s serving_class %s != 30345" % (k, t["serving_class"]))
        if t["lo"] <= 0 or t["hi"] <= 0:
            die("G4 %s SSOT lo/hi invalid" % k)
    gates["G4"] = {"status": "PASS", "targets": sorted(want6),
                   "win": sorted(status_win), "loss": sorted(k for k in want6 if k not in status_win)}
    # G6 (early, chain side): freshness vs canonical head 9c4dd94e
    def cache_rows(path):
        rows = {}
        for l in open(path):
            l = l.strip()
            if not l or l.startswith("#"):
                continue
            parts = [x.strip() for x in l.split(",")]
            if parts[0] != "s5verdict" or len(parts) != 6:
                die("cache row parse: %r" % l)
            rows[(parts[1], parts[2])] = (int(parts[3]), int(parts[4]), int(parts[5]))
        return rows
    inc_path = os.path.join(ER, "increment-erwin18-20261125.cache")
    merged_path = os.path.join(ER, "merged-exact-s5-chain-plus-erwin18-20261125.cache")
    msha = sha256(merged_path)
    if msha != "9c4dd94e61b6ee724a966ecc9552e527ba5a7107de732f0e9c5ced33bdad4a5a":
        die("G6 merged head sha mismatch: %s" % msha)
    merged = cache_rows(merged_path)
    win_count = sum(1 for v in merged.values() if v[1] == 1)
    loss_count = sum(1 for v in merged.values() if v[1] == 2)
    if len(merged) != 6765 or win_count != 186 or loss_count != 6579:
        die("G6 merged census %d/%d/%d != 6765/186/6579" % (len(merged), win_count, loss_count))
    inc = cache_rows(inc_path)
    isha = sha256(inc_path)
    if isha != "4f6b7797df3bb950703f95e7ec72f288a447434da5b4ccf3d6d94ee8d8d6ffc1":
        die("G6 ER increment sha mismatch: %s" % isha)
    if len(inc) != 18:
        die("G6 ER increment rows=%d != 18" % len(inc))
    for k2, v in inc.items():
        if merged.get(k2) != v:
            die("G6 ER increment row %r not preserved in merged head" % (k2,))
    for k in want6:
        b = tmap[k]
        if (str(b["lo"]), str(b["hi"])) in merged:
            die("G6 target %s present in canonical head 9c4dd94e" % k)
    gates["G6"] = {"status": "PASS", "merged_sha256": msha,
                   "increment_sha256": isha, "rows": len(merged),
                   "win": win_count, "loss": loss_count,
                   "targets_fresh_vs": "9c4dd94e"}
    # G5: per-target raw discipline + expected extraction
    expected = {}
    for k in want6:
        t = tmap[k]
        r1, t1 = replay_row(os.path.join(RES, "output/raw/%s.p1.out" % k))
        r2, t2 = replay_row(os.path.join(RES, "output/raw/%s.p2.out" % k))
        if t1.count("# forbidden quadruples") != 1 or t2.count("# forbidden quadruples") != 1:
            die("G5 %s: jsreplay telemetry marker missing" % k)
        if t1.count("# forbidden quadruples: 95670") != 1:
            die("G5 %s: forbidden-quadruples header drift" % k)
        if r1[:7] != r2[:7] or r1[8:] != r2[8:]:
            die("G5 %s: p1/p2 drift %r %r" % (k, r1, r2))
        _, _, legal, _, budget, result, nodes = r1[0], r1[1], r1[2], r1[3], r1[4], r1[5], r1[6]
        if int(budget) != 30000000:
            die("G5 %s: raw budget %s != 30000000" % (k, budget))
        if int(legal) != t["legal"]:
            die("G5 %s: raw legal %s != SSOT %s" % (k, legal, t["legal"]))
        if int(r1[8]) != t["lo"] or int(r1[9]) != t["hi"]:
            die("G5 %s: raw key %s/%s != SSOT %s/%s" % (k, r1[8], r1[9], t["lo"], t["hi"]))
        if (int(budget), int(result)) != (status_pass[k][0], status_pass[k][1]):
            die("G5 %s: raw triple header != status" % k)
        if int(nodes) != status_pass[k][2]:
            die("G5 %s: nodes %s vs status %s" % (k, nodes, status_pass[k][2]))
        expected[k] = "%s,%s,%s,%s" % (legal, budget, result, nodes)
        icontent = open(os.path.join(RES, "input/%s.input.csv" % k)).read()
        want = "target,0,5,%d,%d,%d,0,0,0,0,0\n" % (t["lo"], t["hi"], t["legal"])
        if icontent != want:
            die("G5 %s: input csv %r != %r" % (k, icontent, want))
    gates["G5"] = {"status": "PASS", "targets": len(expected)}
    # G7: anchors
    A = {}
    for k, budget in [("anchor-at2m", 2000000), ("anchor-af039", 30000000), ("anchor-aj001", 30000000)]:
        r1, _ = replay_row(os.path.join(EQK, "output/raw/%s.p1.out" % k))
        r2, _ = replay_row(os.path.join(EQK, "output/raw/%s.p2.out" % k))
        if r1[:7] != r2[:7] or r1[8:] != r2[8:]:
            die("G7 %s: anchor p1/p2 drift" % k)
        legal, bud, result, nodes = r1[2], r1[4], r1[5], r1[6]
        if int(bud) != budget:
            die("G7 %s: budget %s != %d" % (k, bud, budget))
        A[k] = "%s,%s,%s,%s" % (legal, bud, result, nodes)
    if A != {"anchor-af039": "89,30000000,2,19234232",
             "anchor-aj001": "84,30000000,2,5156075",
             "anchor-at2m": "98,2000000,0,2000000"}:
        die("G7 anchor expected set mismatch: %r" % A)
    gates["G7"] = {"status": "PASS", "anchors": A}
    # G8: emit kit
    inp = os.path.join(KIT, "input")
    os.makedirs(inp, exist_ok=True)
    for k in want6:
        shutil.copyfile(os.path.join(RES, "input/%s.input.csv" % k), os.path.join(inp, "%s.input.csv" % k))
    for k in ["anchor-at2m", "anchor-af039", "anchor-aj001"]:
        shutil.copyfile(os.path.join(EQK, "input/%s.input.csv" % k), os.path.join(inp, "%s.input.csv" % k))
    # runner: EQ bytes with the Part-ET comment block (disclosed diff)
    runner = open(os.path.join(EQK, "scripts/gate_runner.sh")).read()
    if runner.count("# Part EQ C++ scrutiny gate runner. Usage: gate_runner.sh <key> <budget> <expected-fields>") != 1:
        die("G8 runner EQ header not unique")
    runner = runner.replace("# Part EQ C++ scrutiny gate runner. Usage: gate_runner.sh <key> <budget> <expected-fields>",
                            "# Part ET C++ scrutiny gate runner. Usage: gate_runner.sh <key> <budget> <expected-fields>")
    runner = runner.replace("# Machine-identical to the EN/EO runner rev2 (3a8ee4fd bytes; only this comment\n# block names Part EQ). Two fresh-cold passes (one process per pass, like the\n# drive runners).",
                            "# Machine-identical to the EN/EO/EQ runner rev2 (3a8ee4fd bytes; only this comment\n# block names Part ET). Two fresh-cold passes (one process per pass, like the\n# drive runners).")
    with open(os.path.join(KIT, "scripts/gate_runner.sh"), "w") as f:
        f.write(runner)
    # audit script: EQ gates kept verbatim; ROWS/RAW_PROV/part/schema regenerated
    ROWS = {}
    for k in want6:
        ROWS[k] = ("30000000", expected[k], espins["input/%s.input.csv" % k][0],
                   "ES kit input/%s.input.csv (byte-clone of b38 kit input; targets-30m SSOT 1c27a238)" % k)
    for k in ["anchor-at2m", "anchor-af039", "anchor-aj001"]:
        ROWS[k] = (str(2000000 if k == "anchor-at2m" else 30000000), A[k],
                   eq_manifest["input/%s.input.csv" % k][0],
                   "EQ kit input/%s.input.csv (byte-clone; == EO/EN kit input)" % k)
    rows_lit = json.dumps(ROWS, indent=4, sort_keys=True)
    RAW = {}
    for k in want6:
        RAW[k] = ("ES kit output/raw/%s.p1.out (replay...,%s,...); two-pass node-exact vs %s.p2" % (k, expected[k].split(",")[3], k))
    RAW["anchor-at2m"] = "EQ kit output/raw/anchor-at2m.p1.out (2000000,0,2000000); budget-ceiling baseline; EO raws == EN raws (published observation)"
    RAW["anchor-af039"] = "EQ kit output/raw/anchor-af039.p1.out (30000000,2,19234232); canonical cache row, budget-ceiling baseline"
    RAW["anchor-aj001"] = "EQ kit output/raw/anchor-aj001.p1.out (30000000,2,5156075); budget-ceiling baseline"
    eq_audit = open(os.path.join(EQK, "scripts/audit_gate.py")).read()
    m0 = eq_audit.index("ROWS = {")
    mc = eq_audit.index("# published raw provenance")
    eq_audit = eq_audit[:m0] + "ROWS = " + rows_lit + "\n\n" + eq_audit[mc:]
    m2 = eq_audit.index("RAW_PROV = {")
    m3 = eq_audit.index("REPLAY = re.compile(")
    eq_audit = eq_audit[:m2] + "RAW_PROV = " + json.dumps(RAW, indent=4, sort_keys=True) + "\n\n" + eq_audit[m3:]
    eq_audit = eq_audit.replace('"part": "EQ", "schema": "n11-centralreply-cppgate-30345win18-audit-v1"',
                                '"part": "ET", "schema": "n11-centralreply-cppgate-30345es6-audit-v1"')
    eq_audit = eq_audit.replace("Part EQ fail-closed machine audit for the C++ scrutiny gate run\n(closure class 30345, b38-win-18 rows).",
                                "Part ET fail-closed machine audit for the C++ scrutiny gate run\n(closure class 30345, ES re-probe-6 rows at the 30M condition).")
    if "b38-win-18 rows" in eq_audit:
        die("G8 audit EQ label residue")
    with open(os.path.join(KIT, "scripts/audit_gate.py"), "w") as f:
        f.write(eq_audit)
    # registry
    reg = {
        "schema": "n11-centralreply-cppgate-30345es6-rows-v1",
        "part": "ET",
        "main_head_at_maker": head,
        "gate_source": {"path": "cpp/solvers/kyouen_dfpn_root.cpp",
                        "commit": "154f3b7a67b97e13acbaee8b04dc74ddca728d19",
                        "sha256": pins0["kyouen_dfpn_root.cpp"],
                        "header_pins": {k: v for k, v in pins0.items() if k != "kyouen_dfpn_root.cpp"}},
        "targets": {k: {"budget": 30000000, "expected": expected[k],
                        "input_pin": espins["input/%s.input.csv" % k][0],
                        "s5_index": tmap[k]["s5_index"], "probe_order": tmap[k]["probe_order"],
                        "serving_class": tmap[k]["serving_class"],
                        "result_label": "WIN" if k in status_win else "LOSS"} for k in want6},
        "anchors": A,
        "canonical_head_freshness": {"merged_sha256": msha, "rows": len(merged),
                                     "win": win_count, "loss": loss_count},
        "out_of_scope": "b018 (dual-class, scrutiny-owner pending, same-condition re-probe prohibited), k04 sixth-cost WIN, all other probe-level WINs",
        "gates": gates,
    }
    with open(os.path.join(inp, "gate-rows-et.json"), "w") as f:
        json.dump(reg, f, indent=1, sort_keys=True)
        f.write("\n")
    print("maker: ALL PASS; targets=%d anchors=%d" % (len(want6), len(A)))
    print("targets:", " ".join(want6))
    print("expected:", json.dumps(expected, sort_keys=True))
    for gname, g in sorted(gates.items()):
        print("  ", gname, g.get("status"), "->", json.dumps({k: v for k, v in g.items() if k != "status"}, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())
