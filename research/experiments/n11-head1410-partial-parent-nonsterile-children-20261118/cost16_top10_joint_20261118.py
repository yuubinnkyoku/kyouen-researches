#!/usr/bin/env python3
"""Top-10 joint membership (45 combinations) for the 31-row cost-16 parent
00000000000000003800000008001000.

This is the follow-up computation explicitly deferred by the published
phase-B groups aggregate output (cost16-b-phase-groups-20261118.json,
"deferred" field): the pairwise joint memberships of the top-10 pair roots
by membership, with A/B split.

Joint of two pair types e1, e2 (all 425 types have multiplicity 1, so a
pair type is exactly one root):

- If e1, e2 share a row (|e1 u e2| = 3):
    joint_A = 0   (an A-type cover covers every row exactly once, so two
                  row-sharing pair roots can never co-occur in one)
    joint_B = pm(V \\ (e1 u e2))   (the shared row is forced to be the single
                  doubly-covered row; the remaining 14 pair roots form a
                  perfect matching on the other 28 rows)
- If e1, e2 are disjoint (|e1 u e2| = 4):
    joint_A = sum_s w1[s] * pm(V \\ e1 \\ e2 \\ {s})
    joint_B = sum_z W(z) * pm(V \\ e1 \\ e2 \\ {z})
            + sum_d sum_{x<y} w(d,x) w(d,y) * pm(V \\ e1 \\ e2 \\ {d,x,y})
  where W(z) = sum_{d in e1 u e2} w(d,z), the first B-term runs over z
  outside e1 u e2 (doubled row inside e1 u e2, its second covering pair
  (d,z)), and the second B-term runs over d outside e1 u e2 and x<y outside
  e1 u e2 u {d} (doubled row outside, covered by (d,x),(d,y)).

This is the direct 2-type generalization of the published, independently
triple-anchored 1-type a_part/b_part formulas in cost16_parent_membership /
cost16_phase_b_groups (same B-type semantics: 16 pair roots, exactly one
doubly-covered row; the remaining pairs form a perfect matching).

Mode validate11: on the 11-row parent (class-2 top parent), enumerate ALL
minimum covers explicitly (A-type: 5 pair roots + 1 singleton; B-type: 6
pair roots, one doubled row), tally type-pair joints with A/B split, and
require the formula above to reproduce them exactly; cross-check the
published total/A/B (359,610 / 337,020 / 22,590), all 757 root memberships,
and all 45 published top-10 root-level joints.

Mode joints FROM TO BUDGET: compute the 45 top-10 combinations of the 31-row
parent, sorted combo indices [FROM, TO), fresh shared-memo PmLazy per
invocation, resume-safe JSONL append (a killed invocation loses nothing).

Mode aggregate: assemble the final output JSON with checks, including the
exact k=1 and k=2 ban survival points.
"""
import json, os, sys, time, gc, resource
from collections import defaultdict
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
import cost16_parent_membership_20261118 as base

TARGET = "00000000000000003800000008001000"
TOP11 = "00000000000000403800000008000000"
COVER_TABLE_PIN = "4e4a911d0e05779437d4a8e97685a8feb66c0d25"
COVER_TABLE_REL = ("research/experiments/n11-head1410-partial-parent-"
                   "nonsterile-children-20261118/output/"
                   "parent-minimum-cover-cost-table-20261118.json")
PHASE_A_PIN = "fe4b4b559fd8c3fdc9bc9b9f40a048fc3217c55b"
GROUPS_AGG_PIN = "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87"
GROUPS_AGG_REL = ("research/experiments/n11-head1410-partial-parent-"
                  "nonsterile-children-20261118/output/"
                  "cost16-b-phase-groups-20261118.json")
ELIM11_PIN = "5f6185483f7a6458535b8e38a73483a23db2ef29"
MEMB11_PIN = "ab1e655f4a89a677e57515cdbacfe56894323013"
ELIM11_REL = ("research/experiments/n11-head1410-partial-parent-"
              "nonsterile-children-20261118/output/"
              "minimum-cover-elimination-structure-20261118.json")
