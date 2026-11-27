#!/usr/bin/env python3
"""Eighth-cost k01 WIN adoption measurement: BASE (seventhcost42 head
of record 5b6e77f7...) vs SCENARIO (eighth-cost k01 single-row
adoption union, 0935c94c...) census deltas.

This follow-up Part is DECLARED (pre-registered in the eighth-cost
k01 WIN adoption completion log as "class-status flip census
measurement" and in the adoption manifest's follow_up_declared field):
the eighth-cost canonical adoption consumes exactly the single
published k01 WIN row (1297036692750860288:64; replica cold pair
3be9db9b x2
and advances the canonical head of record from 5b6e77f7... (6,874
rows WIN 202 / LOSS 6,672; the Part SZ adoption head of record) to
0935c94c... (6,875 rows WIN 203 / LOSS 6,672).  This script is a
disclosed structural adaptation of the Part SZ wave E measurer
(fresh single-row expectations); it MEASURES the census/scheduling
delta of that declared adoption, from published-byte-verbatim local
inputs, and cross-checks this kit's reaudit refresh outputs (byte-
clone refresh of the published Part SZ wave E refresh d8b14697...,
three byte-identical determinism runs):

* SCEN cache must equal BASE cache rows + exactly the 1 increment
  row; the adopted row is fresh to BASE and matches the increment
  verdict/nodes exactly;
* the adoption manifest (eighthcost-k01-win-adoption-manifest-v1)
  pins: base head 5b6e77f7 (6,874/202/6,672), increment 8e649a0a,
  adopted 1 row WIN 1, nodes_total 8,514,427, freshness 1, WIN-LOSS
  conflict 0, duplicate 0, merger sha 90711961 (3 runs), the
  replica/C++-gate/third-impl pillars and the 42 WIN-stopping-rule
  suppressed keys NOT adopted;
* the refresh status logic is replicated independently and must
  reproduce the refreshed class status census EXACTLY on both sides
  (BASE 34,403/117/39/390 unknown/excluded_now/free_now/excluded;
  SCEN 34,400/120/39/390);
* this adoption is a single WIN row, so class-status flips are
  MEASURED, not asserted empty: the measured flip list is exactly
  the three owner classes of the WIN key (s5 index 91779): classes
  2182 (mask 1154117773392084992:0), 2197 (the eighth-cost serving
  class, mask 1297036692750860288:0, unknown 100 -> 99, the adopted
  row owned here, status unknown -> excluded_now) and 16914 (mask
  1152921504675004416:64) - the Part EW/EM win-hit mechanism;
* no class flips to free_now and no free_now class is lost (39 -> 39,
  Board-verified both sides);
* closure-classes.csv and per-root-coverage.csv churn are MEASURED
  (both measured BYTE-IDENTICAL to the BASE side this time: no
  ladder re-rank, no unknown_now churn, no entered/left, no greedy
  re-route);
* the update8 refresh fields: the single adopted s5 index (91779,
  WIN) sits OUTSIDE the frozen baseline requirement, so resolved
  stays 282 -> 282 and remaining_now stays 31,444; the win-hit group
  set is unchanged (25 groups);
* joint greedy and worklist totals are measured against the
  published Part SZ wave E reaudit outputs (BASE side pins
  3944bf1c/ae1d0a7f/81b17904): joint greedy 37,398 -> 37,398
  (identical), worklist 64,273 -> 64,273 (total identical, regen
  content sha differs from the BASE pin).

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
D = ROOT / "research/experiments/n11-eighthcost-k01-win-adoption-reaudit-20261127"
SV = ROOT / "research/experiments/n11-seventhcost-sz-reaudit-20261127"
SZ = ROOT / "research/experiments/n11-eighthcost-k01-win-adoption-20261127"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
MANIFEST = SZ / "output/adoption-manifest.json"
MERGER = ROOT / "research/experiments/n11-centralreply-sixthlossk38-adoption-reaudit-20261126/scripts/s5_union_merge.py"

BASE_CACHE = ROOT / "research/experiments/n11-seventhcost-sz-adoption-20261127/output/merged/merged-exact-s5-chain-plus-seventhcost42-20261127.cache"
SCEN_CACHE = SZ / "output/merged-exact-s5-chain-plus-eighthcost-k01-20261127.cache"
INCREMENT = SZ / "output/increment-eighthcost-k01-win-adoption-20261127.cache"
BASE_SUMMARY = SV / "reaudit/output/refresh-summary.json"
SCEN_SUMMARY = D / "reaudit/output/refresh-summary.json"
BASE_CLOSURE = SV / "reaudit/output/closure-classes.csv"
SCEN_CLOSURE = D / "reaudit/output/closure-classes.csv"
BASE_PERROOT = SV / "reaudit/output/per-root-coverage.csv"
SCEN_PERROOT = D / "reaudit/output/per-root-coverage.csv"
BASE_CENSUS_JSON = SV / "output/census-deltas-seventhcost42-adoption.json"

BASE_CACHE_SHA_EXPECTED = "5b6e77f7d7832d4ce84cb1f080a93e066eb052dcf8b817e5d560f95499fcdde2"
SCEN_CACHE_SHA_EXPECTED = "0935c94c03a9a3fbdf2a55aca90bb986a019dfd26c0097ab2c75709d590e9ca4"
INCREMENT_SHA_EXPECTED = "8e649a0a591bbe53ef35c625957c4886752bfb7f662d5483e9d03dede35023d9"
MANIFEST_SHA_EXPECTED = "09cf869ece71f6d0dcb909c50e30277959aa5fa33608948108f25b08a7c4a940"
BASE_SUMMARY_SHA_EXPECTED = "3944bf1c5353abdf5772230774d56c4be7c67569080505364ef9ed793c0d05f1"
BASE_CLOSURE_SHA_EXPECTED = "ae1d0a7f32b02db148c3123c9fb6b57610beb4754ba8e491a3d145f199110533"
BASE_PERROOT_SHA_EXPECTED = "81b17904ec3ba8a530a54e4f315e1e225191ef5c1d62b6fb4b648bbe797775ff"
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_WORKLIST_PIN_SOURCE = json.loads(
    BASE_CENSUS_JSON.read_text(encoding="utf-8"))["worklist_regen_pins"]["scen"]

ADOPTED_COUNT = 1
ADOPTED_NODES_TOTAL = 8514427
SERVING_CLASS = 2197
SERVING_CLASS_MASK = (1297036692750860288, 0)
WIN_KEY = (1297036692750860288, 64)
WIN_S5_INDEX = 91779
WIN_OWNER_CLASSES = [2182, 2197, 16914]
EXPECTED_FLIPS = [2182, 2197, 16914]
NEWLY_RESOLVED_BASELINE_INDEX = None  # none this time (WIN row outside requirement)
NEWLY_RESOLVED_BASELINE_KEY = None


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
    assert (len(base), base_wins, base_loss) == (6874, 202, 6672)
    assert (len(scen), scen_wins, scen_loss) == (6875, 203, 6672)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "eighthcost-k01-win-adoption-manifest-v1"
    assert manifest["base_head"]["sha256"] == BASE_CACHE_SHA_EXPECTED
    assert (manifest["base_head"]["rows"], manifest["base_head"]["win"],
            manifest["base_head"]["loss"]) == (6874, 202, 6672)
    assert manifest["kit"] == "n11-eighthcost-k01-win-adoption-20261127"
    assert manifest["expected_merged"] == {"rows": 6875, "win": 203, "loss": 6672}
    assert manifest["merger"]["sha256"] == MERGER_SHA_EXPECTED
    assert manifest["merger"]["runs"] == 3
    assert manifest["suppressed_not_adopted"]["keys"] == 42
    assert manifest["adopted"]["row"] == \
        "s5verdict,1297036692750860288,64,5,1,8514427"
    adopted = manifest["adopted"]
    assert (adopted["rows"], adopted["win"], adopted["loss"]) == (1, 1, 0)
    assert adopted["nodes_total"] == ADOPTED_NODES_TOTAL
    assert adopted["freshness"] == ADOPTED_COUNT
    assert adopted["win_loss_conflicts"] == 0
    assert adopted["duplicates"] == 0
    assert manifest["pillars"]["replica"]["at15m_pair_sha256"] == \
        "3be9db9b76f5dbd2756ffe51a2eb4e2c62c09f12d6999f7bc9a0376075479062"
    assert manifest["pillars"]["replica"]["win_nodes"] == 8514427
    assert manifest["pillars"]["cpp_gate"]["files"] == 24
    assert manifest["pillars"]["third_impl"]["expansions"] == 9987963

    # adopted rows derived from the increment itself (the SZ manifest has
    # no per-row table; per-row fields are graph-derived here)
    assert len(incr) == ADOPTED_COUNT
    win_keys = [k for k, v in incr.items() if v[0] == 1]
    loss_keys = [k for k, v in incr.items() if v[0] == 2]
    assert len(win_keys) == 1 and len(loss_keys) == 0
    assert win_keys[0] == WIN_KEY
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
    assert mask_to_index[WIN_KEY] == WIN_S5_INDEX

    update8 = json.loads(UPDATE8.read_text(encoding="utf-8"))
    receipt = {int(k): int(v) for k, v in update8["resolved_s5_verdicts"].items()}

    # s5 index round trip + owner classes at graph time for all 42 rows
    owner_classes = {}
    adopted_indices = {}
    for key in incr:
        idx = mask_to_index.get(key)
        assert idx is not None, key
        adopted_indices[key] = idx
        owner_classes[key] = [ci for ci in range(len(s4_masks))
                              if idx in s4_cost[ci]]
    assert adopted_indices[WIN_KEY] == WIN_S5_INDEX
    assert owner_classes[WIN_KEY] == WIN_OWNER_CLASSES, owner_classes[WIN_KEY]
    # the seventh-cost serving class owns all 42 adopted rows
    for key, idx in adopted_indices.items():
        assert idx in s4_cost[SERVING_CLASS], key
    out["owner_class_count_hist"] = {
        str(n): sum(1 for x in owner_classes.values() if len(x) == n)
        for n in {len(x) for x in owner_classes.values()}}
    assert out["owner_class_count_hist"] == {"3": 1}, \
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
    assert cb == {"unknown": 34403, "excluded_now": 117,
                  "free_now": 39, "excluded": 390}, cb
    assert cs == {"unknown": 34400, "excluded_now": 120,
                  "free_now": 39, "excluded": 390}, cs

    # WIN-side flips (Part EW/EM win-hit mechanism): MEASURED.
    # Every flip must be an owner class of the WIN row and must go
    # unknown -> excluded_now; no other flip direction may occur.
    flips = sorted(ci for ci in base_status
                   if base_status[ci] != scen_status[ci])
    out["status_flips"] = [
        {"class_index": ci, "base": base_status[ci], "scen": scen_status[ci],
         "class_mask": s4_masks[ci]}
        for ci in flips]
    assert flips == EXPECTED_FLIPS, flips
    assert set(flips) == set(owner_classes[WIN_KEY]), \
        "the flip list must be exactly the WIN row owner classes"
    for ci in flips:
        assert base_status[ci] == "unknown", ci
        assert scen_status[ci] == "excluded_now", ci
    out["status_flip_count"] = len(flips)
    # no free_now change and no other census movement
    assert cb["free_now"] == cs["free_now"] == 39
    assert cb["excluded"] == cs["excluded"] == 390
    assert cs["unknown"] == cb["unknown"] - len(flips)

    # serving-class unknown arithmetic (graph-derived, class 3291)
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
    # the eighth-cost selection class 1297036692750860288:0 held 43
    # exclusive unknown keys (head 5b6e77f7 basis); adopting exactly one
    # of them (the k01 WIN) drops its cost-unknown 100 -> 99 and the
    # k01 WIN flips it unknown -> excluded_now (the win-hit mechanism)
    assert serving_rows[str(cls)]["base_status"] == "unknown"
    assert serving_rows[str(cls)]["scen_status"] == "excluded_now"
    assert (serving_rows[str(cls)]["unknown_before"],
            serving_rows[str(cls)]["unknown_after"]) == (100, 99), cls
    assert serving_rows[str(cls)]["adopted_owned_here"] == 1
    out["serving_class_rows"] = serving_rows

    # closure-classes.csv churn (measured, NOT asserted empty: the WIN
    # flip and the LOSS consumption re-rank the closure ladder)
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
    # MEASURED: this single-WIN adoption leaves the closure ladder
    # completely unchanged (no entered/left, no unknown_now churn, no
    # rank churn, and the CSV is byte-identical to the BASE side)
    assert entered == [], entered
    assert left == [], left
    assert unknown_churn == [], unknown_churn
    assert len(rank_churn) == 0, len(rank_churn)
    assert BASE_CLOSURE.read_text() == SCEN_CLOSURE.read_text(), \
        "closure-classes.csv must be byte-identical to the BASE side"
    out["closure_byte_identical_to_base"] = True
    # the flipped classes are not closure-ladder candidates on
    # either side (excluded_now classes never enter the ladder)
    for ci in WIN_OWNER_CLASSES:
        assert ci not in bc and ci not in sc, ci

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
    # MEASURED: the per-root CSV is byte-identical this time (no
    # greedy re-routing anywhere)
    out["per_root_coverage_byte_identical"] = \
        BASE_PERROOT.read_text() == SCEN_PERROOT.read_text()
    assert out["per_root_coverage_byte_identical"] is True
    assert greedy_delta == [], greedy_delta

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
    # MEASURED: the single adopted row is a WIN that sits OUTSIDE the
    # frozen requirement, so NO new baseline s5 resolves
    assert new_resolved == set(), sorted(new_resolved)
    assert WIN_S5_INDEX not in baseline_req
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
    # measured: the WIN row's owner classes are not update8 plan group
    # classes, so the win-hit group set is unchanged
    assert out["win_hit_groups_identical"], \
        "the win-hit group set must be unchanged by this adoption"
    assert len(b_groups) == 25, len(b_groups)

    out["joint_greedy"] = {
        "base": base_sum["joint_greedy"]["greedy_union_size"],
        "scen": scen_sum["joint_greedy"]["greedy_union_size"],
    }
    out["worklist_total"] = {
        "base": base_sum["worklist_total"],
        "scen": scen_sum["worklist_total"],
    }
    # measured: the win-hit flips re-route the joint greedy and shrink
    # the probing worklist
    assert out["joint_greedy"] == {"base": 37398, "scen": 37398}, \
        out["joint_greedy"]
    assert out["worklist_total"] == {"base": 64273, "scen": 64273}, \
        out["worklist_total"]

    # worklist regen pins (UNPUBLISHED per size policy; the BASE side is
    # the published Part SV census json's scen regen pin, the SCEN side
    # is this kit's local regen pin)
    swl = D / "reaudit/output/probe-worklist.csv"
    assert swl.is_file()
    out["worklist_regen_pins"] = {
        "base": BASE_WORKLIST_PIN_SOURCE,
        "scen": {"sha256": sha(swl), "size": swl.stat().st_size},
    }
    assert out["worklist_regen_pins"]["base"]["sha256"] == \
        "2987300a57e3ed1594c5058221e5b81cf24af27447d43f627bd59bae4e65e8eb"
    assert out["worklist_regen_pins"]["base"]["size"] == 3715383
    assert out["worklist_regen_pins"]["scen"]["size"] == 3715383, \
        out["worklist_regen_pins"]["scen"]

    out["verdict"] = {
        "part_declared": True,
        "part": "eighthcost-k01-flip-census",
        "canonical_head_sha256": SCEN_CACHE_SHA_EXPECTED,
        "consumed": ("exactly the single published eighth-cost k01 "
                     "WIN row 1297036692750860288:64"),
        "status_flips": len(flips),
        "status_flip_mechanism": (
            "win-hit (the Part EW/EM mechanism): the single adopted WIN "
            "row k01 (s5 index 91779) flips its three owner classes "
            "2182 (1154117773392084992:0), 2197 (the eighth-cost "
            "serving class 1297036692750860288:0, unknown 100 -> 99) "
            "and 16914 (1152921504675004416:64) "
            "from unknown to excluded_now; no class flips to free_now, "
            "free_now stays 39 (Board-verified both sides), the closure "
            "ladder is byte-identical to BASE (no churn at all), the "
            "per-root coverage is byte-identical, the joint greedy stays "
            "37398 and the probing worklist total stays 64273 (regen "
            "content sha differs from the BASE pin); the single adopted "
            "s5 index 91779 (WIN) sits outside the frozen update8 "
            "baseline requirement (resolved 282 -> 282, remaining_now "
            "31444 -> 31444); the win-hit group set is unchanged (25)"),
        "census_counts_identical_to_published_summaries": True,
        "note": ("declared Part SZ wave E adoption measurement; adopting "
                 "solver-trusted S5 labels flips class-status bookkeeping "
                 "only: no root verdict is consumed, no root freed, no "
                 "root excluded, no coverage claim is made or changed; "
                 "11x11 stays UNKNOWN; no root verdict; nodes are "
                 "bookkeeping"),
    }

    outp = D / "output/census-deltas-eighthcost-k01-adoption.json"
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
