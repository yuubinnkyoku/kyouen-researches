#!/usr/bin/env python3
"""Verification-side crosscheck of the complete published fold chain
head-1410 -> head-1476 (standard 11x11 lane, receipt-fold bookkeeping).

Chain records (all in research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/,
pinned at commit 376e4f44c791cfae345de564ee8a414ee0c8afa1):

  cost65j (1410->1419), cost64d (1419->1435), cost64f (1435->1438),
  cost64g (1438->1441), cost65n (1441->1444), cost66c (1444->1450),
  cost76d77e (1450->1452), cost64h (1452->1472), cost76c (1472->1473),
  cost66i bit19 (1473->1476)

Against the raw head-1410 worklist (6,438 rows, total cost 509,109) the script
independently recomputes:

  - per-record closures and per-parent attributions (both published styles),
  - D4 orbit-join membership of every attributed row (5-subset canon index,
    cross-validated against the direct join),
  - absolute per-parent ledgers (rows_before / rows_after vs join1410 minus
    cumulative chain closures) for every record,
  - global disjointness of all 66 closed rows and the telescoping head ledger
    (solved / unique_remaining / sum_remaining_cost) at every record.

FINDING (verified here): the published cost76c record's parents_after entry for
parent 00000000000000801202000000040000 re-lists the 77e row (closed by the
cost76d77e fold at head-1452) as a loss on a post-cost64h baseline, double-counting
it: published rows_after 69 / edge 5725, chain-correct values 70 / 5802. The 76c
row itself is a D4 child of parents P and E only, not of B. Global head arithmetic
is unaffected.

No engine is run; no new verdict is produced. REFUTED-D10 is not a LOSS proof.

Usage: python3 crosscheck_fold_chain_ledger_1410_1476_20261118.py --input-dir in --folds-dir folds --output out.json
"""
import argparse
import csv
import hashlib
import json
import os
import sys
from pathlib import Path

N = 11

TFS = [
    lambda x, y: (x, y),
    lambda x, y: (y, N - 1 - x),
    lambda x, y: (N - 1 - x, N - 1 - y),
    lambda x, y: (N - 1 - y, x),
    lambda x, y: (N - 1 - x, y),
    lambda x, y: (x, N - 1 - y),
    lambda x, y: (y, x),
    lambda x, y: (N - 1 - y, N - 1 - x),
]

CHAIN = [
    ("cost65j", "class-frontier-cost65j-receipts-recompute-20261116.json", "old"),
    ("cost64d", "class-frontier-cost64d-receipts-recompute-20261116.json", "old"),
    ("cost64f", "class-frontier-cost64f-receipts-recompute-20261116.json", "old"),
    ("cost64g", "class-frontier-cost64g-receipts-recompute-20261116.json", "old"),
    ("cost65n", "class-frontier-cost65n-receipts-recompute-20261116.json", "old"),
    ("cost66c", "class-frontier-cost66c-receipts-recompute-20261116.json", "old"),
    ("cost76d77e", "class-frontier-cost76d77e-receipts-recompute-20261116.json", "old"),
    ("cost64h", "class-frontier-cost64h-receipts-recompute-20261117.json", "new"),
    ("cost76c", "class-frontier-cost76c-receipts-recompute-20261117.json", "new"),
    ("cost66i", "class-frontier-cost66i-bit19-receipts-recompute-20261118.json", "new"),
]

PARENT_B = "00000000000000801202000000040000"
ROW_76C = "00000000010000809002000001000000"
ROW_77E = "00000000040000809002000000004000"

KNOWN_PINS = {
    "worklist1410.csv": "2fee1d0718547a62e346d35f5858d7913e37c097",
    "reconc.json": "6992f2dcc8b87a5409cff31c8a87134fc4283a6a",
}

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail if isinstance(detail, str) else json.dumps(detail)})


def hx(m):
    return format(m, "032x")


def popcount(m):
    return bin(m).count("1")


