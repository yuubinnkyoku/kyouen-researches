#!/usr/bin/env python3
"""Part EA maker: derive the reprobe registry (input/reprobe-keys.json) for the
batch-33 (closure class 34908) remaining-EXHAUSTED-5-row
(af003/af023/af034/af039/af048) higher-budget (30M) reprobe.

Scope dispute guard: this maker performs NO solver run and NO key selection.
The key set is the machine-extracted remaining EXHAUSTED rows of the
PUBLISHED batch-33 status.log (sha256 1f663fc8..., itself byte-published by
the Part DS full-batch completion commit 72877473), corroborated by the
published batch-33 README aggregate (LOSS 45 / WIN 4 {af029,af047,af050,af053}
/ EXHAUSTED 5 {af003,af023,af034,af039,af048}). The reprobe condition
(budget 30000000) is a NEW condition relative to the published batch-33 15M
probes; the no-same-condition-re-search rule for COMPLETED exhaustion rows is
untouched: no row here is re-searched at 15M.
Part CT/DI precedent (batch-28 aa050 / batch-31 ad043, published
research/experiments/n11-centralreply-class5343-b28aa050-reprobe30m-20261123/
and
research/experiments/n11-centralreply-closure-class5804-b31ad043-reprobe30m-20261124/)
is followed byte-for-byte in design; the derived 30M runner is byte-identical
to the published CT/DI runner (sha256 3b5083b4...).

Fail-closed gates (any mismatch aborts with rc=1, no partial output written):
  G1  input/batch-keys.json sha256 == 8a863381... (published batch-33 packet)
      and its budget field == 15000000 and class_index == 34908.
  G2  pinned target/anchor id list found in batch-keys packet (5+2 ids).
  G3  each target/anchor input CSV sha256 == its published pin; CSV field
      structure target,0,5,<lo>,<hi>,<legal>,0*5; lo/hi/legal match packet row.
  G4  each target's published 15M exhaustion raw pass files
      (sources/exh15m/<kid>.p{1,2}.out, byte-pinned to the published batch-33
      raw) are complete (replay_done), budget field 15000000, result 0,
      nodes 15000000, p1/p2 node-exact (wall_s exempt).
  G5  --b33-status PATH: sha256 == 1f663fc8... (published batch-33 status.log,
      66 lines); every pinned target carries an EXHAUSTED line
      "15000000,0,15000000" and NO resolved line of its own (no PASS line with
      a result-1/2 field triple, no WIN-HALT; the pinned runner's
      pre-registered double-record design writes PASS-then-EXHAUSTED for
      exhaustion rows and both are pinned here); the machine-extracted
      EXHAUSTED id set of the whole status.log equals the pinned target set
      (target selection is machine-extracted, prose not used); anchors carry
      pinned PASS lines (af001 "15000000,2,2952432"; af029 "15000000,1,4862485"
      + WIN-HALT).
  G6  --base-cache PATH: the cache file sha256 == 4a30b88d... (Part DZ merged
      canonical 6,660 verdict rows, the current canonical chain head per the
      published Part DZ outputs commit 01f1fcc9); every target (lo,hi) must be
      ABSENT from the cache (0 hits). Recorded in the registry as a selection
      fact.
  G7  anchors: input CSV sha-pinned (G3); published 15M raw pass files
      (sources/anchor-15m/<kid>.p{1,2}.out) sha-pinned; parsed replay rows
      must equal the pinned expectation (af001: result 2 nodes 2952432;
      af029: result 1 nodes 4862485) at budget field 15000000.

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

PIN_BATCH_KEYS = "8a863381454fcfec3cb190db7130ce6801accf56170ee3a1b944402491fecbaa"
PIN_B33_STATUS = "1f663fc802c03b27c2e39d6130cf6c1392d62dd99b5847d6af477cd823a94b52"
PIN_BASE_CACHE = "4a30b88dba782138585f16e1ad0ea65da55431dbc2c59250998fc5a1331349c9"
PIN_DERIVED_RUNNER = "3b5083b47c043f93bbe01a5f3335baba6be6d1d6929885f4ab5b28b1778cf7b4"
TARGET_IDS = ["af003", "af023", "af034", "af039", "af048"]
PIN_INPUT_CSV = {
    "af001": "b2ef3588267694aff51b5ec7aa9940064c5199db2b5f00644a9ed27fca2a127b",
    "af029": "b5500b8d98cd3cbef56f6177245d8e3c21c31081f2252c6454f1aee73ce30c10",
    "af003": "1ab3277e33ad16b66caf796e4c5f2211bfbbe62eec01f02a71bdc5de13a9330a",
    "af023": "0ba31256582eae15cc80fb2bdbfe56a140533828cdab7a05eeef6ca1089a1c08",
    "af034": "a4bff56606cbb11107b77dac677b1e1151f59686174bddcf7e08c0558f590326",
    "af039": "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691",
    "af048": "d619dcd7d47d7b65f1c4325d99b69211826eb83732c3eb475f14ea4f9f973422",
}
PIN_EXH15M_RAW = {
    "af003": {"p1": "fdd1e84dc9b5a4e9cd49c6d26c33d208ac9f3f89125594426606f5fba15d597a",
              "p2": "4ef154cba92ba078bd31f68ba1643c22518057243bdeb00e53894b5840e41225"},
    "af023": {"p1": "225b4d6526f1f8c5b6a6dafe6b5b359df4718c6b6b958147582ead3c14b5e33a",
              "p2": "fc86c52502e08f04dd2a7d35d257021d808f1a3652f1ed758f91ac3c3954e17f"},
    "af034": {"p1": "6041fdeed69907458ca68cb7b335793d3c172a017368da868345f98ac8b45af0",
              "p2": "710a214bb5737b5011e8e7fe3377f6f85adc6fe3430c53c064b44eccc550d102"},
    "af039": {"p1": "a04e23ea9bd1914c997dfb26b820ce793572d2c96e9aebbae7ce283a59281331",
              "p2": "aaaaef87ff9406f8f49ea395a9d6513379636e5c2491ce9d4b95fbc7d5ef3abe"},
    "af048": {"p1": "95c30994057c5017b5e3f153fea9432c21ca7d9da119ff1181ffee95805ce2a4",
              "p2": "25fa2c2279eadd297b488d2156dfac9ee5c9abbb06e0026bfc878aaf4fce6450"},
}
PIN_ANCHOR15M = {
    "af001": {"p1": "6adb122cb8c6b0df4792bca2f4e5f43ad1e597ecea45a31bcd1af13135b69125",
              "p2": "6adb122cb8c6b0df4792bca2f4e5f43ad1e597ecea45a31bcd1af13135b69125",
              "result": 2, "nodes": 2952432},
    "af029": {"p1": "6bd7a2ac37cccd8a387d6b505112c1a93b712e8d41b43467fa0844ce64ec0036",
              "p2": "b6abaa6384ee93c890cadd350f2f844889f3ee42110935a366af7893a2030e0b",
              "result": 1, "nodes": 4862485},
}
PIN_STATUS_FACTS = {
    "target_exhausted_fields": "15000000,0,15000000",
    "anchor_pass": {"af001": "15000000,2,2952432", "af029": "15000000,1,4862485"},
    "anchor_win_halt": ["af029"],
    "published_win_halt_set": ["af029", "af047", "af050", "af053"],
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
    if bk.get("class_index") != 34908:
        fail("G1 class_index != 34908")
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
                         15000000, 0, 15000000, f"G4 {kid}")
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
    b33_status_block = None
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
                "path": ("research/experiments/n11-centralreply-b4loss1-b36loss40-"
                         "b37loss46-adoption-reaudit-20261125/output/"
                         "merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-"
                         "plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-"
                         "plus-b33loss45-plus-b35loss26-plus-b4loss1-plus-b36loss40-"
                         "plus-b37loss46-20261125.cache"),
                "sha256": PIN_BASE_CACHE,
                "verdict_rows": n,
                "target_hits": {t: 0 for t in TARGET_IDS},
                "note": ("Part DZ merged canonical 6,660-row chain head (published as the "
                         "Part DZ outputs commit 01f1fcc9); the 5 batch-33 EXHAUSTED "
                         "targets are pre-adoption there by construction (EXHAUSTED "
                         "rows are never consumed into any canonical cache) - recorded "
                         "here as a machine fact"),
            }
        elif a == "--b33-status":
            ap = Path(args[i + 1])
            g = sha(ap)
            if g != PIN_B33_STATUS:
                fail("G5 b33 status sha mismatch " + g)
            fact = PIN_STATUS_FACTS
            exh_fields = fact["target_exhausted_fields"]
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
            for t in TARGET_IDS:
                if (t, exh_fields) not in exhaustive:
                    fail(f"G5 target EXHAUSTED line absent from published b33 status.log: {t}")
                if t in winhalt:
                    fail(f"G5 target appears WIN-HALT-resolved in published b33 status.log: {t}")
                pf = passive.get(t)
                if pf is not None and pf.split(",")[1] in ("1", "2"):
                    fail(f"G5 target appears resolved (PASS result 1/2) in published b33 status.log: {t}")
            exh_ids = sorted({kid for (kid, _f) in exhaustive})
            if exh_ids != sorted(TARGET_IDS):
                fail("G5 published b33 EXHAUSTED id set != pinned target set ("
                     "target selection is machine-extracted, prose not used): "
                     + json.dumps(exh_ids))
            if sorted(winhalt) != sorted(fact["published_win_halt_set"]):
                fail("G5 published b33 WIN-HALT set != pinned set: " + json.dumps(sorted(winhalt)))
            if not all(anchor_pass_ok.values()):
                fail("G5 anchor PASS facts absent from published b33 status.log: "
                     + json.dumps(anchor_pass_ok))
            for k in fact["anchor_win_halt"]:
                if k not in winhalt:
                    fail("G5 anchor WIN-HALT absent from published b33 status.log: " + k)
            b33_status_block = {
                "sha256": PIN_B33_STATUS,
                "published_commit": "72877473",
                "lines": len(ap.read_text(encoding="utf-8").splitlines()),
                "target_remaining_exhausted_set": {t: exh_fields for t in TARGET_IDS},
                "targets_in_resolved_lines": False,
                "win_halt_set": sorted(winhalt),
                "anchor_facts": {"af001_pass": "15000000,2,2952432",
                                 "af029_pass": "15000000,1,4862485",
                                 "af029_win_halt": True},
                "source_experiment_dir":
                    "research/experiments/n11-centralreply-closure-class34908-batch33-20261124/",
            }

    reg = {
        "schema": "n11-centralreply-c34908-b33exh5-reprobe30m-input-v1",
        "class_index": 34908,
        "batch": 33,
        "source_condition": {
            "budget": 15000000,
            "published_batch_packet_sha256": PIN_BATCH_KEYS,
            "published_b33_status": b33_status_block,
            "published_aggregate": {
                "loss": 45, "win": ["af029", "af047", "af050", "af053"],
                "exhausted": ["af003", "af023", "af034", "af039", "af048"],
                "source": "published batch-33 README (Part DS full-batch completion, commit 72877473)"},
        },
        "reprobe_condition": {
            "budget": REPROBE_BUDGET,
            "derived_runner_sha256": PIN_DERIVED_RUNNER,
            "note": ("higher-budget NEW-condition reprobe pre-declared by Part EA "
                     "(Part CT/DI precedent followed byte-for-byte in design); the "
                     "published 15M condition is not re-run (no-same-condition-"
                     "re-search rule for COMPLETED exhaustion rows is untouched); "
                     "result 0 at 30M remains honest UNKNOWN with no same-condition "
                     "re-probe; published batch-33 15M exhaustion pass walls are "
                     "88-130s so a 30M single pass is expected ~176-260s: a single "
                     "invocation cannot host p1+p2 inside the 260s inner window, so "
                     "the cross-invocation p1/p2 file-existence resume guard is "
                     "exercised as pre-declared (1-3 invocations per key, "
                     "WINDOW-EXCEEDED backup rule intact); a still-exhausted target "
                     "at 30M would need a future Part with a different window/"
                     "budget design"),
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
