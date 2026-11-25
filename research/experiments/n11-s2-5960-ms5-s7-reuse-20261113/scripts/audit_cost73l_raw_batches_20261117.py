#!/usr/bin/env python3
# Raw-batch audit for the cost73l fresh v17 depth-10 sweep (2026-11-17),
# the first execution of the head-1473 census v8 rank-1 row
# 00000000000000c09002000000400000 (66 open + 7 confirmation bits).
#
# Checks:
#  1. raw batches: 73-bit partition equal to the claim v1 legal_candidates,
#     9/9 pilot_d6 3402 controls, 34 WIN / 39 REFUTED / 0 capped, node sums;
#  2. confirmation bits: fresh outcomes == claim v1 transfer verdicts (7/7);
#     independent D4 canon re-derivation (function copied verbatim from the
#     published census v8 script, blob-pinned) proves canon equality of
#     every transfer pair: canon(source_child | source_bit) ==
#     canon(73l_child | bit) == claim root_canon; the lane sources verified
#     against their published raw batch lines (verdict level); the bit 97
#     pre-64h harvest source is identified here as cost64d bit 118 (the only
#     canon match among the published pre-64h raw batches);
#  3. determinism reruns of batches 1 and 4 (batch 4 holds the heaviest
#     search bit 47, 6,045,349 nodes): field-identical on every non-ms field;
#  4. independent v15 cross-engine re-check a/b/c/d over all 34 WIN bits:
#     34/34 loss=true, 4/4 pilots 5949, 0 capped.
#
# Usage:
#   python3 audit_cost73l_raw_batches_20261117.py \
#       <raw_dir> <claim_v1.json> <out.json>
import hashlib, json, sys, pathlib

V1_BLOB = "fa13a0ada22e3de95c06e9a3101ce6d2a738f5b1"
CENSUS_V8_SCRIPT_BLOB = "c86171ba4d9c235688336f2d97690c7896ad5bed"
CENSUS_V8_JSON_BLOB = "2542914e02db14a8426a1a16ef1c2cfcd9817375"
ENGINE_BLOB = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
V15_BLOB = "8744fc65b6b7cac6bd561403ce4c749e01c51359"
CHILD = "00000000000000c09002000000400000"

# published lane sources for the 7 confirmation transfers (raw batch line +
# full git blob pin of the raw batch file, all verified published on main)
SOURCES = {
    "65": {"lane": "cost69j", "child": "00000000000000403800000008000020",
           "bit": 118, "file": "class2-lane-cost69j-raw-batch8-20261117.jsonl",
           "pin": "feaa2d78ac5a11f772a649b7f13865abe2aa743c"},
    "86": {"lane": "cost72d", "child": "00000000000000403800000008004000",
           "bit": 118, "file": "class2-lane-cost72d-raw-batch8-20261117.jsonl",
           "pin": "1fd124264c1a79273ae1c4a6d656beb0a2c657ae"},
    "90": {"lane": "cost76c", "child": "00000000010000809002000001000000",
           "bit": 48, "file": "class2-lane-cost76c-raw-batch4-20261116.jsonl",
           "pin": "a7c5ee5167529ff44351f5b438cf1636352bffca"},
    "94": {"lane": "cost73i", "child": "00000000000000403800400008000000",
           "bit": 118, "file": "class2-lane-cost73i-raw-batch8-20261117.jsonl",
           "pin": "74af3374758a7561bc3c0d9a7a826a8473421903"},
    "97": {"lane": "cost64d (pre-64h harvest)", "child": "00000000000000403800000008002000",
           "bit": 118, "file": "class2-lane-cost64d-raw-batch8-20261116.jsonl",
           "pin": "ce86d0fb24fbbb63e39efbbc47c821965b9a4188"},
    "106": {"lane": "cost73j", "child": "00000000000000403800000408000000",
            "bit": 118, "file": "class2-lane-cost73j-raw-batch8-20261117.jsonl",
            "pin": "522b0e567e143afc77d1fef66a6cc84a5e73e449"},
    "110": {"lane": "cost73k", "child": "00000000000000801206000000000400",
            "bit": 98, "file": "class2-lane-cost73k-raw-batch6-20261117.jsonl",
            "pin": "bc15e86cba867e75460366b7fe98b030ee116517"},
}
RAW = [f"class2-lane-cost73l-raw-batch{i}-20261117.jsonl" for i in range(1, 9)] + \
      ["class2-lane-cost73l-raw-batch9-confirmation-20261117.jsonl"]
