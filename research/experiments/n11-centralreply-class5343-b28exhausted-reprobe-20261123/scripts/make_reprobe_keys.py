#!/usr/bin/env python3
"""Part CQ maker: derive the reprobe registry (input/reprobe-keys.json) for the
batch-28 (closure class 5343) EXHAUSTED-11-row higher-budget reprobe.

Scope dispute guard: this maker performs NO solver run and NO key selection.
The key set is the PINNED published EXHAUSTED row list of batch-28 (exactly the
rows labeled exhausted by the published full row-audit
`n11-centralreply-closure-class5343-batch28-rowaudit-full-v2`, output/row-audit.json
sha256 00c32383..., whose exhausted_rows array was machine-extracted read-only
before the Part CQ declaration). The reprobe condition (budget 20000000) is a
NEW condition relative to the published 15M probes; the no-15M-re-search rule for
COMPLETED exhaustion rows is untouched: no row here is re-searched at 15M.

Fail-closed gates (any mismatch aborts with rc=1, no partial output written):
  G1  input/batch-keys-b28.json sha256 == af19208f... (published batch-28 packet)
      and its budget field == 15000000 and class_index == 5343.
  G2  pinned EXHAUSTED id list found in batch-keys packet (11 ids).
  G3  each target input CSV sha256 == its published pin; CSV field structure
      target,0,5,<lo>,<hi>,<legal>,0*5; lo/hi/legal match the batch-keys row.
  G4  anchors: input CSVs sha-pinned; published 15M raw pass files
      (sources/b28-aaNNN-published15m.p{1,2}.out) sha-pinned; parsed replay rows
      must equal the pinned expectation (aa036: result 2 nodes 955659;
      aa046: result 1 nodes 2185149) at budget 15000000.
  G5  --base-cache PATH (optional, used at declaration preflight): the cache
      file sha256 == 854800f3... (Part CO merged canonical 6301 verdict rows);
      every target (lo,hi) must be ABSENT from the cache (0/11 hits).
      The result is recorded in the registry as a selection fact.

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
EXHAUSTED_IDS = ["aa004", "aa005", "aa021", "aa028", "aa030", "aa031",
                 "aa032", "aa035", "aa047", "aa050", "aa053"]
PIN_INPUT_CSV = {
    "aa004": "466f713d84104d70cfd377e1b1f6dab1dd1ef5aea210c7adbcacdfa3a012c22e",
    "aa005": "404e59ee2088df6b8da7c83a9b9bc903a0aa1f26dffd8ed4754fc38ad7192d05",
    "aa021": "de5d3baa15cbd044bf4515313aa7fc344930197b901632528fe0708acd9a1882",
    "aa028": "769a2fde51dbc59abfe94f7dfe3a5d72f9e2fdf94334c9f975dd652ba4d5b6da",
    "aa030": "d1b12bc9297f2cb8ae8f7e9375332efe9140efb1ced82fafa67fac739b6f34c1",
    "aa031": "adb50b3fd68ff315442d0888e06b50f69cb680f4cc4b69e9d22e056600ebea40",
    "aa032": "2aa666fb3b87e4a3b8901f9ce5cae9a24fc3b078d72a693639239a632236f0fe",
    "aa035": "a54715b68985dcb56c9c0439e9ca0c60d9347a89f6257c6043dec23cabca1018",
    "aa047": "1a3bfab07777557d7e0882525f695acbb5debbd57981c596954273f6ed742e0c",
    "aa050": "cc5e405ab3ba311d7c477c8f960f1f7d1dc49ef3b37b027c2acd0c573d302787",
    "aa053": "7fa4605a757dd93436488018a6991e4459151467b33e8fe4ed7542fb4cd5896a",
    "aa036": "a28b321567620664dea4770c89d2ddb13a5ee093442e3cf18025439ca223d7da",
    "aa046": "89d805819157c3c3fef2c63feea2440c15d8531b62a4f728a7173dde307c9bdb",
}
PIN_PUBLISHED15M = {
    "aa036": {"p1": "cf12fdc76936f4721bde04734935626b6f2d5b88c9d3756b2bd5ce298ce9e286",
              "p2": "cf12fdc76936f4721bde04734935626b6f2d5b88c9d3756b2bd5ce298ce9e286",
              "result": 2, "nodes": 955659},
    "aa046": {"p1": "002812fb2b2583b134516cc69745d67df0ac9b24604b3c4fe0d5d0ec5d13ec2b",
              "p2": "f9787a6bb4171e56d54e0bcee8314d37e43edc60ee6ac4ec85db9617b154c445",
              "result": 1, "nodes": 2185149},
}
REPROBE_BUDGET = 20000000


def fail(msg):
    print("MAKER ABORT: " + msg)
    raise SystemExit(1)


def sha(p):
    d = hashlib.sha256()
    with Path(p).open("rb") as fh:
        for b in iter(lambda: fh.read(1024 * 1024), b""):
            d.update(b)
    return d.hexdigest()


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
    for kid in EXHAUSTED_IDS + list(PIN_PUBLISHED15M):
        if kid not in packet:
            fail("G2 id missing from published packet: " + kid)

    targets = []
    for kid in EXHAUSTED_IDS:
        csvp = EXP / f"input/{kid}.input.csv"
        g = sha(csvp)
        if g != PIN_INPUT_CSV[kid]:
            fail(f"G3 input csv sha mismatch {kid}: {g}")
        fields = csvp.read_text(encoding="utf-8").strip().split(",")
        want = ["target", "0", "5", packet[kid]["lo"], packet[kid]["hi"],
                str(packet[kid]["legal"]), "0", "0", "0", "0", "0"]
        if fields != want:
            fail(f"G3 input csv field mismatch {kid}: {fields} vs {want}")
        targets.append({
            "key_id": kid,
            "s5_index": packet[kid]["s5_index"],
            "lo": packet[kid]["lo"],
            "hi": packet[kid]["hi"],
            "legal": packet[kid]["legal"],
            "membership_class_count": packet[kid]["membership_class_count"],
            "input_csv_sha256": PIN_INPUT_CSV[kid],
            "published_15m": {"result": 0, "nodes": 15000000},
        })

    anchors = []
    for kid, meta in PIN_PUBLISHED15M.items():
        csvp = EXP / f"input/{kid}.input.csv"
        g = sha(csvp)
        if g != PIN_INPUT_CSV[kid]:
            fail(f"G4 anchor input csv sha mismatch {kid}: {g}")
        rows = []
        for p in ("p1", "p2"):
            src = EXP / f"sources/b28-{kid}-published15m.{p}.out"
            g = sha(src)
            if g != meta[p]:
                fail(f"G4 anchor published raw sha mismatch {kid}.{p}: {g}")
            txt = src.read_text(encoding="utf-8")
            if "# replay_done" not in txt:
                fail(f"G4 anchor published raw truncated {kid}.{p}")
            row = [ln for ln in txt.splitlines() if ln.startswith("replay,")]
            if len(row) != 1:
                fail(f"G4 anchor published raw replay rows != 1 {kid}.{p}")
            r = row[0].split(",")
            if int(r[5]) != 15000000 or int(r[6]) != meta["result"] or int(r[7]) != meta["nodes"]:
                fail(f"G4 anchor published raw expectation mismatch {kid}.{p}: {r}")
            rows.append(r)
        if rows[0][:8] + rows[0][9:] != rows[1][:8] + rows[1][9:]:
            fail(f"G4 anchor published rows not node-exact {kid}")
        anchors.append({
            "key_id": kid,
            "lo": packet[kid]["lo"],
            "hi": packet[kid]["hi"],
            "legal": packet[kid]["legal"],
            "expect_at_20m": {"result": meta["result"], "nodes": meta["nodes"]},
            "note": ("resolved rows re-run under the higher budget flag as derived-runner "
                     "val anchors; the deterministic search must reproduce the published "
                     "node count exactly (budget only caps, so nodes are unchanged)"),
        })

    base_cache_block = None
    if len(sys.argv) > 2 and sys.argv[1] == "--base-cache":
        bp = Path(sys.argv[2])
        g = sha(bp)
        if g != PIN_BASE_CACHE:
            fail("G5 base cache sha mismatch " + g)
        hits = {t["key_id"]: 0 for t in targets}
        n = 0
        for ln in bp.read_text(encoding="utf-8").splitlines():
            if not ln.startswith("s5verdict,"):
                continue
            n += 1
            f = ln.split(",")
            for t in targets:
                if f[1] == t["lo"] and f[2] == t["hi"]:
                    hits[t["key_id"]] += 1
        if any(v != 0 for v in hits.values()):
            fail("G5 target rows already present in base cache: " + json.dumps(hits))
        base_cache_block = {
            "path": "research/experiments/n11-centralreply-class5343-loss7-adoption-reaudit-20261123/output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-20261123.cache",
            "sha256": PIN_BASE_CACHE,
            "verdict_rows": n,
            "target_hits": {t["key_id"]: 0 for t in targets},
        }

    reg = {
        "schema": "n11-centralreply-c5343-b28exh-reprobe20m-input-v1",
        "class_index": 5343,
        "batch": 28,
        "source_condition": {
            "budget": 15000000,
            "published_batch_packet_sha256": PIN_BATCH_KEYS,
            "published_row_audit": {
                "schema": "n11-centralreply-closure-class5343-batch28-rowaudit-full-v2",
                "row_audit_json_sha256": PIN_ROW_AUDIT,
                "exhausted_rows": EXHAUSTED_IDS,
            },
        },
        "reprobe_condition": {
            "budget": REPROBE_BUDGET,
            "note": ("higher-budget NEW-condition reprobe pre-declared by Part CQ; "
                     "the published 15M condition is not re-run (no-15M-re-search rule "
                     "for COMPLETED exhaustion rows is untouched); result 0 at 20M "
                     "remains honest UNKNOWN with no same-condition re-probe"),
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
