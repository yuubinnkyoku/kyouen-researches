#!/usr/bin/env python3
"""ncw-class-enum: SYMBOLIC CLASS-ENUMERATION CLOSURE CERTIFICATE for the
K1310 non-congruent window collapse (T-NCW-P / T-NCW-B). Evidence addition
to the published K1310 package; NOT a new theorem.

What this certifies (all three layers machine-checked, deterministic):
  1. PARTITION: the domain cells (z >= 2, k in [1, z-1] with
     k not congruent z mod 2, m >= 1, g >= 1 for pairs; a >= 1 for beds)
     are partitioned by label classes built ONLY from comparison bits:
       pair: pz (z parity), pg (g parity), gs in {<=-1, 0, >=1} (sign of
             z-2k = g*), ggs in {<=gs-2, gs-1, gs, gs+1, >=gs+2},
             gzs in {<=z-3, z-2, z-1, z, z+1, >=z+2},
             tau in {<=z-2, z-1, z, z+1, z+2, z+3, >=z+4} for tau=2m+g,
             and the exact-boundary bits m1 (m==1), g1 (g==1), k1 (k==1);
       bed:  pz, gs 5-class {<=-2, -1, 0, 1, >=2}, tb 5-class
             {<=z-2, z-1, z, z+1, >=z+2} for tb=2a, a1 (a==1), k1.
     Every realizable label combination HAS a concrete witness (searched;
     Box lemma: consistent difference-bound combos occur at small
     coordinates) -> 280 pair classes + 39 bed classes.
  2. DETERMINATION + CLOSURE: for every class, the claim (T-NCW-P for
     pairs / T-NCW-B for beds) and ALL THREE typed child values (A-fall /
     B-exit single token / A-compress or corner bed / C-child with the
     concession flip 1^, or the K1303 band row at k=1) are computed
     SYMBOLICALLY from the class bits alone; mex(children) == claim is
     verified per class. Since labels are functions of the cell and the
     children are functions of the labels, per-class closure + partition
     proves the mex-closure layer of the K1310 hand proof (note SS2.4 /
     SS2.5 region algebra) for ALL cells, by finite case analysis
     (280 + 39 machine cases).
  3. GROUNDING (finite, not part of the universal skeleton): a coverage
     census derives each concrete cell's labels, recomputes claim +
     typed children from the labels, and requires agreement with the
     transcribed laws AND the class-table values AND mex closure; also
     every census cell's label combo must hit an enumerated class
     (partition completeness at census depth). Default census
     z<=30, m<=12, g<=40, a<=14: 108,000 pair + 3,150 bed cells.
     Deep census via argv ZM MM GM AM (e.g. 34 16 44 20).

Law transcriptions are byte-equivalent to the published, engine-audited
K1310 kit verify_k1310.py (P == pairLaw, Bm == bedLaw, single_token,
cpsfG/f0/g1/Lw/sw/Tw identical); the engine grounding of those laws is
the published 51,439-point official audit. This script never imports an
engine: it certifies the closure algebra, not the law values.

Exit gate: prints a RESULT line; rc=0 iff every bad count and the
missing-class count are 0 (fail-closed for tampering).
"""
import sys

IND = lambda b: 1 if b else 0


# ---------------- concrete law implementations (reference) -------------
def pairLaw(z, k, m, g):
    tau = 2 * m + g
    gs = z - 2 * k
    if tau <= z and g <= gs:
        return 2 if tau == z else IND(tau % 2 == 1)
    if gs <= 0:
        return IND(g % 2 == 1)
    if g < gs:
        return IND(g % 2 == 0)
    if g == gs:
        return 2
    return IND(g % 2 == 1)


def bedLaw(z, k, a):
    gs = z - 2 * k
    tb = 2 * a
    if gs < 0:
        return 0
    if gs == 0:
        return 0 if tb < z else 2
    if tb < z:
        return 0
    if tb == z:
        return 2
    return 1


def f0f(d):
    if d == 1:
        return 2
    if d <= 0:
        return IND(d % 2 == 1)
    return IND(d % 2 == 0)


def g1f(d):
    if d == 1:
        return 2
    if d <= 0:
        return IND(d % 2 == 0)
    return IND(d % 2 == 1)


