#!/usr/bin/env python3
"""n11 class2-lane: second-candidate S5 cost-71 row STERILE determination and
69a/76c takeover transfer computation (2026-11-16).

Second-implementation verification of a structural fact that is implicit in
the published head-1452 presweep census
(class2-lane-next-target-presweep-1452-20261116.json, blob 0d9a94a2...) but
whose theorem-level consequence is not stated anywhere on main yet:

  the cost-71 row 00000000000000801202000040000400 of the second coverable
  class-2 candidate S5 00000000000000801202000040000000 has ALL of its 71
  legal candidate 7-stone roots already verdict-resolved as REFUTED-D10 by
  D4-canonical transfer from published sweeps (zero engine runs needed for
  the row itself);

  by the published K0863 STERILE-row unclosability theorem, no WIN7-D10
  receipt (own-row or cross-cover, present or future) can ever close this
  row, therefore the second coverable class-2 candidate S5 (3 rows / 211
  at head 1452) can never be fully closed within the depth-10 receipt
  system, exactly like the best coverable class-2 S5
  00000000000000801202000000200000 (K0863/K0865).

Protocol:
  1. reproduce the head-1452 basis exactly as the published cost-64h fold
     pre-registration does (module-level exec of the blob-pinned
     fold_projection_head1450_tool, basis 771 roots at head 1450, then the
     four published cost-76d/77e receipt roots -> 775 roots / 760 distinct
     D4 canons at head 1452), asserting the published head-1452 six-number
     summary and demand histogram;
  2. rebuild the lane verdict harvest with an INDEPENDENT parser (different
     code path from the census glob: explicit per-file bit accounting with
     recursive schema-sniffing for win/refuted/capped bit lists plus a
     dedicated audit schema path, raw-batch JSONL parsing for
     76d/77e/64h with pilot control 3402, per-file aggregate cross-check
     against the published census harvest.files table, cross-source
     WIN/REFUTED conflict assertion at every canon insertion), and assert
     the phase-A map (79 published census inputs) reproduces the published
     census totals exactly;
  3. independent D4 canonicalization implementation, asserted equal to the
     published tool's canon on all 121 single-stone masks, all 760 folded
     basis canons, all audit transfer canons and the 23 published cost-64h
     receipt canons;
  4. enumerate the cost-71 row's legal candidates with legal_candidates.py
     (exact Bareiss 4x4, no floating point) and verify child safety over
     all 15 stone quadruples;
  5. classify all 71 candidate canons: receipt-win (folded canon) /
     harvested WIN7-D10 / harvested REFUTED-D10 / open, at head 1452 AND at
     the published projected head 1472 (after the published 23 cost-64h
     receipts), recording the attesting source files per canon;
  6. project the published 23 cost-64h receipts onto head 1452 and re-
     assert the published pre-registration projection (head 1472 six
     numbers and demand histogram); the row stays open and stays fully
     transferred-REFUTED at 1472 as K0863 predicts (out-of-sample check:
     none of the 71 canons is covered by any of the 23 receipts);
  7. compute the same classification for the stale in-flight claims cost-76c
     (child 00000000010000809002000001000000) and cost-69a (child
     00000000000000801222000000800000) as takeover prep, including their
     parents' current row counts at head 1452 from the frontier machinery.

Interpretation guard: this is bookkeeping over published verdicts only; no
engine search is run and no new verdict is created here. A transferred
REFUTED-D10 is a depth-10 refutation of the individual 7-stone root by D4
invariance (the game tree is D4-isomorphic), NOT a LOSS proof of any
position; STERILE means unclosable within the depth-10 WIN7-D10 receipt
system, NOT a LOSS proof of the row, the parent S5, any S2 root or the
board. The 11x11 empty board, the two-stone roots {49,60} and {59,60},
S2 {59,60}, and classes 1/2/4 all remain UNKNOWN.
"""
import csv
import gzip
import hashlib
import json
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
SCRIPTS = HERE / "scripts"
MS5 = HERE.parent / "n11-s2-5960-milestone5-20261112" / "output"
sys.path.insert(0, str(SCRIPTS))
from legal_candidates import cells, det4, legal_candidates  # noqa: E402

