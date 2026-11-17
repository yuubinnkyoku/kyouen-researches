#!/usr/bin/env python3
"""Downstream cross-verification of the 13 special non-STERILE candidate rows
of the 57 partial-STERILE head-1410 S5 parents.

The companion audit (audit_partial_parent_nonsterile_children_20261118.py,
published at commit e7743ed4) enumerated the 3,555 distinct non-STERILE
remaining S6 rows of the 57 partial-STERILE (cross_cover_required) S5 parents
and showed that exactly 13 of them carry a non-unswept worklist status:

  9  win_receipt_scheduled  (cost-65j pre-fold cover; fold applied later)
  2  win_pending            (engine WIN7-D10 receipts swept, fold not landed)
  2  transfer_partial       (own candidates pre-determined REFUTED-D10 by
                             canonical verdict-cache transfers)

This script verifies each group against the *downstream* published records on
main, independently of the worklist-producing implementation:

  1. win_receipt_scheduled: the 9 rows are set-identical to the 9 rows closed
     by the published cost-65j receipt fold (head 1410 -> 1419); the 635 own
     candidates equal both the worklist cost sum and the head cost delta
     509109 - 508474.
  2. win_pending: the cost-76d / cost-77e sweep audits, WIN7 certificate
     manifests and the published second independent verification are all
     internally consistent with the worklist tallies, and each WIN root hex
     is re-derived from the child mask by exact one-bit arithmetic
     (root == child | 1 << bit over the 121-bit 11x11 mask).
  3. transfer_partial: every transferred REFUTED-D10 bit is re-verified
     geometrically with an independent D4 canonicalisation (canon of the
     row's one-stone extension equals the canon of the cited via child);
     for the cost-76c child the 15 transfer predictions are additionally
     confirmed against the later direct v17 sweep of that row in the
     published census v19 verdict map (15/15 REFUTED-D10, 0 conflicts, and
     the 2 later WIN bits 61/99 are untouched by the transfers).

No engine is run. No fold is applied. No closure, receipt or verdict claim is
made here beyond quoting the pinned published records.

Inputs (all git-blob-pinned, all published on main):
  head-1410 remaining S6 worklist CSV          2fee1d07...
  theorem-applicability scan output            24f214e6...
  scan second independent verification         65e3e822...
  cost-65j in-flight fold record              7a4c9007...
  cost-76d sweep audit                        a57af016...
  cost-76d WIN7 certificate manifest          e8a6116a...
  cost-76d/77e second independent verific.    d267fa8d...
  cost-77e sweep record                       57afde38...
  presweep census v19 (head 1473)             a0c6abaf...
  companion enumeration output (prior audit) 30c8fdc4...

Output: deterministic; two runs byte-identical.
"""

import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent               # experiments/n11-head1410-partial-parent-nonsterile-children-20261118/
EXP = HERE.parent                                    # experiments/
REPO = EXP.parents[1]                                # repo root
LANE = EXP / "n11-s2-5960-ms5-s7-reuse-20261113" / "output"

WORKLIST = EXP / "n11-class2-lane-closability-ranking-20261116" / "output" / "class-frontier-remaining-s6-worklist-1410-20261116.csv"
SCAN = EXP / "n11-class2-lane-sterile-unclosability-20261116" / "output" / "theorem-applicability-scan-20261116.json"
SCANVERIFY = EXP / "n11-class2-lane-sterile-unclosability-20261116" / "output" / "theorem-applicability-scan-second-independent-verification-20261116.json"
C65J = LANE / "class2-lane-cost65j-inflight-20261115.json"
S76D = LANE / "class2-lane-cost76d-sweep-audit-20261116.json"
C76D = LANE / "class2-lane-cost76d-win7-certificates-20261116.json"
V76D77E = LANE / "class2-lane-cost76d-77e-second-independent-verification-20261116.json"
S77E = LANE / "class2-lane-cost77e-sweep-20261116.json"
CENSUS19 = LANE / "class2-lane-next-target-presweep-1473-v19-20261118.json"
PRIOR = HERE / "output" / "n11-head1410-partial-parent-nonsterile-children-20261118.json"
OUT = HERE / "output" / "nonsterile-special-rows-downstream-20261118.json"

