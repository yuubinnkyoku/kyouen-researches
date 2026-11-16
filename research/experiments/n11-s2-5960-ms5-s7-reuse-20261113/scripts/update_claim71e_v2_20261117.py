#!/usr/bin/env python3
"""Update the cost71e claim from v1 to v2 (sweep complete, bookkeeping).

Reads output/class2-lane-cost71e-inflight-20261117.json (must still be
the published claim v1, git blob f6439474...), the raw sweep batches,
the determinism reruns, the v15 cross-check files and the raw audit
JSON; asserts consistency; rewrites the claim in place as schema v2.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
sys.path.insert(0, str(HERE / "scripts"))
from legal_candidates import legal_candidates  # noqa: E402

CLAIM_V1_BLOB = "f64394741142258206149e652f68e2af558b1cff"
CHILD = "00000000000000c09002000000002000"


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


claim_path = OUT / "class2-lane-cost71e-inflight-20261117.json"
b = claim_path.read_bytes()
assert git_blob_sha(b) == CLAIM_V1_BLOB
claim = json.loads(b)

# ---- erratum: the v1 legal_candidates field is defective ---------------
cands_true = sorted(legal_candidates(CHILD)[1])
assert len(cands_true) == 71
assert sorted(set(cands_true) - {20, 67, 97}) == \
    sorted(claim["engine_candidate_bits"]["open_bits"])
assert sorted(cands_true) == sorted(
    claim["engine_candidate_bits"]["open_bits"] + [20, 67, 97])
assert claim["candidate_count"] == 71
assert len(claim["legal_candidates"]) == 78
assert claim["legal_candidates"] != cands_true
c78a = json.loads((OUT / "class2-lane-cost78a-inflight-20261115.json")
                  .read_bytes())
assert claim["legal_candidates"] == c78a["legal_candidates"]

# aggregate the raw batches
bits = {}
controls = 0
total_nodes = 0
batch_pins = {}
for n in range(1, 10):
    f = OUT / f"class2-lane-cost71e-raw-batch{n}-20261117.jsonl"
    batch_pins[f"batch{n}"] = git_blob_sha(f.read_bytes())
    for line in f.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if "control" in r:
            controls += 1
            assert r == {"control": "pilot_d6", "loss": False,
                         "nodes": 3402, "capped": False}
        else:
            assert r["bit"] not in bits
            bits[r["bit"]] = r
            total_nodes += r["nodes"]
assert controls == 9 and len(bits) == 71
wins = sorted(x for x, r in bits.items() if r["loss"] is True)
refuted = sorted(x for x, r in bits.items() if r["loss"] is False)
capped = sorted(x for x, r in bits.items() if r["capped"])
assert not capped
assert len(wins) == 13 and len(refuted) == 58
assert wins == [3, 4, 8, 41, 54, 58, 76, 79, 94, 96, 100, 116, 119]
for x in (20, 67, 97):
    assert bits[x]["loss"] is False

audit = json.loads((OUT / "class2-lane-cost71e-raw-sweep-audit-"
                           "20261117.json").read_bytes())
assert audit["verdicts"]["win7_d10_bits"] == wins
assert audit["verdicts"]["candidate_nodes_total"] == total_nodes

det_pins = {}
for n in (1, 6):
    f = OUT / f"class2-lane-cost71e-det-batch{n}-20261117.jsonl"
    det_pins[f"det_batch{n}"] = git_blob_sha(f.read_bytes())
v15_pins = {}
for s in ("a", "b", "c"):
    f = OUT / f"class2-lane-cost71e-v15-crosscheck-{s}-20261117.jsonl"
    v15_pins[f"v15_crosscheck_{s}"] = git_blob_sha(f.read_bytes())

claim["schema"] = "n11-class2-lane-cost71e-inflight-20261117-v2"
claim["status"] = (
    "claim v2: sweep complete; all 71 legal bits freshly run (8 sweep "
    "batches + 1 confirmation batch, v17, depth 10, cap 1e9, andclose 1, "
    "0 capped); 13 WIN7-D10 bits [3,4,8,41,54,58,76,79,94,96,100,116,119] "
    "+ 58 REFUTED-D10; the 3 confirmation transfers came out REFUTED-D10 "
    "as predicted by the census v5 overlay (3/3, incl. bit 20 = 64h bit "
    "97, bit 67 = 66i bit 107, bit 97 = pre-64h harvest via cost64d bit "
    "97 canon equivalence); determinism rerun batches 1 and 6 "
    "field-identical on every non-ms field; independent v15 cross-engine "
    "check 13/13 WIN agreement (pilot 5949 exact); stdlib raw audit v1 "
    "all checks passed; erratum: the v1 legal_candidates field was a "
    "cost78a template carry-over (78 bits, wrong child), corrected here "
    "to the recomputed 71-bit list (sweep bits, counts and verdicts "
    "unaffected); receipt fold pending behind the 76c/66i/66j/69j "
    "folds; 11x11 UNKNOWN")
claim["actual_execution"] = {
    "started": "2026-11-17",
    "engine": ("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
               "scripts/class4_child1_runner_v17.ts (v17, blob "
               "c132cc6425eee3feaeef1d697dd74f968cfedb59)"),
    "batches_run": 9,
    "pilot_controls": ("9/9 batches: pilot_d6 exact {loss=false, "
                       "nodes=3402, capped=false}"),
    "results": {
        "win7_d10_bits": wins,
        "win7_d10_nodes": {str(x): bits[x]["nodes"] for x in wins},
        "refuted_d10_bits_count": 58,
        "capped_count": 0,
        "candidate_nodes_total": total_nodes,
        "total_nodes_including_pilots": total_nodes + 9 * 3402,
        "terminal_stone_range": [13, 17],
    },
    "confirmation_outcome": (
        "3/3 REFUTED-D10 as predicted by the census v5 overlay "
        "(bit 20 = cost64h bit 97, bit 67 = cost66i bit 107, "
        "bit 97 = pre-64h harvest via cost64d bit 97 canon equivalence)"),
    "determinism_rerun": (
        "batches 1 (WIN bits 3/4/8) and 6 (heaviest bit 88, 9,928,319 "
        "nodes) re-run in separate processes: field-identical on every "
        "non-ms field"),
    "v15_crosscheck": (
        "independent v15 engine (blob "
        "8744fc65b6b7cac6bd561403ce4c749e01c51359) re-check of all 13 "
        "WIN bits: 13/13 loss=true, pilot 5949 exact, 0 capped"),
    "raw_outputs": {
        "raw_batch_pattern":
            "class2-lane-cost71e-raw-batch{n}-20261117.jsonl",
        "raw_batch_blob_pins": batch_pins,
        "determinism_rerun_blob_pins": det_pins,
        "v15_crosscheck_blob_pins": v15_pins,
        "raw_audit_json": (
            "class2-lane-cost71e-raw-sweep-audit-20261117.json (git blob "
            + git_blob_sha((OUT / "class2-lane-cost71e-raw-sweep-audit-"
                                   "20261117.json").read_bytes()) + ")"),
    },
}
claim["legal_candidates"] = cands_true
claim["erratum_v1_legal_candidates"] = {
    "defect": ("the claim v1 legal_candidates field erroneously contained "
               "the 78-bit candidate list of the cost78a child "
               "(class2-lane-cost78a-inflight-20261115.json, child "
               "00000000000000809102000000400000): a template copy-paste "
               "error in the claim generator"),
    "unaffected": ("candidate_count (71), engine_candidate_bits (68 open "
                   "+ 3 confirmation), child_stones_bit_indices, transfers "
                   "and every executed bit are correct: the raw sweep "
                   "bits equal the freshly recomputed legal candidates of "
                   "the cost71e child, and the published stdlib audit "
                   "recomputes legal_candidates itself and passed all "
                   "checks"),
    "correction": ("v2 replaces the field with the recomputed 71-bit "
                   "list of the cost71e child; claim v1 git blob "
                   "f64394741142258206149e652f68e2af558b1cff carries the "
                   "defect; no verdict, count or executed bit changes"),
}
claim["next_action"] = (
    "extract the 13 WIN7-D10 certificates (cert driver duplicated from "
    "cert_driver69j for cost71e, root defenses via legal_candidates), "
    "verify them independently (root-check stones=7 + loserMobility, "
    "sub-root union, fbt_drops), publish the certificate manifest and "
    "claim v3; the receipt fold stays pending behind the 76c/66i/66j/"
    "69j folds")

payload = json.dumps(claim, indent=1, ensure_ascii=True) + "\n"
claim_path.write_bytes(payload.encode())
print(f"wrote {claim_path} ({claim_path.stat().st_size} bytes)")
print("claim v2 blob:", git_blob_sha(payload.encode()))
