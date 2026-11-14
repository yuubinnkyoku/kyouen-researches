#!/usr/bin/env python3
"""Audit the parallel class-2 frontier union and the cost-65e bit-107 receipt."""
import csv
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
MANIFEST_DIR = HERE.parent / "n11-s2-5960-milestone5-20261112" / "output"

def load(name):
    return json.loads((OUT / name).read_text())

def stones(hex_value):
    value = int(hex_value, 16)
    return [i for i in range(121) if (value >> i) & 1]

PERMS = list(itertools.permutations(range(4)))
def det4(indices):
    rows = []
    for i in indices:
        x, y = i % 11, i // 11
        rows.append((x*x + y*y, x, y, 1))
    total = 0
    for p in PERMS:
        inversions = sum(p[i] > p[j] for i in range(4)
                         for j in range(i+1, 4))
        product = 1
        for i in range(4):
            product *= rows[i][p[i]]
        total += -product if inversions % 2 else product
    return total

def safe(position):
    return all(det4(q) != 0 for q in itertools.combinations(position, 4))

def legal_bits(position):
    occupied = set(position)
    return [i for i in range(121)
            if i not in occupied and safe(position + [i])]

def root_geometry(hex_value):
    position = stones(hex_value)
    assert len(position) == 7 and safe(position)
    return {"stones": len(position), "safe": True,
            "legal_moves": len(legal_bits(position))}

def transform(mask, fn):
    out = 0
    for i in range(121):
        if (mask >> i) & 1:
            x, y = i % 11, i // 11
            u, v = fn(x, y)
            out |= 1 << (v*11 + u)
    return out

SYMMETRIES = [
    lambda x,y: (x,y), lambda x,y: (10-y,x),
    lambda x,y: (10-x,10-y), lambda x,y: (y,10-x),
    lambda x,y: (10-x,y), lambda x,y: (10-y,10-x),
    lambda x,y: (x,10-y), lambda x,y: (y,x),
]

def canonical_s6(mask):
    return f"{min(transform(mask, f) for f in SYMMETRIES):032x}"

def audit_sweep(name, batches, pilot_nodes):
    claim = load(f"class2-lane-{name}-inflight-20261114.json")
    summary = load(f"class2-lane-{name}-sweep-20261114.json")
    all_rows, bits, batch_summary = [], [], []
    for batch in range(1, batches+1):
        path = OUT / f"class2-lane-{name}-raw-batch{batch}-20261114.jsonl"
        parsed = [json.loads(line) for line in path.read_text().splitlines()
                  if line.strip()]
        pilots = [r for r in parsed if r.get("control") == "pilot_d6"]
        rows = [r for r in parsed if "bit" in r]
        assert len(pilots) == 1
        assert pilots[0] == {
            "control": "pilot_d6", "loss": False,
            "nodes": pilot_nodes, "capped": False
        }
        bits.extend(r["bit"] for r in rows)
        all_rows.extend(rows)
        batch_summary.append({
            "batch": batch, "candidates": len(rows),
            "win7_d10_bits": [r["bit"] for r in rows if r["loss"] is True],
            "refuted_d10": sum(r["loss"] is False and not r["capped"]
                               for r in rows),
            "capped": sum(bool(r["capped"]) for r in rows),
            "nodes": sum(r["nodes"] for r in rows),
        })

    parent = stones(claim["s6_child"])
    independently_legal = legal_bits(parent)
    assert len(parent) == 6 and safe(parent)
    assert independently_legal == claim["candidate_bits"]
    assert bits == claim["candidate_bits"]
    assert len(bits) == len(set(bits))
    assert all(r["capped"] is False for r in all_rows)
    assert all(r["terminalStoneRange"] == [13,17] for r in all_rows)
    assert all(r["andclose"] is True for r in all_rows)

    wins = [r for r in all_rows if r["loss"] is True]
    refuted = [r for r in all_rows if r["loss"] is False and not r["capped"]]
    assert len(wins) == summary["win7_d10"]
    assert len(refuted) == summary["refuted_d10"]
    assert sum(r["nodes"] for r in all_rows) == summary["total_nodes"]
    assert summary["capped"] == 0
    assert len(all_rows) == claim["legal_candidates_total"]

    return {
        "s5": claim["s5"], "s6_child": claim["s6_child"],
        "edge_cost": claim["s6_s7_edge_cost"], "engine": claim["engine"],
        "geometry": {
            "parent_safe": True, "independent_legal_count": len(independently_legal),
            "declared_legal_count": len(claim["candidate_bits"]),
            "exact_candidate_set_match": True,
            "method": "24-term permutation expansion of exact integer det([x^2+y^2,x,y,1])",
        },
        "candidates": len(all_rows), "win7_d10": len(wins),
        "win7_bits": [r["bit"] for r in wins],
        "refuted_d10": len(refuted), "capped": 0,
        "total_nodes": sum(r["nodes"] for r in all_rows),
        "pilot_nodes": pilot_nodes, "pilot_batches": batches,
        "terminal_range_all_13_17": True, "andclose_all": True,
        "fbt_drop_field_in_raw": any("fbtDrops" in r for r in all_rows),
        "batches": batch_summary,
    }

