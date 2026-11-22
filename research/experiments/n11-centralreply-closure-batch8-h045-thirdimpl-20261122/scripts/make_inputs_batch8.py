# make_inputs_batch8.py -- machine-derive the batch-8 (class 2634, Part N/U) third-impl
# input CSVs for the Part W cross-verification rows from the published batch-8 raws
# (no hand transcription). Fail-closed: any unexpected field aborts.
#
# Sources (all fetched from repo main at the batch-8 WIN-HALT publication commit
# 1f127fb82971704ace476cac5345d8cda5808e9f, raw CDN, commit-pinned):
#  - sources/raw/<key>.p1.out / .p2.out  (jsreplay replica 2-pass node-exact rows;
#    probed under Part N and the Part U takeover; h045 = WIN-HALT row,
#    h018/h025/h026 = stratified LOSS spot rows spanning the batch-8 LOSS node
#    range 1.56M / 11.19M / 4.28M)
#  - sources/batch-keys.json (published batch-8 input declaration, 51 keys,
#    sha256 5c42a950c687bbd1b8a9e25b1fdd5cffb4b7a19565a3d4372173a2001fcccc02)
#  - sources/status.log (published batch-8 runner status log; every target row
#    must match its `PASS 15000000,<result>,<nodes>` line)
#
# Anchors/negatives identical to Part G/K/O/P/T (same published third-impl values).
# NOTE: batch-8 rows (h001-h045) are NOT consumed into the canonical chain cache;
# this experiment is verdict-level corroboration literature only (verdicts not consumed).
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")

PIN_BATCH_KEYS_SHA = "5c42a950c687bbd1b8a9e25b1fdd5cffb4b7a19565a3d4372173a2001fcccc02"

# Part W targets: the batch-8 WIN row + 3 stratified LOSS spots (replica nodes
# span 1.56M / 4.28M / 6.37M(WIN) / 11.19M, i.e. nearly the full batch-8 probed
# node range; h026 is additionally the takeover rescue cross-check row and
# h025 a declaring-host row)
TARGETS = [("h045", "win"), ("h018", "loss"), ("h025", "loss"), ("h026", "loss")]

ANCHORS = [
    # (key_id, lo, hi, legal, third-impl published result, expansions, ttHits, expect_verdict)
    ("k02a", 1297036692683751424, 68157440, 87, 1, 9106337, 4991527, "win"),
    ("l1a", 13019119616, 16448, 116, 2, 7660602, 3951175, "loss"),
]

def sha256(path):
    import hashlib
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()

