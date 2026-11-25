#!/usr/bin/env python3
"""v17 full-row re-check of the cost-65f/65j sweep (2026-11-17).

Final step of the past-lane v17 re-check queue opened by the 2026-11-17
fbt-saturation defect log: REFUTED-D10 verdicts produced by pre-v16
engines cannot be node-compared with v17, but they must still be
re-swept with the fbt-repaired v17 engine before being reused as
planning evidence (verdict-only comparison).

cost-65f/65j: child 00000000000000809102000080000000
(65 candidates; 64 swept + 1 transferred bit 113 which inherits its
verdict from a source row and is out of scope here).
Published resolution (65j inflight v5, FOLD COMPLETE):
- 17 WIN7-D10 bits 4/15/18/20/21/23/25/28/66/79/91/101/109 (from the
  v15 raw batches 1-7, 2026-11-14) and 112/116/118/119 (from the v16
  raw batch 8, 2026-11-16); all 17 are certificate-backed with
  dual-verified published certificates (65f win13 manifest 617d3d8d,
  65j win4 manifest d4981d7e).
- 48 REFUTED-D10 bits (44 from the v15 raw batches 1-7 including the
  v4 erratum bit 92, and 111/114/117/120 from the v16 batches 8-9).
- 0 capped. v15 raw pilot_d6 = 5949 nodes; v16/v17 pilot_d6 = 3402
  nodes (engine node-counting differs; this is why the v15 part is
  verdict-only).

The row is re-executed here from scratch with the fbt-repaired engine
class4_child1_runner_v17.ts (blob c132cc64) using the published batch
partition (9 batches: 65f 1-7 + 65j 8-9), depth 10, cap 1e9, --andclose
1, fresh engine state per candidate, pilot_d6 control per batch.
Comparison rules:
- v16-derived bits (batches 8-9): full field comparison (node-exact
  unless fb saturation intervened; mismatches are recorded as
  corrections, non-node mismatches as failures).
- v15-derived bits (batches 1-7): verdict-only comparison (loss field
  equality). Nodes/capped/terminalStoneRange are not comparable
  across engines and are recorded for reference only.
Pass criteria: verdict flips 0, WIN bits unchanged, bit-set identity,
v17 pilots 3402, determinism pass when RUN2 is present.

Interpretation guard: bookkeeping verification only; WIN7-D10 proves a
first-player win within depth 10 from the individual 7-stone roots
only; REFUTED-D10 is not a LOSS proof; 11x11 empty board, two-stone
roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain UNKNOWN.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
SCR = HERE / "scripts"
RUN2 = HERE / "o65x-rerun"  # second independent execution (local; optional)

ENGINE_BLOB = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
CHILD = "00000000000000809102000080000000"
V15_PILOT = {"control": "pilot_d6", "loss": False, "nodes": 5949, "capped": False}
V16_PILOT = {"control": "pilot_d6", "loss": False, "nodes": 3402, "capped": False}

BATCHES = {
    1: ("class2-lane-cost65f-raw-batch1-20261114.jsonl", "v15"),
    2: ("class2-lane-cost65f-raw-batch2-20261114.jsonl", "v15"),
    3: ("class2-lane-cost65f-raw-batch3-20261114.jsonl", "v15"),
    4: ("class2-lane-cost65f-raw-batch4-20261114.jsonl", "v15"),
    5: ("class2-lane-cost65f-raw-batch5-20261114.jsonl", "v15"),
    6: ("class2-lane-cost65f-raw-batch6-20261114.jsonl", "v15"),
    7: ("class2-lane-cost65f-raw-batch7-20261114.jsonl", "v15"),
    8: ("class2-lane-cost65j-raw-batch8-20261116.jsonl", "v16"),
    9: ("class2-lane-cost65j-raw-batch9-20261116.jsonl", "v16"),
}
RAW_BLOBS = {
    1: "46ff5b200af04de19db8dd0ce1a57d180c70ba90",
    2: "cd3bfedbb07e7717ae4a5be44ff130dfd6c4a696",
    3: "1f3d6dc89b244f66858824ef99abe6ee2dd2de4e",
    4: "cfffbcdd472a65ca06860d691f2f8506f5315a98",
    5: "9d789a2906b471823a99aed33a2b3dc41c62e271",
    6: "2ae5fd9b57b35ff4660f7da4c13c2122e70cfb7a",
    7: "89b554a338845f7ef77f4497d97ccfa70d84c045",
    8: "963c9f80db41d8d0cce4bdde642917cf5695a210",
    9: "52cd7d8daf0d486d76694fa5e836583bd6bd669f",
}
PUBLISHED_WIN_BITS = [4, 15, 18, 20, 21, 23, 25, 28, 66, 79, 91, 101, 109,
                     112, 116, 118, 119]
FIELDS = ("loss", "nodes", "capped", "terminalStoneRange", "andclose")


def git_blob_sha1(path):
    data = Path(path).read_bytes()
    h = hashlib.sha1()
    h.update(b"blob %d\x00" % len(data))
    h.update(data)
    return h.hexdigest()


def load(path):
    recs = {}
    pilot = None
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        if "bit" in d:
            recs[d["bit"]] = d
        elif d.get("control") == "pilot_d6":
            pilot = d
    return recs, pilot


def norm(rec):
    return {k: v for k, v in rec.items() if k != "ms"}


def main():
    checks = []
    ok = True

    def check(name, cond, detail=None):
        nonlocal ok
        checks.append({"check": name, "pass": bool(cond),
                       "detail": detail if detail else ("" if cond else "FAILED")})
        if not cond:
            ok = False

    check("engine_blob_sha1_matches_pinned_c132cc64",
          git_blob_sha1(SCR / "class4_child1_runner_v17.ts") == ENGINE_BLOB)

    r_pub = {}
    r17 = {}
    v16_part = set()
    verdict_flips = []
    v16_node_corrections = []
    nonconform = []
    per_bit = []
    pilots17_ok = True
    for i in range(1, 10):
        raw_name, era = BATCHES[i]
        raw = OUT / raw_name
        v17 = OUT / f"class2-lane-cost65f65j-v17-recheck-batch{i}-20261117.jsonl"
        check(f"raw_batch{i}_blob_sha1_matches_main",
              git_blob_sha1(raw) == RAW_BLOBS[i])
        ppub, ppubp = load(raw)
        p17, p17p = load(v17)
        check(f"batch{i}_bit_set_identity", sorted(ppub) == sorted(p17),
              f"pub={sorted(ppub)} v17={sorted(p17)}")
        if p17p != V16_PILOT:
            pilots17_ok = False
            nonconform.append(("pilot_v17", i, p17p))
        if era == "v16" and ppubp != V16_PILOT:
            nonconform.append(("pilot_v16", i, ppubp))
        if era == "v15" and ppubp != V15_PILOT:
            nonconform.append(("pilot_v15_unexpected", i, ppubp))
        for b in sorted(ppub):
            a, c = ppub[b], p17[b]
            r_pub[b] = a
            r17[b] = c
            if era == "v16":
                v16_part.add(b)
                for k in FIELDS:
                    if a[k] != c[k]:
                        if k == "nodes":
                            v16_node_corrections.append(
                                {"bit": b, "v16_nodes": a["nodes"],
                                 "v17_nodes": c["nodes"],
                                 "delta": c["nodes"] - a["nodes"],
                                 "verdict_unchanged": a["loss"] == c["loss"]})
                        else:
                            nonconform.append((i, b, k, a[k], c[k]))
            per_bit.append({"batch": i, "era": era, "bit": b,
                             "pub_loss": a["loss"], "v17_loss": c["loss"],
                             "pub_nodes": a["nodes"], "v17_nodes": c["nodes"]})
            if a["loss"] != c["loss"]:
                verdict_flips.append({"bit": b, "era": era,
                                      "pub_loss": a["loss"], "v17_loss": c["loss"]})

    check("all_9_v17_pilots_identity_3402", pilots17_ok)
    check("no_unexpected_non_node_mismatch", len(nonconform) == 0,
          f"nonconform={nonconform}")
    win_bits_v17 = sorted(b for b in r17 if r17[b]["loss"])
    check("win_bits_unchanged_17_certificate_backed",
          win_bits_v17 == PUBLISHED_WIN_BITS,
          f"v17={win_bits_v17} published={PUBLISHED_WIN_BITS}")
    check("verdict_flips_zero", len(verdict_flips) == 0,
          f"flips={verdict_flips}")

    determinism = {"status": "skipped", "detail": f"RUN2 dir absent: {RUN2}"}
    if RUN2.is_dir():
        d_ok = True
        d_detail = []
        for i in range(1, 10):
            v17 = OUT / f"class2-lane-cost65f65j-v17-recheck-batch{i}-20261117.jsonl"
            p1, p1p = load(v17)
            p2, p2p = load(RUN2 / f"v17-batch{i}.jsonl")
            if p1p != V16_PILOT or p2p != V16_PILOT:
                d_ok = False
                d_detail.append(("pilot", i, p1p, p2p))
            for b in p1:
                if norm(p1[b]) != norm(p2[b]):
                    d_ok = False
                    d_detail.append((b, p1[b], p2[b]))
        determinism = {"status": "pass" if d_ok else "fail",
                       "detail": "two full independent executions agree on every bit and pilot (ms excluded)" if d_ok else str(d_detail[:5])}
        check("determinism_second_run_identical", d_ok)

    result = {
        "schema": "n11-class2-lane-cost65f65j-v17-full-row-recheck-20261117-v1",
        "date": "2026-11-17",
        "method": ("fbt-repaired v17 engine (class4_child1_runner_v17.ts, blob "
                   "c132cc64) re-executed all 64 swept bits of the row from "
                   "scratch with the published batch partition (65f raw "
                   "batches 1-7 v15 engine 2026-11-14 + 65j raw batches 8-9 "
                   "v16 engine 2026-11-16), depth 10, cap 1e9, --andclose 1, "
                   "fresh engine state per candidate, pilot_d6 control per "
                   "batch; v16-era bits compared field-by-field (node-exact "
                   "unless fb saturation), v15-era bits compared "
                   "verdict-only because v15 and v17 node counting differs "
                   "(v15 pilot 5949 vs v17 pilot 3402)"),
        "child": CHILD,
        "engine_blob_sha1": ENGINE_BLOB,
        "checked_bits": len(per_bit),
        "v16_era_bits": sorted(v16_part),
        "v15_era_bits": sorted(set(r17) - v16_part),
        "v16_node_corrections": v16_node_corrections,
        "verdict_flips": verdict_flips,
        "win_bits_v17": win_bits_v17,
        "published_win_bits": PUBLISHED_WIN_BITS,
        "total_nodes_v17": sum(r17[b]["nodes"] for b in r17),
        "total_nodes_pub": sum(r_pub[b]["nodes"] for b in r_pub),
        "determinism_rerun": determinism,
        "per_bit": per_bit,
        "checks": checks,
        "all_checks_pass": ok,
        "interpretation_guard": ("bookkeeping verification only; WIN7-D10 proves "
            "a first-player win within depth 10 from the individual 7-stone "
            "roots only; REFUTED-D10 is not a LOSS proof; the v15 part of "
            "this re-check is verdict-only and node totals across engines "
            "are not comparable; 11x11 empty board, two-stone roots "
            "{49,60}/{59,60}, S2 {59,60} and classes 1/2/4 remain UNKNOWN"),
    }
    dest = OUT / "class2-lane-cost65f65j-v17-full-row-recheck-20261117.json"
    with open(dest, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print("checks:", len(checks), "all pass:", ok)
    print("bits", len(per_bit), "wins", win_bits_v17,
          "v16 corrections", len(v16_node_corrections),
          "flips", len(verdict_flips), "determ", determinism["status"])
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
