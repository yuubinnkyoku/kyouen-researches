#!/usr/bin/env python3
"""Generate the cost-69j inflight claim v1 (preregistration) from the
published head-1472 presweep census v4 and the four blob-pinned verdict
maps. No search is run here; the claim is pushed BEFORE the sweep starts.

Interpretation guard: this is a search-plan preregistration only. The
11x11 empty board, the two-stone roots {49,60}/{59,60}, S2 {59,60} and
classes 1/2/4 all remain UNKNOWN.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SCRIPTS = HERE / "scripts"
OUT = HERE / "output"
sys.path.insert(0, str(SCRIPTS))
from legal_candidates import legal_candidates  # noqa: E402

V4_JSON = OUT / "class2-lane-next-target-presweep-1472-v4-20261117.json"
V4_BLOB = "d70eae093e80d19660eae314bd761c21085995bb"
V4_SCRIPT = SCRIPTS / "next_target_presweep_head1472_v4_20261117.py"
V4_SCRIPT_BLOB = "902cd56b0542cd12e7afa8227692827e62241e55"
OUTPUT_JSON = OUT / "class2-lane-cost69j-inflight-20261117.json"


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main():
    assert git_blob_sha(V4_JSON.read_bytes()) == V4_BLOB
    assert git_blob_sha(V4_SCRIPT.read_bytes()) == V4_SCRIPT_BLOB
    v4 = json.loads(V4_JSON.read_text())
    sel = v4["selected_target"]
    target = sel["s6_hex"]
    assert target == "00000000000000403800000008000020", target
    assert sel["parent"] == "00000000000000403800000008000000"
    assert sel["cost"] == 69
    assert sel["demand"] == {"c1": 1, "c2": 1, "c4": 0}

    # rebuild the four verdict maps + canon from the v4 script head
    src = V4_SCRIPT.read_text()
    head = src.split("# ------------------------------------------------ family overlay")[0]
    ns = {"__file__": str(V4_SCRIPT)}
    exec(compile(head, "v4head", "exec"), ns)
    canon = ns["canon"]
    maps = ns["maps"]

    bits = sorted(legal_candidates(target)[1])
    assert len(bits) == 69, len(bits)
    assert sorted(sel["sweep_bits"]) + [] == sorted(
        set(bits) - set(sel["confirmation_bits"]))
    sweep_bits = sel["sweep_bits"]
    confirm_bits = sel["confirmation_bits"]
    assert len(sweep_bits) == 59 and len(confirm_bits) == 10
    assert sorted(sweep_bits + confirm_bits) == bits

    # v1 census bit-table statuses for the confirmation transfers
    v1 = json.loads(
        (OUT / "class2-lane-next-target-presweep-1452-20261116.json").read_text())
    tbl = v1["bit_tables"][target]
    st = {x["bit"]: x for x in tbl["bits"]}

    transfers = {}
    expected = {}
    for b in sorted(confirm_bits):
        c = canon(int(target, 16) | (1 << b))
        assert st[b]["root_canon"] == f"{c:032x}", b
        src_map = None
        for name, mp in maps.items():
            if c in mp:
                src_map = name
                break
        if src_map is not None:
            e = maps[src_map][c]
            assert e["verdict"] == "REFUTED-D10", (b, e)
            engine_bit = e["bit"]
            kind = {
                "cost64h": f"cost-64h orbit transfer (64h bit {engine_bit}, "
                           f"{e['nodes']} nodes, v16 raw batch map)",
                "cost76c": f"cost-76c orbit transfer (76c bit {engine_bit}, "
                           f"{e['nodes']} nodes, v17 raw batch map)",
                "cost66i": f"cost-66i orbit transfer (66i bit {engine_bit}, "
                           f"{e['nodes']} nodes, v17 raw batch map)",
                "cost66j": f"cost-66j orbit transfer (66j bit {engine_bit}, "
                           f"{e['nodes']} nodes, v17 raw batch map)",
            }[src_map]
        else:
            assert st[b]["status"] == "harvested_refuted", (b, st[b])
            kind = ("v1 harvest transfer (head-1452 census bit table "
                    "status harvested_refuted)")
        transfers[str(b)] = {
            "root_canon": f"{c:032x}",
            "verdict": "REFUTED-D10",
            "kind": kind,
        }
        expected[str(b)] = "REFUTED-D10"

    # batch plan: 8 sweep batches (5x8 + 7 + 7 + 5 = 59) + 2 confirmation
    chunks = [sweep_bits[0:8], sweep_bits[8:16], sweep_bits[16:24],
              sweep_bits[24:32], sweep_bits[32:40], sweep_bits[40:47],
              sweep_bits[47:54], sweep_bits[54:59]]
    assert sum(len(c) for c in chunks) == 59
    batches = [{"batch": i + 1, "bits": c, "kind": "sweep"}
               for i, c in enumerate(chunks)]
    batches.append({"batch": 9, "bits": [13, 17, 19, 20, 91],
                    "kind": "confirmation"})
    batches.append({"batch": 10, "bits": [95, 103, 108, 111, 119],
                    "kind": "confirmation"})

    claim = {
        "schema": "n11-class2-lane-cost69j-inflight-20261117-v1",
        "date": "2026-11-17",
        "last_updated": "2026-11-17",
        "title": ("n11 class2-lane cost69j: planned fresh 69-bit depth-10 "
                  "sweep of the cheapest remaining unswept/unclaimed row of "
                  "the primary pure class-2 target family (head-1472 "
                  "presweep census v4 selection)"),
        "status": ("claim v1: preregistered 69-bit fresh v17 depth-10 sweep "
                   "plan for the head-1472 census v4 selected target "
                   "00000000000000403800000008000020 (cost 69, primary "
                   "family, demand c1=1/c2=1; 59 fresh sweep bits + 10 "
                   "confirmation transfers, all expected REFUTED-D10); "
                   "sweep not yet started; runner-up and the pending "
                   "76c/66i/66j folds untouched; 11x11 remains UNKNOWN"),
        "s5": "00000000000000403800000008000000",
        "s6_child": "00000000000000403800000008000020",
        "s6_s7_edge_cost": 69,
        "child_stones_bit_indices": [5, 27, 59, 60, 61, 70],
        "demand": {"c1": 1, "c2": 1, "c4": 0},
        "demand_verification": (
            "row demand c1=1/c2=1 carried over from the published head-1452 "
            "v1 census bit/row tables through the head-1472 presweep "
            "censuses v3/v4 (class2-lane-next-target-presweep-1472-v4-"
            "20261117.json, git blob d70eae093e80d19660eae314bd761c21085995bb), "
            "unchanged by the 64h/76c/66i/66j overlay; this row serves both "
            "a class-1 and a class-2 parent demand"),
        "candidate_count": 69,
        "legal_candidates": bits,
        "engine": {
            "script": ("research/experiments/n11-s2-5960-ms5-s7-reuse-"
                       "20261113/scripts/class4_child1_runner_v17.ts"),
            "blob_sha": "c132cc6425eee3feaeef1d697dd74f968cfedb59",
            "note": ("v17 = the fbt-saturation-repaired engine used for the "
                     "cost-76c resweep and the cost-66i/cost-66j sweeps; "
                     "fresh sweeps must use v17, not v16"),
            "depth": 10,
            "cap": 1000000000,
            "andclose": 1,
            "pilot": ("pilot d6 control per batch: loss=false at exactly "
                      "3402 nodes, else abort"),
            "parallelism": ("sequential node processes (shared-server "
                            "courtesy; this sandbox is capped at ~1 CPU)"),
            "raw_output_pattern":
                "class2-lane-cost69j-raw-batch{n}-20261117.jsonl",
            "batches": batches,
        },
        "engine_candidate_bits": {
            "open_bits": sweep_bits,
            "confirmation_bits": confirm_bits,
            "expected_verdicts": expected,
            "note": ("59 fresh open bits plus 10 known-verdict bits re-run "
                     "fresh for cross-agreement (7 v1 harvest transfers; "
                     "bit 20 = cost-64h orbit transfer; bit 103 = cost-66i "
                     "orbit transfer; bit 108 = cost-66j orbit transfer); "
                     "total fresh bits run = 69 = all legal candidates"),
        },
        "transfers": transfers,
        "basis": {
            "census_v4_json": (
                "class2-lane-next-target-presweep-1472-v4-20261117.json "
                "(git blob d70eae093e80d19660eae314bd761c21085995bb)"),
            "census_v4_script": (
                "next_target_presweep_head1472_v4_20261117.py (git blob "
                "902cd56b0542cd12e7afa8227692827e62241e55)"),
            "selection": ("cheapest remaining unswept/unclaimed/unexcluded "
                          "row of the primary pure class-2 target family "
                          "00000000000000403800000008000000 at head 1472 "
                          "after the landed cost-64h fold closure and the "
                          "66j sweep overlay, excluding the four swept "
                          "children (64h/76c/66i/66j) and every row pending "
                          "the 76c/66i/66j folds; runner-up "
                          "00000000000000801282000040000000 (cost 64, 55 "
                          "open, STERILE-family caveat) is recorded in the "
                          "census v4 ranking but not claimed"),
        },
        "basis_head": ("1472/174/6376/504672/4649/368586 (canonical head "
                       "after the LANDED cost-64h receipt fold; the "
                       "cost-76c, cost-66i and cost-66j folds are still "
                       "pending and are excluded by the v4 overlay, not "
                       "assumed)"),
        "claimed_by": "n11 long-term lane session (head-1472 presweep census v4 selector)",
        "coordination_note": (
            "latest main fetched immediately before this push; no claim, "
            "raw batch or audit exists for this child on main (searched: "
            "child hex 00000000000000403800000008000020, cost69j; GitHub "
            "code search 0 hits for cost69j); the parallel lane holds the "
            "pending cost-76c fold (bit 61 certificate in flight), the "
            "cost-66i receipt fold behind it and the cost-66j receipt fold "
            "behind those; this claim does not touch any fold; the "
            "vertical-fiber lanes (K0881/K0886) are on unrelated paths"),
        "planned_controls": {
            "determinism_rerun": ("one batch re-run byte-compare on nodes "
                                  "(ms-only differences allowed): the "
                                  "heaviest batch and, if any WIN bit "
                                  "appears, a batch containing a WIN bit"),
            "v15_crosscheck": ("independent v15 engine (blob 8744fc65b6b7"
                               "cac6bd561403ce4c749e01c51359) re-check of "
                               "all WIN bits plus anchor bits (pilot 5949), "
                               "verdict agreement required"),
            "independent_audit": ("stdlib-only re-audit of all raw batch "
                                  "lines (pilot exactness, cap, stone "
                                  "counts, canon recomputation from the "
                                  "child, cross-sweep conflict scan against "
                                  "the 64h/76c/66i/66j verdict maps) before "
                                  "any verdict is treated as established"),
        },
        "next_action": ("run the 10 planned v17 batches (8 sweep batches + 2 "
                        "confirmation batches), publish the raw JSONL "
                        "batches, then the stdlib-only raw audit; on WIN "
                        "bits extract certificates, verify independently, "
                        "then wait behind the 76c/66i/66j folds before any "
                        "receipt fold of this row"),
        "receipt_fold": {
            "status": "pending behind the cost-76c, cost-66i and cost-66j folds",
            "note": ("any WIN7-D10 certificates of this row fold only after "
                     "the pending cost-76c, cost-66i and cost-66j folds "
                     "land; no manifest row is closed by the sweep itself"),
        },
        "verdict_semantics": ("loss=true => WIN7-within-depth-10 candidate "
                              "(certificate rebuild target); loss=false && "
                              "!capped => REFUTED-D10, no first-player win "
                              "within depth 10 (NOT a LOSS proof of the "
                              "position); capped => proves nothing either "
                              "way"),
        "unknown_status": ("11x11 empty board: UNKNOWN. A completed sweep "
                           "proves only WIN7-D10/REFUTED-D10 verdicts for "
                           "the 7-stone roots of this child. The two-stone "
                           "roots {49,60} and {59,60}, S2 {59,60} and "
                           "classes 1/2/4 remain UNKNOWN."),
    }
    OUTPUT_JSON.write_text(
        json.dumps(claim, indent=2, sort_keys=False) + "\n",
        encoding="utf-8")
    print("wrote", OUTPUT_JSON.name, OUTPUT_JSON.stat().st_size, "bytes")
    print("target:", target, "sweep", len(sweep_bits),
          "confirm", confirm_bits)
    for b in batches:
        print(" batch", b["batch"], b["kind"], len(b["bits"]), "bits")


if __name__ == "__main__":
    main()
