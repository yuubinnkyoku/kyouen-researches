#!/usr/bin/env python3
"""Finite audit of the z=5 two-token R-induction option-signature table."""
from __future__ import annotations
import json
from pathlib import Path


def mex(values):
    value = 0
    while value in values:
        value += 1
    return value


def ev(r, lo, hi):
    return r % 2 == 0 and lo <= r <= hi


def od(r, lo, hi):
    return r % 2 == 1 and lo <= r <= hi


def h4(x, y, r):
    if r == 0:
        return 0
    s, d = x + y, x - y
    if (x, y) == (1, 1):
        t = {1}
    elif d == 2:
        t = {1, 3, 2*y+3}
    elif d == 5:
        t = {1, 3, s, s+2, s+4}
    elif d >= 6:
        t = {1, 3, 2*y+5}
    elif d == 0 and y == 2:
        t = {1, 3, s+1}
    else:
        t = {1, 3}
    if r in t:
        return 2
    if d == 0:
        p = od(r, 5, s+1) and r not in t
    elif d == 1:
        p = od(r, 5, 2*y+3) or r >= 2*y+4 or ((x, y) == (2, 1) and r == 4)
    elif d == 2:
        p = od(r, 5, 2*y+1)
    elif d == 3:
        p = od(r, 5, 2*y+3) or r >= 2*y+4
    elif d == 4:
        p = od(r, 5, 2*y+3)
    elif d >= 5 and d % 2:
        p = od(r, 5, 2*y+3) or ev(r, 2*y+6, s+5) or r >= s+6
    else:
        p = od(r, 5, 2*y+3) or ev(r, 2*y+6, s+4)
    return int(p)


def h5(x, y, r):
    if r == 0:
        return 0
    s, d = x+y, x-y
    if d == 0:
        t = {1} if y == 1 else ({1,3} if y == 2 else {1,3,5})
    elif d == 1:
        t = {1,3} if y == 1 else {1,3,5,2*y+3}
    elif d == 2:
        t = {1,3} if y == 1 else {1,3,5}
    elif d in (3,4):
        t = {1,3,5}
    elif d == 5:
        t = {1,3,5,2*y+5}
    elif d == 6:
        t = {1,3,5,2*y+5,2*y+7,2*y+9,2*y+11}
    else:
        t = {1,3,5,2*y+5}
    if r in t:
        return 2
    if d == 0:
        p = y >= 3 and ev(r, 6, s+2)
    elif d == 1:
        p = (r >= 4) if y == 1 else (ev(r, 6, s+3) or r >= s+4)
    elif d == 2:
        p = y >= 2 and ev(r, 6, s)
    elif d == 3:
        p = ev(r, 6, s+1) or r >= s+2
    elif d == 4:
        p = ev(r, 6, s)
    elif d == 5:
        p = ev(r, 6, s-1) or r >= s+1
    elif d == 6:
        p = ev(r, 6, s-2)
    elif d >= 7 and d % 2:
        p = ev(r, 6, 2*y+4) or od(r, 2*y+7, s+4) or r >= s+6
    else:
        p = ev(r, 6, 2*y+4) or od(r, 2*y+7, s+5)
    return int(p)


def sigma_expected(d, y, r):
    if r % 2 == 0:
        if r in (2,4):
            return frozenset()
        if d == 0:
            return frozenset({1}) if y == 2 or r > 2*y+2 else frozenset({0})
        if d == 1 or d == 3 or d == 5:
            return frozenset({0})
        if d == 2:
            return frozenset({0}) if r <= 2*y+2 else frozenset({1})
        if d == 4:
            return frozenset({0}) if r <= 2*y+4 else frozenset({1})
        if d == 6:
            return frozenset({0}) if r <= 2*y+4 else frozenset({1})
        s = 2*y+d
        if r <= 2*y+4 or (d % 2 and r >= s+6):
            return frozenset({0})
        return frozenset({1})
    if d == 0:
        return frozenset({0,1}) if r in ((1,3) if y == 2 else (1,3,5)) else frozenset({1})
    if d == 1:
        if r in (1,3,5,2*y+3): return frozenset({0,1})
        if 7 <= r <= 2*y+1: return frozenset({1})
        if r >= 2*y+5: return frozenset({0})
        raise AssertionError((d,y,r))
    if d == 2 or d == 4:
        return frozenset({0,1}) if r in (1,3,5) else frozenset({1})
    if d == 3:
        if r in (1,3,5): return frozenset({0,1})
        return frozenset({1}) if r <= 2*y+3 else frozenset({0})
    if d == 5:
        s = 2*y+5
        if r in (1,3,5,s): return frozenset({0,1})
        return frozenset({1}) if r <= s-2 else frozenset({0})
    if d == 6:
        special = {1,3,5,2*y+5,2*y+7,2*y+9,2*y+11}
        return frozenset({0,1}) if r in special else frozenset({1})
    s = 2*y+d
    if r in (1,3,5,2*y+5): return frozenset({0,1})
    if 7 <= r <= 2*y+3: return frozenset({1})
    if d % 2:
        return frozenset({0}) if r >= 2*y+7 else frozenset()
    if 2*y+7 <= r <= s+5: return frozenset({0})
    if r >= s+7: return frozenset({1})
    raise AssertionError((d,y,r))


