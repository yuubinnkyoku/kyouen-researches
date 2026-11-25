#!/usr/bin/env python3
"""Survival-curve extension k=11..13 with exact A/B type split for the
31-row cost-16 parent 00000000000000003800000008001000.

Extends the published exact survival curve k=1..10 (commit a59881a2,
cost16_survival_k10_20261118.py) to k=11..13 and derives, for every k,
the exact A-type / B-type decomposition of the kill.

Why the structural collapse still holds at k=13:

  * every top-13 pair root contains hub row 18 or 19 (the first
    non-hub root is rank 14 = (0,15)), verified from the pinned
    aggregate ranking;
  * hence no triple of banned roots is pairwise disjoint -> joint_A = 0
    for every triple (two roots always share a hub row, and an A-type
    cover covers each row exactly once);
  * every 4-subset has, by pigeonhole on the hub rows, a row covered
    >= 3x or two rows covered 2x -> impossible in A-type (all rows
    once) and in B-type (exactly one doubly-covered row) -> quads and
    higher vanish by monotonicity;
  * a triple with exactly one doubly-covered row is B-type-only:
    j3 = pm(V \\ union) on a 26-row set (fresh MyPm memo per triple);
    a triple with a >=3x row or two 2x rows is structurally zero.

So kill(k) = sum_i<k m_i - sum_pairs j2 + sum_triples j3 is exact for
k = 1..13, and splits exactly by type:

    kill_A(k) = sum_i<k a_i - sum_pairs joint_A          (j3_A == 0)
    kill_B(k) = sum_b b_i - sum_pairs joint_B + sum_triples j3

with a_i / b_i the pinned per-root A-part / B-part memberships of the
groups aggregate and the 45 published pairwise joints (commit 537a4458,
triple-anchored) reused verbatim; only the 33 new pairs (idx 10..12)
and 166 new triples are computed here.

Mixed-ban interpretation of the B split (full singleton ban):

  every A-type cover contains exactly one singleton root; banning ALL
  1,483 singleton roots kills every A-type plan, while B-type covers
  (16 pair roots, no singleton) are unaffected by singleton bans.  So

      B_survive(k) = B16 - kill_B(k)

  is the exact survival count under "top-k pair-root bans + full
  singleton ban", i.e. the endpoint of the published singleton-row-ban
  mixed curve (rows 4/0/24 on top of the top-10 pair bans, commit
  c98cb51d).

Validation anchors inside this script:

  * all 120 published triples recomputed from scratch (fresh MyPm) and
    matched against the pinned k=1..10 finalize JSON;
  * three published pairwise joints (2 disjoint, 1 shared-row)
    recomputed from scratch and matched against the pinned JSONL;
  * kill(k) for k=1..10 reproduced exactly from the pinned inputs;
  * the A/B split validated at k=4 and k=8 against the published
    direct per-d-slice recomputation (commit 33abfdb8).

Cover-plan combinatorics only.  No engine run, no verdict.

Usage:
  python3 cost16_survival_k13_20261118.py pairs FROM TO [BUDGET]
  python3 cost16_survival_k13_20261118.py triples [SLICE]
  python3 cost16_survival_k13_20261118.py finalize
"""
import hashlib
import itertools
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
import cost16_parent_membership_20261118 as base
import cost16_top10_joint_20261118 as tj
import cost16_survival_k10_20261118 as k10s

TARGET = "00000000000000003800000008001000"
K = 13
R = 31

EXP_REL = ("research/experiments/n11-head1410-partial-parent-"
           "nonsterile-children-20261118/output/")
GROUPS_AGG_REL = EXP_REL + "cost16-b-phase-groups-20261118.json"
GROUPS_AGG_PIN = "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87"
PUB_JOINT_JSONL_REL = EXP_REL + "cost16-top10-joint-20261118.jsonl"
PUB_JOINT_PIN = "95194096b2dcb547b5b77fb846795edbc5c43e05"
K10_JSON_REL = EXP_REL + "cost16-survival-k10-20261118.json"
K10_PIN = "6be591d458e3d9b863c070b85c0196692dfe5c6d"
BAN_JSON_REL = EXP_REL + "cost16-ban-survival-20261118.json"
BAN_SHA256 = ("21d332637e79661c0ca46b1da89388ab54b6be423313e823bce"
              "99828b944ba30")
