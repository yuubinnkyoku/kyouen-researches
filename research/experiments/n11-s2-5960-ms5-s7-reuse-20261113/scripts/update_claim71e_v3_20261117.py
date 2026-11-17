#!/usr/bin/env python3
# claim v3 updater for class2-lane cost71e (2026-11-17)
# v2 -> v3: sweep-complete claim advanced to certificates-complete after the
# 13 WIN7-D10 blind extractions passed independent verification.
# Design: assert the input is the exact published claim v2 git blob, then emit v3.
import hashlib, json, sys, io

V2_BLOB_SHA = "3299f80fd42079a4a956afb606df513b1e7bb869"
V1_BLOB_SHA = "f64394741142258206149e652f68e2af558b1cff"

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
    assert d["schema"] == "n11-class2-lane-cost71e-inflight-20261117-v2"

    d["schema"] = "n11-class2-lane-cost71e-inflight-20261117-v3"
    d["last_updated"] = "2026-11-17"
    d["status"] = (
        "claim v3: certificates complete; the 13 WIN7-D10 bits [3,4,8,41,54,58,"
        "76,79,94,96,100,116,119] of the completed v2 sweep were blindly "
        "extracted (extractor_exact, engine v15 inlined, FBS=1<<20, empty kill "
        "table) into 534,804 certificate rows (141,067,035 extraction nodes, "
        "19,300,105 published bytes; fbt_drops=0, no fatal, no capped per-move on "
        "all thirteen) and independently verified engine-free (verify_bit7_win7_cert: "
        "root-check stones=7 and loser mobility = the legal_candidates.py RAW-root "
        "enumeration, all sub-roots PASS, terminal stone range [13,17], consumed "
        "union 0 missing / 0 extra on every root); bits 41/79/58 published whole, "
        "the other ten split at line boundaries into part1of2/part2of2 with "
        "README-split per bit; extraction proved deterministic: a mid-run execution-"
        "environment reset destroyed the first verified pass before publication "
        "and the fresh-environment re-extraction reproduced all five recorded "
        "pre-reset md5s (bits 41/3/4/8/54) byte-identically and re-verified all "
        "13 (unplanned cross-environment determinism check); manifest "
        "class2-lane-cost71e-win7-certificates-20261117.json; the receipt fold "
        "stays pending behind the 76c/66i/66j/69j folds; no manifest row is "
        "closed by this claim; 11x11 UNKNOWN"
    )
    d["certificates"] = {
        "manifest": "output/class2-lane-cost71e-certificates/class2-lane-cost71e-win7-certificates-20261117.json",
        "schema": "n11-class2-lane-cost71e-win7-certificates-20261117-v1",
        "win7_d10_bits": [3, 4, 8, 41, 54, 58, 76, 79, 94, 96, 100, 116, 119],
        "totals": {
            "certificates": 13,
            "rows": 534804,
            "extraction_nodes": 141067035,
            "published_bytes": 19300105,
            "fbt_drops": 0
        },
        "whole_file_bits": [41, 79, 58],
        "split_bits": [3, 4, 8, 54, 76, 94, 96, 100, 116, 119],
        "verification": "engine-free verify_bit7_win7_cert.ts per root: stones=7 root check, loser mobility = legal_candidates.py RAW-root count (41:51, 79:48, 58:48, others per manifest), all sub-roots PASS, consumed union 0 missing / 0 extra, terminal stone range [13,17]",
        "driver": "scripts/cert_driver71e.ts (69j driver duplicated with the push-transport-mangled literal newline split repaired to String.fromCharCode(10)); ev71e.sh orchestrates; verify_cost71e_one.sh per-root orchestration"
    }
    d["next_action"] = (
        "receipt fold of this row stays pending behind the 76c/66i/66j/69j folds "
        "(managed by their own lanes); next fresh target for this lane: the "
        "census v5 runner-up cost-72 row 00000000000000403800000008004000 (open 67)"
    )
    out = json.dumps(d, indent=1, ensure_ascii=True) + "\n"
    open(dst, "w").write(out)
    print(f"claim v3 written: {dst} ({len(out)} bytes); input blob sha verified {V2_BLOB_SHA[:8]}")

if __name__ == "__main__":
    main()
