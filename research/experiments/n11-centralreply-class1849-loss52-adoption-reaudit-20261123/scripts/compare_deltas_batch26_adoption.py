#!/usr/bin/env python3
"""Batch-26 (class 1849) 52-LOSS canonical-adoption reaudit delta extractor (Part BU).

Fail-closed, read-only audit executing the single-owner Part BU declaration
(note amendment 2026-11-23; no takeover - single owner).  Compares the
published BASE refresh outputs (Part BI reaudit on the canonical cache
f6649fe3..., 6,235 rows) against the single post-adoption computation:

  ADOPTED-CANONICAL = BASE + the 52 resolved LOSS rows
  ({l001..l053} minus l028) of batch-26 (class 1849)

Batch-26 probed all 53 unknown cost children of class 1849 with 2-pass
node-exact results: 52 LOSS / 1 WIN (l028) / 0 exhausted / 0 mismatch
(complete enumeration book, published Part BQ drive-1 + Part BT
contination; row-audit full-v2 schema).  The WIN row l028 (key
(1153485622925590528,0), s5 81011, honest label, 4-systems cross-verified
in Part BS) is NOT adopted and stays unconsumed (scrutiny owner C++
second-implementation gate pin 9193f5b6...; batch-14residual q042
precedent), so full != loss for the batch-26 packet and class 1849 KEEPS
exactly one unknown cost child (l028) unless its scrutiny owner consumes
the WIN.  The adopted packet is loss-only and can free NO class.

The published refresh semantics are re-executed faithfully from the pinned
graph + update8 receipt + cache verdicts (per-class verdict-level status
with Board fail-closed child verification of every free candidate), and
the recomputed class_status_counts, known-universe counts and per-root
coverage counts are asserted equal to the published BASE and scenario
outputs before any delta is emitted.

Gates (all fail-closed):
  * sha256 pins: increment, scenario cache, base cache, base summary,
    scenario summary, base closure-classes.csv, base per-root-coverage.csv,
    scenario closure-classes.csv, scenario per-root-coverage.csv,
    batch-keys, batch-26 row-audit;
  * manifest: 53 resolved / 52 LOSS / 1 WIN (l028) / 0 adopted WIN /
    0 exhausted / probed 53/53, win_ids == unadopted_win_ids == ['l028'],
    exhausted ids empty, loss_ids == the 52 adopted ids, resolved_ids ==
    all 53, full_packet_eq_loss_only FALSE, win_scenario_exists TRUE,
    row-audit 53-row agreement recorded, loss sha == increment sha,
    status-log stop record == the recorded l028 WIN-HALT row of the Part BQ
    drive-1 + published final row pinned;
  * independent two-pass raw re-verification of all 53 keys: both raws
    agree on (stones, legal, is_or, budget, result, nodes, lo, hi), every
    adopted key is result 2 (LOSS), l028 is result 1 (the published honest
    WIN label) with the Part BS replica node count, each key agrees with
    batch-keys;
  * the 52 increment keys exist, are canonical, unquarantined, absent from
    the BASE cache and the update8 receipt, map to their published s5
    indices, are all BASE-unknown cost children of class 1849, and l028's
    key is asserted NOT in the increment, NOT in BASE, NOT in the receipt
    (stays unconsumed);
  * scenario cache == BASE rows + increment rows with verdict agreement
    (6,235 -> 6,287: WIN 158 / LOSS 6,129);
  * every recomputed status transition is one of
    excluded->excluded, excluded_now->excluded_now, free_now->free_now,
    unknown->{unknown, free_now};
  * excluded_now flip set EMPTY (a loss-only increment cannot flip), and
    no excluded_now regression;
  * newly free_now classes == exactly the classes whose BASE-unknown cost
    children are ALL resolved by the increment (computed, not hardcoded)
    AND class 1849 is NOT among them (l028 stays unconsumed) AND its
    scenario status stays "unknown" with exactly the l028 s5 index 81011
    as its one unknown child;
  * class 1849: 53 BASE-unknown cost children == the batch-26 key set,
    52 resolved by the increment, leftover == {81011} == l028;
  * every graph holder class of the 52 keys: scenario unknown_now ==
    BASE unknown_now - own membership in the increment;
  * update8 newly-resolved baseline requirements must lie inside the
    increment universe, no resolution lost, count arithmetic consistent;
  * per-root coverage recomputed from the graph matches the published
    per-root-coverage.csv for BASE and scenario; root 27 stays 119/119;
    with no newly free class, no newly free third and no changed per-root
    row may exist (coverage may only improve, and here nothing frees);
  * closure-candidate table: class 1849 must be present in BOTH tables
    (BASE unknown_now 53 -> scenario unknown_now 1; rank bookkeeping
    recorded from the published rows), class 23101 must stay unknown_now 1
    and class 12643 unknown_now 53 in both tables; every class that left
    or entered the ranked candidate table must keep its recomputed BASE
    == scenario status "unknown" (the table membership churn is pure
    scheduling/ranking bookkeeping caused by the class-1849 remaining
    count 53 -> 1, never a status change).

Measured (recorded, not gated, scheduling quantities only): per-root and
joint greedy, worklist, closure-table rank churn (left/entered), update8
ledger.  No unknown verdict is asserted anywhere.  The standard 11x11
empty board and all 19 central-reply roots stay UNKNOWN.  Nodes are
bookkeeping, never verdicts.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

_here = Path(__file__).resolve()
_CANDS = [q for q in _here.parents if (q / "research" / "experiments").is_dir()]
if not _CANDS:
    raise SystemExit("GATE FAILED: repo root (research/experiments) not found above this script")
ROOT = _CANDS[0]
EXP = _here.parents[1]
OUT = EXP / "output/decomp-deltas-batch26-adoption.json"

GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_DIR = ROOT / "research/experiments/n11-centralreply-class12457-loss53-adoption-reaudit-20261123/reaudit/output"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class12457-loss53-adoption-reaudit-20261123/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-plus-batch20loss53-20261123.cache"
BATCH_DIR = ROOT / "research/experiments/n11-centralreply-closure-class1849-batch26-20261123"
SCEN_OUT = EXP / "reaudit/output"
INCR_CACHE = EXP / "output/increment-batch26-loss52-20261123.cache"
MANIFEST = EXP / "output/increments-manifest.json"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-plus-batch20loss53-plus-batch26loss52-20261123.cache"

INCR_SHA = "19f6306e6c15e11e4eb3ead4c7cd1189f24210a927dcf0a153c3fe5c26733217"
SCEN_CACHE_SHA = "e32a2e442e77799ea36194f675baeb2424f3410a1d3e681b4c4fbb389f66fe93"
BASE_CACHE_SHA = "f6649fe36425f9a4e959b058392746b73e655cda0fcfa223befafd8905d67d26"
BASE_SUMMARY_SHA = "d9d18fc265e7d12b3d7bb672c9e7181d2779d766aa47e5cab64815502ccbbff2"
SCEN_SUMMARY_SHA = "51d6bf0dd6a7d73cc2824a692cf6b086849e5f7945509b9e72c6177ce7599101"
BASE_CLOSURE_SHA = "d57a760926aa609554ca916da80afde5dc0b500c03dc9482b1ef4dee40ad5e52"
BASE_PRC_SHA = "bc409e6336a9e64aed85f20c2017535b7e6a766c7dea260c824202cbe95ea621"
SCEN_CLOSURE_SHA = "e54a0eb831da6ade5cb5c35281713225d50039eb42c7254c50d25ddefd28cd50"
SCEN_PRC_SHA = "c1cb1bf52594eb810fe17cb6e9af0fdfc2791f39f0bb7551aa30c8c608a312fd"
BATCH_KEYS_SHA = "f1ea43aef6ee06c918885a9007ad3f347d96aa198180e87bf3eb14d783304cdd"
ROW_AUDIT_SHA = "cb4158d9ecfa6143c20a8fddb59f03815e385cf90f6389cf032aa7e15779edb7"

SCENARIO = "ADOPTED-CANONICAL"
BATCH_CLASS = 1849
UNIVERSE_SIZE = 31859
RECEIPT_COUNT = 23
ADOPTED_ROWS = 52
UNADOPTED_WIN_KID = "l028"
UNADOPTED_WIN_S5 = 81011
UNADOPTED_WIN_KEY = (1153485622925590528, 0)
UNADOPTED_WIN_NODES = 4893014
LOSS_IDS = [f"l{i:03d}" for i in range(1, 54) if i != 28]
ALLOWED_TRANSITIONS = {"excluded": ["excluded"], "excluded_now": ["excluded_now"],
                       "free_now": ["free_now"], "unknown": ["unknown", "free_now"]}


def fail(msg):
    print("GATE FAILED: " + msg, file=sys.stderr)
    raise SystemExit(1)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_cache(path):
    rows = {}
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        for lineno, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                fail(f"invalid cache row {lineno} in {path}: {row}")
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            key = (lo, hi)
            if stones != 5 or verdict not in (1, 2) or nodes < 0:
                fail(f"invalid cache verdict at row {lineno} in {path}: {row}")
            if key in rows and verdict != rows[key][0]:
                fail(f"cache conflict for {key} in {path}")
            rows[key] = (verdict, nodes)
    return rows


def main():
    # --- pins ---------------------------------------------------------------
    for name, p, want in (("increment", INCR_CACHE, INCR_SHA),
                          ("scenario cache", SCEN_CACHE, SCEN_CACHE_SHA),
                          ("base cache", BASE_CACHE, BASE_CACHE_SHA),
                          ("base summary", BASE_DIR / "refresh-summary.json", BASE_SUMMARY_SHA),
                          ("scenario summary", SCEN_OUT / "refresh-summary.json", SCEN_SUMMARY_SHA),
                          ("base closure-classes", BASE_DIR / "closure-classes.csv", BASE_CLOSURE_SHA),
                          ("base per-root-coverage", BASE_DIR / "per-root-coverage.csv", BASE_PRC_SHA),
                          ("scenario closure-classes", SCEN_OUT / "closure-classes.csv", SCEN_CLOSURE_SHA),
                          ("scenario per-root-coverage", SCEN_OUT / "per-root-coverage.csv", SCEN_PRC_SHA),
                          ("batch-keys", BATCH_DIR / "input/batch-keys.json", BATCH_KEYS_SHA),
                          ("batch-26 row-audit", BATCH_DIR / "output/row-audit.json", ROW_AUDIT_SHA)):
        got = sha(p)
        if got != want:
            fail(f"{name} sha256 drift: {got} != {want}")

    manifest = json.loads(MANIFEST.read_text())
    rc = manifest["row_counts"]
    if not (rc["resolved_rows"] == 53 and rc["losses"] == 52 and rc["wins"] == 1
            and rc["exhausted_excluded"] == 0 and rc["probed_total"] == 53
            and rc["probed_resolved"] == 53):
        fail(f"manifest row_counts not 52 LOSS / 1 WIN (l028) of 53 resolved: {rc}")
    if (manifest["win_ids"] != [UNADOPTED_WIN_KID]
            or manifest["unadopted_win_ids"] != [UNADOPTED_WIN_KID]
            or manifest["exhausted_excluded_ids"] != []):
        fail(f"manifest win/unadopted/exhaustion id lists drift: {manifest}")
    if manifest["loss_ids"] != LOSS_IDS:
        fail("manifest loss_ids != the 52 adopted ids ({l001..l053} minus l028)")
    if manifest["resolved_ids"] != [f"l{i:03d}" for i in range(1, 54)]:
        fail("manifest resolved_ids != all 53 probed keys")
    if manifest["full_packet_eq_loss_only"] is not False or manifest["win_scenario_exists"] is not True:
        fail("manifest full != loss / WIN-scenario bookkeeping not asserted "
             "(l028 WIN exists and is NOT adopted)")
    if manifest["sha256"]["loss"] != INCR_SHA:
        fail("manifest loss sha does not match the pinned increment")
    if manifest["row_audit_sha256"] != ROW_AUDIT_SHA or manifest["row_audit_agreement_rows"] != 53:
        fail("manifest row-audit bookkeeping drift")
    if manifest["status_log_stop_record"] != {"key_id": "l028",
                                              "row": "2026-11-23T08:21:45Z l028 WIN-HALT"}:
        fail(f"manifest status-log stop record drift: {manifest.get('status_log_stop_record')}")
    if manifest["status_log_final_row"] != "2026-11-23T09:42:23Z l053 PASS 15000000,2,5352593":
        fail("manifest status-log final-row drift")
    if manifest["total_nodes_pass_one"] != manifest["total_nodes_pass_two"] \
            or manifest["total_nodes_pass_one"] != 208202177:
        fail("manifest adopted-row pass node totals drift")
    uwr = manifest["unadopted_win_rows"]
    if not (isinstance(uwr, list) and len(uwr) == 1
            and uwr[0].get("key_id") == UNADOPTED_WIN_KID
            and uwr[0].get("s5_index") == UNADOPTED_WIN_S5
            and uwr[0].get("lo") == UNADOPTED_WIN_KEY[0]
            and uwr[0].get("hi") == UNADOPTED_WIN_KEY[1]
            and uwr[0].get("legal") == 88
            and uwr[0].get("result") == 1
            and uwr[0].get("nodes") == UNADOPTED_WIN_NODES
            and uwr[0].get("two_pass_node_exact") is True):
        fail(f"manifest unadopted WIN row bookkeeping drift: {uwr}")

    ra = json.loads((BATCH_DIR / "output/row-audit.json").read_text())
    if ra["schema"] != "n11-centralreply-closure-class1849-batch26-rowaudit-full-v2":
        fail(f"published row-audit schema drift: {ra['schema']}")
    if (ra["class_index"] != 1849 or ra["batch"] != 26 or ra["keys_total"] != 53
            or ra["probed"] != 53 or ra["pass_rows"] != 52
            or ra["win_rows"] != ["l028"] or ra["exhausted_rows"] != [] or ra["mismatches"] != 0
            or ra["input_sha256"] != BATCH_KEYS_SHA):
        fail(f"published row-audit not the published 52-LOSS + l028-WIN picture: {ra}")

    sys.path.insert(0, str(BOARD_SOURCE.parent))
    sys.path.insert(0, str(POLICY.parent))
    from independent import Board
    from s5_evidence_policy import quarantined_cache_keys, is_canonical_safe_s5_key

    quarantined = quarantined_cache_keys()
    board = Board(11)

    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s4_masks, s4_status, s4_cost = g["s4_masks"], g["s4_status"], g["s4_cost"]
    roots = g["roots"]
    s5_masks = g["s5_masks"]
    mask_to_index = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}

    update8 = json.loads(UPDATE8.read_text(encoding="utf-8"))
    if update8["schema"] != "n11-night-repaired-joint-plan-update8-v1":
        fail("update8 schema drift")
    if update8["union_size"] != UNIVERSE_SIZE or len(update8["required_new_s5"]) != UNIVERSE_SIZE:
        fail("update8 baseline drift")
    if not update8["verification"]["passed"]:
        fail("update8 verification flag not passed")
    receipt_verdicts = {int(k): int(v) for k, v in update8["resolved_s5_verdicts"].items()}
    if len(receipt_verdicts) != RECEIPT_COUNT:
        fail(f"receipt verdict count {len(receipt_verdicts)} != {RECEIPT_COUNT}")

    # --- batch keys against the pinned graph --------------------------------
    bk = json.loads((BATCH_DIR / "input/batch-keys.json").read_text())
    if bk["class_index"] != BATCH_CLASS:
        fail(f"batch-keys class_index {bk['class_index']} != {BATCH_CLASS}")
    gs_raw = bk.get("groups_served_full")
    if gs_raw is not None:
        batch_groups_served = sorted((int(e["first"]), int(e["third"]))
                                     for e in gs_raw)
    else:
        e = bk["groups_served_first_seen"]
        batch_groups_served = sorted({(int(e["first"]), int(e["third"]))})
    if [int(x) for x in bk["class_mask"]] != list(s4_masks[BATCH_CLASS]):
        fail("batch-keys class_mask != graph mask of the batch class")
    if not batch_groups_served:
        fail("batch-keys groups-served empty for a closure-class batch")
    if len(bk["keys"]) != 53:
        fail(f"batch-keys count {len(bk['keys'])} != 53")
    batch_keys = {}
    for k in bk["keys"]:
        kid = k["key_id"]
        lo, hi, s5i = int(k["lo"]), int(k["hi"]), int(k["s5_index"])
        if mask_to_index.get((lo, hi)) != s5i:
            fail(f"{kid} (lo,hi) does not map to its published s5 index {s5i}")
        if (lo, hi) in quarantined or not is_canonical_safe_s5_key((lo, hi)):
            fail(f"{kid} noncanonical or quarantined key")
        batch_keys[kid] = (lo, hi, s5i, int(k["membership_class_count"]))
    if len(set(v[2] for v in batch_keys.values())) != 53:
        fail("batch-26 keys collide on s5 indices")

    # --- independent two-pass raw re-verification of ALL 53 keys -------------
    # (second implementation of the maker's row gate; does not trust the maker;
    #  the 52 adopted keys must be LOSS, l028 must be the honest WIN label)
    for kid, (lo, hi, s5i, _m) in sorted(batch_keys.items()):
        rows_raw = []
        for tag in ("p1", "p2"):
            p = BATCH_DIR / f"output/raw/{kid}.{tag}.out"
            rr = None
            txt = p.read_text()
            if "# replay_done" not in txt:
                fail(f"{kid} raw pass {tag} lacks the '# replay_done' completeness guard")
            for line in txt.splitlines():
                if not line.startswith("replay,"):
                    continue
                parts = line.split(",")
                row = (int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5]),
                       int(parts[6]), int(parts[7]), int(parts[9]), int(parts[10]))
                if rr is not None:
                    fail(f"{kid} multiple replay rows in pass {tag}")
                rr = row
            if rr is None:
                fail(f"{kid} no replay row in pass {tag}")
            rows_raw.append(rr)
        p1, p2 = rows_raw
        if p1 != p2:
            fail(f"{kid} two-pass mismatch (node-exact gate): {p1} vs {p2}")
        stones, legal, is_or, budget, result, nodes, klo, khi = p1
        if stones != 5 or is_or != 0 or budget != 15000000:
            fail(f"{kid} raw depth/budget drift: {p1}")
        if kid == UNADOPTED_WIN_KID:
            if result != 1:
                fail(f"{kid} raw result {result} is not the published honest WIN label 1")
            if nodes != UNADOPTED_WIN_NODES:
                fail(f"{kid} nodes {nodes} != the published Part BS replica node count {UNADOPTED_WIN_NODES}")
        elif result != 2:
            fail(f"{kid} raw result {result} is not LOSS - adopted rows must be result 2")
        if (klo, khi) != (lo, hi) or legal != int(next(k for k in bk["keys"] if k["key_id"] == kid)["legal"]):
            fail(f"{kid} raw key/legal != batch-keys")

    incr = read_cache(INCR_CACHE)
    if len(incr) != ADOPTED_ROWS:
        fail(f"increment row count {len(incr)} != {ADOPTED_ROWS}")
    if any(v[0] != 2 for v in incr.values()):
        fail("increment contains a non-LOSS verdict")
    incr_index = {}
    for kid, (lo, hi, s5i, _m) in batch_keys.items():
        row = incr.get((lo, hi))
        if row is None:
            continue
        if row[0] != 2:
            fail(f"{kid} increment row is not LOSS")
        incr_index[s5i] = (lo, hi)
    if set(incr) != {(lo, hi) for (lo, hi, _s, _m) in batch_keys.values()
                     if (lo, hi) in incr}:
        fail("increment key set not contained in the batch-26 key set")
    adopted_loss_ids = sorted(kid for kid, (lo, hi, _s, _m) in batch_keys.items()
                              if (lo, hi) in incr)
    if LOSS_IDS != adopted_loss_ids:
        fail(f"adopted LOSS ids {adopted_loss_ids[:5]}... != the 52 accepted ids")
    if len(incr_index) != 52:
        fail("adopted s5 index set != 52")
    if incr.get(UNADOPTED_WIN_KEY) is not None:
        fail("l028 WIN row leaked into the increment (adoption gate)")

    base_cache = read_cache(BASE_CACHE)
    scen_cache = read_cache(SCEN_CACHE)
    for kid, (lo, hi, s5i, _m) in batch_keys.items():
        if (lo, hi) in base_cache:
            fail(f"{kid} already present in the BASE cache (not a fresh increment)")
        if s5i in receipt_verdicts:
            fail(f"{kid} already resolved by the update8 receipt")
    if len(scen_cache) != len(base_cache) + ADOPTED_ROWS:
        fail(f"scenario cache row count != BASE + {ADOPTED_ROWS}")
    for key, (v, _n) in incr.items():
        row = scen_cache.get(key)
        if row is None or row[0] != v:
            fail(f"scenario cache does not adopt increment row {key}")
    for key in scen_cache:
        if key not in base_cache and key not in incr:
            fail(f"scenario cache key outside BASE+increment: {key}")
    for key, (v, _n) in scen_cache.items():
        if key in base_cache and base_cache[key][0] != v:
            fail(f"scenario cache verdict drift on shared key {key}")
    base_votes = Counter(v for v, _ in base_cache.values())
    scen_votes = Counter(v for v, _ in scen_cache.values())
    if base_votes.get(1, 0) != 158:
        fail(f"BASE cache WIN rows {base_votes.get(1, 0)} != 158")
    if scen_votes.get(1, 0) != 158 or scen_votes.get(2, 0) != 6129:
        fail(f"scenario cache verdict counts not 158 WIN / 6129 LOSS: {dict(sorted(scen_votes.items()))}")
    if UNADOPTED_WIN_KEY in scen_cache:
        fail("l028 WIN key reached the scenario canonical cache (must stay unconsumed)")

    # --- graph holders of the 53 keys ---------------------------------------
    holders = {}
    for kid, (lo, hi, s5i, _m) in batch_keys.items():
        if kid not in adopted_loss_ids:
            continue
        hs = sorted(i for i, c in enumerate(s4_cost) if s5i in c)
        if BATCH_CLASS not in hs:
            fail(f"{kid} own batch class {BATCH_CLASS} not among its graph holders {hs}")
        for i in hs:
            if s4_status[i] not in (-1, 0, 1):
                fail(f"{kid} holder {i} unexpected graph status {s4_status[i]}")
        holders[kid] = hs
    holder_union = sorted(set().union(*[set(h) for h in holders.values()]))
    member_loss_counts = Counter()
    for hs in holders.values():
        for i in hs:
            member_loss_counts[i] += 1

    # --- faithful re-execution of the published refresh class pass -----------
    def refresh_statuses(cache):
        index_verdict = {}
        in_universe = 0
        for (lo, hi), (verdict, _nodes) in cache.items():
            i = mask_to_index.get((lo, hi))
            if i is None:
                continue
            in_universe += 1
            index_verdict[i] = verdict
        for i, v in receipt_verdicts.items():
            if not (0 <= i < len(s5_masks)):
                fail(f"receipt index outside universe: {i}")
            prior = index_verdict.get(i)
            if prior is not None and prior != v:
                fail(f"receipt/cache conflict at index {i}")
            index_verdict[i] = v
        for key in cache:
            if key in quarantined:
                fail(f"quarantined key inside cache: {key}")
            if not is_canonical_safe_s5_key(key):
                fail(f"noncanonical cache key {key}")
        LOSS, UNKNOWN, EXCLUDED = 0, 1, -1
        st, unknown_now = {}, {}
        for i in range(len(s4_masks)):
            base = s4_status[i]
            cost = s4_cost[i]
            if base == EXCLUDED:
                st[i] = "excluded"
                unknown_now[i] = []
                continue
            if base not in (LOSS, UNKNOWN):
                fail(f"unexpected graph base status {base} at class {i}")
            unknown, win_hit = [], False
            for j in cost:
                v = index_verdict.get(j)
                if v == 1:
                    win_hit = True
                elif v is None:
                    unknown.append(j)
            unknown_now[i] = unknown
            if base == UNKNOWN:
                st[i] = "excluded_now" if win_hit else ("free_now" if not unknown else "unknown")
            else:
                st[i] = "excluded_now" if win_hit else "free_now"
        # Board fail-closed child verification of every free candidate
        for i, s in list(st.items()):
            if s != "free_now":
                continue
            lo, hi = s4_masks[i]
            if not is_canonical_safe_s5_key((lo, hi)):
                try:
                    board.legal(lo | (hi << 64))
                except ValueError:
                    st[i] = "free_now_unverified"
                    continue
            for child in board.children(lo | (hi << 64)):
                key = (child & ((1 << 64) - 1), child >> 64)
                have = cache.get(key)
                if have is None:
                    ci = mask_to_index.get(key)
                    rv = receipt_verdicts.get(ci) if ci is not None else None
                    have = (rv, 0) if rv is not None else None
                if have is None or have[0] != 2:
                    st[i] = "free_now_unverified"
                    break
        return st, unknown_now, index_verdict, in_universe

    base_st, base_unknown, base_iv, base_in_univ = refresh_statuses(base_cache)
    scen_st, scen_unknown, _scen_iv, scen_in_univ = refresh_statuses(scen_cache)

    base_summary = json.loads((BASE_DIR / "refresh-summary.json").read_text())
    scen_summary = json.loads((SCEN_OUT / "refresh-summary.json").read_text())
    published = {"BASE": base_summary, SCENARIO: scen_summary}

    # publish-side recompute equality gates
    for name, st in (("BASE", base_st), (SCENARIO, scen_st)):
        counts = Counter(st.values())
        pub = published[name]["class_status_counts"]
        for k in ("excluded", "excluded_now", "free_now", "unknown"):
            if counts.get(k, 0) != pub.get(k, 0):
                fail(f"{name}: recomputed {k} {counts.get(k, 0)} != published {pub.get(k, 0)}")
        if counts.get("free_now_unverified", 0) != 0:
            fail(f"{name}: {counts.get('free_now_unverified', 0)} unverified free candidates")
        pub_in = published[name]["inputs"]
        iv = base_iv if name == "BASE" else _scen_iv
        iu = base_in_univ if name == "BASE" else scen_in_univ
        if pub_in["known_universe_indices"] != len(iv):
            fail(f"{name}: recomputed known universe {len(iv)} != published {pub_in['known_universe_indices']}")
        if pub_in["cache_rows_in_universe"] != iu:
            fail(f"{name}: recomputed cache rows in universe {iu} != published {pub_in['cache_rows_in_universe']}")

    # --- global status-transition gate ---------------------------------------
    transitions = Counter()
    for i in range(len(s4_masks)):
        b, s = base_st[i], scen_st[i]
        transitions[f"{b}->{s}"] += 1
        if s not in ALLOWED_TRANSITIONS.get(b, []):
            fail(f"class {i} forbidden transition {b} -> {s}")

    # --- excluded_now flips must be empty for a zero-WIN increment ----------
    base_excluded_now = {i for i, s in base_st.items() if s == "excluded_now"}
    flips = sorted(i for i, s in scen_st.items()
                   if s == "excluded_now" and i not in base_excluded_now)
    if flips:
        fail(f"excluded_now flips {flips} must be EMPTY for a zero-WIN increment")
    flipped_out = sorted(i for i, s in scen_st.items()
                         if s != "excluded_now" and i in base_excluded_now)
    if flipped_out:
        fail(f"excluded_now regressions {flipped_out} must be EMPTY")

        # --- newly free classes: all BASE-unknown children resolved by the incr --
    new_free = sorted(i for i, s in scen_st.items() if s == "free_now" and base_st[i] != "free_now")
    expected_new_free = sorted(i for i, unk in base_unknown.items()
                               if base_st[i] == "unknown" and unk
                               and all(j in incr_index for j in unk))
    if new_free != expected_new_free:
        fail(f"newly free classes {new_free} != fully-resolved expectation {expected_new_free}")
    if BATCH_CLASS in new_free:
        fail("class 1849 must NOT free: the l028 WIN stays unconsumed, so one "
             "unknown cost child remains and the class stays unknown")
    if scen_st[BATCH_CLASS] != "unknown":
        fail(f"class 1849 scenario status {scen_st[BATCH_CLASS]} != unknown (l028 stays unconsumed)")
    basec = sorted(base_unknown[BATCH_CLASS])
    if len(basec) != 53:
        fail(f"class 1849 BASE-unknown cost children {len(basec)} != 53")
    if not set(incr_index) <= set(basec):
        fail("increment s5 indices are not all BASE-unknown cost children of class 1849")
    leftover = sorted(set(basec) - set(incr_index))
    if leftover != [UNADOPTED_WIN_S5]:
        fail(f"class 1849 leftover BASE-unknown children != exactly the l028 s5 index "
             f"{UNADOPTED_WIN_S5}: {leftover}")
    if sorted(scen_unknown[BATCH_CLASS]) != leftover:
        fail("class 1849 scenario-unknown children != leftover arithmetic")
    if UNADOPTED_WIN_S5 in incr_index:
        fail("the l028 s5 index is inside the increment (adoption gate)")
    batch_s5 = {v[2] for v in batch_keys.values()}
    if batch_s5 != set(basec):
        fail(f"batch-26 key set != the 53 BASE-unknown cost children of class 1849 "
             f"(batch-only {sorted(batch_s5 - set(basec))[:5]}, "
             f"base-only {sorted(set(basec) - batch_s5)[:5]})")

# --- holder-class table with own-membership arithmetic gate --------------
    holder_rows = {}
    for c in holder_union:
        own = sorted(j for j in incr_index if j in s4_cost[c])
        row = {
            "base_status": base_st[c],
            "base_unknown_now": len(base_unknown[c]),
            "own_membership_in_increment": len(own),
            "scenario_status": scen_st[c],
            "scenario_unknown_now": len(scen_unknown[c]),
        }
        if base_st[c] == "excluded":
            if len(scen_unknown[c]) != 0:
                fail(f"holder class {c} excluded at BASE but scenario unknown_now != 0")
        elif len(base_unknown[c]) - len(own) != len(scen_unknown[c]):
            fail(f"holder class {c}: scenario unknown_now {len(scen_unknown[c])} != "
                 f"BASE {len(base_unknown[c])} - own {len(own)}")
        holder_rows[str(c)] = row
    # additivity: own memberships over holder classes must account to exactly the
    # 52 adopted rows' graph memberships (each key's holder count from batch-keys
    # cross-checked against the graph holder sets)
    for kid, (lo, hi, s5i, mcnt) in batch_keys.items():
        if kid not in adopted_loss_ids:
            continue
        if len(holders[kid]) != int(mcnt):
            fail(f"{kid} graph holder count {len(holders[kid])} != batch-keys "
                 f"membership_class_count {mcnt}")

    # --- published metric table and deltas -----------------------------------
    def metric_set(pub):
        csc = pub["class_status_counts"]
        fr = pub["frozen_update8_refresh"]
        return {
            "excluded_now_classes": csc.get("excluded_now", 0),
            "free_now_classes": csc.get("free_now", 0),
            "unknown_classes": csc.get("unknown", 0),
            "update8_remaining_now": fr["remaining_now"],
            "update8_resolved_count": fr["resolved_count"],
            "update8_win_hit_groups": len(fr["win_hit_groups"]),
            "update8_groups_free_now": fr["groups_free_now"],
            "joint_greedy_unique_groups": pub["joint_greedy"]["unique_groups"],
            "joint_greedy_union_size": pub["joint_greedy"]["greedy_union_size"],
            "probe_worklist_total": pub["worklist_total"],
            "group_best_options_nonfree": pub["group_best_options_nonfree"],
            "closure_classes_count": pub["closure_classes_count"],
        }

    flat = {"BASE": metric_set(base_summary), SCENARIO: metric_set(scen_summary)}
    metrics = {}
    for k in flat["BASE"]:
        metrics[k] = {"base": flat["BASE"][k], "scenario": flat[SCENARIO][k],
                     "delta": flat[SCENARIO][k] - flat["BASE"][k]}

    # --- update8 resolved-requirement delta, gated to the increment ----------
    base_resolved = set(base_summary["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    scen_resolved = set(scen_summary["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    lost = sorted(base_resolved - scen_resolved)
    if lost:
        fail(f"update8 resolutions lost: {lost}")
    newly_resolved = sorted(scen_resolved - base_resolved)
    outside = [j for j in newly_resolved if j not in incr_index]
    if outside:
        fail(f"newly resolved s5 outside the increment universe: {outside}")
    if len(newly_resolved) != metrics["update8_resolved_count"]["delta"]:
        fail("update8 resolved-count arithmetic inconsistent with the resolved-set delta")
    for j in newly_resolved:
        lo, hi = incr_index[j]
        if incr[(lo, hi)][0] != 2:
            fail(f"newly resolved s5 {j} increment row is not LOSS")

    # --- per-root coverage recompute + published csv gates -------------------
    def per_root_free_thirds(st):
        per_root = {}
        per_third = {}
        for r in roots:
            free = 0
            for third in r["thirds"]:
                opts = third["options"]
                is_free = bool(opts) and any(st.get(o) == "free_now" for o in opts)
                per_third[(r["origin_first"], third["third"])] = is_free
                if is_free:
                    free += 1
            per_root[r["origin_first"]] = (r["role"], len(r["thirds"]), free)
        return per_root, per_third

    base_by_root, base_by_third = per_root_free_thirds(base_st)
    scen_by_root, scen_by_third = per_root_free_thirds(scen_st)

    def load_prc(path):
        rows = {}
        with Path(path).open() as fh:
            for r in csv.DictReader(fh):
                ig = r["individual_greedy_union"]
                rows[(r["role"], int(r["first"]))] = (
                    int(r["thirds"]), int(r["free_now"]), int(r["uncovered"]),
                    int(ig) if ig else None)
        return rows

    base_prc = load_prc(BASE_DIR / "per-root-coverage.csv")
    scen_prc = load_prc(SCEN_OUT / "per-root-coverage.csv")
    if set(base_prc) != set(scen_prc):
        fail("per-root row set changed between BASE and scenario")
    if len(base_prc) != len(roots):
        fail(f"per-root row count {len(base_prc)} != graph roots {len(roots)}")
    for prc, by_root, by_third, name in ((base_prc, base_by_root, base_by_third, "BASE"),
                                         (scen_prc, scen_by_root, scen_by_third, SCENARIO)):
        if len(by_third) != sum(len(r["thirds"]) for r in roots):
            fail(f"{name}: per-third recount mismatch")
        for (role, first), (thirds, free, uncov, _ig) in prc.items():
            rr, rt, rf = by_root[first]
            if rr != role or rt != thirds or rf != free:
                fail(f"{name}: recomputed root {first} ({rr},{rt},{rf}) != "
                     f"published ({role},{thirds},{free})")
            if free + uncov != thirds:
                fail(f"{name}: root {first} free+uncovered != thirds")
        if len({r["origin_first"] for r in roots}) != len(roots):
            fail("graph roots origin_first not unique")

    # root 27 baseline stays 119/119 in both
    for name, pub in published.items():
        r0 = pub["roots"][0]
        if (r0["role"], r0["origin_first"], r0["thirds"], r0["free_thirds_now"], r0["uncovered"]) \
                != ("known-loss-baseline", 27, 119, 119, 0):
            fail(f"{name}: roots[0] not the 119/119 known-loss baseline: {r0}")
    for prc in (base_prc, scen_prc):
        if prc[("known-loss-baseline", 27)][:3] != (119, 119, 0):
            fail("baseline per-root row not 119/119")

    # changed rows and newly free thirds, machine-identified
    newly_free_thirds = [{"first": f, "third": t}
                         for (f, t), base_free in sorted(base_by_third.items())
                         if not base_free and scen_by_third[(f, t)]]
    for entry in newly_free_thirds:
        opts = None
        for r in roots:
            if r["origin_first"] == entry["first"]:
                for third in r["thirds"]:
                    if third["third"] == entry["third"]:
                        opts = third["options"]
                        break
                break
        if opts is None or not set(opts) & set(new_free):
            fail(f"newly free third {entry} lacks a newly free class among its options")
    changed_rows = {}
    for (role, first), (thirds, bfree, buncov, big) in base_prc.items():
        sthirds, sfree, suncov, sig = scen_prc[(role, first)]
        if (bfree, buncov) == (sfree, suncov):
            continue
        if sfree < bfree or suncov > buncov:
            fail(f"root {first}: coverage regressed ({bfree},{buncov})->({sfree},{suncov})")
        if sfree + suncov != thirds or bfree + buncov != thirds:
            fail(f"root {first}: free+uncovered != thirds after change")
        changed_rows["|".join((role, str(first)))] = {
            "base": {"free_now": bfree, "uncovered": buncov},
            "scenario": {"free_now": sfree, "uncovered": suncov},
            "free_delta": sfree - bfree,
            "uncovered_delta": suncov - buncov,
            "individual_greedy_union": {"base": big, "scenario": sig},
        }
    if not new_free:
        if newly_free_thirds or changed_rows:
            fail("no newly free class but per-root free coverage changed")
    else:
        expected_changed = set()
        for r in roots:
            f = r["origin_first"]
            if any(entry["first"] == f for entry in newly_free_thirds):
                expected_changed.add("|".join((r["role"], str(f))))
        if set(changed_rows) != expected_changed:
            fail(f"changed per-root rows {sorted(changed_rows)} != rows with a newly free third {sorted(expected_changed)}")

    # --- per-root greedy and roots summary movers (measured) -----------------
    prg_base = base_summary["per_root_greedy"]
    prg_scen = scen_summary["per_root_greedy"]
    if set(prg_base) != set(prg_scen):
        fail("per-root greedy root set changed")
    per_root_greedy_movers = {}
    for first in sorted(prg_base, key=lambda x: int(x)):
        b, s = prg_base[first], prg_scen[first]
        row = {"base_greedy_union_size": b["greedy_union_size"],
               "scenario_greedy_union_size": s["greedy_union_size"],
               "delta": s["greedy_union_size"] - b["greedy_union_size"],
               "base_free_thirds": b["free_thirds"],
               "scenario_free_thirds": s["free_thirds"],
               "base_uncovered_thirds": b["uncovered_thirds"],
               "scenario_uncovered_thirds": s["uncovered_thirds"]}
        per_root_greedy_movers[first] = row
    roots_summary_moved = {}
    base_roots_rows = {r["origin_first"]: r for r in base_summary["roots"]}
    for r in scen_summary["roots"]:
        b = base_roots_rows[r["origin_first"]]
        if (b["free_thirds_now"], b["uncovered"]) != (r["free_thirds_now"], r["uncovered"]):
            roots_summary_moved[str(r["origin_first"])] = {
                "base": [b["free_thirds_now"], b["uncovered"]],
                "scenario": [r["free_thirds_now"], r["uncovered"]],
            }

        # --- closure-candidate table observations ---------------------------------
    def load_closure(path):
        with Path(path).open() as fh:
            return list(csv.DictReader(fh))

    base_cc = load_closure(BASE_DIR / "closure-classes.csv")
    scen_cc = load_closure(SCEN_OUT / "closure-classes.csv")
    b1849 = [r for r in base_cc if int(r["class_index"]) == BATCH_CLASS]
    if len(b1849) != 1:
        fail(f"class 1849 appears {len(b1849)} times in the BASE closure-candidate table")
    if int(b1849[0]["unknown_now"]) != 53:
        fail(f"BASE closure row for 1849 unknown_now {b1849[0]['unknown_now']} != 53")
    s1849 = [r for r in scen_cc if int(r["class_index"]) == BATCH_CLASS]
    if len(s1849) != 1:
        fail("class 1849 must STAY in the scenario closure-candidate table "
             "(l028 unconsumed keeps the class unknown)")
    if int(s1849[0]["unknown_now"]) != 1:
        fail(f"scenario closure row for 1849 unknown_now {s1849[0]['unknown_now']} != 1 "
             "(must be exactly the unconsumed l028 child)")
    s23101 = [r for r in scen_cc if int(r["class_index"]) == 23101]
    b23101 = [r for r in base_cc if int(r["class_index"]) == 23101]
    if len(s23101) != 1 or int(s23101[0]["unknown_now"]) != 1:
        fail("class 23101 must stay in the scenario closure-candidate table with "
             "unknown_now 1 (untouched by this adoption)")
    if len(b23101) != 1 or int(b23101[0]["unknown_now"]) != 1:
        fail("class 23101 BASE closure row drift (must be unknown_now 1)")
    s12643 = [r for r in scen_cc if int(r["class_index"]) == 12643]
    b12643 = [r for r in base_cc if int(r["class_index"]) == 12643]
    if len(s12643) != 1 or int(s12643[0]["unknown_now"]) != 53:
        fail("class 12643 must stay in the scenario closure-candidate table with "
             "unknown_now 53 (untouched by this adoption)")
    if len(b12643) != 1 or int(b12643[0]["unknown_now"]) != 53:
        fail("class 12643 BASE closure row drift (must be unknown_now 53)")
    base_idx = {int(r["class_index"]) for r in base_cc}
    scen_idx = {int(r["class_index"]) for r in scen_cc}
    left = sorted(base_idx - scen_idx)
    entered = sorted(scen_idx - base_idx)
    # churn safety gate: leaving/entering the RANKED candidate table may only be
    # scheduling/ranking bookkeeping (class-1849 remaining count 53->1 changes
    # which option class is cheapest for the affected groups); every churned
    # class must keep its recomputed BASE == scenario status "unknown".
    for c in left + entered:
        if base_st[c] != "unknown" or scen_st[c] != "unknown":
            fail(f"closure-table churn class {c} changed recomputed status "
                 f"{base_st[c]} -> {scen_st[c]} (churn must be pure ranking bookkeeping)")
    if BATCH_CLASS in left:
        fail("class 1849 left the closure-candidate table (a status artifact, not ranking churn)")
    closure_rows = {
        "base_class_1849_row": b1849[0],
        "base_class_1849_rank": int(b1849[0]["class_rank"]),
        "base_class_1849_unknown_now": int(b1849[0]["unknown_now"]),
        "scenario_class_1849_row": s1849[0],
        "scenario_class_1849_rank": int(s1849[0]["class_rank"]),
        "scenario_class_1849_unknown_now": int(s1849[0]["unknown_now"]),
        "base_class_23101_row": b23101[0],
        "scenario_class_23101_row": s23101[0],
        "base_class_12643_row": b12643[0],
        "scenario_class_12643_row": s12643[0],
        "scenario_first_row": scen_cc[0] if scen_cc else None,
        "left_table_classes": left,
        "entered_table_classes": entered,
        "churn_gate": ("left/entered classes are ranked-worklist best-option churn "
                       "only: every churned class keeps recomputed BASE == scenario "
                       "status unknown, driven by the class-1849 remaining count "
                       "53->1; no class freed, none excluded, none entered the "
                       "unknown population"),
    }

# --- output --------------------------------------------------------------
    out = {
        "schema": "n11-batch26-adoption-decomp-deltas-v1",
        "scenario": ("ADOPTED-CANONICAL = pre-adoption BASE (canonical 6,235 rows, Part BI "
                     "reaudit state) + the 52 LOSS rows of batch-26 (class 1849); "
                     "full != loss: the resolved packet additionally holds the l028 WIN "
                     "row (honest label), which stays UNCONSUMED (scrutiny owner C++ "
                     "second-implementation gate pin 9193f5b6...; batch-14residual q042 "
                     "precedent), so class 1849 keeps exactly one unknown cost child"),
        "interpretation_guard": ("canonical adoption deltas: only the 52 LOSS rows of "
                                 "batch-26 are consumed into the canonical cache via "
                                 "the fail-closed union merger; the l028 WIN verdict "
                                 "is NOT consumed (28 unconsumed closure WIN "
                                 "candidates, l028 included, stay untouched); NO class "
                                 "frees in this adoption (class 1849 remains unknown "
                                 "with exactly its l028 WIN child); scheduling "
                                 "quantities are bookkeeping; every claim stays "
                                 "UNKNOWN; 11x11 empty board and all 19 roots stay "
                                 "UNKNOWN; nodes are bookkeeping"),
        "recompute_gates": ("class statuses with Board free-candidate child verification, "
                            "known-universe counts and per-root free coverage were "
                            "recomputed from graph + update8 + cache and asserted equal "
                            "to the published BASE (Part BI reaudit) and scenario "
                            "outputs before any delta was emitted"),
        "pins": {
            "increment_sha256": INCR_SHA,
            "scenario_cache_sha256": SCEN_CACHE_SHA,
            "base_cache_sha256": BASE_CACHE_SHA,
            "base_summary_sha256": BASE_SUMMARY_SHA,
            "scenario_summary_sha256": SCEN_SUMMARY_SHA,
            "base_closure_classes_sha256": BASE_CLOSURE_SHA,
            "base_per_root_coverage_sha256": BASE_PRC_SHA,
            "scenario_closure_classes_sha256": SCEN_CLOSURE_SHA,
            "scenario_per_root_coverage_sha256": SCEN_PRC_SHA,
            "batch_keys_sha256": BATCH_KEYS_SHA,
            "row_audit_sha256": ROW_AUDIT_SHA,
        },
        "batch_keys": {
            "count": 53, "adopted_loss": 52, "unadopted_win": 1,
            "batch_class": BATCH_CLASS,
            "class_mask": list(s4_masks[BATCH_CLASS]),
            "cost_children_total": len(s4_cost[BATCH_CLASS]),
            "batch_groups_served": [list(x) for x in batch_groups_served],
        },
        "excluded_now_flips": flips,
        "newly_free_now_classes": new_free,
        "newly_free_now_gate": ("the loss-only packet can only free classes whose "
                                "BASE-unknown children are ALL resolved by the "
                                "increment; machine-computed list is empty here; "
                                "class 1849 does NOT free (l028 unconsumed)"),
        "status_transitions": dict(sorted(transitions.items())),
        "class_1849": {
            "base_unknown_children": len(base_unknown[BATCH_CLASS]),
            "adopted_by_increment": len(incr_index),
            "leftover_unknown_children": leftover,
            "leftover_is_l028": leftover == [UNADOPTED_WIN_S5],
            "scenario_unknown_children": len(scen_unknown[BATCH_CLASS]),
            "scenario_status": scen_st[BATCH_CLASS],
        },
        "unadopted_win_row": {
            "key_id": UNADOPTED_WIN_KID, "s5_index": UNADOPTED_WIN_S5,
            "key": [UNADOPTED_WIN_KEY[0], UNADOPTED_WIN_KEY[1]],
            "result": 1, "nodes": UNADOPTED_WIN_NODES,
            "consumed": False,
            "note": ("honest WIN label only; adopted nowhere; stays unconsumed with "
                     "the 28 unconsumed closure WIN candidates (l028 included); "
                     "scrutiny owner C++ second-implementation gate pin 9193f5b6... "
                     "decides; Part BS third-impl + pinned-replica backing"),
        },
        "newly_free_thirds": newly_free_thirds,
        "changed_per_root_coverage_rows": changed_rows,
        "holder_union_size": len(holder_union),
        "holder_classes": holder_rows,
        "member_loss_counts": {str(k): v for k, v in sorted(member_loss_counts.items())},
        "metrics": metrics,
        "update8": {
            "newly_resolved_s5": newly_resolved,
            "newly_resolved_count": len(newly_resolved),
            "lost_resolved": lost,
        },
        "per_root_greedy": per_root_greedy_movers,
        "roots_summary_moved": roots_summary_moved,
        "closure_candidate_rows": closure_rows,
    }
    OUT.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("OK decomp-deltas-batch26-adoption.json: "
          f"flips={flips} new_free={new_free} "
          f"free_now {metrics['free_now_classes']['base']}->{metrics['free_now_classes']['scenario']} "
          f"class1849_unknown {len(base_unknown[BATCH_CLASS])}->{len(scen_unknown[BATCH_CLASS])} "
          f"(leftover={leftover} l028 unconsumed) "
          f"update8_resolved +{len(newly_resolved)} "
          f"joint_greedy {metrics['joint_greedy_union_size']['base']}->{metrics['joint_greedy_union_size']['scenario']} "
          f"worklist {metrics['probe_worklist_total']['base']}->{metrics['probe_worklist_total']['scenario']} "
          f"changed_rows={sorted(changed_rows)} "
          f"closure_churn left={closure_rows['left_table_classes']} entered={closure_rows['entered_table_classes']}")


if __name__ == "__main__":
    main()
