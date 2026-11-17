#!/usr/bin/env python3
# claim v3 updater for class2-lane cost73j (2026-11-17)
# v2 -> v3: sweep-complete claim advanced to certificates-complete after the
# 16 WIN7-D10 blind extractions passed independent engine-free verification.
# Design: assert the input is the exact published claim v2 git blob, then emit v3.
import hashlib, json, sys

V2_BLOB_SHA = "8324f1d860ddfbfcee2ad114d62ddb435261e153"
V1_BLOB_SHA = "d52005e662d39779d34ee5b1ae59f25a57f545a9"
MANIFEST_BLOB = "e88710b5a2d4848be77a03ae5104e46aefc1279a"

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def main() -> None:
    src = sys.argv[1]  # claim v2 json
    dst = sys.argv[2]  # claim v3 json output
    raw = open(src, "rb").read()
    sha = git_blob_sha(raw)
    if sha != V2_BLOB_SHA:
        sys.exit(f"FATAL: input is not the published claim v2 blob (got {sha})")
    d = json.loads(raw.decode("utf-8"))
    assert d["schema"] == "n11-class2-lane-cost73j-inflight-20261117-v2"

    d["schema"] = "n11-class2-lane-cost73j-inflight-20261117-v3"
    d["last_updated"] = "2026-11-17"
    d["status"] = (
        "claim v3: certificates complete; the 16 WIN7-D10 bits "
        "[0,1,6,29,44,49,52,69,74,82,87,91,98,100,110,118] of the completed v2 "
        "sweep were blindly extracted (extractor_exact, engine v15 inlined, "
        "FBS=1<<20, empty kill table) into 726,778 certificate rows "
        "(166,238,087 extraction nodes, 26,236,851 published bytes; fbt_drops=0, "
        "no fatal, no capped per-move on all sixteen) and independently "
        "verified engine-free (verify_bit7_win7_cert: root-check stones=7 and "
        "loser mobility = the legal_candidates.py RAW-root enumeration, all "
        "sub-roots PASS, terminal stone range within [13,17], consumed union "
        "0 missing / 0 extra on every root, re-verified from the saved "
        "certkeys/consumed artifacts when building the manifest); bits 69/82 "
        "published whole, the other fourteen split at line boundaries into "
        "part1of2/part2of2 with README-split per bit; determinism: fresh-"
        "process re-extraction of the heaviest WIN bit 98 (64,451 rows) is "
        "byte-identical (md5 0d8124b781d6d98878125abdb1a7ce76); all 30 "
        "certificate files landed byte-exact on main (reassembled split "
        "md5s match the manifest); manifest "
        "class2-lane-cost73j-win7-certificates-20261117.json (git blob " +
        MANIFEST_BLOB + "); the receipt fold stays pending behind the "
        "76c/66i/66j/69j/71e/72d/73i folds; no manifest row is closed by "
        "this claim; 11x11 UNKNOWN"
    )
    d["certificates"] = {
        "manifest": "output/class2-lane-cost73j-certificates/class2-lane-cost73j-win7-certificates-20261117.json",
        "schema": "n11-class2-lane-cost73j-win7-certificates-20261117-v1",
        "manifest_git_blob": MANIFEST_BLOB,
        "win7_d10_bits": [0, 1, 6, 29, 44, 49, 52, 69, 74, 82, 87, 91,
                          98, 100, 110, 118],
        "totals": {
            "certificates": 16,
            "rows": 726778,
            "extraction_nodes": 166238087,
            "published_bytes": 26236851,
            "fbt_drops": 0
        },
        "whole_file_bits": [69, 82],
        "split_bits": [0, 1, 6, 29, 44, 49, 52, 74, 87, 91, 98, 100, 110, 118],
        "verification": ("engine-free verify_bit7_win7_cert.ts per root: "
                         "stones=7 root check, loser mobility = "
                         "legal_candidates.py RAW-root count (48-62 per root), "
                         "all sub-roots PASS, consumed union 0 missing / 0 "
                         "extra, terminal stone range within [13,17]; heaviest "
                         "bit 98 blind re-extraction byte-identical (md5 "
                         "0d8124b781d6d98878125abdb1a7ce76)"),
        "driver": ("scripts/cert_driver73j.ts (72d driver duplicated, "
                   "argv-driven, String.fromCharCode(10) newline convention); "
                   "ev73j.sh orchestrates; verify_cost73j_one.sh per-root "
                   "orchestration")
    }
    d["next_action"] = (
        "receipt fold of this row stays pending behind the 76c/66i/66j/69j/71e/"
        "72d/73i folds (managed by their own lanes); the next fresh target for "
        "this lane is the census v6 top-10 cost-73 runner-up row "
        "00000000000000801206000000000400 (open 67, demand c2=2)"
    )
    out = json.dumps(d, indent=1, ensure_ascii=True) + "\n"
    open(dst, "w").write(out)
    print(f"claim v3 written: {dst} ({len(out)} bytes); input blob sha verified {V2_BLOB_SHA[:8]}")

if __name__ == "__main__":
    main()
