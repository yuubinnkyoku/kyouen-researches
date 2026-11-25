#!/usr/bin/env python3
"""Second, independent verification of the published K1076 z=17, y=4
two-token boundary slice.

The fixed verification target is the PUBLISHED K1076 closed form, spliced
verbatim (byte-exact) from the repo main verifier verify_z17_y4.py at
commit 412d75b9 (git blob 911dc4bf, file sha256
a7878b8e40d116b6e5d25a6f94562a5584b8bc0374375868a1e4555a0f205d98).
The oracles are INDEPENDENT engines from a separate same-day derivation:
the order-preserving recursion H_ordered, the descending-canonical
recursion H_canonical, and the first derivation's own closed forms
(cand / cand_pred), all derived and audited independently of the K1076
publication. Both derivations agree with the published forms.

Checks:
- raw engines vs published parent closed form (finite box x<=60)
- published child transcriptions (g17y3/g16y4) vs raw recursion of the
  child positions (closes the anchor transcription risk)
- published signature band table: structural coverage, raw-engine
  signature agreement, mex mapping
- induction-step closure sweep against the published forms (x<=5000)
- height-only reduction (K0832 proven bound R<=18; finite observation
  to R<=21 with the sharpness witness x=14, R=22), general tail
- first independent derivation vs published forms (wide grid x<=2000,
  deep band-edge samples to x<=200000), fixed-seed scatter
"""
from __future__ import annotations
import hashlib, json, random
from functools import lru_cache
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

# ============ independent engines and first derivation (this session) ============
def mex(values):
    m=0; values=set(values)
    while m in values: m+=1
    return m

@lru_cache(None)
def H_ordered(R, X, z):
    if R==0: return 0
    opts=set()
    for i,v in enumerate(X):
        if v>1: opts.add(H_ordered(R-1,X[:i]+(v-1,)+X[i+1:],z))
        else: opts.add(H_ordered(R-1,X[:i]+X[i+1:],z+1))
    if z: opts.add(1^H_ordered(R-1,X,z-1))
    return mex(opts)

@lru_cache(None)
def H_canonical(R, X, z):
    X=tuple(sorted(X,reverse=True))
    if R==0: return 0
    opts=set(); i=0
    while i<len(X):
        v=X[i]
        if v>1:
            Y=tuple(sorted(X[:i]+(v-1,)+X[i+1:],reverse=True))
            opts.add(H_canonical(R-1,Y,z))
        else:
            Y=tuple(sorted(X[:i]+X[i+1:],reverse=True))
            opts.add(H_canonical(R-1,Y,z+1))
        while i+1<len(X) and X[i+1]==v: i+=1
        i+=1
    if z: opts.add(1^H_canonical(R-1,X,z-1))
    return mex(opts)

def O(a,b): return set(range(a+(a%2==0),b+1,2))
def E(a,b): return set(range(a+(a%2==1),b+1,2))
def I(a): return set(range(a,20000))

# ---------- parent closed form: z=17, y=4 ----------
BASE4={18,20,22,24}
def T(x):
    if x==4: return O(1,7)
    if x in (5,6): return O(1,9)
    if x in (7,8): return O(1,11)
    if x in (9,10): return O(1,13)
    if x in (11,12): return O(1,15)
    if x==13: return O(1,21)          # x+y=z row, continuous cap 21=2y+(d+z)/2 (d+z==2 mod 4)
    if x==17: return O(1,17)|{23}     # advance point, d+z=30==2 mod 4 lattice 2y+(d+z)/2
    if x==21: return O(1,17)|{25}     # pin row x=z+y: pin 25=2y+z (odd z)
    if x==22: return O(1,17)|O(25,43) # sweep row z+y+1: O[pin, x+y+z]
    if x>=23: return O(1,17)|{25}     # steady pin
    return O(1,17)

def P(x):
    if x in (4,6,8,10,12): return set()
    if x==5: return I(10)
    if x==7: return I(12)
    if x==9: return I(14)
    if x==11: return I(16)
    if x in (13,15): return {18,20}|I(22)
    if x==14: return {18,20}
    if x in (16,18): return {18,20,22}
    if x in (17,19): return {18,20,22}|I(24)
    if x in (20,22): return BASE4
    if x==21: return BASE4|I(26)
    if x%2: return BASE4|O(27,x+20)|I(x+22)
    return BASE4|O(27,x+21)

def cand(x,r):
    if r==0: return 0
    if r in T(x): return 2
    return 1 if r in P(x) else 0

def actual_sig(x,r):
    vals={H_ordered(r-1,(x-1,4),17),H_ordered(r-1,(x,3),17),1^H_ordered(r-1,(x,4),16)}
    return ''.join(map(str,sorted(vals)))

