"""Batch-28 scaffold keys maker: closure class 5343 (Part CB, 2026-11-23).

Fail-closed, read-only generation of the batch-28 probe packet declared as
Part CB (note amendment, published before this scaffold is executed; the
declaration commit sha and observed-HEAD are recorded in the note text).
Target class: graph class index 5343, mask [1171516445255794688, 0].

SELECTION STATE (all machine-re-derived under the published base; nothing
taken from prose): the unconsumed-WIN set has grown to 29 keys (19 prior +
batch-21 a003 + batch-22 k002 + batch-23 s001/s002 + batch-24 y001/y006 +
batch-25 i001/i002 + batch-26 l028 + batch-27 o002); the canonical adopted
base is now the 6,293-row Part BZ merged cache (9115be9e..., containing the
batch-24 y002/y004 and batch-27 o001/o003/o005/o007 LOSS rows on top of the
Part BU 6,287-row adoption) PLUS the published update8 receipts.  Under that
base: rank 1 class 23101 is refuted via the unconsumed q042 WIN child
{745184}; rank 2 class 1849 via the unconsumed l028 WIN child {81011};
rank 6 class 13342 (the batch-27 target) via the published batch-27 honest
WIN row o002 = s5 209134 (a single-WIN refutation with 4 lineages: BR
drive-1, BY third-impl cross-verification, pinned-replica reproduction,
verdict NOT consumed); rank 10 class 16957 stays refuted via y001+y006
({91296, 368510}); rank 20 class 12643 via a003 ({115192}); rank 21 class
31600 via s001+s002 ({62435, 192809}); rank 24 class 25835 via k002
({150241}); rank 25 class 30565 via i001+i002 ({68580, 191299}).  Rank 19
class 5687 and rank 26 class 5690 remain route-dead via the update8 receipt
WIN child {209644}; rank 16 class 5830 via its 5 receipt WIN children.
Rank 22 class 10968 and rank 23 class 23964 remain packet-collision blocked
(NOT route-dead; collisions unchanged: 10968 = {273033} batch-12 n018,
23964 = {495193, 550880} batch-13 p007 + batch-4 e043).  NEW batch-28
machine fact: the published batch-27 packet now ALSO packet-collision-blocks
rank 28 class 13758 (exactly {459528} = batch-27 o031, fileless UNPROBED, the
declared Part CA continuation owns it) and rank 29 class 14103 (exactly
{460145} = batch-27 o037, fileless UNPROBED); ranks 30..34 (30484/34263/
16901/19749/23482) likewise collide with published packet keys.  Class 5343
at rank 27 (unknown 54 = its full cost set, known children {}, 29-WIN
intersection 0, no known WIN child, ZERO packet-key collision against all
28 published packets) is therefore the FIRST candidate in published-table
order whose all-LOSS closure route is alive AND which passes the full key
gates.  Runner-up: rank 35 class 2251 (route-alive, zero collision).
Backup: rank 36 class 34269 (route-alive, zero collision).

KEY ID PREFIX DESIGN (new): after batch-27, every single lowercase letter
is in use by the 28 published packets (a..z all present as 1-letter key id
prefixes; batch-27 took the last unused letter "o").  Batch-28 therefore
introduces a TWO-LETTER prefix: key ids aa001..aa054.  The maker pins this
new design with gates: every published packet key id matches the strict
1-letter format ^[a-z][0-9]{3}$ (so no published id can ever start with a
2-letter prefix) and no published key id starts with "aa".

Base-independence statement: the base of this maker is the PUBLISHED
adopted canonical exact-S5 verdict cache (6,293 rows, sha256 9115be9e...,
the Part BZ adoption output on main, containing the batch-24 y002/y004 and
batch-27 o001/o003/o005/o007 LOSS rows) PLUS the published update8 receipts
(repaired-joint-plan-update8.json, sha256 b658290a...).  The 54 probed
children of class 5343 are byte-derived from the pinned dependency graph
+ that adopted cache + those receipts; no unpublished artifact (probe
worklist etc.) is read.

NEW batch-28 gates beyond the batch-27 maker:
  * the unconsumed-WIN set is the 29 keys (19 prior + a003 + k002 + s001 +
    s002 + y001 + y006 + i001 + i002 + l028 + o002); every WIN key is
    re-derived from the sha-pinned published packets and must be absent
    from the canonical cache;
  * the Part BZ adoption tie (new): the 6 published keys batch-24 y002/y004
    (s5 166253/272083) and batch-27 o001/o003/o005/o007 (s5 98526/250515/
    348664/416288) must all be LOSS(2) rows of the adopted 6,293-row base;
    class 16957 must have exactly 51 unknown children and class 13342
    exactly 50 under that base (the Part BZ adoption is thereby
    machine-pinned, not trusted from prose);
  * the rank-6 refutation tie (new): unknown_now[13342] & 29-WIN set must
    equal exactly {209134} and class 13342 must have NO known WIN cost
    child (the Part BR/BY o002 row is machine-pinned as the rank-6
    refutation evidence from its published packet);
  * the rank-2 refutation tie (new): unknown_now[1849] must equal exactly
    {81011} (the batch-26 target retains only its unconsumed l028 WIN
    child) and RANK1_CHANGED likewise: unknown_now[23101] == {745184};
  * NEW packet-collision skips at ranks 28/29 (13758 = {459528} batch-27
    o031; 14103 = {460145} batch-27 o037; both fileless, both owned by the
    declared Part CA residual continuation and NOT re-probed here), plus
    extended EXPECTED_RANKS to rank 30 (30484) under the new base;
  * the two-letter prefix gates (1-letter format pin + "aa" freshness).

Carried over from the batch-27 maker (all re-gated here):
  * sha256 pins: graph, update8, Board, evidence policy, quarantine,
    canonical BASE cache (9115be9e..., published 6,293 rows), the
    published closure table (the Part BZ reaudit output, 807 rows) and
    the 28 published batch key packets (batches 1..27, fetched from the
    repo raw and sha-pinned);
  * published-table cross-check: the re-derived ranked closure table must
    agree with the PUBLISHED Part BZ reaudit closure table on every
    (rank -> class) pair and on the target class's unknown/groups row;
  * batch-20 adoption tie: all 53 published batch-20 x-key positions must
    be present in the adopted base cache with verdict LOSS(2), and the
    batch-20 packet's 53 keys must equal the re-derived class-12457
    resolution;
  * rank-20/21/24/25 structural gates: 12643 refuted exactly via {115192};
    31600 via {62435, 192809}; 25835 via {150241}; 30565 via {68580,
    191299}; ranked rows 19 and 26 must carry exactly the update8 receipt
    WIN child {209644} (route dead);
  * re-ranked closure gate: exact ranked list asserted for ranks 1..30;
    ranks 1..26 minus the packet-collision skips (22, 23) must each carry
    refutation evidence (29-WIN intersection OR a known WIN cost child);
    class 5830 must have exactly its 5 known WIN receipt children;
  * REST OF ROUTE-ALIVE GATE: the target class 5343 must have NO known
    WIN cost child and its known-child dictionary must be exactly {}
    (cost size 54, all unknown); runner-up 2251 and backup 34269 must
    have no known WIN child, no 29-WIN intersection and ZERO packet-key
    collision;
  * class gate: mask match, graph status unknown(1), cost size 54 with
    54 undetermined, groups served {(4,59),(4,114),(49,44),(49,54)};
  * key gates: 0/54 hits in the canonical 6,293-row cache; quarantine
    0/54 (published registry, pinned); canonical-safe key form 54/54;
    mask_to_index == derived s5 index 54/54; every key is a graph cost
    child of 5343; Board (independent.py) recomputes legal-move
    popcount 54/54 (no transcribed values); membership_class_count
    re-derived from the graph cost relation 54/54; every key DISJOINT
    from all published packet key positions (including every batch-27
    o-key, pinning the zero-collision selection);
  * overlap gate: the 54 keys are disjoint from all 28 published packet
    key sets (1,406 packet rows, 1,392 distinct positions;
    cross-packet shared 14 positions are membership bookkeeping as
    before);

Outputs: input/batch-keys.json (schema
n11-centralreply-closure-class5343-batch28-input-v1, key ids aa001..aa054
in ascending s5 index) and input/aa***.input.csv one-line solver targets
("target,0,5,lo,hi,legal,0,0,0,0,0").  Run 4x, byte-identical outputs.

Interpretation guard: this scaffold makes NO verdict claims.  The batch
itself (2-pass fresh-cold pinned replica, budget 15M, WIN-HALT rc=45
mismatch HARD-STOP rc=42 pre-registered) is executed only under the
declared Part CB protocol.  The standard 11x11 empty board, the 19
central-reply roots, class 5343, class 1849, class 13342, class 13758,
class 14103 and every key stay UNKNOWN; probe counts and legal counts are
bookkeeping, never verdicts.
"""
import csv
import gzip
import re
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
BZ_DIR = ROOT / "research/experiments/n11-centralreply-class16957-13342-loss6-adoption-reaudit-20261123"
BASE_CACHE = BZ_DIR / "output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-plus-batch20loss53-plus-batch26loss52-plus-batch24loss2-plus-batch27loss4-20261123.cache"
PUBLISHED_CLOSURE = BZ_DIR / "reaudit/output/closure-classes.csv"

