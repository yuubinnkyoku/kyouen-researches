#!/usr/bin/env python3
"""make_batch40_keys.py - batch-40 (n11 central-reply closure class 30118)
key derivation with fail-closed gates.

Fork of the published batch-39 maker (make_batch39_keys.py, sha256
425329c0...). Declared deltas vs the fork source (everything else
byte-level where the class digits allow, logically identical otherwise):

1. class parameters: closure rank 20 -> 21, class 30484 -> 30118, mask
   [1152922604135251968,65536] -> [1152922604118474753,65536],
   unknown_now 52 (unchanged count), worklist probe_order 540..591 ->
   546..597.
2. claim-reserved slot re-pointed: the 2 universe-fresh children of
   class 30118 that are pair-identical to published batch-38 targets are
   ai033/ai034 (dual-class 30345/30118 children, kit batch-keys-b38.json
   sha 29807104..., Part EF in-flight single-owner drive). Same-condition
   re-probe is therefore prohibited for batch-40 exactly as for a prior
   packet key; the two children are claim-reserved and NOT batch-40
   targets. Machine-derived: the reserved pairs are exactly the
   intersection of the class-30118 extract and the batch-38 published
   target set (re-verified by G2/G6/G7 at run time).
3. prior-probe universe honesty extension: batch-39 probed and published
   50 keys (aj001..aj050, batch-keys-b39.json sha 5e25b550...). The
   published universe (6deee846..., 2,104 pairs) predates them. The new
   source prior-probe-universe-b40.csv (09332448..., 2,154 pairs) =
   base UNION exactly those 50 probed keys; provenance machine-written
   to prior-probe-universe-b40.ext-meta.json (61a71240...). G9 verifies
   the union bit-exactly against the published batch-39 packet.
   G7 freshness now gates against BOTH universes.
4. freshness table ranks 13..20 -> ranks 1..21 with a new claimed column
   (the 49 in-flight batch-38 target pairs): G3b asserts every rank
   1..20 row has fresh == 0 (rank 9 class 30484: 4 prior [batch-39
   honest labels aj030/aj039/aj049/aj050] + 2 claimed [ai044/ai048];
   rank 13 class 30345: 1 prior + 49 claimed) and the rank-21 target row
   accounts 52 == 2 (claim-reserved) + 50 (fresh targets), with
   children == prior + cache_hit + claimed + fresh per row and class
   indices agreeing with closure-classes.csv rank anchors.
5. G4 additionally asserts the canonical cache carries exactly 6,712
   s5verdict rows (the Part EI canonical chain 73482be0...).

Scope: the 50 fresh (never-probed, honest-label-free,
canonically-unresolved, quarantine-free, claim-free) unknown
cost-children of closure class 30118 (class_rank 21, mask
[1152922604118474753, 65536]) in the published post-b39loss46-adoption
reaudit (refresh-summary.json 414314eb..., closure-classes.csv
e12bf328..., canonical cache 73482be0..., probe-worklist.csv regen pin
98529a8d..., worklist-class30118-extract.csv 8ed13b8b...).

Selection basis (machine re-derived in the declaring session, no
prose): same 3-way cross-join as batch-38/39 (worklist regen x
prior-probe universe x canonical cache) extended over closure ranks
1..21 with the extended universe and the claimed column. The post-EI
fresh frontier is class 30118 at rank 21 (pre-EI it sat at rank 39,
outside the batch-39 ranks-13..20 scan; its own 2 adopted dual-class
rows moved it to rank 21 in the EI reaudit). Context rows, not
selected, machine-derived: rank 23 class 23964 fresh 51, rank 25 class
8811 fresh 51.

Gates (all fail-closed, rc=1 on any violation, no partial outputs on
failure):
  G1  source sha pins: batch-keys-b38 + batch-keys-b39 + freshness
      table ranks1to21-b40 + refresh-summary + closure-classes +
      canonical cache + quarantine + worklist class-30118 extract +
      prior-probe universe (base) + prior-probe universe (b40 ext) +
      ext meta must match the pinned sha256 byte-exactly.
  G2  batch-38 packet integrity: 49 keys ai001..ai049,
      target_key_count 49, consumed_into_canonical_cache false; the two
      embedded reserved children match the ai033/ai034 rows
      field-for-field (lo/hi/legal/s5_index/membership_class_count);
      no status/verdict of batch-38 is consumed or asserted here.
  G3  closure-classes.csv rank 21 == class 30118 with unknown_now 52
      and mask match; accounting 52 == 2 (claim-reserved) + 50
      (fresh targets).
  G3b freshness table ranks 1..21 (fresh-frontier machine assertion):
      children == unknown_now per row, children == prior + cache_hit +
      claimed + fresh, fresh == 0 for every rank 1..20; rank 21 row =
      class 30118 with claimed == 2 and fresh == 50; class indices
      agree with closure-classes.csv rank anchors.
  G4  exact key pairs (lo,hi) of all 52 children (50 targets + 2
      claim-reserved) absent from the canonical merged chain cache
      (pair-level parse of all s5verdict rows; the cache must carry
      exactly 6,712 rows; same-lo rows counted and reported as context,
      never adopted).
  G5  none of the 52 pairs appears in the active quarantine registry.
  G6  worklist class-30118 extract: exactly 52 rows, probe_order
      546..597 contiguous ascending, serving_class 30118,
      class_unknown_now 52; every row matches an embedded child (target
      or reserved) on (lo, hi, legal, s5_index, membership_class_count);
      the reserved children sit at probe_order 586/596; target
      probe_orders strictly ascend with ak id order.
  G7  prior-probe universe (base / extended): 2,104 / 2,154
      sorted-unique ascending lines, extended a superset of base; none
      of the 50 target pairs and neither reserved pair appears in
      EITHER universe.
  G9  extended-universe integrity: ext == base UNION exactly the 50
      probed batch-39 keys (from the published batch-keys-b39.json) ==
      the ext-meta added set.

Outputs (written atomically only after all gates pass):
  input/ak001.input.csv ... input/ak050.input.csv (50 files)
      (format: target,0,5,lo,hi,legal,0,0,0,0,0 - identical schema to
       the published batch-31..39 inputs)
  input/batch-keys-b40.json
      schema n11-centralreply-closure-batch40-keys-v1, pins included,
      consumed_into_canonical_cache=false

Determinism: pure function of the pinned inputs; run 3x byte-identical
in the completion protocol. Tamper battery (scratch copies) must ABORT
on: pin drift, batch-38 packet field drift, cache hit, cache row-count
drift, quarantine hit, closure-table rank drift, freshness-table drift,
worklist extract field drift, universe drift (base or ext),
ext-integrity drift.
"""
import hashlib
import json
import os
import re
import sys

