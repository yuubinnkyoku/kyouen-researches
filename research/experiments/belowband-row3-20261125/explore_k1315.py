#!/usr/bin/env python3
"""explore_k1315: FROZEN pre-declaration exploration for the K1315 packet
(third below-band row k = z+n-5; observation packet OBS-BBL3 + transcription
lemma L-BR3 + unifying conjecture CONJ-BBL3).

Row-3 canonical value under study:  H(S+z+n-5, X, z)  for a descending heap
multiset X of length n, plane z >= 0, with S = sum(X).  Coordinates:
  E := 2*max(X) - S   (sub-band depth; E = x1 - x2 - ... - xn)
  w := E + z         (the row-3 diagonal coordinate)
  j := number of 1-heaps
  m2 := smallest heap >= 2 (None if all heaps are 1s)
  c2 := number of 2-heaps

Waves (all deterministic; JSON on stdout; frozen as explore_k1315.out):
  WA  L-BR3 transcription: single-token slice of row 3 (n=1, k=z-4,
      R = x+z-4) must equal the published K0832 closed form `single_token`
      on a x,z <= 30 grid.  Machine-verified lemma (grid scope).
  WB  raw-layer non-collapse: value as a function of (E,z) merged over all
      instances of one n is heavily multi-valued (the negative observation:
      row 2's (E,w)-collapse does NOT persist on the raw layer).
  WC  class-layer census: within a layer (n,j) the (E,z) table is almost
      collapse-clean; residual multivalue cells listed with deviants.
  WD  anchor census: the 2-line of each (n,j) class sits at w = A
      (per-family constants).  Full vote tables by (m2,c2), incl. the n=7
      class-(7,0) two-family split (m2=2 -> A=-15; m2>=3 -> A=-17) and the
      four-level n=8 j=0 tail ladder.  Flat spot at j = n-3.
  WE  suppression: rows with no in-window 2 occur exactly when the line
      would hit the z=0 wall (E >= A); anomalies (E < A, no 2) listed.
  WF  3-piece law conformance per measured family anchor:
      V = 2 on the line, [E even] left, [E odd] right; genuine law
      violations listed; rows that satisfy the law but whose measured
      anchor is off the class modal levels are counted separately as
      off_level (declared small-instance outliers), not violations.
  WG  seeded random sweep (seed 1315) beyond the grid families.

Everything here is OBSERVATION grade over the stated swept grids unless a
wave says "machine-verified"; no universal theorem is claimed.  CONJ-BBL3
(the conjecture lifting these tables to all instances) is stated in the
declaration note, not proven here.
"""
import hashlib
import json
import random
import sys
from collections import defaultdict
from itertools import combinations_with_replacement
from functools import lru_cache

sys.setrecursionlimit(100000)

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

sha = hashlib.sha256(ENGINE_BLOCK.encode('utf-8')).hexdigest()
assert sha == 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92', sha
exec(ENGINE_BLOCK)

REPORT = {'engine_sha': sha}

# ------------------------------------------------------------------
# WA: L-BR3 transcription (single-token slice of row 3).
# ------------------------------------------------------------------
wa = {'cells': 0, 'mismatch': []}
for x in range(1, 31):
    for z in range(0, 31):
        R = x + z - 4
        if R < 0:
            continue
        wa['cells'] += 1
        if H_canonical(R, (x,), z) != single_token(x, z, R):
            wa['mismatch'].append([x, z, R])
wa['pass'] = (wa['cells'] == 924 and not wa['mismatch'])
REPORT['WA_LBR3'] = wa

# ------------------------------------------------------------------
# Shared scan machinery (all later waves reuse these rows).
# ------------------------------------------------------------------
GRID = {3: (12, 16), 4: (10, 15), 5: (9, 13), 6: (7, 12), 7: (6, 12)}


def row_vals(Xd, n, zmax):
    S = sum(Xd)
    out = []
    for z in range(0, zmax + 1):
        R = S + z + n - 5
        out.append(H_canonical(R, Xd, z) if R >= 0 else None)
    return out


def feats(Xd):
    j = sum(1 for t in Xd if t == 1)
    m2l = [t for t in Xd if t >= 2]
    m2 = min(m2l) if m2l else None
    c2 = sum(1 for t in Xd if t == 2)
    return j, m2, c2


def sweep_rows(n, hi, zmax, heapmin=1):
    rows = []
    for X in combinations_with_replacement(range(heapmin, hi + 1), n):
        Xd = tuple(sorted(X, reverse=True))
        S = sum(Xd)
        E = 2 * Xd[0] - S
        vs = row_vals(Xd, n, zmax)
        H_canonical.cache_clear()
        j, m2, c2 = feats(Xd)
        twos = [z for z, v in enumerate(vs) if v == 2]
        rows.append({'X': Xd, 'S': S, 'E': E, 'j': j, 'm2': m2, 'c2': c2,
                     'vals': vs, 'twos': twos})
    return rows


ROWS = {}
for n, (hi, zmax) in sorted(GRID.items()):
    ROWS[n] = sweep_rows(n, hi, zmax, heapmin=1)
