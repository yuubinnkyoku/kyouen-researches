"""Twentieth ladder-top k01 adoption measurement: BASE (class-20421
k05 head of record e1a9cacc...) vs SCENARIO (twentieth k01 adoption
union, 1f1430f3...) census deltas.

Part of the kit n11-twentieth-ladder-top-k01-adoption-reaudit-20261128
(declaration commit 2b96c5d9, publish-then-execute): the twentieth
ladder-top k01 canonical adoption consumes exactly the single
published 15M escalation row (1 WIN: k01 10376293541479448576:68719476736,
s5 index 38891, serving class 34269) and advances the canonical head
of record from e1a9cacc... (6,905 rows WIN 223 / LOSS 6,682) to
1f1430f3... (6,906 rows WIN 224 / LOSS 6,682).

This measurer is a structural descendant of the published class20421
k05 measurer (kit n11-class20421-k05-adoption-reaudit-20261128): it
MEASURES the census/scheduling delta of adopting the row, against the
published class20421 k05 adoption-reaudit refresh outputs (BASE side)
and this kit's three byte-identical SCEN refresh runs (byte-clone
refresh differing from the class20421 k05 refresh in three regions:
docstring, CACHE path, expected cache sha).

Fail-closed pins verified before any census is written: the frozen
dependency graph, the update8 repaired joint plan, the fail-closed
union merger (90711961...), the adoption manifest
(n11-twentieth-ladder-top-k01-win-adoption-manifest-v1) pins:
base head e1a9cacc (6,905/223/6,682), increment 57c5314a,
expected merged shape 6,906/224/6,682, the BASE-side class20421 k05
adoption-reaudit kit outputs (summary dae1f1b3, closure a33f0cb9,
per-root ecfe4a0c, census json 86c2f36b, BASE worklist regen pin
09865553 unpublished per size policy), and the SCEN-side outputs of
this kit.

The adopted row is WIN (k01), so class-status flips are win-hit
flips (the Part EW/EM mechanism).  MEASURED (the declaration's
naive TWO-flip prediction HOLDS EXACTLY): the WIN key has owner
union classes 769, 34269; UNLIKE the k05 adoption the serving class
34269 is NOT pre-excluded at BASE (it is unknown, ladder rank 1,
unknown_now 11) and becomes win-hit by its OWN adopted child, so
exactly TWO owner classes flip unknown -> excluded_now (769 and
34269; census unknown 34,352 -> 34,350, excluded_now 168 -> 170,
free_now 39 unchanged).  The serving class 34269 STAYS in the
closure ladder (797 -> 797 rows, entered [], left []; its
unknown_now drops 11 -> 10, it keeps rank 1; NO ladder EXIT, NO
rank churn at all - zero churn cells); 769 sits OUTSIDE the ladder
on both sides.  The adopted s5 index 38891 sits INSIDE the frozen
update8 baseline requirement (resolved 291 -> 292, groups_free_now
131 unchanged; DEVIATION FROM THE DECLARATION'S NAIVE PREDICTION,
MEASURED AND DISCLOSED: remaining_now drops 31,332 -> 31,321 and
the win-hit group set grows 35 -> 40 - the serving class 34269 IS
an update8 plan group class, so its own adoption win-hits its 5
plan groups and removes their 10 further unknown children from the
remaining requirement; the other owner class 769 is NOT a plan
group class).  The per-root coverage MEASURES two individual
greedy re-routes (root 24 drops 2,775 -> 2,774 and root 12 drops
2,931 -> 2,930, scheduling re-route churns, NOT coverage claims;
free_now/uncovered identical on all 20 roots); the joint greedy
union MEASURES 43,184 -> 43,183; the probing worklist row count
drops 64,251 -> 64,250.

Fail-closed (assertions abort before the output json is written);
tamper battery 4/4 fail-closed.  The output json is
output/census-deltas-twentieth-k01-adoption.json.

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
D = ROOT / "research/experiments/n11-twentieth-ladder-top-k01-adoption-reaudit-20261128"
EV = ROOT / "research/experiments/n11-class20421-k05-adoption-reaudit-20261128"
T2 = ROOT / "research/experiments/n11-twentieth-ladder-top-k01-adoption-20261128"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
MANIFEST = T2 / "adoption-manifest.json"
MERGER = ROOT / "research/experiments/n11-centralreply-sixthlossk38-adoption-reaudit-20261126/scripts/s5_union_merge.py"

BASE_CACHE = ROOT / "research/experiments/n11-class20421-k05-adoption-20261128/output/merged/merged-exact-s5-chain-plus-class20421-k05-20261128.cache"
SCEN_CACHE = T2 / "output/merged/merged-exact-s5-chain-plus-twentieth-k01-20261128.cache"
INCREMENT = T2 / "output/increment-twentieth-ladder-top-k01-adoption-20261128.cache"
BASE_SUMMARY = EV / "reaudit/output/refresh-summary.json"
SCEN_SUMMARY = D / "reaudit/output/refresh-summary.json"
BASE_CLOSURE = EV / "reaudit/output/closure-classes.csv"
SCEN_CLOSURE = D / "reaudit/output/closure-classes.csv"
BASE_PERROOT = EV / "reaudit/output/per-root-coverage.csv"
SCEN_PERROOT = D / "reaudit/output/per-root-coverage.csv"
BASE_CENSUS_JSON = EV / "output/census-deltas-class20421-k05-adoption.json"

BASE_CACHE_SHA_EXPECTED = "e1a9cacc54abad5198e455ff53492310fabc28f5f89cf26363a7f3da7fe944de"
SCEN_CACHE_SHA_EXPECTED = "1f1430f3ef808af78b4919a0aea97b2d5075957603ecc4668ad21b3407a63faa"
INCREMENT_SHA_EXPECTED = "57c5314a931c53bd07d3cf8b0a79f8a3d67157e930285038a19fe653e05a9586"
MANIFEST_SHA_EXPECTED = "d687030bc6237f62f322bd3fcf4270001d9db5f5cf9eeca604121ca215ca9296"
BASE_SUMMARY_SHA_EXPECTED = "dae1f1b3b75ac7be7f00c502243130e9c2f87207fb36f1239528dbb8eda2120c"
BASE_CLOSURE_SHA_EXPECTED = "a33f0cb9d8b9e3dabe996b82b7e97d8cb65cc1f8795183aa1fde8e9e45eade19"
BASE_PERROOT_SHA_EXPECTED = "ecfe4a0c471a4f27b92977ca02a623256c6739077769235c56fd2d3156cd9a93"
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_WORKLIST_PIN_SOURCE = json.loads(
    BASE_CENSUS_JSON.read_text(encoding="utf-8"))["worklist_regen_pins"]["scen"]
BASE_WORKLIST_SHA_EXPECTED = "098655539bc681b5974a9b78def686eb95d3e735317caa09b63e74c58796f2ad"
BASE_WORKLIST_SIZE_EXPECTED = 3714021
SCEN_WORKLIST_SHA_EXPECTED = "55778a3f4067d696ae88e9315fdee59f4dfff6ad00136f03404744a1e8b949f7"
SCEN_WORKLIST_SIZE_EXPECTED = 3713956

ADOPTED_COUNT = 1
ADOPTED_WIN = 1
ADOPTED_LOSS = 0
ADOPTED_NODES_TOTAL = 10752246
SERVING_CLASS = 34269
SERVING_CLASS_MASK = (1152921504624672768, 68719476736)
LOSS_KEYS = {}
LOSS_S5_INDICES = {}
LOSS_OWNER_CLASSES = {}
WIN_KEYS = {
    "k01": (10376293541479448576, 68719476736),
}
WIN_S5_INDICES = {"k01": 38891}
WIN_OWNER_CLASSES = {
    "k01": [769, 34269],
}
EXPECTED_FLIPS = [769, 34269]
EXPECTED_UNKNOWN_CHURN = [
    {"class_index": 34269, "base": 11, "scen": 10},
]
EXPECTED_RANK_CHURN_COUNT = 0
EXPECTED_GREEDY_DELTA = [
    {"root": 12, "base": 2931, "scen": 2930},
    {"root": 24, "base": 2775, "scen": 2774},
]
EXPECTED_WIN_HIT_GROUP_ADDED = 5
BASE_CENSUS = {"unknown": 34352, "excluded_now": 168,
               "free_now": 39, "excluded": 390}
SCEN_CENSUS = {"unknown": 34350, "excluded_now": 170,
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
    assert (len(base), base_wins, base_loss) == (6905, 223, 6682)
    assert (len(scen), scen_wins, scen_loss) == (6906, 224, 6682)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "n11-twentieth-ladder-top-k01-win-adoption-manifest-v1"
    assert manifest["base"]["sha256"] == BASE_CACHE_SHA_EXPECTED
    assert (manifest["base"]["rows"], manifest["base"]["win"],
            manifest["base"]["loss"]) == (6905, 223, 6682)
    assert manifest["merger_sha256"] == MERGER_SHA_EXPECTED
    assert manifest["kits"]["replica"].startswith(
        "n11-twentieth-ladder-top-escalation-20261128")
    assert manifest["kits"]["cppgate"].startswith(
        "n11-twentieth-ladder-top-k01-win-cppgate-20261128")
    assert manifest["kits"]["thirdimpl"].startswith(
        "n11-twentieth-ladder-top-k01-thirdimpl-20261128")
    # disclosed in the adoption completion log: the k05 thirdimpl
    # cross-check pins ride in the kit ids; the manifest correctly
    # carries no separate xhost kit entry
    assert "xhost" not in manifest["kits"]
    assert manifest["owner_union_precheck"].startswith(
        "[769, 34269] re-derived from the frozen graph in the "
        "twentieth escalation Part; caveat: shared-owner "
        "pre-exclusion (other owner classes may already be "
        "excluded_now on BASE); this adoption resolves one "
        "cost-unknown of the serving class 34269")
    adopted_rows = manifest["rows"]
    assert len(adopted_rows) == ADOPTED_COUNT
    assert manifest["expected_merged_shape"] == {"rows": 6906, "win": 224, "loss": 6682}
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
    # MEASURED: the declaration's naive TWO-flip prediction HOLDS
    # EXACTLY: UNLIKE the k05 adoption the serving class 34269 is
    # NOT pre-excluded at BASE (unknown, ladder rank 1), so BOTH
    # owner-union classes flip (769 via its child, 34269 via its
    # OWN adopted child).
    flips = sorted(ci for ci in base_status
                   if base_status[ci] != scen_status[ci])
    out["status_flips"] = [
        {"class_index": ci, "base": base_status[ci], "scen": scen_status[ci],
         "class_mask": s4_masks[ci]}
        for ci in flips]
    assert flips == EXPECTED_FLIPS, flips
    win_owner_union = sorted({ci for key in WIN_KEYS.values()
                              for ci in owner_classes[key]})
    # the measured flip list EQUALS the owner union: NO owner class
    # is pre-excluded at BASE in this Part (the declaration's
    # caveat (shared-owner pre-exclusion) does NOT materialise
    # here; both owner classes are unknown at BASE)
    assert set(flips) == set(win_owner_union), \
        "the measured flip list must equal the owner union here"
    assert set(flips) == {769, 34269}, flips
    for ci in (769, 34269):
        assert base_status[ci] == "unknown", ci
        assert scen_status[ci] == "excluded_now", ci
    # the serving class 34269 IS one of the flipping classes (it
    # becomes win-hit by its OWN adopted child; no pre-exclusion)
    assert SERVING_CLASS in flips, flips
    for ci in flips:
        assert base_status[ci] == "unknown", ci
        assert scen_status[ci] == "excluded_now", ci
    out["status_flip_count"] = len(flips)
    out["status_flip_count_predicted_by_declaration"] = 2  # naive owner-union (no pre-excluded owner); MEASURED 2 (prediction holds exactly)
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

    # serving-class unknown arithmetic (graph-derived, class 20421)
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
    # the serving class 1152921504624672768:68719476736 (class
    # 34269) is NOT pre-excluded at BASE (unknown, ladder rank 1,
    # unknown_now 11): adopting the k01 WIN row flips it
    # unknown -> excluded_now (win-hit by its OWN adopted child)
    # and resolves ONE of its 11 cost-unknown children (11 -> 10),
    # so it STAYS in the closure ladder (NO exit)
    assert serving_rows[str(cls)]["base_status"] == "unknown"
    assert serving_rows[str(cls)]["scen_status"] == "excluded_now"
    assert (serving_rows[str(cls)]["unknown_before"],
            serving_rows[str(cls)]["unknown_after"]) == (11, 10), cls
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
    assert (len(bc), len(sc)) == (797, 797), (len(bc), len(sc))
    # MEASURED: the serving class 34269 STAYS in the ladder
    # (unknown_now 11 -> 10, rank 1 -> 1); the other flipping owner
    # class 769 sits OUTSIDE the ladder on both sides; the ladder
    # has NO exits, NO entries and NO rank churn at all (0 churn
    # cells - the rank-1 unknown_now decrement re-sorts nothing)
    assert entered == [], entered
    assert left == [], left
    assert unknown_churn == EXPECTED_UNKNOWN_CHURN, unknown_churn
    assert len(rank_churn) == EXPECTED_RANK_CHURN_COUNT, len(rank_churn)
    assert rank_churn == [], rank_churn
    assert BASE_CLOSURE.read_text() != SCEN_CLOSURE.read_text(), \
        "closure-classes.csv must NOT be byte-identical to the BASE side"
    out["closure_byte_identical_to_base"] = False
    # the serving class 34269 sits INSIDE the ladder on both sides
    # (the measured STAY, rank 1 both sides); the other flipping
    # owner class 769 sits OUTSIDE the ladder on both sides
    assert 34269 in bc and 34269 in sc
    assert bc[34269]["class_rank"] == sc[34269]["class_rank"] == "1"
    assert 769 not in bc and 769 not in sc
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
    # MEASURED: root 24 drops 2,775 -> 2,774 and root 12 drops
    # 2,931 -> 2,930 (the adoption re-routes both roots' greedy
    # unions; scheduling quantities, not coverage claims)
    assert greedy_delta == EXPECTED_GREEDY_DELTA, greedy_delta
    out["per_root_coverage_byte_identical"] = \
        BASE_PERROOT.read_text() == SCEN_PERROOT.read_text()
    assert out["per_root_coverage_byte_identical"] is False
    bp_lines = BASE_PERROOT.read_text().splitlines()
    sp_lines = SCEN_PERROOT.read_text().splitlines()
    assert len(bp_lines) == len(sp_lines) == 21
    differing = [n for n, (a, b) in enumerate(zip(bp_lines, sp_lines)) if a != b]
    assert differing == [15, 18], differing
    assert bp_lines[15] == "24,central,119,12,107,2775", bp_lines[15]
    assert sp_lines[15] == "24,central,119,12,107,2774", sp_lines[15]
    assert bp_lines[18] == "12,central,119,6,113,2931", bp_lines[18]
    assert sp_lines[18] == "12,central,119,6,113,2930", sp_lines[18]

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
    # MEASURED: the adopted s5 index 38891 sits INSIDE the frozen
    # update8 baseline requirement (the sixteenth k01, eighteenth
    # k03, nineteenth k04 and class20421 k05 precedents), so
    # exactly one baseline s5 resolves (291 -> 292)
    assert new_resolved == {38891}, sorted(new_resolved)
    assert adopted_idx & baseline_req == {38891}
    assert adopted_idx - baseline_req == set()
    assert len(new_resolved) == (
        out["update8_refresh_scen"]["resolved"]
        - out["update8_refresh_base"]["resolved"]), "resolved delta"
    out["update8_refresh_base"]["resolved_list_len"] = len(base_req)
    out["update8_refresh_scen"]["resolved_list_len"] = len(scen_req)
    assert out["update8_refresh_base"]["resolved"] == 291
    assert out["update8_refresh_scen"]["resolved"] == 292
    assert out["update8_refresh_base"]["remaining"] == 31332
    assert out["update8_refresh_scen"]["remaining"] == 31321
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
    # MEASURED (DEVIATION from the declaration's naive 35 -> 35
    # prediction, disclosed): the win-hit group set GROWS 35 -> 40;
    # the serving class 34269 IS an update8 plan group class and
    # its own adoption win-hits its 5 plan groups (all 5 added
    # groups have s4_class_index 34269; no group is removed; this
    # also removes the 10 further unknown children of 34269 inside
    # those groups from remaining_now: 31,332 -> 31,321); the other
    # flipping owner class 769 is NOT a plan group class and is
    # absent from the group set on both sides
    assert out["win_hit_groups_identical"] is False
    assert len(b_groups) == 35, len(b_groups)
    assert len(s_groups) == 40, len(s_groups)
    assert len(added_groups) == EXPECTED_WIN_HIT_GROUP_ADDED
    assert removed_groups == [], removed_groups
    u8_group_classes = {gr["s4_class_index"]
                        for gr in scen_sum["frozen_update8_refresh"]["win_hit_groups"]}
    assert 769 not in u8_group_classes
    assert SERVING_CLASS in u8_group_classes, sorted(u8_group_classes)
    assert {gr[-1] for gr in added_groups} == {SERVING_CLASS}, added_groups
    assert added_groups == [(12, 30, 108, 60, 34269), (12, 90, 108, 60, 34269),
                            (12, 108, 30, 60, 34269), (24, 20, 100, 60, 34269),
                            (24, 100, 20, 60, 34269)], added_groups
    out["win_hit_groups_added"] = added_groups

    out["joint_greedy"] = {
        "base": base_sum["joint_greedy"]["greedy_union_size"],
        "scen": scen_sum["joint_greedy"]["greedy_union_size"],
    }
    out["worklist_total"] = {
        "base": base_sum["worklist_total"],
        "scen": scen_sum["worklist_total"],
    }
    # MEASURED: the joint greedy union MEASURES 43,184 -> 43,183
    # (the adoption re-routes the joint greedy union; a scheduling
    # quantity, NOT a coverage claim) and the probing worklist row
    # count drops 64,251 -> 64,250 (the adopted key's OWN
    # membership row leaves the worklist; both are scheduling
    # quantities, not coverage claims)
    assert out["joint_greedy"] == {"base": 43184, "scen": 43183}, \
        out["joint_greedy"]
    assert out["worklist_total"] == {"base": 64251, "scen": 64250}, \
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
    #    the flipped owners 769/34269 BOTH revert to unknown (the
    #    serving class 34269 is win-hit ONLY by its own adopted
    #    child in this Part; no pre-exclusion) - the census must
    #    move
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
    for ci in (769, 34269):
        assert census(flipped)[ci] == "unknown", \
            "tamper 1: owner class %d must revert to unknown" % ci
    assert census(flipped)[SERVING_CLASS] == "unknown", \
        "tamper 1: the serving class must revert to unknown (no pre-exclusion)"
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
        "part": "twentieth-k01-flip-census",
        "canonical_head_sha256": SCEN_CACHE_SHA_EXPECTED,
        "consumed": ("exactly the single published twentieth-escalation "
                     "k01 row (1 WIN: k01, class 34269)"),
        "status_flips": len(flips),
        "deviation_from_predeclared_expectation": (
            "ONE DISCLOSED DEVIATION - the declaration's naive "
            "graph-derived TWO-flip prediction ([769, 34269] unknown "
            "-> excluded_now, census unknown 34,352 -> 34,350, "
            "excluded_now 168 -> 170) HOLDS EXACTLY, and the "
            "pre-registered serving-class STAY materialises too "
            "(ladder 797 -> 797 rows, entered [], left [], rank 1 "
            "kept, ZERO rank-churn cells), BUT the update8 "
            "win-hit-group prediction (35 -> 35 unchanged) DOES NOT "
            "HOLD: MEASURED 35 -> 40 (the serving class 34269 IS an "
            "update8 plan group class, so its own adoption win-hits "
            "its 5 plan groups, all 5 added groups have "
            "s4_class_index 34269, no group removed) and remaining_now "
            "drops 31,332 -> 31,321 (the adopted row resolves 1 and "
            "the 5 newly win-hit groups remove their 10 further "
            "unknown children of 34269); the declaration's standing "
            "caveat (the measured census replaces the prediction) "
            "covers exactly this case"),
        "status_flip_mechanism": (
            "win-hit (the Part EW/EM mechanism): the adopted WIN row "
            "k01 (s5 index 38891, 10376293541479448576:68719476736) "
            "has owner union 769, 34269; BOTH owners flip unknown "
            "-> excluded_now (the measured flip list EQUALS the "
            "owner union; unlike the k05 adoption no owner is "
            "pre-excluded at BASE, and the serving class 34269 "
            "becomes win-hit by its OWN adopted child); the serving "
            "class 34269 (1152921504624672768:68719476736) STAYS in "
            "the closure ladder (unknown_now 11 -> 10, rank 1 -> 1, "
            "NO exit, ZERO rank-churn cells) and 769 sits OUTSIDE "
            "the ladder on both sides; no class flips to free_now, "
            "free_now stays 39 (Board-verified both sides); the "
            "per-root coverage MEASURES two individual greedy "
            "re-routes (root 24 drops 2,775 -> 2,774 and root 12 "
            "drops 2,931 -> 2,930, scheduling re-route churns, NOT "
            "coverage claims; free_now/uncovered identical on all "
            "20 roots); joint greedy MEASURES 43,184 -> 43,183 and "
            "the probing worklist row count drops 64,251 -> 64,250 "
            "(the adopted key's own membership row leaves the "
            "worklist; regen content sha differs from the BASE "
            "pin); the adopted s5 index 38891 sits INSIDE the "
            "frozen update8 baseline requirement (resolved 291 -> "
            "292, groups_free_now 131 -> 131) and the win-hit "
            "group set grows 35 -> 40 (all 5 added groups are the "
            "serving class 34269's own plan groups; the other "
            "owner 769 is NOT a plan group class)"),
        "census_counts_identical_to_published_summaries": True,
        "note": ("declared twentieth-k01 adoption measurement; "
                 "adopting solver-trusted S5 labels flips class-status "
                 "bookkeeping only: no root verdict is consumed, no root "
                 "freed, no root excluded, no coverage claim is made or "
                 "changed; 11x11 stays UNKNOWN; no root verdict; nodes "
                 "are bookkeeping"),
    }

    outp = D / "output/census-deltas-twentieth-k01-adoption.json"
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
