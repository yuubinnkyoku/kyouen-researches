# make_inputs_dh.py -- machine-derive the Part DH third-impl input CSVs and
# rows.json for the NINE published batch-28 (closure class 5343) WIN rows of
# the P4 package of the b28-win46 third-impl queue registry:
# aa011 (key 1171516445255796736,0, legal 90, nodes 12,424,953, decisive
# drive4-15m, cross-log both drive logs) / aa054 (1152921504606863360,4228,
# legal 95, nodes 13,227,570, drive5) / aa022 (1171516479615533056,0, legal
# 87, nodes 14,044,375, drive4-15m, cross-log both drive logs) / aa034
# (1152921504606846977,4228, legal 94, nodes 14,097,048, drive5) / aa037
# (1152921504606846980,4228, legal 87, nodes 14,239,714, drive5) / aa032
# (1171516445255794688,4, legal 91, nodes 20,312,294, cs-25m) / aa028
# (1152921504606879744,4228, legal 95, nodes 21,563,925, cs-25m) / aa021
# (1171516462435663872,0, legal 90, nodes 22,942,323, cs-25m) / aa050
# (1152921504640401408,4228, legal 94, nodes 25,541,199, ct-30m) -- all
# UNCONSUMED honest labels, from the published canonical artifacts (zero
# hand transcription). Fail-closed: any unexpected field aborts.
#
# Byte-descended from the published Part DG maker (make_inputs_dg.py,
# sha256 d3fefbcae37de53700f9e58a08f95890c0267760ec0a211d1940ab1f01fcf917,
# experiment n11-centralreply-closure-b28p3win8-thirdimpl-20261124, itself a
# DE-maker adaptation after the P2-pre-emption pivot). Declared deltas vs
# the DG machine (all declared in the Part DH declaration before execution):
# (a) targets: the NINE P4-package rows (est ascending), with PER-KEY
#     decisive probe budgets (aa011/aa054/aa022/aa034/aa037 = 15,000,000 as
#     in DG; aa032/aa028/aa021 = 25,000,000 from the cs-25m reprobe;
#     aa050 = 30,000,000 from the ct-30m reprobe). The batch-28 batch-keys
#     file keeps its own base probe budget metadata 15,000,000 (declared
#     unchanged gate). New status-log batteries pin the reprobe runner logs:
#     status-cs25m.log cea47a0c... (12 lines: PASS 6 / WIN-HALT 4 /
#     EXHAUSTED 1 / P2-TRUNCATED-RETRY 1) and status-ct30m.log efd18b3c...
#     (6 lines: PASS 3 / WIN-HALT 2 / P2-TRUNCATED-RETRY 1), alongside the
#     unchanged drive4/drive5 batteries (DG-pinned line/kind counts);
# (b) per-target decisive log semantics: DECISIVE_LOG ids drive4-15m /
#     drive5-15m / cs-25m / ct-30m with exact pinned decisive PASS + WIN-HALT
#     lines (single occurrence each). Two HONEST-HISTORY allowances (declared,
#     fail-closed otherwise): a decisive log may carry P1/P2-TRUNCATED-RETRY
#     rows for its target (observed: aa034 P2-TRUNCATED-RETRY in drive5
#     18:49:33Z before the decisive PASS 18:52:04Z; aa050 in ct-30m) and the
#     reprobe-decisive keys carry CO-time 15M EXHAUSTED rows in the drive
#     logs (aa021/aa028 byte-identical in BOTH drive logs; aa032/aa050 in
#     drive5), machine-tied to the Part CO manifest exhausted_excluded_ids
#     roster (the CO-time honest label), and carrying containing-log rows in
#     registry observations. Cross-log identical-byte battery covers the TWO
#     drive-4-decisive rows aa011/aa022 (byte-identical in BOTH drive logs);
# (c) registry battery: rev3 pins unchanged (queue-registry.json 334f6209..
#     + README-queue 4b20c6a0..); state counts (win 46 / done 21 / claimed 0 /
#     open 25); P4 package roster (9 keys, pinned nodes total 158,393,401 =
#     sum of per-key pinned nodes, est crossimpl 2-pass total 373,808,426);
#     per-row: label WIN, thirdimpl state open, decisive log id, budget, rc 1,
#     node-exact vs EXPECT; win_by_resolution_tier totals {15m 35, 20m 7,
#     25m 3, 30m 1} == win_total 46; anchor-invariance ties: registry
#     anchor_invariance_checks aa004 (rc 1, nodes 15,616,012, budgets
#     20M/25M/30M) and aa036 (rc 2, nodes 955,659, budgets 15M/20M/25M/30M)
#     vs the pinned aa004/aa036 PASS rows in the cs-25m and ct-30m logs;
# (d) unadopted-corroboration: unchanged caches (Part DB head 04b0a239.. 6,354
#     rows; Part CO 854800f3.. 6,301 rows; increments + manifests byte-pinned
#     as in DG): all NINE targets carry NO s5verdict row in EITHER merged
#     cache, are absent from both increments and every adopted/loss/fragment
#     list and the entire batch-29 DB manifest text. CO-manifest split
#     (declared): the FIVE 15M-solved targets (aa011/aa054/aa022/aa034/aa037)
#     are the same DG-style win-roster rows (unadopted_win_rows node-exact,
#     two_pass_node_exact true, NOT in exhausted_excluded_ids); the FOUR
#     reprobe targets (aa032/aa028/aa021/aa050) are in exhausted_excluded_ids
#     (CO-time honest EXHAUSTED) and NOT in the CO win roster -- their WIN
#     label provenance is the reprobe publication + registry, and their
#     re-verification cross-ties are the status-cs25m/status-ct30m decisive
#     rows + raw p1/p2 + registry rows (three-way machine-tie);
# (e) anchors/negatives/val-gate: unchanged from DG (published constants,
#     provenance chain byte-clone).
# Verdicts are NOT consumed anywhere; the nine targets stay honest labels.
# The standard 11x11 empty board, the central-reply roots, class 5343 and
# every batch-28 key remain UNKNOWN.
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources")
OUT = os.path.join(ROOT, "input")
VG = os.path.join(ROOT, "val-gate")

