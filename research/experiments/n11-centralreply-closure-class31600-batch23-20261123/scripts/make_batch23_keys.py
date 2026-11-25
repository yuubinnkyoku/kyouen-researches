#!/usr/bin/env python3
"""Batch-23 scaffold keys maker: closure class 31600 (Part BN, 2026-11-23).

Fail-closed, read-only generation of the batch-23 probe packet declared as
Part BN (note amendment, published before this scaffold is executed; the
declaration commit sha and observed-HEAD are recorded in the note text).
Target class: graph class index 31600, mask [1152921505160495104, 32768].

Base-independence statement: the base of this maker is the PUBLISHED
adopted canonical exact-S5 verdict cache (6,235 rows, sha256 f6649fe3...,
Part BI adoption output on main, containing the batch-20 class-12457
53-LOSS rows) PLUS the published update8 receipts
(repaired-joint-plan-update8.json, sha256 b658290a...).  The 53 probed
children of class 31600 are byte-derived from the pinned dependency graph
+ that adopted cache + those receipts; no unpublished artifact (probe
worklist etc.) is read.

Selection gate under the published base (re-derived here, nothing taken
from prose): re-ranked closure-candidate table = 807 classes (class 12457
exited by the Part BI adoption); ranks 1..16 (23101/16757/20421/16371/
30345/12264/5473/2634/8785/1518/8106/16930/5830/16131/16513/5687) each
carry refutation evidence of one of the two published kinds (19 unconsumed
closure WIN children intersection, OR a known WIN cost child: class 5830
via five receipt WIN children {126017,131631,162106,197665,206386}, class
5687 via the update8 receipt WIN child {209644}; rank 1 class 23101's
unknown set is exactly the unconsumed q042 WIN child {745184}); rank 17
class 12643 (the batch-21 target) is refuted via the PUBLISHED batch-21
Part BJ honest WIN row a003 (key (10412339930666631168, 4), Part BK
third-implementation corroborated, verdict NOT consumed): its unknown
child set intersects the unconsumed-WIN set in exactly {115192}; rank 18
class 25835 (the batch-22 target) is refuted the same way via the
PUBLISHED batch-22 Part BL honest WIN row k002 (s5 150241, two-host
pinned-replica plus third-implementation corroborated, verdict NOT
consumed): its unknown child set intersects the unconsumed-WIN set in
exactly {150241}.  Class 31600 at rank 19 (unknown 53 = its full
cost set, known children {}, WIN intersection 0, no known WIN child) is
therefore the FIRST candidate in published-table order whose all-LOSS
closure route is alive.  Runner-up: rank 20 class 10968 (route-alive,
cost 53 all unknown); backup rank 21 class 16957 (route-alive).

NEW batch-23 gates beyond the batch-22 maker:
  * the unconsumed-WIN set is the 21 keys (19 prior + batch-21 a003 +
    batch-22 k002); every WIN key is re-derived from the sha-pinned
    published packets and must be absent from the canonical cache;
  * the rank-17 refutation tie: unknown_now[12643] & WIN set must equal
    exactly {115192} and class 12643 must have NO known WIN cost child
    (the Part BJ a003 row is machine-pinned as the rank-17 refutation
    evidence from its published packet, not trusted from prose);
  * the rank-18 refutation tie: unknown_now[25835] & WIN set must equal
    exactly {150241} and class 25835 must have NO known WIN cost child
    (the Part BL k002 row is machine-pinned as the rank-18 refutation
    evidence from its published packet, not trusted from prose);

Carried over from the batch-21 maker (all re-gated here):
  * sha256 pins: graph, update8, Board, evidence policy, quarantine,
    canonical BASE cache (f6649fe3..., published 6,235 rows), the
    published closure table (d57a7609...) and the 23 published batch key
    packets (batches 1-22, fetched from the repo raw and sha-pinned);
  * published-table cross-check: the re-derived ranked closure table must
    agree with the PUBLISHED Part BI refresh reaudit closure table
    (closure-classes.csv, sha256 d57a7609..., 807 rows) on every
    (rank -> class) pair and on the target class's unknown/groups row;
  * batch-20 adoption tie: all 53 published batch-20 x-key positions must
    be present in the adopted base cache with verdict LOSS(2), and the
    batch-20 packet's 53 keys must equal the re-derived class-12457
    resolution (the Part BI adoption is thereby machine-pinned from its
    published packet, not trusted from prose);
  * re-ranked closure gate: exact ranked list asserted for ranks 1..19;
    ranks 1..18 must each carry refutation evidence (21-WIN intersection
    OR a known WIN cost child); class 5687 must have exactly the known
    WIN child {209644}; rank 1 class 23101's unknown set is exactly
    {745184};
  * REST OF ROUTE-ALIVE GATE: the target class 31600 must have NO known
    WIN cost child and its known-child dictionary must be exactly {}
    (cost size 53, all unknown); runner-up 10968 and backup 16957 must
    also have no known WIN child and no 21-WIN intersection;
  * class gate: mask match, graph status unknown(1), cost size 53 with
    53 undetermined, groups served {(24,29),(24,79),(25,30),(25,85)};
  * key gates: 0/53 hits in the canonical 6,235-row cache; quarantine
    0/53 (published registry, pinned); canonical-safe key form 53/53;
    mask_to_index == derived s5 index 53/53; every key is a graph cost
    child of 31600; Board (independent.py) recomputes legal-move
    popcount 53/53 (no transcribed values); membership_class_count
    re-derived from the graph cost relation 53/53;
  * overlap gate: the 53 keys are disjoint from all 23 published packet
    key sets (1,140 packet rows, 1,126 distinct positions);
  * key id gate: prefix "s" is unused by every one of the 23 published
    packets (key ids s001..s053 are unique across batches 1..23).

Outputs: input/batch-keys.json (schema
n11-centralreply-closure-class31600-batch23-input-v1, key ids s001..s053
in ascending s5 index) and input/s***.input.csv one-line solver targets
("target,0,5,lo,hi,legal,0,0,0,0,0").  Run 3x, byte-identical outputs.

Interpretation guard: this scaffold makes NO verdict claims.  The batch
itself (2-pass fresh-cold pinned replica, budget 15M, WIN-HALT rc=45
mismatch HARD-STOP rc=42 pre-registered) is executed only under the
declared Part BN protocol.  The standard 11x11 empty board, the 19
central-reply roots, class 12643, class 25835, class 31600 and every key
stay UNKNOWN; probe counts
and legal counts are bookkeeping, never verdicts.
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
BI_DIR = ROOT / "research/experiments/n11-centralreply-class12457-loss53-adoption-reaudit-20261123"
BASE_CACHE = BI_DIR / "output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-plus-batch20loss53-20261123.cache"
PUBLISHED_CLOSURE = BI_DIR / "reaudit/output/closure-classes.csv"

CLASS_INDEX = 31600
CLASS_MASK = [1152921505160495104, 32768]
CLASS_RANK = 19      # under the adopted 6,235-row base (published table)
RUNNER_UP_CLASS = 10968      # rank 20, route-alive
BACKUP_CLASSES = [16957]     # rank 21, route-alive
CLASS_GROUPS = [(24, 29), (24, 79), (25, 30), (25, 85)]
UNPROBED = 53
COST_SIZE = 53
KNOWN_CHILDREN = {}   # class 31600 has NO base-resolved cost child
KEY_PREFIX = "s"
CANDIDATE_ROWS = 807   # published-base re-derived candidate count
CANONICAL_ROWS = 6235  # adopted canonical (Part BI adoption output)
BATCH20_PACKET = "n11-centralreply-closure-class12457-batch20-20261123"
BATCH21_PACKET = "n11-centralreply-closure-class12643-batch21-20261123"
BATCH22_PACKET = "n11-centralreply-closure-class25835-batch22-20261123"
BUDGET = 15000000

# ranked closure-candidate expectation under the adopted base
# (class, unknown_now).  Ranks 1..15 win-refuted via the 19-WIN set
# (rank 13 class 5830 additionally via 5 receipt WIN children); rank 16
# class 5687 refuted via its known-WIN child 209644 (route-alive gate).
EXPECTED_RANKS = [
    (1, 23101, 1), (2, 16757, 29), (3, 20421, 49), (4, 16371, 49),
    (5, 30345, 50), (6, 12264, 51), (7, 5473, 51), (8, 2634, 51),
    (9, 8785, 51), (10, 1518, 51), (11, 8106, 52), (12, 16930, 52),
    (13, 5830, 52), (14, 16131, 53), (15, 16513, 53), (16, 5687, 53),
    (17, 12643, 53), (18, 25835, 53), (19, 31600, 53),
]
RANK1_CLASS = 23101
RANK1_UNKNOWN = {745184}   # the unconsumed q042 WIN child only
PRIOR_SELECTED_CLASS = 5687   # rank 16: known-WIN child, route already dead
PRIOR_SELECTED_KNOWN_WIN = {209644}
RECEIPT_WIN_CLASS = 5830     # rank 13: refuted via 5 receipt WIN children
RECEIPT_WIN_CHILDREN = {126017, 131631, 162106, 197665, 206386}
RESOLVED_BATCH20_CLASS = 12457   # class freed by the Part BI adoption
REFUTED_BATCH21_CLASS = 12643    # rank 17: refuted via the a003 honest WIN row
REFUTED_BATCH21_EVIDENCE = {115192}
REFUTED_BATCH22_CLASS = 25835    # rank 18: refuted via the k002 honest WIN row
REFUTED_BATCH22_EVIDENCE = {150241}

PIN_SHA = {
    "graph": "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b",
    "update8": "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719",
    "board": "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f",
    "policy": "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2",
    "quarantine": "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9",
    "canonical_base_cache": "f6649fe36425f9a4e959b058392746b73e655cda0fcfa223befafd8905d67d26",
    "published_closure": "d57a760926aa609554ca916da80afde5dc0b500c03dc9482b1ef4dee40ad5e52",
}

# batches 1..22 published key packets (raw main, sha256-pinned)
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
]
EXPECTED_PRIOR_ROWS = 1140
EXPECTED_PRIOR_UNIQUE = 1126

RAW = "https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/main/research/experiments/"

# 19 unconsumed closure WIN keys (published batch packets, result 1, never
# adopted into canonical; scrutiny owner C++ second implementation pending)
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
    if len(win_s5) != 21:
        fail(f"WIN s5 set {len(win_s5)} != 21")

    # NEW gate: batch-20 adoption tie.  Every published batch-20 x-key must
    # be LOSS in the adopted base cache, and the x-key set must equal the
    # re-derived resolution of class 12457 (its unknown set must be empty,
    # i.e. the Part BI free-class classification is machine-pinned here).
    b20_x = []
    for (dirname, kid), lo_hi in prior_by_id.items():
        if dirname == BATCH20_PACKET and kid.startswith("x"):
            b20_x.append((kid, lo_hi))
    if len(b20_x) != UNPROBED:
        fail(f"batch-20 packet x-keys {len(b20_x)} != {UNPROBED}")
    for kid, lo_hi in sorted(b20_x):
        if cache.get(lo_hi) != 2:
            fail(f"batch-20 key {kid} {lo_hi} not a LOSS(2) row of the adopted base")
    if unknown_now[RESOLVED_BATCH20_CLASS]:
        fail(f"class {RESOLVED_BATCH20_CLASS} still has {len(unknown_now[RESOLVED_BATCH20_CLASS])}"
             " unknown children (Part BI adoption not visible in the base)")

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
    # refutation evidence gate for every class ahead of the target:
    # 19-WIN intersection OR a known WIN cost child (refresh-exclusion rule)
    for rank, cls, _ in EXPECTED_RANKS[:18]:
        ev_win = unknown_now[cls] & win_s5
        ev_known = known_win.get(cls, set())
        if not ev_win and not ev_known:
            fail(f"selection gate: rank {rank} class {cls} carries NO refutation evidence")
    if unknown_now[RANK1_CLASS] != RANK1_UNKNOWN:
        fail(f"rank 1 class {RANK1_CLASS} unknown set {sorted(unknown_now[RANK1_CLASS])} != {sorted(RANK1_UNKNOWN)}")
    # rank 17 class 12643 (the batch-21 target): refuted precisely via the
    # published Part BJ honest WIN row a003 = s5 115192 (unconsumed)
    if unknown_now[REFUTED_BATCH21_CLASS] & win_s5 != REFUTED_BATCH21_EVIDENCE:
        fail(f"selection gate: class {REFUTED_BATCH21_CLASS} WIN-intersection evidence "
             f"{sorted(unknown_now[REFUTED_BATCH21_CLASS] & win_s5)} != {sorted(REFUTED_BATCH21_EVIDENCE)}")
    if known_win.get(REFUTED_BATCH21_CLASS, set()):
        fail(f"selection gate: class {REFUTED_BATCH21_CLASS} unexpectedly has known WIN children")
    # rank 18 class 25835 (the batch-22 target): refuted precisely via the
    # published Part BL honest WIN row k002 = s5 150241 (unconsumed)
    if unknown_now[REFUTED_BATCH22_CLASS] & win_s5 != REFUTED_BATCH22_EVIDENCE:
        fail(f"selection gate: class {REFUTED_BATCH22_CLASS} 21-WIN evidence "
             f"{sorted(unknown_now[REFUTED_BATCH22_CLASS] & win_s5)} != {sorted(REFUTED_BATCH22_EVIDENCE)}")
    if known_win.get(REFUTED_BATCH22_CLASS, set()):
        fail(f"selection gate: class {REFUTED_BATCH22_CLASS} unexpectedly has known WIN children")
    # rank 13 class 5830: refuted via exactly the five receipt WIN children
    if known_win.get(RECEIPT_WIN_CLASS, set()) != RECEIPT_WIN_CHILDREN:
        fail(f"selection gate: class {RECEIPT_WIN_CLASS} known-WIN children"
             f" {known_win.get(RECEIPT_WIN_CLASS, set())} != {RECEIPT_WIN_CHILDREN}")
    # rank 16 class 5687: precisely the known-WIN child 209644, zero 19-WIN
    if unknown_now[PRIOR_SELECTED_CLASS] & win_s5:
        fail("selection gate: class 5687 unexpectedly intersects the 19-WIN set")
    if known_win.get(PRIOR_SELECTED_CLASS, set()) != PRIOR_SELECTED_KNOWN_WIN:
        fail(f"selection gate: class 5687 known-WIN children {known_win.get(PRIOR_SELECTED_CLASS, set())} != {PRIOR_SELECTED_KNOWN_WIN}")
    cls_unknown = unknown_now[CLASS_INDEX]
    if cls_unknown & win_s5:
        fail("selection gate: class 31600 unknown children intersect the 21-WIN set")
    if len(cls_unknown) != UNPROBED:
        fail(f"class 31600 re-derived unknown children {len(cls_unknown)} != {UNPROBED}")
    if known_win.get(CLASS_INDEX, set()):
        fail("route-alive gate: class 31600 has a known WIN cost child")
    derived_known = {j: iv[j] for j in cost_set if iv.get(j) is not None}
    if derived_known != KNOWN_CHILDREN:
        fail(f"route-alive gate: class 31600 known children {derived_known} != declared {KNOWN_CHILDREN}")
    groups = sorted(best_class_groups.get(CLASS_INDEX, []))
    if groups != sorted(CLASS_GROUPS):
        fail(f"re-derived groups for class {CLASS_INDEX} {groups} != declared {sorted(CLASS_GROUPS)}")
    # runner-up and backup must also be route-alive
    for cls in [RUNNER_UP_CLASS] + BACKUP_CLASSES:
        if known_win.get(cls, set()):
            fail(f"runner-up/backup class {cls} has a known WIN cost child (route dead)")
        if cls in best_class_groups and unknown_now[cls] & win_s5:
            fail(f"runner-up/backup class {cls} intersects the 21-WIN set")

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
        "schema": "n11-centralreply-closure-class31600-batch23-input-v1",
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
    if len(list(OUTDIR.glob('s*.input.csv'))) != UNPROBED:
        fail(f"input CSV count {len(list(OUTDIR.glob('s*.input.csv')))} != {UNPROBED}")
    bk_blob = bk_path.read_bytes()
    if len(json.loads(bk_blob)["keys"]) != UNPROBED:
        fail("batch-keys.json re-read mismatch")
    print(f"OK batch-23 keys: {len(keys)} keys class {CLASS_INDEX} rank {CLASS_RANK} "
          f"groups {CLASS_GROUPS} s5 ascending "
          f"legal {min(k['legal'] for k in keys)}..{max(k['legal'] for k in keys)} "
          f"canonical_hits 0 quarantine_hits 0 overlap 0 prior_packets 23/{prior_rows} rows "
          f"unique {len(prior_pairs)} shared_prior_positions {len(shared_pairs)} "
          f"ranks_1_to_18_refuted rank17_12643_via_a003_eq_115192 "
          f"rank1_class_23101_unknown_eq_745184 verified "
          f"rank18_25835_via_k002_eq_150241 5830_receipt_wins_eq_5 5687_known_win_eq_209644 21-WIN disjoint "
          f"route_alive_known_children_empty_31600 "
          f"published_table_807_rows_cross_checked batch20_x_keys_all_loss_in_base "
          f"runner_up {RUNNER_UP_CLASS} prefix_s_unused verified")


if __name__ == "__main__":
    main()
