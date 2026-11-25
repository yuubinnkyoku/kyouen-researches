#!/usr/bin/env python3
"""make_batch39_keys.py - batch-39 (n11 central-reply closure class 30484)
key derivation with fail-closed gates.

Fork of the published batch-38 maker (make_batch38_keys.py, sha256
9b117808...). Declared deltas vs the fork source (everything else
byte-level where the class digits allow, logically identical otherwise):

1. class parameters: closure rank 12 -> 20, class 30345 -> 30484,
   mask [1152922604118478848,65536] -> [1152922604135251968,65536],
   unknown_now 50 -> 52, worklist probe_order 132..181 -> 540..591.
2. prior-child structural slot (batch-1 b018 provenance) replaced by the
   IN-FLIGHT claim-reserved slot: 2 of the 52 universe-fresh children of
   class 30484 are pair-identical to published batch-38 targets
   (ai044 / ai048, dual-class children, kit batch-keys-b38.json sha
   29807104...). Batch-38 is another lane's in-flight, single-owner
   declared probe drive (Part EF); its honest labels are unconsumed and
   the pair verdicts are owned by the EF/adoption path. Same-condition
   re-probe is therefore prohibited for batch-39 exactly as for a prior
   packet key; the two children are claim-reserved and NOT batch-39
   targets. Machine-derived: the reserved pairs are exactly the
   intersection of the class-30484 extract and the batch-38 published
   target set (computed in the declaring session and re-verified by
   G2/G6/G7 at run time).
3. freshness table gates 1..12 -> 13..20: G3b now asserts closure ranks
   13..19 all-prior/fresh-0 (extends the EF scan by the same
   3-way cross-join against the same published pins) and rank 20
   (class 30484) fresh == 52 == 2 (claim-reserved) + 50 (targets).
   The rank 12..19 rows are NOT re-asserted here (they are EF's
   published machine assertion, freshness-ranks1to12.csv e5f51717...,
   and batch-38's in-flight probes do not change the published universe
   CSV 6deee846... which predates them).
4. G2 (packet integrity): batch-1 packet (48 keys + b018 status WIN
   marker) -> batch-38 published batch-keys-b38.json (49 keys
   ai001..ai049, target_key_count 49, consumed_into_canonical_cache
   false); the two reserved rows must match the corresponding batch-38
   key entries field-for-field (lo/hi/legal/s5_index/
   membership_class_count); no status/verdict of batch-38 is consumed or
   asserted here (the batch-38 drive is in flight; its published
   increments are honest labels, unconsumed).
5. G7 (universe freshness): the two reserved pairs are asserted to be
   OUTSIDE the published universe (they are batch-38 fresh targets, not
   prior-packet keys) in addition to the 50 targets being outside.

Scope: the 50 fresh (never-probed, honest-label-free,
canonically-unresolved, quarantine-free, claim-free) unknown
cost-children of closure class 30484 (class_rank 20, mask
[1152922604135251968, 65536]) in the published post-af034loss1-adoption
reaudit (refresh-summary.json 6af660a1..., closure-classes.csv
27e00b0d..., canonical cache fc3e4ac9..., probe-worklist.csv regen pin
b4933810...).

Selection basis (machine re-derived in the declaring session, no
prose): same 3-way cross-join as batch-38 (worklist regen x prior-probe
universe 6deee846... x canonical cache fc3e4ac9...), extended over
closure ranks 13..20. Ranks 13..19 (classes 12264, 5473, 16957, 2634,
8785, 1518, 8106) have ALL of their remaining unknown children inside
the prior-probe universe (fresh 0). Rank 20 class 30484 has 52
universe-fresh children; 2 are claim-reserved (in-flight batch-38
ai044/ai048) and 50 are batch-39 targets aj001..aj050 in worklist
probe_order (540..584, 587..591; probe_orders 585..586 are the
claim-reserved children).

Gates (all fail-closed, rc=1 on any violation, no partial outputs on
failure):
  G1  source sha pins: freshness-ranks13to20 + refresh-summary +
      closure-classes + canonical cache + quarantine + worklist
      class-30484 extract + prior-probe-universe + batch-38
      batch-keys-b38.json must match the pinned sha256 byte-exactly.
  G2  batch-38 packet integrity: 49 keys ai001..ai049,
      target_key_count 49, consumed_into_canonical_cache false; the two
      embedded reserved children match the ai044/ai048 rows
      field-for-field.
  G3  closure-classes.csv rank 20 == class 30484 with unknown_now 52
      and mask match; accounting 52 == 2 (claim-reserved in-flight
      batch-38 dual-class children) + 50 (fresh targets).
  G3b freshness table ranks 13..20: ranks 13..19 all-prior/fresh-0 rows
      (children == unknown_now == prior_probe, cache_hit 0, fresh 0);
      rank 20 row children == 52, prior_probe == 0, cache_hit == 0,
      fresh == 52 == 2 + 50; class indices agree with closure-classes.csv
      rank anchors.
  G4  exact key pairs (lo,hi) of all 52 children (50 targets + 2
      claim-reserved) absent from the canonical merged chain cache
      (pair-level parse of all s5verdict rows; same-lo rows counted
      and reported as context, never adopted).
  G5  none of the 52 pairs appears in the active quarantine registry.
  G6  worklist class-30484 extract: exactly 52 rows, probe_order
      540..591 contiguous ascending, serving_class 30484,
      class_unknown_now 52; every row matches an embedded child (target
      or reserved) on (lo, hi, legal, s5_index, membership_class_count);
      the reserved children sit at probe_order 585..586; target
      probe_orders strictly ascend with aj id order.
  G7  prior-probe universe: 2,104 unique ascending (lo,hi) lines; none
      of the 50 target pairs is in the universe (freshness); the two
      reserved pairs are also outside the universe (batch-38 fresh
      targets, in-flight).

Outputs (written atomically only after all gates pass):
  input/aj001.input.csv ... input/aj050.input.csv (50 files)
      (format: target,0,5,lo,hi,legal,0,0,0,0,0 - identical schema to
       the published batch-31..38 inputs)
  input/batch-keys-b39.json
      schema n11-centralreply-closure-batch39-keys-v1, pins included,
      consumed_into_canonical_cache=false

Determinism: pure function of the pinned inputs; run 3x byte-identical
in the completion protocol. Tamper battery (scratch copies) must ABORT
on: pin drift, batch-38 packet field drift, cache hit, quarantine hit,
closure-table rank drift, freshness-table drift, worklist extract field
drift, universe drift.
"""
import hashlib
import json
import os
import re
import sys