def Lw(w):
    return 2 * ((w + 1) // 2)


def sw(w):
    return 2 * (w // 2)


def Twf(w, d):
    return g1f(d) if w % 2 else f0f(d)


def cpsfG(w, R, d):
    if R < Lw(w):
        return 2 * (R % 2)
    return Twf(w, d - sw(w))


def single_token(x, z, R):
    if R == 0 or x <= 0:
        return 0
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = z if z % 2 else z - 1
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = x if x % 2 else x - 1
        if R <= m:
            return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))


# ---------------- symbolic pair machinery -------------------------------
# gs classes: 0: gs<=-1 (NEG), 1: ==0 (ZERO), 2: >=1 (POS)
# ggs classes: 0: g<=gs-2, 1: g==gs-1, 2: g==gs, 3: g==gs+1, 4: g>=gs+2
# gzs classes: 0: g<=z-3, 1: g==z-2, 2: g==z-1, 3: g==z, 4: g==z+1, 5: g>=z+2
# tau classes: 0: t<=z-2, 1: t==z-1, 2: t==z, 3: t==z+1, 4: t==z+2,
#              5: t==z+3, 6: t>=z+4


class Undetermined(Exception):
    pass


def sym_claim_pair(pz, pg, gs, ggs, tau):
    zone = (tau in (0, 1, 2)) and (ggs in (0, 1, 2))
    if zone:
        return 2 if tau == 2 else pg
    if gs in (0, 1):
        return pg
    if ggs in (0, 1):
        return 1 - pg
    if ggs == 2:
        return 2
    return pg


def sym_fall(pz, pg, gs, ggs, tau):
    # child pair (m-1, g+1), same k, z
    az = tau in (0, 1, 2, 3)          # tau-1 <= z
    bz = tau == 3                      # tau-1 == z  (wave)
    cz = ggs in (0, 1)                 # g+1 <= gs
    if az and cz:
        return 2 if (bz) else (1 - pg)
    if gs in (0, 1):
        return 1 - pg                  # [g+1 odd]
    if ggs in (0,):                    # g+1 <= gs-1 < gs: [even]
        return pg
    if ggs == 1:                       # g+1 == gs
        return 2
    return 1 - pg                       # [g+1 odd]


def sym_compress(pz, pg, gs, ggs, tau):
    # child pair (m, g-1), same k, z
    az = tau in (0, 1, 2, 3)
    bz = tau == 3
    cz = ggs in (0, 1, 2, 3)           # g-1 <= gs
    if az and cz:
        return 2 if (bz) else (1 - pg)
    if gs in (0, 1):
        return 1 - pg                  # [g-1 odd]
    if ggs in (0, 1, 2):               # g-1 < gs: [even]
        return pg
    if ggs == 3:                       # g-1 == gs
        return 2
    return 1 - pg                       # [g-1 odd]


def sym_corner_bed(pz, pg, gs, ggs, tau):
    # child bed (m, m) i.e. bed(k, z, a=m); g==1 -> 2m = tau-1
    tb = (tau in (0, 1, 2), tau == 3, tau in (4, 5, 6))  # (<z, ==z, >z)
    if gs == 0:
        return 0
    if gs == 1:
        return 0 if tb[0] else 2
    return ({0: 0, 1: 2, 2: 1})[[0, 1, 2].index(
        0 if tb[0] else (1 if tb[1] else 2))]


def sym_lbeprime(pz, pg, tau):
    # B-exit single token at m==1: g = tau-2
    if tau in (0, 1, 2, 3):
        return 1 - pg                   # [g even]
    if tau == 4:
        return 1 - pz                   # [z even]
    if tau == 5:
        return pz                       # [z odd]
    return 1 - pg                       # [g even] again


def sym_cchild_kge2(pz, pg, gs, ggs, tau):
    # C-child pair (k-1, z-1, m, g) at m>=... k>=2. CONCESSION: kid = 1 ^ C.
    # Child frame: tau' = tau, g' = g, gs' = gs+1, z' = z-1.
    # gs label: 0 = gs<=-1 (so gs'<=0), 1 = gs==0 (gs'==1), 2 = gs>=1 (gs'>=2)
    az = tau in (0, 1)                 # tau <= z' = z-1
    bz = tau == 1                      # tau == z' (wave in child frame)
    cz = ggs in (0, 1, 2, 3)           # g <= gs'
    if az and cz:
        return 1 ^ (2 if (bz) else pg)
    # f regions with gs' = gs+1
    if gs == 0:                         # parent NEG: gs' = gs+1 <= 0
        return 1 ^ pg                   # f = [g odd]
    if gs == 1:                         # parent ZERO: gs' == 1
        if ggs == 3:                    # g == gs+1 == 1 -> f column
            return 1 ^ 2
        return 1 ^ pg                   # g > gs' -> [g odd]
    # parent POS: gs' >= 2
    if ggs in (0, 1, 2):
        return 1 ^ (1 - pg)             # [g even]
    if ggs == 3:
        return 1 ^ 2
    return 1 ^ pg


