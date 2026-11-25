#!/usr/bin/env python3
"""verify_k1330: audit machine for the z=19 min>=14 (floor-14) strip
(claims and scopes in the single-owner declaration note
research/log/2026-11-25-strip-z19-min14-single-owner-note.md, commit
e07d8f3d; pre-declaration exploration kit already published at
research/experiments/strip-z19-min14-20261125/, commits 6a6832ce ->
e07d8f3d).

Structural copy of the published verify_k1328.py machine (z=18 min>=13
slice, commit 8b157c9e) with the disclosed z 18 -> 19 textual adaptation:
rung count 12 -> 13, floor 13 -> 14, cell budget j+19 -> j+20, the z=18
line transcriptions become the anchor set, D5 z-grid extends to z=20 and
forwarders/counts are re-declared as in the declaration note section 4.

Claims audited here (all UNIVERSAL claims are proven on paper in the note
section 2; this machine independently re-checks the engine agreement and
fail-closed battery totals; battery coverage is finite by construction and
does NOT by itself prove any universal claim):
  A.13 cell lemmas F19f14..A719f14 (floor 14 = every Y token >= 14; s domain
     {0} U {14..}; the 13th rung A719f14 has small token 13 -- the FIFTH
     consecutive in-band base child of the strip series (min=13, z*(13)=25
     > 19) -- and its Y tokens stay >= 14):
     F19f14(s) = H(21;{1}uY;19) = { s==18: 1 ; s>=20: 2 ; else v(s+1,19,21) }
          (TENTH tail form: HOLE+TAIL -- {18 DOWN 1v2, 19 HOLE (=collapse 0),
          s>=20 persistent UP 2v0 tail}; hole+tail@(odd z) holds for the 5th
          consecutive data point; supplied by the below-band j=1 B-move child
          (20;Y;20)=v(s,20,20) absorption identity v(s,20,20)=v(s,19,20) which
          holds on {0} U {12..19} and breaks uniformly 0v1 for all s>=20 --
          the break injects the mex minimum 0 at s=20 supplying the persistent
          tail, the identity final hold point s=19 is the HOLE)
     G19f14(s) = H(22;{2}uY;19) = { s==18: 0 ; else v(s+2,19,22) }
     E19f14(s) = H(23;{3}uY;19) = { s==16: 1 ; s==18: 2 ; else v(s+3,19,23) }
     D19f14(s) = H(24;{4}uY;19) = { s==16: 0 ; else v(s+4,19,24) }
     C19f14(s) = H(25;{5}uY;19) = { s==14: 1 ; s==16: 2 ; else v(s+5,19,25) }
     B19f14(s) = H(26;{6}uY;19) = { s==14: 0 ; else v(s+6,19,26) }
     A19f14(s) = H(27;{7}uY;19) = { s==14: 2 ; else v(s+7,19,27) }
          (A-rank deviant REBORN: first since A17f12, at s=14=z-5, odd-z
          A-break observation 2/2)
     A219f14(s) = H(28;{8}uY;19) = v(s+8,19,28)                    (NONE)
     A319f14(s) = H(29;{9}uY;19) = v(s+9,19,29)                    (NONE)
     A419f14(s) = H(30;{10}uY;19) = v(s+10,19,30)                  (NONE)
     A519f14(s) = H(31;{11}uY;19) = v(s+11,19,31)                  (NONE)
     A619f14(s) = H(32;{12}uY;19) = v(s+12,19,32)                  (NONE)
     A719f14(s) = H(33;{13}uY;19) = v(s+13,19,33)                  (NONE;
          the FIFTH consecutive in-band base child z*(13)=25>19; a 2-hex
          {C,B,A}/{E,D,C}/{F,G,E} triplet ladder at positions 14/16/18 with
          the value multiset {DOWN:1, DOWN:0, UP:2} = the z=17 base-position
          triplet; the (iii) C-hand child (32;{13}uY;18) is the published
          T-Z18 m=13-row claim position, deviant-free by the published theorem)
     (v = published K0832 single-token closed form.)
  T-Z19: for every multiset X with min(X) = m >= 14:
     H(m+20; X; 19) = v(S,19,m+20), S = sum(X). Base m=14 is trivial
     absorption through the fully collapsing A719f14 (the a=14 child);
     m >= 15 is the option-set-identity induction (a=m child = row m-1
     claim position, a>m children = K1264 stair, C-hand child = published
     T-Z18 line rows m >= 13).
  The z=18 lines used by the T-Z19/C-hand recursion (published K1328
  declaration note section 1 cell lemmas F18f13..A618f13 and theorem
  T-Z18) are re-anchored against the engine here (transcriptions checked
  independently; NOT taken on faith). NOTE: the K1328 lines for j=1..12
  carry the floor-13 Y domain {0} U {13..}; the T-Z19 C-hand positions use
  Y tokens >= 14 (subset), and the D3 anchor sweeps use the full K1328
  floor-13 domain (Y=(s,) with s >= 13) which is exactly the published
  lemma domain.

Battery (fail-closed: every gate must produce EXACTLY the declared point
count; any mismatch or failed point sets overall_bad > 0 and rc 1):
  D1 cells        1,521 pts (13 cells x 117 exhaustive floor-14 shapes,
                          s in {0} U {14..44}, arity 0..4)
  D2 strip          230 pts (m in 14..18, S in m..m+39, Y parts >= m,
                          arity(Y) <= 3, engine vs v; identical sweep to
                          the frozen census kit section (c), cumulative
                          68/55/44/35/28)
  D3 z18 anchors    438 pts (12 lines x 34 s-values in {0} U {13..45}
                          = 408 + 30 T-Z18 C-hand anchors m in 13..18)
  D4 stair anchors  403 pts (13 x 31 A-on-Y child stair positions,
                          s in 14..44)
  D5 self anchors 13,419 pts (single-token engine-vs-v grid, x in 1..30,
                          z in 0..20 (z=20 needed by the below-band
                          identity pair), 21 R-points each = 13,230;
                          + 189 empty-position anchors)
  D6 deviant/collapse witnesses 22 pts (literal values, direction and
                          collapse-target checks; includes the F19f14
                          tenth-form DOWN single point s=18, the s=19
                          HOLE flat, the s=20/s=52 persistent-tail points,
                          the G19f14 single DOWN and the G18f13 s=16
                          mex-absorption FLAT, the E/D/C/B DOWN+UP
                          reconstructions, the A19f14 A-rank rebirth
                          witness and the fully collapsing in-band base
                          child A719f14 spots)
  D7 extension anchors 117 pts (tail spots s in 45..52 x 13 cells = 104
                          -- the F19f14 persistent tail holds at all 8
                          window-external F spots, the other 96 rows
                          FLAT --, strip spots m in 19..22 = 12, m=14
                          base spot = 1)
  D8 belowband anchors 117 pts (the below-band (ii') supply-source
                          position H(20;Y;20) vs v(s,20,20) over the full
                          floor-14 census domain: the stair/empty collapse
                          whose absorption identity v(s,20,20)=v(s,19,20)
                          holds on {0} U {12..19} and breaks uniformly
                          0v1 for all s>=20, supplying the F19f14
                          persistent tail)

MODES: default full battery (rc 0 iff overall_bad == 0).
  --tamper-engine      rc 2 (engine block sha mismatch)
  --tamper=cell       flip one declared cell value     -> rc 1, D1 bad
  --tamper=strip      flip one D2 expected value       -> rc 1, D2 bad
  --tamper=anchor18   flip one z18 transcription value -> rc 1, D3 bad
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
        'cell', 'strip', 'anchor18', 'stair', 'deviant', 'ext', 'belowband'), TAMPER
TAM = TAMPER[0] if TAMPER else None

# ---------------------------------------------------------------------------
# Declared z=19 floor-14 cell closed forms (K1330 claims). Domain: all Y
# tokens >= 14, s = sum(Y) in {0} U {14..} (Y blank iff s=0), arity arbitrary.
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
CELLS = [(1, F19), (2, G19), (3, E19), (4, D19),
         (5, C19), (6, B19), (7, A19), (8, A219),
         (9, A319), (10, A419), (11, A519), (12, A619),
         (13, A719)]
CELL_NAMES = {1: 'F', 2: 'G', 3: 'E', 4: 'D',
              5: 'C', 6: 'B', 7: 'A', 8: 'A2', 9: 'A3', 10: 'A4',
              11: 'A5', 12: 'A6', 13: 'A7'}

if TAM == 'cell':  # flip one declared deviant value (G19f14 s=18: 0 -> 1)
    def G19(s):
        return (1 if s == 18 else
                v(s + 2, 19, 22))
    CELLS = [(1, F19), (2, G19), (3, E19), (4, D19),
             (5, C19), (6, B19), (7, A19), (8, A219),
             (9, A319), (10, A419), (11, A519), (12, A619),
             (13, A719)]

# ---------------------------------------------------------------------------
# Transcribed published z=18 lines (K1328 declaration note section 1
# statements; floor-13 domain {0} U {13..} for the 12 cells; used by the
# z=19 C-hand recursion for j=1..12; the j=13 C-hand child is the T-Z18
# theorem line (min=13), anchored by the D3 C-hand sweep). Re-anchored
# against the engine by D3 (independent of the K1328 official verification
# state).
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
LINES18 = [(1, F18), (2, G18), (3, E18), (4, D18),
           (5, C18), (6, B18), (7, A18), (8, A218), (9, A318),
           (10, A418), (11, A518), (12, A618)]

if TAM == 'anchor18':  # flip one transcription value (B18f13 s=14: 2 -> 1)
    def B18(s):
        return 1 if s == 14 else v(s + 6, 18, 25)
    LINES18 = [(1, F18), (2, G18), (3, E18), (4, D18),
               (5, C18), (6, B18), (7, A18), (8, A218), (9, A318),
               (10, A418), (11, A518), (12, A618)]


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
declared = 1521
pts = 0; bad = 0
for j, fn in CELLS:
    R = j + 20
    for s in [0] + list(range(14, 45)):
        ys = [()] if s == 0 else parts(s, 14, 4)
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            hv = H(R, X, 19)
            pts += 1
            if hv != fn(s):
                bad += 1
    H.cache_clear()
total_bad += run_gate('D1_cells', declared, pts, bad)

# --- D2: T-Z19 strip sweep ---------------------------------------------------
declared = 230
pts = 0; bad = 0
if TAM == 'strip':
    flipped = set()
for m in range(14, 19):
    for S in range(m, m + 40):
        for X in parts(max(S - m, 0), m, 3):
            XX = tuple(sorted((m,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(m + 20, XX, 19)
            ev = v(S, 19, m + 20)
            pts += 1
            if TAM == 'strip' and (m, S, XX) not in flipped and len(flipped) == 0:
                flipped.add((m, S, XX)); ev = (ev + 1) % 3
            if hv != ev:
                bad += 1
    H.cache_clear()
total_bad += run_gate('D2_strip', declared, pts, bad)

# --- D3: z18 line transcriptions + T-Z18 C-hand anchors ---------------------
declared = 438
pts = 0; bad = 0
for j, fn in LINES18:
    for s in [0] + list(range(13, 46)):
        X = (j, s) if s > 0 else (j,)
        hv = H(j + 19, tuple(sorted(X, reverse=True)), 18)
        ev = fn(s)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
# T-Z18 C-hand anchors: the (iii) child of the T-Z19 claim position at
# min=m is (m+19; X; 18) = the published T-Z18 m-row claim position.
# m=13 anchors the A719f14 cell C-hand; m in 14..18 anchor the strip rows.
for m in range(13, 19):
    for i in range(1, 6):
        X = tuple(sorted((m, m + i), reverse=True))
        hv = H(m + 19, X, 18)
        ev = v(2 * m + i, 18, m + 19)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D3_z18_anchors', declared, pts, bad)

# --- D4: stair anchors (A-on-Y children of cell parents) ---------------------
declared = 403
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(14, 45):
        child = tuple(sorted((j, s - 1), reverse=True))
        hv = H(j + 19, child, 19)
        ev = v(s + j - 1, 19, j + 19)
        if TAM == 'stair' and j == 3 and s == 14:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D4_stair_anchors', declared, pts, bad)

# --- D5: self anchors (single-token v grid + empty positions) ---------------
grid = []
for x in range(1, 31):
    for z in range(0, 21):
        rs = [0, 1, 5, 14, 17, 18, 19, 20, 21, 22, 23, 24,
              25, 26, 27, 28, 29, 30, x + z - 1, x + z, x + z + 1]
        for R in rs:
            if R < 0 or R > 81:
                continue
            grid.append((x, z, R))
declared = len(grid) + 189
pts = 0; bad = 0
for (x, z, R) in grid:
    hv = H(R, (x,), z)
    ev = v(x, z, R)
    pts += 1
    if hv != ev:
        bad += 1
H.cache_clear()
for R in range(0, 9):
    for z in range(0, 21):
        hv = H(R, (), z)
        pts += 1
        if hv != 0:
            bad += 1
total_bad += run_gate('D5_self_anchors', declared, pts, bad)

# --- D6: deviant / collapse witness literals --------------------------------
WITNESSES = [
    # (j, s, declared_value, collapse_target, direction)
    (1, 16, 1, 1, 'FLAT'),    # F19f14 pre-deviant flat
    (1, 17, 0, 0, 'FLAT'),    # F19f14 flat at the s=17 boundary
    (1, 18, 1, 2, 'DOWN'),    # F19f14 TENTH-form DOWN SINGLE POINT s=18 1v2
    (1, 19, 0, 0, 'FLAT'),    # F19f14 s=19 HOLE (equals the collapse 0)
    (1, 20, 2, 0, 'UP'),      # F19f14 persistent-tail FIRST point s=20
    (1, 52, 2, 0, 'UP'),      # F19f14 far persistent tail (window-external)
    (2, 16, 0, 0, 'FLAT'),    # G19f14 collapses the G18f13 s=16 DOWN supply
    (2, 18, 0, 1, 'DOWN'),    # G19f14 DOWN (F19f14 s=18 DOWN supply mirror)
    (2, 20, 1, 1, 'FLAT'),    # G19f14 tail-region flat (mex absorption)
    (3, 16, 1, 2, 'DOWN'),    # E19f14 DOWN (E18f13 s=16 UP supply)
    (3, 18, 2, 0, 'UP'),      # E19f14 UP (G19f14 s=18 DOWN supply mirror)
    (4, 16, 0, 1, 'DOWN'),    # D19f14 DOWN (E19f14 s=16 DOWN supply mirror)
    (4, 18, 1, 1, 'FLAT'),    # D19f14 s=18 flat (E19f14 UP supply 2 absorbed)
    (5, 14, 1, 2, 'DOWN'),    # C19f14 DOWN (C18f13 s=14 UP supply)
    (5, 16, 2, 0, 'UP'),      # C19f14 UP (D19f14 s=16 DOWN supply mirror)
    (6, 14, 0, 1, 'DOWN'),    # B19f14 DOWN (C19f14 s=14 DOWN supply mirror)
    (7, 14, 2, 0, 'UP'),      # A19f14 UP -- A RANK REBORN (first since z=17)
    (7, 16, 0, 0, 'FLAT'),    # A19f14 flat
    (8, 14, 1, 1, 'FLAT'),    # A219f14 absorbs the A19f14 UP supply above mex
    (13, 14, 0, 0, 'FLAT'),   # A719f14 base-child cell spot (in-band base)
    (13, 18, 0, 0, 'FLAT'),   # A719f14 at the supply position s=18
    (13, 52, 0, 0, 'FLAT'),   # A719f14 far tail spot
]
declared = len(WITNESSES)
pts = 0; bad = 0
for (j, s, val, cval, direction) in WITNESSES:
    if TAM == 'deviant' and j == 1 and s == 18:
        val = (val + 1) % 3
    X = (j, s)
    hv = H(j + 20, X, 19)
    col = v(s + j, 19, j + 20)
    pts += 1
    ok = (hv == val) and (col == cval)
    d = 'UP' if val > col else ('DOWN' if val < col else 'FLAT')
    if d != direction:
        ok = False
    if not ok:
        bad += 1
total_bad += run_gate('D6_deviant_witnesses', declared, pts, bad)

# --- D7: extension anchors (tail spots + strip spots + base spot) ----------
declared = 117
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(45, 53):
        X = (j, s)
        hv = H(j + 20, X, 19)
        ev = fn(s)
        if TAM == 'ext' and j == 1 and s == 45:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
for m in range(19, 23):
    for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
        X = tuple(sorted(shp, reverse=True))
        hv = H(m + 20, X, 19)
        ev = v(sum(X), 19, m + 20)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
hv = H(34, (14, 14), 19)
ev = v(28, 19, 34)
pts += 1
if hv != ev or ev != 1:
    bad += 1
total_bad += run_gate('D7_extension_anchors', declared, pts, bad)

# --- D8: belowband (ii') supply-source anchors -------------------------------
# H(20; Y; 20) = v(s, 20, 20) for every floor-14 multiset Y (empty at s=0
# by K1312-stair-type collapse; the identity v(s,20,20)=v(s,19,20) below).
# This is the below-band j=1 B-move child whose absorption identity
# v(s,20,20)=v(s,19,20) holds on {0} U {12..19} and breaks uniformly 0v1
# for all s>=20 (supplying the F19f14 persistent tail; the identity final
# hold point s=19 is the F19f14 HOLE).
declared = 117
pts = 0; bad = 0
for s in [0] + list(range(14, 45)):
    ys = [()] if s == 0 else parts(s, 14, 4)
    for y in ys:
        hv = H(20, y, 20)
        ev = v(s, 20, 20)
        if TAM == 'belowband' and pts == 0:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D8_belowband_anchors', declared, pts, bad)

battery_declared = sum(g['declared_pts'] for g in gates.values())
battery_pts = sum(g['pts'] for g in gates.values())
res = {'machine': 'verify_k1330', 'engine_sha': sha, 'mode': TAM or 'full',
       'gates': gates, 'battery_declared_pts': battery_declared,
       'battery_pts': battery_pts, 'overall_bad': total_bad,
       'result': 'FAIL' if total_bad else 'PASS'}
print(json.dumps(res, sort_keys=True, separators=(',', ':')))
sys.exit(1 if total_bad else 0)
