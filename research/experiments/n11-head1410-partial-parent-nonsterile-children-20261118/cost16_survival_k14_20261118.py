#!/usr/bin/env python3
"""Survival-curve extension to k=14 for the 31-row cost-16 parent
00000000000000003800000008001000.

k=14 crosses the hub boundary: rank-14 root (0,15) is the first top
root without hub row 18/19, so the I-E machinery of the k=1..13
publication (commit 3a1b9481) no longer truncates at triples:

  * 25 of the 78 new triples are pairwise disjoint -> they have an
    A-type 3-way term j3_A = sum_{s not in union} w1[s] * pm(V \\ union
    \\ {s}) and a two-case B-type term (doubled row inside / outside
    the union);
  * 99 of the 286 new quads (all containing rank-14) have exactly one
    doubly-covered row -> B-type-only j4_B = pm(V \\ union); j4_A = 0
    (a doubled row forbids A-type);
  * hub-only quads remain structurally invalid (verified for all 715),
    and ALL 2,002 5-subsets of the top-14 are structurally invalid
    (>= 4 hub roots -> a hub row covered 3x or both hubs doubled), so
    the I-E still terminates at quads:
      kill(k) = sum m - sum j2 + sum j3 - sum j4   (k <= 14)
      kill_A(k) = sum a - sum j2_A + sum j3_A        (j4_A == 0)
      kill_B(k) = sum b - sum j2_B + sum j3_B - sum j4_B

Anchors and cross-checks inside this script:

  * the generalized disjoint formula (written for arbitrary disjoint
    root sets) is anchored on published pairwise joints: evaluated on
    the union of a published disjoint PAIR it must reproduce the
    pinned joint values exactly (both pm lineages);
  * 2 disjoint triples and 2 quads recomputed with the second pm
    lineage (MyPm) must agree with the primary (PmLazy) values;
  * kill(k) for k=1..13 recomputed from the full k=14 machinery must
    reproduce the pinned k=13 publication exactly.

Cover-plan combinatorics only.  No engine run, no verdict.

Usage:
  python3 cost16_survival_k14_20261118.py pairs [BUDGET]
  python3 cost16_survival_k14_20261118.py triples [SLICE]
  python3 cost16_survival_k14_20261118.py quads [SLICE]
  python3 cost16_survival_k14_20261118.py cross
  python3 cost16_survival_k14_20261118.py finalize
"""
import hashlib
import itertools
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
import cost16_parent_membership_20261118 as base
import cost16_top10_joint_20261118 as tj
import cost16_survival_k10_20261118 as k10s
import cost16_survival_k13_20261118 as k13m

TARGET = "00000000000000003800000008001000"
K = 14
R = 31
IDX14 = 13

EXP_REL = ("research/experiments/n11-head1410-partial-parent-"
           "nonsterile-children-20261118/output/")
GROUPS_AGG_REL = EXP_REL + "cost16-b-phase-groups-20261118.json"
GROUPS_AGG_PIN = "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87"
K13_JSON_REL = EXP_REL + "cost16-survival-k13-20261118.json"
K13_JSON_PIN = "bcf680f7529a119223f362099ed89685b9e37db6"
K13_JSON_COMMIT = "3a1b9481"
RES_JSONL = os.path.join(HERE, "output",
                         "cost16-survival-k14-20261118.jsonl")
RES_JSON = os.path.join(HERE, "output",
                        "cost16-survival-k14-20261118.json")


class PmGet:
    """Adapter: MyPm.count -> .get interface."""

    def __init__(self, pm):
        self.pm = pm

    def get(self, mask):
        return self.pm.count(mask)


def load_top14():
    agg = json.loads(base.read_pinned(GROUPS_AGG_REL, GROUPS_AGG_PIN))
    top = agg["derived"]["top50_by_membership"][:K]
    assert all(e["kind"] == "pair" for e in top)
    memA = agg["derived"]["membership_A_part_pair_roots"]
    memB = agg["derived"]["membership_B_part_pair_roots"]
    for e in top:
        assert memA[e["root"]] + memB[e["root"]] == e["membership"]
    assert not (18 in top[IDX14]["rows_covered"]
                or 19 in top[IDX14]["rows_covered"])
    assert all(18 in e["rows_covered"] or 19 in e["rows_covered"]
               for e in top[:IDX14])
    total = agg["derived"]["total_minimum_covers"]
    A16 = agg["derived"]["type_A_disjoint"]
    B16 = agg["derived"]["type_B_one_duplicate_row"]
    return agg, top, memA, memB, total, A16, B16


