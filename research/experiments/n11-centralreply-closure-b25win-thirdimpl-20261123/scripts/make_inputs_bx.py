# make_inputs_bx.py -- machine-derive the Part BX third-impl input CSVs and
# rows.json for the batch-25 (class 30565, Part BP) WIN rows i001/i002 from
# the published batch-25 canonical artifacts (zero hand transcription).
# Fail-closed: any unexpected field aborts.
#
# Adapted from the published Part BW maker (make_inputs_bw.py, sha256
# f94d6e4fe68f707d25296c5c28b879da7f2cc403c650d86ce29a2aa5f16c0901,
# experiment n11-centralreply-closure-b24win-thirdimpl-20261123) for the
# batch-25 canonical publication; every gate adapted honestly to the
# batch-25 published formats: the batch-25 canonical status.log carries
# exactly 2 PASS lines (the i001/i002 WIN rows) and exactly 2 runner
# WIN-HALT lines (one per WIN key) and nothing else (both workers halted at
# their first keys; there are no LOSS rows, no truncated-retry and no
# fragment lines), the published batch-25 row-audit-winhalt.json battery
# (win_rows ["i001","i002"], loss_rows [], pass_rows 0, probed 2,
# unprobed 51, fragment_keys {}), and README-b25 result-phrase checks.
#
# Sources (all commit-pinned raw fetches of the PUBLISHED canonical batch-25
# publication; local mirrors sha-verified against their published shas):
#  - sources/raw/i001.{p1,p2}.out, sources/raw/i002.{p1,p2}.out -- the
#    published batch-25 replica WIN outputs (canonical outputs commit
#    3b1a6283).
#  - sources/status-b25.log -- the published batch-25 runner status.log
#    (canonical sha256 0b12b101...).
#  - sources/row-audit-winhalt-b25.json -- the published batch-25 winhalt
#    row audit (canonical sha256 cc84d1b3...).
#  - sources/batch-keys-b25.json -- published batch-25 input declaration
#    (53 keys, class 30565, sha256 272c0c13...).
#  - sources/README-b25.md -- published batch-25 README (commit 573099b4,
#    sha256 67ec6ef9...).
#  - sources/published-input/{i001,i002}.input.csv -- published batch-25
#    per-key input CSVs (scaffold commit 2cc4a69a; sha256 cba4b6cb... /
#    1af3487a...).
#  - sources/published-input-bf/{k02a,l1a,ng1,ng2}.input.csv -- published
#    Part BF anchor/negative input CSVs (byte-equality-verified here in
#    this experiment against the sha pins; provenance chain AR -> BF ->
#    BK -> BM -> BS -> BV -> BW -> BX).
#
# NOTE: verdicts are NOT consumed anywhere; this experiment is verdict-level
# corroboration literature only. The standard 11x11 empty board, the 19
# central-reply roots, class 30565 and every key (i001..i053) remain
# UNKNOWN. WIN/LOSS adoption is a separate declared adoption Part with the
# pinned fail-closed merger only; the scrutiny owner C++ second-implementation
# gate pin 9193f5b6... wait is NOT actuated by this experiment.
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")

PIN_B25 = "272c0c134e3be17838311d0d3f18f09340d09094d35e15197481c999892390a5"
PIN_STATUS_B25 = "0b12b10147e94245643664604bb484ed58ebafa287f6e2b3058b98530c287512"
PIN_README_B25 = "67ec6ef906c0100f435f072a757f8f7f9d8f9c6a8cacafeba188b7e607d8136f"
PIN_ROWAUDIT_B25 = "cc84d1b3ae5b001a5a5c46a6d254b2ef871ad6087ef218bc7949f4bc2ab1c7ab"
PIN_RAW = {
    "i001.p1": "4e9e2de212455eec65121506105f4a71e39a4eeedfed9138dec4a76cb60ce9f2",
    "i001.p2": "bc6417d21cda8d505983edbb76bc383197f00212289343a76abe40038be62d3e",
    "i002.p1": "da09e97acb09b3036848c282238b7aa7f3b63be85aec09d8c6b46b038f208fa7",
    "i002.p2": "2730ee6d84447a978f0fae28818b6602de09f7b126bd8ae11a67903a5b7c4363",
}
PIN_PUB_INPUT = {
    "i001": "cba4b6cb0a78a74318443f746f80e9d6a8c574b2ef0976090f1a0e8092833ce6",
    "i002": "1af3487ab826c31e46c9a2ed23674dc83e0da52f8e7b245c8143fcded31ba564",
}
PIN_PUB_INPUT_BF = {
    "k02a": "b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887",
    "l1a": "e13d2a6c5bbaa34833dcaf8bfaaa91f99393942281f001552cb8af49cca8c98a",
    "ng1": "8e64b9ade1c04122ac4bdc5fa5129b5fca6cfac742ed92cb149f9ffb80ad0b09",
    "ng2": "f19cd5a30b0b868f0a0c7f12a6c47376c8ceb6e862f5c769fb14bdf74e8997dc",
}

