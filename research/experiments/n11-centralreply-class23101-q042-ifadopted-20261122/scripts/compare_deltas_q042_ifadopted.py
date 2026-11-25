#!/usr/bin/env python3
"""q042 single-WIN if-adopted delta extractor (Part AT, 2026-11-22).

Fail-closed, read-only audit executing the single-owner Part AT
declaration (note amendment, declaration commit 58938933, observed
HEAD-before-push 2f88a495).  Compares the published BASE refresh outputs
(the Part AS canonical reaudit on the 6,120-row canonical cache
be9cb24e..., scenario = the canonical classification) against the single
if-adopted computation:

  IF-ADOPTED = canonical 6,120 rows + the single q042 WIN row
  (s5_index 745184, key [1152921505747697664, 1032], result 1,
  9,149,084 nodes) of batch-14 (class 23101)

This is a projection for the scrutiny owner's adoption-decision
precomputation (k04 / b018 / d002 / e002 / r001 / r002 precedent).  The WIN
verdict is NOT consumed anywhere by this Part: the canonical cache stays
byte-identical (machine-asserted against the published BASE sha), and the
if-adopted cache is NOT the repo canonical chain.  This Part neither
recommends nor rejects adoption.

Gates (all fail-closed):
  * sha256 pins: increment, if-adopted cache, canonical BASE cache, BASE
    summary, scenario summary, BASE closure-classes.csv, BASE
    per-root-coverage.csv, batch-keys,
  * manifest: 1 row / 1 WIN / 0 LOSS, ifadopted_only, canonical cache
    pinned untouched,
  * the q042 row is re-verified from BOTH published batch-14 raw passes
    (2-pass node-exact result 1, 9,149,084 nodes), keyed to batch-keys
    (s5 index 745184, legal 85), absent from the BASE cache and the
    quarantine registry, canonical-safe, and adopted exactly once into the
    if-adopted cache,
  * if-adopted cache == BASE rows + the single WIN row with verdict
    agreement on every shared row;
  * every recomputed status transition is one of
    excluded->excluded, excluded_now->excluded_now, free_now->free_now,
    unknown->{unknown, free_now, excluded_now},
  * flips (newly excluded_now) == exactly the machine-computed set of
    BASE-unknown graph holder classes of s5 745184 (computed, not
    hardcoded), each transitioning unknown->excluded_now;
  * no excluded_now regression, no newly free class (a WIN adoption can
    only flip classes to excluded_now, never free one - gated),
  * class 23101 IS among the flips (it holds 745184 as a cost child) and
    its scenario-unknown children are exactly the 10 unprobed batch-14
    keys (the consumed WIN child is gone from the unknown boundary),
  * update8: no resolution lost, newly-resolved set and win_hit_groups
    deltas machine-recomputed against the published receipts,
  * per-root coverage recomputed from the graph matches the published
    per-root-coverage.csv for BASE and scenario; root 27 stays 119/119;
    a pure WIN adoption must not move any per-root free/uncovered count
    or create a newly free third (gated),
  * canonical cache byte-pinned untouched (be9cb24e..., 6,120 rows).

Measured (recorded, not gated, scheduling quantities only): whether class
23101 stays in the closure-candidate/probing table view (with its 10
unknown children it remains a probing target there; the flip itself is
recorded by class_status_counts and the transitions ledger), per-root and
joint greedy sizes, probe worklist size, closure-table churn, class 10661
rank position.

Interpretation guard: the IF-ADOPTED projection shows the scrutiny owner
what adopting q042 would do to the classification ledger: the holder
classes of s5 745184 flip to excluded_now (a one-way door - the all-LOSS
closure route of every flipped class is permanently refuted by a verified
WIN child).  It is NOT a verdict consumption, NOT a closure claim, NOT a
19-root or 11x11 result, and neither an adoption recommendation nor a
rejection.  The standard 11x11 empty board, the 19 central-reply roots and
every class stay UNKNOWN; nodes are bookkeeping, never verdicts.
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
OUT = EXP / "output/decomp-deltas-q042-ifadopted.json"

GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_DIR = ROOT / "research/experiments/n11-centralreply-class23101-loss41-adoption-reaudit-20261122/reaudit/output"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class23101-loss41-adoption-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-20261122.cache"
BATCH_DIR = ROOT / "research/experiments/n11-centralreply-closure-class23101-batch14-20261122"
SCEN_OUT = EXP / "reaudit/output"
INCR_CACHE = EXP / "output/increment-q042-win-ifadopted-20261122.cache"
MANIFEST = EXP / "output/increment-manifest.json"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-q042win-IFADOPTED-20261122.cache"

INCR_SHA = "b4958328270f11b24d3a638e1099a0c6047dbebb242e3116217b0473ef63f9b6"
SCEN_CACHE_SHA = "1434c68bc572a9817eca9c9a4ab442005762339cf539f22cb3acb0b24bc5ffd1"
BASE_CACHE_SHA = "be9cb24e899fbe93db51e415320c50fa733e378748bb7a41fe13fd7b22f06685"
BASE_SUMMARY_SHA = "f2008e70b31f23724d9bd8d605f7ab6f1de20f1802e65bd5b955420a2f50a744"
SCEN_SUMMARY_SHA = "029cc3b6daa23ff4bccea66597a93484c1a241ac23b2656f2e4f1bf344e66d5a"
BASE_CLOSURE_SHA = "3ee1dbb6db7a5fc8858f5bbdd5cae7ca754589f376ebb99727535806f917bc9e"
BASE_PRC_SHA = "527c7e9a3f6350f638b5e2e2a70c3115e50533eeca651e38e32329a04ab225d4"
BATCH_KEYS_SHA = "dfde0e90b75fd261b51ef746fe69a16eb182a99f5d2f8e1ff8bfa6efe936d71f"
MANIFEST_SHA = "894e9420b043e12543920bb63c49f00530e45ad5b29c95c65e3dadf3047fc02e"

SCENARIO = "IF-ADOPTED"
WIN_ID = "q042"
WIN_S5 = 745184
WIN_LO = 1152921505747697664
WIN_HI = 1032
WIN_NODES = 9149084
BATCH_CLASS = 23101
UNIVERSE_SIZE = 31859
RECEIPT_COUNT = 23
ALLOWED_TRANSITIONS = {"excluded": ["excluded"], "excluded_now": ["excluded_now"],
                       "free_now": ["free_now"],
                       "unknown": ["unknown", "free_now", "excluded_now"]}


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
    for name, p, want in (("increment", INCR_CACHE, INCR_SHA),
                          ("if-adopted cache", SCEN_CACHE, SCEN_CACHE_SHA),
                          ("canonical BASE cache", BASE_CACHE, BASE_CACHE_SHA),
                          ("manifest", MANIFEST, MANIFEST_SHA),
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
    if not (rc["rows"] == 1 and rc["wins"] == 1 and rc["losses"] == 0):
        fail(f"manifest row_counts not a single WIN row: {rc}")
    if manifest["win_ids"] != [WIN_ID] or manifest["win_s5_index"] != WIN_S5:
        fail(f"manifest win bookkeeping not q042/{WIN_S5}: {manifest}")
    if manifest["ifadopted_only"] is not True:
        fail("manifest ifadopted_only not asserted")
    if manifest["canonical_cache_untouched"] != BASE_CACHE_SHA:
        fail("manifest canonical pin does not match the published BASE sha")
    if manifest["sha256"]["win"] != INCR_SHA:
        fail("manifest win sha does not match the pinned increment")

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
    if [int(x) for x in bk["class_mask"]] != list(s4_masks[BATCH_CLASS]):
        fail("batch-keys class_mask != graph mask of the batch class")
    win_key_row = [k for k in bk["keys"] if k["key_id"] == WIN_ID]
    if len(win_key_row) != 1:
        fail(f"{WIN_ID} not unique in batch-keys")
    wk = win_key_row[0]
    if (int(wk["s5_index"]) != WIN_S5 or int(wk["lo"]) != WIN_LO
            or int(wk["hi"]) != WIN_HI):
        fail(f"batch-keys {WIN_ID} disagreement: {wk}")

    incr = read_cache(INCR_CACHE)
    if len(incr) != 1 or (WIN_LO, WIN_HI) not in incr:
        fail("increment is not exactly the single q042 row")
    if incr[(WIN_LO, WIN_HI)] != (1, WIN_NODES):
        fail(f"increment q042 row {incr[(WIN_LO, WIN_HI)]} != (WIN, {WIN_NODES})")
    if (WIN_LO, WIN_HI) in quarantined or not is_canonical_safe_s5_key((WIN_LO, WIN_HI)):
        fail("q042 key quarantined or noncanonical")
    if mask_to_index.get((WIN_LO, WIN_HI)) != WIN_S5:
        fail("q042 key does not map to its published s5 index")

    # --- 2-pass raw re-verification ------------------------------------------
    win_raw = None
    for tag in ("p1", "p2"):
        p = BATCH_DIR / f"output/raw/{WIN_ID}.{tag}.out"
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
    if (win_raw is None or win_raw[0] != 5 or win_raw[3] != 1
            or win_raw[4] != WIN_NODES):
        fail(f"q042 published raw is not the 2-pass WIN: {win_raw}")
    if (win_raw[5], win_raw[6]) != (WIN_LO, WIN_HI):
        fail("q042 raw key != batch-keys key")

    # --- caches ---------------------------------------------------------------
    base_cache = read_cache(BASE_CACHE)
    scen_cache = read_cache(SCEN_CACHE)
    if len(base_cache) != 6120:
        fail(f"BASE cache rows {len(base_cache)} != 6120")
    if (WIN_LO, WIN_HI) in base_cache:
        fail("q042 already present in the canonical BASE cache (would not be if-adopted)")
    if scen_cache.get((WIN_LO, WIN_HI)) != (1, WIN_NODES):
        fail("scenario cache does not adopt exactly the q042 WIN row")
    if len(scen_cache) != len(base_cache) + 1:
        fail("scenario cache row count != BASE + 1")
    for key, (v, _n) in scen_cache.items():
        b = base_cache.get(key)
        if b is None:
            if key != (WIN_LO, WIN_HI):
                fail(f"scenario-only row outside the increment: {key}")
        elif b[0] != v:
            fail(f"scenario verdict drift on shared key {key}")
    base_votes = Counter(v for v, _ in base_cache.values())
    scen_votes = Counter(v for v, _ in scen_cache.values())
    if base_votes.get(1, 0) != 158 or scen_votes.get(1, 0) != 159:
        fail("WIN counts not 158 -> 159")
    if scen_votes.get(2, 0) != 5962:
        fail("scenario LOSS count != 5,962")
    for key in scen_cache:
        if key in quarantined:
            fail(f"quarantined key inside scenario cache: {key}")
        if not is_canonical_safe_s5_key(key):
            fail(f"noncanonical scenario key {key}")

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
            fail(f"{name}: recomputed known universe {len(iv)} != published")
        if pub_in["cache_rows_in_universe"] != iu:
            fail(f"{name}: recomputed cache rows in universe {iu} != published")
    if base_iv.get(WIN_S5) is not None:
        fail("q042 s5 index resolved in BASE (WIN would be consumed on main)")

    # --- transitions + flips ---------------------------------------------------
    transitions = Counter()
    for i in range(len(s4_masks)):
        b, s = base_st[i], scen_st[i]
        transitions[f"{b}->{s}"] += 1
        if s not in ALLOWED_TRANSITIONS.get(b, []):
            fail(f"class {i} forbidden transition {b} -> {s}")
    base_excluded_now = {i for i, s in base_st.items() if s == "excluded_now"}
    flips = sorted(i for i, s in scen_st.items()
                   if s == "excluded_now" and i not in base_excluded_now)
    flipped_out = sorted(i for i, s in scen_st.items()
                         if s != "excluded_now" and i in base_excluded_now)
    if flipped_out:
        fail(f"excluded_now regressions {flipped_out} must be EMPTY")
    win_holders = sorted(i for i in range(len(s4_masks)) if WIN_S5 in s4_cost[i])
    expected_flips = sorted(i for i in win_holders if base_st[i] == "unknown")
    if flips != expected_flips:
        fail(f"flips {flips} != machine-computed unknown holders of s5 {WIN_S5} {expected_flips}")
    if len(flips) != len(win_holders) and any(base_st[i] != "unknown" for i in win_holders):
        # some holders were already excluded_now/free at BASE - record but only
        # unknown holders may flip (already fails above if sets differ)
        pass
    if BATCH_CLASS not in flips:
        fail("class 23101 (holder of s5 745184) not among the flips")
    for i in flips:
        if base_st[i] != "unknown" or scen_st[i] != "excluded_now":
            fail(f"flip class {i} is not unknown->excluded_now")
    new_free = sorted(i for i, s in scen_st.items() if s == "free_now" and base_st[i] != "free_now")
    if new_free:
        fail(f"a WIN adoption created newly free classes {new_free} (must be impossible)")

    # --- class 23101 scenario unknowns ----------------------------------------
    scen23101 = sorted(scen_unknown[BATCH_CLASS])
    if len(scen23101) != 10:
        fail(f"class 23101 scenario-unknown children {scen23101} != the 10 unprobed keys")
    if WIN_S5 in scen23101:
        fail("consumed WIN child still in class 23101's scenario unknown boundary")
    if sorted(set(base_unknown[BATCH_CLASS]) - {WIN_S5}) != scen23101:
        fail("scenario-unknown children of 23101 != BASE-unknown minus q042 (machine mismatch)")

    # --- holder rows ------------------------------------------------------------
    holder_rows = {}
    for c in win_holders:
        holder_rows[str(c)] = {
            "base_status": base_st[c],
            "base_unknown_now": len(base_unknown[c]),
            "holds_win_child": WIN_S5 in base_unknown[c],
            "scenario_status": scen_st[c],
            "scenario_unknown_now": len(scen_unknown[c]),
        }

    # --- metric table -------------------------------------------------------------
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

    if metrics["excluded_now_classes"]["scenario"] != 23 + len(flips):
        fail("excluded_now arithmetic inconsistent with the flip count")
    if metrics["unknown_classes"]["scenario"] != 34500 - len(flips):
        fail("unknown arithmetic inconsistent with the flip count")

    # --- update8 ---------------------------------------------------------------
    base_resolved = set(base_summary["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    scen_resolved = set(scen_summary["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    lost = sorted(base_resolved - scen_resolved)
    if lost:
        fail(f"update8 resolutions lost: {lost}")
    newly_resolved = sorted(scen_resolved - base_resolved)
    if newly_resolved not in ([], [WIN_S5]):
        fail(f"update8 newly-resolved {newly_resolved} outside the projection universe")
    if len(newly_resolved) != metrics["update8_resolved_count"]["delta"]:
        fail("update8 resolved-count arithmetic inconsistent")

    # --- per-root coverage --------------------------------------------------------
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
    if set(base_prc) != set(scen_prc) or len(base_prc) != len(roots):
        fail("per-root row set changed or count mismatch")
    for prc, by_root, by_third, name in ((base_prc, base_by_root, base_by_third, "BASE"),
                                         (scen_prc, scen_by_root, scen_by_third, SCENARIO)):
        for (role, first), (thirds, free, uncov, _ig) in prc.items():
            rr, rt, rf = by_root[first]
            if rr != role or rt != thirds or rf != free:
                fail(f"{name}: recomputed root {first} ({rr},{rt},{rf}) != "
                     f"published ({role},{thirds},{free})")
    for name, pub in published.items():
        r0 = pub["roots"][0]
        if (r0["role"], r0["origin_first"], r0["thirds"], r0["free_thirds_now"], r0["uncovered"]) \
                != ("known-loss-baseline", 27, 119, 119, 0):
            fail(f"{name}: roots[0] not the 119/119 known-loss baseline")
    newly_free_thirds = [{"first": f, "third": t}
                         for (f, t), base_free in sorted(base_by_third.items())
                         if not base_free and scen_by_third[(f, t)]]
    if newly_free_thirds:
        fail(f"a WIN adoption created newly free thirds {newly_free_thirds} (must be impossible)")
    changed_rows = {}
    for (role, first), (thirds, bfree, buncov, big) in base_prc.items():
        sthirds, sfree, suncov, sig = scen_prc[(role, first)]
        if (bfree, buncov) != (sfree, suncov):
            fail(f"root {first}: per-root free/uncovered moved under a pure WIN "
                 f"adoption ({bfree},{buncov})->({sfree},{suncov}) - impossible")
        del sthirds
    prg_base = base_summary["per_root_greedy"]
    prg_scen = scen_summary["per_root_greedy"]
    per_root_greedy_movers = {}
    for first in sorted(prg_base, key=lambda x: int(x)):
        b, s = prg_base[first], prg_scen[first]
        per_root_greedy_movers[first] = {
            "base_greedy_union_size": b["greedy_union_size"],
            "scenario_greedy_union_size": s["greedy_union_size"],
            "delta": s["greedy_union_size"] - b["greedy_union_size"],
            "free_thirds": [b["free_thirds"], s["free_thirds"]],
            "uncovered_thirds": [b["uncovered_thirds"], s["uncovered_thirds"]],
        }

    # --- closure table observations --------------------------------------------
    def load_closure(path):
        with Path(path).open() as fh:
            return list(csv.DictReader(fh))

    base_cc = load_closure(BASE_DIR / "closure-classes.csv")
    scen_cc = load_closure(SCEN_OUT / "closure-classes.csv")
    s23101 = [r for r in scen_cc if int(r["class_index"]) == BATCH_CLASS]
    if len(s23101) != 1:
        fail("class 23101 not exactly once in the scenario closure-candidate table")
    if int(s23101[0]["unknown_now"]) != 10:
        fail(f"scenario closure row for 23101 unknown_now {s23101[0]['unknown_now']} != 10")
    base_idx = {int(r["class_index"]) for r in base_cc}
    scen_idx = {int(r["class_index"]) for r in scen_cc}
    closure_rows = {
        "scenario_class_23101_rank": int(s23101[0]["class_rank"]),
        "scenario_class_23101_unknown_now": int(s23101[0]["unknown_now"]),
        "scenario_class_10661_row": next((r for r in scen_cc if int(r["class_index"]) == 10661), None),
        "scenario_first_row": scen_cc[0] if scen_cc else None,
        "left_table_classes": sorted(base_idx - scen_idx),
        "entered_table_classes": sorted(scen_idx - base_idx),
        "flipped_classes_in_table": sorted(set(flips) & scen_idx),
        "note": ("the closure-candidate table is a probing-worklist view keyed to "
                 "unknown cost children; the win-flip of class 23101 and the other "
                 "holders is recorded by class_status_counts and the transitions "
                 "ledger, not by this table"),
    }

    out = {
        "schema": "n11-q042-ifadopted-decomp-deltas-v1",
        "scenario": ("IF-ADOPTED = canonical 6,120 rows (be9cb24e..., Part AS) + "
                     "the single batch-14 q042 WIN row (s5 745184, 9,149,084 nodes, "
                     "2-pass re-verified here); a scrutiny-owner precomputation "
                     "projection, NOT the canonical chain"),
        "interpretation_guard": ("if-adopted projection deltas only: the WIN "
                                 "verdict is NOT consumed, the canonical cache is "
                                 "byte-pinned untouched, the holder classes of s5 "
                                 "745184 flip to excluded_now (one-way: their "
                                 "all-LOSS closure routes are permanently refuted "
                                 "by the verified WIN child); no coverage change; "
                                 "this Part neither recommends nor rejects adoption; "
                                 "11x11 empty board and all 19 roots stay UNKNOWN; "
                                 "nodes are bookkeeping"),
        "recompute_gates": ("class statuses with Board free-candidate child "
                            "verification, known-universe counts and per-root free "
                            "coverage were recomputed from graph + update8 + cache "
                            "and asserted equal to the published BASE (Part AS "
                            "reaudit) and if-adopted outputs before any delta was "
                            "emitted"),
        "pins": {
            "increment_sha256": INCR_SHA,
            "ifadopted_cache_sha256": SCEN_CACHE_SHA,
            "canonical_base_cache_sha256": BASE_CACHE_SHA,
            "manifest_sha256": MANIFEST_SHA,
            "base_summary_sha256": BASE_SUMMARY_SHA,
            "ifadopted_summary_sha256": SCEN_SUMMARY_SHA,
            "base_closure_classes_sha256": BASE_CLOSURE_SHA,
            "base_per_root_coverage_sha256": BASE_PRC_SHA,
            "batch_keys_sha256": BATCH_KEYS_SHA,
        },
        "win_row": {
            "key_id": WIN_ID, "s5_index": WIN_S5, "key": [WIN_LO, WIN_HI],
            "result": 1, "nodes": WIN_NODES,
            "raw_2pass": {"stones": win_raw[0], "legal": win_raw[1],
                          "budget": win_raw[2], "result": win_raw[3],
                          "nodes": win_raw[4]},
        },
        "flips_excluded_now": flips,
        "flips_gate": ("flips == the machine-computed BASE-unknown graph holder "
                       "classes of s5 745184 (computed from the pinned graph cost "
                       "sets, not hardcoded); each transitions unknown -> "
                       "excluded_now; no regression; a WIN adoption can never free "
                       "a class or move per-root coverage (all gated)"),
        "status_transitions": dict(sorted(transitions.items())),
        "newly_free_now_classes": new_free,
        "class_23101": {
            "base_status": base_st[BATCH_CLASS],
            "scenario_status": scen_st[BATCH_CLASS],
            "base_unknown_children": len(base_unknown[BATCH_CLASS]),
            "scenario_unknown_children": len(scen_unknown[BATCH_CLASS]),
            "scenario_unknown_indices": sorted(scen_unknown[BATCH_CLASS]),
        },
        "win_holders": holder_rows,
        "update8": {
            "newly_resolved_s5": newly_resolved,
            "lost_resolved": lost,
            "win_hit_groups_base": base_summary["frozen_update8_refresh"]["win_hit_groups"],
            "win_hit_groups_scenario": scen_summary["frozen_update8_refresh"]["win_hit_groups"],
        },
        "newly_free_thirds": newly_free_thirds,
        "changed_per_root_coverage_rows": {},
        "per_root_greedy": per_root_greedy_movers,
        "metrics": metrics,
        "closure_candidate_rows": closure_rows,
    }
    OUT.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("OK decomp-deltas-q042-ifadopted.json: "
          f"flips={flips} new_free={new_free} "
          f"excluded_now {metrics['excluded_now_classes']['base']}->{metrics['excluded_now_classes']['scenario']} "
          f"class23101 unknown {len(base_unknown[BATCH_CLASS])}->{len(scen_unknown[BATCH_CLASS])} "
          f"free_now {metrics['free_now_classes']['base']}->{metrics['free_now_classes']['scenario']} "
          f"update8_resolved +{len(newly_resolved)} "
          f"joint_greedy {metrics['joint_greedy_union_size']['base']}->{metrics['joint_greedy_union_size']['scenario']} "
          f"worklist {metrics['probe_worklist_total']['base']}->{metrics['probe_worklist_total']['scenario']}")


if __name__ == "__main__":
    main()
