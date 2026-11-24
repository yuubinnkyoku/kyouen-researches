#!/usr/bin/env python3
"""make_batch35_keys.py - batch-35 (n11 central-reply closure class 16757)
key derivation with fail-closed gates.

Scope: the 28 clean (never-probed, honest-label-free) unknown cost-children
of closure class 16757 (class_rank 7, mask [1153204079095185408, 65536]) in the
published post-b33loss45-adoption reaudit (refresh-summary.json 38fc4e19...,
closure-classes.csv 6cc33dd7..., canonical cache 973bcd19...).

Key set provenance (no hand transcription): the published batch-1 packet
(research/experiments/n11-centralreply-closure-class16757-batch-20261122)
probed b001-b020 on 2026-11-22 (19 LOSS + b018 WIN-HALT, pre-registered) and
recorded not_probed_unknown == {b021..b048}. This batch-35 maker derives the
28 clean keys from that published packet, cross-checks the probeable subset
(b021..b032) against the published refresh-summary worklist_first entries
probe_order 29..40 (order 28 is b018, the unconsumed WIN, excluded here),
and asserts the accounting 29 unknown_now == 1 (b018 unconsumed) + 28 clean.

Gates (all fail-closed, rc=1 on any violation, no partial outputs on failure):
  G1  source sha pins: batch-1 packet (3 files) + refresh-summary + closure
      classes + canonical cache + quarantine must match the published
      sha256 values byte-exactly.
  G2  batch-1 packet integrity: 48 keys with ids b001..b048; audit
      not_probed_unknown == {b021..b048} exactly; status.log has exactly 20
      PASS rows (19 LOSS result 2 + b018 result 1) and one b018 WIN-HALT row;
      every embedded target matches the packet row (lo, hi, legal, s5_index,
      membership_class_count)
  G3  closure-classes.csv rank 7 == class 16757 with unknown_now 29, and
      29 == 1 (b018 unconsumed) + 28 (clean) accounting
  G4  exact key pairs (lo,hi) of the 28 targets and of b018 absent from the
      canonical merged chain cache (pair-level parse of all s5verdict rows;
      same-lo rows are counted and reported as context, never adopted)
  G5  none of the 28 keys appears in the active quarantine registry entries
  G6  worklist_first class-16757 entries: exactly 13 (probe_order 28..40);
      order 28 == b018 and orders 29..40 == b021..b032 on every field
      (probe_order, serving_class, class_unknown_now, lo, hi, legal,
      s5_index, membership_class_count, class_mask); legal agrees with the
      batch-1 packet (no hand re-typing; the jsreplay solver independently
      re-derives legal at run time and hard-fails on mismatch)

Outputs (written atomically only after all gates pass):
  input/b021.input.csv ... input/b048.input.csv
      (format: target,0,5,lo,hi,legal,0,0,0,0,0 - identical schema to the
       published batch-33/34 inputs)
  input/batch-keys-b35.json
      schema n11-centralreply-closure-batch35-keys-v1, pins included,
      consumed_into_canonical_cache=false

Determinism: pure function of the pinned inputs; run 3x byte-identical in
the completion protocol. Tamper battery (scratch copies) must ABORT on: pin
drift, packet field drift, not_probed drift, cache hit (with re-pinned
sources), quarantine hit, closure-table rank drift, worklist field drift.
"""
import hashlib
import json
import os
import re
import sys

PIN_BATCH1_KEYS = "2aaccc941d7aec35c416b27d5cdd10f7fbb82c9801bcf560b61e20be88c331f8"
PIN_BATCH1_STATUS = "559a0884d4c728c05a992bcf144661fbd8212bc09d2c8b56341aebe7b94348b1"
PIN_BATCH1_AUDIT = "9929bd9f83a1774f00a3791a340b6084a3109b565f482556c7d1f90f88b68abd"
PIN_REFRESH_SUMMARY = "38fc4e193cf08cf4efb7830a8bad3d2245bc732380f44c4ee2913e05d5644732"
PIN_CLOSURE_CLASSES = "6cc33dd731c5d2237291552a91c3f7d60947bba875867fcab10394b533f1a68d"
PIN_CANONICAL_CACHE = "973bcd19309eae1d73b26c40c3d6839a2f35baa74658e0794f19da6f9412ca5b"
PIN_QUARANTINE = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

CLASS_INDEX = 16757
CLASS_MASK = [1153204079095185408, 65536]
CLASS_RANK = 7
CLASS_UNKNOWN_NOW = 29