TARGETS = ["i001", "i002"]
LOSS_ROWS = []  # batch-25 halted at the first key of each worker: no LOSS rows
EXPECT_S5 = {"i001": 68580, "i002": 191299}
EXPECT_REPLICA = {"i001": 13251132, "i002": 7207180}  # published 2-pass node-exact WIN rows
EXPECT_LOSS_NODES = {}  # none in the published batch-25 canonical status.log
# batch-25 canonical status.log: 2 PASS lines (i001/i002 WIN) + 2 WIN-HALT
# runner lines; no LOSS rows, no truncated-retry, no fragment, nothing else
STATUS_PASS_NODES = {"i001": 13251132, "i002": 7207180}
STATUS_LOSS_NODES = {}
STATUS_EXPECT_LINES = 4
STATUS_EXPECT_PASS = 2
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
    # status.log cross-verification (batch-25 canonical format): exactly one
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
    for fname, pin in (("batch-keys-b25.json", PIN_B25), ("status-b25.log", PIN_STATUS_B25),
                       ("README-b25.md", PIN_README_B25), ("row-audit-winhalt-b25.json", PIN_ROWAUDIT_B25)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    for k, pin in PIN_RAW.items():
        got = sha256(os.path.join(SRC, "raw", k + ".out"))
        if got != pin:
            sys.exit(f"ABORT raw {k} sha {got} != pin {pin}")
    bk25 = json.load(open(os.path.join(SRC, "batch-keys-b25.json")))
    if int(bk25["class_index"]) != 30565:
        sys.exit(f"ABORT class_index {bk25.get('class_index')}")
    if bk25.get("schema") != "n11-centralreply-closure-class30565-batch25-input-v1":
        sys.exit(f"ABORT batch-keys schema {bk25.get('schema')}")
    k25 = {k["key_id"]: k for k in bk25["keys"]}
    if len(k25) != 53:
        sys.exit(f"ABORT batch keys count {len(k25)} != 53")
    # -- status log battery gates (published batch-25 canonical runner log):
    #    4 lines = 2 PASS (the i001/i002 WIN pass lines) + 2 WIN-HALT; PASS
    #    key set must equal the row-audit win_rows exactly (batch-25 has no
    #    LOSS rows; machine cross-derivation).
    slog = open(os.path.join(SRC, "status-b25.log")).read()
    lines = [l for l in slog.splitlines() if l.strip()]
    if len(lines) != STATUS_EXPECT_LINES:
        sys.exit(f"ABORT status-b25.log line count {len(lines)} != {STATUS_EXPECT_LINES}")
    kinds = {}
    for ln in lines:
        toks = ln.split()
        kinds[toks[2]] = kinds.get(toks[2], 0) + 1
    if kinds.get("PASS") != STATUS_EXPECT_PASS:
        sys.exit(f"ABORT status-b25.log PASS lines {kinds.get('PASS')} != {STATUS_EXPECT_PASS}")
    n_winhalt = sum(1 for l in lines if l.split()[2] == "WIN-HALT")
    if n_winhalt != 2:
        sys.exit(f"ABORT status-b25.log WIN-HALT lines {n_winhalt} != 2")
    n_retry = sum(1 for l in lines if l.split()[2] in ("P1-TRUNCATED-RETRY", "P2-TRUNCATED-RETRY"))
    if n_retry != STATUS_EXPECT_RETRY:
        sys.exit(f"ABORT status-b25.log truncated-retry lines {n_retry} != {STATUS_EXPECT_RETRY}")
    if kinds.get("PASS", 0) + n_winhalt + n_retry != len(lines):
        sys.exit(f"ABORT status-b25.log carries unexpected line kinds: {sorted(kinds)}")
    pass_keys = [l.split()[1] for l in lines if l.split()[2] == "PASS"]
    if len(pass_keys) != len(set(pass_keys)):
        sys.exit(f"ABORT status-b25.log duplicate PASS keys")
    # -- published row-audit-winhalt battery gates (batch-25 halt-time audit)
    ra = json.load(open(os.path.join(SRC, "row-audit-winhalt-b25.json")))
    if ra.get("schema") != "n11-centralreply-closure-class30565-batch25-rowaudit-winhalt-v1":
        sys.exit(f"ABORT row-audit schema {ra.get('schema')}")
    if ra.get("class_index") != 30565 or ra.get("probed") != 2 or ra.get("pass_rows") != 0:
        sys.exit(f"ABORT row-audit header {ra.get('class_index')},{ra.get('probed')},{ra.get('pass_rows')}")
    if ra.get("win_rows") != ["i001", "i002"]:
        sys.exit(f"ABORT row-audit win_rows {ra.get('win_rows')}")
    if ra.get("loss_rows") != []:
        sys.exit(f"ABORT row-audit loss_rows {ra.get('loss_rows')}")
    if ra.get("mismatches") != 0 or ra.get("exhausted_rows"):
        sys.exit(f"ABORT row-audit mismatches/exhausted {ra.get('mismatches')},{ra.get('exhausted_rows')}")
    if ra.get("unprobed_count") != 51:
        sys.exit(f"ABORT row-audit unprobed_count {ra.get('unprobed_count')}")
    if ra.get("derived_state") is not True:
        sys.exit(f"ABORT row-audit derived_state {ra.get('derived_state')}")
    if ra.get("fragment_keys") != {}:
        sys.exit(f"ABORT row-audit fragment_keys {ra.get('fragment_keys')}")
    if ra.get("batch") != 25 or ra.get("keys_total") != 53:
        sys.exit(f"ABORT row-audit batch/keys_total {ra.get('batch')},{ra.get('keys_total')}")
    if ra.get("input_sha256") != PIN_B25:
        sys.exit("ABORT row-audit input_sha256 != batch-keys pin")
    sr = ra.get("stop_rule") or ""
    if "pre-registered WIN-HALT" not in sr or "verdict not consumed" not in sr:
        sys.exit(f"ABORT row-audit stop_rule wording: {sr[:80]}")
    expected = set(ra.get("loss_rows", [])) | set(ra.get("win_rows", []))
    if set(pass_keys) != expected:
        missing = expected - set(pass_keys)
        extra = set(pass_keys) - expected
        sys.exit(f"ABORT status PASS keys != row-audit rows: missing {sorted(missing)} extra {sorted(extra)}")
    # every PASS row must be one of the two target WIN rows with result 1
    # and the published WIN node counts (batch-25 has no LOSS rows)
    for l in lines:
        toks = l.split()
        if toks[2] == "PASS":
            pl = toks[3].split(",")
            if pl[0] != "15000000":
                sys.exit(f"ABORT status-b25.log {toks[1]} PASS budget {pl[0]}")
            if toks[1] in TARGETS:
                if pl[1] != "1" or int(pl[2]) != STATUS_PASS_NODES[toks[1]]:
                    sys.exit(f"ABORT status-b25.log {toks[1]} PASS line {pl} is not the published WIN row")
            else:
                sys.exit(f"ABORT status-b25.log {toks[1]} PASS line is not a target WIN row (batch-25 has no loss rows)")
    if set(TARGETS) & set(LOSS_ROWS):
        sys.exit("ABORT target/loss row id collision")
    # -- README results battery gates (published batch-25 README)
    rd = open(os.path.join(SRC, "README-b25.md")).read()
    if "i001 WIN (honest label)" not in rd:
        sys.exit("ABORT README lacks the i001 WIN results line")
    if "i002 WIN (honest label)" not in rd:
        sys.exit("ABORT README lacks the i002 WIN results line")
    if "13,251,132" not in rd or "7,207,180" not in rd:
        sys.exit("ABORT README lacks the i001/i002 node counts")
    if "26番目・27番目の unconsumed closure WIN" not in rd:
        sys.exit("ABORT README lacks the 26th/27th-unconsumed-candidate route statement")
    if "候補** で、採用判断は scrutiny owner C++第二実装 gate pin" not in rd:
        sys.exit("ABORT README lacks the candidate/scrutiny-owner continuation")
    if "class 30565" not in rd or "Part BP" not in rd:
        sys.exit("ABORT README lacks the class-30565 Part BP identifier statement")
    # -- per-target raw cross-verification
    rows = []
    for key in TARGETS:
        bk = k25.get(key)
        if bk is None or int(bk["s5_index"]) != EXPECT_S5[key]:
            sys.exit(f"ABORT {key}: batch-25 s5_index {bk and bk.get('s5_index')}")
        r = parse_raw(key, k25, slog)
        r["source"] = "part-bp-batch25-win"
        r["s5_index"] = int(bk["s5_index"])
        r["membership_class_count"] = int(bk["membership_class_count"])
        r["expect_third"] = 1
        rows.append(r)
    # -- anchors/negatives (published constants, AR->BF->BK->BM->BS->BV->BW->BX provenance chain)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b25win-thirdimpl-input-v1",
                 "sources": {
                     "b25": ("sources/raw i001.p1/p2 + i002.p1/p2 + sources/status-b25.log + sources/row-audit-winhalt-b25.json + "
                             "batch-keys-b25.json + published batch-25 (Part BP) canonical outputs, publication "
                             "commits b54fbdd6 (declaration) / 2cc4a69a (scaffold+inputs) / 3b1a6283 "
                             "(raws+status+row-audit) / 573099b4 (README+MANIFEST), commit-pinned raw fetch; "
                             "batch-25 batch-keys sha256 272c0c13.."),
                     "b25_batch_keys_sha256": PIN_B25,
                     "b25_row_audit_winhalt_sha256": PIN_ROWAUDIT_B25,
                     "anchors": ("published Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK/BM/BS/BV/BW anchor/negative values, "
                                 "input CSVs byte-equality-checked against the published Part BF experiment "
                                 "(provenance chain AR -> BF -> BK -> BM -> BS -> BV -> BW -> BX)")},
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
    print("BX-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"])

if __name__ == "__main__":
    main()