CENSUS_JSON = "class2-lane-next-target-presweep-1452-20261116.json"
CENSUS_BLOB = "0d9a94a272de9fe45708757f17bfea60239a3c9b"
PREREG_JSON = "class2-lane-cost64h-fold-preregistration-independent-20261116.json"
CLAIM64H_JSON = "class2-lane-cost64h-inflight-20261116.json"
HEAD_1452 = (1452, 174, 6396, 506144, 4669, 370058)
HEAD_1472 = (1472, 174, 6376, 504672, 4649, 368586)
CENSUS_TOTALS = {"distinct_verdict_canons": 3548,
                 "win7_d10": 353, "refuted_d10": 3195, "conflicts": 0}

S5_SECOND = "00000000000000801202000040000000"
ROW71 = "00000000000000801202000040000400"
ROW64 = "00000000000000801282000040000000"
ROW76C = "00000000010000809002000001000000"
ROW69A = "00000000000000801222000000800000"
P_76C_A = "00000000000000801202000100000000"
P_69A_A = "00000000000000801222000000000000"
P_69A_B = "00000000000000003800000008002000"

WIN_KEYS = ("win7_bits", "win7_d10_bits", "win_bits")
REF_KEYS = ("refuted_d10_bits", "refuted_bits")
CAP_KEYS = ("capped_bits",)
SKIP_KEYS = {"fold"}   # census precedent: fold blocks mix lanes


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


# ---------- 1. published head-1452 basis via the blob-pinned tool ----------
TOOL = SCRIPTS / "fold_projection_head1450_tool_20261116.py"
TOOL_BLOB = "49fcd8ae6706c075b39eea5b115b2a045c2950cf"
tool_data = TOOL.read_bytes()
assert git_blob_sha(tool_data) == TOOL_BLOB, "head-1450 projection tool blob"
ns = {"__file__": str(TOOL), "__name__": "tool1450_import_sterile"}
exec(compile(tool_data.decode(), str(TOOL), "exec"), ns)
tool_canon = ns["canon"]
covers = ns["covers"]
popcount = ns["popcount"]

basis_771 = ns["reconstruct"]()          # asserts every basis blob pin itself
assert len(basis_771) == 771

fold7677 = json.loads((OUT / "class-frontier-cost76d77e-receipts-"
                       "recompute-20261116.json").read_text())
receipt_roots_7677 = []
for rec in fold7677["receipts"]:
    x = int(rec["root_hex"], 16)
    assert popcount(x) == 7
    assert rec["d4_canonical_hex"] == f"{tool_canon(x):032x}"
    receipt_roots_7677.append(x)
assert len(receipt_roots_7677) == 4
assert sorted(fold7677["totals"]["root_hexes"]) == \
    sorted(f"{r:032x}" for r in receipt_roots_7677)
roots_1452 = set(basis_771)
for x in receipt_roots_7677:
    assert x not in roots_1452
    roots_1452.add(x)
assert len(roots_1452) == 775
folded_canons = {tool_canon(r) for r in roots_1452}
assert len(folded_canons) == 760

# frontier machinery (verbatim through the tool's own basis loading)
manifest = set()
for path in sorted(MS5.glob("ms5_s6_manifest_part*.csv")):
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            manifest.add(int(row["hex"], 16))
assert len(manifest) == 7867
with gzip.open(OUT / "s5-remaining-after-reuse.csv.gz", "rt", newline="") as f:
    classes = {r["s5_hex"]: int(r["classes"]) for r in csv.DictReader(f)}
with gzip.open(OUT / "s5-s6-remaining-incidences.csv.gz", "rt",
               newline="") as f:
    incidences = list(csv.DictReader(f))