PIN_B38_KEYS = "298071046bfba8473c5b3d6e0b6a30108697eb0899aed7c70fcb4c5343f7cb8d"
PIN_B39_KEYS = "5e25b550ef42c1f56dc9d4b69d61d33304664ad839ed7f8d19f45fe50f5e63a9"
PIN_REFRESH_SUMMARY = "414314eb38776f7fee69b3f6d1b894ab24b8e4fac4ea578bc109fce82863329f"
PIN_CLOSURE_CLASSES = "e12bf3280c77e31fc91e30e6806d2828b141af565bfa5e565a2aa3410d974673"
PIN_CANONICAL_CACHE = "73482be0cf0201b2d812f9205b0315e91527234e02196691279753853feddc70"
PIN_QUARANTINE = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
PIN_WORKLIST_EXTRACT = "8ed13b8bc2a06fb4e17c9540902add3d6018ada7e70a962eabb34fea49280193"
PIN_UNIVERSE = "6deee846a4e67778437cd052502535f4839f3fbe76d5e1ec9bc9b6c0036e942b"
PIN_UNIVERSE_EXT = "093324488d73f029203cfabdc262b9640c32046a54689a6abc6e80759d2cea98"
PIN_EXT_META = "61a71240a8cdf7d16d7a8be84279bdfc30a6f74a787f1fb059334157b156a725"
PIN_FRESHNESS = "b80f581b98975de29b79721f8781b2f5409045740e7b5edd384a3b74af8ba2fb"

CLASS_INDEX = 30118
CLASS_MASK = [1152922604118474753, 65536]
CLASS_RANK = 21
CLASS_UNKNOWN_NOW = 52
WORKLIST_ORDER_FIRST = 546
WORKLIST_ORDER_LAST = 597
UNIVERSE_PAIRS = 2104
UNIVERSE_EXT_PAIRS = 2154
CANONICAL_CACHE_ROWS = 6712



