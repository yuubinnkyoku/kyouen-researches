# make_inputs_by.py -- machine-derive the Part BY third-impl input CSVs and
# rows.json for the batch-27 (class 13342, Part BR) WIN row o002 from the
# published batch-27 canonical artifacts (zero hand transcription).
# Fail-closed: any unexpected field aborts.
#
# Adapted from the published Part BX maker (sha256
# e1def905912942aa34024fc16f1ed55788e283994d4f4e33a72d012d26d1f49b,
# experiment n11-centralreply-closure-b25win-thirdimpl-20261123, itself from
# BW f94d6e4f... b24win) for the batch-27 canonical publication. Batch-27
# specific gates (all honest):
#  - the published batch-27 status.log carries 6 lines = 4 LOSS PASS rows
#    (o001/o003/o005/o007, adoption candidates only, result 2) + 1 WIN PASS
#    row (o002, result 1, the sole target) + 1 WIN-HALT runner line; no
#    truncated-retry lines (the o009 fragment is NOT in status.log: its p1
#    is a complete single pass kept as bookkeeping only, p2 was cut by the
#    260s bound; evidence false, probed false - UNPROBED).
#  - every PASS row must be either the target WIN row (result 1, published
#    WIN nodes) or one of the row-audit loss_rows (result 2, published LOSS
#    nodes) - BW-style loss-row gate restored (batch-25 had no loss rows).
#  - the row-audit battery gates: win_rows [o002], loss_rows [o001,o003,
#    o005,o007], pass_rows 4, probed 5, unprobed_count 49, fragment_keys
#    exactly {"o009": p1_complete_single_pass true, p2_complete_single_pass
#    false, evidence false, probed false}, derived_state true, stop_rule
#    wording, input_sha256 machine cross-check.
#  - README-b27 result-phrase checks (o002 WIN honest label, 29th
#    unconsumed closure WIN candidate, 4,589,084 nodes, the 4 LOSS node
#    counts, class 13342 / Part BR identifiers, scrutiny-owner wording).
#
# Sources (all commit-pinned raw fetches of the PUBLISHED canonical batch-27
# publication, experiment n11-centralreply-closure-class13342-batch27-
# 20261123, publication commits 14ee1873 (declaration) / 93ef3f89 (scaffold)
# / d2e345e6 (takeover amendment) / 28cf8c2a (raws+status+row-audit) /
# a55813ee (README+MANIFEST); local mirrors sha-verified against the
# published MANIFEST-sha256 (92 files) and pinned fetches):
#  - sources/raw/o002.{p1,p2}.out -- the published batch-27 replica WIN
#    outputs (raws commit).
#  - sources/status-b27.log -- published batch-27 runner status.log.
#  - sources/row-audit-winhalt-b27.json -- published batch-27 winhalt audit.
#  - sources/batch-keys-b27.json -- published batch-27 input declaration
#    (54 keys, class 13342).
#  - sources/README-b27.md -- published batch-27 README.
#  - sources/published-input/o002.input.csv -- published batch-27 per-key
#    input CSV.
#  - sources/published-input-bf/{k02a,l1a,ng1,ng2}.input.csv -- published
#    Part BF anchor/negative input CSVs (provenance chain AR -> BF -> BK ->
#    BM -> BS -> BV -> BW -> BX -> BY).
#
# NOTE: verdicts are NOT consumed anywhere; this experiment is verdict-level
# corroboration literature only. The standard 11x11 empty board, the 19
# central-reply roots, class 13342 and every key (o001..o054) remain
# UNKNOWN. WIN/LOSS adoption is a separate declared adoption Part with the
# pinned fail-closed merger only; the scrutiny owner C++ second-implementation
# gate pin 9193f5b6... wait is NOT actuated by this experiment.
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")

