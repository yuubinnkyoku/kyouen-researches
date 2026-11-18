#!/usr/bin/env python3
"""Exact ban-survival curve for the 31-row cost-16 parent
00000000000000003800000008001000 (minimum cover cost 16).

Bans the k pair roots with the highest published membership (published
phase-B groups aggregate, git blob 31bdefdb; all top-8 roots are pair
roots and all 425 pair types have multiplicity 1, so banning a root
deletes its pair type) and exactly recomputes

  A_k = sum_s w1[s] * pm_k(V \\ {s})                     (A-type covers)
  B_k = sum_d B_d(k),  B_d(k) = sum_{a<b in N'(d)} w'(d,a) w'(d,b)
                             * pm_k(V \\ {d,a,b})      (B-type covers)

with the published PmLazy implementation imported from
cost16_parent_membership_20261118 (same lineage as phase A / phase B /
the groups runner). pm values are memo-history independent, so the
per-slice fresh-memo design below computes the same exact integers as a
single shared-memo run (the published groups run validated this
equivalence).

Every size-16 cover of the 31 rows is A-type (15 pairs + 1 singleton) or
B-type (16 pairs, exactly one doubly-covered row d), so A_k + B_k is the
exact number of minimum covers avoiding the banned roots.

Points k = 0, 1, 2 are NOT recomputed here: k=0 is the published
A16+B16 total, k=1 = total - membership(top1) exactly (a single ban
cannot overlap itself), k=2 = total - (m1 + m2 - joint12) with the joint
from the published top-10 joint output. This script computes the NEW
points k = 4 and k = 8 (any k works) so the curve covers k in
{0,1,2,4,8}.

Modes:
  point K D_FROM D_TO [BUDGET]
      compute A_k (when D_FROM == 0) and B_d for d in [D_FROM, D_TO),
      appending one JSONL record per (k, d); already-recorded (k, d) are
      skipped, so a killed invocation loses nothing (resume-safe).
  assemble
      verify identities and assemble the survival-curve output JSON
      (deterministic: no timing fields are copied into the output).
"""
import json, os, sys, time, gc, hashlib, resource

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
import cost16_parent_membership_20261118 as base

TARGET = "00000000000000003800000008001000"
COVER_TABLE_REL = ("research/experiments/n11-head1410-partial-parent-"
                   "nonsterile-children-20261118/output/"
                   "parent-minimum-cover-cost-table-20261118.json")
GROUPS_AGG_REL = ("research/experiments/n11-head1410-partial-parent-"
                  "nonsterile-children-20261118/output/"
                  "cost16-b-phase-groups-20261118.json")
JOINT_REL = ("research/experiments/n11-head1410-partial-parent-"
             "nonsterile-children-20261118/output/"
             "cost16-top10-joint-20261118.json")
JOINT_SHA256 = ("b84e5c3c12e508e2fd490dd18f35a48020ce66ab0ad5c98"
                "9220a20eaeaec80fb")
PHASE_A_REL = ("research/experiments/n11-head1410-partial-parent-"
               "nonsterile-children-20261118/output/"
               "cost16-a-phase-20261118.json")
JSONL = os.path.join(HERE, "output", "cost16-ban-survival-20261118.jsonl")


def read_sha256(rel, pin):
    with open(os.path.join(ROOT, rel), "rb") as f:
        data = f.read()
    if hashlib.sha256(data).hexdigest() != pin:
        raise SystemExit("sha256 mismatch: " + rel)
    return data


def load_parent():
    table = json.loads(base.read_pinned(COVER_TABLE_REL, "4e4a911d"
                                         "0e05779437d4a8e97685a8fe"
                                         "b66c0d25"))
    tbl = {e["hex"]: e for e in table["derived"]["table"]}[TARGET]
    row_cands = {}
    with open(os.path.join(HERE, "output",
                           "global-candidate-roots-20261118.jsonl")) as f:
        for line in f:
            e = json.loads(line)
            row_cands[e["row"]] = e
    P = base.build_parent(TARGET, row_cands, {})
    del row_cands
    gc.collect()
    return P, tbl