PIN_B38_KEYS = "298071046bfba8473c5b3d6e0b6a30108697eb0899aed7c70fcb4c5343f7cb8d"
PIN_REFRESH_SUMMARY = "6af660a1e0ad8f0ad3b0ac6b32c1a24099aa8f1c3a2271496a9bfb99dc80b6bc"
PIN_CLOSURE_CLASSES = "27e00b0dbf2f33603dfbed91b00153f73c7a2d05b1258133a39c9ec5bfd41364"
PIN_CANONICAL_CACHE = "fc3e4ac9052447158202f09d5efe05468dba32fe95ec90beaaa0a0de9d2c020f"
PIN_QUARANTINE = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
PIN_WORKLIST_EXTRACT = "feda8c7295ec6d17562f786eae9f48c59e7d701fd13748ea655b8bbdb7ea33d0"
PIN_UNIVERSE = "6deee846a4e67778437cd052502535f4839f3fbe76d5e1ec9bc9b6c0036e942b"
PIN_FRESHNESS = "deea05b82a391f5e7d5809c08e2b8c77bc5007cc9ccefab55cee259f65d52b54"

CLASS_INDEX = 30484
CLASS_MASK = [1152922604135251968, 65536]
CLASS_RANK = 20
CLASS_UNKNOWN_NOW = 52
WORKLIST_ORDER_FIRST = 540
WORKLIST_ORDER_LAST = 591
UNIVERSE_PAIRS = 2104