MEMB11_REL = ("research/experiments/n11-head1410-partial-parent-"
              "nonsterile-children-20261118/output/"
              "minimum-cover-root-membership-20261118.json")
JOINTS_JSONL = os.path.join(HERE, "output", "cost16-top10-joint-20261118.jsonl")


def load_parent(target_hex):
    table = json.loads(base.read_pinned(COVER_TABLE_REL, COVER_TABLE_PIN))
    tbl = {e["hex"]: e for e in table["derived"]["table"]}[target_hex]
    row_cands = {}
    with open(os.path.join(HERE, "output",
                           "global-candidate-roots-20261118.jsonl")) as f:
        for line in f:
            e = json.loads(line)
            row_cands[e["row"]] = e
    P = base.build_parent(target_hex, row_cands, {})
    del row_cands
    gc.collect()
    return P, tbl


def enum_matchings(edge_w, mask):
    """Yield all perfect matchings of the row set `mask` as tuples of
    (sorted) pair types with nonzero edge weight."""
    if mask == 0:
        yield ()
        return
    low = mask & -mask
    i = low.bit_length() - 1
    rest = mask ^ low
    mm = rest
    while mm:
        jbit = mm & -mm
        mm ^= jbit
        j = jbit.bit_length() - 1
        e = (i, j) if i < j else (j, i)
        if edge_w.get(e, 0):
            for tail in enum_matchings(edge_w, rest ^ jbit):
                yield (e,) + tail


