"""Part EC adoption delta extraction: BASE (Part EB, b3loss3 merged 6,663 rows)
vs SCENARIO (b33exh5loss2 = Part EA af003/af039 2-LOSS).

Fail-closed machine recomputation of exactly what the Part EC 2-LOSS canonical
adoption changed, from published bytes only:

* every published artifact sha-pinned (the published Part EB outputs -- the
  BASE canonical cache c3026468... 6,663 rows WIN 158 / LOSS 6,505, the BASE
  reaudit outputs refresh-summary 6ff36b6e... / closure-classes f2cf3c43... /
  per-root-coverage cad355a8... / probe-worklist regen pin 15f95053... -- the
  Part EC outputs -- increment 8f45a202..., increments manifest 9c89d3d8...,
  the 6,665-row scenario cache cecc1a0f... WIN 158 / LOSS 6,507 -- the
  merge-audits x3 (identical sha 47420bd0...), the byte-clone of the union
  merger 90711961..., graph/update8/board/policy/quarantine pins);
* the published Part EB refresh fork (reaudit/scripts/refresh_adoption_eb.py,
  sha b6b780a3...) and the published Part EC refresh fork (reaudit/scripts/
  refresh_adoption_ec.py, sha 73186e63...) are RE-EXECUTED byte-verbatim in
  isolated scratch trees against their pinned inputs, and all eight outputs
  must be byte-identical to the published / regenerated pins before any delta
  is emitted (double-run determinism; this simultaneously re-proves the
  published Part EB reaudit outputs are regenerable from published bytes);
* SCEN cache == BASE cache rows + exactly the 2 increment rows (verdict
  agreement everywhere; 6,665 rows, WIN 158 / LOSS 6,507); the re-probed Part
  EA packet at the pre-declared 30M condition is MIXED:
  full_packet_eq_loss_only=false, the probe-level WINs af023/af048 stay
  unconsumed (in NO cache), af034 stays EXHAUSTED honest-UNKNOWN / excluded;
* kit integrity: the published Part EA b33exh5 kit (61 files, MANIFEST
  42ba81bc...) verified file-by-file, the pinned jsreplay.js solver image
  (84585617...), the pinned runbatch 15M base (f591f8c2...) and derived 30M
  runner (3b5083b4...), the reprobe-keys input (3744b522...) and the
  batch-33 packet keys (8a863381...) pins;
* the class-34908 arithmetic is recomputed from the frozen dependency graph
  with the integer-geometry Board: the 56-child canonical boundary is
  regenerated (entirely inside the s5 mask universe; ZERO non-s5 children);
  47 children are known exact LOSS in BASE and SCEN; exactly 9 children are
  unknown in BASE and exactly 7 in SCEN == the 6 unconsumed probe-level WIN
  keys {af029, af047, af050, af053, af023, af048} plus the still-EXHAUSTED
  af034; class 34908 is NOT freed and NOT excluded (unknown 9 -> 7,
  rank 8 static, groups_served 5 static);
* classes 16371 and 20421 are proven BYTE-STATIC across this Part (no EC
  adopted key sits inside either boundary; their closure rows are
  byte-identical before/after);
* every closure-classes.csv row is compared: ZERO unknown_now changes beside
  class 34908; ZERO left/entered rows; ZERO rank-churn rows and ZERO
  groups_served churn (the 807-row table is fully static otherwise;
  806 fully stable rows);
* update8 refresh: BOTH adopted s5 indices (153030 / 950512) sit OUTSIDE the
  frozen update8 baseline requirement: resolved stays 259, remaining stays
  31,600, groups_free_now stays 131, the newly-resolved/lost sets are both
  EMPTY and every per-root remaining is byte-identical;
* class_status counts: excluded 390 / excluded_now 23 / free_now 39 /
  unknown 34,497 IDENTICAL before and after (the loss-only adoption frees
  nothing and excludes nothing); Board verification 39/39 with zero
  rejections on both sides; root 27 stays 119/119;
* per-root coverage: free/uncovered thirds are IDENTICAL at every root; the
  individual greedy union changes only at roots 0 and 12 (pure re-selection
  bookkeeping, no coverage claim);
* the frozen greedy scheduler deltas are recorded as bookkeeping (joint
  greedy 36,511 -> 36,509, worklist 64,417 -> 64,415, known universe
  842 -> 844, cache in universe 819 -> 821).

No unknown verdict is asserted anywhere.  The standard 11x11 empty board
and every one of the 19 central-reply roots stay UNKNOWN; free_now /
coverage quantities are scheduling bookkeeping derived from exact LOSS
verdicts, not root verdict claims.  The two probe-level WIN rows (af023 /
af048) are consumed NOWHERE by this Part (scrutiny-owner C++ second-
implementation gate pin 9193f5b6...); af034 stays honest UNKNOWN (EXHAUSTED
at the 30M condition, same-condition re-probe forbidden); no WIN verdict
and no EXHAUSTED verdict enters the canonical cache.
"""

import csv
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]

BASE_EXP = ROOT / "research/experiments/n11-centralreply-b3loss3-adoption-reaudit-20261125"
BASE_OUT = BASE_EXP / "reaudit/output"
BASE_CACHE = BASE_EXP / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-plus-b35loss26-plus-b4loss1-plus-b36loss40-plus-b37loss46-plus-b3loss3-20261125.cache"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-plus-b35loss26-plus-b4loss1-plus-b36loss40-plus-b37loss46-plus-b3loss3-plus-b33exh5loss2-20261125.cache"
INCR = EXP / "output/increment-b33exh5loss2-20261125.cache"
MANIFEST = EXP / "output/increments-manifest.json"
EA_KIT = ROOT / "research/experiments/n11-centralreply-closure-class34908-b33exh5-reprobe30m-20261125"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_REFRESH_SCRIPT = BASE_EXP / "reaudit/scripts/refresh_adoption_eb.py"
SCEN_REFRESH_SCRIPT = EXP / "reaudit/scripts/refresh_adoption_ec.py"
MERGER = EXP / "scripts/s5_union_merge.py"

