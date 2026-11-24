#!/usr/bin/env python3
"""Part DI maker: derive the reprobe registry (input/reprobe-keys.json) for the
batch-31 (closure class 5804) last-remaining-EXHAUSTED-1-row (ad043)
higher-budget (30M) reprobe.

Scope dispute guard: this maker performs NO solver run and NO key selection.
The key set is the machine-extracted last-remaining EXHAUSTED row of the
PUBLISHED batch-31 status.log (sha256 c69c2fec..., itself byte-published by the
Part CY drive-2 takeover C commit 70d79714), corroborated by the published
batch-31 README aggregate (LOSS 51 / WIN 3 / EXHAUSTED 1 ad043). The reprobe
condition (budget 30000000) is a NEW condition relative to the published
batch-31 15M probes; the no-same-condition-re-search rule for COMPLETED
exhaustion rows is untouched: no row here is re-searched at 15M.
Part CT precedent (batch-28 aa050, published
research/experiments/n11-centralreply-class5343-b28aa050-reprobe30m-20261123/)
is followed byte-for-byte in design; the derived 30M runner is byte-identical
to the published CT runner (sha256 3b5083b4...).

Fail-closed gates (any mismatch aborts with rc=1, no partial output written):
  G1  input/batch-keys.json sha256 == d058fddc... (published batch-31 packet)
      and its budget field == 15000000 and class_index == 5804.
  G2  pinned target/anchor id list found in batch-keys packet (1+2 ids).
  G3  each target/anchor input CSV sha256 == its published pin; CSV field
      structure target,0,5,<lo>,<hi>,<legal>,0*5; lo/hi/legal match packet row.
  G4  target's published 15M exhaustion raw pass files
      (sources/exh15m/ad043.p{1,2}.out, byte-pinned to the published batch-31
      drive-2 raw) are complete (replay_done), budget field 15000000, result 0,
      nodes 15000000, p1/p2 node-exact (wall_s exempt).
  G5  --b31-status PATH: sha256 == c69c2fec... (published batch-31 status.log,
      59 lines); the target ad043 carries an EXHAUSTED line
      "15000000,0,15000000" and NO PASS/WIN-HALT line of its own (the pinned
      runner's pre-registered double-record design writes PASS then EXHAUSTED
      for exhaustion rows; both are pinned here); anchors carry pinned PASS
      lines (ad054 "15000000,2,1644957"; ad055 "15000000,1,3364655" +
      WIN-HALT) - ad043 is thereby machine-extracted as the last remaining
      EXHAUSTED row of batch-31 (prose not used for selection).
  G6  --base-cache PATH: the cache file sha256 == 04b0a239... (Part DB merged
      canonical 6,354 verdict rows, the current canonical chain head per the
      published Part DH A2b sources); the target (lo,hi) must be ABSENT from
      the cache (0/1 hits). Recorded in the registry as a selection fact.
  G7  anchors: input CSV sha-pinned (G3); published 15M raw pass files
      (sources/anchor-15m/ad0NN.p{1,2}.out) sha-pinned; parsed replay rows
      must equal the pinned expectation (ad054: result 2 nodes 1644957;
      ad055: result 1 nodes 3364655) at budget field 15000000.

Output: input/reprobe-keys.json (deterministic byte-stable serialization).
Interpretation guard: nodes counts are bookkeeping, never verdicts; results of
the reprobe are honest labels only; nothing is canonically consumed here; the
standard 11x11 empty board and every key stay UNKNOWN.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
EXP = HERE.parents[1]

PIN_BATCH_KEYS = "d058fddc862c5f62b387eea7c7ac5b78f2c5063661371b388e5078772af4ff0e"
PIN_B31_STATUS = "c69c2fec9d07e50dca6763fdb97acb5a05798b7852a1ab45be8e7a7a7889dd5b"
PIN_BASE_CACHE = "04b0a23987a97518e276ea5ff966496facab22f93628cd5fbc682a04c3650556"
PIN_DERIVED_RUNNER = "3b5083b47c043f93bbe01a5f3335baba6be6d1d6929885f4ab5b28b1778cf7b4"
TARGET_IDS = ["ad043"]
PIN_INPUT_CSV = {
    "ad043": "fda5d01d981b3ae7c1874cb11aae4379d0add8a53f11defb6ded496fd1b2bcd2",
    "ad054": "9bf500fb698bfa2edaedcaf0e6a1657e7a1a23bc7d692036e99a7d54a6de7436",
    "ad055": "cad75b29d57da78d677c26850f515ba62e57596ca938b05c33694741d227e394",
}
PIN_EXH15M_RAW = {
    "ad043": {"p1": "5f3bf5bc6f6bc636c7aa6d7e72619530ce2a0b918558d635ac7191b27c729d11",
              "p2": "1feacf0c91cfaa72e9f3965bc0be83beb6aebbba005a74f0fbbdcfffb4b4db15"},
}
PIN_ANCHOR15M = {
    "ad054": {"p1": "c2d1500b831836c7791d96d3fab5f344c59bff506d96854c510a2c504e9ae1e0",
              "p2": "c2d1500b831836c7791d96d3fab5f344c59bff506d96854c510a2c504e9ae1e0",
              "result": 2, "nodes": 1644957},
    "ad055": {"p1": "61704c55151f00db87c59285e40ba01180da5b762c9bb73ecf285fe93b9c34dd",
              "p2": "61704c55151f00db87c59285e40ba01180da5b762c9bb73ecf285fe93b9c34dd",
              "result": 1, "nodes": 3364655},
}
PIN_STATUS_FACTS = {
    "target_exhausted": {"id": "ad043", "fields": "15000000,0,15000000"},
    "anchor_pass": {"ad054": "15000000,2,1644957", "ad055": "15000000,1,3364655"},
    "anchor_win_halt": ["ad055"],
}
REPROBE_BUDGET = 30000000


def fail(msg):
    print("MAKER ABORT: " + msg)
    raise SystemExit(1)


def sha(p):
    d = hashlib.sha256()
    with Path(p).open("rb") as fh:
        for b in iter(lambda: fh.read(1024 * 1024), b""):
            d.update(b)
    return d.hexdigest()


def parse_raw_expect(path, budget, result, nodes, label):
    g = sha(path)
    txt = Path(path).read_text(encoding="utf-8")
    if "# replay_done" not in txt:
        fail(f"{label}: published raw truncated: {path.name}")
    row = [ln for ln in txt.splitlines() if ln.startswith("replay,")]
    if len(row) != 1:
        fail(f"{label}: published raw replay rows != 1: {path.name}")
    r = row[0].split(",")
    if int(r[5]) != budget or int(r[6]) != result or int(r[7]) != nodes:
        fail(f"{label}: published raw expectation mismatch: {path.name}: {r}")
    return r


def parse_pair_exact(src_p1, src_p2, pin_p1, pin_p2, budget, result, nodes, label):
    for p, pin in ((src_p1, pin_p1), (src_p2, pin_p2)):
        if sha(p) != pin:
            fail(f"{label} raw sha mismatch {p.name}: {sha(p)}")
    rows = [parse_raw_expect(p, budget, result, nodes, f"{label} {p.name}")
            for p in (src_p1, src_p2)]
    if rows[0][:8] + rows[0][9:] != rows[1][:8] + rows[1][9:]:
        fail(f"{label} published rows not node-exact")
    return rows


def main():
    bkp = EXP / "input/batch-keys.json"
    if sha(bkp) != PIN_BATCH_KEYS:
        fail("G1 batch-keys sha mismatch " + sha(bkp))
    bk = json.loads(bkp.read_text(encoding="utf-8"))
    if bk.get("budget") != 15000000:
        fail("G1 batch-keys budget != 15000000")
    if bk.get("class_index") != 5804:
        fail("G1 class_index != 5804")
    packet = {k["key_id"]: k for k in bk["keys"]}
    for kid in TARGET_IDS + list(PIN_ANCHOR15M):
        if kid not in packet:
            fail("G2 id missing from published packet: " + kid)

    targets = []
    for kid in TARGET_IDS:
        csvp = EXP / f"input/{kid}.input.csv"
        g = sha(csvp)
        if g != PIN_INPUT_CSV[kid]:
            fail(f"G3 input csv sha mismatch {kid}: {g}")
        fields = csvp.read_text(encoding="utf-8").strip().split(",")
        want = ["target", "0", "5", packet[kid]["lo"], packet[kid]["hi"],
                str(packet[kid]["legal"]), "0", "0", "0", "0", "0"]
        if fields != want:
            fail(f"G3 input csv field mismatch {kid}: {fields} vs {want}")
        parse_pair_exact(EXP / f"sources/exh15m/{kid}.p1.out",
                          EXP / f"sources/exh15m/{kid}.p2.out",
                          PIN_EXH15M_RAW[kid]["p1"], PIN_EXH15M_RAW[kid]["p2"],
                          15000000, 0, 15000000, "G4")
        targets.append({
            "key_id": kid,
            "s5_index": packet[kid]["s5_index"],
            "lo": packet[kid]["lo"],
            "hi": packet[kid]["hi"],
            "legal": packet[kid]["legal"],
            "membership_class_count": packet[kid]["membership_class_count"],
            "input_csv_sha256": PIN_INPUT_CSV[kid],
            "published_15m": {"result": 0, "nodes": 15000000,
                              "raw_p1_sha256": PIN_EXH15M_RAW[kid]["p1"],
                              "raw_p2_sha256": PIN_EXH15M_RAW[kid]["p2"]},
        })

    anchors = []
    for kid, meta in PIN_ANCHOR15M.items():
        csvp = EXP / f"input/{kid}.input.csv"
        g = sha(csvp)
        if g != PIN_INPUT_CSV[kid]:
            fail(f"G7 anchor input csv sha mismatch {kid}: {g}")
        parse_pair_exact(EXP / f"sources/anchor-15m/{kid}.p1.out",
                          EXP / f"sources/anchor-15m/{kid}.p2.out",
                          meta["p1"], meta["p2"],
                          15000000, meta["result"], meta["nodes"], f"G7 {kid}")
        anchors.append({
            "key_id": kid,
            "lo": packet[kid]["lo"],
            "hi": packet[kid]["hi"],
            "legal": packet[kid]["legal"],
            "published_15m": {"result": meta["result"], "nodes": meta["nodes"],
                              "raw_p1_sha256": meta["p1"],
                              "raw_p2_sha256": meta["p2"]},
            "expect_at_30m": {"result": meta["result"], "nodes": meta["nodes"]},
            "note": ("resolved rows re-run under the higher budget flag as derived-runner "
                     "val anchors; the deterministic search must reproduce the published "
                     "node count exactly (budget only caps, so nodes are unchanged)"),
        })

    base_cache_block = None
    b31_status_block = None
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == "--base-cache":
            bp = Path(args[i + 1])
            if sha(bp) != PIN_BASE_CACHE:
                fail("G6 base cache sha mismatch " + sha(bp))
            hits = {t: 0 for t in TARGET_IDS}
            n = 0
            for ln in bp.read_text(encoding="utf-8").splitlines():
                if not ln.startswith("s5verdict,"):
                    continue
                n += 1
                f = ln.split(",")
                for t in TARGET_IDS:
                    packet_row = packet[t]
                    if f[1] == packet_row["lo"] and f[2] == packet_row["hi"]:
                        hits[t] += 1
            if any(v != 0 for v in hits.values()):
                fail("G6 target rows already present in base cache: " + json.dumps(hits))
            base_cache_block = {
                "path": "research/experiments/n11-centralreply-closure-b28p4win9-thirdimpl-20261124/sources/canonical-cache-db-merged-b29loss37.cache",
                "sha256": PIN_BASE_CACHE,
                "verdict_rows": n,
                "target_hits": {t: 0 for t in TARGET_IDS},
                "note": ("Part DB merged canonical 6354-row chain head (published as Part "
                         "DH A2b source); batch-31 rows incl. the target are pre-adoption "
                         "there by construction - recorded here as a machine fact"),
            }
        elif a == "--b31-status":
            ap = Path(args[i + 1])
            g = sha(ap)
            if g != PIN_B31_STATUS:
                fail("G5 b31 status sha mismatch " + g)
            fact = PIN_STATUS_FACTS
            target = fact["target_exhausted"]
            passive = {}
            exhaustive = set()
            winhalt = set()
            anchor_pass_ok = {k: False for k in fact["anchor_pass"]}
            for ln in ap.read_text(encoding="utf-8").splitlines():
                parts = ln.split()
                if len(parts) < 3:
                    continue
                kid, verdict, fld = parts[1], parts[2], parts[3] if len(parts) > 3 else ""
                if verdict == "PASS":
                    passive[kid] = fld
                    if kid in fact["anchor_pass"] and fld == fact["anchor_pass"][kid]:
                        anchor_pass_ok[kid] = True
                elif verdict == "EXHAUSTED":
                    exhaustive.add((kid, fld))
                elif verdict == "WIN-HALT":
                    winhalt.add(kid)
            if (target["id"], target["fields"]) not in exhaustive:
                fail("G5 target EXHAUSTED line absent from published b31 status.log")
            exh_ids = sorted({kid for (kid, _f) in exhaustive})
            if exh_ids != sorted(TARGET_IDS):
                fail("G5 published b31 EXHAUSTED id set != pinned target set ("
                     "target selection is machine-extracted, prose not used): "
                     + json.dumps(exh_ids))
            # the pinned runner's pre-registered double-record design writes
            # PASS (with result-0 fields) then EXHAUSTED for exhaustion rows;
            # the target is resolved ONLY if it carries a PASS line with a
            # result-1/2 field triple or a WIN-HALT line.
            t_resolved = (target["id"] in winhalt) or any(
                target["id"] == kid and fld.split(",")[1:2] and fld.split(",")[1] in ("1", "2")
                for kid, fld in passive.items())
            if t_resolved:
                fail("G5 target appears resolved in published b31 status.log")
            if not all(anchor_pass_ok.values()):
                fail("G5 anchor PASS facts absent from published b31 status.log: "
                     + json.dumps(anchor_pass_ok))
            for k in fact["anchor_win_halt"]:
                if k not in winhalt:
                    fail("G5 anchor WIN-HALT absent from published b31 status.log: " + k)
            b31_status_block = {
                "sha256": PIN_B31_STATUS,
                "published_commit": "70d79714",
                "lines": len(ap.read_text(encoding="utf-8").splitlines()),
                "target_last_remaining_exhausted": {"id": "ad043",
                    "fields": "15000000,0,15000000"},
                "target_in_resolved_lines": False,
                "anchor_facts": {"ad054_pass": "15000000,2,1644957",
                                 "ad055_pass": "15000000,1,3364655",
                                 "ad055_win_halt": True},
                "source_experiment_dir":
                    "research/experiments/n11-centralreply-closure-class5804-batch31-20261124/",
            }

    reg = {
        "schema": "n11-centralreply-c5804-b31ad043-reprobe30m-input-v1",
        "class_index": 5804,
        "batch": 31,
        "source_condition": {
            "budget": 15000000,
            "published_batch_packet_sha256": PIN_BATCH_KEYS,
            "published_b31_status": b31_status_block,
            "published_aggregate": {
                "loss": 51, "win": ["ad024", "ad028", "ad055"],
                "exhausted": ["ad043"],
                "source": "published batch-31 README (Part CY drive-2 takeover C, commit 70d79714)"},
        },
        "reprobe_condition": {
            "budget": REPROBE_BUDGET,
            "derived_runner_sha256": PIN_DERIVED_RUNNER,
            "note": ("higher-budget NEW-condition reprobe pre-declared by Part DI "
                     "(Part CT precedent followed byte-for-byte in design); the "
                     "published 15M condition is not re-run (no-same-condition-"
                     "re-search rule for COMPLETED exhaustion rows is untouched); "
                     "result 0 at 30M remains honest UNKNOWN with no same-condition "
                     "re-probe; published 15M exhaustion pass wall is 108s so a 30M "
                     "single pass is expected ~216s: a single invocation cannot host "
                     "p1+p2 inside the 260s inner window, so the published "
                     "cross-invocation p1/p2 file-existence resume guard is exercised "
                     "as pre-declared (1-3 invocations per key, WINDOW-EXCEEDED "
                     "backup rule intact); a still-exhausted target at 30M would need "
                     "a future Part with a different window/budget design"),
        },
        "base_cache_absence_check": base_cache_block,
        "keys": targets,
        "anchors": anchors,
    }
    out = EXP / "input/reprobe-keys.json"
    body = json.dumps(reg, indent=1, ensure_ascii=True) + "\n"
    out.write_text(body, encoding="utf-8")
    print(f"reprobe-keys.json written: {len(targets)} targets, {len(anchors)} anchors, "
          f"budget {REPROBE_BUDGET}, sha256 {hashlib.sha256(body.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
