#!/usr/bin/env python3
"""Predecl dossier measurement: BASE (Part EV canonical 63f33c4f...) vs
SCENARIO (emloss21 pre-adoption union, 6e49dd84...) census deltas.

NOT a Part extractor and NOT an adoption: the emloss21 loss adoption is
not declared, nothing is consumed, the canonical head stays 63f33c4f....
This script only MEASURES, from published-byte-verbatim local inputs,
what the census/scheduling delta of the 21 UNCONSUMED closure-batch
exact-LOSS rows would be if a future EM-pattern Part declared their
adoption:

* SCEN cache must equal BASE cache rows + exactly the 21 increment rows;
* every adopted row must be LOSS, fresh to BASE, and its (lo,hi)/legal/
  nodes/s5_index/serving_class must equal the dossier kit's
  increments-manifest.json adopted table (the emloss21 SSOT of record,
  schema emloss21-increments-manifest-v1), with the s5_index verified
  against the frozen dependency graph (mask_to_index round trip) and
  the serving class owning the key at graph time (s4_cost membership);
* the 3 win-tie rows (f017/ai007/ai040, consumed by Parts EV/EU) must
  sit in BASE as WIN with identical nodes (regression ties) and must
  be absent from the increment and from SCEN's added key set;
* the refresh status logic is replicated independently (graph s4_status/
  s4_cost + update8 receipts + cache verdicts; free_now candidates are
  cross-checked against the published refresh summaries' Board-verified
  free_now counts instead of re-running the Board) and must reproduce
  the published class status census EXACTLY on both sides
  (BASE 34,417/103/39/390 vs SCEN 34,417/103/39/390:
  unknown/excluded_now/free_now/excluded);
* LOSS-only adoption flips NO class status: the status flip list must be
  EMPTY (no unknown -> free_now/excluded_now transition, no regression),
  and every owner class of an adopted key keeps its BASE status;
* closure-classes.csv churn (rows enter/leave, unknown_now deltas, rank
  churn), per-root coverage, update8 refresh fields, joint greedy and
  worklist totals are measured against the published Part EV dossier
  reaudit outputs (BASE side pins 1fafd081/6ba51faa/d9eee976).

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
D = ROOT / "research/experiments/n11-centralreply-emloss21-adoption-predecl-20261126"
EV = ROOT / "research/experiments/n11-centralreply-evwin4-adoption-predecl-20261126"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
MANIFEST = D / "output/increments-manifest.json"

BASE_CACHE = EV / "output/merged-exact-s5-chain-plus-evwin4-20261126.cache"
SCEN_CACHE = D / "output/merged-exact-s5-chain-plus-emloss21-20261126.cache"
INCREMENT = D / "output/increment-emloss21-20261126.cache"
BASE_SUMMARY = EV / "reaudit/output/refresh-summary.json"
SCEN_SUMMARY = D / "reaudit/output/refresh-summary.json"
BASE_CLOSURE = EV / "reaudit/output/closure-classes.csv"
SCEN_CLOSURE = D / "reaudit/output/closure-classes.csv"

BASE_CACHE_SHA_EXPECTED = "63f33c4f620583449641102026b261c559ae5ecc29713cd6445d6fe9369858f0"
SCEN_CACHE_SHA_EXPECTED = "6e49dd841b7bfcb335d86ef2479c95f47ab7acbcf41ace389a8b8eb95c778c9d"
INCREMENT_SHA_EXPECTED = "47443dc143c157ab972de0f39f2cf3afb5d062e209da9dcd8e486f0a57c8ebca"
BASE_SUMMARY_SHA_EXPECTED = "1fafd0811d4b5e806a11cf610111967b9d6fdb741fa86b68688ef1cee4411e6e"
BASE_CLOSURE_SHA_EXPECTED = "6ba51faa9824ba5065a8e938cc6970ce2ace464f74d26f30582cbaa8334c930d"
BASE_PERROOT_SHA_EXPECTED = "d9eee976e52c38c71440a26cb6f9f14ae68439feaec21e17600b1052870dd502"


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
    for name, p, expect in (("base_summary", BASE_SUMMARY, BASE_SUMMARY_SHA_EXPECTED),
                            ("base_closure", BASE_CLOSURE, BASE_CLOSURE_SHA_EXPECTED)):
        out[name] = {"sha256": sha(p)}
        assert out[name]["sha256"] == expect, name
    out["base_per_root"] = {"sha256": sha(EV / "reaudit/output/per-root-coverage.csv")}
    assert out["base_per_root"]["sha256"] == BASE_PERROOT_SHA_EXPECTED
    for name, p in (("scen_summary", SCEN_SUMMARY), ("scen_closure", SCEN_CLOSURE)):
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
    assert (len(base), base_wins, base_loss) == (6771, 192, 6579)
    assert (len(scen), scen_wins, scen_loss) == (6792, 192, 6600)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "emloss21-increments-manifest-v1"
    adopted_table = manifest["adopted_table"]
    assert len(adopted_table) == 21
    assert manifest["base_cache_sha256"] == BASE_CACHE_SHA_EXPECTED
    assert manifest["sha256"]["loss_increment"] == INCREMENT_SHA_EXPECTED
    assert manifest["adopted_nodes_total"] == 129518414
    adopted = {}
    for row in adopted_table:
        key = (row["lo"], row["hi"])
        assert key in incr, f"manifest row not in increment: {key}"
        assert incr[key] == (2, row["nodes"]), (key, incr[key])
        assert out != {} or True
        assert scen[key][0] == 2, f"adopted row not LOSS in SCEN: {key}"
        assert key not in base, f"adopted row not fresh to BASE: {key}"
        adopted[key] = row
    assert set(adopted) == keys_inc

    # the 3 win ties: consumed WINs, in BASE as WIN with identical nodes,
    # absent from the increment and from the SCEN-added set
    for tie in manifest["win_ties"]:
        key = (tie["lo"], tie["hi"])
        assert key in base and base[key] == (1, tie["nodes"]), tie
        assert key not in incr, tie
        assert scen[key] == base[key], tie

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
        assert row["serving_class"] in (12264, 30345)
        assert row["s5_index"] in s4_cost[row["serving_class"]], key
    # owner classes of every adopted key (full membership, graph-derived)
    owner_classes = {}
    for key, row in adopted.items():
        owner_classes[key] = [ci for ci in range(len(s4_masks))
                              if row["s5_index"] in s4_cost[ci]]
        assert row["serving_class"] in owner_classes[key], key

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
    assert cb == base_sum["class_status_counts"], (cb, base_sum["class_status_counts"])
    assert cs == scen_sum["class_status_counts"], (cs, scen_sum["class_status_counts"])

    # LOSS-only: ZERO class status flips allowed
    flips = sorted(i for i in base_status if base_status[i] != scen_status[i])
    out["status_flips"] = flips
    assert flips == [], f"loss-only adoption must flip no class: {flips}"
    # every owner class keeps its BASE status
    owners_flat = {}
    for key, ocs in owner_classes.items():
        for ci in ocs:
            owners_flat.setdefault(ci, []).append(key)
    for ci in owners_flat:
        assert base_status[ci] == scen_status[ci], ci

    # serving-class unknown_now arithmetic (graph-derived)
    serving_rows = {}
    for cls in (12264, 30345):
        cost = s4_cost[cls]
        unknown_base = [j for j in cost
                        if tuple(s5_masks[j]) not in base
                        and j not in receipt]
        unknown_scen = [j for j in cost
                        if tuple(s5_masks[j]) not in scen
                        and j not in receipt]
        serving_rows[cls] = {
            "base_status": base_status[cls],
            "scen_status": scen_status[cls],
            "unknown_before": len(unknown_base),
            "unknown_after": len(unknown_scen),
            "adopted_owned_here": sum(1 for k, r in adopted.items()
                                      if r["serving_class"] == cls and r["s5_index"] in cost),
        }
        assert (serving_rows[cls]["unknown_before"]
                - serving_rows[cls]["unknown_after"]
                == serving_rows[cls]["adopted_owned_here"]), cls
    out["serving_class_rows"] = serving_rows
    out["owner_class_count_hist"] = {
        str(n): sum(1 for x in owner_classes.values() if len(x) == n)
        for n in {len(x) for x in owner_classes.values()}}
    out["adopted"] = [
        {"lo": k[0], "hi": k[1], "legal": r["legal"], "nodes": r["nodes"],
         "s5_index": r["s5_index"], "serving_class": r["serving_class"],
         "owner_classes": owner_classes[k], "owner_count": len(owner_classes[k])}
        for k, r in adopted.items()]

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

    # per-root coverage: free_now/uncovered columns must be identical; the
    # individual_greedy_union column may drop (scenario scheduling deltas)
    b_lines = (EV / "reaudit/output/per-root-coverage.csv").read_text().splitlines()
    s_lines = (D / "reaudit/output/per-root-coverage.csv").read_text().splitlines()
    assert len(b_lines) == len(s_lines) == 21
    assert b_lines[0].split(",") == s_lines[0].split(",")
    assert b_lines[0].split(",")[:5] == ["first", "role", "thirds", "free_now", "uncovered"]
    per_root_delta = []
    for bl, sl in zip(b_lines[1:], s_lines[1:]):
        b_row, s_row = bl.split(","), sl.split(",")
        assert b_row[:5] == s_row[:5], (bl, sl)
        b_g = int(b_row[5]) if b_row[5] else None
        s_g = int(s_row[5]) if s_row[5] else None
        if b_g != s_g:
            per_root_delta.append(
                {"first": int(b_row[0]), "free_now": int(b_row[3]),
                 "uncovered": int(b_row[4]),
                 "individual_greedy_union_base": b_g,
                 "individual_greedy_union_scen": s_g})
    out["per_root_greedy_delta"] = per_root_delta
    out["per_root_free_and_uncovered_identical"] = True

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
    # LOSS-only: the resolved pool grows by exactly the adopted keys that
    # sit in the frozen update8 baseline requirement.  Machine-measured:
    # the 17 batch-5 keys are in the baseline requirement (resolved
    # 263 -> 280); the 4 Part ES keys are not (they were first probed in
    # batch-38, after the update8 baseline froze) and remaining_now keeps
    # its BASE value.
    base_req = set(base_sum["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    scen_req = set(scen_sum["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    new_resolved = scen_req - base_req
    expected_new = {r["s5_index"] for r in adopted.values()
                    if r["serving_class"] == 12264}
    unexpected_new = {r["s5_index"] for r in adopted.values()
                      if r["serving_class"] == 30345}
    assert new_resolved == expected_new, (sorted(new_resolved), sorted(expected_new))
    assert not (new_resolved & unexpected_new)
    assert out["update8_refresh_scen"]["remaining"] == \
        out["update8_refresh_base"]["remaining"]
    out["update8_new_resolved"] = sorted(new_resolved)

    def group_key(gr):
        return (gr["first"], gr["third"], gr["fourth"], gr["reply"], gr["s4_class_index"])
    b_groups = sorted(group_key(x) for x in base_sum["frozen_update8_refresh"]["win_hit_groups"])
    s_groups = sorted(group_key(x) for x in scen_sum["frozen_update8_refresh"]["win_hit_groups"])
    out["win_hit_groups_identical"] = b_groups == s_groups
    assert out["win_hit_groups_identical"], "loss-only must add no win-hit group"

    out["joint_greedy"] = {
        "base": base_sum["joint_greedy"]["greedy_union_size"],
        "scen": scen_sum["joint_greedy"]["greedy_union_size"],
    }
    out["worklist_total"] = {
        "base": base_sum["worklist_total"],
        "scen": scen_sum["worklist_total"],
    }
    # worklist regen pins (UNPUBLISHED per size policy; the BASE side is
    # the published Part EV dossier regen pin ca50cb68... 3,717,416 B,
    # the SCEN side is this kit's local regen pin)
    swl = D / "reaudit/output/probe-worklist.csv"
    assert swl.is_file()
    out["worklist_regen_pins"] = {
        "base": {"sha256": "ca50cb68c10827e7e24e02c02e0166813b57ad646eb169bf8bd2c827fcdd09df",
                 "size": 3717416, "source": "published Part EV dossier census json regen pin "
                 "(file unpublished per size policy)"},
        "scen": {"sha256": sha(swl), "size": swl.stat().st_size},
    }

    out["verdict"] = {
        "part_declared": False,
        "canonical_head_sha256": BASE_CACHE_SHA_EXPECTED,
        "consumed": "NOTHING",
        "status_flips": 0,
        "census_counts_identical_to_published_summaries": True,
        "note": ("scenario measurement only; LOSS-only adoption flips no "
                 "class status; 11x11 stays UNKNOWN; no root verdict; "
                 "nodes are bookkeeping"),
    }

    outp = D / "output/census-deltas-emloss21-predecl.json"
    outp.write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "base": cb, "scen": cs, "flips": flips,
        "serving_class_rows": serving_rows,
        "closure_churn": out["closure_churn"],
        "joint_greedy": out["joint_greedy"],
        "worklist_total": out["worklist_total"],
        "per_root_greedy_delta": per_root_delta,
    }, indent=1))
    print("written:", outp)


if __name__ == "__main__":
    main()
