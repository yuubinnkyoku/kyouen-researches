#!/usr/bin/env python3
"""Chunked pair-membership phase B for the 31-row cost-16 parent
00000000000000003800000008001000.

The single-shot phase B of cost16_parent_membership_20261118.py was killed
by the host 4/4 times (traceback-less SIGKILL, first diagnosed as a
container RAM ceiling; follow-up RSS measurement showed the kills are a
~2-minute host time window, not memory: see the companion log
2026-11-18-n11-cost16-phaseb-groups-design.md). This runner splits the 425
pair types (all multiplicity 1) into contiguous groups; each invocation
computes one group with a fresh shared-memo anchored lazy matching DP and
appends one JSONL record per root, so a killed invocation loses nothing and
can be rerun (records already present are skipped).

All formulas and the PmLazy implementation are imported verbatim from the
published, landing-verified cost16_parent_membership_20261118.py (whose
implementation reproduced all 1,505 singleton memberships of the published
29-row runner-up output, 0 mismatches), so the membership lineage is
identical to the published phase A.

Group values are group-composition independent: pm values do not depend on
memo history, so regrouping only changes speed, never numbers.

Provenance note: this published copy was reconstructed from the executed
script's source after a host environment reset destroyed the working
filesystem; byte-identity to the executed file could not be re-verified.
Functional identity (formulas, asserts, resume design, STATE_CAP=12M,
rss_mb instrumentation) is asserted, and the 13 exact pair-membership
values recorded in the companion log are the authoritative outputs of the
executed version; rerunning any recorded type must reproduce them.

Modes:
  groups:    python3 cost16_phase_b_groups_20261118.py GS G [BUDGET]
             compute pair types sorted[(a,b)][G*GS:(G+1)*GS], fresh memo.
  aggregate: python3 cost16_phase_b_groups_20261118.py aggregate
             verify identities, compute exact B-type total and final
             b-phase output from the JSONL + pinned phase-A output.
  direct:    python3 cost16_phase_b_groups_20261118.py direct D [BUDGET]
             independent B_direct contribution of one doubly-covered row D:
             sum over a<b!=D with edges w(D,a)w(D,b) pm(full^d^a^b),
             appended to output/cost16-b-direct-20261118.jsonl.
"""
import json, os, sys, time, gc, resource
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
import cost16_parent_membership_20261118 as base

TARGET = "00000000000000003800000008001000"
COVER_TABLE_PIN = "4e4a911d0e05779437d4a8e97685a8feb66c0d25"
COVER_TABLE_REL = ("research/experiments/n11-head1410-partial-parent-"
                   "nonsterile-children-20261118/output/"
                   "parent-minimum-cover-cost-table-20261118.json")
PHASE_A_OUT = os.path.join(HERE, "output", "cost16-a-phase-20261118.json")
PHASE_A_PIN = "fe4b4b559fd8c3fdc9bc9b9f40a048fc3217c55b"
GROUPS_JSONL = os.path.join(HERE, "output", "cost16-b-groups-20261118.jsonl")
DIRECT_JSONL = os.path.join(HERE, "output", "cost16-b-direct-20261118.jsonl")


def load_parent():
    table = json.loads(base.read_pinned(COVER_TABLE_REL, COVER_TABLE_PIN))
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
    assert len(P["proot_rows"]) == 1908
    mult = {len(rl) for rl in P["pair_roots"].values()}
    assert mult == {1}, mult
    assert len(P["pair_roots"]) == 425, len(P["pair_roots"])
    hist = defaultdict(int)
    for root, cov in P["proot_rows"].items():
        hist[len(cov)] += 1
    assert dict(hist) == {1: 1483, 2: 425}, dict(hist)
    return r, k


def append(rec, path):
    with open(path, "a") as f:
        f.write(json.dumps(rec) + "\n")


