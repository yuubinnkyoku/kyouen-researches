#!/usr/bin/env python3
"""
explore_z22f16: FROZEN PRE-DECLARATION census for the z=22 FLOOR-16
(z-6, SUB-CRITICAL floor) cell ladder — the floor-necessity
exploration of the z=22 slice (the "z-6 floor unswept" open item
registered by the published K1339 completion log section 5 and the
K1339 declaration note section 5). NO K slot is claimed by this
file; the constants below were written BEFORE the first run of this
file; publish-then-execute.

Scope (this file measures and reports; it proves nothing by itself):
  (a) cell census: for each j in 1..15 the floor-16 cell
      Cell_j(s) := H(j+23; {j} U Y; 22), Y tokens >= 16, s = sum(Y) in
      {0} U {16..47}, arity(Y) in 0..4 (0 only at s=0),
      swept EXHAUSTIVELY against the published raw engine (K1138
      recursion, embedded block byte-identical to the K1282..K1339
      chain, pin bd5f22e4...). Reported per cell: deviants from the
      Sigma-collapse v(s+j,22,j+23) (K0832 closed form) and any
      multivalue (decomposition-dependence) rows. The j=15 rung (small
      token 15, one rank beyond the published z=21 A9-cell A921f16) is
      labeled A9 as a PROVISIONAL census label; final naming belongs
      to the declaration lane.

      PREDECLARED CANDIDATES (written before the first run):
      (i) THE s=16 ROW — the floor-necessity test. At the critical
          floor 17 = z-5 the s=16 classes were excluded from the
          domain (the FIFTH domain-exclusion event of the published
          f17 census); at floor 16 = z-6 they are IN-DOMAIN again
          (the z=21 slice classes C/B/A at s=16 supply through the
          C-hand). The FULL s=16 profile was derived BY HAND on
          paper BEFORE the first run of this file, from four
          published inputs: (1) the PROVED K1337 z=21 floor-16 lemma
          values — the C-hand child of Cell_j(16) is exactly the
          K1337 lemma position H(j+22;{j,16};21); (2) the published
          K1264 stair equality at R = z+min(X) EXACTLY — the
          16->15 B-hand children sit at R=j+22 = 22+j exactly and are
          conforming stair values v(j+15,22,j+22); (3) the
          small-token B-child is Cell_{j-1}(16) itself (R=j+22 =
          z+min+1, one ABOVE the stair point — the cell position);
          (4) the j=1 removal child H(23;{16};23) = v(16,23,23).
          Derived s=16 profile (15 points, single shape (j,16)):
          j=1 F conform v(17,22,24)=1; j=2 G conform v(18,22,25)=0;
          j=3 E conform v(19,22,26)=1; j=4 D conform v(20,22,27)=0;
          j=5 C conform v(21,22,28)=1 (the C-hand disturbance
          1^C21f16(16)=0 vs single 1^v(21,21,27)=3 is mex-irrelevant:
          option sets {0,0,0} vs {0,3}, both mex 1);
          j=6 B: ENGINE 0 vs collapse v(22,22,29)=2 — DOWN 0v2
          DEVIANT (options {1,1,1} vs single {0v?}: B-small
          Cell_5(16)=1 conforming, stair B v(21,22,28)=1, C-hand
          1^B21f16(16)=1^0=1; single options {v(21,22,28)=1,
          1^v(22,21,28)=0} -> mex 2; engine mex 0);
          j=7 A: ENGINE 1 vs v(23,22,30)=0 — UP 1v0 DEVIANT
          (B-small Cell_6(16)=0 the j=6 deviant value, stair B
          v(22,22,29)=2, C-hand 1^A21f16(16)=1^2=3; options {0,2,3}
          -> mex 1; single {2, 1^0=1} -> mex 0);
          j=8 A2: ENGINE 2 vs v(24,22,31)=1 — UP 2v1 DEVIANT
          (B-small Cell_7(16)=1 the j=7 deviant value, stair B
          v(23,22,30)=0, C-hand 1^A221f16(16)=1^v(24,21,30)=0;
          options {1,0,0} -> mex 2; single {0, 1^1=0} -> mex 1);
          j=9..15 A3..A9 conform (the B-small disturbances from the
          j=6..8 deviant values are mex-irrelevant at each step).
          Consequences IF CONFIRMED (candidates, to be recorded as
          observation):
          (1) the critical floor 17 = z-5 is NECESSARY at z=22 for
              the cell-ladder Sigma-collapse — the universal floor-16
              cell claim FAILS with witnesses
              H(29;(6,16);22)=0 != v(22,22,29)=2,
              H(30;(7,16);22)=1 != v(23,22,30)=0,
              H(31;(8,16);22)=2 != v(24,22,31)=1. The z-6 floor
              answers the published open item at cell level: the
              floor does NOT drop to z-6.
          (2) the even-z A-break extinction (5/5 at the critical
              floor) FAILS below the critical floor: A22f16 breaks
              at an EVEN z, at s=16=z-6 (not the odd-z s=z-5), UP
              1v0 (not UP 2v0) — the A-rank parity law is a
              critical-floor phenomenon (the first sub-critical
              observation).
          (3) the s=16 relapse station value trio
              {DOWN 0v2, UP 1v0, UP 2v1} at heads {B,A,A2} = the
              even station value trio of the published f17 stations
              {18,20,22}, at NEW heads: the FIRST sub-critical-floor
              station.
      (ii) s in {17..31} (single 2-token shapes (j,s)): LATTICE
           IDENTITY with the published floor-17 census
           (explore_z22f17.out, commit 115c0bb9; identical points,
           identical engine bytes): deviant classes exactly the
           published f17 profile — F {22: UP 1v0}, G {20: DOWN 0v2,
           22: UP 2v1}, E {20: UP 1v0}, D {18: DOWN 0v2, 20: UP 2v1},
           C {18: UP 1v0}, B {18: UP 2v1}, A..A9 collapsed at
           s >= 17. The machine cross-compare of these rows against
           the published f17 out is recorded in the predecl log.
      (iii) s in {32..47} (the first sub-floor MULTI-token shapes;
            16-token components enter the lattice for the first
            time): candidate NO multivalue rows (s-only survives
            its first sub-critical-floor test) and NO new deviant
            classes beyond (i)/(ii) — every shape conforms to the
            same s-value (the published f17 lattice had no classes
            beyond {18,20,22}).
      (iv) all cells s-only; multivalue rows 0.
  (b) tail spots: s in {48..55}, single-token shape Y=(s,), all 15
      cells; lattice identity with the published f17 tail spots
      (j in 1..15 within the f17 j in 1..16, all of which matched):
      candidate 120/120 match.
  (c) strip sweep m in {16..21} at the claim position R=m+23:
      m in {17..21} are the PROVED T-Z22 claim positions (compliance
      recheck only; published f17 cumulative 35/63/86/106/125, 0
      violations); m=16 is the OPEN m=16 ROW at z=22 (z*(16)=30 > 22,
      in-band for min=16 by the K1268 band formula): co-token-style
      arity<=4 sweep, S in {16..55}: candidate 0 violations. The
      measured constants are recorded whatever they are.
  (d) IN-BAND m=16-row record at z=22, R=39, x0 published
      residual-band style (all parts >= 16, co-token 16 allowed,
      arity <= 3 TOTAL, S in {16..54}): CROSS-ARTIFACT RECHECK of
      the published f17 kit record (40 shapes 0 separations) AND
      the candidate FIRST entry of the future T-Z21 declaration
      residual band m=16 z in {22..29} (frontier z*(16)=30; band
      pending that lane's declaration note). PLUS the arity<=4
      co-token extension sweep (published f17 ext: 39 shapes 0
      separations): candidates 0 separations, same shape counts
      (cross-artifact machine-compare against explore_z22f17.out
      recorded in the predecl log).
  (d2) IN-BAND m=15-row z=22 record: cross-artifact recheck of the
      published f17 record (50/0; future T-Z20 residual band second
      entry context unchanged).
  (d3) IN-BAND m=14-row z=22 record: cross-artifact recheck (62/0;
      K1330 published residual band third entry).
  (d4) IN-BAND m=13-row z=22 record: cross-artifact recheck (76/0;
      K1328 published residual band fourth entry).
  (e) strip spots m in {22..25} (lattice identity with the
      published f17 12/12 match), plus the NEW m=16 BASE SPOT
      H(39;(16,16);22) vs v(32,22,39): paper-derived candidate
      value 1, CONFORMING (derivation disclosed here before the
      first run: both B-children land at (38;(15,16);22), the
      m=15-row record position (published observational 0
      separations => v(31,22,38)=0); the C-child is 1^H(38;(16,16);21)
      = 1^v(32,21,38) = 0 by the PROVED T-Z21 m=16-row (z=21); the
      single token x=32,z=22,R=39 has options {v(31,22,38)=0,
      1^v(32,21,38)=0} -> mex 1; engine option set {0,0,0} -> mex 1).
      Never measured by any published kit (the published z21-min16
      census kit measured the z=21 spot H(38;(16,16);21)=1 only).
      This is the m=16-row base point; its value does not claim the
      row.
  (f) below-band bottom-rung child census: the j=1 cell's B-move
      child is the below-band position H(23;Y;23) with min(Y) >= 16,
      swept over s in {0} U {16..47}, arity 0..4, against v(s,23,23).
      This is the FIRST SUB-CRITICAL below-band datum of the series
      (child at z'=z+1=23 with floor 16 = z'-7; the published EIGHT
      consecutive below-band full collapses were all swept at the
      critical-floor pattern z'-5): candidate 0 deviants, 0
      multivalue rows. The published K1264 stair applicability
      R=23 <= 23+min(Y) suggests the collapse is a stair consequence
      at ANY floor; recorded here as observation only, the
      generalization belongs to the declaration lane.
  (g) TAIL SUPPLY PRE-COMPUTATIONS (pure published K0832 closed
      form, NO engine recursion), all over the EXTENDED domain
      s in {0} U {12..60} (each extended by one point from the
      published f17 kit domains):
      (g1) THIRTEENTH-tail identity RECHECK v(s,23,23) vs
          v(s,22,23): candidate hold {0} U {12..21}, 0v2 break at
          s=22, uniformly 2v1 for all s in {23..60}.
      (g2) FOURTEENTH-tail identity RECHECK v(s,24,24) vs
          v(s,23,24): candidate hold {0} U {12..23}, uniform 0v1
          break for all s in {24..60}.
      (g3) FIFTEENTH-tail identity RECHECK v(s,25,25) vs
          v(s,24,25) (predeclared and CONFIRMED over {0} U {12..59}
          by the published f17 kit): candidate hold {0} U {12..23},
          0v2 at s=24, uniformly 2v1 for all s in {25..60}.
      (g4) NEW SIXTEENTH-tail PRE-COMPUTATION v(s,26,26) vs
          v(s,25,26) — the z=25-slice supply datum (registered as
          the natural next pre-computation by the published f17 kit
          handoff section 5): BOTH components predeclared. The
          odd-k identity shape (k=19 z=19-supply, k=21 z=21-supply,
          k=23 z=23-supply: hold {0} U {12..k}, break start s=k+1,
          shape UNIFORM 0v1 for all s >= k+1; odd form 3/3 so far)
          gives the candidate: hold on {0} U {12..25}, break start
          s=26, break shape UNIFORM 0v1 for ALL s in {26..60};
          z=25-supply decides whether the odd-z supply form
          graduates to 4/4. Honest disclosure: the same engine-free
          datum was registered for the z=23 census lane by the
          published f17 handoff; whichever kit publishes first, the
          other's copy becomes a recheck — the constants are
          identical by construction (pure closed form, no engine).

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z22f16.out).
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
    """sweep cell_j over s in {0} U {16..smax}; returns (dev, multi, total)"""
    R = j + 23
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(16, smax + 1)):
        ys = [()] if s == 0 else parts(s, 16, 4)
        vals = {}
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            h = H(R, X, 22)
            vals.setdefault(h, []).append(y)
            total += 1
        if len(vals) > 1:
            multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s + j, 22, R)
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
        dev, multi, total = cell_sweep(j, 47)
        cells[f'cell{j}_{name}22f16'] = {
            'z': 22, 'min': j, 'R': j + 23, 'floor': 16,
            's_domain': '{0} U {16..47}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}22f16',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 16):
        nm = names[j - 1]
        for s in range(48, 56):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 23, X, 22)
            exp = v(s + j, 22, j + 23)
            tail.append({'cell': f'{nm}22f16', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s48_55', 'rows': tail})
    # (c) strip sweep m in 16..21 at R=m+23: m 17..21 are the PROVED
    #     T-Z22 claim positions (compliance recheck); m=16 is the OPEN
    #     m=16 row at z=22 (candidate 0 violations).
    sv = []
    viol = []
    cnt = 0
    for m in range(16, 22):
        H.cache_clear()
        for S in range(m, m + 40):
            for X in parts(max(S - m, 0), m, 3):
                XX = tuple(sorted((m,) + X, reverse=True))
                if sum(XX) != S:
                    continue
                hv = H(m + 23, XX, 22)
                ev = v(S, 22, m + 23)
                cnt += 1
                if hv != ev:
                    viol.append({'m': m, 'X': list(XX), 'S': S,
                                 'value': hv, 'collapse': ev})
        sv.append({'m': m, 'cumulative_shapes': cnt,
                   'cumulative_violations': len(viol)})
    out.append({'section': 'strip_z22_m16_21', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) IN-BAND m=16-row record at the z=22 m=16 row position
    #     (39; X; 22), all parts >= 16 (co-token 16 allowed), arity <= 3
    #     TOTAL. CROSS-ARTIFACT RECHECK of the published f17 kit record
    #     (40 shapes 0 seps) AND candidate FIRST entry of the future
    #     T-Z21 residual band m=16 z in {22..29}. Observational only.
    out.append(row_record_x0(
        'inband_m16_z22_row_record',
        'cross_artifact_recheck_of_published_f17_record_and_candidate_first_entry_of_future_tz21_residual_band_m16_z22',
        {'co_token_16_allowed': True,
         'residual_band': 'future T-Z21 declaration residual band m=16 z in {22..29} (frontier z*(16)=30 per the K1268 formula z*(m)=2m-2+(m mod 2), band pending that lane); published f17 kit entry: 40 shapes 0 separations (recheck expected shape-for-shape)',
         's_domain': '{16..54}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        39, 22, 16, 16, 54))
    out.append(row_record(
        'inband_m16_z22_row_record_ext_arity4',
        'cross_artifact_recheck_arity_le4_extension_cotoken_style',
        {'co_token_16_allowed': True,
         's_domain': '{16..54}', 'arity_max': 4},
        39, 22, 16, 16, 54, 16))
    # (d2) IN-BAND m=15-row z=22 record: cross-artifact recheck (50/0).
    out.append(row_record_x0(
        'inband_m15_z22_row_record',
        'cross_artifact_recheck_future_tz20_residual_m15_z22_expected_50_shapes',
        {'co_token_15_allowed': True,
         'residual_band': 'future T-Z20 residual band m=15 z in {21..28}; published f17 kit entry: 50 shapes 0 separations (recheck expected shape-for-shape)',
         's_domain': '{15..53}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        38, 22, 15, 15, 53))
    # (d3) IN-BAND m=14-row z=22 record: cross-artifact recheck (62/0).
    out.append(row_record_x0(
        'inband_m14_z22_row_record',
        'cross_artifact_recheck_k1330_residual_m14_z22_expected_62_shapes',
        {'co_token_14_allowed': True,
         'residual_band': 'K1330 published m=14 z in {20..25}; published f17 kit entry: 62 shapes 0 separations (recheck expected shape-for-shape)',
         's_domain': '{14..52}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        37, 22, 14, 14, 52))
    # (d4) IN-BAND m=13-row z=22 record: cross-artifact recheck (76/0).
    out.append(row_record_x0(
        'inband_m13_z22_row_record',
        'cross_artifact_recheck_k1328_residual_m13_z22_expected_76_shapes',
        {'co_token_13_allowed': True,
         'residual_band': 'K1328 published m=13 z in {19..24}; published f17 kit entry: 76 shapes 0 separations (recheck expected shape-for-shape)',
         's_domain': '{13..51}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        36, 22, 13, 13, 51))
    # (e) strip spots m in 22..25 (lattice identity with the published
    #     f17 12/12 match)
    spots = []
    for m in range(22, 26):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 23, X, 22)
            ev = v(S, 22, m + 23)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    out.append({'section': 'strip_spots_m22_25', 'rows': spots})
    # NEW m=16 base spot (never measured by any published kit;
    # paper-derived candidate 1 conforming, disclosed in the docstring)
    w = H(39, (16, 16), 22)
    wv = v(32, 22, 39)
    out.append({'section': 'm16_base_spot', 'X': [16, 16], 'R': 39,
                'z': 22, 'value': w, 'collapse_single': wv,
                'match': w == wv,
                'published_probe_crossref': 'NEW measurement: no published kit measured H(39;(16,16);22) (the published z21-min16 census kit measured the z=21 spot H(38;(16,16);21)=1 only); paper-derived candidate value 1 = v(32,22,39) conforming, derivation disclosed in this file docstring before the first run (B-children on the published m=15-row record, C-child on the PROVED T-Z21 m=16 row at z=21)'})
    # (f) below-band bottom-rung child census: H(23;Y;23) vs v(s,23,23)
    #     with Y >= 16 (FIRST SUB-CRITICAL below-band datum, floor
    #     z'-7 at z'=23)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(16, 48)):
        ys = [()] if s == 0 else parts(s, 16, 4)
        vals = {}
        for y in ys:
            h = H(23, y, 23)
            vals.setdefault(h, []).append(y)
            bb_total += 1
        if len(vals) > 1:
            bb_multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s, 23, 23)
            if val != exp:
                bb_dev.append({'s': s, 'value': val, 'collapse': exp,
                               'direction': 'UP' if val > exp else 'DOWN',
                               'shapes': len(vals[val])})
    out.append({'section': 'belowband_j1_child_H23_23',
                'label': 'observational_only_first_subcritical_belowband_supply_source_at_z22_floor16',
                'R': 23, 'z': 23, 'floor': 16,
                's_domain': '{0} U {16..47}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (g1) THIRTEENTH-TAIL SUPPLY IDENTITY RECHECK (pure K0832)
    holds = []
    breaks = []
    for s in [0] + list(range(12, 61)):
        a = v(s, 23, 23)
        b = v(s, 22, 23)
        row = {'s': s, 'v_23_23': a, 'v_22_23': b, 'equal': a == b}
        (holds if a == b else breaks).append(row)
    out.append({'section': 'thirteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,23,23) =? v(s,22,23)',
                's_domain': '{0} U {12..60}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z20-min15 + z21-min16 + z22-min17 census kits: holds {0} U {12..21}, 0v2 break at s=22, then uniformly 2v1 for all s>=23 over s in {0} U {12..59} (both predeclared components confirmed; even-z supply form 4/4 incl. the closed-form z=24-supply); rechecked and extended here over s in {0} U {12..60}',
                'hold_rows': holds, 'break_rows': breaks})
    # (g2) FOURTEENTH-TAIL SUPPLY IDENTITY RECHECK
    t_holds = []
    t_breaks = []
    for s in [0] + list(range(12, 61)):
        a = v(s, 24, 24)
        b = v(s, 23, 24)
        row = {'s': s, 'v_24_24': a, 'v_23_24': b, 'equal': a == b}
        (t_holds if a == b else t_breaks).append(row)
    out.append({'section': 'fourteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,24,24) =? v(s,23,24)',
                's_domain': '{0} U {12..60}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z21-min16 + z22-min17 census kits: holds {0} U {12..23}, uniform 0v1 break for all s>=24 over s in {0} U {12..59} (both predeclared components confirmed; odd-z supply form 3/3); rechecked and extended here',
                'hold_rows': t_holds, 'break_rows': t_breaks})
    # (g3) FIFTEENTH-TAIL SUPPLY IDENTITY RECHECK
    p_holds = []
    p_breaks = []
    for s in [0] + list(range(12, 61)):
        a = v(s, 25, 25)
        b = v(s, 24, 25)
        row = {'s': s, 'v_25_25': a, 'v_24_25': b, 'equal': a == b}
        (p_holds if a == b else p_breaks).append(row)
    out.append({'section': 'fifteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,25,25) =? v(s,24,25)',
                's_domain': '{0} U {12..60}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z22-min17 census kit section (g3): holds {0} U {12..23}, 0v2 break at s=24, uniformly 2v1 for all s in {25..59} (BOTH components predeclared and CONFIRMED; even-z supply form 4/4); rechecked and extended here',
                'hold_rows': p_holds, 'break_rows': p_breaks})
    # (g4) SIXTEENTH-TAIL SUPPLY PRE-COMPUTATION (NEW, pure K0832)
    n_holds = []
    n_breaks = []
    for s in [0] + list(range(12, 61)):
        a = v(s, 26, 26)
        b = v(s, 25, 26)
        row = {'s': s, 'v_26_26': a, 'v_25_26': b, 'equal': a == b}
        (n_holds if a == b else n_breaks).append(row)
    out.append({'section': 'sixteenth_tail_supply_identity_precalc',
                'label': 'observational_only_new_closed_form_precalc_z25_slice_supply_k0832',
                'identity': 'v(s,26,26) =? v(s,25,26)',
                's_domain': '{0} U {12..60}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'predeclared_candidate': 'BOTH components predeclared (registered as the natural next pre-computation by the published z22-min17 kit handoff section 5): odd-k identity shape (k=19/z=19-supply, k=21/z=21-supply, k=23/z=23-supply: hold {0} U {12..k}, break start s=k+1, shape UNIFORM 0v1 for all s>=k+1; odd form 3/3 so far) gives the candidate hold on {0} U {12..25}, break start s=26, break shape UNIFORM 0v1 for ALL s in {26..60}; z=25-supply decides whether the odd-z supply form graduates to 4/4; the same engine-free datum was registered for the z=23 census lane — constants identical by construction whichever publishes first; constants recorded whatever they are',
                'hold_rows': n_holds, 'break_rows': n_breaks})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