def options(x, y, r):
    if r == 0:
        return set()
    a = tuple(sorted((x-1,y), reverse=True))
    b = tuple(sorted((x,y-1), reverse=True))
    return {h5(a[0],a[1],r-1), h5(b[0],b[1],r-1), 1 ^ h4(x,y,r-1)}


def y1_formula(x, r):
    if r == 0: return 0
    if x == 1: return 2 if r == 1 else 0
    if x in (2,3): t = {1,3}
    elif x in (4,5): t = {1,3,5}
    elif x == 6: t = {1,3,5,7}
    elif x == 7: t = {1,3,5,7,9,11,13}
    else: t = {1,3,5,7}
    if r in t: return 2
    if x == 2: return int(r >= 4)
    if x == 3: return 0
    if x == 4: return int(r >= 6)
    if x == 5: return int(r == 6)
    if x == 6: return int(r == 6 or r >= 8)
    if x == 7: return int(r == 6)
    if x >= 8 and x % 2 == 0:
        return int(r == 6 or (r % 2 and 9 <= r <= x+5) or r >= x+7)
    return int(r == 6 or (r % 2 and 9 <= r <= x+6))


def audit(d_max=80, y_max=80):
    checks = {
        "small_d_signature_states": 0, "large_d_signature_states": 0,
        "sigma_mismatches": 0, "mex_mismatches": 0,
        "odd_option_above_one": 0, "even_parent_above_one": 0,
        "y1_boundary_formula_checks": 0, "y1_boundary_formula_mismatches": 0,
        "tail_checks": 0, "tail_mismatches": 0,
    }
    bad = []
    for d in range(d_max+1):
        for y in range(2,y_max+1):
            x, s = y+d, 2*y+d
            for r in range(1,s+13):
                v = options(x,y,r)
                sig = frozenset(v & {0,1})
                exp = sigma_expected(d,y,r)
                checks["small_d_signature_states" if d <= 6 else "large_d_signature_states"] += 1
                if sig != exp:
                    checks["sigma_mismatches"] += 1
                    if len(bad)<10: bad.append(["sigma",d,y,r,sorted(v),sorted(sig),sorted(exp)])
                pred = h5(x,y,r)
                if mex(v) != pred:
                    checks["mex_mismatches"] += 1
                    if len(bad)<10: bad.append(["mex",d,y,r,sorted(v),mex(v),pred])
                if r%2 and any(a>1 for a in v):
                    checks["odd_option_above_one"] += 1
                    if len(bad)<10: bad.append(["odd-high",d,y,r,sorted(v)])
                if r%2 == 0 and pred>1:
                    checks["even_parent_above_one"] += 1
                    if len(bad)<10: bad.append(["even-high",d,y,r,pred])
                if r >= s+6:
                    checks["tail_checks"] += 1
                    if pred != (s&1):
                        checks["tail_mismatches"] += 1
                        if len(bad)<10: bad.append(["tail",d,y,r,pred,s&1])
    for x in range(1,2001):
        for r in range(x+10):
            checks["y1_boundary_formula_checks"] += 1
            if h5(x,1,r) != y1_formula(x,r):
                checks["y1_boundary_formula_mismatches"] += 1
                if len(bad)<10: bad.append(["y1",x,r,h5(x,1,r),y1_formula(x,r)])
    failures = [k for k,v in checks.items() if (k.endswith("_mismatches") or k.endswith("_above_one")) and v]
    return {
        "target":"two-token z=5 full Grundy classification",
        "status":"proved-by-R-strong-induction; finite-audit-is-independent-check",
        "proof_basis":[
            "proved y=1 boundary slice",
            "proved z=4 full two-token slice",
            "Theorem T: H<=2 and even-R H<=1",
            "A/A/C option recurrence and the sigma=V intersect {0,1} table"
        ],
        "domain":{
            "induction_table_grid":f"0<=d<= {d_max}, 2<=y<= {y_max}, 1<=R<=2y+d+12",
            "y1_boundary_formula_grid":"1<=x<=2000, 0<=R<=x+9"
        },
        "checks":checks,"first_mismatches":bad,"all_checks_pass":not failures
    }


def main():
    result = audit()
    out = Path(__file__).resolve().parent / "output" / "audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(out.read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    main()
