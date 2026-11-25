#!/usr/bin/env python3
"""Batch-16 (class 10687) 52-LOSS canonical-adoption reaudit delta extractor (Part AP).

Fail-closed, read-only audit executing the single-owner Part AP
declaration (note amendment of 2026-11-22, published after the Part AP
declaration).  Compares the published BASE refresh outputs (Part AH base
control on the pre-adoption canonical cache 95e868d6...) against the single
post-adoption computation:

  PLOSS52 = BASE + all 52 resolved rows (t001..t052, all LOSS) of batch-16

Batch-16 probed the full unknown cost boundary of class 10687 with 2-pass
node-exact results: 52 LOSS / 0 WIN / 0 exhausted / 0 mismatch, so there is
no PWIN scenario and no exhaustion split: adopting the batch == adopting
its 52 LOSS rows.  That identity is machine-asserted from the published
increments manifest and batch-keys before any delta is emitted.

The published refresh semantics are re-executed faithfully from the pinned
graph + update8 receipt + cache verdicts (per-class verdict-level status
with Board fail-closed child verification of every free candidate), and
the recomputed class_status_counts, known-universe counts and per-root
coverage counts are asserted equal to the published BASE and PLOSS52
outputs before any delta is emitted.

Gates (all fail-closed):
  * sha256 pins: increment, scenario cache, base cache, base summary,
    scenario summary, batch-keys,
  * manifest: 52 resolved / 52 LOSS / 0 WIN / 0 exhausted, win_ids and
    exhausted_excluded_ids empty, full_packet_eq_loss_only,
    win_scenario_exists false, loss sha == increment sha,
  * the 52 increment keys exist, are canonical, unquarantined, absent from
    the BASE cache and the update8 receipt, map to their published s5
    indices, and are exactly the BASE-unknown cost children of class 10687,
  * scenario cache == BASE rows + increment rows with verdict agreement,
  * every recomputed status transition is one of
    excluded->excluded, excluded_now->excluded_now, free_now->free_now,
    unknown->{unknown, free_now},
  * excluded_now flip set EMPTY (a zero-WIN increment cannot flip),
  * newly free_now classes == exactly the classes whose BASE-unknown cost
    children are ALL resolved by the increment, here == {10687},
  * every graph holder class of the 52 keys: scenario unknown_now ==
    BASE unknown_now - own membership in the increment,
  * update8 newly-resolved baseline requirements inside the increment
    universe, no resolution lost, count arithmetic consistent,
  * per-root coverage recomputed from the graph matches the published
    per-root-coverage.csv for BASE and PLOSS52; root 27 stays 119/119;
    changed rows are exactly the roots with a newly free third; every newly
    free third contains a newly free class among its options,
  * class 10687 leaves the scenario closure-candidate table.

Measured (recorded, not gated, scheduling quantities only): per-root and
joint greedy remaining-requirement sizes, probe worklist size, roots
summary rows, closure-candidate rows, group-best option counts.

The 52 LOSS rows ARE consumed into the canonical cache by the Part AP
fail-closed merger (a zero-WIN, zero-exhaustion full-packet adoption); the
only claim established by this reaudit is the closure qualification of
class 10687 (Board-verified free_now, the 36th free class), never a 19-root
or 11x11 result; nodes are bookkeeping only.  The 11x11 empty board stays
UNKNOWN; all 19 central-reply roots stay UNKNOWN.
"""
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
OUT = EXP / "output/decomp-deltas-batch16-adoption.json"

GRAPH =ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_DIR = ROOT / "research/experiments/n11-class8106-n005n006-base-control-20261122/output"
BASE_CACHE = ROOT / "research/experiments/n11-central-reply-8784-closure-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-20261122.cache"
BATCH_DIR = ROOT / "research/experiments/n11-centralreply-closure-class10687-batch16-20261122"
SCEN_OUT = EXP / "reaudit/output"
INCR_CACHE = EXP / "output/increment-batch16-loss52-IFADOPTED-20261122.cache"
MANIFEST = EXP / "output/increments-manifest.json"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-20261122.cache"

INCR_SHA = "95345a5b1484614940e133e042b005ccc5963df15ecb7e5651f092761aa8a7f0"
SCEN_CACHE_SHA = "342e86838e0c2bef915798059cb397f7c91e59c65426bf74db19530ecdd7979e"
BASE_CACHE_SHA = "95e868d6762925b9a27ad963a825a9ad4fd5131a864eb82fac0db77d7acdb326"
BASE_SUMMARY_SHA = "25987addd9bfdb901b341288ca1543ab5f893e77471da636a345c1edfd2acb96"
SCEN_SUMMARY_SHA = "b278f822627560d7c3945ee0c0aded7de415b6141a69f0f8722e670432fc48da"
BATCH_KEYS_SHA = "465cf44721a661ce94babe12212c26c697ebb346392548fcdafaa9d3e8c3dd4e"