# Reconstruct the 7,867-row S6 manifest.
manifest = {}
for part in range(1, 7):
    path = MANIFEST_DIR / f"ms5_s6_manifest_part{part}.csv"
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            key = row["hex"]
            assert key not in manifest
            manifest[key] = {"cost": int(row["cost"]),
                             "classes": int(row["classes"])}
assert len(manifest) == 7867

f63 = load("class-frontier-cost63a-recompute-20261114.json")
f61e = load("class-frontier-cost61e-recompute-20261114.json")
f61f = load("class-frontier-cost61f-recompute-20261114.json")
base63 = f63["controls"]["after_cost61d"]
base61e = f61e["controls"]["after_cost61d"]
base61f = f61f["controls"]["after_cost61e"]
assert base63 == base61e == {
    "solved_in_manifest": 951, "unique_remaining": 6896,
    "sum_cost": 542952, "open_s6": 5166, "open_cost": 406675,
    "reproduced": True,
}
after61e = f61e["frontier_after_cost61e"]
assert base61f == {
    "solved_in_manifest": 954, "unique_remaining": 6893,
    "sum_cost": 542756, "open_s6": 5163, "open_cost": 406479,
    "reproduced": True,
}

def marginal(output, key):
    return {h for item in output[key].values()
            for h in item["marginal_manifest_hexes"]}

m63 = marginal(f63, "cost63a_addition")
m61e = marginal(f61e, "cost61e_addition")
m61f = marginal(f61f, "cost61f_addition")
assert (len(m63), len(m61e), len(m61f)) == (2,3,5)
assert not (m63 & m61e or m63 & m61f or m61e & m61f)
union = m63 | m61e | m61f
assert len(union) == 10 and union <= manifest.keys()
union_cost = sum(manifest[h]["cost"] for h in union)
assert union_cost == 660

frontier = {
    "solved_s6_in_manifest": base63["solved_in_manifest"] + len(union),
    "unique_remaining_s6": base63["unique_remaining"] - len(union),
    "sum_remaining_cost": base63["sum_cost"] - union_cost,
    "s6_needed_by_open_classes": base63["open_s6"] - len(union),
    "cost_needed_by_open_classes": base63["open_cost"] - union_cost,
}
assert frontier == {
    "solved_s6_in_manifest": 961, "unique_remaining_s6": 6886,
    "sum_remaining_cost": 542292, "s6_needed_by_open_classes": 5156,
    "cost_needed_by_open_classes": 406015,
}

# Check the published WIN7 roots by a separate exact geometry implementation.
sw65 = load("class2-lane-cost65e-sweep-20261114.json")
cert65 = load("class2-lane-cost65e-win7-certificates-20261114.json")
sw61 = load("class2-lane-cost61f-sweep-20261114.json")
cert61 = load("class2-lane-cost61f-win7-certificates-20261114.json")

for cert in cert61["certificates"]:
    geom = root_geometry(cert["root_hex"])
    assert geom["legal_moves"] == cert["root_check"]["loser_mobility"]
    assert geom["legal_moves"] == cert["sub_roots_pass"]
    assert cert["union_missing"] == 0 and cert["union_extra"] == 0

bit107 = cert65["certificates"][0]
assert bit107["bit"] == 107
assert bit107["root_hex"] == "00000800000000809102000000800000"
assert int(bit107["root_hex"],16) == int(cert65["child_hex"],16) | (1 << 107)
geom107 = root_geometry(bit107["root_hex"])
assert geom107["legal_moves"] == 44
assert bit107["sub_roots_pass"] == 44
assert bit107["union_missing"] == 0 and bit107["union_extra"] == 0
assert sw65["certificate"]["bit"] == 107
assert sw65["certificate"]["fbt_drops"] == 0

# Lift all seven parents of the cost-65e bit-107 root to D4-canonical S6 keys.
root = int(bit107["root_hex"],16)
parent_rows = []
for bit in stones(bit107["root_hex"]):
    parent = root ^ (1 << bit)
    key = canonical_s6(parent)
    entry = manifest.get(key)
    parent_rows.append({
        "removed_bit": bit, "canonical_s6": key,
        "in_manifest": entry is not None,
        "cost": entry["cost"] if entry else None,
        "classes": entry["classes"] if entry else None,
        "in_three_lane_union": key in union,
    })
target = canonical_s6(int(cert65["child_hex"],16))
target_entry = manifest[target]
assert target_entry == {"cost":65,"classes":2}
assert any(r["canonical_s6"] == target and r["in_manifest"] for r in parent_rows)
assert target not in union
assert sum(r["in_manifest"] for r in parent_rows) == 4

