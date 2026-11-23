"""Batch-29 scaffold keys maker: closure class 2251 (Part CI, 2026-11-23).

Fail-closed, read-only generation of the batch-29 probe packet declared as
Part CI (published as research/log/2026-11-23-part-ci-batch29-declaration.md
before any probe execution; single owner: n11 central-reply lane).
Target class: graph class index 2251, mask [1155314042043105280, 0], rank 35
under the Part CH adopted base (6,294-row merged canonical cache
3124461b..., containing the batch-28 aa003 LOSS row on top of the Part BZ
6,293-row cache) PLUS the published update8 receipts.

SELECTION STATE (machine facts re-derived in this session, pre-registered in
the Part CI declaration): under the Part CH base the ranked closure table
(807 rows) matches the published Part CH reaudit closure-classes.csv
(baa2db13...) exactly; ranks 1..34 are each either refuted/route-dead
(unconsumed-WIN intersection exactly as pinned below, or a known receipt
WIN cost child) or packet-collision blocked (colliding keys exactly as
pinned); rank 35 class 2251 is the FIRST clean candidate: unknown_now 54
(all of its cost set), no known WIN cost child, zero packet-key collision
against all 29 published packets (1,460 rows), zero quarantine hit,
groups exactly [(37, 81)].  Runner-up: rank 36 class 34269 (clean; zero
collision).  Rank 37 class 34948 is packet-collision blocked (1 key).

KEY ID PREFIX (continuation of the 2-letter design): batch-28 introduced
the two-letter prefix (aa001..aa054); batch-29 uses ab001..ab054.  Gates:
every published packet key id matches ^[a-z][0-9]{3}$ (1-letter) or starts
with "aa" (batch-28), and NO published key id starts with "ab".

Base-independence statement: the base of this maker is the PUBLISHED
Part CH adopted canonical exact-S5 verdict cache (6,294 rows, sha256
3124461b14e4f73a7248cbf5b96c7ff59ebfdcc05258adeb9c81791d86cc461e) PLUS the
published update8 receipts (b658290a...).  The 54 probed children of class
2251 are byte-derived from the pinned dependency graph + that adopted cache
+ those receipts; no unpublished artifact (probe worklist etc.) is read.

Gates (fail-closed; every value below is a pin that the derived state must
match exactly, or the maker fails):
  * sha256 pins: graph, update8, Board, evidence policy, quarantine,
    canonical BASE cache (Part CH merged 6,294 rows), published closure table
    (Part CH reaudit, 807 rows), and the 29 published batch key packets
    (batches 1..28 + batch-14 residual, fetched from repo raw and
    sha-pinned);
  * class gate: mask match, graph status unknown(1), cost size 54,
    groups served exactly [(37, 81)];
  * adoption ties (machine-pinned, not trusted from prose):
    - batch-20: all 53 published x-keys are LOSS(2) rows of the base, and
      class 12457 has zero unknown children;
    - Part BZ: the 6 published keys batch-24 y002/y004 (s5 166253/272083)
      and batch-27 o001/o003/o005/o007 (s5 98526/250515/348664/416288) are
      LOSS(2) rows of the base; class 16957 has exactly 51 unknown and
      class 13342 exactly 50;
    - Part CH: batch-28 aa003 (s5 104943) is a LOSS(2) row of the base and
      is NOT in the prior packets' probe evidence; class 5343 has exactly
      53 unknown children;
  * closure re-derivation: the re-derived ranked closure table (best-class
    groups over central roots) must agree with the published Part CH
    reaudit closure table on all 807 (rank -> class, unknown) pairs, and
    with the pinned EXPECTED_RANKS 1..40;
  * selection classification pins (this is the batch-29 selection core):
    for every rank 1..34, the derived state must match the pinned
    classification exactly - REFUTED (unconsumed-WIN intersection %in)
    exactly the pinned s5 set, or ROUTE-DEAD (known WIN cost child) exactly
    the pinned set, or PKT-SKIP (unknown keys colliding with published
    packet positions) exactly the pinned s5 set; ranks 35 and 36 must be
    CLEAN (no WIN intersection, no known WIN child, zero collision);
  * target gates: 0/54 hits in the 6,294-row base; quarantine 0/54;
    canonical-safe key form 54/54; mask_to_index == derived s5 index 54/54;
    every key is a graph cost child of 2251; Board recomputes legal-move
    popcount 54/54; membership_class_count re-derived from the graph cost
    relation 54/54; every key DISJOINT from all 29 published packet key
    positions; unconsumed WIN 33-set intersection 0;
  * runner-up gate: class 34269 has no known WIN child, no WIN-33
    intersection, zero packet collision, groups exactly [(12, 108)], and
    rank 36.

Outputs: input/batch-keys.json (schema
n11-centralreply-closure-class2251-batch29-input-v1, key ids ab001..ab054)
and input/abNNN.input.csv (54 single-row target CSVs for the pinned
runner). Standard 11x11, all 19 central-reply roots, class 2251 and every
key stay UNKNOWN; nodes are bookkeeping, never verdicts.
"""

import csv
import gzip
import hashlib
import json
import sys
import urllib.request
from collections import Counter
from pathlib import Path

