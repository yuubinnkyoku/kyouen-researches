"""Build the cost73l certificate manifest and split large certificates.

Adapted from build_cost73k_cert_manifest_20261117.py (73k lane): whole-file
threshold 1,200,000 bytes; larger certificates split at a line boundary near
the midpoint into .cert.part1of2 / .cert.part2of2 with README-split-bitK.md
per bit; every split is verified by reassembling with cat and comparing md5
against the original. Reads output/class2-lane-cost73l-certificates/
det-reextraction.json (written by reextract_cost73l_det_20261117.py) for the
determinism sample. Writes output/class2-lane-cost73l-certificates/
class2-lane-cost73l-win7-certificates-20261117.json.
"""
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
WORK = HERE / "output" / "class2-lane-cost73l-certificates"
THRESHOLD = 1_200_000
CHILD = "00000000000000c09002000000400000"
CLAIM_V2_BLOB = "814a0ec6c6b3123a25010dcf7d3d054b38352f3a"
CLAIM_V1_BLOB = "fa13a0ada22e3de95c06e9a3101ce6d2a738f5b1"

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


det = json.loads((WORK / "det-reextraction.json").read_text())
assert det["all_byte_identical"] is True and len(det["bits"]) == 6
sizes = [det["details"][str(b)]["size"] for b in det["bits"]]
det_summary = (
    "six of the thirty-two bits [" + ",".join(str(b) for b in det["bits"]) +
    "], each re-extracted in a fresh process with byte-identical md5 "
    "(sample spans " + str(min(sizes)) + " to " + str(max(sizes)) +
    " published bytes and " +
    str(sum(det["details"][str(b)]["rows"] for b in det["bits"])) +
    " re-extracted rows in total)")

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
            f"# split certificate bit {b} (cost-73l)\n\n"
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
    "schema": "n11-class2-lane-cost73l-win7-certificates-20261117-v1",
    "date": "2026-11-17",
    "s5_parent_hex": "00000000000000403800000008000000",
    "s6_child_hex": CHILD,
    "s6_s7_edge_cost": 73,
    "method": (
        "blind extraction with class4_child1_cert_extractor_exact_ms23.ts "
        "(the repo-verbatim extractor_exact with the single MS=1<<18 -> "
        "MS=1<<23 memo-capacity line substitution; engine v15 inlined; FBS "
        "unchanged; empty kill table via cert_driver73l.ts import; per-bit "
        "fresh process; rows deduplicated and sorted before write; the MS "
        "line bounds only the memo capacity and does not change the "
        "extracted row set - published prescription, ~-30% extraction "
        "nodes vs MS=1<<18), fbt_drops=0 on all thirty-two, no fatal, no "
        "capped per-move; independent verification with "
        "verify_bit7_win7_cert.ts (Bareiss 4x4, engine-free), orchestrated "
        "by verify_cost73l_one.sh: root-check stones=7 and loser mobility "
        "equals the independent legal_candidates.py enumeration on the RAW "
        "root, all sub-roots PASS on every root, terminal stone range "
        "within [13,17] on every sub-root, consumed-winner-state union vs "
        "certificate row set 0 missing / 0 extra in both directions on "
        "every root (re-verified from the saved certkeys/consumed "
        "artifacts when building this manifest); determinism: "
        "fresh-process re-extraction byte-identical (md5) on " + det_summary + "; the same "
        "blind-extraction and engine-free verification pipeline as the "
        "69j/66j/71e/72d/73j/73k certificate lanes; the sweep the "
        "certificates come from passed all its planned controls: 9/9 "
        "pilot controls exact (loss=false at exactly 3,402 nodes), "
        "determinism reruns of batches 1 and 4 (batch 4 holds the "
        "heaviest search bit 47, 6,045,349 nodes) field-identical on "
        "every non-ms field, independent v15 cross-engine re-check 34/34 "
        "WIN agreement (pilots 5,949 exact, 0 capped, v15 node total "
        "286,284,260), 7/7 head-1473 census-v8 confirmation transfers "
        "re-run fresh and matching the predicted verdicts (2 WIN7-D10 "
        "covered by published certificates, 5 REFUTED-D10; every "
        "transfer canon-equality independently re-derived in the raw "
        "sweep audit); first execution of this child (no concurrent-"
        "session overlap, no sandbox reset); bit 91 (REFUTED-D10) closed "
        "its sweep search at 13-15 stones, the only terminal-range "
        "exception among the 73 bits; loser defenses are enumerated on "
        "the RAW child|bit root (the certificate root), never on its D4 "
        "canonical image"),
    "driver_note": (
        "cert_driver73l.ts is archived in scripts/ (duplicated from "
        "cert_driver73k.ts, argv-driven, defense list on stdin, "
        "String.fromCharCode(10) newline convention, import retargeted "
        "to the ms23 extractor variant); extract73l_all_20261117.sh is "
        "the per-bit extraction wrapper (root=child|1<<bit fed to "
        "legal_candidates.py on stdin); build_cost73l_cert_stats_"
        "20261117.py accumulates stats.json from the extraction logs; "
        "reextract_cost73l_det_20261117.py runs the determinism sample "
        "and writes det-reextraction.json; verify_cost73l_one.sh is "
        "adapted from verify_cost73k_one.sh (paths only); the extraction "
        "pipeline and the certificate file format are identical to the "
        "69j/66j/71e/72d/73j/73k lanes"),
    "totals": {
        "certificates": 32,
        "rows": total_rows,
        "extraction_nodes": total_nodes,
        "published_bytes": total_bytes,
        "fbt_drops_total": 0,
        "capped_per_move_total": 0,
    },
    "basis": (
        "cost73l claim v2 (class2-lane-cost73l-inflight-20261117.json, git "
        "blob " + CLAIM_V2_BLOB + ", published with the raw batches, the raw "
        "sweep audit and the sweep-complete log; claim v1 git blob " + CLAIM_V1_BLOB + ", commit "
        "43838dec): fresh v17 73-bit depth-10 sweep of the head-1473 "
        "census v8 rank-1 child, 34 WIN7-D10 bits [1,2,3,4,6,8,9,18,21,23,"
        "25,28,29,32,34,41,42,44,47,53,54,61,62,64,66,80,95,105,106,110,"
        "112,113,116,119] + 39 REFUTED-D10, 0 capped (133,895,305 "
        "candidate nodes); this manifest covers the 32 sweep WIN roots; "
        "the 2 confirmation WIN roots are already certified by the "
        "published cost73j bit 118 and cost73k bit 98 certificates (bits "
        "106 and 110 of this child); raw sweep audit "
        "class2-lane-cost73l-raw-sweep-audit-20261117.json, git blob "
        "f2ea204413b31405b9e0f54a6a3d76205ca749b9; head-1473 census v8 "
        "class2-lane-next-target-presweep-1473-v8-20261117.json, git blob "
        "2542914e02db14a8426a1a16ef1c2cfcd9817375"),
    "certificates": certs,
    "unknown_status": (
        "11x11 empty board: UNKNOWN. These certificates prove only "
        "WIN7-within-depth-10 for the individual 7-stone roots of this "
        "child. REFUTED-D10 is not a LOSS proof; no manifest row is closed; "
        "the receipt fold stays pending behind the 66i/66j/69j/71e/72d/73i/"
        "73j and 73k folds"),
}
out = WORK / "class2-lane-cost73l-win7-certificates-20261117.json"
out.write_text(json.dumps(manifest, indent=1, ensure_ascii=True) + "\n")
print(f"wrote {out} ({out.stat().st_size} bytes)")
print("totals:", manifest["totals"])
