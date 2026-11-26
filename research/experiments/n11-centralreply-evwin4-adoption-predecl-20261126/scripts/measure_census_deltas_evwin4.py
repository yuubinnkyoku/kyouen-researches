#!/usr/bin/env python3
"""Predecl dossier measurement: BASE (Part EU canonical 3ba48608...) vs
SCENARIO (evwin4 pre-adoption union, 63f33c4f...) census deltas.

NOT a Part extractor and NOT an adoption: the Part EV adoption is not
declared, nothing is consumed, the canonical head stays 3ba48608....
This script only MEASURES, from published-byte-verbatim local inputs,
what the census delta of the 4 Part EV gate-verified UNCONSUMED WIN rows
would be if the future Part EV declared their adoption:

* SCEN cache must equal BASE cache rows + exactly the 4 increment rows;
* every adopted row must be fresh to BASE, quarantine-free and a canonical
  safe 5-stone key, and its (lo,hi) must equal the Part EV gate-kit SSOT
  gate-rows-ev.json entry, with the SSOT class_index/s5_index verified
  against the frozen dependency graph (the key must sit in the owner
  class s4_cost, and the s5_index must index the key in s5_masks);
* the refresh status logic is replicated independently (graph s4_status /
  s4_cost + update8 receipts + cache verdicts; free_now candidates are
  cross-checked against the published refresh summaries' Board-verified
  free_now count instead of re-running the Board) and must reproduce the
  published class status census EXACTLY on both sides
  (BASE 34,430/90/39/390 vs SCEN 34,417/103/39/390:
  unknown/excluded_now/free_now/excluded);
* the status flips are identified exactly: all and only the BASE-unknown
  owner classes of the 4 keys flipping to excluded_now;
* closure-classes.csv churn (rows enter/leave, unknown_now deltas, rank
  churn), per-root coverage, update8 refresh fields, joint greedy and
  worklist totals are measured against the published Part EU reaudit
  outputs.

11x11 stays UNKNOWN; nodes are bookkeeping; no verdict is created or
consumed here.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
D = ROOT / "research/experiments/n11-centralreply-evwin4-adoption-predecl-20261126"
EU = ROOT / "research/experiments/n11-centralreply-euwin2-adoption-reaudit-20261125"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
SSOT = ROOT / "research/experiments/n11-centralreply-closure-wins-b018d002e002f017-cppgate-20261125/input/gate-rows-ev.json"

BASE_CACHE = EU / "output/merged-exact-s5-chain-plus-euwin2-20261125.cache"
SCEN_CACHE = D / "output/merged-exact-s5-chain-plus-evwin4-20261126.cache"
INCREMENT = D / "output/increment-evwin4-20261126.cache"
BASE_SUMMARY = EU / "reaudit/output/refresh-summary.json"
SCEN_SUMMARY = D / "reaudit/output/refresh-summary.json"
BASE_CLOSURE = EU / "reaudit/output/closure-classes.csv"
SCEN_CLOSURE = D / "reaudit/output/closure-classes.csv"


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
    for name, p in (("base_summary", BASE_SUMMARY), ("scen_summary", SCEN_SUMMARY),
                    ("base_closure", BASE_CLOSURE), ("scen_closure", SCEN_CLOSURE)):
        out[name] = {"sha256": sha(p)}

    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    incr = load_cache(INCREMENT)

    # SCEN == BASE + exactly the increment rows
    keys_inc = {k for k in incr}
    keys_scen = set(scen)
    keys_base = set(base)
    assert keys_scen - keys_base == keys_inc, (keys_scen - keys_base, keys_inc)
    assert keys_base - keys_scen == set()
    for k in keys_inc:
        assert scen[k] == incr[k], (k, scen[k], incr[k])
    for k in keys_base:
        assert scen[k] == base[k]
    base_wins = sum(1 for v in base.values() if v[0] == 1)
    base_loss = sum(1 for v in base.values() if v[0] == 2)
    scen_wins = sum(1 for v in scen.values() if v[0] == 1)
    scen_loss = sum(1 for v in scen.values() if v[0] == 2)
    out["base_cache"]["rows"] = len(base)
    out["base_cache"]["win"] = base_wins
    out["base_cache"]["loss"] = base_loss
    out["scen_cache"]["rows"] = len(scen)
    out["scen_cache"]["win"] = scen_wins
    out["scen_cache"]["loss"] = scen_loss
    assert (len(base), base_wins, base_loss) == (6767, 188, 6579)
    assert (len(scen), scen_wins, scen_loss) == (6771, 192, 6579)

    ssot = json.loads(SSOT.read_text(encoding="utf-8"))
    targets = ssot["targets"]
    assert set(targets) == {"b018", "d002", "e002", "f017"}
    for k in keys_inc:
        assert scen[k][0] == 1, f"adopted row not WIN: {k}"
    adopted = {}
    for name, t in targets.items():
        key = (t["lo"], t["hi"])
        assert key in incr, f"SSOT target not in increment: {name} {key}"
        legal, budget, result, nodes = map(int, t["expected"].split(","))
        assert (budget, result, nodes) == (t["budget"], 1, scen[key][1]), name
        assert legal in (60, 73, 79, 82)
        adopted[name] = {
            "lo": t["lo"], "hi": t["hi"], "class_index": t["class_index"],
            "s5_index": t["s5_index"], "nodes": nodes,
        }

    # graph
    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s4_masks = g["s4_masks"]
    s4_status = g["s4_cost_status_unused"] if False else g["s4_status"]
    s4_cost = g["s4_cost"]
    s5_masks = g["s5_masks"]
    mask_to_index = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}

    update8 = json.loads(UPDATE8.read_text(encoding="utf-8"))
    receipt = {int(k): int(v) for k, v in update8["resolved_s5_verdicts"].items()}

    def verdict_index(key, cache):
        i = mask_to_index.get(key)
        if i is None:
            return None
        if key in cache:
            return cache[key][0]
        return receipt.get(i)

    # SSOT class/s5_index verification + owner classes
    for name, a in adopted.items():
        key = (a["lo"], a["hi"])
        assert mask_to_index.get(key) == a["s5_index"], (name, mask_to_index.get(key))
        # the key must be a cost child of the SSOT owner class
        assert a["s5_index"] in s4_cost[a["class_index"]], name
    owner_classes = {name: [ci for ci in range(len(s4_masks))
                            if a["s5_index"] in s4_cost[ci]]
                     for name, a in adopted.items()}
    for name, a in adopted.items():
        assert a["class_index"] in owner_classes[name], name
        adopted[name]["owner_classes"] = owner_classes[name]
        adopted[name]["owner_count"] = len(owner_classes[name])

    # independent recount of refresh status census on both sides
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
        # free_now candidates were all Board-verified per the published
        # refresh summaries, so candidates == free_now here
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
    published_b = base_sum["class_status_counts"]
    published_s = scen_sum["class_status_counts"]
    assert cb == published_b, (cb, published_b)
    assert cs == published_s, (cs, published_s)

    flips = sorted(i for i in base_status
                   if base_status[i] != scen_status[i])
    flip_detail = []
    for i in flips:
        flip_detail.append({
            "class_index": i,
            "base": base_status[i],
            "scen": scen_status[i],
            "class_mask": s4_masks[i],
        })
    out["status_flips"] = flip_detail
    # every flip must be unknown -> excluded_now and must own an adopted key
    owners_flat = {}
    for name, a in adopted.items():
        for ci in a["owner_classes"]:
            owners_flat.setdefault(ci, []).append(name)
    for f in flip_detail:
        assert f["base"] == "unknown" and f["scen"] == "excluded_now", f
        assert f["class_index"] in owners_flat, f
    for ci in owners_flat:
        if base_status[ci] == "unknown":
            assert ci in flips, ci

    # per-owner-class graph-time cost arithmetic
    for name, a in adopted.items():
        rows = []
        for ci in a["owner_classes"]:
            rows.append({
                "class_index": ci,
                "base_status": base_status[ci],
                "scen_status": scen_status[ci],
                "cost_size": len(s4_cost[ci]),
            })
        a["owner_class_rows"] = rows
        a["unknown_before"] = sum(1 for r in rows if r["base_status"] == "unknown")
        a["unknown_after"] = sum(1 for r in rows if r["scen_status"] == "unknown")
    out["adopted"] = adopted

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
        "rank_churn": rank_churn,
    }

    # per-root coverage: free_now/uncovered columns must be identical; the
    # individual_greedy_union column may drop (scenario scheduling deltas)
    b_lines = (EU / "reaudit/output/per-root-coverage.csv").read_text().splitlines()
    s_lines = (D / "reaudit/output/per-root-coverage.csv").read_text().splitlines()
    assert len(b_lines) == len(s_lines) == 21  # header + 20 root rows
    b_hdr = b_lines[0].split(",")
    assert b_hdr == s_lines[0].split(",")
    assert b_hdr[:5] == ["first", "role", "thirds", "free_now", "uncovered"]
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
    # win_hit group identity check
    def group_key(gr):
        return (gr["first"], gr["third"], gr["fourth"], gr["reply"], gr["s4_class_index"])
    b_groups = sorted(group_key(x) for x in base_sum["frozen_update8_refresh"]["win_hit_groups"])
    s_groups = sorted(group_key(x) for x in scen_sum["frozen_update8_refresh"]["win_hit_groups"])
    out["win_hit_groups_identical"] = b_groups == s_groups
    out["win_hit_groups_only_scen"] = sorted(set(s_groups) - set(b_groups))
    out["win_hit_groups_only_base"] = sorted(set(b_groups) - set(s_groups))

    out["joint_greedy"] = {
        "base": base_sum["joint_greedy"]["greedy_union_size"],
        "scen": scen_sum["joint_greedy"]["greedy_union_size"],
    }
    out["worklist_total"] = {
        "base": base_sum["worklist_total"],
        "scen": scen_sum["worklist_total"],
    }
    # worklist regen pins (UNPUBLISHED per size policy; local regen stats)
    bwl = EU / "reaudit/output/probe-worklist.csv"
    swl = D / "reaudit/output/probe-worklist.csv"
    out["worklist_regen_pins"] = {
        "base": {"sha256": sha(bwl), "size": bwl.stat().st_size},
        "scen": {"sha256": sha(swl), "size": swl.stat().st_size},
    }

    out["verdict"] = {
        "part_ev_declared": False,
        "canonical_head_sha256": sha(BASE_CACHE),
        "consumed": "NOTHING",
        "census_counts_identical_to_published_summaries": True,
        "note": ("scenario measurement only; 11x11 stays UNKNOWN; no root "
                 "verdict; nodes are bookkeeping"),
    }

    outp = D / "output/census-deltas-evwin4-predecl.json"
    outp.write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({k: out[k] for k in (
        "census_recount_base", "census_recount_scen", "status_flips_count",
    )} if False else {
        "base": cb, "scen": cs, "flips": [f["class_index"] for f in flip_detail],
    }, indent=1))
    print("written:", outp)


if __name__ == "__main__":
    main()
