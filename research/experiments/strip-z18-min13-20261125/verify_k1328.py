#!/usr/bin/env python3
"""verify_k1328: audit machine for the z=18 min>=13 (floor-13) strip
(claims and scopes in the single-owner declaration note
research/log/2026-11-25-strip-z18-min13-single-owner-note.md, commit
71c66058 + name-repair b94835e0; pre-declaration exploration kit already
published at research/experiments/strip-z18-min13-20261125/, commit
f152a6f5).

Structural copy of the published verify_k1325.py machine (z=17 min>=12
slice, commit 5a3c17f4) with the disclosed z 17 -> 18 textual adaptation:
rung count 11 -> 12, floor 12 -> 13, R budget j+18 -> j+19, the z=17
line transcriptions become the anchor set, D5 z-grid extends to z=19 and
forwarders/counts are re-declared as in this note section 4.

Claims audited here (all UNIVERSAL claims are proven on paper in the note
section 2; this machine independently re-checks the engine agreement and
fail-closed battery totals; battery coverage is finite by construction and
does NOT by itself prove any universal claim):
  A.12 cell lemmas F18f13..A618f13 (floor 13 = every Y token >= 13; s domain
     {0} U {13..}; the 12th rung A618f13 has small token 12 -- the FOURTH
     consecutive in-band base child of the strip series (min=12, z*(12)=22
     > 18) -- and its Y tokens stay >= 13):
     F18f13(s) = H(20;{1}uY;18) = { s==18: 1 ; else v(s+1,18,20) }
          (NINTH tail form: SINGLE POINT s=18 UP 1v0, NO hole, NO persistent
          tail -- single@even-z holds for the 4th consecutive data point;
          supplied by the below-band j=1 B-move child (19;Y;19)=v(s,19,19)
          absorption identity v(s,19,19)=v(s,18,19) which holds on
          {0} U {12..17} and breaks 0v2 at s=18 then uniformly 2v1 at
          s>=19 -- the 1-change supplies the single deviant and the
          uniform break leaves no tail)
     G18f13(s) = H(21;{2}uY;18) = { s==16: 0 ; s==18: 2 ; else v(s+2,18,21) }
     E18f13(s) = H(22;{3}uY;18) = { s==16: 1 ; else v(s+3,18,22) }
     D18f13(s) = H(23;{4}uY;18) = { s==14: 0 ; s==16: 2 ; else v(s+4,18,23) }
     C18f13(s) = H(24;{5}uY;18) = { s==14: 1 ; else v(s+5,18,24) }
     B18f13(s) = H(25;{6}uY;18) = { s==14: 2 ; else v(s+6,18,25) }
     A18f13(s) = H(26;{7}uY;18) = v(s+7,18,26)                     (NONE)
     A218f13(s) = H(27;{8}uY;18) = v(s+8,18,27)                    (NONE)
     A318f13(s) = H(28;{9}uY;18) = v(s+9,18,28)                    (NONE)
     A418f13(s) = H(29;{10}uY;18) = v(s+10,18,29)                  (NONE)
     A518f13(s) = H(30;{11}uY;18) = v(s+11,18,30)                  (NONE)
     A618f13(s) = H(31;{12}uY;18) = v(s+12,18,31)                  (NONE;
          the FOURTH consecutive in-band base child z*(12)=22>18, longest
          six-rung full-collapse run of the series; the (iii) C-hand child
          (30;{12}uY;17) is the published T-Z17 m=12-row claim position,
          deviant-free by the published theorem)
     (v = published K0832 single-token closed form.)
  T-Z18: for every multiset X with min(X) = m >= 13:
     H(m+19; X; 18) = v(S,18,m+19), S = sum(X). Base m=13 is trivial
     absorption through the fully collapsing A618f13 (the a=13 child);
     m >= 14 is the option-set-identity induction (a=m child = row m-1
     claim position, a>m children = K1264 stair, C-hand child = published
     T-Z17 line).
  The z=17 lines used by the T-Z18/C-hand recursion (published K1325
  declaration note section 1 cell lemmas F17f12..A517f12 and theorem
  T-Z17) are re-anchored against the engine here (transcriptions checked
  independently; NOT taken on faith). NOTE: the K1325 lines for j=1..11
  carry the floor-12 Y domain {0} U {12..}; the T-Z18 C-hand positions use
  Y tokens >= 12 (subset), and the D3 anchor sweeps use the full K1325
  floor-12 domain (Y=(s,) with s >= 12) which is exactly the published
  lemma domain.

Battery (fail-closed: every gate must produce EXACTLY the declared point
count; any mismatch or failed point sets overall_bad > 0 and rc 1):
  D1 cells        1,596 pts (12 cells x 133 exhaustive floor-13 shapes,
                          s in {0} U {13..43}, arity 0..4)
  D2 strip          286 pts (m in 13..17, S in m..m+39, Y parts >= m,
                          arity(Y) <= 3, engine vs v; identical sweep to
                          the frozen census kit section (c), cumulative
                          84/152/207/251/286)
  D3 z17 anchors    382 pts (11 lines x 32 s-values in {0} U {12..41}
                          = 352 + 30 T-Z17 C-hand anchors m in 12..17)
  D4 stair anchors  372 pts (12 x 31 A-on-Y child stair positions,
                          s in 13..43)
  D5 self anchors 12,780 pts (single-token engine-vs-v grid, x in 1..30,
                          z in 0..19 (z=19 needed by the below-band
                          identity pair), 21 R-points each = 12,600;
                          + 180 empty-position anchors)
  D6 deviant/collapse witnesses 22 pts (literal values, direction and
                          collapse-target checks; includes the F18f13
                          ninth-form single point s=18, the s=17/s=19
                          flats ruling out hole/tail, the far-tail
                          absence spot, the G18 DOWN/2-point
                          reconstruction, the mex-absorption FLAT
                          witnesses G17f12-style, and the fully
                          collapsing A-rank cells' spots incl. the
                          in-band base child A618f13 and its far tail)
  D7 extension anchors 109 pts (tail spots s in 44..51 x 12 cells = 96
                          -- ALL FLAT, the ninth form has NO persistent
                          tail --, strip spots m in 18..21 = 12, m=13
                          base spot = 0)
  D8 belowband anchors 133 pts (the below-band (ii') supply-source
                          position H(19;Y;19) vs v(s,19,19) over the full
                          floor-13 census domain: the stair/empty collapse
                          whose absorption identity v(s,19,19)=v(s,18,19)
                          holds on {0} U {12..17}, breaks 0v2 at s=18 and
                          2v1 uniformly at s>=19, supplying the F18f13
                          single point and leaving no tail)

MODES: default full battery (rc 0 iff overall_bad == 0).
  --tamper-engine      rc 2 (engine block sha mismatch)
  --tamper=cell       flip one declared cell value     -> rc 1, D1 bad
  --tamper=strip      flip one D2 expected value       -> rc 1, D2 bad
  --tamper=anchor17   flip one z17 transcription value -> rc 1, D3 bad
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
        'cell', 'strip', 'anchor17', 'stair', 'deviant', 'ext', 'belowband'), TAMPER
TAM = TAMPER[0] if TAMPER else None

# ---------------------------------------------------------------------------
# Declared z=18 floor-13 cell closed forms (K1328 claims). Domain: all Y
# tokens >= 13, s = sum(Y) in {0} U {13..} (Y blank iff s=0), arity arbitrary.
# ---------------------------------------------------------------------------
def F18(s):
    if s == 18:
        return 1
    return v(s + 1, 18, 20)
def G18(s):
    if s == 16:
        return 0
    if s == 18:
        return 2
    return v(s + 2, 18, 21)
def E18(s):
    if s == 16:
        return 1
    return v(s + 3, 18, 22)
def D18(s):
    if s == 14:
        return 0
    if s == 16:
        return 2
    return v(s + 4, 18, 23)
def C18(s):
    if s == 14:
        return 1
    return v(s + 5, 18, 24)
def B18(s):
    if s == 14:
        return 2
    return v(s + 6, 18, 25)
def A18(s):
    return v(s + 7, 18, 26)
def A218(s):
    return v(s + 8, 18, 27)
def A318(s):
    return v(s + 9, 18, 28)
def A418(s):
    return v(s + 10, 18, 29)
def A518(s):
    return v(s + 11, 18, 30)
def A618(s):
    return v(s + 12, 18, 31)
CELLS = [(1, F18), (2, G18), (3, E18), (4, D18),
         (5, C18), (6, B18), (7, A18), (8, A218),
         (9, A318), (10, A418), (11, A518), (12, A618)]
CELL_NAMES = {1: 'F', 2: 'G', 3: 'E', 4: 'D',
              5: 'C', 6: 'B', 7: 'A', 8: 'A2', 9: 'A3', 10: 'A4',
              11: 'A5', 12: 'A6'}

if TAM == 'cell':  # flip one declared deviant value (G18f13 s=16: 0 -> 1)
    def G18(s):
        return (1 if s == 16 else
                (2 if s == 18 else v(s + 2, 18, 21)))
    CELLS = [(1, F18), (2, G18), (3, E18), (4, D18),
             (5, C18), (6, B18), (7, A18), (8, A218),
             (9, A318), (10, A418), (11, A518), (12, A618)]

# ---------------------------------------------------------------------------
# Transcribed published z=17 lines (K1325 declaration note section 1
# statements; floor-12 domain {0} U {12..} for the 11 cells; used by the
# z=18 C-hand recursion for j=1..11; the j=12 C-hand child is the T-Z17
# theorem line (min=12), anchored by the D3 C-hand sweep). Re-anchored
# against the engine by D3 (independent of the K1325 official verification
# state).
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
LINES17 = [(1, F17), (2, G17), (3, E17), (4, D17),
           (5, C17), (6, B17), (7, A17), (8, A217), (9, A317),
           (10, A417), (11, A517)]

if TAM == 'anchor17':  # flip one transcription value
    def B17(s):
        return 1 if s == 12 else v(s + 6, 17, 24)
    LINES17 = [(1, F17), (2, G17), (3, E17), (4, D17),
               (5, C17), (6, B17), (7, A17), (8, A217), (9, A317),
               (10, A417), (11, A517)]


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
declared = 1596
pts = 0; bad = 0
for j, fn in CELLS:
    R = j + 19
    for s in [0] + list(range(13, 44)):
        ys = [()] if s == 0 else parts(s, 13, 4)
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            hv = H(R, X, 18)
            pts += 1
            if hv != fn(s):
                bad += 1
    H.cache_clear()
total_bad += run_gate('D1_cells', declared, pts, bad)

# --- D2: T-Z18 strip sweep ---------------------------------------------------
declared = 286
pts = 0; bad = 0
if TAM == 'strip':
    flipped = set()
for m in range(13, 18):
    for S in range(m, m + 40):
        for X in parts(max(S - m, 0), m, 3):
            XX = tuple(sorted((m,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(m + 19, XX, 18)
            ev = v(S, 18, m + 19)
            pts += 1
            if TAM == 'strip' and (m, S, XX) not in flipped and len(flipped) == 0:
                flipped.add((m, S, XX)); ev = (ev + 1) % 3
            if hv != ev:
                bad += 1
    H.cache_clear()
total_bad += run_gate('D2_strip', declared, pts, bad)

# --- D3: z17 line transcriptions + T-Z17 C-hand anchors ---------------------
declared = 382
pts = 0; bad = 0
for j, fn in LINES17:
    for s in [0] + list(range(12, 43)):
        X = (j, s) if s > 0 else (j,)
        hv = H(j + 18, tuple(sorted(X, reverse=True)), 17)
        ev = fn(s)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
# T-Z17 C-hand anchors: the (iii) child of the T-Z18 claim position at
# min=m is (m+18; X; 17) = the published T-Z17 m-row claim position.
# m=12 anchors the A618f13 cell C-hand; m in 13..17 anchor the strip rows.
for m in range(12, 18):
    for i in range(1, 6):
        X = tuple(sorted((m, m + i), reverse=True))
        hv = H(m + 18, X, 17)
        ev = v(2 * m + i, 17, m + 18)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D3_z17_anchors', declared, pts, bad)

# --- D4: stair anchors (A-on-Y children of cell parents) ---------------------
declared = 372
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(13, 44):
        child = tuple(sorted((j, s - 1), reverse=True))
        hv = H(j + 18, child, 18)
        ev = v(s + j - 1, 18, j + 18)
        if TAM == 'stair' and j == 3 and s == 13:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D4_stair_anchors', declared, pts, bad)

# --- D5: self anchors (single-token v grid + empty positions) ---------------
grid = []
for x in range(1, 31):
    for z in range(0, 20):
        rs = [0, 1, 5, 14, 17, 18, 19, 20, 21, 22, 23, 24,
              25, 26, 27, 28, 29, 30, x + z - 1, x + z, x + z + 1]
        for R in rs:
            if R < 0 or R > 81:
                continue
            grid.append((x, z, R))
declared = len(grid) + 180
pts = 0; bad = 0
for (x, z, R) in grid:
    hv = H(R, (x,), z)
    ev = v(x, z, R)
    pts += 1
    if hv != ev:
        bad += 1
H.cache_clear()
for R in range(0, 9):
    for z in range(0, 20):
        hv = H(R, (), z)
        pts += 1
        if hv != 0:
            bad += 1
total_bad += run_gate('D5_self_anchors', declared, pts, bad)

# --- D6: deviant / collapse witness literals --------------------------------
WITNESSES = [
    # (j, s, declared_value, collapse_target, direction)
    (1, 16, 1, 1, 'FLAT'),    # F18f13 collapse at the F17f12 s=16 DOWN supply
    (1, 17, 0, 0, 'FLAT'),    # F18f13 s=17 flat -- the ninth form has NO hole
    (1, 18, 1, 0, 'UP'),      # F18f13 NINTH-form SINGLE POINT s=18 UP 1v0
    (1, 19, 0, 0, 'FLAT'),    # F18f13 s=19 flat -- NO persistent tail
    (1, 41, 0, 0, 'FLAT'),    # F18f13 far tail spot absent (eighth form gone)
    (2, 14, 0, 0, 'FLAT'),    # G18f13 collapse at the G17f12 s=14 supply
    (2, 16, 0, 2, 'DOWN'),    # G18f13 DOWN (published G17f12 s=16 supply)
    (2, 18, 2, 1, 'UP'),      # G18f13 UP 2v1 (F18f13 s=18 single point supply)
    (3, 14, 1, 1, 'FLAT'),    # E18f13 collapse at the E17f12 s=14 supply
    (3, 16, 1, 0, 'UP'),      # E18f13 UP (G17f12 s=16 supply)
    (3, 18, 0, 0, 'FLAT'),    # E18f13 s=18 flat (mex absorption of 2)
    (4, 14, 0, 2, 'DOWN'),    # D18f13 DOWN (published D17f12 s=14 supply)
    (4, 16, 2, 1, 'UP'),      # D18f13 UP (E17f12 s=16 supply)
    (5, 14, 1, 0, 'UP'),      # C18f13 UP (C17f12 s=14 supply)
    (5, 16, 0, 0, 'FLAT'),    # C18f13 s=16 flat
    (6, 14, 2, 1, 'UP'),      # B18f13 UP (B17f12 s=14 supply)
    (6, 16, 1, 1, 'FLAT'),    # B18f13 s=16 flat (mex absorption)
    (7, 14, 0, 0, 'FLAT'),    # A18f13 full-collapse spot (6-run collapse start)
    (8, 14, 1, 1, 'FLAT'),    # A218f13 absorbs the A18 neighborhood
    (12, 14, 1, 1, 'FLAT'),   # A618f13 base-child cell spot (in-band base)
    (12, 18, 1, 1, 'FLAT'),   # A618f13 at the base supply position s=18
    (12, 41, 1, 1, 'FLAT'),   # A618f13 far tail spot
]
declared = len(WITNESSES)
pts = 0; bad = 0
for (j, s, val, cval, direction) in WITNESSES:
    if TAM == 'deviant' and j == 1 and s == 18:
        val = (val + 1) % 3
    X = (j, s)
    hv = H(j + 19, X, 18)
    col = v(s + j, 18, j + 19)
    pts += 1
    ok = (hv == val) and (col == cval)
    d = 'UP' if val > col else ('DOWN' if val < col else 'FLAT')
    if d != direction:
        ok = False
    if not ok:
        bad += 1
total_bad += run_gate('D6_deviant_witnesses', declared, pts, bad)

# --- D7: extension anchors (tail spots + strip spots + base spot) ----------
declared = 109
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(44, 52):
        X = (j, s)
        hv = H(j + 19, X, 18)
        ev = fn(s)
        if TAM == 'ext' and j == 1 and s == 44:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
for m in range(18, 22):
    for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
        X = tuple(sorted(shp, reverse=True))
        hv = H(m + 19, X, 18)
        ev = v(sum(X), 18, m + 19)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
hv = H(32, (13, 13), 18)
ev = v(26, 18, 32)
pts += 1
if hv != ev or ev != 0:
    bad += 1
total_bad += run_gate('D7_extension_anchors', declared, pts, bad)

# --- D8: belowband (ii') supply-source anchors -------------------------------
# H(19; Y; 19) = v(s, 19, 19) for every floor-13 multiset Y (K1264 stair at
# R=19 <= 19+min(Y); empty at s=0 by K1312). This is the below-band j=1
# B-move child whose absorption identity v(s,19,19)=v(s,18,19) holds on
# {0} U {12..17} and breaks 0v2 at s=18, then uniformly 2v1 at s>=19
# (supplying the F18f13 single point and leaving no tail).
declared = 133
pts = 0; bad = 0
for s in [0] + list(range(13, 44)):
    ys = [()] if s == 0 else parts(s, 13, 4)
    for y in ys:
        hv = H(19, y, 19)
        ev = v(s, 19, 19)
        if TAM == 'belowband' and pts == 0:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D8_belowband_anchors', declared, pts, bad)

battery_declared = sum(g['declared_pts'] for g in gates.values())
battery_pts = sum(g['pts'] for g in gates.values())
res = {'machine': 'verify_k1328', 'engine_sha': sha, 'mode': TAM or 'full',
       'gates': gates, 'battery_declared_pts': battery_declared,
       'battery_pts': battery_pts, 'overall_bad': total_bad,
       'result': 'FAIL' if total_bad else 'PASS'}
print(json.dumps(res, sort_keys=True, separators=(',', ':')))
sys.exit(1 if total_bad else 0)