assert len(incidences) == 14558
winners = set()
with gzip.open(OUT / "win7-reuse-hits.csv.gz", "rt", newline="") as f:
    for row in csv.DictReader(f):
        winners.add(int(row["s6_hex"], 16))
assert len(winners) == 498

LOSS6 = ("00000000000000809202000400000000",
         "00000000000000003800004008000008",
         "00000000000000805202000000002000")
rejected = {r["s5_hex"] for r in incidences
            if int(r["s6_hex"], 16) in {int(x, 16) for x in LOSS6}}


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


solved_1452 = set(winners)
for r in roots_1452:
    solved_1452 |= covers(r)
st = summary(solved_1452)
assert tuple(st[k] for k in
             ("solved_s6_in_manifest", "remaining_s5_orbits",
              "unique_remaining_s6", "sum_remaining_cost",
              "s6_needed_by_open_classes",
              "cost_needed_by_open_classes")) == HEAD_1452, st

# ---------- 3. independent D4 canon implementation ----------
def images8(mask):
    out = []
    for r in range(8):
        v = 0
        for p in range(121):
            if mask >> p & 1:
                x, y = p % 11, p // 11
                if r == 0:
                    a, b = x, y
                elif r == 1:
                    a, b = y, 10 - x
                elif r == 2:
                    a, b = 10 - x, 10 - y
                elif r == 3:
                    a, b = 10 - y, x
                elif r == 4:
                    a, b = 10 - x, y
                elif r == 5:
                    a, b = x, 10 - y
                elif r == 6:
                    a, b = y, x
                else:
                    a, b = 10 - y, 10 - x
                v |= 1 << (11 * b + a)
        out.append(v)
    return out


def my_canon(mask):
    return min(images8(mask))


for p in range(121):
    assert my_canon(1 << p) == tool_canon(1 << p)
for r in roots_1452:
    assert my_canon(r) == tool_canon(r)
canon = my_canon

# ---------- 2. independent harvest rebuild ----------
census = json.loads((OUT / CENSUS_JSON).read_text())
assert git_blob_sha((OUT / CENSUS_JSON).read_bytes()) == CENSUS_BLOB
pub_files = {f["file"]: f for f in census["harvest"]["files"]}
assert len(pub_files) == 79
pub_raw = {n: f for n, f in pub_files.items() if "raw-batch" in n}
assert len(pub_raw) == 2, sorted(pub_raw)

VERDICT = {}            # canon -> {"verdict": ..., "sources": [file,...]}
conflicts = []


def record(child_hex, bit, verdict, source):
    root = int(child_hex, 16) | (1 << bit)
    c = canon(root)
    e = VERDICT.get(c)
    if e is None:
        VERDICT[c] = {"verdict": verdict, "sources": [source]}
    else:
        if e["verdict"] != verdict:
            conflicts.append((child_hex, bit, verdict, e["verdict"],
                              source, e["sources"]))
        e["sources"].append(source)
    return c


def collect_bits(obj):
    """Independent schema sniff: collect every win/refuted/capped bit-list
    match anywhere under obj (skipping SKIP_KEYS subtrees), asserting all
    matches per verdict class are identical. Returns (wins, refs, caps) with
    None for absent classes."""
    found = {"w": [], "r": [], "c": []}

    def flat_of(v):
        if isinstance(v, list):
            return sorted({int(b) for b in v})
        if isinstance(v, dict):
            vals = list(v.values())
            if all(not isinstance(x, (list, dict)) for x in vals):
                return sorted({int(b) for b in v})      # keyed by bit
            return sorted({int(b) for vv in vals
                           for b in (vv if isinstance(vv, list)
                                     else vv.values() if isinstance(vv, dict)
                                     else [vv])})
        return None

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in SKIP_KEYS:
                    continue
                if isinstance(v, (list, dict)):
                    if k in WIN_KEYS or k in REF_KEYS or k in CAP_KEYS:
                        flat = flat_of(v)
                        if flat is not None:
                            if k in WIN_KEYS:
                                found["w"].append(flat)
                            elif k in REF_KEYS:
                                found["r"].append(flat)
                            else:
                                found["c"].append(flat)
                    walk(v)
        elif isinstance(o, list):
            for e in o:
                walk(e)

    walk(obj)
    out = []
    for cls in ("w", "r", "c"):
        lst = found[cls]
        assert all(x == lst[0] for x in lst), "inconsistent bit lists"
        out.append(lst[0] if lst else None)
    return out


