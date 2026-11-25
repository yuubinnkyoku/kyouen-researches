#!/usr/bin/env python3
"""Fold the four cost-76d / cost-77e WIN7-D10 receipts (76d bits 19 and 49 of
the child 00000000040000003800080008000000, 77e bits 37 and 69 of the child
00000000040000809002000000004000; roots published and dual-verified as
certificates) into the canonical head 1450/174/6398/506297/4671/370211 (the
post-cost-66c-fold head, 2026-11-16).

Protocol (adapted from the published cost-66c fold,
recompute_frontier_cost66c_receipts_20261116.py, commit 0b737862; inputs
mirroring the pre-registration script preregister_cost76d_77e_fold_20261116.py,
commit 76e7bd8f):

1. blob-verify every input (claims v1, sweeps, 20 raw batches, v15
   crosschecks, determinism rerun, certificates, verify records, head-1450
   fold-projection tool + projection record, pre-registration JSON);
2. independently reconstruct the basis solved set of head 1450 (771 receipt
   roots, 756 distinct D4 canons) and assert the six head numbers, the demand
   histogram and the published cost-66c fold record;
3. re-derive both sweeps from the raw batches and re-assert the cross-engine
   v15 crosschecks, the 77e determinism rerun and the published aggregates;
4. re-hash all four certificates byte-for-byte (whole or joined parts) with
   the sorted-unique row property;
5. conflict census: 76 + 77 candidate D4 orbits, zero overlaps with the 771
   folded roots, the one cross-lane shared orbit (76d bit 86 == 77e bit 7,
   both REFUTED-D10, agreement), the four WIN roots pairwise distinct;
6. assert both children genuinely remain open at head 1450 on their two open
   class-2 parents each;
7. fold the four receipts in publication order (76d bit 19, 76d bit 49,
   77e bit 37, 77e bit 69) with per-receipt marginals and a set-equality
   control; every fold result is compared field-by-field against the
   pre-registration published before this fold (git blob d150d3118227f1f0-
   ed1b7b96a83c0ac96521bd27, commit 40d1e16b);
8. emit the new canonical head 1452/174/6396/506144/4669/370058, per-parent
   deltas, closed-row demand invariants, rankings, the fold JSON and the
   claim updates (76d v1 completed -> v2 fold-complete; 77e v1 in-flight ->
   v2 completed+fold; all v1 fields preserved, v1 restorable
   byte-identically).

Bookkeeping over published receipts only; solved counts measure manifest
coverage, not the game-theoretic value of any position; WIN7 certificates
prove a first-player win within depth 10 from the individual 7-stone roots
only; REFUTED-D10 is never a LOSS proof; the 11x11 empty board, two-stone
roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain UNKNOWN.
"""
import csv
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
SCRIPTS = HERE / "scripts"
sys.path.insert(0, str(SCRIPTS))

from fold_projection_head1450_tool_20261116 import (  # noqa: E402
    canon, covers, popcount, reconstruct, EXPECT_HEAD, HIST_1450,
    FOLD66C_JSON, FOLD66C_BLOB, git_blob_sha)
import preregister_cost76d_77e_fold_20261116 as pre  # noqa: E402

PREREG_JSON = "class2-lane-cost76d-77e-fold-preregistration-20261116.json"
PREREG_BLOB = "d150d3118227f1f0ed1b7b96a83c0ac96521bd27"
PREREG_COMMIT = "40d1e16b591242b5239da163dd9281f62aec2584"
PROJ_COMMIT = "e97ba632ee46edf7fb1fb36d2ee6ade3e2891baf"
TOOL_COMMIT = "f337939803a328cc987881e4447fea0e83aab801"
STERILITY_AUDIT = ("class2-lane-post-cost66c-top-candidates-sterility-"
                   "audit-20261116.json (commit 0e972b0d)")
AUDIT_STERILE_S5 = "00000000000000801202000000200000"  # 3 rows / 209, fully sterile
NEXT_S5 = "00000000000000403800000008000000"            # 18 rows / 1287, unswept unclaimed

CLAIM76 = "class2-lane-cost76d-inflight-20261116.json"
CLAIM76_V1_BLOB = "d2e40a3e4c3ff5002395c7dcf46d50977c3a4964"
CLAIM76_V1_COMMIT = "99848fd309b32f26cfe91f8fda0be03568425412"
CLAIM76_V2_SCHEMA = "n11-class2-lane-cost76d-fold-complete-20261116-v2"
CLAIM77 = "class2-lane-cost77e-inflight-20261116.json"
CLAIM77_V1_BLOB = "1cfa89e5b95b43dc497b439f9e1bfb4481c64669"
CLAIM77_V1_COMMIT = "e11268dac7ca62f642f4186d90160a200b43bec0"
CLAIM77_V2_SCHEMA = "n11-class2-lane-cost77e-completed-20261116-v2"

GZ_BLOBS = {
    "s5-remaining-after-reuse.csv.gz": "953eec41cab43f19849f31e5879cf5de932d9d3f",
    "s5-s6-remaining-incidences.csv.gz": "7f0d7f4ab87585515d67a393464b2472e5171001",
    "win7-reuse-hits.csv.gz": "9fdad0e922c00af813c5c398277f2bddaa3283cd",
}
MS5_BLOBS = {
    "ms5_s6_manifest_part1.csv": "6b30ad1b224ead35ffc999e1358e2451446adeeb",
    "ms5_s6_manifest_part2.csv": "8aff65fa2942e7be2ee1adf08ffea6a21a4a02c3",
    "ms5_s6_manifest_part3.csv": "203b0fbd071bfe5f4da8a6cd34fcf3a65670df23",
    "ms5_s6_manifest_part4.csv": "1ec608cc12842bd4472a3039fcc0514494e1960c",
    "ms5_s6_manifest_part5.csv": "e2aad9cef9f9a4af3bc659043631558408b6672b",
    "ms5_s6_manifest_part6.csv": "acc1a8b3869a9917be7dd1b55574c756b59b0351",
}

