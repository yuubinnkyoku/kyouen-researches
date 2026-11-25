#!/usr/bin/env python3
"""make_batch34_keys.py - batch-34 (n11 central-reply closure small-pockets) key
derivation with fail-closed gates.

Scope: the two last unknown cost-children of closure classes 23101 (class_rank 1)
and 1849 (class_rank 2) in the published post-b33loss45-adoption reaudit
(refresh-summary.json sha256 38fc4e19..., closure-classes.csv 6cc33dd7...).

Targets (embedded from the published refresh-summary.json worklist_first entries
probe_order 1 and 2; verified against the fetched published file at run time,
never hand-trcribed into the outputs):

  ag001: serving_class 23101, lo=1152921505747697664, hi=1032,
         legal=85, s5_index=745184, membership_class_count=4
  ag002: serving_class 1849, lo=1153485622925590528, hi=0,
         legal=88, s5_index=81011, membership_class_count=3

Gates (all fail-closed, rc=1 on any violation, no partial outputs on failure):
  G1  source sha pins: refresh-summary / closure-classes / canonical cache /
      quarantine registry must match the published sha256 values byte-exactly.
  G2  worklist_first[0] and [1] must match the embedded target table on every
      derived field (probe_order, serving_class, lo, hi, legal, s5_index,
      class_unknown_now, membership_class_count, class_mask).
  G3  closure-classes.csv rank 1 == class 23101 unknown_now 1 and
      rank 2 == class 1849 unknown_now 1 (both rows byte-parsed).
  G4  exact key pairs (lo,hi) absent from the canonical merged chain cache
      (pair-level parse of all s5verdict rows; same-lo rows are counted and
      reported as context, never adopted).
  G5  neither key appears in the active quarantine registry entries.
  G6  input CSV legal field == worklist_first legal field (no hand re-typing;
      the jsreplay solver independently re-derives legal at run time and
      hard-fails on mismatch).

Outputs (written atomically only after all gates pass):
  input/ag001.input.csv, input/ag002.input.csv
      (format: target,0,5,lo,hi,legal,0,0,0,0,0 - identical schema to the
       published batch-33 inputs; field 2 = replay id, f[2]=stones, f[3]=lo,
       f[4]=hi, f[5]=legal, trailing zeros unused by the replica driver)
  input/batch-keys-b34.json
      schema n11-centralreply-closure-batch34-keys-v1, pins included,
      consumed_into_canonical_cache=false

Determinism: pure function of the pinned inputs; run 3x byte-identical in the
completion protocol. Tamper battery (scratch copies) must ABORT on: pin drift,
worklist field drift, cache hit, quarantine hit, closure-table rank drift.
"""
import hashlib
import json
import os
import sys

PIN_REFRESH_SUMMARY = "38fc4e193cf08cf4efb7830a8bad3d2245bc732380f44c4ee2913e05d5644732"
PIN_CLOSURE_CLASSES = "6cc33dd731c5d2237291552a91c3f7d60947bba875867fcab10394b533f1a68d"
PIN_CANONICAL_CACHE = "973bcd19309eae1d73b26c40c3d6839a2f35baa74658e0794f19da6f9412ca5b"
PIN_QUARANTINE = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

EMBEDDED_TARGETS = [
    {
        "key_id": "ag001",
        "probe_order": 1,
        "serving_class": 23101,
        "class_mask": [1152921504892059648, 16],
        "class_unknown_now": 1,
        "lo": 1152921505747697664,
        "hi": 1032,
        "legal": 85,
        "s5_index": 745184,
        "membership_class_count": 4,
    },
    {
        "key_id": "ag002",
        "probe_order": 2,
        "serving_class": 1849,
        "class_mask": [1152922672972169216, 0],
        "class_unknown_now": 1,
        "lo": 1153485622925590528,
        "hi": 0,
        "legal": 88,
        "s5_index": 81011,
        "membership_class_count": 3,
    },
]

