#!/usr/bin/env python3
"""Cross-lane agreement check: two independent BigInt bytes reverifications of
the cost73j certificates (16 WIN7-D10), performed by two concurrent lanes.

Lane A (published first, commit tree fetched from main raw): parallel lane
  - mirror built from the pin commit via raw CDN fetch + GitHub directory
    listing blob sha assertions
Lane B (local, this lane): independent mirror fetched separately from the
  same band at pin commit 6758f03e485c6896d5101d3a4d31bc59fb9537e9,
  independently re-verified with a separately written verifier script.

This script compares the 16 entries field-by-field (37 common fields per
entry, including nested parts pins) between the two reverification JSONs.
It does NOT publish either JSON; it only records agreement.

Usage: python3 check_cost73j_reverification_cross_lane_agreement_20261117.py \
          <lane_a_json> <lane_b_json> <output_json>
"""
import hashlib
import json
import sys


def canon_entry(e):
    return {
        "bit": e["bit"],
        "root_hex": e["root_hex"],
        "d4_canon_root": e["d4_canon_root"],
        "raw_is_canon": e["raw_is_canon"],
        "certificate": e["certificate"],
        "storage": e["storage"],
        "record_source": e["record_source"],
        "record_kind": e["record_kind"],
        "readme_split_doc": e.get("readme_split_doc"),
        "joined_bytes": e["joined_bytes"],
        "joined_md5": e["joined_md5"],
        "joined_sha256": e["joined_sha256"],
        "joined_git_blob_sha": e["joined_git_blob_sha"],
        "manifest_md5_match": e["manifest_md5_match"],
        "manifest_sha256_match": e["manifest_sha256_match"],
        "record_rows": e["record_rows"],
        "record_extraction_nodes": e["record_extraction_nodes"],
        "record_sub_roots_pass": e["record_sub_roots_pass"],
        "record_loser_mobility": e["record_loser_mobility"],
        "record_terminal_stone_range": e["record_terminal_stone_range"],
        "rootcheck_stones": e["rootcheck_stones"],
        "rootcheck_loser_mobility": e["rootcheck_loser_mobility"],
        "subroots_sidecar_lines": e["subroots_sidecar_lines"],
        "subroots_sidecar_keys": e["subroots_sidecar_keys"],
        "verifier_status": e["verifier_status"],
        "verifier_root_mobility": e["verifier_root_mobility"],
        "verifier_rows": e["verifier_rows"],
        "verifier_subroots_passed": e["verifier_subroots_passed"],
        "verifier_terminal_range": e["verifier_terminal_range"],
        "verifier_terminal_count": e["verifier_terminal_count"],
        "verifier_visited_states": e["verifier_visited_states"],
        "verifier_loser_reply_edges": e["verifier_loser_reply_edges"],
        "verifier_winner_states": e["verifier_winner_states"],
        "verifier_loser_states": e["verifier_loser_states"],
        "verifier_union_missing": e["verifier_union_missing"],
        "verifier_union_extra": e["verifier_union_extra"],
        "parts": {
            name: {"pinned_blob_sha": pd["pinned_blob_sha"],
                   "bytes": pd["bytes"]}
            for name, pd in sorted((e.get("parts") or {}).items())
        },
    }


