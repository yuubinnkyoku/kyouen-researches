# make_inputs_cc.py -- machine-derive the Part CC third-impl input CSVs and
# rows.json for the batch-28 (class 5343, Part CB) WIN rows aa001/aa002 from the
# published batch-28 canonical artifacts (zero hand transcription).
# Fail-closed: any unexpected field aborts.
#
# Adapted from the published Part BY maker (sha256
# 359abebcd7b403a8b848d1b9bfa9866e2bb368f2ba01f6ffd071c44de36eedc5,
# experiment n11-centralreply-closure-b27win-thirdimpl-20261123, itself from
# BX e1def905... b25win / BW f94d6e4f... b24win) for the batch-28 canonical
# publication. Batch-28 specific gates (all honest):
#  - the published batch-28 status.log carries 4 lines = 2 WIN PASS rows
#    (aa001/aa002, result 1, the two targets) + 2 WIN-HALT runner lines
#    (one per halted worker); no LOSS rows, no truncated-retry lines, no
#    fragments (remaining 52 keys aa003..aa054 are fileless UNPROBED).
#  - every PASS row must be one of the 2 target WIN rows (result 1,
#    published WIN nodes) - there are no loss rows in this batch.
#  - the row-audit battery gates: win_rows [aa001, aa002], loss_rows [],
#    pass_rows 0, probed 2, unprobed_count 52, fragment_keys {}, derived_state
#    true, stop_rule wording, input_sha256 machine cross-check, the 52
#    fileless_unprobed keys disjoint from the PASS keys.
#  - README-b28 result-phrase checks (aa001/aa002 WIN honest labels, 30th/31st
#    unconsumed closure WIN candidates, the two node counts, the 52-key
#    fileless UNPROBED statement, class 5343 / Part CB identifiers,
#    scrutiny-owner wording).
#
# Sources (all commit-pinned raw fetches of the PUBLISHED canonical batch-28
# publication, experiment n11-centralreply-closure-class5343-batch28-
# 20261123, publication commits 39521983 (declaration) / a3dc8202 (scaffold)
# / 84d495e8 (raws+status+row-audit) / 4f9d2cef (README+MANIFEST); local
# mirrors sha-verified against the published MANIFEST-sha256 (81 lines) and
# pinned fetches):
#  - sources/raw/aa00{1,2}.{p1,p2}.out -- the published batch-28 replica WIN
#    outputs (raws commit).
#  - sources/status-b28.log -- published batch-28 runner status.log.
#  - sources/row-audit-winhalt-b28.json -- published batch-28 winhalt audit.
#  - sources/batch-keys-b28.json -- published batch-28 input declaration
#    (54 keys, class 5343).
#  - sources/README-b28.md -- published batch-28 README.
#  - sources/published-input/aa00{1,2}.input.csv -- published batch-28
#    per-key input CSVs.
#  - sources/published-input-bf/{k02a,l1a,ng1,ng2}.input.csv -- published
#    Part BF anchor/negative input CSVs (provenance chain AR -> BF -> BK ->
#    BM -> BS -> BV -> BW -> BX -> BY -> CC).
#
# NOTE: verdicts are NOT consumed anywhere; this experiment is verdict-level
# corroboration literature only. The standard 11x11 empty board, the 19
# central-reply roots, class 5343 and every key (aa001..aa054) remain
# UNKNOWN. WIN/LOSS adoption is a separate declared adoption Part with the
# pinned fail-closed merger only; the scrutiny owner C++ second-implementation
# gate pin 9193f5b6... wait is NOT actuated by this experiment.
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")

