#!/usr/bin/env python3
"""verify_k1344: audit machine for the z=23 min>=18 (floor-18) strip
(claims and scopes in the single-owner declaration note
research/log/2026-11-25-strip-z23-min18-single-owner-note.md; pre-declaration
exploration kit already published at
research/experiments/strip-z23-min18-20261125/, commit 25522d56).

Structural copy of the published verify_k1339.py machine (z=22 min>=17
slice, publication commit e2c79d64) with the disclosed z 22 -> 23 textual
adaptation: rung count 16 -> 17, floor 17 -> 18, cell budget j+23 ->
j+24, the z=22 line transcriptions (published K1339 cells
F22f17..A1022f17 + the T-Z22 m=17 theorem row) become the D3 anchor
set, the D5 z-grid extends to z=24 (the below-band identity pair needs
z=24) and forwarders/counts are re-declared as in the declaration note
section 4. Renamed from the pre-publication drafting machine verify_tz23.py
(unpublished, local only, identical battery code) after the declaration
note push (commit 66ac2775); predry/tamper shas of BOTH machines are
disclosed in the declaration note section 4/section 6.

Claims audited here (all UNIVERSAL claims are proven on paper in the note
section 2; this machine independently re-checks the engine agreement and
fail-closed battery totals; battery coverage is finite by construction and
does NOT by itself prove any universal claim):
  A. 17 cell lemmas F23f18..A1123f18 (floor 18 = every Y token >= 18; s
     domain {0} U {18..}; the 17th rung A1123f18 has small token 17 -- the
     NINTH consecutive in-band base child of the strip series (min=17,
     z*(17)=33 > 23) -- and its Y tokens stay >= 18):
     F23f18(s) = H(25;{1}uY;23) = { s==22: 1 ; s>=24: 2 ; else v(s+1,23,25) }
          (FOURTEENTH tail form: ODD-z HOLE+TAIL -- single point at
          s=22=z-1 DOWN 1v2, CONFORMING hole at s=23=z, tail value 2 for
          s>=24; the z-relative profile IDENTICAL to z=15/z=17/z=19/z=21:
          the single@(even z) / hole+tail@(odd z) typology alternation is
          now NINE consecutive consistent slices (z15..z23); supplied by
          the below-band j=1 B-move child (24;Y;24)=v(s,24,24) whose
          absorption identity v(s,24,24)=v(s,23,24) holds on {0} U
          {12..23} and breaks uniformly (0,1) for s>=24 -- the s=24
          uniform break injects the mex minimum 0 into the option set
          for every s>=24 while the conforming value rides 1, so the
          tail value is 2 for all s>=24)
     G23f18(s) = H(26;{2}uY;23) = { s==22: 0 ; else v(s+2,23,26) }
     E23f18(s) = H(27;{3}uY;23) = { s==20: 1 ; s==22: 2 ; else v(s+3,23,27) }
     D23f18(s) = H(28;{4}uY;23) = { s==20: 0 ; else v(s+4,23,28) }
     C23f18(s) = H(29;{5}uY;23) = { s==18: 1 ; s==20: 2 ; else v(s+5,23,29) }
     B23f18(s) = H(30;{6}uY;23) = { s==18: 0 ; else v(s+6,23,30) }
     A23f18(s) = H(31;{7}uY;23) = { s==18: 2 ; else v(s+7,23,31) }
          (A-RANK BREAK REBIRTH at s=18=z-5: the odd-z A-break class is
          now 4/4 (z=15,17,19,21,23) against the even-z annihilation 5/5;
          the s=18 station rides UP 2v0)
     A223f18(s) = H(32;{8}uY;23) = v(s+8,23,32)                    (NONE)
     A323f18(s) = H(33;{9}uY;23) = v(s+9,23,33)                    (NONE)
     A423f18(s) = H(34;{10}uY;23) = v(s+10,23,34)                  (NONE)
     A523f18(s) = H(35;{11}uY;23) = v(s+11,23,35)                  (NONE)
     A623f18(s) = H(36;{12}uY;23) = v(s+12,23,36)                  (NONE)
     A723f18(s) = H(37;{13}uY;23) = v(s+13,23,37)                  (NONE)
     A823f18(s) = H(38;{14}uY;23) = v(s+14,23,38)                  (NONE)
     A923f18(s) = H(39;{15}uY;23) = v(s+15,23,39)                  (NONE)
     A1023f18(s) = H(40;{16}uY;23) = v(s+16,23,40)                 (NONE)
     A1123f18(s) = H(41;{17}uY;23) = v(s+17,23,41)                 (NONE;
          the NINTH consecutive in-band base child z*(17)=33>23; the
          (iii) C-hand child (40;{17}uY;22) is the published T-Z22
          m=17-row claim position, deviant-free by the published theorem)
     (v = published K0832 single-token closed form.)
     Deviant station structure (odd-z form, the exact +2 successor of
     the published z=21 stations): s=18: {B,C,A} = {DOWN 0v1, DOWN 1v2,
     UP 2v0}, s=20: {D,E,C} = {DOWN 0v1, DOWN 1v2, UP 2v0}, s=22:
     {G,F,E} = {DOWN 0v1, DOWN 1v2, UP 2v0}. Observed deviant position
     set {18,20,22} = the z=22 set {18,20,22} surviving the floor 17->18
     shift with NO exclusion (the THIRD consecutive even->odd transition
     without a definition-domain exclusion; contrast z=22 where the
     z=21 s=16 classes fell below floor 17) plus the F23f18 single
     point at s=22=z-1 and its hole at s=23=z; the odd-z pattern value
     assignment {0 at j=24-s, 1 at j=23-s, 2 at j=25-s} mirrors the
     even-z {0 at j=z-s, 1 at z+1-s, 2 at z+2-s} through the A-rank.
  T-Z23: for every multiset X with min(X) = m >= 18:
     H(m+24; X; 23) = v(S,23,m+24), S = sum(X). Base m=18 is trivial
     absorption through the fully collapsing A1123f18 (the a=18 child);
     m >= 19 is the option-set-identity induction (a=m child = row m-1
     claim position, a>m children = K1264 stair, C-hand child = published
     T-Z22 line rows m >= 17).
     Corollary 1: z*(18)=34 > 23 closes the z=23 slice (in-band base
     child completes the induction).
     Corollary 2: min=18 row z in {0..23}; residual band z in {24..33},
     frontier z=34.
  The z=22 lines used by the T-Z23/C-hand recursion (published K1339
  declaration note section 1 cell lemmas F22f17..A1022f17 and theorem
  T-Z22) are re-anchored against the engine here (transcriptions checked
  independently; NOT taken on faith). NOTE: the K1339 lines for j=1..16
  carry the floor-17 Y domain {0} U {17..}; the T-Z23 C-hand positions use
  Y tokens >= 18 (subset), and the D3 anchor sweeps use the full K1339
  floor-17 domain (Y=(s,) with s >= 17) which is exactly the published
  lemma domain.

Battery (fail-closed: every gate must produce EXACTLY the declared point
count; any mismatch or failed point sets overall_bad > 0 and rc 1):
  D1 cells        1,377 pts (17 cells x 81 exhaustive floor-18 shapes,
                          s in {0} U {18..48}, arity 0..4)
  D2 strip          108 pts (m in 18..22, census-mirroring sweep,
                          cumulative 28/51/71/90/108)
  D3 z22 anchors    542 pts (16 lines x 32 s-values in {0} U {17..47}
                          = 512 + 30 T-Z22 C-hand anchors m in 17..22)
  D4 stair anchors   527 pts (17 x 31 A-on-Y child stair positions,
                          s in 18..48)
  D5 self anchors 16,725 pts (single-token engine-vs-v grid, x in 1..30,
                          z in 0..24 (z=24 needed by the below-band
                          identity pair), 22 R-points each = 16,500;
                          + 225 empty-position anchors)
  D6 deviant/collapse witnesses 23 pts (literal values, direction and
                          collapse-target checks; includes the F23f18
                          fourteenth-form single point s=22=z-1, the
                          s=23=z hole-conforming point and s=24 first
                          tail point and the far spot, the G/E/D/C/B/A
                          station reconstructions, the A23f18 odd-z
                          break-rebirth witness at s=18=z-5 (UP 2v0)
                          and the fully collapsing in-band base child
                          A1123f18 spots)
  D7 extension anchors 149 pts (tail spots s in 49..56 x 17 cells = 136
                          -- F cell declared 2 at all 8 spots (the odd-
                          form signature; contrast z=22's ALL-conforming
                          even signature), the other 16 cells conform
                          -- strip spots m in 23..26 = 12, m=18 base
                          spot = 1)
  D8 belowband anchors 81 pts (the below-band (ii') supply-source
                          position H(24;Y;24) vs v(s,24,24) over the full
                          floor-18 census domain)

MODES: default full battery (rc 0 iff overall_bad == 0).
  --tamper-engine      rc 2 (engine block sha mismatch)
  --tamper=cell       flip one declared cell value     -> rc 1, D1 bad
  --tamper=strip      flip one D2 expected value       -> rc 1, D2 bad
  --tamper=anchor22   flip one z22 transcription value -> rc 1, D3 bad
  --tamper=stair      flip one D4 expected value       -> rc 1, D4 bad
  --tamper=deviant    flip one D6 literal              -> rc 1, D6 bad
  --tamper=ext        flip one D7 expected value        -> rc 1, D7 bad
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
        'cell', 'strip', 'anchor22', 'stair', 'deviant', 'ext', 'belowband'), TAMPER
TAM = TAMPER[0] if TAMPER else None

# ---------------------------------------------------------------------------
# Candidate z=23 floor-18 cell closed forms (T-Z23 declaration candidates).
# ---------------------------------------------------------------------------
def F23(s):
    if s == 22:
        return 1
    if s >= 24:
        return 2
    return v(s + 1, 23, 25)
def G23(s):
    if s == 22:
        return 0
    return v(s + 2, 23, 26)
def E23(s):
    if s == 20:
        return 1
    if s == 22:
        return 2
    return v(s + 3, 23, 27)
def D23(s):
    if s == 20:
        return 0
    return v(s + 4, 23, 28)
def C23(s):
    if s == 18:
        return 1
    if s == 20:
        return 2
    return v(s + 5, 23, 29)
def B23(s):
    if s == 18:
        return 0
    return v(s + 6, 23, 30)
def A23(s):
    if s == 18:
        return 2
    return v(s + 7, 23, 31)
def A223(s):
    return v(s + 8, 23, 32)
def A323(s):
    return v(s + 9, 23, 33)
def A423(s):
    return v(s + 10, 23, 34)
def A523(s):
    return v(s + 11, 23, 35)
def A623(s):
    return v(s + 12, 23, 36)
def A723(s):
    return v(s + 13, 23, 37)
def A823(s):
    return v(s + 14, 23, 38)
def A923(s):
    return v(s + 15, 23, 39)
def A1023(s):
    return v(s + 16, 23, 40)
def A1123(s):
    return v(s + 17, 23, 41)
CELLS = [(1, F23), (2, G23), (3, E23), (4, D23),
         (5, C23), (6, B23), (7, A23), (8, A223),
         (9, A323), (10, A423), (11, A523), (12, A623),
         (13, A723), (14, A823), (15, A923), (16, A1023),
         (17, A1123)]

if TAM == 'cell':  # flip one candidate deviant value (F23f18 s=22: 1 -> 0)
    def F23(s):
        return (0 if s == 22 else
                (2 if s >= 24 else v(s + 1, 23, 25)))
    CELLS = [(1, F23), (2, G23), (3, E23), (4, D23),
             (5, C23), (6, B23), (7, A23), (8, A223),
             (9, A323), (10, A423), (11, A523), (12, A623),
             (13, A723), (14, A823), (15, A923), (16, A1023),
             (17, A1123)]

# ---------------------------------------------------------------------------
# Transcribed published z=22 lines (K1339 declarations; floor-17 domain
# {0} u {17..}; used by the z=23 C-hand recursion for j=1..16; the j=17
# C-hand child (40;{17}uY;22) is the published T-Z22 theorem line (min=17),
# anchored by the D3 C-hand sweep. Re-anchored against the engine by D3.
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
LINES22 = [(1, F22), (2, G22), (3, E22), (4, D22),
           (5, C22), (6, B22), (7, A22), (8, A222), (9, A322),
           (10, A422), (11, A522), (12, A622), (13, A722), (14, A822),
           (15, A922), (16, A1022)]

if TAM == 'anchor22':  # flip one transcription value (F22f17 s=22: 1 -> 0)
    def F22(s):
        return 0 if s == 22 else v(s + 1, 22, 24)
    LINES22 = [(1, F22), (2, G22), (3, E22), (4, D22),
               (5, C22), (6, B22), (7, A22), (8, A222), (9, A322),
               (10, A422), (11, A522), (12, A622), (13, A722), (14, A822),
               (15, A922), (16, A1022)]


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
declared = 1377
pts = 0; bad = 0
for j, fn in CELLS:
    R = j + 24
    for s in [0] + list(range(18, 49)):
        ys = [()] if s == 0 else parts(s, 18, 4)
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            hv = H(R, X, 23)
            pts += 1
            if hv != fn(s):
                bad += 1
    H.cache_clear()
total_bad += run_gate('D1_cells', declared, pts, bad)

# --- D2: T-Z23 strip sweep ---------------------------------------------------
declared = 108
pts = 0; bad = 0
if TAM == 'strip':
    flipped = set()
for m in range(18, 23):
    for S in range(m, m + 40):
        for X in parts(max(S - m, 0), m, 3):
            XX = tuple(sorted((m,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(m + 24, XX, 23)
            ev = v(S, 23, m + 24)
            pts += 1
            if TAM == 'strip' and (m, S, XX) not in flipped and len(flipped) == 0:
                flipped.add((m, S, XX)); ev = (ev + 1) % 3
            if hv != ev:
                bad += 1
    H.cache_clear()
total_bad += run_gate('D2_strip', declared, pts, bad)

# --- D3: z22 line transcriptions + T-Z22 C-hand anchors ---------------------
declared = 542
pts = 0; bad = 0
for j, fn in LINES22:
    for s in [0] + list(range(17, 48)):
        X = (j, s) if s > 0 else (j,)
        hv = H(j + 23, tuple(sorted(X, reverse=True)), 22)
        ev = fn(s)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
# T-Z22 C-hand anchors: the (iii) child of the T-Z23 claim position at
# min=m is (m+23; X; 22) = the published T-Z22 m-row claim position.
# m=17 anchors the A1123f18 cell C-hand child (the T-Z22 m=17 row);
# m in 18..22 anchor the strip rows.
for m in range(17, 23):
    for i in range(1, 6):
        X = tuple(sorted((m, m + i), reverse=True))
        hv = H(m + 23, X, 22)
        ev = v(2 * m + i, 22, m + 23)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D3_z22_anchors', declared, pts, bad)

# --- D4: stair anchors (A-on-Y children of cell parents) ---------------------
declared = 527
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(18, 49):
        child = tuple(sorted((j, s - 1), reverse=True))
        hv = H(j + 23, child, 23)
        ev = v(s + j - 1, 23, j + 23)
        if TAM == 'stair' and j == 3 and s == 18:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D4_stair_anchors', declared, pts, bad)

# --- D5: self anchors (single-token v grid + empty positions) ---------------
grid = []
for x in range(1, 31):
    for z in range(0, 25):
        rs = [0, 1, 5, 14, 17, 18, 19, 20, 21, 22, 23, 24,
              25, 26, 27, 28, 29, 30, 31, x + z - 1, x + z, x + z + 1]
        for R in rs:
            if R < 0 or R > 81:
                continue
            grid.append((x, z, R))
declared = len(grid) + 225
pts = 0; bad = 0
for (x, z, R) in grid:
    hv = H(R, (x,), z)
    ev = v(x, z, R)
    pts += 1
    if hv != ev:
        bad += 1
H.cache_clear()
for R in range(0, 9):
    for z in range(0, 25):
        hv = H(R, (), z)
        pts += 1
        if hv != 0:
            bad += 1
total_bad += run_gate('D5_self_anchors', declared, pts, bad)

# --- D6: deviant / collapse witness literals --------------------------------
WITNESSES = [
    # (j, s, declared_value, collapse_target, direction)
    (1, 18, 1, 1, 'FLAT'),    # F23f18 first in-domain FLAT (identity holds
                              # through s=23; conforming v(s+1,23,25))
    (1, 22, 1, 2, 'DOWN'),    # F23f18 FOURTEENTH-form single point s=22=z-1
                              # (DOWN 1v2; the s=22 class absorbs the
                              # conforming value 2 out of the option set)
    (1, 23, 0, 0, 'FLAT'),    # F23f18 s=23=z HOLE conforming (the odd-z
                              # hole: NO deviant at s=z)
    (1, 24, 2, 0, 'UP'),      # F23f18 first tail spot s=24=z+1 (tail open;
                              # the below-band break injects mex 0)
    (1, 52, 2, 0, 'UP'),      # F23f18 far spot (the tail rides to the
                              # horizon)
    (2, 18, 0, 0, 'FLAT'),    # G23f18 flat (mex-absorption probe point)
    (2, 20, 0, 0, 'FLAT'),    # G23f18 flat over the z=22 G22f17 s=20
                              # supply ride (value absorbed)
    (2, 22, 0, 1, 'DOWN'),    # G23f18 DOWN 0v1 (F22f17 s=22 supply mirror:
                              # the 1^1=0 conforming slot is displaced)
    (2, 24, 1, 1, 'FLAT'),    # G23f18 break-region flat
    (3, 18, 1, 1, 'FLAT'),    # E23f18 flat
    (3, 20, 1, 2, 'DOWN'),    # E23f18 DOWN 1v2 (E22f17 s=20 supply mirror)
    (3, 22, 2, 0, 'UP'),      # E23f18 UP 2v0 (D22f17 s=20 supply ride
                              # displaced UP)
    (4, 18, 0, 0, 'FLAT'),    # D23f18 flat below the supply position
    (4, 20, 0, 1, 'DOWN'),    # D23f18 DOWN 0v1 (D22f17 s=20 supply ride)
    (5, 18, 1, 2, 'DOWN'),    # C23f18 DOWN 1v2 (C22f17 s=18 supply ride)
    (5, 20, 2, 0, 'UP'),      # C23f18 UP 2v0 (station value-2 class)
    (6, 18, 0, 1, 'DOWN'),    # B23f18 DOWN 0v1 (station value-0 class)
    (6, 20, 1, 1, 'FLAT'),    # B23f18 flat at the supply position s=20
    (7, 18, 2, 0, 'UP'),      # A23f18 A-RANK BREAK REBIRTH witness at
                              # s=18=z-5 (odd-z break birth now 4/4, UP 2v0)
    (7, 20, 0, 0, 'FLAT'),    # A23f18 flat at the supply position s=20
    (8, 18, 1, 1, 'FLAT'),    # A223f18 conforming
    (17, 18, 0, 0, 'FLAT'),   # A1123f18 base-child cell spot (in-band base)
    (17, 52, 0, 0, 'FLAT'),   # A1123f18 far spot
]
declared = len(WITNESSES)
pts = 0; bad = 0
for (j, s, val, cval, direction) in WITNESSES:
    if TAM == 'deviant' and j == 1 and s == 22:
        val = (val + 1) % 3
    X = (j, s)
    hv = H(j + 24, X, 23)
    col = v(s + j, 23, j + 24)
    pts += 1
    ok = (hv == val) and (col == cval)
    d = 'UP' if val > col else ('DOWN' if val < col else 'FLAT')
    if d != direction:
        ok = False
    if not ok:
        bad += 1
total_bad += run_gate('D6_deviant_witnesses', declared, pts, bad)

# --- D7: extension anchors (tail spots + strip spots + base spot) ----------
declared = 149
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(49, 57):
        X = (j, s)
        hv = H(j + 24, X, 23)
        ev = fn(s)
        if TAM == 'ext' and j == 1 and s == 49:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
for m in range(23, 27):
    for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
        X = tuple(sorted(shp, reverse=True))
        hv = H(m + 24, X, 23)
        ev = v(sum(X), 23, m + 24)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
hv = H(42, (18, 18), 23)
ev = v(36, 23, 42)
pts += 1
if hv != ev or ev != 1:
    bad += 1
total_bad += run_gate('D7_extension_anchors', declared, pts, bad)

# --- D8: belowband (ii') supply-source anchors -------------------------------
# H(24; Y; 24) = v(s,24,24) for every floor-18 multiset Y (empty at s=0
# by K1312-stair-type collapse). This is the below-band j=1 B-move child
# whose absorption identity v(s,24,24)=v(s,23,24) holds on {0} U {12..23}
# (K1334 Theorem A, k=23 ODD: hold [0..k-1]) and breaks uniformly (0,1)
# at s>=24 (the s=24 break point injects the mex minimum 0 producing the
# F23f18 tail; the s<=23 hold keeps the F cell conforming including the
# s=23=z hole position).
declared = 81
pts = 0; bad = 0
for s in [0] + list(range(18, 49)):
    ys = [()] if s == 0 else parts(s, 18, 4)
    for y in ys:
        hv = H(24, y, 24)
        ev = v(s, 24, 24)
        if TAM == 'belowband' and pts == 0:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D8_belowband_anchors', declared, pts, bad)

battery_declared = sum(g['declared_pts'] for g in gates.values())
battery_pts = sum(g['pts'] for g in gates.values())
res = {'machine': 'verify_k1344', 'engine_sha': sha, 'mode': TAM or 'full',
       'gates': gates, 'battery_declared_pts': battery_declared,
       'battery_pts': battery_pts, 'overall_bad': total_bad,
       'result': 'FAIL' if total_bad else 'PASS'}
print(json.dumps(res, sort_keys=True, separators=(',', ':')))
sys.exit(1 if total_bad else 0)
