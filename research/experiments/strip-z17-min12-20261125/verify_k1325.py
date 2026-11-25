#!/usr/bin/env python3
"""verify_k1325: audit machine for the z=17 min>=12 (floor-12) strip
(claims and scopes in the single-owner declaration note
research/log/2026-11-25-strip-z17-min12-single-owner-note.md;
pre-declaration exploration kit already published at
research/experiments/strip-z17-min12-20261125/, commit 2c74f1c6).

Claims audited here (all UNIVERSAL claims are proven on paper in the note
section 2; this machine independently re-checks the engine agreement and
fail-closed battery totals; battery coverage is finite by construction and
does NOT by itself prove any universal claim):
  A.11 cell lemmas F17f12..A517f12 (floor 12 = every Y token >= 12; s domain
     {0} U {12..}; the 11th rung A517f12 has small token 11 -- the THIRD
     consecutive in-band base child of the strip series (min=11, z*(11)=21
     > 17) -- and its Y tokens stay >= 12):
     F17f12(s) = H(19;{1}uY;17) = { s==16: 1 ; s>=18: 2 ; else v(s+1,17,19) }
          (1 DOWN at 16, hole at 17, CONSTANT-2 UP TAIL for ALL s>=18 --
          the F-family EIGHTH tail typology: the persistent 2-tail REBORN
          one slice after the z=16 single-point seventh form, with the
          SAME profile as the z=15 sixth form shifted by +2; supplied by
          the below-band j=1 B-move child (18;Y;18)=v(s,18,18) absorption
          identity break at s>=18 against the stair value v(s,17,18))
     G17f12(s) = H(20;{2}uY;17) = { s==16: 0 ; else v(s+2,17,20) }      (1 DOWN)
     E17f12(s) = H(21;{3}uY;17) = { s==14: 1 ; s==16: 2 ; else v(s+3,17,21) }
     D17f12(s) = H(22;{4}uY;17) = { s==14: 0 ; else v(s+4,17,22) }     (1 DOWN)
     C17f12(s) = H(23;{5}uY;17) = { s==12: 1 ; s==14: 2 ; else v(s+5,17,23) }
     B17f12(s) = H(24;{6}uY;17) = { s==12: 0 ; else v(s+6,17,24) }     (1 DOWN)
     A17f12(s) = H(25;{7}uY;17) = { s==12: 2 ; else v(s+7,17,25) }     (1 UP
          -- the A-RANK BREAKS the z=16 four-rung collapse run)
     A217f12(s) = H(26;{8}uY;17) = v(s+8,17,26)                        (NONE)
     A317f12(s) = H(27;{9}uY;17) = v(s+9,17,27)                        (NONE)
     A417f12(s) = H(28;{10}uY;17) = v(s+10,17,28)                      (NONE)
     A517f12(s) = H(29;{11}uY;17) = v(s+11,17,29)                      (NONE;
          the (iii) C-hand child (28;{11}uY;16) is the published T-Z16
          m=11-row claim position, deviant-free by the published theorem)
     (v = published K0832 single-token closed form.)
  T-Z17: for every multiset X with min(X) = m >= 12:
     H(m+18; X; 17) = v(S,17,m+18), S = sum(X). Base m=12 is trivial
     absorption through the fully collapsing A517f12 (the a=12 child);
     m >= 13 is the option-set-identity induction (a=m child = row m-1
     claim position, a>m children = K1264 stair, C-hand child = published
     T-Z16 line).
  The z=16 lines used by the T-Z17/C-hand recursion (published K1322
  declaration note section 1 cell lemmas F16f11..A416f11 and theorem
  T-Z16) are re-anchored against the engine here (transcriptions checked
  independently; NOT taken on faith). NOTE: the K1322 lines for j=1..10
  carry the floor-11 Y domain {0} U {11..}; the T-Z17 C-hand positions use
  Y tokens >= 12 which is a subset, and the D3 anchor sweeps use the full
  K1322 floor-11 domain (Y=(s,) with s >= 11) which is exactly the
  published lemma domain.

Battery (fail-closed: every gate must produce EXACTLY the declared point
count; any mismatch or failed point sets overall_bad > 0 and rc 1):
  D1 cells        1,705 pts (11 cells x 155 exhaustive floor-12 shapes,
                          s in {0} U {12..42}, arity 0..4)
  D2 strip          358 pts (m in 12..16, S in m..m+39, Y parts >= m,
                          arity(Y) <= 3, engine vs v; identical sweep to
                          the frozen census kit section (c), cumulative
                          107/191/259/314/358)
  D3 z16 anchors    350 pts (10 lines x 32 s-values in {0} U {11..41}
                          = 320 + 30 T-Z16 C-hand anchors m in 11..16)
  D4 stair anchors  341 pts (11 x 31 A-on-Y child stair positions)
  D5 self anchors 12,141 pts (single-token engine-vs-v grid, x in 1..30,
                          z in 0..18, 21 R-points each = 11,970;
                          + 171 empty-position anchors)
  D6 deviant/collapse witnesses 22 pts (literal values, direction and
                          collapse-target checks; includes the F17f12
                          eighth-form DOWN point and tail start, the
                          s=17 hole, the FLAT absorptions at the
                          in-run supply points of G17/D17/B17/A217 and
                          the far-tail spot, and the fully collapsing
                          A-rank cells' spots incl. the in-band base child)
  D7 extension anchors 101 pts (tail spots s in 43..50 x 11 cells = 88
                          -- the F tail rows are engine==form=2 mismatches
                          against the collapse by design --, strip spots
                          m in 17..20 = 12, m=12 base spot = 1)
  D8 belowband anchors 155 pts (the (ii') supply-source position
                          H(18;Y;18) vs v(s,18,18) over the full floor-12
                          census domain: the stair/empty collapse whose
                          absorption identity v(s,18,18)=v(s,17,18) holds
                          on {0} U {12..17} and breaks at s>=18, supplying
                          the F17f12 constant-2 tail)

MODES: default full battery (rc 0 iff overall_bad == 0).
  --tamper-engine      rc 2 (engine block sha mismatch)
  --tamper=cell       flip one declared cell value     -> rc 1, D1 bad
  --tamper=strip      flip one D2 expected value       -> rc 1, D2 bad
  --tamper=anchor16   flip one z16 transcription value -> rc 1, D3 bad
  --tamper=stair      flip one D4 expected value       -> rc 1, D4 bad
  --tamper=deviant    flip one D6 literal              -> rc 1, D6 bad
  --tamper=ext        flip one D7 expected value       -> rc 1, D7 bad
  --tamper=belowband  flip one D8 expected value       -> rc 1, D8 bad
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
        'cell', 'strip', 'anchor16', 'stair', 'deviant', 'ext', 'belowband'), TAMPER
TAM = TAMPER[0] if TAMPER else None

# ---------------------------------------------------------------------------
# Declared z=17 floor-12 cell closed forms (K1325 claims). Domain: all Y
# tokens >= 12, s = sum(Y) in {0} U {12..} (Y blank iff s=0), arity arbitrary.
# ---------------------------------------------------------------------------
def F17(s):
    if s == 16:
        return 1
    if s >= 18:
        return 2
    return v(s + 1, 17, 19)
def G17(s):
    if s == 16:
        return 0
    return v(s + 2, 17, 20)
def E17(s):
    if s == 14:
        return 1
    if s == 16:
        return 2
    return v(s + 3, 17, 21)
def D17(s):
    if s == 14:
        return 0
    return v(s + 4, 17, 22)
def C17(s):
    if s == 12:
        return 1
    if s == 14:
        return 2
    return v(s + 5, 17, 23)
def B17(s):
    if s == 12:
        return 0
    return v(s + 6, 17, 24)
def A17(s):
    if s == 12:
        return 2
    return v(s + 7, 17, 25)
def A217(s):
    return v(s + 8, 17, 26)
def A317(s):
    return v(s + 9, 17, 27)
def A417(s):
    return v(s + 10, 17, 28)
def A517(s):
    return v(s + 11, 17, 29)
CELLS = [(1, F17), (2, G17), (3, E17), (4, D17),
         (5, C17), (6, B17), (7, A17), (8, A217),
         (9, A317), (10, A417), (11, A517)]
CELL_NAMES = {1: 'F', 2: 'G', 3: 'E', 4: 'D',
              5: 'C', 6: 'B', 7: 'A', 8: 'A2', 9: 'A3', 10: 'A4',
              11: 'A5'}

if TAM == 'cell':  # flip one declared deviant value (G17f12 s=16: 0 -> 1)
    def G17(s):
        return (1 if s == 16 else
                v(s + 2, 17, 20))
    CELLS = [(1, F17), (2, G17), (3, E17), (4, D17),
             (5, C17), (6, B17), (7, A17), (8, A217),
             (9, A317), (10, A417), (11, A517)]

# ---------------------------------------------------------------------------
# Transcribed published z=16 lines (K1322 declaration note section 1
# statements; floor-11 domain {0} U {11..} for the 10 cells; used by the
# z=17 C-hand recursion for j=1..10; the j=11 C-hand child is the T-Z16
# theorem line (min=11), anchored by the D3 C-hand sweep). Re-anchored
# against the engine by D3 (independent of the K1322 official verification
# state).
# ---------------------------------------------------------------------------
def F16(s):
    if s == 16:
        return 1
    return v(s + 1, 16, 18)
def G16(s):
    if s == 14:
        return 0
    if s == 16:
        return 2
    return v(s + 2, 16, 19)
def E16(s):
    if s == 14:
        return 1
    return v(s + 3, 16, 20)
def D16(s):
    if s == 12:
        return 0
    if s == 14:
        return 2
    return v(s + 4, 16, 21)
def C16(s):
    if s == 12:
        return 1
    return v(s + 5, 16, 22)
def B16(s):
    if s == 12:
        return 2
    return v(s + 6, 16, 23)
def A16(s):
    return v(s + 7, 16, 24)
def A216(s):
    return v(s + 8, 16, 25)
def A316(s):
    return v(s + 9, 16, 26)
def A416(s):
    return v(s + 10, 16, 27)
LINES16 = [(1, F16), (2, G16), (3, E16), (4, D16),
           (5, C16), (6, B16), (7, A16), (8, A216), (9, A316), (10, A416)]

if TAM == 'anchor16':  # flip one transcription value
    def B16(s):
        return 1 if s == 12 else v(s + 6, 16, 23)
    LINES16 = [(1, F16), (2, G16), (3, E16), (4, D16),
               (5, C16), (6, B16), (7, A16), (8, A216), (9, A316),
               (10, A416)]


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
declared = 1705
pts = 0; bad = 0
for j, fn in CELLS:
    R = j + 18
    for s in [0] + list(range(12, 43)):
        ys = [()] if s == 0 else parts(s, 12, 4)
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            hv = H(R, X, 17)
            pts += 1
            if hv != fn(s):
                bad += 1
    H.cache_clear()
total_bad += run_gate('D1_cells', declared, pts, bad)

# --- D2: T-Z17 strip sweep ---------------------------------------------------
declared = 358
pts = 0; bad = 0
if TAM == 'strip':
    flipped = set()
for m in range(12, 17):
    for S in range(m, m + 40):
        for X in parts(max(S - m, 0), m, 3):
            XX = tuple(sorted((m,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(m + 18, XX, 17)
            ev = v(S, 17, m + 18)
            pts += 1
            if TAM == 'strip' and (m, S, XX) not in flipped and len(flipped) == 0:
                flipped.add((m, S, XX)); ev = (ev + 1) % 3
            if hv != ev:
                bad += 1
    H.cache_clear()
total_bad += run_gate('D2_strip', declared, pts, bad)

# --- D3: z16 line transcriptions + T-Z16 C-hand anchors ---------------------
declared = 350
pts = 0; bad = 0
for j, fn in LINES16:
    for s in [0] + list(range(11, 42)):
        X = (j, s) if s > 0 else (j,)
        hv = H(j + 17, tuple(sorted(X, reverse=True)), 16)
        ev = fn(s)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
# T-Z16 C-hand anchors: the (iii) child of the T-Z17 claim position at
# min=m is (m+17; X; 16) = the published T-Z16 m-row claim position.
# m=11 anchors the A517f12 cell C-hand; m in 12..16 anchor the strip rows.
for m in range(11, 17):
    for i in range(1, 6):
        X = tuple(sorted((m, m + i), reverse=True))
        hv = H(m + 17, X, 16)
        ev = v(2 * m + i, 16, m + 17)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D3_z16_anchors', declared, pts, bad)

# --- D4: stair anchors (A-on-Y children of cell parents) ---------------------
declared = 341
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(12, 43):
        child = tuple(sorted((j, s - 1), reverse=True))
        hv = H(j + 17, child, 17)
        ev = v(s + j - 1, 17, j + 17)
        if TAM == 'stair' and j == 3 and s == 12:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D4_stair_anchors', declared, pts, bad)

# --- D5: self anchors (single-token v grid + empty positions) ---------------
grid = []
for x in range(1, 31):
    for z in range(0, 19):
        rs = [0, 1, 5, 14, 17, 18, 19, 20, 21, 22, 23, 24,
              25, 26, 27, 28, 29, 30, x + z - 1, x + z, x + z + 1]
        for R in rs:
            if R < 0 or R > 81:
                continue
            grid.append((x, z, R))
declared = len(grid) + 171
pts = 0; bad = 0
for (x, z, R) in grid:
    hv = H(R, (x,), z)
    ev = v(x, z, R)
    pts += 1
    if hv != ev:
        bad += 1
H.cache_clear()
for R in range(0, 9):
    for z in range(0, 19):
        hv = H(R, (), z)
        pts += 1
        if hv != 0:
            bad += 1
total_bad += run_gate('D5_self_anchors', declared, pts, bad)

# --- D6: deviant / collapse witness literals --------------------------------
WITNESSES = [
    # (j, s, Y, declared_value, collapse_target, direction)
    (1, 14, (14,), 1, 1, 'FLAT'),    # F17f12 collapse (E16f11 non-dev region)
    (1, 16, (16,), 1, 2, 'DOWN'),    # F17f12 DOWN (F16f11 UP supply)
    (1, 17, (17,), 0, 0, 'FLAT'),    # F17f12 EIGHTH-form hole at s=17
    (1, 18, (18,), 2, 0, 'UP'),      # F17f12 constant-2 tail start (break s>=18)
    (1, 41, (41,), 2, 0, 'UP'),      # F17f12 far tail spot (persistent)
    (2, 14, (14,), 0, 0, 'FLAT'),    # G17f12 collapse at the G16f11 s=14 supply
    (2, 16, (16,), 0, 1, 'DOWN'),    # G17f12 DOWN
    (2, 18, (18,), 1, 1, 'FLAT'),    # G17f12 tail absorption (F tail absorbed)
    (3, 14, (14,), 1, 2, 'DOWN'),    # E17f12 DOWN (E16f11 s=14 supply)
    (3, 16, (16,), 2, 0, 'UP'),      # E17f12 UP (G17f12 s=16 supply)
    (4, 12, (12,), 0, 0, 'FLAT'),    # D17f12 collapse at the D16f11 s=12 supply
    (4, 14, (14,), 0, 1, 'DOWN'),    # D17f12 DOWN
    (4, 16, (16,), 1, 1, 'FLAT'),    # D17f12 collapse at the E17f12 s=16 dev
    (5, 12, (12,), 1, 2, 'DOWN'),    # C17f12 DOWN (C16f11 s=12 supply)
    (5, 14, (14,), 2, 0, 'UP'),      # C17f12 UP (D17f12 s=14 supply)
    (6, 12, (12,), 0, 1, 'DOWN'),    # B17f12 DOWN (B16f11 s=12 supply)
    (6, 14, (14,), 1, 1, 'FLAT'),    # B17f12 collapse at the C17f12 s=14 dev
    (7, 12, (12,), 2, 0, 'UP'),      # A17f12 UP -- the A-RANK break
    (8, 12, (12,), 1, 1, 'FLAT'),    # A217f12 absorbs the A17f12 UP
    (9, 12, (12,), 0, 0, 'FLAT'),    # A317f12 full-collapse spot
    (11, 12, (12,), 0, 0, 'FLAT'),   # A517f12 base-child cell spot (in-band base)
    (11, 41, (41,), 0, 0, 'FLAT'),   # A517f12 far tail spot
]
declared = len(WITNESSES)
pts = 0; bad = 0
for (j, s, y, val, cval, direction) in WITNESSES:
    if TAM == 'deviant' and j == 7 and s == 12:
        val = (val + 1) % 3
    X = tuple(sorted((j,) + y, reverse=True))
    hv = H(j + 18, X, 17)
    col = v(s + j, 17, j + 18)
    pts += 1
    ok = (hv == val) and (col == cval)
    d = 'UP' if val > col else ('DOWN' if val < col else 'FLAT')
    if d != direction:
        ok = False
    if not ok:
        bad += 1
total_bad += run_gate('D6_deviant_witnesses', declared, pts, bad)

# --- D7: extension anchors (tail spots + strip spots + base spot) ----------
declared = 101
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(43, 51):
        X = tuple(sorted((j, s), reverse=True))
        hv = H(j + 18, X, 17)
        ev = fn(s)
        if TAM == 'ext' and j == 1 and s == 43:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
for m in range(17, 21):
    for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
        X = tuple(sorted(shp, reverse=True))
        hv = H(m + 18, X, 17)
        ev = v(sum(X), 17, m + 18)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
hv = H(30, (12, 12), 17)
ev = v(24, 17, 30)
pts += 1
if hv != ev or ev != 1:
    bad += 1
total_bad += run_gate('D7_extension_anchors', declared, pts, bad)

# --- D8: belowband (ii') supply-source anchors -------------------------------
# H(18; Y; 18) = v(s, 18, 18) for every floor-12 multiset Y (K1264 stair at
# R=18 <= 18+min(Y); empty at s=0 by K1312). This is the below-band j=1
# B-move child whose absorption identity v(s,18,18)=v(s,17,18) holds on
# {0} U {12..17} and breaks at s>=18 (supplying the F17f12 constant-2 tail).
declared = 155
pts = 0; bad = 0
for s in [0] + list(range(12, 43)):
    ys = [()] if s == 0 else parts(s, 12, 4)
    for y in ys:
        hv = H(18, y, 18)
        ev = v(s, 18, 18)
        if TAM == 'belowband' and pts == 0:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D8_belowband_anchors', declared, pts, bad)

battery_declared = sum(g['declared_pts'] for g in gates.values())
battery_pts = sum(g['pts'] for g in gates.values())
res = {'machine': 'verify_k1325', 'engine_sha': sha, 'mode': TAM or 'full',
       'gates': gates, 'battery_declared_pts': battery_declared,
       'battery_pts': battery_pts, 'overall_bad': total_bad,
       'result': 'FAIL' if total_bad else 'PASS'}
print(json.dumps(res, sort_keys=True, separators=(',', ':')))
sys.exit(1 if total_bad else 0)
