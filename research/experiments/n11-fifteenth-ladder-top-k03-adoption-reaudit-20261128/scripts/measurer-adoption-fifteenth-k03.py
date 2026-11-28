"""Fifteenth k03 adoption measurement: BASE (fifteenth k01 head
of record b5f322dd...) vs SCENARIO (fifteenth class-5804 k03
adoption union, 3a527d39...) census deltas.

Part of the kit n11-fifteenth-ladder-top-k03-adoption-reaudit-20261128
(declaration commit 08a1163d, publish-then-execute): the fifteenth
k03 canonical adoption consumes exactly the single published
re-escalation row (1 WIN: k03 6053400849139367936:128, s5 index
212536, serving class 5804) and advances the canonical head of
record from b5f322dd... (6,898 rows WIN 216 / LOSS 6,682) to
3a527d39... (6,899 rows WIN 217 / LOSS 6,682).

This measurer is a structural descendant of the published
fifteenth k01 measurer (kit n11-fifteenth-k01-adoption-reaudit-
20261128): it MEASURES the census/scheduling delta of adopting the
row, against the published fifteenth k01 adoption-reaudit refresh
(three byte-identical runs of the byte-clone refresh published in
this kit's reaudit/ directory, three regions differing from the
fifteenth k01 refresh: docstring, CACHE path, expected cache sha).

Fail-closed pins verified before any census is written: the frozen
dependency graph, the update8 repaired joint plan, the fail-closed
union merger (90711961...), the adoption manifest
(n11-fifteenth-ladder-top-k03-win-adoption-manifest-v1) pins:
base head b5f322dd (6,898/216/6,682), increment 16dd8594,
expected merged shape 6,899/217/6,682, the BASE-side fifteenth k01
adoption-reaudit kit outputs (summary cafa9c29, closure 3f3b7154,
per-root 1638c435, census json beda7654, BASE worklist regen pin
0fff5135 unpublished per size policy), and the SCEN-side outputs of
this kit.

The adopted row is WIN (k03), so class-status flips are win-hit
flips (the Part EW/EM mechanism).  MEASURED (the declaration's
naive ONE-flip prediction HOLDS EXACTLY): the WIN key has owner
union classes 5803, 5804, and the serving class 5804 is ALREADY
excluded_now at BASE (it flipped unknown -> excluded_now in the
fourteenth Part), so exactly ONE owner class flips unknown ->
excluded_now (5803; census unknown 34,369 -> 34,368, excluded_now
151 -> 152, free_now 39 unchanged).  The serving class 5804 STAYS
in the closure ladder at rank 1 with cost-unknown dropping 2 -> 1
(NOT a ladder exit; k02 remains its last cost-unknown child); the
ladder-row rank set is UNCHANGED (rank churn count 0, ladder 799
-> 799 rows); owner 5803 sits outside the ladder.  The adopted s5
index
212536 sits OUTSIDE the frozen update8 baseline requirement
(resolved 286 -> 286, remaining_now unchanged 31,332,
groups_free_now 131, win-hit group set unchanged 35 -> 35, no
added or removed groups; neither owner class 5803 nor 5804 is a
plan group class).  The per-root coverage MEASURES two individual
greedy re-routes (root 38 drops 2,877 -> 2,876, root 49 drops
2,691 -> 2,690, free_now/uncovered identical on all 20 roots) and
the joint greedy union drops 43,149 -> 43,148 (scheduling
quantities, not coverage claims); the probing worklist row count
drops 64,260 -> 64,259.

Fail-closed (assertions abort before the output json is written);
tamper battery 4/4 fail-closed.  The output json is
output/census-deltas-fifteenth-k03-adoption.json.

Adopting solver-trusted S5 labels flips class-status bookkeeping
only: no root verdict is consumed, no root freed, no root excluded,
no coverage claim is made or changed.  The standard 11x11 empty
board and every one of the 19 central-reply roots stay UNKNOWN.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
D = ROOT / "research/experiments/n11-fifteenth-ladder-top-k03-adoption-reaudit-20261128"
EV = ROOT / "research/experiments/n11-fifteenth-k01-adoption-reaudit-20261128"
T2 = ROOT / "research/experiments/n11-fifteenth-ladder-top-k03-adoption-20261128"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
MANIFEST = T2 / "adoption-manifest.json"
MERGER = ROOT / "research/experiments/n11-centralreply-sixthlossk38-adoption-reaudit-20261126/scripts/s5_union_merge.py"

BASE_CACHE = ROOT / "research/experiments/n11-fifteenth-ladder-top-k01-adoption-20261128/output/merged/merged-exact-s5-chain-plus-fifteenth-k01-20261128.cache"
SCEN_CACHE = T2 / "output/merged/merged-exact-s5-chain-plus-fifteenth-k03-20261128.cache"
INCREMENT = T2 / "output/increment-fifteenth-k03-adoption-20261128.cache"
BASE_SUMMARY = EV / "reaudit/output/refresh-summary.json"
SCEN_SUMMARY = D / "reaudit/output/refresh-summary.json"
BASE_CLOSURE = EV / "reaudit/output/closure-classes.csv"
SCEN_CLOSURE = D / "reaudit/output/closure-classes.csv"
BASE_PERROOT = EV / "reaudit/output/per-root-coverage.csv"
SCEN_PERROOT = D / "reaudit/output/per-root-coverage.csv"
BASE_CENSUS_JSON = EV / "output/census-deltas-fifteenth-k01-adoption.json"

BASE_CACHE_SHA_EXPECTED = "b5f322dda85946e10feb95c62f40123827ef1271fcc27e5542047d17c1d59bcf"
SCEN_CACHE_SHA_EXPECTED = "3a527d39db7acec32b4c688e0bbbafea8015d9d4aac778cf51e7e5c37afe6a3a"
INCREMENT_SHA_EXPECTED = "16dd859404627ca6e4e5b9f600390a8da54f79342db6b0f07b9b4dbb40140fc4"
MANIFEST_SHA_EXPECTED = "f3f2bc207284245753a3bf5a1f3cec46a1d5ab85cdb23789eae3c47ed39eed91"
BASE_SUMMARY_SHA_EXPECTED = "cafa9c29034aae26b7696349887df26e0205579d2cf36a15d165f3f5b2cb3dbf"
BASE_CLOSURE_SHA_EXPECTED = "3f3b7154c4af0ed645e9df93a8136d8c395cd63ea60151d3f272fbfed131471b"
BASE_PERROOT_SHA_EXPECTED = "1638c43550a891cd8ab1773837764281f2108592d09974d0fdac29e7495fd347"
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_WORKLIST_PIN_SOURCE = json.loads(
    BASE_CENSUS_JSON.read_text(encoding="utf-8"))["worklist_regen_pins"]["scen"]
BASE_WORKLIST_SHA_EXPECTED = "0fff5135baed26410089724778a7f6af5350dca942274eb761e8f67ea30b820b"
BASE_WORKLIST_SIZE_EXPECTED = 3714556
SCEN_WORKLIST_SHA_EXPECTED = "e165cf369afa5aaa5845b4f2027dab617cc088adcaad23bd1b06540fb4942c5f"
SCEN_WORKLIST_SIZE_EXPECTED = 3714501

ADOPTED_COUNT = 1
ADOPTED_WIN = 1
ADOPTED_LOSS = 0
ADOPTED_NODES_TOTAL = 3364655
SERVING_CLASS = 5804
SERVING_CLASS_MASK = (6053400849139367936, 0)
LOSS_KEYS = {}
LOSS_S5_INDICES = {}
LOSS_OWNER_CLASSES = {}
WIN_KEYS = {
    "k03": (6053400849139367936, 128),
}
WIN_S5_INDICES = {"k03": 212536}
WIN_OWNER_CLASSES = {
    "k03": [5803, 5804],
}
EXPECTED_FLIPS = [5803]
EXPECTED_UNKNOWN_CHURN = [
    {"class_index": 5804, "base": 2, "scen": 1},
]
EXPECTED_RANK_CHURN_COUNT = 0
EXPECTED_GREEDY_DELTA = [
    {"root": 38, "base": 2877, "scen": 2876},
    {"root": 49, "base": 2691, "scen": 2690},
]
EXPECTED_WIN_HIT_GROUP_ADDED = 0
BASE_CENSUS = {"unknown": 34369, "excluded_now": 151,
               "free_now": 39, "excluded": 390}
SCEN_CENSUS = {"unknown": 34368, "excluded_now": 152,
               "free_now": 39, "excluded": 390}


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
    assert (len(base), base_wins, base_loss) == (6898, 216, 6682)
    assert (len(scen), scen_wins, scen_loss) == (6899, 217, 6682)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "n11-fifteenth-ladder-top-k03-win-adoption-manifest-v1"
    assert manifest["base"]["sha256"] == BASE_CACHE_SHA_EXPECTED
    assert (manifest["base"]["rows"], manifest["base"]["win"],
            manifest["base"]["loss"]) == (6898, 216, 6682)
    assert manifest["merger_sha256"] == MERGER_SHA_EXPECTED
    assert manifest["kits"]["replica"].startswith(
        "n11-fifteenth-ladder-top-k02k03-reescalation-20261128")
    assert manifest["kits"]["cppgate"].startswith(
        "n11-fifteenth-ladder-top-k03-win-cppgate-20261128")
    assert manifest["kits"]["thirdimpl"].startswith(
        "n11-fifteenth-ladder-top-k03-thirdimpl-20261128")
    # disclosed in the adoption completion log: no cross-host
    # replication kit exists for this row yet (unlike the
    # thirteenth adoption); the manifest correctly carries no xhost
    assert "xhost" not in manifest["kits"]
    assert manifest["owner_union_precheck"].startswith(
        "none for this key; owner class union to be derived from "
        "the frozen graph in the declared flip-census follow-up "
        "Part (caveat: shared-owner pre-exclusion)")
    adopted_rows = manifest["rows"]
    assert len(adopted_rows) == ADOPTED_COUNT
    assert manifest["expected_merged_shape"] == {"rows": 6899, "win": 217, "loss": 6682}
    assert manifest["nodes_total_bookkeeping"] == ADOPTED_NODES_TOTAL
    assert manifest["status_guard"].endswith("11x11 UNKNOWN")

    # adopted rows derived from the increment itself
    assert len(incr) == ADOPTED_COUNT
    win_keys = sorted(k for k, v in incr.items() if v[0] == 1)
    loss_keys = sorted(k for k, v in incr.items() if v[0] == 2)
    assert len(win_keys) == ADOPTED_WIN and len(loss_keys) == ADOPTED_LOSS
    assert set(win_keys) == set(WIN_KEYS.values()), win_keys
    assert set(loss_keys) == set(LOSS_KEYS.values()), loss_keys
    for k, v in incr.items():
        assert k not in base, f"adopted row not fresh to BASE: {k}"
        assert scen[k] == v
    for row in adopted_rows:
        key = tuple(int(x) for x in row["key"].split(":"))
        assert key in incr and incr[key] == (row["result"], row["nodes"]), row
        assert row["class_index"] == SERVING_CLASS, row

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
    for label, key in LOSS_KEYS.items():
        assert mask_to_index[key] == LOSS_S5_INDICES[label], label

    update8 = json.loads(UPDATE8.read_text(encoding="utf-8"))
    receipt = {int(k): int(v) for k, v in update8["resolved_s5_verdicts"].items()}

    # s5 index round trip + owner classes for both rows
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
    for label, key in LOSS_KEYS.items():
        assert owner_classes[key] == LOSS_OWNER_CLASSES[label], \
            (label, owner_classes[key])
    # the ultra-cheap serving class owns the adopted row
    for key, idx in adopted_indices.items():
        assert idx in s4_cost[SERVING_CLASS], key
    out["owner_class_count_hist"] = {
        str(n): sum(1 for x in owner_classes.values() if len(x) == n)
        for n in {len(x) for x in owner_classes.values()}}
    assert out["owner_class_count_hist"] == {"2": 1}, \
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
    assert cb == BASE_CENSUS, cb
    assert cs == SCEN_CENSUS, cs

    # WIN-side flips (Part EW/EM win-hit mechanism): MEASURED.
    # Every flip must be an owner class of a WIN row and must go
    # unknown -> excluded_now; no other flip direction may occur.
    # MEASURED: the declaration's naive ONE-flip prediction HOLDS
    # EXACTLY: the serving class 5804 is already excluded_now at
    # BASE (it flipped in the fourteenth Part), so exactly ONE of
    # the two owner-union classes flips.
    flips = sorted(ci for ci in base_status
                   if base_status[ci] != scen_status[ci])
    out["status_flips"] = [
        {"class_index": ci, "base": base_status[ci], "scen": scen_status[ci],
         "class_mask": s4_masks[ci]}
        for ci in flips]
    assert flips == EXPECTED_FLIPS, flips
    win_owner_union = sorted({ci for key in WIN_KEYS.values()
                              for ci in owner_classes[key]})
    # the measured flip list is a STRICT SUBSET of the owner union:
    # exactly the non-pre-excluded owner classes flip (the
    # declaration's caveat (shared-owner pre-exclusion) materialises)
    assert set(flips) < set(win_owner_union), \
        "the measured flip list must be a strict subset of the owner union"
    assert set(win_owner_union) - set(flips) == {SERVING_CLASS}, flips
    assert set(flips) == {5803}, flips
    for ci in (5803,):
        assert base_status[ci] == "unknown", ci
        assert scen_status[ci] == "excluded_now", ci
    # the pre-excluded serving class does NOT flip (already
    # excluded_now at BASE, flipped in the fourteenth Part)
    assert base_status[SERVING_CLASS] == "excluded_now", SERVING_CLASS
    assert scen_status[SERVING_CLASS] == "excluded_now", SERVING_CLASS
    for ci in flips:
        assert base_status[ci] == "unknown", ci
        assert scen_status[ci] == "excluded_now", ci
    out["status_flip_count"] = len(flips)
    out["status_flip_count_predicted_by_declaration"] = 1  # naive owner-union; MEASURED 1 (prediction holds exactly)
    # no free_now change and no other census movement
    assert cb["free_now"] == cs["free_now"] == 39
    assert cb["excluded"] == cs["excluded"] == 390
    assert cs["unknown"] == cb["unknown"] - len(flips)
    # no LOSS rows are adopted in this Part (LOSS_KEYS is empty; the
    # loop is kept for structural parity with the u03 measurer)
    for label, key in LOSS_KEYS.items():
        for ci in owner_classes[key]:
            if ci in (SERVING_CLASS,):
                continue
            assert base_status[ci] == scen_status[ci] == "unknown", ci

    # serving-class unknown arithmetic (graph-derived, class 5804)
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
    # the fifteenth serving class 6053400849139367936:0 (class
    # 5804) is ALREADY excluded_now at BASE (it flipped unknown ->
    # excluded_now in the fourteenth Part, the rank-1 closure ladder
    # row): adopting the k03 WIN row does NOT flip its status (it
    # stays excluded_now) but drops its cost-unknown 2 -> 1 while it
    # STAYS in the ladder (NOT a ladder exit, rank 1 maintained;
    # k02 remains its last cost-unknown child)
    assert serving_rows[str(cls)]["base_status"] == "excluded_now"
    assert serving_rows[str(cls)]["scen_status"] == "excluded_now"
    assert (serving_rows[str(cls)]["unknown_before"],
            serving_rows[str(cls)]["unknown_after"]) == (2, 1), cls
    assert serving_rows[str(cls)]["adopted_owned_here"] == 1
    out["serving_class_rows"] = serving_rows

    # closure-classes.csv churn (measured; the serving class STAYS
    # in the ladder; no other ladder cell churns rank)
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
    for ci in sorted(set(bc) & set(sc)):
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
    assert (len(bc), len(sc)) == (799, 799), (len(bc), len(sc))
    # MEASURED: the serving class 5804 STAYS in the ladder at rank 1
    # (unknown_now 2 -> 1) and NO cell re-ranks (rank churn 0)
    assert entered == [], entered
    assert left == [], left
    assert unknown_churn == EXPECTED_UNKNOWN_CHURN, unknown_churn
    assert len(rank_churn) == EXPECTED_RANK_CHURN_COUNT, len(rank_churn)
    assert BASE_CLOSURE.read_text() != SCEN_CLOSURE.read_text(), \
        "closure-classes.csv must NOT be byte-identical to the BASE side"
    out["closure_byte_identical_to_base"] = False
    # the serving class stays in the ladder on both sides; the
    # non-serving owner 5803 sits outside on both sides
    assert 5804 in bc and 5804 in sc
    assert 5803 not in bc and 5803 not in sc
    out["loss_owner_class_union"] = sorted(
        {ci for k, v in incr.items() if v[0] == 2
         for ci in owner_classes[k]})

    # per-root coverage: free_now/uncovered identical on all 20 roots;
    # TWO individual greedy re-routes are MEASURED
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
    # MEASURED: root 49 drops 2,691 -> 2,690 and root 38 drops
    # 2,877 -> 2,876 (the adoption re-routes both roots' greedy
    # unions; scheduling quantities, not coverage claims)
    assert greedy_delta == EXPECTED_GREEDY_DELTA, greedy_delta
    out["per_root_coverage_byte_identical"] = \
        BASE_PERROOT.read_text() == SCEN_PERROOT.read_text()
    assert out["per_root_coverage_byte_identical"] is False
    bp_lines = BASE_PERROOT.read_text().splitlines()
    sp_lines = SCEN_PERROOT.read_text().splitlines()
    assert len(bp_lines) == len(sp_lines) == 21
    differing = [n for n, (a, b) in enumerate(zip(bp_lines, sp_lines)) if a != b]
    assert differing == [2, 3], differing
    assert bp_lines[2] == "49,central,119,10,109,2691", bp_lines[2]
    assert sp_lines[2] == "49,central,119,10,109,2690", sp_lines[2]
    assert bp_lines[3] == "38,central,119,15,104,2877", bp_lines[3]
    assert sp_lines[3] == "38,central,119,15,104,2876", sp_lines[3]

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
    # MEASURED: the adopted s5 index 212536 sits OUTSIDE the frozen
    # update8 baseline requirement (the u04 precedent), so NO
    # baseline s5 resolves (286 -> 286)
    assert new_resolved == set(), sorted(new_resolved)
    assert adopted_idx & baseline_req == set()
    assert adopted_idx - baseline_req == {212536}
    assert len(new_resolved) == (
        out["update8_refresh_scen"]["resolved"]
        - out["update8_refresh_base"]["resolved"]), "resolved delta"
    out["update8_refresh_base"]["resolved_list_len"] = len(base_req)
    out["update8_refresh_scen"]["resolved_list_len"] = len(scen_req)
    assert out["update8_refresh_base"]["resolved"] == 286
    assert out["update8_refresh_scen"]["resolved"] == 286
    assert out["update8_refresh_base"]["remaining"] == 31332
    assert out["update8_refresh_scen"]["remaining"] == 31332
    assert out["update8_refresh_base"]["groups_free_now"] == 131
    assert out["update8_refresh_scen"]["groups_free_now"] == 131
    out["update8_new_resolved"] = sorted(new_resolved)

    def group_key(gr):
        return (gr["first"], gr["third"], gr["fourth"], gr["reply"],
                gr["s4_class_index"])
    b_groups = sorted(group_key(x)
                      for x in base_sum["frozen_update8_refresh"]["win_hit_groups"])
    s_groups = sorted(group_key(x)
                      for x in scen_sum["frozen_update8_refresh"]["win_hit_groups"])
    added_groups = sorted(set(s_groups) - set(b_groups))
    removed_groups = sorted(set(b_groups) - set(s_groups))
    out["win_hit_groups_identical"] = b_groups == s_groups
    # MEASURED: the win-hit group set is IDENTICAL (35 -> 35, no
    # added or removed groups); NEITHER owner-union class
    # (5803, 5804) is an update8 plan group class
    assert out["win_hit_groups_identical"] is True
    assert len(b_groups) == 35, len(b_groups)
    assert len(s_groups) == 35, len(s_groups)
    assert len(added_groups) == EXPECTED_WIN_HIT_GROUP_ADDED
    assert removed_groups == [], removed_groups
    u8_group_classes = {gr["s4_class_index"]
                        for gr in scen_sum["frozen_update8_refresh"]["win_hit_groups"]}
    assert {5803, 5804}.isdisjoint(u8_group_classes)
    out["win_hit_groups_added"] = added_groups

    out["joint_greedy"] = {
        "base": base_sum["joint_greedy"]["greedy_union_size"],
        "scen": scen_sum["joint_greedy"]["greedy_union_size"],
    }
    out["worklist_total"] = {
        "base": base_sum["worklist_total"],
        "scen": scen_sum["worklist_total"],
    }
    # MEASURED: the joint greedy union drops 43,149 -> 43,148 and
    # the probing worklist row count drops 64,260 -> 64,259 (the
    # adopted key's OWN membership rows leave the worklist; both are
    # scheduling quantities, not coverage claims)
    assert out["joint_greedy"] == {"base": 43149, "scen": 43148}, \
        out["joint_greedy"]
    assert out["worklist_total"] == {"base": 64260, "scen": 64259}, \
        out["worklist_total"]

    # worklist regen pins (UNPUBLISHED per size policy; the BASE side is
    # the published thirteenth census json's scen regen pin, the SCEN
    # side is this kit's local regen pin)
    swl = D / "reaudit/output/probe-worklist.csv"
    assert swl.is_file()
    out["worklist_regen_pins"] = {
        "base": BASE_WORKLIST_PIN_SOURCE,
        "scen": {"sha256": sha(swl), "size": swl.stat().st_size},
    }
    assert out["worklist_regen_pins"]["base"]["sha256"] == \
        BASE_WORKLIST_SHA_EXPECTED
    assert out["worklist_regen_pins"]["base"]["size"] == \
        BASE_WORKLIST_SIZE_EXPECTED
    assert out["worklist_regen_pins"]["scen"]["sha256"] == \
        SCEN_WORKLIST_SHA_EXPECTED, out["worklist_regen_pins"]["scen"]
    assert out["worklist_regen_pins"]["scen"]["size"] == \
        SCEN_WORKLIST_SIZE_EXPECTED, out["worklist_regen_pins"]["scen"]
    assert out["worklist_regen_pins"]["scen"]["sha256"] != \
        out["worklist_regen_pins"]["base"]["sha256"]

    # tamper battery (fail-closed): each tamper variant must change the
    # independent census recount (the measurement cannot be reproduced
    # from a tampered cache), and every tampered cache breaks the
    # sha-pinned gate
    tamper = {}
    # 1. flip the adopted row's verdict WIN -> LOSS in a SCEN copy:
    #    the flipped owner 5803 reverts to unknown, and the
    #    pre-excluded serving class 5804 STAYS excluded_now (it
    #    is win-hit by previously adopted rows of the chain) -
    #    the census must move
    scen_rows = []
    with SCEN_CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if (int(row[1]), int(row[2])) in WIN_KEYS.values():
                assert int(row[4]) == 1
                row = row[:4] + ["2"] + row[5:]
            scen_rows.append(row)
    flipped = {}
    for row in scen_rows:
        lo, hi, stones, verdict, nodes = map(int, row[1:])
        flipped[(lo, hi)] = (verdict, nodes)
    tampered_census = counts_from(census(flipped))
    assert tampered_census != cs, "tamper 1 must change the census"
    for ci in (5803,):
        assert census(flipped)[ci] == "unknown", \
            "tamper 1: owner class %d must revert to unknown" % ci
    assert census(flipped)[SERVING_CLASS] == "excluded_now", \
        "tamper 1: the pre-excluded serving class must stay excluded_now"
    tamper["verdict_flip_changes_census"] = True
    # 2. delete the adopted row from the SCEN copy: the recount must
    #    fall back to the BASE census exactly
    deleted = {k: v for k, v in flipped.items()
               if k not in WIN_KEYS.values()}
    # (the flipped row is absent, so deletion restores the SCEN rows
    # minus the adopted row == BASE rows)
    assert counts_from(census(deleted)) == cb, \
        "tamper 2 must restore the BASE census"
    tamper["row_delete_restores_base_census"] = True
    # 3. append the adopted row to a BASE copy: the recount must equal
    #    the SCEN census exactly (the adoption is exactly this row)
    appended = dict(base)
    for key in WIN_KEYS.values():
        appended[key] = incr[key]
    assert counts_from(census(appended)) == cs, \
        "tamper 3 must reproduce the SCEN census"
    tamper["row_append_reproduces_scen_census"] = True
    # 4. every tampered cache byte-content differs from both pinned
    #    heads, so the sha gate refuses it
    import io
    def rows_bytes(rows):
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        for r in rows:
            w.writerow(r)
        return buf.getvalue().encode("utf-8")
    t1 = rows_bytes(scen_rows)
    t2 = rows_bytes([r for r in scen_rows
                     if (int(r[1]), int(r[2])) not in WIN_KEYS.values()])
    h = hashlib.sha256
    assert h(t1).hexdigest() not in (BASE_CACHE_SHA_EXPECTED,
                                     SCEN_CACHE_SHA_EXPECTED)
    assert h(t2).hexdigest() not in (BASE_CACHE_SHA_EXPECTED,
                                     SCEN_CACHE_SHA_EXPECTED)
    tamper["tampered_caches_break_sha_gate"] = True
    out["tamper_battery"] = tamper

    out["verdict"] = {
        "part_declared": True,
        "part": "fifteenth-k03-flip-census",
        "canonical_head_sha256": SCEN_CACHE_SHA_EXPECTED,
        "consumed": ("exactly the single published fifteenth k03 "
                     "re-escalation row (1 WIN: k03, class 5804)"),
        "status_flips": len(flips),
        "deviation_from_predeclared_expectation": (
            "NO DEVIATION - the declaration's naive graph-derived "
            "ONE-flip prediction ([5803] unknown -> excluded_now, "
            "census unknown 34,369 -> 34,368, excluded_now 151 -> "
            "152) HOLDS EXACTLY: the pre-registered shared-owner "
            "pre-exclusion caveat materialises on the serving class "
            "5804, which is ALREADY excluded_now at BASE (it "
            "flipped unknown -> excluded_now in the fourteenth Part) "
            "and does not flip; the serving class stays in the "
            "closure ladder at rank 1 with unknown_now 2 -> 1 "
            "(k02 remains its last cost-unknown child)"),
        "status_flip_mechanism": (
            "win-hit (the Part EW/EM mechanism): the adopted WIN row "
            "k03 (s5 index 212536, 6053400849139367936:128) has owner "
            "union 5803, 5804; the one NOT-pre-excluded owner 5803 "
            "flips unknown -> excluded_now (measured flip list is a "
            "strict subset of the owner union, the caveat-"
            "materialisation case); the serving class 5804 "
            "(6053400849139367936:0) is pre-excluded at BASE and "
            "does NOT flip, it stays excluded_now and STAYS in the "
            "closure ladder at rank 1 (cost-unknown 2 -> 1, NOT a "
            "ladder exit; k02 remains its last cost-unknown "
            "child); owner 5803 sits outside the ladder on both "
            "sides and no closure cell re-ranks (rank churn 0, "
            "ladder 799 -> 799 rows); no class flips to free_now, "
            "free_now stays 39 (Board-verified both sides); the "
            "per-root coverage MEASURES two individual greedy "
            "re-routes (root 38 drops 2,877 -> 2,876, root 49 "
            "drops 2,691 -> 2,690, free_now/uncovered identical on "
            "all 20 roots); joint greedy drops 43,149 -> 43,148 "
            "(a scheduling quantity, not a coverage claim) and the "
            "probing worklist row count drops 64,260 -> 64,259 (the "
            "adopted key's own membership rows leave the worklist; "
            "regen content sha differs from the BASE pin); the "
            "adopted s5 index 212536 sits OUTSIDE the frozen update8 "
            "baseline requirement (resolved 286 -> 286, remaining_now "
            "31,332 -> 31,332, groups_free_now 131 -> 131); the "
            "win-hit group set is unchanged (35 -> 35, no added or "
            "removed groups; neither owner class is a plan group "
            "class)"),
        "census_counts_identical_to_published_summaries": True,
        "note": ("declared fifteenth k03 adoption measurement; "
                 "adopting solver-trusted S5 labels flips class-status "
                 "bookkeeping only: no root verdict is consumed, no root "
                 "freed, no root excluded, no coverage claim is made or "
                 "changed; 11x11 stays UNKNOWN; no root verdict; nodes "
                 "are bookkeeping"),
    }

    outp = D / "output/census-deltas-fifteenth-k03-adoption.json"
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
        "tamper_battery": tamper,
    }, indent=1))
    print("written:", outp)


if __name__ == "__main__":
    main()
