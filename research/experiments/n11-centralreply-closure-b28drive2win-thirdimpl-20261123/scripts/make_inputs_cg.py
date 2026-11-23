# make_inputs_cg.py -- machine-derive the Part CG third-impl input CSVs and
# rows.json for the batch-28 (class 5343) drive-2 WIN rows aa006/aa007 from
# the published batch-28 drive-2 (Part CD) canonical artifacts (zero hand
# transcription). Fail-closed: any unexpected field aborts.
#
# Reconstruction provenance (honest disclosure): the original Part CG
# declaration (2026-11-23T16:30:48Z, note section "Part CG 宣言", kit pin
# d7155bd9...) and the first Part CG takeover (commit d5e9acc2, 2026-11-23
# 18:01Z, re-registered maker pin 95e18953...) both vanished before
# publishing any scaffold/outputs: neither d7155bd9 nor 95e18953 bytes were
# ever published, so they are NOT inherited. This file is a fresh
# reconstruction from the published Part CC maker (sha256
# 8255d0adfe82ccc33d49c1339281fb18410748d165fa36e099529233249ab700,
# experiment n11-centralreply-closure-b28win-thirdimpl-20261123) with the
# declared deltas only: sources switched to the published Part CD (batch-28
# drive-2) canonical outputs, targets switched to the drive-2 WIN rows
# aa006/aa007, the Part CG schema strings, and this takeover provenance
# note in the header. Gate skeleton unchanged from Part CC. The
# machine-derived outputs are byte-verified against the published Part CD
# per-key input CSV pins (cdd84899.../493e0a58...), so every target field
# is machine-checked against published bytes.
#
# Batch-28 drive-2 specific gates (all honest):
#  - the published Part CD status.log carries 17 lines = 7 PASS rows
#    (aa001..aa007: 4 WIN aa001/aa002/aa006/aa007 + 1 LOSS aa003 + 2
#    EXHAUSTED aa004/aa005) + 4 WIN-HALT runner lines (aa001/aa002/aa006/
#    aa007, one per halted worker) + 2 EXHAUSTED lines + 4 TRUNCATED-RETRY
#    lines (aa004 P2 / aa005 P1 / aa006 P2 / aa007 P2).
#  - the 2 targets aa006/aa007 must each be a published in-budget WIN row
#    (result 1, published WIN nodes, WIN-HALT line present).
#  - the row-audit-cd battery gates: probed 7, win_rows [aa001, aa002,
#    aa006, aa007], loss_rows [aa003], exhausted_rows [aa004, aa005],
#    pass_rows 1, mismatches 0, fileless_unprobed = aa008..aa054 (47 keys),
#    derived_state true, stop_rule wording, input_sha256 machine
#    cross-check.
#  - README-cd result-phrase checks (aa006/aa007 WIN-HALT honest labels,
#    the two node counts, the fileless-47 statement, class 5343 / Part CD
#    identifiers, scrutiny-owner wording).
#  - anchor/negative battery: the anchor and negative constants must
#    equal the published Part CC rows.json arrays byte-for-field (the
#    published Part BF CSV pins b6174a3f/e13d2a6c/8e64b9ad/f19cd5a3 stay
#    the authority for CSV bytes).
#
# Sources (all commit-pinned raw fetches of the PUBLISHED canonical
# batch-28 drive-2 (Part CD) publication, experiment
# n11-centralreply-closure-class5343-batch28-drive2-20261123; local mirrors
# sha-verified against the published CD MANIFEST-sha256 (56 lines) and the
# Part CC MANIFEST):
#  - sources/raw/aa00{6,7}.{p1,p2}.out -- the published Part CD replica WIN
#    outputs (raws commit).
#  - sources/status-cd.log -- published Part CD runner status.log (17 lines).
#  - sources/row-audit-cd.json -- published Part CD winhalt audit.
#  - sources/batch-keys-cd.json -- published batch-28 input declaration
#    (54 keys, class 5343, identical bytes with the Part CB/CB-scaffold pin).
#  - sources/README-cd.md -- published Part CD README.
#  - sources/published-input/aa00{6,7}.input.csv -- published Part CD
#    per-key input CSVs.
#  - sources/published-input-bf/{k02a,l1a,ng1,ng2}.input.csv -- published
#    Part BF anchor/negative input CSVs (provenance chain AR -> BF -> BK ->
#    BM -> BS -> BV -> BW -> BX -> BY -> CC -> CG).
#  - sources/published-rows-cc.json -- the published Part CC rows.json
#    (b7222edf...) used ONLY as the anchor/negative equality battery.
#
# NOTE: verdicts are NOT consumed anywhere; this experiment is verdict-level
# corroboration literature only. The standard 11x11 empty board, the 19
# central-reply roots, class 5343 and every key (aa001..aa054) remain
# UNKNOWN. WIN/LOSS adoption is a separate declared adoption Part with the
# pinned fail-closed merger only; the scrutiny owner C++ second-implementation
# gate pin 9193f5b6... is NOT actuated by this experiment.
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")

