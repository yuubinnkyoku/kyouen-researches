#!/usr/bin/env python3
"""make_batch37_keys.py - batch-37 (n11 central-reply closure class 16371)
key derivation with fail-closed gates.

Scope: the 47 clean (never-probed, honest-label-free) unknown cost-children
of closure class 16371 (class_rank 10, mask [1153202979851993088, 16]) in
the published post-b35loss26-adoption reaudit (refresh-summary.json
5fe3e5ab..., closure-classes.csv b7241eb0..., canonical cache 23d40e36...).

Key set provenance (no hand transcription): the published batch-4 packet
(research/experiments/n11-centralreply-closure-class16371-batch4-20261122)
probed exactly 2 of its 50 keys on 2026-11-22 (e001 PASS LOSS
15000000,2,882800 / e002 PASS WIN 15000000,1,14112632 with WIN-HALT
marker) and stopped; e001's LOSS verdict and e002's WIN verdict were never
consumed into the canonical chain (e002 requires the scrutiny-owner C++
gate). One further packet key, e022 (s5 546606, dual-class 16371/23101,
probed as batch-14 q007 on 2026-11-22 PASS LOSS 15000000,2,1494975), IS
already consumed into the canonical chain cache and is therefore NOT part
of the class-16371 unknown set. This box derives the 47 clean keys
(= packet e003..e050 minus e022) from the published packet, cross-checks
all 49 current unknowns against the class-16371 worklist extract (probe
orders 126..174 of the byte-identical probe-worklist.csv regen, sha
86767be9...), and asserts the accounting 49 unknown_now == 2 (probed
honest labels, none consumed) + 47 (clean).

Gates (all fail-closed, rc=1 on any violation, no partial outputs on failure):
  G1  source sha pins: batch-4 packet (2 files) + refresh-summary + closure
      classes + canonical cache + quarantine + worklist class-16371 extract
      must match the published sha256 values byte-exactly.
  G2  batch-4 packet integrity: 50 keys with ids e001..e050; status.log has
      exactly 2 PASS rows (1 LOSS result 2: e001 + 1 WIN result 1: e002)
      and one e002 WIN-HALT row; every embedded row matches the packet
      (lo, hi, legal, s5_index, membership_class_count); clean == packet
      minus status-PASS ids minus the canonically-consumed e022 == 47 keys
  G3  closure-classes.csv rank 10 == class 16371 with unknown_now 49, and
      49 == 2 (probed honest labels) + 47 (clean) accounting
  G4  exact key pairs (lo,hi) of all 49 unknowns (47 targets + 2 probed)
      absent from the canonical merged chain cache (pair-level parse of all
      s5verdict rows; same-lo rows are counted and reported as context,
      never adopted); G4b: the consumed e022 pair IS present in the cache
      as result 2 nodes 1494975 (adopted-loss row) and is excluded from
      targets
  G5  none of the 47 targets appears in the active quarantine registry
  G6  worklist class-16371 extract: exactly 49 rows, probe_order 126..174
      contiguous ascending; every row's (lo, hi, legal, s5_index,
      membership_class_count, serving_class, class_unknown_now) matches the
      corresponding packet key; the consumed e022 pair is NOT in the extract
      (no hand re-typing; the jsreplay solver independently re-derives legal
      at run time and hard-fails on mismatch)

Outputs (written atomically only after all gates pass):
  input/e003.input.csv ... input/e050.input.csv (minus e022; 47 files)
      (format: target,0,5,lo,hi,legal,0,0,0,0,0 - identical schema to the
       published batch-33/34/35/36 inputs)
  input/batch-keys-b37.json
      schema n11-centralreply-closure-batch37-keys-v1, pins included,
      consumed_into_canonical_cache=false

Determinism: pure function of the pinned inputs; run 3x byte-identical in
the completion protocol. Tamper battery (scratch copies) must ABORT on: pin
drift, packet field drift, status drift, cache hit, quarantine hit,
closure-table rank drift, worklist extract field drift.
"""
import hashlib
import json
import os
import re
import sys