CLASS_INDEX = 5343
CLASS_MASK = [1171516445255794688, 0]
CLASS_RANK = 27      # under the adopted 6,293-row base (published table);
# rank 22 class 10968 and rank 23 class 23964 stay packet-collision blocked
# (see PKT_COLLISION_SKIPS); rank 28 class 13758 and rank 29 class 14103
# are NEW packet-collision blocked via the published batch-27 packet
# (o031/o037, fileless UNPROBED, owned by the declared Part CA residual
# continuation); rank 19 class 5687 and rank 26 class 5690 are ROUTE-DEAD
# via the update8 receipt WIN child {209644}; ranks 1..26 (minus skips)
# all carry WIN refutation evidence under the 29-WIN set
RUNNER_UP_CLASS = 2251      # rank 35, route-alive + zero packet collision
BACKUP_CLASSES = [34269]   # rank 36, route-alive + zero packet collision
ROUTE_DEAD_RANK19_CLASS = 5687
ROUTE_DEAD_RANK26_CLASS = 5690
ROUTE_DEAD_RANK26_KNOWN_WIN = {209644}
PRIOR_SELECTED_CLASS = 5687   # rank 19: known-WIN child, route already dead
PRIOR_SELECTED_KNOWN_WIN = {209644}
CLASS_GROUPS = [(4, 59), (4, 114), (49, 44), (49, 54)]
UNPROBED = 54
COST_SIZE = 54
KNOWN_CHILDREN = {}   # class 5343 has NO base-resolved cost child
KEY_PREFIX = "aa"    # NEW 2-letter design: all 26 single letters are used
PRIOR_KEYID_RE = re.compile(r"^[a-z][0-9]{3}$")  # pin the 1-letter prior id format
CANDIDATE_ROWS = 807   # published-base re-derived candidate count
CANONICAL_ROWS = 6293  # adopted canonical (Part BZ merged adoption output)
BATCH20_PACKET = "n11-centralreply-closure-class12457-batch20-20261123"
BATCH21_PACKET = "n11-centralreply-closure-class12643-batch21-20261123"
BATCH22_PACKET = "n11-centralreply-closure-class25835-batch22-20261123"
BATCH23_PACKET = "n11-centralreply-closure-class31600-batch23-20261123"
BATCH24_PACKET = "n11-centralreply-closure-class16957-batch24-20261123"
BATCH25_PACKET = "n11-centralreply-closure-class30565-batch25-20261123"
BATCH26_PACKET = "n11-centralreply-closure-class1849-batch26-20261123"
BATCH27_PACKET = "n11-centralreply-closure-class13342-batch27-20261123"
BUDGET = 15000000

