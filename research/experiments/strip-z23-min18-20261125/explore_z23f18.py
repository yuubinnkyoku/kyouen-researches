#!/usr/bin/env python3
"""
explore_z23f18: FROZEN PRE-DECLARATION census for the z=23 min>=18
(floor-18) cell ladder and the T-Z23 strip (the z22-min17 census
continuation; NO K slot is claimed by this file; the constants below
were written BEFORE the first run of this file; publish-then-execute).

Scope (this file measures and reports; it proves nothing by itself):
  (a) cell census: for each j in 1..17 the floor-18 cell
      Cell_j(s) := H(j+24; {j} U Y; 23), Y tokens >= 18, s = sum(Y) in
      {0} U {18..48}, arity(Y) in 0..4 (0 only at s=0),
      swept EXHAUSTIVELY against the published raw engine (K1138
      recursion, embedded block byte-identical to the K1282..K1331
      chain, pin bd5f22e4...). Reported per cell: deviants from the
      Sigma-collapse v(s+j,23,j+24) (K0832 closed form) and any
      multivalue (decomposition-dependence) rows. The j=17 rung (small
      token 17, one rank beyond the published z=22 A10-cell A1022f17)
      is prefixed A11 as a PROVISIONAL census label; final naming
      belongs to the declaration lane.

      PREDECLARED CANDIDATES (written before the first run; derived
      from the published z=21 ODD profile (the declared K1337 cell
      lemmas F21f16..A921f16) shifted +2 in position AND +2 in the
      ladder budget -- the (even, following-odd) pair-rule chain and
      the odd->odd two-step station profile; the FULL per-cell deviant
      list is written below so that nothing can be silently discovered
      and re-narrated -- lesson of the honest disclosure of the z21
      C-cell second deviant; measured constants recorded whatever
      they are):
      (i) deviant position set candidate {18, 20, 22}: inherited from
          z=22's measured {18, 20, 22} UNCHANGED (the pair-rule test:
          the (even, following-odd) pair z=22/z=23 graduates to 4/4
          if the position set is carried without loss), with NO
          definition-domain exclusion event -- z=22's classes at
          {18, 20, 22} all survive the floor-17 -> floor-18 raise,
          the THIRD consecutive non-exclusion on the even->odd steps
          (z=18 -> 19, z=20 -> 21, z=22 -> 23), in contrast with the
          odd->even steps (z=19 -> 20, z=21 -> 22) which killed the
          oldest z-relative class each time;
      (ii) the FULL predeclared per-cell deviant lists (the exact
           +2 shift of the published z=21 odd profile):
             F23f18: {22: DOWN 1v2} plus s=23 the HOLE (a CONFORMING
                     mirror-0 point, the odd-form hole at s=z) plus
                     the persistent tail s>=24: UP 2v0; this is the
                     FOURTEENTH tail form (odd-z HOLE+TAIL, the
                     z-relative profile IDENTICAL to z=15/z=17/z=19/
                     z=21);
             G23f18: {22: DOWN 0v1};
             E23f18: {20: DOWN 1v2, 22: UP 2v0};
             D23f18: {20: DOWN 0v1};
             C23f18: {18: DOWN 1v2, 20: UP 2v0};
             B23f18: {18: DOWN 0v1};
             A..A11: A23f18 {18: UP 2v0} -- the A-RANK BREAK REBIRTH
                     at s=18=z-5 (an EVEN s at an odd z; the odd-z
                     birth sequence candidate 4/4: z=17 s=12, z=19
                     s=14, z=21 s=16, z=23 s=18, all UP 2v0, the
                     birth position z-5 always even);
                     A223f18..A1123f18 fully collapsed (10 rungs);
      (iii) the station structure: {C,B,A}@18 = {DOWN 1v2, DOWN 0v1,
            UP 2v0}, {E,D,C}@20 = {DOWN 1v2, DOWN 0v1, UP 2v0},
            {F,G,E}@22 = {DOWN 1v2, DOWN 0v1, UP 2v0} -- the odd-form
            station triplet {DOWN:1, DOWN:0, UP:2}, candidate 4/4
            at z=17/z=19/z=21/z=23 (the exact two-step successor of
            the published z=21 stations {C,B,A}@16/{E,D,C}@18/
            {F,G,E}@20);
      (iv) the F-cell hole+tail@(odd z) typology: F deviates at
           s=22 (=z-1) DOWN 1v2, CONFORMS at the HOLE s=23 (=z,
           mirror 0), and carries the persistent tail UP 2v0 for ALL
           s >= 24; the single@(even z)/hole-and-tail@(odd z) typology
           alternation would reach NINE consecutive consistent slices
           z15..z23 (odd-z form candidate 5/5);
      (v) A2..A11 fully collapsed (the TEN consecutive full collapses
          after the A-boundary rung, extending the z=19..z=22
          A2..A10 pattern); A1123f18 (small token 17,
          z*(17)=2*17-2+1=33 > 23) is the candidate NINTH
          consecutive in-band base child;
      (vi) all cells s-only, multivalue rows 0.
  (b) tail spots: s in {49..56}, single-token shape Y=(s,), all 17
      cells; candidate: the 8 F-cell spots MISMATCH UP 2 (the
      odd-form tail signature; contrast z=22's 128/128 all-match),
      all other 9x8 spots match.
  (c) strip sweep (T-Z23 claim position, PROVISIONAL label): m in
      {18..22}, S in {m..m+39}, Y parts tokens >= m, arity(Y) <= 3:
      H(m+24; X; 23) vs v(S,23,m+24). EXHAUSTIVE in-sweep; candidate
      0 violations.
  (d) IN-BAND base-child / m=17-row record (the structurally decisive
      section; observational only, NOT a T-Z23 claim position): the
      T-Z23 base m=18 a=18 child lands at (41; {17} U Y; 23) = the
      m=17-row position H(41; X; 23), and z=23 is IN BAND for min=17
      (z*(17) = 2*17-2+(17 mod 2) = 33 > 23), the NINTH consecutive
      slice whose base child is in-band -- the row is simultaneously
      the CANDIDATE FIRST entry of the future T-Z22 declaration lane's
      residual band m=17 z in {23..32} (frontier z*(17)=33; band
      pending that lane's declaration note). Swept: S in {17..55},
      all parts >= 17 (co-token 17 shapes INCLUDED, X[0]=17), arity <= 3,
      recorded against the Sigma-collapse v(S,23,41) with every
      separation listed, PLUS an arity<=4 co-token-style extension sweep
      (published style lesson of the z18/z19/z20/z21/z22 kits).
  (d2) IN-BAND m=16-row z=23 record: the SECOND entry of the future
      T-Z21 residual band m=16 z in {22..29} (z=22 entry measured by
      the published z22-min17 census kit 40/0 + ext 39/0). SAME
      enumeration here -> same 40 shapes, cross-artifact consistency
      machine-checked.
  (d3) IN-BAND m=15-row z=23 record: the THIRD entry of the future
      T-Z20 residual band m=15 z in {21..28} (z=21 entry (z21-min16
      census kit) 50/0 + ext 49/0; z=22 entry 50/0). SAME enumeration
      -> same 50 shapes.
  (d4) IN-BAND m=14-row z=23 record: the FOURTH entry of the K1330
      published residual band m=14 z in {20..25} (z=20 62/0, z=21
      62/0, z=22 62/0). SAME enumeration -> same 62 shapes.
  (d5) IN-BAND m=13-row z=23 record: the FIFTH entry of the K1328
      published residual band m=13 z in {19..24} (z=19 76/0, z=20
      76/0, z=21 76/0, z=22 76/0). SAME enumeration -> same 76
      shapes.
  (NOT swept: the m=12-row z=23 record -- the K1325 published residual
  band m=12 z in {18..21} was CLOSED by the published z21-min16
  census kit (fourth final entry 92/0 at z=21); no band entry exists
  at z=22 or z=23.)
  (e) strip spots: m in {23..26}, X in {(m,m+1),(m,m+2),(m,m,m+1)},
      plus the m=18 base spot X=(18,18) at the T-Z23 slice base
      position H(42;(18,18);23) -- never measured by any published kit
      (the published z22-min17 census kit measured the z=22 spot only);
      candidate value 1 from the base-spot z-parity sequence
      0(z16),1(z17),0(z18),1(z19),0(z20),1(z21),0(z22) -- the EIGHTH
      point, odd z=23.
  (f) below-band bottom-rung child census (the z=23 analog of the
      K1320/K1322/K1325/K1328/z19/z20/z21/z22 section-(f) censuses;
      observational only): the j=1 rung's B-move child is the
      BELOW-BAND position (24; Y; 24) (min(Y) >= 18 so R=24 lies deep
      below z'+min(Y) >= 42). This section measures the z=23 child
      directly (H(24;Y;24) vs v(s,24,24), s in {0} U {18..48},
      arity(Y) in 0..4); candidate: full collapse, the NINTH
      consecutive below-band full collapse; the proof belongs to the
      declaration lane.
  (g) TAIL SUPPLY PRE-COMPUTATIONS (pure published K0832 closed form,
      NO engine recursion):
      (g1) FOURTEENTH-tail identity RECHECK (the z=23 slice supply
          datum): the published z21-min16 census kit measured
          v(s,24,24)=v(s,23,24) holding on {0} U {12..23} with a
          UNIFORM 0v1 break for all s>=24 over s in {0} U {12..58},
          and the published z22-min17 census kit rechecked and
          extended it over s in {0} U {12..59} (both predeclared
          components confirmed; the odd-z supply form graduated to
          3/3 at z=19/z=21/z=23). Rechecked here over the EXTENDED
          domain s in {0} U {12..60}: candidate hold {0} U {12..23},
          uniform 0v1 for all s in {24..60}.
      (g2) FIFTEENTH-tail identity RECHECK (the z=24 slice supply
          datum): the published z22-min17 census kit measured
          v(s,25,25)=v(s,24,25) holding on {0} U {12..23}, breaking
          0v2 at s=24 then uniformly 2v1 for all s>=25 over s in
          {0} U {12..59} (both predeclared components confirmed;
          even-z supply form graduated to 4/4 at z=18/z=20/z=22/
          z=24-supply). Rechecked here over the extended domain
          s in {0} U {12..60}: candidate hold {0} U {12..23}, 0v2 at
          s=24, uniform 2v1 for all s in {25..60}.
      (g3) SIXTEENTH-tail identity PRE-COMPUTATION (NEW, the z=25
          slice supply datum): v(s,26,26) vs v(s,25,26) over s in
          {0} U {12..60}. PREDECLARED candidate (written before the
          first run, BOTH components predeclared, the first
          predeclaration of an odd-k supply beyond k=23): odd-z
          supply identities (fourteenth tail at z=23-supply: hold
          {0,12..23}, uniform 0v1 s>=24; the published k=19 and k=21
          forms the same shape) hold on [0..k] and break as a
          UNIFORM 0v1 for s>=k+1 -- so the candidate is hold on
          {0} U {12..25}, break shape UNIFORM 0v1 for ALL s in
          {26..60}; z=25 decides whether the odd-z supply form
          graduates from 3/3 (z=19, z=21, z=23) to 4/4.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z23f18.out).

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
    R = j + 24
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(18, smax + 1)):
        ys = [()] if s == 0 else parts(s, 18, 4)
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
    for j in range(1, 18):
        name = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
                'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11'][j - 1]
        dev, multi, total = cell_sweep(j, 48)
        cells[f'cell{j}_{name}23f18'] = {
            'z': 23, 'min': j, 'R': j + 24, 'floor': 18,
            's_domain': '{0} U {18..48}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}23f18',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 18):
        nm = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
              'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11'][j - 1]
        for s in range(49, 57):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 24, X, 23)
            exp = v(s + j, 23, j + 24)
            tail.append({'cell': f'{nm}23f18', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s49_56', 'rows': tail})
    # (c) strip sweep m in 18..22 (T-Z23 claim position, provisional)
    sv = []
    viol = []
    cnt = 0
    for m in range(18, 23):
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
    out.append({'section': 'strip_z23_m18_22', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) IN-BAND base-child / m=17-row record at the z=23 m=17 row
    #     position (41; X; 23), all parts >= 17 (co-token 17 allowed),
    #     arity <= 3 TOTAL. Observational only: NOT a T-Z23 claim
    #     position. Candidate FIRST entry of the future T-Z22 residual
    #     band m=17 z in {23..32}. Published residual-band record style.
    out.append(row_record_x0(
        'inband_m17_z23_row_record',
        'observational_only_base_child_in_band_zstar17_33_gt_23_ninth_consecutive',
        {'co_token_17_allowed': True,
         'residual_band': 'CANDIDATE first entry of the future T-Z22 declaration residual band m=17 z in {23..32} (frontier z*(17)=33; band pending that lane; per the K1268 formula z*(m)=2m-2+(m mod 2)); the row is simultaneously the T-Z23 base m=18 a=18 child, the NINTH consecutive in-band base child',
         's_domain': '{17..55}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        41, 23, 17, 17, 55))
    out.append(row_record(
        'inband_m17_z23_row_record_ext_arity4',
        'observational_only_arity_le4_extension_of_the_m17_z23_record_cotoken_style',
        {'co_token_17_allowed': True,
         's_domain': '{17..55}', 'arity_max': 4},
        41, 23, 17, 17, 55, 17))
    # (d2) IN-BAND m=16-row z=23 record: SECOND entry of the future
    #      T-Z21 residual band m=16 z in {22..29}, published record
    #      style (z=22 entry (z22-min17 census kit) 40/0 + ext 39/0).
    #      Cross-artifact consistency recheck.
    out.append(row_record_x0(
        'inband_m16_z23_row_record',
        'observational_only_future_tz21_residual_m16_z23_second_entry_zstar16_30_gt_23_cross_artifact_recheck',
        {'co_token_16_allowed': True,
         'residual_band': 'future T-Z21 residual band m=16 z in {22..29}; z=22 entry (z22-min17 census kit) 40 shapes 0 seps + arity<=4 ext 39/0; same enumeration -> same 40 shapes here',
         's_domain': '{16..54}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        40, 23, 16, 16, 54))
    # (d3) IN-BAND m=15-row z=23 record: THIRD entry of the future
    #      T-Z20 residual band m=15 z in {21..28}, published record
    #      style (z=21 50/0 + ext 49/0, z=22 50/0).
    out.append(row_record_x0(
        'inband_m15_z23_row_record',
        'observational_only_future_tz20_residual_m15_z23_third_entry_zstar15_29_gt_23_cross_artifact_recheck',
        {'co_token_15_allowed': True,
         'residual_band': 'future T-Z20 residual band m=15 z in {21..28}; z=21 entry (z21-min16 census kit) 50 shapes 0 seps + arity<=4 ext 49/0; z=22 entry (z22-min17 census kit) 50/0; same enumeration -> same 50 shapes here',
         's_domain': '{15..53}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        39, 23, 15, 15, 53))
    # (d4) IN-BAND m=14-row z=23 record: FOURTH entry of the K1330
    #      published residual m=14 z in {20..25}, published record
    #      style (62/0 at z=20, z=21, z=22).
    out.append(row_record_x0(
        'inband_m14_z23_row_record',
        'observational_only_k1330_residual_m14_z23_fourth_entry_zstar14_26_gt_23_cross_artifact_recheck',
        {'co_token_14_allowed': True,
         'residual_band': 'K1330 published m=14 z in {20..25}; z=20 (z20-min15 census kit) 62/0; z=21 (z21-min16 census kit) 62/0; z=22 (z22-min17 census kit) 62/0; same enumeration -> same 62 shapes here',
         's_domain': '{14..52}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        38, 23, 14, 14, 52))
    # (d5) IN-BAND m=13-row z=23 record: FIFTH entry of the K1328
    #      published residual m=13 z in {19..24}, published record
    #      style (76/0 at z=19, z=20, z=21, z=22).
    out.append(row_record_x0(
        'inband_m13_z23_row_record',
        'observational_only_k1328_residual_m13_z23_fifth_entry_zstar13_25_gt_23_cross_artifact_recheck',
        {'co_token_13_allowed': True,
         'residual_band': 'K1328 published m=13 z in {19..24}; z=19 (z19-min14 census kit) 76/0; z=20 (z20 probe kit + z20-min15 census kit) 76/0 + ext 75/0; z=21 (z21-min16 census kit) 76/0; z=22 (z22-min17 census kit) 76/0; same enumeration -> same 76 shapes here',
         's_domain': '{13..51}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        37, 23, 13, 13, 51))
    # (e) strip spots m in 23..26
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
    # m=18 base spot (S=36, both 18-tokens) at the T-Z23 slice base
    # position
    w = H(42, (18, 18), 23)
    wv = v(36, 23, 42)
    out.append({'section': 'm18_base_spot', 'X': [18, 18], 'R': 42,
                'z': 23, 'value': w, 'collapse_single': wv,
                'match': w == wv,
                'published_probe_crossref': 'NEW measurement: no published kit measured H(42;(18,18);23) (the published z22-min17 census kit measured the z=22 spot H(40;(17,17);22)=0 only); candidate 1 from the base-spot z-parity sequence 0(z16),1(z17),0(z18),1(z19),0(z20),1(z21),0(z22)'})
    # (f) below-band bottom-rung child census: H(24; Y; 24) vs v(s,24,24)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(18, 49)):
        ys = [()] if s == 0 else parts(s, 18, 4)
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
                'label': 'observational_only_belowband_supply_source_at_z23',
                'R': 24, 'z': 24, 'floor': 18,
                's_domain': '{0} U {18..48}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (g1) FOURTEENTH-TAIL SUPPLY IDENTITY RECHECK (pure K0832 closed form)
    holds = []
    breaks = []
    for s in [0] + list(range(12, 61)):
        a = v(s, 24, 24)
        b = v(s, 23, 24)
        row = {'s': s, 'v_24_24': a, 'v_23_24': b, 'equal': a == b}
        (holds if a == b else breaks).append(row)
    out.append({'section': 'fourteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,24,24) =? v(s,23,24)',
                's_domain': '{0} U {12..60}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z21-min16 census kit section (g3) + z22-min17 census kit section (g2): holds {0} U {12..23}, uniform 0v1 break for all s>=24 over s in {0} U {12..59} (both predeclared components confirmed; the odd-z supply form graduated to 3/3 at z=19/z=21/z=23); rechecked and extended here over s in {0} U {12..60}',
                'hold_rows': holds, 'break_rows': breaks})
    # (g2) FIFTEENTH-TAIL SUPPLY IDENTITY RECHECK (published anchor)
    t_holds = []
    t_breaks = []
    for s in [0] + list(range(12, 61)):
        a = v(s, 25, 25)
        b = v(s, 24, 25)
        row = {'s': s, 'v_25_25': a, 'v_24_25': b, 'equal': a == b}
        (t_holds if a == b else t_breaks).append(row)
    out.append({'section': 'fifteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,25,25) =? v(s,24,25)',
                's_domain': '{0} U {12..60}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z22-min17 census kit section (g3): holds {0} U {12..23}, 0v2 break at s=24, then uniformly 2v1 for all s>=25 over s in {0} U {12..59} (both predeclared components confirmed; even-z supply form graduated to 4/4 at z=18/z=20/z=22/z=24-supply); rechecked and extended here',
                'hold_rows': t_holds, 'break_rows': t_breaks})
    # (g3) SIXTEENTH-TAIL SUPPLY PRE-COMPUTATION (NEW, pure K0832)
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
                'predeclared_candidate': 'BOTH components predeclared (first predeclaration of an odd-k supply beyond k=23): odd-z supply identities (fourteenth tail at z=23-supply: hold {0,12..23}, uniform 0v1 s>=24; the published k=19/k=21 identities are the same shape) hold on [0..k] and break as a UNIFORM 0v1 for s>=k+1 -- so the candidate is hold on {0} U {12..25}, break shape UNIFORM 0v1 for ALL s in {26..60}; z=25 decides whether the odd-z supply form graduates from 3/3 (z=19, z=21, z=23) to 4/4; constants recorded whatever they are',
                'hold_rows': n_holds, 'break_rows': n_breaks})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
