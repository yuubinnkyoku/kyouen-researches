# make_inputs_cm.py -- machine-derive the Part CM third-impl input CSVs and
# rows.json for the two published batch-28 (class 5343) drive-3 WIN-HALT
# rows aa008 and aa009 (unconsumed closure WIN candidates 34/35) from the
# published canonical artifacts (zero hand transcription). Fail-closed: any
# unexpected field aborts.
#
# Adapted from the published Part CL maker (maker make_inputs_ck.py, sha256
# 177c4409, experiment n11-centralreply-closure-b28drive2loss-thirdimpl-
# 20261123, itself from the published Part CC maker 8255d0ad..., experiment
# n11-centralreply-closure-b28win-thirdimpl-20261123 / BY 359abebc...
# b27win / BX e1def905... b25win / BW f94d6e4f... b24win). Deltas (all
# declared in the Part CM declaration before execution): sources switch from
# the Part CD drive-2 experiment to the published Part CJ drive-3 experiment
# (status-cj.log 21-line battery, row-audit-cj 9-key battery, README-cj
# drive-3 phrases), the target battery gates the TWO drive-3 WIN-HALT rows
# (result 1 = WIN rows) instead of the single adopted LOSS row, and the
# adoption-corroboration source battery is replaced by the NEW
# unadopted-WIN-row corroboration battery (the two cross-verified WIN rows
# must NOT appear anywhere in the Part CH adopted canonical cache / increment
# / increments-manifest -- verdicts never consumed, canonical cache 3124461b
# unchanged). Verdicts are NOT consumed anywhere; aa008/aa009 are honest WIN
# labels pending the scrutiny owner C++ second-implementation gate 9193f5b6
# unchanged. The standard 11x11 empty board, the 19 central-reply roots,
# class 5343 and every key (aa001..aa054) remain UNKNOWN.
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")

# -- published source pins (Part CJ drive-3 experiment
#    n11-centralreply-closure-class5343-batch28-drive3-20261123 + Part CH
#    adoption re-audit n11-centralreply-class5343-loss1-adoption-reaudit-20261123)
PIN_B28 = "af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5"
PIN_STATUS_CJ = "1a5c08c516dbc34bde466a55a39f7e9acdfef57f09bc1bd7e19d2efb9fd5137c"
PIN_ROWAUDIT_CJ = "eb1d1e98f967925a92739fca5fcf925c37a8e3f488434926b8625195c0241402"
PIN_README_CJ = "3615b5c1f02fd841eeefcc2fd2c0cda92182c0a5d14166521de4583a30e4356a"
PIN_RAW_CM = {
    "aa008.p1": "f87c2ae9968b17b443b222921fbf2c0d57630792fe55675eeeb941e319759e84",
    "aa008.p2": "5546ed29d5af5dc499e107656f61c44ee73f3a924568dcbf3b04e9fe3572a9ba",
    "aa009.p1": "50c32fd5e354f2242119b8d034b50ca045f9d51b55b3dfff813fb49b1e83b3b8",
    "aa009.p2": "d79fc6d870ef6c561778854694b6f319d7f0c5985a920ecd3bc1b246d7399381",
}
PIN_PUB_INPUT = {
    "aa008": "3aaf4e1b6ddb69c2ca4cf184bc3ed4d77e32666242d0e43df68bb957bd3f0bb1",
    "aa009": "47ce8cf9aeafdbc07e75b9a52431a3f2e100655a1c2ab68ae27de3411f28fee6",
}
PIN_PUB_INPUT_BF = {
    "k02a": "b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887",
    "l1a": "e13d2a6c5bbaa34833dcaf8bfaaa91f99393942281f001552cb8af49cca8c98a",
    "ng1": "8e64b9ade1c04122ac4bdc5fa5129b5fca6cfac742ed92cb149f9ffb80ad0b09",
    "ng2": "f19cd5a30b0b868f0a0c7f12a6c47376c8ceb6e862f5c769fb14bdf74e8997dc",
}
# Part CH adoption re-audit publications (canonical cache / increment / manifest --
# for the NEW unadopted-WIN-row corroboration battery: aa008/aa009 must NOT appear)
PIN_MERGED_CANONICAL = "3124461b14e4f73a7248cbf5b96c7ff59ebfdcc05258adeb9c81791d86cc461e"
PIN_INCREMENT = "dc857bfd2ecd00deaea3dbe214e0eec0e5b9d7704104a8721d046f262f170487"
PIN_INCR_MANIFEST = "017c7c3036927ddc8107258029d6a89318d04d5923103d7b8ae97952225aaa71"
PIN_MERGER = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"

