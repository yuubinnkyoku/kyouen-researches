#!/usr/bin/env python3
"""Part SK (sixth-cost exclusive C++ scrutiny gate) fail-closed machine
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
"""
import hashlib, json, os, re, sys

KIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
KIT = os.path.abspath(KIT)

# key -> (budget, expected "legal,budget,result,nodes",
#          input sha256 pin, provenance of the input pin)
ROWS = {
 "k01": [
  "15000000",
  "87,15000000,2,10369650",
  "fd2cf12d5d0691a85309ffd56508dcaa9dbd429a299d34c19e17692686647c7c",
  "probe kit input/k01.input.csv (sixth-cost exclusive probe batch; input byte-pin registry SSOT)"
 ],
 "k02": [
  "15000000",
  "87,15000000,1,7717432",
  "b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887",
  "probe kit input/k02.input.csv (sixth-cost exclusive probe batch; input byte-pin registry SSOT)"
 ],
 "k03": [
  "15000000",
  "81,15000000,1,9255414",
  "9e40900a8df77e9ce139359ec289d664c08b8f9010d50e80149b4e9e624a3b40",
  "probe kit input/k03.input.csv (sixth-cost exclusive probe batch; input byte-pin registry SSOT)"
 ],
 "k04": [
  "15000000",
  "83,15000000,1,9433024",
  "110776a29b4a9ce4fa0b61c47fc2a586e3475bdd94328db77b506ae8456a80a4",
  "probe kit input/k04.input.csv (sixth-cost exclusive probe batch; input byte-pin registry SSOT)"
 ],
 "k05": [
  "15000000",
  "88,15000000,1,13397611",
  "7f30311de61973274163246fb9502b65922788da868b47165ef86646ebb3e750",
  "probe kit input/k05.input.csv (sixth-cost exclusive probe batch; input byte-pin registry SSOT)"
 ],
 "k06": [
  "15000000",
  "89,15000000,2,8182231",
  "e94c2ade1facf9de78b91936238acacc196770878c50bd84bfdd585d91e8e6a4",
  "probe kit input/k06.input.csv (sixth-cost exclusive probe batch; input byte-pin registry SSOT)"
 ],
 "k07": [
  "2000000",
  "87,2000000,2,1419823",
  "1e3deebf9777b232e6dbec4cabf64a12039926f339b8ca9a91c95635e094bdb5",
  "probe kit input/k07.input.csv (sixth-cost exclusive probe batch; input byte-pin registry SSOT)"
 ],
 "k08": [
  "15000000",
  "89,15000000,1,6195897",
  "6fcbf158817f25e82ebb73010c49638949aa2f8ff9d48713d4806a2d4426c35f",
  "probe kit input/k08.input.csv (sixth-cost exclusive probe batch; input byte-pin registry SSOT)"
 ],
 "anchor-af039": [
  "30000000",
  "89,30000000,2,19234232",
  "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691",
  "EQ kit input/anchor-af039.input.csv (byte-clone; == EN/EO/EV kit input; EV kit MANIFEST-sha256.txt pin)"
 ],
 "anchor-aj001": [
  "30000000",
  "84,30000000,2,5156075",
  "2f6daea5ca3b3fe6b7713c8d450af3f3c9f203acacb8a1340255d8e8f656496c",
  "EQ kit input/anchor-aj001.input.csv (byte-clone; == EN/EO/EV kit input; EV kit MANIFEST-sha256.txt pin)"
 ],
 "anchor-at2m": [
  "2000000",
  "98,2000000,0,2000000",
  "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
  "EQ kit input/anchor-at2m.input.csv (byte-clone; == EN/EO/EV kit input; EV kit MANIFEST-sha256.txt pin)"
 ]
}

RAW_PROV = {
 "k01": "probe kit output/raw/at15m-run1-k01.out.csv (published replica 87,15000000,2,10369650); two-pass node-exact vs at15m-run2-k01.out.csv; third-impl verdict-level agreement published",
 "k02": "probe kit output/raw/at15m-run1-k02.out.csv (published replica 87,15000000,1,7717432); two-pass node-exact vs at15m-run2-k02.out.csv; NO published third-impl reproduction (k02): the C++ gate IS the second implementation for this row",
 "k03": "probe kit output/raw/at15m-run1-k03.out.csv (published replica 81,15000000,1,9255414); two-pass node-exact vs at15m-run2-k03.out.csv; third-impl verdict-level agreement published",
 "k04": "probe kit output/raw/at15m-run1-k04.out.csv (published replica 83,15000000,1,9433024); two-pass node-exact vs at15m-run2-k04.out.csv; third-impl verdict-level agreement published",
 "k05": "probe kit output/raw/at15m-run1-k05.out.csv (published replica 88,15000000,1,13397611); two-pass node-exact vs at15m-run2-k05.out.csv; third-impl verdict-level agreement published",
 "k06": "probe kit output/raw/at15m-run1-k06.out.csv (published replica 89,15000000,2,8182231); two-pass node-exact vs at15m-run2-k06.out.csv; third-impl verdict-level agreement published",
 "k07": "probe kit output/raw/at15m-run1-k07.out.csv (published replica 87,2000000,2,1419823); two-pass node-exact vs at15m-run2-k07.out.csv; third-impl verdict-level agreement published",
 "k08": "probe kit output/raw/at15m-run1-k08.out.csv (published replica 89,15000000,1,6195897); two-pass node-exact vs at15m-run2-k08.out.csv; third-impl verdict-level agreement published",
 "anchor-af039": "EQ kit raw condition (budget-ceiling baseline); == EV kit anchors block",
 "anchor-aj001": "EQ kit raw condition (budget-ceiling baseline); == EV kit anchors block",
 "anchor-at2m": "EQ kit raw condition (budget-ceiling baseline); == EV kit anchors block"
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
    out = {"part": "SK", "schema": "n11-sixthcost-exclusive-cppgate-audit-v1",
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
