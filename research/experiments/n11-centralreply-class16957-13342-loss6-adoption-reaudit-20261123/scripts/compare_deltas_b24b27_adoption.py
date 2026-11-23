#!/usr/bin/env python3
"""Batch-24 (class 16957) + batch-27 (class 13342) joint 6-LOSS canonical-adoption
reaudit delta extractor (Part BZ).

Fail-closed, read-only audit executing the single-owner Part BZ declaration
(note amendment 2026-11-23; no takeover - single owner).  Compares the
published BASE refresh outputs (Part BU reaudit on the canonical cache
e32a2e44..., 6,287 rows, itself the Part BI batch-20 chain) against the
single post-adoption computation:

  ADOPTED-CANONICAL = BASE + the 6 resolved LOSS rows
  ({y002, y004} of batch-24 / class 16957 + {o001, o003, o005, o007} of
  batch-27 / class 13342)

Neither packet is a complete enumeration book: batch-24 probed 4/53 keys
(pre-registered WIN-HALT; the published 2 WIN-HALT pairs y001 and y006),
batch-27 probed 5/54 (the o002 WIN-HALT pair; the o009 fragment is
bookkeeping only, UNPROBED); the fileless unprobed keys (49 + 48) are
untouched.  The WIN rows y001 (s5 91296) and y006 (s5 368510) (batch-24,
third-implementation cross-verified in Part BW) and o002 (s5 209134)
(batch-27, cross-verified in Part BY) are HONEST LABELS ONLY and NOT
adopted - they stay unconsumed (scrutiny owner C++ second-implementation
gate pin 9193f5b6...; batch-14residual q042 / batch-26 l028 precedents),
so full != loss for both packets and NEITHER class 16957 NOR class 13342
frees in this adoption.  The adopted packet is loss-only and can free NO
class unless all BASE-unknown cost children of the class are resolved
(machine-gated below); class 16957 keeps the y001/y006 WIN children plus
51 unknowns, class 13342 keeps o002 plus 50 unknowns.

Gates (fail-closed, machine-checked):

  * sha256 pins: increment, scenario cache, base cache, base summary,
    scenario summary, base closure-classes.csv, base per-root-coverage.csv,
    scenario closure-classes.csv, scenario per-root-coverage.csv,
    both batch-keys files, both row-audit-winhalt files;
  * manifest: 6 adopted LOSS / 3 unadopted WIN (y001/y006/o002) /
    0 exhausted / probed 4+5 with the fragment o009 UNPROBED,
    loss_ids == the 6 adopted ids, resolved_ids == the 9 probed ids,
    win_ids == unadopted_win_ids == [y001, y006, o002],
    full_packet_eq_loss_only FALSE, win_scenario_exists TRUE,
    per-batch loss sha == increment sha, per-batch stop records pinned,
    per-batch adopted-row node totals pinned (850,035 / 13,967,778 per pass);
  * both published row-audit-winhalt summaries agree with the manifest
    and the pinned keys (schema, class, batch, probed, loss/win rows,
    fragment o009 bookkeeping, mismatches 0, input pins);
  * independent two-pass raw re-verification of all 9 probed keys: both
    raws agree on (stones, legal, is_or, budget, result, nodes, lo, hi),
    every adopted key is result 2 (LOSS), the 3 WIN keys are result 1
    (the published honest labels with their published node counts), each
    key agrees with its batch-keys; the fragment o009 is asserted
    bookkeeping-only (p1 complete single pass flagged by the row-audit,
    p2 truncated, NO status.log row, NOT adopted, NOT in any cache);
  * the 6 increment keys exist, are canonical, unquarantined, absent
    from the BASE cache and the update8 receipt, map to their published
    s5 indices, are BASE-unknown cost children of their own class, and
    the 3 WIN keys are asserted NOT in the increment, NOT in BASE, NOT
    in the receipt (stay unconsumed);
  * scenario cache == BASE rows + increment rows with verdict agreement
    (6,287 -> 6,293: WIN 158 / LOSS 6,135);
  * every recomputed status transition is one of
    excluded->excluded, excluded_now->excluded_now, free_now->free_now,
    unknown->{unknown, free_now};
  * excluded_now flip set EMPTY (a loss-only increment cannot flip), and
    no excluded_now regression;
  * newly free_now classes == exactly the classes whose BASE-unknown cost
    children are ALL resolved by the increment (computed, not hardcoded)
    AND neither class 16957 nor class 13342 is among them (their WIN
    children stay unconsumed) AND their scenario statuses stay "unknown";
  * per class: BASE-unknown cost children == the batch key set (53 / 54),
    own-class adopted membership (2 / 4), leftover arithmetic ==
    scenario-unknown children, the unadopted WIN s5 indices (91296,
    368510 / 209134) are inside the leftover and NOT in the increment;
  * every graph holder class of the 6 keys: scenario unknown_now ==
    BASE unknown_now - own membership in the increment;
  * update8 newly-resolved baseline requirements must lie inside the
    increment universe, no resolution lost, count arithmetic consistent;
  * per-root coverage recomputed from the graph matches the published
    per-root-coverage.csv for BASE and scenario; root 27 stays 119/119;
    with no newly free class, no changed per-root free/uncovered row may
    exist (the individual greedy union column is scheduling bookkeeping
    and its measured movers are recorded, never gated as verdicts);
  * closure-candidate table: classes 16957 and 13342 must be present in
    BOTH tables (BASE unknown_now 53 -> 51 and 54 -> 50; ranks and rows
    recorded from the published rows), classes 23101 (1), 1849 (1) and
    12643 (53) must stay untouched in both tables as anchors; every class
    that left or entered the ranked candidate table must keep its
    recomputed BASE == scenario status "unknown" (the table membership
    churn is pure scheduling/ranking bookkeeping caused by the class
    remaining-count changes, never a status change).

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
OUT = EXP / "output/decomp-deltas-b24b27-adoption.json"

GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_DIR = ROOT / "research/experiments/n11-centralreply-class1849-loss52-adoption-reaudit-20261123/reaudit/output"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class1849-loss52-adoption-reaudit-20261123/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-plus-batch20loss53-plus-batch26loss52-20261123.cache"
BATCH24_DIR = ROOT / "research/experiments/n11-centralreply-closure-class16957-batch24-20261123"
BATCH27_DIR = ROOT / "research/experiments/n11-centralreply-closure-class13342-batch27-20261123"
SCEN_OUT = EXP / "reaudit/output"
INCR_CACHE = EXP / "output/increment-b24b27-loss6-20261123.cache"
MANIFEST = EXP / "output/increments-manifest.json"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-plus-batch20loss53-plus-batch26loss52-plus-batch24loss2-plus-batch27loss4-20261123.cache"

INCR_SHA = "1d8556c128e09fa8d41a22d749af5a28dd4babf30c33d6317cb29af5cdd22074"
SCEN_CACHE_SHA = "9115be9eca1e60828a90c50041f511b598ef79fc0be76d5e16821816e478e93e"
BASE_CACHE_SHA = "e32a2e442e77799ea36194f675baeb2424f3410a1d3e681b4c4fbb389f66fe93"
BASE_SUMMARY_SHA = "51d6bf0dd6a7d73cc2824a692cf6b086849e5f7945509b9e72c6177ce7599101"
SCEN_SUMMARY_SHA = "fca242cc767f4e30b1d450a3b10cbd524b18b96f28b4cc4ba83c8762f8bb2ff2"
BASE_CLOSURE_SHA = "e54a0eb831da6ade5cb5c35281713225d50039eb42c7254c50d25ddefd28cd50"
BASE_PRC_SHA = "c1cb1bf52594eb810fe17cb6e9af0fdfc2791f39f0bb7551aa30c8c608a312fd"
SCEN_CLOSURE_SHA = "14fc37c3a6f5c6753cac72a094d2c7693defb4a5e483558b3b87a42016b679d9"
SCEN_PRC_SHA = "4218a6b49f8dd4df41f9bb3b746c7f2a32afeb3e22d175243e9319c8f46ca56a"
B24_KEYS_SHA = "486858d6e2de0662ef38a6ff1fd61c1c0dcf6e9b09012c2c32fdd99153d096cc"
B27_KEYS_SHA = "67814ed6287d68d6e97212c931dce2b7ee585219e20b4d43edb621632220a014"
B24_ROW_AUDIT_SHA = "9d073038f99af68f5832e6b49de2f760356dbfddcbd468623b762cce1083c0d5"
B27_ROW_AUDIT_SHA = "530fe94712c79bc73f0df4933e2778bc90eb372675fcb7f5d9ca2d4236ac03ed"

SCENARIO = "ADOPTED-CANONICAL"
UNIVERSE_SIZE = 31859
RECEIPT_COUNT = 23
ADOPTED_ROWS = 6
B24_CLASS = 16957
B27_CLASS = 13342
UNADOPTED_WINS = {
    "y001": {"s5": 91296, "key": (10376293541461753856, 264), "legal": 87, "nodes": 5291064, "batch": 24},
    "y006": {"s5": 368510, "key": (1152921504607043584, 264), "legal": 84, "nodes": 5321639, "batch": 24},
    "o002": {"s5": 209134, "key": (3494793310856282144, 0), "legal": 79, "nodes": 4589084, "batch": 27},
}
FRAGMENT = {"kid": "o009", "s5": 420631, "key": (1188950301642588704, 0), "legal": 99, "batch": 27}
CLASS_INFO = {
    B24_CLASS: {"batch": 24, "keys_total": 53, "adopted": ["y002", "y004"],
                "probed": ["y001", "y002", "y004", "y006"],
                "dir": BATCH24_DIR, "keys_sha": B24_KEYS_SHA,
                "inputs_sha": B24_KEYS_SHA, "row_audit_sha": B24_ROW_AUDIT_SHA,
                "expected_base_unknown": 53, "expected_leftover": 51,
                "win_kids": ["y001", "y006"]},
    B27_CLASS: {"batch": 27, "keys_total": 54, "adopted": ["o001", "o003", "o005", "o007"],
                "probed": ["o001", "o002", "o003", "o005", "o007"],
                "dir": BATCH27_DIR, "keys_sha": B27_KEYS_SHA,
                "inputs_sha": B27_KEYS_SHA, "row_audit_sha": B27_ROW_AUDIT_SHA,
                "expected_base_unknown": 54, "expected_leftover": 50,
                "win_kids": ["o002"]},
}
LOSS_IDS = ["y002", "y004", "o001", "o003", "o005", "o007"]
RESOLVED_IDS = ["y001", "y002", "y004", "y006", "o001", "o002", "o003", "o005", "o007"]
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
                          ("batch-24 keys", BATCH24_DIR / "input/batch-keys.json", B24_KEYS_SHA),
                          ("batch-27 keys", BATCH27_DIR / "input/batch-keys.json", B27_KEYS_SHA),
                          ("batch-24 row-audit", BATCH24_DIR / "output/row-audit-winhalt.json", B24_ROW_AUDIT_SHA),
                          ("batch-27 row-audit", BATCH27_DIR / "output/row-audit-winhalt.json", B27_ROW_AUDIT_SHA)):
        got = sha(p)
        if got != want:
            fail(f"{name} sha256 drift: {got} != {want}")

    manifest = json.loads(MANIFEST.read_text())
    if manifest["schema"] != "b24b27-loss6-increments-manifest-v1":
        fail(f"manifest schema drift: {manifest['schema']}")
    rc = manifest["row_counts"]
    if not (rc["adopted_loss_rows"] == 6 and rc["wins"] == 3
            and rc["exhausted_excluded"] == 0 and rc["probed_rows"] == 9
            and rc["fragments_unprobed"] == 1 and rc["fileless_unprobed"] == 97):
        fail(f"manifest row_counts not the 6-LOSS / 3-WIN / 1-fragment picture: {rc}")
    if (manifest["win_ids"] != ["y001", "y006", "o002"]
            or manifest["unadopted_win_ids"] != ["y001", "y006", "o002"]
            or manifest["exhausted_excluded_ids"] != []):
        fail(f"manifest win/unadopted/exhaustion id lists drift: {manifest}")
    if manifest["loss_ids"] != LOSS_IDS:
        fail("manifest loss_ids != the 6 adopted ids")
    if manifest["resolved_ids"] != RESOLVED_IDS:
        fail("manifest resolved_ids != the 9 probed ids")
    if manifest["full_packet_eq_loss_only"] is not False or manifest["win_scenario_exists"] is not True:
        fail("manifest full != loss / WIN-scenario bookkeeping not asserted "
             "(3 WIN rows exist and are NOT adopted)")
    if manifest["sha256"]["loss"] != INCR_SHA:
        fail("manifest loss sha does not match the pinned increment")
    if manifest["merger_sha256"] != "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a":
        fail("manifest merger pin drift (the pinned fail-closed union merger)")
    per_batch_manifest = {b["batch"]: b for b in manifest["batches"]}
    if set(per_batch_manifest) != {24, 27}:
        fail("manifest batches != {24, 27}")
    for bid, cls in ((24, B24_CLASS), (27, B27_CLASS)):
        mb = per_batch_manifest[bid]
        ci = CLASS_INFO[cls]
        if mb["class_index"] != cls or mb["keys_total"] != ci["keys_total"]:
            fail(f"manifest batch-{bid} class/keys_total drift")
        if mb["adopted_loss_ids"] != ci["adopted"] or mb["unadopted_win_ids"] != ci["win_kids"]:
            fail(f"manifest batch-{bid} adopted/unadopted id lists drift")
        if sorted(mb["probed_ids"]) != sorted(ci["probed"]):
            fail(f"manifest batch-{bid} probed ids drift")
        if mb["input_sha256"] != ci["keys_sha"] or mb["row_audit_sha256"] != ci["row_audit_sha"]:
            fail(f"manifest batch-{bid} input/row-audit sha bookkeeping drift")
        if mb["total_nodes_pass_one"] != mb["total_nodes_pass_two"]:
            fail(f"manifest batch-{bid} pass node totals disagree")
        if len(mb["status_log_stop_records"]) != len(ci["win_kids"]):
            fail(f"manifest batch-{bid} stop-record count drift")
    if per_batch_manifest[24]["total_nodes_pass_one"] != 850035:
        fail("manifest batch-24 adopted-row node total drift (850,035 expected)")
    if per_batch_manifest[27]["total_nodes_pass_one"] != 13967778:
        fail("manifest batch-27 adopted-row node total drift (13,967,778 expected)")
    if per_batch_manifest[27]["fragment_state"].get("o009", {}).get("evidence") is not False:
        fail("manifest fragment o009 must be flagged bookkeeping-only (evidence false)")
    uwr = manifest["unadopted_win_rows"]
    if not (isinstance(uwr, list) and len(uwr) == 3):
        fail("manifest unadopted_win_rows must list the 3 honest WIN labels")
    for row in uwr:
        w = UNADOPTED_WINS[row["key_id"]]
        if not (row["s5_index"] == w["s5"] and (row["lo"], row["hi"]) == w["key"]
                and row["legal"] == w["legal"] and row["result"] == 1
                and row["nodes"] == w["nodes"] and row["two_pass_node_exact"] is True):
            fail(f"manifest unadopted WIN row bookkeeping drift: {row}")

    # both published row-audit-winhalt summaries agree with the manifest
    for bid, cls in ((24, B24_CLASS), (27, B27_CLASS)):
        ra = json.loads((CLASS_INFO[cls]["dir"] / "output/row-audit-winhalt.json").read_text())
        ci = CLASS_INFO[cls]
        if (ra["class_index"] != cls or ra["batch"] != bid
                or ra["keys_total"] != ci["keys_total"] or ra["probed"] != len(ci["probed"])
                or ra["loss_rows"] != ci["adopted"] or ra["win_rows"] != ci["win_kids"]
                or ra["exhausted_rows"] != [] or ra["mismatches"] != 0
                or ra["input_sha256"] != ci["keys_sha"]):
            fail(f"published row-audit (batch {bid}) not the published picture: {ra}")
    ra27 = json.loads((BATCH27_DIR / "output/row-audit-winhalt.json").read_text())
    frag27 = ra27["fragment_keys"].get("o009")
    if not frag27 or frag27["evidence"] is not False or frag27["probed"] is not False \
            or frag27["pass_pair_complete"] is not False or frag27["p1_complete_single_pass"] is not True:
        fail(f"published row-audit fragment o009 bookkeeping drift: {frag27}")

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
    batch_keys = {}
    class_groups = {}
    for cls, ci in CLASS_INFO.items():
        bk, groups_served = load_keys(ci["dir"], cls, ci["keys_total"])
        if [int(x) for x in bk["class_mask"]] != list(s4_masks[cls]):
            fail(f"batch-keys class_mask != graph mask of class {cls}")
        if len(bk["keys"]) != ci["keys_total"]:
            fail(f"class {cls} batch-keys count {len(bk['keys'])} != {ci['keys_total']}")
        class_groups[cls] = groups_served
        for k in bk["keys"]:
            kid = k["key_id"]
            lo, hi, s5i = int(k["lo"]), int(k["hi"]), int(k["s5_index"])
            if mask_to_index.get((lo, hi)) != s5i:
                fail(f"{kid} (lo,hi) does not map to its published s5 index {s5i}")
            if (lo, hi) in quarantined or not is_canonical_safe_s5_key((lo, hi)):
                fail(f"{kid} noncanonical or quarantined key")
            batch_keys[kid] = (lo, hi, s5i, int(k["membership_class_count"]), cls)
    if len(set(v[2] for v in batch_keys.values())) != len(batch_keys):
        fail("batch keys collide on s5 indices")

    # --- independent two-pass raw re-verification of ALL 9 probed keys ------
    # (second implementation of the maker's row gate; does not trust the maker;
    #  the 6 adopted keys must be LOSS, the 3 WIN keys must be honest labels)
    for kid, (lo, hi, s5i, _m, cls) in sorted(batch_keys.items()):
        if kid not in RESOLVED_IDS:
            continue
        ci = CLASS_INFO[cls]
        rows_raw = []
        for tag in ("p1", "p2"):
            p = ci["dir"] / f"output/raw/{kid}.{tag}.out"
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
        if kid in UNADOPTED_WINS:
            w = UNADOPTED_WINS[kid]
            if result != 1:
                fail(f"{kid} raw result {result} is not the published honest WIN label 1")
            if nodes != w["nodes"]:
                fail(f"{kid} nodes {nodes} != the published node count {w['nodes']}")
        elif result != 2:
            fail(f"{kid} raw result {result} is not LOSS - adopted rows must be result 2")
        if (klo, khi) != (lo, hi) or legal != int(
                next(k for k in json.loads((ci["dir"] / "input/batch-keys.json").read_text())["keys"]
                     if k["key_id"] == kid)["legal"]):
            fail(f"{kid} raw key/legal != batch-keys")

    # --- fragment o009: bookkeeping only, NOT probed ------------------------
    frags = [FRAGMENT["kid"]]
    p1f = BATCH27_DIR / f"output/raw/{FRAGMENT['kid']}.p1.out"
    p2f = BATCH27_DIR / f"output/raw/{FRAGMENT['kid']}.p2.out"
    txt1, txt2 = p1f.read_text(), p2f.read_text()
    if "# replay_done" not in txt1:
        fail("fragment o009.p1 must carry the '# replay_done' single-pass record (bookkeeping)")
    if "# replay_done" in txt2 or any(l.startswith("replay,") for l in txt2.splitlines()):
        fail("fragment o009.p2 must be the truncated pass (no replay row, no guard)")
    f1 = None
    for line in txt1.splitlines():
        if line.startswith("replay,"):
            parts = line.split(",")
            f1 = (int(parts[6]), int(parts[7]), int(parts[9]), int(parts[10]))
    if f1 is None or f1[2:] != FRAGMENT["key"] or f1[0] != 2:
        fail(f"fragment o009.p1 bookkeeping row drift: {f1}")
    if f1[0] != frag27["p1_result_bookkeeping"]:
        fail("fragment o009.p1 bookkeeping result != published row-audit record")
    FK = FRAGMENT["key"]
    if FK in read_cache(BASE_CACHE) or FK in read_cache(SCEN_CACHE) or FK in read_cache(INCR_CACHE):
        fail("fragment o009 key leaked into a cache (UNPROBED gate)")

    incr = read_cache(INCR_CACHE)
    if len(incr) != ADOPTED_ROWS:
        fail(f"increment row count {len(incr)} != {ADOPTED_ROWS}")
    if any(v[0] != 2 for v in incr.values()):
        fail("increment contains a non-LOSS verdict")
    incr_index = {}
    for kid, (lo, hi, s5i, _m, _cls) in batch_keys.items():
        row = incr.get((lo, hi))
        if row is None:
            continue
        if row[0] != 2:
            fail(f"{kid} increment row is not LOSS")
        incr_index[s5i] = (lo, hi)
    if set(incr) != {(lo, hi) for (lo, hi, _s, _m, _c) in batch_keys.values()
                     if (lo, hi) in incr}:
        fail("increment key set not contained in the two batch key sets")
    adopted_loss_ids = sorted(kid for kid, (lo, hi, _s, _m, _c) in batch_keys.items()
                              if (lo, hi) in incr)
    if sorted(LOSS_IDS) != adopted_loss_ids:
        fail(f"adopted LOSS ids {adopted_loss_ids} != the 6 declared ids")
    if len(incr_index) != 6:
        fail("adopted s5 index set != 6")
    for kid, w in UNADOPTED_WINS.items():
        if incr.get(w["key"]) is not None:
            fail(f"{kid} WIN row leaked into the increment (adoption gate)")

    base_cache = read_cache(BASE_CACHE)
    scen_cache = read_cache(SCEN_CACHE)
    for kid, (lo, hi, s5i, _m, _cls) in batch_keys.items():
        if kid in frags:
            continue
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
    if scen_votes.get(1, 0) != 158 or scen_votes.get(2, 0) != 6135:
        fail(f"scenario cache verdict counts not 158 WIN / 6135 LOSS: {dict(sorted(scen_votes.items()))}")
    for kid, w in UNADOPTED_WINS.items():
        if w["key"] in scen_cache:
            fail(f"{kid} WIN key reached the scenario canonical cache (must stay unconsumed)")

    # --- graph holders of the 6 adopted keys -------------------------------
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

    # --- per-class arithmetic gates -------------------------------------------
    class_rows = {}
    for cls, ci in CLASS_INFO.items():
        if cls in new_free:
            fail(f"class {cls} must NOT free: its WIN children stay unconsumed, so "
                 "unknown cost children remain and the class stays unknown")
        if scen_st[cls] != "unknown":
            fail(f"class {cls} scenario status {scen_st[cls]} != unknown (WIN stays unconsumed)")
        basec = sorted(base_unknown[cls])
        if len(basec) != ci["expected_base_unknown"]:
            fail(f"class {cls} BASE-unknown cost children {len(basec)} != {ci['expected_base_unknown']}")
        own_class_incr = sorted(j for j in incr_index if j in s4_cost[cls])
        if not set(own_class_incr) <= set(basec):
            fail(f"class {cls}: increment s5 indices not all BASE-unknown cost children of the class")
        leftover = sorted(set(basec) - set(own_class_incr))
        if len(leftover) != ci["expected_leftover"]:
            fail(f"class {cls} leftover BASE-unknown children {len(leftover)} != {ci['expected_leftover']}")
        if sorted(scen_unknown[cls]) != leftover:
            fail(f"class {cls} scenario-unknown children != leftover arithmetic")
        batch_s5 = {v[2] for v in batch_keys.values() if v[4] == cls}
        if batch_s5 != set(basec):
            fail(f"class {cls}: batch key set != the {ci['expected_base_unknown']} BASE-unknown "
                 f"cost children (batch-only {sorted(batch_s5 - set(basec))[:5]}, "
                 f"base-only {sorted(set(basec) - batch_s5)[:5]})")
        win_s5 = [UNADOPTED_WINS[k]["s5"] for k in ci["win_kids"]]
        if not set(win_s5) <= set(leftover):
            fail(f"class {cls}: unadopted WIN s5 indices {win_s5} not inside the leftover set")
        for k in ci["win_kids"]:
            if UNADOPTED_WINS[k]["s5"] in incr_index:
                fail(f"class {cls}: the {k} WIN s5 index is inside the increment (adoption gate)")
        class_rows[str(cls)] = {
            "class_index": cls, "batch": ci["batch"],
            "base_unknown_children": len(base_unknown[cls]),
            "adopted_by_increment": len(own_class_incr),
            "leftover_unknown_children": len(leftover),
            "scenario_unknown_children": len(scen_unknown[cls]),
            "scenario_status": scen_st[cls],
            "unadopted_win_s5_in_leftover": win_s5,
        }

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
    for kid, (lo, hi, s5i, mcnt, _cls) in batch_keys.items():
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
        "anchors": {},
        "churn_gate": ("left/entered classes are ranked-worklist best-option churn "
                       "only: every churned class keeps recomputed BASE == scenario "
                       "status unknown, driven by the class-16957/13342 remaining-"
                       "count changes (53->51, 54->50); no class freed, none "
                       "excluded, none entered the unknown population"),
    }
    class_expect = {
        B24_CLASS: (53, 51),  # (base unknown_now, scenario unknown_now)
        B27_CLASS: (54, 50),
    }
    for cls, (b_unk, s_unk) in class_expect.items():
        b_rows = [r for r in base_cc if int(r["class_index"]) == cls]
        s_rows = [r for r in scen_cc if int(r["class_index"]) == cls]
        if len(b_rows) != 1 or len(s_rows) != 1:
            fail(f"class {cls} must appear exactly once in BOTH closure-candidate tables "
                 f"(base {len(b_rows)} / scenario {len(s_rows)})")
        if int(b_rows[0]["unknown_now"]) != b_unk:
            fail(f"BASE closure row for class {cls} unknown_now {b_rows[0]['unknown_now']} != {b_unk}")
        if int(s_rows[0]["unknown_now"]) != s_unk:
            fail(f"scenario closure row for class {cls} unknown_now {s_rows[0]['unknown_now']} != {s_unk}")
        if scen_st[cls] != "unknown" or base_st[cls] != "unknown":
            fail(f"class {cls} recomputed status must stay unknown in BASE and scenario")
        closure_rows["classes"][str(cls)] = {
            "base_rank": int(b_rows[0]["class_rank"]), "base_unknown_now": b_unk,
            "scenario_rank": int(s_rows[0]["class_rank"]), "scenario_unknown_now": s_unk,
        }
    # untouched anchor classes: 23101 (1), 1849 (1), 12643 (53)
    for anchor, a_unk in ((23101, 1), (1849, 1), (12643, 53)):
        b_rows = [r for r in base_cc if int(r["class_index"]) == anchor]
        s_rows = [r for r in scen_cc if int(r["class_index"]) == anchor]
        if len(b_rows) != 1 or len(s_rows) != 1 \
                or int(b_rows[0]["unknown_now"]) != a_unk or int(s_rows[0]["unknown_now"]) != a_unk:
            fail(f"anchor class {anchor} closure-row drift (must stay unknown_now {a_unk} in both tables)")
        closure_rows["anchors"][str(anchor)] = {
            "base_rank": int(b_rows[0]["class_rank"]),
            "scenario_rank": int(s_rows[0]["class_rank"]),
            "unknown_now": a_unk,
        }
    base_idx = {int(r["class_index"]) for r in base_cc}
    scen_idx = {int(r["class_index"]) for r in scen_cc}
    left = sorted(base_idx - scen_idx)
    entered = sorted(scen_idx - base_idx)
    for c in left + entered:
        if base_st.get(c) != "unknown" or scen_st.get(c) != "unknown":
            fail(f"closure-table churn class {c} changed recomputed status "
                 f"{base_st.get(c)} -> {scen_st.get(c)} (churn must be pure ranking bookkeeping)")
    for cls in class_expect:
        if cls in left:
            fail(f"class {cls} left the closure-candidate table (a status artifact, not ranking churn)")
    closure_rows["left_table_classes"] = left
    closure_rows["entered_table_classes"] = entered

    # --- output --------------------------------------------------------------
    out = {
        "schema": "n11-b24b27-adoption-decomp-deltas-v1",
        "scenario": ("ADOPTED-CANONICAL = pre-adoption BASE (canonical 6,287 rows, Part BU "
                     "reaudit state) + the 6 LOSS rows of batch-24 (class 16957: y002, y004) "
                     "and batch-27 (class 13342: o001, o003, o005, o007); full != loss for "
                     "both packets: the resolved probed sets additionally hold the 3 WIN "
                     "rows (y001/y006/o002, honest labels), which stay UNCONSUMED "
                     "(scrutiny owner C++ second-implementation gate pin 9193f5b6...; "
                     "batch-14residual q042 / batch-26 l028 precedents), and both "
                     "batches keep their fileless UNPROBED keys; neither class frees"),
        "interpretation_guard": ("canonical joint adoption deltas: only the 6 LOSS rows are "
                                 "consumed into the canonical cache via the fail-closed "
                                 "union merger; the y001/y006/o002 WIN verdicts are NOT "
                                 "consumed (the unconsumed closure WIN candidates stay "
                                 "untouched); NEITHER class 16957 NOR class 13342 frees in "
                                 "this adoption; scheduling quantities are bookkeeping; "
                                 "every claim stays UNKNOWN; 11x11 empty board and all 19 "
                                 "roots stay UNKNOWN; nodes are bookkeeping"),
        "recompute_gates": ("class statuses with Board free-candidate child verification, "
                            "known-universe counts and per-root free coverage were "
                            "recomputed from graph + update8 + cache and asserted equal "
                            "to the published BASE (Part BU reaudit) and scenario "
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
            "batch24_keys_sha256": B24_KEYS_SHA,
            "batch27_keys_sha256": B27_KEYS_SHA,
            "batch24_row_audit_sha256": B24_ROW_AUDIT_SHA,
            "batch27_row_audit_sha256": B27_ROW_AUDIT_SHA,
        },
        "batch_keys": {
            "count": 107, "adopted_loss": 6, "unadopted_win": 3,
            "b24_class": B24_CLASS, "b24_keys": 53, "b24_adopted": 2, "b24_win": 2,
            "b27_class": B27_CLASS, "b27_keys": 54, "b27_adopted": 4, "b27_win": 1,
            "b24_class_mask": list(s4_masks[B24_CLASS]),
            "b27_class_mask": list(s4_masks[B27_CLASS]),
            "b24_cost_children_total": len(s4_cost[B24_CLASS]),
            "b27_cost_children_total": len(s4_cost[B27_CLASS]),
            "b24_groups_served": [list(x) for x in class_groups[B24_CLASS]],
            "b27_groups_served": [list(x) for x in class_groups[B27_CLASS]],
        },
        "excluded_now_flips": flips,
        "newly_free_now_classes": new_free,
        "newly_free_now_gate": ("the loss-only packet can only free classes whose "
                                "BASE-unknown children are ALL resolved by the "
                                "increment; machine-computed list is empty here; "
                                "classes 16957 and 13342 do NOT free (their WIN "
                                "children and fileless keys stay unconsumed/unprobed)"),
        "status_transitions": dict(sorted(transitions.items())),
        "class_rows": class_rows,
        "unadopted_win_rows": [
            {"key_id": kid, "s5_index": w["s5"], "key": [w["key"][0], w["key"][1]],
             "result": 1, "nodes": w["nodes"], "consumed": False,
             "note": ("honest WIN label only; adopted nowhere; stays unconsumed with the "
                      "unconsumed closure WIN candidates; scrutiny owner C++ "
                      "second-implementation gate pin 9193f5b6... decides; "
                      + ("Part BW" if w["batch"] == 24 else "Part BY")
                      + " third-impl + pinned-replica backing")}
            for kid, w in UNADOPTED_WINS.items()],
        "fragment_row": {
            "key_id": FRAGMENT["kid"], "s5_index": FRAGMENT["s5"],
            "key": [FRAGMENT["key"][0], FRAGMENT["key"][1]],
            "consumed": False, "probed": False, "evidence": False,
            "note": ("p1 complete single pass is bookkeeping only; p2 truncated; "
                     "UNPROBED and untouched by this Part"),
        },
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
    print("OK decomp-deltas-b24b27-adoption.json: "
          f"flips={flips} new_free={new_free} "
          f"free_now {metrics['free_now_classes']['base']}->{metrics['free_now_classes']['scenario']} "
          f"class16957_unknown {len(base_unknown[B24_CLASS])}->{len(scen_unknown[B24_CLASS])} "
          f"class13342_unknown {len(base_unknown[B27_CLASS])}->{len(scen_unknown[B27_CLASS])} "
          f"(3 WIN unconsumed) "
          f"update8_resolved +{len(newly_resolved)} "
          f"joint_greedy {metrics['joint_greedy_union_size']['base']}->{metrics['joint_greedy_union_size']['scenario']} "
          f"worklist {metrics['probe_worklist_total']['base']}->{metrics['probe_worklist_total']['scenario']} "
          f"changed_rows={sorted(changed_rows)} "
          f"greedy_movers={sorted(greedy_moved_rows)} "
          f"closure_churn left={closure_rows['left_table_classes']} entered={closure_rows['entered_table_classes']}")


if __name__ == "__main__":
    main()
