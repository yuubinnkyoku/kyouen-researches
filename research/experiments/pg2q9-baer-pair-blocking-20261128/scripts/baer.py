"""Baer subplane pair analysis for double blocking in PG(2,q^2), q = 2,3,4.

Key facts used (Baer subplane B of PG(2,q^2), |B| = q^2+q+1):
 - every line meets B in 1 or q+1 points (verified per base + orbit samples)
 - for two Baer subplanes A, B: a line L has |(A u B) cap L| < 2 only if
   |A cap L| = 1 or |B cap L| = 1, since otherwise |A u B cap L| >= max >= 2.
   So the double-blocking test only needs the solo lines of A and B.
 - if A and B are disjoint, every line meets A u B in >= 2 automatically
   (1 from each) -> size-2(q^2+q+1) double blocking.

Modes: q=2 (PG(2,4)) and q=3 (PG(2,9)) use the FULL Baer orbit with an exact
pair census; q=4 (PG(2,16)) uses a seeded random walk (sampled, disclosed).

Outputs: intersection census, minimal double-blocking union among Baer pairs
(exact for q=2,3; best-found for q=4), witnesses (definition-verified),
disjoint-pair counts.
"""
import json, math, os, random, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boards9 import build_pg

def matvec_perm(board, m):
    add, mul = board['add'], board['mul']
    pts = board['points']
    inv = board['inv']
    idx = {tuple(p): i for i, p in enumerate(pts)}
    def canon(v):
        for i in range(3):
            if v[i] != 0:
                s = inv[v[i]]
                return tuple(mul[s][v[i]] for i in range(3))
        return None
    perm = []
    for pv in pts:
        v = [0, 0, 0]
        for r in range(3):
            acc = 0
            for c in range(3):
                acc = add[acc][mul[m[r][c]][pv[c]]]
            v[r] = acc
        perm.append(idx[canon(v)])
    assert sorted(perm) == list(range(len(pts)))
    return tuple(perm)