def load_k13_pairs_triples():
    """All 78 pairwise joints and 286 triples among the top-13, from
    the pinned publications."""
    k13 = json.loads(base.read_pinned(K13_JSON_REL, K13_JSON_PIN))
    pairs = {}
    for c, v in k13["values"]["new_pair_joints"].items():
        i, j = (int(x) for x in c.split(","))
        pairs[(i, j)] = {"A": int(v["joint_A"]),
                         "B": int(v["joint_B"]),
                         "joint": int(v["joint"]),
                         "shared": v["shared_row"]}
    pubj = k13m.load_pub_joints()
    for (i, j), e in pubj.items():
        pairs[(i, j)] = {"A": e["joint_A"], "B": e["joint_B"],
                         "joint": e["joint"],
                         "shared": e["shared_row"]}
    assert len(pairs) == 78
    triples = {}
    # k13 JSON keys "%d%d%d" are ambiguous for indices >= 10; parse
    # by enumeration (verified collision-free: all 286 combos map to
    # distinct keys) instead of char-by-char.
    k10 = k13m.load_k10()
    pub3 = set()
    for key, v in k10["values"]["triples"].items():
        c = tuple(int(ch) for ch in key)
        assert len(key) == 3 and all(x < 10 for x in c)
        pub3.add(c)
        triples[c] = {"class": v["class"], "joint": int(v["joint"])}
    new3 = {("%d%d%d" % c): c for c in itertools.combinations(
        range(13), 3) if c not in pub3}
    assert len(new3) == 166
    assert set(new3) == set(k13["values"]["new_triples"])
    for key, v in k13["values"]["new_triples"].items():
        c = new3[key]
        triples[c] = {"class": v["class"], "joint": int(v["joint"])}
    assert len(triples) == 286
    return k13, pairs, triples


def mults(rows, combo):
    c = {}
    for i in combo:
        for r in rows[i]:
            c[r] = c.get(r, 0) + 1
    return c


def classify(rows, combo):
    """(kind, union) for an arbitrary subset of roots:
    'b_only'  -> exactly one doubly-covered row (B-type-only term)
    'zero'    -> >=3x row or two 2x rows (structurally impossible)
    'disjoint'-> all rows distinct (A-type possible)
    """
    c = mults(rows, combo)
    if max(c.values()) >= 3:
        return "zero", sorted(c)
    twos = [r for r, v in c.items() if v == 2]
    if len(twos) >= 2:
        return "zero", sorted(c)
    if len(twos) == 1:
        return "b_only", sorted(c)
    return "disjoint", sorted(c)


def disjoint_joint(edge_w, pmget, w1, union):
    """Exact joint kill of a set of pairwise-disjoint banned roots,
    split by cover type.  Valid for pairs (|union|=4) AND triples
    (|union|=6): anchored on published pairs.

    A-type: all rows once + one singleton root on row s outside the
    union: jA = sum_{s} w1[s] * pm(V\\union\\{s}).
    B-type (one doubly-covered row d):
      d in union: one extra root (d,a), a outside union; the rest is a
        perfect matching on mask\\{a}: sum_a W(a) pm(mask\\{a}) with
        W(a) = sum_{d in union} w(d,a);
      d outside: two extra roots (d,a),(d,b); matching on
        mask\\{d,a,b}: sum_{d,a<b} w(d,a) w(d,b) pm(mask\\{d,a,b}).
    """
    full = (1 << R) - 1
    rmask = 0
    for x in union:
        rmask |= 1 << x
    mask = full & ~rmask
    ja = 0
    for s in range(R):
        if w1.get(s) and not (rmask >> s) & 1:
            ja += w1[s] * pmget.get(mask ^ (1 << s))
    jb = 0
    for a in range(R):
        if (rmask >> a) & 1:
            continue
        W = 0
        for z in union:
            W += edge_w.get((min(z, a), max(z, a)), 0)
        if W:
            jb += W * pmget.get(mask ^ (1 << a))
    for d in range(R):
        if (rmask >> d) & 1:
            continue
        cand = [x for x in range(R)
                if x != d and not (rmask >> x) & 1
                and edge_w.get((min(x, d), max(x, d)))]
        for i1 in range(len(cand)):
            a = cand[i1]
            wa = edge_w[(min(a, d), max(a, d))]
            for i2 in range(i1 + 1, len(cand)):
                b = cand[i2]
                wb = edge_w[(min(b, d), max(b, d))]
                jb += (wa * wb
                       * pmget.get(mask ^ (1 << d) ^ (1 << a)
                                  ^ (1 << b)))
    return ja, jb