# the 2 claim-reserved dual-class children (batch-38 targets ai033/ai034,
# Part EF in-flight single-owner drive, honest labels unconsumed). NOT
# batch-40 targets; gate-checked for bookkeeping consistency (published
# batch-38 packet row match + cache absence + quarantine absence +
# worklist position + universe absence).
EMBEDDED_RESERVED = [
    {"batch38_key_id": "ai033", "probe_order": 586, "lo": 1152922604118478849, "hi": 65536, "legal": 80, "s5_index": 895907, "membership_class_count": 3},
    {"batch38_key_id": "ai034", "probe_order": 596, "lo": 1152921573326324736, "hi": 68720525312, "legal": 74, "s5_index": 896605, "membership_class_count": 3}
]

# the 50 fresh targets, embedded from the pinned worklist extract rows
# (verified against the pinned published file at run time; probe_orders
# 585..586 = the claim-reserved batch-38 children are excluded).
# the 50 fresh targets, embedded from the pinned worklist extract rows
# (verified against the pinned published file at run time; probe_orders
# 586/596 = the claim-reserved batch-38 children are excluded).
EMBEDDED_TARGETS = [
    {"key_id": "ak001", "probe_order": 546, "lo": 10376294640973250561, "hi": 65536, "legal": 93, "s5_index": 81988, "membership_class_count": 4},
    {"key_id": "ak002", "probe_order": 547, "lo": 1153485554071896065, "hi": 65536, "legal": 87, "s5_index": 118409, "membership_class_count": 4},
    {"key_id": "ak003", "probe_order": 548, "lo": 3458765613332168705, "hi": 65536, "legal": 92, "s5_index": 194821, "membership_class_count": 4},
    {"key_id": "ak004", "probe_order": 549, "lo": 1152922878996381697, "hi": 65536, "legal": 91, "s5_index": 227043, "membership_class_count": 4},
    {"key_id": "ak005", "probe_order": 550, "lo": 5764608622545862657, "hi": 65536, "legal": 92, "s5_index": 298378, "membership_class_count": 4},
    {"key_id": "ak006", "probe_order": 551, "lo": 1152922604118540289, "hi": 65536, "legal": 93, "s5_index": 326923, "membership_class_count": 4},
    {"key_id": "ak007", "probe_order": 552, "lo": 1152922604118474753, "hi": 65537, "legal": 96, "s5_index": 391514, "membership_class_count": 4},
    {"key_id": "ak008", "probe_order": 553, "lo": 1152922604118474785, "hi": 65536, "legal": 91, "s5_index": 417028, "membership_class_count": 4},
    {"key_id": "ak009", "probe_order": 554, "lo": 1152922604118474753, "hi": 65538, "legal": 94, "s5_index": 473783, "membership_class_count": 4},
    {"key_id": "ak010", "probe_order": 555, "lo": 1152922741557428225, "hi": 65536, "legal": 90, "s5_index": 565239, "membership_class_count": 4},
    {"key_id": "ak011", "probe_order": 556, "lo": 1152923153874288641, "hi": 65536, "legal": 82, "s5_index": 598584, "membership_class_count": 4},
    {"key_id": "ak012", "probe_order": 557, "lo": 1155174403932160001, "hi": 65536, "legal": 90, "s5_index": 654829, "membership_class_count": 4},
    {"key_id": "ak013", "probe_order": 558, "lo": 1152922604118474753, "hi": 66048, "legal": 90, "s5_index": 657136, "membership_class_count": 4},
    {"key_id": "ak014", "probe_order": 559, "lo": 1152922604185583617, "hi": 65536, "legal": 97, "s5_index": 683483, "membership_class_count": 4},
    {"key_id": "ak015", "probe_order": 560, "lo": 1152922604386910209, "hi": 65536, "legal": 84, "s5_index": 711038, "membership_class_count": 4},
    {"key_id": "ak016", "probe_order": 561, "lo": 1157426203745845249, "hi": 65536, "legal": 87, "s5_index": 753170, "membership_class_count": 4},
    {"key_id": "ak017", "probe_order": 562, "lo": 1152922604118474753, "hi": 66560, "legal": 100, "s5_index": 754462, "membership_class_count": 4},
    {"key_id": "ak018", "probe_order": 563, "lo": 1152922604118507521, "hi": 65536, "legal": 100, "s5_index": 773515, "membership_class_count": 4},
    {"key_id": "ak019", "probe_order": 564, "lo": 1152922604118605825, "hi": 65536, "legal": 92, "s5_index": 795949, "membership_class_count": 4},
    {"key_id": "ak020", "probe_order": 565, "lo": 1161929803373215745, "hi": 65536, "legal": 90, "s5_index": 826438, "membership_class_count": 4},
    {"key_id": "ak021", "probe_order": 566, "lo": 1152922604118474753, "hi": 67584, "legal": 99, "s5_index": 827401, "membership_class_count": 4},
    {"key_id": "ak022", "probe_order": 567, "lo": 1152922604118474769, "hi": 65536, "legal": 85, "s5_index": 840491, "membership_class_count": 4},
    {"key_id": "ak023", "probe_order": 568, "lo": 1152922604118474817, "hi": 65536, "legal": 98, "s5_index": 855551, "membership_class_count": 4},
    {"key_id": "ak024", "probe_order": 569, "lo": 1170937002627956737, "hi": 65536, "legal": 98, "s5_index": 878660, "membership_class_count": 4},
    {"key_id": "ak025", "probe_order": 570, "lo": 1152922604118474753, "hi": 69632, "legal": 87, "s5_index": 879328, "membership_class_count": 4},
    {"key_id": "ak026", "probe_order": 571, "lo": 1152922672837951489, "hi": 65536, "legal": 92, "s5_index": 887249, "membership_class_count": 3},
    {"key_id": "ak027", "probe_order": 572, "lo": 1152922604118475265, "hi": 65536, "legal": 96, "s5_index": 887601, "membership_class_count": 4},
    {"key_id": "ak028", "probe_order": 573, "lo": 1152922604120571905, "hi": 65536, "legal": 100, "s5_index": 887902, "membership_class_count": 4},
    {"key_id": "ak029", "probe_order": 574, "lo": 1152922604118475009, "hi": 65536, "legal": 95, "s5_index": 889244, "membership_class_count": 4},
    {"key_id": "ak030", "probe_order": 575, "lo": 1152922608413442049, "hi": 65536, "legal": 99, "s5_index": 889805, "membership_class_count": 4},
    {"key_id": "ak031", "probe_order": 576, "lo": 1152931400211496961, "hi": 65536, "legal": 96, "s5_index": 891480, "membership_class_count": 4},
    {"key_id": "ak032", "probe_order": 577, "lo": 1152921573326324736, "hi": 1056768, "legal": 89, "s5_index": 892933, "membership_class_count": 4},
    {"key_id": "ak033", "probe_order": 578, "lo": 1152922604118474757, "hi": 65536, "legal": 99, "s5_index": 893349, "membership_class_count": 4},
    {"key_id": "ak034", "probe_order": 579, "lo": 1152921573326324736, "hi": 17825792, "legal": 101, "s5_index": 894448, "membership_class_count": 4},
    {"key_id": "ak035", "probe_order": 580, "lo": 1152922604118474755, "hi": 65536, "legal": 96, "s5_index": 894552, "membership_class_count": 4},
    {"key_id": "ak036", "probe_order": 581, "lo": 1152921573326324736, "hi": 34360786944, "legal": 101, "s5_index": 895602, "membership_class_count": 4},
    {"key_id": "ak037", "probe_order": 582, "lo": 1152922604118999041, "hi": 65536, "legal": 100, "s5_index": 895731, "membership_class_count": 4},
    {"key_id": "ak038", "probe_order": 583, "lo": 1152922604118736897, "hi": 65536, "legal": 97, "s5_index": 895794, "membership_class_count": 4},
    {"key_id": "ak039", "probe_order": 584, "lo": 1152922604118491137, "hi": 65536, "legal": 90, "s5_index": 895825, "membership_class_count": 4},
    {"key_id": "ak040", "probe_order": 585, "lo": 1152922604118482945, "hi": 65536, "legal": 99, "s5_index": 895876, "membership_class_count": 4},
    {"key_id": "ak041", "probe_order": 587, "lo": 1152922606265958401, "hi": 65536, "legal": 100, "s5_index": 895992, "membership_class_count": 4},
    {"key_id": "ak042", "probe_order": 588, "lo": 1152922604655345665, "hi": 65536, "legal": 94, "s5_index": 896044, "membership_class_count": 4},
    {"key_id": "ak043", "probe_order": 589, "lo": 1152922604152029185, "hi": 65536, "legal": 90, "s5_index": 896091, "membership_class_count": 4},
    {"key_id": "ak044", "probe_order": 590, "lo": 1152927002164985857, "hi": 65536, "legal": 95, "s5_index": 896208, "membership_class_count": 4},
    {"key_id": "ak045", "probe_order": 591, "lo": 1152924803141730305, "hi": 65536, "legal": 95, "s5_index": 896248, "membership_class_count": 4},
    {"key_id": "ak046", "probe_order": 592, "lo": 1152921573326324736, "hi": 1064960, "legal": 94, "s5_index": 896368, "membership_class_count": 4},
    {"key_id": "ak047", "probe_order": 593, "lo": 1152921573326324736, "hi": 1081344, "legal": 91, "s5_index": 896402, "membership_class_count": 4},
    {"key_id": "ak048", "probe_order": 594, "lo": 1152921573326324736, "hi": 1114112, "legal": 88, "s5_index": 896599, "membership_class_count": 3},
    {"key_id": "ak049", "probe_order": 595, "lo": 1152921573326324736, "hi": 34603008, "legal": 97, "s5_index": 896604, "membership_class_count": 4},
    {"key_id": "ak050", "probe_order": 597, "lo": 1152921573326324736, "hi": 70368745226240, "legal": 88, "s5_index": 896606, "membership_class_count": 2},
]

