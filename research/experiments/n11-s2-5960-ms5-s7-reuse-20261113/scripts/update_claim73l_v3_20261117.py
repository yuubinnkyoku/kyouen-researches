#!/usr/bin/env python3
# claim v3 updater for class2-lane cost73l (2026-11-17)
# v2 -> v3: in-flight claim advanced to certificates-complete. The 32 sweep
# WIN7-D10 roots are published as blind-extracted, engine-free verified
# WIN7-D10 certificates (30 split part1of2/part2of2 + 2 whole files, one
# file per commit, plus the certificate manifest, stats, det-reextraction,
# 30 README-split docs, 32 rootcheck/subroots sidecars, the verify worker
# script and the extraction scripts).
# BigInt independent third-implementation re-verification: planned next.
import hashlib, json, sys, pathlib

V2_BLOB_SHA = "814a0ec6c6b3123a25010dcf7d3d054b38352f3a"
MANIFEST_BLOB = "6e0a94aba212ba54bb5329fbea4643c9dcdb1ec4"
BAND_FIRST = "3a442e0f3e7441a690f4df0b3d01acd1875e48f3"
BAND_LAST = "a53e768ad1410f0207ecc33076c2e8060abff8e6"

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def main() -> None:
    src = sys.argv[1]  # published claim v2 json (must match V2_BLOB_SHA)
    dst = sys.argv[2]  # claim v3 json output
    raw = pathlib.Path(src).read_bytes()
    sha = git_blob_sha(raw)
    if sha != V2_BLOB_SHA:
        sys.exit(f"FATAL: input is not the published claim v2 blob (got {sha})")
    d = json.loads(raw.decode("utf-8"))
    assert d["schema"] == "n11-class2-lane-cost73l-inflight-20261117-v2"

    d["schema"] = "n11-class2-lane-cost73l-inflight-20261117-v3"
    d["last_updated"] = "2026-11-17"
    d["status"] = (
        "claim v3: certificates complete; the 32 sweep WIN7-D10 roots of the "
        "census-v7 rank-1 child are published as blind-extracted, "
        "engine-free verified WIN7-D10 certificates: 32 certificates, "
        "1,693,203 rows, 424,657,112 extraction nodes, 61,171,191 published "
        "bytes, fbt_drops 0, no capped per-move; 30 certificates split at a "
        "line boundary into .cert.part1of2/.part2of2 (whole-file threshold "
        "1,200,000 bytes) + 2 whole files (bits 41, 61), pushed one file per "
        "commit (band commits " + BAND_FIRST[:8] + ".." + BAND_LAST[:8] +
        "); every landed certificate and sidecar file was verified "
        "byte-exact against the local extraction via git blob sha, "
        "160/160 (159 files in the certificate output directory + the "
        "verify worker script); certificate manifest "
        "class2-lane-cost73l-win7-certificates-20261117.json (git blob " +
        MANIFEST_BLOB + ") published together with stats.json, "
        "det-reextraction.json, 30 README-split-bit{N}.md recombination "
        "docs, 32 per-bit rootcheck.json + subroots.jsonl verification "
        "sidecars and scripts/verify_cost73l_worker.sh in the three "
        "bundle commits ending " + BAND_LAST[:8] + "; the seven extraction "
        "and verification scripts (class4_child1_cert_extractor_exact_ms23."
        "ts, cert_driver73l.ts, extract73l_all_20261117.sh, "
        "verify_cost73l_one.sh, build_cost73l_cert_stats_20261117.py, "
        "reextract_cost73l_det_20261117.py, build_cost73l_cert_manifest_"
        "20261117.py) were published earlier in separate archive commits "
        "and re-verified by blob sha; verification per verify_cost73l_one."
        "sh with verify_bit7_win7_cert.ts (Bareiss 4x4, engine-free): "
        "root-check stones=7 and loser mobility equal to the independent "
        "legal_candidates.py enumeration on the RAW root on all 32, all "
        "sub-roots PASS on every root (32/32 PASS), terminal stone range "
        "within [13,17] on every sub-root, consumed-winner-state union vs "
        "certificate row set 0 missing / 0 extra in both directions on "
        "all 32 (re-verified from the saved certkeys/consumed artifacts "
        "when building the manifest); determinism: fresh-process "
        "re-extraction byte-identical (md5) on six of the thirty-two bits "
        "[1,9,47,61,64,116], including the heaviest bit 116 "
        "(22,587,921 extraction nodes, 73,217 rows, 2,638,690 whole-file "
        "bytes, reproduced 1dec0c4b094e6a4b64fbb11aecf37164 "
        "byte-identically); cross-environment determinism: the execution "
        "environment was wiped mid-extraction, the workspace was rebuilt "
        "from the repo tarball and bits 61 (28,229 rows), 1 and 9 were "
        "re-extracted to byte-identical md5s (1391b4c4faf8152ab706637280"
        "c0014c, 114b255f4bf3b4d1dfcb3f8cfe80795f, 807c0aedd1edfd8c426635"
        "4a483f6bfe) matching the pre-wipe extraction on a different "
        "sandbox instance; the 2 confirmation WIN roots (bits 106, 110) "
        "are already covered by the published cost73j bit 118 and cost73k "
        "bit 98 certificates; a third-implementation BigInt independent "
        "re-verification of this band (as done for the 69j/71e/72d/73j/73k "
        "bands) is planned as the next step; the receipt fold stays "
        "pending behind the 66i/66j/69j/71e/72d/73i/73j/73k folds; no "
        "manifest row is closed by this claim; 11x11 UNKNOWN"
    )
    d["certificates"] = {
        "status": (
            "complete: 32 WIN7-D10 certificates published (30 split "
            "part1of2/part2of2 + 2 whole files, one file per commit, band "
            "commits " + BAND_FIRST[:8] + ".." + BAND_LAST[:8] + "), "
            "manifest class2-lane-cost73l-win7-certificates-20261117.json "
            "(git blob " + MANIFEST_BLOB + "); the 2 confirmation WIN "
            "roots (bits 106, 110) are covered by the published cost73j "
            "bit 118 and cost73k bit 98 certificates; BigInt independent "
            "third-implementation re-verification planned next"
        ),
        "driver": (
            "cert_driver73l.ts (73k driver duplicated, argv-driven, "
            "String.fromCharCode(10) newline convention) with "
            "class4_child1_cert_extractor_exact_ms23.ts (repo-verbatim "
            "extractor_exact with the single MS=1<<18 -> MS=1<<23 "
            "memo-capacity line; engine v15 inlined; empty kill table), "
            "published in the archive commits before the band"
        ),
        "manifest": "class2-lane-cost73l-win7-certificates-20261117.json",
        "manifest_blob_sha": MANIFEST_BLOB,
        "totals": {
            "certificates": 32,
            "rows": 1693203,
            "extraction_nodes": 424657112,
            "published_bytes": 61171191,
            "fbt_drops_total": 0,
            "capped_per_move_total": 0,
        },
        "determinism_sample_bits": [1, 9, 47, 61, 64, 116],
    }
    d["next_action"] = (
        "BigInt independent third-implementation re-verification of the 32 "
        "published certificates (adapt "
        "reverify_cost73j_certificates_bigint_20261117.py: manifest inside "
        "the band dir, per-bit rootcheck/subroots sidecars, cross-batch "
        "disjointness vs the earlier BigInt-verified roots); then the "
        "receipt fold of this row stays pending behind the 66i/66j/69j/71e/"
        "72d/73i/73j/73k folds"
    )
    out = pathlib.Path(dst)
    out.write_text(json.dumps(d, indent=1, ensure_ascii=True) + "\n")
    print(f"wrote {out} ({out.stat().st_size} bytes, git blob "
          f"{git_blob_sha(out.read_bytes())})")

if __name__ == "__main__":
    main()
