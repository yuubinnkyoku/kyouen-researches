#!/usr/bin/env python3
"""Part EV fail-closed machine audit for the C++ scrutiny gate run
(closure-batch WINs b018/d002/e002/f017 at the 15M condition).

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
      (closure batch kits class16757/20421/16371-batch4/12264-batch5 at
      15M for the four WIN rows; EQ kit raws for the anchors).
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
    ],
    "b018": [
        "15000000",
        "60,15000000,1,3549602",
        "18f9aa5423aa2ff36adb5e49756e188f990e7d74cab5939dfd9ff908227c1b2a",
        "batch kit input/b018.input.csv (class 16757 batch; batch-keys SSOT)"
    ],
    "d002": [
        "15000000",
        "73,15000000,1,5359994",
        "d2d739232fe2cf57fa9e0aafdd3117c5469877572b2681db2c574bb8c6b0537d",
        "batch kit input/d002.input.csv (class 20421 batch; batch-keys SSOT)"
    ],
    "e002": [
        "15000000",
        "79,15000000,1,14112632",
        "d0a7ae5d073fb1f701f014730b46dbea90d20e9b05526a4e48d4b8a82a19a28e",
        "batch kit input/e002.input.csv (class 16371 batch; batch-keys SSOT)"
    ],
    "f017": [
        "15000000",
        "82,15000000,1,3522635",
        "d15dae820370554357059bc7b676a624d34e9ca2a7037ab0abd5f25f928e5c5f",
        "batch kit input/f017.input.csv (class 12264 batch; batch-keys SSOT)"
    ]
}

# published raw provenance of the expected (budget,result,nodes) per key
RAW_PROV = {
    "anchor-af039": "EQ kit output/raw/anchor-af039.p1.out (30000000,2,19234232); budget-ceiling baseline",
    "anchor-aj001": "EQ kit output/raw/anchor-aj001.p1.out (30000000,2,5156075); budget-ceiling baseline",
    "anchor-at2m": "EQ kit output/raw/anchor-at2m.p1.out (2000000,0,2000000); budget-ceiling baseline",
    "b018": "batch kit output/raw/b018.p1.out (replay...,3549602,...); two-pass node-exact vs b018.p2; third-impl reverify a/b agree verdict-level",
    "d002": "batch kit output/raw/d002.p1.out (replay...,5359994,...); two-pass node-exact vs d002.p2; third-impl reverify a/b agree verdict-level",
    "e002": "batch kit output/raw/e002.p1.out (replay...,14112632,...); two-pass node-exact vs e002.p2; third-impl reverify a/b agree verdict-level",
    "f017": "batch kit output/raw/f017.p1.out (replay...,3522635,...); two-pass node-exact vs f017.p2; third-impl reverify a/b agree verdict-level"
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
    out = {"part": "EV", "schema": "n11-centralreply-cppgate-wins41164-audit-v1",
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
