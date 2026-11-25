#!/usr/bin/env python3
"""Head-1452 next-target pre-sweep census v1 (post-cost-76d/77e fold) for the
class-2 lane.

Protocol (adapted from the published head-1441 census,
next_target_presweep_head1441_20261116.py, and rebased on the new canonical
head 1452):

1. reproduce head 1452 exactly the way the published fold script does:
   module-level runpy of recompute_frontier_cost76d_77e_receipts_20261116.py
   (blob d2411023..., commit dab9e741) gives the projection-tool basis
   machinery (independent reconstruction of the 771 receipt roots / 756 D4
   canons at head 1450), then the four WIN7-D10 receipts are folded in the
   published order (76d bit 19, 76d bit 49, 77e bit 37, 77e bit 69) with the
   per-receipt marginals (5/4/6/4), in-manifest marginals (1/0/1/0),
   child-closed-by bits (76d:19, 77e:37), the three affected-parent deltas,
   the demand-histogram delta and the new six-number head re-asserted against
   the published fold JSON (blob 8d4bc622..., commit 4b17a1a2);
2. harvest the lane-local sweep verdict corpus from every published
   class2-lane-cost*.json claim/sweep file (glob + bit accounting + conflict
   assertion), including the retired v2 fold-complete claims of cost-76d and
   cost-77e;
3. canonical-root census over the next pure class-2 sweep target
   P = 00000000000000403800000008000000 (18 rows / 1287, unswept unclaimed per
   the published sterility audit) plus, for comparison, the best coverable
   class-2 S5 (3 rows / 211) and the best class-4 blocker S5 (18 rows / 1460):
   per row and per legal candidate bit, the status is receipt-win / harvested
   WIN7-D10 / harvested REFUTED-D10 / open against the 775 receipt roots
   (760 distinct D4 canons) at head 1452.

Interpretation guard: this is search-plan bookkeeping only. No engine search
was run here, no verdict was created, and no row was closed. WIN7-D10 proves
a first-player win within depth 10 from the individual 7-stone root only;
REFUTED-D10 is not a LOSS proof; receipt folds are manifest-coverage
bookkeeping. The 11x11 empty board, the two-stone roots {49,60} and {59,60},
S2 {59,60}, and classes 1/2/4 all remain UNKNOWN.
"""
import json
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SCRIPTS = HERE / "scripts"
OUT = HERE / "output"
sys.path.insert(0, str(SCRIPTS))
from legal_candidates import legal_candidates  # noqa: E402

P_TARGET = "00000000000000403800000008000000"     # next pure class-2 target
P_COVER2 = "00000000000000801202000040000000"     # best coverable class-2
P_CLASS4 = "00000000020000003800000080000000"     # best class-4 blocker
HEAD_AFTER = (1452, 174, 6396, 506144, 4669, 370058)
FOLD_JSON = "class-frontier-cost76d77e-receipts-recompute-20261116.json"

# ---------- 1. reproduce head 1452 via the published fold script ----------
ns = runpy.run_path(str(SCRIPTS / "recompute_frontier_cost76d_77e_receipts_"
                        "20261116.py"))
pre = ns["pre"]
canon = ns["canon"]
covers = ns["covers"]
popcount = ns["popcount"]
reconstruct = ns["reconstruct"]
git_blob_sha = ns["git_blob_sha"]
ROOTS = ns["ROOTS"]
ORDER = ns["ORDER"]

manifest, classes, incidences, winners, rejected = pre.load_basis()
pre.manifest_holder[0] = manifest
frontier, summary = pre.make_frontier(classes, incidences, rejected)

basis_roots = reconstruct()
assert len(basis_roots) == 771
folded_canons = {canon(r) for r in basis_roots}
assert len(folded_canons) == 756
solved = set(winners)
for r in basis_roots:
    solved |= covers(r)
