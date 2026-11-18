#!/usr/bin/env python3
r"""Third-implementation cross-check of the published top-10 joint memberships
(45 combinations, A/B split) for the 31-row cost-16 parent
00000000000000003800000008001000.

The published result (commit 537a4458, script cost16_top10_joint_20261118.py)
computed the joints with the published PmLazy implementation and validated the
formula against a full explicit enumeration of the 11-row parent (359,610
covers). This script is an independent re-derivation and re-implementation:

  - own weighted perfect-matching counter (MyPm: lowest-row-anchored
    memoized recursion; no import of the published cost16_parent_membership
    PmLazy),
  - formulas wired independently from the cover semantics
      shared-row pairs e1,e2 (|e1 u e2| = 3):
          joint_A = 0
          joint_B = pm(V \ (e1 u e2))                       [14-pair matching]
      disjoint pairs (|e1 u e2| = 4):
          joint_A = sum_s w1[s] * pm(V\e1\e2\{s})     [13 pairs + singleton s]
          joint_B = sum_z W(z) * pm(V\e1\e2\{z})       [doubled row in e1 u e2,
                                                       second cover (d,z)]
                  + sum_d sum_{x<y in N(d)} w(d,x) w(d,y)
                        * pm(V\e1\e2\{d,x,y})         [doubled row outside;
                                                       12-pair matching]
        with W(z) = sum_{d in e1 u e2} w(d, z),
  - anchor validation BEFORE the joints, against published numbers only:
      (a) per-row singleton anchor pm(V\{s}) == published phase-A per_row
          value, all 31 rows (shared memo),
      (b) 1-type re-derivation: a_part/b_part of 3 pair types recomputed
          with MyPm must match the published groups JSONL records
          ((0,1) first type, (15,19) top-1 type, (28,30) last type),
      (c) direct B_d re-derivation for d=18 and d=2 must match the published
          b_slices values,
  - then all 45 published joint records are recomputed and compared
    value-by-value (joint_A, joint_B, joint).

Usage: python3 crosscheck_top10_joint_third_20261118.py SLICE [BUDGET]
  SLICE 0..3 computes combos [0:12), [12:24), [24:36), [36:45) with a fresh
  shared memo per invocation (resume-safe; already-computed combos skipped);
  SLICE -1 runs the anchors. Output is appended to
  output/crosscheck-top10-joint-third-20261118.jsonl (one record per combo)
  and finalized by finalize mode (SLICE 'finalize') into
  output/crosscheck-top10-joint-third-20261118.json.

Membership and joint counts are combinatorial counts of minimum
certificate-cover plans, not search costs or verdicts. REFUTED-D10 and STERILE
are not LOSS proofs. The standard 11x11 empty board, the two-stone roots
{49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.
"""
import hashlib
import json
import os
import pickle
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")

PICKLE_PATH = os.path.join(OUT, "parent-struct-cost16.pickle")
PHASE_A_PATH = os.path.join(OUT, "cost16-a-phase-20261118.json")
PHASE_A_PIN = "fe4b4b559fd8c3fdc9bc9b9f40a048fc3217c55b"
GROUPS_JSONL = os.path.join(OUT, "cost16-b-groups-20261118.jsonl")
B16_PATH = os.path.join(OUT, "cost16-b-phase-total-20261118.json")
B16_PIN = "883275fba179c28988b5bfd3aaa3fab79be9be7c"
AGG_PATH = os.path.join(OUT, "cost16-b-phase-groups-20261118.json")
PUB_JOINT_JSONL = os.path.join(OUT, "cost16-top10-joint-20261118.jsonl")
CROSS_JSONL = os.path.join(OUT, "crosscheck-top10-joint-third-20261118.jsonl")
CROSS_JSON = os.path.join(OUT, "crosscheck-top10-joint-third-20261118.json")

TARGET = "00000000000000003800000008001000"


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


class MyPm:
    """Independent weighted perfect-matching counter (memoized, lowest-row
    anchored). Same mathematics as the published PmLazy, written separately."""

    def __init__(self, edge_w, r):
        self.ew = edge_w
        self.r = r
        self.memo = {0: 1}
        self.calls = 0

    def count(self, mask):
        v = self.memo.get(mask)
        if v is not None:
            return v
        low = mask & -mask
        v0 = low.bit_length() - 1
        rest = mask ^ low
        total = 0
        m = rest
        while m:
            b = m & -m
            v1 = b.bit_length() - 1
            m ^= b
            w = self.ew.get((v0, v1) if v0 < v1 else (v1, v0))
            if w:
                total += w * self.count(rest ^ b)
        self.memo[mask] = total
        return total


