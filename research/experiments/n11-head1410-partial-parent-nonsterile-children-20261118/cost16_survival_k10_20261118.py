#!/usr/bin/env python3
"""Survival curve k=1..10, exact, for the 31-row cost-16 parent.

Banning the top-k pair roots (by minimum-cover membership) kills every
minimum cover plan containing at least one banned root:

    kill(k) = sum_i<k m_i - sum_pairs j_ij + sum_triples j_ijk - ...   (I-E)

Structural collapse that makes k up to 10 exact and cheap:

  * every top-10 root contains row 18 or row 19 (hub rows);
  * therefore no 3 roots are pairwise disjoint (a disjoint set can hold
    at most one {x,18} and one {y,19}) -> every triple shares a row ->
    joint_A = 0 for all triples;
  * every 4-subset has, by pigeonhole on the hub rows, either a row
    covered >= 3x or two rows covered 2x -> impossible in A-type (all
    rows once) and in B-type (exactly one doubly-covered row) ->
    joint = 0; higher orders are then 0 by monotonicity (a cover
    containing 5 banned roots contains 4 of them);
  * a triple with exactly one doubly-covered row is B-type-only with
    that row as the unique double row, so the remaining 13 pairs form a
    perfect matching of V \\ (union):  j3 = pm(V \\ union), a 26-row set
    (fresh memo each, ~0.2M states, <1s);
  * a triple with a row covered >= 3x, or with two rows covered 2x, is
    structurally zero.

So kill(k) = sum m - sum j2 + sum j3 with pairwise joints taken from the
published 45-combo table (commit 537a4458; already matched 45/45 by the
third-implementation crosscheck) and 120 triples computed here with the
independent MyPm counter (no PmLazy import).

Cover-plan combinatorics only.  No engine run, no verdict.

Usage:
  python3 cost16_survival_k10_20261118.py run [slice]
  python3 cost16_survival_k10_20261118.py classify   # zero/B-only census
  python3 cost16_survival_k10_20261118.py finalize
"""

import hashlib
import itertools
import json
import os
import pickle
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")

PICKLE_PATH = os.path.join(OUT, "parent-struct-cost16.pickle")
AGG_PATH = os.path.join(OUT, "cost16-b-phase-groups-20261118.json")
AGG_PIN = "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87"
PUB_JOINT_JSONL = os.path.join(OUT, "cost16-top10-joint-20261118.jsonl")
PUB_JOINT_PIN = "95194096b2dcb547b5b77fb846795edbc5c43e05"
CROSS_JSONL = os.path.join(OUT, "crosscheck-top10-joint-third-20261118.jsonl")
K34_JSON = os.path.join(OUT, "cost16-survival-k34-20261118.json")
RES_JSONL = os.path.join(OUT, "cost16-survival-k10-20261118.jsonl")
RES_JSON = os.path.join(OUT, "cost16-survival-k10-20261118.json")

TARGET = "00000000000000003800000008001000"
R = 31


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


class MyPm:
    """Independent weighted perfect-matching counter (memoized, lowest-row
    anchored).  Same mathematics as the published PmLazy, written
    separately (third-implementation lineage)."""

    def __init__(self, edge_w, r):
        self.ew = edge_w
        self.r = r
        self.memo = {0: 1}

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


def load_top10():
    b = open(AGG_PATH, "rb").read()
    assert git_blob_sha(b) == AGG_PIN, "aggregate pin"
    agg = json.loads(b)
    top10 = agg["derived"]["top50_by_membership"][:10]
    assert all(e["kind"] == "pair" for e in top10)
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top10)}
    m = [e["membership"] for e in top10]
    total = agg["derived"]["total_minimum_covers"]
    return rows, m, total


def pub_pair_joint():
    b = open(PUB_JOINT_JSONL, "rb").read()
    assert git_blob_sha(b) == PUB_JOINT_PIN, "published joint JSONL pin"
    out = {}
    for line in b.decode().splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        if "idx_i" in e:
            out[(e["idx_i"], e["idx_j"])] = e
    assert len(out) == 45
    return out