@lru_cache(None)
def single(x,z,r):
    if r==0 or (x==0 and z==0): return 0
    opts=set()
    if x>1: opts.add(single(x-1,z,r-1))
    elif x==1: opts.add(single(0,z+1,r-1))
    if z: opts.add(1^single(x,z-1,r-1))
    return mex(opts)

# Logic predicates mirroring the set-based closed forms exactly, O(1) membership.

def cand_pred(x,r):
    if r==0: return 0
    # --- T(x) ---
    if x==4: t=(r%2==1 and r<=7)
    elif x in (5,6): t=(r%2==1 and r<=9)
    elif x in (7,8): t=(r%2==1 and r<=11)
    elif x in (9,10): t=(r%2==1 and r<=13)
    elif x in (11,12): t=(r%2==1 and r<=15)
    elif x==13: t=(r%2==1 and r<=21)
    elif x==17: t=(r%2==1 and r<=17) or r==23
    elif x==21: t=(r%2==1 and r<=17) or r==25
    elif x==22: t=(r%2==1 and r<=17) or (r%2==1 and 25<=r<=43)
    elif x>=23: t=(r%2==1 and r<=17) or r==25
    else: t=(r%2==1 and r<=17)
    if t: return 2
    # --- P(x) ---
    if x in (4,6,8,10,12): return 0
    if x==5: return 1 if r>=10 else 0
    if x==7: return 1 if r>=12 else 0
    if x==9: return 1 if r>=14 else 0
    if x==11: return 1 if r>=16 else 0
    if x in (13,15): return 1 if (r in (18,20) or r>=22) else 0
    if x==14: return 1 if r in (18,20) else 0
    if x in (16,18): return 1 if r in (18,20,22) else 0
    if x in (17,19): return 1 if (r in (18,20,22) or r>=24) else 0
    if x in (20,22): return 1 if r in BASE4 else 0
    if x==21: return 1 if (r in BASE4 or r>=26) else 0
    if x%2: return 1 if (r in BASE4 or (r%2==1 and 27<=r<=x+20) or r>=x+22) else 0
    return 1 if (r in BASE4 or (r%2==1 and 27<=r<=x+21)) else 0

# ============ end independent engines ============