def mode_groups(gs, g, budget):
    P, tbl = load_parent()
    r, k = check_structure(P, tbl)
    pair_roots = P["pair_roots"]; edge_w = P["edge_w"]
    w1 = {s: len(rl) for s, rl in P["singleton_roots"].items()}
    for s in range(r):
        w1.setdefault(s, 0)
    types = sorted(pair_roots.keys())
    assert len(types) == 425
    lo, hi = g * gs, min((g + 1) * gs, len(types))
    if lo >= len(types):
        print("[groups] group %d out of range (%d types)" % (g, len(types)))
        return 0
    done = set()
    if os.path.exists(GROUPS_JSONL):
        with open(GROUPS_JSONL) as f:
            for line in f:
                e = json.loads(line)
                if not e.get("summary"):
                    done.add(e["root"])
    todo = [t for t in types[lo:hi]
            if pair_roots[t][0] not in done]
    print("[groups] group %d slice [%d:%d) todo %d/%d (done total %d)"
          % (g, lo, hi, len(todo), hi - lo, len(done)), flush=True)
    if not todo:
        return 0
    base.STATE_CAP = 12_000_000
    base.BUDGET_SECONDS = budget
    pm = base.PmLazy(edge_w, r)
    full = (1 << r) - 1
    t0 = time.time()
    n = 0
    for e in todo:
        root = pair_roots[e][0]
        ea, eb = e
        ea_bit = 1 << ea; eb_bit = 1 << eb
        bmask = full & ~(ea_bit | eb_bit)
        a_part = 0
        for s in range(r):
            if w1[s] and s != ea and s != eb:
                a_part += w1[s] * pm.get(bmask ^ (1 << s))
        b_part = 0
        for d in e:
            for z in range(r):
                if z == ea or z == eb:
                    continue
                wz = edge_w.get((min(d, z), max(d, z)), 0)
                if wz:
                    b_part += wz * pm.get(bmask ^ (1 << z))
        for d in range(r):
            if d == ea or d == eb:
                continue
            dbit = 1 << d
            for a2 in range(r):
                if a2 == d or a2 == ea or a2 == eb:
                    continue
                wa = edge_w.get((min(d, a2), max(d, a2)), 0)
                if not wa:
                    continue
                for b2 in range(a2 + 1, r):
                    if b2 == ea or b2 == eb:
                        continue
                    wb = edge_w.get((min(d, b2), max(d, b2)), 0)
                    if wb:
                        b_part += wa * wb * pm.get(bmask ^ dbit ^ (1 << a2) ^ (1 << b2))
        append({"root": root, "pair": [ea, eb], "a_part": a_part,
                "b_part": b_part, "memo_states": len(pm.memo),
                "rss_mb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024,
                "gets": pm.gets, "sec_root": round(time.time() - t0, 1),
                "group": g}, GROUPS_JSONL)
        n += 1
        print("[groups] root %s pair %s a=%d b=%d memo=%d %.1fs"
              % (root, e, a_part, b_part, len(pm.memo), time.time() - t0),
              flush=True)
        if time.time() - t0 > budget:
            print("[groups] budget hit after %d roots" % n, flush=True)
            break
    append({"summary": True, "group": g, "slice": [lo, hi],
            "computed": n, "remaining_in_slice": len(todo) - n,
            "memo_states_final": len(pm.memo), "gets": pm.gets,
            "seconds": round(time.time() - t0, 1)}, GROUPS_JSONL)
    print("[groups] group %d done: computed %d remaining %d memo %d"
          % (g, n, len(todo) - n, len(pm.memo)))
    return 0


def read_groups():
    recs = {}
    summaries = []
    with open(GROUPS_JSONL) as f:
        for line in f:
            e = json.loads(line)
            if e.get("summary"):
                summaries.append(e)
            else:
                if e["root"] in recs:
                    raise SystemExit("duplicate root record " + e["root"])
                recs[e["root"]] = e
    return recs, summaries