def mode_validate11():
    P, tbl = load_parent(TOP11)
    r = len(P["target"])
    k = tbl["witness_size"]
    assert r == 11 and k == 6 and tbl["exact"], (r, k, tbl["exact"])
    edge_w = P["edge_w"]
    w1 = {s: len(rl) for s, rl in P["singleton_roots"].items()}
    for s in range(r):
        w1.setdefault(s, 0)
    full = (1 << r) - 1
    root_row = {root: s for s, rl in P["singleton_roots"].items()
                for root in rl}
    mult = {e: len(rl) for e, rl in P["pair_roots"].items()}
    checks = []

    def check(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok),
                       "detail": detail if isinstance(detail, str)
                       else json.dumps(detail)})
        print(("PASS " if ok else "FAIL ") + name, flush=True)

    # ---- explicit enumeration of ALL minimum covers, type level
    joint_A_T = defaultdict(int)
    joint_B_T = defaultdict(int)
    a_part_T = defaultdict(int)
    b_part_T = defaultdict(int)
    A_total = 0
    B_total = 0
    sing_covers_by_row = {}  # row -> number of A covers using a singleton of that row
    for s in range(r):
        if not w1[s]:
            continue
        sub = full ^ (1 << s)
        cnt = 0
        for matching in enum_matchings(edge_w, sub):
            c = w1[s]
            A_total += c
            cnt += 1
            for e in matching:
                a_part_T[e] += c
            for e1, e2 in combinations(matching, 2):
                key = (e1, e2) if e1 < e2 else (e2, e1)
                joint_A_T[key] += c
        sing_covers_by_row[s] = cnt
    for z in range(r):
        for x in range(r):
            if x == z:
                continue
            ex = (min(z, x), max(z, x))
            wx = edge_w.get(ex, 0)
            if not wx:
                continue
            for y in range(x + 1, r):
                if y == z:
                    continue
                ey = (min(z, y), max(z, y))
                wy = edge_w.get(ey, 0)
                if not wy:
                    continue
                sub = full & ~((1 << z) | (1 << x) | (1 << y))
                for matching in enum_matchings(edge_w, sub):
                    c = wx * wy
                    B_total += c
                    types6 = (ex, ey) + matching
                    for e in types6:
                        b_part_T[e] += c
                    for e1, e2 in combinations(types6, 2):
                        key = (e1, e2) if e1 < e2 else (e2, e1)
                        joint_B_T[key] += c
    total = A_total + B_total
    check("enum11.total", total == 359610, str(total))
    check("enum11.A_total", A_total == 337020, str(A_total))
    check("enum11.B_total", B_total == 22590, str(B_total))

    # ---- per-root membership vs published
    memb11 = json.loads(base.read_pinned(MEMB11_REL, MEMB11_PIN))
    pub = {e["root"]: e for e in memb11["derived"]["all_root_memberships"]}
    check("enum11.pub_root_count", len(pub) == 757, len(pub))
    mism = 0
    for root, s in root_row.items():
        v = sing_covers_by_row[s]
        if pub[root]["membership"] != v or pub[root]["six_pair_type_covers"]:
            mism += 1
    for e, rl in P["pair_roots"].items():
        m = mult[e]
        if a_part_T[e] % m or b_part_T[e] % m:
            mism += 1000
        for root in rl:
            v = a_part_T[e] // m + b_part_T[e] // m
            if pub[root]["membership"] != v or \
               pub[root]["singleton_type_covers"] != a_part_T[e] // m or \
               pub[root]["six_pair_type_covers"] != b_part_T[e] // m:
                mism += 1
    check("enum11.pub_memberships_757", mism == 0, mism)

    # ---- formula vs enumeration on a targeted type-pair sample
    pm = base.PmLazy(edge_w, r)
    base.STATE_CAP = 4_000_000
    base.BUDGET_SECONDS = 600.0

    def joint_formula(e1, e2):
        rows = sorted(set(e1) | set(e2))
        shared = len(rows) == 3
        rmask = 0
        for x in rows:
            rmask |= 1 << x
        mask_e = full & ~rmask
        if shared:
            ja = 0
            jb = pm.get(mask_e)
        else:
            ja = 0
            for s in range(r):
                if w1[s] and not (rmask >> s) & 1:
                    ja += w1[s] * pm.get(mask_e ^ (1 << s))
            jb = 0
            for z in range(r):
                if (rmask >> z) & 1:
                    continue
                W = 0
                for d in rows:
                    W += edge_w.get((min(d, z), max(d, z)), 0)
                if W:
                    jb += W * pm.get(mask_e ^ (1 << z))
            for d in range(r):
                if (rmask >> d) & 1:
                    continue
                dbit = 1 << d
                for x2 in range(r):
                    if (rmask >> x2) & 1 or x2 == d:
                        continue
                    wa = edge_w.get((min(d, x2), max(d, x2)), 0)
                    if not wa:
                        continue
                    for y2 in range(x2 + 1, r):
                        if (rmask >> y2) & 1 or y2 == d:
                            continue
                        wb = edge_w.get((min(d, y2), max(d, y2)), 0)
                        if wb:
                            jb += wa * wb * pm.get(mask_e ^ dbit ^ (1 << x2)
                                                   ^ (1 << y2))
        return ja, jb, shared

    # sample: all 45 combos of the top-10 pair roots by membership (derived
    # from our own enumeration, then matched against the published top-10),
    # every shared-row pair among those types, plus 30 deterministic extras.
    root_mem = {}
    for root, s in root_row.items():
        root_mem[root] = sing_covers_by_row[s]
    for e, rl in P["pair_roots"].items():
        m = mult[e]
        v = (a_part_T[e] + b_part_T[e]) // m
        for root in rl:
            root_mem[root] = v
    by_mem = sorted(root_mem, key=lambda x: (-root_mem[x], x))
    top10_roots = by_mem[:10]
    type_of = {}
    for e, rl in P["pair_roots"].items():
        for root in rl:
            type_of[root] = e
    is_pair = set(type_of)
    check("enum11.top10_all_pair_roots",
          all(x in is_pair for x in top10_roots),
          [x for x in top10_roots if x not in is_pair])
    elim11 = json.loads(base.read_pinned(ELIM11_REL, ELIM11_PIN))
    pub_top = elim11["derived"]["top10_joint_membership"]
    pub_top_roots = {pub_top[0]["a"], pub_top[0]["b"]}
    for rec in pub_top[1:]:
        pub_top_roots.add(rec["a"])
        pub_top_roots.add(rec["b"])
    check("enum11.top10_match_published",
          set(top10_roots) == pub_top_roots,
          sorted(set(top10_roots) ^ pub_top_roots))
    top_types = [type_of[x] for x in top10_roots]
    sample = list(combinations(range(10), 2))
    tp = set()
    for i, j in sample:
        tp.add((top_types[i], top_types[j]) if top_types[i] < top_types[j]
               else (top_types[j], top_types[i]))
    # every shared-row pair among top-10 types
    for i in range(10):
        for j in range(i + 1, 10):
            e1, e2 = top_types[i], top_types[j]
            if len(set(e1) | set(e2)) == 3:
                tp.add((e1, e2) if e1 < e2 else (e2, e1))
    # 30 deterministic extras spread over the type list
    all_types = sorted(P["pair_roots"])
    for n in range(30):
        e1 = all_types[(n * 7) % len(all_types)]
        e2 = all_types[(n * 11 + 3) % len(all_types)]
        if e1 == e2:
            continue
        tp.add((e1, e2) if e1 < e2 else (e2, e1))
    mismA = mismB = 0
    for e1, e2 in sorted(tp):
        ja, jb, shared = joint_formula(e1, e2)
        key = (e1, e2)
        if ja != joint_A_T.get(key, 0):
            mismA += 1
            print("A-MISMATCH", key, ja, joint_A_T.get(key, 0))
        if jb != joint_B_T.get(key, 0):
            mismB += 1
            print("B-MISMATCH", key, jb, joint_B_T.get(key, 0))
    check("enum11.formula_joint_A_sample", mismA == 0,
          {"pairs": len(tp), "mismatches": mismA})
    check("enum11.formula_joint_B_sample", mismB == 0,
          {"pairs": len(tp), "mismatches": mismB})
    check("enum11.shared_pairs_in_sample",
          any(len(set(top_types[i]) | set(top_types[j])) == 3
              for i in range(10) for j in range(i + 1, 10)), "")

    # ---- published 45 top-10 root-level joints
    mism = 0
    for rec in pub_top:
        e1 = type_of[rec["a"]]
        e2 = type_of[rec["b"]]
        key = (e1, e2) if e1 < e2 else (e2, e1)
        m = mult[e1] * mult[e2]
        vA = joint_A_T.get(key, 0)
        vB = joint_B_T.get(key, 0)
        if (vA + vB) % m or (vA + vB) // m != rec["joint_membership"]:
            mism += 1
            print("TOP10-JOINT MISMATCH", key, (vA + vB) // m,
                  rec["joint_membership"])
        if root_mem[rec["a"]] != rec["membership_a"] or \
           root_mem[rec["b"]] != rec["membership_b"]:
            mism += 1
    check("enum11.pub_top10_45_joints", mism == 0, mism)

    out = {
        "schema": "n11-cost16-top10-joint-validate11-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Formula validation for pair-root joint membership on the "
                  "11-row parent: full explicit enumeration vs the "
                  "2-type a/b formula"),
        "derived": {
            "total_minimum_covers": total,
            "type_A_total": A_total,
            "type_B_total": B_total,
            "sample_pairs_checked": len(tp),
            "mismatch_A": mismA,
            "mismatch_B": mismB,
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all(c["pass"] for c in checks),
        "interpretation_guard": ("Cover-plan combinatorics only. Membership "
                                 "and joint counts are alternative-cover "
                                 "counts, not search cost and not verdicts. "
                                 "REFUTED-D10 and STERILE are not LOSS "
                                 "proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots "
                           "{49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 "
                           "remain UNKNOWN."),
    }
    print("validate11 all_pass:", out["all_pass"])
    return out


