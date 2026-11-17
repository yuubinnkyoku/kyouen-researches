#!/usr/bin/env python3
"""Audit the cost72d raw sweep batches (stdlib only, bookkeeping).

Adapted from audit_cost71e_raw_batches_20261117.py (same design, paths and
constants changed for the cost-72 row 00000000000000403800000008004000):
reads the 9 raw batch files (batches 1-8 sweep + batch 9 confirmation),
the determinism rerun files, the v15 cross-check files, the published
69j/64h/66i/66j raw records for the cross-source scan, the 69c sweep JSON
(the pre-64h harvest source of confirmation bit 115), and the published
cost72d claim v1 from output/; asserts every check; writes
output/class2-lane-cost72d-raw-sweep-audit-20261117.json.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from legal_candidates import legal_candidates  # noqa: E402

CHILD = "00000000000000403800000008004000"
CLAIM_V1_BLOB = "b4454257b73a471417bcad0dd3172fd035e493b8"


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
total_nodes = 0
batch_pins = {}
for n in range(1, 10):
    suffix = "9-confirmation" if n == 9 else str(n)
    f = OUT / f"class2-lane-cost72d-raw-batch{suffix}-20261117.jsonl"
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
assert sorted(bits) == cands and len(bits) == 72
wins = sorted(b for b, r in bits.items() if r["loss"] is True)
refuted = sorted(b for b, r in bits.items() if r["loss"] is False)
capped = sorted(b for b, r in bits.items() if r["capped"])
assert not capped
assert len(wins) + len(refuted) == 72
assert wins == [1, 6, 24, 25, 43, 49, 75, 80, 83, 98, 114], wins

# --------------------------------------------- 2. claim v1 agreement checks
claim_path = OUT / "class2-lane-cost72d-inflight-20261117.json"
claim = json.loads(claim_path.read_bytes())
assert git_blob_sha(claim_path.read_bytes()) == CLAIM_V1_BLOB
assert claim["s6_child"] == CHILD
assert claim["engine_candidate_bits"]["open_bit_count"] == 67
CONFIRM = [5, 20, 103, 108, 115]
assert sorted(claim["engine_candidate_bits"]["open_bits"]) == \
    sorted(set(cands) - set(CONFIRM))
assert claim["engine_candidate_bits"]["confirmation_bits"] == CONFIRM
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
# transfer canon match (5/5) + predicted verdicts + actual agreement
transfer_outcome = {}
for b_ in CONFIRM:
    t = claim["transfers"][str(b_)]
    assert t["root_canon"] == f"{canon_of[b_]:032x}", (b_, t)
    pred = t["verdict"]
    got = "WIN7-D10" if bits[b_]["loss"] is True else "REFUTED-D10"
    assert pred == "REFUTED-D10" and got == "REFUTED-D10", (b_, pred, got)
    transfer_outcome[str(b_)] = {
        "predicted": pred, "actual": got, "match": True}

# --------------------------------- 3. cross-source conflict scan (canon-eq)
xscan = {"sources": [], "conflicts": 0, "agreements": {}}


def find_raw_record(fname, want_bit, want_child):
    hit = None
    for line in (OUT / fname).read_text().splitlines():
        if not line.strip():
            continue
        rr = json.loads(line)
        if rr.get("bit") == want_bit:
            assert hit is None
            hit = rr
    assert hit is not None, (fname, want_bit)
    c = canon(int(want_child, 16) | (1 << want_bit))
    return hit, c


# 69j bit 14 (cost72d bit 5)
r69j, c69j = find_raw_record(
    "class2-lane-cost69j-raw-batch2-20261117.jsonl", 14,
    "00000000000000403800000008000020")
assert r69j["loss"] is False and c69j == canon_of[5]
xscan["sources"].append("cost69j raw batch2 bit 14 (canon-equal to 72d bit 5)")
xscan["agreements"]["72d bit 5 = 69j bit 14"] = {
    "verdict": "REFUTED-D10 both", "nodes_69j": r69j["nodes"],
    "nodes_72d": bits[5]["nodes"]}
# 64h bit 14 (cost72d bit 20)
r64h, c64h = find_raw_record(
    "class2-lane-cost64h-raw-batch1-20261116.jsonl", 14,
    "00000000000000403800000008100000")
assert r64h["loss"] is False and c64h == canon_of[20]
xscan["sources"].append("cost64h raw batch1 bit 14 (canon-equal to 72d bit 20)")
xscan["agreements"]["72d bit 20 = 64h bit 14"] = {
    "verdict": "REFUTED-D10 both", "nodes_64h": r64h["nodes"],
    "nodes_72d": bits[20]["nodes"]}
# 66i bit 34 (cost72d bit 103)
r66i, c66i = find_raw_record(
    "class2-lane-cost66i-raw-batch4-20261116.jsonl", 34,
    "00000000000000801226000000000000")
assert r66i["loss"] is False and c66i == canon_of[103]
xscan["sources"].append("cost66i raw batch4 bit 34 (canon-equal to 72d bit 103)")
xscan["agreements"]["72d bit 103 = 66i bit 34"] = {
    "verdict": "REFUTED-D10 both", "nodes_66i": r66i["nodes"],
    "nodes_72d": bits[103]["nodes"]}
# 66j bit 86 (cost72d bit 108)
r66j, c66j = find_raw_record(
    "class2-lane-cost66j-raw-batch6-20261117.jsonl", 86,
    "00000000000000c09002000000001000")
assert r66j["loss"] is False and c66j == canon_of[108]
xscan["sources"].append("cost66j raw batch6 bit 86 (canon-equal to 72d bit 108)")
xscan["agreements"]["72d bit 108 = 66j bit 86"] = {
    "verdict": "REFUTED-D10 both", "nodes_66j": r66j["nodes"],
    "nodes_72d": bits[108]["nodes"]}
# pre-64h harvest: 69c sweep JSON is the recorded harvest source of bit 115
d69c = json.loads((OUT / "class2-lane-cost69c-sweep-20261114.json").read_bytes())
child69c = d69c["s6_child_hex"]
cand69c = sorted(legal_candidates(child69c)[1])
win69c = set(d69c["win7_bits"])
assert d69c["capped"] == 0 and len(cand69c) == 69
# find the 69c bit whose canon equals canon_of[115]
hit_bit = None
for b_ in cand69c:
    if canon(int(child69c, 16) | (1 << b_)) == canon_of[115]:
        assert hit_bit is None
        hit_bit = b_
assert hit_bit is not None and hit_bit not in win69c
xscan["sources"].append(
    f"cost69c sweep JSON bit {hit_bit} (canon-equal to 72d bit 115; the "
    "pre-64h harvest source recorded by the census v5 overlay)")
xscan["agreements"][f"72d bit 115 = 69c bit {hit_bit}"] = {
    "verdict": "REFUTED-D10 both",
    "nodes_72d": bits[115]["nodes"]}
assert xscan["conflicts"] == 0

# ------------------------------------------------ 4. determinism + v15
def load_recs(p):
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


det = {}
for name, n in (("batch1", 1), ("batch3", 3)):
    orig = load_recs(OUT / f"class2-lane-cost72d-raw-batch{n}-20261117.jsonl")
    rerun = load_recs(OUT / f"class2-lane-cost72d-det-batch{n}-20261117.jsonl")
    assert len(orig) == len(rerun)
    for x, y in zip(orig, rerun):
        for k in set(x) | set(y):
            if k == "ms":
                continue
            assert x.get(k) == y.get(k), (n, k)
    det[name] = "field-identical on every non-ms field"

v15 = {}
v15_ctrl = 0
for f in ("class2-lane-cost72d-v15-crosscheck-a-20261117.jsonl",
          "class2-lane-cost72d-v15-crosscheck-b-20261117.jsonl"):
    for r in load_recs(OUT / f):
        if "control" in r:
            v15_ctrl += 1
            assert r == {"control": "pilot_d6", "loss": False,
                         "nodes": 5949, "capped": False}, r
        else:
            assert r["bit"] not in v15
            v15[r["bit"]] = r
assert v15_ctrl == 2 and sorted(v15) == wins
for b_ in wins:
    assert v15[b_]["loss"] is True and v15[b_]["capped"] is False
    assert bits[b_]["loss"] is True and bits[b_]["capped"] is False

# ------------------------------------------------------------- 5. output
audit = {
    "schema": "n11-class2-lane-cost72d-raw-sweep-audit-20261117-v1",
    "date": "2026-11-17",
    "status": ("all checks passed; 11 WIN7-D10 + 61 REFUTED-D10, 0 capped; "
               "5/5 confirmation transfers REFUTED-D10 as predicted by the "
               "census v5 overlay; 11/11 v15 WIN agreement; 9/9 pilot "
               "controls exact; 11x11 UNKNOWN"),
    "target": {
        "s5": "00000000000000403800000008000000",
        "s6_child": CHILD,
        "legal_candidate_count": 72,
        "canonical_head_at_sweep": "1472/174/6376/504672/4649/368586",
        "selection": ("head-1472 presweep census v5 runner-up "
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
        "refuted_d10_bits_count": len(refuted),
        "capped_count": 0,
        "candidate_nodes_total": total_nodes,
        "total_nodes_including_pilots": total_nodes + 9 * 3402,
        "terminal_stone_range": [13, 17],
    },
    "confirmation_bits": {
        "bits": CONFIRM,
        "verdicts": {str(b): "REFUTED-D10" for b in CONFIRM},
        "predicted_by_census_v5_overlay": True,
        "outcome": transfer_outcome,
    },
    "determinism_rerun": {
        "batches": [1, 3],
        "batch1_note": "contains WIN bits 1 and 6",
        "batch3_note": "contains the heaviest bit 41 (4,501,083 nodes)",
        "field_identical_non_ms": True,
    },
    "v15_cross_engine_check": {
        "engine": "v15 (blob 8744fc65b6b7cac6bd561403ce4c749e01c51359)",
        "pilot_nodes_each": 5949,
        "win_bit_agreement": "11/11",
        "capped": 0,
        "v15_win_nodes": {str(b): v15[b]["nodes"] for b in wins},
    },
    "canon_checks": {
        "child_stones_bit_indices":
            [p for p in range(121) if child_v >> p & 1],
        "transfer_canons_match_claim": "5/5",
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
        "76c/66i/66j/69j/71e folds; the 11x11 empty board, the two-stone "
        "roots {49,60} and {59,60}, S2 {59,60} and classes 1/2/4 "
        "remain UNKNOWN"),
}

out = OUT / "class2-lane-cost72d-raw-sweep-audit-20261117.json"
payload = json.dumps(audit, indent=1, ensure_ascii=True) + "\n"
out.write_bytes(payload.encode())
print(f"wrote {out} ({out.stat().st_size} bytes)")
print("win bits:", wins)
print("total nodes:", total_nodes)
print("69c canon-equal bit:", hit_bit)
