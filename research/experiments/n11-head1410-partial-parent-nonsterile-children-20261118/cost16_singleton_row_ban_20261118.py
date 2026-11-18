#!/usr/bin/env python3
"""Singleton-row ban extension of the survival curve for the 31-row
cost-16 parent.

Event F_s = "the singleton of an A-type plan covers row s".  Banning ALL
singleton roots on row s (w1[s] interchangeable roots) removes exactly
the F_s plans.  Structure:

  * plans with a singleton are A-type only (a B-type cover is 16 pair
    roots, no singleton) -> every overlap term here is A-type;
  * F_s and F_s' are disjoint (an A-plan has exactly one singleton) ->
    row marginals are additive on top of the pair-ban union;
  * |F_s| = w1[s] * pm(V \\ {s})   (published per-row pm, phase A);
  * F_s n E_e = w1[s] * pm(V \\ {s} \\ e) for each top-10 pair root e;
  * F_s n E_e n E_e' is nonzero only for pairwise-disjoint e, e'
    (a shared row would be covered twice in an A-plan) and equals
    w1[s] * pm(V \\ {s} \\ e \\ e');  triples of pairwise-disjoint
    top-10 pairs do not exist (hub rows 18/19), so the I-E for
    |F_s n (union of pair events)| stops at pairs:

    marginal(s) = |F_s| - sum_e j2(s,e) + sum_{disjoint e<e'} j3(s,e')

All counts scale linearly in w1[s], so the same numbers give the
root-level marginal (ban ONE singleton root on row s) by dividing by
w1[s].  Exact mixed survival points:

    kill(10 pairs + rows s1..sj) = kill(10) + sum marginal(s_i)

Rows are ranked by |F_s| = w1[s]*pm(V\\{s}) from the pinned phase-A
per-row table; the top-3 rows (4, 0, 24) are computed here.

Counter: independent MyPm (third-implementation lineage, no PmLazy
import), one fresh shared memo per row.

Cover-plan combinatorics only.  No engine run, no verdict.

Usage:
  python3 cost16_singleton_row_ban_20261118.py run [row_rank]
  python3 cost16_singleton_row_ban_20261118.py finalize
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
AGG_PATH = os.path.join(OUT, "cost16-b-phase-groups-20261118.json")
AGG_PIN = "31bdefdb2e2cc90b706cbb8090e98eb5eece4d87"
PHASE_A_PATH = os.path.join(OUT, "cost16-a-phase-20261118.json")
PHASE_A_PIN = "fe4b4b559fd8c3fdc9bc9b9f40a048fc3217c55b"
PUB_JOINT_JSONL = os.path.join(OUT, "cost16-top10-joint-20261118.jsonl")
PUB_JOINT_PIN = "95194096b2dcb547b5b77fb846795edbc5c43e05"
K10_JSON = os.path.join(OUT, "cost16-survival-k10-20261118.json")
K10_PIN = "6be591d458e3d9b863c070b85c0196692dfe5c6d"
RES_JSONL = os.path.join(OUT, "cost16-singleton-row-ban-20261118.jsonl")
RES_JSON = os.path.join(OUT, "cost16-singleton-row-ban-20261118.json")

TARGET = "00000000000000003800000008001000"
R = 31
ROW_RANKS = [4, 0, 24]  # top-3 rows by |F_s| = w1[s]*pm(V\\{s})


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


class MyPm:
    """Independent weighted perfect-matching counter (memoized, lowest-row
    anchored).  Third-implementation lineage, no PmLazy import."""

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
    return P


def load_inputs():
    b = open(PHASE_A_PATH, "rb").read()
    assert git_blob_sha(b) == PHASE_A_PIN, "phase A pin"
    pa = json.loads(b)
    per_row = pa["derived"]["singleton_membership_stats"]["per_row"]
    b = open(AGG_PATH, "rb").read()
    assert git_blob_sha(b) == AGG_PIN, "aggregate pin"
    agg = json.loads(b)
    top10 = agg["derived"]["top50_by_membership"][:10]
    rows = {i: tuple(e["rows_covered"]) for i, e in enumerate(top10)}
    total = agg["derived"]["total_minimum_covers"]
    b = open(PUB_JOINT_JSONL, "rb").read()
    assert git_blob_sha(b) == PUB_JOINT_PIN, "published joint pin"
    shared = {}
    for line in b.decode().splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        if "idx_i" in e:
            shared[(e["idx_i"], e["idx_j"])] = bool(e["shared_row"])
    assert len(shared) == 45
    return per_row, rows, total, shared


def full_mask():
    return (1 << R) - 1


def append(rec):
    with open(RES_JSONL, "a") as f:
        f.write(json.dumps(rec) + "\n")


def done_rows():
    done = set()
    if os.path.exists(RES_JSONL):
        with open(RES_JSONL) as f:
            for line in f:
                e = json.loads(line)
                if e.get("kind") == "row":
                    done.add(e["row"])
    return done


def run_mode(P, rank):
    edge_w = P["edge_w"]
    per_row, rows, total, shared = load_inputs()
    w1 = {s: len(rl) for s, rl in P["singleton_roots"].items()}
    s = ROW_RANKS[rank]
    assert s not in done_rows()
    disjoint = sorted(k for k, v in shared.items() if not v)
    pm = MyPm(edge_w, R)
    t0 = time.time()
    base = full_mask() ^ (1 << s)
    pm_full = pm.count(base)
    j2 = {}
    for i in range(10):
        e = rows[i]
        j2[i] = pm.count(base & ~((1 << e[0]) | (1 << e[1])))
    j3 = {}
    for (i, k) in disjoint:
        ei, ek = rows[i], rows[k]
        j3["%d,%d" % (i, k)] = pm.count(
            base & ~((1 << ei[0]) | (1 << ei[1])
                     | (1 << ek[0]) | (1 << ek[1])))
    rec = {"kind": "row", "row": s, "w1": w1[s],
           "pm_full": pm_full, "per_row_pub": int(per_row[str(s)]),
           "anchor_pm": pm_full == int(per_row[str(s)]),
           "j2": {str(i): j2[i] for i in j2},
           "j3": j3,
           "memo_states": len(pm.memo),
           "sec": round(time.time() - t0, 1)}
    append(rec)
    marg_root = (pm_full - sum(j2.values()) + sum(j3.values()))
    print("[row %d] w1=%d pm=%d anchor=%s j2sum=%d j3sum=%d "
          "marg_root=%d marg_row=%d memo=%d %.1fs"
          % (s, w1[s], pm_full, rec["anchor_pm"], sum(j2.values()),
             sum(j3.values()), marg_root, w1[s] * marg_root,
             len(pm.memo), rec["sec"]), flush=True)
    return 0


def load_rows():
    out = {}
    with open(RES_JSONL) as f:
        for line in f:
            e = json.loads(line)
            if e.get("kind") == "row":
                assert e["row"] not in out
                out[e["row"]] = e
    return out


def finalize_mode():
    checks = []

    def chk(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok), "detail": detail})

    per_row, rows, total, shared = load_inputs()
    disjoint = sorted(k for k, v in shared.items() if not v)
    chk("disjoint_pairs.count_23", len(disjoint) == 23, len(disjoint))

    rowrecs = load_rows()
    chk("rows.count_3", sorted(rowrecs) == sorted(ROW_RANKS),
        sorted(rowrecs))
    chk("rows.rank_by_Fs",
        all(rowrecs[ROW_RANKS[i]]["w1"] * rowrecs[ROW_RANKS[i]]["pm_full"]
            >= rowrecs[ROW_RANKS[j]]["w1"]
            * rowrecs[ROW_RANKS[j]]["pm_full"]
            for i in range(len(ROW_RANKS))
            for j in range(i + 1, len(ROW_RANKS))))

    marg_root = {}
    for s, e in sorted(rowrecs.items()):
        chk("anchor.pm_row_%d" % s, e["anchor_pm"] and
            e["pm_full"] == int(per_row[str(s)]))
        j2 = {int(k): v for k, v in e["j2"].items()}
        chk("row%d.j2_le_pmfull" % s,
            len(j2) == 10 and all(v <= e["pm_full"] for v in j2.values()))
        j3 = e["j3"]
        chk("row%d.j3_keys_match_disjoint" % s,
            sorted(k for k in j3) ==
            sorted("%d,%d" % (i, k) for (i, k) in disjoint))
        chk("row%d.j3_le_min_j2" % s,
            all(j3["%d,%d" % (i, k)] <= min(j2[i], j2[k])
                for (i, k) in disjoint))
        m = e["pm_full"] - sum(j2.values()) + sum(j3.values())
        chk("row%d.marginal_bounds" % s, 0 <= m <= e["pm_full"],
            {"marg_root": str(m), "pm_full": str(e["pm_full"])})
        marg_root[s] = m

    b = open(K10_JSON, "rb").read()
    assert git_blob_sha(b) == K10_PIN, "k10 pin"
    k10 = json.loads(b)
    kill10 = int(k10["values"]["kill"]["k10"])
    chk("k10.pin_and_value", kill10 == 1176471942925388348)

    kill_mixed = {"pairs10": kill10}
    acc = kill10
    for j, s in enumerate(ROW_RANKS, 1):
        acc = acc + rowrecs[s]["w1"] * marg_root[s]
        kill_mixed["pairs10_plus_rows%d" % j] = acc
    chk("mixed.monotone_le_total",
        kill10 <= kill_mixed["pairs10_plus_rows3"] <= total,
        {k: str(v) for k, v in kill_mixed.items()})

    out = {
        "schema": "n11-cost16-singleton-row-ban-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Exact singleton-row ban marginals on top of the top-10 "
                  "pair-root bans for the 31-row cost-16 parent: event "
                  "F_s (A-plan singleton on row s), I-E truncated at "
                  "pairs because three pairwise-disjoint top-10 pairs do "
                  "not exist (hub rows 18/19); rows ranked by "
                  "|F_s| = w1[s]*pm(V\\{s}), top-3 rows 4/0/24 computed "
                  "with the independent MyPm counter"),
        "inputs": {
            "phase_a": {"git_blob_sha1": PHASE_A_PIN},
            "groups_aggregate": {"git_blob_sha1": AGG_PIN},
            "published_joint_jsonl": {"git_blob_sha1": PUB_JOINT_PIN},
            "survival_k10_json": {"git_blob_sha1": K10_PIN},
            "parent_pickle": "(regenerable via the canonical loader)",
        },
        "structure": {
            "event": "F_s = plans whose singleton covers row s "
                     "(banning all w1[s] singleton roots on row s)",
            "a_type_only": "a B-type cover has 16 pair roots and no "
                           "singleton, so all overlap terms are A-type",
            "rows_disjoint": "F_s and F_s' are disjoint (exactly one "
                             "singleton per A-plan) -> marginals add",
            "ie_truncation": "F_s n E_e n E_e' nonzero only for disjoint "
                             "e,e'; no three pairwise-disjoint top-10 "
                             "pairs exist, so the I-E stops at pairs",
        },
        "values": {
            "rows": {str(s): {
                "w1": rowrecs[s]["w1"],
                "pm_full": str(rowrecs[s]["pm_full"]),
                "j2": {k: str(v) for k, v in rowrecs[s]["j2"].items()},
                "j3": {k: str(v) for k, v in rowrecs[s]["j3"].items()},
                "marginal_root_level": str(marg_root[s]),
                "marginal_row_level": str(rowrecs[s]["w1"] * marg_root[s]),
            } for s in sorted(rowrecs)},
            "kill_mixed": {k: str(v) for k, v in kill_mixed.items()},
            "kill_share_percent": {
                k: round(100 * v / total, 6)
                for k, v in kill_mixed.items()},
            "total_minimum_covers": str(total),
            "root_level_note": ("a single top singleton root "
                                "(row 18 by root-level pm) has "
                                "|F| = 1,798,095,446,108,235 = 0.0606% of "
                                "total, so root-level singleton bans are "
                                "an order of magnitude weaker than any "
                                "top-10 pair ban"),
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all(c["pass"] for c in checks),
        "interpretation_guard": ("Marginals count minimum cover plans; "
                                 "cover-plan combinatorics only, not "
                                 "search costs or verdicts. REFUTED-D10 "
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
                      "failed": [c["name"] for c in checks if not c["pass"]]},
                     indent=1))
    return 0 if out["all_pass"] else 1


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    P = load_parent()
    if mode == "run":
        rank = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        return run_mode(P, rank)
    if mode == "finalize":
        return finalize_mode()
    print("usage: run [row_rank 0..2] | finalize")
    return 2


if __name__ == "__main__":
    sys.exit(main())