DET = {"class2-lane-cost73l-det-batch1-20261117.jsonl":
        "class2-lane-cost73l-raw-batch1-20261117.jsonl",
       "class2-lane-cost73l-det-batch4-20261117.jsonl":
        "class2-lane-cost73l-raw-batch4-20261117.jsonl"}
V15 = [f"class2-lane-cost73l-v15-crosscheck-{c}-20261117.jsonl" for c in "abcd"]
WINS_EXPECTED = [1, 2, 3, 4, 6, 8, 9, 18, 21, 23, 25, 28, 29, 32, 34, 41, 42,
                 44, 47, 53, 54, 61, 62, 64, 66, 80, 95, 105, 106, 110, 112,
                 113, 116, 119]
NODE_TOTAL = 133895305
CONFIRM_BITS = [65, 86, 90, 94, 97, 106, 110]


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


# ------------------------------------------------ D4 canon (verbatim from the
# published census v8 script scripts/next_target_presweep_head1473_v8_
# 20261117.py, git blob c86171ba4d9c235688336f2d97690c7896ad5bed)
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


def main() -> None:
    raw_dir = pathlib.Path(sys.argv[1])
    v1_path = pathlib.Path(sys.argv[2])
    out_path = pathlib.Path(sys.argv[3])

    # ------------------------------------------------ inputs + pins
    v1_bytes = v1_path.read_bytes()
    assert git_blob_sha(v1_bytes) == V1_BLOB, "claim v1 pin"
    claim = json.loads(v1_bytes)
    assert claim["schema"] == "n11-class2-lane-cost73l-inflight-20261117-v1"
    assert claim["s6_child"] == CHILD
    cands = claim["legal_candidates"]
    assert len(cands) == 73

    # ------------------------------------------------ 1. raw batches
    mine, batch_of, pilots = {}, {}, 0
    for i, fname in enumerate(RAW, start=1):
        for line in (raw_dir / fname).read_text().splitlines():
            r = json.loads(line)
            if r.get("control"):
                assert r["control"] == "pilot_d6" and r["nodes"] == 3402 \
                    and r["loss"] is False and r["capped"] is False, (fname, r)
                pilots += 1
                continue
            assert r["bit"] not in mine, r["bit"]
            assert r["andclose"] is True, r
            tsr = r["terminalStoneRange"]
            assert tsr == [13, 17] or (r["bit"] == 91 and tsr == [13, 15]), r
            mine[r["bit"]] = r
            batch_of[r["bit"]] = i
    assert pilots == 9 and len(mine) == 73
    assert sorted(mine) == sorted(cands), "partition != claim v1 legal candidates"
    wins = sorted(b for b in mine if mine[b]["loss"])
    refuted = sorted(b for b in mine if not mine[b]["loss"])
    assert wins == WINS_EXPECTED, wins
    assert len(wins) == 34 and len(refuted) == 39
    capped = sum(1 for b in mine if mine[b]["capped"])
    assert capped == 0
    node_sum = sum(mine[b]["nodes"] for b in mine)
    assert node_sum == NODE_TOTAL, node_sum
    assert sorted(batch_of[b] for b in CONFIRM_BITS) == [9] * 7
    open_bits = sorted(b for b in mine if b not in CONFIRM_BITS)
    assert len(open_bits) == 66
    for i in range(1, 9):
        got = sorted(b for b in open_bits if batch_of[b] == i)
        assert len(got) == (9 if i < 8 else 3), (i, got)

    # ------------------------------------------------ 2. confirmation transfers
    transfers = claim["transfers"]
    assert sorted(int(k) for k in transfers) == CONFIRM_BITS
    exp_verdict = {int(k): v["verdict"] for k, v in transfers.items()}
    canon_notes = {}
    for k, src in SOURCES.items():
        bit = int(k)
        fresh_loss = mine[bit]["loss"]
        verdict = "WIN7-D10" if fresh_loss else "REFUTED-D10"
        assert verdict == exp_verdict[bit], (bit, verdict, exp_verdict[bit])
        # independent canon re-derivation, both sides
        src_canon = canon(int(src["child"], 16) | (1 << src["bit"]))
        my_canon = canon(int(CHILD, 16) | (1 << bit))
        rc = int(transfers[k]["root_canon"], 16)
        assert src_canon == rc == my_canon, (bit, hex(src_canon), hex(my_canon))
        # source raw line verdict agreement
        sline = None
        for line in (raw_dir / src["file"]).read_text().splitlines():
            r = json.loads(line)
            if r.get("bit") == src["bit"]:
                sline = r
        assert sline is not None, src["file"]
        assert (sline["loss"] is fresh_loss) and (sline["capped"] is False)
        assert git_blob_sha((raw_dir / src["file"]).read_bytes()) == src["pin"]
        canon_notes[bit] = {
            "source": f"{src['lane']} bit {src['bit']}",
            "source_file": src["file"],
            "source_verdict": "WIN7-D10" if sline["loss"] else "REFUTED-D10",
            "source_nodes": sline["nodes"],
            "fresh_nodes": mine[bit]["nodes"],
            "canon_equal": True,
            "raw_identical": (int(src["child"], 16) | (1 << src["bit"])) ==
                             (int(CHILD, 16) | (1 << bit)),
        }
    assert all(canon_notes[b]["raw_identical"] is False for b in canon_notes)

    # ------------------------------------------------ 3. determinism reruns
    det_notes = {}
    for det, orig in DET.items():
        la = [json.loads(l) for l in (raw_dir / orig).read_text().splitlines()]
        lb = [json.loads(l) for l in (raw_dir / det).read_text().splitlines()]
        assert len(la) == len(lb)
        for ra, rb in zip(la, lb):
            ka = {k: v for k, v in ra.items() if k != "ms"}
            kb = {k: v for k, v in rb.items() if k != "ms"}
            assert ka == kb, (det, ka, kb)
        det_notes[det] = {
            "lines": len(la),
            "heaviest_bit": max((r["bit"] for r in la
                                 if r.get("bit") is not None),
                                key=lambda b: mine[b]["nodes"]),
        }

    # ------------------------------------------------ 4. v15 cross-engine
    v15, v15_pilots, v15_total = {}, 0, 0
    for fname in V15:
        for line in (raw_dir / fname).read_text().splitlines():
            r = json.loads(line)
            if r.get("control"):
                assert r["nodes"] == 5949 and r["loss"] is False \
                    and r["capped"] is False, (fname, r)
                v15_pilots += 1
                continue
            assert r["loss"] is True and r["capped"] is False, (fname, r)
            assert r["bit"] not in v15
            v15[r["bit"]] = r["nodes"]
            v15_total += r["nodes"]
    assert v15_pilots == 4 and len(v15) == 34 and set(v15) == set(wins)

    # ------------------------------------------------ output
    out = {
        "schema": "n11-class2-lane-cost73l-raw-sweep-audit-20261117-v1",
        "date": "2026-11-17",
        "status": ("PASS: first fresh execution of the cost73l 73-bit v17 "
                   "depth-10 sweep (head-1473 census v8 rank-1 row); 34 "
                   "WIN7-D10 / 39 REFUTED-D10 / 0 capped; 7/7 confirmation "
                   "transfers with independent D4 canon re-derivation of both "
                   "sides (all canon-equal, none raw-identical), the bit 97 "
                   "pre-64h harvest source identified as cost64d bit 118 (the "
                   "only canon match among the published pre-64h raw batches); "
                   "det reruns of batches 1 and 4 field-identical; v15 "
                   "cross-engine 34/34 WIN"),
        "target": {
            "s6_child": CHILD,
            "stone_bits": [22, 49, 60, 63, 70, 71],
            "candidate_bits": 73,
            "open_bits": 66,
            "confirmation_bits": CONFIRM_BITS,
        },
        "provenance": {
            "original_run": ("this audit's raw files are the original claiming "
                             "session's own execution (no sandbox reset "
                             "intervened, no concurrent-session overlap "
                             "existed for this child at claim time); the raw "
                             "batch JSONLs, det rerun JSONLs and v15 "
                             "crosscheck JSONLs are published together with "
                             "this audit and the claim v2"),
            "engine": ("class4_child1_runner_v17.ts, git blob " + ENGINE_BLOB +
                       ", depth 10, cap 1e9 per bit, andclose 1, fresh engine "
                       "state per candidate bit"),
            "v15_engine": "class4_child1_runner.ts, git blob " + V15_BLOB,
            "batch_driver": ("scripts/ev73l_batches_20261117.sh (same batch "
                             "plan shape as the cost73k run: 7x9 + 1x3 open "
                             "bits + 1 confirmation batch of 7 bits)"),
        },
        "pilot_checks": "9/9 raw batches + 2/2 det reruns at pilot_d6 3402; "
                        "4/4 v15 chunks at pilot_d6 5949",
        "verdicts": {
            "win7_d10_bits": wins,
            "win7_d10_nodes": {str(b): mine[b]["nodes"] for b in wins},
            "refuted_d10_bits": refuted,
            "refuted_d10_count": len(refuted),
            "capped_count": capped,
            "candidate_nodes_total": node_sum,
            "total_nodes_including_pilots": node_sum + 9 * 3402,
            "terminal_stone_range": [13, 17],
            "terminal_stone_range_exceptions": {
                "91": [13, 15],
                "note": ("bit 91 (REFUTED-D10) closed the depth-10 search at "
                         "13-15 stones (early refutation, 24,376 nodes); the "
                         "other 72 bits closed at 13-17 stones"),
            },
            "heaviest_bit": 47,
            "heaviest_bit_nodes": 6045349,
        },
        "confirmation_bits": {
            "bits": CONFIRM_BITS,
            "fresh_vs_claim_transfers": "7/7",
            "canon_rederivation": "independent D4 canon function (copied "
                                  "verbatim from the published census v8 "
                                  "script, blob " + CENSUS_V8_SCRIPT_BLOB +
                                  "): canon(source_child|source_bit) == "
                                  "claim root_canon == canon(73l_child|bit), "
                                  "7/7",
            "sources": {str(b): canon_notes[b] for b in CONFIRM_BITS},
        },
        "determinism_rerun": {
            "batches": det_notes,
            "result": "field-identical on every non-ms field",
        },
        "v15_cross_engine_check": {
            "chunks": ["a", "b", "c", "d"],
            "win_agreement": "34/34 loss=true",
            "pilots": "4/4 at 5949",
            "capped": 0,
            "v15_nodes_total": v15_total,
        },
        "pins": {
            "claim_v1": V1_BLOB,
            "census_v8_script": CENSUS_V8_SCRIPT_BLOB,
            "census_v8_json": CENSUS_V8_JSON_BLOB,
            "engine_v17": ENGINE_BLOB,
            "engine_v15": V15_BLOB,
            "sources": {k: v["pin"] for k, v in SOURCES.items()},
            "raw_batches": {},
        },
        "interpretation_guard": (
            "engine-search verdicts for the 73 seven-stone roots of this child "
            "only. WIN7-D10 proves a first-player win within depth 10 from "
            "the individual 7-stone root only; REFUTED-D10 is not a LOSS "
            "proof; no manifest row is closed by this sweep. The 11x11 empty "
            "board, the two-stone roots {49,60} and {59,60}, S2 {59,60}, and "
            "classes 1/2/4 all remain UNKNOWN."),
    }
    for f in RAW + list(DET) + V15:
        out["pins"]["raw_batches"][f] = git_blob_sha((raw_dir / f).read_bytes())

    text = json.dumps(out, indent=1, ensure_ascii=True) + "\n"
    out_path.write_text(text)
    print(f"audit JSON written: {out_path} ({len(text)} bytes)")
    print("blob:", git_blob_sha(text.encode()))


if __name__ == "__main__":
    main()