PIN_B4_KEYS = "70b8a4c89f7cea454bfd2b52f720245b6d9c5d7311878bf8aac637940825ecdf"
PIN_B4_STATUS = "63c2d9693a374453bea604b85e1b69ac41c06a214675ea63100a675b1f064ac0"
PIN_REFRESH_SUMMARY = "5fe3e5ab176df05ef30894d6e0df6ceb292d3ac2280ff543e94bbee69e549de4"
PIN_CLOSURE_CLASSES = "b7241eb046e32f4900c9f9a976ada326c5124ad18c01de6b4eb40b97a8a7f24e"
PIN_CANONICAL_CACHE = "23d40e36ed1730ace4986461995dfc0ee606a380da9b156cdddaf09ef8a29822"
PIN_QUARANTINE = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
PIN_WORKLIST_EXTRACT = "da8130274f0dcbeb57ed7994f0a7f210f7c04c641b0f2ebb24b22956e94ffdbc"

CLASS_INDEX = 16371
CLASS_MASK = [1153202979851993088, 16]
CLASS_RANK = 10
CLASS_UNKNOWN_NOW = 49
WORKLIST_ORDER_FIRST = 126
WORKLIST_ORDER_LAST = 174

# the 2 already-probed honest-labeled keys of class 16371 (batch-4,
# 2026-11-22, 2-pass fresh-cold node-exact; verdicts NOT consumed: e001's
# LOSS row is absent from the canonical chain, e002's WIN is unconsumable
# without the scrutiny-owner C++ gate). They are NOT batch-37 targets; they
# are gate-checked for bookkeeping consistency (status/labels + cache
# absence + worklist order + legal cross-check).
EMBEDDED_PROBED = [
    {"key_id": "e001", "lo": 10376575016706768896, "hi": 16, "legal": 88, "s5_index": 93170, "membership_class_count": 4},
    {"key_id": "e002", "lo": 1153765929805414400, "hi": 16, "legal": 79, "s5_index": 183566, "membership_class_count": 4}
]
PROBED_LABELS = {"e001": 2, "e002": 1}
PROBED_NODES = {"e001": 882800, "e002": 14112632}

# the canonically-consumed packet key e022 (dual-class 16371/23101, probed
# as batch-14 q007 on 2026-11-22): PASS LOSS 15000000,2,1494975, consumed
# into the canonical chain cache. Absent from the class-16371 worklist by
# construction; gate-checked in G4b (present in cache) and G6 (absent from
# the worklist extract).
EMBEDDED_ADOPTED = [
    {"key_id": "e022", "lo": 1153202979868770304, "hi": 16, "legal": 78, "s5_index": 546606, "membership_class_count": 3}
]
ADOPTED_CACHE_RES = 2
ADOPTED_CACHE_NODES = 1494975