def sniff_child(obj):
    for key in ("s6_child_hex", "s6_child", "child"):
        v = obj.get(key)
        if isinstance(v, str) and len(v) == 32:
            return v
    pd = obj.get("parent_derivation") or {}
    for key in ("s6_child", "child"):
        v = pd.get(key)
        if isinstance(v, str) and len(v) == 32:
            return v
    return None


harvest_rows = []
claim_files = sorted(set(pub_files) - set(pub_raw))
for name in claim_files:
    d = json.loads((OUT / name).read_text())
    pub = pub_files[name]
    child = sniff_child(d)
    assert child == pub["child"], (name, child, pub["child"])
    cands = sorted(legal_candidates(child)[1])
    assert len(cands) == pub["candidates"], name
    if "sweep_aggregate" in d:            # dedicated audit schema path
        sa = d["sweep_aggregate"]
        wins, _, _ = collect_bits({"win7_d10_bits": sa["win7_d10_bits"]})
        swept = sorted({b for batch in sa["batches"]
                        for b in batch["candidate_bits"]})
        transfers = {int(k): v for k, v in (d.get("transfers") or {}).items()}
        assert set(transfers) <= set(cands), name
        assert sorted(set(swept) | set(transfers)) == cands, name
        for bit, tr in transfers.items():
            assert my_canon(int(tr["root"], 16)) == int(tr["d4_canon"], 16), \
                (name, bit)
        refs = sorted(set(cands) - set(wins))
        assert sa["capped"] == 0, name
        assert sa["refuted_d10_swept"] + sa["refuted_d10_transferred"] == \
            len(refs), name
        assert sa["refuted_d10_transferred"] == len(transfers), name
        caps = []
    else:
        wins, refs, caps = collect_bits(d)
        if wins is None:
            raise SystemExit(f"no win bits found in {name}")
        if caps is None:
            caps = []
        if refs is None:
            refs = sorted(set(cands) - set(wins) - set(caps))
    assert len(wins) == pub["win7"], (name, pub["win7"], len(wins))
    assert len(refs) == pub["refuted"], (name, pub["refuted"], len(refs))
    assert len(caps) == pub["capped"], name
    assert set(wins) | set(refs) | set(caps) == set(cands), name
    assert not (set(wins) & set(refs)), name
    for b in wins:
        record(child, b, "WIN7-D10", name)
    for b in refs:
        record(child, b, "REFUTED-D10", name)
    harvest_rows.append({"file": name, "child": child,
                         "candidates": len(cands), "win7": len(wins),
                         "refuted": len(refs), "capped": len(caps)})

# raw batches, parsed from the published JSONL files (76d/77e: 10 batches of
# 8/8 bits; 64h: 8 batches of 8 bits - published after the census)
def parse_raw(tmpl, rng, child_hex):
    bits_seen = {}
    pilot_nodes = set()
    node_sum = 0
    for n in rng:
        for line in (OUT / tmpl.format(n=n)).read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if "control" in r:
                assert r["loss"] is False and r["capped"] is False
                pilot_nodes.add(r["nodes"])
            else:
                assert r["bit"] not in bits_seen, (tmpl, r["bit"])
                assert r["andclose"] is True and r["capped"] is False
                assert popcount(int(child_hex, 16) | (1 << r["bit"])) == 7
                bits_seen[r["bit"]] = ("WIN7-D10" if r["loss"] is True
                                       else "REFUTED-D10")
                node_sum += r["nodes"]
    assert pilot_nodes == {3402}, (tmpl, pilot_nodes)
    assert sorted(bits_seen) == sorted(legal_candidates(child_hex)[1]), tmpl
    win_bits = sorted(b for b, v in bits_seen.items() if v == "WIN7-D10")
    return bits_seen, win_bits, node_sum