def append(rec):
    with open(RES_JSONL, "a") as f:
        f.write(json.dumps(rec) + "\n")


def done(kind, keyfmt):
    out = {}
    if os.path.exists(RES_JSONL):
        with open(RES_JSONL) as f:
            for line in f:
                e = json.loads(line)
                if e.get("kind") == kind:
                    out[keyfmt(e)] = e
    return out


def new_pair_combos():
    return [(i, IDX14) for i in range(IDX14)]


def new_triple_combos():
    return [(IDX14, i, j) for i, j in
            itertools.combinations(range(IDX14), 2)]


def new_quad_combos():
    return [(IDX14, i, j, l) for i, j, l in
            itertools.combinations(range(IDX14), 3)]


def get_parent():
    P, tbl = tj.load_parent(TARGET)
    assert len(P["target"]) == R and tbl["witness_size"] == 16
    assert tbl["exact"] and len(P["pair_roots"]) == 425
    return P


def w1_map(P):
    return {s: len(rl) for s, rl in P["singleton_roots"].items()}


def mode_pairs(budget):
    agg, top, memA, memB, total, A16, B16 = load_top14()
    P = get_parent()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    base.STATE_CAP = 16_000_000
    base.BUDGET_SECONDS = budget
    pm = base.PmLazy(P["edge_w"], R)
    donep = done("pair", lambda e: (e["idx_i"], e["idx_j"]))
    todo = [c for c in new_pair_combos() if c not in donep]
    print("[pairs] todo %d (done %d/13)" % (len(todo), len(donep)),
          flush=True)
    t0 = time.time()
    n = 0
    for (i, j) in todo:
        e1 = rows[i]
        e2 = rows[j]
        ja, jb, shared = tj.joint_pair(P, pm, e1, e2)
        append({"kind": "pair", "idx_i": i, "idx_j": j,
                "shared_row": shared, "joint_A": ja, "joint_B": jb,
                "joint": ja + jb, "memo_states": len(pm.memo),
                "sec": round(time.time() - t0, 1)})
        n += 1
        print("[pairs] (%d,%d) shared=%s A=%d B=%d memo=%d %.1fs"
              % (i, j, shared, ja, jb, len(pm.memo), time.time() - t0),
              flush=True)
    print("[pairs] done %d/13" % len(done("pair",
           lambda e: (e["idx_i"], e["idx_j"]))), flush=True)
    return 0


