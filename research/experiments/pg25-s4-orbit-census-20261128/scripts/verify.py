"""Independent verification for the PG(2,5) s=4 orbit census (affine model).

Different implementation choices from enum.c/orbits.js on purpose:
- PG(2,5) built in the AFFINE model: points (x,y,1) [25], (1,m,0) [5]
  (infinity of direction (1,m)), (0,1,0) [1] (vertical direction).
  The C enumerator's canonical-triple labeling is mapped onto this model and
  the map is fail-closed checked (image of every C line must be a line).
- PGL(3,5) built from 4 generators DIFFERENT from the JS set; group order
  must be exactly 372000.
- Full independent orbit partition of the size class, compared against the
  JS classification (orbit size multiset + rep membership), fail-closed.

Modes (argv):
  verify <size>  : verify all masks of the given size (safety, maximality,
                   complement 2-fold blocking + minimality) + total counts
  orbit <size>   : group order check + full orbit re-partition of the size
                   class, compare with orbits JSON
"""

import json, struct, sys

Q = 5
INV = {1: 1, 2: 3, 3: 2, 4: 4}
FULL = 0x7fffffff


def affine_points():
    pts = []
    for y in range(Q):
        for x in range(Q):
            pts.append((x, y, 1))
    for m in range(Q):
        pts.append((1, m, 0))
    pts.append((0, 1, 0))
    return pts


def affine_lines():
    aff = {t: i for i, t in enumerate(affine_points())}
    pid = aff.__getitem__
    lines = []
    for m in range(Q):
        for b in range(Q):
            lines.append([pid((x, (m * x + b) % Q, 1)) for x in range(Q)]
                         + [pid((1, m, 0))])
    for a in range(Q):
        lines.append([pid((a, y, 1)) for y in range(Q)] + [pid((0, 1, 0))])
    lines.append([pid((1, m, 0)) for m in range(Q)] + [pid((0, 1, 0))])
    assert len(lines) == 31
    for L in lines:
        assert len(L) == 6 and len(set(L)) == 6
    return lines


def c_labels():
    pts = []
    for a in range(Q):
        for b in range(Q):
            for c in range(Q):
                if not a and not b and not c:
                    continue
                if not (a == 1 or (not a and b == 1) or (not a and not b and c == 1)):
                    continue
                pts.append((a, b, c))
    assert len(pts) == 31
    return pts


def c_lines():
    pts = c_labels()
    masks = []
    for a in range(Q):
        for b in range(Q):
            for c in range(Q):
                if not a and not b and not c:
                    continue
                if not (a == 1 or (not a and b == 1) or (not a and not b and c == 1)):
                    continue
                m = 0
                for i, (x, y, z) in enumerate(pts):
                    if (a * x + b * y + c * z) % Q == 0:
                        m |= 1 << i
                masks.append(m)
    assert len(masks) == 31
    return masks


def c_to_affine():
    aff = {t: i for i, t in enumerate(affine_points())}
    out = []
    for (a, b, c) in c_labels():
        if c:
            ic = INV[c]
            t = ((a * ic) % Q, (b * ic) % Q, 1)
        elif b:
            if a:
                t = (1, (b * INV[a]) % Q, 0)
            else:
                t = (0, 1, 0)
        else:
            t = (1, 0, 0)
        assert t in aff, (a, b, c, t)
        out.append(aff[t])
    assert len(set(out)) == 31
    return out


def relabel_tables(c2a):
    T = []
    for k in range(4):
        tab = [0] * 256
        for b in range(256):
            v = 0
            for j in range(8):
                if (b >> j) & 1 and 8 * k + j < 31:
                    v |= 1 << c2a[8 * k + j]
            tab[b] = v
        T.append(tab)
    return T


def relabel(masks, c2a):
    T0, T1, T2, T3 = relabel_tables(c2a)
    return [T0[m & 255] | T1[(m >> 8) & 255] | T2[(m >> 16) & 255]
            | T3[(m >> 24) & 255] for m in masks]


def perm_tables(perm):
    T = []
    for k in range(4):
        tab = [0] * 256
        for b in range(256):
            v = 0
            for j in range(8):
                if (b >> j) & 1 and 8 * k + j < 31:
                    v |= 1 << perm[8 * k + j]
            tab[b] = v
        T.append(tab)
    return T


def build_perm_from_matrix(M):
    pts = affine_points()
    aff = {t: i for i, t in enumerate(pts)}
    perm = [0] * 31
    for i, (x, y, z) in enumerate(pts):
        v = [(M[r][0] * x + M[r][1] * y + M[r][2] * z) % Q for r in range(3)]
        if not any(v):
            raise ValueError('zero image')
        if v[2] != 0:
            w = ((v[0] * INV[v[2]]) % Q, (v[1] * INV[v[2]]) % Q, 1)
        elif v[0] != 0:
            w = (1, (v[1] * INV[v[0]]) % Q, 0)
        else:
            w = (0, 1, 0)
        perm[i] = aff[w]
    return bytes(perm)


