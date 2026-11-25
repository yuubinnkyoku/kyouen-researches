#!/usr/bin/env python3
"""Universal induction proof: all-ones residual family h(k,z,R) = U(k,z,R) for ALL
k,z,R >= 0 (z=0 slice: h(k,0,R) = U0(k,R)).

Machine parts (audit JSON to stdout; deterministic; run twice for byte-identical):
  B0  base R=0 checks (paper case analysis in report.md; box-checked here)
  S1  atom table: every branch condition of U/U0/mex at evaluation points
      P=(k,z,R), B=(k-1,z+1,R-1), C=(k,z-1,R-1), G=(k-1,1,R-2) reduced to
      alpha*s+beta*s2+gamma*R <= t (witness coords s=R-k, s2=R-z) or mod-4 congruence
  S2  transcription: U_tab (same tree, conditions read from witness side) == U at
      every box point P/B/C/G + randoms; per-atom truth equivalence both sides
  S3  step identity over box (k,z in [0..64]^2, R in [1..maxBP(k,z)+6]):
      mex{U(B) [k>=1], 1^Utilde(C) [z>=1]} == U(k,z,R)  (z>=1)
      mex{U(k-1,1,R-1) [k>=1]} == U0(k,R)               (z=0)
      checked with published U and with U_tab (double entry)
  C1  covering: signature = per-family comparison bit vector + (s,s2,R) mod 4.
      Reachable witness sweep (|s|,|s2| <= WIT_W, R <= WIT_R, s,s2 <= R) realizes
      C_wit; box sweep realizes C_box; saturation sweep (larger) realizes C_sat.
      Assert C_wit == C_box == C_sat (with the covering lemma in report.md).
  E*  engine cross-checks (h vs multiset engine; h vs U/U0 on grids; random
      large; 2-position corollary; z=1,2 slices)
"""
import sys, json, random
from functools import lru_cache
sys.setrecursionlimit(100000)

BOX = 64
WIT_W, WIT_R = 160, 320
SAT_W, SAT_R = 224, 512

def q(n):
    return n if n % 2 == 1 else n - 1

def mex(vals):
    g = 0
    s = set(vals)
    while g in s:
        g += 1
    return g

@lru_cache(maxsize=None)
def h(k, z, R):
    if R == 0:
        return 0
    cands = set()
    if k >= 1:
        cands.add(h(k - 1, z + 1, R - 1))
    if z >= 1:
        cands.add(1 ^ h(k, z - 1, R - 1))
    g = 0
    while g in cands:
        g += 1
    return g

@lru_cache(maxsize=None)
def H(R, X, z):
    if R == 0:
        return 0
    cands = set()
    for x in set(X):
        nx = list(X)
        if x >= 2:
            nx.remove(x); nx.append(x - 1); nx.sort()
            cands.add(H(R - 1, tuple(nx), z))
        else:
            nx.remove(1); nx.sort()
            cands.add(H(R - 1, tuple(nx), z + 1))
    if z >= 1:
        cands.add(1 ^ H(R - 1, X, z - 1))
    g = 0
    while g in cands:
        g += 1
    return g

def U(k, z, R):  # published unified slice closed form (verbatim)
    if z < 1:
        raise ValueError
    if z % 2 == 1:
        if R % 2 == 1:
            return 2 if R <= q(k) else (1 if k % 2 == 1 else 0)
        if k % 2 == 1:
            if R <= min(z - 3, k - 1):
                return 0
            if R % 4 == (z - 1) % 4 and z - 1 <= R <= 2 * k - z - 1:
                return 0
            return 1
        else:
            if R % 4 == (z + 1) % 4 and z + 1 <= R <= 2 * k - z - 1:
                return 1
            return 0
    else:
        twos = set(range(1, q(min(k, z)) + 1, 2))
        far = 2 * k - z + 1
        if far >= 1:
            twos.add(far)
        if R in twos:
            return 2
        if R % 4 == (z + 1) % 4 and z + 1 <= R <= 2 * k - z - 1 and R != far:
            return 1
        if k % 2 == 1:
            if (R % 2 == 0 and R <= k - 1) or (R % 4 == (z - 1) % 4 and z + 3 <= R <= 2 * k - z - 3):
                return 0
            return 1
        return 0