_here = Path(__file__).resolve()
_CANDS = [q for q in _here.parents if (q / "research" / "experiments").is_dir()]
if not _CANDS:
    raise SystemExit("GATE FAILED: repo root not found above this script")
ROOT = _CANDS[0]
EXP = _here.parents[1]
OUTDIR = EXP / "input"

GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
CH_DIR = ROOT / "research/experiments/n11-centralreply-class5343-loss1-adoption-reaudit-20261123"
BASE_CACHE = CH_DIR / ("output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-"
                        "plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-plus-batch20loss53-"
                        "plus-batch26loss52-plus-batch24loss2-plus-batch27loss4-plus-batch28loss1-20261123.cache")
PUBLISHED_CLOSURE = CH_DIR / "reaudit/output/closure-classes.csv"

CLASS_INDEX = 2251
CLASS_MASK = [1155314042043105280, 0]
CLASS_RANK = 35      # under the adopted 6,294-row base (published Part CH table)
COST_SIZE = 54
UNPROBED = 54
KNOWN_CHILDREN = {}   # class 2251 has NO base-resolved cost child
CLASS_GROUPS = [(37, 81)]
RUNNER_UP_CLASS = 34269       # rank 36
RUNNER_UP_GROUPS = [(12, 108)]
BACKUP_CLASSES = []            # rank 37 class 34948 is pkt-blocked (pin below)
BUDGET = 15000000
CANONICAL_ROWS = 6294          # Part CH merged cache
CANDIDATE_ROWS = 807           # published Part CH closure table rows
KEY_PREFIX = "ab"
PRIOR_KEYID_RE_STR = r"^[a-z][0-9]{3}$"

WIN33 = [
    ("b018", "n11-centralreply-closure-class16757-batch-20261122", 528497),
    ("d002", "n11-centralreply-closure-class20421-batch-20261122", 197253),
    ("e002", "n11-centralreply-closure-class16371-batch4-20261122", 183566),
    ("f017", "n11-centralreply-closure-class12264-batch5-20261122", 415095),
    ("g018", "n11-centralreply-closure-class5473-batch6-20261122", 184684),
    ("h045", "n11-centralreply-closure-class2634-batch8-20261122", 103558),
    ("j033", "n11-centralreply-closure-class1518-batch9-20261122", 69347),
    ("z003", "n11-centralreply-closure-class8785-batch11-20261122", 198530),
    ("n005", "n11-centralreply-closure-class8106-batch12-20261122", 188395),
    ("n006", "n11-centralreply-closure-class8106-batch12-20261122", 219608),
    ("p002", "n11-centralreply-closure-class16930-batch13-20261122", 185003),
    ("p003", "n11-centralreply-closure-class16930-batch13-20261122", 203419),
    ("r001", "n11-centralreply-closure-class5830-batch15-20261122", 103560),
    ("r002", "n11-centralreply-closure-class5830-batch15-20261122", 103561),
    ("q042", "n11-centralreply-closure-class23101-batch14-20261122", 745184),
    ("v001", "n11-centralreply-closure-class16131-batch18-20261122", 153671),
    ("v002", "n11-centralreply-closure-class16131-batch18-20261122", 207534),
    ("w001", "n11-centralreply-closure-class16513-batch19-20261123", 63802),
    ("w002", "n11-centralreply-closure-class16513-batch19-20261123", 109169),
    ("a003", "n11-centralreply-closure-class12643-batch21-20261123", 115192),
    ("k002", "n11-centralreply-closure-class25835-batch22-20261123", 150241),
    ("s001", "n11-centralreply-closure-class31600-batch23-20261123", 62435),
    ("s002", "n11-centralreply-closure-class31600-batch23-20261123", 192809),
    ("y001", "n11-centralreply-closure-class16957-batch24-20261123", 91296),
    ("y006", "n11-centralreply-closure-class16957-batch24-20261123", 368510),
    ("i001", "n11-centralreply-closure-class30565-batch25-20261123", 68580),
    ("i002", "n11-centralreply-closure-class30565-batch25-20261123", 191299),
    ("l028", "n11-centralreply-closure-class1849-batch26-20261123", 81011),
    ("o002", "n11-centralreply-closure-class13342-batch27-20261123", 209134),
    ("aa001", "n11-centralreply-closure-class5343-batch28-20261123", 28037),
    ("aa002", "n11-centralreply-closure-class5343-batch28-20261123", 87306),
    ("aa006", "n11-centralreply-closure-class5343-batch28-20261123", 129823),
    ("aa007", "n11-centralreply-closure-class5343-batch28-20261123", 135236),
]
WIN_COUNT = 33

BATCH20_PACKET = "n11-centralreply-closure-class12457-batch20-20261123"
BATCH20_X_KEYS = 53
BZ_ADOPTED_CLASS = 16957
BZ_ADOPTED_CLASS_UNKNOWN = 51
BZ_ADOPTED_CLASS27 = 13342
BZ_ADOPTED_CLASS27_UNKNOWN = 50
BZ_ADOPTED_KEYS = [
    ("y002", "n11-centralreply-closure-class16957-batch24-20261123", 166253),
    ("y004", "n11-centralreply-closure-class16957-batch24-20261123", 272083),
    ("o001", "n11-centralreply-closure-class13342-batch27-20261123", 98526),
    ("o003", "n11-centralreply-closure-class13342-batch27-20261123", 250515),
    ("o005", "n11-centralreply-closure-class13342-batch27-20261123", 348664),
    ("o007", "n11-centralreply-closure-class13342-batch27-20261123", 416288),
]
CH_ADOPTED_KEY = ("aa003", "n11-centralreply-closure-class5343-batch28-20261123", 104943)
CH_ADOPTED_CLASS = 5343
CH_ADOPTED_CLASS_UNKNOWN = 53

