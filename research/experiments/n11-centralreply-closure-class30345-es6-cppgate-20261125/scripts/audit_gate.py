#!/usr/bin/env python3
"""Part ET fail-closed machine audit for the C++ scrutiny gate run
(closure class 30345, ES re-probe-6 rows at the 30M condition).

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
    "ai007": [
        "30000000",
        "84,30000000,1,16090493",
        "73c6f31983c8a23490f30120fbe9951ca97d294461af7186fa4983278f610bc8",
        "ES kit input/ai007.input.csv (byte-clone of b38 kit input; targets-30m SSOT 1c27a238)"
    ],
    "ai024": [
        "30000000",
        "86,30000000,2,19127057",
        "52d5edeade664da448d0414f8035026659a802b8a884e0ba7f3198ec38dab88a",
        "ES kit input/ai024.input.csv (byte-clone of b38 kit input; targets-30m SSOT 1c27a238)"
    ],
    "ai030": [
        "30000000",
        "91,30000000,2,16504156",
        "99f67a1f27fe31cb480bceeb2579f63467dd7e45fe5051610c02036b8c1d40b2",
        "ES kit input/ai030.input.csv (byte-clone of b38 kit input; targets-30m SSOT 1c27a238)"
    ],
    "ai038": [
        "30000000",
        "89,30000000,2,19851840",
        "93f1f2d168e0b21ad6bbbfbc1f65c3653930f71d78731d58f070eb07aa154572",
        "ES kit input/ai038.input.csv (byte-clone of b38 kit input; targets-30m SSOT 1c27a238)"
    ],
    "ai040": [
        "30000000",
        "85,30000000,1,20711023",
        "e535844a4133e34542df079644514cea868bd062acaa8adef5026b8ca90f6656",
        "ES kit input/ai040.input.csv (byte-clone of b38 kit input; targets-30m SSOT 1c27a238)"
    ],
    "ai041": [
        "30000000",
        "91,30000000,2,15781960",
        "443f757c0052e48b3bd5bd8cd30588cac8e5041ae96811a947928cc7ce0f4fa1",
        "ES kit input/ai041.input.csv (byte-clone of b38 kit input; targets-30m SSOT 1c27a238)"
    ],
    "anchor-af039": [
        "30000000",
        "89,30000000,2,19234232",
        "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691",
        "EQ kit input/anchor-af039.input.csv (byte-clone; == EO/EN kit input)"
    ],
    "anchor-aj001": [
        "30000000",
        "84,30000000,2,5156075",
        "2f6daea5ca3b3fe6b7713c8d450af3f3c9f203acacb8a1340255d8e8f656496c",
        "EQ kit input/anchor-aj001.input.csv (byte-clone; == EO/EN kit input)"
    ],
    "anchor-at2m": [
        "2000000",
        "98,2000000,0,2000000",
        "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
        "EQ kit input/anchor-at2m.input.csv (byte-clone; == EO/EN kit input)"
    ]
}

# published raw provenance of the expected (budget,result,nodes) per key
RAW_PROV = {
    "ai007": "ES kit output/raw/ai007.p1.out (replay...,16090493,...); two-pass node-exact vs ai007.p2",
    "ai024": "ES kit output/raw/ai024.p1.out (replay...,19127057,...); two-pass node-exact vs ai024.p2",
    "ai030": "ES kit output/raw/ai030.p1.out (replay...,16504156,...); two-pass node-exact vs ai030.p2",
    "ai038": "ES kit output/raw/ai038.p1.out (replay...,19851840,...); two-pass node-exact vs ai038.p2",
    "ai040": "ES kit output/raw/ai040.p1.out (replay...,20711023,...); two-pass node-exact vs ai040.p2",
    "ai041": "ES kit output/raw/ai041.p1.out (replay...,15781960,...); two-pass node-exact vs ai041.p2",
    "anchor-af039": "EQ kit output/raw/anchor-af039.p1.out (30000000,2,19234232); canonical cache row, budget-ceiling baseline",
    "anchor-aj001": "EQ kit output/raw/anchor-aj001.p1.out (30000000,2,5156075); budget-ceiling baseline",
    "anchor-at2m": "EQ kit output/raw/anchor-at2m.p1.out (2000000,0,2000000); budget-ceiling baseline; EO raws == EN raws (published observation)"
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
    out = {"part": "ET", "schema": "n11-centralreply-cppgate-30345es6-audit-v1",
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
