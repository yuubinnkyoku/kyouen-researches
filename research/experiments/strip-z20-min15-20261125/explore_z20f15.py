#!/usr/bin/env python3
"""
explore_z20f15: FROZEN PRE-DECLARATION census for the z=20 min>=15
(floor-15) cell ladder and the T-Z20 strip (the K1330 (T-Z19)
declaration continuation; NO K slot is claimed by this file;
publish-then-execute).

Scope (this file measures and reports; it proves nothing by itself):
  (a) cell census: for each j in 1..14 the floor-15 cell
      Cell_j(s) := H(j+21; {j} U Y; 20), Y tokens >= 15, s = sum(Y) in
      {0} U {15..45}, arity(Y) in 0..4 (0 only at s=0),
      swept EXHAUSTIVELY against the published raw engine (K1138
      recursion, embedded block byte-identical to the K1282..K1328
      chain, pin bd5f22e4...). Reported per cell: deviants from the
      Sigma-collapse v(s+j,20,j+21) (K0832 closed form) and any
      multivalue (decomposition-dependence) rows. The j=14 rung (small
      token 14, one rank beyond the published z=19 A7-cell A719f14) is
      prefixed A8 as a PROVISIONAL census label; final naming belongs
      to the declaration lane. STRUCTURAL NOTE for the declaration
      lane: the published z=19 (z19-min14 census) deviant position set
      is {14, 16, 18} (C/B/A at 14; E/D at 16; F/G/E at 18, F hole at
      19, F tail s>=20). Under the new floor 15 the position-14 classes
      fall BELOW the floor: the candidate is a definition-domain-
      exclusion event for the 14-classes (contrast the z=17 -> z=18
      shift where the s=12 classes fell below floor 13, and the z=19
      shift which excluded nothing; this would be the 4th recorded
      exclusion event if it happens) and the ladder would re-form
      around the surviving positions {16, 18} -- this census probes
      (i) which of the 16/18 classes persist at z=20 with which
      positions/directions/values, (ii) the EVEN-z F-cell candidate:
      the single@(even z) / hole+tail@(odd z) typology alternation has
      FIVE consecutive consistent slices (z15..z19) and predicts a
      SINGLE-POINT F deviant at s=20; the supply datum is the published
      ELEVENTH-tail identity v(s,21,21)=v(s,20,21) holding on {0} U
      {12..19}, breaking 0v2 at s=20 then uniformly 2v1 for s>=21
      (the z=20 F-cell deviant constants are NOT predeclared; the
      naive +2-shift of published constants is not assumed anywhere),
      and (iii) whether the z=19 A-rank deviant (at s=14=z-5) being
      floor-excluded re-extends the A-family full-collapse run, and
      whether the A-family collapse run extends to EIGHT rungs
      (A20f15 .. A820f15), which is exactly the T-Z20 base-m=15
      trivial-absorption case: the a=15 child of the T-Z20 base
      position H(36;{15} U Y;20) is precisely the cell-14 domain
      H(35; {14} U Y;20) -- the SIXTH consecutive in-band base child
      (after K1320 min=9, K1322 min=10, K1325 min=11, K1328 min=12,
      K1330 min=13; z*(14)=26 > 20).
  (b) tail spots: s in {46..53}, single-token shape Y=(s,), all 14
      cells.
  (c) strip sweep (T-Z20 claim position, PROVISIONAL label): m in
      {15..19}, S in {m..m+39}, Y parts tokens >= m, arity(Y) <= 3:
      H(m+21; X; 20) vs v(S,20,m+21). EXHAUSTIVE in-sweep.
  (d) IN-BAND base-child / m=14-row record (the structurally decisive
      section; observational only, NOT a T-Z20 claim position): the
      T-Z20 base m=15 a=15 child lands at (35; {14} U Y; 20) = the
      m=14-row claim position H(35; X; 20), and z=20 is IN BAND for
      min=14 (z*(14) = 26 > 20, K1268 formula z*(m)=2m-2+(m mod 2)),
      the SIXTH consecutive slice whose base child is in-band. Swept:
      S in {14..52}, all parts >= 14 (co-token 14 shapes INCLUDED,
      X[0]=14), arity <= 3, recorded against the Sigma-collapse
      v(S,20,35) with every separation listed, PLUS an arity<=4
      co-token-style extension sweep (published style lesson of the
      z18/z19 kits: the base record itself is kept in the published
      residual-band style, the arity<=4 version as a labelled
      extension). This is simultaneously the FIRST entry of the
      K1330 (T-Z19) published residual band m=14 z in {20..25}
      (frontier z*(14)=26; band per the published K1330 declaration
      note, official runs published OFFICIAL-PASS).
  (d2) IN-BAND m=13-row z=20 record: the SECOND entry of the K1328
      published residual band m=13 z in {19..24}. The z=19 entry was
      measured by the published z19-min14 census kit (76 shapes 0 seps
      + arity<=4 ext 75/0); the z=20 entry was measured by the
      published z20 beyond/frontier probe kit (76/0 + 75/0). SAME
      enumeration here -> same 76 shapes, cross-artifact shape-for-
      shape consistency machine-checked.
  (d3) IN-BAND m=12-row z=20 record: the THIRD entry of the K1325
      published residual band m=12 z in {18..21}. The z=18/z=19
      entries were measured by the published z18/z19 kits (92 shapes
      0 seps each); the z=20 entry by the published z20 probe kit
      (92/0). SAME enumeration -> same 92 shapes here.
  (NOT swept: the m=11-row z=20 record -- the K1322 published residual
      band m=11 z in {17..20} was CLOSED by the published z20 probe kit
      (fourth final entry 110/0); adding no band entry.)
  (e) strip spots: m in {20..23}, X in {(m,m+1),(m,m+2),(m,m,m+1)},
      plus the m=15 base spot X=(15,15) at the T-Z20 slice base
      position H(36;(15,15);20) -- already measured by the published
      z20 probe kit (=0=v(30,20,36)); rechecked here as the
      census-internal cross-check of the frozen chain value.
  (f) below-band bottom-rung child census (the z=20 analog of the
      K1320/K1322/K1325/K1328/z19 section-(f) census; observational
      only): the j=1 rung's B-move child is the BELOW-BAND position
      (21; Y; 21) (min(Y) >= 15 so R=21 lies deep below z'+min(Y)
      >= 36). At z=19 the analogous child H(20;Y;20) collapsed over
      the full floor-14 census against v(s,20,20) (FIFTH consecutive
      full collapse). This section measures the z=20 child directly
      (H(21;Y;21) vs v(s,21,21), s in {0} U {15..45}, arity(Y) in
      0..4); the proof belongs to the declaration lane.
  (g) TAIL SUPPLY PRE-COMPUTATIONS (pure published K0832 closed form,
      NO engine recursion):
      (g1) ELEVENTH-tail identity RECHECK: the published z19 census
      kit measured v(s,21,21)=v(s,20,21) holding on {0} U {12..19},
      breaking at s=20 as 0v2 then uniformly 2v1 for all s>=21, over
      s in {0} U {12..56}; the published z20 probe kit rechecked the
      same domain. Rechecked here over the EXTENDED domain s in
      {0} U {12..57} (the z=20 slice supply datum).
      (g2) TWELFTH-tail identity RECHECK: the published z20 probe kit
      measured v(s,22,22)=v(s,21,22) holding on {0} U {12..21} with
      a UNIFORM 0v1 break for all s>=22 over s in {0} U {12..57}
      (predeclared odd-z candidate confirmed). Rechecked here over
      the same extended domain (the z=21 slice supply datum).
      (g3) THIRTEENTH-tail identity PRE-COMPUTATION (NEW): the z=22
      slice supply identity v(s,23,23) vs v(s,22,23) over s in
      {0} U {12..57}. PREDECLARED candidate (written before the first
      run): the even-z identities break AT s=z (z=16: break at s=16
      uniform 1-vs-0; z=18: 0v2 at s=18 then uniform 2v1 from s=19;
      z=20: 0v2 at s=20 then uniform 2v1 from s=21), so the candidate
      break start is s=22 AND the candidate break shape is 0v2@22 +
      uniform 2v1@23+ (the newest even-z form, 2/2 so far at z=18 and
      z=20); constants recorded whatever they are (z=22 decides
      whether the 0v2+2v1 form is the stable even-z shape or a
      two-data-point coincidence).

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z20f15.out).
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
    R = j + 21
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(15, smax + 1)):
        ys = [()] if s == 0 else parts(s, 15, 4)
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
    z19-min14 kit sections (d)/(d2)): position X = parts(S, m, 3) with
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
    for j in range(1, 15):
        name = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
                'A5', 'A6', 'A7', 'A8'][j - 1]
        dev, multi, total = cell_sweep(j, 45)
        cells[f'cell{j}_{name}20f15'] = {
            'z': 20, 'min': j, 'R': j + 21, 'floor': 15,
            's_domain': '{0} U {15..45}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}20f15',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 15):
        nm = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
              'A5', 'A6', 'A7', 'A8'][j - 1]
        for s in range(46, 54):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 21, X, 20)
            exp = v(s + j, 20, j + 21)
            tail.append({'cell': f'{nm}20f15', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s46_53', 'rows': tail})
    # (c) strip sweep m in 15..19 (T-Z20 claim position, provisional)
    sv = []
    viol = []
    cnt = 0
    for m in range(15, 20):
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
    out.append({'section': 'strip_z20_m15_19', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) IN-BAND base-child / m=14-row record at the z=20 m=14 claim
    #     position (35; X; 20), all parts >= 14 (co-token 14 allowed),
    #     arity <= 3 TOTAL. Observational only: NOT a T-Z20 claim
    #     position. Published residual-band record style.
    out.append(row_record_x0(
        'inband_m14_z20_row_record',
        'observational_only_base_child_in_band_zstar14_26_gt_20_sixth_consecutive',
        {'co_token_14_allowed': True,
         'residual_band': 'K1330 (T-Z19) published residual band m=14 z in {20..25}; frontier z=26; FIRST entry (z*(14)=26>20 in-band; band per the published K1330 declaration note, official runs OFFICIAL-PASS)',
         's_domain': '{14..52}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        35, 20, 14, 14, 52))
    out.append(row_record(
        'inband_m14_z20_row_record_ext_arity4',
        'observational_only_arity_le4_extension_of_the_m14_z20_record_cotoken_style',
        {'co_token_14_allowed': True,
         's_domain': '{14..52}', 'arity_max': 4},
        35, 20, 14, 14, 52, 14))
    # (d2) IN-BAND m=13-row z=20 record: SECOND entry of the K1328
    #      published residual m=13 z in {19..24}, published record
    #      style (z=19 census entry 76/0 + ext 75/0; z=20 probe entry
    #      76/0 + ext 75/0). Cross-artifact consistency recheck.
    out.append(row_record_x0(
        'inband_m13_z20_row_record',
        'observational_only_k1328_residual_m13_z20_second_entry_zstar13_25_gt_20_cross_artifact_recheck',
        {'co_token_13_allowed': True,
         'residual_band': 'K1328 published m=13 z in {19..24}; z=19 entry (z19-min14 census kit) 76/0 + arity<=4 ext 75/0; z=20 entry (z20 beyond probe kit) 76/0 + ext 75/0; same enumeration -> same 76 shapes here',
         's_domain': '{13..51}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        34, 20, 13, 13, 51))
    # (d3) IN-BAND m=12-row z=20 record: THIRD entry of the K1325
    #      published residual m=12 z in {18..21}, published record
    #      style (92/0 at z=18, z=19, z=20-probe).
    out.append(row_record_x0(
        'inband_m12_z20_row_record',
        'observational_only_k1325_residual_m12_z20_third_entry_zstar12_22_gt_20_cross_artifact_recheck',
        {'co_token_12_allowed': True,
         'residual_band': 'K1325 published m=12 z in {18..21}; z=18 (z18-min13 kit) 92/0; z=19 (z19-min14 census kit) 92/0; z=20 (z20 beyond probe kit) 92/0; same enumeration -> same 92 shapes here',
         's_domain': '{12..50}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        33, 20, 12, 12, 50))
    # (e) strip spots m in 20..23
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
    # m=15 base spot (S=30, both 15-tokens) at the T-Z20 slice base
    # position
    w = H(36, (15, 15), 20)
    wv = v(30, 20, 36)
    out.append({'section': 'm15_base_spot', 'X': [15, 15], 'R': 36,
                'z': 20, 'value': w, 'collapse_single': wv,
                'match': w == wv,
                'published_probe_crossref': 'beyond_z20 kit (0906ff21) measured H(36;(15,15);20)=0=v(30,20,36); rechecked here'})
    # (f) below-band bottom-rung child census: H(21; Y; 21) vs v(s,21,21)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(15, 46)):
        ys = [()] if s == 0 else parts(s, 15, 4)
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
                'label': 'observational_only_belowband_supply_source_at_z20',
                'R': 21, 'z': 21, 'floor': 15,
                's_domain': '{0} U {15..45}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (g1) ELEVENTH-TAIL SUPPLY IDENTITY RECHECK (pure K0832 closed form)
    holds = []
    breaks = []
    for s in [0] + list(range(12, 58)):
        a = v(s, 21, 21)
        b = v(s, 20, 21)
        row = {'s': s, 'v_21_21': a, 'v_20_21': b, 'equal': a == b}
        (holds if a == b else breaks).append(row)
    out.append({'section': 'eleventh_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,21,21) =? v(s,20,21)',
                's_domain': '{0} U {12..57}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z19-min14 census kit section (g2) + beyond_z20 kit section (9): holds {0} U {12..19}, breaks at s=20 as 0v2, then uniform 2v1 for all s>=21, over s in {0} U {12..56}; rechecked and extended here over s in {0} U {12..57}',
                'hold_rows': holds, 'break_rows': breaks})
    # (g2) TWELFTH-TAIL SUPPLY IDENTITY RECHECK (published anchor)
    t_holds = []
    t_breaks = []
    for s in [0] + list(range(12, 58)):
        a = v(s, 22, 22)
        b = v(s, 21, 22)
        row = {'s': s, 'v_22_22': a, 'v_21_22': b, 'equal': a == b}
        (t_holds if a == b else t_breaks).append(row)
    out.append({'section': 'twelfth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,22,22) =? v(s,21,22)',
                's_domain': '{0} U {12..57}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'beyond_z20 kit section (10): holds {0} U {12..21}, uniform 0v1 break for all s>=22 over s in {0} U {12..57} (predeclared odd-z candidate confirmed); rechecked here',
                'hold_rows': t_holds, 'break_rows': t_breaks})
    # (g3) THIRTEENTH-TAIL SUPPLY PRE-COMPUTATION (NEW, pure K0832)
    n_holds = []
    n_breaks = []
    for s in [0] + list(range(12, 58)):
        a = v(s, 23, 23)
        b = v(s, 22, 23)
        row = {'s': s, 'v_23_23': a, 'v_22_23': b, 'equal': a == b}
        (n_holds if a == b else n_breaks).append(row)
    out.append({'section': 'thirteenth_tail_supply_identity_precalc',
                'label': 'observational_only_new_closed_form_precalc_z22_slice_supply_k0832',
                'identity': 'v(s,23,23) =? v(s,22,23)',
                's_domain': '{0} U {12..57}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'predeclared_candidate': 'break starts AT s=22 (even-z identities break at s=z: z=16 uniform 1-vs-0, z=18 0v2@18 + 2v1@>=19, z=20 0v2@20 + 2v1@>=21) AND the candidate break shape is 0v2@22 + uniform 2v1@>=23 (the newest even-z form, 2/2 at z=18/z=20); constants recorded whatever they are - z=22 decides whether the 0v2+2v1 form is the stable even-z shape',
                'hold_rows': n_holds, 'break_rows': n_breaks})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