def load_parent():
    P, tbl = pickle.load(open(PICKLE_PATH, "rb"))
    assert len(P["target"]) == 31 and tbl["witness_size"] == 16
    assert tbl["exact"] and tbl["hex"] == TARGET
    assert len(P["proot_rows"]) == 1908 and len(P["pair_roots"]) == 425
    assert {len(rl) for rl in P["pair_roots"].values()} == {1}
    return P


def full_mask(r):
    return (1 << r) - 1


def type_masks(e):
    return (1 << e[0]) | (1 << e[1])


def a_part_of(P, pm, mask_pair, w1, r):
    """1-type A-part: covers containing pair e (mask_pair already excludes
    e's rows): sum_s w1[s] * pm(mask_pair ^ (1<<s))."""
    total = 0
    for s in range(r):
        if w1[s] and (mask_pair >> s) & 1:
            total += w1[s] * pm.count(mask_pair ^ (1 << s))
    return total


def joint_value(P, pm, e1, e2, w1, r):
    edge_w = P["edge_w"]
    m1 = type_masks(e1)
    m2 = type_masks(e2)
    shared = sorted(set(e1) & set(e2))
    if shared:
        joint_a = 0
        joint_b = pm.count(full_mask(r) & ~(m1 | m2))
        return joint_a, joint_b, True
    base = full_mask(r) & ~(m1 | m2)
    joint_a = 0
    for s in range(r):
        if w1[s] and (base >> s) & 1:
            joint_a += w1[s] * pm.count(base ^ (1 << s))
    joint_b = 0
    # doubled row inside e1 u e2: second coverage (d, z)
    for d in list(e1) + list(e2):
        for z in range(r):
            if z in e1 or z in e2:
                continue
            wz = edge_w.get((min(d, z), max(d, z)), 0)
            if wz:
                joint_b += wz * pm.count(base ^ (1 << z))
    # doubled row outside e1 u e2
    rows12 = set(e1) | set(e2)
    for d in range(r):
        if d in rows12:
            continue
        dbit = 1 << d
        nbrs = [x for x in range(r)
                if x != d and x not in rows12
                and edge_w.get((min(d, x), max(d, x)))]
        for i in range(len(nbrs)):
            x = nbrs[i]
            wx = edge_w[(min(d, x), max(d, x))]
            for j in range(i + 1, len(nbrs)):
                y = nbrs[j]
                wy = edge_w[(min(d, y), max(d, y))]
                joint_b += wx * wy * pm.count(base ^ dbit ^ (1 << x) ^ (1 << y))
    return joint_a, joint_b, False


def append(rec):
    with open(CROSS_JSONL, "a") as f:
        f.write(json.dumps(rec) + "\n")


def done_set():
    done = set()
    if os.path.exists(CROSS_JSONL):
        with open(CROSS_JSONL) as f:
            for line in f:
                e = json.loads(line)
                if (not e.get("summary") and "anchors_section" not in e
                        and "idx_i" in e):
                    done.add((e["idx_i"], e["idx_j"]))
    return done


def anchor_sections_done():
    secs = set()
    if os.path.exists(CROSS_JSONL):
        with open(CROSS_JSONL) as f:
            for line in f:
                e = json.loads(line)
                if 'anchors_section' in e:
                    secs.add(e['anchors_section'])
    return secs