def generators(board):
    q2 = board['q']
    gens = []
    ident = [[1 if i == j else 0 for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            for c in range(1, q2):
                m = [row[:] for row in ident]
                m[i][j] = c
                gens.append(m)
    for a in range(1, q2):
        m = [[a if i == 0 and j == 0 else (1 if i == j else 0) for j in range(3)]
             for i in range(3)]
        gens.append(m)
    for (i, j) in ((0, 1), (1, 2)):
        m = [row[:] for row in ident]
        m[i], m[j] = m[j], m[i]
        gens.append(m)
    return [matvec_perm(board, m) for m in gens]

def apply_perm(mask, perm):
    r = 0
    m = mask
    while m:
        b = m & -m
        r |= 1 << perm[b.bit_length() - 1]
        m ^= b
    return r

def orbit_bfs(base_mask, perms):
    seen = {base_mask}
    frontier = [base_mask]
    while frontier:
        nf = []
        for x in frontier:
            for pm in perms:
                y = apply_perm(x, pm)
                if y not in seen:
                    seen.add(y)
                    nf.append(y)
        frontier = nf
    return seen

def verify_baer_base(board):
    base = set(board['baer_base'])
    q = (math.isqrt(4 * len(base) - 3) - 1) // 2
    assert q * q + q + 1 == len(base)
    assert q * q == board['q']
    prof = Counter()
    for L in board['lines']:
        prof[len(base.intersection(L))] += 1
    assert set(prof) <= {1, q + 1}, prof
    assert sum(prof.values()) == len(board['lines'])
    sublines = [L for L in board['lines'] if len(base.intersection(L)) == q + 1]
    assert len(sublines) == q * q + q + 1
    from collections import defaultdict
    pc = defaultdict(int)
    for L in sublines:
        ss = sorted(base.intersection(L))
        for i in range(len(ss)):
            for j in range(i + 1, len(ss)):
                pc[(ss[i], ss[j])] += 1
    assert len(pc) == len(base) * (len(base) - 1) // 2
    assert all(v == 1 for v in pc.values())
    return q, {'profile': {str(k): v for k, v in sorted(prof.items())},
               'sublines': len(sublines), 'design': '2-(%d,%d,1) OK' % (len(base), q + 1)}

def solo_lines(board, mask, lineM):
    return [li for li in range(len(lineM)) if (mask & lineM[li]).bit_count() == 1]

def double_blocks(umask, board, lineM, soloA, soloB):
    for li in soloA:
        if (umask & lineM[li]).bit_count() < 2:
            return False
    for li in soloB:
        if (umask & lineM[li]).bit_count() < 2:
            return False
    return True

def analyze_plane(q2, mode, sample_n=3000):
    board = build_pg(q2)
    q, baer_check = verify_baer_base(board)
    base_mask = sum(1 << p for p in board['baer_base'])
    lineM = [sum(1 << p for p in L) for L in board['lines']]
    gens = generators(board)
    solo_base = solo_lines(board, base_mask, lineM)
    if mode == 'full':
        orbit = orbit_bfs(base_mask, gens)
        masks = sorted(orbit)
        N = len(masks)
        # orbit-stabilizer consistency
        gl = (q2**3 - 1) * (q2**3 - q2) * (q2**3 - q2 * q2)
        pgl = gl // (q2 - 1)
        assert pgl % N == 0
        stab = pgl // N
        # precompute solo lines per mask
        solos = {m: solo_lines(board, m, lineM) for m in masks}
        inter_hist = Counter()
        disjoint_pairs = 0
        for i in range(N):
            mi = masks[i]
            for j in range(i + 1, N):
                c = (mi & masks[j]).bit_count()
                inter_hist[c] += 1
                if c == 0:
                    disjoint_pairs += 1
        result = {'mode': 'full', 'plane': f'PG(2,{q2})', 'subplane': f'PG(2,{q})',
                  'baer_base_check': baer_check, 'orbit_size': N,
                  'pgl_order': pgl, 'stabilizer_order': stab,
                  'intersection_census': {str(k): v for k, v in sorted(inter_hist.items())},
                  'disjoint_pairs': disjoint_pairs}
        # find minimal double-blocking union: re-scan pairs per intersection
        # size c in descending order (union ascending), no pair storage
        found = None
        for c in sorted(inter_hist, reverse=True):
            u = 2 * (q * q + q + 1) - c
            hits = 0
            for i in range(N):
                mi = masks[i]
                si = solos[mi]
                for j in range(i + 1, N):
                    if (mi & masks[j]).bit_count() != c:
                        continue
                    mj = masks[j]
                    if double_blocks(mi | mj, board, lineM, si, solos[mj]):
                        hits += 1
                        if found is None:
                            found = (u, c, i, j, mi | mj)
            result[f'passing_pairs_union_{u}'] = hits
            print(f'  c={c} (union {u}): {hits} double-blocking pairs '
                  f'of {inter_hist[c]}')
            if found is not None:
                break
        if found:
            u, c, i, j, umask = found
            per_line = [(umask & lineM[li]).bit_count() for li in range(len(lineM))]
            assert min(per_line) >= 2
            result['min_double_blocking_union'] = u
            result['min_pair_intersection'] = c
            result['passing_pairs_at_min'] = result[f'passing_pairs_union_{u}']
            result['witness_points'] = sorted([k for k in range(board['n'])
                                                if (umask >> k) & 1])
            result['witness_profile'] = {str(k): v for k, v in
                                         sorted(Counter(per_line).items())}
        else:
            result['min_double_blocking_union'] = None
        return result
    else:
        # sampled random-walk census (disclosed as sampling)
        random.seed(20261128)
        inter_hist = Counter()
        best_disjoint = None
        best_small = None
        cur = base_mask
        for _ in range(sample_n):
            cur = apply_perm(cur, random.choice(gens))
            c = (base_mask & cur).bit_count()
            inter_hist[c] += 1
            u = 2 * (q * q + q + 1) - c
            if c == 0 and best_disjoint is None:
                best_disjoint = cur
            if best_small is None or u < 2 * (q * q + q + 1) - (base_mask & best_small).bit_count():
                if double_blocks(base_mask | cur, board, lineM,
                                 solo_base, solo_lines(board, cur, lineM)):
                    best_small = cur
        result = {'mode': 'sample', 'plane': f'PG(2,{q2})', 'subplane': f'PG(2,{q})',
                  'baer_base_check': baer_check, 'samples': sample_n,
                  'sampled_intersection_census': {str(k): v for k, v in sorted(inter_hist.items())}}
        if best_disjoint is not None:
            umask = base_mask | best_disjoint
            per_line = [(umask & lineM[li]).bit_count() for li in range(len(lineM))]
            assert min(per_line) >= 2
            result['disjoint_witness_size'] = umask.bit_count()
            result['disjoint_witness_points'] = sorted([k for k in range(board['n'])
                                                        if (umask >> k) & 1])
        if best_small is not None:
            umask = base_mask | best_small
            per_line = [(umask & lineM[li]).bit_count() for li in range(len(lineM))]
            assert min(per_line) >= 2
            result['best_small_witness_size'] = umask.bit_count()
            result['best_small_witness_points'] = sorted([k for k in range(board['n'])
                                                          if (umask >> k) & 1])
        return result

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plane = sys.argv[1] if len(sys.argv) > 1 else 'all'
    out = {}
    plan = [('4', 'full'), ('9', 'full'), ('16', 'sample')]
    for q2, mode in plan:
        if plane != 'all' and plane != q2:
            continue
        print(f'=== PG(2,{q2}) ({mode}) ===')
        out[f'pg2q{q2}'] = analyze_plane(int(q2), mode)
        print(json.dumps(out[f'pg2q{q2}'])[:600])
    path = os.path.join(root, 'out', 'baer_pairs.json')
    if plane != 'all':
        try:
            prev = json.load(open(path))
        except FileNotFoundError:
            prev = {}
        prev.update(out)
        out = prev
    with open(path, 'w') as f:
        json.dump(out, f, indent=1)
    print('wrote', path)

if __name__ == '__main__':
    main()