SRB_JSON_REL = EXP_REL + "cost16-singleton-row-ban-20261118.json"
SRB_SHA256 = ("5a7c2ab6f981a33a1240f95138152e0730c03530e756944bd2"
              "7552206ec0a676")
RES_JSONL = os.path.join(HERE, "output",
                         "cost16-survival-k13-20261118.jsonl")
RES_JSON = os.path.join(HERE, "output",
                        "cost16-survival-k13-20261118.json")


def read_sha256(rel, pin):
    with open(os.path.join(ROOT, rel), "rb") as f:
        data = f.read()
    if hashlib.sha256(data).hexdigest() != pin:
        raise SystemExit("sha256 mismatch: " + rel)
    return data


def load_top():
    agg = json.loads(base.read_pinned(GROUPS_AGG_REL, GROUPS_AGG_PIN))
    top = agg["derived"]["top50_by_membership"][:K]
    assert all(e["kind"] == "pair" for e in top)
    assert all(e["rows_covered"] == sorted(e["rows_covered"]) for e in top)
    memA = agg["derived"]["membership_A_part_pair_roots"]
    memB = agg["derived"]["membership_B_part_pair_roots"]
    for e in top:
        assert memA[e["root"]] + memB[e["root"]] == e["membership"]
    total = agg["derived"]["total_minimum_covers"]
    A16 = agg["derived"]["type_A_disjoint"]
    B16 = agg["derived"]["type_B_one_duplicate_row"]
    return agg, top, memA, memB, total, A16, B16


def load_pub_joints():
    b = base.read_pinned(PUB_JOINT_JSONL_REL, PUB_JOINT_PIN)
    out = {}
    for line in b.decode().splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        if "idx_i" in e:
            out[(e["idx_i"], e["idx_j"])] = e
    assert len(out) == 45
    return out


def load_k10():
    b = base.read_pinned(K10_JSON_REL, K10_PIN)
    return json.loads(b)


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
    return [c for c in itertools.combinations(range(K), 2)
            if c[1] >= 10]


def mode_pairs(frm, to, budget):
    agg, top, memA, memB, total, A16, B16 = load_top()
    P, tbl = tj.load_parent(TARGET)
    r = len(P["target"])
    assert r == R and tbl["witness_size"] == 16 and tbl["exact"]
    assert len(P["pair_roots"]) == 425
    assert all(len(rl) == 1 for rl in P["pair_roots"].values())
    combos = new_pair_combos()
    assert len(combos) == 33
    if to > len(combos):
        to = len(combos)
    donep = done("pair", lambda e: (e["idx_i"], e["idx_j"]))
    todo = [c for c in combos[frm:to] if c not in donep]
    print("[pairs] slice [%d:%d) todo %d (done %d/33)"
          % (frm, to, len(todo), len(donep)), flush=True)
    if not todo:
        return 0
    base.STATE_CAP = 16_000_000
    base.BUDGET_SECONDS = budget
    pm = base.PmLazy(P["edge_w"], r)
    t0 = time.time()
    n = 0
    for (i, j) in todo:
        e1 = tuple(top[i]["rows_covered"])
        e2 = tuple(top[j]["rows_covered"])
        ja, jb, shared = tj.joint_pair(P, pm, e1, e2)
        rec = {"kind": "pair", "idx_i": i, "idx_j": j,
               "a": top[i]["root"], "b": top[j]["root"],
               "rows_a": list(e1), "rows_b": list(e2),
               "shared_row": shared, "joint_A": ja, "joint_B": jb,
               "joint": ja + jb,
               "memo_states": len(pm.memo),
               "sec": round(time.time() - t0, 1)}
        append(rec)
        n += 1
        print("[pairs] (%d,%d) rows %s/%s shared=%s A=%d B=%d memo=%d"
              " %.1fs" % (i, j, e1, e2, shared, ja, jb, len(pm.memo),
                          time.time() - t0), flush=True)
        if time.time() - t0 > budget:
            print("[pairs] budget hit after %d joints" % n, flush=True)
            break
    print("[pairs] slice done: computed %d, total done %d/33"
          % (n, len(done("pair", lambda e: (e["idx_i"], e["idx_j"])))),
          flush=True)
    return 0


