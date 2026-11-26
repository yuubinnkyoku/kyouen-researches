#!/usr/bin/env python3
"""
explore_z24f18: FROZEN PRE-DECLARATION census for the z=24 FLOOR-18
(z-6, SUB-CRITICAL floor) cell ladder — the TENTH edition of the
floor-(z-6) series (z=15 K1321, z=16 `059c531e`, z=17 `82f98ef4`,
z=18 `0bb7e440`, z=19 `5b2275bc`, z=20 `2d8cea40`, z=21 `5b01e14c`,
z=22 `fb215b76`/`daa9a805`, z=23 `9577fadc`) and the FIFTH EVEN
edition of the 11-entry lattice prediction. NO K slot is claimed by
this file; the constants below were frozen into this docstring
BEFORE the first run of this file and the file has not been edited
after any of its runs.

The architectural target is the REGISTERED PREDICTION carried by
the published even-edition chain and restated by the published
z21-floor15 kit log section 5 (commit `5b01e14c`) and the
z23-floor17 kit log section 5 (commit `9577fadc`): "z=24 floor-18
(even, the registered 11-entry lattice prediction at positions
{18,20,22,24})" — plus the registered TWENTY-FIRST-tail handoff of
the z23-floor17 kit log: "The TWENTY-FIRST-tail (k=30, even form,
v(s,31,31) vs v(s,30,31)) is the natural next pre-computation
(z=30 supply; even-form candidate: hold {0} U {12..29}, 0v2@30,
UNIFORM 2v1 s >= 31; both components derivable from the current
closed-form data)". The counter-probe required before claiming was
performed at kit-build time: NO T-Z24 declaration exists on main,
no z24-min19 census kit exists (filename:explore_z24 returns
nothing), so this kit is a pure pre-declaration exploration of the
unsurveyed z=24 lattice — the natural pre-cursor of the future
T-Z24 lane, in the exact role the published z23-min18 kit played
for K1344.

HONEST DISCLOSURE (drafting discipline, before the freeze): the
hand derivations below were written in-session from published
PROVED facts only (the PROVED T-Z23/K1344 z=23 floor-18 ladder row
constants at s=18 — including the three PROVED class values C DOWN
1v2 => 1, B DOWN 0v1 => 0, A UP 2v0 => 2 at s=18 — the K1264 stair
equality, the K0832 closed form) and the child-position INPUT
LITERALS were cross-checked against a drafting scratch engine
evaluation BEFORE this file was frozen (the K1344-D6 discipline
applied: derivation -> engine cross-check of the input literals ->
freeze; the scratch machine itself is NOT published and evaluates
NONE of the declared outcome values). The file itself ran for the
first time only after the freeze. The genuinely BLIND
pre-declarations of this file (no engine evaluation before the
freeze) are: the s=18 head-row OUTCOME values (the mex results),
the registered 11-entry lattice block s in {19..35} (read at
positions {20,22,24}; no same-z critical census exists to compare
against — these are value-exact blind candidates carried by the
published even-chain registered 4/4), the BLIND sub-floor block
s in {36..49}, the multivalue census, the strip/row/base-spot/
below-band measurements (b)-(f) and every measured COUNT (shape
counts are measured, not predeclared, per series convention). The
tail-identity constants of section (g) are pure published K0832
closed-form evaluations (engine-free).

Scope (this file measures and reports; it proves nothing by
itself):
  (a) cell census: for each j in 1..17 the floor-18 cell
      Cell_j(s) := H(j+25; {j} U Y; 24), Y tokens >= 18, s = sum(Y)
      in {0} U {18..49}, arity(Y) in 0..4 (0 only at s=0), swept
      EXHAUSTIVELY against the published raw engine (K1138
      recursion, embedded block byte-identical to the K1282..K1344
      chain, pin bd5f22e4...). Reported per cell: deviants from the
      Sigma-collapse v(s+j,24,j+25) (K0832 closed form) and any
      multivalue (decomposition-dependence) rows. The 17 rungs are
      labeled F..A11 ALIGNED with the rung-count convention of the
      published z=23 floor-17 kit; no rank beyond A11 is swept (a
      j=18 rung is NOT paper-derivable at s=18: both its B-hand
      children land on (42;(17,18);24) = the OPEN z=24 m=17-row
      position, covered by no published record at the time of the
      freeze — that rank belongs to a future lane).
      PREDECLARED CANDIDATES (frozen before the first run):
      (i) THE s=18 ROW — the floor-necessity test and the
          registered EVEN HEAD TRIO. Single shape (j,18) at every
          j. Full 17-point profile derived BY HAND from four
          published inputs: (1) the C-hand child of Cell_j(18) is
          exactly the published PROVED T-Z23/K1344 z=23 floor-18
          ladder position H(j+24;{j,18};23) — the PROVED row
          constants at s=18: F..A11 conform except the three PROVED
          class cells C23f18 {s=18 DOWN 1v2 => value 1},
          B23f18 {s=18 DOWN 0v1 => value 0}, A23f18 {s=18 UP 2v0
          => value 2}; (2) the published K1264 stair equality
          covers every 18->17 B-hand child (j,17) at R=j+24 EXACTLY
          (min=j) for j in 1..17; (3) the small-token B-child is the
          in-kit cascade Cell_{j-1}(18), R=j+24 = 24+(j-1)+1 one
          ABOVE the stair, and the j=1 removal child is the single
          token H(25;(18,);25) = v(18,25,25) = 0 (stair
          R=25 <= 25+18); (4) all inputs are PROVED/published —
          NO observational dependency enters the head derivation
          this time (the z=23 lattice is fully PROVED by K1344).
          Derived profile (every option set below was written
          BEFORE the first run; input literals engine-cross-checked
          at drafting; b_j = [0,1,0,1,0,1,2,0,1,0,1,0,1,0,1,0,1],
          c_j = [1,0,1,0,1,0,2,1,0,1,0,1,0,1,0,1,0],
          d_j = [1,0,1,0,1,2,0,1,0,1,0,1,0,1,0,1,0]):
          j=1  F conform v(19,24,26)=1 (options {stair v(18,24,25)=0,
               removal v(18,25,25)=0, 1^C-hand v(19,23,25)=1^1=0} ->
               mex 1 = collapse);
          j=2  G conform v(20,24,27)=0 (options {stair v(19,24,26)=1,
               Cell_1=1, 1^v(20,23,26)=1^0=1} -> mex 0 = collapse);
          j=3  E conform v(21,24,28)=1 (options {stair v(20,24,27)=0,
               Cell_2=0, 1^v(21,23,27)=1^1=0} -> mex 1 = collapse);
          j=4  D conform v(22,24,29)=0 (options {stair v(21,24,28)=1,
               Cell_3=1, 1^v(22,23,28)=1^0=1} -> mex 0 = collapse);
          j=5  C conform v(23,24,30)=1 (options {stair v(22,24,29)=0,
               Cell_4=0, 1^C23f18-class=1^1=0} -> mex 1 = collapse);
          j=6  B DOWN 0v2 v(24,24,31)=2 (options {stair v(23,24,30)=1,
               Cell_5=1, 1^B23f18-class=1^0=1} -> mex 0 != collapse
               2) — THE REGISTERED HEAD TRIO ENTRY 1;
          j=7  A UP 1v0 v(25,24,32)=0 (options {stair v(24,24,31)=2,
               Cell_6=0, 1^A23f18-class=1^2=3} -> mex 1 != collapse
               0) — THE REGISTERED HEAD TRIO ENTRY 2;
          j=8  A2 UP 2v1 v(26,24,33)=1 (options {stair v(25,24,32)=0,
               Cell_7=1, 1^v(26,23,32)=1^1=0} -> mex 2 != collapse
               1) — THE REGISTERED HEAD TRIO ENTRY 3;
          j=9..17 A3..A11 conform (the cascade re-locks after the
               trio: option sets {stair, Cell_{j-1}, 1^c_j} =
               {1,1,1} -> mex 0 for odd j, {0,0,0} -> mex 1 for
               even j (j=9..17 c_j alternates 0/1 in step), the
               collapse v(j+18,24,j+25) alternating in step; j=17
               closes conform v(35,24,42)=0).
          THE REGISTERED CLAIM CARRIED BY THIS ROW: the even
          sub-critical head trio {B DOWN 0v2, A UP 1v0, A2 UP 2v1}
          at s=z-6=18 extends its published value-exact even chain
          (z=16 `059c531e`, z=18 `0bb7e440`, z=20 `2d8cea40`, z=22
          `fb215b76`) to its candidate 5/5, the mirror of the odd
          head-empty rule 5/5 (z=15/17/19/21/23). Consequence IF
          CONFIRMED: the critical floor 19 = z-5 remains
          NECESSARY at z=24 for the full Sigma-collapse (the trio's
          DOWN-cells and the A-cell exotic option set {0,2,3} ->
          mex 1 witness the head-only failure), and the even/odd
          head dichotomy (trio vs empty) is now carried by ten
          consecutive editions.
      (ii) s in {19..35}: THE REGISTERED 11-ENTRY LATTICE read at
           positions {20,22,24} — value-exact BLIND candidates
           (scaled +2 from the measured value-exact even chain
           z=16/18/20/22, 4/4 at positions {z-4, z-2, z}):
           at s=20 (z-4): C(j=5) UP 1v0 (vs collapse v(25,24,30)=0),
               B(j=6) UP 2v1 (vs v(26,24,31)=1), D(j=4) DOWN 0v2
               (vs v(24,24,29)=2);
           at s=22 (z-2): E(j=3) UP 1v0 (vs v(25,24,28)=0),
               D(j=4) UP 2v1 (vs v(26,24,29)=1), G(j=2) DOWN 0v2
               (vs v(24,24,27)=2);
           at s=24 (=z): F(j=1) UP 1v0 (vs v(25,24,26)=0),
               G(j=2) UP 2v1 (vs v(26,24,27)=1);
           and NO other deviant row in {19..35} (the even chain
           shows clean single-entry rows outside the 11 positions;
           the odd editions' F persistent UP 2v0 tail does NOT
           continue in even editions — the even F cell carries a
           single UP 1v0 at s=z only), 0 multivalue.
      (iii) s in {36..49} (the BLIND sub-floor block: 18-token
            components enter the lattice for the first time —
            (18,18) at s=36, then (18,k) from s=37): candidates NO
            multivalue rows and NO new deviant classes (the
            published z21-f15 {30..46}, z22-f16 {32..47} and
            z23-f17 {34..48} analogs were empty of both).
      (iv) all cells s-only; multivalue rows 0.
  (b) tail spots: s in {50..57}, single-token shape Y=(s,), all 17
      cells — candidate 136/136 MATCH (the EVEN-edition signature:
      the published z22-f16 tail spots were 120/120 match — the
      odd editions' F 8/8 mismatch signature does NOT appear at
      even z). BLIND (no even tail-spot row was published at more
      than one edition before).
  (c) strip sweep m in {18..23} at R=m+25: NO T-Z24 exists, so
      every segment is a NEW in-band z=24 measurement (z*(m) =
      2m-2+(m mod 2) > 24 for all m in {18..23}); m=18 is the
      head-floor row segment (the even-chain convention: the m=z-6
      strip segment, like the published z20-f14 m=14 and z22-f16
      m=16 segments), m in {19..23} the would-be T-Z24 claim
      positions. Candidates 0 violations for every segment (the
      strip family has never produced a violation in any published
      kit); measured counts recorded whatever they are.
  (d) IN-BAND m=18-row z=24 record at R=43, x0 published
      residual-band style (all parts >= 18, co-token 18 allowed,
      arity <= 3 TOTAL, S in {18..56}): the FIRST-EVER z=24 m=18
      row record (in-band, z*(18)=34 > 24; the frontier target of
      the future T-Z24 lane). Candidate 0 separations. PLUS the
      arity<=4 co-token extension sweep.
  (d2) IN-BAND m=17-row z=24 record at R=42, S in {17..55}: the
      SECOND entry of the future T-Z22 declaration residual band
      m=17 z in {23..32} (first: the published z23-min18 kit
      32/0, rechecked by the z23-f17 kit). Candidate 0
      separations.
  (d3) IN-BAND m=16-row z=24 record at R=41, S in {16..54}: the
      z=24 entry of the future T-Z21 residual band m=16 z in
      {22..29} (published entries: 40/0 at z=22, 40/0 at z=23).
  (d4) IN-BAND m=15-row z=24 record at R=40, S in {15..53}: the
      K1335 (T-Z20) published residual band m=15 z in {21..28}
      z=24 entry (published 50/0 at z=21/22/23).
  (d5) IN-BAND m=14-row z=24 record at R=39, S in {14..52}: the
      K1330 residual band m=14 z in {20..25} z=24 entry (62/0 at
      z=21/22/23).
  (d6) IN-BAND m=13-row z=24 record at R=38, S in {13..51}: the
      K1328 residual band m=13 z in {19..24} z=24 entry (76/0 at
      z=19..23); z*(13)=25 > 24, in-band by one point — the
      CLOSEST-to-frontier row record of any published kit.
  (e) strip spots m in {24..27} at R=m+25, X in
      {(m,m+1),(m,m+2),(m,m,m+1)}: NEW z=24 spots (candidate 12/12
      match per the strip family), PLUS the NEW m=18 BASE SPOT
      H(43;(18,18);24) vs v(36,24,43)=1: paper-derived candidate
      value 1, CONFORMING (derivation disclosed here before the
      first run: both B-hand children land at (42;(17,18);24) =
      the m=17-row z=24 record position — the SINGLE OBSERVATIONAL
      DEPENDENCY, disclosed: candidate value v(35,24,42)=0 IF that
      row conforms as every published m=17..m=13 row has; the
      C-child is 1^H(42;(18,18);23) = 1^v(36,23,42) = 1^1 = 0 by
      the PROVED T-Z23 base m=18; the options are {0, 0} -> mex 1
      = the collapse v(36,24,43)=1). Never measured by any
      published kit (the published z23-f17 kit measured the m=17
      base spot at z=23 = 0; the published z23-min18 kit measured
      H(42;(18,18);23)=1 at z=23). The m=18 base-spot z-sequence
      so far: z in {16..23} all CONFORMING (0,1,0,1,0,1,0,1);
      z=24: 1 (candidate here) — the first even-z edition measured
      at the m=18 row.
  (f) below-band bottom-rung child census: the j=1 cell's B-move
      removal child is the below-band position H(25;Y;25) with
      min(Y) >= 18 (child slice z'=25, floor 18 = z'-7), swept over
      s in {0} U {18..49}, arity 0..4, against v(s,25,25). This is
      the EIGHTH z'-7 empty-datum candidate of the series (the
      seven published below-band full collapses were swept at
      z'=17/19/20/21/22/23/24): candidate 0 deviants, 0 multivalue
      rows. The published K1264 stair applicability
      R=25 <= 25+min(Y) suggests the collapse is a stair
      consequence at ANY floor; recorded here as a machine
      corroboration of that PROVED lemma's instance; the
      generalization belongs to a declaration lane.
  (g) TAIL SUPPLY PRE-COMPUTATIONS (pure published K0832 closed
      form, NO engine recursion), all over the EXTENDED domain
      s in {0} U {12..64} (each extended by one point from the
      published z23-floor17 kit domain {0} U {12..63}):
      (g1) FIFTEENTH-tail identity RECHECK v(s,25,25) vs
          v(s,24,25) — THIS slice's own F-cell supply datum
          (z=24): candidate hold {0} U {12..23}, 0v2 break at
          s=24, uniformly 2v1 for all s in {25..64} (even-z
          supply form).
      (g2) SIXTEENTH-tail identity RECHECK v(s,26,26) vs
          v(s,25,26): candidate hold {0} U {12..25}, uniform 0v1
          break for all s in {26..64} (odd-z supply form).
      (g3) SEVENTEENTH-tail identity RECHECK v(s,27,27) vs
          v(s,26,27): candidate hold {0} U {12..25}, 0v2 break at
          s=26, uniformly 2v1 for all s in {27..64}.
      (g4) EIGHTEENTH-tail identity RECHECK v(s,28,28) vs
          v(s,27,28): candidate hold {0} U {12..27}, uniform 0v1
          break for all s in {28..64}.
      (g5) NINETEENTH-tail identity RECHECK v(s,29,29) vs
          v(s,28,29): candidate hold {0} U {12..27}, 0v2 break at
          s=28, uniformly 2v1 for all s in {29..64} (published NEW
          by the z23-floor17 kit; rechecked here extended).
      (g6) TWENTIETH-tail identity RECHECK v(s,30,30) vs
          v(s,29,30): candidate hold {0} U {12..29}, uniform 0v1
          break for all s in {30..64} (published NEW by the
          z23-floor17 kit; rechecked here extended).
      (g7) NEW TWENTY-FIRST-tail PRE-COMPUTATION v(s,31,31) vs
          v(s,30,31) — the z=30-slice supply datum (registered as
          the natural next pre-computation by the published
          z23-floor17 kit log section 5 handoff): BOTH components
          predeclared. The even-k identity shape (published even
          constants k=20/22/24/26/28: hold {0} U {12..k-2}...,
          0v2@k, UNIFORM 2v1 s >= k+1, measured 5/5) gives the
          candidate: hold on {0} U {12..29}, break START at s=30
          (=k), break shape 0v2 at s=30 then UNIFORM 2v1 for ALL
          s in {31..64}; z=30-supply decides whether the even-z
          supply form graduates to 6/6; constants recorded
          whatever they are.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z24f18.out).
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
    """sweep cell_j over s in {0} U {18..smax}; returns (dev, multi, total)"""
    R = j + 25
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(18, smax + 1)):
        ys = [()] if s == 0 else parts(s, 18, 4)
        vals = {}
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            h = H(R, X, 24)
            vals.setdefault(h, []).append(y)
            total += 1
        if len(vals) > 1:
            multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s + j, 24, R)
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


def main():
    out = []
    out.append({'section': 'engine_gate', 'engine_sha': sha, 'pin': PIN,
                'gate': 'PASS'})
    cells = {}
    names = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
             'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11']
    for j in range(1, 18):
        name = names[j - 1]
        dev, multi, total = cell_sweep(j, 49)
        cells[f'cell{j}_{name}24f18'] = {
            'z': 24, 'min': j, 'R': j + 25, 'floor': 18,
            's_domain': '{0} U {18..49}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}24f18',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 18):
        nm = names[j - 1]
        for s in range(50, 58):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 25, X, 24)
            exp = v(s + j, 24, j + 25)
            tail.append({'cell': f'{nm}24f18', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s50_57', 'rows': tail})
    # (c) strip sweep m in 18..23 at R=m+25: NO T-Z24 exists — every
    #     segment is a NEW in-band z=24 measurement (candidate 0
    #     violations per the strip family).
    sv = []
    viol = []
    cnt = 0
    for m in range(18, 24):
        H.cache_clear()
        for S in range(m, m + 40):
            for X in parts(max(S - m, 0), m, 3):
                XX = tuple(sorted((m,) + X, reverse=True))
                if sum(XX) != S:
                    continue
                hv = H(m + 25, XX, 24)
                ev = v(S, 24, m + 25)
                cnt += 1
                if hv != ev:
                    viol.append({'m': m, 'X': list(XX), 'S': S,
                                 'value': hv, 'collapse': ev})
        sv.append({'m': m, 'cumulative_shapes': cnt,
                   'cumulative_violations': len(viol)})
    out.append({'section': 'strip_z24_m18_23', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) IN-BAND m=18-row z=24 record — FIRST-EVER, frontier target of
    #     the future T-Z24 lane.
    out.append(row_record_x0(
        'inband_m18_z24_row_record',
        'first_ever_z24_m18_row_record_in_band_zstar18_34_gt_24_future_tz24_lane_target',
        {'co_token_18_allowed': True,
         'residual_band': 'no band published (the future T-Z24 declaration residual band m=18 z in {25..33} is unborn; frontier z*(18)=34 per the K1268 formula z*(m)=2m-2+(m mod 2)); candidate 0 separations per the strip family',
         's_domain': '{18..56}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        43, 24, 18, 18, 56))
    out.append(row_record(
        'inband_m18_z24_row_record_ext_arity4',
        'arity_le4_extension_cotoken_style',
        {'co_token_18_allowed': True,
         's_domain': '{18..56}', 'arity_max': 4},
        43, 24, 18, 18, 56, 18))
    # (d2) IN-BAND m=17-row z=24 record: future T-Z22 band second entry.
    out.append(row_record_x0(
        'inband_m17_z24_row_record',
        'future_tz22_residual_band_m17_z24_second_entry_after_published_z23_32_shapes',
        {'co_token_17_allowed': True,
         'residual_band': 'future T-Z22 declaration residual band m=17 z in {23..32} (frontier z*(17)=33); published z=23 entry: 32 shapes 0 separations (z23-min18 kit, rechecked by the z23-floor17 kit); candidate 0 separations here',
         's_domain': '{17..55}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        42, 24, 17, 17, 55))
    # (d3) IN-BAND m=16-row z=24 record.
    out.append(row_record_x0(
        'inband_m16_z24_row_record',
        'future_tz21_residual_band_m16_z24_entry',
        {'co_token_16_allowed': True,
         'residual_band': 'future T-Z21 residual band m=16 z in {22..29}; published entries: z=22 40/0, z=23 40/0; candidate 0 separations here',
         's_domain': '{16..54}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        41, 24, 16, 16, 54))
    # (d4) IN-BAND m=15-row z=24 record.
    out.append(row_record_x0(
        'inband_m15_z24_row_record',
        'k1335_residual_band_m15_z24_entry',
        {'co_token_15_allowed': True,
         'residual_band': 'K1335 (T-Z20) published residual band m=15 z in {21..28}; published entries: 50 shapes 0 separations at z=21/22/23; candidate 0 separations here',
         's_domain': '{15..53}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        40, 24, 15, 15, 53))
    # (d5) IN-BAND m=14-row z=24 record.
    out.append(row_record_x0(
        'inband_m14_z24_row_record',
        'k1330_residual_band_m14_z24_entry',
        {'co_token_14_allowed': True,
         'residual_band': 'K1330 published m=14 z in {20..25}; published entries: 62 shapes 0 separations at z=21/22/23; candidate 0 separations here',
         's_domain': '{14..52}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        39, 24, 14, 14, 52))
    # (d6) IN-BAND m=13-row z=24 record (in-band by one point, z*(13)=25).
    out.append(row_record_x0(
        'inband_m13_z24_row_record',
        'k1328_residual_band_m13_z24_entry_closest_to_frontier_zstar13_25',
        {'co_token_13_allowed': True,
         'residual_band': 'K1328 published m=13 z in {19..24}; published entries: 76 shapes 0 separations at z=19..23; z*(13)=25 > 24 by one point, the closest-to-frontier row record of any published kit; candidate 0 separations here',
         's_domain': '{13..51}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        38, 24, 13, 13, 51))
    # (e) strip spots m in 24..27 at R=m+25 (NEW z=24 spots)
    spots = []
    for m in range(24, 28):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 25, X, 24)
            ev = v(S, 24, m + 25)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    out.append({'section': 'strip_spots_m24_27', 'rows': spots})
    # NEW m=18 base spot (never measured by any published kit;
    # paper-derived candidate 1 CONFORMING, disclosed in the docstring)
    w = H(43, (18, 18), 24)
    wv = v(36, 24, 43)
    out.append({'section': 'm18_base_spot', 'X': [18, 18], 'R': 43,
                'z': 24, 'value': w, 'collapse_single': wv,
                'match': w == wv,
                'published_probe_crossref': 'NEW measurement: no published kit measured H(43;(18,18);24) (the published z23-min18 kit measured the z=23 spot H(42;(18,18);23)=1; the published z23-floor17 kit measured the z=23 m=17 spot H(41;(17,17);23)=0); paper-derived candidate value 1 = v(36,24,43) conforming, derivation disclosed in this file docstring before the first run (B-children on the z=24 m=17-row record entry — the single disclosed observational dependency, premised conforming — C-child on the PROVED T-Z23 base m=18)'})
    # (f) below-band bottom-rung child census: H(25;Y;25) vs v(s,25,25)
    #     with Y >= 18 (EIGHTH z'-7 empty-datum candidate, floor
    #     z'-7 at z'=25)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(18, 50)):
        ys = [()] if s == 0 else parts(s, 18, 4)
        vals = {}
        for y in ys:
            h = H(25, y, 25)
            vals.setdefault(h, []).append(y)
            bb_total += 1
        if len(vals) > 1:
            bb_multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s, 25, 25)
            if val != exp:
                bb_dev.append({'s': s, 'value': val, 'collapse': exp,
                               'direction': 'UP' if val > exp else 'DOWN',
                               'shapes': len(vals[val])})
    out.append({'section': 'belowband_j1_child_H25_25',
                'label': 'observational_only_eighth_zprime7_datum_belowband_supply_source_at_z24_floor18',
                'R': 25, 'z': 25, 'floor': 18,
                's_domain': '{0} U {18..49}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (g1) FIFTEENTH-TAIL SUPPLY IDENTITY RECHECK (pure K0832)
    holds = []
    breaks = []
    for s in [0] + list(range(12, 65)):
        a = v(s, 25, 25)
        b = v(s, 24, 25)
        row = {'s': s, 'v_25_25': a, 'v_24_25': b, 'equal': a == b}
        (holds if a == b else breaks).append(row)
    out.append({'section': 'fifteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,25,25) =? v(s,24,25)',
                's_domain': '{0} U {12..64}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z21-min16 + z20-floor14 + z21-floor15 + z23-min18 + z23-floor17 kits: holds {0} U {12..23}, 0v2 break at s=24, then uniformly 2v1 for all s>=25 (this slice own F-supply datum at z=24); rechecked and extended here over s in {0} U {12..64}',
                'hold_rows': holds, 'break_rows': breaks})
    # (g2) SIXTEENTH-TAIL SUPPLY IDENTITY RECHECK
    t_holds = []
    t_breaks = []
    for s in [0] + list(range(12, 65)):
        a = v(s, 26, 26)
        b = v(s, 25, 26)
        row = {'s': s, 'v_26_26': a, 'v_25_26': b, 'equal': a == b}
        (t_holds if a == b else t_breaks).append(row)
    out.append({'section': 'sixteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,26,26) =? v(s,25,26)',
                's_domain': '{0} U {12..64}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'NEW by the z22-floor16 kit, predeclared and confirmed by the z23-min18 precalc and rechecked by the z21-floor15 / z23-floor17 kits: holds {0} U {12..25}, uniform 0v1 break for all s>=26 (odd-z supply form); rechecked and extended here',
                'hold_rows': t_holds, 'break_rows': t_breaks})
    # (g3) SEVENTEENTH-TAIL SUPPLY IDENTITY RECHECK
    n_holds = []
    n_breaks = []
    for s in [0] + list(range(12, 65)):
        a = v(s, 27, 27)
        b = v(s, 26, 27)
        row = {'s': s, 'v_27_27': a, 'v_26_27': b, 'equal': a == b}
        (n_holds if a == b else n_breaks).append(row)
    out.append({'section': 'seventeenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,27,27) =? v(s,26,27)',
                's_domain': '{0} U {12..64}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'NEW by the z20-floor14 kit, rechecked by z21-floor15 / z23-floor17 kits: hold {0} U {12..25}, 0v2 break at s=26, UNIFORM 2v1 for ALL s>=27 (even-z supply form); rechecked and extended here',
                'hold_rows': n_holds, 'break_rows': n_breaks})
    # (g4) EIGHTEENTH-TAIL SUPPLY IDENTITY RECHECK
    e_holds = []
    e_breaks = []
    for s in [0] + list(range(12, 65)):
        a = v(s, 28, 28)
        b = v(s, 27, 28)
        row = {'s': s, 'v_28_28': a, 'v_27_28': b, 'equal': a == b}
        (e_holds if a == b else e_breaks).append(row)
    out.append({'section': 'eighteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,28,28) =? v(s,27,28)',
                's_domain': '{0} U {12..64}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'NEW by the z21-floor15 kit, rechecked by the z23-floor17 kit: hold {0} U {12..27}, UNIFORM 0v1 for ALL s>=28 (odd-z supply form 5/5; the z=27 slice supply datum); rechecked and extended here',
                'hold_rows': e_holds, 'break_rows': e_breaks})
    # (g5) NINETEENTH-TAIL SUPPLY IDENTITY RECHECK
    n19_holds = []
    n19_breaks = []
    for s in [0] + list(range(12, 65)):
        a = v(s, 29, 29)
        b = v(s, 28, 29)
        row = {'s': s, 'v_29_29': a, 'v_28_29': b, 'equal': a == b}
        (n19_holds if a == b else n19_breaks).append(row)
    out.append({'section': 'nineteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,29,29) =? v(s,28,29)',
                's_domain': '{0} U {12..64}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'NEW by the z23-floor17 kit (commit 9577fadc): hold {0} U {12..27}, 0v2 break at s=28, UNIFORM 2v1 for ALL s>=29 (even-z supply form graduated 5/5; the z=28 slice supply datum); rechecked and extended here',
                'hold_rows': n19_holds, 'break_rows': n19_breaks})
    # (g6) TWENTIETH-TAIL SUPPLY IDENTITY RECHECK
    t20_holds = []
    t20_breaks = []
    for s in [0] + list(range(12, 65)):
        a = v(s, 30, 30)
        b = v(s, 29, 30)
        row = {'s': s, 'v_30_30': a, 'v_29_30': b, 'equal': a == b}
        (t20_holds if a == b else t20_breaks).append(row)
    out.append({'section': 'twentieth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,30,30) =? v(s,29,30)',
                's_domain': '{0} U {12..64}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'NEW by the z23-floor17 kit (commit 9577fadc): hold {0} U {12..29}, UNIFORM 0v1 for ALL s>=30 (odd-z supply form 6/6 candidate confirmed; the z=29 slice supply datum); rechecked and extended here',
                'hold_rows': t20_holds, 'break_rows': t20_breaks})
    # (g7) TWENTY-FIRST-TAIL SUPPLY PRE-COMPUTATION (NEW, pure K0832)
    h21 = []
    b21 = []
    for s in [0] + list(range(12, 65)):
        a = v(s, 31, 31)
        b = v(s, 30, 31)
        row = {'s': s, 'v_31_31': a, 'v_30_31': b, 'equal': a == b}
        (h21 if a == b else b21).append(row)
    out.append({'section': 'twentyfirst_tail_supply_identity_precalc',
                'label': 'observational_only_new_closed_form_precalc_z30_slice_supply_k0832',
                'identity': 'v(s,31,31) =? v(s,30,31)',
                's_domain': '{0} U {12..64}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'predeclared_candidate': 'BOTH components predeclared (registered as the natural next pre-computation by the published z23-floor17 kit log section 5 handoff): even-k identity shape (published even constants k=20/22/24/26/28 measured 5/5: hold {0} U {12..k-2} pattern, 0v2@k, UNIFORM 2v1 s>=k+1) gives the candidate: hold on {0} U {12..29}, break START at s=30 (=k), break shape 0v2 at s=30 then UNIFORM 2v1 for ALL s in {31..64}; z=30-supply decides whether the even-z supply form graduates to 6/6; constants recorded whatever they are',
                'hold_rows': h21, 'break_rows': b21})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
