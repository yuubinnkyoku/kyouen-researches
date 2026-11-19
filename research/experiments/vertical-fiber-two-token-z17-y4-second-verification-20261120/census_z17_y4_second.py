#!/usr/bin/env python3
"""Third independent census of the z=17, y=4 boundary slice, checked against
the PUBLISHED K1076 closed form (verbatim splice of repo verify_z17_y4.py at
commit 412d75b9, sha256 a7878b8e40d116b6e5d25a6f94562a5584b8bc0374375868a1e4555a0f205d98).

Engine H3 is a third implementation written from scratch against the game
definition: it enumerates moves by DISTINCT TOKEN VALUE on a canonical
sorted multiset with an explicit dict memo (no lru_cache). It knows nothing
about the published closed form; its output is compared with the published
predicates row by row for x=4..45, R=0..x+45.
"""
import hashlib
from pathlib import Path

PUBLISHED_VERIFIER_SHA256 = "a7878b8e40d116b6e5d25a6f94562a5584b8bc0374375868a1e4555a0f205d98"
PUBLISHED_BLOCK_SHA256 = "73435e45844749abccea98706df60146652dbb7e6d5a2a2a7a9104da505a4cf4"

# ============ PUBLISHED K1076 CLOSED FORMS (verbatim, byte-exact splice) ============
def odd(r: int, a: int, b: int) -> bool:
    return a <= r <= b and (r & 1) == 1

def even(r: int, a: int, b: int) -> bool:
    return a <= r <= b and (r & 1) == 0

def g17y3(x: int, r: int) -> int:
    # K1067: z=17, y=3
    t = False
    if x == 3: t = odd(r, 1, 5)
    elif x in (4, 5): t = odd(r, 1, 7)
    elif x in (6, 7): t = odd(r, 1, 9)
    elif x in (8, 9): t = odd(r, 1, 11)
    elif x in (10, 11): t = odd(r, 1, 13)
    elif x in (12, 13): t = odd(r, 1, 15)
    elif x == 14: t = odd(r, 1, 19)
    elif 15 <= x <= 20: t = odd(r, 1, 17)
    elif x >= 22: t = odd(r, 1, 17) or r == 23
    if x == 16 and r == 21: t = True
    if x == 20 and r == 23: t = True
    if x == 21 and (odd(r, 1, 17) or odd(r, 23, 41)): t = True
    if t: return 2

    p = False
    if x in (4, 6, 8, 10, 12):
        p = r >= x + 4
    elif x == 14:
        p = r == 18 or r >= 20
    elif x in (15, 17):
        p = r in (18, 20)
    elif x in (16, 18):
        p = r in (18, 20) or r >= 22
    elif x in (19, 21):
        p = r in (18, 20, 22)
    elif x == 20:
        p = r in (18, 20, 22) or r >= 24
    elif x >= 23 and (x & 1):
        p = r in (18, 20, 22) or odd(r, 25, x + 20)
    elif x >= 22 and not (x & 1):
        p = r in (18, 20, 22) or odd(r, 25, x + 19) or r >= x + 21
    if p: return 1
    return 0

def g16y4(x: int, r: int) -> int:
    # K1064: z=16, y=4
    t = False
    if x == 4: t = odd(r, 1, 7)
    elif x in (5, 6): t = odd(r, 1, 9)
    elif x in (7, 8): t = odd(r, 1, 11)
    elif x in (9, 10): t = odd(r, 1, 13)
    elif x == 11: t = odd(r, 1, 15)
    elif x == 12: t = odd(r, 1, 19)
    elif 13 <= x <= 21: t = odd(r, 1, 15)
    elif x >= 22: t = odd(r, 1, 15) or r == 25
    if x == 14 and r == 21: t = True
    if x == 18 and r == 23: t = True
    if x == 21 and odd(r, 25, 41): t = True
    if t: return 2

    p = False
    if x in (5, 7, 9, 11):
        p = r >= x + 5
    elif x in (13, 15):
        p = r in (17, 19) or r >= 21
    elif x == 14:
        p = r in (17, 19)
    elif x in (16, 18):
        p = r in (17, 19, 21)
    elif x in (17, 19):
        p = r in (17, 19, 21) or r >= 23
    elif x == 20:
        p = r in (17, 19, 21, 23)
    elif x >= 21 and (x & 1):
        p = (r in (17, 19, 21, 23) or even(r, 26, x + 19)
             or r >= x + 21)
    elif x >= 22 and not (x & 1):
        p = r in (17, 19, 21, 23) or even(r, 26, x + 20)
    if p: return 1
    return 0

