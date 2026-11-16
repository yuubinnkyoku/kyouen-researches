#!/usr/bin/env python3
"""Closability re-ranking of the whole head-1410 class-2-lane frontier under the
K0863 STERILE-row depth-10 unclosability theorem.

This script reproduces the published cost-60c fold chain (which internally
reproduces the whole reconciliation chain byte-identically) to the canonical
head 1410/174/6438/509109/4711/373023, then classifies every one of the 6,438
unique remaining S6 rows (12,274 parent-incidences over the 174 remaining S5
orbits) and every one of the 174 remaining S5 orbits by closability:

row categories (pre-registered, priority order):
  win_receipt_scheduled - the row is in the pending cost-65j pre-fold cover
                          map union (17 WIN7-D10 receipts, 34-row union) and
                          still remains at head 1410; its closure does not
                          need its own sweep (the cost-65j fold is scheduled)
  win_pending           - the row has engine WIN7-D10 receipts (swept) whose
                          receipt fold has not landed yet (cost-76d/77e)
  sterile               - every own candidate is determined REFUTED-D10
                          (engine + theorem transfer), 0 WIN7-D10, 0 capped
                          (the K0863 census; these rows can never be covered
                          by any WIN7-D10 receipt root)
  transfer_partial      - some own candidates are pre-determined REFUTED-D10
                          by the canonical verdict-cache transfers, rest open
  unswept               - no own candidate determined yet

S5 orbit categories:
  fully_sterile        - every remaining row of the orbit is sterile
  cross_cover_required - at least one sterile and at least one non-sterile
  own_closable         - no sterile rows (closure by own-row sweep work only)

Inputs (all blob-pinned, all published on main):
  - the published cost-60c fold chain script (re-run via runpy; it re-asserts
    the head-1410 output blobs 239a6cf4.../a01cfd53.../08aaf318... itself)
  - theorem-applicability scan output (engine verdict tallies per target,
    115 transfers, 35-row STERILE census)
  - cost-65j pre-fold cover map (17 receipts, 34-row union)
  - STERILE-rows neighbor analysis (route-exhaustion context for 65k/70j/74h)

Method notes:
  - the D4 canonical form and the legal-candidate enumeration are taken from
    the published theorem_applicability_scan_20261116.py implementation
    (stdlib-only, second-verified); the enumeration is additionally
    re-implemented here with exact integer circumcircle/line arithmetic and
    cross-checked bit-exact against the scan implementation on a fixed
    sample, then used for the all-rows invariant check
    "s6-s7 edge cost == own legal candidate count" (0 mismatches expected
    over all 6,438 rows, i.e. sum_remaining_cost 509,109 is exactly the
    number of remaining own-sweep candidates)
  - the scan's D4 canonical form is checked against the chain's canonical
    form on all 12,274 parent-incidences

Outputs (deterministic; two runs byte-identical):
  - output/class-frontier-closability-ranking-1410-20261116.json
  - output/class-frontier-remaining-s6-worklist-1410-20261116.csv (6,438 rows)
  - output/class-frontier-s5-closability-after-cost60c-20261116.csv (174 rows)

Pre-registered expectations (from the original 2026-11-16 derivation, all
re-asserted by this re-derivation):
  row categories: unswept 6,390 / sterile 35 / win_receipt_scheduled 9 /
    transfer_partial 2 (cost-76c child 76/15/61, cost-69a child 69/3/66) /
    win_pending 2 (cost-76d/77e children, 2 WIN7-D10 each)
  S5 categories: own_closable 114 / cross_cover_required 57 / fully_sterile 3
    (best coverable class-2 3/209 rows 65k/70j/74h, audit-blocked class-2
    10/698, best class-4 18/1460)
  STERILE blocking leverage: 35 rows block 91 parent-incidences over 60
    distinct S5 orbits (22 rows x 3 orbits, 12 x 2, 1 x 1)
  remaining sweep work after theorem transfers, swept-determined candidates
    and the pending cost-65j reservations: 505,675 candidates
  best own-closable class-2 target 00000000000000403800000008000000 (24/1704);
    best any-class 00000000000000821082000000000000 (18/1238, class-1);
    best class-4 own-closable 00000000000000003800002000800000 (60/4216)
  no cost-65j receipt covers a STERILE row (K0863's strong negative
    prediction)

11x11 empty board / two-stone root {49,60} / S2 {59,60} / class 1 / class 2 /
class 4 remain UNKNOWN; this is closability bookkeeping only. REFUTED-D10 is
not a LOSS proof and STERILE rows are open (their game-theoretic values are
unknown).
"""
import csv
import hashlib
import importlib.util
import json
import runpy
import time
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
EXP = Path(__file__).resolve().parents[2]
S2 = EXP / "n11-s2-5960-ms5-s7-reuse-20261113"
STERY = EXP / "n11-class2-lane-sterile-unclosability-20261116"

