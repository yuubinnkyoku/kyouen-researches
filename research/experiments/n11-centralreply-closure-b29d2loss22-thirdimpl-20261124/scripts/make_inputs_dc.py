# make_inputs_dc.py -- machine-derive the Part DC third-impl input CSVs and
# rows.json for the TWENTY-TWO published batch-29 (closure class 2251) drive-2
# ckpt-3/3 LOSS rows (ab033..ab054, result 2, budget 15000000,
# nodes 1.9M-7.9M) -- UNCONSUMED honest probe-level labels -- from the published canonical
# artifacts (zero hand transcription). Fail-closed: any unexpected field
# aborts.
#
# Adapted from the published Part DA maker (make_inputs_da.py, sha256
# 2cfe8d32e70cbd1e9c9cfa5878d47f38c59a2e1c9144caf5878ff32e5cda377,
# experiment n11-centralreply-closure-b29d2loss15-thirdimpl-20261124, itself
# adapted from the published Part CW maker (make_inputs_cw.py, sha256
# 8a9fe75e4d22f8a6b51aeeacc7c571f0dc62fe5a83b1b2612f95958199fbba74,
# experiment n11-centralreply-closure-b28cqwin2-thirdimpl-20261124, itself
# from the published Part CR maker 364a217f.. / CM f926b5be.. / CL 177c4409 /
# CC 8255d0ad / BY 359aebef / BX e1def905 / BW f94d6e4f). Declared deltas
# (all in the Part DC declaration before execution):
# (a) sources are the same published batch-29 kit + Part CI takeover drive-2
#     publications as the published Part DA kit (ver byte-clones here)
#     (experiment n11-centralreply-closure-class2251-batch29-20261123:
#     batch-keys json 330c0b9f.., full 55-line status.log b49322d9.. with the
#     drive-1 prefix byte-pinned to the Part CU manifest status_log_sha256
#     6b877344.., README 56fa34e3.., drive-2 declaration/completion logs
#     8819c366../46c461bd.., the 22 targets' raw p1+p2 pins (44), published
#     input csv pins (22));
# (b) the target battery gates the TWENTY-TWO batch-29 drive-2 ckpt-3/3 LOSS
#     rows (ab033..ab054, result 2, budget 15000000) instead
#     of CZ's single WIN row ab028; the replica budget gate is 15000000
#     (the declared batch-29 probe condition), and the batch-29
#     s5/membership values come from batch-keys json; NEW drive-2 status
#     battery: 55 lines = 54 PASS + 1 WIN-HALT, the WIN-HALT key is exactly
#     ab028 (NOT a DC target), each target PASS row == the published
#     drive-2 LOSS row (15000000,2,<nodes>), each drive-1 PASS row
#     (ab001..ab016) node-matches the Part CU adopted
#     increment row for the same key, every other PASS row result 2, and the
#     drive-2 PASS roster == batch-keys-minus-probed == the CU manifest
#     fileless_unprobed_ids roster exactly;
# (c) the unadopted-corroboration sources switch from the Part CO 7-LOSS
#     adoption to the Part CU 16-LOSS adoption publications (merged canonical
#     cache 30ddad9d.. 6,317 rows = CO base 854800f3 6,301 + the 16 adopted
#     drive-1 LOSS rows; increment bab011e3..; increments-manifest f9f58ee1..).
#     DECLARED batch-29 adaptation of the CW id-list gates: each of the 15
#     targets is a batch-29 member whose CU-time status was fileless
#     UNPROBED (the CU manifest carries it ONLY in
#     batches[0].fileless_unprobed_ids, the 38-key roster), so the machine
#     gates below require every target to be absent from every ADOPTED/WIN
#     id list (loss_ids / win_ids / unadopted_win_ids /
#     unadopted_win_rows / batches adopted_loss_ids / already_adopted_ids /
#     unadopted_win_ids / fragment_ids / resolved_ids / probed_ids) AND
#     PRESENT in fileless_unprobed_ids, and require the CU merged canonical
#     cache (6,317 rows) to carry NO s5verdict row for any target key
#     (never adopted; the LOSS verdicts stay unconsumed pending the
#     canonical adoption Parts).
# Verdicts are NOT consumed anywhere; the 22 LOSS rows stay honest labels.
# The standard 11x11 empty board, the central-reply roots, class 2251 and
# every batch-29 key remain UNKNOWN.
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
PIN_RAW_DC = {
    "ab033.p1": "1fb2b25017e6d899b105652fd104316628ec66aaa5e35ef91e3ee5876396e260",
    "ab033.p2": "b4545d3682aafb11701f344a82e38f4f817b713e6e5a6936e6f89f68faabd39c",
    "ab034.p1": "02cc6aac705e6ebe788486f8ef5e5aa835d9238d076dadc5706ba14b92118b33",
    "ab034.p2": "1276f66702e70de460e612c5b0a26e6f083e3c471080ac10699a32db43f32a4a",
    "ab035.p1": "a64a66c342c01a798b707111b6e1959a373d6784c23a231626cbb54bf51e07c1",
    "ab035.p2": "cac28df0e7bc55707c762e4db490694f66148d4e2e1ac68725e5497a521d3f04",
    "ab036.p1": "fb66e6ba9f93c02cc63821a432e94aa98485adbe501cb7d2969ab913849043ba",
    "ab036.p2": "612cf8697ac4f05a351205e665c779a6a9643f1cad4ce7f7f0e19e8806a06c66",
    "ab037.p1": "ccf3bdc3912be63d0236cfcf1ef98ed1de5fbbb7a1a7f6fad26068fb9f67cd10",
    "ab037.p2": "ec56ba4c8081c1a57170012304a9af6429743d235dc0321c967a4b47e0eba730",
    "ab038.p1": "1faabe063bdf0e11895fe569896e780c86e596015110928b77b9c2ace11858c9",
    "ab038.p2": "b1c8bbf46d84600126765480133328830e80fab29f2e68f2b813a01ae5a04f2e",
    "ab039.p1": "6010281e79aca63c1017b3dae72fe3559482e4d5ffeec0e0fba16e8988830769",
    "ab039.p2": "6e66a85edc3b0fcaa9da92fd58630586266527fb299ac329162d081bfb3a8d36",
    "ab040.p1": "d5458452c343f7f82e6f278e9760f7675ae6aa8d7ea107344a798cb59d0df335",
    "ab040.p2": "5f49c18615e2278cf872ea7afb9a7fa0b0679f04322cfbf9679742a60a9ab99e",
    "ab041.p1": "b2aec1abca8019fbc4f7496f5c89dfe0ce4eb0150e3af946f04676501b0c47bb",
    "ab041.p2": "0a24ebf4a96207c4c1df0d68a482f0875ca61a97da5d2c8b9f55beab6b9fd666",
    "ab042.p1": "714daf54f12b742dc80ba5140c5626d639f9cd9cbce1b15749efcf202725a6e0",
    "ab042.p2": "e7042cd71c8407c3f2b48eda39f6a26de3e1303fdc3afd43d21f206cd5093c65",
    "ab043.p1": "a0d6c3a07d922ed3abda4f7fecb562ad6747acd9ff93c89b0c9ef57cdaecced5",
    "ab043.p2": "430ff6e191f49e71d60d81ff60c7c44fe09638431673d9b1886effed801f9fd9",
    "ab044.p1": "18128ecb2bf8fc74f0bab09a6b57ceabfdae66a47eefbe8830cfa76d826944b6",
    "ab044.p2": "6c391e4d32fdcd85f6744d23fafef6c23e75f46c5937d105a24fa5578258f4bb",
    "ab045.p1": "4f4cb428c31e26ca537aa1bbde092a333141d9dd6edb494afadf1fce1bf2e39c",
    "ab045.p2": "acb756456316f34959332292dc6f125242c40b973e8ef7d2b2e1ad3b50a5c4f8",
    "ab046.p1": "d0aa5b31e90fae9e2eba9f8cff0eff7cc5d41fb28b174fd1f5165bc03169676a",
    "ab046.p2": "6b2b38ef1900d6a150a2f0b36d6f5125bea2d408b83eac2e82b48e21d1a6b9ea",
    "ab047.p1": "2e9f7cf2b19a1896933e9201a7245b218c89895325aee2c8720448e64af03850",
    "ab047.p2": "f53697178e1f6aa8b6561a26c043a00729963c6e15c806599c0c2e912cecdb03",
    "ab048.p1": "30b633c167824c84fb32e117c164aacf026aafeaa4f35cfcaa051d3ddaa2c087",
    "ab048.p2": "d71f73ccad93b58f6dffe09faf0d3eea8bc97007a794a13814bf5047a51d4fc9",
    "ab049.p1": "44b431f5941d5f35138c63eacf1ac6e662431f06c87d06ce39d103bb60065071",
    "ab049.p2": "6c3aac130f498985e993bb78cc4c80b364a3e7b15293048ee69f93dd6bd0098e",
    "ab050.p1": "b027f4d91a95f954049d1d8313e2b9a7c07f6b719d22a7edcf7829adae371d9e",
    "ab050.p2": "b027f4d91a95f954049d1d8313e2b9a7c07f6b719d22a7edcf7829adae371d9e",
    "ab051.p1": "198af4f083bf59dd971b6e4dd775a6d7120d1b315dc8d18164e0b18bed65a91c",
    "ab051.p2": "3898a79281f3ff8f3e884fa1e1f3dfa4c962b023cece5787c88786b17ea937f1",
    "ab052.p1": "28b105794acb36705102755a39d3a64d1a718bc5b900f5d0f758c8ebcd7cd74e",
    "ab052.p2": "eae0d933fc275933fdad3d46ff0cf53625f371f48d11d46ca0502688a1c243b7",
    "ab053.p1": "a92b7c0a78ea5eb66c0e0ef9b82410507faf1e8047ce417c77598a7a406ef533",
    "ab053.p2": "a92b7c0a78ea5eb66c0e0ef9b82410507faf1e8047ce417c77598a7a406ef533",
    "ab054.p1": "22a825e42af6ab1cdd7b83390c9831a69a9a1841aee6f979136decdf266bb6a3",
    "ab054.p2": "2e4c5e1dbcc379f1f50f64fb83e4aa0a5d73b1fb20a17152353205b835fbbeab",
}
PIN_PUB_INPUT = {
    "ab033": "90198c23475ee6249cf626d553d608147bd586d6cced1c4cc701b50b77dca5d9",
    "ab034": "06f8cd09bfde349cb8f04614950555fc1655fc874a8ca31ff5e752f1d71e47a9",
    "ab035": "108b865422318d8616f8763c19134b77f0ef73f8725a56591f51a317f794f1fa",
    "ab036": "b80e36a6ae7f0fdd58c59ab0b7cda8a8258e48048d3eaed7ec2779aa90e4099b",
    "ab037": "034fe3fbf4120e1a3deb37bcdb7fe9e448c76841b61f8fd2a00cb04274489292",
    "ab038": "4800383bfd56fd3e1d7d0ee89fd953337f60d9f86851f137a6674ca5af94650f",
    "ab039": "b5ea825a8be4f56f23004aac31e50dfc09465a6c839332a91c851cf6ca04386d",
    "ab040": "3c417efcc096d71fd7baa1a49b92c5a1e3402a1bd785ec7e08b0819a07ce757b",
    "ab041": "fd208a23b758951fef82e0da0434366c0e5bafe0dafb9fb3479b310a749d2210",
    "ab042": "ed0dcdcb18bc71e6e9dea2fd18552ba1396c17edcd984ae370517c3ac6826c5c",
    "ab043": "77704b1467e4cc737a44496909cd54d2743a527bdd2816f209171a6bd73a18e1",
    "ab044": "16b1bfce3313691fec71f80714cf22cde6bf68188f9c95842e74c925bdc8a835",
    "ab045": "76c627bf788b54855387aff661318ffaddd0dfd426f94dd7dee60de38fa53f6f",
    "ab046": "588666ed2e6a942268cfc2d478abe131974fb2770d3980ad4a0dc051800147d5",
    "ab047": "45cf9d2d96839c40d6a8ed54e856c3ff3b6ee3fb47b619e0b87bc64da19ce9c1",
    "ab048": "7fc102e1b4b27985855867038ff604f67c036622b9b4c5b6b130fa7096b4cf6d",
    "ab049": "bc6ff70c2bd08bad203fe49a15db27bf9d2d43c6c9e1a1a3efe5078f1c60d2ab",
    "ab050": "8ecb0b745f08f0fdcf3c896fb4c5503ef7ee554f13fa1e8fddac08fc5ed4e25e",
    "ab051": "20cb3cd848b2ede226bb288871eac64d17bed2b0e5f61e81300a8216747ea71e",
    "ab052": "efe3f08a003e9c6ae34f7abb05e763f56835f67fe725cbec618dcbf6e1220af1",
    "ab053": "10f91d6f0ea8c6dc91915d9d52a38fceee46fe0829faac2c4ebb7190b945e590",
    "ab054": "6f8abf10d6a680c1ae99c2b1d341bd53aad002883d9f8f51b1fda16fd4e88bc0",
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
# Part DB 37-LOSS adoption publications (post-CU canonical chain, published
# 2026-11-24: increment 37 rows 85bd4469.. + post-adoption canonical merged
# cache 6,354 rows 04b0a239..). The 22 DC targets are byte-present in BOTH
# (G6b corroboration target) -- this is NOT a new verdict.
PIN_INCREMENT_DB = "85bd44693edfd862a7cf74fc10414978fcf248dcef684a821b487f9757b443cc"
PIN_MERGED_DB = "04b0a23987a97518e276ea5ff966496facab22f93628cd5fbc682a04c3650556"

TARGETS = ["ab033", "ab034", "ab035", "ab036", "ab037", "ab038",
    "ab039", "ab040", "ab041", "ab042", "ab043", "ab044",
    "ab045", "ab046", "ab047", "ab048", "ab049", "ab050",
    "ab051", "ab052", "ab053", "ab054"]
EXPECT_S5 = {
    "ab033": 93820,
    "ab034": 93821,
    "ab035": 93822,
    "ab036": 93823,
    "ab037": 93824,
    "ab038": 93825,
    "ab039": 93826,
    "ab040": 93827,
    "ab041": 93828,
    "ab042": 93829,
    "ab043": 93830,
    "ab044": 93831,
    "ab045": 93832,
    "ab046": 93833,
    "ab047": 93834,
    "ab048": 93835,
    "ab049": 93836,
    "ab050": 93837,
    "ab051": 93838,
    "ab052": 93839,
    "ab053": 93840,
    "ab054": 93841,
}
EXPECT_MEMBERSHIP = {
    "ab033": 4,
    "ab034": 4,
    "ab035": 4,
    "ab036": 2,
    "ab037": 4,
    "ab038": 4,
    "ab039": 4,
    "ab040": 4,
    "ab041": 4,
    "ab042": 4,
    "ab043": 4,
    "ab044": 4,
    "ab045": 4,
    "ab046": 4,
    "ab047": 4,
    "ab048": 4,
    "ab049": 4,
    "ab050": 4,
    "ab051": 4,
    "ab052": 4,
    "ab053": 4,
    "ab054": 4,
}
EXPECT_RESULT = {
    "ab033": 2,
    "ab034": 2,
    "ab035": 2,
    "ab036": 2,
    "ab037": 2,
    "ab038": 2,
    "ab039": 2,
    "ab040": 2,
    "ab041": 2,
    "ab042": 2,
    "ab043": 2,
    "ab044": 2,
    "ab045": 2,
    "ab046": 2,
    "ab047": 2,
    "ab048": 2,
    "ab049": 2,
    "ab050": 2,
    "ab051": 2,
    "ab052": 2,
    "ab053": 2,
    "ab054": 2,
}
EXPECT_REPLICA = {
    "ab033": 5737514,
    "ab034": 2421190,
    "ab035": 3712073,
    "ab036": 5512708,
    "ab037": 3582387,
    "ab038": 7949979,
    "ab039": 3343978,
    "ab040": 3796441,
    "ab041": 4746725,
    "ab042": 1926643,
    "ab043": 3003611,
    "ab044": 4719146,
    "ab045": 3978891,
    "ab046": 4979936,
    "ab047": 5604561,
    "ab048": 3457154,
    "ab049": 4332757,
    "ab050": 4127068,
    "ab051": 6906311,
    "ab052": 5830122,
    "ab053": 2832769,
    "ab054": 3014059,
}
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
    if result != 2:
        sys.exit(f"ABORT {key}: Part DC targets are the drive-2 LOSS rows (ckpt-3/3), got result={result}")
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
                        ("increments-manifest-cu.json", PIN_INCR_MANIFEST),
                        ("increment-b29loss37.cache", PIN_INCREMENT_DB),
                        ("merged-cache-db-b29loss37.cache", PIN_MERGED_DB)):
        got = sha256(os.path.join(SRC, fname))
        if got != pin:
            sys.exit(f"ABORT {fname} sha {got} != pin {pin}")
    for k, pin in PIN_RAW_DC.items():
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
    WINHALT_KEYS = ["ab028"]
    if sorted(winhalt_map) != WINHALT_KEYS:
        sys.exit(f"ABORT status-b29.log WIN-HALT keys {sorted(winhalt_map)} != {WINHALT_KEYS}")
    # target PASS rows == the published drive-2 LOSS rows (budget, result 2, node pins)
    for kk in TARGETS:
        if pass_map[kk][0] != [str(B29_BUDGET), str(EXPECT_RESULT[kk]), str(EXPECT_REPLICA[kk])]:
            sys.exit(f"ABORT status-b29.log {kk} PASS row is not the published drive-2 LOSS row: {pass_map[kk][0]}")
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
    # every non-target drive-2 PASS row is result 2 (LOSS discipline); the
    # published WIN row ab028 (the WIN-HALT key) is the single declared
    # result-1 exception and its PASS row is node-pinned to the published
    # drive-2 WIN row (15000000,1,3167121 -- the Part CZ target)
    WIN_ROWS = {"ab028": ["15000000", "1", "3167121"]}
    for kk in DRIVE2_KEYS:
        if kk in TARGETS:
            continue
        if kk in WIN_ROWS:
            if pass_map[kk][0] != WIN_ROWS[kk]:
                sys.exit(f"ABORT status-b29.log {kk} PASS row is not the published drive-2 WIN row: {pass_map[kk][0]}")
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
    # -- post-DB canonical corroboration (Part DC declared adaptation): the
    #    22 targets were adopted into the canonical chain by the Part DB
    #    37-LOSS adoption (published 2026-11-24 02:38Z: increment 37 rows
    #    85bd4469.., post-adoption canonical merged cache 6,354 rows
    #    04b0a239..). Each target row must be BYTE-IDENTICALLY present in
    #    BOTH with (result 2, published nodes): a machine cross-artifact
    #    consistency gate on the pinned DB publications, NOT a new verdict
    #    and NOT any claim about coverage/class status.
    db_inc_rows = [l for l in open(os.path.join(SRC, "increment-b29loss37.cache")).read().splitlines()
                   if l.startswith("s5verdict,")]
    if len(db_inc_rows) != 37:
        sys.exit(f"ABORT DB increment s5verdict rows {len(db_inc_rows)} != 37")
    db_merged = open(os.path.join(SRC, "merged-cache-db-b29loss37.cache")).read().splitlines()
    db_s5rows = [l for l in db_merged if l.startswith("s5verdict,")]
    if len(db_s5rows) != 6354:
        sys.exit(f"ABORT DB post-adoption canonical s5verdict rows {len(db_s5rows)} != 6354")
    for r in rows:
        row_expected = f"s5verdict,{r['lo']},{r['hi']},5,{r['replica_result']},{r['replica_nodes']}"
        if sum(1 for l in db_inc_rows if l == row_expected) != 1:
            sys.exit(f"ABORT {r['key_id']}: DB increment row not byte-unique: {row_expected}")
        if sum(1 for l in db_s5rows if l == row_expected) != 1:
            sys.exit(f"ABORT {r['key_id']}: DB post-adoption canonical row not byte-unique: {row_expected}")
    # -- anchors/negatives (published constants, AR->BF->...->CR->CW->CZ->DA
    #    provenance chain)
    anchor_rows = []
    for key, lo, hi, legal, res, exp, ttH, expect in ANCHORS:
        anchor_rows.append({
            "key_id": key, "stones": 5, "lo": lo, "hi": hi, "legal": legal,
            "expect_third": res, "anchor_expansions": exp, "anchor_ttHits": ttH,
            "expect_kind": expect, "replica_result": None, "replica_nodes": None,
        })
    # -- rows.json
    rows_json = {"schema": "n11-centralreply-closure-b29d2loss22-thirdimpl-input-v1",
                 "sources": {
                     "b29drive2": ("sources/raw 22 targets p1+p2 + sources/status-b29.log + sources/log-b29drive2-declaration.md "
                                   "+ log-b29drive2-completion.md + batch-keys-b29.json + published batch-29 drive-2 "
                                   "canonical outputs (experiment n11-centralreply-closure-class2251-batch29-20261123, "
                                   "completion log research/log/2026-11-24-part-ci-takeover-batch29-drive2-completion.md), "
                                   "commit-pinned raw fetch; batch-keys sha256 330c0b9f..; the 22 targets are the "
                                   "batch-29 drive-2 ckpt-3/3 LOSS rows ab033..ab054 (budget 15000000, "
                                   "result 2, cross-checked against the drive-2 status PASS rows)"),
                     "b29_batch_keys_sha256": PIN_B29,
                     "b29drive2_status_sha256": PIN_STATUS_B29,
                     "b29drive2_status_drive1_prefix_sha256": PIN_STATUS_DRIVE1_PREFIX,
                     "b29drive2_completion_log_sha256": PIN_LOG_COMPL,
                     "b29loss37_adoption": ("published Part DB 37-LOSS adoption (experiment "
                                            "n11-centralreply-class2251-loss37-adoption-reaudit-20261124, MANIFEST d5ed5dc3): "
                                            "increment sha256 85bd4469.. (37 rows incl. the 22 targets), post-adoption canonical "
                                            "merged cache sha256 04b0a239.. (6,354 rows = CU 30ddad9d 6,317 + 37); each target "
                                            "row byte-identical in both (machine gate)"),
                     "unadopted": ("published Part CU 16-LOSS adoption re-audit (experiment "
                                  "n11-centralreply-class2251-loss16-adoption-reaudit-20261123): merged canonical "
                                  "cache sha256 30ddad9d.. (6,317 rows = Part CO base 854800f3 6,301 + the 16 adopted "
                                  "batch-29 drive-1 LOSS rows) is UNCHANGED and carries NO row for any of the 22 "
                                  "ckpt-3/3 targets (machine-gated both by this maker and by audit_dc.py G6); "
                                  "increment bab011e3.., increments-manifest f9f58ee1.., pinned fail-closed merger "
                                  "90711961..; DECLARED batch-29 adaptation: the 22 cross-verified drive-2 LOSS "
                                  "rows appear ONLY in the manifest batches[0].fileless_unprobed_ids roster "
                                  "(their CU-time UNPROBED status), NOT in any adopted/win/probed id list; they "
                                  "were UNADOPTED honest labels at CU snapshot time; DISCLOSED: they have since been adopted into the canonical chain by the published Part DB 37-LOSS adoption (2026-11-24 02:38Z: increment 85bd4469.., post-adoption canonical cache 04b0a239.. 6,354 rows; machine cross-checked here -- each target row byte-identical in both); this Part DC is a read-only corroboration lane and consumes no verdict"),
                     "anchors": ("published anchor/negative values, input CSVs byte-equality-checked against the "
                                 "published Part BF experiment (provenance chain AR -> BF -> BK -> BM -> BS -> BV -> "
                                 "BW -> BX -> BY -> CC -> CL -> CM -> CR -> CW -> CZ -> DA -> DC)")},
                 "consumed_into_canonical_cache": False,
                 "unadopted_win_rows": False,
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
    print("DC-SCAFFOLD maker gates PASS")
    print("targets", len(rows), "anchors", len(anchor_rows), "negatives", len(NEGATIVES))
    for r in rows:
        print(" ", r["key_id"], f"[{r['lo']}, {r['hi']}]", "legal", r["legal"], "s5", r["s5_index"],
              "membership", r["membership_class_count"], "replica_result", r["replica_result"],
              "replica_nodes", r["replica_nodes"], "expect_third", r["expect_third"])
    print("unadopted rows: absent from merged canonical cache + increment + every adopted/win id list (machine-gated)")
    print("cross-artifact: drive-2 PASS roster == batch-keys minus CU-adopted 16 == CU fileless roster (machine-gated)")

if __name__ == "__main__":
    main()
