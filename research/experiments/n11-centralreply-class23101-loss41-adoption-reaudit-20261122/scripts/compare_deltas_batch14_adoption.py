#!/usr/bin/env python3
"""Batch-14 (class 23101) 41-LOSS canonical-adoption reaudit delta extractor (Part AS).

Fail-closed, read-only audit executing the single-owner Part AS
declaration (note amendment of 2026-11-22, declaration commit 5b6af2ed).
Compares the published BASE refresh outputs (Part AP reaudit on the
pre-adoption canonical cache 342e8683..., 6,079 rows) against the single
post-adoption computation:

  ADOPTED-CANONICAL = BASE + the 41 resolved LOSS rows (q001..q041) of
  batch-14 (class 23101)

Batch-14 probed 42 of the 52 unknown cost children of class 23101 with
2-pass node-exact results: 41 LOSS / 1 WIN (q042) / 0 exhausted / 0
mismatch, stopping on the pre-registered WIN-HALT rule.  The single WIN
row q042 (s5_index 745184, result 1, 9,149,084 nodes) is NOT consumed
anywhere in this adoption: its verdict stays unconsumed (scrutiny owner
gate 9193f5b6... unchanged), so the full resolved packet (42 rows) is NOT
identical to the adopted 41 LOSS rows - full != loss here, and that
non-identity plus the q042 exclusion is machine-asserted from the
published batch-14 raws/status/batch-keys and the increments manifest
before any delta is emitted.

The published refresh semantics are re-executed faithfully from the pinned
graph + update8 receipt + cache verdicts (per-class verdict-level status
with Board fail-closed child verification of every free candidate), and
the recomputed class_status_counts, known-universe counts and per-root
coverage counts are asserted equal to the published BASE and scenario
outputs before any delta is emitted.

Gates (all fail-closed):
  * sha256 pins: increment, scenario cache, base cache, base summary,
    scenario summary, base closure-classes.csv, base per-root-coverage.csv,
    batch-keys,
  * manifest: 41 resolved / 41 LOSS / 0 adopted WIN / 0 exhausted,
    win_ids empty, unadopted_win_ids == ['q042'], full_packet_eq_loss_only
    false, win_scenario_exists true, loss sha == increment sha,
  * the 41 increment keys exist, are canonical, unquarantined, absent from
    the BASE cache and the update8 receipt, map to their published s5
    indices, and are all BASE-unknown cost children of class 23101;
  * q042 non-consumption: its key and s5 index are absent from the BASE
    cache, the increment, the scenario cache, the quarantine registry and
    both index_verdict maps, and remain among the scenario-unknown cost
    children of class 23101;
  * scenario cache == BASE rows + increment rows with verdict agreement;
  * every recomputed status transition is one of
    excluded->excluded, excluded_now->excluded_now, free_now->free_now,
    unknown->{unknown, free_now},
  * excluded_now flip set EMPTY (a zero-WIN increment cannot flip),
  * newly free_now classes == exactly the classes whose BASE-unknown cost
    children are ALL resolved by the increment (computed, not hardcoded;
    in this adoption class 23101 itself can NOT be among them because
    q042 + the 10 unprobed keys stay unresolved - gated explicitly),
  * class 23101: 52 BASE-unknown cost children, of which exactly the 41
    increment keys are resolved, leaving exactly 11 scenario-unknown
    children including s5 index 745184 (q042),
  * every graph holder class of the 41 keys: scenario unknown_now ==
    BASE unknown_now - own membership in the increment,
  * update8 newly-resolved baseline requirements inside the increment
    universe, no resolution lost, count arithmetic consistent,
  * per-root coverage recomputed from the graph matches the published
    per-root-coverage.csv for BASE and scenario; root 27 stays 119/119;
    with no newly free class there must be no newly free third and no
    changed per-root coverage row,
  * class 23101 stays in the scenario closure-candidate table as an
    unknown class with unknown_now 11 (it neither closes nor is excluded
    by this adoption).

Measured (recorded, not gated, scheduling quantities only): per-root and
joint greedy remaining-requirement sizes, probe worklist size, roots
summary rows, closure-candidate rows (incl. rank advances), group-best
option counts, closure-table churn.

The 41 LOSS rows ARE consumed into the canonical cache by the Part AS
fail-closed merger (a zero-WIN partial-packet adoption); the only
canonical claim established by this reaudit is the classification delta
itself on the canonical cache: class 23101's unknown cost boundary drops
52 -> 11 (it becomes rank 1 of the closure table WITHOUT closing, since
its WIN child is not consumed and 10 keys remain unprobed).  Never a
19-root or 11x11 result; nodes are bookkeeping only.  The 11x11 empty
board stays UNKNOWN; all 19 central-reply roots stay UNKNOWN.
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
OUT = EXP / "output/decomp-deltas-batch14-adoption.json"

GRAPH =ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_DIR = ROOT / "research/experiments/n11-centralreply-class10687-loss52-adoption-reaudit-20261122/reaudit/output"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class10687-loss52-adoption-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-20261122.cache"
BATCH_DIR = ROOT / "research/experiments/n11-centralreply-closure-class23101-batch14-20261122"
SCEN_OUT = EXP / "reaudit/output"
INCR_CACHE = EXP / "output/increment-batch14-loss41-20261122.cache"
MANIFEST = EXP / "output/increments-manifest.json"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-20261122.cache"

INCR_SHA = "5194af934a5373823a819ec53178dd008d1c6d5b17488101aa742ca1230d0831"
SCEN_CACHE_SHA = "be9cb24e899fbe93db51e415320c50fa733e378748bb7a41fe13fd7b22f06685"
BASE_CACHE_SHA = "342e86838e0c2bef915798059cb397f7c91e59c65426bf74db19530ecdd7979e"
BASE_SUMMARY_SHA = "b278f822627560d7c3945ee0c0aded7de415b6141a69f0f8722e670432fc48da"
SCEN_SUMMARY_SHA = "f2008e70b31f23724d9bd8d605f7ab6f1de20f1802e65bd5b955420a2f50a744"
BASE_CLOSURE_SHA = "7405699e183acea509e71e58dfc7c15904c675dff0b04518201484e72185041b"
BASE_PRC_SHA = "ec52a56d6b6e7af6401698d59ec9f07e0628e02059240ff63f84913df09caa37"
BATCH_KEYS_SHA = "dfde0e90b75fd261b51ef746fe69a16eb182a99f5d2f8e1ff8bfa6efe936d71f"

SCENARIO = "ADOPTED-CANONICAL"
BATCH_CLASS = 23101
UNADOPTED_WIN_ID = "q042"
UNADOPTED_WIN_S5 = 745184
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
                          ("base closure-classes", BASE_DIR / "closure-classes.csv", BASE_CLOSURE_SHA),
                          ("base per-root-coverage", BASE_DIR / "per-root-coverage.csv", BASE_PRC_SHA),
                          ("batch-keys", BATCH_DIR / "input/batch-keys.json", BATCH_KEYS_SHA)):
        got = sha(p)
        if got != want:
            fail(f"{name} sha256 drift: {got} != {want}")

    manifest = json.loads(MANIFEST.read_text())
    rc = manifest["row_counts"]
    if not (rc["resolved_rows"] == 41 and rc["losses"] == 41 and rc["wins"] == 0
            and rc["exhausted_excluded"] == 0 and rc["probed_total"] == 52
            and rc["probed_resolved"] == 42):
        fail(f"manifest row_counts not 41 LOSS / 0 adopted WIN / 0 exhausted of 42 resolved: {rc}")
    if manifest["win_ids"] != [] or manifest["exhausted_excluded_ids"] != []:
        fail(f"manifest win/exhaustion id lists not empty: {manifest}")
    if manifest["unadopted_win_ids"] != [UNADOPTED_WIN_ID] or manifest["unadopted_win_s5_index"] != UNADOPTED_WIN_S5:
        fail(f"manifest unadopted WIN bookkeeping not q042/{UNADOPTED_WIN_S5}: {manifest}")
    if manifest["full_packet_eq_loss_only"] is not False or manifest["win_scenario_exists"] is not True:
        fail("manifest full!=loss / win-scenario bookkeeping not asserted")
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
        fail("batch-14 keys collide on s5 indices")

    incr = read_cache(INCR_CACHE)
    if len(incr) != 41:
        fail(f"increment row count {len(incr)} != 41")
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
        fail("increment key set not contained in the batch-14 key set")
    adopted_loss_ids = sorted(kid for kid, (lo, hi, _s, _m) in batch_keys.items()
                              if (lo, hi) in incr)
    if [f"q{i:03d}" for i in range(1, 42)] != adopted_loss_ids:
        fail(f"adopted LOSS ids {adopted_loss_ids[:5]}... != q001..q041")

    # --- the unadopted WIN row q042: verifier-level non-consumption gates -----
    win_lo, win_hi, win_s5i, _m = batch_keys[UNADOPTED_WIN_ID]
    if win_s5i != UNADOPTED_WIN_S5:
        fail(f"batch-keys q042 s5 index {win_s5i} != published {UNADOPTED_WIN_S5}")
    base_cache = read_cache(BASE_CACHE)
    scen_cache = read_cache(SCEN_CACHE)
    for name, tab in (("increment", incr), ("BASE", base_cache), ("scenario", scen_cache)):
        if (win_lo, win_hi) in tab:
            fail(f"q042 WIN key present in {name} (verdict would be consumed)")
    if (win_lo, win_hi) in quarantined:
        fail("q042 WIN key quarantined")
    # q042's raw published two-pass WIN result (honest re-verification label)
    # replay row: replay,id,stones,legal,is_or,budget,result,nodes,wall_s,key_lo,key_hi
    win_raw = None
    for tag in ("p1", "p2"):
        p = BATCH_DIR / f"output/raw/{UNADOPTED_WIN_ID}.{tag}.out"
        for line in p.read_text().splitlines():
            if not line.startswith("replay,"):
                continue
            parts = line.split(",")
            row = (int(parts[2]), int(parts[3]), int(parts[5]),
                   int(parts[6]), int(parts[7]), int(parts[9]), int(parts[10]))
            if win_raw is None:
                win_raw = row
            elif win_raw != row:
                fail(f"q042 pass mismatch {tag}: {row} vs {win_raw}")
    if win_raw is None or win_raw[0] != 5 or win_raw[3] != 1:
        fail(f"q042 published raw is not a 5-stone WIN: {win_raw}")
    if win_raw[2] != int(bk["budget"]):
        fail(f"q042 raw budget {win_raw[2]} != batch-keys budget {bk['budget']}")
    if (win_raw[5], win_raw[6]) != (win_lo, win_hi):
        fail("q042 raw key != batch-keys key")

    for kid, (lo, hi, s5i, _m) in batch_keys.items():
        if (lo, hi) in base_cache:
            fail(f"{kid} already present in the BASE cache (not a fresh increment)")
        if s5i in receipt_verdicts:
            fail(f"{kid} already resolved by the update8 receipt")
    if len(scen_cache) != len(base_cache) + 41:
        fail("scenario cache row count != BASE + 41")
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
    if scen_votes.get(1, 0) != 158 or scen_votes.get(2, 0) != 5962:
        fail(f"scenario cache verdict counts not 158 WIN / 5962 LOSS: {dict(sorted(scen_votes.items()))}")

    # --- graph holders of the 41 keys ---------------------------------------
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
        fail("class 23101 must NOT free under a loss-only partial adoption "
             "(its WIN child and 10 unprobed keys stay unknown)")
    base23101 = sorted(base_unknown[BATCH_CLASS])
    if len(base23101) != 52:
        fail(f"class 23101 BASE-unknown cost children {len(base23101)} != 52")
    if not set(incr_index) <= set(base23101):
        fail("increment s5 indices are not all BASE-unknown cost children of class 23101")
    leftover23101 = sorted(set(base23101) - set(incr_index))
    if leftover23101 != sorted(scen_unknown[BATCH_CLASS]) or len(leftover23101) != 11:
        fail(f"class 23101 scenario-unknown children {sorted(scen_unknown[BATCH_CLASS])} "
             f"!= the 11 leftover BASE-unknown children {leftover23101}")
    if UNADOPTED_WIN_S5 not in leftover23101:
        fail("q042 s5 index is not among class 23101's scenario-unknown cost children "
             "(WIN verdict would have been consumed)")
    batch_s5 = {v[2] for v in batch_keys.values()}
    if batch_s5 != set(base23101):
        fail(f"batch-14 key set != the 52 BASE-unknown cost children of class 23101 "
             f"(batch-only {sorted(batch_s5 - set(base23101))[:5]}, "
             f"base-only {sorted(set(base23101) - batch_s5)[:5]})")
    if base_iv.get(UNADOPTED_WIN_S5) is not None or _scen_iv.get(UNADOPTED_WIN_S5) is not None:
        fail("q042 s5 index resolved in BASE or scenario index_verdict (verdict consumed)")

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
    # 41 adopted rows' graph memberships (each key's holder count from batch-keys
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
    b23101 = [r for r in base_cc if int(r["class_index"]) == BATCH_CLASS]
    if len(b23101) != 1:
        fail(f"class 23101 appears {len(b23101)} times in the BASE closure-candidate table")
    if int(b23101[0]["unknown_now"]) != 52:
        fail(f"BASE closure row for 23101 unknown_now {b23101[0]['unknown_now']} != 52")
    s23101 = [r for r in scen_cc if int(r["class_index"]) == BATCH_CLASS]
    if len(s23101) != 1:
        fail("class 23101 missing from (or duplicated in) the scenario closure-candidate "
             "table: a loss-only partial adoption can neither close nor exclude it")
    if int(s23101[0]["unknown_now"]) != 11:
        fail(f"scenario closure row for 23101 unknown_now {s23101[0]['unknown_now']} != 11")
    base_idx = {int(r["class_index"]) for r in base_cc}
    scen_idx = {int(r["class_index"]) for r in scen_cc}
    closure_rows = {
        "base_class_23101_rank": int(b23101[0]["class_rank"]),
        "scenario_class_23101_rank": int(s23101[0]["class_rank"]),
        "base_rank14_row": next((r for r in base_cc if r["class_rank"] == "14"), None),
        "scenario_rank14_row": next((r for r in scen_cc if r["class_rank"] == "14"), None),
        "scenario_first_row": scen_cc[0] if scen_cc else None,
        "scenario_class_10661_row": next((r for r in scen_cc if int(r["class_index"]) == 10661), None),
        "left_table_classes": sorted(base_idx - scen_idx),
        "entered_table_classes": sorted(scen_idx - base_idx),
    }

    # --- output --------------------------------------------------------------
    out = {
        "schema": "n11-batch14-adoption-decomp-deltas-v1",
        "scenario": ("ADOPTED-CANONICAL = pre-adoption BASE (canonical 6,079 rows, Part AP "
                     "reaudit state) + the 41 LOSS rows of batch-14 (class 23101); "
                     "full!=loss: the q042 WIN row is NOT adopted and its verdict is NOT "
                     "consumed (2-pass re-verified here and machine-excluded)"),
        "interpretation_guard": ("canonical adoption deltas: the 41 LOSS rows of batch-14 "
                                 "are consumed into the canonical cache via the fail-closed "
                                 "union merger; scheduling quantities are bookkeeping; "
                                 "class 23101 stays UNKNOWN-status (an unknown class with "
                                 "11 remaining unknown cost children: the unconsumed WIN "
                                 "child q042 + 10 unprobed keys) and neither closes nor "
                                 "excludes; 11x11 empty board and all 19 roots stay "
                                 "UNKNOWN; nodes are bookkeeping"),
        "recompute_gates": ("class statuses with Board free-candidate child verification, "
                            "known-universe counts and per-root free coverage were "
                            "recomputed from graph + update8 + cache and asserted equal "
                            "to the published BASE (Part AP reaudit) and scenario "
                            "outputs before any delta was emitted"),
        "pins": {
            "increment_sha256": INCR_SHA,
            "scenario_cache_sha256": SCEN_CACHE_SHA,
            "base_cache_sha256": BASE_CACHE_SHA,
            "base_summary_sha256": BASE_SUMMARY_SHA,
            "scenario_summary_sha256": SCEN_SUMMARY_SHA,
            "base_closure_classes_sha256": BASE_CLOSURE_SHA,
            "base_per_root_coverage_sha256": BASE_PRC_SHA,
            "batch_keys_sha256": BATCH_KEYS_SHA,
        },
        "batch_keys": {
            "count": 52, "adopted_loss": 41, "unadopted_win": 1,
            "unadopted_win_id": UNADOPTED_WIN_ID,
            "unadopted_win_s5_index": UNADOPTED_WIN_S5,
            "unadopted_win_raw_2pass": {"stones": win_raw[0], "legal": win_raw[1],
                                        "budget": win_raw[2], "result": win_raw[3],
                                        "nodes": win_raw[4],
                                        "key": [win_lo, win_hi]},
            "batch_class": BATCH_CLASS,
            "class_mask": list(s4_masks[BATCH_CLASS]),
            "cost_children_total": len(s4_cost[BATCH_CLASS]),
            "batch_groups_served": [list(x) for x in batch_groups_served],
        },
        "excluded_now_flips": flips,
        "newly_free_now_classes": new_free,
        "newly_free_now_gate": ("each newly free class was BASE-unknown and every "
                                "BASE-unknown cost child is resolved by the increment; "
                                "a zero-WIN partial packet can only free, never flip; "
                                "class 23101 itself is gated NOT free (11 children stay "
                                "unknown)"),
        "status_transitions": dict(sorted(transitions.items())),
        "class_23101": {
            "base_unknown_children": len(base_unknown[BATCH_CLASS]),
            "adopted_by_increment": len(incr_index),
            "scenario_unknown_children": len(scen_unknown[BATCH_CLASS]),
            "scenario_unknown_indices": sorted(scen_unknown[BATCH_CLASS]),
            "contains_unconsumed_win_child": UNADOPTED_WIN_S5 in scen_unknown[BATCH_CLASS],
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
    print("OK decomp-deltas-batch14-adoption.json: "
          f"flips={flips} new_free={new_free} "
          f"free_now {metrics['free_now_classes']['base']}->{metrics['free_now_classes']['scenario']} "
          f"class23101_unknown {len(base_unknown[BATCH_CLASS])}->{len(scen_unknown[BATCH_CLASS])} "
          f"update8_resolved +{len(newly_resolved)} "
          f"joint_greedy {metrics['joint_greedy_union_size']['base']}->{metrics['joint_greedy_union_size']['scenario']} "
          f"worklist {metrics['probe_worklist_total']['base']}->{metrics['probe_worklist_total']['scenario']} "
          f"changed_rows={sorted(changed_rows)}")


if __name__ == "__main__":
    main()
