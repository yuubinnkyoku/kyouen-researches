#!/usr/bin/env python3
"""
explore_z20f14: FROZEN PRE-DECLARATION census for the z=20 FLOOR-14
(z-6, SUB-CRITICAL floor) cell ladder — the SEVENTH edition of the
floor-(z-6) series (z=15 K1321, z=16 `059c531e`, z=17 `82f98ef4`,
z=18 `0bb7e440`, z=19 `5b2275bc`, z=22 `fb215b76`/`daa9a805`) and
the LAST unswept even floor below z=24. NO K slot is claimed by this
file; publish-then-execute; the constants below were frozen into
this docstring BEFORE the first run of this file and the file has
not been edited after any of its runs.

The architectural target is the REGISTERED PREDICTION of the
published z=22 floor-16 kit log section 5 (commit `daa9a805`, same
day, BEFORE the fact): "head trio {B 0v2, A 1v0, A2 2v1} at s=14 and
the ladder B {16 UP 2v1}, C {16 UP 1v0}, D {16 DOWN 0v2, 18 UP 2v1},
E {18 UP 1v0}, F {20 UP 1v0}, G {18 DOWN 0v2, 20 UP 2v1} — 11
entries total, the same cellwise constants, all cells s-only,
0 multivalue rows; each row single-shape, matching the arithmetic
set {z-6, z-4, z-2, z} at z=20. If the z=20 edition hits this
profile exactly, the full-lattice uniformity reaches 4/4 across ALL
consecutive even z 16..22."

HONEST DISCLOSURE (drafting discipline, before the freeze): the
hand derivation below was written in-session from published PROVED
facts only (the T-Z19/K1330 z=19 critical ladder constants, the
K1264 stair equality, the K0832 closed form, the published T-Z19
m=14-row claim and the published z=20 f15 census constants); its
child-position constants were then cross-checked against a drafting
scratch engine evaluation BEFORE this file was frozen (the K1344-D6
discipline applied: derivation -> engine cross-check of the input
literals -> freeze). The file itself ran for the first time only
after the freeze. The genuinely BLIND pre-declarations of this file
(none of them was engine-checked before the freeze) are: (iii) the
sub-floor multi-token rows s in {28..45}, the multivalue census
(iv), the strip/row/base-spot/below-band/identity measurements
(b)-(g), and every measured COUNT (shape counts are measured, not
predeclared, per series convention).

Scope (this file measures and reports; it proves nothing by
itself):
  (a) cell census: for each j in 1..14 the floor-14 cell
      Cell_j(s) := H(j+21; {j} U Y; 20), Y tokens >= 14, s = sum(Y)
      in {0} U {14..45}, arity(Y) in 0..4 (0 only at s=0), swept
      EXHAUSTIVELY against the published raw engine (K1138
      recursion, embedded block byte-identical to the K1282..K1339
      chain, pin bd5f22e4...). Reported per cell: deviants from the
      Sigma-collapse v(s+j,20,j+21) (K0832 closed form) and any
      multivalue (decomposition-dependence) rows. The 14 rungs are
      labeled F..A8 ALIGNED with the published z=20 critical ladder
      (F20f15..A820f15); no rank beyond A8 is swept (a j=15 rung is
      NOT paper-derivable at s=14: its C-hand child H(35;{14,15};19)
      is covered by no published ladder cell nor strip claim — that
      rank belongs to a future lane).
      PREDECLARED CANDIDATES (frozen before the first run):
      (i) THE s=14 ROW — the floor-necessity test and the
          registered head trio. Single shape (j,14) at every j.
          Full 14-point profile derived BY HAND from four published
          inputs: (1) the C-hand child of Cell_j(14) is exactly the
          published PROVED z=19 critical-ladder position
          H(j+20;{j,14};19) (Y-token 14 >= that ladder's floor 14)
          — for j in 1..13 the published T-Z19 (K1330) cell-j
          constants (C/B/A deviant DOWN 1 / DOWN 0 / UP 2 at s=14,
          all others conform), for j=14 the published PROVED T-Z19
          m=14-row claim position H(34;{14,14};19) = v(28,19,34);
          (2) the published K1264 stair equality H(R;X;20) =
          v(sumX,20,R) for R <= 20+min(X) — every 14->13 B-hand
          child (j,13) at R=j+20 sits at the stair EXACTLY for
          j in 1..13 (min=j); (3) the small-token B-child is
          Cell_{j-1}(14) itself (R=j+20 = 20+(j-1)+1, one ABOVE
          the stair point — the in-kit cascade) and the j=1 removal
          child is the single token H(20;(14,);21) = v(14,21,20);
          (4) the sole NON-proved input: for j=14 the 14->13
          child (13,14) at (34;.;20) is the published m=13-row
          z=20 OBSERVATIONAL record position (f15 kit: 76 shapes 0
          separations) => H(34;(13,14);20)=v(27,20,34) — a single
          observational dependency, disclosed. Derived profile:
          j=1 F conform v(15,20,22)=1 (options {stair v(14,20,20)=0,
          removal v(14,21,20)=0, 1^C-hand v(15,19,21)=1^1=0} ->
          mex 1 = collapse); j=2 G conform v(16,20,23)=0 (options
          {stair v(15,20,22)=1, Cell_1=1, 1^v(16,19,22)=1^0=1} ->
          mex 0 = collapse); j=3 E conform v(17,20,24)=1 (options
          {stair v(16,20,23)=0, Cell_2=0, 1^v(17,19,23)=1^1=0} ->
          mex 1 = collapse); j=4 D conform v(18,20,25)=0 (options
          {stair v(17,20,24)=1, Cell_3=1, 1^v(18,19,24)=1^0=1} ->
          mex 0 = collapse); j=5 C conform v(19,20,26)=1 (the C-hand
          disturbance 1^C19(14)=1^1=0 is mex-irrelevant: options
          {0,0,0} -> mex 1 = collapse); j=6 B ENGINE 0 vs collapse
          v(20,20,27)=2 — DOWN 0v2 DEVIANT (options {stair
          v(19,20,26)=1, Cell_5=1, 1^B19(14)=1^0=1} -> mex 0);
          j=7 A ENGINE 1 vs collapse v(21,20,28)=0 — UP 1v0 DEVIANT
          (options {v(20,20,27)=2, Cell_6=0, 1^A19(14)=1^2=3} ->
          mex 1); j=8 A2 ENGINE 2 vs collapse v(22,20,29)=1 —
          UP 2v1 DEVIANT (options {v(21,20,28)=0, Cell_7=1,
          1^v(22,19,28)=0} -> mex 2); j=9..14 A3..A8 conform
          (0,1,0,1,0,1 = the collapses, the B-small disturbances
          from the j=6..8 deviant values are mex-irrelevant at each
          step; j=14's option set {0,0,0} -> mex 1 = collapse
          v(28,20,35)=1 depends only on the disclosed
          observational record fact).
          Consequences IF CONFIRMED (candidates, observation only):
          (1) the critical floor 15 = z-5 is NECESSARY at z=20 for
              the cell-ladder Sigma-collapse — with witnesses
              H(27;(6,14);20)=0 != v(20,20,27)=2,
              H(28;(7,14);20)=1 != v(21,20,28)=0,
              H(29;(8,14);20)=2 != v(22,20,29)=1 (the sub-critical
              floor-14 cell claim FAILS at z=20 as it did at z=22).
          (2) the even-z A-rank sub-critical REVIVAL is now
              value-exact 4/4 (z=16 s=10, z=18 s=12, z=20 s=14,
              z=22 s=16 — all UP 1v0 at s=z-6, never the odd-z
              s=z-5 UP 2v0 birth form).
          (3) the FULL 11-entry deviant lattice reaches cellwise
              VALUE-EXACT 4/4 across the consecutive even z
              16,18,20,22 (published z16-f10/z18-f12/z22-f16 frozen
              outputs + this kit), the s-positions the arithmetic
              set {z-6, z-4, z-2, z}.
      (ii) s in {15..27}: LATTICE IDENTITY with the published
           floor-15 census (explore_z20f15.out, commit 2cc16d34):
           at every s in {15..27} the Y-shape sets of this census
           coincide exactly with the published f15 shape sets (no
           14-token component fits below s=28), so every shared
           engine point is byte-identical by determinism; the
           deviant classes are exactly the published f15 profile —
           F {20: UP 1v0}, G {18: DOWN 0v2, 20: UP 2v1},
           E {18: UP 1v0}, D {16: DOWN 0v2, 18: UP 2v1},
           C {16: UP 1v0}, B {16: UP 2v1}, A..A8 collapsed at
           s >= 15 — and NO other deviant row in {15..27}.
      (iii) s in {28..45} (the BLIND sub-floor block: 14-token
            components enter the lattice for the first time —
            (14,14) at s=28, then (14,k) pairs from s=29, then
            (14,14,k) from s=42): candidates NO multivalue rows
            and NO new deviant classes beyond the f15 classes of
            (ii) (the published z22-f16 kit's {32..47} analog was
            empty of both).
      (iv) all cells s-only; multivalue rows 0.
  (b) tail spots: s in {46..53}, single-token shape Y=(s,), all 14
      cells; candidate 112/112 match (lattice identity with the
      published f15 tail spots, which matched 112/112).
  (c) strip sweep m in {14..19} at R=m+21: m in {15..19} are the
      PROVED T-Z20 claim positions (compliance recheck only;
      the published f15 cumulative profile 55/99/134/162/185,
      0 violations — incrementals 55/44/35/28/23 expected EXACT);
      m=14 is the OPEN m=14 row at z=20 (z*(14)=26 > 20, in-band
      for min=14 by the K1268 band formula z*(m)=2m-2+(m mod 2)):
      co-token-style arity<=4-TOTAL sweep, S in {14..53}:
      candidate 0 violations (measured count recorded whatever it
      is).
  (d) IN-BAND m=14-row record at z=20, R=35, x0 published
      residual-band style (all parts >= 14, co-token 14 allowed,
      arity <= 3 TOTAL, S in {14..52}): CROSS-ARTIFACT RECHECK of
      the published f15 kit record (62 shapes 0 separations) AND
      the published K1330 (T-Z19) published residual band m=14
      z in {20..25} first-entry datum. PLUS the arity<=4 co-token
      extension sweep (published f15 ext: 61 shapes 0 separations).
  (d2) IN-BAND m=13-row z=20 record: cross-artifact recheck of the
      published f15 record (76/0; K1328 published residual band
      m=13 z in {19..24} second entry).
  (d3) IN-BAND m=12-row z=20 record: cross-artifact recheck of the
      published f15 record (92/0; K1325 published residual band
      m=12 z in {18..21} final entry context).
  (e) strip spots m in {20..23} (lattice identity with the
      published f15 12/12 match), plus the NEW m=14 BASE SPOT
      H(35;(14,14);20) vs v(28,20,35): paper-derived candidate
      value 1, CONFORMING (derivation disclosed here before the
      first run: both B-children land at (34;(13,14);20), the
      m=13-row record position (published observational 0
      separations => v(27,20,34)=0); the C-child is
      1^H(34;(14,14);19) = 1^v(28,19,34) = 0 by the PROVED T-Z19
      m=14-row claim; the single token x=28,z=20,R=35 has options
      {0, 0} -> mex 1 = collapse). Never measured by any published
      kit (the published f15 kit measured the m=15 base spot
      H(36;(15,15);20)=0 only). This is the m=14-row base point;
      its value does not claim the row. The m=14 base-spot
      z-sequence so far: z=19: 1 (PROVED claim value), z=20: 1
      (candidate here) — no alternation yet, third datum at z=21
      pending.
  (f) below-band bottom-rung child census: the j=1 cell's B-move
      removal child is the below-band position H(21;Y;21) with
      min(Y) >= 14, swept over s in {0} U {14..45}, arity 0..4,
      against v(s,21,21). This is the FIFTH z'-7 empty-datum
      candidate of the series (child slice z'=z+1=21 with floor
      14 = z'-7; the published four consecutive below-band full
      collapses were swept at z'=17/19/20/23): candidate 0
      deviants, 0 multivalue rows. The published K1264 stair
      applicability R=21 <= 21+min(Y) suggests the collapse is a
      stair consequence at ANY floor; recorded here as a machine
      corroboration of that PROVED lemma's instance, the
      generalization belongs to the declaration lane.
  (g) TAIL SUPPLY PRE-COMPUTATIONS (pure published K0832 closed
      form, NO engine recursion), all over the EXTENDED domain
      s in {0} U {12..61} (each extended by one point from the
      published z22-f16/z23-f18 kit domains {0} U {12..60}):
      (g1) THIRTEENTH-tail identity RECHECK v(s,23,23) vs
          v(s,22,23): candidate hold {0} U {12..21}, 0v2 break at
          s=22, uniformly 2v1 for all s in {23..61}.
      (g2) FOURTEENTH-tail identity RECHECK v(s,24,24) vs
          v(s,23,24): candidate hold {0} U {12..23}, uniform 0v1
          break for all s in {24..61}.
      (g3) FIFTEENTH-tail identity RECHECK v(s,25,25) vs
          v(s,24,25): candidate hold {0} U {12..23}, 0v2 break at
          s=24, uniformly 2v1 for all s in {25..61}.
      (g4) SIXTEENTH-tail identity RECHECK v(s,26,26) vs
          v(s,25,26): candidate hold {0} U {12..25}, uniform 0v1
          break for all s in {26..61} (published NEW by the z22-f16
          kit, rechecked here extended).
      (g5) NEW SEVENTEENTH-tail PRE-COMPUTATION v(s,27,27) vs
          v(s,26,27) — the z=26-slice supply datum (registered as
          the natural next pre-computation by the published
          z22-f16 log handoff and the K1339 chain handoff): BOTH
          components predeclared. The even-k identity shape
          (published constants: k=20 z=20-supply hold {0}U{12..19}
          break 0v2@20 uniform 2v1@21+; k=22 z=22-supply hold
          {0}U{12..21} 0v2@22 2v1@23+; k=24 z=24-supply hold
          {0}U{12..23} 0v2@24 2v1@25+; even form 3/3)
          gives the candidate: hold on {0} U {12..25}, break
          0v2 at s=26, break shape UNIFORM 2v1 for ALL s in
          {27..61}; z=26-supply decides whether the even-z supply
          form graduates to 4/4; constants recorded whatever they
          are.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z20f14.out).
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
    """sweep cell_j over s in {0} U {14..smax}; returns (dev, multi, total)"""
    R = j + 21
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(14, smax + 1)):
        ys = [()] if s == 0 else parts(s, 14, 4)
        vals = {}
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            h = H(R, X, 20)
            vals.setdefault(h, []).append(y)
            total += 1
        if len(vals) > 1:
            multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s + j, 20, R)
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
             'A5', 'A6', 'A7', 'A8']
    for j in range(1, 15):
        name = names[j - 1]
        dev, multi, total = cell_sweep(j, 45)
        cells[f'cell{j}_{name}20f14'] = {
            'z': 20, 'min': j, 'R': j + 21, 'floor': 14,
            's_domain': '{0} U {14..45}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}20f14',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 15):
        nm = names[j - 1]
        for s in range(46, 54):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 21, X, 20)
            exp = v(s + j, 20, j + 21)
            tail.append({'cell': f'{nm}20f14', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s46_53', 'rows': tail})
    # (c) strip sweep m in 14..19 at R=m+21: m 15..19 are the PROVED
    #     T-Z20 claim positions (compliance recheck); m=14 is the OPEN
    #     m=14 row at z=20 (candidate 0 violations).
    sv = []
    viol = []
    cnt = 0
    for m in range(14, 20):
        H.cache_clear()
        for S in range(m, m + 40):
            for X in parts(max(S - m, 0), m, 3):
                XX = tuple(sorted((m,) + X, reverse=True))
                if sum(XX) != S:
                    continue
                hv = H(m + 21, XX, 20)
                ev = v(S, 20, m + 21)
                cnt += 1
                if hv != ev:
                    viol.append({'m': m, 'X': list(XX), 'S': S,
                                 'value': hv, 'collapse': ev})
        sv.append({'m': m, 'cumulative_shapes': cnt,
                   'cumulative_violations': len(viol)})
    out.append({'section': 'strip_z20_m14_19', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) IN-BAND m=14-row record at the z=20 m=14 row position
    #     (35; X; 20), all parts >= 14 (co-token 14 allowed), arity <= 3
    #     TOTAL. CROSS-ARTIFACT RECHECK of the published f15 kit record
    #     (62 shapes 0 seps) AND the K1330 published residual band
    #     m=14 z in {20..25} first-entry datum. Observational only.
    out.append(row_record_x0(
        'inband_m14_z20_row_record',
        'cross_artifact_recheck_of_published_f15_record_and_k1330_residual_band_m14_first_entry',
        {'co_token_14_allowed': True,
         'residual_band': 'K1330 (T-Z19) published residual band m=14 z in {20..25} (frontier z*(14)=26 per the K1268 formula z*(m)=2m-2+(m mod 2)); published f15 kit entry: 62 shapes 0 separations (recheck expected shape-for-shape)',
         's_domain': '{14..52}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        35, 20, 14, 14, 52))
    out.append(row_record(
        'inband_m14_z20_row_record_ext_arity4',
        'cross_artifact_recheck_arity_le4_extension_cotoken_style',
        {'co_token_14_allowed': True,
         's_domain': '{14..52}', 'arity_max': 4},
        35, 20, 14, 14, 52, 14))
    # (d2) IN-BAND m=13-row z=20 record: cross-artifact recheck (76/0).
    out.append(row_record_x0(
        'inband_m13_z20_row_record',
        'cross_artifact_recheck_future_k1328_residual_m13_z20_expected_76_shapes',
        {'co_token_13_allowed': True,
         'residual_band': 'K1328 published m=13 z in {19..24}; published f15 kit entry: 76 shapes 0 separations (recheck expected shape-for-shape)',
         's_domain': '{13..51}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        34, 20, 13, 13, 51))
    # (d3) IN-BAND m=12-row z=20 record: cross-artifact recheck (92/0).
    out.append(row_record_x0(
        'inband_m12_z20_row_record',
        'cross_artifact_recheck_k1325_residual_m12_z20_expected_92_shapes',
        {'co_token_12_allowed': True,
         'residual_band': 'K1325 published m=12 z in {18..21}; published f15 kit entry: 92 shapes 0 separations (recheck expected shape-for-shape)',
         's_domain': '{12..50}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        33, 20, 12, 12, 50))
    # (e) strip spots m in 20..23 (lattice identity with the published
    #     f15 12/12 match)
    spots = []
    for m in range(20, 24):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 21, X, 20)
            ev = v(S, 20, m + 21)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    out.append({'section': 'strip_spots_m20_23', 'rows': spots})
    # NEW m=14 base spot (never measured by any published kit;
    # paper-derived candidate 1 conforming, disclosed in the docstring)
    w = H(35, (14, 14), 20)
    wv = v(28, 20, 35)
    out.append({'section': 'm14_base_spot', 'X': [14, 14], 'R': 35,
                'z': 20, 'value': w, 'collapse_single': wv,
                'match': w == wv,
                'published_probe_crossref': 'NEW measurement: no published kit measured H(35;(14,14);20) (the published z20-min15 census kit measured the m=15 base spot H(36;(15,15);20)=0 only); paper-derived candidate value 1 = v(28,20,35) conforming, derivation disclosed in this file docstring before the first run (B-children on the published m=13-row z=20 record, C-child on the PROVED T-Z19 m=14-row claim)'})
    # (f) below-band bottom-rung child census: H(21;Y;21) vs v(s,21,21)
    #     with Y >= 14 (FIFTH z'-7 empty-datum candidate, floor
    #     z'-7 at z'=21)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(14, 46)):
        ys = [()] if s == 0 else parts(s, 14, 4)
        vals = {}
        for y in ys:
            h = H(21, y, 21)
            vals.setdefault(h, []).append(y)
            bb_total += 1
        if len(vals) > 1:
            bb_multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s, 21, 21)
            if val != exp:
                bb_dev.append({'s': s, 'value': val, 'collapse': exp,
                               'direction': 'UP' if val > exp else 'DOWN',
                               'shapes': len(vals[val])})
    out.append({'section': 'belowband_j1_child_H21_21',
                'label': 'observational_only_fifth_zprime7_datum_belowband_supply_source_at_z20_floor14',
                'R': 21, 'z': 21, 'floor': 14,
                's_domain': '{0} U {14..45}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (g1) THIRTEENTH-TAIL SUPPLY IDENTITY RECHECK (pure K0832)
    holds = []
    breaks = []
    for s in [0] + list(range(12, 62)):
        a = v(s, 23, 23)
        b = v(s, 22, 23)
        row = {'s': s, 'v_23_23': a, 'v_22_23': b, 'equal': a == b}
        (holds if a == b else breaks).append(row)
    out.append({'section': 'thirteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,23,23) =? v(s,22,23)',
                's_domain': '{0} U {12..61}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z20-min15 + z21-min16 + z22-min17 + z22-floor16 census kits: holds {0} U {12..21}, 0v2 break at s=22, then uniformly 2v1 for all s>=23 over s in {0} U {12..60} (both predeclared components confirmed; even-z supply form); rechecked and extended here over s in {0} U {12..61}',
                'hold_rows': holds, 'break_rows': breaks})
    # (g2) FOURTEENTH-TAIL SUPPLY IDENTITY RECHECK
    t_holds = []
    t_breaks = []
    for s in [0] + list(range(12, 62)):
        a = v(s, 24, 24)
        b = v(s, 23, 24)
        row = {'s': s, 'v_24_24': a, 'v_23_24': b, 'equal': a == b}
        (t_holds if a == b else t_breaks).append(row)
    out.append({'section': 'fourteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,24,24) =? v(s,23,24)',
                's_domain': '{0} U {12..61}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z21-min16 + z22-min17 + z22-floor16 + z23-min18 census kits: holds {0} U {12..23}, uniform 0v1 break for all s>=24 over s in {0} U {12..60} (both predeclared components confirmed; odd-z supply form); rechecked and extended here',
                'hold_rows': t_holds, 'break_rows': t_breaks})
    # (g3) FIFTEENTH-TAIL SUPPLY IDENTITY RECHECK
    p_holds = []
    p_breaks = []
    for s in [0] + list(range(12, 62)):
        a = v(s, 25, 25)
        b = v(s, 24, 25)
        row = {'s': s, 'v_25_25': a, 'v_24_25': b, 'equal': a == b}
        (p_holds if a == b else p_breaks).append(row)
    out.append({'section': 'fifteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,25,25) =? v(s,24,25)',
                's_domain': '{0} U {12..61}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z22-min17 + z22-floor16 + z23-min18 census kits: holds {0} U {12..23}, 0v2 break at s=24, uniformly 2v1 for all s in {25..60} (both predeclared components CONFIRMED; even-z supply form); rechecked and extended here',
                'hold_rows': p_holds, 'break_rows': p_breaks})
    # (g4) SIXTEENTH-TAIL SUPPLY IDENTITY RECHECK
    n_holds = []
    n_breaks = []
    for s in [0] + list(range(12, 62)):
        a = v(s, 26, 26)
        b = v(s, 25, 26)
        row = {'s': s, 'v_26_26': a, 'v_25_26': b, 'equal': a == b}
        (n_holds if a == b else n_breaks).append(row)
    out.append({'section': 'sixteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,26,26) =? v(s,25,26)',
                's_domain': '{0} U {12..61}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'published NEW by the z22-floor16 kit (hold {0} U {12..25}, UNIFORM 0v1 for ALL s in {26..60}, both components predeclared and confirmed; odd-z supply form 4/4 = the z=25 slice supply datum) and rechecked by the z23-min18 kit; rechecked and extended here over s in {0} U {12..61}',
                'hold_rows': n_holds, 'break_rows': n_breaks})
    # (g5) SEVENTEENTH-TAIL SUPPLY PRE-COMPUTATION (NEW, pure K0832)
    s_holds = []
    s_breaks = []
    for s in [0] + list(range(12, 62)):
        a = v(s, 27, 27)
        b = v(s, 26, 27)
        row = {'s': s, 'v_27_27': a, 'v_26_27': b, 'equal': a == b}
        (s_holds if a == b else s_breaks).append(row)
    out.append({'section': 'seventeenth_tail_supply_identity_precalc',
                'label': 'observational_only_new_closed_form_precalc_z26_slice_supply_k0832',
                'identity': 'v(s,27,27) =? v(s,26,27)',
                's_domain': '{0} U {12..61}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'predeclared_candidate': 'BOTH components predeclared (registered as the natural next pre-computation by the published z22-floor16 kit handoff and the K1339/K1344 chain handoffs): even-k identity shape (k=20 z=20-supply hold {0} U {12..19} 0v2@20 uniform 2v1@21+; k=22 z=22-supply hold {0} U {12..21} 0v2@22 2v1@23+; k=24 z=24-supply hold {0} U {12..23} 0v2@24 2v1@25+; even form 3/3 so far) gives the candidate hold on {0} U {12..25}, break 0v2 at s=26, break shape UNIFORM 2v1 for ALL s in {27..61}; z=26-supply decides whether the even-z supply form graduates to 4/4; constants recorded whatever they are',
                'hold_rows': s_holds, 'break_rows': s_breaks})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
