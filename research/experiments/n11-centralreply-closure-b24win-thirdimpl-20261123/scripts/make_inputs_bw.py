# make_inputs_bw.py -- machine-derive the Part BW third-impl input CSVs and
# rows.json for the batch-24 (class 16957, Part BO) WIN rows y001/y006 from
# the published batch-24 canonical artifacts (zero hand transcription).
# Fail-closed: any unexpected field aborts.
#
# Adapted from the published Part BV maker (make_inputs_bv.py, sha256
# a4031abe0bc669f0ec9843d224e5930eb2352cd60a22c49794347bf2a9445073,
# experiment n11-centralreply-closure-b23win-thirdimpl-20261123) for the
# batch-24 canonical publication; every gate adapted honestly to the
# batch-24 published formats: the batch-24 canonical status.log carries
# exactly 4 PASS lines (the y001/y006 WIN rows plus the y002/y004 LOSS
# adoption-candidate rows) and exactly 2 runner WIN-HALT lines (one per WIN
# key) and nothing else (batch-24 halted at the third key of worker 2; there
# are no truncated-retry or fragment lines), the published batch-24
# row-audit-winhalt.json battery (win_rows ["y001","y006"], loss_rows
# ["y002","y004"], pass_rows 2, probed 4, unprobed 49), and README-b24
# result-phrase checks.
#
# Sources (all commit-pinned raw fetches of the PUBLISHED canonical batch-24
# publication; local mirrors sha-verified against their published shas):
#  - sources/raw/y001.{p1,p2}.out, sources/raw/y006.{p1,p2}.out -- the
#    published batch-24 replica WIN outputs (canonical outputs commit
#    18420555).
#  - sources/status-b24.log -- the published batch-24 runner status.log
#    (canonical sha256 dcba6b0e...).
#  - sources/row-audit-winhalt-b24.json -- the published batch-24 winhalt
#    row audit (canonical sha256 9d073038...).
#  - sources/batch-keys-b24.json -- published batch-24 input declaration
#    (53 keys, class 16957, sha256 486858d6...).
#  - sources/README-b24.md -- published batch-24 README (commit d4c0074e,
#    sha256 672d18cf...).
#  - sources/published-input/{y001,y006}.input.csv -- published batch-24
#    per-key input CSVs (scaffold commit d7ee67c7; sha256 f746648e... /
#    34db2f1f...).
#  - sources/published-input-bf/{k02a,l1a,ng1,ng2}.input.csv -- published
#    Part BF anchor/negative input CSVs (byte-equality-verified here in
#    this experiment against the sha pins; provenance chain AR -> BF ->
#    BK -> BM -> BS -> BV -> BW).
#
# NOTE: verdicts are NOT consumed anywhere; this experiment is verdict-level
# corroboration literature only. The standard 11x11 empty board, the 19
# central-reply roots, class 16957 and every key (y001..y053, including the
# y002/y004 LOSS rows) remain UNKNOWN. WIN/LOSS adoption is a separate
# declared adoption Part with the pinned fail-closed merger only; the
# scrutiny owner C++ second-implementation gate pin 9193f5b6... wait is NOT
# actuated by this experiment.
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")

