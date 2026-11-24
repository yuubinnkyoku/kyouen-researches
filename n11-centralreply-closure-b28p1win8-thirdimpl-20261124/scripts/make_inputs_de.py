# make_inputs_de.py -- machine-derive the Part DE third-impl input CSVs and
# rows.json for the EIGHT published batch-28 (closure class 5343) drive-4/5
# 15M-probe WIN rows of the P1 package of the b28-win46 third-impl queue
# registry: aa046 (key 1152921779484753920,4228, legal 78, nodes 2,185,149,
# decisive drive5) / aa016 (1171516445255860224,0, legal 78, nodes 2,621,847,
# drive4) / aa025 (1171516720133701632,0, legal 80, nodes 3,056,950, drive4)
# / aa033 (1171516445255794688,128, legal 86, nodes 3,347,117, drive5) /
# aa027 (1171516445255794688,64, legal 81, nodes 4,860,191, drive4) / aa038
# (1152921504606849024,4228, legal 82, nodes 4,911,996, drive5) / aa012
# (1171516445255798784,0, legal 81, nodes 4,994,213, drive4) / aa042
# (1152921504606847008,4228, legal 88, nodes 5,800,791, drive5) -- all
# UNCONSUMED honest probe-level labels, from the published canonical
# artifacts (zero hand transcription). Fail-closed: any unexpected field
# aborts.
#
# Adapted from the published Part CX maker (make_inputs_cx.py, sha256
# 7abf48c5e15607db250d141ec47480d92fe227dde292d01ba29594505c7c8958,
# experiment n11-centralreply-closure-b28cqwin5-thirdimpl-20261124, itself
# from the published Part CW maker 8a9fe75e... / CR 364a217f... / CM
# f926b5be... / CL 177c4409 / CC 8255d0ad / BY 359aebef / BX e1def905 / BW
# f94d6e4f). Declared deltas (all in the Part DE declaration before
# execution):
# (a) sources are the published batch-28 drive-4/drive-5 experiments (class
#     5343, n11-centralreply-closure-class5343-batch28-drive{4,5}-20261123):
#     status-drive4.log 59817444... / status-drive5.log ca1e98cc... (raw
#     node-exact rows for the eight targets, pinned decisive PASS + WIN-HALT
#     lines) and their output/raw p1/p2 byte pins (PIN_RAW_DE, 16 files);
#     batch-keys-b28.json af19208f...; the b28-win46 third-impl queue
#     registry (queue-registry.json 8c4216c6... + README-queue.md 00d1062e...)
#     supplies the published P1 package roster (8 keys, pinned nodes total
#     31,778,254) and the honest-label/unknown guard wording;
# (b) the target battery gates EIGHT batch-28 drive-4/5 15M-solved WIN rows
#     (aa046/aa016/aa025/aa033/aa027/aa038/aa012/aa042, all result 1, budget
#     15000000) instead of CX's five CQ 20M-reprobe rows; the replica budget
#     gate is 15000000 (the published batch-28 drive-4/5 probe condition),
#     and the batch-28 s5_index/membership values come from
#     batch-keys-b28.json;
# (c) the unadopted-corroboration sources switch to the CURRENT canonical
#     chain head (Part DB batch-29 37-LOSS adoption publications: merged
#     canonical cache 04b0a239... 6,354 rows, base CU 30ddad9d...; increment
#     b29loss37 85bd4469...; increments-manifest-db 1b51f30d... KEEPING the
#     Part CO 7-LOSS adoption publications as the batch-28 roster source
#     (merged canonical cache 854800f3... 6,301 rows; increment bd5ef7d7...
#     7 rows; increments-manifest-co b47e07ca...)). DECLARED batch-28
#     member adaptation for DE (unlike CX, whose targets were CO-time
#     15M-EXHAUSTED): the eight DE targets were 15M-solved WIN rows at CO
#     time, so they legitimately appear in the CO manifest's win_ids /
#     unadopted_win_ids / unadopted_win_rows / probed_ids / resolved_ids and
#     must NOT appear in exhausted_excluded_ids or any loss/adopted/fragment
#     list. The machine gates below require the targets to (i) carry NO
#     s5verdict row in EITHER the Part CO merged cache (6,301 rows) or the
#     Part DB merged cache (6,354 rows -- the current canonical chain head:
#     verdict non-consumption at the current state), (ii) be absent from the
#     CO increment (7 LOSS rows) and from the DB increment rows and from
#     every ADOPTED id list of both manifests (loss_ids / batches
#     adopted_loss_ids / already_adopted_ids / fragment_ids) and from
#     exhausted_excluded_ids, (iii) be PRESENT in the CO roster win lists
#     with node-exact unadopted_win_rows entries (result 1, pinned nodes,
#     two_pass_node_exact true) and in probed_ids/resolved_ids, and (iv) be
#     absent from the entire Part DB manifest text (batch-29 scope only).
#     A NEW cross-artifact gate machine-ties the drive status decisive rows
#     to the CO manifest win roster: for every target the CO
#     unadopted_win_rows nodes must equal the decisive-log PASS nodes.
# Verdicts are NOT consumed anywhere; the eight targets stay honest labels.
# The standard 11x11 empty board, the central-reply roots, class 5343 and
# every batch-28 key remain UNKNOWN.
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")
VG = os.path.join(ROOT, "val-gate")

