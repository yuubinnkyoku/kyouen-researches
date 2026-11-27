"""Ultra-cheap u03 adoption measurement: BASE (ultra-cheap u02 head
of record 82b52577...) vs SCENARIO (ultra-cheap u03 adoption union,
c5082866...) census deltas.

This follow-up Part is DECLARED in
n11-ultra-cheap-u03-adoption-reaudit-20261127/DECLARATION.md
(publish-then-execute, commit 7446f225): the ultra-cheap u03 canonical
adoption consumes exactly the one published row (1 WIN u03) and
advances the canonical head of record from 82b52577... (6,892 rows
WIN 210 / LOSS 6,682) to c5082866... (6,893 rows WIN 211 / LOSS
6,682).  This script is a disclosed structural adaptation of the
ultra-cheap u02 measurer; it MEASURES the census/scheduling delta of
that declared adoption, from published-byte-verbatim local inputs,
and cross-checks this kit's reaudit refresh outputs (byte-clone
refresh of the published u02 refresh, three byte-identical
determinism runs).

DEVIATION FROM THE PRE-REGISTERED EXPECTATION (disclosed in the
declaration BEFORE execution): the declaration pre-registered the
graph-derived THREE-owner union flip prediction (classes 16371,
16404 and 16930 all unknown -> excluded_now, census unknown 34,382
-> 34,379, excluded_now 138 -> 141).  The MEASURED census is unknown
34,382 -> 34,380, excluded_now 138 -> 140: exactly TWO classes flip
(16404 and 16930).  The serving class 16371 was ALREADY
excluded_now on the BASE head (its win-hit predates the u03
adoption; another of its 52 cost children is a known WIN in the
u02 head), so adopting the u03 row resolves its LAST unknown cost
child (unknown_now 1 -> 0, the class leaves the closure ladder 802
-> 801) without changing its census status.  The measured facts:

* SCEN cache must equal BASE cache rows + exactly the 1 increment
  row; the adopted row is fresh to BASE and matches the increment
  verdict/nodes exactly;
* the adoption manifest (n11-ultra-cheap-u03-win-adoption-manifest-v1)
  pins: base head 82b52577 (6,892/210/6,682), increment 0796a210,
  adopted 1 row WIN 1, nodes_total 2,909,040, the escalation and
  pillars kits and merger sha 90711961;
* the refresh status logic is replicated independently and must
  reproduce the refreshed class status census EXACTLY on both sides
  (BASE 34,382/138/39/390 unknown/excluded_now/free_now/excluded;
  SCEN 34,380/140/39/390);
* the single adopted row is a WIN (u03), so class-status flips are
  MEASURED: the measured flip list is exactly TWO of the THREE owner
  classes of the WIN key u03 (s5 index 550879): classes 16404
  (1154047404580798464:64, cost-unknown 98 -> 97) and 16930
  (1152921504875282432:272, cost-unknown 52 -> 51), each unknown ->
  excluded_now (the Part EW/EM win-hit mechanism); the third owner
  class, the serving class 16371 (1153202979851993088:16), keeps its
  BASE status excluded_now (already win-hit on the BASE head);
* no class flips to free_now and no free_now class is lost (39 -> 39,
  Board-verified both sides);
* closure-classes.csv churn is MEASURED: 802 -> 801 rows, entered [],
  left [16371] (the serving class leaves the closure ladder after
  resolving its last unknown child), one unknown_now churn (class
  16930: 52 -> 51) and 797 rank-churn cells (the ladder re-ranks
  behind the leaving class); the closure CSV is NOT byte-identical to
  the BASE side;
* per-root coverage MEASURES two individual greedy re-routes (root
  26: 5,228 -> 5,227, root 48: 2,893 -> 2,980; free_now/uncovered
  identical on all 20 roots); joint greedy 43,830 -> 43,830
  (unchanged) and the probing worklist row count 64,268 -> 64,266
  (the adopted key's TWO membership rows - serving classes 16371
  and 16930 - leave the worklist; scheduling quantities, not
  coverage claims);
* the adopted s5 index 550879 sits OUTSIDE the frozen update8
  baseline requirement (resolved 284 -> 284, remaining_now 31,332
  -> 31,332, groups_free_now 131 -> 131, win-hit group set 35 -> 35
  unchanged).

Fail-closed (assertions abort before the output json is written);
tamper battery 4/4 fail-closed.  The output json is
output/census-deltas-ultra-cheap-u03-adoption.json.

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
D = ROOT / "research/experiments/n11-ultra-cheap-u03-adoption-reaudit-20261127"
EV = ROOT / "research/experiments/n11-ultra-cheap-u02-adoption-reaudit-20261127"
T2 = ROOT / "research/experiments/n11-ultra-cheap-u03-win-adoption-20261127"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
MANIFEST = T2 / "adoption-manifest.json"
MERGER = ROOT / "research/experiments/n11-centralreply-sixthlossk38-adoption-reaudit-20261126/scripts/s5_union_merge.py"

BASE_CACHE = ROOT / "research/experiments/n11-ultra-cheap-u02-win-adoption-20261127/output/merged/merged-exact-s5-chain-plus-ultra-cheap-u02-20261127.cache"
SCEN_CACHE = T2 / "output/merged/merged-exact-s5-chain-plus-ultra-cheap-u03-20261127.cache"
INCREMENT = T2 / "output/increment-ultra-cheap-u03-adoption-20261127.cache"
BASE_SUMMARY = EV / "reaudit/output/refresh-summary.json"
SCEN_SUMMARY = D / "reaudit/output/refresh-summary.json"
BASE_CLOSURE = EV / "reaudit/output/closure-classes.csv"
SCEN_CLOSURE = D / "reaudit/output/closure-classes.csv"
BASE_PERROOT = EV / "reaudit/output/per-root-coverage.csv"
SCEN_PERROOT = D / "reaudit/output/per-root-coverage.csv"
BASE_CENSUS_JSON = EV / "output/census-deltas-ultra-cheap-u02-adoption.json"

BASE_CACHE_SHA_EXPECTED = "82b525777843ecb44c3857b034f7a135284c2587b42dbaa94aa295b01adc7509"
SCEN_CACHE_SHA_EXPECTED = "c5082866c1bb61e9cbcb86b80b29c3b2a141b4b5e93a0b8d4b46e04151b631c8"
INCREMENT_SHA_EXPECTED = "0796a210bfd7519922de2bad488fbd6fcb240d287183b8731f49e081afbd2b26"
MANIFEST_SHA_EXPECTED = "f09075f0c680635e45e2c8405d1f00f5b0de39367d0c15c457ce3d51445fa51e"
BASE_SUMMARY_SHA_EXPECTED = "722c70d89aa125b8abe089807d87b56a893d3fc6113ce42e7d99662b9b9da70d"
BASE_CLOSURE_SHA_EXPECTED = "535e2684c11e659a9f1c36d70094cd8e0567277c199c708ddd79d35cbf0849e1"
BASE_PERROOT_SHA_EXPECTED = "a5d0e9dee1ed842557344fb475e28f4bccfaffecc3230523b800fc5610eac57a"
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_WORKLIST_PIN_SOURCE = json.loads(
    BASE_CENSUS_JSON.read_text(encoding="utf-8"))["worklist_regen_pins"]["scen"]
BASE_WORKLIST_SHA_EXPECTED = "9fec423a4c62ce7cf5048b2e5c5f34ece768246e5e5fe2c39e5aeb4ab7689d6b"
BASE_WORKLIST_SIZE_EXPECTED = 3715002
SCEN_WORKLIST_SHA_EXPECTED = "ece167236cb3d6d76c9ab8c5c8a8fa20c324dff11a4368bc50bbe70c65438ef5"
SCEN_WORKLIST_SIZE_EXPECTED = 3714889

ADOPTED_COUNT = 1
ADOPTED_WIN = 1
ADOPTED_LOSS = 0
ADOPTED_NODES_TOTAL = 2909040
SERVING_CLASS = 16371
SERVING_CLASS_MASK = (1153202979851993088, 16)
LOSS_KEYS = {}
LOSS_S5_INDICES = {}
LOSS_OWNER_CLASSES = {}
WIN_KEYS = {
    "u03": (1153202979851993088, 272),
}
WIN_S5_INDICES = {"u03": 550879}
WIN_OWNER_CLASSES = {
    "u03": [16371, 16404, 16930],
}
EXPECTED_FLIPS = [16404, 16930]
EXPECTED_UNKNOWN_CHURN = [{"class_index": 16930, "base": 52, "scen": 51}]
EXPECTED_RANK_CHURN_COUNT = 797
EXPECTED_GREEDY_DELTA = [
    {"root": 26, "base": 5228, "scen": 5227},
    {"root": 48, "base": 2893, "scen": 2980},
]
EXPECTED_WIN_HIT_GROUP_ADDED = 0
BASE_CENSUS = {"unknown": 34382, "excluded_now": 138,
               "free_now": 39, "excluded": 390}
SCEN_CENSUS = {"unknown": 34380, "excluded_now": 140,
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
    assert (len(base), base_wins, base_loss) == (6892, 210, 6682)
    assert (len(scen), scen_wins, scen_loss) == (6893, 211, 6682)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "n11-ultra-cheap-u03-win-adoption-manifest-v1"
    assert manifest["base"]["sha256"] == BASE_CACHE_SHA_EXPECTED
    assert (manifest["base"]["rows"], manifest["base"]["win"],
            manifest["base"]["loss"]) == (6892, 210, 6682)
    assert manifest["merger_sha256"] == MERGER_SHA_EXPECTED
    assert manifest["kits"]["replica"].startswith(
        "n11-ultra-cheap-u03-escalation-15m-20261127")
    assert manifest["kits"]["pillars"].startswith(
        "n11-ultra-cheap-u03-win-pillars-20261127")
    adopted_rows = manifest["rows"]
    assert len(adopted_rows) == ADOPTED_COUNT
    assert manifest["expected_merged_shape"] == {"rows": 6893, "win": 211, "loss": 6682}
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
    # MEASURED DEVIATION from the declaration's graph-derived
    # prediction: only TWO of the THREE owner classes flip, because
    # the serving class 16371 was ALREADY excluded_now on the BASE
    # head (win-hit predates the u03 adoption)
    assert set(flips) < set(win_owner_union), \
        "the measured flip list must be a strict subset of the owner union"
    assert set(win_owner_union) - set(flips) == {SERVING_CLASS}, \
        "the only non-flipping owner class must be the serving class"
    for ci in flips:
        assert base_status[ci] == "unknown", ci
        assert scen_status[ci] == "excluded_now", ci
    assert base_status[SERVING_CLASS] == scen_status[SERVING_CLASS] \
        == "excluded_now", SERVING_CLASS
    out["status_flip_count"] = len(flips)
    out["status_flip_count_predicted_by_declaration"] = 3
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

    # serving-class unknown arithmetic (graph-derived, class 2251)
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
    # the ultra-cheap serving class 1153202979851993088:16 was ALREADY
    # excluded_now on the BASE head (another of its 52 cost children
    # is a known WIN in the u02 head, so the win-hit predates the u03
    # adoption) and held exactly ONE unknown child (the u03 key
    # itself); the adopted WIN row resolves that last unknown child
    # (unknown_now 1 -> 0, the class leaves the closure ladder) but
    # cannot change its already-excluded_now census status
    assert serving_rows[str(cls)]["base_status"] == "excluded_now"
    assert serving_rows[str(cls)]["scen_status"] == "excluded_now"
    assert (serving_rows[str(cls)]["unknown_before"],
            serving_rows[str(cls)]["unknown_after"]) == (1, 0), cls
    assert serving_rows[str(cls)]["adopted_owned_here"] == 1
    out["serving_class_rows"] = serving_rows

    # closure-classes.csv churn (measured; the serving class LEAVES
    # the ladder and class 14338 loses one unknown child)
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
    assert (len(bc), len(sc)) == (802, 801), (len(bc), len(sc))
    # MEASURED: the serving class 16371 leaves the ladder (its last
    # unknown child was the adopted key); class 16930 loses one
    # unknown child; the ladder re-ranks (797 cells)
    assert entered == [], entered
    assert left == [16371], left
    assert unknown_churn == EXPECTED_UNKNOWN_CHURN, unknown_churn
    assert len(rank_churn) == EXPECTED_RANK_CHURN_COUNT, len(rank_churn)
    assert BASE_CLOSURE.read_text() != SCEN_CLOSURE.read_text(), \
        "closure-classes.csv must NOT be byte-identical to the BASE side"
    out["closure_byte_identical_to_base"] = False
    # the leaving class was in the BASE ladder and is gone in SCEN;
    # the other flipped classes sit outside the ladder on both sides
    # (16404) or inside it with one fewer unknown child (16930)
    assert 16371 in bc and 16371 not in sc
    assert 16404 not in bc and 16404 not in sc
    assert 16930 in bc and 16930 in sc
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
    # MEASURED: root 48 grows 2,893 -> 2,980 and root 26 drops
    # 5,228 -> 5,227 (the serving class 16371 leaving the unknown
    # set re-routes both roots' greedy unions)
    assert greedy_delta == EXPECTED_GREEDY_DELTA, greedy_delta
    out["per_root_coverage_byte_identical"] = \
        BASE_PERROOT.read_text() == SCEN_PERROOT.read_text()
    assert out["per_root_coverage_byte_identical"] is False
    bp_lines = BASE_PERROOT.read_text().splitlines()
    sp_lines = SCEN_PERROOT.read_text().splitlines()
    assert len(bp_lines) == len(sp_lines) == 21
    differing = [n for n, (a, b) in enumerate(zip(bp_lines, sp_lines)) if a != b]
    assert differing == [6, 8], differing
    assert bp_lines[6] == "48,central,119,7,112,2893", bp_lines[6]
    assert sp_lines[6] == "48,central,119,7,112,2980", sp_lines[6]
    assert bp_lines[8] == "26,central,119,8,111,5228", bp_lines[8]
    assert sp_lines[8] == "26,central,119,8,111,5227", sp_lines[8]

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
    # MEASURED: the adopted s5 index 550879 sits OUTSIDE the frozen
    # update8 baseline requirement, so NO baseline s5 resolves
    assert new_resolved == set(), sorted(new_resolved)
    assert adopted_idx & baseline_req == set()
    assert adopted_idx - baseline_req == {550879}
    assert len(new_resolved) == (
        out["update8_refresh_scen"]["resolved"]
        - out["update8_refresh_base"]["resolved"]), "resolved delta"
    out["update8_refresh_base"]["resolved_list_len"] = len(base_req)
    out["update8_refresh_scen"]["resolved_list_len"] = len(scen_req)
    assert out["update8_refresh_base"]["resolved"] == 284
    assert out["update8_refresh_scen"]["resolved"] == 284
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
    # added or removed groups); none of the three owner classes
    # (16371, 16404, 16930) is an update8 plan group class
    assert out["win_hit_groups_identical"] is True
    assert len(b_groups) == 35, len(b_groups)
    assert len(s_groups) == 35, len(s_groups)
    assert len(added_groups) == EXPECTED_WIN_HIT_GROUP_ADDED
    assert removed_groups == [], removed_groups
    u8_group_classes = {gr["s4_class_index"]
                        for gr in scen_sum["frozen_update8_refresh"]["win_hit_groups"]}
    assert {16371, 16404, 16930}.isdisjoint(u8_group_classes)
    out["win_hit_groups_added"] = added_groups

    out["joint_greedy"] = {
        "base": base_sum["joint_greedy"]["greedy_union_size"],
        "scen": scen_sum["joint_greedy"]["greedy_union_size"],
    }
    out["worklist_total"] = {
        "base": base_sum["worklist_total"],
        "scen": scen_sum["worklist_total"],
    }
    # MEASURED: the joint greedy union is UNCHANGED (43,830 -> 43,830)
    # and the probing worklist row count drops 64,268 -> 64,266 (the
    # adopted key's TWO membership rows - serving classes 16371 and
    # 16930 - leave the worklist; scheduling quantities, not coverage
    # claims)
    assert out["joint_greedy"] == {"base": 43830, "scen": 43830}, \
        out["joint_greedy"]
    assert out["worklist_total"] == {"base": 64268, "scen": 64266}, \
        out["worklist_total"]

    # worklist regen pins (UNPUBLISHED per size policy; the BASE side is
    # the published ultra-cheap u01 census json's scen regen pin, the SCEN
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
    #    the serving class STAYS excluded_now (its win-hit comes from
    #    another known WIN cost child in the BASE head), but the two
    #    16404/16930 flips revert to unknown - the census must move
    scen_rows = []
    with SCEN_CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if (int(row[1]), int(row[2])) == WIN_KEYS["u03"]:
                assert int(row[4]) == 1
                row = row[:4] + ["2"] + row[5:]
            scen_rows.append(row)
    flipped = {}
    for row in scen_rows:
        lo, hi, stones, verdict, nodes = map(int, row[1:])
        flipped[(lo, hi)] = (verdict, nodes)
    tampered_census = counts_from(census(flipped))
    assert tampered_census != cs, "tamper 1 must change the census"
    assert census(flipped)[SERVING_CLASS] == "excluded_now", \
        "tamper 1: the serving class keeps its pre-existing win-hit"
    assert census(flipped)[16404] == "unknown" and \
        census(flipped)[16930] == "unknown", \
        "tamper 1: the owner-class flips must revert to unknown"
    tamper["verdict_flip_changes_census"] = True
    # 2. delete the adopted row from the SCEN copy: the recount must
    #    fall back to the BASE census exactly
    deleted = {k: v for k, v in flipped.items() if k != WIN_KEYS["u03"]}
    # (the flipped row is absent, so deletion restores the SCEN rows
    # minus the adopted row == BASE rows)
    assert counts_from(census(deleted)) == cb, \
        "tamper 2 must restore the BASE census"
    tamper["row_delete_restores_base_census"] = True
    # 3. append the adopted row to a BASE copy: the recount must equal
    #    the SCEN census exactly (the adoption is exactly this row)
    appended = dict(base)
    appended[WIN_KEYS["u03"]] = incr[WIN_KEYS["u03"]]
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
                     if (int(r[1]), int(r[2])) != WIN_KEYS["u03"]])
    h = hashlib.sha256
    assert h(t1).hexdigest() not in (BASE_CACHE_SHA_EXPECTED,
                                     SCEN_CACHE_SHA_EXPECTED)
    assert h(t2).hexdigest() not in (BASE_CACHE_SHA_EXPECTED,
                                     SCEN_CACHE_SHA_EXPECTED)
    tamper["tampered_caches_break_sha_gate"] = True
    out["tamper_battery"] = tamper

    out["verdict"] = {
        "part_declared": True,
        "part": "ultra-cheap-u03-flip-census",
        "canonical_head_sha256": SCEN_CACHE_SHA_EXPECTED,
        "consumed": ("exactly the one published ultra-cheap row "
                     "(1 WIN u03)"),
        "status_flips": len(flips),
        "deviation_from_predeclared_expectation": (
            "the declaration pre-registered the graph-derived "
            "THREE-owner union flip prediction (16371, 16404, 16930 "
            "all unknown -> excluded_now, census unknown 34,382 -> "
            "34,379, excluded_now 138 -> 141); the MEASURED flip count "
            "is TWO (16404 and 16930), because the serving class 16371 "
            "was ALREADY excluded_now on the BASE head (its win-hit "
            "predates the u03 adoption; the adopted row resolves its "
            "LAST unknown child, 1 -> 0, and the class leaves the "
            "closure ladder 802 -> 801 without changing census "
            "status); the measured census unknown 34,380 / "
            "excluded_now 140 supersedes the predicted 34,379 / 141"),
        "status_flip_mechanism": (
            "win-hit (the Part EW/EM mechanism): the adopted WIN row u03 "
            "(s5 index 550879) flips two of its three owner classes, "
            "16404 (1154047404580798464:64, cost-unknown 98 -> 97) and "
            "16930 (1152921504875282432:272, cost-unknown 52 -> 51, one "
            "unknown_now churn cell in the ladder), from unknown to "
            "excluded_now; the third owner class, the serving class "
            "16371 (1153202979851993088:16), was ALREADY excluded_now "
            "on the BASE head and keeps that status while the adopted "
            "row resolves its last unknown cost child (1 -> 0; the "
            "class leaves the closure ladder 802 -> 801); no class "
            "flips to free_now, free_now stays 39 (Board-verified both "
            "sides); the closure ladder re-ranks (797 cells); the "
            "per-root coverage MEASURES two individual greedy "
            "re-routes (root 26 drops 5,228 -> 5,227, root 48 grows "
            "2,893 -> 2,980, free_now/uncovered identical on all 20 "
            "roots); joint greedy is UNCHANGED at 43,830 (a "
            "scheduling quantity, not a coverage claim) and the "
            "probing worklist row count drops 64,268 -> 64,266 (the "
            "adopted key's two membership rows, serving classes 16371 "
            "and 16930, leave the worklist; regen content sha differs "
            "from the BASE pin); the adopted s5 index 550879 sits "
            "OUTSIDE the frozen update8 baseline requirement (resolved "
            "284 -> 284, remaining_now 31,332 -> 31,332, "
            "groups_free_now 131 -> 131); the win-hit group set is "
            "unchanged (35 -> 35, no added or removed groups)"),
        "census_counts_identical_to_published_summaries": True,
        "note": ("declared ultra-cheap u03 adoption measurement; "
                 "adopting solver-trusted S5 labels flips class-status "
                 "bookkeeping only: no root verdict is consumed, no root "
                 "freed, no root excluded, no coverage claim is made or "
                 "changed; 11x11 stays UNKNOWN; no root verdict; nodes "
                 "are bookkeeping"),
    }

    outp = D / "output/census-deltas-ultra-cheap-u03-adoption.json"
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
