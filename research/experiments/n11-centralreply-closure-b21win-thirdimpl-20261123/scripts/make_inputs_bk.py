# make_inputs_bk.py -- machine-derive the Part BK third-impl input CSVs and
# rows.json for the batch-21 (class 12643, Part BJ) WIN row a003 from the
# published batch-21 canonical artifacts (zero hand transcription).
# Fail-closed: any unexpected field aborts.
#
# Adapted from the published Part BF maker (make_inputs_bf.py, sha256
# 20d52c75..., experiment n11-centralreply-closure-b19win-thirdimpl-20261123)
# for the batch-21 canonical publication; every gate adapted to the batch-21
# published formats honestly (no WIN-ROW-DETAIL lines exist in the batch-21
# canonical status.log; the batch-21 status.log is exactly 5 runner lines).
#
# Sources (all commit-pinned raw fetches of the PUBLISHED canonical batch-21
# publication; local mirrors sha-verified against the publish-time MANIFEST):
#  - sources/raw/a003.{p1,p2}.out -- the published batch-21 replica WIN outputs
#    (canonical outputs commit 0022c8c5).
#  - sources/status-b21.log -- the published batch-21 runner status.log
#    (canonical sha256 0c5d691a...).
#  - sources/batch-keys-b21.json -- published batch-21 input declaration
#    (53 keys, class 12643, sha256 1f9346a7...).
#  - sources/README-b21.md -- published batch-21 README (a38153a8,
#    sha256 27dd1abf...).
#  - sources/published-input/a003.input.csv -- published batch-21 per-key
#    input CSV (scaffold commit 85d0c4d7; MANIFEST a38153a8 row 3a3cae78...).
#  - sources/published-input-bf/{k02a,l1a,ng1,ng2}.input.csv -- published
#    Part BF anchor/negative input CSVs (themselves byte-equality-checked
#    against Part AR at BF time; provenance chain AR -> BF -> BK).
#
# NOTE: verdicts are NOT consumed anywhere; this experiment is verdict-level
# corroboration literature only. The standard 11x11 empty board, the 19
# central-reply roots, class 12643 and every key remain UNKNOWN.
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")

PIN_BK_B21 = "1f9346a7027e95b162f27b933bddec05151473d87ab7ed35832619026ae6759d"
PIN_STATUS_B21 = "0c5d691a215e1b56663b2ced52367792343d1da7386a1086b24b0ae7e129cbb9"
PIN_README_B21 = "27dd1abf26036c1b1a6e16ea07476caf3512949558ef1b28053deb27ca8dc17f"
PIN_RAW = {
    "a003.p1": "7f272ce36515ada2b15ada75cc57331a7788f15bd952a7f386087a0b4470a4f4",
    "a003.p2": "b8b19e6170a4bd2c64cb743da1e67f821a5b67c07ede3caeffcc1fb9ec9ebbce",
}
PIN_PUB_INPUT = {
    "a003": "3a3cae78016f1262604c92ec3652275be23a71942e7e0773629b097791c6bedd",
}
PIN_PUB_INPUT_BF = {
    "k02a": "b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887",
    "l1a": "e13d2a6c5bbaa34833dcaf8bfaaa91f99393942281f001552cb8af49cca8c98a",
    "ng1": "8e64b9ade1c04122ac4bdc5fa5129b5fca6cfac742ed92cb149f9ffb80ad0b09",
    "ng2": "f19cd5a30b0b868f0a0c7f12a6c47376c8ceb6e862f5c769fb14bdf74e8997dc",
}