def main():
    mode = sys.argv[1]
    size = int(sys.argv[2])
    dump = '/home/user/work/pg25c/masks25s4_fresh.bin'
    orbits_json = '/home/user/work/pg25c/orbits25s4.json'

    c2a = c_to_affine()
    # fail-closed: relabeling must map C lines to affine lines
    alines = affine_lines()
    amask = set(sum(1 << p for p in L) for L in alines)
    for L in c_lines():
        img = 0
        for i in range(31):
            if (L >> i) & 1:
                img |= 1 << c2a[i]
        assert img in amask, 'c2a does not preserve lines'
    line_masks = [sum(1 << p for p in L) for L in alines]
    through = [[] for _ in range(31)]
    for li, L in enumerate(alines):
        for p in L:
            through[p].append(li)

    data = open(dump, 'rb').read()
    n = len(data) // 4
    assert n * 4 == len(data)
    masks_c = list(struct.unpack('<%dI' % n, data))
    masks = relabel(masks_c, c2a)
    by = {}
    for m in masks:
        by.setdefault(m.bit_count(), []).append(m)
    counts = {k: len(v) for k, v in sorted(by.items())}
    print('counts', json.dumps(counts), flush=True)
    assert counts == {13: 15500, 14: 372000, 15: 604500, 16: 595975}
    del data, masks_c, masks
    import gc
    gc.collect()

    if mode == 'verify':
        sel = by[size]
        bad = 0
        shown = 0
        for m in sel:
            cnt = [(m & lm).bit_count() for lm in line_masks]
            ok = True
            if max(cnt) > 4:
                ok = False
                tag = 'UNSAFE'
            else:
                fullmask = 0
                for i, c in enumerate(cnt):
                    if c == 4:
                        fullmask |= line_masks[i]
                excl = (~m) & FULL
                if (excl & fullmask) != excl:
                    ok = False
                    tag = 'NOT MAXIMAL'
            if not ok:
                bad += 1
                if shown < 5:
                    print(tag, hex(m), flush=True)
                    shown += 1
        print('verify size', size, 'n', len(sel), 'bad', bad, flush=True)
        assert bad == 0
        print('VERIFY_OK', size, flush=True)

    elif mode == 'orbit':
        gens_m = [
            [[1, 2, 0], [0, 1, 0], [0, 0, 1]],
            [[1, 0, 0], [0, 1, 3], [0, 0, 1]],
            [[3, 0, 0], [0, 1, 0], [0, 0, 1]],
            [[0, 0, 1], [1, 0, 0], [0, 1, 0]],
        ]
        gens = [build_perm_from_matrix(M) for M in gens_m]
        gtab = [perm_tables(h) for h in gens]
        ident = bytes(range(31))
        seen = {ident}
        frontier = [ident]
        while frontier:
            nxt = []
            for g in frontier:
                for h in gens:
                    c = bytes(map(h.__getitem__, g))
                    if c not in seen:
                        seen.add(c)
                        nxt.append(c)
            frontier = nxt
        order = len(seen)
        print('python group order', order, flush=True)
        assert order == 372000, 'GROUP ORDER WRONG'

        sel = by[size]
        assign = {}
        orbits = []
        for m in sel:
            if m in assign:
                continue
            oid = len(orbits)
            stack = [m]
            assign[m] = oid
            members = []
            while stack:
                s = stack.pop()
                members.append(s)
                for gt in gtab:
                    r = (gt[0][s & 255] | gt[1][(s >> 8) & 255]
                         | gt[2][(s >> 16) & 255] | gt[3][(s >> 24) & 255])
                    if r not in assign:
                        assign[r] = oid
                        stack.append(r)
            orbits.append(members)
        sizes = sorted(len(o) for o in orbits)
        print('python orbit sizes', size, sizes, flush=True)

        d = json.load(open(orbits_json))
        js = sorted(o['size'] for o in d['sizes'][str(size)]['orbits'])
        assert sizes == js, ('ORBIT SIZE MISMATCH', sizes, js)
        for o in d['sizes'][str(size)]['orbits']:
            rep_c = int(o['rep'], 16)
            rep_a = 0
            for i in range(31):
                if (rep_c >> i) & 1:
                    rep_a |= 1 << c2a[i]
            assert rep_a in assign, 'JS rep not in python partition'
            assert len(orbits[assign[rep_a]]) == o['size'], 'rep orbit size mismatch'
        print('ORBIT_OK', size, len(orbits), 'orbits', flush=True)


if __name__ == '__main__':
    main()
