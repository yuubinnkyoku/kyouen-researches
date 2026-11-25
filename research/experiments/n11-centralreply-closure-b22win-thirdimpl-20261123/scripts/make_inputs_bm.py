# make_inputs_bm.py -- machine-derive the Part BM third-impl input CSVs and
# rows.json for the batch-22 (class 25835, Part BL) WIN row k002 from the
# published batch-22 canonical artifacts (zero hand transcription).
# Fail-closed: any unexpected field aborts.
#
# Adapted from the published Part BK maker (make_inputs_bk.py, sha256
# e664c4e6..., experiment n11-centralreply-closure-b21win-thirdimpl-20261123)
# for the batch-22 canonical publication; every gate adapted to the batch-22
# published formats honestly: the batch-22 canonical status.log carries exactly
# 2 runner lines (1 k002 PASS + 1 k002 WIN-HALT, the drive halted at the first
# probed key per the pre-registered stop rule), so the batch-21 4-PASS battery
# is replaced by (a) the 2-line status battery, (b) the published batch-22
# row-audit-winhalt.json battery (win_rows [k002], fragment k001 not evidence,
# unprobed_count 52), and (c) README-b22 result-phrase checks.
#
# Sources (all commit-pinned raw fetches of the PUBLISHED canonical batch-22
# publication; local mirrors sha-verified against the publish-time MANIFEST
#  of n11-centralreply-closure-class25835-batch22-20261123):
#  - sources/raw/k002.{p1,p2}.out -- the published batch-22 replica WIN outputs
#    (canonical outputs commit 2ed5b90).
#  - sources/status-b22.log -- the published batch-22 runner status.log
#    (canonical sha256 27dc7e7c...).
#  - sources/row-audit-winhalt-b22.json -- the published batch-22 winhalt
#    row audit (canonical sha256 c6f7585c...).
#  - sources/batch-keys-b22.json -- published batch-22 input declaration
#    (53 keys, class 25835, sha256 b5f567bd...).
#  - sources/README-b22.md -- published batch-22 README (a83da90,
#    sha256 eab65d4f...).
#  - sources/published-input/k002.input.csv -- published batch-22 per-key
#    input CSV (scaffold commit 106c469; MANIFEST a83da90 row 2736d30a...).
#  - sources/published-input-bf/{k02a,l1a,ng1,ng2}.input.csv -- published
#    Part BF anchor/negative input CSVs (themselves byte-equality-checked
#    against Part AR at BF time; provenance chain AR -> BF -> BK -> BM).
#
# NOTE: verdicts are NOT consumed anywhere; this experiment is verdict-level
# corroboration literature only. The standard 11x11 empty board, the 19
# central-reply roots, class 25835, class 12643 and every key remain UNKNOWN.
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")

PIN_BM_B22 = "b5f567bd72835ebfe347d7363f3d244565757deb8e8572b6fb2820625ae39035"
PIN_STATUS_B22 = "27dc7e7c1b98455d9e034e64c506936dd6f38c6705ff3a5796e4f6539168f7b6"
PIN_README_B22 = "eab65d4fc9122b16530d2111ee514825f1e81a12e26ae499f49988cefb963128"
PIN_ROWAUDIT_B22 = "c6f7585cf7b7fcbc6bf1d6a940785cab7773ba0b9a843d1ca151e6bc10539f8d"
PIN_RAW = {
    "k002.p1": "baf468a39630c94e3e5ce3d578ee90d6a70b3a027f5641ebd8b4c724b603b785",
    "k002.p2": "0ef25c4a45ce7207a7cc19f335df22c05aa124af596b6e087b9f60ecc4a17fbb",
}
PIN_PUB_INPUT = {
    "k002": "2736d30abd71bd1b0b6dca46f11410258801b4ab11e1a71f77a83e4adc149570",
}
PIN_PUB_INPUT_BF = {
    "k02a": "b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887",
    "l1a": "e13d2a6c5bbaa34833dcaf8bfaaa91f99393942281f001552cb8af49cca8c98a",
    "ng1": "8e64b9ade1c04122ac4bdc5fa5129b5fca6cfac742ed92cb149f9ffb80ad0b09",
    "ng2": "f19cd5a30b0b868f0a0c7f12a6c47376c8ceb6e862f5c769fb14bdf74e8997dc",
}

