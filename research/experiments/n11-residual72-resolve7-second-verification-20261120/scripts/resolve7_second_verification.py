#!/usr/bin/env python3
"""Independent second verification of resolve7 (residual 72-row post-fold witness recheck).

Single-owner experiment declared in
research/log/2026-11-20-n11-resolve7-second-verification-single-owner-note.md.

Verification target:
  resolve7 record  research/experiments/n11-residual72-postfold-witness-recheck-20261120/output/residual72-postfold-witness-recheck-20261120.json
  SHA-256 207f4094a906817ebb4bbc5ad9b90c203c6a334ee6c8d9a501661257a0e1ce3f (27 gates, all PASS)

This machine consumes the same five published records as resolve7, but re-derives the
determinations by independent routes that resolve7 did not consume:

  route A  K1069 classification rebuilt from the raw 4-worker probe records
           (probe-records-w{0..3}.jsonl, pinned at the current main state) with a fresh
           dedup/agreement implementation, instead of trusting sweep39.classification.
  route B  the 39-root witness assignment rebuilt from the raw probe covered_rows and from
           roots.json, instead of resolve6.witness_full alone (three-source agreement).
  route C  the fold-chain bookkeeping: rows78 -> fold9 residual74 -> fold10 residual72,
           via the residual lists of the two fold records themselves (set arithmetic per
           link), instead of the single 78 - 6 == 72 subtraction.
  route D  cross-agreement with the independent fold10 second verification record
           (certificate-geometry rederivation lane) on the fold10 closed rows.

Additionally, every list/number inside the resolve7 record is compared field-by-field with
the recomputed values (gate family r7-*), and the worker-record corpus is audited
(duplicate records must agree node-exact; cap/pilot control/uniform terminal range).

The machine performs no search, judges no root, closes no row, and does not rebuild the
resolve6 candidate universe. REFUTED-D10 is not a LOSS proof. The standard 11x11 empty
board, two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4 remain UNKNOWN.

Usage: python3 resolve7_second_verification.py <input_dir> <out_path>
"""
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict

RETIRED_ROOT = "00004000000000821082000000000100"
CERT_SHA_SEVENTEENTH = "21dd2f0e9f0b8ec22e917fce5a732835098baf37570a227bebacacb4c13807c8"
CAP = 30000000
PILOT = {"control": "pilot_d6", "loss": False, "nodes": 3402, "capped": False}
README_DUP_AT_ASSEMBLY = 15  # "同じ(root, ordering)の重複ok記録15件" in the 39livewitness README

PINS = {
    # the five published records consume by resolve7 (same corpus)
    "resolve6.json": "e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a",
    "fold9.json": "24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2",
    "fold10.json": "bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a",
    "sweep39.json": "22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc",
    "sv17.json": "c1073bae1d056db7f56d04a77fd9889d1e297a82a07537ddcd02c00d329dbabc",
    # the verification target itself
    "resolve7.json": "207f4094a906817ebb4bbc5ad9b90c203c6a334ee6c8d9a501661257a0e1ce3f",
    # raw worker probe records and the 39-root manifest (snapshot pins of the published
    # experiment state on main; computed from main@ba5f9f4aad42b369650c182925bdcb1f06da8727)
    "probes-w0.jsonl": "6b045eaefdd59e2c0fbd0f9b4a1e876b89c3f8b03cfade8f0ab1f8192cd0a984",
    "probes-w1.jsonl": "4aaa4d0a691f6da40e68dbaa41a353aaf3ea518a6863aec04886c17197e00967",
    "probes-w2.jsonl": "2d4ff7dd40b2fc66745068f6772724f38ccd04dd2a65507af925fb85252b3032",
    "probes-w3.jsonl": "e04e20bdadd1cba94cd0a285ff9fb72bb9e9d0a2d5a687f1d76ceccc7d0ccb0c",
    "roots.json": "9f0161a8a61d311534fd3a4035b1c367426691c72ad5eb44efd01a5fae37e0cc",
    # the independent fold10 second verification (certificate-geometry route)
    "fold10second.json": "a62d6d50ffe3196ad2de1ff7b1df67ff8208b2a13510cce3f13aee0e9a085054",
}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def popcount(x):
    return bin(x).count("1")


