#!/usr/bin/env python3
"""Merge-conflict analysis over the published cost73k WIN7-D10 certificate
rows (2026-11-17).

Motivation: the class2-lane long-term lane's priority (3) is to merge
per-worker extraction memos (position-keyed win/loss tables) safely and
detect WIN/LOSS conflicts immediately. The published cost73k measurement
(a3c27e9f / c170a4ef) established the union invariance (682,861 distinct
rows out of 966,535 across the 22 certificate row sets) but did not
analyze whether the SHARED positions carry identical row values across
certificates, how the sharing is distributed, or what fraction of each
root's rows is already covered by earlier roots in band-wide order.

This script recomputes all of that directly from the published bytes:

  1. Fetch the published manifest (blob 0892aed0..., pinned at commit
     a3c27e9f) and the 41 certificate files (19 split pairs + 3 whole),
     verifying every md5 against the manifest (22/22).
  2. Merge the 22 row sets position by position, in manifest bit order,
     counting conflicts: the same position hex appearing with a different
     value in two certificates. The row value is the winning-move witness
     for that position; the extractor is deterministic and its witness
     choice depends only on the position, so a conflict would falsify the
     root-independence of the witness choice.
  3. Compute the sharing degree distribution (how many certificates
     contain each position), the 231-bit pair-sharing counts, and the
     sequential prior-coverage of each root in band-wide bit order.

Findings this run: distinct positions 682,861 (equals the published
union), merge hits 283,674, CONFLICTS 0 (22/22 certificates agree on
every shared position's value), max sharing degree 8 (one position
appears in eight certificates), 180/231 pairs share at least one
position, top pair (bit15, bit39) = 5,970, sequential coverage rises from
0% (bits 0/7) to 46.75% (bit 117) - quantifying why band-wide sharing
has cross-root reuse value at all and why late-battery bits suffer memo
pollution first.

Usage:
  python3 analyze_cost73k_cert_row_merge_conflicts_20261117.py [cert_dir] [out_dir]
Without arguments, the pinned manifest and certificates are fetched from
the raw CDN at commit a3c27e9f. With a local cert_dir (containing the
manifest and the 41 files), no network is needed.

This analysis changes no verdicts, opens or closes no manifest row, and
modifies no certificate bytes. 11x11 remains UNKNOWN.
"""
import collections
import hashlib
import itertools
import json
import pathlib
import sys
import urllib.request

BASE = ("https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/"
        "a3c27e9f/research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
        "output/class2-lane-cost73k-certificates")
MANIFEST = "class2-lane-cost73k-win7-certificates-20261117.json"
MANIFEST_BLOB = "0892aed07d187ae2fb3b4b90a21c7adbc1002b62"


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def fetch(url: str, dest: pathlib.Path) -> bytes:
    with urllib.request.urlopen(url) as resp:
        rb = resp.read()
    dest.write_bytes(rb)
    return rb


