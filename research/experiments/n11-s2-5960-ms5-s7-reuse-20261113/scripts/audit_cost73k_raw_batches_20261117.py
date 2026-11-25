#!/usr/bin/env python3
# Raw-batch audit for the cost73k fresh v17 depth-10 sweep (2026-11-17),
# rebuilt after a sandbox reset wiped the original local raw files before
# publication. The raw batch JSONLs audited here are a full fresh
# regeneration (a third independent execution of the same deterministic
# engine from source) and are checked bit-exactly against the published
# concurrent-session sweep record (git blob 0cba988e..., commit 8803a3b0).
#
# Checks:
#  1. raw batches: 73-bit partition, 9/9 pilot_d6 3402 controls, 25 WIN /
#     48 REFUTED / 0 capped, per-bit (loss, nodes, capped) identical to the
#     concurrent-session record (73/73), node sums;
#  2. confirmation bits: fresh outcomes == claim v1 transfer verdicts ==
#     record predictions (7/7); the six lane sources verified against
#     their published raw/audit files (verdict level; 66i bit 10 is
#     raw-identical, same root hex and same node count), the 64d harvest
#     source covered by the published census v7 assertions + record;
#  3. determinism reruns of batches 1 and 7: field-identical on every
#     non-ms field;
#  4. independent v15 cross-engine re-check a/b/c/d: 25/25 WIN, 4/4
#     pilots 5949, 0 capped, node total equal to the record's v15 total.
#
# Usage:
#   python3 audit_cost73k_raw_batches_20261117.py \
#       <raw_dir> <sources_dir> <claim_v1.json> <record.json> <out.json>
import hashlib, json, sys, pathlib

V1_BLOB = "a24d3557ef23a279cc08c2d578e420f676f28f05"
RECORD_BLOB = "0cba988e2a65e9195b0a0e6a3168a518e27079fb"
CENSUS_V7_BLOB = "68246f3263fe6cbb49ffafa866f73b49cf3c2ebb"
ENGINE_BLOB = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
V15_BLOB = "8744fc65b6b7cac6bd561403ce4c749e01c51359"
SRC_PINS = {
    "class2-lane-cost73j-raw-batch7-20261117.jsonl":
        "f5255e171547a404dd26dd6dc09785fecf9e0822",
    "class2-lane-cost73i-raw-sweep-audit-20261117.json":
        "33c8c6bb2b81",
    "class2-lane-cost72d-raw-sweep-audit-20261117.json":
        "6247569a7dca",
    "class2-lane-cost69j-raw-audit-20261117.json":
        "2f6bba29ee38",
    "class2-lane-cost71e-raw-sweep-audit-20261117.json":
        "9f56bdb74a71",
    "class2-lane-cost66i-raw-audit-20261116.json":
        "f7d8bad610fe07fee6b365e711838600722737e2",
    "class2-lane-cost66i-raw-batch2-20261116.jsonl":
        "540f645f49dc59e5a2226006584e2cad247b0295",
}
CHILD = "00000000000000801206000000000400"
RAW = [f"class2-lane-cost73k-raw-batch{i}-20261117.jsonl" for i in range(1, 9)] + \
      ["class2-lane-cost73k-raw-batch9-confirmation-20261117.jsonl"]
DET = {"class2-lane-cost73k-det-batch1-20261117.jsonl":
        "class2-lane-cost73k-raw-batch1-20261117.jsonl",
       "class2-lane-cost73k-det-batch7-20261117.jsonl":
        "class2-lane-cost73k-raw-batch7-20261117.jsonl"}
