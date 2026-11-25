#!/usr/bin/env python3
"""safe_subset_sat.py — SAT certification of SAFE-subset cardinality rows.

Encodes, for the n x n kyouen board with the Leibniz catalog text:
  - cell indicator x_c for every cell,
  - a blocking clause ¬a∨¬b∨¬c∨¬d for EVERY forbidden quartet,
  - cardinality EXACTLY k: Sinz sequential-counter at-most-k on the
    positive indicators (<= k stones) AND on the negated indicators
    (<= N-k non-stones, i.e. >= k stones),
with NO maximality constraint — this is ONLY the safety lattice.

Modes:
  count     : enumerate ALL models by iterative blocking (each model
              blocks its exact stone set); on UNSAT the model list is
              complete by construction.
  decidesat : single kissat call, SAT/UNSAT + first model.

Validation policy (fail-closed): self-check on n=3/n=4 against the
brute-force safe histograms before trusting big-board UNSAT.
"""
import json
import subprocess
import sys
import os


def load_quartets(path):
    out = []
    for line in open(path, encoding='utf8'):
        line = line.strip()
        if line and not line.startswith('n='):
            out.append(tuple(int(t) for t in line.split()))
    return out


def sinz_atmost(pred, k, nv_offset):
    """Sinz sequential-counter at-most-k over literals `pred` (list of
    signed ints). Returns (clauses, next_free_var)."""
    n = len(pred)
    clauses = []
    v = nv_offset
    if k >= n:
        return clauses, v
    if k == 0:
        for l in pred:
            clauses.append([-l])
        return clauses, v
    s = {}
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            s[(i, j)] = v
            v += 1
    # s(1,1) <-> pred[0]
    clauses.append([pred[0], -s[(1, 1)]])
    clauses.append([-pred[0], s[(1, 1)]])
    for j in range(2, k + 1):
        clauses.append([-s[(1, j)]])
    for i in range(2, n + 1):
        clauses.append([-s[(i - 1, 1)], s[(i, 1)]])
        clauses.append([-pred[i - 1], s[(i, 1)]])
        for j in range(2, k + 1):
            clauses.append([-s[(i - 1, j)], s[(i, j)]])
            clauses.append([-pred[i - 1], -s[(i - 1, j - 1)], s[(i, j)]])
        clauses.append([-pred[i - 1], -s[(i - 1, k)]])
    return clauses, v


def build_cnf(N, k, quartets, extra_clauses=()):
    clauses = []
    for q in quartets:
        clauses.append([-(c + 1) for c in q])
    c1, v1 = sinz_atmost(list(range(1, N + 1)), k, N + 1)
    clauses += c1
    negs = [-(c + 1) for c in range(N)]
    c2, v2 = sinz_atmost(negs, N - k, v1)
    clauses += c2
    clauses += [list(cl) for cl in extra_clauses]
    nv = v2 - 1
    return nv, clauses


def cnf_text(nv, clauses):
    return f"p cnf {nv} {len(clauses)}\n" + \
        '\n'.join(' '.join(map(str, cl)) + ' 0' for cl in clauses) + '\n'


def parse_model(stdout, N):
    lits = []
    for line in stdout.splitlines():
        if line.startswith('v '):
            lits += [int(t) for t in line[2:].split() if t]
    return sorted(x - 1 for x in lits if 1 <= x <= N)


def run_kissat(nv, clauses, path, kissat_path):
    with open(path, 'w') as f:
        f.write(cnf_text(nv, clauses))
    r = subprocess.run([kissat_path, path], capture_output=True, text=True)
    out = r.stdout
    if 'UNSATISFIABLE' in out:
        return None
    if 'SATISFIABLE' not in out:
        raise RuntimeError('kissat anomaly: rc=%d %s' % (r.returncode, out[:200]))
    return out


def count_mode(n, k, quartets, kissat_path, out_path):
    N = n * n
    workdir = f"work/safecount_n{n}_k{k}"
    os.makedirs(workdir, exist_ok=True)
    models = []
    seen = set()
    it = 0
    while True:
        it += 1
        blocks = [[-(c + 1) for c in m] for m in models]
        nv, clauses = build_cnf(N, k, quartets, blocks)
        path = f"{workdir}/iter_{it}.cnf"
        out = run_kissat(nv, clauses, path, kissat_path)
        if out is None:
            break
        stones = tuple(parse_model(out, N))
        if len(stones) != k or stones in seen:
            raise RuntimeError('bad model %r' % (stones,))
        seen.add(stones)
        models.append(stones)
    res = {'mode': 'count', 'n': n, 'k': k, 'N': N,
           'models': len(models), 'distinct': len(set(models)),
           'iterations': it - 1}
    with open(out_path, 'w') as f:
        f.write(json.dumps(res, indent=1) + '\n')
        for m in sorted(models):
            f.write(','.join(map(str, m)) + '\n')
    print(json.dumps(res))
    return 0


def decidesat_mode(n, k, quartets, kissat_path, out_path):
    N = n * n
    os.makedirs('work/safecnf', exist_ok=True)
    nv, clauses = build_cnf(N, k, quartets)
    path = f"work/safecnf/safe_n{n}_k{k}.cnf"
    out = run_kissat(nv, clauses, path, kissat_path)
    sat = out is not None
    res = {'mode': 'decidesat', 'n': n, 'k': k, 'N': N, 'sat': sat,
           'model': (tuple(parse_model(out, N)) if sat else None),
           'nvars': nv, 'nclauses': len(clauses), 'cnf': path}
    with open(out_path, 'w') as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res))
    return 0


def main():
    mode, n, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    qtext, kissat_path, out_path = sys.argv[4], sys.argv[5], sys.argv[6]
    quartets = load_quartets(qtext)
    if mode == 'count':
        return count_mode(n, k, quartets, kissat_path, out_path)
    if mode == 'decidesat':
        return decidesat_mode(n, k, quartets, kissat_path, out_path)
    print('modes: count | decidesat', file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