def sym_cchild_k1(pz, pg, gzs, tau):
    # band child: cpsfG(z-1, tau, g) ; C-value = 1 ^ band
    if pz == 1:
        # z odd: w = z-1 even, Lw = z-1, sw = z-1
        if tau == 0:
            b = 2 * pg                  # tau <= z-2
        else:
            # f0(g - (z-1)) = f0(g-z+1)
            if gzs in (0, 1, 2):
                b = IND(pg == pz)       # [d odd], d = g-z+1
            elif gzs == 3:
                b = 2                   # d == 1
            else:
                b = IND(pg != pz)       # [d even]
    else:
        # z even: w = z-1 odd, Lw = z, sw = z-2
        if tau in (0, 1):
            b = 2 * pg                  # tau <= z-1
        else:
            # g1f(g - (z-2)) = g1f(g-z+2)
            if gzs in (0, 1):
                b = IND(pg == pz)       # [d even]
            elif gzs == 2:
                b = 2                   # d == 1
            else:
                b = IND(pg != pz)       # [d odd]
    return 1 ^ b


def pair_class_children(pz, pg, gs, ggs, gzs, tau, m1, g1, k1):
    kids = []
    if m1:
        kids.append(sym_lbeprime(pz, pg, tau))
    else:
        kids.append(sym_fall(pz, pg, gs, ggs, tau))
    if g1:
        kids.append(sym_corner_bed(pz, pg, gs, ggs, tau))
    else:
        kids.append(sym_compress(pz, pg, gs, ggs, tau))
    if k1:
        kids.append(sym_cchild_k1(pz, pg, gzs, tau))
    else:
        kids.append(sym_cchild_kge2(pz, pg, gs, ggs, tau))
    return kids


def mex(vals):
    s = set(vals)
    i = 0
    while i in s:
        i += 1
    return i


# ---- typed (concrete-coordinates) children, identical to typed_check.py,
#      engine-verified version; used as coverage-census ground truth ----
def typed_pair_children(k, z, m, g):
    kids = []
    if m >= 2:
        kids.append(pairLaw(z, k, m - 1, g + 1))
    else:
        kids.append(single_token(g + 1, z + 1, g + k + 1))
    if g >= 2:
        kids.append(pairLaw(z, k, m, g - 1))
    else:
        kids.append(bedLaw(z, k, m))
    if k >= 2:
        kids.append(1 ^ pairLaw(z - 1, k - 1, m, g))
    else:
        kids.append(1 ^ cpsfG(z - 1, 2 * m + g, g))
    return kids


def typed_bed_children(k, z, a):
    kids = []
    if a >= 2:
        kids.append(pairLaw(z, k, a - 1, 1))
    else:
        kids.append(single_token(1, z + 1, k + 1))
    if k >= 2:
        kids.append(1 ^ bedLaw(z - 1, k - 1, a))
    else:
        kids.append(1 ^ cpsfG(z - 1, 2 * a, 0))
    return kids


# ---------------- witness search (pair) ---------------------------------
def pair_witness(pz, pg, gsC, ggsC, gzsC, tauC, m1, g1, k1):
    """search a concrete (z,k,m,g) realizing the class; Box lemma:
    difference-bound offsets <= 6."""
    for z in range(2, 34):
        if z % 2 != pz:
            continue
        for k in range(1, z):
            if (k % 2) == (z % 2):
                continue
            if k1 != (k == 1):
                continue
            gs = z - 2 * k
            if gsC == 0 and gs >= -1:
                continue
            if gsC == 1 and gs != 0:
                continue
            if gsC == 2 and gs < 1:
                continue
            for g in range(1, 50):
                if g % 2 != pg:
                    continue
                if g1 != (g == 1):
                    continue
                if ggsC == 0 and g > gs - 2:
                    continue
                if ggsC == 1 and g != gs - 1:
                    continue
                if ggsC == 2 and g != gs:
                    continue
                if ggsC == 3 and g != gs + 1:
                    continue
                if ggsC == 4 and g < gs + 2:
                    continue
                if gzsC == 0 and g > z - 3:
                    continue
                if gzsC == 1 and g != z - 2:
                    continue
                if gzsC == 2 and g != z - 1:
                    continue
                if gzsC == 3 and g != z:
                    continue
                if gzsC == 4 and g != z + 1:
                    continue
                if gzsC == 5 and g < z + 2:
                    continue
                # tau = 2m + g
                for m in range(1, 26):
                    if m1 != (m == 1):
                        continue
                    t = 2 * m + g
                    if tauC == 0 and t > z - 2:
                        continue
                    if tauC == 1 and t != z - 1:
                        continue
                    if tauC == 2 and t != z:
                        continue
                    if tauC == 3 and t != z + 1:
                        continue
                    if tauC == 4 and t != z + 2:
                        continue
                    if tauC == 5 and t != z + 3:
                        continue
                    if tauC == 6 and t < z + 4:
                        continue
                    return (z, k, m, g)
    return None


