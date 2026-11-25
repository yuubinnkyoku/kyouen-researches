#!/usr/bin/env python3
"""General exact minimum-cover membership / joint analysis for a single open S5
parent, applied to three targets:

  1. validation on the class-2 top parent (11 rows): the published membership
     output (singleton-type 337,020 + six-pair-type 22,590 = 359,610 total,
     per-root A/B splits, blob ab1e655f...) must be reproduced exactly;
  2. validation on the cost-9 parent (18 rows): the published membership
     output (3,427,072,113,767 total, blob a1c5c8b6...) must be reproduced
     exactly;
  3. NEW: the cost-12 parent 00000000000000003800000008002000 (23 rows,
     partial_sterile, exact cost 12).

Cover semantics are the published ones (a root covers the open non-STERILE
rows that generate it; maxspan is 2 for every parent). Let k be the exact
minimum size and r the number of target rows.

Even r: every minimum cover is a perfect matching of pair roots
  (s + p = k, s + 2p >= r forces s = 0, and k pair roots over r slots force
   all rows disjoint), so total = weighted pm(V) and membership of a pair
   root on {a,b} = pm(V\\{a,b}); singleton-span roots never appear.

Odd r: two cover types exist (s + p = k, s + 2p >= r):
  A (k-1 pairs + 1 singleton, all disjoint):
     A = sum_s w1(s) * pm(V\\{s})
  B (k pairs, exactly one doubly covered row d, the two pairs containing d
     being {d,a},{d,b} with a != b, all other pairs disjoint from these):
     B = sum_d sum_{a<b, a,b != d} w(d,a) * w(d,b) * pm(V\\{d,a,b})
  Membership of a pair root on e={x,y}:
     A-part = sum_{s not in e} w1(s) * pm(V\\e\\{s})
     B-part = sum_{d in e}  sum_{z not in e} w(d,z) * pm(V\\e\\{z})          [e is a duplicate pair]
            + sum_{d not in e} sum_{a<b, a,b not in e+{d}} w(d,a)w(d,b)
                                  * pm(V\\e\\{d,a,b})                        [e is a regular pair]
  Membership of a singleton root on row s: A-part = pm(V\\{s}), B-part = 0.
  Identities: sum of A-parts == k*A and sum of B-parts == k*B.

All pm values come from one bottom-up all-mask weighted matching DP over 2^r
row masks (odd-popcount masks have pm 0 and are skipped). Every pm lookup in
the formulas above is a table read, so the whole analysis is exact.

Joint membership of two roots (covers containing both), full case analysis:
  even r: disjoint pairs -> pm(V\\e1\\e2); sharing a row -> 0.
  odd r, pair roots e1, e2:
    sharing row d (e1={d,a}, e2={d,b}, a!=b): only type B with e1,e2 as the
      duplicate pairs: pm(V\\{d,a,b});
    disjoint:
      A: sum_{s not in e1+e2} w1(s) * pm(V\\e1\\e2\\{s})
      B-i (neither is a duplicate pair): sum_{d not in e1+e2}
           sum_{a<b, a,b not in e1+e2+{d}} w(d,a)w(d,b) pm(V\\e1\\e2\\{d,a,b})
      B-ii (e1 or e2 is a duplicate pair): sum_{d in e1} sum_{z not in e1+e2}
           w(d,z) * pm(V\\e1\\e2\\{z}), and symmetrically for e2.
  odd r, singleton root on s with pair root on e: 0 if s in e else
      pm(V\\e\\{s}) (type A only); two singleton roots: 0 (type A covers have
      exactly one singleton).

Machine checks include the two k*total identities, witness crosschecks against
the published cover-cost table (blob 4e4a911d), and for the two validation
targets a full per-root numeric comparison with the published membership
outputs (blob-pinned).
"""
import json, os, sys, hashlib, time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
N = 11

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()

