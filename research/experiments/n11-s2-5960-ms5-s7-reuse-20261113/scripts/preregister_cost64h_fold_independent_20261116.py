#!/usr/bin/env python3
"""Pre-registration of the cost-64h receipt fold: an independent projection of
the 23 published cost-64h WIN7-D10 receipt roots (child
00000000000000403800000008100000, win bits per the published claim v2) onto the
canonical head 1452/174/6396/506144/4669/370058, published BEFORE the parallel
session's cost-64h fold receipt lands.

Protocol (adapted from the published cost-65n fold pre-registration
class2-lane-cost65n-fold-preregistration-20261116.json, blob da2b2292, and the
head-1450 fold-projection tool, blob 49fcd8ae):

1. blob-verify every input actually read: the published head-1450 projection
   tool and its pinned basis file list (the 133 BASIS_JSON_BLOBS / GZ_BLOBS /
   MS5_BLOBS inputs re-declared by the cost-66c fold script, blob 898cfa61),
   the cost-66c fold JSON (blob 8783993e), the cost-76d/77e fold JSON (blob
   8d4bc622), the head-1452 presweep census JSON (blob 0d9a94a2) and the
   cost-64h claim v2 (blob 68e48780);
2. independently reconstruct the receipt-root basis: the 764 published roots
   of the head-1444 basis, plus the seven cost-66c receipt roots, plus the
   four cost-76d/77e receipt roots = 775 roots / 760 distinct D4 canons at
   head 1452, and assert the published head-1452 six-number summary and its
   demand histogram (frontier semantics verbatim-ported through the
   published tool's own functions, loaded blob-pinned);
3. re-derive the 23 WIN7-D10 receipt roots as child|1<<bit from the claim's
   win7_d10_bits list (ascending publication order as listed), assert each is
   a 7-stone position, that its D4 canon equals the census bit-table
   root_canon for that bit, that all 23 canons are pairwise distinct and
   disjoint from the 760 folded canons (conflict census zero);
4. fold the 23 receipts in that order with an independent implementation of
   the published fold semantics (covers = D4 canons of the one-stone
   deletions; marginal / marginal-in-manifest against the basis solved set)
   and project the new head: six-number summary, demand-histogram deltas,
   per-affected-parent row/edge-cost deltas, closed manifest rows with edge
   costs, per-receipt marginals.

Interpretation guard: this is bookkeeping over published receipts only; no
engine search is run and no verdict is created here.  Solved counts measure
manifest coverage, not the game-theoretic value of any position.  WIN7
certificates prove a first-player win within depth 10 from the individual
7-stone roots only; REFUTED-D10 is not a LOSS proof.  The 11x11 empty board,
the two-stone roots {49,60} and {59,60}, S2 {59,60}, and classes 1/2/4 all
remain UNKNOWN.
"""
import gzip
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
SCRIPTS = HERE / "scripts"
sys.path.insert(0, str(SCRIPTS))

TOOL = "fold_projection_head1450_tool_20261116.py"
TOOL_BLOB = "49fcd8ae6706c075b39eea5b115b2a045c2950cf"
FOLD66C_JSON = "class-frontier-cost66c-receipts-recompute-20261116.json"
FOLD66C_BLOB = "8783993e5c73cc9697c3ca48aef981725f422be8"
FOLD7677_JSON = "class-frontier-cost76d77e-receipts-recompute-20261116.json"
FOLD7677_BLOB = "8d4bc622f9da22b8754f2e398e5481359656d956"
CENSUS_JSON = "class2-lane-next-target-presweep-1452-20261116.json"
CENSUS_BLOB = "0d9a94a272de9fe45708757f17bfea60239a3c9b"
CLAIM_JSON = "class2-lane-cost64h-inflight-20261116.json"
CLAIM_BLOB = "68e4878094b78eaf0a465033d0289a6db5d94861"

HEAD_1452 = (1452, 174, 6396, 506144, 4669, 370058)
CHILD = int("00000000000000403800000008100000", 16)
PARENT_P = "00000000000000403800000008000000"
SUMMARY_KEYS = ("solved_s6_in_manifest", "remaining_s5_orbits",
                "unique_remaining_s6", "sum_remaining_cost",
                "s6_needed_by_open_classes", "cost_needed_by_open_classes")


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def assert_blob(name, blob):
    data = (OUT / name).read_bytes()
    got = git_blob_sha(data)
    assert got == blob, f"{name}: {got} != {blob}"
    return json.loads(data.decode())