# the 2 claim-reserved dual-class children (batch-38 targets ai044/ai048,
# Part EF in-flight single-owner drive, honest labels unconsumed). NOT
# batch-39 targets; gate-checked for bookkeeping consistency (published
# batch-38 packet row match + cache absence + quarantine absence +
# worklist position + universe absence).
EMBEDDED_RESERVED = [
    {"batch38_key_id": "ai044", "probe_order": 585, "lo": 1152922604135256064, "hi": 65536, "legal": 72, "s5_index": 900354, "membership_class_count": 3},
    {"batch38_key_id": "ai048", "probe_order": 586, "lo": 1152921573327372288, "hi": 68157440, "legal": 68, "s5_index": 900718, "membership_class_count": 3}
]

# the 50 fresh targets, embedded from the pinned worklist extract rows
# (verified against the pinned published file at run time; probe_orders
# 585..586 = the claim-reserved batch-38 children are excluded).
EMBEDDED_TARGETS = [
    {"key_id": "aj001", "probe_order": 540, "lo": 1152922604269469696, "hi": 65536, "legal": 84, "s5_index": 63021, "membership_class_count": 4},
    {"key_id": "aj002", "probe_order": 541, "lo": 10376294640990027776, "hi": 65536, "legal": 90, "s5_index": 82345, "membership_class_count": 4},
    {"key_id": "aj003", "probe_order": 542, "lo": 3458765613348945920, "hi": 65536, "legal": 81, "s5_index": 195180, "membership_class_count": 4},
    {"key_id": "aj004", "probe_order": 543, "lo": 1152922879013158912, "hi": 65536, "legal": 84, "s5_index": 281792, "membership_class_count": 4},
    {"key_id": "aj005", "probe_order": 544, "lo": 5764608622562639872, "hi": 65536, "legal": 86, "s5_index": 298723, "membership_class_count": 4},
    {"key_id": "aj006", "probe_order": 545, "lo": 1152922604135317504, "hi": 65536, "legal": 88, "s5_index": 375902, "membership_class_count": 4},
    {"key_id": "aj007", "probe_order": 546, "lo": 1152922604135251968, "hi": 65537, "legal": 91, "s5_index": 391885, "membership_class_count": 4},
    {"key_id": "aj008", "probe_order": 547, "lo": 1152922604135251968, "hi": 65538, "legal": 92, "s5_index": 474119, "membership_class_count": 4},
    {"key_id": "aj009", "probe_order": 548, "lo": 1152922741574205440, "hi": 65536, "legal": 81, "s5_index": 634046, "membership_class_count": 4},
    {"key_id": "aj010", "probe_order": 549, "lo": 1152923153891065856, "hi": 65536, "legal": 83, "s5_index": 644052, "membership_class_count": 4},
    {"key_id": "aj011", "probe_order": 550, "lo": 1155174403948937216, "hi": 65536, "legal": 84, "s5_index": 655118, "membership_class_count": 4},
    {"key_id": "aj012", "probe_order": 551, "lo": 1152922604135251968, "hi": 66048, "legal": 89, "s5_index": 657320, "membership_class_count": 4},
    {"key_id": "aj013", "probe_order": 552, "lo": 1152922604202360832, "hi": 65536, "legal": 91, "s5_index": 739110, "membership_class_count": 4},
    {"key_id": "aj014", "probe_order": 553, "lo": 1152922604403687424, "hi": 65536, "legal": 79, "s5_index": 744807, "membership_class_count": 4},
    {"key_id": "aj015", "probe_order": 554, "lo": 1157426203762622464, "hi": 65536, "legal": 79, "s5_index": 753448, "membership_class_count": 4},
    {"key_id": "aj016", "probe_order": 555, "lo": 1152922604135251968, "hi": 66560, "legal": 91, "s5_index": 754653, "membership_class_count": 4},
    {"key_id": "aj017", "probe_order": 556, "lo": 1152922604135284736, "hi": 65536, "legal": 96, "s5_index": 815958, "membership_class_count": 4},
    {"key_id": "aj018", "probe_order": 557, "lo": 1152922604135383040, "hi": 65536, "legal": 87, "s5_index": 819898, "membership_class_count": 4},
    {"key_id": "aj019", "probe_order": 558, "lo": 1161929803389992960, "hi": 65536, "legal": 86, "s5_index": 826659, "membership_class_count": 4},
    {"key_id": "aj020", "probe_order": 559, "lo": 1152922604135251968, "hi": 67584, "legal": 92, "s5_index": 827583, "membership_class_count": 4},
    {"key_id": "aj021", "probe_order": 560, "lo": 1152922604135252032, "hi": 65536, "legal": 95, "s5_index": 873785, "membership_class_count": 4},
    {"key_id": "aj022", "probe_order": 561, "lo": 1170937002644733952, "hi": 65536, "legal": 96, "s5_index": 878828, "membership_class_count": 4},
    {"key_id": "aj023", "probe_order": 562, "lo": 1152922604135251968, "hi": 69632, "legal": 82, "s5_index": 879486, "membership_class_count": 4},
    {"key_id": "aj024", "probe_order": 563, "lo": 1152922604135252480, "hi": 65536, "legal": 97, "s5_index": 888597, "membership_class_count": 4},
    {"key_id": "aj025", "probe_order": 564, "lo": 1152922604137349120, "hi": 65536, "legal": 93, "s5_index": 888632, "membership_class_count": 4},
    {"key_id": "aj026", "probe_order": 565, "lo": 1152922604135252224, "hi": 65536, "legal": 95, "s5_index": 890205, "membership_class_count": 4},
    {"key_id": "aj027", "probe_order": 566, "lo": 1152922608430219264, "hi": 65536, "legal": 91, "s5_index": 890217, "membership_class_count": 4},
    {"key_id": "aj028", "probe_order": 567, "lo": 1152922604135252096, "hi": 65536, "legal": 91, "s5_index": 891252, "membership_class_count": 4},
    {"key_id": "aj029", "probe_order": 568, "lo": 1152931400228274176, "hi": 65536, "legal": 94, "s5_index": 891691, "membership_class_count": 4},
    {"key_id": "aj030", "probe_order": 569, "lo": 1152922604135251976, "hi": 65536, "legal": 83, "s5_index": 892576, "membership_class_count": 4},
    {"key_id": "aj031", "probe_order": 570, "lo": 1152921574400065536, "hi": 1056768, "legal": 85, "s5_index": 893069, "membership_class_count": 4},
    {"key_id": "aj032", "probe_order": 571, "lo": 1152922604135251972, "hi": 65536, "legal": 95, "s5_index": 893865, "membership_class_count": 4},
    {"key_id": "aj033", "probe_order": 572, "lo": 1152921574400065536, "hi": 17825792, "legal": 97, "s5_index": 894452, "membership_class_count": 4},
    {"key_id": "aj034", "probe_order": 573, "lo": 1152922604135251970, "hi": 65536, "legal": 96, "s5_index": 895046, "membership_class_count": 4},
    {"key_id": "aj035", "probe_order": 574, "lo": 1152921573326324224, "hi": 68157440, "legal": 97, "s5_index": 895603, "membership_class_count": 4},
    {"key_id": "aj036", "probe_order": 575, "lo": 1152922604135251969, "hi": 65536, "legal": 84, "s5_index": 896123, "membership_class_count": 3},
    {"key_id": "aj037", "probe_order": 576, "lo": 1152921573326324736, "hi": 68157440, "legal": 82, "s5_index": 896603, "membership_class_count": 3},
    {"key_id": "aj038", "probe_order": 577, "lo": 1152922604135776256, "hi": 65536, "legal": 96, "s5_index": 897649, "membership_class_count": 4},
    {"key_id": "aj039", "probe_order": 578, "lo": 1152922606282735616, "hi": 65536, "legal": 88, "s5_index": 897668, "membership_class_count": 4},
    {"key_id": "aj040", "probe_order": 579, "lo": 1152922604135514112, "hi": 65536, "legal": 89, "s5_index": 898280, "membership_class_count": 4},
    {"key_id": "aj041", "probe_order": 580, "lo": 1152927002181763072, "hi": 65536, "legal": 94, "s5_index": 898533, "membership_class_count": 4},
    {"key_id": "aj042", "probe_order": 581, "lo": 1152922604135268352, "hi": 65536, "legal": 83, "s5_index": 899043, "membership_class_count": 4},
    {"key_id": "aj043", "probe_order": 582, "lo": 1152921574400065536, "hi": 1064960, "legal": 89, "s5_index": 899372, "membership_class_count": 4},
    {"key_id": "aj044", "probe_order": 583, "lo": 1152922604135260160, "hi": 65536, "legal": 91, "s5_index": 899741, "membership_class_count": 4},
    {"key_id": "aj045", "probe_order": 584, "lo": 1152921574400065536, "hi": 34603008, "legal": 96, "s5_index": 900167, "membership_class_count": 4},
    {"key_id": "aj046", "probe_order": 587, "lo": 1152922672854728704, "hi": 65536, "legal": 88, "s5_index": 901454, "membership_class_count": 3},
    {"key_id": "aj047", "probe_order": 588, "lo": 1152924803158507520, "hi": 65536, "legal": 91, "s5_index": 901621, "membership_class_count": 4},
    {"key_id": "aj048", "probe_order": 589, "lo": 1152921574400065536, "hi": 1081344, "legal": 86, "s5_index": 902090, "membership_class_count": 4},
    {"key_id": "aj049", "probe_order": 590, "lo": 1152921574400065536, "hi": 1114112, "legal": 80, "s5_index": 902511, "membership_class_count": 3},
    {"key_id": "aj050", "probe_order": 591, "lo": 1152921574400065536, "hi": 68157440, "legal": 80, "s5_index": 902512, "membership_class_count": 2}
]

