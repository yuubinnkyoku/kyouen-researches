"""Independent class (origin=1, both=1, none=0) schema; no SAT library."""
from collections import Counter


def structural(p):
    h = (p-1)//2
    assert p >= 5 and p % 2
    selectors = 4*h
    base = selectors+h-1
    clauses = []

    def add(*literals):
        clauses.append(tuple(sorted(literals)))

    for i in range(h):
        states = list(range(4*i+1, 4*i+5))
        add(*states)
        for a in range(4):
            for b in range(a):
                add(-states[a], -states[b])
    both = [4*i+1 for i in range(h)]
    prefix = [selectors+i+1 for i in range(h-1)]
    add(*both)
    for i in range(h-1):
        add(-both[i], prefix[i])
    for i in range(1, h-1):
        add(-prefix[i-1], prefix[i])
    for i in range(1, h):
        add(-both[i], -prefix[i-1])
    for i in range(h):
        add(-4*i-2)
    for t in range(1, p):
        i = min(t, p-t)-1
        side = 4*i+(3 if t <= h else 4)
        b, point = 4*i+1, base+t
        add(-point, side, b)
        add(point, -side)
        add(point, -b)
    return clauses, base+p-1, base


def parse(raw):
    header, clauses, current = None, [], []
    for line in raw.decode('ascii').splitlines():
        if not line.strip() or line.startswith('c'):
            continue
        if line.startswith('p'):
            assert header is None and not clauses and not current
            fields = line.split()
            assert fields[:2] == ['p', 'cnf'] and len(fields) == 4
            header = tuple(map(int, fields[2:]))
            continue
        assert header is not None
        for literal in map(int, line.split()):
            if literal:
                assert abs(literal) <= header[0]
                current.append(literal)
            else:
                assert len(current) == len(set(current))
                clauses.append(tuple(sorted(current)))
                current = []
    assert header is not None and not current and len(clauses) == header[1]
    return header[0], clauses


def audit(raw, p=2207):
    variables, clauses = parse(raw)
    expected, nv, base = structural(p)
    assert variables == nv
    counts, wanted = Counter(clauses), Counter(expected)
    assert not wanted-counts, 'missing or modified structural clause'
    remaining = counts-wanted
    edges = []
    for clause, count in remaining.items():
        assert len(clause) in (3, 4) and all(-nv <= lit < -base for lit in clause)
        points = sorted(-lit-base for lit in clause)
        if len(points) == 3:
            points.insert(0, 0)
        assert len(set(points)) == 4 and 0 <= points[0] < points[-1] < p
        edges.extend([tuple(points)]*count)
    return edges, dict(p=p, variables=nv, clauses=len(clauses),
                      structural_clauses=len(expected), geometry_clauses=len(edges),
                      selectors=[1, 4*((p-1)//2)],
                      prefix_counter=[4*((p-1)//2)+1, base],
                      point_variables=[base+1, nv],
                      point_base=base, origin_both_none=[1, 1, 0],
                      method='Explicit one-hot, Sinz exactly-one BOTH, NONE units and point definitions; no CardEnc or search encoder import.')
