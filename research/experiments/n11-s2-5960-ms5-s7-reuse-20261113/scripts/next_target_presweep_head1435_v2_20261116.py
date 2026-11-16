#!/usr/bin/env python3
"""Head-1435 next-target pre-sweep census v2 (post-cost-64e) for the class-2 lane.

Identical protocol to v1 (next_target_presweep_head1435_20261116.py) with one
addition: the published cost-64e completed STERILE raw sweep (8 v16 raw
batches, claim v2 blob 55c51c92) is now harvested as well, validated bit-exact
against the claim's own bit lists. Everything else (head-1435 fold-chain
reproduction, lane verdict corpus harvest, canonical-root census) is unchanged.

Interpretation guard: this is search-plan bookkeeping only. No engine search
was run here, no verdict was created, and no row was closed. WIN7-D10 proves a
first-player win within depth 10 from the individual 7-stone root only;
REFUTED-D10 is not a LOSS proof; STERILE is not a LOSS proof; receipt folds are
manifest-coverage bookkeeping. The 11x11 empty board, the two-stone roots
{49,60} and {59,60}, S2 {59,60}, and classes 1/2/4 all remain UNKNOWN.
"""
import csv
import json
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SCRIPTS = HERE / "scripts"
OUT = HERE / "output"
sys.path.insert(0, str(SCRIPTS))
from legal_candidates import legal_candidates  # noqa: E402

P_PARENT = "00000000000000403800000008000000"
SH_PARENT = "00000000000000003800000008002000"
CHILD_64D = "00000000000000403800000008002000"
WIN_BITS_64D = [0, 1, 2, 11, 16, 30, 32, 43, 53, 66, 69, 75, 79, 86, 92,
                95, 98, 106, 107, 109, 111, 113, 120]
CHILD_64E = "0000000000000000380000000a002000"
CLAIM_64E = OUT / "class2-lane-cost64e-inflight-20261116.json"

# ---------- 1. reproduce head 1435 via the published fold chain ----------
ns = runpy.run_path(str(SCRIPTS / "recompute_frontier_cost64d_receipts_"
                        "20261116.py"))
s_cur = set(ns["s_cur"])
rem_after = ns["rem_after"]
uniq_after = ns["uniq_after"]
dem_after = ns["dem_after"]
canon = ns["canon"]
git_blob_sha = ns["git_blob_sha"]
st_after = ns["st_after"]
assert (st_after["solved_s6_in_manifest"], st_after["remaining_s5_orbits"],
        st_after["unique_remaining_s6"], st_after["sum_remaining_cost"],
        st_after["s6_needed_by_open_classes"],
        st_after["cost_needed_by_open_classes"]) == \
    (1435, 174, 6413, 507337, 4686, 371251), st_after

folded = set(ns["folded"])                       # receipt roots at 1419
roots_64d = {int(h, 16) for h in ns["ROOTS"].values()}   # 23 WIN receipts
receipt_roots = folded | roots_64d
assert len(folded) == 734 and len(roots_64d) == 23
assert len(receipt_roots) == 757  # 735+23 receipts, one 65f bit-25 duplicate
receipt_canon = {canon(r) for r in receipt_roots}
print("head 1435 reproduced; receipt roots (distinct):", len(receipt_roots),
      "distinct canons:", len(receipt_canon))

# ---------- 2. harvest the lane-local sweep verdict corpus ----------
def find_key(obj, names, depth=0):
    """First matching key at top level or one nesting level down."""
    for n in names:
        if n in obj:
            return obj[n]
    if depth < 1:
        for v in obj.values():
            if isinstance(v, dict):
                r = find_key(v, names, depth + 1)
                if r is not None:
                    return r
    return None


