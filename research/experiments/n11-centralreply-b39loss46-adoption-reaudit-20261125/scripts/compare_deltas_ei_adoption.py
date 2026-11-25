"""BASE (canonical chain through the Part EE af034loss1 adoption)
vs SCENARIO (b39loss46 = Part EH batch-39 46-LOSS adoption).

Fail-closed machine recomputation of exactly what the Part EI 46-LOSS
canonical adoption changed, from published bytes only:

* every published artifact sha-pinned (the published Part EE outputs -- the
  BASE canonical cache fc3e4ac9... 6,666 rows WIN 158 / LOSS 6,508, the BASE
  reaudit outputs refresh-summary 6af660a1... / closure-classes 27e00b0d... /
  per-root-coverage 6974299b... / probe-worklist regen pin b4933810... -- the
  Part EI outputs -- increment a2b24baa..., increments manifest 6ae4058b...
  (schema b39loss46-increments-manifest-v1), the 6,712-row scenario cache
  73482be0... WIN 158 / LOSS 6,554 (chain name merged-exact-s5-chain-plus-
  b39loss46-20261125.cache; the sha pin carries the identity), the
  merge-audits x3 (identical sha 387010c5...), the byte-clone of the union
  merger 90711961..., the frozen graph/update8/board/policy/quarantine pins);
* the published Part EE refresh fork (reaudit/scripts/refresh_adoption_ee.py,
  sha 01937f23...) and the published Part EI refresh fork (reaudit/scripts/
  refresh_adoption_ei.py, sha 1bcf1972...) are RE-EXECUTED byte-verbatim in
  isolated scratch trees against their pinned inputs, and all eight outputs
  must be byte-identical to the published / regenerated pins before any delta
  is emitted (double-run determinism; this simultaneously re-proves the
  published Part EE reaudit outputs are regenerable from published bytes);
* SCEN cache == BASE cache rows + exactly the 46 increment rows (verdict
  agreement everywhere; 6,712 rows, WIN 158 / LOSS 6,554); the adopted rows
  are the 46 honest-label exact-LOSS rows of the published Part EH batch-39
  probe (closure class 30484 rank-20 fresh frontier: fresh-cold two-pass
  node-exact at the pre-declared 15M budget, order 0, MISMATCH 0, adopted
  total 140,162,086 nodes/pass of the whole packet 177,032,132; the 2
  probe-level WIN rows aj049/aj050 and the 2 EXHAUSTED honest-UNKNOWN rows
  aj030/aj039 are consumed NOWHERE; the 2 claim-reserved dual-class batch-38
  keys ai044/ai048 are Part EF in-flight owner and untouched);
* kit integrity: the published batch-39 kit (178 files, MANIFEST-sha256
  52b69c04...) verified file-by-file, including the pinned solver image
  jsreplay.js (84585617...) and runner runbatch.sh (f591f8c2...), the
  54-line honest-history status.log (08d70bb7...), the machine audit
  batch-audit.json (5a2b67cb...: 46 LOSS / 2 WIN unconsumed / 2 EXHAUSTED
  honest UNKNOWN / MISMATCH 0 / verdicts_consumed=false), the batch registry
  batch-keys-b39.json (5e25b550...), and ALL 100 byte-pinned raw replay
  files with two-pass node-exact agreement;
* the class-30484 arithmetic is recomputed from the frozen dependency graph
  with the integer-geometry Board: the 54-child canonical boundary is
  regenerated (entirely inside the s5 mask universe; ZERO non-s5 children;
  ZERO update8-receipt children); 2 children are known exact LOSS in BASE and
  52 are unknown in BASE and exactly 6 in SCEN == the pinned 6 remaining
  unknown s5 keys {892576 aj030 EXHAUSTED, 897668 aj039 EXHAUSTED,
  900354 ai044 claim-reserved, 900718 ai048 claim-reserved, 902511 aj049
  probe-level WIN unconsumed, 902512 aj050 probe-level WIN unconsumed};
  class 30484 is NOT freed and NOT excluded (unknown 52 -> 6, rank 20 -> 9,
  groups_served_count 4 static); the secondary dual-class owner 30118 shows
  unknown 54 -> 52 (exactly its 2 own adopted members; rank 39 -> 21);
* classes 16371 / 20421 / 34908 are proven BYTE-STATIC across this Part
  (their closure rows are byte-identical before/after; no adopted key sits
  inside any of their boundaries; their unconsumed WIN / EXHAUSTED pools are
  untouched);
* every closure-classes.csv row is compared: ZERO unknown_now changes beside
  classes 30484 and 30118; ZERO left/entered rows; exactly 29 rank-churn-
  only rows and ZERO groups_served churn (776 fully stable rows);
* update8 refresh: all 46 adopted s5 indices sit OUTSIDE the frozen update8
  baseline requirement: resolved stays 259, remaining stays 31,600,
  groups_free_now stays 131, the newly-resolved/lost sets are both EMPTY,
  win_hit_groups stays [] and every per-root remaining is byte-identical;
* class_status counts: excluded 390 / excluded_now 23 / free_now 39 /
  unknown 34,497 IDENTICAL before and after (the loss-only adoption frees
  nothing and excludes nothing); Board verification 39/39 with zero
  rejections on both sides; root 27 stays 119/119;
* per-root coverage: free/uncovered thirds are IDENTICAL at every root; the
  individual greedy union changes only at roots 0 and 24 (pure re-selection
  bookkeeping, no coverage claim);
* the frozen greedy scheduler deltas are recorded as bookkeeping (joint
  greedy 36,508 -> 36,505, worklist 64,414 -> 64,366, known universe
  845 -> 891, cache in universe 822 -> 868).

No unknown verdict is asserted anywhere.  The standard 11x11 empty board
and every one of the 19 central-reply roots stay UNKNOWN; free_now /
coverage quantities are scheduling bookkeeping derived from exact LOSS
verdicts, not root verdict claims.  The 2 batch-39 probe-level WIN rows and
the 2 claim-reserved batch-38 keys are consumed NOWHERE by this Part
(scrutiny-owner C++ second-implementation gate pin 9193f5b6...); no WIN
verdict and no EXHAUSTED verdict enters the canonical cache; 11x11 stays
UNKNOWN.
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

BASE_EXP = ROOT / "research/experiments/n11-centralreply-af034loss1-adoption-reaudit-20261125"
BASE_OUT = BASE_EXP / "reaudit/output"
BASE_CACHE = BASE_EXP / "output/merged-exact-s5-chain-plus-af034loss1-20261125.cache"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-b39loss46-20261125.cache"
INCR = EXP / "output/increment-b39loss46-20261125.cache"
MANIFEST = EXP / "output/increments-manifest.json"
B39_KIT = ROOT / "research/experiments/n11-centralreply-closure-class30484-batch39-20261125"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_REFRESH_SCRIPT = BASE_EXP / "reaudit/scripts/refresh_adoption_ee.py"
SCEN_REFRESH_SCRIPT = EXP / "reaudit/scripts/refresh_adoption_ei.py"
MERGER = EXP / "scripts/s5_union_merge.py"

BASE_CACHE_SHA = "fc3e4ac9052447158202f09d5efe05468dba32fe95ec90beaaa0a0de9d2c020f"
SCEN_CACHE_SHA = "73482be0cf0201b2d812f9205b0315e91527234e02196691279753853feddc70"
INCR_SHA = "a2b24baa0acb253f6b5a2901b601834b8dc50163ad500407192989efcc75e659"
MANIFEST_SHA = "6ae4058b4e419a4a05ddfff1947b23aa52acdd54febecb5d207aed7241ea5338"
BASE_SUMMARY_SHA = "6af660a1e0ad8f0ad3b0ac6b32c1a24099aa8f1c3a2271496a9bfb99dc80b6bc"
BASE_CLOSURE_SHA = "27e00b0dbf2f33603dfbed91b00153f73c7a2d05b1258133a39c9ec5bfd41364"
BASE_PRC_SHA = "6974299b57a39f7fa6aa72d76bef83a647c637dce4b2fdf23d0db4380c04a5fb"
BASE_WORKLIST_SHA = "b4933810ccd6229e43b89f6c08f3984288026925c2b44c6398a4afd0a83a183b"
SCEN_SUMMARY_SHA = "414314eb38776f7fee69b3f6d1b894ab24b8e4fac4ea578bc109fce82863329f"
SCEN_CLOSURE_SHA = "e12bf3280c77e31fc91e30e6806d2828b141af565bfa5e565a2aa3410d974673"
SCEN_PRC_SHA = "2525f3069826a055bf9bf4343c08ac217722beefdce054138a68a0976c875b8d"
SCEN_WORKLIST_SHA = "98529a8ddd457c09506a80ce2f7a6344fee3c3fcc0d63969aa391e67ad6c8e79"
BASE_REFRESH_SHA = "01937f237b922542cd0a33c6750c84f83e0be1589ed528c217e2b0e4ac2630f5"
SCEN_REFRESH_SHA = "1bcf1972be102781d056f6caae15bfc239c145d79700b74b6bac3919f03da2d6"
MERGE_AUDIT_SHA = "387010c54846676aed1cc83ae5606bc8b6e8399fc022ee9bee8f192786b128e1"
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
ADOPTED_TABLE_DIGEST = "a7ef2336dd7a93f43619a58677de2c11b6126bb89c5c8cb7fef144dfc4b3d2db"

B39_MANIFEST_SHA = "52b69c0404c9f78451249c6decc65f70b908e44a98bebac0b827d8eb8aa5bf41"
B39_KIT_FILES = 178
B39_STATUS_SHA = "08d70bb77c08e7a37b77005b3b2dca1a759f56b4146e1623eef4eb69759a3cea"
B39_AUDIT_SHA = "5a2b67cb4e8bb6b2e3cf6e8f79806ab219ff83b91639e9b4333ed2b9eb91bb4f"
B39_KEYS_SHA = "5e25b550ef42c1f56dc9d4b69d61d33304664ad839ed7f8d19f45fe50f5e63a9"
JSREPLAY_SHA = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
RUNBATCH_SHA = "f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84"
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
BOARD_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

CLASS_30484 = 30484
CLASS_30118 = 30118
CLASS_16371 = 16371
CLASS_20421 = 20421
CLASS_34908 = 34908
ADOPTED_ROWS = 46
ADOPTED_TOTAL_NODES = 140162086
WHOLE_PACKET_NODES = 177032132

ADOPTED_IDS = ["aj001", "aj002", "aj003", "aj004", "aj005", "aj006", "aj007", "aj008", "aj009", "aj010", "aj011", "aj012", "aj013", "aj014", "aj015", "aj016", "aj017", "aj018", "aj019", "aj020", "aj021", "aj022", "aj023", "aj024", "aj025", "aj026", "aj027", "aj028", "aj029", "aj031", "aj032", "aj033", "aj034", "aj035", "aj036", "aj037", "aj038", "aj040", "aj041", "aj042", "aj043", "aj044", "aj045", "aj046", "aj047", "aj048"]
PACKET_IDS = sorted(ADOPTED_IDS + ["aj049", "aj050", "aj030", "aj039"])
WIN_IDS_UNCONSUMED = ["aj049", "aj050"]
EXHAUSTED_EXCLUDED_IDS = ["aj030", "aj039"]
CLAIM_RESERVED_IDS = ["ai044", "ai048"]
CLAIM_RESERVED_PAIRS = {
    "ai044": (1152922604135256064, 65536),
    "ai048": (1152921573327372288, 68157440),
}

# class 30484 (the EI target): Board 54-child boundary, all in the s5 universe
BOUNDARY_30484_RAW = 54
BOUNDARY_30484_S5 = 54
BASE_KNOWN_LOSS_30484 = 2
UNKNOWN_BASE_30484 = 52
UNKNOWN_SCEN_30484 = 6
WIN_S5_PINNED = {"aj049": 902511, "aj050": 902512}
EXH_S5_PINNED = {"aj030": 892576, "aj039": 897668}
RESERVED_S5_PINNED = {"ai044": 900354, "ai048": 900718}
UNKNOWN_S5_REMAINING = [892576, 897668, 900354, 900718, 902511, 902512]
# secondary dual-class owner 30118 (2 own adopted members)
BOUNDARY_30118_RAW = 56
UNKNOWN_BASE_30118 = 54
UNKNOWN_SCEN_30118 = 52
OWN_ADOPTED_30118 = 2

STATUS_EXPECTED = {"excluded": 390, "excluded_now": 23, "free_now": 39, "unknown": 34497}
UPD8_RESOLVED_BEFORE = 259
UPD8_RESOLVED_AFTER = 259
UPD8_REMAINING_BEFORE = 31600
UPD8_REMAINING_AFTER = 31600
JOINT_GREEDY_BEFORE = 36508
JOINT_GREEDY_AFTER = 36505
WORKLIST_BEFORE = 64414
WORKLIST_AFTER = 64366
KNOWN_UNIVERSE_BEFORE = 845
KNOWN_UNIVERSE_AFTER = 891
CACHE_IN_UNIVERSE_BEFORE = 822
CACHE_IN_UNIVERSE_AFTER = 868
CACHE_VERDICTS_BEFORE = {"1": 158, "2": 6508}
CACHE_VERDICTS_AFTER = {"1": 158, "2": 6554}
UNIQUE_GROUPS_BEFORE = 2115
UNIQUE_GROUPS_AFTER = 2115
GROUP_BEST_NONFREE = 2115
PER_ROOT_REMAINING_DELTA = {}
PER_ROOT_COVERAGE_DELTA = {
    "0": {"free": [7, 7], "uncovered": [112, 112], "greedy": [3003, 3001]},
    "24": {"free": [12, 12], "uncovered": [107, 107], "greedy": [2827, 2782]},
}
CLOSURE_ROWS_BEFORE = 807
CLOSURE_ROWS_AFTER = 807
CLOSURE_LEFT = []
CLOSURE_ENTERED = []
CLASS_30484_ROW_BEFORE = {"class_rank": "20", "unknown_now": "52", "groups_served_count": "4"}
CLASS_30484_ROW_AFTER = {"class_rank": "9", "unknown_now": "6", "groups_served_count": "4"}
CLASS_30118_ROW_BEFORE = {"class_rank": "39", "unknown_now": "54", "groups_served_count": "4"}
CLASS_30118_ROW_AFTER = {"class_rank": "21", "unknown_now": "52", "groups_served_count": "4"}
RANK_CHURN_DETAIL = [(1518, 18, 19), (2634, 16, 17), (5343, 10, 11), (5473, 14, 15), (5687, 26, 27), (5690, 35, 36), (5830, 23, 24), (8106, 19, 20), (8785, 17, 18), (8811, 24, 25), (10968, 30, 31), (12264, 13, 14), (12643, 27, 28), (13342, 11, 12), (13758, 37, 38), (14103, 38, 39), (16131, 25, 26), (16513, 28, 29), (16930, 21, 22), (16957, 15, 16), (19749, 31, 32), (23482, 32, 33), (23964, 22, 23), (25835, 33, 34), (30345, 12, 13), (30565, 34, 35), (31600, 29, 30), (34263, 36, 37), (34269, 9, 10)]
GS_CHURN_DECREASE = []
RANK_CHURN_ROWS = 29
FULLY_STABLE_ROWS = 776
CHANGED_CLASS_SET = []

KEY_PINS = {
    "aj001": {"lo": 1152922604269469696, "hi": 65536, "legal": 84,
              "s5_index": 63021, "probe_order": 540, "membership_class_count": 4},
    "aj002": {"lo": 10376294640990027776, "hi": 65536, "legal": 90,
              "s5_index": 82345, "probe_order": 541, "membership_class_count": 4},
    "aj003": {"lo": 3458765613348945920, "hi": 65536, "legal": 81,
              "s5_index": 195180, "probe_order": 542, "membership_class_count": 4},
    "aj004": {"lo": 1152922879013158912, "hi": 65536, "legal": 84,
              "s5_index": 281792, "probe_order": 543, "membership_class_count": 4},
    "aj005": {"lo": 5764608622562639872, "hi": 65536, "legal": 86,
              "s5_index": 298723, "probe_order": 544, "membership_class_count": 4},
    "aj006": {"lo": 1152922604135317504, "hi": 65536, "legal": 88,
              "s5_index": 375902, "probe_order": 545, "membership_class_count": 4},
    "aj007": {"lo": 1152922604135251968, "hi": 65537, "legal": 91,
              "s5_index": 391885, "probe_order": 546, "membership_class_count": 4},
    "aj008": {"lo": 1152922604135251968, "hi": 65538, "legal": 92,
              "s5_index": 474119, "probe_order": 547, "membership_class_count": 4},
    "aj009": {"lo": 1152922741574205440, "hi": 65536, "legal": 81,
              "s5_index": 634046, "probe_order": 548, "membership_class_count": 4},
    "aj010": {"lo": 1152923153891065856, "hi": 65536, "legal": 83,
              "s5_index": 644052, "probe_order": 549, "membership_class_count": 4},
    "aj011": {"lo": 1155174403948937216, "hi": 65536, "legal": 84,
              "s5_index": 655118, "probe_order": 550, "membership_class_count": 4},
    "aj012": {"lo": 1152922604135251968, "hi": 66048, "legal": 89,
              "s5_index": 657320, "probe_order": 551, "membership_class_count": 4},
    "aj013": {"lo": 1152922604202360832, "hi": 65536, "legal": 91,
              "s5_index": 739110, "probe_order": 552, "membership_class_count": 4},
    "aj014": {"lo": 1152922604403687424, "hi": 65536, "legal": 79,
              "s5_index": 744807, "probe_order": 553, "membership_class_count": 4},
    "aj015": {"lo": 1157426203762622464, "hi": 65536, "legal": 79,
              "s5_index": 753448, "probe_order": 554, "membership_class_count": 4},
    "aj016": {"lo": 1152922604135251968, "hi": 66560, "legal": 91,
              "s5_index": 754653, "probe_order": 555, "membership_class_count": 4},
    "aj017": {"lo": 1152922604135284736, "hi": 65536, "legal": 96,
              "s5_index": 815958, "probe_order": 556, "membership_class_count": 4},
    "aj018": {"lo": 1152922604135383040, "hi": 65536, "legal": 87,
              "s5_index": 819898, "probe_order": 557, "membership_class_count": 4},
    "aj019": {"lo": 1161929803389992960, "hi": 65536, "legal": 86,
              "s5_index": 826659, "probe_order": 558, "membership_class_count": 4},
    "aj020": {"lo": 1152922604135251968, "hi": 67584, "legal": 92,
              "s5_index": 827583, "probe_order": 559, "membership_class_count": 4},
    "aj021": {"lo": 1152922604135252032, "hi": 65536, "legal": 95,
              "s5_index": 873785, "probe_order": 560, "membership_class_count": 4},
    "aj022": {"lo": 1170937002644733952, "hi": 65536, "legal": 96,
              "s5_index": 878828, "probe_order": 561, "membership_class_count": 4},
    "aj023": {"lo": 1152922604135251968, "hi": 69632, "legal": 82,
              "s5_index": 879486, "probe_order": 562, "membership_class_count": 4},
    "aj024": {"lo": 1152922604135252480, "hi": 65536, "legal": 97,
              "s5_index": 888597, "probe_order": 563, "membership_class_count": 4},
    "aj025": {"lo": 1152922604137349120, "hi": 65536, "legal": 93,
              "s5_index": 888632, "probe_order": 564, "membership_class_count": 4},
    "aj026": {"lo": 1152922604135252224, "hi": 65536, "legal": 95,
              "s5_index": 890205, "probe_order": 565, "membership_class_count": 4},
    "aj027": {"lo": 1152922608430219264, "hi": 65536, "legal": 91,
              "s5_index": 890217, "probe_order": 566, "membership_class_count": 4},
    "aj028": {"lo": 1152922604135252096, "hi": 65536, "legal": 91,
              "s5_index": 891252, "probe_order": 567, "membership_class_count": 4},
    "aj029": {"lo": 1152931400228274176, "hi": 65536, "legal": 94,
              "s5_index": 891691, "probe_order": 568, "membership_class_count": 4},
    "aj031": {"lo": 1152921574400065536, "hi": 1056768, "legal": 85,
              "s5_index": 893069, "probe_order": 570, "membership_class_count": 4},
    "aj032": {"lo": 1152922604135251972, "hi": 65536, "legal": 95,
              "s5_index": 893865, "probe_order": 571, "membership_class_count": 4},
    "aj033": {"lo": 1152921574400065536, "hi": 17825792, "legal": 97,
              "s5_index": 894452, "probe_order": 572, "membership_class_count": 4},
    "aj034": {"lo": 1152922604135251970, "hi": 65536, "legal": 96,
              "s5_index": 895046, "probe_order": 573, "membership_class_count": 4},
    "aj035": {"lo": 1152921573326324224, "hi": 68157440, "legal": 97,
              "s5_index": 895603, "probe_order": 574, "membership_class_count": 4},
    "aj036": {"lo": 1152922604135251969, "hi": 65536, "legal": 84,
              "s5_index": 896123, "probe_order": 575, "membership_class_count": 3},
    "aj037": {"lo": 1152921573326324736, "hi": 68157440, "legal": 82,
              "s5_index": 896603, "probe_order": 576, "membership_class_count": 3},
    "aj038": {"lo": 1152922604135776256, "hi": 65536, "legal": 96,
              "s5_index": 897649, "probe_order": 577, "membership_class_count": 4},
    "aj040": {"lo": 1152922604135514112, "hi": 65536, "legal": 89,
              "s5_index": 898280, "probe_order": 579, "membership_class_count": 4},
    "aj041": {"lo": 1152927002181763072, "hi": 65536, "legal": 94,
              "s5_index": 898533, "probe_order": 580, "membership_class_count": 4},
    "aj042": {"lo": 1152922604135268352, "hi": 65536, "legal": 83,
              "s5_index": 899043, "probe_order": 581, "membership_class_count": 4},
    "aj043": {"lo": 1152921574400065536, "hi": 1064960, "legal": 89,
              "s5_index": 899372, "probe_order": 582, "membership_class_count": 4},
    "aj044": {"lo": 1152922604135260160, "hi": 65536, "legal": 91,
              "s5_index": 899741, "probe_order": 583, "membership_class_count": 4},
    "aj045": {"lo": 1152921574400065536, "hi": 34603008, "legal": 96,
              "s5_index": 900167, "probe_order": 584, "membership_class_count": 4},
    "aj046": {"lo": 1152922672854728704, "hi": 65536, "legal": 88,
              "s5_index": 901454, "probe_order": 587, "membership_class_count": 3},
    "aj047": {"lo": 1152924803158507520, "hi": 65536, "legal": 91,
              "s5_index": 901621, "probe_order": 588, "membership_class_count": 4},
    "aj048": {"lo": 1152921574400065536, "hi": 1081344, "legal": 86,
              "s5_index": 902090, "probe_order": 589, "membership_class_count": 4},
}

LABEL_PINS = {
    "aj001": (2, 5156075),
    "aj002": (2, 3369672),
    "aj003": (2, 3540581),
    "aj004": (2, 2262352),
    "aj005": (2, 1633255),
    "aj006": (2, 2722354),
    "aj007": (2, 3164790),
    "aj008": (2, 2063326),
    "aj009": (2, 1387399),
    "aj010": (2, 1456727),
    "aj011": (2, 3327536),
    "aj012": (2, 3786919),
    "aj013": (2, 3372877),
    "aj014": (2, 2835620),
    "aj015": (2, 1067011),
    "aj016": (2, 2629159),
    "aj017": (2, 2855076),
    "aj018": (2, 2238708),
    "aj019": (2, 2269913),
    "aj020": (2, 8446897),
    "aj021": (2, 2357351),
    "aj022": (2, 2872347),
    "aj023": (2, 2536040),
    "aj024": (2, 3959639),
    "aj025": (2, 2265870),
    "aj026": (2, 7255317),
    "aj027": (2, 2846576),
    "aj028": (2, 2976049),
    "aj029": (2, 4011534),
    "aj031": (2, 9591637),
    "aj032": (2, 2768559),
    "aj033": (2, 4367387),
    "aj034": (2, 3029800),
    "aj035": (2, 2604201),
    "aj036": (2, 2158472),
    "aj037": (2, 2348985),
    "aj038": (2, 2701920),
    "aj040": (2, 1869701),
    "aj041": (2, 1382704),
    "aj042": (2, 1487463),
    "aj043": (2, 1414800),
    "aj044": (2, 3325637),
    "aj045": (2, 3712262),
    "aj046": (2, 2031254),
    "aj047": (2, 3033556),
    "aj048": (2, 1666778),
    "aj030": (0, 15000000),      # EXHAUSTED honest UNKNOWN, no same-condition re-probe
    "aj039": (0, 15000000),      # EXHAUSTED honest UNKNOWN, no same-condition re-probe
    "aj049": (1, 4998452),      # probe-level WIN, UNCONSUMED (scrutiny-owner C++ gate only)
    "aj050": (1, 1871594),      # probe-level WIN, UNCONSUMED (scrutiny-owner C++ gate only)
}

RAW_SHAS = {
    "aj001.p1.out": "9666ca540a9df869847094989da30dc96e4d0285b782f22397c57172d83a9d85",
    "aj001.p2.out": "25278cdd052da6f4b2e0cc9954e88d8dd496ab0b81a8eedd6e0b4603931eb04b",
    "aj002.p1.out": "8949697f87317eabb9700a6e5d897d10690b3173800f6b8cae5d1b485431931f",
    "aj002.p2.out": "8949697f87317eabb9700a6e5d897d10690b3173800f6b8cae5d1b485431931f",
    "aj003.p1.out": "8cf27a85697a4aa5124d65ae6fe39f4de6e8db8394a7a2be5e3272f2a5c1d6d9",
    "aj003.p2.out": "8acf755c0a48590d9e8bd213a0e22ab8b8fc9ab819c35e914d344e7dd3dbf308",
    "aj004.p1.out": "42ce5d28566d8c7b5beebdd5c4c2d820a704cb330c7ab7e90de55a5756c468d6",
    "aj004.p2.out": "69bbd88a72ec061057e273ab283df750216a488915e557862683c5eaab0b6782",
    "aj005.p1.out": "78631be25aece45afa80ace6fead4ca155f8014e4c2d9826e7d973ab7b8673e6",
    "aj005.p2.out": "206319ea967918cd990f3dce81132fd647042ee031d3624e6a564568ab3379ef",
    "aj006.p1.out": "efd9b8b402a33afdcc4a166fb2cc86aa60321cfe4e75489c66b2321d9451681e",
    "aj006.p2.out": "3d71e086504f548b81a4b71822203ab7cfe25c5e32cccba7698ec4b574b217af",
    "aj007.p1.out": "b5a0a5c4cd10895da2fdb9ecb862ca3e9d385243ccd19b68440e78e21f22e03f",
    "aj007.p2.out": "1e66d8f34d278ae68f8992f7f6a1b81ce031e4cdcdf021bdd3fcdaff256105ad",
    "aj008.p1.out": "fd6d28b5539b64c17319d1abc49de46ca6fe271744760e94e2c059e673402cee",
    "aj008.p2.out": "666855ca6dd9df74f1553942f1d439ef6f2efb6bf1d0c97a0a7243d6f23d3371",
    "aj009.p1.out": "eaa74d446489c0291efc80d836cc8c0a1a522063828f32bb6bc4fa1b37c3cf48",
    "aj009.p2.out": "d5d14051989407ddb98b35df0102230416de12412e6d0c8916415404c89f6994",
    "aj010.p1.out": "f535f7d8db8896950e2bf3ba445d93146ae90e08eb82f7c129e7c18b86dd3bdc",
    "aj010.p2.out": "00e3d2c4daa47b136476cfea32f9ddc9c1fd334cb1ef7711dc91065376547096",
    "aj011.p1.out": "e6d9e1bfa795c409aabced98ac8a4ffd056eb4e652a438be8a3dfb3724abb4f2",
    "aj011.p2.out": "d70ad80023f63932a1039a4bfc09a3d6a0853e73b91bd14b7638aaac97efd599",
    "aj012.p1.out": "bd7c356afe21f3e508deb63b7831e64e3bb587676e4a90a25e29e04218679e4c",
    "aj012.p2.out": "38823089d1b023f20791a6f151a483192511f49ecd4f53ebd43aad0a8a8db3f7",
    "aj013.p1.out": "b63686550fda7c141b16f33b0fdf0cec2ae1f2473870ef44470e0045ed0e4d3f",
    "aj013.p2.out": "d6db26d024d4f8b408ed84a8a7c9a59e58d4470c3910d1ad2f391c53a29c908d",
    "aj014.p1.out": "240afa41bc1eba0aca23a2f3675cddf423bba60c0e1bf960e70b309b871848e9",
    "aj014.p2.out": "240afa41bc1eba0aca23a2f3675cddf423bba60c0e1bf960e70b309b871848e9",
    "aj015.p1.out": "e7b42c0da52da64e01211eb9bbabc12527aba625273bb294f3b222ba84bc94f7",
    "aj015.p2.out": "97b45f39c619a6ebf97962f0e6fbe7f67f9250f14ae7cbab3fb260c9a1871978",
    "aj016.p1.out": "536d309cd1e894ea628d670f568abe7c418dc7bf557b22127c7554c81926f6bb",
    "aj016.p2.out": "6b51f3717989c33712e3c167bb8e3f11ea844346a483b0e94066fb1100da7585",
    "aj017.p1.out": "6cc6cc13a781c84cfd4186a5c33e7516c87bb9d79c34500b37596b7b95215279",
    "aj017.p2.out": "2bbe05692891b3e7fc9e84a44074dca5a0c7f52ccf8d5a7f80a416d79e7530b8",
    "aj018.p1.out": "08817a6517d88ba6ce29b26125c65dc76dadbdd4185595a5cbc8e5f0f485bc5b",
    "aj018.p2.out": "237da4263355c17184ce401bbed3fac7189d2e2d262402e51b5c04bae7362919",
    "aj019.p1.out": "046d4e9e34fe914c5b265179d178fced31199b2d4e566d37140e532495533474",
    "aj019.p2.out": "63d6edb36f28ad68d76ec4b25caee10817c4e0db8a536529181123b16751b8d7",
    "aj020.p1.out": "a39a8e5a07e65f5b6010806b01af457a9c8f653baa4edc65b866f81b29fe2e8e",
    "aj020.p2.out": "50dcdc94cfa2a4db9acbdcb649b57b4ae8bd4b979a569cdb92c4844714d3d1ca",
    "aj021.p1.out": "cd37ccaa2c053b739ca186b73b42edb4827144a3b12a5db49f2f403ea7452384",
    "aj021.p2.out": "be27c17e38db12238bd46b58674515580e87da549280845c52905c128d4a729b",
    "aj022.p1.out": "b2379e4fb2a00e81fc2193dbf815e7b1a99ab9cfe61f56f6a3a14ff81966a749",
    "aj022.p2.out": "6a2114665133a3ecf9a711dd4303b7416972bb0883dc4fe817f74875930a6119",
    "aj023.p1.out": "3161b5fe3cb849fa7301e0df67396237dc9c45b1fe0ec7d4c9bca7628105b021",
    "aj023.p2.out": "3161b5fe3cb849fa7301e0df67396237dc9c45b1fe0ec7d4c9bca7628105b021",
    "aj024.p1.out": "086e97c1ade6111ecea4acd7aeb327e513b0eaf9427775fb4ba8d473be7278ed",
    "aj024.p2.out": "3dcf62aa560b216c5fbf640542b5fee92a80a755848fc729ed90171e6dc97934",
    "aj025.p1.out": "ad8d5b1a3136cc25685ccf6b93ac6a5e12c985cae555889171377fab1bd27e5c",
    "aj025.p2.out": "e965f4007e49d6d62371bbc91fe7da94dc6cf6df7511025381d2af2410c0641e",
    "aj026.p1.out": "5343fa1106f83496e19dd7eb2d1a9cbcd3e3dd5bb46b0ad260aafc184a7d1044",
    "aj026.p2.out": "95e7a972f13c58f8c75c320375d97f5fba1100b15fe3b8b4776ba07f8caaa199",
    "aj027.p1.out": "503025b99a15bc853dbaf3137983eb2a510bed7c9d4f868801ea554a634104a5",
    "aj027.p2.out": "9c654a186790c79cb7aa15391399de74501d2a295b31e08fe33b28b8b71e6a9a",
    "aj028.p1.out": "65be6b06cba4ba0dabcd60711aeeaa60a1982666087ed10cf631d45097ad41fc",
    "aj028.p2.out": "0bdbff7dc3f0387d9db612f5f39cdcfc177196dbf017e8c559792c007bed23d8",
    "aj029.p1.out": "83e4eccfe66b9578c40ba131e141a965202fd5650969ded3942631689a1ae2ba",
    "aj029.p2.out": "8d9f4cae54f07cb0cd7d7e1b1e1f83e968ae1f5fdb484c315c61a695641af9a0",
    "aj030.p1.out": "843a0a0c976699d937391377455504797f5bece24222eef74d4452f20e20178c",
    "aj030.p2.out": "661c8e410f8e3f93227ac635233556fec5069ccf115117255a38b3b19f551757",
    "aj031.p1.out": "5504dd94a6158db298537289474d8d328338dc9ed24a0df11583c26f46f2a740",
    "aj031.p2.out": "51749d8e538d7783bf48e12bee073a2f4043e16c0bbcd1dd1d24dc0ef3b1a62a",
    "aj032.p1.out": "926de19c7c651af999fc53cd0cff4c663a882160f9130242c00b5c1b880b8ddd",
    "aj032.p2.out": "926de19c7c651af999fc53cd0cff4c663a882160f9130242c00b5c1b880b8ddd",
    "aj033.p1.out": "de8564d4e2602d2656d5e0ff6f816694d93df8ac295fa97ce51c143e1e15ce84",
    "aj033.p2.out": "97af056fa673c635227eead5aae5af358f7c6be1497993a1e90dd5e9b430f008",
    "aj034.p1.out": "2995e911d98c1068731a2af38fe5124b5705962206d4d0f6c332e4b5364e8757",
    "aj034.p2.out": "2995e911d98c1068731a2af38fe5124b5705962206d4d0f6c332e4b5364e8757",
    "aj035.p1.out": "2399c538b6c5c8f1f8d21a82140512d2ef0bb9a812a07777407ace372e979e84",
    "aj035.p2.out": "e2143007d9dedf7bfccaa82436be4cea85dda4ed06377848fb637d6a8226203b",
    "aj036.p1.out": "13e240dd3aafe4f17e966d65897630f62496bc0b41d5c09aaeef4e7feaa934a4",
    "aj036.p2.out": "c804396450572319cf4680befa41beb9687a4a08bb14e9d7da3ec71ae6c96051",
    "aj037.p1.out": "d4410dce0e0183bc1b2ad4dc38c7e15cf49db824e2c0dcaaed0e306317eb501e",
    "aj037.p2.out": "20d2c70d5d3e7aa22f6716018f27d6938fc9094c4dd669ce4a52b6f9541f4ca7",
    "aj038.p1.out": "40783d648c22e3dbfee0317db49a2b05b2c3bd40fff2641b7a9b86f5bf164a05",
    "aj038.p2.out": "8c8911e3a1b60e474fccf7fb98010abf1dc6837c6b498d42bf238cc0cef65ea3",
    "aj039.p1.out": "60ae21db0e099b22403b8ce64ba97e15de3987acfafb218d79c11aae6c3b4906",
    "aj039.p2.out": "c51899d50649444c3ee8cbb43f3318392131cc3add8b54cbe77d3f600a59dfbb",
    "aj040.p1.out": "f22352e6f0c10f57331c9ec5820acd1ae19098a42642c5327f9f7cadadf5ddd8",
    "aj040.p2.out": "3bf639e7ce62e299a3e83b901585c89b548297854d9807412c41719833cedaf2",
    "aj041.p1.out": "60dad9728700b01bcd3cfdb2c3ac4ebb64133ca3b9e65cd2c5cefe76c70d3dca",
    "aj041.p2.out": "76b9c6656cfd7a5baa4ff1b56aa201fad70b6928a0dcb99419f3aff6ad35a3dd",
    "aj042.p1.out": "a05c6fc592baeae2e980546ecb5756d819975ac5f718f2598f65298cc4dd8621",
    "aj042.p2.out": "c77a84437a65b3743e293102c54ce385675964ac98f5d0b0b9e0d2b64cc6d136",
    "aj043.p1.out": "8220827aab50a8db18af6133f93ddc471a56b3a548d9135ecca3f3bcd520398d",
    "aj043.p2.out": "7d2af2a8379ac2d3a4ba34e436f2521c2cc0d3dcfd2ebddcdf41466c13ff43a3",
    "aj044.p1.out": "f8fa1da185b52f6bf45ef4d5a0d10e0c0bfd1be3f37df7e14dbf5d8637d6eb54",
    "aj044.p2.out": "9d4fcce8bc527707b63537674f7161340f77026b2ec579a23703509b14928b65",
    "aj045.p1.out": "3449d0e484b2b507dd3e541bbe1d48ddf2fa46195bfcfeab748c37144cf0fac1",
    "aj045.p2.out": "9e3c8301242092b54217a5e78df44e07f19c1014ce4ccc6bf42340bdae300cb9",
    "aj046.p1.out": "907db6eeb6637755d49521a1400a36040400c6e4392ae55b7c02f48c0f258eb9",
    "aj046.p2.out": "0da68bb4455fa1d421562cdd88ec5e7b866cca8010f4a190b4a6c5a69b7867a6",
    "aj047.p1.out": "bb5c805201b2344ff8bc93f09dd4cfbb39be3d827c5f6298c23022e2b3e57a4c",
    "aj047.p2.out": "ea2b3d61a57447ce78b74eb0d621163efd5b81bd4a7db1716757e956a797a345",
    "aj048.p1.out": "913c96d67ff9bf8b8cc923b1044cc3138eb0bdee3c30333259e4848aef6903ec",
    "aj048.p2.out": "179f96fd1e75a1788103dfccabc48103a8a3cb7ce6a630b54f7bd2d6f58b4d7e",
    "aj049.p1.out": "50a195f0a1348812bca31ba2279f123bd39cd6928cf4e022c775257771fa695e",
    "aj049.p2.out": "9b7c058feb4665546b4c05b53cd8363bd38c5b30bd9c5fd4ec7a0a701eb83b2d",
    "aj050.p1.out": "50e997dbc23df812f52f6ddcd57839ce447aa92425908b35f34077d47918def2",
    "aj050.p2.out": "8ea868801d44f8522e2ba481c4d8cfdebbf4a2b4cba75f9a0034f61d739cb9f8",
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fail(msg):
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


def verify_kit(dirp: Path, manifest_sha, files_expected):
    if sha(dirp / "MANIFEST-sha256.txt") != manifest_sha:
        fail(f"kit {dirp.name} MANIFEST sha drift")
    n = 0
    prefix = "research/experiments/" + dirp.name + "/"
    for line in (dirp / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split()
        want, rel = fields[0], fields[1]
        if not rel.startswith(prefix):
            fail(f"kit {dirp.name} MANIFEST path outside the kit dir: {rel}")
        p = dirp / rel[len(prefix):]
        if not p.is_file():
            fail(f"kit {dirp.name} file missing: {rel}")
        if sha(p) != want:
            fail(f"kit {dirp.name} sha drift at {rel}")
        n += 1
    if n != files_expected:
        fail(f"kit {dirp.name} files {n} != {files_expected}")
    return n


def rerun_refresh(script: Path, script_sha: str, tmp_name: str):
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


def two_pass_raw(kid: str, shas: dict):
    rows = {}
    for tag in ("p1", "p2"):
        p = B39_KIT / f"output/raw/{kid}.{tag}.out"
        if sha(p) != shas[f"{kid}.{tag}.out"]:
            fail(f"raw replay sha drift vs the pinned published bytes: {kid}.{tag}.out")
        row = None
        seen = 0
        for line in p.read_text().splitlines():
            if line.startswith("replay,"):
                parts = line.split(",")
                seen += 1
                row = {"stones": int(parts[2]), "legal": int(parts[3]),
                       "is_or": int(parts[4]), "budget": int(parts[5]),
                       "result": int(parts[6]), "nodes": int(parts[7]),
                       "lo": parts[9], "hi": parts[10]}
        if seen != 1 or row is None:
            fail(f"expected exactly one replay row in {p}")
        if "# replay_done" not in p.read_text():
            fail(f"raw {kid}.{tag}.out lacks the '# replay_done' completeness guard")
        rows[tag] = row
    ref = rows["p1"]
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
    for tag, r in rows.items():
        if tuple(r[f] for f in fields) != tuple(ref[f] for f in fields):
            fail(f"two-pass raw disagreement (fresh-cold node-exact gate): {kid}.{tag}")
    return ref


def main() -> None:
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
        ("b39 kit status", B39_KIT / "output/status.log", B39_STATUS_SHA),
        ("b39 kit audit", B39_KIT / "output/batch-audit.json", B39_AUDIT_SHA),
        ("b39 kit keys", B39_KIT / "input/batch-keys-b39.json", B39_KEYS_SHA),
    ]
    for name, p, want in pins:
        got = sha(p)
        if got != want:
            fail(f"{name} sha drift: {got} != {want}")
    kit_files = verify_kit(B39_KIT, B39_MANIFEST_SHA, B39_KIT_FILES)
    if sha(B39_KIT / "scripts/jsreplay.js") != JSREPLAY_SHA:
        fail("jsreplay.js sha drift in the batch-39 kit (pinned solver image 8458...)")
    if sha(B39_KIT / "scripts/runbatch.sh") != RUNBATCH_SHA:
        fail("runbatch.sh sha drift in the batch-39 kit (pinned runner f591...)")

    # --- batch-39 audit honesty pins ---------------------------------------
    audit = json.loads((B39_KIT / "output/batch-audit.json").read_text())
    if audit["schema"] != "n11-centralreply-closure-batch39-audit-v1":
        fail("batch-39 audit schema drift")
    res = audit["results"]
    if (res["LOSS"], res["WIN"], res["EXHAUSTED"], res["MISMATCH"]) != (46, 2, 2, 0):
        fail("batch-39 audit honest-label accounting drift (46/2/2/0)")
    if res["total_nodes_all_keys_single_pass"] != WHOLE_PACKET_NODES:
        fail("batch-39 whole-packet node total drift")
    if res["win_keys_unconsumed"] != WIN_IDS_UNCONSUMED:
        fail("batch-39 audit unconsumed-WIN key set drift")
    if res["exhausted_keys_honest_unknown"] != EXHAUSTED_EXCLUDED_IDS:
        fail("batch-39 audit exhausted key set drift")
    if audit["verdicts_consumed_into_canonical_cache"]:
        fail("batch-39 audit verdicts_consumed must be false")
    audit_per = {e["key_id"]: e for e in audit["per_key"]}
    if len(audit_per) != 50:
        fail("batch-39 audit per_key must hold exactly 50 rows")

    # --- batch-39 key registry: extend pins to all 50 packet keys ----------
    registry = json.loads((B39_KIT / "input/batch-keys-b39.json").read_text())
    if registry["schema"] != "n11-centralreply-closure-batch39-keys-v1":
        fail("batch-39 key registry schema drift")
    reg_keys = registry["keys"]
    if len(reg_keys) != 50:
        fail("batch-39 key registry must hold 50 keys")
    REG = {e["key_id"]: e for e in reg_keys}
    if sorted(REG) != sorted(PACKET_IDS):
        fail("batch-39 key registry id set != the 50-key packet")
    EXT_KEYS = {}
    for kid, e in KEY_PINS.items():
        r = REG[kid]
        if (r["lo"], r["hi"], r["legal"], r["s5_index"], r["probe_order"]) != (
                e["lo"], e["hi"], e["legal"], e["s5_index"], e["probe_order"]):
            fail(f"KEY_PINS registry disagreement for {kid}")
        EXT_KEYS[kid] = e
    for kid in PACKET_IDS:
        if kid not in EXT_KEYS:
            EXT_KEYS[kid] = {"lo": REG[kid]["lo"], "hi": REG[kid]["hi"],
                             "legal": REG[kid]["legal"], "s5_index": REG[kid]["s5_index"],
                             "probe_order": REG[kid]["probe_order"]}

    # --- all 100 raw pairs two-pass node-exact vs status labels -------------
    raws = {}
    for kid in PACKET_IDS:
        raws[kid] = two_pass_raw(kid, RAW_SHAS)
        e = EXT_KEYS[kid]
        r = raws[kid]
        if r["stones"] != 5 or r["is_or"] != 0 or r["budget"] != 15000000:
            fail(f"{kid} raw depth/or/budget drift")
        if (r["legal"], r["lo"], r["hi"]) != (e["legal"], str(e["lo"]), str(e["hi"])):
            fail(f"{kid} raw key-field disagreement vs the pinned registry")
        if (r["result"], r["nodes"]) != LABEL_PINS[kid]:
            fail(f"{kid} raw honest-label drift vs the pinned audit label")
        ap = audit_per[kid]
        if (ap["result"], ap["nodes"], ap["probe_order"]) != (r["result"], r["nodes"], e["probe_order"]):
            fail(f"{kid} batch-audit per_key drift vs the raw replay")
    if sorted(k for k in raws if raws[k]["result"] == 2) != sorted(ADOPTED_IDS):
        fail("batch-39 decisive LOSS set != the adopted 46")
    if sum(raws[k]["nodes"] for k in ADOPTED_IDS) != ADOPTED_TOTAL_NODES:
        fail("adopted node total drift")
    if sum(raws[k]["nodes"] for k in PACKET_IDS) != WHOLE_PACKET_NODES:
        fail("whole-packet node total drift")

    # --- manifest decomposition ---------------------------------------------
    manifest = json.loads(MANIFEST.read_text())
    if manifest["schema"] != "b39loss46-increments-manifest-v1":
        fail("manifest schema drift")
    if manifest["base_cache_sha256"] != BASE_CACHE_SHA:
        fail("manifest base cache pin drift")
    if manifest["sha256"]["loss_increment"] != INCR_SHA:
        fail("manifest loss_increment pin drift")
    if manifest["merger_sha256"] != MERGER_SHA:
        fail("manifest merger pin drift")
    if manifest["adopted_table_digest_sha256"] != ADOPTED_TABLE_DIGEST:
        fail("manifest adopted-table digest drift")
    if len(manifest["adopted_table"]) != ADOPTED_ROWS:
        fail("manifest adopted_table must hold 46 rows")
    if sum(r["nodes"] for r in manifest["adopted_table"]) != ADOPTED_TOTAL_NODES:
        fail("manifest adopted_table node sum drift")
    if manifest["base_cache_rows"] != 6666:
        fail("manifest base rows drift")
    if manifest["base_cache_absent_hits_for_emitted"] != 0:
        fail("manifest emitted rows must be absent from BASE")
    if manifest["quarantine_hits"] != 0:
        fail("manifest quarantine hits must be 0")
    if manifest["row_counts"] != {"adopted_loss_rows": 46, "wins_unconsumed": 2,
                                  "exhausted_excluded": 2, "claim_reserved_excluded": 2,
                                  "prior_adopted_loss_rows_base": 1}:
        fail("manifest row_counts drift")
    if manifest["loss_ids"] != ADOPTED_IDS or manifest["resolved_ids"] != ADOPTED_IDS:
        fail("manifest loss/resolved id sets drift")
    if manifest["unadopted_win_ids"] != WIN_IDS_UNCONSUMED:
        fail("manifest unconsumed WIN id set drift")
    if manifest["exhausted_excluded_ids"] != EXHAUSTED_EXCLUDED_IDS:
        fail("manifest exhausted id set drift")
    if manifest["full_packet_eq_loss_only"] is not False:
        fail("manifest full_packet_eq_loss_only must be false (packet spans 46+2+2)")
    if manifest["win_scenario_exists"] is not True:
        fail("manifest win_scenario_exists must be true (2 probe-level WIN rows)")
    wr = {(e["lo"], e["hi"]): e for e in manifest["unadopted_win_rows"]}
    if len(manifest["unadopted_win_rows"]) != len(wr):
        fail("manifest unconsumed WIN rows contain a duplicate (lo,hi) pair")
    if sorted(wr) != sorted((EXT_KEYS[k]["lo"], EXT_KEYS[k]["hi"]) for k in WIN_IDS_UNCONSUMED):
        fail("manifest unconsumed WIN rows keys drift")
    for k in WIN_IDS_UNCONSUMED:
        e = wr[(EXT_KEYS[k]["lo"], EXT_KEYS[k]["hi"])]
        if (e["hi"], e["legal"], e["result"], e["nodes"]) != (
                EXT_KEYS[k]["hi"], EXT_KEYS[k]["legal"], 1, LABEL_PINS[k][1]):
            fail(f"manifest unconsumed WIN row {k} pin drift")
    er = {(e["lo"], e["hi"]): e for e in manifest["exhausted_rows"]}
    if len(er) != len(manifest["exhausted_rows"]):
        fail("manifest exhausted rows contain a duplicate (lo,hi) pair")
    for k in EXHAUSTED_EXCLUDED_IDS:
        e = er[(EXT_KEYS[k]["lo"], EXT_KEYS[k]["hi"])]
        if (e["hi"], e["legal"], e["result"], e["nodes"]) != (
                EXT_KEYS[k]["hi"], EXT_KEYS[k]["legal"], 0, LABEL_PINS[k][1]):
            fail(f"manifest exhausted row {k} pin drift")
    if len(manifest["batches"]) != 1:
        fail("manifest must hold exactly one batch pool")
    b = manifest["batches"][0]
    if b["pool"] != "b39loss46":
        fail("unexpected pool in the EI manifest")
    if b["adopted_loss_ids"] != ADOPTED_IDS:
        fail("pool adopted id set drift")
    if b["probed_ids"] != PACKET_IDS:
        fail("pool probed id set drift")
    if b["unadopted_win_ids"] != WIN_IDS_UNCONSUMED or b["exhausted_excluded_ids"] != EXHAUSTED_EXCLUDED_IDS:
        fail("pool unconsumed/excluded sets drift")
    if b["claim_reserved_excluded_ids"] != CLAIM_RESERVED_IDS:
        fail("pool claim-reserved id set drift")
    if b["adopted_nodes_per_pool"] != ADOPTED_TOTAL_NODES or b["whole_packet_nodes"] != WHOLE_PACKET_NODES:
        fail("pool node accounting drift")
    if b["status_log_sha256"] != B39_STATUS_SHA or b["status_log_lines"] != 54:
        fail("pool status-log pin drift")
    if b["probed_budget"] != 15000000:
        fail("pool probed budget drift (pre-declared 15M)")
    ki = b["kit_integrity"]
    if ki["kit_manifest_sha256"] != B39_MANIFEST_SHA or ki["kit_files_verified"] != B39_KIT_FILES:
        fail("pool kit integrity pins drift")
    if ki["raw_file_sha256_pins"] != RAW_SHAS:
        fail("pool raw-file pin table drift")
    if ki["batch_audit_sha256"] != B39_AUDIT_SHA or ki["batch_keys_sha256"] != B39_KEYS_SHA:
        fail("pool batch audit/keys pins drift")

    # --- refresh re-execution (double-run determinism) -----------------------
    base_tmp = rerun_refresh(BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA, ".eiverify-base-ee2")
    scen_tmp = rerun_refresh(SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA, ".eiverify-scen-ei")
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
    shutil.rmtree(ROOT / "research/experiments/.eiverify-base-ee2")
    shutil.rmtree(ROOT / "research/experiments/.eiverify-scen-ei")

    # --- cache relation: SCEN == BASE + exactly the 46 increment rows --------
    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    incr = load_cache(INCR)
    if len(base) != 6666 or len(scen) != 6712 or len(incr) != ADOPTED_ROWS:
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
    if (wins, losses) != (158, 6554):
        fail(f"scenario verdict counts {wins}/{losses} != 158/6,554")
    adopted_keys = {(KEY_PINS[k]["lo"], KEY_PINS[k]["hi"]) for k in ADOPTED_IDS}
    if set(incr) != adopted_keys or len(incr) != 46:
        fail("increment key set != the pinned 46 adopted keys")
    tab = {(int(e["lo"]), int(e["hi"])): e for e in manifest["adopted_table"]}
    if set(tab) != set(incr):
        fail("manifest adopted_table keys != increment keys")
    for key, row in incr.items():
        if row != (tab[key]["result"], tab[key]["nodes"]):
            fail(f"manifest adopted_table row != increment row: {key}")
        if tab[key]["legal"] != KEY_PINS[[k for k in ADOPTED_IDS
                                           if (KEY_PINS[k]["lo"], KEY_PINS[k]["hi"]) == key][0]]["legal"]:
            fail(f"manifest adopted_table legal drift: {key}")
    for kid in WIN_IDS_UNCONSUMED + EXHAUSTED_EXCLUDED_IDS:
        key = (EXT_KEYS[kid]["lo"], EXT_KEYS[kid]["hi"])
        if key in incr or key in base or key in scen:
            fail(f"the unconsumed key {kid} must sit in NO cache (WIN scrutiny / EXH no-reprobe)")
    for cid, key in CLAIM_RESERVED_PAIRS.items():
        if key in incr or key in base or key in scen:
            fail(f"the claim-reserved batch-38 key {cid} must sit in NO cache (Part EF owner)")

    # --- Board arithmetic ------------------------------------------------------
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
    adopted_s5 = sorted(mask_to_index[k] for k in adopted_keys)
    if len(adopted_s5) != 46:
        fail("adopted s5 index set size drift")
    if set(adopted_s5) & set(update8["required_new_s5"]):
        fail("an adopted s5 index sits inside the frozen update8 baseline requirement")
    for pinned, ids in ((WIN_S5_PINNED, WIN_IDS_UNCONSUMED),
                        (EXH_S5_PINNED, EXHAUSTED_EXCLUDED_IDS),
                        (RESERVED_S5_PINNED, CLAIM_RESERVED_IDS)):
        for kid in ids:
            if kid in EXT_KEYS:
                pair = (EXT_KEYS[kid]["lo"], EXT_KEYS[kid]["hi"])
            else:
                pair = CLAIM_RESERVED_PAIRS[kid]
            idx = mask_to_index.get(pair)
            if idx is None:
                fail(f"{kid} mask pair is not an s5 universe member")
            if idx != pinned[kid]:
                fail(f"{kid} s5 index {idx} != the pinned {pinned[kid]}")

    # --- class 30484 (the EI target) -----------------------------------------
    lo, hi = s4_masks[CLASS_30484]
    children = board.children(lo | (hi << 64))
    child_keys = {(c & ((1 << 64) - 1), c >> 64) for c in children}
    if len(child_keys) != BOUNDARY_30484_RAW:
        fail(f"class-30484 Board child boundary {len(child_keys)} != {BOUNDARY_30484_RAW}")
    non_s5 = [k for k in child_keys if k not in mask_to_index]
    if non_s5:
        fail("class-30484 boundary must have ZERO non-s5 children")
    in_s5 = list(child_keys)
    receipt_child = [k for k in in_s5 if mask_to_index[k] in receipt_verdicts]
    if receipt_child:
        fail("class-30484 must have ZERO update8-receipt children")
    known_base = [k for k in in_s5 if k in base]
    if len(known_base) != BASE_KNOWN_LOSS_30484:
        fail(f"class-30484 BASE-known child count {len(known_base)} != {BASE_KNOWN_LOSS_30484}")
    for k in known_base:
        if base[k][0] != 2:
            fail("a BASE-known child of 30484 is not an exact LOSS")
    unknown_base = [k for k in in_s5 if k not in base]
    if len(unknown_base) != UNKNOWN_BASE_30484:
        fail(f"class-30484 BASE unknown {len(unknown_base)} != {UNKNOWN_BASE_30484}")
    unknown_scen = [k for k in in_s5 if k not in scen]
    if len(unknown_scen) != UNKNOWN_SCEN_30484:
        fail(f"class-30484 SCEN unknown {len(unknown_scen)} != {UNKNOWN_SCEN_30484} (NOT freed: reserved/EXH/WIN remain)")
    if sorted(mask_to_index[k] for k in unknown_scen) != UNKNOWN_S5_REMAINING:
        fail("scenario unknown children of 30484 != the pinned 6 remaining s5 keys")
    own = in_s5 and (set(in_s5) & adopted_keys)
    if own != adopted_keys:
        fail("class-30484 adopted-own set != exactly the 46 EI rows")
    if any(k in quarantined for k in child_keys):
        fail("a quarantined key sits inside the class-30484 child boundary")

    # --- class 30118 (secondary dual-class owner) ---------------------------
    lo2, hi2 = s4_masks[CLASS_30118]
    kids2 = {(c & ((1 << 64) - 1), c >> 64) for c in board.children(lo2 | (hi2 << 64))}
    if len(kids2) != BOUNDARY_30118_RAW:
        fail(f"class-30118 Board child boundary {len(kids2)} != {BOUNDARY_30118_RAW}")
    own2 = kids2 & adopted_keys
    if len(own2) != OWN_ADOPTED_30118:
        fail(f"secondary dual-class owner 30118 must hold exactly 2 adopted members (got {len(own2)})")
    unk2b = [k for k in kids2 if k not in base]
    unk2s = [k for k in kids2 if k not in scen]
    if len(unk2b) != UNKNOWN_BASE_30118 or len(unk2s) != UNKNOWN_SCEN_30118:
        fail(f"class-30118 unknown {len(unk2b)}->{len(unk2s)} != 54->52")
    if set(unk2b) - set(unk2s) != own2:
        fail("class-30118 unknown delta != its own adopted membership")

    # --- not-EI-owned classes: boundary + byte-static assertion -------------
    for cls in (CLASS_16371, CLASS_20421, CLASS_34908):
        clo, chi = s4_masks[cls]
        kids = {(c & ((1 << 64) - 1), c >> 64) for c in board.children(clo | (chi << 64))}
        if adopted_keys & kids:
            fail(f"no adopted key may sit inside the class-{cls} boundary (not EI-owned)")
        if any(k in quarantined for k in kids):
            fail(f"a quarantined key sits inside the class-{cls} boundary")

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
    if newly or lost:
        fail("update8 newly-resolved/lost sets must BOTH be empty (46 adopted keys sit outside)")
    if rb["groups_free_now"] != 131 or rs["groups_free_now"] != 131:
        fail("update8 groups_free_now drift (must stay 131 static)")
    if rs.get("win_hit_groups", rb.get("win_hit_groups")) not in ([], None):
        fail("win_hit_groups non-empty (a WIN was consumed)")

    # --- class status / universe metrics ------------------------------------
    cb, cs = base_summary["class_status_counts"], scen_summary["class_status_counts"]
    if cb != STATUS_EXPECTED or cs != STATUS_EXPECTED:
        fail(f"class status counts drift vs the pinned static transition: {cb} {cs}")
    if scen_summary["board_verification"] != {"free_candidates": 39, "board_verified_free": 39, "rejected": {}}:
        fail("scenario board verification shape drift")
    if base_summary["board_verification"] != {"free_candidates": 39, "board_verified_free": 39, "rejected": {}}:
        fail("base board verification shape drift")
    if scen_summary["inputs"]["cache_rows"] != 6712 \
            or scen_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_AFTER \
            or scen_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_AFTER:
        fail("scenario inputs metrics drift")
    if base_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["cache_rows"] != 6666:
        fail("base inputs metrics drift")
    bcv, scv = base_summary["inputs"]["cache_verdicts"], scen_summary["inputs"]["cache_verdicts"]
    if bcv != CACHE_VERDICTS_BEFORE or scv != CACHE_VERDICTS_AFTER:
        fail("cache verdict counts drift")

    # per-root coverage: free/uncovered thirds identical at EVERY root
    prc_pairs = list(zip(
        csv.DictReader(BASE_OUT.joinpath("per-root-coverage.csv").open()),
        csv.DictReader((EXP / "reaudit/output/per-root-coverage.csv").open())))
    prc_delta = {}
    for bb, srow in prc_pairs:
        if bb["first"] != srow["first"]:
            fail("per-root rows misaligned")
        if bb["free_now"] != srow["free_now"] or bb["uncovered"] != srow["uncovered"] \
                or bb["individual_greedy_union"] != srow["individual_greedy_union"]:
            prc_delta[srow["first"]] = {
                "free": [int(bb["free_now"]), int(srow["free_now"])],
                "uncovered": [int(bb["uncovered"]), int(srow["uncovered"])],
                "greedy": [int(bb["individual_greedy_union"]), int(srow["individual_greedy_union"])],
            }
    if prc_delta != PER_ROOT_COVERAGE_DELTA:
        fail(f"per-root coverage delta {prc_delta} != the pinned re-selection churn")
    for root, d in prc_delta.items():
        if d["free"][0] != d["free"][1] or d["uncovered"][0] != d["uncovered"][1]:
            fail(f"root {root} free/uncovered thirds changed although no class was freed")
    root27 = [srow for bb, srow in prc_pairs if srow["first"] == "27"][0]
    if root27["free_now"] != "119" or root27["uncovered"] != "0":
        fail("root 27 coverage regressed")
    rb_pr, rs_pr = rb["per_root_remaining"], rs["per_root_remaining"]
    deltas = {k: rs_pr[k] - rb_pr[k] for k in rb_pr if rs_pr[k] != rb_pr[k]}
    if deltas != PER_ROOT_REMAINING_DELTA:
        fail(f"per-root remaining delta {deltas} != pinned")
    if any(v > 0 for v in deltas.values()):
        fail("a per-root remaining INCREASED (coverage regression)")

    # --- joint greedy / worklist bookkeeping ---------------------------------
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

    # --- closure-classes table diff -------------------------------------------
    def read_closure(p: Path):
        return {int(r["class_index"]): r for r in csv.DictReader(p.open())}

    cb_t = read_closure(BASE_OUT / "closure-classes.csv")
    cs_t = read_closure(EXP / "reaudit/output/closure-classes.csv")
    if len(cb_t) != CLOSURE_ROWS_BEFORE or len(cs_t) != CLOSURE_ROWS_AFTER:
        fail(f"closure table row counts {len(cb_t)}/{len(cs_t)} != 807/807")
    left = sorted(set(cb_t) - set(cs_t))
    entered = sorted(set(cs_t) - set(cb_t))
    if left != CLOSURE_LEFT or entered != CLOSURE_ENTERED:
        fail(f"closure table left/entered must be EMPTY: {left} / {entered}")
    for col, want in CLASS_30484_ROW_BEFORE.items():
        if cb_t[CLASS_30484][col] != want:
            fail(f"base class-30484 row {col} drift: {cb_t[CLASS_30484][col]} != {want}")
    for col, want in CLASS_30484_ROW_AFTER.items():
        if cs_t[CLASS_30484][col] != want:
            fail(f"scenario class-30484 row {col} drift: {cs_t[CLASS_30484][col]} != {want}")
    if int(cb_t[CLASS_30484]["unknown_now"]) - int(cs_t[CLASS_30484]["unknown_now"]) != len(own):
        fail("class-30484 unknown delta != its own adopted children (Board boundary)")
    for col, want in CLASS_30118_ROW_BEFORE.items():
        if cb_t[CLASS_30118][col] != want:
            fail(f"base class-30118 row {col} drift")
    for col, want in CLASS_30118_ROW_AFTER.items():
        if cs_t[CLASS_30118][col] != want:
            fail(f"scenario class-30118 row {col} drift")
    diff_30118 = {k: (cb_t[CLASS_30118][k], cs_t[CLASS_30118][k])
                  for k in cb_t[CLASS_30118] if cb_t[CLASS_30118][k] != cs_t[CLASS_30118][k]}
    if set(diff_30118) != {"class_rank", "unknown_now"}:
        fail(f"class-30118 must differ in class_rank/unknown_now ONLY: {diff_30118}")
    for cls in (CLASS_16371, CLASS_20421, CLASS_34908):
        if cb_t.get(cls) != cs_t.get(cls):
            fail(f"class-{cls} closure row must be byte-identical before/after (not EI-owned)")
    changed, rank_churn, stable, gs_dec, gs_bad = [], 0, 0, [], []
    rank_churn_classes = []
    for ci, brow in sorted(cb_t.items()):
        if ci in (CLASS_30484, CLASS_30118) or ci not in cs_t:
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
            gs_dec.append({"class_index": ci,
                           "class_rank": [int(diff["class_rank"][0]), int(diff["class_rank"][1])],
                           "groups_served_count": [int(diff["groups_served_count"][0]),
                                                    int(diff["groups_served_count"][1])],
                           "unknown_now": [int(brow["unknown_now"]), int(srow["unknown_now"])]})
            continue
        if "unknown_now" not in diff:
            fail(f"class {ci} changed unexpected columns: {diff}")
        b_unk, s_unk = int(diff["unknown_now"][0]), int(diff["unknown_now"][1])
        clo, chi = s4_masks[ci]
        kids = {(c & ((1 << 64) - 1), c >> 64) for c in board.children(clo | (chi << 64))}
        own_c = len(kids & adopted_keys)
        if (b_unk - s_unk) != own_c or own_c == 0:
            fail(f"class {ci} unknown delta {b_unk}->{s_unk} != own adopted membership {own_c}")
        changed.append({"class_index": ci, "unknown_before": b_unk,
                        "unknown_after": s_unk, "own_adopted": own_c})
    if changed != CHANGED_CLASS_SET:
        fail(f"changed-class set must be EMPTY beside the dedicated 30484/30118 "
              f"sections: {changed}")
    if rank_churn_classes != RANK_CHURN_DETAIL:
        fail(f"rank-churn-only rows != the pinned 29-row churn detail: {rank_churn_classes}")
    if rank_churn != RANK_CHURN_ROWS or stable != FULLY_STABLE_ROWS:
        fail(f"rank churn {rank_churn}/stable {stable} != pinned {RANK_CHURN_ROWS}/{FULLY_STABLE_ROWS}")
    if gs_dec != GS_CHURN_DECREASE:
        fail(f"groups_served_count churn set != the pinned empty churn: {gs_dec}")
    scen_first = scen_summary["closure_classes_first"]
    c30484 = [e for e in scen_first if e["class_index"] == CLASS_30484]
    if len(c30484) != 1 or c30484[0]["unknown_now"] != 6 or len(c30484[0]["groups_served"]) != 4:
        fail("scenario closure_classes_first entry for class 30484 drift (rank-9 / 6-unknown / 4-group)")

    # --- emit decomp -------------------------------------------------------
    out = {
        "schema": "b39loss46-adoption-decomp-deltas-v1",
        "scenario": "ADOPTED-CANONICAL",
        "packet": {
            "batches": [{"pool": "b39loss46", "class_index": 30484,
                         "probed_rows": 50, "adopted_loss_rows": 46,
                         "unadopted_win_rows": 2, "exhausted_excluded_rows": 2,
                         "adopted_nodes_per_pool": ADOPTED_TOTAL_NODES,
                         "whole_packet_nodes": WHOLE_PACKET_NODES}],
            "adopted_loss_rows": ADOPTED_ROWS,
            "unadopted_win_rows": 2,
            "exhausted_excluded_rows": 2,
            "claim_reserved_untouched": 2,
            "adopted_total_nodes_per_pass": ADOPTED_TOTAL_NODES,
            "whole_packet_nodes_per_pass": WHOLE_PACKET_NODES,
            "adopted_loss_ids": ADOPTED_IDS,
            "decisive_labels": "46 fresh LOSS @15M order 0 adopted (Part EH batch-39, "
                               "two-pass fresh-cold node-exact, MISMATCH 0); 2 probe-level "
                               "WIN rows (aj049/aj050) are unconsumed (scrutiny-owner C++ "
                               "gate 9193f5b6 exclusive); 2 EXHAUSTED rows (aj030/aj039) "
                               "stay honest UNKNOWN (same-condition re-probe prohibited); "
                               "the 2 claim-reserved dual-class batch-38 keys ai044/ai048 "
                               "untouched (Part EF in-flight owner)",
        },
        "cache": {
            "base_sha256": BASE_CACHE_SHA, "scenario_sha256": SCEN_CACHE_SHA,
            "base_rows": len(base), "scenario_rows": len(scen), "increment_rows": len(incr),
            "verdict_counts": {"WIN": 158, "LOSS": 6554},
            "relation": "scenario == base rows + the 46 increment rows verbatim (no other row changed)",
            "merge_audit_runs": 3, "merge_audit_sha256_each": MERGE_AUDIT_SHA,
            "adopted_s5_indices": adopted_s5,
            "naming_note": "chain name merged-exact-s5-chain-plus-b39loss46-20261125.cache "
                           "(short-form convention; the sha pin carries the identity)",
        },
        "class_30484": {
            "children_total_raw": len(child_keys), "non_s5_children": 0,
            "unknown_before": 52, "unknown_after": 6,
            "adopted_own": 46,
            "unconsumed_win_children": 2, "still_exhausted_children": 2,
            "claim_reserved_children": 2,
            "base_known_loss_children": 2, "receipt_known_loss_children": 0,
            "status_before": "unknown", "status_after": "unknown",
            "class_rank": [int(cb_t[CLASS_30484]["class_rank"]), int(cs_t[CLASS_30484]["class_rank"])],
            "groups_served_count": [4, 4],
            "unknown_s5_remaining": UNKNOWN_S5_REMAINING,
            "unknown_s5_remaining_ids": {"aj030": 892576, "aj039": 897668,
                                          "ai044": 900354, "ai048": 900718,
                                          "aj049": 902511, "aj050": 902512},
            "not_a_root_verdict": "the loss-only adoption of the 46 rows frees nothing and "
                                  "excludes nothing; free_now/coverage quantities are "
                                  "Board-derived scheduling bookkeeping; no root verdict and "
                                  "no coverage claim is made",
        },
        "class_30118": {
            "status": "secondary dual-class owner: exactly 2 adopted members inside its "
                      "56-child Board boundary",
            "class_rank": [int(cb_t[CLASS_30118]["class_rank"]), int(cs_t[CLASS_30118]["class_rank"])],
            "groups_served_count": [4, 4], "unknown": [54, 52], "own_adopted": 2},
        "class_16371": {"status": "byte-static across Part EI (not EI-owned; closure row "
                                   "byte-identical, no adopted key inside its Board boundary, "
                                   "no consumed and no quarantined key enters or leaves it)"},
        "class_20421": {"status": "byte-static across Part EI (not EI-owned; closure row "
                                   "byte-identical, no adopted key inside its Board boundary, "
                                   "no consumed and no quarantined key enters or leaves it)"},
        "class_34908": {"status": "byte-static across Part EI (not EI-owned; closure row "
                                   "byte-identical, no adopted key inside its Board boundary, "
                                   "no consumed and no quarantined key enters or leaves it)"},
        "closure_table": {
            "rows_before": CLOSURE_ROWS_BEFORE, "rows_after": CLOSURE_ROWS_AFTER,
            "left": left, "entered": entered,
            "left_reason": "EMPTY: the 807-row frontier table is fully static across this "
                           "Part (no left/entered exchange)",
            "unknown_changed_classes": changed,
            "rank_churn_only_rows": rank_churn,
            "rank_churn_detail": [{"class_index": ci, "from": f, "to": t}
                                  for ci, f, t in rank_churn_classes],
            "groups_served_decrease_churn": gs_dec,
            "fully_stable_rows": stable,
        },
        "update8": {
            "resolved_before": UPD8_RESOLVED_BEFORE, "resolved_after": UPD8_RESOLVED_AFTER,
            "newly_resolved_s5": [],
            "newly_resolved_within_adopted": False,
            "note": "all 46 adopted s5 indices sit OUTSIDE the frozen update8 baseline "
                    "requirement: resolved, remaining and every per-root remaining are "
                    "BYTE-STATIC",
            "remaining_before": UPD8_REMAINING_BEFORE, "remaining_after": UPD8_REMAINING_AFTER,
            "groups_free_now_static": 131,
        },
        "class_status_counts_before": cb,
        "class_status_counts_after": cs,
        "metrics": {
            "joint_greedy_union_size": [JOINT_GREEDY_BEFORE, JOINT_GREEDY_AFTER],
            "worklist_total": [WORKLIST_BEFORE, WORKLIST_AFTER],
            "known_universe_indices": [KNOWN_UNIVERSE_BEFORE, KNOWN_UNIVERSE_AFTER],
            "cache_rows_in_universe": [CACHE_IN_UNIVERSE_BEFORE, CACHE_IN_UNIVERSE_AFTER],
            "unique_groups": [UNIQUE_GROUPS_BEFORE, UNIQUE_GROUPS_AFTER],
            "per_root_remaining_delta": PER_ROOT_REMAINING_DELTA,
            "per_root_coverage_delta": PER_ROOT_COVERAGE_DELTA,
            "note": "the joint greedy union shrinks (36,508 -> 36,505) and the worklist "
                    "shrinks (64,414 -> 64,366) after class 30484's frontier cost drops "
                    "(unknown 52 -> 6); per-root free/uncovered thirds are IDENTICAL at "
                    "every root (nothing was freed); roots 0/24 individual greedy unions "
                    "shift as pure bookkeeping; root 27 stays 119/119",
        },
        "verification": {
            "kit_files_verified": {"b39": kit_files},
            "packet_pins": {"status_log": B39_STATUS_SHA, "batch_audit": B39_AUDIT_SHA,
                            "batch_keys": B39_KEYS_SHA, "ed_manifest": B39_MANIFEST_SHA},
            "refresh_scripts_reexecuted": [BASE_REFRESH_SHA, SCEN_REFRESH_SHA],
            "refresh_outputs_byte_identical": True,
            "board_child_regeneration": "class-30484 54-child and class-30118 56-child "
                                        "boundaries regenerated via Board(11).children",
        },
        "interpretation_guard":
            "only the 46 fresh batch-39 exact-LOSS rows (two-pass fresh-cold node-exact at "
            "the pre-declared 15M condition) are consumed into the canonical cache by this "
            "Part; the 2 probe-level WIN rows (aj049/aj050) and the 2 EXHAUSTED "
            "honest-UNKNOWN rows (aj030/aj039) are consumed NOWHERE (WIN adoption is "
            "scrutiny-owner C++ second-implementation gate pin 9193f5b6 exclusive; EXH "
            "same-condition re-probe prohibited); the 2 claim-reserved dual-class batch-38 "
            "keys (ai044/ai048) are the Part EF in-flight owner and untouched; class 30484 "
            "(6 children remaining: 2 EXH, 2 unconsumed WIN, 2 claim-reserved) and class "
            "30118 (52 remaining) are NOT freed and NOT excluded; classes "
            "16371/20421/34908 are byte-static; class status stays unknown, free_now 39 "
            "static, closure table 807 rows static with NO left/entered exchange, 29 "
            "rank-churn-only rows being pure bookkeeping; no root verdict and no coverage "
            "claim is made anywhere; the per-root/greedy/worklist quantities quoted here "
            "are bookkeeping, never verdicts; no update8 resolution changed (all 46 "
            "adopted keys sit outside the frozen baseline requirement); 11x11 stays UNKNOWN",
    }
    (EXP / "output/decomp-deltas-b39loss46-adoption.json").write_text(
        json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("DECOMP OK changed=%d rank_churn=%d gs_dec=%d stable=%d left=%d entered=%d" % (
        len(changed), rank_churn, len(gs_dec), stable, len(left), len(entered)))
    print("class30484: unknown 52 -> 6 (46 adopted; 2 EXH + 2 unconsumed WIN + 2 reserved remain), NOT freed, rank 20 -> 9")
    print("class30118: secondary owner unknown 54 -> 52 (2 own adopted), rank 39 -> 21")
    print("16371/20421/34908: byte-static")


if __name__ == "__main__":
    main()
