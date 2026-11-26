#!/usr/bin/env python3
"""Part SQ adoption measurement: BASE (sixthwin2 head of record
cc3694bb...) vs SCENARIO (sixthwin3 adoption union, 02db5ab3...) census
deltas.

This Part SQ is DECLARED: the sixthwin3 canonical WIN adoption consumes
exactly the 2 parked4rest2 L50M ladder exact-WIN rows k20/k33 and
advances the canonical head of record from cc3694bb... (6,799 rows WIN
199 / LOSS 6,600; the Part SP adoption head of record) to 02db5ab3...
(6,801 rows WIN 201 / LOSS 6,600).  This script MEASURES the
census/scheduling delta of that declared adoption, from published-byte-
verbatim local inputs, and cross-checks the kit's own reaudit refresh
outputs:

* SCEN cache must equal BASE cache rows + exactly the 2 increment rows;
* every adopted row must be WIN, fresh to BASE, and its (lo,hi)/legal/
  nodes/s5_index/serving_class must equal the Part kit's
  increments-manifest.json adopted table (the sixthwin3 SSOT of record,
  schema sixthwin3-adoption-increments-manifest-v1), with the s5_index
  verified against the frozen dependency graph (mask_to_index round
  trip) and the serving class (3077) owning the key at graph time
  (s4_cost membership);
* there are NO win-ties: the win_ties table must be empty;
* the refresh status logic is replicated independently (graph s4_status/
  s4_cost + update8 receipts + cache verdicts; free_now candidates are
  cross-checked against the published refresh summaries' Board-verified
  free_now counts instead of re-running the Board) and must reproduce
  the published class status census EXACTLY on both sides
  (BASE 34,407/113/39/390 vs SCEN 34,405/115/39/390:
  unknown/excluded_now/free_now/excluded);
* WIN-only adoption flips classes ONLY by the win-hit mechanism,
  unknown -> excluded_now: the flip list must be exactly the owner
  classes of the adopted keys that were unknown at BASE (machine
  2 classes: 3054 owner of k20, 2402 owner of k33), every flip must be
  unknown -> excluded_now, and no class may change status otherwise;
  the serving class 3077 was already flipped excluded_now by Part EW
  and only its cost-unknown count changes (93 -> 91);
* closure-classes.csv churn (rows enter/leave, unknown_now deltas, rank
  churn; measured empty here), per-root coverage (measured
  byte-identical to BASE here), the update8 refresh fields (both
  adopted s5 indices 97791/111843 sit OUTSIDE the frozen baseline
  requirement: resolved stays 281, remaining_now unchanged, win-hit
  group set unchanged), joint greedy and worklist totals are measured
  against the published sixthwin2 dossier reaudit outputs (BASE side
  pins 7a500a03/350e269a/9c5b2774).

11x11 stays UNKNOWN; nodes are bookkeeping; no root verdict is created
or implied by consuming a WIN label.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
D = ROOT / "research/experiments/n11-centralreply-sixthwin3-adoption-reaudit-20261126"
B2 = ROOT / "research/experiments/n11-centralreply-sixthwin2-adoption-reaudit-20261126"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
MANIFEST = D / "output/increments-manifest.json"

BASE_CACHE = B2 / "output/merged-exact-s5-chain-plus-sixthwin2-20261126.cache"
SCEN_CACHE = D / "output/merged-exact-s5-chain-plus-sixthwin3-20261126.cache"
INCREMENT = D / "output/increment-sixthwin3-adoption-20261126.cache"
BASE_SUMMARY = B2 / "reaudit/output/refresh-summary.json"
SCEN_SUMMARY = D / "reaudit/output/refresh-summary.json"
BASE_CLOSURE = B2 / "reaudit/output/closure-classes.csv"
SCEN_CLOSURE = D / "reaudit/output/closure-classes.csv"
BASE_PERROOT = B2 / "reaudit/output/per-root-coverage.csv"
SCEN_PERROOT = D / "reaudit/output/per-root-coverage.csv"
BASE_CENSUS_JSON = B2 / "output/census-deltas-sixthwin2-adoption.json"

BASE_CACHE_SHA_EXPECTED = "cc3694bbe871ccf27bdf4dbcf5e93586da440164fd75c02c15dc2a0ae46d11b8"
SCEN_CACHE_SHA_EXPECTED = "02db5ab35b8ad71dfd0699217756291c6bc896c78e9fd7c609b5e25177f6b25c"
INCREMENT_SHA_EXPECTED = "47f7dfb02489a960184b5c83bd3ed36e33936bd40067c7cc97299ab1f740ecc6"
BASE_SUMMARY_SHA_EXPECTED = "7a500a032f997307defb37f28ce65f93ce935f2feca9ca6281c5474775ef4bc7"
BASE_CLOSURE_SHA_EXPECTED = "350e269a9d4e0827274aff7c587cdb389f070eade0ff54c220c7c14f9197bc6d"
BASE_PERROOT_SHA_EXPECTED = "9c5b277429f99157ff2e65323b5912b9ce957f1d2008f8ac8fc1e03b49f91ad1"
# the BASE-side worklist regen pin is the published sixthwin2 dossier
# census json's scen regen pin (the file itself is unpublished per size
# policy)
BASE_WORKLIST_PIN_SOURCE = json.loads(
    BASE_CENSUS_JSON.read_text(encoding="utf-8"))["worklist_regen_pins"]["scen"]
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
MANIFEST_SHA_EXPECTED_CALCULATED = None  # measured, not asserted here


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
    assert out["base_cache"]["sha256"] == BASE_CACHE_SHA_EXPECTED
    assert out["scen_cache"]["sha256"] == SCEN_CACHE_SHA_EXPECTED
    assert out["increment"]["sha256"] == INCREMENT_SHA_EXPECTED
    assert sha(D / "scripts/s5_union_merge.py") == MERGER_SHA_EXPECTED
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
    assert (len(base), base_wins, base_loss) == (6799, 199, 6600)
    assert (len(scen), scen_wins, scen_loss) == (6801, 201, 6600)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "sixthwin3-adoption-increments-manifest-v1"
    adopted_table = manifest["adopted_table"]
    assert len(adopted_table) == 2
    assert manifest["base_cache_sha256"] == BASE_CACHE_SHA_EXPECTED
    assert manifest["sha256"]["win_increment"] == INCREMENT_SHA_EXPECTED
    assert manifest["adopted_nodes_total"] == 32038980
    adopted = {}
    for row in adopted_table:
        key = (row["lo"], row["hi"])
        assert key in incr, f"manifest row not in increment: {key}"
        assert incr[key] == (1, row["nodes"]), (key, incr[key])
        assert scen[key][0] == 1, f"adopted row not WIN in SCEN: {key}"
        assert key not in base, f"adopted row not fresh to BASE: {key}"
        adopted[key] = row
    assert set(adopted) == keys_inc
    assert manifest["win_ties"] == []
    assert manifest["loss_ids"] == []

    # graph
    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s4_masks = g["s4_masks"]
    s4_status = g["s4_status"]
    s4_cost = g["s4_cost"]
    s5_masks = g["s5_masks"]
    mask_to_index = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}

    update8 = json.loads(UPDATE8.read_text(encoding="utf-8"))
    receipt = {int(k): int(v) for k, v in update8["resolved_s5_verdicts"].items()}

    # manifest s5_index round trip + serving-class ownership at graph time
    for key, row in adopted.items():
        assert mask_to_index.get(key) == row["s5_index"], (key, row)
        assert row["result"] == 1
        assert row["serving_class"] == 3077
        assert row["s5_index"] in s4_cost[row["serving_class"]], key
        owner_classes = [ci for ci in range(len(s4_masks))
                         if row["s5_index"] in s4_cost[ci]]
        assert row["serving_class"] in owner_classes, key
        assert owner_classes == row["owner_classes_graph"], key
    # owner classes of every adopted key (full membership, graph-derived)
    owner_classes = {}
    for key, row in adopted.items():
        owner_classes[key] = [ci for ci in range(len(s4_masks))
                              if row["s5_index"] in s4_cost[ci]]

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
                status[i] = "free_now_candidate"
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

    def counts_from(status):
        c = {"unknown": 0, "excluded_now": 0, "free_now": 0, "excluded": 0}
        for v in status.values():
            if v == "free_now_candidate":
                c["free_now"] += 1
            else:
                c[v] += 1
        return c

    cb, cs = counts_from(base_status), counts_from(scen_status)
    out["census_recount_base"] = cb
    out["census_recount_scen"] = cs
    assert cb == base_sum["class_status_counts"], \
        (cb, base_sum["class_status_counts"])
    assert cs == scen_sum["class_status_counts"], \
        (cs, scen_sum["class_status_counts"])

    # WIN-only: the ONLY allowed status change is unknown -> excluded_now,
    # and exactly for the owner classes of the adopted keys
    owners_flat = {}
    for key, ocs in owner_classes.items():
        for ci in ocs:
            owners_flat.setdefault(ci, []).append(key)
    expected_flips = {ci for ci in owners_flat if base_status[ci] == "unknown"}
    flips = sorted(ci for ci in base_status
                   if base_status[ci] != scen_status[ci])
    out["status_flips"] = flips
    assert set(flips) == expected_flips, \
        (sorted(flips), sorted(expected_flips))
    assert flips == [2402, 3054], flips
    for ci in flips:
        assert base_status[ci] == "unknown", ci
        assert scen_status[ci] == "excluded_now", ci
        assert ci in owners_flat, ci
    for ci in owners_flat:
        if base_status[ci] != "unknown":
            assert base_status[ci] == scen_status[ci], ci
    out["status_flip_count"] = len(flips)
    out["owner_class_count_hist"] = {
        str(n): sum(1 for x in owner_classes.values() if len(x) == n)
        for n in {len(x) for x in owner_classes.values()}}
    assert out["owner_class_count_hist"] == {"3": 2}, \
        out["owner_class_count_hist"]
    out["adopted"] = [
        {"lo": k[0], "hi": k[1], "legal": r["legal"], "nodes": r["nodes"],
         "s5_index": r["s5_index"], "serving_class": r["serving_class"],
         "owner_classes": owner_classes[k], "owner_count": len(owner_classes[k])}
        for k, r in adopted.items()]

    # serving-class unknown arithmetic (graph-derived, single class 3077)
    serving_rows = {}
    cls = 3077
    cost = s4_cost[cls]
    unknown_base = [j for j in cost
                    if tuple(s5_masks[j]) not in base and j not in receipt]
    unknown_scen = [j for j in cost
                    if tuple(s5_masks[j]) not in scen and j not in receipt]
    serving_rows[str(cls)] = {
        "base_status": base_status[cls],
        "scen_status": scen_status[cls],
        "unknown_before": len(unknown_base),
        "unknown_after": len(unknown_scen),
        "adopted_owned_here": sum(1 for k, r in adopted.items()
                                  if r["serving_class"] == cls
                                  and r["s5_index"] in cost),
    }
    assert (serving_rows[str(cls)]["unknown_before"]
            - serving_rows[str(cls)]["unknown_after"]
            == serving_rows[str(cls)]["adopted_owned_here"]), cls
    # Part EW already flipped 3077 to excluded_now; Part SP measured its
    # cost-unknown 95 -> 93; the SQ adoption only changes it further
    # (93 -> 91, measured)
    assert serving_rows[str(cls)]["base_status"] == "excluded_now"
    assert serving_rows[str(cls)]["scen_status"] == "excluded_now"
    assert (serving_rows[str(cls)]["unknown_before"],
            serving_rows[str(cls)]["unknown_after"]) == (93, 91), cls
    out["serving_class_rows"] = serving_rows

    # closure-classes.csv churn
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
    assert entered == left == unknown_churn == rank_churn == []

    # per-root coverage: measured byte-identical to BASE for this scenario
    b_text = BASE_PERROOT.read_text()
    s_text = SCEN_PERROOT.read_text()
    assert out["base_per_root"]["sha256"] == BASE_PERROOT_SHA_EXPECTED
    per_root_byte_identical = b_text == s_text
    out["per_root_greedy_delta"] = []
    out["per_root_free_and_uncovered_identical"] = True
    out["per_root_coverage_byte_identical"] = per_root_byte_identical
    assert per_root_byte_identical

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
    # the frozen update8 baseline requirement is replayed from the
    # published plan file (required_new_s5), exactly as the refresh fork
    # does: only the adopted keys INSIDE that frozen requirement can
    # newly resolve.  Machine expectation here: BOTH adopted keys sit
    # OUTSIDE the frozen baseline requirement (k20 s5_index 111843,
    # k33 s5_index 97791), so nothing newly resolves.
    baseline_req = set(update8["required_new_s5"])
    adopted_indices = {r["s5_index"] for r in adopted.values()}
    expected_new = adopted_indices & baseline_req
    adopted_outside_requirement = sorted(adopted_indices - baseline_req)
    assert base_req <= baseline_req, \
        "base resolved set must sit in the frozen requirement"
    assert new_resolved == expected_new, \
        (sorted(new_resolved), sorted(expected_new))
    assert new_resolved == set(), \
        "both adopted keys must sit outside the frozen requirement"
    assert adopted_outside_requirement == [97791, 111843], \
        adopted_outside_requirement
    assert set(new_resolved) <= adopted_indices, \
        "only adopted keys may newly resolve"
    assert len(new_resolved) == (
        out["update8_refresh_scen"]["resolved"]
        - out["update8_refresh_base"]["resolved"]), "resolved delta"
    assert out["update8_refresh_scen"]["remaining"] == \
        out["update8_refresh_base"]["remaining"], \
        "WIN-only adoption must not change remaining_now"
    out["update8_refresh_base"]["resolved_list_len"] = len(base_req)
    out["update8_refresh_scen"]["resolved_list_len"] = len(scen_req)
    assert out["update8_refresh_base"]["resolved"] == 281
    assert out["update8_refresh_scen"]["resolved"] == 281
    assert out["update8_refresh_base"]["remaining"] == 31445
    assert out["update8_refresh_scen"]["remaining"] == 31445
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
    # every adopted s5_index in a baseline-requirement group sits in a
    # group that was ALREADY a win-hit group at BASE (no new group appears)
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
    assert out["worklist_total"]["base"] - out["worklist_total"]["scen"] \
        == len(new_resolved), \
        "each newly resolved in-requirement key leaves the probe worklist"
    assert out["joint_greedy"]["base"] == out["joint_greedy"]["scen"], \
        "joint greedy must be unchanged by this adoption (measured)"
    assert out["joint_greedy"] == {"base": 35155, "scen": 35155}, \
        out["joint_greedy"]
    assert out["worklist_total"] == {"base": 64276, "scen": 64276}, \
        out["worklist_total"]

    # worklist regen pins (UNPUBLISHED per size policy; the BASE side is
    # the published sixthwin2 dossier census json regen pin, the SCEN
    # side is this kit's local regen pin)
    swl = D / "reaudit/output/probe-worklist.csv"
    assert swl.is_file()
    out["worklist_regen_pins"] = {
        "base": BASE_WORKLIST_PIN_SOURCE,
        "scen": {"sha256": sha(swl), "size": swl.stat().st_size},
    }
    assert out["worklist_regen_pins"]["base"]["sha256"] == \
        "0818da81ba01259945d7fb0051b07221582cd4dc68d55d9edb61aa447e4628ac"
    assert out["worklist_regen_pins"]["base"]["size"] == 3715904
    assert out["worklist_regen_pins"]["scen"]["size"] == 3715904, \
        out["worklist_regen_pins"]["scen"]["size"]

    out["verdict"] = {
        "part_declared": True,
        "part": "SQ",
        "canonical_head_sha256": SCEN_CACHE_SHA_EXPECTED,
        "consumed": "exactly the 2 parked4rest2 L50M ladder exact-WIN rows "
                    "k20 (10376293541461626880:33619968) and k33 "
                    "(12682136550675320832:65536)",
        "status_flips": len(flips),
        "status_flip_mechanism":
            "unknown -> excluded_now only, win-hit; exactly the owner "
            "classes of the 2 adopted WIN keys that were unknown at BASE "
            "(3054 owner of k20, 2402 owner of k33); serving class 3077 "
            "stays excluded_now (Part EW) with cost-unknown 93 -> 91",
        "census_counts_identical_to_published_summaries": True,
        "note": ("declared Part SQ adoption measurement; WIN-only "
                 "adoption flips no root verdict, frees no class, "
                 "changes no coverage claim; 11x11 stays UNKNOWN; no "
                 "root verdict; nodes are bookkeeping"),
    }

    outp = D / "output/census-deltas-sixthwin3-adoption.json"
    outp.write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "base_census": cb, "scen_census": cs,
        "status_flip_count": len(flips), "flips": flips,
        "serving_class_rows": serving_rows,
        "closure_churn": out["closure_churn"],
        "joint_greedy": out["joint_greedy"],
        "worklist_total": out["worklist_total"],
        "update8_new_resolved": out["update8_new_resolved"],
        "adopted_outside_baseline_requirement":
            out["adopted_outside_baseline_requirement"],
        "per_root_coverage_byte_identical": per_root_byte_identical,
    }, indent=1))
    print("written:", outp)


if __name__ == "__main__":
    main()