CHILD76 = pre.CHILD76
CHILD77 = pre.CHILD77
CHILD76_V = pre.CHILD76_V
CHILD77_V = pre.CHILD77_V
WIN76 = pre.WIN76
WIN77 = pre.WIN77
ROOTS = pre.ROOTS
ORDER = [("76d", 19), ("76d", 49), ("77e", 37), ("77e", 69)]
PARENT_A = pre.PARENT_A
PARENT_B76 = pre.PARENT_B76
PARENT_B77 = pre.PARENT_B77


def load_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]


def main():
    # ---------- 1. blob verification --------------------------------------
    for name, blob in pre.INPUT_BLOBS.items():
        assert git_blob_sha((OUT / name).read_bytes()) == blob, name
    assert git_blob_sha((OUT / PREREG_JSON).read_bytes()) == PREREG_BLOB
    assert git_blob_sha((OUT / pre.PROJ_JSON).read_bytes()) == pre.PROJ_JSON_BLOB
    assert git_blob_sha((SCRIPTS / pre.TOOL_SCRIPT).read_bytes()) == pre.TOOL_SCRIPT_BLOB
    assert git_blob_sha((OUT / FOLD66C_JSON).read_bytes()) == FOLD66C_BLOB
    ms5 = HERE.parent / "n11-s2-5960-milestone5-20261112" / "output"
    for name, blob in GZ_BLOBS.items():
        assert git_blob_sha((OUT / name).read_bytes()) == blob, name
    for name, blob in MS5_BLOBS.items():
        assert git_blob_sha((ms5 / name).read_bytes()) == blob, name
    assert git_blob_sha((OUT / CLAIM76).read_bytes()) == CLAIM76_V1_BLOB
    assert git_blob_sha((OUT / CLAIM77).read_bytes()) == CLAIM77_V1_BLOB
    print(f"CONTROL all {len(pre.INPUT_BLOBS) + 9} input artifacts blob-verified "
          f"(incl. claims v1, gz + ms5 sources, 66c fold JSON, prereg JSON "
          f"{PREREG_BLOB[:8]}, projection tool + record)")

    prereg = json.loads((OUT / PREREG_JSON).read_text())
    assert prereg["schema"] == "n11-class2-lane-cost76d-77e-fold-preregistration-20261116-v1"
    assert prereg["receipt_bits"] == {"cost-76d": WIN76, "cost-77e": WIN77}
    assert prereg["planned_fold_publication"]["fold_json"] == \
        "class-frontier-cost76d77e-receipts-recompute-20261116.json"
    assert prereg["planned_fold_publication"]["fold_script"] == \
        "recompute_frontier_cost76d_77e_receipts_20261116.py"
    claim76 = json.loads((OUT / CLAIM76).read_text())
    claim77 = json.loads((OUT / CLAIM77).read_text())
    assert claim76["schema"] == "n11-class2-lane-cost76d-inflight-20261116-v1"
    assert claim77["schema"] == "n11-class2-lane-cost77e-inflight-20261116-v1"
    assert claim76["status"] == "completed" and claim77["status"] == "in-flight"
    assert claim76["s6_child"] == CHILD76 and claim77["s6_child"] == CHILD77

    # ---------- 2. basis head 1450 ----------------------------------------
    basis_roots = reconstruct()
    folded_d4 = {canon(r) for r in basis_roots}
    assert len(basis_roots) == 771 and len(folded_d4) == 756
    manifest, classes, incidences, winners, rejected = pre.load_basis()
    pre.manifest_holder[0] = manifest
    frontier, summary = pre.make_frontier(classes, incidences, rejected)
    solved = set(winners)
    for r in basis_roots:
        solved |= covers(r)
    base_summary = summary(solved)
    got = [base_summary[k] for k in
           ("solved_s6_in_manifest", "remaining_s5_orbits", "unique_remaining_s6",
            "sum_remaining_cost", "s6_needed_by_open_classes",
            "cost_needed_by_open_classes")]
    assert got == EXPECT_HEAD, got
    assert base_summary["hist"] == HIST_1450, base_summary["hist"]
    fold66 = json.loads((OUT / FOLD66C_JSON).read_text())
    fa = fold66["frontier_after_cost66c"]
    assert [fa[k] for k in
            ("solved_s6_in_manifest", "remaining_s5_orbits", "unique_remaining_s6",
             "sum_remaining_cost", "s6_needed_by_open_classes",
             "cost_needed_by_open_classes")] == got
    assert prereg["basis_head_numbers"] == got == EXPECT_HEAD
    print(f"CONTROL basis head 1450 independently reconstructed: {got}, "
          f"771 receipt roots / 756 distinct D4 canons, histogram + 66c fold "
          f"record + prereg basis agree")

    # ---------- 3. sweep re-derivation ------------------------------------
    def rederive(prefix, ncand, win_bits, node_total, win_nodes):
        recs = {}
        for n in range(1, 11):
            rows = load_jsonl(OUT / f"class2-lane-{prefix}-raw-batch{n}-20261116.jsonl")
            ctrl = [r for r in rows if "control" in r]
            assert len(ctrl) == 1 and ctrl[0]["control"] == "pilot_d6"
            assert ctrl[0]["nodes"] == 3402 and ctrl[0]["loss"] is False \
                and ctrl[0]["capped"] is False
            for r in [x for x in rows if "bit" in x]:
                assert r["bit"] not in recs
                assert r["andclose"] is True and r["capped"] is False
                assert r["terminalStoneRange"] == [13, 17]
                recs[r["bit"]] = r
        assert len(recs) == ncand
        claim = claim76 if prefix == "cost76d" else claim77
        assert sorted(recs) == sorted(claim["legal_candidates"])
        win = sorted(b for b, r in recs.items() if r["loss"])
        assert win == win_bits and ncand - len(win) >= 0
        assert sum(r["nodes"] for r in recs.values()) == node_total
        for b in win_bits:
            assert recs[b]["nodes"] == win_nodes[b], b
        return recs

    recs76 = rederive("cost76d", 76, WIN76, pre.NODES76, pre.WIN_NODES76)
    recs77 = rederive("cost77e", 77, WIN77, pre.NODES77, pre.WIN_NODES77)
    assert claim76["completion"]["sweep"]["win7_d10_bits"] == WIN76
    assert claim76["completion"]["sweep"]["node_sum"] == pre.NODES76
    sw77 = json.loads((OUT / "class2-lane-cost77e-sweep-20261116.json").read_text())
    ag = sw77["aggregate"]
    assert (ag["candidates"], ag["win7_d10_bits"], ag["refuted_d10"], ag["capped"]) == \
        (77, WIN77, 75, 0)
    assert ag["total_nodes"] == pre.NODES77 and ag["win_node_sum"] == 4443282
    for lane, recs, win_bits, lines in (
            ("76d", recs76, WIN76,
             load_jsonl(OUT / "class2-lane-cost76d-v15-crosscheck-20261116.jsonl")),
            ("77e", recs77, WIN77,
             load_jsonl(OUT / "class2-lane-cost77e-v15-crosscheck-20261116.jsonl"))):
        pit = [r for r in lines if "control" in r]
        assert len(pit) == 1 and pit[0]["nodes"] == 5949 and pit[0]["loss"] is False
        bits = {r["bit"]: r for r in lines if "bit" in r}
        for b, r in bits.items():
            assert r["loss"] == recs[b]["loss"], (lane, b)
        for b in win_bits:
            assert b in bits and bits[b]["loss"] is True
    det = [r for r in load_jsonl(OUT / "class2-lane-cost77e-v16-determinism-rerun-20261116.jsonl")
           if "bit" in r]
    assert len(det) == 16
    for r in det:
        raw = recs77[r["bit"]]
        assert (r["loss"], r["nodes"], r["capped"]) == \
            (raw["loss"], raw["nodes"], raw["capped"]), r["bit"]
    print(f"CONTROL sweeps re-derived: 76d 76/76 WIN {WIN76} "
          f"({pre.NODES76} nodes) + 77e 77/77 WIN {WIN77} "
          f"({pre.NODES77} nodes), 0 capped, v15 anchors agree, 77e "
          f"determinism rerun (16 bits) node-exact")

    # ---------- 4. certificates byte-for-byte ------------------------------
    wman = json.loads((OUT / "class2-lane-cost76d-win7-certificates-20261116.json").read_text())
    certs76 = {c["bit"]: c for c in wman["certificates"]}
    cert_info = {}
    for bit in WIN76:
        c = certs76[bit]
        pc = c["published_cert"]
        assert c["root_hex"] == ROOTS[("76d", bit)] and c["child_hex"] == CHILD76
        assert c["verdict"] == "WIN7" and c["fbt_drops"] == 0 and c["fatal"] is None
        pre.check_cert_whole(
            OUT / f"class2-lane-cost76d-certificates/bit{bit}-root-{c['root_hex']}.cert",
            c["rows"], c["root_hex"], pc["md5"], pc["sha256"],
            pc["git_blob_sha"], pc["bytes"])
        cert_info[("76d", bit)] = {
            "rows": c["rows"], "sub_roots": c["sub_roots"],
            "extraction_nodes": c["extraction_nodes"],
            "md5": pc["md5"], "sha256": pc["sha256"],
            "git_blob_sha": pc["git_blob_sha"], "bytes": pc["bytes"]}
    assert wman["totals"]["rows"] == 78458
    for bit in WIN77:
        root_hex = ROOTS[("77e", bit)]
        rec = json.loads((OUT / f"tmp-cost77e/bit{bit}.cert-receipt.json").read_text())
        assert rec["root_hex"] == root_hex
        whole = b""
        for part in rec["parts"]:
            pd = (OUT / f"class2-lane-cost77e-certificates/{part['name']}").read_bytes()
            assert git_blob_sha(pd) == part["git_blob_sha"], part["name"]
            assert len(pd) == part["bytes"], part["name"]
            whole += pd
        assert len(whole) == rec["whole_bytes"]
        assert hashlib.md5(whole).hexdigest() == rec["whole_md5"]
        assert hashlib.sha256(whole).hexdigest() == rec["whole_sha256"]
        lines = whole.decode().splitlines()
        assert lines[0] == ("n11-terminal-strategy-v1 original_first_WIN7 "
                            "second_to_move_LOSS")
        assert lines[1] == f"root {root_hex}"
        hexes = [ln.split(" ")[0] for ln in lines[2:]]
        assert len(hexes) == rec["strategy_rows"] and hexes == sorted(set(hexes))
        bi = json.loads((OUT / f"tmp-cost77e/bit{bit}.bigint.json").read_text())
        assert bi["union_missing"] == 0 and bi["union_extra"] == 0
        assert bi["subroots_passed"] == 57 and bi["strategy_rows"] == rec["strategy_rows"]
        s = sw77["certificates"][f"bit{bit}"]
        assert s["md5"] == rec["whole_md5"] and s["bytes"] == rec["whole_bytes"]
        cert_info[("77e", bit)] = {
            "rows": rec["strategy_rows"], "sub_roots": 57,
            "extraction_nodes": None,  # not separately published for 77e
            "md5": rec["whole_md5"], "sha256": rec["whole_sha256"],
            "git_blob_sha": None, "bytes": rec["whole_bytes"]}
    print("CONTROL all four certificates re-hashed byte-for-byte (76d whole "
          "44,810 + 33,648 rows; 77e parts joined == whole 47,018 + 54,491 "
          "rows), sorted-unique rows, BigInt union 0/0")

    # ---------- 5. conflict census ----------------------------------------
    canons76 = {canon(CHILD76_V | (1 << b)) for b in claim76["legal_candidates"]}
    canons77 = {canon(CHILD77_V | (1 << b)) for b in claim77["legal_candidates"]}
    assert len(canons76) == 76 and len(canons77) == 77
    assert not (canons76 & folded_d4) and not (canons77 & folded_d4)
    cross = sorted(canons76 & canons77)
    assert len(cross) == 1
    cross_canon = cross[0]
    b76 = [b for b in claim76["legal_candidates"]
           if canon(CHILD76_V | (1 << b)) == cross_canon][0]
    b77 = [b for b in claim77["legal_candidates"]
           if canon(CHILD77_V | (1 << b)) == cross_canon][0]
    assert (b76, b77) == (pre.EXPECT_CROSS[1], pre.EXPECT_CROSS[2])
    assert recs76[b76]["loss"] is False and recs77[b77]["loss"] is False
    assert recs76[b76]["nodes"] == pre.EXPECT_CROSS[3]
    assert recs77[b77]["nodes"] == pre.EXPECT_CROSS[4]
    pre_cross = prereg["conflict_census"]["cross_lane_overlap"]
    assert pre_cross["d4_canonical_hex"] == f"{cross_canon:032x}"
    assert (pre_cross["cost-76d_bit"], pre_cross["cost-77e_bit"]) == (b76, b77)
    assert pre_cross["agreement"] is True
    win_vs = [int(h, 16) for h in ROOTS.values()]
    assert len({canon(v) for v in win_vs}) == 4
    for v in win_vs:
        assert v not in basis_roots and canon(v) not in folded_d4
    assert pre.WATCH_65O not in canons76 and pre.WATCH_65O not in canons77
    assert prereg["conflict_census"]["overlaps_with_folded_roots"] == 0
    print(f"CONTROL conflict census: zero overlaps with the 771 folded roots; "
          f"cross-lane orbit {cross_canon:032x} = 76d bit {b76} == 77e bit "
          f"{b77}, both REFUTED-D10 (agreement); WIN roots pairwise distinct")

    # ---------- 6. the children remain open at head 1450 ------------------
    rem_b, uniq_b, dem_b, open_b = frontier(solved)
    for child, parents in ((CHILD76, (PARENT_A, PARENT_B76)),
                           (CHILD77, (PARENT_A, PARENT_B77))):
        for h in parents:
            ch = [r for r in rem_b.get(h, []) if r["s6_hex"] == child]
            assert len(ch) == 1 and classes[h] == 2, (child, h)
        d = dem_b[child]
        assert (d["c1"], d["c2"], d["c4"]) == (0, 2, 0), (child, d)
    pre_children = prereg["children_open_before_fold"]
    assert pre_children[CHILD76]["open_parents"] == [PARENT_A, PARENT_B76]
    assert pre_children[CHILD77]["open_parents"] == [PARENT_A, PARENT_B77]
    for h, (rows, cost) in ((PARENT_A, (5, 364)), (PARENT_B76, (65, 5358)),
                            (PARENT_B77, (72, 5960))):
        rr = rem_b[h]
        assert len(rr) == rows and \
            sum(int(r["s6_s7_edge_cost"]) for r in rr) == cost, h
    print("CONTROL both children open at head 1450 on their two open class-2 "
          "parents each (5/364, 65/5358, 72/5960 asserted)")

    # ---------- 7. the four-receipt fold -----------------------------------
    s_cur = set(solved)
    addition = []
    child_closed_by = {}
    marg_union = set()
    for lane, bit in ORDER:
        root_v = int(ROOTS[(lane, bit)], 16)
        child_v = CHILD76_V if lane == "76d" else CHILD77_V
        cov = covers(root_v)
        assert child_v in cov
        marg = cov - s_cur
        marg_m = marg & manifest
        assert not (marg & marg_union), "receipt marginals must be disjoint"
        marg_union |= marg
        ci = cert_info[(lane, bit)]
        rec = {
            "lane": f"cost-{lane}",
            "bit": bit,
            "root_hex": ROOTS[(lane, bit)],
            "d4_canonical_hex": f"{canon(root_v):032x}",
            "d4_orbit_distinct_from_all_folded_roots": True,
            "certificate": ci,
            "covers": len(cov),
            "covers_hexes": sorted(f"{k:032x}" for k in cov),
            "marginal": len(marg),
            "marginal_hexes": sorted(f"{k:032x}" for k in marg),
            "marginal_in_manifest": len(marg_m),
            "marginal_manifest_hexes": sorted(f"{k:032x}" for k in marg_m),
            "marginal_non_manifest_hexes":
                sorted(f"{k:032x}" for k in marg - marg_m),
            "sweep_nodes": (pre.WIN_NODES76 if lane == "76d" else pre.WIN_NODES77)[bit],
        }
        addition.append(rec)
        if child_v in marg_m:
            child_closed_by[f"cost-{lane}"] = bit
        s_cur |= marg
    assert child_closed_by == {"cost-76d": 19, "cost-77e": 37}, child_closed_by
    assert child_closed_by == prereg["child_closed_by"]
    cov_all = set()
    for lane, bit in ORDER:
        cov_all |= covers(int(ROOTS[(lane, bit)], 16))
    assert s_cur == solved | cov_all, "set-equality control"
    total_marg = sum(a["marginal"] for a in addition)
    total_mim = sum(a["marginal_in_manifest"] for a in addition)
    assert (total_marg, total_mim) == (19, 2)
    st_after = summary(s_cur)
    got_after = [st_after[k] for k in
                 ("solved_s6_in_manifest", "remaining_s5_orbits",
                  "unique_remaining_s6", "sum_remaining_cost",
                  "s6_needed_by_open_classes", "cost_needed_by_open_classes")]
    assert got_after == [1452, 174, 6396, 506144, 4669, 370058], got_after
    assert st_after["solved_s6_in_manifest"] == 1450 + total_mim
    want_hist = {k: HIST_1450[k] + prereg["demand_histogram_deltas"].get(k, 0)
                 for k in HIST_1450}
    assert st_after["hist"] == want_hist, st_after["hist"]
    pre_proj = prereg["projected_head"]
    assert [pre_proj[k] for k in
            ("solved_s6_in_manifest", "remaining_s5_orbits", "unique_remaining_s6",
             "sum_remaining_cost", "s6_needed_by_open_classes",
             "cost_needed_by_open_classes")] == got_after
    for p_rec, a in zip(prereg["receipts"], addition):
        for k in ("lane", "bit", "root_hex", "d4_canonical_hex", "covers",
                  "covers_hexes", "marginal", "marginal_hexes",
                  "marginal_in_manifest", "marginal_manifest_hexes",
                  "marginal_non_manifest_hexes", "sweep_nodes"):
            assert p_rec[k] == a[k], (a["lane"], a["bit"], k)
        assert p_rec["d4_orbit_distinct_from_all_folded_roots"] is True
        assert p_rec["certified"] is True
    print("AFTER cost-76d/77e fold:", json.dumps(
        {k: v for k, v in st_after.items() if k != "hist"}, indent=1))
    print(f"total marginal={total_marg} marginal_in_manifest={total_mim}; "
          f"children closed by bits: {child_closed_by}; all receipt fields "
          f"agree field-by-field with the pre-registration")

    # ---------- 8. per-parent rows at the new head ------------------------
    rem_a, uniq_a, dem_a, open_a = frontier(s_cur)
    cov_hexes = {f"{k:032x}" for k in cov_all}
    parents_after = {}
    lost_detail = {}
    for h in sorted(rem_b):
        old = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_b[h]}
        new = {r["s6_hex"]: int(r["s6_s7_edge_cost"]) for r in rem_a.get(h, [])}
        lost = {k: v for k, v in old.items() if k not in new}
        if not lost:
            assert new == old, h
            continue
        assert set(lost) <= cov_hexes, (h, sorted(set(lost) - cov_hexes))
        assert new == {k: v for k, v in old.items() if k not in lost}, h
        parents_after[h] = {"s5_hex": h, "classes": classes.get(h, 0),
                            "rows": len(new),
                            "edge_cost": sum(new.values()),
                            "rows_before": len(old),
                            "edge_cost_before": sum(old.values())}
        lost_detail[h] = lost
    incidences2 = sum(len(v) for v in lost_detail.values())
    cost_delta = sum(sum(v.values()) for v in lost_detail.values())
    assert (incidences2, cost_delta) == (pre.EXPECT_INCIDENCES, pre.EXPECT_COST_DELTA)
    assert sorted(parents_after) == sorted([PARENT_A, PARENT_B76, PARENT_B77])
    for h, pa in parents_after.items():
        exp = pre.EXPECT_AFFECTED[h]
        assert (pa["rows_before"], pa["edge_cost_before"]) == \
            (exp["rows_before"], exp["edge_cost_before"]), h
        assert (pa["rows"], pa["edge_cost"]) == \
            (exp["rows_after"], exp["edge_cost_after"]), h
        assert sorted(lost_detail[h]) == exp["lost_rows_hexes"], h
        assert sum(lost_detail[h].values()) == exp["lost_edge_cost"], h
        p_pa = prereg["affected_parents"][h]
        assert p_pa["rows_before"] == pa["rows_before"] and \
            p_pa["rows_after"] == pa["rows"] and \
            p_pa["edge_cost_before"] == pa["edge_cost_before"] and \
            p_pa["edge_cost_after"] == pa["edge_cost"] and \
            sorted(p_pa["lost_rows_hexes"]) == sorted(lost_detail[h]), h
    closed_hexes = sorted({h for a in addition
                           for h in a["marginal_manifest_hexes"]})
    pre_closed = sorted(h for r in prereg["receipts"]
                        for h in r["marginal_manifest_hexes"])
    assert closed_hexes == pre_closed and closed_hexes == [CHILD76, CHILD77]
    assert set(open_b) - set(open_a) == {CHILD76, CHILD77}
    assert set(open_a) - set(open_b) == set()
    print("per-parent rows at the new head (touched parents): " + "; ".join(
        f"{k} {v['rows_before']}/{v['edge_cost_before']} -> "
        f"{v['rows']}/{v['edge_cost']}" for k, v in parents_after.items()))
    print(f"parent-row incidences {incidences2}, parent edge cost delta "
          f"{cost_delta}; open-needed set loses exactly the two children")

    # ---------- 9. closed-row demand invariants ---------------------------
    s_hex = {f"{k:032x}" for k in s_cur}
    for a in addition:
        for row_hex in a["marginal_manifest_hexes"]:
            assert row_hex in s_hex, row_hex
            dd = dem_b.get(row_hex)
            assert dd["c1"] == 0 and (dd["c2"] + dd["c4"]) > 0, (row_hex, dd)
    for child in (CHILD76, CHILD77):
        dd = dem_b[child]
        assert (dd["c1"], dd["c2"], dd["c4"]) == (0, 2, 0), dd

    # ---------- 10. rankings at the new head -------------------------------
    def best(rem, bit_):
        return sorted(
            ({"s5_hex": k, "classes": classes.get(k, 0),
              "remaining_s6_orbits": len(rows),
              "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"])
                                          for r in rows)}
             for k, rows in rem.items() if classes.get(k, 0) & bit_),
            key=lambda r: (r["remaining_s6_orbits"], r["remaining_s7_edge_cost"],
                           r["s5_hex"]))

    class2 = best(rem_a, 2)
    class4 = best(rem_a, 4)
    class1 = best(rem_a, 1)
    sterile = next((c for c in class2 if c["s5_hex"] == AUDIT_STERILE_S5), None)
    coverable = [c for c in class2 if c["s5_hex"] != AUDIT_STERILE_S5]
    pure2 = [c for c in coverable if c["classes"] == 2]
    next_target = next((c for c in pure2 if c["s5_hex"] == NEXT_S5), None)
    assert sterile is not None and sterile["remaining_s6_orbits"] == 3 \
        and sterile["remaining_s7_edge_cost"] == 209, sterile
    assert coverable[0]["s5_hex"] == PARENT_A and \
        coverable[0]["remaining_s6_orbits"] == 3 and \
        coverable[0]["remaining_s7_edge_cost"] == 211, coverable[0]
    assert coverable[1]["s5_hex"] == "00000000000000809082000000000000" and \
        coverable[1]["classes"] == 3 and \
        coverable[1]["remaining_s6_orbits"] == 10 and \
        coverable[1]["remaining_s7_edge_cost"] == 698, coverable[1]
    assert next_target is not None and \
        next_target["remaining_s6_orbits"] == 18 and \
        next_target["remaining_s7_edge_cost"] == 1287, next_target
    print("best class-4:", class4[0] if class4 else None)
    print("best class-1 (mixed 1+2):", class1[0] if class1 else None)
    print("best class-2 (fully sterile, receipt-unclosable):", sterile)
    print("best coverable class-2:", coverable[0])
    print("second coverable (bit-2 ranking):", coverable[1])
    print("effective next sweep target (pure class-2, unswept unclaimed):",
          next_target)

    result = {
        "schema": "n11-class-frontier-cost76d77e-receipts-20261116-v1",
        "date": "2026-11-16",
        "baseline_record": {
            "basis_head_1450": ("1450/174/6398/506297/4671/370211 (independently "
                                "reconstructed from the 764 published receipt "
                                "roots + the seven cost-66c WIN7-D10 receipt "
                                "roots of the published fold JSON "
                                "(8783993e5c73cc9697c3ca48aef981725f422be8) + "
                                "the 498 sweep winners; 771 roots / 756 "
                                "distinct D4 canons; identical to the published "
                                "cost-66c fold record and to the pre-"
                                "registration basis summary)"),
            "receipt_roots": {"count": 771, "distinct_d4_canons": 756},
            "claims": (f"cost-76d {CLAIM76} (v1 completed, git blob "
                       f"{CLAIM76_V1_BLOB}, commit {CLAIM76_V1_COMMIT}) and "
                       f"cost-77e {CLAIM77} (v1 in-flight, git blob "
                       f"{CLAIM77_V1_BLOB}, commit {CLAIM77_V1_COMMIT}); both "
                       "superseded by the v2 fold-complete claim updates in "
                       "this fold"),
            "sweeps": ("20 raw batch JSONLs (v16), all blob-pinned: 76d 76/76 "
                       "candidates = WIN7-D10 bits [19, 49] + 74 REFUTED-D10, "
                       "0 capped, 96246915 nodes + 10 pilots x 3402 "
                       "(sweep audit + claim completed, commit eba444aa); 77e "
                       "77/77 = WIN7-D10 bits [37, 69] + 75 REFUTED-D10, "
                       "0 capped, 116019458 nodes + 10 pilots x 3402 (sweep "
                       "record class2-lane-cost77e-sweep-20261116.json, git "
                       "blob 57afde38..., commit 35b8ccee); v15 crosschecks "
                       "(76d anchors 19/49, 77e anchors 0/37/69) verdict-"
                       "agree; 77e determinism rerun batches 4+6 (16 bits) "
                       "node-exact; 76d determinism batches 3+5 node-exact "
                       "(claim note)"),
            "certificates": ("all four WIN7-D10 certificates re-hashed "
                             "byte-for-byte: 76d bit19 44,810 rows / 1,618,698 B "
                             "and bit49 33,648 rows / 1,215,488 B (manifest "
                             "class2-lane-cost76d-win7-certificates-20261116.json, "
                             "git blob e8a6116a..., commit 6c3432d5; Bareiss "
                             "55/54 sub-roots PASS); 77e bit37 47,018 rows / "
                             "1,695,679 B and bit69 54,491 rows / 1,964,949 B "
                             "(parts joined == whole; BigInt union 0/0 with "
                             "57/57 sub-roots each); second independent "
                             "verification VERIFICATION PASSED (git blob "
                             "d267fa8d..., commit ce88e071)"),
            "preregistration": (f"class2-lane-cost76d-77e-fold-preregistration-"
                                f"20261116.json (git blob {PREREG_BLOB}, commit "
                                f"{PREREG_COMMIT}, published before this fold; "
                                "every machine-checkable field re-derived and "
                                "compared here), projection artifact "
                                f"{pre.PROJ_JSON} (git blob {pre.PROJ_JSON_BLOB}, "
                                f"commit {PROJ_COMMIT}), tool "
                                f"{pre.TOOL_SCRIPT} (git blob "
                                f"{pre.TOOL_SCRIPT_BLOB}, commit {TOOL_COMMIT})"),
            "sterility_audit": STERILITY_AUDIT,
        },
        "method": ("independent basis reconstruction of head 1450 (published "
                   "fold-projection tool), re-derivation of both sweeps from "
                   "the 20 blob-pinned raw batches with the v15 crosschecks "
                   "and the 77e determinism rerun, re-hashing of all four "
                   "certificates byte-for-byte, 153-candidate-orbit conflict "
                   "census vs the 771 folded roots (zero overlaps; one "
                   "cross-lane shared orbit 00000000040000809002000000004080 = "
                   "76d bit 86 == 77e bit 7, both REFUTED-D10, agreement), the "
                   "children-remaining fact asserted on both open parents "
                   "each, then the four receipts folded in publication order "
                   "(76d bit 19, 76d bit 49, 77e bit 37, 77e bit 69) with "
                   "per-receipt marginals, a set-equality control and "
                   "field-by-field agreement with the pre-registration"),
        "receipts": addition,
        "totals": {
            "receipts": 4,
            "win_bits": {"cost-76d": WIN76, "cost-77e": WIN77},
            "root_hexes": [ROOTS[k] for k in ORDER],
            "total_marginal": total_marg,
            "total_marginal_in_manifest": total_mim,
            "children_closed_by_bit": child_closed_by,
            "conflict_census_overlaps": 0,
            "folded_roots_at_1450": {"receipt_roots": 771,
                                     "distinct_d4_canons": 756},
            "cross_lane_overlap": {
                "d4_canonical_hex": f"{cross_canon:032x}",
                "cost-76d_bit": b76, "cost-77e_bit": b77,
                "verdicts": ["REFUTED-D10", "REFUTED-D10"],
                "agreement": True},
            "rows_closed_hexes": closed_hexes,
            "sweep_nodes_76d": pre.NODES76,
            "sweep_nodes_77e": pre.NODES77,
            "parent_row_incidences": incidences2,
            "parent_edge_cost_delta": cost_delta,
        },
        "frontier_after_cost76d77e": {
            "solved_s6_in_manifest": st_after["solved_s6_in_manifest"],
            "remaining_s5_orbits": st_after["remaining_s5_orbits"],
            "unique_remaining_s6": st_after["unique_remaining_s6"],
            "sum_remaining_cost": st_after["sum_remaining_cost"],
            "s6_needed_by_open_classes": st_after["s6_needed_by_open_classes"],
            "cost_needed_by_open_classes": st_after["cost_needed_by_open_classes"],
            "demand_histogram_open_only": st_after["hist"],
            "best_class2_fully_sterile": sterile,
            "best_class4": class4[0] if class4 else None,
            "best_class1": class1[0] if class1 else None,
            "best_coverable_class2": coverable[0],
            "second_coverable_class2": coverable[1] if len(coverable) > 1 else None,
            "next_pure_class2_sweep_target": next_target,
        },
        "parents_after": parents_after,
        "lost_rows_per_parent": lost_detail,
        "interpretation_guard": ("bookkeeping over published receipts; solved "
                                "counts measure manifest coverage, not the "
                                "game-theoretic value of any position; WIN7 "
                                "certificates prove a first-player win within "
                                "depth 10 from the individual 7-stone roots "
                                "only; REFUTED-D10 proves only absence of "
                                "WIN7-D10 from that root and is never a LOSS "
                                "proof; 11x11 empty board / two-stone roots "
                                "{49,60} and {59,60} / S2 {59,60} / class 1 / "
                                "class 2 / class 4 remain UNKNOWN"),
    }
    (OUT / "class-frontier-cost76d77e-receipts-recompute-20261116.json"
     ).write_text(json.dumps(result, indent=1) + "\n")
    print("written class-frontier-cost76d77e-receipts-recompute-20261116.json")

    ranking = sorted(
        ({"s5_hex": k, "classes": classes.get(k, 0),
          "remaining_s6_orbits": len(rows),
          "remaining_s7_edge_cost": sum(int(r["s6_s7_edge_cost"])
                                        for r in rows)}
         for k, rows in rem_a.items()),
        key=lambda r: (0 if r["classes"] & 6 else 1, r["remaining_s6_orbits"],
                       r["remaining_s7_edge_cost"], r["s5_hex"]))
    with (OUT / ("class-frontier-s5-ranking-after-cost76d77e-"
                 "receipts-20261116.csv")).open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(("s5_hex", "classes", "remaining_s6_orbits",
                    "remaining_s7_edge_cost"))
        for r in ranking:
            w.writerow((r["s5_hex"], r["classes"], r["remaining_s6_orbits"],
                        r["remaining_s7_edge_cost"]))

    with (OUT / ("class-frontier-top-candidates-s6-after-cost76d77e-"
                 "receipts-20261116.csv")).open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        for label, cand in (("best class-4 blocker-candidate S5",
                             class4[0] if class4 else None),
                            ("best class-1 blocker-candidate S5",
                             class1[0] if class1 else None),
                            ("best class-2 S5 (fully sterile, "
                             "receipt-unclosable per the post-cost-66c "
                             "sterility audit)", sterile),
                            ("best coverable class-2 blocker-candidate S5",
                             coverable[0] if coverable else None),
                            ("second coverable class-2 candidate S5 "
                             "(bit-2 ranking)",
                             coverable[1] if len(coverable) > 1 else None),
                            ("effective next sweep target S5 (pure class-2, "
                             "unswept unclaimed per the post-cost-66c "
                             "sterility audit)",
                             next_target)):
            if cand is None:
                continue
            w.writerow([f"# {label}: s5={cand['s5_hex']} "
                        f"classes={cand['classes']} "
                        f"remaining={cand['remaining_s6_orbits']} "
                        f"cost={cand['remaining_s7_edge_cost']}"])
            w.writerow(("s5_hex", "s6_hex", "s6_s7_edge_cost", "demand"))
            for row in sorted(rem_a.get(cand["s5_hex"], []),
                              key=lambda r: int(r["s6_s7_edge_cost"])):
                dd = dem_a.get(row["s6_hex"],
                               {"c1": -1, "c2": -1, "c4": -1})
                w.writerow((cand["s5_hex"], row["s6_hex"],
                            row["s6_s7_edge_cost"],
                            f"c1={dd['c1']},c2={dd['c2']},c4={dd['c4']}"))
    print("written ranking + top-candidates CSVs (after-cost76d77e-receipts)")

    # ---------- 11. claim updates ------------------------------------------
    fold_json_sha = git_blob_sha(
        (OUT / "class-frontier-cost76d77e-receipts-recompute-20261116.json")
        .read_bytes())
    head_before = "1450/174/6398/506297/4671/370211"
    head_after = (f"{st_after['solved_s6_in_manifest']}/"
                  f"{st_after['remaining_s5_orbits']}/"
                  f"{st_after['unique_remaining_s6']}/"
                  f"{st_after['sum_remaining_cost']}/"
                  f"{st_after['s6_needed_by_open_classes']}/"
                  f"{st_after['cost_needed_by_open_classes']}")

    fold_record = {
        "schema": "n11-class2-lane-cost76d-77e-fold-20261116-v1",
        "fold_json": ("class-frontier-cost76d77e-receipts-recompute-20261116.json"
                      " (git blob sha " + fold_json_sha + ")"),
        "preregistration": ("class2-lane-cost76d-77e-fold-preregistration-"
                            "20261116.json (git blob sha " + PREREG_BLOB +
                            ", commit " + PREREG_COMMIT + ", published "
                            "before the fold; field-by-field agreement "
                            "asserted by the fold script)"),
        "head_before": head_before,
        "head_after": head_after,
        "receipts": 4,
        "win_bits": {"cost-76d": WIN76, "cost-77e": WIN77},
        "root_hexes": [ROOTS[k] for k in ORDER],
        "total_marginal": total_marg,
        "total_marginal_in_manifest": total_mim,
        "children_closed_by_bit": child_closed_by,
        "parent_row_incidences": incidences2,
        "parent_edge_cost_delta": cost_delta,
        "parents_after": parents_after,
        "conflict_census": ("zero overlaps with the 771 folded roots; cross-"
                            f"lane orbit {cross_canon:032x} = 76d bit {b76} "
                            f"== 77e bit {b77}, both REFUTED-D10, agreement"),
    }

    # cost-76d: v1 completed -> v2 fold-complete
    claim_path76 = OUT / CLAIM76
    t = json.loads(claim_path76.read_text())
    rt = json.dumps(t, indent=2) + "\n"
    assert git_blob_sha(rt.encode()) == CLAIM76_V1_BLOB, \
        "76d v1 round-trip is not byte-identical"
    claim76v2 = {k: v for k, v in claim76.items()}
    claim76v2["schema"] = CLAIM76_V2_SCHEMA
    claim76v2["status"] = (
        "FOLD COMPLETE on 2026-11-16 by the long-term lane session: the two "
        "WIN7-D10 receipts (bits 19 and 49, roots published and dual-verified "
        "as certificates) are folded together with the two cost-77e receipts "
        "on the head-1450 basis (independent reconstruction of the published "
        "fold chain state; every input blob-pinned) - the child row closes in "
        "the manifest exactly once (child closed by bit 19) and the shared "
        "second-coverable class-2 S5 loses both in-flight rows; every fold "
        "result agrees field-by-field with the pre-registration published "
        "before the fold (git blob " + PREREG_BLOB + ", commit " +
        PREREG_COMMIT + "); new canonical head " + head_after + "; conflict "
        "census vs the 771 folded roots (756 D4 canons) at 1450: zero "
        "overlaps, zero WIN/LOSS conflicts (the one cross-lane shared orbit "
        "00000000040000809002000000004080 = 76d bit 86 == 77e bit 7 is "
        "REFUTED-D10 in both sweeps, agreement); all v1 fields preserved (v1 "
        "restorable byte-identically from the fold record); 11x11 empty "
        "board, two-stone roots {49,60} and {59,60}, S2 {59,60}, and classes "
        "1/2/4 all remain UNKNOWN")
    claim76v2["supersedes"] = ("v1 (completed claim, git blob sha " +
                              CLAIM76_V1_BLOB + ", commit " +
                              CLAIM76_V1_COMMIT + ", all fields preserved)")
    claim76v2["fold"] = dict(fold_record)
    claim_path76.write_text(json.dumps(claim76v2, indent=2) + "\n")

    # cost-77e: v1 in-flight -> v2 completed + fold
    claim_path77 = OUT / CLAIM77
    t = json.loads(claim_path77.read_text())
    rt = json.dumps(t, indent=1) + "\n"
    assert git_blob_sha(rt.encode()) == CLAIM77_V1_BLOB, \
        "77e v1 round-trip is not byte-identical"
    claim77v2 = {k: v for k, v in claim77.items()}
    claim77v2["schema"] = CLAIM77_V2_SCHEMA
    claim77v2["status"] = (
        "COMPLETED and FOLD COMPLETE on 2026-11-16 by the long-term lane "
        "session: the 77-candidate sweep finished WIN7-D10 bits [37, 69] + "
        "75 REFUTED-D10, 0 capped, 116019458 nodes + 10 pilots x 3402 "
        "(published as class2-lane-cost77e-sweep-20261116.json, git blob "
        "57afde38509ae3c10df0c6c38883c9b5d4fc67a5, commit 35b8ccee, with all "
        "ten raw batches blob-pinned, the v15 crosscheck (anchors 0/37/69) "
        "and the v16 determinism rerun of batches 4+6, 16 bits node-exact); "
        "both WIN7 roots are certified (bit37 47,018 rows / bit69 54,491 "
        "rows, parts joined == whole, BigInt union 0/0 with 57/57 sub-roots "
        "each) and dual-independently verified together with the cost-76d "
        "artifacts (class2-lane-cost76d-77e-second-independent-verification-"
        "20261116.json, VERIFICATION PASSED, git blob d267fa8d93017110ff74"
        "df4520b3a8e8a47bee5b, commit ce88e071); the two receipts are folded "
        "together with the two cost-76d receipts on the head-1450 basis "
        "(every input blob-pinned) - the child row closes in the manifest "
        "exactly once (child closed by bit 37) and the shared second-"
        "coverable class-2 S5 loses both in-flight rows; every fold result "
        "agrees field-by-field with the pre-registration published before "
        "the fold (git blob " + PREREG_BLOB + ", commit " + PREREG_COMMIT +
        "); new canonical head " + head_after + "; conflict census vs the "
        "771 folded roots (756 D4 canons) at 1450: zero overlaps, zero "
        "WIN/LOSS conflicts (the one cross-lane shared orbit "
        "00000000040000809002000000004080 = 76d bit 86 == 77e bit 7 is "
        "REFUTED-D10 in both sweeps, agreement); all v1 fields preserved "
        "(v1 restorable byte-identically from the fold record); 11x11 empty "
        "board, two-stone roots {49,60} and {59,60}, S2 {59,60}, and classes "
        "1/2/4 all remain UNKNOWN")
    claim77v2["supersedes"] = ("v1 (in-flight claim, git blob sha " +
                              CLAIM77_V1_BLOB + ", commit " +
                              CLAIM77_V1_COMMIT + ", all fields preserved)")
    claim77v2["completion"] = {
        "sweep": ("class2-lane-cost77e-sweep-20261116.json (git blob "
                  "57afde38509ae3c10df0c6c38883c9b5d4fc67a5, commit "
                  "35b8ccee): 77 candidates = WIN7-D10 bits [37, 69], "
                  "REFUTED-D10 75, capped 0 (all within depth 10, terminal "
                  "stone range [13,17], andclose true), total_nodes "
                  "116019458, win7_d10_nodes {bit37: 1819936, bit69: "
                  "2623346}; raw batches class2-lane-cost77e-raw-batch1..10-"
                  "20261116.jsonl all blob-pinned; v15 crosscheck anchors "
                  "0/37/69 verdict-agree; determinism rerun batches 4+6 "
                  "(16 bits) node-exact"),
        "certificates": ("bit37 47,018 rows / 1,695,679 B and bit69 54,491 "
                         "rows / 1,964,949 B, published as parts in "
                         "class2-lane-cost77e-certificates/ with receipts, "
                         "BigInt and tsverify records in tmp-cost77e/ (all "
                         "blob-pinned); dual independent verification: "
                         "verify_win7_certificate_bigint_independent.mjs "
                         "(57/57 sub-roots each, union 0/0, terminal "
                         "[13,17]) + ts Bareiss row checks; second "
                         "independent verification of the whole 76d+77e "
                         "corpus: class2-lane-cost76d-77e-second-independent-"
                         "verification-20261116.json (VERIFICATION PASSED, "
                         "commit ce88e071)"),
        "verdict_semantics_note": claim77["verdict_semantics"],
    }
    claim77v2["fold"] = dict(fold_record)
    claim_path77.write_text(json.dumps(claim77v2, indent=1) + "\n")

    for p in ("class-frontier-cost76d77e-receipts-recompute-20261116.json",
              "class-frontier-s5-ranking-after-cost76d77e-receipts-20261116.csv",
              "class-frontier-top-candidates-s6-after-cost76d77e-"
              "receipts-20261116.csv",
              CLAIM76, CLAIM77):
        data = (OUT / p).read_bytes()
        sha = git_blob_sha(data)
        blen = len(data)
        print(f"blob {p}: {sha} ({blen} bytes)")
    print(f"new canonical head: {head_before} -> {head_after}")


if __name__ == "__main__":
    main()