N8 = {'j0': sweep_rows(8, 6, 16, heapmin=2)}
# n=8 j=1/j=2 rows (explicit enumeration: j ones + heaps 2..6)
for key, jcount in (('j1', 1), ('j2', 2)):
    rows = []
    for Y in combinations_with_replacement(range(2, 7), 8 - jcount):
        Xd = tuple(sorted(Y, reverse=True)) + (1,) * jcount
        S = sum(Xd)
        E = 2 * Xd[0] - S
        vs = row_vals(Xd, 8, 14)
        H_canonical.cache_clear()
        jj, m2, c2 = feats(Xd)
        twos = [z for z, v in enumerate(vs) if v == 2]
        rows.append({'X': Xd, 'S': S, 'E': E, 'j': jj, 'm2': m2, 'c2': c2,
                     'vals': vs, 'twos': twos})
    N8[key] = rows

# ------------------------------------------------------------------
# WB: raw-layer (E,z) non-collapse, per n (negative observation).
# ------------------------------------------------------------------
wb = {}
for n in sorted(ROWS):
    tab = defaultdict(lambda: defaultdict(list))
    for r in ROWS[n]:
        for z, v in enumerate(r['vals']):
            if v is None:
                continue
            tab[(r['E'], z)][v].append(r['X'])
    multi = sorted([k for k, d in tab.items() if len(d) > 1])
    wb[n] = {'cells': len(tab), 'multivalue_cells': len(multi),
             'examples': {f'{k[0]},{k[1]}': {v: xs[:2] for v, xs in sorted(tab[k].items())}
                          for k in multi[:6]}}
REPORT['WB_raw_layer_noncollapse'] = wb

# ------------------------------------------------------------------
# WC: class-layer (n,j) census with full deviant bookkeeping.
# ------------------------------------------------------------------
wc = {}
for n in sorted(ROWS):
    cls = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for r in ROWS[n]:
        for z, v in enumerate(r['vals']):
            if v is None:
                continue
            cls[r['j']][(r['E'], z)][v].append(r['X'])
    wc[n] = {}
    for j in sorted(cls):
        cells = cls[j]
        multi = sorted([k for k, d in cells.items() if len(d) > 1])
        wc[n][j] = {
            'cells': len(cells), 'multivalue': len(multi),
            'deviants': {f'{k[0]},{k[1]}': {v: xs[:2] for v, xs in sorted(cells[k].items())}
                         for k in multi[:24]},
        }
REPORT['WC_class_census'] = wc

# ------------------------------------------------------------------
# WD: anchor (2-line) census per (n,j); levels, votes, (m2,c2) breakdown.
# ------------------------------------------------------------------
def vote_table(rows):
    votes = defaultdict(int)
    byfeat = defaultdict(lambda: defaultdict(int))
    for r in rows:
        if len(r['twos']) == 1:
            A = r['E'] + r['twos'][0]
            votes[A] += 1
            byfeat[A][f'm2={r["m2"]},c2={r["c2"]}'] += 1
    return votes, byfeat


wd = {}
for n in sorted(ROWS):
    wd[str(n)] = {}
    byj = defaultdict(list)
    for r in ROWS[n]:
        byj[r['j']].append(r)
    for j in sorted(byj):
        votes, byfeat = vote_table(byj[j])
        total = sum(votes.values())
        wd[str(n)][j] = {'votes': dict(sorted(votes.items())),
                    'total_single2': total,
                    'by_m2c2': {A: dict(sorted(byfeat[A].items())) for A in sorted(byfeat)}}
wd['8'] = {}
for key, jtag in (('j0', 0), ('j1', 1), ('j2', 2)):
    votes, byfeat = vote_table(N8[key])
    wd['8'][jtag] = {'votes': dict(sorted(votes.items())),
                     'total_single2': sum(votes.values()),
                     'by_m2c2': {A: dict(sorted(byfeat[A].items())) for A in sorted(byfeat)}}
REPORT['WD_anchor_census'] = wd

