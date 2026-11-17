#!/usr/bin/env python3
"""Receipt-channel closure-distance audit of the K0865 effective-worklist
rank-1 partial-STERILE S5 parent (2026-11-18).

Parent P = 00000000000000801202000040000000 (class 2) is the rank-1 entry of
the K0865 effective worklist (effective_cost 229, effective_remaining 3) and
one of the 57 partial-STERILE (cross_cover_required) parents. The companion
enumeration (commit e7743ed4) and its follow-ups showed that all three of
its non-STERILE remaining rows are among the 13 special rows of the head-1410
worklist. This audit makes that observation exact and verifies, from pinned
published records only, that P's receipt channel needs no further sweep work
on its own remaining rows:

  - its 5 remaining rows are re-derived by an independent orbit join from the
    raw worklist and match the K0865 census entry field by field;
  - the 2 STERILE rows (cost 64 / 71) have every own candidate REFUTED-D10,
    so by K0863 no depth-10 WIN7 receipt root can ever cover them;
  - the 3 non-STERILE rows are fully determined by published sweeps:
    cost-76d row: 2 WIN7-D10 (bits 19/49) + 74 REFUTED-D10 + 0 capped,
    cost-77e row: 2 WIN7-D10 (bits 37/69) + 75 REFUTED-D10 + 0 capped,
    cost-76c row: 2 WIN7-D10 (bits 61/99) + 74 REFUTED-D10 + 0 capped
                  (census v19 verdict map; 15/15 head-1410 transfer
                  predictions confirmed by that direct sweep);
  - all six WIN root hexes are re-derived exactly as child | 1<<bit (121-bit
    mask arithmetic; the cost-76c canonical root forms are derived here and
    labelled as derived, not as published values);
  - the three receipt folds are PENDING in every pinned record that speaks to
    them (fold application is sweep-lane jurisdiction; this audit folds
    nothing).

No engine is run. No closure, receipt or verdict claim is made beyond the
pinned published records. A parent is not a position value: parent closure
bookkeeping is manifest work, and this audit states only that no further
sweep work is pending on P's own remaining rows at head 1410 per the pinned
records.

Inputs (all git-blob-pinned, all published on main):
  head-1410 remaining S6 worklist CSV          2fee1d07...
  K0865 receipt-unclosability census           9c251da3...
  theorem-applicability scan output            24f214e6...
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

PARENT = "00000000000000801202000040000000"
ROW_76C = "00000000010000809002000001000000"
ROW_76D = "00000000040000003800080008000000"
ROW_77E = "00000000040000809002000000004000"
STERILE_1 = "00000000000000801282000040000000"
STERILE_2 = "00000000000000801202000040000400"

WORKLIST = EXP / "n11-class2-lane-closability-ranking-20261116" / "output" / "class-frontier-remaining-s6-worklist-1410-20261116.csv"
CENSUS = EXP / "n11-head1410-receipt-unclosability-census-20261116" / "output" / "n11-head1410-receipt-unclosability-census-20261116.json"
SCAN = EXP / "n11-class2-lane-sterile-unclosability-20261116" / "output" / "theorem-applicability-scan-20261116.json"
S76D = LANE / "class2-lane-cost76d-sweep-audit-20261116.json"
C76D = LANE / "class2-lane-cost76d-win7-certificates-20261116.json"
V76D77E = LANE / "class2-lane-cost76d-77e-second-independent-verification-20261116.json"
S77E = LANE / "class2-lane-cost77e-sweep-20261116.json"
CENSUS19 = LANE / "class2-lane-next-target-presweep-1473-v19-20261118.json"
PRIOR = HERE / "output" / "n11-head1410-partial-parent-nonsterile-children-20261118.json"
OUT = HERE / "output" / "rank1-parent-receipt-channel-20261118.json"

PINS = {
    "worklist": (str(WORKLIST), "2fee1d0718547a62e346d35f5858d7913e37c097"),
    "census": (str(CENSUS), "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"),
    "scan": (str(SCAN), "24f214e6a9dd721ef95ac97d6b84cf34af33b14b"),
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

    census = json.loads(Path(PINS["census"][0]).read_text())
    scan = json.loads(Path(PINS["scan"][0]).read_text())
    s76d = json.loads(Path(PINS["s76d"][0]).read_text())
    c76d = json.loads(Path(PINS["c76d"][0]).read_text())
    v76d77e = json.loads(Path(PINS["v76d77e"][0]).read_text())
    s77e = json.loads(Path(PINS["s77e"][0]).read_text())
    census19 = json.loads(Path(PINS["census19"][0]).read_text())
    prior = json.loads(Path(PINS["prior"][0]).read_text())

    with Path(PINS["worklist"][0]).open() as fh:
        wrows = {r["s6_canonical_hex"]: r for r in csv.DictReader(fh)}

    # ---- B: K0865 census entry for P ---------------------------------
    entry = next(e for e in census["open_s5_census"] if e["hex"] == PARENT)
    check("B.census_entry", entry["classes"] == 2 and
          entry["classification"] == "partial_sterile" and
          entry["d4_canon"] == PARENT and
          entry["remaining_s6_orbits"] == 5 and
          entry["sterile_refs_count"] == 2 and
          entry["effective_remaining"] == 3 and
          entry["effective_cost"] == 229 and
          entry["remaining_s7_edge_cost"] == 364 and
          entry["sterile_cost"] == 135 and
          entry["effective_cost"] == entry["remaining_s7_edge_cost"] - entry["sterile_cost"] and
          entry["pending_65j_covered_refs"] == 0,
          f"effCost {entry['effective_cost']} / effRem {entry['effective_remaining']}")
    check("B.census_sterile_refs",
          sorted(r["hex"] for r in entry["sterile_refs"]) == sorted([STERILE_1, STERILE_2]) and
          sorted(r["cost"] for r in entry["sterile_refs"]) == [64, 71])
    check("B.rank1_effective_worklist",
          census["effective_worklist_top16"][0]["hex"] == PARENT and
          census["effective_worklist_top16"][0]["effective_cost"] == 229)
    pentry = next(e for e in prior["parents_by_min_child_cost"] if e["hex"] == PARENT)
    check("B.prior_enumeration_entry",
          pentry["nonsterile_count"] == 3 and pentry["min_child_cost"] == 76 and
          pentry["min_child_hex"] == ROW_76C and pentry["sterile_refs_count"] == 2,
          f"nonsterile {pentry['nonsterile_count']} / min {pentry['min_child_cost']}")

    # ---- C: independent orbit join from the raw worklist --------------
    pm = int(PARENT, 16)
    imgs = [t(pm, r) for r in range(8)]
    related = [h for h, m in ((h, int(h, 16)) for h in wrows)
               if any(im & ~m == 0 for im in imgs)]
    check("C.join_rows", len(related) == 5 and
          sorted(related) == sorted([STERILE_1, STERILE_2, ROW_76C, ROW_76D, ROW_77E]),
          related)
    check("C.join_matches_census", len(related) == entry["remaining_s6_orbits"])
    check("C.nonsterile_rows_are_special",
          sorted(h for h in related if wrows[h]["category"] != "sterile") ==
          sorted([ROW_76C, ROW_76D, ROW_77E]))
    ok_c2 = True
    for h in related:
        w = wrows[h]
        ok_c2 = ok_c2 and int(w["own_candidates_s6_s7_edge_cost"]) in (64, 71, 76, 76, 77)
    check("C.row_costs", ok_c2)

    # ---- D: the three non-STERILE rows are fully determined -----------
    # D1 cost-76d row
    w76d = wrows[ROW_76D]
    tot = s76d["sweep_totals"]
    check("D1.s76d_fully_determined",
          tot["candidates"] == 76 and tot["win7_d10_bits"] == [19, 49] and
          tot["refuted_d10_count"] == 74 and tot["capped_count"] == 0 and
          2 + 74 == 76 and
          int(w76d["engine_win7_d10"]) == 2 and
          int(w76d["engine_refuted_d10"]) == 74 and
          w76d["category"] == "win_pending",
          "2 WIN + 74 REFUTED + 0 capped == 76/76")
    c76 = int(ROW_76D, 16)
    roots76d = {b: format(c76 | (1 << b), "032x") for b in [19, 49]}
    check("D1b.s76d_win_roots_bit_arithmetic",
          all(int(tot["win_roots"][str(b)], 16) == c76 | (1 << b) for b in [19, 49]),
          [tot["win_roots"][str(b)] for b in [19, 49]])
    check("D1c.s76d_certs_published",
          len(c76d["certificates"]) == 2 and
          {c["bit"] for c in c76d["certificates"]} == {19, 49} and
          all(c["published_cert"]["git_blob_sha"] for c in c76d["certificates"]))
    check("D1d.s76d_second_verification",
          v76d77e["verdict"] == "VERIFICATION PASSED" and
          v76d77e["cost76d"]["claim_completion_win_bits"] is True)
    # D2 cost-77e row
    w77e = wrows[ROW_77E]
    agg = s77e["aggregate"]
    check("D2.s77e_fully_determined",
          agg["candidates"] == 77 and agg["win7_d10_bits"] == [37, 69] and
          agg["refuted_d10"] == 75 and agg["capped"] == 0 and
          2 + 75 == 77 and
          int(w77e["engine_win7_d10"]) == 2 and
          int(w77e["engine_refuted_d10"]) == 75 and
          w77e["category"] == "win_pending",
          "2 WIN + 75 REFUTED + 0 capped == 77/77")
    c77 = int(ROW_77E, 16)
    check("D2b.s77e_win_roots_bit_arithmetic",
          all(int(s77e["certificates"][f"bit{b}"]["root_hex"], 16) == c77 | (1 << b)
              for b in [37, 69]))
    # D3 cost-76c row (later direct sweep in census v19)
    w76c = wrows[ROW_76C]
    m76c = census19["new_verdict_maps"]["cost76c"]
    check("D3.s76c_fully_determined",
          m76c["child"] == ROW_76C and m76c["bits"] == 76 and
          m76c["win7_d10_bits"] == [61, 99] and
          len(m76c["refuted_d10_bits"]) == 74 and m76c["capped"] == 0 and
          2 + 74 == 76 and w76c["category"] == "transfer_partial",
          "2 WIN + 74 REFUTED + 0 capped == 76/76 (census v19 map)")
    c76c = int(ROW_76C, 16)
    derived_roots_76c = {b: format(canon(c76c | (1 << b)), "032x") for b in [61, 99]}
    check("D3b.s76c_win_roots_derived_canonical",
          all(len(h) == 32 and bin(int(h, 16)).count("1") == 7
              for h in derived_roots_76c.values()),
          "derived canon forms (labelled derived, not published values)")
    st76c = scan["targets"][ROW_76C]
    transferred_bits = sorted(e["bit"] for e in st76c["transferred"]["REFUTED-D10"])
    check("D3c.s76c_transfer_predictions_confirmed",
          all(b in set(m76c["refuted_d10_bits"]) for b in transferred_bits) and
          len(transferred_bits) == 15 and
          not (set(m76c["win7_d10_bits"]) & set(transferred_bits)),
          "15/15 confirmed REFUTED-D10 by the later direct sweep, 0 conflicts")
    # D4 aggregate: no unswept non-STERILE row remains for P
    check("D4.zero_unswept_nonsterile_rows",
          all(wrows[h]["category"] != "unswept" for h in related if
              wrows[h]["category"] != "sterile") and
          prior["totals"]["distinct_nonsterile_rows"] == 3555)

    # ---- E: the two STERILE rows are D10-unclosable -------------------
    sterile_set = {r["child"] for r in scan["sterile_rows_detected"]}
    ok_e = True
    for h in (STERILE_1, STERILE_2):
        w = wrows[h]
        own = int(w["own_candidates_s6_s7_edge_cost"])
        ok_e = ok_e and w["category"] == "sterile"
        ok_e = ok_e and int(w["engine_refuted_d10"]) == own
        ok_e = ok_e and int(w["engine_win7_d10"]) == 0
        ok_e = ok_e and int(w["open_candidates_after_transfers"]) == 0
        ok_e = ok_e and h in sterile_set
    check("E.sterile_rows_all_candidates_refuted", ok_e,
          "64/64 and 71/71 REFUTED-D10, 0 WIN, 0 capped -> K0863 unclosable")

    # ---- F: fold states in the pinned records ------------------------
    check("F.folds_pending",
          "PENDING" in s77e["fold_status"] and
          "NOT yet been folded" in c76d["frontier_impact"] and
          "PENDING" in m76c["fold"] and
          "PENDING" in v76d77e["cross_lane_facts"]["fold_status_at_record_time"],
          "76c / 76d / 77e receipt folds all PENDING at the pinned records")

    # ---- summary ------------------------------------------------------
    rows_out = []
    for h in sorted(related):
        w = wrows[h]
        entry_out = {
            "hex": h,
            "category": w["category"],
            "cost": int(w["own_candidates_s6_s7_edge_cost"]),
            "engine_win7_d10": int(w["engine_win7_d10"]),
            "engine_refuted_d10": int(w["engine_refuted_d10"]),
            "transferred_refuted_d10": int(w["transferred_refuted_d10"]),
            "open_after_transfers": int(w["open_candidates_after_transfers"]),
        }
        if h == ROW_76D:
            entry_out["win_bits"] = [19, 49]
            entry_out["win_root_hexes"] = [tot["win_roots"]["19"], tot["win_roots"]["49"]]
            entry_out["determination"] = "cost-76d sweep (published, second-verified)"
            entry_out["fold"] = "PENDING (cost-76d receipt fold onto head 1405)"
        elif h == ROW_77E:
            entry_out["win_bits"] = [37, 69]
            entry_out["win_root_hexes"] = [s77e["certificates"]["bit37"]["root_hex"],
                                           s77e["certificates"]["bit69"]["root_hex"]]
            entry_out["determination"] = "cost-77e sweep (published, dual-verified)"
            entry_out["fold"] = "PENDING (cost-77e receipt fold onto head 1405)"
        elif h == ROW_76C:
            entry_out["win_bits"] = [61, 99]
            entry_out["win_root_canon_hexes_derived"] = [derived_roots_76c[61],
                                                         derived_roots_76c[99]]
            entry_out["determination"] = ("census v19 cost76c verdict map "
                                          "(direct v17 sweep; 15/15 head-1410 "
                                          "transfer predictions confirmed)")
            entry_out["fold"] = m76c["fold"]
        else:
            entry_out["determination"] = "STERILE: all own candidates REFUTED-D10 (K0863 unclosable)"
        rows_out.append(entry_out)

    summary = {
        "parent": PARENT,
        "classes": 2,
        "k0865_classification": "partial_sterile (cross_cover_required)",
        "effective_worklist_rank": 1,
        "effective_cost": 229,
        "remaining_rows": 5,
        "sterile_rows": 2,
        "nonsterile_rows": 3,
        "nonsterile_rows_unswept": 0,
        "nonsterile_rows_fully_determined": 3,
        "win7_d10_roots_available": 6,
        "win7_d10_bits": [19, 37, 49, 61, 69, 99],
        "certificates_published_and_verified": [19, 37, 49, 69],
        "fold_pending_bands": ["cost76c", "cost76d", "cost77e"],
        "receipt_channel_sweep_work_remaining_on_own_rows": 0,
        "note": ("the parent's non-STERILE receipt channel is fully determined "
                 "by published sweeps; what remains on this channel is the three "
                 "pending receipt folds (sweep-lane jurisdiction), not sweep work; "
                 "the two STERILE rows can never be covered by a D10 WIN7 "
                 "receipt (K0863); no parent-closure claim is made here"),
    }

    emit(checks, {
        "schema": "rank1-parent-receipt-channel-20261118-v1",
        "date": "2026-11-18",
        "lane": "n11 long-term lane, autonomous session (standard 11x11 weak-resolution)",
        "title": ("receipt-channel closure-distance audit of the K0865 effective-worklist "
                  "rank-1 partial-STERILE S5 parent 00000000000000801202000040000000: "
                  "all 3 non-STERILE remaining rows fully determined by published "
                  "sweeps (6 WIN7-D10 roots), 2 STERILE rows K0863-unclosable, "
                  "remaining work on this channel is the 3 pending receipt folds"),
        "inputs": {k: {"git_blob_sha1": v[1]} for k, v in PINS.items()},
        "method": ("independent orbit join (exists sigma in D4 with sigma(P) subset R, "
                   "121-bit masks, 8 transforms) from the raw worklist; exact one-bit "
                   "root arithmetic; third-implementation D4 canonicalisation for the "
                   "derived cost-76c root forms; no engine, no float, no fold"),
        "checks": checks,
        "all_checks_pass": all(c["pass"] for c in checks),
        "rows": rows_out,
        "summary": summary,
        "interpretation_guard": ("fully determined rows and WIN7 certificates prove only "
                                 "individual 7-stone roots and row-level bookkeeping; a "
                                 "parent is not a position value and parent closure is "
                                 "manifest work; REFUTED-D10 is not a LOSS proof; STERILE "
                                 "is not a LOSS proof; folds remain sweep-lane "
                                 "jurisdiction and none is applied here"),
        "trust_boundary": ("engine depth-10 verdict soundness underlying the pinned sweep "
                           "records, identical to all published lane verdicts; the "
                           "cost-76c determination is the census v19 verdict map's "
                           "published record"),
        "unknown_status": ("11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} "
                           "and classes 1/2/4 all remain UNKNOWN; REFUTED-D10 is not a "
                           "LOSS proof; STERILE is not a LOSS proof"),
    })


def emit(checks, payload):
    if payload is None:
        payload = {"schema": "rank1-parent-receipt-channel-20261118-v1",
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
