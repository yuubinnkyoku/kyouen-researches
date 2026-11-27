#!/usr/bin/env python3
"""Ninth-cost 12-row adoption measurement: BASE (eighth-cost k01 head
of record 0935c94c...) vs SCENARIO (ninth-cost 12-row adoption union,
47280073...) census deltas.

This follow-up Part is DECLARED (pre-registered in the ninth-cost
12-row adoption completion log as "the flip-census / reaudit Part of
the three WIN rows (k12/k02/k07) against this new head" and in the
adoption manifest's interpretation_guard field): the ninth-cost
canonical adoption consumes exactly the twelve published rows (9 LOSS
+ 3 WIN k12/k02/k07) and advances the canonical head of record from
0935c94c... (6,875 rows WIN 203 / LOSS 6,672) to 47280073... (6,887
rows WIN 206 / LOSS 6,681).  This script is a disclosed structural
adaptation of the eighth-cost k01 measurer 9c1b79a7... (itself the
Part SZ wave E measurer 29317c93... adaptation); it MEASURES the
census/scheduling delta of that declared adoption, from
published-byte-verbatim local inputs, and cross-checks this kit's
reaudit refresh outputs (byte-clone refresh of the published
eighth-cost k01 refresh 7e11a316..., three byte-identical
determinism runs):

* SCEN cache must equal BASE cache rows + exactly the 12 increment
  rows; every adopted row is fresh to BASE and matches the increment
  verdict/nodes exactly;
* the adoption manifest (ninthcost12-adoption-manifest-v1) pins: base
  head 0935c94c (6,875/203/6,672), increment 72eac70c, adopted 12
  rows WIN 3 / LOSS 9, nodes_total 130,803,321, freshness 12,
  WIN-LOSS conflict 0, duplicate 0, merger sha 90711961, the four
  C++-gate kits (33/32/23/29 files, audit_gate: PASS each) and the
  four third-impl kits (per-file byte pins, third_impl 08ea958f);
* the refresh status logic is replicated independently and must
  reproduce the refreshed class status census EXACTLY on both sides
  (BASE 34,400/120/39/390 unknown/excluded_now/free_now/excluded;
  SCEN 34,393/127/39/390);
* three of the twelve adopted rows are WINs (k12/k02/k07), so
  class-status flips are MEASURED, not asserted empty: the measured
  flip list is exactly the SEVEN owner classes of the three WIN keys
  (s5 indices 78950/62804/37372): classes 735
  (1152921539100807168:0), 1347 (1152921539117580288:0), 1780
  (1153203014077513728:0), 1845 (the ninth-cost serving class
  1297036692683751424:134217728, cost-unknown 99 -> 87, all twelve
  rows owned here), 16293 (1152921504607895552:32832), 31179
  (1152921505144766464:68719476736) and 31563
  (1152921504607895552:67141632), each unknown -> excluded_now (the
  Part EW/EM win-hit mechanism); the nine LOSS rows flip nothing
  (their owner classes keep their status; class 1792 merely drops
  cost-unknown 100 -> 99, the closure ladder's single measured
  unknown_now churn);
* no class flips to free_now and no free_now class is lost (39 -> 39,
  Board-verified both sides);
* closure-classes.csv churn is MEASURED: 804 -> 804 rows, entered [],
  left [], exactly ONE unknown_now churn (class 1792, 100 -> 99) and
  22 rank churns in the 521..536 band, CSV differs from the BASE side
  (unlike the single-row eighth-cost adoption);
* per-root coverage: free_now/uncovered identical on all 20 roots;
  exactly ONE individual greedy re-route is measured (root 26,
  5,229 -> 5,228); the CSV differs from the BASE side;
* the update8 refresh fields: all twelve adopted s5 indices sit
  OUTSIDE the frozen baseline requirement, so resolved stays 282 ->
  282 and remaining_now stays 31,444; the win-hit group set is
  unchanged (25 groups); groups_free_now stays 131;
* joint greedy stays 37,398 -> 37,398 and the probing worklist drops
  64,273 -> 64,272 (regen content sha differs from the BASE pin
  76b77442.../3,715,383 bytes; SCEN regen is 3,715,222 bytes).

11x11 stays UNKNOWN; nodes are bookkeeping; no root verdict is
consumed by this measurement; adopting solver-trusted S5 labels
flips class-status bookkeeping only (the scheduling machinery);
nothing is freed, excluded or covered at root level.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
D = ROOT / "research/experiments/n11-ninthcost-12row-adoption-reaudit-20261127"
EV = ROOT / "research/experiments/n11-eighthcost-k01-win-adoption-reaudit-20261127"
N12 = ROOT / "research/experiments/n11-ninthcost-12row-adoption-20261127"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
MANIFEST = N12 / "output/adoption-manifest.json"
MERGER = ROOT / "research/experiments/n11-centralreply-sixthlossk38-adoption-reaudit-20261126/scripts/s5_union_merge.py"

BASE_CACHE = ROOT / "research/experiments/n11-eighthcost-k01-win-adoption-20261127/output/merged-exact-s5-chain-plus-eighthcost-k01-20261127.cache"
SCEN_CACHE = N12 / "output/merged/merged-exact-s5-chain-plus-ninthcost12-20261127.cache"
INCREMENT = N12 / "output/increment-ninthcost12-adoption-20261127.cache"
BASE_SUMMARY = EV / "reaudit/output/refresh-summary.json"
SCEN_SUMMARY = D / "reaudit/output/refresh-summary.json"
BASE_CLOSURE = EV / "reaudit/output/closure-classes.csv"
SCEN_CLOSURE = D / "reaudit/output/closure-classes.csv"
BASE_PERROOT = EV / "reaudit/output/per-root-coverage.csv"
SCEN_PERROOT = D / "reaudit/output/per-root-coverage.csv"
BASE_CENSUS_JSON = EV / "output/census-deltas-eighthcost-k01-adoption.json"

BASE_CACHE_SHA_EXPECTED = "0935c94c03a9a3fbdf2a55aca90bb986a019dfd26c0097ab2c75709d590e9ca4"
SCEN_CACHE_SHA_EXPECTED = "4728007306598298f7fdb43d0368bc4e5fbd6c9435a38f8d1732d1df8368a622"
INCREMENT_SHA_EXPECTED = "72eac70c1503e7bfafcbdbe66adb12b1a1e52224ffca3eac296e2118c47a6bb0"
MANIFEST_SHA_EXPECTED = "db43c1a52171df30b10ff4b65dfd28eb2eb1435b41b2a95ff721852577f4537e"
BASE_SUMMARY_SHA_EXPECTED = "ff5c1586e79280ea927f0d189f64c49a7b85d5aec8b5acad435f616bed3f0a9a"
BASE_CLOSURE_SHA_EXPECTED = "ae1d0a7f32b02db148c3123c9fb6b57610beb4754ba8e491a3d145f199110533"
BASE_PERROOT_SHA_EXPECTED = "81b17904ec3ba8a530a54e4f315e1e225191ef5c1d62b6fb4b648bbe797775ff"
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_WORKLIST_PIN_SOURCE = json.loads(
    BASE_CENSUS_JSON.read_text(encoding="utf-8"))["worklist_regen_pins"]["scen"]

ADOPTED_COUNT = 12
ADOPTED_WIN = 3
ADOPTED_LOSS = 9
ADOPTED_NODES_TOTAL = 130803321
SERVING_CLASS = 1845
SERVING_CLASS_MASK = (1297036692683751424, 134217728)
WIN_KEYS = {
    "k12": (1297036692683751424, 134217792),
    "k02": (1297036692683751424, 201326592),
    "k07": (1152923703765368832, 68719476736),
}
WIN_S5_INDICES = {"k12": 78950, "k02": 62804, "k07": 37372}
WIN_OWNER_CLASSES = {
    "k12": [1780, 1845, 16293],
    "k02": [1347, 1845, 31563],
    "k07": [735, 1845, 31179],
}
EXPECTED_FLIPS = [735, 1347, 1780, 1845, 16293, 31179, 31563]
EXPECTED_UNKNOWN_CHURN = [{"class_index": 1792, "base": 100, "scen": 99}]
EXPECTED_RANK_CHURN_COUNT = 22
EXPECTED_GREEDY_DELTA = [{"root": 26, "base": 5229, "scen": 5228}]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_cache(path: Path) -> dict:
    cache = {}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].lstrip().startswith("#"):
                continue
            assert len(row) == 6 and row[0] == "s5verdict", row
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            assert stones == 5 and verdict in (1, 2) and nodes >= 0
            key = (lo, hi)
            if key in cache and cache[key][0] != verdict:
                raise ValueError(f"WIN/LOSS conflict inside {path}: {key}")
            cache[key] = (verdict, nodes)
    return cache


def main() -> None:
    out = {}
    out["base_cache"] = {"sha256": sha(BASE_CACHE)}
    out["scen_cache"] = {"sha256": sha(SCEN_CACHE)}
    out["increment"] = {"sha256": sha(INCREMENT)}
    out["manifest"] = {"sha256": sha(MANIFEST)}
    assert out["base_cache"]["sha256"] == BASE_CACHE_SHA_EXPECTED
    assert out["scen_cache"]["sha256"] == SCEN_CACHE_SHA_EXPECTED
    assert out["increment"]["sha256"] == INCREMENT_SHA_EXPECTED
    assert out["manifest"]["sha256"] == MANIFEST_SHA_EXPECTED
    assert sha(MERGER) == MERGER_SHA_EXPECTED
    for name, p, expect in (("base_summary", BASE_SUMMARY, BASE_SUMMARY_SHA_EXPECTED),
                            ("base_closure", BASE_CLOSURE, BASE_CLOSURE_SHA_EXPECTED),
                            ("base_per_root", BASE_PERROOT, BASE_PERROOT_SHA_EXPECTED)):
        out[name] = {"sha256": sha(p)}
        assert out[name]["sha256"] == expect, name
    for name, p in (("scen_summary", SCEN_SUMMARY), ("scen_closure", SCEN_CLOSURE),
                    ("scen_per_root", SCEN_PERROOT)):
        out[name] = {"sha256": sha(p)}

    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    incr = load_cache(INCREMENT)

    # SCEN == BASE + exactly the increment rows
    keys_inc = set(incr)
    keys_scen = set(scen)
    keys_base = set(base)
    assert keys_scen - keys_base == keys_inc
    assert keys_base - keys_scen == set()
    for k in keys_inc:
        assert scen[k] == incr[k], (k, scen[k], incr[k])
    for k in keys_base:
        assert scen[k] == base[k]
    base_wins = sum(1 for v in base.values() if v[0] == 1)
    base_loss = sum(1 for v in base.values() if v[0] == 2)
    scen_wins = sum(1 for v in scen.values() if v[0] == 1)
    scen_loss = sum(1 for v in scen.values() if v[0] == 2)
    out["base_cache"].update(rows=len(base), win=base_wins, loss=base_loss)
    out["scen_cache"].update(rows=len(scen), win=scen_wins, loss=scen_loss)
    assert (len(base), base_wins, base_loss) == (6875, 203, 6672)
    assert (len(scen), scen_wins, scen_loss) == (6887, 206, 6681)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "ninthcost12-adoption-manifest-v1"
    assert manifest["base_head"]["sha256"] == BASE_CACHE_SHA_EXPECTED
    assert (manifest["base_head"]["rows"], manifest["base_head"]["win"],
            manifest["base_head"]["loss"]) == (6875, 203, 6672)
    assert manifest["kit"] == "n11-ninthcost-12row-adoption-20261127"
    assert manifest["increment"]["sha256"] == INCREMENT_SHA_EXPECTED
    assert manifest["frozen_pins"]["merger_sha256"] == MERGER_SHA_EXPECTED
    adopted = manifest["adopted"]
    assert (adopted["rows"], adopted["win"], adopted["loss"]) == (12, 3, 9)
    assert adopted["nodes_total"] == ADOPTED_NODES_TOTAL
    assert adopted["freshness"] == ADOPTED_COUNT
    assert adopted["win_loss_conflicts"] == 0
    assert adopted["duplicates"] == 0
    assert manifest["third_impl_pillar"]["third_impl_sha256"] == \
        "08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998"
    for kit, files in (("G4L", 33), ("G4R", 32), ("GK12", 23), ("GP3", 29)):
        assert manifest["pillars"][kit]["files"] == files, kit
        assert manifest["pillars"][kit]["audit_live"] == "audit_gate: PASS", kit
    for kit, files in (("T4L", 14), ("T4R", 10), ("TK12", 4), ("TP3", 8)):
        ti = manifest["third_impl_pillar"]["kits"][kit]
        assert ti["files"] == ti["pins_verified"] == files, kit

    # adopted rows derived from the increment itself
    assert len(incr) == ADOPTED_COUNT
    win_keys = sorted(k for k, v in incr.items() if v[0] == 1)
    loss_keys = sorted(k for k, v in incr.items() if v[0] == 2)
    assert len(win_keys) == ADOPTED_WIN and len(loss_keys) == ADOPTED_LOSS
    assert set(win_keys) == set(WIN_KEYS.values()), win_keys
    for k, v in incr.items():
        assert k not in base, f"adopted row not fresh to BASE: {k}"
        assert scen[k] == v

    # graph
    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s4_masks = g["s4_masks"]
    s4_status = g["s4_status"]
    s4_cost = g["s4_cost"]
    s5_masks = g["s5_masks"]
    mask_to_index = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}
    assert tuple(s4_masks[SERVING_CLASS]) == SERVING_CLASS_MASK
    for label, key in WIN_KEYS.items():
        assert mask_to_index[key] == WIN_S5_INDICES[label], label

    update8 = json.loads(UPDATE8.read_text(encoding="utf-8"))
    receipt = {int(k): int(v) for k, v in update8["resolved_s5_verdicts"].items()}

    # s5 index round trip + owner classes for all 12 rows
    owner_classes = {}
    adopted_indices = {}
    for key in incr:
        idx = mask_to_index.get(key)
        assert idx is not None, key
        adopted_indices[key] = idx
        owner_classes[key] = [ci for ci in range(len(s4_masks))
                              if idx in s4_cost[ci]]
    for label, key in WIN_KEYS.items():
        assert owner_classes[key] == WIN_OWNER_CLASSES[label], \
            (label, owner_classes[key])
    # the ninth-cost serving class owns all 12 adopted rows
    for key, idx in adopted_indices.items():
        assert idx in s4_cost[SERVING_CLASS], key
    out["owner_class_count_hist"] = {
        str(n): sum(1 for x in owner_classes.values() if len(x) == n)
        for n in {len(x) for x in owner_classes.values()}}
    assert out["owner_class_count_hist"] == {"3": 12}, \
        out["owner_class_count_hist"]
    out["adopted"] = [
        {"lo": k[0], "hi": k[1], "verdict": incr[k][0], "nodes": incr[k][1],
         "s5_index": adopted_indices[k],
         "serving_class": SERVING_CLASS,
         "owner_classes": owner_classes[k], "owner_count": len(owner_classes[k])}
        for k in sorted(incr)]

    def census(cache):
        status = {}
        for i in range(len(s4_masks)):
            st = s4_status[i]
            cost = s4_cost[i]
            if st == -1:
                status[i] = "excluded"
                continue
            win_hit = False
            unknown_left = False
            for j in cost:
                v = None
                key = tuple(s5_masks[j])
                if key in cache:
                    v = cache[key][0]
                else:
                    v = receipt.get(j)
                if v == 1:
                    win_hit = True
                elif v is None:
                    unknown_left = True
            if win_hit:
                status[i] = "excluded_now"
            elif not unknown_left:
                status[i] = "free_now"
            else:
                status[i] = "unknown"
        return status

    base_status = census(base)
    scen_status = census(scen)

    base_sum = json.loads(BASE_SUMMARY.read_text(encoding="utf-8"))
    scen_sum = json.loads(SCEN_SUMMARY.read_text(encoding="utf-8"))
    fb = base_sum["board_verification"]["board_verified_free"]
    fs = scen_sum["board_verification"]["board_verified_free"]
    assert fb == base_sum["board_verification"]["free_candidates"] == \
        base_sum["class_status_counts"]["free_now"] == 39
    assert fs == scen_sum["board_verification"]["free_candidates"] == \
        scen_sum["class_status_counts"]["free_now"] == 39
    assert base_sum["board_verification"]["rejected"] == {}
    assert scen_sum["board_verification"]["rejected"] == {}

    def counts_from(status):
        c = {"unknown": 0, "excluded_now": 0, "free_now": 0, "excluded": 0}
        for v in status.values():
            c[v] += 1
        return c

    cb, cs = counts_from(base_status), counts_from(scen_status)
    out["census_recount_base"] = cb
    out["census_recount_scen"] = cs
    assert cb == base_sum["class_status_counts"], \
        (cb, base_sum["class_status_counts"])
    assert cs == scen_sum["class_status_counts"], \
        (cs, scen_sum["class_status_counts"])
    assert cb == {"unknown": 34400, "excluded_now": 120,
                  "free_now": 39, "excluded": 390}, cb
    assert cs == {"unknown": 34393, "excluded_now": 127,
                  "free_now": 39, "excluded": 390}, cs

    # WIN-side flips (Part EW/EM win-hit mechanism): MEASURED.
    # Every flip must be an owner class of a WIN row and must go
    # unknown -> excluded_now; no other flip direction may occur.
    flips = sorted(ci for ci in base_status
                   if base_status[ci] != scen_status[ci])
    out["status_flips"] = [
        {"class_index": ci, "base": base_status[ci], "scen": scen_status[ci],
         "class_mask": s4_masks[ci]}
        for ci in flips]
    assert flips == EXPECTED_FLIPS, flips
    win_owner_union = sorted({ci for key in WIN_KEYS.values()
                              for ci in owner_classes[key]})
    assert set(flips) == set(win_owner_union), \
        "the flip list must be exactly the WIN rows' owner classes"
    for ci in flips:
        assert base_status[ci] == "unknown", ci
        assert scen_status[ci] == "excluded_now", ci
    out["status_flip_count"] = len(flips)
    # no free_now change and no other census movement
    assert cb["free_now"] == cs["free_now"] == 39
    assert cb["excluded"] == cs["excluded"] == 390
    assert cs["unknown"] == cb["unknown"] - len(flips)

    # serving-class unknown arithmetic (graph-derived, class 1845)
    serving_rows = {}
    cls = SERVING_CLASS
    cost = s4_cost[cls]
    unknown_base = [j for j in cost
                    if tuple(s5_masks[j]) not in base and j not in receipt]
    unknown_scen = [j for j in cost
                    if tuple(s5_masks[j]) not in scen and j not in receipt]
    serving_rows[str(cls)] = {
        "class_mask": list(SERVING_CLASS_MASK),
        "base_status": base_status[cls],
        "scen_status": scen_status[cls],
        "unknown_before": len(unknown_base),
        "unknown_after": len(unknown_scen),
        "adopted_owned_here": sum(1 for key in incr
                                  if adopted_indices[key] in cost),
    }
    assert (serving_rows[str(cls)]["unknown_before"]
            - serving_rows[str(cls)]["unknown_after"]
            == serving_rows[str(cls)]["adopted_owned_here"]), cls
    # the ninth-cost selection class 1297036692683751424:134217728 held
    # 99 unknown children on the BASE head; adopting exactly its twelve
    # resolved keys drops its cost-unknown 99 -> 87 and the three WIN
    # rows among them flip it unknown -> excluded_now (win-hit)
    assert serving_rows[str(cls)]["base_status"] == "unknown"
    assert serving_rows[str(cls)]["scen_status"] == "excluded_now"
    assert (serving_rows[str(cls)]["unknown_before"],
            serving_rows[str(cls)]["unknown_after"]) == (99, 87), cls
    assert serving_rows[str(cls)]["adopted_owned_here"] == 12
    out["serving_class_rows"] = serving_rows

    # closure-classes.csv churn (measured, NOT asserted empty: the LOSS
    # consumption re-ranks the closure ladder this time)
    def load_closure(p):
        rows = {}
        with p.open() as stream:
            for r in csv.DictReader(stream):
                rows[int(r["class_index"])] = r
        return rows

    bc, sc = load_closure(BASE_CLOSURE), load_closure(SCEN_CLOSURE)
    entered = sorted(set(sc) - set(bc))
    left = sorted(set(bc) - set(sc))
    unknown_churn = []
    rank_churn = []
    for ci in set(bc) & set(sc):
        a, b = bc[ci], sc[ci]
        if a["unknown_now"] != b["unknown_now"]:
            unknown_churn.append(
                {"class_index": ci, "base": int(a["unknown_now"]),
                 "scen": int(b["unknown_now"])})
        if a["class_rank"] != b["class_rank"]:
            rank_churn.append(
                {"class_index": ci, "base": int(a["class_rank"]),
                 "scen": int(b["class_rank"])})
    out["closure_churn"] = {
        "rows_base": len(bc), "rows_scen": len(sc),
        "entered": entered, "left": left,
        "unknown_now_churn": unknown_churn,
        "rank_churn_ranked": rank_churn,
    }
    assert len(bc) == len(sc) == 804, (len(bc), len(sc))
    # MEASURED: no entered/left, exactly one unknown_now churn (class
    # 1792, a LOSS-row owner class, 100 -> 99), 22 rank churns in the
    # 521..536 band; the CSV differs from the BASE side
    assert entered == [], entered
    assert left == [], left
    assert unknown_churn == EXPECTED_UNKNOWN_CHURN, unknown_churn
    assert len(rank_churn) == EXPECTED_RANK_CHURN_COUNT, len(rank_churn)
    # the churned class 1792 (unknown 100 -> 99) leapfrogs from rank 537
    # to rank 516 and the 21 classes it passes each shift down by one
    churn_map = {item["class_index"]: (item["base"], item["scen"])
                 for item in rank_churn}
    assert churn_map[1792] == (537, 516), churn_map[1792]
    assert len(churn_map) == 22
    for ci, (b, s) in churn_map.items():
        if ci == 1792:
            continue
        assert s == b + 1 and 516 <= b <= 536, (ci, b, s)
    assert BASE_CLOSURE.read_text() != SCEN_CLOSURE.read_text(), \
        "closure-classes.csv must differ from the BASE side this time"
    out["closure_byte_identical_to_base"] = False
    churn_classes = {item["class_index"] for item in unknown_churn}
    # the churn class is a LOSS-row owner class; the flipped (excluded_now)
    # classes never enter the ladder on either side
    for ci in win_owner_union:
        assert ci not in bc and ci not in sc, ci
    loss_owner_union = sorted({ci for k, v in incr.items() if v[0] == 2
                               for ci in owner_classes[k]})
    assert churn_classes <= set(loss_owner_union), churn_classes
    out["loss_owner_class_union"] = loss_owner_union

    # per-root coverage: free_now/uncovered identical on all 20 roots;
    # the individual greedy unions re-route (measured)
    def load_perroot(p):
        rows = {}
        with p.open() as stream:
            for r in csv.DictReader(stream):
                rows[int(r["first"])] = r
        return rows

    bp, sp = load_perroot(BASE_PERROOT), load_perroot(SCEN_PERROOT)
    assert set(bp) == set(sp) and len(bp) == 20
    greedy_delta = []
    for ci in sorted(bp):
        a, b = bp[ci], sp[ci]
        assert a["free_now"] == b["free_now"], ci
        assert a["uncovered"] == b["uncovered"], ci
        ga = int(a["individual_greedy_union"] or 0)
        gb = int(b["individual_greedy_union"] or 0)
        if ga != gb:
            greedy_delta.append({"root": ci, "base": ga, "scen": gb})
    out["per_root_greedy_delta"] = greedy_delta
    out["per_root_free_and_uncovered_identical"] = True
    # MEASURED: exactly one greedy re-route (root 26, 5229 -> 5228);
    # the per-root CSV differs from the BASE side
    assert greedy_delta == EXPECTED_GREEDY_DELTA, greedy_delta
    out["per_root_coverage_byte_identical"] = \
        BASE_PERROOT.read_text() == SCEN_PERROOT.read_text()
    assert out["per_root_coverage_byte_identical"] is False

    # update8 refresh, joint greedy, worklist
    out["update8_refresh_base"] = {
        "resolved": base_sum["frozen_update8_refresh"]["resolved_count"],
        "remaining": base_sum["frozen_update8_refresh"]["remaining_now"],
        "groups_free_now": base_sum["frozen_update8_refresh"]["groups_free_now"],
        "win_hit_groups": len(base_sum["frozen_update8_refresh"]["win_hit_groups"]),
    }
    out["update8_refresh_scen"] = {
        "resolved": scen_sum["frozen_update8_refresh"]["resolved_count"],
        "remaining": scen_sum["frozen_update8_refresh"]["remaining_now"],
        "groups_free_now": scen_sum["frozen_update8_refresh"]["groups_free_now"],
        "win_hit_groups": len(scen_sum["frozen_update8_refresh"]["win_hit_groups"]),
    }
    base_req = set(base_sum["frozen_update8_refresh"]
                   ["resolved_among_baseline_requirement"])
    scen_req = set(scen_sum["frozen_update8_refresh"]
                   ["resolved_among_baseline_requirement"])
    new_resolved = scen_req - base_req
    baseline_req = set(update8["required_new_s5"])
    adopted_idx = set(adopted_indices.values())
    expected_new = adopted_idx & baseline_req
    assert base_req <= baseline_req, \
        "base resolved set must sit in the frozen requirement"
    assert new_resolved == expected_new, \
        (sorted(new_resolved), sorted(expected_new))
    # MEASURED: all twelve adopted rows sit OUTSIDE the frozen
    # requirement, so NO new baseline s5 resolves
    assert new_resolved == set(), sorted(new_resolved)
    assert adopted_idx & baseline_req == set()
    adopted_outside_requirement = sorted(adopted_idx - baseline_req)
    assert len(adopted_outside_requirement) == ADOPTED_COUNT
    assert len(new_resolved) == (
        out["update8_refresh_scen"]["resolved"]
        - out["update8_refresh_base"]["resolved"]), "resolved delta"
    out["update8_refresh_base"]["resolved_list_len"] = len(base_req)
    out["update8_refresh_scen"]["resolved_list_len"] = len(scen_req)
    assert out["update8_refresh_base"]["resolved"] == 282
    assert out["update8_refresh_scen"]["resolved"] == 282
    assert out["update8_refresh_base"]["remaining"] == 31444
    assert out["update8_refresh_scen"]["remaining"] == 31444
    assert out["update8_refresh_base"]["groups_free_now"] == 131
    assert out["update8_refresh_scen"]["groups_free_now"] == 131
    out["update8_new_resolved"] = sorted(new_resolved)
    out["adopted_outside_baseline_requirement"] = adopted_outside_requirement

    def group_key(gr):
        return (gr["first"], gr["third"], gr["fourth"], gr["reply"],
                gr["s4_class_index"])
    b_groups = sorted(group_key(x)
                      for x in base_sum["frozen_update8_refresh"]["win_hit_groups"])
    s_groups = sorted(group_key(x)
                      for x in scen_sum["frozen_update8_refresh"]["win_hit_groups"])
    out["win_hit_groups_identical"] = b_groups == s_groups
    # measured: none of the seven flipped classes is an update8 plan
    # group class, so the win-hit group set is unchanged
    assert out["win_hit_groups_identical"], \
        "the win-hit group set must be unchanged by this adoption"
    assert len(b_groups) == 25, len(b_groups)
    u8_group_classes = {gr["s4_class_index"]
                        for gr in base_sum["frozen_update8_refresh"]["win_hit_groups"]}
    assert set(win_owner_union).isdisjoint(u8_group_classes)

    out["joint_greedy"] = {
        "base": base_sum["joint_greedy"]["greedy_union_size"],
        "scen": scen_sum["joint_greedy"]["greedy_union_size"],
    }
    out["worklist_total"] = {
        "base": base_sum["worklist_total"],
        "scen": scen_sum["worklist_total"],
    }
    # measured: the joint greedy is unchanged and the probing worklist
    # drops by exactly one row
    assert out["joint_greedy"] == {"base": 37398, "scen": 37398}, \
        out["joint_greedy"]
    assert out["worklist_total"] == {"base": 64273, "scen": 64272}, \
        out["worklist_total"]

    # worklist regen pins (UNPUBLISHED per size policy; the BASE side is
    # the published eighth-cost census json's scen regen pin, the SCEN
    # side is this kit's local regen pin)
    swl = D / "reaudit/output/probe-worklist.csv"
    assert swl.is_file()
    out["worklist_regen_pins"] = {
        "base": BASE_WORKLIST_PIN_SOURCE,
        "scen": {"sha256": sha(swl), "size": swl.stat().st_size},
    }
    assert out["worklist_regen_pins"]["base"]["sha256"] == \
        "76b7744293d31bd0f708307c41fddb5e257f1ff0e4284e8a5cfdf0802338e1cf"
    assert out["worklist_regen_pins"]["base"]["size"] == 3715383
    assert out["worklist_regen_pins"]["scen"]["size"] == 3715222, \
        out["worklist_regen_pins"]["scen"]

    out["verdict"] = {
        "part_declared": True,
        "part": "ninthcost12-flip-census",
        "canonical_head_sha256": SCEN_CACHE_SHA_EXPECTED,
        "consumed": ("exactly the twelve published ninth-cost rows "
                     "(9 LOSS + 3 WIN k12/k02/k07)"),
        "status_flips": len(flips),
        "status_flip_mechanism": (
            "win-hit (the Part EW/EM mechanism): the three adopted WIN "
            "rows k12 (s5 index 78950), k02 (62804) and k07 (37372) flip "
            "their seven owner classes 735 (1152921539100807168:0), 1347 "
            "(1152921539117580288:0), 1780 (1153203014077513728:0), 1845 "
            "(the ninth-cost serving class 1297036692683751424:134217728, "
            "cost-unknown 99 -> 87, all twelve rows owned here), 16293 "
            "(1152921504607895552:32832), 31179 "
            "(1152921505144766464:68719476736) and 31563 "
            "(1152921504607895552:67141632) from unknown to excluded_now; "
            "no class flips to free_now, free_now stays 39 (Board-verified "
            "both sides); the nine LOSS rows flip nothing, they only "
            "consume unknown children (closure ladder: one unknown_now "
            "churn, class 1792 100 -> 99, 22 rank churns, no entered/left); "
            "per-root coverage: one greedy re-route (root 26, 5229 -> "
            "5228); joint greedy stays 37398 and the probing worklist "
            "drops 64273 -> 64272 (regen content sha differs from the "
            "BASE pin); all twelve adopted s5 indices sit outside the "
            "frozen update8 baseline requirement (resolved 282 -> 282, "
            "remaining_now 31444 -> 31444, groups_free_now 131 -> 131); "
            "the win-hit group set is unchanged (25)"),
        "census_counts_identical_to_published_summaries": True,
        "note": ("declared ninth-cost 12-row adoption measurement; adopting "
                 "solver-trusted S5 labels flips class-status bookkeeping "
                 "only: no root verdict is consumed, no root freed, no "
                 "root excluded, no coverage claim is made or changed; "
                 "11x11 stays UNKNOWN; no root verdict; nodes are "
                 "bookkeeping"),
    }

    outp = D / "output/census-deltas-ninthcost12-adoption.json"
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "base_census": cb, "scen_census": cs,
        "status_flip_count": len(flips), "flips": out["status_flips"],
        "serving_class_rows": serving_rows,
        "owner_class_count_hist": out["owner_class_count_hist"],
        "closure_churn": {k: out["closure_churn"][k] for k in
                          ("rows_base", "rows_scen", "entered", "left",
                           "unknown_now_churn")},
        "closure_rank_churn_count": len(rank_churn),
        "per_root_greedy_delta": greedy_delta,
        "joint_greedy": out["joint_greedy"],
        "worklist_total": out["worklist_total"],
        "update8_new_resolved": out["update8_new_resolved"],
        "win_hit_groups_identical": out["win_hit_groups_identical"],
    }, indent=1))
    print("written:", outp)


if __name__ == "__main__":
    main()
