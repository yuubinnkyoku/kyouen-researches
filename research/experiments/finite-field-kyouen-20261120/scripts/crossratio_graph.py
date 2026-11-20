"""THE CROSS-RATIO REFORMULATION: kyouen on the inversive plane is a
maximum-independent-set problem on an explicit graph.

SETUP.  The inversive plane of order q is

    points  = P^1(F_{q^2}) = F_{q^2} union {infinity}
    circles = { g(P^1(F_q)) : g in PGL(2, F_{q^2}) }

KEY FACT (classical).  Four points are concyclic iff the unique Mobius map
sending three of them to 0, 1, infinity sends the fourth into P^1(F_q).
Equivalently, the cross-ratio lies in P^1(F_q).

NORMALISATION.  PGL(2,F_{q^2}) is 3-transitive and preserves the circle
family, so any three points of a safe set S can be sent to 0, 1, infinity.
Write

    S = {0, 1, infinity}  union  T,     T subset of F_{q^2} \\ F_q.

Then S is safe iff every 4-subset is non-concyclic.  The 4-subsets are
{0,1,inf,z} (automatic once T avoids F_q) and, for distinct z,z' in T,

    {0,1,z,z'},  {0,inf,z,z'},  {1,inf,z,z'}.

So define a graph G_q on the vertex set F_{q^2} \\ F_q by

    z ~ z'   iff   one of those three quadruples is concyclic.

Then

    K(inversive q) = 3 + alpha(G_q),

where alpha is the independence number.  This turns the kyouen game into a
concrete graph problem on q^2 - q vertices.

Run:  python crossratio_graph.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field, build_inversive_plane, mobius  # noqa: E402


# ------------------------------------------------------------------ concyclicity


def to_homogeneous(F, z):
    """P^1 point as a homogeneous pair (u, v); z = u/v, None = infinity."""
    if z is None:
        return (F.one, F.zero)
    return (z, F.one)


def concyclic(F, subfield, quad) -> bool:
    """Are the four points of `quad` (elements of P^1(F_{q^2})) concyclic?

    Uses the PROJECTIVE cross-ratio, which handles infinity with no special
    cases.  For homogeneous points z_i = (u_i : v_i),

        [z_i, z_j] = u_i v_j - u_j v_i        (2x2 determinant)
        (z1,z2;z3,z4) = [z1,z3][z2,z4] / ([z1,z4][z2,z3])

    and the quadruple is concyclic iff this lies in P^1(F_q), i.e. iff the
    denominator vanishes (value = infinity) or the quotient is in F_q.
    """
    h = [to_homogeneous(F, z) for z in quad]

    def det(i, j):
        ui, vi = h[i]
        uj, vj = h[j]
        return F.sub(F.mul(ui, vj), F.mul(uj, vi))

    num = F.mul(det(0, 2), det(1, 3))
    den = F.mul(det(0, 3), det(1, 2))
    if F.is_zero(den):
        return True                # cross-ratio = infinity, in P^1(F_q)
    return F.div(num, den) in subfield


# ------------------------------------------------------------------ verify key fact


def verify_crossratio_key(q: int) -> dict:
    """Check: 4 points concyclic (by circle list) <=> cross-ratio in P^1(F_q)."""
    F, sub = build_field(q)
    points, circles = build_inversive_plane(q)
    idx = {p: i for i, p in enumerate(points)}
    circ_sets = [frozenset(idx[p] for p in c) for c in circles]

    pts = list(points)
    bad = 0
    checked = 0
    for quad in itertools.combinations(range(len(pts)), 4):
        z = [pts[i] for i in quad]
        truth = any(all(i in cs for i in quad) for cs in circ_sets)
        pred = concyclic(F, sub, z)
        checked += 1
        if truth != pred:
            bad += 1
            if bad <= 3:
                print(f"    MISMATCH q={q} quad={quad} truth={truth} "
                      f"pred={pred}", flush=True)
    return {"q": q, "quads_checked": checked, "mismatches": bad,
            "key_fact_holds": bad == 0}


# ------------------------------------------------------------------ build graph


def build_graph(q: int):
    """Vertices = F_{q^2} \\ F_q, edges = pairs completing a concyclic quad."""
    F, sub = build_field(q)
    subset = set(sub)
    verts = [x for x in F.elements() if x not in subset]
    n = len(verts)
    assert n == q * q - q, f"vertex count {n} != q^2-q = {q*q-q}"

    zero, one, inf = F.zero, F.one, None

    adj = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            a, b = verts[i], verts[j]
            if (concyclic(F, sub, (zero, one, a, b))
                    or concyclic(F, sub, (zero, inf, a, b))
                    or concyclic(F, sub, (one, inf, a, b))):
                adj[i].add(j)
                adj[j].add(i)
    return verts, adj


# ------------------------------------------------------------------ max independent set


def max_independent(adj, node_cap: int = 50_000_000):
    n = len(adj)
    best: list[list[int]] = [[]]
    cur: list[int] = []
    state = {"nodes": 0}

    def rec(cand: list[int]) -> None:
        state["nodes"] += 1
        if state["nodes"] > node_cap:
            raise RuntimeError("node cap exceeded")
        if len(cur) > len(best[0]):
            best[0] = cur.copy()
        if len(cur) + len(cand) <= len(best[0]):
            return
        order = sorted(cand, key=lambda v: -len(adj[v]))
        for k, v in enumerate(order):
            if len(cur) + len(cand) - k <= len(best[0]):
                return
            cur.append(v)
            rec([u for u in cand[k + 1:] if u not in adj[v]])
            cur.pop()

    rec(list(range(n)))
    return best[0], state["nodes"]


# ------------------------------------------------------------------ main


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7, 8, 9])
    ap.add_argument("--node-cap", type=int, default=50_000_000)
    ap.add_argument("--skip-key", action="store_true")
    args = ap.parse_args()

    INV_K = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7, 9: 9, 11: 9, 13: 8}

    rows = []
    if not args.skip_key:
        print("=== step 1: verify the cross-ratio key fact ===")
        for q in args.q:
            if q > 9:
                continue
            r = verify_crossratio_key(q)
            rows.append({"check": "crossratio_key", **r})
            print(f"  q={q}: {r['quads_checked']} quadruples, "
                  f"{r['mismatches']} mismatches -> "
                  f"{'OK' if r['key_fact_holds'] else 'FAIL'}", flush=True)
        print()

    print("=== step 2: K = 3 + alpha(G_q) ===")
    print(f"{'q':>3} {'|V|':>5} {'|E|':>7} {'alpha':>6} {'3+alpha':>8} "
          f"{'K(inv)':>7} {'match':>6}")
    for q in args.q:
        t0 = time.time()
        verts, adj = build_graph(q)
        n = len(verts)
        m = sum(len(a) for a in adj) // 2
        try:
            ind, nodes = max_independent(adj, node_cap=args.node_cap)
            alpha, err = len(ind), None
        except RuntimeError as exc:
            alpha, ind, nodes, err = None, None, -1, str(exc)
        dt = time.time() - t0
        K = INV_K.get(q)
        pred = 3 + alpha if alpha is not None else None
        match = (pred == K) if (K is not None and pred is not None) else None
        rows.append({
            "check": "graph", "q": q, "vertices": n, "edges": m,
            "alpha": alpha, "K_predicted": pred, "K_observed": K,
            "match": match, "witness": ind, "nodes": nodes,
            "seconds": round(dt, 2), "error": err,
        })
        print(f"{q:>3} {n:>5} {m:>7} {alpha!s:>6} {pred!s:>8} {K!s:>7} "
              f"{match!s:>6}  {dt:.1f}s"
              + (f"  ERROR {err}" if err else ""), flush=True)

    print()
    print("K(inversive q) = 3 + alpha(G_q),  G_q on q^2-q vertices.")
    print("The kyouen game on the inversive plane is a maximum independent")
    print("set problem in an explicit graph.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