# ranked closure-candidate expectation under the adopted base
# (class, unknown_now).  Ranks 1..15 win-refuted via the 19-WIN set
# (rank 13 class 5830 additionally via 5 receipt WIN children); rank 16
# class 5687 refuted via its known-WIN child 209644 (route-alive gate).
EXPECTED_RANKS = [
    (1, 23101, 1), (2, 1849, 1), (3, 16757, 29), (4, 20421, 49),
    (5, 16371, 49), (6, 13342, 50), (7, 30345, 50), (8, 12264, 51),
    (9, 5473, 51), (10, 16957, 51), (11, 2634, 51), (12, 8785, 51),
    (13, 1518, 51), (14, 8106, 52), (15, 16930, 52), (16, 5830, 52),
    (17, 16131, 53), (18, 16513, 53), (19, 5687, 53), (20, 12643, 53),
    (21, 31600, 53), (22, 10968, 53), (23, 23964, 53), (24, 25835, 53),
    (25, 30565, 53), (26, 5690, 53), (27, 5343, 54), (28, 13758, 54),
    (29, 14103, 54), (30, 30484, 54),
]
RANK1_CLASS = 23101
RANK1_UNKNOWN = {745184}   # the unconsumed q042 WIN child only
RANK2_CLASS = 1849          # NEW batch-28 gate: the batch-26 target class
RANK2_UNKNOWN = {81011}    # retains exactly its unconsumed l028 WIN child
RECEIPT_WIN_CLASS = 5830     # rank 16: refuted via 5 receipt WIN children
RECEIPT_WIN_CHILDREN = {126017, 131631, 162106, 197665, 206386}
RESOLVED_BATCH20_CLASS = 12457   # class freed by the Part BI adoption
REFUTED_BATCH21_CLASS = 12643    # rank 20: refuted via the a003 honest WIN row
REFUTED_BATCH21_EVIDENCE = {115192}
REFUTED_BATCH22_CLASS = 25835    # rank 24: refuted via the k002 honest WIN row
REFUTED_BATCH22_EVIDENCE = {150241}
REFUTED_BATCH23_CLASS = 31600    # rank 21: refuted via the s001+s002 WIN pair
REFUTED_BATCH23_EVIDENCE = {62435, 192809}
REFUTED_BATCH24_CLASS = 16957    # rank 10: refuted via the y001+y006 WIN pair
REFUTED_BATCH24_EVIDENCE = {91296, 368510}
REFUTED_BATCH25_CLASS = 30565    # rank 25: refuted via the i001+i002 WIN pair
REFUTED_BATCH25_EVIDENCE = {68580, 191299}
REFUTED_BATCH27_CLASS = 13342    # rank 6: refuted via the o002 honest WIN row
REFUTED_BATCH27_EVIDENCE = {209134}
# Part BZ adoption tie (NEW): the 6 LOSS rows adopted by Part BZ must be
# visible in the base; their s5 indices are pinned here
BZ_ADOPTED_CLASS = 16957
BZ_ADOPTED_CLASS_UNKNOWN = 51     # 53 -> 51 after the y002/y004 adoption
BZ_ADOPTED_CLASS27 = 13342
BZ_ADOPTED_CLASS27_UNKNOWN = 50   # 54 -> 50 after the o001/o003/o005/o007 adoption
BZ_ADOPTED_KEYS = [
    ("y002", BATCH24_PACKET, 166253), ("y004", BATCH24_PACKET, 272083),
    ("o001", BATCH27_PACKET, 98526), ("o003", BATCH27_PACKET, 250515),
    ("o005", BATCH27_PACKET, 348664), ("o007", BATCH27_PACKET, 416288),
]
# packet-collision BLOCKED classes (blocked, NOT refuted): their unknown
# sets collide with published packet key positions; the collided keys of
# the NEW rank-28/29 skips are fileless batch-27 keys owned by the
# declared Part CA residual continuation (never re-probed here)
PKT_COLLISION_SKIPS = [
    # rank 22 class 10968: exactly one colliding key: batch-12 n018
    (10968, {273033}, "n11-centralreply-closure-class8106-batch12-20261122",
     {"n018"}),
    # rank 23 class 23964: exactly two colliding keys: batch-13 p007
    # and batch-4 e043 (both UNPROBED; recorded for future selections)
    (23964, {495193, 550880},
     "n11-centralreply-closure-class16930-batch13-20261122",
     {"p007"}),
    # rank 28 class 13758: exactly one colliding key: batch-27 o031
    # (fileless, UNPROBED, Part CA residual continuation owns it)
    (13758, {459528}, BATCH27_PACKET, {"o031"}),
    # rank 29 class 14103: exactly one colliding key: batch-27 o037
    # (fileless, UNPROBED, Part CA residual continuation owns it)
    (14103, {460145}, BATCH27_PACKET, {"o037"}),
]
PKT_COLLISION_SECOND_PACKETS = {
    # the second colliding key of class 23964 comes from batch-4 e043
    (23964, 550880): ("n11-centralreply-closure-class16371-batch4-20261122",
                      {"e043"}),
}