PIN_B28 = "af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5"
PIN_STATUS_B28 = "e98b5d23b09cddf2d118ba6da6f340541b6535501529857de88890ecb846b953"
PIN_README_B28 = "1b9f87b1ed83236dd081040be72dd6d64a5a9a0e303b031be21144fd139d954e"
PIN_ROWAUDIT_B28 = "3f50b4f6df4e5139c9559e9a8a727bcfa170edf07e2623ecaf23e4732707cbd6"
PIN_RAW = {
    "aa001.p1": "b3f396bdfd606c3ffb8d3d08c7c51eced921a37b963706e20864c8423b598995",
    "aa001.p2": "59a3e8a1e12c24e467b5227c2af839bb1b40f901340325eddcd4b68652b1ebc5",
    "aa002.p1": "07d9d643f7d7cb6e76568e7429fec22173a2a4fbf144970da4a1dad9d38d87d3",
    "aa002.p2": "7d2d26a874f58396cee0e96f0950e0f9a1f0b0bffe71f3784fcae12574e732ba",
}
PIN_PUB_INPUT = {
    "aa001": "8083b62e425505e8957a5d046d7754032bf9ddfc69d6b36bb81ebdacab1401d4",
    "aa002": "6310e6412aed3957bf0e5e3dc7c01054c8f50ddf5c1dca086aac0435b0140fa9",
}
PIN_PUB_INPUT_BF = {
    "k02a": "b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887",
    "l1a": "e13d2a6c5bbaa34833dcaf8bfaaa91f99393942281f001552cb8af49cca8c98a",
    "ng1": "8e64b9ade1c04122ac4bdc5fa5129b5fca6cfac742ed92cb149f9ffb80ad0b09",
    "ng2": "f19cd5a30b0b868f0a0c7f12a6c47376c8ceb6e862f5c769fb14bdf74e8997dc",
}