# 29 published key packets (raw main, sha256-pinned): batches 1..28 + residual
PRIOR_BATCHES = [
    ("n11-centralreply-closure-class16757-batch-20261122", 48,
     "2aaccc941d7aec35c416b27d5cdd10f7fbb82c9801bcf560b61e20be88c331f8"),
    ("n11-centralreply-closure-class23963-batch-20261122", 48,
     "3b37c92387336407d6399a689befb2fad99e01520a390294a2370daa11e631e3"),
    ("n11-centralreply-closure-class20421-batch-20261122", 49,
     "ad05073a845e511669d28fde3691fe9f3bf9f08eef2021039c884f1411f6dd3f"),
    ("n11-centralreply-closure-class16371-batch4-20261122", 50,
     "70b8a4c89f7cea454bfd2b52f720245b6d9c5d7311878bf8aac637940825ecdf"),
    ("n11-centralreply-closure-class12264-batch5-20261122", 51,
     "57da4702161ab781350ebf4236791266b31bdcd78b017eaa6e4a9391ecf5451d"),
    ("n11-centralreply-closure-class5473-batch6-20261122", 51,
     "c16d36e041da855ab654841f25d2bf5a64fb9ce4a2c1fde75e1217c7b082c59e"),
    ("n11-centralreply-closure-class10324-batch7-20261122", 51,
     "91d0f49254652cbc282cb8869b50d918ae16084c1bba1dcfcb725e15d7a3d434"),
    ("n11-centralreply-closure-class2634-batch8-20261122", 51,
     "5c42a950c687bbd1b8a9e25b1fdd5cffb4b7a19565a3d4372173a2001fcccc02"),
    ("n11-centralreply-closure-class1518-batch9-20261122", 51,
     "8f2035d17b3c987c8e5c848b23b6849ad5f3508a51d64002c1fef0e8c5ed7e9e"),
    ("n11-centralreply-closure-class8784-batch10-20261122", 52,
     "a1401ee2769f3943f993527dd4934ce82e99c6d55ee27a13cf74b1b417148ebf"),
    ("n11-centralreply-closure-class8785-batch11-20261122", 51,
     "8ef2206986a87f3859aa0a4b25f9936ffa82001d1fd3214013dc6351ecf8b08b"),
    ("n11-centralreply-closure-class8106-batch12-20261122", 52,
     "de55df83483663e31b1c1db0fb8a1239079e7152bddef9bd893439b7b2fdbdc2"),
    ("n11-centralreply-closure-class16930-batch13-20261122", 52,
     "c6c56a1a0552b8a87d1e1f5f9e0d6c3955cf1f58a85ef6726317d17846a0a2c7"),
    ("n11-centralreply-closure-class23101-batch14-20261122", 52,
     "dfde0e90b75fd261b51ef746fe69a16eb182a99f5d2f8e1ff8bfa6efe936d71f"),
    ("n11-centralreply-closure-class5830-batch15-20261122", 52,
     "af3e4c46af0d84bcb248c350283b07e26b901f6e0d196038e24bd1292b133727"),
    ("n11-centralreply-closure-class10687-batch16-20261122", 52,
     "465cf44721a661ce94babe12212c26c697ebb346392548fcdafaa9d3e8c3dd4e"),
    ("n11-centralreply-closure-class10661-batch17-20261122", 52,
     "db762175272206aa53622f30addc1267d534e8a3e576f70c6a084f21392645d2"),
    ("n11-centralreply-closure-class23101-batch14-residual-20261122", 10,
     "d4fada6801173499750d1739bf7aee45cbd01eab316e11b210436f8bb1f94121"),
    ("n11-centralreply-closure-class16131-batch18-20261122", 53,
     "1bb3ed41b26af92491ed579a7c05471f271ed1394d8b5f817b5110794d926667"),
    ("n11-centralreply-closure-class16513-batch19-20261123", 53,
     "9609aaf3116f2ba80c206ae66b09249af1855d509d17be588911e6ab72e53d50"),
    (BATCH20_PACKET, 53,
     "efb40b1bb7a43595bb8d014a31af2b878c404be86b8f9d5abc717eb176d1ed51"),
    ("n11-centralreply-closure-class12643-batch21-20261123", 53,
     "1f9346a7027e95b162f27b933bddec05151473d87ab7ed35832619026ae6759d"),
    ("n11-centralreply-closure-class25835-batch22-20261123", 53,
     "b5f567bd72835ebfe347d7363f3d244565757deb8e8572b6fb2820625ae39035"),
    ("n11-centralreply-closure-class31600-batch23-20261123", 53,
     "2776acafbb638cb148661b3988b7eb36bc8519e5b7b75b415b01618bfcb85bf7"),
    ("n11-centralreply-closure-class16957-batch24-20261123", 53,
     "486858d6e2de0662ef38a6ff1fd61c1c0dcf6e9b09012c2c32fdd99153d096cc"),
    ("n11-centralreply-closure-class30565-batch25-20261123", 53,
     "272c0c134e3be17838311d0d3f18f09340d09094d35e15197481c999892390a5"),
    ("n11-centralreply-closure-class1849-batch26-20261123", 53,
     "f1ea43aef6ee06c918885a9007ad3f347d96aa198180e87bf3eb14d783304cdd"),
    ("n11-centralreply-closure-class13342-batch27-20261123", 54,
     "67814ed6287d68d6e97212c931dce2b7ee585219e20b4d43edb621632220a014"),
    ("n11-centralreply-closure-class5343-batch28-20261123", 54,
     "af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5"),
]
EXPECTED_PRIOR_ROWS = 1460
EXPECTED_PRIOR_UNIQUE = 1446