def U0(k, R):
    if k >= 1 and R >= 1:
        return 1 if U(k - 1, 1, R - 1) == 0 else 0
    return 0

def predT(k, z):
    if z == 0:
        return set()
    if z % 2 == 1:
        return set(range(1, q(k) + 1, 2))
    s = set(range(1, q(min(k, z)) + 1, 2))
    far = 2 * k - z + 1
    if far >= 1:
        s.add(far)
    return s

def slice12(k, z, R):  # published z=1,2 slice form (verbatim)
    if k == 0:
        return 0
    if z == 1:
        if k % 2 == 1:
            if R % 2 == 1 and R <= k:
                return 2
            if R % 4 == 0 and R <= 2 * k - 2:
                return 0
            return 1
        else:
            if R % 2 == 1 and R <= k - 1:
                return 2
            if R % 4 == 2 and 2 <= R <= 2 * k - 2:
                return 1
            return 0
    if z == 2:
        if k % 2 == 1:
            if R == 1 or R == 2 * k - 1:
                return 2
            if R % 2 == 0 and R <= k - 1:
                return 0
            if R % 4 == 1 and 5 <= R <= 2 * k - 5:
                return 0
            return 1
        else:
            if R == 1 or R == 2 * k - 1:
                return 2
            if R % 4 == 3 and 3 <= R <= 2 * k - 5:
                return 1
            return 0
    raise ValueError

# ------------------------------------------------------------ S1: atom table
# comparison atoms:  coeffs . (localK, localZ, localR) + rhs <= 0
L_ATOMS = [
    ("b>=1",        (0, -1, 0), 1),
    ("c<=a",        (-1, 0, 1), 0),
    ("c<=a-1",      (-1, 0, 1), 1),
    ("c<=b-3",      (0, -1, 1), 3),
    ("c<=b",        (0, -1, 1), 0),
    ("c<=b-1",      (0, -1, 1), 1),
    ("b-1<=c",      (0, 1, -1), -1),
    ("b+1<=c",      (0, 1, -1), 1),
    ("b+3<=c",      (0, 1, -1), 3),
    ("c<=2a-b-1",   (-2, 1, 1), 1),
    ("c<=2a-b-3",   (-2, 1, 1), 3),
    ("c<=2a-b+1",   (-2, 1, 1), -1),
    ("2a-b+1<=c",   (2, -1, -1), 1),
    ("b<=a",        (-1, 1, 0), 0),
    ("b<=2a",       (-2, 1, 0), 0),
    ("a>=1",        (-1, 0, 0), 1),
    ("c>=1",        (0, 0, -1), 1),
    ("c>=2",        (0, 0, -1), 2),
]
L_CONGS = [
    ("a%2==1",   (1, 0, 0), 1),
    ("b%2==1",   (0, 1, 0), 1),
    ("c%2==1",   (0, 0, 1), 1),
    ("c==b-1%4", (0, -1, 1), 3),
    ("c==b+1%4", (0, -1, 1), 1),
]
POINTS = ("P", "B", "C", "G")
KOFF = {"P": 0, "B": 1, "C": 0, "G": 1}   # localK = k - KOFF[pt]
ROFF = {"P": 0, "B": 1, "C": 1, "G": 1}   # localR = R - ROFF[pt]

def point_coords(pt, k, z, R):
    if pt == "P":
        return (k, z, R)
    if pt == "B":
        return (k - 1, z + 1, R - 1)
    if pt == "C":
        return (k, z - 1, R - 1)
    if pt == "G":
        return (k - 1, 1, R - 1)
    raise ValueError

def local_to_global(coeffs, rhs, pt):
    a, b, c = coeffs
    if pt == "P":
        return (a, b, c, rhs)
    if pt == "B":
        return (a, b, c, rhs - a + b - c)
    if pt == "C":
        return (a, b, c, rhs - b - c)
    if pt == "G":
        return (a, 0, c, rhs - a + b - c)
    raise ValueError

def global_to_witness(g):
    """A k + B z + C R + cst <= 0  ->  (alpha, beta, gamma, t) with
       alpha*s + beta*s2 + gamma*R <= t, where t = -cst."""
    A, B, C, cst = g
    return (-A, -B, A + B + C, -cst)

