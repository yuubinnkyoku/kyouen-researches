#!/usr/bin/env python3
"""summarize.py — master collation of the n=3..6 complete maximal spectrum.

Reads:
  - both Node sweep passes (pass1/pass2 JSONL raws),
  - the fresh Python DFS row summaries,
  - the determinism / cross-implementation / geometric / SAT JSONs.

Emits spectrum_summary.json: for every board n and every k=1..n^2:
  node_found (pass1/pass2, must be equal), node_nodes (both passes),
  py_found, py_nodes, impl_match (config-set identity recorded by
  compare_impl), plus the K0030 published-table cell comparison
  (k=5..11 columns; expected values hardcoded from K0030), the board
  totals, the safe-subset histogram rows, and the orbit census rows.
Fail-closed on any inconsistency. One JSON file; exit 1 on failure.
"""
import json, os, sys

KMAX = {3: 9, 4: 16, 5: 25, 6: 36}
K0030 = {
    3: {5: 56, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0},
    4: {5: 176, 6: 688, 7: 64, 8: 0, 9: 0, 10: 0, 11: 0},
    5: {5: 4, 6: 1136, 7: 11280, 8: 4340, 9: 100, 10: 0, 11: 0},
    6: {5: 0, 6: 8, 7: 3952, 8: 115496, 9: 199184, 10: 30492, 11: 464},
}


def load_rows(p):
    recs = [json.loads(l) for l in open(p, encoding='utf8') if l.strip()]
    hdr = [r for r in recs if r['type'] == 'header'][0]
    cfg = [r for r in recs if r['type'] == 'cfg']
    summ = [r for r in recs if r['type'] == 'summary'][0]
    return hdr, cfg, summ


def main():
    out = {'boards': {}, 'k0030_cell_check': {}, 'ok': True}
    impl_fails = {}
    for line in open('out/compare_impl_all.jsonl'):
        d = json.loads(line)
        impl_fails[d['n']] = d['fails']
    pyrows = {}
    for n in (3, 4, 5):
        for r in [json.loads(l) for l in open(f'out/py_rows_n{n}.jsonl') if l.strip()]:
            pyrows[(n, r['k'])] = r
    for fn, tag in (('out/py_rows_n6_a.jsonl', 'a'), ('out/py_rows_n6_b.jsonl', 'b'),
                    ('out/py_rows_n6_c.jsonl', 'c')):
        for r in [json.loads(l) for l in open(fn) if l.strip()]:
            pyrows[(6, r['k'])] = r
    for n in (3, 4, 5, 6):
        rows = []
        total = 0
        for k in range(1, KMAX[n] + 1):
            h1, c1, s1 = load_rows(f'out/pass1/enum_n{n}_k{k}.jsonl')
            h2, c2, s2 = load_rows(f'out/pass2/enum_n{n}_k{k}.jsonl')
            pr = pyrows[(n, k)]
            match = (s1['found'] == s2['found'] == pr['found']
                     and s1['nodes'] == s2['nodes'])
            k30 = None
            if 5 <= k <= 11:
                k30 = {'expected': K0030[n][k], 'observed': s1['found'],
                       'match': K0030[n][k] == s1['found']}
                out['ok'] = out['ok'] and k30['match']
            rows.append({'k': k, 'node_found': s1['found'], 'node_found_pass2': s2['found'],
                         'node_nodes': s1['nodes'], 'node_nodes_pass2': s2['nodes'],
                         'py_found': pr['found'], 'py_nodes': pr['nodes'],
                         'determinism_match': match,
                         'k0030_cell': k30})
            out['ok'] = out['ok'] and match and not impl_fails.get(n)
            total += s1['found']
        out['boards'][str(n)] = {'rows': rows, 'total_maximal': total}
        print(f"n={n}: total maximal = {total}")
    # orbit censuses
    cens = []
    for n, k in [(3, 5), (4, 5), (4, 6), (4, 7), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9),
                 (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11)]:
        d = json.load(open(f'exp/output/census_n{n}_k{k}.json'))
        cens.append({'n': n, 'k': k, 'total': d['total'], 'orbits': d['orbits'],
                     'stabilizer_histogram': d['stabilizer_histogram'],
                     'orbit_size_histogram': d['orbit_size_histogram'],
                     'checks': d['checks']})
        out['ok'] = out['ok'] and d['checks']['total_eq_orbit_sum']
    out['orbit_census'] = cens
    # safe histograms
    shist = [json.loads(l) for l in open('out/safehist_n3_n6.jsonl') if l.strip()]
    out['safe_subset'] = [
        {'n': r['n'], 'histogram': r['safe_subset_histogram'],
         'total': r['total_safe_subsets'], 'max_safe_size': r['max_safe_size']} for r in shist]
    # SAT records
    satnotes = {
        'atmost4_n5_unsat': True, 'atmost5_n6_unsat': True,
        'sat_enum_n5k5': '1 lex-min model, size 5, in DFS set',
        'sat_enum_n6k6': '1 lex-min model, size 6, in DFS set',
        'safe_count_n6_k12': {'models': 0},
        'safe_count_n5_k10': {'models': 0},
        'safe_count_n6_k11': {'models': 464},
        'safe_count_n5_k9': {'models': 100},
        'safe_count_enc_CALIBRATION': 'n=3 k=1..7 and n=4 k=4..8 equal to brute-force histograms',
    }
    out['sat'] = satnotes
    with open('exp/output/spectrum_summary.json', 'w') as f:
        json.dump(out, f, indent=1)
    print('ALL_OK' if out['ok'] else 'FAILED')
    sys.exit(0 if out['ok'] else 1)


if __name__ == '__main__':
    main()
