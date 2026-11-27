#!/usr/bin/env python3
"""Authoritative cross-check: published kit-19x blind census vs published kit-19 (kit-19x lane).

To be executed ONLY after the kit-19 build lane has published its frozen .out
to main. Command line:
  python3 crosscheck_kit19_authoritative.py <published_kit19x_census.out> <published_kit19.out> <expected_sha256_of_kit19_out>

Method: kit-18x authoritative precedent (commit 6ee2cfc0). Fresh single-file
comparator; neither explorer source is read. Per row_record section (49 rows),
separation multisets of canonicalized tuples (sorted X, S, value, collapse,
direction) must be identical on both sides.

Gates (all fail-closed):
  G0  kit-19x census sha256 == 275faedc... (published f38d2b43 record).
  G1  kit-19x census engine pin == 582c93c1... and gate PASS.
  G2  kit-19 .out sha256 == expected (pinned at execution time from main).
  G3  49 row_record sections on each side, identical name sets.
  G4  all 49 row separation multisets identical.
  G5  totals == 273 on both sides.
"""
import hashlib, json, sys

X_SHA = "275faedc80d04e2899c081eb7c56a0bcb80f7cf01b644793c6b846eb3d10a2f4"
ENG = "582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0"

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()

def rows(doc):
    return {s["section"]: s for s in doc["sections"] if s.get("section", "").endswith("_row_record")}

def sepmultiset(sec):
    return sorted((tuple(sorted(sp["X"])), sp["S"], sp["value"], sp["collapse"], sp["direction"])
                  for sp in sec.get("separations", []))

def main():
    if len(sys.argv) != 4:
        print("usage: crosscheck_kit19_authoritative.py <kit19x.out> <kit19.out> <expected_kit19_sha256>")
        sys.exit(2)
    x_path, k_path, k_exp = sys.argv[1], sys.argv[2], sys.argv[3]
    gates = []
    def gate(name, ok, msg=""):
        gates.append(ok)
        print(("GATE-PASS " if ok else "GATE-FAIL ") + name + (" " + msg if msg else ""))
        return ok

    xs, ks = sha256(x_path), sha256(k_path)
    gate("G0_kit19x_census_sha", xs == X_SHA, xs)
    xd = json.load(open(x_path))
    eng = [s for s in xd["sections"] if s.get("section") == "engine_gate"]
    gate("G1_kit19x_engine_pin", bool(eng) and eng[0].get("engine_sha") == ENG and eng[0].get("gate") == "PASS")
    gate("G2_kit19_out_sha_pinned", ks == k_exp, ks)
    kd = json.load(open(k_path))
    xr, kr = rows(xd), rows(kd)
    gate("G3_row_counts_49x49_names_equal", len(xr) == 49 and len(kr) == 49 and set(xr) == set(kr),
         "x=%d k=%d" % (len(xr), len(kr)))
    diffs, tx, tk = [], 0, 0
    if set(xr) == set(kr):
        for name in sorted(xr):
            mx, mk = sepmultiset(xr[name]), sepmultiset(kr[name])
            tx += len(mx); tk += len(mk)
            if mx != mk:
                diffs.append((name, len(mx), len(mk), [(a, b) for a, b in zip(mx, mk) if a != b][:10]))
        gate("G4_all_49_rows_identical", not diffs,
             ("first=" + json.dumps(diffs[0])[:300]) if diffs else "")
        gate("G5_totals_273", tx == 273 and tk == 273, "x=%d k=%d" % (tx, tk))
    else:
        gate("G4_all_49_rows_identical", False, "row name sets differ")
        gate("G5_totals_273", False, "skipped")
    print("RESULT:", "CROSSCHECK-PASS" if all(gates) else "CROSSCHECK-FAIL")
    sys.exit(0 if all(gates) else 1)

if __name__ == "__main__":
    main()
