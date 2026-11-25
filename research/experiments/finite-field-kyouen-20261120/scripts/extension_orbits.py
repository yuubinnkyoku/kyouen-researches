"""Analyse the four-point extensions of the canonical triple at a given q.

The empty board's outcome reduces to g3, the Grundy value of a 3-point position,
which in turn is the mex of the Grundy values of its q^2-q four-point extensions
(K1253).  This script

  * builds the setwise stabiliser of the triple {0,1,2} inside PGL(2,q^2)
    (exactly S3, because PGL is sharply 3-transitive),
  * computes the orbits of the extensions under that stabiliser,
  * computes the cross-ratio class of every extension (the invariant of the
    4-point PGL-orbit),
  * writes the extension masks, so grundy_full can report the Grundy value of
    each extension position.

Run:  python extension_orbits.py --q 7 --fast ../output/circles_q7_fast.txt
"""

from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field  # noqa: E402
from inversive_fast import build_circles  # noqa: E402


def mobius_from_triples(F, t, u):
    """Moebius map with f(t[0])=u[0], f(t[1])=u[1], f(t[2])=u[2] (all finite)."""
    one = F.pow(t[0], 0)
    zero = F.sub(one, one)
    t0, t1, t2 = t
    u0, u1, u2 = u
    d_t = F.sub(t1, t0)
    inv_d_t = F.div(one, d_t)
    # phi_t(z) = ((z - t0)*(t1 - t2)) / ((z - t2)*(t1 - t0))
    num_t = F.sub(t1, t2)
    c = F.mul(F.sub(u1, u0), one)      # u1 - u0
    d = F.sub(u2, u1)                  # u2 - u1

    def f(z):
        if z == t2:
            return u2
        num = F.mul(F.sub(z, t0), num_t)
        den = F.mul(F.sub(z, t2), d_t)
        w = F.mul(num, F.div(one, den))
        # psi_u(w) = (u2*(u1-u0)*w + u0*(u2-u1)) / ((u1-u0)*w + (u2-u1))
        num2 = F.add(F.mul(F.mul(u2, c), w), F.mul(u0, d))
        den2 = F.add(F.mul(c, w), d)
        if F.is_zero(den2):
            return None
        return F.mul(num2, F.div(one, den2))

    return f


def cross_ratio(F, one, z1, z2, z3, z4):
    """(z4; z1,z2,z3) = (z4-z1)(z2-z3) / ((z4-z3)(z2-z1)), None for infinity."""
    num = F.mul(F.sub(z4, z1), F.sub(z2, z3))
    den = F.mul(F.sub(z4, z3), F.sub(z2, z1))
    if F.is_zero(den):
        return None
    return F.mul(num, F.div(one, den))


def cr_class(F, one, x):
    """S4 orbit of the cross-ratio value (the PGL-orbit invariant of a 4-set)."""
    if x is None:
        return "inf"
    vals = set()
    one_m = F.sub(one, one)            # 0
    for _ in range(2):                 # closure is small; iterate a few times
        new = set()
        for v in (vals or {x}):
            if v is None:
                new.add("inf")
                continue
            inv = None if F.is_zero(v) else F.div(one, v)
            new.add(v)
            new.add(inv)
            new.add(F.sub(one, v))
            if not F.is_zero(F.sub(one, v)):
                new.add(F.div(one, F.sub(one, v)))
            if not F.is_zero(F.sub(v, one)):
                new.add(F.div(v, F.sub(v, one)))
            if not F.is_zero(v):
                new.add(F.div(F.sub(v, one), v))
        vals |= {v for v in new if v != "inf"} | ({"inf"} if "inf" in new else set())
    return frozenset(vals)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--masks", type=Path, default=None)
    args = ap.parse_args()
    q = args.q

    F, sub = build_field(q)
    elems = list(F.elements())
    one = F.pow(elems[0], 0)
    points, blocks = build_circles(q, check_orbit_size=True)
    idx = {p: i for i, p in enumerate(points)}
    t = [elems[0], elems[1], elems[2]]          # points 0,1,2
    assert points[0] == t[0] and points[1] == t[1] and points[2] == t[2]

    # the six setwise stabiliser elements of {0,1,2}
    perms = list(itertools.permutations(range(3)))
    maps = [mobius_from_triples(F, t, [t[p] for p in perm]) for perm in perms]
    # sanity: each map permutes the triple
    for f, perm in zip(maps, perms):
        img = [f(t[i]) for i in range(3)]
        assert sorted(img, key=lambda z: idx[z]) == sorted([t[p] for p in perm], key=lambda z: idx[z]), \
            f"map for {perm} does not permute the triple"

    # extensions: points p with {0,1,2,p} safe, i.e. p not on the circle through 0,1,2
    triple_blocks = [bi for bi, B in enumerate(blocks) if set(range(3)) <= set(B)]
    assert len(triple_blocks) == 1, "the triple should lie on exactly one circle"
    on_circle = set(blocks[triple_blocks[0]])
    extensions = [i for i in range(len(points)) if i not in on_circle]
    assert len(extensions) == q * q - q, (len(extensions), q * q - q)
    print(f"q={q}: triple circle has {len(on_circle)} points; extensions = {len(extensions)}")

    # orbits under the stabiliser
    seen = set()
    orbits = []
    for p in extensions:
        if p in seen:
            continue
        orb = set()
        stack = [p]
        while stack:
            x = stack.pop()
            if x in orb:
                continue
            orb.add(x)
            z = points[x]
            for f in maps:
                w = f(z)
                if w is None:
                    continue
                y = idx[w]
                if y not in orb:
                    stack.append(y)
        seen |= orb
        orbits.append(sorted(orb))
    orbits.sort(key=lambda o: (-len(o), o[0]))
    print(f"q={q}: {len(orbits)} orbits, sizes {[len(o) for o in orbits]}")

    # cross-ratio classes
    class_of = {}
    for p in extensions:
        z = points[p]
        cr = cross_ratio(F, one, z, t[0], t[1], t[2])
        class_of[p] = cr_class(F, one, cr)
    classes = {}
    for p in extensions:
        classes.setdefault(class_of[p], []).append(p)
    print(f"q={q}: {len(classes)} cross-ratio classes, sizes "
          f"{sorted((len(v) for v in classes.values()), reverse=True)}")

    report = {
        "q": q,
        "extensions": len(extensions),
        "orbits": [{"size": len(o), "members": o} for o in orbits],
        "class_sizes": sorted((len(v) for v in classes.values()), reverse=True),
        "class_members": [[len(v), v[:8]] for v in classes.values()],
    }
    if args.out:
        import json
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"wrote {args.out}")
    if args.masks:
        with args.masks.open("w", encoding="utf-8") as fh:
            fh.write(f"{len(extensions)}\n")
            for p in sorted(extensions):
                fh.write(f"{(1 << 0) | (1 << 1) | (1 << 2) | (1 << p)}\n")
        print(f"wrote {args.masks} ({len(extensions)} masks)")


if __name__ == "__main__":
    main()
