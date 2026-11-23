# make_inputs_bv.py -- machine-derive the Part BV third-impl input CSVs and
# rows.json for the batch-23 (class 31600, Part BN) WIN rows s001/s002 from
# the published batch-23 canonical artifacts (zero hand transcription).
# Fail-closed: any unexpected field aborts.
#
# Adapted from the published Part BS maker (make_inputs_bs.py, sha256
# 313a8d71..., experiment n11-centralreply-closure-b26win-thirdimpl-20261123)
# for the batch-23 canonical publication; every gate adapted honestly to the
# batch-23 published formats: the batch-23 canonical status.log carries
# exactly 2 PASS lines (the s001/s002 WIN rows) and exactly 2 runner WIN-HALT
# lines (one per worker key) and nothing else (batch-23 halted at the first
# key of both workers, so there are no truncated-retry or fragment lines),
# the published batch-23 row-audit-winhalt.json battery (win_rows
# ["s001","s002"], pass_rows 0, fragment_keys {}, unprobed_count 51), and
# README-b23 result-phrase checks.
#
# Sources (all commit-pinned raw fetches of the PUBLISHED canonical batch-23
# publication; local mirrors sha-verified against their published shas):
#  - sources/raw/s001.{p1,p2}.out, sources/raw/s002.{p1,p2}.out -- the
#    published batch-23 replica WIN outputs (canonical outputs commit
#    597d810).
#  - sources/status-b23.log -- the published batch-23 runner status.log
#    (canonical sha256 1e4ccea9...).
#  - sources/row-audit-winhalt-b23.json -- the published batch-23 winhalt
#    row audit (canonical sha256 14aa7f63...).
#  - sources/batch-keys-b23.json -- published batch-23 input declaration
#    (53 keys, class 31600, sha256 2776acaf...).
#  - sources/README-b23.md -- published batch-23 README (4dad105b,
#    sha256 f38922ca...).
#  - sources/published-input/{s001,s002}.input.csv -- published batch-23
#    per-key input CSVs (scaffold commit 52ff9a09; sha256 422161a1... /
#    32257e8e...).
#  - sources/published-input-bf/{k02a,l1a,ng1,ng2}.input.csv -- published
#    Part BF anchor/negative input CSVs (byte-equality-verified here in
#    this experiment against the sha pins; provenance chain AR -> BF ->
#    BK -> BM -> BS -> BV).
#
# NOTE: verdicts are NOT consumed anywhere; this experiment is verdict-level
# corroboration literature only. The standard 11x11 empty board, the 19
# central-reply roots, class 31600 and every key remain UNKNOWN.
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")

PIN_B23 = "2776acafbb638cb148661b3988b7eb36bc8519e5b7b75b415b01618bfcb85bf7"
PIN_STATUS_B23 = "1e4ccea9025cb11f38a05c7403a85a7d838398040506201738516bf46fa97e60"
PIN_README_B23 = "f38922ca4a4928602be32b0b74318d43c84348556ce11d20b2fe69c473d3d825"
PIN_ROWAUDIT_B23 = "14aa7f63abcc6943b4625f8d171ca8f7b5f248de57d03306075a2f77643fec86"
PIN_RAW = {
    "s001.p1": "8446306972d3b5f7908b44cef8c1ea505b0193ee16ef102d00942f2b41a2e1df",
    "s001.p2": "cd7633fb9459e804fced201715ae61ac78673d0eecce026816bd2f3b3fc053d4",
    "s002.p1": "39664259df7873df2c1848b08b9877042d9481946cb44a799e3bb1847ec3c92f",
    "s002.p2": "8ce830378efb7e5b6a1fdccf09a402f7938b122aa5ab128a2222fc5764f8bb42",
}
PIN_PUB_INPUT = {
    "s001": "422161a1fb8da6cdd16932d191c2d9d4a7d5f2949887959d572caeed4d782d7f",
    "s002": "32257e8e4aa8642be0fd804119bb1821034f1cd73508dc2d9436b15d61d32fa5",
}
PIN_PUB_INPUT_BF = {
    "k02a": "b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887",
    "l1a": "e13d2a6c5bbaa34833dcaf8bfaaa91f99393942281f001552cb8af49cca8c98a",
    "ng1": "8e64b9ade1c04122ac4bdc5fa5129b5fca6cfac742ed92cb149f9ffb80ad0b09",
    "ng2": "f19cd5a30b0b868f0a0c7f12a6c47376c8ceb6e862f5c769fb14bdf74e8997dc",
}

