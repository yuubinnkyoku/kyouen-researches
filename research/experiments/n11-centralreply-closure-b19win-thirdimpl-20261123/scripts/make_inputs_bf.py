# make_inputs_bf.py -- machine-derive the Part BF third-impl input CSVs and
# rows.json for the batch-19 (class 16513, Part BE) WIN rows w001/w002 from
# the published batch-19 artifacts (zero hand transcription).
# Fail-closed: any unexpected field aborts.
#
# Sources (all fetched from the repo main raw CDN, commit-pinned to the
# published batch-19 publication commits; MANIFEST-sha256.txt 74 file rows
# commit 9719e926 verified byte-identical local vs remote):
#  - sources/raw/w001.{p1,p2}.out + raw/w002.{p1,p2}.out -- the published
#    batch-19 replica WIN outputs (raws published at commit 51e73082).
#  - sources/status-b19.log -- the published batch-19 runner status.log
#    (sha256 e3a9e5b4... per the published MANIFEST).
#  - sources/batch-keys-b19.json -- published batch-19 input declaration
#    (53 keys, class 16513, sha256 9609aaf3...).
#  - sources/README-b19.md -- published batch-19 README (results section,
#    sha256 29c7ea51...).
#  - sources/published-input/{w001,w002}.input.csv -- published batch-19
#    per-key input CSVs (byte-equality asserted for both targets).
#  - sources/published-input-ar/{k02a,l1a,ng1,ng2}.input.csv -- published
#    Part AR third-impl anchor/negative input CSVs (byte-equality asserted).
#
# Anchors/negatives identical to Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ (same
# published third-impl values).
# NOTE: verdicts are NOT consumed anywhere; this experiment is verdict-level
# corroboration literature only. The standard 11x11 empty board, the 19
# central-reply roots, class 16513 and every key remain UNKNOWN.
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")

PIN_BK_B19 = "9609aaf3116f2ba80c206ae66b09249af1855d509d17be588911e6ab72e53d50"
PIN_STATUS_B19 = "e3a9e5b41b0dd763e22d39da68cf92fe37d5869912053000f06ef8239b4d197e"
PIN_README_B19 = "29c7ea51ba035a2b5b3fe58d96365b714bb3700a17066c3a7025dfeb00534067"
PIN_RAW = {
    "w001.p1": "8cf13d13fb08e842c05610bae0d5fe0add92bd573597d212316beb01c51526d6",
    "w001.p2": "8cf13d13fb08e842c05610bae0d5fe0add92bd573597d212316beb01c51526d6",
    "w002.p1": "1faf8d15ed1fbcff2db775f87f7b177db4c76a1a7e55ca22fd58666428c2a948",
    "w002.p2": "feb8475bf5f25154d7625a9041b4a6ea7e70fec74d98bdfea83e36a84cbda72a",
}
# NOTE: w001 p1/p2 raws are byte-identical (both passes wall_s 67 -> identical
# output bytes incl. the wall_s field); w002 p1/p2 differ only in wall_s
# (81 vs 67). Node-exactness across passes is asserted field-wise below
# (fields 3,6,7,9,10 - never wall_s), matching the published WIN-ROW-DETAIL
# "wall_s 67/67" and "wall_s 81/67" records.
PIN_PUB_INPUT = {
    "w001": "f232a593b671e9b441037f71a63f667fbfe7e0b50de7a5fae2edc134c073c0f7",
    "w002": "574a4124eba600b2474e0c5ab6adf1941c90e4796946237da305444d5248ec77",
}
PIN_PUB_INPUT_AR = {
    "k02a": "b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887",
    "l1a": "e13d2a6c5bbaa34833dcaf8bfaaa91f99393942281f001552cb8af49cca8c98a",
    "ng1": "8e64b9ade1c04122ac4bdc5fa5129b5fca6cfac742ed92cb149f9ffb80ad0b09",
    "ng2": "f19cd5a30b0b868f0a0c7f12a6c47376c8ceb6e862f5c769fb14bdf74e8997dc",
}

TARGETS = ["w001", "w002"]
EXPECT_S5 = {"w001": 63802, "w002": 109169}
EXPECT_REPLICA = {"w001": 6639780, "w002": 7738714}  # published 2-pass node-exact WIN rows
HOLDER_LINE = {  # published WIN-ROW-DETAIL holder-class records (cost-child graph relation)
    "w001": "1363 (unknown), 16513 (unknown)",
    "w002": "2901 (unknown), 16513 (unknown)",
}

ANCHORS = [
    # (key_id, lo, hi, legal, third-impl published result, expansions, ttHits, expect_verdict)
    ("k02a", 1297036692683751424, 68157440, 87, 1, 9106337, 4991527, "win"),
    ("l1a", 13019119616, 16448, 116, 2, 7660602, 3951175, "loss"),
]
NEGATIVES = [
    {"key_id": "ng1", "lo": 1297036692683751424, "hi": 68157440, "legal": 88,
     "stones": 5, "why": "legal+1 vs derived 87"},
    {"key_id": "ng2", "lo": 1297036692683751424, "hi": 68157440, "legal": 87,
     "stones": 6, "why": "stones 6 vs actual 5"},
]

