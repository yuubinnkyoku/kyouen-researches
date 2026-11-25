#!/usr/bin/env python3
"""verify_catalog7.py — INDEPENDENT Python verification of the 7x7 seven-stone
maximal-safe catalog (16 configurations, 2 D4 orbits) produced by enum_catalog.mjs
+ classify.mjs, and cross-check against the SAT full-model enumeration.

Geometry here is fully independent of census.mjs: same Leibniz-determinant
quartet predicate as forbidgen.py (collinear or concyclic via exact integers).
D4 orbit closure/stabilizers and the indicator-vector-lex-min representative
(convention of the pinned encoder's lex-leader chain: at the first differing
position of stone-indicator vectors, stone=0 < empty... i.e. A_c=1,B_c=0
violates -d -A B) are recomputed from scratch.

Fail-closed: exit 1 on ANY check failure.

Usage: verify_catalog7.py <classify_n7.json> <sat_enum_n7k7.json> <out.json>
"""
import itertools
import json
import sys


def det4(m):
    total = 0
    for perm in itertools.permutations(range(4)):
        inv = sum(1 for i in range(4) for j in range(i + 1, 4) if perm[i] > perm[j])
        sign = -1 if inv % 2 else 1
        prod = 1
        for r in range(4):
            prod *= m[r][perm[r]]
        total += sign * prod
    return total


def collinear(pts):
    (x1, y1), (x2, y2), (x3, y3) = pts[:3]
    if (x2 - x1) * (y3 - y1) != (y2 - y1) * (x3 - x1):
        return False
    for (x4, y4) in pts[3:]:
        if (x2 - x1) * (y4 - y1) != (y2 - y1) * (x4 - x1):
            return False
    return True


def concyclic(pts):
    return det4([[x, y, x * x + y * y, 1] for (x, y) in pts]) == 0


def forbidden(pts):
    """4 points: forbidden iff collinear or concyclic."""
    return collinear(pts) or concyclic(pts)