def all_triples():
    return list(itertools.combinations(range(K), 3))


def new_triples():
    k10 = load_k10()
    pub = {tuple(int(c) for c in key)
           for key in k10["values"]["triples"]}
    return [c for c in all_triples() if c not in pub]


def mode_triples(slice_arg):
    agg, top, memA, memB, total, A16, B16 = load_top()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    triples = new_triples()
    assert len(triples) == 166, len(triples)
    lo = slice_arg * 40
    hi = min(lo + 40, len(triples))
    donet = done("triple", lambda e: tuple(e["combo"]))
    edge_w = None
    P = None
    t00 = time.time()
    for combo in triples[lo:hi]:
        if combo in donet:
            continue
        kind, union, reason = k10s.classify_triple(rows, combo)
        if kind in ("zero3x", "zero2x2"):
            append({"kind": "triple", "combo": list(combo),
                    "class": kind, "union": union, "joint": 0,
                    "reason": reason})
            print("[t%s %s] %s -> 0" % (kind, combo, reason), flush=True)
            continue
        if kind == "disjoint":
            raise SystemExit("unexpected disjoint triple %s -- abort"
                             % (combo,))
        if P is None:
            P, tbl = tj.load_parent(TARGET)
            edge_w = P["edge_w"]
        pm = k10s.MyPm(edge_w, R)
        t0 = time.time()
        mask = (1 << R) - 1
        for u in union:
            mask &= ~(1 << u)
        val = pm.count(mask)
        append({"kind": "triple", "combo": list(combo),
                "class": "b_only", "union": union, "joint": val,
                "reason": reason, "memo_states": len(pm.memo),
                "sec": round(time.time() - t0, 1)})
        print("[b_only %s] union=%s j3=%d memo=%d %.1fs"
              % (combo, union, val, len(pm.memo), time.time() - t0),
              flush=True)
    print("[triples] slice %d done, done %d/166 in %.1fs"
          % (slice_arg, len(done("triple", lambda e: tuple(e["combo"]))),
             time.time() - t00), flush=True)
    return 0


def mode_anchor():
    """Recompute all 120 published triples and 3 published pairs from
    scratch and match them against the pinned published outputs."""
    agg, top, memA, memB, total, A16, B16 = load_top()
    k10 = load_k10()
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    P, tbl = tj.load_parent(TARGET)
    edge_w = P["edge_w"]
    pub3 = k10["values"]["triples"]
    t0 = time.time()
    nbad = 0
    for c in itertools.combinations(range(10), 3):
        key = "%d%d%d" % c
        kind, union, reason = k10s.classify_triple(rows, c)
        if kind in ("zero3x", "zero2x2"):
            val, mst = 0, 0
        elif kind == "disjoint":
            raise SystemExit("unexpected disjoint triple %s" % (c,))
        else:
            pm = k10s.MyPm(edge_w, R)
            mask = (1 << R) - 1
            for u in union:
                mask &= ~(1 << u)
            val = pm.count(mask)
            mst = len(pm.memo)
        match = (val == int(pub3[key]["joint"])
                 and kind == pub3[key]["class"])
        append({"kind": "anchor3", "combo": list(c), "class": kind,
                "joint": val, "published": int(pub3[key]["joint"]),
                "match": match, "memo_states": mst})
        if not match:
            nbad += 1
            print("[anchor3 MISMATCH] %s mine=%d pub=%d"
                  % (c, val, pub3[key]["joint"]), flush=True)
    print("[anchor3] 120 triples, mismatches %d, %.1fs"
          % (nbad, time.time() - t0), flush=True)
    # pair anchors: (0,1) disjoint, (4,8) disjoint, (0,8) shared-row
    pubj = load_pub_joints()
    base.STATE_CAP = 16_000_000
    base.BUDGET_SECONDS = 600.0
    pm = base.PmLazy(edge_w, R)
    for (i, j) in [(0, 1), (4, 8), (0, 8)]:
        e1 = tuple(top[i]["rows_covered"])
        e2 = tuple(top[j]["rows_covered"])
        ja, jb, shared = tj.joint_pair(P, pm, e1, e2)
        p = pubj[(i, j)]
        match = (ja == p["joint_A"] and jb == p["joint_B"]
                 and shared == p["shared_row"])
        append({"kind": "anchor2", "idx_i": i, "idx_j": j,
                "joint_A": ja, "joint_B": jb, "shared_row": shared,
                "published_A": p["joint_A"],
                "published_B": p["joint_B"], "match": match})
        print("[anchor2] (%d,%d) shared=%s A=%d B=%d match=%s"
              % (i, j, shared, ja, jb, match), flush=True)
        if not match:
            nbad += 1
    print("[anchor] total mismatches %d" % nbad, flush=True)
    return 0 if nbad == 0 else 1