def cross_pair_joint():
    out = {}
    with open(CROSS_JSONL) as f:
        for line in f:
            e = json.loads(line)
            if "idx_i" in e:
                out[(e["idx_i"], e["idx_j"])] = e
    assert len(out) == 45
    return out


def mults(rows, combo):
    """row -> coverage count for the union of the roots in combo."""
    c = {}
    for i in combo:
        for r in rows[i]:
            c[r] = c.get(r, 0) + 1
    return c


def classify_triple(rows, combo):
    """Return (kind, union, reason):
    'b_only'  -> exactly one row covered 2x, others 1x: B-type-only,
                 j3 = pm(V \\ union)
    'zero3x'  -> some row covered >= 3x
    'zero2x2' -> two rows covered 2x
    'disjoint'-> all rows distinct (A-type possible; NOT expected among
                 top-10; abort if seen)
    """
    c = mults(rows, combo)
    if max(c.values()) >= 3:
        trip = sorted(r for r, v in c.items() if v >= 3)
        return ("zero3x", sorted(c), "row %s covered >=3x" % trip)
    twos = sorted(r for r, v in c.items() if v == 2)
    if len(twos) >= 2:
        return ("zero2x2", sorted(c), "rows %s both covered 2x" % twos)
    if len(twos) == 1:
        return ("b_only", sorted(c), "row %s is the unique double" % twos)
    return ("disjoint", sorted(c), "all rows distinct")


def quad_invalid(rows, quad):
    """True if the 4-subset cannot be part of any A- or B-type cover.
    Valid patterns would be: all rows 1x (A possible) or exactly one
    row 2x (B possible)."""
    c = mults(rows, quad)
    if max(c.values()) >= 3:
        return True
    return sum(1 for v in c.values() if v == 2) != 1


def full_mask():
    return (1 << R) - 1


def append(rec):
    with open(RES_JSONL, "a") as f:
        f.write(json.dumps(rec) + "\n")


def done_triples():
    done = set()
    if os.path.exists(RES_JSONL):
        with open(RES_JSONL) as f:
            for line in f:
                e = json.loads(line)
                if e.get("kind") == "triple":
                    done.add(tuple(e["combo"]))
    return done


def run_mode(P, slice_arg):
    rows, m, total = load_top10()
    edge_w = P["edge_w"]
    triples = list(itertools.combinations(range(10), 3))
    # slices of 40: 3 invocations expected (0-39, 40-79, 80-119)
    lo = slice_arg * 40
    hi = min(lo + 40, len(triples))
    done = done_triples()
    t00 = time.time()
    for combo in triples[lo:hi]:
        if combo in done:
            continue
        kind, union, reason = classify_triple(rows, combo)
        if kind in ("zero3x", "zero2x2"):
            rec = {"kind": "triple", "combo": list(combo),
                   "class": kind, "union": union, "joint": 0,
                   "reason": reason}
            append(rec)
            print("[t%s %s] %s -> 0" % (kind, combo, reason), flush=True)
            continue
        if kind == "disjoint":
            raise SystemExit("unexpected disjoint triple %s -- A-type "
                             "formulas required, abort" % (combo,))
        pm = MyPm(edge_w, R)
        mask = full_mask()
        for u in union:
            mask &= ~(1 << u)
        t0 = time.time()
        val = pm.count(mask)
        rec = {"kind": "triple", "combo": list(combo),
               "class": "b_only", "union": union, "joint": val,
               "reason": reason,
               "memo_states": len(pm.memo),
               "sec": round(time.time() - t0, 1)}
        append(rec)
        print("[b_only %s] union=%s j3=%d memo=%d %.1fs"
              % (combo, union, val, len(pm.memo), rec["sec"]), flush=True)
    print("[slice %d] done %d/%d in %.1fs"
          % (slice_arg, len(done_triples()), len(triples),
             time.time() - t00), flush=True)
    return 0