# the 47 clean targets, embedded from the published batch-4 packet rows
# (verified against the pinned published file at run time).
EMBEDDED_TARGETS = [
    {"key_id": "e003", "lo": 5764888998279380992, "hi": 16, "legal": 88, "s5_index": 306951, "membership_class_count": 4},
    {"key_id": "e004", "lo": 1153202979851993088, "hi": 17, "legal": 75, "s5_index": 399422, "membership_class_count": 4},
    {"key_id": "e005", "lo": 1153202979851993088, "hi": 18, "legal": 92, "s5_index": 480806, "membership_class_count": 4},
    {"key_id": "e006", "lo": 1153202979851993090, "hi": 16, "legal": 93, "s5_index": 498207, "membership_class_count": 4},
    {"key_id": "e007", "lo": 1153202979851993092, "hi": 16, "legal": 86, "s5_index": 502385, "membership_class_count": 4},
    {"key_id": "e008", "lo": 1153202979851993096, "hi": 16, "legal": 92, "s5_index": 505442, "membership_class_count": 4},
    {"key_id": "e009", "lo": 1153202979851993104, "hi": 16, "legal": 85, "s5_index": 509234, "membership_class_count": 4},
    {"key_id": "e010", "lo": 1153202979851993152, "hi": 16, "legal": 90, "s5_index": 512923, "membership_class_count": 4},
    {"key_id": "e011", "lo": 1153202979851993216, "hi": 16, "legal": 93, "s5_index": 516385, "membership_class_count": 4},
    {"key_id": "e012", "lo": 1153202979851993600, "hi": 16, "legal": 93, "s5_index": 522643, "membership_class_count": 4},
    {"key_id": "e013", "lo": 1153202979851994112, "hi": 16, "legal": 87, "s5_index": 525693, "membership_class_count": 4},
    {"key_id": "e014", "lo": 1153202979851997184, "hi": 16, "legal": 82, "s5_index": 528188, "membership_class_count": 3},
    {"key_id": "e015", "lo": 1153202979852001280, "hi": 16, "legal": 88, "s5_index": 530117, "membership_class_count": 4},
    {"key_id": "e016", "lo": 1153202979852009472, "hi": 16, "legal": 89, "s5_index": 532225, "membership_class_count": 4},
    {"key_id": "e017", "lo": 1153202979852025856, "hi": 16, "legal": 87, "s5_index": 534675, "membership_class_count": 4},
    {"key_id": "e018", "lo": 1153202979852124160, "hi": 16, "legal": 91, "s5_index": 537035, "membership_class_count": 4},
    {"key_id": "e019", "lo": 1153202979852517376, "hi": 16, "legal": 89, "s5_index": 541141, "membership_class_count": 4},
    {"key_id": "e020", "lo": 1153202979853041664, "hi": 16, "legal": 84, "s5_index": 543110, "membership_class_count": 4},
    {"key_id": "e021", "lo": 1153202979854090240, "hi": 16, "legal": 92, "s5_index": 544907, "membership_class_count": 4},
    {"key_id": "e023", "lo": 1153202979885547520, "hi": 16, "legal": 86, "s5_index": 547319, "membership_class_count": 4},
    {"key_id": "e024", "lo": 1153202979919101952, "hi": 16, "legal": 80, "s5_index": 548819, "membership_class_count": 4},
    {"key_id": "e025", "lo": 1154328879758835712, "hi": 16, "legal": 80, "s5_index": 549855, "membership_class_count": 4},
    {"key_id": "e026", "lo": 1153202980388864000, "hi": 16, "legal": 87, "s5_index": 550280, "membership_class_count": 4},
    {"key_id": "e027", "lo": 1153202980925734912, "hi": 16, "legal": 79, "s5_index": 550330, "membership_class_count": 4},
    {"key_id": "e028", "lo": 1153202981999476736, "hi": 16, "legal": 89, "s5_index": 550357, "membership_class_count": 4},
    {"key_id": "e029", "lo": 1153202984146960384, "hi": 16, "legal": 91, "s5_index": 550403, "membership_class_count": 4},
    {"key_id": "e030", "lo": 1153203048571469824, "hi": 16, "legal": 74, "s5_index": 550446, "membership_class_count": 3},
    {"key_id": "e031", "lo": 1153205178875248640, "hi": 16, "legal": 84, "s5_index": 550549, "membership_class_count": 4},
    {"key_id": "e032", "lo": 1153207377898504192, "hi": 16, "legal": 88, "s5_index": 550593, "membership_class_count": 4},
    {"key_id": "e033", "lo": 1153211775945015296, "hi": 16, "legal": 93, "s5_index": 550622, "membership_class_count": 4},
    {"key_id": "e034", "lo": 1171217378361475072, "hi": 16, "legal": 86, "s5_index": 550719, "membership_class_count": 4},
    {"key_id": "e035", "lo": 1162210179106734080, "hi": 16, "legal": 86, "s5_index": 550757, "membership_class_count": 4},
    {"key_id": "e036", "lo": 1157706579479363584, "hi": 16, "legal": 83, "s5_index": 550795, "membership_class_count": 4},
    {"key_id": "e037", "lo": 1154047404580798464, "hi": 1028, "legal": 82, "s5_index": 550839, "membership_class_count": 4},
    {"key_id": "e038", "lo": 1154047404580798464, "hi": 1032, "legal": 84, "s5_index": 550868, "membership_class_count": 4},
    {"key_id": "e039", "lo": 1153202979851993088, "hi": 528, "legal": 80, "s5_index": 550876, "membership_class_count": 4},
    {"key_id": "e040", "lo": 1153202979851993088, "hi": 1040, "legal": 77, "s5_index": 550877, "membership_class_count": 4},
    {"key_id": "e041", "lo": 1157425104234221568, "hi": 268435712, "legal": 84, "s5_index": 550878, "membership_class_count": 3},
    {"key_id": "e042", "lo": 1153202979851993088, "hi": 272, "legal": 78, "s5_index": 550879, "membership_class_count": 3},
    {"key_id": "e043", "lo": 1157425104234217473, "hi": 268435712, "legal": 76, "s5_index": 550880, "membership_class_count": 3},
    {"key_id": "e044", "lo": 1154047404580798464, "hi": 33555456, "legal": 87, "s5_index": 550882, "membership_class_count": 4},
    {"key_id": "e045", "lo": 1154047404580798464, "hi": 16778240, "legal": 94, "s5_index": 550883, "membership_class_count": 4},
    {"key_id": "e046", "lo": 1154047404580798464, "hi": 17408, "legal": 90, "s5_index": 550884, "membership_class_count": 4},
    {"key_id": "e047", "lo": 1157425104234217474, "hi": 268435712, "legal": 94, "s5_index": 550885, "membership_class_count": 4},
    {"key_id": "e048", "lo": 1154047404580798464, "hi": 9216, "legal": 92, "s5_index": 550886, "membership_class_count": 4},
    {"key_id": "e049", "lo": 1154047404580798464, "hi": 33792, "legal": 91, "s5_index": 550887, "membership_class_count": 4},
    {"key_id": "e050", "lo": 1154047404580798464, "hi": 66560, "legal": 76, "s5_index": 550888, "membership_class_count": 3}
]

