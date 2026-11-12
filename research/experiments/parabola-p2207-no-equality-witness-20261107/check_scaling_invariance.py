"""Is the parameter scaling t -> a*t a symmetry of parabola safety?

The counting argument for A(p) uses only the reflection t -> p-t, which is the
integer-plane reflection (x, y) -> (p-x, y) and hence an isometry (it preserves
circles and lines).  A tempting extra symmetry is multiplication of parameters
by a unit a, because four parabola parameters are *mod-p* concyclic exactly when
their sum is 0 mod p (K0334).  That is only a necessary condition for exact
integer concyclicity, and the real objects here are the integer points
(t, t^2 mod p).  This script measures the failure on the audited 1104-point
witness of Q_2207.

Concretely:
  * read the audited point list,
  * check it against the forbidden-edge list (must be 0),
  * multiply every parameter by 307^-1 mod 2207 (307 is the witness's complete
    pair, so the scaled set has complete pair {1, p-1}),
  * check the scaled set against the same edge list, and for every edge that it
    now contains recompute exact integer concyclicity with an independent
    generic 4x4 Leibniz determinant of the circle matrix
        (x^2 + y^2, x, y, 1)  for the four points.

Usage: check_scaling_invariance.py [--output PATH]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from probe_driver import run_gen  # noqa: E402

HERE = Path(__file__).resolve().parent
CANDIDATE = ROOT / "research/experiments/parabola-p2207-1104-witness-20261110/output/candidate.txt"
P = 2207
COMPLETE_PAIR = 307


def det4(m):
    """Exact integer determinant of a 4x4 matrix (Leibniz over permutations)."""
    import itertools

    total = 0
    for perm in itertools.permutations(range(4)):
        sign = 1
        for i in range(4):
            for j in range(i + 1, 4):
                if perm[i] > perm[j]:
                    sign = -sign
        term = sign
        for i in range(4):
            term *= m[i][perm[i]]
        total += term
    return total


def concyclic(q, p=P):
    """Generic integer test: rows (x^2+y^2, x, y, 1) for the points (t, t^2 mod p)."""
    rows = []
    for t in q:
        y = (t * t) % p
        rows.append([t * t + y * y, t, y, 1])
    return det4(rows) == 0


def classify(points, p=P):
    h = (p - 1) // 2
    S = set(points)
    x = 1 if 0 in S else 0
    complete = [t for t in range(1, h + 1) if t in S and p - t in S]
    empty = [t for t in range(1, h + 1) if t not in S and p - t not in S]
    return {"contains_origin": bool(x), "complete": complete, "empty": empty,
            "size": len(S), "x": x, "c": len(complete), "e": len(empty)}


def contained(points, edges):
    S = set(points)
    return [q for q in edges if set(q) <= S]


def check(points, edges, label):
    inside = contained(points, edges)
    zero = sum(1 for q in inside if concyclic(q))
    return {"label": label, "size": len(points), "class": classify(points),
            "edges_inside": len(inside),
            "edges_inside_concyclic": zero,
            "first_edges": inside[:5]}


def main() -> int:
    out = HERE / "output" / "scaling_invariance.json"
    if "--output" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--output") + 1])
    lines = CANDIDATE.read_text(encoding="ascii").split("\n")
    header = lines[0].split()
    if [int(x) for x in header] != [P, 1104]:
        raise SystemExit(f"unexpected candidate header: {header}")
    points = sorted(int(x) for x in " ".join(lines[1:]).split())
    if len(points) != 1104 or len(set(points)) != 1104:
        raise SystemExit("unexpected candidate size")
    edges = run_gen(str(Path(__import__("os").environ["TEMP"]) / "forbidden_edges.exe"), P)
    a = pow(COMPLETE_PAIR, -1, P)
    scaled = sorted((a * t) % P for t in points)
    record = {
        "p": P,
        "candidate": str(CANDIDATE.relative_to(ROOT)),
        "candidate_sha256": __import__("hashlib").sha256(
            CANDIDATE.read_bytes()).hexdigest(),
        "edges": len(edges),
        "scaling": a,
        "scaling_inverse_of": COMPLETE_PAIR,
        "raw": check(points, edges, "raw witness"),
        "scaled": check(scaled, edges, f"scaled by {COMPLETE_PAIR}^-1"),
        "sum_check": {
            "note": ("mod-p four-sums are plentiful and do not imply integer "
                     "concyclicity; the audit of this witness already recorded "
                     "27941252 mod-p filtered candidates with nonzero determinant"),
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(record, indent=2, ensure_ascii=False) + "\n"
    out.write_text(text, encoding="utf-8", newline="\n")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