SCHEMA = "n11-centralreply-closure-batch39-keys-v1"


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
    cache_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(src, "canonical-cache-fc3e4ac9.cache")
    quarantine_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(src, "quarantine.json")
    refresh_path = sys.argv[3] if len(sys.argv) > 3 else os.path.join(src, "refresh-summary.json")
    closure_path = sys.argv[4] if len(sys.argv) > 4 else os.path.join(src, "closure-classes.csv")
    worklist_path = sys.argv[5] if len(sys.argv) > 5 else os.path.join(src, "worklist-class30484-extract.csv")
    universe_path = sys.argv[6] if len(sys.argv) > 6 else os.path.join(src, "prior-probe-universe.csv")
    freshness_path = sys.argv[7] if len(sys.argv) > 7 else os.path.join(src, "freshness-ranks13to20.csv")
    b38_keys_path = sys.argv[8] if len(sys.argv) > 8 else os.path.join(src, "batch-keys-b38.json")

    # G1 source pins
    for path, pin, what in [
        (b38_keys_path, PIN_B38_KEYS, "batch-38 batch-keys"),
        (refresh_path, PIN_REFRESH_SUMMARY, "refresh-summary"),
        (closure_path, PIN_CLOSURE_CLASSES, "closure-classes"),
        (cache_path, PIN_CANONICAL_CACHE, "canonical cache"),
        (quarantine_path, PIN_QUARANTINE, "quarantine"),
        (worklist_path, PIN_WORKLIST_EXTRACT, "worklist class-30484 extract"),
        (universe_path, PIN_UNIVERSE, "prior-probe universe"),
        (freshness_path, PIN_FRESHNESS, "freshness table ranks 13..20"),
    ]:
        if sha256_file(path) != pin:
            fail("G1 pin mismatch on %s (%s)" % (what, path))

    # G2 batch-38 packet integrity (the claim-reserved dual-class provenance)
    with open(b38_keys_path, "r", encoding="utf-8") as f:
        packet = json.load(f)
    keys = packet.get("keys", [])
    if len(keys) != 49 or packet.get("target_key_count") != 49:
        fail("G2 batch-38 packet has %d keys / target_key_count %r, want 49"
             % (len(keys), packet.get("target_key_count")))
    ids = [k.get("key_id") for k in keys]
    if ids != ["ai%03d" % i for i in range(1, 50)]:
        fail("G2 batch-38 packet id set drift")
    if packet.get("consumed_into_canonical_cache") is not False:
        fail("G2 batch-38 packet consumed flag drift")
    pkt = {k["key_id"]: k for k in keys}
    for q in EMBEDDED_RESERVED:
        row = pkt.get(q["batch38_key_id"])
        if row is None:
            fail("G2 batch-38 packet missing %s" % q["batch38_key_id"])
        for field in ("lo", "hi", "legal", "s5_index", "membership_class_count"):
            if row.get(field) != q[field]:
                fail("G2 %s field %s drift: packet %r embedded %r"
                     % (q["batch38_key_id"], field, row.get(field), q[field]))

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
    if CLASS_UNKNOWN_NOW != len(EMBEDDED_RESERVED) + len(EMBEDDED_TARGETS):
        fail("G3 accounting: %d != %d (claim-reserved) + %d (fresh)"
             % (CLASS_UNKNOWN_NOW, len(EMBEDDED_RESERVED), len(EMBEDDED_TARGETS)))
    rank_class = {}
    for r in rows[1:]:
        rk = int(r[0])
        if 13 <= rk <= 20:
            rank_class[rk] = r[1]

    # G3b freshness table ranks 13..20 (fresh-frontier machine assertion)
    with open(freshness_path, "r", encoding="utf-8") as f:
        frows = [line.rstrip("\n").split(",") for line in f if line.strip()]
    if frows[0] != ["rank", "class_index", "unknown_now", "children", "prior_probe", "cache_hit", "fresh"]:
        fail("G3b freshness header drift")
    fby_rank = {int(r[0]): r for r in frows[1:]}
    for rk in range(13, 21):
        if rk not in fby_rank:
            fail("G3b freshness missing rank %d" % rk)
        fr = fby_rank[rk]
        if fr[1] != rank_class.get(rk):
            fail("G3b freshness rank %d class %s != closure-classes %s" % (rk, fr[1], rank_class.get(rk)))
        if rk != 20:
            if int(fr[2]) != int(fr[3]) or int(fr[3]) != int(fr[4]) or int(fr[5]) != 0 or int(fr[6]) != 0:
                fail("G3b rank %d is not all-prior/fresh-0: %r" % (rk, fr))
    fr20 = fby_rank[20]
    if fr20[1] != str(CLASS_INDEX) or int(fr20[2]) != CLASS_UNKNOWN_NOW or int(fr20[3]) != CLASS_UNKNOWN_NOW:
        fail("G3b rank-20 row drift: %r" % (fr20,))
    if int(fr20[4]) != 0 or int(fr20[5]) != 0 or int(fr20[6]) != len(EMBEDDED_RESERVED) + len(EMBEDDED_TARGETS):
        fail("G3b rank-20 prior/fresh accounting drift: %r" % (fr20,))

    # G4 exact-pair absence in canonical cache (+ same-lo context)
    all_rows = EMBEDDED_TARGETS + [
        {"key_id": q["batch38_key_id"], "lo": q["lo"], "hi": q["hi"]} for q in EMBEDDED_RESERVED
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

    # G5 quarantine absence (50 targets + the 2 claim-reserved pairs)
    with open(quarantine_path, "r", encoding="utf-8") as f:
        q = json.load(f)
    active_keys = {tuple(e["key"]) for e in q.get("entries", []) if e.get("active")}
    for t in all_rows:
        if (t["lo"], t["hi"]) in active_keys:
            fail("G5 key %s is quarantined" % t.get("key_id"))

    # G6 worklist class-30484 extract cross-check (probe_order 540..591)
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
    reserved_pairs = {(q["lo"], q["hi"]) for q in EMBEDDED_RESERVED}
    targets_by_pair = {(t["lo"], t["hi"]): t for t in EMBEDDED_TARGETS}
    reserved_orders = []
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
        elif pair in reserved_pairs:
            pr = None
            for cnd in EMBEDDED_RESERVED:
                if (cnd["lo"], cnd["hi"]) == pair:
                    pr = cnd
            if int(po) != pr["probe_order"]:
                fail("G6 reserved %s probe_order drift: %s vs %d" % (pr["batch38_key_id"], po, pr["probe_order"]))
            if int(s5) != pr["s5_index"] or int(legal) != pr["legal"] or int(mcc) != pr["membership_class_count"]:
                fail("G6 reserved %s s5/legal/membership drift" % pr["batch38_key_id"])
            reserved_orders.append(int(po))
        else:
            fail("G6 worklist row (%s,%s) matches no embedded child" % (lo, hi))
    if reserved_orders != sorted(q["probe_order"] for q in EMBEDDED_RESERVED):
        fail("G6 reserved orders %r want %r" % (reserved_orders, sorted(q["probe_order"] for q in EMBEDDED_RESERVED)))
    if len(targets_by_pair) != len(EMBEDDED_TARGETS):
        fail("G6 extract does not cover all %d embedded targets" % len(EMBEDDED_TARGETS))
    prev = -1
    for t in EMBEDDED_TARGETS:
        if t["probe_order"] <= prev:
            fail("G6 target probe_order not ascending with aj id at %s" % t["key_id"])
        prev = t["probe_order"]

    # G7 prior-probe universe (freshness of the 50 targets + 2 reserved)
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
    for q in EMBEDDED_RESERVED:
        if (q["lo"], q["hi"]) in uset:
            fail("G7 reserved %s is inside the prior-probe universe" % q["batch38_key_id"])

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
        "batch": "batch-39",
        "description": "n11 central-reply closure batch-39: fresh (never-probed) 50 unknown cost-children of closure class 30484 (rank 20, fresh frontier per the post-af034loss1 reaudit and the ranks-13..20 freshness scan), derived from the worklist regen extract; 2 of the 52 universe-fresh children are claim-reserved in-flight batch-38 targets (ai044/ai048, dual-class, Part EF single-owner, verdict path owned by EF/adoption) and are NOT targets",
        "target_key_count": len(EMBEDDED_TARGETS),
        "claim_reserved_excluded": [
            {"key_id": q["batch38_key_id"], "batch": "batch-38 (closure class 30345 packet, Part EF in-flight, published batch-keys-b38.json)",
             "probe_order": q["probe_order"], "lo": q["lo"], "hi": q["hi"], "legal": q["legal"],
             "s5_index": q["s5_index"], "membership_class_count": q["membership_class_count"],
             "note": "dual-class child (30345/30484); in-flight claimed by the Part EF single-owner drive; same-condition re-probe prohibited; excluded from batch-39 targets"}
            for q in EMBEDDED_RESERVED
        ],
        "keys": [
            {
                "key_id": t["key_id"],
                "probe_order": t["probe_order"],
                "serving_class": CLASS_INDEX,
                "class_mask": CLASS_MASK,
                "class_unknown_now_at_selection": CLASS_UNKNOWN_NOW,
                "lo": t["lo"], "hi": t["hi"], "legal": t["legal"],
                "s5_index": t["s5_index"], "membership_class_count": t["membership_class_count"],
                "canonical_cache_same_lo_rows_context": same_lo[t["lo"]],
            }
            for t in EMBEDDED_TARGETS
        ],
        "pins": {
            "batch38_batch_keys": PIN_B38_KEYS,
            "refresh_summary": PIN_REFRESH_SUMMARY,
            "closure_classes": PIN_CLOSURE_CLASSES,
            "canonical_cache": PIN_CANONICAL_CACHE,
            "quarantine": PIN_QUARANTINE,
            "worklist_class30484_extract": PIN_WORKLIST_EXTRACT,
            "prior_probe_universe": PIN_UNIVERSE,
            "freshness_ranks13to20": PIN_FRESHNESS,
            "jsreplay": "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
            "runbatch": "f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84",
        },
        "gates": ["G1-source-sha-pins", "G2-batch38-packet-claim-reserved-provenance",
                  "G3-closure-rank-anchor-and-accounting",
                  "G3b-freshness-frontier-ranks13to20",
                  "G4-exact-pair-absent-in-canonical-cache",
                  "G5-not-quarantined",
                  "G6-worklist-extract-field-match",
                  "G7-prior-probe-universe-freshness"],
        "canonical_cache_s5verdict_rows": n_rows,
        "consumed_into_canonical_cache": False,
    }
    tmp = os.path.join(input_dir, "batch-keys-b39.json.tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(keys_doc, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, os.path.join(input_dir, "batch-keys-b39.json"))

    print("make_batch39_keys: ALL GATES PASS, wrote %d inputs + batch-keys-b39.json" % len(EMBEDDED_TARGETS))


if __name__ == "__main__":
    main()
