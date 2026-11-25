#!/usr/bin/env python3
"""Part EO fail-closed machine audit for the C++ scrutiny gate run
(closure class 34908, b33-win-6 rows).

Gates (all must PASS; any failure -> rc=1 and a FAIL entry in the JSON):
  G1  every raw has a `replay,` row and a terminal `# replay_done rows=1`
      line, and the driver header set (# exact replay: order=0 ... and the
      id,stones,... header line) is present. [EN rev3 lesson kept: the
      jsreplay replica also prints a "# forbidden quadruples: ..." telemetry
      line; the pinned C++ standalone driver at 154f3b7a67 does NOT, so G1
      must not require it - output-format-only difference.]
  G2  per-row determinism: p1 == p2 on all replay fields EXCEPT wall_s.
  G3  per-row published-raw pins: (legal, budget, result, nodes) equal the
      pinned expected values transcribed from the published source raws
      (EG kit sources/b33-raw at 15M for af029/af047/af050/af053 and
      sources/ea-raw at 30M for af023/af048; EN kit raws for the anchors).
      [EN rev4 lesson kept: REPLAY regex must have exactly 10 capture
      groups; under an 11-group regex G2/G3 silently never matched. The
      regex below is byte-checked against a 10-group pattern.]
  G4  gate-status.log accounting: exactly ROWS GATE-PASS lines, zero
      MISMATCH/GATE-FAIL/GATE-CRASH lines.
  G5  input byte-clones: sha256 equal the pinned source-kit input pins
      (EG kit input/ for the six WIN rows at commit bb661fbb; EN kit
      input/ for the three anchors at commit 949e68a7).
"""
import hashlib, json, os, re, sys

KIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
KIT = os.path.abspath(KIT)