def mode_triples(slice_arg):
    agg, top, memA, memB, total, A16, B16 = load_top14()
    P = get_parent()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    combos = new_triple_combos()
    assert len(combos) == 78
    lo = slice_arg * 40
    hi = min(lo + 40, len(combos))
    donet = done("triple", lambda e: tuple(e["combo"]))
    pm = None
    t00 = time.time()
    for combo in combos[lo:hi]:
        if combo in donet:
            continue
        kind, union = classify(rows, combo)
        if kind == "zero":
            append({"kind": "triple", "combo": list(combo),
                    "class": "zero", "union": union,
                    "joint_A": 0, "joint_B": 0, "joint": 0})
            print("[tzero %s] -> 0" % (combo,), flush=True)
            continue
        if kind == "b_only":
            pmf = k10s.MyPm(P["edge_w"], R)
            t0 = time.time()
            mask = (1 << R) - 1
            for u in union:
                mask &= ~(1 << u)
            val = pmf.count(mask)
            append({"kind": "triple", "combo": list(combo),
                    "class": "b_only", "union": union,
                    "joint_A": 0, "joint_B": val, "joint": val,
                    "memo_states": len(pmf.memo),
                    "sec": round(time.time() - t0, 1)})
            print("[b_only %s] union=%s j3B=%d %.1fs"
                  % (combo, union, val, time.time() - t0), flush=True)
            continue
        # disjoint: 3-way A term + two-case B term (shared PmLazy)
        if pm is None:
            base.STATE_CAP = 16_000_000
            base.BUDGET_SECONDS = 900.0
            pm = base.PmLazy(P["edge_w"], R)
            w1 = w1_map(P)
        t0 = time.time()
        ja, jb = disjoint_joint(P["edge_w"], pm, w1, union)
        append({"kind": "triple", "combo": list(combo),
                "class": "disjoint", "union": union,
                "joint_A": ja, "joint_B": jb, "joint": ja + jb,
                "memo_states": len(pm.memo),
                "sec": round(time.time() - t0, 1)})
        print("[disjoint %s] union=%s A=%d B=%d memo=%d %.1fs"
              % (combo, union, ja, jb, len(pm.memo), time.time() - t0),
              flush=True)
    print("[triples] slice %d done, done %d/78 in %.1fs"
          % (slice_arg, len(done("triple", lambda e: tuple(e["combo"]))),
             time.time() - t00), flush=True)
    return 0


def mode_quads(slice_arg):
    agg, top, memA, memB, total, A16, B16 = load_top14()
    P = get_parent()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    combos = new_quad_combos()
    assert len(combos) == 286
    lo = slice_arg * 60
    hi = min(lo + 60, len(combos))
    doneq = done("quad", lambda e: tuple(e["combo"]))
    t00 = time.time()
    n = 0
    for combo in combos[lo:hi]:
        if combo in doneq:
            continue
        kind, union = classify(rows, combo)
        assert kind != "disjoint", combo
        if kind == "zero":
            append({"kind": "quad", "combo": list(combo),
                    "class": "zero", "union": union, "joint": 0})
            continue
        pmf = k10s.MyPm(P["edge_w"], R)
        t0 = time.time()
        mask = (1 << R) - 1
        for u in union:
            mask &= ~(1 << u)
        val = pmf.count(mask)
        append({"kind": "quad", "combo": list(combo),
                "class": "b_only", "union": union, "joint": val,
                "memo_states": len(pmf.memo),
                "sec": round(time.time() - t0, 1)})
        n += 1
        print("[quad b_only %s] union=%s j4B=%d %.1fs"
              % (combo, union, val, time.time() - t0), flush=True)
        if time.time() - t00 > 240:
            print("[quads] budget hit at %d computed" % n, flush=True)
            break
    print("[quads] slice %d done, done %d/286"
          % (slice_arg, len(done("quad", lambda e: tuple(e["combo"])))),
          flush=True)
    return 0


