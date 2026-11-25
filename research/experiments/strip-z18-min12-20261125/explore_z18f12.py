#!/usr/bin/env python3
"""
explore_z18f12: FROZEN PRE-DECLARATION census for the FLOOR-(z-6) edition of
the z=18 slice: the z=18 min>=12 (floor-12) cell ladder. NO K slot is
claimed by this file and NO universal claim is made: everything below is
finite machine observation against the pinned engine, plus engine-free
closed-form re-computations. Publish-then-execute.

Series context (the floor-necessity open rule): the classical slice floors
are z-5 (T-Z15..T-Z21 chain). The floor-(z-6) editions published so far:
  z=15 min>=9 (K1321: PROVED - the z-6 floor held the full closed ladder);
  z=16 min>=10 (kit 059c531e: the s=10 classes REVIVED at the reopened
    floor and RESTRUCTURED as {B DOWN:0, A UP:1, A2 UP:2}@10 - the
    even-s class revival; floor z-5 LOADS new classes at even slices);
  z=17 min>=11 (kit 82f98ef4: s>=12 classes identical to floor-12 and the
    s=11 domain entry EMPTY - the first odd-s domain entry carrying no
    class).
This kit extends the floor-(z-6) series to z=18 (even): the s=12 domain
re-entry loads the published z=17 s=12 deviant classes (A{12 UP:2},
C{12 DOWN:1}, B{12 DOWN:0}; K1325 census) as (iii)-hand supplies into the
z=18 floor-12 ladder. It is simultaneously the candidate support for a
future T-Z18(min>=12) slice declaration (which would close the z=18 slice
at min>=12, prove the published K1325 residual band m=12 z=18 entry
(92/0, published by the z18-min13 kit) as a corollary base) - NOTE: the
classical T-Z18 m>=13 proof does NOT extend trivially, because the s=12
revival classes break the full-collapse assumption of the trivial
absorption; the census measures exactly what a floor-12 declaration would
have to handle. Everything is measured; nothing is claimed.

Scope (this file measures and reports; it proves nothing by itself):
  (a) cell census: for each j in 1..13 the floor-12 cell
      Cell_j(s) := H(j+19; {j} U Y; 18), Y tokens >= 12, s = sum(Y) in
      {0} U {12..43}, arity(Y) in 0..4 (0 only at s=0),
      swept EXHAUSTIVELY against the published raw engine (K1138
      recursion, embedded block byte-identical to the K1282..K1330
      chain, pin bd5f22e4...). Reported per cell: deviants from the
      Sigma-collapse v(s+j,18,j+19) (K0832 closed form) and any
      multivalue (decomposition-dependence) rows.
      The 13th rung (small token 13, one rank beyond the published
      T-Z18 cell table depth) is prefixed A7 as a PROVISIONAL census
      label; final naming belongs to the declaration lane.
      STRUCTURAL NOTES for the declaration lane (derivable from
      published material; this census tests them):
        (m1) For j in 1..11: the (iii) C-hand children are the
             published K1325 floor-12 z=17 cells (EXACT domain match
             Y>=12); the (i) A-hand children stay in-stair exactly as at
             floor-13 (a-1 >= 11 >= j at the s=12 boundary; deeper s
             values with 12-parts keep min = j for j <= 11); the j=1
             (ii') below-band child is in-stair at R=19 <= 19+12.
             Candidate: the s>=13 classes are the FULL floor-13 deviant
             profile {s=14,16,18}+ (the floor-12 domain adds ONLY the
             s=12 boundary class candidates below).
        (m2) Rung 12 (A618f12, R=31): the published T-Z18 cell A618f13
             position with the EXTENDED Y-domain (Y>=12 admitted). At
             s=12 the (i)/(ii)-child (30;{12,11};18) is a member of the
             published m=11-row z=18 record (110 shapes, 0 separations)
             and the (iii)-child (30;{12,12};17) is the PROVED T-Z17
             m=12 claim position: candidate COLlapSE at s=12.
        (m3) Rung 13 (A718f12, R=32): OUTSIDE the published cell tables.
             At s=12 the (i)-child (31;{13,11};18) and the (iii)-child
             (31;{13,12};17) are UNPUBLISHED positions (min 11 R=31 at
             z=18; min 12 R=31 at z=17, one above the T-Z17 m=12 claim);
             at s in {24,36} the 12-multiple decompositions drive
             further out-of-stair children. Candidate: collapse
             everywhere; alternative: a new rung-tail class or a
             multivalue row; measurement decides and this census reports
             it either way.
        (m4) PREDECLARED s=12 REVIVAL PROFILE (engine-free closed-form
             cascade, K0832 only, no raw engine used; written BEFORE
             the first run; published supply constants only). The
             published z=17 s=12 deviants supply mirror-DIFFERING
             (iii)-hand options at exactly three rungs: C(5) (1^1=0 vs
             mirror 1^2=3), B(6) (1^0=1 vs mirror 1^1=0), A(7) (1^2=3 vs
             mirror 1^0=1). The full-mex cascade over the three-option
             sets {(i) mirror, (ii) lower cell, (iii) actual} yields the
             PREDECLARED candidate profile:
               F(1) G(2) E(3) D(4) C(5): CONFORM (the C supply 0
                 replicates the (i) option value 0: mex-level flat
                 absorption, the published z=18/z=20 pattern);
               B(6): DEVIANT DOWN, options {1,1,1} -> mex 0 vs target
                 v(18,18,25)=2 (0v2);
               A(7): DEVIANT UP, options {2,0,3} -> mex 1 vs target
                 v(19,18,26)=0 (1v0);
               A2(8): DEVIANT UP, options {0,1,0} -> mex 2 vs target
                 v(20,18,27)=1 (2v1);
               A3(9)..A6(12): CONFORM (cascade closes: A3 options
                 {1,2,1} -> mex 0 = target 0; the rung-12 boundary uses
                 the published record member, mex{0,0,0}=1 = target 1);
               A7(13): SHARP OPEN CASE - options {(i)=UNKNOWN (31;
                 {13,11};18), (ii)=cell_12(12)=1, (iii)=1^UNKNOWN(31;
                 {13,12};17)} with mirror set {1,1} (target
                 v(25,18,32)=0): the rung CONFORMS iff neither unknown
                 equals the mex-breaking values ((i)=0 would NOT break
                 - wait: 0 in the set makes mex{0,1}=1... the rung
                 deviates iff (i)=0 or H(31;{13,12};17)=1); candidate:
                 CONFORM, alternative recorded.
             THE HEADLINE CANDIDATE: the predicted revival profile
             {B DOWN:0, A UP:1, A2 UP:2} at s=12 is EXACTLY the
             published z=16 floor-10 revival profile {B DOWN:0, A UP:1,
             A2 UP:2}@10 (kit 059c531e), +2 shifted - the even-z
             floor-(z-6) revival-profile repeat law, 2/2 even slices
             candidate. If confirmed, the z=20 floor-14 edition (loading
             the z=19 s=14 classes C/B/A) is the next discrimination
             (a different supply constellation: the odd slice feeds
             {DOWN:1, DOWN:0, UP:2} at s=14), and the floor-necessity
             rule would read: floor z-5 is necessary at EVEN z (the z-6
             floor loads revival classes) but not at ODD z (z-15
             PROVED, z-17 observed, z-19 candidate after this series).
  (b) tail spots: s in {44..51}, single-token shape Y=(s,), all 13
      cells.
  (c) strip sweep (T-Z18 min>=12 CANDIDATE claim position; observational
      only): m in {12..16}, S in {m..m+39}, Y parts tokens >= m,
      arity(Y) <= 3: H(m+19; X; 18) vs v(S,18,m+19). EXHAUSTIVE
      in-sweep. The m=13..16 columns re-measure the published z18f13
      sweep (identical enumeration) as cross-artifact consistency; the
      m=12 column is the NEW candidate T-Z18(min>=12) base claim
      position sweep.
  (d) s=12 boundary special-child spots (the positions that the
      floor-12 ladder touches OUTSIDE any published theorem or record):
      (d1) (30;{12,11};18) vs v(23,18,30) - the (i)/(ii)-child of rung
           12 at s=12; published member of the m=11-row z=18 record
           (110 shapes, 0 separations; cross-artifact).
      (d2) (31;{13,11};18) vs v(24,18,31) - the (i)-child of rung 13 at
           s=12; UNPUBLISHED (min 11, R=31, z=18); candidate collapse.
      (d3) (31;{13,12};17) vs v(25,17,31) - the (iii)-child of rung 13
           at s=12; UNPUBLISHED (min 12, R=31, z=17, one above the
           T-Z17 m=12 claim position R=30); candidate collapse. This is
           simultaneously a min-drop probe of the published m=13-row
           z=17 claim value v(25,17,31) at the position where the
           dropped min token takes it outside the claim domain.
  (e) strip spots m in {17..20}, X in {(m,m+1),(m,m+2),(m,m,m+1)}, plus
      the m=12 base spot X=(12,12) at the candidate T-Z18(min>=12) base
      position H(31;(12,12);18) - a published member of the 92-shape
      m=12-row z=18 record (cross-artifact).
  (f) below-band bottom-rung child census (the floor-12 edition of the
      published section-(f) censuses; observational only): the j=1
      rung's B-move child is the BELOW-BAND position (19; Y; 19)
      (min(Y) >= 12 so R=19 lies deep below z'+min(Y) >= 31). The
      published floor-13 edition collapsed over its full census against
      v(s,19,19). This section measures the same child over the
      floor-12 domain (H(19;Y;19) vs v(s,19,19), s in {0} U {12..43},
      arity(Y) in 0..4); the proof belongs to the declaration lane
      (K1264 stair covers it trivially for s>0; s=0 is the empty
      position 0 = v(0,19,19)).
  (g) supply identity RECHECKS (pure published K0832 closed form, NO
      engine recursion): the floor-12 z=18 slice supply is the SAME k=18
      identity pair as floor-13 (floor-independent):
      v(s,19,19) = v(s,18,19) holding on {0} U {12..17} and breaking
      0v2 at s=18 then uniformly 2v1 for s>=19 (published by the
      z18-min13 kit; K1334 theorem A k=18 even instance), rechecked
      over s in {0} U {12..55}; plus the z=17 partner identity recheck
      v(s,18,18) =? v(s,17,18) over the same domain (published
      K1325 supply; frozen cross-artifact consistency rows).

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z18f12.out).
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
    """sweep cell_j over s in {0} U {12..smax}; returns (dev, multi, total)"""
    R = j + 19
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(12, smax + 1)):
        ys = [()] if s == 0 else parts(s, 12, 4)
        vals = {}
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            h = H(R, X, 18)
            vals.setdefault(h, []).append(y)
            total += 1
        if len(vals) > 1:
            multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s + j, 18, R)
            if val != exp:
                dev.append({'s': s, 'value': val, 'collapse': exp,
                            'direction': 'UP' if val > exp else 'DOWN',
                            'shapes': len(vals[val])})
    H.cache_clear()
    return dev, multi, total


def main():
    out = []
    out.append({'section': 'engine_gate', 'engine_sha': sha, 'pin': PIN,
                'gate': 'PASS'})
    cells = {}
    for j in range(1, 14):
        name = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
                'A5', 'A6', 'A7'][j - 1]
        dev, multi, total = cell_sweep(j, 43)
        cells[f'cell{j}_{name}18f12'] = {
            'z': 18, 'min': j, 'R': j + 19, 'floor': 12,
            's_domain': '{0} U {12..43}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}18f12',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 14):
        nm = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
              'A5', 'A6', 'A7'][j - 1]
        for s in range(44, 52):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 19, X, 18)
            exp = v(s + j, 18, j + 19)
            tail.append({'cell': f'{nm}18f12', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s44_51', 'rows': tail})
    # (c) strip sweep m in 12..16 (T-Z18 min>=12 candidate claim base;
    #     m=13..16 re-measure the published z18f13 enumeration)
    sv = []
    viol = []
    cnt = 0
    for m in range(12, 17):
        H.cache_clear()
        for S in range(m, m + 40):
            for X in parts(max(S - m, 0), m, 3):
                XX = tuple(sorted((m,) + X, reverse=True))
                if sum(XX) != S:
                    continue
                hv = H(m + 19, XX, 18)
                ev = v(S, 18, m + 19)
                cnt += 1
                if hv != ev:
                    viol.append({'m': m, 'X': list(XX), 'S': S,
                                 'value': hv, 'collapse': ev})
        sv.append({'m': m, 'cumulative_shapes': cnt,
                   'cumulative_violations': len(viol)})
    out.append({'section': 'strip_z18_m12_16', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) s=12 boundary special-child spots
    d1 = H(30, tuple(sorted((12, 11), reverse=True)), 18)
    d1v = v(23, 18, 30)
    d2 = H(31, tuple(sorted((13, 11), reverse=True)), 18)
    d2v = v(24, 18, 31)
    d3 = H(31, tuple(sorted((13, 12), reverse=True)), 17)
    d3v = v(25, 17, 31)
    out.append({'section': 'boundary_s12_special_children',
                'label': 'observational_only_the_three_positions_outside_published_cover',
                'rows': [
                    {'id': 'd1_rung12_i_ii_child', 'R': 30, 'z': 18,
                     'X': [12, 11], 'value': d1, 'collapse': d1v,
                     'match': d1 == d1v,
                     'published_status': 'member of the published m=11-row z=18 record (110 shapes, 0 separations) - cross-artifact'},
                    {'id': 'd2_rung13_i_child', 'R': 31, 'z': 18,
                     'X': [13, 11], 'value': d2, 'collapse': d2v,
                     'match': d2 == d2v,
                     'published_status': 'UNPUBLISHED position (min 11, R=31, z=18); candidate collapse'},
                    {'id': 'd3_rung13_iii_child', 'R': 31, 'z': 17,
                     'X': [13, 12], 'value': d3, 'collapse': d3v,
                     'match': d3 == d3v,
                     'published_status': 'UNPUBLISHED position (min 12, R=31, z=17, one above the T-Z17 m=12 claim); simultaneous min-drop probe of the proved m=13-row z=17 claim value v(25,17,31); candidate collapse'}]})
    # (e) strip spots m in 17..20
    spots = []
    for m in range(17, 21):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 19, X, 18)
            ev = v(S, 18, m + 19)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    out.append({'section': 'strip_spots_m17_20', 'rows': spots})
    # m=12 base spot (S=24, both 12-tokens) at the candidate T-Z18
    # (min>=12) base position; published member of the m=12-row z=18
    # 92-shape record (cross-artifact).
    w = H(31, (12, 12), 18)
    wv = v(24, 18, 31)
    out.append({'section': 'm12_base_spot', 'X': [12, 12], 'R': 31,
                'z': 18, 'value': w, 'collapse_single': wv,
                'match': w == wv,
                'published_crossref': 'member of the published m=12-row z=18 record (92 shapes, 0 separations; z18-min13 kit)'})
    # (f) below-band bottom-rung child census: H(19; Y; 19) vs v(s,19,19)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(12, 44)):
        ys = [()] if s == 0 else parts(s, 12, 4)
        vals = {}
        for y in ys:
            h = H(19, y, 19)
            vals.setdefault(h, []).append(y)
            bb_total += 1
        if len(vals) > 1:
            bb_multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s, 19, 19)
            if val != exp:
                bb_dev.append({'s': s, 'value': val, 'collapse': exp,
                               'direction': 'UP' if val > exp else 'DOWN',
                               'shapes': len(vals[val])})
    out.append({'section': 'belowband_j1_child_H19_19_floor12',
                'label': 'observational_only_belowband_supply_source_floor12_edition',
                'R': 19, 'z': 19, 'floor': 12,
                's_domain': '{0} U {12..43}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (g) supply identity rechecks (pure K0832 closed form)
    holds = []
    breaks = []
    for s in [0] + list(range(12, 56)):
        a = v(s, 19, 19)
        b = v(s, 18, 19)
        row = {'s': s, 'v_19_19': a, 'v_18_19': b, 'equal': a == b}
        (holds if a == b else breaks).append(row)
    out.append({'section': 'ninth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832_floor_independent',
                'identity': 'v(s,19,19) =? v(s,18,19)',
                's_domain': '{0} U {12..55}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z18-min13 census kit (f152a6f5): holds {0} U {12..17}, breaks 0v2 at s=18, then uniformly 2v1 for all s>=19; K1334 theorem A k=18 even instance; floor-independent (the floor-12 slice supply datum)',
                'hold_rows': holds, 'break_rows': breaks})
    z17_holds = []
    z17_breaks = []
    for s in [0] + list(range(12, 56)):
        a = v(s, 18, 18)
        b = v(s, 17, 18)
        row = {'s': s, 'v_18_18': a, 'v_17_18': b, 'equal': a == b}
        (z17_holds if a == b else z17_breaks).append(row)
    out.append({'section': 'z17_partner_identity_recheck',
                'label': 'observational_only_recheck_of_published_K1325_supply_identity',
                'identity': 'v(s,18,18) =? v(s,17,18)',
                's_domain': '{0} U {12..55}',
                'hold_rows': z17_holds, 'break_rows': z17_breaks})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
