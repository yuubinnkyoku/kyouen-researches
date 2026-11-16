#!/usr/bin/env python3
"""head-1452 next-target presweep census v2 (2026-11-16).

Incremental update of the published head-1452 presweep census
(class2-lane-next-target-presweep-1452-20261116.json, git blob
0d9a94a272de9fe45708757f17bfea60239a3c9b) with the two sweeps published
AFTER that census whose receipt folds have NOT landed yet:

  * cost-64h child 00000000000000403800000008100000 -- 64 bits:
    23 WIN7-D10 + 41 REFUTED-D10, 0 capped (claim v2, git blob
    68e4878094b78eaf0a465033d0289a6db5d94861; raw batches 1-8,
    blob-pinned below). Fold preregistered (git blob
    5074a8a0cbb75fcc91b5b999a3135fac06d42400, projected head 1472,
    20 closed manifest rows); fold receipt NOT landed.
  * cost-76c child 00000000010000809002000001000000 -- 76 bits;
    v17-corrected WIN7-D10 bits 61/99 only (bit 113 flipped WIN->REFUTED
    by the fbt-saturation repair; v17 sweep-and-fbt audit git blob
    235f964365a7ab33e33986c915fc7f6861e4d686); claim v4 sweep-complete
    (git blob 58b60b0c3ca267919862c115ea16488b1ad9a5c6); fold NOT landed.

Method: the v1 census JSON (blob-pinned) is taken as the authoritative
baseline for the head-1452 bit statuses of the three actionable target
families. For every family row this script re-derives the legal candidate
bits (legal_candidates.py, exact integer Bareiss 4x4) and the D4 canonical
root hex of every candidate (canon verbatim-ported from
fold_projection_head1450_tool_20261116.py), overlays the 64h/76c verdicts
as canonical-root verdict maps, marks every family row that a pending fold
would close (the 20 preregistered 64h rows + any family row whose candidate
canon set contains a pending WIN receipt canon), and re-ranks the remaining
unswept/unclaimed rows.

Cross-checks (all asserted):
  * computed root canon == v1 bit-table root_canon for every bit of the 16
    rows covered by the v1 bit tables;
  * computed 64h WIN canon set == prereg receipts' d4_canonical_hex set;
  * within the three families, the preregistered 20-row 64h closed map
    intersects the families in exactly the rows whose candidate canons
    contain a 64h WIN canon;
  * computed 76c WIN canon set == {bit61, bit99} root canons with bit 61
    matching the claim v4 winner_roots entry, and bit 113 REFUTED in v17;
  * v16 vs v17 raw-batch agreement for 76c is 75/76 with the single
    documented bit-113 flip;
  * zero verdict conflicts between the v1 statuses and the overlay.

Interpretation guard: search-plan bookkeeping only. No engine search is
run here, no verdict is created, no row is closed. WIN7-D10 proves a
first-player win within depth 10 from the individual 7-stone root only;
REFUTED-D10 is not a LOSS proof; receipt folds are manifest-coverage
bookkeeping. The 11x11 empty board, the two-stone roots {49,60} and
{59,60}, S2 {59,60}, and classes 1/2/4 all remain UNKNOWN.
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
PREREG64H = load_out(
    "class2-lane-cost64h-fold-preregistration-independent-20261116.json",
    "5074a8a0cbb75fcc91b5b999a3135fac06d42400")
CLAIM64H = load_out("class2-lane-cost64h-inflight-20261116.json",
                    "68e4878094b78eaf0a465033d0289a6db5d94861")
CLAIM76C = load_out("class2-lane-cost76c-inflight-20261116.json",
                    "58b60b0c3ca267919862c115ea16488b1ad9a5c6")
AUDIT76C = load_out(
    "class2-lane-cost76c-v17-sweep-and-fbt-saturation-audit-20261117.json",
    "235f964365a7ab33e33986c915fc7f6861e4d686")

PIN64H = ["47da4e04357b7012c55903aea22160f3ca0767c9",
          "04e59e2ed62ba2306c80743e9c0517a6d89e70a2",
          "78bb44093ef56191110119009ce788d0cd4f383f",
          "7d196917961356c69cfa608930c3a1b7716aaf59",
          "ba6a36d4cb93111461aeec86b55e2909cbc0a489",
          "a49e2b9cd7d239fd95681afa83793deb075b4ccf",
          "6771b7a900191fce3d11feccf3da0e2e05f001e9",
          "5e778cae345d2a1d0d50455a3633ea673b6c08be"]
PIN76C16 = ["1aebb80f0b4f4384a7207afff4c706433d0fcaff",
            "7b0b471d81ad1815f529bfc98a63acdff73ccc7a",
            "9f5c63cd2c93a276ebcfc6874f2f0aa870921c0c",
            "a7c5ee5167529ff44351f5b438cf1636352bffca",
            "a07e06607aeb6b9a06f629e9210bc6774b43e964",
            "beb9283161491d17c435890f563b8c7f283b48a3",
            "a511e748ba227b2d20627f653acde89fca0e19e6",
            "a2aa8bb60fd7f5c875a234ead60f4826335d32a6",
            "0f41ee0c7f685f8a41a5574a399dde3c6eea7eee",
            "273f6e710d791b20e5ec2ab57ae53b7127f18122"]
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

CHILD64H = int("00000000000000403800000008100000", 16)
CHILD76C = int("00000000010000809002000001000000", 16)

# ------------------------------------------------ 64h verdict map (v16 raw)
verdict64h = {}   # canon -> {"verdict","bit","nodes"}
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
assert len(win64h_bits) == 23
# prereg agreement: WIN canon set
win64h_canons = {c for c, e in verdict64h.items()
                 if e["verdict"] == "WIN7-D10"}
prereg_canons = {r["d4_canonical_hex"] for r in PREREG64H["receipts"]}
assert prereg_canons == {f"{c:032x}" for c in win64h_canons}, "prereg mismatch"
assert PREREG64H["win_bits_in_fold_order"] == sorted(win64h_bits)

# ------------------------------------------------ 76c verdict map (v17 raw)
verdict76c = {}
pilots = 0
v16_bits = {}
for i in range(1, 11):
    rows17 = load_jsonl(
        f"class2-lane-cost76c-v17-raw-batch{i}-20261117.jsonl",
        PIN76C17[i - 1])
    rows16 = load_jsonl(
        f"class2-lane-cost76c-raw-batch{i}-20261116.jsonl",
        PIN76C16[i - 1])
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
        verdict76c[c] = {"verdict": v, "bit": r["bit"],
                         "nodes": r["nodes"]}
    for r in rows16:
        if r.get("control") == "pilot_d6":
            continue
        v16_bits[r["bit"]] = "WIN7-D10" if r["loss"] else "REFUTED-D10"
assert pilots == 10
assert len(verdict76c) == 76
win76c_bits = sorted(e["bit"] for e in verdict76c.values()
                     if e["verdict"] == "WIN7-D10")
assert win76c_bits == [61, 99], win76c_bits
assert AUDIT76C["v17_full_resweep"]["win_bits_corrected"] == [61, 99]
# bit 61/99/113 root canons recomputed from child|1<<bit and cross-checked
# against the claim v4 winner_roots and transfers root_canon fields: all
# are valid D4 images of the true roots. (An earlier unpublished draft of
# this script carried a corrupted local copy of the child constant -- an
# 8-stone 9002->9092 mistype, the same pattern as the recorded 77e
# child-hex incident -- which produced a false data-quality suspicion
# against the claim; the draft was never published and the constant was
# fixed before this run.)
bit_canon_76c = {e["bit"]: c for c, e in verdict76c.items()}
CLAIM_CHECK = {
    "finding": ("the cost-76c claim v4 (git blob 58b60b0c...) winner_roots "
                "and transfers root_canon hexes are all valid D4 images "
                "of the true roots child|1<<bit, recomputed and matched "
                "by this census (18/18); an earlier unpublished draft of "
                "this script carried a corrupted local child constant "
                "(8-stone 9002->9092 mistype, the same pattern as the "
                "recorded 77e child-hex incident) which produced a false "
                "data-quality suspicion against the claim; the constant "
                "was fixed before this run and nothing was published "
                "from the corrupted draft"),
    "claim_hexes_checked": 3 + len(CLAIM76C["transfers"]),
    "claim_hexes_valid_d4_images": 3 + len(CLAIM76C["transfers"]),
    "winner_roots_bit113_superseded_by_v17": {
        "claim_v4_verdict": "WIN7-D10",
        "v17_verdict": "REFUTED-D10",
        "note": ("claim v4 winner_roots bit 113 is superseded by the v17 "
                 "fbt-repair audit (git blob 235f9643...); bits 61/99 "
                 "stand as WIN7-D10 in both the claim and the v17 resweep"),
    },
}
for w in CLAIM76C["actual_execution"]["winner_roots"]:
    assert f"{bit_canon_76c[w['bit']]:032x}" == w["root_canon"], w
for tb, t in CLAIM76C["transfers"].items():
    assert f"{canon(CHILD76C | (1 << int(tb))):032x}" == t["root_canon"], tb
# v16 vs v17 agreement: only bit 113 differs
diff = sorted(b for b in v16_bits
              for c, e in verdict76c.items()
              if e["bit"] == b and e["verdict"] != v16_bits[b])
assert diff == [113], diff

# ------------------------------------------------ pending-fold row closure
CLOSED64H = set(PREREG64H["closed_row_parent_map"])
assert len(CLOSED64H) == 20
SWEPT_CHILDREN = {f"{CHILD64H:032x}", f"{CHILD76C:032x}"}
win76c_canons = {c for c, e in verdict76c.items()
                 if e["verdict"] == "WIN7-D10"}

# ------------------------------------------------ family overlay
fams = V1["census"]
bit_tables = V1["bit_tables"]
overlay = {}
conflicts = []
newly_known_rows = {}
for parent, fam in fams.items():
    rows_out = []
    for row in fam["rows"]:
        hex_ = row["s6_hex"]
        v = int(hex_, 16)
        bits = sorted(legal_candidates(hex_)[1])
        assert len(bits) == row["cost"], (hex_, len(bits), row["cost"])
        v1_tbl = bit_tables.get(hex_)
        canon_by_bit = {}
        known = 0
        pending_close_64h = None
        pending_close_76c = None
        new_refuted = 0
        new_win = 0
        conflict = None
        for b in bits:
            c = canon(v | (1 << b))
            canon_by_bit[b] = f"{c:032x}"
            if c in win64h_canons:
                pending_close_64h = b
            if c in win76c_canons:
                pending_close_76c = b
            in64 = c in verdict64h
            in76 = c in verdict76c
            if in64 or in76:
                known += 1
                src = ("cost64h" if in64 else "cost76c")
                e = verdict64h.get(c) or verdict76c[c]
                if v1_tbl is not None:
                    st = {x["bit"]: x for x in v1_tbl["bits"]}[b]["status"]
                    assert {x["bit"]: x for x in v1_tbl["bits"]}[b][
                        "root_canon"] == f"{c:032x}", (hex_, b)
                    if st == "open":
                        if e["verdict"] == "WIN7-D10":
                            new_win += 1
                        else:
                            new_refuted += 1
                    elif st == "harvested_refuted":
                        if e["verdict"] == "WIN7-D10":
                            conflict = (b, st, e["verdict"], src)
                            conflicts.append((hex_, b, st, e["verdict"]))
                    elif st == "receipt_win":
                        pass
                    elif st == "harvested_win":
                        if e["verdict"] == "REFUTED-D10":
                            conflict = (b, st, e["verdict"], src)
                            conflicts.append((hex_, b, st, e["verdict"]))
        rec = dict(row)
        rec["bits_in_new_sweeps"] = known
        rec["new_refuted_bits"] = new_refuted
        rec["new_win_bits"] = new_win
        if pending_close_64h is not None:
            rec["pending_close_64h_fold_by_bit"] = pending_close_64h
        if pending_close_76c is not None:
            rec["pending_close_76c_fold_by_bit"] = pending_close_76c
        rows_out.append(rec)
    overlay[parent] = rows_out
assert not conflicts, conflicts

# cross-check: within the families, preregistered 64h closed rows == rows
# whose candidate canons contain a 64h WIN canon
fam_rows = {r["s6_hex"] for f in overlay.values() for r in f}
detected64 = {r["s6_hex"] for f in overlay.values() for r in f
              if "pending_close_64h_fold_by_bit" in r}
assert detected64 == (CLOSED64H & fam_rows), (
    sorted(detected64), sorted(CLOSED64H & fam_rows))

# ------------------------------------------------ ranking + selection
# Selection policy (following the published lane plan, commits 0e972b0d /
# 01a8738a): the next pure class-2 target family
# 00000000000000403800000008000000 (18 rows / 1287 occurrences) is the
# designated effective next sweep target; within that family pick the
# cheapest-cost row (then fewest open bits, then hex). The global cheapest
# remaining row 00000000000000801282000040000000 (cost 64, 56 open) belongs
# to the best-coverable family whose third row 00000000000000801202000040000400
# is STERILE (71/71 candidates REFUTED-D10 in the v1 census), so that family
# can never fully close under depth-10 receipts (K0863); it is recorded as
# runner-up.
P_TARGET = "00000000000000403800000008000000"
CLAIMED = {f"{CHILD64H:032x}", f"{CHILD76C:032x}"}
ranked = []
for parent, rows in overlay.items():
    for r in rows:
        hex_ = r["s6_hex"]
        if hex_ in CLAIMED:
            r["excluded"] = "swept/claimed by an in-flight lane (64h/76c)"
            continue
        if hex_ in CLOSED64H:
            r["excluded"] = "closed by the pending cost-64h fold (prereg)"
            continue
        if "pending_close_76c_fold_by_bit" in r:
            r["excluded"] = ("closed by the pending cost-76c fold "
                             f"(bit {r['pending_close_76c_fold_by_bit']})")
            continue
        open_v2 = r["open_after_census"] - r["new_refuted_bits"] \
            - r["new_win_bits"]
        assert open_v2 >= 0, r
        r["open_after_census_v2"] = open_v2
        if open_v2 == 0:
            r["excluded"] = "no open bits remain after the 64h/76c overlay"
            continue
        ranked.append((r["cost"], open_v2, hex_, parent, r))
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
    if st_by_bit[b]["status"] == "harvested_refuted"
    or canon(int(SELECTED, 16) | (1 << b)) in verdict64h
    or canon(int(SELECTED, 16) | (1 << b)) in verdict76c)
sweep_bits = [b for b in sel_bits if b not in known_bits]
runner_up = ranked[0]
assert runner_up[2] != SELECTED or runner_up[3] == P_TARGET

result = {
    "schema": "n11-class2-lane-next-target-presweep-1452-v2-20261116-v1",
    "date": "2026-11-16",
    "chain_head": V1["chain_head"],
    "baseline": {
        "v1_census_json":
            "class2-lane-next-target-presweep-1452-20261116.json "
            "(git blob 0d9a94a272de9fe45708757f17bfea60239a3c9b)",
        "note": ("v1 census head-1452 bit statuses carried over; this v2 "
                 "overlays the post-census 64h/76c sweeps only"),
    },
    "new_verdict_maps": {
        "cost64h": {"child": f"{CHILD64H:032x}", "bits": 64,
                    "win7_d10_bits": win64h_bits,
                    "refuted_d10_bits": sorted(
                        e["bit"] for e in verdict64h.values()
                        if e["verdict"] == "REFUTED-D10"),
                    "source": "raw batches 1-8 (blob-pinned), claim v2"},
        "cost76c": {"child": f"{CHILD76C:032x}", "bits": 76,
                    "win7_d10_bits": win76c_bits,
                    "refuted_d10_bits": sorted(
                        e["bit"] for e in verdict76c.values()
                        if e["verdict"] == "REFUTED-D10"),
                    "source": ("v17 raw batches 1-10 (blob-pinned, "
                               "fbt-repaired engine; v16 agreement 75/76 "
                               "with the single documented bit-113 flip)")},
    },
    "cross_checks": {
        "bit_table_canon_agreement": "16/16 rows, all bits",
        "prereg_win_canon_agreement": "23/23 receipts",
        "prereg_closed_rows_within_families":
            sorted(CLOSED64H & fam_rows),
        "v16_v17_disagreement_bits": [113],
        "verdict_conflicts": 0,
    },
    "claim_hex_verification": CLAIM_CHECK,
    "families_v2": overlay,
    "ranking_top10": [
        {"s6_hex": t[2], "parent": t[3], "cost": t[0],
         "open_after_census_v2": t[1],
         "demand": t[4]["demand"]} for t in ranked[:10]],
    "selection_policy": (
        "primary family = the published next pure class-2 target "
        f"{P_TARGET} (18 rows / 1287 occurrences, designated effective "
        "next sweep target by the head-1452 census); within the family "
        "cheapest cost, then fewest open bits after the 64h/76c overlay, "
        "then hex. The globally cheapest remaining row "
        "00000000000000801282000040000000 (cost 64, 56 open, best-coverable "
        "family) is the runner-up: that family's row "
        "00000000000000801202000040000400 is STERILE (71/71 candidates "
        "REFUTED-D10 at the v1 census), so the family can never fully "
        "close under depth-10 receipts (K0863)"),
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
                      "open_after_census_v2": runner_up[1]},
        "note": ("cheapest remaining unswept/unclaimed row of the primary "
                 "family after excluding the 64h/76c children, the "
                 "preregistered 64h-closed rows and the 76c-pending rows; "
                 "the confirmation bits carry already-known REFUTED-D10 "
                 "verdicts (2 v1 harvest transfers + 1 orbit transfer "
                 "from the cost-64h sweep) and will be re-run fresh for "
                 "confirmation, giving a complete fresh 66-bit row"),
    },
    "interpretation_guard": (
        "search-plan bookkeeping only; no engine search was run, no "
        "verdict was created, no row was closed; WIN7-D10 proves a "
        "first-player win within depth 10 from the individual 7-stone "
        "root only; REFUTED-D10 is not a LOSS proof; the 11x11 empty "
        "board, two-stone roots {49,60}/{59,60}, S2 {59,60} and classes "
        "1/2/4 all remain UNKNOWN"),
}
out_path = OUT / "class2-lane-next-target-presweep-1452-v2-20261116.json"
out_path.write_text(json.dumps(result, indent=1, sort_keys=False) + "\n")
print(f"wrote {out_path} ({out_path.stat().st_size} bytes)")
print("selected:", SELECTED, "cost", sel_row["cost"],
      "open", len(sweep_bits), "confirm", known_bits, "parent", sel[3])
for t in ranked[:8]:
    print(f"  rank: cost {t[0]} open {t[1]} {t[2]} parent {t[3]}")
