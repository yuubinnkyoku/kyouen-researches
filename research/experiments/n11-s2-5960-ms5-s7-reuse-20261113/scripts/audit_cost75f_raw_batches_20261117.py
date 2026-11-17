#!/usr/bin/env python3
"""Raw sweep audit builder for the cost75f fresh v17 depth-10 sweep
(2026-11-17, head-1473 census v10 rank-1 row
00000000020000003800020080000000).

Reads the 9 raw batch JSONLs + 2 determinism rerun JSONLs + 2 v15
crosscheck JSONLs of this band (all published together with this
audit), verifies their git blob shas, and re-derives every check:

  * 9/9 pilot_d6 controls at {loss=false, nodes=3402, capped=false}
  * 75/75 candidate bits covered exactly once; the open/confirmation
    split and the legal candidate list match claim v1 (blob d9186019)
  * verdicts: 0 WIN7-D10 / 75 REFUTED-D10 / 0 capped; node totals;
    terminal stone range [13,17] on all 75 bits (no exceptions)
  * 4/4 confirmation transfers with an independent D4 canon
    re-derivation of both sides: canon(source_child|source_bit) ==
    claim root_canon == canon(75f_child|bit); every source verdict is
    re-read from the published source raw batch line (loss=false,
    not capped); bit 27 is raw-identical (same mask, same node count
    680730, source cost74i bit 41), the other three are canon-equal
    only (bit 93 = cost74i bit 79, bit 90 = cost73f bit 79, bit 115 =
    cost74f bit 79)
  * det reruns of batches 1 and 8 field-identical on every non-ms
    field
  * v15 cross-engine re-check of the 4 confirmation bits + the 5
    heaviest bits [7, 15, 66, 86, 105] (a/b chunks): 9/9 verdict
    agreement, 2/2 pilots at 5949, 0 capped

Emits class2-lane-cost75f-raw-sweep-audit-20261117.json.
No engine search is run by this script; WIN7-D10 proves a first-player
win within depth 10 from the individual 7-stone root only and
REFUTED-D10 is not a LOSS proof. 11x11 stays UNKNOWN.
"""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "output"

CHILD = "00000000020000003800020080000000"
CLAIM_V1 = "d9186019142efbb8284e8937f358c8d1a9632222"
CENSUS_V10_JSON = "fc2509f0bfa49359a3053289a9af1244cafcd950"
CENSUS_V10_SCRIPT = "6802948c83d5f83ffdf07b8bf675a42e94718533"
ENGINE_V17 = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
ENGINE_V15 = "8744fc65b6b7cac6bd561403ce4c749e01c51359"

RAW = {
    "class2-lane-cost75f-raw-batch1-20261117.jsonl": None,  # filled below
    "class2-lane-cost75f-raw-batch2-20261117.jsonl": None,
    "class2-lane-cost75f-raw-batch3-20261117.jsonl": None,
    "class2-lane-cost75f-raw-batch4-20261117.jsonl": None,
    "class2-lane-cost75f-raw-batch5-20261117.jsonl": None,
    "class2-lane-cost75f-raw-batch6-20261117.jsonl": None,
    "class2-lane-cost75f-raw-batch7-20261117.jsonl": None,
    "class2-lane-cost75f-raw-batch8-20261117.jsonl": None,
    "class2-lane-cost75f-raw-batch9-confirmation-20261117.jsonl": None,
    "class2-lane-cost75f-det-batch1-20261117.jsonl": None,
    "class2-lane-cost75f-det-batch8-20261117.jsonl": None,
    "class2-lane-cost75f-v15-crosscheck-a-20261117.jsonl": None,
    "class2-lane-cost75f-v15-crosscheck-b-20261117.jsonl": None,
}
def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def load_jsonl(name, pin):
    b = (OUT / name).read_bytes()
    got = git_blob_sha(b)
    assert got == pin, (name, got, pin)
    return [json.loads(line) for line in b.decode().splitlines() if line]


# ------------------------------------------------------------------ D4 canon
def images(mask):
    result = [0] * 8
    for p in range(121):
        if mask >> p & 1:
            x, y = p % 11, p // 11
            coords = ((x, y), (y, 10 - x), (10 - x, 10 - y), (10 - y, x),
                      (10 - x, y), (x, 10 - y), (y, x), (10 - y, 10 - x))
            for i, (a, b) in enumerate(coords):
                result[i] |= 1 << (11 * b + a)
    return result