def parse_raw(key, kmap):
    """Parse the jsreplay replica row from a batch-8 raw; cross-check the p2 twin,
    the published batch-keys.json declaration and the published status.log."""
    per_pass = []
    for p in ("p1", "p2"):
        path = os.path.join(SRC, "raw", f"{key}.{p}.out")
        if not os.path.isfile(path):
            sys.exit(f"ABORT missing raw {path}")
        got = []
        with open(path) as fh:
            for line in fh:
                if line.startswith("replay,"):
                    got.append(line.strip())
        if len(got) != 1:
            sys.exit(f"ABORT raw parse {path}: {len(got)} replay rows")
        per_pass.append(got[0].split(","))
    f1, f2 = per_pass
    # raw field layout: [0]='replay', [1]=id, [2]=stones, [3]=legal, [4]=is_or,
    # [5]=budget, [6]=result, [7]=nodes, [8]=wall_s, [9]=key_lo, [10]=key_hi
    for i in (3, 6, 7, 9, 10):
        if f1[i] != f2[i]:
            sys.exit(f"ABORT {key}: source raw passes differ at field {i}: {f1[i]} vs {f2[i]}")
    if f1[2] != "5" or f1[4] != "0" or f1[5] != "15000000":
        sys.exit(f"ABORT {key}: unexpected source schema {f1[:6]}")
    lo, hi, legal = int(f1[9]), int(f1[10]), int(f1[3])
    bk = kmap[key]
    # batch-8 batch-keys.json stores lo/hi as decimal STRINGS (121-bit keys cannot
    # round-trip JSON numbers); compare digit-for-digit in exact Python ints
    if lo != int(bk["lo"]) or hi != int(bk["hi"]) or legal != bk["legal"]:
        sys.exit(f"ABORT {key}: raw key/legal {lo},{hi},{legal} != batch-keys {bk}")
    result, nodes = int(f1[6]), int(f1[7])
    # status.log cross-check: `DATE <key> PASS 15000000,<result>,<nodes>`
    stat = None
    with open(os.path.join(SRC, "status.log")) as fh:
        for line in fh:
            toks = line.split()
            if len(toks) >= 4 and toks[1] == key and toks[2] == "PASS":
                stat = toks[3].split(",")
    if stat is None:
        sys.exit(f"ABORT {key}: no PASS line in status.log")
    if stat[0] != "15000000" or int(stat[1]) != result or int(stat[2]) != nodes:
        sys.exit(f"ABORT {key}: status.log {stat} != raw ({result},{nodes})")
    return {"key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "replica_result": result, "replica_nodes": nodes}

def main():
    os.makedirs(OUT, exist_ok=True)
    bk_sha = sha256(os.path.join(SRC, "batch-keys.json"))
    if bk_sha != PIN_BATCH_KEYS_SHA:
        sys.exit(f"ABORT batch-keys.json sha {bk_sha} != pin {PIN_BATCH_KEYS_SHA}")
    keys_json = json.load(open(os.path.join(SRC, "batch-keys.json")))
    kmap = {k["key_id"]: k for k in keys_json["keys"]}
    rows = []
    for key, kind in TARGETS:
        r = parse_raw(key, kmap)
        expect = 1 if kind == "win" else 2
        if r["replica_result"] != expect:
            sys.exit(f"ABORT {key}: replica result {r['replica_result']} != expected {expect}")
        r["expect_third"] = expect
        rows.append(r)
    # h045 must additionally be the published WIN-HALT row
    with open(os.path.join(SRC, "status.log")) as fh:
        slog = fh.read()
    if "h045 WIN-HALT" not in slog:
        sys.exit("ABORT status.log lacks the h045 WIN-HALT stop line")
    if "RUNNER-STOP" in slog:
        sys.exit("ABORT unexpected RUNNER-STOP line in batch-8 status.log")
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    negatives = [
        {"key_id": "ng1", "lo": 1297036692683751424, "hi": 68157440, "legal": 88,
         "stones": 5, "why": "legal+1 vs derived 87"},
        {"key_id": "ng2", "lo": 1297036692683751424, "hi": 68157440, "legal": 87,
         "stones": 6, "why": "stones 6 vs actual 5"},
    ]
    rows_json = {"schema": "n11-centralreply-closure-batch8-h045-thirdimpl-input-v1",
                 "sources": {"batch_keys_sha256": PIN_BATCH_KEYS_SHA,
                             "raws": "sources/raw (published batch-8 raws 8 files @ commit 1f127fb8, fetched from the repo raw CDN, commit-pinned)",
                             "status_log": "sources/status.log (published batch-8 runner log @ commit 1f127fb8, fetched from the repo raw CDN, commit-pinned)"},
                 "consumed_into_canonical_cache": False,
                 "targets": rows, "anchors": anchor_rows, "negatives": negatives}
    with open(os.path.join(OUT, "rows.json"), "w") as fh:
        json.dump(rows_json, fh, indent=1)
        fh.write("\n")
    for r in rows + anchor_rows:
        csv = f"target,0,5,{r['lo']},{r['hi']},{r['legal']},0,0,0,0,0\n"
        with open(os.path.join(OUT, f"{r['key_id']}.input.csv"), "w") as fh:
            fh.write(csv)
    for r in negatives:
        csv = f"target,0,{r['stones']},{r['lo']},{r['hi']},{r['legal']},0,0,0,0,0\n"
        with open(os.path.join(OUT, f"{r['key_id']}.input.csv"), "w") as fh:
            fh.write(csv)
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(negatives))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"],
              "replica_result", r["replica_result"], "replica_nodes", r["replica_nodes"],
              "expect_third", r["expect_third"])

if __name__ == "__main__":
    main()
