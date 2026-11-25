"""Curve-based SAT encoding for a bounded-size maximal safe set on n x n.

A rich curve is a line or circle containing at least four grid points.
Safety: at most 3 points of S on any rich curve.
Maximality: every grid point p outside S lies on a rich curve with exactly
3 points of S (then S + p would contain 4 points on that curve).

Encoded with a blocking variable z_C per rich curve:
  z_C -> at least 3 points of C are in S   (pair clauses)
  coverage: p in S or some z_C with p on C
  safety: for each rich curve, every 4-subset of its grid points gets a
  no-all clause (same clauses as the forbidden quadruple family).
Optional --lex adds S <=lex r(S) and S <=lex s(S) over point order y*n+x,
which is sound because each orbit's lex-minimum element satisfies both.
"""
import argparse
import hashlib
import sys
import time
from pathlib import Path

REPO = Path(r"D:\ghq\github.com\yuubinnkyoku\kyouen-researches")
sys.path.insert(0, str(REPO / "research/experiments/original-claims/scripts"))
sys.path.insert(0, str(Path(r"C:\Users\yuubi\AppData\Local\Temp\opencode\pysat-env")))

from round25_forced_verify import geometry, bits  # noqa: E402


def add_lex_leader(clauses, top, perm, m):
    """Enforce S <=lex perm(S) over point order 0..m-1 (index y*n+x)."""
    e = [None] * (m + 1)
    e[0] = top + 1
    top += 1
    clauses.append([e[0]])
    for i in range(m):
        x, y = i + 1, perm[i] + 1
        clauses.append([-e[i], -x, y])
        if i + 1 < m:
            e[i + 1] = top + 1
            top += 1
            clauses.append([-e[i + 1], e[i]])
            clauses.append([-e[i + 1], -x, y])
            clauses.append([-e[i + 1], x, -y])
            clauses.append([-e[i], -x, -y, e[i + 1]])
            clauses.append([-e[i], x, y, e[i + 1]])
    return top


def build(n, bound, exact, wedge, lex):
    points, quads, curve_masks = geometry(n)
    V = n * n
    clauses = []
    top = V
    z = {}
    for mask in sorted(curve_masks):
        top += 1
        z[mask] = top
    for mask in sorted(curve_masks):
        idx = sorted(bits(mask))
        zc = z[mask]
        for i in range(len(idx)):
            for j in range(i + 1, len(idx)):
                rest = [idx[k] for k in range(len(idx)) if k != i and k != j]
                clauses.append([-zc] + [p + 1 for p in rest])
    covering = [[] for _ in range(V)]
    for mask in sorted(curve_masks):
        for p in bits(mask):
            covering[p].append(z[mask])
    for p in range(V):
        clauses.append([p + 1] + covering[p])
    for q in quads:
        clauses.append([-(p + 1) for p in bits(q)])
    if lex:
        # full-group canonicalization: the lex-minimum element of each orbit
        # satisfies S <=lex g(S) for every g in D4 simultaneously.
        def r1(x, y):
            return (y, n - 1 - x)

        def s0(x, y):
            return (n - 1 - x, y)

        cur = list(points)
        perms = []
        for _ in range(3):
            cur = [r1(x, y) for x, y in cur]
            perms.append([y * n + x for x, y in cur])
        cur = [s0(x, y) for x, y in points]
        for _ in range(4):
            perms.append([y * n + x for x, y in cur])
            cur = [r1(x, y) for x, y in cur]
        seen = set()
        for perm in perms:
            t = tuple(perm)
            if t in seen:
                continue
            seen.add(t)
            top = add_lex_leader(clauses, top, perm, V)
    return points, quads, curve_masks, clauses, top, V


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--bound", type=int, default=9)
    ap.add_argument("--exact", action="store_true")
    ap.add_argument("--wedge", action="store_true")
    ap.add_argument("--lex", action="store_true")
    args = ap.parse_args()
    if args.wedge and args.lex:
        raise SystemExit("wedge and lex must not be combined: orbit-minima "
                         "need not contain an orbit representative")
    started = time.monotonic()
    points, quads, curves, clauses, top, V = build(
        args.n, args.bound, args.exact, args.wedge, args.lex)
    from pysat.card import CardEnc, EncType  # noqa: E402
    lits = list(range(1, V + 1))
    if args.exact:
        card = CardEnc.equals(lits=lits, bound=args.bound, top_id=top,
                              encoding=EncType.seqcounter)
    else:
        card = CardEnc.atmost(lits=lits, bound=args.bound, top_id=top,
                              encoding=EncType.seqcounter)
    clauses.extend(card.clauses)
    nv = card.nv
    n = args.n
    if args.wedge:
        reps = set()
        for x in range(n):
            for y in range(n):
                orbit = {(x, y)}
                frontier = [(x, y)]
                while frontier:
                    a, b = frontier.pop()
                    for u, v in [(b, n - 1 - a), (n - 1 - a, b)]:
                        if (u, v) not in orbit:
                            orbit.add((u, v))
                            frontier.append((u, v))
                reps.add(min(orbit, key=lambda t: t[1] * n + t[0]))
        clauses.append([x * n + y + 1 for x, y in sorted(reps)])
    outdir = Path(r"C:\Users\yuubi\AppData\Local\Temp\opencode\kyouen-n10-nine")
    tag = (f"curve_n{n}_{'eq' if args.exact else 'le'}{args.bound}"
           f"{'_w' if args.wedge else ''}{'_lex' if args.lex else ''}")
    cnf = outdir / f"{tag}.cnf"
    with cnf.open("w", encoding="ascii", newline="\n") as f:
        f.write(f"p cnf {nv} {len(clauses)}\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")
    print(f"tag={tag} vars={nv} clauses={len(clauses)} curves={len(curves)} "
          f"quads={len(quads)} "
          f"sha={hashlib.sha256(cnf.read_bytes()).hexdigest()}", flush=True)
    print(f"build_seconds={round(time.monotonic()-started,1)}", flush=True)


if __name__ == "__main__":
    main()