TARGETS = ["aa008", "aa009"]
EXPECT_S5 = {"aa008": 140489, "aa009": 142299}
EXPECT_MEMBERSHIP = {"aa008": 4, "aa009": 4}
EXPECT_REPLICA = {"aa008": 5270340, "aa009": 7319605}  # published 2-pass node-exact WIN-HALT rows
STATUS_EXHAUSTED_NODES = {"aa004": 15000000, "aa005": 15000000}
STATUS_PASS_WIN_NODES = {"aa001": 13183855, "aa002": 6527041,
                         "aa006": 14303810, "aa007": 13483540,
                         "aa008": 5270340, "aa009": 7319605}
STATUS_PASS_LOSS_NODES = {"aa003": 4070373}
STATUS_EXPECT_LINES = 21
STATUS_EXPECT_PASS = 9
STATUS_EXPECT_WINHALT = 6
STATUS_EXPECT_EXHAUSTED = 2
STATUS_EXPECT_RETRY = 4
FILELESS_UNPROBED_COUNT = 45
WIN_KEYS = ["aa001", "aa002", "aa006", "aa007", "aa008", "aa009"]
LOSS_KEYS = ["aa003"]
EXHAUSTED_KEYS = ["aa004", "aa005"]

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
        sys.exit(f"ABORT {key}: expected in-budget WIN-HALT (result 1) row, got result={result}")
    if nodes >= 15000000:
        sys.exit(f"ABORT {key}: WIN row at/near budget: nodes={nodes}")
    if nodes != EXPECT_REPLICA[key]:
        sys.exit(f"ABORT {key}: replica nodes {nodes} != published {EXPECT_REPLICA[key]}")
    return {"key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "replica_result": result, "replica_nodes": nodes}

def main():
    os.makedirs(OUT, exist_ok=True)
    # -- source pins
    for fname, pin in (("batch-keys-cd.json", PIN_B28), ("status-cj.log", PIN_STATUS_CJ),
                       ("README-cj.md", PIN_README_CJ), ("row-audit-cj.json", PIN_ROWAUDIT_CJ),
                       ("canonical-cache-ch-merged-b28loss1.cache", PIN_MERGED_CANONICAL),
                       ("increment-b28loss1.cache", PIN_INCREMENT),
                       ("increments-manifest-ch.json", PIN_INCR_MANIFEST)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    for k, pin in PIN_RAW_CM.items():
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
    bk28 = json.load(open(os.path.join(SRC, "batch-keys-cd.json")))
    if int(bk28["class_index"]) != 5343:
        sys.exit(f"ABORT class_index {bk28.get('class_index')}")
    if bk28.get("schema") != "n11-centralreply-closure-class5343-batch28-input-v1":
        sys.exit(f"ABORT batch-keys schema {bk28.get('schema')}")
    k28 = {k["key_id"]: k for k in bk28["keys"]}
    if len(k28) != 54:
        sys.exit(f"ABORT batch keys count {len(k28)} != 54")
    if sorted(TARGETS) != ["aa008", "aa009"] or len(TARGETS) != 2:
        sys.exit("ABORT Part CM targets must be exactly the two drive-3 WIN-HALT rows aa008/aa009")
    for t in TARGETS:
        if not re.fullmatch(r"aa[0-9]{3}", t):
            sys.exit(f"ABORT batch-28 key id form {t}")
    # -- status log battery gates (published Part CJ drive-3 runner log):
    #    21 lines = 9 PASS (2 win drive-1 + 1 loss + 2 exhausted + 2 win drive-2
    #    + 2 win drive-3) + 6 WIN-HALT (aa002/aa001 drive-1 + aa007/aa006 drive-2
    #    + aa008/aa009 drive-3) + 2 EXHAUSTED + 4 TRUNCATED-RETRY bookkeeping
    #    lines; no FAIL/MISMATCH rows.
    slog = open(os.path.join(SRC, "status-cj.log")).read()
    lines = [l for l in slog.splitlines() if l.strip()]
    if len(lines) != STATUS_EXPECT_LINES:
        sys.exit(f"ABORT status-cj.log line count {len(lines)} != {STATUS_EXPECT_LINES}")
    kinds = {}
    for ln in lines:
        toks = ln.split()
        if len(toks) < 3:
            sys.exit(f"ABORT status-cj.log malformed line {ln!r}")
        kinds[toks[2]] = kinds.get(toks[2], 0) + 1
    if kinds.get("PASS") != STATUS_EXPECT_PASS:
        sys.exit(f"ABORT status-cj.log PASS lines {kinds.get('PASS')} != {STATUS_EXPECT_PASS}")
    if kinds.get("WIN-HALT") != STATUS_EXPECT_WINHALT:
        sys.exit(f"ABORT status-cj.log WIN-HALT lines {kinds.get('WIN-HALT')} != {STATUS_EXPECT_WINHALT}")
    if kinds.get("EXHAUSTED") != STATUS_EXPECT_EXHAUSTED:
        sys.exit(f"ABORT status-cj.log EXHAUSTED lines {kinds.get('EXHAUSTED')} != {STATUS_EXPECT_EXHAUSTED}")
    retry = sum(1 for k in kinds if k.endswith("TRUNCATED-RETRY") for _ in range(kinds[k]))
    if retry != STATUS_EXPECT_RETRY:
        sys.exit(f"ABORT status-cj.log TRUNCATED-RETRY lines {retry} != {STATUS_EXPECT_RETRY}")
    for bad_kind in ("FAIL", "MISMATCH", "LOSS-HALT"):
        if bad_kind in kinds:
            sys.exit(f"ABORT status-cj.log carries unexpected line kind {bad_kind}")
    pass_keys = [l.split()[1] for l in lines if l.split()[2] == "PASS"]
    if sorted(set(pass_keys)) != sorted(set(WIN_KEYS + EXHAUSTED_KEYS + LOSS_KEYS)):
        sys.exit(f"ABORT status-cj.log PASS key set {sorted(set(pass_keys))}")
    if len(pass_keys) != len(set(pass_keys)):
        sys.exit("ABORT status-cj.log duplicate PASS keys")
    pass_map = {}
    for l in lines:
        toks = l.split()
        if toks[2] == "PASS":
            pass_map.setdefault(toks[1], []).append(toks[3].split(","))
    for kk, nodes in STATUS_PASS_WIN_NODES.items():
        pl = pass_map.get(kk)
        if not pl or len(pl) != 1 or pl[0][0] != "15000000" or pl[0][1] != "1" or int(pl[0][2]) != nodes:
            sys.exit(f"ABORT status-cj.log win PASS row {kk}: {pl}")
    for kk, nodes in STATUS_PASS_LOSS_NODES.items():
        pl = pass_map.get(kk)
        if not pl or len(pl) != 1 or pl[0] != ["15000000", "2", str(nodes)]:
            sys.exit(f"ABORT status-cj.log loss PASS row {kk}: {pl}")
    for kk in EXHAUSTED_KEYS:
        pl = pass_map.get(kk)
        if not pl or len(pl) != 1 or pl[0][0] != "15000000" or pl[0][1] != "0" or int(pl[0][2]) != STATUS_EXHAUSTED_NODES[kk]:
            sys.exit(f"ABORT status-cj.log exhausted PASS row {kk}: {pl}")
        ex_lines = [l for l in lines if l.split()[1] == kk and l.split()[2] == "EXHAUSTED"]
        if len(ex_lines) != 1:
            sys.exit(f"ABORT status-cj.log EXHAUSTED record count for {kk}: {len(ex_lines)}")
    for kk in TARGETS:
        pl = pass_map.get(kk)
        if not pl or len(pl) != 1 or pl[0] != ["15000000", "1", str(EXPECT_REPLICA[kk])]:
            sys.exit(f"ABORT status-cj.log {kk} PASS row is not the published drive-3 WIN-HALT row: {pl}")
        if [l for l in lines if l.split()[1] == kk and l.split()[2] == "EXHAUSTED"]:
            sys.exit(f"ABORT {kk} carries an unexpected EXHAUSTED line")
    winhalt_keys = [l.split()[1] for l in lines if l.split()[2] == "WIN-HALT"]
    if sorted(winhalt_keys) != sorted(WIN_KEYS):
        sys.exit(f"ABORT status-cj.log WIN-HALT keys {sorted(winhalt_keys)} != {sorted(WIN_KEYS)}")
    for kk in TARGETS:
        wh = [l for l in lines if l.split()[1] == kk and l.split()[2] == "WIN-HALT"]
        if len(wh) != 1:
            sys.exit(f"ABORT status-cj.log {kk} WIN-HALT record count {len(wh)}")
    # -- published row-audit battery gates (drive-3 halt-time audit)
    ra = json.load(open(os.path.join(SRC, "row-audit-cj.json")))
    if ra.get("schema") != "n11-centralreply-closure-class5343-batch28-rowaudit-winhalt-v1":
        sys.exit(f"ABORT row-audit schema {ra.get('schema')}")
    if ra.get("class_index") != 5343 or ra.get("probed") != 9 or ra.get("pass_rows") != 1:
        sys.exit(f"ABORT row-audit header {ra.get('class_index')},{ra.get('probed')},{ra.get('pass_rows')}")
    if ra.get("win_rows") != WIN_KEYS:
        sys.exit(f"ABORT row-audit win_rows {ra.get('win_rows')}")
    if ra.get("loss_rows") != LOSS_KEYS:
        sys.exit(f"ABORT row-audit loss_rows {ra.get('loss_rows')}")
    if ra.get("exhausted_rows") != EXHAUSTED_KEYS:
        sys.exit(f"ABORT row-audit exhausted_rows {ra.get('exhausted_rows')}")
    if ra.get("mismatches") != 0:
        sys.exit(f"ABORT row-audit mismatches {ra.get('mismatches')}")
    if ra.get("unprobed_count") != FILELESS_UNPROBED_COUNT:
        sys.exit(f"ABORT row-audit unprobed_count {ra.get('unprobed_count')}")
    if ra.get("derived_state") is not True:
        sys.exit(f"ABORT row-audit derived_state {ra.get('derived_state')}")
    if ra.get("batch") != 28 or ra.get("keys_total") != 54:
        sys.exit(f"ABORT row-audit batch/keys_total {ra.get('batch')},{ra.get('keys_total')}")
    if ra.get("input_sha256") != PIN_B28:
        sys.exit("ABORT row-audit input_sha256 != batch-keys pin")
    frag = ra.get("fragment_keys") or {}
    if frag != {}:
        sys.exit(f"ABORT row-audit fragment_keys {sorted(frag.keys())} != empty")
    fm = ra.get("fileless_unprobed") or []
    expected_fileless = [f"aa{i:03d}" for i in range(10, 55)]
    if fm != expected_fileless:
        sys.exit("ABORT row-audit fileless_unprobed != aa010..aa054 exact list")
    sr = ra.get("stop_rule") or ""
    if "pre-registered WIN-HALT" not in sr or "verdict not consumed" not in sr:
        sys.exit(f"ABORT row-audit stop_rule wording: {sr[:80]}")
    expected_rows = set(ra.get("loss_rows", [])) | set(ra.get("win_rows", [])) | set(ra.get("exhausted_rows", []))
    if set(pass_keys) != expected_rows:
        sys.exit(f"ABORT status PASS keys {sorted(set(pass_keys))} != row-audit probed rows {sorted(expected_rows)}")
    # -- README-cj drive-3 phrase battery (whitespace-normalized)
    rd = re.sub(r"\s+", " ", open(os.path.join(SRC, "README-cj.md")).read())
    for phrase in ("aa008 WIN-HALT (result 1・nodes 5,270,340・legal 85・2-pass node-exact)",
                   "aa009 WIN-HALT (result 1・nodes 7,319,605・legal 91・2-pass node-exact)",
                   "残り45キー (aa010..aa054) はfileless UNPROBEDのまま",
                   "scrutiny owner",
                   "class 5343",
                   "Part CJ",
                   "verdict不消費"):
        if phrase not in rd:
            sys.exit(f"ABORT README-cj lacks phrase: {phrase!r}")
    if "閉鎖・被覆・secured・root勝敗の主張はしない" not in rd:
        sys.exit("ABORT README-cj lacks the no-claims guard")
    # -- per-target raw cross-verification
    rows = []
    for key in TARGETS:
        bk = k28.get(key)
        if bk is None or int(bk["s5_index"]) != EXPECT_S5[key]:
            sys.exit(f"ABORT {key}: batch-28 s5_index {bk and bk.get('s5_index')}")
        if int(bk["membership_class_count"]) != EXPECT_MEMBERSHIP[key]:
            sys.exit(f"ABORT {key}: membership_class_count {bk.get('membership_class_count')}")
        r = parse_raw(key, k28)
        r["source"] = "part-cj-batch28-drive3win"
        r["s5_index"] = int(bk["s5_index"])
        r["membership_class_count"] = int(bk["membership_class_count"])
        r["expect_third"] = 1
        rows.append(r)
    # -- NEW unadopted-WIN-row corroboration battery (Part CH publications):
    #    the two rows this experiment cross-verifies must NOT appear anywhere
    #    in the adopted canonical cache / increment / increments-manifest.
    #    Verdicts never consumed; canonical cache 3124461b unchanged.
    merged = open(os.path.join(SRC, "canonical-cache-ch-merged-b28loss1.cache")).read().splitlines()
    s5rows = [l for l in merged if l.startswith("s5verdict,")]
    if len(s5rows) != 6294:
        sys.exit(f"ABORT merged canonical cache s5verdict rows {len(s5rows)} != 6294")
    for r in rows:
        win_row = f"s5verdict,{r['lo']},{r['hi']},5,{r['replica_result']},{r['replica_nodes']}"
        hits = [l for l in s5rows if l == win_row]
        if hits:
            sys.exit(f"ABORT {r['key_id']}: WIN row unexpectedly present in the adopted canonical cache: {hits}")
        other_key = [l for l in s5rows if l.startswith(f"s5verdict,{r['lo']},{r['hi']},")]
        if other_key:
            sys.exit(f"ABORT merged cache carries a conflicting row for the same key: {other_key}")
    inc = open(os.path.join(SRC, "increment-b28loss1.cache")).read().splitlines()
    inc_rows = [l for l in inc if l.startswith("s5verdict,")]
    if inc_rows != ["s5verdict,1152921504741064704,4228,5,2,4070373"]:
        sys.exit(f"ABORT increment rows != the single aa003 adopted row: {inc_rows}")
    if "ADOPTED set = {aa003}" not in "\n".join(inc):
        sys.exit("ABORT increment header lacks the ADOPTED set statement")
    im = json.load(open(os.path.join(SRC, "increments-manifest-ch.json")))
    if im.get("schema") != "b28loss1-increments-manifest-v1":
        sys.exit(f"ABORT increments-manifest schema {im.get('schema')}")
    if im.get("loss_ids") != LOSS_KEYS:
        sys.exit(f"ABORT increments-manifest loss_ids {im.get('loss_ids')}")
    b = im["batches"][0]
    if b.get("adopted_loss_ids") != LOSS_KEYS or b.get("batch") != 28 or int(b.get("class_index")) != 5343:
        sys.exit(f"ABORT increments-manifest batch block {b.get('adopted_loss_ids')}")
    if b.get("unadopted_win_ids") != ["aa001", "aa002", "aa006", "aa007"] or b.get("exhausted_excluded_ids") != EXHAUSTED_KEYS:
        sys.exit(f"ABORT increments-manifest win/exhausted ids {b.get('unadopted_win_ids')}")
    if b.get("input_sha256") != PIN_B28:
        sys.exit("ABORT increments-manifest input sha pin")
    if int(b.get("fileless_unprobed_count")) != 47:
        sys.exit("ABORT increments-manifest fileless count (Part CH time: aa008/aa009 were fileless)")
    if im.get("sha256", {}).get("loss") != PIN_INCREMENT:
        sys.exit("ABORT increments-manifest loss sha256 != increment pin")
    if im.get("merger_sha256") != PIN_MERGER:
        sys.exit(f"ABORT increments-manifest merger sha {im.get('merger_sha256')}")
    if int(im.get("base_cache_rows")) != 6293 or int(im.get("base_cache_absent_hits")) != 0:
        sys.exit(f"ABORT increments-manifest base cache {im.get('base_cache_rows')},{im.get('base_cache_absent_hits')}")
    if im.get("full_packet_eq_loss_only") is not False:
        sys.exit("ABORT increments-manifest full == loss")
    rc = im.get("row_counts", {})
    if int(rc.get("adopted_loss_rows")) != 1 or int(rc.get("wins")) != 4 or int(rc.get("exhausted_excluded")) != 2 or int(rc.get("fileless_unprobed")) != 47:
        sys.exit(f"ABORT increments-manifest row_counts {rc}")
    # machine scan over every id LIST in the manifest (NOT raw text scan: the
    # manifest prose legitimately mentions the pre-drive-3 fileless range
    # "aa008..aa054" in fragment_rows_note, which carries no id-list entry)
    man_ids = set()
    for fld in ("loss_ids", "win_ids", "unadopted_win_ids", "exhausted_excluded_ids", "resolved_ids"):
        v = im.get(fld) or []
        if not isinstance(v, list):
            sys.exit(f"ABORT increments-manifest {fld} is not a list")
        man_ids |= set(v)
    for b in im.get("batches", []):
        for fld in ("adopted_loss_ids", "unadopted_win_ids", "exhausted_excluded_ids", "fragment_ids", "probed_ids"):
            v = b.get(fld) or []
            if not isinstance(v, list):
                sys.exit(f"ABORT increments-manifest batch {fld} is not a list")
            man_ids |= set(v)
    for uwr in im.get("unadopted_win_rows") or []:
        if isinstance(uwr, dict) and "key_id" in uwr:
            man_ids.add(uwr["key_id"])
    for t in TARGETS:
        if t in man_ids:
            sys.exit(f"ABORT {t}: target id must not appear in any id list of the Part CH increments-manifest")
    # -- anchors/negatives (published constants, AR->BF->BK->BM->BS->BV->BW->BX->BY->CC->CL provenance chain)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b28drive3win-thirdimpl-input-v1",
                 "sources": {
                     "b28drive3": ("sources/raw aa008/aa009 p1+p2 + sources/status-cj.log + sources/row-audit-cj.json "
                                  "+ batch-keys-cd.json + published batch-28 drive-3 (Part CJ) canonical outputs "
                                  "(experiment n11-centralreply-closure-class5343-batch28-drive3-20261123, "
                                  "MANIFEST at commit eed9f348), commit-pinned raw fetch; batch-keys sha256 af19208f.."),
                     "b28_batch_keys_sha256": PIN_B28,
                     "b28drive3_row_audit_sha256": PIN_ROWAUDIT_CJ,
                     "b28drive3_status_sha256": PIN_STATUS_CJ,
                     "unadopted": ("published Part CH 1-LOSS adoption re-audit (experiment "
                                  "n11-centralreply-class5343-loss1-adoption-reaudit-20261123): merged canonical "
                                  "cache sha256 3124461b.. (6294 rows, BASE 6293 + aa003 only) is UNCHANGED and "
                                  "carries NO row for aa008/aa009 (machine-gated both by this maker and by "
                                  "audit_cm.py G6); increment dc857bfd.., increments-manifest 017c7c30.., pinned "
                                  "fail-closed merger 90711961..; the two cross-verified WIN rows are UNADOPTED "
                                  "honest labels pending the scrutiny owner C++ second-implementation gate "
                                  "9193f5b6 unchanged"),
                     "anchors": ("published Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK/BM/BS/BV/BW/BX/BY/CC/CL "
                                 "anchor/negative values, input CSVs byte-equality-checked against the published "
                                 "Part BF experiment (provenance chain AR -> BF -> BK -> BM -> BS -> BV -> BW -> "
                                 "BX -> BY -> CC -> CL -> CM)")},
                 "consumed_into_canonical_cache": False,
                 "unadopted_win_rows": True,
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
    print("CM-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"])
    print("unadopted WIN rows: absent from merged canonical cache + increment + manifest (machine-gated)")

if __name__ == "__main__":
    main()