SCHEMA = "n11-centralreply-closure-batch34-keys-v1"


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
    cache_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(kit_root, "..", "canonical.cache")
    quarantine_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(kit_root, "..", "quarantine.json")
    refresh_path = sys.argv[3] if len(sys.argv) > 3 else os.path.join(kit_root, "..", "sources", "refresh-summary.json")
    closure_path = sys.argv[4] if len(sys.argv) > 4 else os.path.join(kit_root, "..", "sources", "closure-classes.csv")

    # G1 source pins
    for path, pin, what in [
        (refresh_path, PIN_REFRESH_SUMMARY, "refresh-summary"),
        (closure_path, PIN_CLOSURE_CLASSES, "closure-classes"),
        (cache_path, PIN_CANONICAL_CACHE, "canonical cache"),
        (quarantine_path, PIN_QUARANTINE, "quarantine"),
    ]:
        if sha256_file(path) != pin:
            fail("G1 pin mismatch on %s (%s)" % (what, path))

    # G2 worklist_first match
    with open(refresh_path, "r", encoding="utf-8") as f:
        rs = json.load(f)
    wl = rs.get("worklist_first", [])
    if len(wl) < 2:
        fail("G2 worklist_first too short")
    for emb, entry in zip(EMBEDDED_TARGETS, wl[:2]):
        checks = [
            ("probe_order", emb["probe_order"]),
            ("serving_class", emb["serving_class"]),
            ("class_unknown_now", emb["class_unknown_now"]),
            ("lo", emb["lo"]),
            ("hi", emb["hi"]),
            ("legal", emb["legal"]),
            ("s5_index", emb["s5_index"]),
            ("membership_class_count", emb["membership_class_count"]),
            ("class_mask", emb["class_mask"]),
        ]
        for field, want in checks:
            if entry.get(field) != want:
                fail("G2 worklist_first mismatch %s: got %r want %r" % (field, entry.get(field), want))

    # G3 closure-classes rank anchors
    with open(closure_path, "r", encoding="utf-8") as f:
        rows = [line.rstrip("\n").split(",") for line in f if line.strip()]
    header = rows[0]
    if header[:2] != ["class_rank", "class_index"]:
        fail("G3 closure-classes header drift")
    by_rank = {r[0]: r for r in rows[1:]}
    if by_rank.get("1", [None] * 5)[1] != "23101" or by_rank["1"][4] != "1":
        fail("G3 rank1 is not class 23101 unknown_now 1")
    if by_rank.get("2", [None] * 5)[1] != "1849" or by_rank["2"][4] != "1":
        fail("G3 rank2 is not class 1849 unknown_now 1")

    # G4 exact-pair absence in canonical cache
    wanted_pairs = {(t["lo"], t["hi"]) for t in EMBEDDED_TARGETS}
    present = {}
    same_lo = {t["lo"]: 0 for t in EMBEDDED_TARGETS}
    with open(cache_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("s5verdict,"):
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
        "batch": "batch-34",
        "description": "n11 central-reply closure small-pocket batch: last unknown cost-children of closure classes 23101 (rank 1) and 1849 (rank 2), post-b33loss45 reaudit",
        "keys": [
            {
                "key_id": t["key_id"],
                "probe_order": t["probe_order"],
                "serving_class": t["serving_class"],
                "class_mask": t["class_mask"],
                "class_unknown_now_at_selection": t["class_unknown_now"],
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
            "refresh_summary": PIN_REFRESH_SUMMARY,
            "closure_classes": PIN_CLOSURE_CLASSES,
            "canonical_cache": PIN_CANONICAL_CACHE,
            "quarantine": PIN_QUARANTINE,
        },
        "gates": ["G1-source-sha-pins", "G2-worklist-first-field-match",
                  "G3-closure-rank-anchors", "G4-exact-pair-absent-in-canonical-cache",
                  "G5-not-quarantined", "G6-legal-from-worklist"],
        "consumed_into_canonical_cache": False,
    }
    tmp = os.path.join(input_dir, "batch-keys-b34.json.tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(keys_doc, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, os.path.join(input_dir, "batch-keys-b34.json"))

    print("make_batch34_keys: ALL GATES PASS, wrote 2 inputs + batch-keys-b34.json")


if __name__ == "__main__":
    main()