def run():
    c={'engine_ordered_vs_published':0,'engine_canonical_vs_published':0,'ordered_vs_canonical':0,
       'child_anchor_K1067':0,'child_anchor_K1064':0,
       'published_band_raw_signature':0,'published_band_coverage_rows':0,
       'tail_raw_vs_published':0,'height_only_proven':0,'height_only_observed':0,'height_only_witness':0,
       'first_derivation_vs_published':0,'deep_edge_agreement':0,
       'closure_base':0,'closure_sweep_published':0,'scatter':0}
    # 1. raw engines vs the published parent closed form on a finite box.
    for x in range(4,61):
        for r in range(x+47):
            v=parent_formula(x,r);a=H_ordered(r,(x,4),17);b=H_canonical(r,(x,4),17)
            assert a==v and b==v and a==b,(x,r,a,b,v)
            c['engine_ordered_vs_published']+=1;c['engine_canonical_vs_published']+=1;c['ordered_vs_canonical']+=1
    # 2. the published child transcriptions vs raw recursion of the child positions.
    for x in range(3,61):
        for r in range(x+47):
            v=g17y3(x,r)
            assert H_ordered(r,(x,3),17)==v and H_canonical(r,(x,3),17)==v,(x,r,v)
            c['child_anchor_K1067']+=2
    for x in range(4,61):
        for r in range(x+47):
            v=g16y4(x,r)
            assert H_ordered(r,(x,4),16)==v and H_canonical(r,(x,4),16)==v,(x,r,v)
            c['child_anchor_K1064']+=2
    # 3. the published signature band table vs raw-engine signatures, coverage, mex.
    mm={'01':2,'23':0,'03':1,'0':1,'1':0,'12':0,'13':0,'023':1,'123':0,'02':1}
    for x in range(4,96):
        for r in range(1,x+22):
            exp=expected_signature(x,r)
            got=actual_sig(x,r)
            assert exp is not None,(x,r,'coverage gap in published table')
            assert exp==got,(x,r,exp,got,'raw signature vs published table')
            assert mex(sorted(set(map(int,got))))==mm[got]==parent_formula(x,r),(x,r,got)
            c['published_band_raw_signature']+=1
        # structural coverage of the published table, per row-parity
        for par in (0,1):
            if x<=22: bands=SIG[x][par]
            elif par==1: bands=[(1,17,'01'),(19,23,'1'),(25,25,'01'),(27,x+(20 if (x&1) else 21),'0')]
            else: bands=[(2,16,'23'),(18,18,'02'),(20,22,'0'),(24,24,'02'),(26,26,'123'),(28,x+(21 if (x&1) else 20),'12' if x==23 else '1')]
            assert bands[0][0]==(1 if par else 2),(x,par)
            prev_hi=None
            for lo,hi2,s in bands:
                assert lo<=hi2 and (lo%2==par),(x,par,lo,hi2)
                if prev_hi is not None: assert lo==prev_hi+2,(x,par,lo,prev_hi)
                prev_hi=hi2
            exp_hi=(x+21) if ((x+21)%2==par) else (x+20)
            assert prev_hi==exp_hi,(x,par,prev_hi,exp_hi)
            c['published_band_coverage_rows']+=1
    # 4. general tail: raw engines match the published claim.
    for x in range(4,96):
        for r in range(x+22,x+67):
            assert H_ordered(r,(x,4),17)==(x+4)%2,(x,r)
            assert parent_formula(x,r)==(x+4)%2,(x,r)
            c['tail_raw_vs_published']+=1
    # 5. height-only reduction: proven to R<=18 (K0832), observed to R<=21.
    for x in range(4,96):
        for r in range(19):
            assert H_ordered(r,(x,4),17)==single(x+4,17,r)==parent_formula(x,r),(x,r)
            c['height_only_proven']+=1
        for r in range(19,22):
            assert H_ordered(r,(x,4),17)==single(x+4,17,r)==parent_formula(x,r),(x,r)
            c['height_only_observed']+=1
    # sharpness witness of the observed range (first failure x=14, R=22)
    assert H_ordered(22,(14,4),17)!=single(18,17,22)
    assert parent_formula(14,22)==H_ordered(22,(14,4),17)
    c['height_only_witness']=1
    # 6. the first independent derivation (this session) vs the published forms.
    for x in range(4,61):
        for r in range(x+47):
            assert cand(x,r)==parent_formula(x,r),(x,r,cand(x,r),parent_formula(x,r))
    for x in range(4,2001):
        for r in range(x+47):
            assert cand_pred(x,r)==parent_formula(x,r),(x,r)
            c['first_derivation_vs_published']+=1
    # 7. deep band-edge agreement between both derivations, x<=200000.
    for x in range(23,200001):
        for r in (x+22,x+30,x+40):
            assert cand_pred(x,r)==parent_formula(x,r)==(x+4)%2,(x,r)
            c['deep_edge_agreement']+=1
        for r in (17,18,20,22,24,25,26,27):
            assert cand_pred(x,r)==parent_formula(x,r),(x,r)
            c['deep_edge_agreement']+=1
        if x&1:
            for r in (x+20,x+21):
                assert cand_pred(x,r)==parent_formula(x,r),(x,r)
                c['deep_edge_agreement']+=1
        else:
            r=x+21
            assert cand_pred(x,r)==parent_formula(x,r),(x,r)
            c['deep_edge_agreement']+=1
    # 8. the induction step against the published forms (closure base + sweep).
    for r in range(1,26):
        assert parent_formula(4,r)==mex3(g17y3(4,r-1),g17y3(4,r-1),1^g16y4(4,r-1)),r
        c['closure_base']+=1
    for x in range(5,5001):
        for r in range(1,x+22):
            assert parent_formula(x,r)==mex3(parent_formula(x-1,r-1),g17y3(x,r-1),1^g16y4(x,r-1)),(x,r)
            c['closure_sweep_published']+=1
    # 9. fixed-seed scatter with raw engines.
    rng=random.Random(20261123)
    for _ in range(8000):
        x=rng.randint(4,90);r=rng.randint(0,x+55)
        a=H_ordered(r,(x,4),17);b=H_canonical(r,(x,4),17)
        assert a==b==parent_formula(x,r),(x,r,a,b)
        c['scatter']+=1
    return c

if __name__=='__main__':
    result=run();result['total_comparisons']=sum(result.values())
    result['finite_grid']='engines x=4..60 R<=x+46; bands x=4..95 R<=x+21; first-derivation x=4..2000 R<=x+46; deep edges x<=200000; closure sweep x<=5000'
    result['ordered_states']=H_ordered.cache_info().currsize
    result['canonical_states']=H_canonical.cache_info().currsize
    result['single_token_states']=single.cache_info().currsize
    result['published_target']='K1076 z=17 y=4 boundary slice, repo verify_z17_y4.py verbatim splice'
    result['published_verifier_sha256']=PUBLISHED_VERIFIER_SHA256
    result['published_block_sha256']=PUBLISHED_BLOCK_SHA256
    result['verifier_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (Path(__file__).parent/'output').mkdir(exist_ok=True)
    (Path(__file__).parent/'output'/'audit.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,sort_keys=True,indent=2))