def cross_joint(edge_w, pm, w1, e1, e2):
    """Independent re-implementation of the pairwise joint formulas,
    written from the structure of A/B-type covers (NOT copied from
    tj.joint_pair), using the third-lineage MyPm counter.

    A-type cover: every row exactly once + one singleton root.
    B-type cover: exactly one doubly-covered row d, no singleton.

    shared (|e1 u e2| == 3): the doubled row must be the shared row
    (both banned roots cover it); the remaining 28 rows are matched by
    14 pair roots: joint_B = pm(V \\ union); joint_A = 0 (two roots
    sharing a row force a double).

    disjoint (|e1 u e2| == 4):
      doubled row z in the union (say z in e1): the second root on z
      is (z, a) with a outside the union (a inside would double a
      second row); remaining 26 rows matched: term
      sum_a [sum_z in union w(z,a)] * pm(mask \\ a).
      doubled row z outside the union: two roots (z,a),(z,b), a<b,
      both outside the union; remaining 24 rows matched: term
      sum_z sum_{a<b} w(z,a) w(z,b) pm(mask \\ {z,a,b}).
      joint_A = sum_s w1[s] * pm(V \\ e1 \\ e2 \\ {s}).
    """
    r = R
    full = (1 << r) - 1
    union = sorted(set(e1) | set(e2))
    rmask = 0
    for x in union:
        rmask |= 1 << x
    mask = full & ~rmask
    rows = set(union)
    if len(union) == 3:
        ja = 0
        jb = pm.count(mask)
        return ja, jb
    ja = 0
    for s in range(r):
        if w1.get(s) and not (rmask >> s) & 1:
            ja += w1[s] * pm.count(mask ^ (1 << s))
    jb = 0
    for a in range(r):
        if (rmask >> a) & 1:
            continue
        W = 0
        for z in union:
            W += edge_w.get((min(z, a), max(z, a)), 0)
        if W:
            jb += W * pm.count(mask ^ (1 << a))
    for z in range(r):
        if (rmask >> z) & 1:
            continue
        cand = [x for x in range(r)
                if x != z and not (rmask >> x) & 1
                and edge_w.get((min(x, z), max(x, z)))]
        for i1 in range(len(cand)):
            a = cand[i1]
            wa = edge_w[(min(a, z), max(a, z))]
            for i2 in range(i1 + 1, len(cand)):
                b = cand[i2]
                wb = edge_w[(min(b, z), max(b, z))]
                jb += (wa * wb
                       * pm.count(mask ^ (1 << z) ^ (1 << a)
                                  ^ (1 << b)))
    return ja, jb


