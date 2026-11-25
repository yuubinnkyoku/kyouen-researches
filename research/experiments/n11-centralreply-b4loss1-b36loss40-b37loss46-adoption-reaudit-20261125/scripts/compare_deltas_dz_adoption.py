"""Part DZ adoption delta extraction: BASE (Part DW, b35loss26) vs SCENARIO (b4loss1+b36loss40+b37loss46).

Fail-closed machine recomputation of exactly what the three-batch 87-LOSS
canonical adoption (batch-4 e001 class 16371 + batch-36 40 LOSS class 20421 +
batch-37 46 LOSS class 16371) changed, from published bytes only:

* every published artifact sha-pinned (the Part DW experiment outputs, the
  Part DZ experiment outputs, both chain caches, the three increments, the
  increments manifest, the published batch-36/batch-37 kit MANIFEST files
  verified file-by-file (160 + 166 files), the batch-4 kit pinned
  file-by-file - status.log, batch-keys.json, both honest passes of e001,
  both passes of e002, runbatch.sh, jsreplay.js - plus graph/update8/board/
  policy/quarantine pins);
* the published Part DW refresh script (reaudit/scripts/
  refresh_adoption_b35loss26.py, sha 4aaabcd5...) and the published Part DZ
  refresh fork (reaudit/scripts/refresh_adoption_dz.py, sha cbb1d2b7...)
  are RE-EXECUTED byte-verbatim in isolated scratch trees against their
  pinned inputs, and all eight outputs (two x refresh-summary/
  closure-classes/per-root-coverage/probe-worklist) must be byte-identical
  to their pins before any delta is emitted (double-run determinism; the
  scenario probe-worklist.csv itself stays UNPUBLISHED and is pinned as a
  regen sha only);
* SCEN cache == BASE cache rows + exactly the 87 increment rows across the
  three increments (verdict agreement everywhere, all adopted rows LOSS;
  6,660 rows, WIN 158 / LOSS 6,502);
* the manifests are MIXED packets: seven probe-level WIN rows stay
  unconsumed (batch-36 d008/d009/d021/d026/d029, batch-37 e042, batch-4
  e002); the already-canonical dual-class child e022 (s5 546606) was
  excluded at selection and enters nothing;
* the class-16371 and class-20421 arithmetic is independently recomputed
  from the frozen dependency graph with the integer-geometry Board:
  class 16371's canonical 5-stone child boundary regenerates 52 children
  (1 base cache LOSS e022 s5 546606 + 2 update8-receipt LOSS s5 {381858,
  550881} + the 47 batch-37 keys + e001 + e002); exactly 47 children
  resolve to LOSS in the scenario (batch-37's 46 + e001) and exactly 2 stay
  unknown == the 2 unconsumed WIN keys {e042 s5 550879, e002 s5 183566};
  class 20421's boundary regenerates 50 children (1 base cache LOSS child
  outside the s5 universe key (10378545341275312128, 131072) + 45 batch-36
  keys + 4 batch-3 honest-labeled rows whose raws are NOT yet published);
  exactly 40 children resolve to LOSS in the scenario and exactly 9 stay
  unknown == the 5 unconsumed batch-36 WIN keys {528689, 543795, 605961,
  620742, 625899} + the 4 batch-3 unconsumed keys {38215, 197253, 259023,
  300778}; BOTH classes stay unknown closure classes (NOT free, NOT
  excluded; free_now 39 static, board_verified 39/39, unknown 34,497
  static);
* every closure-classes.csv row that changes unknown_now is asserted to be
  a Board-verified holder of adopted keys with exact own-membership
  arithmetic; beside the two macro classes (16371: 49 -> 2 own 47; 20421:
  49 -> 9 own 40) exactly 25 micro-classes change, each by exactly 1 own
  adopted child; the two macro row deltas equal their own adopted children
  by the Board boundary; rank churn is pure bookkeeping (348 rows) and
  groups_served_count never changes (0 rows);
* the closure table stays 807 rows but is a fixed-size frontier selection:
  exactly 4 classes leave and 4 enter as re-selection bookkeeping - the 4
  left rows own ZERO adopted children (pure displacement of the fixed-807
  tail after the two macro frontier costs collapse); each of the 4 entered
  rows owns exactly ONE adopted child (its frontier cost improved, pure
  scheduling bookkeeping; Board-verified: unknown_before - unknown_after ==
  own); NONE is freed (free_now stays 39, class_status_counts static) -
  left {1530, 6241, 15393, 23410}, entered {16367, 18047, 21857, 23034},
  all 8 rows pinned;
* update8 refresh: resolved_among_baseline_requirement grows 214 -> 256
  (+42 == exactly the adopted s5 indices that lie in the frozen baseline
  requirement: batch-36's 40 + batch-37's 498207 and 544907); remaining
  31,645 -> 31,603; no resolution is lost; groups_free_now stays 131;
* class_status counts: excluded 390 / excluded_now 23 / free_now 39 /
  unknown 34,497 IDENTICAL before and after (the loss-only adoption frees
  nothing and excludes nothing); root 27 stays 119/119;
* per-root coverage: free/uncovered thirds are IDENTICAL at every root
  (no class became free); the individual greedy union changes at 8 roots
  {48, 37, 26, 36, 14, 24, 12, 0} (re-selection bookkeeping after the two
  macro frontier costs collapse; greedy unions may increase or decrease -
  pure scheduling bookkeeping, no coverage claim); per-root remaining
  decreases only at roots 1 (-4), 12 (-80), 26 (-4), 37 (-80);
* the frozen greedy scheduler deltas are recorded as bookkeeping
  (joint greedy 36,943 -> 36,511, worklist 64,535 -> 64,420).

No unknown verdict is asserted anywhere.  The standard 11x11 empty board
and every one of the 19 central-reply roots stay UNKNOWN; free_now /
coverage quantities are scheduling bookkeeping derived from exact LOSS
verdicts, not root verdict claims.  The seven probe-level WIN rows and the
batch-3 honest-labeled rows are consumed NOWHERE by this Part
(scrutiny-owner C++ second-implementation gate pin 9193f5b6...); no WIN
verdict and no EXHAUSTED verdict enters the canonical cache.
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

BASE_EXP = ROOT / "research/experiments/n11-centralreply-class16757-b35loss26-adoption-reaudit-20261124"
BASE_OUT = BASE_EXP / "reaudit/output"
BASE_CACHE = BASE_EXP / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-plus-b35loss26-20261124.cache"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-plus-b35loss26-plus-b4loss1-plus-b36loss40-plus-b37loss46-20261125.cache"
INCR_B4 = EXP / "output/increment-b4loss1-20261125.cache"
INCR_B36 = EXP / "output/increment-b36loss40-20261125.cache"
INCR_B37 = EXP / "output/increment-b37loss46-20261125.cache"
MANIFEST = EXP / "output/increments-manifest.json"
KIT_B36 = ROOT / "research/experiments/n11-centralreply-closure-class20421-batch36-20261124"
KIT_B37 = ROOT / "research/experiments/n11-centralreply-closure-class16371-batch37-20261125"
KIT_B4 = ROOT / "research/experiments/n11-centralreply-closure-class16371-batch4-20261122"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_REFRESH_SCRIPT = BASE_EXP / "reaudit/scripts/refresh_adoption_b35loss26.py"
SCEN_REFRESH_SCRIPT = EXP / "reaudit/scripts/refresh_adoption_dz.py"

BASE_CACHE_SHA = "23d40e36ed1730ace4986461995dfc0ee606a380da9b156cdddaf09ef8a29822"
SCEN_CACHE_SHA = "4a30b88dba782138585f16e1ad0ea65da55431dbc2c59250998fc5a1331349c9"
INCR_B4_SHA = "d238c7d8a96885ce184f0d12ef7f23c4b8c09c31bf6fc5e7135cca56b73a2d17"
INCR_B36_SHA = "e6ac36278dc03cac3541a61a79d49c2a54b367c571a3ec2d384de12ce220cbfa"
INCR_B37_SHA = "835adcb09f57a2edd50701b19feda2e8978e4a8a648224d675c6a6fcb4f378a4"
MANIFEST_SHA = "bf7817f96c73b5c060ed9475d867cd068606997d324146d8ad349cf7775892da"
BASE_SUMMARY_SHA = "5fe3e5ab176df05ef30894d6e0df6ceb292d3ac2280ff543e94bbee69e549de4"
BASE_CLOSURE_SHA = "b7241eb046e32f4900c9f9a976ada326c5124ad18c01de6b4eb40b97a8a7f24e"
BASE_PRC_SHA = "f1abcd8554cc30c9833c645d67a190957bca975c1d81f9d5031db782683e8154"
BASE_WORKLIST_SHA = "86767be94e21259507dc75e9092caa935a8c77e2ab80b6c91deebc84fc48eef3"
SCEN_SUMMARY_SHA = "7f7465ab189798e8a0214803daf6200a3c6c32f96318223b204d8ca45bbebc26"
SCEN_CLOSURE_SHA = "026412359c9c025d2dbcfc694fe981c8db30507738942c9a995769010248039b"
SCEN_PRC_SHA = "f7418e980a9753bedafd85857c839f7c21545397913b01a0762224e4c7c7a6d8"
SCEN_WORKLIST_SHA = "9b4208758e22be467919e09d6f83eb15443fa84b8e84495b6ff87cbae150ceae"
BASE_REFRESH_SHA = "4aaabcd5a1a8ac2dc44be600d920b55294d8cc64a1e26b408bbcd45a4b7011fa"
SCEN_REFRESH_SHA = "cbb1d2b753975563efa193b06a56919b6e1758ab13bcfcedc77d0bfd76751e56"
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
MERGE_AUDIT_SHA = "49592ccc249969a428e49e8d9b7dd4749c7b784f5ee356ce1eadcb9c6dde1613"
KIT_B36_MANIFEST_SHA = "f4a6d53f65694b1393767d562a14266d8bc91b3f255ba23c5d828414adcd0826"
KIT_B36_FILES = 160
KIT_B36_KEYS_SHA = "d59182030ce1ade5ad02c8db3836291e2feadfa84325fd4729001e80bfc0c815"
KIT_B37_MANIFEST_SHA = "e4a9d32691bc045e296f6a64f7d277086ce02b1c5bb02f4e71badb9fa6c0a455"
KIT_B37_FILES = 166
KIT_B37_KEYS_SHA = "25b9388e9f855f30bf334bc825f483dbe66becc5c49b918bd1aaa74d3f3765a8"
KIT_B4_KEYS_SHA = "70b8a4c89f7cea454bfd2b52f720245b6d9c5d7311878bf8aac637940825ecdf"
KIT_B4_STATUS_SHA = "63c2d9693a374453bea604b85e1b69ac41c06a214675ea63100a675b1f064ac0"
KIT_B4_E001_P1_SHA = "84a3c2877fe928dc013eebe70706927178be30085b6a02e489574691c88228a4"
KIT_B4_E001_P2_SHA = "84a3c2877fe928dc013eebe70706927178be30085b6a02e489574691c88228a4"
KIT_B4_E002_P1_SHA = "8108953223410bcb73e1c66fad48f52af8437ad03a164688fea0d97db93eb5e7"
KIT_B4_E002_P2_SHA = "1914d0485d66327e28bd938d25d812bea8de28d4986d3324067dcd5d10d5aaa2"
KIT_B4_RUNBATCH_SHA = "4e47fd12234e9d9cc4f94bbd3e80d8c06805836a6f0ac4285d16e1f0d966b05f"
JSREPLAY_SHA = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
BOARD_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

CLASS_A = 16371
CLASS_B = 20421
ADOPTED_ROWS = 87
ADOPTED_ROWS_B4 = 1
ADOPTED_ROWS_B36 = 40
ADOPTED_ROWS_B37 = 46
UNCONSUMED_WIN_IDS = ["d008", "d009", "d021", "d026", "d029", "e002", "e042"]
UNCONSUMED_WIN_ROWS = 7
E001_KEY = (10376575016706768896, 16)
E001_S5 = 93170
E002_KEY = (1153765929805414400, 16)
E002_S5 = 183566
E042_S5 = 550879
# class 16371 boundary decomposition (52 children)
A_CHILDREN = 52
A_BASE_CACHE_S5 = [546606]                  # e022, already canonical before this Part
A_RECEIPT_LOSS_S5 = [381858, 550881]        # update8 receipts, LOSS
A_B37_KEYS_IN_BOUNDARY = 47                  # all of batch-37 (46 adopted LOSS + e042 WIN)
A_B4_KEYS_IN_BOUNDARY = 50                   # the whole batch-4 packet lies in the boundary
                                             # (e001 adopted + e002 WIN-probed; e003..e049 minus
                                             #  e022 re-probed as batch-37; e050 unprobed)
A_UNKNOWN_BEFORE = 49
A_UNKNOWN_AFTER = 2
A_UNKNOWN_AFTER_S5 = [183566, 550879]        # e002 + e042, both unconsumed WIN
A_ADOPTED_OWN = 47
A_ADOPTED_OWN_S5 = [93170, 306951, 399422, 480806, 498207, 502385, 505442,
                    509234, 512923, 516385, 522643, 525693, 528188, 530117,
                    532225, 534675, 537035, 541141, 543110, 544907, 547319,
                    548819, 549855, 550280, 550330, 550357, 550403, 550446,
                    550549, 550593, 550622, 550719, 550757, 550795, 550839,
                    550868, 550876, 550877, 550878, 550880, 550882, 550883,
                    550884, 550885, 550886, 550887, 550888]
# class 20421 boundary decomposition (50 children)
B_CHILDREN = 50
B_OUTSIDE_KEY = (10378545341275312128, 131072)   # base cache LOSS row outside the s5 universe
B_B36_KEYS_IN_BOUNDARY = 45                      # all of batch-36 (40 adopted LOSS + 5 WIN)
B_UNKNOWN_BEFORE = 49                            # 45 batch-36 + 4 batch-3 (raws NOT yet published)
B_UNKNOWN_AFTER = 9
B_UNKNOWN_AFTER_S5 = [38215, 197253, 259023, 300778,   # batch-3 unconsumed
                      528689, 543795, 605961, 620742, 625899]  # batch-36 WINs unconsumed
B_ADOPTED_OWN = 40
B_ADOPTED_OWN_S5 = [356378, 393798, 441775, 565995, 570139, 574236, 578232,
                    582153, 585861, 589727, 593275, 596738, 602640, 605690,
                    608779, 611801, 614833, 617672, 623364, 625189, 630432,
                    636913, 641189, 643424, 645317, 650304, 651925, 653505,
                    655969, 657407, 662182, 664455, 669726, 671112, 671120,
                    671129, 671133, 671137, 671143, 671146]
NEWLY_RESOLVED_UPD8_S5 = [356378, 393798, 441775, 498207, 544907, 565995,
                          570139, 574236, 578232, 582153, 585861, 589727,
                          593275, 596738, 602640, 605690, 608779, 611801,
                          614833, 617672, 623364, 625189, 630432, 636913,
                          641189, 643424, 645317, 650304, 651925, 653505,
                          655969, 657407, 662182, 664455, 669726, 671112,
                          671120, 671129, 671133, 671137, 671143, 671146]
STATUS_BEFORE = {"excluded": 390, "excluded_now": 23, "free_now": 39, "unknown": 34497}
STATUS_AFTER = {"excluded": 390, "excluded_now": 23, "free_now": 39, "unknown": 34497}
UPD8_RESOLVED_BEFORE = 214
UPD8_RESOLVED_AFTER = 256
UPD8_REMAINING_BEFORE = 31645
UPD8_REMAINING_AFTER = 31603
JOINT_GREEDY_BEFORE = 36943
JOINT_GREEDY_AFTER = 36511
WORKLIST_BEFORE = 64535
WORKLIST_AFTER = 64420
KNOWN_UNIVERSE_BEFORE = 752
KNOWN_UNIVERSE_AFTER = 839
CACHE_IN_UNIVERSE_BEFORE = 729
CACHE_IN_UNIVERSE_AFTER = 816
CACHE_VERDICTS_BEFORE = {"1": 158, "2": 6415}
CACHE_VERDICTS_AFTER = {"1": 158, "2": 6502}
UNIQUE_GROUPS_BEFORE = 2115
UNIQUE_GROUPS_AFTER = 2115
PER_ROOT_REMAINING_DELTA = {"1": -4, "12": -80, "26": -4, "37": -80}
PER_ROOT_COVERAGE_DELTA = {
    "0": {"free": [7, 7], "uncovered": [112, 112], "greedy": [3008, 3006]},
    "12": {"free": [6, 6], "uncovered": [113, 113], "greedy": [2984, 2896]},
    "14": {"free": [8, 8], "uncovered": [111, 111], "greedy": [4540, 4538]},
    "24": {"free": [12, 12], "uncovered": [107, 107], "greedy": [2829, 2827]},
    "26": {"free": [8, 8], "uncovered": [111, 111], "greedy": [5122, 5230]},
    "36": {"free": [4, 4], "uncovered": [115, 115], "greedy": [2954, 2997]},
    "37": {"free": [4, 4], "uncovered": [115, 115], "greedy": [3756, 3622]},
    "48": {"free": [7, 7], "uncovered": [112, 112], "greedy": [2942, 2895]},
}
CLOSURE_ROWS_BEFORE = 807
CLOSURE_ROWS_AFTER = 807
# fixed-size frontier selection churn: 4 rows leave, 4 rows enter, NONE freed
LEFT_CLASSES = [1530, 6241, 15393, 23410]
ENTERED_CLASSES = [16367, 18047, 21857, 23034]
LEFT_ROWS = {
    1530: {"class_rank": "615", "class_lo": "1152956689180262400", "class_hi": "0",
           "unknown_now": "102", "first_group_first": "15", "first_group_third": "46",
           "groups_served_count": "2"},
    6241: {"class_rank": "720", "class_lo": "1731634056723956224", "class_hi": "0",
           "unknown_now": "106", "first_group_first": "1", "first_group_third": "47",
           "groups_served_count": "2"},
    15393: {"class_rank": "610", "class_lo": "1153202979650666752", "class_hi": "0",
            "unknown_now": "102", "first_group_first": "2", "first_group_third": "28",
            "groups_served_count": "2"},
    23410: {"class_rank": "612", "class_lo": "1152922638746648576", "class_hi": "0",
            "unknown_now": "102", "first_group_first": "25", "first_group_third": "68",
            "groups_served_count": "2"},
}
ENTERED_ROWS = {
    16367: {"class_rank": "579", "class_lo": "1154082588952887296", "class_hi": "0",
            "unknown_now": "101", "first_group_first": "15", "first_group_third": "46",
            "groups_served_count": "2"},
    18047: {"class_rank": "724", "class_lo": "1153062242096250882", "class_hi": "0",
            "unknown_now": "106", "first_group_first": "1", "first_group_third": "47",
            "groups_served_count": "2"},
    21857: {"class_rank": "577", "class_lo": "1152921504875282436", "class_hi": "16",
            "unknown_now": "101", "first_group_first": "2", "first_group_third": "28",
            "groups_served_count": "2"},
    23034: {"class_rank": "578", "class_lo": "1152921504908836864", "class_hi": "16",
            "unknown_now": "101", "first_group_first": "25", "first_group_third": "68",
            "groups_served_count": "2"},
}
CLASS_A_ROW_BEFORE = {"class_rank": "10", "unknown_now": "49", "groups_served_count": "3"}
CLASS_A_ROW_AFTER = {"class_rank": "4", "unknown_now": "2", "groups_served_count": "3"}
CLASS_B_ROW_BEFORE = {"class_rank": "9", "unknown_now": "49", "groups_served_count": "4"}
CLASS_B_ROW_AFTER = {"class_rank": "8", "unknown_now": "9", "groups_served_count": "4"}
GS_CHURN_DECREASE = []
CHANGED_CLASS_SET = [
    {"class_index": 19299, "unknown_before": 59, "unknown_after": 58, "own_adopted": 1},
    {"class_index": 19749, "unknown_before": 54, "unknown_after": 53, "own_adopted": 1},
    {"class_index": 19774, "unknown_before": 95, "unknown_after": 94, "own_adopted": 1},
    {"class_index": 20175, "unknown_before": 99, "unknown_after": 98, "own_adopted": 1},
    {"class_index": 20417, "unknown_before": 59, "unknown_after": 58, "own_adopted": 1},
    {"class_index": 20418, "unknown_before": 60, "unknown_after": 59, "own_adopted": 1},
    {"class_index": 20423, "unknown_before": 59, "unknown_after": 58, "own_adopted": 1},
    {"class_index": 20810, "unknown_before": 106, "unknown_after": 105, "own_adopted": 1},
    {"class_index": 21050, "unknown_before": 106, "unknown_after": 105, "own_adopted": 1},
    {"class_index": 21069, "unknown_before": 106, "unknown_after": 105, "own_adopted": 1},
    {"class_index": 21071, "unknown_before": 106, "unknown_after": 105, "own_adopted": 1},
    {"class_index": 21387, "unknown_before": 107, "unknown_after": 106, "own_adopted": 1},
    {"class_index": 21934, "unknown_before": 107, "unknown_after": 106, "own_adopted": 1},
    {"class_index": 22095, "unknown_before": 107, "unknown_after": 106, "own_adopted": 1},
    {"class_index": 22239, "unknown_before": 103, "unknown_after": 102, "own_adopted": 1},
    {"class_index": 22637, "unknown_before": 56, "unknown_after": 55, "own_adopted": 1},
    {"class_index": 23283, "unknown_before": 107, "unknown_after": 106, "own_adopted": 1},
    {"class_index": 23337, "unknown_before": 101, "unknown_after": 100, "own_adopted": 1},
    {"class_index": 23482, "unknown_before": 54, "unknown_after": 53, "own_adopted": 1},
    {"class_index": 23777, "unknown_before": 94, "unknown_after": 93, "own_adopted": 1},
    {"class_index": 23960, "unknown_before": 56, "unknown_after": 55, "own_adopted": 1},
    {"class_index": 23962, "unknown_before": 103, "unknown_after": 102, "own_adopted": 1},
    {"class_index": 23964, "unknown_before": 53, "unknown_after": 52, "own_adopted": 1},
    {"class_index": 23965, "unknown_before": 107, "unknown_after": 106, "own_adopted": 1},
    {"class_index": 23966, "unknown_before": 57, "unknown_after": 56, "own_adopted": 1},
]
RANK_CHURN_ROWS = 348
STABLE_ROWS = 428
NODES_B4 = 882800
NODES_B36 = 159499387
NODES_B37 = 96295019
ALL_B36_TOTAL_NODES = 183921575   # all 45 probed rows (40 adopted + 5 WIN unconsumed)
ALL_B37_TOTAL_NODES = 99204059   # all 47 probed rows (46 adopted + 1 WIN unconsumed)


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
    """MANIFEST sha-verify file-by-file; accepts both the 2-column
    'sha256 path' form (batch-37) and the 4-column
    'sha256 git-blob-sha1 size path' form (batch-36); paths repo-relative
    or kit-relative."""
    if sha(dirp / "MANIFEST-sha256.txt") != manifest_sha:
        fail(f"kit {dirp.name} MANIFEST sha drift")
    n = 0
    for line in (dirp / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split()
        want, rel = parts[0], parts[-1]
        p = next((c for c in _kit_candidates(dirp, rel) if c.is_file()), None)
        if p is None:
            fail(f"kit {dirp.name} file missing: {rel}")
        if sha(p) != want:
            fail(f"kit {dirp.name} sha drift at {rel}")
        n += 1
    if n != files_expected:
        fail(f"kit {dirp.name} files {n} != {files_expected}")
    return n


def _json_keys(p: Path, want_sha: str):
    if sha(p) != want_sha:
        fail(f"batch-keys sha drift: {p}")
    return {(int(e["lo"]), int(e["hi"])) for e in json.loads(p.read_text())["keys"]}


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
        ("increment b4", INCR_B4, INCR_B4_SHA),
        ("increment b36", INCR_B36, INCR_B36_SHA),
        ("increment b37", INCR_B37, INCR_B37_SHA),
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
        ("merger", EXP / "scripts/s5_union_merge.py", MERGER_SHA),
        ("merge-audit run1", EXP / "output/merge-audit-run1.json", MERGE_AUDIT_SHA),
        ("merge-audit run2", EXP / "output/merge-audit-run2.json", MERGE_AUDIT_SHA),
        ("merge-audit run3", EXP / "output/merge-audit-run3.json", MERGE_AUDIT_SHA),
    ]
    for name, p, want in pins:
        got = sha(p)
        if got != want:
            fail(f"{name} sha drift: {got} != {want}")
    k36 = verify_kit(KIT_B36, KIT_B36_MANIFEST_SHA, KIT_B36_FILES)
    k37 = verify_kit(KIT_B37, KIT_B37_MANIFEST_SHA, KIT_B37_FILES)
    # batch-4 kit: declaration-only (no MANIFEST), pinned file-by-file
    b4_pins = [
        (KIT_B4 / "output/status.log", KIT_B4_STATUS_SHA),
        (KIT_B4 / "input/batch-keys.json", KIT_B4_KEYS_SHA),
        (KIT_B4 / "output/raw/e001.p1.out", KIT_B4_E001_P1_SHA),
        (KIT_B4 / "output/raw/e001.p2.out", KIT_B4_E001_P2_SHA),
        (KIT_B4 / "output/raw/e002.p1.out", KIT_B4_E002_P1_SHA),
        (KIT_B4 / "output/raw/e002.p2.out", KIT_B4_E002_P2_SHA),
        (KIT_B4 / "scripts/runbatch.sh", KIT_B4_RUNBATCH_SHA),
        (KIT_B4 / "scripts/jsreplay.js", JSREPLAY_SHA),
    ]
    for p, want in b4_pins:
        if sha(p) != want:
            fail(f"batch-4 kit file sha drift: {p.name}")
    keys36 = _json_keys(KIT_B36 / "input/batch-keys-b36.json", KIT_B36_KEYS_SHA)
    keys37 = _json_keys(KIT_B37 / "input/batch-keys-b37.json", KIT_B37_KEYS_SHA)
    keys4 = _json_keys(KIT_B4 / "input/batch-keys.json", KIT_B4_KEYS_SHA)

    # --- manifest gates ----------------------------------------------------
    manifest = json.loads(MANIFEST.read_text())
    if manifest["schema"] != "dz-adoption-increments-manifest-v1":
        fail("manifest schema drift")
    batches = {b["batch"]: b for b in manifest["batches"]}
    if sorted(batches) != ["batch-36", "batch-37", "batch-4"] or len(manifest["batches"]) != 3:
        fail("manifest batch set drift")
    if sorted(manifest["loss_ids"]) != sorted(
            batches["batch-4"]["adopted_loss_ids"]
            + batches["batch-36"]["adopted_loss_ids"]
            + batches["batch-37"]["adopted_loss_ids"]):
        fail("manifest loss_ids != union of per-batch adopted ids")
    if len(manifest["loss_ids"]) != ADOPTED_ROWS \
            or len(batches["batch-4"]["adopted_loss_ids"]) != ADOPTED_ROWS_B4 \
            or len(batches["batch-36"]["adopted_loss_ids"]) != ADOPTED_ROWS_B36 \
            or len(batches["batch-37"]["adopted_loss_ids"]) != ADOPTED_ROWS_B37:
        fail(f"manifest adopted id counts drift (1/40/46 of {ADOPTED_ROWS})")
    if sorted(manifest["unadopted_win_ids"]) != UNCONSUMED_WIN_IDS:
        fail("manifest unconsumed WIN id set drift")
    if manifest["exhausted_excluded_ids"] != [] or manifest["exhausted_rows"] != []:
        fail("an EXHAUSTED row must not be present in this Part")
    if sorted(manifest["resolved_ids"]) != sorted(manifest["loss_ids"]):
        fail("manifest resolved_ids != loss_ids")
    if manifest["full_packet_eq_loss_only"] is not False:
        fail("the three packets together are MIXED: full_packet_eq_loss_only must be false")
    if manifest["win_scenario_exists"] is not True:
        fail("manifest win_scenario_exists must be true (7 probe-level WIN rows)")
    if manifest["base_cache_sha256"] != BASE_CACHE_SHA:
        fail("manifest base cache pin drift")
    if manifest["merger_sha256"] != MERGER_SHA:
        fail("manifest merger pin drift")
    if manifest["row_counts"] != {"probed_rows": 94, "adopted_loss_rows": 87,
                                  "prior_adopted_loss_rows": 0, "wins": 7,
                                  "exhausted_excluded": 0, "fragments_unprobed": 0,
                                  "fileless_unprobed": 0}:
        fail("manifest row_counts drift")
    if manifest["quarantine_hits"] != 0 or manifest["base_cache_absent_hits_for_emitted"] != 0:
        fail("manifest quarantine / absent-hit gates drifted (must both be 0)")
    if manifest["sha256"] != {"loss_b4loss1": INCR_B4_SHA, "loss_b36loss40": INCR_B36_SHA,
                              "loss_b37loss46": INCR_B37_SHA}:
        fail("manifest increment sha pins drift")
    for name, cls, keys_total, nodes, lines, halts in (
            ("batch-4", CLASS_A, 2, NODES_B4, 3, 1),
            ("batch-36", CLASS_B, 45, NODES_B36, 50, 5),
            ("batch-37", CLASS_A, 47, NODES_B37, 48, 1)):
        b = batches[name]
        if b["class_index"] != cls or b["keys_total"] != keys_total:
            fail(f"manifest {name} identity drift")
        if b["total_nodes_pass_one"] != nodes or b["total_nodes_pass_two"] != nodes:
            fail(f"manifest {name} node totals drift")
        if b["status_log_lines"] != lines:
            fail(f"manifest {name} status-log line count drift")
    halts4 = batches["batch-4"]["status_log_win_halt_lines"]
    if not isinstance(halts4, list) or len(halts4) != 1 or halts4[0] != "2026-11-22T03:26:03Z e002 WIN-HALT":
        fail("manifest batch-4 WIN-HALT line drift (must pin the exact e002 halt line)")
    halts36 = batches["batch-36"]["status_log_win_halt_lines"]
    if halts36 != ["2026-11-24T23:42:13Z d008 WIN-HALT", "2026-11-24T23:43:06Z d009 WIN-HALT",
                   "2026-11-24T23:53:24Z d021 WIN-HALT", "2026-11-24T23:57:59Z d026 WIN-HALT",
                   "2026-11-24T23:59:30Z d029 WIN-HALT"]:
        fail("manifest batch-36 WIN-HALT lines drift (must pin the exact 5 halt lines)")
    halts37 = batches["batch-37"]["status_log_win_halt_lines"]
    if halts37 != ["2026-11-25T00:24:44Z e042 WIN-HALT"]:
        fail("manifest batch-37 WIN-HALT line drift (must pin the exact e042 halt line)")
        if b["val_gate_multi_host_node_exact"] is not True:
            fail(f"manifest {name} val-gate multi-host node-exact flag must be true")
        if b["already_adopted_ids"] not in ([], ["e022"]):
            fail(f"manifest {name} already-adopted id set drift")
    if batches["batch-37"]["already_adopted_ids"] != ["e022"]:
        fail("batch-37 must exclude exactly the already-canonical e022")
    if len(batches["batch-4"]["probed_ids"]) != 2 or len(batches["batch-36"]["probed_ids"]) != 45 \
            or len(batches["batch-37"]["probed_ids"]) != 47:
        fail("manifest probed_ids counts drift (2/45/47)")
    adopted_ids = manifest["loss_ids"]
    win_ids = manifest["unadopted_win_ids"]
    exh_ids = manifest["exhausted_excluded_ids"]

    # --- refresh re-execution (double-run determinism) ---------------------
    base_tmp = rerun_refresh(BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA, ".dzverify-base-b35loss26")
    scen_tmp = rerun_refresh(SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA, ".dzverify-scen-dz")
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
    shutil.rmtree(ROOT / "research/experiments/.dzverify-base-b35loss26")
    shutil.rmtree(ROOT / "research/experiments/.dzverify-scen-dz")

    # --- cache relation: SCEN == BASE + exactly the 87 increment rows ------
    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    incr = {}
    for path, want_sha, want_rows in ((INCR_B4, INCR_B4_SHA, ADOPTED_ROWS_B4),
                                      (INCR_B36, INCR_B36_SHA, ADOPTED_ROWS_B36),
                                      (INCR_B37, INCR_B37_SHA, ADOPTED_ROWS_B37)):
        if sha(path) != want_sha:
            fail(f"increment sha drift at re-read: {path.name}")
        part = load_cache(path)
        if len(part) != want_rows:
            fail(f"increment {path.name} rows {len(part)} != {want_rows}")
        for key, row in part.items():
            if key in incr:
                fail(f"increment key collision across the three packets: {key}")
            incr[key] = row
    if len(base) != 6573 or len(scen) != 6660 or len(incr) != ADOPTED_ROWS:
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
    if (wins, losses) != (158, 6502):
        fail(f"scenario verdict counts {wins}/{losses} != 158/6,502")
    if base.items() > scen.items():
        fail("a BASE row is missing from the scenario cache (no row may change)")

    # --- Board arithmetic for classes 16371 and 20421 ---------------------
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
    update8 = json.loads(UPDATE8.read_text())
    receipt_verdicts = {int(k): int(v) for k, v in update8["resolved_s5_verdicts"].items()}
    board = Board(11)

    def children_keys(cls):
        lo, hi = s4_masks[cls]
        return {(c & ((1 << 64) - 1), c >> 64) for c in board.children(lo | (hi << 64))}

    # class 16371 (batch-4 + batch-37 packets)
    child_a = children_keys(CLASS_A)
    if len(child_a) != A_CHILDREN:
        fail(f"class-16371 Board child boundary {len(child_a)} != {A_CHILDREN}")
    inbase_a = {k for k in child_a if k in base}
    if sorted(mask_to_index[k] for k in inbase_a) != A_BASE_CACHE_S5:
        fail("the base-known lossless children of 16371 != the pinned e022 set")
    if any(base[k][0] != 2 for k in inbase_a):
        fail("a base-known child of 16371 is not an exact LOSS in BASE")
    rec_a = {k for k in child_a if mask_to_index.get(k) in receipt_verdicts}
    if sorted(mask_to_index[k] for k in rec_a) != A_RECEIPT_LOSS_S5:
        fail("the update8-receipt children of 16371 != the pinned receipt set")
    for k in rec_a:
        if receipt_verdicts[mask_to_index[k]] != 2:
            fail("an update8-receipt child of 16371 is not LOSS")
        if k in base or k in scen:
            fail("a receipt child of 16371 is also a cache row")
    b37_in = child_a & keys37
    b4_in = child_a & keys4
    if len(b37_in) != A_B37_KEYS_IN_BOUNDARY or len(keys37) != A_B37_KEYS_IN_BOUNDARY:
        fail("batch-37 keys not exactly the 47 in-boundary children of 16371")
    if len(b4_in) != A_B4_KEYS_IN_BOUNDARY:
        fail("the whole batch-4 50-key packet must lie inside the class-16371 child boundary")
    if keys37 >= keys4:
        fail("batch-37 keys must be a subset of the 50-key batch-4 packet (dual-class packet reuse)")
    unk_b_a = child_a - inbase_a - rec_a
    unk_s_a = child_a - {k for k in child_a if k in scen} - rec_a
    if len(unk_b_a) != A_UNKNOWN_BEFORE:
        fail(f"class-16371 BASE unknown children {len(unk_b_a)} != {A_UNKNOWN_BEFORE}")
    if len(unk_s_a) != A_UNKNOWN_AFTER:
        fail(f"class-16371 scenario unknown children {len(unk_s_a)} != {A_UNKNOWN_AFTER} (NOT freed)")
    if sorted(mask_to_index[k] for k in unk_s_a) != A_UNKNOWN_AFTER_S5:
        fail("class-16371 scenario unknown children != the pinned unconsumed WIN pair {e002, e042}")
    if E001_KEY not in unk_b_a or E002_KEY not in unk_b_a:
        fail("pinned e001/e002 packet keys missing from the class-16371 boundary")
    if mask_to_index[E001_KEY] != E001_S5 or mask_to_index[E002_KEY] != E002_S5:
        fail("pinned e001/e002 s5 indices drift")
    adopted_a = unk_b_a - unk_s_a
    if len(adopted_a) != A_ADOPTED_OWN:
        fail(f"class-16371 adopted children {len(adopted_a)} != {A_ADOPTED_OWN}")
    if sorted(mask_to_index[k] for k in adopted_a) != A_ADOPTED_OWN_S5:
        fail("class-16371 adopted s5 set != the pinned adopted list")
    for k in adopted_a:
        if scen[k][0] != 2:
            fail("an adopted child of 16371 is not an exact LOSS in the scenario")
    if any(k in quarantined for k in child_a):
        fail("a quarantined key sits inside the class-16371 child boundary")

    # class 20421 (batch-36 packet + 4 unpublished batch-3 rows)
    child_b = children_keys(CLASS_B)
    if len(child_b) != B_CHILDREN:
        fail(f"class-20421 Board child boundary {len(child_b)} != {B_CHILDREN}")
    if B_OUTSIDE_KEY not in child_b or B_OUTSIDE_KEY not in base or base[B_OUTSIDE_KEY][0] != 2:
        fail("the pinned out-of-universe base LOSS child of 20421 drift")
    inbase_b = {k for k in child_b if k in base}
    rec_b = {k for k in child_b if mask_to_index.get(k) in receipt_verdicts}
    if rec_b:
        fail("class-20421 must have no update8-receipt children")
    b36_in = child_b & keys36
    if len(b36_in) != B_B36_KEYS_IN_BOUNDARY or len(keys36) != B_B36_KEYS_IN_BOUNDARY:
        fail("batch-36 keys not exactly the 45 in-boundary children of 20421")
    unk_b_bb = child_b - inbase_b - rec_b
    unk_s_b = child_b - {k for k in child_b if k in scen} - rec_b
    if len(unk_b_bb) != B_UNKNOWN_BEFORE:
        fail(f"class-20421 BASE unknown children {len(unk_b_bb)} != {B_UNKNOWN_BEFORE} (45 batch-36 + 4 batch-3)")
    if len(unk_s_b) != B_UNKNOWN_AFTER:
        fail(f"class-20421 scenario unknown children {len(unk_s_b)} != {B_UNKNOWN_AFTER} (NOT freed)")
    if sorted(mask_to_index[k] for k in unk_s_b) != B_UNKNOWN_AFTER_S5:
        fail("class-20421 scenario unknown children != batch-3 four + batch-36 five WINs")
    adopted_b = unk_b_bb - unk_s_b
    if len(adopted_b) != B_ADOPTED_OWN:
        fail(f"class-20421 adopted children {len(adopted_b)} != {B_ADOPTED_OWN}")
    if sorted(mask_to_index[k] for k in adopted_b) != B_ADOPTED_OWN_S5:
        fail("class-20421 adopted s5 set != the pinned adopted list")
    for k in adopted_b:
        if scen[k][0] != 2:
            fail("an adopted child of 20421 is not an exact LOSS in the scenario")
    if any(k in quarantined for k in child_b):
        fail("a quarantined key sits inside the class-20421 child boundary")

    adopted_all = {k for k in scen if k not in base}
    if adopted_all != incr.keys() or adopted_all != (adopted_a | adopted_b):
        fail("the 87 adopted keys != union of the two macro boundaries' own adopted children")
    if adopted_a & adopted_b:
        fail("the two macro boundaries' adopted sets overlap (count arithmetic would drift)")

    # --- update8 refresh deltas ---------------------------------------------
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
        fail(f"newly resolved update8 set != the pinned 42-entry adopted-in-requirement set: {newly}")
    if lost:
        fail(f"update8 resolution LOST rows: {sorted(lost)}")
    adopted_idx = {mask_to_index[k] for k in incr}
    if not set(newly) <= adopted_idx:
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
    if scen_summary["inputs"]["cache_rows"] != 6660 or scen_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_AFTER \
            or scen_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_AFTER:
        fail("scenario inputs metrics drift")
    if base_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["cache_rows"] != 6573:
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
        fail(f"closure table row counts {len(cb_t)}/{len(cs_t)} != 807/807")
    left = sorted(set(cb_t) - set(cs_t))
    entered = sorted(set(cs_t) - set(cb_t))
    if left != LEFT_CLASSES or entered != ENTERED_CLASSES:
        fail(f"closure table churn sets drift: left={left} entered={entered}")
    churn_detail = {"left": [], "entered": []}
    for ci in left:
        want = dict(LEFT_ROWS[ci])
        want["class_index"] = str(ci)
        if cb_t[ci] != want:
            fail(f"left class {ci} base row drift vs pin: {cb_t[ci]}")
        kids = children_keys(ci)
        rec = {k for k in kids if mask_to_index.get(k) in receipt_verdicts}
        unk_b = len([k for k in kids if k not in base and k not in rec])
        unk_s = len([k for k in kids if k not in scen and k not in rec])
        own = len(kids & adopted_all)
        if own != 0 or unk_b != int(want["unknown_now"]) or unk_s != unk_b:
            fail(f"left class {ci}: pure displacement churn expected (own 0, unknown static); "
                 f"own={own} unk_b={unk_b} unk_s={unk_s}")
        churn_detail["left"].append({"class_index": ci, "unknown_now": int(want["unknown_now"]),
                                     "class_rank": int(want["class_rank"]), "own_adopted": 0})
    for ci in entered:
        want = dict(ENTERED_ROWS[ci])
        want["class_index"] = str(ci)
        if cs_t[ci] != want:
            fail(f"entered class {ci} scenario row drift vs pin: {cs_t[ci]}")
        kids = children_keys(ci)
        rec = {k for k in kids if mask_to_index.get(k) in receipt_verdicts}
        unk_b = len([k for k in kids if k not in base and k not in rec])
        unk_s = len([k for k in kids if k not in scen and k not in rec])
        own = len(kids & adopted_all)
        if own != 1 or unk_s != int(want["unknown_now"]) or unk_b - unk_s != own:
            fail(f"entered class {ci}: own-1 re-rank churn expected; own={own} "
                 f"unk_b={unk_b} unk_s={unk_s}")
        churn_detail["entered"].append({"class_index": ci, "unknown_now": int(want["unknown_now"]),
                                        "class_rank": int(want["class_rank"]),
                                        "own_adopted": own, "unknown_before": unk_b})
    for ci, row, rowb, rowa in ((CLASS_A, cb_t, CLASS_A_ROW_BEFORE, CLASS_A_ROW_AFTER),
                               (CLASS_B, cb_t, CLASS_B_ROW_BEFORE, CLASS_B_ROW_AFTER)):
        if ci not in cb_t or ci not in cs_t:
            fail(f"class {ci} must remain in BOTH closure tables (not freed, not excluded)")
        for col, want in rowb.items():
            if row[ci][col] != want:
                fail(f"base class-{ci} row {col} drift: {row[ci][col]} != {want}")
        for col, want in rowa.items():
            if cs_t[ci][col] != want:
                fail(f"scenario class-{ci} row {col} drift: {cs_t[ci][col]} != {want}")
    own_a = len(child_a & adopted_all)
    own_b = len(child_b & adopted_all)
    if int(cb_t[CLASS_A]["unknown_now"]) - int(cs_t[CLASS_A]["unknown_now"]) != own_a or own_a != A_ADOPTED_OWN:
        fail("class-16371 unknown delta != its own adopted children (Board boundary)")
    if int(cb_t[CLASS_B]["unknown_now"]) - int(cs_t[CLASS_B]["unknown_now"]) != own_b or own_b != B_ADOPTED_OWN:
        fail("class-20421 unknown delta != its own adopted children (Board boundary)")
    changed, rank_churn, stable, gs_dec, gs_bad = [], 0, 0, [], []
    for ci, brow in sorted(cb_t.items()):
        if ci in LEFT_CLASSES:
            continue
        if ci in (CLASS_A, CLASS_B):
            continue
        if ci not in cs_t:
            fail(f"class {ci} vanished from the closure table without being pinned in LEFT")
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
        kids_keys = children_keys(ci)
        own = len(kids_keys & adopted_all)
        if (b_unk - s_unk) != own or own == 0:
            fail(f"class {ci} unknown delta {b_unk}->{s_unk} != own adopted membership {own}")
        changed.append({"class_index": ci, "unknown_before": b_unk, "unknown_after": s_unk,
                        "own_adopted": own})
    if changed != CHANGED_CLASS_SET:
        fail(f"changed-class set != the pinned 25-micro-class set: {changed}")
    if rank_churn != RANK_CHURN_ROWS:
        fail(f"rank-churn-only row count {rank_churn} != {RANK_CHURN_ROWS}")
    if stable != STABLE_ROWS:
        fail(f"fully-stable row count {stable} != {STABLE_ROWS}")
    for e in gs_dec:
        if e["unknown_now"][0] != e["unknown_now"][1]:
            fail(f"groups_served_churn class {e['class_index']} changed unknown_now: {e}")
    if gs_dec != GS_CHURN_DECREASE:
        fail(f"groups_served_count churn set != the pinned empty churn: {gs_dec}")
    scen_first = {e["class_index"]: e for e in scen_summary["closure_classes_first"]}
    fa = scen_first.get(CLASS_A)
    if fa is None or fa["unknown_now"] != 2 or len(fa["groups_served"]) != 3:
        fail("scenario closure_classes_first entry for class 16371 drift (2 unknown / 3 groups)")
    fb = scen_first.get(CLASS_B)
    if fb is None or fb["unknown_now"] != 9 or len(fb["groups_served"]) != 4:
        fail("scenario closure_classes_first entry for class 20421 drift (9 unknown / 4 groups)")

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
        "schema": "dz-adoption-decomp-deltas-v1",
        "scenario": "ADOPTED-CANONICAL",
        "batches": {
            "batch-4": {"class_index": CLASS_A, "probed_rows": 2,
                        "adopted_loss_rows": ADOPTED_ROWS_B4,
                        "adopted_total_nodes_per_pass": NODES_B4,
                        "decisive_labels": "1 LOSS @15M adopted (e001) + 1 probe-level WIN @15M "
                                           "unconsumed (e002, WIN-HALT stop rule)"},
            "batch-36": {"class_index": CLASS_B, "probed_rows": 45,
                         "adopted_loss_rows": ADOPTED_ROWS_B36,
                         "adopted_total_nodes_per_pass": NODES_B36,
                         "all45_total_nodes": ALL_B36_TOTAL_NODES,
                         "decisive_labels": "40 LOSS @15M adopted + 5 probe-level WIN unconsumed "
                                            "(honest two-pass labels, Part DV probe-drive family raws)"},
            "batch-37": {"class_index": CLASS_A, "probed_rows": 47,
                         "adopted_loss_rows": ADOPTED_ROWS_B37,
                         "adopted_total_nodes_per_pass": NODES_B37,
                         "all47_total_nodes": ALL_B37_TOTAL_NODES,
                         "decisive_labels": "46 LOSS @15M adopted + 1 probe-level WIN unconsumed "
                                            "(e042); the already-canonical dual-class child e022 "
                                            "(s5 546606) excluded at selection"},
            "adopted_loss_ids": adopted_ids,
            "unadopted_win_ids": win_ids,
            "exhausted_excluded_ids": exh_ids,
        },
        "cache": {"base_sha256": BASE_CACHE_SHA, "scenario_sha256": SCEN_CACHE_SHA,
                  "base_rows": len(base), "scenario_rows": len(scen),
                  "increment_rows": {"b4loss1": ADOPTED_ROWS_B4, "b36loss40": ADOPTED_ROWS_B36,
                                     "b37loss46": ADOPTED_ROWS_B37, "total": ADOPTED_ROWS},
                  "verdict_counts": {"WIN": 158, "LOSS": 6502},
                  "relation": "scenario == base rows + the 87 increment rows verbatim "
                              "(no other row changed)",
                  "merge_audit_runs": 3, "merge_audit_sha256_each": MERGE_AUDIT_SHA,
                  "merger": "pinned s5_union_merge.py fail-closed union merger (pinned merger "
                            "exclusivity: no other tool may emit canonical rows)"},
        "class_16371": {"children_total": A_CHILDREN,
                        "unknown_before": A_UNKNOWN_BEFORE, "unknown_after": A_UNKNOWN_AFTER,
                        "adopted_own": A_ADOPTED_OWN,
                        "unconsumed_win_children": A_UNKNOWN_AFTER,
                        "base_known_loss_s5_cache": A_BASE_CACHE_S5,
                        "receipt_known_loss_s5": A_RECEIPT_LOSS_S5,
                        "unknown_after_s5": A_UNKNOWN_AFTER_S5,
                        "class_rank": [10, 4], "groups_served_count": [3, 3],
                        "status_before": "unknown",
                        "status_after": "unknown (NOT freed, NOT excluded: 2 unconsumed WIN "
                                        "children remain (e002, e042); Board-verified by the "
                                        "reaudit refresh free_now 39 -> 39, board_verified "
                                        "39/39, unknown 34,497 static)",
                        "not_a_root_verdict": "the loss-only adoption of mixed packets frees "
                                              "nothing; no root verdict and no coverage claim is "
                                              "made"},
        "class_20421": {"children_total": B_CHILDREN,
                        "unknown_before": B_UNKNOWN_BEFORE, "unknown_after": B_UNKNOWN_AFTER,
                        "adopted_own": B_ADOPTED_OWN,
                        "unconsumed_children": B_UNKNOWN_AFTER,
                        "base_out_of_universe_child": list(B_OUTSIDE_KEY),
                        "unknown_after_s5": B_UNKNOWN_AFTER_S5,
                        "class_rank": [9, 8], "groups_served_count": [4, 4],
                        "status_before": "unknown",
                        "status_after": "unknown (NOT freed, NOT excluded: 9 unknown children "
                                        "remain = 5 batch-36 WINs unconsumed + 4 batch-3 "
                                        "honest-labeled rows whose raws are NOT yet published); "
                                        "Board-verified by the reaudit refresh",
                        "not_a_root_verdict": "no root verdict and no coverage claim is made"},
        "closure_table": {"rows_before": CLOSURE_ROWS_BEFORE, "rows_after": CLOSURE_ROWS_AFTER,
                          "left": churn_detail["left"], "entered": churn_detail["entered"],
                          "churn_reason": "fixed-size frontier selection: re-selection "
                                          "bookkeeping after the two macro frontier costs collapse "
                                          "(16371 rank 10 -> 4, 20421 rank 9 -> 8); the 4 left "
                                          "rows own ZERO adopted children (pure displacement of "
                                          "the fixed-807 tail); each of the 4 entered rows owns "
                                          "exactly ONE adopted child (frontier cost improved); "
                                          "Board-verified own-membership on all 8 rows; free_now "
                                          "stays 39 static (nothing was freed)",
                          "unknown_changed_classes": changed,
                          "macro_classes": [CLASS_A, CLASS_B],
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
                    "note": "greedy/worklist deltas are frozen-scheduler bookkeeping after the two "
                            "macro frontier costs collapse: the joint greedy union DECREASES "
                            "(36,943 -> 36,511) and the worklist shrinks (64,535 -> 64,420); "
                            "per-root free/uncovered thirds are IDENTICAL at every root (nothing "
                            "was freed); the root-26 (5,122 -> 5,230) and root-36 (2,954 -> 2,997) "
                            "individual greedy unions INCREASE as pure re-selection bookkeeping; "
                            "per-root remaining decreases only at roots 1 (-4), 12 (-80), 26 (-4) "
                            "and 37 (-80); root 27 stays 119/119"},
        "verification": {"kit_files_verified": {"batch-36": k36, "batch-37": k37},
                         "batch4_kit_pinned_files": len(b4_pins),
                         "refresh_scripts_reexecuted": [BASE_REFRESH_SHA, SCEN_REFRESH_SHA],
                         "refresh_outputs_byte_identical": True,
                         "scenario_probe_worklist_unpublished_regen_sha256": SCEN_WORKLIST_SHA,
                         "board_child_regeneration": "class-16371 canonical 52-child and class-20421 "
                                                     "canonical 50-child 5-stone boundaries "
                                                     "regenerated via Board(11).children"},
        "interpretation_guard":
            "only the 87 fresh LOSS rows (batch-4 e001 + batch-36 40 + batch-37 46) are consumed "
            "into the canonical cache by this Part via the pinned fail-closed union merger; the "
            "seven probe-level WIN rows (batch-36 d008/d009/d021/d026/d029, batch-37 e042, "
            "batch-4 e002) are consumed NOWHERE and belong to the scrutiny-owner C++ "
            "second-implementation gate (pin 9193f5b6...); the batch-3 honest-labeled rows "
            "{d001, d002 WIN, d003, d004} stay unconsumed outside this Part because their raws "
            "are not yet published; classes 16371 and 20421 are NOT freed and NOT excluded (class "
            "status stays unknown, free_now 39 static, closure table 807 rows static); the 8 "
            "left/entered closure rows are frontier selection bookkeeping, no freedom claim; no "
            "root verdict and no coverage claim is made anywhere; the per-root/greedy/worklist "
            "quantities quoted here are bookkeeping, never verdicts; no update8 resolution was "
            "lost; 11x11 stays UNKNOWN",
    }
    (EXP / "output/decomp-deltas-dz-adoption.json").write_text(
        json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("DECOMP OK changed=%d rank_churn=%d gs_dec=%d stable=%d left=%d entered=%d" %
          (len(changed), rank_churn, len(gs_dec), stable, len(left), len(entered)))
    print("class16371: unknown 49 -> 2 (47 adopted, {e002, e042} WINs stay), NOT freed")
    print("class20421: unknown 49 -> 9 (40 adopted, 5 b36 WINs + 4 batch-3 stay), NOT freed")


if __name__ == "__main__":
    main()