harvest = {}          # canon(int) -> {"verdict", "sources"}
harvest_files = []
skipped = []
for path in sorted(OUT.glob("class2-lane-cost*.json")):
    name = path.name
    try:
        d = json.loads(path.read_text())
    except Exception:
        skipped.append((name, "unparseable"))
        continue
    if not isinstance(d, dict):
        continue
    child = None
    for key in ("s6_child_hex", "s6_child", "child"):
        v = d.get(key)
        if isinstance(v, str) and len(v) == 32:
            child = v
            break
    if child is None and "sweep_aggregate" in d:
        # raw-sweep-audit style: child recoverable from parent_derivation
        pd = d.get("parent_derivation") or {}
        v = pd.get("s6_child") or pd.get("child")
        if isinstance(v, str) and len(v) == 32:
            child = v
    if child is None:
        skipped.append((name, "no child hex"))
        continue
    win_bits = find_key(d, ("win7_bits", "win7_d10_bits"))
    capped_bits = find_key(d, ("capped_bits",))
    capped_n = find_key(d, ("capped", "capped_count"))
    ref_bits = find_key(d, ("refuted_d10_bits", "refuted_bits"))
    ref_n = find_key(d, ("refuted_d10", "refuted_d10_count"))
    cands = d.get("legal_candidates")
    if win_bits is None:
        skipped.append((name, "no win bits"))
        continue
    win_bits = sorted(set(int(b) for b in win_bits))
    if cands is None:
        cands = legal_candidates(child)[1]
    else:
        cands = sorted(set(int(b) for b in cands))
        assert cands == sorted(legal_candidates(child)[1]), name
    capped_bits = sorted(set(int(b) for b in capped_bits)) \
        if capped_bits else []
    if ref_bits is None:
        if capped_n not in (None, 0, len(capped_bits)) or capped_bits:
            skipped.append((name, "capped bits unaccounted"))
            continue
        ref_bits = sorted(set(cands) - set(win_bits) - set(capped_bits))
    else:
        ref_bits = sorted(set(int(b) for b in ref_bits))
    if ref_n is not None and isinstance(ref_n, int) and ref_n != len(ref_bits):
        skipped.append((name, f"refuted count {ref_n} != {len(ref_bits)}"))
        continue
    if set(win_bits) | set(ref_bits) | set(capped_bits) != set(cands) or \
            (win_bits and ref_bits and set(win_bits) & set(ref_bits)):
        skipped.append((name, "bit accounting mismatch"))
        continue
    n_before = len(harvest)
    child_v = int(child, 16)
    conflicts_here = []
    for b in win_bits:
        c = canon(child_v | (1 << b))
        e = harvest.get(c)
        if e and e["verdict"] != "WIN7-D10":
            conflicts_here.append((child, b, e["verdict"]))
        harvest[c] = {"verdict": "WIN7-D10", "sources":
                      e["sources"] + [name] if e else [name]}
    for b in ref_bits:
        c = canon(child_v | (1 << b))
        e = harvest.get(c)
        if e and e["verdict"] != "REFUTED-D10":
            conflicts_here.append((child, b, e["verdict"]))
        harvest[c] = {"verdict": "REFUTED-D10", "sources":
                      e["sources"] + [name] if e else [name]}
    assert not conflicts_here, conflicts_here
    harvest_files.append({
        "file": name, "git_blob_sha": git_blob_sha(path), "child": child,
        "candidates": len(cands), "win7": len(win_bits),
        "refuted": len(ref_bits), "capped": len(capped_bits)})
    print(f"harvest {name}: child {child} win {len(win_bits)} "
          f"refuted {len(ref_bits)} (+{len(harvest)-n_before} new canons)")

# validate bit-exact against the published cost-64d raw batches, then add
# the 64d verdicts to the harvest (cross-sweep agreement asserted)
bit_recs = {}
for i in range(1, 9):
    for line in (OUT / f"class2-lane-cost64d-raw-batch{i}-20261116.jsonl"
                 ).read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if "control" in r:
            assert r["loss"] is False and r["capped"] is False
        else:
            assert r["bit"] not in bit_recs
            bit_recs[r["bit"]] = r
assert sorted(bit_recs) == sorted(legal_candidates(CHILD_64D)[1])
raw_win = sorted(b for b, r in bit_recs.items() if r["loss"] is True)
assert raw_win == WIN_BITS_64D, raw_win
child_v = int(CHILD_64D, 16)
x64d_agree = x64d_new = 0
for b, r in bit_recs.items():
    c = canon(child_v | (1 << b))
    expect = "WIN7-D10" if r["loss"] is True else "REFUTED-D10"
    assert r["capped"] is False
    e = harvest.get(c)
    if e:
        assert e["verdict"] == expect, (b, expect, e)
        x64d_agree += 1
    else:
        harvest[c] = {"verdict": expect,
                      "sources": ["cost64d-raw-batches (claim v4 e3cf7378)"]}
        x64d_new += 1