PIN_B24 = "486858d6e2de0662ef38a6ff1fd61c1c0dcf6e9b09012c2c32fdd99153d096cc"
PIN_STATUS_B24 = "dcba6b0e25b9643651eafaac6f4da85624e1335a6936762b10a2a00dcb04d7d5"
PIN_README_B24 = "672d18cfee8e58b939b8ec504991b25896edf178f11a20043921d54a2c5bf482"
PIN_ROWAUDIT_B24 = "9d073038f99af68f5832e6b49de2f760356dbfddcbd468623b762cce1083c0d5"
PIN_RAW = {
    "y001.p1": "03ae7d71d17ad3c2f06e45868482ae07c22d246feedb95697306e71ed3b873e6",
    "y001.p2": "03ae7d71d17ad3c2f06e45868482ae07c22d246feedb95697306e71ed3b873e6",
    "y006.p1": "2c21a9e1c0eb46fd48f2027d1bc838ab71a7a7e95d7e3ac696e6f3242c8fd254",
    "y006.p2": "1e2b6d13e1424112a72e2ca5eca697c8a17de12212a83e10d39aae36f7c617c2",
}
PIN_PUB_INPUT = {
    "y001": "f746648eb09058b699284fc304383d9e3ec40b17367201d6d015b670f63a3291",
    "y006": "34db2f1fd755e95b6a9101196cb19ec70d75531ee1629b059461e640906bbed3",
}
PIN_PUB_INPUT_BF = {
    "k02a": "b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887",
    "l1a": "e13d2a6c5bbaa34833dcaf8bfaaa91f99393942281f001552cb8af49cca8c98a",
    "ng1": "8e64b9ade1c04122ac4bdc5fa5129b5fca6cfac742ed92cb149f9ffb80ad0b09",
    "ng2": "f19cd5a30b0b868f0a0c7f12a6c47376c8ceb6e862f5c769fb14bdf74e8997dc",
}

