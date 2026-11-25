# make_inputs_ck.py -- machine-derive the Part CK third-impl input CSVs and
# rows.json for the batch-28 (class 5343) drive-2 LOSS row aa003 (the row the
# Part CH pinned merger adopted into the canonical cache) from the published
# canonical artifacts (zero hand transcription). Fail-closed: any unexpected
# field aborts.
#
# Adapted from the published Part CC maker (sha256
# 8255d0adfe82ccc33d49c1339281fb18410748d165fa36e099529233249ab700,
# experiment n11-centralreply-closure-b28win-thirdimpl-20261123, itself from
# BY 359abebc... b27win / BX e1def905... b25win / BW f94d6e4f... b24win) for
# the batch-28 drive-2 LOSS-row cross-verification. Deltas (all declared in
# the Part CK declaration before execution): sources switch from Part CB to
# the published Part CD drive-2 experiment (status-cd.log 17-line battery,
# row-audit-cd 7-key battery, README-cd drive-2 phrases), the target battery
# gates the single LOSS row (result 2) instead of the 2 WIN rows, and the NEW
# adoption-corroboration source battery (merged canonical cache / increment /
# increments-manifest pins from the published Part CH adoption re-audit).
# Verdicts are NOT consumed anywhere; aa003's LOSS row was already consumed
# into the canonical cache by the separate declared Part CH adoption BEFORE
# this experiment: this experiment corroborates that exact adopted row; it
# does not adopt, free, close, or claim anything. The standard 11x11 empty
# board, the 19 central-reply roots, class 5343 and every key (aa001..aa054)
# remain UNKNOWN.
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")

# -- published source pins (Part CD drive-2 experiment
#    n11-centralreply-closure-class5343-batch28-drive2-20261123 + Part CH
#    adoption re-audit n11-centralreply-class5343-loss1-adoption-reaudit-20261123)
PIN_B28 = "af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5"
PIN_STATUS_CD = "343097c268425cc62263935f1063c26689515bc797c68bbdb82389c713952c98"
PIN_ROWAUDIT_CD = "3e86a32b847b5799594be5fbee6624878deadf02990940b2503f931d7af30e91"
PIN_README_CD = "338fc1361a2aaaa0276b9b050cf2cc0a3073f15fc64f382f5edb7e784e5dd9e6"
PIN_RAW_AA003 = {
    "aa003.p1": "9fff0eea0eddf4be3134ba41a1ce8717549ec2dc344824b643a7ca256e1af503",
    "aa003.p2": "a1edb177847cf101df458a9c6a5a86746dcd2ebd3e63fce066d037e39850bad0",
}
PIN_PUB_INPUT_AA003 = "95abcd03283027e087a14fdd660578723ece2bec346c811273261609d718e7ec"
PIN_PUB_INPUT_BF = {
    "k02a": "b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887",
    "l1a": "e13d2a6c5bbaa34833dcaf8bfaaa91f99393942281f001552cb8af49cca8c98a",
    "ng1": "8e64b9ade1c04122ac4bdc5fa5129b5fca6cfac742ed92cb149f9ffb80ad0b09",
    "ng2": "f19cd5a30b0b868f0a0c7f12a6c47376c8ceb6e862f5c769fb14bdf74e8997dc",
}
# Part CH adoption re-audit publications (merged canonical cache / increment / manifest)
PIN_MERGED_CANONICAL = "3124461b14e4f73a7248cbf5b96c7ff59ebfdcc05258adeb9c81791d86cc461e"
PIN_INCREMENT = "dc857bfd2ecd00deaea3dbe214e0eec0e5b9d7704104a8721d046f262f170487"
PIN_INCR_MANIFEST = "017c7c3036927ddc8107258029d6a89318d04d5923103d7b8ae97952225aaa71"
PIN_MERGER = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"

TARGETS = ["aa003"]
EXPECT_S5 = {"aa003": 104943}
EXPECT_MEMBERSHIP = {"aa003": 3}
EXPECT_REPLICA = {"aa003": 4070373}  # published 2-pass node-exact LOSS row
STATUS_PASS_WIN_NODES = {"aa001": 13183855, "aa002": 6527041,
                         "aa006": 14303810, "aa007": 13483540}
