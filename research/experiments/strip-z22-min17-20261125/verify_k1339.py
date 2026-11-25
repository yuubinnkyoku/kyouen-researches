#!/usr/bin/env python3
"""verify_k1339: audit machine for the z=22 min>=17 (floor-17) strip
(claims and scopes in the single-owner declaration note
research/log/2026-11-25-strip-z22-min17-single-owner-note.md; pre-declaration
exploration kit already published at
research/experiments/strip-z22-min17-20261125/, commit 115c0bb9).

Structural copy of the published verify_k1337.py machine (z=21 min>=16
slice, commit 08e44814) with the disclosed z 21 -> 22 textual adaptation:
rung count 15 -> 16, floor 16 -> 17, cell budget j+22 -> j+23, the z=21
line transcriptions (published K1337 cells F21f16..A921f16 + the T-Z21
m=16 theorem row) become the D3 anchor set, D5 z-grid extends to z=23 and
forwarders/counts are re-declared as in the declaration note section 4.
The pre-publication drafting machine verify_tz22.py (unpublished, local
only) had identical battery code and its predry/tamper shas are disclosed
in the declaration note section 6.

Claims audited here (all UNIVERSAL claims are proven on paper in the note
section 2; this machine independently re-checks the engine agreement and
fail-closed battery totals; battery coverage is finite by construction and
does NOT by itself prove any universal claim):
  A. 16 cell lemmas F22f17..A1022f17 (floor 17 = every Y token >= 17; s domain
     {0} U {17..}; the 16th rung A1022f17 has small token 16 -- the EIGHTH
     consecutive in-band base child of the strip series (min=16, z*(16)=30
     > 22) -- and its Y tokens stay >= 17):
     F22f17(s) = H(24;{1}uY;22) = { s==22: 1 ; else v(s+1,22,24) }
          (THIRTEENTH tail form: EVEN-z SINGLE POINT at s=22=z, NO hole, NO
          tail -- the z-relative profile IDENTICAL to z=16/z=18/z=20: the
          single@(even z) / hole+tail@(odd z) typology alternation is now
          EIGHT consecutive consistent slices (z15..z22); supplied by the
          below-band j=1 B-move child (23;Y;23)=v(s,23,23) absorption
          identity v(s,23,23)=v(s,22,23) which holds on {0} U {12..21}
          (K1334 Theorem A, k=22 EVEN: hold [0..k-1]) and breaks (0,2) at
          s=22 -- the s=22 first break point injects the mex minimum 0
          into the option set producing the single point; for s>=23 the
          pairwise break value 2 rides above the mex minimum so NO tail
          is regenerated)
     G22f17(s) = H(25;{2}uY;22) = { s==20: 0 ; s==22: 2 ; else v(s+2,22,25) }
     E22f17(s) = H(26;{3}uY;22) = { s==20: 1 ; else v(s+3,22,26) }
     D22f17(s) = H(27;{4}uY;22) = { s==18: 0 ; s==20: 2 ; else v(s+4,22,27) }
     C22f17(s) = H(28;{5}uY;22) = { s==18: 1 ; else v(s+5,22,28) }
     B22f17(s) = H(29;{6}uY;22) = { s==18: 2 ; else v(s+6,22,29) }
     A22f17(s) = H(30;{7}uY;22) = v(s+7,22,30)   (NONE -- the would-be
          break position z-5=17 is an ODD s and no odd-s A-rank deviant
          class has ever been observed; the published z=21 A21f16 break
          class s=16 falls BELOW floor 17 = part of the FIFTH definition-
          domain exclusion event; the even-z A annihilation is now 5/5
          (z=14 low-floor precedent plus z=16, z=18, z=20, z=22))
     A222f17(s) = H(31;{8}uY;22) = v(s+8,22,31)                    (NONE)
     A322f17(s) = H(32;{9}uY;22) = v(s+9,22,32)                    (NONE)
     A422f17(s) = H(33;{10}uY;22) = v(s+10,22,33)                  (NONE)
     A522f17(s) = H(34;{11}uY;22) = v(s+11,22,34)                  (NONE)
     A622f17(s) = H(35;{12}uY;22) = v(s+12,22,35)                  (NONE)
     A722f17(s) = H(36;{13}uY;22) = v(s+13,22,36)                  (NONE)
     A822f17(s) = H(37;{14}uY;22) = v(s+14,22,37)                  (NONE)
     A922f17(s) = H(38;{15}uY;22) = v(s+15,22,38)                  (NONE)
     A1022f17(s) = H(39;{16}uY;22) = v(s+16,22,39)                  (NONE;
          the EIGHTH consecutive in-band base child z*(16)=30>22; the
          (iii) C-hand child (38;{16}uY;21) is the published T-Z21
          m=16-row claim position, deviant-free by the published theorem)
     (v = published K0832 single-token closed form.)
     Deviant station structure (even-z form, the exact +2 successor of
     the published z=20 stations, confirmed on consecutive steps
     z=18 -> z=20 -> z=22): {D,C,B}@18 = {DOWN 0v2, UP 1v0, UP 2v1},
     {G,E,D}@20 = {DOWN 0v2, UP 1v0, UP 2v1}, {F,G}@22 = {UP 1v0, UP 2v1}.
     Observed deviant position set {18,20,22} = survivors {18,20} of the
     z=21 set {16,18,20} (the s=16 classes fall BELOW floor 17 = the
     FIFTH definition-domain-exclusion event) plus the newborn {22} from
     the k=22 identity first break.
  T-Z22: for every multiset X with min(X) = m >= 17:
     H(m+23; X; 22) = v(S,22,m+23), S = sum(X). Base m=17 is trivial
     absorption through the fully collapsing A1022f17 (the a=17 child);
     m >= 18 is the option-set-identity induction (a=m child = row m-1
     claim position, a>m children = K1264 stair, C-hand child = published
     T-Z21 line rows m >= 16).
  The z=21 lines used by the T-Z22/C-hand recursion (published K1337
  declaration note section 1 cell lemmas F21f16..A921f16 and theorem
  T-Z21) are re-anchored against the engine here (transcriptions checked
  independently; NOT taken on faith). NOTE: the K1337 lines for j=1..15
  carry the floor-16 Y domain {0} U {16..}; the T-Z22 C-hand positions use
  Y tokens >= 17 (subset), and the D3 anchor sweeps use the full K1337
  floor-16 domain (Y=(s,) with s >= 16) which is exactly the published
  lemma domain.

Battery (fail-closed: every gate must produce EXACTLY the declared point
count; any mismatch or failed point sets overall_bad > 0 and rc 1):
  D1 cells        1,408 pts (16 cells x 88 exhaustive floor-17 shapes,
                          s in {0} U {17..47}, arity 0..4)
  D2 strip          125 pts (m in 17..21, census-mirroring sweep,
                          cumulative 35/63/86/106/125)
  D3 z21 anchors    510 pts (15 lines x 32 s-values in {0} U {16..46}
                          = 480 + 30 T-Z21 C-hand anchors m in 16..21)
  D4 stair anchors  496 pts (16 x 31 A-on-Y child stair positions,
                          s in 17..47)
  D5 self anchors 15,336 pts (single-token engine-vs-v grid, x in 1..30,
                          z in 0..23 (z=23 needed by the below-band
                          identity pair), 21 R-points each = 15,120;
                          + 216 empty-position anchors)
  D6 deviant/collapse witnesses 24 pts (literal values, direction and
                          collapse-target checks; includes the F22f17
                          thirteenth-form single point s=22, the s=21
                          boundary and s=23 first beyond-point conforming
                          points and the far spot, the G/E/D/C/B DOWN+UP
                          reconstructions, the A22f17 even-z annihilation
                          witness at the would-be break position s=17=z-5
                          (odd s) and the fully collapsing in-band base
                          child A1022f17 spots)
  D7 extension anchors 141 pts (tail spots s in 48..55 x 16 cells = 128
                          -- ALL declared conforming (the even-form
                          signature; contrast z=21's F 8/8 TAIL 2) --,
                          strip spots m in 22..25 = 12, m=17 base spot
                          = 1)
  D8 belowband anchors 88 pts (the below-band (ii') supply-source
                          position H(23;Y;23) vs v(s,23,23) over the full
                          floor-17 census domain)

MODES: default full battery (rc 0 iff overall_bad == 0).
  --tamper-engine      rc 2 (engine block sha mismatch)
  --tamper=cell       flip one declared cell value     -> rc 1, D1 bad
  --tamper=strip      flip one D2 expected value       -> rc 1, D2 bad
  --tamper=anchor21   flip one z21 transcription value -> rc 1, D3 bad
  --tamper=stair      flip one D4 expected value       -> rc 1, D4 bad
  --tamper=deviant    flip one D6 literal              -> rc 1, D6 bad
  --tamper=ext        flip one D7 expected value       -> rc 1, D7 bad
  --tamper=belowband  flip one D8 expected value      -> rc 1, D8 bad
"""
import hashlib, json, sys
from functools import lru_cache

