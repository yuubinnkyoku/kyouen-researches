#!/usr/bin/env python3
"""D4-canonical-key extension of the certificate state-sharing measurement.

The v1 measurement (class2-lane-cert-state-sharing-and-conf-cost-
measurement-20261117.json, commit 9f2422d3) quantified state sharing with
exact 32-hex equality and explicitly left symmetry-aware keying
unquantified. This addendum quantifies it: every certificate row state is
mapped to its D4 canonical form (min hex over the eight square symmetries
of the 11x11 board) and the same sharing statistics are recomputed on the
canonical keys.

Correctness gate: the generalized canon function is asserted against all
published d4_canon_root values of the cost73j certificate manifest (16
seven-stone roots) before measuring.

Deterministic: set operations only; two runs produce byte-identical
output.

Usage: python3 measure_cert_state_sharing_d4canon_20261117.py <out.json>
"""
import glob
import hashlib
import json
import os
import sys

BANDS = {
    "73j": "/home/user/krepo/certs73j/class2-lane-cost73j-certificates",
    "72d": "/home/user/krepo/certs72d",
    "71e": "/home/user/krepo/certs71e",
}
MANIFEST_73J = ("class2-lane-cost73j-certificates/"
                "class2-lane-cost73j-win7-certificates-20261117.json")
MANIFEST_73J_PATH = ("/home/user/krepo/certs73j/" + MANIFEST_73J)


def d4_canon(h):
    """Min hex over the eight square symmetries of the 11x11 board.
    Generalized (any stone count) from the validated 7-stone lineage
    implementation used by the 73j BigInt reverification (asserted there
    against every record's d4_canon_root)."""
    v_in = int(h, 16)
    stones = [i for i in range(121) if v_in >> i & 1]
    best = None
    for xf in (False, True):
        for yf in (False, True):
            for sw in (False, True):
                v = 0
                for i in stones:
                    x, y = i % 11, i // 11
                    if xf:
                        x = 10 - x
                    if yf:
                        y = 10 - y
                    if sw:
                        x, y = y, x
                    v |= 1 << (y * 11 + x)
                hs = "%032x" % v
                if best is None or hs < best:
                    best = hs
    return best


def load_band_canon(band_dir):
    """Return (canon->cert-count map, rows, ncerts, exact_distinct)."""
    groups = []
    for p1 in sorted(glob.glob(os.path.join(band_dir, "*.part1of2"))):
        groups.append([p1, p1.replace("part1of2", "part2of2")])
    for w in sorted(glob.glob(os.path.join(band_dir, "*.cert"))):
        if "part" not in w:
            groups.append([w])
    canon_certs = {}
    rows = 0
    exact = set()
    for parts in groups:
        text = ""
        for p in parts:
            with open(p, "r", encoding="utf-8") as fh:
                text += fh.read()
        for ln in text.splitlines()[2:]:
            if not ln.strip():
                continue
            st = ln.split(" ", 1)[0]
            exact.add(st)
            c = d4_canon(st)
            canon_certs[c] = canon_certs.get(c, 0) + 1
            rows += 1
    return canon_certs, rows, len(groups), len(exact)


def main():
    out_path = sys.argv[1]

    # correctness gate: published d4_canon_root values for the 73j roots
    manifest = json.load(open(MANIFEST_73J_PATH, "r", encoding="utf-8"))
    checked = 0
    for rec in manifest["certificates"]:
        got = d4_canon(rec["root"])
        exp = rec["d4_canon_root"]
        assert got == exp, ("D4 canon mismatch", rec["root"], got, exp)
        checked += 1

    bands = {}
    sets = {}
    for tag, d in BANDS.items():
        canon_certs, rows, ncerts, exact_n = load_band_canon(d)
        canon_n = len(canon_certs)
        shared = sum(1 for v in canon_certs.values() if v > 1)
        dup_rows = sum(v - 1 for v in canon_certs.values())
        hist = {}
        for v in canon_certs.values():
            hist[v] = hist.get(v, 0) + 1
        bands[tag] = {
            "certificates": ncerts,
            "rows_total": rows,
            "exact_distinct_states": exact_n,
            "d4_canon_distinct_states": canon_n,
            "canon_reduction_pct": round(100.0 * (exact_n - canon_n) / exact_n, 3),
            "canon_states_in_multiple_certs": shared,
            "canon_states_shared_pct": round(100.0 * shared / canon_n, 3),
            "canon_duplicate_rows": dup_rows,
            "canon_duplicate_rows_pct": round(100.0 * dup_rows / rows, 3),
            "canon_cert_count_histogram": {str(k): hist[k] for k in sorted(hist)},
        }
        sets[tag] = set(canon_certs.keys())

    pairwise = {}
    tags = sorted(sets)
    for i in range(len(tags)):
        for j in range(i + 1, len(tags)):
            a, b = tags[i], tags[j]
            inter = sets[a] & sets[b]
            pairwise["%s_and_%s" % (a, b)] = {
                "canon_shared_states": len(inter),
                "pct_of_%s" % a: round(100.0 * len(inter) / len(sets[a]), 3),
                "pct_of_%s" % b: round(100.0 * len(inter) / len(sets[b]), 3),
            }
    inter3 = sets["73j"] & sets["72d"] & sets["71e"]

    out = {
        "schema": ("n11-class2-lane-cert-state-sharing-d4canon-"
                   "measurement-20261117-v1"),
        "date": "2026-11-17",
        "extends": ("class2-lane-cert-state-sharing-and-conf-cost-"
                    "measurement-20261117.json (commit 9f2422d3)"),
        "method": (
            "Same three published certificate bands, same input pins as the "
            "v1 measurement; every row state mapped to its D4 canonical "
            "form (min hex over the eight square symmetries of the 11x11 "
            "board) and all sharing statistics recomputed on canonical "
            "keys. Correctness gate: the canon function reproduces all "
            "%d published d4_canon_root values of the cost73j certificate "
            "manifest before measuring." % checked),
        "d4_canon_root_assertions": checked,
        "bands": bands,
        "cross_band_pairwise": pairwise,
        "cross_band_three_way_canon_shared_states": len(inter3),
        "interpretation_guard": (
            "Efficiency measurement only, on published certificate bytes. "
            "WIN7-D10 certificates prove a first-player win within depth "
            "10 from the individual 7-stone roots only; REFUTED-D10 is "
            "not a LOSS proof. No manifest row is closed. The 11x11 "
            "empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and "
            "classes 1/2/4 all remain UNKNOWN."),
    }
    doc = json.dumps(out, indent=1, ensure_ascii=False) + "\n"
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print("d4_canon_root assertions:", checked)
    for tag in tags:
        b = bands[tag]
        print("%s: exact %d -> canon %d (-%.2f%%) canon_shared %d (%.2f%%) canon_dup_rows %.2f%%"
              % (tag, b["exact_distinct_states"], b["d4_canon_distinct_states"],
                 b["canon_reduction_pct"], b["canon_states_in_multiple_certs"],
                 b["canon_states_shared_pct"], b["canon_duplicate_rows_pct"]))
    for k, v in pairwise.items():
        print("%s: canon shared %d" % (k, v["canon_shared_states"]))
    print("three-way canon shared:", len(inter3))
    print("wrote", out_path)


if __name__ == "__main__":
    main()
