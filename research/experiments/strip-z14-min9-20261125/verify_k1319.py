#!/usr/bin/env python3
"""verify_k1319: audit machine for the z=14 min>=9 (floor-9) strip
(claims and scopes in the single-owner declaration note
research/log/2026-11-25-strip-z14-min9-single-owner-note.md;
pre-declaration exploration kit already published at
research/experiments/strip-z14-min9-20261125/).

Claims audited here (all UNIVERSAL claims are proven on paper in the note
section 2; this machine independently re-checks the engine agreement and
fail-closed battery totals; battery coverage is finite by construction and
does NOT by itself prove any universal claim):
  A.8 cell lemmas F14f9..A214f9 (floor 9 = every Y token >= 9; s domain
     {0} U {9..}; the 8th rung A214f9 has small token 8 -- one rank BELOW
     the published z=13 A-cell -- and its Y tokens stay >= 9):
     F14f9(s) = H(16;{1}uY;14) = { s==14: 1 ; else v(s+1,14,16) }
     G14f9(s) = H(17;{2}uY;14) = { s==12: 0 ; s==14: 2 ; else v(s+2,14,17) }
     E14f9(s) = H(18;{3}uY;14) = { s==12: 1 ; else v(s+3,14,18) }
     D14f9(s) = H(19;{4}uY;14) = { s==10: 0 ; s==12: 2 ; else v(s+4,14,19) }
     C14f9(s) = H(20;{5}uY;14) = { s==10: 1 ; else v(s+5,14,20) }
     B14f9(s) = H(21;{6}uY;14) = { s==10: 2 ; else v(s+6,14,21) }
     A14f9(s) = H(22;{7}uY;14) = v(s+7,14,22)          (NO deviants)
     A214f9(s) = H(23;{8}uY;14) = v(s+8,14,23)         (NO deviants)
     (v = published K0832 single-token closed form.)
  T-Z14: for every multiset X with min(X) = m >= 9:
     H(m+15; X; 14) = v(S,14,m+15), S = sum(X).
  The z=13 lines used by the T-Z14/C-hand recursion (published K1317 note
  cell lemmas F13f8..A13f8 and theorem T-Z13(8)) are re-anchored against
  the engine here (transcriptions checked independently; NOT taken on
  faith). NOTE: the K1317 lines for j=1..7 carry the floor-8 Y domain
  {0} U {8..}; the T-Z14 C-hand positions use Y tokens >= 9 which is a
  subset, and the D3 anchor sweeps use the full K1317 floor-8 domain
  (Y=(s,) with s >= 8) which is exactly the published lemma domain.

Battery (fail-closed: every gate must produce EXACTLY the declared point
count; any mismatch or failed point sets overall_bad > 0 and rc 1):
  D1 cells        2,496 pts (8 cells x 312 exhaustive floor-9 shapes,
                          s in {0} U {9..40}, arity 0..4)
  D2 strip          791 pts (m in 9..13, S in m..m+39, Y parts >= m,
                          arity(Y) <= 3, engine vs v)
  D3 z13 anchors    297 pts (8 lines x 34 s-values in {0} U {8..40}
                          = 272 + 25 T-Z13 C-hand anchors m in 9..13)
  D4 stair anchors  256 pts (8 x 32 A-on-Y child stair positions)
  D5 self anchors 4,464 pts (single-token engine-vs-v grid, x in 1..27,
                          z in 0..15, 10 R-points each = 4,320;
                          + 144 empty-position anchors)
  D6 deviant/collapse witnesses 13 pts (literal values, direction and
                          collapse-target checks; includes the two
                          fully-collapsing A-rank cells)
  D7 extension anchors 77 pts (tail spots s in 41..48 x 8 cells,
                          strip spots m in 14..17, m=9 base spot)

MODES: default full battery (rc 0 iff overall_bad == 0).
  --tamper-engine      rc 2 (engine block sha mismatch)
  --tamper=cell      flip one declared cell value     -> rc 1, D1 bad
  --tamper=strip     flip one D2 expected value       -> rc 1, D2 bad
  --tamper=anchor13  flip one z13 transcription value -> rc 1, D3 bad
  --tamper=stair     flip one D4 expected value       -> rc 1, D4 bad
  --tamper=deviant   flip one D6 literal              -> rc 1, D6 bad
  --tamper=ext       flip one D7 expected value       -> rc 1, D7 bad
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
        'cell', 'strip', 'anchor13', 'stair', 'deviant', 'ext'), TAMPER
TAM = TAMPER[0] if TAMPER else None

# ---------------------------------------------------------------------------
# Declared z=14 floor-9 cell closed forms (K1319 claims). Domain: all Y
# tokens >= 9, s = sum(Y) in {0} U {9..} (Y blank iff s=0), arity arbitrary.
# ---------------------------------------------------------------------------
def F14(s):
    return 1 if s == 14 else v(s + 1, 14, 16)
def G14(s):
    if s == 12: return 0
    if s == 14: return 2
    return v(s + 2, 14, 17)
def E14(s):
    if s == 12: return 1
    return v(s + 3, 14, 18)
def D14(s):
    if s == 10: return 0
    if s == 12: return 2
    return v(s + 4, 14, 19)
def C14(s):
    if s == 10: return 1
    return v(s + 5, 14, 20)
def B14(s):
    if s == 10: return 2
    return v(s + 6, 14, 21)
def A14(s):
    return v(s + 7, 14, 22)
def A214(s):
    return v(s + 8, 14, 23)
CELLS = [(1, F14), (2, G14), (3, E14), (4, D14),
         (5, C14), (6, B14), (7, A14), (8, A214)]
CELL_NAMES = {1: 'F', 2: 'G', 3: 'E', 4: 'D',
              5: 'C', 6: 'B', 7: 'A', 8: 'A2'}

if TAM == 'cell':  # flip one declared deviant value (G14f9 s=12: 0 -> 1)
    def G14(s):
        return (1 if s == 12 else (2 if s == 14 else v(s + 2, 14, 17)))
    CELLS = [(1, F14), (2, G14), (3, E14), (4, D14),
             (5, C14), (6, B14), (7, A14), (8, A214)]

# ---------------------------------------------------------------------------
# Transcribed published z=13 lines (K1317 note section 1/2 statements;
# floor-8 domain for the 7 cells {0} U {8..}; rung 8 = T-Z13(8) theorem
# line, no deviants). Re-anchored against the engine by D3 (independent of
# the K1317 official verification state).
# ---------------------------------------------------------------------------
def F13f8t(s):
    return 2 if s >= 14 else (1 if s == 12 else v(s + 1, 13, 15))
def G13f8t(s):
    return 0 if s == 12 else v(s + 2, 13, 16)
def E13f8t(s):
    if s == 10: return 1
    if s == 12: return 2
    return v(s + 3, 13, 17)
def D13f8t(s):
    return 0 if s == 10 else v(s + 4, 13, 18)
def C13f8t(s):
    if s == 8: return 1
    if s == 10: return 2
    return v(s + 5, 13, 19)
def B13f8t(s):
    return 0 if s == 8 else v(s + 6, 13, 20)
def A13f8t(s):
    return 2 if s == 8 else v(s + 7, 13, 21)
def TZ13_8t(s):
    return v(s + 8, 13, 22)  # T-Z13(m=8) theorem line
LINES13 = [(1, F13f8t), (2, G13f8t), (3, E13f8t), (4, D13f8t),
           (5, C13f8t), (6, B13f8t), (7, A13f8t), (8, TZ13_8t)]

if TAM == 'anchor13':  # flip one transcription value
    def B13f8t(s):
        return 1 if s == 8 else v(s + 6, 13, 20)
    LINES13 = [(1, F13f8t), (2, G13f8t), (3, E13f8t), (4, D13f8t),
               (5, C13f8t), (6, B13f8t), (7, A13f8t), (8, TZ13_8t)]


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
declared = 2496
pts = 0; bad = 0
for j, fn in CELLS:
    R = j + 15
    for s in [0] + list(range(9, 41)):
        ys = [()] if s == 0 else parts(s, 9, 4)
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            hv = H(R, X, 14)
            pts += 1
            if hv != fn(s):
                bad += 1
    H.cache_clear()
total_bad += run_gate('D1_cells', declared, pts, bad)

# --- D2: T-Z14 strip sweep ---------------------------------------------------
declared = 791
pts = 0; bad = 0
if TAM == 'strip':
    flipped = set()
for m in range(9, 14):
    for S in range(m, m + 40):
        for X in parts(max(S - m, 0), m, 3):
            XX = tuple(sorted((m,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(m + 15, XX, 14)
            ev = v(S, 14, m + 15)
            pts += 1
            if TAM == 'strip' and (m, S, XX) not in flipped and len(flipped) == 0:
                flipped.add((m, S, XX)); ev = (ev + 1) % 3
            if hv != ev:
                bad += 1
    H.cache_clear()
total_bad += run_gate('D2_strip', declared, pts, bad)

# --- D3: z13 line transcriptions + T-Z13 C-hand anchors ---------------------
declared = 297
pts = 0; bad = 0
for j, fn in LINES13:
    for s in [0] + list(range(8, 41)):
        X = (j, s) if s > 0 else (j,)
        hv = H(j + 14, tuple(sorted(X, reverse=True)), 13)
        ev = fn(s)
        if ev is None:
            ev = -1  # transcription holes must never happen on the domain
            bad += 1
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
for m in range(9, 14):
    for i in range(1, 6):
        X = tuple(sorted((m, m + i), reverse=True))
        hv = H(m + 14, X, 13)
        ev = v(2 * m + i, 13, m + 14)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D3_z13_anchors', declared, pts, bad)

# --- D4: stair anchors (A-on-Y children of cell parents) ---------------------
declared = 256
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(9, 41):
        child = tuple(sorted((j, s - 1), reverse=True))
        hv = H(j + 14, child, 14)
        ev = v(s + j - 1, 14, j + 14)
        if TAM == 'stair' and j == 3 and s == 10:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D4_stair_anchors', declared, pts, bad)

# --- D5: self anchors (single-token v grid + empty positions) ---------------
grid = []
for x in range(1, 28):
    for z in range(0, 16):
        rs = [0, 1, 5, 14, 22, 23, 24, x + z - 1, x + z, x + z + 1]
        for R in rs:
            if R < 0 or R > 71:
                continue
            grid.append((x, z, R))
declared = len(grid) + 144
pts = 0; bad = 0
for (x, z, R) in grid:
    hv = H(R, (x,), z)
    ev = v(x, z, R)
    pts += 1
    if hv != ev:
        bad += 1
for R in range(0, 9):
    for z in range(0, 16):
        hv = H(R, (), z)
        pts += 1
        if hv != 0:
            bad += 1
total_bad += run_gate('D5_self_anchors', declared, pts, bad)

# --- D6: deviant / collapse witness literals --------------------------------
WITNESSES = [
    # (j, s, Y, declared_value, collapse_target, direction)
    (1, 14, (14,), 1, 0, 'UP'),      # F14f9 sole deviant (single-point tail)
    (1, 41, (41,), 0, 0, 'FLAT'),    # F14f9 tail collapse: NO constant tail
    (2, 12, (12,), 0, 2, 'DOWN'),    # G14f9 DOWN
    (2, 14, (14,), 2, 1, 'UP'),      # G14f9 UP
    (3, 12, (12,), 1, 0, 'UP'),      # E14f9 UP
    (4, 10, (10,), 0, 2, 'DOWN'),    # D14f9 DOWN
    (4, 12, (12,), 2, 1, 'UP'),      # D14f9 UP
    (5, 10, (10,), 1, 0, 'UP'),      # C14f9 UP
    (6, 10, (10,), 2, 1, 'UP'),      # B14f9 UP
    (7, 10, (10,), 0, 0, 'FLAT'),    # A14f9 FULL COLLAPSE at the absorbed source
    (8, 9, (9,), 1, 1, 'FLAT'),      # A214f9 base-cell collapse (s=9)
    (8, 10, (10,), 1, 1, 'FLAT'),    # A214f9 collapse at the bottom-source s=10
    (8, 41, (41,), 1, 1, 'FLAT'),    # A214f9 tail spot
]
declared = len(WITNESSES)
pts = 0; bad = 0
for (j, s, y, val, cval, direction) in WITNESSES:
    if TAM == 'deviant' and j == 6 and s == 10:
        val = (val + 1) % 3
    X = tuple(sorted((j,) + y, reverse=True))
    hv = H(j + 15, X, 14)
    col = v(s + j, 14, j + 15)
    pts += 1
    ok = (hv == val) and (col == cval)
    d = 'UP' if val > col else ('DOWN' if val < col else 'FLAT')
    if d != direction:
        ok = False
    if not ok:
        bad += 1
total_bad += run_gate('D6_deviant_witnesses', declared, pts, bad)

# --- D7: extension anchors (tail spots + strip spots + base spot) ----------
declared = 77
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(41, 49):
        X = tuple(sorted((j, s), reverse=True))
        hv = H(j + 15, X, 14)
        ev = fn(s)
        if TAM == 'ext' and j == 1 and s == 41:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
for m in range(14, 18):
    for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
        X = tuple(sorted(shp, reverse=True))
        hv = H(m + 15, X, 14)
        ev = v(sum(X), 14, m + 15)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
hv = H(24, (9, 9), 14)
ev = v(18, 14, 24)
pts += 1
if hv != ev or ev != 0:
    bad += 1
total_bad += run_gate('D7_extension_anchors', declared, pts, bad)

battery_declared = sum(g['declared_pts'] for g in gates.values())
battery_pts = sum(g['pts'] for g in gates.values())
res = {'machine': 'verify_k1319', 'engine_sha': sha, 'mode': TAM or 'full',
       'gates': gates, 'battery_declared_pts': battery_declared,
       'battery_pts': battery_pts, 'overall_bad': total_bad,
       'result': 'FAIL' if total_bad else 'PASS'}
print(json.dumps(res, sort_keys=True, separators=(',', ':')))
sys.exit(1 if total_bad else 0)