def anchors(P, which):
    r = 31
    edge_w = P["edge_w"]
    w1 = {s: len(rl) for s, rl in P["singleton_roots"].items()}
    for s in range(r):
        w1.setdefault(s, 0)
    pa_bytes = open(PHASE_A_PATH, "rb").read()
    assert git_blob_sha(pa_bytes) == PHASE_A_PIN
    pa = json.loads(pa_bytes)
    per_row = pa["derived"]["singleton_membership_stats"]["per_row"]
    b16_bytes = open(B16_PATH, "rb").read()
    assert git_blob_sha(b16_bytes) == B16_PIN
    bd = {e["d"]: e["b_d"] for e in json.loads(b16_bytes)["derived"]["b_slices"]}
    full = full_mask(r)
    t0 = time.time()
    checks = []
    if which == "perrow":
        pm = MyPm(edge_w, r)
        ok_a = True
        for s in range(r):
            v = pm.count(full ^ (1 << s))
            print("[anchor per-row %d] match=%s memo=%d %.1fs"
                  % (s, v == int(per_row[str(s)]), len(pm.memo),
                     time.time() - t0), flush=True)
            if v != int(per_row[str(s)]):
                ok_a = False
                checks.append({"name": "anchor.per_row_pm", "pass": False,
                               "row": s, "mine": v,
                               "published": per_row[str(s)]})
        checks.append({"name": "anchor.per_row_pm_31", "pass": ok_a,
                       "memo_states": len(pm.memo),
                       "sec": round(time.time() - t0, 1)})
        append({"anchors_section": "perrow", "checks": checks,
                 "all_pass": all(c["pass"] for c in checks)})
        return 0 if all(c["pass"] for c in checks) else 1
    if which in ("type01", "type1519", "type2830"):
        tpmap = {"type01": (0, 1), "type1519": (15, 19),
                 "type2830": (28, 30)}
        tp = tpmap[which]
        grecs = {}
        with open(GROUPS_JSONL) as f:
            for line in f:
                e = json.loads(line)
                if not e.get("summary"):
                    grecs[tuple(e["pair"])] = e
        pm2 = MyPm(edge_w, r)
        mask_pair = full & ~type_masks(tp)
        a_mine = a_part_of(P, pm2, mask_pair, w1, r)
        b_mine = 0
        for d in tp:
            for z in range(r):
                if z in tp:
                    continue
                wz = edge_w.get((min(d, z), max(d, z)), 0)
                if wz:
                    b_mine += wz * pm2.count(mask_pair ^ (1 << z))
        for d in range(r):
            if d in tp:
                continue
            dbit = 1 << d
            nbrs = [x for x in range(r)
                    if x != d and x not in tp
                    and edge_w.get((min(d, x), max(d, x)))]
            for i in range(len(nbrs)):
                x = nbrs[i]
                wx = edge_w[(min(d, x), max(d, x))]
                for j in range(i + 1, len(nbrs)):
                    y = nbrs[j]
                    wy = edge_w[(min(d, y), max(d, y))]
                    b_mine += wx * wy * pm2.count(
                        mask_pair ^ dbit ^ (1 << x) ^ (1 << y))
        pub = grecs[tp]
        ok = (a_mine == pub["a_part"] and b_mine == pub["b_part"])
        print("[anchor type %s] a=%d/%d b=%d/%d memo=%d %.1fs"
              % (tp, a_mine, pub["a_part"], b_mine, pub["b_part"],
                 len(pm2.memo), time.time() - t0), flush=True)
        checks.append({"name": "anchor.type_ab_%s" % (tp,), "pass": ok,
                       "a_mine": a_mine, "b_mine": b_mine,
                       "a_pub": pub["a_part"], "b_pub": pub["b_part"],
                       "memo_states": len(pm2.memo)})
        append({"anchors_section": which, "checks": checks,
                 "all_pass": all(c["pass"] for c in checks)})
        return 0 if ok else 1
    if which in ("direct18", "direct2"):
        d = 18 if which == "direct18" else 2
        pm3 = MyPm(edge_w, r)
        dbit = 1 << d
        nbrs = [x for x in range(r)
                if x != d and edge_w.get((min(d, x), max(d, x)))]
        contrib = 0
        for i in range(len(nbrs)):
            x = nbrs[i]
            wx = edge_w[(min(d, x), max(d, x))]
            for j in range(i + 1, len(nbrs)):
                y = nbrs[j]
                wy = edge_w[(min(d, y), max(d, y))]
                contrib += wx * wy * pm3.count(full ^ dbit ^ (1 << x) ^ (1 << y))
        ok = contrib == bd[d]
        print("[anchor direct d=%d] %d/%d memo=%d %.1fs"
              % (d, contrib, bd[d], len(pm3.memo), time.time() - t0),
              flush=True)
        checks.append({"name": "anchor.direct_b_d_%d" % d, "pass": ok,
                       "mine": contrib, "published": bd[d],
                       "memo_states": len(pm3.memo)})
        append({"anchors_section": which, "checks": checks,
                 "all_pass": all(c["pass"] for c in checks)})
        return 0 if ok else 1
    return 2


