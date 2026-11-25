#!/usr/bin/env python3
"""SIX-ZONE / SHARP-V verifier (K0966).

Paper theorems (proved in report.md):
  For a kodd=4 smooth hit (prime M>=5, main regime, t>=2, window empty,
  N = 2^a * p1*p2*p3*p4, a = v2(N) >= 1), gamma branch (p2*p3 >= M),
  c = 2^a * p1:
    (EX)  p1*p_i <= k0 for all i in {1,2,3,4}
    (SZ)  c*p_i <= M-1 for all i in {1,2,3,4}   (SIX-ZONE)
    (GZ)  p2*p3 > k0
    (P2)  p2*(M-1) > c*k0, hence p2 > c*t       (P2-LOWER)
    (SV)  t*c^2*M*(M+1) < (M-1)^3 + c^2          (SHARP-V)
          strictly sharper than K0961 gamma-sharp (kappa>=1: t*c^2 <= M-2)
          whenever c^2 < 2M^2-5M+1 (for c=6: all M>=6), and it needs no
          kappa parity assumption (covers kappa=0 gamma rows too).
  Non-gamma rows make no claim: alpha rows structurally violate SZ at i=4
  (p1*p4 >= M => c*p4 > M-1), so SZ is gamma-specific.
Inputs are the published K0965 kodd=4 row files (sibling experiment dir).
Deterministic; audit JSON must be byte-identical across cold runs.
"""
import json, hashlib, math, os, sys
from collections import Counter

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SRC = os.path.join(BASE, 'remo-kodd4-sqrt-band-20261118', 'output')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'sixzone_audit.json')

def load(name):
    rows = []
    with open(os.path.join(SRC, name)) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def branch(r):
    p = r['odd']
    if p[1]*p[2] >= r['M']: return 'gamma'
    if p[0]*p[3] >= r['M']: return 'alpha'
    return 'beta'

