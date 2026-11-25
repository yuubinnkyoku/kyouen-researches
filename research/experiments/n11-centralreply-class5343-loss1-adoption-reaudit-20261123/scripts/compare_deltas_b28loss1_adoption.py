#!/usr/bin/env python3
"""Batch-28 (class 5343) 1-LOSS canonical-adoption reaudit delta extractor
(Part CH).

Fail-closed, read-only audit executing the single-owner Part CH declaration
(note amendment 2026-11-23; publish-then-execute).  Compares the published
BASE refresh outputs (Part BZ reaudit on the canonical cache 9115be9e...,
6,293 rows, itself the Part BU 6,287-row chain) against the single
post-adoption computation:

  ADOPTED-CANONICAL = BASE + the single adopted LOSS row aa003
  (batch-28 / class 5343; s5 104943; nodes 4,070,373)

The batch is NOT a complete enumeration book: batch-28 probed 7/54 keys
(Part CB drive-1 aa001/aa002 WIN-HALT pairs; Part CD drive-2 aa003 LOSS
row + aa004/aa005 EXHAUSTED honest-UNKNOWN + aa006/aa007 WIN-HALT pairs);
the 47 fileless keys (aa008..aa054) are untouched.  The WIN rows aa001
and aa002 (third-implementation cross-verified in Part CC), aa006 and
aa007 (Part CG cross-verification lane declared, pending output) are
HONEST LABELS ONLY and are NOT adopted - they stay unconsumed (scrutiny
owner C++ second-implementation gate pin 9193f5b6...; batch-14residual
q042 / batch-26 l028 precedents) - and the EXHAUSTED rows aa004/aa005
are honest UNKNOWN bookkeeping, so full != loss and class 5343 does NOT
free in this adoption.  The adopted packet is loss-only and can free NO
class unless all BASE-unknown cost children of the class are resolved
(machine-gated below); class 5343 keeps its 4 WIN children plus 53
unknowns in the refreshed table.

Gates (fail-closed, machine-checked) mirror the Part BZ extractor
discipline adapted to the 1-batch / 1-row / 4-WIN / 2-EXHAUSTED / 0-
fragment shape of batch-28:

  * sha256 pins: increment, scenario cache, base cache, base summary,
    scenario summary, base closure-classes.csv, base per-root-coverage.csv,
    scenario closure-classes.csv, scenario per-root-coverage.csv,
    the batch-28 batch-keys file and the row-audit-winhalt file;
  * manifest: 1 adopted LOSS / 4 unadopted WIN (aa001/aa002/aa006/aa007) /
    2 EXHAUSTED excluded (aa004/aa005) / probed 7 with 0 fragments,
    loss_ids == [aa003], resolved_ids == the 7 probed ids,
    win_ids == unadopted_win_ids == [aa001, aa002, aa006, aa007],
    exhausted_excluded_ids == [aa004, aa005],
    full_packet_eq_loss_only FALSE, win_scenario_exists TRUE,
    loss sha == increment sha, merger pin, adopted-row node totals
    pinned (4,070,373 on both passes);
  * the published row-audit-winhalt summary agrees with the manifest and
    the pinned keys (schema, class, batch, probed 7, pass_rows 1,
    loss/win rows, exhausted rows, fragment bookkeeping empty,
    mismatches 0, input_pins);
  * independent two-pass raw re-verification of all 7 probed keys: both
    raws agree on (stones, legal, is_or, budget, result, nodes, lo, hi),
    the adopted key aa003 is result 2 (LOSS) with its published node
    count, the 4 WIN keys are result 1 (honest labels with published
    node counts), the 2 EXHAUSTED keys are result 0 with nodes == budget
    (honest UNKNOWN, NOT adopted), each key agrees with batch-keys;
  * increment == exactly the aa003 row; both WIN and EXHAUSTED keys are
    asserted NOT in the increment, NOT in BASE, NOT in the scenario cache,
    not in the update8 receipt, quarantined nowhere, canonical-safe;
  * scenario cache == BASE rows + increment row with verdict agreement
    (6,294 rows; 158 WIN / 6,136 LOSS);
  * every graph holder class of the adopted key: scenario unknown_now ==
    BASE unknown_now - own membership in the increment; holder count ==
    batch-keys membership_class_count (3);
  * the published refresh recomputes (class statuses with Board
    free-candidate child verification, known-universe counts, per-root
    coverage) are re-executed from graph + update8 + cache and asserted
    equal to the published BASE (Part BZ reaudit) and scenario outputs
    before any delta is emitted;
  * no excluded_now flips, no newly free class beyond the machine
    recomputation, no per-root coverage regression, root 27 stays
    119/119;
  * closure table: class 5343 unknown_now 54 -> 53 (rank 27 -> 19),
    the -- churn classes are pure ranking bookkeeping (recomputed BASE ==
    scenario unknown at every churned class), untouched anchors 23101 /
    1849 / 12643 stay unknown_now 1/1/53 in both tables;
  * update8 resolved-requirement delta gated to the increment: newly
    resolved set == {104943} only.

Scheduling quantities are bookkeeping, never verdicts.  11x11 stays
UNKNOWN; nodes are bookkeeping, never verdicts.
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
OUT = EXP / "output/decomp-deltas-b28loss1-adoption.json"

GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_DIR = ROOT / "research/experiments/n11-centralreply-class16957-13342-loss6-adoption-reaudit-20261123/reaudit/output"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class16957-13342-loss6-adoption-reaudit-20261123/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-plus-batch20loss53-plus-batch26loss52-plus-batch24loss2-plus-batch27loss4-20261123.cache"
BATCH28_DIR = ROOT / "research/experiments/n11-centralreply-closure-class5343-batch28-drive2-20261123"
SCEN_OUT = EXP / "reaudit/output"
INCR_CACHE = EXP / "output/increment-b28loss1-20261123.cache"
MANIFEST = EXP / "output/increments-manifest.json"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-plus-batch20loss53-plus-batch26loss52-plus-batch24loss2-plus-batch27loss4-plus-batch28loss1-20261123.cache"

INCR_SHA = "dc857bfd2ecd00deaea3dbe214e0eec0e5b9d7704104a8721d046f262f170487"
SCEN_CACHE_SHA = "3124461b14e4f73a7248cbf5b96c7ff59ebfdcc05258adeb9c81791d86cc461e"
BASE_CACHE_SHA = "9115be9eca1e60828a90c50041f511b598ef79fc0be76d5e16821816e478e93e"
BASE_SUMMARY_SHA = "fca242cc767f4e30b1d450a3b10cbd524b18b96f28b4cc4ba83c8762f8bb2ff2"
SCEN_SUMMARY_SHA = "76cad2a14263ee59cd8bc83008c26bd0b656f2c74e2e7a650550306dda40d395"
BASE_CLOSURE_SHA = "14fc37c3a6f5c6753cac72a094d2c7693defb4a5e483558b3b87a42016b679d9"
BASE_PRC_SHA = "4218a6b49f8dd4df41f9bb3b746c7f2a32afeb3e22d175243e9319c8f46ca56a"
SCEN_CLOSURE_SHA = "baa2db136c18c681633e5bfe3b5a1dec3f084d0c696b4454ae1855ab0773e7fd"
SCEN_PRC_SHA = "75e594419d7822752c9b91b58b8c96ba352296f83707b98786a8bd07afb6c439"
B28_KEYS_SHA = "af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5"
B28_ROW_AUDIT_SHA = "3e86a32b847b5799594be5fbee6624878deadf02990940b2503f931d7af30e91"

SCENARIO = "ADOPTED-CANONICAL"
UNIVERSE_SIZE = 31859
RECEIPT_COUNT = 23
ADOPTED_ROWS = 1
B28_CLASS = 5343
BUDGET = 15000000
UNADOPTED_WINS = {
    "aa001": {"s5": 28037, "key": (1315631633331650560, 0), "legal": 88,
              "nodes": 13183855, "cross": "Part CC third-implementation cross-verified"},
    "aa002": {"s5": 87306, "key": (1171516445390012416, 0), "legal": 86,
              "nodes": 6527041, "cross": "Part CC third-implementation cross-verified"},
    "aa006": {"s5": 129823, "key": (1171516445255794692, 0), "legal": 88,
              "nodes": 14303810, "cross": "Part CG cross-verification lane declared (pending output)"},
    "aa007": {"s5": 135236, "key": (1171516445255794696, 0), "legal": 95,
              "nodes": 13483540, "cross": "Part CG cross-verification lane declared (pending output)"},
}
EXHAUSTED_IDS = {
    "aa004": {"s5": 118693, "key": (1171516445255794689, 0), "legal": 91},
    "aa005": {"s5": 124331, "key": (1171516445255794690, 0), "legal": 89},
}
ADOPTED_LOSS = {"aa003"}
RESOLVED_IDS = ["aa001", "aa002", "aa003", "aa004", "aa005", "aa006", "aa007"]
ADOPTED_TOTAL_NODES = 4070373
ADOPTED_S5 = 104943
ADOPTED_KEY = (1152921504741064704, 4228)
ADOPTED_LEGAL = 86
ALLOWED_TRANSITIONS = {"excluded": ["excluded"], "excluded_now": ["excluded_now"],
                       "free_now": ["free_now"], "unknown": ["unknown", "free_now"]}
# closure-table churn observed machine-side (declared before this run):
# rank 27 -> 19 for class 5343; every class ranked 19..26 shifts +1.
CHURN_RANK_EXPECT = {
    5343: (27, 19), 5687: (19, 20), 12643: (20, 21), 31600: (21, 22),
    10968: (22, 23), 23964: (23, 24), 25835: (24, 25), 30565: (25, 26),
    5690: (26, 27),
}


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


def load_keys(batch_dir, class_index, expected_total):
    bk = json.loads((batch_dir / "input/batch-keys.json").read_text())
    if bk["class_index"] != class_index:
        fail(f"batch-keys class_index {bk['class_index']} != {class_index}")
    gs_raw = bk.get("groups_served_full")
    if gs_raw is not None:
        groups_served = sorted((int(e["first"]), int(e["third"])) for e in gs_raw)
    else:
        e = bk["groups_served_first_seen"]
        groups_served = sorted({(int(e["first"]), int(e["third"]))})
    if not groups_served:
        fail(f"batch-keys groups-served empty for class {class_index}")
    return bk, groups_served


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
                          ("batch-28 keys", BATCH28_DIR / "input/batch-keys.json", B28_KEYS_SHA),
                          ("batch-28 row-audit", BATCH28_DIR / "output/row-audit-winhalt.json", B28_ROW_AUDIT_SHA)):
        got = sha(p)
        if got != want:
            fail(f"{name} sha256 drift: {got} != {want}")

    manifest = json.loads(MANIFEST.read_text())
    if manifest["schema"] != "b28loss1-increments-manifest-v1":
        fail(f"manifest schema drift: {manifest['schema']}")
    rc = manifest["row_counts"]
    if not (rc["adopted_loss_rows"] == 1 and rc["wins"] == 4
            and rc["exhausted_excluded"] == 2 and rc["probed_rows"] == 7
            and rc["fragments_unprobed"] == 0 and rc["fileless_unprobed"] == 47):
        fail(f"manifest row_counts not the 1-LOSS / 4-WIN / 2-EXHAUSTED picture: {rc}")
    if (manifest["win_ids"] != ["aa001", "aa002", "aa006", "aa007"]
            or manifest["unadopted_win_ids"] != ["aa001", "aa002", "aa006", "aa007"]
            or manifest["exhausted_excluded_ids"] != ["aa004", "aa005"]):
        fail(f"manifest win/unadopted/exhaustion id lists drift: {manifest}")
    if manifest["loss_ids"] != ["aa003"]:
        fail("manifest loss_ids != [aa003]")
    if sorted(manifest["resolved_ids"]) != RESOLVED_IDS:
        fail("manifest resolved_ids != the 7 probed ids")
    if manifest["full_packet_eq_loss_only"] is not False or manifest["win_scenario_exists"] is not True:
        fail("manifest full != loss / WIN-scenario bookkeeping not asserted "
             "(4 WIN rows exist and are NOT adopted)")
    if manifest["sha256"]["loss"] != INCR_SHA:
        fail("manifest loss sha does not match the pinned increment")
    if manifest["merger_sha256"] != "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a":
        fail("manifest merger pin drift (the pinned fail-closed union merger)")
    per_batch_manifest = {b["batch"]: b for b in manifest["batches"]}
    if set(per_batch_manifest) != {28}:
        fail("manifest batches != {28}")
    mb = per_batch_manifest[28]
    if mb["class_index"] != B28_CLASS or mb["keys_total"] != 54:
        fail("manifest batch-28 class/keys_total drift")
    if mb["adopted_loss_ids"] != ["aa003"] or mb["unadopted_win_ids"] != ["aa001", "aa002", "aa006", "aa007"]:
        fail("manifest batch-28 adopted/unadopted id lists drift")
    if sorted(mb["probed_ids"]) != sorted(RESOLVED_IDS):
        fail("manifest batch-28 probed ids drift")
    if mb["input_sha256"] != B28_KEYS_SHA or mb["row_audit_sha256"] != B28_ROW_AUDIT_SHA:
        fail("manifest batch-28 input/row-audit sha bookkeeping drift")
    if mb["total_nodes_pass_one"] != mb["total_nodes_pass_two"] or mb["total_nodes_pass_one"] != ADOPTED_TOTAL_NODES:
        fail(f"manifest batch-28 adopted-row node total drift ({ADOPTED_TOTAL_NODES} expected)")
    if len(mb["status_log_stop_records"]) != 4:
        fail("manifest batch-28 stop-record count drift (4 WIN-HALT pairs)")
    if len(mb["status_log_exhausted_records"]) != 2:
        fail("manifest batch-28 EXHAUSTED-record count drift (2 records)")
    if mb["fragment_state"] != {}:
        fail("manifest batch-28 fragment_state must be empty (0 fragments)")
    uwr = manifest["unadopted_win_rows"]
    if not (isinstance(uwr, list) and len(uwr) == 4):
        fail("manifest unadopted_win_rows must list the 4 honest WIN labels")
    for row in uwr:
        w = UNADOPTED_WINS[row["key_id"]]
        if not (row["s5_index"] == w["s5"] and (row["lo"], row["hi"]) == w["key"]
                and row["legal"] == w["legal"] and row["result"] == 1
                and row["nodes"] == w["nodes"] and row["two_pass_node_exact"] is True):
            fail(f"manifest unadopted WIN row bookkeeping drift: {row}")
    exr = manifest["exhausted_rows"]
    if not (isinstance(exr, list) and len(exr) == 2):
        fail("manifest exhausted_rows must list the 2 honest EXHAUSTED labels")
    for row in exr:
        e = EXHAUSTED_IDS[row["key_id"]]
        if not (row["s5_index"] == e["s5"] and (row["lo"], row["hi"]) == e["key"]
                and row["legal"] == e["legal"] and row["result"] == 0
                and row["nodes"] == BUDGET and row["two_pass_node_exact"] is True):
            fail(f"manifest EXHAUSTED row bookkeeping drift: {row}")

    # the published row-audit-winhalt summary agrees with the manifest
    ra = json.loads((BATCH28_DIR / "output/row-audit-winhalt.json").read_text())
    if (ra["class_index"] != B28_CLASS or ra["batch"] != 28
            or ra["keys_total"] != 54 or ra["probed"] != 7
            or ra["pass_rows"] != 1
            or ra["loss_rows"] != ["aa003"]
            or ra["win_rows"] != ["aa001", "aa002", "aa006", "aa007"]
            or ra["exhausted_rows"] != ["aa004", "aa005"]
            or ra["mismatches"] != 0
            or ra["input_sha256"] != B28_KEYS_SHA
            or ra["fragment_keys"] != {}):
        fail(f"published row-audit (batch 28) not the published picture: {ra}")

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
    bk, groups_served = load_keys(BATCH28_DIR, B28_CLASS, 54)
    if [int(x) for x in bk["class_mask"]] != list(s4_masks[B28_CLASS]):
        fail("batch-keys class_mask != graph mask of class 5343")
    if len(bk["keys"]) != 54:
        fail(f"class 5343 batch-keys count {len(bk['keys'])} != 54")
    batch_keys = {}
    for k in bk["keys"]:
        kid = k["key_id"]
        lo, hi, s5i = int(k["lo"]), int(k["hi"]), int(k["s5_index"])
        if mask_to_index.get((lo, hi)) != s5i:
            fail(f"{kid} (lo,hi) does not map to its published s5 index {s5i}")
        if (lo, hi) in quarantined or not is_canonical_safe_s5_key((lo, hi)):
            fail(f"{kid} noncanonical or quarantined key")
        batch_keys[kid] = (lo, hi, s5i, int(k["membership_class_count"]), B28_CLASS)
    if len(set(v[2] for v in batch_keys.values())) != len(batch_keys):
        fail("batch keys collide on s5 indices")

    # --- independent two-pass raw re-verification of ALL 7 probed keys ------
    # (second implementation of the maker's row gate; does not trust the maker;
    #  the adopted key must be LOSS, the 4 WIN keys honest labels, the 2
    #  EXHAUSTED keys honest UNKNOWN budget-exhaustions)
    for kid, (lo, hi, s5i, _m, cls) in sorted(batch_keys.items()):
        if kid not in RESOLVED_IDS:
            continue
        rows_raw = []
        for tag in ("p1", "p2"):
            p = BATCH28_DIR / f"output/raw/{kid}.{tag}.out"
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
        if stones != 5 or is_or != 0 or budget != BUDGET:
            fail(f"{kid} raw depth/budget drift: {p1}")
        if kid in UNADOPTED_WINS:
            w = UNADOPTED_WINS[kid]
            if result != 1:
                fail(f"{kid} raw result {result} is not the published honest WIN label 1")
            if nodes != w["nodes"]:
                fail(f"{kid} nodes {nodes} != the published node count {w['nodes']}")
        elif kid in EXHAUSTED_IDS:
            e = EXHAUSTED_IDS[kid]
            if result != 0 or nodes != BUDGET:
                fail(f"{kid} raw record is not the published budget exhaustion: {p1}")
            if legal != e["legal"]:
                fail(f"{kid} EXHAUSTED legal drift")
        elif result != 2:
            fail(f"{kid} raw result {result} is not LOSS - adopted rows must be result 2")
        if (klo, khi) != (lo, hi) or legal != int(
                next(k for k in bk["keys"] if k["key_id"] == kid)["legal"]):
            fail(f"{kid} raw key/legal != batch-keys")
    # the adopted row values
    if batch_keys["aa003"] != (ADOPTED_KEY[0], ADOPTED_KEY[1], ADOPTED_S5, 3, B28_CLASS):
        fail("aa003 batch-keys entry drift")

    incr = read_cache(INCR_CACHE)
    if len(incr) != ADOPTED_ROWS:
        fail(f"increment row count {len(incr)} != {ADOPTED_ROWS}")
    if any(v[0] != 2 for v in incr.values()):
        fail("increment contains a non-LOSS verdict")
    row = incr.get(ADOPTED_KEY)
    if row is None or row != (2, ADOPTED_TOTAL_NODES):
        fail(f"increment row != the adopted aa003 verdict: {row}")
    incr_index = {ADOPTED_S5: ADOPTED_KEY}
    adopted_loss_ids = sorted(kid for kid, (lo, hi, _s, _m, _c) in batch_keys.items()
                              if (lo, hi) in incr)
    if adopted_loss_ids != ["aa003"]:
        fail(f"adopted LOSS ids {adopted_loss_ids} != ['aa003']")
    for kid, w in UNADOPTED_WINS.items():
        if incr.get(w["key"]) is not None:
            fail(f"{kid} WIN row leaked into the increment (adoption gate)")
    for kid, e in EXHAUSTED_IDS.items():
        if incr.get(e["key"]) is not None:
            fail(f"{kid} EXHAUSTED row leaked into the increment (honest UNKNOWN gate)")

    base_cache = read_cache(BASE_CACHE)
    scen_cache = read_cache(SCEN_CACHE)
    for kid, (lo, hi, s5i, _m, _cls) in batch_keys.items():
        if (lo, hi) in base_cache:
            fail(f"{kid} already present in the BASE cache (not a fresh increment)")
        if s5i in receipt_verdicts:
            fail(f"{kid} already resolved by the update8 receipt")
    if len(scen_cache) != len(base_cache) + ADOPTED_ROWS:
        fail(f"scenario cache row count != BASE + {ADOPTED_ROWS}")
    for key, (v, _n) in incr.items():
        srow = scen_cache.get(key)
        if srow is None or srow[0] != v:
            fail(f"scenario cache does not adopt increment row {key}")
    for key in scen_cache:
        if key not in base_cache and key not in incr:
            fail(f"scenario cache key outside BASE+increment: {key}")
    for key, (v, _n) in scen_cache.items():
        if key in base_cache and base_cache[key][0] != v:
            fail(f"scenario cache verdict drift on shared key {key}")
    base_votes = Counter(v for v, _ in base_cache.values())
    scen_votes = Counter(v for v, _ in scen_cache.values())
    if base_votes.get(1, 0) != 158 or base_votes.get(2, 0) != 6135:
        fail(f"BASE cache verdict counts not 158 WIN / 6135 LOSS: {dict(sorted(base_votes.items()))}")
    if scen_votes.get(1, 0) != 158 or scen_votes.get(2, 0) != 6136:
        fail(f"scenario cache verdict counts not 158 WIN / 6136 LOSS: {dict(sorted(scen_votes.items()))}")
    for kid, w in UNADOPTED_WINS.items():
        if w["key"] in scen_cache:
            fail(f"{kid} WIN key reached the scenario canonical cache (must stay unconsumed)")
    for kid, e in EXHAUSTED_IDS.items():
        if e["key"] in scen_cache:
            fail(f"{kid} EXHAUSTED key reached the scenario canonical cache (honest UNKNOWN)")

    # --- graph holders of the adopted key ----------------------------------
    holders = {}
    for kid, (lo, hi, s5i, _m, cls) in batch_keys.items():
        if kid not in adopted_loss_ids:
            continue
        hs = sorted(i for i, c in enumerate(s4_cost) if s5i in c)
        if cls not in hs:
            fail(f"{kid} own batch class {cls} not among its graph holders {hs}")
        for i in hs:
            if s4_status[i] not in (-1, 0, 1):
                fail(f"{kid} holder {i} unexpected graph status {s4_status[i]}")
        holders[kid] = hs
    holder_union = sorted(set().union(*[set(h) for h in holders.values()]))
    member_loss_counts = Counter()
    for hs in holders.values():
        for i in hs:
            member_loss_counts[i] += 1
    for kid, (lo, hi, s5i, mcnt, _cls) in batch_keys.items():
        if kid not in adopted_loss_ids:
            continue
        if len(holders[kid]) != int(mcnt):
            fail(f"{kid} graph holder count {len(holders[kid])} != batch-keys "
                 f"membership_class_count {mcnt}")

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
    if base_summary["inputs"]["cache_rows"] != 6293 or scen_summary["inputs"]["cache_rows"] != 6294:
        fail("published cache_rows not 6293 -> 6294")

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

    # --- per-class arithmetic gates -------------------------------------------
    cls = B28_CLASS
    if cls in new_free:
        fail(f"class {cls} must NOT free: its WIN children stay unconsumed, so "
             "unknown cost children remain and the class stays unknown")
    if scen_st[cls] != "unknown":
        fail(f"class {cls} scenario status {scen_st[cls]} != unknown (WIN stays unconsumed)")
    basec = sorted(base_unknown[cls])
    if len(basec) != 54:
        fail(f"class {cls} BASE-unknown cost children {len(basec)} != 54")
    own_class_incr = sorted(j for j in incr_index if j in s4_cost[cls])
    if not set(own_class_incr) <= set(basec):
        fail(f"class {cls}: increment s5 indices not all BASE-unknown cost children of the class")
    leftover = sorted(set(basec) - set(own_class_incr))
    if len(leftover) != 53:
        fail(f"class {cls} leftover BASE-unknown children {len(leftover)} != 53")
    if sorted(scen_unknown[cls]) != leftover:
        fail(f"class {cls} scenario-unknown children != leftover arithmetic")
    batch_s5 = {v[2] for v in batch_keys.values()}
    if batch_s5 != set(basec):
        fail(f"class {cls}: batch key set != the 54 BASE-unknown cost children "
             f"(batch-only {sorted(batch_s5 - set(basec))[:5]}, "
             f"base-only {sorted(set(basec) - batch_s5)[:5]})")
    win_s5 = [UNADOPTED_WINS[k]["s5"] for k in ("aa001", "aa002", "aa006", "aa007")]
    if not set(win_s5) <= set(leftover):
        fail(f"class {cls}: unadopted WIN s5 indices {win_s5} not inside the leftover set")
    exhaust_s5 = [EXHAUSTED_IDS[k]["s5"] for k in ("aa004", "aa005")]
    if not set(exhaust_s5) <= set(leftover):
        fail(f"class {cls}: EXHAUSTED s5 indices {exhaust_s5} not inside the leftover set")
    class_rows = {str(cls): {
        "class_index": cls, "batch": 28,
        "base_unknown_children": len(base_unknown[cls]),
        "adopted_by_increment": len(own_class_incr),
        "leftover_unknown_children": len(leftover),
        "scenario_unknown_children": len(scen_unknown[cls]),
        "scenario_status": scen_st[cls],
        "unadopted_win_s5_in_leftover": win_s5,
        "exhausted_s5_in_leftover": exhaust_s5,
    }}

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
        if c == cls and len(own) != 1:
            fail("holder class 5343 must hold exactly the aa003 membership")
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
    if metrics["free_now_classes"]["delta"] != 0:
        fail("free_now class count must not change in a 1-LOSS non-closing adoption")
    if metrics["joint_greedy_union_size"]["delta"] != 0:
        fail("joint greedy union must not change (no newly free class)")
    if metrics["update8_resolved_count"]["delta"] != 1:
        fail("update8 resolved-count delta != 1")
    if metrics["probe_worklist_total"]["delta"] != -1:
        fail("probe worklist delta != -1 (the single adopted row leaves the worklist)")

    # --- update8 resolved-requirement delta, gated to the increment ----------
    base_resolved = set(base_summary["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    scen_resolved = set(scen_summary["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    lost = sorted(base_resolved - scen_resolved)
    if lost:
        fail(f"update8 resolutions lost: {lost}")
    newly_resolved = sorted(scen_resolved - base_resolved)
    if newly_resolved != [ADOPTED_S5]:
        fail(f"newly resolved s5 {newly_resolved} != the adopted aa003 s5 index [{ADOPTED_S5}]")
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

    # root 27 baseline stays 119/119 in both
    for name, pub in published.items():
        r0 = pub["roots"][0]
        if (r0["role"], r0["origin_first"], r0["thirds"], r0["free_thirds_now"], r0["uncovered"]) \
                != ("known-loss-baseline", 27, 119, 119, 0):
            fail(f"{name}: roots[0] not the 119/119 known-loss baseline: {r0}")
    for prc in (base_prc, scen_prc):
        if prc[("known-loss-baseline", 27)][:3] != (119, 119, 0):
            fail("baseline per-root row not 119/119")

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
    greedy_moved_rows = {}
    for (role, first), (thirds, bfree, buncov, big) in base_prc.items():
        sthirds, sfree, suncov, sig = scen_prc[(role, first)]
        if big != sig:
            greedy_moved_rows["|".join((role, str(first)))] = {"base": big, "scenario": sig}
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

    # --- per-root greedy movers (measured bookkeeping) ------------------------
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
        if row["delta"] != 0 and row["delta"] != -1:
            fail(f"per-root greedy delta for root {first} not 0/-1: {row}")
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
    closure_rows = {
        "scenario_first_row": scen_cc[0] if scen_cc else None,
        "classes": {},
        "churn": {},
        "anchors": {},
        "churn_gate": ("rank churn only: every churned class keeps recomputed BASE == "
                       "scenario status unknown, driven by the class-5343 remaining-"
                       "count change (54->53) moving 5343 ahead in the ranked table; "
                       "no class freed, none excluded, none entered the unknown "
                       "population"),
    }
    # class 5343: unknown_now 54 -> 53, rank 27 -> 19
    b_rows = [r for r in base_cc if int(r["class_index"]) == cls]
    s_rows = [r for r in scen_cc if int(r["class_index"]) == cls]
    if len(b_rows) != 1 or len(s_rows) != 1:
        fail("class 5343 must appear exactly once in BOTH closure-candidate tables")
    if int(b_rows[0]["unknown_now"]) != 54:
        fail(f"BASE closure row for class 5343 unknown_now {b_rows[0]['unknown_now']} != 54")
    if int(s_rows[0]["unknown_now"]) != 53:
        fail(f"scenario closure row for class 5343 unknown_now {s_rows[0]['unknown_now']} != 53")
    if scen_st[cls] != "unknown" or base_st[cls] != "unknown":
        fail("class 5343 recomputed status must stay unknown in BASE and scenario")
    closure_rows["classes"][str(cls)] = {
        "base_rank": int(b_rows[0]["class_rank"]), "base_unknown_now": 54,
        "scenario_rank": int(s_rows[0]["class_rank"]), "scenario_unknown_now": 53,
    }
    # rank churn: exactly the machine-declared mapping
    churn_actual = {}
    b_by_cls = {int(r["class_index"]): int(r["class_rank"]) for r in base_cc}
    s_by_cls = {int(r["class_index"]): int(r["class_rank"]) for r in scen_cc}
    for c, (b_rank, s_rank) in CHURN_RANK_EXPECT.items():
        if b_by_cls[c] != b_rank or s_by_cls[c] != s_rank:
            fail(f"closure rank churn drift at class {c}: "
                 f"{b_by_cls.get(c)}->{s_by_cls.get(c)} != {b_rank}->{s_rank}")
        churn_actual[str(c)] = {"base_rank": b_rank, "scenario_rank": s_rank}
    # every other class row is byte-identical in rank AND unknown_now
    b_full = {int(r["class_index"]): (int(r["class_rank"]), int(r["unknown_now"]))
              for r in base_cc}
    s_full = {int(r["class_index"]): (int(r["class_rank"]), int(r["unknown_now"]))
              for r in scen_cc}
    if set(b_full) != set(s_full):
        fail("closure table class set changed")
    for c in b_full:
        if c in CHURN_RANK_EXPECT:
            continue
        if b_full[c] != s_full[c]:
            fail(f"closure row for class {c} changed outside the declared churn: "
                 f"{b_full[c]} -> {s_full[c]}")
    closure_rows["churn"] = churn_actual
    # untouched anchor classes: 23101 (1), 1849 (1) stay rank-stable unknown
    # population anchors; 12643 (53) is pinned as rank 20 -> 21 by the churn map
    # above and unknown_now-stable - its gate lives in CHURN_RANK_EXPECT.
    for anchor, a_unk in ((23101, 1), (1849, 1)):
        if b_full[anchor] != s_full[anchor] or b_full[anchor][1] != a_unk:
            fail(f"anchor class {anchor} closure-row drift (must stay unknown_now {a_unk} "
                 "with unchanged rank in both tables)")
        closure_rows["anchors"][str(anchor)] = {
            "base_rank": b_full[anchor][0],
            "scenario_rank": s_full[anchor][0],
            "unknown_now": a_unk,
        }
    if b_full[12643][1] != s_full[12643][1] or b_full[12643][1] != 53:
        fail("class 12643 unknown_now must stay 53 in both closure tables "
             "(only its rank churns 20 -> 21)")
    closure_rows["anchors"]["12643"] = {
        "base_rank": b_full[12643][0], "scenario_rank": s_full[12643][0],
        "unknown_now": 53,
        "note": "rank churns per the declared map; unknown_now stays 53",
    }
    base_idx = {int(r["class_index"]) for r in base_cc}
    scen_idx = {int(r["class_index"]) for r in scen_cc}
    left = sorted(base_idx - scen_idx)
    entered = sorted(scen_idx - base_idx)
    for c in left + entered:
        if base_st.get(c) != "unknown" or scen_st.get(c) != "unknown":
            fail(f"closure-table churn class {c} changed recomputed status "
                 f"{base_st.get(c)} -> {scen_st.get(c)} (churn must be pure ranking bookkeeping)")
    closure_rows["left_table_classes"] = left
    closure_rows["entered_table_classes"] = entered

    # --- output --------------------------------------------------------------
    out = {
        "schema": "n11-b28loss1-adoption-decomp-deltas-v1",
        "scenario": ("ADOPTED-CANONICAL = pre-adoption BASE (canonical 6,293 rows, Part "
                     "BZ reaudit state) + the single LOSS row aa003 of batch-28 (class "
                     "5343; s5 104943; nodes 4,070,373); full != loss: the resolved "
                     "packet additionally holds the 4 WIN rows (aa001/aa002 Part CC "
                     "cross-verified, aa006/aa007 Part CG lane declared, honest labels), "
                     "which stay UNCONSUMED (scrutiny owner C++ second-implementation "
                     "gate pin 9193f5b6...; batch-14residual q042 / batch-26 l028 "
                     "precedents), the 2 EXHAUSTED rows aa004/aa005 stay honest "
                     "UNKNOWN, and the batch keeps its 47 fileless UNPROBED keys; "
                     "class 5343 does not free"),
        "interpretation_guard": ("canonical single-row adoption deltas: only the 1 LOSS "
                                 "row aa003 is consumed into the canonical cache via "
                                 "the fail-closed union merger; the aa001/aa002/aa006/"
                                 "aa007 WIN verdicts are NOT consumed (the unconsumed "
                                 "closure WIN candidates stay untouched); the "
                                 "aa004/aa005 EXHAUSTED rows stay honest UNKNOWN; class "
                                 "5343 does NOT free in this adoption; scheduling "
                                 "quantities are bookkeeping; every claim stays "
                                 "UNKNOWN; 11x11 empty board and all 19 roots stay "
                                 "UNKNOWN; nodes are bookkeeping"),
        "recompute_gates": ("class statuses with Board free-candidate child verification, "
                            "known-universe counts and per-root free coverage were "
                            "recomputed from graph + update8 + cache and asserted equal "
                            "to the published BASE (Part BZ reaudit) and scenario "
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
            "batch28_keys_sha256": B28_KEYS_SHA,
            "batch28_row_audit_sha256": B28_ROW_AUDIT_SHA,
        },
        "batch_keys": {
            "count": 54, "adopted_loss": 1, "unadopted_win": 4, "exhausted_excluded": 2,
            "b28_class": B28_CLASS, "b28_keys": 54, "b28_adopted": 1, "b28_win": 4,
            "b28_exhausted": 2, "b28_fragments": 0, "b28_fileless_unprobed": 47,
            "b28_class_mask": list(s4_masks[B28_CLASS]),
            "b28_cost_children_total": len(s4_cost[B28_CLASS]),
            "b28_groups_served": [list(x) for x in groups_served],
        },
        "excluded_now_flips": flips,
        "newly_free_now_classes": new_free,
        "newly_free_now_gate": ("the loss-only packet can only free classes whose "
                                "BASE-unknown children are ALL resolved by the "
                                "increment; machine-computed list is empty here; "
                                "class 5343 does NOT free (its 4 WIN children and the "
                                "2 EXHAUSTED + 47 fileless keys stay unconsumed/"
                                "unprobed/unknown)"),
        "status_transitions": dict(sorted(transitions.items())),
        "class_rows": class_rows,
        "unadopted_win_rows": [
            {"key_id": kid, "s5_index": w["s5"], "key": [w["key"][0], w["key"][1]],
             "result": 1, "nodes": w["nodes"], "consumed": False,
             "note": ("honest WIN label only; adopted nowhere; stays unconsumed with the "
                      "unconsumed closure WIN candidates; scrutiny owner C++ "
                      "second-implementation gate pin 9193f5b6... decides; "
                      + w["cross"])}
            for kid, w in UNADOPTED_WINS.items()],
        "exhausted_rows": [
            {"key_id": kid, "s5_index": e["s5"], "key": [e["key"][0], e["key"][1]],
             "result": 0, "nodes": BUDGET, "consumed": False, "probed": True,
             "note": ("budget exhaustion at 15M on both passes; honest UNKNOWN; "
                      "same-condition re-probe not performed; adopted nowhere; the "
                      "completeness guard re-runs any truncated pass fresh-cold")}
            for kid, e in EXHAUSTED_IDS.items()],
        "fragment_rows": [],
        "newly_free_thirds": newly_free_thirds,
        "changed_per_root_coverage_rows": changed_rows,
        "individual_greedy_union_movers": greedy_moved_rows,
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
    print("OK decomp-deltas-b28loss1-adoption.json: "
          f"flips={flips} new_free={new_free} "
          f"free_now {metrics['free_now_classes']['base']}->{metrics['free_now_classes']['scenario']} "
          f"class5343_unknown {len(base_unknown[cls])}->{len(scen_unknown[cls])} "
          f"(4 WIN unconsumed + 2 EXHAUSTED honest UNKNOWN) "
          f"update8_resolved +{len(newly_resolved)} "
          f"joint_greedy {metrics['joint_greedy_union_size']['base']}->{metrics['joint_greedy_union_size']['scenario']} "
          f"worklist {metrics['probe_worklist_total']['base']}->{metrics['probe_worklist_total']['scenario']} "
          f"changed_rows={sorted(changed_rows)} "
          f"greedy_movers={sorted(greedy_moved_rows)} "
          f"churn5343={b_full[cls][0]}->{s_full[cls][0]} "
          f"closure_churn left={left} entered={entered}")


if __name__ == "__main__":
    main()
