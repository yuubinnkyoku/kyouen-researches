#!/usr/bin/env python3
"""Batch-18 scaffold keys maker: closure class 16131 (Part AY, 2026-11-22).

Fail-closed, read-only generation of the batch-18 probe packet declared as
Part AY (note amendment, declaration push before this scaffold commit).
Target class: graph class index 16131, mask [1154047404513693696, 64].

Base-independence statement: the base of this maker is the PUBLISHED
canonical exact-S5 verdict cache (6,120 rows, sha256 be9cb24e..., Part AS
adoption output on main).  The 53 probed children of class 16131 are
byte-derived from the pinned dependency graph + that published cache;
none of Part AV's unpublished artifacts are read.  Machine fact recorded
by the Part AY declaration: class 16131's unknown-child set is identical
under the published 6,120-row base and under the Part AV declared
6,172-row post-adoption base (the batch-17 keys are class 10661's
children, not 16131's), so this packet does not depend on whether Part
AV publishes first.

Selection gate under the published base (re-derived here, nothing taken
from prose): re-ranked closure-candidate table = 809 classes; rank 1-13
(23101/16757/20421/16371/30345/12264/5473/2634/8785/1518/8106/16930/5830)
each intersect the 15 unconsumed closure WIN children (win-refuted
closure routes); rank 14 (class 10661, unknown 52) intersects NO
unconsumed WIN but ALL 52 unknown children are already probed by the
published batch-17 packet (52/52 two-pass LOSS rows, verdict consumption
pending the separately declared Part AV adoption); class 16131 at rank
15 (unknown 53) is the first candidate with no refutation evidence and
no already-probed children.  Rank 16 (class 16513) recorded as runner-up.

Authoritative key derivation (no worklist input): the 53 keys are the
graph cost children of class 16131 absent from the published canonical
cache (plus update8 receipts), ordered by ascending s5 index -> key ids
v001..v053.  Every downstream fact is re-derived and gated here:

  * sha256 pins: graph, update8, Board, evidence policy, quarantine,
    canonical BASE cache (be9cb24e..., published 6,120 rows) and the 18
    published batch key packets (batches 1-17 plus the batch-14 residual
    packet, fetched from the repo raw and sha-pinned);
  * the 15 unconsumed closure WIN keys are re-derived from the sha-pinned
    published batch packets (key_id -> lo,hi -> graph mask_to_index) and
    must equal the declared s5 indices; none may appear in the canonical
    cache (unconsumed) and none may be a batch-18 key;
  * re-ranked closure gate: exact ranked list asserted for ranks 1..16;
    ranks 1..13 WIN-refuted; rank 14 class 10661 fully probed by the
    published batch-17 packet (unknown set == packet key set), no WIN
    intersection; class 16131 rank 15, unknown 53, WIN intersection 0;
  * class gate: mask match, graph status unknown(1), cost size 53 =
    all 53 children undetermined, groups served
    {(12,50),(12,70),(48,20),(48,72),(48,100)};
  * key gates: 0/53 hits in the canonical 6,120-row cache; quarantine
    0/53 (published registry, pinned); canonical-safe key form 53/53;
    mask_to_index == derived s5 index 53/53; every key is a graph cost
    child of 16131; Board (independent.py) recomputes legal-move
    popcount 53/53 (no transcribed values); membership_class_count
    re-derived from the graph cost relation 53/53;
  * overlap gate: the 53 keys are disjoint from all 18 published packet
    key sets (875 packet rows, 861 distinct positions; 4 cross-packet
    shared positions recorded as bookkeeping, not failures).

Outputs: input/batch-keys.json (schema
n11-centralreply-closure-class16131-batch18-input-v1, key ids v001..v053
in ascending s5 index) and input/v***.input.csv one-line solver targets
("target,0,5,lo,hi,legal,0,0,0,0,0").  Run 3x, byte-identical outputs.

Interpretation guard: this scaffold makes NO verdict claims.  The batch
itself (2-pass fresh-cold pinned replica, budget 15M, WIN-HALT rc=45 /
mismatch HARD-STOP rc=42 pre-registered) is executed by a later run
under the declared protocol.  The standard 11x11 empty board, the 19
central-reply roots, class 16131 and every key stay UNKNOWN; probe
counts and legal counts are bookkeeping, never verdicts.
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
AS_DIR = ROOT / "research/experiments/n11-centralreply-class23101-loss41-adoption-reaudit-20261122"
BASE_CACHE = AS_DIR / "output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-20261122.cache"

CLASS_INDEX = 16131
CLASS_MASK = [1154047404513693696, 64]
CLASS_RANK = 15      # under the published 6,120-row base
RUNNER_UP_CLASS = 16513
CLASS_GROUPS = [(12, 50), (12, 70), (48, 20), (48, 72), (48, 100)]
UNPROBED = 53
COST_SIZE = 53
KEY_PREFIX = "v"
CANDIDATE_ROWS = 809   # published-base re-derived candidate count
CANONICAL_ROWS = 6120  # published canonical (Part AS output)
BUDGET = 15000000

# ranked closure-candidate expectation under the published base
# (class, unknown_now).  Ranks 1-13 win-refuted; rank 14 fully probed.
EXPECTED_RANKS = [
    (1, 23101, 11), (2, 16757, 29), (3, 20421, 49), (4, 16371, 49),
    (5, 30345, 50), (6, 12264, 51), (7, 5473, 51), (8, 2634, 51),
    (9, 8785, 51), (10, 1518, 51), (11, 8106, 52), (12, 16930, 52),
    (13, 5830, 52), (14, 10661, 52), (15, 16131, 53), (16, 16513, 53),
]
FULLY_PROBED_CLASS = 10661    # rank 14; all children probed by batch-17

PIN_SHA = {
    "graph": "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b",
    "update8": "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719",
    "board": "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f",
    "policy": "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2",
    "quarantine": "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9",
    "canonical_base_cache": "be9cb24e899fbe93db51e415320c50fa733e378748bb7a41fe13fd7b22f06685",
}

# batches 1..17 + batch-14 residual published key packets (raw main,
# sha256-pinned)
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
]
EXPECTED_PRIOR_ROWS = 875
EXPECTED_PRIOR_UNIQUE = 861   # 4 cross-packet shared positions

RAW = "https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/main/research/experiments/"

# 15 unconsumed closure WIN keys (published batch packets, result 1, never
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
]

BATCH17_PACKET = "n11-centralreply-closure-class10661-batch17-20261122"


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
                          ("canonical cache", BASE_CACHE, PIN_SHA["canonical_base_cache"])):
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

    # canonical cache (published Part AS output, 6,120 rows) + receipts
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
    unknown_now = {}
    for i in range(len(s4_masks)):
        base = s4_status[i]
        if base == EXCLUDED:
            unknown_now[i] = set()
            continue
        if base not in (LOSS, UNKNOWN):
            fail(f"unexpected graph status {base} at class {i}")
        unknown_now[i] = {j for j in s4_cost[i] if iv.get(j) is None}

    # published batch packets: sha-pinned fetch, key dicts
    # NOTE: an S5 position may serve several closure classes (high
    # membership_class_count); the same (lo,hi) can legitimately appear
    # in more than one published packet (observed: e042 in batch-4 class
    # 16371 and p028 in batch-13 class 16930 are the same position).
    # The union below therefore tracks per-(dirname, key_id) identity and
    # records cross-packet shared positions as bookkeeping instead of
    # failing.
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
    if len(win_s5) != 15:
        fail(f"WIN s5 set {len(win_s5)} != 15")

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
    for rank, cls, _ in EXPECTED_RANKS[:13]:
        if not (unknown_now[cls] & win_s5):
            fail(f"selection gate: rank {rank} class {cls} unknown children do NOT intersect the 15-WIN set")
    fp = FULLY_PROBED_CLASS
    if unknown_now[fp] & win_s5:
        fail("selection gate: fully-probed class 10661 unexpectedly intersects the WIN set")
    fp_pairs = {tuple(s5_masks[j]) for j in unknown_now[fp]}
    if not fp_pairs <= prior_pairs:
        fail("selection gate: class 10661 has unknown children NOT probed by a published packet")
    if len(fp_pairs) != 52:
        fail(f"class 10661 unknown children {len(fp_pairs)} != 52")
    cls_unknown = unknown_now[CLASS_INDEX]
    if cls_unknown & win_s5:
        fail("selection gate: class 16131 unknown children intersect the 15-WIN set")
    if len(cls_unknown) != UNPROBED:
        fail(f"class 16131 re-derived unknown children {len(cls_unknown)} != {UNPROBED}")
    groups = sorted(best_class_groups.get(CLASS_INDEX, []))
    if groups != sorted(CLASS_GROUPS):
        fail(f"re-derived groups for class {CLASS_INDEX} {groups} != declared {sorted(CLASS_GROUPS)}")

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
        "schema": "n11-centralreply-closure-class16131-batch18-input-v1",
        "class_index": CLASS_INDEX,
        "class_mask": [str(CLASS_MASK[0]), str(CLASS_MASK[1])],
        "closure_class_rank_in_published_base": CLASS_RANK,
        "runner_up_class": RUNNER_UP_CLASS,
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
    if len(list(OUTDIR.glob('v*.input.csv'))) != UNPROBED:
        fail(f"input CSV count {len(list(OUTDIR.glob('v*.input.csv')))} != {UNPROBED}")
    bk_blob = bk_path.read_bytes()
    if len(json.loads(bk_blob)["keys"]) != UNPROBED:
        fail("batch-keys.json re-read mismatch")
    print(f"OK batch-18 keys: {len(keys)} keys class {CLASS_INDEX} rank {CLASS_RANK} "
          f"groups {CLASS_GROUPS} s5 ascending "
          f"legal {min(k['legal'] for k in keys)}..{max(k['legal'] for k in keys)} "
          f"canonical_hits 0 quarantine_hits 0 overlap 0 prior_packets 18/{prior_rows} rows "
          f"unique {len(prior_pairs)} shared_prior_positions {len(shared_pairs)} "
          f"ranks_1_to_13_win_refuted rank14_class_10661_fully_probed_by_batch17 verified, "
          f"15-WIN disjoint, runner_up {RUNNER_UP_CLASS}")


if __name__ == "__main__":
    main()
