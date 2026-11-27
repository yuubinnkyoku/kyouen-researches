#!/usr/bin/env python3
"""Ninth-cost k12 WIN row fail-closed single-row audit.

Disclosed ADAPTATION of the published n11-ninthcost-4loss-cppgate
batch audit (same session lineage): the target set is reduced to the
single WIN row k12 (class 1297036692683751424:134217728) + 3
calibration anchors; all pins (input sha, expected quadruple
92,15000000,1,14521862, key-pair, schema names) are the k12 values;
the G0-G6 gate semantics are unchanged from the published audit.
Reads input/gate-rows.json and audits the gate outputs of k12 and the
3 anchors (anchor-at2m / anchor-aj001 / anchor-af039).

Gates: G0 gate-rows pins (schema, gate-source commit/sha/header pins,
k12 expected quadruple + stage pin, head pin); G1 per-row raw shape;
G2 per-row determinism (p1 == p2 on every replay field except wall_s);
G3 published pin (legal,budget,result,nodes) + key-pair fields; G4
gate-status accounting (exactly 4 GATE-PASS, zero bad); G5 input byte
pins (k12 == published ninth-cost kit MANIFEST pin, anchors == SW kit
anchor pins); G6 canonical head freshness re-verification (sha 0935c94c
+ census 6,875 WIN203/LOSS6672 + k12 [lo,hi] absent) via N9_HEAD
(fail-closed: no skip allowed).

No verdict is consumed: the k12 WIN row stays an UNCONSUMED label
(canonical head 0935c94c keeps it absent). A WIN(1) gate result is a
verdict-level agreement of the second implementation with the published
first-implementation cold pair, nothing more. 11x11, the two-stone root
{60,27}, and its remaining third moves 100/108 stay UNKNOWN throughout.
Nodes are bookkeeping, never verdicts.
"""
import hashlib, json, os, re, sys

KIT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

REPLAY = re.compile(r"^replay,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),([0-9.]+),(\d+),(\d+)$")
assert REPLAY.groups == 10, "exactly 10 capture groups"

INPUT_PINS = {
    "k12": "03311e09112bb9998b4621087abe90f91fa4fdaf61afeed52b62521dafaaa2c2",
    "anchor-af039": "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691",
    "anchor-aj001": "2f6daea5ca3b3fe6b7713c8d450af3f3c9f203acacb8a1340255d8e8f656496c",
    "anchor-at2m": "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
}
ANCHORS = {
    "anchor-at2m": "98,2000000,0,2000000",
    "anchor-aj001": "84,30000000,2,5156075",
    "anchor-af039": "89,30000000,2,19234232",
}
KEYPAIRS = {
    "k12": ("1297036692683751424", "134217792"),
}
BUDGET = "15000000"
EXPECT = {
    "k12": "92,15000000,1,14521862",
}
HEAD_SHA = "0935c94c03a9a3fbdf2a55aca90bb986a019dfd26c0097ab2c75709d590e9ca4"
HEAD_ROWS, HEAD_WIN, HEAD_LOSS = 6875, 203, 6672
ROWS = dict([(k, [BUDGET, EXPECT[k]]) for k in EXPECT] + [(a, [ANCHORS[a].split(",")[1], ANCHORS[a]]) for a in ANCHORS])

def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def main():
    gates = {}
    def g(name, ok, detail=""):
        gates[name] = {"status": "PASS" if ok else "FAIL", "detail": str(detail)}
        return ok
    ok = True
    gr = json.load(open(os.path.join(KIT, "input", "gate-rows.json")))
    ok &= g("G0:schema", gr.get("schema") == "n11-ninthcost-k12win-cppgate-rows-v1", gr.get("schema"))
    gs = gr.get("gate_source", {})
    ok &= g("G0:gate-source", gs.get("commit") == "154f3b7a67b97e13acbaee8b04dc74ddca728d19"
            and gs.get("sha256") == "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e"
            and gs.get("header_pins", {}).get("kyouen_residual_micro.hpp") == "5976935dcfccb9b5a26fa68f8de20868ce45363dd8c372dcd67d9b841167e7f5"
            and gs.get("header_pins", {}).get("n11_s5_quarantine.hpp") == "2e36d69481fafcde7aede8ae4fedf3d5477f91ee9846bcd4ae2975f32a4ba1a5")
    for k in EXPECT:
        t = gr.get("targets", {}).get(k, {})
        ok &= g("G0:target-expected:" + k, t.get("expected") == EXPECT[k], t.get("expected"))
    ok &= g("G0:anchors", gr.get("anchors") == ANCHORS)
    ok &= g("G0:head-pin", gr.get("canonical_head", {}).get("sha256") == HEAD_SHA)

    parsed = {}
    for key in sorted(ROWS):
        budget, expected = ROWS[key]
        rec = {"budget": budget, "expected": expected}
        ip = os.path.join(KIT, "input", key + ".input.csv")
        isha = sha256(ip) if os.path.isfile(ip) else "missing"
        ok &= g("G5:" + key, isha == INPUT_PINS[key], isha)
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
        quad = ",".join([a[2], a[4], a[5], a[6]])
        ok &= g("G3:" + key, quad == expected, "observed %s expected %s" % (quad, expected))
        if key in KEYPAIRS:
            ok &= g("G3:%s:key-pair" % key, a[8] == KEYPAIRS[key][0] and a[9] == KEYPAIRS[key][1], "%s:%s" % (a[8], a[9]))
        rec["observed_p1"] = quad
        parsed[key] = rec
    spath = os.path.join(KIT, "output", "gate-status.log")
    okp = 0; bad = []
    if os.path.isfile(spath):
        for line in open(spath):
            if " GATE-PASS " in line: okp += 1
            elif "MISMATCH" in line or "GATE-FAIL" in line or "GATE-CRASH" in line:
                bad.append(line.strip())
    ok &= g("G4", okp == len(ROWS) and not bad, "passes=%d/%d bad=%d" % (okp, len(ROWS), len(bad)))
    head = os.environ.get("N9_HEAD", "")
    ok &= g("G6:head-env", bool(head), "N9_HEAD must point at the canonical head cache")
    if head:
        hs = sha256(head)
        ok &= g("G6:head-sha", hs == HEAD_SHA, hs)
        data = [l for l in open(head).read().splitlines() if l.startswith("s5verdict,")]
        wins = sum(1 for l in data if l.split(",")[4] == "1")
        losses = sum(1 for l in data if l.split(",")[4] == "2")
        ok &= g("G6:head-census", len(data) == HEAD_ROWS and wins == HEAD_WIN and losses == HEAD_LOSS,
                "rows=%d WIN=%d LOSS=%d" % (len(data), wins, losses))
        present = [k for k in KEYPAIRS if any(l.split(",")[1] == KEYPAIRS[k][0] and l.split(",")[2] == KEYPAIRS[k][1] for l in data)]
        ok &= g("G6:freshness-absent", not present, "present=%s" % present)

    out = {"part": "ninth-cost k12 WIN row C++ scrutiny gate", "schema": "n11-ninthcost-k12win-cppgate-audit-v1",
           "rows": parsed, "gates": gates, "overall": "PASS" if ok else "FAIL"}
    with open(os.path.join(KIT, "output", "audit_gate.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True); f.write("\n")
    print("audit_gate:", out["overall"])
    for k, v in sorted(gates.items()):
        if v["status"] == "FAIL": print("FAIL", k, v["detail"])
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