def mode_aggregate():
    P, tbl = load_parent()
    r, k = check_structure(P, tbl)
    pair_roots = P["pair_roots"]
    root_pair = {root: e for e, rl in pair_roots.items() for root in rl}
    with open(PHASE_A_OUT, "rb") as f:
        pa_bytes = f.read()
    if base.git_blob_sha(pa_bytes) != PHASE_A_PIN:
        raise SystemExit("phase-A output pin mismatch")
    pa = json.loads(pa_bytes)
    A = pa["derived"]["type_A_total"]
    per_row = pa["derived"]["singleton_membership_stats"]["per_row"]
    recs, summaries = read_groups()
    checks = []
    def check(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok),
                       "detail": detail if isinstance(detail, str)
                       else json.dumps(detail)})
    types = sorted(pair_roots.keys())
    roots_expected = {pair_roots[t][0]: t for t in types}
    check("roots.count", len(recs) == 425, len(recs))
    check("roots.set_match", set(recs) == set(roots_expected),
          len(set(recs) ^ set(roots_expected)))
    check("records.pair_consistent",
          all(tuple(recs[root]["pair"]) == roots_expected[root] for root in recs))
    sum_a = sum(e["a_part"] for e in recs.values())
    sum_b = sum(e["b_part"] for e in recs.values())
    check("identity.sum_a_eq_15A", sum_a == 15 * A, {"sum_a": str(sum_a), "15A": str(15 * A)})
    check("identity.sum_b_divisible_16", sum_b % 16 == 0, str(sum_b))
    B = sum_b // 16
    total = A + B
    mem = {}
    mem_A = {}; mem_B = {}
    for root, e in recs.items():
        mem[root] = e["a_part"] + e["b_part"]
        mem_A[root] = e["a_part"]; mem_B[root] = e["b_part"]
    root_row = {root: s for s, rl in P["singleton_roots"].items() for root in rl}
    for root, s in root_row.items():
        v = int(per_row[str(s)])
        mem[root] = v; mem_A[root] = v; mem_B[root] = 0
    check("identity.sum_all_eq_16total",
          sum(mem.values()) == 16 * total,
          {"sum_all": str(sum(mem.values())), "16total": str(16 * total)})
    wit = tbl["witness_roots"]
    check("witness.membership_positive", all(mem[x] > 0 for x in wit))
    check("witness.A_split",
          sorted(len(P["proot_rows"][x]) for x in wit) == [1] + [2] * 15)
    nz = {"count": sum(1 for v in mem.values() if v > 0),
          "min": min(v for v in mem.values() if v > 0),
          "max": max(mem.values()),
          "singleton_max": max(v for root, v in mem.items() if root in root_row),
          "pair_min": min(v for root, v in mem.items() if root in root_pair),
          "pair_max": max(v for root, v in mem.items() if root in root_pair)}
    check("all_roots_positive", nz["count"] == len(mem), nz["count"])
    by_mem = sorted(mem, key=lambda x: (-mem[x], x))
    top50 = [{"root": x, "membership": mem[x],
              "kind": "pair" if x in root_pair else "singleton",
              "rows_covered": list(root_pair[x]) if x in root_pair else [root_row[x]],
              "membership_A": mem_A[x], "membership_B": mem_B[x]}
             for x in by_mem[:50]]
    out = {
        "schema": "n11-cost16-parent-b-phase-groups-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Exact B-type total and all 425 pair-root memberships (A/B split) "
                  "for the 31-row cost-16 parent 00000000000000003800000008001000"),
        "inputs": {
            "cover_table": {"path": COVER_TABLE_REL, "git_blob_sha1": COVER_TABLE_PIN},
            "phase_a_output": {"path": ("research/experiments/n11-head1410-partial-parent-"
                                        "nonsterile-children-20261118/output/"
                                        "cost16-a-phase-20261118.json"),
                               "git_blob_sha1": PHASE_A_PIN},
            "candidate_roots": {"path": "(regenerated) output/global-candidate-roots-20261118.jsonl",
                                "regenerated_by": "enumerate_global_candidate_roots_20261118.py"},
            "groups_jsonl": {"path": "(appended) output/cost16-b-groups-20261118.jsonl",
                             "records": len(recs)},
        },
        "method": ("The single-shot phase B was host-killed 4/4 at a ~2-minute "
                   "wall-time window (not memory: RSS peaked 1001MB at 10.3M memo "
                   "states, far below the 3.2GB ceiling). This output aggregates "
                   "per-pair-root memberships computed in contiguous fresh-memo "
                   "group invocations of the same published PmLazy implementation. "
                   "pm values are memo-history independent, so group composition "
                   "affects only speed. Identities: sum(a_part)==15*A against the "
                   "pinned phase-A A-type total, sum(b_part)==16*B, "
                   "sum(all)==16*(A+B)."),
        "derived": {
            "rows": r, "minimum_size": k,
            "total_minimum_covers": total,
            "type_A_disjoint": A,
            "type_B_one_duplicate_row": B,
            "membership": {x: mem[x] for x in sorted(mem)},
            "membership_A_part_pair_roots": {x: mem_A[x] for x in sorted(recs)},
            "membership_B_part_pair_roots": {x: mem_B[x] for x in sorted(recs)},
            "membership_nonzero_stats": nz,
            "top50_by_membership": top50,
            "group_summaries": summaries,
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all(c["pass"] for c in checks),
        "deferred": ("top-10 joint memberships and the direct B cross-check "
                     "(sum_d B_direct) are follow-up computations and are not "
                     "claimed here."),
        "interpretation_guard": ("Cover-plan combinatorics only. Membership counts are "
                                 "not search costs or verdicts. REFUTED-D10 and STERILE "
                                 "are not LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
                           "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    out_path = os.path.join(HERE, "output", "cost16-b-phase-groups-20261118.json")
    with open(out_path, "w") as f:
        f.write(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"A": A, "B": B, "total": total, "nz": nz,
                      "checks": len(checks), "all_pass": out["all_pass"],
                      "top5": [{"kind": e["kind"], "membership": e["membership"]}
                               for e in top50[:5]]}, indent=1))
    return 0 if out["all_pass"] else 1


