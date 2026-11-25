#!/usr/bin/env python3
"""make_batch38_keys.py - batch-38 (n11 central-reply closure class 30345)
key derivation with fail-closed gates.

Scope: the 49 fresh (never-probed, honest-label-free, canonically-unresolved,
quarantine-free) unknown cost-children of closure class 30345 (class_rank 12,
mask [1152922604118478848, 65536]) in the published post-af034loss1-adoption
reaudit (refresh-summary.json 6af660a1..., closure-classes.csv 27e00b0d...,
canonical cache fc3e4ac9..., probe-worklist.csv regen pin b4933810...).

Class-30345 accounting (50 == 1 + 49, all machine-derived):
  - 1 unknown child is pair-identical to batch-1 key b018 (class 16757
    packet, 2026-11-22, dual-class 16757/30345): probed honest-label WIN
    PASS 15000000,1,3549602 with the pre-registered WIN-HALT marker; the
    WIN verdict was never consumed into the canonical chain (it requires
    the scrutiny-owner C++ gate), so the child stays unknown in the
    closure table. It is NOT a batch-38 target (same-condition re-probe
    prohibited; it is owned by the pending scrutiny path).
  - 49 children are fresh: absent from the canonical cache (no verdict
    row), absent from the prior-probe universe (2,104 unique (lo,hi)
    positions actually probed by published n11 batches/status logs,
    serialized ascending as prior-probe-universe.csv sha 6deee846...),
    and not quarantined. They are the batch-38 targets ai001..ai049 in
    worklist probe_order (132..139, 141..181; probe_order 140 is the
    prior-packeted b018 child).

Fresh-frontier selection basis (machine re-derived in the declaring
session, no prose): closure ranks 1..11 (classes 23101, 1849, 2251,
16371, 16757, 5804, 34908, 20421, 34269, 5343, 13342) have ALL of their
remaining 131 unknown children inside the prior-probe universe
(fresh 0), so no same-condition new probe can open there without first
consuming existing honest labels through the scrutiny/adoption path.
Class 30345 (rank 12) is the first ranked class with fresh children
(49). freshness-ranks1to12.csv (sha e5f51717...) records that scan; its
re-derivation needs only published bytes (dependency-graph 54f9c364...
+ update8 receipts + independent.py 954d3a10... + policy 78655e94...
+ quarantine 81d23160... + canonical cache fc3e4ac9... via the published
refresh fork 01937f23..., whose 4 outputs the declaring environment
reproduced byte-identically, regen pin b4933810...).

Gates (all fail-closed, rc=1 on any violation, no partial outputs on
failure):
  G1  source sha pins: batch-1 packet (2 files) + refresh-summary +
      closure-classes + canonical cache + quarantine + worklist
      class-30345 extract + prior-probe-universe + freshness table
      must match the pinned sha256 values byte-exactly.
  G2  batch-1 packet integrity: 48 keys b001..b048; b018 row matches
      the embedded prior child field-for-field; status.log contains
      exactly one b018 PASS row with budget/result/nodes 15000000/1/
      3549602 plus the b018 WIN-HALT marker row.
  G3  closure-classes.csv rank 12 == class 30345 with unknown_now 50
      and mask match; accounting 50 == 1 (prior dual-class probe-level
      WIN unconsumed) + 49 (fresh targets).
  G3b freshness table: ranks 1..11 all-fresh-0 rows (children ==
      unknown_now == prior_probe, cache_hit 0, fresh 0); rank 12 row
      children == 50, prior_probe == 1, fresh == 49 == len(targets);
      class indices agree with closure-classes.csv rank anchors.
  G4  exact key pairs (lo,hi) of all 50 unknown children (49 targets +
      the unconsumed b018 pair) absent from the canonical merged chain
      cache (pair-level parse of all s5verdict rows; same-lo rows are
      counted and reported as context, never adopted).
  G5  none of the 50 pairs (49 targets + b018) appears in the active
      quarantine registry.
  G6  worklist class-30345 extract: exactly 50 rows, probe_order
      132..181 contiguous ascending, serving_class 30345,
      class_unknown_now 50; every row matches an embedded child
      (target or prior) on (lo, hi, legal, s5_index,
      membership_class_count); the b018 child sits at probe_order 140;
      target probe_orders strictly ascend with ai id order.
  G7  prior-probe universe: 2,104 unique ascending (lo,hi) lines; none
      of the 49 target pairs is in the universe (freshness); the b018
      prior pair IS in the universe.

Outputs (written atomically only after all gates pass):
  input/ai001.input.csv ... input/ai049.input.csv (49 files)
      (format: target,0,5,lo,hi,legal,0,0,0,0,0 - identical schema to
       the published batch-31..37 inputs)
  input/batch-keys-b38.json
      schema n11-centralreply-closure-batch38-keys-v1, pins included,
      consumed_into_canonical_cache=false

Determinism: pure function of the pinned inputs; run 3x byte-identical
in the completion protocol. Tamper battery (scratch copies) must ABORT
on: pin drift, batch-1 packet field drift, status drift, cache hit,
quarantine hit, closure-table rank drift, freshness-table drift,
worklist extract field drift, universe drift.
"""
import hashlib
import json
import os
import re
import sys