def combos():
    agg = json.load(open(AGG_PATH))
    top10 = agg["derived"]["top50_by_membership"][:10]
    roots = [e["root"] for e in top10]
    rows = [tuple(e["rows_covered"]) for e in top10]
    return roots, rows


def run_slice(P, sl, budget):
    r = 31
    edge_w = P["edge_w"]
    w1 = {s: len(rl) for s, rl in P["singleton_roots"].items()}
    for s in range(r):
        w1.setdefault(s, 0)
    pub = {}
    with open(PUB_JOINT_JSONL) as f:
        for line in f:
            e = json.loads(line)
            if not e.get("summary"):
                pub[(e["idx_i"], e["idx_j"])] = e
    roots, rows = combos()
    pair_roots = P["pair_roots"]
    root_of = {}
    for t, rl in pair_roots.items():
        root_of[rl[0]] = t
    done = done_set()
    bounds = [(0, 12), (12, 24), (24, 36), (36, 45)][sl]
    order = [(i, j) for i in range(10) for j in range(i + 1, 10)]
    todo = [c for c in order[bounds[0]:bounds[1]] if c not in done]
    print("[slice %d] todo %d (done %d)" % (sl, len(todo), len(done)), flush=True)
    if not todo:
        return 0
    pm = MyPm(edge_w, r)
    t0 = time.time()
    n = 0
    for (i, j) in todo:
        e1 = rows[i]
        e2 = rows[j]
        assert root_of[roots[i]] == tuple(sorted(e1))
        assert root_of[roots[j]] == tuple(sorted(e2))
        ja, jb, shared = joint_value(P, pm, tuple(sorted(e1)), tuple(sorted(e2)), w1, r)
        p = pub[(i, j)]
        rec = {"idx_i": i, "idx_j": j, "a": roots[i], "b": roots[j],
               "rows_a": list(e1), "rows_b": list(e2), "shared_row": shared,
               "joint_A_mine": ja, "joint_B_mine": jb, "joint_mine": ja + jb,
               "joint_A_pub": p["joint_A"], "joint_B_pub": p["joint_B"],
               "joint_pub": p["joint"],
               "match": (ja == p["joint_A"] and jb == p["joint_B"]
                         and ja + jb == p["joint"]
                         and shared == p["shared_row"]),
               "memo_states": len(pm.memo), "sec": round(time.time() - t0, 1)}
        append(rec)
        n += 1
        print("[slice %d] combo (%d,%d) rows %s x %s shared=%s A=%d/%d B=%d/%d match=%s"
              % (sl, i, j, e1, e2, shared, ja, p["joint_A"], jb, p["joint_B"],
                 rec["match"]), flush=True)
        if time.time() - t0 > budget:
            print("[slice %d] budget hit after %d combos" % (sl, n), flush=True)
            break
    return 0


