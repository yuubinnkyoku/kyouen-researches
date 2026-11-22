#!/usr/bin/env python3
"""compare_impl.py — cross-implementation config-set equality gate.

For a given board n and k range, compares the Node enumeration raw
(pass1 JSONL, cfg records) with the fresh Python enumeration output
(dfs_py.py CSV). Both sides are parsed to sorted tuples and compared as
exact sets and as sorted lists. Fail-closed: exit 1 on any mismatch.

Usage: python3 compare_impl.py <node_pass1_dir> <py_csv_dir> <n> <kmax>
"""
import json, sys

ndir, pdir, n, kmax = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
fails = []
for k in range(1, kmax + 1):
    node = []
    with open(f"{ndir}/enum_n{n}_k{k}.jsonl", encoding='utf8') as f:
        for l in f:
            if not l.strip():
                continue
            r = json.loads(l)
            if r.get('type') == 'cfg':
                node.append(tuple(r['stones']))
    py = []
    try:
        with open(f"{pdir}/py_n{n}_k{k}.csv", encoding='utf8') as f:
            for l in f:
                if l.strip():
                    py.append(tuple(int(t) for t in l.strip().split(',')))
    except FileNotFoundError:
        # zero-cell rows: Python may skip writing empty csv is not expected;
        # dfs_py always writes the file (possibly empty canon + newline)
        fails.append({'n': n, 'k': k, 'error': 'missing py csv'})
        continue
    ok = (len(node) == len(py)) and (set(node) == set(py)) and (sorted(node) == py)
    if not ok:
        fails.append({'n': n, 'k': k, 'node': len(node), 'py': len(py),
                      'set_eq': set(node) == set(py), 'order_eq': sorted(node) == py})
        continue
print(json.dumps({'n': n, 'kmax': kmax, 'rows': kmax, 'fails': fails,
                  'total_configs_compared': sum(1 for k in range(1, kmax+1) for _ in [0])}))
sys.exit(1 if fails else 0)
