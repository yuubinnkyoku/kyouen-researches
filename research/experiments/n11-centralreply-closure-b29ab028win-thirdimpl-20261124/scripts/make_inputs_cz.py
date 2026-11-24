# make_inputs_cz.py -- machine-derive the Part CZ third-impl input CSVs and
# rows.json for the ONE published batch-29 (closure class 2251) drive-2 WIN
# row ab028 (key 1297036830121656320, 131074, legal 80, nodes 3,167,121) --
# an UNCONSUMED honest probe-level label -- from the published canonical
# artifacts (zero hand transcription). Fail-closed: any unexpected field
# aborts.
#
# Adapted from the published Part CW maker (make_inputs_cw.py, sha256
# 8a9fe75e4d22f8a6b51aeeacc7c571f0dc62fe5a83b1b2612f95958199fbba74,
# experiment n11-centralreply-closure-b28cqwin2-thirdimpl-20261124, itself
# from the published Part CR maker 364a217f.. / CM f926b5be.. / CL 177c4409 /
# CC 8255d0ad / BY 359aebef / BX e1def905 / BW f94d6e4f). Declared deltas
# (all in the Part CZ declaration before execution):
# (a) sources switch from the Part CQ batch-28 20M-reprobe experiment to the
#     published batch-29 kit + Part CI takeover drive-2 publications
#     (experiment n11-centralreply-closure-class2251-batch29-20261123:
#     batch-keys json 330c0b9f.., full 55-line status.log b49322d9.. with the
#     drive-1 prefix byte-pinned to the Part CU manifest status_log_sha256
#     6b877344.., README 56fa34e3.., drive-2 declaration/completion logs
#     8819c366../46c461bd.., raw ab028 p1/p2 pins, published input csv pin);
# (b) the target battery gates the ONE batch-29 drive-2 WIN row (ab028,
#     result 1, budget 15000000) instead of CW's two batch-28 CQ WIN rows;
#     the replica budget gate is 15000000 (the declared batch-29 probe
#     condition), and the batch-29 s5/membership values come from
#     batch-keys json; NEW drive-2 status battery: 55 lines = 54 PASS + 1
#     WIN-HALT, ab028 PASS row == the published WIN row (15000000,1,3167121),
#     each drive-1 PASS row (ab001..ab016) node-matches the Part CU adopted
#     increment row for the same key, every other PASS row result 2, and the
#     drive-2 PASS roster == batch-keys-minus-probed == the CU manifest
#     fileless_unprobed_ids roster exactly;
# (c) the unadopted-corroboration sources switch from the Part CO 7-LOSS
#     adoption to the Part CU 16-LOSS adoption publications (merged canonical
#     cache 30ddad9d.. 6,317 rows = CO base 854800f3 6,301 + the 16 adopted
#     drive-1 LOSS rows; increment bab011e3..; increments-manifest f9f58ee1..).
#     DECLARED batch-29 adaptation of the CW id-list gates: ab028 is a
#     batch-29 member whose CU-time status was fileless UNPROBED (the CU
#     manifest carries it ONLY in batches[0].fileless_unprobed_ids, the
#     38-key roster), so the machine gates below require the target to be
#     absent from every ADOPTED/WIN id list (loss_ids / win_ids /
#     unadopted_win_ids / unadopted_win_rows / batches adopted_loss_ids /
#     already_adopted_ids / unadopted_win_ids / fragment_ids / resolved_ids /
#     probed_ids) AND PRESENT in fileless_unprobed_ids, and require the CU
#     merged canonical cache (6,317 rows) to carry NO s5verdict row for the
#     target key (never adopted; the WIN verdict stays unconsumed pending
#     the scrutiny owner C++ second-implementation gate 9193f5b6 unchanged).
# Verdicts are NOT consumed anywhere; ab028 stays an honest label. The
# standard 11x11 empty board, the central-reply roots, class 2251 and every
# batch-29 key remain UNKNOWN.
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")
VG = os.path.join(ROOT, "val-gate")

