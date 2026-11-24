"""Batch-31 scaffold keys maker: closure class 5804 (Part CY, 2026-11-24).

Fail-closed, read-only generation of the batch-31 probe packet declared as
Part CY (published before any probe execution; single owner: n11
central-reply long lane).  Target class: graph class index 5804, mask
[6053400849139367936, 0], rank 38 under the Part CU adopted base (the
6,317-row merged canonical cache 30ddad9d..., the Part CO 6,301-row cache
plus the sixteen batch-29 LOSS rows adopted by Part CU) PLUS the published
update8 receipts.

SELECTION STATE (machine facts re-derived pre-declaration, published in the
Part CY declaration): under the Part CU base the re-derived ranked closure
table matches the published Part CU reaudit closure-classes.csv (808 rows,
3019d37f...) exactly; ranks 1..37 and 40..42 are each pinned exactly as
triples below (unconsumed-WIN77 intersection, known receipt WIN cost
children, or published packet collision; first-clean gate: every rank 1..37
carries a non-empty blocker union, so rank 38 class 5804 is the FIRST clean
candidate); rank 36 class 34269 is now doubly blocked (its own unconsumed
batch-30 WIN candidates ac002/ac003 intersect it AND all 54 of its cost
children are packet-published by batch-30); rank 39 class 11490 is the
runner-up clean candidate.  Rank 18 class 5830 keeps its five known WIN
receipt cost children; ranks 21/28 (classes 5687/5690) keep known-WIN
child 209644.

WIN77 candidate set: the published batch-30 maker WIN64 tuple list (29 prior
unconsumed keys + 35 batch-28 aa rows; 64 unique s5) UNION the eleven
batch-28 re-probe WIN rows (aa004/aa005/aa021/aa028/aa030/aa031/aa032/
aa035/aa047/aa050/aa053) UNION the two batch-30 drive-1 WIN rows
(ac002/ac003), 77 unique s5, all validated unconsumed against the CU base.

KEY ID PREFIX (continuation of the 2-letter design): batch-30 used ac;
batch-31 uses ad001..ad055.  Gates: every published packet key id matches
^[a-z][0-9]{3}$ (1-letter) or starts with "aa"/"ab"/"ac", and NO published
key id starts with "ad".

Base-independence statement: the base of this maker is the PUBLISHED Part CU
adopted canonical exact-S5 verdict cache (6,317 rows, sha256
30ddad9dc0add7e21698e864b5c202b8e6ebd3e396c4eb6156a85ff2d34005c4) PLUS the
published update8 receipts (b658290a...).  The 55 probed children of class
5804 are byte-derived from the pinned dependency graph + that adopted cache
+ those receipts; no unpublished artifact (probe worklist etc.) is read.

Gates (fail-closed; every value below is a pin the derived state must match
exactly, or the maker fails):
  * sha256 pins: graph, update8, Board, evidence policy, quarantine,
    canonical BASE cache (Part CU merged 6,317 rows), published closure table
    (Part CU reaudit, 808 rows), and the 31 published batch key packets
    (batches 1..28 + batch-14 residual + batch-29 + batch-30, fetched from
    repo raw and sha-pinned);
  * class gate: mask match, graph status unknown(1), cost size 56, unknown
    exactly 55 of them, groups served exactly [(38, 59), (38, 61),
    (49, 58), (49, 62)];
  * adoption ties (machine-pinned, not trusted from prose):
    - batch-20: all 53 published x-keys are LOSS(2) rows of the base, and
      class 12457 has zero unknown children;
    - Part BZ: the 6 published keys batch-24 y002/y004 (s5 166253/272083)
      and batch-27 o001/o003/o005/o007 (s5 98526/250515/348664/416288) are
      LOSS(2) rows of the base; class 16957 has exactly 51 unknown and
      class 13342 exactly 50;
    - Part CH: batch-28 aa003 (s5 104943) is a LOSS(2) row of the base and
      is NOT consumed anywhere else;
    - Part CO: the seven batch-28 LOSS rows aa015/aa017/aa018/aa023/aa024/
      aa029/aa036 are LOSS(2) rows of the base and class 5343 has exactly
      46 unknown children;
    - Part CU: the sixteen batch-29 LOSS rows ab001..ab016 are LOSS(2)
      rows of the base, class 2251 has exactly 38 unknown children, and NO
      OTHER key of the batch-29 packet is consumed in the base;
  * closure re-derivation: the re-derived ranked closure table (best-class
    groups over central roots) must agree with the published Part CU reaudit
    closure table on all 808 (rank -> class, unknown) pairs and with the
    pinned EXPECTED_RANKS 1..42;
  * selection classification pins (batch-31 selection core): for every rank
    1..37 and 40..42 the derived state must match the pinned triple exactly
    (unconsumed-WIN77 intersection, known-WIN receipt children, packet
    collision set); ranks 38 and 39 must be CLEAN (all three sets empty);
    first-clean gate: every rank 1..37 carries a non-empty blocker union;
  * target gates: 0/55 hits in the 6,317-row base; derived_known exactly
    the pinned {167863: 2}; quarantine 0/55; canonical-safe key form 55/55;
    mask_to_index == derived s5 index 55/55; every key is a graph cost
    child of 5804; Board recomputes legal-move popcount 55/55 in the pinned
    range 82..101; membership re-derived from the graph cost relation 55/55
    with the pinned histogram {2: 1, 3: 7, 4: 47}; every key DISJOINT from
    all 31 published packet key positions and from the WIN77 set;
  * runner-up gate: class 11490 has no known WIN child, no WIN77
    intersection, zero packet collision, derived_known exactly the pinned
    {376421: 2}, groups exactly the pinned four, and rank 39.

Outputs: input/batch-keys.json (schema
n11-centralreply-closure-class5804-batch31-input-v1, key ids ad001..ad055)
and input/adNNN.input.csv (55 single-row target CSVs for the pinned runner).
Standard 11x11, all 19 central-reply roots, class 5804 and every key stay
UNKNOWN; nodes are bookkeeping, never verdicts.
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
CU_DIR = ROOT / "research/experiments/n11-centralreply-class2251-loss16-adoption-reaudit-20261123"
BASE_CACHE = CU_DIR / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-20261123.cache"
PUBLISHED_CLOSURE = CU_DIR / "reaudit/output/closure-classes.csv"

CLASS_INDEX = 5804
CLASS_MASK = [6053400849139367936, 0]
CLASS_RANK = 38      # under the adopted 6,317-row base (published Part CU table)
COST_SIZE = 56
UNPROBED = 55
KNOWN_CHILDREN = {167863: 2}   # the single base-resolved cost child of 5804 (LOSS)
CLASS_GROUPS = [(38, 59), (38, 61), (49, 58), (49, 62)]
RUNNER_UP_CLASS = 11490       # rank 39
RUNNER_UP_KNOWN_CHILDREN = {376421: 2}   # its single base-resolved cost child (LOSS)
RUNNER_UP_GROUPS = [(16, 48), (16, 50), (48, 16), (48, 56)]
RANK37_PKT_BLOCKED = (34948, {415128})
BUDGET = 15000000
LEGAL_RANGE = (82, 101)        # recomputed Board legal popcount range, 55/55
MEMBERSHIP_HIST = {2: 1, 3: 7, 4: 47}
CANONICAL_ROWS = 6317          # Part CU merged cache
CANDIDATE_ROWS = 808           # published Part CU closure table rows
KEY_PREFIX = "ad"
PRIOR_KEYID_RE_STR = r"^[a-z][0-9]{3}$"

# WIN77: 29 prior unconsumed keys (published batch-29 maker pins, via the
# published batch-30 maker WIN64 list: 29 prior + 35 batch-28 aa rows,
# 64 unique s5) + the eleven batch-28 re-probe WIN rows + the two batch-30
# drive-1 WIN rows (ac002/ac003).  77 unique s5 indices.
WIN77 = [
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
    ("aa001", "n11-centralreply-closure-class5343-batch28-20261123", 28037),
    ("aa002", "n11-centralreply-closure-class5343-batch28-20261123", 87306),
    ("aa006", "n11-centralreply-closure-class5343-batch28-20261123", 129823),
    ("aa007", "n11-centralreply-closure-class5343-batch28-20261123", 135236),
    ("aa008", "n11-centralreply-closure-class5343-batch28-20261123", 140489),
    ("aa009", "n11-centralreply-closure-class5343-batch28-20261123", 142299),
    ("aa010", "n11-centralreply-closure-class5343-batch28-20261123", 144019),
    ("aa011", "n11-centralreply-closure-class5343-batch28-20261123", 147632),
    ("aa012", "n11-centralreply-closure-class5343-batch28-20261123", 151960),
    ("aa013", "n11-centralreply-closure-class5343-batch28-20261123", 156182),
    ("aa014", "n11-centralreply-closure-class5343-batch28-20261123", 160350),
    ("aa016", "n11-centralreply-closure-class5343-batch28-20261123", 167491),
    ("aa019", "n11-centralreply-closure-class5343-batch28-20261123", 183025),
    ("aa020", "n11-centralreply-closure-class5343-batch28-20261123", 185891),
    ("aa022", "n11-centralreply-closure-class5343-batch28-20261123", 191399),
    ("aa025", "n11-centralreply-closure-class5343-batch28-20261123", 198223),
    ("aa026", "n11-centralreply-closure-class5343-batch28-20261123", 199711),
    ("aa027", "n11-centralreply-closure-class5343-batch28-20261123", 199712),
    ("aa033", "n11-centralreply-closure-class5343-batch28-20261123", 199718),
    ("aa034", "n11-centralreply-closure-class5343-batch28-20261123", 199719),
    ("aa037", "n11-centralreply-closure-class5343-batch28-20261123", 199722),
    ("aa038", "n11-centralreply-closure-class5343-batch28-20261123", 199723),
    ("aa039", "n11-centralreply-closure-class5343-batch28-20261123", 199724),
    ("aa040", "n11-centralreply-closure-class5343-batch28-20261123", 199725),
    ("aa041", "n11-centralreply-closure-class5343-batch28-20261123", 199726),
    ("aa042", "n11-centralreply-closure-class5343-batch28-20261123", 199727),
    ("aa043", "n11-centralreply-closure-class5343-batch28-20261123", 199728),
    ("aa044", "n11-centralreply-closure-class5343-batch28-20261123", 199729),
    ("aa045", "n11-centralreply-closure-class5343-batch28-20261123", 199730),
    ("aa046", "n11-centralreply-closure-class5343-batch28-20261123", 199731),
    ("aa048", "n11-centralreply-closure-class5343-batch28-20261123", 199733),
    ("aa049", "n11-centralreply-closure-class5343-batch28-20261123", 199734),
    ("aa051", "n11-centralreply-closure-class5343-batch28-20261123", 199736),
    ("aa052", "n11-centralreply-closure-class5343-batch28-20261123", 199737),
    ("aa054", "n11-centralreply-closure-class5343-batch28-20261123", 199739),
    ("aa004", "n11-centralreply-closure-class5343-batch28-20261123", 118693),
    ("aa005", "n11-centralreply-closure-class5343-batch28-20261123", 124331),
    ("aa021", "n11-centralreply-closure-class5343-batch28-20261123", 188751),
    ("aa028", "n11-centralreply-closure-class5343-batch28-20261123", 199713),
    ("aa030", "n11-centralreply-closure-class5343-batch28-20261123", 199715),
    ("aa031", "n11-centralreply-closure-class5343-batch28-20261123", 199716),
    ("aa032", "n11-centralreply-closure-class5343-batch28-20261123", 199717),
    ("aa035", "n11-centralreply-closure-class5343-batch28-20261123", 199720),
    ("aa047", "n11-centralreply-closure-class5343-batch28-20261123", 199732),
    ("aa050", "n11-centralreply-closure-class5343-batch28-20261123", 199735),
    ("aa053", "n11-centralreply-closure-class5343-batch28-20261123", 199738),
    ("ac002", "n11-centralreply-closure-class34269-batch30-20261123", 38891),
    ("ac003", "n11-centralreply-closure-class34269-batch30-20261123", 178184),
]
WIN_COUNT = 77

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
CO_ADOPTED_KEYS = [
    ("aa015", "n11-centralreply-closure-class5343-batch28-20261123"),
    ("aa017", "n11-centralreply-closure-class5343-batch28-20261123"),
    ("aa018", "n11-centralreply-closure-class5343-batch28-20261123"),
    ("aa023", "n11-centralreply-closure-class5343-batch28-20261123"),
    ("aa024", "n11-centralreply-closure-class5343-batch28-20261123"),
    ("aa029", "n11-centralreply-closure-class5343-batch28-20261123"),
    ("aa036", "n11-centralreply-closure-class5343-batch28-20261123"),
]
CO_ADOPTED_CLASS = 5343
CO_ADOPTED_CLASS_UNKNOWN = 46

# Part CU adoption: the sixteen batch-29 LOSS rows adopted into the 6,317-row
# CU base; NO other ab key of the batch-29 packet is consumed in the base.
CU_ADOPTED_KEYS = [
    ("ab001", "n11-centralreply-closure-class2251-batch29-20261123", 3964),
    ("ab002", "n11-centralreply-closure-class2251-batch29-20261123", 9935),
    ("ab003", "n11-centralreply-closure-class2251-batch29-20261123", 15659),
    ("ab004", "n11-centralreply-closure-class2251-batch29-20261123", 21341),
    ("ab005", "n11-centralreply-closure-class2251-batch29-20261123", 26610),
    ("ab006", "n11-centralreply-closure-class2251-batch29-20261123", 33712),
    ("ab007", "n11-centralreply-closure-class2251-batch29-20261123", 38148),
    ("ab008", "n11-centralreply-closure-class2251-batch29-20261123", 42711),
    ("ab009", "n11-centralreply-closure-class2251-batch29-20261123", 51145),
    ("ab010", "n11-centralreply-closure-class2251-batch29-20261123", 53947),
    ("ab011", "n11-centralreply-closure-class2251-batch29-20261123", 56596),
    ("ab012", "n11-centralreply-closure-class2251-batch29-20261123", 60153),
    ("ab013", "n11-centralreply-closure-class2251-batch29-20261123", 63620),
    ("ab014", "n11-centralreply-closure-class2251-batch29-20261123", 67275),
    ("ab015", "n11-centralreply-closure-class2251-batch29-20261123", 73062),
    ("ab016", "n11-centralreply-closure-class2251-batch29-20261123", 76023),
]
CU_ADOPTED_CLASS = 2251
CU_ADOPTED_CLASS_UNKNOWN = 38
BATCH29_PACKET = "n11-centralreply-closure-class2251-batch29-20261123"

# 31 published key packets (raw main, sha256-pinned): batches 1..28 +
# batch-14 residual + batch-29 + batch-30
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
    ("n11-centralreply-closure-class12457-batch20-20261123", 53,
     "efb40b1bb7a43595bb8d014a31af2b878c404be86b8f9d5abc717eb176d1ed51"),
    ("n11-centralreply-closure-class2251-batch29-20261123", 54,
     "330c0b9f3166e9f6e21b739a851a881d800ab9f58a14dccaa0c772118dee716c"),    ("n11-centralreply-closure-class34269-batch30-20261123", 54,
     "79fbd1664f4ad66ea62d9c8a8aa5aaff5d16bcdaa397895119ce4d8f47961232"),
]
EXPECTED_PRIOR_ROWS = 1568
EXPECTED_PRIOR_UNIQUE = 1554

# ranked closure rows 1..42 under the Part CU base (published table)
EXPECTED_RANKS = [
    (1, 23101, 1),
    (2, 1849, 1),
    (3, 16757, 29),
    (4, 2251, 38),
    (5, 5343, 46),
    (6, 20421, 49),
    (7, 16371, 49),
    (8, 13342, 50),
    (9, 30345, 50),
    (10, 12264, 51),
    (11, 5473, 51),
    (12, 16957, 51),
    (13, 2634, 51),
    (14, 8785, 51),
    (15, 1518, 51),
    (16, 8106, 52),
    (17, 16930, 52),
    (18, 5830, 52),
    (19, 16131, 53),
    (20, 16513, 53),
    (21, 5687, 53),
    (22, 12643, 53),
    (23, 31600, 53),
    (24, 10968, 53),
    (25, 23964, 53),
    (26, 25835, 53),
    (27, 30565, 53),
    (28, 5690, 53),
    (29, 13758, 54),
    (30, 14103, 54),
    (31, 30484, 54),
    (32, 34263, 54),
    (33, 16901, 54),
    (34, 19749, 54),
    (35, 23482, 54),
    (36, 34269, 54),
    (37, 34948, 54),
    (38, 5804, 55),
    (39, 11490, 55),
    (40, 12857, 55),
    (41, 14743, 55),
    (42, 15453, 55),
]

# selection classification pins (fail-closed): for every rank 1..37 and
#   40..42 (all ranks except the target 38 and the runner-up 39)
#   rank: (class, unconsumed-WIN77 intersection s5 set, known-WIN receipt
#          children, packet collision s5 set)
# ranks 38 (target) and 39 (runner-up) are CLEAN by construction (gated).
# first-clean gate: every rank 1..37 carries a non-empty blocker union, so
# class 5804 is the first clean candidate; ranks 41/42 are clean but
# rank-ordered behind the target and the runner-up.
SELECTION_PINS = {
    1: (23101, {745184}, set(), {745184}),
    2: (1849, {81011}, set(), {81011}),
    3: (16757, {528497}, set(), {528497, 535179, 537545, 539592, 541610, 545364, 546902, 548070, 549153, 551777, 554104, 555161, 556117, 558018, 558054, 558079, 558120, 558183, 558228, 558261, 558283, 558334, 558367, 558393, 558410, 558443, 558486, 558506, 558553}),
    4: (2251, set(), set(), {78838, 84223, 86005, 87025, 89372, 91588, 93761, 93811, 93812, 93813, 93814, 93815, 93816, 93817, 93818, 93819, 93820, 93821, 93822, 93823, 93824, 93825, 93826, 93827, 93828, 93829, 93830, 93831, 93832, 93833, 93834, 93835, 93836, 93837, 93838, 93839, 93840, 93841}),
    5: (5343, {28037, 87306, 118693, 124331, 129823, 135236, 140489, 142299, 144019, 147632, 151960, 156182, 160350, 167491, 183025, 185891, 188751, 191399, 198223, 199711, 199712, 199713, 199715, 199716, 199717, 199718, 199719, 199720, 199722, 199723, 199724, 199725, 199726, 199727, 199728, 199729, 199730, 199731, 199732, 199733, 199734, 199735, 199736, 199737, 199738, 199739}, set(), {28037, 87306, 118693, 124331, 129823, 135236, 140489, 142299, 144019, 147632, 151960, 156182, 160350, 167491, 183025, 185891, 188751, 191399, 198223, 199711, 199712, 199713, 199715, 199716, 199717, 199718, 199719, 199720, 199722, 199723, 199724, 199725, 199726, 199727, 199728, 199729, 199730, 199731, 199732, 199733, 199734, 199735, 199736, 199737, 199738, 199739}),
    6: (20421, {197253}, set(), {38215, 197253, 259023, 300778, 356378, 393798, 441775, 528689, 543795, 565995, 570139, 574236, 578232, 582153, 585861, 589727, 593275, 596738, 602640, 605690, 605961, 608779, 611801, 614833, 617672, 620742, 623364, 625189, 625899, 630432, 636913, 641189, 643424, 645317, 650304, 651925, 653505, 655969, 657407, 662182, 664455, 669726, 671112, 671120, 671129, 671133, 671137, 671143, 671146}),
    7: (16371, {183566}, set(), {93170, 183566, 306951, 399422, 480806, 498207, 502385, 505442, 509234, 512923, 516385, 522643, 525693, 528188, 530117, 532225, 534675, 537035, 541141, 543110, 544907, 547319, 548819, 549855, 550280, 550330, 550357, 550403, 550446, 550549, 550593, 550622, 550719, 550757, 550795, 550839, 550868, 550876, 550877, 550878, 550879, 550880, 550882, 550883, 550884, 550885, 550886, 550887, 550888}),
    8: (13342, {209134}, set(), {209134, 311233, 403418, 420603, 420631, 424940, 425010, 429122, 429212, 433235, 436911, 440454, 440471, 443828, 443913, 447151, 447245, 450306, 450380, 453531, 456481, 458998, 459133, 459256, 459388, 459466, 459528, 459586, 459747, 459872, 459982, 460087, 460145, 460195, 460199, 460200, 460201, 460202, 460203, 460204, 460205, 460206, 460207, 460208, 460209, 460210, 460211, 460212, 460213, 460214}),
    9: (30345, {528497}, set(), {528497}),
    10: (12264, {415095}, set(), {348, 4231, 115134, 119290, 223911, 224296, 227832, 323984, 324399, 327676, 414362, 415090, 415091, 415092, 415093, 415094, 415095, 415096, 415097, 415098, 415099, 415100, 415101, 415102, 415103, 415104, 415105, 415106, 415107, 415108, 415109, 415110, 415111, 415112, 415113, 415114, 415115, 415116, 415117, 415118, 415119, 415120, 415121, 415122, 415123, 415124, 415125, 415126, 415127, 415128, 415129}),
    11: (5473, {184684}, set(), {91746, 107082, 124588, 130089, 135518, 140758, 147898, 152203, 156428, 160599, 164711, 167624, 170359, 173922, 177219, 180267, 183294, 184684, 186150, 191645, 198326, 203504, 203505, 203506, 203507, 203508, 203509, 203510, 203511, 203512, 203513, 203514, 203515, 203516, 203517, 203518, 203519, 203520, 203521, 203522, 203523, 203524, 203525, 203526, 203527, 203528, 203529, 203530, 203531, 203532, 203533}),
    12: (16957, {91296, 368510}, set(), {91296, 201465, 303941, 368510, 398128, 452611, 495175, 499281, 503457, 507434, 511103, 513916, 517326, 523639, 526581, 531174, 533768, 536195, 537809, 537973, 539885, 541944, 545698, 547061, 548421, 549792, 550743, 552036, 553257, 554350, 555422, 556254, 556821, 558776, 559391, 559914, 560428, 560848, 561195, 561250, 561273, 561286, 561317, 561337, 561355, 561369, 561384, 561412, 561426, 561457, 561493}),
    13: (2634, {103558, 103560, 103561}, set(), {5299, 11390, 17131, 22726, 28026, 30697, 35113, 39323, 44195, 48403, 52487, 54877, 57818, 61535, 68710, 74525, 77496, 80293, 88503, 90823, 93116, 102681, 102752, 102798, 102834, 102879, 102927, 102966, 103007, 103067, 103100, 103140, 103189, 103225, 103284, 103300, 103332, 103364, 103400, 103430, 103466, 103497, 103531, 103557, 103558, 103559, 103560, 103561, 103562, 103563, 103564}),
    14: (8785, {198530}, set(), {86114, 100564, 198530, 211089, 227919, 233308, 238493, 243520, 248374, 251373, 255118, 259270, 263355, 267293, 271059, 273610, 276382, 279713, 285590, 290848, 295771, 298083, 300236, 302291, 304232, 307676, 309185, 312063, 312103, 312210, 312253, 312295, 312334, 312367, 312426, 312457, 312495, 312536, 312599, 312620, 312670, 312687, 312723, 312765, 312785, 312824, 312854, 312889, 312915, 312953, 312960}),
    15: (1518, {69347}, set(), {2585, 8526, 14284, 19934, 25252, 29393, 32365, 36876, 41312, 45607, 49812, 53395, 69327, 69328, 69329, 69330, 69331, 69332, 69333, 69334, 69335, 69336, 69337, 69338, 69339, 69340, 69341, 69342, 69343, 69344, 69345, 69346, 69347, 69348, 69349, 69350, 69351, 69352, 69353, 69354, 69355, 69356, 69357, 69358, 69359, 69360, 69361, 69362, 69363, 69364, 69365}),
    16: (8106, {188395, 219608}, set(), {48210, 75387, 110810, 161205, 188395, 219608, 232022, 237227, 242240, 247139, 250781, 253887, 258068, 262121, 266048, 268033, 269828, 273033, 275172, 278496, 284380, 292761, 292762, 292763, 292764, 292765, 292766, 292767, 292768, 292769, 292770, 292771, 292772, 292773, 292774, 292775, 292776, 292777, 292778, 292779, 292780, 292781, 292782, 292783, 292784, 292785, 292786, 292787, 292788, 292789, 292790, 292791}),
    17: (16930, {185003, 203419}, set(), {91793, 185003, 203419, 305820, 382876, 479896, 495193, 499324, 503517, 507510, 511150, 513950, 517400, 520499, 523708, 526648, 528664, 531239, 533828, 536102, 537872, 542007, 543890, 545722, 548469, 549875, 550798, 550879, 552089, 554393, 555460, 556286, 556851, 557488, 558197, 558818, 559418, 559947, 560833, 560860, 560873, 560908, 560932, 560956, 560963, 560982, 561006, 561040, 561059, 561076, 561102, 561141}),
    18: (5830, {103560, 103561}, {126017, 131631, 162106, 197665, 206386}, {103560, 103561, 120355, 120370, 126032, 126066, 131633, 131690, 137043, 137046, 137100, 142280, 142283, 142320, 144501, 149388, 153601, 153617, 157836, 157861, 157873, 162100, 162136, 166171, 166175, 166211, 167914, 171811, 175418, 178520, 178533, 181624, 181634, 181660, 184670, 184682, 184706, 187878, 190447, 193077, 195399, 195416, 197666, 197687, 198652, 200898, 202883, 204660, 208173, 209583, 211072, 212535}),
    19: (16131, {153671, 207534}, set(), {153671, 207534, 259131, 309691, 356499, 401999, 482963, 497687, 497757, 500954, 501999, 505002, 506464, 508811, 510565, 512474, 514362, 515931, 518307, 521369, 522241, 524564, 525298, 527455, 528708, 529234, 529721, 531915, 532784, 535548, 538077, 538916, 540644, 540864, 542705, 542998, 543058, 543113, 543166, 543219, 543382, 543480, 543528, 543572, 543762, 543796, 544054, 544130, 544554, 544555, 544556, 544557, 544558}),
    20: (16513, {63802, 109169}, set(), {63802, 109169, 177512, 178574, 282555, 377383, 460197, 461037, 494825, 498443, 502579, 505615, 509346, 513071, 516514, 519643, 522773, 528281, 530334, 532378, 534795, 537179, 541264, 545036, 546690, 547451, 550318, 551526, 552832, 552919, 552956, 553007, 553091, 553131, 553170, 553235, 553271, 553309, 553318, 553375, 553401, 553466, 553485, 553516, 553553, 553583, 553602, 553639, 553676, 553699, 553753, 553820, 553923}),
    21: (5687, set(), {209644}, {30697, 103564, 144501, 209583}),
    22: (12643, {115192}, set(), {23431, 87361, 115192, 223962, 245065, 302198, 324036, 343700, 395222, 414417, 432051, 432052, 432053, 432054, 432055, 432056, 432057, 432058, 432059, 432060, 432061, 432062, 432063, 432064, 432065, 432066, 432067, 432068, 432069, 432070, 432071, 432072, 432073, 432074, 432075, 432076, 432077, 432078, 432079, 432080, 432081, 432082, 432083, 432084, 432085, 432086, 432087, 432088, 432089, 432090, 432091, 432092, 432093}),
    23: (31600, {62435, 192809}, set(), {62435, 192809, 281313, 296441, 389791, 472152, 546669, 547437, 559167, 633454, 635621, 653653, 658694, 738616, 740458, 755752, 816927, 825712, 828412, 871442, 878117, 880091, 901328, 904617, 906148, 907617, 909037, 910413, 911713, 912942, 914090, 915161, 916210, 917232, 918230, 919203, 920050, 920881, 922258, 922913, 923543, 924498, 924553, 924567, 924612, 924679, 924790, 924791, 924792, 924793, 924794, 924795, 924796}),
    24: (10968, set(), set(), {273033}),
    25: (23964, set(), set(), {495193, 550880}),
    26: (25835, {150241}, set(), {91297, 150241, 202300, 256847, 304718, 354522, 397407, 478905, 527836, 603600, 612767, 667196, 714967, 722209, 759412, 760753, 772527, 775345, 778182, 780889, 783530, 792894, 795081, 797258, 799204, 801162, 803089, 805738, 807551, 809368, 809460, 809519, 809566, 809621, 809669, 809765, 809862, 809944, 809985, 810109, 810139, 810239, 810370, 810371, 810372, 810373, 810374, 810375, 810376, 810377, 810378, 810379, 810380}),
    27: (30565, {68580, 191299}, set(), {68580, 191299, 286434, 294966, 388472, 463454, 548129, 552626, 556154, 637247, 643432, 652710, 654401, 741646, 744080, 752770, 817883, 825164, 826156, 872234, 873223, 878457, 887233, 888836, 890426, 891783, 892837, 894102, 895286, 896320, 897016, 897872, 898622, 899208, 899902, 900497, 901026, 901442, 901737, 902032, 902085, 902616, 902862, 903040, 903065, 903068, 903093, 903103, 903116, 903131, 903143, 903156, 903169}),
    28: (5690, set(), {209644}, set()),
    29: (13758, set(), set(), {459528}),
    30: (14103, set(), set(), {460145}),
    31: (30484, set(), set(), {546902, 558506}),
    32: (34263, set(), set(), {528281, 553923, 958125}),
    33: (16901, set(), set(), {528689}),
    34: (19749, set(), set(), {657407}),
    35: (23482, set(), set(), {550446, 561141}),
    36: (34269, {38891, 178184}, set(), {36668, 38891, 178184, 257581, 259840, 355050, 357255, 440522, 442454, 542960, 544425, 604378, 605817, 625811, 715677, 731067, 732474, 799572, 800491, 809575, 810549, 858406, 859149, 865769, 866494, 900276, 900687, 916195, 916640, 920775, 921287, 939058, 939315, 941211, 941466, 951686, 951830, 952950, 953103, 955954, 956329, 956625, 956972, 957287, 957713, 957935, 958064, 958080, 958082, 958097, 958105, 958114, 958125, 958143}),
    37: (34948, set(), set(), {415128}),
    40: (12857, set(), set(), {440454}),
    41: (14743, set(), set(), set()),
    42: (15453, set(), set(), set()),
}

PIN_SHA = {
    "graph": "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b",
    "update8": "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719",
    "board": "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f",
    "policy": "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2",
    "quarantine": "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9",
    "canonical_base_cache": "30ddad9dc0add7e21698e864b5c202b8e6ebd3e396c4eb6156a85ff2d34005c4",
    "published_closure": "3019d37f72ac6a46672f0fd027eae1c42c708f6e68d082925d85243d64195754",
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

    # class sanity
    if list(s4_masks[CLASS_INDEX]) != CLASS_MASK:
        fail(f"graph mask {s4_masks[CLASS_INDEX]} != declared class mask")
    if s4_status[CLASS_INDEX] != 1:
        fail(f"graph status of class {CLASS_INDEX} is {s4_status[CLASS_INDEX]}, not unknown(1)")
    cost_set = set(s4_cost[CLASS_INDEX])
    if len(cost_set) != COST_SIZE:
        fail(f"class cost size {len(cost_set)} != {COST_SIZE}")

    # canonical cache (published Part CO adopted output, 6,301 rows) + receipts
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
                fail(f"key id prefix already used in {dirname}")
            if not (prior_keyid_re.match(kid) or kid.startswith("aa") or kid.startswith("ab") or kid.startswith("ac")):
                fail(f"prior key id {kid!r} violates the pinned format")
            lo_hi = (int(k["lo"]), int(k["hi"]))
            prior_by_id[(dirname, kid)] = lo_hi
            prior_pairs.add(lo_hi)
    if prior_rows != EXPECTED_PRIOR_ROWS:
        fail(f"prior key rows {prior_rows} != expected {EXPECTED_PRIOR_ROWS}")
    if len(prior_pairs) != EXPECTED_PRIOR_UNIQUE:
        fail(f"prior unique positions {len(prior_pairs)} != expected {EXPECTED_PRIOR_UNIQUE}")

    # unconsumed-WIN re-derivation gate (77 keys)
    win_s5 = set()
    for kid, dirname, want_s5 in WIN77:
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

    # adoption ties (batch-20 / Part BZ / Part CH / Part CO)
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
        fail(f"class {resolved20} still has unknown children")
    for kid, dirname, want_s5 in BZ_ADOPTED_KEYS:
        lo_hi = prior_by_id.get((dirname, kid))
        if lo_hi is None:
            fail(f"BZ adoption tie: key {kid} not found in packet {dirname}")
        lo, hi = lo_hi
        if mask_to_index.get((lo, hi)) != want_s5:
            fail(f"BZ adoption tie: key {kid} s5 mismatch")
        if cache.get(lo_hi) != 2:
            fail(f"BZ adoption tie: key {kid} {lo_hi} not a LOSS(2) row of the adopted base")
    if len(unknown_now[BZ_ADOPTED_CLASS]) != BZ_ADOPTED_CLASS_UNKNOWN:
        fail(f"BZ adoption tie: class {BZ_ADOPTED_CLASS} unknown mismatch")
    if len(unknown_now[BZ_ADOPTED_CLASS27]) != BZ_ADOPTED_CLASS27_UNKNOWN:
        fail(f"BZ adoption tie: class {BZ_ADOPTED_CLASS27} unknown mismatch")
    kid, dirname, want_s5 = CH_ADOPTED_KEY
    lo_hi = prior_by_id.get((dirname, kid))
    if lo_hi is None:
        fail("CH adoption tie: aa003 not found in the batch-28 published packet")
    if mask_to_index.get(lo_hi) != want_s5:
        fail("CH adoption tie: aa003 s5 mismatch")
    if cache.get(lo_hi) != 2:
        fail("CH adoption tie: aa003 not a LOSS(2) row of the adopted base")
    for kid, dirname in CO_ADOPTED_KEYS:
        lo_hi = prior_by_id.get((dirname, kid))
        if lo_hi is None:
            fail(f"CO adoption tie: key {kid} not found in the batch-28 packet")
        if cache.get(lo_hi) != 2:
            fail(f"CO adoption tie: key {kid} not a LOSS(2) row of the adopted base")
    if len(unknown_now[CO_ADOPTED_CLASS]) != CO_ADOPTED_CLASS_UNKNOWN:
        fail(f"CO adoption tie: class {CO_ADOPTED_CLASS} unknown {len(unknown_now[CO_ADOPTED_CLASS])} != {CO_ADOPTED_CLASS_UNKNOWN}")
    # Part CU adoption tie: the sixteen batch-29 LOSS rows are consumed as
    # LOSS(2) in the base, class 2251 has exactly 38 unknown left, and no
    # other ab key of the published batch-29 packet is consumed anywhere.
    by_kid_b29 = {}
    for k in prior_by_id:
        if k[0] == BATCH29_PACKET:
            by_kid_b29[k[1]] = prior_by_id[k]
    if len(by_kid_b29) != 54:
        fail(f"batch-29 packet ids {len(by_kid_b29)} != 54")
    for kid, dirname, want_s5 in CU_ADOPTED_KEYS:
        lo_hi = prior_by_id.get((dirname, kid))
        if lo_hi is None:
            fail(f"CU adoption tie: key {kid} not found in the batch-29 packet")
        if mask_to_index.get(lo_hi) != want_s5:
            fail(f"CU adoption tie: key {kid} s5 {mask_to_index.get(lo_hi)} != pinned {want_s5}")
        if cache.get(lo_hi) != 2:
            fail(f"CU adoption tie: key {kid} {lo_hi} not a LOSS(2) row of the adopted base")
    n_b29_consumed = 0
    for kid, lo_hi in by_kid_b29.items():
        if lo_hi in cache:
            n_b29_consumed += 1
            if (kid, mask_to_index[lo_hi]) not in {(k, s) for k, d, s in CU_ADOPTED_KEYS}:
                fail(f"unexpected consumed batch-29 key {kid}")
    if n_b29_consumed != len(CU_ADOPTED_KEYS):
        fail(f"consumed batch-29 rows {n_b29_consumed} != {len(CU_ADOPTED_KEYS)}")
    if len(unknown_now[CU_ADOPTED_CLASS]) != CU_ADOPTED_CLASS_UNKNOWN:
        fail(f"CU adoption tie: class {CU_ADOPTED_CLASS} unknown {len(unknown_now[CU_ADOPTED_CLASS])} != {CU_ADOPTED_CLASS_UNKNOWN}")

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

    # selection classification pins (batch-30 core gate)
    for rank, (cls, win_pin, kwin_pin, pkt_pin) in SELECTION_PINS.items():
        got_cls, _ = ranked[rank - 1]
        if got_cls != cls:
            fail(f"classification pin rank {rank}: class {got_cls} != pinned {cls}")
        got_win = unknown_now[cls] & win_s5
        got_kwin = known_win.get(cls, set())
        got_pkt = {j for j in unknown_now[cls]
                   if (int(s5_masks[j][0]), int(s5_masks[j][1])) in prior_pairs}
        if got_win != win_pin:
            fail(f"rank {rank} class {cls} WIN intersection {sorted(got_win)} != pinned {sorted(win_pin)}")
        if got_kwin != kwin_pin:
            fail(f"rank {rank} class {cls} known-WIN {sorted(got_kwin)} != pinned {sorted(kwin_pin)}")
        if got_pkt != pkt_pin:
            fail(f"rank {rank} class {cls} pkt-collision {sorted(got_pkt)} != pinned {sorted(pkt_pin)}")
    # first-clean gate: every rank before the target carries a blocker
    for rank, (cls, win_pin, kwin_pin, pkt_pin) in SELECTION_PINS.items():
        if rank < CLASS_RANK and not (win_pin | kwin_pin | pkt_pin):
            fail(f"first-clean gate: rank {rank} class {cls} pinned clean before the target")

    # target class gates
    cls_unknown = unknown_now[CLASS_INDEX]
    if cls_unknown & win_s5:
        fail(f"selection gate: class {CLASS_INDEX} unknown children intersect the WIN64 set")
    if len(cls_unknown) != UNPROBED:
        fail(f"class {CLASS_INDEX} re-derived unknown children {len(cls_unknown)} != {UNPROBED}")
    if known_win.get(CLASS_INDEX, set()):
        fail(f"route-alive gate: class {CLASS_INDEX} has a known WIN cost child")
    derived_known = {j: iv[j] for j in cost_set if iv.get(j) is not None}
    if derived_known != KNOWN_CHILDREN:
        fail(f"route-alive gate: class {CLASS_INDEX} known children != declared")
    groups = sorted(best_class_groups.get(CLASS_INDEX, []))
    if groups != sorted(CLASS_GROUPS):
        fail(f"re-derived groups for class {CLASS_INDEX} {groups} != declared")
    # rank 37 bookkeeping pin
    cls37, pinned37 = RANK37_PKT_BLOCKED
    if ranked[36][0] != cls37:
        fail(f"rank 37 class {ranked[36][0]} != pinned {cls37}")
    got37 = {j for j in unknown_now[cls37]
             if (int(s5_masks[j][0]), int(s5_masks[j][1])) in prior_pairs}
    if got37 != pinned37:
        fail(f"rank 37 pkt-collision {sorted(got37)} != pinned {sorted(pinned37)}")
    # runner-up gates (rank 39)
    if ranked[38][0] != RUNNER_UP_CLASS:
        fail(f"runner-up rank 39 class {ranked[38][0]} != pinned {RUNNER_UP_CLASS}")
    ru_known = {j: iv[j] for j in set(s4_cost[RUNNER_UP_CLASS]) if iv.get(j) is not None}
    if ru_known != RUNNER_UP_KNOWN_CHILDREN:
        fail(f"runner-up derived_known {ru_known} != pinned {RUNNER_UP_KNOWN_CHILDREN}")
    if known_win.get(RUNNER_UP_CLASS, set()):
        fail(f"runner-up class {RUNNER_UP_CLASS} has a known WIN cost child")
    if unknown_now[RUNNER_UP_CLASS] & win_s5:
        fail(f"runner-up class {RUNNER_UP_CLASS} intersects the WIN64 set")
    ov = {j for j in unknown_now[RUNNER_UP_CLASS]
          if (int(s5_masks[j][0]), int(s5_masks[j][1])) in prior_pairs}
    if ov:
        fail(f"runner-up class {RUNNER_UP_CLASS} packet-collides {sorted(ov)}")
    if sorted(best_class_groups.get(RUNNER_UP_CLASS, [])) != sorted(RUNNER_UP_GROUPS):
        fail(f"runner-up groups mismatch")

    # published-table cross-check (Part CO reaudit output, 808 rows)
    pub_rows = []
    with PUBLISHED_CLOSURE.open(encoding="utf-8-sig", newline="") as stream:
        for r in csv.DictReader(stream):
            pub_rows.append((int(r["class_rank"]), int(r["class_index"]),
                             int(r["unknown_now"]), int(r["groups_served_count"])))
    if len(pub_rows) != CANDIDATE_ROWS:
        fail(f"published closure table rows {len(pub_rows)} != {CANDIDATE_ROWS}")
    for rank, cls, unk, _gs in pub_rows:
        dcls, _dg = ranked[rank - 1]
        if dcls != cls:
            fail(f"published-table cross-check rank {rank}: derived class {dcls} != published {cls}")
        if unk != len(unknown_now[cls]):
            fail(f"published-table cross-check class {cls}: unknown mismatch")
    for rank, cls, unk, gs in pub_rows:
        if cls == CLASS_INDEX:
            if rank != CLASS_RANK or unk != UNPROBED or gs != len(CLASS_GROUPS):
                fail("published target row does not match the declared class facts")

    # keys: derived from the class unknown set, ascending s5 index
    quarantined = quarantined_cache_keys()
    membership = Counter()
    for cost in s4_cost:
        for j in cost:
            membership[j] += 1
    keys = []
    for j in sorted(cls_unknown):
        lo, hi = s5_masks[j]
        lo, hi = int(lo), int(hi)
        legal = bin(board.legal(lo | (hi << 64))).count("1")
        mem = membership[j]
        if not LEGAL_RANGE[0] <= legal <= LEGAL_RANGE[1]:
            fail(f"key ({lo},{hi}) legal {legal} outside the pinned range {LEGAL_RANGE}")
        if (lo, hi) in cache:
            fail(f"key ({lo},{hi}) already in the canonical cache")
        if (lo, hi) in quarantined:
            fail(f"key ({lo},{hi}) quarantined")
        if not is_canonical_safe_s5_key((lo, hi)):
            fail(f"key ({lo},{hi}) noncanonical")
        if mask_to_index.get((lo, hi)) != j:
            fail(f"key ({lo},{hi}) s5 index mismatch")
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
    if keyset & prior_pairs:
        fail("overlap with prior batches")

    batch_keys = {
        "schema": "n11-centralreply-closure-class5804-batch31-input-v1",
        "class_index": CLASS_INDEX,
        "class_mask": [str(CLASS_MASK[0]), str(CLASS_MASK[1])],
        "closure_class_rank_in_published_base": CLASS_RANK,
        "runner_up_class": RUNNER_UP_CLASS,
        "published_base_canonical_rows": CANONICAL_ROWS,
        "groups_served_count": len(CLASS_GROUPS),
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
    if mem_hist != Counter(MEMBERSHIP_HIST):
        fail(f"membership histogram {dict(mem_hist)} != pinned {MEMBERSHIP_HIST}")
    print(f"OK batch-31 keys: {len(keys)} keys class {CLASS_INDEX} rank {CLASS_RANK} "
          f"groups {CLASS_GROUPS} s5 ascending "
          f"{min(k['s5_index'] for k in keys)}..{max(k['s5_index'] for k in keys)} / "
          f"legal {min(k['legal'] for k in keys)}..{max(k['legal'] for k in keys)} "
          f"membership {dict(sorted(mem_hist.items()))} "
          f"canonical_hits 0 quarantine_hits 0 prior_packets {len(PRIOR_BATCHES)} rows {prior_rows} "
          f"unique {len(prior_pairs)} WIN77 {WIN_COUNT} "
          f"adoption_ties batch20_53_x_loss bz_6_loss ch_aa003_loss co_7_loss_cu_16_loss "
          f"class16957_{BZ_ADOPTED_CLASS_UNKNOWN} class13342_{BZ_ADOPTED_CLASS27_UNKNOWN} "
          f"class5343_{CO_ADOPTED_CLASS_UNKNOWN} class2251_{CU_ADOPTED_CLASS_UNKNOWN} "
          f"published_table_{CANDIDATE_ROWS}_rows_cross_checked "
          f"selection_pins_ranks_1_37_40_42 rank37_pkt_pinned first_clean_gate "
          f"runner_up {RUNNER_UP_CLASS} clean rank_38_39_only "
          f"prefix_ad_new verified")


if __name__ == "__main__":
    main()
