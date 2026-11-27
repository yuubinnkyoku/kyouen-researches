"""Ultra-cheap u01 adoption measurement: BASE (eleventh-cost k01 head
of record 1e2eeda2...) vs SCENARIO (ultra-cheap u01 adoption union,
0ec4080d...) census deltas.

This follow-up Part is DECLARED in
n11-ultra-cheap-u01-adoption-reaudit-20261127/DECLARATION.md
(publish-then-execute, commit 740c980b): the ultra-cheap canonical
adoption consumes exactly the one published row (1 WIN u01) and
advances the canonical head of record from 1e2eeda2... (6,890 rows
WIN 208 / LOSS 6,682) to 0ec4080d... (6,891 rows WIN 209 / LOSS
6,682).  This script is a disclosed structural adaptation of the
eleventh-cost k01 measurer f286f165...; it MEASURES the
census/scheduling delta of that declared adoption, from
published-byte-verbatim local inputs, and cross-checks this kit's
reaudit refresh outputs (byte-clone refresh of the published
eleventh-cost k01 refresh 0355d7fb..., three byte-identical
determinism runs).

DEVIATION FROM THE PRE-REGISTERED EXPECTATION (disclosed in the
declaration BEFORE execution): the declaration predicted a single
class flip (unknown 34,388 -> 34,387, excluded_now 132 -> 133).
The MEASURED census is unknown 34,388 -> 34,385, excluded_now
132 -> 135: the adopted WIN key u01 (s5 index 81011) has THREE
owner classes, not one.  The measured facts:

* SCEN cache must equal BASE cache rows + exactly the 1 increment
  row; the adopted row is fresh to BASE and matches the increment
  verdict/nodes exactly;
* the adoption manifest (n11-ultra-cheap-u01-win-adoption-manifest-v1)
  pins: base head 1e2eeda2 (6,890/208/6,682), increment 5d2d89dd,
  adopted 1 row WIN 1, nodes_total 4,893,014, the replica and
  pillars kits and merger sha 90711961;
* the refresh status logic is replicated independently and must
  reproduce the refreshed class status census EXACTLY on both sides
  (BASE 34,388/132/39/390 unknown/excluded_now/free_now/excluded;
  SCEN 34,385/135/39/390);
* the single adopted row is a WIN (u01), so class-status flips are
  MEASURED: the measured flip list is exactly the THREE owner
  classes of the WIN key u01 (s5 index 81011): classes 1849 (the
  ultra-cheap serving class 1152922672972169216:0, cost-unknown
  1 -> 0, the adopted row owned here), 1858
  (1153484523413962752:0, cost-unknown 96 -> 95) and 5160
  (1153485622791372800:0, cost-unknown 56 -> 55), each unknown ->
  excluded_now (the Part EW/EM win-hit mechanism);
* no class flips to free_now and no free_now class is lost (39 -> 39,
  Board-verified both sides);
* closure-classes.csv churn is MEASURED: 804 -> 803 rows, entered [],
  left [1849] (the serving class leaves the closure ladder), one
  unknown_now churn (class 5160: 56 -> 55) and 785 rank-churn cells
  (the ladder re-ranks behind the leaving class); the closure CSV is
  NOT byte-identical to the BASE side;
* per-root coverage: free_now/uncovered identical on all 20 roots but
  this adoption MEASURES two individual greedy re-routes: root 36's
  individual greedy union grows 3,001 -> 3,029 and root 49's drops
  2,696 -> 2,693; the per-root CSV is NOT byte-identical to the BASE
  side (exactly two rows differ);
* the update8 refresh fields: the adopted s5 index 81011 sits INSIDE
  the frozen baseline requirement, so resolved moves 282 -> 283
  (new_resolved == [81011]) and remaining_now 31,444 -> 31,388;
  the win-hit group set is NOT unchanged (25 -> 31 groups; six added
  groups, all owned by the flipped class 5160); groups_free_now stays
  131;
* joint greedy is MEASURED to move 37,398 -> 43,776 and the probing
  worklist row count 64,272 -> 64,270 (regen content sha differs from
  the BASE pin 407a340f.../3,715,222 bytes; SCEN regen is
  5feaba28.../3,715,117 bytes - the adopted key's probe row leaves
  the worklist);
* tamper battery (fail-closed): flipping the adopted row's verdict
  in a SCEN copy, deleting the row, or appending it to a BASE copy
  each changes the independent census recount and/or breaks the
  sha-pinned gate; the measurement refuses tampered inputs.

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
D = ROOT / "research/experiments/n11-ultra-cheap-u01-adoption-reaudit-20261127"
EV = ROOT / "research/experiments/n11-eleventhcost-k01-adoption-reaudit-20261127"
T2 = ROOT / "research/experiments/n11-ultra-cheap-u01-win-adoption-20261127"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
MANIFEST = T2 / "adoption-manifest.json"
MERGER = ROOT / "research/experiments/n11-centralreply-sixthlossk38-adoption-reaudit-20261126/scripts/s5_union_merge.py"

BASE_CACHE = ROOT / "research/experiments/n11-eleventhcost-k01-win-adoption-20261127/output/merged/merged-exact-s5-chain-plus-eleventhcost-k01-20261127.cache"
SCEN_CACHE = T2 / "output/merged/merged-exact-s5-chain-plus-ultra-cheap-u01-20261127.cache"
INCREMENT = T2 / "output/increment-ultra-cheap-u01-adoption-20261127.cache"
BASE_SUMMARY = EV / "reaudit/output/refresh-summary.json"
SCEN_SUMMARY = D / "reaudit/output/refresh-summary.json"
BASE_CLOSURE = EV / "reaudit/output/closure-classes.csv"
SCEN_CLOSURE = D / "reaudit/output/closure-classes.csv"
BASE_PERROOT = EV / "reaudit/output/per-root-coverage.csv"
SCEN_PERROOT = D / "reaudit/output/per-root-coverage.csv"
BASE_CENSUS_JSON = EV / "output/census-deltas-eleventhcost-k01-adoption.json"

BASE_CACHE_SHA_EXPECTED = "1e2eeda2db33738de99612531f9bb67456f90c81ceedf123c8bbba117aff2a17"
SCEN_CACHE_SHA_EXPECTED = "0ec4080da825a344a8dbbe0835da80dd506b06fa45f9f926b401d2387f3ed1e5"
INCREMENT_SHA_EXPECTED = "5d2d89dd46032687f1f228e841578f02cbd1080c993bcdc294a0d9fbb0cd3132"
MANIFEST_SHA_EXPECTED = "afda1015250664d2aa5ef26c2eb121efe3db1aa21ba20842a92d5b21ebb0d40c"
BASE_SUMMARY_SHA_EXPECTED = "abaf62aadbdd4b41203d1bff7d362010ff83b4aae82114cdd0eaff67fab5b79e"
BASE_CLOSURE_SHA_EXPECTED = "d7ae77ddd05d433c0a59555f86efb009e64a5651ad6b918407682bdc5f3178f0"
BASE_PERROOT_SHA_EXPECTED = "03fd32f2ff8da948a5e8df825b049f6e890749105ab6370dbaef2595d0f1ea2c"
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_WORKLIST_PIN_SOURCE = json.loads(
    BASE_CENSUS_JSON.read_text(encoding="utf-8"))["worklist_regen_pins"]["scen"]
BASE_WORKLIST_SHA_EXPECTED = "407a340fdb9cc4db8b1d806fe13e4a2228b6783c974d1a54000029159475ff85"
BASE_WORKLIST_SIZE_EXPECTED = 3715222
SCEN_WORKLIST_SHA_EXPECTED = "5feaba280720a1ded80c95e50669162dad7aa0045357a9bceada92373214d0f6"
SCEN_WORKLIST_SIZE_EXPECTED = 3715117

ADOPTED_COUNT = 1
ADOPTED_WIN = 1
ADOPTED_LOSS = 0
ADOPTED_NODES_TOTAL = 4893014
SERVING_CLASS = 1849
SERVING_CLASS_MASK = (1152922672972169216, 0)
LOSS_KEYS = {}
LOSS_S5_INDICES = {}
LOSS_OWNER_CLASSES = {}
WIN_KEYS = {
    "u01": (1153485622925590528, 0),
}
WIN_S5_INDICES = {"u01": 81011}
WIN_OWNER_CLASSES = {
    "u01": [1849, 1858, 5160],
}
EXPECTED_FLIPS = [1849, 1858, 5160]
EXPECTED_UNKNOWN_CHURN = [{"class_index": 5160, "base": 56, "scen": 55}]
EXPECTED_RANK_CHURN_COUNT = 785
EXPECTED_GREEDY_DELTA = [
    {"root": 36, "base": 3001, "scen": 3029},
    {"root": 49, "base": 2696, "scen": 2693},
]
EXPECTED_WIN_HIT_GROUP_ADDED = 6
BASE_CENSUS = {"unknown": 34388, "excluded_now": 132,
               "free_now": 39, "excluded": 390}
SCEN_CENSUS = {"unknown": 34385, "excluded_now": 135,
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
    assert (len(base), base_wins, base_loss) == (6890, 208, 6682)
    assert (len(scen), scen_wins, scen_loss) == (6891, 209, 6682)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "n11-ultra-cheap-u01-win-adoption-manifest-v1"
    assert manifest["base"]["sha256"] == BASE_CACHE_SHA_EXPECTED
    assert (manifest["base"]["rows"], manifest["base"]["win"],
            manifest["base"]["loss"]) == (6890, 208, 6682)
    assert manifest["merger_sha256"] == MERGER_SHA_EXPECTED
    assert manifest["kits"]["replica"].startswith(
        "n11-ultra-cheap-batch-stage1-2m-20261127")
    assert manifest["kits"]["pillars"].startswith(
        "n11-ultra-cheap-u01-win-pillars-20261127")
    adopted_rows = manifest["rows"]
    assert len(adopted_rows) == ADOPTED_COUNT
    assert manifest["expected_merged_shape"] == {"rows": 6891, "win": 209, "loss": 6682}
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
    assert cb == BASE_CENSUS, cb
    assert cs == SCEN_CENSUS, cs

    # WIN-side flips (Part EW/EM win-hit mechanism): MEASURED.
    # Every flip must be an owner class of a WIN row and must go
    # unknown -> excluded_now; no other flip direction may occur.
    # MEASURED DEVIATION from the declaration's pre-registered
    # expectation (which predicted ONE flip): the WIN key has THREE
    # owner classes, so THREE classes flip.
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
    out["status_flip_count_predicted_by_declaration"] = 1
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

    # serving-class unknown arithmetic (graph-derived, class 1849)
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
    # the ultra-cheap serving class 1152922672972169216:0 held exactly
    # ONE unknown child on the BASE head (the u01 key itself); the
    # adopted WIN row resolves it, but a WIN cannot free a class, so
    # the class flips unknown -> excluded_now (win-hit), NOT free_now
    assert serving_rows[str(cls)]["base_status"] == "unknown"
    assert serving_rows[str(cls)]["scen_status"] == "excluded_now"
    assert (serving_rows[str(cls)]["unknown_before"],
            serving_rows[str(cls)]["unknown_after"]) == (1, 0), cls
    assert serving_rows[str(cls)]["adopted_owned_here"] == 1
    out["serving_class_rows"] = serving_rows

    # closure-classes.csv churn (measured; the serving class LEAVES
    # the ladder and class 5160 loses one unknown child)
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
    assert (len(bc), len(sc)) == (804, 803), (len(bc), len(sc))
    # MEASURED: the serving class 1849 leaves the ladder; class 5160
    # loses one unknown child; the ladder re-ranks (785 cells)
    assert entered == [], entered
    assert left == [1849], left
    assert unknown_churn == EXPECTED_UNKNOWN_CHURN, unknown_churn
    assert len(rank_churn) == EXPECTED_RANK_CHURN_COUNT, len(rank_churn)
    assert BASE_CLOSURE.read_text() != SCEN_CLOSURE.read_text(), \
        "closure-classes.csv must NOT be byte-identical to the BASE side"
    out["closure_byte_identical_to_base"] = False
    # the leaving class was in the BASE ladder and is gone in SCEN;
    # the other flipped classes sit outside the ladder on both sides
    # (1858) or inside it with one fewer unknown child (5160)
    assert 1849 in bc and 1849 not in sc
    assert 1858 not in bc and 1858 not in sc
    assert 5160 in bc and 5160 in sc
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
    # MEASURED: root 36 grows 3,001 -> 3,029 and root 49 drops
    # 2,696 -> 2,693 (the serving class 1849 leaving the unknown set
    # re-routes both roots' individual greedy unions)
    assert greedy_delta == EXPECTED_GREEDY_DELTA, greedy_delta
    out["per_root_coverage_byte_identical"] = \
        BASE_PERROOT.read_text() == SCEN_PERROOT.read_text()
    assert out["per_root_coverage_byte_identical"] is False
    bp_lines = BASE_PERROOT.read_text().splitlines()
    sp_lines = SCEN_PERROOT.read_text().splitlines()
    assert len(bp_lines) == len(sp_lines) == 21
    differing = [n for n, (a, b) in enumerate(zip(bp_lines, sp_lines)) if a != b]
    assert differing == [2, 11], differing
    assert bp_lines[2] == "49,central,119,10,109,2696", bp_lines[2]
    assert sp_lines[2] == "49,central,119,10,109,2693", sp_lines[2]
    assert bp_lines[11] == "36,central,119,4,115,3001", bp_lines[11]
    assert sp_lines[11] == "36,central,119,4,115,3029", sp_lines[11]

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
    # MEASURED: the adopted s5 index 81011 sits INSIDE the frozen
    # update8 baseline requirement, so exactly one baseline s5
    # resolves
    assert new_resolved == {81011}, sorted(new_resolved)
    assert adopted_idx & baseline_req == {81011}
    assert adopted_idx - baseline_req == set()
    assert len(new_resolved) == (
        out["update8_refresh_scen"]["resolved"]
        - out["update8_refresh_base"]["resolved"]), "resolved delta"
    out["update8_refresh_base"]["resolved_list_len"] = len(base_req)
    out["update8_refresh_scen"]["resolved_list_len"] = len(scen_req)
    assert out["update8_refresh_base"]["resolved"] == 282
    assert out["update8_refresh_scen"]["resolved"] == 283
    assert out["update8_refresh_base"]["remaining"] == 31444
    assert out["update8_refresh_scen"]["remaining"] == 31388
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
    # MEASURED: the win-hit group set GROWS by six groups, all owned
    # by the flipped class 5160 (an update8 plan group class); the
    # other flipped classes (1849, 1858) are not plan group classes
    assert out["win_hit_groups_identical"] is False
    assert len(b_groups) == 25, len(b_groups)
    assert len(s_groups) == 31, len(s_groups)
    assert len(added_groups) == EXPECTED_WIN_HIT_GROUP_ADDED
    assert removed_groups == [], removed_groups
    assert all(g[4] == 5160 for g in added_groups), added_groups
    u8_group_classes = {gr["s4_class_index"]
                        for gr in scen_sum["frozen_update8_refresh"]["win_hit_groups"]}
    assert {1849, 1858}.isdisjoint(u8_group_classes)
    out["win_hit_groups_added"] = added_groups

    out["joint_greedy"] = {
        "base": base_sum["joint_greedy"]["greedy_union_size"],
        "scen": scen_sum["joint_greedy"]["greedy_union_size"],
    }
    out["worklist_total"] = {
        "base": base_sum["worklist_total"],
        "scen": scen_sum["worklist_total"],
    }
    # MEASURED: the joint greedy union grows 37,398 -> 43,776 (the
    # greedy re-routes behind the leaving serving class; a scheduling
    # quantity, not a coverage claim) and the probing worklist row
    # count drops 64,272 -> 64,270 (the adopted key's probe row
    # leaves the worklist)
    assert out["joint_greedy"] == {"base": 37398, "scen": 43776}, \
        out["joint_greedy"]
    assert out["worklist_total"] == {"base": 64272, "scen": 64270}, \
        out["worklist_total"]

    # worklist regen pins (UNPUBLISHED per size policy; the BASE side is
    # the published eleventh-cost census json's scen regen pin, the SCEN
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
    #    the serving class would become free_now (all children
    #    resolved LOSS) - the census must move
    scen_rows = []
    with SCEN_CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if (int(row[1]), int(row[2])) == WIN_KEYS["u01"]:
                assert int(row[4]) == 1
                row = row[:4] + ["2"] + row[5:]
            scen_rows.append(row)
    flipped = {}
    for row in scen_rows:
        lo, hi, stones, verdict, nodes = map(int, row[1:])
        flipped[(lo, hi)] = (verdict, nodes)
    tampered_census = counts_from(census(flipped))
    assert tampered_census != cs, "tamper 1 must change the census"
    assert census(flipped)[SERVING_CLASS] == "free_now", \
        "tamper 1: the serving class would become free_now, not excluded_now"
    tamper["verdict_flip_changes_census"] = True
    # 2. delete the adopted row from the SCEN copy: the recount must
    #    fall back to the BASE census exactly
    deleted = {k: v for k, v in flipped.items() if k != WIN_KEYS["u01"]}
    # (the flipped row is absent, so deletion restores the SCEN rows
    # minus the adopted row == BASE rows)
    assert counts_from(census(deleted)) == cb, \
        "tamper 2 must restore the BASE census"
    tamper["row_delete_restores_base_census"] = True
    # 3. append the adopted row to a BASE copy: the recount must equal
    #    the SCEN census exactly (the adoption is exactly this row)
    appended = dict(base)
    appended[WIN_KEYS["u01"]] = incr[WIN_KEYS["u01"]]
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
                     if (int(r[1]), int(r[2])) != WIN_KEYS["u01"]])
    h = hashlib.sha256
    assert h(t1).hexdigest() not in (BASE_CACHE_SHA_EXPECTED,
                                     SCEN_CACHE_SHA_EXPECTED)
    assert h(t2).hexdigest() not in (BASE_CACHE_SHA_EXPECTED,
                                     SCEN_CACHE_SHA_EXPECTED)
    tamper["tampered_caches_break_sha_gate"] = True
    out["tamper_battery"] = tamper

    out["verdict"] = {
        "part_declared": True,
        "part": "ultra-cheap-u01-flip-census",
        "canonical_head_sha256": SCEN_CACHE_SHA_EXPECTED,
        "consumed": ("exactly the one published ultra-cheap row "
                     "(1 WIN u01)"),
        "status_flips": len(flips),
        "deviation_from_predeclared_expectation": (
            "the declaration pre-registered ONE class flip; the "
            "MEASURED flip count is THREE (the WIN key u01, s5 index "
            "81011, has three owner classes: the serving class 1849 "
            "plus 1858 and 5160); the measured census unknown 34,385 / "
            "excluded_now 135 supersedes the predicted 34,387 / 133"),
        "status_flip_mechanism": (
            "win-hit (the Part EW/EM mechanism): the adopted WIN row u01 "
            "(s5 index 81011) flips its three owner classes 1849 (the "
            "ultra-cheap serving class 1152922672972169216:0, "
            "cost-unknown 1 -> 0, the adopted row owned here; the class "
            "leaves the closure ladder 804 -> 803), 1858 "
            "(1153484523413962752:0, cost-unknown 96 -> 95) and 5160 "
            "(1153485622791372800:0, cost-unknown 56 -> 55, one "
            "unknown_now churn cell in the ladder, six new win-hit "
            "groups) from unknown to excluded_now; no class flips to "
            "free_now, free_now stays 39 (Board-verified both sides); "
            "the closure ladder re-ranks (785 cells); the per-root "
            "coverage MEASURES two individual greedy re-routes (root "
            "36 grows 3,001 -> 3,029, root 49 drops 2,696 -> 2,693, "
            "free_now/uncovered identical on all 20 roots); joint "
            "greedy moves 37,398 -> 43,776 (a scheduling quantity, "
            "not a coverage claim) and the probing worklist row count "
            "drops 64,272 -> 64,270 (regen content sha differs from "
            "the BASE pin); the adopted s5 index 81011 sits INSIDE "
            "the frozen update8 baseline requirement (resolved 282 -> "
            "283, remaining_now 31,444 -> 31,388, groups_free_now 131 "
            "-> 131); the win-hit group set grows 25 -> 31 (six added "
            "groups, all owned by class 5160)"),
        "census_counts_identical_to_published_summaries": True,
        "note": ("declared ultra-cheap u01 adoption measurement; "
                 "adopting solver-trusted S5 labels flips class-status "
                 "bookkeeping only: no root verdict is consumed, no root "
                 "freed, no root excluded, no coverage claim is made or "
                 "changed; 11x11 stays UNKNOWN; no root verdict; nodes "
                 "are bookkeeping"),
    }

    outp = D / "output/census-deltas-ultra-cheap-u01-adoption.json"
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
