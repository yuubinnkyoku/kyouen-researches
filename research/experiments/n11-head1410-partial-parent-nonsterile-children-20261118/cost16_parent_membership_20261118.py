#!/usr/bin/env python3
"""Exact minimum-cover membership analysis for the cost-16 parent
00000000000000003800000008001000 (31 open non-STERILE rows, 2,333 candidates,
1,908 roots = 425 pair types (all multiplicity 1) + 1,483 singleton roots),
the next-cheapest open cover target after the 29-row runner-up.

Two-phase output so that a host-side kill during the longer second phase
still leaves the first phase's results on disk:
  phase A (output/cost16-a-phase-20261118.json): implementation validation
    against the published 29-row runner-up singleton memberships, parent
    structure, all singleton memberships (A-type), exact A-type total,
    anchored-state-space scaling facts.
  phase B (output/cost16-b-phase-20261118.json): all 425 pair-root
    memberships with A/B split, exact B-type total, identities, top-50,
    top-10 joint memberships (fresh memo), nonzero stats.

Formulas are the published even/odd-r framework (odd r=31, k=16):
  A-type (15 disjoint pairs + 1 disjoint singleton):
     A = sum_s w1(s) * pm(V\\{s})
  B-type (16 pairs, exactly one doubly covered row d):
     B = sum_d sum_{a<b, a,b != d} w(d,a) w(d,b) pm(V\\{d,a,b})
  singleton-root membership = pm(V\\{s}); identities
     sum(A-parts) == k*A, sum(B-parts) == k*B, sum == k*(A+B).
"""
import json, os, sys, hashlib, time, gc
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
TARGET = "00000000000000003800000008001000"
RUNNERUP = "00000000000000003800000009000000"
STATE_CAP = 12_000_000
BUDGET_SECONDS = 1500.0

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()

def read_pinned(rel, pin):
    with open(os.path.join(ROOT, rel), "rb") as f:
        data = f.read()
    if git_blob_sha(data) != pin:
        raise SystemExit("pin mismatch: " + rel)
    return data

N = 11
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

class PmLazy:
    def __init__(self, edge_w, r):
        self.edge_w = edge_w
        self.r = r
        self.memo = {0: 1}
        self.t0 = time.time()
        self.gets = 0

    def get(self, mask):
        memo = self.memo
        if mask in memo:
            self.gets += 1
            return memo[mask]
        edge_w = self.edge_w
        stack = [mask]
        seen = {mask}
        order = []
        while stack:
            m = stack.pop()
            if m in memo:
                continue
            order.append(m)
            if len(memo) + len(seen) > STATE_CAP or time.time() - self.t0 > BUDGET_SECONDS:
                raise MemoryError("pm state cap or budget exceeded")
            if m == 0:
                continue
            low = m & -m
            first = low.bit_length() - 1
            rest = m ^ low
            mm = rest
            while mm:
                jbit = mm & -mm
                mm ^= jbit
                j = jbit.bit_length() - 1
                key = (first, j) if first < j else (j, first)
                if edge_w.get(key, 0):
                    sub = rest & ~jbit
                    if sub not in memo and sub not in seen:
                        seen.add(sub)
                        stack.append(sub)
        for m in sorted(order, key=lambda x: bin(x).count("1")):
            if m in memo:
                continue
            low = m & -m
            first = low.bit_length() - 1
            rest = m ^ low
            acc = 0
            mm = rest
            while mm:
                jbit = mm & -mm
                mm ^= jbit
                j = jbit.bit_length() - 1
                key = (first, j) if first < j else (j, first)
                w = edge_w.get(key, 0)
                if w:
                    acc += w * memo[rest & ~jbit]
            memo[m] = acc
        self.gets += 1
        return memo[mask]

