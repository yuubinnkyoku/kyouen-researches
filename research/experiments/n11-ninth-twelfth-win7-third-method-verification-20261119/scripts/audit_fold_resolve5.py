#!/usr/bin/env python3
# Third-environment cross-check of the K1057 fold (9th..12th receipts) and resolve5
# (post-twelfth candidate cover) using only:
#   - resolve4 residual 86 rows (published record, local byte copy)
#   - sweep43 witness/census facts (independently re-derived in audit_sweep43.py)
#   - the published fold912 + resolve5 records (the claims UNDER TEST)
# Everything geometric is recomputed from scratch here (third algebra method).
# Output: PASS/FAIL gate table on stdout; if argv[2] given, machine JSON summary.
import json, sys, time

X = [b % 11 for b in range(121)]
Y = [b // 11 for b in range(121)]
S = [X[b]*X[b] + Y[b]*Y[b] for b in range(121)]
TF = []
for t in range(8):
    tab = []
    for p in range(121):
        x, y = p % 11, p // 11
        if t == 0: X_, Y_ = x, y
        elif t == 1: X_, Y_ = 10 - y, x
        elif t == 2: X_, Y_ = 10 - x, 10 - y
        elif t == 3: X_, Y_ = y, 10 - x
        elif t == 4: X_, Y_ = 10 - x, y
        elif t == 5: X_, Y_ = x, 10 - y
        elif t == 6: X_, Y_ = y, x
        else: X_, Y_ = 10 - y, 10 - x
        tab.append(11 * Y_ + X_)
    TF.append(tab)

def bits_of(mask):
    out = []
    while mask:
        low = mask & -mask
        out.append(low.bit_length() - 1)
        mask ^= low
    return out

def transform(mask, t):
    return sum(1 << TF[t][p] for p in bits_of(mask))

def canon(mask):
    return min(transform(mask, t) for t in range(8))

def canon_h(mask):
    return '%032x' % canon(mask)

def det3s(a, b, c):
    x1, y1, s1 = X[a], Y[a], S[a]
    x2, y2, s2 = X[b], Y[b], S[b]
    x3, y3, s3 = X[c], Y[c], S[c]
    A1, B1 = x2 - x1, y2 - y1
    A2, B2 = x3 - x1, y3 - y1
    W = A1 * B2 - A2 * B1
    if W == 0:
        dx, dy = x2 - x1, y2 - y1
        return lambda d: dx * (Y[d] - y1) - dy * (X[d] - x1) == 0
    C1, C2 = -(s2 - s1), -(s3 - s1)
    DD = C1 * B2 - C2 * B1
    EE = A1 * C2 - A2 * C1
    return lambda d: W * (S[d] - s1) + DD * (X[d] - x1) + EE * (Y[d] - y1) == 0

def is_safe_points(points):
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                test = det3s(points[i], points[j], points[k])
                for l in range(k + 1, n):
                    if test(points[l]):
                        return False
    return True

def coverage_rows(root_mask, universal):
    cov = set()
    for t in range(8):
        img = transform(root_mask, t)
        for b in bits_of(img):
            h = canon_h(img ^ (1 << b))
            if h in universal:
                cov.add(h)
    return cov

GATES = []
def gate(ok, name, detail=''):
    line = ('[PASS] ' if ok else '[FAIL] ') + name + ' ' + str(detail)
    print(line)
    GATES.append({'name': name, 'pass': bool(ok), 'detail': str(detail)})

def main(wd, out_json):
    t0 = time.time()
    r4 = json.load(open(f'{wd}/resolve4.json'))
    sweep = json.load(open(f'{wd}/sweep43.json'))
    fold = json.load(open(f'{wd}/fold912.json'))
    r5 = json.load(open(f'{wd}/resolve5.json'))

    residual86 = set(r4['resolve']['stranded_row_hex'])

    # universe for receipt-row checks: residual target rows + extra S6 rows claimed
    extra_rows = set()
    for rc in fold['receipts']:
        for h in (rc.get('extra_s6_rows_not_in_target') or []):
            extra_rows.add(h)
    check_universe = residual86 | extra_rows

    recs = {r['root']: r for r in sweep['witness_records']}
    closed_by_fold = []
    total_s6_covered = []
    gate(fold['receipt_count'] == 4 and [rc['receipt'] for rc in fold['receipts']] == ['ninth', 'tenth', 'eleventh', 'twelfth'],
         'four receipts ninth..twelfth')
    for rc in fold['receipts']:
        root = rc['root']
        m = int(root, 16)
        my_cov_any = coverage_rows(m, check_universe)
        rows_t = rc['covered_five_parent_target_rows']
        rows_s6 = list(rc.get('covered_s6_rows') or [])
        gate(set(rows_t) == my_cov_any & residual86,
             f'fold receipt {rc["receipt"]}: target rows == third-method coverage restricted to residual86', f'{sorted(rows_t)}')
        gate(set(rows_s6) == my_cov_any,
             f'fold receipt {rc["receipt"]}: covered_s6_rows == third-method coverage over residual86+extras', f'{sorted(rows_s6)}')
        gate(set(rc.get('extra_s6_rows_not_in_target') or []) == my_cov_any - residual86,
             f'fold receipt {rc["receipt"]}: extras == coverage minus residual86')
        gate(set(rows_s6) - residual86 == set(rc.get('extra_s6_rows_not_in_target') or []),
             f'fold receipt {rc["receipt"]}: S6 rows partition into target + extras')
        gate(recs[root]['covered_stranded_rows'] == rows_t, f'fold receipt {rc["receipt"]} rows == sweep43 witness rows')
        gate(len(rows_s6) == len(set(rows_s6)), f'fold receipt {rc["receipt"]} S6 rows unique', len(rows_s6))
        gate(m.bit_count() == 7, f'{rc["receipt"]} root 7 stones')
        gate(canon_h(m) == root, f'{rc["receipt"]} root D4-canonical')
        gate(is_safe_points(bits_of(m)), f'{rc["receipt"]} root safe (third method)')
        closed_by_fold.extend(rows_t)
        total_s6_covered.extend(rows_s6)
    gate(len(closed_by_fold) == 8, 'fold closed exactly 8 target rows', len(closed_by_fold))
    gate(len(set(closed_by_fold)) == 8, 'fold-receipt target rows disjoint')
    s6_all = set(total_s6_covered)
    gate(len(s6_all) == 9, 'nine S6 rows closed in total (8 target + 1 extra)', len(s6_all))
    gate(set(closed_by_fold) <= s6_all and len(s6_all - set(closed_by_fold)) == len(extra_rows),
         'S6 closed = 8 target + declared extras', (len(s6_all - set(closed_by_fold)), len(extra_rows)))

    fb, fa = fold['frontier_before'], fold['frontier_after']
    gate(fb['unique_remaining_s6'] == 6222 and fb['solved_s6_in_manifest'] == 1626
         and fb['sum_remaining_cost'] == 492688 and fb['parent_row_incidence'] == 11848,
         'fold frontier_before republishes the K1046 post-eighth state')
    cost_sum = sum(rc.get('closed_edge_cost', 0) for rc in fold['receipts'])
    gate(fa['sum_remaining_cost'] == fb['sum_remaining_cost'] - cost_sum,
         'cost delta == sum of closed edge costs', cost_sum)
    gate(fa['unique_remaining_s6'] + fa['solved_s6_in_manifest'] == fb['unique_remaining_s6'] + fb['solved_s6_in_manifest'],
         'S6 conservation across fold')
    gate(fa['solved_s6_in_manifest'] == 1635 and fa['unique_remaining_s6'] == 6213,
         'post-twelfth frontier 1635 solved / 6213 remaining')
    gate(fa['solved_s6_in_manifest'] - fb['solved_s6_in_manifest'] == len(set(total_s6_covered)),
         'solved S6 delta == number of closed S6 rows', (fa['solved_s6_in_manifest'] - fb['solved_s6_in_manifest']))
    tgt = fold['five_parent_target_after']
    gate(tgt['closed_target_rows_total'] == 34 and tgt['residual_target_rows'] == 78,
         'five-parent target 34/112 closed, 78 residual')

    residual78 = set(r5['base_state']['residual_row_hex'])
    mine = residual86 - set(closed_by_fold)
    gate(residual78 == mine, 'resolve5 residual78 == resolve4-86 minus fold-closed rows (third recomputation)')
    gate(len(residual78) == 78, 'residual 78 rows')
    gate(set(tgt['residual_row_hex_after']) == mine, 'fold record residual_after == my recomputation')

    universe = set()
    for h in residual78:
        m = int(h, 16)
        for p in range(121):
            if (m >> p) & 1:
                continue
            universe.add(canon_h(m | (1 << p)))
    gate(len(universe) == r5['expansion']['universe_roots'],
         'expansion universe size == third recomputation', (len(universe), r5['expansion']['universe_roots']))

    wit = r5['witness_full']
    gate(len(wit) == 39, 'witness list 39', len(wit))
    cov_count = {}
    roots_seen = set()
    struct_ok = 0
    for w in wit:
        root = w['root']; m = int(root, 16)
        ok = m.bit_count() == 7 and canon_h(m) == root and is_safe_points(bits_of(m))
        mc = coverage_rows(m, residual78)
        ok = ok and mc == set(w['rows'])
        for h in w['rows']:
            cov_count[h] = cov_count.get(h, 0) + 1
        roots_seen.add(root)
        if ok: struct_ok += 1
    gate(struct_ok == 39, 'witness roots: 7 stones + D4-canon + safe + coverage recomputed', f'{struct_ok}/39')
    gate(len(roots_seen) == 39, 'witness roots distinct')
    gate(len(cov_count) == 78 and all(v == 1 for v in cov_count.values()),
         '78 residual rows covered exactly once by the 39 witnesses')
    gate(set(cov_count) == residual78, 'witness coverage == residual 78 set')

    old_roots = set(r['root'] for r in sweep['witness_records'])
    gate(len(roots_seen & old_roots) == 0, 'witness roots disjoint from the 43 sweep43 roots',
         sorted(roots_seen & old_roots)[:3])
    gate(len(roots_seen & set(rc['root'] for rc in fold['receipts'])) == 0,
         'witness roots disjoint from the four new receipt roots')

    gate(r5['resolve']['matched_rows'] == 78 and r5['resolve']['stranded_rows'] == 0
         and r5['resolve']['witness_size'] == 39, 'resolve5 counters 78/0/39')
    gate(r5['expansion']['in_pool_117'] + r5['expansion']['known_refuted_expansion']
         + r5['expansion']['known_win_expansion'] + r5['expansion']['fresh_all']
         == r5['expansion']['universe_roots'], 'expansion partition sums to universe')
    gate(r5['expansion']['fresh_safe'] + r5['expansion']['fresh_unsafe'] == r5['expansion']['fresh_all'],
         'fresh partition safe+unsafe')
    gate(r5['verdict_pool']['known_refuted_roots'] == 379 and r5['verdict_pool']['known_win_roots'] == 168,
         'verdict pool 379 REFUTED / 168 WIN growth from 340/164 (+39/+4)')

    summary = {
        'schema': 'n11-fold9-12-resolve5-third-method-cross-check-20261119-v1',
        'method': 'exact rational circle solve (cross-multiplied) + exact line test; python3 stdlib only',
        'gates': GATES,
        'all_pass': len([g for g in GATES if not g['pass']]) == 0,
        'closed_target_rows_by_third_recomputation': sorted(closed_by_fold),
        'closed_s6_rows_by_third_recomputation': sorted(set(total_s6_covered)),
        'residual78_consistent': residual78 == mine,
        'expansion_universe_third_recomputation': len(universe),
        'witness39_structural_audit_pass': struct_ok == 39,
        'wall_s': round(time.time() - t0, 1),
    }
    if out_json:
        json.dump(summary, open(out_json, 'w'), indent=1, ensure_ascii=False)
        open(out_json, 'a').write('\n')
    print()
    if not summary['all_pass']:
        print('CROSS-CHECK FAILED GATES:', [g['name'] for g in GATES if not g['pass']])
        sys.exit(1)
    print('ALL FOLD/RESOLVE5 THIRD-METHOD CROSS-CHECKS PASS')

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.',
         sys.argv[2] if len(sys.argv) > 2 else None)
