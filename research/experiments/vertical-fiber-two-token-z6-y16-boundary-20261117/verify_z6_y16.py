#!/usr/bin/env python3
"""Finite independent audit for the universally proved z=6, y=16 slice."""
from __future__ import annotations
import hashlib
import json
import random
from functools import lru_cache
from pathlib import Path


def mex(v):
    s = set(v)
    g = 0
    while g in s:
        g += 1
    return g


def O(r, a, b=None):
    return r >= a and (b is None or r <= b) and r % 2 == 1


def E(r, a, b=None):
    return r >= a and (b is None or r <= b) and r % 2 == 0


def h5(x, y, r):
    if r == 0:
        return 0
    s, d = x + y, x - y
    t = {1, 3, 5}
    if d == 1:
        t.add(2*y + 3)
    elif d == 5:
        t.add(2*y + 5)
    elif d == 6:
        t.update({2*y+5, 2*y+7, 2*y+9, 2*y+11})
    elif d >= 7:
        t.add(2*y + 5)
    if r in t:
        return 2
    if d == 0:
        p = E(r, 6, s+2)
    elif d == 1:
        p = E(r, 6, s+3) or r >= s+4
    elif d == 2:
        p = E(r, 6, s)
    elif d == 3:
        p = E(r, 6, s+1) or r >= s+2
    elif d == 4:
        p = E(r, 6, s)
    elif d == 5:
        p = E(r, 6, s-1) or r >= s+1
    elif d == 6:
        p = E(r, 6, s-2)
    elif d >= 7 and d % 2:
        p = E(r, 6, 2*y+4) or O(r, 2*y+7, s+4) or r >= s+6
    else:
        p = E(r, 6, 2*y+4) or O(r, 2*y+7, s+5)
    return int(p)


def h6y15(x, r):
    if r == 0:
        return 0
    t = {1, 3, 5}
    if x == 15:
        t.add(33)
    elif x == 19:
        t.add(35)
    elif x == 22:
        t.update({37, 39, 41, 43})
    elif x >= 23:
        t.add(37)
    if r in t:
        return 2
    if x == 15:
        p = O(r, 7, 31)
    elif x == 16:
        p = O(r, 7, 37) or E(r, 34, 36) or r >= 38
    elif x == 17:
        p = O(r, 7, 33)
    elif x == 18:
        p = O(r, 7, 39) or E(r, 36, 38) or r >= 40
    elif x == 19:
        p = O(r, 7, 33)
    elif x == 20:
        p = O(r, 7, 41) or E(r, 36, 40) or r >= 42
    elif x == 21:
        p = O(r, 7, 35)
    elif x == 22:
        p = O(r, 7, 35) or E(r, 38, 42) or r >= 44
    elif x % 2:
        p = O(r, 7, 35) or E(r, 38, x+21)
    else:
        p = O(r, 7, 35) or E(r, 38, x+20) or r >= x+22
    return int(p)


def h6y16(x, r):
    if x < 16:
        raise ValueError("x must be at least 16")
    if r == 0:
        return 0
    t = {1, 3, 5}
    if x == 16:
        t.add(35)
    elif x == 20:
        t.add(37)
    elif x == 23:
        t.update({39, 41, 43, 45})
    elif x >= 24:
        t.add(39)
    if r in t:
        return 2
    if x == 16:
        p = O(r, 7, 33)
    elif x == 17:
        p = O(r, 7, 35) or r >= 36
    elif x == 18:
        p = O(r, 7, 35)
    elif x == 19:
        p = O(r, 7, 35) or r >= 37
    elif x == 20:
        p = O(r, 7, 35)
    elif x == 21:
        p = O(r, 7, 35) or r >= 37
    elif x == 22:
        p = O(r, 7, 37)
    else:
        p = (O(r, 7, 37)
             or E(r, 40, x + (21 if x % 2 else 22))
             or (x % 2 == 1 and r >= x+23))
    return int(p)