def mode_direct(d, budget):
    P, tbl = load_parent()
    r, k = check_structure(P, tbl)
    edge_w = P["edge_w"]
    done_d = set()
    if os.path.exists(DIRECT_JSONL):
        with open(DIRECT_JSONL) as f:
            for line in f:
                e = json.loads(line)
                if not e.get("summary"):
                    done_d.add(e["d"])
    if d in done_d:
        print("[direct] row %d already recorded" % d)
        return 0
    base.STATE_CAP = 8_000_000
    base.BUDGET_SECONDS = budget
    pm = base.PmLazy(edge_w, r)
    full = (1 << r) - 1
    dbit = 1 << d
    t0 = time.time()
    nbrs = [a for a in range(r)
            if a != d and edge_w.get((min(d, a), max(d, a)))]
    contrib = 0
    terms = 0
    for i in range(len(nbrs)):
        a = nbrs[i]
        wa = edge_w[(min(d, a), max(d, a))]
        for j in range(i + 1, len(nbrs)):
            b = nbrs[j]
            wb = edge_w[(min(d, b), max(d, b))]
            contrib += wa * wb * pm.get(full ^ dbit ^ (1 << a) ^ (1 << b))
            terms += 1
    append({"d": d, "terms": terms, "contrib": contrib,
            "memo_states": len(pm.memo), "gets": pm.gets,
            "sec": round(time.time() - t0, 1)}, DIRECT_JSONL)
    print("[direct] row %d terms %d contrib %d memo %d %.1fs"
          % (d, terms, contrib, len(pm.memo), time.time() - t0), flush=True)
    return 0


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "direct":
        d = int(sys.argv[2])
        budget = float(sys.argv[3]) if len(sys.argv) > 3 else 240.0
        return mode_direct(d, budget)
    if len(sys.argv) >= 3 and sys.argv[1].isdigit() and sys.argv[2].isdigit():
        return mode_groups(int(sys.argv[1]), int(sys.argv[2]),
                           float(sys.argv[3]) if len(sys.argv) > 3 else 240.0)
    if len(sys.argv) >= 2 and sys.argv[1] == "aggregate":
        return mode_aggregate()
    print(__doc__)
    return 2

if __name__ == "__main__":
    sys.exit(main())