PINS = {
    "worklist": (str(WORKLIST), "2fee1d0718547a62e346d35f5858d7913e37c097"),
    "scan": (str(SCAN), "24f214e6a9dd721ef95ac97d6b84cf34af33b14b"),
    "scanverify": (str(SCANVERIFY), "65e3e822a390ee945f632d07e80c95049985078c"),
    "c65j": (str(C65J), "7a4c900710e3ddb34fb9e272e8e673815e13a4f3"),
    "s76d": (str(S76D), "a57af0161942a6f597cfabe9aef892df2fa7be3f"),
    "c76d": (str(C76D), "e8a6116aec45c19642877db85340e120d23331b3"),
    "v76d77e": (str(V76D77E), "d267fa8d93017110ff74df4520b3a8e8a47bee5b"),
    "s77e": (str(S77E), "57afde38509ae3c10df0c6c38883c9b5d4fc67a5"),
    "census19": (str(CENSUS19), "a0c6abaf0df163eddc35f8b8dc0f8c0eb4268fe6"),
    "prior": (str(PRIOR), "30c8fdc4e7212bafe271662d8dcf0bbbde35b63b"),
}


def images(mask):
    result = [0] * 8
    for p in range(121):
        if mask >> p & 1:
            x, y = p % 11, p // 11
            coords = ((x, y), (y, 10 - x), (10 - x, 10 - y), (10 - y, x),
                      (10 - x, y), (x, 10 - y), (y, x), (10 - y, 10 - x))
            for i, (a, b) in enumerate(coords):
                result[i] |= 1 << (11 * b + a)
    return result


IMG = [images(1 << p) for p in range(121)]


def t(mask, r):
    v = 0
    for p in range(121):
        if mask >> p & 1:
            v |= IMG[p][r]
    return v


def canon(mask):
    return min(t(mask, r) for r in range(8))


def gitblob(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def all_bools_true(obj):
    """True iff every boolean leaf in obj (dict/list) is True; non-bool leaves
    (strings, ints such as node counts) are ignored."""
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, dict):
        return all(all_bools_true(v) for v in obj.values())
    if isinstance(obj, list):
        return all(all_bools_true(v) for v in obj)
    return True


