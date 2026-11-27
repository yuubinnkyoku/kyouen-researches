#!/usr/bin/env python3
"""
explore_z24f19: FROZEN PRE-DECLARATION census for the z=24 min>=19
(floor-19) cell ladder and the T-Z24 strip (the z23-min18 census
continuation; NO K slot is claimed by this file; the constants below
were written BEFORE the first run of this file; publish-then-execute).

Slot check (pre-claim, per the registered handoffs): at kit-build time
the latest main contained NO T-Z24 declaration, NO z24-min19 critical
census kit, and no `explore_z24f19` (`explore_z24f19` / `T-Z24` /
`z24-min19` code probes -> only handoff references; the published
z24-floor18 kit log section 5 item 1 registers this lane as the
highest-information next target and the published m18spot/z25min20
kits explicitly did NOT take it). The z=24 floor-19 (z-5, CRITICAL)
census is therefore the slot this kit claims: the cell-ladder material
the future T-Z24 declaration lane consumes, exactly as the published
z22-min17 and z23-min18 kits did for K1339/K1344.

Scope (this file measures and reports; it proves nothing by itself):
  (a) cell census: for each j in 1..18 the floor-19 cell
      Cell_j(s) := H(j+25; {j} U Y; 24), Y tokens >= 19, s = sum(Y) in
      {0} U {19..49}, arity(Y) in 0..4 (0 only at s=0),
      swept EXHAUSTIVELY against the published raw engine (K1138
      recursion, embedded block byte-identical to the K1282..K1345
      chain, pin bd5f22e4...). Reported per cell: deviants from the
      Sigma-collapse v(s+j,24,j+25) (K0832 closed form) and any
      multivalue (decomposition-dependence) rows. The j=18 rung (small
      token 18, one rank beyond the published z=24 floor-18 A11-cell)
      is prefixed A12 as a PROVISIONAL census label; final naming
      belongs to the declaration lane.

      PREDECLARED CANDIDATES (written before the first run; primary
      derivation from the published z=22 EVEN profile (the PROVED
      K1339 cell lemmas F22f17..A1022f17) shifted +2 in position per
      the consecutive-even structural identity chain, with the z=23
      ODD-form classes at s=18 falling BELOW the floor-19 domain; the
      published z24-floor18 kit's measured 11-entry lattice is a
      DISCLOSED consistency anchor, NOT a premise -- the s-only premise
      is itself a candidate here; the FULL per-cell deviant list is
      written below so that nothing can be silently discovered and
      re-narrated -- lesson of the honest disclosure of the z21
      C-cell second deviant; measured constants recorded whatever
      they are):
      (i) deviant position set candidate {20, 22, 24}: the z=22 proved
          profile's {18, 20, 22} shifted +2 (even->even lattice step
          z 22->24, floor 17->19), i.e. the z=23 measured set
          {18, 20, 22} with the s=18 triplet EXCLUDED below the
          floor-19 domain -- the THIRD odd->even oldest-station death
          (z=19->20 killed s=14, z=21->22 killed s=16, z=23->24 kills
          s=18 = the z=23 A RANK BREAK REBIRTH position), the SIXTH
          definition-domain exclusion event of the series; NO newborn
          at s=19 (the even form carries no A-rank birth: the A-break
          position z-5=19 is an ODD s at even z and no odd-s A-rank
          deviant class has ever been observed);
      (ii) the FULL predeclared per-cell deviant lists (the exact +2
           shift of the PROVED z=22 profile):
             F24f19: {24: UP 1v0}                       (single point at
                                                       s=24=z, even
                                                       form, NO hole,
                                                       NO tail; the
                                                       single@(even z)
                                                       typology would
                                                       reach TEN
                                                       consecutive
                                                       consistent
                                                       slices z15..z24,
                                                       even-z single
                                                       form 6/6);
             G24f19: {22: DOWN 0v2, 24: UP 2v1};
             E24f19: {22: UP 1v0};
             D24f19: {20: DOWN 0v2, 22: UP 2v1};
             C24f19: {20: UP 1v0};
             B24f19: {20: UP 2v1};
             A..A12: fully collapsed (12 rungs; at even z the A-break
                     position z-5=19 is an odd s and no odd-s A-rank
                     deviant class has ever been observed -- the
                     A-break extinction/rebirth alternation continues:
                     reborn at z=23 (s=18, K1344), candidate extinct
                     again at z=24; extinction would graduate to 6/6
                     even slices z=14/16/18/20/22/24);
      (iii) the station structure: {D,C,B}@20 = {DOWN 0v2, UP 1v0,
            UP 2v1} and {G,E,D}@22 = {DOWN 0v2, UP 1v0, UP 2v1} and
            {F,G}@24 = {UP 1v0, UP 2v1} (the two-cell lattice head) --
            the even-form station triplet {DOWN 0v2, UP 1v0, UP 2v1},
            the EXACT parity mirror of the z=23 odd-form triplet
            {DOWN 1v2, DOWN 0v1, UP 2v0} (K1344 census 4/4);
      (iv) the F-cell single@(even z) typology: F deviates ONLY at
           s=24 (=z) as UP 1v0 and CONFORMS for ALL s in
           {19..23} U {25..49} U {50..57} (no hole, no persistent
           tail; contrast the z=23 odd HOLE+TAIL form);
      (v) A2..A12 fully collapsed (the ELEVEN consecutive full
          collapses after the A-boundary rung); A1224f19 (small token
          18, z*(18)=2*18-2+(18 mod 2)=34 > 24) is the candidate
          TENTH consecutive in-band base child; its j=18 C-hand
          child (42; {18} U Y; 23) is the published T-Z23 m=18-row
          claim position ITSELF (K1344 proved theorem T-Z23:
          H(42; X; 23) = v(sumX, 23, 42) for all min(X)=18), and the
          j=1..17 C-hand children (j+24; {j} U Y; 23) land on the
          PROVED K1344 floor-18 cells (co-floor 18 subset argument:
          Y tokens >= 19 >= 18 sit inside the K1344 lemma domain) --
          the whole declaration-lane supply side is PROVED material;
      (vi) all cells s-only, multivalue rows 0;
      (vii) head row s=19: ALL-CONFORMING candidate (the even-profile
            lowest station is at s=20; no deviant class below 20
            survives the z=23->24 step).
  (b) tail spots: s in {50..57}, single-token shape Y=(s,), all 18
      cells; candidate: ALL match (even z -- no F tail form; the
      z=23 odd-form 8/8 F value-2 tail signature absent); crosscheck
      anchor: the published z24-floor18 kit's own tail spots measured
      all-match at the same (j, s) shapes.
  (c) strip sweep (T-Z24 claim position, PROVISIONAL label): m in
      {19..23}, S in {m..m+39}, Y parts tokens >= m, arity(Y) <= 3:
      H(m+25; X; 24) vs v(S,24,m+25). EXHAUSTIVE in-sweep; candidate
      0 violations; CROSS-ARTIFACT recheck: the published z24-floor18
      kit strip m in {18..23} measured cumulative 28/51/71/90/108/125
      shapes 0 violations -- the m in {19..23} segments here enumerate
      the SAME shapes, candidate per-m deltas 23/20/19/18/17,
      cumulative 97, 0 violations.
  (d) IN-BAND base-child / m=18-row record (the structurally decisive
      section; observational only, NOT a T-Z24 claim position): the
      T-Z24 base m=19 a=19 child lands at (43; {18} U Y; 24) = the
      m=18-row position H(43; X; 24), and z=24 is IN BAND for min=18
      (z*(18) = 34 > 24), the TENTH consecutive slice whose base child
      is in-band -- the row is simultaneously the FIRST entry of the
      K1344-registered T-Z23 residual band m=18 z in {24..33}
      (frontier z*(18)=34; band registered by the published K1344
      corollary). Swept: S in {18..56}, all parts >= 18 (co-token 18
      shapes INCLUDED, X[0]=18), arity <= 3, recorded against the
      Sigma-collapse v(S,24,43) with every separation listed, PLUS an
      arity<=4 co-token-style extension sweep; CROSS-ARTIFACT recheck:
      the published z24-floor18 kit measured this row 26/0 + ext
      25/0 -- candidate identical counts, 0 separations.
  (d2) IN-BAND m=17-row z=24 record: the THIRD entry of the future
       T-Z22 residual band m=17 z in {23..32} (z=23 entry 32+31/0 by
       the z23-min18 kit; z=24 entry 32/0 by the z24-floor18 kit);
       SAME enumeration -> same 32 shapes, cross-artifact recheck,
       candidate 0 separations.
  (d3) IN-BAND m=16-row z=24 record: the FOURTH entry of the future
       T-Z21 residual band m=16 z in {22..29} (z=22 40/0, z=23 40/0,
       z=24 40/0 by the published kits); same 40 shapes, recheck.
  (d4) IN-BAND m=15-row z=24 record: the FIFTH entry of the K1335
       published residual band m=15 z in {21..28} (z=21..24); same 50
       shapes, recheck.
  (d5) IN-BAND m=14-row z=24 record: the SIXTH entry of the K1330
       published residual band m=14 z in {20..25}; same 62 shapes,
       recheck.
  (d6) IN-BAND m=13-row z=24 record: the SIXTH AND FINAL entry of
       the K1328 published residual band m=13 z in {19..24} -- the
       band CLOSES at z=24 (z*(13)=25 > 24 by one point, the
       closest-to-frontier row record of the series); same 76 shapes,
       recheck, candidate 0 separations.
  (NOT swept: the m=12-row z=24 record -- the K1325 published band
  m=12 z in {18..21} was CLOSED at z=21; no band entry exists at z=24.)
  (e) strip spots: m in {24..27}, X in {(m,m+1),(m,m+2),(m,m,m+1)}
      (cross-artifact recheck of the published z24-floor18 12/12), plus
      the m=19 base spot X=(19,19) at the T-Z24 slice base position
      H(44;(19,19);24) -- never measured by any published kit;
      candidate value 0 from the base-spot z-parity sequence
      0(z16),1(z17),0(z18),1(z19),0(z20),1(z21),0(z22),1(z23) -- the
      NINTH point, even z=24; NOTE the z24-floor18 kit's section-5
      item-3 registration of the m=18-row spot H(43;(18,18);24)=1
      (measured conforming) is a DIFFERENT sequence point (m=18 fixed,
      z-varying), rechecked here as a published anchor.
  (f) below-band bottom-rung child census (the z=24 analog of the
      K1320/K1322/K1325/K1328/z19/z20/z21/z22/z23 section-(f) censuses;
      observational only): the j=1 rung's B-move child is the
      BELOW-BAND position (25; Y; 25) (min(Y) >= 19 so R=25 lies deep
      below z'+min(Y) >= 44). This section measures the z=24 child
      directly at the FLOOR-19 shape set (H(25;Y;25) vs v(s,25,25),
      s in {0} U {19..49}, arity(Y) in 0..4) -- a DIFFERENT shape set
      from the published z24-floor18 kit's floor-18 version (89/0);
      candidate: full collapse, the TENTH consecutive below-band full
      collapse; the proof belongs to the declaration lane (BB-lemma
      stair R=25 <= 25+min(Y)).
  (g) TAIL SUPPLY BATTERY (pure published K0832 closed form, NO
      engine recursion; per the published K1345 theorem handoff item
      2 these d=1 identities are now PROVED universal corollaries of
      the K1345 d-shift family -- the rechecks here are the prescribed
      small battery spot-checks, NOT new pre-computations; the k=27..31
      chain is already precomputed by the published z23-floor17 /
      z24-floor18 / m18spot kits and k=32 by the published tail22
      handoff kit):
      (g1) FIFTEENTH-tail identity RECHECK (the z=24 slice supply
          datum): v(s,25,25) =? v(s,24,25) over s in {0} U {12..61}.
          Published anchors: the z22-min17 kit (g3) measured hold
          {0} U {12..23}, 0v2 break at s=24, uniform 2v1 for s >= 25;
          rechecked by the z23-min18 (g2) and z24-floor18 kits.
          Candidate: hold {0} U {12..23}, 0v2 at s=24, uniform 2v1
          for all s in {25..61}.
      (g2) SIXTEENTH-tail identity RECHECK (the z=25 slice supply
          datum): v(s,26,26) =? v(s,25,26) over s in {0} U {12..61}.
          Published anchors: the z23-min18 kit (g3) precomputed hold
          {0} U {12..25}, UNIFORM 0v1 for all s >= 26 (both components
          predeclared and confirmed); rechecked by the z24-floor18
          kit. Candidate: hold {0} U {12..25}, uniform 0v1 for all s
          in {26..61}.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z24f19.out).

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
    """sweep cell_j over s in {0} U {19..smax}; returns (dev, multi, total)"""
    R = j + 25
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(19, smax + 1)):
        ys = [()] if s == 0 else parts(s, 19, 4)
        vals = {}
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            h = H(R, X, 24)
            vals.setdefault(h, []).append(y)
            total += 1
        if len(vals) > 1:
            multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s + j, 24, R)
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
    for j in range(1, 19):
        name = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
                'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12'][j - 1]
        dev, multi, total = cell_sweep(j, 49)
        cells[f'cell{j}_{name}24f19'] = {
            'z': 24, 'min': j, 'R': j + 25, 'floor': 19,
            's_domain': '{0} U {19..49}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}24f19',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 19):
        nm = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
              'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12'][j - 1]
        for s in range(50, 58):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 25, X, 24)
            exp = v(s + j, 24, j + 25)
            tail.append({'cell': f'{nm}24f19', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s50_57', 'rows': tail})
    # (c) strip sweep m in 19..23 (T-Z24 claim position, provisional)
    sv = []
    viol = []
    cnt = 0
    for m in range(19, 24):
        H.cache_clear()
        for S in range(m, m + 40):
            for X in parts(max(S - m, 0), m, 3):
                XX = tuple(sorted((m,) + X, reverse=True))
                if sum(XX) != S:
                    continue
                hv = H(m + 25, XX, 24)
                ev = v(S, 24, m + 25)
                cnt += 1
                if hv != ev:
                    viol.append({'m': m, 'X': list(XX), 'S': S,
                                 'value': hv, 'collapse': ev})
        sv.append({'m': m, 'cumulative_shapes': cnt,
                   'cumulative_violations': len(viol)})
    out.append({'section': 'strip_z24_m19_23', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) IN-BAND base-child / m=18-row record at the z=24 m=18 row
    #     position (43; X; 24), all parts >= 18 (co-token 18 allowed),
    #     arity <= 3 TOTAL. Observational only: NOT a T-Z24 claim
    #     position. FIRST entry of the K1344-registered T-Z23 residual
    #     band m=18 z in {24..33}; simultaneously the T-Z24 base m=19
    #     a=19 child, TENTH consecutive in-band base child.
    out.append(row_record_x0(
        'inband_m18_z24_row_record',
        'observational_only_base_child_in_band_zstar18_34_gt_24_tenth_consecutive_first_tz23_band_entry',
        {'co_token_18_allowed': True,
         'residual_band': 'FIRST entry of the K1344-registered T-Z23 residual band m=18 z in {24..33} (frontier z*(18)=34 per the K1268 formula z*(m)=2m-2+(m mod 2)); the row is simultaneously the T-Z24 base m=19 a=19 child, the TENTH consecutive in-band base child; cross-artifact recheck of the published z24-floor18 kit entry 26/0',
         's_domain': '{18..56}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        43, 24, 18, 18, 56))
    out.append(row_record(
        'inband_m18_z24_row_record_ext_arity4',
        'observational_only_arity_le4_extension_of_the_m18_z24_record_cotoken_style',
        {'co_token_18_allowed': True,
         's_domain': '{18..56}', 'arity_max': 4},
        43, 24, 18, 18, 56, 18))
    # (d2) IN-BAND m=17-row z=24 record: THIRD entry of the future
    #      T-Z22 residual band m=17 z in {23..32} (z=23 32+31/0, z=24
    #      32/0 by the published kits), published record style.
    out.append(row_record_x0(
        'inband_m17_z24_row_record',
        'observational_only_future_tz22_residual_m17_z24_third_entry_zstar17_33_gt_24_cross_artifact_recheck',
        {'co_token_17_allowed': True,
         'residual_band': 'future T-Z22 residual band m=17 z in {23..32}; z=23 entry (z23-min18 kit) 32+31 shapes 0 seps; z=24 entry (z24-floor18 kit) 32/0; same enumeration -> same 32 shapes here',
         's_domain': '{17..55}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        42, 24, 17, 17, 55))
    # (d3) IN-BAND m=16-row z=24 record: FOURTH entry of the future
    #      T-Z21 residual band m=16 z in {22..29}.
    out.append(row_record_x0(
        'inband_m16_z24_row_record',
        'observational_only_future_tz21_residual_m16_z24_fourth_entry_zstar16_30_gt_24_cross_artifact_recheck',
        {'co_token_16_allowed': True,
         'residual_band': 'future T-Z21 residual band m=16 z in {22..29}; z=22 40/0, z=23 40/0, z=24 (z24-floor18 kit) 40/0; same enumeration -> same 40 shapes here',
         's_domain': '{16..54}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        41, 24, 16, 16, 54))
    # (d4) IN-BAND m=15-row z=24 record: FIFTH entry of the K1335
    #      published residual m=15 z in {21..28}.
    out.append(row_record_x0(
        'inband_m15_z24_row_record',
        'observational_only_k1335_residual_m15_z24_fifth_entry_zstar15_29_gt_24_cross_artifact_recheck',
        {'co_token_15_allowed': True,
         'residual_band': 'K1335 published m=15 z in {21..28}; z=21..24 entries 50/0 each (z=24 by the z24-floor18 kit); same enumeration -> same 50 shapes here',
         's_domain': '{15..53}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        40, 24, 15, 15, 53))
    # (d5) IN-BAND m=14-row z=24 record: SIXTH entry of the K1330
    #      published residual m=14 z in {20..25}.
    out.append(row_record_x0(
        'inband_m14_z24_row_record',
        'observational_only_k1330_residual_m14_z24_sixth_entry_zstar14_26_gt_24_cross_artifact_recheck',
        {'co_token_14_allowed': True,
         'residual_band': 'K1330 published m=14 z in {20..25}; z=20..24 entries 62/0 each; same enumeration -> same 62 shapes here',
         's_domain': '{14..52}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        39, 24, 14, 14, 52))
    # (d6) IN-BAND m=13-row z=24 record: SIXTH AND FINAL entry of the
    #      K1328 published residual m=13 z in {19..24} -- the band
    #      CLOSES at z=24 (z*(13)=25 > 24 by one point).
    out.append(row_record_x0(
        'inband_m13_z24_row_record',
        'observational_only_k1328_residual_m13_z24_sixth_final_entry_band_closes_zstar13_25_gt_24_cross_artifact_recheck',
        {'co_token_13_allowed': True,
         'residual_band': 'K1328 published m=13 z in {19..24}; z=19..24 entries 76/0 each (z=24 by the z24-floor18 kit, the closest-to-frontier row record of the series); same enumeration -> same 76 shapes here; the band CLOSES at z=24',
         's_domain': '{13..51}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        38, 24, 13, 13, 51))
    # (NOT swept: m=12-row -- the K1325 band m=12 z in {18..21} closed
    #  at z=21; no band entry exists at z=24.)
    # (e) strip spots m in 24..27
    spots = []
    for m in range(24, 28):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 25, X, 24)
            ev = v(S, 24, m + 25)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    out.append({'section': 'strip_spots_m24_27', 'rows': spots})
    # m=19 base spot (S=38, both 19-tokens) at the T-Z24 slice base
    # position
    w = H(44, (19, 19), 24)
    wv = v(38, 24, 44)
    out.append({'section': 'm19_base_spot', 'X': [19, 19], 'R': 44,
                'z': 24, 'value': w, 'collapse_single': wv,
                'match': w == wv,
                'published_probe_crossref': 'NEW measurement: no published kit measured H(44;(19,19);24); candidate 0 from the base-spot z-parity sequence 0(z16),1(z17),0(z18),1(z19),0(z20),1(z21),0(z22),1(z23) -- the NINTH point, even z=24'})
    # published anchor recheck: the z24-floor18 kit's m=18-row spot
    a = H(43, (18, 18), 24)
    av = v(36, 24, 43)
    out.append({'section': 'm18row_published_anchor_recheck',
                'X': [18, 18], 'R': 43, 'z': 24, 'value': a,
                'collapse_single': av, 'match': a == av,
                'published_anchor': 'z24-floor18 kit m18_base_spot measured value 1 (conforming v(36,24,43)=1); candidate identical'})
    # (f) below-band bottom-rung child census: H(25; Y; 25) vs v(s,25,25)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(19, 50)):
        ys = [()] if s == 0 else parts(s, 19, 4)
        vals = {}
        for y in ys:
            h = H(25, y, 25)
            vals.setdefault(h, []).append(y)
            bb_total += 1
        if len(vals) > 1:
            bb_multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s, 25, 25)
            if val != exp:
                bb_dev.append({'s': s, 'value': val, 'collapse': exp,
                               'direction': 'UP' if val > exp else 'DOWN',
                               'shapes': len(vals[val])})
    out.append({'section': 'belowband_j1_child_H25_25',
                'label': 'observational_only_belowband_supply_source_at_z24_floor19_shape_set',
                'R': 25, 'z': 25, 'floor': 19,
                's_domain': '{0} U {19..49}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (g1) FIFTEENTH-TAIL SUPPLY IDENTITY RECHECK (pure K0832 closed form)
    holds = []
    breaks = []
    for s in [0] + list(range(12, 62)):
        a1 = v(s, 25, 25)
        b1 = v(s, 24, 25)
        row = {'s': s, 'v_25_25': a1, 'v_24_25': b1, 'equal': a1 == b1}
        (holds if a1 == b1 else breaks).append(row)
    out.append({'section': 'fifteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832_k1345_corollary_battery',
                'identity': 'v(s,25,25) =? v(s,24,25)',
                's_domain': '{0} U {12..61}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion; PROVED universal by the published K1345 d-shift theorem (d=1 slice); this recheck is the prescribed small battery spot-check',
                'published_anchor': 'z22-min17 kit (g3): holds {0} U {12..23}, 0v2 break at s=24, then uniformly 2v1 for all s>=25; rechecked by the z23-min18 (g2) and z24-floor18 kits; candidate hold {0} U {12..23}, 0v2 at s=24, uniform 2v1 for all s in {25..61}',
                'hold_rows': holds, 'break_rows': breaks})
    # (g2) SIXTEENTH-TAIL SUPPLY IDENTITY RECHECK (published anchor)
    t_holds = []
    t_breaks = []
    for s in [0] + list(range(12, 62)):
        a2 = v(s, 26, 26)
        b2 = v(s, 25, 26)
        row = {'s': s, 'v_26_26': a2, 'v_25_26': b2, 'equal': a2 == b2}
        (t_holds if a2 == b2 else t_breaks).append(row)
    out.append({'section': 'sixteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832_k1345_corollary_battery',
                'identity': 'v(s,26,26) =? v(s,25,26)',
                's_domain': '{0} U {12..61}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion; PROVED universal by the published K1345 d-shift theorem (d=1 slice); this recheck is the prescribed small battery spot-check',
                'published_anchor': 'z23-min18 kit (g3) precompute (both components predeclared, confirmed): holds {0} U {12..25}, UNIFORM 0v1 for all s>=26; rechecked by the z24-floor18 kit; candidate hold {0} U {12..25}, uniform 0v1 for all s in {26..61}',
                'hold_rows': t_holds, 'break_rows': t_breaks})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