PIN_B1_KEYS = "2aaccc941d7aec35c416b27d5cdd10f7fbb82c9801bcf560b61e20be88c331f8"
PIN_B1_STATUS = "559a0884d4c728c05a992bcf144661fbd8212bc09d2c8b56341aebe7b94348b1"
PIN_REFRESH_SUMMARY = "6af660a1e0ad8f0ad3b0ac6b32c1a24099aa8f1c3a2271496a9bfb99dc80b6bc"
PIN_CLOSURE_CLASSES = "27e00b0dbf2f33603dfbed91b00153f73c7a2d05b1258133a39c9ec5bfd41364"
PIN_CANONICAL_CACHE = "fc3e4ac9052447158202f09d5efe05468dba32fe95ec90beaaa0a0de9d2c020f"
PIN_QUARANTINE = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
PIN_WORKLIST_EXTRACT = "7fe5551327f1ac65e2ce1477b5dde8ab03a7cae23aa0be86ce4821c8c3dc7a72"
PIN_UNIVERSE = "6deee846a4e67778437cd052502535f4839f3fbe76d5e1ec9bc9b6c0036e942b"
PIN_FRESHNESS = "e5f517177778102d2313da5bb6b46c3084c9a99c11323b750407b0f1919da148"

CLASS_INDEX = 30345
CLASS_MASK = [1152922604118478848, 65536]
CLASS_RANK = 12
CLASS_UNKNOWN_NOW = 50
WORKLIST_ORDER_FIRST = 132
WORKLIST_ORDER_LAST = 181
UNIVERSE_PAIRS = 2104

# the 1 prior-probed dual-class child (batch-1 b018, 2026-11-22, probe-level
# honest WIN, never consumed into the canonical chain, scrutiny-owner C++
# gate pending). NOT a batch-38 target; gate-checked for bookkeeping
# consistency (packet row + status PASS row + WIN-HALT marker + cache
# absence + quarantine absence + worklist position + universe membership).
EMBEDDED_PRIOR = [
        {"batch1_key_id": "b018", "probe_order": 140, "lo": 1153204079095189504, "hi": 65536, "legal": 60, "s5_index": 528497, "membership_class_count": 3}
]
PROBED_BUDGET, PROBED_RESULT, PROBED_NODES = 15000000, 1, 3549602