@lru_cache(None)
def ordered(r, tokens, z):
    if r == 0:
        return 0
    v = []
    for i, t in enumerate(tokens):
        q = list(tokens)
        if t >= 2:
            q[i] = t-1
            zz = z
        else:
            q.pop(i)
            zz = z+1
        v.append(ordered(r-1, tuple(q), zz))
    if z:
        v.append(1 ^ ordered(r-1, tokens, z-1))
    return mex(v)


@lru_cache(None)
def canonical(r, tokens, z):
    if r == 0:
        return 0
    v = []
    for i, t in enumerate(tokens):
        q = list(tokens)
        if t >= 2:
            q[i] = t-1
            zz = z
        else:
            q.pop(i)
            zz = z+1
        v.append(canonical(r-1, tuple(sorted(q, reverse=True)), zz))
    if z:
        v.append(1 ^ canonical(r-1, tuple(sorted(tokens, reverse=True)), z-1))
    return mex(v)


# Each row list contains (inclusive lower, inclusive upper, signature digits).
SIG = {
 16: ([(1,5,"01"),(7,33,"0"),(35,35,"01"),(37,37,"1")],
      [(2,6,"23"),(8,38,"1")]),
 17: ([(1,5,"01"),(7,39,"0")],
      [(2,6,"23"),(8,34,"1"),(36,36,"023"),(38,38,"0")]),
 18: ([(1,5,"01"),(7,35,"0"),(37,39,"1")],
      [(2,6,"23"),(8,40,"1")]),
 19: ([(1,5,"01"),(7,41,"0")],
      [(2,6,"23"),(8,34,"1"),(36,36,"12"),(38,40,"0")]),
 20: ([(1,5,"01"),(7,35,"0"),(37,37,"01"),(39,41,"1")],
      [(2,6,"23"),(8,42,"1")]),
 21: ([(1,5,"01"),(7,43,"0")],
      [(2,6,"23"),(8,36,"1"),(38,38,"023"),(40,42,"0")]),
 22: ([(1,5,"01"),(7,37,"0"),(39,43,"1")],
      [(2,6,"23"),(8,36,"1"),(38,44,"123")]),
 23: ([(1,5,"01"),(7,37,"0"),(39,45,"01")],
      [(2,6,"23"),(8,36,"1"),(38,38,"123"),(40,44,"0")]),
 24: ([(1,5,"01"),(7,37,"0"),(39,39,"01"),(41,45,"1")],
      [(2,6,"23"),(8,36,"1"),(38,38,"123"),(40,46,"02")]),
}


def expected_signature(x, r):
    if x <= 24:
        rows = SIG[x][0 if r % 2 else 1]
    elif r % 2:
        hi = x+21 if x % 2 == 0 else x+22
        rows = [(1,5,"01"),(7,37,"0"),(39,39,"01"),(41,hi,"1")]
    else:
        hi = x+22 if x % 2 == 0 else x+21
        rows = [(2,6,"23"),(8,36,"1"),(38,38,"123"),
                (40,40,"02"),(42,hi,"0")]
    for lo, hi, digits in rows:
        if lo <= r <= hi and (r-lo) % 2 == 0:
            return tuple(int(c) for c in digits)
    return None


def actual_signature(x, r):
    a = h6y15(16, r-1) if x == 16 else h6y16(x-1, r-1)
    b = h6y15(x, r-1)
    c = 1 ^ h5(x, 16, r-1)
    return tuple(sorted({a, b, c}))


def value2_set(x):
    t = {1, 3, 5}
    if x == 16:
        t.add(35)
    elif x == 20:
        t.add(37)
    elif x == 23:
        t.update({39, 41, 43, 45})
    elif x >= 24:
        t.add(39)
    return t


