"""Thirteenth k01+k02 adoption measurement: BASE (ultra-cheap u04
head of record beecb024...) vs SCENARIO (thirteenth class-16757
k01+k02 adoption union, d772f73c...) census deltas.

Part of the kit n11-thirteenth-k01k02-adoption-reaudit-20261128
(declaration commit 0bb54826, publish-then-execute): the thirteenth
k01+k02 canonical adoption consumes exactly the two published
ladder-top rows (2 WIN: k01 1153204147814662144:65536 and k02
1152922672837951488:65792, both serving class 16757) and advances
the canonical head of record from beecb024... (6,894 rows WIN 212 /
LOSS 6,682) to d772f73c... (6,896 rows WIN 214 / LOSS 6,682).

This measurer is a structural descendant of the published
ultra-cheap u04 measurer (kit n11-ultra-cheap-u04-adoption-reaudit-
20261127): it MEASURES the census/scheduling delta of adopting the
two rows, against the published u04 adoption-reaudit refresh (three
byte-identical runs of the byte-clone refresh published in this
kit's reaudit/ directory, three regions differing from the u04
refresh: docstring, CACHE path, expected cache sha).

Fail-closed pins verified before any census is written: the frozen
dependency graph, the update8 repaired joint plan, the fail-closed
union merger (90711961...), the adoption manifest
(n11-thirteenth-ladder-top-k01k02-win-adoption-manifest-v1) pins:
base head beecb024 (6,894/212/6,682), increment cebd8dc9,
expected merged shape 6,896/214/6,682, the BASE-side u04
adoption-reaudit kit outputs (summary d35900b9, closure ef344748,
per-root d3c404e9), and the SCEN-side outputs of this kit.

Both adopted rows are WIN (k01, k02), so class-status flips are
win-hit flips (the Part EW/EM mechanism).  MEASURED (this is the
first thirteenth adoption where the declaration's serving-class
pre-exclusion caveat MATERIALISES): the two WIN keys have owner
union classes 16612 (k01-only), 16740 (k02-only), 16757 and 30542
(shared, both already excluded_now on the BASE head via earlier
win-hits); only 16612 and 16740 flip unknown -> excluded_now
(census unknown 34,376 -> 34,374, excluded_now 144 -> 146, free_now
39 unchanged); the serving class 16757 was already excluded_now at
BASE and resolves its last TWO unknown children (k01 and k02,
cost-unknown 2 -> 0), leaving the closure ladder 800 -> 799 (an
all-rank churn of 799 cells, zero unknown_now churn).  Both adopted
s5 indices (556117, 558553) sit INSIDE the frozen update8 baseline
requirement (resolved 284 -> 286, remaining_now unchanged 31,332,
groups_free_now 131, win-hit groups unchanged 35).  The per-root
coverage MEASURES two individual greedy re-routes (root 48 rises
2,980 -> 3,069, root 36 drops 3,029 -> 3,028) and the joint greedy
union drops 43,830 -> 43,151 (scheduling quantities, not coverage
claims); the probing worklist row count drops 64,265 -> 64,263.

Fail-closed (assertions abort before the output json is written);
tamper battery 4/4 fail-closed.  The output json is
output/census-deltas-thirteenth-k01k02-adoption.json.

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
D = ROOT / "research/experiments/n11-thirteenth-k01k02-adoption-reaudit-20261128"
EV = ROOT / "research/experiments/n11-ultra-cheap-u04-adoption-reaudit-20261127"
T2 = ROOT / "research/experiments/n11-thirteenth-ladder-top-k01k02-adoption-20261128"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
MANIFEST = T2 / "adoption-manifest.json"
MERGER = ROOT / "research/experiments/n11-centralreply-sixthlossk38-adoption-reaudit-20261126/scripts/s5_union_merge.py"

BASE_CACHE = ROOT / "research/experiments/n11-ultra-cheap-u04-win-adoption-20261127/output/merged/merged-exact-s5-chain-plus-ultra-cheap-u04-20261127.cache"
SCEN_CACHE = T2 / "output/merged/merged-exact-s5-chain-plus-thirteenth-k01k02-20261128.cache"
INCREMENT = T2 / "output/increment-thirteenth-k01k02-adoption-20261128.cache"
BASE_SUMMARY = EV / "reaudit/output/refresh-summary.json"
SCEN_SUMMARY = D / "reaudit/output/refresh-summary.json"
BASE_CLOSURE = EV / "reaudit/output/closure-classes.csv"
SCEN_CLOSURE = D / "reaudit/output/closure-classes.csv"
BASE_PERROOT = EV / "reaudit/output/per-root-coverage.csv"
SCEN_PERROOT = D / "reaudit/output/per-root-coverage.csv"
BASE_CENSUS_JSON = EV / "output/census-deltas-ultra-cheap-u04-adoption.json"

BASE_CACHE_SHA_EXPECTED = "beecb024a648d0ddb29eaf261b09326f9412328cd09f85cb180ee2ffd9ed4544"
SCEN_CACHE_SHA_EXPECTED = "d772f73c68bf051e7b90e5cd6cfef2a7b1c8e07da888c5f728f7a04b39edd1ec"
INCREMENT_SHA_EXPECTED = "cebd8dc964f68635b253289a4e39422f958cc321842612956391fc4832ac5c27"
MANIFEST_SHA_EXPECTED = "18433ac031443da86c2419cd99e936194b67b12fa7ef4060ac90bc357800f6a9"
BASE_SUMMARY_SHA_EXPECTED = "d35900b9a8eb4d6043fef7ce4bfe8950c8749ac5ec2685fe51af96e604dac958"
BASE_CLOSURE_SHA_EXPECTED = "ef3447481abb14af3c56a64251d86e63b178c7fb57b0ce8898e67303c24dc3e2"
BASE_PERROOT_SHA_EXPECTED = "d3c404e9d216d2e953082b7862ecec217e5c27e4baf798cfc286b7f870e311e8"
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_WORKLIST_PIN_SOURCE = json.loads(
    BASE_CENSUS_JSON.read_text(encoding="utf-8"))["worklist_regen_pins"]["scen"]
BASE_WORKLIST_SHA_EXPECTED = "c38831c1c2ed9a2f186386111fcfcd9657e1b08fe15b3398f86cfbd02328a2e5"
BASE_WORKLIST_SIZE_EXPECTED = 3714832
SCEN_WORKLIST_SHA_EXPECTED = "da2d22e1fd5123283f2921d97e6bd33c4a77d467a41aab65b09118e2292a9dab"
SCEN_WORKLIST_SIZE_EXPECTED = 3714716

ADOPTED_COUNT = 2
ADOPTED_WIN = 2
ADOPTED_LOSS = 0
ADOPTED_NODES_TOTAL = 6163868
SERVING_CLASS = 16757
SERVING_CLASS_MASK = (1153204079095185408, 65536)
LOSS_KEYS = {}
LOSS_S5_INDICES = {}
LOSS_OWNER_CLASSES = {}
WIN_KEYS = {
    "k01": (1153204147814662144, 65536),
    "k02": (1152922672837951488, 65792),
}
WIN_S5_INDICES = {"k01": 556117, "k02": 558553}
WIN_OWNER_CLASSES = {
    "k01": [16612, 16757, 30542],
    "k02": [16740, 16757, 30542],
}
EXPECTED_FLIPS = [16612, 16740]
EXPECTED_UNKNOWN_CHURN = []
EXPECTED_RANK_CHURN_COUNT = 799
EXPECTED_GREEDY_DELTA = [
    {"root": 36, "base": 3029, "scen": 3028},
    {"root": 48, "base": 2980, "scen": 3069},
]
EXPECTED_WIN_HIT_GROUP_ADDED = 0
BASE_CENSUS = {"unknown": 34376, "excluded_now": 144,
               "free_now": 39, "excluded": 390}
SCEN_CENSUS = {"unknown": 34374, "excluded_now": 146,
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
    assert (len(base), base_wins, base_loss) == (6894, 212, 6682)
    assert (len(scen), scen_wins, scen_loss) == (6896, 214, 6682)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "n11-thirteenth-ladder-top-k01k02-win-adoption-manifest-v1"
    assert manifest["base"]["sha256"] == BASE_CACHE_SHA_EXPECTED
    assert (manifest["base"]["rows"], manifest["base"]["win"],
            manifest["base"]["loss"]) == (6894, 212, 6682)
    assert manifest["merger_sha256"] == MERGER_SHA_EXPECTED
    assert manifest["kits"]["replica"].startswith(
        "n11-thirteenth-ladder-top-escalation-20261128")
    assert manifest["kits"]["cppgate"].startswith(
        "n11-thirteenth-ladder-top-k01-win-cppgate-20261128")
    assert manifest["kits"]["thirdimpl"].startswith(
        "n11-thirteenth-ladder-top-k01-thirdimpl-20261128")
    assert manifest["kits"]["xhost"].startswith(
        "n11-thirteenth-ladder-top-k01-pillars-xhost-20261128")
    assert manifest["owner_union_precheck"].startswith(
        "n11-thirteenth-owner-union-precheck-20261128")
    adopted_rows = manifest["rows"]
    assert len(adopted_rows) == ADOPTED_COUNT
    assert manifest["expected_merged_shape"] == {"rows": 6896, "win": 214, "loss": 6682}
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
    assert out["owner_class_count_hist"] == {"3": 2}, \
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
    # MEASURED: the declaration's naive FOUR-owner union flip
    # prediction does NOT hold; the declared pre-exclusion caveat
    # MATERIALISES (classes 16757 and 30542 were already
    # excluded_now at BASE), so only 16612 and 16740 flip.
    flips = sorted(ci for ci in base_status
                   if base_status[ci] != scen_status[ci])
    out["status_flips"] = [
        {"class_index": ci, "base": base_status[ci], "scen": scen_status[ci],
         "class_mask": s4_masks[ci]}
        for ci in flips]
    assert flips == EXPECTED_FLIPS, flips
    win_owner_union = sorted({ci for key in WIN_KEYS.values()
                              for ci in owner_classes[key]})
    # the measured flip list is a strict subset of the owner union;
    # the non-flipping owner classes were PRE-EXCLUDED at BASE
    assert set(flips) < set(win_owner_union), \
        "the measured flip list must be a strict subset of the owner union"
    assert set(flips) == {16612, 16740}, flips
    for ci in (16757, 30542):
        assert base_status[ci] == scen_status[ci] == "excluded_now", ci
    for ci in flips:
        assert base_status[ci] == "unknown", ci
        assert scen_status[ci] == "excluded_now", ci
    out["status_flip_count"] = len(flips)
    out["status_flip_count_predicted_by_declaration"] = 4  # naive owner-union; caveat materialised
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

    # serving-class unknown arithmetic (graph-derived, class 16757)
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
    # the thirteenth serving class 1153204079095185408:65536 was
    # already excluded_now on the BASE head (earlier win-hits) and
    # held exactly TWO unknown children (the k01 and k02 keys
    # themselves); the two adopted WIN rows resolve those last two
    # unknown children (cost-unknown 2 -> 0, the class leaves the
    # closure ladder 800 -> 799) while its status stays excluded_now
    assert serving_rows[str(cls)]["base_status"] == "excluded_now"
    assert serving_rows[str(cls)]["scen_status"] == "excluded_now"
    assert (serving_rows[str(cls)]["unknown_before"],
            serving_rows[str(cls)]["unknown_after"]) == (2, 0), cls
    assert serving_rows[str(cls)]["adopted_owned_here"] == 2
    out["serving_class_rows"] = serving_rows

    # closure-classes.csv churn (measured; the serving class LEAVES
    # the ladder; zero unknown_now churn)
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
    assert (len(bc), len(sc)) == (800, 799), (len(bc), len(sc))
    # MEASURED: the serving class 16757 leaves the ladder (its last
    # two unknown children were the adopted keys); the ladder
    # re-ranks (799 cells, an all-rank churn)
    assert entered == [], entered
    assert left == [16757], left
    assert unknown_churn == EXPECTED_UNKNOWN_CHURN, unknown_churn
    assert len(rank_churn) == EXPECTED_RANK_CHURN_COUNT, len(rank_churn)
    assert BASE_CLOSURE.read_text() != SCEN_CLOSURE.read_text(), \
        "closure-classes.csv must NOT be byte-identical to the BASE side"
    out["closure_byte_identical_to_base"] = False
    # the leaving class was in the BASE ladder and is gone in SCEN;
    # the other three flipped owner classes sit outside the ladder on
    # both sides
    assert 16757 in bc and 16757 not in sc
    for ci in (16612, 16740, 30542):
        assert ci not in bc and ci not in sc, ci
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
    # MEASURED: root 48 rises 2,980 -> 3,069 and root 36 drops
    # 3,029 -> 3,028 (the adoption re-routes both roots' greedy
    # unions; scheduling quantities, not coverage claims)
    assert greedy_delta == EXPECTED_GREEDY_DELTA, greedy_delta
    out["per_root_coverage_byte_identical"] = \
        BASE_PERROOT.read_text() == SCEN_PERROOT.read_text()
    assert out["per_root_coverage_byte_identical"] is False
    bp_lines = BASE_PERROOT.read_text().splitlines()
    sp_lines = SCEN_PERROOT.read_text().splitlines()
    assert len(bp_lines) == len(sp_lines) == 21
    differing = [n for n, (a, b) in enumerate(zip(bp_lines, sp_lines)) if a != b]
    assert differing == [6, 11], differing
    assert bp_lines[6] == "48,central,119,7,112,2980", bp_lines[6]
    assert sp_lines[6] == "48,central,119,7,112,3069", sp_lines[6]
    assert bp_lines[11] == "36,central,119,4,115,3029", bp_lines[11]
    assert sp_lines[11] == "36,central,119,4,115,3028", sp_lines[11]

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
    # MEASURED: BOTH adopted s5 indices (556117 k01, 558553 k02)
    # sit INSIDE the frozen update8 baseline requirement (unlike the
    # u04 adoption), so TWO baseline s5 resolve (284 -> 286)
    assert new_resolved == {556117, 558553}, sorted(new_resolved)
    assert adopted_idx & baseline_req == {556117, 558553}
    assert adopted_idx - baseline_req == set()
    assert len(new_resolved) == (
        out["update8_refresh_scen"]["resolved"]
        - out["update8_refresh_base"]["resolved"]), "resolved delta"
    out["update8_refresh_base"]["resolved_list_len"] = len(base_req)
    out["update8_refresh_scen"]["resolved_list_len"] = len(scen_req)
    assert out["update8_refresh_base"]["resolved"] == 284
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
    # added or removed groups); the serving class 16757 IS an
    # update8 plan group class (5 groups, already win-hit at BASE via
    # other children, unchanged 35 -> 35); the other three
    # owner-union classes (16612, 16740, 30542) are not plan classes
    assert out["win_hit_groups_identical"] is True
    assert len(b_groups) == 35, len(b_groups)
    assert len(s_groups) == 35, len(s_groups)
    assert len(added_groups) == EXPECTED_WIN_HIT_GROUP_ADDED
    assert removed_groups == [], removed_groups
    u8_group_classes = {gr["s4_class_index"]
                        for gr in scen_sum["frozen_update8_refresh"]["win_hit_groups"]}
    assert {16612, 16740, 30542}.isdisjoint(u8_group_classes)
    assert 16757 in u8_group_classes
    assert sum(1 for gr in scen_sum["frozen_update8_refresh"]["win_hit_groups"]
               if gr["s4_class_index"] == 16757) == 5
    out["win_hit_groups_added"] = added_groups

    out["joint_greedy"] = {
        "base": base_sum["joint_greedy"]["greedy_union_size"],
        "scen": scen_sum["joint_greedy"]["greedy_union_size"],
    }
    out["worklist_total"] = {
        "base": base_sum["worklist_total"],
        "scen": scen_sum["worklist_total"],
    }
    # MEASURED: the joint greedy union drops 43,830 -> 43,151 and
    # the probing worklist row count drops 64,265 -> 64,263 (the two
    # adopted keys' OWN membership rows leave the worklist; both are
    # scheduling quantities, not coverage claims)
    assert out["joint_greedy"] == {"base": 43830, "scen": 43151}, \
        out["joint_greedy"]
    assert out["worklist_total"] == {"base": 64265, "scen": 64263}, \
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
    # 1. flip BOTH adopted rows' verdicts WIN -> LOSS in a SCEN copy:
    #    the two flipped owner classes 16612 and 16740 revert to
    #    unknown; the serving class 16757 STAYS excluded_now (it was
    #    already pre-excluded at BASE by earlier win-hits, which the
    #    tampered verdicts cannot remove) - the census must move
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
    assert census(flipped)[16612] == "unknown", \
        "tamper 1: the k01-only owner class must revert to unknown"
    assert census(flipped)[16740] == "unknown", \
        "tamper 1: the k02-only owner class must revert to unknown"
    assert census(flipped)[SERVING_CLASS] == "excluded_now", \
        "tamper 1: the pre-excluded serving class stays excluded_now"
    tamper["verdict_flip_changes_census"] = True
    # 2. delete BOTH adopted rows from the SCEN copy: the recount must
    #    fall back to the BASE census exactly
    deleted = {k: v for k, v in flipped.items()
               if k not in WIN_KEYS.values()}
    # (the flipped rows are absent, so deletion restores the SCEN rows
    # minus the two adopted rows == BASE rows)
    assert counts_from(census(deleted)) == cb, \
        "tamper 2 must restore the BASE census"
    tamper["row_delete_restores_base_census"] = True
    # 3. append BOTH adopted rows to a BASE copy: the recount must equal
    #    the SCEN census exactly (the adoption is exactly these rows)
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
        "part": "thirteenth-k01k02-flip-census",
        "canonical_head_sha256": SCEN_CACHE_SHA_EXPECTED,
        "consumed": ("exactly the two published thirteenth ladder-top "
                     "rows (2 WIN: k01, k02, both class 16757)"),
        "status_flips": len(flips),
        "deviation_from_predeclared_expectation": (
            "MATERIALISED CAVEAT, DISCLOSED - the declaration's naive "
            "graph-derived FOUR-owner union flip prediction "
            "(16612, 16740, 16757, 30542 all unknown -> excluded_now, "
            "census unknown 34,376 -> 34,372, excluded_now 144 -> 148) "
            "does NOT hold as measured; the declaration's explicitly "
            "pre-registered u03-style pre-exclusion caveat MATERIALISED: "
            "classes 16757 and 30542 were already excluded_now on the "
            "BASE head (earlier win-hits), so only 16612 (k01-only "
            "owner) and 16740 (k02-only owner) flip unknown -> "
            "excluded_now and the measured census is unknown 34,376 -> "
            "34,374, excluded_now 144 -> 146"),
        "status_flip_mechanism": (
            "win-hit (the Part EW/EM mechanism): the two adopted WIN "
            "rows k01 (s5 index 556117, 1153204147814662144:65536) "
            "and k02 (s5 index 558553, 1152922672837951488:65792) "
            "have owner union 16612, 16740, 16757, 30542; only the "
            "k01-only owner 16612 and the k02-only owner 16740 flip "
            "unknown -> excluded_now (the shared classes 16757 and "
            "30542 were already excluded_now on the BASE head, the "
            "pre-exclusion caveat); the serving class 16757 "
            "(1153204079095185408:65536) resolves its last TWO "
            "unknown children (cost-unknown 2 -> 0) and leaves the "
            "closure ladder 800 -> 799 (all-rank churn, 799 cells, "
            "zero unknown_now churn); no class flips to free_now, "
            "free_now stays 39 (Board-verified both sides); the "
            "per-root coverage MEASURES two individual greedy "
            "re-routes (root 48 rises 2,980 -> 3,069, root 36 drops "
            "3,029 -> 3,028, free_now/uncovered identical on all 20 "
            "roots); joint greedy drops 43,830 -> 43,151 (a "
            "scheduling quantity, not a coverage claim) and the "
            "probing worklist row count drops 64,265 -> 64,263 (the "
            "two adopted keys' own membership rows leave the "
            "worklist; regen content sha differs from the BASE pin); "
            "BOTH adopted s5 indices sit INSIDE the frozen update8 "
            "baseline requirement (resolved 284 -> 286, remaining_now "
            "31,332 -> 31,332, groups_free_now 131 -> 131); the "
            "win-hit group set is unchanged (35 -> 35, no added or "
            "removed groups)"),
        "census_counts_identical_to_published_summaries": True,
        "note": ("declared thirteenth k01+k02 adoption measurement; "
                 "adopting solver-trusted S5 labels flips class-status "
                 "bookkeeping only: no root verdict is consumed, no root "
                 "freed, no root excluded, no coverage claim is made or "
                 "changed; 11x11 stays UNKNOWN; no root verdict; nodes "
                 "are bookkeeping"),
    }

    outp = D / "output/census-deltas-thirteenth-k01k02-adoption.json"
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
