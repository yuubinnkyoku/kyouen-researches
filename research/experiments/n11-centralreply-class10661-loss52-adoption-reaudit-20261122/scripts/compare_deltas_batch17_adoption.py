#!/usr/bin/env python3
"""Batch-17 (class 10661) 52-LOSS canonical-adoption reaudit delta extractor (Part AV).

Fail-closed, read-only audit executing the single-owner Part AV declaration
(note amendment commit 340abef3) as taken over by the published Part AV
takeover amendment (commit d3ef2dc6, observed HEAD-before-push 432664f7;
scope unchanged - ownership transfer only).  Compares the published BASE
refresh outputs (Part AS reaudit on the canonical cache be9cb24e..., 6,120
rows) against the single post-adoption computation:

  ADOPTED-CANONICAL = BASE + the 52 resolved LOSS rows (u001..u052) of
  batch-17 (class 10661)

Batch-17 probed all 52 unknown cost children of class 10661 with 2-pass
node-exact results: 52 LOSS / 0 WIN / 0 exhausted / 0 mismatch
(EXECUTION-COMPLETE clean all-LOSS batch, published Part AU).  Batch-17
contains NO WIN row (absence gate), so the adopted packet IS the full
resolved packet - full == loss here, machine-asserted from the published
batch-17 raws/status/batch-keys/row-audit and the increments manifest
before any delta is emitted, including an independent two-pass raw
re-verification of all 52 rows (verdict 2, node-exact, key and legal
agreement with batch-keys) that does not rely on the maker.

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
    batch-keys, batch-17 row-audit,
  * manifest: 52 resolved / 52 LOSS / 0 adopted WIN / 0 exhausted /
    probed 52/52, win_ids and unadopted_win_ids and exhausted ids empty,
    full_packet_eq_loss_only TRUE, win_scenario_exists FALSE, row-audit
    52-row agreement recorded, loss sha == increment sha;
  * independent two-pass raw re-verification of all 52 keys: both raws
    agree on (stones, legal, is_or, budget, result, nodes, lo, hi), every
    result is 2 (LOSS), every key agrees with batch-keys, and NONE of the
    52 keys is a WIN anywhere (no WIN verdict arises from this batch);
  * the 52 increment keys exist, are canonical, unquarantined, absent from
    the BASE cache and the update8 receipt, map to their published s5
    indices, and are all BASE-unknown cost children of class 10661;
  * scenario cache == BASE rows + increment rows with verdict agreement;
  * every recomputed status transition is one of
    excluded->excluded, excluded_now->excluded_now, free_now->free_now,
    unknown->{unknown, free_now};
  * excluded_now flip set EMPTY (a zero-WIN increment cannot flip), and no
    excluded_now regression;
  * newly free_now classes == exactly the classes whose BASE-unknown cost
    children are ALL resolved by the increment (computed, not hardcoded)
    AND class 10661 IS among them (this is the central machine-checked
    consequence of consuming its full all-LOSS child boundary; its
    Board-verification is part of the refresh re-execution);
  * class 10661: 52 BASE-unknown cost children == the batch-17 key set,
    ALL resolved by the increment, scenario-unknown cost children 0
    (the class leaves the unknown population);
  * every graph holder class of the 52 keys: scenario unknown_now ==
    BASE unknown_now - own membership in the increment;
  * update8 newly-resolved baseline requirements must lie inside the
    increment universe, no resolution lost, count arithmetic consistent;
  * per-root coverage recomputed from the graph matches the published
    per-root-coverage.csv for BASE and scenario; root 27 stays 119/119;
    newly free thirds must contain a newly free class among their options
    and the changed per-root rows must be exactly the rows with a newly
    free third (coverage may only improve);
  * class 10661 must be present in the BASE closure-candidate table
    (unknown_now 52) and ABSENT from the scenario table (exited by
    freeing); class 23101 must stay an unknown class with unknown_now 11
    in both tables (this adoption neither closes nor excludes it).

Measured (recorded, not gated, scheduling quantities only): per-root and
joint greedy remaining-requirement sizes, probe worklist size, roots
summary rows, closure-candidate rows, group-best option counts,
closure-table churn.

The 52 LOSS rows ARE consumed into the canonical cache by the Part AV
fail-closed merger (a zero-WIN full-packet adoption); the only canonical
claim established by this reaudit is the classification delta itself on
the canonical cache: class 10661 leaves the unknown population and becomes
the 37th Board-verified free class, unknown classes 34,500 -> 34,499.
Never a 19-root or 11x11 result; nodes are bookkeeping only.  The 11x11
empty board stays UNKNOWN; all 19 central-reply roots stay UNKNOWN.
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
OUT = EXP / "output/decomp-deltas-batch17-adoption.json"

GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_DIR = ROOT / "research/experiments/n11-centralreply-class23101-loss41-adoption-reaudit-20261122/reaudit/output"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class23101-loss41-adoption-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-20261122.cache"
BATCH_DIR = ROOT / "research/experiments/n11-centralreply-closure-class10661-batch17-20261122"
SCEN_OUT = EXP / "reaudit/output"
INCR_CACHE = EXP / "output/increment-batch17-loss52-20261122.cache"
MANIFEST = EXP / "output/increments-manifest.json"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-20261122.cache"

INCR_SHA = "afcdad5b9fa864d076e6998c12dc4ff1fdf69c110a2cf1495af2b3a96c3c4d52"
SCEN_CACHE_SHA = "a554081156e2c2f940ecf2cc3c7af082dde6b760d6019e0a5113c4ddd5e12a3a"
BASE_CACHE_SHA = "be9cb24e899fbe93db51e415320c50fa733e378748bb7a41fe13fd7b22f06685"
BASE_SUMMARY_SHA = "f2008e70b31f23724d9bd8d605f7ab6f1de20f1802e65bd5b955420a2f50a744"
SCEN_SUMMARY_SHA = "a0043c76c05ee949a533f31e6f21616d51f67e211c45fec5cc96431fb7d28dc4"
BASE_CLOSURE_SHA = "3ee1dbb6db7a5fc8858f5bbdd5cae7ca754589f376ebb99727535806f917bc9e"
BASE_PRC_SHA = "527c7e9a3f6350f638b5e2e2a70c3115e50533eeca651e38e32329a04ab225d4"
SCEN_CLOSURE_SHA = "e60c1088f99aac0ae527b78eac9d192d7e1d2aa4f1a125fa52bc75c86ae16710"
SCEN_PRC_SHA = "4c7ec5d78b7a3496c01fc37a229cc85f27708926511476f516f7f6cedd975e35"
BATCH_KEYS_SHA = "db762175272206aa53622f30addc1267d534e8a3e576f70c6a084f21392645d2"
ROW_AUDIT_SHA = "c19e768f1ce4223de6736713a679028990ef5a884c9886affd62c951e307d5f9"

SCENARIO = "ADOPTED-CANONICAL"
BATCH_CLASS = 10661
UNIVERSE_SIZE = 31859
RECEIPT_COUNT = 23
ADOPTED_ROWS = 52
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
                          ("batch-17 row-audit", BATCH_DIR / "output/row-audit.json", ROW_AUDIT_SHA)):
        got = sha(p)
        if got != want:
            fail(f"{name} sha256 drift: {got} != {want}")

    manifest = json.loads(MANIFEST.read_text())
    rc = manifest["row_counts"]
    if not (rc["resolved_rows"] == 52 and rc["losses"] == 52 and rc["wins"] == 0
            and rc["exhausted_excluded"] == 0 and rc["probed_total"] == 52
            and rc["probed_resolved"] == 52):
        fail(f"manifest row_counts not 52 LOSS / 0 adopted WIN / 0 exhausted of 52 resolved: {rc}")
    if (manifest["win_ids"] != [] or manifest["unadopted_win_ids"] != []
            or manifest["exhausted_excluded_ids"] != []):
        fail(f"manifest win/unadopted/exhaustion id lists not empty (absence gate): {manifest}")
    if manifest["loss_ids"] != manifest["resolved_ids"]:
        fail("manifest loss_ids != resolved_ids (all resolved rows are adopted)")
    if [f"u{i:03d}" for i in range(1, 53)] != manifest["loss_ids"]:
        fail("manifest loss_ids != u001..u052")
    if manifest["full_packet_eq_loss_only"] is not True or manifest["win_scenario_exists"] is not False:
        fail("manifest full==loss / no-WIN-scenario bookkeeping not asserted")
    if manifest["sha256"]["loss"] != INCR_SHA:
        fail("manifest loss sha does not match the pinned increment")
    if manifest["row_audit_sha256"] != ROW_AUDIT_SHA or manifest["row_audit_agreement_rows"] != 52:
        fail("manifest row-audit bookkeeping drift")
    if manifest["status_log_stop_record"] != "EXECUTION-COMPLETE: 52/52 probed = 52 LOSS":
        fail("manifest status-log stop record drift")

    ra = json.loads((BATCH_DIR / "output/row-audit.json").read_text())
    if ra["results"] != {"loss": 52, "win": 0, "exhausted": 0, "mismatch": 0}:
        fail(f"published row-audit results not the clean all-LOSS picture: {ra['results']}")

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
        fail("batch-17 keys collide on s5 indices")

    # --- independent two-pass raw re-verification of ALL 52 keys -------------
    # (second implementation of the maker's row gate; does not trust the maker)
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
        if result != 2:
            fail(f"{kid} raw result {result} is not LOSS - batch-17 must be a clean all-LOSS batch")
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
        fail("increment key set not contained in the batch-17 key set")
    adopted_loss_ids = sorted(kid for kid, (lo, hi, _s, _m) in batch_keys.items()
                              if (lo, hi) in incr)
    if [f"u{i:03d}" for i in range(1, 53)] != adopted_loss_ids:
        fail(f"adopted LOSS ids {adopted_loss_ids[:5]}... != u001..u052")
    if len(incr_index) != 52:
        fail("adopted s5 index set != 52")

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
    if scen_votes.get(1, 0) != 158 or scen_votes.get(2, 0) != 6014:
        fail(f"scenario cache verdict counts not 158 WIN / 6014 LOSS: {dict(sorted(scen_votes.items()))}")

    # --- graph holders of the 52 keys ---------------------------------------
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
    if BATCH_CLASS not in new_free:
        fail("class 10661 must BE among the newly free classes: consuming its clean "
             "all-LOSS child boundary frees it (Board-verified in the re-execution)")
    if scen_st[BATCH_CLASS] != "free_now" or len(scen_unknown[BATCH_CLASS]) != 0:
        fail("class 10661 scenario status/unknown drift")
    basec10661 = sorted(base_unknown[BATCH_CLASS])
    if len(basec10661) != 52:
        fail(f"class 10661 BASE-unknown cost children {len(basec10661)} != 52")
    if not set(incr_index) <= set(basec10661):
        fail("increment s5 indices are not all BASE-unknown cost children of class 10661")
    leftover10661 = sorted(set(basec10661) - set(incr_index))
    if leftover10661:
        fail(f"class 10661 has leftover BASE-unknown children not resolved by the full "
             f"packet: {leftover10661}")
    if sorted(scen_unknown[BATCH_CLASS]) != leftover10661:
        fail("class 10661 scenario-unknown children != leftover arithmetic")
    batch_s5 = {v[2] for v in batch_keys.values()}
    if batch_s5 != set(basec10661):
        fail(f"batch-17 key set != the 52 BASE-unknown cost children of class 10661 "
             f"(batch-only {sorted(batch_s5 - set(basec10661))[:5]}, "
             f"base-only {sorted(set(basec10661) - batch_s5)[:5]})")

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
    b10661 = [r for r in base_cc if int(r["class_index"]) == BATCH_CLASS]
    if len(b10661) != 1:
        fail(f"class 10661 appears {len(b10661)} times in the BASE closure-candidate table")
    if int(b10661[0]["unknown_now"]) != 52:
        fail(f"BASE closure row for 10661 unknown_now {b10661[0]['unknown_now']} != 52")
    s10661 = [r for r in scen_cc if int(r["class_index"]) == BATCH_CLASS]
    if s10661:
        fail("class 10661 must be ABSENT from the scenario closure-candidate table "
             "(exited by becoming a Board-verified free class)")
    s23101 = [r for r in scen_cc if int(r["class_index"]) == 23101]
    if len(s23101) != 1 or int(s23101[0]["unknown_now"]) != 11:
        fail("class 23101 must stay in the scenario closure-candidate table with "
             "unknown_now 11 (untouched by this adoption)")
    b23101 = [r for r in base_cc if int(r["class_index"]) == 23101]
    if len(b23101) != 1 or int(b23101[0]["unknown_now"]) != 11:
        fail("class 23101 BASE closure row drift")
    base_idx = {int(r["class_index"]) for r in base_cc}
    scen_idx = {int(r["class_index"]) for r in scen_cc}
    closure_rows = {
        "base_class_10661_row": b10661[0],
        "base_class_10661_rank": int(b10661[0]["class_rank"]),
        "scenario_class_10661_row": None,
        "base_class_23101_row": b23101[0],
        "scenario_class_23101_row": s23101[0],
        "scenario_first_row": scen_cc[0] if scen_cc else None,
        "left_table_classes": sorted(base_idx - scen_idx),
        "entered_table_classes": sorted(scen_idx - base_idx),
    }
    if BATCH_CLASS not in closure_rows["left_table_classes"]:
        fail(f"class 10661 must be among the classes leaving the closure-candidate "
              f"table (exited by becoming a Board-verified free class): "
              f"{closure_rows['left_table_classes']}")

    # --- output --------------------------------------------------------------
    out = {
        "schema": "n11-batch17-adoption-decomp-deltas-v1",
        "scenario": ("ADOPTED-CANONICAL = pre-adoption BASE (canonical 6,120 rows, Part AS "
                     "reaudit state) + the 52 LOSS rows of batch-17 (class 10661); "
                     "full==loss: batch-17 contains no WIN row (absence gate) and no "
                     "exhaustion row, so the adopted packet IS the full resolved packet"),
        "interpretation_guard": ("canonical adoption deltas: the 52 LOSS rows of batch-17 "
                                 "are consumed into the canonical cache via the fail-closed "
                                 "union merger; scheduling quantities are bookkeeping; "
                                 "class 10661 becomes the 37th Board-verified free class "
                                 "and leaves the unknown population; every other claim "
                                 "stays UNKNOWN; 11x11 empty board and all 19 roots stay "
                                 "UNKNOWN; nodes are bookkeeping"),
        "recompute_gates": ("class statuses with Board free-candidate child verification, "
                            "known-universe counts and per-root free coverage were "
                            "recomputed from graph + update8 + cache and asserted equal "
                            "to the published BASE (Part AS reaudit) and scenario "
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
            "count": 52, "adopted_loss": 52, "unadopted_win": 0,
            "batch_class": BATCH_CLASS,
            "class_mask": list(s4_masks[BATCH_CLASS]),
            "cost_children_total": len(s4_cost[BATCH_CLASS]),
            "batch_groups_served": [list(x) for x in batch_groups_served],
        },
        "excluded_now_flips": flips,
        "newly_free_now_classes": new_free,
        "newly_free_now_gate": ("each newly free class was BASE-unknown and every "
                                "BASE-unknown cost child is resolved by the increment "
                                "(clean all-LOSS); a zero-WIN full packet can only free, "
                                "never flip; class 10661 IS the newly freed class"),
        "status_transitions": dict(sorted(transitions.items())),
        "class_10661": {
            "base_unknown_children": len(base_unknown[BATCH_CLASS]),
            "adopted_by_increment": len(incr_index),
            "scenario_unknown_children": len(scen_unknown[BATCH_CLASS]),
            "scenario_status": scen_st[BATCH_CLASS],
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
    print("OK decomp-deltas-batch17-adoption.json: "
          f"flips={flips} new_free={new_free} "
          f"free_now {metrics['free_now_classes']['base']}->{metrics['free_now_classes']['scenario']} "
          f"class10661_unknown {len(base_unknown[BATCH_CLASS])}->{len(scen_unknown[BATCH_CLASS])} "
          f"update8_resolved +{len(newly_resolved)} "
          f"joint_greedy {metrics['joint_greedy_union_size']['base']}->{metrics['joint_greedy_union_size']['scenario']} "
          f"worklist {metrics['probe_worklist_total']['base']}->{metrics['probe_worklist_total']['scenario']} "
          f"changed_rows={sorted(changed_rows)}")


if __name__ == "__main__":
    main()