# ranked closure rows 1..40 under the Part CH base (published table)
EXPECTED_RANKS = [
    (1, 23101, 1), (2, 1849, 1), (3, 16757, 29), (4, 20421, 49),
    (5, 16371, 49), (6, 13342, 50), (7, 30345, 50), (8, 12264, 51),
    (9, 5473, 51), (10, 16957, 51), (11, 2634, 51), (12, 8785, 51),
    (13, 1518, 51), (14, 8106, 52), (15, 16930, 52), (16, 5830, 52),
    (17, 16131, 53), (18, 16513, 53), (19, 5343, 53), (20, 5687, 53),
    (21, 12643, 53), (22, 31600, 53), (23, 10968, 53), (24, 23964, 53),
    (25, 25835, 53), (26, 30565, 53), (27, 5690, 53), (28, 13758, 54),
    (29, 14103, 54), (30, 30484, 54), (31, 34263, 54), (32, 16901, 54),
    (33, 19749, 54), (34, 23482, 54), (35, 2251, 54), (36, 34269, 54),
    (37, 34948, 54), (38, 5804, 55), (39, 11490, 55), (40, 12857, 55),
]

# selection classification pins for ranks 1..34 (fail-closed):
#   ("win", class, {unconsumed-WIN intersection s5 set})  -> refuted via WIN
#   ("knownwin", class, {known WIN receipt children})     -> route-dead
#   ("winknown", class, ({win set}, {known set}))         -> refuted both ways
#   ("pkt", class, {colliding s5 set})                    -> packet skip
# ranks 35/36 are CLEAN by construction (gated in main).
SELECTION_PINS = {
    1: ("win", 23101, {745184}),
    2: ("win", 1849, {81011}),
    3: ("win", 16757, {528497}),
    4: ("win", 20421, {197253}),
    5: ("win", 16371, {183566}),
    6: ("win", 13342, {209134}),
    7: ("win", 30345, {528497}),
    8: ("win", 12264, {415095}),
    9: ("win", 5473, {184684}),
    10: ("win", 16957, {91296, 368510}),
    11: ("win", 2634, {103558, 103560, 103561}),
    12: ("win", 8785, {198530}),
    13: ("win", 1518, {69347}),
    14: ("win", 8106, {188395, 219608}),
    15: ("win", 16930, {185003, 203419}),
    16: ("winknown", 5830, ({103560, 103561}, {126017, 131631, 162106, 197665, 206386})),
    17: ("win", 16131, {153671, 207534}),
    18: ("win", 16513, {63802, 109169}),
    19: ("win", 5343, {28037, 87306, 129823, 135236}),
    20: ("knownwin", 5687, {209644}),
    21: ("win", 12643, {115192}),
    22: ("win", 31600, {62435, 192809}),
    23: ("pkt", 10968, {273033}),
    24: ("pkt", 23964, {495193, 550880}),
    25: ("win", 25835, {150241}),
    26: ("win", 30565, {68580, 191299}),
    27: ("knownwin", 5690, {209644}),
    28: ("pkt", 13758, {459528}),
    29: ("pkt", 14103, {460145}),
    30: ("pkt", 30484, {546902, 558506}),
    31: ("pkt", 34263, {528281, 553923}),
    32: ("pkt", 16901, {528689}),
    33: ("pkt", 19749, {657407}),
    34: ("pkt", 23482, {550446, 561141}),
}
# rank 37 class 34948 (behind the runner-up) is pkt-blocked; pinned for
# bookkeeping so a future batch-30 selection sees it machine-verified
RANK37_PKT_BLOCKED = (34948, {415128})

PIN_SHA = {
    "graph": "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b",
    "update8": "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719",
    "board": "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f",
    "policy": "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2",
    "quarantine": "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9",
    "canonical_base_cache": "3124461b14e4f73a7248cbf5b96c7ff59ebfdcc05258adeb9c81791d86cc461e",
    "published_closure": "baa2db136c18c681633e5bfe3b5a1dec3f084d0c696b4454ae1855ab0773e7fd",
}

RAW = "https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/main/research/experiments/"


