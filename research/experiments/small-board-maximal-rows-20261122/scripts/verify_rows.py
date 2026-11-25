#!/usr/bin/env python3
"""verify_rows.py — INDEPENDENT Python verification of complete maximal-safe
row catalogs (all k-stone maximal safe configurations on the n x n standard
kyouen board, q = 4), produced by enum_catalog.mjs.

Geometry is fully independent of census.mjs: the quartet catalog is read from
a forbidgen-written canonical text file (system B: Leibniz 4x4 determinant +
cross-product collinearity over ALL C(n^2,4) subsets — see forbidgen_write.py).
The verification engine is a fresh implementation using a triple->completions
map, different from the DFS's incremental cov bookkeeping:

  comp_map[T] = list of cells e such that {e} union T is a forbidden quartet.

  SAFE(S)    iff no stone triple T of S has a completion inside S.
  MAXIMAL(S) iff every cell outside S is a completion of some stone triple
              of S (i.e. is "covered").

Fail-closed: exit 1 on ANY failure.

Also recomputed independently (all fail-closed):
  - D4 closure of each row, orbit count, stabilizer histogram (orbit sum gate).
  - three-collinear triple count / distinct-direction count per configuration
    (fresh collinearity over stone triples) + row histograms.
  - adjacent-row inclusion ("removal") statistics: for each configuration S of
    row k, remov = #{s in S : S \\ {s} belongs to the row-(k-1) catalog}.
    Both directions aggregated (edge count, per-parent superset histogram).
  - controls: deterministic unsafe tamper (add a covered cell to a row config)
    must be judged UNSAFE; when the row-(k-1) catalog is available, a
    deterministic non-maximal tamper (remove a stone whose removal is not a
    row-(k-1) member) must be judged NOT MAXIMAL.

Usage:
  python3 verify_rows.py <n> <quartets.txt> <outdir_prefix> <k:jsonl> [<k:jsonl>...]
     rows must be given in ascending k; each row's jsonl path follows "k:path".
Output: <outdir_prefix>_rows.json (machine record) + stdout summary.
"""
import hashlib
import itertools
import json
import sys
from math import gcd

N_COLL = 0


def load_row(path):
    cfgs = []
    found = None
    nodes = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r.get("type") == "cfg":
                cfgs.append(tuple(r["stones"]))
            elif r.get("type") == "summary":
                found = r["found"]
                nodes = r["nodes"]
    return cfgs, found, nodes


def bitmask(cells):
    m = 0
    for c in cells:
        m |= 1 << c
    return m