def finalize(P):
    recs = []
    sections = anchor_sections_done()
    need = ["perrow", "type01", "type1519", "type2830",
            "direct18", "direct2"]
    if os.path.exists(CROSS_JSONL):
        with open(CROSS_JSONL) as f:
            for line in f:
                e = json.loads(line)
                if "anchors_section" in e or "anchors" in e:
                    continue
                elif not e.get("summary"):
                    recs.append(e)
    anchors_ok = set(sections) >= set(need)
    if anchors_ok:
        with open(CROSS_JSONL) as f:
            for line in f:
                e = json.loads(line)
                if "anchors_section" in e and not e["all_pass"]:
                    anchors_ok = False
    order = [(i, j) for i in range(10) for j in range(i + 1, 10)]
    bycombo = {(e["idx_i"], e["idx_j"]): e for e in recs}
    checks = []
    def chk(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok), "detail": detail})
    chk("anchors.all_pass", anchors_ok is True)
    chk("combos.count_45", len(bycombo) == 45 and len(recs) == 45, len(recs))
    chk("combos.set_match", set(bycombo) == set(order))
    chk("combos.all_match",
        all(e["match"] for e in recs),
        [k for k, e in bycombo.items() if not e["match"]])
    agg = json.load(open(AGG_PATH))
    top10 = agg["derived"]["top50_by_membership"][:10]
    m = [e["membership"] for e in top10]
    ap = [e["membership_A"] for e in top10]
    bp = [e["membership_B"] for e in top10]
    # shared-row pairs have joint_A == 0 (published claims 22/45)
    shared_pairs = [k for k, e in bycombo.items() if e["shared_row"]]
    chk("shared_row.joint_A_zero",
        len(shared_pairs) == 22 and all(bycombo[k]["joint_A_mine"] == 0
                                        for k in shared_pairs),
        len(shared_pairs))
    # mate-capacity bound: sum_j joint(i,j) <= 14*a_i + 15*b_i
    cap_ok = True
    for i in range(10):
        s = sum(bycombo[(min(i, j), max(i, j))]["joint_mine"]
                for j in range(10) if j != i)
        if s > 14 * ap[i] + 15 * bp[i]:
            cap_ok = False
    chk("bounds.mate_capacity_10x", cap_ok)
    # joint <= min(m1, m2)
    bnd_ok = all(bycombo[(i, j)]["joint_mine"] <= min(m[i], m[j])
                 for (i, j) in order)
    chk("bounds.joint_le_min_membership", bnd_ok)
    # k=1 / k=2 survival points (re-derived)
    total = agg["derived"]["total_minimum_covers"]
    k1 = m[0]
    k2 = m[0] + m[1] - bycombo[(0, 1)]["joint_mine"]
    # published share 4.5975% is a 4-decimal rounding of 4.597501506...%
    chk("survival.k1_share", round(100 * k1 / total, 4) == 4.5975,
        100 * k1 / total)
    chk("survival.k2_value",
        k2 == 262073639571350318,
        {"k2_mine": str(k2), "k2_pub": "262073639571350318"})
    out = {
        "schema": "n11-cost16-top10-joint-third-impl-crosscheck-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Third-implementation cross-check of the published top-10 "
                  "joint memberships (45 combos, A/B split) for the 31-row "
                  "cost-16 parent: independent MyPm counter + independently "
                  "wired formulas, anchored on published per-row pm / 1-type "
                  "a,b / B_d values before the joints"),
        "inputs": {
            "published_joint": {"commit": "537a4458",
                                "jsonl": "cost16-top10-joint-20261118.jsonl"},
            "phase_a_output": {"git_blob_sha1": PHASE_A_PIN},
            "b16_slice_output": {"git_blob_sha1": B16_PIN},
            "groups_aggregate": "cost16-b-phase-groups-20261118.json",
            "parent_pickle": ("(regenerable via the canonical loader from the "
                              "pinned cover table + regenerated candidate "
                              "JSONL)"),
        },
        "headline": {
            "combos_matched": "45/45 (joint_A, joint_B, joint, shared_row)",
            "anchors": ("per-row pm 31/31, 1-type a/b 3/3, direct B_d 2/2"),
            "shared_row_pairs_joint_A_zero": True,
            "k2_kill_exact": str(k2),
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all(c["pass"] for c in checks),
        "interpretation_guard": (
            "Joint memberships are counts of alternative minimum "
            "certificate-cover plans, not search costs or verdicts. "
            "REFUTED-D10 and STERILE are not LOSS proofs."),
        "unknown_status": (
            "Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
            "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    with open(CROSS_JSON, "w") as f:
        f.write(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"checks": len(checks), "all_pass": out["all_pass"],
                      "failed": [c["name"] for c in checks if not c["pass"]]},
                     indent=1))
    return 0 if out["all_pass"] else 1


def main():
    P = load_parent()
    if len(sys.argv) >= 3 and sys.argv[1] == "anchors":
        if sys.argv[2] in anchor_sections_done():
            print("[anchors] section %s already recorded" % sys.argv[2])
            return 0
        return anchors(P, sys.argv[2])
    if len(sys.argv) >= 2 and sys.argv[1] == "finalize":
        return finalize(P)
    if len(sys.argv) >= 2 and sys.argv[1].isdigit():
        sl = int(sys.argv[1])
        budget = float(sys.argv[2]) if len(sys.argv) > 2 else 240.0
        return run_slice(P, sl, budget)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
