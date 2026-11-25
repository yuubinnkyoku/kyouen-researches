"""Batch-31 (class 5804) 51-LOSS adoption reaudit delta extractor (Part DL).

Fail-closed, read-only audit executing the single-owner Part DL declaration
(research/log/2026-11-24-part-dl-b31loss51-adoption-declaration.md,
2026-11-24; publish-then-execute).  Compares the published BASE refresh
outputs (the Part DB reaudit on the canonical cache 04b0a239..., 6,354
rows) against the single post-adoption computation:

  ADOPTED-CANONICAL = BASE + the 51 fresh LOSS rows
  (batch-31 / class 5804: ad001..ad054 except {ad024, ad028, ad043, ad055};
  nodes total 237,596,711 per pass)

The batch is PROBE-COMPLETE: all 55 of 55 keys carry honest two-pass
fresh-cold probe labels (51 LOSS adopted here; 4 probe-level WINs
ad024 (nodes 4,360,661, s5 198576), ad028 (nodes 12,803,283, s5 207094),
ad055 (nodes 3,364,655, s5 212536) at budget 15M and ad043 (nodes
18,247,029, s5 212115) at the Part DI 30M reprobe, superseding its
published 15M EXHAUSTED label).  All four WIN rows stay UNCONSUMED: not
adopted, not emitted, not written into any canonical cache, and NOT a
verdict claim (WIN-row scrutiny belongs to the C++ second-implementation
owner pin 9193f5b6...).  Hence class 5804 does NOT free and is NOT
excluded: its leftover unknown children are exactly the four unconsumed
WIN s5 indices {198576, 207094, 212115, 212536}; scenario status stays
unknown with unknown 55 -> 4 (rank 38 -> 4 in the closure table).

Gates (fail-closed, machine-checked) mirror the Part DB extractor
discipline adapted to the probe-complete 1-kit + 1-reprobe-kit /
51-fresh-LOSS-row / 4-unconsumed-WIN / 1-superseded-EXHAUSTED /
0-fileless shape of batch-31:

  * sha256 pins: increment, increments manifest, scenario cache, base
    cache, base summary, scenario summary, base/scenario
    closure-classes.csv, base/scenario per-root-coverage.csv,
    base/scenario probe-worklist.csv (the BASE worklist is the Part DB
    regenerable pin 4ecb9a0a...), the batch-31 batch-keys file, the
    drive status log, the batch-31 kit MANIFEST-sha256.txt AND the
    published Part DI reprobe kit MANIFEST-sha256.txt (with a full
    file-by-file sha re-verification of all 194 + 40 listed files), and
    all 24 val-gate host files (4 patterns x 6 hosts);
  * status log gates: 59 lines = 55 strict PASS rows (51 LOSS, 3 WIN
    rows ad024/ad028/ad055 with result 1, one superseded ad043
    exhaustion row with result 0) + exactly three pinned WIN-HALT rows
    (ad024/ad028/ad055) + exactly one pinned ad043 EXHAUSTED row; the
    per-key (result, nodes) == the pinned raw table for all 55 keys;
    the final line and the timestamp window pinned;
  * manifest (b31loss51-increments-manifest-v1): 51 fresh LOSS / 0
    prior / 4 unconsumed WIN / 0 excluded-EXHAUSTED / 0 fragments /
    0 fileless; win_ids == the four keys; unadopted_win_rows == the
    pinned rows; ad043_supersede block (DI kit 40 files, DI status
    f681a3c4..., DI ad043 30M raws pinned, the DI exh15m clones
    byte-equal to the batch-31 15M exhaustion raws, DI canonical-cache
    clone byte-equal to BASE); not loss-only; loss sha == increment
    sha; merger pin; base cache pin 04b0a239... (6,354 rows,
    prior adoption confirmations 0, zero absent hits for emitted rows,
    zero quarantine hits); node totals pinned (237,596,711 both
    passes); stop rule pinned; fragment_state empty;
  * val-gate six-host gates: for each of the 4 probe patterns the
    replay rows of published-baseline / b31-host / d2-host / tk-host /
    di-host are byte-compared field-by-field except wall time
    (node-exact), the budgets/results/nodes pinned (adaptive 2M
    exhaustion (0, 2000000) x2, 15M LOSS (2, 3651923) and
    (2, 5040200)), the two val-gate molecules canonical-safe, not
    quarantined, and disjoint from the batch keys, the caches, the
    increment and the update8 receipts;
  * independent two-pass raw re-verification of ALL 55 probed keys from
    the kit raws: both passes agree exactly, every row at budget 15M
    with the pinned (result, nodes); the DI reprobe gates: the ad043
    30M raws two-pass node-exact (result 1, nodes 18,247,029), the DI
    exh15m clones byte-equal to the batch-31 ad043 15M raws, and the
    ad054/ad055 30M anchor raws reproducing the batch-31 rows
    node-exactly (ad055 WIN 3,364,655 at both 15M and 30M,
    budget-independence anchor); the raw inventory is exactly the 110
    files ad001..ad055 x {p1,p2};
  * increment == exactly the 51 fresh LOSS rows; the four WIN keys
    asserted NOT in the increment and absent from BASE (consumed
    nowhere); the 51 adopted keys absent from BASE; exactly one
    adopted s5 index (148458, ad009) intersects the update8 baseline
    requirement (declared machine-observed);
  * scenario cache == BASE rows + the 51 increment rows with verdict
    agreement (6,405 rows; 158 WIN / 6,247 LOSS);
  * every graph holder class of every adopted key (union 126: class
    5804 holds all 51; 8730 holds 2; the remaining 124 holders hold
    exactly 1 or 2 with the pinned distribution {1: 102, 2: 23,
    51: 1});
  * the published refresh recomputes (class statuses with Board
    free-candidate child verification, known-universe counts, per-root
    coverage) are re-executed from graph + update8 + cache and asserted
    equal to the published BASE (Part DB reaudit) and scenario outputs
    before any delta is emitted;
  * status transitions pinned all-stable (excluded 390 / excluded_now
    23 / free_now 38 / unknown 34,498 on both sides), no excluded_now
    flips (a zero-WIN-consumed adoption excludes nothing), no newly
    free class beyond the machine recomputation, no per-root coverage
    regression, root 27 stays 119/119;
  * class 5804 focus gates: BASE-unknown children == exactly the 55 s5
    indices of the batch keys, own increment membership == 51,
    leftover == [198576, 207094, 212115, 212536] == the unconsumed
    WIN s5 set, scenario unknown == the leftover, scenario status ==
    "unknown" (NOT free_now, NOT excluded_now);
  * closure table: class 5804 unknown_now 55 -> 4 (rank 38 -> 4); the
    only other unknown_now changes are the holder classes 8730
    ((60, 56) -> (30, 54), own 2) and 8811 ((50, 55) -> (38, 54),
    own 1); every class that changes unknown_now is a holder with
    exact own-membership arithmetic and every other column stable;
    exactly 54 classes churn rank with stable unknown (pure ranking
    bookkeeping, none of them a holder of the adopted keys;
    {'excluded_now': 4, 'unknown': 50}); table stays 808 rows with
    left == entered == empty; anchors 23101 (rank 1, unknown 1) and
    1849 (rank 2, unknown 1) stay fully stable while 16757 holds
    unknown 29 in both rows, its rank moving 4 -> 5 because classes
    5804/8730/8811 overtake;
  * update8 refresh: resolved 141 -> 142 (+1: s5 148458 == ad009, the
    single adopted key that is an update8 baseline requirement),
    remaining 31,718 -> 31,717, no resolution lost, newly resolved
    set exactly [148458];
  * metrics pinned (both sides exact): excluded 390 / excluded_now 23
    / free_now 38 / unknown 34,498 class_status_counts pairs; joint
    greedy 36,903 -> 36,854 (net -49, frozen greedy scheduler
    bookkeeping decrease after 51 frontier slots resolve: per-root
    free/uncovered thirds are unchanged everywhere, NOT a coverage
    claim and NOT a verdict); worklist 64,765 -> 64,711 (net -54);
    group best options 2,119 stable; per-root greedy movers exactly
    roots 4 (-1), 5 (-2), 13 (-1), 25 (-1), 38 (-50), 49 (-105) with
    pinned values and unchanged free/uncovered thirds; roots_summary
    moved EMPTY; worklist serving rows of class 5804 shrink 55 -> 4
    (exactly the four unconsumed WIN rows remain), no adopted key row
    remains in the scenario worklist, the four unconsumed WIN keys
    keep their worklist presence (ad024 serves {5804, 8811}; ad028/
    ad043/ad055 serve {5804} only on the scenario side), and the
    serving class deltas pinned {5804: 55->4, 8730: 56->54, 8811:
    55->54}.

Scheduling quantities are bookkeeping, never verdicts.  11x11 stays
UNKNOWN; the four unconsumed WIN rows are not verdicts; nodes are
bookkeeping, never verdicts.  This extractor is a REGENERATION after
the 2026-11-24T08:16-08:19Z sandbox environment reset destroyed the
pre-publication Part DL working tree (only the declaration survived on
main); all BASE/scenario outputs, caches, kits and fresh pins were
byte-recovered or byte-reproduced first, and the superseded pins are
recorded in the incident amendment log.
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
OUT = EXP / "output/decomp-deltas-b31loss51-adoption.json"

GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_DIR = ROOT / "research/experiments/n11-centralreply-class2251-loss37-adoption-reaudit-20261124/reaudit/output"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class2251-loss37-adoption-reaudit-20261124/output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-20261124.cache"
KIT_DIR = ROOT / "research/experiments/n11-centralreply-closure-class5804-batch31-20261124"
DI_DIR = ROOT / "research/experiments/n11-centralreply-closure-class5804-b31ad043-reprobe30m-20261124"
SCEN_OUT = EXP / "reaudit/output"
INCR_CACHE = EXP / "output/increment-b31loss51-20261124.cache"
MANIFEST = EXP / "output/increments-manifest.json"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-20261124.cache"

INCR_SHA = "e750a0e6ea4333f9705c0898914a289c388143ac78cbf58d337d640a7457c0d5"
MANIFEST_SHA = "ae06f855a34cc186eb1811629f2911958fefc7ed073e220bdceba76388575f27"
SCEN_CACHE_SHA = "60222707dd13902103fc8f7ef11c8487ec1be531ad0711e23e50c32154e30b84"
BASE_CACHE_SHA = "04b0a23987a97518e276ea5ff966496facab22f93628cd5fbc682a04c3650556"
BASE_SUMMARY_SHA = "1fc531d32fcd8817ec2b4bcfafea2b2c40fecde409c62347da3d7e7e1d601148"
SCEN_SUMMARY_SHA = "fea0b0d4473b34447556f3a3e8b9ecc7c57c59221b18c4bb58222e0149b2e4bc"
BASE_CLOSURE_SHA = "b37425d7686efc5446bd5e0dca9feac0413284e23f4e16e32cf8c5abc4d05bfb"
BASE_PRC_SHA = "8f69d5bbfbcace73985a66c2167b2b4f5e177a22f2bf427c71a7e466a93326bd"
SCEN_CLOSURE_SHA = "50841fa47676be8af145f1f8f751b0d96f75e94417990418cbe1d2a52bd4d389"
SCEN_PRC_SHA = "136e308a332c8ab6fe877f3ef3a3b361770931285d91a0d12a59a6dd9707b487"
BASE_WORKLIST_SHA = "4ecb9a0ac2d1c9282f54f1a554fd17088b5a47b93936e5c96d783cec91483599"
SCEN_WORKLIST_SHA = "006ccd78d061c22838b3cee7701a91649d35abf3c8d56cecbb05931b604846d5"
B31_KEYS_SHA = "d058fddc862c5f62b387eea7c7ac5b78f2c5063661371b388e5078772af4ff0e"
STATUS_LOG_SHA = "c69c2fec9d07e50dca6763fdb97acb5a05798b7852a1ab45be8e7a7a7889dd5b"
KIT_MANIFEST_SHA = "3481019545cc1ed6d86765130ea895915e5b18865dfd6ed29d673fdff2d98b9a"
KIT_FILES = 194
DI_MANIFEST_SHA = "31ac5acdc2fcacb58f1bf5e27ddcff3e6dd09be0885c434a084354a71de3a682"
DI_KIT_FILES = 40
DI_STATUS_SHA = "f681a3c47c00f2f14ba670162a3606903ebde246df6b8ea634888730a582c2c5"
DI_STATUS_LINES = 5
DI_STATUS_FINAL_LINE = "2026-11-24T07:16:30Z ad043 WIN-HALT"
DI_AD043_P1_SHA = "a17572d9768cc341f2618e3a6c79b549acbe19c2b514e57662fc1386f22f8049"
DI_AD043_P2_SHA = "dd405f061a2c485cda4467752e3579cc897b1f421ee7b2117d9bda3e7ba7ee01"
DI_EXH15M_P1_SHA = "5f3bf5bc6f6bc636c7aa6d7e72619530ce2a0b918558d635ac7191b27c729d11"
DI_EXH15M_P2_SHA = "1feacf0c91cfaa72e9f3965bc0be83beb6aebbba005a74f0fbbdcfffb4b4db15"
DI_ANCHOR54_SHA = "c2d1500b831836c7791d96d3fab5f344c59bff506d96854c510a2c504e9ae1e0"
DI_ANCHOR55_SHA = "61704c55151f00db87c59285e40ba01180da5b762c9bb73ecf285fe93b9c34dd"
MERGE_AUDIT_SHA = "dc312c0720f81b61bbe3bb70e55736d2773de8714bd782992098c1341b531622"
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"

SCENARIO = "ADOPTED-CANONICAL"
UNIVERSE_SIZE = 31859
RECEIPT_COUNT = 23
ADOPTED_ROWS = 51
PRIOR_ROWS = 0
B31_CLASS = 5804
BUDGET = 15000000
REPROBE_BUDGET = 30000000
STATUS_LINES = 59
STATUS_FINAL_ROW = "2026-11-24T06:57:11Z ad055 WIN-HALT"
STATUS_TS_MIN = "2026-11-24T01:42:23Z"
STATUS_TS_MAX = "2026-11-24T06:57:10Z"
WIN_IDS = ["ad024", "ad028", "ad043", "ad055"]
WIN_HALT_LINES = [
    "2026-11-24T02:01:45Z ad024 WIN-HALT",
    "2026-11-24T02:05:32Z ad028 WIN-HALT",
    "2026-11-24T06:57:11Z ad055 WIN-HALT",
]
EXHAUSTED_LINES = [
    "2026-11-24T06:46:37Z ad043 EXHAUSTED 15000000,0,15000000",
]
EXHAUSTED_ID = "ad043"
STOP_RULE = ('batch-31 probe-complete (55/55 keys carry honest labels: 51 LOSS 2-pass fresh-cold budget 15M across Part CY drive-1 + drive-2 takeover + Part DI reprobe; loss-only adoption of the 51 fresh rows; the four probe-level WINs ad024/ad028/ad043/ad055 stay unconsumed pending the scrutiny-owner C++ gate; verdict not consumed)')
STATUS_LOG_NOTE = ("the drive log lists exactly one strict verdict row per probed key "
                   "plus three WIN-HALT rows (ad024/ad028/ad055, result 1) and one "
                   "superseded 15M EXHAUSTED row (ad043, result 0): 51 LOSS rows, "
                   "3 WIN rows and one exhaustion row, all two-pass node-exact "
                   "against the raws; lines are completion-ordered, not key-ordered "
                   "(parallel workers); no junk rows, no fragment rows, no truncated "
                   "sidecars")
ADOPTED_IDS = ['ad001', 'ad002', 'ad003', 'ad004', 'ad005', 'ad006', 'ad007', 'ad008', 'ad009', 'ad010', 'ad011', 'ad012', 'ad013', 'ad014', 'ad015', 'ad016', 'ad017', 'ad018', 'ad019', 'ad020', 'ad021', 'ad022', 'ad023', 'ad025', 'ad026', 'ad027', 'ad029', 'ad030', 'ad031', 'ad032', 'ad033', 'ad034', 'ad035', 'ad036', 'ad037', 'ad038', 'ad039', 'ad040', 'ad041', 'ad042', 'ad044', 'ad045', 'ad046', 'ad047', 'ad048', 'ad049', 'ad050', 'ad051', 'ad052', 'ad053', 'ad054']
PRIOR_IDS = []  # zero prior rows: batch-31 is fully fresh (no batch-31 row was adopted before)
PROBED_IDS = ["ad%03d" % i for i in range(1, 56)]
FILELESS_IDS = []
ADOPTED_TOTAL_NODES = 237596711
NEWLY_RESOLVED_S5 = [148458]  # == ad009's s5 index; the single update8 requirement resolved here
HOLDER_UNION_SIZE = 126
HOLDER_DISTRIBUTION_PIN = {1: 102, 2: 23, 51: 1}  # member_loss_counts distribution
EXPECTED_MEMBER_LOSS_COUNTS = {5804: 51, 8730: 2}
ALLOWED_TRANSITIONS = {"excluded": ["excluded"], "excluded_now": ["excluded_now"],
                       "free_now": ["free_now"], "unknown": ["unknown", "free_now"]}
STATUS_TRANSITIONS_PIN = {'excluded->excluded': 390,
 'excluded_now->excluded_now': 23,
 'free_now->free_now': 38,
 'unknown->unknown': 34498}
# closure-table pins (declared pre-run in the published declaration; machine-verified)
CLOSURE_COUNTS = (808, 808)
CLASS_5804_CLOSURE_PIN = ((38, 55), (4, 4))
CHANGED_UNKNOWN_CLOSURE_PIN = {8730: ((60, 56), (30, 54)),
                               8811: ((50, 55), (38, 54))}
STABLE_UNKNOWN_RANK_CHURN_COUNT = 54
CHURN_STABLE_STATUS_DIST = {'excluded_now': 4, 'unknown': 50}
CLOSURE_ENTERED_PIN = {}
CLOSURE_LEFT_PIN = {}
CLOSURE_ANCHORS_PIN = {1849: ((2, 1), (2, 1)),
                       16757: ((4, 29), (5, 29)),
                       23101: ((1, 1), (1, 1))}
# metrics pins (BASE -> scenario)
METRICS_PIN = {
    "excluded_now_classes": (23, 23),
    "free_now_classes": (38, 38),
    "unknown_classes": (34498, 34498),
    "update8_remaining_now": (31718, 31717),
    "update8_resolved_count": (141, 142),
    "update8_win_hit_groups": (0, 0),
    "update8_groups_free_now": (131, 131),
    "joint_greedy_unique_groups": (2119, 2119),
    "joint_greedy_union_size": (36903, 36854),
    "probe_worklist_total": (64765, 64711),
    "group_best_options_nonfree": (2119, 2119),
    "closure_classes_count": (808, 808),
}
JOINT_GREEDY_DELTA_EXPECTED = -49  # frozen greedy scheduler bookkeeping decrease; NOT a verdict
WORKLIST_DELTA_EXPECTED = -54
PRG_MOVERS_PIN = {'4': (5949, 5948), '5': (2940, 2938), '25': (5920, 5919),
                  '13': (6176, 6175), '38': (3118, 3068), '49': (2802, 2697)}
PRG_MOVER_DELTAS = {'4': -1, '5': -2, '13': -1, '25': -1, '38': -50, '49': -105}
# worklist serving-class deltas (base count -> scenario count), machine-observed:
SERVING_ROWS_PIN = {"5804": (55, 4), "8730": (56, 54), "8811": (55, 54)}
# the four unconsumed WIN keys keep their scheduling rows on both sides (NO verdict):
WIN_WORKLIST_PIN = {
    "ad024": {"base": {"5804": (1778, 55, 38, 59, 3), "8811": (2417, 55, 38, 58, 3)},
              "scenario": {"5804": (4, 4, 38, 59, 3), "8811": (1707, 54, 38, 58, 3)}},
    "ad028": {"base": {"5804": (1782, 55, 38, 59, 3)},
              "scenario": {"5804": (5, 4, 38, 59, 3)}},
    "ad043": {"base": {"5804": (1797, 55, 38, 59, 4)},
              "scenario": {"5804": (6, 4, 38, 59, 4)}},
    "ad055": {"base": {"5804": (1809, 55, 38, 59, 2)},
              "scenario": {"5804": (7, 4, 38, 59, 2)}},
}
# the four scenario serving rows of class 5804 are exactly the unconsumed WIN rows
SCEN_5804_ROWS_PIN = {"ad024": 4, "ad028": 5, "ad043": 6, "ad055": 7}
ADOPTED = {  # the 51 fresh LOSS rows adopted by Part DL (ad001..ad054 except the four WINs)
 'ad001': {'key': (6053400849273585664, 0),
           'legal': 92,
           'nodes': 5609720,
           's5': 97381},
 'ad002': {'key': (6052837899320164352, 128),
           'legal': 94,
           'nodes': 4555434,
           's5': 102238},
 'ad003': {'key': (6053400849139367937, 0),
           'legal': 96,
           'nodes': 5940995,
           's5': 119474},
 'ad004': {'key': (6053400849139367938, 0),
           'legal': 97,
           'nodes': 3434932,
           's5': 125125},
 'ad005': {'key': (6053400849139367940, 0),
           'legal': 94,
           'nodes': 3420177,
           's5': 130687},
 'ad006': {'key': (6053400849139367944, 0),
           'legal': 96,
           'nodes': 7296844,
           's5': 136105},
 'ad007': {'key': (6053400849139367952, 0),
           'legal': 100,
           'nodes': 7840993,
           's5': 141315},
 'ad008': {'key': (6053400849139367968, 0),
           'legal': 94,
           'nodes': 2362665,
           's5': 144458},
 'ad009': {'key': (6053400849139369984, 0),
           'legal': 100,
           'nodes': 2479959,
           's5': 148458},
 'ad010': {'key': (6053400849139372032, 0),
           'legal': 89,
           'nodes': 12273095,
           's5': 152721},
 'ad011': {'key': (6053400849139376128, 0),
           'legal': 94,
           'nodes': 2914995,
           's5': 156973},
 'ad012': {'key': (6053400849139384320, 0),
           'legal': 92,
           'nodes': 5968986,
           's5': 161166},
 'ad013': {'key': (6053400849139400704, 0),
           'legal': 97,
           'nodes': 5270933,
           's5': 165259},
 'ad014': {'key': (6053400849143562240, 0),
           'legal': 97,
           'nodes': 3337929,
           's5': 170887},
 'ad015': {'key': (6053400849147756544, 0),
           'legal': 96,
           'nodes': 4271124,
           's5': 174498},
 'ad016': {'key': (6053400849156145152, 0),
           'legal': 90,
           'nodes': 3479933,
           's5': 177679},
 'ad017': {'key': (6053400849172922368, 0),
           'legal': 89,
           'nodes': 2805657,
           's5': 180752},
 'ad018': {'key': (6053400849206476800, 0),
           'legal': 82,
           'nodes': 7948923,
           's5': 183816},
 'ad019': {'key': (6053400857729302528, 0),
           'legal': 100,
           'nodes': 6567285,
           's5': 186724},
 'ad020': {'key': (6053400866319237120, 0),
           'legal': 97,
           'nodes': 4663738,
           's5': 189532},
 'ad021': {'key': (6053400883499106304, 0),
           'legal': 95,
           'nodes': 4826218,
           's5': 192176},
 'ad022': {'key': (6053400917858844672, 0),
           'legal': 89,
           'nodes': 3183609,
           's5': 194523},
 'ad023': {'key': (6053400986578321408, 0),
           'legal': 96,
           'nodes': 2795664,
           's5': 196763},
 'ad025': {'key': (6053418441325412352, 0),
           'legal': 93,
           'nodes': 2750868,
           's5': 199913},
 'ad026': {'key': (6053436033511456768, 0),
           'legal': 99,
           'nodes': 3940244,
           's5': 201807},
 'ad027': {'key': (6053471217883545600, 0),
           'legal': 84,
           'nodes': 1624906,
           's5': 203738},
 'ad029': {'key': (6053400849139367936, 4),
           'legal': 100,
           'nodes': 2936438,
           's5': 211491},
 'ad030': {'key': (6052837907775881216, 128),
           'legal': 100,
           'nodes': 3146845,
           's5': 211529},
 'ad031': {'key': (6052837899190140928, 128),
           'legal': 98,
           'nodes': 5946707,
           's5': 211582},
 'ad032': {'key': (6052837899185948672, 128),
           'legal': 95,
           'nodes': 11268913,
           's5': 211655},
 'ad033': {'key': (6052837899185946625, 128),
           'legal': 99,
           'nodes': 5883887,
           's5': 211693},
 'ad034': {'key': (6053400849139367936, 8),
           'legal': 98,
           'nodes': 4885748,
           's5': 211744},
 'ad035': {'key': (6052837916365815808, 128),
           'legal': 90,
           'nodes': 3582819,
           's5': 211788},
 'ad036': {'key': (6052837899194335232, 128),
           'legal': 87,
           'nodes': 1675597,
           's5': 211830},
 'ad037': {'key': (6052837899185950720, 128),
           'legal': 94,
           'nodes': 5417573,
           's5': 211891},
 'ad038': {'key': (6052837899185946626, 128),
           'legal': 101,
           'nodes': 4503724,
           's5': 211921},
 'ad039': {'key': (6053400849139367936, 16),
           'legal': 92,
           'nodes': 4962308,
           's5': 211965},
 'ad040': {'key': (6052837933545684992, 128),
           'legal': 89,
           'nodes': 1723362,
           's5': 211996},
 'ad041': {'key': (6052837899202723840, 128),
           'legal': 84,
           'nodes': 2168706,
           's5': 212031},
 'ad042': {'key': (6052837899185954816, 128),
           'legal': 99,
           'nodes': 3179879,
           's5': 212087},
 'ad044': {'key': (6053400849139367936, 32),
           'legal': 91,
           'nodes': 2251201,
           's5': 212160},
 'ad045': {'key': (6052837967905423360, 128),
           'legal': 89,
           'nodes': 7781306,
           's5': 212175},
 'ad046': {'key': (6052837899185963008, 128),
           'legal': 92,
           'nodes': 3560629,
           's5': 212243},
 'ad047': {'key': (6052837899185946632, 128),
           'legal': 94,
           'nodes': 11064379,
           's5': 212273},
 'ad048': {'key': (6053400849139367936, 64),
           'legal': 86,
           'nodes': 10316369,
           's5': 212307},
 'ad049': {'key': (6052838036624900096, 128),
           'legal': 92,
           'nodes': 3146801,
           's5': 212340},
 'ad050': {'key': (6052837899253055488, 128),
           'legal': 91,
           'nodes': 1897590,
           's5': 212372},
 'ad051': {'key': (6052837899185979392, 128),
           'legal': 100,
           'nodes': 3580351,
           's5': 212404},
 'ad052': {'key': (6052837899185946640, 128),
           'legal': 101,
           'nodes': 5410550,
           's5': 212432},
 'ad053': {'key': (6052837899185946656, 128),
           'legal': 92,
           'nodes': 4094246,
           's5': 212464},
 'ad054': {'key': (6052838174063853568, 128),
           'legal': 86,
           'nodes': 1644957,
           's5': 212512},
}

MEMBERSHIP_EXPECT = {  # graph holder count == batch-keys membership_class_count
 'ad001': 3,
 'ad002': 3,
 'ad003': 4,
 'ad004': 4,
 'ad005': 4,
 'ad006': 4,
 'ad007': 4,
 'ad008': 3,
 'ad009': 4,
 'ad010': 4,
 'ad011': 4,
 'ad012': 4,
 'ad013': 4,
 'ad014': 4,
 'ad015': 4,
 'ad016': 4,
 'ad017': 4,
 'ad018': 4,
 'ad019': 4,
 'ad020': 4,
 'ad021': 4,
 'ad022': 4,
 'ad023': 4,
 'ad025': 4,
 'ad026': 4,
 'ad027': 4,
 'ad029': 4,
 'ad030': 4,
 'ad031': 4,
 'ad032': 4,
 'ad033': 4,
 'ad034': 4,
 'ad035': 4,
 'ad036': 4,
 'ad037': 4,
 'ad038': 4,
 'ad039': 4,
 'ad040': 4,
 'ad041': 4,
 'ad042': 4,
 'ad044': 4,
 'ad045': 4,
 'ad046': 4,
 'ad047': 4,
 'ad048': 4,
 'ad049': 4,
 'ad050': 4,
 'ad051': 4,
 'ad052': 4,
 'ad053': 3,
 'ad054': 3,
}

PINNED_PROBED = {  # (result, nodes) per probed key, from the two-pass raws / status log
 'ad001': (2, 5609720),
 'ad002': (2, 4555434),
 'ad003': (2, 5940995),
 'ad004': (2, 3434932),
 'ad005': (2, 3420177),
 'ad006': (2, 7296844),
 'ad007': (2, 7840993),
 'ad008': (2, 2362665),
 'ad009': (2, 2479959),
 'ad010': (2, 12273095),
 'ad011': (2, 2914995),
 'ad012': (2, 5968986),
 'ad013': (2, 5270933),
 'ad014': (2, 3337929),
 'ad015': (2, 4271124),
 'ad016': (2, 3479933),
 'ad017': (2, 2805657),
 'ad018': (2, 7948923),
 'ad019': (2, 6567285),
 'ad020': (2, 4663738),
 'ad021': (2, 4826218),
 'ad022': (2, 3183609),
 'ad023': (2, 2795664),
 'ad024': (1, 4360661),
 'ad025': (2, 2750868),
 'ad026': (2, 3940244),
 'ad027': (2, 1624906),
 'ad028': (1, 12803283),
 'ad029': (2, 2936438),
 'ad030': (2, 3146845),
 'ad031': (2, 5946707),
 'ad032': (2, 11268913),
 'ad033': (2, 5883887),
 'ad034': (2, 4885748),
 'ad035': (2, 3582819),
 'ad036': (2, 1675597),
 'ad037': (2, 5417573),
 'ad038': (2, 4503724),
 'ad039': (2, 4962308),
 'ad040': (2, 1723362),
 'ad041': (2, 2168706),
 'ad042': (2, 3179879),
 'ad043': (0, 15000000),
 'ad044': (2, 2251201),
 'ad045': (2, 7781306),
 'ad046': (2, 3560629),
 'ad047': (2, 11064379),
 'ad048': (2, 10316369),
 'ad049': (2, 3146801),
 'ad050': (2, 1897590),
 'ad051': (2, 3580351),
 'ad052': (2, 5410550),
 'ad053': (2, 4094246),
 'ad054': (2, 1644957),
 'ad055': (1, 3364655),
}

WIN_PINS = {  # the four unconsumed probe-level WIN rows (scrutiny owner lane)
 'ad024': {'key': (6053401124017274880, 0), 'legal': 86, 'nodes': 4360661, 's5': 198576,
           'membership': 3, 'decisive_budget': 15000000},
 'ad028': {'key': (6053682324116078592, 0), 'legal': 82, 'nodes': 12803283, 's5': 207094,
           'membership': 3, 'decisive_budget': 15000000},
 'ad043': {'key': (6052837899185946628, 128), 'legal': 87, 'nodes': 18247029, 's5': 212115,
           'membership': 4, 'decisive_budget': 30000000},
 'ad055': {'key': (6053400849139367936, 128), 'legal': 92, 'nodes': 3364655, 's5': 212536,
           'membership': 2, 'decisive_budget': 15000000},
}
WIN_S5 = [198576, 207094, 212115, 212536]

VAL_GATES = {
 'at2m-s5-1152921504606851072-536870946': {'input_csv': 'ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348',
           'published_baseline': '6e902ab147b117bb09216070f272969418247f5eb73870bf7705c8220fc9c35c',
           'b31_host': 'ff4dbb8344400c6cc629038e833110e4b5ada5bf24bfa70d07a525d159276a22',
           'd2_host': 'ff4dbb8344400c6cc629038e833110e4b5ada5bf24bfa70d07a525d159276a22',
           'tk_host': 'ff4dbb8344400c6cc629038e833110e4b5ada5bf24bfa70d07a525d159276a22',
           'di_host': 'ff4dbb8344400c6cc629038e833110e4b5ada5bf24bfa70d07a525d159276a22',
           'hi': 536870946, 'legal': 98, 'lo': 1152921504606851072},
 'at2m-s5-1188950301626860544-536870912': {'input_csv': '56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62',
           'published_baseline': 'eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24',
           'b31_host': 'eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24',
           'd2_host': 'eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24',
           'tk_host': '661a2842573f3a92df28bc4fdaf2feace2ae63717a73e140384c64039666b551',
           'di_host': 'eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24',
           'hi': 536870912, 'legal': 99, 'lo': 1188950301626860544},
 'first-15m-s5-1152921504606851072-536870946': {'input_csv': 'ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348',
           'published_baseline': '8035fe54f8c79dd44c4c80d6b38e4ad39d3d4660eaf57a32799969087b8a5591',
           'b31_host': '8035fe54f8c79dd44c4c80d6b38e4ad39d3d4660eaf57a32799969087b8a5591',
           'd2_host': '2e8c1dd59de4ed011684c877e2117dc992195015992647f1418370c1732ae21e',
           'tk_host': '2e8c1dd59de4ed011684c877e2117dc992195015992647f1418370c1732ae21e',
           'di_host': '8675ae4b4904485d5ffde72578342d69668a5c8bd39b82d93193177f515ebafb',
           'hi': 536870946, 'legal': 98, 'lo': 1152921504606851072},
 'second-15m-s5-1188950301626860544-536870912': {'input_csv': '56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62',
           'published_baseline': '91dffdec33a409bc3e5f6eb50c0ea95313574ef74d0692c5912a0814946de1fb',
           'b31_host': 'c3d1577d0663f62ad04c370d1194f25ca2359de229c9fc72bd883abb28268f5f',
           'd2_host': '9d2ebcf15cb8c05ce5cd4e52cf34068ad5e71056339f38017ac034d41645d6ce',
           'tk_host': '45cb1348c0a805ddff4b7d7a9db39cf56cd91f0669dae8f385f0ee7c33d2e4e2',
           'di_host': '45cb1348c0a805ddff4b7d7a9db39cf56cd91f0669dae8f385f0ee7c33d2e4e2',
           'hi': 536870912, 'legal': 99, 'lo': 1188950301626860544},
}
VAL_GATE_PATTERNS = {
    "at2m-s5-1152921504606851072-536870946": (2000000, 0, 2000000),
    "at2m-s5-1188950301626860544-536870912": (2000000, 0, 2000000),
    "first-15m-s5-1152921504606851072-536870946": (15000000, 2, 3651923),
    "second-15m-s5-1188950301626860544-536870912": (15000000, 2, 5040200),
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


def load_keys(batch_dir, class_index):
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


def parse_raw(path, tag, kid):
    txt = path.read_text()
    if "# replay_done" not in txt:
        fail(f"{kid} raw pass {tag} lacks the '# replay_done' completeness guard")
    rr = None
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
    return rr


def parse_valgate_out(path):
    txt = Path(path).read_text()
    if "# replay_done" not in txt:
        fail(f"val-gate out {path.name} lacks the '# replay_done' completeness guard")
    rr = None
    for line in txt.splitlines():
        if not line.startswith("replay,"):
            continue
        parts = line.split(",")
        row = (int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5]),
               int(parts[6]), int(parts[7]), int(parts[9]), int(parts[10]))
        if rr is not None:
            fail(f"val-gate out {path.name} has multiple replay rows")
        rr = row
    if rr is None:
        fail(f"val-gate out {path.name} has no replay row")
    return rr


def main():
    # --- sha pins ------------------------------------------------------------
    for name, p, want in (("increment", INCR_CACHE, INCR_SHA),
                          ("manifest", MANIFEST, MANIFEST_SHA),
                          ("scenario cache", SCEN_CACHE, SCEN_CACHE_SHA),
                          ("base cache", BASE_CACHE, BASE_CACHE_SHA),
                          ("base summary", BASE_DIR / "refresh-summary.json", BASE_SUMMARY_SHA),
                          ("scenario summary", SCEN_OUT / "refresh-summary.json", SCEN_SUMMARY_SHA),
                          ("base closure-classes", BASE_DIR / "closure-classes.csv", BASE_CLOSURE_SHA),
                          ("base per-root-coverage", BASE_DIR / "per-root-coverage.csv", BASE_PRC_SHA),
                          ("base probe-worklist", BASE_DIR / "probe-worklist.csv", BASE_WORKLIST_SHA),
                          ("scenario closure-classes", SCEN_OUT / "closure-classes.csv", SCEN_CLOSURE_SHA),
                          ("scenario per-root-coverage", SCEN_OUT / "per-root-coverage.csv", SCEN_PRC_SHA),
                          ("scenario probe-worklist", SCEN_OUT / "probe-worklist.csv", SCEN_WORKLIST_SHA),
                          ("batch-31 batch keys", KIT_DIR / "input/batch-keys.json", B31_KEYS_SHA),
                          ("batch-31 status log", KIT_DIR / "output/status.log", STATUS_LOG_SHA),
                          ("batch-31 kit manifest", KIT_DIR / "MANIFEST-sha256.txt", KIT_MANIFEST_SHA),
                          ("DI reprobe kit manifest", DI_DIR / "MANIFEST-sha256.txt", DI_MANIFEST_SHA),
                          ("DI status log", DI_DIR / "output/status.log", DI_STATUS_SHA),
                          ("DI ad043 30M raw p1", DI_DIR / "output/raw/ad043.p1.out", DI_AD043_P1_SHA),
                          ("DI ad043 30M raw p2", DI_DIR / "output/raw/ad043.p2.out", DI_AD043_P2_SHA),
                          ("DI exh15m clone p1", DI_DIR / "sources/exh15m/ad043.p1.out", DI_EXH15M_P1_SHA),
                          ("DI exh15m clone p2", DI_DIR / "sources/exh15m/ad043.p2.out", DI_EXH15M_P2_SHA),
                          ("DI anchor ad054 p1 raw", DI_DIR / "sources/anchor-15m/ad054.p1.out", DI_ANCHOR54_SHA),
                          ("DI anchor ad054 p2 raw", DI_DIR / "sources/anchor-15m/ad054.p2.out", DI_ANCHOR54_SHA),
                          ("DI anchor ad055 p1 raw", DI_DIR / "sources/anchor-15m/ad055.p1.out", DI_ANCHOR55_SHA),
                          ("DI anchor ad055 p2 raw", DI_DIR / "sources/anchor-15m/ad055.p2.out", DI_ANCHOR55_SHA),
                          ("DI b31 status clone", DI_DIR / "sources/b31-status.log", STATUS_LOG_SHA),
                          ("DI canonical-cache clone", DI_DIR / "sources/canonical-cache-db-merged-b29loss37.cache", BASE_CACHE_SHA),
                          ("merge-audit run1", EXP / "output/merge-audit-run1.json", MERGE_AUDIT_SHA),
                          ("merge-audit run2", EXP / "output/merge-audit-run2.json", MERGE_AUDIT_SHA),
                          ("merge-audit run3", EXP / "output/merge-audit-run3.json", MERGE_AUDIT_SHA)):
        got = sha(p)
        if got != want:
            fail(f"{name} sha256 drift: {got} != {want}")

    def verify_kit_dir(dirp, manifest_sha, kit_files):
        if sha(dirp / "MANIFEST-sha256.txt") != manifest_sha:
            fail(f"kit {dirp.name} MANIFEST sha drift")
        entries = []
        for line in (dirp / "MANIFEST-sha256.txt").read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(None, 1)
            if len(parts) != 2:
                fail(f"kit manifest line not '<sha256> <path>': {line}")
            entries.append((parts[0], parts[1]))
        if len(entries) != kit_files:
            fail(f"kit {dirp.name} manifest lists {len(entries)} files != {kit_files}")
        for want_sha, rel in entries:
            p = dirp / rel
            if not p.is_file():
                p = ROOT / rel  # published manifests record work-tree-relative paths
            if not p.is_file():
                fail(f"kit {dirp.name} file missing: {rel}")
            got = sha(p)
            if got != want_sha:
                fail(f"kit {dirp.name} file sha drift at {rel}: {got} != {want_sha}")
        return len(entries)

    kit_b31_files = verify_kit_dir(KIT_DIR, KIT_MANIFEST_SHA, KIT_FILES)
    kit_di_files = verify_kit_dir(DI_DIR, DI_MANIFEST_SHA, DI_KIT_FILES)
    if sha(KIT_DIR / "output/raw/ad043.p1.out") != DI_EXH15M_P1_SHA \
            or sha(KIT_DIR / "output/raw/ad043.p2.out") != DI_EXH15M_P2_SHA:
        fail("batch-31 ad043 15M exhaustion raws != the DI exh15m byte clones "
             "(supersede chain drift)")
    kit_info = {"manifest_sha256": KIT_MANIFEST_SHA, "files_verified": kit_b31_files}
    di_kit_info = {"manifest_sha256": DI_MANIFEST_SHA, "files_verified": kit_di_files}

    # --- status log gates -----------------------------------------------------
    import re
    log_lines = [l for l in (KIT_DIR / "output/status.log").read_text().splitlines() if l.strip()]
    if len(log_lines) != STATUS_LINES:
        fail(f"status log line count {len(log_lines)} != {STATUS_LINES}")
    pat = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z) (ad\d{3}) PASS (\d+),(\d+),(\d+)$")
    halt_pat = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z) (ad\d{3}) WIN-HALT$")
    exh_pat = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z) (ad\d{3}) EXHAUSTED (\d+),(\d+),(\d+)$")
    seen_ids, seen_ts, halt_rows, exh_rows = set(), [], [], []
    for line in log_lines:
        m = pat.match(line)
        if m is None:
            m2 = halt_pat.match(line)
            m3 = exh_pat.match(line)
            if m2 is not None:
                halt_rows.append((m2.group(2), m2.group(1)))
                continue
            if m3 is not None:
                exh_rows.append((m3.group(2), m3.group(1),
                                 (int(m3.group(3)), int(m3.group(4)), int(m3.group(5)))))
                continue
            fail(f"status log line not a strict verdict/halt/exhaustion row: {line!r}")
        if m.group(3) != str(BUDGET):
            fail(f"status log row not a 15M verdict row: {line!r}")
        kid = m.group(2)
        ts = m.group(1)
        rres = int(m.group(4))
        if rres not in (0, 1, 2):
            fail(f"status log row result {rres} invalid: {line!r}")
        if kid in seen_ids:
            fail(f"status log duplicate key row: {kid}")
        seen_ids.add(kid)
        seen_ts.append(ts)
        want_res, want_nodes = PINNED_PROBED[kid]
        if rres != want_res or int(m.group(5)) != want_nodes:
            fail(f"status log (result, nodes) for {kid} != the pinned raw row: {line!r}")
        if rres == 1 and kid not in WIN_IDS:
            fail(f"only the pinned WIN keys {WIN_IDS} may carry result 1: {line!r}")
        if rres == 0 and kid != EXHAUSTED_ID:
            fail(f"only the pinned superseded key {EXHAUSTED_ID} may carry result 0: {line!r}")
    if len(seen_ids) != 55:
        fail(f"status log PASS verdict rows {len(seen_ids)} != 55 (probe-complete batch)")
    if seen_ids != set(PROBED_IDS):
        fail("status log key-id set != the 55 probed keys")
    want_halts = [(l.split()[1], l.split()[0]) for l in WIN_HALT_LINES]
    if sorted(halt_rows) != sorted(want_halts):
        fail(f"status log WIN-HALT rows {halt_rows} != the three pinned rows {want_halts}")
    want_exh = [(EXHAUSTED_LINES[0].split()[1], EXHAUSTED_LINES[0].split()[0],
                 (15000000, 0, 15000000))]
    if exh_rows != want_exh:
        fail(f"status log EXHAUSTED rows {exh_rows} != the one pinned ad043 row {want_exh}")
    if log_lines[-1] != STATUS_FINAL_ROW:
        fail(f"status log final line {log_lines[-1]!r} != pinned {STATUS_FINAL_ROW!r}")
    if min(seen_ts) != STATUS_TS_MIN or max(seen_ts) != STATUS_TS_MAX:
        fail(f"status log timestamp window {min(seen_ts)}..{max(seen_ts)} != pinned")
    status_log_info = {
        "lines": len(log_lines), "pass_rows": len(seen_ids),
        "halt_rows": len(halt_rows), "exhausted_rows": len(exh_rows),
        "loss_rows": 51, "win_rows": 3, "superseded_exhausted_rows": 1,
        "final_line": STATUS_FINAL_ROW,
        "win_halt_rows": WIN_HALT_LINES,
        "exhausted_row": EXHAUSTED_LINES[0],
        "ts_window": [STATUS_TS_MIN, STATUS_TS_MAX],
        "note": STATUS_LOG_NOTE,
    }

    # --- manifest gates --------------------------------------------------------
    manifest = json.loads(MANIFEST.read_text())
    if sha(MANIFEST) != MANIFEST_SHA:
        fail("manifest file sha drift (double-read)")
    if manifest["schema"] != "b31loss51-increments-manifest-v1":
        fail(f"manifest schema drift: {manifest['schema']}")
    rc = manifest["row_counts"]
    if not (rc["adopted_loss_rows"] == 51 and rc["prior_adopted_loss_rows"] == 0
            and rc["wins"] == 4 and rc["exhausted_excluded"] == 0
            and rc["probed_rows"] == 55 and rc["fragments_unprobed"] == 0
            and rc["fileless_unprobed"] == 0):
        fail(f"manifest row_counts not the probe-complete 51-fresh-LOSS / 0-prior / "
             f"4-unconsumed-WIN / 0-excluded-EXHAUSTED picture: {rc}")
    if manifest["loss_ids"] != ADOPTED_IDS:
        fail(f"manifest loss id list drift: {manifest['loss_ids']}")
    if manifest["win_ids"] != WIN_IDS or manifest["unadopted_win_ids"] != WIN_IDS:
        fail("manifest WIN id lists must be exactly the four unconsumed keys")
    if manifest["exhausted_excluded_ids"] != []:
        fail("manifest excluded-EXHAUSTED id list must be empty (the ad043 15M "
             "exhaustion is superseded by the DI 30M WIN, not adopted, not excluded)")
    if sorted(manifest["resolved_ids"]) != sorted(ADOPTED_IDS):
        fail(f"manifest resolved_ids != the 51 adopted keys: {manifest['resolved_ids']}")
    if manifest["full_packet_eq_loss_only"] is not False or manifest["win_scenario_exists"] is not True:
        fail("manifest not-loss-only / WIN-scenario-exists flags not asserted")
    if manifest["sha256"]["loss"] != INCR_SHA:
        fail("manifest loss sha does not match the pinned increment")
    if manifest["merger_sha256"] != MERGER_SHA:
        fail("manifest merger pin drift (the pinned fail-closed union merger)")
    if (manifest["base_cache_sha256"] != BASE_CACHE_SHA
            or manifest["base_cache_rows"] != 6354
            or manifest["base_cache_absent_hits_for_emitted"] != 0
            or manifest["base_cache_prior_adoption_confirmed"] != 0
            or manifest["quarantine_hits"] != 0):
        fail("manifest BASE-cache bookkeeping drift (6,354 rows 04b0a239..., "
             "0 prior adoption confirmations (batch-31 fully fresh), no absent hits)")
    if manifest["exhausted_rows"] != []:
        fail("manifest exhausted row list must be empty (superseded, consumed nowhere)")
    want_win_rows = [{"key_id": kid, "result": 1, "nodes": WIN_PINS[kid]["nodes"],
                      "legal": WIN_PINS[kid]["legal"], "lo": WIN_PINS[kid]["key"][0],
                      "hi": WIN_PINS[kid]["key"][1], "s5_index": WIN_PINS[kid]["s5"],
                      "decisive_budget": WIN_PINS[kid]["decisive_budget"]}
                     for kid in WIN_IDS]
    if manifest["unadopted_win_rows"] != want_win_rows:
        fail(f"manifest unadopted WIN rows != the pinned four rows: {manifest['unadopted_win_rows']}")
    if len(manifest["batches"]) != 1:
        fail("manifest batches != exactly [batch-31]")
    mb = manifest["batches"][0]
    if (mb["batch"] != 31 or mb["class_index"] != B31_CLASS or mb["keys_total"] != 55):
        fail("manifest batch-31 identity drift")
    if (mb["adopted_loss_ids"] != ADOPTED_IDS or mb["already_adopted_ids"] != []
            or mb["unadopted_win_ids"] != WIN_IDS or mb["exhausted_excluded_ids"] != []
            or mb["fragment_ids"] != []):
        fail("manifest batch-31 adopted/prior/unadopted/fragment id lists drift "
             "(batch-31 is fully fresh: zero prior rows)")
    if mb["probed_ids"] != PROBED_IDS:
        fail("manifest batch-31 probed ids != all 55 keys")
    if (mb["fileless_unprobed_count"] != 0 or mb["fileless_unprobed_ids"] != []):
        fail("manifest batch-31 fileless bookkeeping must be empty (probe-complete)")
    if mb["input_sha256"] != B31_KEYS_SHA:
        fail("manifest batch-31 input sha drift")
    if (mb["status_log_sha256"] != STATUS_LOG_SHA or mb["status_log_lines"] != STATUS_LINES
            or mb["status_log_final_line"] != STATUS_FINAL_ROW
            or mb["status_log_win_halt_lines"] != WIN_HALT_LINES
            or mb["status_log_exhausted_lines"] != EXHAUSTED_LINES):
        fail("manifest batch-31 status-log bookkeeping drift")
    sup = mb["ad043_supersede"]
    if (sup["di_kit_manifest_sha256"] != DI_MANIFEST_SHA
            or sup["di_kit_files_verified"] != DI_KIT_FILES
            or sup["di_status_sha256"] != DI_STATUS_SHA
            or sup["di_ad043_p1_sha256"] != DI_AD043_P1_SHA
            or sup["di_ad043_p2_sha256"] != DI_AD043_P2_SHA
            or sup["di_b31_status_clone_sha256"] != STATUS_LOG_SHA
            or sup["di_base_cache_clone_sha256"] != BASE_CACHE_SHA
            or sup["superseded_15m_label"] != "EXHAUSTED (result 0, nodes 15,000,000)"
            or sup["resolution"] != ("Part DI 30M two-pass fresh-cold WIN (result 1, "
                                     "nodes 18,247,029, p1==p2 node-exact)")):
        fail("manifest ad043 supersede block drift")
    if (mb["kit_integrity"]["manifest_sha256"] != KIT_MANIFEST_SHA
            or mb["kit_integrity"]["files_verified"] != KIT_FILES):
        fail("manifest batch-31 kit integrity drift")
    if mb["val_gate_multi_host_node_exact"] is not True:
        fail("manifest val-gate multi-host node-exact flag not asserted")
    if (mb["total_nodes_pass_one"] != mb["total_nodes_pass_two"]
            or mb["total_nodes_pass_one"] != ADOPTED_TOTAL_NODES):
        fail(f"manifest batch-31 adopted-row node total drift ({ADOPTED_TOTAL_NODES} expected)")
    if mb["stop_rule"] != STOP_RULE:
        fail("manifest batch-31 stop rule drift")
    if mb["fragment_state"] != {}:
        fail("manifest batch-31 fragment_state must be empty (0 fragments)")

    # --- DI reprobe status gates ----------------------------------------------
    di_log = [l for l in (DI_DIR / "output/status.log").read_text().splitlines() if l.strip()]
    if len(di_log) != DI_STATUS_LINES:
        fail(f"DI status line count {len(di_log)} != {DI_STATUS_LINES}")
    if di_log != [
        "2026-11-24T07:12:24Z ad054 PASS 30000000,2,1644957",
        "2026-11-24T07:12:58Z ad055 PASS 30000000,1,3364655",
        "2026-11-24T07:12:58Z ad055 WIN-HALT",
        "2026-11-24T07:16:30Z ad043 PASS 30000000,1,18247029",
        "2026-11-24T07:16:30Z ad043 WIN-HALT",
    ][:DI_STATUS_LINES]:
        fail(f"DI status log rows {di_log} != the pinned five rows")
    if di_log[-1] != DI_STATUS_FINAL_LINE:
        fail("DI status final line drift")
    di_status_info = {"lines": len(di_log), "final_line": DI_STATUS_FINAL_LINE,
                      "ad043_reprobe": "PASS 30000000,1,18247029 + WIN-HALT",
                      "anchors": "ad054 (2, 1644957) / ad055 (1, 3364655) at 30M"}

    for pat_name, want in VAL_GATE_PATTERNS.items():
        g = VAL_GATES[pat_name]
        molecule = (g["lo"], g["hi"])
        if sha(KIT_DIR / f"val-gate/{pat_name}.input.csv") != g["input_csv"]:
            fail(f"val-gate {pat_name} input.csv sha drift")
        rows = {}
        for host, key in (("published-baseline", "published_baseline"),
                          ("b31-host", "b31_host"),
                          ("d2-host", "d2_host"),
                          ("tk-host", "tk_host"),
                          ("di-host", "di_host")):
            p = DI_DIR / f"val-gate/{pat_name}.{host}.out" if host == "di-host" \
                else KIT_DIR / f"val-gate/{pat_name}.{host}.out"
            if sha(p) != g[key]:
                fail(f"val-gate {pat_name} {host} sha drift")
            rows[host] = parse_valgate_out(p)
        base = rows["published-baseline"]
        for host in ("b31-host", "d2-host", "tk-host", "di-host"):
            if rows[host] != base:
                fail(f"val-gate {pat_name} {host} replay row {rows[host]} != published-baseline {base} "
                     "(six-host node-exact gate)")
        stones, legal, is_or, budget, result, nodes, klo, khi = base
        if (stones, is_or) != (5, 0) or (klo, khi) != molecule or legal != g["legal"]:
            fail(f"val-gate {pat_name} replay key/stones/and-or gate drift: {base}")
        if (budget, result, nodes) != want:
            fail(f"val-gate {pat_name} budget/result/nodes {want} gate drift: {base}")
    val_gate_info = {
        "patterns": {p: {"molecule": [g["lo"], g["hi"]], "legal": g["legal"],
                         "budget": VAL_GATE_PATTERNS[p][0], "result": VAL_GATE_PATTERNS[p][1],
                         "nodes": VAL_GATE_PATTERNS[p][2],
                         "input_csv_sha256": g["input_csv"],
                         "published_baseline_sha256": g["published_baseline"],
                         "b31_host_sha256": g["b31_host"],
                         "d2_host_sha256": g["d2_host"],
                         "tk_host_sha256": g["tk_host"],
                         "di_host_sha256": g["di_host"]} for p, g in VAL_GATES.items()},
        "multi_host_node_exact": "4/4 patterns: published-baseline == b31-host == "
                                 "d2-host == tk-host == di-host on the full replay row "
                                 "modulo wall time (20 file-pin checks + 4 DI-host files)",
    }

    # --- graph + update8 ------------------------------------------------------
    sys.path.insert(0, str(BOARD_SOURCE.parent))
    sys.path.insert(0, str(POLICY.parent))
    from independent import Board
    from s5_evidence_policy import quarantined_cache_keys, is_canonical_safe_s5_key

    quarantined = quarantined_cache_keys()
    board = Board(11)

    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        gph = json.load(stream)
    s4_masks, s4_status, s4_cost = gph["s4_masks"], gph["s4_status"], gph["s4_cost"]
    roots = gph["roots"]
    s5_masks = gph["s5_masks"]
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

    # --- batch keys against the pinned graph ----------------------------------
    bk, groups_served = load_keys(KIT_DIR, B31_CLASS)
    if [int(x) for x in bk["class_mask"]] != list(s4_masks[B31_CLASS]):
        fail("batch-keys class_mask != graph mask of class 5804")
    if len(bk["keys"]) != 55:
        fail(f"class 5804 batch-keys count {len(bk['keys'])} != 55")
    batch_keys = {}
    for k in bk["keys"]:
        kid = k["key_id"]
        lo, hi, s5i = int(k["lo"]), int(k["hi"]), int(k["s5_index"])
        if mask_to_index.get((lo, hi)) != s5i:
            fail(f"{kid} (lo,hi) does not map to its published s5 index {s5i}")
        if (lo, hi) in quarantined or not is_canonical_safe_s5_key((lo, hi)):
            fail(f"{kid} noncanonical or quarantined key")
        batch_keys[kid] = (lo, hi, s5i, int(k["membership_class_count"]), int(k["legal"]))
    if len(set(v[2] for v in batch_keys.values())) != len(batch_keys):
        fail("batch keys collide on s5 indices")
    for kid, (lo, hi, s5i, _m, _lg) in batch_keys.items():
        if s5i in receipt_verdicts:
            fail(f"{kid} already resolved by the update8 receipt")
    for pat_name, g in VAL_GATES.items():
        molecule = (g["lo"], g["hi"])
        if molecule in batch_keys or molecule in quarantined \
                or not is_canonical_safe_s5_key(molecule):
            fail(f"val-gate molecule {pat_name} must be canonical-safe and disjoint from the batch")

    # --- independent two-pass raw re-verification of all 55 probed keys -------
    adopted_nodes_sum = 0
    for kid, (lo, hi, s5i, _m, bk_legal) in sorted(batch_keys.items()):
        rows_raw = []
        for tag in ("p1", "p2"):
            rows_raw.append(parse_raw(KIT_DIR / f"output/raw/{kid}.{tag}.out", tag, kid))
        p1, p2 = rows_raw
        if p1 != p2:
            fail(f"{kid} two-pass mismatch (node-exact gate): {p1} vs {p2}")
        stones, legal, is_or, budget, result, nodes, klo, khi = p1
        if stones != 5 or is_or != 0 or budget != BUDGET:
            fail(f"{kid} raw depth/budget drift: {p1}")
        if (klo, khi) != (lo, hi) or legal != bk_legal:
            fail(f"{kid} raw key/legal != batch-keys")
        want_res, want_nodes = PINNED_PROBED[kid]
        if result != want_res or nodes != want_nodes:
            fail(f"{kid} raw record != the pinned (result, nodes) row: {p1}")
        if kid == EXHAUSTED_ID:
            # the batch-31 raw is the SUPERSEDED 15M exhaustion (result 0, full
            # budget); the WIN row is the DI 30M reprobe, gated further below
            if result != 0 or nodes != BUDGET:
                fail(f"{kid} raw must be the pinned superseded 15M exhaustion row: {p1}")
            continue
        if kid in WIN_IDS:
            wp = WIN_PINS[kid]
            if result != 1:
                fail(f"{kid} must be a probe-level WIN row: {p1}")
            if (klo, khi) != wp["key"] or legal != wp["legal"] or s5i != wp["s5"] \
                    or nodes != wp["nodes"]:
                fail(f"{kid} raw row != the pinned unconsumed WIN pin: {p1}")
            continue
        if result != 2:
            fail(f"{kid} not a WIN/exhausted key but raw result != 2 (LOSS): {p1}")
        a = ADOPTED[kid]
        if legal != a["legal"] or s5i != a["s5"] or (lo, hi) != tuple(a["key"]):
            fail(f"{kid} raw legal/key/s5 != the published adopted LOSS row: {p1}")
        adopted_nodes_sum += nodes
    if adopted_nodes_sum != ADOPTED_TOTAL_NODES:
        fail(f"adopted raw node sum {adopted_nodes_sum} != pinned total {ADOPTED_TOTAL_NODES}")
    # raw inventory gate: exactly the 110 probed raw files
    raw_dir = KIT_DIR / "output/raw"
    raws = sorted(p.name for p in raw_dir.iterdir() if p.is_file())
    expected_raws = sorted(f"{kid}.{tag}.out" for kid in PROBED_IDS for tag in ("p1", "p2"))
    if raws != expected_raws:
        fail(f"raw inventory drift: {len(raws)} files, expected exactly the 110 probed files")

    # --- DI ad043 30M reprobe gates (supersede chain) --------------------------
    dp1 = parse_raw(DI_DIR / "output/raw/ad043.p1.out", "p1", "ad043-di30m")
    dp2 = parse_raw(DI_DIR / "output/raw/ad043.p2.out", "p2", "ad043-di30m")
    if dp1 != dp2:
        fail(f"ad043 DI 30M two-pass mismatch: {dp1} vs {dp2}")
    lo43, hi43, s5i43, _m43, bk_legal43 = batch_keys["ad043"]
    stones, legal, is_or, dbudget, dresult, dnodes, dklo, dkhi = dp1
    if (stones, is_or, dbudget) != (5, 0, REPROBE_BUDGET):
        fail(f"ad043 DI raw not a 30M five-stone row: {dp1}")
    if (dklo, dkhi) != (lo43, hi43) or legal != bk_legal43:
        fail("ad043 DI raw key/legal != batch-keys")
    if (dresult, dnodes) != (1, WIN_PINS["ad043"]["nodes"]):
        fail(f"ad043 DI 30M WIN row != the pinned (1, 18247029): {dp1}")
    if sha(DI_DIR / "sources/exh15m/ad043.p1.out") != DI_EXH15M_P1_SHA \
            or sha(DI_DIR / "sources/exh15m/ad043.p2.out") != DI_EXH15M_P2_SHA:
        fail("DI exh15m clone sha drift")
    if (DI_DIR / "sources/exh15m/ad043.p1.out").read_bytes() != (KIT_DIR / "output/raw/ad043.p1.out").read_bytes() \
            or (DI_DIR / "sources/exh15m/ad043.p2.out").read_bytes() != (KIT_DIR / "output/raw/ad043.p2.out").read_bytes():
        fail("DI exh15m clones not byte-equal to the batch-31 ad043 15M exhaustion raws")
    # anchors: the DI kit carries byte clones of the batch-31 15M raws and
    # re-derived the same (result, nodes) at 30M (budget independence)
    for akid, apk in (("ad054", DI_ANCHOR54_SHA), ("ad055", DI_ANCHOR55_SHA)):
        c1 = (DI_DIR / f"sources/anchor-15m/{akid}.p1.out").read_bytes()
        c2 = (DI_DIR / f"sources/anchor-15m/{akid}.p2.out").read_bytes()
        if c1 != c2:
            fail(f"{akid} DI 15M anchor-clone files differ")
        if sha(DI_DIR / f"sources/anchor-15m/{akid}.p1.out") != apk \
                or sha(DI_DIR / f"sources/anchor-15m/{akid}.p2.out") != apk:
            fail(f"{akid} DI 15M anchor-clone sha drift")
        if c1 != (KIT_DIR / f"output/raw/{akid}.p1.out").read_bytes() \
                or c2 != (KIT_DIR / f"output/raw/{akid}.p2.out").read_bytes():
            fail(f"{akid} DI 15M anchor clones not byte-equal to the batch-31 raws")
        a1 = parse_raw(DI_DIR / f"output/raw/{akid}.p1.out", "p1", akid + "-di30m")
        a2 = parse_raw(DI_DIR / f"output/raw/{akid}.p2.out", "p2", akid + "-di30m")
        if a1 != a2:
            fail(f"{akid} DI 30M anchor two-pass mismatch: {a1} vs {a2}")
        b1 = parse_raw(KIT_DIR / f"output/raw/{akid}.p1.out", "p1", akid)
        stones, legal, is_or, abud, ares, anodes, alo, ahi = a1
        _bs, _bl, _io, kbud, kres, knodes, _kl, _kh = b1
        if abud != REPROBE_BUDGET:
            fail(f"{akid} DI 30M anchor raw not a 30M row: {a1}")
        if (ares, anodes) != (kres, knodes) or (ares, anodes) != (kres, knodes):
            fail(f"{akid} DI 30M anchor row not budget-independent node-exact vs 15M: {a1} vs {b1}")
        if (alo, ahi) != batch_keys[akid][:2] or legal != batch_keys[akid][4]:
            fail(f"{akid} DI 30M anchor raw identity drift vs batch-keys")
    di_raws = sorted(p.name for p in (DI_DIR / "output/raw").iterdir() if p.is_file())
    if di_raws != sorted(f"{k}.{t}.out" for k in ("ad043", "ad054", "ad055") for t in ("p1", "p2")):
        fail(f"DI raw inventory drift: {di_raws}")
    di_reprobe_info = {
        "ad043_30m": {"result": 1, "nodes": WIN_PINS["ad043"]["nodes"],
                      "two_pass_node_exact": True, "supersedes": "15M EXHAUSTED (0, 15000000)"},
        "exh15m_clones_byte_equal_batch31": True,
        "anchors_budget_independent": ["ad054 (2, 1644957)", "ad055 (1, 3364655)"],
    }

    # --- increment gates -----------------------------------------------------
    incr = read_cache(INCR_CACHE)
    if len(incr) != ADOPTED_ROWS:
        fail(f"increment row count {len(incr)} != {ADOPTED_ROWS}")
    if any(v[0] != 2 for v in incr.values()):
        fail("increment contains a non-LOSS verdict")
    if set(incr) != {tuple(ADOPTED[k]["key"]) for k in ADOPTED_IDS}:
        fail("increment keys != exactly the 51 adopted LOSS keys")
    for kid in ADOPTED_IDS:
        a = ADOPTED[kid]
        row = incr.get(tuple(a["key"]))
        if row is None or row != (2, a["nodes"]):
            fail(f"increment row for {kid} != the adopted verdict: {row}")
    for kid in WIN_IDS:
        if tuple(batch_keys[kid][:2]) in incr:
            fail(f"{kid} leaked into the increment (the WIN rows are consumed nowhere)")

    base_cache = read_cache(BASE_CACHE)
    scen_cache = read_cache(SCEN_CACHE)
    for kid in ADOPTED_IDS:
        lo, hi, _s5i, _m, _lg = batch_keys[kid]
        if (lo, hi) in base_cache:
            fail(f"{kid} already present in the BASE cache (not a fresh increment)")
        if tuple(ADOPTED[kid]["key"]) != (lo, hi):
            fail(f"adopted row pin key for {kid} != batch-keys")
    if PRIOR_IDS:
        fail("PRIOR_IDS must be empty in this fully-fresh batch-31 adoption")
    base_kids = set()
    for kid in WIN_IDS:
        wk_lo, wk_hi = WIN_PINS[kid]["key"]
        if (wk_lo, wk_hi) in base_cache:
            fail(f"the unconsumed WIN key {kid} is present in the BASE cache (consumed nowhere)")
        base_kids.add((wk_lo, wk_hi))
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
    if base_votes.get(1, 0) != 158 or base_votes.get(2, 0) != 6196:
        fail(f"BASE cache verdict counts not 158 WIN / 6196 LOSS: {dict(sorted(base_votes.items()))}")
    if scen_votes.get(1, 0) != 158 or scen_votes.get(2, 0) != 6247:
        fail(f"scenario cache verdict counts not 158 WIN / 6247 LOSS: {dict(sorted(scen_votes.items()))}")
    for kid in WIN_IDS:
        wk_lo, wk_hi = WIN_PINS[kid]["key"]
        if (wk_lo, wk_hi) in scen_cache:
            fail(f"the unconsumed WIN key {kid} reached the scenario canonical cache "
                 "(the WIN verdict is consumed NOWHERE)")

    # --- graph holders of the adopted keys -----------------------------------
    holders = {}
    for kid in ADOPTED_IDS:
        lo, hi, s5i, mcnt, _lg = batch_keys[kid]
        hs = sorted(i for i, c in enumerate(s4_cost) if s5i in c)
        if B31_CLASS not in hs:
            fail(f"{kid} own batch class {B31_CLASS} not among its graph holders {hs}")
        if len(hs) != mcnt or mcnt != MEMBERSHIP_EXPECT[kid]:
            fail(f"{kid} graph holder count {len(hs)} != batch-keys membership "
                 f"{mcnt} != pinned {MEMBERSHIP_EXPECT[kid]}")
        for i in hs:
            if s4_status[i] not in (-1, 0, 1):
                fail(f"{kid} holder {i} unexpected graph status {s4_status[i]}")
        holders[kid] = hs
    holder_union = sorted(set().union(*[set(h) for h in holders.values()]))
    if len(holder_union) != HOLDER_UNION_SIZE:
        fail(f"holder union {len(holder_union)} != pinned {HOLDER_UNION_SIZE}")
    member_loss_counts = Counter()
    for hs in holders.values():
        for i in hs:
            member_loss_counts[i] += 1
    dist = dict(sorted(Counter(member_loss_counts.values()).items()))
    if dist != HOLDER_DISTRIBUTION_PIN:
        fail(f"member-loss distribution {dist} != pinned {HOLDER_DISTRIBUTION_PIN}")
    for c, want_cnt in EXPECTED_MEMBER_LOSS_COUNTS.items():
        if member_loss_counts[c] != want_cnt:
            fail(f"member loss count for {c} != pinned {want_cnt}")
    incr_index = {}
    for kid in ADOPTED_IDS:
        incr_index[ADOPTED[kid]["s5"]] = tuple(ADOPTED[kid]["key"])
    adopted_s5_set = set(incr_index)
    req_inter = adopted_s5_set & set(update8["required_new_s5"])
    if req_inter != set(NEWLY_RESOLVED_S5):
        fail(f"adopted s5 ∩ update8 requirement {sorted(req_inter)} != the declared "
             f"exactly-one set {NEWLY_RESOLVED_S5} (== ad009's s5 148458)")
    if ADOPTED["ad009"]["s5"] != NEWLY_RESOLVED_S5[0]:
        fail("the pinned newly-resolved s5 index is not ad009's published index")
    # the unconsumed WIN s5 indices must not be in the increment either
    for kid in WIN_IDS:
        if WIN_PINS[kid]["s5"] in incr_index:
            fail(f"the unconsumed WIN s5 of {kid} leaked into the increment index")

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
    if base_summary["inputs"]["cache_rows"] != 6354 or scen_summary["inputs"]["cache_rows"] != 6405:
        fail("published cache_rows not 6354 -> 6405")

    # --- global status-transition gate ----------------------------------------
    transitions = Counter()
    for i in range(len(s4_masks)):
        b, s = base_st[i], scen_st[i]
        transitions[f"{b}->{s}"] += 1
        if s not in ALLOWED_TRANSITIONS.get(b, []):
            fail(f"class {i} forbidden transition {b} -> {s}")
    if dict(sorted(transitions.items())) != STATUS_TRANSITIONS_PIN:
        fail(f"status transitions {dict(sorted(transitions.items()))} != pinned {STATUS_TRANSITIONS_PIN}")

    # --- excluded_now flips must be empty for a zero-WIN-consumed increment ---
    base_excluded_now = {i for i, s in base_st.items() if s == "excluded_now"}
    flips = sorted(i for i, s in scen_st.items()
                   if s == "excluded_now" and i not in base_excluded_now)
    if flips:
        fail(f"excluded_now flips {flips} must be EMPTY for a zero-WIN-consumed "
             "adoption (the probe-level WINs ad024/ad028/ad043/ad055 are consumed "
             "nowhere)")
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
    cls = B31_CLASS
    if cls in new_free:
        fail(f"class {cls} must NOT free: its four unconsumed WIN children remain "
             "verdict-unconsumed, so the class stays unknown")
    if scen_st[cls] != "unknown":
        fail(f"class {cls} scenario status {scen_st[cls]} != unknown (the four "
             "unconsumed WIN children remain; the class is NOT freed and NOT excluded)")
    basec = sorted(base_unknown[cls])
    if len(basec) != 55:
        fail(f"class {cls} BASE-unknown cost children {len(basec)} != 55 (zero prior adoption; "
             "the whole batch is fresh)")
    own_class_incr = sorted(j for j in incr_index if j in s4_cost[cls])
    if not set(own_class_incr) <= set(basec):
        fail(f"class {cls}: increment s5 indices not all BASE-unknown cost children of the class")
    if len(own_class_incr) != 51:
        fail(f"class {cls}: own increment membership {len(own_class_incr)} != 51")
    leftover = sorted(set(basec) - set(own_class_incr))
    if leftover != sorted(WIN_S5):
        fail(f"class {cls} leftover BASE-unknown children {leftover} != exactly the four "
             f"unconsumed WIN s5 {sorted(WIN_S5)}")
    if sorted(scen_unknown[cls]) != leftover:
        fail(f"class {cls} scenario-unknown children != leftover arithmetic")
    batch_s5 = {v[2] for v in batch_keys.values()}
    win_s5 = {WIN_PINS[k]["s5"] for k in WIN_IDS}
    if set(basec) != batch_s5:
        fail(f"class {cls}: BASE-unknown cost children != the 55 batch s5 (zero prior rows)")
    if not win_s5 <= batch_s5:
        fail("the unconsumed WIN s5 must be a subset of the batch s5 set")
    if set(own_class_incr) & win_s5:
        fail("an unconsumed WIN s5 leaked into the fresh increment")
    class_rows = {str(cls): {
        "class_index": cls, "batch": 31,
        "base_unknown_children": len(base_unknown[cls]),
        "adopted_by_increment": len(own_class_incr),
        "leftover_unknown_children": len(leftover),
        "scenario_unknown_children": len(scen_unknown[cls]),
        "scenario_status": scen_st[cls],
        "leftover_is_exactly_the_unconsumed_wins": True,
    }}

    # --- holder-class table with own-membership arithmetic gate ---------------
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
        if c == cls and len(own) != 51:
            fail(f"holder class {cls} must hold exactly the 51 adopted memberships")
        holder_rows[str(c)] = row

    # --- published metric table and pinned deltas -----------------------------
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
    for k, (want_base, want_scen) in METRICS_PIN.items():
        if metrics[k]["base"] != want_base or metrics[k]["scenario"] != want_scen:
            fail(f"metric {k} {metrics[k]['base']}->{metrics[k]['scenario']} != "
                 f"declared pin {want_base}->{want_scen}")
    if metrics["free_now_classes"]["delta"] != 0:
        fail("free_now class count must not change in a non-closing adoption")
    if metrics["update8_resolved_count"]["delta"] != 1:
        fail("update8 resolved-count delta != +1 (declared machine-observed: exactly "
             "one adopted key, s5 148458 == ad009, is an update8 baseline requirement)")
    if metrics["update8_remaining_now"]["delta"] != -1:
        fail("update8 remaining delta != -1")
    if metrics["probe_worklist_total"]["delta"] != WORKLIST_DELTA_EXPECTED:
        fail(f"probe worklist delta != {WORKLIST_DELTA_EXPECTED} (declared machine-observed)")
    if metrics["joint_greedy_union_size"]["delta"] != JOINT_GREEDY_DELTA_EXPECTED:
        fail(f"joint greedy union delta != {JOINT_GREEDY_DELTA_EXPECTED} (declared "
             "machine-observed bookkeeping decrease; per-root free/uncovered thirds "
             "are unchanged everywhere; NOT a coverage claim)")
    if metrics["closure_classes_count"]["delta"] != 0:
        fail("closure classes count delta != 0")
    for k in ("update8_win_hit_groups", "update8_groups_free_now",
              "joint_greedy_unique_groups", "group_best_options_nonfree"):
        if metrics[k]["delta"] != 0:
            fail(f"metric {k} must stay unchanged for a zero-WIN-consumed adoption")

    # --- update8 resolved-requirement delta, gated to the increment ----------
    base_resolved = set(base_summary["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    scen_resolved = set(scen_summary["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    lost = sorted(base_resolved - scen_resolved)
    if lost:
        fail(f"update8 resolutions lost: {lost}")
    newly_resolved = sorted(scen_resolved - base_resolved)
    if newly_resolved != NEWLY_RESOLVED_S5:
        fail(f"newly resolved s5 {newly_resolved} != the pinned {NEWLY_RESOLVED_S5} "
             "(exactly one adopted key resolves an update8 requirement)")
    if ADOPTED["ad009"]["s5"] != newly_resolved[0] \
            or incr_index[newly_resolved[0]] != tuple(ADOPTED["ad009"]["key"]):
        fail("the newly-resolved update8 requirement must be exactly ad009's increment row")
    # --- per-root coverage recompute + published csv gates --------------------
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

    for name, pub in published.items():
        r0 = pub["roots"][0]
        if (r0["role"], r0["origin_first"], r0["thirds"], r0["free_thirds_now"], r0["uncovered"]) \
                != ("known-loss-baseline", 27, 119, 119, 0):
            fail(f"{name}: roots[0] not the 119/119 known-loss baseline: {r0}")
    for prc in (base_prc, scen_prc):
        if prc[("known-loss-baseline", 27)][:3] != (119, 119, 0):
            fail("baseline per-root row not 119/119")

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
        }
    # individual greedy union movers: exactly the 5 pinned roots with pinned values
    ig_movers_by_first = {}
    for key, row in greedy_moved_rows.items():
        first = key.split("|")[1]
        ig_movers_by_first[first] = (row["base"], row["scenario"])
    if ig_movers_by_first != PRG_MOVERS_PIN:
        fail(f"individual greedy union movers {ig_movers_by_first} != pinned "
             f"{PRG_MOVERS_PIN} (per-root coverage free/uncovered must be unchanged)")
    if changed_rows:
        fail(f"per-root free coverage changed despite no newly free class: {changed_rows}")

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
        if row["delta"] != 0 and first not in PRG_MOVERS_PIN:
            fail(f"per-root greedy mover root {first} not in the declared mover set")
        if first in PRG_MOVERS_PIN:
            if (row["base_greedy_union_size"], row["scenario_greedy_union_size"]) != PRG_MOVERS_PIN[first]:
                fail(f"per-root greedy values for root {first} {row} != declared pin")
            if row["delta"] != PRG_MOVER_DELTAS[first]:
                fail(f"per-root greedy delta for root {first} != declared {PRG_MOVER_DELTAS[first]}")
            if row["base_free_thirds"] != row["scenario_free_thirds"] \
                    or row["base_uncovered_thirds"] != row["scenario_uncovered_thirds"]:
                fail(f"per-root greedy free/uncovered thirds changed for root {first} "
                     "(no class freed; the +101 on root 14 is plan-size bookkeeping, "
                     "NOT a coverage change)")
        elif row["delta"] != 0:
            fail(f"per-root greedy delta for non-mover root {first} != 0: {row}")
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
    if roots_summary_moved:
        fail(f"roots summary moved despite no newly free class: {roots_summary_moved}")

    # --- probe worklist gates --------------------------------------------------
    def load_worklist(path):
        with Path(path).open() as fh:
            return list(csv.DictReader(fh))

    base_wl = load_worklist(BASE_DIR / "probe-worklist.csv")
    scen_wl = load_worklist(SCEN_OUT / "probe-worklist.csv")
    if len(base_wl) != metrics["probe_worklist_total"]["base"] \
            or len(scen_wl) != metrics["probe_worklist_total"]["scenario"]:
        fail("worklist row counts != published metrics")
    base_cls_rows = [r for r in base_wl if r["serving_class"] == str(B31_CLASS)]
    scen_cls_rows = [r for r in scen_wl if r["serving_class"] == str(B31_CLASS)]
    if len(base_cls_rows) != 55 or len(scen_cls_rows) != 4:
        fail(f"class {B31_CLASS} serving rows {len(base_cls_rows)}->{len(scen_cls_rows)} "
             f"!= 55->4 (zero prior rows; the batch is fully fresh)")
    adopted_lohi = {tuple(ADOPTED[k]["key"]) for k in ADOPTED_IDS}
    for r in scen_wl:
        if (int(r["lo"]), int(r["hi"])) in adopted_lohi:
            fail(f"adopted key still in the scenario worklist at s5 {r['s5_index']}")
    # the four scenario serving rows of class 5804 are exactly the unconsumed WIN keys
    win_by_key = {WIN_PINS[kid]["key"]: kid for kid in WIN_IDS}
    scen_seen = set()
    for r in scen_cls_rows:
        kid = win_by_key.get((int(r["lo"]), int(r["hi"])))
        if kid is None or int(r["s5_index"]) != WIN_PINS[kid]["s5"] \
                or int(r["legal"]) != WIN_PINS[kid]["legal"]:
            fail(f"a class {B31_CLASS} scenario serving row is not one of the pinned "
                 f"WIN rows: {r}")
        if int(r["class_unknown_now"]) != 4 or int(r["closure_first"]) != 38 \
                or int(r["closure_third"]) != 59 \
                or int(r["membership_class_count"]) != WIN_PINS[kid]["membership"]:
            fail(f"class {B31_CLASS} scenario WIN row field drift for {kid}: {r}")
        if kid in scen_seen or int(r["probe_order"]) != SCEN_5804_ROWS_PIN[kid]:
            fail(f"class {B31_CLASS} scenario WIN row probe-order drift for {kid}: {r}")
        scen_seen.add(kid)
    if scen_seen != set(WIN_IDS):
        fail(f"class {B31_CLASS} scenario serving rows {sorted(scen_seen)} != all four "
             f"unconsumed WIN keys {sorted(WIN_IDS)}")
    # the four WIN keys keep their full scheduling rows on both sides (NO verdict)
    for kid in WIN_IDS:
        lo_w, hi_w = str(WIN_PINS[kid]["key"][0]), str(WIN_PINS[kid]["key"][1])
        win_base_rows = {r["serving_class"]: (int(r["probe_order"]), int(r["class_unknown_now"]),
                                              int(r["closure_first"]), int(r["closure_third"]),
                                              int(r["membership_class_count"]))
                         for r in base_wl if r["lo"] == lo_w and r["hi"] == hi_w}
        win_scen_rows = {r["serving_class"]: (int(r["probe_order"]), int(r["class_unknown_now"]),
                                              int(r["closure_first"]), int(r["closure_third"]),
                                              int(r["membership_class_count"]))
                         for r in scen_wl if r["lo"] == lo_w and r["hi"] == hi_w}
        if win_base_rows != WIN_WORKLIST_PIN[kid]["base"]:
            fail(f"{kid} BASE worklist rows != pinned: {win_base_rows}")
        if win_scen_rows != WIN_WORKLIST_PIN[kid]["scenario"]:
            fail(f"{kid} scenario worklist rows != pinned: {win_scen_rows}")
    # serving-class deltas pinned (net -54; honest machine-observed bookkeeping)
    base_serving = Counter(r["serving_class"] for r in base_wl)
    scen_serving = Counter(r["serving_class"] for r in scen_wl)
    serving_deltas = {c: (base_serving.get(c, 0), scen_serving.get(c, 0))
                      for c in set(base_serving) | set(scen_serving)
                      if base_serving.get(c, 0) != scen_serving.get(c, 0)}
    if serving_deltas != SERVING_ROWS_PIN:
        fail(f"serving-class deltas {serving_deltas} != pinned {SERVING_ROWS_PIN}")
    net = len(scen_wl) - len(base_wl)
    if net != WORKLIST_DELTA_EXPECTED:
        fail(f"worklist net delta {net} != {WORKLIST_DELTA_EXPECTED}")
    base_cls_s5 = sorted(int(r["s5_index"]) for r in base_cls_rows)
    if base_cls_s5 != sorted(batch_s5):
        fail(f"the 55 BASE serving rows of class {B31_CLASS} != the s5 of the batch "
             f"(fully fresh: zero prior means all 55 keys serve the class)")
    worklist_info = {
        "base_total": len(base_wl), "scenario_total": len(scen_wl),
        "class_5804_serving_rows": [len(base_cls_rows), len(scen_cls_rows)],
        "adopted_keys_absent_from_scenario_worklist": True,
        "win_rows": WIN_WORKLIST_PIN,
        "win_probe_orders": SCEN_5804_ROWS_PIN,
        "serving_class_deltas": SERVING_ROWS_PIN,
        "note": ("ad024 keeps 2 scheduling rows (serving classes 5804 and 8811), "
                 "ad028/ad043/ad055 keep 1 (serving class 5804) on both sides: "
                 "schedule bookkeeping only, the four WIN verdicts are consumed "
                 "NOWHERE"),
    }

    # --- closure-candidate table observations ---------------------------------
    def load_closure(path):
        with Path(path).open() as fh:
            return list(csv.DictReader(fh))

    base_cc = load_closure(BASE_DIR / "closure-classes.csv")
    scen_cc = load_closure(SCEN_OUT / "closure-classes.csv")
    closure_rows = {
        "scenario_first_row": scen_cc[0] if scen_cc else None,
        "counts": {"base": len(base_cc), "scenario": len(scen_cc)},
        "classes": {},
        "changed_unknown": {},
        "stable_unknown_rank_churn": {
            "count": STABLE_UNKNOWN_RANK_CHURN_COUNT,
            "status_distribution": dict(sorted(CHURN_STABLE_STATUS_DIST.items())),
            "gate": ("every churned class with stable unknown_now is pure ranking "
                     "bookkeeping: recomputed status UNCHANGED between BASE and "
                     f"scenario ({CHURN_STABLE_STATUS_DIST}), none of them a "
                     "holder of the adopted keys"),
        },
        "anchors": {},
    }
    if (len(base_cc), len(scen_cc)) != CLOSURE_COUNTS:
        fail(f"closure table counts {(len(base_cc), len(scen_cc))} != pinned {CLOSURE_COUNTS}")
    b_full = {int(r["class_index"]): r for r in base_cc}
    s_full = {int(r["class_index"]): r for r in scen_cc}
    base_idx = set(b_full)
    scen_idx = set(s_full)

    # class 5804: unknown_now 55 -> 4 (rank 38 -> 4)
    cls_row_pin = CLASS_5804_CLOSURE_PIN
    if int(b_full[cls]["unknown_now"]) != cls_row_pin[0][1] or int(b_full[cls]["class_rank"]) != cls_row_pin[0][0]:
        fail(f"BASE closure row for class {cls} unexpected: {b_full[cls]}")
    if int(s_full[cls]["unknown_now"]) != cls_row_pin[1][1] or int(s_full[cls]["class_rank"]) != cls_row_pin[1][0]:
        fail(f"scenario closure row for class {cls} unexpected: {s_full[cls]}")
    closure_rows["classes"][str(cls)] = {
        "base_rank": cls_row_pin[0][0], "base_unknown_now": cls_row_pin[0][1],
        "scenario_rank": cls_row_pin[1][0], "scenario_unknown_now": cls_row_pin[1][1],
        "note": ("unknown 55 -> 4 (the four leftovers are the unconsumed WINs "
                 "ad024/ad028/ad043/ad055); rank 38 -> 4; the class stays UNKNOWN, "
                 "NOT free_now, NOT excluded_now (the declaration's own closure "
                 "delta -51 confirms the 51 own fresh resolutions)"),
    }

    inter = base_idx & scen_idx
    changed_unknown = sorted(c for c in inter
                             if int(b_full[c]["unknown_now"]) != int(s_full[c]["unknown_now"]))
    if changed_unknown != sorted([cls] + list(CHANGED_UNKNOWN_CLOSURE_PIN)):
        fail(f"closure unknown_now changes {changed_unknown} != class 5804 + the pinned "
             f"holder classes 8730/8811 (own 2 / own 1 of the 51 fresh rows)")
    for c in changed_unknown:
        own = sorted(j for j in incr_index if j in s4_cost[c])
        if c not in holder_union:
            fail(f"closure class {c} changed unknown_now but is not a holder of the "
                 "adopted keys")
        if int(b_full[c]["unknown_now"]) - len(own) != int(s_full[c]["unknown_now"]):
            fail(f"closure class {c} unknown_now arithmetic drift: "
                 f"{b_full[c]['unknown_now']} - {len(own)} != {s_full[c]['unknown_now']}")
        if int(s_full[c]["unknown_now"]) != len(scen_unknown[c]):
            fail(f"closure class {c} scenario row unknown_now != recomputed scen unknown")
        if c != cls:
            pin = CHANGED_UNKNOWN_CLOSURE_PIN[c]
            if (int(b_full[c]["class_rank"]), int(b_full[c]["unknown_now"])) != pin[0] \
                    or (int(s_full[c]["class_rank"]), int(s_full[c]["unknown_now"])) != pin[1]:
                fail(f"closure holder row for class {c} != declared pin {pin}")
        for col in ("class_lo", "class_hi", "first_group_first", "first_group_third",
                    "groups_served_count"):
            if b_full[c][col] != s_full[c][col]:
                fail(f"closure row for class {c} changed column {col} (must stay stable)")
        if base_st.get(c) != "unknown" or scen_st.get(c) != "unknown":
            fail(f"closure changed-unknown class {c} recomputed status drift")
        closure_rows["changed_unknown"][str(c)] = {
            "base": [int(b_full[c]["class_rank"]), int(b_full[c]["unknown_now"])],
            "scenario": [int(s_full[c]["class_rank"]), int(s_full[c]["unknown_now"])],
            "own_membership_in_increment": len(own),
        }

    stable_churn = sorted(c for c in inter if c not in changed_unknown
                          and int(b_full[c]["class_rank"]) != int(s_full[c]["class_rank"]))
    if len(stable_churn) != STABLE_UNKNOWN_RANK_CHURN_COUNT:
        fail(f"stable-unknown rank churn count {len(stable_churn)} != pinned "
             f"{STABLE_UNKNOWN_RANK_CHURN_COUNT}")
    holder_set = set(holder_union)
    churn_status_dist = Counter()
    for c in stable_churn:
        if base_st.get(c) != scen_st.get(c):
            fail(f"churned class {c} changed recomputed status "
                 f"{base_st.get(c)} -> {scen_st.get(c)} (churn must be pure ranking "
                 "bookkeeping with stable recomputed status)")
        if c in holder_set:
            fail(f"churned holder class {c} must change unknown_now, not just rank")
        churn_status_dist[f"{base_st.get(c)}"] += 1
    if dict(sorted(churn_status_dist.items())) != dict(sorted(CHURN_STABLE_STATUS_DIST.items())):
        fail(f"stable-unknown churn status distribution {dict(sorted(churn_status_dist.items()))} != "
             f"declared pin {dict(sorted(CHURN_STABLE_STATUS_DIST.items()))}")

    # untouched anchor classes: stable rows (16757 rank moves 4 -> 5 with unknown 29
    # stable: class 5804 overtakes it at unknown 4; machine-observed, no verdict)
    for anchor, pin in CLOSURE_ANCHORS_PIN.items():
        if (int(b_full[anchor]["class_rank"]), int(b_full[anchor]["unknown_now"])) != pin[0] \
                or (int(s_full[anchor]["class_rank"]), int(s_full[anchor]["unknown_now"])) != pin[1]:
            fail(f"anchor class {anchor} closure-row drift: BASE {pin[0]}/scenario {pin[1]} expected")
        closure_rows["anchors"][str(anchor)] = {
            "base_rank": pin[0][0], "base_unknown_now": pin[0][1],
            "scenario_rank": pin[1][0], "scenario_unknown_now": pin[1][1],
        }

    left = sorted(base_idx - scen_idx)
    entered = sorted(scen_idx - base_idx)
    if left != sorted(CLOSURE_LEFT_PIN) or entered != sorted(CLOSURE_ENTERED_PIN):
        fail(f"closure table left {left} / entered {entered} != pinned "
             f"{sorted(CLOSURE_LEFT_PIN)} / {sorted(CLOSURE_ENTERED_PIN)}")
    for c in left:
        pin = CLOSURE_LEFT_PIN[c]
        if (int(b_full[c]["class_rank"]), int(b_full[c]["unknown_now"])) != pin:
            fail(f"left class {c} base row != declared pin {pin}")
        if base_st.get(c) != "unknown":
            fail(f"left class {c} must stay recomputed unknown")
        if int(b_full[c]["unknown_now"]) != len(base_unknown[c]):
            fail(f"left class {c} base row unknown != recomputed BASE unknown")
    for c in entered:
        pin = CLOSURE_ENTERED_PIN[c]
        if (int(s_full[c]["class_rank"]), int(s_full[c]["unknown_now"])) != pin:
            fail(f"entered class {c} scenario row != declared pin {pin}")
        if scen_st.get(c) != "unknown":
            fail(f"entered class {c} must be recomputed unknown (tie-swap churn)")
        if int(s_full[c]["unknown_now"]) != len(scen_unknown[c]):
            fail(f"entered class {c} scenario row unknown != recomputed scen unknown")
        if c not in holder_union and sum(1 for j in incr_index if j in s4_cost[c]) != 0:
            fail(f"entered non-holder class {c} unexpectedly holds an adopted s5 index")
    closure_rows["left_table_classes"] = [{"class_index": c,
                                           "base_row": list(CLOSURE_LEFT_PIN[c])} for c in left]
    closure_rows["entered_table_classes"] = [{"class_index": c,
                                              "scenario_row": list(CLOSURE_ENTERED_PIN[c])} for c in entered]
    closure_rows["churn_note"] = ("54 stable-unknown classes re-rank after the 51 "
                                 "frontier resolutions (50 unknown / 4 excluded_now "
                                 "churn; machine-observed; every churned class keeps "
                                 "its recomputed status and none is a holder of the "
                                 "adopted keys); the left/entered lists are empty; "
                                 "16757 rank 4 -> 5 at stable unknown 29 because "
                                 "class 5804 overtakes it at unknown 4")

    # --- output ----------------------------------------------------------------
    out = {
        "schema": "n11-b31loss51-adoption-decomp-deltas-v1",
        "scenario": ("ADOPTED-CANONICAL = pre-adoption BASE (the Part DB canonical "
                     "state, 6,354 rows, 04b0a239...) + the 51 fresh LOSS rows of "
                     "batch-31 (class 5804; ad001..ad054 except ad024/ad028/ad043/"
                     "ad055; nodes total 237,596,711 per pass); the batch is PROBE-"
                     "COMPLETE: all 55 keys two-pass node-exact (55/55; Part CY "
                     "drive-1 + drive-2 takeover + Part DI reprobe), 51 LOSS rows "
                     "adopted here (zero prior rows: batch-31 is fully fresh) and "
                     "four probe-level WIN verdicts UNCONSUMED: ad024/ad028/ad055 "
                     "halted WINs plus the ad043 15M-EXHAUSTED->DI-30M-WIN supersede "
                     "chain; none is adopted, emitted or written into any canonical "
                     "cache, and NONE is a verdict claim (the C++ second-"
                     "implementation scrutiny owner holds the WIN lane); class 5804 "
                     "does NOT free and is NOT excluded (its leftover unknown "
                     "children are exactly those four WINs; unknown 55 -> 4, rank "
                     "38 -> 4, status stays unknown"),
        "interpretation_guard": ("canonical 51-LOSS adoption deltas: only the 51 "
                                 "fresh LOSS rows are consumed into the canonical "
                                 "cache via the fail-closed union merger; the four "
                                 "probe-level WINs are consumed NOWHERE (no verdict "
                                 "claim, no exclusion claim); class 5804 does NOT "
                                 "free and is NOT excluded in this adoption "
                                 "(unknown 55 -> 4 via the unconsumed WIN "
                                 "children); scheduling quantities are bookkeeping "
                                 "(the joint greedy union -49, the worklist -54 and "
                                 "the per-root greedy mover deltas are honest "
                                 "NON-monotone bookkeeping of the frozen greedy "
                                 "scheduler, with per-root free/uncovered thirds "
                                 "unchanged everywhere; they are NOT coverage "
                                 "claims and NOT progress); every claim stays "
                                 "UNKNOWN; 11x11 empty board and all 19 roots stay "
                                 "UNKNOWN (root 27 baseline 119/119 unchanged); "
                                 "nodes are bookkeeping"),
        "recompute_gates": ("class statuses with Board free-candidate child "
                            "verification, known-universe counts and per-root free "
                            "coverage were recomputed from graph + update8 + cache and "
                            "asserted equal to the published BASE (Part DB reaudit) and "
                            "scenario outputs before any delta was emitted"),
        "pins": {
            "increment_sha256": INCR_SHA,
            "manifest_sha256": MANIFEST_SHA,
            "scenario_cache_sha256": SCEN_CACHE_SHA,
            "base_cache_sha256": BASE_CACHE_SHA,
            "base_summary_sha256": BASE_SUMMARY_SHA,
            "scenario_summary_sha256": SCEN_SUMMARY_SHA,
            "base_closure_classes_sha256": BASE_CLOSURE_SHA,
            "base_per_root_coverage_sha256": BASE_PRC_SHA,
            "base_probe_worklist_sha256": BASE_WORKLIST_SHA,
            "scenario_closure_classes_sha256": SCEN_CLOSURE_SHA,
            "scenario_per_root_coverage_sha256": SCEN_PRC_SHA,
            "scenario_probe_worklist_sha256": SCEN_WORKLIST_SHA,
            "batch31_keys_sha256": B31_KEYS_SHA,
            "status_log_sha256": STATUS_LOG_SHA,
            "kit_manifest_sha256": KIT_MANIFEST_SHA,
            "di_kit_manifest_sha256": DI_MANIFEST_SHA,
            "di_status_sha256": DI_STATUS_SHA,
            "di_ad043_p1_sha256": DI_AD043_P1_SHA,
            "di_ad043_p2_sha256": DI_AD043_P2_SHA,
            "di_exh15m_p1_sha256": DI_EXH15M_P1_SHA,
            "di_exh15m_p2_sha256": DI_EXH15M_P2_SHA,
            "di_anchor_ad054_sha256": DI_ANCHOR54_SHA,
            "di_anchor_ad055_sha256": DI_ANCHOR55_SHA,
            "merge_audit_sha256": MERGE_AUDIT_SHA,
            "merger_sha256": MERGER_SHA,
        },
        "kit_integrity": kit_info,
        "di_kit_integrity": di_kit_info,
        "di_reprobe": di_reprobe_info,
        "di_status": di_status_info,
        "status_log": status_log_info,
        "val_gate": val_gate_info,
        "batch_keys": {
            "count": len(batch_keys), "adopted_loss": 51, "prior_adopted_loss": 0,
            "unadopted_win": 4, "exhausted_excluded": 0, "fileless_unprobed": 0,
            "b31_class": B31_CLASS,
            "b31_keys": 55, "b31_probed": 55, "b31_fragments": 0,
            "b31_class_mask": list(s4_masks[B31_CLASS]),
            "b31_cost_children_total": len(s4_cost[B31_CLASS]),
            "b31_groups_served": [list(x) for x in groups_served],
        },
        "unconsumed_win_rows": [
            {"key_id": kid, "s5_index": WIN_PINS[kid]["s5"],
             "key": [WIN_PINS[kid]["key"][0], WIN_PINS[kid]["key"][1]],
             "legal": WIN_PINS[kid]["legal"], "nodes": WIN_PINS[kid]["nodes"],
             "decisive_budget": WIN_PINS[kid]["decisive_budget"],
             "membership_class_count": WIN_PINS[kid]["membership"],
             "consumed": False,
             "note": ("probe-level WIN (result 1) observed two-pass node-exact and "
                      "halted (WIN-HALT); NOT adopted, NOT emitted, NOT in any "
                      "canonical cache; verdict not consumed; WIN-row scrutiny "
                      "belongs to the C++ second-implementation owner pin "
                      "9193f5b6... (Part CZ published the three-implementation "
                      "corroboration); class 5804 stays unknown because of them")}
            for kid in WIN_IDS],
        "status_transitions": dict(sorted(transitions.items())),
        "excluded_now_flips": flips,
        "newly_free_now_classes": new_free,
        "newly_free_now_gate": ("the zero-WIN-consumed packet can only free classes "
                               "whose BASE-unknown children are ALL resolved by the "
                               "loss-only increment; the machine-computed list is "
                               "empty here; class 5804 does NOT free (its four "
                               "unconsumed WIN children remain) and is NOT excluded"),
        "class_rows": class_rows,
        "adopted_rows": [
            {"key_id": kid, "s5_index": a["s5"], "key": [a["key"][0], a["key"][1]],
             "legal": a["legal"], "nodes": a["nodes"], "consumed": True,
             "note": ("two-pass node-exact LOSS row adopted into the canonical chain "
                      "via the pinned fail-closed union merger 90711961...; batch-31 "
                      "probe-complete drive (Part CY drive-1 + drive-2 takeover + "
                      "Part DI reprobe); node-exact 15M/30M budget-independence "
                      "anchored by the DI host; verdict not consumed")}
            for kid, a in ((k, ADOPTED[k]) for k in ADOPTED_IDS)],
        "prior_rows_note": ("zero prior rows: batch-31 is fully fresh (BASE is the "
                            "Part DB canonical state of 6,354 rows and no batch-31 "
                            "key had been adopted before Part DL)"),
        "changed_per_root_coverage_rows": changed_rows,
        "individual_greedy_union_movers": greedy_moved_rows,
        "holder_union_size": len(holder_union),
        "holder_classes": holder_rows,
        "member_loss_counts": {str(k): v for k, v in sorted(member_loss_counts.items())},
        "metrics": metrics,
        "metrics_note": ("joint_greedy_union_size 36,903 -> 36,854 (-49) after the 51 "
                         "frontier slots resolve: NON-monotone bookkeeping of the "
                         "frozen greedy scheduling heuristic; the probe worklist "
                         "shrinks 64,765 -> 64,711 (-54); per-root free/uncovered "
                         "thirds are unchanged everywhere; NOT a coverage claim and "
                         "NOT a verdict; per-root greedy movers 4/5/13/25/38/49 with "
                         "deltas -1/-2/-1/-1/-50/-105"),
        "update8": {
            "newly_resolved_s5": newly_resolved,
            "newly_resolved_count": len(newly_resolved),
            "lost_resolved": lost,
            "note": ("exactly one adopted key (ad009, s5 148458) resolves an "
                     "update8 baseline requirement (machine-observed): "
                     "resolved_count 141 -> 142 and remaining_now 31,718 -> 31,717"),
        },
        "per_root_greedy": per_root_greedy_movers,
        "roots_summary_moved": roots_summary_moved,
        "probe_worklist": worklist_info,
        "closure_candidate_rows": closure_rows,
    }
    OUT.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("OK decomp-deltas-b31loss51-adoption.json: "
          f"flips={flips} new_free={new_free} "
          f"free_now {metrics['free_now_classes']['base']}->{metrics['free_now_classes']['scenario']} "
          f"class5804_unknown {len(base_unknown[cls])}->{len(scen_unknown[cls])} "
          f"rank {closure_rows['classes'][str(cls)]['base_rank']}->{closure_rows['classes'][str(cls)]['scenario_rank']} "
          f"(status {scen_st[cls]}; 4 WINs unconsumed) "
          f"update8_resolved +{len(newly_resolved)} "
          f"joint_greedy {metrics['joint_greedy_union_size']['base']}->{metrics['joint_greedy_union_size']['scenario']} "
          f"worklist {metrics['probe_worklist_total']['base']}->{metrics['probe_worklist_total']['scenario']} "
          f"kit={kit_info['files_verified']} di_kit={di_kit_info['files_verified']} "
          f"changed_unknown={sorted(changed_unknown)} "
          f"ig_movers={sorted(greedy_moved_rows)} "
          f"closure_left={left} closure_entered={entered}")


if __name__ == "__main__":
    main()