STATUS_EXHAUSTED_NODES = {"aa004": 15000000, "aa005": 15000000}
STATUS_EXPECT_LINES = 17
STATUS_EXPECT_PASS = 7
STATUS_EXPECT_WINHALT = 4
STATUS_EXPECT_EXHAUSTED = 2
STATUS_EXPECT_RETRY = 4
FILELESS_UNPROBED_COUNT = 47
WIN_KEYS = ["aa001", "aa002", "aa006", "aa007"]
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
    if result != 2:
        sys.exit(f"ABORT {key}: expected in-budget LOSS (result 2) row, got result={result}")
    if nodes >= 15000000:
        sys.exit(f"ABORT {key}: LOSS row at/near budget: nodes={nodes}")
    if nodes != EXPECT_REPLICA[key]:
        sys.exit(f"ABORT {key}: replica nodes {nodes} != published {EXPECT_REPLICA[key]}")
    return {"key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "replica_result": result, "replica_nodes": nodes}

def main():
    os.makedirs(OUT, exist_ok=True)
    # -- source pins
    for fname, pin in (("batch-keys-cd.json", PIN_B28), ("status-cd.log", PIN_STATUS_CD),
                       ("README-cd.md", PIN_README_CD), ("row-audit-cd.json", PIN_ROWAUDIT_CD),
                       ("canonical-cache-ch-merged-b28loss1.cache", PIN_MERGED_CANONICAL),
                       ("increment-b28loss1.cache", PIN_INCREMENT),
                       ("increments-manifest-ch.json", PIN_INCR_MANIFEST)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    for k, pin in PIN_RAW_AA003.items():
        got = sha256(os.path.join(SRC, "raw", k + ".out"))
        if got != pin:
            sys.exit(f"ABORT raw {k} sha {got} != pin {pin}")
    for kk, pin in PIN_PUB_INPUT_BF.items():
        got = sha256(os.path.join(SRC, "published-input-bf", kk + ".input.csv"))
        if got != pin:
            sys.exit(f"ABORT published-input-bf {kk} sha {got} != pin {pin}")
    if sha256(os.path.join(SRC, "published-input", "aa003.input.csv")) != PIN_PUB_INPUT_AA003:
        sys.exit("ABORT published-input aa003 sha mismatch")
    bk28 = json.load(open(os.path.join(SRC, "batch-keys-cd.json")))
    if int(bk28["class_index"]) != 5343:
        sys.exit(f"ABORT class_index {bk28.get('class_index')}")
    if bk28.get("schema") != "n11-centralreply-closure-class5343-batch28-input-v1":
        sys.exit(f"ABORT batch-keys schema {bk28.get('schema')}")
    k28 = {k["key_id"]: k for k in bk28["keys"]}
    if len(k28) != 54:
        sys.exit(f"ABORT batch keys count {len(k28)} != 54")
    if len(TARGETS) != 1 or not re.fullmatch(r"aa[0-9]{3}", TARGETS[0]):
        sys.exit("ABORT batch-28 key ids must be the 2-char aa### form (one target)")
    # -- status log battery gates (published Part CD drive-2 runner log):
    #    17 lines = 7 PASS (2 win drive-1 + 1 loss + 2 exhausted + 2 win drive-2)
    #    + 4 WIN-HALT (aa002/aa001 drive-1 + aa007/aa006 drive-2) + 2 EXHAUSTED
    #    + 4 TRUNCATED-RETRY bookkeeping lines; no FAIL/MISMATCH rows.
    slog = open(os.path.join(SRC, "status-cd.log")).read()
    lines = [l for l in slog.splitlines() if l.strip()]
    if len(lines) != STATUS_EXPECT_LINES:
        sys.exit(f"ABORT status-cd.log line count {len(lines)} != {STATUS_EXPECT_LINES}")
    kinds = {}
    for ln in lines:
        toks = ln.split()
        if len(toks) < 3:
            sys.exit(f"ABORT status-cd.log malformed line {ln!r}")
        kinds[toks[2]] = kinds.get(toks[2], 0) + 1
    if kinds.get("PASS") != STATUS_EXPECT_PASS:
        sys.exit(f"ABORT status-cd.log PASS lines {kinds.get('PASS')} != {STATUS_EXPECT_PASS}")
    if kinds.get("WIN-HALT") != STATUS_EXPECT_WINHALT:
        sys.exit(f"ABORT status-cd.log WIN-HALT lines {kinds.get('WIN-HALT')} != {STATUS_EXPECT_WINHALT}")
    if kinds.get("EXHAUSTED") != STATUS_EXPECT_EXHAUSTED:
        sys.exit(f"ABORT status-cd.log EXHAUSTED lines {kinds.get('EXHAUSTED')} != {STATUS_EXPECT_EXHAUSTED}")
    retry = sum(1 for k in kinds if k.endswith("TRUNCATED-RETRY") for _ in range(kinds[k]))
    if retry != STATUS_EXPECT_RETRY:
        sys.exit(f"ABORT status-cd.log TRUNCATED-RETRY lines {retry} != {STATUS_EXPECT_RETRY}")
    for bad_kind in ("FAIL", "MISMATCH", "LOSS-HALT"):
        if bad_kind in kinds:
            sys.exit(f"ABORT status-cd.log carries unexpected line kind {bad_kind}")
    pass_keys = [l.split()[1] for l in lines if l.split()[2] == "PASS"]
    if sorted(set(pass_keys)) != sorted(set(WIN_KEYS + EXHAUSTED_KEYS + TARGETS)):
        sys.exit(f"ABORT status-cd.log PASS key set {sorted(set(pass_keys))}")
    if len(pass_keys) != len(set(pass_keys)):
        sys.exit("ABORT status-cd.log duplicate PASS keys")
    pass_map = {}
    for l in lines:
        toks = l.split()
        if toks[2] == "PASS":
            pass_map.setdefault(toks[1], []).append(toks[3].split(","))
    for kk, nodes in STATUS_PASS_WIN_NODES.items():
        pl = pass_map.get(kk)
        if not pl or len(pl) != 1 or pl[0][0] != "15000000" or pl[0][1] != "1" or int(pl[0][2]) != nodes:
            sys.exit(f"ABORT status-cd.log win PASS row {kk}: {pl}")
    for kk in EXHAUSTED_KEYS:
        pl = pass_map.get(kk)
        if not pl or len(pl) != 1 or pl[0][0] != "15000000" or pl[0][1] != "0" or int(pl[0][2]) != STATUS_EXHAUSTED_NODES[kk]:
            sys.exit(f"ABORT status-cd.log exhausted PASS row {kk}: {pl}")
        ex_lines = [l for l in lines if l.split()[1] == kk and l.split()[2] == "EXHAUSTED"]
        if len(ex_lines) != 1:
            sys.exit(f"ABORT status-cd.log EXHAUSTED record count for {kk}: {len(ex_lines)}")
    pl = pass_map.get(TARGETS[0])
    if not pl or len(pl) != 1 or pl[0] != ["15000000", "2", str(EXPECT_REPLICA[TARGETS[0]])]:
        sys.exit(f"ABORT status-cd.log aa003 PASS row is not the published LOSS row: {pl}")
    if [l for l in lines if l.split()[1] == TARGETS[0] and l.split()[2] in ("WIN-HALT", "EXHAUSTED")]:
        sys.exit("ABORT aa003 carries an unexpected WIN-HALT/EXHAUSTED line")
    winhalt_keys = [l.split()[1] for l in lines if l.split()[2] == "WIN-HALT"]
    if sorted(winhalt_keys) != sorted(WIN_KEYS):
        sys.exit(f"ABORT status-cd.log WIN-HALT keys {sorted(winhalt_keys)} != {sorted(WIN_KEYS)}")
    # -- published row-audit battery gates (drive-2 halt-time audit)
    ra = json.load(open(os.path.join(SRC, "row-audit-cd.json")))
    if ra.get("schema") != "n11-centralreply-closure-class5343-batch28-rowaudit-winhalt-v1":
        sys.exit(f"ABORT row-audit schema {ra.get('schema')}")
    if ra.get("class_index") != 5343 or ra.get("probed") != 7 or ra.get("pass_rows") != 1:
        sys.exit(f"ABORT row-audit header {ra.get('class_index')},{ra.get('probed')},{ra.get('pass_rows')}")
    if ra.get("win_rows") != WIN_KEYS:
        sys.exit(f"ABORT row-audit win_rows {ra.get('win_rows')}")
    if ra.get("loss_rows") != TARGETS:
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
    expected_fileless = [f"aa{i:03d}" for i in range(8, 55)]
    if fm != expected_fileless:
        sys.exit(f"ABORT row-audit fileless_unprobed != aa008..aa054 exact list")
    sr = ra.get("stop_rule") or ""
    if "pre-registered WIN-HALT" not in sr or "verdict not consumed" not in sr:
        sys.exit(f"ABORT row-audit stop_rule wording: {sr[:80]}")
    expected_rows = set(ra.get("loss_rows", [])) | set(ra.get("win_rows", [])) | set(ra.get("exhausted_rows", []))
    if set(pass_keys) != expected_rows:
        sys.exit(f"ABORT status PASS keys {sorted(set(pass_keys))} != row-audit probed rows {sorted(expected_rows)}")
    # -- README-cd drive-2 phrase battery (whitespace-normalized)
    rd = re.sub(r"\s+", " ", open(os.path.join(SRC, "README-cd.md")).read())
    for phrase in ("aa003 PASS (result 2 = LOSS行・nodes 4,070,373)",
                   "aa006 WIN-HALT (result 1・nodes 14,303,810)",
                   "aa007 WIN-HALT (result 1・nodes 13,483,540)",
                   "(aa008..aa054) はfileless UNPROBEDのまま",
                   "scrutiny owner C++第二実装",
                   "class 5343",
                   "Part CD"):
        if phrase not in rd:
            sys.exit(f"ABORT README-cd lacks phrase: {phrase!r}")
    if "閉鎖・被覆・secured・root勝敗の主張はしない" not in rd:
        sys.exit("ABORT README-cd lacks the no-claims guard")
    # -- per-target raw cross-verification
    rows = []
    for key in TARGETS:
        bk = k28.get(key)
        if bk is None or int(bk["s5_index"]) != EXPECT_S5[key]:
            sys.exit(f"ABORT {key}: batch-28 s5_index {bk and bk.get('s5_index')}")
        if int(bk["membership_class_count"]) != EXPECT_MEMBERSHIP[key]:
            sys.exit(f"ABORT {key}: membership_class_count {bk.get('membership_class_count')}")
        r = parse_raw(key, k28)
        r["source"] = "part-cd-batch28-loss"
        r["s5_index"] = int(bk["s5_index"])
        r["membership_class_count"] = int(bk["membership_class_count"])
        r["expect_third"] = 2
        rows.append(r)
    # -- NEW adoption-corroboration battery (Part CH publications):
    #    the row this experiment cross-verifies must be the EXACT row the
    #    pinned fail-closed merger adopted into the canonical cache.
    t0 = rows[0]
    adopted_row = f"s5verdict,{t0['lo']},{t0['hi']},5,{t0['replica_result']},{t0['replica_nodes']}"
    merged = open(os.path.join(SRC, "canonical-cache-ch-merged-b28loss1.cache")).read().splitlines()
    s5rows = [l for l in merged if l.startswith("s5verdict,")]
    if len(s5rows) != 6294:
        sys.exit(f"ABORT merged canonical cache s5verdict rows {len(s5rows)} != 6294")
    hits = [l for l in s5rows if l == adopted_row]
    if len(hits) != 1:
        sys.exit(f"ABORT adopted row in merged cache occurs {len(hits)} times (expect exactly 1)")
    other_key = [l for l in s5rows if l.startswith(f"s5verdict,{t0['lo']},{t0['hi']},") and l != adopted_row]
    if other_key:
        sys.exit(f"ABORT merged cache carries a conflicting row for the same key: {other_key}")
    inc = open(os.path.join(SRC, "increment-b28loss1.cache")).read().splitlines()
    inc_rows = [l for l in inc if l.startswith("s5verdict,")]
    if inc_rows != [adopted_row]:
        sys.exit(f"ABORT increment rows != the single adopted row: {inc_rows}")
    if "ADOPTED set = {aa003}" not in "\n".join(inc):
        sys.exit("ABORT increment header lacks the ADOPTED set statement")
    im = json.load(open(os.path.join(SRC, "increments-manifest-ch.json")))
    if im.get("schema") != "b28loss1-increments-manifest-v1":
        sys.exit(f"ABORT increments-manifest schema {im.get('schema')}")
    if im.get("loss_ids") != TARGETS or im.get("resolved_ids") and sorted(im["resolved_ids"]) != sorted(WIN_KEYS + EXHAUSTED_KEYS + TARGETS):
        sys.exit(f"ABORT increments-manifest loss/resolved ids {im.get('loss_ids')},{im.get('resolved_ids')}")
    b = im["batches"][0]
    if b.get("adopted_loss_ids") != TARGETS or b.get("batch") != 28 or int(b.get("class_index")) != 5343:
        sys.exit(f"ABORT increments-manifest batch block {b.get('adopted_loss_ids')}")
    if b.get("unadopted_win_ids") != WIN_KEYS or b.get("exhausted_excluded_ids") != EXHAUSTED_KEYS:
        sys.exit(f"ABORT increments-manifest win/exhausted ids {b.get('unadopted_win_ids')}")
    if b.get("input_sha256") != PIN_B28 or b.get("row_audit_sha256") != PIN_ROWAUDIT_CD or b.get("status_log_sha256") != PIN_STATUS_CD:
        sys.exit("ABORT increments-manifest source sha pins")
    if int(b.get("total_nodes_pass_one")) != t0["replica_nodes"] or int(b.get("total_nodes_pass_two")) != t0["replica_nodes"]:
        sys.exit(f"ABORT increments-manifest total_nodes {b.get('total_nodes_pass_one')},{b.get('total_nodes_pass_two')}")
    if int(b.get("fileless_unprobed_count")) != FILELESS_UNPROBED_COUNT:
        sys.exit("ABORT increments-manifest fileless count")
    if im.get("sha256", {}).get("loss") != PIN_INCREMENT:
        sys.exit("ABORT increments-manifest loss sha256 != increment pin")
    if im.get("merger_sha256") != PIN_MERGER:
        sys.exit(f"ABORT increments-manifest merger sha {im.get('merger_sha256')}")
    if int(im.get("base_cache_rows")) != 6293 or int(im.get("base_cache_absent_hits")) != 0:
        sys.exit(f"ABORT increments-manifest base cache {im.get('base_cache_rows')},{im.get('base_cache_absent_hits')}")
    if im.get("full_packet_eq_loss_only") is not False:
        sys.exit("ABORT increments-manifest full == loss")
    rc = im.get("row_counts", {})
    if int(rc.get("adopted_loss_rows")) != 1 or int(rc.get("wins")) != 4 or int(rc.get("exhausted_excluded")) != 2 or int(rc.get("fileless_unprobed")) != FILELESS_UNPROBED_COUNT:
        sys.exit(f"ABORT increments-manifest row_counts {rc}")
    # -- anchors/negatives (published constants, AR->BF->BK->BM->BS->BV->BW->BX->BY->CC->CK provenance chain)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b28drive2loss-thirdimpl-input-v1",
                 "sources": {
                     "b28drive2": ("sources/raw aa003.p1/p2 + sources/status-cd.log + sources/row-audit-cd.json + "
                                  "batch-keys-cd.json + published batch-28 drive-2 (Part CD) canonical outputs "
                                  "(experiment n11-centralreply-closure-class5343-batch28-drive2-20261123, "
                                  "MANIFEST 2811b577..), commit-pinned raw fetch; batch-keys sha256 af19208f.."),
                     "b28_batch_keys_sha256": PIN_B28,
                     "b28drive2_row_audit_sha256": PIN_ROWAUDIT_CD,
                     "b28drive2_status_sha256": PIN_STATUS_CD,
                     "adoption": ("published Part CH 1-LOSS adoption re-audit (experiment "
                                  "n11-centralreply-class5343-loss1-adoption-reaudit-20261123): merged canonical "
                                  "cache sha256 3124461b.. (6294 rows, BASE 6293 + aa003 only), increment "
                                  "dc857bfd.., increments-manifest 017c7c30.., pinned fail-closed merger "
                                  "90711961..; the adopted row == the raw aa003 LOSS row byte-for-byte "
                                  "(machine-gated both by this maker and by audit_ck.py G6)"),
                     "anchors": ("published Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK/BM/BS/BV/BW/BX/BY/CC "
                                 "anchor/negative values, input CSVs byte-equality-checked against the published "
                                 "Part BF experiment (provenance chain AR -> BF -> BK -> BM -> BS -> BV -> BW -> "
                                 "BX -> BY -> CC -> CK)")},
                 "consumed_into_canonical_cache": False,
                 "adopted_before_this_experiment_by_part_ch": True,
                 "adopted_canonical_cache_sha256": PIN_MERGED_CANONICAL,
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
    print("CK-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"])
    print("adopted canonical row byte-gated:", adopted_row)

if __name__ == "__main__":
    main()
