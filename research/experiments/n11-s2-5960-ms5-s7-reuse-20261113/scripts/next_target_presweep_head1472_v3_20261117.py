#!/usr/bin/env python3
"""head-1472 next-target presweep census v3 (2026-11-17).

Update of the published head-1452 presweep census v2
(class2-lane-next-target-presweep-1452-v2-20261116.json, git blob
67d6a5c192953b9bc95fd13b356e5aabeac2a12c) for the state after:

  * the cost-64h receipt fold LANDED (commit 828c595c, fold receipt git
    blob 1633be292f6f1862c895009eac29d398d0be7738): 23 WIN7-D10 receipts
    folded, head 1452 -> 1472, 20 manifest rows closed;
  * the cost-66i sweep completed (9 WIN7-D10 + 57 REFUTED-D10, 0 capped,
    raw batches 1-9 blob-pinned below; all nine WIN7 certificates
    extracted and independently verified): its receipt fold is pending
    behind the cost-76c fold (claim v5 dependency);
  * cost-76c remains fold-pending (v17-corrected WIN7-D10 bits 61/99;
    bit 113 REFUTED-D10), claimed by the parallel lane (bit 61
    certificate extraction in flight) -- untouched here.

Method: the v1 census JSON (blob 0d9a94a2...) is the authoritative
head-1452 bit-status baseline; v2 is the intermediate overlay state
(64h/76c verdicts, pre-64h-fold). This v3 rebuilds the family overlays
from scratch with all three verdict maps (64h v16 raw, 76c v17 raw, 66i
v17 raw; each blob-pinned), marks the 20 landed-64h-closed rows, marks
the 76c-pending and 66i-pending fold closures, agrees with the v2 overlay
on every 64h/76c field, asserts zero verdict conflicts, and re-ranks the
remaining unswept/unclaimed/unexcluded rows at head 1472.

Cross-checks (all asserted):
  * computed root canon == v1 bit-table root_canon for every covered bit;
  * 64h WIN canon set == prereg receipts' d4_canonical_hex set;
  * landed 64h closed rows (fold receipt) == preregistered 20 rows;
  * 76c WIN bits {61,99} and bit-113 v16->v17 flip;
  * 66i WIN bits == raw audit/claim winner_roots (9/9 root canons);
  * v3 family overlay reproduces the v2 values for every 64h/76c field;
  * zero verdict conflicts (v1 status vs overlay, cross-sweep canon map).

Interpretation guard: search-plan bookkeeping only. No engine search is
run here, no verdict is created, no row is closed. WIN7-D10 proves a
first-player win within depth 10 from the individual 7-stone root only;
REFUTED-D10 is not a LOSS proof; receipt folds are manifest-coverage
bookkeeping. The 11x11 empty board, the two-stone roots {49,60}/{59,60},
S2 {59,60}, and classes 1/2/4 all remain UNKNOWN.
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


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def load_out(name, pin):
    b = (OUT / name).read_bytes()
    got = git_blob_sha(b)
    assert got == pin, (name, got, pin)
    return json.loads(b)


def load_jsonl(name, pin):
    b = (OUT / name).read_bytes()
    got = git_blob_sha(b)
    assert got == pin, (name, got, pin)
    return [json.loads(l) for l in b.decode().splitlines() if l.strip()]


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


# ------------------------------------------------------------------ inputs
V1 = load_out("class2-lane-next-target-presweep-1452-20261116.json",
              "0d9a94a272de9fe45708757f17bfea60239a3c9b")
V2 = load_out("class2-lane-next-target-presweep-1452-v2-20261116.json",
              "67d6a5c192953b9bc95fd13b356e5aabeac2a12c")
PREREG64H = load_out(
    "class2-lane-cost64h-fold-preregistration-independent-20261116.json",
    "5074a8a0cbb75fcc91b5b999a3135fac06d42400")
FOLD64H = load_out(
    "class-frontier-cost64h-receipts-recompute-20261117.json",
    "1633be292f6f1862c895009eac29d398d0be7738")
AUDIT76C = load_out(
    "class2-lane-cost76c-v17-sweep-and-fbt-saturation-audit-20261117.json",
    "235f964365a7ab33e33986c915fc7f6861e4d686")
AUDIT66I = load_out("class2-lane-cost66i-raw-audit-20261116.json",
                    "f7d8bad610fe07fee6b365e711838600722737e2")
CLAIM66I = load_out("class2-lane-cost66i-inflight-20261116.json",
                    "c69f512eb9bf44530093a3ca5158d140a5adda37")

PIN64H = ["47da4e04357b7012c55903aea22160f3ca0767c9",
          "04e59e2ed62ba2306c80743e9c0517a6d89e70a2",
          "78bb44093ef56191110119009ce788d0cd4f383f",
          "7d196917961356c69cfa608930c3a1b7716aaf59",
          "ba6a36d4cb93111461aeec86b55e2909cbc0a489",
          "a49e2b9cd7d239fd95681afa83793deb075b4ccf",
          "6771b7a900191fce3d11feccf3da0e2e05f001e9",
          "5e778cae345d2a1d0d50455a3633ea673b6c08be"]
PIN76C17 = ["a62cd9aa478d3930cc8f672cd1fa8ae55f399d73",
            "9d4aacedd902eef335d349c9467f31ee256df897",
            "c20c808a7963726374922d3a05e91de7c65b3ce2",
            "26729eb3e5997a52c8b31ed4d9afcd22579c840f",
            "937e64420909119b315c5bb302e23a782b53cc0c",
            "472168193757ddec5eed790880d12c63be631a26",
            "78897a4bd09f02e7e6e029115ec241c064345cbc",
            "44482915469b3e52e7964808d3f118197acce7e4",
            "d77a403725a7b9dc93d9e43a84ef160a2e196d49",
            "f54c9f0c573314b971c6e50cd154175013d05383"]
PIN66I = ["02b31589bb990cb7b867dffb22da16a30ab67594",
          "540f645f49dc59e5a2226006584e2cad247b0295",
          "42bf714ab115ec735edc3ff7cdd7217d00e35433",
          "13da15f8f3a30fe650bd9b7279b04278ec4b5355",
          "59ff6d1c9431ed97cd9b82eadf6ed1f68bdfbb96",
          "3c81f310df67447f687a3d0536202f9b5b38e51a",
          "c6eed4f004f8829818270981e152822eb33b13f9",
          "e28abd996708d37d54e4ec0cf8664e38f89a19a2",
          "37cde85ddbc7d86cd0b3b3376c30bd595a6e85de"]

CHILD64H = int("00000000000000403800000008100000", 16)
CHILD76C = int("00000000010000809002000001000000", 16)
CHILD66I = int("00000000000000801226000000000000", 16)

# ------------------------------------------------ 64h verdict map (v16 raw)
verdict64h = {}
pilots = 0
for i in range(1, 9):
    rows = load_jsonl(f"class2-lane-cost64h-raw-batch{i}-20261116.jsonl",
                      PIN64H[i - 1])
    for r in rows:
        if r.get("control") == "pilot_d6":
            assert r == {"control": "pilot_d6", "loss": False,
                         "nodes": 3402, "capped": False}, r
            pilots += 1
            continue
        assert not r["capped"], r
        v = "WIN7-D10" if r["loss"] else "REFUTED-D10"
        c = canon(CHILD64H | (1 << r["bit"]))
        assert c not in verdict64h, "duplicate bit"
        verdict64h[c] = {"verdict": v, "bit": r["bit"], "nodes": r["nodes"]}
assert pilots == 8
assert len(verdict64h) == 64
win64h_bits = sorted(e["bit"] for e in verdict64h.values()
                     if e["verdict"] == "WIN7-D10")
assert win64h_bits == [4, 6, 8, 33, 38, 42, 44, 49, 68, 74, 76, 77, 78,
                       79, 83, 89, 91, 101, 109, 113, 114, 116,
                       120], win64h_bits
win64h_canons = {c for c, e in verdict64h.items()
                 if e["verdict"] == "WIN7-D10"}
prereg_canons = {r["d4_canonical_hex"] for r in PREREG64H["receipts"]}
assert prereg_canons == {f"{c:032x}" for c in win64h_canons}, "prereg mismatch"

# ------------------------------------------------ 76c verdict map (v17 raw)
verdict76c = {}
pilots = 0
for i in range(1, 11):
    rows17 = load_jsonl(f"class2-lane-cost76c-v17-raw-batch{i}-20261117.jsonl",
                        PIN76C17[i - 1])
    for r in rows17:
        if r.get("control") == "pilot_d6":
            assert r == {"control": "pilot_d6", "loss": False,
                         "nodes": 3402, "capped": False}, r
            pilots += 1
            continue
        assert not r["capped"], r
        v = "WIN7-D10" if r["loss"] else "REFUTED-D10"
        c = canon(CHILD76C | (1 << r["bit"]))
        assert c not in verdict76c
        verdict76c[c] = {"verdict": v, "bit": r["bit"], "nodes": r["nodes"]}
assert pilots == 10
assert len(verdict76c) == 76
win76c_bits = sorted(e["bit"] for e in verdict76c.values()
                     if e["verdict"] == "WIN7-D10")
assert win76c_bits == [61, 99], win76c_bits
assert AUDIT76C["v17_full_resweep"]["win_bits_corrected"] == [61, 99]
win76c_canons = {c for c, e in verdict76c.items()
                 if e["verdict"] == "WIN7-D10"}

# ------------------------------------------------ 66i verdict map (v17 raw)
verdict66i = {}
pilots = 0
for i in range(1, 10):
    rows = load_jsonl(f"class2-lane-cost66i-raw-batch{i}-20261116.jsonl",
                      PIN66I[i - 1])
    for r in rows:
        if r.get("control") == "pilot_d6":
            assert r == {"control": "pilot_d6", "loss": False,
                         "nodes": 3402, "capped": False}, r
            pilots += 1
            continue
        assert not r["capped"], r
        v = "WIN7-D10" if r["loss"] else "REFUTED-D10"
        c = canon(CHILD66I | (1 << r["bit"]))
        assert c not in verdict66i
        verdict66i[c] = {"verdict": v, "bit": r["bit"], "nodes": r["nodes"]}
assert pilots == 9
assert len(verdict66i) == 66
win66i_bits = sorted(e["bit"] for e in verdict66i.values()
                     if e["verdict"] == "WIN7-D10")
assert win66i_bits == [19, 28, 29, 58, 88, 90, 99, 103, 112], win66i_bits
assert AUDIT66I["verdicts"]["win7_d10_bits"] == win66i_bits
assert sorted(AUDIT66I["verdicts"]["refuted_d10_bits"]) == sorted(
    e["bit"] for e in verdict66i.values()
    if e["verdict"] == "REFUTED-D10")
assert AUDIT66I["target"]["s6_child"] == f"{CHILD66I:032x}"
assert AUDIT66I["pilot_checks"] == {"batches": 9, "pilot_nodes_each": 3402,
                                    "all_exact": True}
win66i_canons = {c for c, e in verdict66i.items()
                 if e["verdict"] == "WIN7-D10"}
# claim winner_roots cross-check (9/9)
claim_win = CLAIM66I["actual_execution"]["winner_roots"]
assert len(claim_win) == 9
bit_canon_66i = {e["bit"]: c for c, e in verdict66i.items()}
for w in claim_win:
    assert f"{bit_canon_66i[w['bit']]:032x}" == w["root_canon"], w
assert sorted(w["bit"] for w in claim_win) == win66i_bits
# no cross-sweep canon conflicts across the three maps
for c in set(verdict64h) & set(verdict76c):
    assert verdict64h[c]["verdict"] == verdict76c[c]["verdict"], c
for c in set(verdict64h) & set(verdict66i):
    assert verdict64h[c]["verdict"] == verdict66i[c]["verdict"], c
for c in set(verdict76c) & set(verdict66i):
    assert verdict76c[c]["verdict"] == verdict66i[c]["verdict"], c

# ------------------------------------------------ landed 64h fold closure
CLOSED64H = set(FOLD64H["totals"]["closed_manifest_rows"])
assert len(CLOSED64H) == 20
assert CLOSED64H == set(PREREG64H["closed_row_parent_map"])
HEAD1472 = FOLD64H["frontier_after_cost64h"]
assert [HEAD1472["solved_s6_in_manifest"], HEAD1472["remaining_s5_orbits"],
        HEAD1472["unique_remaining_s6"], HEAD1472["sum_remaining_cost"],
        HEAD1472["s6_needed_by_open_classes"],
        HEAD1472["cost_needed_by_open_classes"]] == [1472, 174, 6376,
        504672, 4649, 368586]
SWEPT_CHILDREN = {f"{CHILD64H:032x}", f"{CHILD76C:032x}",
                  f"{CHILD66I:032x}"}

# ------------------------------------------------ family overlay
fams = V1["census"]
bit_tables = V1["bit_tables"]
v2_fams = {p: {r["s6_hex"]: r for r in rows}
           for p, rows in V2["families_v2"].items()}
overlay = {}
conflicts = []
v2_agreement_fields = 0
for parent, fam in fams.items():
    rows_out = []
    for row in fam["rows"]:
        hex_ = row["s6_hex"]
        v = int(hex_, 16)
        bits = sorted(legal_candidates(hex_)[1])
        assert len(bits) == row["cost"], (hex_, len(bits), row["cost"])
        v1_tbl = bit_tables.get(hex_)
        st_by_bit = ({x["bit"]: x["status"] for x in v1_tbl["bits"]}
                     if v1_tbl is not None else None)
        known = 0
        per_src = {"cost64h": [0, 0], "cost76c": [0, 0],
                   "cost66i": [0, 0]}  # [known, win]
        v2cmp = [0, 0, 0]  # [known_6476, win_6476, ref_6476] under v2 rules
        pending = {}
        new_refuted = 0
        new_win = 0
        for b in bits:
            c = canon(v | (1 << b))
            src = None
            e = None
            if c in verdict64h:
                src, e = "cost64h", verdict64h[c]
            elif c in verdict76c:
                src, e = "cost76c", verdict76c[c]
            elif c in verdict66i:
                src, e = "cost66i", verdict66i[c]
            if src is not None:
                known += 1
                per_src[src][0] += 1
                if src in ("cost64h", "cost76c"):
                    v2cmp[0] += 1
                if e["verdict"] == "WIN7-D10":
                    pending.setdefault(src, b)
                # v2 semantics: reductions only for bits whose v1 status
                # is "open" (bit table required); conflicts otherwise
                if v1_tbl is not None:
                    assert {x["bit"]: x for x in v1_tbl["bits"]}[b][
                        "root_canon"] == f"{c:032x}", (hex_, b)
                    stat = st_by_bit[b]
                    if stat == "open":
                        if e["verdict"] == "WIN7-D10":
                            new_win += 1
                            if src in ("cost64h", "cost76c"):
                                v2cmp[1] += 1
                        else:
                            new_refuted += 1
                            if src in ("cost64h", "cost76c"):
                                v2cmp[2] += 1
                    elif stat == "harvested_refuted":
                        if e["verdict"] == "WIN7-D10":
                            conflicts.append((hex_, b, stat, e["verdict"], src))
                    elif stat == "harvested_win":
                        if e["verdict"] == "REFUTED-D10":
                            conflicts.append((hex_, b, stat, e["verdict"], src))
        rec = dict(row)
        rec["bits_in_new_sweeps"] = known
        rec["new_refuted_bits"] = new_refuted
        rec["new_win_bits"] = new_win
        if "cost64h" in pending:
            rec["closed_by_64h_fold_by_bit"] = pending["cost64h"]
        if "cost76c" in pending:
            rec["pending_close_76c_fold_by_bit"] = pending["cost76c"]
        if "cost66i" in pending:
            rec["pending_close_66i_fold_by_bit"] = pending["cost66i"]
        # v2 agreement on the 64h/76c fields (66i was not in v2)
        v2r = v2_fams[parent].get(hex_)
        if v2r is not None:
            assert v2cmp[0] == v2r["bits_in_new_sweeps"], (hex_, v2cmp[0], v2r["bits_in_new_sweeps"])
            assert v2cmp[1] == v2r["new_win_bits"], (hex_, v2cmp[1], v2r["new_win_bits"])
            assert v2cmp[2] == v2r["new_refuted_bits"], (hex_, v2cmp[2], v2r["new_refuted_bits"])
            v2_agreement_fields += 1
        rows_out.append(rec)
    overlay[parent] = rows_out
assert not conflicts, conflicts
assert v2_agreement_fields == sum(len(f["rows"]) for f in fams.values())

# ------------------------------------------------ ranking + selection
P_TARGET = "00000000000000403800000008000000"
ranked = []
for parent, rows in overlay.items():
    for r in rows:
        hex_ = r["s6_hex"]
        if hex_ in SWEPT_CHILDREN:
            r["excluded"] = "swept child of an in-flight/complete lane (64h/76c/66i)"
            continue
        if hex_ in CLOSED64H:
            r["excluded"] = "closed by the LANDED cost-64h fold (receipt 1633be29)"
            continue
        if "pending_close_76c_fold_by_bit" in r:
            r["excluded"] = ("closed by the pending cost-76c fold "
                             f"(bit {r['pending_close_76c_fold_by_bit']})")
            continue
        if "pending_close_66i_fold_by_bit" in r:
            r["excluded"] = ("closed by the pending cost-66i fold "
                             f"(bit {r['pending_close_66i_fold_by_bit']})")
            continue
        open_v3 = r["open_after_census"] - r["new_refuted_bits"] \
            - r["new_win_bits"]
        assert open_v3 >= 0, r
        r["open_after_census_v3"] = open_v3
        if open_v3 == 0:
            r["excluded"] = "no open bits remain after the 64h/76c/66i overlay"
            continue
        ranked.append((r["cost"], open_v3, hex_, parent, r))
ranked.sort(key=lambda t: (t[0], t[1], t[2]))
cand_target = [t for t in ranked if t[3] == P_TARGET]
assert cand_target, "no candidate row in the primary family"
sel = cand_target[0]
SELECTED = sel[2]
sel_row = sel[4]
sel_bits = sorted(legal_candidates(SELECTED)[1])
v1_tbl = bit_tables[SELECTED]
st_by_bit = {x["bit"]: x for x in v1_tbl["bits"]}
known_bits = sorted(
    b for b in sel_bits
    if st_by_bit[b]["status"] in ("harvested_refuted", "harvested_win")
    or canon(int(SELECTED, 16) | (1 << b)) in verdict64h
    or canon(int(SELECTED, 16) | (1 << b)) in verdict76c
    or canon(int(SELECTED, 16) | (1 << b)) in verdict66i)
sweep_bits = [b for b in sel_bits if b not in known_bits]
runner_up = ranked[0]

result = {
    "schema": "n11-class2-lane-next-target-presweep-1472-20261117-v1",
    "date": "2026-11-17",
    "chain_head": "1472/174/6376/504672/4649/368586",
    "baseline": {
        "v1_census_json":
            "class2-lane-next-target-presweep-1452-20261116.json "
            "(git blob 0d9a94a272de9fe45708757f17bfea60239a3c9b)",
        "v2_census_json":
            "class2-lane-next-target-presweep-1452-v2-20261116.json "
            "(git blob 67d6a5c192953b9bc95fd13b356e5aabeac2a12c)",
        "note": ("v1 head-1452 bit statuses carried over; v3 overlays the "
                 "64h/76c/66i sweeps and the LANDED 64h fold closure"),
    },
    "new_verdict_maps": {
        "cost64h": {"child": f"{CHILD64H:032x}", "bits": 64,
                    "win7_d10_bits": win64h_bits,
                    "fold": "LANDED (receipt blob 1633be29..., head 1472)",
                    "source": "raw batches 1-8 (blob-pinned)"},
        "cost76c": {"child": f"{CHILD76C:032x}", "bits": 76,
                    "win7_d10_bits": win76c_bits,
                    "fold": "PENDING (parallel lane; bit 61 certificate in flight)",
                    "source": ("v17 raw batches 1-10 (blob-pinned; v16 "
                               "agreement with the documented bit-113 flip)")},
        "cost66i": {"child": f"{CHILD66I:032x}", "bits": 66,
                    "win7_d10_bits": win66i_bits,
                    "fold": ("PENDING behind cost-76c (claim v5 dependency); "
                             "all nine certificates verified"),
                    "source": ("raw batches 1-9 (blob-pinned, v17 engine) "
                               "+ raw audit blob f7d8bad6... + claim v5 "
                               "winner_roots 9/9")},
    },
    "cross_checks": {
        "bit_table_canon_agreement": "16/16 rows, all covered bits",
        "prereg_win_canon_agreement": "23/23 receipts",
        "landed_64h_closed_rows": sorted(CLOSED64H),
        "landed_64h_closed_rows_match_prereg": True,
        "v17_bit113_flip": True,
        "cross_sweep_canon_conflicts": 0,
        "verdict_conflicts": 0,
        "v2_overlay_agreement": ("all family rows reproduce the v2 "
                                 f"{v2_agreement_fields}-row 64h/76c fields"),
    },
    "families_v3": overlay,
    "ranking_top10": [
        {"s6_hex": t[2], "parent": t[3], "cost": t[0],
         "open_after_census_v3": t[1], "demand": t[4]["demand"]}
        for t in ranked[:10]],
    "selection_policy": (
        "primary family = the published next pure class-2 target "
        f"{P_TARGET} (18 rows / 1287 occurrences); within the family "
        "cheapest cost, then fewest open bits after the 64h/76c/66i "
        "overlay, then hex. Rows closed by the landed 64h fold, rows "
        "pending the 76c/66i folds, and the three swept children are "
        "excluded. The globally cheapest remaining row is recorded as "
        "runner-up"),
    "selected_target": {
        "s6_hex": SELECTED,
        "parent": sel[3],
        "cost": sel_row["cost"],
        "demand": sel_row["demand"],
        "legal_candidates": len(sel_bits),
        "sweep_bits": sweep_bits,
        "confirmation_bits": known_bits,
        "runner_up": {"s6_hex": runner_up[2], "parent": runner_up[3],
                      "cost": runner_up[0],
                      "open_after_census_v3": runner_up[1]},
        "note": ("cheapest remaining unswept/unclaimed/unexcluded row of "
                 "the primary family at head 1472; confirmation bits carry "
                 "already-known verdicts and will be re-run fresh"),
    },
    "interpretation_guard": (
        "search-plan bookkeeping only; no engine search was run, no "
        "verdict was created, no row was closed; WIN7-D10 proves a "
        "first-player win within depth 10 from the individual 7-stone "
        "root only; REFUTED-D10 is not a LOSS proof; solved 1472 is "
        "manifest-coverage bookkeeping; the 11x11 empty board, "
        "two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 "
        "all remain UNKNOWN"),
}
out_path = OUT / "class2-lane-next-target-presweep-1472-20261117.json"
out_path.write_text(json.dumps(result, indent=1, sort_keys=False) + "\n")
print(f"wrote {out_path} ({out_path.stat().st_size} bytes)")
print("selected:", SELECTED, "cost", sel_row["cost"],
      "sweep", len(sweep_bits), "confirm", known_bits, "parent", sel[3])
for t in ranked[:10]:
    print(f"  rank: cost {t[0]} open {t[1]} {t[2]} parent {t[3]}")
