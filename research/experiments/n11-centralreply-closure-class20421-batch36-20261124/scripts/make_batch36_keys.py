#!/usr/bin/env python3
"""make_batch36_keys.py - batch-36 (n11 central-reply closure class 20421)
key derivation with fail-closed gates.

Scope: the 45 clean (never-probed, honest-label-free) unknown cost-children
of closure class 20421 (class_rank 9, mask [1155173304420536320, 131072]) in
the published post-b35loss26-adoption reaudit (refresh-summary.json 5fe3e5ab...,
closure-classes.csv b7241eb0..., canonical cache 23d40e36...).

Key set provenance (no hand transcription): the published batch-3 packet
(research/experiments/n11-centralreply-closure-class20421-batch-20261122)
probed exactly 4 of its 49 keys on 2026-11-22 (d001 PASS LOSS 15000000,2,879510
/ d003 PASS LOSS 15000000,2,2113678 / d002 PASS WIN 15000000,1,5359994 with
WIN-HALT marker / d004 PASS LOSS 15000000,2,11969338); the 3 LOSS rows were
never consumed into the canonical chain and the WIN is unconsumed (scrutiny
owner C++ gate pending), so class 20421 still holds 45 honest-label-free keys
d005..d049. This box derives those 45 clean keys from the published packet,
cross-checks all 49 keys against the class-20421 worklist extract (probe
orders 77..125 of the byte-identical probe-worklist.csv regen, sha 86767be9...),
and asserts the accounting 49 unknown_now == 4 (probed honest labels, none
consumed) + 45 (clean).

Gates (all fail-closed, rc=1 on any violation, no partial outputs on failure):
  G1  source sha pins: batch-3 packet (2 files) + refresh-summary + closure
      classes + canonical cache + quarantine + worklist class-20421 extract
      must match the published sha256 values byte-exactly.
  G2  batch-3 packet integrity: 49 keys with ids d001..d049; status.log has
      exactly 4 PASS rows (3 LOSS result 2: d001/d003/d004 + 1 WIN result 1:
      d002) and one d002 WIN-HALT row; every embedded row matches the packet
      (lo, hi, legal, s5_index, membership_class_count); clean == packet minus
      status-PASS ids == {d005..d049}
  G3  closure-classes.csv rank 9 == class 20421 with unknown_now 49, and
      49 == 4 (probed honest labels) + 45 (clean) accounting
  G4  exact key pairs (lo,hi) of all 49 keys (45 targets + 4 probed) absent
      from the canonical merged chain cache (pair-level parse of all s5verdict
      rows; same-lo rows are counted and reported as context, never adopted)
  G5  none of the 45 targets appears in the active quarantine registry entries
  G6  worklist class-20421 extract: exactly 49 rows, probe_order 77..125
      contiguous ascending; every row's (lo, hi, legal, s5_index,
      membership_class_count, serving_class, class_unknown_now) matches the
      corresponding packet key (no hand re-typing; the jsreplay solver
      independently re-derives legal at run time and hard-fails on mismatch)

Outputs (written atomically only after all gates pass):
  input/d005.input.csv ... input/d049.input.csv
      (format: target,0,5,lo,hi,legal,0,0,0,0,0 - identical schema to the
       published batch-33/34/35 inputs)
  input/batch-keys-b36.json
      schema n11-centralreply-closure-batch36-keys-v1, pins included,
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

PIN_B3_KEYS = "ad05073a845e511669d28fde3691fe9f3bf9f08eef2021039c884f1411f6dd3f"
PIN_B3_STATUS = "7877f4a085b466289b7647a1d88b98b755afa2065efae8f59c01bb10dca4cbbb"
PIN_REFRESH_SUMMARY = "5fe3e5ab176df05ef30894d6e0df6ceb292d3ac2280ff543e94bbee69e549de4"
PIN_CLOSURE_CLASSES = "b7241eb046e32f4900c9f9a976ada326c5124ad18c01de6b4eb40b97a8a7f24e"
PIN_CANONICAL_CACHE = "23d40e36ed1730ace4986461995dfc0ee606a380da9b156cdddaf09ef8a29822"
PIN_QUARANTINE = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
PIN_WORKLIST_EXTRACT = "2e6102be49eb997b833f68dea99151924c353f3d771b6574ff881c1321c55c99"

CLASS_INDEX = 20421
CLASS_MASK = [1155173304420536320, 131072]
CLASS_RANK = 9
CLASS_UNKNOWN_NOW = 49
WORKLIST_ORDER_FIRST = 77

# the 4 already-probed honest-labeled keys of class 20421 (batch-3,
# 2026-11-22, 2-pass fresh-cold node-exact; verdicts NOT consumed: 3 LOSS
# rows absent from the canonical chain, 1 WIN unwinnable without the
# scrutiny-owner C++ gate). They are NOT batch-36 targets; they are
# gate-checked for bookkeeping consistency (status/labels + cache absence +
# worklist order + legal cross-check).
EMBEDDED_PROBED = [
    {"key_id": "d001", "lo": 1155173304554754048, "hi": 131072, "legal": 77, "s5_index": 38215, "membership_class_count": 4},
    {"key_id": "d002", "lo": 3461016313634230272, "hi": 131072, "legal": 73, "s5_index": 197253, "membership_class_count": 4},
    {"key_id": "d003", "lo": 1155173579298443264, "hi": 131072, "legal": 86, "s5_index": 259023, "membership_class_count": 4},
    {"key_id": "d004", "lo": 5766859322847924224, "hi": 131072, "legal": 86, "s5_index": 300778, "membership_class_count": 4},
]
PROBED_LABELS = {"d001": 2, "d002": 1, "d003": 2, "d004": 2}
PROBED_NODES = {"d001": 879510, "d002": 5359994, "d003": 2113678, "d004": 11969338}

# the 45 clean targets, embedded from the published batch-3 packet rows
# (verified against the pinned published file at run time).
EMBEDDED_TARGETS = [
    {"key_id": "d005", "lo": 1155173304420601856, "hi": 131072, "legal": 87, "s5_index": 356378, "membership_class_count": 4},
    {"key_id": "d006", "lo": 1155173304420536320, "hi": 131073, "legal": 85, "s5_index": 393798, "membership_class_count": 4},
    {"key_id": "d007", "lo": 1155173304420536352, "hi": 131072, "legal": 82, "s5_index": 441775, "membership_class_count": 4},
    {"key_id": "d008", "lo": 1155454779397246976, "hi": 131072, "legal": 76, "s5_index": 528689, "membership_class_count": 3},
    {"key_id": "d009", "lo": 1156299204327378944, "hi": 131072, "legal": 73, "s5_index": 543795, "membership_class_count": 4},
    {"key_id": "d010", "lo": 1155173304420537344, "hi": 131072, "legal": 86, "s5_index": 565995, "membership_class_count": 4},
    {"key_id": "d011", "lo": 1155173304422633472, "hi": 131072, "legal": 79, "s5_index": 570139, "membership_class_count": 4},
    {"key_id": "d012", "lo": 1155173308715503616, "hi": 131072, "legal": 91, "s5_index": 574236, "membership_class_count": 4},
    {"key_id": "d013", "lo": 1155182100513558528, "hi": 131072, "legal": 89, "s5_index": 578232, "membership_class_count": 4},
    {"key_id": "d014", "lo": 1173187702930018304, "hi": 131072, "legal": 83, "s5_index": 582153, "membership_class_count": 4},
    {"key_id": "d015", "lo": 1155173304420536320, "hi": 135168, "legal": 91, "s5_index": 585861, "membership_class_count": 4},
    {"key_id": "d016", "lo": 1153062242096250880, "hi": 532480, "legal": 89, "s5_index": 589727, "membership_class_count": 4},
    {"key_id": "d017", "lo": 1153062242096250880, "hi": 17301504, "legal": 89, "s5_index": 593275, "membership_class_count": 4},
    {"key_id": "d018", "lo": 1153062242096250880, "hi": 34360262656, "legal": 88, "s5_index": 596738, "membership_class_count": 4},
    {"key_id": "d019", "lo": 1155173304420536832, "hi": 131072, "legal": 88, "s5_index": 602640, "membership_class_count": 4},
    {"key_id": "d020", "lo": 1155173304421584896, "hi": 131072, "legal": 85, "s5_index": 605690, "membership_class_count": 4},
    {"key_id": "d021", "lo": 1155173441859489792, "hi": 131072, "legal": 73, "s5_index": 605961, "membership_class_count": 4},
    {"key_id": "d022", "lo": 1155173306568019968, "hi": 131072, "legal": 80, "s5_index": 608779, "membership_class_count": 4},
    {"key_id": "d023", "lo": 1155177702467047424, "hi": 131072, "legal": 89, "s5_index": 611801, "membership_class_count": 4},
    {"key_id": "d024", "lo": 1164180503675277312, "hi": 131072, "legal": 91, "s5_index": 614833, "membership_class_count": 4},
    {"key_id": "d025", "lo": 1155173304420536320, "hi": 133120, "legal": 86, "s5_index": 617672, "membership_class_count": 4},
    {"key_id": "d026", "lo": 1153062242096250880, "hi": 540672, "legal": 83, "s5_index": 620742, "membership_class_count": 4},
    {"key_id": "d027", "lo": 1153062242096250880, "hi": 34078720, "legal": 88, "s5_index": 623364, "membership_class_count": 4},
    {"key_id": "d028", "lo": 1155173854176350208, "hi": 131072, "legal": 82, "s5_index": 625189, "membership_class_count": 4},
    {"key_id": "d029", "lo": 1152921642046849024, "hi": 68719477248, "legal": 78, "s5_index": 625899, "membership_class_count": 3},
    {"key_id": "d030", "lo": 1155173304420536576, "hi": 131072, "legal": 89, "s5_index": 630432, "membership_class_count": 4},
    {"key_id": "d031", "lo": 1155175503443791872, "hi": 131072, "legal": 80, "s5_index": 636913, "membership_class_count": 4},
    {"key_id": "d032", "lo": 1155173304420536320, "hi": 132096, "legal": 86, "s5_index": 641189, "membership_class_count": 4},
    {"key_id": "d033", "lo": 1153062242096250880, "hi": 557056, "legal": 85, "s5_index": 643424, "membership_class_count": 4},
    {"key_id": "d034", "lo": 1153062242096250880, "hi": 67633152, "legal": 80, "s5_index": 645317, "membership_class_count": 3},
    {"key_id": "d035", "lo": 1155173304420536448, "hi": 131072, "legal": 90, "s5_index": 650304, "membership_class_count": 4},
    {"key_id": "d036", "lo": 1155173304420798464, "hi": 131072, "legal": 83, "s5_index": 651925, "membership_class_count": 4},
    {"key_id": "d037", "lo": 1155173304957407232, "hi": 131072, "legal": 89, "s5_index": 653505, "membership_class_count": 4},
    {"key_id": "d038", "lo": 1155173304420536320, "hi": 131584, "legal": 81, "s5_index": 655969, "membership_class_count": 4},
    {"key_id": "d039", "lo": 1153062242096250880, "hi": 589824, "legal": 70, "s5_index": 657407, "membership_class_count": 3},
    {"key_id": "d040", "lo": 1155173304420536384, "hi": 131072, "legal": 90, "s5_index": 662182, "membership_class_count": 4},
    {"key_id": "d041", "lo": 1155173304688971776, "hi": 131072, "legal": 85, "s5_index": 664455, "membership_class_count": 4},
    {"key_id": "d042", "lo": 1155173304420569088, "hi": 131072, "legal": 81, "s5_index": 669726, "membership_class_count": 4},
    {"key_id": "d043", "lo": 1155173304420552704, "hi": 131072, "legal": 84, "s5_index": 671112, "membership_class_count": 4},
    {"key_id": "d044", "lo": 1155173304454090752, "hi": 131072, "legal": 85, "s5_index": 671120, "membership_class_count": 4},
    {"key_id": "d045", "lo": 1155173373140013056, "hi": 131072, "legal": 80, "s5_index": 671129, "membership_class_count": 3},
    {"key_id": "d046", "lo": 1155173304420536321, "hi": 131072, "legal": 84, "s5_index": 671133, "membership_class_count": 3},
    {"key_id": "d047", "lo": 1155173304420536322, "hi": 131072, "legal": 82, "s5_index": 671137, "membership_class_count": 4},
    {"key_id": "d048", "lo": 1155173304420536324, "hi": 131072, "legal": 85, "s5_index": 671143, "membership_class_count": 4},
    {"key_id": "d049", "lo": 1155173304437313536, "hi": 131072, "legal": 86, "s5_index": 671146, "membership_class_count": 3},
]

SCHEMA = "n11-centralreply-closure-batch36-keys-v1"


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
    b3 = os.path.join(src, "batch3-packet")
    cache_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(src, "canonical-cache-23d40e36.cache")
    quarantine_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(src, "quarantine.json")
    refresh_path = sys.argv[3] if len(sys.argv) > 3 else os.path.join(src, "refresh-summary.json")
    closure_path = sys.argv[4] if len(sys.argv) > 4 else os.path.join(src, "closure-classes.csv")
    worklist_path = sys.argv[5] if len(sys.argv) > 5 else os.path.join(src, "worklist-class20421-extract.csv")
    b3_keys_path = sys.argv[6] if len(sys.argv) > 6 else os.path.join(b3, "batch-keys.json")
    b3_status_path = sys.argv[7] if len(sys.argv) > 7 else os.path.join(b3, "status.log")

    # G1 source pins
    for path, pin, what in [
        (b3_keys_path, PIN_B3_KEYS, "batch-3 batch-keys"),
        (b3_status_path, PIN_B3_STATUS, "batch-3 status.log"),
        (refresh_path, PIN_REFRESH_SUMMARY, "refresh-summary"),
        (closure_path, PIN_CLOSURE_CLASSES, "closure-classes"),
        (cache_path, PIN_CANONICAL_CACHE, "canonical cache"),
        (quarantine_path, PIN_QUARANTINE, "quarantine"),
        (worklist_path, PIN_WORKLIST_EXTRACT, "worklist class-20421 extract"),
    ]:
        if sha256_file(path) != pin:
            fail("G1 pin mismatch on %s (%s)" % (what, path))

    # G2 batch-3 packet integrity
    with open(b3_keys_path, "r", encoding="utf-8") as f:
        packet = json.load(f)
    keys = packet.get("keys", [])
    if len(keys) != 49:
        fail("G2 batch-3 packet has %d keys, want 49" % len(keys))
    ids = [k.get("key_id") for k in keys]
    want_ids = ["d%03d" % i for i in range(1, 50)]
    if ids != want_ids:
        fail("G2 batch-3 packet id set drift")
    pkt = {k["key_id"]: k for k in keys}
    for t in EMBEDDED_PROBED + EMBEDDED_TARGETS:
        row = pkt[t["key_id"]]
        for field in ("lo", "hi", "legal", "s5_index", "membership_class_count"):
            if row.get(field) != t[field]:
                fail("G2 embedded row %s field %s drift: packet %r embedded %r"
                     % (t["key_id"], field, row.get(field), t[field]))

    pass_re = re.compile(r"^\S+ (d\d{3}) PASS (\d+),(\d+),(\d+)$")
    halt_re = re.compile(r"^\S+ (d\d{3}) WIN-HALT$")
    pass_rows = {}
    halt_rows = []
    with open(b3_status_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            m = pass_re.match(line)
            if m:
                if m.group(1) in pass_rows:
                    fail("G2 batch-3 status.log duplicate PASS row for %s" % m.group(1))
                pass_rows[m.group(1)] = (int(m.group(2)), int(m.group(3)), int(m.group(4)))
                continue
            m = halt_re.match(line)
            if m:
                halt_rows.append(m.group(1))
    if len(pass_rows) != 4:
        fail("G2 batch-3 status.log PASS rows = %d, want 4" % len(pass_rows))
    if halt_rows != ["d002"]:
        fail("G2 batch-3 status.log WIN-HALT rows drift: %r" % (halt_rows,))
    if sorted(pass_rows) != ["d001", "d002", "d003", "d004"]:
        fail("G2 batch-3 status.log PASS id set drift: %r" % sorted(pass_rows))
    for kid, want in PROBED_LABELS.items():
        got = pass_rows.get(kid)
        if got is None:
            fail("G2 batch-3 status.log missing PASS row %s" % kid)
        if got[0] != 15000000:
            fail("G2 batch-3 status.log budget drift on %s" % kid)
        if got[1] != want:
            fail("G2 batch-3 status.log result drift on %s: %d want %d" % (kid, got[1], want))
        if got[2] != PROBED_NODES[kid]:
            fail("G2 batch-3 status.log nodes drift on %s: %d want %d" % (kid, got[2], PROBED_NODES[kid]))
    loss_ids = sorted(k for k, v in pass_rows.items() if v[1] == 2)
    win_ids = sorted(k for k, v in pass_rows.items() if v[1] == 1)
    if loss_ids != ["d001", "d003", "d004"] or win_ids != ["d002"]:
        fail("G2 batch-3 status.log LOSS/WIN key sets drift: %r %r" % (loss_ids, win_ids))
    probed_ids = set(pass_rows)
    clean_ids = [k["key_id"] for k in keys if k["key_id"] not in probed_ids]
    want_clean = ["d%03d" % i for i in range(5, 50)]
    if clean_ids != want_clean:
        fail("G2 clean set drift: %r" % (clean_ids,))
    if sorted(k["key_id"] for k in EMBEDDED_PROBED) != sorted(probed_ids):
        fail("G2 embedded probed set drift")
    if sorted(k["key_id"] for k in EMBEDDED_TARGETS) != want_clean:
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
    if CLASS_UNKNOWN_NOW != len(EMBEDDED_PROBED) + len(EMBEDDED_TARGETS):
        fail("G3 accounting: %d != %d (probed) + %d (clean)"
             % (CLASS_UNKNOWN_NOW, len(EMBEDDED_PROBED), len(EMBEDDED_TARGETS)))

    # G4 exact-pair absence in canonical cache (+ same-lo context)
    all_rows = EMBEDDED_TARGETS + EMBEDDED_PROBED
    wanted = {t["key_id"]: (t["lo"], t["hi"]) for t in all_rows}
    wanted_pairs = set(wanted.values())
    present = {}
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
                elif lo in same_lo:
                    same_lo[lo] += 1
    if present:
        fail("G4 canonical cache already contains key(s): %r" % sorted(present))

    # G5 quarantine absence
    with open(quarantine_path, "r", encoding="utf-8") as f:
        q = json.load(f)
    active_keys = {tuple(e["key"]) for e in q.get("entries", []) if e.get("active")}
    for t in EMBEDDED_TARGETS:
        if (t["lo"], t["hi"]) in active_keys:
            fail("G5 key %s is quarantined" % t["key_id"])

    # G6 worklist class-20421 extract cross-check (probe_order 77..125)
    with open(worklist_path, "r", encoding="utf-8") as f:
        wl = [line.rstrip("\n").split(",") for line in f if line.strip()]
    wl_header = wl[0]
    if wl_header[:2] != ["probe_order", "s5_index"]:
        fail("G6 worklist extract header drift")
    wl_rows = wl[1:]
    if len(wl_rows) != 49:
        fail("G6 worklist extract rows = %d, want 49" % len(wl_rows))
    orders = []
    for r in wl_rows:
        orders.append(int(r[0]))
    if orders != list(range(WORKLIST_ORDER_FIRST, WORKLIST_ORDER_FIRST + 49)):
        fail("G6 worklist extract probe_order not contiguous 77..125: %r" % (orders[:5],))
    worklist_order_map = {}
    for r in wl_rows:
        (po, s5, lo, hi, legal, scl, cun, cf, ct, mcc) = r
        if int(scl) != CLASS_INDEX:
            fail("G6 worklist extract serving_class drift: %s" % scl)
        if int(cun) != CLASS_UNKNOWN_NOW:
            fail("G6 worklist extract class_unknown_now drift")
        kid = None
        for t in all_rows:
            if t["lo"] == int(lo) and t["hi"] == int(hi):
                kid = t["key_id"]
                break
        if kid is None:
            fail("G6 worklist row (%s,%s) not in packet" % (lo, hi))
        worklist_order_map[kid] = int(po)
        emb = {t["key_id"]: t for t in all_rows}[kid]
        if int(s5) != emb["s5_index"] or int(legal) != emb["legal"]:
            fail("G6 worklist row %s s5/legal drift" % kid)
        if int(mcc) != emb["membership_class_count"]:
            fail("G6 worklist row %s membership drift" % kid)
    if len(worklist_order_map) != 49:
        fail("G6 worklist extract does not cover all 49 packet keys")
    prev = -1
    for i, kid in enumerate(ids):
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
        "batch": "batch-36",
        "description": "n11 central-reply closure batch-36: clean (never-probed) 45 unknown cost-children of closure class 20421 (rank 9), derived from the published batch-3 packet (49 keys, 4 probed honest-labeled unconsumed), post-b35loss26 reaudit",
        "target_key_count": len(EMBEDDED_TARGETS),
        "probed_unconsumed_same_class": [
            {"key_id": t["key_id"], "budget_result_nodes": "15000000,%d,%d" % (PROBED_LABELS[t["key_id"]], PROBED_NODES[t["key_id"]]),
             "probe_order": worklist_order_map[t["key_id"]],
             "note": "batch-3 (2026-11-22) 2-pass node-exact; verdict not consumed into the canonical chain; unconsumed-WIN d002 requires the scrutiny-owner C++ gate"}
            for t in EMBEDDED_PROBED
        ],
        "keys": [
            {
                "key_id": t["key_id"],
                "probe_order": worklist_order_map[t["key_id"]],
                "batch3_key_id": t["key_id"],
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
            "batch3_batch_keys": PIN_B3_KEYS,
            "batch3_status": PIN_B3_STATUS,
            "refresh_summary": PIN_REFRESH_SUMMARY,
            "closure_classes": PIN_CLOSURE_CLASSES,
            "canonical_cache": PIN_CANONICAL_CACHE,
            "quarantine": PIN_QUARANTINE,
            "worklist_class20421_extract": PIN_WORKLIST_EXTRACT,
            "jsreplay": "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
            "runbatch": "f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84",
        },
        "gates": ["G1-source-sha-pins", "G2-batch3-packet-integrity",
                  "G3-closure-rank-anchor-and-accounting",
                  "G4-exact-pair-absent-in-canonical-cache",
                  "G5-not-quarantined", "G6-worklist-extract-field-match"],
        "canonical_cache_s5verdict_rows": n_rows,
        "consumed_into_canonical_cache": False,
    }
    tmp = os.path.join(input_dir, "batch-keys-b36.json.tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(keys_doc, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, os.path.join(input_dir, "batch-keys-b36.json"))

    print("make_batch36_keys: ALL GATES PASS, wrote 45 inputs + batch-keys-b36.json")


if __name__ == "__main__":
    main()