print(f"64d raw batches: {x64d_agree} canons cross-agree with other "
      f"sweeps, {x64d_new} new canons added")
harvest_files.append({
    "file": "class2-lane-cost64d-raw-batch1..8-20261116.jsonl",
    "git_blob_sha": "per-batch pinned in claim v4 (e3cf7378)",
    "child": CHILD_64D, "candidates": 64, "win7": 23, "refuted": 41,
    "capped": 0})

# validate bit-exact against the published cost-64e raw batches and the
# completed-STERILE claim v2 (blob 55c51c92), then add the 60 swept REFUTED-D10
# verdicts to the harvest (conflict-asserted like every other source)
claim64e = json.loads(CLAIM_64E.read_text())
res64e = claim64e["results"]
assert claim64e["s6_child"] == CHILD_64E
assert claim64e["open_candidate_count"] == 60
assert res64e["win7_d10_bits"] == [] and res64e["capped_bits"] == []
swept64e = [int(b) for b in res64e["refuted_d10_bits_swept_v16"]]
transferred64e = [int(b) for b in res64e["refuted_d10_bits_transferred"]]
batch_lists64e = {int(k): [int(b) for b in v]
                  for k, v in res64e["batch_bit_lists"].items()}
assert sorted(swept64e) == sorted(
    set(legal_candidates(CHILD_64E)[1]) - set(transferred64e))
assert sum((len(v) for v in batch_lists64e.values()), 0) == 60
assert sorted(sum(batch_lists64e.values(), [])) == sorted(swept64e)
bit_recs_e = {}
for i in sorted(batch_lists64e):
    for line in (OUT / f"class2-lane-cost64e-raw-batch{i}-20261116.jsonl"
                 ).read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if "control" in r:
            assert r["loss"] is False and r["capped"] is False
        else:
            assert r["bit"] not in bit_recs_e
            bit_recs_e[r["bit"]] = r
assert sorted(bit_recs_e) == sorted(swept64e)
raw_win_e = sorted(b for b, r in bit_recs_e.items() if r["loss"] is True)
assert raw_win_e == [], raw_win_e
child_e_v = int(CHILD_64E, 16)
x64e_agree = x64e_new = 0
for b, r in bit_recs_e.items():
    c = canon(child_e_v | (1 << b))
    expect = "WIN7-D10" if r["loss"] is True else "REFUTED-D10"
    assert r["capped"] is False
    e = harvest.get(c)
    if e:
        assert e["verdict"] == expect, (b, expect, e)
        x64e_agree += 1
    else:
        harvest[c] = {"verdict": expect,
                      "sources": ["cost64e-raw-batches (claim v2 55c51c92)"]}
        x64e_new += 1
print(f"64e raw batches: {x64e_agree} canons cross-agree with other "
      f"sources, {x64e_new} new canons added (all REFUTED-D10)")
harvest_files.append({
    "file": "class2-lane-cost64e-raw-batch1..8-20261116.jsonl",
    "git_blob_sha": "per-batch pinned in claim v2 (55c51c92)",
    "child": CHILD_64E, "candidates": 64, "win7": 0, "refuted": 64,
    "capped": 0})
print("harvest total canons:", len(harvest),
      "win:", sum(1 for v in harvest.values()
                  if v["verdict"] == "WIN7-D10"),
      "refuted:", sum(1 for v in harvest.values()
                      if v["verdict"] == "REFUTED-D10"))
print("skipped:", skipped)

# ---------- 3. family census at head 1435 ----------
def bit_status(row_hex, b):
    c = canon(int(row_hex, 16) | (1 << b))
    if c in receipt_canon:
        return "receipt_win", c
    e = harvest.get(c)
    if e:
        return ("harvested_win" if e["verdict"] == "WIN7-D10"
                else "harvested_refuted"), c
    return "open", c


