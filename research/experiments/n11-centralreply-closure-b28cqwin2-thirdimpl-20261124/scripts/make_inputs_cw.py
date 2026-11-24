# make_inputs_cw.py -- machine-derive the Part CW third-impl input CSVs and
# rows.json for the TWO published batch-28 (closure class 5343) Part CQ
# 20M-reprobe NEWLY-SOLVED WIN rows aa004 (key 1171516445255794689,0, legal 91,
# nodes 15,616,012) / aa035 (key 1152921504606846978,4228, legal 96, nodes
# 15,424,243) -- both UNCONSUMED honest probe-level labels, from the published
# canonical artifacts (zero hand transcription). Fail-closed: any unexpected
# field aborts.
#
# Adapted from the published Part CR maker (make_inputs_cr.py, sha256
# 364a217f5248a0dc7a8cd7fab7f4dc8e8a3c4c111fff21b9d7c31ded06e1498e, experiment n11-centralreply-closure-class34269-batch30drive1-
# thirdimpl-20261123, itself from the published Part CM maker f926b5be... /
# CL 177c4409 / CC 8255d0ad / BY 359aebef / BX e1def905 / BW f94d6e4f).
# Declared deltas (all in the Part CW declaration before execution):
# (a) sources switch from the Part CP batch-30 drive-1 experiment (class
#     34269) to the published Part CQ batch-28 EXHAUSTED-11-row 20M reprobe
#     experiment (class 5343, n11-centralreply-class5343-b28exhausted-reprobe-
#     20261123): batch-keys-b28.json af19208f..., status-cq.log afc48734...
#     (25 lines: 13 PASS + 8 WIN-HALT + 4 EXHAUSTED, zero duplicates, zero
#     retries), README-cq.md e0153971... and the published Part CQ completion
#     log be208f9c... The CR completion-log sha pin-table machine-parse gate
#     is REPLACED by a phrase battery (the CQ completion log has no sha pin
#     table): the raw aa004/aa035 p1/p2 bytes are still machine-pinned by
#     PIN_RAW_CW and cross-checked against the fetched source bytes here;
# (b) the target battery gates TWO batch-28 CQ WIN rows (aa004/aa035, both
#     result 1, budget 20000000) instead of CR's four batch-30 drive-1 rows;
#     the replica budget gate is 20000000 (the CQ reprobe condition), and the
#     batch-28 s5_index/membership values come from batch-keys-b28.json;
# (c) the unadopted-corroboration sources switch from the Part CH 1-LOSS
#     adoption to the Part CO 7-LOSS adoption publications (merged canonical
#     cache 854800f3... 6,301 rows; increment bd5ef7d7... 7 rows;
#     increments-manifest b47e07ca...). DECLARED batch-28 adaptation of the
#     CR "absent from any id list" gate: aa004/aa035 are batch-28 MEMBERS, so
#     they legitimately appear in the manifest's probed_ids/resolved_ids and
#     -- as Part CQ resolved them only AFTER the Part CO publication while
#     they were still 15M-EXHAUSTED -- in exhausted_excluded_ids (CO-time
#     status, 11 rows). The machine gates below require the targets to be
#     absent from every ADOPTED/WIN id list (loss_ids / win_ids /
#     unadopted_win_ids / unadopted_win_rows / adopted_loss_ids /
#     already_adopted_ids / fragment_ids) and PRESENT in exhausted_excluded_ids
#     (top-level AND the batch-28 block) and in probed_ids/resolved_ids. A NEW
#     cross-artifact consistency gate requires the CQ status PASS key set
#     minus the 2 anchors {aa036, aa046} to equal the manifest
#     exhausted_excluded_ids set exactly (machine-ties the CO-time EXHAUSTED
#     roster to the CQ 20M reprobe roster) and requires the manifest's 6,301-row
#     merged canonical cache to carry NO s5verdict row for either target key
#     (never adopted; their WIN verdicts stay unconsumed pending the scrutiny
#     owner C++ second-implementation gate 9193f5b6 unchanged).
# Verdicts are NOT consumed anywhere; aa004/aa035 stay honest labels. The
# standard 11x11 empty board, the central-reply roots, class 5343 and every
# batch-28 key remain UNKNOWN.
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")
VG = os.path.join(ROOT, "val-gate")