def enumerate_pair_classes():
    classes = []
    for pz in (0, 1):
        for pg in (0, 1):
            for gsC in (0, 1, 2):
                for ggsC in range(5):
                    for gzsC in range(6):
                        for tauC in range(7):
                            for m1 in (True, False):
                                for g1 in (True, False):
                                    for k1 in (True, False):
                                        w = pair_witness(pz, pg, gsC, ggsC,
                                                         gzsC, tauC, m1, g1, k1)
                                        if w is None:
                                            continue
                                        claim = sym_claim_pair(pg=pg, gs=gsC,
                                                               ggs=ggsC,
                                                               tau=tauC,
                                                               pz=pz)
                                        kids = pair_class_children(
                                            pz, pg, gsC, ggsC, gzsC, tauC,
                                            m1, g1, k1)
                                        classes.append(dict(
                                            fam='pair', pz=pz, pg=pg,
                                            gs=gsC, ggs=ggsC, gzs=gzsC,
                                            tau=tauC, m1=m1, g1=g1, k1=k1,
                                            witness=w, claim=claim,
                                            kids=kids,
                                            mex=mex(kids)))
    return classes


# ---------------- symbolic bed machinery -------------------------------
# bed gs classes: 0: gs<=-2, 1: gs==-1, 2: gs==0, 3: gs==1, 4: gs>=2
# tb classes: 0: tb<=z-2, 1: tb==z-1, 2: tb==z, 3: tb==z+1, 4: tb>=z+2


def sym_claim_bed(gs, tb):
    if gs in (0, 1):
        return 0
    if gs == 2:
        return 0 if tb in (0, 1) else 2
    if tb in (0, 1):
        return 0
    if tb == 2:
        return 2
    return 1


def sym_bed_compress_child(gs, tb):
    # child pair (k, z, a-1, 1): tau'' = 2a-1 (odd), g''=1
    az = tb in (0, 1, 2, 3)             # tau'' <= z
    bz = tb == 3                        # tau'' == z (wave)
    cz = gs in (3, 4)                   # 1 <= gs
    if az and cz:
        return 2 if (bz) else 1         # [tau'' odd] = 1
    # f(1)
    if gs in (0, 1, 2):
        return 1                        # [1 odd]
    if gs == 3:
        return 2
    return 0                            # [1 even]


def sym_bed_cchild_kge2(gs, tb):
    # C-child bed (k-1, z-1, a), k>=2. CONCESSION: kid = 1 ^ C.
    # Child frame: gs' = gs+1, tb unchanged, z' = z-1.
    # gs label: 0: gs<=-2 (gs'<=-1), 1: gs==-1 (gs'==0), 2: gs==0 (gs'==1),
    #           3: gs==1 (gs'==2), 4: gs>=2 (gs'>=3)
    if gs == 0:                         # gs' <= -1 < 0
        return 1 ^ 0
    if gs == 1:                         # gs' == 0: tb<z' -> 0 else 2
        return 1 ^ (0 if tb == 0 else 2)
    # gs' >= 1: 0 / 2 / 1 by tb vs z' ; tb < z'=z-1 <==> tb<=z-2 (B0)
    if tb == 0:
        return 1 ^ 0
    if tb == 1:                         # tb == z-1 == z'
        return 1 ^ 2
    return 1 ^ 1


def sym_bed_cchild_k1(pz, tb):
    # band bed cpsfG(z-1, 2a, 0); (k==1 => z even); C = 1 ^ band
    # band = 0 if 2a < Lw(z-1)=z else g1f(2-z)=1
    band = 0 if tb in (0, 1) else 1
    return 1 ^ band