# b018: the already-probed unconsumed WIN row of class 16757 (batch-1, WIN-HALT
# 2026-11-22T02:39:43Z). It is NOT a batch-35 target; it is gate-checked for
# bookkeeping consistency (unknown accounting + cache absence + worklist order
# 28 + legal cross-check).
B018 = {
    "key_id": "b018",
    "lo": 1153204079095189504,
    "hi": 65536,
    "legal": 60,
    "s5_index": 528497,
    "membership_class_count": 3,
}

# the 28 clean targets, embedded from the published batch-1 packet rows
# (verified against the pinned published file at run time).
EMBEDDED_TARGETS = [
    {"key_id": "b021", "lo": 1153204079095218176, "hi": 65536, "legal": 83, "s5_index": 535179, "membership_class_count": 4},
    {"key_id": "b022", "lo": 1153204079095316480, "hi": 65536, "legal": 79, "s5_index": 537545, "membership_class_count": 4},
    {"key_id": "b023", "lo": 1153204079095447552, "hi": 65536, "legal": 76, "s5_index": 539592, "membership_class_count": 4},
    {"key_id": "b024", "lo": 1153204079095709696, "hi": 65536, "legal": 83, "s5_index": 541610, "membership_class_count": 4},
    {"key_id": "b025", "lo": 1153204079097282560, "hi": 65536, "legal": 87, "s5_index": 545364, "membership_class_count": 4},
    {"key_id": "b026", "lo": 1153204079111962624, "hi": 65536, "legal": 72, "s5_index": 546902, "membership_class_count": 3},
    {"key_id": "b027", "lo": 1153204079128739840, "hi": 65536, "legal": 75, "s5_index": 548070, "membership_class_count": 4},
    {"key_id": "b028", "lo": 1153204079162294272, "hi": 65536, "legal": 83, "s5_index": 549153, "membership_class_count": 4},
    {"key_id": "b029", "lo": 1153204079632056320, "hi": 65536, "legal": 81, "s5_index": 551777, "membership_class_count": 4},
    {"key_id": "b030", "lo": 1153204081242669056, "hi": 65536, "legal": 87, "s5_index": 554104, "membership_class_count": 4},
    {"key_id": "b031", "lo": 1153204083390152704, "hi": 65536, "legal": 86, "s5_index": 555161, "membership_class_count": 4},
    {"key_id": "b032", "lo": 1153204147814662144, "hi": 65536, "legal": 72, "s5_index": 556117, "membership_class_count": 3},
    {"key_id": "b033", "lo": 1153206278118440960, "hi": 65536, "legal": 83, "s5_index": 558018, "membership_class_count": 4},
    {"key_id": "b034", "lo": 1153208477141696512, "hi": 65536, "legal": 84, "s5_index": 558054, "membership_class_count": 4},
    {"key_id": "b035", "lo": 1153212875188207616, "hi": 65536, "legal": 83, "s5_index": 558079, "membership_class_count": 4},
    {"key_id": "b036", "lo": 1171218477604667392, "hi": 65536, "legal": 84, "s5_index": 558120, "membership_class_count": 4},
    {"key_id": "b037", "lo": 1157707678722555904, "hi": 65536, "legal": 72, "s5_index": 558183, "membership_class_count": 4},
    {"key_id": "b038", "lo": 1152922604118507520, "hi": 65792, "legal": 86, "s5_index": 558228, "membership_class_count": 4},
    {"key_id": "b039", "lo": 1152922604185583616, "hi": 65792, "legal": 82, "s5_index": 558261, "membership_class_count": 4},
    {"key_id": "b040", "lo": 1152922741557428224, "hi": 65792, "legal": 81, "s5_index": 558283, "membership_class_count": 4},
    {"key_id": "b041", "lo": 1152922604118474756, "hi": 65792, "legal": 88, "s5_index": 558334, "membership_class_count": 4},
    {"key_id": "b042", "lo": 1152922604118474754, "hi": 65792, "legal": 88, "s5_index": 558367, "membership_class_count": 4},
    {"key_id": "b043", "lo": 1152922604118474753, "hi": 65792, "legal": 78, "s5_index": 558393, "membership_class_count": 3},
    {"key_id": "b044", "lo": 1152922604118491136, "hi": 65792, "legal": 80, "s5_index": 558410, "membership_class_count": 4},
    {"key_id": "b045", "lo": 1152922604118482944, "hi": 65792, "legal": 87, "s5_index": 558443, "membership_class_count": 4},
    {"key_id": "b046", "lo": 1152922604152029184, "hi": 65792, "legal": 81, "s5_index": 558486, "membership_class_count": 4},
    {"key_id": "b047", "lo": 1152922604135251968, "hi": 65792, "legal": 74, "s5_index": 558506, "membership_class_count": 3},
    {"key_id": "b048", "lo": 1152922672837951488, "hi": 65792, "legal": 72, "s5_index": 558553, "membership_class_count": 3},
]