TARGETS = ["a003"]
EXPECT_S5 = {"a003": 115192}
EXPECT_REPLICA = {"a003": 5021280}  # published 2-pass node-exact WIN row
# batch-21 canonical status.log carries exactly 4 PASS lines + 1 WIN-HALT line
STATUS_PASS_NODES = {"a001": 2392778, "a002": 6755079, "a003": 5021280, "a004": 4151964}

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
    # status.log cross-verification (batch-21 canonical format): exactly one
    # PASS line for the key, budget,result,nodes matching the raw row, one
    # runner WIN-HALT line for the key, and no other keys carry WIN-HALT.
    stat = None
    pass_lines = []
    for line in status_text.splitlines():
        toks = line.split()
        if len(toks) >= 4 and toks[1] == key and toks[2] == "PASS":
            pass_lines.append(toks[3].split(","))
        if len(toks) >= 3 and toks[1] == key and toks[2] == "WIN-HALT":
            stat = True
    if len(pass_lines) != 1:
        sys.exit(f"ABORT {key}: PASS lines for key != 1 in status log")
    pl = pass_lines[0]
    if pl[0] != "15000000" or int(pl[1]) != result or int(pl[2]) != nodes:
        sys.exit(f"ABORT {key}: status.log {pl} != raw ({result},{nodes})")
    if stat is not True:
        sys.exit(f"ABORT {key}: no WIN-HALT line in status log")
    n_winhalt = sum(1 for l in status_text.splitlines() if l.split()[2:3] == ["WIN-HALT"] if len(l.split()) >= 3)
    if n_winhalt != 1:
        sys.exit(f"ABORT status.log WIN-HALT runner lines != 1: {n_winhalt}")
    return {"key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "replica_result": result, "replica_nodes": nodes}

def main():
    os.makedirs(OUT, exist_ok=True)
    # -- source pins
    for fname, pin in (("batch-keys-b21.json", PIN_BK_B21), ("status-b21.log", PIN_STATUS_B21),
                       ("README-b21.md", PIN_README_B21)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    for k, pin in PIN_RAW.items():
        got = sha256(os.path.join(SRC, "raw", k + ".out"))
        if got != pin:
            sys.exit(f"ABORT raw {k} sha {got} != pin {pin}")
    bk21 = json.load(open(os.path.join(SRC, "batch-keys-b21.json")))
    if int(bk21["class_index"]) != 12643:
        sys.exit(f"ABORT class_index {bk21.get('class_index')}")
    k21 = {k["key_id"]: k for k in bk21["keys"]}
    if len(k21) != 53:
        sys.exit(f"ABORT batch keys count {len(k21)} != 53")
    # -- status log battery gates (published batch-21 canonical runner log):
    #    exactly 5 runner lines: 4 PASS + 1 WIN-HALT, no truncation retries,
    #    no exhaustion, the halted key is a003.
    slog = open(os.path.join(SRC, "status-b21.log")).read()
    lines = [l for l in slog.splitlines() if l.strip()]
    if len(lines) != 5:
        sys.exit(f"ABORT status-b21.log line count {len(lines)} != 5")
    for ln in lines:
        toks = ln.split()
        if toks[2] not in ("PASS", "WIN-HALT"):
            sys.exit(f"ABORT status-b21.log unexpected line kind: {ln}")
    n_pass = sum(1 for l in lines if l.split()[2] == "PASS")
    if n_pass != 4:
        sys.exit(f"ABORT status-b21.log PASS lines {n_pass} != 4")
    pass_nodes = {}
    for l in lines:
        toks = l.split()
        if toks[2] == "PASS":
            pass_nodes[toks[1]] = toks[3].split(",")
    for kid, nodes in STATUS_PASS_NODES.items():
        if kid not in pass_nodes:
            sys.exit(f"ABORT status-b21.log lacks the {kid} PASS line")
        pl = pass_nodes[kid]
        if pl[0] != "15000000" or int(pl[1]) not in (1, 2) or int(pl[2]) != nodes:
            sys.exit(f"ABORT status-b21.log {kid} PASS line {pl} != expected nodes {nodes}")
    if pass_nodes["a001"][1] != "2" or pass_nodes["a002"][1] != "2" or pass_nodes["a003"][1] != "1" or pass_nodes["a004"][1] != "2":
        sys.exit("ABORT status-b21.log PASS result labels unexpected")
    if "a003 WIN-HALT" not in slog:
        sys.exit("ABORT status-b21.log lacks the a003 WIN-HALT runner line")
    # -- README results battery gates (published batch-21 README)
    rd = open(os.path.join(SRC, "README-b21.md")).read()
    if "a003 WIN (result 1" not in rd:
        sys.exit("ABORT README lacks the a003 WIN results line")
    if "5,021,280" not in rd:
        sys.exit("ABORT README lacks the a003 node count 5,021,280")
    if "a001 LOSS (result 2, nodes 2,392,778)" not in rd:
        sys.exit("ABORT README lacks the a001 LOSS results line")
    if "s5 115192" not in rd:
        sys.exit("ABORT README lacks the a003 s5 index route statement")
    # -- per-target raw cross-verification
    rows = []
    for key in TARGETS:
        bk = k21.get(key)
        if bk is None or int(bk["s5_index"]) != EXPECT_S5[key]:
            sys.exit(f"ABORT {key}: batch-21 s5_index {bk and bk.get('s5_index')}")
        r = parse_raw(key, k21, slog)
        r["source"] = "part-bj-batch21-win"
        r["s5_index"] = int(bk["s5_index"])
        r["membership_class_count"] = int(bk["membership_class_count"])
        r["expect_third"] = 1
        rows.append(r)
    # -- anchors/negatives (published constants, AR->BF provenance chain)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b21win-thirdimpl-input-v1",
                 "sources": {
                     "b21": ("sources/raw a003.p1/p2 + sources/status-b21.log + batch-keys-b21.json + "
                             "published batch-21 (Part BJ) canonical outputs, publication commits "
                             "85d0c4d7 (scaffold+inputs) / 0022c8c5 (raws+status+row-audit) / "
                             "a38153a8 (README+MANIFEST), commit-pinned raw fetch; batch-21 "
                             "batch-keys sha256 1f9346a7.."),
                     "b21_batch_keys_sha256": PIN_BK_B21,
                     "anchors": ("published Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF anchor/negative "
                                 "values, input CSVs byte-equality-checked against the published Part BF "
                                 "experiment (provenance chain AR -> BF -> BK)")},
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
        pub = open(os.path.join(SRC, "published-input-bf", f"{r['key_id']}.input.csv")).read()
        if csv != pub:
            sys.exit(f"ABORT anchor {r['key_id']}: derived CSV {csv!r} != published Part BF {pub!r}")
        if sha256(os.path.join(SRC, "published-input-bf", f"{r['key_id']}.input.csv")) != PIN_PUB_INPUT_BF[r["key_id"]]:
            sys.exit(f"ABORT anchor {r['key_id']}: published Part BF CSV sha mismatch")
        with open(os.path.join(OUT, f"{r['key_id']}.input.csv"), "w") as fh:
            fh.write(csv)
    for r in NEGATIVES:
        csv = f"target,0,{r['stones']},{r['lo']},{r['hi']},{r['legal']},0,0,0,0,0\n"
        pub = open(os.path.join(SRC, "published-input-bf", f"{r['key_id']}.input.csv")).read()
        if csv != pub:
            sys.exit(f"ABORT negative {r['key_id']}: derived CSV {csv!r} != published Part BF {pub!r}")
        if sha256(os.path.join(SRC, "published-input-bf", f"{r['key_id']}.input.csv")) != PIN_PUB_INPUT_BF[r["key_id"]]:
            sys.exit(f"ABORT negative {r['key_id']}: published Part BF CSV sha mismatch")
        with open(os.path.join(OUT, f"{r['key_id']}.input.csv"), "w") as fh:
            fh.write(csv)
    print("BK-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"])

if __name__ == "__main__":
    main()