def in_parent_T(x: int, r: int) -> bool:
    if x == 4: return odd(r, 1, 7)
    if x in (5, 6): return odd(r, 1, 9)
    if x in (7, 8): return odd(r, 1, 11)
    if x in (9, 10): return odd(r, 1, 13)
    if x in (11, 12): return odd(r, 1, 15)
    if x == 13: return odd(r, 1, 21)
    if x in (14, 15, 16, 17, 18, 19, 20): return odd(r, 1, 17) or (x == 17 and r == 23)
    if x == 21: return odd(r, 1, 17) or r == 25
    if x == 22: return odd(r, 1, 17) or odd(r, 25, 43)
    return odd(r, 1, 17) or r == 25

def in_parent_P(x: int, r: int) -> bool:
    if x == 5: return r >= 10
    if x == 7: return r >= 12
    if x == 9: return r >= 14
    if x == 11: return r >= 16
    if x == 13: return r in (18, 20, 22) or r >= 23
    if x == 14: return r in (18, 20)
    if x == 15: return r in (18, 20, 22) or r >= 23
    if x == 16: return r in (18, 20, 22)
    if x == 17: return r in (18, 20, 22, 24) or r >= 25
    if x == 18: return r in (18, 20, 22)
    if x == 19: return r in (18, 20, 22, 24) or r >= 25
    if x == 20: return r in (18, 20, 22, 24)
    if x == 21: return r in (18, 20, 22, 24) or r >= 26
    if x == 22: return r in (18, 20, 22, 24)
    if x >= 23:
        base = r in (18, 20, 22, 24)
        if x & 1:
            return base or odd(r, 27, x + 20) or r >= x + 22
        return base or odd(r, 27, x + 21)
    return False

def parent_formula(x: int, r: int) -> int:
    if in_parent_T(x, r): return 2
    if in_parent_P(x, r): return 1
    return 0

def mex3(a: int, b: int, c: int) -> int:
    s = {a, b, c}
    g = 0
    while g in s: g += 1
    return g

def signature(x: int, r: int) -> str:
    if x == 4:
        a = g17y3(4, r - 1)
    else:
        a = parent_formula(x - 1, r - 1)
    b = g17y3(x, r - 1)
    c = 1 ^ g16y4(x, r - 1)
    return ''.join(str(v) for v in sorted({a, b, c}))

# Each row stores inclusive arithmetic-progression bands (lo, hi, signature).
SIG = {
4:  ({1:[(1,7,'01'),(9,25,'1')], 0:[(2,8,'23'),(10,24,'1')]}),
5:  ({1:[(1,9,'01'),(11,25,'0')], 0:[(2,8,'23'),(10,10,'03'),(12,26,'0')]}),
6:  ({1:[(1,9,'01'),(11,27,'1')], 0:[(2,10,'23'),(12,26,'1')]}),
7:  ({1:[(1,11,'01'),(13,27,'0')], 0:[(2,10,'23'),(12,12,'03'),(14,28,'0')]}),
8:  ({1:[(1,11,'01'),(13,29,'1')], 0:[(2,12,'23'),(14,28,'1')]}),
9:  ({1:[(1,13,'01'),(15,29,'0')], 0:[(2,12,'23'),(14,14,'03'),(16,30,'0')]}),
10: ({1:[(1,13,'01'),(15,31,'1')], 0:[(2,14,'23'),(16,30,'1')]}),
11: ({1:[(1,15,'01'),(17,31,'0')], 0:[(2,14,'23'),(16,16,'03'),(18,32,'0')]}),
12: ({1:[(1,15,'01'),(17,33,'1')], 0:[(2,16,'23'),(18,20,'13'),(22,32,'1')]}),
13: ({1:[(1,21,'01'),(23,33,'0')], 0:[(2,16,'23'),(18,34,'0')]}),
14: ({1:[(1,17,'01'),(19,35,'1')], 0:[(2,16,'23'),(18,20,'02'),(22,22,'123'),(24,34,'1')]}),
15: ({1:[(1,17,'01'),(19,21,'1'),(23,35,'0')], 0:[(2,16,'23'),(18,18,'02'),(20,36,'0')]}),
16: ({1:[(1,17,'01'),(19,37,'1')], 0:[(2,16,'23'),(18,18,'02'),(20,20,'0'),(22,22,'02'),(24,36,'1')]}),
17: ({1:[(1,17,'01'),(19,21,'1'),(23,23,'01'),(25,37,'0')], 0:[(2,16,'23'),(18,18,'02'),(20,38,'0')]}),
18: ({1:[(1,17,'01'),(19,39,'1')], 0:[(2,16,'23'),(18,18,'02'),(20,22,'0'),(24,24,'123'),(26,38,'1')]}),
19: ({1:[(1,17,'01'),(19,23,'1'),(25,39,'0')], 0:[(2,16,'23'),(18,18,'02'),(20,40,'0')]}),
20: ({1:[(1,17,'01'),(19,41,'1')], 0:[(2,16,'23'),(18,18,'02'),(20,22,'0'),(24,24,'02'),(26,40,'1')]}),
21: ({1:[(1,17,'01'),(19,23,'1'),(25,25,'01'),(27,41,'0')], 0:[(2,16,'23'),(18,18,'02'),(20,22,'0'),(24,24,'02'),(26,42,'023')]}),
22: ({1:[(1,17,'01'),(19,23,'1'),(25,43,'01')], 0:[(2,16,'23'),(18,18,'02'),(20,22,'0'),(24,24,'02'),(26,26,'123'),(28,42,'1')]}),
}