def joint_pair(P, pm, e1, e2):
    edge_w = P["edge_w"]
    r = len(P["target"])
    full = (1 << r) - 1
    w1 = {s: len(rl) for s, rl in P["singleton_roots"].items()}
    for s in range(r):
        w1.setdefault(s, 0)
    rows = sorted(set(e1) | set(e2))
    shared = len(rows) == 3
    rmask = 0
    for x in rows:
        rmask |= 1 << x
    mask_e = full & ~rmask
    if shared:
        ja = 0
        jb = pm.get(mask_e)
    else:
        ja = 0
        for s in range(r):
            if w1[s] and not (rmask >> s) & 1:
                ja += w1[s] * pm.get(mask_e ^ (1 << s))
        jb = 0
        for z in range(r):
            if (rmask >> z) & 1:
                continue
            W = 0
            for d in rows:
                W += edge_w.get((min(d, z), max(d, z)), 0)
            if W:
                jb += W * pm.get(mask_e ^ (1 << z))
        for d in range(r):
            if (rmask >> d) & 1:
                continue
            dbit = 1 << d
            for x2 in range(r):
                if (rmask >> x2) & 1 or x2 == d:
                    continue
                wa = edge_w.get((min(d, x2), max(d, x2)), 0)
                if not wa:
                    continue
                for y2 in range(x2 + 1, r):
                    if (rmask >> y2) & 1 or y2 == d:
                        continue
                    wb = edge_w.get((min(d, y2), max(d, y2)), 0)
                    if wb:
                        jb += wa * wb * pm.get(mask_e ^ dbit ^ (1 << x2)
                                               ^ (1 << y2))
    return ja, jb, shared


