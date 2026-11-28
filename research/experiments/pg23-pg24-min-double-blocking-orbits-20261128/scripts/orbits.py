import os
"""PGL(3,q) orbit census of maximal-safe / minimal-double-blocking families
in PG(2,3) and PG(2,4), plus complement-bijection verification (K1365 duality).

Group: GL(3,q) modulo scalar centers, acting on 1-d subspaces (points).
Orbit partition computed by BFS from orbit representatives (each group element
applied once per orbit), which is exact because the orbit count is small.
"""
import json, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boards import make_field, inv_table

def gen_pgl(q, board):
    add, mul = make_field(q)
    inv = inv_table(q, mul)
    pts = board['points']
    index = {tuple(p): i for i, p in enumerate(pts)}
    def canon(v):
        for i in range(3):
            if v[i] != 0:
                s = inv[v[i]]
                return tuple(mul[s][v[i]] for i in range(3))
        return None
    # proper determinant via expansion with field add/sub
    # char 2 (q=4): additive inverse = identity; else -a
    neg = list(range(q)) if q % 2 == 0 else [(q - a) % q for a in range(q)]
    def sub(x, y): return add[x][neg[y]]
    def det(m):
        t1 = mul[m[0][0]][sub(mul[m[1][1]][m[2][2]], mul[m[1][2]][m[2][1]])]
        t2 = mul[m[0][1]][sub(mul[m[1][0]][m[2][2]], mul[m[1][2]][m[2][0]])]
        t3 = mul[m[0][2]][sub(mul[m[1][0]][m[2][1]], mul[m[1][1]][m[2][0]])]
        return add[sub(t1, t2)][t3]
    perms = {}
    for a0 in range(q):
     for a1 in range(q):
      for a2 in range(q):
       for b0 in range(q):
        for b1 in range(q):
         for b2 in range(q):
          for c0 in range(q):
           for c1 in range(q):
            for c2 in range(q):
                m = ((a0,a1,a2),(b0,b1,b2),(c0,c1,c2))
                if det(m) == 0:
                    continue
                # normalize mod scalar: divide by first nonzero entry
                flat = [a0,a1,a2,b0,b1,b2,c0,c1,c2]
                nz = next(x for x in flat if x != 0)
                s = inv[nz]
                key = tuple(mul[s][x] for x in flat)
                if key in perms:
                    continue
                perm = [None]*len(pts)
                for pi, p in enumerate(pts):
                    v = [0,0,0]
                    for r in range(3):
                        acc = 0
                        for cc in range(3):
                            acc = add[acc][mul[m[r][cc]][p[cc]]]
                        v[r] = acc
                    perm[pi] = index[canon(v)]
                assert len(set(perm)) == len(pts)
                perms[key] = tuple(perm)
    return list(perms.values())

def apply_perm(mask, perm):
    r = 0
    m = mask
    while m:
        b = m & -m
        r |= 1 << perm[b.bit_length()-1]
        m ^= b
    return r

def orbit_partition(masks, perms):
    seen = {}
    reps = []
    for g in masks:
        if g in seen:
            continue
        # orbit = G.g (image of rep under every group element is the whole orbit)
        orbit = set(apply_perm(g, pm) for pm in perms)
        for y in orbit:
            seen[y] = len(reps)
        reps.append(g)
    return reps, seen

def profile(mask, board):
    from collections import Counter
    return dict(sorted(Counter(bin(mask & sum(1 << p for p in L)).count('1')
                               for L in board['lines']).items()))

def main():
    boards = json.load(open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/out/boards.json'))
    out = {}
    for q in (3, 4):
        board = boards[f'pg2q{q}']
        t0 = time.time()
        perms = gen_pgl(q, board)
        wallg = time.time()-t0
        print(f'PG(2,{q}): |PGL(3,{q})| = {len(perms)} (gen {wallg:.1f}s)')
        fams = {}
        for name in ('maximal_safe', 'minimal_db'):
            masks = []
            for line in open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+f'/out/pg2q{q}_{name}.txt'):
                sz, g = line.split()
                masks.append(int(g))
            t1 = time.time()
            reps, seen = orbit_partition(masks, perms)
            fams[name] = {'masks': masks, 'reps': reps, 'seen': seen,
                          'wall_s': round(time.time()-t1, 2)}
            sizes = [bin(r).count('1') for r in reps]
            counts = [0]*len(reps)
            for g, oi in seen.items():
                counts[oi] += 1
            assert sum(counts) == len(masks)
            print(f'  {name}: {len(masks)} masks -> {len(reps)} PGL orbits '
                  f'(sizes {sizes}, orbit sizes {sorted(counts, reverse=True)})')
        # complement bijection check (K1365): complement of maximal safe is
        # minimal DB and vice versa, both directions
        full = (1 << board['n']) - 1
        ms_set = set(fams['maximal_safe']['masks'])
        db_set = set(fams['minimal_db']['masks'])
        fwd = all((full ^ g) in db_set for g in ms_set)
        bwd = all((full ^ g) in ms_set for g in db_set)
        print(f'  complement bijection maximal_safe<->minimal_db: fwd={fwd} bwd={bwd}')
        # orbit-level info with invariants
        orbits_info = {}
        for name in ('maximal_safe', 'minimal_db'):
            reps = fams[name]['reps']
            counts = [0]*len(reps)
            for g, oi in fams[name]['seen'].items():
                counts[oi] += 1
            info = []
            for r, c in zip(reps, counts):
                info.append({
                    'rep_mask': r, 'rep_points': sorted(
                        [i for i in range(board['n']) if (r >> i) & 1]),
                    'size': bin(r).count('1'), 'orbit_size': c,
                    'line_profile': {str(k): v for k, v in profile(r, board).items()},
                })
            info.sort(key=lambda x: (x['size'], x['rep_mask']))
            orbits_info[name] = info
        out[f'pg2q{q}'] = {
            'pgl_order': len(perms),
            'group_gen_wall_s': round(wallg, 2),
            'maximal_safe': {'masks': len(fams['maximal_safe']['masks']),
                             'orbits': orbits_info['maximal_safe'],
                             'wall_s': fams['maximal_safe']['wall_s']},
            'minimal_db': {'masks': len(fams['minimal_db']['masks']),
                           'orbits': orbits_info['minimal_db'],
                           'wall_s': fams['minimal_db']['wall_s']},
            'complement_bijection': {'fwd': fwd, 'bwd': bwd},
        }
    with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/out/orbits.json', 'w') as f:
        json.dump(out, f, indent=1)
    print('wrote orbits.json')

if __name__ == '__main__':
    main()
