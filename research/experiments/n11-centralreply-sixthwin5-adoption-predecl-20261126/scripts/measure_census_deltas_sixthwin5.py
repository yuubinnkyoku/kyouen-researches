#!/usr/bin/env python3
"""Predecl dossier measurement: BASE (Part EM canonical 6e49dd84...) vs
SCENARIO (sixthwin5 pre-adoption union, 16a12390...) census deltas.

NOT a Part extractor and NOT an adoption: the sixthwin5 WIN adoption is
not declared, nothing is consumed, the canonical head stays 6e49dd84....
This script only MEASURES, from published-byte-verbatim local inputs,
what the census/scheduling delta of the 5 UNCONSUMED sixth-cost
exclusive-probe exact-WIN rows would be if a future EV-pattern Part
declared their adoption:

* SCEN cache must equal BASE cache rows + exactly the 5 increment rows;
* every adopted row must be WIN, fresh to BASE, and its (lo,hi)/legal/
  nodes/s5_index/serving_class must equal the dossier kit's
  increments-manifest.json adopted table (the sixthwin5 SSOT of record,
  schema sixthwin5-increments-manifest-v1), with the s5_index verified
  against the frozen dependency graph (mask_to_index round trip) and
  the serving class (3077) owning the key at graph time (s4_cost
  membership);
* there are NO win-ties this time (unlike emloss21's f017/ai007/ai040):
  the win_ties table must be empty;
* the refresh status logic is replicated independently (graph s4_status/
  s4_cost + update8 receipts + cache verdicts; free_now candidates are
  cross-checked against the published refresh summaries' Board-verified
  free_now counts instead of re-running the Board) and must reproduce
  the published class status census EXACTLY on both sides
  (BASE 34,417/103/39/390 vs SCEN 34,409/111/39/390:
  unknown/excluded_now/free_now/excluded);
* WIN-only adoption flips classes ONLY by the win-hit mechanism,
  unknown -> excluded_now: the flip list must be exactly the owner
  classes of the adopted keys that were unknown at BASE (machine
  8 classes), every flip must be unknown -> excluded_now, and no class
  may change status otherwise;
* closure-classes.csv churn (rows enter/leave, unknown_now deltas, rank
  churn), per-root coverage (measured byte-identical to BASE here), the
  update8 refresh fields (resolved grows by exactly the adopted keys in
  the frozen baseline requirement, remaining_now unchanged, win-hit
  group set unchanged), joint greedy and worklist totals are measured
  against the published Part EM dossier reaudit outputs (BASE side pins
  7f379b71/68628134/9c5b2774).

11x11 stays UNKNOWN; nodes are bookkeeping; no verdict is created or
consumed here.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
D = ROOT / "research/experiments/n11-centralreply-sixthwin5-adoption-predecl-20261126"
EM = ROOT / "research/experiments/n11-centralreply-emloss21-adoption-predecl-20261126"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
MANIFEST = D / "output/increments-manifest.json"

BASE_CACHE = EM / "output/merged-exact-s5-chain-plus-emloss21-20261126.cache"
SCEN_CACHE = D / "output/merged-exact-s5-chain-plus-sixthwin5-20261126.cache"
INCREMENT = D / "output/increment-sixthwin5-20261126.cache"
BASE_SUMMARY = EM / "reaudit/output/refresh-summary.json"
SCEN_SUMMARY = D / "reaudit/output/refresh-summary.json"
BASE_CLOSURE = EM / "reaudit/output/closure-classes.csv"
SCEN_CLOSURE = D / "reaudit/output/closure-classes.csv"
BASE_PERROOT = EM / "reaudit/output/per-root-coverage.csv"
SCEN_PERROOT = D / "reaudit/output/per-root-coverage.csv"
BASE_CENSUS_JSON = EM / "output/census-deltas-emloss21-predecl.json"

BASE_CACHE_SHA_EXPECTED = "6e49dd841b7bfcb335d86ef2479c95f47ab7acbcf41ace389a8b8eb95c778c9d"
SCEN_CACHE_SHA_EXPECTED = "16a12390c0c3f046f0ae537b2a9940e15661263fc5034ce1b155c138bb9043cd"
INCREMENT_SHA_EXPECTED = "44c16a28f944e255d3968f49a16cc61e06f70269ada833fe976f1607b7d40b03"
BASE_SUMMARY_SHA_EXPECTED = "7f379b718e48330c5acbc3c9c79be3c4fb6d616c4dc7bedfe7691e6ebb225f0b"
BASE_CLOSURE_SHA_EXPECTED = "6862813431dd1abbaba81ac2a720385be394ce774f259b8001ca49630fc4a8e2"
BASE_PERROOT_SHA_EXPECTED = "9c5b277429f99157ff2e65323b5912b9ce957f1d2008f8ac8fc1e03b49f91ad1"
# the BASE-side worklist regen pin is the published Part EM dossier census
# json's scen regen pin (the file itself is unpublished per size policy)
BASE_WORKLIST_PIN = {
    "sha256": "147b62d643ba9039e9e2b64363cec602405bf11210a3aa4cfd9084eb0df3a973",
    "size": 3715963,
    "source": "published Part EM dossier census json scen regen pin "
              "(file unpublished per size policy)"},
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"


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
    assert (len(base), base_wins, base_loss) == (6792, 192, 6600)
    assert (len(scen), scen_wins, scen_loss) == (6797, 197, 6600)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "sixthwin5-increments-manifest-v1"
    adopted_table = manifest["adopted_table"]
    assert len(adopted_table) == 5
    assert manifest["base_cache_sha256"] == BASE_CACHE_SHA_EXPECTED
    assert manifest["sha256"]["win_increment"] == INCREMENT_SHA_EXPECTED
    assert manifest["adopted_nodes_total"] == 45999378
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
    assert serving_rows[str(cls)]["base_status"] == "unknown"
    assert serving_rows[str(cls)]["scen_status"] == "excluded_now"
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

    # per-root coverage: measured byte-identical to BASE for this scenario
    b_text = BASE_PERROOT.read_text()
    s_text = SCEN_PERROOT.read_text()
    assert out["base_per_root"]["sha256"] == BASE_PERROOT_SHA_EXPECTED
    per_root_byte_identical = b_text == s_text
    out["per_root_greedy_delta"] = []
    out["per_root_free_and_uncovered_identical"] = True
    out["per_root_coverage_byte_identical"] = per_root_byte_identical
    if not per_root_byte_identical:
        b_lines, s_lines = b_text.splitlines(), s_text.splitlines()
        assert len(b_lines) == len(s_lines) == 21
        assert b_lines[0].split(",")[:5] == \
            ["first", "role", "thirds", "free_now", "uncovered"]
        for bl, sl in zip(b_lines[1:], s_lines[1:]):
            b_row, s_row = bl.split(","), sl.split(",")
            assert b_row[:5] == s_row[:5], (bl, sl)

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
    # newly resolve.  Machine expectation here: k02 / s5_index 64872.
    baseline_req = set(update8["required_new_s5"])
    adopted_indices = {r["s5_index"] for r in adopted.values()}
    expected_new = adopted_indices & baseline_req
    adopted_outside_requirement = sorted(adopted_indices - baseline_req)
    assert base_req <= baseline_req, \
        "base resolved set must sit in the frozen requirement"
    assert new_resolved == expected_new, \
        (sorted(new_resolved), sorted(expected_new))
    assert set(new_resolved) <= adopted_indices, \
        "only adopted keys may newly resolve"
    assert len(new_resolved) == (
        out["update8_refresh_scen"]["resolved"]
        - out["update8_refresh_base"]["resolved"]), "resolved delta"
    assert out["update8_refresh_scen"]["remaining"] == \
        out["update8_refresh_base"]["remaining"], \
        "WIN-only adoption must not change remaining_now"
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
        "the win-hit group set must be unchanged by this scenario"

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
        "joint greedy must be unchanged by this scenario (measured)"

    # worklist regen pins (UNPUBLISHED per size policy; the BASE side is
    # the published Part EM dossier census json regen pin, the SCEN side
    # is this kit's local regen pin)
    swl = D / "reaudit/output/probe-worklist.csv"
    assert swl.is_file()
    out["worklist_regen_pins"] = {
        "base": BASE_WORKLIST_PIN,
        "scen": {"sha256": sha(swl), "size": swl.stat().st_size},
    }

    out["verdict"] = {
        "part_declared": False,
        "canonical_head_sha256": BASE_CACHE_SHA_EXPECTED,
        "consumed": "NOTHING",
        "status_flips": len(flips),
        "status_flip_mechanism":
            "unknown -> excluded_now only, win-hit; exactly the owner "
            "classes of the 5 adopted WIN keys that were unknown at BASE",
        "census_counts_identical_to_published_summaries": True,
        "note": ("scenario measurement only; WIN-only adoption flips no "
                 "root verdict, frees no class, changes no coverage "
                 "claim; 11x11 stays UNKNOWN; no root verdict; nodes are "
                 "bookkeeping"),
    }

    outp = D / "output/census-deltas-sixthwin5-predecl.json"
    outp.write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "base_census": cb, "scen_census": cs,
        "status_flip_count": len(flips), "flips": flips,
        "serving_class_rows": serving_rows,
        "closure_churn": out["closure_churn"],
        "joint_greedy": out["joint_greedy"],
        "worklist_total": out["worklist_total"],
        "update8_new_resolved": out["update8_new_resolved"],
        "per_root_coverage_byte_identical": per_root_byte_identical,
    }, indent=1))
    print("written:", outp)


if __name__ == "__main__":
    main()
