#!/usr/bin/env python3
"""Neighbor analysis for the three STERILE rows of the best coverable
class-2 S5 00000000000000801202000000200000 at the post-cost-60c canonical
head 1410: enumerate the one-stone-replacement open-row neighbors of each
STERILE child (65k / 70j / 74h), classify them by edge cost and swept /
claimed status, and pre-compute which legal candidate roots of the cheapest
unswept neighbors cover which STERILE rows (cross-cover pre-check).

Python standard library only; exact integer Bareiss determinants; no
repository engine code.  Bookkeeping only; 11x11 empty board and all roots /
classes remain UNKNOWN.
"""
import glob
import json
import os
import runpy

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'output')
MS5 = os.path.join(HERE, '..', '..', 'n11-s2-5960-milestone5-20261112', 'output')

STERILE = {
    '65k': '00000000020000801202000000200000',
    '70j': '00000000000000801282000000200000',
    '74h': '00000000000000889002000000000800',
}


def bareiss4(m):
    m = [row[:] for row in m]
    prev = 1
    for k in range(3):
        if m[k][k] == 0:
            for r in range(k + 1, 4):
                if m[r][k] != 0:
                    m[k], m[r] = m[r], m[k]
                    break
            else:
                return 0
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                m[i][j] = (m[i][j] * m[k][k] - m[i][k] * m[k][j]) // prev
            m[i][k] = 0
        prev = m[k][k]
    return m[3][3]


def row_of(cell):
    x = cell % 11
    y = cell // 11
    return [x * x + y * y, x, y, 1]


def det4(cells):
    return bareiss4([row_of(c) for c in cells])


def stones(hexstr):
    v = int(hexstr, 16)
    return [i for i in range(121) if (v >> i) & 1]


def enumerate_legal(hexstr):
    st = stones(hexstr)
    legal = []
    for p in range(121):
        if p in st:
            continue
        unsafe = False
        n = len(st)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if det4([st[i], st[j], st[k], p]) == 0:
                        unsafe = True
                        break
                if unsafe:
                    break
            if unsafe:
                break
        if not unsafe:
            legal.append(p)
    return st, legal


def d4_canon(hexstr):
    st = stones(hexstr)
    best = None
    for swap in (0, 1):
        for fx in (0, 1):
            for fy in (0, 1):
                t = []
                for c in st:
                    x, y = c % 11, c // 11
                    a, b = (y, x) if swap else (x, y)
                    if fx:
                        a = 10 - a
                    if fy:
                        b = 10 - b
                    t.append(a + 11 * b)
                v = 0
                for i in t:
                    v |= 1 << i
                h = format(v, '032x')
                if best is None or h < best:
                    best = h
    return best