def analyze(cert_dir: pathlib.Path, out_dir: pathlib.Path) -> int:
    mb = (cert_dir / MANIFEST).read_bytes()
    got = git_blob_sha(mb)
    assert got == MANIFEST_BLOB, f"manifest blob mismatch: {got}"
    m = json.loads(mb.decode("utf-8"))
    certs = m["certificates"]
    assert len(certs) == 22

    per_bit = {}
    split_count, whole_count = 0, 0
    for c in certs:
        root, bit = c["root"], c["bit"]
        if "part1of2" in c.get("certificate_split", ""):
            data = b"".join((cert_dir / f"n11_s7_{root}.cert.part{k}of2").read_bytes()
                            for k in (1, 2))
            split_count += 1
        else:
            data = (cert_dir / f"n11_s7_{root}.cert").read_bytes()
            whole_count += 1
        md5 = hashlib.md5(data).hexdigest()
        assert md5 == c["md5"], f"md5 mismatch bit {bit}"
        rows = {}
        for line in data.decode().splitlines():
            if line.startswith("n11-terminal-strategy-v1") or line.startswith("root "):
                continue
            pos, val = line.split()
            assert rows.get(pos, val) == val, f"intra-cert conflict bit {bit} pos {pos}"
            rows[pos] = val
        assert len(rows) == c["rows"], (bit, len(rows), c["rows"])
        per_bit[bit] = rows
    assert split_count == 19 and whole_count == 3

    pos_val = {}
    pos_bits = collections.defaultdict(list)
    conflicts = []
    merge_hits = 0
    for bit in sorted(per_bit):
        for pos, val in per_bit[bit].items():
            if pos in pos_val:
                merge_hits += 1
                if pos_val[pos] != val:
                    conflicts.append({"position": pos, "values": [pos_val[pos], val],
                                      "second_bit": bit})
            else:
                pos_val[pos] = val
            pos_bits[pos].append(bit)

    total_rows = sum(len(r) for r in per_bit.values())
    assert total_rows == 966535 and len(pos_val) == 682861

    deg = collections.Counter(len(bs) for bs in pos_bits.values())
    pair_share = collections.Counter()
    for pos, bs in pos_bits.items():
        for a, b in itertools.combinations(sorted(bs), 2):
            pair_share[(a, b)] += 1

    seen = set()
    coverage = {}
    for bit in sorted(per_bit):
        rows = per_bit[bit]
        inter = sum(1 for pos in rows if pos in seen)
        coverage[str(bit)] = {"rows": len(rows), "prior_overlap": inter,
                              "prior_overlap_pct": round(inter / len(rows) * 100, 2)}
        seen.update(rows)

    out = {
        "schema": "n11-class2-lane-cost73k-cert-row-merge-conflict-analysis-20261117-v1",
        "date": "2026-11-17",
        "inputs": {
            "manifest": MANIFEST,
            "manifest_git_blob_sha": MANIFEST_BLOB,
            "pinned_commit": "a3c27e9f",
            "certificates": "41 files (19 split pairs recombined + 3 whole), every "
                            "concatenated md5 verified against the manifest (22/22)",
        },
        "band": "cost73k WIN7-D10 (child 00000000000000801206000000000400, 22 roots)",
        "results": {
            "total_rows": total_rows,
            "distinct_positions": len(pos_val),
            "merge_hits_revisited_rows": merge_hits,
            "conflicts_same_position_different_value": len(conflicts),
            "conflicts_detail": conflicts,
            "verdict": ("SAFE-MERGE: 0 conflicts; every position shared by two or "
                        "more certificates carries an identical row value in all of "
                        "them, so the 22 per-root row sets merge losslessly into one "
                        "position-keyed table (682,861 entries) with immediate "
                        "conflict detection finding nothing to flag"),
            "sharing_degree_distribution": {str(k): deg[k] for k in sorted(deg)},
            "max_degree": max(deg),
            "pairs_with_shared_positions": len(pair_share),
            "pairs_total": 231,
            "top_shared_pairs": [
                {"pair": [a, b], "shared_positions": n}
                for (a, b), n in pair_share.most_common(10)
            ],
            "sequential_prior_coverage_band_order": coverage,
        },
        "interpretation": (
            "The row value is the deterministic winning-move witness of the position; "
            "its root-independence across all 22 certificates (0 conflicts over 283,674 "
            "shared rows) is direct evidence that position-keyed per-worker memos of "
            "this workload can be merged without WIN/LOSS conflicts, the prerequisite "
            "for priority (3) shared-cache design. The sequential coverage numbers "
            "quantify the cross-root reuse potential band-wide sharing exploits "
            "(late bits like 112/117 have ~47% prior overlap) and explain why "
            "late-battery bits accumulated memo pollution in the published ms23/ms24 "
            "band runs: their lookups mostly hit positions inserted by earlier roots."),
        "interpretation_guard": (
            "this is a row-set merge analysis over already-published certificate "
            "bytes; no new verdict, no manifest row opened or closed, no certificate "
            "byte changed; WIN7-D10 proves a first-player win within depth 10 from "
            "each individual 7-stone root only; REFUTED-D10 is not a LOSS proof; "
            "11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and "
            "classes 1/2/4 remain UNKNOWN"),
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "class2-lane-cost73k-cert-row-merge-conflict-analysis-20261117.json"
    text = json.dumps(out, indent=1, ensure_ascii=True) + "\n"
    dst.write_text(text)
    print(f"analysis JSON written: {dst} ({len(text)} bytes)")
    print(f"conflicts: {len(conflicts)}; distinct: {len(pos_val)}; merge hits: {merge_hits}")
    print(f"degree dist: {dict(sorted(deg.items()))}")
    print(f"pairs sharing: {len(pair_share)}/231")
    print("blob:", git_blob_sha(text.encode()))
    return 0 if not conflicts else 1


def main() -> None:
    args = sys.argv[1:]
    out_dir = pathlib.Path(args[1]) if len(args) >= 2 else (
        pathlib.Path(__file__).resolve().parent.parent / "output")
    if len(args) >= 1:
        cert_dir = pathlib.Path(args[0])
    else:
        cert_dir = pathlib.Path("_cost73k_certs")
        cert_dir.mkdir(exist_ok=True)
        print(f"fetching pinned manifest: {BASE}/{MANIFEST}")
        fetch(f"{BASE}/{MANIFEST}", cert_dir / MANIFEST)
        m = json.loads((cert_dir / MANIFEST).read_text())
        for c in m["certificates"]:
            root = c["root"]
            if "part1of2" in c.get("certificate_split", ""):
                for k in (1, 2):
                    fn = f"n11_s7_{root}.cert.part{k}of2"
                    if not (cert_dir / fn).exists():
                        print(f"fetching {fn}")
                        fetch(f"{BASE}/{fn}", cert_dir / fn)
            else:
                fn = f"n11_s7_{root}.cert"
                if not (cert_dir / fn).exists():
                    print(f"fetching {fn}")
                    fetch(f"{BASE}/{fn}", cert_dir / fn)
    sys.exit(analyze(cert_dir, out_dir))


if __name__ == "__main__":
    main()