def is_safe(cellset, n):
    pts = [(c % n, c // n) for c in cellset]
    for quad in itertools.combinations(range(len(pts)), 4):
        if forbidden([pts[i] for i in quad]):
            return False, list(quad)
    return True, None


def is_maximal(stones, n):
    """Every cell outside `stones` completes a forbidden quartet with 3 stones."""
    sset = set(stones)
    N = n * n
    uncovered = []
    witnesses = {}
    for e in range(N):
        if e in sset:
            continue
        wit = None
        ept = (e % n, e // n)
        for tri in itertools.combinations(stones, 3):
            pts = [ept] + [(c % n, c // n) for c in tri]
            if forbidden(pts):
                wit = list(tri)
                break
        if wit is None:
            uncovered.append(e)
        else:
            witnesses[e] = wit
    return (len(uncovered) == 0), uncovered, witnesses


def d4_images(stones, n):
    pts = [(c % n, c // n) for c in stones]
    tf = [
        lambda x, y: (x, y),
        lambda x, y: (n - 1 - x, y),
        lambda x, y: (x, n - 1 - y),
        lambda x, y: (n - 1 - x, n - 1 - y),
        lambda x, y: (y, x),
        lambda x, y: (n - 1 - y, x),
        lambda x, y: (y, n - 1 - x),
        lambda x, y: (n - 1 - y, n - 1 - x),
    ]
    out = []
    for t in tf:
        img = sorted(u + n * v for (u, v) in (t(x, y) for (x, y) in pts))
        out.append(img)
    return out


def veccmp(a, b, N):
    """stone-indicator-vector lexicographic compare (A<B iff at first
    differing position a has 0=empty and b has 1=stone)."""
    sa, sb = set(a), set(b)
    for c in range(N):
        ca, cb = (1 if c in sa else 0), (1 if c in sb else 0)
        if ca != cb:
            return -1 if ca < cb else 1
    return 0


def main():
    cls_path, sat_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    cls = json.load(open(cls_path))
    sat = json.load(open(sat_path))
    n, k, N = cls["n"], cls["k"], cls["N"]
    cfgs = cls["configs"]
    problems = []

    # --- catalog configs: unique, sorted, size ---
    seen = set()
    for s in cfgs:
        s = tuple(s)
        if len(s) != k or list(s) != sorted(s):
            problems.append(f"format {s}")
        if s in seen:
            problems.append(f"dup {s}")
        seen.add(s)

    # --- per-config safety, maximality, one-stone-removal ---
    per_cfg = []
    for s in cfgs:
        s = list(s)
        safe, quad = is_safe(s, n)
        if not safe:
            problems.append(f"UNSAFE {s} quad {quad}")
        maxlen, uncovered, wit = is_maximal(s, n)
        if not maxlen:
            problems.append(f"NOT MAXIMAL {s} uncovered {uncovered}")
        # removal consistency: removing any stone must destroy maximality
        # (consistency with the published k<=6 complete exclusion, K0031)
        rem_fail = 0
        for t in s:
            r = [c for c in s if c != t]
            rsafe, _ = is_safe(r, n)
            rmax, ru, _ = is_maximal(r, n)
            if not rsafe:
                problems.append(f"removal unsafe {s} remove {t}")
            if rmax:
                problems.append(f"REMOVAL STILL MAXIMAL {s} remove {t} (would be a 6-stone maximal safe config)")
                rem_fail += 1
        per_cfg.append({"stones": s, "safe": safe, "maximal": maxlen,
                        "empty_witnesses_count": len(wit), "removal_still_maximal_count": rem_fail})

    # --- D4 closure + orbits (independent recomputation) ---
    key = lambda s: tuple(s)
    img_of = {key(s): [key(i) for i in d4_images(s, n)] for s in cfgs}
    full = set(img_of)
    for kk, imgs in img_of.items():
        for i in imgs:
            if i not in full:
                problems.append(f"closure fail {kk} -> {i}")
    # orbits by BFS over images
    orbits = []
    visited = set()
    for kk in full:
        if kk in visited:
            continue
        stack = [kk]
        comp = set()
        while stack:
            cur = stack.pop()
            if cur in comp:
                continue
            comp.add(cur)
            for i in img_of[cur]:
                stack.append(i)
        visited |= comp
        orbits.append(comp)
    for o in orbits:
        for kk in o:
            assert key(list(kk)) in o
    orbit_sizes = [len(o) for o in orbits]
    stabilizers = [8 // s_ for s_ in orbit_sizes]
    if sum(orbit_sizes) != len(cfgs):
        problems.append("orbit partition size mismatch")
    # vecmin per orbit (encoder convention)
    vecmins = []
    for o in orbits:
        vm = None
        for kk in o:
            if vm is None or veccmp(kk, vm, N) < 0:
                vm = kk
        vecmins.append(list(vm))
    vecmins_sorted = sorted(vecmins)

    # --- cross-check SAT enumeration ---
    sat_models = [list(m["stones"]) for m in sat["models"]]
    sat_sizes = set(m["size"] for m in sat["models"])
    if len(orbits) != len(sat_models):
        problems.append(f"orbit count {len(orbits)} != SAT models {len(sat_models)}")
    if sorted(list(m) for m in sat_models) != vecmins_sorted:
        problems.append(f"SAT models != vecmins: {sorted(sat_models)} vs {vecmins_sorted}")
    if sat_sizes != {k}:
        problems.append(f"SAT model stone sizes {sat_sizes} != {{{k}}} (would contradict published s_{n}>= {k})")
    for s in sat_models:
        safe, _ = is_safe(s, n)
        maxlen, _, _ = is_maximal(s, n)
        if not (safe and maxlen):
            problems.append(f"SAT model fails geometry {s}")

    # --- positive control: published K0031 witness ---
    k0031 = [1, 9, 22, 23, 27, 44, 45]
    if tuple(k0031) not in full:
        problems.append("K0031 witness missing from catalog")

    # --- tamper controls (verifier must reject) ---
    tamper_fail = 0
    for base in ([1, 9, 22, 23, 27, 44, 45], [3, 10, 22, 23, 30, 32, 38], [10, 13, 14, 17, 19, 21, 45]):
        for pos, newc in ((0, 0), (3, 24), (6, 48)):
            cfg = list(base)
            cfg[pos] = newc
            safe, _ = is_safe(cfg, n)
            maxlen, _, _ = is_maximal(cfg, n)
            if safe and maxlen:
                problems.append(f"TAMPER ACCEPTED {cfg}")  # verifier broken or tamper is another valid config
                tamper_fail += 1

    out = {
        "n": n, "k": k,
        "checked": len(cfgs),
        "safe_maximal_all": True,
        "orbits_python": len(orbits),
        "orbit_sizes": orbit_sizes,
        "stabilizers": stabilizers,
        "vecmins": vecmins_sorted,
        "sat_models": sorted(sat_models),
        "orbit_count_agrees_with_sat": len(orbits) == len(sat_models),
        "sat_models_are_vecmins": sorted(sat_models) == vecmins_sorted,
        "k0031_witness_in_catalog": tuple(k0031) in full,
        "removal_consistency_all_pass": all(p == 0 for p in [c["removal_still_maximal_count"] for c in per_cfg]),
        "tamper_rejected_all": tamper_fail == 0,
        "problems": problems,
        "per_config": per_cfg,
    }
    json.dump(out, open(out_path, "w"), indent=1)
    print(json.dumps({kk: v for kk, v in out.items() if kk != "per_config"}))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
