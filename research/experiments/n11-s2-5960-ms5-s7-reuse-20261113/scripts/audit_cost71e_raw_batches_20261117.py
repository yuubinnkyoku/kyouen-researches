#!/usr/bin/env python3
"""Audit the cost71e raw sweep batches (stdlib only, bookkeeping).

Repo-layout script: reads the 9 raw batch files (batches 1-8 sweep +
batch 9 confirmation), the determinism rerun files, the v15 cross-check
files, the 64h/66i/64d published raw records for the cross-source scan,
and the published claim v1 from output/; asserts every check; writes
output/class2-lane-cost71e-raw-sweep-audit-20261117.json.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from legal_candidates import legal_candidates  # noqa: E402

CHILD = "00000000000000c09002000000002000"
CLAIM_V1_BLOB = "f64394741142258206149e652f68e2af558b1cff"


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


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


# ------------------------------------------------------- 1. aggregate raws
bits = {}
controls = 0
control_nodes = None
total_nodes = 0
batch_pins = {}
for n in range(1, 10):
    f = OUT / f"class2-lane-cost71e-raw-batch{n}-20261117.jsonl"
    b = f.read_bytes()
    batch_pins[f"batch{n}"] = git_blob_sha(b)
    for line in b.decode().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if "control" in r:
            controls += 1
            assert r == {"control": "pilot_d6", "loss": False,
                         "nodes": 3402, "capped": False}, r
        else:
            assert r["bit"] not in bits, r
            assert r["andclose"] is True and r["capped"] is False, r
            assert r["terminalStoneRange"] == [13, 17], r
            bits[r["bit"]] = r
            total_nodes += r["nodes"]
assert controls == 9
st, lc = legal_candidates(CHILD)
cands = sorted(lc)
assert sorted(bits) == cands and len(bits) == 71
wins = sorted(b for b, r in bits.items() if r["loss"] is True)
refuted = sorted(b for b, r in bits.items() if r["loss"] is False)
capped = sorted(b for b, r in bits.items() if r["capped"])
assert not capped
assert len(wins) + len(refuted) == 71
assert wins == [3, 4, 8, 41, 54, 58, 76, 79, 94, 96, 100, 116, 119], wins

# --------------------------------------------- 2. claim v1 agreement checks
claim_path = OUT / "class2-lane-cost71e-inflight-20261117.json"
claim = json.loads(claim_path.read_bytes())
assert git_blob_sha(claim_path.read_bytes()) == CLAIM_V1_BLOB
assert claim["s6_child"] == CHILD
assert claim["engine_candidate_bits"]["open_bit_count"] == 68
assert sorted(claim["engine_candidate_bits"]["open_bits"]) == \
    sorted(set(cands) - {20, 67, 97})
assert claim["engine_candidate_bits"]["confirmation_bits"] == [20, 67, 97]
child_v = int(CHILD, 16)
canon_of = {}
for b_ in cands:
    canon_of[b_] = canon(child_v | (1 << b_))
# internal canon collisions
collisions = {}
seen = {}
for b_, c in canon_of.items():
    if c in seen:
        collisions[f"{seen[c]},{b_}"] = f"{c:032x}"
    seen[c] = b_
assert not collisions
# transfer canon match (3/3) + predicted verdicts + actual agreement
transfer_outcome = {}
for b_ in (20, 67, 97):
    t = claim["transfers"][str(b_)]
    assert t["root_canon"] == f"{canon_of[b_]:032x}", (b_, t)
    pred = t["verdict"]
    got = "WIN7-D10" if bits[b_]["loss"] is True else "REFUTED-D10"
    assert pred == "REFUTED-D10" and got == "REFUTED-D10", (b_, pred, got)
    transfer_outcome[str(b_)] = {
        "predicted": pred, "actual": got, "match": True}

# --------------------------------- 3. cross-source conflict scan (canon-eq)
xscan = {"sources": [], "conflicts": 0, "agreements": {}}
# 64h bit 97 (published raw batch6)
r64h = None
for line in (OUT / "class2-lane-cost64h-raw-batch6-20261116.jsonl").\
        read_text().splitlines():
    rr = json.loads(line)
    if rr.get("bit") == 97:
        r64h = rr
assert r64h is not None and r64h["loss"] is False
c64h = canon(int("00000000000000403800000008100000", 16) | (1 << 97))
assert c64h == canon_of[20]
xscan["sources"].append("cost64h raw batch6 bit 97 (canon-equal to 71e bit 20)")
xscan["agreements"]["71e bit 20 = 64h bit 97"] = {
    "verdict": "REFUTED-D10 both", "nodes_64h": r64h["nodes"],
    "nodes_71e": bits[20]["nodes"]}
# 66i bit 107 (published raw batch7)
r66i = None
for line in (OUT / "class2-lane-cost66i-raw-batch7-20261116.jsonl").\
        read_text().splitlines():
    rr = json.loads(line)
    if rr.get("bit") == 107:
        r66i = rr
assert r66i is not None and r66i["loss"] is False
c66i = canon(int("00000000000000801226000000000000", 16) | (1 << 107))
assert c66i == canon_of[67]
xscan["sources"].append("cost66i raw batch7 bit 107 (canon-equal to 71e bit 67)")
xscan["agreements"]["71e bit 67 = 66i bit 107"] = {
    "verdict": "REFUTED-D10 both", "nodes_66i": r66i["nodes"],
    "nodes_71e": bits[67]["nodes"]}
# pre-64h harvest (cost64d raw batches, canon-equal to 71e bit 97)
r64d = None
b64d = None
d64h_child = int("00000000000000801202000040000400", 16)
# 64d child hex: from the cost64d inflight claim
d = json.loads((OUT / "class2-lane-cost64d-inflight-20261116.json").read_bytes())
dchild = d["s6_child"]
for n in range(1, 9):
    f = OUT / f"class2-lane-cost64d-raw-batch{n}-20261116.jsonl"
    for line in f.read_text().splitlines():
        rr = json.loads(line)
        if "bit" not in rr:
            continue
        c = canon(int(dchild, 16) | (1 << rr["bit"]))
        if c == canon_of[97]:
            assert r64d is None
            r64d, b64d = rr, rr["bit"]
assert r64d is not None and r64d["loss"] is False
xscan["sources"].append(
    f"cost64d raw batches bit {b64d} (canon-equal to 71e bit 97; "
    "pre-64h harvest source of the census v5 overlay)")
xscan["agreements"][f"71e bit 97 = 64d bit {b64d}"] = {
    "verdict": "REFUTED-D10 both", "nodes_64d": r64d["nodes"],
    "nodes_71e": bits[97]["nodes"]}
assert xscan["conflicts"] == 0

# ------------------------------------------------ 4. determinism + v15
def load_recs(p):
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


det = {}
for name, n, bl in (("batch1", 1, "0,1,2,3,4,6,7,8,9"),
                    ("batch6", 6, "86,87,88,91,92,94,95,96,98")):
    orig = load_recs(OUT / f"class2-lane-cost71e-raw-batch{n}-"
                                 "20261117.jsonl")
    rerun = load_recs(OUT / f"class2-lane-cost71e-det-batch{n}-"
                                 "20261117.jsonl")
    assert len(orig) == len(rerun)
    for x, y in zip(orig, rerun):
        for k in set(x) | set(y):
            if k == "ms":
                continue
            assert x.get(k) == y.get(k), (n, k)
    det[name] = "field-identical on every non-ms field"

v15 = {}
v15_ctrl = 0
for f in ("class2-lane-cost71e-v15-crosscheck-a-20261117.jsonl",
          "class2-lane-cost71e-v15-crosscheck-b-20261117.jsonl",
          "class2-lane-cost71e-v15-crosscheck-c-20261117.jsonl"):
    for r in load_recs(OUT / f):
        if "control" in r:
            v15_ctrl += 1
            assert r == {"control": "pilot_d6", "loss": False,
                         "nodes": 5949, "capped": False}, r
        else:
            assert r["bit"] not in v15
            v15[r["bit"]] = r
assert v15_ctrl == 3 and sorted(v15) == wins
for b_ in wins:
    assert v15[b_]["loss"] is True and v15[b_]["capped"] is False
    assert bits[b_]["loss"] is True and bits[b_]["capped"] is False

# ------------------------------------------------------------- 5. output
audit = {
    "schema": "n11-class2-lane-cost71e-raw-sweep-audit-20261117-v1",
    "date": "2026-11-17",
    "status": ("all checks passed; 13 WIN7-D10 + 58 REFUTED-D10, 0 capped; "
               "3/3 confirmation transfers REFUTED-D10 as predicted by the "
               "census v5 overlay; 13/13 v15 WIN agreement; 9/9 pilot "
               "controls exact; 11x11 UNKNOWN"),
    "target": {
        "s5": "00000000000000403800000008000000",
        "s6_child": CHILD,
        "legal_candidate_count": 71,
        "canonical_head_at_sweep": "1472/174/6376/504672/4649/368586",
        "selection": ("head-1472 presweep census v5 selected target "
                      "(class2-lane-next-target-presweep-1472-v5-"
                      "20261117.json, git blob "
                      "ea85c02319350b5953e0e70c3eb812fb78bbf17c; claim v1 "
                      "git blob " + CLAIM_V1_BLOB + ")"),
        "engine": ("class4_child1_runner_v17.ts, git blob "
                   "c132cc6425eee3feaeef1d697dd74f968cfedb59, depth 10, "
                   "cap 1e9, andclose 1"),
    },
    "pilot_checks": {"batches": 9, "pilot_nodes_each": 3402,
                     "all_exact": True},
    "verdicts": {
        "win7_d10_bits": wins,
        "win7_d10_nodes": {str(b): bits[b]["nodes"] for b in wins},
        "refuted_d10_bits": refuted,
        "capped_count": 0,
        "candidate_nodes_total": total_nodes,
        "total_nodes_including_pilots": total_nodes + 9 * 3402,
        "terminal_stone_range": [13, 17],
    },
    "confirmation_bits": {
        "bits": [20, 67, 97],
        "verdicts": {"20": "REFUTED-D10", "67": "REFUTED-D10",
                      "97": "REFUTED-D10"},
        "predicted_by_census_v5_overlay": True,
        "outcome": transfer_outcome,
    },
    "determinism_rerun": {
        "batches": [1, 6],
        "batch1_note": "contains WIN bits 3/4/8",
        "batch6_note": "contains the heaviest bit 88 (9,928,319 nodes)",
        "field_identical_non_ms": True,
    },
    "v15_cross_engine_check": {
        "engine": "v15 (blob 8744fc65b6b7cac6bd561403ce4c749e01c51359)",
        "pilot_nodes_each": 5949,
        "win_bit_agreement": "13/13",
        "capped": 0,
        "v15_win_nodes": {str(b): v15[b]["nodes"] for b in wins},
    },
    "canon_checks": {
        "child_stones_bit_indices":
            [p for p in range(121) if child_v >> p & 1],
        "transfer_canons_match_claim": "3/3",
        "internal_canon_collisions": collisions,
        "v1_bit_table": ("this child has no v1 head-1452 census bit table "
                         "(not one of the 16 bit-table children); the "
                         "pre-sweep knowledge came from the census v5 "
                         "rebuilt harvest + six-map overlay"),
    },
    "cross_source_conflict_scan": xscan,
    "raw_batch_pins": batch_pins,
    "interpretation_guard": (
        "engine bookkeeping audit only; WIN7-D10 proves a first-player "
        "win within depth 10 from the individual 7-stone root only; "
        "REFUTED-D10 is not a LOSS proof; no manifest row is closed by "
        "this audit; the receipt fold stays pending behind the "
        "76c/66i/66j/69j folds; the 11x11 empty board, the two-stone "
        "roots {49,60} and {59,60}, S2 {59,60} and classes 1/2/4 "
        "remain UNKNOWN"),
}

out = OUT / "class2-lane-cost71e-raw-sweep-audit-20261117.json"
payload = json.dumps(audit, indent=1, ensure_ascii=True) + "\n"
out.write_bytes(payload.encode())
print(f"wrote {out} ({out.stat().st_size} bytes)")
print("win bits:", wins)
print("total nodes:", total_nodes)
print("64d canon-equal bit:", b64d, "nodes", r64d["nodes"])
