"""Part DW adoption delta extraction: BASE (Part DT, b33loss45) vs SCENARIO (b35loss26).

Fail-closed machine recomputation of exactly what the batch-35 (class 16757)
26-LOSS canonical adoption changed, from published bytes only:

* every published artifact sha-pinned (the Part DW experiment outputs, the
  Part DT BASE reaudit outputs, both chain caches, the increment, the
  increments manifest, the published batch-35 kit MANIFEST verified
  file-by-file 109 files, graph/update8/board/policy/quarantine pins);
* the published Part DT refresh script (reaudit/scripts/
  refresh_adoption_b33loss45.py, sha 5533b3f9...) and the published Part DW
  refresh fork (reaudit/scripts/refresh_adoption_b35loss26.py, sha
  4aaabcd5...) are RE-EXECUTED byte-verbatim in isolated scratch trees
  against their pinned inputs, and all eight outputs (two x
  refresh-summary/closure-classes/per-root-coverage/probe-worklist) must be
  byte-identical to the published / regenerated pins before any delta is
  emitted (double-run determinism);
* SCEN cache == BASE cache rows + exactly the 26 increment rows (verdict
  agreement everywhere; 6,573 rows, WIN 158 / LOSS 6,415); the manifest is a
  MIXED packet: full_packet_eq_loss_only=false, 2 probe-level WIN rows
  unconsumed, 0 EXHAUSTED rows;
* the class-16757 arithmetic is independently recomputed from the frozen
  dependency graph with the integer-geometry Board: the class's canonical
  5-stone child boundary is regenerated (49 children: 19 base-known exact
  LOSS in the BASE cache + 1 update8-receipt LOSS s5 558600 + 28 batch keys
  + the batch-1 probe-level WIN b018 s5 528497); exactly 26 children
  resolve to LOSS in the scenario (the adopted rows) and exactly 3 stay
  unknown == the 3 unconsumed WIN keys {b018, b032, b048}, so class 16757
  is NOT freed and NOT excluded (it stays an unknown closure class;
  Board-verified by the reaudit refresh: free_now 39 -> 39,
  board_verified 39/39, unknown 34,497 -> 34,497);
* every closure-classes.csv row that changes unknown_now is asserted to be
  a Board-verified holder of adopted keys with exact own-membership
  arithmetic (delta == children-of-class intersect adopted set): beside
  class 16757 (29 -> 3, own 26), exactly two micro-classes change, 30118
  (55 -> 54, own 1) and 30484 (54 -> 52, own 2); rank churn is pure
  bookkeeping and counted (28 rows); NO class leaves or enters the closure
  table (base 807 rows -> scenario 807 rows); the class-16757 row itself
  changes exactly rank 7 -> 4, unknown_now 29 -> 3 with groups_served_count
  static 5 (its 26-adoption delta equals its own adopted children by the
  Board boundary);
* update8 refresh: resolved_among_baseline_requirement grows from 188 to
  214 (+26 == exactly the 26 adopted s5 indices that lie in the frozen
  baseline requirement); remaining 31,671 -> 31,645; no resolution is
  lost; groups_free_now stays 131;
* class_status counts: excluded 390 / excluded_now 23 / free_now 39 /
  unknown 34,497 IDENTICAL before and after (the loss-only adoption frees
  nothing and excludes nothing); root 27 stays 119/119;
* per-root coverage: free/uncovered thirds are IDENTICAL at every root
  (class 16757 did not become free); the individual greedy union changes
  at roots 48 (2968 -> 2942), 36 (2980 -> 2954), 0 (3009 -> 3008) and
  24 (2778 -> 2829) (re-selection bookkeeping after class 16757's frontier
  cost drops 29 -> 3; the root-24 greedy union INCREASES - pure scheduling
  bookkeeping, no coverage claim); per-root remaining decreases only at
  roots 36 (-78) and 48 (-52), the two roots whose groups class 16757
  serves;
* the frozen greedy scheduler deltas are recorded as bookkeeping
  (joint greedy 36,849 -> 36,943, worklist 64,564 -> 64,535).

No unknown verdict is asserted anywhere.  The standard 11x11 empty board
and every one of the 19 central-reply roots stay UNKNOWN; free_now /
coverage quantities are scheduling bookkeeping derived from exact LOSS
verdicts, not root verdict claims.  The two probe-level WIN rows
(b032/b048) and the batch-1 probe-level WIN b018 are consumed NOWHERE by
this Part (scrutiny-owner C++ second-implementation gate pin
9193f5b6...); no WIN verdict and no EXHAUSTED verdict enters the
canonical cache.
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

BASE_EXP = ROOT / "research/experiments/n11-centralreply-class34908-b33loss45-adoption-reaudit-20261124"
BASE_OUT = BASE_EXP / "reaudit/output"
BASE_CACHE = BASE_EXP / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-20261124.cache"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-plus-b35loss26-20261124.cache"
INCR = EXP / "output/increment-b35loss26-20261124.cache"
MANIFEST = EXP / "output/increments-manifest.json"
KIT1 = ROOT / "research/experiments/n11-centralreply-closure-class16757-batch35-20261124"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_REFRESH_SCRIPT = BASE_EXP / "reaudit/scripts/refresh_adoption_b33loss45.py"
SCEN_REFRESH_SCRIPT = EXP / "reaudit/scripts/refresh_adoption_b35loss26.py"

BASE_CACHE_SHA = "973bcd19309eae1d73b26c40c3d6839a2f35baa74658e0794f19da6f9412ca5b"
SCEN_CACHE_SHA = "23d40e36ed1730ace4986461995dfc0ee606a380da9b156cdddaf09ef8a29822"
INCR_SHA = "10cb85892e43be42008558abf021e647256c3b58243c8434c7b2682eb924cb67"
MANIFEST_SHA = "e925cf0c50d2b6985d5354bf8724e2480a2f8db7a38c6883b77e7f2373ca15f8"
BASE_SUMMARY_SHA = "38fc4e193cf08cf4efb7830a8bad3d2245bc732380f44c4ee2913e05d5644732"
BASE_CLOSURE_SHA = "6cc33dd731c5d2237291552a91c3f7d60947bba875867fcab10394b533f1a68d"
BASE_PRC_SHA = "c5a2721d60c641ead369d10184e477cd5156ba7d02561c31dcd77b7b81b6f504"
BASE_WORKLIST_SHA = "5881d7b3b51ef0ce780abaadaf7043c1fbcd3b258b9a261cadd2c539fb35ba61"
SCEN_SUMMARY_SHA = "5fe3e5ab176df05ef30894d6e0df6ceb292d3ac2280ff543e94bbee69e549de4"
SCEN_CLOSURE_SHA = "b7241eb046e32f4900c9f9a976ada326c5124ad18c01de6b4eb40b97a8a7f24e"
SCEN_PRC_SHA = "f1abcd8554cc30c9833c645d67a190957bca975c1d81f9d5031db782683e8154"
SCEN_WORKLIST_SHA = "86767be94e21259507dc75e9092caa935a8c77e2ab80b6c91deebc84fc48eef3"
BASE_REFRESH_SHA = "5533b3f908cff069c6d86c5b96f32c6f978fda6b7ec5e8d32a3302a344363dee"
SCEN_REFRESH_SHA = "4aaabcd5a1a8ac2dc44be600d920b55294d8cc64a1e26b408bbcd45a4b7011fa"
KIT1_MANIFEST_SHA = "791996c1ad86a75cdc630434d2dff6e559583f804527f04dfe377ce123d4155c"
KIT1_FILES = 109
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
BOARD_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
CLASS_IDX = 16757
ADOPTED_ROWS = 26
UNCONSUMED_WIN_ROWS = 2   # probe-level WIN rows carried by the batch-35 kit raws
WIN_S5_PINNED = [556117, 558553]   # b032, b048
B018_ID = "b018"
B018_KEY = (1153204079095189504, 65536)
B018_S5 = 528497
EXHAUSTED_EXCLUDED_ROWS = 0
ADOPTED_TOTAL_NODES = 67593391
ALL28_TOTAL_NODES = 73757659
BOUNDARY_CHILDREN = 49
BASE_KNOWN_LOSS_S5 = [82690, 194261, 297931, 299014, 391206, 392179, 473572,
                      474401, 495020, 498907, 503090, 507102, 509890, 513542,
                      516932, 520108, 523270, 530835, 533411]
RECEIPT_LOSS_S5 = [558600]
BATCH_KEYS_TOTAL = 28
UNCONSUMED_WIN_IDS = ["b032", "b048"]
EXHAUSTED_IDS = []
NEWLY_RESOLVED_UPD8_S5 = [535179, 537545, 539592, 541610, 545364, 546902,
                          548070, 549153, 551777, 554104, 555161, 558018,
                          558054, 558079, 558120, 558183, 558228, 558261,
                          558283, 558334, 558367, 558393, 558410, 558443,
                          558486, 558506]
MERGE_AUDIT_SHA = "a2548c1a8151fd16be49dc9241008c6d1268142e34bdcdac98ba31e42309d756"
STATUS_BEFORE = {"excluded": 390, "excluded_now": 23, "free_now": 39, "unknown": 34497}
STATUS_AFTER = {"excluded": 390, "excluded_now": 23, "free_now": 39, "unknown": 34497}
UPD8_RESOLVED_BEFORE = 188
UPD8_RESOLVED_AFTER = 214
UPD8_REMAINING_BEFORE = 31671
UPD8_REMAINING_AFTER = 31645
JOINT_GREEDY_BEFORE = 36849
JOINT_GREEDY_AFTER = 36943
WORKLIST_BEFORE = 64564
WORKLIST_AFTER = 64535
KNOWN_UNIVERSE_BEFORE = 726
KNOWN_UNIVERSE_AFTER = 752
CACHE_IN_UNIVERSE_BEFORE = 703
CACHE_IN_UNIVERSE_AFTER = 729
CACHE_VERDICTS_BEFORE = {"1": 158, "2": 6389}
CACHE_VERDICTS_AFTER = {"1": 158, "2": 6415}
UNIQUE_GROUPS_BEFORE = 2115
UNIQUE_GROUPS_AFTER = 2115
PER_ROOT_REMAINING_DELTA = {"36": -78, "48": -52}
PER_ROOT_COVERAGE_DELTA = {
    "0": {"free": [7, 7], "uncovered": [112, 112], "greedy": [3009, 3008]},
    "24": {"free": [12, 12], "uncovered": [107, 107], "greedy": [2778, 2829]},
    "36": {"free": [4, 4], "uncovered": [115, 115], "greedy": [2980, 2954]},
    "48": {"free": [7, 7], "uncovered": [112, 112], "greedy": [2968, 2942]},
}
CLOSURE_ROWS_BEFORE = 807
CLOSURE_ROWS_AFTER = 807
CLASS_16757_ROW_BEFORE = {"class_rank": "7", "unknown_now": "29", "groups_served_count": "5"}
CLASS_16757_ROW_AFTER = {"class_rank": "4", "unknown_now": "3", "groups_served_count": "5"}
GS_CHURN_DECREASE = []
CHANGED_CLASS_SET = [
    {"class_index": 30118, "unknown_before": 55, "unknown_after": 54, "own_adopted": 1},
    {"class_index": 30484, "unknown_before": 54, "unknown_after": 52, "own_adopted": 2},
]


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
        want, rel = line.split(None, 1)
        p = next((c for c in _kit_candidates(dirp, rel) if c.is_file()), None)
        if p is None:
            fail(f"kit {dirp.name} file missing: {rel}")
        if sha(p) != want:
            fail(f"kit {dirp.name} sha drift at {rel}")
        n += 1
    if n != files_expected:
        fail(f"kit {dirp.name} files {n} != {files_expected}")
    return n


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
    k1 = verify_kit(KIT1, KIT1_MANIFEST_SHA, KIT1_FILES)

    manifest = json.loads(MANIFEST.read_text())
    batch = manifest["batches"][0]
    adopted_ids = manifest["loss_ids"]
    win_ids = manifest["unadopted_win_ids"]
    exh_ids = manifest["exhausted_excluded_ids"]
    if len(adopted_ids) != ADOPTED_ROWS:
        fail(f"manifest adopted id count drift ({len(adopted_ids)} != {ADOPTED_ROWS})")
    if sorted(win_ids) != UNCONSUMED_WIN_IDS or sorted(exh_ids) != EXHAUSTED_IDS:
        fail("manifest unconsumed WIN / EXHAUSTED id sets drift vs the pinned batch-35 packet")
    if batch["class_index"] != CLASS_IDX or batch["batch"] != 35 or batch["keys_total"] != 28:
        fail("manifest batch identity drift")
    if manifest.get("full_packet_eq_loss_only") is not False:
        fail("batch-35 is a MIXED packet: manifest full_packet_eq_loss_only must be false")
    if manifest.get("win_scenario_exists") is not True:
        fail("manifest win_scenario_exists must be true (2 probe-level WIN rows exist)")
    if sorted(manifest["resolved_ids"]) != sorted(adopted_ids):
        fail("manifest resolved_ids != loss_ids")
    if batch["total_nodes_pass_one"] != ADOPTED_TOTAL_NODES or batch["total_nodes_pass_two"] != ADOPTED_TOTAL_NODES:
        fail("manifest node totals drift")
    if batch.get("status_log_lines") != 30:
        fail("manifest status-log honest-history line count drift")
    win_s5 = sorted(r["s5_index"] for r in manifest["unadopted_win_rows"])
    exh_s5 = sorted(r["s5_index"] for r in manifest["exhausted_rows"])
    if win_s5 != WIN_S5_PINNED or exh_s5 != []:
        fail("manifest WIN/EXHAUSTED row decomposition drift")
    unconsumed_s5 = win_s5 + exh_s5

    # --- refresh re-execution (double-run determinism) ---------------------
    base_tmp = rerun_refresh(BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA, ".dwverify-base-b33loss45")
    scen_tmp = rerun_refresh(SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA, ".dwverify-scen-b35loss26")
    checks = [
        (base_tmp / "refresh-summary.json", BASE_OUT / "refresh-summary.json", BASE_SUMMARY_SHA),
        (base_tmp / "closure-classes.csv", BASE_OUT / "closure-classes.csv", BASE_CLOSURE_SHA),
        (base_tmp / "per-root-coverage.csv", BASE_OUT / "per-root-coverage.csv", BASE_PRC_SHA),
        (base_tmp / "probe-worklist.csv", None, BASE_WORKLIST_SHA),
        (scen_tmp / "refresh-summary.json", EXP / "reaudit/output/refresh-summary.json", SCEN_SUMMARY_SHA),
        (scen_tmp / "closure-classes.csv", EXP / "reaudit/output/closure-classes.csv", SCEN_CLOSURE_SHA),
        (scen_tmp / "per-root-coverage.csv", EXP / "reaudit/output/per-root-coverage.csv", SCEN_PRC_SHA),
        (scen_tmp / "probe-worklist.csv", EXP / "reaudit/output/probe-worklist.csv", SCEN_WORKLIST_SHA),
    ]
    for tmp_out, pub, want_sha in checks:
        if sha(tmp_out) != want_sha:
            fail(f"refresh re-execution output drift: {tmp_out.name} ({tmp_out.parent.parent.name})")
        if pub is not None and sha(pub) != want_sha:
            fail(f"published output drifted from pin: {pub}")
    shutil.rmtree(ROOT / "research/experiments/.dwverify-base-b33loss45")
    shutil.rmtree(ROOT / "research/experiments/.dwverify-scen-b35loss26")

    # --- cache relation: SCEN == BASE + exactly the 45 increment rows ------
    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    incr = load_cache(INCR)
    if len(base) != 6547 or len(scen) != 6573 or len(incr) != ADOPTED_ROWS:
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
    if (wins, losses) != (158, 6415):
        fail(f"scenario verdict counts {wins}/{losses} != 158/6,415")
    for key, row in incr.items():
        v, n = row
        nodes = scen[key][1]
        if n != nodes:
            fail(f"scenario nodes for {key} differ from increment: {nodes} != {n}")

    # --- Board arithmetic for class 16757 ---------------------------------
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
    lo, hi = s4_masks[CLASS_IDX]
    board = Board(11)
    children = board.children(lo | (hi << 64))
    child_keys = {(c & ((1 << 64) - 1), c >> 64) for c in children}
    bkeys = json.loads((KIT1 / "input/batch-keys-b35.json").read_text())["keys"]
    batch_keys = {(int(e["lo"]), int(e["hi"])) for e in bkeys}
    if len(batch_keys) != BATCH_KEYS_TOTAL or not batch_keys <= child_keys:
        fail("batch-35 key set not inside the Board-regenerated class-16757 child boundary")
    if len(child_keys) != BOUNDARY_CHILDREN:
        fail(f"class-16757 Board child boundary {len(child_keys)} != {BOUNDARY_CHILDREN} (19 base LOSS + 1 receipt LOSS + 28 batch + b018)")
    update8 = json.loads(UPDATE8.read_text())
    receipt_verdicts = {int(k): int(v) for k, v in update8["resolved_s5_verdicts"].items()}
    receipt_child = {k for k in child_keys if mask_to_index[k] in receipt_verdicts}
    if sorted(mask_to_index[k] for k in receipt_child) != RECEIPT_LOSS_S5:
        fail("the update8-receipt LOSS children of 16757 != the pinned receipt set")
    for k in receipt_child:
        if receipt_verdicts[mask_to_index[k]] != 2:
            fail("an update8-receipt child of 16757 is not LOSS")
        if k in base or k in scen:
            fail("a receipt child of 16757 is also a cache row")
    unknown_base = {k for k in child_keys if k not in base and k not in receipt_child}
    unknown_scen = {k for k in child_keys if k not in scen and k not in receipt_child}
    exp_unknown_base = batch_keys | {B018_KEY}
    if len(unknown_base) != 29 or unknown_base != exp_unknown_base:
        fail("BASE unknown children of 16757 != the 28 batch keys + b018 (29)")
    if len(unknown_scen) != 3:
        fail(f"scenario unknown children of 16757 = {len(unknown_scen)} != 3 (b018 + b032 + b048; class NOT freed)")
    if sorted(mask_to_index[k] for k in unknown_scen) != sorted([B018_S5] + WIN_S5_PINNED):
        fail("scenario unknown children != the pinned 3 unconsumed WIN keys (b018, b032, b048)")
    adopted_keys = batch_keys - unknown_scen
    if len(adopted_keys) != ADOPTED_ROWS or {mask_to_index[k] for k in adopted_keys} != {mask_to_index[k] for k in incr}:
        fail("adopted key set != increment key set (child-boundary mismatch)")
    if sorted(mask_to_index[k] for k in adopted_keys) == sorted([B018_S5] + WIN_S5_PINNED):
        fail("adopted set collides with the unconsumed WIN set")
    adopted_idx = sorted(mask_to_index[k] for k in adopted_keys)
    if adopted_idx != NEWLY_RESOLVED_UPD8_S5:
        fail("adopted s5 set != the pinned adopted s5 list")
    base_known = child_keys - batch_keys - {B018_KEY} - receipt_child
    if len(base_known) != 19 or sorted(mask_to_index[k] for k in base_known) != BASE_KNOWN_LOSS_S5:
        fail("the 19 base-known exact-LOSS children of 16757 != the pinned s5 indices")
    if any(base.get(k, (0, 0))[0] != 2 for k in base_known):
        fail("a base-known child of 16757 is not an exact LOSS in BASE")
    for k in adopted_keys:
        if scen[k][0] != 2:
            fail(f"an adopted child of 16757 is not an exact LOSS in the scenario: {k}")
    if any(k in quarantined for k in child_keys):
        fail("a quarantined key sits inside the class-16757 child boundary")


    # --- update8 refresh deltas ---------------------------------------------
    update8 = json.loads(UPDATE8.read_text())
    required = set(update8["required_new_s5"])
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
        fail(f"newly resolved update8 set != the pinned adopted-in-requirement set: {newly}")
    if lost:
        fail(f"update8 resolution LOST rows: {sorted(lost)}")
    if not set(newly) <= set(adopted_idx):
        fail("newly resolved update8 set is not a subset of the adopted s5 set")
    if rb["remaining_now"] - rs["remaining_now"] != len(NEWLY_RESOLVED_UPD8_S5):
        fail("update8 remaining delta != the pinned newly-resolved count")
    if rb["groups_free_now"] != 131 or rs["groups_free_now"] != 131:
        fail("update8 groups_free_now drift (must stay 131 static)")

    # --- class status / universe metrics --------------------------------------
    cb, cs = base_summary["class_status_counts"], scen_summary["class_status_counts"]
    if cb != STATUS_BEFORE or cs != STATUS_AFTER:
        fail(f"class status counts drift vs the pinned static transition: {cb} {cs}")
    if scen_summary["board_verification"] != {"free_candidates": 39, "board_verified_free": 39, "rejected": {}}:
        fail("scenario board verification shape drift")
    if base_summary["board_verification"] != {"free_candidates": 39, "board_verified_free": 39, "rejected": {}}:
        fail("base board verification shape drift")
    if scen_summary["inputs"]["cache_rows"] != 6573 or scen_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_AFTER \
            or scen_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_AFTER:
        fail("scenario inputs metrics drift")
    if base_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["cache_rows"] != 6547:
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
        fail(f"per-root coverage delta {prc_delta} != the pinned re-selection churn {PER_ROOT_COVERAGE_DELTA}")
    for root, d in prc_delta.items():
        if d["free"][0] != d["free"][1] or d["uncovered"][0] != d["uncovered"][1]:
            fail(f"root {root} free/uncovered thirds changed although no class was freed")
        # the root-24 greedy union INCREASES (2778 -> 2829) as pure
        # re-selection bookkeeping; the pinned delta equality is the machine check
    root27 = [s for b, s in prc_pairs if s["first"] == "27"][0]
    if root27["free_now"] != "119" or root27["uncovered"] != "0":
        fail("root 27 coverage regressed")
    # per-root greedy remaining decreases only at the roots whose groups
    # the (still-unknown) class 34908 serves: first 0 and first 12
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
    if left or entered:
        fail(f"closure table left/entered non-empty (adoption must not free any class): {left} {entered}")
    if CLASS_IDX not in cb_t or CLASS_IDX not in cs_t:
        fail("class 34908 must remain in BOTH closure tables (not freed, not excluded)")
    for col, want in CLASS_16757_ROW_BEFORE.items():
        if cb_t[CLASS_IDX][col] != want:
            fail(f"base class-16757 row {col} drift: {cb_t[CLASS_IDX][col]} != {want}")
    for col, want in CLASS_16757_ROW_AFTER.items():
        if cs_t[CLASS_IDX][col] != want:
            fail(f"scenario class-16757 row {col} drift: {cs_t[CLASS_IDX][col]} != {want}")
    own_34908 = len(child_keys & set(adopted_keys))
    if int(cb_t[CLASS_IDX]["unknown_now"]) - int(cs_t[CLASS_IDX]["unknown_now"]) != own_34908 \
            or own_34908 != ADOPTED_ROWS:
        fail("class-16757 unknown delta != its own adopted children (Board boundary)")
    changed, rank_churn, stable, gs_dec, gs_bad = [], 0, 0, [], []
    for ci, brow in sorted(cb_t.items()):
        if ci == CLASS_IDX:
            continue
        srow = cs_t[ci]
        diff = {k: (brow[k], srow[k]) for k in brow if brow[k] != srow[k]}
        if not diff:
            stable += 1
            continue
        if set(diff) == {"class_rank"}:
            rank_churn += 1
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
        own = len(kids_keys & set(adopted_keys))
        if (b_unk - s_unk) != own or own == 0:
            fail(f"class {ci} unknown delta {b_unk}->{s_unk} != own adopted membership {own}")
        changed.append({"class_index": ci, "unknown_before": b_unk, "unknown_after": s_unk,
                        "own_adopted": own})
    if changed != CHANGED_CLASS_SET:
        fail(f"changed-class set != the pinned 2-micro-class set: {changed}")
    for e in gs_dec:
        if e["unknown_now"][0] != e["unknown_now"][1]:
            fail(f"groups_served_churn class {e['class_index']} changed unknown_now: {e}")
    if gs_dec != GS_CHURN_DECREASE:
        fail(f"groups_served_count churn set != the pinned empty churn: {gs_dec}")
    scen_first = scen_summary["closure_classes_first"]
    c16757_first = [e for e in scen_first if e["class_index"] == CLASS_IDX]
    if len(c16757_first) != 1 or c16757_first[0]["unknown_now"] != 3 or len(c16757_first[0]["groups_served"]) != 5:
        fail("scenario closure_classes_first entry for class 16757 drift (rank-4 / 3-unknown / 5-group)")

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
        "schema": "b35loss26-adoption-decomp-deltas-v1",
        "scenario": "ADOPTED-CANONICAL",
        "batch": {"batch": 35, "class_index": CLASS_IDX, "probed_rows": 28,
                  "adopted_loss_rows": ADOPTED_ROWS, "unadopted_win_rows": UNCONSUMED_WIN_ROWS,
                  "exhausted_excluded_rows": EXHAUSTED_EXCLUDED_ROWS,
                  "adopted_total_nodes_per_pass": ADOPTED_TOTAL_NODES,
                  "all28_total_nodes": ALL28_TOTAL_NODES,
                  "decisive_labels": "26 LOSS @15M adopted + 2 probe-level WIN @15M (unconsumed) + "
                                     "0 EXHAUSTED + MISMATCH 0 (Part DV probe drive kit raws, "
                                     "2-pass fresh-cold); batch-1 probe-level WIN b018 stays "
                                     "unconsumed outside this packet",
                  "adopted_loss_ids": adopted_ids,
                  "unadopted_win_ids": win_ids,
                  "unadopted_win_s5": win_s5,
                  "exhausted_excluded_ids": exh_ids,
                  "exhausted_s5": exh_s5},
        "cache": {"base_sha256": BASE_CACHE_SHA, "scenario_sha256": SCEN_CACHE_SHA,
                  "base_rows": len(base), "scenario_rows": len(scen), "increment_rows": len(incr),
                  "verdict_counts": {"WIN": 158, "LOSS": 6415},
                  "relation": "scenario == base rows + the 26 increment rows verbatim (no other row changed)",
                  "merge_audit_runs": 3, "merge_audit_sha256_each": MERGE_AUDIT_SHA},
        "class_16757": {"children_total": len(child_keys),
                        "unknown_before": 29, "unknown_after": 3,
                        "adopted_own": ADOPTED_ROWS,
                        "unconsumed_win_children": 3,
                        "exhausted_children": 0,
                        "base_known_loss_s5_cache": BASE_KNOWN_LOSS_S5,
                        "receipt_known_loss_s5": RECEIPT_LOSS_S5,
                        "b018_key": list(B018_KEY),
                        "status_before": "unknown",
                        "status_after": "unknown (NOT freed, NOT excluded: 3 unconsumed WIN "
                                        "children remain (b018, b032, b048); Board-verified by "
                                        "the reaudit refresh free_now 39 -> 39, board_verified "
                                        "39/39, unknown 34,497 static)",
                        "class_rank": [7, 4],
                        "groups_served_count": [5, 5],
                        "not_a_root_verdict": "the loss-only adoption of a mixed packet frees nothing and "
                                               "excludes nothing; free_now/coverage quantities are "
                                               "Board-derived scheduling bookkeeping; no root verdict and "
                                               "no coverage claim is made"},
        "closure_table": {"rows_before": CLOSURE_ROWS_BEFORE, "rows_after": CLOSURE_ROWS_AFTER,
                          "left": [], "entered": [],
                          "left_reason": "no class left the closure table (class 16757 is not freed)",
                          "unknown_changed_classes": changed,
                          "rank_churn_only_rows": rank_churn,
                          "groups_served_decrease_churn": gs_dec,
                          "fully_stable_rows": stable},
        "update8": {"resolved_before": UPD8_RESOLVED_BEFORE, "resolved_after": UPD8_RESOLVED_AFTER,
                    "newly_resolved_s5": NEWLY_RESOLVED_UPD8_S5,
                    "newly_resolved_within_adopted": True,
                    "remaining_before": UPD8_REMAINING_BEFORE, "remaining_after": UPD8_REMAINING_AFTER,
                    "groups_free_now_static": 131},
        "class_status_counts_before": STATUS_BEFORE,
        "class_status_counts_after": STATUS_AFTER,
        "metrics": {"joint_greedy_union_size": [JOINT_GREEDY_BEFORE, JOINT_GREEDY_AFTER],
                    "worklist_total": [WORKLIST_BEFORE, WORKLIST_AFTER],
                    "known_universe_indices": [KNOWN_UNIVERSE_BEFORE, KNOWN_UNIVERSE_AFTER],
                    "cache_rows_in_universe": [CACHE_IN_UNIVERSE_BEFORE, CACHE_IN_UNIVERSE_AFTER],
                    "unique_groups": [UNIQUE_GROUPS_BEFORE, UNIQUE_GROUPS_AFTER],
                    "per_root_remaining_delta": PER_ROOT_REMAINING_DELTA,
                    "per_root_coverage_delta": PER_ROOT_COVERAGE_DELTA,
                    "note": "greedy/worklist deltas are frozen-scheduler bookkeeping after class-16757's "
                            "frontier cost drops 29 -> 3: the joint greedy union rises "
                            "(36,849 -> 36,943: re-selection churn, no coverage claim) and the worklist "
                            "shrinks (64,564 -> 64,535); per-root free/uncovered thirds are IDENTICAL at "
                            "every root (nothing was freed); the root-24 individual greedy union "
                            "INCREASES (2778 -> 2829) as pure bookkeeping; per-root remaining decreases "
                            "only at roots 36 (-78) and 48 (-52) whose groups class 16757 serves; "
                            "root 27 stays 119/119"},
        "verification": {"kit_files_verified": {"kit1": k1},
                         "refresh_scripts_reexecuted": [BASE_REFRESH_SHA, SCEN_REFRESH_SHA],
                         "refresh_outputs_byte_identical": True,
                         "board_child_regeneration": "class-16757 canonical 49-child 5-stone boundary "
                                                      "regenerated via Board(11).children "
                                                      "(19 base-known exact LOSS + 1 update8-receipt LOSS "
                                                      "{558600} + 28 batch keys + the unconsumed WIN b018)"},
        "interpretation_guard":
            "only the 26 fresh LOSS rows are consumed into the canonical cache by this Part; "
            "batch-35 is a MIXED packet: the 2 probe-level WIN rows (b032/b048) are consumed "
            "NOWHERE and belong to the scrutiny-owner C++ second-implementation gate (pin "
            "9193f5b6...), and the batch-1 probe-level WIN b018 stays unconsumed outside this "
            "packet; class 16757 is NOT freed and NOT excluded (3 verdict-pending WIN children "
            "remain; class status stays unknown, free_now 39 static, closure table 807 rows "
            "static); no root verdict and no coverage claim is made anywhere; the per-root/"
            "greedy/worklist quantities quoted here are bookkeeping, never verdicts; no update8 "
            "resolution was lost; 11x11 stays UNKNOWN",
    }
    (EXP / "output/decomp-deltas-b35loss26-adoption.json").write_text(
        json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("DECOMP OK changed=%d rank_churn=%d gs_dec=%d stable=%d" % (len(changed), rank_churn, len(gs_dec), stable))
    print("class16757: unknown 29 -> 3 (26 adopted, 3 unconsumed WINs remain), NOT freed; left=[] entered=[]")


if __name__ == "__main__":
    main()