PIN_SHA = {
    "graph": "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b",
    "update8": "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719",
    "board": "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f",
    "policy": "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2",
    "quarantine": "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9",
    "canonical_base_cache": "9115be9eca1e60828a90c50041f511b598ef79fc0be76d5e16821816e478e93e",
    "published_closure": "14fc37c3a6f5c6753cac72a094d2c7693defb4a5e483558b3b87a42016b679d9",
}

# batches 1..26 published key packets (raw main, sha256-pinned)
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
    (BATCH21_PACKET, 53,
     "1f9346a7027e95b162f27b933bddec05151473d87ab7ed35832619026ae6759d"),
    (BATCH22_PACKET, 53,
     "b5f567bd72835ebfe347d7363f3d244565757deb8e8572b6fb2820625ae39035"),
    (BATCH23_PACKET, 53,
     "2776acafbb638cb148661b3988b7eb36bc8519e5b7b75b415b01618bfcb85bf7"),
    (BATCH24_PACKET, 53,
     "486858d6e2de0662ef38a6ff1fd61c1c0dcf6e9b09012c2c32fdd99153d096cc"),
    (BATCH25_PACKET, 53,
     "272c0c134e3be17838311d0d3f18f09340d09094d35e15197481c999892390a5"),
    (BATCH26_PACKET, 53,
     "f1ea43aef6ee06c918885a9007ad3f347d96aa198180e87bf3eb14d783304cdd"),
    (BATCH27_PACKET, 54,
     "67814ed6287d68d6e97212c931dce2b7ee585219e20b4d43edb621632220a014"),
]
EXPECTED_PRIOR_ROWS = 1406
EXPECTED_PRIOR_UNIQUE = 1392

RAW = "https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/main/research/experiments/"