# The cost-65e S5 target has 37/2,658 after cost-63a; cost-61e/61f
# leave that target at 38/2,721 on their parallel baseline.
s5 = "00000000000000809102000000000000"
t63 = next(x for x in f63["frontier_after_cost63a"]["next_class2"]
           if x["s5_hex"] == s5)
t61e = next(x for x in f61e["frontier_after_cost61e"]["next_class2"]
            if x["s5_hex"] == s5)
t61f = next(x for x in f61f["frontier_after_cost61f"]["next_class2"]
            if x["s5_hex"] == s5)
assert (t63["remaining_s6_orbits"],t63["remaining_s7_edge_cost"]) == (37,2658)
assert (t61e["remaining_s6_orbits"],t61e["remaining_s7_edge_cost"]) == (38,2721)
assert (t61f["remaining_s6_orbits"],t61f["remaining_s7_edge_cost"]) == (38,2721)
local_after = {"remaining_s6_orbits":36,"remaining_s7_edge_cost":2593}

# Only the target parent is known to be new against the three-lane union.
# Do not count the other three manifest parents without a solved-set merge.
lower_bound = {
    "solved_s6_in_manifest_at_least": frontier["solved_s6_in_manifest"] + 1,
    "unique_remaining_s6_at_most": frontier["unique_remaining_s6"] - 1,
    "sum_remaining_cost_at_most": frontier["sum_remaining_cost"] - 65,
    "s6_needed_by_open_classes_at_most": frontier["s6_needed_by_open_classes"] - 1,
    "cost_needed_by_open_classes_at_most": frontier["cost_needed_by_open_classes"] - 65,
}
assert lower_bound == {
    "solved_s6_in_manifest_at_least": 962,
    "unique_remaining_s6_at_most": 6885,
    "sum_remaining_cost_at_most": 542227,
    "s6_needed_by_open_classes_at_most": 5155,
    "cost_needed_by_open_classes_at_most": 405950,
}

sweep65 = audit_sweep("cost65e", 9, 5949)
sweep61 = audit_sweep("cost61f", 8, 3402)
assert (sweep65["candidates"],sweep65["win7_d10"],sweep65["refuted_d10"],
        sweep65["total_nodes"]) == (65,21,44,308092253)
assert (sweep61["candidates"],sweep61["win7_d10"],sweep61["refuted_d10"],
        sweep61["total_nodes"]) == (61,11,50,45925702)

result = {
    "schema": "n11-class2-frontier-union-cost65e-bit107-audit-20261115-v1",
    "date": "2026-11-15",
    "frontier_union": {
        "baseline": base63,
        "marginal_counts_by_lane": {"cost63a":len(m63),"cost61e":len(m61e),"cost61f":len(m61f)},
        "marginal_s6_hexes": sorted(union),
        "marginal_cost_sum": union_cost,
        "combined": frontier,
        "method": "Exact disjoint set union of three published recomputations; all ten marginal keys are present in the 7,867-row manifest and their manifest costs sum to 660."
    },
    "sweeps": {"cost65e":sweep65,"cost61f":sweep61},
    "certificates": {
        "cost61f": [
            {"bit":c["bit"],"root_hex":c["root_hex"],"rows":c["rows"],
             "legal_moves_independent":root_geometry(c["root_hex"])["legal_moves"],
             "sub_roots_pass":c["sub_roots_pass"],"union_missing":c["union_missing"],
             "union_extra":c["union_extra"]} for c in cert61["certificates"]
        ],
        "cost65e_bit107": {
            "root_hex":bit107["root_hex"],"rows":bit107["rows"],
            "legal_moves_independent":geom107["legal_moves"],
            "sub_roots_pass":bit107["sub_roots_pass"],
            "union_missing":bit107["union_missing"],
            "union_extra":bit107["union_extra"],
            "fbt_drops":sw65["certificate"]["fbt_drops"],
            "sha256":bit107["sha256"]
        }
    },
    "cost65e_bit107_parent_lift": parent_rows,
    "local_s5_809102": {
        "after_cost63a":t63,
        "after_cost61e_parallel_baseline":t61e,
        "after_cost61f_parallel_baseline":t61f,
        "known_new_parent_s6":target,
        "known_new_parent_cost":65,
        "after_bit107":local_after
    },
    "global_lower_bound_after_bit107": lower_bound,
    "exact_global_frontier_after_bit107":"not recomputed; three other manifest parents of bit107 were not reconciled against the baseline solved set",
    "interpretation_guard":"WIN7-D10 search candidates are not certificates; REFUTED-D10 is not a LOSS proof. The lower bound counts only the one confirmed new S6 parent. Standard 11x11 empty root, {49,60}, S2 {59,60}, class 2 and class 4 remain UNKNOWN."
}
(OUT / "frontier-union-cost65e-bit107-audit-20261115.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + chr(10))
print(json.dumps({"frontier_union":frontier,"after_bit107_lower_bound":lower_bound,
                  "local_s5_809102":local_after},ensure_ascii=False,sort_keys=True))
