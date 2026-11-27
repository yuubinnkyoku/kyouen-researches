#!/usr/bin/env python3
"""verify_k1337: audit machine for the z=21 min>=16 (floor-16) strip
(claims and scopes in the single-owner declaration note
research/log/2026-11-25-strip-z21-min16-single-owner-note.md; pre-declaration
exploration kit already published at
research/experiments/strip-z21-min16-20261125/, commit 8a106233).

Structural copy of the published verify_k1335.py machine (z=20 min>=15
slice, commit 59741769) with the disclosed z 20 -> 21 textual adaptation:
rung count 14 -> 15, floor 15 -> 16, cell budget j+21 -> j+22, the z=20
line transcriptions (published K1335 cells F20f15..A820f15 + the T-Z20
m=15 theorem row) become the D3 anchor set, D5 z-grid extends to z=22 and
forwarders/counts are re-declared as in the declaration note section 4.

Claims audited here (all UNIVERSAL claims are proven on paper in the note
section 2; this machine independently re-checks the engine agreement and
fail-closed battery totals; battery coverage is finite by construction and
does NOT by itself prove any universal claim):
  A.15 cell lemmas F21f16..A921f16 (floor 16 = every Y token >= 16; s domain
     {0} U {16..}; the 15th rung A921f16 has small token 15 -- the SEVENTH
     consecutive in-band base child of the strip series (min=15, z*(15)=29
     > 21) -- and its Y tokens stay >= 16):
     F21f16(s) = H(23;{1}uY;21) = { s==20: 1 ; s>=22: 2 ; else v(s+1,21,23) }
          (TWELFTH tail form: HOLE+TAIL {z-1 DOWN 1v2, z HOLE, z+1+
          persistent UP 2v0 tail} -- the odd-z hydrogen of the alternation,
          the z-relative profile IDENTICAL to z=17 and z=19: the
          single@(even z) / hole+tail@(odd z) typology alternation is now
          SEVEN consecutive consistent slices (z=z15..z21); supplied by
          the below-band j=1 B-move child (22;Y;22)=v(s,22,22) absorption
          identity v(s,22,22)=v(s,21,22) which holds on {0} U {12..21}
          (K1334 Theorem A, k=21 ODD: [0..k]) and breaks uniformly (0,1)
          for all s>=22 -- the s=22 first break point injects the mex
          minimum 0 into the option set supplying the persistent UP tail;
          the s=20 DOWN deviant is the z=20 F single point supply
          (F20f15(20)=1 -> the (iii) child injects 0); the s=21 identity
          final hold point is exactly the HOLE)
     G21f16(s) = H(24;{2}uY;21) = { s==20: 0 ; else v(s+2,21,24) }
     E21f16(s) = H(25;{3}uY;21) = { s==18: 1 ; s==20: 2 ; else v(s+3,21,25) }
     D21f16(s) = H(26;{4}uY;21) = { s==18: 0 ; else v(s+4,21,26) }
     C21f16(s) = H(27;{5}uY;21) = { s==16: 1 ; s==18: 2 ; else v(s+5,21,27) }
     B21f16(s) = H(28;{6}uY;21) = { s==16: 0 ; else v(s+6,21,28) }
     A21f16(s) = H(29;{7}uY;21) = { s==16: 2 ; else v(s+7,21,29) }   (UP
          2v0 at s=16=z-5 -- the A-RANK BREAK REBIRTH on the third
          consecutive odd slice (z=17 s=12, z=19 s=14, z=21 s=16, all
          UP 2v0); the even-z A annihilation is 4/4 (z=16, z=18, z=20
          A..A8 fully collapsed))
     A221f16(s) = H(30;{8}uY;21) = v(s+8,21,30)                    (NONE;
          the A21f16 s=16 UP supply 2 rides above the mex minimum and is
          absorbed)
     A321f16(s) = H(31;{9}uY;21) = v(s+9,21,31)                    (NONE)
     A421f16(s) = H(32;{10}uY;21) = v(s+10,21,32)                  (NONE)
     A521f16(s) = H(33;{11}uY;21) = v(s+11,21,33)                  (NONE)
     A621f16(s) = H(34;{12}uY;21) = v(s+12,21,34)                  (NONE)
     A721f16(s) = H(35;{13}uY;21) = v(s+13,21,35)                  (NONE)
     A821f16(s) = H(36;{14}uY;21) = v(s+14,21,36)                  (NONE)
     A921f16(s) = H(37;{15}uY;21) = v(s+15,21,37)                  (NONE;
          the SEVENTH consecutive in-band base child z*(15)=29>21; the
          (iii) C-hand child (36;{15}uY;20) is the published T-Z20 m=15-row
          claim position, deviant-free by the published theorem)
     (v = published K0832 single-token closed form.)
     Deviant station triplet (odd-z form, 3/3 with z=17/z=19): value
     multiset {DOWN:1, DOWN:0, UP:2} at positions {C,B,A}@16,
     {E,D}@18, {F,G,E}@20 -- the exact +2 shift of the published z=19
     profile, same rank heads. Observed deviant position set {16,18,20}
     inherited from z=20 exactly (no definition-domain exclusion at the
     odd step; the (even, following-odd) pair rule 3/3).
  T-Z21: for every multiset X with min(X) = m >= 16:
     H(m+22; X; 21) = v(S,21,m+22), S = sum(X). Base m=16 is trivial
     absorption through the fully collapsing A921f16 (the a=16 child);
     m >= 17 is the option-set-identity induction (a=m child = row m-1
     claim position, a>m children = K1264 stair, C-hand child = published
     T-Z20 line rows m >= 15).
  The z=20 lines used by the T-Z21/C-hand recursion (published K1335
  declaration note section 1 cell lemmas F20f15..A820f15 and theorem
  T-Z20) are re-anchored against the engine here (transcriptions checked
  independently; NOT taken on faith). NOTE: the K1335 lines for j=1..14
  carry the floor-15 Y domain {0} U {15..}; the T-Z21 C-hand positions use
  Y tokens >= 16 (subset), and the D3 anchor sweeps use the full K1335
  floor-15 domain (Y=(s,) with s >= 15) which is exactly the published
  lemma domain.

Battery (fail-closed: every gate must produce EXACTLY the declared point
count; any mismatch or failed point sets overall_bad > 0 and rc 1):
  D1 cells        1,440 pts (15 cells x 96 exhaustive floor-16 shapes,
                          s in {0} U {16..46}, arity 0..4)
  D2 strip          150 pts (m in 16..20, S in m..m+39, Y parts >= m,
                          arity(Y) <= 3, engine vs v; identical sweep to
                          the frozen census kit section (c), cumulative
                          44/79/107/130/150)
  D3 z20 anchors    478 pts (14 lines x 32 s-values in {0} U {15..45}
                          = 448 + 30 T-Z20 C-hand anchors m in 15..20)
  D4 stair anchors  465 pts (15 x 31 A-on-Y child stair positions,
                          s in 16..46)
  D5 self anchors 14,697 pts (single-token engine-vs-v grid, x in 1..30,
                          z in 0..22 (z=22 needed by the below-band
                          identity pair), 21 R-points each = 14,490;
                          + 207 empty-position anchors)
  D6 deviant/collapse witnesses 23 pts (literal values, direction and
                          collapse-target checks; includes the F21f16
                          twelfth-form DOWN point s=20, the s=21 HOLE
                          conforming point, the s=22 first tail point and
                          the far tail spot, the G/E/D/C/B DOWN+UP
                          reconstructions, the A21f16 A-RANK BREAK
                          rebirth witness, the A221f16 supply-absorption
                          witness and the fully collapsing in-band base
                          child A921f16 spots)
  D7 extension anchors 133 pts (tail spots s in 47..54 x 15 cells = 120
                          -- F 8/8 declared TAIL 2, all other 112 rows
                          the collapse form (the odd-form signature) --,
                          strip spots m in 21..24 = 12, m=16 base spot
                          = 1)
  D8 belowband anchors 96 pts (the below-band (ii') supply-source
                          position H(22;Y;22) vs v(s,22,22) over the full
                          floor-16 census domain)

MODES: default full battery (rc 0 iff overall_bad == 0).
  --tamper-engine      rc 2 (engine block sha mismatch)
  --tamper=cell       flip one declared cell value     -> rc 1, D1 bad
  --tamper=strip      flip one D2 expected value       -> rc 1, D2 bad
  --tamper=anchor20   flip one z20 transcription value -> rc 1, D3 bad
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
        'cell', 'strip', 'anchor20', 'stair', 'deviant', 'ext', 'belowband'), TAMPER
TAM = TAMPER[0] if TAMPER else None

# ---------------------------------------------------------------------------
# Declared z=21 floor-16 cell closed forms (K1337 claims). Domain: all Y
# tokens >= 16, s = sum(Y) in {0} U {16..} (Y blank iff s=0), arity arbitrary.
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
CELLS = [(1, F21), (2, G21), (3, E21), (4, D21),
         (5, C21), (6, B21), (7, A21), (8, A221),
         (9, A321), (10, A421), (11, A521), (12, A621),
         (13, A721), (14, A821), (15, A921)]

if TAM == 'cell':  # flip one declared deviant value (G21f16 s=20: 0 -> 1)
    def G21(s):
        return (1 if s == 20 else
                v(s + 2, 21, 24))
    CELLS = [(1, F21), (2, G21), (3, E21), (4, D21),
             (5, C21), (6, B21), (7, A21), (8, A221),
             (9, A321), (10, A421), (11, A521), (12, A621),
             (13, A721), (14, A821), (15, A921)]

# ---------------------------------------------------------------------------
# Transcribed published z=20 lines (K1335 declaration note section 1
# statements; floor-15 domain {0} U {15..} for the 14 cells; used by the
# z=21 C-hand recursion for j=1..14; the j=15 C-hand child is the T-Z20
# theorem line (min=15), anchored by the D3 C-hand sweep). Re-anchored
# against the engine by D3 (independent of the K1335 official verification
# state).
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
LINES20 = [(1, F20), (2, G20), (3, E20), (4, D20),
           (5, C20), (6, B20), (7, A20), (8, A220), (9, A320),
           (10, A420), (11, A520), (12, A620), (13, A720), (14, A820)]

if TAM == 'anchor20':  # flip one transcription value (B20f15 s=16: 2 -> 0)
    def B20(s):
        return 0 if s == 16 else v(s + 6, 20, 27)
    LINES20 = [(1, F20), (2, G20), (3, E20), (4, D20),
               (5, C20), (6, B20), (7, A20), (8, A220), (9, A320),
               (10, A420), (11, A520), (12, A620), (13, A720), (14, A820)]


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
declared = 1440
pts = 0; bad = 0
for j, fn in CELLS:
    R = j + 22
    for s in [0] + list(range(16, 47)):
        ys = [()] if s == 0 else parts(s, 16, 4)
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            hv = H(R, X, 21)
            pts += 1
            if hv != fn(s):
                bad += 1
    H.cache_clear()
total_bad += run_gate('D1_cells', declared, pts, bad)

# --- D2: T-Z21 strip sweep ---------------------------------------------------
declared = 150
pts = 0; bad = 0
if TAM == 'strip':
    flipped = set()
for m in range(16, 21):
    for S in range(m, m + 40):
        for X in parts(max(S - m, 0), m, 3):
            XX = tuple(sorted((m,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(m + 22, XX, 21)
            ev = v(S, 21, m + 22)
            pts += 1
            if TAM == 'strip' and (m, S, XX) not in flipped and len(flipped) == 0:
                flipped.add((m, S, XX)); ev = (ev + 1) % 3
            if hv != ev:
                bad += 1
    H.cache_clear()
total_bad += run_gate('D2_strip', declared, pts, bad)

# --- D3: z20 line transcriptions + T-Z20 C-hand anchors ---------------------
declared = 478
pts = 0; bad = 0
for j, fn in LINES20:
    for s in [0] + list(range(15, 46)):
        X = (j, s) if s > 0 else (j,)
        hv = H(j + 21, tuple(sorted(X, reverse=True)), 20)
        ev = fn(s)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
# T-Z20 C-hand anchors: the (iii) child of the T-Z21 claim position at
# min=m is (m+21; X; 20) = the published T-Z20 m-row claim position.
# m=15 anchors the A921f16 cell C-hand child (the T-Z20 m=15 row);
# m in 16..20 anchor the strip rows.
for m in range(15, 21):
    for i in range(1, 6):
        X = tuple(sorted((m, m + i), reverse=True))
        hv = H(m + 21, X, 20)
        ev = v(2 * m + i, 20, m + 21)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D3_z20_anchors', declared, pts, bad)

# --- D4: stair anchors (A-on-Y children of cell parents) ---------------------
declared = 465
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(16, 47):
        child = tuple(sorted((j, s - 1), reverse=True))
        hv = H(j + 21, child, 21)
        ev = v(s + j - 1, 21, j + 21)
        if TAM == 'stair' and j == 3 and s == 16:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D4_stair_anchors', declared, pts, bad)

# --- D5: self anchors (single-token v grid + empty positions) ---------------
grid = []
for x in range(1, 31):
    for z in range(0, 23):
        rs = [0, 1, 5, 14, 17, 18, 19, 20, 21, 22, 23, 24,
              25, 26, 27, 28, 29, 30, x + z - 1, x + z, x + z + 1]
        for R in rs:
            if R < 0 or R > 81:
                continue
            grid.append((x, z, R))
declared = len(grid) + 207
pts = 0; bad = 0
for (x, z, R) in grid:
    hv = H(R, (x,), z)
    ev = v(x, z, R)
    pts += 1
    if hv != ev:
        bad += 1
H.cache_clear()
for R in range(0, 9):
    for z in range(0, 23):
        hv = H(R, (), z)
        pts += 1
        if hv != 0:
            bad += 1
total_bad += run_gate('D5_self_anchors', declared, pts, bad)

# --- D6: deviant / collapse witness literals --------------------------------
WITNESSES = [
    # (j, s, declared_value, collapse_target, direction)
    (1, 16, 1, 1, 'FLAT'),    # F21f16 in-identity flat (identity holds 16..21)
    (1, 18, 1, 1, 'FLAT'),    # F21f16 flat over the z=20 F supply-free zone
    (1, 19, 0, 0, 'FLAT'),    # F21f16 flat one below the published z20 point
    (1, 20, 1, 2, 'DOWN'),    # F21f16 TWELFTH-form DOWN s=20 1v2
                              # (the z=20 F single point F20f15(20)=1 supply)
    (1, 21, 0, 0, 'FLAT'),    # F21f16 HOLE at the identity final hold point
    (1, 22, 2, 0, 'UP'),      # F21f16 first tail point (k=21 first break)
    (1, 52, 2, 0, 'UP'),      # F21f16 far tail spot (window-external)
    (2, 18, 0, 0, 'FLAT'),    # G21f16 flat (G20f15 s=18 DOWN supply absorbed)
    (2, 20, 0, 1, 'DOWN'),    # G21f16 DOWN (G20f15 s=20 UP supply mirror)
    (2, 22, 1, 1, 'FLAT'),    # G21f16 break-region flat
    (3, 18, 1, 2, 'DOWN'),    # E21f16 DOWN (E20f15 s=18 UP supply mirror)
    (3, 20, 2, 0, 'UP'),      # E21f16 UP (G21f16 s=20 DOWN supply mirror)
    (4, 16, 0, 0, 'FLAT'),    # D21f16 mex-absorption of the D20f15 supply
    (4, 18, 0, 1, 'DOWN'),    # D21f16 DOWN (E21f16 s=18 DOWN supply mirror)
    (5, 16, 1, 2, 'DOWN'),    # C21f16 DOWN (C20f15 s=16 UP supply mirror)
    (5, 18, 2, 0, 'UP'),      # C21f16 UP (D21f16 s=18 DOWN supply mirror)
    (6, 16, 0, 1, 'DOWN'),    # B21f16 DOWN (C21f16 s=16 DOWN supply mirror)
    (6, 18, 1, 1, 'FLAT'),    # B21f16 flat (C21f16 UP supply absorbed)
    (7, 16, 2, 0, 'UP'),      # A21f16 A-RANK BREAK REBIRTH s=16=z-5 UP 2v0
    (7, 20, 0, 0, 'FLAT'),    # A21f16 flat at the supply position s=20
    (8, 16, 1, 1, 'FLAT'),    # A221f16 absorbs the A21f16 UP supply above mex
    (15, 16, 0, 0, 'FLAT'),   # A921f16 base-child cell spot (in-band base)
    (15, 52, 0, 0, 'FLAT'),   # A921f16 far tail spot
]
declared = len(WITNESSES)
pts = 0; bad = 0
for (j, s, val, cval, direction) in WITNESSES:
    if TAM == 'deviant' and j == 1 and s == 20:
        val = (val + 1) % 3
    X = (j, s)
    hv = H(j + 22, X, 21)
    col = v(s + j, 21, j + 22)
    pts += 1
    ok = (hv == val) and (col == cval)
    d = 'UP' if val > col else ('DOWN' if val < col else 'FLAT')
    if d != direction:
        ok = False
    if not ok:
        bad += 1
total_bad += run_gate('D6_deviant_witnesses', declared, pts, bad)

# --- D7: extension anchors (tail spots + strip spots + base spot) ----------
declared = 133
pts = 0; bad = 0
for j, fn in CELLS:
    for s in range(47, 55):
        X = (j, s)
        hv = H(j + 22, X, 21)
        ev = fn(s)
        if TAM == 'ext' and j == 1 and s == 47:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
for m in range(21, 25):
    for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
        X = tuple(sorted(shp, reverse=True))
        hv = H(m + 22, X, 21)
        ev = v(sum(X), 21, m + 22)
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
hv = H(38, (16, 16), 21)
ev = v(32, 21, 38)
pts += 1
if hv != ev or ev != 1:
    bad += 1
total_bad += run_gate('D7_extension_anchors', declared, pts, bad)

# --- D8: belowband (ii') supply-source anchors -------------------------------
# H(22; Y; 22) = v(s, 22, 22) for every floor-16 multiset Y (empty at s=0
# by K1312-stair-type collapse; the identity v(s,22,22)=v(s,21,22) below).
# This is the below-band j=1 B-move child whose absorption identity
# v(s,22,22)=v(s,21,22) holds on {0} U {12..21} (K1334 Theorem A, k=21
# ODD: [0..k]) and breaks uniformly (0,1) for all s>=22 (supplying the
# F21f16 persistent tail from s=22 = z+1; the s=21 final hold point is
# exactly the HOLE).
declared = 96
pts = 0; bad = 0
for s in [0] + list(range(16, 47)):
    ys = [()] if s == 0 else parts(s, 16, 4)
    for y in ys:
        hv = H(22, y, 22)
        ev = v(s, 22, 22)
        if TAM == 'belowband' and pts == 0:
            ev = (ev + 1) % 3
        pts += 1
        if hv != ev:
            bad += 1
    H.cache_clear()
total_bad += run_gate('D8_belowband_anchors', declared, pts, bad)

battery_declared = sum(g['declared_pts'] for g in gates.values())
battery_pts = sum(g['pts'] for g in gates.values())
res = {'machine': 'verify_k1337', 'engine_sha': sha, 'mode': TAM or 'full',
       'gates': gates, 'battery_declared_pts': battery_declared,
       'battery_pts': battery_pts, 'overall_bad': total_bad,
       'result': 'FAIL' if total_bad else 'PASS'}
print(json.dumps(res, sort_keys=True, separators=(',', ':')))
sys.exit(1 if total_bad else 0)
