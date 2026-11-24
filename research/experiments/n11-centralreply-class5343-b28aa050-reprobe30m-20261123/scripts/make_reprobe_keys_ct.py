#!/usr/bin/env python3
"""Part CT maker: derive the reprobe registry (input/reprobe-keys.json) for the
batch-28 (closure class 5343) last-remaining-EXHAUSTED-1-row (aa050)
higher-budget (30M) reprobe.

Scope dispute guard: this maker performs NO solver run and NO key selection.
The key set is the machine-extracted still_exhausted_rows array of the PUBLISHED
Part CS audit (`n11-centralreply-c5343-b28exh-reprobe25m-audit-v1`, output/audit.json
sha256 c6622d57..., fetched commit-pinned 37c52cfb), itself derived from the
published Part CQ audit (6227eb2c...), itself derived from the published
batch-28 full row-audit (00c32383...). The reprobe condition (budget 30000000)
is a NEW condition relative to the published 15M probes, the published Part CQ
20M probes and the published Part CS 25M probes; the no-same-condition-re-search
rule for COMPLETED exhaustion rows is untouched: no row here is re-searched at
15M, 20M or 25M.

Fail-closed gates (any mismatch aborts with rc=1, no partial output written):
  G1  input/batch-keys-b28.json sha256 == af19208f... (published batch-28 packet)
      and its budget field == 15000000 and class_index == 5343.
  G2  pinned target/anchor id list found in batch-keys packet (1+2 ids).
  G3  each target/anchor input CSV sha256 == its published pin; CSV field
      structure target,0,5,<lo>,<hi>,<legal>,0*5; lo/hi/legal match packet row.
  G4  target's published 15M exhaustion raw pass files
      (sources/exh15m/aa050.p{1,2}.out, byte-pinned to the published Part CN
      drive-5 raw) are complete (replay_done), budget field 15000000, result 0,
      nodes 15000000, p1/p2 node-exact.
  G5  target's published CQ 20M exhaustion raw pass files
      (sources/exh20m/aa050.p{1,2}.out, byte-pinned) are complete, budget field
      20000000, result 0, nodes 20000000, p1/p2 node-exact.
  G6  target's published CS 25M exhaustion raw pass files
      (sources/exh25m/aa050.p{1,2}.out, byte-pinned) are complete, budget field
      25000000, result 0, nodes 25000000, p1/p2 node-exact.
  G7  anchors: input CSV sha-pinned; published 20M raw pass files
      (sources/cq-aaNNN-published20m.p{1,2}.out) sha-pinned; parsed replay rows
      must equal the pinned expectation (aa036: result 2 nodes 955659;
      aa004: result 1 nodes 15616012) at budget field 20000000.
  G8  --cs-audit PATH: sha256 == c6622d57... (published Part CS audit.json);
      its still_exhausted_rows == ["aa050"]; resolved_win_rows contains
      aa021/aa028/aa032 and NOT the target aa050.
  G9  --base-cache PATH: the cache file sha256 == 854800f3... (Part CO merged
      canonical 6301 verdict rows); the target (lo,hi) must be ABSENT from
      the cache (0/1 hits). Recorded in the registry as a selection fact.

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

PIN_BATCH_KEYS = "af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5"
PIN_BASE_CACHE = "854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d"
PIN_ROW_AUDIT = "00c323835f9ebc048b6ffea81a8fd556e3e8146adf1c562c34aa89d9d7bb69c0"
PIN_CQ_AUDIT = "6227eb2cfeb14c31799d94f19436c07233d55c8301d8640ee266b8cc3a366692"
PIN_CS_AUDIT = "c6622d575f8379383856510caad1bffb6bd05bf047ba54a1589f7e01090e3796"
TARGET_IDS = ["aa050"]
PIN_INPUT_CSV = {
    "aa050": "cc5e405ab3ba311d7c477c8f960f1f7d1dc49ef3b37b027c2acd0c573d302787",
    "aa036": "a28b321567620664dea4770c89d2ddb13a5ee093442e3cf18025439ca223d7da",
    "aa004": "466f713d84104d70cfd377e1b1f6dab1dd1ef5aea210c7adbcacdfa3a012c22e",
}
PIN_EXH15M_RAW = {
    "aa050": {"p1": "4b9cb07b6dbd59a341ad14c370bec299d30503f3a455da162b9a16c5fcb48e1a",
              "p2": "a6e1fde68592a5fe0fbacc2eaa23cd97d9031b89a8d506f8ce57a0c888163c3c"},
}
PIN_EXH20M_RAW = {
    "aa050": {"p1": "8a0cbbfb2dbada37728123c26c7ae00fe36b8dcee1bbb2cb3c75f9d1f6fcf39f",
              "p2": "b410dfaa1543f92c6522fb7123e83f46d9397bc0647b01289715ce0efc3ffd60"},
}
PIN_EXH25M_RAW = {
    "aa050": {"p1": "44a9239d14286b005c0aba1307bb447b3680a8422e434fc79ca770ecefe389ef",
              "p2": "44a9239d14286b005c0aba1307bb447b3680a8422e434fc79ca770ecefe389ef"},
}
PIN_PUBLISHED20M = {
    "aa036": {"p1": "f1b05b578e016cb2c64352a89151bd6379896e4e157d58500628079814ed0706",
              "p2": "f1b05b578e016cb2c64352a89151bd6379896e4e157d58500628079814ed0706",
              "result": 2, "nodes": 955659},
    "aa004": {"p1": "82ebc402cc83cf463e4921d2ebecd9ed63f6567a505444ee0cad5f5a49e02f48",
              "p2": "ec10d92b696a6144656db2d5bbcae764b7ebf529c1dd42926e5d258bb3c87701",
              "result": 1, "nodes": 15616012},
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
    bkp = EXP / "input/batch-keys-b28.json"
    if sha(bkp) != PIN_BATCH_KEYS:
        fail("G1 batch-keys sha mismatch " + sha(bkp))
    bk = json.loads(bkp.read_text(encoding="utf-8"))
    if bk.get("budget") != 15000000:
        fail("G1 batch-keys budget != 15000000")
    if bk.get("class_index") != 5343:
        fail("G1 class_index != 5343")
    packet = {k["key_id"]: k for k in bk["keys"]}
    for kid in TARGET_IDS + list(PIN_PUBLISHED20M):
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
        parse_pair_exact(EXP / f"sources/exh20m/{kid}.p1.out",
                          EXP / f"sources/exh20m/{kid}.p2.out",
                          PIN_EXH20M_RAW[kid]["p1"], PIN_EXH20M_RAW[kid]["p2"],
                          20000000, 0, 20000000, "G5")
        parse_pair_exact(EXP / f"sources/exh25m/{kid}.p1.out",
                          EXP / f"sources/exh25m/{kid}.p2.out",
                          PIN_EXH25M_RAW[kid]["p1"], PIN_EXH25M_RAW[kid]["p2"],
                          25000000, 0, 25000000, "G6")
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
            "published_cq20m": {"result": 0, "nodes": 20000000,
                                 "raw_p1_sha256": PIN_EXH20M_RAW[kid]["p1"],
                                 "raw_p2_sha256": PIN_EXH20M_RAW[kid]["p2"]},
            "published_cs25m": {"result": 0, "nodes": 25000000,
                                 "raw_p1_sha256": PIN_EXH25M_RAW[kid]["p1"],
                                 "raw_p2_sha256": PIN_EXH25M_RAW[kid]["p2"]},
        })

    anchors = []
    for kid, meta in PIN_PUBLISHED20M.items():
        csvp = EXP / f"input/{kid}.input.csv"
        g = sha(csvp)
        if g != PIN_INPUT_CSV[kid]:
            fail(f"G7 anchor input csv sha mismatch {kid}: {g}")
        parse_pair_exact(EXP / f"sources/cq-{kid}-published20m.p1.out",
                          EXP / f"sources/cq-{kid}-published20m.p2.out",
                          meta["p1"], meta["p2"],
                          20000000, meta["result"], meta["nodes"], f"G7 {kid}")
        anchors.append({
            "key_id": kid,
            "lo": packet[kid]["lo"],
            "hi": packet[kid]["hi"],
            "legal": packet[kid]["legal"],
            "expect_at_30m": {"result": meta["result"], "nodes": meta["nodes"]},
            "note": ("resolved rows re-run under the higher budget flag as derived-runner "
                     "val anchors; the deterministic search must reproduce the published "
                     "node count exactly (budget only caps, so nodes are unchanged)"),
        })

    base_cache_block = None
    cq_audit_block = None
    cs_audit_block = None
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == "--base-cache":
            bp = Path(args[i + 1])
            if sha(bp) != PIN_BASE_CACHE:
                fail("G9 base cache sha mismatch " + sha(bp))
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
                fail("G9 target rows already present in base cache: " + json.dumps(hits))
            base_cache_block = {
                "path": "research/experiments/n11-centralreply-class5343-loss7-adoption-reaudit-20261123/output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-20261123.cache",
                "sha256": PIN_BASE_CACHE,
                "verdict_rows": n,
                "target_hits": {t: 0 for t in TARGET_IDS},
            }
        elif a == "--cq-audit":
            ap = Path(args[i + 1])
            g = sha(ap)
            if g != PIN_CQ_AUDIT:
                fail("G8 cq audit sha mismatch " + g)
            cqa = json.loads(ap.read_text(encoding="utf-8"))
            if cqa.get("schema") != "n11-centralreply-c5343-b28exh-reprobe20m-audit-v1":
                fail("G8 cq audit schema mismatch")
            if "aa050" not in cqa.get("still_exhausted_rows", []):
                fail("G8 cq audit still_exhausted_rows missing aa050")
            if "aa050" in cqa.get("resolved_win_rows", []) or "aa050" in cqa.get("resolved_loss_rows", []):
                fail("G8 cq audit wrongly lists aa050 as resolved")
            cq_audit_block = {
                "schema": cqa["schema"],
                "audit_json_sha256": PIN_CQ_AUDIT,
                "published_commit": "962348f99bcb91f09accd33a76851f733160e5a3",
                "still_exhausted_rows_at_20m": sorted(cqa["still_exhausted_rows"]),
                "still_exhausted_at_20m_eligible_for_25m": ["aa021", "aa028", "aa032", "aa050"],
                "source_experiment_dir": "research/experiments/n11-centralreply-class5343-b28exhausted-reprobe-20261123/",
            }
        elif a == "--cs-audit":
            ap = Path(args[i + 1])
            g = sha(ap)
            if g != PIN_CS_AUDIT:
                fail("G8 cs audit sha mismatch " + g)
            csa = json.loads(ap.read_text(encoding="utf-8"))
            if csa.get("schema") != "n11-centralreply-c5343-b28exh-reprobe25m-audit-v1":
                fail("G8 cs audit schema mismatch")
            if sorted(csa.get("still_exhausted_rows", [])) != sorted(TARGET_IDS):
                fail("G8 cs audit still_exhausted_rows != pinned target set: "
                     + json.dumps(csa.get("still_exhausted_rows")))
            for w in ("aa021", "aa028", "aa032"):
                if w not in csa.get("resolved_win_rows", []):
                    fail("G8 cs audit resolved_win_rows missing " + w)
            for t in TARGET_IDS:
                if t in csa.get("resolved_win_rows", []) or t in csa.get("resolved_loss_rows", []):
                    fail(f"G8 cs audit target {t} wrongly in a resolved list")
            cs_audit_block = {
                "schema": csa["schema"],
                "audit_json_sha256": PIN_CS_AUDIT,
                "published_commit": "37c52cfb6ca1ee0b1171e91bd7a587366a2e0118",
                "still_exhausted_rows": sorted(csa["still_exhausted_rows"]),
                "resolved_win_rows": sorted(csa["resolved_win_rows"]),
                "source_experiment_dir": "research/experiments/n11-centralreply-class5343-b28exhausted-reprobe25m-20261123/",
            }

    reg = {
        "schema": "n11-centralreply-c5343-b28aa050-reprobe30m-input-v1",
        "class_index": 5343,
        "batch": 28,
        "source_condition": {
            "budget": 15000000,
            "published_batch_packet_sha256": PIN_BATCH_KEYS,
            "published_row_audit": {
                "schema": "n11-centralreply-closure-class5343-batch28-rowaudit-full-v2",
                "row_audit_json_sha256": PIN_ROW_AUDIT,
                "exhausted_rows": ["aa004", "aa005", "aa021", "aa028", "aa030",
                                   "aa031", "aa032", "aa035", "aa047", "aa050", "aa053"],
            },
            "published_cq20m_reprobe": cq_audit_block,
            "published_cs25m_reprobe": cs_audit_block,
        },
        "reprobe_condition": {
            "budget": REPROBE_BUDGET,
            "note": ("higher-budget NEW-condition reprobe pre-declared by Part CT; "
                     "the published 15M condition, the published Part CQ 20M "
                     "condition and the published Part CS 25M condition are not "
                     "re-run (no-same-condition-re-search rule for COMPLETED "
                     "exhaustion rows is untouched); result 0 at 30M remains "
                     "honest UNKNOWN with no same-condition re-probe; expected "
                     "single-pass wall ~131-165s (published 25M pass wall 131s) "
                     "so the published cross-invocation p1/p2 file-existence "
                     "resume guard is exercised as pre-declared (1-3 "
                     "invocations per key, WINDOW-EXCEEDED backup rule intact)"),
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