TARGETS = ["s001", "s002"]
EXPECT_S5 = {"s001": 62435, "s002": 192809}
EXPECT_REPLICA = {"s001": 5415927, "s002": 9329444}  # published 2-pass node-exact WIN rows
# batch-23 canonical status.log: 2 PASS lines + 2 WIN-HALT lines (halt at the
# first key of both workers; no truncated-retry, no fragment, nothing else)
STATUS_PASS_NODES = {"s001": 5415927, "s002": 9329444}
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
    # status.log cross-verification (batch-23 canonical format): exactly one
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
    if n_winhalt != 2:
        sys.exit(f"ABORT status.log WIN-HALT runner lines != 2: {n_winhalt}")
    return {"key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "replica_result": result, "replica_nodes": nodes}

def main():
    os.makedirs(OUT, exist_ok=True)
    # -- source pins
    for fname, pin in (("batch-keys-b23.json", PIN_B23), ("status-b23.log", PIN_STATUS_B23),
                       ("README-b23.md", PIN_README_B23), ("row-audit-winhalt-b23.json", PIN_ROWAUDIT_B23)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    for k, pin in PIN_RAW.items():
        got = sha256(os.path.join(SRC, "raw", k + ".out"))
        if got != pin:
            sys.exit(f"ABORT raw {k} sha {got} != pin {pin}")
    bk23 = json.load(open(os.path.join(SRC, "batch-keys-b23.json")))
    if int(bk23["class_index"]) != 31600:
        sys.exit(f"ABORT class_index {bk23.get('class_index')}")
    k23 = {k["key_id"]: k for k in bk23["keys"]}
    if len(k23) != 53:
        sys.exit(f"ABORT batch keys count {len(k23)} != 53")
    # -- status log battery gates (published batch-23 canonical runner log):
    #    4 lines = 2 PASS (the s001/s002 WIN pass lines) + 2 WIN-HALT; PASS
    #    key set must equal the row-audit loss_rows + win_rows exactly
    #    (machine cross-derivation).
    slog = open(os.path.join(SRC, "status-b23.log")).read()
    lines = [l for l in slog.splitlines() if l.strip()]
    if len(lines) != STATUS_EXPECT_LINES:
        sys.exit(f"ABORT status-b23.log line count {len(lines)} != {STATUS_EXPECT_LINES}")
    kinds = {}
    for ln in lines:
        toks = ln.split()
        kinds[toks[2]] = kinds.get(toks[2], 0) + 1
    if kinds.get("PASS") != STATUS_EXPECT_PASS:
        sys.exit(f"ABORT status-b23.log PASS lines {kinds.get('PASS')} != {STATUS_EXPECT_PASS}")
    n_winhalt = sum(1 for l in lines if l.split()[2] == "WIN-HALT")
    if n_winhalt != 2:
        sys.exit(f"ABORT status-b23.log WIN-HALT lines {n_winhalt} != 2")
    n_retry = sum(1 for l in lines if l.split()[2] in ("P1-TRUNCATED-RETRY", "P2-TRUNCATED-RETRY"))
    if n_retry != STATUS_EXPECT_RETRY:
        sys.exit(f"ABORT status-b23.log truncated-retry lines {n_retry} != {STATUS_EXPECT_RETRY}")
    if kinds.get("PASS", 0) + n_winhalt + n_retry != len(lines):
        sys.exit(f"ABORT status-b23.log carries unexpected line kinds: {sorted(kinds)}")
    pass_keys = [l.split()[1] for l in lines if l.split()[2] == "PASS"]
    if len(pass_keys) != len(set(pass_keys)):
        sys.exit(f"ABORT status-b23.log duplicate PASS keys")
    # -- published row-audit-winhalt battery gates (batch-23 halt-time audit)
    ra = json.load(open(os.path.join(SRC, "row-audit-winhalt-b23.json")))
    if ra.get("schema") != "n11-centralreply-closure-class31600-batch23-rowaudit-winhalt-v1":
        sys.exit(f"ABORT row-audit schema {ra.get('schema')}")
    if ra.get("class_index") != 31600 or ra.get("probed") != 2 or ra.get("pass_rows") != 0:
        sys.exit(f"ABORT row-audit header {ra.get('class_index')},{ra.get('probed')},{ra.get('pass_rows')}")
    if ra.get("win_rows") != ["s001", "s002"]:
        sys.exit(f"ABORT row-audit win_rows {ra.get('win_rows')}")
    if ra.get("mismatches") != 0 or ra.get("exhausted_rows"):
        sys.exit(f"ABORT row-audit mismatches/exhausted {ra.get('mismatches')},{ra.get('exhausted_rows')}")
    if ra.get("unprobed_count") != 51:
        sys.exit(f"ABORT row-audit unprobed_count {ra.get('unprobed_count')}")
    if ra.get("derived_state") is not True:
        sys.exit(f"ABORT row-audit derived_state {ra.get('derived_state')}")
    if ra.get("fragment_keys") != {}:
        sys.exit(f"ABORT row-audit fragment_keys {ra.get('fragment_keys')}")
    if ra.get("batch") != 23 or ra.get("keys_total") != 53:
        sys.exit(f"ABORT row-audit batch/keys_total {ra.get('batch')},{ra.get('keys_total')}")
    if ra.get("input_sha256") != PIN_B23:
        sys.exit("ABORT row-audit input_sha256 != batch-keys pin")
    expected = set(ra.get("loss_rows", [])) | set(ra.get("win_rows", []))
    if set(pass_keys) != expected:
        missing = expected - set(pass_keys)
        extra = set(pass_keys) - expected
        sys.exit(f"ABORT status PASS keys != row-audit rows: missing {sorted(missing)} extra {sorted(extra)}")
    # every PASS row must be one of the two target WIN rows with result 1
    for l in lines:
        toks = l.split()
        if toks[2] == "PASS":
            if toks[1] not in TARGETS:
                sys.exit(f"ABORT status-b23.log {toks[1]} PASS line is not a target WIN row")
            pl = toks[3].split(",")
            if pl[0] != "15000000" or pl[1] != "1":
                sys.exit(f"ABORT status-b23.log {toks[1]} PASS line {pl} is not a WIN row")
    # -- README results battery gates (published batch-23 README)
    rd = open(os.path.join(SRC, "README-b23.md")).read()
    if "s001 WIN (honest label)" not in rd:
        sys.exit("ABORT README lacks the s001 WIN results line")
    if "s002 WIN (honest label)" not in rd:
        sys.exit("ABORT README lacks the s002 WIN results line")
    if "5,415,927" not in rd or "9,329,444" not in rd:
        sys.exit("ABORT README lacks the s001/s002 node counts")
    if "22番目・23番目の unconsumed" not in rd or "closure WIN 候補" not in rd:
        sys.exit("ABORT README lacks the 22nd/23rd-unconsumed-candidate route statement")
    if "class 31600" not in rd or "Part BN" not in rd:
        sys.exit("ABORT README lacks the class-31600 Part BN identifier statement")
    # -- per-target raw cross-verification
    rows = []
    for key in TARGETS:
        bk = k23.get(key)
        if bk is None or int(bk["s5_index"]) != EXPECT_S5[key]:
            sys.exit(f"ABORT {key}: batch-23 s5_index {bk and bk.get('s5_index')}")
        r = parse_raw(key, k23, slog)
        r["source"] = "part-bn-batch23-win"
        r["s5_index"] = int(bk["s5_index"])
        r["membership_class_count"] = int(bk["membership_class_count"])
        r["expect_third"] = 1
        rows.append(r)
    # -- anchors/negatives (published constants, AR->BF->BK->BM->BS->BV provenance chain)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b23win-thirdimpl-input-v1",
                 "sources": {
                     "b23": ("sources/raw s001.p1/p2 + s002.p1/p2 + sources/status-b23.log + sources/row-audit-winhalt-b23.json + "
                             "batch-keys-b23.json + published batch-23 (Part BN) canonical outputs, publication "
                             "commits bde1c7de (declaration) / 52ff9a09 (scaffold+inputs) / 597d810 "
                             "(raws+status+row-audit) / 4dad105b (README+MANIFEST), commit-pinned raw fetch; "
                             "batch-23 batch-keys sha256 2776acaf.."),
                     "b23_batch_keys_sha256": PIN_B23,
                     "b23_row_audit_winhalt_sha256": PIN_ROWAUDIT_B23,
                     "anchors": ("published Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK/BM/BS anchor/negative values, "
                                 "input CSVs byte-equality-checked against the published Part BF experiment "
                                 "(provenance chain AR -> BF -> BK -> BM -> BS -> BV)")},
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
    print("BV-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"])

if __name__ == "__main__":
    main()