def sha256(path):
    import hashlib
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()

def parse_replay_csv(path):
    got = []
    done = False
    with open(path) as fh:
        for line in fh:
            if line.startswith("replay,"):
                got.append(line.strip())
            if line.startswith("# replay_done"):
                done = True
    if len(got) != 1 or not done:
        sys.exit(f"ABORT raw parse {path}: {len(got)} replay rows, replay_done={done}")
    return got[0].split(",")

def parse_raw(key, kmap, status_text):
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
    if f1[1] != "0":
        sys.exit(f"ABORT {key}: unexpected replay id {f1[1]}")
    lo, hi, legal = int(f1[9]), int(f1[10]), int(f1[3])
    bk = kmap[key]
    if int(bk["lo"]) != lo or int(bk["hi"]) != hi or int(bk["legal"]) != legal:
        sys.exit(f"ABORT {key}: raw key/legal {lo},{hi},{legal} != batch-keys {bk}")
    result, nodes = int(f1[6]), int(f1[7])
    if result != 1:
        sys.exit(f"ABORT {key}: expected in-budget WIN (result 1) row, got result={result}")
    if nodes >= 15000000:
        sys.exit(f"ABORT {key}: WIN row at/near budget: nodes={nodes}")
    if nodes != EXPECT_REPLICA[key]:
        sys.exit(f"ABORT {key}: replica nodes {nodes} != published {EXPECT_REPLICA[key]}")
    # status.log cross-verification: PASS line + WIN-HALT + WIN-ROW-DETAIL
    stat = None
    for line in status_text.splitlines():
        toks = line.split()
        if len(toks) >= 4 and toks[1] == key and toks[2] == "PASS":
            if stat is not None:
                sys.exit(f"ABORT {key}: multiple PASS lines in status log")
            stat = toks[3].split(",")
    if stat is None:
        sys.exit(f"ABORT {key}: no PASS line in status log")
    if stat[0] != "15000000" or int(stat[1]) != result or int(stat[2]) != nodes:
        sys.exit(f"ABORT {key}: status.log {stat} != raw ({result},{nodes})")
    if f"{key} WIN-HALT" not in status_text:
        sys.exit(f"ABORT {key}: no WIN-HALT line in status log")
    # batch-19 WIN-ROW-DETAIL format (differs from batch-18/AZ: s5 index sits
    # between result and keys):
    # ... nodes N == p2 nodes N (...wall_s X/Y), legal L, budget B, result R,
    #     s5 index S, keys lo/hi, ...
    m = re.search(rf"WIN-ROW-DETAIL {key} .*nodes (\d+) == p2 nodes \d+ "
                  rf".*legal (\d+), budget (\d+), result (\d+), s5 index (\d+), keys (\d+)/(\d+)",
                  status_text)
    if m is None:
        sys.exit(f"ABORT {key}: no WIN-ROW-DETAIL line in status log")
    if (int(m.group(1)) != nodes or int(m.group(2)) != legal or int(m.group(3)) != 15000000
            or int(m.group(4)) != result or int(m.group(5)) != EXPECT_S5[key]
            or int(m.group(6)) != lo or int(m.group(7)) != hi):
        sys.exit(f"ABORT {key}: WIN-ROW-DETAIL {m.groups()} != raw/batch-keys")
    if HOLDER_LINE[key] not in status_text:
        sys.exit(f"ABORT {key}: WIN-ROW-DETAIL holder-class record missing")
    return {"key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "replica_result": result, "replica_nodes": nodes}

def main():
    os.makedirs(OUT, exist_ok=True)
    # -- source pins
    for fname, pin in (("batch-keys-b19.json", PIN_BK_B19), ("status-b19.log", PIN_STATUS_B19),
                       ("README-b19.md", PIN_README_B19)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    for k, pin in PIN_RAW.items():
        got = sha256(os.path.join(SRC, "raw", k + ".out"))
        if got != pin:
            sys.exit(f"ABORT raw {k} sha {got} != pin {pin}")
    bk19 = json.load(open(os.path.join(SRC, "batch-keys-b19.json")))
    if int(bk19["class_index"]) != 16513:
        sys.exit(f"ABORT class_index {bk19.get('class_index')}")
    k19 = {k["key_id"]: k for k in bk19["keys"]}
    if len(k19) != 53:
        sys.exit(f"ABORT batch keys count {len(k19)} != 53")
    # -- status log battery gates (published batch-19 runner log)
    slog = open(os.path.join(SRC, "status-b19.log")).read()
    if "VAL-GATE 4/4 node-exact this-host re-verified" not in slog:
        sys.exit("ABORT status-b19.log lacks the VAL-GATE 4/4 line")
    if "EXECUTION-HALTED batch-19 stopped at first wave" not in slog:
        sys.exit("ABORT status-b19.log lacks the EXECUTION-HALTED line")
    if "2/53 keys probed, 51 keys UNPROBED" not in slog:
        sys.exit("ABORT status-b19.log lacks the 51-unprobed honesty line")
    if "Unconsumed closure WIN candidates now 19" not in slog:
        sys.exit("ABORT status-b19.log lacks the 19-candidates line")
    # total WIN-HALT mentions: w001 + w002 runner lines
    if len([l for l in slog.splitlines() if l.endswith(" WIN-HALT")]) != 2:
        sys.exit("ABORT status-b19.log WIN-HALT runner lines != 2")
    # -- README results battery gates (published batch-19 README)
    rd = open(os.path.join(SRC, "README-b19.md")).read()
    for key in TARGETS:
        if f"**{key}: WIN (result 1)**" not in rd:
            sys.exit(f"ABORT README lacks the {key} WIN results line")
        nn = f"{EXPECT_REPLICA[key]:,}"
        if nn not in rd:
            sys.exit(f"ABORT README lacks the {key} node count {nn}")
    # -- per-target raw cross-verification
    rows = []
    for key in TARGETS:
        bk = k19.get(key)
        if bk is None or int(bk["s5_index"]) != EXPECT_S5[key]:
            sys.exit(f"ABORT {key}: batch-19 s5_index {bk and bk.get('s5_index')}")
        r = parse_raw(key, k19, slog)
        r["source"] = "part-be-batch19-win"
        r["s5_index"] = int(bk["s5_index"])
        r["membership_class_count"] = int(bk["membership_class_count"])
        r["expect_third"] = 1
        rows.append(r)
    # -- anchors/negatives (published constants, AR-identical)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b19win-thirdimpl-input-v1",
                 "sources": {
                     "b19": ("sources/raw w001/w002 4 files + sources/status-b19.log + batch-keys-b19.json + "
                             "published batch-19 (Part BE) outputs, publication commits 49c3bea7 "
                             "(scaffold+inputs) / 51e73082 (raws+status) / 9719e926 (README+MANIFEST), "
                             "commit-pinned raw fetch; batch-19 batch-keys sha256 9609aaf3.."),
                     "b19_batch_keys_sha256": PIN_BK_B19,
                     "anchors": ("published Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ anchor/negative values, "
                                 "input CSVs byte-equality-checked against the published Part AR experiment")},
                 "consumed_into_canonical_cache": False,
                 "targets": rows, "anchors": anchor_rows, "negatives": NEGATIVES}
    with open(os.path.join(OUT, "rows.json"), "w") as fh:
        json.dump(rows_json, fh, indent=1)
        fh.write("\n")
    # -- derived-vs-published input CSV byte-equality gates + input emission
    for r in rows:
        csv = f"target,0,5,{r['lo']},{r['hi']},{r['legal']},0,0,0,0,0\n"
        pub = open(os.path.join(SRC, "published-input", f"{r['key_id']}.input.csv")).read()
        if csv != pub:
            sys.exit(f"ABORT {r['key_id']}: derived CSV {csv!r} != published {pub!r}")
        if sha256(os.path.join(SRC, "published-input", f"{r['key_id']}.input.csv")) != PIN_PUB_INPUT[r["key_id"]]:
            sys.exit(f"ABORT {r['key_id']}: published input CSV sha mismatch")
        with open(os.path.join(OUT, f"{r['key_id']}.input.csv"), "w") as fh:
            fh.write(csv)
    for r in anchor_rows:
        csv = f"target,0,5,{r['lo']},{r['hi']},{r['legal']},0,0,0,0,0\n"
        pub = open(os.path.join(SRC, "published-input-ar", f"{r['key_id']}.input.csv")).read()
        if csv != pub:
            sys.exit(f"ABORT anchor {r['key_id']}: derived CSV {csv!r} != published Part AR {pub!r}")
        if sha256(os.path.join(SRC, "published-input-ar", f"{r['key_id']}.input.csv")) != PIN_PUB_INPUT_AR[r["key_id"]]:
            sys.exit(f"ABORT anchor {r['key_id']}: published Part AR CSV sha mismatch")
        with open(os.path.join(OUT, f"{r['key_id']}.input.csv"), "w") as fh:
            fh.write(csv)
    for r in NEGATIVES:
        csv = f"target,0,{r['stones']},{r['lo']},{r['hi']},{r['legal']},0,0,0,0,0\n"
        pub = open(os.path.join(SRC, "published-input-ar", f"{r['key_id']}.input.csv")).read()
        if csv != pub:
            sys.exit(f"ABORT negative {r['key_id']}: derived CSV {csv!r} != published Part AR {pub!r}")
        if sha256(os.path.join(SRC, "published-input-ar", f"{r['key_id']}.input.csv")) != PIN_PUB_INPUT_AR[r["key_id"]]:
            sys.exit(f"ABORT negative {r['key_id']}: published Part AR CSV sha mismatch")
        with open(os.path.join(OUT, f"{r['key_id']}.input.csv"), "w") as fh:
            fh.write(csv)
    print("BF-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"])

if __name__ == "__main__":
    main()