ENGINE_BLOCK = '''def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m

# ------------------------------------------------------------------
# Raw engines (verbatim from the published K1138 verifier block; the same
# transcription is embedded in the published y22 machine K1257).
# ------------------------------------------------------------------
@lru_cache(maxsize=6_000_000)
def H_ordered(R, X, z):
    if R == 0:
        return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return mex(opts)

@lru_cache(maxsize=6_000_000)
def H_canonical(R, X, z):
    X = tuple(sorted(X, reverse=True))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z))
        else:
            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)

def vC(x, z, R):  # canonical-engine single token
    return H_canonical(R, (x,), z)
def vO(x, z, R):  # ordered-engine single token
    return H_ordered(R, (x,), z)

# ------------------------------------------------------------------
# Published K0832 single-token closed form (transcription of the published
# single_token block in the y22 machine K1257; see report provenance).
# ------------------------------------------------------------------
def q_odd(k):
    return k if k % 2 else k - 1

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
        m = q_odd(z)
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd(x)
        if R <= m:
            return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))
'''

PIN = 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'
sha = hashlib.sha256(ENGINE_BLOCK.encode('utf-8')).hexdigest()
if '--tamper-engine' in sys.argv:
    sha = sha[:-1] + ('0' if sha[-1] != '0' else '1')
    assert sha != PIN
    print(json.dumps({'mode': 'tamper-engine', 'engine_sha': sha,
                      'engine_gate': 'FAIL'}, sort_keys=True))
    sys.exit(2)
