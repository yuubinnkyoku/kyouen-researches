#!/usr/bin/env python3
"""cost-64a v17 full-row re-check + census runner-up harvest-gap audit
(2026-11-17).

Background
----------
The past-lane v17 re-check queue (fbt-saturation repair re-runs of the
v16-era swept rows) covered 64d/64g/64f/76d/77e/65f/65j/65n/66c/58c but
cost-64a was NOT in it: its 64-bit sweep (child
00000000000000801282000040000000, STERILE, 64/64 REFUTED-D10, 38,157,151
nodes, v16 engine) predates the queue and no lane re-ran it.

Separately, the head-1452 presweep census v1 (and therefore the v3/v4
head-1472 overlays built on it) ranks this same child as the globally
cheapest remaining row ("runner-up", 55-56 open bits). The v1 harvest
ingested NO bit of the 64a sweep: the harvest glob pass skips
class2-lane-cost64a-inflight-20261116.json with reason "no win bits"
(the claim stores verdicts as sweep_result counts, not bit lists), and
unlike 64f/76d/77e/65f/65j there is no explicit raw-batch ingestion
pass for 64a. The census "open" statuses of this row are therefore
bookkeeping artifacts, not unswept bits.

This experiment closes both gaps in one record:
  1. fresh v17 (fbt-repaired, blob c132cc64...) full-row re-check of all
     64 legal bits (8 batches, batch partition identical to the published
     v16 raw batches) + determinism re-runs (batches 5 and 8);
  2. field-by-field v16-vs-v17 comparison (verdict / nodes / capped /
     terminal range), pilot controls, and a cross-source conflict scan
     against the four published verdict maps (64h/76c/66i/66j);
  3. quantification of the census gap: every "open" bit of the row is
     covered by the 64a REFUTED-D10 map, so the corrected census status
     of the row is swept/STERILE/open=0, which removes the v4 ranking's
     #1 row from candidacy.

Interpretation guard: REFUTED-D10 is NOT a LOSS proof. STERILE means
the row cannot be closed by depth-10 WIN7 receipts (K0863). No manifest
row is closed or changed by this record; head 1472 is untouched.
The 11x11 empty board, the two-stone roots {49,60}/{59,60}, S2 {59,60}
and classes 1/2/4 all remain UNKNOWN.
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

CHILD_HEX = "00000000000000801282000040000000"
CHILD = int(CHILD_HEX, 16)

PIN_V16 = {
    1: "650e56d1004616ada4dab4ad227377b002e2e015",
    2: "029698f2d34b6dee31e5b094b8c986b1315a4612",
    3: "25ef5c04db02895510c568569240cdca141d4040",
    4: "8906b5c150ee316253dbc0946dfd11d39b7b6641",
    5: "d49d20d8926da5d841279e7280fb3563fe6aee88",
    6: "ec67df84c32e4c7edeb64b95fb43780a9735306a",
    7: "edeac203b101d478dbf7a2e9e0c4ca952fa7778b",
    8: "579b44a1025310396e592164f08df8ffa2a842b2",
}
PIN_V17 = {
    1: "706ca61a517bc89213e69af6fff9f9c5e47c558a",
    2: "9bcd8eb276c738c95978bd71a3d2a34c16d50231",
    3: "80edf14b6d2cf9fa25d34a879a5fc23c1a461ae4",
    4: "e6497a8d9aa372dc86cac00df95ed78b5e0c05a1",
    5: "bf13850027cc55e0b8750a2071a0a7395cf78041",
    6: "aeaf87ea29d0f30a00da44ce399e68bb42ca40a1",
    7: "51b6c685612ea3c85caf8c3498bcf3049edaa979",
    8: "e9db9ef64c16ec71b9d9b7b33c5a6e2125e0d3ab",
}
PIN_DET = {
    5: "d3d35e830f723d54b91bf83c1cffe34ab0fb34e2",
    8: "9e38cf95f8f14862510d125ff86641d7f678f9d8",
}
PIN_V1_CENSUS = "0d9a94a272de9fe45708757f17bfea60239a3c9b"
PIN_V4_CENSUS = "d70eae093e80d19660eae314bd761c21085995bb"
PIN_V4_SCRIPT = "902cd56b0542cd12e7afa8227692827e62241e55"
PIN_CLAIM64A = "08551cd0716b3655f03ddb2256bef942c1f89ab6"
PIN_V17_ENGINE = "c132cc6425eee3feaeef1d697dd74f968cfedb59"

OUTPUT_JSON = OUT / "class2-lane-cost64a-v17-full-row-recheck-20261117.json"


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def load_jsonl(name, pin):
    b = (OUT / name).read_bytes()
    got = git_blob_sha(b)
    assert got == pin, (name, got, pin)
    return [json.loads(l) for l in b.decode().splitlines() if l.strip()]


def load_out(name, pin):
    b = (OUT / name).read_bytes()
    got = git_blob_sha(b)
    assert got == pin, (name, got, pin)
    return json.loads(b)


def build_map(prefix, pins, datestr):
    """Build the per-bit verdict map from raw batch files."""
    vmap = {}
    pilots = 0
    for i in sorted(pins):
        rows = load_jsonl(f"{prefix}{i}-{datestr}.jsonl", pins[i])
        for r in rows:
            if r.get("control") == "pilot_d6":
                assert r == {"control": "pilot_d6", "loss": False,
                             "nodes": 3402, "capped": False}, r
                pilots += 1
                continue
            assert r["capped"] is False, r
            assert r["terminalStoneRange"] == [13, 17], r
            b = r["bit"]
            assert b not in vmap, ("duplicate bit", b)
            vmap[b] = {"verdict": "WIN7-D10" if r["loss"] else "REFUTED-D10",
                       "nodes": r["nodes"], "ms": r.get("ms"),
                       "andclose": r.get("andclose")}
    return vmap, pilots


def main():
    # ---------- 0. verify the fresh-sweep engine + census inputs (pinned)
    assert git_blob_sha((SCRIPTS / "class4_child1_runner_v17.ts")
                        .read_bytes()) == PIN_V17_ENGINE

    # four published verdict maps + D4 canon, from the v4 census head
    v4_path = SCRIPTS / "next_target_presweep_head1472_v4_20261117.py"
    assert git_blob_sha(v4_path.read_bytes()) == PIN_V4_SCRIPT
    src = v4_path.read_text()
    head = src.split("# ------------------------------------------------ "
                    "family overlay")[0]
    ns = {"__file__": str(v4_path)}
    exec(compile(head, "v4head", "exec"), ns)
    canon = ns["canon"]
    maps = ns["maps"]

    v1 = load_out("class2-lane-next-target-presweep-1452-20261116.json",
                  PIN_V1_CENSUS)
    v4 = load_out(
        "class2-lane-next-target-presweep-1472-v4-20261117.json",
        PIN_V4_CENSUS)
    claim = load_out("class2-lane-cost64a-inflight-20261116.json",
                    PIN_CLAIM64A)
    assert claim["s6_child"] == CHILD_HEX
    assert claim["s6_s7_edge_cost"] == 64
    assert claim["demand"] == {"c1": 1, "c2": 1, "c4": 0}
    assert claim["sweep_result"]["win7_d10"] == 0
    assert claim["sweep_result"]["refuted_d10"] == 64
    assert claim["sweep_result"]["capped"] == 0
    assert claim["sweep_result"]["candidates"] == 64
    assert claim["sweep_result"]["candidate_nodes"] == 38157151

    # ---------- 1. legal candidate set (independent enumeration)
    stones, bits = legal_candidates(CHILD_HEX)
    assert sorted(stones) == sorted(claim["child_stones_bit_indices"])
    assert len(bits) == 64 and sorted(bits) == sorted(
        claim["legal_candidates"])

    # ---------- 2. v16 (published) and v17 (fresh) verdict maps
    v16, pilots16 = build_map("class2-lane-cost64a-raw-batch", PIN_V16,
                              "20261116")
    v17, pilots17 = build_map("class2-lane-cost64a-v17-recheck-batch", PIN_V17,
                              "20261117")
    assert pilots16 == 8 and pilots17 == 8
    assert sorted(v16) == sorted(bits) and sorted(v17) == sorted(bits)
    assert all(e["verdict"] == "REFUTED-D10" for e in v16.values())
    assert all(e["verdict"] == "REFUTED-D10" for e in v17.values())
    t16 = sum(e["nodes"] for e in v16.values())
    t17 = sum(e["nodes"] for e in v17.values())
    assert t16 == 38157151, t16

    # ---------- 3. v16 vs v17 field comparison
    flips = [b for b in v17 if v16[b]["verdict"] != v17[b]["verdict"]]
    node_exact = [b for b in v17 if v16[b]["nodes"] == v17[b]["nodes"]]
    corrections = [{"bit": b, "v16_nodes": v16[b]["nodes"],
                    "v17_nodes": v17[b]["nodes"],
                    "delta": v17[b]["nodes"] - v16[b]["nodes"]}
                   for b in sorted(v17) if v16[b]["nodes"] != v17[b]["nodes"]]
    assert flips == [], flips
    assert len(node_exact) == 63, len(node_exact)
    assert corrections == [{"bit": 87, "v16_nodes": 2102913,
                            "v17_nodes": 2101158, "delta": -1755}], corrections

    # ---------- 4. determinism re-runs (batches 5 and 8)
    det = {}
    for n, pin in PIN_DET.items():
        rows = load_jsonl(f"class2-lane-cost64a-v17-det-batch{n}-20261117.jsonl",
                          pin)
        for r in rows:
            if r.get("control") == "pilot_d6":
                assert r == {"control": "pilot_d6", "loss": False,
                             "nodes": 3402, "capped": False}
                continue
            det[r["bit"]] = r
    det_bits = sorted(det)
    assert det_bits == sorted(
        b for b in v17 if b in det) and len(det) == 16
    for b, r in det.items():
        for f in ("loss", "nodes", "capped", "terminalStoneRange"):
            assert r[f] == {"loss": v17[b]["verdict"] == "WIN7-D10",
                            "nodes": v17[b]["nodes"],
                            "capped": False,
                            "terminalStoneRange": [13, 17]}[f], (b, f)

    # ---------- 5. cross-source conflict scan (four published maps)
    overlap = {}
    conflicts = []
    for b in sorted(v17):
        c = canon(CHILD | (1 << b))
        src_map = None
        for name, mp in maps.items():
            if c in mp:
                src_map = name
                break
        if src_map is not None:
            overlap[b] = src_map
            if maps[src_map][c]["verdict"] != "REFUTED-D10":
                conflicts.append((b, src_map, maps[src_map][c]["verdict"]))
    assert conflicts == [], conflicts

    # ---------- 6. census gap quantification
    tbl = v1["bit_tables"][CHILD_HEX]
    st = {x["bit"]: x for x in tbl["bits"]}
    assert len(st) == 64
    status_counts = {}
    for x in tbl["bits"]:
        status_counts[x["status"]] = status_counts.get(x["status"], 0) + 1
    assert status_counts == {"open": 56, "harvested_refuted": 8}, \
        status_counts
    # every census bit of this row is covered by the 64a REFUTED map;
    # the bit-table root_canon values must agree with the D4 canon
    for b, x in st.items():
        assert x["root_canon"] == f"{canon(CHILD | (1 << b)):032x}", b
        assert v17[b]["verdict"] == "REFUTED-D10", b
    # the harvest skip of the 64a claim is on the record in the census
    skip = dict((s[0], s[1]) for s in v1["harvest"]["skipped"])
    assert skip["class2-lane-cost64a-inflight-20261116.json"] == \
        "no win bits"
    # no harvest file carries this child (no other source covers it)
    assert not any(f["child"] == CHILD_HEX
                  for f in v1["harvest"]["files"])

    # ---------- 7. v4 ranking correction
    ranking = v4["ranking_top10"]
    assert ranking[0]["s6_hex"] == CHILD_HEX, ranking[0]["s6_hex"]
    assert ranking[0]["cost"] == 64
    assert ranking[0]["open_after_census_v4"] == 55
    sel = v4["selected_target"]
    remaining = [r for r in ranking[1:]]

    result = {
        "schema": "n11-class2-lane-cost64a-v17-full-row-recheck-20261117",
        "date": "2026-11-17",
        "status": ("completed: v17 full-row re-check 64/64 REFUTED-D10, "
                   "verdict flips 0, node-exact 63/64 (bit 87 -1755), "
                   "determinism 16/16, census runner-up harvest-gap "
                   "confirmed and corrected; row is swept STERILE; "
                   "11x11 UNKNOWN"),
        "target": {
            "s5": claim["s5"],
            "s6_child": CHILD_HEX,
            "s6_s7_edge_cost": 64,
            "demand": {"c1": 1, "c2": 1, "c4": 0},
            "legal_candidate_count": 64,
            "engine": "class4_child1_runner_v17.ts (git blob "
                      "c132cc6425eee3feaeef1d697dd74f968cfedb59, "
                      "fbt-saturation-repaired)",
            "depth": 10,
            "cap": 1000000000,
            "andclose": 1,
        },
        "v16_published": {
            "source": "class2-lane-cost64a-raw-batch{1..8}-20261116.jsonl "
                      "(git blob sha pinned in this record)",
            "verdicts": {"win7_d10": 0, "refuted_d10": 64, "capped": 0},
            "candidate_nodes": t16,
            "pilots": "3402 x8",
            "claim_blob": PIN_CLAIM64A,
        },
        "v17_recheck": {
            "source": "class2-lane-cost64a-v17-recheck-batch{1..8}-"
                      "20261117.jsonl (git blob sha pinned in this record)",
            "verdicts": {"win7_d10": 0, "refuted_d10": 64, "capped": 0},
            "candidate_nodes": t17,
            "pilots": "3402 x8",
            "terminal_ranges": "[13,17] only",
            "batch_partition": "identical to the published v16 raw batches",
            "wall_time_note": "single sandbox, 2 concurrent node "
                              "processes (nproc=2)",
        },
        "v16_vs_v17": {
            "verdict_flips": flips,
            "node_exact_bits": len(node_exact),
            "node_corrections": corrections,
            "total_nodes_v16": t16,
            "total_nodes_v17": t17,
            "total_delta": t17 - t16,
            "note": "bit 87 is the only fbt-saturation node correction "
                    "(-1755 nodes, -0.08%); v17 engine-corrected total "
                    "for this row is 38,155,396",
        },
        "determinism": {
            "batches": [5, 8],
            "result": "field-identical on loss/nodes/capped/"
                      "terminalStoneRange for all 16 bits",
        },
        "cross_source_conflict_scan": {
            "maps_scanned": sorted(maps),
            "overlap_bits_in_new_sweeps": sorted(overlap),
            "conflicts": conflicts,
        },
        "census_harvest_gap": {
            "finding": ("the head-1452 census v1 bit table marks this "
                        "row open=56 / harvested_refuted=8, but all 64 "
                        "legal bits are REFUTED-D10 in the published "
                        "cost-64a sweep; the corrected status is "
                        "swept, STERILE, open=0"),
            "root_cause": ("the v1 harvest glob pass skips "
                           "class2-lane-cost64a-inflight-20261116.json "
                           "with reason 'no win bits' (the claim stores "
                           "verdicts as sweep_result counts, not bit "
                           "lists) and there is no explicit raw-batch "
                           "ingestion pass for 64a, unlike "
                           "64f/76d/77e/65f/65j"),
            "v1_bit_table_status_counts": status_counts,
            "corrected_status_counts": {"open": 0,
                                        "harvested_refuted": 8,
                                        "refuted_via_cost64a_v17": 56},
            "v4_ranking_consequence": (
                "census v4 ranking_top10[0] is this child (cost 64, 55 "
                "open): a false-open row. Removing it, the cheapest "
                "remaining unclaimed rows are ranking[1] "
                "00000000000000403800000008000020 (cost 69, the in-flight "
                "cost-69j target) and then ranking[2] "
                "00000000000000c09002000000002000 (cost 71, 70 open, "
                "demand c2=2/c4=2), subject to the v4 selection policy "
                "(fold-pending exclusions); the definitive next-target "
                "selection belongs to the next census run with the 64a "
                "verdict map ingested"),
            "family_consequence": (
                "family 00000000000000801202000040000000 (S5) can only be "
                "closed through its cost-76 child 0000000001000080909200"
                "0001000000 (WIN7-D10 bits {61,99}, fold pending on the "
                "parallel lane); the cost-71 sibling is also STERILE "
                "(71/71 REFUTED-D10, K0863)"),
            "rows_affected_in_v1_bit_tables": 1,
            "other_open_rows_check": (
                "none of the other 12 census open rows matches a "
                "skipped claim file's child: the only other swept "
                "children among them (64h/76c/66i/66j/69j) are handled "
                "by the v2/v3/v4 overlays or are the active 69j claim"),
        },
        "verdict_semantics": ("loss=false && !capped => REFUTED-D10, no "
                              "first-player win within depth 10 (NOT a "
                              "LOSS proof); STERILE => the row cannot be "
                              "closed by depth-10 WIN7 receipts"),
        "interpretation_guard": ("no manifest row is closed or changed; "
                                 "head 1472 untouched; solved counts are "
                                 "manifest-coverage bookkeeping"),
        "unknown_status": ("11x11 empty board: UNKNOWN. The two-stone "
                           "roots {49,60} and {59,60}, S2 {59,60} and "
                           "classes 1/2/4 remain UNKNOWN."),
    }

    data = json.dumps(result, indent=2, sort_keys=True) + "\n"
    OUTPUT_JSON.write_text(data)
    print(f"written {OUTPUT_JSON.name}: {len(data.encode())} bytes, "
          f"md5 {hashlib.md5(data.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
