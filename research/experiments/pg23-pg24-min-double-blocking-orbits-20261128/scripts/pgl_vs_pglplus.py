import os
"""PGL vs PGL+ (semilinear) orbit comparison for PG(2,4).

The field automorphism sigma: alpha -> alpha+1 (i.e. 2 <-> 3 on
{0,1,2,3}) acts on point coordinates; PGL(3,4) < PGammaL(3,4) of order
2*60480 = 120960. Reports whether the PGL orbit classes merge under
PGammaL. Fails closed on any inconsistency.
"""
import json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boards import make_field
from orbits import gen_pgl, apply_perm, orbit_partition

def sigma_perm(board):
    add, _ = make_field(4)
    # sigma: 0->0, 1->1, 2->3, 3->2  (alpha -> alpha+1)
    sig = [0, 1, 3, 2]
    pts = board['points']
    index = {tuple(p): i for i, p in enumerate(pts)}
    perm = []
    for p in pts:
        q = tuple(sig[x] for x in p)
        # re-canonicalize: first nonzero must be 1; over GF(4) sig(1)=1 so the
        # canonical form is preserved automatically
        perm.append(index[q])
    assert len(set(perm)) == len(pts)
    return tuple(perm)

def main():
    boards = json.load(open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/out/boards.json'))
    board = boards['pg2q4']
    perms = gen_pgl(4, board)
    sp = sigma_perm(board)
    # sanity: sigma^2 = id
    assert all(sp[sp[i]] == i for i in range(len(sp)))
    full_group = perms + [tuple(sp[pm[i]] for i in range(len(pm))) for pm in perms]
    assert len(full_group) == 2*len(perms)
    out = {}
    for name in ('maximal_safe', 'minimal_db'):
        masks = [int(l.split()[1]) for l in
                 open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+f'/out/pg2q4_{name}.txt')]
        reps, seen = orbit_partition(masks, full_group)
        # also PGL-only for comparison
        reps_g, seen_g = orbit_partition(masks, perms)
        sizes = [bin(r).count('1') for r in reps]
        counts = [0]*len(reps)
        for g, oi in seen.items():
            counts[oi] += 1
        out[name] = {
            'pgl_orbits': len(reps_g), 'pgammal_orbits': len(reps),
            'pgammal_orbit_sizes': dict(zip(sizes, counts)) if len(sizes) == len(set(sizes)) else None,
            'orbits': [{'size': sz, 'orbit_size': c} for sz, c in zip(sizes, counts)],
        }
        print(f'PG(2,4) {name}: PGL {len(reps_g)} orbits -> PGammaL {len(reps)} orbits')
        for e in out[name]['orbits']:
            print('   ', e)
    with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/out/pgammal.json', 'w') as f:
        json.dump(out, f, indent=1)

if __name__ == '__main__':
    main()