IMG = [images(1 << p) for p in range(121)]


def canon(mask):
    best = None
    for r in range(8):
        v = 0
        for p in range(121):
            if mask >> p & 1:
                v |= IMG[p][r]
        if best is None or v < best:
            best = v
    return best


# ------------------------------------------------------------------- inputs
pins = {}
raws = {}
for name in RAW:
    b = (OUT / name).read_bytes()
    pins[name] = git_blob_sha(b)
    RAW[name] = pins[name]
    raws[name] = [json.loads(line) for line in b.decode().splitlines()
                  if line]

# claim v1 fields carried verbatim (the claim file on main advances to
# v2+ after the sweep; the v1 blob pin above is the historical record)
LEGAL_CANDIDATES = [
    0, 2, 3, 4, 7, 8, 10, 11, 12, 14, 15, 16, 17, 18, 26, 27, 28, 29,
    32, 33, 37, 38, 39, 40, 42, 43, 44, 45, 46, 48, 49, 50, 53, 54, 66,
    67, 69, 70, 72, 74, 75, 76, 77, 78, 79, 80, 82, 83, 84, 85, 86, 87,
    88, 90, 92, 93, 94, 95, 99, 102, 103, 104, 105, 106, 108, 109, 110,
    112, 113, 114, 115, 116, 117, 118, 120]
CONFIRMATION_BITS = [27, 90, 93, 115]
OPEN_BITS = [b for b in LEGAL_CANDIDATES if b not in CONFIRMATION_BITS]
TRANSFER_ROOT_CANONS = {
    "27": "00000000020000003800020088000000",
    "90": "000000000200800038000000c0000000",
    "93": "00000000020080003800000088000000",
    "115": "00000000020080003800000080000020",
}

# ------------------------------------------------------------ 1. aggregation
per_bit = {}
pilots = 0
for name, recs in raws.items():
    if "v15" in name or "-det-" in name:
        continue
    for d in recs:
        if "control" in d:
            assert d == {"control": "pilot_d6", "loss": False,
                         "nodes": 3402, "capped": False}, (name, d)
            pilots += 1
        else:
            assert d["bit"] not in per_bit, (name, d["bit"])
            per_bit[d["bit"]] = d
assert pilots == 9, pilots
assert len(per_bit) == 75, len(per_bit)
assert sorted(per_bit) == LEGAL_CANDIDATES

open_bits = OPEN_BITS
conf_bits = CONFIRMATION_BITS
assert sorted(open_bits + conf_bits) == sorted(per_bit)
assert len(open_bits) == 71 and len(conf_bits) == 4

wins = sorted(b for b, d in per_bit.items() if d["loss"])
refuted = sorted(b for b, d in per_bit.items() if not d["loss"])
capped = sorted(b for b, d in per_bit.items() if d["capped"])
assert wins == [] and len(refuted) == 75 and capped == []
for b, d in per_bit.items():
    assert d["terminalStoneRange"] == [13, 17], (b, d)
cand_total = sum(d["nodes"] for d in per_bit.values())
heaviest = max(per_bit, key=lambda b: per_bit[b]["nodes"])

