"""Part EB adoption delta extraction: BASE (Part DZ, b4loss1+b36loss40+b37loss46) vs SCENARIO (b3loss3).

Fail-closed machine recomputation of exactly what the batch-3 3-LOSS canonical
adoption changed, from published bytes only:

* every published artifact sha-pinned (the published Part DZ outputs -- the
  BASE canonical cache 4a30b88d... 6,660 rows WIN 158 / LOSS 6,502, the BASE
  reaudit outputs refresh-summary 7f7465ab... / closure-classes 02641235... /
  per-root-coverage f7418e98... / probe-worklist regen pin 9b420875... -- the
  Part EB outputs -- increment 94da84da..., increments manifest 97912a39...,
  the 6,663-row scenario cache c3026468... WIN 158 / LOSS 6,505 -- the
  merge-audits x3 (identical sha), the byte-clone of the union merger,
  graph/update8/board/policy/quarantine pins);
* the published Part DZ refresh fork (reaudit/scripts/refresh_adoption_dz.py,
  sha cbb1d2b7...) and the published Part EB refresh fork (reaudit/scripts/
  refresh_adoption_eb.py, sha b6b780a3...) are RE-EXECUTED byte-verbatim in
  isolated scratch trees against their pinned inputs, and all eight outputs
  must be byte-identical to the published / regenerated pins before any delta
  is emitted (double-run determinism; this simultaneously re-proves the
  published Part DZ reaudit outputs are regenerable from published bytes);
* SCEN cache == BASE cache rows + exactly the 3 increment rows (verdict
  agreement everywhere; 6,663 rows, WIN 158 / LOSS 6,505); the batch-3 probed
  packet is MIXED: full_packet_eq_loss_only=false, the probe-level WIN d002
  stays unconsumed, 0 EXHAUSTED rows;
* kit integrity: the batch-36 kit (160 files, MANIFEST f4a6d53f...) verified
  file-by-file (its adopted rows sit inside BASE and inside the class-20421
  boundary); the pinned jsreplay.js solver image (84585617...); the published
  batch-3 packet keys (ad05073a... 3691fe9f) / status (7877f4a0...) pins and
  the batch-36 kit batch3-pins + byte-clone agreement;
* the class-16371 arithmetic is recomputed from the frozen dependency graph
  with the integer-geometry Board: the 52-child boundary is regenerated;
  Part DZ already adopted 47 own children (46 batch-37 + e001), leaving
  exactly 2 unknown children == the 2 unconsumed WIN keys {e042, e002};
  Part EB adopts NOTHING inside this boundary: unknown stays 2, rank stays 4,
  groups_served stays 3 -- class 16371 is byte-static across this Part;
* the class-20421 arithmetic likewise (raw boundary 50 children: 49 in the
  s5 mask universe + 1 pre-existing non-s5 cache row pinned
  (10378545341275312128, 131072) exact LOSS nodes 0 present in BASE and
  SCEN): the 40 Part-DZ batch-36 rows are known-LOSS in BASE; the 3 adopted
  batch-3 rows resolve; exactly 6 children stay unknown == the unconsumed
  WIN keys {d002, d008, d009, d021, d026, d029}, so class 20421 is NOT freed
  and NOT excluded (unknown 9 -> 6, rank 8 -> 7, groups_served 4 static,
  one pure rank bookkeeping exchange with class 34908 which shifts 7 -> 8);
* every closure-classes.csv row is compared: ZERO unknown_now changes beside
  class 20421; 1 rank-churn-only row (34908); 804 fully stable rows; the
  groups_served_count churn set is EMPTY; the closure table keeps 807 rows
  on both sides; NO left/entered row (pure static table);
* update8 refresh: resolved_among_baseline_requirement grows from 256 to
  259 (+3 == exactly the 3 adopted s5 indices {38215, 259023, 300778} inside
  the frozen baseline requirement); remaining 31,603 -> 31,600; no
  resolution is lost; groups_free_now stays 131;
* class_status counts: excluded 390 / excluded_now 23 / free_now 39 /
  unknown 34,497 IDENTICAL before and after (the loss-only adoption frees
  nothing and excludes nothing); Board verification 39/39 with zero
  rejections on both sides; root 27 stays 119/119;
* per-root coverage: free/uncovered thirds are IDENTICAL at every root; the
  individual greedy union changes only at roots 12 and 37 (pure re-selection
  bookkeeping, no coverage claim); per-root remaining decreases only at
  roots 12/37 (-6 each, class 20421's groups);
* the frozen greedy scheduler deltas are recorded as bookkeeping (joint
  greedy 36,511 static, worklist 64,420 -> 64,417, known universe 839 -> 842,
  cache in universe 816 -> 819).

No unknown verdict is asserted anywhere.  The standard 11x11 empty board
and every one of the 19 central-reply roots stay UNKNOWN; free_now /
coverage quantities are scheduling bookkeeping derived from exact LOSS
verdicts, not root verdict claims.  The single probe-level WIN row (batch-3
d002) is consumed NOWHERE by this Part (scrutiny-owner C++ second-
implementation gate pin 9193f5b6...); no WIN verdict and no EXHAUSTED
verdict enters the canonical cache.
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

BASE_EXP = ROOT / "research/experiments/n11-centralreply-b4loss1-b36loss40-b37loss46-adoption-reaudit-20261125"
BASE_OUT = BASE_EXP / "reaudit/output"
BASE_CACHE = BASE_EXP / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-plus-b35loss26-plus-b4loss1-plus-b36loss40-plus-b37loss46-20261125.cache"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-plus-b35loss26-plus-b4loss1-plus-b36loss40-plus-b37loss46-plus-b3loss3-20261125.cache"
INCR = EXP / "output/increment-b3loss3-20261125.cache"
MANIFEST = EXP / "output/increments-manifest.json"
KIT36 = ROOT / "research/experiments/n11-centralreply-closure-class20421-batch36-20261124"
KIT37 = ROOT / "research/experiments/n11-centralreply-closure-class16371-batch37-20261125"
B4_DIR = ROOT / "research/experiments/n11-centralreply-closure-class16371-batch4-20261122"
B3_DIR = ROOT / "research/experiments/n11-centralreply-closure-class20421-batch-20261122"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_REFRESH_SCRIPT = BASE_EXP / "reaudit/scripts/refresh_adoption_dz.py"
SCEN_REFRESH_SCRIPT = EXP / "reaudit/scripts/refresh_adoption_eb.py"
MERGER = EXP / "scripts/s5_union_merge.py"

BASE_CACHE_SHA = "4a30b88dba782138585f16e1ad0ea65da55431dbc2c59250998fc5a1331349c9"
SCEN_CACHE_SHA = "c3026468c74b56e71f3a9e0cd45c13e4a8cba147d137c25703c5be62b9c4c94e"
INCR_SHA = "94da84da8116bb89457b32b0b72cbcb667406b75ee1a0b4d76107b9b05df9859"
MANIFEST_SHA = "97912a398fab7cbe15e5e5e15a93b3a580460b2c4aca58d9b67305e45659c1e8"
BASE_SUMMARY_SHA = "7f7465ab189798e8a0214803daf6200a3c6c32f96318223b204d8ca45bbebc26"
BASE_CLOSURE_SHA = "026412359c9c025d2dbcfc694fe981c8db30507738942c9a995769010248039b"
BASE_PRC_SHA = "f7418e980a9753bedafd85857c839f7c21545397913b01a0762224e4c7c7a6d8"
BASE_WORKLIST_SHA = "9b4208758e22be467919e09d6f83eb15443fa84b8e84495b6ff87cbae150ceae"
SCEN_SUMMARY_SHA = "6ff36b6e02c3dc2b958be25af6af8d5adcb001aa7af8918173896bac73c9bf2e"
SCEN_CLOSURE_SHA = "f2cf3c4373bd81a264b62956776e8e46e8506b90461c5e1dba8e0b8065b48c57"
SCEN_PRC_SHA = "cad355a82af4450666ce23f605782e06e23bdb95baeb33fff8230af63558f439"
SCEN_WORKLIST_SHA = "15f95053cf50ce9f388f4b267d5bcce2cbba2f4abaf80fc57d20dfa9ab28cbb1"
BASE_REFRESH_SHA = "cbb1d2b753975563efa193b06a56919b6e1758ab13bcfcedc77d0bfd76751e56"
SCEN_REFRESH_SHA = "b6b780a3fd3ef81a07a052c48002fa511f016b30cae3007f199283c6f87a3b7a"
MERGE_AUDIT_SHA = "e4dd5024ade5d793db96f82b7f20e6201fe480303c19e2fd81679376f0f523ff"
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
ADOPTED_TABLE_DIGEST = "6c713953b96bb8f98d1a9146c53d90342395042a5aab1f0731273678d82b9036"

KIT36_MANIFEST_SHA = "f4a6d53f65694b1393767d562a14266d8bc91b3f255ba23c5d828414adcd0826"
KIT36_FILES = 160
KIT36_KEYS_SHA = "d59182030ce1ade5ad02c8db3836291e2feadfa84325fd4729001e80bfc0c815"
KIT36_STATUS_SHA = "dd8c180b9ad19937634d6ad7d0b0964a08f637d9d3d24dbbeabf198e6f6d74fb"
KIT37_KEYS_SHA = "25b9388e9f855f30bf334bc825f483dbe66becc5c49b918bd1aaa74d3f3765a8"
B4_KEYS_SHA = "70b8a4c89f7cea454bfd2b52f720245b6d9c5d7311878bf8aac637940825ecdf"
B3_KEYS_SHA = "ad05073a845e511669d28fde3691fe9f3bf9f08eef2021039c884f1411f6dd3f"
B3_STATUS_SHA = "7877f4a085b466289b7647a1d88b98b755afa2065efae8f59c01bb10dca4cbbb"
JSREPLAY_SHA = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
RUNBATCH_SHA = "f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84"
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
BOARD_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

CLASS_16371 = 16371
CLASS_20421 = 20421
ADOPTED_ROWS = 3
UNCONSUMED_WIN_ROWS = 1
ADOPTED_TOTAL_NODES = 14962526

B36_ADOPTED_IDS = ["d005", "d006", "d007", "d010", "d011", "d012", "d013",
                   "d014", "d015", "d016", "d017", "d018", "d019", "d020",
                   "d022", "d023", "d024", "d025", "d027", "d028", "d030",
                   "d031", "d032", "d033", "d034", "d035", "d036", "d037",
                   "d038", "d039", "d040", "d041", "d042", "d043", "d044",
                   "d045", "d046", "d047", "d048", "d049"]
B36_WIN_IDS = ["d008", "d009", "d021", "d026", "d029"]
B37_WIN_ID = "e042"
B4_WIN_ID = "e002"
B3_ADOPTED_IDS = ["d001", "d003", "d004"]
B3_PACKET_IDS = ["d001", "d002", "d003", "d004"]

WIN_S5_PINNED = {"d002": 197253, "d008": 528689, "d009": 543795, "d021": 605961,
                 "d026": 620742, "d029": 625899, "e042": 550879, "e002": 183566}
WIN_NODES_PINNED_EB = {"d002": 5359994}
POOL_WIN_IDS = {"b3": ["d002"]}
POOL_NODE_PINS = {
    "b3": {"adopted_nodes": 14962526, "whole_packet_nodes": 20322520,
           "status_lines": 5,
           "first": "2026-11-22T03:14:35Z d001 PASS 15000000,2,879510",
           "final": "2026-11-22T03:17:41Z d004 PASS 15000000,2,11969338",
           "win_halt": ["2026-11-22T03:16:25Z d002 WIN-HALT"]},
}

ADOPTED_S5 = [38215, 259023, 300778]
NEWLY_RESOLVED_UPD8_S5 = [38215, 259023, 300778]

# class 16371 (Part DZ already adopted its own 47; EB adopts nothing here)
BOUNDARY_16371 = 52
BASE_KNOWN_LOSS_S5_16371 = [546606]      # the batch-4 key e022, already exact LOSS in BASE
RECEIPT_LOSS_S5_16371 = [381858, 550881]
B37_ADOPTED_COUNT = 46                   # 46 batch-37 adopted rows + e001 = 47 own in BASE

BOUNDARY_20421_RAW = 50
BOUNDARY_20421_S5 = 49
NON_S5_CACHE_KEY_20421 = (10378545341275312128, 131072)
B36_KEYS_TOTAL = 45
RANK_CHURN_CLASS = 34908                  # the single pure rank bookkeeping exchange

STATUS_EXPECTED = {"excluded": 390, "excluded_now": 23, "free_now": 39, "unknown": 34497}
UPD8_RESOLVED_BEFORE = 256
UPD8_RESOLVED_AFTER = 259
UPD8_REMAINING_BEFORE = 31603
UPD8_REMAINING_AFTER = 31600
JOINT_GREEDY_BEFORE = 36511
JOINT_GREEDY_AFTER = 36511
WORKLIST_BEFORE = 64420
WORKLIST_AFTER = 64417
KNOWN_UNIVERSE_BEFORE = 839
KNOWN_UNIVERSE_AFTER = 842
CACHE_IN_UNIVERSE_BEFORE = 816
CACHE_IN_UNIVERSE_AFTER = 819
CACHE_VERDICTS_BEFORE = {"1": 158, "2": 6502}
CACHE_VERDICTS_AFTER = {"1": 158, "2": 6505}
UNIQUE_GROUPS_BEFORE = 2115
UNIQUE_GROUPS_AFTER = 2115
PER_ROOT_REMAINING_DELTA = {"12": -6, "37": -6}
PER_ROOT_COVERAGE_DELTA = {
    "12": {"free": [6, 6], "uncovered": [113, 113], "greedy": [2896, 2893]},
    "37": {"free": [4, 4], "uncovered": [115, 115], "greedy": [3622, 3620]},
}
CLOSURE_ROWS_BEFORE = 807
CLOSURE_ROWS_AFTER = 807
CLOSURE_LEFT = []
CLOSURE_ENTERED = []
CLASS_16371_ROW_BEFORE = {"class_rank": "4", "unknown_now": "2", "groups_served_count": "3"}
CLASS_16371_ROW_AFTER = {"class_rank": "4", "unknown_now": "2", "groups_served_count": "3"}
CLASS_20421_ROW_BEFORE = {"class_rank": "8", "unknown_now": "9", "groups_served_count": "4"}
CLASS_20421_ROW_AFTER = {"class_rank": "7", "unknown_now": "6", "groups_served_count": "4"}
GS_CHURN_DECREASE = []
RANK_CHURN_ROWS = 1
FULLY_STABLE_ROWS = 804
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


def _kit_candidates(kit_dir: Path, rel: str):
    cands = [kit_dir / rel, ROOT / rel]
    stripped = rel.split("research/experiments/", 1)[-1]
    if stripped.startswith("n11"):
        stripped = stripped[stripped.index("/") + 1:]
    cands.append(kit_dir / stripped)
    cands.append(kit_dir / "output" / stripped)
    return cands


def verify_kit(dirp: Path, manifest_sha: str, files_expected: int):
    if sha(dirp / "MANIFEST-sha256.txt") != manifest_sha:
        fail(f"kit {dirp.name} MANIFEST sha drift")
    n = 0
    for line in (dirp / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split()
        if len(fields) >= 4:  # batch-36 format: sha blobsha size relpath
            want, rel = fields[0], fields[3]
        else:                 # batch-37 format: sha relpath
            want, rel = fields[0], fields[1]
        p = next((c for c in _kit_candidates(dirp, rel) if c.is_file()), None)
        if p is None:
            fail(f"kit {dirp.name} file missing: {rel}")
        if sha(p) != want:
            fail(f"kit {dirp.name} sha drift at {rel}")
        n += 1
    if n != files_expected:
        fail(f"kit {dirp.name} files {n} != {files_expected}")
    return n


def _read_keys(p: Path):
    d = json.loads(p.read_text())
    return {e["key_id"]: (int(e["lo"]), int(e["hi"])) for e in d["keys"]}, d


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
    k36 = verify_kit(KIT36, KIT36_MANIFEST_SHA, KIT36_FILES)
    js = [p for p in (KIT36 / "scripts/jsreplay.js", KIT36 / "replay/jsreplay.js",
                      KIT36 / "jsreplay.js") if p.is_file()]
    if not js or sha(js[0]) != JSREPLAY_SHA:
        fail("jsreplay.js sha drift in kit batch-36 (pinned solver image 8458...)")
    if sha(KIT36 / "input/batch-keys-b36.json") != KIT36_KEYS_SHA or sha(KIT36 / "output/status.log") != KIT36_STATUS_SHA:
        fail("batch-36 kit keys/status sha drift")
    if sha(B3_DIR / "input/batch-keys.json") != B3_KEYS_SHA:
        fail("batch-3 packet keys sha drift vs the pinned ad05073a... 3691fe9f")
    if sha(B3_DIR / "output/status.log") != B3_STATUS_SHA:
        fail("batch-3 packet status sha drift")
    if sha(KIT37 / "input/batch-keys-b37.json") != KIT37_KEYS_SHA:
        fail("batch-37 kit keys sha drift (needed for the 16371 boundary)")
    if sha(B4_DIR / "input/batch-keys.json") != B4_KEYS_SHA:
        fail("batch-4 packet keys sha drift (needed for the 16371 boundary)")
    keys36, bk36 = _read_keys(KIT36 / "input/batch-keys-b36.json")
    keys37, _ = _read_keys(KIT37 / "input/batch-keys-b37.json")
    keys4, _ = _read_keys(B4_DIR / "input/batch-keys.json")
    keys3, _ = _read_keys(B3_DIR / "input/batch-keys.json")
    # kit batch3 pins + byte-clone agreement re-verified (maker covers too)
    if bk36["pins"]["batch3_batch_keys"] != B3_KEYS_SHA or bk36["pins"]["batch3_status"] != B3_STATUS_SHA:
        fail("batch-36 kit batch-3 packet pin drift")
    clone_keys = KIT36 / "sources/batch3-packet/batch-keys.json"
    clone_status = KIT36 / "sources/batch3-packet/status.log"
    if (clone_keys.read_bytes() != (B3_DIR / "input/batch-keys.json").read_bytes()
            or clone_status.read_bytes() != (B3_DIR / "output/status.log").read_bytes()):
        fail("published batch-3 packet != batch-36 kit byte-clone")

    # --- manifest decomposition ------------------------------------------
    manifest = json.loads(MANIFEST.read_text())
    if manifest["schema"] != "b3loss3-increments-manifest-v1":
        fail("manifest schema drift")
    if manifest["base_cache_sha256"] != BASE_CACHE_SHA:
        fail("manifest base cache pin drift")
    if manifest["sha256"]["loss_increment"] != INCR_SHA:
        fail("manifest loss_increment pin drift")
    if manifest["merger_sha256"] != MERGER_SHA:
        fail("manifest merger pin drift")
    if manifest["adopted_table_digest_sha256"] != ADOPTED_TABLE_DIGEST:
        fail("manifest adopted-table digest drift")
    if manifest["base_cache_rows"] != 6660:
        fail("manifest base rows drift")
    if manifest["base_cache_absent_hits_for_emitted"] != 0:
        fail("manifest emitted rows must be absent from BASE (fresh increment)")
    if manifest["base_cache_prior_adoption_confirmed"] != 0:
        fail("manifest prior-adoption count drift")
    if manifest["quarantine_hits"] != 0:
        fail("manifest quarantine hits must be 0")
    if manifest["row_counts"] != {"adopted_loss_rows": 3, "exhausted_excluded": 0,
                                  "prior_adopted_loss_rows": 0, "wins_unconsumed": 1}:
        fail("manifest row_counts drift")
    if manifest["provenance"] != {"batch36_kit_files": 160, "batch3_status_lines": 5,
                                  "batch3_raws_published": True}:
        fail("manifest provenance drift")
    adopted_ids = manifest["loss_ids"]
    if adopted_ids != B3_ADOPTED_IDS:
        fail(f"manifest adopted ids != the pinned batch-3 adopted set: {adopted_ids}")
    if sorted(manifest["resolved_ids"]) != sorted(adopted_ids):
        fail("manifest resolved_ids != loss_ids")
    if manifest.get("full_packet_eq_loss_only") is not False:
        fail("the probed batch-3 packet is MIXED: manifest full_packet_eq_loss_only must be false")
    if manifest.get("win_scenario_exists") is not True:
        fail("manifest win_scenario_exists must be true (the d002 probe-level WIN exists)")
    win_ids = manifest["unadopted_win_ids"]
    if sorted(win_ids) != ["d002"]:
        fail("manifest unconsumed WIN id set drift")
    if manifest["exhausted_excluded_ids"] or manifest["exhausted_rows"]:
        fail("manifest EXHAUSTED decomposition must be empty")
    win_rows = manifest["unadopted_win_rows"]
    if len(win_rows) != UNCONSUMED_WIN_ROWS:
        fail("manifest WIN row count drift")
    for w in win_rows:
        if w["key_id"] != "d002" or w["verdict"] != "WIN":
            fail(f"manifest WIN row identity drift: {w['key_id']}")
        if w["nodes"] != WIN_NODES_PINNED_EB[w["key_id"]]:
            fail(f"manifest WIN row node drift: {w['key_id']}")
        if w["pool"] not in POOL_WIN_IDS or w["key_id"] not in POOL_WIN_IDS[w["pool"]]:
            fail(f"manifest WIN row pool drift: {w['key_id']}")
    if len(manifest["adopted_table"]) != ADOPTED_ROWS or any(r["result"] != 2 for r in manifest["adopted_table"]):
        fail("manifest adopted_table must be 3 exact-LOSS rows")
    if sum(r["nodes"] for r in manifest["adopted_table"]) != ADOPTED_TOTAL_NODES:
        fail("manifest adopted_table node sum drift")
    for b in manifest["batches"]:
        pool = b["pool"]
        if pool != "b3":
            fail(f"unexpected pool {pool} in the EB manifest")
        pins_p = POOL_NODE_PINS[pool]
        if sorted(b["adopted_loss_ids"]) != sorted(B3_ADOPTED_IDS):
            fail(f"pool {pool} adopted id set drift")
        if sorted(b["unadopted_win_ids"]) != sorted(POOL_WIN_IDS[pool]):
            fail(f"pool {pool} unconsumed WIN id set drift")
        if sorted(b["probed_ids"]) != sorted(B3_PACKET_IDS):
            fail(f"pool {pool} probed != adopted + WIN")
        if b["exhausted_excluded_ids"]:
            fail(f"pool {pool} EXHAUSTED drift")
        if b["status_log_lines"] != pins_p["status_lines"]:
            fail(f"pool {pool} status-log honest-history line count drift")
        if b["status_log_first_line"] != pins_p["first"] or b["status_log_final_line"] != pins_p["final"]:
            fail(f"pool {pool} status-log first/final line drift")
        if b["status_log_win_halt_lines"] != pins_p["win_halt"]:
            fail(f"pool {pool} status-log WIN-HALT drift")
        if b["adopted_nodes_per_pool"] != pins_p["adopted_nodes"]:
            fail(f"pool {pool} adopted node total drift")
        if b["whole_packet_nodes"] != pins_p["whole_packet_nodes"]:
            fail(f"pool {pool} whole-packet node total drift")

    # --- refresh re-execution (double-run determinism) ---------------------
    base_tmp = rerun_refresh(BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA, ".ebverify-base-dz87")
    scen_tmp = rerun_refresh(SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA, ".ebverify-scen-b3loss3")
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
    shutil.rmtree(ROOT / "research/experiments/.ebverify-base-dz87")
    shutil.rmtree(ROOT / "research/experiments/.ebverify-scen-b3loss3")

    # --- cache relation: SCEN == BASE + exactly the 3 increment rows -------
    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    incr = load_cache(INCR)
    if len(base) != 6660 or len(scen) != 6663 or len(incr) != ADOPTED_ROWS:
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
    if (wins, losses) != (158, 6505):
        fail(f"scenario verdict counts {wins}/{losses} != 158/6,505")
    # the WIN discretization keys must not collide with the adopted set:
    tab = {(int(e["lo"]), int(e["hi"])): (e["legal"], e["result"], e["nodes"])
           for e in manifest["adopted_table"]}
    if set(tab) != set(incr) or len(tab) != 3:
        fail("manifest adopted_table keys != increment keys")
    for key, row in incr.items():
        if (row[0], row[1]) != (tab[key][1], tab[key][2]):
            fail(f"manifest adopted_table row != increment row: {key}")
    if keys3["d002"] in incr or keys3["d002"] in base or keys3["d002"] in scen:
        fail("the unconsumed WIN key d002 must sit in NO cache (scrutiny gate owns it)")

    # --- Board arithmetic for classes 16371 and 20421 ----------------------
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
    adopted_keys_20421 = {keys3[k] for k in B3_ADOPTED_IDS}
    if {mask_to_index[k] for k in adopted_keys_20421} != set(ADOPTED_S5):
        fail("adopted s5 index set != the pinned adopted list")

    # --- class 16371 (must be BYTE-STATIC across this Part) ----------------
    lo, hi = s4_masks[CLASS_16371]
    children = board.children(lo | (hi << 64))
    child_keys_16371 = {(c & ((1 << 64) - 1), c >> 64) for c in children}
    if len(child_keys_16371) != BOUNDARY_16371:
        fail(f"class-16371 Board child boundary {len(child_keys_16371)} != {BOUNDARY_16371}")
    if any(k not in mask_to_index for k in child_keys_16371):
        fail("class-16371 boundary must be entirely inside the s5 mask universe")
    if not set(keys37.values()) <= child_keys_16371 or not {keys4["e001"], keys4["e002"]} <= child_keys_16371:
        fail("batch-37 / batch-4 key sets not inside the class-16371 child boundary")
    receipt_child_16371 = {k for k in child_keys_16371 if mask_to_index[k] in receipt_verdicts}
    if sorted(mask_to_index[k] for k in receipt_child_16371) != RECEIPT_LOSS_S5_16371:
        fail("the update8-receipt LOSS children of 16371 != the pinned receipt set")
    for k in receipt_child_16371:
        if receipt_verdicts[mask_to_index[k]] != 2:
            fail("an update8-receipt child of 16371 is not LOSS")
        if k in base or k in scen:
            fail("a receipt child of 16371 is also a cache row")
    known_base_16371 = {k for k in child_keys_16371 if k in base}
    if sorted(mask_to_index[k] for k in known_base_16371) != sorted(
            [BASE_KNOWN_LOSS_S5_16371[0]]
            + [mask_to_index[keys37[k]] for k in keys37 if k != B37_WIN_ID]
            + [mask_to_index[keys4["e001"]]]):
        fail("BASE-known children of 16371 != e022 + the 46 batch-37 adopted + e001 (48)")
    if len(known_base_16371) != 48:
        fail(f"class-16371 BASE-known child count {len(known_base_16371)} != 48")
    for k in known_base_16371:
        if base[k][0] != 2:
            fail("a BASE-known child of 16371 is not an exact LOSS")
    unknown_base_16371 = {k for k in child_keys_16371 if k not in base and k not in receipt_child_16371}
    if sorted(mask_to_index[k] for k in unknown_base_16371) != sorted(
            [WIN_S5_PINNED[B37_WIN_ID], WIN_S5_PINNED[B4_WIN_ID]]):
        fail("BASE unknown children of 16371 != the pinned unconsumed WIN keys {e042, e002}")
    if len(unknown_base_16371) != 2:
        fail("class-16371 BASE unknown count != 2")
    unknown_scen_16371 = {k for k in child_keys_16371 if k not in scen and k not in receipt_child_16371}
    if unknown_scen_16371 != unknown_base_16371:
        fail("class 16371 must be BYTE-STATIC: scenario unknown children != BASE unknown children")
    own_16371 = child_keys_16371 & adopted_keys_20421
    if own_16371:
        fail("no adopted key may sit inside the class-16371 boundary (16371 is DZ-owned)")
    if any(k in quarantined for k in child_keys_16371):
        fail("a quarantined key sits inside the class-16371 child boundary")

    # --- class 20421 (the single EB target) ----------------------------------
    lo, hi = s4_masks[CLASS_20421]
    children = board.children(lo | (hi << 64))
    child_keys_20421 = {(c & ((1 << 64) - 1), c >> 64) for c in children}
    if len(child_keys_20421) != BOUNDARY_20421_RAW:
        fail(f"class-20421 raw Board child boundary {len(child_keys_20421)} != {BOUNDARY_20421_RAW}")
    non_s5 = [k for k in child_keys_20421 if k not in mask_to_index]
    if len(non_s5) != 1 or non_s5[0] != NON_S5_CACHE_KEY_20421:
        fail("class-20421 boundary must contain exactly the one pinned non-s5 pre-existing cache key")
    if NON_S5_CACHE_KEY_20421 not in base or base[NON_S5_CACHE_KEY_20421] != (2, 0) \
            or scen.get(NON_S5_CACHE_KEY_20421) != (2, 0):
        fail("class-20421 non-s5 cache child must be an exact LOSS nodes-0 row in BOTH caches")
    in_s5_20421 = {k for k in child_keys_20421 if k in mask_to_index}
    if len(in_s5_20421) != BOUNDARY_20421_S5:
        fail(f"class-20421 in-s5 boundary {len(in_s5_20421)} != {BOUNDARY_20421_S5}")
    if not set(keys36.values()) <= child_keys_20421 or not {keys3[k] for k in B3_PACKET_IDS} <= child_keys_20421:
        fail("batch-36 / batch-3 key sets not inside the class-20421 child boundary")
    receipt_child_20421 = {k for k in in_s5_20421 if mask_to_index[k] in receipt_verdicts}
    if receipt_child_20421:
        fail("class-20421 must have ZERO update8-receipt children")
    known_base_20421 = {k for k in in_s5_20421 if k in base}
    if known_base_20421 != {keys36[k] for k in B36_ADOPTED_IDS}:
        fail("BASE-known children of 20421 != the 40 Part-DZ batch-36 adopted keys")
    if len(known_base_20421) != 40:
        fail("class-20421 BASE-known child count != 40")
    for k in known_base_20421:
        if base[k][0] != 2:
            fail("a BASE-known child of 20421 is not an exact LOSS")
    unknown_base_20421 = {k for k in in_s5_20421 if k not in base}
    if unknown_base_20421 != {keys36[k] for k in B36_WIN_IDS} | {keys3[k] for k in B3_PACKET_IDS}:
        fail("BASE unknown children of 20421 != batch-36 5 WINs + the 4 batch-3 rows (9)")
    if len(unknown_base_20421) != 9:
        fail("class-20421 BASE unknown count != 9")
    unknown_scen_20421 = {k for k in in_s5_20421 if k not in scen}
    if len(unknown_scen_20421) != 6:
        fail(f"scenario unknown children of 20421 = {len(unknown_scen_20421)} != 6 (5 batch-36 WINs + d002; class NOT freed)")
    want = sorted(WIN_S5_PINNED[k] for k in ("d002", "d008", "d009", "d021", "d026", "d029"))
    if sorted(mask_to_index[k] for k in unknown_scen_20421) != want:
        fail("scenario unknown children of 20421 != the pinned unconsumed WIN keys")
    own_20421 = in_s5_20421 & adopted_keys_20421
    if len(own_20421) != 3 or own_20421 != adopted_keys_20421:
        fail("class-20421 adopted-own set != exactly the 3 batch-3 rows")
    for k in own_20421:
        if scen[k][0] != 2:
            fail(f"an adopted child of 20421 is not an exact LOSS in the scenario: {k}")
    if own_20421 & unknown_scen_20421:
        fail("adopted set collides with the unconsumed WIN set inside 20421")
    if any(k in quarantined for k in child_keys_20421):
        fail("a quarantined key sits inside the class-20421 child boundary")

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
    if newly != NEWLY_RESOLVED_UPD8_S5:
        fail(f"newly resolved update8 set != the pinned adopted-in-requirement 3-set: {newly}")
    if lost:
        fail(f"update8 resolution LOST rows: {sorted(lost)}")
    if not set(newly) <= set(ADOPTED_S5):
        fail("newly resolved update8 set is not a subset of the adopted s5 set")
    if rb["remaining_now"] - rs["remaining_now"] != len(NEWLY_RESOLVED_UPD8_S5):
        fail("update8 remaining delta != the pinned newly-resolved count")
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
    if scen_summary["inputs"]["cache_rows"] != 6663 or scen_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_AFTER \
            or scen_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_AFTER:
        fail("scenario inputs metrics drift")
    if base_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["cache_rows"] != 6660:
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
    if CLASS_16371 not in cb_t or CLASS_16371 not in cs_t:
        fail("class 16371 must remain in BOTH closure tables (not freed, not excluded)")
    for col, want in CLASS_16371_ROW_BEFORE.items():
        if cb_t[16371][col] != want:
            fail(f"base class-16371 row {col} drift: {cb_t[16371][col]} != {want}")
    for col, want in CLASS_16371_ROW_AFTER.items():
        if cs_t[16371][col] != want:
            fail(f"scenario class-16371 row {col} drift: {cs_t[16371][col]} != {want} (16371 must be byte-static)")
    if CLASS_20421 not in cb_t or CLASS_20421 not in cs_t:
        fail("class 20421 must remain in BOTH closure tables (not freed, not excluded)")
    for col, want in CLASS_20421_ROW_BEFORE.items():
        if cb_t[20421][col] != want:
            fail(f"base class-20421 row {col} drift: {cb_t[20421][col]} != {want}")
    for col, want in CLASS_20421_ROW_AFTER.items():
        if cs_t[20421][col] != want:
            fail(f"scenario class-20421 row {col} drift: {cs_t[20421][col]} != {want}")
    if int(cb_t[20421]["unknown_now"]) - int(cs_t[20421]["unknown_now"]) != len(own_20421) or len(own_20421) != 3:
        fail("class-20421 unknown delta != its own adopted children (Board boundary)")
    if cb_t[16371] != cs_t[16371]:
        fail("class-16371 full row must be byte-identical before/after")
    changed, rank_churn, stable, gs_dec, gs_bad = [], 0, 0, [], []
    rank_churn_classes = []
    for ci, brow in sorted(cb_t.items()):
        if ci in (CLASS_16371, CLASS_20421) or ci not in cs_t:
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
        own = len(kids_keys & adopted_keys_20421)
        if (b_unk - s_unk) != own or own == 0:
            fail(f"class {ci} unknown delta {b_unk}->{s_unk} != own adopted membership {own}")
        changed.append({"class_index": ci, "unknown_before": b_unk, "unknown_after": s_unk,
                        "own_adopted": own})
    if changed != CHANGED_CLASS_SET:
        fail(f"changed-class set != the pinned EMPTY set: {changed}")
    if rank_churn != RANK_CHURN_ROWS or stable != FULLY_STABLE_ROWS:
        fail(f"rank churn {rank_churn}/stable {stable} != pinned {RANK_CHURN_ROWS}/{FULLY_STABLE_ROWS}")
    if rank_churn_classes != [(RANK_CHURN_CLASS, 7, 8)]:
        fail(f"the single rank-churn row must be class {RANK_CHURN_CLASS} 7->8 (bookkeeping swap with 20421): {rank_churn_classes}")
    for e in gs_dec:
        if e["unknown_now"][0] != e["unknown_now"][1]:
            fail(f"groups_served_churn class {e['class_index']} changed unknown_now: {e}")
    if gs_dec != GS_CHURN_DECREASE:
        fail(f"groups_served_count churn set != the pinned empty churn: {gs_dec}")
    scen_first = scen_summary["closure_classes_first"]
    c16371 = [e for e in scen_first if e["class_index"] == CLASS_16371]
    if len(c16371) != 1 or c16371[0]["unknown_now"] != 2 or len(c16371[0]["groups_served"]) != 3:
        fail("scenario closure_classes_first entry for class 16371 drift (rank-4 / 2-unknown / 3-group)")
    c20421 = [e for e in scen_first if e["class_index"] == CLASS_20421]
    if len(c20421) != 1 or c20421[0]["unknown_now"] != 6 or len(c20421[0]["groups_served"]) != 4:
        fail("scenario closure_classes_first entry for class 20421 drift (rank-7 / 6-unknown / 4-group)")

    # --- metric deltas -------------------------------------------------------------
    jb, js = base_summary["joint_greedy"], scen_summary["joint_greedy"]
    if jb["greedy_union_size"] != JOINT_GREEDY_BEFORE or js["greedy_union_size"] != JOINT_GREEDY_AFTER:
        fail("joint greedy union size drift vs pins")
    if base_summary["worklist_total"] != WORKLIST_BEFORE or scen_summary["worklist_total"] != WORKLIST_AFTER:
        fail("worklist totals drift vs pins")
    if jb["unique_groups"] != UNIQUE_GROUPS_BEFORE or js["unique_groups"] != UNIQUE_GROUPS_AFTER:
        fail("greedy group universe must stay static (no class freed)")
    if base_summary["group_best_options_nonfree"] != 2115 or scen_summary["group_best_options_nonfree"] != 2115:
        fail("nonfree best-option count drift")

    # --- emit decomp -----------------------------------------------------------------
    out = {
        "schema": "b3loss3-adoption-decomp-deltas-v1",
        "scenario": "ADOPTED-CANONICAL",
        "packet": {"batches": [
            {"pool": "b3", "class_index": 20421, "probed_rows": 4,
             "adopted_loss_rows": 3, "unadopted_win_rows": 1,
             "adopted_nodes_per_pool": 14962526, "whole_packet_nodes": 20322520},
        ],
            "adopted_loss_rows": ADOPTED_ROWS,
            "unadopted_win_rows": UNCONSUMED_WIN_ROWS,
            "exhausted_excluded_rows": 0,
            "adopted_total_nodes_per_pass": ADOPTED_TOTAL_NODES,
            "adopted_loss_ids": adopted_ids,
            "unadopted_win_ids": ["d002"],
            "unadopted_win_s5": {"d002": 197253},
            "decisive_labels": "3 fresh LOSS @15M adopted (batch-3 d001/d003/d004, "
                               "2-pass node-exact) + 1 probe-level WIN @15M (d002) "
                               "unconsumed + 0 EXHAUSTED + MISMATCH 0"},
        "cache": {"base_sha256": BASE_CACHE_SHA, "scenario_sha256": SCEN_CACHE_SHA,
                  "base_rows": len(base), "scenario_rows": len(scen), "increment_rows": len(incr),
                  "verdict_counts": {"WIN": 158, "LOSS": 6505},
                  "relation": "scenario == base rows + the 3 increment rows verbatim (no other row changed)",
                  "merge_audit_runs": 3, "merge_audit_sha256_each": MERGE_AUDIT_SHA,
                  "adopted_s5_indices": ADOPTED_S5},
        "class_16371": {"children_total": len(child_keys_16371),
                        "unknown_before": 2, "unknown_after": 2,
                        "adopted_own": 0,
                        "unconsumed_win_children": 2,
                        "base_known_loss_s5_cache": BASE_KNOWN_LOSS_S5_16371,
                        "receipt_known_loss_s5": RECEIPT_LOSS_S5_16371,
                        "status_before": "unknown",
                        "status_after": "unknown (BYTE-STATIC across Part EB: no EB row "
                                        "sits in this class; the 2 unconsumed probe-level "
                                        "WIN children {e042, e002} remain)",
                        "class_rank": [4, 4],
                        "groups_served_count": [3, 3],
                        "unknown_s5_remaining": [183566, 550879],
                        "not_a_root_verdict": "the loss-only adoption of a mixed packet frees "
                                               "nothing and excludes nothing; free_now/coverage "
                                               "quantities are Board-derived scheduling "
                                               "bookkeeping; no root verdict and no coverage "
                                               "claim is made"},
        "class_20421": {"children_total_raw": len(child_keys_20421),
                        "children_total_s5": len(in_s5_20421),
                        "non_s5_precious_cache_child": list(NON_S5_CACHE_KEY_20421),
                        "unknown_before": 9, "unknown_after": 6,
                        "adopted_own": len(own_20421),
                        "unconsumed_win_children": 6,
                        "base_known_loss_s5_cache": sorted(mask_to_index[k] for k in known_base_20421),
                        "receipt_known_loss_s5": [],
                        "status_before": "unknown",
                        "status_after": "unknown (NOT freed, NOT excluded: the 6 unconsumed "
                                        "probe-level WIN children remain)",
                        "class_rank": [8, 7],
                        "groups_served_count": [4, 4],
                        "unknown_s5_remaining": sorted(WIN_S5_PINNED[k] for k in
                                                       ("d002", "d008", "d009", "d021",
                                                        "d026", "d029")),
                        "not_a_root_verdict": "identical guard as class_16371"},
        "closure_table": {"rows_before": CLOSURE_ROWS_BEFORE, "rows_after": CLOSURE_ROWS_AFTER,
                          "left": left, "entered": entered,
                          "left_reason": "EMPTY: the 807-row frontier table is fully static "
                                         "across this Part (no rank-bookkeeping exchange rows)",
                          "unknown_changed_classes": changed,
                          "rank_churn_only_rows": rank_churn,
                          "rank_churn_detail": rank_churn_classes,
                          "groups_served_decrease_churn": gs_dec,
                          "fully_stable_rows": stable},
        "update8": {"resolved_before": UPD8_RESOLVED_BEFORE, "resolved_after": UPD8_RESOLVED_AFTER,
                    "newly_resolved_s5": NEWLY_RESOLVED_UPD8_S5,
                    "newly_resolved_within_adopted": True,
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
                    "note": "the joint greedy union stays 36,511 static and the worklist "
                            "shrinks (64,420 -> 64,417) after class 20421's frontier cost "
                            "drops (unknown 9 -> 6); per-root free/uncovered thirds are "
                            "IDENTICAL at every root (nothing was freed); roots 12/37 "
                            "individual greedy unions shift as pure bookkeeping; per-root "
                            "remaining decreases only at roots 12/37 (-6 each); root 27 "
                            "stays 119/119"},
        "verification": {"kit_files_verified": {"b36": k36},
                          "packet_pins": {"b3_keys": B3_KEYS_SHA, "b3_status": B3_STATUS_SHA},
                          "refresh_scripts_reexecuted": [BASE_REFRESH_SHA, SCEN_REFRESH_SHA],
                          "refresh_outputs_byte_identical": True,
                          "board_child_regeneration": "class-16371 52-child and class-20421 "
                                                      "50-child (49 s5 + 1 pinned non-s5 cache "
                                                      "row) canonical 5-stone boundaries "
                                                      "regenerated via Board(11).children"},
        "interpretation_guard":
            "only the 3 fresh batch-3 LOSS rows are consumed into the canonical cache by "
            "this Part; the probed packet is MIXED: the d002 probe-level WIN row is "
            "consumed NOWHERE and belongs to the scrutiny-owner C++ second-implementation "
            "gate (pin 9193f5b6...); classes 16371 (byte-static, 2 WIN children) and 20421 "
            "(6 WIN children) are NOT freed and NOT excluded; class status stays unknown, "
            "free_now 39 static, closure table 807 rows fully static with NO left/entered "
            "exchange; no root verdict and no coverage claim is made anywhere; the "
            "per-root/greedy/worklist quantities quoted here are bookkeeping, never "
            "verdicts; no update8 resolution was lost; 11x11 stays UNKNOWN",
    }
    (EXP / "output/decomp-deltas-b3loss3-adoption.json").write_text(
        json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("DECOMP OK changed=%d rank_churn=%d gs_dec=%d stable=%d left=%d entered=%d" % (
        len(changed), rank_churn, len(gs_dec), stable, len(left), len(entered)))
    print("class16371: unknown 2 -> 2 (byte-static, no EB row inside), NOT freed")
    print("class20421: unknown 9 -> 6 (3 adopted, 6 unconsumed WINs remain), NOT freed")


if __name__ == "__main__":
    main()
