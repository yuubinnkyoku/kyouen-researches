#!/usr/bin/env python3
"""verify_k1321: audit machine for the z=15 min>=9 (floor-9) strip
(claims and scopes in the single-owner declaration note
research/log/2026-11-25-strip-z15-min9-single-owner-note.md;
pre-declaration exploration kit already published at
research/experiments/strip-z15-min9-20261125/, commit 5ec6c35d).

Claims audited here (all UNIVERSAL claims are proven on paper in the note
section 2; this machine independently re-checks the engine agreement and
fail-closed battery totals; battery coverage is finite by construction and
does NOT by itself prove any universal claim):
  A.9 cell lemmas F15f9..A315f9 (floor 9 = every Y token >= 9; s domain
     {0} U {9..}; the domain EXTENDS the published floor-10 cells of K1320
     by one floor level -- the FIRST z-6 floor of the series, breaking the
     z-5 classical floor -- and the 9th rung A315f9 has small token 9 with
     Y tokens >= 9, i.e. CO-TOKEN-9 SHAPES INCLUDED: A315f9 IS the full
     m=9-row z=15 claim position H(25;{9}uY;15)):
     F15f9(s) = H(17;{1}uY;15) = { s==14: 1 ; s>=16: 2 ; else v(s+1,15,17) }
     G15f9(s) = H(18;{2}uY;15) = { s==14: 0 ; else v(s+2,15,18) }
     E15f9(s) = H(19;{3}uY;15) = { s==12: 1 ; s==14: 2 ; else v(s+3,15,19) }
     D15f9(s) = H(20;{4}uY;15) = { s==12: 0 ; else v(s+4,15,20) }
     C15f9(s) = H(21;{5}uY;15) = { s==10: 1 ; s==12: 2 ; else v(s+5,15,21) }
     B15f9(s) = H(22;{6}uY;15) = { s==10: 0 ; else v(s+6,15,22) }
     A15f9(s) = H(23;{7}uY;15) = { s==10: 2 ; else v(s+7,15,23) }
     A215f9(s) = H(24;{8}uY;15) = v(s+8,15,24)          (NO deviants)
     A315f9(s) = H(25;{9}uY;15) = v(s+9,15,25)          (NO deviants,
                full m=9-row claim position incl. co-token 9, all arity)
     (v = published K0832 single-token closed form.) Every closed form is
     IDENTICAL to its published floor-10 counterpart (K1320): the floor
     drop 10 -> 9 changes not a single value -- now PROVED universally by
     the note (floor-insensitivity corollary), observed before by the kit
     census. The F15f9 tail (constant 2 for ALL s >= 16, hole at s=15,
     DOWN single point at s=14) is the SIXTH F-family tail form, supplied
     by the below-band j=1 B-move child (16;Y;16) = v(s,16,16) (K1264
     stair / K1312 empty) whose floor-9-extended collapse (lemma BB-f9)
     is anchored by D8 over the floor-9 census domain.
  T-Z15min9: for every multiset X with min(X) = m >= 9:
     H(m+16; X; 15) = v(S,15,m+16), S = sum(X).
     Bottom m=9 is proven NEW here (co-token-9 A-children land on the
     A215f9 cell = the stair value, an equivalent replication); m >= 10 is
     inherited verbatim from the published T-Z15 (K1320).
     Corollaries: the z=15 slice is closed for ALL min >= 9 (every m>=9
     has z*(m) >= z*(9) = 17 > 15, K1268), and the m=9 row is determined
     for z in {0..15} (residual in-band z=16, frontier z=17 = z*(9)).
  The z=14 lines used by the C-hand recursion (published K1319 note
  cell lemmas F14f9..A214f9 and theorem T-Z14(9)) are re-anchored against
  the engine here (transcriptions checked independently; NOT taken on
  faith). The K1319 lines carry the floor-9 Y domain {0} U {9..} which is
  now the EXACT fit of the floor-9 ladder C-hand children (K1320 needed a
  subset argument); the j=9 C-hand child is the T-Z14(9) theorem line,
  which D3 anchors DIRECTLY for m in {9..14} (closing the D3 m=9 gap
  noticed by the K1320 second-lane verification log).

Battery (fail-closed: every gate must produce EXACTLY the declared point
count; any mismatch or failed point sets overall_bad > 0 and rc 1):
  D1 cells        2,808 pts (9 cells x 312 exhaustive floor-9 shapes,
                          s in {0} U {9..40}, arity 0..4)
  D2 strip          859 pts (m in 9..14 -- NEW m=9 claim positions 265
                          shapes, plus m in 10..14 = 594 re-measured,
                          engine vs v)
  D3 z14 anchors    294 pts (8 lines x 33 s-values in {0} U {9..40}
                          = 264 + 30 T-Z14 C-hand anchors m in 9..14
                          -- including m=9, the j=9 C-hand line)
  D4 stair anchors  288 pts (9 x 32 A-on-Y child stair positions,
                          s in 9..40)
  D5 self anchors 5,865 pts (single-token engine-vs-v grid, x in 1..28,
                          z in 0..16, 12 R-points each = 5,712;
                          + 153 empty-position anchors)
  D6 deviant/collapse witnesses 20 pts (the 17 K1320 witnesses over the
                          floor-9 domain + 3 NEW floor-entry witnesses:
                          F15f9 s=9 FLAT, A215f9 s=9 FLAT, A315f9
                          co-token-9 (Y=(9,)) FLAT)
  D7 extension anchors 86 pts (tail spots s in 41..48 x 9 cells,
                          strip spots m in 15..18, m=9 base spot
                          (25;(9,9);15)=0=v(18,15,25), m=10 base spot
                          (26;(10,10);15)=1=v(20,15,26))
  D8 belowband anchors 312 pts (the (ii') supply-source positions
                          H(16;Y;16) vs v(s,16,16) over the FULL floor-9
                          census domain: lemma BB-f9, the extended
                          stair/empty collapse that drives the F15f9 tail)

MODES: default full battery (rc 0 iff overall_bad == 0).
  --tamper-engine      rc 2 (engine block sha mismatch)
  --tamper=cell       flip one declared cell value     -> rc 1, D1 bad
  --tamper=strip      flip one D2 expected value       -> rc 1, D2 bad
  --tamper=anchor14   flip one z14 transcription value -> rc 1, D3 bad
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
        'cell', 'strip', 'anchor14', 'stair', 'deviant', 'ext', 'belowband'), TAMPER
TAM = TAMPER[0] if TAMPER else None

# ---------------------------------------------------------------------------
# Declared z=15 floor-9 cell closed forms (K1321 claims). Domain: all Y
# tokens >= 9, s = sum(Y) in {0} U {9..} (Y blank iff s=0), arity arbitrary.
# Every closed form is IDENTICAL to the published floor-10 table (K1320);
# the note proves floor-insensitivity 10 -> 9 universally (no supply source
# sits below 9: z=14 deviant positions {10,12,14} and tail region s>=16).
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
    if s == 10: return 0
    return v(s + 6, 15, 22)
def A15(s):
    if s == 10: return 2
    return v(s + 7, 15, 23)
def A215(s):
    return v(s + 8, 15, 24)
def A315(s):
    return v(s + 9, 15, 25)
CELLS = [(1, F15), (2, G15), (3, E15), (4, D15),
         (5, C15), (6, B15), (7, A15), (8, A215), (9, A315)]
CELL_NAMES = {1: 'F', 2: 'G', 3: 'E', 4: 'D',
              5: 'C', 6: 'B', 7: 'A', 8: 'A2', 9: 'A3'}

if TAM == 'cell':  # flip one declared deviant value (G15f10 s=14: 0 -> 1)
    def G15(s):
        return (1 if s == 14 else v(s + 2, 15, 18))
    CELLS = [(1, F15), (2, G15), (3, E15), (4, D15),
             (5, C15), (6, B15), (7, A15), (8, A215), (9, A315)]

# ---------------------------------------------------------------------------
# Transcribed published z=14 lines (K1319 note section 1 statements;
# floor-9 domain for the 8 cells {0} U {9..}; used by the z=15 C-hand
# recursion for j=1..8). Re-anchored against the engine by D3 (independent
# of the K1319 official verification state). The j=9 C-hand child is the
# T-Z14(9) theorem line (no deviants), anchored by the D3 C-hand sweep.
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
    return 2 if s == 10 else v(s + 6, 14, 21)
def A14(s):
    return v(s + 7, 14, 22)
def A214(s):
    return v(s + 8, 14, 23)
LINES14 = [(1, F14), (2, G14), (3, E14), (4, D14),
           (5, C14), (6, B14), (7, A14), (8, A214)]

if TAM == 'anchor14':  # flip one transcription value
    def B14(s):
        return 0 if s == 10 else v(s + 6, 14, 21)
    LINES14 = [(1, F14), (2, G14), (3, E14), (4, D14),
               (5, C14), (6, B14), (7, A14), (8, A214)]


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
declared = 2808
pts = 0; bad = 0
for j, fn in CELLS:
    R = j + 16
    for s in [0] + list(range(9, 41)):
        ys = [()] if s == 0 else parts(s, 9, 4)
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            hv = H(R, X, 15)
            pts += 1
            if hv != fn(s):
                bad += 1
    H.cache_clear()
total_bad += run_gate('D1_cells', declared, pts, bad)

# --- D2: T-Z15 strip sweep ---------------------------------------------------
declared = 859
pts = 0; bad = 0
if TAM == 'strip':
    flipped = set()
for m in range(9, 15):
    for S in range(m, m + 40):
        for X in parts(max(S - m, 0), m, 3):
            XX = tuple(sorted((m,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(m + 16, XX, 15)
            ev = v(S, 15, m + 16)
            pts += 1
            if TAM == 'strip' and (m, S, XX) not in flipped and len(flipped) == 0:
                flipped.add((m, S, XX)); ev = (ev + 1) % 3
            if hv != ev:
                bad += 1
    H.cache_clear()
total_bad += run_gate('D2_strip', declared, pts, bad)

# --- D3: z14 line transcriptions + T-Z14 C-hand anchors ---------------------
declared = 294
pts = 0; bad = 0
for j, fn in LINES14:
    for s in [0] + list(range(9, 41)):
        X = (j, s) if s > 0 else (j,)
        hv = H(j + 15, tuple(sorted(X, reverse=True)), 14)
        ev = fn(s)
        if ev is None:
            ev = -1  # transcription holes must never happen on the domain
            bad += 1
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
for m in range(9, 15):
    for i in range(1, 6):
        X = tuple(sorted((m, m + i), reverse=True))
        hv = H(m + 15, X, 14)
        ev = v(2 * m + i, 14, m + 15)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D3_z14_anchors', declared, pts, bad)

# --- D4: stair anchors (A-on-Y children of cell parents) ---------------------
declared = 288
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(9, 41):
        child = tuple(sorted((j, s - 1), reverse=True))
        hv = H(j + 15, child, 15)
        ev = v(s + j - 1, 15, j + 15)
        if TAM == 'stair' and j == 3 and s == 10:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D4_stair_anchors', declared, pts, bad)

# --- D5: self anchors (single-token v grid + empty positions) ---------------
grid = []
for x in range(1, 29):
    for z in range(0, 17):
        rs = [0, 1, 5, 14, 22, 23, 24, 25, 26, x + z - 1, x + z, x + z + 1]
        for R in rs:
            if R < 0 or R > 77:
                continue
            grid.append((x, z, R))
declared = len(grid) + 153
pts = 0; bad = 0
for (x, z, R) in grid:
    hv = H(R, (x,), z)
    ev = v(x, z, R)
    pts += 1
    if hv != ev:
        bad += 1
for R in range(0, 9):
    for z in range(0, 17):
        hv = H(R, (), z)
        pts += 1
        if hv != 0:
            bad += 1
total_bad += run_gate('D5_self_anchors', declared, pts, bad)

# --- D6: deviant / collapse witness literals --------------------------------
WITNESSES = [
    # (j, s, Y, declared_value, collapse_target, direction)
    (1, 14, (14,), 1, 2, 'DOWN'),    # F15f10 sole DOWN (single pre-tail point)
    (1, 15, (15,), 0, 0, 'FLAT'),    # F15f10 hole: tail absent exactly at s=15
    (1, 16, (16,), 2, 0, 'UP'),      # F15f10 tail start (constant-2, s>=16)
    (1, 17, (17,), 2, 0, 'UP'),      # F15f10 tail second point
    (2, 12, (12,), 0, 0, 'FLAT'),    # G15f10 collapse at the G14f9 supply s=12
    (2, 14, (14,), 0, 1, 'DOWN'),    # G15f10 DOWN (coalesced double supply)
    (2, 16, (16,), 1, 1, 'FLAT'),    # G-rung TAIL ABSORPTION witness (s>=16)
    (3, 12, (12,), 1, 2, 'DOWN'),    # E15f10 DOWN
    (3, 14, (14,), 2, 0, 'UP'),      # E15f10 UP
    (4, 12, (12,), 0, 1, 'DOWN'),    # D15f10 DOWN
    (5, 10, (10,), 1, 2, 'DOWN'),    # C15f10 DOWN
    (5, 12, (12,), 2, 0, 'UP'),      # C15f10 UP
    (6, 10, (10,), 0, 1, 'DOWN'),    # B15f10 DOWN
    (7, 10, (10,), 2, 0, 'UP'),      # A15f10 UP
    (8, 10, (10,), 1, 1, 'FLAT'),    # A215f10 collapse at the absorbed source
    (9, 10, (10,), 0, 0, 'FLAT'),    # A315f9 base-cell collapse (s=10)
    (9, 41, (41,), 0, 0, 'FLAT'),    # A315f9 tail spot
    (1, 9, (9,), 0, 0, 'FLAT'),      # F15f9 s=9 floor-entry collapse (NEW)
    (8, 9, (9,), 1, 1, 'FLAT'),      # A215f9 s=9 floor-entry collapse (NEW)
    (9, 9, (9,), 0, 0, 'FLAT'),      # A315f9 co-token-9 claim-position shape
                                     # H(25;(9,9);15) = v(18,15,25) (NEW)
]
declared = len(WITNESSES)
pts = 0; bad = 0
for (j, s, y, val, cval, direction) in WITNESSES:
    if TAM == 'deviant' and j == 6 and s == 10:
        val = (val + 1) % 3
    X = tuple(sorted((j,) + y, reverse=True))
    hv = H(j + 16, X, 15)
    col = v(s + j, 15, j + 16)
    pts += 1
    ok = (hv == val) and (col == cval)
    d = 'UP' if val > col else ('DOWN' if val < col else 'FLAT')
    if d != direction:
        ok = False
    if not ok:
        bad += 1
total_bad += run_gate('D6_deviant_witnesses', declared, pts, bad)

# --- D7: extension anchors (tail spots + strip spots + base spot) ----------
declared = 86
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(41, 49):
        X = tuple(sorted((j, s), reverse=True))
        hv = H(j + 16, X, 15)
        ev = fn(s)
        if TAM == 'ext' and j == 1 and s == 41:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
for m in range(15, 19):
    for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
        X = tuple(sorted(shp, reverse=True))
        hv = H(m + 16, X, 15)
        ev = v(sum(X), 15, m + 16)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
hv = H(25, (9, 9), 15)
ev = v(18, 15, 25)
pts += 1
if hv != ev or ev != 0:
    bad += 1
hv = H(26, (10, 10), 15)
ev = v(20, 15, 26)
pts += 1
if hv != ev or ev != 1:
    bad += 1
total_bad += run_gate('D7_extension_anchors', declared, pts, bad)

# --- D8: belowband (ii') supply-source anchors -------------------------------
# H(16; Y; 16) = v(s, 16, 16) for every floor-9 multiset Y (K1264 stair at
# R=16 <= 16+min(Y); empty at s=0 by K1312). This is the below-band j=1
# B-move child that supplies the F15f9 constant-2 tail; the floor-9 domain
# extension (lemma BB-f9) admits min(Y)=9 and single-piece shapes.
declared = 312
pts = 0; bad = 0
for s in [0] + list(range(9, 41)):
    ys = [()] if s == 0 else parts(s, 9, 4)
    for y in ys:
        hv = H(16, y, 16)
        ev = v(s, 16, 16)
        if TAM == 'belowband' and pts == 0:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D8_belowband_anchors', declared, pts, bad)

battery_declared = sum(g['declared_pts'] for g in gates.values())
battery_pts = sum(g['pts'] for g in gates.values())
res = {'machine': 'verify_k1321', 'engine_sha': sha, 'mode': TAM or 'full',
       'gates': gates, 'battery_declared_pts': battery_declared,
       'battery_pts': battery_pts, 'overall_bad': total_bad,
       'result': 'FAIL' if total_bad else 'PASS'}
print(json.dumps(res, sort_keys=True, separators=(',', ':')))
sys.exit(1 if total_bad else 0)