def top10_list():
    agg = json.loads(base.read_pinned(GROUPS_AGG_REL, GROUPS_AGG_PIN))
    top = [x for x in agg["derived"]["top50_by_membership"]
           if x["kind"] == "pair"][:10]
    assert len(top) == 10
    for x in top:
        assert x["rows_covered"] == sorted(x["rows_covered"])
    memA = agg["derived"]["membership_A_part_pair_roots"]
    memB = agg["derived"]["membership_B_part_pair_roots"]
    for x in top:
        x["a_part"] = memA[x["root"]]
        x["b_part"] = memB[x["root"]]
        x["membership"] = x["a_part"] + x["b_part"]
    return agg, top


def mode_joints(frm, to, budget):
    agg, top = top10_list()
    P, tbl = load_parent(TARGET)
    r, k = len(P["target"]), tbl["witness_size"]
    assert r == 31 and k == 16 and tbl["exact"]
    combos = [(i, j) for i, j in combinations(range(10), 2)]
    if to > len(combos):
        to = len(combos)
    done = set()
    if os.path.exists(JOINTS_JSONL):
        with open(JOINTS_JSONL) as f:
            for line in f:
                e = json.loads(line)
                if not e.get("summary"):
                    done.add((e["idx_i"], e["idx_j"]))
    todo = [c for c in combos[frm:to] if c not in done]
    print("[joints] slice [%d:%d) todo %d (done %d)"
          % (frm, to, len(todo), len(done)), flush=True)
    if not todo:
        return 0
    base.STATE_CAP = 16_000_000
    base.BUDGET_SECONDS = budget
    pm = base.PmLazy(P["edge_w"], r)
    t0 = time.time()
    n = 0
    for (i, j) in todo:
        x1, x2 = top[i], top[j]
        e1 = tuple(x1["rows_covered"])
        e2 = tuple(x2["rows_covered"])
        ja, jb, shared = joint_pair(P, pm, e1, e2)
        rec = {"idx_i": i, "idx_j": j, "a": x1["root"], "b": x2["root"],
               "rows_a": list(e1), "rows_b": list(e2),
               "shared_row": shared, "joint_A": ja, "joint_B": jb,
               "joint": ja + jb,
               "memo_states": len(pm.memo),
               "rss_mb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024,
               "gets": pm.gets, "sec": round(time.time() - t0, 1)}
        with open(JOINTS_JSONL, "a") as f:
            f.write(json.dumps(rec) + "\n")
        n += 1
        print("[joints] (%d,%d) roots %s/%s shared=%s A=%d B=%d memo=%d %.1fs"
              % (i, j, x1["root"][:8], x2["root"][:8], shared, ja, jb,
                 len(pm.memo), time.time() - t0), flush=True)
        if time.time() - t0 > budget:
            print("[joints] budget hit after %d joints" % n, flush=True)
            break
    with open(JOINTS_JSONL, "a") as f:
        f.write(json.dumps({"summary": True, "slice": [frm, to],
                            "computed": n,
                            "remaining_in_slice": len(todo) - n,
                            "memo_states_final": len(pm.memo),
                            "gets": pm.gets,
                            "seconds": round(time.time() - t0, 1)}) + "\n")
    print("[joints] slice done: computed %d remaining %d memo %d"
          % (n, len(todo) - n, len(pm.memo)))
    return 0