# ------------------------------------------------------------------
# WE+WF: suppression census and 3-piece law conformance per class.
# Levels = A-values with >= 3 votes in WD (deterministic threshold).
# ------------------------------------------------------------------
wef = {}
for n in sorted(ROWS):
    byj = defaultdict(list)
    for r in ROWS[n]:
        byj[r['j']].append(r)
    wef[n] = {}
    for j in sorted(byj):
        rows = byj[j]
        votes, _ = vote_table(rows)
        levels = sorted([A for A, c in votes.items() if c >= 3])
        n_line = n_supp_ok = n_supp_bad = n_mult2 = 0
        line_conform = line_violate = off_level = 0
        viol_ex = []
        off_ex = []
        anom = []
        for r in rows:
            E = r['E']
            nt = len(r['twos'])
            if nt == 1:
                n_line += 1
                A = E + r['twos'][0]
                ok = A in levels
                bad = 0
                for z, v in enumerate(r['vals']):
                    if v is None:
                        continue
                    w = E + z
                    pred = 2 if w == A else (E % 2 == 0 if w < A else E % 2 == 1)
                    if v != pred:
                        bad += 1
                if bad == 0:
                    if ok:
                        line_conform += 1
                    else:
                        off_level += 1
                        if len(off_ex) < 6:
                            off_ex.append([r['X'], E, r['twos'], r['vals'], A, levels])
                else:
                    line_violate += 1
                    if len(viol_ex) < 6:
                        viol_ex.append([r['X'], E, r['twos'], r['vals'], A, levels])
            elif nt == 0:
                if any(E >= A for A in levels):
                    pred = (E % 2 == 1)
                    bad = sum(1 for v in r['vals'] if v is not None and v != pred)
                    if bad == 0:
                        n_supp_ok += 1
                    else:
                        n_supp_bad += 1
                        if len(anom) < 6:
                            anom.append([r['X'], E, r['vals'], 'supp_violating'])
                else:
                    anom.append([r['X'], E, r['twos'], r['vals'], 'no2_below_line'])
                    anom = anom[:6]
            else:
                n_mult2 += 1
                if len(anom) < 10:
                    anom.append([r['X'], E, r['twos'], r['vals'], 'multi2'])
        wef[n][j] = {'levels': levels,
                     'line': n_line, 'line_conform': line_conform,
                     'line_violate': line_violate, 'line_violate_ex': viol_ex,
                     'off_level': off_level, 'off_level_ex': off_ex,
                     'supp_ok': n_supp_ok, 'supp_bad_violating': n_supp_bad,
                     'multi2': n_mult2, 'anomalies': anom}
REPORT['WEWF_suppression_and_law'] = wef

# n=8 conformance (same 3-piece logic, levels from its own votes)
wef8 = {}
for key, jtag in (('j0', 0), ('j1', 1), ('j2', 2)):
    rows = N8[key]
    votes, _ = vote_table(rows)
    levels = sorted([A for A, c in votes.items() if c >= 3])
    st = {'levels': levels, 'line': 0, 'line_conform': 0, 'line_violate': 0,
          'off_level': 0, 'supp_ok': 0, 'supp_bad_violating': 0,
          'multi2': 0, 'viol_ex': [], 'off_ex': []}
    for r in rows:
        E = r['E']
        nt = len(r['twos'])
        if nt == 1:
            st['line'] += 1
            A = E + r['twos'][0]
            bad = 0
            for z, v in enumerate(r['vals']):
                if v is None:
                    continue
                w = E + z
                pred = 2 if w == A else (E % 2 == 0 if w < A else E % 2 == 1)
                if v != pred:
                    bad += 1
            if bad == 0:
                if A in levels:
                    st['line_conform'] += 1
                else:
                    st['off_level'] += 1
                    if len(st['off_ex']) < 4:
                        st['off_ex'].append([r['X'], E, r['twos'], r['vals'], A])
            else:
                st['line_violate'] += 1
                if len(st['viol_ex']) < 4:
                    st['viol_ex'].append([r['X'], E, r['twos'], r['vals'], A])
        elif nt == 0:
            if any(E >= A for A in levels):
                pred = (E % 2 == 1)
                bad = sum(1 for v in r['vals'] if v is not None and v != pred)
                if bad == 0:
                    st['supp_ok'] += 1
                else:
                    st['supp_bad_violating'] += 1
            else:
                st['multi2'] += 1000000  # no-2 below line: should not happen
        else:
            st['multi2'] += 1
    wef8[f'8_{jtag}'] = st
REPORT['WEWF_n8'] = wef8

# ------------------------------------------------------------------
# WG: seeded random sweep (seed 1315).
# ------------------------------------------------------------------
rng = random.Random(1315)
st = {'samples': 0, 'line': 0, 'line_conform': 0, 'supp_ok': 0,
      'other': 0, 'violations': []}
for _ in range(150):
    n = rng.randint(3, 8)
    heaps = sorted((rng.randint(1, 8) for _ in range(n)), reverse=True)
    Xd = tuple(heaps)
    S = sum(Xd)
    E = 2 * Xd[0] - S
    vs = row_vals(Xd, n, 10)
    H_canonical.cache_clear()
    twos = [z for z, v in enumerate(vs) if v == 2]
    st['samples'] += 1
    if len(twos) == 1:
        st['line'] += 1
        A = E + twos[0]
        bad = sum(1 for z, v in enumerate(vs)
                   if v is not None and v != (2 if E + z == A else
                                               (E % 2 == 0 if E + z < A else E % 2 == 1)))
        if bad == 0:
            st['line_conform'] += 1
        elif len(st['violations']) < 12:
            st['violations'].append([Xd, n, E, twos, vs, A])
    elif not twos:
        # suppressed consistency candidate: whole window right of the line
        vals = set(v for v in vs if v is not None)
        if vals == {1 if E % 2 == 1 else 0}:
            st['supp_ok'] += 1
        else:
            st['other'] += 1
    else:
        st['other'] += 1
REPORT['WG_random_seed1315'] = st

print(json.dumps(REPORT, sort_keys=True, indent=1))