SCENARIO = "PLOSS52"
BATCH_CLASS = 10687
UNIVERSE_SIZE = 31859
RECEIPT_COUNT = 23
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
                          ("batch-keys", BATCH_DIR / "input/batch-keys.json", BATCH_KEYS_SHA)):
        got = sha(p)
        if got != want:
            fail(f"{name} sha256 drift: {got} != {want}")

    manifest = json.loads(MANIFEST.read_text())
    rc = manifest["row_counts"]
    if not (rc["resolved_rows"] == 52 and rc["losses"] == 52 and rc["wins"] == 0
            and rc["exhausted_excluded"] == 0):
        fail(f"manifest row_counts not 52 LOSS / 0 WIN / 0 exhausted: {rc}")
    if manifest["win_ids"] != [] or manifest["exhausted_excluded_ids"] != []:
        fail(f"manifest win/exhaustion id lists not empty: {manifest}")
    if manifest["full_packet_eq_loss_only"] is not True or manifest["win_scenario_exists"] is not False:
        fail("manifest full==loss identity not asserted")
    if manifest["sha256"]["loss"] != INCR_SHA:
        fail("manifest loss sha does not match the pinned increment")

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
    batch_groups_served = sorted((int(e["first"]), int(e["third"]))
                                 for e in bk["groups_served_full"])
    if [int(x) for x in bk["class_mask"]] != list(s4_masks[BATCH_CLASS]):
        fail("batch-keys class_mask != graph mask of the batch class")
    if not batch_groups_served:
        fail("batch-keys groups_served_full empty for a closure-class batch")
    if len(bk["keys"]) != 52:
        fail(f"batch-keys count {len(bk['keys'])} != 52")
    batch_keys = {}
    for k in bk["keys"]:
        kid = k["key_id"]
        lo, hi, s5i = int(k["lo"]), int(k["hi"]), int(k["s5_index"])
        if mask_to_index.get((lo, hi)) != s5i:
            fail(f"{kid} (lo,hi) does not map to its published s5 index {s5i}")
        if (lo, hi) in quarantined or not is_canonical_safe_s5_key((lo, hi)):
            fail(f"{kid} noncanonical or quarantined key")
        batch_keys[kid] = (lo, hi, s5i, int(k["membership_class_count"]))
    if len(set(v[2] for v in batch_keys.values())) != 52:
        fail("batch-16 keys collide on s5 indices")

    incr = read_cache(INCR_CACHE)
    if len(incr) != 52:
        fail(f"increment row count {len(incr)} != 52")
    if any(v[0] != 2 for v in incr.values()):
        fail("increment contains a non-LOSS verdict")
    incr_index = {}
    for kid, (lo, hi, s5i, _m) in batch_keys.items():
        row = incr.get((lo, hi))
        if row is None:
            fail(f"{kid} (lo,hi) missing from the increment")
        if row[0] != 2:
            fail(f"{kid} increment row is not LOSS")
        incr_index[s5i] = (lo, hi)
    if set(incr) != {(lo, hi) for (lo, hi, _s, _m) in batch_keys.values()}:
        fail("increment key set != batch-16 key set")

    base_cache = read_cache(BASE_CACHE)
    scen_cache = read_cache(SCEN_CACHE)
    for kid, (lo, hi, s5i, _m) in batch_keys.items():
        if (lo, hi) in base_cache:
            fail(f"{kid} already present in the BASE cache (not a fresh increment)")
        if s5i in receipt_verdicts:
            fail(f"{kid} already resolved by the update8 receipt")
    if len(scen_cache) != len(base_cache) + 52:
        fail("scenario cache row count != BASE + 52")
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
    if scen_votes.get(1, 0) != 158 or scen_votes.get(2, 0) != 5921:
        fail(f"scenario cache verdict counts not 158 WIN / 5921 LOSS: {dict(sorted(scen_votes.items()))}")

    # --- graph holders of the 52 keys ---------------------------------------
    holders = {}
    for kid, (lo, hi, s5i, _m) in batch_keys.items():
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

    # --- newly free classes: all BASE-unknown children resolved by the incr --
    new_free = sorted(i for i, s in scen_st.items() if s == "free_now" and base_st[i] != "free_now")
    expected_new_free = sorted(i for i, unk in base_unknown.items()
                               if base_st[i] == "unknown" and unk
                               and all(j in incr_index for j in unk))
    if new_free != expected_new_free:
        fail(f"newly free classes {new_free} != fully-resolved expectation {expected_new_free}")
    if new_free != [BATCH_CLASS]:
        fail(f"newly free set {new_free} != the batch class [{BATCH_CLASS}]")
    if sorted(base_unknown[BATCH_CLASS]) != sorted(incr_index):
        fail("class 10687 BASE-unknown children != the 52 increment s5 indices")
    if len(s4_cost[BATCH_CLASS]) != 52:
        fail(f"class 10687 full cost size {len(s4_cost[BATCH_CLASS])} != 52")

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
        # per-third free recompute must cover every graph third exactly once
        if len(by_third) != sum(len(r["thirds"]) for r in roots):
            fail(f"{name}: per-third recount mismatch")
        n_free_thirds = 0
        for (role, first), (thirds, free, uncov, _ig) in prc.items():
            rr, rt, rf = by_root[first]
            if rr != role or rt != thirds or rf != free:
                fail(f"{name}: recomputed root {first} ({rr},{rt},{rf}) != "
                     f"published ({role},{thirds},{free})")
            if free + uncov != thirds:
                fail(f"{name}: root {first} free+uncovered != thirds")
            n_free_thirds += free
        # roots must be keyed uniquely by origin_first
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
    batch_groups_served_set = {(f, t) for f, t in batch_groups_served}
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
    measured_new_thirds = {(e["first"], e["third"]) for e in newly_free_thirds}
    if measured_new_thirds != batch_groups_served_set:
        fail(f"newly free thirds {sorted(measured_new_thirds)} != batch groups_served "
             f"{sorted(batch_groups_served_set)}")
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
    b10687 = [r for r in base_cc if int(r["class_index"]) == BATCH_CLASS]
    if len(b10687) == 0:
        fail("class 10687 missing from the BASE closure-candidate table")
    if len(b10687) > 1:
        fail("class 10687 duplicated in the BASE closure-candidate table")
    if int(b10687[0]["unknown_now"]) != 52:
        fail(f"BASE closure row for 10687 unknown_now {b10687[0]['unknown_now']} != 52")
    if any(int(r["class_index"]) == BATCH_CLASS for r in scen_cc):
        fail("class 10687 still present in the scenario closure-candidate table")
    closure_rows = {
        "base_class_10687_rank": int(b10687[0]["class_rank"]),
        "base_rank14_row": next((r for r in base_cc if r["class_rank"] == "14"), None),
        "scenario_rank14_row": next((r for r in scen_cc if r["class_rank"] == "14"), None),
        "scenario_first_row": scen_cc[0] if scen_cc else None,
        "scenario_class_10661_row": next((r for r in scen_cc if int(r["class_index"]) == 10661), None),
    }

    # --- output --------------------------------------------------------------
    out = {
        "schema": "n11-batch16-adoption-decomp-deltas-v1",
        "scenario": "ADOPTED-CANONICAL = pre-adoption BASE + the 52 LOSS rows of batch-16 (class 10687); full==loss; the 52 LOSS rows are consumed into the canonical cache",
        "interpretation_guard": ("canonical adoption deltas: the 52 LOSS rows of "
                                 "batch-16 are consumed into the canonical cache via the "
                                 "fail-closed union merger; scheduling quantities are "
                                 "bookkeeping; class 10687 is Board-verified free_now (the "
                                 "36th free class) in the reaudit refresh against the "
                                 "adopted canonical cache, establishing its closure "
                                 "qualification under the Part AP declaration; 11x11 "
                                 "empty board and all 19 roots stay UNKNOWN; nodes are "
                                 "bookkeeping"),
        "recompute_gates": ("class statuses with Board free-candidate child verification, "
                            "known-universe counts and per-root free coverage were "
                            "recomputed from graph + update8 + cache and asserted equal "
                            "to the published BASE and PLOSS52 outputs before any delta "
                            "was emitted"),
        "pins": {
            "increment_sha256": INCR_SHA,
            "scenario_cache_sha256": SCEN_CACHE_SHA,
            "base_cache_sha256": BASE_CACHE_SHA,
            "base_summary_sha256": BASE_SUMMARY_SHA,
            "scenario_summary_sha256": SCEN_SUMMARY_SHA,
            "batch_keys_sha256": BATCH_KEYS_SHA,
        },
        "batch_keys": {
            "count": len(batch_keys), "all_loss": True, "batch_class": BATCH_CLASS,
            "class_mask": list(s4_masks[BATCH_CLASS]),
            "cost_children_total": len(s4_cost[BATCH_CLASS]),
        },
        "excluded_now_flips": flips,
        "newly_free_now_classes": new_free,
        "newly_free_now_gate": ("each newly free class was BASE-unknown and every "
                                "BASE-unknown cost child is resolved by the increment; "
                                "a zero-WIN batch can only free, never flip"),
        "status_transitions": dict(sorted(transitions.items())),
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
    print("OK decomp-deltas-batch16-adoption.json: "
          f"flips={flips} new_free={new_free} "
          f"free_now {metrics['free_now_classes']['base']}->{metrics['free_now_classes']['scenario']} "
          f"update8_resolved +{len(newly_resolved)} "
          f"joint_greedy {metrics['joint_greedy_union_size']['base']}->{metrics['joint_greedy_union_size']['scenario']} "
          f"worklist {metrics['probe_worklist_total']['base']}->{metrics['probe_worklist_total']['scenario']} "
          f"changed_rows={sorted(changed_rows)}")


if __name__ == "__main__":
    main()
