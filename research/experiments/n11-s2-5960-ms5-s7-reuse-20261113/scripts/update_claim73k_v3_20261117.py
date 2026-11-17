#!/usr/bin/env python3
# claim v3 updater for class2-lane cost73k (2026-11-17)
# v2 -> v3: in-flight claim advanced to certificates-complete. The 22 sweep
# WIN7-D10 roots are published as blind-extracted, engine-free verified
# WIN7-D10 certificates (19 split part1of2/part2of2 + 3 whole files, one
# file per commit, plus the certificate manifest, 19 README-split docs,
# 22 rootcheck/subroots sidecars and the extraction scripts in one commit).
# BigInt independent third-implementation re-verification: planned next.
import hashlib, json, sys, pathlib

V2_BLOB_SHA = "2150277f95fa202837d1cda10b390ee2bb54761b"
MANIFEST_BLOB = "0892aed07d187ae2fb3b4b90a21c7adbc1002b62"
BAND_FIRST = "40f8db4b215ce90d4fc2cfe52b82fcead03a2558"
BAND_LAST = "4c383a14025a6a8c8551cb20e7eb7b26288f1bee"

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
    assert d["schema"] == "n11-class2-lane-cost73k-inflight-20261117-v2"

    d["schema"] = "n11-class2-lane-cost73k-inflight-20261117-v3"
    d["last_updated"] = "2026-11-17"
    d["status"] = (
        "claim v3: certificates complete; the 22 sweep WIN7-D10 roots of the "
        "census-v7 rank-1 child are published as blind-extracted, "
        "engine-free verified WIN7-D10 certificates: 22 certificates, 966,535 "
        "rows, 155,946,109 extraction nodes, 34,933,538 published bytes, "
        "fbt_drops 0, no capped per-move; 19 certificates split at a line "
        "boundary into .cert.part1of2/.part2of2 (whole-file threshold "
        "1,200,000 bytes) + 3 whole files, pushed one file per commit (band "
        "commits " + BAND_FIRST[:8] + ".." + BAND_LAST[:8] + "; the first two "
        "commits carried a chunk-boundary newline corruption introduced by "
        "the publication tooling and were immediately repushed with the "
        "correct bytes; every landed certificate file was verified "
        "byte-exact against the local extraction md5 via git blob sha, "
        "41/41); certificate manifest class2-lane-cost73k-win7-"
        "certificates-20261117.json (git blob " + MANIFEST_BLOB + ") "
        "published together with 19 README-split-bit{N}.md recombination "
        "docs, 22 per-bit rootcheck.json + subroots.jsonl verification "
        "sidecars and the extraction scripts (cert_driver73k.ts, "
        "extract73k_all_20261117.sh, verify_cost73k_one.sh, "
        "build_cost73k_cert_manifest_20261117.py) in commit " +
        BAND_LAST[:8] + "; verification per verify_cost73k_one.sh with "
        "verify_bit7_win7_cert.ts (Bareiss 4x4, engine-free): root-check "
        "stones=7 and loser mobility equal to the independent "
        "legal_candidates.py enumeration on the RAW root on all 22, all "
        "sub-roots PASS on every root, terminal stone range within [13,17] "
        "on every sub-root, consumed-winner-state union vs certificate row "
        "set 0 missing / 0 extra in both directions on all 22 (re-verified "
        "from the saved certkeys/consumed artifacts when building the "
        "manifest); determinism: fresh-process re-extraction byte-identical "
        "(md5) on six of the twenty-two bits [0,7,11,15,35,117], including "
        "the heaviest bit 117 (2,150,734 bytes, 59,587 rows, reproduced "
        "98352c2e560977e20c14584d59ffa56b byte-identically); the 3 "
        "confirmation WIN roots (bits 14, 26, 55) are already covered by "
        "the published cost73j bit 110, cost73i bit 110 and cost69j bit 110 "
        "certificates; a third-implementation BigInt independent "
        "re-verification of this band (as done for the 69j/71e/72d/73j "
        "bands) is planned as the next step; the receipt fold stays pending "
        "behind the 76c/66i/66j/69j/71e/72d/73i folds; no manifest row is "
        "closed by this claim; 11x11 UNKNOWN"
    )
    d["certificates"] = {
        "status": (
            "complete: 22 WIN7-D10 certificates published (19 split "
            "part1of2/part2of2 + 3 whole files, one file per commit, band "
            "commits " + BAND_FIRST[:8] + ".." + BAND_LAST[:8] + "), "
            "manifest class2-lane-cost73k-win7-certificates-20261117.json "
            "(git blob " + MANIFEST_BLOB + "); the 3 confirmation WIN roots "
            "(bits 14, 26, 55) are covered by the published cost73j bit 110, "
            "cost73i bit 110 and cost69j bit 110 certificates; BigInt "
            "independent third-implementation re-verification planned next"
        ),
        "driver": "cert_driver73k.ts (73j driver duplicated, argv-driven, String.fromCharCode(10) newline convention), published in commit " + BAND_LAST[:8],
        "manifest": "class2-lane-cost73k-win7-certificates-20261117.json",
        "manifest_blob_sha": MANIFEST_BLOB,
    }
    d["next_action"] = (
        "BigInt independent third-implementation re-verification of the 22 "
        "published certificates (adapt "
        "reverify_cost73j_certificates_bigint_20261117.py: manifest inside "
        "the band dir, per-bit rootcheck/subroots sidecars, cross-batch "
        "disjointness vs the earlier BigInt-verified roots); then the "
        "receipt fold of this row stays pending behind the 76c/66i/66j/69j/"
        "71e/72d/73i folds"
    )
    out = pathlib.Path(dst)
    out.write_text(json.dumps(d, indent=1, ensure_ascii=True) + "\n")
    print(f"wrote {out} ({out.stat().st_size} bytes, git blob "
          f"{git_blob_sha(out.read_bytes())})")

if __name__ == "__main__":
    main()
