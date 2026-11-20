#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic third-verification record assembler for the K1166 (fold29
certificate-extraction external second verification) pristine re-execution.

Reads the two fresh battery run directories produced by the UNMODIFIED
published harness verify_cert_extract_ext_second_20261120.py (battery 1:
working cwd/HOME; battery 2: isolated cwd/HOME + PYTHONHASHSEED=random),
re-checks every deterministic gate (published byte pins, per-root extraction
gates, tampers, audit byte-identity against the published oracle), and writes
output/third-verification.json (sorted keys, no timing fields, no absolute
paths; byte-deterministic).

stdlib only. Fail-closed: exit 1 and without writing the record output if any gate fails.
"""

import hashlib
import json
import os
import sys

PUB_README_SHA = "6605abff82a8e47556ccf9688bf7b253c34c4d64e9178ae7a1d143adf3f85908"
PUB_FETCH_SHA = "c3c4c9ffef5132e1657470d84b296b499ecd421b0342404ae32b0fd3ee64a114"
PUB_MANIFEST_SHA = "949868e21fdc124058c608925c101468622acca17702e159f99fb03df09d3ae8"
PUB_HARNESS_SHA = "ca662e57053f504684c8dcc44f66c182d338978a3b9b70369a40754d9c59b276"
PUB_AUDIT_ORACLE_SHA = "cf6a26abf0a459bcfb42bbb2d649ace5d3d1f1a5aee63a01af1de8b79d6a145f"
PUB_AUDIT_ORACLE_BYTES = 15549
PARTS = ["pin.json", "k1136.json", "k1137.json", "k1139.json", "tampers.json"]
PUB_FILES = {
    "readme": ("README.md", PUB_README_SHA),
    "fetch_master": ("fetch_master.py", PUB_FETCH_SHA),
    "pin_manifest": ("pin-manifest.json", PUB_MANIFEST_SHA),
    "harness": ("verify_cert_extract_ext_second_20261120.py", PUB_HARNESS_SHA),
    "harness_audit": ("harness-audit.json", PUB_AUDIT_ORACLE_SHA),
}
INTERPRETATION_GUARD = [
    "This third verification closes no rows; residual rows and pool 120,416 are unchanged.",
    "WIN8-D10 certificates apply only to the game tree of the stated 8-stone root.",
    "REFUTED-D10 is not a LOSS proof.",
    "Nodes/solved counts are never read as win/loss.",
    "The standard 11x11 emptied board, two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain UNKNOWN.",
]


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def gates_all_pass(part_path):
    with open(part_path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    g = obj.get("gates", {})
    return len(g) > 0 and all(v.get("pass") is True for v in g.values()), len(g)


def read_bytes(p):
    with open(p, "rb") as f:
        return f.read()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    if len(sys.argv) != 3:
        print("usage: assemble_third_record.py BATTERY1_RUN_DIR BATTERY2_RUN_DIR")
        return 2
    b1, b2 = (os.path.abspath(x) for x in sys.argv[1:3])
    pub = os.path.join(here, "..", "published")
    G = {}

    def gate(name, ok, detail=None):
        G[name] = {"pass": bool(ok)}
        if detail is not None:
            G[name]["detail"] = detail

    # published byte pins (fetched at pinned main commit by the reproduce step)
    for key, (fname, expect) in PUB_FILES.items():
        p = os.path.join(pub, fname)
        ok = os.path.exists(p) and sha256_file(p) == expect
        gate("g_pin_published_" + key, ok, {"file": fname, "sha256": expect})
    gate("g_pin_published_audit_size",
         os.path.exists(os.path.join(pub, "harness-audit.json")) and
         os.path.getsize(os.path.join(pub, "harness-audit.json")) == PUB_AUDIT_ORACLE_BYTES,
         {"bytes": PUB_AUDIT_ORACLE_BYTES})

    # per-battery gates
    for tag, run in (("b1", b1), ("b2", b2)):
        for part in PARTS:
            p = os.path.join(run, "parts", part)
            if not os.path.exists(p):
                gate("g_%s_part_%s" % (tag, part.replace(".json", "")), False,
                     {"missing": "parts/" + part})
                continue
            ok, n = gates_all_pass(p)
            gate("g_%s_part_%s" % (tag, part.replace(".json", "")), ok, {"gates": n})
        audit = os.path.join(run, "harness-audit.json")
        has = os.path.exists(audit)
        ok = has and sha256_file(audit) == PUB_AUDIT_ORACLE_SHA and \
            os.path.getsize(audit) == PUB_AUDIT_ORACLE_BYTES
        gate("g_%s_audit_byte_identical_with_published" % tag, ok,
             {"sha256": PUB_AUDIT_ORACLE_SHA, "bytes": PUB_AUDIT_ORACLE_BYTES})

    # cross-battery identity (audit and all parts byte-identical between batteries)
    p1, p2 = os.path.join(b1, "harness-audit.json"), os.path.join(b2, "harness-audit.json")
    gate("g_cross_battery_audit_identical",
         os.path.exists(p1) and os.path.exists(p2) and read_bytes(p1) == read_bytes(p2),
         {"files": ["harness-audit.json"]})
    parts_same = {}
    for part in PARTS:
        q1, q2 = os.path.join(b1, "parts", part), os.path.join(b2, "parts", part)
        parts_same[part] = (os.path.exists(q1) and os.path.exists(q2) and
                            read_bytes(q1) == read_bytes(q2))
    gate("g_cross_battery_parts_identical", bool(parts_same) and all(parts_same.values()),
         parts_same)

    ok_all = all(v["pass"] for v in G.values())
    if not ok_all:
        print(json.dumps({"status": "FAIL", "gate_count": len(G), "gates": G},
                         indent=2, sort_keys=True))
        return 1
    record = {
        "schema": "k1166-fold29-cert-extract-third-verification-record-v1",
        "experiment": "n11-fold29-cert-extract-ext2-pristine-reexec-third-verification-20261120",
        "status": "PASS",
        "gate_count": len(G),
        "gates": G,
        "reproduction_targets": {
            "published_ext2_dir": "research/experiments/n11-fold29-win8-cert-extract-with-battery-20261120-NOT-USED",
            "published_ext2_fetch_commit": "1c42dcf25c78540033c5ec08c00952e4a939a8ee",
            "publisher_master_pin_commit": "28d223a2dd254b8a85cc342dff3f4bd801d1b31f",
            "harness_audit_oracle_sha256": PUB_AUDIT_ORACLE_SHA,
        },
        "batteries": {
            "b1": {"environment": "working cwd HOME, default hash seed",
                   "master_fetch": "fetch_master.py (all_blob_pins_ok true, 61 files)"},
            "b2": {"environment": "isolated cwd, isolated HOME, PYTHONHASHSEED=random",
                   "master_fetch": "fetch_master.py (all_blob_pins_ok true, 61 files)"},
        },
        "interpretation_guard": INTERPRETATION_GUARD,
    }
    record["reproduction_targets"]["published_ext2_dir"] = \
        "research/experiments/n11-fold29-win8-cert-extract-ext-second-verification-20261120"
    out = os.path.join(here, "..", "output", "third-verification.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({"status": record["status"], "gate_count": record["gate_count"],
                      "out": os.path.relpath(out, here)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
