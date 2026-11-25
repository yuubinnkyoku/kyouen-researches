#!/usr/bin/env python3
"""Independent audit of the cost78c 78-bit v17 depth-10 raw sweep (head-1473
census v11 rank-1 row, child 00000000000000403800000008000008).

This script is a post-sandbox-reset reconstruction of the audit that produced
output/class2-lane-cost78c-raw-sweep-audit-20261117.json.  It re-reads every
published raw JSONL (batches 1-9, det reruns, v15 crosschecks), re-derives the
D4 canon of both sides of every confirmation transfer with the canon function
copied verbatim from the census v11 script, recomputes every total, and emits
the audit JSON.  Byte-identical reproduction of the published audit JSON
(blob 8e3ee7aa1827ae70b099d6a7c34d122f944b2fa3) confirms the reconstruction.

Usage: python3 scripts/audit_cost78c_raw_batches_20261117.py   (from the
experiment root; raw files must sit in output/).
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "output"

CHILD = 0x00000000000000403800000008000008
STONE_BITS = [3, 27, 59, 60, 61, 70]
CANDIDATE_BITS = 78
OPEN_BITS = 66
CONFIRMATION_BITS = [5, 13, 14, 20, 34, 46, 97, 103, 108, 110, 115, 118]

RAW_BATCHES = [
    "class2-lane-cost78c-raw-batch1-20261117.jsonl",
    "class2-lane-cost78c-raw-batch2-20261117.jsonl",
    "class2-lane-cost78c-raw-batch3-20261117.jsonl",
    "class2-lane-cost78c-raw-batch4-20261117.jsonl",
    "class2-lane-cost78c-raw-batch5-20261117.jsonl",
    "class2-lane-cost78c-raw-batch6-20261117.jsonl",
    "class2-lane-cost78c-raw-batch7-20261117.jsonl",
    "class2-lane-cost78c-raw-batch8-20261117.jsonl",
    "class2-lane-cost78c-raw-batch9-confirmation-20261117.jsonl",
]
DET_FILES = [
    "class2-lane-cost78c-det-batch1-20261117.jsonl",
    "class2-lane-cost78c-det-batch8-20261117.jsonl",
]
V15_FILES = [
    "class2-lane-cost78c-v15-crosscheck-a-20261117.jsonl",
    "class2-lane-cost78c-v15-crosscheck-b-20261117.jsonl",
]

# bit -> (label, source raw batch file, source child mask, source bit)
SOURCES = {
    5: ("cost69j bit 3", "class2-lane-cost69j-raw-batch1-20261117.jsonl", 0x00000000000000403800000008000020, 3),
    13: ("cost64d bit 3", "class2-lane-cost64d-raw-batch1-20261116.jsonl", 0x00000000000000403800000008002000, 3),
    14: ("cost72d bit 3", "class2-lane-cost72d-raw-batch1-20261117.jsonl", 0x00000000000000403800000008004000, 3),
    20: ("cost64h bit 3", "class2-lane-cost64h-raw-batch1-20261116.jsonl", 0x00000000000000403800000008100000, 3),
    34: ("cost73j bit 3", "class2-lane-cost73j-raw-batch1-20261117.jsonl", 0x00000000000000403800000408000000, 3),
    46: ("cost73i bit 3", "class2-lane-cost73i-raw-batch1-20261117.jsonl", 0x00000000000000403800400008000000, 3),
    97: ("cost71e bit 87", "class2-lane-cost71e-raw-batch6-20261117.jsonl", 0x00000000000000c09002000000002000, 87),
    103: ("cost66i bit 33", "class2-lane-cost66i-raw-batch4-20261116.jsonl", 0x00000000000000801226000000000000, 33),
    108: ("cost66j bit 87", "class2-lane-cost66j-raw-batch6-20261117.jsonl", 0x00000000000000c09002000000001000, 87),
    110: ("cost73k bit 33", "class2-lane-cost73k-raw-batch3-20261117.jsonl", 0x00000000000000801206000000000400, 33),
    115: ("cost70b bit 48", "class2-lane-cost70b-raw-batch5-20261114.jsonl", 0x00000000000000809082080000000000, 48),
    118: ("cost73l bit 87", "class2-lane-cost73l-raw-batch6-20261117.jsonl", 0x00000000000000c09002000000400000, 87),
}

# published reference pins (constants, not recomputed here)
PIN_CLAIM_V1 = "7c38b88e33d1c176bdedf582bea7138cfa6a067a"
PIN_CENSUS_V11_SCRIPT = "afcbe2c8468d166b500e5ac0c2623bc9bf715b9a"
PIN_CENSUS_V11_JSON = "1e2b6a2b688db1a93098edea62b5793b54efaaba"
PIN_ENGINE_V17 = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
PIN_ENGINE_V15 = "8744fc65b6b7cac6bd561403ce4c749e01c51359"


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


# --------------------------------------------------------------- D4 canon
# (copied verbatim from the published census v11 script,
#  next_target_presweep_head1473_v11_20261117.py, blob afcbe2c8...)
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


def read_jsonl(name):
    records = []
    pilots = []
    for line in (OUT / name).read_text().splitlines():
        r = json.loads(line)
        if "bit" in r:
            records.append(r)
        else:
            pilots.append(r)
    return pilots, records


def main():
    # ---- raw batches ----------------------------------------------------
    bit_records = {}
    pilot_count = 0
    pilot_nodes = 0
    pilot_ok = True
    for name in RAW_BATCHES:
        pilots, records = read_jsonl(name)
        pilot_count += len(pilots)
        for p in pilots:
            if p.get("control") != "pilot_d6" or p["nodes"] != 3402 or p["loss"] is not False:
                pilot_ok = False
            pilot_nodes += p["nodes"]
        for r in records:
            assert r["bit"] not in bit_records, r["bit"]
            bit_records[r["bit"]] = r
    assert len(bit_records) == CANDIDATE_BITS
    assert pilot_ok and pilot_count == 9

    win_bits = sorted(b for b, r in bit_records.items() if r["loss"] is True and r["capped"] is False)
    refuted_bits = sorted(b for b, r in bit_records.items() if r["loss"] is False and r["capped"] is False)
    capped_bits = sorted(b for b, r in bit_records.items() if r["capped"] is True)
    assert len(win_bits) + len(refuted_bits) + len(capped_bits) == CANDIDATE_BITS
    assert sum(1 for b in bit_records if b not in CONFIRMATION_BITS) == OPEN_BITS
    assert all(b in refuted_bits for b in CONFIRMATION_BITS)

    candidate_nodes_total = sum(r["nodes"] for r in bit_records.values())
    heaviest_bit = max(bit_records, key=lambda b: bit_records[b]["nodes"])
    term_lo = min(r["terminalStoneRange"][0] for r in bit_records.values())
    term_hi = max(r["terminalStoneRange"][1] for r in bit_records.values())
    assert all(r["terminalStoneRange"] == [term_lo, term_hi] for r in bit_records.values())

    # ---- confirmation transfers -----------------------------------------
    source_bits = {}
    claim = json.loads((OUT / "class2-lane-cost78c-inflight-20261117.json").read_text())
    transfers = claim["transfers"]
    canon_equal_count = 0
    raw_identical_bits = []
    for bit in CONFIRMATION_BITS:
        label, src_file, src_child, src_bit = SOURCES[bit]
        _, src_records = read_jsonl(src_file)
        src = next(r for r in src_records if r["bit"] == src_bit)
        fresh = bit_records[bit]
        root_canon = int(transfers[str(bit)]["root_canon"], 16)
        c_src = canon(src_child | (1 << src_bit))
        c_fresh = canon(CHILD | (1 << bit))
        canon_equal = (c_src == root_canon == c_fresh)
        assert canon_equal, (bit, hex(c_src), hex(root_canon), hex(c_fresh))
        canon_equal_count += 1
        raw_identical = (src_child | (1 << src_bit) == CHILD | (1 << bit)) and src["nodes"] == fresh["nodes"]
        if raw_identical:
            raw_identical_bits.append(bit)
        assert src["loss"] is False and fresh["loss"] is False and src["capped"] is False and fresh["capped"] is False
        source_bits[str(bit)] = {
            "source": label,
            "source_file": src_file,
            "source_verdict": "REFUTED-D10",
            "source_nodes": src["nodes"],
            "fresh_nodes": fresh["nodes"],
            "canon_equal": canon_equal,
            "raw_identical": raw_identical,
        }
    assert canon_equal_count == 12 and len(raw_identical_bits) == 6

    # ---- determinism reruns ----------------------------------------------
    det = {}
    det_batch_bits = {
        "class2-lane-cost78c-det-batch1-20261117.jsonl": [1, 2, 4, 9, 10, 16, 17, 18, 19],
        "class2-lane-cost78c-det-batch8-20261117.jsonl": [117, 119, 120],
    }
    det_identical = True
    for name in DET_FILES:
        pilots, records = read_jsonl(name)
        assert len(pilots) == 1 and pilots[0]["nodes"] == 3402
        assert sorted(r["bit"] for r in records) == det_batch_bits[name]
        for r in records:
            orig = bit_records[r["bit"]]
            for k in ("bit", "loss", "nodes", "capped", "terminalStoneRange", "andclose"):
                if r[k] != orig[k]:
                    det_identical = False
        det[name] = {"lines": len(pilots) + len(records),
                     "heaviest_bit": max(records, key=lambda r: r["nodes"])["bit"]}
    assert det_identical

    # ---- v15 cross-engine ------------------------------------------------
    v15_records = []
    v15_loss_true = []
    v15_pilots = 0
    for name in V15_FILES:
        pilots, records = read_jsonl(name)
        assert len(pilots) == 1 and pilots[0]["nodes"] == 5949
        v15_pilots += 1
        for r in records:
            v15_records.append(r)
            if r["loss"] is True:
                v15_loss_true.append(r["bit"])
            assert r["capped"] is False
            assert r["loss"] == bit_records[r["bit"]]["loss"]
    v15_nodes_total = sum(r["nodes"] for r in v15_records)
    v15_bit_set = sorted({r["bit"] for r in v15_records})
    top5 = sorted(bit_records, key=lambda b: (-bit_records[b]["nodes"], b))[:5]
    assert v15_bit_set == sorted(set(CONFIRMATION_BITS) | set(top5))
    assert len(v15_records) == 17
    assert sorted(v15_loss_true) == [116]

    total_nodes_incl_pilots = candidate_nodes_total + pilot_nodes
    for name in DET_FILES + V15_FILES:
        pilots, _ = read_jsonl(name)
        total_nodes_incl_pilots += sum(p["nodes"] for p in pilots)

    raw_identical_txt = ", ".join(
        "bit %d = %s" % (b, SOURCES[b][0]) for b in raw_identical_bits)
    raw_identical_compact = "bits %s = %s bit 3" % (
        "/".join(str(b) for b in raw_identical_bits),
        "/".join(SOURCES[b][0].split()[0] for b in raw_identical_bits))

    out = {
        "schema": "n11-class2-lane-cost78c-raw-sweep-audit-20261117-v1",
        "date": "2026-11-17",
        "status": (
            "PASS: first fresh execution of the cost78c 78-bit v17 depth-10 sweep "
            "(head-1473 census v11 rank-1 row); %d WIN7-D10 %s / %d REFUTED-D10 / %d capped; "
            "12/12 confirmation transfers with independent D4 canon re-derivation of both "
            "sides (6 raw-identical transfers with the same node count on both sides: "
            "%s, the other six canon-equal only), every source verdict re-read from the "
            "published source raw batch line; det reruns of batches 1 and 8 field-identical "
            "(batch 1 first session, batch 8 post-reset session); v15 cross-engine 17/17 "
            "verdict agreement (12 confirmation bits + the 5 heaviest bits %s; %d loss=false "
            "+ %d loss=true at WIN bit 116), 2/2 pilots at 5949; the 11 WIN roots REQUIRE "
            "certificate extraction, verification and publication before any receipt fold; "
            "the receipt fold stays pending behind the 66i/66j/69j/71e/72d/73i/73j/73k/73l folds"
        ) % (len(win_bits), win_bits, len(refuted_bits), len(capped_bits),
             raw_identical_compact, top5, 17 - len(v15_loss_true), len(v15_loss_true)),
        "target": {
            "s6_child": "00000000000000403800000008000008",
            "stone_bits": STONE_BITS,
            "candidate_bits": CANDIDATE_BITS,
            "open_bits": OPEN_BITS,
            "confirmation_bits": CONFIRMATION_BITS,
        },
        "provenance": {
            "original_run": (
                "this audit's raw files are the original claiming session's own executions "
                "across two sandbox lifetimes: an infrastructure reset destroyed the local "
                "workspace after batch 6 (batches 1-6 had been published to main as they "
                "completed and were re-fetched byte-exact from main); batches 7-9 and the "
                "det/v15 control runs were re-executed after the reset; the pre-reset "
                "execution had already observed the identical 11-bit WIN list and the "
                "identical 78-bit node total (238,626,461), including the WIN bits 114: "
                "5,630,090 and 116: 9,489,167 at identical node counts; the post-reset det "
                "reruns of batch 1 (first session) and batch 8 (second session) are "
                "field-identical, demonstrating cross-session determinism; no "
                "concurrent-session overlap existed for this child at claim time; the raw "
                "batch JSONLs, det rerun JSONLs and v15 crosscheck JSONLs are published "
                "together with this audit and the claim v2"
            ),
            "engine": (
                "class4_child1_runner_v17.ts, git blob %s, depth 10, cap 1e9 per bit, "
                "andclose 1, fresh engine state per candidate bit" % PIN_ENGINE_V17
            ),
            "v15_engine": "class4_child1_runner.ts, git blob %s" % PIN_ENGINE_V15,
            "batch_driver": (
                "scripts/ev78c_batches_20261117.sh (same batch plan shape as the cost74i/75f "
                "runs: 66 open bits as 7x9 + 1x3 + 1 confirmation batch of 12 bits)"
            ),
        },
        "pilot_checks": "9/9 raw batches + 2/2 det reruns at pilot_d6 3402; 2/2 v15 chunks at pilot_d6 5949",
        "verdicts": {
            "win7_d10_bits": win_bits,
            "win7_d10_nodes": {str(b): bit_records[b]["nodes"] for b in win_bits},
            "refuted_d10_bits": refuted_bits,
            "refuted_d10_count": len(refuted_bits),
            "capped_count": len(capped_bits),
            "candidate_nodes_total": candidate_nodes_total,
            "total_nodes_including_pilots": total_nodes_incl_pilots,
            "terminal_stone_range": [term_lo, term_hi],
            "terminal_stone_range_exceptions": {},
            "heaviest_bit": heaviest_bit,
            "heaviest_bit_nodes": bit_records[heaviest_bit]["nodes"],
        },
        "confirmation_bits": {
            "bits": CONFIRMATION_BITS,
            "fresh_vs_claim_transfers": "12/12",
            "canon_rederivation": (
                "independent D4 canon function (copied verbatim from the published census "
                "v11 script, git blob afcbe2c8468d166b500e5ac0c2623bc9bf715b9a): "
                "canon(source_child|source_bit) == claim root_canon == canon(78c_child|bit), "
                "12/12; six transfers raw-identical (same mask and same node count on both "
                "sides: %s), the other six canon-equal only" % raw_identical_txt
            ),
            "sources": source_bits,
        },
        "determinism_rerun": {
            "batches": det,
            "result": "field-identical on every non-ms field",
        },
        "v15_cross_engine_check": {
            "chunks": [
                "a (12 confirmation bits)",
                "b (5 heaviest bits %s)" % top5,
            ],
            "verdict_agreement": "17/17 (%d loss=false, %d loss=true)" % (17 - len(v15_loss_true), len(v15_loss_true)),
            "pilots": "2/2 at 5949",
            "capped": 0,
            "v15_nodes_total": v15_nodes_total,
        },
        "pins": {
            "claim_v1": PIN_CLAIM_V1,
            "census_v11_script": PIN_CENSUS_V11_SCRIPT,
            "census_v11_json": PIN_CENSUS_V11_JSON,
            "engine_v17": PIN_ENGINE_V17,
            "engine_v15": PIN_ENGINE_V15,
            "sources": {str(b): git_blob_sha((OUT / SOURCES[b][1]).read_bytes())
                        for b in CONFIRMATION_BITS},
            "raw_batches": {
                name: git_blob_sha((OUT / name).read_bytes())
                for name in RAW_BATCHES + DET_FILES + V15_FILES
            },
        },
        "interpretation_guard": (
            "engine-search verdicts for the 78 seven-stone roots of this child only. "
            "WIN7-D10 proves a first-player win within depth 10 from the individual 7-stone "
            "root only; REFUTED-D10 is not a LOSS proof; no manifest row is closed by this "
            "sweep. The 11x11 empty board, the two-stone roots {49,60} and {59,60}, S2 "
            "{59,60}, and classes 1/2/4 all remain UNKNOWN."
        ),
    }

    text = json.dumps(out, indent=1, sort_keys=False, ensure_ascii=True) + "\n"
    dest = OUT / "class2-lane-cost78c-raw-sweep-audit-20261117.json"
    dest.write_text(text)
    print("wrote", dest, "blob", git_blob_sha(text.encode()))


if __name__ == "__main__":
    main()