# the 49 fresh targets, embedded from the pinned worklist extract rows
# (verified against the pinned published file at run time; probe_order 140
# = the prior b018 child is excluded).
EMBEDDED_TARGETS = [
    {"key_id": "ai001", "probe_order": 132, "lo": 1152922604252696576, "hi": 65536, "legal": 83, "s5_index": 39148, "membership_class_count": 3},
    {"key_id": "ai002", "probe_order": 133, "lo": 1153485554071900160, "hi": 65536, "legal": 74, "s5_index": 151694, "membership_class_count": 4},
    {"key_id": "ai003", "probe_order": 134, "lo": 3458765613332172800, "hi": 65536, "legal": 79, "s5_index": 195012, "membership_class_count": 4},
    {"key_id": "ai004", "probe_order": 135, "lo": 5764608622545866752, "hi": 65536, "legal": 87, "s5_index": 298570, "membership_class_count": 4},
    {"key_id": "ai005", "probe_order": 136, "lo": 1152922604118544384, "hi": 65536, "legal": 87, "s5_index": 355799, "membership_class_count": 4},
    {"key_id": "ai006", "probe_order": 137, "lo": 1152922604118478848, "hi": 65537, "legal": 88, "s5_index": 391735, "membership_class_count": 4},
    {"key_id": "ai007", "probe_order": 138, "lo": 1152922604118478880, "hi": 65536, "legal": 84, "s5_index": 441292, "membership_class_count": 4},
    {"key_id": "ai008", "probe_order": 139, "lo": 1152922604118478848, "hi": 65538, "legal": 87, "s5_index": 473959, "membership_class_count": 4},
    {"key_id": "ai009", "probe_order": 141, "lo": 1152922741557432320, "hi": 65536, "legal": 78, "s5_index": 604944, "membership_class_count": 4},
    {"key_id": "ai010", "probe_order": 142, "lo": 1152923153874292736, "hi": 65536, "legal": 78, "s5_index": 624629, "membership_class_count": 4},
    {"key_id": "ai011", "probe_order": 143, "lo": 1152922604118478848, "hi": 66048, "legal": 82, "s5_index": 657234, "membership_class_count": 4},
    {"key_id": "ai012", "probe_order": 144, "lo": 1152922604185587712, "hi": 65536, "legal": 87, "s5_index": 716150, "membership_class_count": 4},
    {"key_id": "ai013", "probe_order": 145, "lo": 1152922604386914304, "hi": 65536, "legal": 78, "s5_index": 731678, "membership_class_count": 4},
    {"key_id": "ai014", "probe_order": 146, "lo": 1157426203745849344, "hi": 65536, "legal": 79, "s5_index": 753317, "membership_class_count": 4},
    {"key_id": "ai015", "probe_order": 147, "lo": 1152922604118478848, "hi": 66560, "legal": 91, "s5_index": 754556, "membership_class_count": 4},
    {"key_id": "ai016", "probe_order": 148, "lo": 1152922604118511616, "hi": 65536, "legal": 83, "s5_index": 800006, "membership_class_count": 4},
    {"key_id": "ai017", "probe_order": 149, "lo": 1161929803373219840, "hi": 65536, "legal": 81, "s5_index": 826581, "membership_class_count": 4},
    {"key_id": "ai018", "probe_order": 150, "lo": 1152922604118478848, "hi": 67584, "legal": 91, "s5_index": 827502, "membership_class_count": 4},
    {"key_id": "ai019", "probe_order": 151, "lo": 1152922604118478912, "hi": 65536, "legal": 91, "s5_index": 866157, "membership_class_count": 4},
    {"key_id": "ai020", "probe_order": 152, "lo": 1170937002627960832, "hi": 65536, "legal": 87, "s5_index": 878758, "membership_class_count": 4},
    {"key_id": "ai021", "probe_order": 153, "lo": 1152922604118478848, "hi": 69632, "legal": 78, "s5_index": 879412, "membership_class_count": 4},
    {"key_id": "ai022", "probe_order": 154, "lo": 1152922604118479360, "hi": 65536, "legal": 90, "s5_index": 888325, "membership_class_count": 4},
    {"key_id": "ai023", "probe_order": 155, "lo": 1152922604120576000, "hi": 65536, "legal": 85, "s5_index": 888357, "membership_class_count": 4},
    {"key_id": "ai024", "probe_order": 156, "lo": 1152922604118479104, "hi": 65536, "legal": 86, "s5_index": 889534, "membership_class_count": 4},
    {"key_id": "ai025", "probe_order": 157, "lo": 1152922608413446144, "hi": 65536, "legal": 90, "s5_index": 889976, "membership_class_count": 4},
    {"key_id": "ai026", "probe_order": 158, "lo": 1152922604118478976, "hi": 65536, "legal": 87, "s5_index": 891015, "membership_class_count": 4},
    {"key_id": "ai027", "probe_order": 159, "lo": 1152931400211501056, "hi": 65536, "legal": 85, "s5_index": 891592, "membership_class_count": 4},
    {"key_id": "ai028", "probe_order": 160, "lo": 1152921573327372288, "hi": 1056768, "legal": 76, "s5_index": 892997, "membership_class_count": 4},
    {"key_id": "ai029", "probe_order": 161, "lo": 1152922604118478852, "hi": 65536, "legal": 89, "s5_index": 893644, "membership_class_count": 4},
    {"key_id": "ai030", "probe_order": 162, "lo": 1152921573327372288, "hi": 17825792, "legal": 91, "s5_index": 894456, "membership_class_count": 4},
    {"key_id": "ai031", "probe_order": 163, "lo": 1152922604118478850, "hi": 65536, "legal": 84, "s5_index": 894824, "membership_class_count": 4},
    {"key_id": "ai032", "probe_order": 164, "lo": 1152921573327372288, "hi": 34360786944, "legal": 89, "s5_index": 895608, "membership_class_count": 4},
    {"key_id": "ai033", "probe_order": 165, "lo": 1152922604118478849, "hi": 65536, "legal": 80, "s5_index": 895907, "membership_class_count": 3},
    {"key_id": "ai034", "probe_order": 166, "lo": 1152921573326324736, "hi": 68720525312, "legal": 74, "s5_index": 896605, "membership_class_count": 3},
    {"key_id": "ai035", "probe_order": 167, "lo": 1152922672837955584, "hi": 65536, "legal": 84, "s5_index": 897030, "membership_class_count": 3},
    {"key_id": "ai036", "probe_order": 168, "lo": 1152922604119003136, "hi": 65536, "legal": 82, "s5_index": 897221, "membership_class_count": 4},
    {"key_id": "ai037", "probe_order": 169, "lo": 1152922606265962496, "hi": 65536, "legal": 89, "s5_index": 897427, "membership_class_count": 4},
    {"key_id": "ai038", "probe_order": 170, "lo": 1152927002164989952, "hi": 65536, "legal": 89, "s5_index": 898436, "membership_class_count": 4},
    {"key_id": "ai039", "probe_order": 171, "lo": 1152921573327372288, "hi": 1064960, "legal": 87, "s5_index": 899303, "membership_class_count": 4},
    {"key_id": "ai040", "probe_order": 172, "lo": 1152922604118487040, "hi": 65536, "legal": 85, "s5_index": 899584, "membership_class_count": 4},
    {"key_id": "ai041", "probe_order": 173, "lo": 1152921573327372288, "hi": 34603008, "legal": 91, "s5_index": 900170, "membership_class_count": 4},
    {"key_id": "ai042", "probe_order": 174, "lo": 1152922604655349760, "hi": 65536, "legal": 86, "s5_index": 900292, "membership_class_count": 4},
    {"key_id": "ai043", "probe_order": 175, "lo": 1152922604152033280, "hi": 65536, "legal": 74, "s5_index": 900322, "membership_class_count": 4},
    {"key_id": "ai044", "probe_order": 176, "lo": 1152922604135256064, "hi": 65536, "legal": 72, "s5_index": 900354, "membership_class_count": 3},
    {"key_id": "ai045", "probe_order": 177, "lo": 1152924803141734400, "hi": 65536, "legal": 86, "s5_index": 900436, "membership_class_count": 4},
    {"key_id": "ai046", "probe_order": 178, "lo": 1152921573327372288, "hi": 1081344, "legal": 80, "s5_index": 900561, "membership_class_count": 4},
    {"key_id": "ai047", "probe_order": 179, "lo": 1152921573327372288, "hi": 1114112, "legal": 82, "s5_index": 900716, "membership_class_count": 3},
    {"key_id": "ai048", "probe_order": 180, "lo": 1152921573327372288, "hi": 68157440, "legal": 68, "s5_index": 900718, "membership_class_count": 3},
    {"key_id": "ai049", "probe_order": 181, "lo": 1152921573327372288, "hi": 68720525312, "legal": 72, "s5_index": 900719, "membership_class_count": 1},
]

