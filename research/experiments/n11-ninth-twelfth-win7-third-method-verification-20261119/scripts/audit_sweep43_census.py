#!/usr/bin/env python3
# Static audit of the K1057 sweep43 + add-one-stone-census claims, third environment.
# Checks (all third-method, no repo code):
#  1. residual 86 rows (resolve4) == exactly the union of witness covered rows, each
#     covered exactly once by the 43 pair witnesses.
#  2. every witness root: 7 stones, D4-canonical, safe (third algebra), maxbit child
#     convention (child = root ^ 1<<maxbit), and its covered rows recomputed
#     independently from the 8-D4-image-minus-one-stone relation match the record.
#  3. roots.json (sweep driver input) == witness_records roots/children/bits/rows.
#  4. probe-record jsonls match the published witness records per-root, per-ordering
#     node counts, cap, uncapped flags and pilot_d6 control.
#  5. classification (WIN/REFUTED/CAPPED/CONFLICT) recomputed from probe records.
#  6. controls totals recomputed (nodes_total_all_probes).
#  7. the 4 WIN roots are exactly the 4 certificate roots (9th..12th).
import json, sys

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
    out = 0
    for p in bits_of(mask):
        out |= 1 << TF[t][p]
    return out

def canon(mask):
    return min(transform(mask, t) for t in range(8))

def canon_h(mask):
    return '%032x' % canon(mask)

def popcount(m):
    return m.bit_count()

def det3s(a, b, c):
    # exact rational-circle cross-multiplied coefficients; banned(d) test below
    x1, y1, s1 = X[a], Y[a], S[a]
    x2, y2, s2 = X[b], Y[b], S[b]
    x3, y3, s3 = X[c], Y[c], S[c]
    A1, B1 = x2 - x1, y2 - y1
    A2, B2 = x3 - x1, y3 - y1
    W = A1 * B2 - A2 * B1
    if W == 0:
        dx, dy = x2 - x1, y2 - y1
        def test(d):
            return dx * (Y[d] - y1) - dy * (X[d] - x1) == 0
    else:
        C1, C2 = -(s2 - s1), -(s3 - s1)
        DD = C1 * B2 - C2 * B1
        EE = A1 * C2 - A2 * C1
        def test(d):
            return W * (S[d] - s1) + DD * (X[d] - x1) + EE * (Y[d] - y1) == 0
    return test

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
            row = canon_h(img ^ (1 << b))
            if row in universal:
                cov.add(row)
    return cov

GATES = []
FAILS = []
def gate(ok, name, detail=''):
    status = 'PASS' if ok else 'FAIL'
    print(f'[{status}] {name} {detail}')
    GATES.append({'name': name, 'pass': bool(ok), 'detail': str(detail)})
    if not ok:
        FAILS.append(name)

