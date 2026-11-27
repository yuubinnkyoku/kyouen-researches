#!/usr/bin/env python3
"""Part SX (seventh-cost k05 L50M WIN row) fail-closed single-row audit.

FRESH single-row implementation (Part SS precedent, disclosed in the
declaration/README/maker): not a byte transform of the SW/SR batch audit.
Reads input/gate-rows.json (machine-derived pins from the maker) and
audits the gate outputs of the single k05 target + 3 calibration anchors.

Gates: G0 gate-rows pins (schema, gate-source commit/sha/header pins,
target expected quadruple + input pin, anchors block); G1 per-row raw
shape (replay row + terminal replay_done + driver headers); G2 per-row
determinism (p1 == p2 on every replay field except wall_s); G3 published
pin (legal,budget,result,nodes) - for k05 the published WIN(1) quadruple
90,50000000,1,15763505 of the at50m cold pair (ff750cc6 x2); G4
gate-status accounting (exactly len(ROWS) GATE-PASS, zero bad); G5 input
byte-clone pins (k05 == published seventh-cost kit MANIFEST pin, anchors
== SR/SW kit anchor pins).

No verdict is consumed: the k05 WIN row stays an UNCONSUMED label
(canonical head 42dbb58f keeps it absent). A WIN(1) gate result is a
verdict-level agreement of the second implementation with the published
first-implementation cold pair, nothing more; third-impl corroboration
stays a separate future Part before any adoption. 11x11, the two-stone
root {60,27}, and its remaining third moves 100/108 stay UNKNOWN
throughout. Nodes are bookkeeping, never verdicts.
"""
import hashlib, json, os, re, sys

KIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
KIT = os.path.abspath(KIT)

REPLAY = re.compile(r"^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),([0-9.]+),(\d+),(\d+)$")
assert REPLAY.groups == 10, "rev4 lesson: exactly 10 capture groups"

INPUT_PINS = {
    "k05": "a73a6c70a221619b94ce29c188434d24a1f8af43653b37c1019a3286ba2ddb91",
    "anchor-af039": "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691",
    "anchor-aj001": "2f6daea5ca3b3fe6b7713c8d450af3f3c9f203acacb8a1340255d8e8f656496c",
    "anchor-at2m": "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
}
ANCHORS = {
    "anchor-at2m": "98,2000000,0,2000000",
    "anchor-aj001": "84,30000000,2,5156075",
    "anchor-af039": "89,30000000,2,19234232",
}
K05_EXPECT = "90,50000000,1,15763505"
K05_BUDGET = "50000000"
ROWS = dict([("k05", [K05_BUDGET, K05_EXPECT])] + [(a, [ANCHORS[a].split(",")[1], ANCHORS[a]]) for a in ANCHORS])

def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def main():
    gates = {}
    def g(name, ok, detail=""):
        gates[name] = {"status": "PASS" if ok else "FAIL", "detail": detail}
        return ok
    ok = True
    gr = json.load(open(os.path.join(KIT, "input", "gate-rows.json")))
    ok &= g("G0:schema", gr.get("schema") == "n11-seventhcost-k05-l50m-cppgate-rows-v1", gr.get("schema"))
    gs = gr.get("gate_source", {})
    ok &= g("G0:gate-source", gs.get("commit") == "154f3b7a67b97e13acbaee8b04dc74ddca728d19"
            and gs.get("sha256") == "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e"
            and gs.get("header_pins", {}).get("kyouen_residual_micro.hpp") == "5976935dcfccb9b5a26fa68f8de20868ce45363dd8c372dcd67d9b841167e7f5"
            and gs.get("header_pins", {}).get("n11_s5_quarantine.hpp") == "2e36d69481fafcde7aede8ae4fedf3d5477f91ee9846bcd4ae2975f32a4ba1a5")
    ok &= g("G0:target-expected", gr.get("target", {}).get("k05", {}).get("expected") == K05_EXPECT
            and gr.get("target", {}).get("k05", {}).get("raw_pair_sha256") == "ff750cc63e3ead314a5c5a22b09cca5588f284a34dc08c5c4d1cc5716eda342c")
    ok &= g("G0:anchors", gr.get("anchors") == ANCHORS)
    ok &= g("G0:head-pin", gr.get("canonical_head", {}).get("sha256") == "42dbb58ffe8dd02a81f4a92993d08e3fbebdaeb4b4f7bf33e142120ff055bdc4")

    parsed = {}
    for key in sorted(ROWS):
        budget, expected = ROWS[key]
        rec = {"budget": budget, "expected": expected}
        ok &= g("G5:" + key, sha256(os.path.join(KIT, "input", key + ".input.csv")) == INPUT_PINS[key],
                "input sha mismatch" if sha256(os.path.join(KIT, "input", key + ".input.csv")) != INPUT_PINS[key] else "")
        rows = {}
        for p in ("p1", "p2"):
            rpath = os.path.join(KIT, "output", "raw", key + "." + p + ".out")
            if not os.path.isfile(rpath):
                ok &= g("G1:%s:%s" % (key, p), False, "missing raw"); rows[p] = None; continue
            text = open(rpath).read()
            m = [REPLAY.match(l) for l in text.splitlines() if l.startswith("replay,")]
            done = "# replay_done rows=1" in text
            hdr = "# exact replay: order=0 " in text and "# exact replay: id,stones,legal,is_or,budget,result,nodes,wall_s,key_lo,key_hi" in text
            ok &= g("G1:%s:%s" % (key, p), bool(len(m) == 1 and done and hdr),
                    "replay_rows=%d done=%s header=%s" % (len(m), done, hdr))
            rows[p] = list(m[0].groups()) if len(m) == 1 and m[0] else None
        if rows["p1"] is None or rows["p2"] is None:
            parsed[key] = rec; continue
        a, b = rows["p1"], rows["p2"]
        ok &= g("G2:" + key, (a[:7] == b[:7]) and (a[8:] == b[8:]), "p1=%s p2=%s" % (",".join(a), ",".join(b)))
        ok &= g("G3:" + key, ",".join([a[2], a[4], a[5], a[6]]) == expected,
                "observed %s expected %s" % (",".join([a[2], a[4], a[5], a[6]]), expected))
        rec["observed_p1"] = ",".join([a[2], a[4], a[5], a[6]])
        parsed[key] = rec
    spath = os.path.join(KIT, "output", "gate-status.log")
    okp = 0; bad = []
    if os.path.isfile(spath):
        for line in open(spath):
            if " GATE-PASS " in line: okp += 1
            elif "MISMATCH" in line or "GATE-FAIL" in line or "GATE-CRASH" in line:
                bad.append(line.strip())
    ok &= g("G4", okp == len(ROWS) and not bad, "passes=%d/%d bad=%d" % (okp, len(ROWS), len(bad)))
    out = {"part": "SX", "schema": "n11-seventhcost-k05-l50m-cppgate-audit-v1",
           "rows": parsed, "gates": gates, "overall": "PASS" if ok else "FAIL"}
    with open(os.path.join(KIT, "output", "audit_gate.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True); f.write("\n")
    print("audit_gate:", out["overall"])
    for k, v in sorted(gates.items()):
        if v["status"] == "FAIL": print("FAIL", k, v["detail"])
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
