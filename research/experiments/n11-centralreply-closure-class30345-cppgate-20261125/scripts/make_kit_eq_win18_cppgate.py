#!/usr/bin/env python3
"""Part EQ fail-closed kit maker: C++ scrutiny gate for the 18 unconsumed
batch-38 WIN rows (closure class 30345).

Every gate must PASS before any kit file is emitted (fail-closed; rc=1 on
ANY drift).  No per-file sha is hand-typed: every pin is machine-extracted
from the published source-kit MANIFESTs and the published raws (Part EP pin
policy).

Source kits (all fetched from published bytes at the recorded main head and
verified file-by-file against their MANIFEST-sha256.txt):
  S1  b38 kit   research/experiments/n11-centralreply-closure-class30345-batch38-20261125
                (MANIFEST 181 entries; Part EF batch-38)
  S2  EO kit    research/experiments/n11-centralreply-closure-class34908-cppgate-20261125
                (MANIFEST 37 entries; Part EO C++ gate, source pin 9193f5b6)
  S3  EP chain  increment-epwin10-20261125.cache (c245bc4c) merged
                merged-exact-s5-chain-plus-epwin10-20261125.cache (fd29a337),
                fetched from the published Part EP kit at the recorded head
                of n11-centralreply-epwin10-adoption-reaudit-20261125.

Gates:
  G1  S1 byte verification: every fetched b38 file matches its MANIFEST pin
      (49 inputs, batch-keys SSOT, status.log, batch-audit.json, 105 raws).
  G2  S2 byte verification: fetched EO runner/audit/anchor-inputs/anchor-raws
      match the EO MANIFEST pins.
  G3  cross-SSOT: status.log PASS lines == batch-audit per_key records
      (budget,result,nodes) for all 49 keys.
  G4  target derivation: per_key result_label WIN, minus ai048 (consumed by
      Part EP adoption; the EP increment contains its row) = EXACTLY 18
      targets; every target serving_class 30345 in the batch-keys SSOT.
  G5  per-target raw discipline: p1 == p2 on all replay fields except
      wall_s; (legal,budget,result,nodes) == status.log == batch-audit;
      input CSV (lo,hi,legal) == batch-keys SSOT quadruple (lo,hi,legal,
      s5_index); raw carries the jsreplay '# forbidden quadruples'
      telemetry line (drive-engine provenance marker).
  G6  freshness: every target (lo,hi) absent from the EP merged canonical
      head fd29a337 (union-merge chain property => absent from all prior
      canonical heads); ai0xx truncated-remnant pass outputs are NOT
      evidence (no replay_done marker) and are ignored by machine check.
  G7  anchors: EO anchor raws p1==p2 and expected quadruples regenerate
      from the raws; anchor input CSVs byte-match the EO kit pins.
  G8  emit: input CSVs byte-cloned, runner (EO bytes, comment block names
      Part EQ - disclosed below), audit script (EO gates kept verbatim,
      ROWS/RAW_PROV regenerated), gate-rows-eq.json registry.
"""
import hashlib, json, os, re, shutil, sys