bits76d, win76d, nodes76d = parse_raw(
    "class2-lane-cost76d-raw-batch{n}-20261116.jsonl", range(1, 11),
    "00000000040000003800080008000000")
bits77e, win77e, nodes77e = parse_raw(
    "class2-lane-cost77e-raw-batch{n}-20261116.jsonl", range(1, 11),
    "00000000040000809002000000004000")
assert win76d == [19, 49] and win77e == [37, 69]

# phase A = the census input set: 77 claim files + 76d/77e raw batches
for child_hex, bits in (("00000000040000003800080008000000", bits76d),
                        ("00000000040000809002000000004000", bits77e)):
    for b, v in bits.items():
        record(child_hex, b, v, "cost-76d-raw-batches" if bits is bits76d
               else "cost-77e-raw-batches")
# census aggregate entries for the raw batches
for n, f in pub_raw.items():
    if "76d" in n:
        assert (f["candidates"], f["win7"], f["refuted"], f["capped"]) == \
            (76, 2, 74, 0), f
    else:
        assert (f["candidates"], f["win7"], f["refuted"], f["capped"]) == \
            (77, 2, 75, 0), f

assert not conflicts, conflicts[:5]
phase_a = {
    "distinct_verdict_canons": len(VERDICT),
    "win7_d10": sum(1 for v in VERDICT.values()
                    if v["verdict"] == "WIN7-D10"),
    "refuted_d10": sum(1 for v in VERDICT.values()
                       if v["verdict"] == "REFUTED-D10"),
    "conflicts": len(conflicts),
}
assert phase_a == CENSUS_TOTALS, (phase_a, CENSUS_TOTALS)

# phase B: the published cost-64h raw sweep (postdates the census); the
# published claim v2 records counts and node sums, the raw batches carry
# the per-bit verdicts
bits64h, win64h, nodes64h = parse_raw(
    "class2-lane-cost64h-raw-batch{n}-20261116.jsonl", range(1, 9),
    "00000000000000403800000008100000")
claim64h = json.loads((OUT / CLAIM64H_JSON).read_text())
sr64h = claim64h["sweep_results"]
assert sr64h["candidates_resolved"] == len(bits64h) == 64
assert sorted(sr64h["win7_d10_bits"]) == win64h, "claim v2 win bits"
assert sr64h["refuted_d10_count"] == 64 - len(win64h) == 41
assert sr64h["capped_count"] == 0
assert sr64h["node_sum_v16"] == nodes64h == 47017565, nodes64h
before = len(VERDICT)
for b, v in bits64h.items():
    record("00000000000000403800000008100000", b, v,
           "cost-64h-raw-batches")
assert not conflicts, conflicts[:5]
n_new_canons_64h = len(VERDICT) - before
n_win = sum(1 for v in VERDICT.values() if v["verdict"] == "WIN7-D10")
n_ref = len(VERDICT) - n_win

# ---------- 4+5. the cost-71 row ----------
def child_safe(hexstr):
    rows = []
    for i in cells(hexstr):
        x, y = i % 11, i // 11
        rows.append([x * x + y * y, x, y, 1])
    return all(det4([rows[a], rows[b], rows[c], rows[d]]) != 0
               for a, b, c, d in combinations(range(len(rows)), 4))


def classify_row(row_hex, receipt_canons):
    bits = sorted(legal_candidates(row_hex)[1])
    out = []
    for b in bits:
        c = canon(int(row_hex, 16) | (1 << b))
        if c in receipt_canons:
            stt = "receipt_win"
        elif c in VERDICT:
            stt = ("harvested_win" if VERDICT[c]["verdict"] == "WIN7-D10"
                   else "harvested_refuted")
        else:
            stt = "open"
        out.append({"bit": b, "status": stt, "root_canon": f"{c:032x}",
                    "sources": VERDICT[c]["sources"] if c in VERDICT else []})
    return bits, out


