#!/usr/bin/env python3
"""
explore_z21f16: FROZEN PRE-DECLARATION census for the z=21 min>=16
(floor-16) cell ladder and the T-Z21 strip (the z20-min15 census
continuation; NO K slot is claimed by this file; the constants below
were written BEFORE the first run of this file; publish-then-execute).

Scope (this file measures and reports; it proves nothing by itself):
  (a) cell census: for each j in 1..15 the floor-16 cell
      Cell_j(s) := H(j+22; {j} U Y; 21), Y tokens >= 16, s = sum(Y) in
      {0} U {16..46}, arity(Y) in 0..4 (0 only at s=0),
      swept EXHAUSTIVELY against the published raw engine (K1138
      recursion, embedded block byte-identical to the K1282..K1330
      chain, pin bd5f22e4...). Reported per cell: deviants from the
      Sigma-collapse v(s+j,21,j+22) (K0832 closed form) and any
      multivalue (decomposition-dependence) rows. The j=15 rung (small
      token 15, one rank beyond the published z=20 A8-cell A820f15) is
      prefixed A9 as a PROVISIONAL census label; final naming belongs
      to the declaration lane.

      PREDECLARED CANDIDATES (written before the first run; derived
      from the published z=19 odd profile, commit 6a6832ce, shifted +2
      in position -- the odd-z station form is 2/2 at z=17/z=19 via the
      pair law {12,14,16}@z17 / {14,16,18}@z19, and z=21 is the +2
      shift of z=19; measured constants recorded whatever they are):
      (i) deviant position set candidate {16, 18, 20} (inherited from
          z=20 per the (even, following-odd) pair rule:
          {12,14,16} shared by z16/z17, {14,16,18} by z18/z19,
          {16,18,20} by z20 and candidate z21) -- NO new exclusion and
          NO +2 shift at this odd step;
      (ii) the odd-z station triplet {DOWN:1, DOWN:0, UP:2} at the
          station positions, as the exact +2 shift of the published
          z=19 profile:
            position 16: C DOWN 1v2, B DOWN 0v1, A UP 2v0
                         (z=19: C/B/A at 14 -- the A-RANK BREAK
                         REBIRTH candidate: A deviates at s=16=z-5,
                         the z=17 (s=12)/z=19 (s=14) pattern; at even
                         z the A-break position z-5 is odd and no odd-s
                         deviant class has ever been observed);
            position 18: E DOWN 1v2, D DOWN 0v1 (z=19: E/D at 16);
            position 20: F DOWN 1v2, G DOWN 0v1, E UP 2v0
                         (z=19: F/G/E at 18);
      (iii) the F-cell TWELFTH tail odd form: DOWN 1v2 at s=20 (=z-1),
            CONFORMING HOLE at s=21 (=z, the final hold position of the
            twelfth-tail supply identity), then the persistent tail UP
            2v0 for ALL s>=22 (census window {22..46} + tail spots
            {47..54} 8/8 mismatch; z=19 analogue: DOWN@18, hole@19,
            tail 2v0@s>=20; the single@(even z)/hole-and-tail@(odd z)
            typology alternation would reach SEVEN consecutive
            consistent slices z15..z21);
      (iv) A2..A9 fully collapsed (the EIGHT consecutive full collapses
           after the A-boundary rung, matching z=19's A2..A7 pattern);
      (v) all cells s-only, multivalue rows 0.
  (b) tail spots: s in {47..54}, single-token shape Y=(s,), all 15
      cells; candidate F 8/8 mismatch, all other cells match.
  (c) strip sweep (T-Z21 claim position, PROVISIONAL label): m in
      {16..20}, S in {m..m+39}, Y parts tokens >= m, arity(Y) <= 3:
      H(m+22; X; 21) vs v(S,21,m+22). EXHAUSTIVE in-sweep; candidate
      0 violations.
  (d) IN-BAND base-child / m=15-row record (the structurally decisive
      section; observational only, NOT a T-Z21 claim position): the
      T-Z21 base m=16 a=16 child lands at (37; {15} U Y; 21) = the
      m=15-row position H(37; X; 21), and z=21 is IN BAND for min=15
      (z*(15) = 2*15-2+(15 mod 2) = 29 > 21), the SEVENTH consecutive
      slice whose base child is in-band -- the row is simultaneously
      the CANDIDATE FIRST entry of the future T-Z20 declaration lane's
      residual band m=15 z in {21..28} (frontier z*(15)=29; band
      pending that lane's declaration note). Swept: S in {15..53},
      all parts >= 15 (co-token 15 shapes INCLUDED, X[0]=15), arity <= 3,
      recorded against the Sigma-collapse v(S,21,37) with every
      separation listed, PLUS an arity<=4 co-token-style extension sweep
      (published style lesson of the z18/z19/z20 kits).
  (d2) IN-BAND m=14-row z=21 record: the SECOND entry of the K1330
      published residual band m=14 z in {20..25} (z=20 entry measured
      by the published z20-min15 census kit 62/0 + ext 61/0). SAME
      enumeration here -> same 62 shapes, cross-artifact consistency
      machine-checked.
  (d3) IN-BAND m=13-row z=21 record: the THIRD entry of the K1328
      published residual band m=13 z in {19..24} (z=19 census 76/0,
      z=20 probe + census 76/0). SAME enumeration -> same 76 shapes.
  (d4) IN-BAND m=12-row z=21 record: the FOURTH AND FINAL entry of the
      K1325 published residual band m=12 z in {18..21} (z=18 92/0,
      z=19 92/0, z=20 92/0) -- if 0 separations, the published m=12
      residual band CLOSES at its frontier z*(12)=22. SAME enumeration
      -> same 92 shapes.
  (NOT swept: the m=11-row z=21 record -- the K1322 published residual
      band m=11 z in {17..20} was CLOSED by the published z20 probe kit
      (fourth final entry 110/0 at z=20); no band entry exists at
      z=21.)
  (e) strip spots: m in {21..24}, X in {(m,m+1),(m,m+2),(m,m,m+1)},
      plus the m=16 base spot X=(16,16) at the T-Z21 slice base
      position H(38;(16,16);21) -- never measured by any published kit
      (the published beyond_z20 probe kit 0906ff21 covered z=20 rows
      m in {8..13} and z=20 spots only); candidate value 1 from the
      base-spot z-parity sequence 0(z16),1(z17),0(z18),1(z19),0(z20).
  (f) below-band bottom-rung child census (the z=21 analog of the
      K1320/K1322/K1325/K1328/z19/z20 section-(f) censuses;
      observational only): the j=1 rung's B-move child is the
      BELOW-BAND position (22; Y; 22) (min(Y) >= 16 so R=22 lies deep
      below z'+min(Y) >= 38). This section measures the z=21 child
      directly (H(22;Y;22) vs v(s,22,22), s in {0} U {16..46},
      arity(Y) in 0..4); candidate: full collapse, the SEVENTH
      consecutive below-band full collapse; the proof belongs to the
      declaration lane.
  (g) TAIL SUPPLY PRE-COMPUTATIONS (pure published K0832 closed form,
      NO engine recursion):
      (g1) TWELFTH-tail identity RECHECK (the z=21 F-cell supply
          datum): the published z20 probe kit (0906ff21, section 10)
          measured v(s,22,22)=v(s,21,22) holding on {0} U {12..21}
          with a UNIFORM 0v1 break for all s>=22 over s in {0} U
          {12..57}; the published z20-min15 census kit rechecked the
          same domain. Rechecked here over the EXTENDED domain
          s in {0} U {12..58}: candidate hold {0} U {12..21}, uniform
          0v1 for all s in {22..58} (final hold s=21 = the F hole;
          first break s=22 = the tail start).
      (g2) THIRTEENTH-tail identity RECHECK (the z=22 slice supply
          datum): the published z20-min15 census kit measured
          v(s,23,23)=v(s,22,23) holding on {0} U {12..21}, breaking
          0v2 at s=22 then uniformly 2v1 for all s>=23 over s in
          {0} U {12..57} (both predeclared components confirmed;
          even-z supply form 3/3 at z=18/z=20/z=22-supply). Rechecked
          here over the same extended domain s in {0} U {12..58}.
      (g3) FOURTEENTH-tail identity PRE-COMPUTATION (NEW, the z=23
          slice supply datum): v(s,24,24) vs v(s,23,24) over s in
          {0} U {12..58}. PREDECLARED candidate (written before the
          first run, BOTH components predeclared for the first time
          for an odd slice): odd-z supply identities (tenth tail at
          z=19: hold {0,12..19} uniform 0v1 s>=20; twelfth tail at
          z=21: hold {0,12..21} uniform 0v1 s>=22) break UNIFORMLY
          0v1 starting at s=z+1 -- so the candidate is hold on
          {0} U {12..23}, break start at s=24 (=z+1 at z=23), and
          break shape UNIFORM 0v1 for ALL s in {24..58}; z=23 decides
          whether the odd-z supply form graduates from 2/2
          (z=17-supply?; z=19, z=21) to 3/3.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z21f16.out).
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
    R = j + 22
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(16, smax + 1)):
        ys = [()] if s == 0 else parts(s, 16, 4)
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
    z19-min14 / z20-min15 kit sections (d)/(d2)/(d3)): position
    X = parts(S, m, 3) with X[0] == m, i.e. all parts >= m with
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
    for j in range(1, 16):
        name = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
                'A5', 'A6', 'A7', 'A8', 'A9'][j - 1]
        dev, multi, total = cell_sweep(j, 46)
        cells[f'cell{j}_{name}21f16'] = {
            'z': 21, 'min': j, 'R': j + 22, 'floor': 16,
            's_domain': '{0} U {16..46}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}21f16',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 16):
        nm = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
              'A5', 'A6', 'A7', 'A8', 'A9'][j - 1]
        for s in range(47, 55):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 22, X, 21)
            exp = v(s + j, 21, j + 22)
            tail.append({'cell': f'{nm}21f16', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s47_54', 'rows': tail})
    # (c) strip sweep m in 16..20 (T-Z21 claim position, provisional)
    sv = []
    viol = []
    cnt = 0
    for m in range(16, 21):
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
    out.append({'section': 'strip_z21_m16_20', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) IN-BAND base-child / m=15-row record at the z=21 m=15 row
    #     position (37; X; 21), all parts >= 15 (co-token 15 allowed),
    #     arity <= 3 TOTAL. Observational only: NOT a T-Z21 claim
    #     position. Candidate FIRST entry of the future T-Z20 residual
    #     band m=15 z in {21..28}. Published residual-band record style.
    out.append(row_record_x0(
        'inband_m15_z21_row_record',
        'observational_only_base_child_in_band_zstar15_29_gt_21_seventh_consecutive',
        {'co_token_15_allowed': True,
         'residual_band': 'CANDIDATE first entry of the future T-Z20 declaration residual band m=15 z in {21..28} (frontier z*(15)=29; band pending that lane; per the K1268 formula z*(m)=2m-2+(m mod 2))',
         's_domain': '{15..53}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        37, 21, 15, 15, 53))
    out.append(row_record(
        'inband_m15_z21_row_record_ext_arity4',
        'observational_only_arity_le4_extension_of_the_m15_z21_record_cotoken_style',
        {'co_token_15_allowed': True,
         's_domain': '{15..53}', 'arity_max': 4},
        37, 21, 15, 15, 53, 15))
    # (d2) IN-BAND m=14-row z=21 record: SECOND entry of the K1330
    #      published residual m=14 z in {20..25}, published record
    #      style (z=20 entry (z20-min15 census kit) 62/0 + ext 61/0).
    #      Cross-artifact consistency recheck.
    out.append(row_record_x0(
        'inband_m14_z21_row_record',
        'observational_only_k1330_residual_m14_z21_second_entry_zstar14_26_gt_21_cross_artifact_recheck',
        {'co_token_14_allowed': True,
         'residual_band': 'K1330 published m=14 z in {20..25}; z=20 entry (z20-min15 census kit) 62 shapes 0 seps + arity<=4 ext 61/0; same enumeration -> same 62 shapes here',
         's_domain': '{14..52}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        36, 21, 14, 14, 52))
    # (d3) IN-BAND m=13-row z=21 record: THIRD entry of the K1328
    #      published residual m=13 z in {19..24}, published record
    #      style (76/0 at z=19, z=20, z=20-census).
    out.append(row_record_x0(
        'inband_m13_z21_row_record',
        'observational_only_k1328_residual_m13_z21_third_entry_zstar13_25_gt_21_cross_artifact_recheck',
        {'co_token_13_allowed': True,
         'residual_band': 'K1328 published m=13 z in {19..24}; z=19 (z19-min14 census kit) 76/0; z=20 (z20 probe kit + z20-min15 census kit) 76/0 + ext 75/0; same enumeration -> same 76 shapes here',
         's_domain': '{13..51}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        35, 21, 13, 13, 51))
    # (d4) IN-BAND m=12-row z=21 record: FOURTH AND FINAL entry of the
    #      K1325 published residual m=12 z in {18..21} (92/0 at z=18,
    #      z=19, z=20). If 0 separations, the published m=12 residual
    #      band CLOSES at its frontier z*(12)=22.
    out.append(row_record_x0(
        'inband_m12_z21_row_record',
        'observational_only_k1325_residual_m12_z21_fourth_final_entry_zstar12_22_gt_21_band_closes_if_0_seps',
        {'co_token_12_allowed': True,
         'residual_band': 'K1325 published m=12 z in {18..21}; z=18 (z18-min13 kit) 92/0; z=19 (z19-min14 census kit) 92/0; z=20 (z20 probe kit + z20-min15 census kit) 92/0; same enumeration -> same 92 shapes here; FOURTH AND FINAL entry (frontier z*(12)=22)',
         's_domain': '{12..50}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        34, 21, 12, 12, 50))
    # (e) strip spots m in 21..24
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
    # m=16 base spot (S=32, both 16-tokens) at the T-Z21 slice base
    # position
    w = H(38, (16, 16), 21)
    wv = v(32, 21, 38)
    out.append({'section': 'm16_base_spot', 'X': [16, 16], 'R': 38,
                'z': 21, 'value': w, 'collapse_single': wv,
                'match': w == wv,
                'published_probe_crossref': 'NEW measurement: no published kit measured H(38;(16,16);21) (the published beyond_z20 probe kit 0906ff21 covered z=20 rows m in {8..13} and z=20 spots only); candidate 1 from the base-spot z-parity sequence 0(z16),1(z17),0(z18),1(z19),0(z20)'})
    # (f) below-band bottom-rung child census: H(22; Y; 22) vs v(s,22,22)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(16, 47)):
        ys = [()] if s == 0 else parts(s, 16, 4)
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
                'label': 'observational_only_belowband_supply_source_at_z21',
                'R': 22, 'z': 22, 'floor': 16,
                's_domain': '{0} U {16..46}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (g1) TWELFTH-TAIL SUPPLY IDENTITY RECHECK (pure K0832 closed form)
    holds = []
    breaks = []
    for s in [0] + list(range(12, 59)):
        a = v(s, 22, 22)
        b = v(s, 21, 22)
        row = {'s': s, 'v_22_22': a, 'v_21_22': b, 'equal': a == b}
        (holds if a == b else breaks).append(row)
    out.append({'section': 'twelfth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,22,22) =? v(s,21,22)',
                's_domain': '{0} U {12..58}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'beyond_z20 kit section (10) + z20-min15 census kit section (g2): holds {0} U {12..21}, uniform 0v1 break for all s>=22 over s in {0} U {12..57} (predeclared odd-z candidate confirmed); rechecked and extended here over s in {0} U {12..58} - the z=21 F-cell supply datum (final hold s=21 = the F hole; first break s=22 = the tail start)',
                'hold_rows': holds, 'break_rows': breaks})
    # (g2) THIRTEENTH-TAIL SUPPLY IDENTITY RECHECK (published anchor)
    t_holds = []
    t_breaks = []
    for s in [0] + list(range(12, 59)):
        a = v(s, 23, 23)
        b = v(s, 22, 23)
        row = {'s': s, 'v_23_23': a, 'v_22_23': b, 'equal': a == b}
        (t_holds if a == b else t_breaks).append(row)
    out.append({'section': 'thirteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,23,23) =? v(s,22,23)',
                's_domain': '{0} U {12..58}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z20-min15 census kit section (g3): holds {0} U {12..21}, breaks at s=22 as 0v2, then uniformly 2v1 for all s>=23 over s in {0} U {12..57} (both predeclared components confirmed; even-z supply form 3/3 at z=18/z=20/z=22-supply); rechecked and extended here',
                'hold_rows': t_holds, 'break_rows': t_breaks})
    # (g3) FOURTEENTH-TAIL SUPPLY PRE-COMPUTATION (NEW, pure K0832)
    n_holds = []
    n_breaks = []
    for s in [0] + list(range(12, 59)):
        a = v(s, 24, 24)
        b = v(s, 23, 24)
        row = {'s': s, 'v_24_24': a, 'v_23_24': b, 'equal': a == b}
        (n_holds if a == b else n_breaks).append(row)
    out.append({'section': 'fourteenth_tail_supply_identity_precalc',
                'label': 'observational_only_new_closed_form_precalc_z23_slice_supply_k0832',
                'identity': 'v(s,24,24) =? v(s,23,24)',
                's_domain': '{0} U {12..58}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'predeclared_candidate': 'BOTH components predeclared for the first time for an odd slice: odd-z supply identities break starting at s=z+1 with shape UNIFORM 0v1 (tenth tail z=19: hold {0,12..19} uniform 0v1 s>=20; twelfth tail z=21: hold {0,12..21} uniform 0v1 s>=22) - so the candidate is hold on {0} U {12..23}, break start s=24 (=z+1 at z=23), break shape UNIFORM 0v1 for ALL s in {24..58}; z=23 decides whether the odd-z supply form graduates from 2/2 (z=19, z=21) to 3/3; constants recorded whatever they are',
                'hold_rows': n_holds, 'break_rows': n_breaks})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()