def main():
    ns = runpy.run_path(os.path.join(HERE, 'recompute_frontier_cost60c_receipts_20261116.py'))
    s_after = set(ns['s_after'])
    manifest = ns['manifest']
    rem = ns['rem_after']
    dem = ns['dem_after']
    st_after = ns['st_after']
    assert (st_after['solved_s6_in_manifest'], st_after['remaining_s5_orbits'],
            st_after['unique_remaining_s6'], st_after['sum_remaining_cost'],
            st_after['s6_needed_by_open_classes'],
            st_after['cost_needed_by_open_classes']) == \
        (1410, 174, 6438, 509109, 4711, 373023), st_after
    canon = ns['canon']

    # edge cost lookup from the published MS5 S6 manifest parts
    cost = {}
    for mp in sorted(glob.glob(os.path.join(MS5, 'ms5_s6_manifest_part*.csv'))):
        with open(mp) as f:
            for line in f:
                if line.startswith('hex,'):
                    continue
                parts = line.strip().split(',')
                if parts and parts[0]:
                    cost[parts[0]] = int(parts[1])

    # swept / claimed children: every published claim file's s6_child
    claimed = {}
    for p in glob.glob(os.path.join(OUT, '*inflight*.json')):
        try:
            c = json.load(open(p))
        except Exception:
            continue
        ch = c.get('s6_child')
        if ch:
            claimed[ch] = os.path.basename(p)

    targets = {name: int(h, 16) for name, h in STERILE.items()}
    result = {}
    unswept_pool = {}
    for name, hexstr in STERILE.items():
        assert hexstr in cost and int(hexstr, 16) in manifest, name
        st = stones(hexstr)
        assert len(st) == 6
        neighbors = {}
        for s in st:
            for p in range(121):
                if p == s or p in st:
                    continue
                v = 0
                for x in st:
                    if x != s:
                        v |= 1 << x
                v |= 1 << p
                h = d4_canon(format(v, '032x'))
                neighbors[h] = True
        rows = []
        for h in sorted(neighbors):
            v = int(h, 16)
            in_man = v in manifest
            open_ = in_man and v not in s_after
            rows.append({
                'hex': h,
                'cost': cost.get(h),
                'in_manifest': in_man,
                'open': open_,
                'claimed': claimed.get(h),
                'demand': dem.get(h),
            })
        open_rows = [r for r in rows if r['open']]
        open_rows.sort(key=lambda r: (r['cost'], r['hex']))
        unswept = [r for r in open_rows if not r['claimed']]
        result[name] = {
            'sterile_row': hexstr,
            'edge_cost': cost[hexstr],
            'one_stone_replacement_neighbors': len(rows),
            'open_rows': len(open_rows),
            'unswept_open_rows': len(unswept),
            'cheapest_unswept': [
                {'hex': r['hex'], 'cost': r['cost'], 'demand': r['demand']}
                for r in unswept[:8]],
            'cheapest_open_all': [
                {'hex': r['hex'], 'cost': r['cost'],
                 'claimed': r['claimed']} for r in open_rows[:8]],
        }
        for r in unswept[:6]:
            unswept_pool[r['hex']] = r['cost']
        print(name, hexstr, 'cost', cost[hexstr], 'neighbors', len(rows),
              'open', len(open_rows), 'unswept', len(unswept))
        for r in unswept[:6]:
            print('   cheapest unswept:', r['hex'], 'cost', r['cost'],
                  'demand', r['demand'])

    # cross-cover pre-check for the cheapest unswept neighbors (cost <= 70)
    cover_map = {}
    for h, c in sorted(unswept_pool.items(), key=lambda kv: (kv[1], kv[0])):
        if c > 70:
            continue
        st, legal = enumerate_legal(h)
        cov = {}
        for b in legal:
            root = st + [b]
            dels = set()
            for s in root:
                v = 0
                for x in root:
                    if x != s:
                        v |= 1 << x
                dels.add(int(d4_canon(format(v, '032x')), 16))
            for name, tv in targets.items():
                if tv in dels:
                    cov.setdefault(name, []).append(b)
        if cov:
            cover_map[h] = {'cost': c, 'legal': len(legal), 'covers': cov}
            print('CROSS-COVER', h, 'cost', c, 'legal', len(legal),
                  'covers', cov)
    out = {
        'schema': 'n11-class2-lane-sterile-neighbor-analysis-20261116-v1',
        'date': '2026-11-16',
        'head': '1410/174/6438/509109/4711/373023',
        'sterile_rows': result,
        'cross_cover_precheck_cost_le_70': cover_map,
        'note': 'covers re-derived by exact-integer D4 canonicalization over all '
                'legal candidates x 7 deletions; bookkeeping only; NOT a claim; '
                '11x11 empty board and all roots/classes remain UNKNOWN',
    }
    with open(os.path.join(OUT, 'class2-lane-sterile-rows-neighbor-analysis-20261116.json'), 'w') as f:
        f.write(json.dumps(out, indent=1) + '\n')
    print('written class2-lane-sterile-rows-neighbor-analysis-20261116.json')


if __name__ == '__main__':
    main()