# ---------- 0. blob-verify the imported tool itself ----------
tool_data = (SCRIPTS / TOOL).read_bytes()
assert git_blob_sha(tool_data) == TOOL_BLOB, "head-1450 projection tool blob"
ns = {"__file__": str(SCRIPTS / TOOL), "__name__": "tool1450_import"}
exec(compile(tool_data.decode(), str(SCRIPTS / TOOL), "exec"), ns)
canon = ns["canon"]
covers = ns["covers"]
popcount = ns["popcount"]
extract_roots = ns["extract_roots"]
reconstruct_771 = ns["reconstruct"]          # 764 basis + 7 cost-66c receipts

# the tool asserts every basis-file blob on its own (133 JSON + 3 gz + 6 csv
# manifest parts + the cost-66c fold JSON); calling it re-verifies all pins
basis_771 = reconstruct_771()
assert len(basis_771) == 771, len(basis_771)

fold7677 = assert_blob(FOLD7677_JSON, FOLD7677_BLOB)
census = assert_blob(CENSUS_JSON, CENSUS_BLOB)
claim = assert_blob(CLAIM_JSON, CLAIM_BLOB)

# ---------- 1. basis frontier (verbatim semantics, published inputs) ----------
import csv  # noqa: E402

MS5 = HERE.parent / "n11-s2-5960-milestone5-20261112" / "output"

manifest = set()
for path in sorted(MS5.glob("ms5_s6_manifest_part*.csv")):
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            manifest.add(int(row["hex"], 16))
assert len(manifest) == 7867, len(manifest)

classes = {}
with gzip.open(OUT / "s5-remaining-after-reuse.csv.gz", "rt", newline="") as f:
    for row in csv.DictReader(f):
        classes[row["s5_hex"]] = int(row["classes"])
incidences = []
with gzip.open(OUT / "s5-s6-remaining-incidences.csv.gz", "rt", newline="") as f:
    incidences = list(csv.DictReader(f))
assert len(incidences) == 14558, len(incidences)
winners = set()
with gzip.open(OUT / "win7-reuse-hits.csv.gz", "rt", newline="") as f:
    for row in csv.DictReader(f):
        winners.add(int(row["s6_hex"], 16))
assert len(winners) == 498, len(winners)

LOSS6 = ("00000000000000809202000400000000",
         "00000000000000003800004008000008",
         "00000000000000805202000000002000")
loss = {int(x, 16) for x in LOSS6}
rejected = {r["s5_hex"] for r in incidences if int(r["s6_hex"], 16) in loss}


def frontier(solved):
    remaining = defaultdict(list)
    for row in incidences:
        if row["s5_hex"] not in rejected and int(row["s6_hex"], 16) not in solved:
            remaining[row["s5_hex"]].append(row)
    unique = {r["s6_hex"]: int(r["s6_s7_edge_cost"])
              for rows in remaining.values() for r in rows}
    demand = defaultdict(lambda: {"c1": 0, "c2": 0, "c4": 0})
    for s5, rows in remaining.items():
        bits = classes.get(s5, 0)
        for row in rows:
            d = demand[row["s6_hex"]]
            if bits & 1:
                d["c1"] += 1
            if bits & 2:
                d["c2"] += 1
            if bits & 4:
                d["c4"] += 1
    open_only = {k: v for k, v in demand.items() if v["c1"] == 0}
    return remaining, unique, demand, open_only


def summary(solved):
    remaining, unique, demand, open_only = frontier(solved)
    hist = defaultdict(int)
    for v in open_only.values():
        hist[f"c2={v['c2']},c4={v['c4']}"] += 1
    return {
        "solved_s6_in_manifest": len(solved & manifest),
        "remaining_s5_orbits": len(remaining),
        "unique_remaining_s6": len(unique),
        "sum_remaining_cost": sum(unique.values()),
        "s6_needed_by_open_classes": len(open_only),
        "cost_needed_by_open_classes": sum(int(unique[k]) for k in open_only),
        "hist": dict(sorted(hist.items())),
    }


# ---------- 2. fold the four cost-76d/77e receipts -> head 1452 ----------
receipts_7677 = fold7677["receipts"]
assert [r["root_hex"] for r in receipts_7677] == fold7677["totals"]["root_hexes"]
roots_7677 = [int(r["root_hex"], 16) for r in receipts_7677]
folded = set(basis_771)
for r in roots_7677:
    assert popcount(r) == 7
    folded.add(r)
assert len(folded) == 775, len(folded)
folded_canons = {canon(r) for r in folded}
assert len(folded_canons) == 760, len(folded_canons)