def main():
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "pass": bool(ok), "detail": str(detail)})
        return bool(ok)

    # ---- A: pin all inputs -------------------------------------------
    pin_ok = True
    for key, (path, expected) in PINS.items():
        data = Path(path).read_bytes()
        actual = gitblob(data)
        ok = actual == expected
        pin_ok = pin_ok and ok
        check(f"A.pin.{key}", ok, actual if ok else f"{actual} != {expected}")
    if not pin_ok:
        emit(checks, None)
        return

    scan = json.loads(Path(PINS["scan"][0]).read_text())
    scanverify = json.loads(Path(PINS["scanverify"][0]).read_text())
    c65j = json.loads(Path(PINS["c65j"][0]).read_text())
    s76d = json.loads(Path(PINS["s76d"][0]).read_text())
    c76d = json.loads(Path(PINS["c76d"][0]).read_text())
    v76d77e = json.loads(Path(PINS["v76d77e"][0]).read_text())
    s77e = json.loads(Path(PINS["s77e"][0]).read_text())
    census19 = json.loads(Path(PINS["census19"][0]).read_text())
    prior = json.loads(Path(PINS["prior"][0]).read_text())

    with Path(PINS["worklist"][0]).open() as fh:
        wrows = {r["s6_canonical_hex"]: r for r in csv.DictReader(fh)}

    special = prior["special_nonsterile_rows"]
    check("B.prior.special_rows", len(special) == 13, len(special))
    by_cat = {}
    for r in special:
        by_cat.setdefault(r["category"], []).append(r["hex"])
    check("B.prior.categories",
          sorted((k, len(v)) for k, v in by_cat.items()) ==
          [("transfer_partial", 2), ("win_pending", 2), ("win_receipt_scheduled", 9)],
          {k: len(v) for k, v in by_cat.items()})

    # every special row's worklist record agrees with the prior audit fields
    # (open_parents counts all open parents, incl. own_closable ones, so it is
    # not required to equal the partial-parent count of the prior enumeration)
    ok_b2 = True
    for r in special:
        w = wrows[r["hex"]]
        ok_b2 = ok_b2 and w["category"] == r["category"]
        ok_b2 = ok_b2 and int(w["own_candidates_s6_s7_edge_cost"]) == r["cost"]
        ok_b2 = ok_b2 and int(w["open_parents"]) >= len(r["partial_parents"])
    check("B.worklist_fields_match", ok_b2)

    # ---- C: win_receipt_scheduled (9 rows) ----------------------------
    sched = sorted(by_cat["win_receipt_scheduled"])
    fold = c65j["fold"]
    closed = sorted(fold["rows_closed_hexes"])
    check("C1.scheduled_equals_fold_rows_closed", sched == closed,
          f"{len(sched)} vs {len(closed)}")
    check("C1.fold.rows_closed", fold["rows_closed"] == 9, fold["rows_closed"])
    own_sum = sum(int(wrows[h]["own_candidates_s6_s7_edge_cost"]) for h in sched)
    hb = [int(x) for x in fold["head_before"].split("/")]
    ha = [int(x) for x in fold["head_after"].split("/")]
    check("C2.scheduled_own_sum", own_sum == 635, own_sum)
    check("C2.head_cost_delta", hb[3] - ha[3] == 635, hb[3] - ha[3])
    check("C3.head_rows_delta", hb[2] - ha[2] == 9 == len(sched), hb[2] - ha[2])
    check("C3.head_parents_unchanged", hb[1] == ha[1] == 174, (hb[1], ha[1]))
    ok_c4 = all(h not in scan["targets"] for h in sched)
    check("C4.scheduled_absent_from_scan_targets", ok_c4)
    ok_c5 = all(wrows[h]["engine_win7_d10"] == "0" and
                wrows[h]["engine_refuted_d10"] == "0" and
                wrows[h]["transferred_refuted_d10"] == "0" and
                wrows[h]["open_candidates_after_transfers"] == "0"
                for h in sched)
    check("C5.scheduled_worklist_counters_zero", ok_c5)
    status_txt = c65j["status"]
    ok_c6 = ("65/65 candidates resolved" in status_txt and
             "17 WIN7-D10" in status_txt and
             "48 REFUTED-D10" in status_txt and
             "0 capped" in status_txt)
    check("C6.c65j_status_receipt_counts", ok_c6,
          "65/65 resolved / 17 WIN receipts / 48 REFUTED / 0 capped")

    # ---- D: win_pending (2 rows) -------------------------------------
    row76 = "00000000040000003800080008000000"
    row77 = "00000000040000809002000000004000"
    check("D0.pending_hexes", sorted(by_cat["win_pending"]) == sorted([row76, row77]),
          by_cat["win_pending"])
    tgt = s76d["target"]
    check("D1.s76d_target_child", tgt["s6_child_hex"] == row76, tgt["s6_child_hex"])
    check("D1.s76d_target_parent_is_claimant",
          tgt["s5_hex"] in next(r["partial_parents"] for r in special if r["hex"] == row76),
          tgt["s5_hex"])
    tot = s76d["sweep_totals"]
    w76 = wrows[row76]
    check("D2.s76d_totals",
          tot["candidates"] == int(w76["own_candidates_s6_s7_edge_cost"]) == 76 and
          tot["win7_d10_bits"] == [19, 49] and
          tot["refuted_d10_count"] == int(w76["engine_refuted_d10"]) == 74 and
          tot["capped_count"] == 0 and int(w76["engine_win7_d10"]) == 2,
          f"win bits {tot['win7_d10_bits']}")
    c76 = int(row76, 16)
    ok_d2b = all(int(tot["win_roots"][str(b)], 16) == (c76 | (1 << b)) for b in [19, 49])
    check("D2b.s76d_win_roots_bit_arithmetic", ok_d2b,
          "root == child | 1<<bit (121-bit exact)")
    certs = c76d["certificates"]
    check("D3.c76d_manifest",
          len(certs) == 2 and
          {c["bit"] for c in certs} == {19, 49} and
          all(c["verdict"] == "WIN7" for c in certs) and
          all(c["root_hex"] == tot["win_roots"][str(c["bit"])] for c in certs) and
          all(c["published_cert"]["git_blob_sha"] for c in certs),
          f"{len(certs)} certificates")
    ok_d3b = True
    for c in certs:
        root = int(c["root_hex"], 16)
        ok_d3b = ok_d3b and canon(root) == root and c["d4_canonical_hex"] == c["root_hex"]
    check("D3b.c76d_roots_are_d4_canonical", ok_d3b)
    check("D4.v76d77e_verdict", v76d77e["verdict"] == "VERIFICATION PASSED",
          v76d77e["verdict"])
    check("D4.v76d77e_cost76d_checks_all_true", all_bools_true(v76d77e["cost76d"]))
    check("D4.v76d77e_cost77e_checks_all_true", all_bools_true(v76d77e["cost77e"]))
    agg = s77e["aggregate"]
    w77 = wrows[row77]
    check("D5.s77e_child_and_parent",
          s77e["s6_child"] == row77 and
          s77e["s5"] in next(r["partial_parents"] for r in special if r["hex"] == row77),
          (s77e["s6_child"], s77e["s5"]))
    check("D5.s77e_totals",
          agg["candidates"] == int(w77["own_candidates_s6_s7_edge_cost"]) == 77 and
          agg["win7_d10_bits"] == [37, 69] and
          agg["refuted_d10"] == int(w77["engine_refuted_d10"]) == 75 and
          agg["capped"] == 0 and int(w77["engine_win7_d10"]) == 2,
          f"win bits {agg['win7_d10_bits']}")
    c77 = int(row77, 16)
    ok_d5b = all(int(s77e["certificates"][f"bit{b}"]["root_hex"], 16) == (c77 | (1 << b))
                 for b in [37, 69])
    check("D5b.s77e_win_roots_bit_arithmetic", ok_d5b)
    check("D5c.s77e_fold_pending", "PENDING" in s77e["fold_status"])
    ok_d6 = True
    for hx, legal, refuted in ((row76, 76, 74), (row77, 77, 75)):
        st = scan["targets"][hx]
        ok_d6 = ok_d6 and st["legal_count"] == legal
        ok_d6 = ok_d6 and st["engine"]["REFUTED-D10"] == refuted
        ok_d6 = ok_d6 and st["engine"]["WIN7-D10"] == 2
        ok_d6 = ok_d6 and st["open"] == 0 and not st["transferred"]["REFUTED-D10"]
    check("D6.scan_targets_match", ok_d6)
    check("D7.pending_open_after_zero",
          wrows[row76]["open_candidates_after_transfers"] == "0" and
          wrows[row77]["open_candidates_after_transfers"] == "0")

    # ---- E: transfer_partial (2 rows) --------------------------------
    row76c = "00000000010000809002000001000000"
    row69a = "00000000000000801222000000800000"
    check("E0.transfer_hexes", sorted(by_cat["transfer_partial"]) == sorted([row76c, row69a]),
          by_cat["transfer_partial"])
    st76c = scan["targets"][row76c]
    st69a = scan["targets"][row69a]
    tr76c = st76c["transferred"]["REFUTED-D10"]
    tr69a = st69a["transferred"]["REFUTED-D10"]
    check("E1.transfer_counts",
          len(tr76c) == int(wrows[row76c]["transferred_refuted_d10"]) == 15 and
          len(tr69a) == int(wrows[row69a]["transferred_refuted_d10"]) == 3,
          (len(tr76c), len(tr69a)))
    ok_e1b = all(v["kind"] == "engine"
                 for tr in (tr76c, tr69a) for e in tr for v in e["via"])
    check("E1b.all_via_kind_engine", ok_e1b)
    ok_e2 = True
    n_via = 0
    for hx, trs in ((row76c, tr76c), (row69a, tr69a)):
        m = int(hx, 16)
        for e in trs:
            target_canon = canon(m | (1 << e["bit"]))
            for v in e["via"]:
                n_via += 1
                via_root = int(v["child"], 16) | (1 << v["bit"])
                if canon(via_root) != target_canon:
                    ok_e2 = False
    check("E2.canon_of_extension_equals_via_root", ok_e2,
          f"{n_via} via entries: canon(row|1<<b) == canon(via_child|1<<via_bit)")
    ok_e3 = (int(wrows[row76c]["open_candidates_after_transfers"]) == 61 ==
             76 - 15 and
             int(wrows[row69a]["open_candidates_after_transfers"]) == 66 ==
             69 - 3 and
             st76c["open"] == 61 and st69a["open"] == 66 and
             wrows[row76c]["engine_win7_d10"] == "0" and
             wrows[row69a]["engine_win7_d10"] == "0")
    check("E3.open_arithmetic", ok_e3)
    m76c = census19["new_verdict_maps"]["cost76c"]
    check("E4.census19_76c_map_child", m76c["child"] == row76c, m76c["child"])
    transferred_bits = sorted(e["bit"] for e in tr76c)
    refuted_later = set(m76c["refuted_d10_bits"])
    win_later = set(m76c["win7_d10_bits"])
    check("E4.transferred_bits_all_confirmed_refuted",
          all(b in refuted_later for b in transferred_bits),
          f"{sum(1 for b in transferred_bits if b in refuted_later)}/15")
    check("E4.win_bits_disjoint_from_transfers",
          not (win_later & set(transferred_bits)) and win_later == {61, 99},
          sorted(win_later))
    check("E4.census19_76c_totals",
          len(m76c["refuted_d10_bits"]) == 74 and len(m76c["win7_d10_bits"]) == 2 and
          m76c["capped"] == 0 and len(m76c["refuted_d10_bits"]) + len(m76c["win7_d10_bits"]) == 76)
    txt19 = Path(PINS["census19"][0]).read_text()
    check("E5.row69a_absent_from_census19", row69a not in txt19)
    check("E5b.pending_rows_absent_from_census19",
          row76 not in txt19 and row77 not in txt19)
    check("E6.scanverify_verdict", scanverify["verdict"] == "VERIFICATION PASSED")
    check("E6.scanverify_transfer_canon_count",
          scanverify["extra_checks"]["x1_transfer_roots_canonically_verified"] == 115
          == scan["transfers"]["total"] and not scanverify["problems"])

    # ---- summary ------------------------------------------------------
    rows_out = []
    for r in sorted(special, key=lambda r: (r["category"], r["hex"])):
        w = wrows[r["hex"]]
        entry = {
            "hex": r["hex"],
            "category": r["category"],
            "cost": r["cost"],
            "partial_parents": r["partial_parents"],
            "worklist": {
                "own_candidates": int(w["own_candidates_s6_s7_edge_cost"]),
                "engine_win7_d10": int(w["engine_win7_d10"]),
                "engine_refuted_d10": int(w["engine_refuted_d10"]),
                "transferred_refuted_d10": int(w["transferred_refuted_d10"]),
                "open_after_transfers": int(w["open_candidates_after_transfers"]),
            },
        }
        if r["category"] == "win_pending":
            entry["win_bits"] = ([19, 49] if r["hex"] == row76 else [37, 69])
            entry["win_root_hexes"] = ([tot["win_roots"]["19"], tot["win_roots"]["49"]]
                                       if r["hex"] == row76 else
                                       [s77e["certificates"]["bit37"]["root_hex"],
                                        s77e["certificates"]["bit69"]["root_hex"]])
            entry["fold_status_at_record"] = "PENDING (cost-76d/77e records)"
        elif r["category"] == "win_receipt_scheduled":
            entry["closed_by"] = "cost-65j receipt fold, head 1410 -> 1419"
        elif r["category"] == "transfer_partial":
            if r["hex"] == row76c:
                entry["transferred_bits"] = transferred_bits
                entry["later_direct_sweep"] = {
                    "source": "census v19 cost76c verdict map (v17 raw batches)",
                    "win7_d10_bits": sorted(win_later),
                    "transferred_bits_confirmed_refuted": 15,
                    "conflicts": 0,
                    "fold": m76c["fold"],
                }
            else:
                entry["transferred_bits"] = sorted(e["bit"] for e in tr69a)
                entry["later_direct_sweep"] = None
        rows_out.append(entry)

    summary = {
        "special_rows_total": 13,
        "win_receipt_scheduled": 9,
        "win_pending": 2,
        "transfer_partial": 2,
        "engine_win7_roots_pending_fold": 4,
        "engine_win7_bits_pending_fold": [19, 37, 49, 69],
        "win_pending_rows_serve_partial_parents": sorted(
            set(p for r in special if r["category"] == "win_pending"
                for p in r["partial_parents"])),
        "scheduled_rows_closed_at_head": "1410 -> 1419 (cost-65j fold, 9 rows / 635 own candidates)",
        "transfer_predictions_confirmed_by_later_sweep": "76c row: 15/15 REFUTED-D10, 0 conflicts",
        "distinct_partial_parents_touched": len(
            set(p for r in special for p in r["partial_parents"])),
    }

    emit(checks, {
        "schema": "nonsterile-special-rows-downstream-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long-term lane, autonomous session (standard 11x11 weak-resolution)",
        "title": ("downstream cross-verification of the 13 special non-STERILE candidate "
                  "rows of the 57 partial-STERILE head-1410 S5 parents (9 cost-65j fold "
                  "closures, 2 cost-76d/77e WIN7 receipt rows, 2 transfer_partial rows)"),
        "inputs": {k: {"git_blob_sha1": v[1]} for k, v in PINS.items()},
        "method": ("independent cross-file consistency verification over pinned published "
                   "records; exact 121-bit one-bit extension arithmetic; third-implementation "
                   "D4 canonicalisation for every transfer via entry; no engine, no float"),
        "checks": checks,
        "all_checks_pass": all(c["pass"] for c in checks),
        "rows": rows_out,
        "summary": summary,
        "interpretation_guard": ("this audit verifies bookkeeping and record consistency only; "
                                 "WIN7 certificates prove individual 7-stone roots; REFUTED-D10 "
                                 "is not a LOSS proof; STERILE is not a LOSS proof; folds and "
                                 "sweeps remain sweep-lane jurisdiction; non-STERILE remains "
                                 "only a necessary condition for depth-10 receipt cover"),
        "trust_boundary": ("engine depth-10 verdict soundness underlying the pinned sweep "
                           "records, identical to all published lane verdicts; the cost-65j "
                           "and cost-76d/77e records carry their own published verifications "
                           "which are quoted, not re-run"),
        "unknown_status": ("11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} "
                           "and classes 1/2/4 all remain UNKNOWN; REFUTED-D10 is not a LOSS "
                           "proof; STERILE is not a LOSS proof"),
    })


def emit(checks, payload):
    if payload is None:
        payload = {"schema": "nonsterile-special-rows-downstream-20261118-v1",
                   "checks": checks, "all_checks_pass": all(c["pass"] for c in checks)}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=1, sort_keys=False) + "\n")
    failed = [c for c in checks if not c["pass"]]
    print(f"checks: {len(checks)}  pass: {len(checks) - len(failed)}  fail: {len(failed)}")
    for c in failed:
        print("FAIL:", c["check"], c["detail"])
    print("all_checks_pass:", all(c["pass"] for c in checks))


if __name__ == "__main__":
    main()