SCHEMA = "n11-centralreply-closure-batch40-keys-v1"


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
    cache_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(src, "canonical-cache-73482be0.cache")
    quarantine_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(src, "quarantine.json")
    refresh_path = sys.argv[3] if len(sys.argv) > 3 else os.path.join(src, "refresh-summary.json")
    closure_path = sys.argv[4] if len(sys.argv) > 4 else os.path.join(src, "closure-classes.csv")
    worklist_path = sys.argv[5] if len(sys.argv) > 5 else os.path.join(src, "worklist-class30118-extract.csv")
    universe_path = sys.argv[6] if len(sys.argv) > 6 else os.path.join(src, "prior-probe-universe.csv")
    freshness_path = sys.argv[7] if len(sys.argv) > 7 else os.path.join(src, "freshness-ranks1to21-b40.csv")
    b38_keys_path = sys.argv[8] if len(sys.argv) > 8 else os.path.join(src, "batch-keys-b38.json")
    universe_ext_path = sys.argv[9] if len(sys.argv) > 9 else os.path.join(src, "prior-probe-universe-b40.csv")
    b39_keys_path = sys.argv[10] if len(sys.argv) > 10 else os.path.join(src, "batch-keys-b39.json")
    ext_meta_path = sys.argv[11] if len(sys.argv) > 11 else os.path.join(src, "prior-probe-universe-b40.ext-meta.json")

    # G1 source pins
    for path, pin, what in [
        (b38_keys_path, PIN_B38_KEYS, "batch-38 batch-keys"),
        (b39_keys_path, PIN_B39_KEYS, "batch-39 batch-keys"),
        (refresh_path, PIN_REFRESH_SUMMARY, "refresh-summary"),
        (closure_path, PIN_CLOSURE_CLASSES, "closure-classes"),
        (cache_path, PIN_CANONICAL_CACHE, "canonical cache"),
        (quarantine_path, PIN_QUARANTINE, "quarantine"),
        (worklist_path, PIN_WORKLIST_EXTRACT, "worklist class-30118 extract"),
        (universe_path, PIN_UNIVERSE, "prior-probe universe (base)"),
        (universe_ext_path, PIN_UNIVERSE_EXT, "prior-probe universe (b40 ext)"),
        (ext_meta_path, PIN_EXT_META, "ext-provenance meta"),
        (freshness_path, PIN_FRESHNESS, "freshness table ranks 1..21"),
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
        if 1 <= rk <= 21:
            rank_class[rk] = r[1]

    # G3b freshness table ranks 1..21 (fresh-frontier machine assertion;
    # prior counts use the b40 extended universe, claimed = the in-flight
    # batch-38 target pairs)
    with open(freshness_path, "r", encoding="utf-8") as f:
        frows = [line.rstrip("\n").split(",") for line in f if line.strip()]
    if frows[0] != ["rank", "class_index", "unknown_now", "children", "prior_probe", "cache_hit", "claimed", "fresh"]:
        fail("G3b freshness header drift")
    fby_rank = {int(r[0]): r for r in frows[1:]}
    if sorted(fby_rank) != list(range(1, 22)):
        fail("G3b freshness table must cover exactly ranks 1..21")
    for rk in range(1, 22):
        if rk not in fby_rank:
            fail("G3b freshness missing rank %d" % rk)
        fr = fby_rank[rk]
        if fr[1] != rank_class.get(rk):
            fail("G3b freshness rank %d class %s != closure-classes %s" % (rk, fr[1], rank_class.get(rk)))
        if int(fr[2]) != int(fr[3]):
            fail("G3b rank %d unknown_now != children: %r" % (rk, fr))
        if int(fr[3]) != int(fr[4]) + int(fr[5]) + int(fr[6]) + int(fr[7]):
            fail("G3b rank %d children != prior+cache_hit+claimed+fresh: %r" % (rk, fr))
        if rk != 21 and int(fr[7]) != 0:
            fail("G3b rank %d is not fresh-0: %r" % (rk, fr))
    fr21 = fby_rank[21]
    if fr21[1] != str(CLASS_INDEX) or int(fr21[2]) != CLASS_UNKNOWN_NOW or int(fr21[3]) != CLASS_UNKNOWN_NOW:
        fail("G3b rank-21 row drift: %r" % (fr21,))
    if int(fr21[4]) != 0 or int(fr21[5]) != 0 or int(fr21[6]) != len(EMBEDDED_RESERVED) or int(fr21[7]) != len(EMBEDDED_TARGETS):
        fail("G3b rank-21 prior/cache/claimed/fresh accounting drift: %r" % (fr21,))

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
    if n_rows != CANONICAL_CACHE_ROWS:
        fail("G4 canonical cache s5verdict rows = %d, want %d" % (n_rows, CANONICAL_CACHE_ROWS))

    # G5 quarantine absence (50 targets + the 2 claim-reserved pairs)
    with open(quarantine_path, "r", encoding="utf-8") as f:
        q = json.load(f)
    active_keys = {tuple(e["key"]) for e in q.get("entries", []) if e.get("active")}
    for t in all_rows:
        if (t["lo"], t["hi"]) in active_keys:
            fail("G5 key %s is quarantined" % t.get("key_id"))

    # G6 worklist class-30118 extract cross-check (probe_order 546..597)
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
            fail("G6 target probe_order not ascending with ak id at %s" % t["key_id"])
        prev = t["probe_order"]

    # G7 prior-probe universe freshness (base and b40-extended)
    upairs = []
    with open(universe_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            a, b = line.rstrip("\n").split(",")
            upairs.append((int(a), int(b)))
    if len(upairs) != UNIVERSE_PAIRS:
        fail("G7 universe lines = %d, want %d" % (len(upairs), UNIVERSE_PAIRS))
    if upairs != sorted(set(upairs)):
        fail("G7 universe not sorted-unique ascending")
    upairs_ext = []
    with open(universe_ext_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            a, b = line.rstrip("\n").split(",")
            upairs_ext.append((int(a), int(b)))
    if len(upairs_ext) != UNIVERSE_EXT_PAIRS:
        fail("G7 extended universe lines = %d, want %d" % (len(upairs_ext), UNIVERSE_EXT_PAIRS))
    if upairs_ext != sorted(set(upairs_ext)):
        fail("G7 extended universe not sorted-unique ascending")
    uset = set(upairs)
    uset_ext = set(upairs_ext)
    if not uset <= uset_ext:
        fail("G7 extended universe is not a superset of the base universe")
    for t in EMBEDDED_TARGETS:
        if (t["lo"], t["hi"]) in uset:
            fail("G7 target %s was already prior-probed (base universe hit)" % t["key_id"])
        if (t["lo"], t["hi"]) in uset_ext:
            fail("G7 target %s was already prior-probed (extended universe hit)" % t["key_id"])
    for q in EMBEDDED_RESERVED:
        if (q["lo"], q["hi"]) in uset:
            fail("G7 reserved %s is inside the prior-probe universe" % q["batch38_key_id"])
        if (q["lo"], q["hi"]) in uset_ext:
            fail("G7 reserved %s is inside the extended prior-probe universe" % q["batch38_key_id"])

    # G9 extended-universe integrity (provenance: base + the 50 probed
    # batch-39 keys, cross-checked against the published batch-39 packet)
    with open(b39_keys_path, "r", encoding="utf-8") as f:
        b39_packet = json.load(f)
    b39_keys = b39_packet.get("keys", [])
    if len(b39_keys) != 50 or b39_packet.get("target_key_count") != 50:
        fail("G9 batch-39 packet has %d keys / target_key_count %r, want 50"
             % (len(b39_keys), b39_packet.get("target_key_count")))
    b39_ids = [k.get("key_id") for k in b39_keys]
    if b39_ids != ["aj%03d" % i for i in range(1, 51)]:
        fail("G9 batch-39 packet id set drift")
    if b39_packet.get("consumed_into_canonical_cache") is not False:
        fail("G9 batch-39 packet consumed flag drift")
    b39_pairs = set((int(k["lo"]), int(k["hi"])) for k in b39_keys)
    with open(ext_meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    added = [tuple(p) for p in meta.get("added_probed_batch39_keys", [])]
    if len(added) != 50 or set(added) != b39_pairs:
        fail("G9 ext-meta added set != batch-39 published target pairs")
    if meta.get("base_universe_sha256") != PIN_UNIVERSE or meta.get("base_universe_pairs") != UNIVERSE_PAIRS:
        fail("G9 ext-meta base universe provenance drift")
    if len(uset | b39_pairs) != UNIVERSE_EXT_PAIRS or (uset | b39_pairs) != uset_ext:
        fail("G9 extended universe != base UNION the 50 probed batch-39 keys")

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
        "batch": "batch-40",
        "description": "n11 central-reply closure batch-40: fresh (never-probed) 50 unknown cost-children of closure class 30118 (rank 21, fresh frontier per the post-b39loss46 reaudit and the ranks-1..21 freshness scan with the extended universe and claimed column), derived from the worklist regen extract; 2 of the 52 universe-fresh children are claim-reserved in-flight batch-38 targets (ai033/ai034, dual-class, Part EF single-owner, verdict path owned by EF/adoption) and are NOT targets",
        "target_key_count": len(EMBEDDED_TARGETS),
        "claim_reserved_excluded": [
            {"key_id": q["batch38_key_id"], "batch": "batch-38 (closure class 30345 packet, Part EF in-flight, published batch-keys-b38.json)",
             "probe_order": q["probe_order"], "lo": q["lo"], "hi": q["hi"], "legal": q["legal"],
             "s5_index": q["s5_index"], "membership_class_count": q["membership_class_count"],
             "note": "dual-class child (30345/30118); in-flight claimed by the Part EF single-owner drive; same-condition re-probe prohibited; excluded from batch-40 targets"}
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
            "batch39_batch_keys": PIN_B39_KEYS,
            "refresh_summary": PIN_REFRESH_SUMMARY,
            "closure_classes": PIN_CLOSURE_CLASSES,
            "canonical_cache": PIN_CANONICAL_CACHE,
            "quarantine": PIN_QUARANTINE,
            "worklist_class30118_extract": PIN_WORKLIST_EXTRACT,
            "prior_probe_universe_base": PIN_UNIVERSE,
            "prior_probe_universe_b40_ext": PIN_UNIVERSE_EXT,
            "prior_probe_universe_b40_ext_meta": PIN_EXT_META,
            "freshness_ranks1to21_b40": PIN_FRESHNESS,
            "jsreplay": "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
            "runbatch": "f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84",
        },
        "gates": ["G1-source-sha-pins", "G2-batch38-packet-claim-reserved-provenance",
                  "G3-closure-rank-anchor-and-accounting",
                  "G3b-freshness-frontier-ranks1to21",
                  "G4-exact-pair-absent-in-canonical-cache",
                  "G5-not-quarantined",
                  "G6-worklist-extract-field-match",
                  "G7-prior-probe-universe-freshness",
                  "G9-extended-universe-integrity"],
        "canonical_cache_s5verdict_rows": n_rows,
        "consumed_into_canonical_cache": False,
    }
    tmp = os.path.join(input_dir, "batch-keys-b40.json.tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(keys_doc, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, os.path.join(input_dir, "batch-keys-b40.json"))

    print("make_batch40_keys: ALL GATES PASS, wrote %d inputs + batch-keys-b40.json" % len(EMBEDDED_TARGETS))


if __name__ == "__main__":
    main()