def bed_class_children(gs, tb, a1, k1, pz):
    kids = []
    if a1:
        kids.append(1)                   # single_token(1, z+1, k+1) == 1
    else:
        kids.append(sym_bed_compress_child(gs, tb))
    if k1:
        kids.append(sym_bed_cchild_k1(pz, tb))
    else:
        kids.append(sym_bed_cchild_kge2(gs, tb))
    return kids


def bed_witness(pz, gsC, tbC, a1, k1):
    for z in range(2, 34):
        if z % 2 != pz:
            continue
        for k in range(1, z):
            if (k % 2) == (z % 2):
                continue
            if k1 != (k == 1):
                continue
            gs = z - 2 * k
            if gsC == 0 and gs > -2:
                continue
            if gsC == 1 and gs != -1:
                continue
            if gsC == 2 and gs != 0:
                continue
            if gsC == 3 and gs != 1:
                continue
            if gsC == 4 and gs < 2:
                continue
            for a in range(1, 25):
                if a1 != (a == 1):
                    continue
                tb = 2 * a
                if tbC == 0 and tb > z - 2:
                    continue
                if tbC == 1 and tb != z - 1:
                    continue
                if tbC == 2 and tb != z:
                    continue
                if tbC == 3 and tb != z + 1:
                    continue
                if tbC == 4 and tb < z + 2:
                    continue
                return (z, k, a)
    return None


def enumerate_bed_classes():
    classes = []
    for pz in (0, 1):
        for gsC in range(5):
            for tbC in range(5):
                for a1 in (True, False):
                    for k1 in (True, False):
                        w = bed_witness(pz, gsC, tbC, a1, k1)
                        if w is None:
                            continue
                        claim = sym_claim_bed(gsC, tbC)
                        kids = bed_class_children(gsC, tbC, a1, k1, pz)
                        classes.append(dict(
                            fam='bed', pz=pz, gs=gsC, tb=tbC, a1=a1, k1=k1,
                            witness=w, claim=claim, kids=kids,
                            mex=mex(kids)))
    return classes