PIN_BCD = "af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5"
PIN_STATUS_CD = "343097c268425cc62263935f1063c26689515bc797c68bbdb82389c713952c98"
PIN_README_CD = "338fc1361a2aaaa0276b9b050cf2cc0a3073f15fc64f382f5edb7e784e5dd9e6"
PIN_ROWAUDIT_CD = "3e86a32b847b5799594be5fbee6624878deadf02990940b2503f931d7af30e91"
PIN_RAW = {
    "aa006.p1": "c94558829259c8edfdc5d204806f0b0fbf3f4bed49fdc483b40862f2643ab2a4",
    "aa006.p2": "e157a451ab33af09596537e1357473fe1fd21812e63759a8e91127bf999b7927",
    "aa007.p1": "ad2870eaf14d7bd72858a018a65e86613d00d5c61931afe1ac2d6c9d9447011d",
    "aa007.p2": "bbacf3e3c37964cf4d093938f566d63f66623a229662d9324094000aa411b93c",
}
PIN_PUB_INPUT = {
    "aa006": "cdd84899d9859ea5a2971e96e6d6b313eb0bd1026dc034ea38d392e242f6eddf",
    "aa007": "493e0a58f74e898ef33f83838dddfd6e246efd2767e27fc12c80129c4da4be8a",
}
PIN_PUB_ROWS_CC = "b7222edf773c541fafac165d16355fd1f9469ec31bc233f78a35037fad542d39"
PIN_PUB_INPUT_BF = {
    "k02a": "b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887",
    "l1a": "e13d2a6c5bbaa34833dcaf8bfaaa91f99393942281f001552cb8af49cca8c98a",
    "ng1": "8e64b9ade1c04122ac4bdc5fa5129b5fca6cfac742ed92cb149f9ffb80ad0b09",
    "ng2": "f19cd5a30b0b868f0a0c7f12a6c47376c8ceb6e862f5c769fb14bdf74e8997dc",
}