def main():
    n = int(sys.argv[1])
    qpath = sys.argv[2]
    outprefix = sys.argv[3]
    row_specs = []
    for arg in sys.argv[4:]:
        kpart, p = arg.split(":", 1)
        row_specs.append((int(kpart), p))

    N = n * n
    # --- quartet catalog (system B) ---
    quarts = []
    with open(qpath, "r", encoding="utf-8") as f:
        first = f.readline().strip()
        assert first == "n=%d" % n, "quartet file board mismatch: %r" % first
        for line in f:
            line = line.strip()
            if line:
                quarts.append(tuple(int(x) for x in line.split()))
    qsha = hashlib.sha256(open(qpath, "rb").read().replace(b"\r\n", b"\n")).hexdigest()
    quarts.sort()

    # triple -> completions map
    comp_map = {}
    for q in quarts:
        for i in range(4):
            e = q[i]
            tri = tuple(sorted(q[:i] + q[i + 1:]))
            comp_map.setdefault(tri, []).append(e)

    def d4(x, y, t):
        if t == 0:
            return x, y
        if t == 1:
            return n - 1 - x, y
        if t == 2:
            return x, n - 1 - y
        if t == 3:
            return n - 1 - x, n - 1 - y
        if t == 4:
            return y, x
        if t == 5:
            return n - 1 - y, x
        if t == 6:
            return y, n - 1 - x
        return n - 1 - y, n - 1 - x

    d4tab = []
    for t in range(8):
        arr = []
        for c in range(N):
            x, y = c % n, c // n
            u, v = d4(x, y, t)
            arr.append(u + n * v)
        d4tab.append(arr)

    def images(cfg):
        out = []
        for t in range(8):
            im = sorted(d4tab[t][c] for c in cfg)
            out.append(tuple(im))
        return out

    problems = []
    results = []
    prev_row_set = set()
    prev_k = None

    for (k, path) in row_specs:
        cfgs, found, nodes = load_row(path)
        had_prev = (prev_k == k - 1)
        if found is None or nodes is None:
            problems.append("row %d: missing summary line in %s" % (k, path))
            continue
        if len(cfgs) != found:
            problems.append("row %d: cfg lines %d != found %d" % (k, len(cfgs), found))
        seen = set()
        for s in cfgs:
            if len(s) != k or list(s) != sorted(s):
                problems.append("row %d: format %s" % (k, s))
            if s in seen:
                problems.append("row %d: duplicate %s" % (k, s))
            seen.add(s)

        safe_cnt = 0
        max_cnt = 0
        triple_h = {}
        dir_h = {}
        remov_h = {}
        remov_edges = 0
        configs_with_parent = 0
        supcount = {}
        canon = {}
        for s in cfgs:
            k3 = 0
            Smask = bitmask(s)
            covered = set()
            unsafe = False
            for T in itertools.combinations(s, 3):
                k3 += 1
                comps = comp_map.get(T)
                if not comps:
                    continue
                for e in comps:
                    if (Smask >> e) & 1:
                        unsafe = True
                        break
                    covered.add(e)
                if unsafe:
                    break
            if unsafe:
                problems.append("row %d: UNSAFE %s" % (k, s))
            else:
                safe_cnt += 1
                if len(covered) == N - k:
                    max_cnt += 1
                else:
                    problems.append("row %d: NOT MAXIMAL %s uncovered=%d" % (k, s, N - k - len(covered)))
            # three-collinear triples + directions (fresh geometry)
            pts = [(c % n, c // n) for c in s]
            trips = 0
            dirs = set()
            for (i, j, m3) in itertools.combinations(range(k), 3):
                (x1, y1), (x2, y2), (x3, y3) = pts[i], pts[j], pts[m3]
                if (x2 - x1) * (y3 - y1) == (y2 - y1) * (x3 - x1):
                    trips += 1
                    dx, dy = x2 - x1, y2 - y1
                    g = gcd(abs(dx), abs(dy)) or 1
                    dirs.add((dx // g, dy // g))
            triple_h[trips] = triple_h.get(trips, 0) + 1
            dir_h[len(dirs)] = dir_h.get(len(dirs), 0) + 1
            imgs = images(s)
            for im in imgs:
                if im not in seen:
                    problems.append("row %d: closure fail %s -> %s" % (k, s, im))
            canon[s] = min(imgs)
            if had_prev:
                remov = 0
                for st in s:
                    sub_t = tuple(sorted([c for c in s if c != st]))
                    if bitmask(sub_t) in prev_row_set:
                        remov += 1
                        remov_edges += 1
                        supcount[sub_t] = supcount.get(sub_t, 0) + 1
                remov_h[remov] = remov_h.get(remov, 0) + 1
                if remov > 0:
                    configs_with_parent += 1

        # orbits
        orbit_map = {}
        for s, c in canon.items():
            orbit_map[c] = orbit_map.get(c, 0) + 1
        orbits = len(orbit_map)
        orbit_sum = sum(orbit_map.values())
        stab_h = {}
        for c, cnt in orbit_map.items():
            stab = 8 // cnt if cnt in (1, 2, 4, 8) else -1
            stab_h[stab] = stab_h.get(stab, 0) + 1
        if orbit_sum != len(cfgs):
            problems.append("row %d: orbit sum %d != %d" % (k, orbit_sum, len(cfgs)))

        rec = {
            "k": k,
            "found": found,
            "k3_prefixes": k3 if cfgs else 0,
            "nodes": nodes,
            "safe_all": safe_cnt == len(cfgs) and len(cfgs) == found,
            "maximal_all": max_cnt == len(cfgs) and len(cfgs) == found,
            "orbits_python": orbits,
            "orbit_sum": orbit_sum,
            "stabilizer_histogram": dict(sorted(stab_h.items())),
            "trips3_histogram": dict(sorted(triple_h.items())),
            "dirs_histogram": dict(sorted(dir_h.items())),
            "all_have_three_collinear": (0 not in triple_h),
            "remov_histogram": dict(sorted(remov_h.items())) if had_prev else None,
            "configs_containing_prev_row_member": configs_with_parent if had_prev else None,
            "edges_to_prev_row": remov_edges if had_prev else None,
        }
        if had_prev and results:
            sup_h = {}
            for parent, cnt in supcount.items():
                sup_h[cnt] = sup_h.get(cnt, 0) + 1
            results[-1]["supersets_in_next_row_histogram"] = dict(sorted(sup_h.items()))
            results[-1]["parents_covered"] = len(supcount)
            results[-1]["parents_total"] = results[-1]["found"]
        results.append(rec)

        # --- controls on the first configuration of the row ---
        if cfgs:
            s0 = cfgs[0]
            S0mask = bitmask(s0)
            tamper_unsafe = None
            for e in range(N):
                if (S0mask >> e) & 1:
                    continue
                for T in itertools.combinations(s0, 3):
                    comps = comp_map.get(T)
                    if comps and e in comps:
                        tamper_unsafe = (e, T)
                        break
                if tamper_unsafe:
                    break
            if tamper_unsafe is None:
                problems.append("row %d: control (b) no covered cell found for %s" % (k, s0))
            else:
                e, _T = tamper_unsafe
                bad = tuple(sorted(list(s0) + [e]))
                Bm = bitmask(bad)
                unsafe = False
                for TT in itertools.combinations(bad, 3):
                    comps = comp_map.get(TT)
                    if comps:
                        for ee in comps:
                            if (Bm >> ee) & 1:
                                unsafe = True
                                break
                    if unsafe:
                        break
                if not unsafe:
                    problems.append("row %d: TAMPER (b) not rejected: %s + %d" % (k, s0, e))
                rec["control_unsafe_tamper"] = {"added": e, "rejected": unsafe}
            # control (c): remove a stone whose removal is not a row-(k-1) member
            target = None
            if had_prev:
                for s in cfgs:
                    for st in s:
                        sub_t = tuple(sorted([c for c in s if c != st]))
                        if bitmask(sub_t) not in prev_row_set:
                            target = (s, st)
                            break
                    if target:
                        break
                if target is None:
                    # every removal of the FIRST config... search exhausted all cfgs
                    problems.append("row %d: control (c) no non-member removal found (all removals of all configs are row-(k-1) members)" % k)
                else:
                    s, st = target
                    sub = [c for c in s if c != st]
                    m = bitmask(sub)
                    covered = set()
                    for T in itertools.combinations(sub, 3):
                        comps = comp_map.get(T)
                        if not comps:
                            continue
                        for e2 in comps:
                            if not (m >> e2) & 1:
                                covered.add(e2)
                    not_max = (len(covered) != N - (k - 1))
                    if not not_max:
                        problems.append("row %d: TAMPER (c) not rejected: %s - %d" % (k, s, st))
                    rec["control_nonmax_tamper"] = {"removed": st, "rejected": not_max}
            else:
                rec["control_nonmax_tamper"] = {"applicable": False}

        prev_row_set = seen if found > 0 else set()
        prev_k = k

    out = {
        "n": n,
        "N": N,
        "quartets": len(quarts),
        "quartet_file_sha256": qsha,
        "rows": results,
        "problems": problems,
    }
    with open(outprefix + "_rows.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    brief = {k2: v for k2, v in out.items() if k2 != "rows"}
    brief_rows = [{kk: vv for kk, vv in r.items()
                   if kk in ("k", "found", "nodes", "safe_all", "maximal_all",
                             "orbits_python", "closure_violations")}
                  for r in results]
    brief["rows_brief"] = brief_rows
    print(json.dumps(brief))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