FOLD_SCRIPT = S2 / "scripts" / "recompute_frontier_cost60c_receipts_20261116.py"
FOLD_SCRIPT_BLOB = "148acc7f4ecee6b487a010dfeb1959444f472ee6"
HEAD_JSON = "class-frontier-cost60c-receipts-recompute-20261116.json"
HEAD_JSON_BLOB = "239a6cf432e53713514d583e3682e1bef6075968"
HEAD_RANKING_BLOB = "a01cfd5340fa89c0eaf834dcb96000f9b04d20ae"
HEAD_TOPCAND_BLOB = "08aaf31892680668e7e292848235a154eb746407"
SCAN_JSON = STERY / "output" / "theorem-applicability-scan-20261116.json"
SCAN_BLOB = "24f214e6a9dd721ef95ac97d6b84cf34af33b14b"
SCAN_SCRIPT = STERY / "theorem_applicability_scan_20261116.py"
MAP65J = S2 / "output" / "class2-lane-cost65j-win-marginals-20261116.json"
MAP65J_BLOB = "d6d20e52c6b5af8f268222bfc9c87d6ac77c655d"
NEIGH = S2 / "output" / "class2-lane-sterile-rows-neighbor-analysis-20261116.json"
NEIGH_BLOB = "031b8d62d7bfd222772588d9dfce46c35cda9c61"

BEST_COVERABLE_C2 = "00000000000000801202000000200000"  # 3/209, rows 65k/70j/74h
SECOND_COVERABLE_C2 = "00000000000000801202000040000000"  # 5/364
AUDIT_BLOCKED = "00000000000000809082000000000000"  # 10/698
BEST_CLASS4 = "00000000020000003800000080000000"  # 18/1460
ROW_65K = "00000000020000801202000000200000"
ROW_70J = "00000000000000801282000000200000"
ROW_74H = "00000000000000889002000000000800"
ROW_76C = "00000000010000809002000001000000"  # cost-76c child
ROW_69A = "00000000000000801222000000800000"  # cost-69a child
ROW_76D = "00000000040000003800080008000000"  # cost-76d child
ROW_77E = "00000000040000809002000000004000"  # cost-77e child
ROW_65J = "00000000000000809102000080000000"  # cost-65j/65f child

CATEGORY_ORDER = ["sterile", "transfer_partial", "win_pending",
                  "win_receipt_scheduled", "unswept"]


def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), len(data)


