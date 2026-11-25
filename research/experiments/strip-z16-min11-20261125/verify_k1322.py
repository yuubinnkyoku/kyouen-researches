#!/usr/bin/env python3
"""verify_k1322: audit machine for the z=16 min>=11 (floor-11) strip
(claims and scopes in the single-owner declaration note
research/log/2026-11-25-strip-z16-min11-single-owner-note.md;
pre-declaration exploration kit already published at
research/experiments/strip-z16-min11-20261125/, commit e0ca8d75).

Claims audited here (all UNIVERSAL claims are proven on paper in the note
section 2; this machine independently re-checks the engine agreement and
fail-closed battery totals; battery coverage is finite by construction and
does NOT by itself prove any universal claim):
  A.10 cell lemmas F16f11..A416f11 (floor 11 = every Y token >= 11; s domain
     {0} U {11..}; the 10th rung A416f11 has small token 10 -- the SECOND
     consecutive in-band base child of the strip series (min=10, z*(10)=18
     > 16) -- and its Y tokens stay >= 11):
     F16f11(s) = H(18;{1}uY;16) = { s==16: 1 ; else v(s+1,16,18) }      (1 UP)
     G16f11(s) = H(19;{2}uY;16) = { s==14: 0 ; s==16: 2 ; else v(s+2,16,19) }
     E16f11(s) = H(20;{3}uY;16) = { s==14: 1 ; else v(s+3,16,20) }      (1 UP)
     D16f11(s) = H(21;{4}uY;16) = { s==12: 0 ; s==14: 2 ; else v(s+4,16,21) }
     C16f11(s) = H(22;{5}uY;16) = { s==12: 1 ; else v(s+5,16,22) }      (1 UP)
     B16f11(s) = H(23;{6}uY;16) = { s==12: 2 ; else v(s+6,16,23) }      (1 UP)
     A16f11(s) = H(24;{7}uY;16) = v(s+7,16,24)                         (NONE)
     A216f11(s) = H(25;{8}uY;16) = v(s+8,16,25)                        (NONE)
     A316f11(s) = H(26;{9}uY;16) = v(s+9,16,26)                        (NONE)
     A416f11(s) = H(27;{10}uY;16) = v(s+10,16,27)                      (NONE)
     (v = published K0832 single-token closed form.) The F16f11 form is the
     F-family SEVENTH tail typology: an isolated UP point at s=16 (supplied
     by the below-band j=1 B-move child (17;Y;17)=v(s,17,17) absorption
     break at s=16) and NO permanent tail: the whole region s >= 17
     collapses uniformly (options constants {1,2,3}, mex 0 = W), the
     z=15 constant-2 F-tail (s>=16) being fully absorbed at the mex level.
  T-Z16: for every multiset X with min(X) = m >= 11:
     H(m+17; X; 16) = v(S,16,m+17), S = sum(X). Base m=11 is trivial
     absorption through the fully collapsing A416f11 (the a=11 child);
     m >= 12 is the option-set-identity induction (a=m child = row m-1
     claim position, a>m children = K1264 stair, C-hand child = published
     T-Z15 line).
  The z=15 lines used by the T-Z16/C-hand recursion (published K1320 note
  section 1 cell lemmas F15f10..A315f10 and theorem T-Z15) are re-anchored
  against the engine here (transcriptions checked independently; NOT taken
  on faith). NOTE: the K1320 lines for j=1..9 carry the floor-10 Y domain
  {0} U {10..}; the T-Z16 C-hand positions use Y tokens >= 11 which is a
  subset, and the D3 anchor sweeps use the full K1320 floor-10 domain
  (Y=(s,) with s >= 10) which is exactly the published lemma domain.

Battery (fail-closed: every gate must produce EXACTLY the declared point
count; any mismatch or failed point sets overall_bad > 0 and rc 1):
  D1 cells        1,830 pts (10 cells x 183 exhaustive floor-11 shapes,
                          s in {0} U {11..41}, arity 0..4)
  D2 strip          456 pts (m in 11..15, S in m..m+39, Y parts >= m,
                          arity(Y) <= 3, engine vs v; identical sweep to
                          the frozen census kit section (c))
  D3 z15 anchors    322 pts (9 lines x 33 s-values in {0} U {10..41}
                          = 297 + 25 T-Z15 C-hand anchors m in 11..15)
  D4 stair anchors  310 pts (10 x 31 A-on-Y child stair positions)
  D5 self anchors 10,080 pts (single-token engine-vs-v grid, x in 1..29,
                          z in 0..17, 19 R-points each = 9,918;
                          + 162 empty-position anchors)
  D6 deviant/collapse witnesses 19 pts (literal values, direction and
                          collapse-target checks; includes the F16f11
                          absorption-break UP, the s>=17 uniform-tail
                          absorption witness, the FLAT absorptions at the
                          in-run supply points of E16/D16/C16/A16 and the
                          four fully collapsing A-rank cells' spots)
  D7 extension anchors 93 pts (tail spots s in 42..49 x 10 cells,
                          strip spots m in 16..19, m=11 base spot)
  D8 belowband anchors 183 pts (the (ii') supply source position
                          H(17;Y;17) vs v(s,17,17) over the full floor-11
                          census domain: the stair/empty collapse whose
                          absorption break at s=16 supplies the F16f11 UP)

MODES: default full battery (rc 0 iff overall_bad == 0).
  --tamper-engine      rc 2 (engine block sha mismatch)
  --tamper=cell       flip one declared cell value     -> rc 1, D1 bad
  --tamper=strip      flip one D2 expected value       -> rc 1, D2 bad
  --tamper=anchor15   flip one z15 transcription value -> rc 1, D3 bad
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
        'cell', 'strip', 'anchor15', 'stair', 'deviant', 'ext', 'belowband'), TAMPER
TAM = TAMPER[0] if TAMPER else None

# ---------------------------------------------------------------------------
# Declared z=16 floor-11 cell closed forms (K1322 claims). Domain: all Y
# tokens >= 11, s = sum(Y) in {0} U {11..} (Y blank iff s=0), arity arbitrary.
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
CELLS = [(1, F16), (2, G16), (3, E16), (4, D16),
         (5, C16), (6, B16), (7, A16), (8, A216),
         (9, A316), (10, A416)]
CELL_NAMES = {1: 'F', 2: 'G', 3: 'E', 4: 'D',
              5: 'C', 6: 'B', 7: 'A', 8: 'A2', 9: 'A3', 10: 'A4'}

if TAM == 'cell':  # flip one declared deviant value (G16f11 s=14: 0 -> 1)
    def G16(s):
        return (1 if s == 14 else
                (2 if s == 16 else v(s + 2, 16, 19)))
    CELLS = [(1, F16), (2, G16), (3, E16), (4, D16),
             (5, C16), (6, B16), (7, A16), (8, A216),
             (9, A316), (10, A416)]

# ---------------------------------------------------------------------------
# Transcribed published z=15 lines (K1320 note section 1 statements;
# floor-10 domain {0} U {10..} for the 9 cells; used by the z=16 C-hand
# recursion for j=1..9; the j=10 C-hand child is the T-Z15 theorem line
# (min=10), anchored by the D3 C-hand sweep). Re-anchored against the
# engine by D3 (independent of the K1320 official verification state).
# ---------------------------------------------------------------------------
def F15(s):
    if s >= 16:
        return 2
    if s == 14:
        return 1
    return v(s + 1, 15, 17)
def G15(s):
    if s == 14:
        return 0
    return v(s + 2, 15, 18)
def E15(s):
    if s == 12: return 1
    if s == 14: return 2
    return v(s + 3, 15, 19)
def D15(s):
    if s == 12: return 0
    return v(s + 4, 15, 20)
def C15(s):
    if s == 10: return 1
    if s == 12: return 2
    return v(s + 5, 15, 21)
def B15(s):
    return 0 if s == 10 else v(s + 6, 15, 22)
def A15(s):
    return 2 if s == 10 else v(s + 7, 15, 23)
def A215(s):
    return v(s + 8, 15, 24)
def A315(s):
    return v(s + 9, 15, 25)
LINES15 = [(1, F15), (2, G15), (3, E15), (4, D15),
           (5, C15), (6, B15), (7, A15), (8, A215), (9, A315)]

if TAM == 'anchor15':  # flip one transcription value
    def B15(s):
        return 1 if s == 10 else v(s + 6, 15, 22)
    LINES15 = [(1, F15), (2, G15), (3, E15), (4, D15),
               (5, C15), (6, B15), (7, A15), (8, A215), (9, A315)]


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
declared = 1830
pts = 0; bad = 0
for j, fn in CELLS:
    R = j + 17
    for s in [0] + list(range(11, 42)):
        ys = [()] if s == 0 else parts(s, 11, 4)
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            hv = H(R, X, 16)
            pts += 1
            if hv != fn(s):
                bad += 1
    H.cache_clear()
total_bad += run_gate('D1_cells', declared, pts, bad)

# --- D2: T-Z16 strip sweep ---------------------------------------------------
declared = 456
pts = 0; bad = 0
if TAM == 'strip':
    flipped = set()
for m in range(11, 16):
    for S in range(m, m + 40):
        for X in parts(max(S - m, 0), m, 3):
            XX = tuple(sorted((m,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(m + 17, XX, 16)
            ev = v(S, 16, m + 17)
            pts += 1
            if TAM == 'strip' and (m, S, XX) not in flipped and len(flipped) == 0:
                flipped.add((m, S, XX)); ev = (ev + 1) % 3
            if hv != ev:
                bad += 1
    H.cache_clear()
total_bad += run_gate('D2_strip', declared, pts, bad)

# --- D3: z15 line transcriptions + T-Z15 C-hand anchors ---------------------
declared = 322
pts = 0; bad = 0
for j, fn in LINES15:
    for s in [0] + list(range(10, 42)):
        X = (j, s) if s > 0 else (j,)
        hv = H(j + 16, tuple(sorted(X, reverse=True)), 15)
        ev = fn(s)
        if ev is None:
            ev = -1  # transcription holes must never happen on the domain
            bad += 1
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
for m in range(11, 16):
    for i in range(1, 6):
        X = tuple(sorted((m, m + i), reverse=True))
        hv = H(m + 16, X, 15)
        ev = v(2 * m + i, 15, m + 16)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D3_z15_anchors', declared, pts, bad)

# --- D4: stair anchors (A-on-Y children of cell parents) ---------------------
declared = 310
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(11, 42):
        child = tuple(sorted((j, s - 1), reverse=True))
        hv = H(j + 16, child, 16)
        ev = v(s + j - 1, 16, j + 16)
        if TAM == 'stair' and j == 3 and s == 11:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D4_stair_anchors', declared, pts, bad)

# --- D5: self anchors (single-token v grid + empty positions) ---------------
grid = []
for x in range(1, 30):
    for z in range(0, 18):
        rs = [0, 1, 5, 14, 17, 18, 19, 20, 21, 22, 23, 24,
              25, 26, 27, 28, x + z - 1, x + z, x + z + 1]
        for R in rs:
            if R < 0 or R > 81:
                continue
            grid.append((x, z, R))
declared = len(grid) + 162
pts = 0; bad = 0
for (x, z, R) in grid:
    hv = H(R, (x,), z)
    ev = v(x, z, R)
    pts += 1
    if hv != ev:
        bad += 1
for R in range(0, 9):
    for z in range(0, 18):
        hv = H(R, (), z)
        pts += 1
        if hv != 0:
            bad += 1
total_bad += run_gate('D5_self_anchors', declared, pts, bad)

# --- D6: deviant / collapse witness literals --------------------------------
WITNESSES = [
    # (j, s, Y, declared_value, collapse_target, direction)
    (1, 14, (14,), 1, 1, 'FLAT'),    # F16f11 collapse at the F15f10 s=14 supply
    (1, 16, (16,), 1, 0, 'UP'),      # F16f11 sole UP (absorption break s=16)
    (1, 17, (17,), 0, 0, 'FLAT'),    # F16f11 uniform-tail absorption start
    (1, 41, (41,), 0, 0, 'FLAT'),    # F16f11 far tail spot
    (2, 14, (14,), 0, 2, 'DOWN'),    # G16f11 DOWN (G15f10 s=14 supply)
    (2, 16, (16,), 2, 1, 'UP'),      # G16f11 UP (F16f11-deviant propagation)
    (3, 12, (12,), 1, 1, 'FLAT'),    # E16f11 collapse at the E15f10 s=12 supply
    (3, 14, (14,), 1, 0, 'UP'),      # E16f11 UP (double supply s=14)
    (3, 16, (16,), 0, 0, 'FLAT'),    # E16f11 collapse at the G16f11-deviant s=16
    (4, 12, (12,), 0, 2, 'DOWN'),    # D16f11 DOWN (D15f10 s=12 supply)
    (4, 14, (14,), 2, 1, 'UP'),      # D16f11 UP (E16f11-deviant propagation)
    (5, 12, (12,), 1, 0, 'UP'),      # C16f11 UP (C15f10 s=12 + D16f11-dev supplies)
    (5, 14, (14,), 0, 0, 'FLAT'),    # C16f11 collapse at the D16f11-deviant s=14
    (6, 12, (12,), 2, 1, 'UP'),      # B16f11 UP (C16f11-deviant propagation)
    (7, 12, (12,), 0, 0, 'FLAT'),    # A16f11 collapse at the B16f11-deviant s=12
    (8, 12, (12,), 1, 1, 'FLAT'),    # A216f11 full-collapse spot
    (9, 12, (12,), 0, 0, 'FLAT'),    # A316f11 full-collapse spot
    (10, 11, (11,), 1, 1, 'FLAT'),   # A416f11 base-child cell spot (in-band base)
    (10, 41, (41,), 1, 1, 'FLAT'),   # A416f11 far tail spot
]
declared = len(WITNESSES)
pts = 0; bad = 0
for (j, s, y, val, cval, direction) in WITNESSES:
    if TAM == 'deviant' and j == 6 and s == 12:
        val = (val + 1) % 3
    X = tuple(sorted((j,) + y, reverse=True))
    hv = H(j + 17, X, 16)
    col = v(s + j, 16, j + 17)
    pts += 1
    ok = (hv == val) and (col == cval)
    d = 'UP' if val > col else ('DOWN' if val < col else 'FLAT')
    if d != direction:
        ok = False
    if not ok:
        bad += 1
total_bad += run_gate('D6_deviant_witnesses', declared, pts, bad)

# --- D7: extension anchors (tail spots + strip spots + base spot) ----------
declared = 93
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(42, 50):
        X = tuple(sorted((j, s), reverse=True))
        hv = H(j + 17, X, 16)
        ev = fn(s)
        if TAM == 'ext' and j == 1 and s == 42:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
for m in range(16, 20):
    for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
        X = tuple(sorted(shp, reverse=True))
        hv = H(m + 17, X, 16)
        ev = v(sum(X), 16, m + 17)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
hv = H(28, (11, 11), 16)
ev = v(22, 16, 28)
pts += 1
if hv != ev or ev != 0:
    bad += 1
total_bad += run_gate('D7_extension_anchors', declared, pts, bad)

# --- D8: belowband (ii') supply-source anchors -------------------------------
# H(17; Y; 17) = v(s, 17, 17) for every floor-11 multiset Y (K1264 stair at
# R=17 <= 17+min(Y); empty at s=0 by K1312). This is the below-band j=1
# B-move child whose absorption identity v(s,17,17)=v(s,16,17) holds on
# {0} U {11..15} and breaks at s=16 (supplying the F16f11 UP).
declared = 183
pts = 0; bad = 0
for s in [0] + list(range(11, 42)):
    ys = [()] if s == 0 else parts(s, 11, 4)
    for y in ys:
        hv = H(17, y, 17)
        ev = v(s, 17, 17)
        if TAM == 'belowband' and pts == 0:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D8_belowband_anchors', declared, pts, bad)

battery_declared = sum(g['declared_pts'] for g in gates.values())
battery_pts = sum(g['pts'] for g in gates.values())
res = {'machine': 'verify_k1322', 'engine_sha': sha, 'mode': TAM or 'full',
       'gates': gates, 'battery_declared_pts': battery_declared,
       'battery_pts': battery_pts, 'overall_bad': total_bad,
       'result': 'FAIL' if total_bad else 'PASS'}
print(json.dumps(res, sort_keys=True, separators=(',', ':')))
sys.exit(1 if total_bad else 0)
