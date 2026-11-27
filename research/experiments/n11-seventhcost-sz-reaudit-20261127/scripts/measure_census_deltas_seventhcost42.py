#!/usr/bin/env python3
"""Part SZ wave E adoption measurement: BASE (sixthlossk38 head of
record 42dbb58f...) vs SCENARIO (seventh-cost 42-row adoption union,
5b6e77f7...) census deltas.

This Part SZ wave E is DECLARED (pre-registered in the Part SZ wave A
declaration and restated in the completion log): the seventh-cost
canonical adoption consumes exactly the 42 published seventh-cost
batch rows (41 LOSS k01..k42 minus k05 + the single WIN k05
1152921504607932416:536870912; SW/SX C++-gated, SY third-impl
corroborated) and advances the canonical head of record from
42dbb58f... (6,832 rows WIN 201 / LOSS 6,631; the Part SV adoption
head of record) to 5b6e77f7... (6,874 rows WIN 202 / LOSS 6,672).
This script is a disclosed structural adaptation of the Part SV
measurer (fresh 42-row expectations); it MEASURES the census/
scheduling delta of that declared adoption, from published-byte-
verbatim local inputs, and cross-checks the wave E reaudit refresh
outputs (kit n11-seventhcost-sz-reaudit-20261127, byte-clone refresh
of the published Part SV refresh fd2e799e..., three byte-identical
determinism runs):

* SCEN cache must equal BASE cache rows + exactly the 42 increment
  rows; every adopted row is fresh to BASE and matches the increment
  verdict/nodes exactly;
* the adoption manifest (seventhcost42-adoption-manifest-v1) pins:
  base head 42dbb58f, increment 959ae2dd, adopted 42 rows WIN 1 /
  LOSS 41, nodes_total 227,552,924, freshness 42, WIN-LOSS conflict 0,
  duplicate 0, quarantined 0, noncanonical 0, frozen pins
  (graph 54f9c364 / quarantine 81d23160 / policy 78655e94 / merger
  90711961);
* the refresh status logic is replicated independently and must
  reproduce the published class status census EXACTLY on both sides
  (BASE 34,405/115/39/390 unknown/excluded_now/free_now/excluded;
  SCEN 34,403/117/39/390);
* unlike the LOSS-only predecessors this adoption contains ONE WIN
  row, so class-status flips are MEASURED, not asserted empty: the
  measured flip list is exactly the two owner classes of the WIN key
  (s5 index 114754): class 3291 (the seventh-cost serving class,
  mask 1306043891938492416:0, unknown 100 -> 58, all 42 adopted rows
  owned here, status unknown -> excluded_now) and class 25463 (mask
  1152921504607932416:0, unknown -> excluded_now) - the Part EW/EM
  win-hit mechanism, first WIN-side flip since the WIN-side adoption
  series;
* no class flips to free_now and no free_now class is lost (39 -> 39,
  Board-verified both sides);
* closure-classes.csv churn and per-root greedy re-routing are
  MEASURED (non-empty this time: the ladder re-ranks, 45 classes change
  rank, 2 classes change unknown_now, entered/left measured);
* the update8 refresh fields: exactly one adopted s5 index
  (111999, LOSS row 1306044991450120192:0) sits INSIDE the frozen
  baseline requirement (resolved 281 -> 282, remaining_now
  31,445 -> 31,444); the WIN key sits outside the requirement; the
  win-hit group set is unchanged (25 groups);
* joint greedy and worklist totals are measured against the published
  Part SV reaudit outputs (BASE side pins 451c1e36/0eb19c89/1828d7f7):
  joint greedy 36,789 -> 37,398 (re-route), worklist 64,275 -> 64,273.

11x11 stays UNKNOWN; nodes are bookkeeping; no root verdict is
created or implied by adopting S5 labels; the WIN-side flips are
class-status bookkeeping inside the scheduling machinery and exclude
no root, free no root, and consume no root verdict.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
D = ROOT / "research/experiments/n11-seventhcost-sz-reaudit-20261127"
SV = ROOT / "research/experiments/n11-centralreply-sixthlossk38-adoption-reaudit-20261126"
SZ = ROOT / "research/experiments/n11-seventhcost-sz-adoption-20261127"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
MANIFEST = SZ / "output/adoption-manifest.json"
MERGER = SV / "scripts/s5_union_merge.py"

BASE_CACHE = SV / "output/merged-exact-s5-chain-plus-sixthlossk38-20261126.cache"
SCEN_CACHE = SZ / "output/merged/merged-exact-s5-chain-plus-seventhcost42-20261127.cache"
INCREMENT = SZ / "output/increment-seventhcost42-adoption-20261127.cache"
BASE_SUMMARY = SV / "reaudit/output/refresh-summary.json"
SCEN_SUMMARY = D / "reaudit/output/refresh-summary.json"
BASE_CLOSURE = SV / "reaudit/output/closure-classes.csv"
SCEN_CLOSURE = D / "reaudit/output/closure-classes.csv"
BASE_PERROOT = SV / "reaudit/output/per-root-coverage.csv"
SCEN_PERROOT = D / "reaudit/output/per-root-coverage.csv"
BASE_CENSUS_JSON = SV / "output/census-deltas-sixthlossk38-adoption.json"

BASE_CACHE_SHA_EXPECTED = "42dbb58ffe8dd02a81f4a92993d08e3fbebdaeb4b4f7bf33e142120ff055bdc4"
SCEN_CACHE_SHA_EXPECTED = "5b6e77f7d7832d4ce84cb1f080a93e066eb052dcf8b817e5d560f95499fcdde2"
INCREMENT_SHA_EXPECTED = "959ae2dd249a1d78be1f67f68640a4371fa13ca2e4b31d3b39bb44cb05519f1f"
MANIFEST_SHA_EXPECTED = "14ef4fc23cf6649b47fb67a9f544626ec3a4637d08c5e2b236e7906cbe0b9f82"
BASE_SUMMARY_SHA_EXPECTED = "451c1e3647b2a4431cb57a81c5c4b372ffd111638ef2f77bf95a295d2a36e19d"
BASE_CLOSURE_SHA_EXPECTED = "0eb19c8955e92c3e96c9a7d40f84a4d2c274489fb03b8d1266b850995ea818e9"
BASE_PERROOT_SHA_EXPECTED = "1828d7f764015a2d319dd56fc19de666fef49a30843b4a6ec37187d14370f849"
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_WORKLIST_PIN_SOURCE = json.loads(
    BASE_CENSUS_JSON.read_text(encoding="utf-8"))["worklist_regen_pins"]["scen"]

ADOPTED_COUNT = 42
ADOPTED_NODES_TOTAL = 227552924
SERVING_CLASS = 3291
SERVING_CLASS_MASK = (1306043891938492416, 0)
WIN_KEY = (1152921504607932416, 536870912)
WIN_S5_INDEX = 114754
WIN_OWNER_CLASSES = [3291, 25463]
EXPECTED_FLIPS = [3291, 25463]
NEWLY_RESOLVED_BASELINE_INDEX = 111999
NEWLY_RESOLVED_BASELINE_KEY = (1306044991450120192, 0)


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
    assert (len(base), base_wins, base_loss) == (6832, 201, 6631)
    assert (len(scen), scen_wins, scen_loss) == (6874, 202, 6672)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "seventhcost42-adoption-manifest-v1"
    assert manifest["part"] == "SZ"
    assert manifest["base_head"]["sha256"] == BASE_CACHE_SHA_EXPECTED
    assert (manifest["base_head"]["rows"], manifest["base_head"]["win"],
            manifest["base_head"]["loss"]) == (6832, 201, 6631)
    assert manifest["increment"]["sha256"] == INCREMENT_SHA_EXPECTED
    adopted = manifest["adopted"]
    assert (adopted["rows"], adopted["win"], adopted["loss"]) == (42, 1, 41)
    assert adopted["nodes_total"] == ADOPTED_NODES_TOTAL
    assert adopted["freshness"] == ADOPTED_COUNT
    assert adopted["win_loss_conflicts"] == 0
    assert adopted["duplicates"] == 0
    assert adopted["quarantined"] == 0
    assert adopted["noncanonical"] == 0
    assert manifest["frozen_pins"] == {
        "quarantine_sha256": "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9",
        "policy_sha256": "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2",
        "dependency_graph_sha256": "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b",
        "merger_sha256": "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a",
    }

    # adopted rows derived from the increment itself (the SZ manifest has
    # no per-row table; per-row fields are graph-derived here)
    assert len(incr) == ADOPTED_COUNT
    win_keys = [k for k, v in incr.items() if v[0] == 1]
    loss_keys = [k for k, v in incr.items() if v[0] == 2]
    assert len(win_keys) == 1 and len(loss_keys) == 41
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
    assert out["owner_class_count_hist"] == {"1": 1, "2": 2, "3": 38, "4": 1}, \
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
    # the seventh-cost selection class 1306043891938492416:0 held 42
    # exclusive unknown keys (head 42dbb58f basis); adopting all 42
    # (41 LOSS + the k05 WIN) drops its cost-unknown 100 -> 58 and the
    # k05 WIN flips it unknown -> excluded_now (the win-hit mechanism)
    assert serving_rows[str(cls)]["base_status"] == "unknown"
    assert serving_rows[str(cls)]["scen_status"] == "excluded_now"
    assert (serving_rows[str(cls)]["unknown_before"],
            serving_rows[str(cls)]["unknown_after"]) == (100, 58), cls
    assert serving_rows[str(cls)]["adopted_owned_here"] == 42
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
    assert entered == [1579], entered
    assert left == [13970], left
    assert unknown_churn == [
        {"class_index": 25462, "base": 97, "scen": 96},
        {"class_index": 25489, "base": 104, "scen": 103},
    ], unknown_churn
    assert len(rank_churn) == 45, len(rank_churn)
    # the two flipped classes are not closure-ladder candidates on
    # either side (excluded_now classes never enter the ladder)
    assert SERVING_CLASS not in bc and SERVING_CLASS not in sc
    assert 25463 not in bc and 25463 not in sc

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
    # measured: the per-root CSV is NOT byte-identical this time (the
    # greedy re-routing on roots 14/15 changes individual_greedy_union)
    out["per_root_coverage_byte_identical"] = \
        BASE_PERROOT.read_text() == SCEN_PERROOT.read_text()
    assert out["per_root_coverage_byte_identical"] is False
    assert greedy_delta == [
        {"root": 14, "base": 4538, "scen": 4537},
        {"root": 15, "base": 5990, "scen": 5977},
    ], greedy_delta

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
    assert new_resolved == {NEWLY_RESOLVED_BASELINE_INDEX}, sorted(new_resolved)
    assert adopted_indices[NEWLY_RESOLVED_BASELINE_KEY] == \
        NEWLY_RESOLVED_BASELINE_INDEX
    # the newly resolved baseline index is a LOSS row; the WIN key sits
    # OUTSIDE the frozen requirement (measured)
    assert incr[NEWLY_RESOLVED_BASELINE_KEY][0] == 2
    assert WIN_S5_INDEX not in baseline_req
    adopted_outside_requirement = sorted(adopted_idx - baseline_req)
    assert len(adopted_outside_requirement) == ADOPTED_COUNT - 1
    assert len(new_resolved) == (
        out["update8_refresh_scen"]["resolved"]
        - out["update8_refresh_base"]["resolved"]), "resolved delta"
    out["update8_refresh_base"]["resolved_list_len"] = len(base_req)
    out["update8_refresh_scen"]["resolved_list_len"] = len(scen_req)
    assert out["update8_refresh_base"]["resolved"] == 281
    assert out["update8_refresh_scen"]["resolved"] == 282
    assert out["update8_refresh_base"]["remaining"] == 31445
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
    assert out["joint_greedy"] == {"base": 36789, "scen": 37398}, \
        out["joint_greedy"]
    assert out["worklist_total"] == {"base": 64275, "scen": 64273}, \
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
        "b946ed062e84d0a14f84dd4db167d1b051bb1459bc3a8ff738eeda3d9c6d8c26"
    assert out["worklist_regen_pins"]["base"]["size"] == 3715960
    assert out["worklist_regen_pins"]["scen"]["size"] == 3715383, \
        out["worklist_regen_pins"]["scen"]

    out["verdict"] = {
        "part_declared": True,
        "part": "SZ-wave-E",
        "canonical_head_sha256": SCEN_CACHE_SHA_EXPECTED,
        "consumed": ("exactly the 42 published seventh-cost rows "
                     "(41 LOSS k01..k42 minus k05 + 1 WIN k05 "
                     "1152921504607932416:536870912)"),
        "status_flips": len(flips),
        "status_flip_mechanism": (
            "win-hit (the Part EW/EM mechanism): the single adopted WIN "
            "row k05 (s5 index 114754) flips its two owner classes "
            "3291 (the seventh-cost serving class 1306043891938492416:0, "
            "unknown 100 -> 58, all 42 adopted rows owned here) and 25463 "
            "(1152921504607932416:0) from unknown to excluded_now; no "
            "class flips to free_now, free_now stays 39 (Board-verified "
            "both sides), the closure ladder re-ranks (45 rank churn, 2 "
            "unknown_now churn, entered 1579 / left 13970), the joint "
            "greedy re-routes 36789 -> 37398 and the probing worklist "
            "shrinks 64275 -> 64273; exactly one adopted LOSS row "
            "(1306044991450120192:0, s5 index 111999) sits inside the "
            "frozen update8 baseline requirement (resolved 281 -> 282, "
            "remaining_now 31445 -> 31444); the WIN key sits outside the "
            "requirement and the win-hit group set is unchanged (25)"),
        "census_counts_identical_to_published_summaries": True,
        "note": ("declared Part SZ wave E adoption measurement; adopting "
                 "solver-trusted S5 labels flips class-status bookkeeping "
                 "only: no root verdict is consumed, no root freed, no "
                 "root excluded, no coverage claim is made or changed; "
                 "11x11 stays UNKNOWN; no root verdict; nodes are "
                 "bookkeeping"),
    }

    outp = D / "output/census-deltas-seventhcost42-adoption.json"
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