family = {}
for parent in (P_PARENT, SH_PARENT):
    rows = rem_after[parent]
    fam_rows = []
    fam_canon_open = {}
    fam_canon_receipt = set()
    fam_canon_harvested = set()
    occ = 0
    for r in sorted(rows, key=lambda r: (int(r["s6_s7_edge_cost"]),
                                         r["s6_hex"])):
        row_hex = r["s6_hex"]
        cost = int(r["s6_s7_edge_cost"])
        bits = legal_candidates(row_hex)[1]
        assert len(bits) == cost, (row_hex, len(bits), cost)
        per = {"receipt_win": 0, "harvested_win": 0,
               "harvested_refuted": 0, "open": 0}
        row_detail = {}
        for b in bits:
            st, c = bit_status(row_hex, b)
            per[st] += 1
            occ += 1
            if st == "open":
                fam_canon_open.setdefault(c, []).append((row_hex, b))
            elif st == "receipt_win":
                fam_canon_receipt.add(c)
            else:
                fam_canon_harvested.add(c)
            row_detail[b] = st
        dem = dem_after.get(row_hex, {})
        fam_rows.append({
            "s6_hex": row_hex, "cost": cost,
            "demand": {k: int(dem.get(k, -1)) for k in ("c1", "c2", "c4")},
            "census": per,
            "open_after_census": per["open"]})
    family[parent] = {
        "s5_hex": parent, "rows": fam_rows,
        "row_count": len(fam_rows),
        "occurrences": occ,
        "distinct_receipt_win_canons": len(fam_canon_receipt),
        "distinct_harvested_canons": len(fam_canon_harvested),
        "distinct_open_canons": len(fam_canon_open),
        "occurrence_reduction": occ - len(fam_canon_open) -
        len(fam_canon_receipt) - len(fam_canon_harvested),
        "sum_open_after_census": sum(r["open_after_census"]
                                      for r in fam_rows)}
    print(f"family {parent}: rows {len(fam_rows)} occ {occ} "
          f"open canons {len(fam_canon_open)} "
          f"sum open after census {family[parent]['sum_open_after_census']}")

fp = family[P_PARENT]
fsh = family[SH_PARENT]
assert fp["row_count"] == 18 and sum(r["cost"] for r in fp["rows"]) == 1287
assert fsh["row_count"] == 31 and sum(r["cost"] for r in fsh["rows"]) == 2145

# ---------- 4. cheapest-row ranking + per-bit census for the cheapest rows ----------
all_rows = []
for parent in (P_PARENT, SH_PARENT):
    for r in family[parent]["rows"]:
        all_rows.append((r["cost"], parent, r))

fully_determined = [r for _, _, r in all_rows if r["open_after_census"] == 0]
open_rows = [r for _, _, r in all_rows if r["open_after_census"] > 0]
best_open = sorted(
    open_rows,
    key=lambda r: (r["open_after_census"], r["cost"], r["s6_hex"]))

bit_tables = {}
for r in [x[2] for x in sorted(all_rows,
                               key=lambda t: (t[0], t[2]["s6_hex"]))[:8]] + \
        best_open[:4]:
    row_hex = r["s6_hex"]
    bits = legal_candidates(row_hex)[1]
    tbl = []
    for b in bits:
        st, c = bit_status(row_hex, b)
        tbl.append({"bit": b, "status": st, "root_canon": f"{c:032x}"})
    bit_tables[row_hex] = tbl

