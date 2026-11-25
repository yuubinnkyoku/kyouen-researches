#!/usr/bin/env python3
"""verify_k1317: audit machine for the z=13 min>=8 (floor-8) strip
(claims and scopes in the single-owner declaration note
research/log/2026-11-25-strip-z13-min8-single-owner-note.md).

Claims audited here (all UNIVERSAL claims are proven on paper in the note
section 2; this machine independently re-checks the engine agreement and
fail-closed battery totals; battery coverage is finite by construction and
does NOT by itself prove any universal claim):
  A.7 cell lemmas F13f8..A13f8 (floor 8 = every Y token >= 8):
     F13f8(s) = H(15;{1}uY;13) = { s>=14: 2 ; s==12: 1 ; else v(s+1,13,15) }
     G13f8(s) = H(16;{2}uY;13) = { s==12: 0 ; else  v(s+2,13,16) }
     E13f8(s) = H(17;{3}uY;13) = { s==10: 1 ; s==12: 2 ; else v(s+3,13,17) }
     D13f8(s) = H(18;{4}uY;13) = { s==10: 0 ; else v(s+4,13,18) }
     C13f8(s) = H(19;{5}uY;13) = { s==8: 1 ; s==10: 2 ; else v(s+5,13,19) }
     B13f8(s) = H(20;{6}uY;13) = { s==8: 0 ; else v(s+6,13,20) }
     A13f8(s) = H(21;{7}uY;13) = { s==8: 2 ; else v(s+7,13,21) }
     (s in {0} U {8..}; v = published K0832 single-token closed form.)
  T-Z13: for every multiset X with min(X) = m >= 8:
     H(m+14; X; 13) = v(S,13,m+14), S = sum(X).
  The z=12 lines used by the T-Z13/C-hand recursion (published K1316 note
  tables F12..B12 and T-Z12) are re-anchored against the engine here
  (transcriptions checked independently; they are NOT taken on faith).

Battery (fail-closed: every gate must produce EXACTLY the declared point
count; any mismatch or failed point sets overall_bad > 0 and rc 1):
  D1 cells        3,220 pts (7 cells x 460 exhaustive floor-8 shapes,
                          s in {0} U {8..40}, arity 0..4)
  D2 strip        1,069 pts (m in 8..12, S in m..m+39, Y parts >= m,
                          arity(Y) <= 3, engine vs v)
  D3 z12 anchors    263 pts (7 cell lines x 34 s-values in {0} U {8..40}
                          = 238 + 25 T-Z12 C-hand anchors m in 8..12)
  D4 stair anchors  231 pts (7 x 33 A-on-Y child stair positions)
  D5 self anchors     ? pts (single-token engine-vs-v grid; declared in
                          note section 4) + 126 empty-position anchors
  D6 deviant witnesses 13 pts (literal values AND non-equality with the
                          collapse target)
  D7 extension anchors 69 pts (tail spots s in 41..48, strip m in 13..16,
                          m=8 base absorption spot)

MODES: default full battery (rc 0 iff overall_bad == 0).
  --tamper-engine      rc 2 (engine block sha mismatch)
  --tamper=cell      flip one declared cell value     -> rc 1, D1 bad
  --tamper=strip     flip one D2 expected value       -> rc 1, D2 bad
  --tamper=anchor12  flip one z12 transcription value -> rc 1, D3 bad
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
        'cell', 'strip', 'anchor12', 'stair', 'deviant', 'ext'), TAMPER
TAM = TAMPER[0] if TAMPER else None

# ---------------------------------------------------------------------------
# Declared z=13 floor-8 cell closed forms (K1317 claims).
# ---------------------------------------------------------------------------
def F13(s):
    return 2 if s >= 14 else (1 if s == 12 else v(s + 1, 13, 15))
def G13(s):
    return 0 if s == 12 else v(s + 2, 13, 16)
def E13(s):
    if s == 10: return 1
    if s == 12: return 2
    return v(s + 3, 13, 17)
def D13(s):
    return 0 if s == 10 else v(s + 4, 13, 18)
def C13(s):
    if s == 8: return 1
    if s == 10: return 2
    return v(s + 5, 13, 19)
def B13(s):
    return 0 if s == 8 else v(s + 6, 13, 20)
def A13(s):
    return 2 if s == 8 else v(s + 7, 13, 21)
CELLS = [(1, F13), (2, G13), (3, E13), (4, D13), (5, C13), (6, B13), (7, A13)]
CELL_NAMES = {1: 'F', 2: 'G', 3: 'E', 4: 'D', 5: 'C', 6: 'B', 7: 'A'}

if TAM == 'cell':  # flip the declared value at one deviant position
    _orig = E13(12)
    def E13(s, _orig=_orig):
        return (0 if s == 12 else (1 if s == 10 else v(s + 3, 13, 17)))
    CELLS = [(1, F13), (2, G13), (3, E13), (4, D13), (5, C13), (6, B13), (7, A13)]

# ---------------------------------------------------------------------------
# Transcribed published z=12 line tables (K1316 note section 1/2 statements;
# floors: F/E/G >= 3, D12 >= 5, C12 >= 6, B12 >= 7, T-Z12 m >= 7).
# Re-anchored against the engine by D3 (independent of the K1316 official
# verification state).
# ---------------------------------------------------------------------------
def F12t(s):
    return 1 if s == 0 else (0 if s >= 13 else ((s + 1) % 2 if 3 <= s <= 12 else None))
def G12t(s):
    tbl = {0: 0, 3: 1, 4: 0, 5: 1, 6: 0, 7: 1, 8: 0, 9: 1, 10: 0, 11: 1, 12: 2}
    return tbl.get(s, 1 if s >= 13 else None)
def E12t(s):
    tbl = {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1, 9: 0, 10: 1, 11: 0}
    return tbl.get(s, 0 if s >= 12 else None)
def D12t(s):
    if s == 8: return 0
    if s == 10: return 2
    return v(s + 4, 12, 17)
def C12t(s):
    if s == 0: return 1
    if s == 8: return 1
    return v(s + 5, 12, 18)
def B12t(s):
    if s == 8: return 2
    return v(s + 6, 12, 19)
def A12t(s):
    return v(s + 7, 12, 20)  # T-Z12(m=7) theorem line
LINES12 = [(1, F12t), (2, G12t), (3, E12t), (4, D12t), (5, C12t), (6, B12t), (7, A12t)]

if TAM == 'anchor12':  # flip one transcription value
    _origB = B12t(8)
    def B12t(s, _origB=_origB):
        return 0 if s == 8 else v(s + 6, 12, 19)
    LINES12 = [(1, F12t), (2, G12t), (3, E12t), (4, D12t), (5, C12t), (6, B12t), (7, A12t)]


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
def gate(gname, declared_pts):
    bad = 0
    pts = 0
    return [gname, declared_pts, bad, pts]

def run_gate(gname, declared_pts, pts, bad):
    if pts != declared_pts and not TAM:
        bad += abs(pts - declared_pts)  # fail-closed count mismatch
    gates[gname] = {'declared_pts': declared_pts, 'pts': pts, 'bad': bad}
    return bad

total_bad = 0

# --- D1: exhaustive cell sweeps ---------------------------------------------
declared = 3220
pts = 0; bad = 0
for j, fn in CELLS:
    R = j + 14
    for s in [0] + list(range(8, 41)):
        ys = [()] if s == 0 else parts(s, 8, 4)
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            hv = H(R, X, 13)
            pts += 1
            if hv != fn(s):
                bad += 1
    H.cache_clear()
total_bad += run_gate('D1_cells', declared, pts, bad)

# --- D2: T-Z13 strip sweep ---------------------------------------------------
declared = 1069
pts = 0; bad = 0
if TAM == 'strip':
    flipped = set()
for m in range(8, 13):
    for S in range(m, m + 40):
        for X in parts(max(S - m, 0), m, 3):
            XX = tuple(sorted((m,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(m + 14, XX, 13)
            ev = v(S, 13, m + 14)
            pts += 1
            if TAM == 'strip' and (m, S, XX) not in flipped and len(flipped) == 0:
                flipped.add((m, S, XX)); ev = (ev + 1) % 3
            if hv != ev:
                bad += 1
    H.cache_clear()
total_bad += run_gate('D2_strip', declared, pts, bad)

# --- D3: z12 line transcriptions + T-Z12 C-hand anchors ---------------------
declared = 263
pts = 0; bad = 0
for j, fn in LINES12:
    for s in [0] + list(range(8, 41)):
        X = (j, s) if s > 0 else (j,)
        hv = H(j + 13, tuple(sorted(X, reverse=True)), 12)
        ev = fn(s)
        if ev is None:
            ev = -1  # transcription holes must never happen on the domain
            bad += 1
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
for m in range(8, 13):
    for i in range(1, 6):
        X = tuple(sorted((m, m + i), reverse=True))
        hv = H(m + 13, X, 12)
        ev = v(2 * m + i, 12, m + 13)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D3_z12_anchors', declared, pts, bad)

# --- D4: stair anchors (A-on-Y children of cell parents) ---------------------
declared = 231
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(8, 41):
        child = tuple(sorted((j, s - 1), reverse=True))
        hv = H(j + 13, child, 13)
        ev = v(s + j - 1, 13, j + 13)
        if TAM == 'stair' and j == 3 and s == 10:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D4_stair_anchors', declared, pts, bad)

# --- D5: self anchors (single-token v grid + empty positions) ---------------
grid = []
for x in range(1, 27):
    for z in range(0, 14):
        rs = [0, 1, 5, 13, 20, 21, 22, x + z - 1, x + z, x + z + 1]
        for R in rs:
            if R < 0 or R > 63:
                continue
            grid.append((x, z, R))
declared = len(grid) + 126
pts = 0; bad = 0
for (x, z, R) in grid:
    hv = H(R, (x,), z)
    ev = v(x, z, R)
    pts += 1
    if hv != ev:
        bad += 1
for R in range(0, 9):
    for z in range(0, 14):
        hv = H(R, (), z)
        pts += 1
        if hv != 0:
            bad += 1
total_bad += run_gate('D5_self_anchors', declared, pts, bad)

# --- D6: deviant witness literals -------------------------------------------
WITNESSES = [
    # (j, s, Y, declared_value, collapse_target, direction)
    (1, 12, (12,), 1, 2, 'DOWN'),
    (1, 14, (14,), 2, 0, 'UP'),
    (1, 16, (8, 8), 2, 0, 'UP'),
    (1, 20, (20,), 2, 0, 'UP'),
    (1, 40, (40,), 2, 0, 'UP'),
    (2, 12, (12,), 0, 1, 'DOWN'),
    (3, 10, (10,), 1, 2, 'DOWN'),
    (3, 12, (12,), 2, 0, 'UP'),
    (4, 10, (10,), 0, 1, 'DOWN'),
    (5, 8, (8,), 1, 2, 'DOWN'),
    (5, 10, (10,), 2, 0, 'UP'),
    (6, 8, (8,), 0, 1, 'DOWN'),
    (7, 8, (8,), 2, 0, 'UP'),
]
declared = len(WITNESSES)
pts = 0; bad = 0
for (j, s, y, val, cval, direction) in WITNESSES:
    if TAM == 'deviant' and j == 6 and s == 8:
        val = (val + 1) % 3
    X = tuple(sorted((j,) + y, reverse=True))
    hv = H(j + 14, X, 13)
    col = v(s + j, 13, j + 14)
    pts += 1
    ok = (hv == val) and (val != cval) and (col == cval)
    d = 'UP' if val > col else ('DOWN' if val < col else 'FLAT')
    if d != direction:
        ok = False
    if not ok:
        bad += 1
total_bad += run_gate('D6_deviant_witnesses', declared, pts, bad)

# --- D7: extension anchors (tail spots + strip spots + absorption) ----------
declared = 69
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(41, 49):
        X = tuple(sorted((j, s), reverse=True))
        hv = H(j + 14, X, 13)
        ev = fn(s)
        if TAM == 'ext' and j == 1 and s == 41:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
for m in range(13, 17):
    for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
        X = tuple(sorted(shp, reverse=True))
        hv = H(m + 14, X, 13)
        ev = v(sum(X), 13, m + 14)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
hv = H(22, (8, 8), 13)
ev = v(16, 13, 22)
pts += 1
if hv != ev or ev != 1:
    bad += 1
total_bad += run_gate('D7_extension_anchors', declared, pts, bad)

battery_declared = sum(g['declared_pts'] for g in gates.values())
battery_pts = sum(g['pts'] for g in gates.values())
res = {'machine': 'verify_k1317', 'engine_sha': sha, 'mode': TAM or 'full',
       'gates': gates, 'battery_declared_pts': battery_declared,
       'battery_pts': battery_pts, 'overall_bad': total_bad,
       'result': 'PASS' if total_bad == 0 else 'FAIL'}
print(json.dumps(res, sort_keys=True, separators=(',', ':')))
sys.exit(0 if total_bad == 0 else 1)