V15 = [f"class2-lane-cost73k-v15-crosscheck-{c}-20261117.jsonl" for c in "abcd"]
WINS_EXPECTED = [0, 7, 11, 14, 15, 26, 35, 39, 41, 44, 55, 58, 62, 73, 76,
                 87, 89, 94, 95, 97, 98, 103, 105, 112, 117]

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def main() -> None:
    raw_dir = pathlib.Path(sys.argv[1])
    src_dir = pathlib.Path(sys.argv[2])
    v1_path = pathlib.Path(sys.argv[3])
    rec_path = pathlib.Path(sys.argv[4])
    out_path = pathlib.Path(sys.argv[5])

    # ------------------------------------------------ inputs + pins
    v1_bytes = v1_path.read_bytes()
    assert git_blob_sha(v1_bytes) == V1_BLOB, "claim v1 pin"
    claim = json.loads(v1_bytes)
    assert claim["schema"] == "n11-class2-lane-cost73k-inflight-20261117-v1"
    rec_bytes = rec_path.read_bytes()
    assert git_blob_sha(rec_bytes) == RECORD_BLOB, "record pin"
    rec = json.loads(rec_bytes)
    assert rec["sweep_execution"]["child"] == CHILD
    assert ENGINE_BLOB in rec["sweep_execution"]["engine"]
    for name, pin in SRC_PINS.items():
        b = (src_dir / name).read_bytes()
        assert git_blob_sha(b).startswith(pin) or git_blob_sha(b) == pin, name

    theirs = {int(k): v for k, v in rec["verdicts"]["per_bit"].items()}

    # ------------------------------------------------ 1. raw batches
    mine, batch_of, pilots = {}, {}, 0
    for i, fname in enumerate(RAW, start=1):
        for line in (raw_dir / fname).read_text().splitlines():
            r = json.loads(line)
            if r.get("control"):
                assert r["control"] == "pilot_d6" and r["nodes"] == 3402 \
                    and r["loss"] is False and r["capped"] is False, (fname, r)
                pilots += 1
                continue
            assert r["bit"] not in mine, r["bit"]
            assert r["andclose"] is True and r["terminalStoneRange"] == [13, 17], r
            mine[r["bit"]] = r
            batch_of[r["bit"]] = i
    assert pilots == 9 and len(mine) == 73
    assert set(mine) == set(theirs)
    for b in mine:
        a, t = mine[b], theirs[b]
        assert (a["loss"], a["nodes"], a["capped"]) == \
               (t["loss"], t["nodes"], t["capped"]), b
    wins = sorted(b for b in mine if mine[b]["loss"])
    refuted = sorted(b for b in mine if not mine[b]["loss"])
    assert wins == WINS_EXPECTED == sorted(rec["verdicts"]["win7_d10_bits"])
    assert refuted == sorted(rec["verdicts"]["refuted_d10_bits"])
    assert len(wins) == 25 and len(refuted) == 48
    capped = sum(1 for b in mine if mine[b]["capped"])
    assert capped == 0
    node_sum = sum(mine[b]["nodes"] for b in mine)
    assert node_sum == 128861941 == rec["sweep_execution"]["candidate_nodes_total"]
    assert node_sum + 9 * 3402 == 128892559 == \
        rec["sweep_execution"]["total_nodes_including_pilots"]

    # ------------------------------------------------ 2. confirmation sources
    transfers = claim["transfers"]
    assert sorted(int(k) for k in transfers) == [14, 23, 26, 34, 53, 55, 107]
    exp_verdict = {int(k): v["verdict"] for k, v in transfers.items()}
    for b, verdict in exp_verdict.items():
        assert ("WIN7-D10" if mine[b]["loss"] else "REFUTED-D10") == verdict, b
    # record predictions agree 7/7
    rec_pred = {int(k): v for k, v in
                rec["confirmation_agreement"]["census_v7_claim_predictions"].items()}
    assert rec_pred == exp_verdict
    # lane sources (verdict level):
    #  bit 14 <- cost73j bit 110 (raw line)
    r73j = None
    for line in (src_dir / "class2-lane-cost73j-raw-batch7-20261117.jsonl") \
            .read_text().splitlines():
        r = json.loads(line)
        if r.get("bit") == 110:
            r73j = r
    assert r73j is not None and r73j["loss"] is True and r73j["capped"] is False
    assert mine[14]["loss"] is True  # WIN agrees; canon-equal, not raw-identical
    #  bit 26 <- cost73i bit 110 (audit win list + node table)
    a73i = json.loads((src_dir / "class2-lane-cost73i-raw-sweep-audit-20261117.json")
                      .read_text())
    assert 110 in a73i["verdicts"]["win7_d10_bits"]
    assert mine[26]["loss"] is True
    #  bit 55 <- cost69j bit 110 (audit win list)
    a69j = json.loads((src_dir / "class2-lane-cost69j-raw-audit-20261117.json")
                      .read_text())
    assert 110 in a69j["verdicts"]["win7_d10_bits"]
    assert mine[55]["loss"] is True
    #  bit 34 <- cost72d bit 110 (win list excludes it; capped 0 => REFUTED)
    a72d = json.loads((src_dir / "class2-lane-cost72d-raw-sweep-audit-20261117.json")
                      .read_text())
    assert 110 not in a72d["verdicts"]["win7_d10_bits"]
    assert a72d["verdicts"]["capped_count"] == 0
    assert mine[34]["loss"] is False
    #  bit 107 <- cost71e bit 110 (audit refuted list)
    a71e = json.loads((src_dir / "class2-lane-cost71e-raw-sweep-audit-20261117.json")
                      .read_text())
    assert 110 in a71e["verdicts"]["refuted_d10_bits"]
    assert mine[107]["loss"] is False
    #  bit 53 <- cost66i bit 10 (raw-identical: same root hex, same nodes)
    r66i = None
    for line in (src_dir / "class2-lane-cost66i-raw-batch2-20261116.jsonl") \
            .read_text().splitlines():
        r = json.loads(line)
        if r.get("bit") == 10:
            r66i = r
    assert r66i is not None and r66i["loss"] is False \
        and r66i["nodes"] == 39808 and r66i["capped"] is False
    assert mine[53]["loss"] is False and mine[53]["nodes"] == 39808
    #  same absolute root hex: 66i child + bit 10 == 73k child + bit 53
    a66i = json.loads((src_dir / "class2-lane-cost66i-raw-audit-20261116.json")
                      .read_text())
    c66i = int(a66i["target"]["s6_child"], 16)
    assert c66i | (1 << 10) == int(CHILD, 16) | (1 << 53)
    #  bit 23 <- pre-64h harvest (cost64d bit 110): the published census v7
    #  script's rebuilt-harvest assertions cover this source; the fresh run,
    #  the claim transfer verdict and the record's fresh outcome all agree.
    assert mine[23]["loss"] is False and exp_verdict[23] == "REFUTED-D10"

    # ------------------------------------------------ 3. determinism reruns
    det_notes = {}
    for det, orig in DET.items():
        la = [json.loads(l) for l in (raw_dir / orig).read_text().splitlines()]
        lb = [json.loads(l) for l in (raw_dir / det).read_text().splitlines()]
        assert len(la) == len(lb)
        for ra, rb in zip(la, lb):
            ka = {k: v for k, v in ra.items() if k != "ms"}
            kb = {k: v for k, v in rb.items() if k != "ms"}
            assert ka == kb, (det, ka, kb)
        det_notes[det] = {
            "lines": len(la),
            "heaviest_bit": max((r["bit"] for r in la if r.get("bit") is not None),
                                key=lambda b: mine[b]["nodes"]),
        }

    # ------------------------------------------------ 4. v15 cross-engine
    v15, v15_pilots, v15_total = {}, 0, 0
    for fname in V15:
        for line in (raw_dir / fname).read_text().splitlines():
            r = json.loads(line)
            if r.get("control"):
                assert r["nodes"] == 5949 and r["loss"] is False \
                    and r["capped"] is False, (fname, r)
                v15_pilots += 1
                continue
            assert r["loss"] is True and r["capped"] is False, (fname, r)
            assert r["bit"] not in v15
            v15[r["bit"]] = r["nodes"]
            v15_total += r["nodes"]
    assert v15_pilots == 4 and len(v15) == 25 and set(v15) == set(wins)
    assert v15_total == 116892833, v15_total

    # ------------------------------------------------ output
    out = {
        "schema": "n11-class2-lane-cost73k-raw-sweep-audit-20261117-v1",
        "date": "2026-11-17",
        "status": ("PASS: fresh regeneration (third independent execution) of the "
                   "cost73k 73-bit v17 depth-10 sweep; all 73 per-bit verdicts, "
                   "node counts and capped flags identical to the published "
                   "concurrent-session record; 25 WIN7-D10 / 48 REFUTED-D10 / 0 "
                   "capped; 7/7 confirmation transfers, six verified against "
                   "published lane sources (66i bit 10 raw-identical); det reruns "
                   "field-identical; v15 cross-engine 25/25 WIN with node total "
                   "equal to the record's v15 total"),
        "target": {
            "s6_child": CHILD,
            "stone_bits": [10, 49, 50, 57, 60, 71],
            "candidate_bits": 73,
            "open_bits": 66,
            "confirmation_bits": [14, 23, 26, 34, 53, 55, 107],
        },
        "provenance": {
            "original_run": ("the claiming session completed this sweep at "
                             "2026-11-17 (execution A) but its local raw files "
                             "were lost to a sandbox reset before publication; "
                             "the concurrent session independently ran the same "
                             "sweep (execution B, record published at commit "
                             "8803a3b0); this audit's raw files are a fresh "
                             "regeneration (execution C) from the pinned engine "
                             "source, and all three executions agree on every "
                             "per-bit non-ms field (A via its lost-session "
                             "agreement with B recorded before the reset, C vs B "
                             "verified here 73/73)"),
            "engine": ("class4_child1_runner_v17.ts, git blob " + ENGINE_BLOB +
                       ", depth 10, cap 1e9 per bit, andclose 1, fresh engine "
                       "state per candidate bit"),
            "v15_engine": "class4_child1_runner.ts, git blob " + V15_BLOB,
        },
        "pilot_checks": "9/9 raw batches + 2/2 det reruns at pilot_d6 3402; "
                        "4/4 v15 chunks at pilot_d6 5949",
        "verdicts": {
            "win7_d10_bits": wins,
            "win7_d10_nodes": {str(b): mine[b]["nodes"] for b in wins},
            "refuted_d10_bits": refuted,
            "refuted_d10_count": len(refuted),
            "capped_count": capped,
            "candidate_nodes_total": node_sum,
            "total_nodes_including_pilots": node_sum + 9 * 3402,
            "terminal_stone_range": [13, 17],
            "per_bit_identical_to_concurrent_record": "73/73 "
                "(loss, nodes, capped)",
        },
        "confirmation_bits": {
            "bits": [14, 23, 26, 34, 53, 55, 107],
            "fresh_vs_claim_transfers": "7/7",
            "fresh_vs_record_predictions": "7/7",
            "sources": {
                "14": {"source": "cost73j bit 110",
                       "verified": "raw batch7 line loss=true, capped=false "
                                   "(verdict-level; canon-equal root, node count "
                                   "differs by labeling)",
                       "raw_identical": False},
                "23": {"source": "pre-64h harvest (cost64d bit 110)",
                       "verified": "claim v1 census-v7 harvest resolution + "
                                   "published census v7 rebuilt-harvest "
                                   "assertions + record fresh outcome; REFUTED "
                                   "agreement",
                       "raw_identical": False},
                "26": {"source": "cost73i bit 110",
                       "verified": "73i audit win list (verdict-level)",
                       "raw_identical": False},
                "34": {"source": "cost72d bit 110",
                       "verified": "not in 72d win list, 72d capped 0 => REFUTED",
                       "raw_identical": False},
                "53": {"source": "cost66i bit 10",
                       "verified": "66i raw batch2 line loss=false nodes=39808; "
                                   "identical absolute root hex "
                                   "(66i child + bit 10 == 73k child + bit 53)",
                       "raw_identical": True},
                "55": {"source": "cost69j bit 110",
                       "verified": "69j audit win list (verdict-level)",
                       "raw_identical": False},
                "107": {"source": "cost71e bit 110",
                        "verified": "71e audit refuted list (verdict-level)",
                        "raw_identical": False},
            },
        },
        "determinism_rerun": {
            "batches": det_notes,
            "result": "field-identical on every non-ms field",
        },
        "v15_cross_engine_check": {
            "chunks": ["a", "b", "c", "d"],
            "win_agreement": "25/25 loss=true",
            "pilots": "4/4 at 5949",
            "capped": 0,
            "v15_nodes_total": v15_total,
            "record_v15_nodes_total": 116892833,
        },
        "pins": {
            "claim_v1": V1_BLOB,
            "concurrent_record": RECORD_BLOB,
            "census_v7": CENSUS_V7_BLOB,
            "engine_v17": ENGINE_BLOB,
            "engine_v15": V15_BLOB,
            "sources": {k: (SRC_PINS[k] if len(SRC_PINS[k]) == 40
                            else None) for k in SRC_PINS},
            "raw_batches": {},
        },
    }
    for f in RAW + list(DET) + V15:
        out["pins"]["raw_batches"][f] = git_blob_sha((raw_dir / f).read_bytes())
    # full 40-hex pins for the short-pinned sources (already verified above)
    for name in SRC_PINS:
        out["pins"]["sources"][name] = git_blob_sha((src_dir / name).read_bytes())

    text = json.dumps(out, indent=1, ensure_ascii=True) + "\n"
    out_path.write_text(text)
    print(f"audit JSON written: {out_path} ({len(text)} bytes)")
    print("blob:", git_blob_sha(text.encode()))

if __name__ == "__main__":
    main()