TARGETS = ["aa006", "aa007"]
# published Part CD rows outside the 2 targets (status/row-audit battery):
STATUS_PASS_NODES = {  # key -> (result, nodes) for every PASS row (17-line status-cd.log)
    "aa001": (1, 13183855), "aa002": (1, 6527041),
    "aa003": (2, 4070373),
    "aa004": (0, 15000000), "aa005": (0, 15000000),
    "aa006": (1, 14303810), "aa007": (1, 13483540),
}
STATUS_EXPECT_LINES = 17
STATUS_EXPECT_PASS = 7
STATUS_EXPECT_WINHALT = 4
STATUS_EXPECT_EXHAUSTED = 2
STATUS_EXPECT_RETRY = 4
WINHALT_KEYS = {"aa001", "aa002", "aa006", "aa007"}
EXHAUSTED_KEYS = {"aa004", "aa005"}
RETRY_KEYS = {"aa004", "aa005", "aa006", "aa007"}
FILELESS_UNPROBED_COUNT = 47
EXPECT_S5 = {"aa006": 129823, "aa007": 135236}
EXPECT_MEMBERSHIP = {"aa006": 4, "aa007": 4}
EXPECT_REPLICA = {"aa006": 14303810, "aa007": 13483540}  # published 2-pass node-exact WIN rows

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
    # status.log cross-verification (Part CD canonical format)
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
    for fname, pin in (("batch-keys-cd.json", PIN_BCD), ("status-cd.log", PIN_STATUS_CD),
                       ("README-cd.md", PIN_README_CD), ("row-audit-cd.json", PIN_ROWAUDIT_CD)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    for k, pin in PIN_RAW.items():
        got = sha256(os.path.join(SRC, "raw", k + ".out"))
        if got != pin:
            sys.exit(f"ABORT raw {k} sha {got} != pin {pin}")
    got = sha256(os.path.join(SRC, "published-rows-cc.json"))
    if got != PIN_PUB_ROWS_CC:
        sys.exit(f"ABORT published-rows-cc.json sha {got} != pin {PIN_PUB_ROWS_CC}")
    bk28 = json.load(open(os.path.join(SRC, "batch-keys-cd.json")))
    if int(bk28["class_index"]) != 5343:
        sys.exit(f"ABORT class_index {bk28.get('class_index')}")
    if bk28.get("schema") != "n11-centralreply-closure-class5343-batch28-input-v1":
        sys.exit(f"ABORT batch-keys schema {bk28.get('schema')}")
    k28 = {k["key_id"]: k for k in bk28["keys"]}
    if len(k28) != 54:
        sys.exit(f"ABORT batch keys count {len(k28)} != 54")
    if not re.fullmatch(r"aa[0-9]{3}", TARGETS[0]) or not re.fullmatch(r"aa[0-9]{3}", TARGETS[1]):
        sys.exit("ABORT batch-28 key ids must be the 2-char aa### form")
    # -- status log battery gates (published Part CD canonical runner log):
    #    17 lines = 7 PASS + 4 WIN-HALT + 2 EXHAUSTED + 4 TRUNCATED-RETRY;
    #    PASS key set must equal the row-audit probed rows exactly; only the
    #    4 win-halted workers carry WIN-HALT lines; truncated-retry keys match
    #    the published truncated sidecars.
    slog = open(os.path.join(SRC, "status-cd.log")).read()
    lines = [l for l in slog.splitlines() if l.strip()]
    if len(lines) != STATUS_EXPECT_LINES:
        sys.exit(f"ABORT status-cd.log line count {len(lines)} != {STATUS_EXPECT_LINES}")
    kinds = {}
    for ln in lines:
        toks = ln.split()
        kinds[toks[2]] = kinds.get(toks[2], 0) + 1
    if kinds.get("PASS") != STATUS_EXPECT_PASS:
        sys.exit(f"ABORT status-cd.log PASS lines {kinds.get('PASS')} != {STATUS_EXPECT_PASS}")
    if kinds.get("WIN-HALT") != STATUS_EXPECT_WINHALT:
        sys.exit(f"ABORT status-cd.log WIN-HALT lines {kinds.get('WIN-HALT')} != {STATUS_EXPECT_WINHALT}")
    if kinds.get("EXHAUSTED") != STATUS_EXPECT_EXHAUSTED:
        sys.exit(f"ABORT status-cd.log EXHAUSTED lines {kinds.get('EXHAUSTED')} != {STATUS_EXPECT_EXHAUSTED}")
    n_retry = sum(1 for kk in ("P1-TRUNCATED-RETRY", "P2-TRUNCATED-RETRY") if kk in kinds for _ in [0])
    n_retry = kinds.get("P1-TRUNCATED-RETRY", 0) + kinds.get("P2-TRUNCATED-RETRY", 0)
    if n_retry != STATUS_EXPECT_RETRY:
        sys.exit(f"ABORT status-cd.log TRUNCATED-RETRY lines {n_retry} != {STATUS_EXPECT_RETRY}")
    if set(kinds) != {"PASS", "WIN-HALT", "EXHAUSTED", "P1-TRUNCATED-RETRY", "P2-TRUNCATED-RETRY"}:
        sys.exit(f"ABORT status-cd.log carries unexpected line kinds: {sorted(kinds)}")
    pass_keys = [l.split()[1] for l in lines if l.split()[2] == "PASS"]
    if len(pass_keys) != len(set(pass_keys)):
        sys.exit("ABORT status-cd.log duplicate PASS keys")
    if set(pass_keys) != set(STATUS_PASS_NODES):
        sys.exit(f"ABORT status-cd.log PASS keys {sorted(pass_keys)} != published rows")
    winhalt_keys = {l.split()[1] for l in lines if l.split()[2] == "WIN-HALT"}
    if winhalt_keys != WINHALT_KEYS:
        sys.exit(f"ABORT status-cd.log WIN-HALT keys {sorted(winhalt_keys)} != {sorted(WINHALT_KEYS)}")
    exhausted_keys = {l.split()[1] for l in lines if l.split()[2] == "EXHAUSTED"}
    if exhausted_keys != EXHAUSTED_KEYS:
        sys.exit(f"ABORT status-cd.log EXHAUSTED keys {sorted(exhausted_keys)} != {sorted(EXHAUSTED_KEYS)}")
    retry_keys = {l.split()[1] for l in lines if l.split()[2] in ("P1-TRUNCATED-RETRY", "P2-TRUNCATED-RETRY")}
    if retry_keys != RETRY_KEYS:
        sys.exit(f"ABORT status-cd.log TRUNCATED-RETRY keys {sorted(retry_keys)} != {sorted(RETRY_KEYS)}")
    # every PASS row must reproduce its published (result, nodes) pair
    for l in lines:
        toks = l.split()
        if toks[2] == "PASS":
            pl = toks[3].split(",")
            want = STATUS_PASS_NODES[toks[1]]
            if pl[0] != "15000000" or int(pl[1]) != want[0] or int(pl[2]) != want[1]:
                sys.exit(f"ABORT status-cd.log {toks[1]} PASS line {pl} is not the published row {want}")
        elif toks[2] == "EXHAUSTED":
            pl = toks[3].split(",")
            if pl != ["15000000", "0", "15000000"]:
                sys.exit(f"ABORT status-cd.log {toks[1]} EXHAUSTED line {pl} is not the honest-UNKNOWN row")
    # -- published row-audit-cd battery gates (Part CD halt-time audit)
    ra = json.load(open(os.path.join(SRC, "row-audit-cd.json")))
    if ra.get("schema") != "n11-centralreply-closure-class5343-batch28-rowaudit-winhalt-v1":
        sys.exit(f"ABORT row-audit schema {ra.get('schema')}")
    if ra.get("class_index") != 5343 or ra.get("probed") != 7 or ra.get("pass_rows") != 1:
        sys.exit(f"ABORT row-audit header {ra.get('class_index')},{ra.get('probed')},{ra.get('pass_rows')}")
    if ra.get("win_rows") != ["aa001", "aa002", "aa006", "aa007"]:
        sys.exit(f"ABORT row-audit win_rows {ra.get('win_rows')}")
    if ra.get("loss_rows") != ["aa003"]:
        sys.exit(f"ABORT row-audit loss_rows {ra.get('loss_rows')}")
    if ra.get("exhausted_rows") != ["aa004", "aa005"]:
        sys.exit(f"ABORT row-audit exhausted_rows {ra.get('exhausted_rows')}")
    if ra.get("mismatches") != 0:
        sys.exit(f"ABORT row-audit mismatches {ra.get('mismatches')}")
    if ra.get("unprobed_count") != FILELESS_UNPROBED_COUNT:
        sys.exit(f"ABORT row-audit unprobed_count {ra.get('unprobed_count')}")
    if ra.get("derived_state") is not True:
        sys.exit(f"ABORT row-audit derived_state {ra.get('derived_state')}")
    if ra.get("batch") != 28 or ra.get("keys_total") != 54:
        sys.exit(f"ABORT row-audit batch/keys_total {ra.get('batch')},{ra.get('keys_total')}")
    if ra.get("input_sha256") != PIN_BCD:
        sys.exit("ABORT row-audit input_sha256 != batch-keys pin")
    frag = ra.get("fragment_keys") or {}
    if frag != {}:
        sys.exit(f"ABORT row-audit fragment_keys {sorted(frag.keys())} != empty")
    fm = ra.get("fileless_unprobed") or []
    expected_fileless = [f"aa{i:03d}" for i in range(8, 55)]
    if fm != expected_fileless or len(fm) != FILELESS_UNPROBED_COUNT or set(fm) & set(pass_keys):
        sys.exit(f"ABORT row-audit fileless_unprobed != aa008..aa054 (47) disjoint from PASS keys")
    sr = ra.get("stop_rule") or ""
    if "pre-registered WIN-HALT" not in sr or "verdict not consumed" not in sr:
        sys.exit(f"ABORT row-audit stop_rule wording: {sr[:80]}")
    expected = set(ra.get("loss_rows", [])) | set(ra.get("win_rows", [])) | set(ra.get("exhausted_rows", []))
    if set(pass_keys) != expected:
        missing = expected - set(pass_keys)
        extra = set(pass_keys) - expected
        sys.exit(f"ABORT status PASS keys != row-audit rows: missing {sorted(missing)} extra {sorted(extra)}")
    # -- README results battery gates (published Part CD README,
    #    whitespace-normalized so wrapped lines cannot defeat phrase checks)
    rd = re.sub(r"\s+", " ", open(os.path.join(SRC, "README-cd.md")).read())
    for phrase in ("aa006 WIN-HALT (result 1・nodes 14,303,810)",
                   "aa007 WIN-HALT (result 1・nodes 13,483,540)"):
        if phrase not in rd:
            sys.exit(f"ABORT README lacks the {phrase.split()[0]} WIN-HALT published-row phrase")
    if "14,303,810" not in rd or "13,483,540" not in rd:
        sys.exit("ABORT README lacks the aa006/aa007 node counts")
    if "WIN 4 (aa001, aa002, aa006, aa007)" not in rd:
        sys.exit("ABORT README lacks the row-audit WIN-4 statement")
    if "EXHAUSTED 2 (aa004, aa005)" not in rd:
        sys.exit("ABORT README lacks the row-audit EXHAUSTED-2 statement")
    if "fileless 47" not in rd:
        sys.exit("ABORT README lacks the fileless-47 statement")
    if "scrutiny owner C++" not in rd or "9193f5b6" not in rd:
        sys.exit("ABORT README lacks the scrutiny-owner continuation")
    if "class 5343" not in rd or "Part CD" not in rd:
        sys.exit("ABORT README lacks the class-5343 Part CD identifier statement")
    if "UNKNOWNのまま" not in rd:
        sys.exit("ABORT README lacks the UNKNOWN-stays statement")
    # -- anchor/negative battery: constants equal the published Part CC rows.json
    rcc = json.load(open(os.path.join(SRC, "published-rows-cc.json")))
    if rcc.get("schema") != "n11-centralreply-closure-b28win-thirdimpl-input-v1":
        sys.exit(f"ABORT published-rows-cc schema {rcc.get('schema')}")
    if rcc.get("consumed_into_canonical_cache") is not False:
        sys.exit("ABORT published-rows-cc consumed_into_canonical_cache not False")
    if [t["key_id"] for t in rcc.get("targets", [])] != ["aa001", "aa002"]:
        sys.exit(f"ABORT published-rows-cc targets {[t['key_id'] for t in rcc.get('targets', [])]}")
    if any(t.get("replica_result") != 1 for t in rcc.get("targets", [])):
        sys.exit("ABORT published-rows-cc targets are not the Part CC WIN rows")
    for a_cc in rcc.get("anchors", []):
        hit = [a for a in ANCHORS if a[0] == a_cc["key_id"]]
        if len(hit) != 1:
            sys.exit(f"ABORT anchor {a_cc['key_id']} missing from the published Part CC anchor battery")
        a = hit[0]
        if (a_cc["lo"], a_cc["hi"], a_cc["legal"], a_cc["expect_third"],
                a_cc["anchor_expansions"], a_cc["anchor_ttHits"], a_cc["expect_kind"]) != (a[1], a[2], a[3], a[4], a[5], a[6], a[7]):
            sys.exit(f"ABORT anchor {a_cc['key_id']} differs from the published Part CC values")
    if len(rcc.get("anchors", [])) != len(ANCHORS):
        sys.exit("ABORT published-rows-cc anchor count")
    for ng_cc in rcc.get("negatives", []):
        hit = [n for n in NEGATIVES if n["key_id"] == ng_cc["key_id"]]
        if len(hit) != 1:
            sys.exit(f"ABORT negative {ng_cc['key_id']} missing from the published Part CC battery")
        n = hit[0]
        if (ng_cc["lo"], ng_cc["hi"], ng_cc["legal"], ng_cc["stones"], ng_cc["why"]) != (n["lo"], n["hi"], n["legal"], n["stones"], n["why"]):
            sys.exit(f"ABORT negative {ng_cc['key_id']} differs from the published Part CC values")
    if len(rcc.get("negatives", [])) != len(NEGATIVES):
        sys.exit("ABORT published-rows-cc negative count")
    # -- per-target raw cross-verification
    rows = []
    for key in TARGETS:
        bk = k28.get(key)
        if bk is None or int(bk["s5_index"]) != EXPECT_S5[key]:
            sys.exit(f"ABORT {key}: batch-28 s5_index {bk and bk.get('s5_index')}")
        if int(bk["membership_class_count"]) != EXPECT_MEMBERSHIP[key]:
            sys.exit(f"ABORT {key}: membership_class_count {bk.get('membership_class_count')}")
        r = parse_raw(key, k28, slog)
        r["source"] = "part-cd-batch28-win"
        r["s5_index"] = int(bk["s5_index"])
        r["membership_class_count"] = int(bk["membership_class_count"])
        r["expect_third"] = 1
        rows.append(r)
    # -- anchors/negatives (published constants, AR->BF->BK->BM->BS->BV->BW->BX->BY->CC->CG provenance chain)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b28drive2win-thirdimpl-input-v1",
                 "sources": {
                     "b28drive2": ("sources/raw aa006.p1/p2 + aa007.p1/p2 + sources/status-cd.log + sources/row-audit-cd.json + "
                                   "batch-keys-cd.json + published batch-28 drive-2 (Part CD) canonical outputs "
                                   "(experiment n11-centralreply-closure-class5343-batch28-drive2-20261123), commit-pinned raw fetch; "
                                   "batch-28 batch-keys sha256 af19208f.."),
                     "b28_batch_keys_sha256": PIN_BCD,
                     "b28_row_audit_winhalt_sha256": PIN_ROWAUDIT_CD,
                     "anchors": ("published Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK/BM/BS/BV/BW/BX/BY/CC anchor/negative values, "
                                 "input CSVs byte-equality-checked against the published Part BF experiment and the "
                                 "published Part CC rows.json (provenance chain AR -> BF -> BK -> BM -> BS -> BV -> BW -> BX -> BY -> CC -> CG)")},
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
    print("CG-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"])

if __name__ == "__main__":
    main()
