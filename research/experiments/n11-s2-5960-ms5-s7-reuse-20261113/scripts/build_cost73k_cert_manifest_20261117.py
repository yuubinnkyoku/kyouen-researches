#!/usr/bin/env python3
"""Build the cost73k certificate manifest and split large certificates.

Adapted from build_cost73j_cert_manifest_20261117.py (73j lane): whole-file
threshold 1,200,000 bytes; larger certificates split at a line boundary near
the midpoint into .cert.part1of2 / .cert.part2of2 with README-split-bitK.md
per bit; every split is verified by reassembling with cat and comparing md5
against the original. Writes output/class2-lane-cost73k-certificates/
class2-lane-cost73k-win7-certificates-20261117.json.
"""
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
WORK = HERE / "output" / "class2-lane-cost73k-certificates"
THRESHOLD = 1_200_000
CHILD = "00000000000000801206000000000400"
CLAIM_V2_BLOB = "2150277f95fa202837d1cda10b390ee2bb54761b"
CLAIM_V1_BLOB = "a24d3557ef23a279cc08c2d578e420f676f28f05"

# ------------------------------------------------------------------ D4 canon
def images(mask):
    result = [0] * 8
    for p in range(121):
        if mask >> p & 1:
            x, y = p % 11, p // 11
            coords = ((x, y), (y, 10 - x), (10 - x, 10 - y), (10 - y, x),
                      (10 - x, y), (x, 10 - y), (y, x), (10 - y, 10 - x))
            for i, (a, b) in enumerate(coords):
                result[i] |= 1 << (11 * b + a)
    return result


IMG = [images(1 << p) for p in range(121)]


def canon(mask):
    best = None
    for r in range(8):
        v = 0
        for p in range(121):
            if mask >> p & 1:
                v |= IMG[p][r]
        if best is None or v < best:
            best = v
    return best