# ------------------------------------------- 2. confirmation canon rederivation
SOURCES = {
    "27": {"band": "cost74i", "child": "00000000020000003800000088000000",
           "bit": 41, "file": "class2-lane-cost74i-raw-batch3-20261117.jsonl",
           "pin": "60d7aea63d5a028146dd1040ff8e35b684fd810f"},
    "90": {"band": "cost73f", "child": "000000000200000038000000c0000000",
           "bit": 79, "file": "class2-lane-cost73f-raw-batch6-20261115.jsonl",
           "pin": "819918d6ed0d1beee1e38fdf6fac8e5d2f7624ef"},
    "93": {"band": "cost74i", "child": "00000000020000003800000088000000",
           "bit": 79, "file": "class2-lane-cost74i-raw-batch5-20261117.jsonl",
           "pin": "cd5dcb1068376e40a35d0d1d58ef6f5c86facbdb"},
    "115": {"band": "cost74f", "child": "00000000020000003800000080000020",
            "bit": 79, "file": "class2-lane-cost74f-raw-batch6-20261115.jsonl",
            "pin": "e0b57492f0d2f8daf84aab5a6bde99670508ebbe"},
}
child_v = int(CHILD, 16)
conf_out = {}
for b_str, s in SOURCES.items():
    b = int(b_str)
    tr = {"root_canon": TRANSFER_ROOT_CANONS[b_str]}
    # fresh side
    fresh = per_bit[b]
    assert fresh["loss"] is False and not fresh["capped"], fresh
    fresh_canon = canon(child_v | (1 << b))
    assert format(fresh_canon, "032x") == tr["root_canon"], (b, tr)
    # source side
    src_bytes = (OUT / s["file"]).read_bytes()
    assert git_blob_sha(src_bytes) == s["pin"], s["file"]
    src_line = None
    for line in src_bytes.decode().splitlines():
        d = json.loads(line)
        if "bit" in d and d["bit"] == s["bit"]:
            assert src_line is None, (s, "duplicate")
            src_line = d
    assert src_line is not None, s
    assert src_line["loss"] is False and not src_line["capped"], src_line
    src_canon = canon(int(s["child"], 16) | (1 << s["bit"]))
    assert src_canon == fresh_canon, (b, "canon mismatch")
    raw_identical = ((int(s["child"], 16) | (1 << s["bit"]))
                     == (child_v | (1 << b)))
    conf_out[b_str] = {
        "source": f"{s['band']} bit {s['bit']}",
        "source_file": s["file"],
        "source_verdict": "REFUTED-D10",
        "source_nodes": src_line["nodes"],
        "fresh_nodes": fresh["nodes"],
        "canon_equal": True,
        "raw_identical": raw_identical,
    }

# ------------------------------------------------------------- 3. det + v15
def strip_ms(recs):
    return [{k: v for k, v in d.items() if k != "ms"} for d in recs]


det_results = {}
for b in (1, 8):
    a = strip_ms(raws[f"class2-lane-cost75f-raw-batch{b}-20261117.jsonl"])
    d = strip_ms(raws[f"class2-lane-cost75f-det-batch{b}-20261117.jsonl"])
    assert a == d, f"det batch {b} differs"
    det_results[f"class2-lane-cost75f-det-batch{b}-20261117.jsonl"] = {
        "lines": len(d),
        "heaviest_bit": max(
            (x for x in d if "bit" in x), key=lambda x: x["nodes"])["bit"],
    }

v15 = (raws["class2-lane-cost75f-v15-crosscheck-a-20261117.jsonl"]
       + raws["class2-lane-cost75f-v15-crosscheck-b-20261117.jsonl"])
v15_pilots = [d for d in v15 if "control" in d]
assert len(v15_pilots) == 2
for p in v15_pilots:
    assert p == {"control": "pilot_d6", "loss": False, "nodes": 5949,
                 "capped": False}, p
v15_bits = [d for d in v15 if "bit" in d]
assert len(v15_bits) == 9
v15_nodes = 0
for d in v15_bits:
    fresh = per_bit[d["bit"]]
    assert d["loss"] == fresh["loss"] and not d["capped"], d
    v15_nodes += d["nodes"]
v15_cover = sorted(d["bit"] for d in v15_bits)
assert v15_cover == sorted(conf_bits + [7, 15, 66, 86, 105])