assert sha == PIN, sha
ns = {'lru_cache': lru_cache}
exec(ENGINE_BLOCK, ns)
H = ns['H_canonical']
v = ns['single_token']

TAMPER = [a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--tamper=')]
if TAMPER:
    assert len(TAMPER) == 1 and TAMPER[0] in (
        'cell', 'strip', 'anchor21', 'stair', 'deviant', 'ext', 'belowband'), TAMPER
TAM = TAMPER[0] if TAMPER else None

# ---------------------------------------------------------------------------
# Candidate z=22 floor-17 cell closed forms (T-Z22 declaration candidates).
# ---------------------------------------------------------------------------
def F22(s):
    if s == 22:
        return 1
    return v(s + 1, 22, 24)
def G22(s):
    if s == 20:
        return 0
    if s == 22:
        return 2
    return v(s + 2, 22, 25)
def E22(s):
    if s == 20:
        return 1
    return v(s + 3, 22, 26)
def D22(s):
    if s == 18:
        return 0
    if s == 20:
        return 2
    return v(s + 4, 22, 27)
def C22(s):
    if s == 18:
        return 1
    return v(s + 5, 22, 28)
def B22(s):
    if s == 18:
        return 2
    return v(s + 6, 22, 29)
def A22(s):
    return v(s + 7, 22, 30)
def A222(s):
    return v(s + 8, 22, 31)
def A322(s):
    return v(s + 9, 22, 32)
def A422(s):
    return v(s + 10, 22, 33)
def A522(s):
    return v(s + 11, 22, 34)
def A622(s):
    return v(s + 12, 22, 35)
def A722(s):
    return v(s + 13, 22, 36)
def A822(s):
    return v(s + 14, 22, 37)
def A922(s):
    return v(s + 15, 22, 38)
def A1022(s):
    return v(s + 16, 22, 39)
CELLS = [(1, F22), (2, G22), (3, E22), (4, D22),
         (5, C22), (6, B22), (7, A22), (8, A222),
         (9, A322), (10, A422), (11, A522), (12, A622),
         (13, A722), (14, A822), (15, A922), (16, A1022)]

if TAM == 'cell':  # flip one candidate deviant value (G22f17 s=22: 2 -> 0)
    def G22(s):
        return (0 if s == 22 else
                (0 if s == 20 else v(s + 2, 22, 25)))
    CELLS = [(1, F22), (2, G22), (3, E22), (4, D22),
             (5, C22), (6, B22), (7, A22), (8, A222),
             (9, A322), (10, A422), (11, A522), (12, A622),
             (13, A722), (14, A822), (15, A922), (16, A1022)]

# ---------------------------------------------------------------------------
# Transcribed published z=21 lines (K1337 declarations; floor-16 domain
# {0} u {16..}; used by the z=22 C-hand recursion for j=1..15; the j=16
# C-hand child (38;{16}uY;21) is the published T-Z21 theorem line (min=16),
# anchored by the D3 C-hand sweep). Re-anchored against the engine by D3.
# ---------------------------------------------------------------------------
def F21(s):
    if s == 20:
        return 1
    if s >= 22:
        return 2
    return v(s + 1, 21, 23)
def G21(s):
    if s == 20:
        return 0
    return v(s + 2, 21, 24)
def E21(s):
    if s == 18:
        return 1
    if s == 20:
        return 2
    return v(s + 3, 21, 25)
def D21(s):
    if s == 18:
        return 0
    return v(s + 4, 21, 26)
def C21(s):
    if s == 16:
        return 1
    if s == 18:
        return 2
    return v(s + 5, 21, 27)
def B21(s):
    if s == 16:
        return 0
    return v(s + 6, 21, 28)
def A21(s):
    if s == 16:
        return 2
    return v(s + 7, 21, 29)
def A221(s):
    return v(s + 8, 21, 30)
def A321(s):
    return v(s + 9, 21, 31)
def A421(s):
    return v(s + 10, 21, 32)
def A521(s):
    return v(s + 11, 21, 33)
def A621(s):
    return v(s + 12, 21, 34)
def A721(s):
    return v(s + 13, 21, 35)
def A821(s):
    return v(s + 14, 21, 36)
def A921(s):
    return v(s + 15, 21, 37)
LINES21 = [(1, F21), (2, G21), (3, E21), (4, D21),
           (5, C21), (6, B21), (7, A21), (8, A221), (9, A321),
           (10, A421), (11, A521), (12, A621), (13, A721), (14, A821),
           (15, A921)]

if TAM == 'anchor21':  # flip one transcription value (A21f16 s=16: 2 -> 0)
    def A21(s):
        return 0 if s == 16 else v(s + 7, 21, 29)
    LINES21 = [(1, F21), (2, G21), (3, E21), (4, D21),
               (5, C21), (6, B21), (7, A21), (8, A221), (9, A321),
               (10, A421), (11, A521), (12, A621), (13, A721), (14, A821),
               (15, A921)]


def parts(s, lo, arity):
    out = []
    def rec(rem, k, cur):
        if rem == 0:
            if 1 <= len(cur) <= arity:
                out.append(tuple(cur))
            return
        if k == arity:
            return
        for t in range(lo, rem + 1):
            if cur and t < cur[-1]:
                continue
            cur.append(t)
            rec(rem - t, k + 1, cur)
            cur.pop()
    rec(s, 0, [])
    return out


gates = {}

def run_gate(gname, declared_pts, pts, bad):
    if pts != declared_pts and not TAM:
        bad += abs(pts - declared_pts)  # fail-closed count mismatch
    gates[gname] = {'declared_pts': declared_pts, 'pts': pts, 'bad': bad}
    return bad

total_bad = 0

# --- D1: exhaustive cell sweeps ---------------------------------------------
declared = 1408
pts = 0; bad = 0
for j, fn in CELLS:
    R = j + 23
    for s in [0] + list(range(17, 48)):
        ys = [()] if s == 0 else parts(s, 17, 4)
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            hv = H(R, X, 22)
            pts += 1
            if hv != fn(s):
                bad += 1
    H.cache_clear()
total_bad += run_gate('D1_cells', declared, pts, bad)

# --- D2: T-Z22 strip sweep ---------------------------------------------------
declared = 125
pts = 0; bad = 0
if TAM == 'strip':
    flipped = set()
for m in range(17, 22):
    for S in range(m, m + 40):
        for X in parts(max(S - m, 0), m, 3):
            XX = tuple(sorted((m,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(m + 23, XX, 22)
            ev = v(S, 22, m + 23)
            pts += 1
            if TAM == 'strip' and (m, S, XX) not in flipped and len(flipped) == 0:
                flipped.add((m, S, XX)); ev = (ev + 1) % 3
            if hv != ev:
                bad += 1
    H.cache_clear()
total_bad += run_gate('D2_strip', declared, pts, bad)

# --- D3: z21 line transcriptions + T-Z21 C-hand anchors ---------------------
declared = 510
pts = 0; bad = 0
for j, fn in LINES21:
    for s in [0] + list(range(16, 47)):
        X = (j, s) if s > 0 else (j,)
        hv = H(j + 22, tuple(sorted(X, reverse=True)), 21)
        ev = fn(s)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
# T-Z21 C-hand anchors: the (iii) child of the T-Z22 claim position at
# min=m is (m+22; X; 21) = the published T-Z21 m-row claim position.
# m=16 anchors the A1022f17 cell C-hand child (the T-Z21 m=16 row);
# m in 17..21 anchor the strip rows.
for m in range(16, 22):
    for i in range(1, 6):
        X = tuple(sorted((m, m + i), reverse=True))
        hv = H(m + 22, X, 21)
        ev = v(2 * m + i, 21, m + 22)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D3_z21_anchors', declared, pts, bad)

# --- D4: stair anchors (A-on-Y children of cell parents) ---------------------
declared = 496
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(17, 48):
        child = tuple(sorted((j, s - 1), reverse=True))
        hv = H(j + 22, child, 22)
        ev = v(s + j - 1, 22, j + 22)
        if TAM == 'stair' and j == 3 and s == 17:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D4_stair_anchors', declared, pts, bad)

# --- D5: self anchors (single-token v grid + empty positions) ---------------
grid = []
for x in range(1, 31):
    for z in range(0, 24):
        rs = [0, 1, 5, 14, 17, 18, 19, 20, 21, 22, 23, 24,
              25, 26, 27, 28, 29, 30, x + z - 1, x + z, x + z + 1]
        for R in rs:
            if R < 0 or R > 81:
                continue
            grid.append((x, z, R))
declared = len(grid) + 216
pts = 0; bad = 0
for (x, z, R) in grid:
    hv = H(R, (x,), z)
    ev = v(x, z, R)
    pts += 1
    if hv != ev:
        bad += 1
H.cache_clear()
for R in range(0, 9):
    for z in range(0, 24):
        hv = H(R, (), z)
        pts += 1
        if hv != 0:
            bad += 1
total_bad += run_gate('D5_self_anchors', declared, pts, bad)

# --- D6: deviant / collapse witness literals --------------------------------
WITNESSES = [
    # (j, s, declared_value, collapse_target, direction)
    (1, 17, 0, 0, 'FLAT'),    # F22f17 in-identity flat (identity holds ..21)
    (1, 21, 0, 0, 'FLAT'),    # F22f17 boundary FLAT s=21=z-1 (no hole: even)
    (1, 22, 1, 0, 'UP'),      # F22f17 THIRTEENTH-form single s=22=z UP 1v0
                              # (the k=22 first break injects mex 0)
    (1, 23, 0, 0, 'FLAT'),    # F22f17 first beyond-point conforming (no tail)
    (1, 52, 0, 0, 'FLAT'),    # F22f17 far spot conforming (even signature)
    (2, 17, 1, 1, 'FLAT'),    # G22f17 flat (mex-absorption probe point)
    (2, 18, 0, 0, 'FLAT'),    # G22f17 flat over the z=21 G supply-free zone
    (2, 20, 0, 2, 'DOWN'),    # G22f17 DOWN (G21f16 s=20 DOWN supply mirror)
    (2, 22, 2, 1, 'UP'),      # G22f17 UP 2v1 (F22f17 s=22 supply mirror)
    (2, 24, 1, 1, 'FLAT'),    # G22f17 break-region flat
    (3, 17, 0, 0, 'FLAT'),    # E22f17 flat
    (3, 20, 1, 0, 'UP'),      # E22f17 UP 1v0 (E21f16 s=20 UP supply mirror)
    (4, 17, 1, 1, 'FLAT'),    # D22f17 flat (below the D supply position)
    (4, 18, 0, 2, 'DOWN'),    # D22f17 DOWN 0v2 (D21f16 s=18 supply mirror)
    (4, 20, 2, 1, 'UP'),      # D22f17 UP 2v1 (E22f17 s=20 UP supply mirror)
    (5, 18, 1, 0, 'UP'),      # C22f17 UP 1v0 (C21f16 s=18 UP supply mirror)
    (5, 20, 0, 0, 'FLAT'),    # C22f17 flat at the supply position s=20
    (6, 18, 2, 1, 'UP'),      # B22f17 UP 2v1 (B21f16 s=16 class excluded;
                              # the s=18 position is the +2 successor)
    (6, 20, 1, 1, 'FLAT'),    # B22f17 flat (D/C UP supplies ride above mex)
    (7, 17, 0, 0, 'FLAT'),    # A22f17 EVEN-Z ANNIHILATION witness at the
                              # would-be break position s=17=z-5 (odd s)
    (7, 20, 0, 0, 'FLAT'),    # A22f17 flat at the supply position s=20
    (8, 18, 1, 1, 'FLAT'),    # A222f17 conforming
    (16, 17, 1, 1, 'FLAT'),   # A1022f17 base-child cell spot (in-band base)
    (16, 52, 1, 1, 'FLAT'),   # A1022f17 far spot
]
declared = len(WITNESSES)
pts = 0; bad = 0
for (j, s, val, cval, direction) in WITNESSES:
    if TAM == 'deviant' and j == 1 and s == 22:
        val = (val + 1) % 3
    X = (j, s)
    hv = H(j + 23, X, 22)
    col = v(s + j, 22, j + 23)
    pts += 1
    ok = (hv == val) and (col == cval)
    d = 'UP' if val > col else ('DOWN' if val < col else 'FLAT')
    if d != direction:
        ok = False
    if not ok:
        bad += 1
total_bad += run_gate('D6_deviant_witnesses', declared, pts, bad)

# --- D7: extension anchors (tail spots + strip spots + base spot) ----------
declared = 141
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(48, 56):
        X = (j, s)
        hv = H(j + 23, X, 22)
        ev = fn(s)
        if TAM == 'ext' and j == 1 and s == 48:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
for m in range(22, 26):
    for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
        X = tuple(sorted(shp, reverse=True))
        hv = H(m + 23, X, 22)
        ev = v(sum(X), 22, m + 23)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
hv = H(40, (17, 17), 22)
ev = v(34, 22, 40)
pts += 1
if hv != ev or ev != 0:
    bad += 1
total_bad += run_gate('D7_extension_anchors', declared, pts, bad)

# --- D8: belowband (ii') supply-source anchors -------------------------------
# H(23; Y; 23) = v(s, 23, 23) for every floor-17 multiset Y (empty at s=0
# by K1312-stair-type collapse). This is the below-band j=1 B-move child
# whose absorption identity v(s,23,23)=v(s,22,23) holds on {0} U {12..21}
# (K1334 Theorem A, k=22 EVEN: [0..k-1]) and breaks (0,2) at s=22 then
# uniformly (2,1) for all s>=23 (the s=22 first break point injects the
# mex minimum 0 producing the F22f17 single point; no tail regeneration).
declared = 88
pts = 0; bad = 0
for s in [0] + list(range(17, 48)):
    ys = [()] if s == 0 else parts(s, 17, 4)
    for y in ys:
        hv = H(23, y, 23)
        ev = v(s, 23, 23)
        if TAM == 'belowband' and pts == 0:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D8_belowband_anchors', declared, pts, bad)

battery_declared = sum(g['declared_pts'] for g in gates.values())
battery_pts = sum(g['pts'] for g in gates.values())
res = {'machine': 'verify_k1339', 'engine_sha': sha, 'mode': TAM or 'full',
       'gates': gates, 'battery_declared_pts': battery_declared,
       'battery_pts': battery_pts, 'overall_bad': total_bad,
       'result': 'FAIL' if total_bad else 'PASS'}
print(json.dumps(res, sort_keys=True, separators=(',', ':')))
sys.exit(1 if total_bad else 0)
