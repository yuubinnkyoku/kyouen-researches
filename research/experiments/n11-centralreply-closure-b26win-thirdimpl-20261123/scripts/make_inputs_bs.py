# make_inputs_bs.py -- machine-derive the Part BS third-impl input CSVs and
# rows.json for the batch-26 (class 1849, Part BQ) WIN row l028 from the
# published batch-26 canonical artifacts (zero hand transcription).
# Fail-closed: any unexpected field aborts.
#
# Adapted from the published Part BM maker (make_inputs_bm.py, sha256
# d560b8cd..., experiment n11-centralreply-closure-b22win-thirdimpl-20261123)
# for the batch-26 canonical publication; every gate adapted honestly to the
# batch-26 published formats: the batch-26 canonical status.log carries
# 31 PASS lines (30 LOSS rows + the l028 WIN row), exactly 1 runner WIN-HALT
# line, 10 P1/P2-TRUNCATED-RETRY bookkeeping lines and nothing else
# (the batch-2x 2-line battery is replaced by this 42-line battery), the
# published batch-26 row-audit-winhalt.json battery (win_rows ["l028"],
# fragment l035 not evidence, unprobed_count 22), and README-b26
# result-phrase checks.
#
# Sources (all commit-pinned raw fetches of the PUBLISHED canonical batch-26
# publication; local mirrors sha-verified against their published shas):
#  - sources/raw/l028.{p1,p2}.out -- the published batch-26 replica WIN
#    outputs (canonical outputs commit 32fbe3bb99).
#  - sources/status-b26.log -- the published batch-26 runner status.log
#    (canonical sha256 4e167469...).
#  - sources/row-audit-winhalt-b26.json -- the published batch-26 winhalt
#    row audit (canonical sha256 8c91b134...).
#  - sources/batch-keys-b26.json -- published batch-26 input declaration
#    (53 keys, class 1849, sha256 f1ea43ae...).
#  - sources/README-b26.md -- published batch-26 README (9eda46aff1,
#    sha256 602fb209...).
#  - sources/published-input/l028.input.csv -- published batch-26 per-key
#    input CSV (scaffold commit 309386d578; sha256 52d79efc...).
#  - sources/published-input-bf/{k02a,l1a,ng1,ng2}.input.csv -- published
#    Part BF anchor/negative input CSVs (byte-equality-verified here in
#    this experiment against the sha pins; provenance chain AR -> BF ->
#    BK -> BM -> BS).
#
# NOTE: verdicts are NOT consumed anywhere; this experiment is verdict-level
# corroboration literature only. The standard 11x11 empty board, the 19
# central-reply roots, class 1849, class 13342 and every key remain UNKNOWN.
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")

PIN_BS_B26 = "f1ea43aef6ee06c918885a9007ad3f347d96aa198180e87bf3eb14d783304cdd"
PIN_STATUS_B26 = "4e167469a29cb00a41bd9c5e22b58d30de8e03dd1419440cc7b0f77148b87f14"
PIN_README_B26 = "602fb2092923e5e5f56cabd7478e56139a9313116000d55831c51a1fd84a09c0"
PIN_ROWAUDIT_B26 = "8c91b1342d82f99b95800af0093d8459b6a3ca5fca5c41c28394aa91cd2de4a4"
PIN_RAW = {
    "l028.p1": "1e499c11e415e2bdbeab19280c97b5cf8591b14f357136ff864f016dc3090935",
    "l028.p2": "1e499c11e415e2bdbeab19280c97b5cf8591b14f357136ff864f016dc3090935",
}
PIN_PUB_INPUT = {
    "l028": "52d79efc91f4b12935e9fcf6529e3b53a896d30060e8ef5af5503fc7e6fca21e",
}
PIN_PUB_INPUT_BF = {
    "k02a": "b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887",
    "l1a": "e13d2a6c5bbaa34833dcaf8bfaaa91f99393942281f001552cb8af49cca8c98a",
    "ng1": "8e64b9ade1c04122ac4bdc5fa5129b5fca6cfac742ed92cb149f9ffb80ad0b09",
    "ng2": "f19cd5a30b0b868f0a0c7f12a6c47376c8ceb6e862f5c769fb14bdf74e8997dc",
}

