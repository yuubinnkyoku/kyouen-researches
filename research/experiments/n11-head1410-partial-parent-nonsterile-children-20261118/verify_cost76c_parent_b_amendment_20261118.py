#!/usr/bin/env python3
"""Verification-side crosscheck of the additive amendment to the cost76c fold
record's parent-B entry (main commit c4ab218965).

Independently recomputes, from the pinned head-1410 worklist, the K0865 census,
and the fold-chain ledger:
  - that the amendment is a pure textual insert (the pre-amendment record is
    reconstructed byte-exactly and pinned at its original git blob),
  - the chain-correct parent-B state at the cost76c fold (the amendment's
    corrected_entry values),
  - the corrected aggregate-field reading (381 / 5) and the strict chain
    marginal of the cost76c fold (2 parent incidences / 152 edge delta),
  - the D4-parent attribution of the 76c/76d/77e rows over all 174 open S5
    parents, and
  - the chain-consistency of every other parents_after entry of the record.
"""
import json, sys, os, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
INPUTS = {
    "worklist": ("research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
                 "2fee1d0718547a62e346d35f5858d7913e37c097"),
    "census": ("research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
               "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"),
    "ledger": ("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
               "e8785d509e8a11a37c0d03cc450455a14708c34d"),
    "bookkeeping": ("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-parent-bookkeeping-crosscheck-20261118.json",
                    "ed98c01429f08d6f046905b4bc2633c18767ca95"),
    "record_amended": ("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost76c-receipts-recompute-20261117.json",
                       "cb875a1da69eff1a80341e563130faa618706f48"),
}
ORIGINAL_BLOB = "953beaea054989e8b1de33f48b1f2ebc13ae7e11"
N = 11
ROW_76C = "00000000010000809002000001000000"
ROW_76D = "00000000040000003800080008000000"
ROW_77E = "00000000040000809002000000004000"
PARENT_B = "00000000000000801202000000040000"
PARENT_RANK1 = "00000000000000801202000040000000"
PARENT_P76D = "00000000000000003800000208000000"
PARENT_E = "00000000000000801202000100000000"

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()

def read_pinned(name):
    rel, pin = INPUTS[name]
    with open(os.path.join(ROOT, rel), "rb") as f:
        data = f.read()
    sha = git_blob_sha(data)
    if sha != pin:
        raise SystemExit("%s git blob SHA mismatch: %s != %s" % (name, sha, pin))
    return data

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