# ---------- 5. emit ----------
inp_pins = {
    "fold_script": {
        "path": "scripts/recompute_frontier_cost64d_receipts_20261116.py",
        "git_blob_sha": git_blob_sha(SCRIPTS /
            "recompute_frontier_cost64d_receipts_20261116.py")},
    "fold_output_json": {
        "path": "output/class-frontier-cost64d-receipts-recompute-20261116.json",
        "git_blob_sha": git_blob_sha(OUT /
            "class-frontier-cost64d-receipts-recompute-20261116.json")},
    "presweep_audit_1410": {
        "path": "output/class2-lane-next-target-presweep-audit-20261116.json",
        "git_blob_sha": git_blob_sha(OUT /
            "class2-lane-next-target-presweep-audit-20261116.json")},
    "parent_incidence_audit_1410": {
        "path": "output/class2-lane-parent-incidence-audit-20261116.json",
        "git_blob_sha": git_blob_sha(OUT /
            "class2-lane-parent-incidence-audit-20261116.json")},
    "claim_v4": {
        "path": "output/class2-lane-cost64d-inflight-20261116.json",
        "git_blob_sha": git_blob_sha(OUT /
            "class2-lane-cost64d-inflight-20261116.json")},
    "claim_v2_64e": {
        "path": "output/class2-lane-cost64e-inflight-20261116.json",
        "git_blob_sha": git_blob_sha(CLAIM_64E)},
    "raw_batches_64e": {
        "path": "output/class2-lane-cost64e-raw-batch1..8-20261116.jsonl",
        "git_blob_sha": {f"batch{i}": git_blob_sha(OUT /
            f"class2-lane-cost64e-raw-batch{i}-20261116.jsonl")
            for i in range(1, 9)}},
}

best_rows = sorted(
    ({"cost": r["cost"], "s5_hex": parent, **{k: v for k, v in r.items()
                                              if k != "census"},
      "census": r["census"]} for parent in (P_PARENT, SH_PARENT)
     for r in family[parent]["rows"]),
    key=lambda x: (x["cost"], x["s5_hex"], x["s6_hex"]))
best_open_with_parent = sorted(
    ((parent, r) for parent in (P_PARENT, SH_PARENT)
     for r in family[parent]["rows"] if r["open_after_census"] > 0),
    key=lambda pr: (pr[1]["open_after_census"], pr[1]["cost"],
                    pr[1]["s6_hex"], pr[0]))
best_open_rows = [
    {"cost": r["cost"], "s5_hex": parent, **r}
    for parent, r in best_open_with_parent[:12]]
assert len(best_open_rows) == min(12, len(best_open_with_parent))
assert all(any(r["s6_hex"] == item["s6_hex"]
               for r in family[item["s5_hex"]]["rows"])
           for item in best_open_rows)
fully_determined_rows = [
    {"cost": r["cost"], "s5_hex": parent, **r}
    for parent in (P_PARENT, SH_PARENT)
    for r in family[parent]["rows"] if r["open_after_census"] == 0]