# -- published source pins (batch-28 drive-4/drive-5 + reprobe25m/reprobe30m
#    experiments + b28-win46 third-impl queue registry + Part CO 7-LOSS and
#    Part DB 37-LOSS adoption publications)
PIN_B28 = "af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5"
PIN_STATUS_D4 = "598174447fa878c2e0a6d6db6f892c5c279063174d763746456476e3051633f8"
PIN_STATUS_D5 = "ca1e98ccd952b29e8295147add50e6b4a3ff3732748bf544b9c3a7018d495df0"
PIN_STATUS_CS25 = "cea47a0c887b0380ebb9604a11ad1bf7fab78a1c58e5e3a1b8e9c555b394524f"
PIN_STATUS_CT30 = "efd18b3c21a375864d11e740397d9d2aba833a9911cd287f881aa6df8c7f9865"
PIN_QREG_JSON = "334f6209d0628cdf8f5c997e92bc5e5e63ae7f450345dc1a8393488941f1f6e9"
PIN_QREG_README = "4b20c6a0f98b399dcbfd86386134cab9d1258a7dbcb1690387dcb2f46d1a793e"
PIN_RAW_DH = {
    "aa011.p1": "171d63813822c074ccfea28b55818191f789cb39b19fbeda0cb5125266ca01f0",
    "aa011.p2": "9864d2b0f3487ff7ee84587cbc0c46ea1642b57e261fd492fd4c274695dcfe7f",
    "aa022.p1": "5feb035316488b9ff9f353d11ab146d52832cafa99cc316480e86442f3b0afda",
    "aa022.p2": "da703e37eff3de00e9e19d0451eca25f278323bd634bb99b04fbc89456582a7c",
    "aa054.p1": "d79d24f7763df06dfed33ef24e92ae43830ef97ef035f8a623ff825a89a3b53c",
    "aa054.p2": "997a0aae3a886f9227eae99b671f212e05ba75a87212670bb3d18ee764208a17",
    "aa034.p1": "42580df2c86f7b602880d0fe453c8fb0af3c315e2cc989a1e3df6bf2fa2d82e9",
    "aa034.p2": "42580df2c86f7b602880d0fe453c8fb0af3c315e2cc989a1e3df6bf2fa2d82e9",
    "aa037.p1": "4defd77a37554eba0692cc2ff15cf363970fdfa830dfb29871296b58bed6a045",
    "aa037.p2": "5bc188380b8d89c0dc3ca304622d21264c24a0bccc130628cdc590e2f3f89712",
    "aa021.p1": "0082e9d0621fb96ab21ebf0965d7d9fc2289601490ebb908d53b0d34deb6ecec",
    "aa021.p2": "35a98fda2355d6c83317fd49573ecbac22cfd3329109605e40d63c5096607bb3",
    "aa028.p1": "d57f3c0715a9d585853a0010f73c6c4e9504f65c5b7b7c68ddc8799f8cdf4539",
    "aa028.p2": "c41b5ab452ce85aa827d04a8d4055369f965cae553632810f6e41b92be9d8b18",
    "aa032.p1": "85a787a9d814b0e1277498af3abc65450315125cc1d4c26d3c4ed349b4560dbf",
    "aa032.p2": "312271645e1014cc5eefbc685e1eb613600c1433f31bc73e373e7dc6a0651e61",
    "aa050.p1": "aada66cf31f2f99a04433d04c237cac3e3b22a02cd5a6514c75a440073d099c8",
    "aa050.p2": "aada66cf31f2f99a04433d04c237cac3e3b22a02cd5a6514c75a440073d099c8",
}
PIN_PUB_INPUT = {
    "aa011": "316329c5efc60178390c1dd1fb158fe2c3c2eb956e71b5e14f5ee713889a270c",
    "aa021": "de5d3baa15cbd044bf4515313aa7fc344930197b901632528fe0708acd9a1882",
    "aa022": "c7729d314c6f4418b4f261eb489a76df622a5eccbd4e7984ecdae2f47bf0dfdd",
    "aa028": "769a2fde51dbc59abfe94f7dfe3a5d72f9e2fdf94334c9f975dd652ba4d5b6da",
    "aa032": "2aa666fb3b87e4a3b8901f9ce5cae9a24fc3b078d72a693639239a632236f0fe",
    "aa034": "c18dc23256d8efc899e2e709f56f5b1b059eb5a03e76470e31bcc441e9267529",
    "aa037": "488d15c69cbcb83a61a1d712bb333d02a9f28e1578d005b0e80674e45dbf1938",
    "aa050": "cc5e405ab3ba311d7c477c8f960f1f7d1dc49ef3b37b027c2acd0c573d302787",
    "aa054": "36cb283f0aa82f379ebb119564f9cb342f24dbda70398cac3b9de6e2d04c13c5",
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

TARGETS = ["aa011", "aa054", "aa022", "aa034", "aa037", "aa032", "aa028", "aa021", "aa050"]
DECISIVE_LOG = {"aa011": "drive4-15m", "aa054": "drive5-15m", "aa022": "drive4-15m",
                "aa034": "drive5-15m", "aa037": "drive5-15m", "aa032": "cs-25m",
                "aa028": "cs-25m", "aa021": "cs-25m", "aa050": "ct-30m"}
EXPECT_BUDGET = {"aa011": 15000000, "aa054": 15000000, "aa022": 15000000,
                 "aa034": 15000000, "aa037": 15000000, "aa032": 25000000,
                 "aa028": 25000000, "aa021": 25000000, "aa050": 30000000}
EXPECT_S5 = {"aa011": 147632, "aa054": 199739, "aa022": 191399, "aa034": 199719,
             "aa037": 199722, "aa032": 199717, "aa028": 199713, "aa021": 188751,
             "aa050": 199735}
EXPECT_MEMBERSHIP = {k: 4 for k in TARGETS}
EXPECT_RESULT = {k: 1 for k in TARGETS}
EXPECT_REPLICA = {"aa011": 12424953, "aa054": 13227570, "aa022": 14044375,
                  "aa034": 14097048, "aa037": 14239714, "aa032": 20312294,
                  "aa028": 21563925, "aa021": 22942323, "aa050": 25541199}
DECISIVE_PASS_LINE = {
    "aa011": "2026-11-23T17:45:59Z aa011 PASS 15000000,1,12424953",
    "aa054": "2026-11-23T19:24:56Z aa054 PASS 15000000,1,13227570",
    "aa022": "2026-11-23T18:02:11Z aa022 PASS 15000000,1,14044375",
    "aa034": "2026-11-23T18:52:04Z aa034 PASS 15000000,1,14097048",
    "aa037": "2026-11-23T18:54:58Z aa037 PASS 15000000,1,14239714",
    "aa032": "2026-11-23T23:43:10Z aa032 PASS 25000000,1,20312294",
    "aa028": "2026-11-23T23:39:26Z aa028 PASS 25000000,1,21563925",
    "aa021": "2026-11-23T23:35:29Z aa021 PASS 25000000,1,22942323",
    "aa050": "2026-11-24T00:14:52Z aa050 PASS 30000000,1,25541199",
}
DECISIVE_HALT_LINE = {
    "aa011": "2026-11-23T17:45:59Z aa011 WIN-HALT",
    "aa054": "2026-11-23T19:24:56Z aa054 WIN-HALT",
    "aa022": "2026-11-23T18:02:11Z aa022 WIN-HALT",
    "aa034": "2026-11-23T18:52:04Z aa034 WIN-HALT",
    "aa037": "2026-11-23T18:54:58Z aa037 WIN-HALT",
    "aa032": "2026-11-23T23:43:10Z aa032 WIN-HALT",
    "aa028": "2026-11-23T23:39:26Z aa028 WIN-HALT",
    "aa021": "2026-11-23T23:35:29Z aa021 WIN-HALT",
    "aa050": "2026-11-24T00:14:52Z aa050 WIN-HALT",
}
# CO-time 15M EXHAUSTED rows of the four reprobe-decisive keys (honest history
# in the drive logs; machine-tied to the Part CO exhausted_excluded_ids roster)
CO_TIME_EXHAUSTED = {
    "aa021": ("2026-11-23T17:58:44Z aa021 PASS 15000000,0,15000000", "both"),
    "aa028": ("2026-11-23T18:10:46Z aa028 PASS 15000000,0,15000000", "both"),
    "aa032": ("2026-11-23T18:44:54Z aa032 PASS 15000000,0,15000000", "drive5"),
    "aa050": ("2026-11-23T19:18:31Z aa050 PASS 15000000,0,15000000", "drive5"),
}
# base probe budget (batch-28 batch-keys file metadata; unchanged DG gate)
BK_BUDGET = 15000000
# drive-4 status.log battery: 61 lines = 31 PASS + 18 WIN-HALT + 6 EXHAUSTED +
# 1 P1-TRUNCATED-RETRY + 5 P2-TRUNCATED-RETRY (unchanged DG pins)
D4_LINES, D4_PASS, D4_WINHALT, D4_EXH = 61, 31, 18, 6
D4_P1RETRY, D4_P2RETRY = 1, 5
# drive-5 status.log battery: 109 lines = 54 PASS + 35 WIN-HALT + 11 EXHAUSTED +
# 1 P1-TRUNCATED-RETRY + 7 P2-TRUNCATED-RETRY + 1 known junk line "P1-FAIL "
# (unchanged DG pins)
D5_LINES, D5_PASS, D5_WINHALT, D5_EXH = 109, 54, 35, 11
D5_P1RETRY, D5_P2RETRY, D5_JUNK = 1, 7, 1
JUNK_LINE_D5 = "P1-FAIL "
# cs-25m reprobe status.log battery: 12 lines = 6 PASS + 4 WIN-HALT +
# 1 EXHAUSTED + 1 P2-TRUNCATED-RETRY
CS_LINES, CS_PASS, CS_WINHALT, CS_EXH, CS_P2RETRY = 12, 6, 4, 1, 1
# ct-30m reprobe status.log battery: 6 lines = 3 PASS + 2 WIN-HALT +
# 1 P2-TRUNCATED-RETRY
CT_LINES, CT_PASS, CT_WINHALT, CT_P2RETRY = 6, 3, 2, 1
# anchor-invariance cross-tie rows pinned in BOTH reprobe logs (machine-ties
# the reprobe logs to the registry anchor_invariance_checks entries)
ANCHOR_INVARIANT_ROWS = [
    ("cs-25m", "2026-11-23T23:28:32Z aa036 PASS 25000000,2,955659"),
    ("cs-25m", "2026-11-23T23:31:19Z aa004 PASS 25000000,1,15616012"),
    ("ct-30m", "2026-11-24T00:05:11Z aa036 PASS 30000000,2,955659"),
    ("ct-30m", "2026-11-24T00:08:05Z aa004 PASS 30000000,1,15616012"),
]
# queue-registry battery values (published bookkeeping, rev3 unchanged)
QREG_WIN_TOTAL, QREG_DONE, QREG_CLAIMED, QREG_OPEN = 46, 21, 0, 25
QREG_P4_TOTAL = 158393401
QREG_EST_TOTAL = 373808426
QREG_TIER_15M, QREG_TIER_20M, QREG_TIER_25M, QREG_TIER_30M = 35, 7, 3, 1
# the five 15M-solved P4 rows (CO win-roster members node-exact)
TIER15_KEYS = ["aa011", "aa054", "aa022", "aa034", "aa037"]
# the four reprobe-decisive P4 rows (CO-time exhausted_excluded members)
REPROBE_KEYS = ["aa032", "aa028", "aa021", "aa050"]

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
    for i in (3, 5, 6, 7, 9, 10):
        if f1[i] != f2[i]:
            sys.exit(f"ABORT {key}: source raw passes differ at field {i}: {f1[i]} vs {f2[i]}")
    if f1[2] != "5" or f1[4] != "0" or f1[5] != str(EXPECT_BUDGET[key]):
        sys.exit(f"ABORT {key}: unexpected source schema {f1[:6]} (expected budget {EXPECT_BUDGET[key]})")
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
        sys.exit(f"ABORT {key}: Part DH targets are the published WIN rows, got result={result}")
    if nodes >= EXPECT_BUDGET[key]:
        sys.exit(f"ABORT {key}: in-budget expected, nodes={nodes}")
    if nodes != EXPECT_REPLICA[key]:
        sys.exit(f"ABORT {key}: replica nodes {nodes} != published {EXPECT_REPLICA[key]}")
    return {"key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "replica_result": result, "replica_nodes": nodes}

def main():
    os.makedirs(OUT, exist_ok=True)
    # -- source pins
    for fname, pin in (("batch-keys-b28.json", PIN_B28), ("status-drive4.log", PIN_STATUS_D4),
                        ("status-drive5.log", PIN_STATUS_D5), ("status-cs25m.log", PIN_STATUS_CS25),
                        ("status-ct30m.log", PIN_STATUS_CT30), ("queue-registry.json", PIN_QREG_JSON),
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
    for k, pin in PIN_RAW_DH.items():
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
    if int(bk28.get("budget", -1)) != BK_BUDGET:
        sys.exit(f"ABORT batch-keys budget {bk28.get('budget')} != base probe budget {BK_BUDGET}")
    k28 = {k["key_id"]: k for k in bk28["keys"]}
    if len(k28) != 54:
        sys.exit(f"ABORT batch keys count {len(k28)} != 54")
    for t in TARGETS:
        if t not in k28:
            sys.exit(f"ABORT batch-keys lacks target {t}")
        if not re.fullmatch(r"aa[0-9]{3}", t):
            sys.exit(f"ABORT batch-28 key id form {t}")
    # -- status log batteries (pinned line counts / exact kind-count dicts;
    #    fail-closed on any unexpected line kind)
    def status_battery(logname, nlines, expect, junk_allowed):
        lines = [l for l in open(os.path.join(SRC, logname)).read().splitlines() if l.strip()]
        if len(lines) != nlines:
            sys.exit(f"ABORT {logname} line count {len(lines)} != {nlines}")
        kinds = {}
        junk = 0
        for ln in lines:
            toks = ln.split()
            if len(toks) < 3:
                if junk_allowed and ln.rstrip() == JUNK_LINE_D5.strip():
                    junk += 1
                    continue
                sys.exit(f"ABORT {logname} malformed line {ln!r}")
            kinds[toks[2]] = kinds.get(toks[2], 0) + 1
        if junk and not junk_allowed:
            sys.exit(f"ABORT {logname} unexpected junk line form")
        if kinds != expect:
            sys.exit(f"ABORT {logname} kind counts {kinds} != pinned {expect}")
        return lines, junk
    d4, _ = status_battery("status-drive4.log", D4_LINES,
                           {"PASS": D4_PASS, "WIN-HALT": D4_WINHALT, "EXHAUSTED": D4_EXH,
                            "P1-TRUNCATED-RETRY": D4_P1RETRY, "P2-TRUNCATED-RETRY": D4_P2RETRY}, False)
    d5, d5_junk = status_battery("status-drive5.log", D5_LINES,
                                 {"PASS": D5_PASS, "WIN-HALT": D5_WINHALT, "EXHAUSTED": D5_EXH,
                                  "P1-TRUNCATED-RETRY": D5_P1RETRY, "P2-TRUNCATED-RETRY": D5_P2RETRY}, True)
    if d5_junk != D5_JUNK:
        sys.exit(f"ABORT status-drive5.log junk line count {d5_junk} != {D5_JUNK}")
    cs, _ = status_battery("status-cs25m.log", CS_LINES,
                           {"PASS": CS_PASS, "WIN-HALT": CS_WINHALT, "EXHAUSTED": CS_EXH,
                            "P2-TRUNCATED-RETRY": CS_P2RETRY}, False)
    ct, _ = status_battery("status-ct30m.log", CT_LINES,
                           {"PASS": CT_PASS, "WIN-HALT": CT_WINHALT,
                            "P2-TRUNCATED-RETRY": CT_P2RETRY}, False)
    by_log = {"drive4-15m": d4, "drive5-15m": d5, "cs-25m": cs, "ct-30m": ct}
    # -- per-target decisive rows (exact pinned lines; single occurrence;
    #    honest-history allowance: P1/P2-TRUNCATED-RETRY rows for the target
    #    in the decisive log, e.g. aa034 drive5 18:49:33Z / aa050 ct-30m)
    for t in TARGETS:
        logid = DECISIVE_LOG[t]
        lines = by_log[logid]
        exact = [l for l in lines if l == DECISIVE_PASS_LINE[t]]
        if len(exact) != 1:
            sys.exit(f"ABORT decisive PASS line for {t} in {logid} log: {len(exact)} occurrences")
        halt = DECISIVE_HALT_LINE[t]
        if sum(1 for l in lines if l == halt) != 1:
            sys.exit(f"ABORT WIN-HALT line for {t} missing/non-unique in {logid} log")
        other_rows = [l for l in lines if len(l.split()) > 1 and l.split()[1] == t
                      and not (l == DECISIVE_PASS_LINE[t] or l == halt)]
        for l in other_rows:
            k = l.split()[2]
            if k in ("EXHAUSTED", "LOSS-HALT", "MISMATCH", "FAIL"):
                sys.exit(f"ABORT {logid} log carries a non-decisive verdict row for target {t}: {l!r}")
            if not k.endswith("TRUNCATED-RETRY"):
                sys.exit(f"ABORT {logid} log carries an unexpected row kind for target {t}: {l!r}")
    # -- cross-log identical-byte battery: the TWO drive-4-decisive 15M rows
    #    aa011/aa022 are byte-identical in BOTH drive logs
    for t in ("aa011", "aa022"):
        if DECISIVE_PASS_LINE[t] not in d5 or DECISIVE_HALT_LINE[t] not in d5:
            sys.exit(f"ABORT {t}: decisive rows expected byte-identical in both drive logs")
    # -- CO-time 15M EXHAUSTED rows of the four reprobe-decisive keys
    #    (honest history in the drive logs; MUST also appear in the CO
    #    manifest exhausted_excluded_ids roster below)
    for t, (eline, where) in CO_TIME_EXHAUSTED.items():
        xline = eline.replace(" PASS ", " EXHAUSTED ", 1)
        for line, logs in ((eline, where), (xline, where)):
            if logs == "both":
                if line not in d4 or line not in d5:
                    sys.exit(f"ABORT {t}: CO-time row {line!r} expected byte-identical in both drive logs")
            elif logs == "drive5":
                if line not in d5:
                    sys.exit(f"ABORT {t}: CO-time row {line!r} missing from drive5 log")
            else:
                sys.exit(f"ABORT {t}: unknown containing-log spec {where!r}")
    # -- anchor-invariance cross-tie rows (registry vs reprobe logs)
    for logid, row in ANCHOR_INVARIANT_ROWS:
        if row not in by_log[logid]:
            sys.exit(f"ABORT anchor-invariance row missing from {logid} log: {row!r}")
    # -- queue-registry battery (published bookkeeping artifact, rev3 pinned)
    qreg = json.load(open(os.path.join(SRC, "queue-registry.json")))
    if qreg.get("schema") != "n11-centralreply-class5343-b28-thirdimpl-queue-registry-v1":
        sys.exit(f"ABORT queue-registry schema {qreg.get('schema')}")
    if int(qreg["revision"]["rev"]) != 3:
        sys.exit(f"ABORT queue-registry revision {qreg['revision'].get('rev')} != 3 (rev3 pinned)")
    qsc = qreg["views"]["queue_state_counts"]
    if (qsc.get("win_total") != QREG_WIN_TOTAL or qsc.get("thirdimpl_done_win") != QREG_DONE
            or qsc.get("thirdimpl_claimed_win") != QREG_CLAIMED or qsc.get("thirdimpl_open_win") != QREG_OPEN):
        sys.exit(f"ABORT queue-registry state counts {qsc}")
    p4 = qreg["views"]["packages"]["P4"]
    if p4.get("keys") != TARGETS or int(p4.get("n_keys")) != 9:
        sys.exit(f"ABORT queue-registry P4 package keys {p4.get('keys')}")
    if int(p4.get("pinned_nodes_total")) != QREG_P4_TOTAL or int(p4.get("est_crossimpl_2pass_total")) != QREG_EST_TOTAL:
        sys.exit(f"ABORT queue-registry P4 package totals {p4.get('pinned_nodes_total')} / {p4.get('est_crossimpl_2pass_total')}")
    if p4.get("status") is not None or "done_part" in p4:
        sys.exit("ABORT queue-registry P4 package unexpectedly claimed/done")
    tiers = qreg.get("accounting", {}).get("win_by_resolution_tier", {})
    if (int(tiers.get("15m", -1)) != QREG_TIER_15M or int(tiers.get("20m", -1)) != QREG_TIER_20M
            or int(tiers.get("25m", -1)) != QREG_TIER_25M or int(tiers.get("30m", -1)) != QREG_TIER_30M):
        sys.exit(f"ABORT queue-registry win_by_resolution_tier {tiers}")
    if QREG_TIER_15M + QREG_TIER_20M + QREG_TIER_25M + QREG_TIER_30M != QREG_WIN_TOTAL:
        sys.exit("ABORT tier totals do not sum to win_total")
    # anchor_invariance_checks tie (registry bookkeeping vs the reprobe logs)
    aic = {a.get("key_id"): a for a in qreg.get("accounting", {}).get("anchor_invariance_checks", [])}
    if int(aic.get("aa004", {}).get("decisive_nodes", -1)) != 15616012 or int(aic.get("aa004", {}).get("decisive_rc", -1)) != 1:
        sys.exit(f"ABORT registry anchor_invariance aa004 {aic.get('aa004')}")
    if int(aic.get("aa036", {}).get("decisive_nodes", -1)) != 955659 or int(aic.get("aa036", {}).get("decisive_rc", -1)) != 2:
        sys.exit(f"ABORT registry anchor_invariance aa036 {aic.get('aa036')}")
    if 25000000 not in aic.get("aa004", {}).get("node_exact_budgets", []) or 30000000 not in aic.get("aa004", {}).get("node_exact_budgets", []):
        sys.exit("ABORT registry aa004 budgets do not include the 25m/30m reprobes")
    if 25000000 not in aic.get("aa036", {}).get("node_exact_budgets", []) or 30000000 not in aic.get("aa036", {}).get("node_exact_budgets", []):
        sys.exit("ABORT registry aa036 budgets do not include the 25m/30m reprobes")
    qrows = {r["key_id"]: r for r in qreg["rows"]}
    for t in TARGETS:
        r = qrows[t]
        if r.get("pinned_honest_label") != "WIN":
            sys.exit(f"ABORT queue-registry {t} label {r.get('pinned_honest_label')}")
        if r["thirdimpl"].get("state") != "open":
            sys.exit(f"ABORT queue-registry {t} thirdimpl state {r['thirdimpl']}")
        d = r["decisive"]
        if d.get("log") != DECISIVE_LOG[t]:
            sys.exit(f"ABORT queue-registry {t} decisive log {d.get('log')} != {DECISIVE_LOG[t]}")
        if int(d.get("budget")) != EXPECT_BUDGET[t] or int(d.get("rc")) != 1 or int(d.get("nodes")) != EXPECT_REPLICA[t]:
            sys.exit(f"ABORT queue-registry {t} decisive row {d}")
    qrd = open(os.path.join(SRC, "README-queue.md")).read()
    for phrase in ("**P4** (9\u884c): aa011, aa054, aa022, aa034, aa037, aa032, aa028, aa021, aa050",
                   "pinned\u8a08 158,393,401 nodes",
                   "est\u8a08 \u2248 373,808,426 nodes",
                   "**rev3 (2026-11-24T05:15Z)**",
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
        r["source"] = f"batch-28-{DECISIVE_LOG[key]}"
        r["s5_index"] = int(bk["s5_index"])
        r["membership_class_count"] = int(bk["membership_class_count"])
        r["expect_third"] = EXPECT_RESULT[key]
        rows.append(r)
    # -- unadopted-row corroboration battery: NO s5verdict row for any target
    #    in EITHER the CO cache (6,301 rows) or the DB cache (6,354 rows --
    #    the current canonical chain head; verdicts never consumed)
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
    # DECLARED DH split of the id-list gates: the FIVE 15M-solved targets
    # (TIER15_KEYS) are CO win-roster rows node-exact (as in DE/DG); the FOUR
    # reprobe-decisive targets (REPROBE_KEYS) are CO-time exhausted_excluded
    # members (their later WIN labels come from the reprobe publications +
    # registry, machine-tied three-way by the status-cs25m/status-ct30m
    # decisive rows + raw p1/p2 + registry rows above).
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
        if t not in member_ids:
            sys.exit(f"ABORT {t}: target id missing from CO member bookkeeping (probed/resolved)")
    for t in TIER15_KEYS:
        if t in exhausted_roster:
            sys.exit(f"ABORT {t}: 15M-solved target id appears in exhausted_excluded_ids (CO-time), unexpected")
        if t not in win_roster:
            sys.exit(f"ABORT {t}: target id missing from the CO win roster (unadopted_win_ids)")
        u = uwr_rows.get(t)
        if u is None:
            sys.exit(f"ABORT {t}: target id missing from unadopted_win_rows")
        if int(u.get("result")) != 1 or int(u.get("nodes")) != EXPECT_REPLICA[t] or u.get("two_pass_node_exact") is not True:
            sys.exit(f"ABORT {t}: unadopted_win_rows entry {u}")
    for t in REPROBE_KEYS:
        if t not in exhausted_roster:
            sys.exit(f"ABORT {t}: reprobe-decisive target id missing from CO exhausted_excluded_ids (CO-time honest label)")
        if t in win_roster:
            sys.exit(f"ABORT {t}: reprobe-decisive target id appears in the CO win roster, unexpected")
        if t in uwr_rows:
            sys.exit(f"ABORT {t}: reprobe-decisive target id appears in unadopted_win_rows, unexpected")
    if sorted(set(uwr_rows) & set(TIER15_KEYS)) != sorted(TIER15_KEYS):
        sys.exit("ABORT unadopted_win_rows coverage of the five 15M targets")
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
    # NEW cross-artifact consistency gates (declared): for the FIVE 15M keys,
    # the CO manifest unadopted_win_rows nodes == drive decisive PASS nodes
    # == queue-registry pinned nodes; for the FOUR reprobe keys, the cs-25m /
    # ct-30m decisive PASS nodes == raw p1/p2 nodes == queue-registry pinned
    # nodes (and the CO-time exhausted rows are the pinned 15M drive rows).
    for t in TIER15_KEYS:
        u = uwr_rows[t]
        if int(u["nodes"]) != EXPECT_REPLICA[t]:
            sys.exit(f"ABORT {t}: CO unadopted win nodes {u['nodes']} != drive decisive nodes {EXPECT_REPLICA[t]}")
    for t in TARGETS:
        if int(qrows[t]["decisive"]["nodes"]) != EXPECT_REPLICA[t]:
            sys.exit(f"ABORT {t}: queue-registry decisive nodes != pinned nodes")
    if sum(EXPECT_REPLICA.values()) != QREG_P4_TOTAL:
        sys.exit("ABORT P4 pinned-nodes total mismatch vs queue registry")
    if sum(EXPECT_REPLICA[t] for t in TIER15_KEYS) != sum(uwr_rows[t]["nodes"] for t in TIER15_KEYS):
        sys.exit("ABORT 15M-tier CO win nodes sum mismatch")
    # -- anchors/negatives (published constants, AR->BF->BK->BM->BS->BV->BW->BX->BY->CC->CL->CM->CR->CW->CX->DE->DG provenance chain)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b28p4win9-thirdimpl-input-v1",
                 "sources": {
                     "b28p4win": ("sources/raw aa011/aa054/aa022/aa034/aa037/aa032/aa028/aa021/aa050 p1+p2 "
                                  "+ sources/status-drive4.log + sources/status-drive5.log + status-cs25m.log "
                                  "+ status-ct30m.log + batch-keys-b28.json + published batch-28 drive-4/drive-5 "
                                  "15M-probe canonical outputs (experiments "
                                  "n11-centralreply-closure-class5343-batch28-drive{4,5}-20261123) and the "
                                  "exhausted-reprobe canonical outputs (experiments "
                                  "n11-centralreply-class5343-b28exhausted-reprobe25m-20261123 / "
                                  "n11-centralreply-class5343-b28aa050-reprobe30m-20261123), commit-pinned "
                                  "raw fetch; batch-keys sha256 af19208f..; the nine targets are the P4 package "
                                  "WIN rows of the b28-win46 thirdimpl queue registry with PER-KEY decisive "
                                  "probe budgets 15M/15M/15M/15M/15M/25M/25M/25M/30M"),
                     "queue_registry": ("published bookkeeping registry (experiment "
                                        "n11-centralreply-class5343-b28win46-thirdimpl-queue-registry-20261124): "
                                        "rev3 queue-registry.json 334f6209.. + README 4b20c6a0.. (P4 keys and "
                                        "pinned nodes machine-gated by this maker; the registry reserves NO "
                                        "package -- this Part is the single-owner publish-then-execute declaration"),
                     "b28_batch_keys_sha256": PIN_B28,
                     "b28_status_drive4_sha256": PIN_STATUS_D4,
                     "b28_status_drive5_sha256": PIN_STATUS_D5,
                     "b28_status_cs25m_sha256": PIN_STATUS_CS25,
                     "b28_status_ct30m_sha256": PIN_STATUS_CT30,
                     "unadopted": ("published Part DB batch-29 37-LOSS adoption re-audit (experiment "
                                   "n11-centralreply-class2251-loss37-adoption-reaudit-20261124): merged canonical "
                                   "cache sha256 04b0a239.. (6,354 rows = CU 6,317 30ddad9d.. + 37 batch-29 LOSS "
                                   "rows) is the CURRENT canonical chain head and carries NO row for the nine "
                                   "targets (machine-gated both by this maker and by audit_dh.py G6); the Part CO "
                                   "merged cache 854800f3.. (6,301 rows) likewise; increment b29loss37 85bd4469.., "
                                   "increments-manifest-db 1b51f30d..; DECLARED DH split: the five 15M-solved "
                                   "targets (aa011/aa054/aa022/aa034/aa037) legitimately appear in the Part CO "
                                   "manifest win roster (win_ids/unadopted_win_ids/unadopted_win_rows "
                                   "node-exact) and must NOT appear in exhausted_excluded_ids; the four "
                                   "reprobe-decisive targets (aa032/aa028/aa021/aa050) are Part CO "
                                   "exhausted_excluded_ids members (their 15M drive EXHAUSTED rows are pinned "
                                   "above) whose WIN labels come from the cs-25m/ct-30m reprobe publications + "
                                   "registry; all nine must NOT appear in any adopted/loss/fragment list, nor "
                                   "anywhere in the batch-29-scoped DB manifest; they are UNADOPTED honest "
                                   "labels pending the scrutiny owner C++ second-implementation gate "
                                   "9193f5b6 unchanged"),
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
    print("DH-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"], "src", r["source"])
    print("unadopted rows: absent from CO and DB merged canonical caches + both increments + every adopted/loss/fragment list (machine-gated)")
    print("win roster: five 15M targets node-exact in CO unadopted_win_rows; four reprobe targets in CO exhausted_excluded_ids with cs-25m/ct-30m decisive rows == raw == queue-registry rows (machine-gated)")

if __name__ == "__main__":
    main()