def transform(mask, t):
    out = 0
    for i in range(121):
        if (mask >> i) & 1:
            qx, qy = t(i % N, i // N)
            out |= 1 << (qy * N + qx)
    return out

def canon(mask):
    return min(transform(mask, t) for t in T)

def canon_hex(mask):
    return format(canon(mask), "032x")

def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "output", "cost76c-parent-b-amendment-crosscheck-20261118.json")
    checks = []
    def check(name, ok, detail=""):
        checks.append({"name": name, "pass": bool(ok),
                       "detail": detail if isinstance(detail, str) else json.dumps(detail)})

    wl_bytes = read_pinned("worklist")
    cen = json.loads(read_pinned("census"))
    led = json.loads(read_pinned("ledger"))
    book = json.loads(read_pinned("bookkeeping"))
    rec_bytes = read_pinned("record_amended")
    for k in INPUTS:
        check("pin.%s" % k, True, INPUTS[k][1])

    # ---------- A. textual insert reconstruction ----------
    lines = rec_bytes.decode("utf-8").split("\n")
    # amendment commit diff: 1a2,16 -> amended lines 2..16 are the insert
    reconstructed = ("\n".join([lines[0]] + lines[16:])).encode("utf-8")
    rec_orig_blob = git_blob_sha(reconstructed)
    check("insert.reconstructs_original_blob", rec_orig_blob == ORIGINAL_BLOB, rec_orig_blob)
    rec = json.loads(rec_bytes.decode("utf-8"))
    check("insert.amended_parses", "amendment_20261118" in rec)
    am = rec["amendment_20261118"]
    ce = am["corrected_entry_%s" % PARENT_B]
    check("insert.original_fields_preserved",
          rec["parents_after"][PARENT_B]["rows_after"] == 69
          and rec["parents_after"][PARENT_B]["edge_cost_after"] == 5725
          and rec["parents_after"][PARENT_B]["lost_rows"] == 1
          and rec["parents_after"][PARENT_B]["lost_rows_hexes"] == [ROW_77E])

    # ---------- B. worklist / joins ----------
    wl_lines = wl_bytes.decode("utf-8").rstrip("\r\n").split("\n")
    headers = [h.strip() for h in wl_lines[0].split(",")]
    rows = {}
    for line in wl_lines[1:]:
        vals = line.split(",")
        r = {h: (vals[i].strip() if i < len(vals) else "") for i, h in enumerate(headers)}
        rows[r["s6_canonical_hex"]] = r
    def cost(h):
        return int(rows[h]["own_candidates_s6_s7_edge_cost"])
    parents = [p["hex"] for p in cen["open_s5_census"]]
    check("worklist.rows", len(rows) == 6438, len(rows))
    check("census.parents", len(parents) == 174, len(parents))

    # 5-subset canon index join
    join_of = {}
    def join(parent):
        if parent not in join_of:
            j = []
            for h in rows:
                m = int(h, 16)
                bits = [i for i in range(121) if (m >> i) & 1]
                if parent in {canon_hex(m ^ (1 << b)) for b in bits}:
                    j.append(h)
            join_of[parent] = sorted(j)
        return join_of[parent]

    chain = led["derived"]["chain"]
    closed_upto = {}
    acc = set()
    for c in chain:
        acc = acc | set(c["closure"])
        closed_upto[c["tag"]] = set(acc)

    def state_through(parent, tag):
        j = join(parent)
        cl = closed_upto[tag]
        rem = [h for h in j if h not in cl]
        return rem

    # ---------- C. parent-B recomputation ----------
    bj = join(PARENT_B)
    bcost = sum(cost(h) for h in bj)
    check("B.join1410", len(bj) == 74 and bcost == 6113, {"rows": len(bj), "cost": bcost})
    b_history = []
    seen = set()
    for c in chain:
        cl = sorted(h for h in c["closure"] if h in set(bj))
        b_history.append({"tag": c["tag"], "rows_closed_in_B": cl, "costs": [cost(h) for h in cl]})
    check("B.closure_history",
          [x["tag"] for x in b_history if x["rows_closed_in_B"]] == ["cost64d", "cost76d77e", "cost64h"],
          [x for x in b_history if x["rows_closed_in_B"]])
    b_after = state_through(PARENT_B, "cost76c")
    b_after_cost = sum(cost(h) for h in b_after)
    check("B.state_through_76c", len(b_after) == 70 and b_after_cost == 5802,
          {"rows": len(b_after), "cost": b_after_cost})
    check("amendment.corrected_entry_matches",
          ce["rows_after"] == 70 and ce["edge_cost_after"] == 5802
          and ce["lost_rows"] == 0 and ce["lost_rows_hexes"] == [] and ce["lost_edge_cost"] == 0,
          ce)
    check("amendment.original_entry_was_chain_wrong",
          rec["parents_after"][PARENT_B]["rows_before"] == 70
          and rec["parents_after"][PARENT_B]["edge_cost_before"] == 5802,
          "post-cost64h baseline of 70/5802 already excludes the 77e row (closed at head-1452); "
          "re-listing it gives the recorded but chain-wrong 69/5725")
    # crosscheck against the per-parent bookkeeping baseline facts
    bf = book["derived"]["baseline_facts"]["fold76c:%s" % PARENT_B]
    check("bookkeeping.baseline_agrees",
          bf["rows_before"] == 70 and bf["edge_cost_before"] == 5802
          and bf["join1410_rows"] == 74 and bf["join1410_cost"] == 6113
          and bf["rows_closed_by_earlier_folds"] == 4 and bf["cost_closed_by_earlier_folds"] == 311,
          bf)

    # ---------- D. row->parent D4 attribution over all 174 open parents ----------
    def row_parents(h):
        m = int(h, 16)
        bits = [i for i in range(121) if (m >> i) & 1]
        subs = {canon_hex(m ^ (1 << b)) for b in bits}
        return sorted(p for p in parents if p in subs)

    rp_76c = row_parents(ROW_76C)
    rp_76d = row_parents(ROW_76D)
    rp_77e = row_parents(ROW_77E)
    check("attribution.76c_row_parents", rp_76c == sorted([PARENT_RANK1, PARENT_E]), rp_76c)
    check("attribution.76d_row_parents", rp_76d == sorted([PARENT_RANK1, PARENT_P76D]), rp_76d)
    check("attribution.77e_row_parents", rp_77e == sorted([PARENT_RANK1, PARENT_B]), rp_77e)
    check("attribution.B_not_a_76c_parent", PARENT_B not in rp_76c)
    check("attribution.amendment_P_hex_is_76d_parent_not_76c",
          PARENT_P76D in rp_76d and PARENT_P76D not in rp_76c,
          "the amendment finding text says the 76c row is a D4 child of parents P "
          "(00000000000000003800000208000000) and E; direct recomputation over all 174 open "
          "parents shows the 76c row's parents are the rank-1 parent "
          "(00000000000000801202000040000000) and E; the P hex belongs to the 76d row")
    check("attribution.root_cause_ledger_letter",
          "parents P and E only" in led["finding"]["summary"]
          and book["derived"]["parent_join_stats_1410"][PARENT_RANK1] == {"rows_1410": 5, "cost_1410": 364}
          and book["derived"]["parent_join_stats_1410"][PARENT_P76D] == {"rows_1410": 65, "cost_1410": 5358},
          "the ledger finding used the bare letter P (= the rank-1 parent, join 5/364, in the "
          "per-parent crosscheck convention) without a hex; the amendment resolved P to the "
          "65/5358 parent, which is the 76d row's parent")

    # ---------- E. aggregates ----------
    pa = rec["parents_after"]
    orig_delta = sum(pa[k]["lost_edge_cost"] for k in pa)
    orig_inc = sum(pa[k]["lost_rows"] for k in pa)
    check("aggregate.original_fields", orig_delta == 458 and orig_inc == 6,
          {"delta": orig_delta, "incidences": orig_inc})
    non_b_delta = sum(pa[k]["lost_edge_cost"] for k in pa if k != PARENT_B)
    non_b_inc = sum(pa[k]["lost_rows"] for k in pa if k != PARENT_B)
    check("aggregate.corrected_381_5", non_b_delta == 381 and non_b_inc == 5,
          {"delta": non_b_delta, "incidences": non_b_inc})
    strict_marginal_delta = sum(cost(h) for h in [ROW_76C] if True) * len(rp_76c)
    check("aggregate.strict_76c_marginal",
          strict_marginal_delta == 152 and len(rp_76c) == 2,
          {"parents": len(rp_76c), "delta": strict_marginal_delta,
           "note": "the strict chain marginal of the cost76c fold is 2 parent incidences / "
                   "152 edge delta (the 76c row cost 76 x its 2 parents); the amendment's "
                   "381/5 is the corrected record-total of the cumulative-style parents_after "
                   "bookkeeping, which also lists the 76d row (76) and the rank-1 cumulative "
                   "loss (229 = 76+77+76)"})

    # ---------- F. chain-consistency of every other parents_after entry ----------
    # P (76d row parent)
    pj = join(PARENT_P76D)
    p_after = state_through(PARENT_P76D, "cost76c")
    p_cost = sum(cost(h) for h in p_after)
    check("entry.P.join1410", len(pj) == 65 and sum(cost(h) for h in pj) == 5358)
    check("entry.P.after_matches_record",
          pa[PARENT_P76D]["rows_after"] == len(p_after) == 64
          and pa[PARENT_P76D]["edge_cost_after"] == p_cost == 5282
          and pa[PARENT_P76D]["lost_rows_hexes"] == [ROW_76D],
          {"rows": len(p_after), "cost": p_cost})
    # rank-1 parent
    rj = join(PARENT_RANK1)
    r_after = state_through(PARENT_RANK1, "cost76c")
    r_cost = sum(cost(h) for h in r_after)
    check("entry.rank1.join1410", len(rj) == 5 and sum(cost(h) for h in rj) == 364)
    check("entry.rank1.after_matches_record",
          pa[PARENT_RANK1]["rows_after"] == len(r_after) == 2
          and pa[PARENT_RANK1]["edge_cost_after"] == r_cost == 135
          and sorted(pa[PARENT_RANK1]["lost_rows_hexes"]) == sorted([ROW_76C, ROW_76D, ROW_77E]),
          {"rows": len(r_after), "cost": r_cost})
    # E
    ej = join(PARENT_E)
    e_after = state_through(PARENT_E, "cost76c")
    e_cost = sum(cost(h) for h in e_after)
    e_earlier = sorted(set(ej) - set(e_after) - {ROW_76C})
    check("entry.E.join1410", len(ej) == 71 and sum(cost(h) for h in ej) == 5912)
    check("entry.E.baseline_69_5758",
          pa[PARENT_E]["rows_before"] == 69 and pa[PARENT_E]["edge_cost_before"] == 5758
          and len(e_earlier) == 2 and sum(cost(h) for h in e_earlier) == 154,
          {"earlier_closed": e_earlier, "costs": [cost(h) for h in e_earlier]})
    check("entry.E.after_matches_record",
          pa[PARENT_E]["rows_after"] == len(e_after) == 68
          and pa[PARENT_E]["edge_cost_after"] == e_cost == 5682
          and pa[PARENT_E]["lost_rows_hexes"] == [ROW_76C],
          {"rows": len(e_after), "cost": e_cost})
    # bookkeeping baseline facts crosscheck for P / rank1 / E
    for ph, tag in ((PARENT_P76D, "P"), (PARENT_RANK1, "rank1"), (PARENT_E, "E")):
        bf = book["derived"]["baseline_facts"]["fold76c:%s" % ph]
        check("bookkeeping.fold76c.%s" % tag, True, bf)
    bfb = book["derived"]["baseline_facts"]
    check("bookkeeping.fold76c.P_values",
          bfb["fold76c:%s" % PARENT_P76D]["rows_before"] == 65
          and bfb["fold76c:%s" % PARENT_P76D]["cost_closed_by_earlier_folds"] == 0)
    check("bookkeeping.fold76c.E_values",
          bfb["fold76c:%s" % PARENT_E]["rows_before"] == 69
          and bfb["fold76c:%s" % PARENT_E]["cost_closed_by_earlier_folds"] == 154)

    # ---------- G. global head arithmetic ----------
    fa = rec["frontier_after_cost76c"]
    check("global.frontier_after_76c",
          fa["solved_s6_in_manifest"] == 1473 and fa["unique_remaining_s6"] == 6375
          and fa["sum_remaining_cost"] == 504596,
          [fa["solved_s6_in_manifest"], fa["unique_remaining_s6"], fa["sum_remaining_cost"]])
    led_after = led["derived"]["head_points"][-1]
    check("global.ledger_endpoint_unaffected_note",
          led_after["solved"] == 1476 and led_after["uniq"] == 6372 and led_after["cost"] == 504389,
          "the 76c fold is one link of the verified chain; the amendment does not touch any "
          "global field")
    check("global.amendment_claim",
          "1473" in am["global_arithmetic_unaffected"] or "1473 / 6375 / 504596" in am["global_arithmetic_unaffected"])

    all_pass = all(c["pass"] for c in checks)
    output = {
        "schema": "n11-cost76c-parent-b-amendment-crosscheck-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long lane (verification side)",
        "title": "Independent crosscheck of the additive amendment to the cost76c fold record parent-B entry (commit c4ab218965); corrected values confirmed; one parent-attribution sentence in the amendment finding text is mis-resolved",
        "inputs": {k: {"path": INPUTS[k][0], "git_blob_sha1": INPUTS[k][1]} for k in INPUTS},
        "method": ("5-subset D4 canon-index join recomputation over the pinned head-1410 worklist "
                   "and all 174 open S5 parents; fold-chain ledger closures as the chain ground "
                   "truth; textual-insert reconstruction of the pre-amendment record pinned at "
                   "git blob %s" % ORIGINAL_BLOB),
        "derived": {
            "insert_verification": {"reconstructed_original_blob": rec_orig_blob,
                                    "amendment_block_keys": sorted(am.keys())},
            "parent_B": {"join1410_rows": len(bj), "join1410_cost": bcost,
                         "closure_history": [x for x in b_history if x["rows_closed_in_B"]],
                         "state_through_cost76c": {"rows": len(b_after), "cost": b_after_cost},
                         "corrected_entry": ce,
                         "original_misrecorded_entry": rec["parents_after"][PARENT_B]},
            "row_parent_attribution": {
                "row_76c": {"hex": ROW_76C, "cost": cost(ROW_76C), "parents": rp_76c},
                "row_76d": {"hex": ROW_76D, "cost": cost(ROW_76D), "parents": rp_76d},
                "row_77e": {"hex": ROW_77E, "cost": cost(ROW_77E), "parents": rp_77e}},
            "aggregates": {"original": {"parent_edge_cost_delta": orig_delta,
                                         "parent_row_incidences": orig_inc},
                           "corrected_record_total": {"delta": non_b_delta, "incidences": non_b_inc},
                           "strict_76c_chain_marginal": {"parent_incidences": len(rp_76c),
                                                          "edge_delta": strict_marginal_delta}},
            "other_entries_chain_check": {
                "P_76d_row_parent": {"join1410": [len(pj), sum(cost(h) for h in pj)],
                                       "after_through_76c": [len(p_after), p_cost]},
                "rank1": {"join1410": [len(rj), sum(cost(h) for h in rj)],
                           "after_through_76c": [len(r_after), r_cost]},
                "E": {"join1410": [len(ej), sum(cost(h) for h in ej)],
                       "earlier_closed_before_record_basis": e_earlier,
                       "earlier_closed_costs": [cost(h) for h in e_earlier],
                       "after_through_76c": [len(e_after), e_cost]}},
        },
        "findings": {
            "confirmed": ("the amendment's corrected parent-B values (lost 0 / rows_after 70 / "
                          "edge_cost_after 5802) and corrected aggregate record-total (381 / 5) "
                          "are chain-correct; the insert preserves the original record verbatim; "
                          "the original 69/5725 entry is internally consistent but double-counts "
                          "the 77e row against a post-cost64h baseline that already excludes it"),
            "attribution_error_in_amendment_text": (
                "the amendment finding text states 'The cost76c WIN row is a D4 child of parents "
                "P and E only' and resolves P to 00000000000000003800000208000000. Direct "
                "recomputation over all 174 open parents shows the 76c row "
                "00000000010000809002000001000000 is a D4 child of the rank-1 parent "
                "00000000000000801202000040000000 and E 00000000000000801202000100000000 only. "
                "The hex 00000000000000003800000208000000 is a D4 parent of the 76d row "
                "00000000040000003800080008000000. Root cause: the fold-chain ledger finding "
                "(aa3af62b) used the bare letter P meaning the rank-1 parent (join 5/364 in the "
                "per-parent crosscheck convention) without a hex, and the amendment resolved "
                "that letter to the 65/5358 parent. No corrected value is affected: B is in "
                "neither parent set, so the B correction stands"),
            "clarification": (
                "the amendment's gloss 'chain-correct cost76c marginal per-parent values are "
                "381 and 5' refers to the corrected record-total of the cumulative-style "
                "parents_after bookkeeping (76 + 229 + 76 and 1 + 3 + 1); the strict chain "
                "marginal of the cost76c fold itself is 2 parent incidences / 152 edge delta "
                "(the single closed 76c row, cost 76, times its 2 D4 parents)"),
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all_pass,
        "interpretation_guard": ("Bookkeeping verification only. No engine run, no new verdict, "
                                 "no fold, no closure claim. REFUTED-D10 and STERILE are not "
                                 "LOSS proofs."),
        "unknown_status": ("Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
                           "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."),
    }
    with open(out_path, "w") as f:
        f.write(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"out": out_path, "all_pass": all_pass, "checks": len(checks),
                      "failed": [c for c in checks if not c["pass"]]}, indent=2))
    if not all_pass:
        sys.exit(1)

if __name__ == "__main__":
    main()
