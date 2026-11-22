# make_inputs_batch7.py -- machine-derive the batch-7 (class 10324) third-impl input CSVs
# from the batch raws (no hand transcription). Fail-closed: any unexpected field aborts.
#
# Sources:
#  - batch 7 raws  _19root-refresh-kit/batch10324/output/raw/<key>.p1.out / .p2.out
#    (jsreplay replica 2-pass node-exact rows; key/legal cross-checked against
#     batch10324/input/batch-keys.json; probed under Part L, 51/51 exact LOSS)
#  - third-impl witness anchors (k02 / l1) from the published
#    n11-sixthcost-third-implementation-verdict-reverification-20261121 witness outputs
#    (same anchor values Part G/K reproduced host-exactly)
import json, os, sys

KIT = "/home/user/knowledge/kyouen-research/_19root-refresh-kit"
BATCH = os.path.join(KIT, "batch10324")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "input")

# batch-7 probed rows: ALL 51 keys, every one expected LOSS (verdict-unconsumed)
TARGETS = [(f"h{i:03d}", "loss") for i in range(1, 52)]

ANCHORS = [
    # (key_id, lo, hi, legal, third-impl published result, expansions, ttHits, expect_verdict)
    ("k02a", 1297036692683751424, 68157440, 87, 1, 9106337, 4991527, "win"),
    ("l1a", 13019119616, 16448, 116, 2, 7660602, 3951175, "loss"),
]

def parse_raw(key):
    """Parse the jsreplay replica row from a batch-7 p1 raw; cross-check the p2 twin
    and the batch-keys.json declaration."""
    keys_json = json.load(open(os.path.join(BATCH, "input", "batch-keys.json")))
    kmap = {k["key_id"]: k for k in keys_json["keys"]}
    per_pass = []
    for p in ("p1", "p2"):
        path = os.path.join(BATCH, "output", "raw", f"{key}.{p}.out")
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
    if lo != bk["lo"] or hi != bk["hi"] or legal != bk["legal"]:
        sys.exit(f"ABORT {key}: raw key/legal {lo},{hi},{legal} != batch-keys {bk}")
    return {"key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "replica_result": int(f1[6]), "replica_nodes": int(f1[7])}

def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for key, kind in TARGETS:
        r = parse_raw(key)
        expect = 1 if kind == "win" else 2
        if r["replica_result"] != expect:
            sys.exit(f"ABORT {key}: replica result {r['replica_result']} != expected {expect}")
        r["expect_third"] = expect
        rows.append(r)
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
    rows_json = {"schema": "n11-centralreply-closure-class10324-batch7-thirdimpl-input-v1",
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