def main():
    pc = enumerate_pair_classes()
    bc = enumerate_bed_classes()
    badp = [c for c in pc if c['claim'] != c['mex']]
    badb = [c for c in bc if c['claim'] != c['mex']]
    print(f'pair classes: {len(pc)}  bad={len(badp)}')
    for c in badp[:10]:
        print('  BADPAIR', c)
    print(f'bed classes: {len(bc)}  bad={len(badb)}')
    for c in badb[:10]:
        print('  BADBED', c)

    # --- cross-validation: per class, symbolic vs concrete on the witness ---
    xc = 0
    for c in pc:
        z, k, m, g = c['witness']
        ok1 = pairLaw(z, k, m, g) == c['claim']
        kids = []
        if m >= 2:
            kids.append(pairLaw(z, k, m - 1, g + 1))
        else:
            kids.append(single_token(g + 1, z + 1, g + k + 1))
        if g >= 2:
            kids.append(pairLaw(z, k, m, g - 1))
        else:
            kids.append(bedLaw(z, k, m))
        if k >= 2:
            kids.append(1 ^ pairLaw(z - 1, k - 1, m, g))
        else:
            kids.append(1 ^ cpsfG(z - 1, 2 * m + g, g))
        ok2 = kids == c['kids']
        ok3 = mex(kids) == c['mex']
        if not (ok1 and ok2 and ok3):
            print('  XPAIR', c, kids)
            xc += 1
    xb = 0
    for c in bc:
        z, k, a = c['witness']
        ok1 = bedLaw(z, k, a) == c['claim']
        kids = []
        if a >= 2:
            kids.append(pairLaw(z, k, a - 1, 1))
        else:
            kids.append(single_token(1, z + 1, k + 1))
        if k >= 2:
            kids.append(1 ^ bedLaw(z - 1, k - 1, a))
        else:
            kids.append(1 ^ cpsfG(z - 1, 2 * a, 0))
        ok2 = kids == c['kids']
        ok3 = mex(kids) == c['mex']
        if not (ok1 and ok2 and ok3):
            print('  XBED', c, kids)
            xb += 1
    print(f'cross-validation failures: pair={xc} bed={xb}')

    # --- coverage census: EVERY concrete cell's labels must drive the sym
    # machinery to the concrete law, the concrete typed children, and mex
    # closure. This catches label-derivation errors far from witnesses.
    # Additionally every cell's label combo must MATCH an enumerated class
    # (partition-completeness at census depth), with identical claim+kids.
    pidx = {(c['pz'], c['pg'], c['gs'], c['ggs'], c['gzs'], c['tau'],
             c['m1'], c['g1'], c['k1']): c for c in pc}
    bidx = {(c['pz'], c['gs'], c['tb'], c['a1'], c['k1']): c for c in bc}
    ZM = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    MM = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    GM = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    AM = int(sys.argv[4]) if len(sys.argv) > 4 else 14
    pcells = pbad = bcells = bbad = 0
    missing = 0
    for z in range(2, ZM + 1):
        for k in range(1, z):
            if (k % 2) == (z % 2):
                continue
            gs = z - 2 * k
            for m in range(1, MM + 1):
                for g in range(1, GM + 1):
                    tau = 2 * m + g
                    pz, pg = z % 2, g % 2
                    gsC = 0 if gs <= -1 else (1 if gs == 0 else 2)
                    d = g - gs
                    ggsC = 0 if d <= -2 else (1 if d == -1 else
                                               (2 if d == 0 else
                                                (3 if d == 1 else 4)))
                    dd = g - z
                    gzsC = 0 if dd <= -3 else (1 if dd == -2 else
                                               (2 if dd == -1 else
                                                (3 if dd == 0 else
                                                 (4 if dd == 1 else 5))))
                    dt = tau - z
                    tauC = 0 if dt <= -2 else (1 if dt == -1 else
                                               (2 if dt == 0 else
                                                (3 if dt == 1 else
                                                 (4 if dt == 2 else
                                                  (5 if dt == 3 else 6)))))
                    kids = pair_class_children(pz, pg, gsC, ggsC, gzsC,
                                               tauC, m == 1, g == 1, k == 1)
                    claim = sym_claim_pair(pg=pg, gs=gsC, ggs=ggsC,
                                           tau=tauC, pz=pz)
                    c = pidx.get((pz, pg, gsC, ggsC, gzsC, tauC,
                                  m == 1, g == 1, k == 1))
                    if c is None:
                        missing += 1
                    ok = (c is not None
                          and kids == typed_pair_children(k, z, m, g)
                          and claim == pairLaw(z, k, m, g)
                          and mex(kids) == claim
                          and c['claim'] == claim and c['kids'] == kids)
                    pcells += 1
                    if not ok:
                        pbad += 1
                        if pbad <= 5:
                            print('  CPAIR', (z, k, m, g), claim, kids,
                                  typed_pair_children(k, z, m, g))
            for a in range(1, AM + 1):
                pz = z % 2
                gsb = z - 2 * k
                gsC = (0 if gsb <= -2 else (1 if gsb == -1 else
                                            (2 if gsb == 0 else
                                             (3 if gsb == 1 else 4))))
                tb = 2 * a
                dt = tb - z
                tbC = 0 if dt <= -2 else (1 if dt == -1 else
                                          (2 if dt == 0 else
                                           (3 if dt == 1 else 4)))
                kids = bed_class_children(gsC, tbC, a == 1, k == 1, pz)
                claim = sym_claim_bed(gsC, tbC)
                c = bidx.get((pz, gsC, tbC, a == 1, k == 1))
                if c is None:
                    missing += 1
                ok = (c is not None
                      and kids == typed_bed_children(k, z, a)
                      and claim == bedLaw(z, k, a)
                      and mex(kids) == claim
                      and c['claim'] == claim and c['kids'] == kids)
                bcells += 1
                if not ok:
                    bbad += 1
                    if bbad <= 5:
                        print('  CBED', (z, k, a), claim, kids,
                              typed_bed_children(k, z, a))
    print(f'coverage census: pair cells={pcells} bad={pbad} '
          f'bed cells={bcells} bad={bbad} missing-class={missing}')
    total_bad = (len(badp) + len(badb) + xc + xb + pbad + bbad + missing)
    print(f'RESULT: {"PASS" if total_bad == 0 else "FAIL"} '
          f'pair_classes={len(pc)} pair_bad={len(badp)} '
          f'bed_classes={len(bc)} bed_bad={len(badb)} '
          f'xpair={xc} xbed={xb} census_pair={pcells} '
          f'census_pair_bad={pbad} census_bed={bcells} '
          f'census_bed_bad={bbad} missing_class={missing}')
    sys.exit(0 if total_bad == 0 else 1)


if __name__ == '__main__':
    main()