TARGETS = ["l028"]
EXPECT_S5 = {"l028": 81011}
EXPECT_REPLICA = {"l028": 4893014}  # published 2-pass node-exact WIN row
# batch-26 canonical status.log: 31 PASS lines + 1 WIN-HALT + 10 truncated-retry
STATUS_PASS_NODES = {"l028": 4893014}
STATUS_EXPECT_LINES = 42
STATUS_EXPECT_PASS = 31
STATUS_EXPECT_RETRY = 10

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
    # status.log cross-verification (batch-26 canonical format): exactly one
    # PASS line for the key, budget,result,nodes matching the raw row, one
    # runner WIN-HALT line for the key, and no other runner lines exist.
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
    n_winhalt = sum(1 for l in status_text.splitlines() if len(l.split()) >= 3 and l.split()[2] == "WIN-HALT")
    if n_winhalt != 1:
        sys.exit(f"ABORT status.log WIN-HALT runner lines != 1: {n_winhalt}")
    return {"key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "replica_result": result, "replica_nodes": nodes}

def main():
    os.makedirs(OUT, exist_ok=True)
    # -- source pins
    for fname, pin in (("batch-keys-b26.json", PIN_BS_B26), ("status-b26.log", PIN_STATUS_B26),
                       ("README-b26.md", PIN_README_B26), ("row-audit-winhalt-b26.json", PIN_ROWAUDIT_B26)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    for k, pin in PIN_RAW.items():
        got = sha256(os.path.join(SRC, "raw", k + ".out"))
        if got != pin:
            sys.exit(f"ABORT raw {k} sha {got} != pin {pin}")
    bk26 = json.load(open(os.path.join(SRC, "batch-keys-b26.json")))
    if int(bk26["class_index"]) != 1849:
        sys.exit(f"ABORT class_index {bk26.get('class_index')}")
    k26 = {k["key_id"]: k for k in bk26["keys"]}
    if len(k26) != 53:
        sys.exit(f"ABORT batch keys count {len(k26)} != 53")
    # -- status log battery gates (published batch-26 canonical runner log):
    #    42 lines = 31 PASS (30 LOSS + the l028 WIN pass line) + 1 WIN-HALT +
    #    10 P1/P2-TRUNCATED-RETRY bookkeeping lines; PASS key set must equal
    #    the row-audit loss_rows + win_rows exactly (machine cross-derivation).
    slog = open(os.path.join(SRC, "status-b26.log")).read()
    lines = [l for l in slog.splitlines() if l.strip()]
    if len(lines) != STATUS_EXPECT_LINES:
        sys.exit(f"ABORT status-b26.log line count {len(lines)} != {STATUS_EXPECT_LINES}")
    kinds = {}
    for ln in lines:
        toks = ln.split()
        kinds[toks[2]] = kinds.get(toks[2], 0) + 1
    if kinds.get("PASS") != STATUS_EXPECT_PASS:
        sys.exit(f"ABORT status-b26.log PASS lines {kinds.get('PASS')} != {STATUS_EXPECT_PASS}")
    n_winhalt = sum(1 for l in lines if l.split()[2] == "WIN-HALT")
    if n_winhalt != 1:
        sys.exit(f"ABORT status-b26.log WIN-HALT lines {n_winhalt} != 1")
    n_retry = sum(1 for l in lines if l.split()[2] in ("P1-TRUNCATED-RETRY", "P2-TRUNCATED-RETRY"))
    if n_retry != STATUS_EXPECT_RETRY:
        sys.exit(f"ABORT status-b26.log truncated-retry lines {n_retry} != {STATUS_EXPECT_RETRY}")
    if kinds.get("PASS", 0) + n_winhalt + n_retry != len(lines):
        sys.exit(f"ABORT status-b26.log carries unexpected line kinds: {sorted(kinds)}")
    pass_keys = [l.split()[1] for l in lines if l.split()[2] == "PASS"]
    if len(pass_keys) != len(set(pass_keys)):
        sys.exit(f"ABORT status-b26.log duplicate PASS keys")
    # -- published row-audit-winhalt battery gates (batch-26 halt-time audit)
    ra = json.load(open(os.path.join(SRC, "row-audit-winhalt-b26.json")))
    if ra.get("schema") != "n11-centralreply-closure-class1849-batch26-rowaudit-winhalt-v1":
        sys.exit(f"ABORT row-audit schema {ra.get('schema')}")
    if ra.get("class_index") != 1849 or ra.get("probed") != 31 or ra.get("pass_rows") != 30:
        sys.exit(f"ABORT row-audit header {ra.get('class_index')},{ra.get('probed')},{ra.get('pass_rows')}")
    if ra.get("win_rows") != ["l028"]:
        sys.exit(f"ABORT row-audit win_rows {ra.get('win_rows')}")
    if ra.get("mismatches") != 0 or ra.get("exhausted_rows"):
        sys.exit(f"ABORT row-audit mismatches/exhausted {ra.get('mismatches')},{ra.get('exhausted_rows')}")
    if ra.get("unprobed_count") != 22:
        sys.exit(f"ABORT row-audit unprobed_count {ra.get('unprobed_count')}")
    if ra.get("derived_state") is not True:
        sys.exit(f"ABORT row-audit derived_state {ra.get('derived_state')}")
    frag = ra.get("fragment_keys") or {}
    if set(frag) != {"l035"} or frag.get("l035", {}).get("evidence") is not False \
            or frag.get("l035", {}).get("probed") is not False:
        sys.exit(f"ABORT row-audit fragment_keys {frag}")
    if ra.get("input_sha256") != PIN_BS_B26:
        sys.exit("ABORT row-audit input_sha256 != batch-keys pin")
    expected = set(ra.get("loss_rows", [])) | set(ra.get("win_rows", []))
    if set(pass_keys) != expected:
        missing = expected - set(pass_keys)
        extra = set(pass_keys) - expected
        sys.exit(f"ABORT status PASS keys != row-audit rows: missing {sorted(missing)} extra {sorted(extra)}")
    # every non-target PASS row must be result 2 (LOSS honest label)
    for l in lines:
        toks = l.split()
        if toks[2] == "PASS" and toks[1] != "l028":
            pl = toks[3].split(",")
            if pl[0] != "15000000" or pl[1] != "2":
                sys.exit(f"ABORT status-b26.log {toks[1]} PASS line {pl} is not a LOSS row")
    # -- README results battery gates (published batch-26 README)
    rd = open(os.path.join(SRC, "README-b26.md")).read()
    if "l028 WIN (honest label)" not in rd:
        sys.exit("ABORT README lacks the l028 WIN results line")
    if "4,893,014" not in rd:
        sys.exit("ABORT README lacks the l028 node count 4,893,014")
    if "28番目の unconsumed" not in rd or "closure WIN 候補" not in rd:
        sys.exit("ABORT README lacks the 28th-unconsumed-candidate route statement")
    if "rank 26 class 13342" not in rd or "batch-27" not in rd:
        sys.exit("ABORT README lacks the batch-27 pointer route statement")
    # -- per-target raw cross-verification
    rows = []
    for key in TARGETS:
        bk = k26.get(key)
        if bk is None or int(bk["s5_index"]) != EXPECT_S5[key]:
            sys.exit(f"ABORT {key}: batch-26 s5_index {bk and bk.get('s5_index')}")
        r = parse_raw(key, k26, slog)
        r["source"] = "part-bq-batch26-win"
        r["s5_index"] = int(bk["s5_index"])
        r["membership_class_count"] = int(bk["membership_class_count"])
        r["expect_third"] = 1
        rows.append(r)
    # -- anchors/negatives (published constants, AR->BF->BK->BM->BS provenance chain)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b26win-thirdimpl-input-v1",
                 "sources": {
                     "b26": ("sources/raw l028.p1/p2 + sources/status-b26.log + sources/row-audit-winhalt-b26.json + "
                             "batch-keys-b26.json + published batch-26 (Part BQ) canonical outputs, publication "
                             "commits 8e64ba1c (declaration) / 309386d578 (scaffold+inputs) / 32fbe3bb99 "
                             "(raws+status+row-audit) / 9eda46aff1 (README+MANIFEST), commit-pinned raw fetch; "
                             "batch-26 batch-keys sha256 f1ea43ae.."),
                     "b26_batch_keys_sha256": PIN_BS_B26,
                     "b26_row_audit_winhalt_sha256": PIN_ROWAUDIT_B26,
                     "anchors": ("published Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK/BM anchor/negative values, "
                                 "input CSVs byte-equality-checked against the published Part BF experiment "
                                 "(provenance chain AR -> BF -> BK -> BM -> BS)")},
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
    print("BS-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"])

if __name__ == "__main__":
    main()