FAM_THR = {}
FAM_OF = {}
for (nm, co, rhs) in L_ATOMS:
    for pt in POINTS:
        al, be, ga, t = global_to_witness(local_to_global(co, rhs, pt))
        FAM_THR.setdefault((al, be, ga), set()).add(t)
        FAM_OF[(nm, pt)] = ((al, be, ga), t)
FAMS = sorted(FAM_THR)
FAM_THR_LIST = [(f, sorted(FAM_THR[f])) for f in FAMS]
FAM_IDX = {f: i for i, f in enumerate(FAMS)}
ATOM_LOCAL = {nm: (co, rhs) for (nm, co, rhs) in L_ATOMS}
CONG_LOCAL = {nm: (co, rhs) for (nm, co, rhs) in L_CONGS}

def wit_v(s, s2, R):
    """per-family packed comparison bits from witness coordinates only"""
    out = []
    for (f, thr) in FAM_THR_LIST:
        x = f[0] * s + f[1] * s2 + f[2] * R
        v = 0
        for i, t in enumerate(thr):
            if x <= t:
                v |= 1 << i
        out.append(v)
    return tuple(out)

def signature(s, s2, R):
    return (wit_v(s, s2, R), (s % 4, s2 % 4, R % 4))

def signature_kzr(k, z, R):
    return signature(R - k, R - z, R)

# witness-side closures for congruence atoms at point pt (from residues only)
def wit_congs(pt, s, s2, R):
    aodd = (R - s - KOFF[pt]) % 2 == 1     # localK = k - KOFF = R-s-KOFF
    if pt == "G":
        bodd = True                          # localZ == 1
    else:
        bmod = (R - s2 + (1 if pt == "B" else (-1 if pt == "C" else 0)))
        bodd = bmod % 2 == 1
    codd = (R - ROFF[pt]) % 2 == 1
    if pt == "G":
        d = (R - 2) % 4   # localR - localZ = (R-1) - 1
    else:
        d = (s2 - (2 if pt == "B" else 0)) % 4
    return aodd, bodd, codd, (d == 3), (d == 1)

def tab_cmp(nm, pt, s, s2, R):
    fam, t = FAM_OF[(nm, pt)]
    return fam[0] * s + fam[1] * s2 + fam[2] * R <= t

def U_tab_at(pt, k, z, R):
    """published decision tree, all conditions read from witness side"""
    s, s2 = R - k, R - z
    aodd, bodd, codd, cbm1, cbp1 = wit_congs(pt, s, s2, R)
    if bodd:
        if codd:
            if tab_cmp("c<=a", pt, s, s2, R) and (aodd or tab_cmp("c<=a-1", pt, s, s2, R)):
                return 2
            return 1 if aodd else 0
        if aodd:
            if tab_cmp("c<=b-3", pt, s, s2, R) and tab_cmp("c<=a-1", pt, s, s2, R):
                return 0
            if cbm1 and tab_cmp("b-1<=c", pt, s, s2, R) and tab_cmp("c<=2a-b-1", pt, s, s2, R):
                return 0
            return 1
        else:
            if cbp1 and tab_cmp("b+1<=c", pt, s, s2, R) and tab_cmp("c<=2a-b-1", pt, s, s2, R):
                return 1
            return 0
    else:
        in_twos = False
        if codd:
            if tab_cmp("b<=a", pt, s, s2, R):
                if tab_cmp("c<=b", pt, s, s2, R) and (bodd or tab_cmp("c<=b-1", pt, s, s2, R)):
                    in_twos = True
            else:
                if tab_cmp("c<=a", pt, s, s2, R) and (aodd or tab_cmp("c<=a-1", pt, s, s2, R)):
                    in_twos = True
        if not in_twos and tab_cmp("b<=2a", pt, s, s2, R) \
           and tab_cmp("c<=2a-b+1", pt, s, s2, R) and tab_cmp("2a-b+1<=c", pt, s, s2, R):
            in_twos = True
        if in_twos:
            return 2
        far_is = tab_cmp("c<=2a-b+1", pt, s, s2, R) and tab_cmp("2a-b+1<=c", pt, s, s2, R)
        if cbp1 and tab_cmp("b+1<=c", pt, s, s2, R) and tab_cmp("c<=2a-b-1", pt, s, s2, R) \
           and not far_is:
            return 1
        if aodd:
            if (not codd and tab_cmp("c<=a-1", pt, s, s2, R)) \
               or (cbm1 and tab_cmp("b+3<=c", pt, s, s2, R) and tab_cmp("c<=2a-b-3", pt, s, s2, R)):
                return 0
            return 1
        return 0