SCHEMA = "n11-centralreply-closure-batch38-keys-v1"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(msg):
    sys.stderr.write("ABORT: %s\n" % msg)
    sys.exit(1)


def main():
    kit_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = os.path.join(kit_root, "sources")
    b1 = os.path.join(src, "batch1-packet")
    cache_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(src, "canonical-cache-fc3e4ac9.cache")
    quarantine_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(src, "quarantine.json")
    refresh_path = sys.argv[3] if len(sys.argv) > 3 else os.path.join(src, "refresh-summary.json")
    closure_path = sys.argv[4] if len(sys.argv) > 4 else os.path.join(src, "closure-classes.csv")
    worklist_path = sys.argv[5] if len(sys.argv) > 5 else os.path.join(src, "worklist-class30345-extract.csv")
    universe_path = sys.argv[6] if len(sys.argv) > 6 else os.path.join(src, "prior-probe-universe.csv")
    freshness_path = sys.argv[7] if len(sys.argv) > 7 else os.path.join(src, "freshness-ranks1to12.csv")
    b1_keys_path = sys.argv[8] if len(sys.argv) > 8 else os.path.join(b1, "batch-keys.json")
    b1_status_path = sys.argv[9] if len(sys.argv) > 9 else os.path.join(b1, "status.log")

    # G1 source pins
    for path, pin, what in [
        (b1_keys_path, PIN_B1_KEYS, "batch-1 batch-keys"),
        (b1_status_path, PIN_B1_STATUS, "batch-1 status.log"),
        (refresh_path, PIN_REFRESH_SUMMARY, "refresh-summary"),
        (closure_path, PIN_CLOSURE_CLASSES, "closure-classes"),
        (cache_path, PIN_CANONICAL_CACHE, "canonical cache"),
        (quarantine_path, PIN_QUARANTINE, "quarantine"),
        (worklist_path, PIN_WORKLIST_EXTRACT, "worklist class-30345 extract"),
        (universe_path, PIN_UNIVERSE, "prior-probe universe"),
        (freshness_path, PIN_FRESHNESS, "freshness table ranks 1..12"),
    ]:
        if sha256_file(path) != pin:
            fail("G1 pin mismatch on %s (%s)" % (what, path))

    # G2 batch-1 packet integrity (the prior b018 child provenance)
    with open(b1_keys_path, "r", encoding="utf-8") as f:
        packet = json.load(f)
    keys = packet.get("keys", [])
    if len(keys) != 48:
        fail("G2 batch-1 packet has %d keys, want 48" % len(keys))
    ids = [k.get("key_id") for k in keys]
    if ids != ["b%03d" % i for i in range(1, 49)]:
        fail("G2 batch-1 packet id set drift")
    pkt = {k["key_id"]: k for k in keys}
    p = EMBEDDED_PRIOR[0]
    row = pkt.get(p["batch1_key_id"])
    if row is None:
        fail("G2 batch-1 packet missing b018")
    for field in ("lo", "hi", "legal", "s5_index", "membership_class_count"):
        if row.get(field) != p[field]:
            fail("G2 b018 field %s drift: packet %r embedded %r" % (field, row.get(field), p[field]))
    pass_re = re.compile(r"^\S+ (b\d{3}) PASS (\d+),(\d+),(\d+)$")
    halt_re = re.compile(r"^\S+ (b\d{3}) WIN-HALT$")
    pass_rows = {}
    halt_rows = []
    with open(b1_status_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            m = pass_re.match(line)
            if m:
                if m.group(1) in pass_rows:
                    fail("G2 batch-1 status.log duplicate PASS row for %s" % m.group(1))
                pass_rows[m.group(1)] = (int(m.group(2)), int(m.group(3)), int(m.group(4)))
                continue
            m = halt_re.match(line)
            if m:
                halt_rows.append(m.group(1))
    if p["batch1_key_id"] not in pass_rows:
        fail("G2 batch-1 status.log missing b018 PASS row")
    got = pass_rows[p["batch1_key_id"]]
    if got != (PROBED_BUDGET, PROBED_RESULT, PROBED_NODES):
        fail("G2 batch-1 status.log b018 PASS row drift: %r" % (got,))
    if halt_rows != [p["batch1_key_id"]]:
        fail("G2 batch-1 status.log WIN-HALT rows drift: %r" % (halt_rows,))
    for kid in pass_rows:
        if kid not in pkt:
            fail("G2 batch-1 status.log PASS id %s absent from packet" % kid)

    # G3 closure-classes rank anchor + accounting
    with open(closure_path, "r", encoding="utf-8") as f:
        rows = [line.rstrip("\n").split(",") for line in f if line.strip()]
    if rows[0][:2] != ["class_rank", "class_index"]:
        fail("G3 closure-classes header drift")
    by_rank = {r[0]: r for r in rows[1:]}
    crow = by_rank.get(str(CLASS_RANK))
    if crow is None or crow[1] != str(CLASS_INDEX):
        fail("G3 rank %d is not class %d" % (CLASS_RANK, CLASS_INDEX))
    if crow[4] != str(CLASS_UNKNOWN_NOW):
        fail("G3 class %d unknown_now %s, want %d" % (CLASS_INDEX, crow[4], CLASS_UNKNOWN_NOW))
    if crow[2] != str(CLASS_MASK[0]) or crow[3] != str(CLASS_MASK[1]):
        fail("G3 class %d mask drift" % CLASS_INDEX)
    if CLASS_UNKNOWN_NOW != len(EMBEDDED_PRIOR) + len(EMBEDDED_TARGETS):
        fail("G3 accounting: %d != %d (prior) + %d (fresh)"
             % (CLASS_UNKNOWN_NOW, len(EMBEDDED_PRIOR), len(EMBEDDED_TARGETS)))
    rank_class = {}
    for r in rows[1:]:
        rk = int(r[0])
        if 1 <= rk <= 12:
            rank_class[rk] = r[1]

    # G3b freshness table (fresh-frontier machine assertion)
    with open(freshness_path, "r", encoding="utf-8") as f:
        frows = [line.rstrip("\n").split(",") for line in f if line.strip()]
    if frows[0] != ["rank", "class_index", "unknown_now", "children", "prior_probe", "cache_hit", "fresh"]:
        fail("G3b freshness header drift")
    fby_rank = {int(r[0]): r for r in frows[1:]}
    for rk in range(1, 13):
        if rk not in fby_rank:
            fail("G3b freshness missing rank %d" % rk)
        fr = fby_rank[rk]
        if fr[1] != rank_class.get(rk):
            fail("G3b freshness rank %d class %s != closure-classes %s" % (rk, fr[1], rank_class.get(rk)))
        if rk != 12:
            if int(fr[2]) != int(fr[3]) or int(fr[3]) != int(fr[4]) or int(fr[5]) != 0 or int(fr[6]) != 0:
                fail("G3b rank %d is not all-prior/fresh-0: %r" % (rk, fr))
    fr12 = fby_rank[12]
    if fr12[1] != str(CLASS_INDEX) or int(fr12[2]) != CLASS_UNKNOWN_NOW or int(fr12[3]) != CLASS_UNKNOWN_NOW:
        fail("G3b rank-12 row drift: %r" % (fr12,))
    if int(fr12[4]) != 1 or int(fr12[5]) != 0 or int(fr12[6]) != len(EMBEDDED_TARGETS):
        fail("G3b rank-12 prior/fresh accounting drift: %r" % (fr12,))

    # G4 exact-pair absence in canonical cache (+ same-lo context)
    all_rows = EMBEDDED_TARGETS + [
        {"key_id": q["batch1_key_id"], "lo": q["lo"], "hi": q["hi"]} for q in EMBEDDED_PRIOR
    ]
    wanted_pairs = set((t["lo"], t["hi"]) for t in all_rows)
    same_lo = {t["lo"]: 0 for t in all_rows}
    present = {}
    n_rows = 0
    with open(cache_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("s5verdict,"):
                n_rows += 1
                parts = line.rstrip("\n").split(",")
                lo, hi = int(parts[1]), int(parts[2])
                if (lo, hi) in wanted_pairs:
                    present[(lo, hi)] = line.strip()
                elif lo in same_lo:
                    same_lo[lo] += 1
    if present:
        fail("G4 canonical cache already contains key(s): %r" % sorted(present))

    # G5 quarantine absence (49 targets + the unconsumed b018 pair)
    with open(quarantine_path, "r", encoding="utf-8") as f:
        q = json.load(f)
    active_keys = {tuple(e["key"]) for e in q.get("entries", []) if e.get("active")}
    for t in all_rows:
        if (t["lo"], t["hi"]) in active_keys:
            fail("G5 key %s is quarantined" % t.get("key_id"))

    # G6 worklist class-30345 extract cross-check (probe_order 132..181)
    with open(worklist_path, "r", encoding="utf-8") as f:
        wl = [line.rstrip("\n").split(",") for line in f if line.strip()]
    if wl[0][:2] != ["probe_order", "s5_index"]:
        fail("G6 worklist extract header drift")
    wl_rows = wl[1:]
    if len(wl_rows) != CLASS_UNKNOWN_NOW:
        fail("G6 worklist extract rows = %d, want %d" % (len(wl_rows), CLASS_UNKNOWN_NOW))
    orders = [int(r[0]) for r in wl_rows]
    if orders != list(range(WORKLIST_ORDER_FIRST, WORKLIST_ORDER_LAST + 1)):
        fail("G6 worklist extract probe_order not contiguous %d..%d" % (WORKLIST_ORDER_FIRST, WORKLIST_ORDER_LAST))
    prior_pair = (EMBEDDED_PRIOR[0]["lo"], EMBEDDED_PRIOR[0]["hi"])
    targets_by_pair = {(t["lo"], t["hi"]): t for t in EMBEDDED_TARGETS}
    prior_orders = []
    for r in wl_rows:
        (po, s5, lo, hi, legal, scl, cun, cf, ct, mcc) = r
        if int(scl) != CLASS_INDEX:
            fail("G6 worklist extract serving_class drift: %s" % scl)
        if int(cun) != CLASS_UNKNOWN_NOW:
            fail("G6 worklist extract class_unknown_now drift")
        pair = (int(lo), int(hi))
        if pair in targets_by_pair:
            t = targets_by_pair[pair]
            if int(po) != t["probe_order"]:
                fail("G6 target %s probe_order drift: extract %s embedded %d" % (t["key_id"], po, t["probe_order"]))
            if int(s5) != t["s5_index"] or int(legal) != t["legal"] or int(mcc) != t["membership_class_count"]:
                fail("G6 target %s s5/legal/membership drift" % t["key_id"])
        elif pair == prior_pair:
            pr = EMBEDDED_PRIOR[0]
            if int(po) != pr["probe_order"]:
                fail("G6 prior b018 probe_order drift: %s vs %d" % (po, pr["probe_order"]))
            if int(s5) != pr["s5_index"] or int(legal) != pr["legal"] or int(mcc) != pr["membership_class_count"]:
                fail("G6 prior b018 s5/legal/membership drift")
            prior_orders.append(int(po))
        else:
            fail("G6 worklist row (%s,%s) matches no embedded child" % (lo, hi))
    if len(prior_orders) != 1:
        fail("G6 prior b018 appears %d times in the extract" % len(prior_orders))
    if len(targets_by_pair) != len(EMBEDDED_TARGETS):
        fail("G6 extract does not cover all %d embedded targets" % len(EMBEDDED_TARGETS))
    prev = -1
    for t in EMBEDDED_TARGETS:
        if t["probe_order"] <= prev:
            fail("G6 target probe_order not ascending with ai id at %s" % t["key_id"])
        prev = t["probe_order"]

    # G7 prior-probe universe (freshness of the 49 targets)
    with open(universe_path, "r", encoding="utf-8") as f:
        upairs = []
        for line in f:
            if not line.strip():
                continue
            a, b = line.rstrip("\n").split(",")
            upairs.append((int(a), int(b)))
    if len(upairs) != UNIVERSE_PAIRS:
        fail("G7 universe lines = %d, want %d" % (len(upairs), UNIVERSE_PAIRS))
    if upairs != sorted(set(upairs)):
        fail("G7 universe not sorted-unique ascending")
    uset = set(upairs)
    for t in EMBEDDED_TARGETS:
        if (t["lo"], t["hi"]) in uset:
            fail("G7 target %s was already prior-probed (universe hit)" % t["key_id"])
    if prior_pair not in uset:
        fail("G7 prior b018 pair missing from the prior-probe universe")

    # gates passed -> write outputs atomically
    input_dir = os.path.join(kit_root, "input")
    os.makedirs(input_dir, exist_ok=True)
    for t in EMBEDDED_TARGETS:
        csv = "target,0,5,%d,%d,%d,0,0,0,0,0\n" % (t["lo"], t["hi"], t["legal"])
        tmp = os.path.join(input_dir, t["key_id"] + ".input.csv.tmp")
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            f.write(csv)
        os.replace(tmp, os.path.join(input_dir, t["key_id"] + ".input.csv"))

    keys_doc = {
        "schema": SCHEMA,
        "batch": "batch-38",
        "description": "n11 central-reply closure batch-38: fresh (never-probed) 49 unknown cost-children of closure class 30345 (rank 12, fresh frontier per the post-af034loss1 reaudit), derived from the worklist regen extract; the 50th unknown child is the batch-1 dual-class key b018 (probe-level unconsumed WIN, scrutiny-owner pending) and is NOT a target",
        "target_key_count": len(EMBEDDED_TARGETS),
        "prior_packeted_excluded": [
            {"key_id": "b018", "batch": "batch-1 (class 16757 packet, 2026-11-22)",
             "probe_order": p["probe_order"], "lo": p["lo"], "hi": p["hi"], "legal": p["legal"],
             "s5_index": p["s5_index"], "membership_class_count": p["membership_class_count"],
             "budget_result_nodes": "15000000,1,3549602",
             "note": "probe-level honest WIN never consumed into the canonical chain; unconsumable without the scrutiny-owner C++ gate; same-condition re-probe prohibited; excluded from batch-38 targets"}
        ],
        "keys": [
            {
                "key_id": t["key_id"],
                "probe_order": t["probe_order"],
                "serving_class": CLASS_INDEX,
                "class_mask": CLASS_MASK,
                "class_unknown_now_at_selection": CLASS_UNKNOWN_NOW,
                "lo": t["lo"], "hi": t["hi"], "legal": t["legal"],
                "s5_index": t["s5_index"],
                "membership_class_count": t["membership_class_count"],
                "canonical_cache_same_lo_rows_context": same_lo[t["lo"]],
            }
            for t in EMBEDDED_TARGETS
        ],
        "pins": {
            "batch1_batch_keys": PIN_B1_KEYS,
            "batch1_status": PIN_B1_STATUS,
            "refresh_summary": PIN_REFRESH_SUMMARY,
            "closure_classes": PIN_CLOSURE_CLASSES,
            "canonical_cache": PIN_CANONICAL_CACHE,
            "quarantine": PIN_QUARANTINE,
            "worklist_class30345_extract": PIN_WORKLIST_EXTRACT,
            "prior_probe_universe": PIN_UNIVERSE,
            "freshness_ranks1to12": PIN_FRESHNESS,
            "jsreplay": "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
            "runbatch": "f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84",
        },
        "gates": ["G1-source-sha-pins", "G2-batch1-packet-b018-provenance",
                  "G3-closure-rank-anchor-and-accounting",
                  "G3b-freshness-frontier-ranks1to12",
                  "G4-exact-pair-absent-in-canonical-cache",
                  "G5-not-quarantined",
                  "G6-worklist-extract-field-match",
                  "G7-prior-probe-universe-freshness"],
        "canonical_cache_s5verdict_rows": n_rows,
        "consumed_into_canonical_cache": False,
    }
    tmp = os.path.join(input_dir, "batch-keys-b38.json.tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(keys_doc, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, os.path.join(input_dir, "batch-keys-b38.json"))

    print("make_batch38_keys: ALL GATES PASS, wrote %d inputs + batch-keys-b38.json" % len(EMBEDDED_TARGETS))


if __name__ == "__main__":
    main()
