#!/usr/bin/env python3
"""Case-split SAT decision for 2-fold blocking sets of size <= k.

Any 2-fold blocking set C has max line count >= 3 in PG(2,q) (if every line
had exactly 2, sum_l |C^l| = 2(q^2+q+1) = |C|(q+1), impossible for q >= 2).
In AG(2,q) the all-lines-exactly-2 case forces |C| = 2q (case C).

  Case A (max >= 4): PGL/AGL transitive on (line, ordered triple of points
    on it) [line stabilizer acts as PGL(2,q), sharply 3-transitive]; WLOG C
    contains A0,A1,A2 on fixed line l0 and |C^l0| >= 4 (l0 = a max line).
  Case B (max = 3): WLOG l0 is a max line with A0,A1,A2 in C and every line
    has <= 3 C-points.
  Case C (AG only, max = 2): every line exactly 2 (|C| = 2q forced).
  Sub-cases A_j (j = 4..7): additionally every line <= j (valid: l0 is a max
  line). A8: l0 completely contained in C. A = A4 u ... u A7 u A8.
All cases UNSAT at k  ->  no 2-fold blocking set of size <= k (rigorous).
SAT witnesses independently verified per definition.
"""
import json, subprocess, sys, os
from itertools import combinations
sys.path.insert(0, os.path.dirname(__file__))
from boards import affine_plane, projective_plane

KISSAT = '/home/user/work/a2q7/kissat'

def get_plane(kind, q):
    if kind == 'ag':
        pts, lines = affine_plane(q)
    else:
        pts, lines = projective_plane(q)
    return len(pts), [sorted(l) for l in lines]

def at_least(cls, pts, t):
    v = [p + 1 for p in pts]
    if t <= 0: return
    if t == 1:
        cls.append(v); return
    for sub in combinations(v, len(v) - t + 1):
        cls.append(list(sub))

def at_most(cls, pts, t):
    v = [p + 1 for p in pts]
    for sub in combinations(v, t + 1):
        cls.append([-x for x in sub])

def amk_counter(cls, n, k):
    if k >= n:
        return n
    base = n
    def s(i, j): return base + (i - 1) * (k + 1) + j
    cls.append([-1, s(1, 1)])
    for i in range(2, n + 1):
        for j in range(1, k + 2):
            cls.append([-s(i - 1, j), s(i, j)])
        cls.append([-i, s(i, 1)])
        for j in range(2, k + 2):
            cls.append([-i, -s(i - 1, j - 1), s(i, j)])
    cls.append([-s(n, k + 1)])
    return base + n * (k + 1)

def encode(kind, q, k, case):
    n, lines = get_plane(kind, q)
    cls = []
    for L in lines:
        at_least(cls, L, 2)
    nvars = amk_counter(cls, n, k)
    if case == 'C':
        assert kind == 'ag'
        for L in lines:
            at_most(cls, L, 2)
        return cls, nvars, n, lines
    cand = [L for L in lines if 0 in L and q in L]
    assert len(cand) == 1, cand
    l0 = cand[0]
    trip = [0, q, [p for p in l0 if p not in (0, q)][0]]
    assert len(set(trip)) == 3 and set(trip) <= set(l0)
    for p in trip:
        cls.append([p + 1])
    if case == 'A':
        at_least(cls, l0, 4)
    elif case in ('A4', 'A5', 'A6', 'A7'):
        j = int(case[1])
        at_least(cls, l0, 4)
        for L in lines:
            at_most(cls, L, j)
    elif case == 'A8':
        for p in l0:
            cls.append([p + 1])
    elif case == 'B':
        at_least(cls, l0, 3)
        for L in lines:
            at_most(cls, L, 3)
    else:
        raise ValueError(case)
    return cls, nvars, n, lines

def run(cls, nvars, tag, cap=280):
    d = '/tmp/sat2_%s' % tag
    os.makedirs(d, exist_ok=True)
    cnf = d + '/in.cnf'
    with open(cnf, 'w') as f:
        f.write('p cnf %d %d\n' % (nvars, len(cls)))
        for c in cls:
            f.write(' '.join(map(str, c)) + ' 0\n')
    out = subprocess.run([KISSAT, cnf], capture_output=True, text=True, timeout=cap)
    so = out.stdout
    if 's UNSATISFIABLE' in so:
        return 'UNSAT', None
    if 's SATISFIABLE' in so:
        model = set()
        for line in so.splitlines():
            if line.startswith('v'):
                for tok in line.split()[1:]:
                    v = int(tok)
                    if 1 <= v <= nvars and v > 0:
                        model.add(v)
        return 'SAT', model
    raise RuntimeError('no verdict')

def main():
    kind, q, k, case = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    cap = int(sys.argv[5]) if len(sys.argv) > 5 else 280
    cls, nvars, n, lines = encode(kind, q, k, case)
    res, model = run(cls, nvars, '%s%d_%d_%s' % (kind, q, k, case), cap)
    if res == 'SAT':
        C = sorted(p for p in range(n) if p + 1 in model)
        Cset = set(C)
        for L in lines:
            assert len(Cset & set(L)) >= 2, (L, C)
        assert len(C) <= k
        print(json.dumps({'kind': kind, 'q': q, 'k': k, 'case': case,
                          'res': 'SAT', 'size': len(C), 'witness': C}))
    else:
        print(json.dumps({'kind': kind, 'q': q, 'k': k, 'case': case, 'res': 'UNSAT'}))

if __name__ == '__main__':
    main()
