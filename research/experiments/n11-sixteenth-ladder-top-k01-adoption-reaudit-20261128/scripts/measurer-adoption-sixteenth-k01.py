"""Sixteenth k01 adoption measurement: BASE (fifteenth k02 head
of record 58110025...) vs SCENARIO (sixteenth class-20421 k01
adoption union, dbc1d950...) census deltas.

Part of the kit n11-sixteenth-ladder-top-k01-adoption-reaudit-20261128
(declaration commit d9d53a8d, publish-then-execute): the sixteenth
k01 canonical adoption consumes exactly the single published 15M
escalation row (1 WIN: k01 1155454779397246976:131072, s5 index
528689, serving class 20421) and advances the canonical head of
record from 58110025... (6,900 rows WIN 218 / LOSS 6,682) to
dbc1d950... (6,901 rows WIN 219 / LOSS 6,682).

This measurer is a structural descendant of the published fifteenth
k02 measurer (kit n11-fifteenth-ladder-top-k02-adoption-reaudit-
20261128): it MEASURES the census/scheduling delta of adopting the
row, against the published fifteenth k02 adoption-reaudit refresh
outputs (BASE side) and this kit's three byte-identical SCEN
refresh runs (byte-clone refresh differing from the fifteenth k02
refresh in three regions: docstring, CACHE path, expected cache
sha).

Fail-closed pins verified before any census is written: the frozen
dependency graph, the update8 repaired joint plan, the fail-closed
union merger (90711961...), the adoption manifest
(n11-sixteenth-ladder-top-k01-win-adoption-manifest-v1) pins:
base head 58110025 (6,900/218/6,682), increment bb029422,
expected merged shape 6,901/219/6,682, the BASE-side fifteenth k02
adoption-reaudit kit outputs (summary df5e7607, closure e10b5765,
per-root f2d5d2a7, census json b089b269, BASE worklist regen pin
a8ebeffc unpublished per size policy), and the SCEN-side outputs of
this kit.

The adopted row is WIN (k01), so class-status flips are win-hit
flips (the Part EW/EM mechanism).  MEASURED (the declaration's
naive TWO-flip prediction HOLDS EXACTLY): the WIN key has owner
union classes 15647, 16901, 20421; the serving class 20421 is
ALREADY excluded_now at BASE (win-hit by a previously adopted row
of the chain) and stays excluded_now while remaining IN the
closure ladder (798 -> 798 rows, entered [], left []; its
cost-unknown children drop 5 -> 4; k02-k05 remain 2M UNKNOWN), so
exactly TWO owner classes flip unknown -> excluded_now (15647 and
16901; census unknown 34,365 -> 34,363, excluded_now 155 -> 157,
free_now 39 unchanged).  The owner class 16901 sits IN the ladder
on both sides (unknown_now 54 -> 53, rank 31 -> 23; rank churn 9
cells); 15647 sits outside the ladder on both sides.  The adopted
s5 index 528689 sits INSIDE the frozen update8 baseline
requirement (resolved 286 -> 287, remaining_now unchanged 31,332,
groups_free_now 131, win-hit group set unchanged 35 -> 35, no
added or removed groups; none of the owner classes is a plan
group class).  The per-root coverage MEASURES three individual
greedy re-routes (root 12 drops 2,843 -> 2,842, root 37 drops
3,639 -> 3,638, root 48 drops 3,069 -> 3,068, free_now/uncovered
identical on all 20 roots) and the joint greedy union drops
43,147 -> 43,146 (scheduling quantities, not coverage claims);
the probing worklist row count drops 64,258 -> 64,256.

Fail-closed (assertions abort before the output json is written);
tamper battery 4/4 fail-closed.  The output json is
output/census-deltas-sixteenth-k01-adoption.json.

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
D = ROOT / "research/experiments/n11-sixteenth-ladder-top-k01-adoption-reaudit-20261128"
EV = ROOT / "research/experiments/n11-fifteenth-ladder-top-k02-adoption-reaudit-20261128"
T2 = ROOT / "research/experiments/n11-sixteenth-ladder-top-k01-adoption-20261128"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
MANIFEST = T2 / "adoption-manifest.json"
MERGER = ROOT / "research/experiments/n11-centralreply-sixthlossk38-adoption-reaudit-20261126/scripts/s5_union_merge.py"

BASE_CACHE = ROOT / "research/experiments/n11-fifteenth-ladder-top-k02-adoption-20261128/output/merged/merged-exact-s5-chain-plus-fifteenth-k02-20261128.cache"
SCEN_CACHE = T2 / "output/merged/merged-exact-s5-chain-plus-sixteenth-k01-20261128.cache"
INCREMENT = T2 / "output/increment-sixteenth-k01-adoption-20261128.cache"
BASE_SUMMARY = EV / "reaudit/output/refresh-summary.json"
SCEN_SUMMARY = D / "reaudit/output/refresh-summary.json"
BASE_CLOSURE = EV / "reaudit/output/closure-classes.csv"
SCEN_CLOSURE = D / "reaudit/output/closure-classes.csv"
BASE_PERROOT = EV / "reaudit/output/per-root-coverage.csv"
SCEN_PERROOT = D / "reaudit/output/per-root-coverage.csv"
BASE_CENSUS_JSON = EV / "output/census-deltas-fifteenth-k02-adoption.json"

BASE_CACHE_SHA_EXPECTED = "58110025dd5cca7f1e824d8871b50462dc9fcbeac8b9aa69c5f4d33299c894ae"
SCEN_CACHE_SHA_EXPECTED = "dbc1d9508dda61a353ba7b9ef60371bb28eb08cf8f4cd6d30122eafd6a72bc21"
INCREMENT_SHA_EXPECTED = "bb02942212f03195a7d9448770700354b68bf10d423cc26013bd4c47526035ce"
MANIFEST_SHA_EXPECTED = "97604d6c739ff04dffaedcfc591da1fbc54dece0998bddf74096ceb12a7f6211"
BASE_SUMMARY_SHA_EXPECTED = "df5e76079470f4312a3a4d4e277e2e571a4cbb0f0849ee7f8fc85af5a7a2601a"
BASE_CLOSURE_SHA_EXPECTED = "e10b5765fba4903614b087d90f715bdf4aa15a39809d75b7f0ef66aed7a3036c"
BASE_PERROOT_SHA_EXPECTED = "f2d5d2a78742fb8b73e1fe941714591aa50e404a2fca989fad39c0a28090da60"
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_WORKLIST_PIN_SOURCE = json.loads(
    BASE_CENSUS_JSON.read_text(encoding="utf-8"))["worklist_regen_pins"]["scen"]
BASE_WORKLIST_SHA_EXPECTED = "a8ebeffcc8cf07533e14bebde2987902d891a6188c191a93e211a77da097a596"
BASE_WORKLIST_SIZE_EXPECTED = 3714446
SCEN_WORKLIST_SHA_EXPECTED = "0aa54ad7444f42ca7e30567771cd81f174902749b8034100a996300c00504f1b"
SCEN_WORKLIST_SIZE_EXPECTED = 3714327

ADOPTED_COUNT = 1
ADOPTED_WIN = 1
ADOPTED_LOSS = 0
ADOPTED_NODES_TOTAL = 5273778
SERVING_CLASS = 20421
SERVING_CLASS_MASK = (1155173304420536320, 131072)
LOSS_KEYS = {}
LOSS_S5_INDICES = {}
LOSS_OWNER_CLASSES = {}
WIN_KEYS = {
    "k01": (1155454779397246976, 131072),
}
WIN_S5_INDICES = {"k01": 528689}
WIN_OWNER_CLASSES = {
    "k01": [15647, 16901, 20421],
}
EXPECTED_FLIPS = [15647, 16901]
EXPECTED_UNKNOWN_CHURN = [
    {"class_index": 16901, "base": 54, "scen": 53},
    {"class_index": 20421, "base": 5, "scen": 4},
]
EXPECTED_RANK_CHURN_COUNT = 9
EXPECTED_GREEDY_DELTA = [
    {"root": 12, "base": 2843, "scen": 2842},
    {"root": 37, "base": 3639, "scen": 3638},
    {"root": 48, "base": 3069, "scen": 3068},
]
EXPECTED_WIN_HIT_GROUP_ADDED = 0
BASE_CENSUS = {"unknown": 34365, "excluded_now": 155,
               "free_now": 39, "excluded": 390}
SCEN_CENSUS = {"unknown": 34363, "excluded_now": 157,
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
    assert (len(base), base_wins, base_loss) == (6900, 218, 6682)
    assert (len(scen), scen_wins, scen_loss) == (6901, 219, 6682)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "n11-sixteenth-ladder-top-k01-win-adoption-manifest-v1"
    assert manifest["base"]["sha256"] == BASE_CACHE_SHA_EXPECTED
    assert (manifest["base"]["rows"], manifest["base"]["win"],
            manifest["base"]["loss"]) == (6900, 218, 6682)
    assert manifest["merger_sha256"] == MERGER_SHA_EXPECTED
    assert manifest["kits"]["replica"].startswith(
        "n11-sixteenth-ladder-top-escalation-20261128")
    assert manifest["kits"]["cppgate"].startswith(
        "n11-sixteenth-ladder-top-k01-win-cppgate-20261128")
    assert manifest["kits"]["thirdimpl"].startswith(
        "n11-sixteenth-ladder-top-k01-thirdimpl-20261128")
    # disclosed in the adoption completion log: no cross-host
    # replication kit exists for this row yet (unlike the
    # thirteenth adoption); the manifest correctly carries no xhost
    assert "xhost" not in manifest["kits"]
    assert manifest["owner_union_precheck"].startswith(
        "[15647, 16901, 20421] derived from the frozen graph in "
        "the sixteenth escalation Part; caveat: shared-owner "
        "pre-exclusion (other owner classes may already be "
        "excluded_now on BASE; serving class 20421 unknown_now "
        "rank 1 on BASE)")
    adopted_rows = manifest["rows"]
    assert len(adopted_rows) == ADOPTED_COUNT
    assert manifest["expected_merged_shape"] == {"rows": 6901, "win": 219, "loss": 6682}
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
    # MEASURED: the declaration's naive TWO-flip prediction HOLDS
    # EXACTLY: the serving class 20421 is already excluded_now at
    # BASE (win-hit by a previously adopted row of the chain), so
    # exactly TWO of the three owner-union classes flip.
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
    assert set(flips) == {15647, 16901}, flips
    for ci in (15647, 16901):
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
    out["status_flip_count_predicted_by_declaration"] = 2  # naive owner-union minus pre-excluded serving class; MEASURED 2 (prediction holds exactly)
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
    # the serving class 1155173304420536320:131072 (class 20421)
    # is ALREADY excluded_now at BASE (win-hit by a previously
    # adopted row of the chain): adopting the k01 WIN row does NOT
    # flip its status (it stays excluded_now) but drops its
    # cost-unknown 5 -> 4 while it STAYS in the ladder (NOT a
    # ladder exit; k02-k05 remain its cost-unknown children)
    assert serving_rows[str(cls)]["base_status"] == "excluded_now"
    assert serving_rows[str(cls)]["scen_status"] == "excluded_now"
    assert (serving_rows[str(cls)]["unknown_before"],
            serving_rows[str(cls)]["unknown_after"]) == (5, 4), cls
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
    assert (len(bc), len(sc)) == (798, 798), (len(bc), len(sc))
    # MEASURED: the serving class 20421 STAYS in the ladder
    # (unknown_now 5 -> 4) and rank churn is exactly 9 cells
    # (16901 re-ranks 31 -> 23 inside the ladder)
    assert entered == [], entered
    assert left == [], left
    assert unknown_churn == EXPECTED_UNKNOWN_CHURN, unknown_churn
    assert len(rank_churn) == EXPECTED_RANK_CHURN_COUNT, len(rank_churn)
    assert BASE_CLOSURE.read_text() != SCEN_CLOSURE.read_text(), \
        "closure-classes.csv must NOT be byte-identical to the BASE side"
    out["closure_byte_identical_to_base"] = False
    # the serving class and the owner class 16901 stay in the
    # ladder on both sides; the non-serving owner 15647 sits
    # outside the ladder on both sides
    assert 20421 in bc and 20421 in sc
    assert 16901 in bc and 16901 in sc
    assert 15647 not in bc and 15647 not in sc
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
    assert differing == [6, 7, 18], differing
    assert bp_lines[6] == "48,central,119,7,112,3069", bp_lines[6]
    assert sp_lines[6] == "48,central,119,7,112,3068", sp_lines[6]
    assert bp_lines[7] == "37,central,119,4,115,3639", bp_lines[7]
    assert sp_lines[7] == "37,central,119,4,115,3638", sp_lines[7]
    assert bp_lines[18] == "12,central,119,6,113,2843", bp_lines[18]
    assert sp_lines[18] == "12,central,119,6,113,2842", sp_lines[18]

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
    # MEASURED: the adopted s5 index 212115 sits OUTSIDE the frozen
    # update8 baseline requirement (the u04 precedent), so NO
    # baseline s5 resolves (286 -> 286)
    assert new_resolved == {528689}, sorted(new_resolved)
    assert adopted_idx & baseline_req == {528689}
    assert adopted_idx - baseline_req == set()
    assert len(new_resolved) == (
        out["update8_refresh_scen"]["resolved"]
        - out["update8_refresh_base"]["resolved"]), "resolved delta"
    out["update8_refresh_base"]["resolved_list_len"] = len(base_req)
    out["update8_refresh_scen"]["resolved_list_len"] = len(scen_req)
    assert out["update8_refresh_base"]["resolved"] == 286
    assert out["update8_refresh_scen"]["resolved"] == 287
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
    # added or removed groups, and every group entry including
    # unknown_s5_children is byte-identical); the two flipping
    # owner classes (15647, 16901) are NOT update8 plan group
    # classes; the pre-excluded serving class 20421 IS an update8
    # plan group class on BOTH sides (already in the win-hit
    # group set at BASE, 4 of the 35 groups) and the adoption does
    # NOT touch its group entries
    assert out["win_hit_groups_identical"] is True
    assert len(b_groups) == 35, len(b_groups)
    assert len(s_groups) == 35, len(s_groups)
    assert len(added_groups) == EXPECTED_WIN_HIT_GROUP_ADDED
    assert removed_groups == [], removed_groups
    u8_group_classes = {gr["s4_class_index"]
                        for gr in scen_sum["frozen_update8_refresh"]["win_hit_groups"]}
    assert {15647, 16901}.isdisjoint(u8_group_classes)
    assert SERVING_CLASS in u8_group_classes, sorted(u8_group_classes)
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
    assert out["joint_greedy"] == {"base": 43147, "scen": 43146}, \
        out["joint_greedy"]
    assert out["worklist_total"] == {"base": 64258, "scen": 64256}, \
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
    #    the flipped owners 15647/16901 revert to unknown, and the
    #    pre-excluded serving class 20421 STAYS excluded_now (it
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
    for ci in (15647, 16901):
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
        "part": "sixteenth-k01-flip-census",
        "canonical_head_sha256": SCEN_CACHE_SHA_EXPECTED,
        "consumed": ("exactly the single published sixteenth 15M "
                     "escalation row (1 WIN: k01, class 20421)"),
        "status_flips": len(flips),
        "deviation_from_predeclared_expectation": (
            "NO DEVIATION - the declaration's naive graph-derived "
            "TWO-flip prediction ([15647, 16901] unknown -> "
            "excluded_now, census unknown 34,365 -> 34,363, "
            "excluded_now 155 -> 157) HOLDS EXACTLY: the "
            "pre-registered shared-owner pre-exclusion caveat "
            "materialises on the serving class 20421, which is "
            "ALREADY excluded_now at BASE (win-hit by a previously "
            "adopted row of the chain) and does not flip; the "
            "serving class STAYS in the closure ladder (798 -> 798 "
            "rows, entered [], left []) and the adoption drops its "
            "cost-unknown 5 -> 4 (k02-k05 remain 2M UNKNOWN)"),
        "status_flip_mechanism": (
            "win-hit (the Part EW/EM mechanism): the adopted WIN row "
            "k01 (s5 index 528689, 1155454779397246976:131072) has owner "
            "union 15647, 16901, 20421; the two NOT-pre-excluded "
            "owners 15647, 16901 flip unknown -> excluded_now "
            "(measured flip list is a strict subset of the owner "
            "union, the caveat-materialisation case); the serving "
            "class 20421 (1155173304420536320:131072) is pre-excluded at "
            "BASE and does NOT flip, it stays excluded_now and STAYS "
            "in the closure ladder (cost-unknown 5 -> 4, ladder 798 -> "
            "798 rows, entered [], left []; rank churn 9 cells, its "
            "unknown_now 54 -> 53, rank 31 -> 23); the owner class "
            "16901 sits IN the ladder on both sides, 15647 sits "
            "outside the ladder on both sides; no class flips to "
            "free_now, "
            "free_now stays 39 (Board-verified both sides); the "
            "per-root coverage MEASURES three individual greedy "
            "re-routes (root 12 drops 2,843 -> 2,842, root 37 drops "
            "3,639 -> 3,638, root 48 drops 3,069 -> 3,068, "
            "free_now/uncovered identical on "
            "all 20 roots); joint greedy drops 43,147 -> 43,146 "
            "(a scheduling quantity, not a coverage claim) and the "
            "probing worklist row count drops 64,258 -> 64,256 (the "
            "adopted key's own membership rows leave the worklist; "
            "regen content sha differs from the BASE pin); the "
            "adopted s5 index 528689 sits INSIDE the frozen update8 "
            "baseline requirement (resolved 286 -> 287, remaining_now "
            "31,332 -> 31,332, groups_free_now 131 -> 131); the "
            "win-hit group set is unchanged (35 -> 35, every group "
            "entry byte-identical; the flipping owners 15647, 16901 "
            "are NOT plan group classes, while the pre-excluded "
            "serving class 20421 IS a plan group class on BOTH "
            "sides and its group entries are untouched)"),
        "census_counts_identical_to_published_summaries": True,
        "note": ("declared sixteenth k01 adoption measurement; "
                 "adopting solver-trusted S5 labels flips class-status "
                 "bookkeeping only: no root verdict is consumed, no root "
                 "freed, no root excluded, no coverage claim is made or "
                 "changed; 11x11 stays UNKNOWN; no root verdict; nodes "
                 "are bookkeeping"),
    }

    outp = D / "output/census-deltas-sixteenth-k01-adoption.json"
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