def fail(msg):
    print("GATE FAILED: " + msg, file=sys.stderr)
    sys.exit(1)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    import re as _re
    for name, p, want in (("graph", GRAPH, PIN_SHA["graph"]),
                          ("update8", UPDATE8, PIN_SHA["update8"]),
                          ("board", BOARD_SOURCE, PIN_SHA["board"]),
                          ("policy", POLICY, PIN_SHA["policy"]),
                          ("quarantine", QUARANTINE, PIN_SHA["quarantine"]),
                          ("canonical cache", BASE_CACHE, PIN_SHA["canonical_base_cache"]),
                          ("published closure table", PUBLISHED_CLOSURE, PIN_SHA["published_closure"])):
        got = sha(p)
        if got != want:
            fail(f"{name} sha256 drift: {got} != {want}")

    sys.path.insert(0, str(BOARD_SOURCE.parent))
    sys.path.insert(0, str(POLICY.parent))
    from independent import Board
    from s5_evidence_policy import quarantined_cache_keys, is_canonical_safe_s5_key

    board = Board(11)
    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s4_masks, s4_status, s4_cost, s5_masks = g["s4_masks"], g["s4_status"], g["s4_cost"], g["s5_masks"]
    mask_to_index = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}
    membership = Counter()
    for cost in s4_cost:
        for j in cost:
            membership[j] += 1

    # class sanity
    if list(s4_masks[CLASS_INDEX]) != CLASS_MASK:
        fail(f"graph mask {s4_masks[CLASS_INDEX]} != declared class mask")
    if s4_status[CLASS_INDEX] != 1:
        fail(f"graph status of class {CLASS_INDEX} is {s4_status[CLASS_INDEX]}, not unknown(1)")
    cost_set = set(s4_cost[CLASS_INDEX])
    if len(cost_set) != COST_SIZE:
        fail(f"class cost size {len(cost_set)} != {COST_SIZE}")

    # canonical cache (published Part CH adopted output, 6,294 rows) + receipts
    update8 = json.loads(UPDATE8.read_text(encoding="utf-8"))
    if update8["schema"] != "n11-night-repaired-joint-plan-update8-v1":
        fail("update8 schema drift")
    receipts = {int(k): int(v) for k, v in update8["resolved_s5_verdicts"].items()}
    cache = {}
    with BASE_CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for lineno, r in enumerate(csv.reader(stream), 1):
            if not r or r[0].lstrip().startswith("#"):
                continue
            lo, hi, stones, verdict = int(r[1]), int(r[2]), int(r[3]), int(r[4])
            if r[0] != "s5verdict" or stones != 5 or verdict not in (1, 2):
                fail(f"invalid canonical row {lineno}")
            cache[(lo, hi)] = verdict
    if len(cache) != CANONICAL_ROWS:
        fail(f"canonical cache {len(cache)} rows != {CANONICAL_ROWS}")
    iv = {}
    for (lo, hi), v in cache.items():
        i = mask_to_index.get((lo, hi))
        if i is not None:
            iv[i] = v
    for i, v in receipts.items():
        iv[i] = v
    LOSS, UNKNOWN, EXCLUDED = 0, 1, -1
    known_win = {}
    unknown_now = {}
    for i in range(len(s4_masks)):
        base = s4_status[i]
        if base == EXCLUDED:
            unknown_now[i] = set()
            continue
        if base not in (LOSS, UNKNOWN):
            fail(f"unexpected graph status {base} at class {i}")
        unknown_now[i] = {j for j in s4_cost[i] if iv.get(j) is None}
        for j in s4_cost[i]:
            if iv.get(j) == 1:
                known_win.setdefault(i, set()).add(j)

    # published batch packets: sha-pinned fetch, key dicts
    prior_keyid_re = _re.compile(PRIOR_KEYID_RE_STR)
    prior_by_id = {}
    prior_pairs = set()
    prior_rows = 0
    for dirname, nkeys, want in PRIOR_BATCHES:
        url = RAW + dirname + "/input/batch-keys.json"
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                data = resp.read()
        except Exception as e:
            fail(f"fetch {dirname}: {e}")
        if hashlib.sha256(data).hexdigest() != want:
            fail(f"batch-keys sha drift for {dirname}")
        pkt = json.loads(data)
        if len(pkt["keys"]) != nkeys:
            fail(f"batch {dirname} key count drift")
        prior_rows += len(pkt["keys"])
        for k in pkt["keys"]:
            kid = k["key_id"]
            if kid.startswith(KEY_PREFIX):
                fail(f"key id prefix {KEY_PREFIX!r} already used in {dirname}")
            if not (prior_keyid_re.match(kid) or kid.startswith("aa")):
                fail(f"prior key id {kid!r} violates the pinned 1-letter/aa format")
            lo_hi = (int(k["lo"]), int(k["hi"]))
            prior_by_id[(dirname, kid)] = lo_hi
            prior_pairs.add(lo_hi)
    if prior_rows != EXPECTED_PRIOR_ROWS:
        fail(f"prior key rows {prior_rows} != expected {EXPECTED_PRIOR_ROWS}")
    if len(prior_pairs) != EXPECTED_PRIOR_UNIQUE:
        fail(f"prior unique positions {len(prior_pairs)} != expected {EXPECTED_PRIOR_UNIQUE}")

    # unconsumed-WIN re-derivation gate (33 keys)
    win_s5 = set()
    for kid, dirname, want_s5 in WIN33:
        lo_hi = prior_by_id.get((dirname, kid))
        if lo_hi is None:
            fail(f"WIN key {kid} not found in packet {dirname}")
        lo, hi = lo_hi
        got_s5 = mask_to_index.get((lo, hi))
        if got_s5 != want_s5:
            fail(f"WIN key {kid} s5 {got_s5} != declared {want_s5}")
        if (lo, hi) in cache:
            fail(f"WIN key {kid} ({lo},{hi}) already consumed in canonical cache")
        win_s5.add(want_s5)
    if len(win_s5) != WIN_COUNT:
        fail(f"WIN s5 set {len(win_s5)} != {WIN_COUNT}")

    # adoption ties (batch-20 / Part BZ / Part CH)
    b20_x = []
    for (dirname, kid), lo_hi in prior_by_id.items():
        if dirname == BATCH20_PACKET and kid.startswith("x"):
            b20_x.append((kid, lo_hi))
    if len(b20_x) != BATCH20_X_KEYS:
        fail(f"batch-20 packet x-keys {len(b20_x)} != {BATCH20_X_KEYS}")
    for kid, lo_hi in sorted(b20_x):
        if cache.get(lo_hi) != 2:
            fail(f"batch-20 key {kid} {lo_hi} not a LOSS(2) row of the adopted base")
    resolved20 = 12457
    if unknown_now[resolved20]:
        fail(f"class {resolved20} still has unknown children (Part BI adoption not visible)")
    for kid, dirname, want_s5 in BZ_ADOPTED_KEYS:
        lo_hi = prior_by_id.get((dirname, kid))
        if lo_hi is None:
            fail(f"BZ adoption tie: key {kid} not found in packet {dirname}")
        lo, hi = lo_hi
        if mask_to_index.get((lo, hi)) != want_s5:
            fail(f"BZ adoption tie: key {kid} s5 {mask_to_index.get((lo, hi))} != pinned {want_s5}")
        if cache.get(lo_hi) != 2:
            fail(f"BZ adoption tie: key {kid} {lo_hi} not a LOSS(2) row of the adopted base")
    if len(unknown_now[BZ_ADOPTED_CLASS]) != BZ_ADOPTED_CLASS_UNKNOWN:
        fail(f"BZ adoption tie: class {BZ_ADOPTED_CLASS} unknown {len(unknown_now[BZ_ADOPTED_CLASS])} != {BZ_ADOPTED_CLASS_UNKNOWN}")
    if len(unknown_now[BZ_ADOPTED_CLASS27]) != BZ_ADOPTED_CLASS27_UNKNOWN:
        fail(f"BZ adoption tie: class {BZ_ADOPTED_CLASS27} unknown {len(unknown_now[BZ_ADOPTED_CLASS27])} != {BZ_ADOPTED_CLASS27_UNKNOWN}")
    kid, dirname, want_s5 = CH_ADOPTED_KEY
    lo_hi = prior_by_id.get((dirname, kid))
    if lo_hi is None:
        fail("CH adoption tie: aa003 not found in the batch-28 published packet")
    if mask_to_index.get(lo_hi) != want_s5:
        fail(f"CH adoption tie: aa003 s5 {mask_to_index.get(lo_hi)} != pinned {want_s5}")
    if cache.get(lo_hi) != 2:
        fail("CH adoption tie: aa003 not a LOSS(2) row of the adopted base")
    if len(unknown_now[CH_ADOPTED_CLASS]) != CH_ADOPTED_CLASS_UNKNOWN:
        fail(f"CH adoption tie: class {CH_ADOPTED_CLASS} unknown {len(unknown_now[CH_ADOPTED_CLASS])} != {CH_ADOPTED_CLASS_UNKNOWN}")

    # selection gate: re-ranked group-best closure view under published base
    best_class_groups = {}
    for r in g["roots"]:
        if r["role"] != "central":
            continue
        for t in r["thirds"]:
            best_o, best_r = None, None
            for o in t["options"]:
                base = s4_status[o]
                if base == UNKNOWN:
                    rr = len(unknown_now[o])
                elif base == LOSS:
                    rr = 0
                else:
                    continue
                if rr == 0:
                    best_o, best_r = o, 0
                    break
                if best_r is None or rr < best_r:
                    best_o, best_r = o, rr
            if best_r:
                best_class_groups.setdefault(best_o, []).append((r["origin_first"], t["third"]))
    if len(best_class_groups) != CANDIDATE_ROWS:
        fail(f"re-derived closure candidate count {len(best_class_groups)} != {CANDIDATE_ROWS}")
    ranked = sorted(best_class_groups.items(),
                    key=lambda kv: (len(unknown_now[kv[0]]), -len(kv[1])))
    for rank, cls, unknown in EXPECTED_RANKS:
        got_cls, _ = ranked[rank - 1]
        if got_cls != cls:
            fail(f"re-ranked closure row {rank}: class {got_cls} != expected {cls}")
        if len(unknown_now[cls]) != unknown:
            fail(f"class {cls} unknown_now {len(unknown_now[cls])} != expected {unknown}")

    # selection classification pins (batch-29 core gate)
    for rank, (kind, cls, pinned) in SELECTION_PINS.items():
        got_cls, _ = ranked[rank - 1]
        if got_cls != cls:
            fail(f"classification pin rank {rank}: class {got_cls} != pinned {cls}")
        if kind == "win":
            got = unknown_now[cls] & win_s5
            if got != pinned:
                fail(f"rank {rank} class {cls} WIN intersection {sorted(got)} != pinned {sorted(pinned)}")
            if known_win.get(cls, set()):
                fail(f"rank {rank} class {cls} unexpectedly has known WIN children")
        elif kind == "knownwin":
            got = known_win.get(cls, set())
            if got != pinned:
                fail(f"rank {rank} class {cls} known-WIN {sorted(got)} != pinned {sorted(pinned)}")
            if unknown_now[cls] & win_s5:
                fail(f"rank {rank} class {cls} unexpectedly intersects the WIN-33 set")
        elif kind == "winknown":
            win_pin, kwin_pin = pinned
            got_w = unknown_now[cls] & win_s5
            got_k = known_win.get(cls, set())
            if got_w != win_pin:
                fail(f"rank {rank} class {cls} WIN intersection {sorted(got_w)} != pinned {sorted(win_pin)}")
            if got_k != kwin_pin:
                fail(f"rank {rank} class {cls} known-WIN {sorted(got_k)} != pinned {sorted(kwin_pin)}")
        elif kind == "pkt":
            got = {j for j in unknown_now[cls]
                   if (int(s5_masks[j][0]), int(s5_masks[j][1])) in prior_pairs}
            if got != pinned:
                fail(f"rank {rank} class {cls} pkt-collision {sorted(got)} != pinned {sorted(pinned)}")
            if unknown_now[cls] & win_s5:
                fail(f"rank {rank} class {cls} NOW carries WIN refutation evidence; reclassify")
            if known_win.get(cls, set()):
                fail(f"rank {rank} class {cls} NOW has known WIN children; reclassify")
    # rank 37 bookkeeping pin
    cls37, pinned37 = RANK37_PKT_BLOCKED
    if ranked[36][0] != cls37:
        fail(f"rank 37 class {ranked[36][0]} != pinned {cls37}")

    # target class gates
    cls_unknown = unknown_now[CLASS_INDEX]
    if cls_unknown & win_s5:
        fail(f"selection gate: class {CLASS_INDEX} unknown children intersect the WIN-33 set")
    if len(cls_unknown) != UNPROBED:
        fail(f"class {CLASS_INDEX} re-derived unknown children {len(cls_unknown)} != {UNPROBED}")
    if known_win.get(CLASS_INDEX, set()):
        fail(f"route-alive gate: class {CLASS_INDEX} has a known WIN cost child")
    derived_known = {j: iv[j] for j in cost_set if iv.get(j) is not None}
    if derived_known != KNOWN_CHILDREN:
        fail(f"route-alive gate: class {CLASS_INDEX} known children {derived_known} != declared {KNOWN_CHILDREN}")
    groups = sorted(best_class_groups.get(CLASS_INDEX, []))
    if groups != sorted(CLASS_GROUPS):
        fail(f"re-derived groups for class {CLASS_INDEX} {groups} != declared {sorted(CLASS_GROUPS)}")
    # runner-up gates
    if ranked[35][0] != RUNNER_UP_CLASS:
        fail(f"runner-up rank 36 class {ranked[35][0]} != pinned {RUNNER_UP_CLASS}")
    if known_win.get(RUNNER_UP_CLASS, set()):
        fail(f"runner-up class {RUNNER_UP_CLASS} has a known WIN cost child (route dead)")
    if unknown_now[RUNNER_UP_CLASS] & win_s5:
        fail(f"runner-up class {RUNNER_UP_CLASS} intersects the WIN-33 set")
    ov = {j for j in unknown_now[RUNNER_UP_CLASS]
          if (int(s5_masks[j][0]), int(s5_masks[j][1])) in prior_pairs}
    if ov:
        fail(f"runner-up class {RUNNER_UP_CLASS} packet-collides {sorted(ov)}")
    if sorted(best_class_groups.get(RUNNER_UP_CLASS, [])) != sorted(RUNNER_UP_GROUPS):
        fail(f"runner-up groups mismatch: {sorted(best_class_groups.get(RUNNER_UP_CLASS, []))}")

    # published-table cross-check (Part CH reaudit output, 807 rows)
    pub_rows = []
    with PUBLISHED_CLOSURE.open(encoding="utf-8-sig", newline="") as stream:
        for r in csv.DictReader(stream):
            pub_rows.append((int(r["class_rank"]), int(r["class_index"]),
                             int(r["unknown_now"]), int(r["groups_served_count"])))
    if len(pub_rows) != CANDIDATE_ROWS:
        fail(f"published closure table rows {len(pub_rows)} != {CANDIDATE_ROWS}")
    for rank, cls, unk, _gs in pub_rows:
        if rank < 1 or rank > len(ranked):
            fail(f"published closure table rank {rank} out of range")
        dcls, _dg = ranked[rank - 1]
        if dcls != cls:
            fail(f"published-table cross-check rank {rank}: derived class {dcls} != published {cls}")
        if unk != len(unknown_now[cls]):
            fail(f"published-table cross-check class {cls}: unknown {len(unknown_now[cls])} != published {unk}")
    for rank, cls, unk, gs in pub_rows:
        if cls == CLASS_INDEX:
            if rank != CLASS_RANK or unk != UNPROBED or gs != len(CLASS_GROUPS):
                fail("published target row does not match the declared class facts")

    # keys: derived from the class unknown set, ascending s5 index
    quarantined = quarantined_cache_keys()
    keys = []
    for j in sorted(cls_unknown):
        lo, hi = s5_masks[j]
        lo, hi = int(lo), int(hi)
        legal = bin(board.legal(lo | (hi << 64))).count("1")
        mem = membership[j]
        if (lo, hi) in cache:
            fail(f"key ({lo},{hi}) already in the canonical cache")
        if (lo, hi) in quarantined:
            fail(f"key ({lo},{hi}) quarantined")
        if not is_canonical_safe_s5_key((lo, hi)):
            fail(f"key ({lo},{hi}) noncanonical")
        if mask_to_index.get((lo, hi)) != j:
            fail(f"key ({lo},{hi}) s5_index mismatch")
        if j not in cost_set:
            fail(f"s5 {j} not a cost child of class {CLASS_INDEX}")
        if (lo, hi) in prior_pairs:
            fail(f"key ({lo},{hi}) already probed by a published packet")
        keys.append({
            "key_id": f"{KEY_PREFIX}{len(keys)+1:03d}",
            "s5_index": j,
            "lo": str(lo),
            "hi": str(hi),
            "legal": legal,
            "membership_class_count": mem,
        })
    keyset = {(int(k["lo"]), int(k["hi"])) for k in keys}
    keys5 = {k["s5_index"] for k in keys}
    if len(keyset) != UNPROBED:
        fail("duplicate keys within the batch")
    if keys5 & win_s5:
        fail("unconsumed WIN child must not be a batch key")
    overlap = keyset & prior_pairs
    if overlap:
        fail(f"overlap with prior batches: {sorted(overlap)}")

    batch_keys = {
        "schema": "n11-centralreply-closure-class2251-batch29-input-v1",
        "class_index": CLASS_INDEX,
        "class_mask": [str(CLASS_MASK[0]), str(CLASS_MASK[1])],
        "closure_class_rank_in_published_base": CLASS_RANK,
        "runner_up_class": RUNNER_UP_CLASS,
        "backup_classes": BACKUP_CLASSES,
        "published_base_canonical_rows": CANONICAL_ROWS,
        "groups_served_count": len(CLASS_GROUPS),
        "groups_served_first_seen": {"first": CLASS_GROUPS[0][0], "third": CLASS_GROUPS[0][1]},
        "groups_served_full": [{"first": a, "third": b} for a, b in CLASS_GROUPS],
        "budget": BUDGET,
        "keys": keys,
    }
    OUTDIR.mkdir(parents=True, exist_ok=True)
    bk_path = OUTDIR / "batch-keys.json"
    bk_path.write_text(json.dumps(batch_keys, indent=1) + "\n", encoding="utf-8")
    for k in keys:
        csv_path = OUTDIR / f"{k['key_id']}.input.csv"
        csv_path.write_text(
            "target,0,5," + k["lo"] + "," + k["hi"] + "," + str(k["legal"]) + ",0,0,0,0,0\n",
            encoding="utf-8")
    # durability check: every written file must re-read byte-identical
    import time
    def _reread(path, want):
        for _ in range(5):
            try:
                return path.read_bytes() == want
            except FileNotFoundError:
                time.sleep(0.3)
        return False
    for k in keys:
        csv_path = OUTDIR / f"{k['key_id']}.input.csv"
        want = ("target,0,5," + k["lo"] + "," + k["hi"] + "," + str(k["legal"]) + ",0,0,0,0,0\n").encode("utf-8")
        if not _reread(csv_path, want):
            fail(f"{csv_path.name} re-read mismatch or missing")
    n_csv = len(list(OUTDIR.glob(f"{KEY_PREFIX}*.input.csv")))
    if n_csv != UNPROBED:
        fail(f"input CSV count {n_csv} != {UNPROBED}")
    bk_blob = bk_path.read_bytes()
    if len(json.loads(bk_blob)["keys"]) != UNPROBED:
        fail("batch-keys.json re-read mismatch")
    mem_hist = Counter(k["membership_class_count"] for k in keys)
    print(f"OK batch-29 keys: {len(keys)} keys class {CLASS_INDEX} rank {CLASS_RANK} "
          f"groups {CLASS_GROUPS} s5 ascending "
          f"{min(k['s5_index'] for k in keys)}..{max(k['s5_index'] for k in keys)} / "
          f"legal {min(k['legal'] for k in keys)}..{max(k['legal'] for k in keys)} "
          f"membership {dict(sorted(mem_hist.items()))} "
          f"canonical_hits 0 quarantine_hits 0 prior_packets {len(PRIOR_BATCHES)} rows {prior_rows} "
          f"unique {len(prior_pairs)} WIN33 {WIN_COUNT} "
          f"adoption_ties batch20_53_x_loss bz_6_loss ch_aa003 loss "
          f"class16957_{BZ_ADOPTED_CLASS_UNKNOWN} class13342_{BZ_ADOPTED_CLASS27_UNKNOWN} "
          f"class5343_{CH_ADOPTED_CLASS_UNKNOWN} "
          f"published_table_{CANDIDATE_ROWS}_rows_cross_checked "
          f"selection_pins_ranks_1_34 rank37_pkt_pinned "
          f"runner_up {RUNNER_UP_CLASS} clean rank_35_36_only "
          f"prefix_ab_new verified")


if __name__ == "__main__":
    main()