def stone_bits(mask):
    return [i for i in range(N * N) if (mask >> i) & 1]


def apply_t(mask, t):
    out = 0
    for i in stone_bits(mask):
        x, y = i % N, i // N
        x2, y2 = t(x, y)
        out |= 1 << (y2 * N + x2)
    return out


def canon(mask):
    return min(apply_t(mask, t) for t in TFS)


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", default="in")
    ap.add_argument("--folds-dir", default="folds")
    ap.add_argument("--output", default="out.json")
    args = ap.parse_args()
    ind, fd = Path(args.input_dir), Path(args.folds_dir)

    # ---------- pins ----------
    pin_values = {}
    for name, pin in sorted(KNOWN_PINS.items()):
        data = (ind / name).read_bytes()
        sha = git_blob_sha(data)
        pin_values[name] = sha
        check("pin." + name.rsplit(".", 1)[0], sha == pin, sha)
    for _tag, fn, _style in CHAIN:
        data = (fd / fn).read_bytes()
        sha = git_blob_sha(data)
        pin_values[fn] = sha
        check("pin." + fn.replace("class-frontier-", "").replace(".json", ""), True, sha)
    d60c_data = (fd / "class-frontier-cost60c-receipts-recompute-20261116.json").read_bytes()
    pin_values["class-frontier-cost60c-receipts-recompute-20261116.json"] = git_blob_sha(d60c_data)
    check("pin.cost60c", True, git_blob_sha(d60c_data))

    # ---------- worklist ----------
    work_rows = list(csv.DictReader((ind / "worklist1410.csv").open()))
    wl = {r["s6_canonical_hex"]: r for r in work_rows}
    cost = {h: int(r["own_candidates_s6_s7_edge_cost"]) for h, r in wl.items()}
    check("wl.rows", len(work_rows) == 6438, str(len(work_rows)))
    check("wl.all_six_stones", all(popcount(int(h, 16)) == 6 for h in wl), "")
    WL_TOTAL_COST = sum(cost.values())
    check("wl.total_cost", WL_TOTAL_COST == 509109, str(WL_TOTAL_COST))

    # ---------- D4 5-subset canon index ----------
    index = {}
    for h in wl:
        m = int(h, 16)
        bits = stone_bits(m)
        for drop in range(6):
            sub = 0
            for j, b in enumerate(bits):
                if j != drop:
                    sub |= 1 << b
            index.setdefault(hx(canon(sub)), []).append(h)
    for k in index:
        index[k] = sorted(set(index[k]))

    def join(parent_hex):
        return index.get(parent_hex, [])

    # self-test against direct join on the deliverable-2 nine parents
    nine = {
        "H": ("00000000000000003800000000808000", 83),
        "A": ("00000000000000003800000208000000", 65),
        "F": ("00000000000000003801000000800000", 69),
        "X": ("00000000000000403800000008000000", 24),
        "B": (PARENT_B, 74),
        "I": ("00000000000000801202000000080000", 68),
        "P": ("00000000000000801202000040000000", 5),
        "E": ("00000000000000801202000100000000", 71),
        "G": ("00000000000000801222000000000000", 70),
    }

    def direct_join(ph):
        pm = int(ph, 16)
        imgs = [apply_t(pm, t) for t in TFS]
        out = []
        for h in wl:
            rm = int(h, 16)
            for im in imgs:
                if im & ~rm == 0:
                    out.append(h)
                    break
        return sorted(out)

    ok = True
    for tag, (p, expect) in nine.items():
        if direct_join(p) != join(p) or len(join(p)) != expect:
            ok = False
    check("join.index_selftest_vs_direct_and_deliverable2", ok, json.dumps({t: len(join(p)) for t, (p, _) in nine.items()}))

    # ---------- load records ----------
    recs = []
    for tag, fn, style in CHAIN:
        d = json.loads((fd / fn).read_bytes())
        fa_key = [k for k in d if k.startswith("frontier_after")][0]
        fa = d[fa_key]
        br = d.get("baseline_record") or {}
        fb = br.get("frontier_before") if isinstance(br, dict) else None
        if fb is not None:
            basis = {"solved": fb["solved_s6_in_manifest"], "cost": fb["sum_remaining_cost"], "uniq": fb["unique_remaining_s6"]}
        elif isinstance(d.get("basis_head"), int):
            basis = {"solved": d["basis_head"], "cost": None, "uniq": None}
        elif isinstance(d.get("basis_head"), dict):
            bh = d["basis_head"]
            basis = {"solved": bh["solved_s6_in_manifest"], "cost": bh["sum_remaining_cost"], "uniq": bh["unique_remaining_s6"]}
        elif isinstance(br, dict):
            basis = None
            for k, v in br.items():
                if isinstance(v, str) and v.count("/") >= 5:
                    head = v.split(" (")[0].split("/")
                    try:
                        basis = {"solved": int(head[0]), "cost": int(head[3]), "uniq": int(head[2])}
                    except ValueError:
                        basis = None
                    break
        else:
            basis = None
        recs.append({"tag": tag, "file": fn, "style": style, "d": d, "basis": basis,
                     "after": fa, "after_solved": fa["solved_s6_in_manifest"]})

    # ---------- 60c boundary ----------
    d60c = json.loads(d60c_data)
    fa60c = d60c["frontier_after_cost60c"]
    lost60c = set()
    for p, v in d60c.get("lost_rows_per_parent", {}).items():
        if isinstance(v, dict):
            lost60c |= set(v)
    check("b60c.after_state_is_worklist", fa60c["solved_s6_in_manifest"] == 1410
          and fa60c["unique_remaining_s6"] == 6438 and fa60c["sum_remaining_cost"] == 509109, "")
    check("b60c.lost_rows_absent_from_worklist",
          len(lost60c) == 3 and not (lost60c & set(wl)), json.dumps(sorted(lost60c)))

    # ---------- chain contiguity ----------
    ok = True
    prev_after = 1410
    for r in recs:
        if r["basis"] is None or r["basis"]["solved"] != prev_after:
            ok = False
        prev_after = r["after_solved"]
    check("chain.contiguity_1410_to_1476", ok and prev_after == 1476,
          json.dumps([{"tag": r["tag"], "basis": r["basis"]["solved"] if r["basis"] else None,
                        "after": r["after_solved"]} for r in recs]))
    ok_basis_cost = True
    for r in recs:
        if r["basis"]["cost"] is not None:
            fa_prev = recs[recs.index(r) - 1]["after"] if recs.index(r) > 0 else None
            if fa_prev is not None and (r["basis"]["cost"] != fa_prev["sum_remaining_cost"]
                                        or r["basis"]["uniq"] != fa_prev["unique_remaining_s6"]):
                ok_basis_cost = False
    check("chain.basis_cost_uniq_match_predecessor_after", ok_basis_cost, "")

    others = []
    chain_files = set(f for _, f, _ in CHAIN)
    for fn in sorted(os.listdir(fd)):
        if fn in chain_files or fn.startswith("class-frontier-cost60c"):
            continue
        try:
            dd = json.loads((fd / fn).read_bytes())
        except Exception:
            continue
        for k in dd:
            if k.startswith("frontier_after") and isinstance(dd[k], dict):
                s = dd[k].get("solved_s6_in_manifest")
                if s is not None and 1410 < s <= 1476:
                    others.append((fn, s))
    check("chain.no_other_published_segments_in_window", others == [], json.dumps(others))

    # ---------- per-record closures and attributions ----------
    prev_closed = set()
    for r in recs:
        d = r["d"]
        style = r["style"]
        attributed = {}  # parent -> set(rows) attributed to this record (candidates)
        if style == "old":
            lrp = d.get("lost_rows_per_parent") or {}
            for p, v in lrp.items():
                if isinstance(v, dict):
                    attributed[p] = set(v)
                    # recorded costs must match worklist
            r["closure"] = set().union(*attributed.values()) if attributed else set()
            r["attributed"] = attributed
            r["closes_on"] = {p: rows for p, rows in attributed.items()}  # actual new closures
        else:
            pa = d.get("parents_after") or {}
            if r["tag"] == "cost64h":
                for p, e in pa.items():
                    attributed[p] = set(e.get("lost_rows_hexes", []))
                r["closure"] = set().union(*attributed.values()) if attributed else set()
                r["attributed"] = attributed
                r["closes_on"] = {p: set(rows) for p, rows in attributed.items()}
            elif r["tag"] == "cost76c":
                for p, e in pa.items():
                    attributed[p] = set(e.get("lost_rows_hexes", []))
                cand = set().union(*attributed.values()) if attributed else set()
                r["closure"] = cand - prev_closed
                r["attributed"] = attributed
                r["closes_on"] = {p: rows & r["closure"] for p, rows in attributed.items()}
                r["relisted"] = {p: rows & prev_closed for p, rows in attributed.items()}
            else:  # cost66i: closure derived from receipt marginal manifest
                marg = set(d["receipts"][0]["marginal_manifest_hexes"])
                open_at_basis = set(wl) - prev_closed
                r["closure"] = marg & open_at_basis
                r["attributed"] = {}
                r["closes_on"] = {}
                for p, e in pa.items():
                    r["closes_on"][p] = set(x for x in r["closure"] if x in set(join(p)))
        delta = r["after_solved"] - r["basis"]["solved"]
        check("closure.%s_matches_head_delta" % r["tag"], len(r["closure"]) == delta,
              "closed=%d delta=%d" % (len(r["closure"]), delta))
        r["closure_cost"] = sum(cost[x] for x in r["closure"])
        fa_cost = r["after"]["sum_remaining_cost"]
        check("closure.%s_cost_delta" % r["tag"],
              r["basis"]["cost"] is not None and r["basis"]["cost"] - fa_cost == r["closure_cost"],
              "basis=%s after=%s closed=%d" % (r["basis"]["cost"], fa_cost, r["closure_cost"]))
        tot = d.get("totals")
        if isinstance(tot, dict) and "s6_edge_cost_removed" in tot:
            check("closure.%s_totals_field" % r["tag"], tot["s6_edge_cost_removed"] == r["closure_cost"], "")
        prev_closed |= r["closure"]
        r["prev_closed_before"] = set(x for x in prev_closed)  # not used later; kept for clarity

    # 64h top-level incidence/cost fields (incidence-weighted vs unique-row closure cost)
    d64h = [r for r in recs if r["tag"] == "cost64h"][0]
    inc = sum(len(rows) for rows in d64h["attributed"].values())
    attr_cost = sum(sum(cost[x] for x in rows) for rows in d64h["attributed"].values())
    check("closure.cost64h_incidence_fields",
          d64h["d"].get("parent_row_incidences") == inc
          and d64h["d"].get("parent_edge_cost_delta") == attr_cost
          and attr_cost >= d64h["closure_cost"],
          "incidences=%d attr_cost=%d unique_closure_cost=%d" % (inc, attr_cost, d64h["closure_cost"]))

    # 76c re-listed rows must have been closed earlier by the chain (attribution completeness)
    r76c = [r for r in recs if r["tag"] == "cost76c"][0]
    earlier = set().union(*[x["closure"] for x in recs[:recs.index(r76c)]])
    relisted = set().union(*r76c["relisted"].values()) if r76c["relisted"] else set()
    check("closure.cost76c_relisted_rows_closed_earlier",
          relisted != set() and relisted <= earlier,
          json.dumps({p: sorted(v) for p, v in r76c["relisted"].items() if v}))

    # ---------- global disjointness and worklist containment ----------
    global_closed = {}
    ok_disjoint = True
    for r in recs:
        for row in r["closure"]:
            if row in global_closed:
                ok_disjoint = False
            global_closed[row] = r["tag"]
    check("chain.global_disjoint_66_rows", ok_disjoint and len(global_closed) == 66, str(len(global_closed)))
    check("chain.closed_rows_in_worklist", all(row in wl for row in global_closed), "")
    check("chain.total_closed_cost", sum(cost[x] for x in global_closed) == 509109 - 504389,
          str(sum(cost[x] for x in global_closed)))

    # ---------- membership of every attributed row ----------
    ok_mem = True
    mem_bad = []
    all_parents = set()
    for r in recs:
        for p, rows in r["attributed"].items():
            all_parents.add(p)
            j = set(join(p))
            for row in rows:
                if row not in j:
                    ok_mem = False
                    mem_bad.append((r["tag"], p, row))
    for r in recs:
        for p in (r["d"].get("parents_after") or {}):
            if len(p) == 32:
                all_parents.add(p)
    check("chain.attributed_rows_join_membership", ok_mem and not mem_bad, json.dumps(mem_bad[:5]))

    ok = True
    for p in all_parents:
        if popcount(int(p, 16)) != 5 or hx(canon(int(p, 16))) != p:
            ok = False
    check("chain.parents_canon_popcount5", ok, str(len(all_parents)))

    # ---------- absolute per-parent ledger ----------
    mismatches = []
    parent_ledger = {}
    order = {r["tag"]: i for i, r in enumerate(recs)}
    for p in sorted(all_parents):
        jrows = set(join(p))
        jcost = sum(cost[x] for x in jrows)
        cum_rows, cum_cost = 0, 0
        events = []
        for r in recs:
            closes = set(r.get("closes_on", {}).get(p, []))
            entry = (r["d"].get("parents_after") or {}).get(p)
            if not closes and entry is None:
                continue
            cum_rows += len(closes)
            cum_cost += sum(cost[x] for x in closes)
            ev = {"tag": r["tag"], "closes": sorted(closes),
                  "cum_rows": cum_rows, "cum_cost": cum_cost,
                  "ledger_rows_before": len(jrows) - (cum_rows - len(closes)),
                  "ledger_rows_after": len(jrows) - cum_rows,
                  "ledger_cost_after": jcost - cum_cost}
            if isinstance(entry, dict):
                ra = entry.get("rows_after", entry.get("rows"))
                ea = entry.get("edge_cost_after", entry.get("edge_cost"))
                rb = entry.get("rows_before")
                eb = entry.get("edge_cost_before")
                ev["published_rows_after"] = ra
                ev["published_cost_after"] = ea
                if ra is not None and ra != ev["ledger_rows_after"]:
                    mismatches.append({"tag": r["tag"], "parent": p, "field": "rows_after",
                                       "published": ra, "ledger": ev["ledger_rows_after"]})
                if ea is not None and ea != ev["ledger_cost_after"]:
                    mismatches.append({"tag": r["tag"], "parent": p, "field": "edge_cost_after",
                                       "published": ea, "ledger": ev["ledger_cost_after"]})
                if r["style"] == "old" or r["tag"] == "cost64h":
                    if rb is not None and rb != ev["ledger_rows_before"]:
                        mismatches.append({"tag": r["tag"], "parent": p, "field": "rows_before",
                                           "published": rb, "ledger": ev["ledger_rows_before"]})
                    if eb is not None and eb != jcost - (cum_cost - sum(cost[x] for x in closes)):
                        mismatches.append({"tag": r["tag"], "parent": p, "field": "edge_cost_before",
                                           "published": eb, "ledger": jcost - (cum_cost - sum(cost[x] for x in closes))})
                # internal arithmetic of the entry itself
                if r["style"] == "old" and rb is not None:
                    if rb - ra != len(closes):
                        mismatches.append({"tag": r["tag"], "parent": p, "field": "internal_rows_delta",
                                           "published": rb - ra, "ledger": len(closes)})
                if r["tag"] in ("cost64h", "cost76c") and "lost_rows" in entry:
                    if entry["rows_after"] != entry["rows_before"] - entry["lost_rows"]:
                        mismatches.append({"tag": r["tag"], "parent": p, "field": "internal_rows_delta2"})
                    if entry.get("edge_cost_after") != entry.get("edge_cost_before") - entry.get("lost_edge_cost"):
                        mismatches.append({"tag": r["tag"], "parent": p, "field": "internal_cost_delta2"})
                if r["tag"] == "cost76c" and "lost_rows" in entry:
                    cand = set(entry.get("lost_rows_hexes", []))
                    if entry["lost_rows"] != len(cand):
                        mismatches.append({"tag": r["tag"], "parent": p, "field": "lost_rows_vs_hexes"})
            events.append(ev)
        if events:
            parent_ledger[p] = {"join1410_rows": len(jrows), "join1410_cost": jcost,
                                "cum_closed": cum_rows, "final_ledger_rows": len(jrows) - cum_rows,
                                "final_ledger_cost": jcost - cum_cost, "events": events}

    expected_mismatch = {"tag": "cost76c", "parent": PARENT_B, "field_rows": {"published": 69, "ledger": 70},
                          "field_cost": {"published": 5725, "ledger": 5802}}
    b_mm = [m for m in mismatches if m["tag"] == "cost76c" and m["parent"] == PARENT_B]
    others_mm = [m for m in mismatches if not (m["tag"] == "cost76c" and m["parent"] == PARENT_B)]
    check("ledger.all_other_entries_absolute_consistent", others_mm == [], json.dumps(others_mm[:8]))
    check("findings.cost76c_B_entry_double_counts_77e",
          sorted(m["field"] for m in b_mm) == ["edge_cost_after", "rows_after"]
          and all(m["published"] == expected_mismatch["field_" + ("rows" if m["field"] == "rows_after" else "cost")]["published"]
                  and m["ledger"] == expected_mismatch["field_" + ("rows" if m["field"] == "rows_after" else "cost")]["ledger"] for m in b_mm),
          json.dumps(b_mm))
    # characterization: 76c row not a child of B; 77e row closed at head-1452 by cost76d77e
    jb = set(join(PARENT_B))
    check("findings.cost76c_row_not_child_of_B_and_77e_closed_at_1452",
          ROW_76C not in jb and ROW_77E in jb
          and ROW_77E in [r for r in recs if r["tag"] == "cost76d77e"][0]["closure"]
          and ROW_77E not in [r for r in recs if r["tag"] == "cost76c"][0]["closure"],
          "76c_row_in_join_B=%s; 77e_closed_by=cost76d77e" % (ROW_76C in jb))
    # B ledger facts
    pb = parent_ledger.get(PARENT_B)
    check("findings.B_true_state_at_1476", pb is not None and pb["final_ledger_rows"] == 70
          and pb["final_ledger_cost"] == 5802 and pb["cum_closed"] == 4
          and pb["join1410_rows"] == 74, json.dumps({k: v for k, v in pb.items() if k != "events"} if pb else {}))

    # 66i per-parent derivation crosscheck
    r66i = [r for r in recs if r["tag"] == "cost66i"][0]
    ok = True
    for p, e in (r66i["d"].get("parents_after") or {}).items():
        derived = set(r66i["closes_on"].get(p, []))
        if e.get("lost_rows") != len(derived) or e.get("lost_edge_cost") != sum(cost[x] for x in derived):
            ok = False
    check("closure.cost66i_per_parent_derivation", ok, "")

    # ---------- telescoping head ledger ----------
    ok = True
    cum_rows, cum_cost = 0, 0
    head_points = []
    for r in recs:
        cum_rows += len(r["closure"])
        cum_cost += r["closure_cost"]
        fa = r["after"]
        if (fa["solved_s6_in_manifest"] != 1410 + cum_rows or fa["unique_remaining_s6"] != 6438 - cum_rows
                or fa["sum_remaining_cost"] != 509109 - cum_cost):
            ok = False
        head_points.append({"tag": r["tag"], "solved": fa["solved_s6_in_manifest"],
                            "uniq": fa["unique_remaining_s6"], "cost": fa["sum_remaining_cost"],
                            "ledger": [1410 + cum_rows, 6438 - cum_rows, 509109 - cum_cost]})
    check("ledger.head_telescopes_from_worklist_at_every_record", ok, json.dumps(head_points))

    reconc = json.loads((ind / "reconc.json").read_bytes())
    final = recs[-1]["after"]
    check("ledger.head1476_matches_reconciliation",
          final["solved_s6_in_manifest"] == 1476 and final["unique_remaining_s6"] == 6372
          and final["sum_remaining_cost"] == 504389
          and reconc["current_parent"]["head"] == "1476/174/6372/504389/4645/368303", "")

    all_pass = all(c["pass"] for c in CHECKS)
    out = {
        "schema": "n11-fold-chain-ledger-1410-1476-crosscheck-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long-term lane, verification-side crosscheck session (standard 11x11 weak-resolution)",
        "title": "complete fold-chain ledger crosscheck head-1410 -> head-1476: ten published receipt-fold records audited against the raw 6,438-row head-1410 worklist; one per-parent double-count found in the published cost76c record (parent B), all other bookkeeping confirmed",
        "inputs": {k: pin_values[k] for k in sorted(pin_values)},
        "source_pin_commit": "376e4f44c791cfae345de564ee8a414ee0c8afa1",
        "method": "fourth-implementation D4; 5-subset canon index over all 6,438 rows (cross-validated against the direct orbit join on the deliverable-2 nine parents); per-record closures extracted from both published bookkeeping styles; absolute per-parent ledgers vs join1410 minus cumulative chain closures; no engine, no new verdict",
        "finding": {
            "summary": "published cost76c parents_after entry for parent 00000000000000801202000000040000 (B) re-lists the 77e row (closed by cost76d77e at head-1452) as a new loss on a post-cost64h baseline: published rows_after 69 / edge_cost_after 5725; chain-correct values 70 / 5802. The 76c row itself is a D4 child of parents P and E only. Global head arithmetic (1473/6375/504596) is unaffected: the fold closes exactly one row once.",
            "recommended_fix": "in class-frontier-cost76c-receipts-recompute-20261117.json, parent B entry: lost_rows 1 -> 0, lost_rows_hexes -> [], lost_edge_cost 77 -> 0, rows_after 69 -> 70, edge_cost_after 5725 -> 5802 (or restated as cumulative-since-1410 with rows_before 74 and lost_rows_hexes of all 5 closed rows).",
        },
        "derived": {
            "chain": [{"tag": r["tag"], "file": r["file"], "basis": r["basis"]["solved"], "after": r["after_solved"],
                       "closed_rows": len(r["closure"]), "closed_cost": r["closure_cost"],
                       "closure": sorted(r["closure"])} for r in recs],
            "closed_rows_66": sorted(global_closed),
            "parent_ledger": parent_ledger,
            "head_points": head_points,
            "parents_count": len(all_parents),
            "mismatches_all": mismatches,
        },
        "checks": CHECKS,
        "check_count": len(CHECKS),
        "all_pass": all_pass,
        "interpretation_guard": "Bookkeeping verification only. The ten fold records form a contiguous, disjoint, fully parent-accounted chain from head-1410 to head-1476 except the single characterized B-entry double-count in cost76c (global state unaffected). Receipt-level certificate content was not re-verified here (see the head-1476 reconciliation crosscheck for six certificates). REFUTED-D10 is not a LOSS proof; no S5 parent is closed by this audit.",
        "unknown_status": "11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
    }
    with open(args.output, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print("checks:", len(CHECKS), "all_pass:", all_pass)
    for c in CHECKS:
        if not c["pass"]:
            print("FAIL:", c["check"], str(c["detail"])[:400])
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
