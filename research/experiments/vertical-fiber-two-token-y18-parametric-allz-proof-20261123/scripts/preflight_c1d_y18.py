#!/usr/bin/env python3
"""Pre-flight validation of the published fixed-z slice anchors at the y=18 rows.

Fail-closed pre-integration check mirroring the y=10 (K1141), y=12 (K1152/K1162),
y=13 (K1231/K1232), y=14 (K1233/K1234), y=15 (K1236), y=16 (K1239) and y=17 (K1240/K1241) part2
procedures: before the anchor functions A8u..A17u are incorporated into the
part2 verifier of this experiment dir, their y=18 rows are validated three-way
against both raw engines (transcribed in the published part1 verifier
verify_y18_universal.py, published SHA-256 14373419... per its own 3-run
byte-identical audit) and against the y=18 closed form cand18.

Anchor provenance: y=10 part2 verifier verify_y10_universal.py (published,
SHA-256 f9169449309dcd25aaba8d6379d4289167f61eb3895b031e45ff9e80c46c05e4,
its own 3-run byte-identical audit 41b7a315...), which transcribed them from
the published slice verifiers:
  z=8 : K0999/K1000 (verify_z8_y_ge9_proof.py  SHA-256 e88e5ea7...)
  z=9 : K1001       (verify_z9_y_ge9_proof.py SHA-256 db1d60c6...)
  z=10: K1011 scope (verify_z10_y_ge9_proof.py SHA-256 42db00b2...)
  z=15: K1065       (verify_z15_y_ge6.py      SHA-256 131e1c64...)
  z=16: K1077       (verify_z16_y_ge6.py      SHA-256 d07c3b0e...)
  z=17: K1087       (verify_z17_y_ge6.py      SHA-256 e49d24d2...)
The anchor block below is byte-verbatim the published y=12 pre-flight's
anchor block (scripts/preflight_c1d_y12.py, in the published y=12 experiment
dir), itself the y=10 part2 verifier transcription; the y=10 pre-flight of
the same transcriptions caught an evaluation-order bug in the K1087
first-draft transcription (170 mismatches); the published rows used here are
the corrected published bytes. The y=10 part2 pre-flight (15,336 points), the
y=12 part2 pre-flight (14,484 anchor points + 9,768 low-R points), the
y=13 part2 pre-flight (14,157 anchor points + 9,702 low-R points), the
y=14 part2 pre-flight (13,824 anchor points + 9,636 low-R points), the
y=15 part2 pre-flight (13,485 anchor points + 9,570 low-R points) and the
y=16 part2 pre-flight (13,140 anchor points + 9,504 low-R points) and
the y=17 part2 pre-flight (12,789 anchor points + 9,438 low-R points)
all passed before this y=18 run.

Pre-flight box (this run): for each z0 in {8,9,10,15,16,17}, x=18..45,
R in [1, x+z0+30], compare A(z0,x,18,R) == H_ordered(R,(x,18),z0)
== H_canonical(R,(x,18),z0) == cand18(z0,x,R). Any mismatch aborts the
part2 integration (the anchors only enter the verifier after this passes).

Low-R single-token reduction pre-flight (published for the fixed-z y>=6
slices, R <= z+6): z0 in {15,16,17}, x=18..159, R in [1, z0+6]:
cand18(z0,x,R) == single_token(x+18, z0, R).

Result: output/preflight-c1d-y18.json (sorted keys, deterministic, no clock).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from verify_y18_universal import H_ordered, H_canonical, cand18, single_token  # noqa: E402


# =====================================================================
# Published fixed-z slice anchors, verbatim block from the y=10 part2
# verifier (see module docstring provenance). (x, y, r) parametric form,
# evaluated at the y row of the caller's choice.
# =====================================================================
# ------------------------------------------------------------------
# Published fixed-z slice anchors specialised at y=10 (C1d).
# Independent of the cand10 tables above. Uniform closed forms kept in
# their published parametric (x,y,r) form and evaluated at the y=10 row:
#   z=8:  K0999/K1000 uniform candidate, scope x>=y>=9
#         (verify_z8_y_ge9_proof.py, SHA-256 e88e5ea7...)
#   z=9:  K1001 uniform candidate, scope x>=y>=9
#         (verify_z9_y_ge9_proof.py, SHA-256 db1d60c6...)
#   z=10: K1002 uniform candidate restricted to y>=9 = the K1011 proof
#         scope (verify_z10_y_ge9_proof.py, SHA-256 42db00b2...)
#   z=15: K1065 uniform y>=6 family (verify_z15_y_ge6.py,
#         SHA-256 131e1c64...); the small-y transitional cells
#         (y,d) in {(6,0),(6,1),(6,2),(7,0),(6,3),(7,1)} are unreachable
#         at y=10, so the published generic rows apply as-is
#   z=16: K1077 uniform y>=6 family (verify_z16_y_ge6.py,
#         SHA-256 d07c3b0e...); unreachable transitional (y,d) cells
#         at y=10 likewise
#   z=17: K1087 uniform y>=6 family (verify_z17_y_ge6.py,
#         SHA-256 e49d24d2...); the S<17 / S==17 transitional branches
#         are unreachable at y=10 (S=x+10>=20)
# Every anchor was pre-validated against both raw engines at the y=10
# rows before incorporation (pre-flight box: z fixed, x=10..45,
# R<=x+z+30: 15,336 points, mismatch 0, both engines).
# ------------------------------------------------------------------



def _od(r, a, b):
    return r % 2 == 1 and a <= r <= b


def _ev(r, a, b):
    return r % 2 == 0 and a <= r <= b


def A8u(x, y, r):
    """K0999/K1000 published uniform form: H(R;(x,y);8), x>=y>=9."""
    if r == 0:
        return 0
    if r >= x + y + 9:
        return (x + y) % 2
    d = x - y
    t = (r in (1, 3, 5, 7) or
         (d == 2 and r == 2 * y + 5) or
         (d == 6 and r == 2 * y + 7) or
         (d == 9 and _od(r, 2 * y + 9, 2 * y + 17)) or
         (d >= 10 and r == 2 * y + 9))
    if t:
        return 2
    if d == 0:
        p = _od(r, 9, 2 * y + 3)
    elif d == 1:
        p = _od(r, 9, 2 * y + 9) or _ev(r, 2 * y + 6, 2 * y + 9)
    elif d == 2:
        p = _od(r, 9, 2 * y + 3)
    elif d == 3:
        p = _od(r, 9, 2 * y + 11) or _ev(r, 2 * y + 6, 2 * y + 11)
    elif d == 4:
        p = _od(r, 9, 2 * y + 5)
    elif d == 5:
        p = _od(r, 9, 2 * y + 13) or _ev(r, 2 * y + 8, 2 * y + 13)
    elif d == 6:
        p = _od(r, 9, 2 * y + 5)
    elif d == 7:
        p = _od(r, 9, 2 * y + 15) or _ev(r, 2 * y + 8, 2 * y + 15)
    elif d == 8:
        p = _od(r, 9, 2 * y + 7)
    elif d == 9:
        p = _od(r, 9, 2 * y + 7) or _ev(r, 2 * y + 10, 2 * y + 16)
    else:
        p = _od(r, 9, 2 * y + 7) or _ev(r, 2 * y + 10, x + y + 8)
    return 1 if p else 0


def A9u(x, y, r):
    """K1001 published uniform form: H(R;(x,y);9), x>=y>=9."""
    if r == 0:
        return 0
    if r >= x + y + 10:
        return (x + y) % 2
    d = x - y
    top = x + y + 9
    t = (r in (1, 3, 5, 7, 9) or
         (d == 1 and r == 2 * y + 5) or
         (d == 5 and r == 2 * y + 7) or
         (d == 9 and r == 2 * y + 9) or
         (d == 10 and _od(r, 2 * y + 9, 2 * y + 19)) or
         (d >= 11 and r == 2 * y + 9))
    if t:
        return 2
    if d == 10:
        p = _ev(r, 10, 2 * y + 8)
    elif d % 2 == 1:
        if d <= 3:
            p = _ev(r, 10, 2 * y + 6) or r >= 2 * y + 7
        elif d <= 7:
            p = _ev(r, 10, 2 * y + 8) or r >= 2 * y + 9
        elif d == 9:
            p = _ev(r, 10, 2 * y + 8) or r >= 2 * y + 10
        else:
            p = _ev(r, 10, 2 * y + 8) or _od(r, 2 * y + 11, top)
    else:
        if d <= 2:
            ht = 2 * y + 4
        elif d <= 6:
            ht = 2 * y + 6
        else:
            ht = 2 * y + 8
        if d >= 12:
            p = _ev(r, 10, ht) or _od(r, 2 * y + 11, top)
        else:
            p = _ev(r, 10, ht)
    return 1 if p else 0


def A10u(x, y, r):
    """K1002 uniform form restricted to y>=9 (K1011 proof scope):
    H(R;(x,y);10), x>=y>=9."""
    if r == 0:
        return 0
    S = x + y
    if r >= S + 11:
        return S % 2
    d = x - y
    t = (r in (1, 3, 5, 7, 9) or
         (d in (0, 4, 8) and r == 2 * y + 5 + d // 2) or
         (d == 11 and _od(r, 2 * y + 11, S + 10)) or
         (d >= 12 and r == 2 * y + 11))
    if t:
        return 2
    if d % 2 == 0 and d <= 10:
        p = _od(r, 11, 2 * y + 3 + 2 * ((d + 3) // 4))
    elif d % 2 == 0:
        p = _od(r, 11, 2 * y + 9) or _ev(r, 2 * y + 12, S + 10)
    elif d <= 9:
        p = _od(r, 11, S + 10) or _ev(r, 2 * y + 6 + 2 * ((d + 1) // 4), S + 9)
    else:
        p = _od(r, 11, 2 * y + 9) or _ev(r, 2 * y + 12, S + 9)
    return 1 if p else 0


def A15u(x, y, r):
    """K1065 published uniform form: H(R;(x,y);15), x>=y>=6.
    The (y,d) transitional cells are unreachable at y=10."""
    d = x - y
    Y = 2 * y
    S = x + y
    if r == 0:
        return 0
    if r >= S + 16:
        return S % 2
    t = (_od(r, 1, 15) or
         (d in (3, 7, 11, 15) and r == Y + (d + 15) // 2) or
         (d == 16 and _od(r, Y + 15, S + 15)) or
         (d >= 17 and r == Y + 15))
    if t:
        return 2
    if d % 2 == 0 and d <= 14:
        p = _ev(r, 16, Y + 6 + 2 * ((d + 3) // 4))
    elif d % 2 == 1 and d <= 15:
        p = (_ev(r, 16, S + 15) or _od(r, Y + 7 + 2 * ((d + 5) // 4), S + 14)
             or r >= S + 16)
    elif d == 16:
        p = _ev(r, 16, Y + 14)
    else:
        hi = S + (15 if d % 2 == 0 else 14)
        p = (_ev(r, 16, Y + 14) or _od(r, Y + 17, hi)
             or (d % 2 == 1 and r >= S + 16))
    return 1 if p else 0


def A16u(x, y, r):
    """K1077 published uniform form: H(R;(x,y);16), x>=y>=6.
    The (y,d) transitional cells are unreachable at y=10."""
    d = x - y
    Y = 2 * y
    S = x + y
    if r == 0:
        return 0
    if r >= S + 17:
        return S % 2
    t = (_od(r, 1, 15) or
         (d in (2, 6, 10, 14) and r == Y + (d + 16) // 2) or
         (d == 17 and _od(r, Y + 17, S + 16)) or
         (d >= 18 and r == Y + 17))
    if t:
        return 2
    if d % 2 == 0 and d <= 14:
        p = _od(r, 17, Y + 7 + 2 * (d // 4))
    elif d % 2 == 1 and d <= 15:
        p = (_od(r, 17, S + 16) or _ev(r, Y + 10 + 2 * ((d - 1) // 4), S + 15)
             or r >= S + 17)
    elif d == 16:
        p = _od(r, 17, Y + 15)
    elif d % 2 == 1:
        p = (_od(r, 17, Y + 15) or _ev(r, Y + 18, S + 15) or r >= S + 17)
    else:
        p = _od(r, 17, Y + 15) or _ev(r, Y + 18, S + 16)
    return 1 if p else 0


def A17u(x, y, r):
    """K1087 published uniform form: H(R;(x,y);17), x>=y>=6.
    T fully evaluated before P (value17 order); the S<17 and S==17
    transitional branches are unreachable at y=10 (S=x+10>=20)."""
    d = x - y
    Y = 2 * y
    S = x + y
    if r == 0:
        return 0
    if r >= S + 18:
        return S % 2
    if _od(r, 1, 17):
        return 2
    if d == 18 and _od(r, Y + 17, S + 17):
        return 2
    if d >= 19 and r == Y + 17:
        return 2
    if d % 2 == 1 and d % 4 == 1 and d <= 17 and r == Y + (d + 17) // 2:
        return 2
    if d >= 19:
        if _ev(r, 18, Y + 16):
            return 1
        if _od(r, Y + 19, S + 17):
            return 1
        if S % 2 == 1 and r >= S + 18:
            return 1
        return 0
    if d == 18:
        return 1 if _ev(r, 18, Y + 16) else 0
    if d % 2 == 1:
        rt = Y + (d + 17) // 2
        if d % 4 == 1:
            p = _ev(r, 18, rt - 1) or r >= rt + 1
        else:
            p = _ev(r, 18, rt - 2) or r >= rt
        return 1 if p else 0
    U = Y + 8 + 2 * (d // 4)
    return 1 if _ev(r, 18, U) else 0


ANCHORS = {8: A8u, 9: A9u, 10: A10u, 15: A15u, 16: A16u, 17: A17u}

def main():
    n = bad = 0
    first_bad = None
    per_z = {}
    for z0, fn in sorted(ANCHORS.items()):
        pz_n = pz_bad = 0
        for x in range(18, 46):
            for R in range(1, x + z0 + 31):
                n += 1
                pz_n += 1
                a = fn(x, 18, R)
                o = H_ordered(R, (x, 18), z0)
                c = H_canonical(R, (x, 18), z0)
                cf = cand18(z0, x, R)
                if a != o or a != c or a != cf:
                    bad += 1
                    pz_bad += 1
                    if first_bad is None:
                        first_bad = (z0, x, R, a, o, c, cf)
        per_z[z0] = {'points': pz_n, 'bad': pz_bad}
    n_low = bad_low = 0
    first_bad_low = None
    for z0 in (15, 16, 17):
        for x in range(18, 160):
            for R in range(1, z0 + 7):
                n_low += 1
                if cand18(z0, x, R) != single_token(x + 18, z0, R):
                    bad_low += 1
                    if first_bad_low is None:
                        first_bad_low = (z0, x, R)
    payload = {
        'check': 'preflight c1d y=18 rows: published z=8/9/10/15/16/17 uniform slice anchors vs raw engines vs cand18',
        'box': 'z0 in {8,9,10,15,16,17}; x=18..45; R=1..x+z0+30',
        'anchor_points': n,
        'anchor_bad': bad,
        'anchor_first_bad': first_bad,
        'per_z': per_z,
        'lowR_box': 'z0 in {15,16,17}; x=18..159; R=1..z0+6',
        'lowR_points': n_low,
        'lowR_bad': bad_low,
        'lowR_first_bad': first_bad_low,
        'overall': 'PASS' if bad == 0 and bad_low == 0 else 'FAIL',
    }
    out = Path(__file__).parent.parent / "output"
    out.mkdir(parents=True, exist_ok=True)
    (out / "preflight-c1d-y18.json").write_text(
        json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))
    return 0 if payload['overall'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
