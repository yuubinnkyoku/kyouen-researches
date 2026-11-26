#!/usr/bin/env python3
"""
explore_z21f15: FROZEN PRE-DECLARATION census for the z=21 FLOOR-15
(z-6, SUB-CRITICAL floor) cell ladder — the EIGHTH edition of the
floor-(z-6) series (z=15 K1321, z=16 `059c531e`, z=17 `82f98ef4`,
z=18 `0bb7e440`, z=19 `5b2275bc`, z=20 `2d8cea40`, z=22
`fb215b76`/`daa9a805`) and the last unswept ODD floor below z=24.
NO K slot is claimed by this file; the constants below were frozen
into this docstring BEFORE the first run of this file and the file
has not been edited after any of its runs.

The architectural target is the REGISTERED PREDICTION of the
published z=20 floor-14 kit log section 5 (commit `2d8cea40`, same
day, BEFORE the fact): "The next floor-(z-6) series datum: z=21
floor-15 (odd, the head candidate is EMPTY per the odd-edition
pattern 3/3 published)" — plus that log's registered EIGHTEENTH-tail
handoff: "the EIGHTEENTH-tail (k=27, odd form, v(s,28,28)=? v(s,27,28))
is the natural next pre-computation (z=27 supply; odd form candidate
5/5 extension confirmed shape: hold {0} U {12..27}? — recorded by
whoever runs it; both components derivable from the current data
as before)".

HONEST DISCLOSURE (drafting discipline, before the freeze): the
hand derivations below were written in-session from published
PROVED facts only (the K1335/T-Z20 proved z=20 floor-15 cell
ladder, the K1264 stair equality, the K0832 closed form, the
published z=21-min16 census records) and the child-position INPUT
LITERALS were cross-checked against a drafting scratch engine
evaluation BEFORE this file was frozen (the K1344-D6 discipline
applied: derivation -> engine cross-check of the input literals ->
freeze; the scratch machine itself is NOT published and evaluates
NONE of the declared outcome values). The file itself ran for the
first time only after the freeze. The genuinely BLIND
pre-declarations of this file (no engine evaluation before the
freeze) are: the s=15 head-row OUTCOME values (the mex results),
the shared-block {16..29} acceptance itself, the BLIND sub-floor
block s in {30..46}, the multivalue census, the strip/row/
base-spot/below-band measurements (b)-(f) and every measured
COUNT (shape counts are measured, not predeclared, per series
convention). The tail-identity constants of section (g) are pure
published K0832 closed-form evaluations (engine-free).

Scope (this file measures and reports; it proves nothing by
itself):
  (a) cell census: for each j in 1..15 the floor-15 cell
      Cell_j(s) := H(j+22; {j} U Y; 21), Y tokens >= 15, s = sum(Y)
      in {0} U {15..46}, arity(Y) in 0..4 (0 only at s=0), swept
      EXHAUSTIVELY against the published raw engine (K1138
      recursion, embedded block byte-identical to the K1282..K1344
      chain, pin bd5f22e4...). Reported per cell: deviants from the
      Sigma-collapse v(s+j,21,j+22) (K0832 closed form) and any
      multivalue (decomposition-dependence) rows. The 15 rungs are
      labeled F..A9 ALIGNED with the published z=21 critical ladder
      (F21f16..A921f16); no rank beyond A9 is swept (a j=16 rung is
      NOT paper-derivable at s=15: its C-hand child (37;{15,16};20)
      is covered by no published ladder cell nor strip claim — that
      rank belongs to a future lane).
      PREDECLARED CANDIDATES (frozen before the first run):
      (i) THE s=15 ROW — the floor-necessity test and the registered
          EMPTY ODD HEAD. Single shape (j,15) at every j. Full
          15-point profile derived BY HAND from four published
          inputs: (1) the C-hand child of Cell_j(15) is exactly the
          published PROVED z=20 critical-ladder position
          H(j+21;{j,15};20) (Y-token 15 >= that ladder's floor 15)
          — the PROVED K1335 (T-Z20) cell constants at s=15: the
          whole published z=20 ladder row at s=15 CONFORMS
          (F..A8 deviants live at {16,18,20}), for j=15 the PROVED
          T-Z20 m=15-row base position H(36;(15,15);20)=v(30,20,36)=
          0; (2) the published K1264 stair equality covers every
          15->14 B-hand child (j,14) at R=j+21 EXACTLY (min=j) for
          j in 1..14; (3) the small-token B-child is the in-kit
          cascade Cell_{j-1}(15), R=j+21 = 21+(j-1)+1 one ABOVE the
          stair, and the j=1 removal child is the single token
          H(22;(15,);22) = v(15,22,22) = 1 (stair R=22 <= 22+15);
          (4) the sole NON-proved input: for j=15 both B-hand
          children land on (36;(14,15);21) = the published z=21
          m=14-row OBSERVATIONAL record position (z21-min16 census
          kit: 62 shapes 0 separations) => H(36;(14,15);21)=
          v(29,21,36)=1 — a single observational dependency,
          disclosed, mirroring the published z20-f14 kit's own
          single-observational-dependency pattern at its j=14 rung.
          Derived profile (every option set below was written
          BEFORE the first run; input literals engine-cross-checked
          at drafting):
          j=1  F conform v(16,21,23)=0 (options {stair v(15,21,22)=1,
               removal v(15,22,22)=1, 1^C-hand v(16,20,22)=0 -> 1} ->
               mex 0 = collapse);
          j=2  G conform v(17,21,24)=1 (options {stair v(16,21,23)=0,
               Cell_1=0, 1^v(17,20,23)=1^1=0} -> mex 1 = collapse);
          j=3  E conform v(18,21,25)=0 (options {stair v(17,21,24)=1,
               Cell_2=1, 1^v(18,20,24)=1^0=1} -> mex 0 = collapse);
          j=4  D conform v(19,21,26)=1 (options {stair v(18,21,25)=0,
               Cell_3=0, 1^v(19,20,25)=1^1=0} -> mex 1 = collapse);
          j=5  C conform v(20,21,27)=0 (options {stair v(19,21,26)=1,
               Cell_4=1, 1^v(20,20,26)=1^0=1} -> mex 0 = collapse);
          j=6  B conform v(21,21,28)=1 (options {stair v(20,21,27)=0,
               Cell_5=0, 1^v(21,20,27)=1^1=0} -> mex 1 = collapse);
          j=7  A conform v(22,21,29)=0 (options {stair v(21,21,28)=1,
               Cell_6=1, 1^v(22,20,28)=1^0=1} -> mex 0 = collapse);
          j=8  A2 conform v(23,21,30)=1 (options {stair v(22,21,29)=0,
               Cell_7=0, 1^v(23,20,29)=1^1=0} -> mex 1 = collapse);
          j=9..14 A3..A8 conform (the same two-member alternation
               continues: option sets {stair v(j+14,21,j+21),
               Cell_{j-1}, 1^v(j+15,20,j+21)} = {1,1,1} -> mex 0 for
               odd j, {0,0,0} -> mex 1 for even j, at each step the
               collapse v(j+15,21,j+22) alternates 0/1 in step);
          j=15 A9 conform v(30,21,37)=0 (options {both B-hand
               children (14,15) at (36;.;21) = 1 (the disclosed
               observational record value), 1^v(30,20,36)=1^0=1} ->
               mex 0 = collapse).
          THE REGISTERED CLAIM CARRIED BY THIS ROW: the odd
          sub-critical head is EMPTY — no deviant class at s=z-6=
          15, the whole row conforming — extending the published
          odd-edition head-empty pattern (z=15 K1321, z=17
          `82f98ef4`, z=19 `5b2275bc`) to its candidate 4/4, the
          mirror of the even head trio {B DOWN 0v2, A UP 1v0, A2
          UP 2v1} registered value-exact 4/4 at z in {16,18,20,22}
          by the published z20-f14 kit. Consequence IF CONFIRMED:
          the critical floor 16 = z-5 is NECESSARY at z=21 for the
          head-only part of the cell-ladder Sigma-collapse — the
          floor-necessity of the ODD editions is witnessed at the
          head not by row deviants but by the (proved, published)
          z=19 A-break class birth s=z-5: the A21f16 rebirth class
          {s=16 UP 2v0} survives at floor 15 (s=16 > 15, see
          candidate (ii)) while remaining UNREACHABLE from the
          s=15 row; also 0 multivalue at s=15.
      (ii) s in {16..29}: LATTICE IDENTITY with the published
           floor-16 census (explore_z21f16.out, z21-min16 census
           kit): at every s in {16..29} the Y-shape sets of this
           census coincide exactly with the published f16 shape
           sets (no 15-token component fits below s=30), so every
           shared engine point is byte-identical by determinism;
           the deviant classes are exactly the published f16
           profile — F {20: DOWN 1v2, 21: HOLE (conforming),
           22..46: UP 2v0 persistent tail}, G {20: DOWN 0v1},
           E {18: DOWN 1v2, 20: UP 2v0}, D {18: DOWN 0v1},
           C {16: DOWN 1v2, 18: UP 2v0}, B {16: DOWN 0v1},
           A {16: UP 2v0 (the A RANK BREAK REBIRTH class, birth
           s=z-5=16: SURVIVES the floor drop 16->15 — the
           definition-domain-exclusion NON-event 3rd consecutive,
           after z=22's G/E-class survival and z=20's survival of
           {16,18})}, A2..A9 collapsed — and NO other deviant row
           in {16..29}.
      (iii) s in {30..46} (the BLIND sub-floor block: 15-token
            components enter the lattice for the first time —
            (15,15) at s=30, then (15,k) from s=31, then (15,15,16)
            at s=46): candidates NO multivalue rows and NO new
            deviant classes beyond the f16 classes of (ii) (the
            published z22-f16 {32..47} and z20-f14 {28..45} analogs
            were empty of both).
      (iv) all cells s-only; multivalue rows 0.
  (b) tail spots: s in {47..54}, single-token shape Y=(s,), all 15
      cells — lattice identity with the published f16 tail spots
      (same positions j+22; (j,s) at z=21): candidate F21f15 8/8
      mismatch (the published F21f16 tail spots were 8/8 mismatch),
      all other cells 112/120 total rows match.
  (c) strip sweep m in {15..20} at R=m+22: m in {16..20} are the
      PROVED T-Z21 claim positions (compliance recheck only; the
      published f16 cumulative profile 44/79/107/130/150, 0
      violations — incrementals 44/35/28/23/20 expected EXACT);
      m=15 is the OPEN m=15 row at z=21 (z*(15)=29 > 21, in-band
      for min=15 by the K1268 band formula z*(m)=2m-2+(m mod 2)):
      co-token-style arity<=4-TOTAL sweep, S in {15..54}: candidate
      0 violations (measured count recorded whatever it is).
  (d) IN-BAND m=15-row z=21 record at R=37, x0 published
      residual-band style (all parts >= 15, co-token 15 allowed,
      arity <= 3 TOTAL, S in {15..53}): CROSS-ARTIFACT RECHECK of
      the published z21-min16 census kit record (50 shapes 0
      separations) AND its continuing role as the FIRST entry of
      the K1335-published T-Z20 residual band m=15 z in {21..28}
      (frontier z*(15)=29). PLUS the arity<=4 co-token extension
      sweep (published z21-min16 ext: 49 shapes 0 separations).
  (d2) IN-BAND m=14-row z=21 record at R=36, S in {14..52}:
      cross-artifact recheck of the published z21-min16 record
      (62/0; K1330 published residual band m=14 z in {20..25}
      second entry context).
  (d3) IN-BAND m=13-row z=21 record at R=35, S in {13..51}:
      cross-artifact recheck (76/0; K1328 band third entry).
  (d4) IN-BAND m=12-row z=21 record at R=34, S in {12..50}:
      cross-artifact recheck (92/0; K1325 band fourth and final
      entry context).
  (e) strip spots m in {21..24}, X in {(m,m+1),(m,m+2),(m,m,m+1)}:
      lattice identity with the published f16 strip spots (12/12
      match), PLUS the NEW m=15 BASE SPOT H(37;(15,15);21) vs
      v(30,21,37): paper-derived candidate value 0, CONFORMING
      (derivation disclosed here before the first run: both
      B-children land at (36;(14,15);21), the z=21 m=14-row
      record position (published observational 0 separations =>
      v(29,21,36)=1); the C-child is 1^H(36;(15,15);20) =
      1^v(30,20,36) = 1 by the PROVED T-Z20 m=15-row claim; the
      single token x=30, z=21, R=37 has options {1, 1} -> mex 0 =
      collapse v(30,21,37)=0). Never measured by any published kit
      (the published z21-min16 kit measured the m=16 base spot
      H(38;(16,16);21)=1 only). This is the m=15-row base point;
      its value does not claim the row. The m=15 base-spot
      z-sequence so far: z=20: 0 (published z20-min15 kit value),
      z=21: 0 (candidate here) — no alternation yet.
  (f) below-band bottom-rung child census: the j=1 cell's B-move
      removal child is the below-band position H(22;Y;22) with
      min(Y) >= 15 (child slice z'=22, floor 15 = z'-7), swept over
      s in {0} U {15..46}, arity 0..4, against v(s,22,22). This is
      the SIXTH z'-7 empty-datum candidate of the series (the five
      published below-band full collapses were swept at
      z'=17/19/20/21/23): candidate 0 deviants, 0 multivalue rows.
      The published K1264 stair applicability R=22 <= 22+min(Y)
      suggests the collapse is a stair consequence at ANY floor;
      recorded here as a machine corroboration of that PROVED
      lemma's instance; the generalization belongs to a declaration
      lane.
  (g) TAIL SUPPLY PRE-COMPUTATIONS (pure published K0832 closed
      form, NO engine recursion), all over the EXTENDED domain
      s in {0} U {12..62} (each extended by one point from the
      published z20-f14 kit domain {0} U {12..61}):
      (g1) TWELFTH-tail identity RECHECK v(s,22,22) vs
          v(s,21,22) — THIS slice's own F-cell supply datum
          (z=21): candidate hold {0} U {12..21}, UNIFORM 0v1
          break for all s in {22..62} (final hold s=21 = the F
          hole; first break s=22 = the tail start; odd-z supply
          form).
      (g2) THIRTEENTH-tail identity RECHECK v(s,23,23) vs
          v(s,22,23): candidate hold {0} U {12..21}, 0v2 break at
          s=22, uniformly 2v1 for all s in {23..62} (even-z supply
          form).
      (g3) FOURTEENTH-tail identity RECHECK v(s,24,24) vs
          v(s,23,24): candidate hold {0} U {12..23}, uniform 0v1
          break for all s in {24..62} (odd-z supply form).
      (g4) FIFTEENTH-tail identity RECHECK v(s,25,25) vs
          v(s,24,25): candidate hold {0} U {12..23}, 0v2 break at
          s=24, uniformly 2v1 for all s in {25..62}.
      (g5) SIXTEENTH-tail identity RECHECK v(s,26,26) vs
          v(s,25,26): candidate hold {0} U {12..25}, uniform 0v1
          break for all s in {26..62} (odd-z supply form).
      (g6) SEVENTEENTH-tail identity RECHECK v(s,27,27) vs
          v(s,26,27): candidate hold {0} U {12..25}, 0v2 break at
          s=26, uniformly 2v1 for all s in {27..62} (published NEW
          by the z20-floor14 kit, rechecked here extended).
      (g7) NEW EIGHTEENTH-tail PRE-COMPUTATION v(s,28,28) vs
          v(s,27,28) — the z=27-slice supply datum (registered as
          the natural next pre-computation by the published
          z20-floor14 kit handoff, the halted 2026-11-26 session's
          hand-preparation, and the K1339/K1344 chain handoffs):
          BOTH components predeclared. The odd-k identity shape
          (published odd constants: k=19 z=19-supply hold {0} U
          {12..19} uniform 0v1 s>=20; k=21 z=21-supply hold
          {0} U {12..21} 0v1 s>=22; k=23 z=23-supply hold
          {0} U {12..23} 0v1 s>=24; k=25 z=25-supply hold
          {0} U {12..25} 0v1 s>=26; odd form 4/4 measured)
          gives the candidate: hold on {0} U {12..27}, break
          START at s=28 (=k+1), break shape UNIFORM 0v1 for ALL
          s in {28..62}; z=27-supply decides whether the odd-z
          supply form graduates to 5/5; constants recorded
          whatever they are. (Registered candidate shape:
          hold {0} U {12..27}.)

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z21f15.out).
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
    """sweep cell_j over s in {0} U {15..smax}; returns (dev, multi, total)"""
    R = j + 22
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(15, smax + 1)):
        ys = [()] if s == 0 else parts(s, 15, 4)
        vals = {}
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            h = H(R, X, 21)
            vals.setdefault(h, []).append(y)
            total += 1
        if len(vals) > 1:
            multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s + j, 21, R)
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
             'A5', 'A6', 'A7', 'A8', 'A9']
    for j in range(1, 16):
        name = names[j - 1]
        dev, multi, total = cell_sweep(j, 46)
        cells[f'cell{j}_{name}21f15'] = {
            'z': 21, 'min': j, 'R': j + 22, 'floor': 15,
            's_domain': '{0} U {15..46}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}21f15',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 16):
        nm = names[j - 1]
        for s in range(47, 55):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 22, X, 21)
            exp = v(s + j, 21, j + 22)
            tail.append({'cell': f'{nm}21f15', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s47_54', 'rows': tail})
    # (c) strip sweep m in 15..20 at R=m+22: m 16..20 are the PROVED
    #     T-Z21 claim positions (compliance recheck); m=15 is the OPEN
    #     m=15 row at z=21 (candidate 0 violations).
    sv = []
    viol = []
    cnt = 0
    for m in range(15, 21):
        H.cache_clear()
        for S in range(m, m + 40):
            for X in parts(max(S - m, 0), m, 3):
                XX = tuple(sorted((m,) + X, reverse=True))
                if sum(XX) != S:
                    continue
                hv = H(m + 22, XX, 21)
                ev = v(S, 21, m + 22)
                cnt += 1
                if hv != ev:
                    viol.append({'m': m, 'X': list(XX), 'S': S,
                                 'value': hv, 'collapse': ev})
        sv.append({'m': m, 'cumulative_shapes': cnt,
                   'cumulative_violations': len(viol)})
    out.append({'section': 'strip_z21_m15_20', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) IN-BAND m=15-row record at the z=21 m=15 row position
    #     (37; X; 21), all parts >= 15 (co-token 15 allowed), arity <= 3
    #     TOTAL. CROSS-ARTIFACT RECHECK of the published z21-min16 kit
    #     record (50 shapes 0 seps) AND its role as the FIRST entry of
    #     the K1335-published T-Z20 residual band m=15 z in {21..28}.
    out.append(row_record_x0(
        'inband_m15_z21_row_record',
        'cross_artifact_recheck_of_published_f16_record_and_k1335_residual_band_m15_first_entry',
        {'co_token_15_allowed': True,
         'residual_band': 'K1335 (T-Z20) published residual band m=15 z in {21..28} (frontier z*(15)=29 per the K1268 formula z*(m)=2m-2+(m mod 2)); published z21-min16 census kit entry: 50 shapes 0 separations (recheck expected shape-for-shape)',
         's_domain': '{15..53}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        37, 21, 15, 15, 53))
    out.append(row_record(
        'inband_m15_z21_row_record_ext_arity4',
        'cross_artifact_recheck_arity_le4_extension_cotoken_style',
        {'co_token_15_allowed': True,
         's_domain': '{15..53}', 'arity_max': 4},
        37, 21, 15, 15, 53, 15))
    # (d2) IN-BAND m=14-row z=21 record: cross-artifact recheck (62/0).
    out.append(row_record_x0(
        'inband_m14_z21_row_record',
        'cross_artifact_recheck_k1330_residual_m14_z21_expected_62_shapes',
        {'co_token_14_allowed': True,
         'residual_band': 'K1330 published m=14 z in {20..25}; published z21-min16 census kit entry: 62 shapes 0 separations (recheck expected shape-for-shape)',
         's_domain': '{14..52}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        36, 21, 14, 14, 52))
    # (d3) IN-BAND m=13-row z=21 record: cross-artifact recheck (76/0).
    out.append(row_record_x0(
        'inband_m13_z21_row_record',
        'cross_artifact_recheck_k1328_residual_m13_z21_expected_76_shapes',
        {'co_token_13_allowed': True,
         'residual_band': 'K1328 published m=13 z in {19..24}; published z21-min16 census kit entry: 76 shapes 0 separations (recheck expected shape-for-shape)',
         's_domain': '{13..51}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        35, 21, 13, 13, 51))
    # (d4) IN-BAND m=12-row z=21 record: cross-artifact recheck (92/0).
    out.append(row_record_x0(
        'inband_m12_z21_row_record',
        'cross_artifact_recheck_k1325_residual_m12_z21_expected_92_shapes',
        {'co_token_12_allowed': True,
         'residual_band': 'K1325 published m=12 z in {18..21}; published z21-min16 census kit entry: 92 shapes 0 separations (recheck expected shape-for-shape)',
         's_domain': '{12..50}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        34, 21, 12, 12, 50))
    # (e) strip spots m in 21..24 (lattice identity with the published
    #     f16 12/12 match)
    spots = []
    for m in range(21, 25):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 22, X, 21)
            ev = v(S, 21, m + 22)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    out.append({'section': 'strip_spots_m21_24', 'rows': spots})
    # NEW m=15 base spot (never measured by any published kit;
    # paper-derived candidate 0 conforming, disclosed in the docstring)
    w = H(37, (15, 15), 21)
    wv = v(30, 21, 37)
    out.append({'section': 'm15_base_spot', 'X': [15, 15], 'R': 37,
                'z': 21, 'value': w, 'collapse_single': wv,
                'match': w == wv,
                'published_probe_crossref': 'NEW measurement: no published kit measured H(37;(15,15);21) (the published z21-min16 census kit measured the m=16 base spot H(38;(16,16);21)=1 only); paper-derived candidate value 0 = v(30,21,37) conforming, derivation disclosed in this file docstring before the first run (B-children on the published z=21 m=14-row observational record, C-child on the PROVED T-Z20 m=15-row claim)'})
    # (f) below-band bottom-rung child census: H(22;Y;22) vs v(s,22,22)
    #     with Y >= 15 (SIXTH z'-7 empty-datum candidate, floor
    #     z'-7 at z'=22)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(15, 47)):
        ys = [()] if s == 0 else parts(s, 15, 4)
        vals = {}
        for y in ys:
            h = H(22, y, 22)
            vals.setdefault(h, []).append(y)
            bb_total += 1
        if len(vals) > 1:
            bb_multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s, 22, 22)
            if val != exp:
                bb_dev.append({'s': s, 'value': val, 'collapse': exp,
                               'direction': 'UP' if val > exp else 'DOWN',
                               'shapes': len(vals[val])})
    out.append({'section': 'belowband_j1_child_H22_22',
                'label': 'observational_only_sixth_zprime7_datum_belowband_supply_source_at_z21_floor15',
                'R': 22, 'z': 22, 'floor': 15,
                's_domain': '{0} U {15..46}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (g1) TWELFTH-TAIL SUPPLY IDENTITY RECHECK (pure K0832)
    holds = []
    breaks = []
    for s in [0] + list(range(12, 63)):
        a = v(s, 22, 22)
        b = v(s, 21, 22)
        row = {'s': s, 'v_22_22': a, 'v_21_22': b, 'equal': a == b}
        (holds if a == b else breaks).append(row)
    out.append({'section': 'twelfth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,22,22) =? v(s,21,22)',
                's_domain': '{0} U {12..62}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'beyond_z20 kit section (10) + z20-min15 census kit section (g2) + z21-min16 census kit section (g1): holds {0} U {12..21}, UNIFORM 0v1 break for all s>=22 over s in {0} U {12..58} (predeclared odd-z candidate confirmed; this slice own F-supply datum; final hold s=21 = the F hole; first break s=22 = the tail start); rechecked and extended here over s in {0} U {12..62}',
                'hold_rows': holds, 'break_rows': breaks})
    # (g2) THIRTEENTH-TAIL SUPPLY IDENTITY RECHECK
    t_holds = []
    t_breaks = []
    for s in [0] + list(range(12, 63)):
        a = v(s, 23, 23)
        b = v(s, 22, 23)
        row = {'s': s, 'v_23_23': a, 'v_22_23': b, 'equal': a == b}
        (t_holds if a == b else t_breaks).append(row)
    out.append({'section': 'thirteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,23,23) =? v(s,22,23)',
                's_domain': '{0} U {12..62}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z20-min15 census kit section (g3) + z21-min16 census kit section (g2) + z20-floor14 census kit section (g1): holds {0} U {12..21}, 0v2 break at s=22, then uniformly 2v1 for all s>=23 over s in {0} U {12..61}; rechecked and extended here',
                'hold_rows': t_holds, 'break_rows': t_breaks})
    # (g3) FOURTEENTH-TAIL SUPPLY IDENTITY RECHECK
    n_holds = []
    n_breaks = []
    for s in [0] + list(range(12, 63)):
        a = v(s, 24, 24)
        b = v(s, 23, 24)
        row = {'s': s, 'v_24_24': a, 'v_23_24': b, 'equal': a == b}
        (n_holds if a == b else n_breaks).append(row)
    out.append({'section': 'fourteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,24,24) =? v(s,23,24)',
                's_domain': '{0} U {12..62}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z21-min16 census kit section (g3, predeclared odd candidate confirmed) + z20-floor14 census kit section (g2): holds {0} U {12..23}, uniform 0v1 break for all s>=24 over s in {0} U {12..61}; rechecked and extended here',
                'hold_rows': n_holds, 'break_rows': n_breaks})
    # (g4) FIFTEENTH-TAIL SUPPLY IDENTITY RECHECK
    p_holds = []
    p_breaks = []
    for s in [0] + list(range(12, 63)):
        a = v(s, 25, 25)
        b = v(s, 24, 25)
        row = {'s': s, 'v_25_25': a, 'v_24_25': b, 'equal': a == b}
        (p_holds if a == b else p_breaks).append(row)
    out.append({'section': 'fifteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,25,25) =? v(s,24,25)',
                's_domain': '{0} U {12..62}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z20-floor14 census kit section (g3): holds {0} U {12..23}, 0v2 break at s=24, uniformly 2v1 for all s in {25..61} (both predeclared components CONFIRMED; even-z supply form); rechecked and extended here',
                'hold_rows': p_holds, 'break_rows': p_breaks})
    # (g5) SIXTEENTH-TAIL SUPPLY IDENTITY RECHECK
    x_holds = []
    x_breaks = []
    for s in [0] + list(range(12, 63)):
        a = v(s, 26, 26)
        b = v(s, 25, 26)
        row = {'s': s, 'v_26_26': a, 'v_25_26': b, 'equal': a == b}
        (x_holds if a == b else x_breaks).append(row)
    out.append({'section': 'sixteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,26,26) =? v(s,25,26)',
                's_domain': '{0} U {12..62}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'published NEW by the z22-floor16 kit (hold {0} U {12..25}, UNIFORM 0v1 for ALL s in {26..60}, both components predeclared and confirmed; odd-z supply form = the z=25 slice supply datum) and rechecked by the z20-floor14 census kit section (g4); rechecked and extended here over s in {0} U {12..62}',
                'hold_rows': x_holds, 'break_rows': x_breaks})
    # (g6) SEVENTEENTH-TAIL SUPPLY IDENTITY RECHECK
    y_holds = []
    y_breaks = []
    for s in [0] + list(range(12, 63)):
        a = v(s, 27, 27)
        b = v(s, 26, 27)
        row = {'s': s, 'v_27_27': a, 'v_26_27': b, 'equal': a == b}
        (y_holds if a == b else y_breaks).append(row)
    out.append({'section': 'seventeenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,27,27) =? v(s,26,27)',
                's_domain': '{0} U {12..62}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'published NEW by the z20-floor14 census kit section (g5): hold {0} U {12..25}, 0v2 break at s=26, UNIFORM 2v1 for ALL s in {27..61} (both components predeclared and confirmed; even-z supply form 4/4 = the z=26 slice supply datum); rechecked and extended here over s in {0} U {12..62}',
                'hold_rows': y_holds, 'break_rows': y_breaks})
    # (g7) EIGHTEENTH-TAIL SUPPLY PRE-COMPUTATION (NEW, pure K0832)
    e_holds = []
    e_breaks = []
    for s in [0] + list(range(12, 63)):
        a = v(s, 28, 28)
        b = v(s, 27, 28)
        row = {'s': s, 'v_28_28': a, 'v_27_28': b, 'equal': a == b}
        (e_holds if a == b else e_breaks).append(row)
    out.append({'section': 'eighteenth_tail_supply_identity_precalc',
                'label': 'observational_only_new_closed_form_precalc_z27_slice_supply_k0832',
                'identity': 'v(s,28,28) =? v(s,27,28)',
                's_domain': '{0} U {12..62}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'predeclared_candidate': 'BOTH components predeclared (registered as the natural next pre-computation by the published z20-floor14 kit handoff section 5, the 2026-11-26 halted-session hand preparation, and the K1339/K1344 chain handoffs): odd-k identity shape (published odd constants: k=19 z=19-supply hold {0} U {12..19} uniform 0v1 s>=20; k=21 z=21-supply hold {0} U {12..21} 0v1 s>=22; k=23 z=23-supply hold {0} U {12..23} 0v1 s>=24; k=25 z=25-supply hold {0} U {12..25} 0v1 s>=26; odd form 4/4 measured) gives the candidate: hold on {0} U {12..27}, break START at s=28 (=k+1), break shape UNIFORM 0v1 for ALL s in {28..62}; z=27-supply decides whether the odd-z supply form graduates to 5/5; constants recorded whatever they are',
                'hold_rows': e_holds, 'break_rows': e_breaks})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