# probe_order anchors in the published refresh-summary worklist_first
# (order 28 == b018 unconsumed WIN; orders 29..40 == b021..b032).
WORKLIST_ORDER_MAP = {28: "b018"}
_order = 29
for _t in EMBEDDED_TARGETS[:12]:
    WORKLIST_ORDER_MAP[_order] = _t["key_id"]
    _order += 1

SCHEMA = "n11-centralreply-closure-batch35-keys-v1"


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
    cache_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(src, "canonical-cache-973bcd19.cache")
    quarantine_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(src, "quarantine.json")
    refresh_path = sys.argv[3] if len(sys.argv) > 3 else os.path.join(src, "refresh-summary.json")
    closure_path = sys.argv[4] if len(sys.argv) > 4 else os.path.join(src, "closure-classes.csv")
    b1_keys_path = sys.argv[5] if len(sys.argv) > 5 else os.path.join(b1, "batch-keys.json")
    b1_status_path = sys.argv[6] if len(sys.argv) > 6 else os.path.join(b1, "status.log")
    b1_audit_path = sys.argv[7] if len(sys.argv) > 7 else os.path.join(b1, "batch-audit.json")

    # G1 source pins
    for path, pin, what in [
        (b1_keys_path, PIN_BATCH1_KEYS, "batch-1 batch-keys"),
        (b1_status_path, PIN_BATCH1_STATUS, "batch-1 status.log"),
        (b1_audit_path, PIN_BATCH1_AUDIT, "batch-1 batch-audit"),
        (refresh_path, PIN_REFRESH_SUMMARY, "refresh-summary"),
        (closure_path, PIN_CLOSURE_CLASSES, "closure-classes"),
        (cache_path, PIN_CANONICAL_CACHE, "canonical cache"),
        (quarantine_path, PIN_QUARANTINE, "quarantine"),
    ]:
        if sha256_file(path) != pin:
            fail("G1 pin mismatch on %s (%s)" % (what, path))

    # G2 batch-1 packet integrity
    with open(b1_keys_path, "r", encoding="utf-8") as f:
        packet = json.load(f)
    keys = packet.get("keys", [])
    if len(keys) != 48:
        fail("G2 batch-1 packet has %d keys, want 48" % len(keys))
    ids = [k.get("key_id") for k in keys]
    want_ids = ["b%03d" % i for i in range(1, 49)]
    if ids != want_ids:
        fail("G2 batch-1 packet id set drift")
    pkt = {k["key_id"]: k for k in keys}
    for t in EMBEDDED_TARGETS + [B018]:
        row = pkt[t["key_id"]]
        for field in ("lo", "hi", "legal", "s5_index", "membership_class_count"):
            if row.get(field) != t[field]:
                fail("G2 embedded target %s field %s drift: packet %r embedded %r"
                     % (t["key_id"], field, row.get(field), t[field]))

    with open(b1_audit_path, "r", encoding="utf-8") as f:
        audit = json.load(f)
    npu = audit.get("not_probed_unknown", [])
    want_npu = ["b%03d" % i for i in range(21, 49)]
    if sorted(npu) != want_npu:
        fail("G2 batch-1 audit not_probed_unknown drift: %r" % (npu,))
    if [w.get("key_id") for w in audit.get("win_keys", [])] != ["b018"]:
        fail("G2 batch-1 audit win_keys drift")

    pass_re = re.compile(r"^\S+ (b\d{3}) PASS (\d+),(\d+),(\d+)$")
    halt_re = re.compile(r"^\S+ (b\d{3}) WIN-HALT$")
    pass_rows = {}
    halt_rows = []
    with open(b1_status_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            m = pass_re.match(line)
            if m:
                pass_rows[m.group(1)] = (int(m.group(2)), int(m.group(3)), int(m.group(4)))
                continue
            m = halt_re.match(line)
            if m:
                halt_rows.append(m.group(1))
    if len(pass_rows) != 20:
        fail("G2 batch-1 status.log PASS rows = %d, want 20" % len(pass_rows))
    if halt_rows != ["b018"]:
        fail("G2 batch-1 status.log WIN-HALT rows drift: %r" % (halt_rows,))
    loss_ids = sorted(k for k, v in pass_rows.items() if v[1] == 2)
    win_ids = sorted(k for k, v in pass_rows.items() if v[1] == 1)
    if loss_ids != ["b%03d" % i for i in list(range(1, 18)) + [19, 20]]:
        fail("G2 batch-1 status.log LOSS key set drift: %r" % (loss_ids,))
    if win_ids != ["b018"]:
        fail("G2 batch-1 status.log WIN key set drift: %r" % (win_ids,))
    if any(v[0] != 15000000 for v in pass_rows.values()):
        fail("G2 batch-1 status.log budget drift")

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
    if CLASS_UNKNOWN_NOW != 1 + len(EMBEDDED_TARGETS):
        fail("G3 accounting: 29 != 1 (b018) + 28 (clean)")

    # G4 exact-pair absence in canonical cache (+ same-lo context)
    wanted = {t["key_id"]: (t["lo"], t["hi"]) for t in EMBEDDED_TARGETS}
    wanted["b018"] = (B018["lo"], B018["hi"])
    wanted_pairs = set(wanted.values())
    present = {}
    same_lo = {t["lo"]: 0 for t in EMBEDDED_TARGETS + [B018]}
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

    # G6 worklist_first cross-check (class 16757 block: probe_order 28..40)
    with open(refresh_path, "r", encoding="utf-8") as f:
        rs = json.load(f)
    wl = rs.get("worklist_first", [])
    wl_16757 = [e for e in wl if e.get("serving_class") == CLASS_INDEX]
    if len(wl_16757) != 13:
        fail("G6 worklist_first class-16757 entries = %d, want 13 (orders 28..40)" % len(wl_16757))
    emb_all = {t["key_id"]: t for t in EMBEDDED_TARGETS + [B018]}
    for i, order in enumerate(range(28, 41)):
        entry = wl_16757[i]
        if entry.get("probe_order") != order:
            fail("G6 worklist class-16757 order drift at index %d: %r" % (i, entry.get("probe_order")))
        kid = WORKLIST_ORDER_MAP[order]
        emb = emb_all[kid]
        checks = [
            ("serving_class", CLASS_INDEX),
            ("class_unknown_now", CLASS_UNKNOWN_NOW),
            ("lo", emb["lo"]),
            ("hi", emb["hi"]),
            ("legal", emb["legal"]),
            ("s5_index", emb["s5_index"]),
            ("membership_class_count", emb["membership_class_count"]),
            ("class_mask", CLASS_MASK),
        ]
        for field, want in checks:
            if entry.get(field) != want:
                fail("G6 worklist probe_order %d (%s) field %s: got %r want %r"
                     % (order, kid, field, entry.get(field), want))

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
        "batch": "batch-35",
        "description": "n11 central-reply closure batch-35: clean (never-probed) 28 unknown cost-children of closure class 16757 (rank 7), derived from the published batch-1 packet not_probed set, post-b33loss45 reaudit",
        "target_key_count": len(EMBEDDED_TARGETS),
        "excluded_unconsumed_win": {
            "key_id": "b018",
            "probe_order": 28,
            "note": "batch-1 (2026-11-22) 2-pass node-exact WIN 15000000,1,3549602, verdict not consumed, scrutiny owner C++ gate pending",
        },
        "keys": [
            {
                "key_id": t["key_id"],
                "probe_order": WORKLIST_ORDER_MAP.get(
                    (29 + EMBEDDED_TARGETS.index(t)), None),
                "batch1_key_id": t["key_id"],
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
            "batch1_batch_keys": PIN_BATCH1_KEYS,
            "batch1_status": PIN_BATCH1_STATUS,
            "batch1_audit": PIN_BATCH1_AUDIT,
            "refresh_summary": PIN_REFRESH_SUMMARY,
            "closure_classes": PIN_CLOSURE_CLASSES,
            "canonical_cache": PIN_CANONICAL_CACHE,
            "quarantine": PIN_QUARANTINE,
            "jsreplay": "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
            "runbatch": "f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84",
        },
        "gates": ["G1-source-sha-pins", "G2-batch1-packet-integrity",
                  "G3-closure-rank-anchor-and-accounting",
                  "G4-exact-pair-absent-in-canonical-cache",
                  "G5-not-quarantined", "G6-worklist-first-field-match"],
        "canonical_cache_s5verdict_rows": n_rows,
        "consumed_into_canonical_cache": False,
    }
    # fix probe_order fields for keys beyond worklist_first (orders 41..56 are
    # not published; the field stays null for b033..b048, honestly)
    tmp = os.path.join(input_dir, "batch-keys-b35.json.tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(keys_doc, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, os.path.join(input_dir, "batch-keys-b35.json"))

    print("make_batch35_keys: ALL GATES PASS, wrote 28 inputs + batch-keys-b35.json")


if __name__ == "__main__":
    main()
