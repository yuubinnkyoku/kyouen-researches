#!/usr/bin/env python3
"""verify_k1335: audit machine for the z=20 min>=15 (floor-15) strip
(claims and scopes in the single-owner declaration note
research/log/2026-11-25-strip-z20-min15-single-owner-note.md; pre-declaration
exploration kit already published at
research/experiments/strip-z20-min15-20261125/, commit 2cc16d34).

Structural copy of the published verify_k1330.py machine (z=19 min>=14
slice, commit ca6d12bc) with the disclosed z 19 -> 20 textual adaptation:
rung count 13 -> 14, floor 14 -> 15, cell budget j+20 -> j+21, the z=19
line transcriptions (published K1330 cells F19f14..A719f14 + the T-Z19
m=14 theorem row) become the D3 anchor set, D5 z-grid extends to z=21 and
forwarders/counts are re-declared as in the declaration note section 4.

Claims audited here (all UNIVERSAL claims are proven on paper in the note
section 2; this machine independently re-checks the engine agreement and
fail-closed battery totals; battery coverage is finite by construction and
does NOT by itself prove any universal claim):
  A.14 cell lemmas F20f15..A820f15 (floor 15 = every Y token >= 15; s domain
     {0} U {15..}; the 14th rung A820f15 has small token 14 -- the SIXTH
     consecutive in-band base child of the strip series (min=14, z*(14)=26
     > 20) -- and its Y tokens stay >= 15):
     F20f15(s) = H(22;{1}uY;20) = { s==20: 1 ; else v(s+1,20,22) }
          (ELEVENTH tail form: SINGLE UP at s=20=z, no hole, no tail --
          the even-z single-point typology now 3/3 (z=16 s=16, z=18
          s=18, z=20 s=20); supplied by the below-band j=1 B-move child
          (21;Y;21)=v(s,21,21) absorption identity v(s,21,21)=v(s,20,21)
          which holds on {0} U {12..19} (K1334 Theorem A, k=20 even:
          [0..k-1]) and breaks (0,2) at s=20 then uniformly (2,1) for all
          s>=21 -- the s=20 first break point injects the mex minimum 0
          into the option set supplying the single UP; the s>=21 region
          rides above the mex minimum, regenerating no tail, exactly the
          z=18 even-z mechanism)
     G20f15(s) = H(23;{2}uY;20) = { s==18: 0 ; s==20: 2 ; else v(s+2,20,23) }
     E20f15(s) = H(24;{3}uY;20) = { s==18: 1 ; else v(s+3,20,24) }
     D20f15(s) = H(25;{4}uY;20) = { s==16: 0 ; s==18: 2 ; else v(s+4,20,25) }
     C20f15(s) = H(26;{5}uY;20) = { s==16: 1 ; else v(s+5,20,26) }
     B20f15(s) = H(27;{6}uY;20) = { s==16: 2 ; else v(s+6,20,27) }
     A20f15(s) = H(28;{7}uY;20) = v(s+7,20,28)                    (NONE;
          the B20f15 s=16 UP supply 2 rides above the mex minimum -- the
          A-rank fully collapses at even z; the z=19 A-break class at
          s=14=z-5 is floor-excluded, the FOURTH recorded definition-domain
          exclusion event)
     A220f15(s) = H(29;{8}uY;20) = v(s+8,20,29)                    (NONE)
     A320f15(s) = H(30;{9}uY;20) = v(s+9,20,30)                    (NONE)
     A420f15(s) = H(31;{10}uY;20) = v(s+10,20,31)                  (NONE)
     A520f15(s) = H(32;{11}uY;20) = v(s+11,20,32)                  (NONE)
     A620f15(s) = H(33;{12}uY;20) = v(s+12,20,33)                  (NONE)
     A720f15(s) = H(34;{13}uY;20) = v(s+13,20,34)                  (NONE)
     A820f15(s) = H(35;{14}uY;20) = v(s+14,20,35)                  (NONE;
          the SIXTH consecutive in-band base child z*(14)=26>20; the (iii)
          C-hand child (34;{14}uY;19) is the published T-Z19 m=14-row
          claim position, deviant-free by the published theorem)
     (v = published K0832 single-token closed form.)
     Deviant station triplet (even-z form, 2/2 with z=18): value multiset
     {DOWN:0, UP:1, UP:2} at positions {D,C,B}@16, {G,E,D}@18, {F,G}@20.
  T-Z20: for every multiset X with min(X) = m >= 15:
     H(m+21; X; 20) = v(S,20,m+21), S = sum(X). Base m=15 is trivial
     absorption through the fully collapsing A820f15 (the a=15 child);
     m >= 16 is the option-set-identity induction (a=m child = row m-1
     claim position, a>m children = K1264 stair, C-hand child = published
     T-Z19 line rows m >= 14).
  The z=19 lines used by the T-Z20/C-hand recursion (published K1330
  declaration note section 1 cell lemmas F19f14..A719f14 and theorem
  T-Z19) are re-anchored against the engine here (transcriptions checked
  independently; NOT taken on faith). NOTE: the K1330 lines for j=1..13
  carry the floor-14 Y domain {0} U {14..}; the T-Z20 C-hand positions use
  Y tokens >= 15 (subset), and the D3 anchor sweeps use the full K1330
  floor-14 domain (Y=(s,) with s >= 14) which is exactly the published
  lemma domain.

Battery (fail-closed: every gate must produce EXACTLY the declared point
count; any mismatch or failed point sets overall_bad > 0 and rc 1):
  D1 cells        1,470 pts (14 cells x 105 exhaustive floor-15 shapes,
                          s in {0} U {15..45}, arity 0..4)
  D2 strip          185 pts (m in 15..19, S in m..m+39, Y parts >= m,
                          arity(Y) <= 3, engine vs v; identical sweep to
                          the frozen census kit section (c), cumulative
                          55/99/134/162/185)
  D3 z19 anchors    459 pts (13 lines x 33 s-values in {0} U {14..45}
                          = 429 + 30 T-Z19 C-hand anchors m in 14..19)
  D4 stair anchors  434 pts (14 x 31 A-on-Y child stair positions,
                          s in 15..45)
  D5 self anchors 14,058 pts (single-token engine-vs-v grid, x in 1..30,
                          z in 0..21 (z=21 needed by the below-band
                          identity pair), 21 R-points each = 13,860;
                          + 198 empty-position anchors)
  D6 deviant/collapse witnesses 23 pts (literal values, direction and
                          collapse-target checks; includes the F20f15
                          eleventh-form SINGLE UP point s=20, the s=19
                          boundary flat, the s=18 mirror flats, the
                          G/E/D/C/B DOWN+UP reconstructions, the A20f15
                          A-rank collapse witness absorbing the B20f15
                          UP supply and the fully collapsing in-band base
                          child A820f15 spots)
  D7 extension anchors 125 pts (tail spots s in 46..53 x 14 cells = 112
                          -- ALL FLAT (the even-z form carries no tail to
                          pierce the census window) --, strip spots
                          m in 20..23 = 12, m=15 base spot = 0)
  D8 belowband anchors 105 pts (the below-band (ii') supply-source
                          position H(21;Y;21) vs v(s,21,21) over the full
                          floor-15 census domain)

MODES: default full battery (rc 0 iff overall_bad == 0).
  --tamper-engine      rc 2 (engine block sha mismatch)
  --tamper=cell       flip one declared cell value     -> rc 1, D1 bad
  --tamper=strip      flip one D2 expected value       -> rc 1, D2 bad
  --tamper=anchor19   flip one z19 transcription value -> rc 1, D3 bad
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
        'cell', 'strip', 'anchor19', 'stair', 'deviant', 'ext', 'belowband'), TAMPER
TAM = TAMPER[0] if TAMPER else None

# ---------------------------------------------------------------------------
# Declared z=20 floor-15 cell closed forms (K1335 claims). Domain: all Y
# tokens >= 15, s = sum(Y) in {0} U {15..} (Y blank iff s=0), arity arbitrary.
# ---------------------------------------------------------------------------
def F20(s):
    if s == 20:
        return 1
    return v(s + 1, 20, 22)
def G20(s):
    if s == 18:
        return 0
    if s == 20:
        return 2
    return v(s + 2, 20, 23)
def E20(s):
    if s == 18:
        return 1
    return v(s + 3, 20, 24)
def D20(s):
    if s == 16:
        return 0
    if s == 18:
        return 2
    return v(s + 4, 20, 25)
def C20(s):
    if s == 16:
        return 1
    return v(s + 5, 20, 26)
def B20(s):
    if s == 16:
        return 2
    return v(s + 6, 20, 27)
def A20(s):
    return v(s + 7, 20, 28)
def A220(s):
    return v(s + 8, 20, 29)
def A320(s):
    return v(s + 9, 20, 30)
def A420(s):
    return v(s + 10, 20, 31)
def A520(s):
    return v(s + 11, 20, 32)
def A620(s):
    return v(s + 12, 20, 33)
def A720(s):
    return v(s + 13, 20, 34)
def A820(s):
    return v(s + 14, 20, 35)
CELLS = [(1, F20), (2, G20), (3, E20), (4, D20),
         (5, C20), (6, B20), (7, A20), (8, A220),
         (9, A320), (10, A420), (11, A520), (12, A620),
         (13, A720), (14, A820)]
CELL_NAMES = {1: 'F', 2: 'G', 3: 'E', 4: 'D',
              5: 'C', 6: 'B', 7: 'A', 8: 'A2', 9: 'A3', 10: 'A4',
              11: 'A5', 12: 'A6', 13: 'A7', 14: 'A8'}

if TAM == 'cell':  # flip one declared deviant value (G20f15 s=20: 2 -> 1)
    def G20(s):
        return (1 if s == 20 else
                (0 if s == 18 else
                 v(s + 2, 20, 23)))
    CELLS = [(1, F20), (2, G20), (3, E20), (4, D20),
             (5, C20), (6, B20), (7, A20), (8, A220),
             (9, A320), (10, A420), (11, A520), (12, A620),
             (13, A720), (14, A820)]

# ---------------------------------------------------------------------------
# Transcribed published z=19 lines (K1330 declaration note section 1
# statements; floor-14 domain {0} U {14..} for the 13 cells; used by the
# z=20 C-hand recursion for j=1..13; the j=14 C-hand child is the T-Z19
# theorem line (min=14), anchored by the D3 C-hand sweep). Re-anchored
# against the engine by D3 (independent of the K1330 official verification
# state).
# ---------------------------------------------------------------------------
def F19(s):
    if s == 18:
        return 1
    if s >= 20:
        return 2
    return v(s + 1, 19, 21)
def G19(s):
    if s == 18:
        return 0
    return v(s + 2, 19, 22)
def E19(s):
    if s == 16:
        return 1
    if s == 18:
        return 2
    return v(s + 3, 19, 23)
def D19(s):
    if s == 16:
        return 0
    return v(s + 4, 19, 24)
def C19(s):
    if s == 14:
        return 1
    if s == 16:
        return 2
    return v(s + 5, 19, 25)
def B19(s):
    if s == 14:
        return 0
    return v(s + 6, 19, 26)
def A19(s):
    if s == 14:
        return 2
    return v(s + 7, 19, 27)
def A219(s):
    return v(s + 8, 19, 28)
def A319(s):
    return v(s + 9, 19, 29)
def A419(s):
    return v(s + 10, 19, 30)
def A519(s):
    return v(s + 11, 19, 31)
def A619(s):
    return v(s + 12, 19, 32)
def A719(s):
    return v(s + 13, 19, 33)
LINES19 = [(1, F19), (2, G19), (3, E19), (4, D19),
           (5, C19), (6, B19), (7, A19), (8, A219), (9, A319),
           (10, A419), (11, A519), (12, A619), (13, A719)]

if TAM == 'anchor19':  # flip one transcription value (B19f14 s=14: 0 -> 2)
    def B19(s):
        return 2 if s == 14 else v(s + 6, 19, 26)
    LINES19 = [(1, F19), (2, G19), (3, E19), (4, D19),
               (5, C19), (6, B19), (7, A19), (8, A219), (9, A319),
               (10, A419), (11, A519), (12, A619), (13, A719)]


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
declared = 1470
pts = 0; bad = 0
for j, fn in CELLS:
    R = j + 21
    for s in [0] + list(range(15, 46)):
        ys = [()] if s == 0 else parts(s, 15, 4)
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            hv = H(R, X, 20)
            pts += 1
            if hv != fn(s):
                bad += 1
    H.cache_clear()
total_bad += run_gate('D1_cells', declared, pts, bad)

# --- D2: T-Z20 strip sweep ---------------------------------------------------
declared = 185
pts = 0; bad = 0
if TAM == 'strip':
    flipped = set()
for m in range(15, 20):
    for S in range(m, m + 40):
        for X in parts(max(S - m, 0), m, 3):
            XX = tuple(sorted((m,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(m + 21, XX, 20)
            ev = v(S, 20, m + 21)
            pts += 1
            if TAM == 'strip' and (m, S, XX) not in flipped and len(flipped) == 0:
                flipped.add((m, S, XX)); ev = (ev + 1) % 3
            if hv != ev:
                bad += 1
    H.cache_clear()
total_bad += run_gate('D2_strip', declared, pts, bad)

# --- D3: z19 line transcriptions + T-Z19 C-hand anchors ---------------------
declared = 459
pts = 0; bad = 0
for j, fn in LINES19:
    for s in [0] + list(range(14, 46)):
        X = (j, s) if s > 0 else (j,)
        hv = H(j + 20, tuple(sorted(X, reverse=True)), 19)
        ev = fn(s)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
# T-Z19 C-hand anchors: the (iii) child of the T-Z20 claim position at
# min=m is (m+20; X; 19) = the published T-Z19 m-row claim position.
# m=14 anchors the A820f15 cell C-hand child (the T-Z19 m=14 row);
# m in 15..19 anchor the strip rows.
for m in range(14, 20):
    for i in range(1, 6):
        X = tuple(sorted((m, m + i), reverse=True))
        hv = H(m + 20, X, 19)
        ev = v(2 * m + i, 19, m + 20)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D3_z19_anchors', declared, pts, bad)

# --- D4: stair anchors (A-on-Y children of cell parents) ---------------------
declared = 434
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(15, 46):
        child = tuple(sorted((j, s - 1), reverse=True))
        hv = H(j + 20, child, 20)
        ev = v(s + j - 1, 20, j + 20)
        if TAM == 'stair' and j == 3 and s == 15:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D4_stair_anchors', declared, pts, bad)

# --- D5: self anchors (single-token v grid + empty positions) ---------------
grid = []
for x in range(1, 31):
    for z in range(0, 22):
        rs = [0, 1, 5, 14, 17, 18, 19, 20, 21, 22, 23, 24,
              25, 26, 27, 28, 29, 30, x + z - 1, x + z, x + z + 1]
        for R in rs:
            if R < 0 or R > 81:
                continue
            grid.append((x, z, R))
declared = len(grid) + 198
pts = 0; bad = 0
for (x, z, R) in grid:
    hv = H(R, (x,), z)
    ev = v(x, z, R)
    pts += 1
    if hv != ev:
        bad += 1
H.cache_clear()
for R in range(0, 9):
    for z in range(0, 22):
        hv = H(R, (), z)
        pts += 1
        if hv != 0:
            bad += 1
total_bad += run_gate('D5_self_anchors', declared, pts, bad)

# --- D6: deviant / collapse witness literals --------------------------------
WITNESSES = [
    # (j, s, declared_value, collapse_target, direction)
    (1, 15, 0, 0, 'FLAT'),    # F20f15 in-identity flat
    (1, 18, 1, 1, 'FLAT'),    # F20f15 flat over the F19f14 DOWN supply
    (1, 19, 0, 0, 'FLAT'),    # F20f15 flat at the identity final hold point
    (1, 20, 1, 0, 'UP'),      # F20f15 ELEVENTH-form SINGLE UP s=20 1v0
    (1, 21, 0, 0, 'FLAT'),    # F20f15 break-region first point (no tail)
    (1, 52, 0, 0, 'FLAT'),    # F20f15 far flat (window-external)
    (2, 16, 0, 0, 'FLAT'),    # G20f15 flat (z19-mirror collapse continues)
    (2, 18, 0, 2, 'DOWN'),    # G20f15 DOWN (G19f14 s=18 DOWN supply)
    (2, 19, 1, 1, 'FLAT'),    # G20f15 mirror-check flat
    (2, 20, 2, 1, 'UP'),      # G20f15 UP (F20f15 s=20 UP supply mirror)
    (3, 16, 1, 1, 'FLAT'),    # E20f15 mex-absorption of the E19f14 supply
    (3, 18, 1, 0, 'UP'),      # E20f15 UP (G20f15 s=18 DOWN supply mirror)
    (3, 20, 0, 0, 'FLAT'),    # E20f15 flat (G20f15 UP supply absorbed)
    (4, 16, 0, 2, 'DOWN'),    # D20f15 DOWN (E19f14 s=16 supply mirror)
    (4, 18, 2, 1, 'UP'),      # D20f15 UP (E20f15 s=18 UP supply mirror)
    (5, 16, 1, 0, 'UP'),      # C20f15 UP (C19f14 s=16 UP supply)
    (5, 18, 0, 0, 'FLAT'),    # C20f15 flat (D20f15 UP supply absorbed)
    (6, 16, 2, 1, 'UP'),      # B20f15 UP (C20f15 s=16 UP supply mirror)
    (7, 16, 0, 0, 'FLAT'),    # A20f15 absorbs the B20f15 UP supply above mex
    (7, 20, 0, 0, 'FLAT'),    # A20f15 flat at the supply position s=20
    (14, 16, 1, 1, 'FLAT'),   # A820f15 base-child cell spot (in-band base)
    (14, 20, 1, 1, 'FLAT'),   # A820f15 at the supply position s=20
    (14, 52, 1, 1, 'FLAT'),   # A820f15 far tail spot
]
declared = len(WITNESSES)
pts = 0; bad = 0
for (j, s, val, cval, direction) in WITNESSES:
    if TAM == 'deviant' and j == 1 and s == 20:
        val = (val + 1) % 3
    X = (j, s)
    hv = H(j + 21, X, 20)
    col = v(s + j, 20, j + 21)
    pts += 1
    ok = (hv == val) and (col == cval)
    d = 'UP' if val > col else ('DOWN' if val < col else 'FLAT')
    if d != direction:
        ok = False
    if not ok:
        bad += 1
total_bad += run_gate('D6_deviant_witnesses', declared, pts, bad)

# --- D7: extension anchors (tail spots + strip spots + base spot) ----------
declared = 125
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(46, 54):
        X = (j, s)
        hv = H(j + 21, X, 20)
        ev = fn(s)
        if TAM == 'ext' and j == 1 and s == 46:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
for m in range(20, 24):
    for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
        X = tuple(sorted(shp, reverse=True))
        hv = H(m + 21, X, 20)
        ev = v(sum(X), 20, m + 21)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
hv = H(36, (15, 15), 20)
ev = v(30, 20, 36)
pts += 1
if hv != ev or ev != 0:
    bad += 1
total_bad += run_gate('D7_extension_anchors', declared, pts, bad)

# --- D8: belowband (ii') supply-source anchors -------------------------------
# H(21; Y; 21) = v(s, 21, 21) for every floor-15 multiset Y (empty at s=0
# by K1312-stair-type collapse; the identity v(s,21,21)=v(s,20,21) below).
# This is the below-band j=1 B-move child whose absorption identity
# v(s,21,21)=v(s,20,21) holds on {0} U {12..19} (K1334 Theorem A, k=20
# even: [0..k-1]) and breaks (0,2) at s=20, then uniformly (2,1) for all
# s>=21 (supplying the F20f15 single UP at s=20; the break-region values
# ride above the mex minimum and regenerate no tail).
declared = 105
pts = 0; bad = 0
for s in [0] + list(range(15, 46)):
    ys = [()] if s == 0 else parts(s, 15, 4)
    for y in ys:
        hv = H(21, y, 21)
        ev = v(s, 21, 21)
        if TAM == 'belowband' and pts == 0:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D8_belowband_anchors', declared, pts, bad)

battery_declared = sum(g['declared_pts'] for g in gates.values())
battery_pts = sum(g['pts'] for g in gates.values())
res = {'machine': 'verify_k1335', 'engine_sha': sha, 'mode': TAM or 'full',
       'gates': gates, 'battery_declared_pts': battery_declared,
       'battery_pts': battery_pts, 'overall_bad': total_bad,
       'result': 'FAIL' if total_bad else 'PASS'}
print(json.dumps(res, sort_keys=True, separators=(',', ':')))
sys.exit(1 if total_bad else 0)
