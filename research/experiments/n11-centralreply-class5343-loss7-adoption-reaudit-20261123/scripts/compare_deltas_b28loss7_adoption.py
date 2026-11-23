#!/usr/bin/env python3
"""Batch-28 (class 5343) 7-LOSS adoption reaudit delta extractor
(Part CO).

Fail-closed, read-only audit executing the single-owner Part CO
declaration (2026-11-23; publish-then-execute).  Compares the published
BASE refresh outputs (Part CH reaudit on the canonical cache 3124461b...,
6,294 rows) against the single post-adoption computation:

  ADOPTED-CANONICAL = BASE + the 7 fresh LOSS rows
  (batch-28 / class 5343: aa015 / aa017 / aa018 / aa023 / aa024 / aa029 /
  aa036; s5 164462 / 170101 / 173654 / 193820 / 196053 / 199714 / 199721;
  nodes total 38,784,669)

The batch is a COMPLETE two-pass enumeration book on drive-5 (all 54 keys
probed node-exactly on both passes; cumulative status log 109 lines with a
final aa054 WIN-HALT row; drive-4 is the byte-prefix 61-line pre-registered
WIN-HALT prefix state with 31 keys).  The resolved packet holds 35 WIN
rows (honest labels; aa001/aa002 Part CC third-implementation
cross-verified, aa006/aa007 Part CG cross-verification lane declared with
the d5e9acc2 takeover still pending output, aa008/aa009 Part CM
third-implementation cross-verified, the remaining 29 unverified labels)
and 11 EXHAUSTED rows (honest UNKNOWN, budget 15M exhausted on both
passes).  Only the 7 fresh LOSS rows are adopted; aa003 was already
adopted by Part CH and is asserted BASE-consistent, NOT re-emitted.
Full != loss, and the WIN rows stay unconsumed (scrutiny owner C++
second-implementation gate pin 9193f5b6...; batch-14residual q042 /
batch-26 l028 precedents), so class 5343 does NOT free: it keeps 46
BASE-unknown cost children (exactly the 35 WIN + 11 EXHAUSTED s5
indices) and stays unknown with rank 19 -> 4 in the closure table.

Gates (fail-closed, machine-checked) mirror the Part CH extractor
discipline adapted to the fully-probed 1-batch / 7-row / 35-WIN /
11-EXHAUSTED shape of batch-28 drive-5:

  * sha256 pins: increment, scenario cache, base cache, base summary,
    scenario summary, base/scenario closure-classes.csv, base/scenario
    per-root-coverage.csv, the shared batch-28 batch-keys file, the
    drive-4 row-audit-winhalt, the drive-5 row-audit full-v2, both
    status logs, and BOTH drive kit MANIFEST-sha256.txt files (with a
    full file-by-file sha re-verification of all 150 drive-4 + 200
    drive-5 kit files from their manifests);
  * status log gates: drive-4 is a byte-prefix of drive-5, drive-5 has
    109 lines with the pinned final verdict row
    "2026-11-23T19:24:56Z aa054 WIN-HALT" and exactly one junk row
    "P1-FAIL " (trailing space; disclosed empty-key invocation artifact,
    no key id, no verdict);
  * manifest (b28loss7-increments-manifest-v1): 7 adopted LOSS / 35
    unadopted WIN / 11 EXHAUSTED / 54 probed / 0 fragments / 0 fileless,
    loss sha == increment sha, merger pin, base cache pin 3124461b...
    (6,294 rows, zero absent hits for emitted rows, zero quarantine
    hits), adopted-row node totals pinned (38,784,669 both passes),
    aa003 BASE-consistency block pinned;
  * both published row audits (drive-4 winhalt + drive-5 full) agree
    with the manifest and the pinned id lists;
  * independent two-pass raw re-verification of ALL 54 probed keys from
    the drive-5 raws: both passes agree exactly, the 7 adopted keys are
    result 2 (LOSS) with published node counts, aa003 is result 2 with
    its Part CH node count, the 35 WIN keys are result 1 honest labels
    with published node counts, the 11 EXHAUSTED keys are result 0 with
    nodes == budget; the 6 adopted keys also present on drive-4 carry
    byte-identical replay rows across both drives (aa036 is drive-5
    only by the pre-registered halt position);
  * increment == exactly the 7 fresh LOSS rows; aa003 NOT re-emitted;
    WIN/EXHAUSTED keys asserted NOT in the increment, NOT in BASE, NOT
    in the scenario cache, not in the update8 receipt, quarantined
    nowhere, canonical-safe;
  * scenario cache == BASE rows + the 7 increment rows with verdict
    agreement (6,301 rows; 158 WIN / 6,143 LOSS);
  * every graph holder class of every adopted key (union 21): scenario
    unknown_now == BASE unknown_now - own membership in the increment
    (class 5343 own == 7; per-key holder counts == batch-keys
    membership_class_count: 4 for six keys, 3 for aa036);
  * the published refresh recomputes (class statuses with Board
    free-candidate child verification, known-universe counts, per-root
    coverage) are re-executed from graph + update8 + cache and asserted
    equal to the published BASE (Part CH reaudit) and scenario outputs
    before any delta is emitted;
  * no excluded_now flips, no newly free class beyond the machine
    recomputation (the loss-only packet frees nothing: free_now stays
    38), no per-root coverage regression, root 27 stays 119/119;
  * closure table: class 5343 unknown_now 53 -> 46 (rank 19 -> 4); the
    only other unknown_now changes are the holder classes 5232
    (102 -> 101, rank 605 -> 570) and 11641 (56 -> 55, rank 69 -> 47);
    every class that changes unknown_now is a holder with exact
    own-membership arithmetic and every other column stable; exactly
    431 classes churn rank with stable unknown (pure ranking
    bookkeeping, none of them a holder); table grows 807 -> 808 with
    left == {12697} and entered == {5233, 5374} (all recomputed
    unknown); anchors 23101 / 1849 / 12643 stay fully stable
    (rank/unknown 1/1, 2/1, 21/53);
  * update8 resolved-requirement delta gated to the increment: newly
    resolved set == {164462, 170101, 173654, 193820, 196053, 199714,
    199721} only, none lost; resolved_count 134 -> 141, remaining
    31,725 -> 31,718;
  * metrics pinned (both sides exact): excluded 390 / excluded_now 23 /
    free_now 38 / unknown 34,498 class_status_counts pairs; joint
    greedy 38,295 -> 38,310; worklist 64,746 -> 64,828; group best
    options 2,119 stable; per-root greedy movers only roots 4
    (5,977 -> 5,949), 16 (2,972 -> 2,971), 49 (2,810 -> 2,803);
    roots_summary_moved EMPTY.

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
OUT = EXP / "output/decomp-deltas-b28loss7-adoption.json"

GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_DIR = ROOT / "research/experiments/n11-centralreply-class5343-loss1-adoption-reaudit-20261123/reaudit/output"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class5343-loss1-adoption-reaudit-20261123/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-plus-batch20loss53-plus-batch26loss52-plus-batch24loss2-plus-batch27loss4-plus-batch28loss1-20261123.cache"
D4_DIR = ROOT / "research/experiments/n11-centralreply-closure-class5343-batch28-drive4-20261123"
D5_DIR = ROOT / "research/experiments/n11-centralreply-closure-class5343-batch28-drive5-20261123"
SCEN_OUT = EXP / "reaudit/output"
INCR_CACHE = EXP / "output/increment-b28loss7-20261123.cache"
MANIFEST = EXP / "output/increments-manifest.json"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-20261123.cache"

INCR_SHA = "bd5ef7d7632816006bd5a74349bf703a8dd3251e3a550a33e7ae7a0253abe382"
SCEN_CACHE_SHA = "854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d"
BASE_CACHE_SHA = "3124461b14e4f73a7248cbf5b96c7ff59ebfdcc05258adeb9c81791d86cc461e"
BASE_SUMMARY_SHA = "76cad2a14263ee59cd8bc83008c26bd0b656f2c74e2e7a650550306dda40d395"
SCEN_SUMMARY_SHA = "4727fb2b991d78107a67aa3ef2bf533be042907214216f8d363a23f884228179"
BASE_CLOSURE_SHA = "baa2db136c18c681633e5bfe3b5a1dec3f084d0c696b4454ae1855ab0773e7fd"
BASE_PRC_SHA = "75e594419d7822752c9b91b58b8c96ba352296f83707b98786a8bd07afb6c439"
SCEN_CLOSURE_SHA = "9d3965d94db9fc8005fda1cd24aadf1b515a799e5558448a391489cd24caa85d"
SCEN_PRC_SHA = "8e6fb981ee637d896cbf6d378d0543db06d5552da725cba2fa24130cc6fd4809"
B28_KEYS_SHA = "af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5"
D4_ROW_AUDIT_SHA = "dcf078aab8f05dea3dde25da517393de9b851cf1042c7a05ff489203ba284358"
D5_ROW_AUDIT_SHA = "00c323835f9ebc048b6ffea81a8fd556e3e8146adf1c562c34aa89d9d7bb69c0"
D4_STATUS_SHA = "598174447fa878c2e0a6d6db6f892c5c279063174d763746456476e3051633f8"
D5_STATUS_SHA = "ca1e98ccd952b29e8295147add50e6b4a3ff3732748bf544b9c3a7018d495df0"
D4_KIT_MANIFEST_SHA = "1e4024f861e0080d63bc606d8d53a02bd909d97708aca0b3933dc3dff1041475"
D5_KIT_MANIFEST_SHA = "e2d81055c19945d4f0a4e29a3c521381c31f540f12537a4daddf5dfb1b597a3c"

SCENARIO = "ADOPTED-CANONICAL"
UNIVERSE_SIZE = 31859
RECEIPT_COUNT = 23
ADOPTED_ROWS = 7
B28_CLASS = 5343
BUDGET = 15000000
ADOPTED_IDS = ["aa015", "aa017", "aa018", "aa023", "aa024", "aa029", "aa036"]
RESOLVED_IDS = [f"aa{i:03d}" for i in range(1, 55)]
ADOPTED_TOTAL_NODES = 38784669
NEWLY_RESOLVED_S5 = [164462, 170101, 173654, 193820, 196053, 199714, 199721]
AA003 = {"s5": 104943, "key": (1152921504741064704, 4228), "legal": 86,
         "nodes": 4070373}
MEMBERSHIP_EXPECT = {"aa015": 4, "aa017": 4, "aa018": 4,
                     "aa023": 4, "aa024": 4, "aa029": 4, "aa036": 3}
HOLDER_UNION_SIZE = 21
ALLOWED_TRANSITIONS = {"excluded": ["excluded"], "excluded_now": ["excluded_now"],
                       "free_now": ["free_now"], "unknown": ["unknown", "free_now"]}
# closure-table pins (observed machine-side, declared before the official run):
CLOSURE_COUNTS = (807, 808)
CLASS_5343_CLOSURE_PIN = ((19, 53), (4, 46))
CHANGED_UNKNOWN_CLOSURE_PIN = {
    5232: ((605, 102), (570, 101)),
    11641: ((69, 56), (47, 55)),
}
STABLE_UNKNOWN_RANK_CHURN_COUNT = 431
CLOSURE_ENTERED_PIN = {5233: (722, 106), 5374: (412, 91)}
CLOSURE_LEFT_PIN = {12697: (721, 106)}
CLOSURE_ANCHORS_PIN = {23101: (1, 1), 1849: (2, 1), 12643: (21, 53)}
D5_STATUS_LINES = 109
D5_FINAL_VERDICT_ROW = "2026-11-23T19:24:56Z aa054 WIN-HALT"
D4_FINAL_ROW = "2026-11-23T18:18:30Z aa031 EXHAUSTED 15000000,0,15000000"
JUNK_ROW = "P1-FAIL "
D4_KIT_FILES = 150
D5_KIT_FILES = 200
D4_PROBED = 31
D4_ADOPTED_PRESENT = ["aa015", "aa017", "aa018", "aa023", "aa024", "aa029"]
# metrics pins (declared before the official run; BASE -> scenario)
METRICS_PIN = {
    "excluded_now_classes": (23, 23),
    "free_now_classes": (38, 38),
    "unknown_classes": (34498, 34498),
    "update8_remaining_now": (31725, 31718),
    "update8_resolved_count": (134, 141),
    "update8_win_hit_groups": (0, 0),
    "update8_groups_free_now": (131, 131),
    "joint_greedy_unique_groups": (2119, 2119),
    "joint_greedy_union_size": (38295, 38310),
    "probe_worklist_total": (64746, 64828),
    "group_best_options_nonfree": (2119, 2119),
    "closure_classes_count": (807, 808),
}
PRG_MOVERS_PIN = {"4": (5977, 5949), "16": (2972, 2971), "49": (2810, 2803)}
WINS = [
    {"kid": "aa001", "s5": 28037, "key": (1315631633331650560, 0),
     "legal": 88, "nodes": 13183855,
     "cross": "Part CC third-implementation cross-verified"},
    {"kid": "aa002", "s5": 87306, "key": (1171516445390012416, 0),
     "legal": 86, "nodes": 6527041,
     "cross": "Part CC third-implementation cross-verified"},
    {"kid": "aa006", "s5": 129823, "key": (1171516445255794692, 0),
     "legal": 88, "nodes": 14303810,
     "cross": "Part CG cross-verification lane declared (takeover d5e9acc2, pending output)"},
    {"kid": "aa007", "s5": 135236, "key": (1171516445255794696, 0),
     "legal": 95, "nodes": 13483540,
     "cross": "Part CG cross-verification lane declared (takeover d5e9acc2, pending output)"},
    {"kid": "aa008", "s5": 140489, "key": (1171516445255794704, 0),
     "legal": 85, "nodes": 5270340,
     "cross": "Part CM third-implementation cross-verified"},
    {"kid": "aa009", "s5": 142299, "key": (1747977197559218176, 0),
     "legal": 91, "nodes": 7319605,
     "cross": "Part CM third-implementation cross-verified"},
    {"kid": "aa010", "s5": 144019, "key": (1171516445255794720, 0),
     "legal": 86, "nodes": 8882182,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa011", "s5": 147632, "key": (1171516445255796736, 0),
     "legal": 90, "nodes": 12424953,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa012", "s5": 151960, "key": (1171516445255798784, 0),
     "legal": 81, "nodes": 4994213,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa013", "s5": 156182, "key": (1171516445255802880, 0),
     "legal": 87, "nodes": 8317071,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa014", "s5": 160350, "key": (1171516445255811072, 0),
     "legal": 88, "nodes": 7263370,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa016", "s5": 167491, "key": (1171516445255860224, 0),
     "legal": 78, "nodes": 2621847,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa019", "s5": 183025, "key": (1171516445322903552, 0),
     "legal": 86, "nodes": 7967030,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa020", "s5": 185891, "key": (1171516453845729280, 0),
     "legal": 90, "nodes": 8432253,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa022", "s5": 191399, "key": (1171516479615533056, 0),
     "legal": 87, "nodes": 14044375,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa025", "s5": 198223, "key": (1171516720133701632, 0),
     "legal": 80, "nodes": 3056950,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa026", "s5": 199711, "key": (1171516445255794688, 32),
     "legal": 88, "nodes": 11019409,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa027", "s5": 199712, "key": (1171516445255794688, 64),
     "legal": 81, "nodes": 4860191,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa033", "s5": 199718, "key": (1171516445255794688, 128),
     "legal": 86, "nodes": 3347117,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa034", "s5": 199719, "key": (1152921504606846977, 4228),
     "legal": 94, "nodes": 14097048,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa037", "s5": 199722, "key": (1152921504606846980, 4228),
     "legal": 87, "nodes": 14239714,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa038", "s5": 199723, "key": (1152921504606849024, 4228),
     "legal": 82, "nodes": 4911996,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa039", "s5": 199724, "key": (1152921504606846984, 4228),
     "legal": 88, "nodes": 11349776,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa040", "s5": 199725, "key": (1152921504606846992, 4228),
     "legal": 89, "nodes": 8916641,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa041", "s5": 199726, "key": (1171516445255794688, 8),
     "legal": 93, "nodes": 10283599,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa042", "s5": 199727, "key": (1152921504606847008, 4228),
     "legal": 88, "nodes": 5800791,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa043", "s5": 199728, "key": (1152921513196781568, 4228),
     "legal": 90, "nodes": 12069965,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa044", "s5": 199729, "key": (1152921521786716160, 4228),
     "legal": 86, "nodes": 9219778,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa045", "s5": 199730, "key": (1152921642045800448, 4228),
     "legal": 84, "nodes": 12371943,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa046", "s5": 199731, "key": (1152921779484753920, 4228),
     "legal": 78, "nodes": 2185149,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa048", "s5": 199733, "key": (1152921504615235584, 4228),
     "legal": 87, "nodes": 10553343,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa049", "s5": 199734, "key": (1152921504623624192, 4228),
     "legal": 83, "nodes": 7272703,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa051", "s5": 199736, "key": (1152921504673955840, 4228),
     "legal": 87, "nodes": 7662388,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa052", "s5": 199737, "key": (1152921504606851072, 4228),
     "legal": 93, "nodes": 8976982,
     "cross": "cross-verification pending (honest label only)"},
    {"kid": "aa054", "s5": 199739, "key": (1152921504606863360, 4228),
     "legal": 95, "nodes": 13227570,
     "cross": "cross-verification pending (honest label only)"},
]

EXHAUSTED = [
    {"kid": "aa004", "s5": 118693, "key": (1171516445255794689, 0),
     "legal": 91},
    {"kid": "aa005", "s5": 124331, "key": (1171516445255794690, 0),
     "legal": 89},
    {"kid": "aa021", "s5": 188751, "key": (1171516462435663872, 0),
     "legal": 90},
    {"kid": "aa028", "s5": 199713, "key": (1152921504606879744, 4228),
     "legal": 95},
    {"kid": "aa030", "s5": 199715, "key": (1243574039293722624, 0),
     "legal": 90},
    {"kid": "aa031", "s5": 199716, "key": (1459746821407506432, 0),
     "legal": 92},
    {"kid": "aa032", "s5": 199717, "key": (1171516445255794688, 4),
     "legal": 91},
    {"kid": "aa035", "s5": 199720, "key": (1152921504606846978, 4228),
     "legal": 96},
    {"kid": "aa047", "s5": 199732, "key": (1152921504611041280, 4228),
     "legal": 92},
    {"kid": "aa050", "s5": 199735, "key": (1152921504640401408, 4228),
     "legal": 94},
    {"kid": "aa053", "s5": 199738, "key": (1152921504606855168, 4228),
     "legal": 95},
]

ADOPTED = {
    "aa036": {"kid": "aa036", "s5": 199721, "key": (1152921504606912512, 4228),
     "legal": 64, "nodes": 955659},
    "aa029": {"kid": "aa029", "s5": 199714, "key": (1171516445255794688, 16),
     "legal": 90, "nodes": 10010789},
    "aa015": {"kid": "aa015", "s5": 164462, "key": (1171516445255827456, 0),
     "legal": 89, "nodes": 6152494},
    "aa017": {"kid": "aa017", "s5": 170101, "key": (1171516445259988992, 0),
     "legal": 92, "nodes": 11446358},
    "aa018": {"kid": "aa018", "s5": 173654, "key": (1171516445264183296, 0),
     "legal": 91, "nodes": 214968},
    "aa023": {"kid": "aa023", "s5": 193820, "key": (1171516513975271424, 0),
     "legal": 84, "nodes": 5000770},
    "aa024": {"kid": "aa024", "s5": 196053, "key": (1171516582694748160, 0),
     "legal": 88, "nodes": 5003631},
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


def main():
    # --- sha pins ------------------------------------------------------------
    for name, p, want in (("increment", INCR_CACHE, INCR_SHA),
                          ("scenario cache", SCEN_CACHE, SCEN_CACHE_SHA),
                          ("base cache", BASE_CACHE, BASE_CACHE_SHA),
                          ("base summary", BASE_DIR / "refresh-summary.json", BASE_SUMMARY_SHA),
                          ("scenario summary", SCEN_OUT / "refresh-summary.json", SCEN_SUMMARY_SHA),
                          ("base closure-classes", BASE_DIR / "closure-classes.csv", BASE_CLOSURE_SHA),
                          ("base per-root-coverage", BASE_DIR / "per-root-coverage.csv", BASE_PRC_SHA),
                          ("scenario closure-classes", SCEN_OUT / "closure-classes.csv", SCEN_CLOSURE_SHA),
                          ("scenario per-root-coverage", SCEN_OUT / "per-root-coverage.csv", SCEN_PRC_SHA),
                          ("drive-4 batch keys", D4_DIR / "input/batch-keys.json", B28_KEYS_SHA),
                          ("drive-5 batch keys", D5_DIR / "input/batch-keys.json", B28_KEYS_SHA),
                          ("drive-4 row-audit", D4_DIR / "output/row-audit-winhalt.json", D4_ROW_AUDIT_SHA),
                          ("drive-5 row-audit", D5_DIR / "output/row-audit.json", D5_ROW_AUDIT_SHA),
                          ("drive-4 status log", D4_DIR / "output/status.log", D4_STATUS_SHA),
                          ("drive-5 status log", D5_DIR / "output/status.log", D5_STATUS_SHA),
                          ("drive-4 kit manifest", D4_DIR / "MANIFEST-sha256.txt", D4_KIT_MANIFEST_SHA),
                          ("drive-5 kit manifest", D5_DIR / "MANIFEST-sha256.txt", D5_KIT_MANIFEST_SHA)):
        got = sha(p)
        if got != want:
            fail(f"{name} sha256 drift: {got} != {want}")

    # --- kit full file-by-file sha re-verification (both drive kits) ----------
    kit_info = {}
    for tag, kit_dir, want_files in (("drive4", D4_DIR, D4_KIT_FILES),
                                     ("drive5", D5_DIR, D5_KIT_FILES)):
        entries = []
        for line in (kit_dir / "MANIFEST-sha256.txt").read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(None, 1)
            if len(parts) != 2:
                fail(f"{tag} kit manifest line not '<sha256> <path>': {line}")
            entries.append((parts[0], parts[1]))
        if len(entries) != want_files:
            fail(f"{tag} kit manifest lists {len(entries)} files != {want_files}")
        for want_sha, rel in entries:
            p = kit_dir / rel
            got = sha(p)
            if got != want_sha:
                fail(f"{tag} kit file sha drift at {rel}: {got} != {want_sha}")
        kit_info[tag] = {"manifest_sha256": D4_KIT_MANIFEST_SHA if tag == "drive4" else D5_KIT_MANIFEST_SHA,
                         "files_verified": len(entries)}

    # --- status log gates: drive-4 is an exact byte-prefix of drive-5 ---------
    d4_bytes = (D4_DIR / "output/status.log").read_bytes()
    d5_bytes = (D5_DIR / "output/status.log").read_bytes()
    if not d5_bytes.startswith(d4_bytes):
        fail("drive-4 status log is not an exact byte-prefix of drive-5")
    d5_lines = d5_bytes.decode("utf-8").splitlines()
    d4_lines = d4_bytes.decode("utf-8").splitlines()
    if len(d5_lines) != D5_STATUS_LINES or len(d4_lines) != 61:
        fail(f"status log line counts {len(d4_lines)}/{len(d5_lines)} != 61/109")
    if d5_lines[-1] != JUNK_ROW:
        fail(f"drive-5 final junk row {d5_lines[-1]!r} != {JUNK_ROW!r}")
    junk = [l for l in d5_lines if l == JUNK_ROW]
    if len(junk) != 1:
        fail(f"junk row count {len(junk)} != 1")
    if d5_lines[-2] != D5_FINAL_VERDICT_ROW:
        fail(f"drive-5 final verdict row {d5_lines[-2]!r} != {D5_FINAL_VERDICT_ROW!r}")
    if d4_lines[-1] != D4_FINAL_ROW:
        fail(f"drive-4 final row {d4_lines[-1]!r} != {D4_FINAL_ROW!r}")
    status_log_info = {
        "drive4_lines": len(d4_lines), "drive5_lines": len(d5_lines),
        "drive4_is_prefix": True, "junk_row": JUNK_ROW,
        "junk_row_note": ("disclosed empty-key invocation artifact (Part CN completion "
                          "log); no key id, no verdict record; '.p1.out' node ENOENT"),
        "drive5_final_verdict_row": D5_FINAL_VERDICT_ROW,
        "drive4_final_row": D4_FINAL_ROW,
    }

    manifest = json.loads(MANIFEST.read_text())
    if manifest["schema"] != "b28loss7-increments-manifest-v1":
        fail(f"manifest schema drift: {manifest['schema']}")
    rc = manifest["row_counts"]
    if not (rc["adopted_loss_rows"] == 7 and rc["wins"] == 35
            and rc["exhausted_excluded"] == 11 and rc["probed_rows"] == 54
            and rc["fragments_unprobed"] == 0 and rc["fileless_unprobed"] == 0):
        fail(f"manifest row_counts not the fully-probed 7-LOSS / 35-WIN / 11-EXHAUSTED picture: {rc}")
    if manifest["loss_ids"] != ADOPTED_IDS:
        fail(f"manifest loss id list drift: {manifest['loss_ids']}")
    if manifest["win_ids"] != manifest["unadopted_win_ids"] or len(manifest["win_ids"]) != 35:
        fail("manifest win_ids != unadopted_win_ids (35 honest WIN labels)")
    if sorted(manifest["resolved_ids"]) != sorted(RESOLVED_IDS):
        fail("manifest resolved_ids != all 54 batch keys")
    if manifest["full_packet_eq_loss_only"] is not False or manifest["win_scenario_exists"] is not True:
        fail("manifest full != loss / WIN-scenario bookkeeping not asserted "
             "(35 WIN rows exist and are NOT adopted)")
    if manifest["sha256"]["loss"] != INCR_SHA:
        fail("manifest loss sha does not match the pinned increment")
    if manifest["merger_sha256"] != "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a":
        fail("manifest merger pin drift (the pinned fail-closed union merger)")
    if (manifest["base_cache_sha256"] != BASE_CACHE_SHA
            or manifest["base_cache_rows"] != 6294
            or manifest["base_cache_absent_hits_for_emitted"] != 0
            or manifest["quarantine_hits"] != 0):
        fail("manifest BASE-cache bookkeeping drift (6,294 rows 3124461b..., no absent hits)")
    per_batch_manifest = {b["batch"]: b for b in manifest["batches"]}
    if set(per_batch_manifest) != {28}:
        fail("manifest batches != {28}")
    mb = per_batch_manifest[28]
    if mb["class_index"] != B28_CLASS or mb["keys_total"] != 54:
        fail("manifest batch-28 class/keys_total drift")
    if (mb["adopted_loss_ids"] != ADOPTED_IDS or mb["already_adopted_ids"] != ["aa003"]
            or mb["unadopted_win_ids"] != manifest["win_ids"]):
        fail("manifest batch-28 adopted/unadopted id lists drift")
    if sorted(mb["probed_ids"]) != sorted(RESOLVED_IDS):
        fail("manifest batch-28 probed ids != all 54 keys")
    if (mb["input_sha256"] != B28_KEYS_SHA
            or mb["row_audit_sha256"]["drive4_winhalt"] != D4_ROW_AUDIT_SHA
            or mb["row_audit_sha256"]["drive5_full_v2"] != D5_ROW_AUDIT_SHA):
        fail("manifest batch-28 input/row-audit sha bookkeeping drift")
    if (mb["status_log_sha256"]["drive4"] != D4_STATUS_SHA
            or mb["status_log_sha256"]["drive5"] != D5_STATUS_SHA
            or mb["status_log_sha256"]["drive4_is_exact_prefix_of_drive5"] is not True):
        fail("manifest batch-28 status-log sha bookkeeping drift")
    if mb["status_log_final_verdict_row"] != D5_FINAL_VERDICT_ROW:
        fail("manifest batch-28 final verdict row drift")
    if mb["status_log_junk_row"]["row"] != JUNK_ROW:
        fail(f"manifest batch-28 junk row drift: {mb['status_log_junk_row']['row']!r}")
    if (mb["kit_integrity"]["drive4"]["manifest_sha256"] != D4_KIT_MANIFEST_SHA
            or mb["kit_integrity"]["drive4"]["files_verified"] != D4_KIT_FILES
            or mb["kit_integrity"]["drive5"]["manifest_sha256"] != D5_KIT_MANIFEST_SHA
            or mb["kit_integrity"]["drive5"]["files_verified"] != D5_KIT_FILES):
        fail("manifest batch-28 kit integrity drift")
    if len(mb["truncated_sidecars"]) != 8 or len(mb["truncated_retry_rows"]) != 8:
        fail("manifest batch-28 truncated sidecar/retry bookkeeping drift (8 each)")
    if (mb["total_nodes_pass_one"] != mb["total_nodes_pass_two"]
            or mb["total_nodes_pass_one"] != ADOPTED_TOTAL_NODES):
        fail(f"manifest batch-28 adopted-row node total drift ({ADOPTED_TOTAL_NODES} expected)")
    if mb["fragment_state"] != {}:
        fail("manifest batch-28 fragment_state must be empty (0 fragments)")
    uwr = manifest["unadopted_win_rows"]
    if not (isinstance(uwr, list) and len(uwr) == 35):
        fail("manifest unadopted_win_rows must list the 35 honest WIN labels")
    win_by_kid = {w["kid"]: w for w in WINS}
    for row in uwr:
        w = win_by_kid.get(row["key_id"])
        if w is None:
            fail(f"manifest unadopted WIN row unknown key_id: {row['key_id']}")
        if not (row["s5_index"] == w["s5"] and (row["lo"], row["hi"]) == w["key"]
                and row["legal"] == w["legal"] and row["result"] == 1
                and row["nodes"] == w["nodes"] and row["two_pass_node_exact"] is True):
            fail(f"manifest unadopted WIN row bookkeeping drift: {row}")
    exr = manifest["exhausted_rows"]
    if not (isinstance(exr, list) and len(exr) == 11):
        fail("manifest exhausted_rows must list the 11 honest EXHAUSTED labels")
    exh_by_kid = {e["kid"]: e for e in EXHAUSTED}
    for row in exr:
        e = exh_by_kid.get(row["key_id"])
        if e is None:
            fail(f"manifest EXHAUSTED row unknown key_id: {row['key_id']}")
        if not (row["s5_index"] == e["s5"] and (row["lo"], row["hi"]) == e["key"]
                and row["legal"] == e["legal"] and row["result"] == 0
                and row["nodes"] == BUDGET and row["two_pass_node_exact"] is True):
            fail(f"manifest EXHAUSTED row bookkeeping drift: {row}")
    a3 = manifest["aa003_base_consistency"]
    if (a3["key_id"] != "aa003" or a3["s5_index"] != AA003["s5"]
            or tuple(a3["key"]) != AA003["key"] or a3["legal"] != AA003["legal"]
            or a3["base_row"] != [2, AA003["nodes"]] or a3["raw_row"] != [2, AA003["nodes"]]
            or a3["re_emitted"] is not False):
        fail(f"manifest aa003 BASE-consistency block drift: {a3}")

    # --- both published row audits -------------------------------------------
    ra4 = json.loads((D4_DIR / "output/row-audit-winhalt.json").read_text())
    if (ra4["schema"] != "n11-centralreply-closure-class5343-batch28-rowaudit-winhalt-v1"
            or ra4["class_index"] != B28_CLASS or ra4["batch"] != 28
            or ra4["keys_total"] != 54 or ra4["probed"] != D4_PROBED
            or ra4["pass_rows"] != 7 or ra4["mismatches"] != 0
            or ra4["input_sha256"] != B28_KEYS_SHA
            or ra4["fragment_keys"] != {} or ra4["derived_state"] is not True
            or ra4["unprobed_count"] != 23):
        fail(f"published drive-4 row-audit not the published picture: {ra4}")
    d4_loss_expected = sorted(["aa003"] + D4_ADOPTED_PRESENT)
    if sorted(ra4["loss_rows"]) != d4_loss_expected:
        fail(f"drive-4 row-audit loss rows {ra4['loss_rows']} != {d4_loss_expected}")
    ra5 = json.loads((D5_DIR / "output/row-audit.json").read_text())
    if (ra5["schema"] != "n11-centralreply-closure-class5343-batch28-rowaudit-full-v2"
            or ra5["class_index"] != B28_CLASS or ra5["batch"] != 28
            or ra5["keys_total"] != 54 or ra5["probed"] != 54
            or ra5["pass_rows"] != 8 or ra5["mismatches"] != 0
            or ra5["input_sha256"] != B28_KEYS_SHA):
        fail(f"published drive-5 row-audit not the published picture: {ra5}")
    if sorted(ra5["loss_rows"]) != sorted(["aa003"] + ADOPTED_IDS):
        fail(f"drive-5 row-audit loss rows {ra5['loss_rows']} != aa003 + the 7 adopted")
    if sorted(ra5["win_rows"]) != sorted(win_by_kid):
        fail("drive-5 row-audit win rows != the 35 honest WIN labels")
    if sorted(ra5["exhausted_rows"]) != sorted(exh_by_kid):
        fail("drive-5 row-audit exhausted rows != the 11 EXHAUSTED labels")

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
    bk, groups_served = load_keys(D5_DIR, B28_CLASS)
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
        batch_keys[kid] = (lo, hi, s5i, int(k["membership_class_count"]), int(k["legal"]))
    if len(set(v[2] for v in batch_keys.values())) != len(batch_keys):
        fail("batch keys collide on s5 indices")

    # --- independent two-pass raw re-verification of ALL 54 probed keys ------
    # (second implementation of the maker's row gate; trusts neither maker nor
    #  row audit; the adopted keys must be LOSS, aa003 must match its Part CH
    #  adoption, the 35 WIN keys are honest labels, the 11 EXHAUSTED keys are
    #  honest UNKNOWN budget-exhaustions)
    adopted_nodes_sum = 0
    cross_drive_rows = {}
    for kid, (lo, hi, s5i, _m, bk_legal) in sorted(batch_keys.items()):
        rows_raw = []
        for tag in ("p1", "p2"):
            rows_raw.append(parse_raw(D5_DIR / f"output/raw/{kid}.{tag}.out", tag, kid))
        p1, p2 = rows_raw
        if p1 != p2:
            fail(f"{kid} two-pass mismatch (node-exact gate): {p1} vs {p2}")
        stones, legal, is_or, budget, result, nodes, klo, khi = p1
        if stones != 5 or is_or != 0 or budget != BUDGET:
            fail(f"{kid} raw depth/budget drift: {p1}")
        if (klo, khi) != (lo, hi) or legal != bk_legal:
            fail(f"{kid} raw key/legal != batch-keys")
        if kid in ADOPTED:
            a = ADOPTED[kid]
            if result != 2 or nodes != a["nodes"] or legal != a["legal"] or s5i != a["s5"]:
                fail(f"{kid} raw record != the published adopted LOSS row: {p1}")
            adopted_nodes_sum += nodes
        elif kid == "aa003":
            if result != 2 or nodes != AA003["nodes"] or s5i != AA003["s5"]:
                fail(f"aa003 raw record != its Part CH adoption: {p1}")
        elif kid in win_by_kid:
            w = win_by_kid[kid]
            if result != 1:
                fail(f"{kid} raw result {result} is not the published honest WIN label 1")
            if nodes != w["nodes"] or s5i != w["s5"]:
                fail(f"{kid} raw nodes/s5 != the published honest WIN label")
        else:
            e = exh_by_kid[kid]
            if result != 0 or nodes != BUDGET:
                fail(f"{kid} raw record is not the published budget exhaustion: {p1}")
            if s5i != e["s5"]:
                fail(f"{kid} EXHAUSTED s5 drift")
    if adopted_nodes_sum != ADOPTED_TOTAL_NODES:
        fail(f"adopted raw node sum {adopted_nodes_sum} != pinned total {ADOPTED_TOTAL_NODES}")
    # cross-drive raw equality for the 6 adopted keys probed on drive-4 too
    for kid in D4_ADOPTED_PRESENT:
        for tag in ("p1", "p2"):
            r4 = parse_raw(D4_DIR / f"output/raw/{kid}.{tag}.out", f"d4-{tag}", kid)
            r5 = parse_raw(D5_DIR / f"output/raw/{kid}.{tag}.out", f"d5-{tag}", kid)
            if r4 != r5:
                fail(f"{kid} cross-drive raw mismatch on pass {tag}")
            cross_drive_rows[kid] = list(r5)
    if not (D4_DIR / "output/raw/aa036.p1.out").exists():
        pass  # aa036 is drive-5 only (drive-4 halted at aa031)

    # --- increment gates ------------------------------------------------------
    incr = read_cache(INCR_CACHE)
    if len(incr) != ADOPTED_ROWS:
        fail(f"increment row count {len(incr)} != {ADOPTED_ROWS}")
    if any(v[0] != 2 for v in incr.values()):
        fail("increment contains a non-LOSS verdict")
    if set(incr) != {ADOPTED[k]["key"] for k in ADOPTED_IDS}:
        fail("increment keys != exactly the 7 adopted LOSS keys")
    for kid in ADOPTED_IDS:
        a = ADOPTED[kid]
        row = incr.get(a["key"])
        if row is None or row != (2, a["nodes"]):
            fail(f"increment row for {kid} != the adopted verdict: {row}")
    if incr.get(AA003["key"]) is not None:
        fail("aa003 re-emitted into the loss-7 increment (Part CH already adopted it)")
    for w in WINS:
        if incr.get(w["key"]) is not None:
            fail(f"{w['kid']} WIN row leaked into the increment (adoption gate)")
    for e in EXHAUSTED:
        if incr.get(e["key"]) is not None:
            fail(f"{e['kid']} EXHAUSTED row leaked into the increment (honest UNKNOWN gate)")

    base_cache = read_cache(BASE_CACHE)
    scen_cache = read_cache(SCEN_CACHE)
    for kid, (lo, hi, s5i, _m, _lg) in batch_keys.items():
        fresh = kid in ADOPTED_IDS
        if fresh and (lo, hi) in base_cache:
            fail(f"{kid} already present in the BASE cache (not a fresh increment)")
        if s5i in receipt_verdicts:
            fail(f"{kid} already resolved by the update8 receipt")
    if base_cache.get(AA003["key"]) != (2, AA003["nodes"]):
        fail("aa003 not present in BASE with its Part CH verdict (2, 4070373)")
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
    if base_votes.get(1, 0) != 158 or base_votes.get(2, 0) != 6136:
        fail(f"BASE cache verdict counts not 158 WIN / 6136 LOSS: {dict(sorted(base_votes.items()))}")
    if scen_votes.get(1, 0) != 158 or scen_votes.get(2, 0) != 6143:
        fail(f"scenario cache verdict counts not 158 WIN / 6143 LOSS: {dict(sorted(scen_votes.items()))}")
    for w in WINS:
        if w["key"] in base_cache:
            fail(f"{w['kid']} WIN key already in BASE (fresh-increment gate)")
        if w["key"] in scen_cache:
            fail(f"{w['kid']} WIN key reached the scenario canonical cache (must stay unconsumed)")
    for e in EXHAUSTED:
        if e["key"] in base_cache:
            fail(f"{e['kid']} EXHAUSTED key already in BASE (fresh-increment gate)")
        if e["key"] in scen_cache:
            fail(f"{e['kid']} EXHAUSTED key reached the scenario canonical cache (honest UNKNOWN)")

    # --- graph holders of the adopted keys -----------------------------------
    holders = {}
    for kid in ADOPTED_IDS:
        lo, hi, s5i, mcnt, _lg = batch_keys[kid]
        hs = sorted(i for i, c in enumerate(s4_cost) if s5i in c)
        if B28_CLASS not in hs:
            fail(f"{kid} own batch class {B28_CLASS} not among its graph holders {hs}")
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
    incr_index = {}
    for kid in ADOPTED_IDS:
        incr_index[ADOPTED[kid]["s5"]] = ADOPTED[kid]["key"]
    if set(incr_index) != set(NEWLY_RESOLVED_S5):
        fail("adopted s5 index set != the pinned newly-resolved set")

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
    if base_summary["inputs"]["cache_rows"] != 6294 or scen_summary["inputs"]["cache_rows"] != 6301:
        fail("published cache_rows not 6294 -> 6301")

    # --- global status-transition gate ----------------------------------------
    transitions = Counter()
    for i in range(len(s4_masks)):
        b, s = base_st[i], scen_st[i]
        transitions[f"{b}->{s}"] += 1
        if s not in ALLOWED_TRANSITIONS.get(b, []):
            fail(f"class {i} forbidden transition {b} -> {s}")

    # --- excluded_now flips must be empty for a zero-WIN increment -----------
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

    # --- per-class arithmetic gates --------------------------------------------
    cls = B28_CLASS
    if cls in new_free:
        fail(f"class {cls} must NOT free: its 35 WIN children stay unconsumed, so "
             "unknown cost children remain and the class stays unknown")
    if scen_st[cls] != "unknown":
        fail(f"class {cls} scenario status {scen_st[cls]} != unknown (WIN stays unconsumed)")
    basec = sorted(base_unknown[cls])
    if len(basec) != 53:
        fail(f"class {cls} BASE-unknown cost children {len(basec)} != 53 (54 minus Part CH aa003)")
    own_class_incr = sorted(j for j in incr_index if j in s4_cost[cls])
    if not set(own_class_incr) <= set(basec):
        fail(f"class {cls}: increment s5 indices not all BASE-unknown cost children of the class")
    if len(own_class_incr) != 7:
        fail(f"class {cls}: own increment membership {len(own_class_incr)} != 7")
    leftover = sorted(set(basec) - set(own_class_incr))
    if len(leftover) != 46:
        fail(f"class {cls} leftover BASE-unknown children {len(leftover)} != 46")
    if sorted(scen_unknown[cls]) != leftover:
        fail(f"class {cls} scenario-unknown children != leftover arithmetic")
    batch_s5 = {v[2] for v in batch_keys.values()}
    if batch_s5 != set(basec) | {AA003["s5"]}:
        fail(f"class {cls}: batch key set != the 53 BASE-unknown cost children plus aa003")
    win_s5 = sorted(w["s5"] for w in WINS)
    if sorted(set(win_s5) | {e["s5"] for e in EXHAUSTED}) != leftover:
        fail(f"class {cls}: leftover 46 != exactly the 35 WIN + 11 EXHAUSTED s5 indices")
    if set(win_s5) & set(own_class_incr):
        fail("class {cls}: a WIN s5 index was adopted (forbidden)")
    class_rows = {str(cls): {
        "class_index": cls, "batch": 28,
        "base_unknown_children": len(base_unknown[cls]),
        "adopted_by_increment": len(own_class_incr),
        "leftover_unknown_children": len(leftover),
        "scenario_unknown_children": len(scen_unknown[cls]),
        "scenario_status": scen_st[cls],
        "leftover_is_exactly_win_plus_exhausted": True,
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
        if c == cls and len(own) != 7:
            fail("holder class 5343 must hold exactly the 7 adopted memberships")
        holder_rows[str(c)] = row

    # --- published metric table and pinned deltas ------------------------------
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
        fail("free_now class count must not change in a loss-only non-closing adoption")
    if metrics["update8_resolved_count"]["delta"] != 7:
        fail("update8 resolved-count delta != 7")
    if metrics["update8_remaining_now"]["delta"] != -7:
        fail("update8 remaining delta != -7")
    if metrics["probe_worklist_total"]["delta"] != 82:
        fail("probe worklist delta != +82 (declared machine-observed)")
    if metrics["joint_greedy_union_size"]["delta"] != 15:
        fail("joint greedy union delta != +15 (declared machine-observed)")
    if metrics["closure_classes_count"]["delta"] != 1:
        fail("closure classes count delta != +1")
    for k in ("update8_win_hit_groups", "update8_groups_free_now",
              "joint_greedy_unique_groups", "group_best_options_nonfree"):
        if metrics[k]["delta"] != 0:
            fail(f"metric {k} must stay unchanged for a zero-WIN adoption")

    # --- update8 resolved-requirement delta, gated to the increment ----------
    base_resolved = set(base_summary["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    scen_resolved = set(scen_summary["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    lost = sorted(base_resolved - scen_resolved)
    if lost:
        fail(f"update8 resolutions lost: {lost}")
    newly_resolved = sorted(scen_resolved - base_resolved)
    if newly_resolved != NEWLY_RESOLVED_S5:
        fail(f"newly resolved s5 {newly_resolved} != the pinned 7 adopted s5 indices")
    for j in newly_resolved:
        lo, hi = incr_index[j]
        if incr[(lo, hi)][0] != 2:
            fail(f"newly resolved s5 {j} increment row is not LOSS")

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
    # individual greedy union movers: exactly roots 4 / 16 / 49 with pinned values
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
        if row["delta"] > 0:
            fail(f"per-root greedy delta for root {first} must be <= 0: {row}")
        if row["delta"] != 0 and first not in PRG_MOVERS_PIN:
            fail(f"per-root greedy mover root {first} not in the declared mover set")
        if first in PRG_MOVERS_PIN:
            if (row["base_greedy_union_size"], row["scenario_greedy_union_size"]) != PRG_MOVERS_PIN[first]:
                fail(f"per-root greedy values for root {first} {row} != declared pin")
            if row["base_free_thirds"] != row["scenario_free_thirds"]:
                fail(f"per-root greedy free thirds changed for root {first} (no class freed)")
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
            "status_distribution": {"unknown": 428, "excluded_now": 3},
            "gate": ("every churned class with stable unknown_now is pure ranking "
                     "bookkeeping: recomputed status UNCHANGED between BASE and "
                     "scenario (428 unknown + 3 excluded_now, all pre-existing on "
                     "both sides), none of them a holder of the adopted keys"),
        },
        "anchors": {},
    }
    if (len(base_cc), len(scen_cc)) != CLOSURE_COUNTS:
        fail(f"closure table counts {(len(base_cc), len(scen_cc))} != pinned {CLOSURE_COUNTS}")
    b_full = {int(r["class_index"]): r for r in base_cc}
    s_full = {int(r["class_index"]): r for r in scen_cc}
    base_idx = set(b_full)
    scen_idx = set(s_full)

    # class 5343: unknown_now 53 -> 46 (rank 19 -> 4)
    cls_row_pin = CLASS_5343_CLOSURE_PIN
    if int(b_full[cls]["unknown_now"]) != cls_row_pin[0][1] or int(b_full[cls]["class_rank"]) != cls_row_pin[0][0]:
        fail(f"BASE closure row for class 5343 unexpected: {b_full[cls]}")
    if int(s_full[cls]["unknown_now"]) != cls_row_pin[1][1] or int(s_full[cls]["class_rank"]) != cls_row_pin[1][0]:
        fail(f"scenario closure row for class 5343 unexpected: {s_full[cls]}")
    closure_rows["classes"][str(cls)] = {
        "base_rank": cls_row_pin[0][2 - 2], "base_unknown_now": cls_row_pin[0][1],
        "scenario_rank": cls_row_pin[1][0], "scenario_unknown_now": cls_row_pin[1][1],
    }

    inter = base_idx & scen_idx
    changed_unknown = sorted(c for c in inter
                             if int(b_full[c]["unknown_now"]) != int(s_full[c]["unknown_now"]))
    if changed_unknown != sorted([cls] + list(CHANGED_UNKNOWN_CLOSURE_PIN)):
        fail(f"closure unknown_now changes {changed_unknown} != class 5343 + the pinned "
             f"holder classes {sorted(CHANGED_UNKNOWN_CLOSURE_PIN)}")
    for c in changed_unknown:
        own = sorted(j for j in incr_index if j in s4_cost[c])
        if c not in holder_union:
            fail(f"closure class {c} changed unknown_now but is not a holder of the "
                 "adopted keys")
        if int(b_full[c]["unknown_now"]) - len(own) != int(s_full[c]["unknown_now"]):
            fail(f"closure class {c} unknown_now arithmetic drift: "
                 f"{b_full[c]['unknown_now']} - {len(own)} != {s_full[c]['unknown_now']}")
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
    if dict(churn_status_dist) != {"unknown": 428, "excluded_now": 3}:
        fail(f"stable-unknown churn status distribution {dict(churn_status_dist)} != "
             "declared pin {'unknown': 428, 'excluded_now': 3}")

    # untouched anchor classes: fully stable rows
    for anchor, pin in CLOSURE_ANCHORS_PIN.items():
        if (int(b_full[anchor]["class_rank"]), int(b_full[anchor]["unknown_now"])) != pin \
                or (int(s_full[anchor]["class_rank"]), int(s_full[anchor]["unknown_now"])) != pin:
            fail(f"anchor class {anchor} closure-row drift (must stay "
                 f"rank/unknown {pin} in both tables)")
        closure_rows["anchors"][str(anchor)] = {
            "base_rank": pin[0], "scenario_rank": pin[0], "unknown_now": pin[1],
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
    for c in entered:
        pin = CLOSURE_ENTERED_PIN[c]
        if (int(s_full[c]["class_rank"]), int(s_full[c]["unknown_now"])) != pin:
            fail(f"entered class {c} scenario row != declared pin {pin}")
        if scen_st.get(c) != "unknown":
            fail(f"entered class {c} must be recomputed unknown (pure ranking bookkeeping)")
    closure_rows["left_table_classes"] = [{"class_index": c,
                                           "base_row": list(CLOSURE_LEFT_PIN[c])} for c in left]
    closure_rows["entered_table_classes"] = [{"class_index": c,
                                              "scenario_row": list(CLOSURE_ENTERED_PIN[c])} for c in entered]

    # --- output --------------------------------------------------------------
    out = {
        "schema": "n11-b28loss7-adoption-decomp-deltas-v1",
        "scenario": ("ADOPTED-CANONICAL = pre-adoption BASE (Part CH canonical state, "
                     "6,294 rows, 3124461b...) + the 7 fresh LOSS rows of batch-28 "
                     "(class 5343; aa015/aa017/aa018/aa023/aa024/aa029/aa036; nodes "
                     "total 38,784,669); full != loss: the fully-probed packet "
                     "additionally holds 35 WIN rows (aa001/aa002 Part CC "
                     "cross-verified, aa006/aa007 Part CG lane declared with the "
                     "d5e9acc2 takeover pending output, aa008/aa009 Part CM "
                     "cross-verified, 29 further honest labels) which stay UNCONSUMED "
                     "(scrutiny owner C++ second-implementation gate pin 9193f5b6...; "
                     "batch-14residual q042 / batch-26 l028 precedents), the 11 "
                     "EXHAUSTED rows stay honest UNKNOWN, aa003 was already adopted "
                     "by Part CH and is asserted BASE-consistent; class 5343 does "
                     "not free (46 leftover = 35 WIN + 11 EXHAUSTED)"),
        "interpretation_guard": ("canonical 7-row adoption deltas: only the 7 fresh "
                                 "LOSS rows are consumed into the canonical cache via "
                                 "the fail-closed union merger; the 35 WIN verdicts "
                                 "are NOT consumed (unconsumed closure WIN candidates "
                                 "stay untouched); the 11 EXHAUSTED rows stay honest "
                                 "UNKNOWN; class 5343 does NOT free in this adoption; "
                                 "scheduling quantities are bookkeeping; every claim "
                                 "stays UNKNOWN; 11x11 empty board and all 19 roots "
                                 "stay UNKNOWN; nodes are bookkeeping"),
        "recompute_gates": ("class statuses with Board free-candidate child "
                            "verification, known-universe counts and per-root free "
                            "coverage were recomputed from graph + update8 + cache and "
                            "asserted equal to the published BASE (Part CH reaudit) and "
                            "scenario outputs before any delta was emitted"),
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
            "drive4_row_audit_sha256": D4_ROW_AUDIT_SHA,
            "drive5_row_audit_sha256": D5_ROW_AUDIT_SHA,
            "drive4_status_log_sha256": D4_STATUS_SHA,
            "drive5_status_log_sha256": D5_STATUS_SHA,
            "drive4_kit_manifest_sha256": D4_KIT_MANIFEST_SHA,
            "drive5_kit_manifest_sha256": D5_KIT_MANIFEST_SHA,
        },
        "kit_integrity": kit_info,
        "status_log": status_log_info,
        "batch_keys": {
            "count": len(batch_keys), "adopted_loss": 7, "unadopted_win": 35,
            "exhausted_excluded": 11, "b28_class": B28_CLASS,
            "b28_keys": 54, "b28_probed": 54, "b28_fragments": 0,
            "b28_class_mask": list(s4_masks[B28_CLASS]),
            "b28_cost_children_total": len(s4_cost[B28_CLASS]),
            "b28_groups_served": [list(x) for x in groups_served],
            "cross_drive_identical_adopted_raws": sorted(cross_drive_rows),
            "aa036_drive5_only": True,
        },
        "excluded_now_flips": flips,
        "newly_free_now_classes": new_free,
        "newly_free_now_gate": ("the loss-only packet can only free classes whose "
                               "BASE-unknown children are ALL resolved by the "
                               "increment; machine-computed list is empty here; class "
                               "5343 does NOT free (its 35 WIN children and the 11 "
                               "EXHAUSTED keys stay unconsumed/honest-UNKNOWN)"),
        "status_transitions": dict(sorted(transitions.items())),
        "class_rows": class_rows,
        "adopted_rows": [
            {"key_id": kid, "s5_index": a["s5"], "key": [a["key"][0], a["key"][1]],
             "legal": a["legal"], "nodes": a["nodes"], "consumed": True,
             "note": ("two-pass node-exact LOSS row adopted into the canonical chain "
                      "via the pinned fail-closed merger 90711961003...; drive-4/"
                      "drive-5 cross-identical raw where probed on both")}
            for kid, a in ((k, ADOPTED[k]) for k in ADOPTED_IDS)],
        "already_adopted": {
            "key_id": "aa003", "s5_index": AA003["s5"],
            "key": [AA003["key"][0], AA003["key"][1]],
            "legal": AA003["legal"], "nodes": AA003["nodes"],
            "adopted_by": "Part CH (base cache 6,294 rows 3124461b...)",
            "re_emitted": False,
            "base_consistency_asserted": True,
        },
        "unadopted_win_rows": [
            {"key_id": w["kid"], "s5_index": w["s5"], "key": [w["key"][0], w["key"][1]],
             "legal": w["legal"], "result": 1, "nodes": w["nodes"], "consumed": False,
             "note": ("honest WIN label only; adopted nowhere; stays unconsumed with "
                      "the unconsumed closure WIN candidates; scrutiny owner C++ "
                      "second-implementation gate pin 9193f5b6... decides; "
                      + w["cross"])}
            for w in WINS],
        "exhausted_rows": [
            {"key_id": e["kid"], "s5_index": e["s5"],
             "key": [e["key"][0], e["key"][1]],
             "legal": e["legal"], "result": 0, "nodes": BUDGET, "consumed": False,
             "probed": True,
             "note": ("budget exhaustion at 15M on both passes; honest UNKNOWN; "
                      "same-condition re-probe not performed; adopted nowhere; the "
                      "truncated sidecars were re-run fresh-cold by the completeness "
                      "guard")}
            for e in EXHAUSTED],
        "fragment_rows": [],
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
    print("OK decomp-deltas-b28loss7-adoption.json: "
          f"flips={flips} new_free={new_free} "
          f"free_now {metrics['free_now_classes']['base']}->{metrics['free_now_classes']['scenario']} "
          f"class5343_unknown {len(base_unknown[cls])}->{len(scen_unknown[cls])} "
          f"rank {closure_rows['classes'][str(cls)]['base_rank']}->{closure_rows['classes'][str(cls)]['scenario_rank']} "
          f"(35 WIN unconsumed + 11 EXHAUSTED honest UNKNOWN) "
          f"update8_resolved +{len(newly_resolved)} "
          f"joint_greedy {metrics['joint_greedy_union_size']['base']}->{metrics['joint_greedy_union_size']['scenario']} "
          f"worklist {metrics['probe_worklist_total']['base']}->{metrics['probe_worklist_total']['scenario']} "
          f"kits={kit_info['drive4']['files_verified']}+{kit_info['drive5']['files_verified']} "
          f"changed_rows={sorted(changed_rows)} "
          f"ig_movers={sorted(greedy_moved_rows)} "
          f"closure_left={left} closure_entered={entered}")


if __name__ == "__main__":
    main()