# -- published source pins (batch-29 kit + Part CI takeover drive-2
#    publications + Part CU 16-LOSS adoption re-audit)
PIN_B29 = "330c0b9f3166e9f6e21b739a851a881d800ab9f58a14dccaa0c772118dee716c"
PIN_STATUS_B29 = "b49322d9ed8cd63e9bba20e10acd52b89849b408d19496931d5545b5ec99a6a0"
PIN_STATUS_DRIVE1_PREFIX = "6b877344b9abea348a9b221f587a771857d3c4091f88fa460ef12595722183e2"
PIN_README_B29 = "56fa34e329051b08ee2ece7ddbbd28e7d37882b71a21b665c5a212cd21a6172c"
PIN_LOG_DECL = "8819c3666bd765e4f6fd5507a763000aa3865a4add6ce69a2c6bca42d65b2acc"
PIN_LOG_COMPL = "46c461bda55240c2ca8e4a582db815adf95b442128097c7f80c51e37263686a0"
PIN_RAW_CZ = {
    "ab028.p1": "af6e6fe493762099a07d0a598471485e3ea1f9cc97f689fb194411192600b5f5",
    "ab028.p2": "77a4736424049fcedb630c53bd84a2e80d16c50aabd9263f444a2673797e5f02",
}
PIN_PUB_INPUT = {
    "ab028": "1d0416af17a79a5008b8cd11102acc4b91e51acd5d2c56ceb1847c5d4baf98cf",
}
PIN_PUB_INPUT_BF = {
    "k02a": "b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887",
    "l1a": "e13d2a6c5bbaa34833dcaf8bfaaa91f99393942281f001552cb8af49cca8c98a",
    "ng1": "8e64b9ade1c04122ac4bdc5fa5129b5fca6cfac742ed92cb149f9ffb80ad0b09",
    "ng2": "f19cd5a30b0b868f0a0c7f12a6c47376c8ceb6e862f5c769fb14bdf74e8997dc",
}
PIN_VALGATE = {
    "at2m-s5-1152921504606851072-536870946.input.csv":
        "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
    "at2m-s5-1152921504606851072-536870946.published-baseline.out":
        "6e902ab147b117bb09216070f272969418247f5eb73870bf7705c8220fc9c35c",
    "at2m-s5-1188950301626860544-536870912.input.csv":
        "56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62",
    "at2m-s5-1188950301626860544-536870912.published-baseline.out":
        "eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24",
    "first-15m-s5-1152921504606851072-536870946.input.csv":
        "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
    "first-15m-s5-1152921504606851072-536870946.published-baseline.out":
        "8035fe54f8c79dd44c4c80d6b38e4ad39d3d4660eaf57a32799969087b8a5591",
    "second-15m-s5-1188950301626860544-536870912.input.csv":
        "56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62",
    "second-15m-s5-1188950301626860544-536870912.published-baseline.out":
        "91dffdec33a409bc3e5f6eb50c0ea95313574ef74d0692c5912a0814946de1fb",
}
# Part CU 16-LOSS adoption publications (canonical cache / increment /
# manifest -- for the unadopted-row corroboration battery)
PIN_MERGED_CANONICAL = "30ddad9dc0add7e21698e864b5c202b8e6ebd3e396c4eb6156a85ff2d34005c4"
PIN_INCREMENT = "bab011e376090f9f4732d63f0084f326ba72dada5cf699d5aabc7e014c29ae24"
PIN_INCR_MANIFEST = "f9f58ee101d53f0598ee01c5c54d5b277797a9e882cfb478ab7f7b3010e191e0"
PIN_MERGER = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"