PIN_B27 = "67814ed6287d68d6e97212c931dce2b7ee585219e20b4d43edb621632220a014"
PIN_STATUS_B27 = "50a4f407b369e06f9569238d1b0c35deb02dfad7d839cf57b2fc97a389512ca9"
PIN_README_B27 = "1ee2666eeac4130d4f6d7515e46ca9a5cc8b19bffdd5f898ff2cf7c0415288d6"
PIN_ROWAUDIT_B27 = "530fe94712c79bc73f0df4933e2778bc90eb372675fcb7f5d9ca2d4236ac03ed"
PIN_RAW = {
    "o002.p1": "56fdf7a4bb7bfdaf77edcde86e6cf20c15a8658c7e62e35cc60379f629f265ea",
    "o002.p2": "cf1ce8ff0feb97e6b003b7c7bc128e65ad5f9b777dd413f2c4abbb5dfd629a6e",
}
PIN_PUB_INPUT = {
    "o002": "d083f5c300a3f9286703c53fcd6a302d9f24b69516720891ad89f92949dfe560",
}
PIN_PUB_INPUT_BF = {
    "k02a": "b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887",
    "l1a": "e13d2a6c5bbaa34833dcaf8bfaaa91f99393942281f001552cb8af49cca8c98a",
    "ng1": "8e64b9ade1c04122ac4bdc5fa5129b5fca6cfac742ed92cb149f9ffb80ad0b09",
    "ng2": "f19cd5a30b0b868f0a0c7f12a6c47376c8ceb6e862f5c769fb14bdf74e8997dc",
}