BASE_CACHE_SHA = "c3026468c74b56e71f3a9e0cd45c13e4a8cba147d137c25703c5be62b9c4c94e"
SCEN_CACHE_SHA = "cecc1a0fae126d98d8e5f23e041657b86e4d7128f80cc1182f4f9830ed1e8626"
INCR_SHA = "8f45a202af94faa448ac5f39f061100e3370ce9397c475c98f75cc9ea30d04a1"
MANIFEST_SHA = "9c89d3d8ab37359693fbed00235763d1fe539c388637e3fc06432f1afcabe80c"
BASE_SUMMARY_SHA = "6ff36b6e02c3dc2b958be25af6af8d5adcb001aa7af8918173896bac73c9bf2e"
BASE_CLOSURE_SHA = "f2cf3c4373bd81a264b62956776e8e46e8506b90461c5e1dba8e0b8065b48c57"
BASE_PRC_SHA = "cad355a82af4450666ce23f605782e06e23bdb95baeb33fff8230af63558f439"
BASE_WORKLIST_SHA = "15f95053cf50ce9f388f4b267d5bcce2cbba2f4abaf80fc57d20dfa9ab28cbb1"
SCEN_SUMMARY_SHA = "936373e6f16cad2b5e0b08fe9177fc577a3f3a072397208aafd72f9ff0944651"
SCEN_CLOSURE_SHA = "0ae9749c2ef1319938bc1219136b287d98e1c56051f8e34dde076e8611340d35"
SCEN_PRC_SHA = "06cd656193b317c25cb1ec6dab4ea771ace93a43c74ce974c0e8897576acb389"
SCEN_WORKLIST_SHA = "36bc6c6c047dff1fa2e21d4d4ceb05eb0248213b039257ea20da6fd0d8cef9cd"
BASE_REFRESH_SHA = "b6b780a3fd3ef81a07a052c48002fa511f016b30cae3007f199283c6f87a3b7a"
SCEN_REFRESH_SHA = "73186e63037cfc8ee7a1266cc0686e827abad1cd2b5ee7d8270a60ae52dbece7"
MERGE_AUDIT_SHA = "47420bd02bfe0403caf9bbe2bbd6c2343a89c404563076180d4acc69dcf7b74c"
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
ADOPTED_TABLE_DIGEST = "7c74832f57c9b54a6b5606880ee8c40b7d563ad518cc04e96ef257b543172182"

EA_MANIFEST_SHA = "42ba81bc79dd887074dbc9514b87f0c9d1a656d53a98ff3dfef29b9c4666601e"
EA_KIT_FILES = 61
EA_REPROBE_KEYS_SHA = "3744b522346b00108f66991cd4009943af84344ab388431652783fbf8227a663"
EA_STATUS_SHA = "db7c7017d7bfeef2d0c17c646b22f77b8bfd52a66796433b86e88444741c0438"
EA_AUDIT_SHA = "5b83d166e0fb7842a0cad949404c572ba666b71a4cd87dd9e704ce97e543cff3"
EA_BATCH_KEYS_SHA = "8a863381454fcfec3cb190db7130ce6801accf56170ee3a1b944402491fecbaa"
B33_STATUS_SHA = "1f663fc802c03b27c2e39d6130cf6c1392d62dd99b5847d6af477cd823a94b52"
JSREPLAY_SHA = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
RUNBATCH_SHA = "f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84"
RUNNER30M_SHA = "3b5083b47c043f93bbe01a5f3335baba6be6d1d6929885f4ab5b28b1778cf7b4"
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
BOARD_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

CLASS_34908 = 34908
CLASS_16371 = 16371
CLASS_20421 = 20421
ADOPTED_ROWS = 2
UNCONSUMED_WIN_ROWS = 2
EXHAUSTED_EXCLUDED_ROWS = 1
ADOPTED_TOTAL_NODES = 42360304
PACKET_NODES = 119110099

ADOPTED_IDS = ["af003", "af039"]
WIN_IDS_UNCONSUMED = ["af023", "af048"]
EXHAUSTED_EXCLUDED_IDS = ["af034"]
PACKET_IDS = ["af003", "af023", "af034", "af039", "af048"]
ANCHOR_IDS = ["af001", "af029"]

ADOPTED_S5 = [153030, 950512]
NEWLY_RESOLVED_UPD8_S5 = []

# class 34908 (the single EC target)
BOUNDARY_34908_RAW = 56
BOUNDARY_34908_S5 = 56
BASE_KNOWN_LOSS_34908 = 47
UNKNOWN_BASE_34908 = 9
UNKNOWN_SCEN_34908 = 7
WIN_S5_PINNED_34908 = {"af029": 900646, "af047": 961976, "af050": 962386,
                       "af053": 962470, "af023": 810351, "af048": 962172}
EXH_S5_PINNED_34908 = {"af034": 930660}
WIN_NODES_PINNED = {"af023": 28933179, "af048": 17816616}
EXH_NODES_PINNED = {"af034": 30000000}
KEY_PINS = {
    "af001": (1152921504742113281, 68719476736),
    "af003": (3458764513821589505, 68719476736),
    "af023": (1152921504607895553, 68719478784),
    "af029": (1152921504607895553, 68720525312),
    "af034": (1152921504607911937, 68719476736),
    "af039": (1152921504607895681, 68719476736),
    "af047": (1152921504607895809, 68719476736),
    "af048": (1152921508902862849, 68719476736),
    "af050": (1152921504607899649, 68719476736),
    "af053": (1152921504606852096, 17660905521152),
}
EA_STATUS_LINES = 13
EA_STATUS_FIRST = "2026-11-25T02:33:51Z af001 PASS 30000000,2,2952432"
EA_STATUS_FINAL = "2026-11-25T03:00:04Z af048 WIN-HALT"
EA_STATUS_WIN_HALT_LINES = [
    "2026-11-25T02:34:39Z af029 WIN-HALT",
    "2026-11-25T02:46:09Z af023 WIN-HALT",
    "2026-11-25T03:00:04Z af048 WIN-HALT",
]
EA_STATUS_RETRY_LINES = [
    "2026-11-25T02:43:31Z af023 P2-TRUNCATED-RETRY",
    "2026-11-25T02:50:34Z af034 P2-TRUNCATED-RETRY",
]
EA_STATUS_EXHAUSTED_LINES = [
    "2026-11-25T02:53:19Z af034 EXHAUSTED 30000000,0,30000000",
]

