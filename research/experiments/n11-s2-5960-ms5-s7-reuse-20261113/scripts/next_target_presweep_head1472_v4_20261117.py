#!/usr/bin/env python3
"""head-1472 next-target presweep census v4 (2026-11-17).

Update of the published head-1472 presweep census v3
(class2-lane-next-target-presweep-1472-20261117.json, git blob
3ee5703c8cabf738eaecefb17a759c78c4a34e61) for the state after:

  * the cost-66j sweep COMPLETED and all nine WIN7-D10 certificates were
    extracted, independently verified and published (commit 020603f8
    sweep + 4f933331..d90ab511 certificates; raw batches 1-9
    blob-pinned below): 9 WIN7-D10 bits [7,9,30,66,78,79,92,96,114] +
    57 REFUTED-D10, 0 capped, 65,981,633 nodes; its receipt fold is
    pending behind the cost-76c and cost-66i folds;
  * the cost-76c and cost-66i folds remain PENDING (76c bit 61
    certificate extraction in flight on the parallel lane; 66i waits on
    76c) -- untouched here;
  * the cost-64h fold remains LANDED (head 1472 unchanged).

Method: v3 is the authoritative overlay state (64h/76c/66i verdicts,
landed-64h closure, pending 76c/66i exclusions). This v4 adds the
fourth verdict map (66j v17 raw, blob-pinned), asserts zero verdict
conflicts across all four maps, reproduces every v3 family field,
marks the pending-66j-fold closures derived from the 66j WIN canons
(cross-checked against the published cost66j candidate-manifest
marginals audit: exactly the 7 marginal manifest rows), excludes the
now-swept 66j child, and re-ranks the remaining unswept/unclaimed/
unexcluded rows at head 1472.

Cross-checks (all asserted):
  * computed root canon == v1 bit-table root_canon for every covered bit
    (now including the 66j-covered bits);
  * 66j WIN bits == raw audit win7_d10_bits == claim v3 winner_roots
    (9/9, root == child|1<<bit, d4_canon agreement);
  * 64h/76c/66i verdict maps and landed-64h closure identical to v3;
  * v4 family overlay reproduces every v3 field on every family row;
  * zero verdict conflicts across the four canon maps;
  * family rows carrying a 66j WIN canon bit == the 7 marginal manifest
    rows of the published marginals audit (intersected with census rows),
    both directions.

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
V3 = load_out("class2-lane-next-target-presweep-1472-20261117.json",
              "3ee5703c8cabf738eaecefb17a759c78c4a34e61")
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
AUDIT66J = load_out("class2-lane-cost66j-raw-audit-20261117.json",
                    "6862eb2db71e087d7c17fec3a157eafc17bf46d3")
CLAIM66J = load_out("class2-lane-cost66j-inflight-20261117.json",
                    "eb08a2db780f2b23c09f07ef96d02c5e0ff772a5")
MARGINALS66J = load_out(
    "class2-lane-cost66j-candidate-manifest-marginals-20261117.json",
    "eaca4280c6f969a7b6ed9341de793e010d977318")

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
PIN66J = ["565e010b46c84e0bc9e51509dc67005634c1d294",
          "470b65d238a2ab06766d551ff903e15346569381",
          "0211836ab9bc3e565e51cd9aaf30383702d3c174",
          "034a565bb3f8abddb8e679ab656bb0e39530ac74",
          "47cb5f8c3aa446d8993369b71e33b45f17038072",
          "b210cae667030ce4e9f59699fcab5d6a233da574",
          "6fd435c94cb700dd0ee14dabb63160cfa523732d",
          "c7b19d015d4ae3d3b0f3b40ec37aa02d62fe4ee3",
          "bdccf073eebaee4fc5ac09d1e59106676c3f140f"]

CHILD64H = int("00000000000000403800000008100000", 16)
CHILD76C = int("00000000010000809002000001000000", 16)
CHILD66I = int("00000000000000801226000000000000", 16)
CHILD66J = int("00000000000000c09002000000001000", 16)

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

# ------------------------------------------------ 66j verdict map (v17 raw)
verdict66j = {}
pilots = 0
for i in range(1, 10):
    rows = load_jsonl(f"class2-lane-cost66j-raw-batch{i}-20261117.jsonl",
                      PIN66J[i - 1])
    for r in rows:
        if r.get("control") == "pilot_d6":
            assert r == {"control": "pilot_d6", "loss": False,
                         "nodes": 3402, "capped": False}, r
            pilots += 1
            continue
        assert not r["capped"], r
        v = "WIN7-D10" if r["loss"] else "REFUTED-D10"
        c = canon(CHILD66J | (1 << r["bit"]))
        assert c not in verdict66j
        verdict66j[c] = {"verdict": v, "bit": r["bit"], "nodes": r["nodes"]}
assert pilots == 9
assert len(verdict66j) == 66
win66j_bits = sorted(e["bit"] for e in verdict66j.values()
                     if e["verdict"] == "WIN7-D10")
assert win66j_bits == [7, 9, 30, 66, 78, 79, 92, 96, 114], win66j_bits
assert AUDIT66J["verdicts"]["win7_d10_bits"] == win66j_bits
assert AUDIT66J["verdicts"]["capped_count"] == 0
assert sorted(AUDIT66J["verdicts"]["refuted_d10_bits"]) == sorted(
    e["bit"] for e in verdict66j.values()
    if e["verdict"] == "REFUTED-D10")
assert AUDIT66J["target"]["s6_child"] == f"{CHILD66J:032x}"
assert CLAIM66J["s6_child"] == f"{CHILD66J:032x}"
claim66j_win = CLAIM66J["winner_roots"]
assert len(claim66j_win) == 9
bit_canon_66j = {e["bit"]: c for c, e in verdict66j.items()}
for w in claim66j_win:
    c = bit_canon_66j[w["bit"]]
    assert f"{c:032x}" == w["d4_canon_root"], w
    assert w["root"] == f"{CHILD66J | (1 << w['bit']):032x}", w
assert sorted(w["bit"] for w in claim66j_win) == win66j_bits
win66j_canons = {c for c, e in verdict66j.items()
                 if e["verdict"] == "WIN7-D10"}
assert {w["d4_canon_root"] for w in claim66j_win} == \
    {f"{c:032x}" for c in win66j_canons}

# -------------------------------------------- zero cross-map conflicts (4-way)
maps = {"cost64h": verdict64h, "cost76c": verdict76c,
        "cost66i": verdict66i, "cost66j": verdict66j}
names = list(maps)
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        a, b = maps[names[i]], maps[names[j]]
        for c in set(a) & set(b):
            assert a[c]["verdict"] == b[c]["verdict"], (
                c, names[i], names[j], a[c], b[c])

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
                  f"{CHILD66I:032x}", f"{CHILD66J:032x}"}

# -------------------------------------------- pending 66j fold closure set
MARGINAL66J = set()
for rec in MARGINALS66J["single_candidate_projections"]:
    MARGINAL66J.update(int(x, 16)
                       for x in rec["marginal_manifest_hexes"])
assert len(MARGINAL66J) == 7, len(MARGINAL66J)
assert f"{CHILD66J:032x}" in {f"{x:032x}" for x in MARGINAL66J}

# ------------------------------------------------ family overlay
fams = V1["census"]
bit_tables = V1["bit_tables"]
v3_fams = {p: {r["s6_hex"]: r for r in rows}
           for p, rows in V3["families_v3"].items()}
overlay = {}
conflicts = []
v3_agreement_fields = 0
rows_with_66j_win_bit = {}
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
        known3 = 0          # union of 64h/76c/66i (v3 semantics)
        known66j = 0        # in the 66j map
        known66j_only = 0   # in 66j but not in the v3 union
        new_refuted = 0     # v1-open + v3-union verdict (v3 semantics)
        new_win = 0
        ref66j = 0          # v1-open + 66j-only REFUTED
        win66j = 0          # v1-open + 66j-only WIN
        pending = {}
        pending66j_bit = None
        for b in bits:
            c = canon(v | (1 << b))
            in3 = (c in verdict64h or c in verdict76c or c in verdict66i)
            inj = c in verdict66j
            if in3:
                known3 += 1
            # v3 priority chain for pending attribution
            if c in verdict64h:
                src = "cost64h"
            elif c in verdict76c:
                src = "cost76c"
            elif c in verdict66i:
                src = "cost66i"
            else:
                src = None
            if src is not None and maps[src][c]["verdict"] == "WIN7-D10":
                pending.setdefault(src, b)
            if inj:
                known66j += 1
                if verdict66j[c]["verdict"] == "WIN7-D10":
                    if pending66j_bit is None:
                        pending66j_bit = b
                if not in3:
                    known66j_only += 1
                    if v1_tbl is not None:
                        assert {x["bit"]: x for x in v1_tbl["bits"]}[b][
                            "root_canon"] == f"{c:032x}", (hex_, b)
                        stat = st_by_bit[b]
                        if stat == "open":
                            if verdict66j[c]["verdict"] == "WIN7-D10":
                                win66j += 1
                            else:
                                ref66j += 1
                        elif stat == "harvested_refuted":
                            if verdict66j[c]["verdict"] == "WIN7-D10":
                                conflicts.append(
                                    (hex_, b, stat, "WIN7-D10", "cost66j"))
                        elif stat == "harvested_win":
                            if verdict66j[c]["verdict"] == "REFUTED-D10":
                                conflicts.append(
                                    (hex_, b, stat, "REFUTED-D10", "cost66j"))
            # v3 reductions (priority chain verdicts, v1-open only)
            if src is not None and v1_tbl is not None:
                assert {x["bit"]: x for x in v1_tbl["bits"]}[b][
                    "root_canon"] == f"{c:032x}", (hex_, b)
                stat = st_by_bit[b]
                if stat == "open":
                    verdict = maps[src][c]["verdict"]
                    if verdict == "WIN7-D10":
                        new_win += 1
                    else:
                        new_refuted += 1
                elif stat == "harvested_refuted":
                    if maps[src][c]["verdict"] == "WIN7-D10":
                        conflicts.append(
                            (hex_, b, stat, maps[src][c]["verdict"], src))
                elif stat == "harvested_win":
                    if maps[src][c]["verdict"] == "REFUTED-D10":
                        conflicts.append(
                            (hex_, b, stat, maps[src][c]["verdict"], src))
        rec = dict(row)
        rec["bits_in_new_sweeps"] = known3
        rec["new_refuted_bits"] = new_refuted
        rec["new_win_bits"] = new_win
        rec["bits_in_66j_sweep"] = known66j
        rec["bits_known_only_via_66j"] = known66j_only
        rec["new_refuted_bits_66j"] = ref66j
        rec["new_win_bits_66j"] = win66j
        if "cost64h" in pending:
            rec["closed_by_64h_fold_by_bit"] = pending["cost64h"]
        if "cost76c" in pending:
            rec["pending_close_76c_fold_by_bit"] = pending["cost76c"]
        if "cost66i" in pending:
            rec["pending_close_66i_fold_by_bit"] = pending["cost66i"]
        if pending66j_bit is not None:
            rec["pending_close_66j_fold_by_bit"] = pending66j_bit
            rows_with_66j_win_bit[hex_] = pending66j_bit
        # v3 agreement on every family row
        v3r = v3_fams[parent][hex_]
        assert rec["bits_in_new_sweeps"] == v3r["bits_in_new_sweeps"], (
            hex_, rec["bits_in_new_sweeps"], v3r["bits_in_new_sweeps"])
        assert rec["new_refuted_bits"] == v3r["new_refuted_bits"], hex_
        assert rec["new_win_bits"] == v3r["new_win_bits"], hex_
        for k in ("closed_by_64h_fold_by_bit", "pending_close_76c_fold_by_bit",
                  "pending_close_66i_fold_by_bit"):
            if k in v3r:
                assert rec.get(k) == v3r[k], (hex_, k, rec.get(k), v3r[k])
            else:
                assert k not in rec, (hex_, k)
        open_v3_re = (row["open_after_census"] - new_refuted - new_win)
        if "open_after_census_v3" in v3r:
            assert open_v3_re == v3r["open_after_census_v3"], (
                hex_, open_v3_re, v3r["open_after_census_v3"])
        v3_agreement_fields += 1
        rows_out.append(rec)
    overlay[parent] = rows_out
assert not conflicts, conflicts
assert v3_agreement_fields == sum(len(f["rows"]) for f in fams.values())

# ------------------------------------ marginal-rows consistency (66j fold)
# a census row carrying a 66j WIN canon bit is a cover of a 66j WIN root;
# if it is still open at head 1472 it must be one of the 7 marginal
# manifest rows of the published marginals audit; if it was already
# closed by the landed 64h fold it is solved and NOT marginal
census_hexes = {r["s6_hex"] for rows in overlay.values() for r in rows}
marginal_in_census = {f"{x:032x}" for x in MARGINAL66J} & census_hexes
rows_with_66j_win_open = {
    h for h in rows_with_66j_win_bit if h not in CLOSED64H}
assert rows_with_66j_win_open == marginal_in_census, (
    sorted(rows_with_66j_win_open - marginal_in_census),
    sorted(marginal_in_census - rows_with_66j_win_open))
rows_with_66j_win_already_closed = sorted(
    set(rows_with_66j_win_bit) - rows_with_66j_win_open)
assert all(h in CLOSED64H for h in rows_with_66j_win_already_closed), \
    rows_with_66j_win_already_closed

# ------------------------------------------------ ranking + selection
P_TARGET = "00000000000000403800000008000000"
ranked = []
for parent, rows in overlay.items():
    for r in rows:
        hex_ = r["s6_hex"]
        if hex_ in SWEPT_CHILDREN:
            r["excluded"] = ("swept child of an in-flight/complete lane "
                             "(64h/76c/66i/66j)")
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
        if "pending_close_66j_fold_by_bit" in r:
            r["excluded"] = ("closed by the pending cost-66j fold "
                             f"(bit {r['pending_close_66j_fold_by_bit']})")
            continue
        open_v3 = r["open_after_census"] - r["new_refuted_bits"] \
            - r["new_win_bits"]
        assert open_v3 >= 0, r
        assert "open_after_census_v3" not in r or \
            r.get("open_after_census_v3", open_v3) == open_v3, hex_
        open_v4 = open_v3 - r["new_refuted_bits_66j"] - r["new_win_bits_66j"]
        assert open_v4 >= 0, r
        r["open_after_census_v4"] = open_v4
        if open_v4 == 0:
            r["excluded"] = ("no open bits remain after the "
                             "64h/76c/66i/66j overlay")
            continue
        ranked.append((r["cost"], open_v4, hex_, parent, r))
ranked.sort(key=lambda t: (t[0], t[1], t[2]))

# ---------------------------- v3/v4 exclusion consistency
v4_excluded = {r["s6_hex"]: r["excluded"]
               for rows in overlay.values() for r in rows
               if "excluded" in r}
for parent, rows in V3["families_v3"].items():
    for r in rows:
        hex_ = r["s6_hex"]
        if "excluded" in r:
            # every v3-excluded row stays excluded in v4 (same reason,
            # since the 64h/76c/66i conditions are reproduced exactly)
            assert hex_ in v4_excluded, (hex_, r["excluded"])
        else:
            # rows ranked in v3 are in v4 either still ranked, or
            # excluded by a new 66j condition (pending 66j fold, zero
            # open after the 66j overlay), or the swept 66j child
            assert hex_ not in v4_excluded or "66j" in v4_excluded[hex_] \
                or "66j" in v4_excluded[hex_].replace(
                    "64h/76c/66i/66j", "66j"), (hex_, v4_excluded.get(hex_))
ranked_hexes = {t[2] for t in ranked}
for hex_, why in v4_excluded.items():
    if "66j" not in why and "(64h/76c/66i/66j)" not in why:
        v3r_all = {r["s6_hex"]: r
                   for rows in V3["families_v3"].values() for r in rows}
        assert "excluded" in v3r_all[hex_], (hex_, why)

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
    or canon(int(SELECTED, 16) | (1 << b)) in verdict66i
    or canon(int(SELECTED, 16) | (1 << b)) in verdict66j)
sweep_bits = [b for b in sel_bits if b not in known_bits]
runner_up = ranked[0]

result = {
    "schema": "n11-class2-lane-next-target-presweep-1472-20261117-v2",
    "date": "2026-11-17",
    "chain_head": "1472/174/6376/504672/4649/368586",
    "baseline": {
        "v1_census_json":
            "class2-lane-next-target-presweep-1452-20261116.json "
            "(git blob 0d9a94a272de9fe45708757f17bfea60239a3c9b)",
        "v3_census_json":
            "class2-lane-next-target-presweep-1472-20261117.json "
            "(git blob 3ee5703c8cabf738eaecefb17a759c78c4a34e61)",
        "note": ("v1 head-1452 bit statuses carried over; v4 overlays the "
                 "64h/76c/66i/66j sweeps, the LANDED 64h fold closure and "
                 "the pending 76c/66i/66j fold closures"),
    },
    "new_verdict_maps": {
        "cost64h": {"child": f"{CHILD64H:032x}", "bits": 64,
                    "win7_d10_bits": win64h_bits,
                    "fold": "LANDED (receipt blob 1633be29..., head 1472)",
                    "source": "raw batches 1-8 (blob-pinned)"},
        "cost76c": {"child": f"{CHILD76C:032x}", "bits": 76,
                    "win7_d10_bits": [61, 99],
                    "fold": "PENDING (parallel lane; bit 61 certificate in flight)",
                    "source": ("v17 raw batches 1-10 (blob-pinned in v3; "
                               "v4 carries the v3-verified WIN canons)")},
        "cost66i": {"child": f"{CHILD66I:032x}", "bits": 66,
                    "win7_d10_bits": win66i_bits,
                    "fold": ("PENDING behind cost-76c (claim v5 dependency); "
                             "all nine certificates verified"),
                    "source": ("raw batches 1-9 (blob-pinned, v17 engine) "
                               "+ raw audit blob f7d8bad6...")},
        "cost66j": {"child": f"{CHILD66J:032x}", "bits": 66,
                    "win7_d10_bits": win66j_bits,
                    "fold": ("PENDING behind the cost-76c and cost-66i "
                             "folds; all nine certificates extracted, "
                             "independently verified and published"),
                    "source": ("raw batches 1-9 (blob-pinned, v17 engine) "
                               "+ raw audit blob 6862eb2d... + claim v3 "
                               "winner_roots 9/9")},
    },
    "cross_checks": {
        "bit_table_canon_agreement": "all covered bits, four sweeps",
        "prereg_win_canon_agreement_64h": "23/23 receipts (via v3)",
        "landed_64h_closed_rows_match_prereg": True,
        "cross_sweep_canon_conflicts": 0,
        "verdict_conflicts": 0,
        "v3_overlay_agreement": (f"all family rows reproduce the v3 "
                                 f"{v3_agreement_fields}-row fields"),
        "pending_66j_marginal_rows_match_marginals_audit": sorted(
            f"{x:032x}" for x in MARGINAL66J),
        "family_rows_closed_by_pending_66j_fold": sorted(
            rows_with_66j_win_open),
        "family_rows_with_66j_win_bit_already_closed_by_64h":
            rows_with_66j_win_already_closed,
    },
    "families_v4": overlay,
    "ranking_top10": [
        {"s6_hex": t[2], "parent": t[3], "cost": t[0],
         "open_after_census_v4": t[1], "demand": t[4]["demand"]}
        for t in ranked[:10]],
    "selection_policy": (
        "primary family = the published next pure class-2 target "
        f"{P_TARGET} (18 rows / 1287 occurrences); within the family "
        "cheapest cost, then fewest open bits after the 64h/76c/66i/66j "
        "overlay, then hex. Rows closed by the landed 64h fold, rows "
        "pending the 76c/66i/66j folds, and the four swept children are "
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
                      "open_after_census_v4": runner_up[1]},
        "note": ("cheapest remaining unswept/unclaimed/unexcluded row of "
                 "the primary family at head 1472 after the 66j sweep; "
                 "confirmation bits carry already-known verdicts and will "
                 "be re-run fresh"),
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
out_path = OUT / "class2-lane-next-target-presweep-1472-v4-20261117.json"
out_path.write_text(json.dumps(result, indent=1, sort_keys=False) + "\n")
print(f"wrote {out_path} ({out_path.stat().st_size} bytes)")
print("66j marginal census rows:", sorted(rows_with_66j_win_bit))
print("selected:", SELECTED, "cost", sel_row["cost"],
      "sweep", len(sweep_bits), "confirm", known_bits, "parent", sel[3])
print("runner-up:", runner_up[2], "cost", runner_up[0],
      "open", runner_up[1])
for t in ranked[:10]:
    print(f"  rank: cost {t[0]} open {t[1]} {t[2]} parent {t[3]}")