def expected_signature(x: int, r: int) -> str | None:
    parity = r & 1
    if x <= 22:
        for lo, hi, sig in SIG[x][parity]:
            if lo <= r <= hi and ((r - lo) & 1) == 0:
                return sig
        return None
    if parity:
        bands = [(1,17,'01'),(19,23,'1'),(25,25,'01'),
                 (27,x + (20 if x & 1 else 21),'0')]
    else:
        last_sig = '12' if x == 23 else '1'
        bands = [(2,16,'23'),(18,18,'02'),(20,22,'0'),
                 (24,24,'02'),(26,26,'123'),
                 (28,x + (21 if x & 1 else 20),last_sig)]
    for lo, hi, sig in bands:
        if lo <= r <= hi and ((r - lo) & 1) == 0:
            return sig
    return None
# ============ END PUBLISHED K1076 BLOCK ============

# ============ third independent engine (this session) ============
def H3(r, tokens, z):
    if r == 0: return 0
    key = (r, tokens, z)
    v = H3.memo.get(key)
    if v is not None: return v
    opts = set()
    prev = None
    for tok in tokens:               # tokens sorted ascending, distinct values
        if tok == prev: continue     # enumerate distinct values once
        prev = tok
        if tok > 1:
            child = list(tokens); child.remove(tok); child.append(tok - 1)
            opts.add(H3(r - 1, tuple(sorted(child)), z))
        else:                        # remove, z grows
            child = list(tokens); child.remove(tok)
            opts.add(H3(r - 1, tuple(sorted(child)), z + 1))
    if z > 0:
        opts.add(1 ^ H3(r - 1, tokens, z - 1))
    res = 0
    while res in opts: res += 1
    H3.memo[key] = res
    return res
H3.memo = {}

# ============ end third engine ============

def main():
    lines = []
    checks = 0
    mismatch = 0
    for x in range(4, 46):
        tvals, pvals = [], []
        for r in range(0, x + 46):
            v = H3(r, (min(x, 4), max(x, 4)), 17)
            checks += 1
            if v != parent_formula(x, r):
                mismatch += 1
            if v == 2: tvals.append(r)
            elif v == 1: pvals.append(r)
        lines.append("x=%d T=%s" % (x, tvals))
        lines.append("x=%d P=%s" % (x, pvals))
    digest = hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()
    out = "\n".join(lines) + "\n"
    out += "checks=%d\n" % checks
    out += "mismatch_vs_published=%d\n" % mismatch
    out += "status=%s\n" % ("PASS" if mismatch == 0 else "FAIL")
    out += "census_sha256=%s\n" % digest
    out += "published_target=K1076 repo verify_z17_y4.py splice, sha256 %s\n" % PUBLISHED_VERIFIER_SHA256
    out += "published_block_sha256=%s\n" % PUBLISHED_BLOCK_SHA256
    (Path(__file__).parent / "output").mkdir(exist_ok=True)
    (Path(__file__).parent / "output" / "census.txt").write_text(out, encoding="utf-8")
    H3.memo.clear()
    print("checks=%d mismatch=%d status=%s" % (checks, mismatch, "PASS" if mismatch == 0 else "FAIL"))

main()