STATUS_EXPECTED = {"excluded": 390, "excluded_now": 23, "free_now": 39, "unknown": 34497}
UPD8_RESOLVED_BEFORE = 259
UPD8_RESOLVED_AFTER = 259
UPD8_REMAINING_BEFORE = 31600
UPD8_REMAINING_AFTER = 31600
JOINT_GREEDY_BEFORE = 36511
JOINT_GREEDY_AFTER = 36509
WORKLIST_BEFORE = 64417
WORKLIST_AFTER = 64415
KNOWN_UNIVERSE_BEFORE = 842
KNOWN_UNIVERSE_AFTER = 844
CACHE_IN_UNIVERSE_BEFORE = 819
CACHE_IN_UNIVERSE_AFTER = 821
CACHE_VERDICTS_BEFORE = {"1": 158, "2": 6505}
CACHE_VERDICTS_AFTER = {"1": 158, "2": 6507}
UNIQUE_GROUPS_BEFORE = 2115
UNIQUE_GROUPS_AFTER = 2115
GROUP_BEST_NONFREE = 2115
PER_ROOT_REMAINING_DELTA = {}
PER_ROOT_COVERAGE_DELTA = {
    "0": {"free": [7, 7], "uncovered": [112, 112], "greedy": [3006, 3004]},
    "12": {"free": [6, 6], "uncovered": [113, 113], "greedy": [2893, 2891]},
}
CLOSURE_ROWS_BEFORE = 807
CLOSURE_ROWS_AFTER = 807
CLOSURE_LEFT = []
CLOSURE_ENTERED = []
CLASS_34908_ROW_BEFORE = {"class_rank": "8", "unknown_now": "9", "groups_served_count": "5"}
CLASS_34908_ROW_AFTER = {"class_rank": "8", "unknown_now": "7", "groups_served_count": "5"}
CLASS_16371_ROW = {"class_rank": "4", "unknown_now": "2", "groups_served_count": "3"}
CLASS_20421_ROW = {"class_rank": "7", "unknown_now": "6", "groups_served_count": "4"}
GS_CHURN_DECREASE = []
RANK_CHURN_ROWS = 0
FULLY_STABLE_ROWS = 806
CHANGED_CLASS_SET = []


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fail(msg: str):
    print(f"ABORT {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_cache(path: Path):
    cache = {}
    for row in csv.reader(path.open(encoding="utf-8-sig", newline="")):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 6 or row[0] != "s5verdict":
            fail(f"invalid cache row: {row}")
        cache[(int(row[1]), int(row[2]))] = (int(row[4]), int(row[5]))
    return cache


def verify_kit(dirp: Path, manifest_sha: str, files_expected: int):
    if sha(dirp / "MANIFEST-sha256.txt") != manifest_sha:
        fail(f"kit {dirp.name} MANIFEST sha drift")
    n = 0
    for line in (dirp / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split()
        if len(fields) >= 4:  # 4-column format: sha blobsha size relpath
            want, rel = fields[0], fields[3]
        else:                 # Part EA format: sha blobsha relpath
            want, rel = fields[0], fields[2]
        p = dirp / rel
        if not p.is_file():
            fail(f"kit {dirp.name} file missing: {rel}")
        if sha(p) != want:
            fail(f"kit {dirp.name} sha drift at {rel}")
        n += 1
    if n != files_expected:
        fail(f"kit {dirp.name} files {n} != {files_expected}")
    return n


def _read_keys(p: Path):
    d = json.loads(p.read_text())
    out = {}
    for e in d["keys"]:
        out[e["key_id"]] = (int(e["lo"]), int(e["hi"]))
    return out, d


def rerun_refresh(script: Path, script_sha: str, tmp_name: str):
    """Re-execute a published refresh script byte-verbatim in a scratch tree."""
    if sha(script) != script_sha:
        fail(f"refresh script sha drift: {script.name}")
    scratch = ROOT / "research/experiments" / tmp_name
    outdir = scratch / "reaudit"
    if scratch.exists():
        shutil.rmtree(scratch)
    (outdir / "scripts").mkdir(parents=True)
    (outdir / "output").mkdir()
    shutil.copyfile(script, outdir / "scripts" / script.name)
    if sha(outdir / "scripts" / script.name) != script_sha:
        fail("scratch copy of refresh script not byte-identical")
    proc = subprocess.run([sys.executable, str(outdir / "scripts" / script.name)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        fail(f"refresh re-execution failed ({script.name}): {proc.stderr[-400:]}")
    return outdir / "output"


def main() -> None:
    # --- sha pins over every published artifact ---------------------------
    pins = [
        ("base cache", BASE_CACHE, BASE_CACHE_SHA),
        ("scenario cache", SCEN_CACHE, SCEN_CACHE_SHA),
        ("increment", INCR, INCR_SHA),
        ("manifest", MANIFEST, MANIFEST_SHA),
        ("base refresh-summary", BASE_OUT / "refresh-summary.json", BASE_SUMMARY_SHA),
        ("base closure-classes", BASE_OUT / "closure-classes.csv", BASE_CLOSURE_SHA),
        ("base per-root-coverage", BASE_OUT / "per-root-coverage.csv", BASE_PRC_SHA),
        ("scenario refresh-summary", EXP / "reaudit/output/refresh-summary.json", SCEN_SUMMARY_SHA),
        ("scenario closure-classes", EXP / "reaudit/output/closure-classes.csv", SCEN_CLOSURE_SHA),
        ("scenario per-root-coverage", EXP / "reaudit/output/per-root-coverage.csv", SCEN_PRC_SHA),
        ("base refresh script", BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA),
        ("scenario refresh script", SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA),
        ("union merger byte-clone", MERGER, MERGER_SHA),
        ("graph", GRAPH, GRAPH_SHA),
        ("update8", UPDATE8, UPDATE8_SHA),
        ("board source", BOARD_SOURCE, BOARD_SHA),
        ("policy", POLICY, POLICY_SHA),
        ("quarantine", QUARANTINE, QUARANTINE_SHA),
        ("merge-audit run1", EXP / "output/merge-audit-run1.json", MERGE_AUDIT_SHA),
        ("merge-audit run2", EXP / "output/merge-audit-run2.json", MERGE_AUDIT_SHA),
        ("merge-audit run3", EXP / "output/merge-audit-run3.json", MERGE_AUDIT_SHA),
    ]
    for name, p, want in pins:
        got = sha(p)
        if got != want:
            fail(f"{name} sha drift: {got} != {want}")
    ea_files = verify_kit(EA_KIT, EA_MANIFEST_SHA, EA_KIT_FILES)
    if sha(EA_KIT / "scripts/jsreplay.js") != JSREPLAY_SHA:
        fail("jsreplay.js sha drift in the Part EA kit (pinned solver image 8458...)")
    if sha(EA_KIT / "scripts/runbatch.sh") != RUNBATCH_SHA:
        fail("runbatch 15M base sha drift in the Part EA kit (pinned f591...)")
    if sha(EA_KIT / "scripts/runbatch_afexh5-30m.sh") != RUNNER30M_SHA:
        fail("derived 30M runner sha drift in the Part EA kit (pinned 3b50...)")
    if sha(EA_KIT / "input/reprobe-keys.json") != EA_REPROBE_KEYS_SHA:
        fail("Part EA reprobe-keys sha drift")
    if sha(EA_KIT / "output/status.log") != EA_STATUS_SHA:
        fail("Part EA status.log sha drift")
    if sha(EA_KIT / "output/audit.json") != EA_AUDIT_SHA:
        fail("Part EA audit.json sha drift")
    if sha(EA_KIT / "input/batch-keys.json") != EA_BATCH_KEYS_SHA:
        fail("batch-33 packet keys sha drift (pinned 8a863381...)")
    if sha(EA_KIT / "sources/b33-status.log") != B33_STATUS_SHA:
        fail("published batch-33 honest-history status sha drift (source 1f66...)")

    # --- manifest decomposition ------------------------------------------
    manifest = json.loads(MANIFEST.read_text())
    if manifest["schema"] != "b33exh5loss2-increments-manifest-v1":
        fail("manifest schema drift")
    if manifest["base_cache_sha256"] != BASE_CACHE_SHA:
        fail("manifest base cache pin drift")
    if manifest["sha256"]["loss_increment"] != INCR_SHA:
        fail("manifest loss_increment pin drift")
    if manifest["merger_sha256"] != MERGER_SHA:
        fail("manifest merger pin drift")
    if manifest["adopted_table_digest_sha256"] != ADOPTED_TABLE_DIGEST:
        fail("manifest adopted-table digest drift")
    if manifest["base_cache_rows"] != 6663:
        fail("manifest base rows drift")
    if manifest["base_cache_absent_hits_for_emitted"] != 0:
        fail("manifest emitted rows must be absent from BASE (fresh increment)")
    if manifest["base_cache_prior_adoption_confirmed"] != 0:
        fail("manifest prior-adoption count drift")
    if manifest["quarantine_hits"] != 0:
        fail("manifest quarantine hits must be 0")
    if manifest["row_counts"] != {"adopted_loss_rows": 2, "exhausted_excluded": 1,
                                  "prior_adopted_loss_rows": 0, "wins_unconsumed": 2}:
        fail("manifest row_counts drift")
    if manifest["provenance"] != {"ea_kit_files": ea_files, "b33_status_lines": 66,
                                  "b33exh5_status_lines": EA_STATUS_LINES,
                                  "raws_published": True}:
        fail("manifest provenance drift")
    adopted_ids = manifest["loss_ids"]
    if adopted_ids != ADOPTED_IDS:
        fail(f"manifest adopted ids != the pinned adopted set: {adopted_ids}")
    if sorted(manifest["resolved_ids"]) != sorted(adopted_ids):
        fail("manifest resolved_ids != loss_ids")
    if manifest.get("full_packet_eq_loss_only") is not False:
        fail("the re-probed Part EA packet is MIXED: manifest full_packet_eq_loss_only must be false")
    if manifest.get("win_scenario_exists") is not True:
        fail("manifest win_scenario_exists must be true (2 probe-level WINs exist)")
    win_ids = manifest["unadopted_win_ids"]
    if sorted(win_ids) != sorted(WIN_IDS_UNCONSUMED):
        fail("manifest unconsumed WIN id set drift")
    if sorted(manifest["exhausted_excluded_ids"]) != sorted(EXHAUSTED_EXCLUDED_IDS):
        fail("manifest exhausted-excluded id set drift")
    win_rows = manifest["unadopted_win_rows"]
    if len(win_rows) != UNCONSUMED_WIN_ROWS:
        fail("manifest WIN row count drift")
    for w in win_rows:
        if w["verdict"] != "WIN" or w["key_id"] not in WIN_IDS_UNCONSUMED:
            fail(f"manifest WIN row identity drift: {w['key_id']}")
        if (w["lo"], w["hi"]) != KEY_PINS[w["key_id"]]:
            fail(f"manifest WIN row key drift: {w['key_id']}")
        if w["nodes"] != WIN_NODES_PINNED[w["key_id"]]:
            fail(f"manifest WIN row node drift: {w['key_id']}")
    exh_rows = manifest["exhausted_rows"]
    if len(exh_rows) != EXHAUSTED_EXCLUDED_ROWS:
        fail("manifest EXHAUSTED row count drift")
    for x in exh_rows:
        if x["verdict"] != "EXHAUSTED" or x["key_id"] not in EXHAUSTED_EXCLUDED_IDS:
            fail(f"manifest EXHAUSTED row identity drift: {x['key_id']}")
        if (x["lo"], x["hi"]) != KEY_PINS[x["key_id"]]:
            fail(f"manifest EXHAUSTED row key drift: {x['key_id']}")
        if x["nodes"] != EXH_NODES_PINNED[x["key_id"]]:
            fail(f"manifest EXHAUSTED row node drift: {x['key_id']}")
    if len(manifest["adopted_table"]) != ADOPTED_ROWS or any(r["result"] != 2 for r in manifest["adopted_table"]):
        fail("manifest adopted_table must be 2 exact-LOSS rows")
    if sum(r["nodes"] for r in manifest["adopted_table"]) != ADOPTED_TOTAL_NODES:
        fail("manifest adopted_table node sum drift")
    for b in manifest["batches"]:
        pool = b["pool"]
        if pool != "b33exh5":
            fail(f"unexpected pool {pool} in the EC manifest")
        if sorted(b["adopted_loss_ids"]) != sorted(ADOPTED_IDS):
            fail(f"pool {pool} adopted id set drift")
        if sorted(b["unadopted_win_ids"]) != sorted(WIN_IDS_UNCONSUMED):
            fail(f"pool {pool} unconsumed WIN id set drift")
        if sorted(b["exhausted_excluded_ids"]) != sorted(EXHAUSTED_EXCLUDED_IDS):
            fail(f"pool {pool} exhausted-excluded id set drift")
        if sorted(b["probed_ids"]) != sorted(PACKET_IDS):
            fail(f"pool {pool} probed != adopted + WIN + EXHAUSTED")
        if b["status_log_lines"] != EA_STATUS_LINES:
            fail(f"pool {pool} status-log honest-history line count drift")
        if b["status_log_first_line"] != EA_STATUS_FIRST or b["status_log_final_line"] != EA_STATUS_FINAL:
            fail(f"pool {pool} status-log first/final line drift")
        if b["status_log_win_halt_lines"] != EA_STATUS_WIN_HALT_LINES:
            fail(f"pool {pool} status-log WIN-HALT drift")
        if b["status_log_retry_lines"] != EA_STATUS_RETRY_LINES:
            fail(f"pool {pool} status-log retry-history drift")
        if b["status_log_exhausted_lines"] != EA_STATUS_EXHAUSTED_LINES:
            fail(f"pool {pool} status-log EXHAUSTED drift")
        if b["adopted_nodes_per_pool"] != ADOPTED_TOTAL_NODES:
            fail(f"pool {pool} adopted node total drift")
        if b["whole_packet_nodes"] != PACKET_NODES:
            fail(f"pool {pool} whole-packet node total drift")
        if b["reprobe_budget"] != 30000000 or b["source_budget"] != 15000000:
            fail(f"pool {pool} budget-condition pins drift")

    # --- refresh re-execution (double-run determinism) ---------------------
    base_tmp = rerun_refresh(BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA, ".ecverify-base-eb")
    scen_tmp = rerun_refresh(SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA, ".ecverify-scen")
    checks = [
        (base_tmp / "refresh-summary.json", BASE_OUT / "refresh-summary.json", BASE_SUMMARY_SHA),
        (base_tmp / "closure-classes.csv", BASE_OUT / "closure-classes.csv", BASE_CLOSURE_SHA),
        (base_tmp / "per-root-coverage.csv", BASE_OUT / "per-root-coverage.csv", BASE_PRC_SHA),
        (base_tmp / "probe-worklist.csv", None, BASE_WORKLIST_SHA),
        (scen_tmp / "refresh-summary.json", EXP / "reaudit/output/refresh-summary.json", SCEN_SUMMARY_SHA),
        (scen_tmp / "closure-classes.csv", EXP / "reaudit/output/closure-classes.csv", SCEN_CLOSURE_SHA),
        (scen_tmp / "per-root-coverage.csv", EXP / "reaudit/output/per-root-coverage.csv", SCEN_PRC_SHA),
        (scen_tmp / "probe-worklist.csv", None, SCEN_WORKLIST_SHA),
    ]
    for tmp_out, pub, want_sha in checks:
        if sha(tmp_out) != want_sha:
            fail(f"refresh re-execution output drift: {tmp_out.name} ({tmp_out.parent.parent.name})")
        if pub is not None and sha(pub) != want_sha:
            fail(f"published output drifted from pin: {pub}")
    shutil.rmtree(ROOT / "research/experiments/.ecverify-base-eb")
    shutil.rmtree(ROOT / "research/experiments/.ecverify-scen")

    # --- cache relation: SCEN == BASE + exactly the 2 increment rows -------
    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    incr = load_cache(INCR)
    if len(base) != 6663 or len(scen) != 6665 or len(incr) != ADOPTED_ROWS:
        fail(f"cache sizes drift: base {len(base)} scen {len(scen)} incr {len(incr)}")
    for key, row in incr.items():
        if row[0] != 2:
            fail(f"increment contains a non-LOSS row: {key}")
        if key in base:
            fail(f"increment key already in BASE: {key}")
        if scen.get(key) != row:
            fail(f"increment row not taken verbatim into scenario cache: {key}")
    merged = dict(base)
    for key, row in incr.items():
        merged[key] = row
    if merged != scen:
        fail("scenario cache != BASE rows + increment rows (set difference)")
    wins = sum(1 for v in scen.values() if v[0] == 1)
    losses = len(scen) - wins
    if (wins, losses) != (158, 6507):
        fail(f"scenario verdict counts {wins}/{losses} != 158/6,507")
    # the WIN discretization keys must not collide with any cache:
    tab = {(int(e["lo"]), int(e["hi"])): (e["legal"], e["result"], e["nodes"])
           for e in manifest["adopted_table"]}
    if set(tab) != set(incr) or len(tab) != 2:
        fail("manifest adopted_table keys != increment keys")
    for key, row in incr.items():
        if (row[0], row[1]) != (tab[key][1], tab[key][2]):
            fail(f"manifest adopted_table row != increment row: {key}")
    for kid in WIN_IDS_UNCONSUMED:
        if KEY_PINS[kid] in incr or KEY_PINS[kid] in base or KEY_PINS[kid] in scen:
            fail(f"the unconsumed WIN key {kid} must sit in NO cache (scrutiny gate owns it)")
    for kid in EXHAUSTED_EXCLUDED_IDS:
        if KEY_PINS[kid] in incr or KEY_PINS[kid] in base or KEY_PINS[kid] in scen:
            fail(f"the still-EXHAUSTED key {kid} must sit in NO cache (honest UNKNOWN)")
    for kid in ("af047", "af050", "af053"):
        if KEY_PINS[kid] in base or KEY_PINS[kid] in scen:
            fail(f"the unconsumed batch-33 WIN key {kid} must sit in NO cache")
    if KEY_PINS["af029"] in base or KEY_PINS["af029"] in scen or KEY_PINS["af029"] in incr:
        fail("the unconsumed batch-33 WIN key af029 must sit in NO cache")
    if KEY_PINS["af001"] not in base or base[KEY_PINS["af001"]] != (2, 2952432):
        fail("the published batch-33 LOSS anchor af001 must reproduce the BASE row verbatim")

    # --- Board arithmetic for classes 34908 / 16371 / 20421 -----------------
    sys.path.insert(0, str(BOARD_SOURCE.parent))
    sys.path.insert(0, str(POLICY.parent))
    from independent import Board  # noqa: E402
    from s5_evidence_policy import quarantined_cache_keys  # noqa: E402
    quarantined = quarantined_cache_keys()
    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s4_masks = g["s4_masks"]
    s5_masks = g["s5_masks"]
    mask_to_index = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}
    board = Board(11)
    update8 = json.loads(UPDATE8.read_text())
    receipt_verdicts = {int(k): int(v) for k, v in update8["resolved_s5_verdicts"].items()}
    adopted_keys = {KEY_PINS[k] for k in ADOPTED_IDS}
    if {mask_to_index[k] for k in adopted_keys} != set(ADOPTED_S5):
        fail("adopted s5 index set != the pinned adopted list")

    # --- class 34908 (the single EC target) ----------------------------------
    lo, hi = s4_masks[CLASS_34908]
    children = board.children(lo | (hi << 64))
    child_keys_34908 = {(c & ((1 << 64) - 1), c >> 64) for c in children}
    if len(child_keys_34908) != BOUNDARY_34908_RAW:
        fail(f"class-34908 Board child boundary {len(child_keys_34908)} != {BOUNDARY_34908_RAW}")
    non_s5 = [k for k in child_keys_34908 if k not in mask_to_index]
    if non_s5:
        fail("class-34908 boundary must have ZERO non-s5 children")
    in_s5_34908 = child_keys_34908
    if len(in_s5_34908) != BOUNDARY_34908_S5:
        fail(f"class-34908 in-s5 boundary {len(in_s5_34908)} != {BOUNDARY_34908_S5}")
    if not adopted_keys <= child_keys_34908:
        fail("the adopted keys must sit inside the class-34908 child boundary")
    receipt_child_34908 = {k for k in in_s5_34908 if mask_to_index[k] in receipt_verdicts}
    if receipt_child_34908:
        fail("class-34908 must have ZERO update8-receipt children")
    known_base_34908 = {k for k in in_s5_34908 if k in base}
    if len(known_base_34908) != BASE_KNOWN_LOSS_34908:
        fail(f"class-34908 BASE-known child count {len(known_base_34908)} != {BASE_KNOWN_LOSS_34908}")
    for k in known_base_34908:
        if base[k][0] != 2:
            fail("a BASE-known child of 34908 is not an exact LOSS")
    unknown_base_34908 = {k for k in in_s5_34908 if k not in base}
    if len(unknown_base_34908) != UNKNOWN_BASE_34908:
        fail(f"class-34908 BASE unknown count {len(unknown_base_34908)} != {UNKNOWN_BASE_34908}")
    want_base_unknown_s5 = sorted(ADOPTED_S5 + list(WIN_S5_PINNED_34908.values())
                                  + list(EXH_S5_PINNED_34908.values()))
    if sorted(mask_to_index[k] for k in unknown_base_34908) != want_base_unknown_s5:
        fail("BASE unknown children of 34908 != the pinned re-probe packet (2 adopted + 6 WIN + 1 EXH)")
    unknown_scen_34908 = {k for k in in_s5_34908 if k not in scen}
    if len(unknown_scen_34908) != UNKNOWN_SCEN_34908:
        fail(f"scenario unknown children of 34908 = {len(unknown_scen_34908)} != 7 (6 unconsumed WINs + af034; class NOT freed)")
    if unknown_scen_34908 != unknown_base_34908 - adopted_keys:
        fail("scenario unknown children of 34908 != BASE unknowns minus the adopted set")
    want_scen_unknown_s5 = sorted(list(WIN_S5_PINNED_34908.values())
                                  + list(EXH_S5_PINNED_34908.values()))
    if sorted(mask_to_index[k] for k in unknown_scen_34908) != want_scen_unknown_s5:
        fail("scenario unknown children of 34908 != the pinned unconsumed WIN s5 + the still-EXHAUSTED af034")
    own_34908 = in_s5_34908 & adopted_keys
    if own_34908 != adopted_keys:
        fail("class-34908 adopted-own set != exactly the 2 re-probe rows")
    for k in own_34908:
        if scen[k][0] != 2:
            fail(f"an adopted child of 34908 is not an exact LOSS in the scenario: {k}")
    if own_34908 & unknown_scen_34908:
        fail("adopted set collides with the unconsumed/EXHAUSTED set inside 34908")
    if any(k in quarantined for k in child_keys_34908):
        fail("a quarantined key sits inside the class-34908 child boundary")

    # --- classes 16371 and 20421 (must be BYTE-STATIC across this Part) ------
    for cls, row_pins in ((CLASS_16371, CLASS_16371_ROW), (CLASS_20421, CLASS_20421_ROW)):
        clo, chi = s4_masks[cls]
        kids = {(c & ((1 << 64) - 1), c >> 64) for c in board.children(clo | (chi << 64))}
        if adopted_keys & kids:
            fail(f"no adopted key may sit inside the class-{cls} boundary ({cls} is not EC-owned)")
        if any(k in quarantined for k in kids):
            fail(f"a quarantined key sits inside the class-{cls} boundary")
        for k in kids:
            if k in base and k in scen and base[k] != scen[k]:
                fail(f"class-{cls} child verdict drifted across EC")

    # --- update8 refresh deltas ---------------------------------------------
    base_summary = json.loads(BASE_OUT.joinpath("refresh-summary.json").read_text())
    scen_summary = json.loads((EXP / "reaudit/output/refresh-summary.json").read_text())
    rb = base_summary["frozen_update8_refresh"]
    rs = scen_summary["frozen_update8_refresh"]
    if rb["resolved_count"] != UPD8_RESOLVED_BEFORE or rs["resolved_count"] != UPD8_RESOLVED_AFTER:
        fail("update8 resolved_count drift vs pins")
    if rb["remaining_now"] != UPD8_REMAINING_BEFORE or rs["remaining_now"] != UPD8_REMAINING_AFTER:
        fail("update8 remaining_now drift vs pins")
    newly = sorted(set(rs["resolved_among_baseline_requirement"]) - set(rb["resolved_among_baseline_requirement"]))
    lost = set(rb["resolved_among_baseline_requirement"]) - set(rs["resolved_among_baseline_requirement"])
    if newly != NEWLY_RESOLVED_UPD8_S5 or lost:
        fail(f"update8 newly-resolved/lost sets must BOTH be empty (both adopted keys sit "
             f"outside the frozen baseline requirement): newly {newly} lost {sorted(lost)}")
    if set(ADOPTED_S5) & set(update8["required_new_s5"]):
        fail("adopted s5 indices must sit OUTSIDE the frozen update8 baseline requirement")
    if rb["groups_free_now"] != 131 or rs["groups_free_now"] != 131:
        fail("update8 groups_free_now drift (must stay 131 static)")

    # --- class status / universe metrics --------------------------------------
    cb, cs = base_summary["class_status_counts"], scen_summary["class_status_counts"]
    if cb != STATUS_EXPECTED or cs != STATUS_EXPECTED:
        fail(f"class status counts drift vs the pinned static transition: {cb} {cs}")
    if scen_summary["board_verification"] != {"free_candidates": 39, "board_verified_free": 39, "rejected": {}}:
        fail("scenario board verification shape drift")
    if base_summary["board_verification"] != {"free_candidates": 39, "board_verified_free": 39, "rejected": {}}:
        fail("base board verification shape drift")
    if scen_summary["inputs"]["cache_rows"] != 6665 or scen_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_AFTER \
            or scen_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_AFTER:
        fail("scenario inputs metrics drift")
    if base_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["cache_rows"] != 6663:
        fail("base inputs metrics drift")
    bcv = base_summary["inputs"]["cache_verdicts"]
    scv = scen_summary["inputs"]["cache_verdicts"]
    if bcv != CACHE_VERDICTS_BEFORE or scv != CACHE_VERDICTS_AFTER:
        fail("cache verdict counts drift")
    if rs.get("win_hit_groups", rb.get("win_hit_groups")) not in ([], None):
        fail("win_hit_groups non-empty (a WIN was consumed)")

    # per-root coverage: free/uncovered thirds identical at EVERY root
    prc_pairs = list(zip(
        csv.DictReader(BASE_OUT.joinpath("per-root-coverage.csv").open()),
        csv.DictReader((EXP / "reaudit/output/per-root-coverage.csv").open())))
    prc_delta = {}
    for b, s in prc_pairs:
        if b["first"] != s["first"]:
            fail("per-root rows misaligned")
        if b["free_now"] != s["free_now"] or b["uncovered"] != s["uncovered"] \
                or b["individual_greedy_union"] != s["individual_greedy_union"]:
            prc_delta[s["first"]] = {
                "free": [int(b["free_now"]), int(s["free_now"])],
                "uncovered": [int(b["uncovered"]), int(s["uncovered"])],
                "greedy": [int(b["individual_greedy_union"]), int(s["individual_greedy_union"])],
            }
    if prc_delta != PER_ROOT_COVERAGE_DELTA:
        fail(f"per-root coverage delta {prc_delta} != the pinned re-selection churn")
    for root, d in prc_delta.items():
        if d["free"][0] != d["free"][1] or d["uncovered"][0] != d["uncovered"][1]:
            fail(f"root {root} free/uncovered thirds changed although no class was freed")
    root27 = [s for b, s in prc_pairs if s["first"] == "27"][0]
    if root27["free_now"] != "119" or root27["uncovered"] != "0":
        fail("root 27 coverage regressed")
    rb_pr = rb["per_root_remaining"]
    rs_pr = rs["per_root_remaining"]
    deltas = {k: rs_pr[k] - rb_pr[k] for k in rb_pr if rs_pr[k] != rb_pr[k]}
    if deltas != PER_ROOT_REMAINING_DELTA:
        fail(f"per-root remaining delta {deltas} != pinned {PER_ROOT_REMAINING_DELTA}")
    if any(v > 0 for v in deltas.values()):
        fail("a per-root remaining INCREASED (coverage regression)")

    # --- closure-classes table diff --------------------------------------------

    def read_closure(p: Path):
        rows = {}
        for r in csv.DictReader(p.open()):
            rows[int(r["class_index"])] = r
        return rows

    cb_t = read_closure(BASE_OUT / "closure-classes.csv")
    cs_t = read_closure(EXP / "reaudit/output/closure-classes.csv")
    if len(cb_t) != CLOSURE_ROWS_BEFORE or len(cs_t) != CLOSURE_ROWS_AFTER:
        fail(f"closure table row counts {len(cb_t)}/{len(cs_t)} != {CLOSURE_ROWS_BEFORE}/{CLOSURE_ROWS_AFTER}")
    left = sorted(set(cb_t) - set(cs_t))
    entered = sorted(set(cs_t) - set(cb_t))
    if left != CLOSURE_LEFT or entered != CLOSURE_ENTERED:
        fail(f"closure table left/entered must be EMPTY (static 807-row table): {left} / {entered}")
    if CLASS_34908 not in cb_t or CLASS_34908 not in cs_t:
        fail("class 34908 must remain in BOTH closure tables (not freed, not excluded)")
    for col, want in CLASS_34908_ROW_BEFORE.items():
        if cb_t[CLASS_34908][col] != want:
            fail(f"base class-34908 row {col} drift: {cb_t[CLASS_34908][col]} != {want}")
    for col, want in CLASS_34908_ROW_AFTER.items():
        if cs_t[CLASS_34908][col] != want:
            fail(f"scenario class-34908 row {col} drift: {cs_t[CLASS_34908][col]} != {want}")
    if int(cb_t[CLASS_34908]["unknown_now"]) - int(cs_t[CLASS_34908]["unknown_now"]) != len(own_34908) or len(own_34908) != 2:
        fail("class-34908 unknown delta != its own adopted children (Board boundary)")
    if CLASS_16371 not in cb_t or CLASS_16371 not in cs_t:
        fail("class 16371 must remain in BOTH closure tables (not freed, not excluded)")
    if cb_t[CLASS_16371] != cs_t[CLASS_16371]:
        fail("class-16371 full row must be byte-identical before/after (not EC-owned)")
    for col, want in CLASS_16371_ROW.items():
        if cs_t[CLASS_16371][col] != want:
            fail(f"class-16371 row {col} drift: {cs_t[CLASS_16371][col]} != {want}")
    if CLASS_20421 not in cb_t or CLASS_20421 not in cs_t:
        fail("class 20421 must remain in BOTH closure tables (not freed, not excluded)")
    if cb_t[CLASS_20421] != cs_t[CLASS_20421]:
        fail("class-20421 full row must be byte-identical before/after (not EC-owned)")
    for col, want in CLASS_20421_ROW.items():
        if cs_t[CLASS_20421][col] != want:
            fail(f"class-20421 row {col} drift: {cs_t[CLASS_20421][col]} != {want}")
    changed, rank_churn, stable, gs_dec, gs_bad = [], 0, 0, [], []
    rank_churn_classes = []
    for ci, brow in sorted(cb_t.items()):
        if ci == CLASS_34908 or ci not in cs_t:
            continue
        srow = cs_t[ci]
        diff = {k: (brow[k], srow[k]) for k in brow if brow[k] != srow[k]}
        if not diff:
            stable += 1
            continue
        if set(diff) == {"class_rank"}:
            rank_churn += 1
            rank_churn_classes.append((ci, int(brow["class_rank"]), int(srow["class_rank"])))
            continue
        if set(diff) == {"class_rank", "groups_served_count"}:
            gs_dec.append({
                "class_index": ci,
                "class_rank": [int(diff["class_rank"][0]), int(diff["class_rank"][1])],
                "groups_served_count": [int(diff["groups_served_count"][0]),
                                        int(diff["groups_served_count"][1])],
                "unknown_now": [int(brow["unknown_now"]), int(srow["unknown_now"])],
            })
            continue
        if "unknown_now" not in diff:
            fail(f"class {ci} changed unexpected columns: {diff}")
        b_unk, s_unk = int(diff["unknown_now"][0]), int(diff["unknown_now"][1])
        clo, chi = s4_masks[ci]
        kids = board.children(clo | (chi << 64))
        kids_keys = {(c & ((1 << 64) - 1), c >> 64) for c in kids}
        own = len(kids_keys & adopted_keys)
        if (b_unk - s_unk) != own or own == 0:
            fail(f"class {ci} unknown delta {b_unk}->{s_unk} != own adopted membership {own}")
        changed.append({"class_index": ci, "unknown_before": b_unk, "unknown_after": s_unk,
                        "own_adopted": own})
    if changed != CHANGED_CLASS_SET:
        fail(f"changed-class set != the pinned EMPTY set: {changed}")
    if rank_churn != RANK_CHURN_ROWS or stable != FULLY_STABLE_ROWS:
        fail(f"rank churn {rank_churn}/stable {stable} != pinned {RANK_CHURN_ROWS}/{FULLY_STABLE_ROWS}")
    if rank_churn_classes:
        fail(f"rank-churn rows must be EMPTY: {rank_churn_classes}")
    for e in gs_dec:
        if e["unknown_now"][0] != e["unknown_now"][1]:
            fail(f"groups_served_churn class {e['class_index']} changed unknown_now: {e}")
    if gs_dec != GS_CHURN_DECREASE:
        fail(f"groups_served_count churn set != the pinned empty churn: {gs_dec}")
    scen_first = scen_summary["closure_classes_first"]
    c34908 = [e for e in scen_first if e["class_index"] == CLASS_34908]
    if len(c34908) != 1 or c34908[0]["unknown_now"] != 7 or len(c34908[0]["groups_served"]) != 5:
        fail("scenario closure_classes_first entry for class 34908 drift (rank-8 / 7-unknown / 5-group)")

    # --- metric deltas -------------------------------------------------------------
    jb, js = base_summary["joint_greedy"], scen_summary["joint_greedy"]
    if jb["greedy_union_size"] != JOINT_GREEDY_BEFORE or js["greedy_union_size"] != JOINT_GREEDY_AFTER:
        fail("joint greedy union size drift vs pins")
    if base_summary["worklist_total"] != WORKLIST_BEFORE or scen_summary["worklist_total"] != WORKLIST_AFTER:
        fail("worklist totals drift vs pins")
    if jb["unique_groups"] != UNIQUE_GROUPS_BEFORE or js["unique_groups"] != UNIQUE_GROUPS_AFTER:
        fail("greedy group universe must stay static (no class freed)")
    if base_summary["group_best_options_nonfree"] != GROUP_BEST_NONFREE \
            or scen_summary["group_best_options_nonfree"] != GROUP_BEST_NONFREE:
        fail("nonfree best-option count drift")

    # --- emit decomp -----------------------------------------------------------------
    out = {
        "schema": "b33exh5loss2-adoption-decomp-deltas-v1",
        "scenario": "ADOPTED-CANONICAL",
        "packet": {"batches": [
            {"pool": "b33exh5", "class_index": 34908, "probed_rows": 5,
             "adopted_loss_rows": 2, "unadopted_win_rows": 2,
             "exhausted_excluded_rows": 1,
             "adopted_nodes_per_pool": ADOPTED_TOTAL_NODES, "whole_packet_nodes": PACKET_NODES},
        ],
            "adopted_loss_rows": ADOPTED_ROWS,
            "unadopted_win_rows": UNCONSUMED_WIN_ROWS,
            "exhausted_excluded_rows": EXHAUSTED_EXCLUDED_ROWS,
            "adopted_total_nodes_per_pass": ADOPTED_TOTAL_NODES,
            "adopted_loss_ids": adopted_ids,
            "unadopted_win_ids": list(WIN_IDS_UNCONSUMED),
            "unadopted_win_s5": {"af023": 810351, "af048": 962172},
            "exhausted_excluded_ids": list(EXHAUSTED_EXCLUDED_IDS),
            "exhausted_excluded_s5": {"af034": 930660},
            "decisive_labels": "2 fresh LOSS @30M adopted (Part EA af003/af039, "
                               "2-pass node-exact, published EXHAUSTED at 15M) + 2 probe-level "
                               "WIN @30M (af023/af048) unconsumed + 1 still-EXHAUSTED @30M "
                               "(af034) excluded + MISMATCH 0"},
        "cache": {"base_sha256": BASE_CACHE_SHA, "scenario_sha256": SCEN_CACHE_SHA,
                  "base_rows": len(base), "scenario_rows": len(scen), "increment_rows": len(incr),
                  "verdict_counts": {"WIN": 158, "LOSS": 6507},
                  "relation": "scenario == base rows + the 2 increment rows verbatim (no other row changed)",
                  "merge_audit_runs": 3, "merge_audit_sha256_each": MERGE_AUDIT_SHA,
                  "adopted_s5_indices": ADOPTED_S5},
        "class_34908": {"children_total_raw": len(child_keys_34908),
                        "children_total_s5": len(in_s5_34908),
                        "non_s5_children": 0,
                        "unknown_before": int(cb_t[CLASS_34908]["unknown_now"]),
                        "unknown_after": int(cs_t[CLASS_34908]["unknown_now"]),
                        "adopted_own": len(own_34908),
                        "unconsumed_win_children": 6,
                        "still_exhausted_children": 1,
                        "base_known_loss_children": len(known_base_34908),
                        "receipt_known_loss_children": 0,
                        "status_before": "unknown",
                        "status_after": "unknown (NOT freed, NOT excluded: 6 unconsumed "
                                        "probe-level WIN children {af029, af047, af050, af053, "
                                        "af023, af048} remain plus the still-EXHAUSTED af034)",
                        "class_rank": [8, 8],
                        "groups_served_count": [5, 5],
                        "unknown_s5_remaining": sorted(list(WIN_S5_PINNED_34908.values())
                                                       + list(EXH_S5_PINNED_34908.values())),
                        "not_a_root_verdict": "the loss-only adoption of a mixed re-probe "
                                               "packet frees nothing and excludes nothing; "
                                               "free_now/coverage quantities are Board-derived "
                                               "scheduling bookkeeping; no root verdict and no "
                                               "coverage claim is made"},
        "class_16371": {"status": "byte-static across Part EC (not EC-owned; 2 unconsumed "
                                  "probe-level WIN children {e042, e002} remain)",
                        "class_rank": [4, 4], "groups_served_count": [3, 3], "unknown": [2, 2]},
        "class_20421": {"status": "byte-static across Part EC (not EC-owned; 6 unconsumed "
                                  "probe-level WIN children remain)",
                        "class_rank": [7, 7], "groups_served_count": [4, 4], "unknown": [6, 6]},
        "closure_table": {"rows_before": CLOSURE_ROWS_BEFORE, "rows_after": CLOSURE_ROWS_AFTER,
                          "left": left, "entered": entered,
                          "left_reason": "EMPTY: the 807-row frontier table is fully static "
                                         "across this Part (no left/entered exchange, no rank churn)",
                          "unknown_changed_classes": changed,
                          "rank_churn_only_rows": rank_churn,
                          "rank_churn_detail": rank_churn_classes,
                          "groups_served_decrease_churn": gs_dec,
                          "fully_stable_rows": stable},
        "update8": {"resolved_before": UPD8_RESOLVED_BEFORE, "resolved_after": UPD8_RESOLVED_AFTER,
                    "newly_resolved_s5": NEWLY_RESOLVED_UPD8_S5,
                    "newly_resolved_within_adopted": True,
                    "note": "both adopted s5 indices (153030 / 950512) sit OUTSIDE the "
                            "frozen update8 baseline requirement: the resolved count, the "
                            "remaining count and every per-root remaining are BYTE-STATIC",
                    "remaining_before": UPD8_REMAINING_BEFORE, "remaining_after": UPD8_REMAINING_AFTER,
                    "groups_free_now_static": 131},
        "class_status_counts_before": cb,
        "class_status_counts_after": cs,
        "metrics": {"joint_greedy_union_size": [JOINT_GREEDY_BEFORE, JOINT_GREEDY_AFTER],
                    "worklist_total": [WORKLIST_BEFORE, WORKLIST_AFTER],
                    "known_universe_indices": [KNOWN_UNIVERSE_BEFORE, KNOWN_UNIVERSE_AFTER],
                    "cache_rows_in_universe": [CACHE_IN_UNIVERSE_BEFORE, CACHE_IN_UNIVERSE_AFTER],
                    "unique_groups": [UNIQUE_GROUPS_BEFORE, UNIQUE_GROUPS_AFTER],
                    "per_root_remaining_delta": PER_ROOT_REMAINING_DELTA,
                    "per_root_coverage_delta": PER_ROOT_COVERAGE_DELTA,
                    "note": "the joint greedy union shrinks (36,511 -> 36,509) and the "
                            "worklist shrinks (64,417 -> 64,415) after class 34908's frontier "
                            "cost drops (unknown 9 -> 7); per-root free/uncovered thirds are "
                            "IDENTICAL at every root (nothing was freed); roots 0/12 "
                            "individual greedy unions shift as pure bookkeeping; root 27 "
                            "stays 119/119"},
        "verification": {"kit_files_verified": {"ea": ea_files},
                         "packet_pins": {"reprobe_keys": EA_REPROBE_KEYS_SHA,
                                         "batch_keys": EA_BATCH_KEYS_SHA,
                                         "b33exh5_status": EA_STATUS_SHA,
                                         "b33_source_status": B33_STATUS_SHA},
                         "refresh_scripts_reexecuted": [BASE_REFRESH_SHA, SCEN_REFRESH_SHA],
                         "refresh_outputs_byte_identical": True,
                         "board_child_regeneration": "class-34908 56-child (all in the s5 "
                                                      "mask universe, ZERO non-s5) and "
                                                      "class-16371 / class-20421 boundaries "
                                                      "regenerated via Board(11).children"},
        "interpretation_guard":
            "only the 2 fresh af003/af039 exact-LOSS rows (resolved from published "
            "15M EXHAUSTED at the pre-declared 30M condition) are consumed into the "
            "canonical cache by this Part; the re-probed packet is MIXED: the af023/af048 "
            "probe-level WIN rows are consumed NOWHERE and belong to the scrutiny-owner C++ "
            "second-implementation gate (pin 9193f5b6...); af034 stays EXHAUSTED (honest "
            "UNKNOWN, same-condition re-probe forbidden, higher budget needs a NEW "
            "declaration); class 34908 (7 children remaining: 6 unconsumed WIN + 1 EXH) and "
            "classes 16371/20421 (byte-static) are NOT freed and NOT excluded; class status "
            "stays unknown, free_now 39 static, closure table 807 rows fully static with NO "
            "left/entered exchange and NO rank churn; no root verdict and no coverage claim "
            "is made anywhere; the per-root/greedy/worklist quantities quoted here are "
            "bookkeeping, never verdicts; no update8 resolution changed (both adopted keys "
            "sit outside the frozen baseline requirement); 11x11 stays UNKNOWN",
    }
    (EXP / "output/decomp-deltas-b33exh5loss2-adoption.json").write_text(
        json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("DECOMP OK changed=%d rank_churn=%d gs_dec=%d stable=%d left=%d entered=%d" % (
        len(changed), rank_churn, len(gs_dec), stable, len(left), len(entered)))
    print("class34908: unknown 9 -> 7 (2 adopted, 6 unconsumed WINs + 1 still-EXHAUSTED remain), NOT freed")
    print("class16371/class20421: byte-static (no EC row inside either boundary)")
    print("update8: byte-static (both adopted s5 indices outside the frozen requirement)")


if __name__ == "__main__":
    main()
