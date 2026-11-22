#!/usr/bin/env python3
"""v001/v002 two-WIN if-adopted delta extractor (Part BA, 2026-11-22).

Fail-closed, read-only audit executing the two-owner Part BA
declaration (note amendment, declaration commit 607c876a, observed
HEAD-before-push f8cc6c9d).  Compares the published BASE refresh outputs
(the Part AS canonical reaudit on the 6,120-row canonical cache
be9cb24e..., scenario = the canonical classification) against the two-WIN
if-adopted computation:

  IF-ADOPTED = canonical 6,120 rows + the two batch-18 (class 16131)
  WIN rows:
    v001: key [1154610354467115008, 64], s5 index 153671, result 1,
          5,656,151 nodes (raw legal 83)
    v002: key [3459890413727387648, 64], s5 index 207534, result 1,
          7,898,204 nodes (raw legal 84)

This is a projection for the scrutiny owner's adoption-decision
precomputation (k04 / b018 / d002 / e002 / r001 / r002 / q042
precedent).  The WIN verdicts are NOT consumed anywhere by this Part:
the canonical cache stays byte-identical (machine-asserted against the
published BASE sha), and the if-adopted cache is NOT the repo canonical
chain.  This Part neither recommends nor rejects adoption.

Gates (all fail-closed):
  * sha256 pins: increment, if-adopted cache, canonical BASE cache, BASE
    summary, scenario summary, BASE closure-classes.csv, BASE
    per-root-coverage.csv, batch-keys, increment manifest,
  * manifest: 2 rows / 2 WINs / 0 LOSS, ifadopted_only, class 16131,
    win ids [v001, v002], win s5 indices [153671, 207534], canonical
    cache pinned untouched,
  * both WIN rows are re-verified from BOTH published batch-18 raw
    passes (2-pass node-exact result 1), keyed to batch-keys
    (s5 index, lo/hi, raw legal == batch-keys legal), absent from the
    BASE cache and the quarantine registry, canonical-safe, and adopted
    exactly once each into the if-adopted cache,
  * if-adopted cache == BASE rows + the two WIN rows (row count
    base+2, no verdict drift on shared rows, scenario-only rows ==
    the two WIN keys), WIN row counts 158 -> 160, LOSS 5,962,
  * neither WIN s5 index is resolved in the BASE known universe (both
    verdicts stay unconsumed on main),
  * every recomputed status transition is one of
    excluded->excluded, excluded_now->excluded_now, free_now->free_now,
    unknown->{unknown, free_now, excluded_now},
  * flips (newly excluded_now) == exactly the machine-computed set of
    BASE-unknown graph holder classes of s5 153671 or s5 207534
    (per-WIN holder sets, union and double holders computed from the
    pinned graph cost sets, never hardcoded); each transition is
    unknown->excluded_now; no regression,
  * no newly free class (a WIN adoption can only flip classes to
    excluded_now, never free one - gated),
  * class 16131 IS among the flips and its BASE-unknown children are
    exactly the 53 batch-18 key s5 indices (the two consumed WIN
    children are gone from the scenario unknown boundary: 53 -> 51),
  * update8: no resolution lost, newly-resolved set within
    {153671, 207534}, win_hit_groups and groups deltas
    machine-recomputed against the published receipts,
  * per-root coverage recomputed from the graph matches the published
    per-root-coverage.csv for BASE and scenario; root 27 stays 119/119;
    a pure WIN adoption must not move any per-root free/uncovered count
    or create a newly free third (gated),
  * canonical cache byte-pinned untouched (be9cb24e..., 6,120 rows).

Measured (recorded, not gated, scheduling quantities only): the
closure-candidate table row of class 16131 (rank 15 -> 7 with its 51
remaining unknown children; the flip itself is recorded by
class_status_counts and the transitions ledger), per-root and joint
greedy sizes, probe worklist size, closure-table churn.

Interpretation guard: the IF-ADOPTED projection shows the scrutiny owner
what adopting v001+v002 together would do to the classification ledger:
the holder classes of s5 153671 / s5 207534 flip to excluded_now (a
one-way door - the all-LOSS closure route of every flipped class is
permanently refuted by a verified WIN child).  It is NOT a verdict
consumption, NOT a closure claim, NOT a 19-root or 11x11 result, and
neither an adoption recommendation nor a rejection.  The standard 11x11
empty board, the 19 central-reply roots and every class stay UNKNOWN;
nodes are bookkeeping, never verdicts.
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
OUT = EXP / "output/decomp-deltas-v001v002-ifadopted.json"

GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_DIR = ROOT / "research/experiments/n11-centralreply-class23101-loss41-adoption-reaudit-20261122/reaudit/output"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class23101-loss41-adoption-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-20261122.cache"
BATCH_DIR = ROOT / "research/experiments/n11-centralreply-closure-class16131-batch18-20261122"
SCEN_OUT = EXP / "reaudit/output"
INCR_CACHE = EXP / "output/increment-b18win-v001v002-ifadopted-20261122.cache"
MANIFEST = EXP / "output/increment-manifest.json"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-b18win-v001v002-IFADOPTED-20261122.cache"

INCR_SHA = "4f8fc29bfd00492aa9a983f20a121737d395b8f80d53e2b04c271fec068bc1ee"
SCEN_CACHE_SHA = "6bfa9faa1dec17cfb827a50668e84f289ffcc7dcb115591fc3280293b1f0f0b6"
BASE_CACHE_SHA = "be9cb24e899fbe93db51e415320c50fa733e378748bb7a41fe13fd7b22f06685"
BASE_SUMMARY_SHA = "f2008e70b31f23724d9bd8d605f7ab6f1de20f1802e65bd5b955420a2f50a744"
SCEN_SUMMARY_SHA = "af95270b5cc3c9c6245314a1eb80399aa9db2b7f424816d942f32a517676e2d4"
BASE_CLOSURE_SHA = "3ee1dbb6db7a5fc8858f5bbdd5cae7ca754589f376ebb99727535806f917bc9e"
BASE_PRC_SHA = "527c7e9a3f6350f638b5e2e2a70c3115e50533eeca651e38e32329a04ab225d4"
BATCH_KEYS_SHA = "1bb3ed41b26af92491ed579a7c05471f271ed1394d8b5f817b5110794d926667"
MANIFEST_SHA = "13736030ea484a0496da7f929b9c6892a2e9ebf6522f96d1c87d2c21000945f1"

SCENARIO = "IF-ADOPTED"
WINS = [
    {"id": "v001", "s5": 153671, "lo": 1154610354467115008, "hi": 64,
     "nodes": 5656151, "legal": 83},
    {"id": "v002", "s5": 207534, "lo": 3459890413727387648, "hi": 64,
     "nodes": 7898204, "legal": 84},
]
WIN_IDS = [w["id"] for w in WINS]
WIN_S5S = [w["s5"] for w in WINS]
WIN_KEYS = [(w["lo"], w["hi"]) for w in WINS]
BATCH_CLASS = 16131
BATCH_KEY_COUNT = 53
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
    if not (rc["rows"] == 2 and rc["wins"] == 2 and rc["losses"] == 0):
        fail(f"manifest row_counts not the two WIN rows: {rc}")
    if manifest["win_ids"] != WIN_IDS or manifest["win_s5_index"] != WIN_S5S:
        fail(f"manifest win bookkeeping not v001/v002/{WIN_S5S}: {manifest}")
    if manifest["win_nodes"] != [w["nodes"] for w in WINS]:
        fail("manifest node bookkeeping disagrees with the pinned WIN nodes")
    if [tuple(k) for k in manifest["win_keys"]] != WIN_KEYS:
        fail("manifest win keys disagree with the pinned WIN keys")
    if manifest["ifadopted_only"] is not True:
        fail("manifest ifadopted_only not asserted")
    if int(manifest["class_index"]) != BATCH_CLASS:
        fail("manifest class_index is not 16131")
    if manifest["part"] != "BA":
        fail("manifest part is not BA")
    if manifest["canonical_cache_untouched"] != BASE_CACHE_SHA:
        fail("manifest canonical pin does not match the published BASE sha")
    if manifest["sha256"]["win"] != INCR_SHA:
        fail("manifest win sha does not match the pinned increment")
    if manifest["raw_publication_commit"] != "938e34f2":
        fail("manifest raw publication commit is not the batch-18 docs commit")

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
    batch_s5s = sorted(int(k["s5_index"]) for k in bk["keys"])
    if len(batch_s5s) != BATCH_KEY_COUNT or len(set(batch_s5s)) != BATCH_KEY_COUNT:
        fail(f"batch-keys s5 index set is not {BATCH_KEY_COUNT} unique indices")
    for w in WINS:
        win_key_row = [k for k in bk["keys"] if k["key_id"] == w["id"]]
        if len(win_key_row) != 1:
            fail(f"{w['id']} not unique in batch-keys")
        wk = win_key_row[0]
        if (int(wk["s5_index"]) != w["s5"] or int(wk["lo"]) != w["lo"]
                or int(wk["hi"]) != w["hi"] or int(wk["legal"]) != w["legal"]):
            fail(f"batch-keys {w['id']} disagreement: {wk}")

    incr = read_cache(INCR_CACHE)
    if len(incr) != 2 or set(incr) != set(WIN_KEYS):
        fail("increment is not exactly the two v001/v002 rows")
    for w in WINS:
        if incr[(w["lo"], w["hi"])] != (1, w["nodes"]):
            fail(f"increment {w['id']} row {incr[(w['lo'], w['hi'])]} != (WIN, {w['nodes']})")
        key = (w["lo"], w["hi"])
        if key in quarantined or not is_canonical_safe_s5_key(key):
            fail(f"{w['id']} key quarantined or noncanonical")
        if mask_to_index.get(key) != w["s5"]:
            fail(f"{w['id']} key does not map to its published s5 index")

    # --- 2-pass raw re-verification ------------------------------------------
    win_raws = {}
    for w in WINS:
        raw = None
        for tag in ("p1", "p2"):
            p = BATCH_DIR / f"output/raw/{w['id']}.{tag}.out"
            for line in p.read_text().splitlines():
                if not line.startswith("replay,"):
                    continue
                parts = line.split(",")
                row = (int(parts[2]), int(parts[3]), int(parts[5]),
                       int(parts[6]), int(parts[7]), int(parts[9]), int(parts[10]))
                if raw is None:
                    raw = row
                elif raw != row:
                    fail(f"{w['id']} pass mismatch {tag}: {row} vs {raw}")
        if (raw is None or raw[0] != 5 or raw[3] != 1
                or raw[4] != w["nodes"]):
            fail(f"{w['id']} published raw is not the 2-pass WIN: {raw}")
        if (raw[1] != w["legal"] or (raw[5], raw[6]) != (w["lo"], w["hi"])):
            fail(f"{w['id']} raw byte bookkeeping != batch-keys row: {raw}")
        win_raws[w["id"]] = raw

    # --- caches ---------------------------------------------------------------
    base_cache = read_cache(BASE_CACHE)
    scen_cache = read_cache(SCEN_CACHE)
    if len(base_cache) != 6120:
        fail(f"BASE cache rows {len(base_cache)} != 6120")
    for w in WINS:
        if (w["lo"], w["hi"]) in base_cache:
            fail(f"{w['id']} already present in the canonical BASE cache (would not be if-adopted)")
    for w in WINS:
        if scen_cache.get((w["lo"], w["hi"])) != (1, w["nodes"]):
            fail(f"scenario cache does not adopt exactly the {w['id']} WIN row")
    if len(scen_cache) != len(base_cache) + 2:
        fail("scenario cache row count != BASE + 2")
    for key, (v, _n) in scen_cache.items():
        b = base_cache.get(key)
        if b is None:
            if key not in WIN_KEYS:
                fail(f"scenario-only row outside the increment: {key}")
        elif b[0] != v:
            fail(f"scenario verdict drift on shared key {key}")
    base_votes = Counter(v for v, _ in base_cache.values())
    scen_votes = Counter(v for v, _ in scen_cache.values())
    if base_votes.get(1, 0) != 158 or scen_votes.get(1, 0) != 160:
        fail("WIN counts not 158 -> 160")
    if base_votes.get(2, 0) != 5962 or scen_votes.get(2, 0) != 5962:
        fail("LOSS counts not 5,962 -> 5,962")
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
    for w in WINS:
        if base_iv.get(w["s5"]) is not None:
            fail(f"{w['id']} s5 index resolved in BASE (WIN would be consumed on main)")

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
    holders = {w["id"]: sorted(i for i in range(len(s4_masks)) if w["s5"] in s4_cost[i])
               for w in WINS}
    holder_union = sorted(set(holders[WINS[0]["id"]]) | set(holders[WINS[1]["id"]]))
    double_holders = sorted(set(holders[WINS[0]["id"]]) & set(holders[WINS[1]["id"]]))
    expected_flips = sorted(i for i in holder_union if base_st[i] == "unknown")
    if flips != expected_flips:
        fail(f"flips {flips} != machine-computed unknown holders of s5 {WIN_S5S} {expected_flips}")
    if BATCH_CLASS not in flips:
        fail("class 16131 (holder of both WIN s5 children) not among the flips")
    for i in flips:
        if base_st[i] != "unknown" or scen_st[i] != "excluded_now":
            fail(f"flip class {i} is not unknown->excluded_now")
    new_free = sorted(i for i, s in scen_st.items() if s == "free_now" and base_st[i] != "free_now")
    if new_free:
        fail(f"a WIN adoption created newly free classes {new_free} (must be impossible)")

    # --- class 16131 scenario unknowns ----------------------------------------
    base_class_unknown = sorted(base_unknown[BATCH_CLASS])
    if base_class_unknown != batch_s5s:
        fail("BASE-unknown children of class 16131 != the 53 batch-18 key s5 indices")
    scen_class = sorted(scen_unknown[BATCH_CLASS])
    if len(scen_class) != 51:
        fail(f"class 16131 scenario-unknown children count {len(scen_class)} != 51")
    if sorted(set(base_class_unknown) - set(WIN_S5S)) != scen_class:
        fail("scenario-unknown children of 16131 != BASE-unknown minus the two WINs (machine mismatch)")
    for w in WINS:
        if w["s5"] in scen_class:
            fail(f"consumed WIN child {w['id']} still in class 16131's scenario unknown boundary")

    # --- holder rows ------------------------------------------------------------
    holder_rows = {}
    for c in holder_union:
        holder_rows[str(c)] = {
            "base_status": base_st[c],
            "base_unknown_now": len(base_unknown[c]),
            "holds_v001": c in holders["v001"],
            "holds_v002": c in holders["v002"],
            "double_holder": c in double_holders,
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

    if metrics["excluded_now_classes"]["base"] != 23:
        fail("BASE excluded_now baseline drift (expected 23)")
    if metrics["unknown_classes"]["base"] != 34500:
        fail("BASE unknown baseline drift (expected 34,500)")
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
    if newly_resolved not in ([], [153671], [207534], [153671, 207534]):
        fail(f"update8 newly-resolved {newly_resolved} outside the projection universe")
    if len(newly_resolved) != metrics["update8_resolved_count"]["delta"]:
        fail("update8 resolved-count arithmetic inconsistent")
    if metrics["update8_win_hit_groups"]["base"] != 0:
        fail("BASE win_hit_groups baseline drift (expected 0)")
    for grp in scen_summary["frozen_update8_refresh"]["win_hit_groups"]:
        if int(grp["s4_class_index"]) != BATCH_CLASS:
            fail(f"scenario win_hit group outside class {BATCH_CLASS}: {grp}")

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
    s_base = [r for r in base_cc if int(r["class_index"]) == BATCH_CLASS]
    s_scen = [r for r in scen_cc if int(r["class_index"]) == BATCH_CLASS]
    if len(s_base) != 1 or len(s_scen) != 1:
        fail(f"class {BATCH_CLASS} not exactly once in base ({len(s_base)}) "
             f"and scenario ({len(s_scen)}) closure-candidate tables")
    if int(s_base[0]["unknown_now"]) != 53:
        fail(f"base closure row for {BATCH_CLASS} unknown_now {s_base[0]['unknown_now']} != 53")
    if int(s_scen[0]["unknown_now"]) != 51:
        fail(f"scenario closure row for {BATCH_CLASS} unknown_now {s_scen[0]['unknown_now']} != 51")
    base_idx = {int(r["class_index"]) for r in base_cc}
    scen_idx = {int(r["class_index"]) for r in scen_cc}
    closure_rows = {
        "base_class_16131_rank": int(s_base[0]["class_rank"]),
        "base_class_16131_unknown_now": int(s_base[0]["unknown_now"]),
        "scenario_class_16131_rank": int(s_scen[0]["class_rank"]),
        "scenario_class_16131_unknown_now": int(s_scen[0]["unknown_now"]),
        "scenario_class_16131_groups_served_count": int(s_scen[0]["groups_served_count"]),
        "left_table_classes": sorted(base_idx - scen_idx),
        "entered_table_classes": sorted(scen_idx - base_idx),
        "flipped_classes_in_table": sorted(set(flips) & scen_idx),
        "note": ("the closure-candidate table is a probing-worklist view keyed to "
                 "unknown cost children; the win-flip of class 16131 and the other "
                 "holders is recorded by class_status_counts and the transitions "
                 "ledger, not by this table"),
    }

    out = {
        "schema": "n11-b18win-v001v002-ifadopted-decomp-deltas-v1",
        "scenario": ("IF-ADOPTED = canonical 6,120 rows (be9cb24e..., Part AS) + "
                     "the two batch-18 WIN rows (v001 s5 153671 5,656,151 nodes / "
                     "v002 s5 207534 7,898,204 nodes, both 2-pass re-verified here); "
                     "a scrutiny-owner precomputation projection, NOT the canonical chain"),
        "interpretation_guard": ("if-adopted projection deltas only: the WIN "
                                 "verdicts are NOT consumed, the canonical cache is "
                                 "byte-pinned untouched, the holder classes of s5 "
                                 "153671 / 207534 flip to excluded_now (one-way: "
                                 "their all-LOSS closure routes are permanently "
                                 "refuted by the verified WIN children); no coverage "
                                 "change; this Part neither recommends nor rejects "
                                 "adoption; 11x11 empty board and all 19 roots stay "
                                 "UNKNOWN; nodes are bookkeeping"),
        "recompute_gates": ("class statuses with Board free-candidate child "
                            "verification, known-universe counts and per-root free "
                            "coverage were recomputed from graph + update8 + cache "
                            "and asserted equal to the published BASE (Part AS "
                            "reaudit) and if-adopted outputs before any delta was "
                            "emitted; the class-16131 BASE-unknown boundary was "
                            "asserted equal to the 53 batch-18 key s5 indices"),
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
        "win_rows": [
            {"key_id": w["id"], "s5_index": w["s5"], "key": [w["lo"], w["hi"]],
             "result": 1, "nodes": w["nodes"],
             "raw_2pass": {"stones": win_raws[w["id"]][0],
                           "legal": win_raws[w["id"]][1],
                           "budget": win_raws[w["id"]][2],
                           "result": win_raws[w["id"]][3],
                           "nodes": win_raws[w["id"]][4]}}
            for w in WINS
        ],
        "flips_excluded_now": flips,
        "flips_gate": ("flips == the machine-computed BASE-unknown graph holder "
                       "classes of s5 153671 or 207534 (computed from the pinned "
                       "graph cost sets, not hardcoded); each transitions unknown "
                       "-> excluded_now; no regression; a WIN adoption can never "
                       "free a class or move per-root coverage (all gated)"),
        "status_transitions": dict(sorted(transitions.items())),
        "newly_free_now_classes": new_free,
        "win_holders": {
            "v001_s5_153671": holders["v001"],
            "v002_s5_207534": holders["v002"],
            "holder_union": holder_union,
            "double_holders": double_holders,
            "rows": holder_rows,
        },
        "class_16131": {
            "base_status": base_st[BATCH_CLASS],
            "scenario_status": scen_st[BATCH_CLASS],
            "base_unknown_children": len(base_unknown[BATCH_CLASS]),
            "scenario_unknown_children": len(scen_unknown[BATCH_CLASS]),
            "base_unknown_equals_batch_keys": True,
            "scenario_unknown_indices": sorted(scen_unknown[BATCH_CLASS]),
        },
        "update8": {
            "newly_resolved_s5": newly_resolved,
            "lost_resolved": lost,
            "win_hit_groups_base": base_summary["frozen_update8_refresh"]["win_hit_groups"],
            "win_hit_groups_scenario": scen_summary["frozen_update8_refresh"]["win_hit_groups"],
            "groups_free_now": [base_summary["frozen_update8_refresh"]["groups_free_now"],
                                scen_summary["frozen_update8_refresh"]["groups_free_now"]],
        },
        "newly_free_thirds": newly_free_thirds,
        "changed_per_root_coverage_rows": changed_rows,
        "per_root_greedy": per_root_greedy_movers,
        "metrics": metrics,
        "closure_candidate_rows": closure_rows,
    }
    OUT.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("OK decomp-deltas-v001v002-ifadopted.json: "
          f"flips={flips} new_free={new_free} double_holders={double_holders} "
          f"excluded_now {metrics['excluded_now_classes']['base']}->{metrics['excluded_now_classes']['scenario']} "
          f"class16131 unknown {len(base_unknown[BATCH_CLASS])}->{len(scen_unknown[BATCH_CLASS])} "
          f"free_now {metrics['free_now_classes']['base']}->{metrics['free_now_classes']['scenario']} "
          f"update8_resolved +{len(newly_resolved)} "
          f"win_hit_groups {metrics['update8_win_hit_groups']['base']}->{metrics['update8_win_hit_groups']['scenario']} "
          f"joint_greedy {metrics['joint_greedy_union_size']['base']}->{metrics['joint_greedy_union_size']['scenario']} "
          f"worklist {metrics['probe_worklist_total']['base']}->{metrics['probe_worklist_total']['scenario']}")


if __name__ == "__main__":
    main()