TARGETS = ["ab028"]
EXPECT_S5 = {"ab028": 93815}
EXPECT_MEMBERSHIP = {"ab028": 3}
EXPECT_RESULT = {"ab028": 1}
EXPECT_REPLICA = {"ab028": 3167121}
B29_BUDGET = 15000000
# status-b29.log battery: 55 lines = 54 PASS (all 54 batch-29 keys, each
# exactly once, drive-1 prefix byte-pinned to the CU manifest) + 1 WIN-HALT
# (ab028); no FAIL / MISMATCH / LOSS-HALT / EXHAUSTED / TRUNCATED-RETRY.
STATUS_EXPECT_LINES = 55
STATUS_EXPECT_PASS = 54
STATUS_EXPECT_WINHALT = 1
ALL_KEYS = [f"ab{i:03d}" for i in range(1, 55)]
DRIVE1_KEYS = [f"ab{i:03d}" for i in range(1, 17)]
DRIVE2_KEYS = [f"ab{i:03d}" for i in range(17, 55)]

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
    if f1[2] != "5" or f1[4] != "0" or f1[5] != str(B29_BUDGET):
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
        sys.exit(f"ABORT {key}: Part CZ target is the drive-2 WIN row ab028, got result={result}")
    if nodes >= B29_BUDGET:
        sys.exit(f"ABORT {key}: in-budget expected, nodes={nodes}")
    if nodes != EXPECT_REPLICA[key]:
        sys.exit(f"ABORT {key}: replica nodes {nodes} != published {EXPECT_REPLICA[key]}")
    return {"key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "replica_result": result, "replica_nodes": nodes}

def main():
    os.makedirs(OUT, exist_ok=True)
    # -- source pins
    for fname, pin in (("batch-keys-b29.json", PIN_B29), ("status-b29.log", PIN_STATUS_B29),
                        ("README-b29.md", PIN_README_B29),
                        ("log-b29drive2-declaration.md", PIN_LOG_DECL),
                        ("log-b29drive2-completion.md", PIN_LOG_COMPL),
                        ("merged-cache-cu-b29loss16.cache", PIN_MERGED_CANONICAL),
                        ("increment-b29loss16.cache", PIN_INCREMENT),
                        ("increments-manifest-cu.json", PIN_INCR_MANIFEST)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    for k, pin in PIN_RAW_CZ.items():
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
    # -- batch-29 batch-keys battery (published byte-clone 330c0b9f)
    bk29 = json.load(open(os.path.join(SRC, "batch-keys-b29.json")))
    if int(bk29["class_index"]) != 2251:
        sys.exit(f"ABORT class_index {bk29.get('class_index')}")
    if bk29.get("schema") != "n11-centralreply-closure-class2251-batch29-input-v1":
        sys.exit(f"ABORT batch-keys schema {bk29.get('schema')}")
    if bk29.get("class_mask") != ["1155314042043105280", "0"]:
        sys.exit(f"ABORT batch-keys class_mask {bk29.get('class_mask')}")
    if int(bk29.get("published_base_canonical_rows", -1)) != 6294:
        sys.exit(f"ABORT batch-keys published_base_canonical_rows {bk29.get('published_base_canonical_rows')}")
    if int(bk29.get("closure_class_rank_in_published_base", -1)) != 35:
        sys.exit(f"ABORT batch-keys rank {bk29.get('closure_class_rank_in_published_base')}")
    if int(bk29.get("budget", -1)) != 15000000:
        sys.exit(f"ABORT batch-keys budget {bk29.get('budget')}")
    k29 = {k["key_id"]: k for k in bk29["keys"]}
    if len(k29) != 54 or sorted(k29) != ALL_KEYS:
        sys.exit(f"ABORT batch keys count {len(k29)} != 54-set")
    for t in TARGETS:
        if t not in k29:
            sys.exit(f"ABORT batch-keys lacks target {t}")
        if not re.fullmatch(r"ab[0-9]{3}", t):
            sys.exit(f"ABORT batch-29 key id form {t}")
    # -- status-b29.log battery gates (published drive-2 final full log,
    #    55 lines: 54 PASS + 1 WIN-HALT / drive-1 prefix byte-pinned to the
    #    Part CU manifest status_log_sha256)
    import hashlib
    raw_log = open(os.path.join(SRC, "status-b29.log"), "rb").read()
    lines = [l for l in raw_log.decode().splitlines() if l.strip()]
    if len(lines) != STATUS_EXPECT_LINES:
        sys.exit(f"ABORT status-b29.log line count {len(lines)} != {STATUS_EXPECT_LINES}")
    prefix = hashlib.sha256("".join(raw_log.decode().splitlines(keepends=True)[:16]).encode()).hexdigest()
    if prefix != PIN_STATUS_DRIVE1_PREFIX:
        sys.exit(f"ABORT status-b29.log drive-1 prefix sha {prefix} != CU manifest pin")
    kinds = {}
    for ln in lines:
        toks = ln.split()
        if len(toks) < 3:
            sys.exit(f"ABORT status-b29.log malformed line {ln!r}")
        kinds[toks[2]] = kinds.get(toks[2], 0) + 1
    if kinds.get("PASS") != STATUS_EXPECT_PASS:
        sys.exit(f"ABORT status-b29.log PASS lines {kinds.get('PASS')} != {STATUS_EXPECT_PASS}")
    if kinds.get("WIN-HALT") != STATUS_EXPECT_WINHALT:
        sys.exit(f"ABORT status-b29.log WIN-HALT lines {kinds.get('WIN-HALT')} != {STATUS_EXPECT_WINHALT}")
    for bad_kind in ("FAIL", "MISMATCH", "LOSS-HALT", "EXHAUSTED"):
        if bad_kind in kinds:
            sys.exit(f"ABORT status-b29.log carries unexpected line kind {bad_kind}")
    retry = sum(v for k, v in kinds.items() if k.endswith("TRUNCATED-RETRY"))
    if retry != 0:
        sys.exit(f"ABORT status-b29.log TRUNCATED-RETRY lines {retry} != 0")
    if sorted(kinds) != ["PASS", "WIN-HALT"]:
        sys.exit(f"ABORT status-b29.log carries line kinds other than PASS/WIN-HALT: {sorted(kinds)}")
    pass_map = {}
    for l in lines:
        toks = l.split()
        if toks[2] == "PASS":
            pass_map.setdefault(toks[1], []).append(toks[3].split(","))
    if sorted(pass_map) != ALL_KEYS:
        sys.exit(f"ABORT status-b29.log PASS key set != all 54 keys")
    for kk, pl in pass_map.items():
        if len(pl) != 1:
            sys.exit(f"ABORT status-b29.log {kk} PASS line count {len(pl)} != 1 (zero duplicates)")
        if pl[0][0] != str(B29_BUDGET):
            sys.exit(f"ABORT status-b29.log {kk} PASS row budget {pl[0][0]} != {B29_BUDGET}")
    winhalt_map = {}
    for l in lines:
        toks = l.split()
        if toks[2] == "WIN-HALT":
            winhalt_map.setdefault(toks[1], []).append(l)
    if sorted(winhalt_map) != TARGETS:
        sys.exit(f"ABORT status-b29.log WIN-HALT keys {sorted(winhalt_map)} != {TARGETS}")
    # target PASS row == the published WIN row
    for kk in TARGETS:
        if pass_map[kk][0] != [str(B29_BUDGET), str(EXPECT_RESULT[kk]), str(EXPECT_REPLICA[kk])]:
            sys.exit(f"ABORT status-b29.log {kk} PASS row is not the published drive-2 WIN row: {pass_map[kk][0]}")
    # drive-1 PASS rows node-match the Part CU adopted increment rows
    inc_rows = [l for l in open(os.path.join(SRC, "increment-b29loss16.cache")).read().splitlines()
                if l.startswith("s5verdict,")]
    if len(inc_rows) != 16:
        sys.exit(f"ABORT increment rows {len(inc_rows)} != the 16 adopted drive-1 LOSS rows")
    inc_by_key = {(int(r.split(",")[1]), int(r.split(",")[2])): r.split(",") for r in inc_rows}
    for kk in DRIVE1_KEYS:
        bk = k29[kk]
        if pass_map[kk][0][1] != "2":
            sys.exit(f"ABORT status-b29.log {kk} drive-1 PASS row is not result 2: {pass_map[kk][0]}")
        row = inc_by_key.get((int(bk["lo"]), int(bk["hi"])))
        if row is None:
            sys.exit(f"ABORT drive-1 key {kk} missing from the Part CU increment")
        if row[4] != "2" or row[5] != pass_map[kk][0][2]:
            sys.exit(f"ABORT status-b29.log {kk} PASS nodes {pass_map[kk][0][2]} != CU adopted increment nodes {row[5]}")
    # every non-target drive-2 PASS row is result 2 (LOSS discipline)
    for kk in DRIVE2_KEYS:
        if kk in TARGETS:
            continue
        if pass_map[kk][0][1] != "2":
            sys.exit(f"ABORT status-b29.log {kk} drive-2 PASS row is not result 2: {pass_map[kk][0]}")
    # -- published drive-2 declaration phrase battery
    log_decl = open(os.path.join(SRC, "log-b29drive2-declaration.md")).read()
    for phrase in ("WIN-CONTINUE",
                   "3時間30分以上の無音",
                   "ab017..ab054 の38キー",
                   "残38キーをab017から昇順に"):
        if phrase not in log_decl:
            sys.exit(f"ABORT log-b29drive2-declaration.md lacks phrase: {phrase!r}")
    # -- published drive-2 completion-log phrase battery
    log_compl = open(os.path.join(SRC, "log-b29drive2-completion.md")).read()
    for phrase in ("batch-29 全54キー (ab001..ab054) probe-complete",
                   "LOSS 53 / WIN 1 / EXHAUSTED 0",
                   "**B final `c608660e`**",
                   "45/45。",
                   "WINは **ab028** のみ",
                   "nodes **3,167,121**",
                   "val-gate fresh 4/4 node-exact",
                   "fetch-back 38/38",
                   "UNKNOWN担保"):
        if phrase not in log_compl:
            sys.exit(f"ABORT log-b29drive2-completion.md lacks phrase: {phrase!r}")
    # -- README-b29 phrase battery (whitespace-normalized)
    rd = re.sub(r"\s+", " ", open(os.path.join(SRC, "README-b29.md")).read())
    for phrase in ("rank 35 class 2251",
                   "budget 15,000,000",
                   "verdict不消費",
                   "s5昇順 3964..93841",
                   "54キー **ab001..ab054**"):
        if phrase not in rd:
            sys.exit(f"ABORT README-b29 lacks phrase: {phrase!r}")
    rd_nospace = re.sub(r"\s+", "", open(os.path.join(SRC, "README-b29.md")).read())
    if "閉鎖・被覆・secured・root勝敗の主張はしない" not in rd_nospace:
        sys.exit("ABORT README-b29 lacks the no-claims guard")
    # -- per-target raw cross-verification
    rows = []
    for key in TARGETS:
        bk = k29.get(key)
        if bk is None or int(bk["s5_index"]) != EXPECT_S5[key]:
            sys.exit(f"ABORT {key}: batch-29 s5_index {bk and bk.get('s5_index')}")
        if int(bk["membership_class_count"]) != EXPECT_MEMBERSHIP[key]:
            sys.exit(f"ABORT {key}: membership_class_count {bk.get('membership_class_count')}")
        r = parse_raw(key, k29)
        r["source"] = "part-ci-takeover-batch29-drive2"
        r["s5_index"] = int(bk["s5_index"])
        r["membership_class_count"] = int(bk["membership_class_count"])
        r["expect_third"] = EXPECT_RESULT[key]
        rows.append(r)
    # -- unadopted-row corroboration battery (Part CU publications, with the
    #    DECLARED batch-29 fileless-UNPROBED adaptation)
    merged = open(os.path.join(SRC, "merged-cache-cu-b29loss16.cache")).read().splitlines()
    s5rows = [l for l in merged if l.startswith("s5verdict,")]
    if len(s5rows) != 6317:
        sys.exit(f"ABORT merged canonical cache s5verdict rows {len(s5rows)} != 6317")
    for r in rows:
        row_would_be = f"s5verdict,{r['lo']},{r['hi']},5,{r['replica_result']},{r['replica_nodes']}"
        hits = [l for l in s5rows if l == row_would_be]
        if hits:
            sys.exit(f"ABORT {r['key_id']}: row unexpectedly present in the adopted canonical cache: {hits}")
        other_key = [l for l in s5rows if l.startswith(f"s5verdict,{r['lo']},{r['hi']},")]
        if other_key:
            sys.exit(f"ABORT merged cache carries a conflicting row for the same key: {other_key}")
    for r in rows:
        if any(l.startswith(f"s5verdict,{r['lo']},{r['hi']},") for l in inc_rows):
            sys.exit(f"ABORT {r['key_id']}: unexpectedly present in the Part CU increment")
    if "ADOPTED set = ab001..ab016" not in open(os.path.join(SRC, "increment-b29loss16.cache")).read():
        sys.exit("ABORT increment header lacks the ADOPTED set statement")
    im = json.load(open(os.path.join(SRC, "increments-manifest-cu.json")))
    if im.get("schema") != "b29loss16-increments-manifest-v1":
        sys.exit(f"ABORT increments-manifest schema {im.get('schema')}")
    LOSS16 = DRIVE1_KEYS
    if im.get("loss_ids") != LOSS16 or im.get("resolved_ids") != LOSS16:
        sys.exit(f"ABORT increments-manifest loss/resolved ids {im.get('loss_ids')}")
    b = im["batches"][0]
    if b.get("batch") != 29 or int(b.get("class_index")) != 2251 or int(b.get("keys_total")) != 54:
        sys.exit(f"ABORT increments-manifest batch block {b.get('batch')},{b.get('class_index')}")
    if b.get("adopted_loss_ids") != LOSS16 or b.get("already_adopted_ids") != []:
        sys.exit(f"ABORT increments-manifest adopted/already ids {b.get('already_adopted_ids')}")
    if b.get("probed_ids") != LOSS16:
        sys.exit("ABORT increments-manifest probed_ids != the 16 drive-1 keys")
    if int(b.get("fileless_unprobed_count", -1)) != 38 or sorted(b.get("fileless_unprobed_ids") or []) != DRIVE2_KEYS:
        sys.exit("ABORT increments-manifest fileless_unprobed_ids != the 38 drive-2 keys")
    if im.get("win_ids") != [] or im.get("unadopted_win_ids") != [] or im.get("exhausted_excluded_ids") != []:
        sys.exit("ABORT increments-manifest win/unadopted/exhausted lists not empty")
    if b.get("unadopted_win_ids") != [] or b.get("exhausted_excluded_ids") != [] or b.get("fragment_ids") != []:
        sys.exit("ABORT increments-manifest batch win/exhausted/fragment lists not empty")
    if b.get("status_log_sha256") != PIN_STATUS_DRIVE1_PREFIX or int(b.get("status_log_lines", -1)) != 16:
        sys.exit(f"ABORT increments-manifest status_log pins {b.get('status_log_sha256')}")
    if int(b.get("total_nodes_pass_one", -1)) != 57463971:
        sys.exit(f"ABORT increments-manifest total_nodes_pass_one {b.get('total_nodes_pass_one')}")
    im2 = im  # alias (direct manifest fields)
    if im2.get("full_packet_eq_loss_only") is not True or im2.get("win_scenario_exists") is not False:
        sys.exit("ABORT increments-manifest flags")
    if im2.get("sha256", {}).get("loss") != PIN_INCREMENT:
        sys.exit("ABORT increments-manifest loss sha256 != increment pin")
    if im2.get("merger_sha256") != PIN_MERGER:
        sys.exit(f"ABORT increments-manifest merger sha {im2.get('merger_sha256')}")
    if im2.get("base_cache_sha256") != "854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d":
        sys.exit("ABORT increments-manifest base cache sha")
    if int(im2.get("base_cache_rows")) != 6301 or int(im2.get("base_cache_absent_hits_for_emitted")) != 0:
        sys.exit(f"ABORT increments-manifest base cache {im2.get('base_cache_rows')},{im2.get('base_cache_absent_hits_for_emitted')}")
    if int(im2.get("quarantine_hits", -1)) != 0:
        sys.exit("ABORT increments-manifest quarantine hits")
    rc = im2.get("row_counts", {})
    if int(rc.get("probed_rows")) != 16 or int(rc.get("adopted_loss_rows")) != 16 \
            or int(rc.get("wins")) != 0 or int(rc.get("exhausted_excluded")) != 0 \
            or int(rc.get("fragments_unprobed")) != 0 or int(rc.get("fileless_unprobed")) != 38:
        sys.exit(f"ABORT increments-manifest row_counts {rc}")
    # DECLARED batch-29 adaptation of the CW id-list gates: target absent from
    # every ADOPTED/WIN/probed id list, present in fileless_unprobed_ids
    adopted_lists = {}
    for fld in ("loss_ids", "win_ids", "unadopted_win_ids", "resolved_ids"):
        adopted_lists[fld] = set(im.get(fld) or [])
    for fld in ("adopted_loss_ids", "already_adopted_ids", "unadopted_win_ids", "fragment_ids", "probed_ids"):
        adopted_lists["batches." + fld] = set(b.get(fld) or [])
    uwr_ids = set()
    for uwr in im.get("unadopted_win_rows") or []:
        if isinstance(uwr, dict) and "key_id" in uwr:
            uwr_ids.add(uwr["key_id"])
    expected_fileless = set(DRIVE2_KEYS)
    if set(b.get("fileless_unprobed_ids") or []) != expected_fileless:
        sys.exit("ABORT increments-manifest fileless roster mismatch")
    for t in TARGETS:
        for fld, s in adopted_lists.items():
            if t in s:
                sys.exit(f"ABORT {t}: target id appears in adopted/win/probed list {fld} of the Part CU increments-manifest")
        if t in uwr_ids:
            sys.exit(f"ABORT {t}: target id appears in unadopted_win_rows")
        if t not in expected_fileless:
            sys.exit(f"ABORT {t}: target id missing from fileless_unprobed_ids (CU-time UNPROBED roster)")
    # NEW cross-artifact consistency gate (declared): the drive-2 PASS roster
    # (38 keys) == batch-keys minus the CU adopted 16 == the CU manifest
    # fileless roster exactly
    if set(DRIVE2_KEYS) & set(k29) != set(DRIVE2_KEYS):
        sys.exit("ABORT drive-2 roster not a subset of the published 54 keys")
    if expected_fileless != set(DRIVE2_KEYS):
        sys.exit("ABORT cross-artifact roster mismatch")
    # -- anchors/negatives (published constants, AR->BF->...->CR->CW->CZ
    #    provenance chain)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b29ab028win-thirdimpl-input-v1",
                 "sources": {
                     "b29drive2": ("sources/raw ab028 p1+p2 + sources/status-b29.log + sources/log-b29drive2-declaration.md "
                                   "+ log-b29drive2-completion.md + batch-keys-b29.json + published batch-29 drive-2 "
                                   "canonical outputs (experiment n11-centralreply-closure-class2251-batch29-20261123, "
                                   "completion log research/log/2026-11-24-part-ci-takeover-batch29-drive2-completion.md), "
                                   "commit-pinned raw fetch; batch-keys sha256 330c0b9f..; the single target is the "
                                   "batch-29 drive-2 WIN row ab028 (budget 15000000)"),
                     "b29_batch_keys_sha256": PIN_B29,
                     "b29drive2_status_sha256": PIN_STATUS_B29,
                     "b29drive2_status_drive1_prefix_sha256": PIN_STATUS_DRIVE1_PREFIX,
                     "b29drive2_completion_log_sha256": PIN_LOG_COMPL,
                     "unadopted": ("published Part CU 16-LOSS adoption re-audit (experiment "
                                  "n11-centralreply-class2251-loss16-adoption-reaudit-20261123): merged canonical "
                                  "cache sha256 30ddad9d.. (6,317 rows = Part CO base 854800f3 6,301 + the 16 adopted "
                                  "batch-29 drive-1 LOSS rows) is UNCHANGED and carries NO row for ab028 "
                                  "(machine-gated both by this maker and by audit_cz.py G6); increment bab011e3.., "
                                  "increments-manifest f9f58ee1.., pinned fail-closed merger 90711961..; DECLARED "
                                  "batch-29 adaptation: the cross-verified drive-2 WIN row ab028 appears ONLY in "
                                  "the manifest's batches[0].fileless_unprobed_ids roster (its CU-time UNPROBED "
                                  "status), NOT in any adopted/win/probed id list; it is an UNADOPTED honest label "
                                  "pending the scrutiny owner C++ second-implementation gate 9193f5b6 unchanged"),
                     "anchors": ("published anchor/negative values, input CSVs byte-equality-checked against the "
                                 "published Part BF experiment (provenance chain AR -> BF -> BK -> BM -> BS -> BV -> "
                                 "BW -> BX -> BY -> CC -> CL -> CM -> CR -> CW -> CZ)")},
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
    print("CZ-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"])
    print("unadopted rows: absent from merged canonical cache + increment + every adopted/win id list (machine-gated)")
    print("cross-artifact: drive-2 PASS roster == batch-keys minus CU-adopted 16 == CU fileless roster (machine-gated)")

if __name__ == "__main__":
    main()