assert child_safe(ROW71)
bits71, per71 = classify_row(ROW71, folded_canons)
assert len(bits71) == 71, len(bits71)
st71 = defaultdict(int)
for e in per71:
    st71[e["status"]] += 1
assert dict(st71) == {"harvested_refuted": 71}, dict(st71)

# row must still be open at head 1452 and be a row of the second-candidate S5
assert int(ROW71, 16) not in solved_1452
rem, uniq, dem, _ = frontier(solved_1452)
rows_second = [r for r in rem[S5_SECOND]]
assert sorted(r["s6_hex"] for r in rows_second) == \
    sorted([ROW71, ROW64, ROW76C]), sorted(r["s6_hex"] for r in rows_second)
assert all(int(r["s6_s7_edge_cost"]) == len(legal_candidates(r["s6_hex"])[1])
           for r in rows_second)
d71 = dem[ROW71]
assert d71 == {"c1": 0, "c2": 2, "c4": 0}, d71

# ---------- 6. the projected head 1472 keeps the row open ----------
prereg = json.loads((OUT / PREREG_JSON).read_text())
receipts23 = [int(r["root_hex"], 16) for r in prereg["receipts"]]
assert len(receipts23) == 23
assert sorted(r["bit"] for r in prereg["receipts"]) == win64h
solved_1472 = set(solved_1452)
canons_1472 = set(folded_canons)
for r in receipts23:
    assert popcount(r) == 7
    c = canon(r)
    assert c not in folded_canons
    canons_1472.add(c)
    assert VERDICT[c]["verdict"] == "WIN7-D10", f"{r:032x}"
    solved_1472 |= covers(r)
assert len(canons_1472) == 783
st14 = summary(solved_1472)
assert tuple(st14[k] for k in
             ("solved_s6_in_manifest", "remaining_s5_orbits",
              "unique_remaining_s6", "sum_remaining_cost",
              "s6_needed_by_open_classes",
              "cost_needed_by_open_classes")) == HEAD_1472, st14
assert st14["hist"] == prereg["projected_demand_histogram"], \
    (st14["hist"], prereg["projected_demand_histogram"])
for row in (ROW71, ROW76C, ROW69A):
    assert int(row, 16) not in solved_1472

# K0863 out-of-sample: none of the 71 canons is covered by the 23 receipts
_, per71_1472 = classify_row(ROW71, canons_1472)
st71_1472 = defaultdict(int)
for e in per71_1472:
    st71_1472[e["status"]] += 1
assert dict(st71_1472) == {"harvested_refuted": 71}, dict(st71_1472)

# ---------- 7. takeover prep: 76c and 69a ----------
assert child_safe(ROW76C) and child_safe(ROW69A)
bits76c, per76c = classify_row(ROW76C, folded_canons)
bits69a, per69a = classify_row(ROW69A, folded_canons)
assert len(bits76c) == 76 and len(bits69a) == 69
c76c = defaultdict(int)
for e in per76c:
    c76c[e["status"]] += 1
c69a = defaultdict(int)
for e in per69a:
    c69a[e["status"]] += 1
_, per76c_1472 = classify_row(ROW76C, canons_1472)
_, per69a_1472 = classify_row(ROW69A, canons_1472)
c76c_1472 = defaultdict(int)
for e in per76c_1472:
    c76c_1472[e["status"]] += 1
c69a_1472 = defaultdict(int)
for e in per69a_1472:
    c69a_1472[e["status"]] += 1

# parent bookkeeping at head 1452 (engine-independent facts for the claims)
parents_1452 = {}
for s5 in (S5_SECOND, P_76C_A, P_69A_A, P_69A_B):
    rows = rem.get(s5, [])
    parents_1452[s5] = {
        "classes": classes.get(s5, 0),
        "rows": len(rows),
        "edge_cost": sum(int(r["s6_s7_edge_cost"]) for r in rows),
    }