def main(wd, out_json):
    sweep = json.load(open(f'{wd}/sweep43.json'))
    roots_in = json.load(open(f'{wd}/roots.json'))
    r4 = json.load(open(f'{wd}/resolve4.json'))
    probes = []
    for f in ('probe-records-w0.jsonl', 'probe-records-w1.jsonl'):
        for line in open(f'{wd}/{f}'):
            if line.strip():
                probes.append(json.loads(line))

    residual = list(r4['resolve']['stranded_row_hex'])
    res_set = set(residual)
    gate(len(residual) == 86 and len(res_set) == 86, 'resolve4 residual 86 unique rows', len(residual))
    # residual rows are 6-stone D4-canonical
    ok6 = all(popcount(int(h, 16)) == 6 and canon_h(int(h, 16)) == h for h in residual)
    gate(ok6, 'residual rows are 6-stone D4-canonical')

    recs = sweep['witness_records']
    gate(len(recs) == 43, 'witness records 43', len(recs))
    gate(len(roots_in) == 43, 'roots.json entries 43', len(roots_in))

    cov_count = {}
    root_audits = 0
    win_roots, refuted_roots = [], []
    for rec in recs:
        root_hex = rec['root']
        m = int(root_hex, 16)
        pts = bits_of(m)
        ok = popcount(m) == 7
        ok = ok and canon_h(m) == root_hex
        ok = ok and is_safe_points(pts)
        mx = max(pts)
        child = m ^ (1 << mx)
        ok = ok and ('%032x' % child) == rec['child_hex'] and mx == rec['added_bit']
        cov = coverage_rows(m, res_set)
        ok = ok and cov == set(rec['covered_stranded_rows'])
        for h in rec['covered_stranded_rows']:
            cov_count[h] = cov_count.get(h, 0) + 1
        if not ok:
            gate(False, 'witness root audit ' + root_hex)
        else:
            root_audits += 1
        runs = rec['probe_runs']
        win = all(r['loss'] is True and not r['capped'] for r in runs)
        ref = all(r['loss'] is False and not r['capped'] for r in runs)
        if win: win_roots.append(root_hex)
        elif ref: refuted_roots.append(root_hex)
    gate(root_audits == 43, 'witness roots: 7 stones + D4-canon + safe + maxbit child + coverage recomputed',
         f'{root_audits}/43')
    gate(len(cov_count) == 86 and all(v == 1 for v in cov_count.values()),
         '86 residual rows each covered exactly once by the 43 witnesses',
         f'{len(cov_count)} rows, cover multiplicities ok={all(v==1 for v in cov_count.values())}')
    gate(set(cov_count) == res_set, 'covered row set == resolve4 residual set')

    # roots.json consistency
    ok = True
    for rj in roots_in:
        rec = next((x for x in recs if x['root'] == rj['root']), None)
        if rec is None or sorted(rj['rows']) != sorted(rec['covered_stranded_rows']) \
           or rj['child'] != rec['child_hex'] or rj['bit'] != rec['added_bit']:
            ok = False
    gate(ok, 'roots.json == witness records (root/child/bit/rows)')

    # probe records
    pb = {}
    for p in probes:
        pb.setdefault(p['root'], []).append(p)
    gate(len(pb) == 43, 'probe records cover 43 roots', len(pb))
    probe_ok = 0
    nodes_sum = 0
    for rec in recs:
        plist = pb.get(rec['root'], [])
        by_ord = {}
        for p in plist:
            by_ord.setdefault(p.get('ordering'), []).append(p)
        ok = set(by_ord.keys()) == {'andclose0', 'andclose1'}
        for o, lst in by_ord.items():
            ok = ok and len(lst) == 1
        if not ok:
            continue
        ctrl_ok = all(p.get('control', {}).get('nodes') == 3402 and p['control']['loss'] is False
                      for p in plist)
        run_ok = True
        for run in rec['probe_runs']:
            lst = by_ord.get(run['ordering'], [])
            if not lst:
                run_ok = False; continue
            r = lst[0]
            res = r.get('result', {})
            run_ok = run_ok and res.get('nodes') == run['nodes'] and res.get('capped') == run['capped'] \
                     and res.get('loss') == run['loss'] and r.get('cap', run.get('cap')) == run['cap'] \
                     and run['cap'] == 30000000
        if ctrl_ok and run_ok:
            probe_ok += 1
        nodes_sum += sum(r['nodes'] for r in rec['probe_runs'])
    gate(probe_ok == 43, 'probe records match published witness records (nodes/cap/loss/pilot)', f'{probe_ok}/43')

    cls = sweep['classification']
    gate(cls['counted_roots'] == 43, 'classification counted 43')
    gate(sorted(cls['win7_d10']['roots']) == sorted(win_roots) and len(win_roots) == 4,
         'classification WIN roots recomputed == 4', len(win_roots))
    gate(sorted(cls['refuted_d10']['roots']) == sorted(refuted_roots) and len(refuted_roots) == 39,
         'classification REFUTED roots recomputed == 39', len(refuted_roots))
    gate(cls['capped']['count'] == 0 and cls['ordering_conflicts']['count'] == 0, 'zero capped/conflicts')

    ctrl = sweep['controls']
    gate(ctrl['nodes_total_all_probes'] == nodes_sum, 'controls.nodes_total_all_probes recomputed',
         f'{nodes_sum} vs {ctrl["nodes_total_all_probes"]}')
    gate(len(win_roots) + len(refuted_roots) == 43, 'verdict partition 4+39')

    # WIN roots == certificate roots 9th..12th
    cert_roots = ['00000000000000801202000001040200', '00000000000000821082040200000000',
                  '00000000000000821092200000000000', '00000000001020003800000048000000']
    gate(sorted(win_roots) == sorted(cert_roots), 'sweep WIN roots == certificate roots 9th..12th')

    summary = {
        'schema': 'n11-sweep43-census-third-method-static-audit-20261119-v1',
        'method': 'exact rational circle solve (cross-multiplied) + exact line test; python3 stdlib only',
        'gates': GATES,
        'all_pass': len(FAILS) == 0,
        'witness_root_structural_audit_pass': root_audits == 43,
        'win_roots_recomputed': sorted(win_roots),
        'refuted_roots_count': len(refuted_roots),
        'nodes_total_recomputed': nodes_sum,
        'covered_rows_exactly_once': len(cov_count) == 86 and all(v == 1 for v in cov_count.values()),
    }
    if out_json:
        json.dump(summary, open(out_json, 'w'), indent=1, ensure_ascii=False)
        open(out_json, 'a').write('\n')
    print()
    if FAILS:
        print('AUDIT FAILED GATES:', FAILS)
        sys.exit(1)
    print('ALL SWEEP43/CENSUS AUDIT GATES PASS')

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.',
         sys.argv[2] if len(sys.argv) > 2 else None)