st_1450 = summary(solved)
assert tuple(st_1450[k] for k in
             ("solved_s6_in_manifest", "remaining_s5_orbits",
              "unique_remaining_s6", "sum_remaining_cost",
              "s6_needed_by_open_classes",
              "cost_needed_by_open_classes")) == (1450, 174, 6398, 506297,
                                                   4671, 370211)

receipts = []
for lane, bit in ORDER:
    root = int(ROOTS[(lane, bit)], 16)
    assert popcount(root) == 7
    c = canon(root)
    assert c not in folded_canons
    folded_canons.add(c)
    cov = covers(root)
    marg = cov - solved
    marg_m = marg & manifest
    receipts.append({
        "lane": f"cost-{lane}", "bit": bit, "root_hex": f"{root:032x}",
        "marginal": len(marg), "marginal_in_manifest": len(marg_m),
        "marginal_manifest_hexes": sorted(f"{x:032x}" for x in marg_m),
    })
    solved |= cov
st_1452 = summary(solved)
assert tuple(st_1452[k] for k in
             ("solved_s6_in_manifest", "remaining_s5_orbits",
              "unique_remaining_s6", "sum_remaining_cost",
              "s6_needed_by_open_classes",
              "cost_needed_by_open_classes")) == HEAD_AFTER

# tie the re-derivation to the published fold JSON (blob-pinned)
fold = json.loads((OUT / FOLD_JSON).read_text())
fa = fold["frontier_after_cost76d77e"]
assert [fa[k] for k in
        ("solved_s6_in_manifest", "remaining_s5_orbits", "unique_remaining_s6",
         "sum_remaining_cost", "s6_needed_by_open_classes",
         "cost_needed_by_open_classes")] == list(HEAD_AFTER)
t = fold["totals"]
assert t["win_bits"] == {"cost-76d": [19, 49], "cost-77e": [37, 69]}
assert t["total_marginal"] == 19 and t["total_marginal_in_manifest"] == 2
assert t["children_closed_by_bit"] == {"cost-76d": 19, "cost-77e": 37}
assert [(r["lane"], r["bit"], r["marginal"], r["marginal_in_manifest"])
        for r in fold["receipts"]] == \
    [("cost-76d", 19, 5, 1), ("cost-76d", 49, 4, 0),
     ("cost-77e", 37, 6, 1), ("cost-77e", 69, 4, 0)]
for rec, pub in zip(receipts, fold["receipts"]):
    assert rec["marginal"] == pub["marginal"]
    assert rec["marginal_in_manifest"] == pub["marginal_in_manifest"]
    assert rec["marginal_manifest_hexes"] == pub["marginal_manifest_hexes"]
print("CONTROL head 1452 reproduced (basis 1450 + 4 receipts); 775 receipt "
      "roots, 760 distinct D4 canons")

# ---------- 2. harvest the lane-local sweep verdict corpus ----------
def find_key(obj, names, depth=0):
    for n in names:
        if n in obj:
            return obj[n]
    if depth < 1:
        for k, v in obj.items():
            if k == "fold":
                continue          # fold.win_bits mixes two lanes' bits
            if isinstance(v, dict):
                r = find_key(v, names, depth + 1)
                if r is not None:
                    return r
    return None