d76c = dem[ROW76C]
d69a = dem[ROW69A]
assert d76c == {"c1": 0, "c2": 2, "c4": 0}, d76c
assert d69a == {"c1": 0, "c2": 2, "c4": 0}, d69a

# the claim v1 six-deletion facts re-derived independently
for row_hex, expect_parents in ((ROW76C, {P_76C_A, S5_SECOND}),
                                (ROW69A, {P_69A_A, P_69A_B})):
    v = int(row_hex, 16)
    dels = {f"{canon(v ^ (1 << s)):032x}" for s in cells(row_hex)}
    assert len(dels) == 6, (row_hex, dels)     # six distinct S5 deletion lifts
    # the open coverable class-2 parents claimed in v1 must be among them
    assert expect_parents <= dels, (row_hex, dels, expect_parents)

result = {
    "schema": ("n11-class2-lane-secondcandidate-cost71-sterile-"
               "verification-20261116-v1"),
    "date": "2026-11-16",
    "method": (
        "second implementation: published head-1452 basis reproduced through "
        "the blob-pinned fold_projection_head1450_tool (basis 771 roots at "
        "1450 + the four published cost-76d/77e receipt roots = 775 roots / "
        "760 distinct D4 canons at head 1452, head six-number summary and "
        "demand histogram re-asserted); independent verdict-harvest parser "
        "over the 77 published claim/audit files (recursive bit-list "
        "collection with per-class identity assertion and a dedicated "
        "audit-schema path cross-checking per-transfer D4 canons) plus "
        "raw-batch JSONL parsing for cost-76d/77e/64h with pilot control "
        "3402 and per-bit conflict assertion at every canon insertion; the "
        "phase-A map over the exact published census input set reproduces "
        "the published census totals (3548/353/3195, 0 conflicts); "
        "independent D4 canonicalization asserted equal to the published "
        "tool canon on all 121 single-stone masks and all 760 folded canons; "
        "legal candidate enumeration via legal_candidates.py (exact Bareiss "
        "4x4)"),
    "controls": {
        "head_1452_reproduced": True,
        "head_1472_projection_reproduced": True,
        "head_1472_histogram_matches_prereg": True,
        "harvest_claim_files_cross_checked": len(harvest_rows),
        "phase_a_matches_census_totals": phase_a,
        "harvest_conflicts_total": len(conflicts),
        "cost64h_new_canons_vs_phase_a": n_new_canons_64h,
        "independent_canon_agrees_with_tool": True,
        "audit_transfer_canons_cross_checked": True,
        "census_blob": CENSUS_BLOB,
    },
    "basis": {
        "head": "1452/174/6396/506144/4669/370058",
        "receipt_roots": 775,
        "distinct_d4_canons": 760,
        "projected_head_after_cost64h": "1472/174/6376/504672/4649/368586",
        "projected_per_prereg_blob": True,
    },
    "harvest": {
        "distinct_verdict_canons": len(VERDICT),
        "win7_d10": n_win,
        "refuted_d10": n_ref,
        "phase_a_inputs": len(harvest_rows) + 2,
        "phase_b_cost64h_bits": len(bits64h),
        "cost64h_wins": win64h,
    },
    "row71_sterile": {
        "s6_hex": ROW71,
        "parent_s5": S5_SECOND,
        "legal_candidates": len(bits71),
        "child_safe": True,
        "status_counts_1452": dict(st71),
        "status_counts_projected_1472": dict(st71_1472),
        "per_bit": per71,
        "engine_runs_needed_for_row_verdicts": 0,
        "determination": (
            "all 71 legal candidate roots of this row are REFUTED-D10 by "
            "D4-canonical transfer from published sweeps; the row is "
            "STERILE in the K0863 sense without any engine run of its own"),
        "k0863_consequence": (
            "by the published STERILE-row unclosability theorem (K0863, "
            "commit 4122ea73), no WIN7-D10 receipt can cover this row, own "
            "or cross; therefore the second coverable class-2 candidate S5 "
            "00000000000000801202000040000000 (3 rows / 211 edge cost at "
            "head 1452: this cost-71 row, the cost-64 row "
            "00000000000000801282000040000000 and the cost-76c row "
            "00000000010000809002000001000000) can never be fully closed "
            "within the depth-10 receipt system; it should be reclassified "
            "from coverable class-2 to the depth>10-evidence-waiting "
            "category, exactly like the best coverable class-2 S5 "
            "00000000000000801202000000200000"),
        "k0863_out_of_sample_check": (
            "the 23 published cost-64h receipts cover none of the row's 71 "
            "candidate canons (0 receipt_win statuses at the projected "
            "head 1472 as well), a passing out-of-sample consistency check "
            "of K0863 on a row that was never swept as a lane"),
        "scope_guard": (
            "STERILE and unclosable-within-depth-10 are NOT loss proofs; "
            "the row, the parent S5, all S2 roots and the 11x11 empty "
            "board remain UNKNOWN; the row stays open in the manifest "
            "bookkeeping forever under the depth-10 receipt system"),
    },
    "takeover_prep": {
        "cost76c": {
            "s6_hex": ROW76C, "legal_candidates": 76,
            "status_counts_1452": dict(c76c),
            "status_counts_projected_1472": dict(c76c_1472),
            "per_bit": per76c,
            "demand_at_1452": d76c,
            "open_parents_at_1452": [
                {"s5_hex": P_76C_A, **parents_1452[P_76C_A]},
                {"s5_hex": S5_SECOND, **parents_1452[S5_SECOND]},
            ],
            "note": ("stale claim (2026-11-15T20:54Z, zero published raw "
                     "batches) taken over by the long-term lane session; "
                     "the S5-parent closure motivation is void per "
                     "row71_sterile.k0863_consequence, the remaining value "
                     "is the row itself for its second parent and the "
                     "harvest verdicts"),
        },
        "cost69a": {
            "s6_hex": ROW69A, "legal_candidates": 69,
            "status_counts_1452": dict(c69a),
            "status_counts_projected_1472": dict(c69a_1472),
            "per_bit": per69a,
            "demand_at_1452": d69a,
            "open_parents_at_1452": [
                {"s5_hex": P_69A_A, **parents_1452[P_69A_A]},
                {"s5_hex": P_69A_B, **parents_1452[P_69A_B]},
            ],
            "note": ("stale claim (2026-11-16T01:31Z, zero published raw "
                     "batches); three bits (55/65/109) were already "
                     "precomputed as transferred REFUTED in the published "
                     "claim; the harvest re-derivation here re-counts them "
                     "plus any newer transfers (incl. cost-64h)"),
        },
    },
    "unknown_status": (
        "11x11 empty board: UNKNOWN. This verification creates no verdict "
        "and closes no row; solved counts are manifest bookkeeping; "
        "REFUTED-D10 is not a LOSS proof; STERILE is not a LOSS proof; the "
        "two-stone roots {49,60} and {59,60}, S2 {59,60} and classes 1/2/4 "
        "all remain UNKNOWN"),
}
out_path = OUT / ("class2-lane-secondcandidate-cost71-row-sterile-"
                  "verification-20261116.json")
with open(out_path, "w") as f:
    json.dump(result, f, indent=1, sort_keys=True)
    f.write("\n")
print("wrote", out_path.name)
print("row71 statuses 1452:", dict(st71), "| 1472:", dict(st71_1472))
print("76c statuses 1452:", dict(c76c), "| 1472:", dict(c76c_1472))
print("69a statuses 1452:", dict(c69a), "| 1472:", dict(c69a_1472))
print("phase A:", phase_a)
print("harvest canons:", len(VERDICT), "win", n_win, "refuted", n_ref,
      "conflicts", len(conflicts), "64h new canons", n_new_canons_64h)
print("parents at 1452:", json.dumps(parents_1452, indent=1))
