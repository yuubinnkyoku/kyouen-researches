# make_inputs_batch12.py -- machine-derive the batch-12 (class 8106, Part AC)
# third-impl input CSVs for the Part AD cross-verification rows from the
# published batch-12 raws (no hand transcription). Fail-closed: any unexpected
# field aborts.
#
# Sources (all fetched from repo main via the raw CDN, commit-pinned):
#  - sources/raw/<key>.p1.out / .p2.out  (declaring-host jsreplay replica
#    2-pass node-exact rows; batch-12 was run in full by the declaring Part AC
#    session itself - 8/52 keys probed (n001-n008), n005/n006 = the two
#    same-wave WIN-HALT rows, n001-n004/n007/n008 = LOSS)
#  - sources/batch-keys.json (published batch-12 input declaration, 52 keys,
#    sha256 de55df83483663e31b1c1db0fb8a1239079e7152bddef9bd893439b7b2fdbdc2,
#    scaffold commit d333bb2c)
#  - sources/status.log (published batch-12 declaring-host runner log; every
#    target row must match its `PASS 15000000,<result>,<nodes>` line; the
#    `n005 WIN-HALT` and `n006 WIN-HALT` stop lines plus RUNNER-STOP/RUNNER-EXIT
#    are asserted present)
#  - sources/<key>.input.csv (published batch-12 input CSVs for the 8 target
#    rows; the freshly derived CSV for every target must be byte-identical to
#    the published one - an extra cross-check available because the declaring
#    session published its input CSVs in the scaffold commit)
#
# Anchors/negatives identical to Part G/K/O/P/T/W/AA (same published third-impl
# values).
# NOTE: batch-12 rows (n001-n008) are NOT consumed into the canonical chain
# cache; this experiment is verdict-level corroboration literature only
# (verdicts not consumed). Batch-12 probed 8/52 keys (n009-n052 untouched).
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")

PIN_BATCH_KEYS_SHA = "de55df83483663e31b1c1db0fb8a1239079e7152bddef9bd893439b7b2fdbdc2"

# Part AD targets: both batch-12 WIN rows + all six probed LOSS rows
# (batch-12 halted in its second wave at the pre-registered WIN-HALT rule,
# which fired twice in the same wave - n006 and n005;
# replica nodes 6.47M / 3.08M / 4.56M / 3.71M / 12.86M(WIN) / 3.70M(WIN) /
# 2.91M / 3.44M)
TARGETS = [("n005", "win"), ("n006", "win"),
           ("n001", "loss"), ("n002", "loss"), ("n003", "loss"),
           ("n004", "loss"), ("n007", "loss"), ("n008", "loss")]

ANCHORS = [
    # (key_id, lo, hi, legal, third-impl published result, expansions, ttHits, expect_verdict)
    ("k02a", 1297036692683751424, 68157440, 87, 1, 9106337, 4991527, "win"),
    ("l1a", 13019119616, 16448, 116, 2, 7660602, 3951175, "loss"),
]

def sha256(path):
    import hashlib
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()

def parse_replay_csv(path):
    """Return the single `replay,...` row of a jsreplay raw, field-split."""
    got = []
    with open(path) as fh:
        for line in fh:
            if line.startswith("replay,"):
                got.append(line.strip())
    if len(got) != 1:
        sys.exit(f"ABORT raw parse {path}: {len(got)} replay rows")
    return got[0].split(",")

def parse_raw(key, kmap):
    """Parse the declaring-host jsreplay replica rows for a batch-12 key;
    cross-check the p2 twin, the published batch-keys.json declaration and
    the published status.log."""
    per_pass = []
    for p in ("p1", "p2"):
        path = os.path.join(SRC, "raw", f"{key}.{p}.out")
        if not os.path.isfile(path):
            sys.exit(f"ABORT missing raw {path}")
        per_pass.append(parse_replay_csv(path))
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
    # batch-12 batch-keys.json stores lo/hi as decimal STRINGS (121-bit keys
    # cannot round-trip JSON numbers); compare digit-for-digit in exact ints
    if lo != int(bk["lo"]) or hi != int(bk["hi"]) or legal != bk["legal"]:
        sys.exit(f"ABORT {key}: raw key/legal {lo},{hi},{legal} != batch-keys {bk}")
    result, nodes = int(f1[6]), int(f1[7])
    # declaring-host status.log cross-check:
    # `DATE <key> PASS 15000000,<result>,<nodes>`
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
    if len(kmap) != 52:
        sys.exit(f"ABORT batch-keys.json keys {len(kmap)} != 52")
    rows = []
    for key, kind in TARGETS:
        r = parse_raw(key, kmap)
        expect = 1 if kind == "win" else 2
        if r["replica_result"] != expect:
            sys.exit(f"ABORT {key}: replica result {r['replica_result']} != expected {expect}")
        r["expect_third"] = expect
        rows.append(r)
    # both WIN-HALT rows plus the runner stop lines are asserted present for
    # schema honesty (batch-12 is the first closure batch with two WIN-HALT
    # stop lines in the same wave)
    with open(os.path.join(SRC, "status.log")) as fh:
        slog = fh.read()
    if "n005 WIN-HALT" not in slog or "n006 WIN-HALT" not in slog:
        sys.exit("ABORT status.log lacks one of the n005/n006 WIN-HALT stop lines")
    if "RUNNER-STOP" not in slog or "RUNNER-EXIT" not in slog:
        sys.exit("ABORT batch-12 status.log lacks its RUNNER-STOP/RUNNER-EXIT lines")
    if int(keys_json["class_index"]) != 8106:
        sys.exit(f"ABORT batch-keys class_index {keys_json['class_index']} != 8106")
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
    rows_json = {"schema": "n11-centralreply-closure-batch12-wins-thirdimpl-input-v1",
                 "sources": {
                     "batch_keys_sha256": PIN_BATCH_KEYS_SHA,
                     "raws": "sources/raw (published batch-12 raws 16 files: declaring-host 8 keys x 2-pass, chunk commits eca35f3c/ace92d84, fetched from the repo raw CDN, commit-pinned)",
                     "status_log": "sources/status.log (published batch-12 declaring-host runner log, commit ace92d84)"},
                 "consumed_into_canonical_cache": False,
                 "targets": rows, "anchors": anchor_rows, "negatives": negatives}
    with open(os.path.join(OUT, "rows.json"), "w") as fh:
        json.dump(rows_json, fh, indent=1)
        fh.write("\n")
    # derived-vs-published input CSV byte-equality gate (batch-12 published
    # its per-key input CSVs in the scaffold commit d333bb2c; every target
    # row's derived CSV must be byte-identical to the published one)
    for r in rows:
        csv = f"target,0,5,{r['lo']},{r['hi']},{r['legal']},0,0,0,0,0\n"
        pub_path = os.path.join(SRC, f"{r['key_id']}.input.csv")
        with open(pub_path) as fh:
            pub = fh.read()
        if csv != pub:
            sys.exit(f"ABORT {r['key_id']}: derived CSV {csv!r} != published {pub!r}")
        with open(os.path.join(OUT, f"{r['key_id']}.input.csv"), "w") as fh:
            fh.write(csv)
    for r in anchor_rows:
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