harvest = {}
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
        pd = d.get("parent_derivation") or {}
        v = pd.get("s6_child") or pd.get("child")
        if isinstance(v, str) and len(v) == 32:
            child = v
    if child is None:
        skipped.append((name, "no child hex"))
        continue
    win_bits = find_key(d, ("win7_bits", "win7_d10_bits", "win_bits"))
    capped_bits = find_key(d, ("capped_bits",))
    capped_n = find_key(d, ("capped", "capped_count"))
    ref_bits = find_key(d, ("refuted_d10_bits", "refuted_bits"))
    ref_n = find_key(d, ("refuted_d10", "refuted_d10_count"))
    cands = d.get("legal_candidates") or d.get("candidate_bits")
    if win_bits is None:
        skipped.append((name, "no win bits"))
        continue
    if isinstance(win_bits, dict):
        win_bits = [b for v in win_bits.values() for b in v]
    win_bits = sorted(set(int(b) for b in win_bits))
    if cands is None:
        cands = sorted(legal_candidates(child)[1])
    else:
        cands = sorted(set(int(b) for b in cands))
        if name not in ("class2-lane-cost66c-inflight-20261116.json",):
            assert cands == sorted(legal_candidates(child)[1]), name
    if isinstance(capped_bits, dict):
        capped_bits = [b for v in capped_bits.values() for b in v]
    capped_bits = sorted(set(int(b) for b in capped_bits)) \
        if capped_bits else []
    if isinstance(ref_bits, dict):
        ref_bits = [b for v in ref_bits.values() for b in v]
    if ref_bits is None:
        if capped_n not in (None, 0, len(capped_bits)) or capped_bits:
            skipped.append((name, "capped bits unaccounted"))
            continue
        ref_bits = sorted(set(cands) - set(win_bits) - set(capped_bits))
    elif isinstance(ref_bits, list):
        ref_bits = sorted(set(int(b) for b in ref_bits))
    else:
        skipped.append((name, "refuted bits not a list"))
        continue
    if ref_n is not None and isinstance(ref_n, int) and ref_n != len(ref_bits):
        skipped.append((name, f"refuted count {ref_n} != {len(ref_bits)}"))
        continue
    if set(win_bits) | set(ref_bits) | set(capped_bits) != set(cands) or \
            (win_bits and ref_bits and set(win_bits) & set(ref_bits)):
        skipped.append((name, "bit accounting mismatch"))
        continue
    child_v = int(child, 16)
    conflicts_here = []
    for b in win_bits:
        c = canon(child_v | (1 << b))
        e = harvest.get(c)
        if e and e["verdict"] != "WIN7-D10":
            conflicts_here.append((child, b, e["verdict"]))
        harvest[c] = {"verdict": "WIN7-D10",
                      "sources": e["sources"] + [name] if e else [name]}
    for b in ref_bits:
        c = canon(child_v | (1 << b))
        e = harvest.get(c)
        if e and e["verdict"] != "REFUTED-D10":
            conflicts_here.append((child, b, e["verdict"]))
        harvest[c] = {"verdict": "REFUTED-D10",
                      "sources": e["sources"] + [name] if e else [name]}
    assert not conflicts_here, conflicts_here
    harvest_files.append({
        "file": name, "git_blob_sha": git_blob_sha(path.read_bytes()),
        "child": child,
        "candidates": len(cands), "win7": len(win_bits),
        "refuted": len(ref_bits), "capped": len(capped_bits)})
print(f"harvest glob: {len(harvest_files)} files, {len(harvest)} distinct "
      f"verdict canons; skipped {len(skipped)}")