def mode_cross():
    """Cross-check 5 of the 33 new pairwise joints with the
    independent MyPm-based implementation."""
    agg, top, memA, memB, total, A16, B16 = load_top()
    P, tbl = tj.load_parent(TARGET)
    edge_w = P["edge_w"]
    w1 = {s: len(rl) for s, rl in P["singleton_roots"].items()}
    donec = done("cross2", lambda e: (e["idx_i"], e["idx_j"]))
    targets = [(0, 10), (0, 11), (5, 10), (10, 12), (11, 12)]
    pairs = done("pair", lambda e: (e["idx_i"], e["idx_j"]))
    nbad = 0
    for (i, j) in targets:
        if (i, j) in donec:
            continue
        e1 = tuple(top[i]["rows_covered"])
        e2 = tuple(top[j]["rows_covered"])
        pm = k10s.MyPm(edge_w, R)
        t0 = time.time()
        ja, jb = cross_joint(edge_w, pm, w1, e1, e2)
        ref = pairs[(i, j)]
        match = (ja == ref["joint_A"] and jb == ref["joint_B"])
        append({"kind": "cross2", "idx_i": i, "idx_j": j,
                "joint_A": ja, "joint_B": jb,
                "ref_A": ref["joint_A"], "ref_B": ref["joint_B"],
                "match": match, "memo_states": len(pm.memo),
                "sec": round(time.time() - t0, 1)})
        print("[cross2] (%d,%d) mine A=%d B=%d ref A=%d B=%d match=%s"
              " memo=%d %.1fs" % (i, j, ja, jb, ref["joint_A"],
                                  ref["joint_B"], match, len(pm.memo),
                                  time.time() - t0), flush=True)
        if not match:
            nbad += 1
    print("[cross2] mismatches %d" % nbad, flush=True)
    return 0 if nbad == 0 else 1


def collect():
    pairs = done("pair", lambda e: (e["idx_i"], e["idx_j"]))
    triples = done("triple", lambda e: tuple(e["combo"]))
    anchors3 = done("anchor3", lambda e: tuple(e["combo"]))
    anchors2 = done("anchor2", lambda e: (e["idx_i"], e["idx_j"]))
    return pairs, triples, anchors3, anchors2


