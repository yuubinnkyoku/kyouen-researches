#!/usr/bin/env python3
"""
explore_z23f17: FROZEN PRE-DECLARATION census for the z=23 FLOOR-17
(z-6, SUB-CRITICAL floor) cell ladder — the NINTH edition of the
floor-(z-6) series (z=15 K1321, z=16 `059c531e`, z=17 `82f98ef4`,
z=18 `0bb7e440`, z=19 `5b2275bc`, z=20 `2d8cea40`, z=21
`5b01e14c`, z=22 `fb215b76`/`daa9a805`) and the fifth ODD edition
of the head-empty pattern. NO K slot is claimed by this file; the
constants below were frozen into this docstring BEFORE the first
run of this file and the file has not been edited after any of
its runs.

The architectural target is the REGISTERED PREDICTION of the
published z=21 floor-15 kit log section 5 (commit `5b01e14c`,
2026-11-26, BEFORE the fact): "Next floor-(z-6) series data points:
z=23 floor-17 (odd, the head-empty 5/5 candidate + preservation
of the published T-Z23/K1344 critical lattice)" — plus that log's
registered NINETEENTH-tail handoff: "The NINETEENTH-tail (k=28,
even form, v(s,29,29) vs v(s,28,29)) is the natural next
pre-computation (z=28 supply; even-form candidate: hold {0} U
{12..27}, 0v2@28, UNIFORM 2v1 s >= 29; both components derivable
from the current closed-form data)". This kit executes exactly
those two registrations and adds the TWENTIETH-tail (k=29, odd
form) pre-computation as the natural next of the same family.

HONEST DISCLOSURE (drafting discipline, before the freeze): the
hand derivations below were written in-session from published
PROVED facts only (the K1339/T-Z22 proved z=22 floor-17 cell
ladder, the K1264 stair equality, the K0832 closed form, the
published z23-min18 census records) and the child-position INPUT
LITERALS were cross-checked against a drafting scratch engine
evaluation BEFORE this file was frozen (the K1344-D6 discipline
applied: derivation -> engine cross-check of the input literals ->
freeze; the scratch machine itself is NOT published and evaluates
NONE of the declared outcome values). The file itself ran for the
first time only after the freeze. The genuinely BLIND
pre-declarations of this file (no engine evaluation before the
freeze) are: the s=17 head-row OUTCOME values (the mex results),
the shared-block {18..33} acceptance itself, the BLIND sub-floor
block s in {34..48}, the multivalue census, the strip/row/
base-spot/below-band measurements (b)-(f) and every measured
COUNT (shape counts are measured, not predeclared, per series
convention). The tail-identity constants of section (g) are pure
published K0832 closed-form evaluations (engine-free).

Scope (this file measures and reports; it proves nothing by
itself):
  (a) cell census: for each j in 1..17 the floor-17 cell
      Cell_j(s) := H(j+24; {j} U Y; 23), Y tokens >= 17, s = sum(Y)
      in {0} U {17..48}, arity(Y) in 0..4 (0 only at s=0), swept
      EXHAUSTIVELY against the published raw engine (K1138
      recursion, embedded block byte-identical to the K1282..K1344
      chain, pin bd5f22e4...). Reported per cell: deviants from the
      Sigma-collapse v(s+j,23,j+24) (K0832 closed form) and any
      multivalue (decomposition-dependence) rows. The 17 rungs are
      labeled F..A11 ALIGNED with the published z=23 critical
      ladder (F23f18..A1123f18); no rank beyond A11 is swept (a
      j=18 rung is NOT paper-derivable at s=17: its C-hand child
      (41;{17,18};22) is covered by no published ladder cell nor
      strip claim — that rank belongs to a future lane).
      PREDECLARED CANDIDATES (frozen before the first run):
      (i) THE s=17 ROW — the floor-necessity test and the
          registered EMPTY ODD HEAD. Single shape (j,17) at every
          j. Full 17-point profile derived BY HAND from four
          published inputs: (1) the C-hand child of Cell_j(17) is
          exactly the published PROVED z=22 critical-ladder
          position H(j+23;{j,17};22) (Y-token 17 >= that ladder's
          floor 17) — the PROVED K1339 (T-Z22) cell constants at
          s=17: the whole published z=22 ladder row at s=17
          CONFORMS (F..A10 deviants live at {18,20,22}), for j=17
          the PROVED T-Z22 m=17-row base position H(40;(17,17);22)=
          v(34,22,40)= 0; (2) the published K1264 stair equality
          covers every 17->16 B-hand child (j,16) at R=j+23 EXACTLY
          (min=j) for j in 1..16; (3) the small-token B-child is
          the in-kit cascade Cell_{j-1}(17), R=j+23 = 23+(j-1)+1
          one ABOVE the stair, and the j=1 removal child is the
          single token H(24;(17,);24) = v(17,24,24) = 1 (stair
          R=24 <= 24+17); (4) the sole NON-proved input: for j=17
          both B-hand children land on (40;(16,17);23) = the
          published z=23 m=16-row OBSERVATIONAL record position
          (z23-min18 census kit: 40 shapes 0 separations) =>
          H(40;(16,17);23)= v(33,23,40)=1 — a single
          observational dependency, disclosed, mirroring the
          published z20-f14 / z21-f15 kits' own
          single-observational-dependency pattern at their top
          rungs.
          Derived profile (every option set below was written
          BEFORE the first run; input literals engine-cross-checked
          at drafting; the alternation b_j = j%2, c_j = (j+1)%2,
          d_j = (j+1)%2 was verified rung by rung at drafting):
          j=1  F conform v(18,23,25)=0 (options {stair v(17,23,24)=1,
               removal v(17,24,24)=1, 1^C-hand v(18,22,24)=0 -> 1} ->
               mex 0 = collapse);
          j=2  G conform v(19,23,26)=1 (options {stair v(18,23,25)=0,
               Cell_1=0, 1^v(19,22,25)=1^1=0} -> mex 1 = collapse);
          j=3  E conform v(20,23,27)=0 (options {stair v(19,23,26)=1,
               Cell_2=1, 1^v(20,22,26)=1^0=1} -> mex 0 = collapse);
          j=4  D conform v(21,23,28)=1 (options {stair v(20,23,27)=0,
               Cell_3=0, 1^v(21,22,27)=1^1=0} -> mex 1 = collapse);
          j=5  C conform v(22,23,29)=0 (options {stair v(21,23,28)=1,
               Cell_4=1, 1^v(22,22,28)=1^0=1} -> mex 0 = collapse);
          j=6  B conform v(23,23,30)=1 (options {stair v(22,23,29)=0,
               Cell_5=0, 1^v(23,22,29)=1^1=0} -> mex 1 = collapse);
          j=7  A conform v(24,23,31)=0 (options {stair v(23,23,30)=1,
               Cell_6=1, 1^v(24,22,30)=1^0=1} -> mex 0 = collapse);
          j=8  A2 conform v(25,23,32)=1 (options {stair v(24,23,31)=0,
               Cell_7=0, 1^v(25,22,31)=1^1=0} -> mex 1 = collapse);
          j=9..16 A3..A10 conform (the same two-member alternation
               continues: option sets {stair v(j+16,23,j+23),
               Cell_{j-1}, 1^v(j+17,22,j+23)} = {1,1,1} -> mex 0 for
               odd j, {0,0,0} -> mex 1 for even j, at each step the
               collapse v(j+17,23,j+24) alternates 0/1 in step);
          j=17 A11 conform v(34,23,41)=0 (options {both B-hand
               children (17,16-decremented pair) at (40;.;23) = 1
               (the disclosed observational record value
               v(33,23,40)=1), 1^v(34,22,40)=1^0=1 (the PROVED
               T-Z22 m=17-row base)} -> mex 0 = collapse).
          THE REGISTERED CLAIM CARRIED BY THIS ROW: the odd
          sub-critical head is EMPTY — no deviant class at s=z-6=
          17, the whole row conforming — extending the published
          odd-edition head-empty pattern (z=15 K1321, z=17
          `82f98ef4`, z=19 `5b2275bc`, z=21 `5b01e14c`) to its
          candidate 5/5. Consequence IF CONFIRMED: the critical
          floor 18 = z-5 is NECESSARY at z=23 for the head-only
          part of the cell-ladder Sigma-collapse — the
          floor-necessity of the ODD editions is witnessed at the
          head not by row deviants but by the (proved, published)
          z=22 A-break class birth s=z-5: the A21f18 rebirth class
          {s=18 UP 2v0} survives at floor 17 (s=18 > 17, see
          candidate (ii)) while remaining UNREACHABLE from the
          s=17 row; also 0 multivalue at s=17.
      (ii) s in {18..33}: LATTICE IDENTITY with the published
           floor-18 census (explore_z23f18.out, z23-min18 census
           kit): at every s in {18..33} the Y-shape sets of this
           census coincide exactly with the published f18 shape
           sets (no 17-token component fits below s=34), so every
           shared engine point is byte-identical by determinism;
           the deviant classes are exactly the published f18
           profile — F {22: DOWN 1v2, 23: HOLE (conforming),
           24..48: UP 2v0 persistent tail}, G {22: DOWN 0v1}, E
           {20: DOWN 1v2, 22: UP 2v0}, D {20: DOWN 0v1}, C {18:
           DOWN 1v2, 20: UP 2v0}, B {18: DOWN 0v1}, A {18: UP 2v0
           (the A RANK BREAK REBIRTH class, birth s=z-5=18:
           SURVIVES the floor drop 18->17 — the
           definition-domain-exclusion NON-event 4th consecutive,
           after z=21's A-class and z=22's G/E-class and z=20's
           survival of {16,18})}, A2..A11 collapsed — and NO other
           deviant row in {18..33}.
      (iii) s in {34..48} (the BLIND sub-floor block: 17-token
            components enter the lattice for the first time —
            (17,17) at s=34, then (17,k) from s=35, the block
            closing at s=48): candidates NO multivalue rows and NO
            new deviant classes beyond the f18 classes of (ii)
            (the published z21-f15 {30..46} and z20-f14 {28..45}
            analogs were empty of both).
      (iv) all cells s-only; multivalue rows 0.
  (b) tail spots: s in {49..56}, single-token shape Y=(s,), all 17
      cells — lattice identity with the published f18 tail spots
      (same positions j+24; (j,s) at z=23): candidate F23f17 8/8
      mismatch (the published F23f18 tail spots were 8/8 mismatch),
      all other cells match row-for-row (128/136 match, F the
      sole exception — by determinism, byte-identical positions).
  (c) strip sweep m in {17..22} at R=m+24: m in {18..22} are the
      PROVED T-Z23 claim positions (compliance recheck only; the
      published f18 cumulative profile 28/51/71/90/108, 0
      violations — incrementals 28/23/20/19/18 expected EXACT);
      m=17 is the OPEN m=17 row at z=23 (z*(17)=33 > 23, in-band
      for min=17 by the K1268 band formula z*(m)=2m-2+(m mod 2)):
      co-token-style arity<=4-TOTAL sweep, S in {17..56}: candidate
      0 violations (measured count recorded whatever it is).
  (d) IN-BAND m=17-row z=23 record at R=41, x0 published
      residual-band style (all parts >= 17, co-token 17 allowed,
      arity <= 3 TOTAL, S in {17..55}): CROSS-ARTIFACT RECHECK of
      the published z23-min18 census kit record (32 shapes 0
      separations) AND its continuing role as the CANDIDATE first
      entry of the future T-Z22 declaration residual band m=17
      z in {23..32} (frontier z*(17)=33). PLUS the arity<=4
      co-token extension sweep (published z23-min18 ext: 31 shapes
      0 separations).
  (d2) IN-BAND m=16-row z=23 record at R=40, S in {16..54}:
      cross-artifact recheck of the published z23-min18 record
      (40/0; the z=23 entry of the future T-Z21 residual band
      m=16 z in {22..29}).
  (d3) IN-BAND m=15-row z=23 record at R=39, S in {15..53}:
      cross-artifact recheck (50/0; the K1335-published T-Z20
      residual band m=15 z in {21..28} z=23 entry).
  (d4) IN-BAND m=14-row z=23 record at R=38, S in {14..52}:
      cross-artifact recheck (62/0; K1330 published residual band
      m=14 z in {20..25} z=23 entry).
  (d5) IN-BAND m=13-row z=23 record at R=37, S in {13..51}:
      cross-artifact recheck (76/0; K1328 published m=13 z in
      {19..24} sixth consecutive 76/0 context).
  (e) strip spots m in {23..26} at R=m+24, X in
      {(m,m+1),(m,m+2),(m,m,m+1)}: lattice identity with the
      published f18 strip spots (12/12 match), PLUS the NEW m=17
      BASE SPOT H(41;(17,17);23) vs v(34,23,41): paper-derived
      candidate value 0, CONFORMING (derivation disclosed here
      before the first run: both B-children land at
      (40;(16,17);23), the z=23 m=16-row record position
      (published observational 0 separations => v(33,23,40)=1);
      the C-child is 1^H(40;(17,17);22) = 1^v(34,22,40) = 1 by
      the PROVED T-Z22 m=17-row claim; the options are {1, 1}
      -> mex 0 = the collapse v(34,23,41)=0). Never measured by
      any published kit (the published z23-min18 kit measured the
      m=18 base spot H(42;(18,18);23)=1 only; the published
      z22-min17 kit measured the z=22 spot H(40;(17,17);22)=0
      only). This is the m=17-row base point; its value does not
      claim the row. The m=17 base-spot z-sequence so far: z=22:
      0 (published z22-min17 kit value), z=23: 0 (candidate here)
      — no alternation yet.
  (f) below-band bottom-rung child census: the j=1 cell's B-move
      removal child is the below-band position H(24;Y;24) with
      min(Y) >= 17 (child slice z'=24, floor 17 = z'-7), swept over
      s in {0} U {17..48}, arity 0..4, against v(s,24,24). This is
      the SEVENTH z'-7 empty-datum candidate of the series (the
      six published below-band full collapses were swept at
      z'=17/19/20/21/22/23): candidate 0 deviants, 0 multivalue
      rows. The published K1264 stair applicability
      R=24 <= 24+min(Y) suggests the collapse is a stair
      consequence at ANY floor; recorded here as a machine
      corroboration of that PROVED lemma's instance; the
      generalization belongs to a declaration lane.
  (g) TAIL SUPPLY PRE-COMPUTATIONS (pure published K0832 closed
      form, NO engine recursion), all over the EXTENDED domain
      s in {0} U {12..63} (each extended by one point from the
      published z21-floor15 kit domain {0} U {12..62}):
      (g1) FOURTEENTH-tail identity RECHECK v(s,24,24) vs
          v(s,23,24) — THIS slice's own F-cell supply datum
          (z=23): candidate hold {0} U {12..23}, UNIFORM 0v1
          break for all s in {24..63} (final hold s=23 = the F
          hole; first break s=24 = the tail start; odd-z supply
          form).
      (g2) FIFTEENTH-tail identity RECHECK v(s,25,25) vs
          v(s,24,25): candidate hold {0} U {12..23}, 0v2 break at
          s=24, uniformly 2v1 for all s in {25..63} (even-z supply
          form).
      (g3) SIXTEENTH-tail identity RECHECK v(s,26,26) vs
          v(s,25,26): candidate hold {0} U {12..25}, uniform 0v1
          break for all s in {26..63} (odd-z supply form;
          originally predeclared and confirmed by the z23-min18
          kit's own precalc section).
      (g4) SEVENTEENTH-tail identity RECHECK v(s,27,27) vs
          v(s,26,27): candidate hold {0} U {12..25}, 0v2 break at
          s=26, uniformly 2v1 for all s in {27..63}.
      (g5) EIGHTEENTH-tail identity RECHECK v(s,28,28) vs
          v(s,27,28): candidate hold {0} U {12..27}, uniform 0v1
          break for all s in {28..63} (NEW by the published
          z21-floor15 kit commit `5b01e14c`; rechecked here
          extended by one point).
      (g6) NEW NINETEENTH-tail PRE-COMPUTATION v(s,29,29) vs
          v(s,28,29) — the z=28-slice supply datum (registered as
          the natural next pre-computation by the published
          z21-floor15 kit log section 5 handoff): BOTH components
          predeclared. The even-k identity shape (published even
          constants: k=20 z=20-supply hold {0} U {12..19} 0v2@20
          2v1 s>=21; k=22 z=22-supply hold {0} U {12..21} 0v2@22
          2v1 s>=23; k=24 z=24-supply hold {0} U {12..23} 0v2@24
          2v1 s>=25; k=26 z=26-supply hold {0} U {12..25} 0v2@26
          2v1 s>=27; even form 4/4 measured) gives the candidate:
          hold on {0} U {12..27}, break START at s=28 (=k), break
          shape 0v2 at s=28 then UNIFORM 2v1 for ALL s in
          {29..63}; z=28-supply decides whether the even-z supply
          form graduates to 5/5; constants recorded whatever they
          are. (Registered candidate shape: hold {0} U {12..27},
          0v2@28, UNIFORM 2v1 s in {29..63}.)
      (g7) NEW TWENTIETH-tail PRE-COMPUTATION v(s,30,30) vs
          v(s,29,30) — the z=29-slice supply datum, the natural
          next of the same family (the odd-k candidate shape:
          hold on {0} U {12..29}, break START at s=30 (=k+1),
          break shape UNIFORM 0v1 for ALL s in {30..63}; odd-z
          supply form extends from its published 5/5 measured
          members (k=19/21/23/25/27) to the 6/6 candidate; both
          components derivable from the current closed-form data;
          constants recorded whatever they are).

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z23f17.out).
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
    """sweep cell_j over s in {0} U {17..smax}; returns (dev, multi, total)"""
    R = j + 24
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(17, smax + 1)):
        ys = [()] if s == 0 else parts(s, 17, 4)
        vals = {}
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            h = H(R, X, 23)
            vals.setdefault(h, []).append(y)
            total += 1
        if len(vals) > 1:
            multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s + j, 23, R)
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
        dev, multi, total = cell_sweep(j, 48)
        cells[f'cell{j}_{name}23f17'] = {
            'z': 23, 'min': j, 'R': j + 24, 'floor': 17,
            's_domain': '{0} U {17..48}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}23f17',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 18):
        nm = names[j - 1]
        for s in range(49, 57):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 24, X, 23)
            exp = v(s + j, 23, j + 24)
            tail.append({'cell': f'{nm}23f17', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s49_56', 'rows': tail})
    # (c) strip sweep m in 17..22 at R=m+24: m 18..22 are the PROVED
    #     T-Z23 claim positions (compliance recheck); m=17 is the OPEN
    #     m=17 row at z=23 (candidate 0 violations).
    sv = []
    viol = []
    cnt = 0
    for m in range(17, 23):
        H.cache_clear()
        for S in range(m, m + 40):
            for X in parts(max(S - m, 0), m, 3):
                XX = tuple(sorted((m,) + X, reverse=True))
                if sum(XX) != S:
                    continue
                hv = H(m + 24, XX, 23)
                ev = v(S, 23, m + 24)
                cnt += 1
                if hv != ev:
                    viol.append({'m': m, 'X': list(XX), 'S': S,
                                 'value': hv, 'collapse': ev})
        sv.append({'m': m, 'cumulative_shapes': cnt,
                   'cumulative_violations': len(viol)})
    out.append({'section': 'strip_z23_m17_22', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) IN-BAND m=17-row record at the z=23 m=17 row position
    #     (41; X; 23), all parts >= 17 (co-token 17 allowed), arity <= 3
    #     TOTAL. CROSS-ARTIFACT RECHECK of the published z23-min18 kit
    #     record (32 shapes 0 seps) AND its role as the CANDIDATE first
    #     entry of the future T-Z22 declaration residual band m=17
    #     z in {23..32} (frontier z*(17)=33).
    out.append(row_record_x0(
        'inband_m17_z23_row_record',
        'cross_artifact_recheck_of_published_f18_record_and_future_tz22_residual_band_m17_first_entry',
        {'co_token_17_allowed': True,
         'residual_band': 'future T-Z22 declaration residual band m=17 z in {23..32} (frontier z*(17)=33 per the K1268 formula z*(m)=2m-2+(m mod 2)); published z23-min18 census kit entry: 32 shapes 0 separations (recheck expected shape-for-shape)',
         's_domain': '{17..55}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        41, 23, 17, 17, 55))
    out.append(row_record(
        'inband_m17_z23_row_record_ext_arity4',
        'cross_artifact_recheck_arity_le4_extension_cotoken_style',
        {'co_token_17_allowed': True,
         's_domain': '{17..55}', 'arity_max': 4},
        41, 23, 17, 17, 55, 17))
    # (d2) IN-BAND m=16-row z=23 record: cross-artifact recheck (40/0).
    out.append(row_record_x0(
        'inband_m16_z23_row_record',
        'cross_artifact_recheck_future_tz21_residual_m16_z23_expected_40_shapes',
        {'co_token_16_allowed': True,
         'residual_band': 'future T-Z21 residual band m=16 z in {22..29}; z=22 entry (z22-min17 census kit) 40 shapes 0 seps + ext 39/0; z=23 entry (z23-min18 kit) 40/0; same enumeration -> same 40 shapes here',
         's_domain': '{16..54}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        40, 23, 16, 16, 54))
    # (d3) IN-BAND m=15-row z=23 record: cross-artifact recheck (50/0).
    out.append(row_record_x0(
        'inband_m15_z23_row_record',
        'cross_artifact_recheck_k1335_residual_m15_z23_expected_50_shapes',
        {'co_token_15_allowed': True,
         'residual_band': 'K1335 (T-Z20) published residual band m=15 z in {21..28}; z=21 (z21-min16 kit) 50/0; z=22 (z22-min17 kit) 50/0; z=23 (z23-min18 kit) 50/0; same enumeration -> same 50 shapes here',
         's_domain': '{15..53}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        39, 23, 15, 15, 53))
    # (d4) IN-BAND m=14-row z=23 record: cross-artifact recheck (62/0).
    out.append(row_record_x0(
        'inband_m14_z23_row_record',
        'cross_artifact_recheck_k1330_residual_m14_z23_expected_62_shapes',
        {'co_token_14_allowed': True,
         'residual_band': 'K1330 published m=14 z in {20..25}; z=21 (z21-min16) 62/0; z=22 (z22-min17) 62/0; z=23 (z23-min18) 62/0; same enumeration -> same 62 shapes here',
         's_domain': '{14..52}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        38, 23, 14, 14, 52))
    # (d5) IN-BAND m=13-row z=23 record: cross-artifact recheck (76/0).
    out.append(row_record_x0(
        'inband_m13_z23_row_record',
        'cross_artifact_recheck_k1328_residual_m13_z23_expected_76_shapes',
        {'co_token_13_allowed': True,
         'residual_band': 'K1328 published m=13 z in {19..24}; z=19 (z19-min14) 76/0; z=20 76/0 + ext 75/0; z=21 76/0; z=22 76/0; z=23 (z23-min18) 76/0; same enumeration -> same 76 shapes here',
         's_domain': '{13..51}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        37, 23, 13, 13, 51))
    # (e) strip spots m in 23..26 at R=m+24 (lattice identity with the
    #     published f18 12/12 match)
    spots = []
    for m in range(23, 27):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 24, X, 23)
            ev = v(S, 23, m + 24)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    out.append({'section': 'strip_spots_m23_26', 'rows': spots})
    # NEW m=17 base spot (never measured by any published kit;
    # paper-derived candidate 0 conforming, disclosed in the docstring)
    w = H(41, (17, 17), 23)
    wv = v(34, 23, 41)
    out.append({'section': 'm17_base_spot', 'X': [17, 17], 'R': 41,
                'z': 23, 'value': w, 'collapse_single': wv,
                'match': w == wv,
                'published_probe_crossref': 'NEW measurement: no published kit measured H(41;(17,17);23) (the published z23-min18 census kit measured the m=18 base spot H(42;(18,18);23)=1 only; the published z22-min17 census kit measured the z=22 spot H(40;(17,17);22)=0 only); paper-derived candidate value 0 = v(34,23,41) conforming, derivation disclosed in this file docstring before the first run (B-children on the published z=23 m=16-row observational record, C-child on the PROVED T-Z22 m=17-row claim)'})
    # (f) below-band bottom-rung child census: H(24;Y;24) vs v(s,24,24)
    #     with Y >= 17 (SEVENTH z'-7 empty-datum candidate, floor
    #     z'-7 at z'=24)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(17, 49)):
        ys = [()] if s == 0 else parts(s, 17, 4)
        vals = {}
        for y in ys:
            h = H(24, y, 24)
            vals.setdefault(h, []).append(y)
            bb_total += 1
        if len(vals) > 1:
            bb_multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s, 24, 24)
            if val != exp:
                bb_dev.append({'s': s, 'value': val, 'collapse': exp,
                               'direction': 'UP' if val > exp else 'DOWN',
                               'shapes': len(vals[val])})
    out.append({'section': 'belowband_j1_child_H24_24',
                'label': 'observational_only_seventh_zprime7_datum_belowband_supply_source_at_z23_floor17',
                'R': 24, 'z': 24, 'floor': 17,
                's_domain': '{0} U {17..48}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (g1) FOURTEENTH-TAIL SUPPLY IDENTITY RECHECK (pure K0832)
    holds = []
    breaks = []
    for s in [0] + list(range(12, 64)):
        a = v(s, 24, 24)
        b = v(s, 23, 24)
        row = {'s': s, 'v_24_24': a, 'v_23_24': b, 'equal': a == b}
        (holds if a == b else breaks).append(row)
    out.append({'section': 'fourteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,24,24) =? v(s,23,24)',
                's_domain': '{0} U {12..63}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z20-min15 census kit + z21-min16 census kit + z20-floor14 kit + z21-floor15 kit + z23-min18 kit (this slice own F-supply datum at z=23): holds {0} U {12..23}, UNIFORM 0v1 break for all s>=24 (final hold s=23 = the F hole; first break s=24 = the tail start; predeclared odd-z candidate confirmed); rechecked and extended here over s in {0} U {12..63}',
                'hold_rows': holds, 'break_rows': breaks})
    # (g2) FIFTEENTH-TAIL SUPPLY IDENTITY RECHECK
    t_holds = []
    t_breaks = []
    for s in [0] + list(range(12, 64)):
        a = v(s, 25, 25)
        b = v(s, 24, 25)
        row = {'s': s, 'v_25_25': a, 'v_24_25': b, 'equal': a == b}
        (t_holds if a == b else t_breaks).append(row)
    out.append({'section': 'fifteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,25,25) =? v(s,24,25)',
                's_domain': '{0} U {12..63}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z21-min16 census kit + z20-floor14 kit + z21-floor15 kit + z23-min18 kit: holds {0} U {12..23}, 0v2 break at s=24, then uniformly 2v1 for all s>=25; rechecked and extended here',
                'hold_rows': t_holds, 'break_rows': t_breaks})
    # (g3) SIXTEENTH-TAIL SUPPLY IDENTITY RECHECK
    n_holds = []
    n_breaks = []
    for s in [0] + list(range(12, 64)):
        a = v(s, 26, 26)
        b = v(s, 25, 26)
        row = {'s': s, 'v_26_26': a, 'v_25_26': b, 'equal': a == b}
        (n_holds if a == b else n_breaks).append(row)
    out.append({'section': 'sixteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,26,26) =? v(s,25,26)',
                's_domain': '{0} U {12..63}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'NEW by the z22-floor16 kit, predeclared and confirmed by the z23-min18 census kit precalc section and rechecked by the z21-floor15 kit: holds {0} U {12..25}, uniform 0v1 break for all s>=26 (odd-z supply form); rechecked and extended here',
                'hold_rows': n_holds, 'break_rows': n_breaks})
    # (g4) SEVENTEENTH-TAIL SUPPLY IDENTITY RECHECK
    p_holds = []
    p_breaks = []
    for s in [0] + list(range(12, 64)):
        a = v(s, 27, 27)
        b = v(s, 26, 27)
        row = {'s': s, 'v_27_27': a, 'v_26_27': b, 'equal': a == b}
        (p_holds if a == b else p_breaks).append(row)
    out.append({'section': 'seventeenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,27,27) =? v(s,26,27)',
                's_domain': '{0} U {12..63}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'NEW by the z20-floor14 kit section (g5): hold {0} U {12..25}, 0v2 break at s=26, UNIFORM 2v1 for ALL s>=27 (both components predeclared and confirmed; even-z supply form); rechecked by the z21-floor15 kit; rechecked and extended here',
                'hold_rows': p_holds, 'break_rows': p_breaks})
    # (g5) EIGHTEENTH-TAIL SUPPLY IDENTITY RECHECK
    e_holds = []
    e_breaks = []
    for s in [0] + list(range(12, 64)):
        a = v(s, 28, 28)
        b = v(s, 27, 28)
        row = {'s': s, 'v_28_28': a, 'v_27_28': b, 'equal': a == b}
        (e_holds if a == b else e_breaks).append(row)
    out.append({'section': 'eighteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,28,28) =? v(s,27,28)',
                's_domain': '{0} U {12..63}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'NEW by the z21-floor15 kit (commit 5b01e14c): hold {0} U {12..27}, UNIFORM 0v1 for ALL s in {28..62} (both components predeclared and confirmed; odd-z supply form 5/5 graduated; the z=27 slice supply datum); rechecked and extended here over s in {0} U {12..63}',
                'hold_rows': e_holds, 'break_rows': e_breaks})
    # (g6) NINETEENTH-TAIL SUPPLY PRE-COMPUTATION (NEW, pure K0832)
    n19_holds = []
    n19_breaks = []
    for s in [0] + list(range(12, 64)):
        a = v(s, 29, 29)
        b = v(s, 28, 29)
        row = {'s': s, 'v_29_29': a, 'v_28_29': b, 'equal': a == b}
        (n19_holds if a == b else n19_breaks).append(row)
    out.append({'section': 'nineteenth_tail_supply_identity_precalc',
                'label': 'observational_only_new_closed_form_precalc_z28_slice_supply_k0832',
                'identity': 'v(s,29,29) =? v(s,28,29)',
                's_domain': '{0} U {12..63}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'predeclared_candidate': 'BOTH components predeclared (registered as the natural next pre-computation by the published z21-floor15 kit log section 5 handoff): even-k identity shape (published even constants: k=20 z=20-supply hold {0} U {12..19} 0v2@20 2v1 s>=21; k=22 z=22-supply hold {0} U {12..21} 0v2@22 2v1 s>=23; k=24 z=24-supply hold {0} U {12..23} 0v2@24 2v1 s>=25; k=26 z=26-supply hold {0} U {12..25} 0v2@26 2v1 s>=27; even form 4/4 measured) gives the candidate: hold on {0} U {12..27}, break START at s=28 (=k), break shape 0v2 at s=28 then UNIFORM 2v1 for ALL s in {29..63}; z=28-supply decides whether the even-z supply form graduates to 5/5; constants recorded whatever they are',
                'hold_rows': n19_holds, 'break_rows': n19_breaks})
    # (g7) TWENTIETH-TAIL SUPPLY PRE-COMPUTATION (NEW, pure K0832)
    t20_holds = []
    t20_breaks = []
    for s in [0] + list(range(12, 64)):
        a = v(s, 30, 30)
        b = v(s, 29, 30)
        row = {'s': s, 'v_30_30': a, 'v_29_30': b, 'equal': a == b}
        (t20_holds if a == b else t20_breaks).append(row)
    out.append({'section': 'twentieth_tail_supply_identity_precalc',
                'label': 'observational_only_new_closed_form_precalc_z29_slice_supply_k0832',
                'identity': 'v(s,30,30) =? v(s,29,30)',
                's_domain': '{0} U {12..63}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'predeclared_candidate': 'BOTH components predeclared (the natural next of the same family, one step past the registered NINETEENTH-tail handoff; both components derivable from the current closed-form data): odd-k identity shape (published odd constants: k=19/21/23/25 measured uniform-shape holds, k=27 NEW by the z21-floor15 kit graduating the odd-z form 5/5) gives the candidate: hold on {0} U {12..29}, break START at s=30 (=k+1), break shape UNIFORM 0v1 for ALL s in {30..63}; z=29-supply extends the odd-z form to the 6/6 candidate; constants recorded whatever they are',
                'hold_rows': t20_holds, 'break_rows': t20_breaks})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