stats = json.loads((WORK / "stats.json").read_text())
certs = []
total_rows = total_nodes = total_bytes = 0
for b_str, v in sorted(stats.items(), key=lambda kv: int(kv[0])):
    b = int(b_str)
    root = v["root"]
    cert = WORK / f"bit{b}.cert"
    data = cert.read_bytes()
    md5 = hashlib.md5(data).hexdigest()
    sha256 = hashlib.sha256(data).hexdigest()
    assert md5 == v["md5"] and len(data) == v["size"]
    # re-verify the consumed union from the saved verification artifacts
    keys = WORK / f"bit{b}-certkeys.txt"
    cons = WORK / f"bit{b}-consumed-sorted.txt"
    miss = subprocess.run(["comm", "-23", str(keys), str(cons)],
                          capture_output=True, text=True).stdout
    extra = subprocess.run(["comm", "-13", str(keys), str(cons)],
                           capture_output=True, text=True).stdout
    assert miss == "" and extra == "", b
    nk = sum(1 for _ in keys.open())
    nc = sum(1 for _ in cons.open())
    assert nk == nc == v["rows"], (b, nk, nc, v["rows"])
    # terminal stone range from the sub-root verifier stats
    lo, hi = 121, 0
    nsub = 0
    for line in (WORK / f"bit{b}-subroots.jsonl").read_text().splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        for m, s in d["stats"].items():
            nsub += 1
            a, c = s["range"]
            lo, hi = min(lo, a), max(hi, c)
    assert lo >= 13 and hi <= 17 and nsub == v["moves"], (b, nsub)
    d4 = canon(int(root, 16))
    raw_is_canon = (d4 == int(root, 16))
    entry = {
        "bit": b,
        "root": root,
        "verdict": "WIN7",
        "depth": 10,
        "rows": v["rows"],
        "extraction_nodes": v["nodes"],
        "fbt_drops": v["fbt_drops"],
        "fatal": None,
        "subroots": v["moves"],
        "subroots_pass": v["moves"],
        "union_missing": 0,
        "union_extra": 0,
        "terminal_stone_range": [lo, hi],
        "loser_mobility": v["moves"],
        "file": f"n11_s7_{root}.cert",
        "md5": md5,
        "sha256": sha256,
        "d4_canon_root": f"{d4:032x}",
        "raw_is_canon": raw_is_canon,
    }
    if len(data) > THRESHOLD:
        half = len(data) // 2
        cut = data.rfind(b"\n", 0, half) + 1
        assert 0 < cut < len(data)
        p1 = data[:cut]
        p2 = data[cut:]
        assert p1 + p2 == data
        (WORK / f"n11_s7_{root}.cert.part1of2").write_bytes(p1)
        (WORK / f"n11_s7_{root}.cert.part2of2").write_bytes(p2)
        cat = subprocess.run(["cat", str(WORK / f"n11_s7_{root}.cert.part1of2"),
                              str(WORK / f"n11_s7_{root}.cert.part2of2")],
                             capture_output=True).stdout
        assert hashlib.md5(cat).hexdigest() == md5 and cat == data
        entry["certificate_split"] = (
            f"{len(data)} bytes exceeds the {THRESHOLD}-byte whole-file "
            f"threshold; pushed as .cert.part1of2 ({len(p1)} bytes) + "
            f".cert.part2of2 ({len(p2)} bytes), recombine with cat (see "
            f"README-split-bit{b}.md), md5 of concatenation below")
        entry["split_cut_byte"] = cut
        entry["storage"] = f"split part1of2/part2of2 + README-split-bit{b}.md"
        readme = (
            f"# split certificate bit {b} (cost-73k)\n\n"
            f"root `{root}`\n\n"
            f"`n11_s7_{root}.cert` is {len(data)} bytes and is published as "
            f"two parts:\n\n```\n"
            f"cat n11_s7_{root}.cert.part1of2 "
            f"n11_s7_{root}.cert.part2of2 > n11_s7_{root}.cert\n"
            f"md5sum n11_s7_{root}.cert   # {md5}\n```\n\n"
            f"The split is at a line boundary (byte {cut}); both parts are "
            f"byte-exact halves of the certificate.\n")
        (WORK / f"README-split-bit{b}.md").write_text(readme)
        print(f"bit {b}: split {len(p1)} + {len(p2)}")
    else:
        entry["certificate_split"] = (
            f"{len(data)} bytes within the {THRESHOLD}-byte whole-file "
            f"threshold; published whole")
        entry["split_cut_byte"] = None
        entry["storage"] = "whole file"
        print(f"bit {b}: whole ({len(data)})")
    certs.append(entry)
    total_rows += v["rows"]
    total_nodes += v["nodes"]
    total_bytes += len(data)