def classify_mode():
    rows, m, total = load_top10()
    census = {"b_only": 0, "zero3x": 0, "zero2x2": 0, "disjoint": 0}
    for combo in itertools.combinations(range(10), 3):
        census[classify_triple(rows, combo)[0]] += 1
    print(json.dumps(census))
    return 0


def load_triples():
    out = {}
    with open(RES_JSONL) as f:
        for line in f:
            e = json.loads(line)
            if e.get("kind") == "triple":
                key = tuple(e["combo"])
                if key in out:
                    assert out[key]["joint"] == e["joint"]
                out[key] = e
    assert len(out) == 120
    return out


def finalize_mode():
    checks = []

    def chk(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok), "detail": detail})

    rows, m, total = load_top10()
    pub = pub_pair_joint()
    cross = cross_pair_joint()

    # hub property: every top-10 root contains row 18 or 19
    hub_ok = all(18 in rows[i] or 19 in rows[i] for i in range(10))
    chk("top10.hub_rows_18_19", hub_ok,
        {str(i): list(rows[i]) for i in range(10)})

    # pairwise: published == third-impl crosscheck on all 45
    chk("pairs45.pub_eq_third_impl",
        all(pub[k]["joint"] == cross[k]["joint_mine"]
            and pub[k]["joint_A"] == cross[k]["joint_A_mine"]
            and pub[k]["joint_B"] == cross[k]["joint_B_mine"]
            for k in pub))
    j2 = {k: pub[k]["joint"] for k in pub}

    triples = load_triples()
    # every triple classified; disjoint must never appear
    classes = [e["class"] for e in triples.values()]
    chk("triples.count_120", len(triples) == 120, len(triples))
    chk("triples.no_disjoint", "disjoint" not in classes,
        {"b_only": classes.count("b_only"),
         "zero3x": classes.count("zero3x"),
         "zero2x2": classes.count("zero2x2")})
    # machine-verify the structural zeros against fresh classification
    cls_ok = True
    for combo, e in triples.items():
        kind, union, reason = classify_triple(rows, combo)
        if kind != e["class"] or union != e["union"]:
            cls_ok = False
    chk("triples.classification_recheck", cls_ok)
    # monotonicity: a plan containing all three contains each pair
    mono_ok = True
    for combo, e in triples.items():
        if e["joint"]:
            cap = min(j2[(combo[0], combo[1])], j2[(combo[0], combo[2])],
                      j2[(combo[1], combo[2])])
            if e["joint"] > cap:
                mono_ok = False
    chk("triples.le_min_pairs", mono_ok)
    j3 = {k: e["joint"] for k, e in triples.items()}

    # all 210 4-subsets structurally invalid -> quads and higher are 0
    quads_bad = all(quad_invalid(rows, q)
                   for q in itertools.combinations(range(10), 4))
    chk("quads210.all_structural_zero", quads_bad)
    chk("quads.pigeonhole_note",
        True, "each top-10 root contains row 18 or 19 -> any 4-subset "
              "has a >=3x row or two 2x rows; higher orders follow by "
              "monotonicity (contain a 4-subset)")

    kill = {}
    for k in range(1, 11):
        v = 0
        for i in range(k):
            v += m[i]
        for i in range(k):
            for j in range(i + 1, k):
                v -= j2[(i, j)]
        for c in itertools.combinations(range(k), 3):
            v += j3[c]
        kill[k] = v

    chk("survival.k1_share", round(100 * kill[1] / total, 4) == 4.5975,
        100 * kill[1] / total)
    chk("survival.k2_value", kill[2] == 262073639571350318,
        {"k2_mine": str(kill[2])})
    # k3/k4 must reproduce the earlier k34 assembly when available
    if os.path.exists(K34_JSON):
        k34 = json.load(open(K34_JSON))["values"]["kill"]
        chk("survival.k34_reproduce",
            kill[3] == int(k34["k3"]) and kill[4] == int(k34["k4"]),
            {"k3": str(kill[3]), "k4": str(kill[4])})
    mono = all(kill[k] <= kill[k + 1] for k in range(1, 10))
    chk("survival.k_monotone", mono and kill[10] <= total,
        [str(kill[k]) for k in range(1, 11)])
    marg_ok = all(0 <= kill[k + 1] - kill[k] <= m[k] for k in range(1, 10))
    chk("survival.marginals", marg_ok,
        {"k%d_minus_k%d" % (k + 1, k): str(kill[k + 1] - kill[k])
         for k in range(1, 10)})

    out = {
        "schema": "n11-cost16-survival-k10-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Exact survival curve k=1..10 for the 31-row cost-16 "
                  "parent (bans of the top-k pair roots by membership), "
                  "via inclusion-exclusion whose higher-order terms "
                  "collapse: every top-10 root contains hub row 18 or 19, "
                  "so no triple is disjoint (joint_A=0 everywhere), every "
                  "4-subset is structurally impossible (>=3x row or two "
                  "2x rows), and each surviving triple is B-type-only "
                  "pm(V \\ union) on a 26-row set, computed with the "
                  "independent MyPm counter (third-implementation "
                  "lineage, no PmLazy import)"),
        "inputs": {
            "groups_aggregate": {"git_blob_sha1": AGG_PIN},
            "published_joint_jsonl": {"git_blob_sha1": PUB_JOINT_PIN,
                                      "commit": "537a4458"},
            "third_impl_crosscheck":
                "crosscheck-top10-joint-third-20261118.jsonl (45/45 match)",
            "parent_pickle": "(regenerable via the canonical loader)",
        },
        "structure": {
            "top10": [{"idx": i, "rows": list(rows[i]),
                       "membership": str(m[i])} for i in range(10)],
            "hub_property": "every top-10 root contains row 18 or 19",
            "triple_census": {"b_only": classes.count("b_only"),
                              "zero3x": classes.count("zero3x"),
                              "zero2x2": classes.count("zero2x2")},
            "quad_note": ("all 210 4-subsets verified structurally "
                          "impossible; quints and higher vanish by "
                          "monotonicity"),
        },
        "values": {
            "kill": {("k%d" % k): str(kill[k]) for k in range(1, 11)},
            "kill_share_percent": {("k%d" % k): round(100 * kill[k] / total, 6)
                                    for k in range(1, 11)},
            "marginals": {"k%d_minus_k%d" % (k + 1, k):
                          str(kill[k + 1] - kill[k]) for k in range(1, 10)},
            "triples": {"%d%d%d" % c: {"class": triples[c]["class"],
                                       "joint": str(j3[c])}
                        for c in sorted(j3)},
            "total_minimum_covers": str(total),
            "surviving_after_top10_bans": str(total - kill[10]),
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all(c["pass"] for c in checks),
        "interpretation_guard": ("Survival points count minimum cover "
                                  "plans containing at least one banned "
                                  "root. They are cover-plan combinatorics, "
                                  "not search costs or verdicts. "
                                  "REFUTED-D10 and STERILE are not LOSS "
                                  "proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots "
                           "{49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 "
                           "remain UNKNOWN."),
    }
    with open(RES_JSON, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    print(json.dumps({"checks": len(checks),
                      "all_pass": out["all_pass"],
                      "failed": [c["name"] for c in checks if not c["pass"]]},
                     indent=1))
    return 0 if out["all_pass"] else 1


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    P = load_parent()
    if mode == "run":
        sl = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        return run_mode(P, sl)
    if mode == "classify":
        return classify_mode()
    if mode == "finalize":
        return finalize_mode()
    print("usage: run [slice] | classify | finalize")
    return 2


if __name__ == "__main__":
    sys.exit(main())
