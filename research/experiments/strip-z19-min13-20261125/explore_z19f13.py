#!/usr/bin/env python3
"""
explore_z19f13: FROZEN PRE-DECLARATION census for the FLOOR-(z-6) edition of
the z=19 slice: the z=19 min>=13 (floor-13) cell ladder. NO K slot is
claimed by this file and NO universal claim is made: everything below is
finite machine observation against the pinned engine, plus engine-free
closed-form re-computations. Publish-then-execute.

Series context (the floor-necessity open rule): the classical slice floors
are z-5 (T-Z15..T-Z21 chain). The floor-(z-6) editions published so far:
  z=15 min>=9 (K1321: PROVED - the z-6 floor held the full closed ladder,
    the first negative-side datum for "is floor z-5 necessary?");
  z=16 min>=10 (kit 059c531e: the s=10 classes REVIVED at the reopened
    floor and restructured - even-s class revival, floor z-5 LOADS new
    classes at the even slice);
  z=17 min>=11 (kit 82f98ef4: s>=12 classes identical to floor-12 and the
    s=11 domain entry EMPTY - the first odd-s domain entry carrying no
    class).
This kit extends the floor-(z-6) series to z=19 (odd): the s=13 domain
entry is the SECOND odd-s domain-entry test (candidate: EMPTY, extending
the odd-s class absence to 2/2 odd revivals after z=17), and the 12
published dependency rungs are the candidate support for a future
T-Z19(min>=13) slice declaration (which would close the z=19 slice at
min>=13, prove the published K1328 residual band m=13 z=19 entry
(currently a 76/0 + 75/0 observation) as a corollary base, and add the
fifth consecutive in-band base child story at m0=13). Everything is
measured; nothing is claimed.

Scope (this file measures and reports; it proves nothing by itself):
  (a) cell census: for each j in 1..14 the floor-13 cell
      Cell_j(s) := H(j+20; {j} U Y; 19), Y tokens >= 13, s = sum(Y) in
      {0} U {13..44}, arity(Y) in 0..4 (0 only at s=0),
      swept EXHAUSTIVELY against the published raw engine (K1138
      recursion, embedded block byte-identical to the K1282..K1330
      chain, pin bd5f22e4...). Reported per cell: deviants from the
      Sigma-collapse v(s+j,19,j+20) (K0832 closed form) and any
      multivalue (decomposition-dependence) rows.
      The 14th rung (small token 14, one rank beyond the published
      T-Z19 cell table depth) is prefixed A8 as a PROVISIONAL census
      label; final naming belongs to the declaration lane.
      STRUCTURAL NOTES for the declaration lane (derivable from
      published material; this census tests them):
        (n1) For j in 1..12: the (iii) C-hand children are the published
             K1328 floor-13 z=18 cells (EXACT domain match Y>=13); the
             (i) A-hand children stay in-stair exactly as at floor-14
             (a-1 >= 12 >= j); the j=1 (ii') below-band child is in-stair
             at R=20 <= 20+13. Candidate: the FULL floor-14 deviant
             profile {14,16,18} U {F tail s>=20} survives with NO s=13
             class (odd-s absence 2/2 candidate; the supply pair
             v(s,20,20)=v(s,19,20) is floor-independent, K1334 theorem A
             k=19 odd form).
        (n2) Rung 13 (A719f13, R=33): the published T-Z19 cell A719f14
             position with the EXTENDED Y-domain (Y>=13 admitted). At
             s=13 both the (i)-child (32;{13,12};19) and the (ii)-child
             coincide with the published m=12-row z=19 record member
             (12,13) (92-shaped, 0 separations), and the (iii)-child is
             the published T-Z18 m=13 claim H(32;X;18): candidate
             COLlapSE at s=13.
        (n3) Rung 14 (A819f13, R=34): OUTSIDE the published cell tables.
             At s=13 the (i)-child (33;{14,12};19) and the (iii)-child
             value 1^H(33;{14,13};18) are UNPUBLISHED positions (min 12
             R=33 at z=19; min 13 R=33 at z=18); at s in {26,39} the
             13-multiple decompositions (13,13)/(13,13,13) drive
             further out-of-stair (i)-children. Candidate: collapse
             everywhere (led by the in-band 0-separation ledgers);
             alternative: a new rung-tail class or a multivalue row;
             measurement decides and this census reports it either way.
        (n4) PREDECLARED s=13 profile (engine-free closed-form cascade,
             K0832 only, no raw engine used; written BEFORE the first
             run; published supply constants only):
             for j in 1..12 every option is a published or closed-form
             value ((i) v(s+j-1,19,j+19) in-stair; (ii) the inductively
             conforming lower cell; (iii) the published K1328 z=18
             cells' conform values at s=13 - the published z=18 floor-13
             census found NO s=13 class (odd-s absence, first datum)),
             and the cascade yields CONFORM at every j in 1..12;
             j=13: (i)/(ii)-child = the published m=12-row z=19 record
             member (12,13) (observed collapse v(25,19,32)=1), (iii) =
             the PROVED T-Z18 m=13 child 1^v(26,18,32)=1 -> mex{1}=0 =
             target v(26,19,33)=0: CONFORM candidate;
             j=14: SHARP OPEN CASE - options {(i)=H(33;{14,12};19)
             UNKNOWN, (ii)=cell_13(13)=0 (predicted), (iii)=
             1^H(33;{14,13};18) UNKNOWN} with mirror set {0, 0} (target
             v(27,19,34)=1): the rung CONFORMS unless one of the two
             unknown children injects the value exactly 1 (then
             mex{0,1}=2: UP deviant 2v1); candidate: CONFORM
             (in-band-ledger lead), alternative: a new rung-tail class.
             The census decides; both outcomes are recorded as measured.
  (b) tail spots: s in {45..52}, single-token shape Y=(s,), all 14
      cells.
  (c) strip sweep (T-Z19 min>=13 CANDIDATE claim position; observational
      only): m in {13..17}, S in {m..m+39}, Y parts tokens >= m,
      arity(Y) <= 3: H(m+20; X; 19) vs v(S,19,m+20). EXHAUSTIVE
      in-sweep. The m=14..17 columns re-measure the published z19f14
      sweep (identical enumeration) as cross-artifact consistency; the
      m=13 column is the NEW candidate T-Z19(min>=13) base claim
      position sweep.
  (d) s=13 boundary special-child spots (the three positions that the
      floor-13 ladder touches OUTSIDE any published theorem or record;
      see (n2)/(n3)):
      (d1) (32;{13,12};19) vs v(25,19,32) - the (i)/(ii)-child of rung
           13 at s=13; published m=12-row z=19 record member
           (cross-artifact; the record measured 0 separations).
      (d2) (33;{14,12};19) vs v(26,19,33) - the (i)-child of rung 14 at
           s=13; UNPUBLISHED (min 12, R=33, z=19); candidate collapse.
      (d3) (33;{14,13};18) vs v(27,18,33) - the (iii)-child of rung 14
           at s=13; UNPUBLISHED (min 13, R=33, z=18; one above the
           T-Z18 m=13 claim position); candidate collapse. This is
           simultaneously a min-drop probe of the proved m=14-row z=18
           claim value v(27,18,33) at the position where the dropped
           min token makes it fall outside the claim domain.
  (e) strip spots m in {18..21}, X in {(m,m+1),(m,m+2),(m,m,m+1)},
      plus the m=13 base spot X=(13,13) at the candidate T-Z19(min>=13)
      base position H(33;(13,13);19) - a published member of the 76-shape
      m=13-row z=19 record (cross-artifact) AND the candidate base spot
      of the floor-13 extension; the K1334 lemma-S candidate value is
      (13+1)%2 = 0.
  (f) below-band bottom-rung child census (the floor-13 edition of the
      published section-(f) censuses; observational only): the j=1
      rung's B-move child is the BELOW-BAND position (20; Y; 20)
      (min(Y) >= 13 so R=20 lies deep below z'+min(Y) >= 33). The
      published floor-14 edition collapsed over its 117 shapes against
      v(s,20,20). This section measures the same child over the
      floor-13 domain (H(20;Y;20) vs v(s,20,20), s in {0} U {13..44},
      arity(Y) in 0..4); the proof belongs to the declaration lane
      (K1264 stair covers it trivially for s>0; s=0 is the empty
      position 0 = v(0,20,20)).
  (g) TENTH-tail supply identity RECHECK (pure published K0832 closed
      form, NO engine recursion): the floor-13 z=19 slice supply is the
      SAME k=19 identity pair as floor-14 (floor-independent):
      v(s,20,20) = v(s,19,20) holding on {0} U {12..19} and breaking
      uniformly 0v1 for s>=20 (published by the z19 probe + z19-min14
      kits; K1334 theorem A k=19 odd instance). Rechecked here over
      s in {0} U {12..56}: frozen cross-artifact consistency row.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z19f13.out).
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
    """sweep cell_j over s in {0} U {13..smax}; returns (dev, multi, total)"""
    R = j + 20
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(13, smax + 1)):
        ys = [()] if s == 0 else parts(s, 13, 4)
        vals = {}
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            h = H(R, X, 19)
            vals.setdefault(h, []).append(y)
            total += 1
        if len(vals) > 1:
            multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s + j, 19, R)
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


def main():
    out = []
    out.append({'section': 'engine_gate', 'engine_sha': sha, 'pin': PIN,
                'gate': 'PASS'})
    cells = {}
    for j in range(1, 15):
        name = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
                'A5', 'A6', 'A7', 'A8'][j - 1]
        dev, multi, total = cell_sweep(j, 44)
        cells[f'cell{j}_{name}19f13'] = {
            'z': 19, 'min': j, 'R': j + 20, 'floor': 13,
            's_domain': '{0} U {13..44}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}19f13',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 15):
        nm = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
              'A5', 'A6', 'A7', 'A8'][j - 1]
        for s in range(45, 53):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 20, X, 19)
            exp = v(s + j, 19, j + 20)
            tail.append({'cell': f'{nm}19f13', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s45_52', 'rows': tail})
    # (c) strip sweep m in 13..17 (T-Z19 min>=13 candidate claim base;
    #     m=14..17 re-measure the published z19f14 enumeration)
    sv = []
    viol = []
    cnt = 0
    for m in range(13, 18):
        H.cache_clear()
        for S in range(m, m + 40):
            for X in parts(max(S - m, 0), m, 3):
                XX = tuple(sorted((m,) + X, reverse=True))
                if sum(XX) != S:
                    continue
                hv = H(m + 20, XX, 19)
                ev = v(S, 19, m + 20)
                cnt += 1
                if hv != ev:
                    viol.append({'m': m, 'X': list(XX), 'S': S,
                                 'value': hv, 'collapse': ev})
        sv.append({'m': m, 'cumulative_shapes': cnt,
                   'cumulative_violations': len(viol)})
    out.append({'section': 'strip_z19_m13_17', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) s=13 boundary special-child spots
    d1 = H(32, tuple(sorted((13, 12), reverse=True)), 19)
    d1v = v(25, 19, 32)
    d2 = H(33, tuple(sorted((14, 12), reverse=True)), 19)
    d2v = v(26, 19, 33)
    d3 = H(33, tuple(sorted((14, 13), reverse=True)), 18)
    d3v = v(27, 18, 33)
    out.append({'section': 'boundary_s13_special_children',
                'label': 'observational_only_the_three_positions_outside_published_cover',
                'rows': [
                    {'id': 'd1_rung13_i_ii_child', 'R': 32, 'z': 19,
                     'X': [13, 12], 'value': d1, 'collapse': d1v,
                     'match': d1 == d1v,
                     'published_status': 'member of the published m=12-row z=19 record (92 shapes, 0 separations) - cross-artifact'},
                    {'id': 'd2_rung14_i_child', 'R': 33, 'z': 19,
                     'X': [14, 12], 'value': d2, 'collapse': d2v,
                     'match': d2 == d2v,
                     'published_status': 'UNPUBLISHED position (min 12, R=33, z=19); candidate collapse'},
                    {'id': 'd3_rung14_iii_child', 'R': 33, 'z': 18,
                     'X': [14, 13], 'value': d3, 'collapse': d3v,
                     'match': d3 == d3v,
                     'published_status': 'UNPUBLISHED position (min 13, R=33, z=18, one above the T-Z18 m=13 claim); simultaneous min-drop probe of the proved m=14-row z=18 claim value v(27,18,33); candidate collapse'}]})
    # (e) strip spots m in 18..21
    spots = []
    for m in range(18, 22):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 20, X, 19)
            ev = v(S, 19, m + 20)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    out.append({'section': 'strip_spots_m18_21', 'rows': spots})
    # m=13 base spot (S=26, both 13-tokens) at the candidate T-Z19
    # (min>=13) base position; published member of the m=13-row z=19
    # 76-shape record (cross-artifact); K1334 lemma-S candidate value 0.
    w = H(33, (13, 13), 19)
    wv = v(26, 19, 33)
    out.append({'section': 'm13_base_spot', 'X': [13, 13], 'R': 33,
                'z': 19, 'value': w, 'collapse_single': wv,
                'match': w == wv,
                'published_crossref': 'member of the published m=13-row z=19 record (76 shapes, 0 separations; z19-min14 kit); K1334 lemma-S candidate (13+1)%2=0'})
    # (f) below-band bottom-rung child census: H(20; Y; 20) vs v(s,20,20)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(13, 45)):
        ys = [()] if s == 0 else parts(s, 13, 4)
        vals = {}
        for y in ys:
            h = H(20, y, 20)
            vals.setdefault(h, []).append(y)
            bb_total += 1
        if len(vals) > 1:
            bb_multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s, 20, 20)
            if val != exp:
                bb_dev.append({'s': s, 'value': val, 'collapse': exp,
                               'direction': 'UP' if val > exp else 'DOWN',
                               'shapes': len(vals[val])})
    out.append({'section': 'belowband_j1_child_H20_20_floor13',
                'label': 'observational_only_belowband_supply_source_floor13_edition',
                'R': 20, 'z': 20, 'floor': 13,
                's_domain': '{0} U {13..44}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (g) TENTH-tail supply identity RECHECK (pure K0832 closed form)
    holds = []
    breaks = []
    for s in [0] + list(range(12, 57)):
        a = v(s, 20, 20)
        b = v(s, 19, 20)
        row = {'s': s, 'v_20_20': a, 'v_19_20': b, 'equal': a == b}
        (holds if a == b else breaks).append(row)
    out.append({'section': 'tenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832_floor_independent',
                'identity': 'v(s,20,20) =? v(s,19,20)',
                's_domain': '{0} U {12..56}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z19 probe kit (9e955243) + z19-min14 census kit (6a6832ce): holds {0} U {12..19}, breaks UNIFORMLY 0v1 for all s>=20; K1334 theorem A k=19 odd instance; floor-independent (the floor-13 slice supply datum)',
                'hold_rows': holds, 'break_rows': breaks})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