def check_structure(P, tbl):
    r = len(P["target"])
    k = tbl["witness_size"]
    assert r == 31 and k == 16 and tbl["exact"], (r, k)
    assert len(P["pair_roots"]) == 425
    assert all(len(rl) == 1 for rl in P["pair_roots"].values())
    hist = {}
    for cov in P["proot_rows"].values():
        hist[len(cov)] = hist.get(len(cov), 0) + 1
    assert hist == {1: 1483, 2: 425}, hist
    return r, k


def top_pair_roots(agg, n):
    top = [x for x in agg["derived"]["top50_by_membership"]
           if x["kind"] == "pair"]
    if len(top) < n:
        raise SystemExit("not enough pair roots in top50")
    return top


def read_done():
    done = {}
    if os.path.exists(JSONL):
        with open(JSONL) as f:
            for line in f:
                e = json.loads(line)
                if not e.get("summary"):
                    done[(e["k"], e["d"])] = e
    return done


def append(rec):
    with open(JSONL, "a") as f:
        f.write(json.dumps(rec) + "\n")


def mode_point(k, d_from, d_to, budget):
    agg = json.loads(base.read_pinned(GROUPS_AGG_REL, "31bdefdb2e"
                                      "2cc90b706cbb8090e98eb5eece4d8"
                                      "7"))
    top = top_pair_roots(agg, k)
    banned_roots = [x["root"] for x in top[:k]]
    done = read_done()
    P, tbl = load_parent()
    r, kk = check_structure(P, tbl)
    root_pair = {rl[0]: e for e, rl in P["pair_roots"].items()}
    banned_types = [root_pair[x] for x in banned_roots]
    edge_w = dict(P["edge_w"])
    for e in banned_types:
        del edge_w[e]
    assert len(edge_w) == 425 - k, len(edge_w)
    w1 = {s: len(rl) for s, rl in P["singleton_roots"].items()}
    for s in range(r):
        w1.setdefault(s, 0)
    full = (1 << r) - 1
    base.STATE_CAP = 16_000_000
    t0 = time.time()
    if d_from == 0 and (k, "A") not in done:
        base.BUDGET_SECONDS = 600.0
        pm = base.PmLazy(edge_w, r)
        A = 0
        for s in range(r):
            if w1[s]:
                A += w1[s] * pm.get(full ^ (1 << s))
        append({"k": k, "d": "A", "value": A,
                "memo_states": len(pm.memo),
                "rss_mb": resource.getrusage(
                    resource.RUSAGE_SELF).ru_maxrss // 1024,
                "gets": pm.gets, "sec": round(time.time() - t0, 1)})
        print("[point] k=%d A=%d memo=%d %.1fs" %
              (k, A, len(pm.memo), time.time() - t0), flush=True)
        del pm
        gc.collect()
    base.BUDGET_SECONDS = budget
    for d in range(max(d_from, 0), d_to):
        if (k, d) in done:
            continue
        if time.time() - t0 > budget:
            print("[point] budget hit before d=%d" % d, flush=True)
            break
        ts = time.time()
        pm = base.PmLazy(edge_w, r)
        dbit = 1 << d
        nbrs = [a for a in range(r)
                if a != d and edge_w.get((min(d, a), max(d, a)))]
        Bd = 0
        for i in range(len(nbrs)):
            a = nbrs[i]
            wa = edge_w[(min(d, a), max(d, a))]
            for j in range(i + 1, len(nbrs)):
                b = nbrs[j]
                wb = edge_w[(min(d, b), max(d, b))]
                Bd += wa * wb * pm.get(full ^ dbit ^ (1 << a) ^ (1 << b))
        append({"k": k, "d": d, "value": Bd,
                "memo_states": len(pm.memo),
                "rss_mb": resource.getrusage(
                    resource.RUSAGE_SELF).ru_maxrss // 1024,
                "gets": pm.gets, "sec": round(time.time() - ts, 1)})
        print("[point] k=%d d=%d B_d=%d memo=%d %.1fs" %
              (k, d, Bd, len(pm.memo), time.time() - ts), flush=True)
        del pm
        gc.collect()
    append({"summary": True, "k": k, "slice": [d_from, d_to],
            "seconds": round(time.time() - t0, 1)})
    return 0