def main():
    lane_a_path, lane_b_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(lane_a_path, "r", encoding="utf-8") as f:
        a_doc = json.load(f)
    with open(lane_b_path, "r", encoding="utf-8") as f:
        b_doc = json.load(f)

    a_entries = {e["bit"]: canon_entry(e) for e in a_doc["entries"]}
    b_entries = {e["bit"]: canon_entry(e) for e in b_doc["entries"]}

    a_bits = sorted(a_entries.keys())
    b_bits = sorted(b_entries.keys())
    mismatches = []
    field_checks = 0

    if a_bits != b_bits:
        mismatches.append(
            {
                "kind": "bit_set",
                "lane_a_bits": a_bits,
                "lane_b_bits": b_bits,
            }
        )

    for bit in sorted(set(a_bits) & set(b_bits)):
        ae, be = a_entries[bit], b_entries[bit]
        for k in ae:
            if k == "parts":
                ap = ae["parts"]
                bp = be["parts"]
                if sorted(ap.keys()) != sorted(bp.keys()):
                    mismatches.append({"kind": "parts_names", "bit": bit,
                                       "lane_a": sorted(ap.keys()),
                                       "lane_b": sorted(bp.keys())})
                    field_checks += 1
                    continue
                for name in sorted(ap.keys()):
                    for fk in ("pinned_blob_sha", "bytes"):
                        field_checks += 1
                        if ap[name][fk] != bp[name][fk]:
                            mismatches.append(
                                {"kind": "parts_field", "bit": bit,
                                 "part": name, "field": fk,
                                 "lane_a": ap[name][fk],
                                 "lane_b": bp[name][fk]})
                continue
            field_checks += 1
            if ae[k] != be[k]:
                mismatches.append({"kind": "entry_field", "bit": bit,
                                   "field": k,
                                   "lane_a": ae[k], "lane_b": be[k]})

    n_fields_per_entry = 36 + 1  # 36 scalar + parts block
    out = {
        "schema": ("n11-class2-lane-cost73j-reverification-cross-lane-"
                   "agreement-20261117-v1"),
        "date": "2026-11-17",
        "method": (
            "Machine comparison of two independent BigInt bytes "
            "reverifications of the 16 cost73j WIN7-D10 certificates "
            "(class2-lane-cost73j). Lane A: reverification JSON published "
            "to main by a concurrent lane (fetched from main raw, "
            "pin.commit "
            + str(a_doc.get("pin", {}).get("commit", "unknown"))
            + "). Lane B: this lane's independent reverification JSON "
            "(separately written verifier, separate mirror fetched from "
            "the same band at pin commit "
            + str(b_doc.get("pin", {}).get("commit", "unknown"))
            + "). All 16 entries compared field-by-field on the 36 "
            "common scalar fields plus the nested per-part pin blocks "
            "(pinned_blob_sha and bytes for each split part)."),
        "lane_a": {
            "source": "main raw fetch of the published reverification JSON",
            "schema": a_doc.get("schema"),
            "pin_commit": a_doc.get("pin", {}).get("commit"),
            "entries": len(a_entries),
        },
        "lane_b": {
            "source": ("this lane's local independent reverification "
                       "(script reverify_cost73j_certificates_bigint_"
                       "20261117.py, run twice byte-identical)"),
            "schema": b_doc.get("schema"),
            "pin_commit": b_doc.get("pin", {}).get("commit"),
            "entries": len(b_entries),
        },
        "bits_compared": sorted(set(a_bits) & set(b_bits)),
        "entries_compared": len(sorted(set(a_bits) & set(b_bits))),
        "field_checks_total": field_checks,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "verdict": ("AGREEMENT" if len(mismatches) == 0 else "DISAGREEMENT"),
        "interpretation_guard": (
            "This agreement record concerns only the independent "
            "reproducibility of the cost73j certificate reverification "
            "(16 seven-stone roots, depth-10 subtree proof of first-player "
            "win). It does not decide the 11x11 empty board or any "
            "two-stone root; the 11x11 game value remains UNKNOWN. "
            "REFUTED-D10 is not a LOSS proof at any larger scope."),
    }
    doc_bytes = json.dumps(out, indent=2, sort_keys=False,
                           ensure_ascii=False).encode("utf-8")
    doc_bytes += b"\n"
    with open(out_path, "wb") as f:
        f.write(doc_bytes)
    print("verdict:", out["verdict"])
    print("entries_compared:", out["entries_compared"])
    print("field_checks_total:", field_checks)
    print("mismatch_count:", len(mismatches))
    for m in mismatches[:20]:
        print("MISMATCH:", json.dumps(m, ensure_ascii=False))
    print("output:", out_path)
    print("sha256:", hashlib.sha256(doc_bytes).hexdigest())
    sys.exit(0 if not mismatches else 1)


if __name__ == "__main__":
    main()
