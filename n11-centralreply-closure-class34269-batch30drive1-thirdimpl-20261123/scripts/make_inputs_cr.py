# make_inputs_cr.py -- machine-derive the Part CR third-impl input CSVs and
# rows.json for the four published batch-30 (class 34269) drive-1 rows ac001
# (LOSS) / ac002 (WIN) / ac003 (WIN) / ac004 (LOSS) -- all four UNCONSUMED
# honest labels (drive-1 WIN-HALT wave, 2 WIN + 2 LOSS), from the published
# canonical artifacts (zero hand transcription). Fail-closed: any unexpected
# field aborts.
#
# Adapted from the published Part CM maker (make_inputs_cm.py, sha256
# f926b5be..., experiment n11-centralreply-closure-b28drive3win-thirdimpl-
# 20261123, itself from the published Part CL maker make_inputs_ck.py
# 177c4409 / CC 8255d0ad... / BY 359abebc / BX e1def905 / BW f94d6e4f).
# Deltas (all declared in the Part CR declaration before execution):
# (a) sources switch from the Part CJ drive-3 experiment to the published
#     Part CP batch-30 drive-1 experiment (class 34269): status-cp.log 9-line
#     battery WITH the disclosed v1-harness duplicate lines (2x ac001 PASS,
#     2x ac002 PASS + 2x ac002 WIN-HALT = 3 duplicate lines, exactly the
#     published record), README-cp batch-30 phrases, and the published Part CP
#     drive-1 completion log (log-cp-drive1.md) whose 9-row output sha pin
#     table is machine-parsed and cross-verified against the fetched source
#     bytes (NEW gate: replaces the Part CJ row-audit battery; batch-30 has no
#     row-audit yet -- the batch is still in progress on ac005..ac054 by the
#     Part CP owner, which stays non-contact);
# (b) the target battery gates FOUR drive-1 rows of BOTH verdict kinds
#     (ac002/ac003 result 1 WIN-HALT rows, ac001/ac004 result 2 LOSS rows --
#     honest labels, adoption candidates only, verdicts never consumed)
#     instead of the two WIN rows of CM;
# (c) the unadopted-corroboration sources switch from the Part CH 1-LOSS
#     adoption to the Part CO 7-LOSS adoption publications (merged canonical
#     cache 854800f3.. 6,301 rows = Part CH 6,294 + 7 batch-28 LOSS rows;
#     increment bd5ef7d7.. 7 rows; increments-manifest b47e07ca..): the four
#     cross-verified rows must NOT appear anywhere in the adopted canonical
#     cache / increment / increments-manifest id lists. Verdicts are NOT
#     consumed anywhere; ac001..ac004 are honest labels pending the scrutiny
#     owner C++ second-implementation gate 9193f5b6 unchanged. The standard
#     11x11 empty board, the 19 central-reply roots, class 34269 and every
#     batch-30 key (ac001..ac054) remain UNKNOWN.
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")
VG = os.path.join(ROOT, "val-gate")

