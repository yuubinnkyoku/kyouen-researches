"""Measure M_4(q), the maximum length of a 4-dimensional MDS code over F_q.

M_4(q) is the maximum size of a set of points of PG(3,q) in general position
(no four coplanar).  By K1250 the inversive-plane K(q) is the same quantity
with the extra requirement that the points lie on the elliptic quadric
Q^-(3,q), so comparing the two measures what the quadric costs.

For a set in general position a point p may be added iff no plane through p
contains three points of the set, so the planes of PG(3,q) are the "blocks" and
arc_maxsearch.c applies unchanged.  Every reported set is then verified by
linear algebra: all four-subsets must have nonzero determinant.

Run:  python mds_maxlength.py --q 3 4 5 7 8 9 11 13 --trials 100 --ils 3000
"""

from __future__ import annotations

import argparse
import itertools
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_prime_power import (  # noqa: E402
    FiniteField, factorize, find_irreducible, is_prime,
)
from pg3_planes import build_prime, build_prime_power, write_blocks  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "output"
EXE = HERE / "arc_maxsearch.exe"
BEST_RE = re.compile(r"^BEST\s+(\d+)((?:\s+\d+)*)\s*$")


def verifier(q: int):
    """Return a function verifying that indices give points in general position."""
    if is_prime(q):
        pts, _ = build_prime(q)
        def ok(arc):
            for quad in itertools.combinations(arc, 4):
                rows = [pts[i] for i in quad]
                # 4x4 determinant over Z/q
                m = [list(r) for r in rows]
                for col in range(4):
                    piv = next((r for r in range(col, 4) if m[r][col] % q), None)
                    if piv is None:
                        return False, quad
                    m[col], m[piv] = m[piv], m[col]
                    inv = pow(m[col][col], -1, q)
                    m[col] = [(inv * x) % q for x in m[col]]
                    for r in range(col + 1, 4):
                        f = m[r][col]
                        if f % q:
                            m[r] = [(m[r][c] - f * m[col][c]) % q for c in range(4)]
            return True, None
        return ok, pts

    p, e = factorize(q)[0]
    F = FiniteField(p, e, find_irreducible(p, e))
    one = F.pow(F.elements()[0], 0)
    pts, _ = build_prime_power(q)

    def ok(arc):
        for quad in itertools.combinations(arc, 4):
            m = [list(pts[i]) for i in quad]
            for col in range(4):
                piv = next((r for r in range(col, 4) if not F.is_zero(m[r][col])), None)
                if piv is None:
                    return False, quad
                m[col], m[piv] = m[piv], m[col]
                inv = F.div(one, m[col][col])
                m[col] = [F.mul(inv, x) for x in m[col]]
                for r in range(col + 1, 4):
                    f = m[r][col]
                    if not F.is_zero(f):
                        m[r] = [F.sub(m[r][c], F.mul(f, m[col][c])) for c in range(4)]
        return True, None
    return ok, pts


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    ap.add_argument("--trials", type=int, default=100)
    ap.add_argument("--ils", type=int, default=3000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        pts, planes = (build_prime(q) if is_prime(q) else build_prime_power(q))
        path = OUT / f"pg3q{q}.txt"
        write_blocks(path, len(pts), planes)
        proc = subprocess.run([str(EXE), str(path), "--trials", str(args.trials),
                               "--ils", str(args.ils)], capture_output=True, text=True,
                              timeout=3600)
        m = BEST_RE.match(proc.stdout.splitlines()[1])
        if not m:
            print(f"q={q}: unparsable output", flush=True)
            rows.append({"q": q, "error": proc.stdout[:200] + proc.stderr[:200]})
            continue
        size = int(m.group(1))
        arc = [int(x) for x in m.group(2).split()] if m.group(2).strip() else []
        check, _points = verifier(q)
        ok, why = check(arc)
        rows.append({"q": q, "n": len(pts), "M4_lower": size, "verified": ok,
                     "bad_quadruple": why, "witness": arc,
                     "q_plus_1": q + 1})
        print(f"q={q:>2}: M_4 >= {size:>2} (q+1={q + 1:>2}) verified={ok}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        print(f"wrote {args.out}")
    if any(not r.get("verified") for r in rows):
        raise SystemExit("M_4 witness FAILED verification")


if __name__ == "__main__":
    main()