def mode_assemble():
    agg = json.loads(base.read_pinned(GROUPS_AGG_REL, "31bdefdb2e"
                                      "2cc90b706cbb8090e98eb5eece4d8"
                                      "7"))
    joint_out = json.loads(read_sha256(JOINT_REL, JOINT_SHA256))
    top = top_pair_roots(agg, 8)
    mem = {x["root"]: x["membership"] for x in top}
    pub_total = agg["derived"]["total_minimum_covers"]
    pub_A = agg["derived"]["type_A_disjoint"]
    pub_B = agg["derived"]["type_B_one_duplicate_row"]
    sp = joint_out["derived"]["exact_survival_points"]
    checks = []

    def check(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok),
                       "detail": detail if isinstance(detail, str)
                       else json.dumps(detail)})
        print(("PASS " if ok else "FAIL ") + name, flush=True)

    # published/derived exact points
    check("k0.total_split", pub_total == pub_A + pub_B,
          {"A": str(pub_A), "B": str(pub_B)})
    k1_pred = pub_total - mem[top[0]["root"]]
    k2_pred = pub_total - (mem[top[0]["root"]] + mem[top[1]["root"]]
                           - sp["k2_joint12"])
    check("k1.matches_published_joint_output",
          k1_pred == pub_total - sp["k1_killed"])
    check("k2.matches_published_joint_output",
          k2_pred == pub_total - sp["k2_killed"])
    derived_points = {
        0: {"total": pub_total,
            "provenance": "published A16+B16 (groups aggregate)"},
        1: {"total": k1_pred,
            "provenance": "total - membership(top1): exact, single ban"},
        2: {"total": k2_pred,
            "provenance": ("inclusion-exclusion with the published "
                           "top-2 joint")},
    }
    done = read_done()
    ks = sorted({e["k"] for e in done.values()})
    curve = {}
    for k in ks:
        nd = sum(1 for d in range(31) if (k, d) in done)
        check("k%d.slices_complete" % k, nd == 31 and (k, "A") in done,
              {"b_slices": nd, "a_phase": (k, "A") in done})
        if nd == 31 and (k, "A") in done:
            A = done[(k, "A")]["value"]
            Bd = sum(done[(k, d)]["value"] for d in range(31))
            curve[k] = {"type_A": A, "type_B": Bd, "total": A + Bd}
            print("[assemble] k=%d A=%d B=%d total=%d" %
                  (k, A, Bd, A + Bd), flush=True)
    if 0 in curve:
        check("k0.recomputed_split_matches_published",
              curve[0]["type_A"] == pub_A and
              curve[0]["type_B"] == pub_B,
              {"A": str(curve[0]["type_A"]), "B": str(curve[0]["type_B"])})
    if 1 in curve:
        check("k1.recomputed_matches_independence",
              curve[1]["total"] == k1_pred,
              {"recomputed": str(curve[1]["total"]),
               "prediction": str(k1_pred)})
    if 2 in curve:
        check("k2.recomputed_matches_inclusion_exclusion",
              curve[2]["total"] == k2_pred,
              {"recomputed": str(curve[2]["total"]),
               "prediction": str(k2_pred)})
    series = []
    for k in sorted(set(list(derived_points) + list(curve))):
        if k in curve:
            series.append((k, curve[k]["total"], "recomputed"))
        else:
            series.append((k, derived_points[k]["total"], "derived"))
    check("monotone_nonincreasing",
          all(series[i][1] >= series[i + 1][1]
              for i in range(len(series) - 1)),
          [str(x[1]) for x in series])
    strict = all(series[i][1] > series[i + 1][1]
                 for i in range(len(series) - 1))
    ub_ok = True
    for k, tot, _ in series:
        if k == 0:
            continue
        ub = pub_total - sum(mem[top[i]["root"]] for i in range(k))
        if tot < ub:
            ub_ok = False
            print("union bound FAIL at k=%d" % k, flush=True)
    check("union_bound", ub_ok)
    out_curve = []
    for k, tot, src in series:
        kill = pub_total - tot
        entry = {
            "k": k, "total": tot, "killed": kill,
            "kill_share": round(kill / pub_total, 6),
            "surviving_share": round(tot / pub_total, 6),
            "banned_roots": [top[i]["root"] for i in range(k)],
            "source": src,
        }
        if k in curve:
            entry["type_A"] = curve[k]["type_A"]
            entry["type_B"] = curve[k]["type_B"]
        else:
            entry["provenance"] = derived_points[k]["provenance"]
        out_curve.append(entry)
    naive = [{"k": k,
              "sum_membership_topk": sum(mem[top[i]["root"]]
                                        for i in range(k)),
              "exact_kill": pub_total - tot}
             for k, tot, _ in series if k]
    out = {
        "schema": "n11-cost16-ban-survival-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Exact ban-survival curve for the 31-row cost-16 parent "
                  "00000000000000003800000008001000: ban the top-k "
                  "membership pair roots and exactly recompute the "
                  "minimum-cover totals"),
        "inputs": {
            "cover_table": {
                "path": COVER_TABLE_REL,
                "git_blob_sha1": ("4e4a911d0e05779437d4a8e97685a8"
                                  "feb66c0d25")},
            "phase_a_output": {"path": PHASE_A_REL},
            "phase_b_groups_aggregate": {
                "path": GROUPS_AGG_REL,
                "git_blob_sha1": ("31bdefdb2e2cc90b706cbb8090e98eb5e"
                                 "ece4d87")},
            "top10_joint_output": {
                "path": JOINT_REL,
                "git_blob_sha1": ("df52b55a81460a60b11030be8bf5c805b"
                                 "fdeb7c5"),
                "sha256": JOINT_SHA256},
            "candidate_roots": {
                "path": "(regenerated) output/global-candidate-roots-"
                        "20261118.jsonl",
                "regenerated_by": "enumerate_global_candidate_roots_"
                                  "20261118.py"},
        },
        "method": ("For each computed k the top-k membership pair roots "
                   "(published ranking) are banned by deleting their "
                   "pair type (all multiplicities 1) and the exact "
                   "A-type and B-type minimum-cover totals are "
                   "recomputed from scratch: the A phase once (shared "
                   "memo over the 31 singleton anchors), then 31 "
                   "independent per-doubled-row B slices, fresh memo per "
                   "slice, resume-safe JSONL. pm values are "
                   "memo-history independent, so per-slice fresh memos "
                   "give the same exact integers as a shared-memo run. "
                   "k=0/1/2 are the published/independently derived "
                   "exact values; any recomputed k=0/1/2 must reproduce "
                   "them (checked)."),
        "derived": {
            "rows": 31,
            "baseline_total": pub_total,
            "baseline_type_A": pub_A,
            "baseline_type_B": pub_B,
            "curve": out_curve,
            "strictly_decreasing": strict,
            "naive_membership_sum_vs_exact_kill": naive,
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all(c["pass"] for c in checks),
        "interpretation_guard": ("Cover-plan combinatorics only. The "
                                 "survival curve counts alternative "
                                 "minimum cover plans avoiding the "
                                 "banned roots; it is not a search cost "
                                 "and implies nothing about WIN/REFUTED "
                                 "verdicts of the banned roots. "
                                 "REFUTED-D10 and STERILE are not LOSS "
                                 "proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots "
                           "{49,60}/{59,60}, S2 {59,60}, and classes "
                           "1/2/4 remain UNKNOWN."),
    }
    print("assemble all_pass:", out["all_pass"], flush=True)
    with open(os.path.join(HERE, "output",
                           "cost16-ban-survival-20261118.json"), "w") as f:
        json.dump(out, f, sort_keys=True, indent=1)
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "point":
        k = int(sys.argv[2])
        d_from = int(sys.argv[3])
        d_to = int(sys.argv[4])
        budget = float(sys.argv[5]) if len(sys.argv) > 5 else 75.0
        return mode_point(k, d_from, d_to, budget)
    if mode == "assemble":
        out = mode_assemble()
        return 0 if out["all_pass"] else 1
    print("usage: point K D_FROM D_TO [BUDGET] | assemble")
    return 2


if __name__ == "__main__":
    sys.exit(main())
