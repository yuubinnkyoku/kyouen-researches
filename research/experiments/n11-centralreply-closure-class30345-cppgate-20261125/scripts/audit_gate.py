#!/usr/bin/env python3
"""Part EQ fail-closed machine audit for the C++ scrutiny gate run
(closure class 30345, b38-win-18 rows).

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
    "ai002": [
        "15000000",
        "74,15000000,1,3552766",
        "e8a5168c154881a71530960ff6121fd86e48544f8906f7d97c94961d2a74192b",
        "b38 kit input/ai002.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)"
    ],
    "ai003": [
        "15000000",
        "79,15000000,1,5682652",
        "255245d76a1e2fdc48bf8553088a55548b81b78835a48a54e66fa74b748ad5b2",
        "b38 kit input/ai003.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)"
    ],
    "ai005": [
        "15000000",
        "87,15000000,1,11770537",
        "296a5d5b07375b3980c5f6b5d00202936dca6eb8d005626b3047169f702d3f5f",
        "b38 kit input/ai005.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)"
    ],
    "ai006": [
        "15000000",
        "88,15000000,1,8819998",
        "3816b998e420f5e3fd5473f4d9aa053e2ee088326fda572064777c38692f60ae",
        "b38 kit input/ai006.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)"
    ],
    "ai010": [
        "15000000",
        "78,15000000,1,13066796",
        "48ed44dbca4a270c655495f40a820cdc2cf035e714807960c275d6f114b15182",
        "b38 kit input/ai010.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)"
    ],
    "ai013": [
        "15000000",
        "78,15000000,1,10255279",
        "cbf3324336e11c5e31a7ed635869468cf598d02b028e6e7ad544916e1ebaf015",
        "b38 kit input/ai013.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)"
    ],
    "ai014": [
        "15000000",
        "79,15000000,1,14969659",
        "a408bbe7a29e8235d3e98b5acd86c8205833afad005fd5f7938bdc9b456d41e6",
        "b38 kit input/ai014.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)"
    ],
    "ai017": [
        "15000000",
        "81,15000000,1,8468415",
        "62a7bf59e5e5be2cae625d1a735e675601a4391ff58fc4af1a9e171d161b5fff",
        "b38 kit input/ai017.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)"
    ],
    "ai023": [
        "15000000",
        "85,15000000,1,13676098",
        "c59090a516f05a45aafc4c3a01fe2835294f24e95ce7f241fa3c00426b603dc9",
        "b38 kit input/ai023.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)"
    ],
    "ai028": [
        "15000000",
        "76,15000000,1,4892185",
        "dfc986475de9bb381991b24bf384fa318feb374f4e2a06df267a0c41532b3541",
        "b38 kit input/ai028.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)"
    ],
    "ai034": [
        "15000000",
        "74,15000000,1,3087464",
        "4d235cf5723f4834204b8f799dd4251ae51f1c219e8d1ce6d3c7ade694b8231c",
        "b38 kit input/ai034.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)"
    ],
    "ai035": [
        "15000000",
        "84,15000000,1,4227036",
        "636d9063538fa96cf21c2aaa58962baaa4a7e2b3895a3b1d70a8dae05cad724a",
        "b38 kit input/ai035.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)"
    ],
    "ai036": [
        "15000000",
        "82,15000000,1,8137160",
        "41fc3ae0c90940bdc1e47699c65258f5d5934e00d0c6abbd63cef1f2ca66e240",
        "b38 kit input/ai036.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)"
    ],
    "ai039": [
        "15000000",
        "87,15000000,1,13065437",
        "399e3f0ec2b00660910d4a41f16d1527766c3272be043f98c3c3398d579a7e9d",
        "b38 kit input/ai039.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)"
    ],
    "ai043": [
        "15000000",
        "74,15000000,1,3897909",
        "9065866c54fc761d7075f488eee0f7eedae4c0136f38ff1074baeafa355fefbc",
        "b38 kit input/ai043.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)"
    ],
    "ai046": [
        "15000000",
        "80,15000000,1,5256793",
        "06bc4683312e2f7ea24eed89b02bdb70e59ea71373f78a34384150c4ca35350c",
        "b38 kit input/ai046.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)"
    ],
    "ai047": [
        "15000000",
        "82,15000000,1,2946085",
        "33ac19f7a3369eefbe80dd59ed6f7a6c7bba89433e87e03d7f68ed5afea9828d",
        "b38 kit input/ai047.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)"
    ],
    "ai049": [
        "15000000",
        "72,15000000,1,832069",
        "6856e70f9b993b50c811a98280b81bcb119e75959b1189203dd81df68b5a4187",
        "b38 kit input/ai049.input.csv (byte-clone; batch-keys-b38 SSOT 29807104)"
    ],
    "anchor-af039": [
        "30000000",
        "89,30000000,2,19234232",
        "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691",
        "EO kit input/anchor-af039.input.csv (byte-clone; == EN kit input)"
    ],
    "anchor-aj001": [
        "30000000",
        "84,30000000,2,5156075",
        "2f6daea5ca3b3fe6b7713c8d450af3f3c9f203acacb8a1340255d8e8f656496c",
        "EO kit input/anchor-aj001.input.csv (byte-clone; == EN kit input)"
    ],
    "anchor-at2m": [
        "2000000",
        "98,2000000,0,2000000",
        "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
        "EO kit input/anchor-at2m.input.csv (byte-clone; == EN kit input)"
    ]
}

# published raw provenance of the expected (budget,result,nodes) per key
RAW_PROV = {
    "ai002": "b38 kit output/raw/ai002.p1.out (replay...,15000000,1,3552766,...); two-pass node-exact vs ai002.p2",
    "ai003": "b38 kit output/raw/ai003.p1.out (replay...,15000000,1,5682652,...); two-pass node-exact vs ai003.p2",
    "ai005": "b38 kit output/raw/ai005.p1.out (replay...,15000000,1,11770537,...); two-pass node-exact vs ai005.p2",
    "ai006": "b38 kit output/raw/ai006.p1.out (replay...,15000000,1,8819998,...); two-pass node-exact vs ai006.p2",
    "ai010": "b38 kit output/raw/ai010.p1.out (replay...,15000000,1,13066796,...); two-pass node-exact vs ai010.p2",
    "ai013": "b38 kit output/raw/ai013.p1.out (replay...,15000000,1,10255279,...); two-pass node-exact vs ai013.p2",
    "ai014": "b38 kit output/raw/ai014.p1.out (replay...,15000000,1,14969659,...); two-pass node-exact vs ai014.p2",
    "ai017": "b38 kit output/raw/ai017.p1.out (replay...,15000000,1,8468415,...); two-pass node-exact vs ai017.p2",
    "ai023": "b38 kit output/raw/ai023.p1.out (replay...,15000000,1,13676098,...); two-pass node-exact vs ai023.p2",
    "ai028": "b38 kit output/raw/ai028.p1.out (replay...,15000000,1,4892185,...); two-pass node-exact vs ai028.p2",
    "ai034": "b38 kit output/raw/ai034.p1.out (replay...,15000000,1,3087464,...); two-pass node-exact vs ai034.p2",
    "ai035": "b38 kit output/raw/ai035.p1.out (replay...,15000000,1,4227036,...); two-pass node-exact vs ai035.p2",
    "ai036": "b38 kit output/raw/ai036.p1.out (replay...,15000000,1,8137160,...); two-pass node-exact vs ai036.p2",
    "ai039": "b38 kit output/raw/ai039.p1.out (replay...,15000000,1,13065437,...); two-pass node-exact vs ai039.p2",
    "ai043": "b38 kit output/raw/ai043.p1.out (replay...,15000000,1,3897909,...); two-pass node-exact vs ai043.p2",
    "ai046": "b38 kit output/raw/ai046.p1.out (replay...,15000000,1,5256793,...); two-pass node-exact vs ai046.p2",
    "ai047": "b38 kit output/raw/ai047.p1.out (replay...,15000000,1,2946085,...); two-pass node-exact vs ai047.p2",
    "ai049": "b38 kit output/raw/ai049.p1.out (replay...,15000000,1,832069,...); two-pass node-exact vs ai049.p2",
    "anchor-af039": "EO kit output/raw/anchor-af039.p1.out (30000000,2,19234232); canonical cache row, budget-ceiling baseline",
    "anchor-aj001": "EO kit output/raw/anchor-aj001.p1.out (30000000,2,5156075); budget-ceiling baseline",
    "anchor-at2m": "EO kit output/raw/anchor-at2m.p1.out (2000000,0,2000000); budget-ceiling baseline; EO raws == EN raws (published observation)"
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
    out = {"part": "EQ", "schema": "n11-centralreply-cppgate-30345win18-audit-v1",
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
