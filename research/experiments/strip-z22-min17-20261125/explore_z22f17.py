#!/usr/bin/env python3
"""
explore_z22f17: FROZEN PRE-DECLARATION census for the z=22 min>=17
(floor-17) cell ladder and the T-Z22 strip (the z21-min16 census
continuation; NO K slot is claimed by this file; the constants below
were written BEFORE the first run of this file; publish-then-execute).

Scope (this file measures and reports; it proves nothing by itself):
  (a) cell census: for each j in 1..16 the floor-17 cell
      Cell_j(s) := H(j+23; {j} U Y; 22), Y tokens >= 17, s = sum(Y) in
      {0} U {17..47}, arity(Y) in 0..4 (0 only at s=0),
      swept EXHAUSTIVELY against the published raw engine (K1138
      recursion, embedded block byte-identical to the K1282..K1331
      chain, pin bd5f22e4...). Reported per cell: deviants from the
      Sigma-collapse v(s+j,22,j+23) (K0832 closed form) and any
      multivalue (decomposition-dependence) rows. The j=16 rung (small
      token 16, one rank beyond the published z=21 A9-cell A921f16) is
      prefixed A10 as a PROVISIONAL census label; final naming belongs
      to the declaration lane.

      PREDECLARED CANDIDATES (written before the first run; derived
      from the published z=20 EVEN profile, commit 2cc16d34, shifted +2
      in position per the (even, following-odd) pair-rule chain; the
      FULL per-cell deviant list is written below so that nothing can
      be silently discovered and re-narrated -- lesson of the honest
      disclosure of the z21 C-cell second deviant; measured constants
      recorded whatever they are):
      (i) deviant position set candidate {18, 20, 22}: inherited from
          z=21's measured {16, 18, 20} by the +2 step, with the
          position-16 classes (the z=21 odd triplet C DOWN 1v2 /
          B DOWN 0v1 at 16 and the A-rank break rebirth A UP 2v0 at
          s=16=z-5) falling BELOW the floor-17 domain -- the FIFTH
          domain-exclusion event (the position-16 classes cannot
          occur since s >= 17);
      (ii) the FULL predeclared per-cell deviant lists (the exact +2
           shift of the published z=20 profile):
             F22f17: {22: UP 1v0}                       (single point at
                                                       s=22=z, even
                                                       form, NO tail);
             G22f17: {20: DOWN 0v2, 22: UP 2v1};
             E22f17: {20: UP 1v0};
             D22f17: {18: DOWN 0v2, 20: UP 2v1};
             C22f17: {18: UP 1v0};
             B22f17: {18: UP 2v1};
             A..A10: fully collapsed (10 rungs; at even z the A-break
                     position z-5=17 is an odd s and no odd-s A-rank
                     deviant class has ever been observed -- the
                     A-break extinction/rebirth alternation continues:
                     extinct at z=20, reborn at z=21 (s=16), candidate
                     extinct again at z=22);
      (iii) the F-cell single@(even z) typology: F deviates ONLY at
            s=22 (=z) as UP 1v0 and CONFORMS for ALL s in
            {23..47} U {48..55} (no hole, no persistent tail; the
            single@(even z)/hole-and-tail@(odd z) typology
            alternation would reach EIGHT consecutive consistent
            slices z15..z22);
      (iv) A2..A10 fully collapsed (the NINE consecutive full collapses
           after the A-boundary rung, extending the z=19 z=20 z=21
           A2..A9 pattern);
      (v) all cells s-only, multivalue rows 0.
  (b) tail spots: s in {48..55}, single-token shape Y=(s,), all 16
      cells; candidate: ALL match (even z -- no F tail form).
  (c) strip sweep (T-Z22 claim position, PROVISIONAL label): m in
      {17..21}, S in {m..m+39}, Y parts tokens >= m, arity(Y) <= 3:
      H(m+23; X; 22) vs v(S,22,m+23). EXHAUSTIVE in-sweep; candidate
      0 violations.
  (d) IN-BAND base-child / m=16-row record (the structurally decisive
      section; observational only, NOT a T-Z22 claim position): the
      T-Z22 base m=17 a=17 child lands at (39; {16} U Y; 22) = the
      m=16-row position H(39; X; 22), and z=22 is IN BAND for min=16
      (z*(16) = 2*16-2+(16 mod 2) = 30 > 22), the EIGHTH consecutive
      slice whose base child is in-band -- the row is simultaneously
      the CANDIDATE FIRST entry of the future T-Z21 declaration lane's
      residual band m=16 z in {22..29} (frontier z*(16)=30; band
      pending that lane's declaration note). Swept: S in {16..54},
      all parts >= 16 (co-token 16 shapes INCLUDED, X[0]=16), arity <= 3,
      recorded against the Sigma-collapse v(S,22,39) with every
      separation listed, PLUS an arity<=4 co-token-style extension sweep
      (published style lesson of the z18/z19/z20/z21 kits).
  (d2) IN-BAND m=15-row z=22 record: the SECOND entry of the future
      T-Z20 residual band m=15 z in {21..28} (z=21 entry measured by
      the published z21-min16 census kit 50/0 + ext 49/0). SAME
      enumeration here -> same 50 shapes, cross-artifact consistency
      machine-checked.
  (d3) IN-BAND m=14-row z=22 record: the THIRD entry of the K1330
      published residual band m=14 z in {20..25} (z=20 census 62/0,
      z=21 census 62/0). SAME enumeration -> same 62 shapes.
  (d4) IN-BAND m=13-row z=22 record: the FOURTH entry of the K1328
      published residual band m=13 z in {19..24} (z=19 76/0, z=20
      76/0, z=21 76/0). SAME enumeration -> same 76 shapes.
  (NOT swept: the m=12-row z=22 record -- the K1325 published residual
      band m=12 z in {18..21} was CLOSED by the published z21-min16
      census kit (fourth final entry 92/0 at z=21); no band entry
      exists at z=22.)
  (e) strip spots: m in {22..25}, X in {(m,m+1),(m,m+2),(m,m,m+1)},
      plus the m=17 base spot X=(17,17) at the T-Z22 slice base
      position H(40;(17,17);22) -- never measured by any published kit
      (the published z21-min16 census kit measured the z=21 spot only);
      candidate value 0 from the base-spot z-parity sequence
      0(z16),1(z17),0(z18),1(z19),0(z20),1(z21) -- the SEVENTH point.
  (f) below-band bottom-rung child census (the z=22 analog of the
      K1320/K1322/K1325/K1328/z19/z20/z21 section-(f) censuses;
      observational only): the j=1 rung's B-move child is the
      BELOW-BAND position (23; Y; 23) (min(Y) >= 17 so R=23 lies deep
      below z'+min(Y) >= 40). This section measures the z=22 child
      directly (H(23;Y;23) vs v(s,23,23), s in {0} U {17..47},
      arity(Y) in 0..4); candidate: full collapse, the EIGHTH
      consecutive below-band full collapse; the proof belongs to the
      declaration lane.
  (g) TAIL SUPPLY PRE-COMPUTATIONS (pure published K0832 closed form,
      NO engine recursion):
      (g1) THIRTEENTH-tail identity RECHECK (the z=22 slice supply
          datum): the published z20-min15 census kit measured
          v(s,23,23)=v(s,22,23) holding on {0} U {12..21}, breaking
          0v2 at s=22 then uniformly 2v1 for all s>=23 over s in
          {0} U {12..57}, and the published z21-min16 census kit
          rechecked and extended it over {0} U {12..58} (both
          predeclared components confirmed; even-z supply form 3/3 at
          z=18/z=20/z=22-supply). Rechecked here over the EXTENDED
          domain s in {0} U {12..59}: candidate hold {0} U {12..21},
          0v2 at s=22, uniform 2v1 for all s in {23..59}.
      (g2) FOURTEENTH-tail identity RECHECK (the z=23 slice supply
          datum): the published z21-min16 census kit measured
          v(s,24,24)=v(s,23,24) holding on
          {0} U {12..23} with a UNIFORM 0v1 break for all s>=24 over
          s in {0} U {12..58} (both predeclared components confirmed;
          the odd-z supply form graduated to 3/3 at z=19/z=21/z=23).
          Rechecked here over the extended domain s in {0} U
          {12..59}: candidate hold {0} U {12..23}, uniform 0v1 for all
          s in {24..59}.
      (g3) FIFTEENTH-tail identity PRE-COMPUTATION (NEW, the z=24
          slice supply datum): v(s,25,25) vs v(s,24,25) over s in
          {0} U {12..59}. PREDECLARED candidate (written before the
          first run, BOTH components predeclared for the second time
          overall, first time for an even slice): even-z supply
          identities (twelfth tail at z=20-supply: hold {0,12..19},
          0v2@20, uniform 2v1 s>=21; thirteenth tail at z=22-supply:
          hold {0,12..21}, 0v2@22, uniform 2v1 s>=23) break as 0v2 at
          s=z then uniformly 2v1 -- so the candidate is hold on
          {0} U {12..23}, break start at s=24 (=z at z=24) as 0v2, and
          break shape UNIFORM 2v1 for ALL s in {25..59}; z=24 decides
          whether the even-z supply form graduates from 3/3
          (z=18, z=20, z=22) to 4/4.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z22f17.out).
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
    R = j + 23
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(17, smax + 1)):
        ys = [()] if s == 0 else parts(s, 17, 4)
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
    """frontier/beyond parameter style sweep: X = (m,) U parts >= min_tok.

    This is the published frontier-record enumeration form (z14pre
    section (d) / z16-min9 section (e): arity up to 4 total tokens,
    co-token m possible).
    """
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
    """published residual-band record style (z17-min12 / z18-min13 /
    z19-min14 / z20-min15 / z21-min16 kit sections (d)/(d2)/(d3)):
    position X = parts(S, m, 3) with X[0] == m, i.e. all parts >= m with
    co-token m allowed, arity <= 3 TOTAL. Shape-for-shape comparable
    with the published entries."""
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
    for j in range(1, 17):
        name = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
                'A5', 'A6', 'A7', 'A8', 'A9', 'A10'][j - 1]
        dev, multi, total = cell_sweep(j, 47)
        cells[f'cell{j}_{name}22f17'] = {
            'z': 22, 'min': j, 'R': j + 23, 'floor': 17,
            's_domain': '{0} U {17..47}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}22f17',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 17):
        nm = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
              'A5', 'A6', 'A7', 'A8', 'A9', 'A10'][j - 1]
        for s in range(48, 56):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 23, X, 22)
            exp = v(s + j, 22, j + 23)
            tail.append({'cell': f'{nm}22f17', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s48_55', 'rows': tail})
    # (c) strip sweep m in 17..21 (T-Z22 claim position, provisional)
    sv = []
    viol = []
    cnt = 0
    for m in range(17, 22):
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
    out.append({'section': 'strip_z22_m17_21', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) IN-BAND base-child / m=16-row record at the z=22 m=16 row
    #     position (39; X; 22), all parts >= 16 (co-token 16 allowed),
    #     arity <= 3 TOTAL. Observational only: NOT a T-Z22 claim
    #     position. Candidate FIRST entry of the future T-Z21 residual
    #     band m=16 z in {22..29}. Published residual-band record style.
    out.append(row_record_x0(
        'inband_m16_z22_row_record',
        'observational_only_base_child_in_band_zstar16_30_gt_22_eighth_consecutive',
        {'co_token_16_allowed': True,
         'residual_band': 'CANDIDATE first entry of the future T-Z21 declaration residual band m=16 z in {22..29} (frontier z*(16)=30; band pending that lane; per the K1268 formula z*(m)=2m-2+(m mod 2)); the row is simultaneously the T-Z22 base m=17 a=17 child, the EIGHTH consecutive in-band base child',
         's_domain': '{16..54}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        39, 22, 16, 16, 54))
    out.append(row_record(
        'inband_m16_z22_row_record_ext_arity4',
        'observational_only_arity_le4_extension_of_the_m16_z22_record_cotoken_style',
        {'co_token_16_allowed': True,
         's_domain': '{16..54}', 'arity_max': 4},
        39, 22, 16, 16, 54, 16))
    # (d2) IN-BAND m=15-row z=22 record: SECOND entry of the future
    #      T-Z20 residual band m=15 z in {21..28}, published record
    #      style (z=21 entry (z21-min16 census kit) 50/0 + ext 49/0).
    #      Cross-artifact consistency recheck.
    out.append(row_record_x0(
        'inband_m15_z22_row_record',
        'observational_only_future_tz20_residual_m15_z22_second_entry_zstar15_29_gt_22_cross_artifact_recheck',
        {'co_token_15_allowed': True,
         'residual_band': 'future T-Z20 residual band m=15 z in {21..28}; z=21 entry (z21-min16 census kit) 50 shapes 0 seps + arity<=4 ext 49/0; same enumeration -> same 50 shapes here',
         's_domain': '{15..53}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        38, 22, 15, 15, 53))
    # (d3) IN-BAND m=14-row z=22 record: THIRD entry of the K1330
    #      published residual m=14 z in {20..25}, published record
    #      style (z=20 62/0, z=21 62/0).
    out.append(row_record_x0(
        'inband_m14_z22_row_record',
        'observational_only_k1330_residual_m14_z22_third_entry_zstar14_26_gt_22_cross_artifact_recheck',
        {'co_token_14_allowed': True,
         'residual_band': 'K1330 published m=14 z in {20..25}; z=20 (z20-min15 census kit) 62/0; z=21 (z21-min16 census kit) 62/0; same enumeration -> same 62 shapes here',
         's_domain': '{14..52}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        37, 22, 14, 14, 52))
    # (d4) IN-BAND m=13-row z=22 record: FOURTH entry of the K1328
    #      published residual m=13 z in {19..24}, published record
    #      style (76/0 at z=19, z=20, z=21).
    out.append(row_record_x0(
        'inband_m13_z22_row_record',
        'observational_only_k1328_residual_m13_z22_fourth_entry_zstar13_25_gt_22_cross_artifact_recheck',
        {'co_token_13_allowed': True,
         'residual_band': 'K1328 published m=13 z in {19..24}; z=19 (z19-min14 census kit) 76/0; z=20 (z20 probe kit + z20-min15 census kit) 76/0 + ext 75/0; z=21 (z21-min16 census kit) 76/0; same enumeration -> same 76 shapes here',
         's_domain': '{13..51}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        36, 22, 13, 13, 51))
    # (e) strip spots m in 22..25
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
    # m=17 base spot (S=34, both 17-tokens) at the T-Z22 slice base
    # position
    w = H(40, (17, 17), 22)
    wv = v(34, 22, 40)
    out.append({'section': 'm17_base_spot', 'X': [17, 17], 'R': 40,
                'z': 22, 'value': w, 'collapse_single': wv,
                'match': w == wv,
                'published_probe_crossref': 'NEW measurement: no published kit measured H(40;(17,17);22) (the published z21-min16 census kit measured the z=21 spot H(38;(16,16);21)=1 only); candidate 0 from the base-spot z-parity sequence 0(z16),1(z17),0(z18),1(z19),0(z20),1(z21)'})
    # (f) below-band bottom-rung child census: H(23; Y; 23) vs v(s,23,23)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(17, 48)):
        ys = [()] if s == 0 else parts(s, 17, 4)
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
                'label': 'observational_only_belowband_supply_source_at_z22',
                'R': 23, 'z': 23, 'floor': 17,
                's_domain': '{0} U {17..47}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (g1) THIRTEENTH-TAIL SUPPLY IDENTITY RECHECK (pure K0832 closed form)
    holds = []
    breaks = []
    for s in [0] + list(range(12, 60)):
        a = v(s, 23, 23)
        b = v(s, 22, 23)
        row = {'s': s, 'v_23_23': a, 'v_22_23': b, 'equal': a == b}
        (holds if a == b else breaks).append(row)
    out.append({'section': 'thirteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,23,23) =? v(s,22,23)',
                's_domain': '{0} U {12..59}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z20-min15 census kit section (g3) + z21-min16 census kit section (g2): holds {0} U {12..21}, 0v2 break at s=22, then uniformly 2v1 for all s>=23 over s in {0} U {12..58} (both predeclared components confirmed; even-z supply form 3/3 at z=18/z=20/z=22-supply); rechecked and extended here over s in {0} U {12..59}',
                'hold_rows': holds, 'break_rows': breaks})
    # (g2) FOURTEENTH-TAIL SUPPLY IDENTITY RECHECK (published anchor)
    t_holds = []
    t_breaks = []
    for s in [0] + list(range(12, 60)):
        a = v(s, 24, 24)
        b = v(s, 23, 24)
        row = {'s': s, 'v_24_24': a, 'v_23_24': b, 'equal': a == b}
        (t_holds if a == b else t_breaks).append(row)
    out.append({'section': 'fourteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,24,24) =? v(s,23,24)',
                's_domain': '{0} U {12..59}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z21-min16 census kit section (g3): holds {0} U {12..23}, uniform 0v1 break for all s>=24 over s in {0} U {12..58} (both predeclared components confirmed; the odd-z supply form graduated to 3/3 at z=19/z=21/z=23); rechecked and extended here',
                'hold_rows': t_holds, 'break_rows': t_breaks})
    # (g3) FIFTEENTH-TAIL SUPPLY PRE-COMPUTATION (NEW, pure K0832)
    n_holds = []
    n_breaks = []
    for s in [0] + list(range(12, 60)):
        a = v(s, 25, 25)
        b = v(s, 24, 25)
        row = {'s': s, 'v_25_25': a, 'v_24_25': b, 'equal': a == b}
        (n_holds if a == b else n_breaks).append(row)
    out.append({'section': 'fifteenth_tail_supply_identity_precalc',
                'label': 'observational_only_new_closed_form_precalc_z24_slice_supply_k0832',
                'identity': 'v(s,25,25) =? v(s,24,25)',
                's_domain': '{0} U {12..59}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'predeclared_candidate': 'BOTH components predeclared for the first time for an even slice: even-z supply identities (z=20-supply: hold {0,12..19}, 0v2@20, uniform 2v1 s>=21; z=22-supply: hold {0,12..21}, 0v2@22, uniform 2v1 s>=23) break as 0v2 at s=z then UNIFORMLY 2v1 - so the candidate is hold on {0} U {12..23}, break at s=24 (=z at z=24) as 0v2, then break shape UNIFORM 2v1 for ALL s in {25..59}; z=24 decides whether the even-z supply form graduates from 3/3 (z=18, z=20, z=22) to 4/4; constants recorded whatever they are',
                'hold_rows': n_holds, 'break_rows': n_breaks})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