# key -> (budget, expected "legal,budget,result,nodes",
#          input sha256 pin, provenance of the input pin)
ROWS = {
    "af029":        ("15000000", "86,15000000,1,4862485",
                     "b5500b8d98cd3cbef56f6177245d8e3c21c31081f2252c6454f1aee73ce30c10",
                     "EG kit (b33win6 thirdimpl) input/af029.input.csv (== b33 kit input, blob 4a589f7a)"),
    "af047":        ("15000000", "84,15000000,1,9841975",
                     "24cc1aa00849f6b74c7f976b46903874321aac981f62dd542e51948a3f351418",
                     "EG kit input/af047.input.csv (== b33 kit input, blob 6e0e1ae7)"),
    "af050":        ("15000000", "94,15000000,1,7311834",
                     "3bc623db974bc6285c575b8575a75510c3e9f1909a650a4969e214225e507729",
                     "EG kit input/af050.input.csv (== b33 kit input, blob bae112ec)"),
    "af053":        ("15000000", "90,15000000,1,5182129",
                     "b30a43a948945d7b49946c28dec20b5859aac1003d522f042cfff4d1225d989e",
                     "EG kit input/af053.input.csv (== b33 kit input, blob 4d8b7bd1)"),
    "af023":        ("30000000", "94,30000000,1,28933179",
                     "0ba31256582eae15cc80fb2bdbfe56a140533828cdab7a05eeef6ca1089a1c08",
                     "EG kit input/af023.input.csv (== EA reprobe kit input, blob c13887eb)"),
    "af048":        ("30000000", "87,30000000,1,17816616",
                     "d619dcd7d47d7b65f1c4325d99b69211826eb83732c3eb475f14ea4f9f973422",
                     "EG kit input/af048.input.csv (== EA reprobe kit input, blob c1057a18)"),
    "anchor-at2m":  ("2000000",  "98,2000000,0,2000000",
                     "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
                     "EN kit (30484 cppgate) input/anchor-at2m.input.csv (== EK at2m val-gate input, blob b6adf964)"),
    "anchor-af039": ("30000000", "89,30000000,2,19234232",
                     "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691",
                     "EN kit input/anchor-af039.input.csv (== EK kit input/af039.input.csv)"),
    "anchor-aj001": ("30000000", "84,30000000,2,5156075",
                     "2f6daea5ca3b3fe6b7713c8d450af3f3c9f203acacb8a1340255d8e8f656496c",
                     "EN kit input/anchor-aj001.input.csv (== EK kit input/aj001.input.csv)"),
}
# published raw provenance of the expected (budget,result,nodes) per key
RAW_PROV = {
    "af029": "EG kit sources/b33-raw/af029.p1.out (replay...,15000000,1,4862485,...); EG sources/ea-raw/af029.p1.out 30M anchor row is (30000000,1,4862485) - identical nodes at the higher budget",
    "af047": "EG kit sources/b33-raw/af047.p1.out (15000000,1,9841975)",
    "af050": "EG kit sources/b33-raw/af050.p1.out (15000000,1,7311834)",
    "af053": "EG kit sources/b33-raw/af053.p1.out (15000000,1,5182129)",
    "af023": "EG kit sources/ea-raw/af023.p1.out (30000000,1,28933179); b33 15M row is EXHAUSTED (budget ceiling) and is NOT pinned here",
    "af048": "EG kit sources/ea-raw/af048.p1.out (30000000,1,17816616); b33 15M row is EXHAUSTED (budget ceiling) and is NOT pinned here",
    "anchor-at2m": "EN kit output/raw/anchor-at2m.p1.out (2000000,0,2000000); budget-ceiling baseline",
    "anchor-af039": "EN kit output/raw/anchor-af039.p1.out (30000000,2,19234232); canonical cache row, budget-ceiling baseline",
    "anchor-aj001": "EN kit output/raw/anchor-aj001.p1.out (30000000,2,5156075); budget-ceiling baseline",
}
REPLAY = re.compile(r"^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),([0-9.]+),(\d+),(\d+)$")
assert len(REPLAY.groupindex) == 0 and REPLAY.groups == 10, "rev4 lesson: exactly 10 capture groups"

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def main():
    gates = {}
    def g(name, ok, detail=""):
        gates[name] = {"status": "PASS" if ok else "FAIL", "detail": detail}
        return ok

    ok = True
    parsed = {}
    for key, (budget, expected, in_pin, prov) in sorted(ROWS.items()):
        rec = {"budget": budget, "expected": expected}
        # G5 input pins
        ipath = os.path.join(KIT, "input", key + ".input.csv")
        if not os.path.isfile(ipath):
            ok &= g("G5:" + key, False, "missing input file")
            continue
        ok &= g("G5:" + key, sha256(ipath) == in_pin,
                "sha256 %s %s" % (sha256(ipath), "==" if sha256(ipath) == in_pin else "!= " + in_pin))
        rows = {}
        for p in ("p1", "p2"):
            rpath = os.path.join(KIT, "output", "raw", key + "." + p + ".out")
            if not os.path.isfile(rpath):
                ok &= g("G1:" + key + ":" + p, False, "missing raw")
                rows[p] = None
                continue
            text = open(rpath).read()
            m = [REPLAY.match(l) for l in text.splitlines() if l.startswith("replay,")]
            done = "# replay_done rows=1" in text
            hdr = "# exact replay: order=0 " in text and "# exact replay: id,stones,legal,is_or,budget,result,nodes,wall_s,key_lo,key_hi" in text
            ok &= g("G1:" + key + ":" + p, bool(len(m) == 1 and done and hdr),
                    "replay_rows=%d done=%s header=%s" % (len(m), done, hdr))
            rows[p] = list(m[0].groups()) if len(m) == 1 and m[0] else None
        if rows["p1"] is None or rows["p2"] is None:
            parsed[key] = rec; continue
        # G2 determinism on all fields except wall_s (index 8)
        a = rows["p1"]; b = rows["p2"]
        det = (a[:7] == b[:7]) and (a[8:] == b[8:])
        ok &= g("G2:" + key, det, "p1=%s p2=%s" % (",".join(a), ",".join(b)))
        # G3 published pins: fields legal(2),budget(4),result(5),nodes(6) -> f3,6,7,8 of csv
        rec["observed_p1"] = ",".join([a[2], a[4], a[5], a[6]])
        ok &= g("G3:" + key, ",".join([a[2], a[4], a[5], a[6]]) == expected,
                "observed %s expected %s (%s)" % (rec["observed_p1"], expected, RAW_PROV[key]))
        parsed[key] = rec
    # G4 status accounting
    spath = os.path.join(KIT, "output", "gate-status.log")
    okp = 0; bad = []
    if os.path.isfile(spath):
        for line in open(spath):
            if " GATE-PASS " in line: okp += 1
            elif "MISMATCH" in line or "GATE-FAIL" in line or "GATE-CRASH" in line:
                bad.append(line.strip())
    ok &= g("G4", okp == len(ROWS) and not bad,
            "passes=%d/%d bad=%d" % (okp, len(ROWS), len(bad)))
    out = {"part": "EO", "schema": "n11-centralreply-cppgate-34908win6-audit-v1",
           "rows": parsed, "gates": gates,
           "overall": "PASS" if ok else "FAIL"}
    opath = os.path.join(KIT, "output", "audit_gate.json")
    with open(opath, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    print("audit_gate:", out["overall"])
    for k, v in sorted(gates.items()):
        if v["status"] == "FAIL":
            print("FAIL", k, v["detail"])
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