def mode_aggregate():
    agg, top = top10_list()
    P, tbl = load_parent(TARGET)
    r, k = len(P["target"]), tbl["witness_size"]
    assert r == 31 and k == 16 and tbl["exact"]
    recs = {}
    summaries = []
    with open(JOINTS_JSONL) as f:
        for line in f:
            e = json.loads(line)
            if e.get("summary"):
                summaries.append(e)
            else:
                key = (e["idx_i"], e["idx_j"])
                if key in recs:
                    raise SystemExit("duplicate joint record %s" % (key,))
                recs[key] = e
    checks = []

    def check(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok),
                       "detail": detail if isinstance(detail, str)
                       else json.dumps(detail)})
        print(("PASS " if ok else "FAIL ") + name, flush=True)

    combos = list(combinations(range(10), 2))
    check("joints.count", len(recs) == len(combos) == 45, len(recs))
    check("joints.combos_match",
          set(recs) == set(combos), len(set(recs) ^ set(combos)))
    ok_pair = all(recs[c]["a"] == top[c[0]]["root"] and
                  recs[c]["b"] == top[c[1]]["root"] for c in combos)
    check("joints.root_match_top10", ok_pair)
    shared_seen = [c for c in combos if recs[c]["shared_row"]]
    check("joints.shared_rows_present",
          len(shared_seen) > 0, len(shared_seen))
    ok = True
    for c in combos:
        e = recs[c]
        x1, x2 = top[c[0]], top[c[1]]
        if e["joint"] != e["joint_A"] + e["joint_B"]:
            ok = False
        if e["joint"] > min(x1["membership"], x2["membership"]):
            ok = False
        if e["shared_row"]:
            if e["joint_A"] != 0:
                ok = False
            if e["joint_B"] > min(x1["b_part"], x2["b_part"]):
                ok = False
        else:
            if e["joint_A"] > min(x1["a_part"], x2["a_part"]) or \
               e["joint_B"] > min(x1["b_part"], x2["b_part"]):
                ok = False
    check("joints.bounds_and_splits", ok)
    # per-root mate-capacity upper bound:
    # sum_{other in top10} joint(x, other) <= 14*a_part + 15*b_part
    ok = True
    for i in range(10):
        s = 0
        for j in range(10):
            if i == j:
                continue
            c = (min(i, j), max(i, j))
            s += recs[c]["joint"]
        cap = 14 * top[i]["a_part"] + 15 * top[i]["b_part"]
        if s > cap:
            ok = False
            print("CAP FAIL", i, s, cap)
    check("joints.mate_capacity_bound", ok)
    # exact survival points
    total = agg["derived"]["total_minimum_covers"]
    m1 = top[0]["membership"]
    joint12 = recs[(0, 1)]["joint"]
    m2 = top[1]["membership"]
    kill1 = m1
    kill2 = m1 + m2 - joint12
    check("survival.k1", 0 < kill1 < total,
          {"killed": str(kill1), "total": str(total)})
    check("survival.k2", kill1 < kill2 < total and kill2 <= m1 + m2,
          {"killed": str(kill2), "total": str(total)})
    by_joint = sorted((recs[c]["joint"], c) for c in combos)
    out = {
        "schema": "n11-cost16-top10-joint-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Exact top-10 joint memberships (45 combinations, A/B "
                  "split) for the 31-row cost-16 parent "
                  "00000000000000003800000008001000"),
        "inputs": {
            "cover_table": {"path": COVER_TABLE_REL,
                            "git_blob_sha1": COVER_TABLE_PIN},
            "phase_a_output": {"path": ("research/experiments/n11-head1410-"
                                        "partial-parent-nonsterile-children-"
                                        "20261118/output/"
                                        "cost16-a-phase-20261118.json"),
                               "git_blob_sha1": PHASE_A_PIN},
            "phase_b_groups_aggregate": {"path": GROUPS_AGG_REL,
                                         "git_blob_sha1": GROUPS_AGG_PIN},
            "candidate_roots": {"path":
                                "(regenerated) output/global-candidate-"
                                "roots-20261118.jsonl",
                                "regenerated_by":
                                "enumerate_global_candidate_roots_20261118.py"},
        },
        "method": ("2-type generalization of the published 1-type a_part/"
                   "b_part closed forms; validated against full explicit "
                   "enumeration on the 11-row parent (mode validate11). "
                   "Shared-row pairs: joint_A=0 (A-covers cover each row "
                   "exactly once) and joint_B=pm(V minus the 3 union rows) "
                   "(the shared row is the forced doubly-covered row). "
                   "pm values are memo-history independent."),
        "derived": {
            "top10": top,
            "joints": [{k: v for k, v in recs[c].items()
                        if k not in ("sec", "rss_mb", "gets", "memo_states")}
                       for c in combos],
            "shared_row_pairs": [list(c) for c in shared_seen],
            "joint_max": {"joint": by_joint[-1][0], "combo": list(by_joint[-1][1])},
            "joint_min": {"joint": by_joint[0][0], "combo": list(by_joint[0][1])},
            "exact_survival_points": {
                "k1_killed": kill1,
                "k1_share": kill1 / total,
                "k2_killed": kill2,
                "k2_share": kill2 / total,
                "k2_joint12": joint12,
            },
            "group_summaries": summaries,
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all(c["pass"] for c in checks),
        "interpretation_guard": ("Cover-plan combinatorics only. Joint "
                                 "memberships count covers containing both "
                                 "roots; they are not search cost and not "
                                 "verdicts. REFUTED-D10 and STERILE are not "
                                 "LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots "
                           "{49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 "
                           "remain UNKNOWN."),
    }
    print("aggregate all_pass:", out["all_pass"])
    with open(os.path.join(HERE, "output",
                           "cost16-top10-joint-20261118.json"), "w") as f:
        json.dump(out, f, sort_keys=True, indent=1)
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "validate11":
        out = mode_validate11()
        with open(os.path.join(HERE, "output",
                               "cost16-top10-joint-validate11-20261118.json"),
                  "w") as f:
            json.dump(out, f, sort_keys=True, indent=1)
        return 0 if out["all_pass"] else 1
    if mode == "joints":
        frm = int(sys.argv[2])
        to = int(sys.argv[3])
        budget = float(sys.argv[4]) if len(sys.argv) > 4 else 85.0
        return mode_joints(frm, to, budget)
    if mode == "aggregate":
        out = mode_aggregate()
        return 0 if out["all_pass"] else 1
    print("usage: validate11 | joints FROM TO [BUDGET] | aggregate")
    return 2


if __name__ == "__main__":
    sys.exit(main())