TARGETS = ["y001", "y006"]
LOSS_ROWS = ["y002", "y004"]  # in-batch LOSS adoption-candidate rows (non-targets)
EXPECT_S5 = {"y001": 91296, "y006": 368510}
EXPECT_REPLICA = {"y001": 5291064, "y006": 5321639}  # published 2-pass node-exact WIN rows
EXPECT_LOSS_NODES = {"y002": 217944, "y004": 632091}  # published LOSS adoption-candidate rows
# batch-24 canonical status.log: 4 PASS lines (y002/y004 LOSS + y001/y006
# WIN) + 2 WIN-HALT runner lines; no truncated-retry, no fragment, nothing
# else)
STATUS_PASS_NODES = {"y001": 5291064, "y006": 5321639}
STATUS_LOSS_NODES = {"y002": 217944, "y004": 632091}
STATUS_EXPECT_LINES = 6
STATUS_EXPECT_PASS = 4
STATUS_EXPECT_RETRY = 0

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
    # status.log cross-verification (batch-24 canonical format): exactly one
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
    return {"key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "replica_result": result, "replica_nodes": nodes}

def main():
    os.makedirs(OUT, exist_ok=True)
    # -- source pins
    for fname, pin in (("batch-keys-b24.json", PIN_B24), ("status-b24.log", PIN_STATUS_B24),
                       ("README-b24.md", PIN_README_B24), ("row-audit-winhalt-b24.json", PIN_ROWAUDIT_B24)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    for k, pin in PIN_RAW.items():
        got = sha256(os.path.join(SRC, "raw", k + ".out"))
        if got != pin:
            sys.exit(f"ABORT raw {k} sha {got} != pin {pin}")
    bk24 = json.load(open(os.path.join(SRC, "batch-keys-b24.json")))
    if int(bk24["class_index"]) != 16957:
        sys.exit(f"ABORT class_index {bk24.get('class_index')}")
    if bk24.get("schema") != "n11-centralreply-closure-class16957-batch24-input-v1":
        sys.exit(f"ABORT batch-keys schema {bk24.get('schema')}")
    k24 = {k["key_id"]: k for k in bk24["keys"]}
    if len(k24) != 53:
        sys.exit(f"ABORT batch keys count {len(k24)} != 53")
    # -- status log battery gates (published batch-24 canonical runner log):
    #    6 lines = 4 PASS (the y001/y006 WIN pass lines + the y002/y004 LOSS
    #    rows) + 2 WIN-HALT; PASS key set must equal the row-audit
    #    loss_rows + win_rows exactly (machine cross-derivation).
    slog = open(os.path.join(SRC, "status-b24.log")).read()
    lines = [l for l in slog.splitlines() if l.strip()]
    if len(lines) != STATUS_EXPECT_LINES:
        sys.exit(f"ABORT status-b24.log line count {len(lines)} != {STATUS_EXPECT_LINES}")
    kinds = {}
    for ln in lines:
        toks = ln.split()
        kinds[toks[2]] = kinds.get(toks[2], 0) + 1
    if kinds.get("PASS") != STATUS_EXPECT_PASS:
        sys.exit(f"ABORT status-b24.log PASS lines {kinds.get('PASS')} != {STATUS_EXPECT_PASS}")
    n_winhalt = sum(1 for l in lines if l.split()[2] == "WIN-HALT")
    if n_winhalt != 2:
        sys.exit(f"ABORT status-b24.log WIN-HALT lines {n_winhalt} != 2")
    n_retry = sum(1 for l in lines if l.split()[2] in ("P1-TRUNCATED-RETRY", "P2-TRUNCATED-RETRY"))
    if n_retry != STATUS_EXPECT_RETRY:
        sys.exit(f"ABORT status-b24.log truncated-retry lines {n_retry} != {STATUS_EXPECT_RETRY}")
    if kinds.get("PASS", 0) + n_winhalt + n_retry != len(lines):
        sys.exit(f"ABORT status-b24.log carries unexpected line kinds: {sorted(kinds)}")
    pass_keys = [l.split()[1] for l in lines if l.split()[2] == "PASS"]
    if len(pass_keys) != len(set(pass_keys)):
        sys.exit(f"ABORT status-b24.log duplicate PASS keys")
    # -- published row-audit-winhalt battery gates (batch-24 halt-time audit)
    ra = json.load(open(os.path.join(SRC, "row-audit-winhalt-b24.json")))
    if ra.get("schema") != "n11-centralreply-closure-class16957-batch24-rowaudit-winhalt-v1":
        sys.exit(f"ABORT row-audit schema {ra.get('schema')}")
    if ra.get("class_index") != 16957 or ra.get("probed") != 4 or ra.get("pass_rows") != 2:
        sys.exit(f"ABORT row-audit header {ra.get('class_index')},{ra.get('probed')},{ra.get('pass_rows')}")
    if ra.get("win_rows") != ["y001", "y006"]:
        sys.exit(f"ABORT row-audit win_rows {ra.get('win_rows')}")
    if ra.get("loss_rows") != ["y002", "y004"]:
        sys.exit(f"ABORT row-audit loss_rows {ra.get('loss_rows')}")
    if ra.get("mismatches") != 0 or ra.get("exhausted_rows"):
        sys.exit(f"ABORT row-audit mismatches/exhausted {ra.get('mismatches')},{ra.get('exhausted_rows')}")
    if ra.get("unprobed_count") != 49:
        sys.exit(f"ABORT row-audit unprobed_count {ra.get('unprobed_count')}")
    if ra.get("derived_state") is not True:
        sys.exit(f"ABORT row-audit derived_state {ra.get('derived_state')}")
    if ra.get("fragment_keys") != {}:
        sys.exit(f"ABORT row-audit fragment_keys {ra.get('fragment_keys')}")
    if ra.get("batch") != 24 or ra.get("keys_total") != 53:
        sys.exit(f"ABORT row-audit batch/keys_total {ra.get('batch')},{ra.get('keys_total')}")
    if ra.get("input_sha256") != PIN_B24:
        sys.exit("ABORT row-audit input_sha256 != batch-keys pin")
    sr = ra.get("stop_rule") or ""
    if "pre-registered WIN-HALT" not in sr or "verdict not consumed" not in sr:
        sys.exit(f"ABORT row-audit stop_rule wording: {sr[:80]}")
    expected = set(ra.get("loss_rows", [])) | set(ra.get("win_rows", []))
    if set(pass_keys) != expected:
        missing = expected - set(pass_keys)
        extra = set(pass_keys) - expected
        sys.exit(f"ABORT status PASS keys != row-audit rows: missing {sorted(missing)} extra {sorted(extra)}")
    # every PASS row must be either one of the two target WIN rows with
    # result 1, or one of the two row-audit loss_rows (adoption candidates,
    # non-targets) with result 2 and the published loss node counts
    for l in lines:
        toks = l.split()
        if toks[2] == "PASS":
            pl = toks[3].split(",")
            if pl[0] != "15000000":
                sys.exit(f"ABORT status-b24.log {toks[1]} PASS budget {pl[0]}")
            if toks[1] in TARGETS:
                if pl[1] != "1" or int(pl[2]) != STATUS_PASS_NODES[toks[1]]:
                    sys.exit(f"ABORT status-b24.log {toks[1]} PASS line {pl} is not the published WIN row")
            elif toks[1] in LOSS_ROWS:
                if pl[1] != "2" or int(pl[2]) != STATUS_LOSS_NODES[toks[1]]:
                    sys.exit(f"ABORT status-b24.log {toks[1]} PASS line {pl} is not the published LOSS row")
            else:
                sys.exit(f"ABORT status-b24.log {toks[1]} PASS line is neither a target WIN row nor a row-audit loss row")
    if set(TARGETS) & set(LOSS_ROWS):
        sys.exit("ABORT target/loss row id collision")
    # -- README results battery gates (published batch-24 README)
    rd = open(os.path.join(SRC, "README-b24.md")).read()
    if "y001 WIN (honest label)" not in rd:
        sys.exit("ABORT README lacks the y001 WIN results line")
    if "y006 WIN (honest label)" not in rd:
        sys.exit("ABORT README lacks the y006 WIN results line")
    if "5,291,064" not in rd or "5,321,639" not in rd:
        sys.exit("ABORT README lacks the y001/y006 node counts")
    if "y002 LOSS (adoption candidateのみ)" not in rd or "y004 LOSS (adoption candidateのみ)" not in rd:
        sys.exit("ABORT README lacks the y002/y004 LOSS adoption-candidate lines")
    if "217,944" not in rd or "632,091" not in rd:
        sys.exit("ABORT README lacks the y002/y004 loss node counts")
    if "24番目・25番目の unconsumed closure WIN" not in rd:
        sys.exit("ABORT README lacks the 24th/25th-unconsumed-candidate route statement (line 85)")
    if "候補** で、採用判断は scrutiny owner C++第二実装 gate pin" not in rd:
        sys.exit("ABORT README lacks the candidate/scrutiny-owner continuation (line 86)")
    if "class 16957" not in rd or "Part BO" not in rd:
        sys.exit("ABORT README lacks the class-16957 Part BO identifier statement")
    # -- per-target raw cross-verification
    rows = []
    for key in TARGETS:
        bk = k24.get(key)
        if bk is None or int(bk["s5_index"]) != EXPECT_S5[key]:
            sys.exit(f"ABORT {key}: batch-24 s5_index {bk and bk.get('s5_index')}")
        r = parse_raw(key, k24, slog)
        r["source"] = "part-bo-batch24-win"
        r["s5_index"] = int(bk["s5_index"])
        r["membership_class_count"] = int(bk["membership_class_count"])
        r["expect_third"] = 1
        rows.append(r)
    # -- anchors/negatives (published constants, AR->BF->BK->BM->BS->BV->BW provenance chain)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b24win-thirdimpl-input-v1",
                 "sources": {
                     "b24": ("sources/raw y001.p1/p2 + y006.p1/p2 + sources/status-b24.log + sources/row-audit-winhalt-b24.json + "
                             "batch-keys-b24.json + published batch-24 (Part BO) canonical outputs, publication "
                             "commits 2c91e033 (declaration) / d7ee67c7 (scaffold+inputs) / 18420555 "
                             "(raws+status+row-audit) / d4c0074e (README+MANIFEST), commit-pinned raw fetch; "
                             "batch-24 batch-keys sha256 486858d6.."),
                     "b24_batch_keys_sha256": PIN_B24,
                     "b24_row_audit_winhalt_sha256": PIN_ROWAUDIT_B24,
                     "anchors": ("published Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK/BM/BS/BV anchor/negative values, "
                                 "input CSVs byte-equality-checked against the published Part BF experiment "
                                 "(provenance chain AR -> BF -> BK -> BM -> BS -> BV -> BW)")},
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
    print("BW-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"])

if __name__ == "__main__":
    main()