# -- published source pins (batch-28 drive-4/drive-5 experiments + b28-win46
#    third-impl queue registry + Part CO 7-LOSS and Part DB 37-LOSS adoption
#    publications)
PIN_B28 = "af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5"
PIN_STATUS_D4 = "598174447fa878c2e0a6d6db6f892c5c279063174d763746456476e3051633f8"
PIN_STATUS_D5 = "ca1e98ccd952b29e8295147add50e6b4a3ff3732748bf544b9c3a7018d495df0"
PIN_QREG_JSON = "8c4216c68366c6a63e426ee36234b68955ef6f3a873429b0baa207f6dfc66592"
PIN_QREG_README = "00d1062ec195362575dcfa19289b5b49d690dbc48cf808af39fac5abf91ba213"
PIN_RAW_DE = {
    "aa012.p1": "5de8cab7c5aab351891fc54ec502db20b04c4aabcf2cc4e943595835270419af",
    "aa012.p2": "298c3e4554a5cdeea778d5607e6bc7de897bd15831ec6613477364ca351f6f85",
    "aa016.p1": "944d0283d65dd0da83a935e334bd84d0648d03e23a60a22a187989295348a46e",
    "aa016.p2": "15a3aed9e5472cadd0c68b6e83ae2745708308110971cdbece890ff2879874f3",
    "aa025.p1": "bcb1255792373b1a7c6bc6320b72d10d09b297be85db7f9ecbd71d3bcc1e3644",
    "aa025.p2": "b13e30bbfd12ee629e03a33876c8f00d844a94a564daae4a4f833154a6c40086",
    "aa027.p1": "82c83500334ab8e8417a499da181f75735b4e32b4d556ec1796fef0a3a1e98ff",
    "aa027.p2": "b4ca598493e901d84f7a02037bd38625cc9034a094c5c6017eb8aa37687b860e",
    "aa033.p1": "6c17ed481989b4059131e06c8e1a477d5619a14b986aa73346e5e081d2bd29c9",
    "aa033.p2": "6c17ed481989b4059131e06c8e1a477d5619a14b986aa73346e5e081d2bd29c9",
    "aa038.p1": "af554be977777d080160f70eb0234f4036c4aceb204a99a1349e16f5413d6e6e",
    "aa038.p2": "be48f875fb572fd6976a80754932226e1e5da08bb8435c19544754c296f561d6",
    "aa042.p1": "539da11ffe1d9c604d04d63795bf18960742fdf958a28679e5dcdf681fef97a5",
    "aa042.p2": "539da11ffe1d9c604d04d63795bf18960742fdf958a28679e5dcdf681fef97a5",
    "aa046.p1": "002812fb2b2583b134516cc69745d67df0ac9b24604b3c4fe0d5d0ec5d13ec2b",
    "aa046.p2": "f9787a6bb4171e56d54e0bcee8314d37e43edc60ee6ac4ec85db9617b154c445",
}
PIN_PUB_INPUT = {
    "aa012": "d8cd78cdc862d4ec457e91f1aaf326531b9cf61c452add560d9bfff7be43b726",
    "aa016": "68072c7d2b507f72954af956259d4e6d14c3b3feedb77fb387784b2f6a0ecc29",
    "aa025": "11c9a01163d35988932e3be00a21d7aeeccf969578342d14c20dcc6c0b66b852",
    "aa027": "b68b0ac1b5d13e179df1a2e62c068ea13b72e0f73f038eb3349b53faa9aa630a",
    "aa033": "8860218159a8ceac864116dc42102cd4ca3daebf264417567929eeffa25336df",
    "aa038": "d5f15306ae23194a88f891a3035b3bc8342b84b1c3cff47da970c8c8ce66401b",
    "aa042": "e77a08575667ecb8b2f80c50cc8f4acf391f39215ad4a7d9932f912e78e246be",
    "aa046": "89d805819157c3c3fef2c63feea2440c15d8531b62a4f728a7173dde307c9bdb",
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
# Part CO 7-LOSS adoption publications (batch-28 roster source)
PIN_MERGED_CANONICAL_CO = "854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d"
PIN_INCREMENT_CO = "bd5ef7d7632816006bd5a74349bf703a8dd3251e3a550a33e7ae7a0253abe382"
PIN_INCR_MANIFEST_CO = "b47e07ca90b0166d22c681a3136a60500d7a4f8671b1e77b656a1b34c7c02192"
# Part DB batch-29 37-LOSS adoption publications (current canonical chain head)
PIN_MERGED_CANONICAL_DB = "04b0a23987a97518e276ea5ff966496facab22f93628cd5fbc682a04c3650556"
PIN_INCREMENT_DB = "85bd44693edfd862a7cf74fc10414978fcf248dcef684a821b487f9757b443cc"
PIN_INCR_MANIFEST_DB = "1b51f30dabed6f4df435a3a034e1b5b9c2f405c75ebdcd918c0e256f2812d25a"
PIN_MERGER = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
PIN_MERGED_BASE_CU = "30ddad9dc0add7e21698e864b5c202b8e6ebd3e396c4eb6156a85ff2d34005c4"

TARGETS = ["aa046", "aa016", "aa025", "aa033", "aa027", "aa038", "aa012", "aa042"]
DECISIVE_LOG = {"aa046": 5, "aa016": 4, "aa025": 4, "aa033": 5,
                "aa027": 4, "aa038": 5, "aa012": 4, "aa042": 5}
EXPECT_S5 = {"aa046": 199731, "aa016": 167491, "aa025": 198223, "aa033": 199718,
             "aa027": 199712, "aa038": 199723, "aa012": 151960, "aa042": 199727}
EXPECT_MEMBERSHIP = {"aa046": 3, "aa016": 3, "aa025": 3, "aa033": 3,
                    "aa027": 3, "aa038": 4, "aa012": 4, "aa042": 3}
EXPECT_RESULT = {k: 1 for k in TARGETS}
EXPECT_REPLICA = {"aa046": 2185149, "aa016": 2621847, "aa025": 3056950, "aa033": 3347117,
                  "aa027": 4860191, "aa038": 4911996, "aa012": 4994213, "aa042": 5800791}
DECISIVE_PASS_LINE = {
    "aa046": "2026-11-23T19:08:58Z aa046 PASS 15000000,1,2185149",
    "aa016": "2026-11-23T17:51:36Z aa016 PASS 15000000,1,2621847",
    "aa025": "2026-11-23T18:03:12Z aa025 PASS 15000000,1,3056950",
    "aa033": "2026-11-23T18:42:44Z aa033 PASS 15000000,1,3347117",
    "aa027": "2026-11-23T18:05:12Z aa027 PASS 15000000,1,4860191",
    "aa038": "2026-11-23T18:56:36Z aa038 PASS 15000000,1,4911996",
    "aa012": "2026-11-23T17:47:44Z aa012 PASS 15000000,1,4994213",
    "aa042": "2026-11-23T19:03:09Z aa042 PASS 15000000,1,5800791",
}
DECISIVE_HALT_LINE = {
    "aa046": "2026-11-23T19:08:58Z aa046 WIN-HALT",
    "aa016": "2026-11-23T17:51:36Z aa016 WIN-HALT",
    "aa025": "2026-11-23T18:03:12Z aa025 WIN-HALT",
    "aa033": "2026-11-23T18:42:44Z aa033 WIN-HALT",
    "aa027": "2026-11-23T18:05:12Z aa027 WIN-HALT",
    "aa038": "2026-11-23T18:56:36Z aa038 WIN-HALT",
    "aa012": "2026-11-23T17:47:44Z aa012 WIN-HALT",
    "aa042": "2026-11-23T19:03:09Z aa042 WIN-HALT",
}
DRIVE_BUDGET = 15000000
# drive-4 status.log battery: 61 lines = 31 PASS + 18 WIN-HALT +
# 6 EXHAUSTED + 1 P1-TRUNCATED-RETRY + 5 P2-TRUNCATED-RETRY; no FAIL /
# MISMATCH / LOSS-HALT / junk.
D4_LINES, D4_PASS, D4_WINHALT, D4_EXH = 61, 31, 18, 6
D4_P1RETRY, D4_P2RETRY = 1, 5
# drive-5 status.log battery: 109 lines = 54 PASS + 35 WIN-HALT +
# 11 EXHAUSTED + 1 P1-TRUNCATED-RETRY + 7 P2-TRUNCATED-RETRY + 1 known junk
# line "P1-FAIL " (empty-key invocation artifact, non-verdict, Part CN
# honest record; excluded from verdict parsing).
D5_LINES, D5_PASS, D5_WINHALT, D5_EXH = 109, 54, 35, 11
D5_P1RETRY, D5_P2RETRY, D5_JUNK = 1, 7, 1
JUNK_LINE_D5 = "P1-FAIL "
# queue-registry battery values (published bookkeeping)
QREG_WIN_TOTAL, QREG_DONE, QREG_CLAIMED, QREG_OPEN = 46, 8, 5, 33
QREG_P1_TOTAL = 31778254
QREG_EST_TOTAL = 74996681

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
    if f1[2] != "5" or f1[4] != "0" or f1[5] != str(DRIVE_BUDGET):
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
        sys.exit(f"ABORT {key}: Part DE targets are the 15M-solved WIN rows, got result={result}")
    if nodes >= DRIVE_BUDGET:
        sys.exit(f"ABORT {key}: in-budget expected, nodes={nodes}")
    if nodes != EXPECT_REPLICA[key]:
        sys.exit(f"ABORT {key}: replica nodes {nodes} != published {EXPECT_REPLICA[key]}")
    return {"key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "replica_result": result, "replica_nodes": nodes}

def main():
    os.makedirs(OUT, exist_ok=True)
    # -- source pins
    for fname, pin in (("batch-keys-b28.json", PIN_B28), ("status-drive4.log", PIN_STATUS_D4),
                        ("status-drive5.log", PIN_STATUS_D5), ("queue-registry.json", PIN_QREG_JSON),
                        ("README-queue.md", PIN_QREG_README),
                        ("canonical-cache-co-merged-b28loss7.cache", PIN_MERGED_CANONICAL_CO),
                        ("increment-b28loss7.cache", PIN_INCREMENT_CO),
                        ("increments-manifest-co.json", PIN_INCR_MANIFEST_CO),
                        ("canonical-cache-db-merged-b29loss37.cache", PIN_MERGED_CANONICAL_DB),
                        ("increment-b29loss37.cache", PIN_INCREMENT_DB),
                        ("increments-manifest-db.json", PIN_INCR_MANIFEST_DB)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    for k, pin in PIN_RAW_DE.items():
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
    if int(bk28.get("budget", -1)) != DRIVE_BUDGET:
        sys.exit(f"ABORT batch-keys budget {bk28.get('budget')}")
    k28 = {k["key_id"]: k for k in bk28["keys"]}
    if len(k28) != 54:
        sys.exit(f"ABORT batch keys count {len(k28)} != 54")
    for t in TARGETS:
        if t not in k28:
            sys.exit(f"ABORT batch-keys lacks target {t}")
        if not re.fullmatch(r"aa[0-9]{3}", t):
            sys.exit(f"ABORT batch-28 key id form {t}")
    # -- drive-4/drive-5 status log battery (published batch-28 drive runner
    #    logs; pinned line counts / kind counts / target decisive rows)
    def status_battery(logname, nlines, npass, nwin, nexh, np1r, np2r):
        lines = [l for l in open(os.path.join(SRC, logname)).read().splitlines() if l.strip()]
        if len(lines) != nlines:
            sys.exit(f"ABORT {logname} line count {len(lines)} != {nlines}")
        kinds = {}
        junk = 0
        for ln in lines:
            toks = ln.split()
            kind = toks[2] if len(toks) >= 3 else (ln.rstrip() if toks[0].endswith("FAIL") else "")
            if kind == JUNK_LINE_D5.strip() and toks[0] == JUNK_LINE_D5.strip():
                junk += 1
                continue
            if len(toks) < 3:
                sys.exit(f"ABORT {logname} malformed line {ln!r}")
            kinds[kind] = kinds.get(kind, 0) + 1
        for k, v in (("PASS", npass), ("WIN-HALT", nwin), ("EXHAUSTED", nexh),
                     ("P1-TRUNCATED-RETRY", np1r), ("P2-TRUNCATED-RETRY", np2r)):
            if kinds.get(k) != v:
                sys.exit(f"ABORT {logname} {k} lines {kinds.get(k)} != {v}")
        for bad_kind in ("FAIL", "MISMATCH", "LOSS-HALT"):
            if bad_kind in kinds:
                sys.exit(f"ABORT {logname} carries unexpected line kind {bad_kind}")
        if sorted(kinds) != ["EXHAUSTED", "P1-TRUNCATED-RETRY", "P2-TRUNCATED-RETRY", "PASS", "WIN-HALT"]:
            sys.exit(f"ABORT {logname} carries line kinds other than the pinned set: {sorted(kinds)}")
        return lines
    d4 = status_battery("status-drive4.log", D4_LINES, D4_PASS, D4_WINHALT, D4_EXH, D4_P1RETRY, D4_P2RETRY)
    d5 = status_battery("status-drive5.log", D5_LINES, D5_PASS, D5_WINHALT, D5_EXH, D5_P1RETRY, D5_P2RETRY)
    if sum(1 for l in d5 if l == JUNK_LINE_D5) != D5_JUNK:
        sys.exit(f"ABORT status-drive5.log junk line count != {D5_JUNK}")
    by_log = {4: d4, 5: d5}
    for t in TARGETS:
        n = DECISIVE_LOG[t]
        lines = by_log[n]
        exact = [l for l in lines if l == DECISIVE_PASS_LINE[t]]
        if len(exact) != 1:
            sys.exit(f"ABORT decisive PASS line for {t} in drive-{n} log: {len(exact)} occurrences")
        halt = DECISIVE_HALT_LINE[t]
        if sum(1 for l in lines if l == halt) != 1:
            sys.exit(f"ABORT WIN-HALT line for {t} missing/non-unique in drive-{n} log")
        for l in lines:
            if l.split()[1] if len(l.split()) > 1 else "" == t:
                pass
        other_rows = [l for l in lines if len(l.split()) > 1 and l.split()[1] == t
                      and not (l == DECISIVE_PASS_LINE[t] or l == halt)]
        for l in other_rows:
            k = l.split()[2]
            if k in ("EXHAUSTED", "LOSS-HALT", "MISMATCH", "FAIL") or k.endswith("TRUNCATED-RETRY"):
                sys.exit(f"ABORT drive-{n} log carries a non-decisive row for target {t}: {l!r}")
        # cross-log identical-byte gate: aa012/aa016/aa025/aa027 decisive rows
        # are byte-identical in BOTH drive logs
        if t in ("aa012", "aa016", "aa025", "aa027"):
            if DECISIVE_PASS_LINE[t] not in by_log[5] or halt not in by_log[5]:
                sys.exit(f"ABORT {t}: decisive rows expected byte-identical in both drive logs")
    # -- queue-registry battery (published bookkeeping artifact)
    qreg = json.load(open(os.path.join(SRC, "queue-registry.json")))
    if qreg.get("schema") != "n11-centralreply-class5343-b28-thirdimpl-queue-registry-v1":
        sys.exit(f"ABORT queue-registry schema {qreg.get('schema')}")
    qsc = qreg["views"]["queue_state_counts"]
    if (qsc.get("win_total") != QREG_WIN_TOTAL or qsc.get("thirdimpl_done_win") != QREG_DONE
            or qsc.get("thirdimpl_claimed_win") != QREG_CLAIMED or qsc.get("thirdimpl_open_win") != QREG_OPEN):
        sys.exit(f"ABORT queue-registry state counts {qsc}")
    p1 = qreg["views"]["packages"]["P1"]
    if p1.get("keys") != TARGETS or int(p1.get("n_keys")) != 8:
        sys.exit(f"ABORT queue-registry P1 package keys {p1.get('keys')}")
    if int(p1.get("pinned_nodes_total")) != QREG_P1_TOTAL or int(p1.get("est_crossimpl_2pass_total")) != QREG_EST_TOTAL:
        sys.exit(f"ABORT queue-registry P1 package totals {p1.get('pinned_nodes_total')}")
    qrows = {r["key_id"]: r for r in qreg["rows"]}
    for t in TARGETS:
        r = qrows[t]
        if r.get("pinned_honest_label") != "WIN":
            sys.exit(f"ABORT queue-registry {t} label {r.get('pinned_honest_label')}")
        if r["thirdimpl"].get("state") != "open":
            sys.exit(f"ABORT queue-registry {t} thirdimpl state {r['thirdimpl']}")
        d = r["decisive"]
        if int(d.get("budget")) != DRIVE_BUDGET or int(d.get("rc")) != 1 or int(d.get("nodes")) != EXPECT_REPLICA[t]:
            sys.exit(f"ABORT queue-registry {t} decisive row {d}")
    qrd = open(os.path.join(SRC, "README-queue.md")).read()
    for phrase in ("**P1** (8\u884c): aa046, aa016, aa025, aa033, aa027, aa038, aa012, aa042",
                   "pinned\u8a08 31,778,254 nodes",
                   "verdict\u4e0d\u6d88\u8cbb",
                   "\u672cregistry\u306f\u3069\u306epackage\u3082\u4e88\u7d04\u3057\u306a\u3044",
                   "\u6a19\u6e9611\u00d711\u7a7a\u76e4\u30fb19 central-reply roots",
                   "UNKNOWN"):
        if phrase not in qrd:
            sys.exit(f"ABORT README-queue.md lacks phrase: {phrase!r}")
    rd_nospace = re.sub(r"\s+", "", qrd)
    if "\u9589\u9396\u30fb\u88ab\u8986\u30fbsecured\u30fbroot\u52dd\u6557\u306e\u4e3b\u5f35\u3092\u4e00\u5207\u542b\u307e\u306a\u3044" not in rd_nospace:
        sys.exit("ABORT README-queue.md lacks the no-claims guard")
    # -- per-target raw cross-verification
    rows = []
    for key in TARGETS:
        bk = k28.get(key)
        if bk is None or int(bk["s5_index"]) != EXPECT_S5[key]:
            sys.exit(f"ABORT {key}: batch-28 s5_index {bk and bk.get('s5_index')}")
        if int(bk["membership_class_count"]) != EXPECT_MEMBERSHIP[key]:
            sys.exit(f"ABORT {key}: membership_class_count {bk.get('membership_class_count')}")
        r = parse_raw(key, k28)
        r["source"] = f"batch-28-drive{DECISIVE_LOG[key]}-15m"
        r["s5_index"] = int(bk["s5_index"])
        r["membership_class_count"] = int(bk["membership_class_count"])
        r["expect_third"] = EXPECT_RESULT[key]
        rows.append(r)
    # -- unadopted-row corroboration battery, Part DB current-head machine
    #    gates first: NO s5verdict row for any target in EITHER the CO cache
    #    (6,301 rows) or the DB cache (6,354 rows -- the current canonical
    #    chain head; verdicts never consumed)
    for cache_file, pin, nrows in (("canonical-cache-co-merged-b28loss7.cache", PIN_MERGED_CANONICAL_CO, 6301),
                                   ("canonical-cache-db-merged-b29loss37.cache", PIN_MERGED_CANONICAL_DB, 6354)):
        merged = open(os.path.join(SRC, cache_file)).read().splitlines()
        s5rows = [l for l in merged if l.startswith("s5verdict,")]
        if len(s5rows) != nrows:
            sys.exit(f"ABORT {cache_file} s5verdict rows {len(s5rows)} != {nrows}")
        for r in rows:
            row_would_be = f"s5verdict,{r['lo']},{r['hi']},5,{r['replica_result']},{r['replica_nodes']}"
            hits = [l for l in s5rows if l == row_would_be]
            if hits:
                sys.exit(f"ABORT {cache_file}: {r['key_id']} row unexpectedly present: {hits}")
            other_key = [l for l in s5rows if l.startswith(f"s5verdict,{r['lo']},{r['hi']},")]
            if other_key:
                sys.exit(f"ABORT {cache_file}: carries a conflicting row for {r['key_id']}: {other_key}")
    # CO increment battery (the exact 7 adopted batch-28 LOSS rows)
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
    # DB increment battery (37 batch-29 LOSS rows; batch-28 targets absent)
    incdb = open(os.path.join(SRC, "increment-b29loss37.cache")).read().splitlines()
    incdb_rows = [l for l in incdb if l.startswith("s5verdict,")]
    if len(incdb_rows) != 37:
        sys.exit(f"ABORT DB increment rows {len(incdb_rows)} != 37")
    for r in rows:
        if any(l.startswith(f"s5verdict,{r['lo']},{r['hi']},") for l in incdb_rows):
            sys.exit(f"ABORT {r['key_id']}: unexpectedly present in the Part DB increment")
    # CO increments-manifest battery (batch-28 roster source)
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
    if im.get("sha256", {}).get("loss") != PIN_INCREMENT_CO:
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
    # DECLARED batch-28 DE adaptation of the id-list gates: the eight DE
    # targets were 15M-solved WIN rows at CO time, so they legitimately
    # appear in the win roster lists and member bookkeeping; they must be
    # absent from every ADOPTED/loss/fragment list and from the CO-time
    # exhausted_excluded_ids roster (11 rows).
    forbidden_ids = set()
    for fld in ("loss_ids",):
        forbidden_ids |= set(im.get(fld) or [])
    for bb in im.get("batches", []):
        for fld in ("adopted_loss_ids", "already_adopted_ids", "fragment_ids"):
            forbidden_ids |= set(bb.get(fld) or [])
    exhausted_roster = set(im.get("exhausted_excluded_ids") or []) | set(b.get("exhausted_excluded_ids") or [])
    win_roster = set(im.get("win_ids") or []) | set(im.get("unadopted_win_ids") or []) | set(b.get("unadopted_win_ids") or [])
    uwr_rows = {u.get("key_id"): u for u in (im.get("unadopted_win_rows") or []) if isinstance(u, dict)}
    member_ids = set(im.get("resolved_ids") or []) | set(b.get("probed_ids") or [])
    if len(exhausted_roster) != 11:
        sys.exit(f"ABORT CO exhausted roster size {len(exhausted_roster)}")
    if len(win_roster) != 35:
        sys.exit(f"ABORT CO win roster size {len(win_roster)}")
    for t in TARGETS:
        if t in forbidden_ids:
            sys.exit(f"ABORT {t}: target id appears in an adopted/loss/fragment list of the Part CO increments-manifest")
        if t in exhausted_roster:
            sys.exit(f"ABORT {t}: target id appears in exhausted_excluded_ids (CO-time), expected 15M-solved WIN")
        if t not in win_roster:
            sys.exit(f"ABORT {t}: target id missing from the CO win roster (unadopted_win_ids)")
        if t not in member_ids:
            sys.exit(f"ABORT {t}: target id missing from CO member bookkeeping (probed_ids/resolved_ids)")
        u = uwr_rows.get(t)
        if u is None:
            sys.exit(f"ABORT {t}: target id missing from unadopted_win_rows")
        if int(u.get("result")) != 1 or int(u.get("nodes")) != EXPECT_REPLICA[t] or u.get("two_pass_node_exact") is not True:
            sys.exit(f"ABORT {t}: unadopted_win_rows entry {u}")
    if sorted(set(uwr_rows) & set(TARGETS)) != sorted(TARGETS):
        sys.exit("ABORT unadopted_win_rows coverage of targets")
    # Part DB increments-manifest battery (current canonical chain head)
    imd = json.load(open(os.path.join(SRC, "increments-manifest-db.json")))
    if imd.get("schema") != "b29loss37-increments-manifest-v1":
        sys.exit(f"ABORT DB increments-manifest schema {imd.get('schema')}")
    if len(imd.get("loss_ids") or []) != 37 or not all(str(x).startswith("ab") for x in imd.get("loss_ids") or []):
        sys.exit(f"ABORT DB increments-manifest loss_ids {imd.get('loss_ids')[:3]}...")
    if imd.get("base_cache_sha256") != PIN_MERGED_BASE_CU or int(imd.get("base_cache_rows")) != 6317:
        sys.exit(f"ABORT DB increments-manifest base cache {imd.get('base_cache_sha256')},{imd.get('base_cache_rows')}")
    db_text = open(os.path.join(SRC, "increments-manifest-db.json")).read()
    for t in TARGETS:
        if t in db_text:
            sys.exit(f"ABORT {t}: target id appears anywhere in the batch-29-scoped DB manifest")
    # NEW cross-artifact consistency gates (declared): the CO manifest
    # unadopted_win_rows nodes for the targets MUST equal the drive
    # decisive-log PASS nodes (machine-ties the CO-time win roster to the
    # published drive rows), and the queue-registry pinned nodes must equal
    # both.
    for t in TARGETS:
        u = uwr_rows[t]
        if int(u["nodes"]) != EXPECT_REPLICA[t]:
            sys.exit(f"ABORT {t}: CO unadopted win nodes {u['nodes']} != drive decisive nodes {EXPECT_REPLICA[t]}")
        if int(qrows[t]["decisive"]["nodes"]) != EXPECT_REPLICA[t]:
            sys.exit(f"ABORT {t}: queue-registry decisive nodes != drive decisive nodes")
    if sum(EXPECT_REPLICA.values()) != QREG_P1_TOTAL:
        sys.exit("ABORT P1 pinned-nodes total mismatch vs queue registry")
    # -- anchors/negatives (published constants, AR->BF->BK->BM->BS->BV->BW->BX->BY->CC->CL->CM->CR->CW->CX provenance chain)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b28p1win8-thirdimpl-input-v1",
                 "sources": {
                     "b28p1win": ("sources/raw aa046/aa016/aa025/aa033/aa027/aa038/aa012/aa042 p1+p2 "
                                  "+ sources/status-drive4.log + sources/status-drive5.log + batch-keys-b28.json "
                                  "+ published batch-28 drive-4/drive-5 15M-probe canonical outputs (experiments "
                                  "n11-centralreply-closure-class5343-batch28-drive{4,5}-20261123), commit-pinned "
                                  "raw fetch; batch-keys sha256 af19208f..; the eight targets are the P1 package "
                                  "15M-solved WIN rows of the b28-win46 thirdimpl queue registry (budget 15000000)"),
                     "queue_registry": ("published bookkeeping registry (experiment "
                                        "n11-centralreply-class5343-b28win46-thirdimpl-queue-registry-20261124): "
                                        "queue-registry.json 8c4216c6.. + README 00d1062e..; P1 package keys and "
                                        "pinned nodes machine-gated by this maker; the registry reserves NO "
                                        "package -- this Part is the single-owner publish-then-execute declaration"),
                     "b28_batch_keys_sha256": PIN_B28,
                     "b28_status_drive4_sha256": PIN_STATUS_D4,
                     "b28_status_drive5_sha256": PIN_STATUS_D5,
                     "unadopted": ("published Part DB batch-29 37-LOSS adoption re-audit (experiment "
                                   "n11-centralreply-class2251-loss37-adoption-reaudit-20261124): merged canonical "
                                   "cache sha256 04b0a239.. (6,354 rows = CU 6,317 30ddad9d.. + 37 batch-29 LOSS "
                                   "rows) is the CURRENT canonical chain head and carries NO row for the eight "
                                   "targets (machine-gated both by this maker and by audit_de.py G6); the Part CO "
                                   "merged cache 854800f3.. (6,301 rows) likewise; increment b29loss37 85bd4469.., "
                                   "increments-manifest-db 1b51f30d..; DECLARED batch-28 DE adaptation: the eight "
                                   "targets are 15M-solved WIN rows at CO time, so they legitimately appear in "
                                   "the Part CO manifest win roster (win_ids/unadopted_win_ids/unadopted_win_rows "
                                   "node-exact) and member bookkeeping (probed_ids/resolved_ids), and must NOT "
                                   "appear in exhausted_excluded_ids or any adopted/loss/fragment list, nor "
                                   "anywhere in the batch-29-scoped DB manifest; they are UNADOPTED honest labels "
                                   "pending the scrutiny owner C++ second-implementation gate 9193f5b6 unchanged"),
                     "anchors": ("published Part G/K/O/P/T/W/AA/AD/AG/AL/AR/AX/AZ/BF/BK/BM/BS/BV/BW/BX/BY/CC/CL/CM/CR/CW/CX "
                                 "anchor/negative values, input CSVs byte-equality-checked against the published "
                                 "Part BF experiment (provenance chain AR -> BF -> BK -> BM -> BS -> BV -> BW -> "
                                 "BX -> BY -> CC -> CL -> CM -> CR -> CW -> CX)")},
                 "consumed_into_canonical_cache": False,
                 "unadopted_win_rows": True,
                 "unadopted_loss_rows": False,
                 "canonical_cache_sha256_unchanged": PIN_MERGED_CANONICAL_DB,
                 "canonical_cache_sha256_unchanged_co": PIN_MERGED_CANONICAL_CO,
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
    print("DE-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"], "src", r["source"])
    print("unadopted rows: absent from CO and DB merged canonical caches + both increments + every adopted/loss/fragment list (machine-gated)")
    print("win roster: targets node-exact in CO unadopted_win_rows; drive decisive rows == CO win rows == queue-registry rows (machine-gated)")

if __name__ == "__main__":
    main()