# -- published source pins (Part CP batch-30 drive-1 experiment
#    n11-centralreply-closure-class34269-batch30-20261123 + Part CO 7-LOSS
#    adoption re-audit n11-centralreply-class5343-loss7-adoption-reaudit-20261123)
PIN_B30 = "79fbd1664f4ad66ea62d9c8a8aa5aaff5d16bcdaa397895119ce4d8f47961232"
PIN_STATUS_CP = "43fcad174e7d3ec4bbc8a9724e764fd93b5d6cfce80e64921d77a76ae8b2360c"
PIN_README_CP = "94bf05175696140faa814b8b54c636e4b757a414877ea5bc3760ef882582ba8e"
PIN_LOG_CP = "9903944e73abc88b7291c665449499ea3c5fb269a01d32059ca47f1ab731d728"
PIN_RAW_CR = {
    "ac001.p1": "1bef2dc2477f36fa21eee3f48438f2792b3f386915753f32f6c4f89573a12df7",
    "ac001.p2": "bde8b2360a65a1424678e42876fb13ef8bc5964087156e96582e2c1c1fe0083e",
    "ac002.p1": "e58cc0618d2c1c38e33e464fd98d89b956c7f7ff0674ebbfd6f352401add2311",
    "ac002.p2": "ad06a109627d5a998f02cb3723f2b20aa844d6216ebfe84277568f2b3e0748aa",
    "ac003.p1": "c585df3bf5c570de19453a861c5b011469f6613b746c3732fcdf177c9358e135",
    "ac003.p2": "0f886d38a51c402949ff363ea673464103bc8268abc168d4f06be0dc50703028",
    "ac004.p1": "4572f41d891fa8e60d88233ded91b46837842d9a6ed85b7d8aa2ae9fc6038d36",
    "ac004.p2": "ed39eb755506661d4091ac37c68bc76b8559516ad4590bde86e075daa9cd1c5d",
}
PIN_PUB_INPUT = {
    "ac001": "a7502c054e43a78cf36bfca90f72af58b32a210207c8a13e34c06e26e89d165a",
    "ac002": "d02d876d47603e941e3378d3c010baa13dfa47c150a2c6872326a3ad9233d6d4",
    "ac003": "9d1bb2b539ea742a15815cee24235faa66d140c498171978616d35b01e222c8f",
    "ac004": "b49fa2904d34d36c5f3c0db56d4d2cd21550b17e95021b28210aa119508300da",
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
# for the unadopted-row corroboration battery: ac001..ac004 must NOT appear)
PIN_MERGED_CANONICAL = "854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d"
PIN_INCREMENT = "bd5ef7d7632816006bd5a74349bf703a8dd3251e3a550a33e7ae7a0253abe382"
PIN_INCR_MANIFEST = "b47e07ca90b0166d22c681a3136a60500d7a4f8671b1e77b656a1b34c7c02192"
PIN_MERGER = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"

TARGETS = ["ac001", "ac002", "ac003", "ac004"]
EXPECT_S5 = {"ac001": 36668, "ac002": 38891, "ac003": 178184, "ac004": 257581}
EXPECT_MEMBERSHIP = {"ac001": 2, "ac002": 2, "ac003": 2, "ac004": 4}
EXPECT_RESULT = {"ac001": 2, "ac002": 1, "ac003": 1, "ac004": 2}
EXPECT_REPLICA = {"ac001": 5635468, "ac002": 10752246, "ac003": 8036766, "ac004": 5816333}
WIN_KEYS = ["ac002", "ac003"]
LOSS_KEYS = ["ac001", "ac004"]
# status-cp.log battery: 9 lines = 6 PASS (ac001 x2, ac002 x2, ac003, ac004 -- the
# 2x duplicates of ac001/ac002 are the disclosed v1-harness re-invoke artifact,
# value-identical) + 3 WIN-HALT (ac002 x2, ac003) + 0 EXHAUSTED + 0 RETRY;
# 4 distinct PASS keys, 2 distinct WIN-HALT keys.
STATUS_EXPECT_LINES = 9
STATUS_EXPECT_PASS = 6
STATUS_EXPECT_WINHALT = 3
STATUS_PASS_COUNTS = {"ac001": 2, "ac002": 2, "ac003": 1, "ac004": 1}
STATUS_WINHALT_COUNTS = {"ac002": 2, "ac003": 1}
DUPLICATE_LINES = 3

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
    if f1[2] != "5" or f1[4] != "0" or f1[5] != "15000000":
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
    if result == 0:
        sys.exit(f"ABORT {key}: drive-1 wave rows are decided rows, got result=0")
    if nodes >= 15000000:
        sys.exit(f"ABORT {key}: in-budget expected, nodes={nodes}")
    if nodes != EXPECT_REPLICA[key]:
        sys.exit(f"ABORT {key}: replica nodes {nodes} != published {EXPECT_REPLICA[key]}")
    return {"key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "replica_result": result, "replica_nodes": nodes}

def main():
    os.makedirs(OUT, exist_ok=True)
    # -- source pins
    for fname, pin in (("batch-keys-b30.json", PIN_B30), ("status-cp.log", PIN_STATUS_CP),
                        ("README-cp.md", PIN_README_CP), ("log-cp-drive1.md", PIN_LOG_CP),
                        ("canonical-cache-co-merged-b28loss7.cache", PIN_MERGED_CANONICAL),
                        ("increment-b28loss7.cache", PIN_INCREMENT),
                        ("increments-manifest-co.json", PIN_INCR_MANIFEST)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    for k, pin in PIN_RAW_CR.items():
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
    bk30 = json.load(open(os.path.join(SRC, "batch-keys-b30.json")))
    if int(bk30["class_index"]) != 34269:
        sys.exit(f"ABORT class_index {bk30.get('class_index')}")
    if bk30.get("schema") != "n11-centralreply-closure-class34269-batch30-input-v1":
        sys.exit(f"ABORT batch-keys schema {bk30.get('schema')}")
    if bk30.get("class_mask") != ["1152921504624672768", "68719476736"]:
        sys.exit(f"ABORT batch-keys class_mask {bk30.get('class_mask')}")
    if int(bk30.get("published_base_canonical_rows", -1)) != 6301:
        sys.exit(f"ABORT batch-keys published_base_canonical_rows {bk30.get('published_base_canonical_rows')}")
    if int(bk30.get("closure_class_rank_in_published_base", -1)) != 36:
        sys.exit(f"ABORT batch-keys rank {bk30.get('closure_class_rank_in_published_base')}")
    if int(bk30.get("budget", -1)) != 15000000:
        sys.exit(f"ABORT batch-keys budget {bk30.get('budget')}")
    k30 = {k["key_id"]: k for k in bk30["keys"]}
    if len(k30) != 54:
        sys.exit(f"ABORT batch keys count {len(k30)} != 54")
    if [k["key_id"] for k in bk30["keys"][:4]] != TARGETS:
        sys.exit(f"ABORT batch-keys first four ids {bk30['keys'][:4]} != drive-1 wave {TARGETS}")
    for t in TARGETS:
        if not re.fullmatch(r"ac[0-9]{3}", t):
            sys.exit(f"ABORT batch-30 key id form {t}")
    # -- status log battery gates (published Part CP drive-1 runner log, 9
    #    lines: 6 PASS (incl. the 3 disclosed value-identical duplicate lines)
    #    + 3 WIN-HALT; no FAIL/MISMATCH/EXHAUSTED/retry rows).
    slog = open(os.path.join(SRC, "status-cp.log")).read()
    lines = [l for l in slog.splitlines() if l.strip()]
    if len(lines) != STATUS_EXPECT_LINES:
        sys.exit(f"ABORT status-cp.log line count {len(lines)} != {STATUS_EXPECT_LINES}")
    kinds = {}
    for ln in lines:
        toks = ln.split()
        if len(toks) < 3:
            sys.exit(f"ABORT status-cp.log malformed line {ln!r}")
        kinds[toks[2]] = kinds.get(toks[2], 0) + 1
    if kinds.get("PASS") != STATUS_EXPECT_PASS:
        sys.exit(f"ABORT status-cp.log PASS lines {kinds.get('PASS')} != {STATUS_EXPECT_PASS}")
    if kinds.get("WIN-HALT") != STATUS_EXPECT_WINHALT:
        sys.exit(f"ABORT status-cp.log WIN-HALT lines {kinds.get('WIN-HALT')} != {STATUS_EXPECT_WINHALT}")
    for bad_kind in ("FAIL", "MISMATCH", "LOSS-HALT", "EXHAUSTED"):
        if bad_kind in [k for k in kinds if k.endswith("TRUNCATED-RETRY")] or bad_kind in kinds:
            if bad_kind in kinds:
                sys.exit(f"ABORT status-cp.log carries unexpected line kind {bad_kind}")
    retry = sum(v for k, v in kinds.items() if k.endswith("TRUNCATED-RETRY"))
    if retry != 0:
        sys.exit(f"ABORT status-cp.log TRUNCATED-RETRY lines {retry} != 0")
    pass_map = {}
    for l in lines:
        toks = l.split()
        if toks[2] == "PASS":
            pass_map.setdefault(toks[1], []).append(toks[3].split(","))
    if sorted(pass_map) != sorted(TARGETS):
        sys.exit(f"ABORT status-cp.log PASS key set {sorted(pass_map)}")
    for kk in TARGETS:
        pl = pass_map.get(kk)
        if not pl or len(pl) != STATUS_PASS_COUNTS[kk]:
            sys.exit(f"ABORT status-cp.log {kk} PASS line count {len(pl or [])} != {STATUS_PASS_COUNTS[kk]}")
        for row in pl:
            if row != ["15000000", str(EXPECT_RESULT[kk]), str(EXPECT_REPLICA[kk])]:
                sys.exit(f"ABORT status-cp.log {kk} PASS row is not the published drive-1 row: {row}")
    winhalt_map = {}
    for l in lines:
        toks = l.split()
        if toks[2] == "WIN-HALT":
            winhalt_map.setdefault(toks[1], []).append(l)
    if sorted(winhalt_map) != sorted(WIN_KEYS):
        sys.exit(f"ABORT status-cp.log WIN-HALT keys {sorted(winhalt_map)} != {sorted(WIN_KEYS)}")
    for kk in WIN_KEYS:
        if len(winhalt_map[kk]) != STATUS_WINHALT_COUNTS[kk]:
            sys.exit(f"ABORT status-cp.log {kk} WIN-HALT record count {len(winhalt_map[kk])}")
    dup = len(lines) - 6  # 4 keys have exactly 1 first-class verdict record each
    if dup != DUPLICATE_LINES:
        sys.exit(f"ABORT status-cp.log duplicate line count {dup} != {DUPLICATE_LINES}")
    if kinds.get("PASS", 0) + kinds.get("WIN-HALT", 0) != len(lines):
        sys.exit("ABORT status-cp.log carries line kinds other than PASS/WIN-HALT")
    # -- published completion-log pin-table battery (NEW, declared): machine-parse
    #    the 9-row output sha pin table of the Part CP drive-1 completion log and
    #    cross-verify it against the fetched source bytes (batch-30 has no
    #    row-audit yet; the completion log is the published drive-1 closure).
    log_cp = open(os.path.join(SRC, "log-cp-drive1.md")).read()
    table = re.findall(r"\|\s*(output/[a-z0-9./]+)\s*\|\s*`([0-9a-f]{64})`\s*\|", log_cp)
    if len(table) != 9:
        sys.exit(f"ABORT log-cp-drive1 pin table rows {len(table)} != 9")
    for repo_rel, h in table:
        if repo_rel.startswith("output/raw/"):
            local = repo_rel.replace("output/raw/", "raw/")
        elif repo_rel == "output/status.log":
            local = "status-cp.log"
        else:
            sys.exit(f"ABORT log pin-table unexpected row {repo_rel}")
        got = sha256(os.path.join(SRC, local))
        if got != h:
            sys.exit(f"ABORT log pin-table mismatch for {repo_rel}: {got} != {h}")
        if repo_rel == "output/status.log" and h != PIN_STATUS_CP:
            sys.exit("ABORT log pin-table status pin != maker status pin")
    for phrase in ("probed 4 = WIN 2・LOSS 2・EXHAUSTED 0・fileless 50・MISMATCH 0",
                   "verdict不消費", "UNKNOWN担保",
                   "ac002 PASS result", "ac003 PASS result",
                   "status.logは9行 (重複3行を含むまま出版"):
        if phrase not in log_cp:
            sys.exit(f"ABORT log-cp-drive1 lacks phrase: {phrase!r}")
    # -- README-cp batch-30 phrase battery (whitespace-normalized)
    rd = re.sub(r"\s+", " ", open(os.path.join(SRC, "README-cp.md")).read())
    for phrase in ("ac001 PASS result **2 (LOSS)** nodes 5,635,468",
                   "ac002 PASS result **1 (WIN)** nodes 10,752,246",
                   "ac003 PASS result **1 (WIN)** nodes 8,036,766",
                   "ac004 PASS result **2 (LOSS)** nodes 5,816,333",
                   "残50キー ac005..ac054 は fileless UNPROBED",
                   "scrutiny owner",
                   "class 34269",
                   "Part CP",
                   "verdict不消費",
                   "scaffold出版順は規約対象外"):
        if phrase not in rd:
            sys.exit(f"ABORT README-cp lacks phrase: {phrase!r}")
    # no-claims guard: whitespace-stripped match (the batch-30 README wraps the
    # phrase across a line break; whitespace is not part of the guard text)
    rd_nospace = re.sub(r"\s+", "", open(os.path.join(SRC, "README-cp.md")).read())
    if "閉鎖・被覆・secured・root勝敗の主張はしない" not in rd_nospace:
        sys.exit("ABORT README-cp lacks the no-claims guard")
    # -- per-target raw cross-verification
    rows = []
    for key in TARGETS:
        bk = k30.get(key)
        if bk is None or int(bk["s5_index"]) != EXPECT_S5[key]:
            sys.exit(f"ABORT {key}: batch-30 s5_index {bk and bk.get('s5_index')}")
        if int(bk["membership_class_count"]) != EXPECT_MEMBERSHIP[key]:
            sys.exit(f"ABORT {key}: membership_class_count {bk.get('membership_class_count')}")
        r = parse_raw(key, k30)
        r["source"] = "part-cp-batch30-drive1"
        r["s5_index"] = int(bk["s5_index"])
        r["membership_class_count"] = int(bk["membership_class_count"])
        r["expect_third"] = EXPECT_RESULT[key]
        rows.append(r)
    # -- NEW unadopted-row corroboration battery (Part CO publications): the
    #    four rows this experiment cross-verifies must NOT appear anywhere in
    #    the adopted canonical cache / increment / increments-manifest.
    #    Verdicts never consumed; canonical cache 854800f3 unchanged (6,301 rows).
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
    # machine scan over every id LIST in the manifest (NOT raw text scan)
    man_ids = set()
    for fld in ("loss_ids", "win_ids", "unadopted_win_ids", "exhausted_excluded_ids", "resolved_ids"):
        v = im.get(fld) or []
        if not isinstance(v, list):
            sys.exit(f"ABORT increments-manifest {fld} is not a list")
        man_ids |= set(v)
    for bb in im.get("batches", []):
        for fld in ("adopted_loss_ids", "already_adopted_ids", "unadopted_win_ids",
                   "exhausted_excluded_ids", "fragment_ids", "probed_ids"):
            v = bb.get(fld) or []
            if not isinstance(v, list):
                sys.exit(f"ABORT increments-manifest batch {fld} is not a list")
            man_ids |= set(v)
    for uwr in im.get("unadopted_win_rows") or []:
        if isinstance(uwr, dict) and "key_id" in uwr:
            man_ids.add(uwr["key_id"])
    for t in TARGETS:
        if t in man_ids:
            sys.exit(f"ABORT {t}: target id must not appear in any id list of the Part CO increments-manifest")
    if {"ac005", "ac010"} & man_ids:
        sys.exit("ABORT batch-30 ids must not appear in the batch-28 manifest id lists")
    # -- anchors/negatives (published constants, AR->BF->BK->BM->BS->BV->BW->BX->BY->CC->CL->CM provenance chain)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-class34269-batch30drive1-thirdimpl-input-v1",
                 "sources": {
                     "b30drive1": ("sources/raw ac001..ac004 p1+p2 + sources/status-cp.log + sources/log-cp-drive1.md "
                                  "+ batch-keys-b30.json + published batch-30 drive-1 (Part CP) canonical outputs "
                                  "(experiment n11-centralreply-closure-class34269-batch30-20261123, scaffold "
                                  "MANIFEST at commit 281d58e6, completion log research/log/2026-11-23-part-cp-"
                                  "batch30-drive1.md), commit-pinned raw fetch; batch-keys sha256 79fbd166.."),
                     "b30_batch_keys_sha256": PIN_B30,
                     "b30drive1_status_sha256": PIN_STATUS_CP,
                     "b30drive1_completion_log_sha256": PIN_LOG_CP,
                     "unadopted": ("published Part CO 7-LOSS adoption re-audit (experiment "
                                  "n11-centralreply-class5343-loss7-adoption-reaudit-20261123): merged canonical "
                                  "cache sha256 854800f3.. (6,301 rows = Part CH 6,294 + 7 batch-28 LOSS rows) is "
                                  "UNCHANGED and carries NO row for ac001..ac004 (machine-gated both by this maker "
                                  "and by audit_cr.py G6); increment bd5ef7d7.., increments-manifest b47e07ca.., "
                                  "pinned fail-closed merger 90711961..; the four cross-verified drive-1 rows "
                                  "(2 WIN + 2 LOSS) are UNADOPTED honest labels pending the scrutiny owner C++ "
                                  "second-implementation gate 9193f5b6 unchanged"),
                     "anchors": ("published Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK/BM/BS/BV/BW/BX/BY/CC/CL/CM "
                                 "anchor/negative values, input CSVs byte-equality-checked against the published "
                                 "Part BF experiment (provenance chain AR -> BF -> BK -> BM -> BS -> BV -> BW -> "
                                 "BX -> BY -> CC -> CL -> CM -> CR)")},
                 "consumed_into_canonical_cache": False,
                 "unadopted_win_rows": True,
                 "unadopted_loss_rows": True,
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
    print("CR-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"])
    print("unadopted rows: absent from merged canonical cache + increment + manifest (machine-gated)")

if __name__ == "__main__":
    main()
