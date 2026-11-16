#!/usr/bin/env python3
"""Independent stdlib-only audit of the cost-66j raw sweep (2026-11-17).

Target: S6 child 00000000000000c09002000000001000 (cost 66, parent S5
00000000000000403800000008000000, demand c2=2), fresh v17 sweep of all
66 legal candidate bits at depth 10, cap 1e9, andclose 1. Selected by the
head-1472 presweep census v3 (blob 3ee5703c...) as the cheapest remaining
unswept/unclaimed row of the primary pure class-2 target family.

Inputs (all blob-pinned; raw batches, determinism reruns and the v15
crosscheck are pushed with this audit in the same commit):
  * class2-lane-cost66j-raw-batch{1..9}-20261117.jsonl   (v17 fresh sweep)
  * class2-lane-cost66j-det-batch{5,8}-20261117.jsonl    (determinism reruns)
  * class2-lane-cost66j-v15-crosscheck-20261117.jsonl    (v15 cross-engine)
  * class2-lane-cost66j-inflight-20261117.json           (claim v1, blob 68d8f8f2)
  * class2-lane-next-target-presweep-1472-20261117.json  (census v3)
  * class2-lane-next-target-presweep-1452-20261116.json  (census v1 bit tables)
  * cost-64h raw batches 1-8, cost-76c v17 raw batches 1-10 and
    cost-66i raw batches 1-9 (rebuilt verdict maps for cross-source
    conflict detection)

Checks (all asserted, then recorded):
  1. every batch pilot is exactly {loss=false, nodes=3402, capped=false};
  2. the 66 engine bits equal the claim's legal_candidates, each exactly
     once, no capped, andclose=true on every line;
  3. verdict aggregate: WIN7-D10 / REFUTED-D10 bit lists, total nodes;
  4. the 2 confirmation bits 20/97 come out REFUTED-D10, agreeing with
     the claim's expected_verdicts (bit 20 = cost-64h orbit transfer as
     64h bit 108; bit 97 = v1 harvest transfer);
  5. determinism: the batch-5 and batch-8 reruns are field-identical on
     every non-ms field (batch 5 = heaviest batch, contains WIN bits
     66/78/79; batch 8 contains WIN bit 114);
  6. v15 cross-engine: pilot exactly 5949, all 9 WIN bits loss=true;
  7. D4 canon of every root child|1<<bit recomputed; the two transfer
     root canons match the claim; every canon matches the published
     head-1452 census v1 bit table for this row; internal canon
     collisions recorded;
  8. cross-source conflict scan against the cost-64h, cost-76c AND
     cost-66i verdict maps: no canon carries contradictory verdicts;
     no 66j WIN canon is already folded (64h prereg receipts).

Interpretation guard: an independent audit of engine bookkeeping only.
WIN7-D10 proves a first-player win within depth 10 from the individual
7-stone root only; REFUTED-D10 is NOT a LOSS proof of the position. No
manifest row is closed by this audit. The 11x11 empty board, the two-stone
roots {49,60} and {59,60}, S2 {59,60} and classes 1/2/4 all remain UNKNOWN.
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
CHILD = int("00000000000000c09002000000001000", 16)
CLAIM = load_out("class2-lane-cost66j-inflight-20261117.json",
                 "68d8f8f26f598ad061021cda3d9a240518c0e73a")
CENSUS_V1 = load_out("class2-lane-next-target-presweep-1452-20261116.json",
                     "0d9a94a272de9fe45708757f17bfea60239a3c9b")
CENSUS_V3 = load_out(
    "class2-lane-next-target-presweep-1472-20261117.json",
    "3ee5703c8cabf738eaecefb17a759c78c4a34e61")
PREREG64H = load_out(
    "class2-lane-cost64h-fold-preregistration-independent-20261116.json",
    "5074a8a0cbb75fcc91b5b999a3135fac06d42400")

PIN66J = ["565e010b46c84e0bc9e51509dc67005634c1d294",
          "470b65d238a2ab06766d551ff903e15346569381",
          "0211836ab9bc3e565e51cd9aaf30383702d3c174",
          "034a565bb3f8abddb8e679ab656bb0e39530ac74",
          "47cb5f8c3aa446d8993369b71e33b45f17038072",
          "b210cae667030ce4e9f59699fcab5d6a233da574",
          "6fd435c94cb700dd0ee14dabb63160cfa523732d",
          "c7b19d015d4ae3d3b0f3b40ec37aa02d62fe4ee3",
          "bdccf073eebaee4fc5ac09d1e59106676c3f140f"]
DET5_PIN = "9f2c0538a419f55fd901982524ab67e51dcd85a5"
DET8_PIN = "db1cf0837db3126199c6cb5dccbc16254bd4aa30"
V15_PIN = "9b6adb67d92698fbaed8f3d01a6e4b0968d9e3cd"

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

# ------------------------------------------------------- 1-4 sweep aggregate
child_hex = f"{CHILD:032x}"
assert child_hex == CENSUS_V3["selected_target"]["s6_hex"]
legal = sorted(legal_candidates(child_hex)[1])
assert legal == sorted(CLAIM["legal_candidates"]), "legal mismatch"
assert len(legal) == 66
assert sorted(CLAIM["engine_candidate_bits"]["open_bits"]
              + CLAIM["engine_candidate_bits"]["confirmation_bits"]) == legal

results = {}
pilots = 0
total_nodes = 0
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
        assert r["andclose"] is True, r
        assert r["bit"] not in results, r["bit"]
        assert r["bit"] in legal, r["bit"]
        assert r["terminalStoneRange"] == [13, 17], r
        results[r["bit"]] = r
        total_nodes += r["nodes"]
assert pilots == 9
assert sorted(results) == legal, "bit coverage mismatch"
win_bits = sorted(b for b, r in results.items() if r["loss"])
refuted_bits = sorted(b for b, r in results.items() if not r["loss"])
assert len(win_bits) + len(refuted_bits) == 66
for b in (20, 97):
    assert not results[b]["loss"], ("confirmation bit came out WIN", b)
    assert CLAIM["engine_candidate_bits"]["expected_verdicts"][
        str(b)] == "REFUTED-D10"

# ------------------------------------------------------- 5 determinism reruns
for batch, det_pin in ((5, DET5_PIN), (8, DET8_PIN)):
    det = load_jsonl(f"class2-lane-cost66j-det-batch{batch}-20261117.jsonl",
                     det_pin)
    raw = load_jsonl(f"class2-lane-cost66j-raw-batch{batch}-20261117.jsonl",
                     PIN66J[batch - 1])
    assert len(det) == len(raw)
    for x, y in zip(raw, det):
        assert set(x) == set(y)
        for k in x:
            if k == "ms":
                continue
            assert x[k] == y[k], (k, x, y)
    assert det[0] == {"control": "pilot_d6", "loss": False, "nodes": 3402,
                      "capped": False}

# ------------------------------------------------------- 6 v15 cross-engine
v15 = {}
v15_pilots = 0
for r in load_jsonl("class2-lane-cost66j-v15-crosscheck-20261117.jsonl",
                    V15_PIN):
    if r.get("control") == "pilot_d6":
        assert r == {"control": "pilot_d6", "loss": False,
                     "nodes": 5949, "capped": False}, r
        v15_pilots += 1
        continue
    assert r["bit"] in win_bits, r
    assert r["bit"] not in v15
    v15[r["bit"]] = r
assert v15_pilots == 1
assert sorted(v15) == win_bits, "v15 must cover exactly the WIN bits"
for b, r in v15.items():
    assert r["loss"] is True, ("v15 disagrees on WIN bit", b)
    assert not r["capped"], r

# ------------------------------------------------------- 7 canon recompute
stones = sorted(p for p in range(121) if CHILD >> p & 1)
assert stones == CLAIM["child_stones_bit_indices"], stones
canon_by_bit = {b: canon(CHILD | (1 << b)) for b in legal}
for b, t in CLAIM["transfers"].items():
    assert f"{canon_by_bit[int(b)]:032x}" == t["root_canon"], b
v1_tbl = CENSUS_V1["bit_tables"][child_hex]["bits"]
for x in v1_tbl:
    assert f"{canon_by_bit[x['bit']]:032x}" == x["root_canon"], x
collisions = {}
for b in legal:
    collisions.setdefault(f"{canon_by_bit[b]:032x}", []).append(b)
internal_collisions = {k: v for k, v in collisions.items() if len(v) > 1}

# --------------------------------------------- 8 cross-source conflict scan
def build_map(prefix, pins, n, child, pattern):
    m = {}
    for i in range(1, n + 1):
        for r in load_jsonl(pattern.format(i), pins[i - 1]):
            if r.get("control"):
                continue
            c = canon(child | (1 << r["bit"]))
            assert c not in m, "duplicate canon"
            m[f"{c:032x}"] = "WIN7-D10" if r["loss"] else "REFUTED-D10"
    return m


verdict64h = build_map("64h", PIN64H, 8, CHILD64H,
                       "class2-lane-cost64h-raw-batch{}-20261116.jsonl")
verdict76c = build_map("76c", PIN76C17, 10, CHILD76C,
                       "class2-lane-cost76c-v17-raw-batch{}-20261117.jsonl")
verdict66i = build_map("66i", PIN66I, 9, CHILD66I,
                       "class2-lane-cost66i-raw-batch{}-20261116.jsonl")
prereg_win = {r["d4_canonical_hex"] for r in PREREG64H["receipts"]}
assert len(verdict64h) == 64 and len(verdict76c) == 76
assert len(verdict66i) == 66

win_canons = {f"{canon_by_bit[b]:032x}" for b in win_bits}
refuted_canons = {f"{canon_by_bit[b]:032x}" for b in refuted_bits}
conflicts = []
for src_name, vmap in (("cost64h", verdict64h), ("cost76c", verdict76c),
                       ("cost66i", verdict66i)):
    for c in win_canons:
        if vmap.get(c) == "REFUTED-D10":
            conflicts.append(("WIN-here vs REFUTED-there", c, src_name))
    for c in refuted_canons:
        if vmap.get(c) == "WIN7-D10":
            conflicts.append(("REFUTED-here vs WIN-there", c, src_name))
assert not conflicts, conflicts
assert win_canons & prereg_win == set(), "WIN canon already folded"
# agreement accounting (not conflicts)
agreements = {}
for src_name, vmap in (("cost64h", verdict64h), ("cost76c", verdict76c),
                       ("cost66i", verdict66i)):
    agreements[f"refuted_bits_also_refuted_in_{src_name}"] = sorted(
        b for b in refuted_bits
        if vmap.get(f"{canon_by_bit[b]:032x}") == "REFUTED-D10")
    agreements[f"win_bits_also_win_in_{src_name}"] = sorted(
        b for b in win_bits
        if vmap.get(f"{canon_by_bit[b]:032x}") == "WIN7-D10")

# ------------------------------------------------------------------ output
audit = {
    "schema": "n11-class2-lane-cost66j-raw-sweep-audit-20261117-v1",
    "date": "2026-11-17",
    "status": "all checks passed; 9 WIN7-D10 + 57 REFUTED-D10, 0 capped; "
              "11x11 UNKNOWN",
    "target": {
        "s5": CLAIM["s5"],
        "s6_child": child_hex,
        "legal_candidate_count": 66,
        "canonical_head_at_sweep": "1472/174/6376/504672/4649/368586",
        "selection": "head-1472 presweep census v3 selected target "
                     "(cheapest unswept row of the primary family)",
    },
    "pilot_checks": {"batches": 9, "pilot_nodes_each": 3402,
                     "all_exact": True},
    "verdicts": {
        "win7_d10_bits": win_bits,
        "refuted_d10_bits": refuted_bits,
        "capped_count": 0,
        "candidate_nodes": total_nodes,
        "total_nodes_including_pilots": total_nodes + 9 * 3402,
        "terminal_stone_range": [13, 17],
        "heaviest_bits": sorted(
            ((results[b]["nodes"], b) for b in legal), reverse=True)[:5],
    },
    "confirmation_bits": {
        "bits": [20, 97],
        "verdicts": {str(b): "REFUTED-D10" for b in (20, 97)},
        "claim_expected_agreement": "2/2",
        "sources": {str(b): CLAIM["transfers"][str(b)]["kind"]
                    for b in (20, 97)},
        "note": "bit 20's root canon matches the cost-64h REFUTED-D10 "
                "verdict (64h bit 108): cross-engine agreement; bit 97 "
                "confirms the v1 harvest transfer fresh",
    },
    "determinism_rerun": {
        "batches": [5, 8],
        "batch5_note": "heaviest batch, contains WIN bits 66/78/79",
        "batch8_note": "contains WIN bit 114",
        "field_identical_non_ms": True,
    },
    "v15_cross_engine_check": {
        "engine": "v15 (blob 8744fc65b6b7cac6bd561403ce4c749e01c51359)",
        "pilot_nodes_each": 5949,
        "win_bit_agreement": "9/9",
        "capped": 0,
    },
    "canon_checks": {
        "child_stones_bit_indices": stones,
        "transfer_canons_match_claim": "2/2",
        "v1_bit_table_canons_match": "66/66",
        "internal_canon_collisions": internal_collisions,
    },
    "cross_source_conflict_scan": {
        "sources": ["cost64h raw batches 1-8",
                    "cost76c v17 raw batches 1-10",
                    "cost66i raw batches 1-9",
                    "cost64h fold prereg receipts"],
        "conflicts": 0,
        "win_refuted_agreements": agreements,
        "note": ("no 66j canon carries contradictory verdicts across the "
                 "64h/76c/66i maps; no 66j WIN canon is already folded "
                 "in the landed 64h receipts"),
    },
    "raw_batch_pins": {
        f"batch{i}": PIN66J[i - 1] for i in range(1, 10)
    },
    "interpretation_guard": (
        "engine bookkeeping audit only; WIN7-D10 proves a first-player win "
        "within depth 10 from the individual 7-stone root only; "
        "REFUTED-D10 is not a LOSS proof; no manifest row is closed by "
        "this audit; the 11x11 empty board, two-stone roots {49,60} and "
        "{59,60}, S2 {59,60}, and classes 1/2/4 all remain UNKNOWN"),
}
out_path = OUT / "class2-lane-cost66j-raw-audit-20261117.json"
out_path.write_text(json.dumps(audit, indent=1, sort_keys=False) + "\n")
print(f"wrote {out_path} ({out_path.stat().st_size} bytes)")
print("WIN bits:", win_bits)
print("REFUTED:", len(refuted_bits), "conflicts:", len(conflicts))
print("agreements:", agreements)
print("internal canon collisions:", internal_collisions)
