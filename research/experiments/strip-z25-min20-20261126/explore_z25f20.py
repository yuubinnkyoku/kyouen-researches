#!/usr/bin/env python3
"""
explore_z25f20: FROZEN PRE-DECLARATION census for the z=25 FLOOR-20
(z-5, CRITICAL floor) cell ladder — the natural pre-cursor census of
the future T-Z25 declaration lane, in the exact role the published
z22-min17 (`115c0bb9`) and z23-min18 (`25522d56`) census kits played
for K1339/K1344, and the first z=25 slice work of any kind on main.
NO K slot is claimed by this file; the constants below were frozen
into this docstring BEFORE the first run of this file and the file is
not edited after any of its runs.

Counter-probe (pre-claim, at kit-build time, head `c77e79ab`): main
contains NO z=25 census kit (filename:explore_z25 -> 0 hits), no
T-Z25 declaration (the only "T-Z25" hits are handoff references in
the published m18spot log), no floor-20 experiment kit. The published
registered handoffs taken here, from the m18spot kit log section 5
(commit `b8146415`): item #1 (TWENTY-THIRD-tail k=32 registered
candidate), item #3 (z=26 base-spot blind picks) and item #4 (z=25
residual-band record entries incl. the m=14 band COMPLETION). Item #2
(z=26 floor-20 sub-critical lattice) is NOT taken here — its head-row
derivation naturally depends on THIS kit's own s=20 row; it belongs to
the next execution once these bytes are published.

HONEST DISCLOSURE (drafting discipline, before the freeze): the head
row (s=20) below was DERIVED BY HAND in-session from published inputs
ONLY: (1) the published z24f18 frozen census s=20 row (finite
observations: deviants D/C/B = heads {0,1,2} at j=4/5/6, every other
rung conform at its PROVED K0832 collapse constant), (2) published
z24f18 zero-violation sweeps for the j>=18 C-children (m=18-row z=24
record position H(43;(18,20);24), strip m=19 position
H(44;(19,20);24), strip m=20 position H(45;(20,20);24)), (3) the
PROVED K0832 closed form for every stair/removal/collapse literal,
(4) the PROVED K1264 stair equality at the floor-token decrease, and
(5) the left-to-right in-head cascade. The drafting scratch machine
cross-checked ONLY these published z=24 input literals against the
engine (20/20 exact matches); it evaluated NO z=25 or z=26
multi-token position, and no single-token z=25/z=26 engine position
either — every z=25/z=26 value below is touched by the engine for
the first time at the frozen first run. The s>=21 rows are NOT
derivable from published data (the z=24 census rows are finite
observations, not proved constants) — they are pre-declared
STRUCTURAL candidates from the published odd critical-chain     profile
(K1330 z=19 / K1337 z=21 / K1344 z=23, all PROVED): the mirror
station rule {DOWN 1v2, DOWN 0v1, UP 2v0} at {z-5, z-3, z-1} =
{20, 22, 24} as {C,B,A} / {E,D,C} / {F,G,E}, the F HOLE at s=z=25
(conform) and the F persistent tail UP 2v0 for all s >= 26; candidate
4/4 of the odd critical station rule, candidate 10th consecutive
slice of the F-family typology alternation (odd = HOLE+TAIL), and the
odd-z A RANK BREAK REBIRTH candidate at s=z-5=20 (A25f20 UP 2v0,
5th odd instance after z=17/19/21/23).

Scope (this file measures and reports; it proves nothing):

  (a) cell census: for each j in 1..20 (rungs F,G,E,D,C,B,A,A2..A14)
      the floor-20 cell Cell_j(s) := H(j+26; {j} U Y; 25), Y tokens
      >= 20, s = sum(Y) in {0} U {20..51}, arity(Y) in 0..4 (0 only
      at s=0), swept EXHAUSTIVELY against the published raw engine
      (K1138 recursion, embedded block byte-identical to the
      K1282..K1344 chain, pin bd5f22e4...). Reported per cell:
      deviants from the Sigma-collapse v(s+j,25,j+26) (K0832 closed
      form) and any multivalue (decomposition-dependence) rows.
      20 rungs = F..A14: A13 (j=19) is the future T-Z25 absorption-
      bottom candidate domain (the a=20 child of the T-Z25 bottom
      m=20 row lands on Cell_19 exactly: (45;{19} U Y;25), the 8th
      consecutive in-band base child candidate z*(19)=37>25); A14
      (j=20) is swept as beyond-bottom EXTENSION coverage (its
      C-child input H(45;(20,20);24) is covered by the published
      z24f18 strip m=20 sweep, so the rank is derivable; no
      published kit swept it before — disclosed as an extra rung, not
      a convention match).
      PREDECLARED CANDIDATES (frozen before the first run):
      (i) THE s=20 ROW (derived, per-rung option sets below):
          j=1  F   CONFORM  v(21,25,27)=1   ({stair v(20,25,26)=0,
               removal v(20,26,25)=0, 1^c1=1^1=0} -> mex 1);
          j=2  G   CONFORM  v(22,25,28)=0   ({stair v(21,25,27)=1,
               cascade 1, 1^c2=1^0=1} -> mex 0);
          j=3  E   CONFORM  v(23,25,29)=1   ({stair v(22,25,28)=0,
               cascade 0, 1^c3=1^1=0} -> mex 1);
          j=4  D   CONFORM  v(24,25,30)=0   ({stair v(23,25,29)=1,
               cascade 1, 1^c4=1^0=1} -> mex 0);
          j=5  C   DOWN 1v2 v(25,25,31)=2   ({stair v(24,25,30)=0,
               cascade 0, 1^c5=1^1=0} -> mex 1);
          j=6  B   DOWN 0v1 v(26,25,32)=1   ({stair v(25,25,31)=2,
               cascade 1, 1^c6=1^2=3} -> mex 0);
          j=7  A   UP   2v0 v(27,25,33)=0   ({stair v(26,25,32)=1,
               cascade 0, 1^c7=1^0=1} -> mex 2) — THE ODD-CRITICAL
               STATION TRIPLET {C DOWN 1v2, B DOWN 0v1, A UP 2v0} AT
               s=z-5=20, the A RANK BREAK REBIRTH candidate (5th odd
               instance after z=17/19/21/23);
          j=8  A2  CONFORM v(28,25,34)=1   ({stair 0, cascade 2,
               1^c8=1^1=0} -> mex 1, the REBIRTH-ABSORPTION option
               set: the cascade value 2 enters but the mex still conforms);
          j=9..19 A3..A13 CONFORM (the cascade re-locks: odd j
               options {1,1,1} -> mex 0, even j options {0,0,0} ->
               mex 1, in step with the collapse
               v(20+j,25,j+26); A13 (j=19) conform 0 =
               v(39,25,45));
          j=20 A14 CONFORM v(40,25,46)=1   (X=(20,20): both
               decreases coincide with Cell_19(20), options {cascade
               head_19=0, 1^c20=1^1=0} -> mex 1).
          where the C-child inputs c_j := H(j+25;{j,20};24) are the
          PUBLISHED z24f18 census values at s=20:
          c = [1,0,1,0,1,2,0,1,0,1,0,1,0,1,0,1,0,1,0,1] for
          j=1..20 (j=4/5/6 measured deviants 0/1/2; j<=17 others the
          conform closed forms v(20+j,24,j+25); j=18/19/20 the
          published zero-violation record constants v(38,24,43)=1,
          v(39,24,44)=0, v(40,24,45)=1).
      (ii) s in {21..51}, the STRUCTURAL CANDIDATES (blind):
           at s=22 (z-3): E(j=3) DOWN 1v2 (1 vs collapse
               v(25,25,29)=2), D(j=4) DOWN 0v1 (0 vs v(26,25,30)=1),
               C(j=5) UP 2v0 (2 vs v(27,25,31)=0);
           at s=24 (z-1): F(j=1) DOWN 1v2 (1 vs collapse
               v(25,25,27)=2), G(j=2) DOWN 0v1 (0 vs v(26,25,28)=1),
               E(j=3) UP 2v0 (2 vs v(27,25,29)=0);
           F HOLE at s=25: F conFORM (0 = v(26,25,27)), mirror of the
               identity's final hold point;
           F persistent tail for ALL s in {26..51}: F value 2 vs
               collapse v(s+1,25,27)=0 (UP 2v0, the ODD-edition
               F-family HOLE+TAIL typology, candidate 10th
               consecutive slice; single- AND multi-shape rows);
           NO other deviant rows anywhere in {21..51}; 0 multivalue.
           Total predicted deviant rows: 9 point + 26 tail = 35.
      (iii) 0 multivalue rows everywhere (all cells s-only).
  (b) tail spots: s in {52..59}, single-token shape Y=(s,), all 20
      cells — the ODD-edition signature candidate: F(j=1) 8/8 spot
      values 2 vs collapse v(s+1,25,27)=0 (the persistent tail past
      the census domain), the other 19 cells 152/152 CONFORM.
  (c) strip sweep m in {20..25} at R=m+26: NO T-Z25 exists, so
      m=20 is the head-floor row segment (critical-kit convention)
      and m in {21..25} are the would-be T-Z25 claim positions
      (z*(m)=2m-2+(m mod 2) > 25 for all m in {20..25}). Candidates
      0 violations for every segment (the strip family has never
      produced a violation in any published kit).
  (d) IN-BAND row records (x0 published residual-band style, arity
      <= 3 total, S in {m..m+38}):
      (d1) m=18-row z=25 record at R=44: the FIRST-EVER z=25 m=18
           row record (first of the future T-Z24
           declaration band m=18 z in {25..33}; the z=24 entry 26/0
           published by z24f18) + the arity<=4 co-token extension.
           Candidate 0 separations.
      (d2) m=17-row z=25 record at R=43: the future T-Z22 band m=17
           z in {23..32} THIRD entry (published 32/0 at z=23,
           32+31/0 at z=24). Candidate 0 separations.
      (d3) m=16-row z=25 record at R=42: the future T-Z21 band m=16
           z in {22..29} FOURTH entry (published 40/0 at
           z=22/23/24; the m18spot kit additionally measured the
           first two co-token members (16,17)/(16,18) conforming 1/1
           — covered by this record sweep). Candidate 0 separations.
      (d4) m=15-row z=25 record at R=41: the K1335 (T-Z20) band m=15
           z in {21..28} FIFTH entry (published 50/0 at
           z=21/22/23/24). Candidate 0 separations.
      (d5) m=14-row z=25 record at R=40: the K1330 band m=14 z in
           {20..25} SIXTH AND FINAL entry (published 62/0 at
           z=20/21/22/23/24) — the registered BAND COMPLETION
           candidate (m18spot S5 item #4 second part). Candidate 0
           separations, which would close the FIRST fully-swept
           residual band in the series.
      (d6) m=13-row z=25 record at R=39: z*(13)=25 EXACTLY (K1268
           formula 2m-2+(m mod 2)) — the FIRST-EVER row record AT
           THE FRONTIER of its row (the K1328 band m=13 z in
           {19..24} is complete with 76/0 at each of z=19..24; z=25
           sits ON the frontier value). NO CANDIDATE: first contact,
           unexplored regime, the constants are recorded whatever
           they are; any separations are the first observed
           frontier datum of the series.
  (e) strip spots m in {26..29} at R=m+26, X in {(m,m+1),(m,m+2),
      (m,m,m+1)}: NEW z=25 spots (candidate 12/12 conform per the
      strip family), PLUS the z=25 base spots:
      (e1) m=20 base spot H(46;(20,20);25): paper-derived candidate
           1 CONFORMING (options {B-child H(45;(19,20);25) =
           the m=19-strip position with the published-formula
           conform candidate v(39,25,45)=0, 1^c20 = 1^1 = 0} ->
           mex{0,0} = 1 = collapse v(40,25,46)); the two disclosed
           premises (conform values of the m=19 strip and of the
           published z24f18 strip m=20 input c20) are observations
           the run tests together.
      (e2) m=19 base spot H(45;(19,19);25): paper-derived candidate
           0 CONFORMING (options {B-child H(44;(18,19);25) = the
           m=18-row z=25 record position S=37 with conform candidate
           v(37,25,44)=1, 1^H(44;(19,19);24) = 1^v(38,24,44)=1^0=1
           (the published z24f18 strip m=19 input)} -> mex{1,1} = 0
           = collapse v(38,25,45)).
      (e3) published recheck anchors (8 spots, all published by the
           m18spot kit): (44;(18,18);25)=1, (45;(18,18);25)=0,
           (44;{17,18};25)=1, (43;{17,18};25)=0, (43;(17,17);25)=0,
           (42;(17,17);25)=1, (42;{16,17};25)=1, (42;{16,18};25)=1.
  (f) below-band bottom-rung child census: the j=1 cell's removal
      child is the below-band position H(26;Y;26) with min(Y) >= 20
      (child slice z'=26, floor 20 = z'-6, the BB-type supply source
      of the future T-Z25 lane), swept over s in {0} U {20..51},
      arity 0..4, against v(s,26,26). Candidate 0 deviants, 0
      multivalue rows (the published D8 analogs of the critical kits
      were all clean).
  (g) TAIL SUPPLY PRE-COMPUTATIONS (pure published K0832 closed
      form, NO engine recursion), each over the EXTENDED domain
      s in {0} U {12..67}: the CONSOLIDATED 14th..24th tail table
      v(s,k+1,k+1) vs v(s,k,k+1) for k in {23..33}:
      - k=23..31 (14th..22nd): RECHECKS of every published constant
        (odd k: hold {0} U {12..k}, UNIFORM 0v1 for all s >= k+1;
        even k: hold {0} U {12..k-1}, 0v2 at s=k, UNIFORM 2v1 for
        all s >= k+1) — the m18spot consolidated table extended by
        one point and by k=32/33 below.
      - k=32 (23rd) NEW: the REGISTERED candidate of the m18spot
        log S5 item #1: hold {0} U {12..31}, 0v2 break at s=32,
        UNIFORM 2v1 for ALL s in {33..66} — the even-z supply form
        candidate graduates to 7/7 (k=20/22/24/26/28/30 measured +
        k=32 closed-form here).
      - k=33 (24th) NEW registration made by this file (both
        components predeclared before the run): hold {0} U {12..33},
        UNIFORM 0v1 for ALL s in {34..67} — the odd-z supply form
        candidate 8/8 (k=19/21/23/25/27/29/31
        measured + k=33 closed-form here); the z=33-slice supply
        datum for the future z=33 declaration lane.
  (h) z=26 CROSS-SLICE HANDOFF (the m18spot log S5 item #3, four
      FIRST-EVER z=26 engine touches, registered option tables
      frozen here BEFORE the run):
      (h1) H(44;{17,18};26) [the m=17-row z=26 first co-token
           member]: candidate collapse-CONFORM 0 = v(35,26,44).
      (h2) H(43;{16,17};26) [the m=16-row z=26 first co-token
           member]: candidate collapse-CONFORM 1 = v(33,26,43).
      (h3) H(45;(18,18);26) [the m=18 base-spot z-sequence 12th
           on-line member]: candidate 1 = collapse v(36,26,45)
           CONFORMING via the frozen table: options {B-child =
           (h1) [itself first-contact, in-kit premise disclosed],
           C-child 1^H(44;(18,18);25) = 1^1 = 0 PUBLISHED} ->
           mex{0,0} = 1 iff (h1) conforms 0.
      (h4) H(44;(17,17);26) [the m=17 base-spot z-sequence 5th
           on-line member]: candidate 0 = collapse v(34,26,44)
           CONFORMING via the frozen table: options {B-child =
           (h2) [in-kit premise disclosed], C-child
           1^H(43;(17,17);25) = 1^0 = 1 PUBLISHED} -> mex{1,1} = 0
           iff (h2) conforms 1.
      The m=18 on-line z-sequence so far: z in {16..25} =
      0,1,0,1,0,1,0,1,1,1 (published, incl. the two z=25 readings by
      the m18spot kit); the z=26 candidate here is the structural
      continuation BEFORE any z lattice exists (the honest form is
      the full option-set table, not a naked value pick).
  (i) K0832 closed-form-vs-engine battery: every single-token
      literal used by this file's derivations (stair/removal
      children, collapses of every measured anchor spot, supply
      sample points), each checked closed_form == vC == vO against
      the raw engines.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z25f20.out).
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
assert sha == PIN, sha
ns = {'lru_cache': lru_cache}
exec(ENGINE_BLOCK, ns)
H = ns['H_canonical']
v = ns['single_token']




def parts(s, lo, arity):
    """all multisets (nondecreasing tuples) of tokens >= lo, sum s, 1..arity tokens"""
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


def cell_sweep(j, smax):
    """sweep cell_j over s in {0} U {20..smax}; returns (dev, multi, total)"""
    R = j + 26
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(20, smax + 1)):
        ys = [()] if s == 0 else parts(s, 20, 4)
        vals = {}
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            h = H(R, X, 25)
            vals.setdefault(h, []).append(y)
            total += 1
        if len(vals) > 1:
            multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s + j, 25, R)
            if val != exp:
                dev.append({'s': s, 'value': val, 'collapse': exp,
                            'direction': 'UP' if val > exp else 'DOWN',
                            'shapes': len(vals[val])})
    H.cache_clear()
    return dev, multi, total


def row_record(sec, rlabel, extra, R, z, m, smin, smax, min_tok):
    """co-token style sweep: X = (m,) U parts >= min_tok (arity up to 4 total)."""
    H.cache_clear()
    sep = []
    scnt = 0
    for S in range(smin, smax + 1):
        for X in parts(max(S - m, 0), min_tok, 3):
            XX = tuple(sorted((m,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(R, XX, z)
            ev = v(S, z, R)
            scnt += 1
            if hv != ev:
                sep.append({'X': list(XX), 'S': S, 'value': hv,
                            'collapse': ev,
                            'direction': 'UP' if hv > ev else 'DOWN'})
    return {'section': sec, 'label': rlabel, 'R': R, 'z': z, 'min': m,
            **extra, 'shapes': scnt, 'separations': sep}


def row_record_x0(sec, rlabel, extra, R, z, m, smin, smax):
    """published residual-band record style: X = parts(S, m, 3) with
    X[0] == m, i.e. all parts >= m with co-token m allowed, arity <= 3
    TOTAL. Shape-for-shape comparable with the published entries."""
    H.cache_clear()
    sep = []
    scnt = 0
    for S in range(smin, smax + 1):
        for X in parts(S, m, 3):
            if not X or X[0] != m:
                continue
            hv = H(R, X, z)
            ev = v(S, z, R)
            scnt += 1
            if hv != ev:
                sep.append({'X': list(X), 'S': S, 'value': hv,
                            'collapse': ev,
                            'direction': 'UP' if hv > ev else 'DOWN'})
    return {'section': sec, 'label': rlabel, 'R': R, 'z': z, 'min': m,
            **extra, 'shapes': scnt, 'separations': sep}


ORDINAL = {23: 'fourteenth', 24: 'fifteenth', 25: 'sixteenth',
           26: 'seventeenth', 27: 'eighteenth', 28: 'nineteenth',
           29: 'twentieth', 30: 'twenty-first', 31: 'twentysecond',
           32: 'twentythird', 33: 'twentyfourth'}


def main():
    out = []
    out.append({'section': 'engine_gate', 'engine_sha': sha, 'pin': PIN,
                'gate': 'PASS'})
    vC = ns['vC']
    vO = ns['vO']
    # (i) K0832 battery: every single-token literal used by the file.
    battery_lits = []
    for j in range(1, 21):                       # stair children j=1..20
        battery_lits.append((19 + j, 25, j + 25))
    battery_lits.append((20, 26, 25))            # j=1 removal child
    # head/station collapse literals
    for (x, z2, R2) in [(21,25,27),(22,25,28),(23,25,29),(24,25,30),
                        (25,25,31),(26,25,32),(27,25,33),(28,25,34),
                        (29,25,35),(30,25,36),(31,25,37),(32,25,38),
                        (33,25,39),(34,25,40),(35,25,41),(36,25,42),
                        (37,25,43),(38,25,44),(39,25,45),(40,25,46),
                        (25,25,29),(26,25,30),(27,25,31),(25,25,27),
                        (26,25,28),(26,25,27),(27,25,27),(52,25,27),
                        (59,25,27)]:
        battery_lits.append((x, z2, R2))
    # measured anchor spot collapses (z=25 rechecks, base spots, z=26)
    for (x, z2, R2) in [(36,25,44),(36,25,45),(35,25,44),(35,25,43),
                        (34,25,43),(34,25,42),(33,25,42),(34,25,42),
                        (40,25,46),(38,25,45),(37,25,44),(39,25,45),
                        (38,24,43),(39,24,44),(40,24,45),(21,24,26),
                        (38,24,44),(35,26,44),(33,26,43),(36,26,45),
                        (34,26,44)]:
        battery_lits.append((x, z2, R2))
    # C-child input literals of the head derivation (z=24 published)
    for j in range(1, 21):
        if j not in (4, 5, 6) and j <= 17:
            battery_lits.append((20 + j, 24, j + 25))
    # supply identity sample points
    for (x, z2, R2) in [(12,33,33),(31,33,33),(32,33,33),(32,32,33),
                        (33,33,33),(66,33,33),(12,34,34),(33,34,34),
                        (34,34,34),(33,33,34),(67,34,34)]:
        battery_lits.append((x, z2, R2))
    battery = []
    bad_bat = 0
    for (x, z2, R2) in battery_lits:
        cf = v(x, z2, R2)
        cn = vC(x, z2, R2)
        od = vO(x, z2, R2)
        ok = (cf == cn == od)
        if not ok:
            bad_bat += 1
        battery.append({'x': x, 'z': z2, 'R': R2, 'closed': cf,
                        'vC': cn, 'vO': od, 'match': ok})
    out.append({'section': 'k0832_battery', 'literals': len(battery),
                'all_match': bad_bat == 0, 'bad': bad_bat,
                'rows': battery})
    # (a) cell census j=1..20 (F..A14)
    cells = {}
    names = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
             'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12',
             'A13', 'A14']
    for j in range(1, 21):
        name = names[j - 1]
        dev, multi, total = cell_sweep(j, 51)
        cells[f'cell{j}_{name}25f20'] = {
            'z': 25, 'min': j, 'R': j + 26, 'floor': 20,
            's_domain': '{0} U {20..51}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}25f20',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots s in {52..59}
    tail = []
    for j in range(1, 21):
        nm = names[j - 1]
        for s in range(52, 60):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 26, X, 25)
            exp = v(s + j, 25, j + 26)
            tail.append({'cell': f'{nm}25f20', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s52_59', 'rows': tail})
    # (c) strip sweep m in {20..25} at R=m+26 (no T-Z25 exists)
    sv = []
    viol = []
    cnt = 0
    for m in range(20, 26):
        H.cache_clear()
        for S in range(m, m + 40):
            for X in parts(max(S - m, 0), m, 3):
                XX = tuple(sorted((m,) + X, reverse=True))
                if sum(XX) != S:
                    continue
                hv = H(m + 26, XX, 25)
                ev = v(S, 25, m + 26)
                cnt += 1
                if hv != ev:
                    viol.append({'m': m, 'X': list(XX), 'S': S,
                                 'value': hv, 'collapse': ev})
        sv.append({'m': m, 'cumulative_shapes': cnt,
                   'cumulative_violations': len(viol)})
    out.append({'section': 'strip_z25_m20_25', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d1) m=18-row z=25 record — FIRST-EVER z=25 m=18 row record.
    out.append(row_record_x0(
        'inband_m18_z25_row_record',
        'first_ever_z25_m18_row_record_in_band_future_tz24_band_m18_z_25_33',
        {'co_token_18_allowed': True,
         'residual_band': 'no band published (future T-Z24 declaration residual band m=18 z in {25..33} unborn; frontier z*(18)=34 per K1268); published z=24 entry: 26 shapes 0 separations (z24f18 kit); candidate 0 separations here',
         's_domain': '{18..56}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        44, 25, 18, 18, 56))
    out.append(row_record(
        'inband_m18_z25_row_record_ext_arity4',
        'arity_le4_extension_cotoken_style',
        {'co_token_18_allowed': True,
         's_domain': '{18..56}', 'arity_max': 4},
        44, 25, 18, 18, 56, 18))
    # (d2) m=17-row z=25 record (future T-Z22 band third entry).
    out.append(row_record_x0(
        'inband_m17_z25_row_record',
        'future_tz22_residual_band_m17_z25_third_entry',
        {'co_token_17_allowed': True,
         'residual_band': 'future T-Z22 declaration residual band m=17 z in {23..32} (frontier z*(17)=33); published entries: z=23 32/0, z=24 32+31 shapes 0 separations; candidate 0 separations here',
         's_domain': '{17..55}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        43, 25, 17, 17, 55))
    # (d3) m=16-row z=25 record (fourth entry).
    out.append(row_record_x0(
        'inband_m16_z25_row_record',
        'future_tz21_residual_band_m16_z25_fourth_entry',
        {'co_token_16_allowed': True,
         'residual_band': 'future T-Z21 residual band m=16 z in {22..29}; published entries: 40/0 at z=22/23/24; the m18spot kit measured the two co-token members (42;{16,17};25)=1 and (42;{16,18};25)=1 (covered again here); candidate 0 separations',
         's_domain': '{16..54}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        42, 25, 16, 16, 54))
    # (d4) m=15-row z=25 record (K1335 band fifth entry).
    out.append(row_record_x0(
        'inband_m15_z25_row_record',
        'k1335_residual_band_m15_z25_fifth_entry',
        {'co_token_15_allowed': True,
         'residual_band': 'K1335 (T-Z20) published residual band m=15 z in {21..28} (frontier z*(15)=29, band completes at z=28); published entries: 50/0 at z=21/22/23/24; candidate 0 separations here',
         's_domain': '{15..53}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        41, 25, 15, 15, 53))
    # (d5) m=14-row z=25 record (K1330 band SIXTH AND FINAL entry).
    out.append(row_record_x0(
        'inband_m14_z25_row_record',
        'k1330_residual_band_m14_z25_sixth_final_entry_band_completion_candidate',
        {'co_token_14_allowed': True,
         'residual_band': 'K1330 published m=14 z in {20..25} (frontier z*(14)=26); published entries: 62/0 at z=20/21/22/23/24; z=25 is the SIXTH AND FINAL in-band entry — the registered BAND COMPLETION candidate (m18spot S5 item #4); candidate 0 separations would close the first fully-swept residual band of the series',
         's_domain': '{14..52}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        40, 25, 14, 14, 52))
    # (d6) m=13-row z=25 record (AT the frontier z*(13)=25): NO candidate.
    out.append(row_record_x0(
        'inband_m13_z25_row_record',
        'k1328_band_m13_z25_AT_FRONTIER_zstar13_equals_25_FIRST_CONTACT_no_candidate',
        {'co_token_13_allowed': True,
         'residual_band': 'K1328 published m=13 z in {19..24} complete with 76/0 at each entry; z*(13)=25 (K1268 formula) and z=25 sits EXACTLY ON the frontier value — the FIRST-EVER row record at the frontier of its own row; NO CANDIDATE predeclared (first contact, unexplored regime); separations recorded whatever they are',
         'no_prediction': 'first contact at the K1268 frontier; both outcomes (clean row or first observed frontier separation) are new finite data',
         's_domain': '{13..51}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        39, 25, 13, 13, 51))
    # (e) strip spots m in {26..29} + z=25 base spots + published rechecks
    spots = []
    for m in range(26, 30):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 26, X, 25)
            ev = v(S, 25, m + 26)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    out.append({'section': 'strip_spots_m26_29', 'rows': spots})
    # (e1) m=20 base spot (paper-derived candidate 1, conforming)
    w20 = H(46, (20, 20), 25)
    w20v = v(40, 25, 46)
    out.append({'section': 'm20_base_spot', 'X': [20, 20], 'R': 46,
                'z': 25, 'value': w20, 'collapse_single': w20v,
                'match': w20 == w20v,
                'published_probe_crossref': 'NEW measurement (no published kit measured H(46;(20,20);25)); paper-derived candidate value 1 = v(40,25,46) conforming, derivation frozen in this file docstring before the first run (B-child on the m=19-strip z=25 position H(45;(19,20);25) with conform candidate v(39,25,45)=0 (in-kit premise), C-child 1^H(45;(20,20);24) = 1^1 = 0 on the published z24f18 strip m=20 input)'})
    # (e2) m=19 base spot (paper-derived candidate 0, conforming)
    w19 = H(45, (19, 19), 25)
    w19v = v(38, 25, 45)
    out.append({'section': 'm19_base_spot', 'X': [19, 19], 'R': 45,
                'z': 25, 'value': w19, 'collapse_single': w19v,
                'match': w19 == w19v,
                'published_probe_crossref': 'NEW measurement (no published kit measured H(45;(19,19);25)); paper-derived candidate value 0 = v(38,25,45) conforming, derivation frozen in this file docstring before the first run (B-child on the m=18-row z=25 record position H(44;(18,19);25) S=37 with conform candidate v(37,25,44)=1 (in-kit premise), C-child 1^H(44;(19,19);24) = 1^v(38,24,44) = 1^0 = 1 on the published z24f18 strip m=19 input)'})
    # (e3) published recheck anchors (8 spots, m18spot kit)
    rechecks = []
    for (R, X, expected) in [
            (44, (18, 18), 1), (45, (18, 18), 0), (44, (17, 18), 1),
            (43, (17, 18), 0), (43, (17, 17), 0), (42, (17, 17), 1),
            (42, (16, 17), 1), (42, (16, 18), 1)]:
        XX = tuple(sorted(X, reverse=True))
        hv = H(R, XX, 25)
        S = sum(X)
        ev = v(S, 25, R)
        rechecks.append({'R': R, 'X': list(XX), 'value': hv,
                         'collapse': ev, 'published_value': expected,
                         'match': hv == ev == expected})
    out.append({'section': 'published_recheck_anchors_z25', 'rows': rechecks})
    # (f) below-band j=1 removal child H(26;Y;26), Y >= 20
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(20, 52)):
        ys = [()] if s == 0 else parts(s, 20, 4)
        vals = {}
        for y in ys:
            h = H(26, y, 26)
            vals.setdefault(h, []).append(y)
            bb_total += 1
        if len(vals) > 1:
            bb_multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s, 26, 26)
            if val != exp:
                bb_dev.append({'s': s, 'value': val, 'collapse': exp,
                               'direction': 'UP' if val > exp else 'DOWN',
                               'shapes': len(vals[val])})
    out.append({'section': 'belowband_j1_child_H26_26',
                'label': 'observational_only_belowband_supply_source_at_z25_floor20_zprime_minus_6_BB_type',
                'R': 26, 'z': 26, 'floor': 20,
                's_domain': '{0} U {20..51}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (g) consolidated tail supply identities k in {23..33}
    for k in range(23, 34):
        holds = []
        breaks = []
        for s in [0] + list(range(12, 68)):
            a = v(s, k + 1, k + 1)
            b = v(s, k, k + 1)
            row = {'s': s, f'v_{k+1}_{k+1}': a, f'v_{k}_{k+1}': b,
                   'equal': a == b}
            (holds if a == b else breaks).append(row)
        if k == 32:
            lab = ('observational_only_new_registered_candidate_twentythird_tail_k32_z30_slice_supply_even_form_7of7_candidate_m18spot_S5_item1')
            note = ('REGISTERED candidate (m18spot kit log S5 item #1, commit b8146415): hold {0} U {12..31}, break 0v2 at s=32, UNIFORM 2v1 for ALL s in {33..66}; even-z supply form measured chain k=20/22/24/26/28/30 (6/6) + k=32 closed-form here = 7/7 candidate')
            secname = 'twentythird_tail_supply_identity_precalc'
        elif k == 33:
            lab = ('observational_only_new_registration_twentyfourth_tail_k33_z33_slice_supply_odd_form_8of8_candidate')
            note = ('NEW registration made by this file BEFORE the run (both components predeclared): hold {0} U {12..33}, UNIFORM 0v1 for ALL s in {34..67}; odd-z supply form chain k=19/21/23/25/27/29/31 (7/7 measured) + k=33 closed-form here = 8/8 candidate; z=33 slice supply datum for the future z=33 declaration lane')
            secname = 'twentyfourth_tail_supply_identity_precalc'
        elif k == 31:
            lab = ('observational_only_closed_form_recheck_supply_identity_k0832')
            note = ('NEW by the m18spot kit (22nd tail): hold {0} U {12..31}, 0v1 break at s=32, UNIFORM 0v1 for ALL s >= 33 (odd-z supply form 7/7); rechecked here extended by one point')
            secname = f'{ORDINAL[k]}_tail_supply_identity_recheck'
        else:
            lab = ('observational_only_closed_form_recheck_supply_identity_k0832')
            if k % 2 == 0:
                shape = 'even-k identity: hold {0} U {12..k-1}, 0v2 break at s=k, UNIFORM 2v1 for all s >= k+1'
            else:
                shape = 'odd-k identity: hold {0} U {12..k}, UNIFORM 0v1 for all s >= k+1'
            note = ('published constant recheck (published by the series kits z20f14/z21f15/z22f16/z23f17/z24f18/m18spot): ' + shape)
            secname = f'{ORDINAL[k]}_tail_supply_identity_recheck'
        out.append({'section': secname,
                    'label': lab,
                    'k': k, 'ordinal': ORDINAL[k],
                    'identity': f'v(s,{k+1},{k+1}) =? v(s,{k},{k+1})',
                    's_domain': '{0} U {12..67}',
                    'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                    'published_anchor': note,
                    'hold_rows': holds, 'break_rows': breaks})
    # (h) z=26 cross-slice handoff (m18spot S5 item #3), four first-ever
    #     z=26 engine touches with option tables frozen before the run.
    h1 = H(44, tuple(sorted((17, 18), reverse=True)), 26)
    h2 = H(43, tuple(sorted((16, 17), reverse=True)), 26)
    h3 = H(45, (18, 18), 26)
    h4 = H(44, (17, 17), 26)
    out.append({'section': 'z26_crossslice_handoff',
                'label': 'm18spot_S5_item3_base_spot_blind_picks_first_ever_z26_engine_touches',
                'spots': [
                    {'id': 'h1', 'X': [17, 18], 'R': 44, 'z': 26,
                     'value': h1, 'collapse': v(35, 26, 44),
                     'role': 'm17-row z=26 first co-token member; candidate collapse-conform 0 = v(35,26,44)',
                     'match': h1 == v(35, 26, 44)},
                    {'id': 'h2', 'X': [16, 17], 'R': 43, 'z': 26,
                     'value': h2, 'collapse': v(33, 26, 43),
                     'role': 'm16-row z=26 first co-token member; candidate collapse-conform 1 = v(33,26,43)',
                     'match': h2 == v(33, 26, 43)},
                    {'id': 'h3', 'X': [18, 18], 'R': 45, 'z': 26,
                     'value': h3, 'collapse': v(36, 26, 45),
                     'role': 'm=18 base-spot z-sequence 12th on-line member; frozen option table {B-child = h1 (in-kit first-contact premise disclosed), C-child 1^H(44;(18,18);25)=1^1=0 PUBLISHED}; candidate mex{0,0}=1 = collapse v(36,26,45) CONFORMING iff h1 conforms 0',
                     'match': h3 == v(36, 26, 45)},
                    {'id': 'h4', 'X': [17, 17], 'R': 44, 'z': 26,
                     'value': h4, 'collapse': v(34, 26, 44),
                     'role': 'm=17 base-spot z-sequence 5th on-line member; frozen option table {B-child = h2 (in-kit first-contact premise disclosed), C-child 1^H(43;(17,17);25)=1^0=1 PUBLISHED}; candidate mex{1,1}=0 = collapse v(34,26,44) CONFORMING iff h2 conforms 1',
                     'match': h4 == v(34, 26, 44)}],
                'published_anchor': 'm=18 on-line z-sequence z in {16..25} = 0,1,0,1,0,1,0,1,1,1 (published incl. both z=25 readings by the m18spot kit); the z=26 candidates here are structural continuations registered before any z=26 lattice exists'})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
