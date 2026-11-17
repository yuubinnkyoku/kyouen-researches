#!/usr/bin/env python3
"""Audit the cost73j raw sweep batches (stdlib only, bookkeeping).

Adapted from audit_cost73i_raw_batches_20261117.py (same design, paths and
constants changed for the cost-73 row 00000000000000403800000408000000, the
census v6 rank-1 selected target): reads the 9 raw batch files (batches 1-8
sweep + batch 9 confirmation), the determinism rerun files (batches 1 and 6),
the v15 cross-check files (a/b), the published source raw records for the
7 confirmation transfers (69j/72d/64h/73i/71e/66i/66j, every source file
pin-verified against its published audit JSON or the pinned census v4 script),
and the published cost73j claim v1 from output/; asserts every check;
writes output/class2-lane-cost73j-raw-sweep-audit-20261117.json.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from legal_candidates import legal_candidates  # noqa: E402

CHILD = "00000000000000403800000408000000"
CLAIM_V1_BLOB = "d52005e662d39779d34ee5b1ae59f25a57f545a9"
CLAIM_V1_COMMIT = "460fbfc0"
WINS_EXPECTED = [0, 1, 6, 29, 44, 49, 52, 69, 74, 82, 87, 91, 98, 100, 110, 118]
DET_BATCHES = (1, 6)

# published pins of the source records used by the cross-source scan
AUD69J_BLOB = "2f6bba29ee388bdf1211400ce5599f0ba24d03e1"  # v6 script pin
AUD71E_BLOB = "9f56bdb74a71ef5a647432409ffd76928702870a"  # v6 script pin
AUD72D_BLOB = "6247569a7dca86053943701a3ae099e704e0cb31"  # v6 script pin
AUD73I_BLOB = "33c8c6bb2b81301354e8b796f5a4751fb52aba3b"  # v6 script pin
AUD66I_BLOB = "f7d8bad610fe07fee6b365e711838600722737e2"  # v4 script pin
AUD66J_BLOB = "6862eb2db71e087d7c17fec3a157eafc17bf46d3"  # v4 script pin
PIN64H_B2 = "04e59e2ed62ba2306c80743e9c0517a6d89e70a2"    # v4 script PIN64H[1]
PIN66I_B2 = "540f645f49dc59e5a2226006584e2cad247b0295"    # v4 script PIN66I[1]
V6_SCRIPT_BLOB = "91c89fa459733c6520ed97031e889aa7ec1a3326"
CENSUS_V6_JSON_BLOB = "c45fc0d118b7222f1e0c5d79227adc3f7ab9d1cb"


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
    f = OUT / f"class2-lane-cost73j-raw-batch{suffix}-20261117.jsonl"
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
assert sorted(bits) == cands and len(bits) == 73
assert st == [27, 34, 59, 60, 61, 70], st
wins = sorted(b for b, r in bits.items() if r["loss"] is True)
refuted = sorted(b for b, r in bits.items() if r["loss"] is False)
capped = sorted(b for b, r in bits.items() if r["capped"])
assert not capped
assert len(wins) + len(refuted) == 73
assert wins == WINS_EXPECTED, wins

# --------------------------------------------- 2. claim v1 agreement checks
claim_path = OUT / "class2-lane-cost73j-inflight-20261117.json"
claim = json.loads(claim_path.read_bytes())
assert git_blob_sha(claim_path.read_bytes()) == CLAIM_V1_BLOB
assert claim["s6_child"] == CHILD
assert claim["engine_candidate_bits"]["open_bit_count"] == 66
CONFIRM = [5, 14, 20, 46, 97, 103, 108]
assert claim["engine_candidate_bits"]["confirmation_bits"] == CONFIRM
assert sorted(claim["engine_candidate_bits"]["open_bits"]) == \
    sorted(set(cands) - set(CONFIRM))
assert claim["engine_candidate_bits"]["open_bit_count"] == \
    len(claim["engine_candidate_bits"]["open_bits"]) == 66
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
# no WIN bit canon-collides with a REFUTED bit of this child (verdict sanity)
for w in wins:
    for b_ in refuted:
        assert canon_of[w] != canon_of[b_], (w, b_)
# transfer canon match (7/7) + predicted verdicts + actual agreement
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

# published audit JSONs used for pins (themselves pin-verified)
aud69j_path = OUT / "class2-lane-cost69j-raw-audit-20261117.json"
aud71e_path = OUT / "class2-lane-cost71e-raw-sweep-audit-20261117.json"
aud72d_path = OUT / "class2-lane-cost72d-raw-sweep-audit-20261117.json"
aud73i_path = OUT / "class2-lane-cost73i-raw-sweep-audit-20261117.json"
aud66i_path = OUT / "class2-lane-cost66i-raw-audit-20261116.json"
aud66j_path = OUT / "class2-lane-cost66j-raw-audit-20261117.json"
for p, want in ((aud69j_path, AUD69J_BLOB), (aud71e_path, AUD71E_BLOB),
                (aud72d_path, AUD72D_BLOB), (aud73i_path, AUD73I_BLOB),
                (aud66i_path, AUD66I_BLOB), (aud66j_path, AUD66J_BLOB)):
    got = git_blob_sha(p.read_bytes())
    assert got == want, (p.name, got, want)
xscan["source_audit_json_pins_verified"] = 6


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
    raw_v = int(want_child, 16) | (1 << want_bit)
    return hit, canon(raw_v), raw_v


TRANSFERS = [
    # (73j confirm bit, source file, source bit, source child, pin getter)
    (5, "class2-lane-cost69j-raw-batch2-20261117.jsonl", 34,
     "00000000000000403800000008000020",
     lambda: json.loads(aud69j_path.read_bytes())
     ["raw_batch_pins"]["batch2"], "cost69j raw audit batch2 pin"),
    (14, "class2-lane-cost72d-raw-batch3-20261117.jsonl", 34,
     "00000000000000403800000008004000",
     lambda: json.loads(aud72d_path.read_bytes())
     ["raw_batch_pins"]["batch3"], "cost72d raw sweep audit batch3 pin"),
    (20, "class2-lane-cost64h-raw-batch2-20261116.jsonl", 34,
     "00000000000000403800000008100000",
     lambda: PIN64H_B2, "census v4 script PIN64H[1]"),
    (46, "class2-lane-cost73i-raw-batch3-20261117.jsonl", 34,
     "00000000000000403800400008000000",
     lambda: json.loads(aud73i_path.read_bytes())
     ["raw_batch_pins"]["batch3"], "cost73i raw sweep audit batch3 pin"),
    (97, "class2-lane-cost71e-raw-batch7-20261117.jsonl", 106,
     "00000000000000c09002000000002000",
     lambda: json.loads(aud71e_path.read_bytes())
     ["raw_batch_pins"]["batch7"], "cost71e raw sweep audit batch7 pin"),
    (103, "class2-lane-cost66i-raw-batch2-20261116.jsonl", 14,
     "00000000000000801226000000000000",
     lambda: PIN66I_B2, "census v4 script PIN66I[1]"),
    (108, "class2-lane-cost66j-raw-batch7-20261117.jsonl", 106,
     "00000000000000c09002000000001000",
     lambda: json.loads(aud66j_path.read_bytes())
     ["raw_batch_pins"]["batch7"], "cost66j raw audit batch7 pin"),
]
for b_, fname, s_bit, s_child, pin_getter, pin_note in TRANSFERS:
    rec, c, raw_v = find_raw_record(fname, s_bit, s_child)
    pin = pin_getter()
    got_pin = git_blob_sha((OUT / fname).read_bytes())
    assert got_pin == pin, (fname, got_pin, pin)
    assert rec["loss"] is False and rec["capped"] is False, rec
    assert c == canon_of[b_], (b_, fname)
    raw_equal = raw_v == (child_v | (1 << b_))
    xscan["sources"].append(
        f"{fname} bit {s_bit} (canon-equal to 73j bit {b_}; "
        f"{'raw-identical' if raw_equal else 'canon-equal only'}; "
        f"source pin verified via {pin_note})")
    xscan["agreements"][f"73j bit {b_} = {fname.split('-')[2]} bit {s_bit}"] = {
        "verdict": "REFUTED-D10 both",
        "raw_identical": raw_equal,
        "nodes_source": rec["nodes"],
        "nodes_73j": bits[b_]["nodes"],
        "nodes_equal": rec["nodes"] == bits[b_]["nodes"],
    }
assert xscan["conflicts"] == 0
# recompute raw-identical count cleanly
raw_identical_count = 0
for b_, fname, s_bit, s_child, _pg, _pn in TRANSFERS:
    key = f"73j bit {b_} = {fname.split('-')[2]} bit {s_bit}"
    if xscan["agreements"][key]["raw_identical"]:
        raw_identical_count += 1
assert raw_identical_count == 4, raw_identical_count
# the 4 raw-identical sources must also give identical node counts
for b_, fname, s_bit, s_child, _pg, _pn in TRANSFERS:
    key = f"73j bit {b_} = {fname.split('-')[2]} bit {s_bit}"
    if xscan["agreements"][key]["raw_identical"]:
        assert xscan["agreements"][key]["nodes_equal"]

# ------------------------------------------------ 4. determinism + v15
def load_recs(p):
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


det = {}
for n in DET_BATCHES:
    orig = load_recs(OUT / f"class2-lane-cost73j-raw-batch{n}-20261117.jsonl")
    rerun = load_recs(OUT / f"class2-lane-cost73j-det-batch{n}-20261117.jsonl")
    assert len(orig) == len(rerun)
    for x, y in zip(orig, rerun):
        for k in set(x) | set(y):
            if k == "ms":
                continue
            assert x.get(k) == y.get(k), (n, k)
    det[f"batch{n}"] = "field-identical on every non-ms field"

v15 = {}
v15_ctrl = 0
for f in ("class2-lane-cost73j-v15-crosscheck-a-20261117.jsonl",
          "class2-lane-cost73j-v15-crosscheck-b-20261117.jsonl"):
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
    "schema": "n11-class2-lane-cost73j-raw-sweep-audit-20261117-v1",
    "date": "2026-11-17",
    "status": ("all checks passed; 16 WIN7-D10 + 57 REFUTED-D10, 0 capped; "
               "7/7 confirmation transfers REFUTED-D10 as predicted by the "
               "census v6 nine-map overlay (4 raw-identical + 3 canon-equal "
               "sources, all source pins verified); 16/16 v15 WIN agreement; "
               "9/9 pilot controls exact; 11x11 UNKNOWN"),
    "target": {
        "s5": "00000000000000403800000008000000",
        "s6_child": CHILD,
        "legal_candidate_count": 73,
        "canonical_head_at_sweep": "1472/174/6376/504672/4649/368586",
        "selection": ("head-1472 presweep census v6 rank-1 "
                      "(class2-lane-next-target-presweep-1472-v6-"
                      "20261117.json, git blob " + CENSUS_V6_JSON_BLOB +
                      "; script git blob " + V6_SCRIPT_BLOB +
                      "; claim v1 git blob " + CLAIM_V1_BLOB +
                      ", commit " + CLAIM_V1_COMMIT + ")"),
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
        "refuted_d10_bits_count": len(refuted),
        "capped_count": 0,
        "candidate_nodes_total": total_nodes,
        "total_nodes_including_pilots": total_nodes + 9 * 3402,
        "terminal_stone_range": [13, 17],
    },
    "confirmation_bits": {
        "bits": CONFIRM,
        "verdicts": {str(b): "REFUTED-D10" for b in CONFIRM},
        "predicted_by_census_v6_overlay": True,
        "outcome": transfer_outcome,
    },
    "determinism_rerun": {
        "batches": list(DET_BATCHES),
        "batch1_note": ("contains WIN bits 0, 1 and 6 and the heaviest "
                        "search of the sweep (bit 3, 11,476,946 nodes)"),
        "batch6_note": ("contains the heaviest WIN bit 98 (8,801,472 "
                        "nodes) and WIN bit 100"),
        "field_identical_non_ms": True,
        "result": det,
    },
    "v15_cross_engine_check": {
        "engine": "v15 (blob 8744fc65b6b7cac6bd561403ce4c749e01c51359)",
        "pilot_nodes_each": 5949,
        "win_bit_agreement": "16/16",
        "capped": 0,
        "v15_win_nodes": {str(b): v15[b]["nodes"] for b in wins},
    },
    "canon_checks": {
        "child_stones_bit_indices":
            [p for p in range(121) if child_v >> p & 1],
        "child_stones_bit_indices_expected":
            [27, 34, 59, 60, 61, 70],
        "transfer_canons_match_claim": "7/7",
        "internal_canon_collisions": collisions,
        "no_win_refuted_canon_overlap": True,
        "v1_bit_table": ("this child has no v1 head-1452 census bit table "
                         "(not one of the 16 bit-table children; the "
                         "pre-sweep knowledge came from the census v6 "
                         "rebuilt harvest + nine-map overlay; the v1 "
                         "census row was open 73 with 0 harvested)"),
    },
    "cross_source_conflict_scan": xscan,
    "raw_batch_pins": batch_pins,
    "interpretation_guard": (
        "engine bookkeeping audit only; WIN7-D10 proves a first-player "
        "win within depth 10 from the individual 7-stone root only; "
        "REFUTED-D10 is not a LOSS proof; no manifest row is closed by "
        "this audit; the receipt fold stays pending behind the "
        "76c/66i/66j/69j/71e/72d/73i folds; the 11x11 empty board, the "
        "two-stone roots {49,60} and {59,60}, S2 {59,60} and classes "
        "1/2/4 remain UNKNOWN"),
}

out = OUT / "class2-lane-cost73j-raw-sweep-audit-20261117.json"
payload = json.dumps(audit, indent=1, ensure_ascii=True) + "\n"
out.write_bytes(payload.encode())
print(f"wrote {out} ({out.stat().st_size} bytes)")
print("win bits:", wins)
print("total nodes:", total_nodes)
print("raw-identical transfer sources:", raw_identical_count)
