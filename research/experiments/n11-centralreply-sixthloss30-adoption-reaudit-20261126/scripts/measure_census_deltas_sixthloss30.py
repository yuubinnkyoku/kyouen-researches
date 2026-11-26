#!/usr/bin/env python3
"""Part ST adoption measurement: BASE (sixthwin3 head of record
02db5ab3...) vs SCENARIO (sixthloss30 adoption union, dade15780...) census
deltas.

This Part ST is DECLARED: the sixthloss30 canonical LOSS adoption consumes
exactly the 30 unconsumed fifth-resumption resolved exact-LOSS rows
(k09..k43 minus k13/k19/k20/k33/k38) and advances the canonical head of
record from 02db5ab3... (6,801 rows WIN 201 / LOSS 6,600; the Part SQ
adoption head of record) to dade15780... (6,831 rows WIN 201 / LOSS
6,630).  This script MEASURES the census/scheduling delta of that
declared adoption, from published-byte-verbatim local inputs, and
cross-checks the kit's own reaudit refresh outputs:

* SCEN cache must equal BASE cache rows + exactly the 30 increment rows;
* every adopted row must be LOSS, fresh to BASE, and its (lo,hi)/legal/
  nodes/s5_index/serving_class must equal the Part kit's
  increments-manifest.json adopted table (the sixthloss30 SSOT of record,
  schema sixthloss30-adoption-increments-manifest-v1), with the s5_index
  verified against the frozen dependency graph (mask_to_index round trip)
  and the serving class (3077) owning the key at graph time (s4_cost
  membership);
* there are NO loss-ties: the loss_ties table must be empty;
* the refresh status logic is replicated independently (graph s4_status/
  s4_cost + update8 receipts + cache verdicts; free_now candidates are
  cross-checked against the published refresh summaries' Board-verified
  free_now counts instead of re-running the Board) and must reproduce
  the published class status census EXACTLY on both sides
  (BASE 34,405/115/39/390 vs SCEN 34,405/115/39/390:
  unknown/excluded_now/free_now/excluded);
* LOSS-only adoption flips NO class status (the Part EM precedent): the
  flip list must be exactly empty; the serving class 3077 keeps its
  excluded_now status with cost-unknown 91 -> 61 (measured);
* closure-classes.csv churn (entered/left, rank churn) and per-root
  greedy re-routing are measured (NOT asserted empty: LOSS consumption
  re-ranks the closure ladder and the per-root greedy unions; free_now/
  uncovered are asserted unchanged on all 20 roots);
* the update8 refresh fields: all 30 adopted s5 indices sit OUTSIDE the
  frozen baseline requirement (resolved stays 281, remaining_now
  unchanged, win-hit group set unchanged);
* joint greedy and worklist totals are measured against the published
  sixthwin3 dossier reaudit outputs (BASE side pins de205c31/350e269a/
  9c5b2774).

11x11 stays UNKNOWN; nodes are bookkeeping; no root verdict is created
or implied by consuming a LOSS label.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
D = ROOT / "research/experiments/n11-centralreply-sixthloss30-adoption-reaudit-20261126"
B2 = ROOT / "research/experiments/n11-centralreply-sixthwin3-adoption-reaudit-20261126"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
MANIFEST = D / "output/increments-manifest.json"

BASE_CACHE = B2 / "output/merged-exact-s5-chain-plus-sixthwin3-20261126.cache"
SCEN_CACHE = D / "output/merged-exact-s5-chain-plus-sixthloss30-20261126.cache"
INCREMENT = D / "output/increment-sixthloss30-adoption-20261126.cache"
BASE_SUMMARY = B2 / "reaudit/output/refresh-summary.json"
SCEN_SUMMARY = D / "reaudit/output/refresh-summary.json"
BASE_CLOSURE = B2 / "reaudit/output/closure-classes.csv"
SCEN_CLOSURE = D / "reaudit/output/closure-classes.csv"
BASE_PERROOT = B2 / "reaudit/output/per-root-coverage.csv"
SCEN_PERROOT = D / "reaudit/output/per-root-coverage.csv"
BASE_CENSUS_JSON = B2 / "output/census-deltas-sixthwin3-adoption.json"

BASE_CACHE_SHA_EXPECTED = "02db5ab35b8ad71dfd0699217756291c6bc896c78e9fd7c609b5e25177f6b25c"
SCEN_CACHE_SHA_EXPECTED = "dade15780ce6625cc70d93ba77b1560145dd2b9f096a53dce556d2fccf7e312b"
INCREMENT_SHA_EXPECTED = "aa54956f2c4b4466e917f9c13802e630dd110890055b9243da3f44bf184445d6"
BASE_SUMMARY_SHA_EXPECTED = "de205c31e59aeeb22e4d040578d1d0d89ec55a074020d4f3a244815964e4eafd"
BASE_CLOSURE_SHA_EXPECTED = "350e269a9d4e0827274aff7c587cdb389f070eade0ff54c220c7c14f9197bc6d"
BASE_PERROOT_SHA_EXPECTED = "9c5b277429f99157ff2e65323b5912b9ce957f1d2008f8ac8fc1e03b49f91ad1"
# the BASE-side worklist regen pin is the published sixthwin3 dossier
# census json's scen regen pin (the file itself is unpublished per size
# policy)
BASE_WORKLIST_PIN_SOURCE = json.loads(
    BASE_CENSUS_JSON.read_text(encoding="utf-8"))["worklist_regen_pins"]["scen"]
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
MANIFEST_SHA_EXPECTED_CALCULATED = None  # measured, not asserted here

ADOPTED_COUNT = 30
ADOPTED_NODES_TOTAL = 181750115
SERVING_CLASS = 3077


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
    assert (len(base), base_wins, base_loss) == (6801, 201, 6600)
    assert (len(scen), scen_wins, scen_loss) == (6831, 201, 6630)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "sixthloss30-adoption-increments-manifest-v1"
    adopted_table = manifest["adopted_table"]
    assert len(adopted_table) == ADOPTED_COUNT
    assert manifest["base_cache_sha256"] == BASE_CACHE_SHA_EXPECTED
    assert manifest["sha256"]["loss_increment"] == INCREMENT_SHA_EXPECTED
    assert manifest["adopted_nodes_total"] == ADOPTED_NODES_TOTAL
    adopted = {}
    for row in adopted_table:
        key = (row["lo"], row["hi"])
        assert key in incr, f"manifest row not in increment: {key}"
        assert incr[key] == (2, row["nodes"]), (key, incr[key])
        assert scen[key][0] == 2, f"adopted row not LOSS in SCEN: {key}"
        assert key not in base, f"adopted row not fresh to BASE: {key}"
        adopted[key] = row
    assert set(adopted) == keys_inc
    assert manifest["loss_ties"] == []
    assert manifest["win_ids"] == []
    assert len(manifest["loss_ids"]) == ADOPTED_COUNT

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
        assert row["result"] == 2
        assert row["serving_class"] == SERVING_CLASS
        assert row["s5_index"] in s4_cost[row["serving_class"]], key
        owner_classes = [ci for ci in range(len(s4_masks))
                         if row["s5_index"] in s4_cost[ci]]
        assert row["serving_class"] in owner_classes, key
        assert owner_classes == row["owner_classes_graph"], key
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

    # LOSS-only: NO class status may change (the Part EM precedent)
    owners_flat = {}
    for key, ocs in owner_classes.items():
        for ci in ocs:
            owners_flat.setdefault(ci, []).append(key)
    flips = sorted(ci for ci in base_status
                   if base_status[ci] != scen_status[ci])
    out["status_flips"] = flips
    # LOSS-only adoption flips NO class: no win-hit can appear, and no
    # owner class may cross to free_now either (measured: none does)
    assert flips == [], flips
    out["status_flip_count"] = 0
    out["owner_class_count_hist"] = {
        str(n): sum(1 for x in owner_classes.values() if len(x) == n)
        for n in {len(x) for x in owner_classes.values()}}
    assert out["owner_class_count_hist"] == {"2": 2, "3": 28}, \
        out["owner_class_count_hist"]
    out["adopted"] = [
        {"lo": k[0], "hi": k[1], "legal": r["legal"], "nodes": r["nodes"],
         "s5_index": r["s5_index"], "serving_class": r["serving_class"],
         "owner_classes": owner_classes[k], "owner_count": len(owner_classes[k])}
        for k, r in adopted.items()]

    # serving-class unknown arithmetic (graph-derived, single class 3077)
    serving_rows = {}
    cls = SERVING_CLASS
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
    # Part EW flipped 3077 to excluded_now; Part SQ measured 93 -> 91;
    # this Part ST consumes the 30 fifth-resumption LOSS rows (91 -> 61)
    assert serving_rows[str(cls)]["base_status"] == "excluded_now"
    assert serving_rows[str(cls)]["scen_status"] == "excluded_now"
    assert (serving_rows[str(cls)]["unknown_before"],
            serving_rows[str(cls)]["unknown_after"]) == (91, 61), cls
    out["serving_class_rows"] = serving_rows

    # closure-classes.csv churn (measured, NOT asserted empty: LOSS
    # consumption re-ranks the closure ladder)
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
    assert entered == [30325], entered
    assert left == [34205], left
    assert unknown_churn == [], unknown_churn
    # every surviving class keeps its unknown_now and groups_served_count;
    # the ladder re-ranks by exactly +1 for the churned rows
    for ci in set(bc) & set(sc):
        assert bc[ci]["unknown_now"] == sc[ci]["unknown_now"], ci
        assert bc[ci]["groups_served_count"] == sc[ci]["groups_served_count"], ci
    assert len(rank_churn) == 26, len(rank_churn)
    for r in rank_churn:
        assert r["scen"] == r["base"] + 1, r

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
    out["per_root_coverage_byte_identical"] = \
        BASE_PERROOT.read_text() == SCEN_PERROOT.read_text()
    assert out["per_root_coverage_byte_identical"] is False
    assert greedy_delta == [
        {"root": 2, "base": 6133, "scen": 6132},
        {"root": 12, "base": 2842, "scen": 2843},
        {"root": 15, "base": 5991, "scen": 5990},
        {"root": 26, "base": 5230, "scen": 5229},
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
    adopted_indices = {r["s5_index"] for r in adopted.values()}
    expected_new = adopted_indices & baseline_req
    adopted_outside_requirement = sorted(adopted_indices - baseline_req)
    assert base_req <= baseline_req, \
        "base resolved set must sit in the frozen requirement"
    assert new_resolved == expected_new, \
        (sorted(new_resolved), sorted(expected_new))
    assert new_resolved == set(), \
        "all 30 adopted keys must sit outside the frozen requirement"
    assert len(adopted_outside_requirement) == 30, \
        adopted_outside_requirement
    assert set(new_resolved) <= adopted_indices
    assert len(new_resolved) == (
        out["update8_refresh_scen"]["resolved"]
        - out["update8_refresh_base"]["resolved"]), "resolved delta"
    assert out["update8_refresh_scen"]["remaining"] == \
        out["update8_refresh_base"]["remaining"], \
        "LOSS-only adoption must not change remaining_now"
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
    # LOSS-only adoption re-routes the greedy scheduler: the joint greedy
    # union grows (measured scheduling quantity, disclosed, NOT a
    # coverage claim); the probe worklist shrinks by the single
    # worklist-level entry the 30 consumed rows collapse into
    assert out["joint_greedy"] == {"base": 35155, "scen": 36789}, \
        out["joint_greedy"]
    assert out["worklist_total"] == {"base": 64276, "scen": 64275}, \
        out["worklist_total"]

    # worklist regen pins (UNPUBLISHED per size policy; the BASE side is
    # the published sixthwin3 dossier census json regen pin, the SCEN
    # side is this kit's local regen pin)
    swl = D / "reaudit/output/probe-worklist.csv"
    assert swl.is_file()
    out["worklist_regen_pins"] = {
        "base": BASE_WORKLIST_PIN_SOURCE,
        "scen": {"sha256": sha(swl), "size": swl.stat().st_size},
    }
    assert out["worklist_regen_pins"]["base"]["sha256"] == \
        "24301312e1e7cfd904da085723144bbbaef15e272c2d430979410520672dcd33"
    assert out["worklist_regen_pins"]["base"]["size"] == 3715904
    assert out["worklist_regen_pins"]["scen"]["size"] == 3715960, \
        out["worklist_regen_pins"]["scen"]

    out["verdict"] = {
        "part_declared": True,
        "part": "ST",
        "canonical_head_sha256": SCEN_CACHE_SHA_EXPECTED,
        "consumed": "exactly the 30 unconsumed fifth-resumption resolved "
                    "exact-LOSS rows (k09..k43 minus k13/k19/k20/k33 and "
                    "the still-parked k38)",
        "status_flips": 0,
        "status_flip_mechanism":
            "none: LOSS-only adoption flips no status (the Part EM "
            "precedent); the serving class 3077 stays excluded_now with "
            "cost-unknown 91 -> 61; closure ladder churn and per-root "
            "greedy re-routing are scheduling effects only",
        "census_counts_identical_to_published_summaries": True,
        "note": ("declared Part ST adoption measurement; LOSS-only "
                 "adoption flips no root verdict, frees no class, "
                 "excludes no class, changes no coverage claim; 11x11 "
                 "stays UNKNOWN; no root verdict; nodes are bookkeeping"),
    }

    outp = D / "output/census-deltas-sixthloss30-adoption.json"
    outp.write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "base_census": cb, "scen_census": cs,
        "status_flip_count": 0, "flips": flips,
        "serving_class_rows": serving_rows,
        "closure_churn": out["closure_churn"],
        "per_root_greedy_delta": greedy_delta,
        "joint_greedy": out["joint_greedy"],
        "worklist_total": out["worklist_total"],
        "update8_new_resolved": out["update8_new_resolved"],
        "adopted_outside_baseline_requirement_count":
            len(out["adopted_outside_baseline_requirement"]),
        "owner_class_count_hist": out["owner_class_count_hist"],
    }, indent=1))
    print("written:", outp)


if __name__ == "__main__":
    main()
