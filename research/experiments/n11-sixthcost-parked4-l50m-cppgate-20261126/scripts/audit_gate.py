#!/usr/bin/env python3
"""Part SM (parked4 L50M WIN rows C++ scrutiny gate) fail-closed
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
"""
import hashlib, json, os, re, sys

KIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
KIT = os.path.abspath(KIT)

# key -> (budget, expected "legal,budget,result,nodes",
#          input sha256 pin, provenance of the input pin)
ROWS = {
 "k13": [
  "50000000",
  "95,50000000,1,16402480",
  "298dd6e6b6655d12aefaae138a2e1d85388220546ff68e4d6b7081c6097b0526",
  "parked4 kit input/batch-k13.input.csv (sixth-cost parked-4-keys S5 L50M ladder kit; input SSOT)"
 ],
 "k19": [
  "50000000",
  "95,50000000,1,15379062",
  "88c107d7d060ef756a394d722de3a80b4ee60bad5647785cbbb65eb088da6190",
  "parked4 kit input/batch-k19.input.csv (sixth-cost parked-4-keys S5 L50M ladder kit; input SSOT)"
 ],
 "anchor-af039": [
  "30000000",
  "89,30000000,2,19234232",
  "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691",
  "SK kit input/anchor-af039.input.csv (byte-clone; == EQ/EN/EO/EV kit input; SK kit MANIFEST-sha256.txt pin)"
 ],
 "anchor-aj001": [
  "30000000",
  "84,30000000,2,5156075",
  "2f6daea5ca3b3fe6b7713c8d450af3f3c9f203acacb8a1340255d8e8f656496c",
  "SK kit input/anchor-aj001.input.csv (byte-clone; == EQ/EN/EO/EV kit input; SK kit MANIFEST-sha256.txt pin)"
 ],
 "anchor-at2m": [
  "2000000",
  "98,2000000,0,2000000",
  "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
  "SK kit input/anchor-at2m.input.csv (byte-clone; == EQ/EN/EO/EV kit input; SK kit MANIFEST-sha256.txt pin)"
 ]
}

RAW_PROV = {
 "k13": "parked4 kit output/raw/l50m-run1-1152921573327376384-536870912.out.csv (published replica 95,50000000,1,16402480); two-pass node-exact vs l50m-run2-1152921573327376384-536870912.out.csv; third-impl verdict-level agreement published (batch 32/32, k-row x3 runs)",
 "k19": "parked4 kit output/raw/l50m-run1-10376293541461626880-65664.out.csv (published replica 95,50000000,1,15379062); two-pass node-exact vs l50m-run2-10376293541461626880-65664.out.csv; third-impl verdict-level agreement published (batch 32/32, k-row x3 runs)",
 "anchor-af039": "EV/SK kit raw condition (budget-ceiling baseline); == SK kit anchors block",
 "anchor-aj001": "EV/SK kit raw condition (budget-ceiling baseline); == SK kit anchors block",
 "anchor-at2m": "EV/SK kit raw condition (budget-ceiling baseline); == SK kit anchors block"
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
    out = {"part": "SM", "schema": "n11-sixthcost-parked4-cppgate-audit-v1",
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