def mode_cross():
    """Anchor the generalized disjoint formula on published pair
    joints (both lineages), then cross-check 2 disjoint triples and 2
    quads across lineages."""
    agg, top, memA, memB, total, A16, B16 = load_top14()
    P = get_parent()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    edge_w = P["edge_w"]
    w1 = w1_map(P)
    _, pairs13, _ = load_k13_pairs_triples()
    nbad = 0
    # anchor: disjoint published pairs (0,1) and (4,8)
    for (i, j) in [(0, 1), (4, 8)]:
        union = sorted(set(rows[i]) | set(rows[j]))
        ref = pairs13[(i, j)]
        for lineage, pmg in [
                ("lazypm", base.PmLazy(edge_w, R)),
                ("mypm", PmGet(k10s.MyPm(edge_w, R)))]:
            base.STATE_CAP = 16_000_000
            base.BUDGET_SECONDS = 900.0
            t0 = time.time()
            ja, jb = disjoint_joint(edge_w, pmg, w1, union)
            match = (ja == ref["A"] and jb == ref["B"])
            append({"kind": "anchor2", "idx_i": i, "idx_j": j,
                    "lineage": lineage, "joint_A": ja, "joint_B": jb,
                    "ref_A": ref["A"], "ref_B": ref["B"],
                    "match": match})
            print("[anchor2 %s (%d,%d)] A=%d B=%d ref A=%d B=%d"
                  " match=%s %.1fs"
                  % (lineage, i, j, ja, jb, ref["A"], ref["B"],
                     match, time.time() - t0), flush=True)
            if not match:
                nbad += 1
    # cross: 2 disjoint triples, both lineages
    tri = done("triple", lambda e: tuple(e["combo"]))
    for combo in [(IDX14, 1, 2), (IDX14, 5, 9)]:
        ref = tri[combo]
        union = sorted(set().union(*[set(rows[i]) for i in combo]))
        for lineage, pmg in [
                ("mypm", PmGet(k10s.MyPm(edge_w, R)))]:
            t0 = time.time()
            ja, jb = disjoint_joint(edge_w, pmg, w1, union)
            match = (ja == ref["joint_A"] and jb == ref["joint_B"])
            append({"kind": "cross3", "combo": list(combo),
                    "lineage": lineage, "joint_A": ja, "joint_B": jb,
                    "ref_A": ref["joint_A"], "ref_B": ref["joint_B"],
                    "match": match})
            print("[cross3 %s %s] A=%d B=%d ref A=%d B=%d match=%s"
                  " %.1fs" % (lineage, combo, ja, jb, ref["joint_A"],
                              ref["joint_B"], match, time.time() - t0),
                  flush=True)
            if not match:
                nbad += 1
    # cross: 2 quads, MyPm vs stored (primary MyPm already; use
    # PmLazy as the second lineage)
    quad = done("quad", lambda e: tuple(e["combo"]))
    for combo in [c for c in new_quad_combos()
                  if c in quad and quad[c]["class"] == "b_only"][:2]:
        ref = quad[combo]
        union = ref["union"]
        base.STATE_CAP = 16_000_000
        base.BUDGET_SECONDS = 900.0
        pmg = base.PmLazy(edge_w, R)
        t0 = time.time()
        mask = (1 << R) - 1
        for u in union:
            mask &= ~(1 << u)
        val = pmg.get(mask)
        match = (val == ref["joint"])
        append({"kind": "cross4", "combo": list(combo),
                "lineage": "lazypm", "joint": val,
                "ref": ref["joint"], "match": match})
        print("[cross4 %s] j4=%d ref=%d match=%s %.1fs"
              % (combo, val, ref["joint"], match, time.time() - t0),
              flush=True)
        if not match:
            nbad += 1
    print("[cross] mismatches %d" % nbad, flush=True)
    return 0 if nbad == 0 else 1