def main():
    t0 = time.time()

    # ---------- pins ----------
    for path, blob, name in (
            (FOLD_SCRIPT, FOLD_SCRIPT_BLOB, "fold chain script"),
            (SCAN_JSON, SCAN_BLOB, "theorem-applicability scan output"),
            (MAP65J, MAP65J_BLOB, "cost-65j pre-fold cover map"),
            (NEIGH, NEIGH_BLOB, "STERILE-rows neighbor analysis")):
        sha, blen = git_blob_sha(path)
        assert sha == blob, (name, sha, blob)
    print(f"CONTROL input blob pins verified: fold chain script "
          f"({FOLD_SCRIPT_BLOB[:8]}...), scan ({SCAN_BLOB[:8]}...), "
          f"cost-65j cover map ({MAP65J_BLOB[:8]}...), neighbor analysis "
          f"({NEIGH_BLOB[:8]}...)")

    # ---------- 1. reproduce the chain head 1410 ----------
    ns = runpy.run_path(str(FOLD_SCRIPT))
    st = ns["st_after"]
    assert (st["solved_s6_in_manifest"], st["remaining_s5_orbits"],
            st["unique_remaining_s6"], st["sum_remaining_cost"],
            st["s6_needed_by_open_classes"],
            st["cost_needed_by_open_classes"]) == \
        (1410, 174, 6438, 509109, 4711, 373023), st
    for name, blob in ((HEAD_JSON, HEAD_JSON_BLOB),
                       ("class-frontier-s5-ranking-after-cost60c-receipts-"
                        "20261116.csv", HEAD_RANKING_BLOB),
                       ("class-frontier-top-candidates-s6-after-cost60c-"
                        "receipts-20261116.csv", HEAD_TOPCAND_BLOB)):
        sha, blen = git_blob_sha(S2 / "output" / name)
        assert sha == blob, name
    rem = ns["rem_after"]
    classes = ns["classes"]
    canon_chain = ns["canon"]
    covers_chain = ns["covers"]
    assert len(rem) == 174 and len(classes) >= 174
    print("CONTROL chain head 1410/174/6438/509109/4711/373023 reproduced "
          "(runpy of the published fold script); the three head-1410 output "
          "blobs re-asserted byte-identical")

    # scan module (geometry from the published, second-verified implementation)
    spec = importlib.util.spec_from_file_location("scanmod", SCAN_SCRIPT)
    scanmod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scanmod)
    scan = json.loads(SCAN_JSON.read_text())
    targets = scan["targets"]
    census = scan["sterile_rows_detected"]
    assert len(targets) == 133 and len(census) == 35

    # ---------- 2. rows, incidences, canon agreement ----------
    row_parents = {}
    row_cost = {}
    for h, rows in rem.items():
        for r in rows:
            row_cost.setdefault(r["s6_hex"], int(r["s6_s7_edge_cost"]))
            row_parents.setdefault(r["s6_hex"], []).append(h)
    assert len(row_cost) == 6438
    incidences = sum(len(v) for v in row_parents.values())
    assert incidences == 12274, incidences
    # canonical-form agreement between the scan implementation and the chain
    canon_pairs = 0
    for h, rows in rem.items():
        for r in rows:
            hx = r["s6_hex"]
            assert scanmod.d4_canon(hx) == format(canon_chain(int(hx, 16)),
                                                   "032x"), hx
            canon_pairs += 1
    assert canon_pairs == 12274
    print(f"CONTROL D4 canonical-form agreement scan-vs-chain: all "
          f"{canon_pairs} parent-incidences match")

    # ---------- 3. legal-candidate enumeration (fast exact re-implementation) --
    _circle_cache = {}

    def circle_cells(a, b, c):
        key = (a, b, c)
        hit = _circle_cache.get(key)
        if hit is not None:
            return hit
        ax, ay = a % 11, a // 11
        bx, by = b % 11, b // 11
        cx, cy = c % 11, c // 11
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        cells = set()
        if d == 0:
            # collinear triple: generalized circle is the line through a,b
            dx, dy = bx - ax, by - ay
            for p in range(121):
                if (p % 11 - ax) * dy == (p // 11 - ay) * dx:
                    cells.add(p)
        else:
            sa = ax * ax + ay * ay
            sb = bx * bx + by * by
            sc = cx * cx + cy * cy
            ux = sa * (by - cy) + sb * (cy - ay) + sc * (ay - by)
            uy = sa * (cx - bx) + sb * (ax - cx) + sc * (bx - ax)
            r2 = (ux - ax * d) ** 2 + (uy - ay * d) ** 2
            for p in range(121):
                px, py = p % 11, p // 11
                if (px * d - ux) ** 2 + (py * d - uy) ** 2 == r2:
                    cells.add(p)
        _circle_cache[key] = cells
        return cells

    def enumerate_legal_fast(hexstr):
        st = scanmod.stones(hexstr)
        stset = set(st)
        forbidden = set()
        n = len(st)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    forbidden |= circle_cells(st[i], st[j], st[k])
        return [p for p in range(121)
                if p not in stset and p not in forbidden]

    # cross-check the fast enumeration against the scan implementation on a
    # fixed sample (first 100 remaining rows in hex order)
    sample = sorted(row_cost)[:100]
    for hx in sample:
        assert enumerate_legal_fast(hx) == scanmod.enumerate_legal(hx), hx
    print("CONTROL fast circumcircle/line enumeration == scan implementation "
          "on the fixed 100-row sample (bit-exact)")

    # ---------- 4. per-row classification ----------
    map65j = json.loads(MAP65J.read_text())
    union65j = set(map65j["covered_manifest_rows_union"])
    assert len(union65j) == 34 and len(map65j["receipts"]) == 17
    scheduled = sorted(h for h in union65j if h in row_cost)
    assert len(scheduled) == 9, scheduled

    rows = {}
    for hx, own in row_cost.items():
        t = targets.get(hx)
        if t is not None:
            assert t["legal_count"] == own, hx
            eng_win = t["engine"]["WIN7-D10"]
            eng_ref = t["engine"]["REFUTED-D10"]
            assert t["engine"]["UNKNOWN-CAPPED"] == 0, hx
            tr = len(t["transferred"]["REFUTED-D10"])
            assert len(t["transferred"]["WIN7-D10"]) == 0, hx
            assert eng_win + eng_ref + tr + t["open"] == own, hx
        else:
            eng_win = eng_ref = tr = 0
        if hx in union65j:
            cat = "win_receipt_scheduled"
        elif eng_win > 0:
            cat = "win_pending"
        elif eng_win == 0 and eng_ref + tr == own:
            cat = "sterile"
        elif tr > 0:
            cat = "transfer_partial"
        else:
            cat = "unswept"
        open_after = 0 if cat == "win_receipt_scheduled" \
            else own - eng_win - eng_ref - tr
        rows[hx] = {
            "s6_hex": hx, "category": cat, "own_candidates": own,
            "open_parents": len(row_parents[hx]),
            "engine_win7_d10": eng_win, "engine_refuted_d10": eng_ref,
            "transferred_refuted_d10": tr,
            "open_candidates_after_transfers": open_after,
        }

    counts = {}
    for r in rows.values():
        counts[r["category"]] = counts.get(r["category"], 0) + 1
    assert counts == {"unswept": 6390, "sterile": 35,
                      "win_receipt_scheduled": 9, "transfer_partial": 2,
                      "win_pending": 2}, counts

    # STERILE census agreement with the scan
    my_sterile = {h for h, r in rows.items() if r["category"] == "sterile"}
    census_remaining = {c["child"] for c in census if c["child"] in rows}
    assert my_sterile == census_remaining, \
        (len(my_sterile), len(census_remaining))
    census_by_child = {c["child"]: c for c in census}
    for h in my_sterile:
        c = census_by_child[h]
        r = rows[h]
        assert (c["engine_refuted"], c["transferred_refuted"]) == \
            (r["engine_refuted_d10"], r["transferred_refuted_d10"]), h
        assert r["engine_win7_d10"] == 0 and \
            r["open_candidates_after_transfers"] == 0, h

    # specific rows
    r = rows[ROW_76C]
    assert (r["category"], r["own_candidates"], r["transferred_refuted_d10"],
            r["open_candidates_after_transfers"]) == \
        ("transfer_partial", 76, 15, 61), r
    r = rows[ROW_69A]
    assert (r["category"], r["own_candidates"], r["transferred_refuted_d10"],
            r["open_candidates_after_transfers"]) == \
        ("transfer_partial", 69, 3, 66), r
    r = rows[ROW_76D]
    assert (r["category"], r["own_candidates"], r["engine_win7_d10"],
            r["open_candidates_after_transfers"]) == \
        ("win_pending", 76, 2, 0), r
    r = rows[ROW_77E]
    assert (r["category"], r["own_candidates"], r["engine_win7_d10"],
            r["open_candidates_after_transfers"]) == \
        ("win_pending", 77, 2, 0), r
    # the cost-65j own row is already closed at head 1410 (by the 65f-era
    # receipts of the reconciliation chain); it is not in the worklist
    assert ROW_65J not in rows
    assert sum(rows[h]["own_candidates"] for h in scheduled) == 635
    print("CONTROL row classification: unswept 6,390 / sterile 35 (== scan "
          "census) / win_receipt_scheduled 9 (cost-65j cover-map union, 635 "
          "own candidates) / transfer_partial 2 (cost-76c 76/15/61, cost-69a "
          "69/3/66) / win_pending 2 (cost-76d/77e, 2 WIN7-D10 each)")

    # ---------- 5. invariants ----------
    mismatches = []
    total_own = 0
    for hx, r in rows.items():
        n = len(enumerate_legal_fast(hx))
        total_own += n
        if n != r["own_candidates"]:
            mismatches.append((hx, n, r["own_candidates"]))
    assert not mismatches, mismatches[:5]
    assert total_own == st["sum_remaining_cost"] == 509109, total_own
    remaining_work = sum(r["open_candidates_after_transfers"]
                         for r in rows.values())
    assert remaining_work == 505675, remaining_work
    print(f"CONTROL invariant: s6-s7 edge cost == own legal candidate count "
          f"on all 6,438 rows (0 mismatches, {total_own} candidates == "
          f"sum_remaining_cost); remaining own-sweep work after transfers, "
          f"swept-determined candidates and the cost-65j reservations: "
          f"{remaining_work}")

    # no cost-65j receipt covers a STERILE row (K0863 strong negative
    # prediction)
    sterile_v = {int(h, 16) for h in my_sterile}
    for bit, rec in map65j["receipts"].items():
        cov = covers_chain(int(rec["root_hex"], 16))
        assert not (cov & sterile_v), (bit, rec["root_hex"])
        assert rec["root_d4_canon"] == \
            format(canon_chain(int(rec["root_hex"], 16)), "032x"), bit
    print("CONTROL no cost-65j receipt covers a STERILE row (all 17 receipt "
          "roots vs the 35-row census; K0863's strong negative prediction "
          "confirmed by the chain covers() function)")

    # ---------- 6. S5 orbit classification ----------
    orbits = {}
    for h, rlist in rem.items():
        cats = [rows[r["s6_hex"]]["category"] for r in rlist]
        n = len(cats)
        nst = cats.count("sterile")
        if nst == n:
            cat = "fully_sterile"
        elif nst > 0:
            cat = "cross_cover_required"
        else:
            cat = "own_closable"
        orbits[h] = {
            "s5_hex": h, "classes": classes.get(h, 0), "category": cat,
            "remaining_s6_orbits": n,
            "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"])
                                           for r in rlist),
            "rows_sterile": nst,
            "rows_win_pending": cats.count("win_pending"),
            "rows_win_receipt_scheduled": cats.count("win_receipt_scheduled"),
            "rows_transfer_partial": cats.count("transfer_partial"),
            "rows_unswept": cats.count("unswept"),
            "own_sweep_candidates_after_transfers":
                sum(rows[r["s6_hex"]]["open_candidates_after_transfers"]
                    for r in rlist),
            "sterile_rows": sorted(r["s6_hex"] for r in rlist
                                   if rows[r["s6_hex"]]["category"] ==
                                   "sterile"),
        }
    ocounts = {}
    for o in orbits.values():
        ocounts[o["category"]] = ocounts.get(o["category"], 0) + 1
    assert ocounts == {"own_closable": 114, "cross_cover_required": 57,
                       "fully_sterile": 3}, ocounts
    fully = {h for h, o in orbits.items() if o["category"] == "fully_sterile"}
    assert fully == {BEST_COVERABLE_C2, AUDIT_BLOCKED, BEST_CLASS4}, fully
    assert orbits[BEST_COVERABLE_C2]["sterile_rows"] == \
        sorted([ROW_65K, ROW_70J, ROW_74H])
    o = orbits[SECOND_COVERABLE_C2]
    assert (o["category"], o["remaining_s6_orbits"],
            o["remaining_s7_edge_cost"], o["rows_sterile"],
            o["rows_win_pending"], o["rows_transfer_partial"],
            o["rows_unswept"], o["rows_win_receipt_scheduled"],
            o["own_sweep_candidates_after_transfers"]) == \
        ("cross_cover_required", 5, 364, 2, 2, 1, 0, 0, 61), o
    print("CONTROL S5 orbit classification: own_closable 114 / "
          "cross_cover_required 57 / fully_sterile 3 (best coverable "
          "class-2 3/209 rows 65k/70j/74h, audit-blocked 10/698, best "
          "class-4 18/1460); second candidate 5/364 is cross_cover_required "
          "(2 STERILE + cost-76d/77e win_pending + cost-76c transfer_partial)")

    # STERILE blocking leverage
    blocked = {}
    for h in my_sterile:
        for p in row_parents[h]:
            blocked.setdefault(p, 0)
            blocked[p] += 1
    per_row_parents = [len(row_parents[h]) for h in my_sterile]
    dist = {}
    for n in per_row_parents:
        dist[n] = dist.get(n, 0) + 1
    assert dist == {3: 22, 2: 12, 1: 1}, dist
    assert sum(per_row_parents) == 91
    assert len(blocked) == 60 == 57 + 3
    print(f"CONTROL STERILE blocking leverage: 35 rows block "
          f"{sum(per_row_parents)} parent-incidences over {len(blocked)} "
          f"distinct S5 orbits (22 rows x 3 orbits, 12 x 2, 1 x 1)")

    # ---------- 7. next targets ----------
    def oc_sorted(bit):
        sel = [o for o in orbits.values()
               if o["category"] == "own_closable" and (bit is None or
                                                      o["classes"] & bit)]
        return sorted(sel, key=lambda o: (o["remaining_s6_orbits"],
                                          o["remaining_s7_edge_cost"],
                                          o["s5_hex"]))

    oc_all = oc_sorted(None)
    oc_c1 = oc_sorted(1)
    oc_c2 = oc_sorted(2)
    oc_c4 = oc_sorted(4)
    assert len(oc_all) == 114
    assert oc_all[0]["s5_hex"] == "00000000000000821082000000000000"
    assert (oc_all[0]["remaining_s6_orbits"],
            oc_all[0]["remaining_s7_edge_cost"],
            oc_all[0]["classes"]) == (18, 1238, 1)
    assert oc_c2[0]["s5_hex"] == "00000000000000403800000008000000"
    assert (oc_c2[0]["remaining_s6_orbits"],
            oc_c2[0]["remaining_s7_edge_cost"]) == (24, 1704)
    assert oc_c4[0]["s5_hex"] == "00000000000000003800002000800000"
    assert (oc_c4[0]["remaining_s6_orbits"],
            oc_c4[0]["remaining_s7_edge_cost"]) == (60, 4216)
    print("CONTROL next targets: best own-closable class-2 "
          "00000000000000403800000008000000 (24/1704); best any-class "
          "00000000000000821082000000000000 (18/1238, class-1); best "
          "class-4 own-closable 00000000000000003800002000800000 (60/4216)")

    # ---------- 8. outputs ----------
    OUT.mkdir(exist_ok=True)

    result = {
        "schema": "n11-class2-lane-closability-ranking-1410-20261116-v1",
        "date": "2026-11-16",
        "head": st,
        "inputs": {
            "chain": "published cost-60c fold script "
                     "recompute_frontier_cost60c_receipts_20261116.py "
                     f"(git blob {FOLD_SCRIPT_BLOB}), re-run via runpy; it "
                     "internally reproduces the whole reconciliation chain "
                     "and re-asserts the head-1410 output blobs "
                     f"{HEAD_JSON_BLOB} / {HEAD_RANKING_BLOB} / "
                     f"{HEAD_TOPCAND_BLOB}",
            "scan": f"theorem-applicability-scan-20261116.json "
                    f"(git blob {SCAN_BLOB}); engine tallies per target, "
                    "115 transfers, 35-row STERILE census; geometry "
                    "(D4 canon + legal-candidate enumeration) from the "
                    "published scan implementation",
            "cost65j_cover_map":
                f"class2-lane-cost65j-win-marginals-20261116.json "
                f"(git blob {MAP65J_BLOB}); 17 WIN7-D10 receipts, 34-row "
                "union",
            "neighbor_analysis":
                f"class2-lane-sterile-rows-neighbor-analysis-20261116.json "
                f"(git blob {NEIGH_BLOB}); route-exhaustion context for the "
                "65k/70j/74h rows",
        },
        "method": {
            "chain_reproduction":
                "runpy reproduction of the published cost-60c fold script "
                "(head 1410/174/6438/509109/4711/373023, all internal "
                "asserts pass)",
            "row_categories":
                "win_receipt_scheduled (pending cost-65j cover-map union) > "
                "win_pending (engine WIN7-D10, fold not landed) > sterile "
                "(all own candidates REFUTED-D10 engine+transfer, 0 WIN, 0 "
                "capped) > transfer_partial > unswept; scheduled rows do "
                "not need their own sweep",
            "s5_categories":
                "fully_sterile (all rows sterile) / cross_cover_required "
                "(some sterile) / own_closable (no sterile rows)",
            "canon_agreement":
                "scan-implementation D4 canonical form == chain canonical "
                "form on all 12,274 parent-incidences",
            "enumeration":
                "exact integer circumcircle/line arithmetic, cross-checked "
                "bit-exact against the scan implementation on the fixed "
                "100-row sample",
        },
        "row_classification": {
            "counts": counts,
            "rows": {c: sorted(h for h, r in rows.items()
                               if r["category"] == c)
                     for c in CATEGORY_ORDER if c not in ("unswept",)},
            "row_details": {h: rows[h] for h in
                            sorted(h for h, r in rows.items()
                                   if r["category"] != "unswept")},
            "cost65j_scheduled_rows": {
                "rows": scheduled,
                "own_candidates_total": 635,
                "union_total_at_map_time": 34,
            },
        },
        "s5_classification": {
            "counts": ocounts,
            "orbits": [orbits[k] for k in sorted(orbits)],
        },
        "sterile_blocking": {
            "sterile_rows": 35,
            "blocked_parent_incidences": 91,
            "blocked_s5_orbits": len(blocked),
            "rows_by_blocked_orbit_count": {str(k): dist[k]
                                             for k in sorted(dist)},
            "note": "the 60 blocked orbits are exactly the 57 "
                    "cross_cover_required + 3 fully_sterile orbits",
        },
        "invariants": {
            "edge_cost_equals_own_candidates": {
                "rows_checked": 6438,
                "mismatches": 0,
                "total_own_candidates": 509109,
            },
            "sum_remaining_cost_equals_own_sweep_candidates": True,
            "remaining_sweep_work_after_transfers_and_cost65j":
                remaining_work,
        },
        "cost65j_consistency": {
            "receipts": 17,
            "union_rows": 34,
            "union_rows_remaining_at_head_1410": 9,
            "scheduled_own_candidates": 635,
            "any_receipt_covers_sterile_row": False,
        },
        "targets": {
            "best_own_closable_class2": {
                "s5_hex": oc_c2[0]["s5_hex"],
                "remaining_s6_orbits": 24, "remaining_s7_edge_cost": 1704},
            "best_own_closable_any_class": {
                "s5_hex": oc_all[0]["s5_hex"],
                "remaining_s6_orbits": 18, "remaining_s7_edge_cost": 1238,
                "classes": 1},
            "best_own_closable_class4": {
                "s5_hex": oc_c4[0]["s5_hex"],
                "remaining_s6_orbits": 60, "remaining_s7_edge_cost": 4216},
            "note": "the best coverable class-2 (3/209), audit-blocked "
                    "class-2 (10/698) and best class-4 (18/1460) S5 orbits "
                    "are fully_sterile: they can never be closed by their "
                    "own rows in the depth-10 receipt system",
        },
        "interpretation":
            "REFUTED-D10 is not a LOSS proof; STERILE rows are open. "
            "win_receipt_scheduled / win_pending / transfer_partial rows "
            "carry no game-theoretic claim. The frontier sweep planner "
            "should consume the worklist (505,675 open candidates) orbit by "
            "orbit, starting from the best own-closable targets.",
        "trust_boundary":
            "engine depth-10 verdict soundness + D4 invariance (identical "
            "to all published lane verdicts) + the published cost-60c fold "
            "chain + the published scan/cover-map/neighbor-analysis blobs. "
            "No new engine run is performed.",
        "unknown_status":
            "11x11 empty board, two-stone root {49,60}/{59,60}, S2 {59,60}, "
            "class 1, class 2 and class 4 all remain UNKNOWN.",
    }

    p = OUT / "class-frontier-closability-ranking-1410-20261116.json"
    p.write_text(json.dumps(result, indent=1) + "\n", newline="\n")
    sha, blen = git_blob_sha(p)
    print(f"blob {p.name}: {sha} ({blen} bytes)")

    p = OUT / "class-frontier-remaining-s6-worklist-1410-20261116.csv"
    with p.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["s6_canonical_hex", "category",
                    "own_candidates_s6_s7_edge_cost", "open_parents",
                    "engine_win7_d10", "engine_refuted_d10",
                    "transferred_refuted_d10",
                    "open_candidates_after_transfers"])
        for hx in sorted(rows,
                         key=lambda h: (CATEGORY_ORDER.index(
                             rows[h]["category"]),
                             rows[h]["own_candidates"], h)):
            r = rows[hx]
            w.writerow([r["s6_hex"], r["category"], r["own_candidates"],
                        r["open_parents"], r["engine_win7_d10"],
                        r["engine_refuted_d10"], r["transferred_refuted_d10"],
                        r["open_candidates_after_transfers"]])
    sha, blen = git_blob_sha(p)
    print(f"blob {p.name}: {sha} ({blen} bytes)")

    p = OUT / "class-frontier-s5-closability-after-cost60c-20261116.csv"
    with p.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["s5_hex", "classes", "category",
                    "remaining_s6_orbits", "remaining_s7_edge_cost",
                    "rows_sterile", "rows_win_pending",
                    "rows_win_receipt_scheduled", "rows_transfer_partial",
                    "rows_unswept", "own_sweep_candidates_after_transfers",
                    "sterile_rows"])
        for h in sorted(orbits, key=lambda k: (
                orbits[k]["remaining_s6_orbits"],
                orbits[k]["remaining_s7_edge_cost"], k)):
            o = orbits[h]
            w.writerow([o["s5_hex"], o["classes"], o["category"],
                         o["remaining_s6_orbits"],
                         o["remaining_s7_edge_cost"], o["rows_sterile"],
                         o["rows_win_pending"],
                         o["rows_win_receipt_scheduled"],
                         o["rows_transfer_partial"], o["rows_unswept"],
                         o["own_sweep_candidates_after_transfers"],
                         ";".join(o["sterile_rows"])])
    sha, blen = git_blob_sha(p)
    print(f"blob {p.name}: {sha} ({blen} bytes)")

    print(f"done in {time.time() - t0:.1f}s; 11x11 remains UNKNOWN")


if __name__ == "__main__":
    main()