solved = set(winners)
for r in folded:
    solved |= covers(r)
st_1452 = summary(solved)
assert tuple(st_1452[k] for k in SUMMARY_KEYS) == HEAD_1452, st_1452
fa = fold7677["frontier_after_cost76d77e"]
assert [fa[k] for k in SUMMARY_KEYS] == list(HEAD_1452)
assert st_1452["hist"] == fa["demand_histogram_open_only"], st_1452["hist"]
HIST_1452 = fa["demand_histogram_open_only"]

# ---------- 3. the 23 cost-64h WIN7-D10 receipt roots ----------
win_bits = list(claim["sweep_results"]["win7_d10_bits"])
assert win_bits == sorted(win_bits) and len(win_bits) == 23, win_bits
assert claim["sweep_results"]["candidates_resolved"] == 64
assert claim["sweep_results"]["capped_count"] == 0
assert claim["sweep_results"]["refuted_d10_count"] == 41
assert claim["s6_child"] == f"{CHILD:032x}"
assert claim["demand"] == {"c1": 0, "c2": 2, "c4": 0}

bit_table = census["bit_tables"][f"{CHILD:032x}"]["bits"]
assert len(bit_table) == 64
canon_by_bit = {e["bit"]: e["root_canon"] for e in bit_table}

new_roots = []
for bit in win_bits:
    root = CHILD | (1 << bit)
    assert popcount(root) == 7, (bit, f"{root:032x}")
    c = canon(root)
    assert f"{c:032x}" == canon_by_bit[bit], (bit, f"{c:032x}", canon_by_bit[bit])
    assert c not in folded_canons, f"bit {bit} D4-collides with a folded root"
    new_roots.append((bit, root, c))
assert len({c for _, _, c in new_roots}) == 23
# the child row itself is a manifest row, open at head 1452
child_canon = canon(CHILD)
assert child_canon in manifest
assert child_canon not in solved

# ---------- 4. fold the 23 receipts in the claim's listed order ----------
rem_b, uniq_b, dem_b, _ = frontier(solved)
receipts = []
union_marg = set()
union_marg_m = set()
for bit, root, c in new_roots:
    cov = covers(root)
    marg = cov - solved
    marg_m = marg & manifest
    receipts.append({
        "bit": bit,
        "root_hex": f"{root:032x}",
        "d4_canonical_hex": f"{c:032x}",
        "d4_orbit_distinct_from_all_folded_roots": True,
        "covers": len(cov),
        "marginal": len(marg),
        "marginal_hexes": sorted(f"{x:032x}" for x in marg),
        "marginal_in_manifest": len(marg_m),
        "marginal_manifest_hexes": sorted(f"{x:032x}" for x in marg_m),
    })
    union_marg |= marg
    union_marg_m |= marg_m
    solved |= cov
    folded_canons.add(c)

child_closed_by_bit = None
for rec in receipts:
    if f"{child_canon:032x}" in rec["marginal_manifest_hexes"]:
        child_closed_by_bit = rec["bit"]
        break
assert child_closed_by_bit is not None

st_after = summary(solved)
hist_deltas = {k: st_after["hist"].get(k, 0) - HIST_1452.get(k, 0)
               for k in set(HIST_1452) | set(st_after["hist"])}

# per-affected-parent deltas (published fold-record semantics)
edge_cost = defaultdict(dict)
for row in incidences:
    edge_cost[row["s5_hex"]][row["s6_hex"]] = int(row["s6_s7_edge_cost"])
rem_a, uniq_a, dem_a, _ = frontier(solved)
parents = {}
for s5 in set(rem_b) | set(rem_a):
    rows_b = list(rem_b.get(s5, []))
    rows_a = list(rem_a.get(s5, []))
    if len(rows_b) == len(rows_a):
        continue
    lost = ({int(r["s6_hex"], 16) for r in rows_b}
            - {int(r["s6_hex"], 16) for r in rows_a})
    lost &= union_marg_m
    if not lost:
        continue
    parents[s5] = {
        "s5_hex": s5,
        "classes": classes.get(s5, 0),
        "rows_before": len(rows_b),
        "rows_after": len(rows_a),
        "edge_cost_before": sum(int(r["s6_s7_edge_cost"]) for r in rows_b),
        "edge_cost_after": sum(int(r["s6_s7_edge_cost"]) for r in rows_a),
        "lost_rows_hexes": sorted(f"{x:032x}" for x in lost),
        "lost_edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows_b
                              if int(r["s6_hex"], 16) in lost),
    }