def U_tab(k, z, R):
    return U_tab_at("P", k, z, R)

def U0_tab(k, R):
    if k >= 1 and R >= 1:
        return 1 if U_tab_at("G", k, 0, R) == 0 else 0
    return 0

def step_published(k, z, R):
    opts = []
    if k >= 1:
        opts.append(U(k - 1, z + 1, R - 1))
    if z >= 1:
        opts.append(1 ^ (U(k, z - 1, R - 1) if z >= 2 else U0(k, R - 1)))
    return mex(opts), opts

def step_tab(k, z, R):
    opts = []
    if k >= 1:
        opts.append(U_tab_at("B", k, z, R))
    if z >= 1:
        opts.append(1 ^ (U_tab_at("C", k, z, R) if z >= 2 else U0_tab(k, R - 1)))
    return mex(opts), opts

def expected_published(k, z, R):
    return U(k, z, R) if z >= 1 else U0(k, R)

def expected_tab(k, z, R):
    return U_tab(k, z, R) if z >= 1 else U0_tab(k, R)

def maxBP(k, z):
    """last R at which any comparison bit changes, for fixed (k,z).
    x = (al+be+ga) R - al k - be z <= t along fixed (k,z)."""
    best = 0
    for (f, thr) in FAM_THR_LIST:
        al, be, ga = f
        c3 = al + be + ga
        if c3 == 0:
            continue
        base = -al * k - be * z
        for t in thr:
            if c3 > 0:
                # x <= t iff R <= (t-base)/c3 ; bit changes up to floor
                r1 = (t - base) // c3
                cand = r1
            else:
                # x <= t iff R >= ceil((t-base)/c3) ; last change at that R
                a_, b_ = t - base, -c3
                cand = -((-a_) // b_)
            if cand > best:
                best = cand
    return best

def atom_truth_local(nm, pt, k, z, R):
    co, rhs = ATOM_LOCAL[nm]
    a, b, c = point_coords(pt, k, z, R)
    return co[0] * a + co[1] * b + co[2] * c + rhs <= 0

def main():
    out = {"params": {"BOX": BOX, "WIT_W": WIT_W, "WIT_R": WIT_R,
                      "SAT_W": SAT_W, "SAT_R": SAT_R}}
    rng = random.Random(20261116)
    out["S1_families"] = [[list(f), thr] for (f, thr) in FAM_THR_LIST]

    # --- S2: transcription over box + randoms
    s2c = {"checks": 0, "mismatch": 0, "first": []}
    def note(res, args, tag):
        s2c["checks"] += 1
        if not res:
            s2c["mismatch"] += 1
            if len(s2c["first"]) < 8:
                s2c["first"].append([tag] + list(args))
    for k in range(0, BOX + 1):
        for z in range(0, BOX + 1):
            for R in range(0, maxBP(k, z) + 7):
                if z >= 1:
                    note(U_tab(k, z, R) == U(k, z, R), (k, z, R), "P")
                if k >= 1 and R >= 1:
                    note(U_tab_at("B", k, z, R) == U(k - 1, z + 1, R - 1), (k, z, R), "B")
                if k >= 1 and z >= 2 and R >= 1:
                    note(U_tab_at("C", k, z, R) == U(k, z - 1, R - 1), (k, z, R), "C")
                if k >= 1 and R >= 1:
                    note(U_tab_at("G", k, z, R) == U(k - 1, 1, R - 1), (k, z, R), "G")
    for _ in range(4000):
        k = rng.randint(0, 220); z = rng.randint(0, 220); R = rng.randint(0, 320)
        if z >= 1:
            note(U_tab(k, z, R) == U(k, z, R), (k, z, R), "P")
        if k >= 1 and R >= 1:
            note(U_tab_at("B", k, z, R) == U(k - 1, z + 1, R - 1), (k, z, R), "B")
        if k >= 1 and z >= 2 and R >= 1:
            note(U_tab_at("C", k, z, R) == U(k, z - 1, R - 1), (k, z, R), "C")
        if k >= 1 and R >= 1:
            note(U_tab_at("G", k, z, R) == U(k - 1, 1, R - 1), (k, z, R), "G")
    out["S2_transcription"] = s2c

    # per-atom equivalence: witness-form truth vs local-coordinate truth
    atc = {"checks": 0, "mismatch": 0, "first": []}
    for _ in range(20000):
        k = rng.randint(0, 150); z = rng.randint(0, 150); R = rng.randint(0, 260)
        s, s2 = R - k, R - z
        for (nm, co, rhs) in L_ATOMS:
            for pt in POINTS:
                fam, t = FAM_OF[(nm, pt)]
                wt = fam[0] * s + fam[1] * s2 + fam[2] * R <= t
                lt = atom_truth_local(nm, pt, k, z, R)
                atc["checks"] += 1
                if wt != lt:
                    atc["mismatch"] += 1
                    if len(atc["first"]) < 8:
                        atc["first"].append([nm, pt, k, z, R])
        aodd, bodd, codd, cbm1, cbp1 = wit_congs("P", s, s2, R)
        lt = (k % 2 == 1, z % 2 == 1, R % 2 == 1, (R - z) % 4 == 3, (R - z) % 4 == 1)
        wt = (aodd, bodd, codd, cbm1, cbp1)
        atc["checks"] += 1
        if wt != lt:
            atc["mismatch"] += 1
            if len(atc["first"]) < 8:
                atc["first"].append(["congs-P", k, z, R])
        for pt in ("B", "C", "G"):
            a2, b2, c2 = point_coords(pt, k, z, R)
            aa, bb, cc, m1, p1 = wit_congs(pt, s, s2, R)
            lt = (a2 % 2 == 1, b2 % 2 == 1, c2 % 2 == 1, (c2 - b2) % 4 == 3, (c2 - b2) % 4 == 1)
            atc["checks"] += 1
            if (aa, bb, cc, m1, p1) != lt:
                atc["mismatch"] += 1
                if len(atc["first"]) < 8:
                    atc["first"].append(["congs-" + pt, k, z, R])
    out["S2_atom_equiv"] = atc

    # --- S3: step identity over box + C_box
    st = {"checks": 0, "mismatch": 0, "base_checks": 0, "base_mismatch": 0,
          "first": []}
    C_box = set()
    for k in range(0, BOX + 1):
        for z in range(0, BOX + 1):
            for R in range(1, maxBP(k, z) + 7):
                st["checks"] += 1
                val, _ = step_published(k, z, R)
                valt, _ = step_tab(k, z, R)
                exp = expected_published(k, z, R)
                expt = expected_tab(k, z, R)
                if val != exp or valt != expt or val != valt:
                    st["mismatch"] += 1
                    if len(st["first"]) < 8:
                        st["first"].append([k, z, R, val, exp, valt, expt])
                C_box.add(signature_kzr(k, z, R))
            st["base_checks"] += 1
            ok = (U(k, z, 0) == 0) if z >= 1 else (U0(k, 0) == 0)
            okt = (U_tab(k, z, 0) == 0) if z >= 1 else (U0_tab(k, 0) == 0)
            if not (ok and okt):
                st["base_mismatch"] += 1
                if len(st["first"]) < 8:
                    st["first"].append([k, z, 0, "base"])
    out["S3_step"] = st
    out["C_box_size"] = len(C_box)

    # --- C1: reachable witness sweep with interval/residue compression
    def sweep(W, Rmax):
        combos = set()
        for s in range(-W, W + 1):
            for s2 in range(-W, W + 1):
                Rlo = max(1, s, s2)
                if Rlo > Rmax:
                    continue
                cuts = set()
                for (f, thr) in FAM_THR_LIST:
                    al, be, ga = f
                    x0 = al * s + be * s2
                    for t in thr:
                        if ga > 0:
                            # x = x0 + ga*R <= t  iff R <= floor((t-x0)/ga)
                            cut = (t - x0) // ga          # true for R <= cut
                        elif ga < 0:
                            # x = x0 + ga*R <= t iff R >= ceil((x0-t)/(-ga))
                            r2 = -((-(x0 - t)) // (-ga))
                            cut = r2 - 1                   # false for R <= cut
                        else:
                            continue
                        if Rlo <= cut < Rmax:
                            cuts.add(cut)
                prev = Rlo - 1
                for cut in sorted(cuts) + [Rmax]:
                    lo = prev + 1
                    hi = min(cut, Rmax)
                    if lo <= hi:
                        reps = [lo, lo + 1, lo + 2, lo + 3] if hi - lo >= 3 else list(range(lo, hi + 1))
                        v = wit_v(s, s2, lo)
                        for rr in reps:
                            combos.add((v, (s % 4, s2 % 4, rr % 4)))
                    prev = cut
                    if prev >= Rmax:
                        break
        return combos

    C_wit = sweep(WIT_W, WIT_R)
    out["C_wit_size"] = len(C_wit)
    cov = {"wit_not_in_box": 0, "box_not_in_wit": 0, "first": []}
    for c in C_wit:
        if c not in C_box:
            cov["wit_not_in_box"] += 1
            if len(cov["first"]) < 6:
                cov["first"].append([c[1]])
    for c in C_box:
        if c not in C_wit:
            cov["box_not_in_wit"] += 1
    out["C1_coverage"] = cov
    C_sat = sweep(SAT_W, SAT_R)
    out["C_sat_size"] = len(C_sat)
    out["C_sat_new_vs_wit"] = sum(1 for c in C_sat if c not in C_wit)
    out["C_sat_equal_C_wit"] = (C_sat == C_wit)

    # --- E*: engine cross-checks
    e1 = {"checks": 0, "mismatch": 0, "first": []}
    for k in range(0, 13):
        for z in range(0, 9):
            for R in range(0, 25):
                e1["checks"] += 1
                if h(k, z, R) != H(R, (1,) * k, z):
                    e1["mismatch"] += 1
                    if len(e1["first"]) < 5:
                        e1["first"].append([k, z, R])
    e2 = {"checks": 0, "mismatch": 0, "first": []}
    for k in range(0, 41):
        for z in range(1, 41):
            for R in range(0, min(2 * k + z + 3, 130)):
                e2["checks"] += 1
                if h(k, z, R) != U(k, z, R):
                    e2["mismatch"] += 1
                    if len(e2["first"]) < 5:
                        e2["first"].append([k, z, R])
    e3 = {"checks": 0, "mismatch": 0, "first": []}
    for k in range(0, 61):
        for R in range(0, 121):
            e3["checks"] += 1
            if h(k, 0, R) != U0(k, R):
                e3["mismatch"] += 1
                if len(e3["first"]) < 5:
                    e3["first"].append([k, R])
    e5 = {"checks": 0, "mismatch": 0, "first": []}
    for _ in range(400):
        k = rng.randint(0, 60); z = rng.randint(0, 60)
        R = rng.randint(0, 2 * k + z + 2)
        e5["checks"] += 1
        if (z >= 1 and h(k, z, R) != U(k, z, R)) or (z == 0 and h(k, 0, R) != U0(k, R)):
            e5["mismatch"] += 1
            if len(e5["first"]) < 5:
                e5["first"].append([k, z, R])
    e6 = {"checks": 0, "mismatch": 0, "first": []}
    for k in range(0, 41):
        for z in range(0, 41):
            n = 2 * k + z
            act = set(R for R in range(0, n + 3) if z >= 1 and U(k, z, R) == 2)
            pred = set(p for p in predT(k, z) if p < n + 3)
            e6["checks"] += 1
            if act != pred:
                e6["mismatch"] += 1
                if len(e6["first"]) < 5:
                    e6["first"].append([k, z])
    e7 = {"checks": 0, "mismatch": 0, "first": []}
    for z in (1, 2):
        for k in range(0, 61):
            for R in range(0, 2 * k + 3):
                e7["checks"] += 1
                if slice12(k, z, R) != U(k, z, R):
                    e7["mismatch"] += 1
                    if len(e7["first"]) < 5:
                        e7["first"].append([k, z, R])
    out["E1_engine_vs_multiset"] = e1
    out["E2_engine_vs_U"] = e2
    out["E3_engine_vs_U0"] = e3
    out["E5_random_large"] = e5
    out["E6_two_positions"] = e6
    out["E7_slices"] = e7

    print(json.dumps(out, ensure_ascii=False, sort_keys=True))

if __name__ == "__main__":
    main()
