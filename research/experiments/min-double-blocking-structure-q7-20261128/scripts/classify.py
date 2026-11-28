#!/usr/bin/env python3
"""Structure classification of minimal 2-fold blocking sets in AG(2,q) (pure python).

Definitions re-verified per mask (independent of the C enumerator):
  2-fold blocking: every line meets C in >= 2 points
  minimality: every p in C lies on a line l with |C cap l| == 2
Line profile = sorted multiset {|C cap l|}, AGL-invariant.
Orbit census via orbit expansion: for one representative per orbit we
enumerate all |AGL(2,q)| images once; profiles partition configs so the
image set of a representative is exactly its orbit within its profile class.
canonical form = min mask in orbit; classes of equal canonical form = orbits.
"""
import json, sys, os
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from boards import affine_plane, field

def load_list(path):
    return [int(l.strip(), 16) for l in open(path) if l.strip()]

def agl_perms(q):
    add, mul, neg, one = field(q)
    pts = [(x, y) for y in range(q) for x in range(q)]
    idx = {p: i for i, p in enumerate(pts)}
    perms = []
    for a in range(q):
        for b in range(q):
            for c in range(q):
                for d in range(q):
                    if add(mul(a, d), neg(mul(b, c))) == 0:
                        continue
                    for t1 in range(q):
                        for t2 in range(q):
                            perm = [0] * q * q
                            for i, (x, y) in enumerate(pts):
                                nx = add(add(mul(a, x), mul(b, y)), t1)
                                ny = add(add(mul(c, x), mul(d, y)), t2)
                                perm[i] = idx[(nx, ny)]
                            perms.append(tuple(perm))
    return perms

def main(list_path, q, s, out_path):
    q = int(q)
    pts, raw = affine_plane(q)
    n = len(pts)
    lines = [sorted(l) for l in raw]
    line_masks = [sum(1 << p for p in l) for l in lines]
    masks = load_list(list_path)
    print('loaded', len(masks), 'masks')
    sizes = Counter()
    for m in masks:
        cnt = [(m & lm).bit_count() for lm in line_masks]
        assert min(cnt) >= 2, hex(m)
        for p in range(n):
            if (m >> p) & 1:
                assert any(c == 2 and (line_masks[i] >> p) & 1
                           for i, c in enumerate(cnt)), (hex(m), p)
        sizes[bin(m).count('1')] += 1
    print('all verified, sizes:', dict(sizes))
    perms = agl_perms(q)
    G = len(perms)
    print('AGL(2,%d) order %d' % (q, G))
    def profile(m):
        return tuple(sorted((m & lm).bit_count() for lm in line_masks))
    by_profile = defaultdict(set)
    for m in masks:
        by_profile[profile(m)].add(m)
    print('profile classes:', len(by_profile))
    orbits = []
    seen = set()
    for prof, cls in sorted(by_profile.items(), key=lambda kv: min(kv[1])):
        remaining = set(cls)
        while remaining:
            rep = min(remaining)
            pts_c = [i for i in range(n) if (rep >> i) & 1]
            orb = set()
            for perm in perms:
                m2 = 0
                for p in pts_c:
                    m2 |= 1 << perm[p]
                orb.add(m2)
            assert orb <= cls
            remaining -= orb
            seen |= orb
            orbits.append((min(orb), len(orb), prof, rep))
    assert len(seen) == len(masks)
    by_size = defaultdict(list)
    for canon, size, prof, rep in orbits:
        by_size[bin(canon).count('1')].append(
            {'canon': hex(canon), 'orbit_size': size, 'rep': hex(rep),
             'profile': list(prof)})
    for k in by_size:
        by_size[k].sort(key=lambda r: -r['orbit_size'])
    summary = {'board': 'AG(2,%d)' % q, 's': s, 'total_masks': len(masks),
               'size_counts': dict(sizes), 'n_points': n, 'n_lines': len(lines),
               'agl_order': G, 'n_profile_classes': len(by_profile),
               'n_orbits': len(orbits),
               'orbits_by_size': {str(k): v for k, v in by_size.items()},
               'orbit_count_by_size': {str(k): len(v) for k, v in by_size.items()}}
    with open(out_path, 'w') as f:
        json.dump(summary, f, indent=1)
    print('orbits total:', len(orbits))
    for k in sorted(by_size):
        print(' size %d: %d orbits' % (k, len(by_size[k])))
        for r in by_size[k][:8]:
            print('   orbit size %6d canon %s profile %s' %
                  (r['orbit_size'], r['canon'], r['profile']))

if __name__ == '__main__':
    main(*sys.argv[1:])