TARGETS = ["o002"]
LOSS_ROWS = ["o001", "o003", "o005", "o007"]  # adoption candidates only
EXPECT_S5 = {"o002": 209134}
EXPECT_REPLICA = {"o002": 4589084}  # published 2-pass node-exact WIN row
EXPECT_LOSS_NODES = {"o001": 2829495, "o003": 2400082, "o005": 2093259, "o007": 6644942}
# batch-27 canonical status.log: 4 LOSS PASS lines + 1 WIN PASS line + 1
# WIN-HALT runner line; no truncated-retry lines, no fragment lines
STATUS_PASS_NODES = {"o002": 4589084}
STATUS_LOSS_NODES = {"o001": 2829495, "o003": 2400082, "o005": 2093259, "o007": 6644942}
STATUS_EXPECT_LINES = 6
STATUS_EXPECT_PASS = 5
STATUS_EXPECT_RETRY = 0
# the o009 fragment (UNPROBED): complete p1 single pass (bookkeeping only)
# + p2 cut by the 260s bound; must NOT appear as a PASS/retry status row
FRAGMENT_KEYS = ["o009"]

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
    # status.log cross-verification (batch-27 canonical format)
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
    for fname, pin in (("batch-keys-b27.json", PIN_B27), ("status-b27.log", PIN_STATUS_B27),
                       ("README-b27.md", PIN_README_B27), ("row-audit-winhalt-b27.json", PIN_ROWAUDIT_B27)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    for k, pin in PIN_RAW.items():
        got = sha256(os.path.join(SRC, "raw", k + ".out"))
        if got != pin:
            sys.exit(f"ABORT raw {k} sha {got} != pin {pin}")
    bk27 = json.load(open(os.path.join(SRC, "batch-keys-b27.json")))
    if int(bk27["class_index"]) != 13342:
        sys.exit(f"ABORT class_index {bk27.get('class_index')}")
    if bk27.get("schema") != "n11-centralreply-closure-class13342-batch27-input-v1":
        sys.exit(f"ABORT batch-keys schema {bk27.get('schema')}")
    k27 = {k["key_id"]: k for k in bk27["keys"]}
    if len(k27) != 54:
        sys.exit(f"ABORT batch keys count {len(k27)} != 54")
    # -- status log battery gates (published batch-27 canonical runner log):
    #    6 lines = 4 LOSS PASS + 1 WIN PASS + 1 WIN-HALT; PASS key set must
    #    equal the row-audit win_rows | loss_rows exactly; no truncated-retry
    #    lines; the o009 fragment must NOT appear as a status row.
    slog = open(os.path.join(SRC, "status-b27.log")).read()
    lines = [l for l in slog.splitlines() if l.strip()]
    if len(lines) != STATUS_EXPECT_LINES:
        sys.exit(f"ABORT status-b27.log line count {len(lines)} != {STATUS_EXPECT_LINES}")
    kinds = {}
    for ln in lines:
        toks = ln.split()
        kinds[toks[2]] = kinds.get(toks[2], 0) + 1
    if kinds.get("PASS") != STATUS_EXPECT_PASS:
        sys.exit(f"ABORT status-b27.log PASS lines {kinds.get('PASS')} != {STATUS_EXPECT_PASS}")
    for bad_kind in ("P1-TRUNCATED-RETRY", "P2-TRUNCATED-RETRY", "EXHAUSTED", "FAIL", "MISMATCH"):
        if bad_kind in kinds:
            sys.exit(f"ABORT status-b27.log carries unexpected line kind {bad_kind}")
    n_winhalt = sum(1 for l in lines if l.split()[2] == "WIN-HALT")
    if n_winhalt != 1:
        sys.exit(f"ABORT status-b27.log WIN-HALT lines {n_winhalt} != 1")
    if kinds.get("PASS", 0) + n_winhalt != len(lines):
        sys.exit(f"ABORT status-b27.log carries unexpected line kinds: {sorted(kinds)}")
    pass_keys = [l.split()[1] for l in lines if l.split()[2] == "PASS"]
    if len(pass_keys) != len(set(pass_keys)):
        sys.exit("ABORT status-b27.log duplicate PASS keys")
    for fk in FRAGMENT_KEYS:
        if fk in pass_keys:
            sys.exit(f"ABORT fragment {fk} appears as a status PASS row (fragments are UNPROBED bookkeeping)")
    # -- published row-audit-winhalt battery gates (batch-27 halt-time audit)
    ra = json.load(open(os.path.join(SRC, "row-audit-winhalt-b27.json")))
    if ra.get("schema") != "n11-centralreply-closure-class13342-batch27-rowaudit-winhalt-v1":
        sys.exit(f"ABORT row-audit schema {ra.get('schema')}")
    if ra.get("class_index") != 13342 or ra.get("probed") != 5 or ra.get("pass_rows") != 4:
        sys.exit(f"ABORT row-audit header {ra.get('class_index')},{ra.get('probed')},{ra.get('pass_rows')}")
    if ra.get("win_rows") != ["o002"]:
        sys.exit(f"ABORT row-audit win_rows {ra.get('win_rows')}")
    if ra.get("loss_rows") != ["o001", "o003", "o005", "o007"]:
        sys.exit(f"ABORT row-audit loss_rows {ra.get('loss_rows')}")
    if ra.get("mismatches") != 0 or ra.get("exhausted_rows"):
        sys.exit(f"ABORT row-audit mismatches/exhausted {ra.get('mismatches')},{ra.get('exhausted_rows')}")
    if ra.get("unprobed_count") != 49:
        sys.exit(f"ABORT row-audit unprobed_count {ra.get('unprobed_count')}")
    if ra.get("derived_state") is not True:
        sys.exit(f"ABORT row-audit derived_state {ra.get('derived_state')}")
    if ra.get("batch") != 27 or ra.get("keys_total") != 54:
        sys.exit(f"ABORT row-audit batch/keys_total {ra.get('batch')},{ra.get('keys_total')}")
    if ra.get("input_sha256") != PIN_B27:
        sys.exit("ABORT row-audit input_sha256 != batch-keys pin")
    frag = ra.get("fragment_keys") or {}
    if set(frag.keys()) != set(FRAGMENT_KEYS):
        sys.exit(f"ABORT row-audit fragment_keys {sorted(frag.keys())} != {FRAGMENT_KEYS}")
    for fk, fv in frag.items():
        if fv.get("p1_complete_single_pass") is not True or fv.get("p2_complete_single_pass") is not False:
            sys.exit(f"ABORT row-audit fragment {fk} pass-completeness {fv}")
        if fv.get("evidence") is not False or fv.get("probed") is not False:
            sys.exit(f"ABORT row-audit fragment {fk} evidence/probed {fv}")
    fm = ra.get("fileless_unprobed") or []
    if len(fm) != 48 or set(fm) & set(pass_keys):
        sys.exit(f"ABORT row-audit fileless_unprobed count {len(fm)} overlaps PASS keys")
    sr = ra.get("stop_rule") or ""
    if "pre-registered WIN-HALT" not in sr or "verdict not consumed" not in sr:
        sys.exit(f"ABORT row-audit stop_rule wording: {sr[:80]}")
    expected = set(ra.get("loss_rows", [])) | set(ra.get("win_rows", []))
    if set(pass_keys) != expected:
        missing = expected - set(pass_keys)
        extra = set(pass_keys) - expected
        sys.exit(f"ABORT status PASS keys != row-audit rows: missing {sorted(missing)} extra {sorted(extra)}")
    # every PASS row must be the target WIN row (result 1, published WIN
    # nodes) or one of the row-audit loss rows (result 2, published LOSS
    # nodes) - BW-style loss-row gate restored
    for l in lines:
        toks = l.split()
        if toks[2] == "PASS":
            pl = toks[3].split(",")
            if pl[0] != "15000000":
                sys.exit(f"ABORT status-b27.log {toks[1]} PASS budget {pl[0]}")
            if toks[1] in TARGETS:
                if pl[1] != "1" or int(pl[2]) != STATUS_PASS_NODES[toks[1]]:
                    sys.exit(f"ABORT status-b27.log {toks[1]} PASS line {pl} is not the published WIN row")
            elif toks[1] in LOSS_ROWS:
                if pl[1] != "2" or int(pl[2]) != STATUS_LOSS_NODES[toks[1]]:
                    sys.exit(f"ABORT status-b27.log {toks[1]} PASS line {pl} is not the published LOSS row")
            else:
                sys.exit(f"ABORT status-b27.log {toks[1]} PASS line is neither a target WIN row nor a row-audit loss row")
    if set(TARGETS) & set(LOSS_ROWS):
        sys.exit("ABORT target/loss row id collision")
    # -- README results battery gates (published batch-27 README)
    rd = open(os.path.join(SRC, "README-b27.md")).read()
    if "o002 WIN (honest label)" not in rd:
        sys.exit("ABORT README lacks the o002 WIN results line")
    if "4,589,084" not in rd:
        sys.exit("ABORT README lacks the o002 node count")
    if "29番目の unconsumed closure WIN候補" not in rd:
        sys.exit("ABORT README lacks the 29th-unconsumed-candidate route statement")
    if "2,829,495 / 2,400,082 / 2,093,259 / 6,644,942" not in rd:
        sys.exit("ABORT README lacks the 4 LOSS row node counts")
    if "o001/o003/o005/o007 はいずれも LOSS (採用候補のみ・verdict不消費)" not in rd:
        sys.exit("ABORT README lacks the 4-LOSS adoption-candidates statement")
    if "fragment o009 (UNPROBED)" not in rd:
        sys.exit("ABORT README lacks the o009 fragment UNPROBED statement")
    if "scrutiny owner C++第二実装 gate pin" not in rd:
        sys.exit("ABORT README lacks the scrutiny-owner continuation")
    if "class 13342" not in rd or "Part BR" not in rd:
        sys.exit("ABORT README lacks the class-13342 Part BR identifier statement")
    # -- per-target raw cross-verification
    rows = []
    for key in TARGETS:
        bk = k27.get(key)
        if bk is None or int(bk["s5_index"]) != EXPECT_S5[key]:
            sys.exit(f"ABORT {key}: batch-27 s5_index {bk and bk.get('s5_index')}")
        r = parse_raw(key, k27, slog)
        r["source"] = "part-br-batch27-win"
        r["s5_index"] = int(bk["s5_index"])
        r["membership_class_count"] = int(bk["membership_class_count"])
        r["expect_third"] = 1
        rows.append(r)
    # -- anchors/negatives (published constants, AR->BF->BK->BM->BS->BV->BW->BX->BY provenance chain)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b27win-thirdimpl-input-v1",
                 "sources": {
                     "b27": ("sources/raw o002.p1/p2 + sources/status-b27.log + sources/row-audit-winhalt-b27.json + "
                             "batch-keys-b27.json + published batch-27 (Part BR) canonical outputs, publication "
                             "commits 14ee1873 (declaration) / 93ef3f89 (scaffold) / d2e345e6 (takeover "
                             "amendment) / 28cf8c2f (raws+status+row-audit) / a55813ee (README+MANIFEST), "
                             "commit-pinned raw fetch; batch-27 batch-keys sha256 67814ed6.."),
                     "b27_batch_keys_sha256": PIN_B27,
                     "b27_row_audit_winhalt_sha256": PIN_ROWAUDIT_B27,
                     "anchors": ("published Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK/BM/BS/BV/BW/BX anchor/negative values, "
                                 "input CSVs byte-equality-checked against the published Part BF experiment "
                                 "(provenance chain AR -> BF -> BK -> BM -> BS -> BV -> BW -> BX -> BY)")},
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
    print("BY-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"])

if __name__ == "__main__":
    main()