# ------------------------------------------------------------------ 4. out
out = {
    "schema": "n11-class2-lane-cost75f-raw-sweep-audit-20261117-v1",
    "date": "2026-11-17",
    "status": (
        "PASS: first fresh execution of the cost75f 75-bit v17 depth-10 "
        "sweep (head-1473 census v10 rank-1 row); 0 WIN7-D10 / 75 "
        "REFUTED-D10 / 0 capped; 4/4 confirmation transfers with "
        "independent D4 canon re-derivation of both sides (bit 27 "
        "raw-identical, same node count 680730 as cost74i bit 41, the "
        "other three canon-equal only), every source verdict re-read "
        "from the published source raw batch line; det reruns of "
        "batches 1 and 8 field-identical; v15 cross-engine 9/9 verdict "
        "agreement (4 confirmation bits + the 5 heaviest bits [7, 15, "
        "66, 86, 105]), 2/2 pilots at 5949; the row is complete at "
        "audit strength with no WIN candidate, so no certificate "
        "extraction and no receipt fold are needed"),
    "target": {
        "s6_child": CHILD,
        "stone_bits": [31, 41, 59, 60, 61, 89],
        "candidate_bits": 75,
        "open_bits": 71,
        "confirmation_bits": [27, 90, 93, 115],
    },
    "provenance": {
        "original_run": ("this audit's raw files are the original claiming "
                         "session's own execution (no sandbox reset "
                         "intervened, no concurrent-session overlap existed "
                         "for this child at claim time); the raw batch "
                         "JSONLs, det rerun JSONLs and v15 crosscheck "
                         "JSONLs are published together with this audit "
                         "and the claim v2"),
        "engine": ("class4_child1_runner_v17.ts, git blob "
                   + ENGINE_V17 + ", depth 10, cap 1e9 per bit, "
                   "andclose 1, fresh engine state per candidate bit"),
        "v15_engine": ("class4_child1_runner.ts, git blob " + ENGINE_V15),
        "batch_driver": ("scripts/ev75f_batches_20261117.sh (same batch plan "
                         "shape as the cost74i run: 7x9 + 1x8 open bits + 1 "
                         "confirmation batch of 4 bits)"),
    },
    "pilot_checks": "9/9 raw batches + 2/2 det reruns at pilot_d6 3402; 2/2 v15 chunks at pilot_d6 5949",
    "verdicts": {
        "win7_d10_bits": [],
        "win7_d10_nodes": {},
        "refuted_d10_bits": refuted,
        "refuted_d10_count": 75,
        "capped_count": 0,
        "candidate_nodes_total": cand_total,
        "total_nodes_including_pilots": cand_total + 9 * 3402 + 2 * 3402
        + 2 * 5949,
        "terminal_stone_range": [13, 17],
        "terminal_stone_range_exceptions": {},
        "heaviest_bit": heaviest,
        "heaviest_bit_nodes": per_bit[heaviest]["nodes"],
    },
    "confirmation_bits": {
        "bits": [27, 90, 93, 115],
        "fresh_vs_claim_transfers": "4/4",
        "canon_rederivation": (
            "independent D4 canon function (copied verbatim from the "
            "published census v10 script, git blob " + CENSUS_V10_SCRIPT
            + "): canon(source_child|source_bit) == claim root_canon == "
            "canon(75f_child|bit), 4/4; bit 27 raw-identical (same mask, "
            "same node count 680730 as cost74i bit 41), bits 90/93/115 "
            "canon-equal only"),
        "sources": conf_out,
    },
    "determinism_rerun": {
        "batches": det_results,
        "result": "field-identical on every non-ms field",
    },
    "v15_cross_engine_check": {
        "chunks": ["a (4 confirmation bits)",
                   "b (5 heaviest bits [7, 15, 66, 86, 105])"],
        "verdict_agreement": "9/9 loss=false",
        "pilots": "2/2 at 5949",
        "capped": 0,
        "v15_nodes_total": v15_nodes,
    },
    "pins": {
        "claim_v1": CLAIM_V1,
        "census_v10_script": CENSUS_V10_SCRIPT,
        "census_v10_json": CENSUS_V10_JSON,
        "engine_v17": ENGINE_V17,
        "engine_v15": ENGINE_V15,
        "sources": {b: s["pin"] for b, s in SOURCES.items()},
        "raw_batches": pins,
    },
    "interpretation_guard": (
        "engine-search verdicts for the 75 seven-stone roots of this child "
        "only. WIN7-D10 proves a first-player win within depth 10 from the "
        "individual 7-stone root only; REFUTED-D10 is not a LOSS proof; no "
        "manifest row is closed by this sweep. The 11x11 empty board, the "
        "two-stone roots {49,60} and {59,60}, S2 {59,60}, and classes "
        "1/2/4 all remain UNKNOWN."),
}
out_path = OUT / "class2-lane-cost75f-raw-sweep-audit-20261117.json"
payload = json.dumps(out, indent=1, sort_keys=False, ensure_ascii=True) + "\n"
out_path.write_bytes(payload.encode())
print(f"wrote {out_path} ({out_path.stat().st_size} bytes)")
print("verdicts: 0 WIN7-D10 / 75 REFUTED-D10 / 0 capped; heaviest bit",
      heaviest, per_bit[heaviest]["nodes"])
