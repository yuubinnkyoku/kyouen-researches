"""Two-dimensional subspaces over the *square-root* field: q = r^2, scalars F_r.

The scan in fp2_subspace_arcs.py used the prime field F_p.  For q = r^2 with
r > p (the first case is q = 16 = 4^2 over F_4) the natural analogue is to view
F_{q^2} = F_{r^4} as a 4-dimensional F_r-space and to test all 2-dimensional
F_r-subspaces: each has exactly r^2 = q elements and is therefore a q-point
subset of the inversive plane.  The number of them is the Gaussian binomial
[4 choose 2]_r = (r^2+1)(r^2+r+1) (357 for r=4).

If one of them is an arc then K(q) >= q, which at q=16 would improve the current
lower bound 12 to 16.

Run:  python subspace_arcs_sqrtfield.py --q 16 --base 4
"""

from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field  # noqa: E402
from inversive_fast import build_circles  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--base", type=int, required=True, help="r with q = r^2")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    q, r = args.q, args.base
    assert r * r == q, "base must satisfy base^2 = q"

    F, sub_q = build_field(q)               # F_{q^2}
    elems = list(F.elements())
    index = {e: i for i, e in enumerate(elems)}
    one = F.pow(elems[0], 0)
    zero = F.sub(one, one)
    points, blocks = build_circles(q, check_orbit_size=True)
    assert len(points) == q * q + 1
    cmasks = []
    for B in blocks:
        mask = 0
        for pt in B:
            mask |= 1 << pt
        cmasks.append(mask)

    # the subfield F_r = {x : x^r = x}
    base_field = [x for x in elems if F.pow(x, r) == x]
    assert len(base_field) == r, (len(base_field), r)

    vectors = [v for v in elems if v != zero]
    seen = set()
    arcs = []
    count = 0
    for v, w in itertools.combinations(vectors, 2):
        span = set()
        for a in base_field:
            for b in base_field:
                span.add(F.add(F.mul(a, v), F.mul(b, w)))
        if len(span) != r * r:
            continue
        key = frozenset(span)
        if key in seen:
            continue
        seen.add(key)
        count += 1
        mask = 0
        for e in span:
            mask |= 1 << index[e]
        if all(bin(mask & m).count("1") < 4 for m in cmasks):
            arcs.append(sorted(index[e] for e in span))
    print(f"q={q} (r={r}): {count} two-dimensional F_r-subspaces, "
          f"{len(arcs)} of them are arcs of size {q}", flush=True)
    if args.out:
        import json
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({"q": q, "base": r, "subspaces": count,
                                        "arcs": len(arcs), "examples": arcs[:3]},
                                       indent=2), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
