"""Eleventh-cost k01 adoption measurement: BASE (tenth-cost k01/k02 head
of record 16b34014...) vs SCENARIO (eleventh-cost k01 adoption union,
1e2eeda2...) census deltas.

This follow-up Part is DECLARED (pre-registered in the eleventh-cost
k01 canonical adoption completion log and in the adoption manifest's
status_guard field, and in the adoption kit README "next follow-up
Part" disclosure): the eleventh-cost canonical adoption consumes
exactly the one published row (1 WIN k01) and advances the canonical
head of record from 16b34014... (6,889 rows WIN 207 / LOSS 6,682) to
1e2eeda2... (6,890 rows WIN 208 / LOSS 6,682).  This script is a
disclosed structural adaptation of the tenth-cost k01/k02 measurer
7e503080... (itself the ninth-cost 12-row measurer d81113df...
adaptation); it MEASURES the census/scheduling delta of that declared
adoption, from published-byte-verbatim local inputs, and cross-checks
this kit's reaudit refresh outputs (byte-clone refresh of the
published tenth-cost k01/k02 refresh 280d7062..., three
byte-identical determinism runs):

* SCEN cache must equal BASE cache rows + exactly the 1 increment
  row; the adopted row is fresh to BASE and matches the increment
  verdict/nodes exactly;
* the adoption manifest (n11-eleventhcost-k01-win-adoption-manifest-v1)
  pins: base head 16b34014 (6,889/207/6,682), increment 0f627887,
  adopted 1 row WIN 1, nodes_total 12,755,963, the three pillar kits
  (replica aaeb282c, C++ gate 25cef9e9, third-impl 26c7b04d) and
  merger sha 90711961;
* the refresh status logic is replicated independently and must
  reproduce the refreshed class status census EXACTLY on both sides
  (BASE 34,391/129/39/390 unknown/excluded_now/free_now/excluded;
  SCEN 34,388/132/39/390);
* the single adopted row is a WIN (k01), so class-status flips are
  MEASURED, not asserted empty: the measured flip list is exactly the
  THREE owner classes of the WIN key k01 (s5 index 97250): classes
  2376 (1297036696977670144:64, cost-unknown 109 -> 108), 3288 (the
  eleventh-cost serving class 1297036696978718720:0, cost-unknown
  102 -> 101) and 17116 (1152921504607895808:64, cost-unknown
  99 -> 98), each unknown -> excluded_now (the Part EW/EM win-hit
  mechanism);
* no class flips to free_now and no free_now class is lost (39 -> 39,
  Board-verified both sides);
* closure-classes.csv churn is MEASURED: 804 -> 804 rows, entered [],
  left [], NO unknown_now churn, NO rank churn - the closure CSV is
  byte-identical to the BASE side;
* per-root coverage: free_now/uncovered identical on all 20 roots but
  this adoption MEASURES one individual greedy re-route: root 2's
  individual greedy union drops 6,132 -> 6,131 (the adopted WIN row
  removes one still-unknown child from a root-2 greedy class union);
  the per-root CSV is NOT byte-identical to the BASE side;
* the update8 refresh fields: the adopted s5 index sits OUTSIDE the
  frozen baseline requirement, so resolved stays 282 -> 282 and
  remaining_now stays 31,444; the win-hit group set is unchanged (25
  groups, no flipped class is an update8 plan group class);
  groups_free_now stays 131;
* joint greedy stays 37,398 -> 37,398 and the probing worklist stays
  64,272 -> 64,272 rows (regen content sha differs from the BASE pin
  b9f3f1a3.../3,715,222 bytes; SCEN regen is 407a340f.../3,715,222
  bytes - same size, different content, the adopted key replaces one
  worklist row).

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
D = ROOT / "research/experiments/n11-eleventhcost-k01-adoption-reaudit-20261127"
EV = ROOT / "research/experiments/n11-tenthcost-k01k02-adoption-reaudit-20261127"
T2 = ROOT / "research/experiments/n11-eleventhcost-k01-win-adoption-20261127"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
MANIFEST = T2 / "adoption-manifest.json"
MERGER = ROOT / "research/experiments/n11-centralreply-sixthlossk38-adoption-reaudit-20261126/scripts/s5_union_merge.py"

BASE_CACHE = ROOT / "research/experiments/n11-tenthcost-k01k02-adoption-20261127/output/merged/merged-exact-s5-chain-plus-tenthcost-k01k02-20261127.cache"
SCEN_CACHE = T2 / "output/merged/merged-exact-s5-chain-plus-eleventhcost-k01-20261127.cache"
INCREMENT = T2 / "output/increment-eleventhcost-k01-adoption-20261127.cache"
BASE_SUMMARY = EV / "reaudit/output/refresh-summary.json"
SCEN_SUMMARY = D / "reaudit/output/refresh-summary.json"
BASE_CLOSURE = EV / "reaudit/output/closure-classes.csv"
SCEN_CLOSURE = D / "reaudit/output/closure-classes.csv"
BASE_PERROOT = EV / "reaudit/output/per-root-coverage.csv"
SCEN_PERROOT = D / "reaudit/output/per-root-coverage.csv"
BASE_CENSUS_JSON = EV / "output/census-deltas-tenthcost2-adoption.json"

BASE_CACHE_SHA_EXPECTED = "16b340146fe8a01667ae31fc2f0534a8a3977e56b7c701803d621edc23312ef3"
SCEN_CACHE_SHA_EXPECTED = "1e2eeda2db33738de99612531f9bb67456f90c81ceedf123c8bbba117aff2a17"
INCREMENT_SHA_EXPECTED = "0f627887bbc370f05309807407b7389eec53d5bc12a002e34a3120a6fcf15db4"
MANIFEST_SHA_EXPECTED = "6442d01d5a53f7e56002df8b21349a951538fb1d66214ac20022737857f6a39b"
BASE_SUMMARY_SHA_EXPECTED = "40268a5e235851d798df9b59e0fd7622b2f667ae05cd447e5d4c1544c539ffef"
BASE_CLOSURE_SHA_EXPECTED = "d7ae77ddd05d433c0a59555f86efb009e64a5651ad6b918407682bdc5f3178f0"
BASE_PERROOT_SHA_EXPECTED = "8cc804bb31fcc29393ee4e06c79e9eb407f10917a7996440c6116e78df5aa670"
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_WORKLIST_PIN_SOURCE = json.loads(
    BASE_CENSUS_JSON.read_text(encoding="utf-8"))["worklist_regen_pins"]["scen"]

ADOPTED_COUNT = 1
ADOPTED_WIN = 1
ADOPTED_LOSS = 0
ADOPTED_NODES_TOTAL = 12755963
SERVING_CLASS = 3288
SERVING_CLASS_MASK = (1297036696978718720, 0)
LOSS_KEYS = {}
LOSS_S5_INDICES = {}
LOSS_OWNER_CLASSES = {}
WIN_KEYS = {
    "k01": (1297036696978718720, 64),
}
WIN_S5_INDICES = {"k01": 97250}
WIN_OWNER_CLASSES = {
    "k01": [2376, 3288, 17116],
}
EXPECTED_FLIPS = [2376, 3288, 17116]
EXPECTED_UNKNOWN_CHURN = []
EXPECTED_RANK_CHURN_COUNT = 0
EXPECTED_GREEDY_DELTA = [{"root": 2, "base": 6132, "scen": 6131}]


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
    assert (len(base), base_wins, base_loss) == (6889, 207, 6682)
    assert (len(scen), scen_wins, scen_loss) == (6890, 208, 6682)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "n11-eleventhcost-k01-win-adoption-manifest-v1"
    assert manifest["base"]["sha256"] == BASE_CACHE_SHA_EXPECTED
    assert (manifest["base"]["rows"], manifest["base"]["win"],
            manifest["base"]["loss"]) == (6889, 207, 6682)
    assert manifest["merger_sha256"] == MERGER_SHA_EXPECTED
    assert manifest["kits"]["replica"].startswith(
        "n11-eleventhcost-batch-stage1-2m-20261127")
    assert manifest["kits"]["cppgate"].startswith(
        "n11-eleventhcost-k01-win-cppgate-20261127")
    assert manifest["kits"]["thirdimpl"].startswith(
        "n11-eleventhcost-k01-win-thirdimpl-corroboration-20261127")
    adopted_rows = manifest["rows"]
    assert len(adopted_rows) == ADOPTED_COUNT
    assert manifest["expected_merged_shape"] == {"rows": 6890, "win": 208, "loss": 6682}
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
    # the eleventh-cost serving class owns the adopted row
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
    assert cb == {"unknown": 34391, "excluded_now": 129,
                  "free_now": 39, "excluded": 390}, cb
    assert cs == {"unknown": 34388, "excluded_now": 132,
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
        "the flip list must be exactly the WIN row's owner classes"
    for ci in flips:
        assert base_status[ci] == "unknown", ci
        assert scen_status[ci] == "excluded_now", ci
    out["status_flip_count"] = len(flips)
    # no free_now change and no other census movement
    assert cb["free_now"] == cs["free_now"] == 39
    assert cb["excluded"] == cs["excluded"] == 390
    assert cs["unknown"] == cb["unknown"] - len(flips)
    # the LOSS row's other owner classes keep their status
    for label, key in LOSS_KEYS.items():
        for ci in owner_classes[key]:
            if ci in (SERVING_CLASS,):
                continue
            assert base_status[ci] == scen_status[ci] == "unknown", ci

    # serving-class unknown arithmetic (graph-derived, class 2310)
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
    # the eleventh-cost selection class 1297036696978718720:0 held
    # 102 unknown children on the BASE head; adopting exactly its one
    # resolved key drops its cost-unknown 102 -> 101 and that WIN row
    # flips it unknown -> excluded_now (win-hit)
    assert serving_rows[str(cls)]["base_status"] == "unknown"
    assert serving_rows[str(cls)]["scen_status"] == "excluded_now"
    assert (serving_rows[str(cls)]["unknown_before"],
            serving_rows[str(cls)]["unknown_after"]) == (102, 101), cls
    assert serving_rows[str(cls)]["adopted_owned_here"] == 1
    out["serving_class_rows"] = serving_rows

    # closure-classes.csv churn (measured; this time NONE - the two
    # adopted rows sit outside every closure-ladder class)
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
    # MEASURED: no entered/left, NO unknown_now churn, NO rank churn;
    # the closure CSV is byte-identical to the BASE side
    assert entered == [], entered
    assert left == [], left
    assert unknown_churn == EXPECTED_UNKNOWN_CHURN, unknown_churn
    assert len(rank_churn) == EXPECTED_RANK_CHURN_COUNT, len(rank_churn)
    assert BASE_CLOSURE.read_text() == SCEN_CLOSURE.read_text(), \
        "closure-classes.csv must be byte-identical to the BASE side"
    out["closure_byte_identical_to_base"] = True
    # the flipped (excluded_now) classes never enter the ladder on
    # either side
    for ci in win_owner_union:
        assert ci not in bc and ci not in sc, ci
    out["loss_owner_class_union"] = sorted(
        {ci for k, v in incr.items() if v[0] == 2
         for ci in owner_classes[k]})

    # per-root coverage: free_now/uncovered identical on all 20 roots;
    # NO individual greedy re-route is measured (measured)
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
    # MEASURED: exactly one individual greedy re-route: root 2 drops
    # 6,132 -> 6,131 (the adopted WIN row removes one still-unknown
    # child from a root-2 greedy class union); free_now/uncovered are
    # identical on all 20 roots and every other root's greedy is
    # unchanged, so the per-root CSV is NOT byte-identical to the BASE
    # side (exactly one row differs: root 2)
    assert greedy_delta == EXPECTED_GREEDY_DELTA, greedy_delta
    out["per_root_coverage_byte_identical"] = \
        BASE_PERROOT.read_text() == SCEN_PERROOT.read_text()
    assert out["per_root_coverage_byte_identical"] is False
    bp_lines = BASE_PERROOT.read_text().splitlines()
    sp_lines = SCEN_PERROOT.read_text().splitlines()
    assert len(bp_lines) == len(sp_lines) == 21
    differing = [n for n, (a, b) in enumerate(zip(bp_lines, sp_lines)) if a != b]
    assert differing == [17], differing
    assert bp_lines[17] == "2,central,119,8,111,6132", bp_lines[17]
    assert sp_lines[17] == "2,central,119,8,111,6131", sp_lines[17]

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
    # MEASURED: the single adopted row sits OUTSIDE the frozen
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
    # measured: neither flipped class is an update8 plan group class,
    # so the win-hit group set is unchanged
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
    # row count is unchanged (content differs)
    assert out["joint_greedy"] == {"base": 37398, "scen": 37398}, \
        out["joint_greedy"]
    assert out["worklist_total"] == {"base": 64272, "scen": 64272}, \
        out["worklist_total"]

    # worklist regen pins (UNPUBLISHED per size policy; the BASE side is
    # the published ninth-cost census json's scen regen pin, the SCEN
    # side is this kit's local regen pin)
    swl = D / "reaudit/output/probe-worklist.csv"
    assert swl.is_file()
    out["worklist_regen_pins"] = {
        "base": BASE_WORKLIST_PIN_SOURCE,
        "scen": {"sha256": sha(swl), "size": swl.stat().st_size},
    }
    assert out["worklist_regen_pins"]["base"]["sha256"] == \
        "b9f3f1a370974fe1cd895304b8a328d1863656725718b2b938bc2aa2d48a3d33"
    assert out["worklist_regen_pins"]["base"]["size"] == 3715222
    assert out["worklist_regen_pins"]["scen"]["size"] == 3715222, \
        out["worklist_regen_pins"]["scen"]
    assert out["worklist_regen_pins"]["scen"]["sha256"] != \
        out["worklist_regen_pins"]["base"]["sha256"]

    out["verdict"] = {
        "part_declared": True,
        "part": "eleventhcost-k01-flip-census",
        "canonical_head_sha256": SCEN_CACHE_SHA_EXPECTED,
        "consumed": ("exactly the one published eleventh-cost row "
                     "(1 WIN k01)"),
        "status_flips": len(flips),
        "status_flip_mechanism": (
            "win-hit (the Part EW/EM mechanism): the adopted WIN row k01 "
            "(s5 index 97250) flips its three owner classes 2376 "
            "(1297036696977670144:64, cost-unknown 109 -> 108), 3288 (the "
            "eleventh-cost serving class 1297036696978718720:0, "
            "cost-unknown 102 -> 101, the adopted row owned here) and "
            "17116 (1152921504607895808:64, cost-unknown 99 -> 98) from "
            "unknown to excluded_now; no class flips to free_now, "
            "free_now stays 39 (Board-verified both sides); the closure "
            "ladder is byte-identical to the BASE side (804 rows, no "
            "entered/left, no unknown_now churn, no rank churn); the "
            "per-root coverage MEASURES one individual greedy re-route "
            "(root 2 drops 6132 -> 6131, free_now/uncovered identical "
            "on all 20 roots); joint greedy stays 37398 and the probing "
            "worklist row count stays 64272 (regen content sha differs "
            "from the BASE pin); the adopted s5 index sits outside the "
            "frozen update8 baseline requirement (resolved 282 -> 282, "
            "remaining_now 31444 -> 31444, groups_free_now 131 -> 131); "
            "the win-hit group set is unchanged (25)"),
        "census_counts_identical_to_published_summaries": True,
        "note": ("declared eleventh-cost k01 adoption measurement; "
                 "adopting solver-trusted S5 labels flips class-status "
                 "bookkeeping only: no root verdict is consumed, no root "
                 "freed, no root excluded, no coverage claim is made or "
                 "changed; 11x11 stays UNKNOWN; no root verdict; nodes "
                 "are bookkeeping"),
    }

    outp = D / "output/census-deltas-eleventhcost-k01-adoption.json"
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