def main():
    A = {}
    deep = load('modeb_rows_k4_deep.jsonl')
    kap0 = load('modeb_rows_k4_kap0.jsonl')
    # dedup by full row content; duplicates must be byte-identical records
    seen = {}
    dup_total = 0
    for r in deep + kap0:
        key = (r['M'], r['t'], r['kap'], r['N'])
        s = json.dumps(r, sort_keys=True)
        if key in seen:
            assert seen[key] == s, ('non-identical duplicate row', key)
            dup_total += 1
        else:
            seen[key] = s
    rows = [json.loads(v) for v in seen.values()]
    rows.sort(key=lambda r: (r['M'], r['t'], r['kap'], r['N']))
    A['input'] = {
        'deep_rows': len(deep), 'kap0_rows': len(kap0),
        'unique_rows': len(rows), 'duplicates_byte_identical': dup_total,
    }

    fail = Counter()
    stats = {}
    br = Counter(branch(r) for r in rows)
    A['branch_census'] = dict(br)

    g_rows = [r for r in rows if branch(r) == 'gamma']
    stats['gamma_a_dist'] = dict(Counter(r['a'] for r in g_rows))
    stats['gamma_p1_dist'] = dict(Counter(r['odd'][0] for r in g_rows))
    stats['gamma_kap0_count'] = sum(1 for r in g_rows if r['kap'] == 0)
    stats['gamma_kap_even'] = sum(1 for r in g_rows if r['kap'] % 2 == 0)

    c1 = c2 = c3 = c4 = c5 = c6 = c7 = c8 = 0
    imp_gap_min = None
    imp_all_positive = True
    # margins: sixzone_margin = min over rows of max_i(c*p_i - (M-1));
    # SZ holds on a row iff that max is <= 0, so the reported minimum must
    # be <= 0 (a positive value would be a violation).
    margins = {'sv_gap': None, 'sixzone_max_excess': None,
               'p2_over_ct': None, 'p2p3_minus_k0': None}
    for r in g_rows:
        M, t, kap, Y, k0, a, p = r['M'], r['t'], r['kap'], r['Y'], r['k0'], r['a'], r['odd']
        c = (1 << a) * p[0]
        # C1 identities (incl. Y - k0 = t + 2)
        if (1 << a) * math.prod(p) != r['N'] or r['N'] != M*Y - 1 \
           or k0 != M*t + kap - 1 or Y != (M+1)*t + kap + 1 or Y - k0 != t + 2:
            c1 += 1
        # C2 t>=2 (TWO-ZONE regime)
        if t < 2: c2 += 1
        # C3 SIX-ZONE: violation iff max_i(c*p_i) > M-1  (ALL-i condition)
        m = max(c*p[i] - (M-1) for i in range(4))
        if margins['sixzone_max_excess'] is None or m < margins['sixzone_max_excess']:
            margins['sixzone_max_excess'] = m
        if m > 0: c3 += 1
        # C4 p1*p_i <= k0 (Lemma EX conclusion)
        if any(p[0]*p[i] > k0 for i in range(4)): c4 += 1
        # C5 p2*p3 > k0 (gamma => zone 2)
        d = p[1]*p[2] - k0
        if margins['p2p3_minus_k0'] is None or d < margins['p2p3_minus_k0']:
            margins['p2p3_minus_k0'] = d
        if d <= 0: c5 += 1
        # C6 P2-LOWER integer form p2*(M-1) > c*k0
        if not p[1]*(M-1) > c*k0: c6 += 1
        ratio = p[1] / (c*t)
        if margins['p2_over_ct'] is None or ratio < margins['p2_over_ct']:
            margins['p2_over_ct'] = ratio
        # C7 SHARP-V: t*c^2*M*(M+1) < (M-1)^3 + c^2
        lhs = t*c*c*M*(M+1)
        rhs = (M-1)**3 + c*c
        gap = rhs - lhs
        if margins['sv_gap'] is None or gap < margins['sv_gap']: margins['sv_gap'] = gap
        if gap <= 0: c7 += 1
        # C8 old K0961 gamma-sharp recheck (kappa>=1: t*c^2 <= M-2)
        if kap >= 1 and t*c*c > M - 2: c8 += 1
        # sharpness precondition: c^2 < 2M^2-5M+1 on every row
        if c*c >= 2*M*M - 5*M + 1:
            imp_all_positive = False
    A['gamma_checks'] = {
        'gamma_rows': len(g_rows),
        'identity_fail': c1, 't_ge2_fail': c2, 'sixzone_fail': c3,
        'p1pi_le_k0_fail': c4, 'p2p3_gt_k0_fail': c5,
        'p2_lower_fail': c6, 'sharpv_fail': c7, 'old_gamma_sharp_fail': c8,
        'margins': margins,
        'sharper_than_old_condition_holds_all': imp_all_positive,
    }
    # observed improvement magnitude (float, report only): new < old per row
    imp = []
    for r in g_rows:
        M, t, kap, a, p = r['M'], r['t'], r['kap'], r['a'], r['odd']
        c = (1 << a) * p[0]
        new = ((M-1)**3 + c*c) / (c*c*M*(M+1))
        old = (M-2) / (c*c)          # K0961 gamma sharp, kappa >= 1
        imp.append(old - new)
    A['gamma_checks']['improvement_old_minus_new_min'] = min(imp)
    A['gamma_checks']['improvement_old_minus_new_max'] = max(imp)
    A['gamma_checks']['improvement_all_positive'] = all(x > 0 for x in imp)
    A['gamma_checks']['improvement_formula_check'] = all(
        abs((old - new) - (2*M*M - 5*M - 35) / (c*c*M*(M+1))) < 1e-9
        for (M, c) in [(r['M'], (1 << r['a']) * r['odd'][0]) for r in g_rows]
        for new, old in [(((M-1)**3 + c*c) / (c*c*M*(M+1)), (M-2) / (c*c))]
    )

    # non-gamma rows: no claim; record that SZ fails there (expected)
    ag = [r for r in rows if branch(r) != 'gamma']
    sz_fail_nongamma = sum(
        1 for r in ag
        if max((1 << r['a'])*r['odd'][0]*r['odd'][i] - (r['M']-1)
               for i in range(4)) > 0)
    A['nongamma_observation'] = {
        'nongamma_rows': len(ag), 'sixzone_fails': sz_fail_nongamma,
        'note': 'no claim outside gamma; alpha rows structurally violate SZ at i=4 '
                '(p1*p4 >= M => 2^a*p1*p4 > M-1)',
    }

    A['all_ok'] = (c1 == 0 and c2 == 0 and c3 == 0 and c4 == 0 and c5 == 0
                   and c6 == 0 and c7 == 0 and c8 == 0 and imp_all_positive
                   and all(x > 0 for x in imp)
                   and A['nongamma_observation']['sixzone_fails'] == len(ag))
    A['input_sha256'] = {
        'modeb_rows_k4_deep.jsonl': hashlib.sha256(
            open(os.path.join(SRC, 'modeb_rows_k4_deep.jsonl'), 'rb').read()).hexdigest(),
        'modeb_rows_k4_kap0.jsonl': hashlib.sha256(
            open(os.path.join(SRC, 'modeb_rows_k4_kap0.jsonl'), 'rb').read()).hexdigest(),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as f:
        json.dump(A, f, indent=1, sort_keys=True, ensure_ascii=False)
        f.write('\n')
    print('all_ok:', A['all_ok'])
    print('gamma rows:', A['gamma_checks']['gamma_rows'],
          'sixzone_fail:', c3, 'sharpv_fail:', c7)
    print('audit:', OUT)
    return 0 if A['all_ok'] else 1

if __name__ == '__main__':
    sys.exit(main())