manifest = {
    "schema": "n11-class2-lane-cost73k-win7-certificates-20261117-v1",
    "date": "2026-11-17",
    "s5_parent_hex": "00000000000000403800000008000000",
    "s6_child_hex": CHILD,
    "s6_s7_edge_cost": 73,
    "method": (
        "blind extraction with class4_child1_cert_extractor_exact.ts "
        "(repo-verbatim, engine v15 inlined; FBS=1<<20, empty kill table via "
        "cert_driver73k.ts import; rows deduplicated and sorted before "
        "write), fbt_drops=0 on all twenty-two, no fatal, no capped per-move; "
        "independent verification with verify_bit7_win7_cert.ts (Bareiss 4x4, "
        "engine-free), orchestrated by verify_cost73k_one.sh: root-check "
        "stones=7 and loser mobility equals the independent legal_candidates"
        ".py enumeration on the RAW root, all sub-roots PASS on every root, "
        "terminal stone range within [13,17] on every sub-root, consumed-"
        "winner-state union vs certificate row set 0 missing / 0 extra in "
        "both directions on every root (re-verified from the saved "
        "certkeys/consumed artifacts when building this manifest); "
        "determinism: fresh-process re-extraction byte-identical (md5) on "
        "six of the twenty-two bits [0,7,11,15,35,117], including the "
        "heaviest bit 117 (2,150,734 bytes, 59,587 rows, reproduced "
        "98352c2e560977e20c14584d59ffa56b byte-identically) and bit 0 "
        "(1,936,240 bytes, 53,456 rows, reproduced "
        "0d1060c8365fd8214e7bb68c2cb11155 byte-identically); the same "
        "blind-extraction and engine-free verification pipeline as the "
        "69j/66j/71e/72d/73j certificate lanes; the sweep the certificates "
        "come from passed all its planned controls: 9/9 pilot controls "
        "exact (loss=false at exactly 3,402 nodes), determinism reruns of "
        "batches 1 and 7 field-identical on every non-ms field, independent "
        "v15 cross-engine re-check 25/25 WIN agreement (pilots 5,949 exact, "
        "0 capped, v15 node total 116,892,833), 7/7 census-v7 confirmation "
        "transfers re-run fresh and matching the predicted verdicts (3 "
        "WIN7-D10, 4 REFUTED-D10), and full per-bit agreement with the "
        "concurrent session's independently executed sweep (73/73 bits, "
        "class2-lane-cost73k-cross-lane-agreement-20261117.json); loser "
        "defenses are enumerated on the RAW child|bit root (the certificate "
        "root), never on its D4 canonical image"),
    "driver_note": (
        "cert_driver73k.ts is archived in scripts/ (duplicated from "
        "cert_driver73j.ts, argv-driven, defense list on stdin, "
        "String.fromCharCode(10) newline convention); extract73k_all_"
        "20261117.sh is the per-bit extraction wrapper (root=child|1<<bit "
        "fed to legal_candidates.py on stdin); verify_cost73k_one.sh is "
        "adapted from verify_cost73j_one.sh (paths only); the extraction "
        "pipeline and the certificate file format are identical to the "
        "69j/66j/71e/72d/73j lanes"),
    "totals": {
        "certificates": 22,
        "rows": total_rows,
        "extraction_nodes": total_nodes,
        "published_bytes": total_bytes,
        "fbt_drops_total": 0,
        "capped_per_move_total": 0,
    },
    "basis": (
        "cost73k claim v2 (class2-lane-cost73k-inflight-20261117.json, git "
        "blob " + CLAIM_V2_BLOB + ", published with the regenerated raw "
        "batches, the raw sweep audit and the cross-lane agreement record; "
        "claim v1 git blob " + CLAIM_V1_BLOB + ", commit a0987c37): fresh "
        "v17 73-bit depth-10 sweep of census-v7 rank-1 child, 25 WIN7-D10 "
        "bits [0,7,11,14,15,26,35,39,41,44,55,58,62,73,76,87,89,94,95,97,"
        "98,103,105,112,117] + 48 REFUTED-D10, 0 capped (128,861,941 "
        "candidate nodes); this manifest covers the 22 sweep WIN roots; the "
        "3 confirmation WIN roots are already certified by the published "
        "cost73j bit 110, cost73i bit 110 and cost69j bit 110 certificates "
        "(bits 14, 26 and 55 of this child); raw sweep audit "
        "class2-lane-cost73k-raw-sweep-audit-20261117.json, git blob "
        "85f4f73fa061c02612f5d24320d668e12468ca4e; cross-lane agreement "
        "class2-lane-cost73k-cross-lane-agreement-20261117.json, git blob "
        "e41143eb0eb79e7d7412596dbb54f1a524f9463c"),
    "certificates": certs,
    "unknown_status": (
        "11x11 empty board: UNKNOWN. These certificates prove only "
        "WIN7-within-depth-10 for the individual 7-stone roots of this "
        "child. REFUTED-D10 is not a LOSS proof; no manifest row is closed; "
        "the receipt fold stays pending behind the 76c/66i/66j/69j/71e/72d/73i "
        "folds"),
}
out = WORK / "class2-lane-cost73k-win7-certificates-20261117.json"
out.write_text(json.dumps(manifest, indent=1, ensure_ascii=True) + "\n")
print(f"wrote {out} ({out.stat().st_size} bytes)")
print("totals:", manifest["totals"])