# unconsumed closure WIN keys (published batch packets, result 1, never
# adopted into canonical; scrutiny owner C++ second implementation pending):
# 19 prior + a003 + k002 + s001 + s002 + y001 + y006 + i001 + i002 + l028
# + o002 = 29
WIN_KEYS = [
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
]


def fail(msg):
    print("GATE FAILED: " + msg, file=sys.stderr)
    raise SystemExit(1)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
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

    # canonical cache (published Part BI adopted output, 6,235 rows) + receipts
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
    # NOTE: an S5 position may serve several closure classes (high
    # membership_class_count); the same (lo,hi) can legitimately appear
    # in more than one published packet.  The union below therefore tracks
    # per-(dirname, key_id) identity and records cross-packet shared
    # positions as bookkeeping instead of failing.
    prior_by_id = {}
    prior_pairs = set()
    shared_pairs = []
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
            if k["key_id"].startswith(KEY_PREFIX):
                fail(f"key id prefix {KEY_PREFIX!r} already used in {dirname}")
            if not PRIOR_KEYID_RE.match(k["key_id"]):
                fail(f"prior key id {k['key_id']!r} violates the pinned 1-letter format")
            lo_hi = (int(k["lo"]), int(k["hi"]))
            prior_by_id[(dirname, k["key_id"])] = lo_hi
            if lo_hi in prior_pairs:
                shared_pairs.append((lo_hi, dirname, k["key_id"]))
            else:
                prior_pairs.add(lo_hi)
    if prior_rows != EXPECTED_PRIOR_ROWS:
        fail(f"prior key rows {prior_rows} != expected {EXPECTED_PRIOR_ROWS}")
    if len(prior_pairs) != EXPECTED_PRIOR_UNIQUE:
        fail(f"prior unique positions {len(prior_pairs)} != expected {EXPECTED_PRIOR_UNIQUE}")

    # unconsumed-WIN re-derivation gate
    win_s5 = set()
    for kid, dirname, want_s5 in WIN_KEYS:
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
    if len(win_s5) != 29:
        fail(f"WIN s5 set {len(win_s5)} != 29")

    # NEW batch-24 PKT-COLLISION SKIP GATE (machine bookkeeping of the
    # rank-20 discovery; blocked classes, NOT refutations):
    # (a) the published packet identities of every prior key are indexed
    #     by position so a collision is attributed machine-side;
    # (b) each declared skip class collides with prior packets in EXACTLY
    #     the pinned s5 keys and packet key ids;
    # (c) the skip classes carry NO WIN refutation evidence (unknown &
    #     win_s5 empty and known_win empty) - if one ever acquires WIN
    #     evidence it is a refutation, not a skip, and this maker must
    #     fail instead of skipping;
    # (d) the batch-26 target class must NOT appear in the skip list
    #     (it passed the per-key overlap gate; pinned here again).
    prior_ids_by_pos = {}
    for (dirname, kid), lo_hi in prior_by_id.items():
        prior_ids_by_pos.setdefault(lo_hi, []).append((dirname, kid))
    for cls, want_s5, want_pkt, want_kids in PKT_COLLISION_SKIPS:
        got_s5 = {j for j in unknown_now[cls]
                  if (int(s5_masks[j][0]), int(s5_masks[j][1])) in prior_pairs}
        if got_s5 != want_s5:
            fail(f"PKT-collision gate: class {cls} collision s5 set {sorted(got_s5)} != "
                 f"pinned {sorted(want_s5)} (published base drift)")
        ids = set()
        for j in got_s5:
            lo, hi = int(s5_masks[j][0]), int(s5_masks[j][1])
            ids.update(prior_ids_by_pos.get((lo, hi), []))
        want_ids = {(want_pkt, k) for k in want_kids}
        for (c, sj), (pk, kids) in PKT_COLLISION_SECOND_PACKETS.items():
            if c == cls and sj in want_s5:
                want_ids |= {(pk, k) for k in kids}
        if ids != want_ids:
            fail(f"PKT-collision gate: class {cls} collision key ids {sorted(ids)} != "
                 f"pinned {sorted(want_ids)}")
        if unknown_now[cls] & win_s5:
            fail(f"PKT-collision gate: class {cls} NOW carries WIN refutation evidence "
                 f"{sorted(unknown_now[cls] & win_s5)}; it must be recorded as a "
                 "refutation, not a skip")
        if known_win.get(cls, set()):
            fail(f"PKT-collision gate: class {cls} NOW has known WIN cost children; "
                 "it must be recorded as a refutation, not a skip")
        if cls == CLASS_INDEX:
            fail("PKT-collision gate: the target class must not be a collision skip")

    # NEW gate: batch-20 adoption tie.  Every published batch-20 x-key must
    # be LOSS in the adopted base cache, and the x-key set must equal the
    # re-derived resolution of class 12457 (its unknown set must be empty,
    # i.e. the Part BI free-class classification is machine-pinned here).
    b20_x = []
    for (dirname, kid), lo_hi in prior_by_id.items():
        if dirname == BATCH20_PACKET and kid.startswith("x"):
            b20_x.append((kid, lo_hi))
    BATCH20_X_KEYS = 53
    if len(b20_x) != BATCH20_X_KEYS:
        fail(f"batch-20 packet x-keys {len(b20_x)} != {BATCH20_X_KEYS}")
    for kid, lo_hi in sorted(b20_x):
        if cache.get(lo_hi) != 2:
            fail(f"batch-20 key {kid} {lo_hi} not a LOSS(2) row of the adopted base")
    if unknown_now[RESOLVED_BATCH20_CLASS]:
        fail(f"class {RESOLVED_BATCH20_CLASS} still has {len(unknown_now[RESOLVED_BATCH20_CLASS])}"
             " unknown children (Part BI adoption not visible in the base)")

    # NEW gate: Part BZ adoption tie.  The 6 LOSS rows adopted by Part BZ
    # (batch-24 y002/y004 + batch-27 o001/o003/o005/o007) must be present
    # in the adopted 6,293-row base cache; classes 16957 and 13342 must
    # have shrunk to exactly 51 / 50 unknown children (the Part BZ
    # adoption is machine-pinned from its published packets, not prose).
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
        fail(f"BZ adoption tie: class {BZ_ADOPTED_CLASS} unknown {len(unknown_now[BZ_ADOPTED_CLASS])}"
             f" != pinned {BZ_ADOPTED_CLASS_UNKNOWN}")
    if len(unknown_now[BZ_ADOPTED_CLASS27]) != BZ_ADOPTED_CLASS27_UNKNOWN:
        fail(f"BZ adoption tie: class {BZ_ADOPTED_CLASS27} unknown {len(unknown_now[BZ_ADOPTED_CLASS27])}"
             f" != pinned {BZ_ADOPTED_CLASS27_UNKNOWN}")

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
    # refutation evidence gate for every class ahead of the target
    # except the packet-collision skips (ranks 22, 23):
    # 29-WIN intersection OR a known WIN cost child (refresh-exclusion rule)
    for rank, cls, _ in [r for r in EXPECTED_RANKS[:26] if r[0] not in (22, 23)]:
        ev_win = unknown_now[cls] & win_s5
        ev_known = known_win.get(cls, set())
        if not ev_win and not ev_known:
            fail(f"selection gate: rank {rank} class {cls} carries NO refutation evidence")
    if unknown_now[RANK1_CLASS] != RANK1_UNKNOWN:
        fail(f"rank 1 class {RANK1_CLASS} unknown set {sorted(unknown_now[RANK1_CLASS])} != {sorted(RANK1_UNKNOWN)}")
    # rank 2 class 1849 (the batch-26 target; NEW batch-28 gate): after the
    # Part BU 52-LOSS adoption it retains exactly its unconsumed l028 WIN child
    if unknown_now[RANK2_CLASS] != RANK2_UNKNOWN:
        fail(f"rank 2 class {RANK2_CLASS} unknown set {sorted(unknown_now[RANK2_CLASS])} != {sorted(RANK2_UNKNOWN)}")
    # rank 20 class 12643 (the batch-21 target): refuted precisely via the
    # published Part BJ honest WIN row a003 = s5 115192 (unconsumed)
    if unknown_now[REFUTED_BATCH21_CLASS] & win_s5 != REFUTED_BATCH21_EVIDENCE:
        fail(f"selection gate: class {REFUTED_BATCH21_CLASS} WIN-intersection evidence "
             f"{sorted(unknown_now[REFUTED_BATCH21_CLASS] & win_s5)} != {sorted(REFUTED_BATCH21_EVIDENCE)}")
    if known_win.get(REFUTED_BATCH21_CLASS, set()):
        fail(f"selection gate: class {REFUTED_BATCH21_CLASS} unexpectedly has known WIN children")
    # rank 24 class 25835 (the batch-22 target): refuted precisely via the
    # published Part BL honest WIN row k002 = s5 150241 (unconsumed)
    if unknown_now[REFUTED_BATCH22_CLASS] & win_s5 != REFUTED_BATCH22_EVIDENCE:
        fail(f"selection gate: class {REFUTED_BATCH22_CLASS} 27-WIN evidence "
             f"{sorted(unknown_now[REFUTED_BATCH22_CLASS] & win_s5)} != {sorted(REFUTED_BATCH22_EVIDENCE)}")
    if known_win.get(REFUTED_BATCH22_CLASS, set()):
        fail(f"selection gate: class {REFUTED_BATCH22_CLASS} unexpectedly has known WIN children")
    # rank 21 class 31600 (the batch-23 target): refuted precisely via the
    # published Part BN honest WIN rows s001 + s002 (s5 {62435, 192809},
    # the first WIN-PAIR refutation inside one class, unconsumed)
    if unknown_now[REFUTED_BATCH23_CLASS] & win_s5 != REFUTED_BATCH23_EVIDENCE:
        fail(f"selection gate: class {REFUTED_BATCH23_CLASS} WIN-intersection evidence "
             f"{sorted(unknown_now[REFUTED_BATCH23_CLASS] & win_s5)} != {sorted(REFUTED_BATCH23_EVIDENCE)}")
    if known_win.get(REFUTED_BATCH23_CLASS, set()):
        fail(f"selection gate: class {REFUTED_BATCH23_CLASS} unexpectedly has known WIN children")
    # rank 10 class 16957 (the batch-24 target): refuted precisely via the
    # published batch-24 Part BO honest WIN rows y001 + y006 (s5 91296 +
    # 368510, the second WIN-PAIR refutation inside one class, unconsumed)
    if unknown_now[REFUTED_BATCH24_CLASS] & win_s5 != REFUTED_BATCH24_EVIDENCE:
        fail(f"selection gate: class {REFUTED_BATCH24_CLASS} 27-WIN evidence "
             f"{sorted(unknown_now[REFUTED_BATCH24_CLASS] & win_s5)} != {sorted(REFUTED_BATCH24_EVIDENCE)}")
    if known_win.get(REFUTED_BATCH24_CLASS, set()):
        fail(f"selection gate: class {REFUTED_BATCH24_CLASS} unexpectedly has known WIN children")
    # rank 25 class 30565 (the batch-25 target): refuted precisely via the
    # published batch-25 Part BP honest WIN rows i001 + i002 (s5 68580 +
    # 191299, the THIRD WIN-PAIR refutation inside one class, unconsumed)
    if unknown_now[REFUTED_BATCH25_CLASS] & win_s5 != REFUTED_BATCH25_EVIDENCE:
        fail(f"selection gate: class {REFUTED_BATCH25_CLASS} 27-WIN evidence "
             f"{sorted(unknown_now[REFUTED_BATCH25_CLASS] & win_s5)} != {sorted(REFUTED_BATCH25_EVIDENCE)}")
    if known_win.get(REFUTED_BATCH25_CLASS, set()):
        fail(f"selection gate: class {REFUTED_BATCH25_CLASS} unexpectedly has known WIN children")
    # rank 6 class 13342 (the batch-27 target): refuted precisely via the
    # published batch-27 Part BR honest single WIN row o002 (s5 209134,
    # the FOURTH single-WIN refutation after a003, k002 and l028,
    # unconsumed; lineages: BR drive-1 + BY third-impl cross-verification
    # + pinned-replica reproduction)
    if unknown_now[REFUTED_BATCH27_CLASS] & win_s5 != REFUTED_BATCH27_EVIDENCE:
        fail(f"selection gate: class {REFUTED_BATCH27_CLASS} 29-WIN evidence "
             f"{sorted(unknown_now[REFUTED_BATCH27_CLASS] & win_s5)} != {sorted(REFUTED_BATCH27_EVIDENCE)}")
    if known_win.get(REFUTED_BATCH27_CLASS, set()):
        fail(f"selection gate: class {REFUTED_BATCH27_CLASS} unexpectedly has known WIN children")
    # rank 26 class 5690: route dead via exactly the update8 receipt WIN
    # child 209644 - pinned so the exclusion is bookkeeping, not prose
    if known_win.get(ROUTE_DEAD_RANK26_CLASS, set()) != ROUTE_DEAD_RANK26_KNOWN_WIN:
        fail(f"route-dead gate: class {ROUTE_DEAD_RANK26_CLASS} known-WIN children "
             f"{known_win.get(ROUTE_DEAD_RANK26_CLASS, set())} != {ROUTE_DEAD_RANK26_KNOWN_WIN}")
    if unknown_now[ROUTE_DEAD_RANK26_CLASS] & win_s5:
        fail(f"route-dead gate: class {ROUTE_DEAD_RANK26_CLASS} unexpectedly intersects the 29-WIN set")
    # rank 13 class 5830: refuted via exactly the five receipt WIN children
    if known_win.get(RECEIPT_WIN_CLASS, set()) != RECEIPT_WIN_CHILDREN:
        fail(f"selection gate: class {RECEIPT_WIN_CLASS} known-WIN children"
             f" {known_win.get(RECEIPT_WIN_CLASS, set())} != {RECEIPT_WIN_CHILDREN}")
    # rank 19 class 5687: precisely the known-WIN child 209644, zero 29-WIN
    if unknown_now[PRIOR_SELECTED_CLASS] & win_s5:
        fail("selection gate: class 5687 unexpectedly intersects the 29-WIN set")
    if known_win.get(PRIOR_SELECTED_CLASS, set()) != PRIOR_SELECTED_KNOWN_WIN:
        fail(f"selection gate: class 5687 known-WIN children {known_win.get(PRIOR_SELECTED_CLASS, set())} != {PRIOR_SELECTED_KNOWN_WIN}")
    cls_unknown = unknown_now[CLASS_INDEX]
    if cls_unknown & win_s5:
        fail("selection gate: class 5343 unknown children intersect the 29-WIN set")
    if len(cls_unknown) != UNPROBED:
        fail(f"class 5343 re-derived unknown children {len(cls_unknown)} != {UNPROBED}")
    if known_win.get(CLASS_INDEX, set()):
        fail("route-alive gate: class 5343 has a known WIN cost child")
    derived_known = {j: iv[j] for j in cost_set if iv.get(j) is not None}
    if derived_known != KNOWN_CHILDREN:
        fail(f"route-alive gate: class 5343 known children {derived_known} != declared {KNOWN_CHILDREN}")
    groups = sorted(best_class_groups.get(CLASS_INDEX, []))
    if groups != sorted(CLASS_GROUPS):
        fail(f"re-derived groups for class {CLASS_INDEX} {groups} != declared {sorted(CLASS_GROUPS)}")
    # runner-up and backup must also be route-alive
    for cls in [RUNNER_UP_CLASS] + BACKUP_CLASSES:
        if known_win.get(cls, set()):
            fail(f"runner-up/backup class {cls} has a known WIN cost child (route dead)")
        if cls in best_class_groups and unknown_now[cls] & win_s5:
            fail(f"runner-up/backup class {cls} intersects the 29-WIN set")
        ov = {j for j in unknown_now[cls]
              if (int(s5_masks[j][0]), int(s5_masks[j][1])) in prior_pairs}
        if ov:
            fail(f"runner-up/backup class {cls} packet-collides with published keys "
                 f"{sorted(ov)} (declare a PKT skip instead)")

    # NEW gate: published-table cross-check (Part BI refresh reaudit output).
    # The re-derived ranking must agree with the published closure table on
    # every (rank -> class) pair, and on the target row's unknown/groups.
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
        dcls, dgroups = ranked[rank - 1]
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
        "schema": "n11-centralreply-closure-class5343-batch28-input-v1",
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
    # completeness + durability check: every written file must re-read
    # byte-identical (guards against transient fs hiccups observed on
    # this host: freshly written CSVs can transiently disappear or come
    # back short; a batch runner reading inputs must never see that)
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
    print(f"OK batch-28 keys: {len(keys)} keys class {CLASS_INDEX} rank {CLASS_RANK} "
          f"groups {CLASS_GROUPS} s5 ascending "
          f"{min(k['s5_index'] for k in keys)}..{max(k['s5_index'] for k in keys)} / "
          f"legal {min(k['legal'] for k in keys)}..{max(k['legal'] for k in keys)} "
          f"membership {dict(sorted(mem_hist.items()))} "
          f"canonical_hits 0 quarantine_hits 0 overlap 0 prior_packets 28/{prior_rows} rows "
          f"unique {len(prior_pairs)} shared_prior_positions {len(shared_pairs)} "
          f"ranks_1_to_26_minus_skips_refuted rank2_1849_unknown_eq_81011 "
          f"rank6_13342_via_o002_eq_209134 rank10_16957_via_y001y006_eq_91296_368510 "
          f"rank20_12643_via_a003_eq_115192 rank21_31600_via_s001s002_eq_62435_192809 "
          f"rank24_25835_via_k002_eq_150241 rank25_30565_via_i001i002_eq_68580_191299 "
          f"rank19_5687_and_rank26_5690_route_dead_known_win_eq_209644 "
          f"pkt_skip_rank22_10968_eq_273033_n018 pkt_skip_rank23_23964_eq_495193_p007_550880_e043 "
          f"pkt_skip_rank28_13758_eq_459528_o031 pkt_skip_rank29_14103_eq_460145_o037 "
          f"5830_receipt_wins_eq_5 5687_known_win_eq_209644 29-WIN disjoint "
          f"route_alive_known_children_empty_5343 bz_adoption_tie_6_loss_rows_in_base "
          f"class16957_unknown_eq_51 class13342_unknown_eq_50 "
          f"published_table_807_rows_cross_checked batch20_x_keys_all_loss_in_base "
          f"runner_up {RUNNER_UP_CLASS} backup {BACKUP_CLASSES} "
          f"zero_collision_runner_up_backup_verified "
          f"prefix_aa_new_2letter_prior_ids_all_1letter_pin verified")


if __name__ == "__main__":
    main()
