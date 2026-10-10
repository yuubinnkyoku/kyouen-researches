"""Standalone integer geometry, fixed-player logic and ranked DAG certificates.

No imports of solver, existing geometry, canonicalization or propagation code.
WIN/LOSS are about the original first player. 0 denotes incomplete evidence.
"""
from functools import lru_cache
from itertools import combinations


def mask_from_key(lo,hi,n=11):
    if type(lo) is not int or type(hi) is not int or not 0<=lo<1<<64 or not 0<=hi<1<<max(0,n*n-64):
        raise ValueError('invalid two-word board key')
    mask=lo|(hi<<64)
    if mask >> (n*n): raise ValueError('key outside board')
    return mask


def aggregate(stones, values):
    values = tuple(values)
    if stones < 0 or any(v not in (0, 1, 2) for v in values):
        raise ValueError('invalid layer/verdict')
    decisive = 2 if stones % 2 else 1
    universal = 3 - decisive
    if decisive in values:
        return decisive
    return universal if set(values) <= {universal} else 0


class Board:
    def __init__(self, n):
        self.n, self.size = n, n*n
        self.full = (1 << self.size)-1
        self.maps = []
        for t in range(8):
            row = []
            for p in range(self.size):
                x, y, m = p % n, p // n, n-1
                images = ((x,y),(m-y,x),(m-x,m-y),(y,m-x),
                          (m-x,y),(m-y,m-x),(x,m-y),(y,x))
                a,b = images[t]
                row.append(1 << (b*n+a))
            self.maps.append(row)

    def points(self, mask):
        if not isinstance(mask, int) or mask < 0 or mask & ~self.full:
            raise ValueError('mask outside board')
        return tuple(i for i in range(self.size) if mask >> i & 1)

    @lru_cache(maxsize=None)
    def canonical(self, mask):
        pts = self.points(mask)
        return min(sum(mapping[p] for p in pts) for mapping in self.maps)

    @lru_cache(maxsize=300000)
    def completion(self, triple):
        # Solve the two perpendicular-bisector equations for a circle center
        # using integer numerators. Collinear triples use their common line.
        a,b,c = triple
        x,y = a % self.n, a // self.n
        u,v = b % self.n-x, b // self.n-y
        s,t = c % self.n-x, c // self.n-y
        cross = u*t-v*s
        if cross == 0:
            return sum(1 << p for p in range(self.size)
                       if u*(p//self.n-y)-v*(p%self.n-x) == 0)
        qb = (b%self.n)**2+(b//self.n)**2-x*x-y*y
        qc = (c%self.n)**2+(c//self.n)**2-x*x-y*y
        cx, cy = qb*t-qc*v, u*qc-s*qb
        return sum(1 << p for p in range(self.size)
                   if cross*((p%self.n)**2+(p//self.n)**2-x*x-y*y)
                   == cx*(p%self.n-x)+cy*(p//self.n-y))

    @lru_cache(maxsize=None)
    def legal(self, mask):
        pts = self.points(mask)
        blocked = mask
        for triple in combinations(pts, 3):
            line_circle = self.completion(triple)
            if line_circle & (mask ^ sum(1 << p for p in triple)):
                raise ValueError('unsafe occupied position')
            blocked |= line_circle
        return self.full & ~blocked

    @lru_cache(maxsize=None)
    def children(self, mask):
        moves = self.legal(mask)
        return frozenset(self.canonical(mask | (1 << p))
                         for p in self.points(moves))

    def predecessors(self, mask):
        self.legal(mask)
        return {self.canonical(mask ^ (1 << p)) for p in self.points(mask)}


def verify_dag(board, certificate, trusted=None):
    """Check existential witnesses/universal completeness and strictly ranked edges.

    trusted is an explicit optional map of solver-trusted leaves, never inferred
    from certificate claims. Without it every leaf must be a geometric terminal.
    """
    nodes = certificate['nodes']
    trusted = trusted or {}
    visiting, done = set(), {}

    def visit(ident):
        if ident in visiting:
            raise ValueError('cycle')
        if ident in done:
            return done[ident]
        node = nodes[ident]
        mask, v = int(node['mask']), node['verdict']
        board.legal(mask)
        if board.canonical(mask) != mask or v not in (1,2):
            raise ValueError('noncanonical/invalid node')
        visiting.add(ident)
        ch = board.children(mask)
        refs = node.get('children', [])
        if len(refs) != len(set(refs)):
            raise ValueError('duplicate reference')
        if node.get('trusted'):
            if refs or trusted.get(mask) != v:
                raise ValueError('unattested trusted leaf')
        else:
            actual, vals = set(), []
            for ref in refs:
                child = int(nodes[ref]['mask'])
                if child.bit_count() != mask.bit_count()+1 or child not in ch:
                    raise ValueError('illegal/unranked child')
                if child in actual:
                    raise ValueError('duplicate canonical child')
                actual.add(child)
                vals.append(visit(ref))
            existential = v == (2 if mask.bit_count()%2 else 1)
            if existential:
                if not vals or v not in vals:
                    raise ValueError('missing decisive witness')
            elif actual != ch or aggregate(mask.bit_count(), vals) != v:
                raise ValueError('incomplete/incorrect universal boundary')
        visiting.remove(ident)
        done[ident] = v
        return v
    if 'roots' in certificate:
        result = {r:visit(r) for r in certificate['roots']}
    else:
        result = visit(certificate['root'])
    if len(done) != len(nodes):
        raise ValueError('unreachable certificate nodes')
    return result


def solve_certificate(board, root, limit):
    """Bounded independent minimax; publish only the reachable proof sub-DAG."""
    memo, proof = {}, {}
    visited = 0
    def solve(mask):
        nonlocal visited
        mask = board.canonical(mask)
        if mask in memo:
            return memo[mask]
        if visited >= limit:
            return 0
        visited += 1
        ch = board.children(mask)
        decisive = 2 if mask.bit_count()%2 else 1
        vals, refs = [], []
        for c in sorted(ch, key=lambda c:(board.legal(c).bit_count(),c)):
            v = solve(c)
            vals.append(v)
            refs.append(str(c))
            if v == decisive:
                vals, refs = [v], [str(c)]
                break
        v = aggregate(mask.bit_count(), vals)
        memo[mask] = v
        if v:
            proof[str(mask)] = dict(mask=str(mask),verdict=v,children=refs)
        return v
    root = board.canonical(root)
    verdict = solve(root)
    if not verdict:
        return dict(verdict=0,visited=visited,certificate=None)
    keep = {}
    def collect(ident):
        if ident in keep:
            return
        keep[ident] = proof[ident]
        for c in keep[ident]['children']:
            collect(c)
    collect(str(root))
    cert = dict(root=str(root),nodes=keep)
    assert verify_dag(board,cert) == verdict
    return dict(verdict=verdict,visited=visited,certificate=cert)