# -- published source pins (Part CQ batch-28 20M-reprobe experiment
#    n11-centralreply-class5343-b28exhausted-reprobe-20261123 + Part CO 7-LOSS
#    adoption re-audit n11-centralreply-class5343-loss7-adoption-reaudit-20261123)
PIN_B28 = "af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5"
PIN_STATUS_CQ = "afc4873482219ec605f62da9a2b543ca8a10f5a2a08d3b3a5ac6de36475704af"
PIN_README_CQ = "e0153971a55060d91ab7a37a568aac9d48c3f5eca1a29b2f13d55dc39f8d51b7"
PIN_LOG_CQ = "be208f9caaff4bae8232e2293417d6859e583c472bdef4f955c6917bab221d64"
PIN_RAW_CW = {
    "aa004.p1": "82ebc402cc83cf463e4921d2ebecd9ed63f6567a505444ee0cad5f5a49e02f48",
    "aa004.p2": "ec10d92b696a6144656db2d5bbcae764b7ebf529c1dd42926e5d258bb3c87701",
    "aa035.p1": "32fc69c35dd00c5d9cec03ca76c516aede7e1922b95f65fd0e6aa3d6fb95420f",
    "aa035.p2": "bb30106af46d532a15641ca27ef2df0a33258146595e3078c21e5ff069711d63",
}
PIN_PUB_INPUT = {
    "aa004": "466f713d84104d70cfd377e1b1f6dab1dd1ef5aea210c7adbcacdfa3a012c22e",
    "aa035": "a54715b68985dcb56c9c0439e9ca0c60d9347a89f6257c6043dec23cabca1018",
}
PIN_PUB_INPUT_BF = {
    "k02a": "b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887",
    "l1a": "e13d2a6c5bbaa34833dcaf8bfaaa91f99393942281f001552cb8af49cca8c98a",
    "ng1": "8e64b9ade1c04122ac4bdc5fa5129b5fca6cfac742ed92cb149f9ffb80ad0b09",
    "ng2": "f19cd5a30b0b868f0a0c7f12a6c47376c8ceb6e862f5c769fb14bdf74e8997dc",
}
PIN_VALGATE = {
    "at2m-s5-1152921504606851072-536870946.published-baseline.out":
        "6e902ab147b117bb09216070f272969418247f5eb73870bf7705c8220fc9c35c",
    "at2m-s5-1152921504606851072-536870946.input.csv":
        "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
    "at2m-s5-1188950301626860544-536870912.published-baseline.out":
        "eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24",
    "at2m-s5-1188950301626860544-536870912.input.csv":
        "56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62",
    "first-15m-s5-1152921504606851072-536870946.published-baseline.out":
        "8035fe54f8c79dd44c4c80d6b38e4ad39d3d4660eaf57a32799969087b8a5591",
    "first-15m-s5-1152921504606851072-536870946.input.csv":
        "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
    "second-15m-s5-1188950301626860544-536870912.published-baseline.out":
        "91dffdec33a409bc3e5f6eb50c0ea95313574ef74d0692c5912a0814946de1fb",
    "second-15m-s5-1188950301626860544-536870912.input.csv":
        "56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62",
}
# Part CO 7-LOSS adoption publications (canonical cache / increment / manifest --
# for the unadopted-row corroboration battery, with the DECLARED batch-28
# exhausted_excluded_ids adaptation described in the header)
PIN_MERGED_CANONICAL = "854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d"
PIN_INCREMENT = "bd5ef7d7632816006bd5a74349bf703a8dd3251e3a550a33e7ae7a0253abe382"
PIN_INCR_MANIFEST = "b47e07ca90b0166d22c681a3136a60500d7a4f8671b1e77b656a1b34c7c02192"
PIN_MERGER = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"

TARGETS = ["aa004", "aa035"]
EXPECT_S5 = {"aa004": 118693, "aa035": 199720}
EXPECT_MEMBERSHIP = {"aa004": 4, "aa035": 4}
EXPECT_RESULT = {"aa004": 1, "aa035": 1}
EXPECT_REPLICA = {"aa004": 15616012, "aa035": 15424243}
WIN_KEYS = list(TARGETS)
CQ_BUDGET = 20000000
# status-cq.log battery: 25 lines = 13 PASS (11 reprobe targets + 2 anchors
# aa036/aa046, zero duplicates) + 8 WIN-HALT + 4 EXHAUSTED; no FAIL / MISMATCH /
# LOSS-HALT / TRUNCATED-RETRY. Distinct PASS keys = 13.
STATUS_EXPECT_LINES = 25
STATUS_EXPECT_PASS = 13
STATUS_EXPECT_WINHALT = 8
STATUS_EXPECT_EXHAUSTED = 4
STATUS_PASS_COUNTS = {k: 1 for k in
                      ("aa036", "aa046", "aa004", "aa005", "aa021", "aa028",
                       "aa030", "aa031", "aa032", "aa035", "aa047", "aa050", "aa053")}