SCHEMA = "n11-centralreply-closure-batch37-keys-v1"


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
    b4 = os.path.join(src, "batch4-packet")
    cache_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(src, "canonical-cache-23d40e36.cache")
    quarantine_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(src, "quarantine.json")
    refresh_path = sys.argv[3] if len(sys.argv) > 3 else os.path.join(src, "refresh-summary.json")
    closure_path = sys.argv[4] if len(sys.argv) > 4 else os.path.join(src, "closure-classes.csv")
    worklist_path = sys.argv[5] if len(sys.argv) > 5 else os.path.join(src, "worklist-class16371-extract.csv")
    b4_keys_path = sys.argv[6] if len(sys.argv) > 6 else os.path.join(b4, "batch-keys.json")
    b4_status_path = sys.argv[7] if len(sys.argv) > 7 else os.path.join(b4, "status.log")

    # G1 source pins
    for path, pin, what in [
        (b4_keys_path, PIN_B4_KEYS, "batch-4 batch-keys"),
        (b4_status_path, PIN_B4_STATUS, "batch-4 status.log"),
        (refresh_path, PIN_REFRESH_SUMMARY, "refresh-summary"),
        (closure_path, PIN_CLOSURE_CLASSES, "closure-classes"),
        (cache_path, PIN_CANONICAL_CACHE, "canonical cache"),
        (quarantine_path, PIN_QUARANTINE, "quarantine"),
        (worklist_path, PIN_WORKLIST_EXTRACT, "worklist class-16371 extract"),
    ]:
        if sha256_file(path) != pin:
            fail("G1 pin mismatch on %s (%s)" % (what, path))

    # G2 batch-4 packet integrity
    with open(b4_keys_path, "r", encoding="utf-8") as f:
        packet = json.load(f)
    keys = packet.get("keys", [])
    if len(keys) != 50:
        fail("G2 batch-4 packet has %d keys, want 50" % len(keys))
    ids = [k.get("key_id") for k in keys]
    want_ids = ["e%03d" % i for i in range(1, 51)]
    if ids != want_ids:
        fail("G2 batch-4 packet id set drift")
    pkt = {k["key_id"]: k for k in keys}
    for t in EMBEDDED_PROBED + EMBEDDED_ADOPTED + EMBEDDED_TARGETS:
        row = pkt[t["key_id"]]
        for field in ("lo", "hi", "legal", "s5_index", "membership_class_count"):
            if row.get(field) != t[field]:
                fail("G2 embedded row %s field %s drift: packet %r embedded %r"
                     % (t["key_id"], field, row.get(field), t[field]))

    pass_re = re.compile(r"^\S+ (e\d{3}) PASS (\d+),(\d+),(\d+)$")
    halt_re = re.compile(r"^\S+ (e\d{3}) WIN-HALT$")
    pass_rows = {}
    halt_rows = []
    with open(b4_status_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            m = pass_re.match(line)
            if m:
                if m.group(1) in pass_rows:
                    fail("G2 batch-4 status.log duplicate PASS row for %s" % m.group(1))
                pass_rows[m.group(1)] = (int(m.group(2)), int(m.group(3)), int(m.group(4)))
                continue
            m = halt_re.match(line)
            if m:
                halt_rows.append(m.group(1))
    if len(pass_rows) != 2:
        fail("G2 batch-4 status.log PASS rows = %d, want 2" % len(pass_rows))
    if halt_rows != ["e002"]:
        fail("G2 batch-4 status.log WIN-HALT rows drift: %r" % (halt_rows,))
    if sorted(pass_rows) != ["e001", "e002"]:
        fail("G2 batch-4 status.log PASS id set drift: %r" % sorted(pass_rows))
    for kid, want in PROBED_LABELS.items():
        got = pass_rows.get(kid)
        if got is None:
            fail("G2 batch-4 status.log missing PASS row %s" % kid)
        if got[0] != 15000000:
            fail("G2 batch-4 status.log budget drift on %s" % kid)
        if got[1] != want:
            fail("G2 batch-4 status.log result drift on %s: %d want %d" % (kid, got[1], want))
        if got[2] != PROBED_NODES[kid]:
            fail("G2 batch-4 status.log nodes drift on %s: %d want %d" % (kid, got[2], PROBED_NODES[kid]))
    loss_ids = sorted(k for k, v in pass_rows.items() if v[1] == 2)
    win_ids = sorted(k for k, v in pass_rows.items() if v[1] == 1)
    if loss_ids != ["e001"] or win_ids != ["e002"]:
        fail("G2 batch-4 status.log LOSS/WIN key sets drift: %r %r" % (loss_ids, win_ids))
    probed_ids = set(pass_rows)
    adopted_ids = {t["key_id"] for t in EMBEDDED_ADOPTED}
    clean_ids = [k["key_id"] for k in keys if k["key_id"] not in probed_ids and k["key_id"] not in adopted_ids]
    want_clean = sorted(clean_ids)
    if len(clean_ids) != 47:
        fail("G2 clean set size %d, want 47" % len(clean_ids))
    if sorted(k["key_id"] for k in EMBEDDED_PROBED) != sorted(probed_ids):
        fail("G2 embedded probed set drift")
    if sorted(k["key_id"] for k in EMBEDDED_ADOPTED) != sorted(adopted_ids) or sorted(adopted_ids) != ["e022"]:
        fail("G2 embedded adopted set drift")
    if sorted(k["key_id"] for k in EMBEDDED_TARGETS) != sorted(clean_ids):
        fail("G2 embedded target set drift")
    probed_emb = {t["key_id"]: t for t in EMBEDDED_PROBED}
    for kid in probed_ids:
        row = pkt[kid]
        if row["lo"] != probed_emb[kid]["lo"] or row["hi"] != probed_emb[kid]["hi"]:
            fail("G2 probed key %s pair drift vs packet" % kid)

    # G3 closure-classes rank anchor + accounting
    with open(closure_path, "r", encoding="utf-8") as f:
        rows = [line.rstrip("\n").split(",") for line in f if line.strip()]
    header = rows[0]
    if header[:2] != ["class_rank", "class_index"]:
        fail("G3 closure-classes header drift")
    by_rank = {r[0]: r for r in rows[1:]}
    crow = by_rank.get(str(CLASS_RANK))
    if crow is None or crow[1] != str(CLASS_INDEX):
        fail("G3 rank %d is not class %d" % (CLASS_RANK, CLASS_INDEX))
    if crow[4] != str(CLASS_UNKNOWN_NOW):
        fail("G3 class %d unknown_now %s, want %d" % (CLASS_INDEX, crow[4], CLASS_UNKNOWN_NOW))
    if crow[2] != str(CLASS_MASK[0]) or crow[3] != str(CLASS_MASK[1]):
        fail("G3 class %d mask drift" % CLASS_INDEX)
    if CLASS_UNKNOWN_NOW != len(EMBEDDED_PROBED) + len(EMBEDDED_TARGETS):
        fail("G3 accounting: %d != %d (probed) + %d (clean)"
             % (CLASS_UNKNOWN_NOW, len(EMBEDDED_PROBED), len(EMBEDDED_TARGETS)))

    # G4 exact-pair absence in canonical cache (+ same-lo context) + G4b adopted presence
    all_rows = EMBEDDED_TARGETS + EMBEDDED_PROBED
    wanted = {t["key_id"]: (t["lo"], t["hi"]) for t in all_rows}
    wanted_pairs = set(wanted.values())
    adopted = EMBEDDED_ADOPTED[0]
    adopted_pair = (adopted["lo"], adopted["hi"])
    present = {}
    adopted_cache_row = None
    same_lo = {t["lo"]: 0 for t in all_rows}
    n_rows = 0
    with open(cache_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("s5verdict,"):
                n_rows += 1
                p = line.rstrip("\n").split(",")
                lo, hi = int(p[1]), int(p[2])
                if (lo, hi) in wanted_pairs:
                    present[(lo, hi)] = line.strip()
                elif (lo, hi) == adopted_pair:
                    if int(p[4]) != ADOPTED_CACHE_RES or int(p[5]) != ADOPTED_CACHE_NODES:
                        fail("G4b adopted e022 cache row drift: %s" % line.strip())
                    adopted_cache_row = line.strip()
                elif lo in same_lo:
                    same_lo[lo] += 1
    if present:
        fail("G4 canonical cache already contains key(s): %r" % sorted(present))
    if adopted_cache_row is None:
        fail("G4b adopted e022 (q007) row missing from canonical cache")

    # G5 quarantine absence
    with open(quarantine_path, "r", encoding="utf-8") as f:
        q = json.load(f)
    active_keys = {tuple(e["key"]) for e in q.get("entries", []) if e.get("active")}
    for t in EMBEDDED_TARGETS:
        if (t["lo"], t["hi"]) in active_keys:
            fail("G5 key %s is quarantined" % t["key_id"])

    # G6 worklist class-16371 extract cross-check (probe_order 126..174)
    with open(worklist_path, "r", encoding="utf-8") as f:
        wl = [line.rstrip("\n").split(",") for line in f if line.strip()]
    wl_header = wl[0]
    if wl_header[:2] != ["probe_order", "s5_index"]:
        fail("G6 worklist extract header drift")
    wl_rows = wl[1:]
    if len(wl_rows) != CLASS_UNKNOWN_NOW:
        fail("G6 worklist extract rows = %d, want %d" % (len(wl_rows), CLASS_UNKNOWN_NOW))
    orders = [int(r[0]) for r in wl_rows]
    if orders != list(range(WORKLIST_ORDER_FIRST, WORKLIST_ORDER_LAST + 1)):
        fail("G6 worklist extract probe_order not contiguous %d..%d" % (WORKLIST_ORDER_FIRST, WORKLIST_ORDER_LAST))
    worklist_order_map = {}
    for r in wl_rows:
        (po, s5, lo, hi, legal, scl, cun, cf, ct, mcc) = r
        if int(scl) != CLASS_INDEX:
            fail("G6 worklist extract serving_class drift: %s" % scl)
        if int(cun) != CLASS_UNKNOWN_NOW:
            fail("G6 worklist extract class_unknown_now drift")
        if (int(lo), int(hi)) == adopted_pair:
            fail("G6 consumed e022 pair appears in the class-16371 worklist extract")
        kid = None
        for t in all_rows:
            if t["lo"] == int(lo) and t["hi"] == int(hi):
                kid = t["key_id"]
                break
        if kid is None:
            fail("G6 worklist row (%s,%s) not in packet unknown set" % (lo, hi))
        worklist_order_map[kid] = int(po)
        emb = {t["key_id"]: t for t in all_rows}[kid]
        if int(s5) != emb["s5_index"] or int(legal) != emb["legal"]:
            fail("G6 worklist row %s s5/legal drift" % kid)
        if int(mcc) != emb["membership_class_count"]:
            fail("G6 worklist row %s membership drift" % kid)
    if len(worklist_order_map) != CLASS_UNKNOWN_NOW:
        fail("G6 worklist extract does not cover all %d packet unknowns" % CLASS_UNKNOWN_NOW)
    prev = -1
    for i, kid in enumerate(ids):
        if kid in worklist_order_map:
            if worklist_order_map[kid] <= prev:
                fail("G6 worklist order not ascending with packet order at %s" % kid)
            prev = worklist_order_map[kid]

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
        "batch": "batch-37",
        "description": "n11 central-reply closure batch-37: clean (never-probed) 47 unknown cost-children of closure class 16371 (rank 10), derived from the published batch-4 packet (50 keys: 2 probed honest-labeled unconsumed e001/e002, 1 canonically-consumed dual-class e022=batch-14 q007), post-b35loss26 reaudit",
        "target_key_count": len(EMBEDDED_TARGETS),
        "probed_unconsumed_same_class": [
            {"key_id": t["key_id"], "budget_result_nodes": "15000000,%d,%d" % (PROBED_LABELS[t["key_id"]], PROBED_NODES[t["key_id"]]),
             "probe_order": worklist_order_map[t["key_id"]],
             "note": "batch-4 (2026-11-22) 2-pass node-exact; verdict not consumed into the canonical chain; unconsumed-WIN e002 requires the scrutiny-owner C++ gate"}
            for t in EMBEDDED_PROBED
        ],
        "consumed_dual_class_excluded": [
            {"key_id": adopted["key_id"], "s5_index": adopted["s5_index"],
             "dual_class_identity": "batch-14 q007 (class 23101 packet, lo/hi identical)",
             "cache_row": adopted_cache_row,
             "note": "already consumed into the canonical chain (LOSS); excluded from batch-37 targets and absent from the class-16371 worklist extract"}
        ],
        "keys": [
            {
                "key_id": t["key_id"],
                "probe_order": worklist_order_map[t["key_id"]],
                "batch4_key_id": t["key_id"],
                "serving_class": CLASS_INDEX,
                "class_mask": CLASS_MASK,
                "class_unknown_now_at_selection": CLASS_UNKNOWN_NOW,
                "lo": t["lo"],
                "hi": t["hi"],
                "legal": t["legal"],
                "s5_index": t["s5_index"],
                "membership_class_count": t["membership_class_count"],
                "canonical_cache_same_lo_rows_context": same_lo[t["lo"]],
            }
            for t in EMBEDDED_TARGETS
        ],
        "pins": {
            "batch4_batch_keys": PIN_B4_KEYS,
            "batch4_status": PIN_B4_STATUS,
            "refresh_summary": PIN_REFRESH_SUMMARY,
            "closure_classes": PIN_CLOSURE_CLASSES,
            "canonical_cache": PIN_CANONICAL_CACHE,
            "quarantine": PIN_QUARANTINE,
            "worklist_class16371_extract": PIN_WORKLIST_EXTRACT,
            "jsreplay": "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
            "runbatch": "f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84",
        },
        "gates": ["G1-source-sha-pins", "G2-batch4-packet-integrity",
                  "G3-closure-rank-anchor-and-accounting",
                  "G4-exact-pair-absent-in-canonical-cache",
                  "G4b-adopted-e022-cache-presence",
                  "G5-not-quarantined", "G6-worklist-extract-field-match"],
        "canonical_cache_s5verdict_rows": n_rows,
        "consumed_into_canonical_cache": False,
    }
    tmp = os.path.join(input_dir, "batch-keys-b37.json.tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(keys_doc, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, os.path.join(input_dir, "batch-keys-b37.json"))

    print("make_batch37_keys: ALL GATES PASS, wrote %d inputs + batch-keys-b37.json" % len(EMBEDDED_TARGETS))


if __name__ == "__main__":
    main()