TARGETS = ["aa001", "aa002"]
LOSS_ROWS = []  # batch-28 halted at the first WIN row per worker: no loss rows
EXPECT_S5 = {"aa001": 28037, "aa002": 87306}
EXPECT_MEMBERSHIP = {"aa001": 4, "aa002": 2}
EXPECT_REPLICA = {"aa001": 13183855, "aa002": 6527041}  # published 2-pass node-exact WIN rows
# batch-28 canonical status.log: 2 WIN PASS lines + 2 WIN-HALT runner lines;
# no truncated-retry lines, no fragment lines, no loss rows
STATUS_PASS_NODES = {"aa001": 13183855, "aa002": 6527041}
STATUS_LOSS_NODES = {}
STATUS_EXPECT_LINES = 4
STATUS_EXPECT_PASS = 2
STATUS_EXPECT_RETRY = 0
FRAGMENT_KEYS = []
FILELESS_UNPROBED_COUNT = 52

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
    # status.log cross-verification (batch-28 canonical format)
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
    for fname, pin in (("batch-keys-b28.json", PIN_B28), ("status-b28.log", PIN_STATUS_B28),
                       ("README-b28.md", PIN_README_B28), ("row-audit-winhalt-b28.json", PIN_ROWAUDIT_B28)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    for k, pin in PIN_RAW.items():
        got = sha256(os.path.join(SRC, "raw", k + ".out"))
        if got != pin:
            sys.exit(f"ABORT raw {k} sha {got} != pin {pin}")
    bk28 = json.load(open(os.path.join(SRC, "batch-keys-b28.json")))
    if int(bk28["class_index"]) != 5343:
        sys.exit(f"ABORT class_index {bk28.get('class_index')}")
    if bk28.get("schema") != "n11-centralreply-closure-class5343-batch28-input-v1":
        sys.exit(f"ABORT batch-keys schema {bk28.get('schema')}")
    k28 = {k["key_id"]: k for k in bk28["keys"]}
    if len(k28) != 54:
        sys.exit(f"ABORT batch keys count {len(k28)} != 54")
    if not re.fullmatch(r"aa[0-9]{3}", TARGETS[0]) or not re.fullmatch(r"aa[0-9]{3}", TARGETS[1]):
        sys.exit("ABORT batch-28 key ids must be the 2-char aa### form")
    # -- status log battery gates (published batch-28 canonical runner log):
    #    4 lines = 2 WIN PASS + 2 WIN-HALT; PASS key set must equal the
    #    row-audit win_rows exactly; no truncated-retry lines; the 52 fileless
    #    keys must not appear as status rows.
    slog = open(os.path.join(SRC, "status-b28.log")).read()
    lines = [l for l in slog.splitlines() if l.strip()]
    if len(lines) != STATUS_EXPECT_LINES:
        sys.exit(f"ABORT status-b28.log line count {len(lines)} != {STATUS_EXPECT_LINES}")
    kinds = {}
    for ln in lines:
        toks = ln.split()
        kinds[toks[2]] = kinds.get(toks[2], 0) + 1
    if kinds.get("PASS") != STATUS_EXPECT_PASS:
        sys.exit(f"ABORT status-b28.log PASS lines {kinds.get('PASS')} != {STATUS_EXPECT_PASS}")
    for bad_kind in ("P1-TRUNCATED-RETRY", "P2-TRUNCATED-RETRY", "EXHAUSTED", "FAIL", "MISMATCH"):
        if bad_kind in kinds:
            sys.exit(f"ABORT status-b28.log carries unexpected line kind {bad_kind}")
    n_winhalt = sum(1 for l in lines if l.split()[2] == "WIN-HALT")
    if n_winhalt != 2:
        sys.exit(f"ABORT status-b28.log WIN-HALT lines {n_winhalt} != 2")
    if kinds.get("PASS", 0) + n_winhalt != len(lines):
        sys.exit(f"ABORT status-b28.log carries unexpected line kinds: {sorted(kinds)}")
    pass_keys = [l.split()[1] for l in lines if l.split()[2] == "PASS"]
    if len(pass_keys) != len(set(pass_keys)):
        sys.exit("ABORT status-b28.log duplicate PASS keys")
    pass_lines_map = {}
    for l in lines:
        toks = l.split()
        if toks[2] == "PASS":
            pass_lines_map.setdefault(toks[1], []).append(toks[3].split(","))
    for fk in FRAGMENT_KEYS:
        if fk in pass_keys:
            sys.exit(f"ABORT fragment {fk} appears as a status PASS row (fragments are UNPROBED bookkeeping)")
    # -- published row-audit-winhalt battery gates (batch-28 halt-time audit)
    ra = json.load(open(os.path.join(SRC, "row-audit-winhalt-b28.json")))
    if ra.get("schema") != "n11-centralreply-closure-class5343-batch28-rowaudit-winhalt-v1":
        sys.exit(f"ABORT row-audit schema {ra.get('schema')}")
    if ra.get("class_index") != 5343 or ra.get("probed") != 2 or ra.get("pass_rows") != 0:
        sys.exit(f"ABORT row-audit header {ra.get('class_index')},{ra.get('probed')},{ra.get('pass_rows')}")
    if ra.get("win_rows") != ["aa001", "aa002"]:
        sys.exit(f"ABORT row-audit win_rows {ra.get('win_rows')}")
    if ra.get("loss_rows") != []:
        sys.exit(f"ABORT row-audit loss_rows {ra.get('loss_rows')}")
    if ra.get("mismatches") != 0 or ra.get("exhausted_rows"):
        sys.exit(f"ABORT row-audit mismatches/exhausted {ra.get('mismatches')},{ra.get('exhausted_rows')}")
    if ra.get("unprobed_count") != FILELESS_UNPROBED_COUNT:
        sys.exit(f"ABORT row-audit unprobed_count {ra.get('unprobed_count')}")
    if ra.get("derived_state") is not True:
        sys.exit(f"ABORT row-audit derived_state {ra.get('derived_state')}")
    if ra.get("batch") != 28 or ra.get("keys_total") != 54:
        sys.exit(f"ABORT row-audit batch/keys_total {ra.get('batch')},{ra.get('keys_total')}")
    if ra.get("input_sha256") != PIN_B28:
        sys.exit("ABORT row-audit input_sha256 != batch-keys pin")
    frag = ra.get("fragment_keys") or {}
    if set(frag.keys()) != set(FRAGMENT_KEYS):
        sys.exit(f"ABORT row-audit fragment_keys {sorted(frag.keys())} != {FRAGMENT_KEYS}")
    fm = ra.get("fileless_unprobed") or []
    if len(fm) != FILELESS_UNPROBED_COUNT or set(fm) & set(pass_keys):
        sys.exit(f"ABORT row-audit fileless_unprobed count {len(fm)} overlaps PASS keys")
    sr = ra.get("stop_rule") or ""
    if "pre-registered WIN-HALT" not in sr or "verdict not consumed" not in sr:
        sys.exit(f"ABORT row-audit stop_rule wording: {sr[:80]}")
    expected = set(ra.get("loss_rows", [])) | set(ra.get("win_rows", []))
    if set(pass_keys) != expected:
        missing = expected - set(pass_keys)
        extra = set(pass_keys) - expected
        sys.exit(f"ABORT status PASS keys != row-audit rows: missing {sorted(missing)} extra {sorted(extra)}")
    # every PASS row must be one of the 2 target WIN rows (result 1, published
    # WIN nodes); batch-28 has no loss rows
    for l in lines:
        toks = l.split()
        if toks[2] == "PASS":
            pl = toks[3].split(",")
            if pl[0] != "15000000":
                sys.exit(f"ABORT status-b28.log {toks[1]} PASS budget {pl[0]}")
            if toks[1] in TARGETS:
                if pl[1] != "1" or int(pl[2]) != STATUS_PASS_NODES[toks[1]]:
                    sys.exit(f"ABORT status-b28.log {toks[1]} PASS line {pl} is not the published WIN row")
            elif toks[1] in LOSS_ROWS:
                if pl[1] != "2" or int(pl[2]) != STATUS_LOSS_NODES[toks[1]]:
                    sys.exit(f"ABORT status-b28.log {toks[1]} PASS line {pl} is not the published LOSS row")
            else:
                sys.exit(f"ABORT status-b28.log {toks[1]} PASS line is neither a target WIN row nor a row-audit loss row")
    if set(TARGETS) & set(LOSS_ROWS):
        sys.exit("ABORT target/loss row id collision")
    # -- README results battery gates (published batch-28 README,
    #    whitespace-normalized so wrapped lines cannot defeat phrase checks)
    rd = re.sub(r"\s+", " ", open(os.path.join(SRC, "README-b28.md")).read())
    for phrase in ("aa001 WIN (honest label)", "aa002 WIN (honest label)"):
        if phrase not in rd:
            sys.exit(f"ABORT README lacks the {phrase.split()[0]} WIN honest-label phrase")
    if "13,183,855" not in rd or "6,527,041" not in rd:
        sys.exit("ABORT README lacks the aa001/aa002 node counts")
    if "30番目・31番目の unconsumed closure WIN候補" not in rd:
        sys.exit("ABORT README lacks the 30th/31st-unconsumed-candidate route statement")
    if "fileless UNPROBED" not in rd:
        sys.exit("ABORT README lacks the 52-key fileless UNPROBED statement")
    if "scrutiny owner C++" not in rd or "第二実装 gate pin" not in rd:
        sys.exit("ABORT README lacks the scrutiny-owner continuation")
    if "class 5343" not in rd or "Part CB" not in rd:
        sys.exit("ABORT README lacks the class-5343 Part CB identifier statement")
    # -- per-target raw cross-verification
    rows = []
    for key in TARGETS:
        bk = k28.get(key)
        if bk is None or int(bk["s5_index"]) != EXPECT_S5[key]:
            sys.exit(f"ABORT {key}: batch-28 s5_index {bk and bk.get('s5_index')}")
        if int(bk["membership_class_count"]) != EXPECT_MEMBERSHIP[key]:
            sys.exit(f"ABORT {key}: membership_class_count {bk.get('membership_class_count')}")
        r = parse_raw(key, k28, slog)
        r["source"] = "part-cb-batch28-win"
        r["s5_index"] = int(bk["s5_index"])
        r["membership_class_count"] = int(bk["membership_class_count"])
        r["expect_third"] = 1
        rows.append(r)
    # -- anchors/negatives (published constants, AR->BF->BK->BM->BS->BV->BW->BX->BY->CC provenance chain)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b28win-thirdimpl-input-v1",
                 "sources": {
                     "b28": ("sources/raw aa001.p1/p2 + aa002.p1/p2 + sources/status-b28.log + sources/row-audit-winhalt-b28.json + "
                             "batch-keys-b28.json + published batch-28 (Part CB) canonical outputs, publication "
                             "commits 39521983 (declaration) / a3dc8202 (scaffold) / 84d495e8 "
                             "(raws+status+row-audit) / 4f9d2cef (README+MANIFEST), commit-pinned raw fetch; "
                             "batch-28 batch-keys sha256 af19208f.."),
                     "b28_batch_keys_sha256": PIN_B28,
                     "b28_row_audit_winhalt_sha256": PIN_ROWAUDIT_B28,
                     "anchors": ("published Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK/BM/BS/BV/BW/BX/BY anchor/negative values, "
                                 "input CSVs byte-equality-checked against the published Part BF experiment "
                                 "(provenance chain AR -> BF -> BK -> BM -> BS -> BV -> BW -> BX -> BY -> CC)")},
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
    print("CC-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"])

if __name__ == "__main__":
    main()