def finalize_mode():
    checks = []

    def chk(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok), "detail": detail})
        print(("PASS " if ok else "FAIL ") + name, flush=True)

    ban = json.loads(read_sha256(BAN_JSON_REL, BAN_SHA256))
    srb = json.loads(read_sha256(SRB_JSON_REL, SRB_SHA256))
    agg, top, memA, memB, total, A16, B16 = load_top()
    mem = [e["membership"] for e in top]
    ap = [memA[e["root"]] for e in top]
    bp = [memB[e["root"]] for e in top]
    k10 = load_k10()
    pubj = load_pub_joints()
    pairs, triples, anchors3, anchors2 = collect()

    # ---- structure
    hub_ok = all(18 in e["rows_covered"] or 19 in e["rows_covered"]
                 for e in top)
    chk("top13.hub_rows_18_19", hub_ok,
        {str(i): list(top[i]["rows_covered"]) for i in range(K)})
    nxt = agg["derived"]["top50_by_membership"][K]
    chk("rank14.first_non_hub", not (18 in nxt["rows_covered"]
                                     or 19 in nxt["rows_covered"]),
        {"rank14_rows": nxt["rows_covered"],
         "note": "k=14 would need the A-type 3-way formulas; not "
                 "attempted here"})
    chk("top13.membership_split", all(
        ap[i] + bp[i] == mem[i] for i in range(K)))

    # ---- published pairwise joints reused
    j2 = {}
    for (i, j), e in pubj.items():
        j2[(i, j)] = {"A": e["joint_A"], "B": e["joint_B"],
                      "joint": e["joint"], "shared": e["shared_row"]}
    chk("pairs.published_45", len(pubj) == 45)
    chk("pairs.new_33", len(pairs) == 33, len(pairs))
    for c, e in pairs.items():
        assert c not in pubj
        j2[c] = {"A": e["joint_A"], "B": e["joint_B"],
                 "joint": e["joint"], "shared": e["shared_row"]}
    chk("pairs.complete_78", len(j2) == 78, len(j2))
    shared_new = [c for c in pairs if pairs[c]["shared_row"]]
    disjoint_new = [c for c in pairs if not pairs[c]["shared_row"]]
    chk("pairs.new_census", len(shared_new) == 17
        and len(disjoint_new) == 16,
        {"shared": len(shared_new), "disjoint": len(disjoint_new)})
    chk("pairs.shared_jointA_zero", all(
        j2[c]["A"] == 0 for c in j2 if j2[c]["shared"]))
    chk("pairs.bounds", all(
        j2[c]["joint"] <= min(mem[c[0]], mem[c[1]])
        and j2[c]["A"] <= min(ap[c[0]], ap[c[1]])
        and j2[c]["B"] <= min(bp[c[0]], bp[c[1]]) for c in j2))

    # ---- triples
    chk("triples.published_anchor_120", len(anchors3) == 120
        and all(e["match"] for e in anchors3.values()),
        {"mismatches": sum(0 if e["match"] else 1
                           for e in anchors3.values())})
    chk("triples.new_166", len(triples) == 166, len(triples))
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top)}
    j3 = {}
    cls_pub = {}
    for key, v in k10["values"]["triples"].items():
        c = tuple(int(ch) for ch in key)
        j3[c] = int(v["joint"])
        cls_pub[c] = v["class"]
    classes = {}
    for c in itertools.combinations(range(K), 3):
        kind, union, reason = k10s.classify_triple(rows, c)
        classes[c] = kind
        if c in triples:
            assert triples[c]["class"] == kind
            j3[c] = triples[c]["joint"]
        else:
            assert kind == cls_pub[c] and j3[c] == int(
                k10["values"]["triples"]["%d%d%d" % c]["joint"])
    chk("triples.complete_286", len(j3) == 286, len(j3))
    census = {"b_only": 0, "zero3x": 0, "zero2x2": 0, "disjoint": 0}
    for c in classes:
        census[classes[c]] += 1
    chk("triples.no_disjoint", census["disjoint"] == 0, census)
    chk("triples.jointA_zero", all(j3[c] == 0
                                   for c in classes if classes[c] != "b_only"))
    chk("triples.le_min_pairs", all(
        j3[c] <= min(j2[(c[0], c[1])]["joint"], j2[(c[0], c[2])]["joint"],
                     j2[(c[1], c[2])]["joint"])
        for c in classes if j3[c]))
    quads_bad = all(k10s.quad_invalid(rows, q)
                    for q in itertools.combinations(range(K), 4))
    chk("quads715.all_structural_zero", quads_bad,
        {"subsets": 715,
         "note": "13 hub roots -> pigeonhole on rows 18/19; higher "
                 "orders vanish by monotonicity"})

    # ---- kill(k) totals and A/B split
    kill = {}
    killA = {}
    killB = {}
    for k in range(1, K + 1):
        v = vA = vB = 0
        for i in range(k):
            v += mem[i]
            vA += ap[i]
            vB += bp[i]
        for i in range(k):
            for j in range(i + 1, k):
                v -= j2[(i, j)]["joint"]
                vA -= j2[(i, j)]["A"]
                vB -= j2[(i, j)]["B"]
        for c in itertools.combinations(range(k), 3):
            v += j3[c]
            vB += j3[c]
        kill[k] = v
        killA[k] = vA
        killB[k] = vB
        assert v == vA + vB
    chk("split.identity_per_k",
        all(kill[k] == killA[k] + killB[k] for k in range(1, K + 1)))
    chk("split.pub_k4_k8",
        A16 - killA[4] == 1912189176067079977
        and B16 - killB[4] == 541653214551014457
        and A16 - killA[8] == 1564239038548375836
        and B16 - killB[8] == 437686674003751251,
        "matches the published direct per-d-slice recomputation "
        "(commit 33abfdb8)")
    direct = {e["k"]: e for e in ban["derived"]["curve"]
              if "type_A" in e}
    chk("split.pub_k4_k8_from_pinned_json",
        all(A16 - killA[k] == direct[k]["type_A"]
            and B16 - killB[k] == direct[k]["type_B"]
            for k in (4, 8)))
    chk("split.monotone",
        all(killA[k] <= killA[k + 1] and killB[k] <= killB[k + 1]
            for k in range(1, K)))

    # ---- reproduce published k=1..10 and monotonicity / bounds
    pubkill = {int(k[1:]): int(v) for k, v in
               k10["values"]["kill"].items()}
    chk("survival.reproduce_k1_k10",
        all(kill[k] == pubkill[k] for k in range(1, 11)),
        {"k10_mine": str(kill[10]),
         "k10_pub": str(pubkill[10])})
    chk("survival.monotone_k1_k13",
        all(kill[k] <= kill[k + 1] for k in range(1, K))
        and kill[K] <= total,
        [str(kill[k]) for k in range(1, K + 1)])
    marg_ok = all(0 <= kill[k + 1] - kill[k] <= mem[k]
                  for k in range(1, K))
    chk("survival.marginals", marg_ok,
        {"k%d_minus_k%d" % (k + 1, k): str(kill[k + 1] - kill[k])
         for k in range(1, K)})
    ub_ok = all(total - kill[k] >= total - sum(mem[:k])
                for k in range(1, K + 1))
    chk("survival.union_bound", ub_ok)

    # ---- full singleton ban mixed curve = B_survive(k)
    Bsurv = {k: B16 - killB[k] for k in range(1, K + 1)}
    Bsurv[0] = B16
    Asurv = {k: A16 - killA[k] for k in range(1, K + 1)}
    chk("mixed.b_survive_monotone",
        all(Bsurv[k] >= Bsurv[k + 1] for k in range(K)))
    chk("mixed.a_survive_monotone",
        all(Asurv[k] >= Asurv[k + 1] for k in range(1, K)))
    chk("mixed.k10_endpoint",
        Bsurv[10] == 389244119480989629,
        {"full_singleton_ban_survive_k10": str(Bsurv[10]),
         "share": round(100 * Bsurv[10] / total, 6)})
    km = srb["values"]["kill_mixed"]
    chk("mixed.consistent_with_row_ban_curve",
        int(km["pairs10"]) == kill[10]
        and int(km["pairs10_plus_rows3"]) <= total - Bsurv[10],
        {"pairs10_plus_rows3": km["pairs10_plus_rows3"],
         "pairs10_plus_full_row_ban": str(total - Bsurv[10])})
    chk("mixed.full_ban_identity",
        total - Bsurv[10] == A16 + killB[10],
        "kill(all singletons + top-10 pairs) = A16 + kill_B(10)")

    # ---- anchors for the pair machinery
    chk("anchors.pairs_3", len(anchors2) == 3
        and all(e["match"] for e in anchors2.values()),
        {"checked": sorted(anchors2)})
    crosses = done("cross2", lambda e: (e["idx_i"], e["idx_j"]))
    chk("cross.new_pairs_5", len(crosses) == 5
        and all(e["match"] for e in crosses.values()),
        {"checked": sorted(crosses),
         "note": "independent re-implementation of the joint formulas "
                 "with the MyPm counter lineage"})

    out = {
        "schema": "n11-cost16-survival-k13-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Exact survival curve k=1..13 with exact A/B type "
                  "split for the 31-row cost-16 parent "
                  "00000000000000003800000008001000: I-E extension to "
                  "k=11..13 (33 new pairwise joints + 166 new triples, "
                  "structural collapse verified for 13 hub roots) and "
                  "the full-singleton-ban mixed curve "
                  "B_survive(k) = B16 - kill_B(k)"),
        "inputs": {
            "groups_aggregate": {"path": GROUPS_AGG_REL,
                                 "git_blob_sha1": GROUPS_AGG_PIN},
            "published_joint_jsonl": {"path": PUB_JOINT_JSONL_REL,
                                      "git_blob_sha1": PUB_JOINT_PIN,
                                      "commit": "537a4458"},
            "survival_k10_json": {"path": K10_JSON_REL,
                                  "git_blob_sha1": K10_PIN,
                                  "commit": "a59881a2"},
            "ban_survival_json": {"path": BAN_JSON_REL,
                                  "sha256": BAN_SHA256,
                                  "commit": "33abfdb8"},
            "singleton_row_ban_json": {"path": SRB_JSON_REL,
                                       "sha256": SRB_SHA256,
                                       "commit": "c98cb51d"},
            "candidate_roots": {"path":
                                "(regenerated) output/global-candidate-"
                                "roots-20261118.jsonl",
                                "regenerated_by":
                                "enumerate_global_candidate_roots_"
                                "20261118.py"},
        },
        "structure": {
            "top13": [{"idx": i, "root": top[i]["root"],
                       "rows": list(top[i]["rows_covered"]),
                       "membership": str(mem[i]),
                       "a_part": str(ap[i]), "b_part": str(bp[i])}
                      for i in range(K)],
            "hub_property": ("every top-13 root contains row 18 or 19; "
                              "rank 14 = %s rows %s is the first "
                              "non-hub root"
                              % (nxt["root"], nxt["rows_covered"])),
            "triple_census": census,
            "quad_note": ("all 715 4-subsets verified structurally "
                          "impossible; quints+ vanish by monotonicity"),
            "new_pair_census": {"shared_row": len(shared_new),
                                "disjoint": len(disjoint_new)},
            "split_identities": (
                "kill_A(k) = sum a_i - sum joint_A (j3_A == 0 by the "
                "hub triple census); kill_B(k) = sum b_i - sum joint_B "
                "+ sum j3; validated at k=4/k=8 against the published "
                "direct per-d-slice recomputation"),
            "full_singleton_ban": (
                "every A-type cover has exactly one singleton root, so "
                "banning all 1,483 singleton roots kills every A-type "
                "plan; B-type covers have no singleton, so "
                "B_survive(k) = B16 - kill_B(k) is the exact survival "
                "count under top-k pair bans + full singleton ban"),
        },
        "values": {
            "total_minimum_covers": str(total),
            "type_A_total": str(A16),
            "type_B_total": str(B16),
            "kill": {("k%d" % k): str(kill[k]) for k in range(1, K + 1)},
            "kill_A": {("k%d" % k): str(killA[k])
                       for k in range(1, K + 1)},
            "kill_B": {("k%d" % k): str(killB[k])
                       for k in range(1, K + 1)},
            "kill_share_percent": {
                ("k%d" % k): round(100 * kill[k] / total, 6)
                for k in range(1, K + 1)},
            "marginals": {"k%d_minus_k%d" % (k + 1, k):
                          str(kill[k + 1] - kill[k])
                          for k in range(1, K)},
            "A_survive": {("k%d" % k): str(Asurv[k])
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
                for c in sorted(pairs)},
            "new_triples": {
                "%d%d%d" % c: {"class": classes[c],
                               "joint": str(j3[c])}
                for c in sorted(triples)},
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all(c["pass"] for c in checks),
        "interpretation_guard": (
            "Cover-plan combinatorics only. Survival points count "
            "minimum cover plans containing at least one banned root; "
            "they are not search costs and imply nothing about "
            "WIN/REFUTED verdicts of the banned roots. REFUTED-D10 "
            "and STERILE are not LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots "
                           "{49,60}/{59,60}, S2 {59,60}, and classes "
                           "1/2/4 remain UNKNOWN."),
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
        frm = int(sys.argv[2])
        to = int(sys.argv[3])
        budget = float(sys.argv[4]) if len(sys.argv) > 4 else 200.0
        return mode_pairs(frm, to, budget)
    if mode == "triples":
        sl = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        return mode_triples(sl)
    if mode == "anchor":
        return mode_anchor()
    if mode == "cross":
        return mode_cross()
    if mode == "finalize":
        return finalize_mode()
    print("usage: pairs FROM TO [BUDGET] | triples [SLICE] | anchor | "
          "finalize")
    return 2


if __name__ == "__main__":
    sys.exit(main())
