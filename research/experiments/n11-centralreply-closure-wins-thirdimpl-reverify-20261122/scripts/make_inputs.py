# make_inputs.py -- machine-derive the target input CSVs from the published batch
# raws (no hand transcription). Fail-closed: any unexpected field aborts.
#
# Sources (published, pinned):
#  - closure batch raws  _19root-refresh-kit/batch*/output/raw/<key>.p1.out
#    (jsreplay replica 2-pass node-exact rows; these raws are byte-identical to the
#     published experiment dirs of batches 1/3/5 on main)
#  - third-impl witness anchors (k02 / l1) from the published
#    n11-third-implementation experiment witness-outputs.txt
import json, os, re, sys

KIT = "/home/user/knowledge/kyouen-research/_19root-refresh-kit"
LANE3 = "/home/user/knowledge/kyouen-research/_class1297036830122704896-lane-kit"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "input")

WIN_TARGETS = [
    ("b018", "batch16757", "win"),
    ("d002", "batch20421", "win"),
    ("e002", "batch16371", "win"),
    ("f017", "batch12264", "win"),
]
LOSS_SAMPLE = [
    ("d001", "batch20421", "loss"),
    ("d003", "batch20421", "loss"),
    ("d004", "batch20421", "loss"),
    ("e001", "batch16371", "loss"),
    ("f001", "batch12264", "loss"),
    ("f005", "batch12264", "loss"),
    ("f009", "batch12264", "loss"),
    ("f013", "batch12264", "loss"),
    ("f016", "batch12264", "loss"),
    ("f018", "batch12264", "loss"),
]
ANCHORS = [
    # (key_id, lo, hi, legal, third-impl published result, expansions, ttHits, expect_verdict)
    ("k02a", 1297036692683751424, 68157440, 87, 1, 9106337, 4991527, "win"),
    ("l1a", 13019119616, 16448, 116, 2, 7660602, 3951175, "loss"),
]

def parse_raw(path, key):
    """Parse the jsreplay replica row from a published p1 raw; cross-check the p2 twin."""
    per_pass = []
    for p in (f"{path}/{key}.p1.out", f"{path}/{key}.p2.out"):
        if not os.path.isfile(os.path.join(KIT, p)):
            sys.exit(f"ABORT missing raw {p}")
        got = []
        with open(os.path.join(KIT, p)) as fh:
            for line in fh:
                if line.startswith("replay,"):
                    got.append(line.strip())
        if len(got) != 1:
            sys.exit(f"ABORT raw parse {p}: {len(got)} replay rows")
        per_pass.append(got[0].split(","))
    f1, f2 = per_pass
    # actual raw field layout: [0]='replay', [1]=id, [2]=stones, [3]=legal, [4]=is_or,
    # [5]=budget, [6]=result, [7]=nodes, [8]=wall_s, [9]=key_lo, [10]=key_hi
    for i in (3, 6, 7):
        if f1[i] != f2[i]:
            sys.exit(f"ABORT {key}: source raw passes differ at field {i}: {f1[i]} vs {f2[i]}")
    if f1[2] != "5" or f1[4] != "0" or f1[5] != "15000000":
        sys.exit(f"ABORT {key}: unexpected source schema {f1[:6]}")
    return {
        "key_id": key,
        "stones": 5,
        "lo": int(f1[9]),
        "hi": int(f1[10]),
        "legal": int(f1[3]),
        "replica_result": int(f1[6]),
        "replica_nodes": int(f1[7]),
    }

def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for key, batch, kind in WIN_TARGETS + LOSS_SAMPLE:
        r = parse_raw(f"{batch}/output/raw", key)
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
    # negative-gate rows (must GATE_FAIL on derived-vs-declared checks)
    negatives = [
        {"key_id": "ng1", "lo": 1297036692683751424, "hi": 68157440, "legal": 88,
         "stones": 5, "why": "legal+1 vs derived 87"},
        {"key_id": "ng2", "lo": 1297036692683751424, "hi": 68157440, "legal": 87,
         "stones": 6, "why": "stones 6 vs actual 5"},
    ]
    rows_json = {"schema": "n11-centralreply-closure-wins-thirdimpl-input-v1",
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
