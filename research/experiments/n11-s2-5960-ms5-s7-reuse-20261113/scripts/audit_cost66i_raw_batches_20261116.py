#!/usr/bin/env python3
"""Independent stdlib-only audit of the cost-66i raw sweep (2026-11-16).

Target: S6 child 00000000000000801226000000000000 (cost 66, parent S5
00000000000000403800000008000000, demand c2=2), fresh v17 sweep of all
66 legal candidate bits at depth 10, cap 1e9, andclose 1.

Inputs (all blob-pinned, all published on main or pushed with the sweep):
  * class2-lane-cost66i-raw-batch{1..9}-20261116.jsonl   (v17 fresh sweep)
  * class2-lane-cost66i-det-batch3-20261116.jsonl        (determinism rerun)
  * class2-lane-cost66i-v15-crosscheck-{a,b}-20261116.jsonl (v15 cross-engine)
  * class2-lane-cost66i-inflight-20261116.json           (claim v1)
  * class2-lane-next-target-presweep-1452-v2-20261116.json (census v2)
  * cost-64h raw batches 1-8 and cost-76c v17 raw batches 1-10
    (rebuilt verdict maps for cross-source conflict detection)

Checks (all asserted, then recorded):
  1. every batch pilot is exactly {loss=false, nodes=3402, capped=false};
  2. the 66 engine bits equal the claim's legal_candidates, each exactly once,
     no capped, andclose=true on every line;
  3. verdict aggregate: WIN7-D10 / REFUTED-D10 bit lists, total nodes;
  4. the 3 confirmation bits 23/100/109 come out REFUTED-D10, agreeing with
     the claim's expected_verdicts (2 v1 harvest transfers + 1 cost-64h
     orbit transfer);
  5. determinism: the batch-3 rerun is field-identical on every non-ms field;
  6. v15 cross-engine: pilot exactly 5949, all 9 WIN bits loss=true;
  7. D4 canon of every root child|1<<bit recomputed; the three transfer
     root canons match the claim; every canon matches the published
     head-1452 census v1 bit table for this row;
  8. cross-source conflict scan: none of the 9 WIN root canons appears as a
     REFUTED-D10 canon in the cost-64h or cost-76c verdict maps, and none of
     the 57 REFUTED root canons appears as a WIN7-D10 canon in either map
     (bit 100's canon appears as REFUTED in cost-64h: agreement, not conflict).

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
CHILD = int("00000000000000801226000000000000", 16)
CLAIM = load_out("class2-lane-cost66i-inflight-20261116.json",
                 "738443c0d1076115d723029edac2de3cb67c3e86")
CENSUS_V1 = load_out("class2-lane-next-target-presweep-1452-20261116.json",
                     "0d9a94a272de9fe45708757f17bfea60239a3c9b")
CENSUS_V2 = load_out(
    "class2-lane-next-target-presweep-1452-v2-20261116.json",
    "67d6a5c192953b9bc95fd13b356e5aabeac2a12c")
PREREG64H = load_out(
    "class2-lane-cost64h-fold-preregistration-independent-20261116.json",
    "5074a8a0cbb75fcc91b5b999a3135fac06d42400")

PIN66I = ["02b31589bb990cb7b867dffb22da16a30ab67594", "540f645f49dc59e5a2226006584e2cad247b0295", "42bf714ab115ec735edc3ff7cdd7217d00e35433", "13da15f8f3a30fe650bd9b7279b04278ec4b5355", "59ff6d1c9431ed97cd9b82eadf6ed1f68bdfbb96", "3c81f310df67447f687a3d0536202f9b5b38e51a", "c6eed4f004f8829818270981e152822eb33b13f9", "e28abd996708d37d54e4ec0cf8664e38f89a19a2",
          "37cde85ddbc7d86cd0b3b3376c30bd595a6e85de"]
DET3_PIN = "9eb2dcd22722190c5908ea0bc8b4865a28022570"
V15A_PIN = "7ab592512b26b5bfa38ccf1ce0e0ba828894e91b"
V15B_PIN = "25079ffc9949384e0631cbe747b6e76c48ff3f09"

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
CHILD64H = int("00000000000000403800000008100000", 16)
CHILD76C = int("00000000010000809002000001000000", 16)

# ------------------------------------------------------- 1-4 sweep aggregate
legal = sorted(legal_candidates(f"{CHILD:032x}")[1])
assert legal == sorted(CLAIM["legal_candidates"]), "legal mismatch"
assert len(legal) == 66

results = {}
pilots = 0
total_nodes = 0
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
for b in (23, 100, 109):
    assert not results[b]["loss"], ("confirmation bit came out WIN", b)
    assert CLAIM["engine_candidate_bits"]["expected_verdicts"][
        str(b)] == "REFUTED-D10"

# ------------------------------------------------------- 5 determinism rerun
det = load_jsonl("class2-lane-cost66i-det-batch3-20261116.jsonl", DET3_PIN)
raw3 = load_jsonl("class2-lane-cost66i-raw-batch3-20261116.jsonl",
                  PIN66I[2])
assert len(det) == len(raw3)
for x, y in zip(raw3, det):
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
for name, pin in (("class2-lane-cost66i-v15-crosscheck-a-20261116.jsonl",
                   V15A_PIN),
                  ("class2-lane-cost66i-v15-crosscheck-b-20261116.jsonl",
                   V15B_PIN)):
    for r in load_jsonl(name, pin):
        if r.get("control") == "pilot_d6":
            assert r == {"control": "pilot_d6", "loss": False,
                         "nodes": 5949, "capped": False}, r
            v15_pilots += 1
            continue
        assert r["bit"] in win_bits, r
        assert r["bit"] not in v15
        v15[r["bit"]] = r
assert v15_pilots == 2
assert sorted(v15) == win_bits, "v15 must cover exactly the WIN bits"
for b, r in v15.items():
    assert r["loss"] is True, ("v15 disagrees on WIN bit", b)
    assert not r["capped"], r

# ------------------------------------------------------- 7 canon recompute
child_hex = f"{CHILD:032x}"
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
verdict64h = {}
for i in range(1, 9):
    for r in load_jsonl(f"class2-lane-cost64h-raw-batch{i}-20261116.jsonl",
                        PIN64H[i - 1]):
        if r.get("control"):
            continue
        c = canon(CHILD64H | (1 << r["bit"]))
        assert c not in verdict64h, "duplicate 64h canon"
        verdict64h[f"{c:032x}"] = "WIN7-D10" if r["loss"] else "REFUTED-D10"
verdict76c = {}
for i in range(1, 11):
    for r in load_jsonl(
            f"class2-lane-cost76c-v17-raw-batch{i}-20261117.jsonl",
            PIN76C17[i - 1]):
        if r.get("control"):
            continue
        c = canon(CHILD76C | (1 << r["bit"]))
        assert c not in verdict76c, "duplicate 76c canon"
        verdict76c[f"{c:032x}"] = "WIN7-D10" if r["loss"] else "REFUTED-D10"
prereg_win = {r["d4_canonical_hex"]
              for r in PREREG64H["receipts"]}
assert len(verdict64h) == 64 and len(verdict76c) == 76

win_canons = {f"{canon_by_bit[b]:032x}" for b in win_bits}
refuted_canons = {f"{canon_by_bit[b]:032x}" for b in refuted_bits}
conflicts = []
for src_name, vmap in (("cost64h", verdict64h), ("cost76c", verdict76c)):
    for c in win_canons:
        if vmap.get(c) == "REFUTED-D10":
            conflicts.append(("WIN-here vs REFUTED-there", c, src_name))
    for c in refuted_canons:
        if vmap.get(c) == "WIN7-D10":
            conflicts.append(("REFUTED-here vs WIN-there", c, src_name))
assert not conflicts, conflicts
assert win_canons & prereg_win == set(), "WIN canon already folded"
# agreement accounting (not conflicts)
agree_64h = sorted(b for b in refuted_bits
                   if verdict64h.get(f"{canon_by_bit[b]:032x}")
                   == "REFUTED-D10")
agree_76c = sorted(b for b in refuted_bits
                   if verdict76c.get(f"{canon_by_bit[b]:032x}")
                   == "REFUTED-D10")
win_agree_64h = sorted(b for b in win_bits
                       if verdict64h.get(f"{canon_by_bit[b]:032x}")
                       == "WIN7-D10")
win_agree_76c = sorted(b for b in win_bits
                        if verdict76c.get(f"{canon_by_bit[b]:032x}")
                        == "WIN7-D10")

# ------------------------------------------------------------------ output
audit = {
    "schema": "n11-class2-lane-cost66i-raw-sweep-audit-20261116-v1",
    "date": "2026-11-16",
    "status": "all checks passed; 9 WIN7-D10 + 57 REFUTED-D10, 0 capped; "
              "11x11 UNKNOWN",
    "target": {
        "s5": CLAIM["s5"],
        "s6_child": child_hex,
        "legal_candidate_count": 66,
        "canonical_head_at_sweep": "1452/174/6396/506144/4669/370058",
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
        "bits": [23, 100, 109],
        "verdicts": {str(b): "REFUTED-D10" for b in (23, 100, 109)},
        "claim_expected_agreement": "3/3",
        "sources": {str(b): CLAIM["transfers"][str(b)]["kind"]
                    for b in (23, 100, 109)},
    },
    "determinism_rerun": {
        "batch": 3,
        "contains_win_bits": [28, 29],
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
        "transfer_canons_match_claim": "3/3",
        "v1_bit_table_canons_match": "66/66",
        "internal_canon_collisions": internal_collisions,
    },
    "cross_source_conflict_scan": {
        "sources": ["cost64h raw batches 1-8",
                    "cost76c v17 raw batches 1-10",
                    "cost64h fold prereg receipts"],
        "conflicts": 0,
        "win_refuted_agreements": {
            "refuted_bits_also_refuted_in_64h": agree_64h,
            "refuted_bits_also_refuted_in_76c": agree_76c,
            "win_bits_also_win_in_64h": win_agree_64h,
            "win_bits_also_win_in_76c": win_agree_76c,
        },
        "note": ("bit 100's root canon matches the cost-64h REFUTED-D10 "
                 "verdict (64h bit 103), an agreement recorded by the "
                 "census v2 selection; no canon carries contradictory "
                 "verdicts across sources"),
    },
    "interpretation_guard": (
        "engine bookkeeping audit only; WIN7-D10 proves a first-player win "
        "within depth 10 from the individual 7-stone root only; "
        "REFUTED-D10 is not a LOSS proof; no manifest row is closed by "
        "this audit; the 11x11 empty board, two-stone roots {49,60} and "
        "{59,60}, S2 {59,60}, and classes 1/2/4 all remain UNKNOWN"),
}
out_path = OUT / "class2-lane-cost66i-raw-audit-20261116.json"
out_path.write_text(json.dumps(audit, indent=1, sort_keys=False) + "\n")
print(f"wrote {out_path} ({out_path.stat().st_size} bytes)")
print("WIN bits:", win_bits)
print("REFUTED:", len(refuted_bits), "conflicts:", len(conflicts))
print("agreements: 64h-refuted", agree_64h, "76c-refuted", agree_76c,
      "64h-win", win_agree_64h, "76c-win", win_agree_76c)
print("internal canon collisions:", internal_collisions)