STATUS_WINHALT_COUNTS = {k: 1 for k in ("aa046", "aa004", "aa005", "aa030", "aa031", "aa035", "aa047", "aa053")}
STATUS_EXHAUSTED_COUNTS = {k: 1 for k in ("aa021", "aa028", "aa032", "aa050")}
EXHAUSTED_PASS_ROWS = {k: [str(CQ_BUDGET), "0", str(CQ_BUDGET)] for k in STATUS_EXHAUSTED_COUNTS}
CQ_ANCHOR_IDS = {"aa036", "aa046"}

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
            if line.startswith("# forbidden quadruples: 95670"):
                pass  # rules header presence is gated by the audit, not the maker
    if len(got) != 1 or not done:
        sys.exit(f"ABORT raw parse {path}: {len(got)} replay rows, replay_done={done}")
    return got[0].split(",")

def parse_raw(key, kmap):
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
    if f1[2] != "5" or f1[4] != "0" or f1[5] != str(CQ_BUDGET):
        sys.exit(f"ABORT {key}: unexpected source schema {f1[:6]}")
    if f1[1] != "0":
        sys.exit(f"ABORT {key}: unexpected replay id {f1[1]}")
    lo, hi, legal = int(f1[9]), int(f1[10]), int(f1[3])
    bk = kmap[key]
    if int(bk["lo"]) != lo or int(bk["hi"]) != hi or int(bk["legal"]) != legal:
        sys.exit(f"ABORT {key}: raw key/legal {lo},{hi},{legal} != batch-keys {bk}")
    result, nodes = int(f1[6]), int(f1[7])
    if result != EXPECT_RESULT[key]:
        sys.exit(f"ABORT {key}: expected published result {EXPECT_RESULT[key]}, got result={result}")
    if result != 1:
        sys.exit(f"ABORT {key}: Part CQ reprobe targets are the newly-solved WIN rows, got result={result}")
    if nodes >= CQ_BUDGET:
        sys.exit(f"ABORT {key}: in-budget expected, nodes={nodes}")
    if nodes != EXPECT_REPLICA[key]:
        sys.exit(f"ABORT {key}: replica nodes {nodes} != published {EXPECT_REPLICA[key]}")
    return {"key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "replica_result": result, "replica_nodes": nodes}

def main():
    os.makedirs(OUT, exist_ok=True)
    # -- source pins
    for fname, pin in (("batch-keys-b28.json", PIN_B28), ("status-cq.log", PIN_STATUS_CQ),
                        ("README-cq.md", PIN_README_CQ), ("log-cq-reprobe.md", PIN_LOG_CQ),
                        ("canonical-cache-co-merged-b28loss7.cache", PIN_MERGED_CANONICAL),
                        ("increment-b28loss7.cache", PIN_INCREMENT),
                        ("increments-manifest-co.json", PIN_INCR_MANIFEST)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    for k, pin in PIN_RAW_CW.items():
        got = sha256(os.path.join(SRC, "raw", k + ".out"))
        if got != pin:
            sys.exit(f"ABORT raw {k} sha {got} != pin {pin}")
    for kk, pin in PIN_PUB_INPUT.items():
        got = sha256(os.path.join(SRC, "published-input", kk + ".input.csv"))
        if got != pin:
            sys.exit(f"ABORT published-input {kk} sha {got} != pin {pin}")
    for kk, pin in PIN_PUB_INPUT_BF.items():
        got = sha256(os.path.join(SRC, "published-input-bf", kk + ".input.csv"))
        if got != pin:
            sys.exit(f"ABORT published-input-bf {kk} sha {got} != pin {pin}")
    for fname, pin in PIN_VALGATE.items():
        got = sha256(os.path.join(VG, fname))
        if got != pin:
            sys.exit(f"ABORT val-gate {fname} sha {got} != pin {pin}")
    # -- batch-28 batch-keys battery (published byte-clone af19208f)
    bk28 = json.load(open(os.path.join(SRC, "batch-keys-b28.json")))
    if int(bk28["class_index"]) != 5343:
        sys.exit(f"ABORT class_index {bk28.get('class_index')}")
    if bk28.get("schema") != "n11-centralreply-closure-class5343-batch28-input-v1":
        sys.exit(f"ABORT batch-keys schema {bk28.get('schema')}")
    if bk28.get("class_mask") != ["1171516445255794688", "0"]:
        sys.exit(f"ABORT batch-keys class_mask {bk28.get('class_mask')}")
    if int(bk28.get("published_base_canonical_rows", -1)) != 6293:
        sys.exit(f"ABORT batch-keys published_base_canonical_rows {bk28.get('published_base_canonical_rows')}")
    if int(bk28.get("closure_class_rank_in_published_base", -1)) != 27:
        sys.exit(f"ABORT batch-keys rank {bk28.get('closure_class_rank_in_published_base')}")
    if int(bk28.get("budget", -1)) != 15000000:
        sys.exit(f"ABORT batch-keys budget {bk28.get('budget')}")
    k28 = {k["key_id"]: k for k in bk28["keys"]}
    if len(k28) != 54:
        sys.exit(f"ABORT batch keys count {len(k28)} != 54")
    for t in TARGETS:
        if t not in k28:
            sys.exit(f"ABORT batch-keys lacks target {t}")
        if not re.fullmatch(r"aa[0-9]{3}", t):
            sys.exit(f"ABORT batch-28 key id form {t}")
    # -- status log battery gates (published Part CQ runner log, 25 lines:
    #    13 PASS + 8 WIN-HALT + 4 EXHAUSTED / zero duplicates / zero retries)
    slog = open(os.path.join(SRC, "status-cq.log")).read()
    lines = [l for l in slog.splitlines() if l.strip()]
    if len(lines) != STATUS_EXPECT_LINES:
        sys.exit(f"ABORT status-cq.log line count {len(lines)} != {STATUS_EXPECT_LINES}")
    kinds = {}
    for ln in lines:
        toks = ln.split()
        if len(toks) < 3:
            sys.exit(f"ABORT status-cq.log malformed line {ln!r}")
        kinds[toks[2]] = kinds.get(toks[2], 0) + 1
    if kinds.get("PASS") != STATUS_EXPECT_PASS:
        sys.exit(f"ABORT status-cq.log PASS lines {kinds.get('PASS')} != {STATUS_EXPECT_PASS}")
    if kinds.get("WIN-HALT") != STATUS_EXPECT_WINHALT:
        sys.exit(f"ABORT status-cq.log WIN-HALT lines {kinds.get('WIN-HALT')} != {STATUS_EXPECT_WINHALT}")
    if kinds.get("EXHAUSTED") != STATUS_EXPECT_EXHAUSTED:
        sys.exit(f"ABORT status-cq.log EXHAUSTED lines {kinds.get('EXHAUSTED')} != {STATUS_EXPECT_EXHAUSTED}")
    for bad_kind in ("FAIL", "MISMATCH", "LOSS-HALT"):
        if bad_kind in kinds:
            sys.exit(f"ABORT status-cq.log carries unexpected line kind {bad_kind}")
    retry = sum(v for k, v in kinds.items() if k.endswith("TRUNCATED-RETRY"))
    if retry != 0:
        sys.exit(f"ABORT status-cq.log TRUNCATED-RETRY lines {retry} != 0")
    if sorted(kinds) != ["EXHAUSTED", "PASS", "WIN-HALT"]:
        sys.exit(f"ABORT status-cq.log carries line kinds other than PASS/WIN-HALT/EXHAUSTED: {sorted(kinds)}")
    pass_map = {}
    for l in lines:
        toks = l.split()
        if toks[2] == "PASS":
            pass_map.setdefault(toks[1], []).append(toks[3].split(","))
    if sorted(pass_map) != sorted(STATUS_PASS_COUNTS):
        sys.exit(f"ABORT status-cq.log PASS key set {sorted(pass_map)}")
    for kk, cnt in STATUS_PASS_COUNTS.items():
        pl = pass_map.get(kk)
        if not pl or len(pl) != cnt:
            sys.exit(f"ABORT status-cq.log {kk} PASS line count {len(pl or [])} != {cnt}")
    for kk in TARGETS:
        for row in pass_map[kk]:
            if row != [str(CQ_BUDGET), str(EXPECT_RESULT[kk]), str(EXPECT_REPLICA[kk])]:
                sys.exit(f"ABORT status-cq.log {kk} PASS row is not the published CQ reprobe row: {row}")
    for kk in STATUS_EXHAUSTED_COUNTS:
        for row in pass_map[kk]:
            if row != EXHAUSTED_PASS_ROWS[kk]:
                sys.exit(f"ABORT status-cq.log {kk} PASS row is not the published 20M-exhaustion row: {row}")
    winhalt_map = {}
    for l in lines:
        toks = l.split()
        if toks[2] == "WIN-HALT":
            winhalt_map.setdefault(toks[1], []).append(l)
    if sorted(winhalt_map) != sorted(STATUS_WINHALT_COUNTS):
        sys.exit(f"ABORT status-cq.log WIN-HALT keys {sorted(winhalt_map)} != {sorted(STATUS_WINHALT_COUNTS)}")
    for kk, cnt in STATUS_WINHALT_COUNTS.items():
        if len(winhalt_map[kk]) != cnt:
            sys.exit(f"ABORT status-cq.log {kk} WIN-HALT record count {len(winhalt_map[kk])}")
    exhausted_map = {}
    for l in lines:
        toks = l.split()
        if toks[2] == "EXHAUSTED":
            exhausted_map.setdefault(toks[1], []).append(l)
    if sorted(exhausted_map) != sorted(STATUS_EXHAUSTED_COUNTS):
        sys.exit(f"ABORT status-cq.log EXHAUSTED keys {sorted(exhausted_map)}")
    if len(pass_map) != STATUS_EXPECT_PASS:
        sys.exit(f"ABORT status-cq.log distinct PASS keys {len(pass_map)} != {STATUS_EXPECT_PASS} (zero duplicates)")
    if len(lines) != STATUS_EXPECT_PASS + STATUS_EXPECT_WINHALT + STATUS_EXPECT_EXHAUSTED:
        sys.exit("ABORT status-cq.log line-kind totals inconsistent")
    # -- published completion-log phrase battery (declared replacement of the
    #    CR pin-table gate: the CQ completion log carries no sha pin table;
    #    raw bytes are independently machine-pinned by PIN_RAW_CW above)
    log_cq = open(os.path.join(SRC, "log-cq-reprobe.md")).read()
    for phrase in ("batch-28 (closure class 5343) の published EXHAUSTED 11行",
                   "7行が解決 (全てWIN・nodes 15.4M〜17.2M)",
                   "aa004 15,616,012",
                   "aa035 15,424,243",
                   "aa021 / aa028 / aa032 / aa050 (全nodes=20,000,000 2-pass一致)",
                   "verdict不消費",
                   "reprobe_condition.budget",
                   "**標準11×11空盤・class 5343・全キーはこの時点で UNKNOWN**"):
        if phrase not in log_cq:
            sys.exit(f"ABORT log-cq-reprobe.md lacks phrase: {phrase!r}")
    # -- README-cq phrase battery (whitespace-normalized)
    rd = re.sub(r"\s+", " ", open(os.path.join(SRC, "README-cq.md")).read())
    for phrase in ("batch-28 (closure class 5343) の published EXHAUSTED 11行",
                   "新条件 budget 20,000,000",
                   "aa004 15,616,012 / aa005 15,957,877",
                   "aa035 15,424,243",
                   "EXHAUSTED at 20M (4行・honest UNKNOWN・same-condition再probeなし)",
                   "batch-28のEXHAUSTED残は 11行 → 4行",
                   "scrutiny owner",
                   "class 5343",
                   "verdict不消費",
                   "20M派生runnerのend-to-end妥当性gateとして事前登録",
                   "7 WIN行は **probe-level honest labels のみ**"):
        if phrase not in rd:
            sys.exit(f"ABORT README-cq lacks phrase: {phrase!r}")
    # no-claims guard: whitespace-stripped match
    rd_nospace = re.sub(r"\s+", "", open(os.path.join(SRC, "README-cq.md")).read())
    if "閉鎖・被覆・secured・root勝敗の主張はしない" not in rd_nospace:
        sys.exit("ABORT README-cq lacks the no-claims guard")
    # -- per-target raw cross-verification
    rows = []
    for key in TARGETS:
        bk = k28.get(key)
        if bk is None or int(bk["s5_index"]) != EXPECT_S5[key]:
            sys.exit(f"ABORT {key}: batch-28 s5_index {bk and bk.get('s5_index')}")
        if int(bk["membership_class_count"]) != EXPECT_MEMBERSHIP[key]:
            sys.exit(f"ABORT {key}: membership_class_count {bk.get('membership_class_count')}")
        r = parse_raw(key, k28)
        r["source"] = "part-cq-b28exhausted-reprobe20m"
        r["s5_index"] = int(bk["s5_index"])
        r["membership_class_count"] = int(bk["membership_class_count"])
        r["expect_third"] = EXPECT_RESULT[key]
        rows.append(r)
    # -- unadopted-row corroboration battery (Part CO publications, with the
    #    DECLARED batch-28 exhausted_excluded_ids adaptation)
    merged = open(os.path.join(SRC, "canonical-cache-co-merged-b28loss7.cache")).read().splitlines()
    s5rows = [l for l in merged if l.startswith("s5verdict,")]
    if len(s5rows) != 6301:
        sys.exit(f"ABORT merged canonical cache s5verdict rows {len(s5rows)} != 6301")
    for r in rows:
        row_would_be = f"s5verdict,{r['lo']},{r['hi']},5,{r['replica_result']},{r['replica_nodes']}"
        hits = [l for l in s5rows if l == row_would_be]
        if hits:
            sys.exit(f"ABORT {r['key_id']}: row unexpectedly present in the adopted canonical cache: {hits}")
        other_key = [l for l in s5rows if l.startswith(f"s5verdict,{r['lo']},{r['hi']},")]
        if other_key:
            sys.exit(f"ABORT merged cache carries a conflicting row for the same key: {other_key}")
    inc = open(os.path.join(SRC, "increment-b28loss7.cache")).read().splitlines()
    inc_rows = [l for l in inc if l.startswith("s5verdict,")]
    if len(inc_rows) != 7:
        sys.exit(f"ABORT increment rows {len(inc_rows)} != the 7 adopted batch-28 LOSS rows")
    inc_keys = [(l.split(",")[1], l.split(",")[2]) for l in inc_rows]
    if len(set(inc_keys)) != 7:
        sys.exit("ABORT increment rows are not 7 distinct keys")
    for r in rows:
        if any(l.startswith(f"s5verdict,{r['lo']},{r['hi']},") for l in inc_rows):
            sys.exit(f"ABORT {r['key_id']}: unexpectedly present in the Part CO increment")
    if "ADOPTED set = {aa015, aa017, aa018, aa023, aa024, aa029, aa036}" not in "\n".join(inc):
        sys.exit("ABORT increment header lacks the ADOPTED set statement")
    im = json.load(open(os.path.join(SRC, "increments-manifest-co.json")))
    if im.get("schema") != "b28loss7-increments-manifest-v1":
        sys.exit(f"ABORT increments-manifest schema {im.get('schema')}")
    LOSS7 = ["aa015", "aa017", "aa018", "aa023", "aa024", "aa029", "aa036"]
    if im.get("loss_ids") != LOSS7:
        sys.exit(f"ABORT increments-manifest loss_ids {im.get('loss_ids')}")
    b = im["batches"][0]
    if b.get("adopted_loss_ids") != LOSS7 or b.get("batch") != 28 or int(b.get("class_index")) != 5343:
        sys.exit(f"ABORT increments-manifest batch block {b.get('adopted_loss_ids')}")
    if b.get("unadopted_win_ids") != im.get("win_ids") or len(b.get("unadopted_win_ids") or []) != 35:
        sys.exit("ABORT increments-manifest unadopted_win_ids != win_ids (35)")
    if len(b.get("exhausted_excluded_ids") or []) != 11 or len(b.get("probed_ids") or []) != 54:
        sys.exit("ABORT increments-manifest exhausted/probed counts")
    if b.get("already_adopted_ids") != ["aa003"]:
        sys.exit("ABORT increments-manifest already_adopted_ids")
    if im.get("aa003_base_consistency", {}).get("re_emitted") is not False:
        sys.exit("ABORT increments-manifest aa003 re_emitted")
    if im.get("sha256", {}).get("loss") != PIN_INCREMENT:
        sys.exit("ABORT increments-manifest loss sha256 != increment pin")
    if im.get("merger_sha256") != PIN_MERGER:
        sys.exit(f"ABORT increments-manifest merger sha {im.get('merger_sha256')}")
    if im.get("base_cache_sha256") != "3124461b14e4f73a7248cbf5b96c7ff59ebfdcc05258adeb9c81791d86cc461e":
        sys.exit("ABORT increments-manifest base cache sha")
    if int(im.get("base_cache_rows")) != 6294 or int(im.get("base_cache_absent_hits_for_emitted")) != 0:
        sys.exit(f"ABORT increments-manifest base cache {im.get('base_cache_rows')},{im.get('base_cache_absent_hits_for_emitted')}")
    if int(im.get("quarantine_hits", -1)) != 0:
        sys.exit("ABORT increments-manifest quarantine hits")
    if im.get("full_packet_eq_loss_only") is not False:
        sys.exit("ABORT increments-manifest full == loss")
    if im.get("win_scenario_exists") is not True:
        sys.exit("ABORT increments-manifest win_scenario_exists")
    rc = im.get("row_counts", {})
    if int(rc.get("probed_rows")) != 54 or int(rc.get("adopted_loss_rows")) != 7 or int(rc.get("wins")) != 35 \
            or int(rc.get("exhausted_excluded")) != 11 or int(rc.get("fragments_unprobed")) != 0 \
            or int(rc.get("fileless_unprobed")) != 0:
        sys.exit(f"ABORT increments-manifest row_counts {rc}")
    # DECLARED batch-28 adaptation of the CR id-list gates: targets absent from
    # every ADOPTED/WIN id list, present in exhausted_excluded_ids (CO-time
    # status) + probed_ids + resolved_ids (batch-28 member bookkeeping)
    adopted_lists = {}
    for fld in ("loss_ids", "win_ids", "unadopted_win_ids"):
        v = im.get(fld) or []
        if not isinstance(v, list):
            sys.exit(f"ABORT increments-manifest {fld} is not a list")
        adopted_lists[fld] = set(v)
    for bb in im.get("batches", []):
        for fld in ("adopted_loss_ids", "already_adopted_ids", "unadopted_win_ids", "fragment_ids"):
            v = bb.get(fld) or []
            if not isinstance(v, list):
                sys.exit(f"ABORT increments-manifest batch {fld} is not a list")
            adopted_lists["batches." + fld] = set(v)
    uwr_ids = set()
    for uwr in im.get("unadopted_win_rows") or []:
        if isinstance(uwr, dict) and "key_id" in uwr:
            uwr_ids.add(uwr["key_id"])
    expected_exhausted = {"aa004", "aa005", "aa021", "aa028", "aa030", "aa031",
                          "aa032", "aa035", "aa047", "aa050", "aa053"}
    if set(im.get("exhausted_excluded_ids") or []) != expected_exhausted:
        sys.exit(f"ABORT increments-manifest exhausted_excluded_ids {im.get('exhausted_excluded_ids')}")
    if set(b.get("exhausted_excluded_ids") or []) != expected_exhausted:
        sys.exit("ABORT increments-manifest batch exhausted_excluded_ids")
    for t in TARGETS:
        for fld, s in adopted_lists.items():
            if t in s:
                sys.exit(f"ABORT {t}: target id appears in adopted/win list {fld} of the Part CO increments-manifest")
        if t in uwr_ids:
            sys.exit(f"ABORT {t}: target id appears in unadopted_win_rows")
        if t not in expected_exhausted:
            sys.exit(f"ABORT {t}: target id missing from exhausted_excluded_ids (CO-time EXHAUSTED roster)")
        if t not in set(b.get("probed_ids") or []):
            sys.exit(f"ABORT {t}: target id missing from batch-28 probed_ids")
        if t not in set(im.get("resolved_ids") or []):
            sys.exit(f"ABORT {t}: target id missing from resolved_ids (batch-28 member bookkeeping)")
    # NEW cross-artifact consistency gate (declared): the CQ 20M reprobe
    # roster (status PASS keys minus the 2 anchors) == the CO manifest
    # exhausted_excluded_ids roster exactly
    if set(pass_map) - CQ_ANCHOR_IDS != expected_exhausted:
        sys.exit(f"ABORT cross-artifact: CQ PASS keys minus anchors {sorted(set(pass_map) - CQ_ANCHOR_IDS)} != exhausted_excluded_ids")
    # -- anchors/negatives (published constants, AR->BF->BK->BM->BS->BV->BW->BX->BY->CC->CL->CM->CR provenance chain)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b28cqwin2-thirdimpl-input-v1",
                 "sources": {
                     "b28cqwin": ("sources/raw aa004/aa035 p1+p2 + sources/status-cq.log + sources/log-cq-reprobe.md "
                                  "+ batch-keys-b28.json + published Part CQ batch-28 EXHAUSTED 11-row 20M-reprobe "
                                  "canonical outputs (experiment n11-centralreply-class5343-b28exhausted-reprobe-"
                                  "20261123, completion log research/log/2026-11-23-part-cq-b28exhausted-reprobe.md), "
                                  "commit-pinned raw fetch; batch-keys sha256 af19208f..; the two targets are the "
                                  "CQ 20M newly-solved WIN rows (budget 20000000)"),
                     "b28_batch_keys_sha256": PIN_B28,
                     "b28cq_status_sha256": PIN_STATUS_CQ,
                     "b28cq_completion_log_sha256": PIN_LOG_CQ,
                     "unadopted": ("published Part CO 7-LOSS adoption re-audit (experiment "
                                  "n11-centralreply-class5343-loss7-adoption-reaudit-20261123): merged canonical "
                                  "cache sha256 854800f3.. (6,301 rows = Part CH 6,294 + 7 batch-28 LOSS rows) is "
                                  "UNCHANGED and carries NO row for aa004/aa035 (machine-gated both by this maker "
                                  "and by audit_cw.py G6); increment bd5ef7d7.., increments-manifest b47e07ca.., "
                                  "pinned fail-closed merger 90711961..; DECLARED batch-28 adaptation: the two "
                                  "cross-verified CQ-WIN rows appear ONLY in the manifest's exhausted_excluded_ids "
                                  "(CO-time 15M EXHAUSTED roster) and member bookkeeping (probed_ids/resolved_ids), "
                                  "NOT in any adopted/win id list; they are UNADOPTED honest labels pending the "
                                  "scrutiny owner C++ second-implementation gate 9193f5b6 unchanged"),
                     "anchors": ("published Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK/BM/BS/BV/BW/BX/BY/CC/CL/CM/CR "
                                 "anchor/negative values, input CSVs byte-equality-checked against the published "
                                 "Part BF experiment (provenance chain AR -> BF -> BK -> BM -> BS -> BV -> BW -> "
                                 "BX -> BY -> CC -> CL -> CM -> CR -> CW)")},
                 "consumed_into_canonical_cache": False,
                 "unadopted_win_rows": True,
                 "unadopted_loss_rows": False,
                 "canonical_cache_sha256_unchanged": PIN_MERGED_CANONICAL,
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
        with open(os.path.join(OUT, f"{r['key_id']}.input.csv"), "w") as fh:
            fh.write(csv)
    for r in anchor_rows:
        csv = f"target,0,5,{r['lo']},{r['hi']},{r['legal']},0,0,0,0,0\n"
        pub = open(os.path.join(SRC, "published-input-bf", f"{r['key_id']}.input.csv")).read()
        if csv != pub:
            sys.exit(f"ABORT anchor {r['key_id']}: derived CSV {csv!r} != published Part BF {pub!r}")
        with open(os.path.join(OUT, f"{r['key_id']}.input.csv"), "w") as fh:
            fh.write(csv)
    for r in NEGATIVES:
        csv = f"target,0,{r['stones']},{r['lo']},{r['hi']},{r['legal']},0,0,0,0,0\n"
        pub = open(os.path.join(SRC, "published-input-bf", f"{r['key_id']}.input.csv")).read()
        if csv != pub:
            sys.exit(f"ABORT negative {r['key_id']}: derived CSV {csv!r} != published Part BF {pub!r}")
        with open(os.path.join(OUT, f"{r['key_id']}.input.csv"), "w") as fh:
            fh.write(csv)
    print("CW-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"])
    print("unadopted rows: absent from merged canonical cache + increment + every adopted/win id list (machine-gated)")
    print("cross-artifact: CQ PASS roster minus anchors == manifest exhausted_excluded_ids (machine-gated)")

if __name__ == "__main__":
    main()