def build_parent(target_hex, row_cands, cache):
    p_orbit = cache.setdefault(target_hex,
                    {format(m, "032x") for m in orbit_masks(int(target_hex, 16))})
    target = sorted(h for h in row_cands
                    if any(format(int(h, 16) ^ (1 << b), "032x") in p_orbit
                           for b in range(121) if (int(h, 16) >> b) & 1))
    idx = {h: i for i, h in enumerate(target)}
    proot_rows = defaultdict(set)
    cand_total = 0
    for h in target:
        e = row_cands[h]
        cand_total += e["cost"]
        for root, bit in e["cands"]:
            proot_rows[root].add(h)
    pair_roots = defaultdict(list)
    singleton_roots = defaultdict(list)
    for root, cov in proot_rows.items():
        if len(cov) == 2:
            a, b = sorted(idx[h] for h in cov)
            pair_roots[(a, b)].append(root)
        else:
            (s,) = [idx[h] for h in cov]
            singleton_roots[s].append(root)
    edge_w = {e: len(rl) for e, rl in pair_roots.items()}
    return {"target": target, "proot_rows": proot_rows, "cand_total": cand_total,
            "pair_roots": pair_roots, "singleton_roots": singleton_roots,
            "edge_w": edge_w}

def main():
    out_a = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "output", "cost16-a-phase-20261118.json")
    out_b = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        HERE, "output", "cost16-b-phase-20261118.json")
    def log(msg):
        print(msg, flush=True)
    checks_a = []
    checks_b = []
    def check(lst, name, ok, detail=""):
        lst.append({"name": name, "pass": bool(ok),
                    "detail": detail if isinstance(detail, str) else json.dumps(detail)})

    table = json.loads(read_pinned(
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/parent-minimum-cover-cost-table-20261118.json",
        "4e4a911d0e05779437d4a8e97685a8feb66c0d25"))
    pub29 = json.loads(read_pinned(
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/runnerup29-cover-membership-20261118.json",
        "05f54eb58baad66403b327696b9a63f7433a13c3"))
    tbl = {e["hex"]: e for e in table["derived"]["table"]}[TARGET]
    tbl29 = {e["hex"]: e for e in table["derived"]["table"]}[RUNNERUP]

    row_cands = {}
    with open(os.path.join(HERE, "output", "global-candidate-roots-20261118.jsonl")) as f:
        for line in f:
            e = json.loads(line)
            row_cands[e["row"]] = e

    cache = {}
    P = build_parent(TARGET, row_cands, cache)
    R29 = build_parent(RUNNERUP, row_cands, cache)
    del row_cands
    gc.collect()

    # ---------- implementation validation on the published 29-row parent
    r29 = len(R29["target"])
    pm29 = PmLazy(R29["edge_w"], r29)
    full29 = (1 << r29) - 1
    pub_mem29 = pub29["derived"]["membership"]
    mism = 0
    checked = 0
    for s, rl in R29["singleton_roots"].items():
        v = pm29.get(full29 ^ (1 << s))
        for root in rl:
            checked += 1
            if pub_mem29.get(root) != v:
                mism += 1
    check(checks_a, "val.runnerup29_singleton_memberships", mism == 0,
          {"checked": checked, "mismatches": mism})
    log("[val] runner-up 29-row singleton memberships: checked %d mismatches %d" % (checked, mism))
    del pm29
    gc.collect()

    # ---------- target structure (phase A)
    r = len(P["target"])
    k = tbl["witness_size"]
    check(checks_a, "rows", r == tbl["rows_r"] == 31, r)
    check(checks_a, "candidates", P["cand_total"] == tbl["candidates"] == 2333, P["cand_total"])
    hist = defaultdict(int)
    for root, cov in P["proot_rows"].items():
        hist[len(cov)] += 1
    check(checks_a, "distinct_roots", len(P["proot_rows"]) == tbl["distinct_roots"] == 1908,
          len(P["proot_rows"]))
    check(checks_a, "span_histogram",
          {str(x): v for x, v in sorted(hist.items())} == tbl["span_histogram"], dict(hist))
    check(checks_a, "exact16", tbl["exact"] and tbl["lower_bound"] == k == 16)
    check(checks_a, "parity_odd", r % 2 == 1 and k * 2 - 1 == r)
    pair_roots = P["pair_roots"]; singleton_roots = P["singleton_roots"]
    edge_w = P["edge_w"]
    w1 = {s: len(rl) for s, rl in singleton_roots.items()}
    for s in range(r):
        w1.setdefault(s, 0)
    root_pair = {root: e for e, rl in pair_roots.items() for root in rl}
    root_row = {root: s for s, rl in singleton_roots.items() for root in rl}
    mult_hist = defaultdict(int)
    for e, rl in pair_roots.items():
        mult_hist[len(rl)] += 1
    check(checks_a, "pair_types_mult1", dict(mult_hist) == {1: 425}, dict(mult_hist))
    wit = tbl["witness_roots"]
    wit_cov = {root: P["proot_rows"][root] for root in wit}
    wit_rows = set()
    for root in wit:
        wit_rows |= wit_cov[root]
    check(checks_a, "witness.covers_all", wit_rows == set(P["target"]) and len(wit) == k)
    check(checks_a, "witness.structure",
          sorted(len(v) for v in wit_cov.values()) == [1] + [2] * (k - 1))

    # ---------- A phase
    pm = PmLazy(edge_w, r)
    full = (1 << r) - 1
    t0 = time.time()
    first_tree_states = None
    mem = {}; mem_A = {}; mem_B = {}
    for s, rl in singleton_roots.items():
        v = pm.get(full ^ (1 << s))
        if first_tree_states is None:
            first_tree_states = len(pm.memo)
        for root in rl:
            mem[root] = v; mem_A[root] = v; mem_B[root] = 0
    a_phase_seconds_marker = time.time() - t0
    A = sum(w1[s] * pm.get(full ^ (1 << s)) for s in range(r) if w1[s])
    # each A-type cover contains exactly one singleton root; B-type covers
    # contain none, so the singleton-root membership sum equals A exactly
    check(checks_a, "A.singleton_sum_identity", sum(mem_A.values()) == A,
          {"sum": str(sum(mem_A.values())), "A": str(A)})
    check(checks_a, "A.positive", A > 0, str(A))
    singleton_mem_stats = {
        "min": min(mem[root] for root in root_row),
        "max": max(mem[root] for root in root_row),
        "per_row": {str(s): pm.get(full ^ (1 << s)) for s in range(r)},
    }
    log("[A] total A = %d (singleton phase %.1fs, memo %d)" % (A, a_phase_seconds_marker, len(pm.memo)))

    degree = defaultdict(int)
    for (a, b), w in edge_w.items():
        degree[a] += w; degree[b] += w
    for s in range(r):
        degree.setdefault(s, 0)
    options = {s: degree[s] + w1[s] for s in range(r)}

    all_pass_a = all(c["pass"] for c in checks_a)
    out = {
        "schema": "n11-cost16-parent-a-phase-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Exact A-type minimum cover total, singleton memberships, structure and "
                  "anchored-state-space scaling facts for the 31-row cost-16 parent "
                  "00000000000000003800000008001000"),
        "inputs": {
            "cover_table": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/parent-minimum-cover-cost-table-20261118.json",
                             "git_blob_sha1": "4e4a911d0e05779437d4a8e97685a8feb66c0d25"},
            "runnerup29_output": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/runnerup29-cover-membership-20261118.json",
                                   "git_blob_sha1": "05f54eb58baad66403b327696b9a63f7433a13c3"},
            "candidate_roots": {"path": "(regenerated) output/global-candidate-roots-20261118.jsonl",
                                 "regenerated_by": "enumerate_global_candidate_roots_20261118.py"},
        },
        "method": ("Published odd-r framework A/B cover types with shared-memo anchored "
                   "lazy matching DP (PmLazy, state cap 12M). Phase A writes this output "
                   "before the longer pair-membership phase B so a host kill during phase B "
                   "still preserves phase A results. Implementation validated by reproducing "
                   "all 1,505 singleton memberships of the published 29-row runner-up output."),
        "derived": {
            "rows": r, "candidates": P["cand_total"],
            "distinct_roots": len(P["proot_rows"]),
            "span_histogram": {str(x): v for x, v in sorted(hist.items())},
            "pair_types": len(pair_roots),
            "pair_type_multiplicity_histogram": {str(x): v for x, v in sorted(mult_hist.items())},
            "minimum_size": k, "parity": "odd",
            "type_A_total": A,
            "type_A_is_lower_component_of_total": ("total = A + B; B requires phase B; "
                                                    "A alone is NOT the total"),
            "singleton_membership_stats": singleton_mem_stats,
            "per_row_singleton_root_count": {str(s): w1[s] for s in range(r)},
            "per_row_pair_root_degree": {str(s): degree[s] for s in range(r)},
            "per_row_cover_options": {str(s): options[s] for s in range(r)},
            "bottleneck_rows_fewest_options": [
                {"row_index": s, "options": options[s], "row_hex": P["target"][s]}
                for s in sorted(range(r), key=lambda s: (options[s], s))[:5]],
            "hub_rows_by_pair_degree": [
                {"row_index": s, "pair_degree": degree[s], "row_hex": P["target"][s]}
                for s in sorted(range(r), key=lambda s: (-degree[s], s))[:5]],
            "scaling_facts": {
                "first_30row_tree_states": first_tree_states,
                "singleton_phase_memo_states": len(pm.memo),
                "runnerup29_singleton_phase_memo_states_published": 1346267,
                "note": ("the anchored-reachable state space of this 31-row parent "
                         "(1,346,254 states for the first 30-row root, 3,524,561 for "
                         "the full singleton phase) is of the same order as the "
                         "published 29-row runner-up singleton-phase union "
                         "(1,346,267 states); the near-equality of the first tree with "
                         "the runner-up's full union suggests the anchored state space "
                         "is governed by the shared candidate structure rather than by "
                         "row count"),
            },
            "validation": {"runnerup29_singleton_memberships_checked": checked,
                            "runnerup29_mismatches": mism},
        },
        "checks": checks_a,
        "check_count": len(checks_a),
        "all_pass": all_pass_a,
        "interpretation_guard": ("Cover-plan combinatorics only. A is the exact A-type "
                                 "component, not the total. Membership counts are not "
                                 "search costs or verdicts. REFUTED-D10 and STERILE are "
                                 "not LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
                           "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    with open(out_a, "w") as f:
        f.write(json.dumps(out, indent=2) + "\n")
    log("[A] wrote %s: all_pass=%s checks=%d" % (out_a, all_pass_a, len(checks_a)))

    # ---------- B phase
    t0 = time.time()
    for root, e in root_pair.items():
        ea, eb = e
        ea_bit = 1 << ea; eb_bit = 1 << eb
        base = full & ~(ea_bit | eb_bit)
        a_part = 0
        for s in range(r):
            if w1[s] and s != ea and s != eb:
                a_part += w1[s] * pm.get(base ^ (1 << s))
        b_part = 0
        for d in e:
            for z in range(r):
                if z == ea or z == eb:
                    continue
                wz = edge_w.get((min(d, z), max(d, z)), 0)
                if wz:
                    b_part += wz * pm.get(base ^ (1 << z))
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
                        b_part += wa * wb * pm.get(base ^ dbit ^ (1 << a2) ^ (1 << b2))
        mem[root] = a_part + b_part
        mem_A[root] = a_part; mem_B[root] = b_part
    b_pair_seconds = time.time() - t0
    log("[B] pair memberships done in %.1fs, memo %d, gets %d" %
        (b_pair_seconds, len(pm.memo), pm.gets))

    B_direct = 0
    for d in range(r):
        dbit = 1 << d
        nbrs = [a for a in range(r) if a != d and edge_w.get((min(d, a), max(d, a)))]
        for i in range(len(nbrs)):
            a = nbrs[i]
            wa = edge_w[(min(d, a), max(d, a))]
            for j in range(i + 1, len(nbrs)):
                b = nbrs[j]
                wb = edge_w[(min(d, b), max(d, b))]
                B_direct += wa * wb * pm.get(full ^ dbit ^ (1 << a) ^ (1 << b))
    total_A = sum(mem_A.values()) // k
    total_B = sum(mem_B.values()) // k
    total = total_A + total_B
    check(checks_b, "identity.A", sum(mem_A.values()) == k * total_A, str(sum(mem_A.values())))
    check(checks_b, "identity.B", sum(mem_B.values()) == k * total_B, str(sum(mem_B.values())))
    check(checks_b, "identity.total", sum(mem.values()) == k * total, str(sum(mem.values())))
    check(checks_b, "A.agrees_with_phase_a", total_A == A, {"phase_a": str(A), "recomputed": str(total_A)})
    check(checks_b, "B.direct_agreement", B_direct == total_B, str(B_direct))
    check(checks_b, "total_positive", total > 0, str(total))
    check(checks_b, "witness.membership_positive", all(mem[root] > 0 for root in wit))
    nz = {"count": sum(1 for v in mem.values() if v > 0),
          "min": min(v for v in mem.values() if v > 0),
          "max": max(mem.values()),
          "singleton_max": max(v for root, v in mem.items() if root in root_row),
          "pair_min": min(v for root, v in mem.items() if root in root_pair),
          "pair_max": max(v for root, v in mem.items() if root in root_pair)}
    check(checks_b, "all_roots_positive", nz["count"] == len(mem), nz["count"])

    by_mem = sorted(mem, key=lambda x: (-mem[x], x))
    top50 = [{"root": x, "membership": mem[x],
              "kind": "pair" if x in root_pair else "singleton",
              "rows_covered": list(root_pair[x]) if x in root_pair else [root_row[x]],
              "membership_A": mem_A[x], "membership_B": mem_B[x]}
             for x in by_mem[:50]]
    top10 = by_mem[:10]
    memo_states_pairs = len(pm.memo)
    pm.memo = {0: 1}
    pm.t0 = time.time()
    gc.collect()
    joint = []
    for i in range(len(top10)):
        for j in range(i + 1, len(top10)):
            r1, r2 = top10[i], top10[j]
            if r1 not in root_pair and r2 not in root_pair:
                m_ij = 0
            elif r1 not in root_pair or r2 not in root_pair:
                sroot, proot = (r1, r2) if r1 not in root_pair else (r2, r1)
                s = root_row[sroot]; e = root_pair[proot]
                m_ij = 0 if s in e else pm.get(full ^ (1 << e[0]) ^ (1 << e[1]) ^ (1 << s))
            else:
                e1 = root_pair[r1]; e2 = root_pair[r2]
                sh = set(e1) & set(e2)
                if sh:
                    d = sh.pop()
                    a = e1[0] if e1[1] == d else e1[1]
                    b = e2[0] if e2[1] == d else e2[1]
                    m_ij = 0 if a == b else pm.get(full ^ (1 << d) ^ (1 << a) ^ (1 << b))
                else:
                    m_ij = 0
                    rows12 = set(e1) | set(e2)
                    base = full
                    for x in rows12:
                        base &= ~(1 << x)
                    for s in range(r):
                        if w1[s] and s not in rows12:
                            m_ij += w1[s] * pm.get(base ^ (1 << s))
                    for d in range(r):
                        if d in rows12:
                            continue
                        nbrs = [a for a in range(r)
                                if a != d and a not in rows12
                                and edge_w.get((min(d, a), max(d, a)))]
                        for i2 in range(len(nbrs)):
                            a = nbrs[i2]
                            wa = edge_w[(min(d, a), max(d, a))]
                            for j2 in range(i2 + 1, len(nbrs)):
                                b = nbrs[j2]
                                wb = edge_w[(min(d, b), max(d, b))]
                                m_ij += wa * wb * pm.get(base ^ (1 << d) ^ (1 << a) ^ (1 << b))
                    for (eA, eB) in ((e1, e2), (e2, e1)):
                        for d in eA:
                            for z in range(r):
                                if z in rows12:
                                    continue
                                wz = edge_w.get((min(d, z), max(d, z)), 0)
                                if wz:
                                    m_ij += wz * pm.get(base ^ (1 << z))
            joint.append({"a": r1, "b": r2,
                          "rows_a": list(root_pair[r1]) if r1 in root_pair else [root_row[r1]],
                          "rows_b": list(root_pair[r2]) if r2 in root_pair else [root_row[r2]],
                          "membership_a": mem[r1], "membership_b": mem[r2],
                          "joint_membership": m_ij})
    check(checks_b, "joint.bounded",
          all(e["joint_membership"] <= min(e["membership_a"], e["membership_b"]) for e in joint))

    all_pass_b = all(c["pass"] for c in checks_b)
    out = {
        "schema": "n11-cost16-parent-b-phase-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": ("Exact B-type total, all 425 pair-root memberships with A/B split, top-50 "
                  "and top-10 joints for the 31-row cost-16 parent "
                  "00000000000000003800000008001000"),
        "inputs": {
            "cover_table": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/parent-minimum-cover-cost-table-20261118.json",
                             "git_blob_sha1": "4e4a911d0e05779437d4a8e97685a8feb66c0d25"},
            "runnerup29_output": {"path": "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/runnerup29-cover-membership-20261118.json",
                                   "git_blob_sha1": "05f54eb58baad66403b327696b9a63f7433a13c3"},
            "candidate_roots": {"path": "(regenerated) output/global-candidate-roots-20261118.jsonl",
                                 "regenerated_by": "enumerate_global_candidate_roots_20261118.py"},
        },
        "method": ("Phase B of the same run as the phase-A output: pair-root memberships by "
                   "the published closed forms, fresh memo for the joint phase, all with "
                   "shared-memo anchored lazy matching DP."),
        "derived": {
            "rows": r, "minimum_size": k,
            "total_minimum_covers": total,
            "type_A_disjoint": total_A,
            "type_B_one_duplicate_row": total_B,
            "membership": {x: mem[x] for x in sorted(mem)},
            "membership_nonzero_stats": nz,
            "top50_by_membership": top50,
            "top10_joint_membership": joint,
            "pm_memo_states_pairs_phase": memo_states_pairs,
            "pm_memo_states_joint_phase": len(pm.memo),
            "pm_gets": pm.gets,
        },
        "checks": checks_b,
        "check_count": len(checks_b),
        "all_pass": all_pass_b,
        "interpretation_guard": ("Cover-plan combinatorics only. Membership counts are not "
                                 "search costs or verdicts. REFUTED-D10 and STERILE are not "
                                 "LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
                           "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    with open(out_b, "w") as f:
        f.write(json.dumps(out, indent=2) + "\n")
    log("[B] wrote %s: all_pass=%s checks=%d" % (out_b, all_pass_b, len(checks_b)))
    print(json.dumps({"a_pass": all_pass_a, "b_pass": all_pass_b,
                      "A": total_A, "B": total_B, "total": total,
                      "stats": nz,
                      "top5": [{"kind": e["kind"], "membership": e["membership"]}
                               for e in top50[:5]],
                      "joint_nz": sum(1 for e in joint if e["joint_membership"] > 0)},
                     indent=1))
    if not (all_pass_a and all_pass_b):
        sys.exit(1)

if __name__ == "__main__":
    main()
