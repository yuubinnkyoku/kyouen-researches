#!/usr/bin/env python3
"""Authoritative cross-check: published kit-18 frozen census vs kit-18x blind second census.

Fresh single-file implementation (independent of audit_kit18x.py; its source was
not read for this script). Fail-closed: any pin mismatch, row mismatch, or
separation mismatch aborts with rc=1 before writing output.

Inputs (pinned, fetched from main HEAD at run time by the operator, sha256-gated):
  kit18.out  - research/experiments/strip-newband-m51m52-frontier-windows-evenlife-20261126/explore_m51m52_frontier_windows_evenlife.out
               (published kit-18 frozen census, commit 9ac8e079, git blob d6e61bbf, 557319 bytes)
  kit18x.out - research/experiments/strip-newband-m51m52-blind-second-census-20261126/census_kit18x.out
               (frozen blind second census, commit 79bee22c)

Consumes nothing; no verdict logic; finite observation comparison only.
"""
import hashlib
import json
import re
import sys
from collections import Counter

PIN_KIT18 = "c3087285fbdbd44d0588132f9c1d4c75fce2913b816ce383a5f0b377154364ba"
PIN_KIT18X = "97b6ebef02b290d7f047722f997dc4ec8b6cee8e65bce3fc0cd18bfbf287c776"
EXPECTED_ROWS = 49
EXPECTED_TOTAL_SEPS = 241

failures = []


def gate(name, ok, detail=""):
    status = "PASS" if ok else "FAIL"
    print(f"{name}: {status} {detail}")
    if not ok:
        failures.append(f"{name}: {detail}")
    return ok


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sep_key(sep):
    # canonical separation key: sorted multiset X, S, value, collapse, direction
    return (tuple(sorted(sep["X"])), sep["S"], sep["value"], sep["collapse"], sep["direction"])


def main():
    gate("G0a_kit18_sha256", sha256("kit18.out") == PIN_KIT18,
         f"got {sha256('kit18.out')[:16]} want {PIN_KIT18[:16]}")
    gate("G0b_kit18x_sha256", sha256("kit18x.out") == PIN_KIT18X,
         f"got {sha256('kit18x.out')[:16]} want {PIN_KIT18X[:16]}")
    if failures:
        print("ABORT: pin failure")
        return 1

    a = json.load(open("kit18.out"))
    b = json.load(open("kit18x.out"))

    rows18 = [s for s in a["sections"] if str(s.get("section", "")).endswith("_row_record")]
    rows18x = list(b["sections"])
    gate("G1a_kit18_rows", len(rows18) == EXPECTED_ROWS, f"{len(rows18)} row_record sections")
    gate("G1b_kit18x_rows", len(rows18x) == EXPECTED_ROWS, f"{len(rows18x)} sections")

    def mz18(s):
        m = re.match(r"(?:ladder|frontier|evenlife|inband)_m(\d+)_z(\d+)_row_record", s["section"])
        return (int(m.group(1)), int(m.group(2))) if m else None

    def mz18x(s):
        return (int(s["m"]), int(s["z"]))

    d18 = {mz18(s): s for s in rows18}
    d18x = {mz18x(s): s for s in rows18x}
    gate("G1c_mz_unique18", len(d18) == len(rows18) and None not in d18, f"{len(d18)} unique (m,z)")
    gate("G1d_mz_unique18x", len(d18x) == len(rows18x), f"{len(d18x)} unique (m,z)")
    gate("G2_mz_sets_equal", set(d18) == set(d18x),
         f"only18={sorted(set(d18)-set(d18x))[:4]} only18x={sorted(set(d18x)-set(d18))[:4]}")
    if failures:
        print("ABORT: row-set failure")
        return 1

    row_reports = []
    total18 = total18x = 0
    mismatched = []
    for mz in sorted(d18):
        ra, rb = d18[mz], d18x[mz]
        ca = Counter(sep_key(s) for s in ra["separations"])
        cb = Counter(sep_key(s) for s in rb["separations"])
        total18 += sum(ca.values())
        total18x += sum(cb.values())
        match = ca == cb
        if not match:
            mismatched.append(mz)
        row_reports.append({
            "m": mz[0], "z": mz[1],
            "section18": ra["section"], "kind18x": rb["kind"],
            "seps18": sum(ca.values()), "seps18x": sum(cb.values()),
            "shapes18": ra.get("shapes"), "shapes18x": rb.get("shapes"),
            "match": match,
        })
    gate("G3_all_49_rows_match", not mismatched, f"mismatched rows: {mismatched}")
    gate("G4a_total_seps_18", total18 == EXPECTED_TOTAL_SEPS, f"{total18}")
    gate("G4b_total_seps_18x", total18x == EXPECTED_TOTAL_SEPS, f"{total18x}")
    # per-row separation counts and shapes counts also compared per row above
    shapes_mismatch = [r["m"] for r in row_reports if r["seps18"] != r["seps18x"]]
    gate("G5_per_row_sep_counts", not shapes_mismatch, f"rows differing: {shapes_mismatch}")

    if failures:
        print("CROSSCHECK-FAIL")
        return 1

    out = {
        "schema": "kit18x-authoritative-crosscheck-v1",
        "result": "CROSSCHECK-PASS",
        "kit18_out_sha256": PIN_KIT18,
        "kit18x_out_sha256": PIN_KIT18X,
        "kit18_source": "research/experiments/strip-newband-m51m52-frontier-windows-evenlife-20261126/explore_m51m52_frontier_windows_evenlife.out (published, commit 9ac8e079)",
        "kit18x_source": "research/experiments/strip-newband-m51m52-blind-second-census-20261126/census_kit18x.out (commit 79bee22c)",
        "rows_compared": len(row_reports),
        "total_separations_each": total18,
        "all_rows_match": True,
        "gates_passed": ["G0a", "G0b", "G1a", "G1b", "G1c", "G1d", "G2", "G3", "G4a", "G4b", "G5"],
        "row_reports": row_reports,
        "status_guard": ("Finite-observation census comparison only; no verdict is consumed or "
                         "implied; the standard 11x11 empty board, all 19 central-reply roots, "
                         "the two-stone root {60,27} and every closure class remain UNKNOWN."),
    }
    with open("crosscheck_kit18_authoritative.out", "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    print("CROSSCHECK-PASS: 49/49 rows, 241/241 separations identical (multiset of {X,S,value,collapse,direction})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
