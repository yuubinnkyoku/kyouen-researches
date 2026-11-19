#!/usr/bin/env python3
"""Agreement audit for the proved z=10, y=5 slice (K1007) against the K1002
uniform candidate (research/experiments/vertical-fiber-two-token-z10-y-ge6-
census-20261119, conjectured for y>=6).

K1002 candidate (verbatim from its report):
  T = {1,3,5,7,9} u Q(d),  Q: d in {0,4,8} -> {2y+5+d/2}, d=11 ->
  O[2y+11,S+10], d>=12 -> {2y+11}, else empty.
  P (<tail): even d, 0<=d<=10: O[11, 2y+3+2*ceil(d/4)];
             even d >=12: O[11,2y+9] u E[2y+12, S+10];
             odd d, 1<=d<=9: O[11,S+10] u E[2y+6+2*floor((d+1)/4), S+9];
             odd d >=11:  O[11,2y+9] u E[2y+12, S+9].
  tail: R >= S+11  ->  H = S mod 2.

Audited claim: on the whole y=5 slice (grid x<=2000, 0<=R<=x+20; both forms
are constant-for-all-R beyond the tail start R>=S+11=x+16, so beyond x+20
nothing new appears), the mismatches are exactly
{(x=5,R=11),(x=5,R=13)} (candidate 1, proved 2): the h=z diagonal row.
The d=0 lattice point 2y+5=15 is shared; every sweep/steady/I-band row and
the tail coincide.  Tail agreement is additionally audited for x<=5000 and
the R<=11 columns against the height-only reduction v_single(x+5,10,R).
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


def qod(k):
    return k if k % 2 == 1 else k - 1


def v_single(x, z, R):
    """K0832 single-token closed form: all x>=1, z>=0."""
    if R == 0 or x <= 0:
        return 0
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 == 1 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = qod(z)
        if R <= m:
            return 2 if R % 2 == 1 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    m = qod(x)
    if R <= m:
        return 2 if R % 2 == 1 else 0
    return x % 2


# ---- K1007 candidate (verbatim copy of the proved closed form) ----
def k1007_T(x, R):
    if x == 5:
        return R in (1, 3, 5, 7, 9, 11, 13, 15)
    if x == 9:
        return R in (1, 3, 5, 7, 9, 17)
    if x == 13:
        return R in (1, 3, 5, 7, 9, 19)
    if x == 16:
        return R in (1, 3, 5, 7, 9) or (21 <= R <= 31 and R % 2 == 1)
    if x in (6, 7, 8, 10, 11, 12, 14, 15):
        return R in (1, 3, 5, 7, 9)
    return R in (1, 3, 5, 7, 9, 21)


def k1007_P(x, R):
    if x == 5:
        return False
    if x == 6:
        return R in (11, 13, 15) or R >= 16
    if x == 7:
        return R in (11, 13, 15)
    if x == 8:
        return R in (11, 13, 15, 17) or R >= 18
    if x == 9:
        return R in (11, 13, 15)
    if x == 10:
        return R in (11, 13, 15, 17) or R >= 18
    if x == 11:
        return R in (11, 13, 15, 17)
    if x == 12:
        return R in (11, 13, 15, 17, 19) or R >= 20
    if x == 13:
        return R in (11, 13, 15, 17)
    if x == 14:
        return R in (11, 13, 15, 17, 19) or R >= 20
    if x == 15:
        return R in (11, 13, 15, 17, 19)
    if x == 16:
        return (R in (11, 13, 15, 17, 19)
                or (22 <= R <= 32 and R % 2 == 0)
                or R >= 33)
    if x % 2 == 0:  # even x >= 18
        return (R in (11, 13, 15, 17, 19)
                or (22 <= R <= x + 16 and R % 2 == 0)
                or R >= x + 17)
    # odd x >= 17
    return R in (11, 13, 15, 17, 19) or (22 <= R <= x + 15 and R % 2 == 0)


def k1007(x, R):
    if R == 0:
        return 0
    if k1007_T(x, R):
        return 2
    return 1 if k1007_P(x, R) else 0


# ---- K1002 uniform candidate ----
def k1002(y, d, S, R):
    if R == 0:
        return 0
    if R >= S + 11:
        return S % 2
    if R in (1, 3, 5, 7, 9):
        return 2
    if d in (0, 4, 8):
        if R == 2 * y + 5 + d // 2:
            return 2
    if d == 11:
        if R % 2 == 1 and 2 * y + 11 <= R <= S + 10:
            return 2
    if d >= 12:
        if R == 2 * y + 11:
            return 2
    if d % 2 == 0:
        if d <= 10:
            hi_p = 2 * y + 3 + 2 * math.ceil(d / 4)
            if R % 2 == 1 and 11 <= R <= hi_p:
                return 1
        else:
            if R % 2 == 1 and 11 <= R <= 2 * y + 9:
                return 1
            if R % 2 == 0 and 2 * y + 12 <= R <= S + 10:
                return 1
    else:
        if d <= 9:
            if R % 2 == 1 and 11 <= R <= S + 10:
                return 1
            lo_e = 2 * y + 6 + 2 * ((d + 1) // 4)
            if R % 2 == 0 and lo_e <= R <= S + 9:
                return 1
        else:
            if R % 2 == 1 and 11 <= R <= 2 * y + 9:
                return 1
            if R % 2 == 0 and 2 * y + 12 <= R <= S + 9:
                return 1
    return 0


EXPECTED_MISMATCHES = [[5, 11], [5, 13]]


def audit_once():
    y = 5
    mismatches = []
    checks = 0
    for x in range(5, 2001):
        d = x - y
        S = x + y
        for R in range(0, x + 21):
            checks += 1
            a = k1007(x, R)
            b = k1002(y, d, S, R)
            if a != b:
                mismatches.append([x, R, a, b])

    tail_checks = 0
    for x in range(5, 5001):
        for off in range(5):
            R = x + 16 + off
            tail_checks += 1
            assert k1007(x, R) == k1002(5, x - 5, x + 5, R) == (x + 5) % 2

    height_checks = 0
    for x in range(5, 501):
        for R in range(1, 12):
            height_checks += 1
            assert k1007(x, R) == v_single(x + 5, 10, R)

    mismatches_short = [[m[0], m[1]] for m in mismatches]
    return {
        "all_pass": mismatches_short == EXPECTED_MISMATCHES,
        "classification": (
            "agreement of the proved K1007 y=5 slice with the K1002 "
            "y>=6 uniform candidate: mismatches exactly the h=z diagonal "
            "points {(5,11),(5,13)}; finite audit, the claim beyond the "
            "grid follows from the closed-form band structure"
        ),
        "expected_mismatches": EXPECTED_MISMATCHES,
        "grid": {"x": [5, 2000], "R": [0, "x+20"], "checks": checks},
        "height_only": {"x": [5, 500], "R": [1, 11], "checks": height_checks},
        "mismatches_observed": mismatches_short,
        "tail": {"x": [5, 5000], "R": "x+16..x+20", "checks": tail_checks},
        "target": "agreement K1007(K1002 on y=5 slice)",
        "total_checks": checks + tail_checks + height_checks,
    }


def run():
    first = audit_once()
    second = audit_once()
    same = (json.dumps(first, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"))
            == json.dumps(second, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":")))
    base = dict(first, repeat_runs=2, repeat_byte_identical=same)
    raw = json.dumps(base, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode()
    result = dict(base, sha256_without_hash_field=hashlib.sha256(raw).hexdigest())
    out = Path(__file__).with_name("output")
    out.mkdir(exist_ok=True)
    (out / "agree_audit.json").write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "all_pass": result["all_pass"],
        "mismatches_observed": result["mismatches_observed"],
        "repeat_byte_identical": same,
        "sha256_without_hash_field": result["sha256_without_hash_field"],
        "total_checks": result["total_checks"],
    }, sort_keys=True))
    if not result["all_pass"] or not same:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