incidences_after = sum(len(v["lost_rows_hexes"]) for v in parents.values())
cost_delta = sum(v["lost_edge_cost"] for v in parents.values())

closed_rows = sorted(f"{x:032x}" for x in union_marg_m)

# the parents of each closed manifest row (via the parent incidence rows)
closed_row_parents = defaultdict(list)
for s5, v in parents.items():
    for h in v["lost_rows_hexes"]:
        closed_row_parents[h].append(s5)

result = {
    "schema": "n11-class2-lane-cost64h-fold-preregistration-independent-20261116-v1",
    "date": "2026-11-16",
    "published_before_fold_receipt_lands": True,
    "basis_head": 1452,
    "basis_head_numbers": list(HEAD_1452),
    "basis_demand_histogram": HIST_1452,
    "basis_receipt_roots": 775,
    "basis_distinct_d4_canons": 760,
    "inputs_blob_pins": {
        "head1450_projection_tool": TOOL_BLOB,
        "cost66c_fold_json": FOLD66C_BLOB,
        "cost76d77e_fold_json": FOLD7677_BLOB,
        "head1452_presweep_census_json": CENSUS_BLOB,
        "cost64h_claim_v2_json": CLAIM_BLOB,
    },
    "child": {
        "s6_hex": f"{CHILD:032x}",
        "d4_canonical_hex": f"{child_canon:032x}",
        "legal_candidates": 64,
        "demand_at_1452": {"c1": 0, "c2": 2, "c4": 0},
        "open_at_basis_head": True,
        "closed_by_receipt_bit": child_closed_by_bit,
    },
    "win_bits_in_fold_order": win_bits,
    "fold_order_note": (
        "receipts folded in the win7_d10_bits order of the published claim v2 "
        "(ascending bit order); totals, projected head, histogram deltas, "
        "affected parents and the closed-row set are order-invariant, "
        "per-receipt marginals are not"),
    "receipts": receipts,
    "totals": {
        "receipts": len(receipts),
        "total_marginal": len(union_marg),
        "total_marginal_in_manifest": len(union_marg_m),
        "closed_manifest_rows": closed_rows,
        "child_closed_by_bit": child_closed_by_bit,
        "conflict_census_overlaps": 0,
        "pairwise_distinct_d4_canons": True,
    },
    "projected_head": {k: st_after[k] for k in SUMMARY_KEYS},
    "projected_demand_histogram": st_after["hist"],
    "demand_histogram_deltas": dict(sorted(hist_deltas.items())),
    "affected_parents": {k: v for k, v in sorted(parents.items())},
    "parent_row_incidences": incidences_after,
    "parent_edge_cost_delta": cost_delta,
    "closed_row_parent_map": {k: sorted(v) for k, v in sorted(closed_row_parents.items())},
    "interpretation_guard": (
        "bookkeeping fold projection over published receipts only; no engine "
        "search was run and no verdict was created; solved counts measure "
        "manifest coverage, not the game-theoretic value of any position; "
        "WIN7 certificates prove a first-player win within depth 10 from the "
        "individual 7-stone roots only; REFUTED-D10 is not a LOSS proof; the "
        "11x11 empty board, the two-stone roots {49,60} and {59,60}, S2 "
        "{59,60} and classes 1/2/4 all remain UNKNOWN"),
}

out_path = OUT / ("class2-lane-cost64h-fold-preregistration-independent-"
                  "20261116.json")
with open(out_path, "w") as f:
    json.dump(result, f, indent=1, sort_keys=True)
    f.write("\n")
print("basis head 1452:", " ".join(str(st_1452[k]) for k in SUMMARY_KEYS))
print("projected head :", " ".join(str(st_after[k]) for k in SUMMARY_KEYS))
print("total marginal:", len(union_marg), "mim:", len(union_marg_m))
print("child closed by bit", child_closed_by_bit)
print("hist deltas:", {k: v for k, v in sorted(hist_deltas.items()) if v})
print("affected parents:", len(parents), "row incidences:", incidences_after,
      "edge cost delta:", cost_delta)
for s5, v in sorted(parents.items()):
    print("  parent", s5, "classes", v["classes"], "rows",
          v["rows_before"], "->", v["rows_after"], "lost", v["lost_rows_hexes"])
for rec in receipts:
    if rec["marginal_in_manifest"]:
        print("  receipt bit", rec["bit"], "marg", rec["marginal"], "mim",
              rec["marginal_in_manifest"], rec["marginal_manifest_hexes"])
print("output:", out_path.name)
