#!/usr/bin/env python3
"""Part EN fail-closed machine audit for the C++ scrutiny gate run.

Gates (all must PASS; any failure -> rc=1 and a FAIL entry in the JSON):
  G1  every raw has a `replay,` row and a terminal `# replay_done rows=1` line,
      and the driver header set (# exact replay: order=0 ... and the
      id,stones,... header line) is present. [rev3: the jsreplay replica also
      prints a "# forbidden quadruples: 95670" telemetry line; the pinned C++
      standalone driver at 154f3b7a67 does NOT, so G1 must not require it -
      the difference is output-format-only, the replay row fields are what
      matter.]
  G2  per-row determinism: p1 == p2 on all replay fields EXCEPT wall_s.
  G3  per-row published-raw pins: (legal, budget, result, nodes) equal the
      pinned expected values transcribed from the published kit raws (SSOT).
  G4  gate-status.log accounting: exactly ROWS GATE-PASS lines, zero
      MISMATCH/GATE-FAIL/GATE-CRASH lines.
  G5  input byte-clones: sha256 equal the published kit input pins.
"""
import hashlib, json, os, re, sys

KIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
KIT = os.path.abspath(KIT)

# key -> (budget, expected "legal,budget,result,nodes",
#          input sha256 pin, provenance of the input pin)
ROWS = {
    "aj030":        ("30000000", "83,30000000,1,15284699",
                     "520ee52abefaec80b800245dd1913489cd511923732e14d3315f4806aec83595",
                     "EK kit (aj030aj039-reprobe30m) input/aj030.input.csv"),
    "aj049":        ("30000000", "80,30000000,1,4998452",
                     "46349391b3aa212cf7ffffbeae94d01b5202f25ca24a6c5294b75ced6184951a",
                     "EK kit input/aj049.input.csv == b39 kit input/aj049.input.csv"),
    "aj050":        ("15000000", "80,15000000,1,1871594",
                     "6c6af79250fce81a25be4d076b75844fc80f6f78bc0b28f17102aae2e3fe8d2e",
                     "b39 kit (class30484-batch39) input/aj050.input.csv"),
    "ai048":        ("15000000", "68,15000000,1,2232854",
                     "e1d2101d2e9daf5a8ef0376e0808412ef17e85f811fae0fa931e38b9bae94710",
                     "b38 kit (class30345-batch38) input/ai048.input.csv"),
    "k04":          ("15000000", "83,15000000,1,9433024",
                     "110776a29b4a9ce4fa0b61c47fc2a586e3475bdd94328db77b506ae8456a80a4",
                     "sixthcost k01-k03 kit input/k04.input.csv"),
    "anchor-at2m":  ("2000000",  "98,2000000,0,2000000",
                     "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
                     "EK kit val-gate at2m-s5-1152921504606851072-536870946.input.csv"),
    "anchor-af039": ("30000000", "89,30000000,2,19234232",
                     "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691",
                     "EK kit input/af039.input.csv"),
    "anchor-aj001": ("30000000", "84,30000000,2,5156075",
                     "2f6daea5ca3b3fe6b7713c8d450af3f3c9f203acacb8a1340255d8e8f656496c",
                     "EK kit input/aj001.input.csv"),
}
# published raw provenance of the expected (budget,result,nodes) per key
RAW_PROV = {
    "aj030": "EK kit output/raw/aj030.p1.out (replay...,30000000,1,15284699,...)",
    "aj049": "EK kit output/raw/aj049.p1.out (30000000,1,4998452); b39 raw is (15000000,1,4998452)",
    "aj050": "b39 kit output/raw/aj050.p1.out (15000000,1,1871594)",
    "ai048": "b38 kit output/raw/ai048.p1.out (15000000,1,2232854)",
    "k04": "sixthcost k01-k03 kit out/k04-replica-raws/at15m-run1-k04.out.csv (15000000,1,9433024)",
    "anchor-at2m": "EK kit val-gate at2m published-baseline (2000000,0,2000000)",
    "anchor-af039": "EK kit output/raw/af039.p1.out (30000000,2,19234232); canonical cache row",
    "anchor-aj001": "EK kit output/raw/aj001.p1.out (30000000,2,5156075)",
}
REPLAY = re.compile(r"^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),([0-9.]+),(\d+),(\d+)$")

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
    out = {"part": "EN", "schema": "n11-centralreply-cppgate-30484win4-audit-v1",
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