KIT = os.path.dirname(os.path.abspath(__file__)) + "/.."
KIT = os.path.abspath(KIT)
S = os.path.join(KIT, "sources")
B38 = os.path.join(S, "b38kit")
EO = os.path.join(S, "eokit")

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
    pins = parse_manifest(os.path.join(root, manifest)) if not os.path.isabs(manifest) else parse_manifest(manifest)
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
    # G1: b38 kit verification (all fetched files) - manifest at kit root
    n, b38pins = verify_tree(os.path.join(B38), "MANIFEST-sha256.txt",
                             subset={"input/ai%03d.input.csv" % i for i in range(1, 50)} |
                                    {"input/batch-keys-b38.json", "output/status.log",
                                     "output/batch-audit.json"} |
                                    {r for r in []})
    # raws are not all in manifest? include raw dir pins too
    raws_needed = set()
    for i in range(1, 50):
        for p in ("p1", "p2"):
            raws_needed.add("output/raw/ai%03d.%s.out" % (i, p))
    n2, b38pins = verify_tree(B38, "MANIFEST-sha256.txt", subset=raws_needed)
    gates["G1"] = {"status": "PASS", "files": n + n2}
    # G2: EO kit verification
    eo_files = {"scripts/gate_runner.sh": "scripts_gate_runner.sh",
                "scripts/audit_gate.py": "scripts_audit_gate.py"}
    for k in ["af023","af029","af047","af048","af050","af053","anchor-af039","anchor-aj001","anchor-at2m"]:
        eo_files["input/%s.input.csv" % k] = "input/%s.input.csv" % k
    for k in ["anchor-af039","anchor-aj001","anchor-at2m"]:
        for p in ("p1","p2"):
            eo_files["output/raw/%s.%s.out" % (k,p)] = "output/raw/%s.%s.out" % (k,p)
    eo_manifest = {}
    for line in open(os.path.join(EO, "MANIFEST-sha256.txt")):
        line=line.strip()
        if not line or line.startswith("#"): continue
        sh, size, rel = line.split()
        eo_manifest[rel] = (sh, int(size))
    solved = {}
    for rel, local in eo_files.items():
        p = os.path.join(EO, local)
        got = sha256(p)
        if got != eo_manifest[rel][0]:
            die("G2 EO sha mismatch %s: %s != %s" % (rel, got, eo_manifest[rel][0]))
        solved[rel] = got
    gates["G2"] = {"status": "PASS", "files": len(eo_files)}
    # gate source pin
    gsrc = os.path.join(S, "kyouen_dfpn_root.cpp")
    gsha = sha256(gsrc)
    if gsha != "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e":
        die("gate source pin mismatch: %s" % gsha)
    gates["G0"] = {"status": "PASS", "gate_source_sha256": gsha}
    # G3: status.log == batch-audit per_key
    per_key = json.load(open(os.path.join(B38, "output/batch-audit.json")))["per_key"]
    pass_re = re.compile(r"^(\S+) (\S+) PASS (\d+),(\d+),(\d+)$")
    halt_re = re.compile(r"^(\S+) (\S+) (WIN-HALT|EXHAUSTED)( \d+,\d+,\d+)?$")
    retry_re = re.compile(r"^(\S+) (\S+) P2-TRUNCATED-RETRY$")
    status_pass, status_halt, status_retry = {}, {}, {}
    for line in open(os.path.join(B38, "output/status.log")):
        line = line.strip()
        m = pass_re.match(line)
        if m:
            status_pass[m.group(2)] = (int(m.group(3)), int(m.group(4)), int(m.group(5)))
            continue
        m = halt_re.match(line)
        if m:
            status_halt.setdefault(m.group(2), m.group(3))
            continue
        m = retry_re.match(line)
        if m:
            status_retry.setdefault(m.group(2), 0)
            status_retry[m.group(2)] += 1
            continue
        die("G3 unparseable status.log line: %r" % line)
    # EXHAUSTED halt lines carry the budget-ceiling triple; WIN-HALT carries none
    for k, lbl in status_halt.items():
        if lbl == "WIN-HALT":
            continue
        if k not in status_pass or status_pass[k] != (15000000, 0, 15000000):
            die("G3 EXHAUSTED halt line inconsistent with PASS for %s" % k)
    if sum(status_retry.values()) != 7:
        die("G3 retry mentions=%d != 7 (published truncated remnants, non-evidence)" % sum(status_retry.values()))
    if len(status_pass) != 49:
        die("G3 status PASS keys=%d != 49" % len(status_pass))
    for rec in per_key:
        k = rec["key_id"]
        if k not in status_pass:
            die("G3 missing status PASS for %s" % k)
        b, res, nodes = status_pass[k]
        if (b, res, nodes) != (rec["budget"], rec["result"], rec["nodes"]):
            die("G3 mismatch %s: status=%r audit=%r" % (k, status_pass[k], rec))
    gates["G3"] = {"status": "PASS", "keys": len(per_key)}
    # G4: target derivation
    audit = json.load(open(os.path.join(B38, "output/batch-audit.json")))
    wins = [r["key_id"] for r in per_key if r["result_label"] == "WIN"]
    # independent derivation from status.log halts
    wins_by_halt = sorted(k for k, v in status_halt.items() if v == "WIN-HALT")
    if sorted(wins) != wins_by_halt:
        die("G4 WIN derivation disagreement: audit=%s status=%s" % (sorted(wins), wins_by_halt))
    if len(wins) != 19:
        die("G4 WIN count=%d != 19" % len(wins))
    # ai048 consumed by Part EP: EP increment contains its (lo,hi) as a WIN row
    bkeys = json.load(open(os.path.join(B38, "input/batch-keys-b38.json")))["keys"]
    bk = {r["key_id"]: r for r in bkeys}
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
    inc = cache_rows(os.path.join(S, "ep", "increment-epwin10-20261125.cache"))
    if len(inc) != 10:
        die("G4 EP increment rows=%d != 10" % len(inc))
    ai48 = bk["ai048"]
    ai48k = (str(ai48["lo"]), str(ai48["hi"]))
    if ai48k not in inc:
        die("G4 ai048 (lo,hi) absent from EP increment")
    stones, verdict, nodes = inc[ai48k]
    if verdict != 1 or nodes != status_pass["ai048"][2] or stones != 5:
        die("G4 ai048 increment row %r vs status %r" % (inc[ai48k], status_pass["ai048"]))
    targets = [k for k in wins if k != "ai048"]
    if len(targets) != 18:
        die("G4 targets=%d != 18" % len(targets))
    for k in targets:
        if bk[k]["serving_class"] != 30345:
            die("G4 %s serving_class=%s != 30345" % (k, bk[k]["serving_class"]))
    gates["G4"] = {"status": "PASS", "targets": targets, "consumed_by_ep": "ai048"}
    merged = cache_rows(os.path.join(S, "ep", "merged-exact-s5-chain-plus-epwin10-20261125.cache"))
    msha = hashlib.sha256(open(os.path.join(S, "ep", "merged-exact-s5-chain-plus-epwin10-20261125.cache"), "rb").read()).hexdigest()
    if msha != "fd29a33726e2e083998c67d83bf90822f84beebac30728ea79ea713e880cd1af":
        die("G6 merged head sha mismatch: %s" % msha)
    win_count = sum(1 for v in merged.values() if v[1] == 1)
    loss_count = sum(1 for v in merged.values() if v[1] == 2)
    if len(merged) != 6747 or win_count != 168 or loss_count != 6579:
        die("G6 merged census %d/%d/%d != 6747/168/6579" % (len(merged), win_count, loss_count))
    for k in targets:
        b = bk[k]
        if (str(b["lo"]), str(b["hi"])) in merged:
            die("G6 target %s present in canonical head fd29a337" % k)
    if ai48k not in merged or merged[ai48k][1] != 1:
        die("G6 consumed key ai048 missing / not WIN in canonical head")
    nm = len(merged)
    gates["G6"] = {"status": "PASS", "merged_sha256": msha, "rows": nm,
                   "win": win_count, "loss": loss_count}
    # increment: verify every EP increment row survived into the merged head
    for k2, v in inc.items():
        if merged.get(k2) != v:
            die("G6 EP increment row %r not preserved in merged head" % (k2,))
    # G5 per-target raw discipline + expected extraction
    expected = {}
    for k in targets:
        b = bk[k]
        r1, t1 = replay_row(os.path.join(B38, "output/raw/%s.p1.out" % k))
        r2, t2 = replay_row(os.path.join(B38, "output/raw/%s.p2.out" % k))
        if t1.count("# forbidden quadruples") != 1 or t2.count("# forbidden quadruples") != 1:
            die("G5 %s: jsreplay telemetry marker missing" % k)
        if r1[:7] != r2[:7] or r1[8:] != r2[8:]:
            die("G5 %s: p1/p2 drift %r %r" % (k, r1, r2))
        _, _, legal, _, budget, result, nodes = r1[0], r1[1], r1[2], r1[3], r1[4], r1[5], r1[6]
        if int(legal) != b["legal"] or int(budget) != 15000000 or int(result) != 1:
            die("G5 %s: raw quadruple %r vs SSOT" % (k, r1))
        if int(nodes) != status_pass[k][2]:
            die("G5 %s: nodes %s vs status.log %s" % (k, nodes, status_pass[k][2]))
        expected[k] = "%s,%s,%s,%s" % (legal, budget, result, nodes)
        # input CSV check
        icontent = open(os.path.join(B38, "input/%s.input.csv" % k)).read()
        want = "target,0,5,%d,%d,%d,0,0,0,0,0\n" % (b["lo"], b["hi"], b["legal"])
        if icontent != want:
            die("G5 %s: input csv %r != %r" % (k, icontent, want))
    gates["G5"] = {"status": "PASS", "targets": len(expected)}
    # G7 anchors
    A = {}
    for k, budget in [("anchor-at2m", 2000000), ("anchor-af039", 30000000), ("anchor-aj001", 30000000)]:
        r1, _ = replay_row(os.path.join(EO, "output/raw/%s.p1.out" % k))
        r2, _ = replay_row(os.path.join(EO, "output/raw/%s.p2.out" % k))
        if r1[:7] != r2[:7] or r1[8:] != r2[8:]:
            die("G7 %s: anchor p1/p2 drift" % k)
        _, _, legal, _, bud, result, nodes = r1[0], r1[1], r1[2], r1[3], r1[4], r1[5], r1[6]
        if int(bud) != budget:
            die("G7 %s: budget %s != %d" % (k, bud, budget))
        A[k] = "%s,%s,%s,%s" % (legal, bud, result, nodes)
    if A != {"anchor-af039": "89,30000000,2,19234232",
             "anchor-aj001": "84,30000000,2,5156075",
             "anchor-at2m": "98,2000000,0,2000000"}:
        die("G7 anchor expected set mismatch: %r" % A)
    gates["G7"] = {"status": "PASS", "anchors": A}
    # G8 emit kit
    inp = os.path.join(KIT, "input")
    for k in targets:
        shutil.copyfile(os.path.join(B38, "input/%s.input.csv" % k), os.path.join(inp, "%s.input.csv" % k))
    for k in ["anchor-at2m", "anchor-af039", "anchor-aj001"]:
        shutil.copyfile(os.path.join(EO, "input/%s.input.csv" % k), os.path.join(inp, "%s.input.csv" % k))
    # runner: EO bytes with the Part-EQ comment block (disclosed diff)
    runner = open(os.path.join(EO, "scripts_gate_runner.sh")).read()
    old_hdr = "# Part EO C++ scrutiny gate runner. Usage: gate_runner.sh <key> <budget> <expected-fields>"
    new_hdr = "# Part EQ C++ scrutiny gate runner. Usage: gate_runner.sh <key> <budget> <expected-fields>"
    if runner.count(old_hdr) != 1:
        die("G8 runner header not unique")
    runner = runner.replace(old_hdr, new_hdr)
    runner = runner.replace(
        "# Machine-identical to Part EN runner rev2 (3a8ee4fd bytes; only this comment\n# block names Part EO). Two fresh-cold passes (one process per pass, like the\n# drive runners).",
        "# Machine-identical to the EN/EO runner rev2 (3a8ee4fd bytes; only this comment\n# block names Part EQ). Two fresh-cold passes (one process per pass, like the\n# drive runners).")
    with open(os.path.join(KIT, "scripts/gate_runner.sh"), "w") as f:
        f.write(runner)
    # audit script: EO gates kept verbatim; ROWS/RAW_PROV/part/schema regenerated
    ROWS = {}
    for k in targets:
        ROWS[k] = ("15000000", expected[k], b38pins["input/%s.input.csv" % k][0],
                   "b38 kit input/%s.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)" % k)
    for k in ["anchor-at2m", "anchor-af039", "anchor-aj001"]:
        ROWS[k] = (str(2000000 if k == "anchor-at2m" else 30000000), A[k],
                   eo_manifest["input/%s.input.csv" % k][0],
                   "EO kit input/%s.input.csv (byte-clone; == EN kit input)" % k)
    order = sorted(ROWS)
    rows_lit = json.dumps(ROWS, indent=4, sort_keys=True)
    RAW = {}
    for k in targets:
        RAW[k] = ("b38 kit output/raw/%s.p1.out (replay...,%s,1,%s,...); "
                  "two-pass node-exact vs %s.p2" % (k, 15000000, expected[k].split(",")[3], k))
    RAW["anchor-at2m"] = "EO kit output/raw/anchor-at2m.p1.out (2000000,0,2000000); budget-ceiling baseline; EO raws == EN raws (published observation)"
    RAW["anchor-af039"] = "EO kit output/raw/anchor-af039.p1.out (30000000,2,19234232); canonical cache row, budget-ceiling baseline"
    RAW["anchor-aj001"] = "EO kit output/raw/anchor-aj001.p1.out (30000000,2,5156075); budget-ceiling baseline"
    eo_audit = open(os.path.join(EO, "scripts_audit_gate.py")).read()
    # splice the generated literals between the EO markers
    m0 = eo_audit.index("ROWS = {")
    m1 = eo_audit.index("}\n# published raw provenance")
    eo_audit = eo_audit[:m0] + "ROWS = " + rows_lit + "\n" + eo_audit[m1+1:]
    m2 = eo_audit.index("RAW_PROV = {")
    m3 = eo_audit.index("}\nREPLAY")
    eo_audit = eo_audit[:m2] + "RAW_PROV = " + json.dumps(RAW, indent=4, sort_keys=True) + "\n" + eo_audit[m3+1:]
    eo_audit = eo_audit.replace('"part": "EO", "schema": "n11-centralreply-cppgate-34908win6-audit-v1"',
                                '"part": "EQ", "schema": "n11-centralreply-cppgate-30345win18-audit-v1"')
    eo_audit = eo_audit.replace("Part EO fail-closed machine audit for the C++ scrutiny gate run\n(closure class 34908, b33-win-6 rows).",
                                "Part EQ fail-closed machine audit for the C++ scrutiny gate run\n(closure class 30345, b38-win-18 rows).")
    unclosed = eo_audit.count("(closure class 34908, b33-win-6 rows).")
    with open(os.path.join(KIT, "scripts/audit_gate.py"), "w") as f:
        f.write(eo_audit)
    # registry
    reg = {
        "schema": "n11-centralreply-cppgate-30345win18-rows-v1",
        "part": "EQ",
        "main_head_at_maker": head,
        "gate_source": {"path": "cpp/solvers/kyouen_dfpn_root.cpp", "commit": "154f3b7a67b97e13acbaee8b04dc74ddca728d19",
                        "sha256": gsha},
        "targets": {k: {"budget": 15000000, "expected": expected[k],
                        "input_pin": b38pins["input/%s.input.csv" % k][0],
                        "s5_index": bk[k]["s5_index"], "probe_order": bk[k]["probe_order"],
                        "serving_class": bk[k]["serving_class"]} for k in targets},
        "anchors": A,
        "consumed_by_ep": "ai048 (s5 %s; EP increment c245bc4c contains its quadruple)" % bk["ai048"]["s5_index"],
        "excluded_truncated_relicts": sorted(os.listdir(os.path.join(B38, "output/raw")) and [x for x in os.listdir(os.path.join(B38, "output/raw")) if "truncated" in x]),
        "gates": gates,
    }
    with open(os.path.join(inp, "gate-rows-eq.json"), "w") as f:
        json.dump(reg, f, indent=1, sort_keys=True)
        f.write("\n")
    print("maker: ALL PASS; targets=%d anchors=%d" % (len(targets), len(A)))
    print("targets:", " ".join(targets))
    for gname, g in sorted(gates.items()):
        print(" ", gname, g.get("status"), "->", json.dumps({k: v for k, v in g.items() if k != "status"}, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())
