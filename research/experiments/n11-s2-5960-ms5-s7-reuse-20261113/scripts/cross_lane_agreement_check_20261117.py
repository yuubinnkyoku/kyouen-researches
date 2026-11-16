#!/usr/bin/env python3
"""Cross-lane agreement check (2026-11-17): compare the two independently
produced BigInt bytes re-verification runs that overlap on 19 certificates.

  A (parallel lane, published at commits 1514699b / c45ad66f):
    output/class2-lane-cost60c69e70g-certificates-bigint-reverification-20261117.json
    19 certificates (60c 1 / 69e 10 / 70g manifest 8)

  B (this lane):
    output/class2-lane-receipts-recompute-bands-certificates-bigint-independent-reverification-20261117.json
    83 certificates (60c 1 / 63h 1 / 63i 18 / 63j 29 / 65m 8 / 67d 1 / 69e 10 / 70g 15)

For every (band, bit) pair covered by both, compares field by field:
git blob sha, published bytes, md5 (bit 116: uncompressed md5/bytes),
expected rows, verifier rows / subroots_passed / root_mobility /
terminal_count / terminal_range / visited_states / loser_reply_edges /
union_missing / union_extra, verifier_status.

Deterministic; exit 0 iff all pairs fully agree and none is missing.
"""
import json
import sys

DEFAULT_A = ("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/"
             "class2-lane-cost60c69e70g-certificates-bigint-reverification-20261117.json")
DEFAULT_B = ("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/"
             "class2-lane-receipts-recompute-bands-certificates-bigint-independent-reverification-20261117.json")

path_a = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_A
path_b = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_B

with open(path_a) as f:
    par = json.load(f)
with open(path_b) as f:
    mine = json.load(f)

mine_idx = {(e["band"], e["bit"]): e for e in mine["entries"]}

FIELD_MAP = [
    ("expected_rows", "record_rows"),
    ("root_hex", "root_hex"),
]
PUB_MAP = [
    ("git_blob_sha", "pinned_blob_sha"),
    ("bytes", "certificate_bytes"),
    ("md5", "computed_md5"),
]
VER_MAP = [
    ("strategy_rows", "verifier_rows"),
    ("subroots_passed", "verifier_subroots_passed"),
    ("root_mobility", "verifier_root_mobility"),
    ("terminal_count", "verifier_terminal_count"),
    ("terminal_range", "verifier_terminal_range"),
    ("visited_states_across_subroots", "verifier_visited_states"),
    ("loser_reply_edges", "verifier_loser_reply_edges"),
    ("union_missing", "verifier_union_missing"),
    ("union_extra", "verifier_union_extra"),
]

results = []
mismatches = []
missing = []

for p in par["per_certificate"]:
    band = p["band"].removeprefix("cost")
    key = (band, p["bit"])
    m = mine_idx.get(key)
    if m is None:
        missing.append(key)
        continue
    pair_checks = [(pf, p.get(pf), m.get(mf)) for pf, mf in FIELD_MAP]
    pub = p.get("published", {})
    if p["bit"] == 116 and band == "69e":
        pair_checks += [
            ("uncompressed_bytes", pub.get("uncompressed_bytes"), m.get("certificate_bytes")),
            ("uncompressed_md5", pub.get("uncompressed_md5"), m.get("computed_md5")),
        ]
    else:
        pair_checks += [(pf, pub.get(pf), m.get(mf)) for pf, mf in PUB_MAP]
    ver = p.get("verifier", {})
    pair_checks += [(pf, ver.get(pf), m.get(mf)) for pf, mf in VER_MAP]
    pair_checks.append(("verifier_status", p.get("verifier_status"), m.get("verifier_status")))

    ok = True
    for name, pv, mv in pair_checks:
        if pv != mv:
            ok = False
            mismatches.append({"band": band, "bit": p["bit"], "field": name,
                               "parallel": pv, "mine": mv})
    results.append({"band": band, "bit": p["bit"], "root_hex": p["root_hex"],
                    "fields_checked": len(pair_checks), "agree": ok})

n_agree = sum(1 for r in results if r["agree"])
out = {
    "schema": "n11-class2-lane-cross-lane-agreement-cost60c69e70g-20261117-v1",
    "date": "2026-11-17",
    "parallel_run": {
        "file": DEFAULT_A,
        "published_commits": {
            "artifacts": "1514699b",
            "log": "c45ad66f"
        },
        "certificates_checked": par.get("certificates_checked")
    },
    "this_run": {
        "file": DEFAULT_B,
        "records": mine.get("summary", {}).get("records")
    },
    "pairs_compared": len(results),
    "pairs_missing_in_this_run": missing,
    "pairs_agree": n_agree,
    "pairs_disagree": len(results) - n_agree,
    "total_field_comparisons": sum(r["fields_checked"] for r in results),
    "mismatches": mismatches,
    "all_agree": n_agree == len(results) and not missing,
    "interpretation_guard": ("agreement of two independently produced bytes-level "
        "re-verification runs over their 19 overlapping certificates; it is not a "
        "game-theoretic result; 11x11 empty board, two-stone roots {49,60}/{59,60}, "
        "S2 {59,60} and classes 1/2/4 remain UNKNOWN"),
}
print(json.dumps(out, indent=1, sort_keys=True))
sys.exit(0 if out["all_agree"] else 1)
