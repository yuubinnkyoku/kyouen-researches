"""THE 3-NET REFORMULATION of the inversive-plane kyouen game.

VERIFIED KEY FACT (see CROSSRATIO_ROUTE.md).  Four points of
P^1(F_{q^2}) are concyclic iff their projective cross-ratio lies in
P^1(F_q).  Verified exhaustively for q = 3,4,5,7 (0 mismatches out of
210 / 2380 / 14950 / 230300 quadruples).

NORMALISATION.  PGL(2,F_{q^2}) is 3-transitive and preserves circles, so a
safe set S with |S| >= 3 can be sent to

    S = {0, 1, infinity}  union  T,     T subset of F_{q^2} \\ F_q.

The 4-subsets of S split into three families:

  (A) {0,1,inf,z}          -- concyclic iff z in F_q, excluded by T's range.
  (B) {a,b,z,z'} with a,b in {0,1,inf}, z,z' in T   -- PAIRWISE in T.
  (C) {a,z,z',z''} with a in {0,1,inf}, z,z',z'' in T -- 3-UNIFORM in T.

Family (B) gives three partitions of F_{q^2} \\ F_q, each into q classes of
size q-1:

    P_0 : classes = the F_q-lines through 0, minus F_q
    P_1 : classes = the F_q-lines through 1, minus F_q
    P_inf : classes = phi^{-1}(F_q-lines through 0), phi(z) = z/(1-z)

A set T meeting every class of every partition in at most one point is a
PARTIAL TRANSVERSAL of the 3-net (P_0, P_1, P_inf) -- equivalently a set of
mutually non-attacking rooks in a 3-dimensional board, or a partial Latin
square.  So:

    K(inversive q) <= 3 + tau_3(q),

where tau_3(q) is the maximum partial transversal of that 3-net.

This script:
  1. builds the three partitions and verifies they are partitions into
     q classes of size q-1;
  2. computes tau_3(q) exactly (max partial transversal);
  3. computes the FULL hypergraph independence number (families B and C)
     and checks it equals K - 3.

Run:  python net3_transversal.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field  # noqa: E402


# ------------------------------------------------------------------ partitions


def build_partitions(q: int):
    """Three partitions of F_{q^2} \\ F_q into q classes of size q-1."""
    F, sub = build_field(q)
    subset = set(sub)
    verts = [x for x in F.elements() if x not in subset]
    n = len(verts)
    assert n == q * q - q

    def classes_through(a):
        """Partition by 'same F_q-line through a', restricted off F_q."""
        cls = {}
        for z in verts:
            d = F.sub(z, a)
            # normalise the F_q-line: pick a canonical representative
            key = None
            for c in sub:
                if F.is_zero(c):
                    continue
                cand = F.div(d, c)
                if key is None or repr(cand) < repr(key):
                    key = cand
            cls.setdefault(repr(key), []).append(z)
        return cls

    def classes_phi():
        """phi(z) = z/(1-z); partition by F_q-line through 0 of phi(z)."""
        cls = {}
        for z in verts:
            d = F.sub(F.one, z)
            phi = F.div(z, d) if not F.is_zero(d) else None
            if phi is None:
                cls.setdefault("inf", []).append(z)
                continue
            key = None
            for c in sub:
                if F.is_zero(c):
                    continue
                cand = F.div(phi, c)
                if key is None or repr(cand) < repr(key):
                    key = cand
            cls.setdefault(repr(key), []).append(z)
        return cls

    P0 = classes_through(F.zero)
    P1 = classes_through(F.one)
    Pinf = classes_phi()
    return F, sub, verts, [P0, P1, Pinf]


def check_partitions(q, verts, parts) -> dict:
    n = len(verts)
    info = []
    ok = True
    for P in parts:
        sizes = sorted(len(v) for v in P.values())
        covered = sum(sizes)
        disjoint = covered == n
        info.append({"classes": len(P), "sizes": sizes,
                     "covers_all": disjoint})
        if len(P) != q or sizes != [q - 1] * q or not disjoint:
            ok = False
    return {"q": q, "vertices": n, "partitions": info, "is_3net": ok}


# ------------------------------------------------------------------ max transversal


def max_transversal(verts, parts, node_cap: int = 50_000_000):
    """Max T meeting every class of every partition in <= 1 point."""
    n = len(verts)
    pos = {repr(z): i for i, z in enumerate(verts)}
    cls_of = []          # cls_of[part][vertex] = class id
    for P in parts:
        keys = sorted(P)
        kid = {k: i for i, k in enumerate(keys)}
        arr = [0] * n
        for k in keys:
            for z in P[k]:
                arr[pos[repr(z)]] = kid[k]
        cls_of.append(arr)

    used = [[False] * len(P) for P in parts]
    chosen: list[int] = []
    best: list[list[int]] = [[]]
    state = {"nodes": 0}

    def rec(start: int) -> None:
        state["nodes"] += 1
        if state["nodes"] > node_cap:
            raise RuntimeError("node cap exceeded")
        if len(chosen) > len(best[0]):
            best[0] = chosen.copy()
        if len(chosen) + (n - start) <= len(best[0]):
            return
        for v in range(start, n):
            ok = True
            for pi in range(len(parts)):
                if used[pi][cls_of[pi][v]]:
                    ok = False
                    break
            if not ok:
                continue
            for pi in range(len(parts)):
                used[pi][cls_of[pi][v]] = True
            chosen.append(v)
            rec(v + 1)
            chosen.pop()
            for pi in range(len(parts)):
                used[pi][cls_of[pi][v]] = False

    rec(0)
    return best[0], state["nodes"]


# ------------------------------------------------------------------ full hypergraph


def max_safe_normalised(F, sub, verts, node_cap: int = 50_000_000):
    """Max T with {0,1,inf} union T safe, checked by the cross-ratio directly."""
    from crossratio_graph import concyclic

    zero, one, inf = F.zero, F.one, None
    n = len(verts)
    chosen: list[int] = []
    best: list[list[int]] = [[]]
    state = {"nodes": 0}

    def ok_add(v):
        z = verts[v]
        # family B: pairs with existing T
        for u in chosen:
            w = verts[u]
            if (concyclic(F, sub, (zero, one, z, w))
                    or concyclic(F, sub, (zero, inf, z, w))
                    or concyclic(F, sub, (one, inf, z, w))):
                return False
        # family C: triples with existing T, one anchor from {0,1,inf}
        for u, w2 in itertools.combinations(chosen, 2):
            a, b = verts[u], verts[w2]
            if (concyclic(F, sub, (zero, z, a, b))
                    or concyclic(F, sub, (one, z, a, b))
                    or concyclic(F, sub, (inf, z, a, b))):
                return False
        # family D: quadruples entirely inside T
        for u, w2, w3 in itertools.combinations(chosen, 3):
            if concyclic(F, sub, (z, verts[u], verts[w2], verts[w3])):
                return False
        return True

    def rec(start: int) -> None:
        state["nodes"] += 1
        if state["nodes"] > node_cap:
            raise RuntimeError("node cap exceeded")
        if len(chosen) > len(best[0]):
            best[0] = chosen.copy()
        if len(chosen) + (n - start) <= len(best[0]):
            return
        for v in range(start, n):
            if not ok_add(v):
                continue
            chosen.append(v)
            rec(v + 1)
            chosen.pop()

    rec(0)
    return best[0], state["nodes"]


# ------------------------------------------------------------------ main


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7])
    ap.add_argument("--node-cap", type=int, default=50_000_000)
    args = ap.parse_args()

    INV_K = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7, 9: 9, 11: 9, 13: 8}

    rows = []
    print("=== step 1: the three partitions form a 3-net ===")
    for q in args.q:
        F, sub, verts, parts = build_partitions(q)
        r = check_partitions(q, verts, parts)
        rows.append({"check": "3net", **r})
        print(f"  q={q}: {r['vertices']} vertices, "
              f"classes per partition {[p['classes'] for p in r['partitions']]}, "
              f"sizes {r['partitions'][0]['sizes']} -> "
              f"{'OK' if r['is_3net'] else 'FAIL'}", flush=True)

    print()
    print("=== step 2: tau_3 (transversal) vs full hypergraph vs K ===")
    print(f"{'q':>3} {'|V|':>5} {'tau_3':>6} {'3+tau':>6} {'full':>5} "
          f"{'3+full':>7} {'K':>4} {'match':>6}")
    for q in args.q:
        t0 = time.time()
        F, sub, verts, parts = build_partitions(q)
        try:
            tv, tn = max_transversal(verts, parts, node_cap=args.node_cap)
            tau = len(tv)
            err = None
        except RuntimeError as exc:
            tau, tv, tn, err = None, None, -1, str(exc)
        try:
            fv, fn = max_safe_normalised(F, sub, verts, node_cap=args.node_cap)
            full = len(fv)
        except RuntimeError as exc:
            full, fv, fn = None, None, -1
        dt = time.time() - t0
        K = INV_K.get(q)
        pred = 3 + full if full is not None else None
        match = (pred == K) if (K is not None and pred is not None) else None
        rows.append({
            "check": "counts", "q": q, "vertices": len(verts),
            "tau_3": tau, "K_from_transversal": 3 + tau if tau else None,
            "full_independence": full, "K_predicted": pred, "K_observed": K,
            "match": match, "transversal_witness": tv,
            "full_witness": fv, "seconds": round(dt, 2), "error": err,
        })
        print(f"{q:>3} {len(verts):>5} {tau!s:>6} "
              f"{(3+tau) if tau else '-':>6} {full!s:>5} {pred!s:>7} "
              f"{K!s:>4} {match!s:>6}  {dt:.1f}s"
              + (f"  ERROR {err}" if err else ""), flush=True)

    print()
    print("K(inversive q) = 3 + (max T with {0,1,inf} u T safe).")
    print("The pairwise part of the constraint is a 3-net partial transversal;")
    print("the 3-uniform part is genuinely extra, so the transversal bound")
    print("3 + tau_3 is an UPPER bound on K, not an equality in general.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