# validate bit-exact against the published 76d/77e raw batches (the retired
# v2 fold-complete claims carry two-lane win_bits maps and are skipped by
# the glob pass; the raw batches are the canonical bit-level records)
for prefix, ncand, win_bits in (("cost76d", 76, [19, 49]),
                                ("cost77e", 77, [37, 69])):
    bit_recs = {}
    for n in range(1, 11):
        for line in (OUT / f"class2-lane-{prefix}-raw-batch{n}"
                     "-20261116.jsonl").read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if "control" in r:
                assert r["loss"] is False and r["capped"] is False
                assert r["nodes"] == 3402, r
            else:
                assert r["bit"] not in bit_recs
                assert r["andclose"] is True and r["capped"] is False
                bit_recs[r["bit"]] = r
    assert len(bit_recs) == ncand
    child = ("00000000040000003800080008000000" if prefix == "cost76d"
             else "00000000040000809002000000004000")
    assert sorted(bit_recs) == sorted(legal_candidates(child)[1])
    raw_win = sorted(b for b, r in bit_recs.items() if r["loss"] is True)
    assert raw_win == win_bits, (prefix, raw_win)
    child_v = int(child, 16)
    agree = new_ = 0
    for b, r in bit_recs.items():
        c = canon(child_v | (1 << b))
        expect = "WIN7-D10" if r["loss"] is True else "REFUTED-D10"
        e = harvest.get(c)
        if e:
            assert e["verdict"] == expect, (prefix, b, expect, e)
            agree += 1
        else:
            harvest[c] = {"verdict": expect,
                          "sources": [f"{prefix}-raw-batches (fold v2)"]}
            new_ += 1
    harvest_files.append({
        "file": f"class2-lane-{prefix}-raw-batch1..10-20261116.jsonl",
        "git_blob_sha": "per-batch pinned in the 76d/77e fold script",
        "child": child, "candidates": ncand, "win7": len(win_bits),
        "refuted": ncand - len(win_bits), "capped": 0})
    print(f"{prefix} raw batches: {agree} canons cross-agree with the glob "
          f"harvest, {new_} new canons added")
print(f"harvest: {len(harvest_files)} files, {len(harvest)} distinct verdict "
      f"canons, win {sum(1 for v in harvest.values() if v['verdict'] == 'WIN7-D10')}"
      f" / refuted {sum(1 for v in harvest.values() if v['verdict'] == 'REFUTED-D10')}"
      f"; skipped {len(skipped)}")

# ---------- 3. family census at head 1452 ----------
def bit_status(row_hex, b):
    c = canon(int(row_hex, 16) | (1 << b))
    if c in folded_canons:
        return "receipt_win", c
    e = harvest.get(c)
    if e:
        return ("harvested_win" if e["verdict"] == "WIN7-D10"
                else "harvested_refuted"), c
    return "open", c


rem, uniq, dem, _ = frontier(solved)
family = {}
for parent in (P_TARGET, P_COVER2, P_CLASS4):
    rows = rem.get(parent, [])
    fam_rows = []
    fam_canon_open = {}
    fam_canon_receipt = set()
    fam_canon_harvested = set()
    occ = 0
    for r in sorted(rows, key=lambda r: (int(r["s6_s7_edge_cost"]),
                                         r["s6_hex"])):
        row_hex = r["s6_hex"]
        cost = int(r["s6_s7_edge_cost"])
        bits = sorted(legal_candidates(row_hex)[1])
        assert len(bits) == cost, (row_hex, len(bits), cost)
        per = {"receipt_win": 0, "harvested_win": 0,
               "harvested_refuted": 0, "open": 0}
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
        d = dem.get(row_hex, {})
        fam_rows.append({
            "s6_hex": row_hex, "cost": cost,
            "demand": {k: int(d.get(k, -1)) for k in ("c1", "c2", "c4")},
            "census": per, "open_after_census": per["open"]})
    family[parent] = {
        "s5_hex": parent, "classes": classes.get(parent, 0),
        "rows": fam_rows, "row_count": len(fam_rows),
        "sum_edge_cost": sum(r["cost"] for r in fam_rows),
        "occurrences": occ,
        "distinct_receipt_win_canons": len(fam_canon_receipt),
        "distinct_harvested_canons": len(fam_canon_harvested),
        "distinct_open_canons": len(fam_canon_open),
        "sum_open_after_census": sum(r["open_after_census"]
                                     for r in fam_rows)}
    print(f"family {parent}: rows {len(fam_rows)} occ {occ} "
          f"open canons {len(fam_canon_open)} "
          f"sum open after census {family[parent]['sum_open_after_census']}")

ft = family[P_TARGET]
assert ft["row_count"] == 18 and ft["sum_edge_cost"] == 1287
fc2 = family[P_COVER2]
assert fc2["row_count"] == 3 and fc2["sum_edge_cost"] == 211
fc4 = family[P_CLASS4]
assert fc4["row_count"] == 18 and fc4["sum_edge_cost"] == 1460