def finalize_mode():
    checks = []

    def chk(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok), "detail": detail})
        print(("PASS " if ok else "FAIL ") + name, flush=True)

    agg, top, memA, memB, total, A16, B16 = load_top14()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    mem = [e["membership"] for e in top]
    ap = [memA[e["root"]] for e in top]
    bp = [memB[e["root"]] for e in top]
    k13, pairs13, triples13 = load_k13_pairs_triples()
    dones = {kind: done(kind, key) for kind, key in [
        ("pair", lambda e: (e["idx_i"], e["idx_j"])),
        ("triple", lambda e: tuple(e["combo"])),
        ("quad", lambda e: tuple(e["combo"])),
        ("anchor2", lambda e: (e["idx_i"], e["idx_j"], e["lineage"])),
        ("cross3", lambda e: (tuple(e["combo"]), e["lineage"])),
        ("cross4", lambda e: (tuple(e["combo"]), e["lineage"])),
    ]}

    # ---- assemble all pairwise joints (91) and triples (364)
    j2 = dict(pairs13)
    chk("pairs.published_78", len(pairs13) == 78)
    chk("pairs.new_13", len(dones["pair"]) == 13)
    for c, e in dones["pair"].items():
        j2[c] = {"A": e["joint_A"], "B": e["joint_B"],
                 "joint": e["joint"], "shared": e["shared_row"]}
    chk("pairs.complete_91", len(j2) == 91)
    chk("pairs.bounds", all(
        j2[c]["joint"] <= min(mem[c[0]], mem[c[1]])
        and j2[c]["A"] <= min(ap[c[0]], ap[c[1]])
        and j2[c]["B"] <= min(bp[c[0]], bp[c[1]]) for c in j2))
    shared_new = [c for c in dones["pair"]
                 if dones["pair"][c]["shared_row"]]
    chk("pairs.new_census_2shared_11disjoint",
        len(shared_new) == 2 and len(dones["pair"]) - len(shared_new)
        == 11)
    chk("pairs.shared_jointA_zero", all(
        j2[c]["A"] == 0 for c in j2 if j2[c]["shared"]))

    j3 = {}
    for c, v in triples13.items():
        j3[c] = {"class": v["class"], "A": 0,
                 "B": v["joint"], "joint": v["joint"]}
    chk("triples.published_286", len(triples13) == 286)
    chk("triples.new_78", len(dones["triple"]) == 78)
    for c, e in dones["triple"].items():
        key = tuple(sorted(e["combo"]))
        j3[key] = {"class": e["class"], "A": e["joint_A"],
                   "B": e["joint_B"], "joint": e["joint"]}
    chk("triples.complete_364", len(j3) == 364)
    tri_census = {"b_only": 0, "zero": 0, "disjoint": 0}
    for c in itertools.combinations(range(K), 3):
        kind, union = classify(rows, c)
        if kind in tri_census:
            tri_census[kind] += 1
        assert j3[c]["class"] in ("b_only", "zero", "disjoint",
                                  "zero3x", "zero2x2")
        eff = ("zero" if j3[c]["class"] in ("zero", "zero3x",
                                            "zero2x2")
               else j3[c]["class"])
        assert eff == kind, (c, eff, kind)
    chk("triples.census", tri_census == {"b_only": 242, "zero": 97,
                                         "disjoint": 25}, tri_census)
    chk("triples.disjoint_A_terms", all(
        j3[c]["A"] > 0 for c in j3 if j3[c]["class"] == "disjoint"))
    chk("triples.bounds", all(
        j3[c]["joint"] <= min(j2[(c[0], c[1])]["joint"],
                              j2[(c[0], c[2])]["joint"],
                              j2[(c[1], c[2])]["joint"])
        for c in j3 if j3[c]["joint"]))

    j4 = {}
    chk("quads.new_286", len(dones["quad"]) == 286)
    for c, e in dones["quad"].items():
        key = tuple(sorted(e["combo"]))
        j4[key] = {"class": e["class"], "joint": e["joint"]}
    quad_census = {"b_only": 0, "zero": 0}
    n_hub_valid = 0
    for c in itertools.combinations(range(K), 4):
        kind, union = classify(rows, c)
        if IDX14 in c:
            quad_census[kind] += 1
            assert j4[c]["class"] == kind, (c, j4[c]["class"], kind)
        else:
            if kind != "zero":
                n_hub_valid += 1
    chk("quads.census_99b_187z", quad_census == {"b_only": 99,
                                                "zero": 187},
        quad_census)
    chk("quads.hub_only_all_zero", n_hub_valid == 0)
    n5 = 0
    n5bad = 0
    for c in itertools.combinations(range(K), 5):
        n5 += 1
        kind, _ = classify(rows, c)
        if kind != "zero":
            n5bad += 1
    chk("quints.all_zero_2002", n5 == 2002 and n5bad == 0)
    # complete the quad map: hub-only quads are structurally zero
    # (verified above), so they enter the I-E as exact zeros
    for c in itertools.combinations(range(K), 4):
        if c not in j4:
            j4[c] = {"class": "zero", "joint": 0}
    chk("quads.complete_1001", len(j4) == 1001, len(j4))

    # ---- anchors and cross-lineage
    chk("anchors.pairs_2x2lineages", len(dones["anchor2"]) == 4
        and all(e["match"] for e in dones["anchor2"].values()),
        {"checked": sorted(dones["anchor2"])})
    chk("cross.triples_2", len(dones["cross3"]) == 2
        and all(e["match"] for e in dones["cross3"].values()))
    chk("cross.quads_2", len(dones["cross4"]) == 2
        and all(e["match"] for e in dones["cross4"].values()))

    # ---- kill(k) for k=1..14 from the full machinery
    kill = {}
    killA = {}
    killB = {}
    for k in range(1, K + 1):
        v = vA = vB = 0
        for i in range(k):
            v += mem[i]
            vA += ap[i]
            vB += bp[i]
        for c in itertools.combinations(range(k), 2):
            v -= j2[c]["joint"]
            vA -= j2[c]["A"]
            vB -= j2[c]["B"]
        for c in itertools.combinations(range(k), 3):
            v += j3[c]["joint"]
            vA += j3[c]["A"]
            vB += j3[c]["B"]
        for c in itertools.combinations(range(k), 4):
            v -= j4[c]["joint"]
            vB -= j4[c]["joint"]
        kill[k] = v
        killA[k] = vA
        killB[k] = vB
        assert v == vA + vB
    chk("split.identity_per_k",
        all(kill[k] == killA[k] + killB[k] for k in range(1, K + 1)))
    chk("reproduce_k1_13",
        all(kill[k] == int(k13["values"]["kill"]["k%d" % k])
            for k in range(1, 14)),
        {"k13_mine": str(kill[13]),
         "k13_pub": k13["values"]["kill"]["k13"]})
    chk("split.reproduce_k1_13",
        all(killA[k] == int(k13["values"]["kill_A"]["k%d" % k])
            and killB[k] == int(k13["values"]["kill_B"]["k%d" % k])
            for k in range(1, 14)))
    chk("split.monotone",
        all(killA[k] <= killA[k + 1] and killB[k] <= killB[k + 1]
            for k in range(1, K)))
    chk("survival.monotone",
        all(kill[k] <= kill[k + 1] for k in range(1, K))
        and kill[K] <= total)
    chk("survival.marginal",
        0 <= kill[K] - kill[K - 1] <= mem[K - 1],
        {"k14_minus_k13": str(kill[K] - kill[K - 1]),
         "m14": str(mem[K - 1])})
    chk("survival.union_bound",
        total - kill[K] >= total - sum(mem[:K]))

    Bsurv = {k: B16 - killB[k] for k in range(1, K + 1)}
    Bsurv[0] = B16
    Asurv = {k: A16 - killA[k] for k in range(1, K + 1)}
    chk("mixed.b_survive_monotone",
        all(Bsurv[k] >= Bsurv[k + 1] for k in range(K)))
    chk("mixed.k14_value",
        Bsurv[K] == B16 - killB[K],
        {"full_singleton_ban_survive_k14": str(Bsurv[K]),
         "share": round(100 * Bsurv[K] / total, 6)})

    out = {
        "schema": "n11-cost16-survival-k14-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Exact survival curve extended to k=14 for the "
                  "31-row cost-16 parent: the rank-14 non-hub root "
                  "(0,15) activates A-type 3-way terms (25 disjoint "
                  "triples) and B-type-only 4-way terms (99 quads); "
                  "I-E verified to terminate at quads (all 2,002 "
                  "5-subsets structurally zero)"),
        "inputs": {
            "groups_aggregate": {"path": GROUPS_AGG_REL,
                                 "git_blob_sha1": GROUPS_AGG_PIN},
            "survival_k13_json": {"path": K13_JSON_REL,
                                  "git_blob_sha1": K13_JSON_PIN,
                                  "commit": K13_JSON_COMMIT},
        },
        "structure": {
            "rank14_root": {"root": top[IDX14]["root"],
                            "rows": list(rows[IDX14]),
                            "membership": str(mem[IDX14]),
                            "a_part": str(ap[IDX14]),
                            "b_part": str(bp[IDX14]),
                            "note": "first top-14 root without hub "
                                    "rows 18/19"},
            "triple_census_k14": tri_census,
            "quad_census_with_rank14": quad_census,
            "hub_only_quads_all_zero": True,
            "quints_all_zero": True,
            "ie_mechanism": ("kill(k) = sum m - sum j2 + sum j3 - "
                             "sum j4 for k <= 14; j3 gains A-type "
                             "terms only for the 25 disjoint "
                             "triples containing rank-14; j4 is "
                             "B-type-only (j4_A == 0); 5-subsets "
                             "all structurally impossible"),
            "formulas": {
                "j3_A_disjoint": "sum_{s not in union} w1[s] * "
                                 "pm(V \\ union \\ {s})",
                "j3_B_disjoint": "two-case (doubled row inside / "
                                 "outside the union), generalized "
                                 "from the published pairwise "
                                 "disjoint formula and anchored on "
                                 "published pairs",
                "j4_B_b_only": "pm(V \\ union) on the 24-row "
                               "residual",
            },
        },
        "values": {
            "total_minimum_covers": str(total),
            "type_A_total": str(A16),
            "type_B_total": str(B16),
            "kill": {("k%d" % k): str(kill[k])
                     for k in range(1, K + 1)},
            "kill_A": {("k%d" % k): str(killA[k])
                       for k in range(1, K + 1)},
            "kill_B": {("k%d" % k): str(killB[k])
                       for k in range(1, K + 1)},
            "kill_share_percent": {
                ("k%d" % k): round(100 * kill[k] / total, 6)
                for k in range(1, K + 1)},
            "marginal_k14": str(kill[K] - kill[K - 1]),
            "A_survive": {("k%d" % k): str(A16 - killA[k])
                          for k in range(1, K + 1)},
            "B_survive_full_singleton_ban": {
                ("k%d" % k): str(Bsurv[k]) for k in range(0, K + 1)},
            "B_survive_share_percent": {
                ("k%d" % k): round(100 * Bsurv[k] / total, 6)
                for k in range(0, K + 1)},
            "new_pair_joints": {
                "%d,%d" % c: {"shared_row": j2[c]["shared"],
                              "joint_A": str(j2[c]["A"]),
                              "joint_B": str(j2[c]["B"]),
                              "joint": str(j2[c]["joint"])}
                for c in sorted(dones["pair"])},
            "new_triples": {
                "%d,%d,%d" % c: {"class": j3[c]["class"],
                                 "joint_A": str(j3[c]["A"]),
                                 "joint_B": str(j3[c]["B"]),
                                 "joint": str(j3[c]["joint"])}
                for c in sorted(tuple(sorted(e["combo"]))
                                for e in dones["triple"].values())},
            "new_quads": {
                "%d,%d,%d,%d" % c: {"class": j4[c]["class"],
                                    "joint": str(j4[c]["joint"])}
                for c in sorted(tuple(sorted(e["combo"]))
                                for e in dones["quad"].values())},
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all(c["pass"] for c in checks),
        "interpretation_guard": (
            "Cover-plan combinatorics only. Survival points count "
            "minimum cover plans containing at least one banned "
            "root; they are not search costs and imply nothing about "
            "WIN/REFUTED verdicts of the banned roots. REFUTED-D10 "
            "and STERILE are not LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone "
                           "roots {49,60}/{59,60}, S2 {59,60}, and "
                           "classes 1/2/4 remain UNKNOWN."),
    }
    with open(RES_JSON, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    print(json.dumps({"checks": len(checks),
                      "all_pass": out["all_pass"],
                      "failed": [c["name"] for c in checks
                                 if not c["pass"]]}, indent=1))
    return 0 if out["all_pass"] else 1


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "pairs":
        budget = float(sys.argv[2]) if len(sys.argv) > 2 else 240.0
        return mode_pairs(budget)
    if mode == "triples":
        sl = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        return mode_triples(sl)
    if mode == "quads":
        sl = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        return mode_quads(sl)
    if mode == "cross":
        return mode_cross()
    if mode == "finalize":
        return finalize_mode()
    print("usage: pairs [BUDGET] | triples [SLICE] | quads [SLICE] | "
          "cross | finalize")
    return 2


if __name__ == "__main__":
    sys.exit(main())