def family_value2(x):
    d = x-16
    t = {1, 3, 5}
    if d <= 6 and d % 2 == 0 and (6+d) % 4 == 2:
        t.add(32 + (6+d)//2)  # EXT; y*=(6-d)/2 <= 16
    elif d == 7:
        t.update({39, 41, 43, 45})
    elif d >= 8:
        t.add(39)
    return t


def run_audit():
    failures = []
    direct = 0
    for x in range(16, 81):
        for r in range(x+51):
            for z, tokens, formula in (
                (6, (x,16), h6y16(x,r)),
                (6, (x,15), h6y15(x,r)),
                (5, (x,16), h5(x,16,r)),
            ):
                a = ordered(r, tokens, z)
                b = canonical(r, tuple(sorted(tokens, reverse=True)), z)
                direct += 1
                if a != b or a != formula:
                    failures.append({"kind":"direct","x":x,"r":r,"z":z,
                                     "ordered":a,"canonical":b,"formula":formula})

    signatures = mex_checks = odd_bounds = even_bounds = 0
    loci = families = 0
    for x in range(16, 2001):
        observed = set()
        for r in range(1, x+23):  # all parents before the general tail
            a = actual_signature(x, r)
            e = expected_signature(x, r)
            signatures += 1
            if a != e:
                failures.append({"kind":"signature","x":x,"r":r,
                                 "actual":a,"expected":e})
            g = mex(a)
            mex_checks += 1
            if g != h6y16(x,r):
                failures.append({"kind":"mex","x":x,"r":r,
                                 "actual":g,"formula":h6y16(x,r)})
            if g == 2:
                observed.add(r)
            if r % 2:
                odd_bounds += 1
                if not set(a).issubset({0,1}):
                    failures.append({"kind":"odd-bound","x":x,"r":r,"options":a})
            else:
                even_bounds += 1
                if g > 1:
                    failures.append({"kind":"even-bound","x":x,"r":r,"value":g})
        t = value2_set(x)
        loci += 1
        if observed != t:
            failures.append({"kind":"value2-locus","x":x,
                             "actual":sorted(observed),"expected":sorted(t)})
        families += 1
        f = family_value2(x)
        if t != f:
            failures.append({"kind":"three-family","x":x,
                             "actual":sorted(t),"predicted":sorted(f)})

    tail = 0
    for x in range(16, 2001):
        for k in range(65):
            r = x+23+k
            tail += 1
            if h6y16(x,r) != (x+16) % 2:
                failures.append({"kind":"tail","x":x,"r":r,
                                 "actual":h6y16(x,r),"expected":(x+16)%2})
    rng = random.Random(20261117)
    far = 0
    for _ in range(2000):
        x = rng.randint(16,100000)
        r = x+23+rng.randint(0,100000)
        far += 1
        if h6y16(x,r) != (x+16) % 2:
            failures.append({"kind":"far-tail","x":x,"r":r})

    counts = {
        "direct_ordered_canonical_formula_anchors": direct,
        "option_signatures": signatures,
        "mex_identity": mex_checks,
        "odd_parent_bounds": odd_bounds,
        "even_parent_bounds": even_bounds,
        "value2_locus": loci,
        "three_family_specialization": families,
        "tail": tail,
        "fixed_seed_far_tail": far,
    }
    return {
        "schema":"two-token-z6-y16-audit-v1",
        "claim":"H(R;(x,16);6) is given by the complete formula for all x>=16,R>=0",
        "classification":"finite-independent-audit-not-proof",
        "counts":counts,
        "total_checks":sum(counts.values()),
        "seed":20261117,
        "failures":failures,
        "pass":not failures,
    }


def main():
    audit = run_audit()
    base = json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    audit["sha256_without_hash_field"] = hashlib.sha256(base.encode("utf-8")).hexdigest()
    encoded = json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    out = Path(__file__).resolve().parent / "output" / "audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(encoded, encoding="utf-8")
    print(json.dumps({"pass":audit["pass"],"total_checks":audit["total_checks"],
                      "failures":len(audit["failures"]),"counts":audit["counts"],
                      "sha256_without_hash_field":audit["sha256_without_hash_field"]},
                     ensure_ascii=False,sort_keys=True))
    if not audit["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