# ---------- 4. cheapest-row ranking + per-bit tables ----------
def best_open(fam):
    return sorted((r for r in fam["rows"] if r["open_after_census"] > 0),
                  key=lambda r: (r["open_after_census"], r["cost"],
                                 r["s6_hex"]))


bit_tables = {}
for parent in (P_TARGET, P_COVER2, P_CLASS4):
    for r in sorted(family[parent]["rows"],
                    key=lambda r: (r["cost"], r["s6_hex"]))[:6] + \
            best_open(family[parent])[:4]:
        row_hex = r["s6_hex"]
        if row_hex in bit_tables:
            continue
        tbl = []
        for b in sorted(legal_candidates(row_hex)[1]):
            st, c = bit_status(row_hex, b)
            tbl.append({"bit": b, "status": st, "root_canon": f"{c:032x}"})
        bit_tables[row_hex] = {"parent": parent, "cost": r["cost"],
                               "demand": r["demand"], "bits": tbl}

# ---------- 5. emit ----------
result = {
    "schema": "n11-class2-lane-next-target-presweep-1452-20261116-v1",
    "date": "2026-11-16",
    "chain_head": "1452/174/6396/506144/4669/370058",
    "method": ("stdlib python re-derivation on the published cost-76d/77e "
               "fold (runpy reproduction of the published fold script at "
               "head 1452 with every published pin re-asserted: the four "
               "receipt marginals, in-manifest marginals, child-closed-by "
               "bits, the three parent deltas and the new head); lane-local "
               "sweep-verdict harvest over every published class2-lane-cost "
               "claim/sweep JSON (glob + per-child bit accounting + "
               "cross-source conflict assertion); canonical-root census via "
               "the chain's D4 canon function; legal candidate enumeration "
               "via legal_candidates.py (independent exact-integer Bareiss "
               "4x4)"),
    "head_reproduction": {
        "basis_head": "1450/174/6398/506297/4671/370211",
        "head_after": "1452/174/6396/506144/4669/370058",
        "receipt_roots": 775, "distinct_d4_canons": 760,
        "fold_json": f"{FOLD_JSON} (git blob sha 8d4bc622f9da22b8754f"
                     "2e398e5481359656d956)"},
    "harvest": {
        "files": harvest_files, "skipped": skipped,
        "distinct_verdict_canons": len(harvest),
        "win7_d10": sum(1 for v in harvest.values()
                        if v["verdict"] == "WIN7-D10"),
        "refuted_d10": sum(1 for v in harvest.values()
                           if v["verdict"] == "REFUTED-D10"),
        "conflicts": 0},
    "census": family,
    "cheapest_open_rows": {
        parent: [{**r} for r in best_open(family[parent])[:8]]
        for parent in (P_TARGET, P_COVER2, P_CLASS4)},
    "bit_tables": bit_tables,
    "interpretation_guard": ("search-plan bookkeeping only; no engine "
                             "search was run, no verdict was created, no row "
                             "was closed; harvest coverage is best-effort "
                             "over published claim/sweep JSONs, so an 'open' "
                             "bit is only provably-open among published "
                             "artifacts; WIN7-D10 proves a first-player win "
                             "within depth 10 from the individual 7-stone "
                             "root only; REFUTED-D10 is not a LOSS proof; "
                             "11x11 empty board, two-stone roots {49,60} and "
                             "{59,60}, S2 {59,60}, and classes 1/2/4 all "
                             "remain UNKNOWN"),
}
out_path = OUT / "class2-lane-next-target-presweep-1452-20261116.json"
with open(out_path, "w") as f:
    json.dump(result, f, indent=1, sort_keys=True)
    f.write("\n")
print("wrote", out_path.name, "blob",
      git_blob_sha(out_path.read_bytes())[:12])