def read_pinned(rel, pin):
    with open(os.path.join(ROOT, rel), "rb") as f:
        data = f.read()
    if git_blob_sha(data) != pin:
        raise SystemExit("pin mismatch: " + rel)
    return data

T = [
    lambda x, y: (x, y),
    lambda x, y: (y, N - 1 - x),
    lambda x, y: (N - 1 - x, N - 1 - y),
    lambda x, y: (N - 1 - y, x),
    lambda x, y: (N - 1 - x, y),
    lambda x, y: (x, N - 1 - y),
    lambda x, y: (y, x),
    lambda x, y: (N - 1 - y, N - 1 - x),
]
TO = [tuple(t(i % N, i // N) for i in range(121)) for t in T]

def orbit_masks(mask):
    outs = []
    for to in TO:
        out = 0
        for i in range(121):
            if (mask >> i) & 1:
                qx, qy = to[i]
                out |= 1 << (qy * N + qx)
        outs.append(out)
    return outs

def pm_all_masks(r, edge_mult):
    """pm[mask] = weighted perfect matching count of the row subset `mask`,
    for ALL masks 0..2^r-1. Bottom-up: removing the lowest set bit and a
    partner strictly decreases the integer."""
    adj = [[] for _ in range(r)]
    for (a, b), w in edge_mult.items():
        if w:
            adj[a].append((1 << b, w))
    size = 1 << r
    pm = [0] * size
    pm[0] = 1
    for mask in range(1, size):
        if mask.bit_count() & 1:
            continue
        low = mask & -mask
        first = low.bit_length() - 1
        sub = mask ^ low
        acc = 0
        for jbit, w in adj[first]:
            if sub & jbit:
                acc += w * pm[sub ^ jbit]
        if acc:
            pm[mask] = acc
    return pm

def analyze_parent(target_hex, row_cands, tbl, p_orbit_cache, log, survival_k=0):
    checks = []
    def check(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok),
                       "detail": detail if isinstance(detail, str) else json.dumps(detail)})

    p_orbit = p_orbit_cache.setdefault(target_hex,
                    {format(m, "032x") for m in orbit_masks(int(target_hex, 16))})
    target = sorted(h for h in row_cands
                    if any(format(int(h, 16) ^ (1 << b), "032x") in p_orbit
                           for b in range(121) if (int(h, 16) >> b) & 1))
    r = len(target)
    check("rows", r == tbl["rows_r"], {"got": r, "table": tbl["rows_r"]})
    k = tbl["witness_size"]
    check("exact", tbl["exact"] and tbl["lower_bound"] == k)

    idx = {h: i for i, h in enumerate(target)}
    proot_rows = defaultdict(set)
    cand_total = 0
    for h in target:
        e = row_cands[h]
        cand_total += e["cost"]
        for root, bit in e["cands"]:
            proot_rows[root].add(h)
    check("candidates", cand_total == tbl["candidates"], {"got": cand_total, "table": tbl["candidates"]})
    check("distinct_roots", len(proot_rows) == tbl["distinct_roots"],
          {"got": len(proot_rows), "table": tbl["distinct_roots"]})
    hist = defaultdict(int)
    for root, cov in proot_rows.items():
        hist[len(cov)] += 1
    check("span_histogram", {str(x): v for x, v in sorted(hist.items())} == tbl["span_histogram"],
          dict(hist))
    check("maxspan2", max(hist) == 2)

    pair_roots = defaultdict(list)
    singleton_roots = defaultdict(list)  # row index -> roots
    for root, cov in proot_rows.items():
        if len(cov) == 2:
            a, b = sorted(idx[h] for h in cov)
            pair_roots[(a, b)].append(root)
        else:
            (s,) = [idx[h] for h in cov]
            singleton_roots[s].append(root)
    edge_w = {e: len(rl) for e, rl in pair_roots.items()}
    w1 = {s: len(rl) for s, rl in singleton_roots.items()}
    root_pair = {root: e for e, rl in pair_roots.items() for root in rl}
    root_row = {root: s for s, rl in singleton_roots.items() for root in rl}
    log("  roots: %d pair-span over %d pair types, %d singleton-span" %
        (sum(len(v) for v in pair_roots.values()), len(pair_roots), sum(len(v) for v in singleton_roots.values())))

    t0 = time.time()
    pm = pm_all_masks(r, edge_w)
    full = (1 << r) - 1
    log("  pm DP over 2^%d masks: %.1fs" % (r, time.time() - t0))

    if r % 2 == 0:
        total = pm[full]
        total_A = total; total_B = 0
        membership = {}
        mem_A = {}; mem_B = {}
        for root, e in root_pair.items():
            m = pm[full & ~((1 << e[0]) | (1 << e[1]))]
            membership[root] = m; mem_A[root] = m; mem_B[root] = 0
        for root, s in root_row.items():
            membership[root] = 0; mem_A[root] = 0; mem_B[root] = 0
    else:
        total_A = sum(w1[s] * pm[full ^ (1 << s)] for s in w1)
        total_B = 0
        for d in range(r):
            inc = [(1 << a, edge_w[(min(d, a), max(d, a))]) for a in range(r)
                   if a != d and edge_w.get((min(d, a), max(d, a)))]
            for i in range(len(inc)):
                for j in range(i + 1, len(inc)):
                    abit, wa = inc[i]; bbit, wb = inc[j]
                    rest = full ^ (1 << d) ^ abit ^ bbit
                    total_B += wa * wb * pm[rest]
        total = total_A + total_B
        membership = {}; mem_A = {}; mem_B = {}
        for root, s in root_row.items():
            m = pm[full ^ (1 << s)]
            membership[root] = m; mem_A[root] = m; mem_B[root] = 0
        for root, e in root_pair.items():
            ea, eb = e
            a_part = 0
            for s in w1:
                if s not in e:
                    a_part += w1[s] * pm[full & ~((1 << ea) | (1 << eb) | (1 << s))]
            b_part = 0
            for d in e:
                for z in range(r):
                    if z in e:
                        continue
                    key = (min(d, z), max(d, z))
                    wz = edge_w.get(key, 0)
                    if wz:
                        b_part += wz * pm[full & ~((1 << ea) | (1 << eb) | (1 << z))]
            for d in range(r):
                if d in e:
                    continue
                inc = []
                for a in range(r):
                    if a in e or a == d:
                        continue
                    key = (min(d, a), max(d, a))
                    wa = edge_w.get(key, 0)
                    if wa:
                        inc.append((1 << a, wa))
                for i in range(len(inc)):
                    for j in range(i + 1, len(inc)):
                        abit, wa = inc[i]; bbit, wb = inc[j]
                        rest = full ^ (1 << d) ^ abit ^ bbit ^ (1 << ea) ^ (1 << eb)
                        b_part += wa * wb * pm[rest]
            membership[root] = a_part + b_part
            mem_A[root] = a_part; mem_B[root] = b_part

    check("total_positive", total > 0, str(total))
    sum_A = sum(mem_A.values()); sum_B = sum(mem_B.values())
    check("identity_A", sum_A == k * total_A, {"sum": str(sum_A), "kA": str(k * total_A)})
    check("identity_B", sum_B == k * total_B, {"sum": str(sum_B), "kB": str(k * total_B)})
    check("identity_total", sum_A + sum_B == k * total,
          {"sum": str(sum_A + sum_B), "kT": str(k * total)})

    # witness crosscheck
    wit = tbl["witness_roots"]
    wit_cov = {root: proot_rows[root] for root in wit}
    wit_rows = set()
    for root in wit:
        wit_rows |= wit_cov[root]
    check("witness.covers_all", wit_rows == set(target) and len(wit) == k)
    check("witness.spans", sum(len(v) for v in wit_cov.values()) == r)
    check("witness.membership_positive", all(membership[root] > 0 for root in wit))

    # top-10 joint membership (pair roots only, by membership)
    by_mem = sorted([x for x in membership if membership[x] > 0 and x in root_pair],
                    key=lambda x: (-membership[x], x))
    top10 = by_mem[:10]
    joint = []
    for i in range(len(top10)):
        for j in range(i + 1, len(top10)):
            r1, r2 = top10[i], top10[j]
            e1 = root_pair[r1]; e2 = root_pair[r2]
            if r % 2 == 0:
                if set(e1) & set(e2):
                    m_ij = 0
                else:
                    m_ij = pm[full & ~((1 << e1[0]) | (1 << e1[1]) | (1 << e2[0]) | (1 << e2[1]))]
            else:
                sh = set(e1) & set(e2)
                if sh:
                    d = sh.pop()
                    a = e1[0] if e1[1] == d else e1[1]
                    b = e2[0] if e2[1] == d else e2[1]
                    m_ij = 0 if a == b else pm[full ^ (1 << d) ^ (1 << a) ^ (1 << b)]
                else:
                    m_ij = 0
                    for s in w1:
                        if s not in e1 and s not in e2:
                            m_ij += w1[s] * pm[full & ~((1 << e1[0]) | (1 << e1[1])
                                                        | (1 << e2[0]) | (1 << e2[1]) | (1 << s))]
                    rows12 = set(e1) | set(e2)
                    # B-i
                    for d in range(r):
                        if d in rows12:
                            continue
                        inc = []
                        for a in range(r):
                            if a in rows12 or a == d:
                                continue
                            key = (min(d, a), max(d, a))
                            wa = edge_w.get(key, 0)
                            if wa:
                                inc.append((1 << a, wa))
                        for x in range(len(inc)):
                            for y in range(x + 1, len(inc)):
                                abit, wa = inc[x]; bbit, wb = inc[y]
                                rest = full ^ (1 << d) ^ abit ^ bbit \
                                       ^ (1 << e1[0]) ^ (1 << e1[1]) ^ (1 << e2[0]) ^ (1 << e2[1])
                                m_ij += wa * wb * pm[rest]
                    # B-ii
                    for (eA, eB) in ((e1, e2), (e2, e1)):
                        for d in eA:
                            for z in range(r):
                                if z in rows12:
                                    continue
                                key = (min(d, z), max(d, z))
                                wz = edge_w.get(key, 0)
                                if wz:
                                    m_ij += wz * pm[full & ~((1 << e1[0]) | (1 << e1[1])
                                                             | (1 << e2[0]) | (1 << e2[1]) | (1 << z))]
            joint.append({"a": r1, "b": r2, "pair_a": list(e1), "pair_b": list(e2),
                          "membership_a": membership[r1], "membership_b": membership[r2],
                          "joint_membership": m_ij})
    check("joint.bounded",
          all(e["joint_membership"] <= min(e["membership_a"], e["membership_b"]) for e in joint))

    # optional survival curve: ban top-k roots by membership (any span)
    survival = None
    if survival_k > 0:
        by_mem_all = sorted(membership, key=lambda x: (-membership[x], x))
        survival = []
        prev_killed = 0
        banned = set()
        for kk in range(0, survival_k + 1):
            if kk > 0:
                banned.add(by_mem_all[kk - 1])
            ew = dict(edge_w)
            ww1 = dict(w1)
            for root in banned:
                if root in root_pair:
                    ew[root_pair[root]] = ew[root_pair[root]] - 1
                else:
                    ww1[root_row[root]] = ww1[root_row[root]] - 1
            pm2 = pm_all_masks(r, ew)
            if r % 2 == 0:
                tot = pm2[full]
            else:
                A2 = 0
                for s, w in ww1.items():
                    if w > 0:
                        A2 += w * pm2[full ^ (1 << s)]
                B2 = 0
                for dd in range(r):
                    inc = []
                    for a in range(r):
                        if a == dd:
                            continue
                        wa = ew.get((min(dd, a), max(dd, a)), 0)
                        if wa > 0:
                            inc.append((1 << a, wa))
                    for i2 in range(len(inc)):
                        for j2 in range(i2 + 1, len(inc)):
                            abit, wa = inc[i2]; bbit, wb = inc[j2]
                            B2 += wa * wb * pm2[full ^ (1 << dd) ^ abit ^ bbit]
                tot = A2 + B2
            killed = total - tot
            survival.append({"k": kk,
                             "banned_root": by_mem_all[kk] if kk < survival_k else None,
                             "surviving_covers": tot, "killed_covers": killed,
                             "killed_share": killed / total,
                             "marginal_kill": killed - prev_killed})
            prev_killed = killed
        check("survival.k1_marginal_equals_membership",
              survival[1]["marginal_kill"] == membership[by_mem_all[0]],
              {"marginal": str(survival[1]["marginal_kill"]),
               "membership": str(membership[by_mem_all[0]])})
        check("survival.monotone",
              all(survival[i2]["surviving_covers"] <= survival[i2 - 1]["surviving_covers"]
                  for i2 in range(1, survival_k + 1)))
        log("  survival curve k=0..%d done" % survival_k)

    return {
        "rows": r, "candidates": cand_total, "distinct_roots": len(proot_rows),
        "span_histogram": {str(x): v for x, v in sorted(hist.items())},
        "pair_types": len(pair_roots),
        "minimum_size": k,
        "parity": "even" if r % 2 == 0 else "odd",
        "total_minimum_covers": total,
        "type_A_disjoint": total_A,
        "type_B_one_duplicate_row": total_B,
        "membership": {x: membership[x] for x in sorted(membership)},
        "membership_A_type": {x: mem_A[x] for x in sorted(mem_A)},
        "membership_B_type": {x: mem_B[x] for x in sorted(mem_B)},
        "top50_by_membership": [
            {"root": x, "membership": membership[x],
             "pair_row_indices": list(root_pair[x]) if x in root_pair else [root_row[x]],
             "pair_rows": [target[root_pair[x][0]], target[root_pair[x][1]]]
                          if x in root_pair else [target[root_row[x]]]}
            for x in by_mem[:50]],
        "top10_joint_membership": joint,
        "survival_curve_banning_topk": survival,
        "membership_nonzero_stats": {
            "count": sum(1 for v in membership.values() if v > 0),
            "min": min((v for v in membership.values() if v > 0), default=0),
            "max": max(membership.values()),
        },
        "per_row_singleton_root_count": {str(s): w1.get(s, 0) for s in range(r)},
        "witness_membership": {root: membership[root] for root in wit},
        "checks": checks,
    }

def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "output", "cost12-parent-cover-membership-20261118.json")
    def log(msg):
        print(msg, flush=True)

    read_pinned("research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
                "2fee1d0718547a62e346d35f5858d7913e37c097")
    read_pinned("research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
                "9c251da3138c5cb0516e097be5e5d0427dfaf5f0")
    read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
                "e8785d509e8a11a37c0d03cc450455a14708c34d")
    table = json.loads(read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/parent-minimum-cover-cost-table-20261118.json",
                                   "4e4a911d0e05779437d4a8e97685a8feb66c0d25"))
    tbl_by_hex = {e["hex"]: e for e in table["derived"]["table"]}

    row_cands = {}
    with open(os.path.join(HERE, "output", "global-candidate-roots-20261118.jsonl")) as f:
        for line in f:
            e = json.loads(line)
            row_cands[e["row"]] = e

    pub11 = json.loads(read_pinned(
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/minimum-cover-root-membership-20261118.json",
        "ab1e655f4a89a677e57515cdbacfe56894323013"))
    pub18 = json.loads(read_pinned(
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/cost9-parent-membership-and-elimination-20261118.json",
        "a1c5c8b6bd577df49cd5c8a445e2b698e1223ef7"))

    p_orbit_cache = {}
    all_checks = []

    # ---- target 1: validation on 11-row parent
    log("[1/3] 11-row validation target")
    v11 = analyze_parent("00000000000000403800000008000000", row_cands,
                         tbl_by_hex["00000000000000403800000008000000"], p_orbit_cache, log)
    cs = v11.pop("checks"); all_checks += cs
    pub_space = pub11["derived"]["cover_space"]
    pub_mem = {e["root"]: e for e in pub11["derived"]["all_root_memberships"]}
    mism = 0
    for root, m in v11["membership"].items():
        p = pub_mem.get(root)
        if p is None or p["membership"] != m \
           or p["singleton_type_covers"] != v11["membership_A_type"][root] \
           or p["six_pair_type_covers"] != v11["membership_B_type"][root]:
            mism += 1
    v11["published_crosscheck"] = {
        "published_total": pub_space["total_minimum_covers"],
        "recomputed_total": v11["total_minimum_covers"],
        "published_A": pub_space["singleton_type_covers"],
        "recomputed_A": v11["type_A_disjoint"],
        "published_B": pub_space["six_pair_covers"],
        "recomputed_B": v11["type_B_one_duplicate_row"],
        "membership_roots_compared": len(v11["membership"]),
        "membership_mismatches": mism,
    }
    v11["checks"] = cs

    # ---- target 2: validation on 18-row parent
    log("[2/3] 18-row validation target")
    v18 = analyze_parent("00000000000000821082000000000000", row_cands,
                         tbl_by_hex["00000000000000821082000000000000"], p_orbit_cache, log)
    cs = v18.pop("checks"); all_checks += cs
    pub_mem18 = pub18["derived"]["membership"]
    mism18 = [root for root, m in v18["membership"].items() if pub_mem18.get(root) != m]
    v18["published_crosscheck"] = {
        "published_total": pub18["derived"]["total_minimum_covers"],
        "recomputed_total": v18["total_minimum_covers"],
        "membership_roots_compared": len(v18["membership"]),
        "membership_mismatches": len(mism18),
        "mismatch_roots": mism18[:5],
    }
    v18["checks"] = cs

    # ---- target 3: NEW cost-12 parent
    log("[3/3] 23-row cost-12 target (with survival curve)")
    v23 = analyze_parent("00000000000000003800000008002000", row_cands,
                         tbl_by_hex["00000000000000003800000008002000"], p_orbit_cache, log,
                         survival_k=12)
    cs = v23.pop("checks"); all_checks += cs
    v23["checks"] = cs

    # validation checks
    def check(name, ok, detail=""):
        all_checks.append({"name": name, "pass": bool(ok),
                           "detail": detail if isinstance(detail, str) else json.dumps(detail)})
    check("validate11.total", v11["published_crosscheck"]["published_total"] == v11["total_minimum_covers"] == 359610)
    check("validate11.A", v11["published_crosscheck"]["published_A"] == v11["type_A_disjoint"] == 337020)
    check("validate11.B", v11["published_crosscheck"]["published_B"] == v11["type_B_one_duplicate_row"] == 22590)
    check("validate11.membership_exact", v11["published_crosscheck"]["membership_mismatches"] == 0,
          v11["published_crosscheck"])
    check("validate18.total", v18["published_crosscheck"]["published_total"] == v18["total_minimum_covers"] == 3427072113767)
    check("validate18.membership_exact", v18["published_crosscheck"]["membership_mismatches"] == 0,
          v18["published_crosscheck"])

    # slim the output for publication size: validation targets drop the full
    # membership dicts (the numeric agreement is recorded in
    # published_crosscheck and checks), and the cost-12 target keeps A/B
    # splits only for the top-50 roots.
    for vv in (v11, v18):
        for key in ("membership", "membership_A_type", "membership_B_type"):
            vv.pop(key)
        vv["membership_dict_note"] = "dropped for size; exact per-root agreement with the published output is machine-checked (0 mismatches)"
    top50_roots = [e["root"] for e in v23["top50_by_membership"]]
    v23["membership_A_type"] = {x: v23["membership_A_type"][x] for x in top50_roots}
    v23["membership_B_type"] = {x: v23["membership_B_type"][x] for x in top50_roots}

    all_pass = all(c["pass"] for c in all_checks)
    output = {
        "schema": "n11-cost12-parent-cover-membership-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("General exact minimum-cover membership framework (even/odd r, disjoint and "
                  "one-duplicate-row types) validated against both published membership outputs, "
                  "then applied to the cost-12 parent 00000000000000003800000008002000 (23 rows)"),
        "inputs": {
            "worklist": {"path": "research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
                          "git_blob_sha1": "2fee1d0718547a62e346d35f5858d7913e37c097"},
            "census": {"path": "research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
                        "git_blob_sha1": "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"},
            "ledger": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
                        "git_blob_sha1": "e8785d509e8a11a37c0d03cc450455a14708c34d"},
            "cover_table": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/parent-minimum-cover-cost-table-20261118.json",
                             "git_blob_sha1": "4e4a911d0e05779437d4a8e97685a8feb66c0d25"},
            "published_membership_11row": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/minimum-cover-root-membership-20261118.json",
                                            "git_blob_sha1": "ab1e655f4a89a677e57515cdbacfe56894323013"},
            "published_membership_18row": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/cost9-parent-membership-and-elimination-20261118.json",
                                             "git_blob_sha1": "a1c5c8b6bd577df49cd5c8a445e2b698e1223ef7"},
            "candidate_roots": {"path": "(regenerated) output/global-candidate-roots-20261118.jsonl",
                                 "regenerated_by": "enumerate_global_candidate_roots_20261118.py",
                                 "note": ("deterministic from the pinned inputs; all per-parent "
                                          "aggregates cross-checked against the published table")},
        },
        "method": ("One bottom-up all-mask weighted matching DP over 2^r row masks gives every pm "
                   "value used below. Even r: minimum covers are perfect matchings of pair roots. "
                   "Odd r: covers are either (k-1 pairs + 1 singleton, disjoint) or (k pairs with "
                   "exactly one doubly covered row); membership, joint membership and both totals "
                   "are closed-form sums of pm table reads, with per-root A/B splits. Identities "
                   "sum(A-parts)==k*A and sum(B-parts)==k*B plus the published-value reproductions "
                   "on the 11-row and 18-row targets validate the framework before the 23-row run."),
        "validation_11row": v11,
        "validation_18row": v18,
        "cost12_parent": v23,
        "checks": all_checks,
        "check_count": len(all_checks),
        "all_pass": all_pass,
        "interpretation_guard": ("Cover-plan combinatorics only. Membership counts alternative "
                                 "minimum cover plans containing a root; it is not a search cost "
                                 "and implies nothing about WIN/REFUTED outcomes. REFUTED-D10 and "
                                 "STERILE are not LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
                           "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    with open(out_path, "w") as f:
        f.write(json.dumps(output, indent=2) + "\n")
    log("wrote %s: all_pass=%s checks=%d" % (out_path, all_pass, len(all_checks)))
    print(json.dumps({"out": out_path, "all_pass": all_pass, "checks": len(all_checks),
                      "failed": [c["name"] for c in all_checks if not c["pass"]][:10],
                      "v11_total": v11["total_minimum_covers"],
                      "v18_total": v18["total_minimum_covers"],
                      "cost12_total": v23["total_minimum_covers"],
                      "cost12_A": v23["type_A_disjoint"],
                      "cost12_B": v23["type_B_one_duplicate_row"],
                      "cost12_stats": v23["membership_nonzero_stats"]},
                     indent=1))
    if not all_pass:
        sys.exit(1)

if __name__ == "__main__":
    main()