result = {
    "schema": "n11-class2-lane-next-target-presweep-1435-20261116-v2",
    "date": "2026-11-16",
    "method": ("stdlib python re-derivation on the published cost-64d fold "
               "chain (runpy reproduction of head 1435 with every published "
               "assert re-run); lane-local sweep-verdict harvest validated "
               "bit-exact against the published cost-64d raw batches AND the "
               "completed-STERILE cost-64e claim v2 raw batches (60 swept "
               "bits, all REFUTED-D10); canonical-root census via the "
               "chain's D4 canon function; legal candidate enumeration via "
               "legal_candidates.py (independent exact-integer Bareiss 4x4)"),
    "chain_head": "1435/174/6413/507337/4686/371251",
    "inputs": inp_pins,
    "receipt_roots": {"count": len(receipt_roots),
                      "distinct_canons": len(receipt_canon)},
    "harvest": {
        "files": harvest_files,
        "skipped": skipped,
        "distinct_verdict_canons": len(harvest),
        "win7_d10": sum(1 for v in harvest.values()
                        if v["verdict"] == "WIN7-D10"),
        "refuted_d10": sum(1 for v in harvest.values()
                           if v["verdict"] == "REFUTED-D10"),
        "conflicts": 0,
        "validation_64d": ("the published cost-64d raw batches re-parse to "
                           "23 WIN / 41 REFUTED (bit-exact vs claim v4); "
                           "every 64d canon that another harvested sweep "
                           "already determined agrees (asserted, zero "
                           "conflicts)"),
        "validation_64e": ("the published cost-64e raw batches re-parse to "
                           "0 WIN / 60 REFUTED (bit-exact vs the completed "
                           "STERILE claim v2, blob 55c51c92, including its "
                           "batch bit lists and the 4 pre-sweep transfers); "
                           "every 64e canon that another harvested source "
                           "already determined agrees (asserted, zero "
                           "conflicts)")
    },
    "family_census": family,
    "cheapest_rows_ranking": best_rows[:12],
    "cheapest_open_rows_ranking": best_open_rows,
    "ranking_parent_mapping_audit": {
        "method": ("preserve each (parent,row) pair from family_census; "
                   "do not cross-product best rows with both parents"),
        "entries": len(best_open_rows),
        "first_entry": {"s5_hex": best_open_rows[0]["s5_hex"],
                        "s6_hex": best_open_rows[0]["s6_hex"],
                        "open_after_census":
                            best_open_rows[0]["open_after_census"]},
        "all_entries_match_family_census": True,
    },
    "parent_mapping_correction": {
        "supersedes_blob_sha": "e2d12b5bc3701aa11afa297bb50e6df771fb91cf",
        "reason": ("the previous list comprehension assigned both protocol "
                   "parents to every best-open row, mislabeling ownership"),
        "corrected_selected_row_parent": SH_PARENT,
        "note": ("the recommendation string already used a membership lookup; "
                 "this fixes the machine-readable ranking"),
    },
    "fully_determined_rows": fully_determined_rows,
    "cheapest_row_bit_tables": bit_tables,
    "recommendation": (
        "cheapest-first within the class-2 lane protocol at head 1435, "
        "ranked by open candidate bits after receipt/harvest transfers: the "
        f"best next sweep target is {best_open[0]['s6_hex']} (parent "
        f"{[p for p in (P_PARENT, SH_PARENT) if any(r['s6_hex'] == best_open[0]['s6_hex'] for r in family[p]['rows'])][0]}, "
        f"cost {best_open[0]['cost']}, demand "
        f"c1={best_open[0]['demand']['c1']},c2={best_open[0]['demand']['c2']},"
        f"c4={best_open[0]['demand']['c4']}) with only "
        f"{best_open[0]['open_after_census']} open bits of "
        f"{best_open[0]['cost']} candidates; "
        f"{len(fully_determined)} of the 49 remaining rows of the two "
        "protocol parents are already fully determined by transfers (no "
        "sweep needed, e.g. the cost-64c STERILE row); sweep the open bits, "
        "extract certificates for any WIN7-D10 roots, and fold receipts "
        "before the next ranking"),
    "interpretation_guard": (
        "search-plan bookkeeping only: no engine search was run, no verdict "
        "was created, no row was closed by this audit; harvested verdicts "
        "are published depth-10 engine results D4-transferred by canonical "
        "root identity; receipt_win canons are folded WIN7-D10 receipts with "
        "published certificates; REFUTED-D10 is not a LOSS proof; STERILE is "
        "not a LOSS proof; solved 1435 is manifest-coverage bookkeeping"),
    "unknown_status": (
        "11x11 empty board, two-stone roots {49,60} and {59,60}, S2 {59,60}, "
        "and classes 1/2/4 all remain UNKNOWN"),
}

out_json = OUT / "class2-lane-next-target-presweep-1435-v2-20261116.json"
out_json.write_text(json.dumps(result, indent=1, sort_keys=False) + "\n")

out_csv = OUT / "class2-lane-next-target-rows-1435-v2-20261116.csv"
with out_csv.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["s5_hex", "s6_hex", "cost", "demand_c1", "demand_c2",
                "demand_c4", "receipt_win", "harvested_win",
                "harvested_refuted", "open_after_census"])
    for parent in (P_PARENT, SH_PARENT):
        for r in family[parent]["rows"]:
            w.writerow([parent, r["s6_hex"], r["cost"],
                        r["demand"]["c1"], r["demand"]["c2"],
                        r["demand"]["c4"], r["census"]["receipt_win"],
                        r["census"]["harvested_win"],
                        r["census"]["harvested_refuted"],
                        r["open_after_census"]])

print("WROTE", out_json.name, out_json.stat().st_size, "bytes;",
      out_csv.name, out_csv.stat().st_size, "bytes")
print("RECOMMENDATION:", result["recommendation"])
