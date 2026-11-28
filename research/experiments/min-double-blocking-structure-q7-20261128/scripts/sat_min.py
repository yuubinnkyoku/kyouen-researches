#!/usr/bin/env python3
"""SAT decision: does plane(2,q) admit a t-fold blocking set of size <= k? (t=2)

Encoding (DIMACS CNF), vars 1..n = points:
  - each line L: at-least-2 = (OR of all) + for each i: (-xi OR rest).
  - at-most-k via one-direction sequential counter s_{i,j} = ">= j of 1..i",
    j in [1..k+1]: x_1 -> s_{1,1}; s_{i-1,j} -> s_{i,j}; x_i -> s_{i,1};
    x_i & s_{i-1,j-1} -> s_{i,j}; unit -s_{n,k+1}.
    Sound both ways: counters only forced up when genuinely reached.
Optional symmetry breaking 'fix': WLOG C contains a fixed non-collinear
triple (PGL(3,q)/AGL(2,q) transitive on non-collinear triples; a 2-fold
blocking set is never contained in one line). Calibrated on q=3,4,5.
SAT witnesses are extracted and independently re-verified per definition.
"""
import json, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from boards import affine_plane, projective_plane

KISSAT = '/home/user/work/a2q7/kissat'

def get_plane(kind, q):
    if kind == 'ag':
        pts, lines = affine_plane(q)
    else:
        pts, lines = projective_plane(q)
    return len(pts), [sorted(l) for l in lines]

def encode(n, lines, k, t=2, fix=()):
    cls = []
    assert t == 2
    for L in lines:
        v = [p + 1 for p in L]
        cls.append(v)
        for i in v:
            cls.append([-i] + [j for j in v if j != i])
    for p in fix:
        cls.append([p + 1])
    base = n
    def s(i, j): return base + (i - 1) * (k + 1) + j
    if k < n:
        cls.append([-1, s(1, 1)])
        for i in range(2, n + 1):
            for j in range(1, k + 2):
                cls.append([-s(i - 1, j), s(i, j)])
            cls.append([-i, s(i, 1)])
            for j in range(2, k + 2):
                cls.append([-i, -s(i - 1, j - 1), s(i, j)])
        cls.append([-s(n, k + 1)])
        nvars = base + n * (k + 1)
    else:
        nvars = base
    return cls, nvars

def default_fix(kind, q, lines):
    if kind == 'ag':
        trip = [0, 1, q]  # (0,0),(1,0),(0,1)
    else:
        trip = [0, q, q * q]  # (0,0,1),(1,0,1),(0,1,0)  [index = x*q+y]
    st = set(trip)
    assert len(st) == 3
    for L in lines:
        assert not st <= set(L), (trip, L)
    return trip

def run_sat(cls, nvars, tag, cap=280):
    d = '/tmp/sat_%s' % tag
    os.makedirs(d, exist_ok=True)
    cnf = d + '/in.cnf'
    with open(cnf, 'w') as f:
        f.write('p cnf %d %d\n' % (nvars, len(cls)))
        for c in cls:
            f.write(' '.join(map(str, c)) + ' 0\n')
    out = subprocess.run([KISSAT, cnf], capture_output=True, text=True, timeout=cap)
    so = out.stdout
    if 's UNSATISFIABLE' in so:
        return 'UNSAT', None, so
    if 's SATISFIABLE' in so:
        model = set()
        for line in so.splitlines():
            if line.startswith('v'):
                for tok in line.split()[1:]:
                    v = int(tok)
                    if 1 <= v <= nvars and v > 0:
                        model.add(v)
        return 'SAT', model, so
    raise RuntimeError('no verdict: ' + so[:300])

def check_blocking(n, lines, C, t=2):
    C = set(C)
    for L in lines:
        if len(C & set(L)) < t:
            return False, L
    return True, None

if __name__ == '__main__':
    kind, q = sys.argv[1], int(sys.argv[2])
    k = int(sys.argv[3])
    use_fix = len(sys.argv) > 4 and sys.argv[4] == 'fix'
    n, lines = get_plane(kind, q)
    fix = default_fix(kind, q, lines) if use_fix else ()
    cls, nvars = encode(n, lines, k, fix=fix)
    res, model, raw = run_sat(cls, nvars, '%s%d_%d%s' % (kind, q, k, '_fix' if use_fix else ''))
    if res == 'SAT':
        C = sorted(p for p in range(n) if (p + 1) in model)
        ok, bad = check_blocking(n, lines, C)
        assert ok and len(C) <= k, (ok, bad, len(C))
        print(json.dumps({'kind': kind, 'q': q, 'k': k, 'res': 'SAT',
                          'size': len(C), 'witness': C}))
    else:
        print(json.dumps({'kind': kind, 'q': q, 'k': k, 'res': 'UNSAT'}))