TARGETS = ["k002"]
EXPECT_S5 = {"k002": 150241}
EXPECT_REPLICA = {"k002": 10542704}  # published 2-pass node-exact WIN row
# batch-22 canonical status.log carries exactly 1 PASS line + 1 WIN-HALT line
STATUS_PASS_NODES = {"k002": 10542704}

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
    # status.log cross-verification (batch-22 canonical format): exactly one
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
    for fname, pin in (("batch-keys-b22.json", PIN_BM_B22), ("status-b22.log", PIN_STATUS_B22),
                       ("README-b22.md", PIN_README_B22), ("row-audit-winhalt-b22.json", PIN_ROWAUDIT_B22)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    for k, pin in PIN_RAW.items():
        got = sha256(os.path.join(SRC, "raw", k + ".out"))
        if got != pin:
            sys.exit(f"ABORT raw {k} sha {got} != pin {pin}")
    bk22 = json.load(open(os.path.join(SRC, "batch-keys-b22.json")))
    if int(bk22["class_index"]) != 25835:
        sys.exit(f"ABORT class_index {bk22.get('class_index')}")
    k22 = {k["key_id"]: k for k in bk22["keys"]}
    if len(k22) != 53:
        sys.exit(f"ABORT batch keys count {len(k22)} != 53")
    # -- status log battery gates (published batch-22 canonical runner log):
    #    exactly 2 runner lines: 1 PASS (k002) + 1 WIN-HALT (k002), the
    #    pre-registered WIN-HALT stop fired at the first probed key.
    slog = open(os.path.join(SRC, "status-b22.log")).read()
    lines = [l for l in slog.splitlines() if l.strip()]
    if len(lines) != 2:
        sys.exit(f"ABORT status-b22.log line count {len(lines)} != 2")
    for ln in lines:
        toks = ln.split()
        if toks[2] not in ("PASS", "WIN-HALT"):
            sys.exit(f"ABORT status-b22.log unexpected line kind: {ln}")
    n_pass = sum(1 for l in lines if l.split()[2] == "PASS")
    if n_pass != 1:
        sys.exit(f"ABORT status-b22.log PASS lines {n_pass} != 1")
    pass_nodes = {}
    for l in lines:
        toks = l.split()
        if toks[2] == "PASS":
            pass_nodes[toks[1]] = toks[3].split(",")
    for kid, nodes in STATUS_PASS_NODES.items():
        if kid not in pass_nodes:
            sys.exit(f"ABORT status-b22.log lacks the {kid} PASS line")
        pl = pass_nodes[kid]
        if pl[0] != "15000000" or int(pl[1]) != 1 or int(pl[2]) != nodes:
            sys.exit(f"ABORT status-b22.log {kid} PASS line {pl} != expected WIN nodes {nodes}")
    if "k002 WIN-HALT" not in slog:
        sys.exit("ABORT status-b22.log lacks the k002 WIN-HALT runner line")
    # -- published row-audit-winhalt battery gates (batch-22 halt-time audit)
    ra = json.load(open(os.path.join(SRC, "row-audit-winhalt-b22.json")))
    if ra.get("schema") != "n11-centralreply-closure-class25835-batch22-rowaudit-winhalt-v1":
        sys.exit(f"ABORT row-audit schema {ra.get('schema')}")
    if ra.get("class_index") != 25835 or ra.get("probed") != 1 or ra.get("pass_rows") != 0:
        sys.exit(f"ABORT row-audit header {ra.get('class_index')},{ra.get('probed')},{ra.get('pass_rows')}")
    if ra.get("win_rows") != ["k002"]:
        sys.exit(f"ABORT row-audit win_rows {ra.get('win_rows')}")
    if ra.get("mismatches") != 0 or ra.get("exhausted_rows"):
        sys.exit(f"ABORT row-audit mismatches/exhausted {ra.get('mismatches')},{ra.get('exhausted_rows')}")
    if ra.get("unprobed_count") != 52:
        sys.exit(f"ABORT row-audit unprobed_count {ra.get('unprobed_count')}")
    frag = ra.get("fragment_key") or {}
    if frag.get("key_id") != "k001" or frag.get("evidence") is not False or frag.get("probed") is not False:
        sys.exit(f"ABORT row-audit fragment_key {frag}")
    if ra.get("input_sha256") != PIN_BM_B22:
        sys.exit("ABORT row-audit input_sha256 != batch-keys pin")
    # -- README results battery gates (published batch-22 README)
    rd = open(os.path.join(SRC, "README-b22.md")).read()
    if "k002 WIN (honest label)" not in rd:
        sys.exit("ABORT README lacks the k002 WIN results line")
    if "10,542,704" not in rd:
        sys.exit("ABORT README lacks the k002 node count 10,542,704")
    if "21番目の unconsumed closure WIN 候補" not in rd:
        sys.exit("ABORT README lacks the 21st-unconsumed-candidate route statement")
    if "rank 19" not in rd or "class 31600" not in rd:
        sys.exit("ABORT README lacks the batch-23 pointer route statement")
    # -- per-target raw cross-verification
    rows = []
    for key in TARGETS:
        bk = k22.get(key)
        if bk is None or int(bk["s5_index"]) != EXPECT_S5[key]:
            sys.exit(f"ABORT {key}: batch-22 s5_index {bk and bk.get('s5_index')}")
        r = parse_raw(key, k22, slog)
        r["source"] = "part-bl-batch22-win"
        r["s5_index"] = int(bk["s5_index"])
        r["membership_class_count"] = int(bk["membership_class_count"])
        r["expect_third"] = 1
        rows.append(r)
    # -- anchors/negatives (published constants, AR->BF->BK->BM provenance chain)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b22win-thirdimpl-input-v1",
                 "sources": {
                     "b22": ("sources/raw k002.p1/p2 + sources/status-b22.log + sources/row-audit-winhalt-b22.json + "
                             "batch-keys-b22.json + published batch-22 (Part BL) canonical outputs, publication "
                             "commits 106c469 (scaffold+inputs) / 2ed5b90 (raws+status+row-audit) / a83da90 "
                             "(README+MANIFEST), commit-pinned raw fetch; batch-22 batch-keys sha256 b5f567bd.."),
                     "b22_batch_keys_sha256": PIN_BM_B22,
                     "b22_row_audit_winhalt_sha256": PIN_ROWAUDIT_B22,
                     "anchors": ("published Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK anchor/negative values, "
                                 "input CSVs byte-equality-checked against the published Part BF experiment "
                                 "(provenance chain AR -> BF -> BK -> BM)")},
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
    print("BM-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"])

if __name__ == "__main__":
    main()