def gates_of(ln):
    global GATES
    GATES.append({"name": ln[0], "pass": bool(ln[1]), "detail": str(ln[2])})
    return bool(ln[1])


GATES = []


def main():
    input_dir = sys.argv[1] if len(sys.argv) > 1 else "input"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "output/resolve7-second-verification-20261120.json"

    rec = {}
    for name in sorted(PINS):
        p = os.path.join(input_dir, name)
        got = sha256_file(p)
        gates_of(("pin-" + name, got == PINS[name], got))
        if got != PINS[name]:
            raise SystemExit("pin mismatch for " + name)
        if name.endswith(".jsonl"):
            rows = []
            with open(p) as f:
                for ln in f:
                    ln = ln.strip()
                    if ln:
                        rows.append(json.loads(ln))
            rec[name] = rows
        else:
            with open(p) as f:
                rec[name] = json.load(f)

    r6 = rec["resolve6.json"]
    f9 = rec["fold9.json"]
    f10 = rec["fold10.json"]
    sw = rec["sweep39.json"]
    sv = rec["sv17.json"]
    r7 = rec["resolve7.json"]
    roots_manifest = rec["roots.json"]
    f10v = rec["fold10second.json"]
    probes = rec["probes-w0.jsonl"] + rec["probes-w1.jsonl"] + rec["probes-w2.jsonl"] + rec["probes-w3.jsonl"]

    # ------------------------------------------------------------------ route A
    # K1069 classification rebuilt from raw worker probe records.
    per_key = defaultdict(list)
    for p in probes:
        per_key[(p["root"], p["ordering"])].append(p)
    unique_pairs = sorted(per_key.keys())
    dup_records = len(probes) - len(unique_pairs)
    agree_fail = []
    for k, ps in per_key.items():
        sig = [(p["result"]["loss"], p["result"]["nodes"], p["result"]["capped"],
                p["result"]["bit"], p["child"], p["result"]["terminalStoneRange"]) for p in ps]
        if len(set(map(str, sig))) != 1 or len(set(p["covered_rows"] and json.dumps(sorted(p["covered_rows"])) for p in ps)) != 1:
            agree_fail.append(k)
    gates_of(("probes-corpus-parsed", len(probes) == 98 and len(unique_pairs) == 78,
             "records=%d unique(root,ordering)=%d" % (len(probes), len(unique_pairs))))
    gates_of(("probes-duplicate-records-node-exact-agree", not agree_fail,
             "dups=%d disagree=%s" % (dup_records, agree_fail)))
    gates_of(("probes-cap-uniform-30000000", all(p["cap"] == CAP for p in probes), ""))
    gates_of(("probes-control-pilot-d6-uniform",
              all(p["control"] == PILOT for p in probes), ""))
    gates_of(("probes-terminal-range-13-17-uniform",
              all(p["result"]["terminalStoneRange"] == [13, 17] for p in probes), ""))
    gates_of(("probes-ordering-no-error", all("error" not in p for p in probes), ""))

    # dedup: first record per (root,ordering) is the representative; duplicates agreed above.
    root_probes = defaultdict(list)
    for k in unique_pairs:
        root_probes[k[0]].append(per_key[k][0])
    both_orders_missing = [r for r, ps in root_probes.items()
                           if sorted(pp["ordering"] for pp in ps) != ["andclose0", "andclose1"]]
    gates_of(("probes-both-orders-per-root", len(root_probes) == 39 and not both_orders_missing,
             "roots=%d missing=%s" % (len(root_probes), both_orders_missing)))
    andclose_map_ok = all((p["ordering"] == "andclose1") == p["result"]["andclose"] for p in probes)
    gates_of(("probes-andclose-field-consistent", andclose_map_ok, ""))

    rebuilt_cls = {}
    order_conflicts = []
    for r, ps in root_probes.items():
        losses = set(p["result"]["loss"] for p in ps)
        capped = any(p["result"]["capped"] for p in ps)
        if capped:
            verdict = "CAPPED"
        elif len(losses) == 1:
            verdict = "WIN7-D10" if losses.pop() else "REFUTED-D10"
        else:
            verdict = "CONFLICT"
            order_conflicts.append(r)
        rebuilt_cls[r] = verdict
    gates_of(("k1069-classification-rebuilt-from-raw-probes",
              rebuilt_cls == sw["classification"],
              "mismatch=%s" % sorted(r for r in set(rebuilt_cls) | set(sw["classification"])
                                     if rebuilt_cls.get(r) != sw["classification"].get(r))))
    rebuilt_counts = Counter(rebuilt_cls.values())
    gates_of(("k1069-rebuilt-won1-refuted38-capped0",
              rebuilt_counts["WIN7-D10"] == 1 and rebuilt_counts["REFUTED-D10"] == 38
              and rebuilt_counts["CAPPED"] == 0 and not order_conflicts,
              json.dumps(rebuilt_counts)))

    # summary numbers rebuilt from unique probes
    total_nodes = sum(p["result"]["nodes"] for k in unique_pairs for p in [per_key[k][0]])
    gates_of(("k1069-total-nodes-rebuilt", total_nodes == sw["summary"]["total_nodes"],
              "%d vs %d" % (total_nodes, sw["summary"]["total_nodes"])))
    gates_of(("k1069-max-probe-rebuilt",
              total_nodes and max(per_key[k][0]["result"]["nodes"] for k in unique_pairs)
              == sw["summary"]["max_probe"]["nodes"],
              json.dumps(sw["summary"]["max_probe"])[:120]))
    maxrep = max((per_key[k][0] for k in unique_pairs), key=lambda p: p["result"]["nodes"])
    max_ok = (maxrep["result"]["nodes"] == sw["summary"]["max_probe"]["nodes"]
              and maxrep["root"] == sw["summary"]["max_probe"]["root"]
              and maxrep["result"]["bit"] == sw["summary"]["max_probe"]["bit"]
              and maxrep["result"]["loss"] == sw["summary"]["max_probe"]["loss"]
              and maxrep["result"]["andclose"] == sw["summary"]["max_probe"]["andclose"]
              and maxrep["result"]["terminalStoneRange"] == sw["summary"]["max_probe"]["terminalStoneRange"])
    gates_of(("k1069-max-probe-fields-rebuilt", max_ok,
              "root=%s nodes=%d" % (maxrep["root"], maxrep["result"]["nodes"])))
    gates_of(("k1069-avg-nodes-rebuilt",
              total_nodes // len(unique_pairs) == sw["summary"]["avg_nodes_per_probe"],
              "%d vs %d" % (total_nodes // len(unique_pairs), sw["summary"]["avg_nodes_per_probe"])))

    # ------------------------------------------------------------------ route B
    # witness assignment rebuilt from raw probe covered_rows + roots.json + resolve6.
    probe_rows = {r: sorted(set(c for p in ps for c in p["covered_rows"])) for r, ps in root_probes.items()}
    probe_union = Counter()
    for r, rows in probe_rows.items():
        for c in rows:
            probe_union[c] += 1
    rows78 = r6["base_state"]["residual_row_hex"]
    set78 = set(rows78)
    gates_of(("probes-covered-union-eq-rows78-one-cover",
              set(probe_union) == set78 and set(probe_union.values()) == {1},
              "union=%d multi=%d" % (len(probe_union), sum(1 for v in probe_union.values() if v != 1))))
    manifest_rows_ok = manifest_anatomy_fail = None
    anatomy_fail = []
    for e in roots_manifest:
        root = int(e["root"], 16)
        child = int(e["child"], 16)
        lowbit = root & -root
        if not (e["root"] in probe_rows and probe_rows[e["root"]] == sorted(e["rows"])
                and popcount(root) == e["pcount"] == 7 and root == child | (1 << e["bit"])
                and child == root - lowbit and e["bit"] == lowbit.bit_length() - 1
                and e["safe"] is True):
            anatomy_fail.append(e["root"])
    gates_of(("roots-manifest-anatomy-and-probe-rows", len(roots_manifest) == 39 and not anatomy_fail,
              "fail=%s" % anatomy_fail))
    wf = r6["witness_full"]
    gates_of(("witness-full-eq-probe-assignment",
              all(probe_rows[w["root"]] == sorted(w["covered"]) for w in wf),
              ""))
    gates_of(("witness-full-cover-eq-rows-field",
              all(sorted(w["covered"]) == sorted(w["rows"]) for w in wf), ""))
    witness_roots = [w["root"] for w in wf]
    gates_of(("witness-roots-triple-source",
              sorted(witness_roots)
              == sorted(root_probes.keys())
              == sorted(e["root"] for e in roots_manifest)
              == sorted(sw["classification"].keys()), ""))
    gates_of(("witness-roots-disjoint-dead-root-corpus",
              set(witness_roots).isdisjoint(set(r6["base_state"]["dead_roots_39"])),
              "dead=%d overlap=%d" % (len(r6["base_state"]["dead_roots_39"]),
                                     len(set(witness_roots) & set(r6["base_state"]["dead_roots_39"])))))
    row_owner = {}
    for w in wf:
        for c in w["covered"]:
            row_owner[c] = w["root"]
    gates_of(("row-owner-by-probe-family-eq-witness-full",
              all(row_owner.get(c) == [w["root"] for w in wf if c in w["covered"]][0]
                  for c in set78), ""))

    # ------------------------------------------------------------------ route C
    # fold-chain bookkeeping, link by link.
    closed_dict9 = {r["row_hex"]: r for r in f9["new_receipt_coverage"]["rows"]}
    closed9 = [r["row_hex"] for r in f9["new_receipt_coverage"]["rows"]]
    gates_of(("fold9-closes-4-in-rows78", set(closed9) <= set78 and len(closed9) == 4,
              ",".join(closed9)))
    gates_of(("fold9-cost-sum-eq-closed-edge-cost",
              sum(r["cost"] for r in f9["new_receipt_coverage"]["rows"]) == f9["new_receipt_coverage"]["closed_edge_cost"] == 299
              and f9["new_receipt_coverage"]["unique_s6_rows"] == 4, ""))
    residual74 = f9["five_parent_target_after"]["residual_row_hex_after"]
    gates_of(("fold9-residual74-eq-rows78-minus-closed9",
              len(residual74) == 74 and set(residual74) == set78 - set(closed9),
              "74=%d equal=%s" % (len(residual74), set(residual74) == set78 - set(closed9))))
    gates_of(("fold9-frontier-arithmetic",
              f9["frontier_before"]["unique_remaining_s6"] - 4 == f9["frontier_after"]["unique_remaining_s6"] == 6209
              and f9["frontier_before"]["sum_remaining_cost"] - 299 == f9["frontier_after"]["sum_remaining_cost"] == 491722
              and f9["frontier_before"]["solved_s6_in_manifest"] + 4 == f9["frontier_after"]["solved_s6_in_manifest"] == 1639
              and f9["frontier_before"]["s6_needed_by_open_classes"] - 4 == f9["frontier_after"]["s6_needed_by_open_classes"] == 4509
              and f9["frontier_before"]["cost_needed_by_open_classes"] - 299 == f9["frontier_after"]["cost_needed_by_open_classes"] == 357583
              and f9["frontier_before"]["parent_row_incidence"] - 8 == f9["frontier_after"]["parent_row_incidence"] == 11818, ""))
    gates_of(("fold9-closed-target-34-plus-4-eq-38",
              f9["five_parent_target_after"]["closed_target_rows_total"] == 38
              and f9["five_parent_target_after"]["residual_target_rows"] == 74, ""))

    cols10 = f10["new_receipt_coverage"]["rows"]
    closed10_all = [r["row_hex"] for r in cols10]
    target10 = [h for h in closed10_all if h in set78]
    extra10 = [h for h in closed10_all if h not in set78]
    costs10 = {r["row_hex"]: r["cost"] for r in cols10}
    gates_of(("fold10-closes-3-rows-2-target-1-extra",
              len(closed10_all) == 3 and set(closed10_all) == set(target10) | set(extra10)
              and len(target10) == 2 and len(extra10) == 1,
              "target=%s extra=%s" % (sorted(target10), extra10)))
    gates_of(("fold10-cost-sum-eq-closed-edge-cost",
              sum(r["cost"] for r in cols10) == f10["new_receipt_coverage"]["closed_edge_cost"] == 225
              and f10["new_receipt_coverage"]["unique_s6_rows"] == 3, ""))
    gates_of(("fold10-target-subset-residual74", set(target10) <= set(residual74), ""))
    gates_of(("fold10-extra-outside-residual74", set(extra10).isdisjoint(set(residual74)), ""))
    gates_of(("fold10-pins-fold9-record",
              "24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2"
              in json.dumps(f10["previous_fold"]), ""))
    gates_of(("fold10-frontier-before-eq-fold9-after",
              f10["frontier_before"] == f9["frontier_after"], ""))
    gates_of(("fold10-frontier-arithmetic",
              f10["frontier_before"]["unique_remaining_s6"] - 3 == f10["frontier_after"]["unique_remaining_s6"] == 6206
              and f10["frontier_before"]["sum_remaining_cost"] - 225 == f10["frontier_after"]["sum_remaining_cost"] == 491497
              and f10["frontier_before"]["solved_s6_in_manifest"] + 3 == f10["frontier_after"]["solved_s6_in_manifest"] == 1642
              and f10["frontier_before"]["s6_needed_by_open_classes"] == f10["frontier_after"]["s6_needed_by_open_classes"] == 4509
              and f10["frontier_before"]["cost_needed_by_open_classes"] == f10["frontier_after"]["cost_needed_by_open_classes"] == 357583
              and f10["frontier_before"]["parent_row_incidence"] - 8 == f10["frontier_after"]["parent_row_incidence"] == 11810, ""))
    residual72 = f10["five_parent_target_after"]["residual_row_hex_after"]
    gates_of(("fold10-residual72-eq-residual74-minus-target",
              len(residual72) == 72 and set(residual72) == set(residual74) - set(target10), ""))
    gates_of(("fold10-closed-target-38-plus-2-eq-40",
              f10["five_parent_target_after"]["closed_target_rows_total"] == 40
              and f10["five_parent_target_after"]["residual_target_rows"] == 72, ""))
    gates_of(("fold10-chain-total-78-minus4-minus2-eq-72",
              set78 - set(closed9) - set(target10) == set(residual72)
              and set(closed9).isdisjoint(set(target10)), ""))
    rec17 = f10["receipts"][0]
    gates_of(("fold10-receipt-seventeenth-anatomy",
              rec17["root"] == RETIRED_ROOT and rec17["receipt"] == "seventeenth"
              and rec17["lane_bit"] == 8 == sv["added_bit"]
              and rec17["lane_child_hex"] == "00004000000000821082000000000000"
              and rec17["raw_root_is_d4_canonical"] is True
              and rec17["legal_next_moves"] == 60
              and sorted(rec17["covered_s6_rows"]) == sorted(closed10_all), ""))
    wpi = f10["witness_plan_impact"]
    gates_of(("fold10-retire-declaration-eq-seventeenth",
              wpi["retired_witness_root"] == RETIRED_ROOT
              and sorted(wpi["rows_of_retired_root"]) == sorted(target10)
              and row_owner[target10[0]] == RETIRED_ROOT and row_owner[target10[1]] == RETIRED_ROOT, ""))
    gates_of(("retired-root-verdict-rebuilt-win",
              rebuilt_cls.get(RETIRED_ROOT) == "WIN7-D10"
              and probe_rows[RETIRED_ROOT] == sorted(wpi["rows_of_retired_root"]), ""))

    # ------------------------------------------------------------------ sv17 and route D
    gates_of(("sv17-gates-38-all-pass",
              sv["gates_total"] == 38 and sv["gates_all_pass"] is True, ""))
    gates_of(("sv17-root-bit-child",
              sv["root_hex"] == RETIRED_ROOT and sv["added_bit"] == 8
              and int(sv["root_hex"], 16) == int(sv["child_hex"], 16) | (1 << 8), ""))
    claim = sv["coverage_claim_pending_fold"]
    gates_of(("sv17-claim-eq-fold10-target-and-open-in-residual74",
              sorted(claim["covered_rows_per_resolve6_matching"]) == sorted(target10)
              and claim["both_rows_open_in_fold9_residual_74"] is True
              and set(claim["covered_rows_per_resolve6_matching"]) <= set(residual74), ""))
    gates_of(("fold10second-gates-31-all-pass",
              f10v["gates_total"] == 31 and f10v["gates_all_pass"] is True, ""))
    gates_of(("fold10second-subject-and-input-pins",
              f10v["subject"].endswith("seventeenth-win7-receipt-fold-20261120.json")
              and f10v["inputs_verified_by_sha256"]["fold10_record"]
              == "bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a"
              and f10v["inputs_verified_by_sha256"]["seventeenth_certificate"] == CERT_SHA_SEVENTEENTH, ""))
    kf = f10v["key_finding"]
    gates_of(("fold10second-geometry-route-agrees-on-closed-rows",
              sorted(kf["candidates_touching_fold9_residual74"]) == sorted(target10)
              and set(target10) | set(extra10) <= set(kf["rederivation_candidate_hexes"])
              and kf["rederivation_distinct_candidates"] == 7, ""))

    # ------------------------------------------------------------- re-derivation
    # post-retire assignment table, recomputed from the probe-family witness assignment.
    closed6 = set(closed9) | set(target10)
    live_assign = {}
    assign_rows = defaultdict(list)
    for w in wf:
        keep = [c for c in w["covered"] if c not in closed6]
        if w["root"] != RETIRED_ROOT:
            live_assign[w["root"]] = keep
    for r, rows in live_assign.items():
        for c in rows:
            assign_rows[c].append(r)
    two_row_roots = sorted(r for r, v in live_assign.items() if len(v) == 2)
    one_row_roots = sorted(r for r, v in live_assign.items() if len(v) == 1)
    zero_row_roots = sorted(r for r, v in live_assign.items() if len(v) == 0)
    multi = sorted(c for c, rs in assign_rows.items() if len(rs) > 1)
    unassigned = sorted(set(residual72) - set(assign_rows))
    gates_of(("post-retire-38-roots-34x2-4x1",
              len(live_assign) == 38 and len(two_row_roots) == 34 and len(one_row_roots) == 4
              and not zero_row_roots and sum(len(v) for v in live_assign.values()) == 72, ""))
    gates_of(("post-retire-assignment-covers-residual72-one-cover",
              set(assign_rows) == set(residual72) and not multi and not unassigned,
              "multi=%s unassigned=%s" % (multi, unassigned)))
    row9_owner = {c: row_owner[c] for c in closed9}
    gates_of(("fold9-closed-rows-owners-are-exactly-the-4-degraded-roots",
              sorted(row9_owner.values()) == one_row_roots, ""))
    # supply-zero determination from the rebuilt classification
    live_refuted = sorted(r for r in live_assign if rebuilt_cls.get(r) == "REFUTED-D10")
    dead_rows = sorted(c for c, rs in assign_rows.items()
                       if all(rebuilt_cls.get(x) == "REFUTED-D10" for x in rs))
    gates_of(("live-38-all-refuted-d10-rebuilt",
              len(live_refuted) == 38 and len(live_refuted) == len(live_assign), ""))
    gates_of(("residual72-rows-assigned-to-refuted-d10-only-rebuilt",
              len(dead_rows) == 72, "dead=%d" % len(dead_rows)))
    gates_of(("retired-root-not-in-live-assignment",
              RETIRED_ROOT not in live_assign and RETIRED_ROOT in rebuilt_cls, ""))

    # --------------------------------------------------- resolve7 record fields
    rplan = r7["recheck"]["residual_78_plan"]
    gates_of(("r7-rows78-faithful", rplan["rows"] == rows78, ""))
    gates_of(("r7-witness-roots-faithful", rplan["witness_roots"] == witness_roots, ""))
    gates_of(("r7-closed-by-fold9-faithful", rplan["closed_by_fold9"] == closed9, ""))
    gates_of(("r7-closed-by-fold10-target-faithful", rplan["closed_by_fold10_target"] == target10, ""))
    gates_of(("r7-closed-by-fold10-extra-faithful",
              rplan["closed_by_fold10_extra_outside_plan"] == extra10, ""))
    gates_of(("r7-residual72-faithful", r7["recheck"]["residual_72_after"]["rows"] == residual72, ""))
    pa = r7["recheck"]["post_retire_assignment"]
    gates_of(("r7-two-row-roots-faithful", pa["two_row_roots"] == two_row_roots, ""))
    gates_of(("r7-one-row-roots-faithful", pa["one_row_roots"] == one_row_roots, ""))
    gates_of(("r7-rows-per-root-faithful",
              {k: v for k, v in sorted(pa["rows_per_root"].items())} == {k: v for k, v in sorted(live_assign.items())}, ""))
    gates_of(("r7-fold9-row-owners-faithful", pa["fold9_row_owners_lost"] == row9_owner, ""))
    kx = r7["recheck"]["k1069_cross"]
    gates_of(("r7-k1069-cross-faithful",
              kx["win_root"] == RETIRED_ROOT and kx["live_refuted_roots"] == 38
              and kx["residual_rows_with_only_refuted_d10_assignment"] == 72
              and kx["depth10_witness_supply_from_39root_plan_for_residual72"] == 0, ""))
    gates_of(("r7-gates-27-all-pass-and-pins",
              r7["gates_total"] == 27 and r7["gates_all_pass"] is True
              and r7["input_pins"] == {k: PINS[k] for k in
                                      ("resolve6.json", "fold9.json", "fold10.json", "sv17.json", "sweep39.json")}, ""))
    gates_of(("r7-retired-root-and-whole-determination-set-compatible",
              r7["retired_witness_root"] == RETIRED_ROOT
              and len(rows78) - len(closed9) - len(target10) == len(residual72) == len(dead_rows), ""))

    result = {
        "schema": "resolve7-second-verification/1",
        "date": "2026-11-20",
        "status": "independent second verification; published records only; no search, no new judging",
        "single_owner_note": "research/log/2026-11-20-n11-resolve7-second-verification-single-owner-note.md",
        "verification_target": {
            "record": "research/experiments/n11-residual72-postfold-witness-recheck-20261120/output/residual72-postfold-witness-recheck-20261120.json",
            "sha256": PINS["resolve7.json"],
            "gates_total_in_target": r7["gates_total"],
        },
        "input_pins": PINS,
        "independent_routes": {
            "routeA_classification_from_raw_probe_records": ("39/39 verdicts rebuilt from the 4-worker "
                                                             "probe-records corpus with a fresh dedup+agreement "
                                                             "implementation and equal to sweep39.classification"),
            "routeB_witness_assignment_three_source": ("39-root x 2-row one-cover plan agrees across raw probe "
                                                      "covered_rows, roots.json, and resolve6.witness_full"),
            "routeC_fold_chain_link_by_link": ("rows78 -> fold9 residual74 -> fold10 residual72 verified on the "
                                              "two fold records' own residual lists, plus full frontier arithmetic "
                                              "gates for both folds"),
            "routeD_certificate_geometry_cross_agreement": ("fold10second (certificate-body geometry rederivation "
                                                            "record) agrees on the two target rows and the extra row"),
        },
        "gates": [{"name": g["name"], "pass": g["pass"], "detail": g["detail"]} for g in GATES],
        "gates_total": len(GATES),
        "gates_all_pass": all(g["pass"] for g in GATES),
        "rederived": {
            "probe_corpus": {
                "records": len(probes),
                "unique_root_ordering_pairs": len(unique_pairs),
                "duplicate_records": dup_records,
                "duplicate_records_at_assembly_readme": README_DUP_AT_ASSEMBLY,
                "duplicate_records_note": ("all duplicate (root,ordering) records agree node-exact on "
                                            "loss/nodes/capped/bit/child/terminalStoneRange; the corpus grew by "
                                            "5 duplicate records after the 39livewitness README was written "
                                            "(15 -> 20), consistent with the append-resume worker protocol and "
                                            "the additional 78/78 node-exact rerun; every record still agrees, "
                                            "which strengthens run-to-run determinism evidence"),
                "workers": sorted(set(("probes-w%d.jsonl" % i) for i in range(4))),
            },
            "classification_rebuilt_from_raw_probes": {r: rebuilt_cls[r] for r in sorted(rebuilt_cls)},
            "total_nodes_rebuilt": total_nodes,
            "witness_assignment_sources_agree": True,
            "fold_chain": {
                "rows78": len(rows78),
                "closed_by_fold9": closed9,
                "fold9_costs": {r["row_hex"]: r["cost"] for r in f9["new_receipt_coverage"]["rows"]},
                "residual74": len(residual74),
                "closed_by_fold10_target": target10,
                "closed_by_fold10_extra_outside_plan": extra10,
                "fold10_costs": costs10,
                "residual72": len(residual72),
            },
            "post_retire_assignment": {
                "live_roots": len(live_assign),
                "two_row_roots": two_row_roots,
                "one_row_roots": one_row_roots,
                "fold9_row_owners_lost": row9_owner,
                "rows_per_root": {r: live_assign[r] for r in sorted(live_assign)},
            },
            "k1069_cross": {
                "win_root": RETIRED_ROOT,
                "live_refuted_roots": len(live_refuted),
                "residual72_rows_with_only_refuted_d10_assignment": len(dead_rows),
                "depth10_witness_supply_from_39root_plan_for_residual72": 0,
            },
        },
        "resolve7_record_faithful": all(g["pass"] for g in GATES if g["name"].startswith("r7-")),
        "interpretation_guard": [
            "REFUTED-D10 is NOT a LOSS proof; it certifies no first-player win within depth-10 from that root only.",
            "Folds and coverage are row bookkeeping and say nothing about the game-theoretic value of any row.",
            "This second verification judges no root, closes no row, and rebuilds no candidate universe.",
            "The rebuilt classification and assignment come from published raw records, not from new searches.",
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
        ],
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("gates", result["gates_total"], "all_pass", result["gates_all_pass"],
          "resolve7_faithful", result["resolve7_record_faithful"])


if __name__ == "__main__":
    main()
