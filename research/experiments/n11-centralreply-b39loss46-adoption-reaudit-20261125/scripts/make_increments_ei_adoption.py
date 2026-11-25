"""Build the b39loss46 (Part EI batch-39 loss-only) canonical-adoption
increment, fail-closed.

Part EI (2026-11-25).  BASE = the published Part EE canonical merged cache
(6,666 rows, sha fc3e4ac9...; WIN 158 / LOSS 6,508; the af034loss1 adoption
of Part ED).  The adopted pool is the published Part EH batch-39 probe
(closure class 30484 rank-20 fresh-frontier, class 30484, 2026-11-25, 178
files, MANIFEST-sha256 52b69c04...): exactly the 46 honest-label exact-LOSS
rows aj001..aj050 minus {aj030, aj039} (EXHAUSTED honest UNKNOWN at the
pre-declared 15M condition; same-condition re-probe prohibited) and minus
{aj049, aj050} (probe-level WINs, UNCONSUMED everywhere; adoption only via
the scrutiny-owner C++ second-implementation gate 9193f5b6...).  All 50
targets were probed fresh-cold two-pass node-exact at budget 15,000,000
order=0 (MISMATCH 0, whole-packet nodes/pass 177,032,132; adopted rows
140,162,086 of those).  The 2 claim-reserved dual-class batch-38 keys
(ai044/ai048, Part EF in-flight single-owner) are excluded at pair level and
untouched.  Loss-only canonical adoption: no WIN verdict is consumed; no
root verdict is asserted; 11x11 stays UNKNOWN.

Every gate is fail-closed: any drift aborts with rc=1 and no output is
written.  The published batch-39 kit is verified file-by-file (byte pins
against the published MANIFEST-sha256), the 100 published raw replay pairs
(two-pass fresh-cold node-exact) and the 54-line honest-history status.log
and the machine audit batch-audit.json (5a2b67cb...) are pinned, the 46
adopted keys are proven absent from BASE (fresh-increment gate) and from the
quarantine registry and from the prior-probe-universe (freshness), and the
WIN/EXHAUSTED keys are proven unconsumed (they must sit in NO cache and are
not emitted).
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
MERGER = EXP / "scripts/s5_union_merge.py"

EE_EXP = "n11-centralreply-af034loss1-adoption-reaudit-20261125"
B39_EXP = "n11-centralreply-closure-class30484-batch39-20261125"
BASE_CACHE = ROOT / "research/experiments" / EE_EXP / (
    "output/merged-exact-s5-chain-plus-af034loss1-20261125.cache")
B39_DIR = ROOT / "research/experiments" / B39_EXP
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"

MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA_EXPECTED = "fc3e4ac9052447158202f09d5efe05468dba32fe95ec90beaaa0a0de9d2c020f"
BASE_CACHE_ROWS_EXPECTED = 6666
BASE_CACHE_WIN_EXPECTED = 158
BASE_CACHE_LOSS_EXPECTED = 6508
QUARANTINE_SHA_EXPECTED = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

B39_MANIFEST_SHA = "52b69c0404c9f78451249c6decc65f70b908e44a98bebac0b827d8eb8aa5bf41"
B39_KIT_FILES = 178
B39_STATUS_SHA = "08d70bb77c08e7a37b77005b3b2dca1a759f56b4146e1623eef4eb69759a3cea"
B39_AUDIT_SHA = "5a2b67cb4e8bb6b2e3cf6e8f79806ab219ff83b91639e9b4333ed2b9eb91bb4f"
B39_KEYS_SHA = "5e25b550ef42c1f56dc9d4b69d61d33304664ad839ed7f8d19f45fe50f5e63a9"
BUDGET = 15000000
STATUS_LINES = 54
STATUS_FIRST = "2026-11-25T09:36:08Z aj002 PASS 15000000,2,3369672"
STATUS_FINAL = "2026-11-25T10:11:26Z aj049 WIN-HALT"
STATUS_WIN_HALT_LINES = [
    "2026-11-25T10:10:53Z aj050 WIN-HALT",
    "2026-11-25T10:11:26Z aj049 WIN-HALT",
]
STATUS_EXHAUSTED_LINES = [
    "2026-11-25T09:56:39Z aj030 EXHAUSTED 15000000,0,15000000",
    "2026-11-25T10:06:11Z aj039 EXHAUSTED 15000000,0,15000000",
]

SOURCE_PINS = {
    "batch38_batch_keys": "298071046bfba8473c5b3d6e0b6a30108697eb0899aed7c70fcb4c5343f7cb8d",
    "canonical_cache": "fc3e4ac9052447158202f09d5efe05468dba32fe95ec90beaaa0a0de9d2c020f",
    "closure_classes": "27e00b0dbf2f33603dfbed91b00153f73c7a2d05b1258133a39c9ec5bfd41364",
    "freshness_ranks13to20": "deea05b82a391f5e7d5809c08e2b8c77bc5007cc9ccefab55cee259f65d52b54",
    "jsreplay": "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
    "prior_probe_universe": "6deee846a4e67778437cd052502535f4839f3fbe76d5e1ec9bc9b6c0036e942b",
    "quarantine": "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9",
    "refresh_summary": "6af660a1e0ad8f0ad3b0ac6b32c1a24099aa8f1c3a2271496a9bfb99dc80b6bc",
    "runbatch": "f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84",
    "worklist_class30484_extract": "feda8c7295ec6d17562f786eae9f48c59e7d701fd13748ea655b8bbdb7ea33d0",
}

ADOPTED_IDS = ["aj001", "aj002", "aj003", "aj004", "aj005", "aj006", "aj007", "aj008", "aj009", "aj010", "aj011", "aj012", "aj013", "aj014", "aj015", "aj016", "aj017", "aj018", "aj019", "aj020", "aj021", "aj022", "aj023", "aj024", "aj025", "aj026", "aj027", "aj028", "aj029", "aj031", "aj032", "aj033", "aj034", "aj035", "aj036", "aj037", "aj038", "aj040", "aj041", "aj042", "aj043", "aj044", "aj045", "aj046", "aj047", "aj048"]
WIN_IDS_UNCONSUMED = ["aj049", "aj050"]
EXHAUSTED_EXCLUDED_IDS = ["aj030", "aj039"]
PACKET_IDS = sorted(ADOPTED_IDS + WIN_IDS_UNCONSUMED + EXHAUSTED_EXCLUDED_IDS)
CLAIM_RESERVED_IDS = ["ai044", "ai048"]
CLAIM_RESERVED_PAIRS = {
    "ai044": (1152922604135256064, 65536),
    "ai048": (1152921573327372288, 68157440),
}

ADOPTED_NODES_PER_PASS = 140162086
WHOLE_PACKET_NODES_PER_PASS = 177032132

KEY_PINS = {
    "aj001": {"lo": 1152922604269469696, "hi": 65536, "legal": 84,
              "s5_index": 63021, "probe_order": 540, "membership_class_count": 4},
    "aj002": {"lo": 10376294640990027776, "hi": 65536, "legal": 90,
              "s5_index": 82345, "probe_order": 541, "membership_class_count": 4},
    "aj003": {"lo": 3458765613348945920, "hi": 65536, "legal": 81,
              "s5_index": 195180, "probe_order": 542, "membership_class_count": 4},
    "aj004": {"lo": 1152922879013158912, "hi": 65536, "legal": 84,
              "s5_index": 281792, "probe_order": 543, "membership_class_count": 4},
    "aj005": {"lo": 5764608622562639872, "hi": 65536, "legal": 86,
              "s5_index": 298723, "probe_order": 544, "membership_class_count": 4},
    "aj006": {"lo": 1152922604135317504, "hi": 65536, "legal": 88,
              "s5_index": 375902, "probe_order": 545, "membership_class_count": 4},
    "aj007": {"lo": 1152922604135251968, "hi": 65537, "legal": 91,
              "s5_index": 391885, "probe_order": 546, "membership_class_count": 4},
    "aj008": {"lo": 1152922604135251968, "hi": 65538, "legal": 92,
              "s5_index": 474119, "probe_order": 547, "membership_class_count": 4},
    "aj009": {"lo": 1152922741574205440, "hi": 65536, "legal": 81,
              "s5_index": 634046, "probe_order": 548, "membership_class_count": 4},
    "aj010": {"lo": 1152923153891065856, "hi": 65536, "legal": 83,
              "s5_index": 644052, "probe_order": 549, "membership_class_count": 4},
    "aj011": {"lo": 1155174403948937216, "hi": 65536, "legal": 84,
              "s5_index": 655118, "probe_order": 550, "membership_class_count": 4},
    "aj012": {"lo": 1152922604135251968, "hi": 66048, "legal": 89,
              "s5_index": 657320, "probe_order": 551, "membership_class_count": 4},
    "aj013": {"lo": 1152922604202360832, "hi": 65536, "legal": 91,
              "s5_index": 739110, "probe_order": 552, "membership_class_count": 4},
    "aj014": {"lo": 1152922604403687424, "hi": 65536, "legal": 79,
              "s5_index": 744807, "probe_order": 553, "membership_class_count": 4},
    "aj015": {"lo": 1157426203762622464, "hi": 65536, "legal": 79,
              "s5_index": 753448, "probe_order": 554, "membership_class_count": 4},
    "aj016": {"lo": 1152922604135251968, "hi": 66560, "legal": 91,
              "s5_index": 754653, "probe_order": 555, "membership_class_count": 4},
    "aj017": {"lo": 1152922604135284736, "hi": 65536, "legal": 96,
              "s5_index": 815958, "probe_order": 556, "membership_class_count": 4},
    "aj018": {"lo": 1152922604135383040, "hi": 65536, "legal": 87,
              "s5_index": 819898, "probe_order": 557, "membership_class_count": 4},
    "aj019": {"lo": 1161929803389992960, "hi": 65536, "legal": 86,
              "s5_index": 826659, "probe_order": 558, "membership_class_count": 4},
    "aj020": {"lo": 1152922604135251968, "hi": 67584, "legal": 92,
              "s5_index": 827583, "probe_order": 559, "membership_class_count": 4},
    "aj021": {"lo": 1152922604135252032, "hi": 65536, "legal": 95,
              "s5_index": 873785, "probe_order": 560, "membership_class_count": 4},
    "aj022": {"lo": 1170937002644733952, "hi": 65536, "legal": 96,
              "s5_index": 878828, "probe_order": 561, "membership_class_count": 4},
    "aj023": {"lo": 1152922604135251968, "hi": 69632, "legal": 82,
              "s5_index": 879486, "probe_order": 562, "membership_class_count": 4},
    "aj024": {"lo": 1152922604135252480, "hi": 65536, "legal": 97,
              "s5_index": 888597, "probe_order": 563, "membership_class_count": 4},
    "aj025": {"lo": 1152922604137349120, "hi": 65536, "legal": 93,
              "s5_index": 888632, "probe_order": 564, "membership_class_count": 4},
    "aj026": {"lo": 1152922604135252224, "hi": 65536, "legal": 95,
              "s5_index": 890205, "probe_order": 565, "membership_class_count": 4},
    "aj027": {"lo": 1152922608430219264, "hi": 65536, "legal": 91,
              "s5_index": 890217, "probe_order": 566, "membership_class_count": 4},
    "aj028": {"lo": 1152922604135252096, "hi": 65536, "legal": 91,
              "s5_index": 891252, "probe_order": 567, "membership_class_count": 4},
    "aj029": {"lo": 1152931400228274176, "hi": 65536, "legal": 94,
              "s5_index": 891691, "probe_order": 568, "membership_class_count": 4},
    "aj031": {"lo": 1152921574400065536, "hi": 1056768, "legal": 85,
              "s5_index": 893069, "probe_order": 570, "membership_class_count": 4},
    "aj032": {"lo": 1152922604135251972, "hi": 65536, "legal": 95,
              "s5_index": 893865, "probe_order": 571, "membership_class_count": 4},
    "aj033": {"lo": 1152921574400065536, "hi": 17825792, "legal": 97,
              "s5_index": 894452, "probe_order": 572, "membership_class_count": 4},
    "aj034": {"lo": 1152922604135251970, "hi": 65536, "legal": 96,
              "s5_index": 895046, "probe_order": 573, "membership_class_count": 4},
    "aj035": {"lo": 1152921573326324224, "hi": 68157440, "legal": 97,
              "s5_index": 895603, "probe_order": 574, "membership_class_count": 4},
    "aj036": {"lo": 1152922604135251969, "hi": 65536, "legal": 84,
              "s5_index": 896123, "probe_order": 575, "membership_class_count": 3},
    "aj037": {"lo": 1152921573326324736, "hi": 68157440, "legal": 82,
              "s5_index": 896603, "probe_order": 576, "membership_class_count": 3},
    "aj038": {"lo": 1152922604135776256, "hi": 65536, "legal": 96,
              "s5_index": 897649, "probe_order": 577, "membership_class_count": 4},
    "aj040": {"lo": 1152922604135514112, "hi": 65536, "legal": 89,
              "s5_index": 898280, "probe_order": 579, "membership_class_count": 4},
    "aj041": {"lo": 1152927002181763072, "hi": 65536, "legal": 94,
              "s5_index": 898533, "probe_order": 580, "membership_class_count": 4},
    "aj042": {"lo": 1152922604135268352, "hi": 65536, "legal": 83,
              "s5_index": 899043, "probe_order": 581, "membership_class_count": 4},
    "aj043": {"lo": 1152921574400065536, "hi": 1064960, "legal": 89,
              "s5_index": 899372, "probe_order": 582, "membership_class_count": 4},
    "aj044": {"lo": 1152922604135260160, "hi": 65536, "legal": 91,
              "s5_index": 899741, "probe_order": 583, "membership_class_count": 4},
    "aj045": {"lo": 1152921574400065536, "hi": 34603008, "legal": 96,
              "s5_index": 900167, "probe_order": 584, "membership_class_count": 4},
    "aj046": {"lo": 1152922672854728704, "hi": 65536, "legal": 88,
              "s5_index": 901454, "probe_order": 587, "membership_class_count": 3},
    "aj047": {"lo": 1152924803158507520, "hi": 65536, "legal": 91,
              "s5_index": 901621, "probe_order": 588, "membership_class_count": 4},
    "aj048": {"lo": 1152921574400065536, "hi": 1081344, "legal": 86,
              "s5_index": 902090, "probe_order": 589, "membership_class_count": 4},
    "aj030": {"lo": 1152922604135251976, "hi": 65536, "legal": 83,
              "s5_index": 892576, "probe_order": 569, "membership_class_count": 4},
    "aj039": {"lo": 1152922606282735616, "hi": 65536, "legal": 88,
              "s5_index": 897668, "probe_order": 578, "membership_class_count": 4},
    "aj049": {"lo": 1152921574400065536, "hi": 1114112, "legal": 80,
              "s5_index": 902511, "probe_order": 590, "membership_class_count": 3},
    "aj050": {"lo": 1152921574400065536, "hi": 68157440, "legal": 80,
              "s5_index": 902512, "probe_order": 591, "membership_class_count": 2},
}

LABEL_PINS = {
    "aj001": (2, 5156075),
    "aj002": (2, 3369672),
    "aj003": (2, 3540581),
    "aj004": (2, 2262352),
    "aj005": (2, 1633255),
    "aj006": (2, 2722354),
    "aj007": (2, 3164790),
    "aj008": (2, 2063326),
    "aj009": (2, 1387399),
    "aj010": (2, 1456727),
    "aj011": (2, 3327536),
    "aj012": (2, 3786919),
    "aj013": (2, 3372877),
    "aj014": (2, 2835620),
    "aj015": (2, 1067011),
    "aj016": (2, 2629159),
    "aj017": (2, 2855076),
    "aj018": (2, 2238708),
    "aj019": (2, 2269913),
    "aj020": (2, 8446897),
    "aj021": (2, 2357351),
    "aj022": (2, 2872347),
    "aj023": (2, 2536040),
    "aj024": (2, 3959639),
    "aj025": (2, 2265870),
    "aj026": (2, 7255317),
    "aj027": (2, 2846576),
    "aj028": (2, 2976049),
    "aj029": (2, 4011534),
    "aj031": (2, 9591637),
    "aj032": (2, 2768559),
    "aj033": (2, 4367387),
    "aj034": (2, 3029800),
    "aj035": (2, 2604201),
    "aj036": (2, 2158472),
    "aj037": (2, 2348985),
    "aj038": (2, 2701920),
    "aj040": (2, 1869701),
    "aj041": (2, 1382704),
    "aj042": (2, 1487463),
    "aj043": (2, 1414800),
    "aj044": (2, 3325637),
    "aj045": (2, 3712262),
    "aj046": (2, 2031254),
    "aj047": (2, 3033556),
    "aj048": (2, 1666778),
    "aj030": (0, 15000000),      # EXHAUSTED honest UNKNOWN, no same-condition re-probe
    "aj039": (0, 15000000),      # EXHAUSTED honest UNKNOWN, no same-condition re-probe
    "aj049": (1, 4998452),      # probe-level WIN, UNCONSUMED (scrutiny-owner C++ gate only)
    "aj050": (1, 1871594),      # probe-level WIN, UNCONSUMED (scrutiny-owner C++ gate only)
}

RAW_SHAS = {
    "aj001.p1.out": "9666ca540a9df869847094989da30dc96e4d0285b782f22397c57172d83a9d85",
    "aj001.p2.out": "25278cdd052da6f4b2e0cc9954e88d8dd496ab0b81a8eedd6e0b4603931eb04b",
    "aj002.p1.out": "8949697f87317eabb9700a6e5d897d10690b3173800f6b8cae5d1b485431931f",
    "aj002.p2.out": "8949697f87317eabb9700a6e5d897d10690b3173800f6b8cae5d1b485431931f",
    "aj003.p1.out": "8cf27a85697a4aa5124d65ae6fe39f4de6e8db8394a7a2be5e3272f2a5c1d6d9",
    "aj003.p2.out": "8acf755c0a48590d9e8bd213a0e22ab8b8fc9ab819c35e914d344e7dd3dbf308",
    "aj004.p1.out": "42ce5d28566d8c7b5beebdd5c4c2d820a704cb330c7ab7e90de55a5756c468d6",
    "aj004.p2.out": "69bbd88a72ec061057e273ab283df750216a488915e557862683c5eaab0b6782",
    "aj005.p1.out": "78631be25aece45afa80ace6fead4ca155f8014e4c2d9826e7d973ab7b8673e6",
    "aj005.p2.out": "206319ea967918cd990f3dce81132fd647042ee031d3624e6a564568ab3379ef",
    "aj006.p1.out": "efd9b8b402a33afdcc4a166fb2cc86aa60321cfe4e75489c66b2321d9451681e",
    "aj006.p2.out": "3d71e086504f548b81a4b71822203ab7cfe25c5e32cccba7698ec4b574b217af",
    "aj007.p1.out": "b5a0a5c4cd10895da2fdb9ecb862ca3e9d385243ccd19b68440e78e21f22e03f",
    "aj007.p2.out": "1e66d8f34d278ae68f8992f7f6a1b81ce031e4cdcdf021bdd3fcdaff256105ad",
    "aj008.p1.out": "fd6d28b5539b64c17319d1abc49de46ca6fe271744760e94e2c059e673402cee",
    "aj008.p2.out": "666855ca6dd9df74f1553942f1d439ef6f2efb6bf1d0c97a0a7243d6f23d3371",
    "aj009.p1.out": "eaa74d446489c0291efc80d836cc8c0a1a522063828f32bb6bc4fa1b37c3cf48",
    "aj009.p2.out": "d5d14051989407ddb98b35df0102230416de12412e6d0c8916415404c89f6994",
    "aj010.p1.out": "f535f7d8db8896950e2bf3ba445d93146ae90e08eb82f7c129e7c18b86dd3bdc",
    "aj010.p2.out": "00e3d2c4daa47b136476cfea32f9ddc9c1fd334cb1ef7711dc91065376547096",
    "aj011.p1.out": "e6d9e1bfa795c409aabced98ac8a4ffd056eb4e652a438be8a3dfb3724abb4f2",
    "aj011.p2.out": "d70ad80023f63932a1039a4bfc09a3d6a0853e73b91bd14b7638aaac97efd599",
    "aj012.p1.out": "bd7c356afe21f3e508deb63b7831e64e3bb587676e4a90a25e29e04218679e4c",
    "aj012.p2.out": "38823089d1b023f20791a6f151a483192511f49ecd4f53ebd43aad0a8a8db3f7",
    "aj013.p1.out": "b63686550fda7c141b16f33b0fdf0cec2ae1f2473870ef44470e0045ed0e4d3f",
    "aj013.p2.out": "d6db26d024d4f8b408ed84a8a7c9a59e58d4470c3910d1ad2f391c53a29c908d",
    "aj014.p1.out": "240afa41bc1eba0aca23a2f3675cddf423bba60c0e1bf960e70b309b871848e9",
    "aj014.p2.out": "240afa41bc1eba0aca23a2f3675cddf423bba60c0e1bf960e70b309b871848e9",
    "aj015.p1.out": "e7b42c0da52da64e01211eb9bbabc12527aba625273bb294f3b222ba84bc94f7",
    "aj015.p2.out": "97b45f39c619a6ebf97962f0e6fbe7f67f9250f14ae7cbab3fb260c9a1871978",
    "aj016.p1.out": "536d309cd1e894ea628d670f568abe7c418dc7bf557b22127c7554c81926f6bb",
    "aj016.p2.out": "6b51f3717989c33712e3c167bb8e3f11ea844346a483b0e94066fb1100da7585",
    "aj017.p1.out": "6cc6cc13a781c84cfd4186a5c33e7516c87bb9d79c34500b37596b7b95215279",
    "aj017.p2.out": "2bbe05692891b3e7fc9e84a44074dca5a0c7f52ccf8d5a7f80a416d79e7530b8",
    "aj018.p1.out": "08817a6517d88ba6ce29b26125c65dc76dadbdd4185595a5cbc8e5f0f485bc5b",
    "aj018.p2.out": "237da4263355c17184ce401bbed3fac7189d2e2d262402e51b5c04bae7362919",
    "aj019.p1.out": "046d4e9e34fe914c5b265179d178fced31199b2d4e566d37140e532495533474",
    "aj019.p2.out": "63d6edb36f28ad68d76ec4b25caee10817c4e0db8a536529181123b16751b8d7",
    "aj020.p1.out": "a39a8e5a07e65f5b6010806b01af457a9c8f653baa4edc65b866f81b29fe2e8e",
    "aj020.p2.out": "50dcdc94cfa2a4db9acbdcb649b57b4ae8bd4b979a569cdb92c4844714d3d1ca",
    "aj021.p1.out": "cd37ccaa2c053b739ca186b73b42edb4827144a3b12a5db49f2f403ea7452384",
    "aj021.p2.out": "be27c17e38db12238bd46b58674515580e87da549280845c52905c128d4a729b",
    "aj022.p1.out": "b2379e4fb2a00e81fc2193dbf815e7b1a99ab9cfe61f56f6a3a14ff81966a749",
    "aj022.p2.out": "6a2114665133a3ecf9a711dd4303b7416972bb0883dc4fe817f74875930a6119",
    "aj023.p1.out": "3161b5fe3cb849fa7301e0df67396237dc9c45b1fe0ec7d4c9bca7628105b021",
    "aj023.p2.out": "3161b5fe3cb849fa7301e0df67396237dc9c45b1fe0ec7d4c9bca7628105b021",
    "aj024.p1.out": "086e97c1ade6111ecea4acd7aeb327e513b0eaf9427775fb4ba8d473be7278ed",
    "aj024.p2.out": "3dcf62aa560b216c5fbf640542b5fee92a80a755848fc729ed90171e6dc97934",
    "aj025.p1.out": "ad8d5b1a3136cc25685ccf6b93ac6a5e12c985cae555889171377fab1bd27e5c",
    "aj025.p2.out": "e965f4007e49d6d62371bbc91fe7da94dc6cf6df7511025381d2af2410c0641e",
    "aj026.p1.out": "5343fa1106f83496e19dd7eb2d1a9cbcd3e3dd5bb46b0ad260aafc184a7d1044",
    "aj026.p2.out": "95e7a972f13c58f8c75c320375d97f5fba1100b15fe3b8b4776ba07f8caaa199",
    "aj027.p1.out": "503025b99a15bc853dbaf3137983eb2a510bed7c9d4f868801ea554a634104a5",
    "aj027.p2.out": "9c654a186790c79cb7aa15391399de74501d2a295b31e08fe33b28b8b71e6a9a",
    "aj028.p1.out": "65be6b06cba4ba0dabcd60711aeeaa60a1982666087ed10cf631d45097ad41fc",
    "aj028.p2.out": "0bdbff7dc3f0387d9db612f5f39cdcfc177196dbf017e8c559792c007bed23d8",
    "aj029.p1.out": "83e4eccfe66b9578c40ba131e141a965202fd5650969ded3942631689a1ae2ba",
    "aj029.p2.out": "8d9f4cae54f07cb0cd7d7e1b1e1f83e968ae1f5fdb484c315c61a695641af9a0",
    "aj030.p1.out": "843a0a0c976699d937391377455504797f5bece24222eef74d4452f20e20178c",
    "aj030.p2.out": "661c8e410f8e3f93227ac635233556fec5069ccf115117255a38b3b19f551757",
    "aj031.p1.out": "5504dd94a6158db298537289474d8d328338dc9ed24a0df11583c26f46f2a740",
    "aj031.p2.out": "51749d8e538d7783bf48e12bee073a2f4043e16c0bbcd1dd1d24dc0ef3b1a62a",
    "aj032.p1.out": "926de19c7c651af999fc53cd0cff4c663a882160f9130242c00b5c1b880b8ddd",
    "aj032.p2.out": "926de19c7c651af999fc53cd0cff4c663a882160f9130242c00b5c1b880b8ddd",
    "aj033.p1.out": "de8564d4e2602d2656d5e0ff6f816694d93df8ac295fa97ce51c143e1e15ce84",
    "aj033.p2.out": "97af056fa673c635227eead5aae5af358f7c6be1497993a1e90dd5e9b430f008",
    "aj034.p1.out": "2995e911d98c1068731a2af38fe5124b5705962206d4d0f6c332e4b5364e8757",
    "aj034.p2.out": "2995e911d98c1068731a2af38fe5124b5705962206d4d0f6c332e4b5364e8757",
    "aj035.p1.out": "2399c538b6c5c8f1f8d21a82140512d2ef0bb9a812a07777407ace372e979e84",
    "aj035.p2.out": "e2143007d9dedf7bfccaa82436be4cea85dda4ed06377848fb637d6a8226203b",
    "aj036.p1.out": "13e240dd3aafe4f17e966d65897630f62496bc0b41d5c09aaeef4e7feaa934a4",
    "aj036.p2.out": "c804396450572319cf4680befa41beb9687a4a08bb14e9d7da3ec71ae6c96051",
    "aj037.p1.out": "d4410dce0e0183bc1b2ad4dc38c7e15cf49db824e2c0dcaaed0e306317eb501e",
    "aj037.p2.out": "20d2c70d5d3e7aa22f6716018f27d6938fc9094c4dd669ce4a52b6f9541f4ca7",
    "aj038.p1.out": "40783d648c22e3dbfee0317db49a2b05b2c3bd40fff2641b7a9b86f5bf164a05",
    "aj038.p2.out": "8c8911e3a1b60e474fccf7fb98010abf1dc6837c6b498d42bf238cc0cef65ea3",
    "aj039.p1.out": "60ae21db0e099b22403b8ce64ba97e15de3987acfafb218d79c11aae6c3b4906",
    "aj039.p2.out": "c51899d50649444c3ee8cbb43f3318392131cc3add8b54cbe77d3f600a59dfbb",
    "aj040.p1.out": "f22352e6f0c10f57331c9ec5820acd1ae19098a42642c5327f9f7cadadf5ddd8",
    "aj040.p2.out": "3bf639e7ce62e299a3e83b901585c89b548297854d9807412c41719833cedaf2",
    "aj041.p1.out": "60dad9728700b01bcd3cfdb2c3ac4ebb64133ca3b9e65cd2c5cefe76c70d3dca",
    "aj041.p2.out": "76b9c6656cfd7a5baa4ff1b56aa201fad70b6928a0dcb99419f3aff6ad35a3dd",
    "aj042.p1.out": "a05c6fc592baeae2e980546ecb5756d819975ac5f718f2598f65298cc4dd8621",
    "aj042.p2.out": "c77a84437a65b3743e293102c54ce385675964ac98f5d0b0b9e0d2b64cc6d136",
    "aj043.p1.out": "8220827aab50a8db18af6133f93ddc471a56b3a548d9135ecca3f3bcd520398d",
    "aj043.p2.out": "7d2af2a8379ac2d3a4ba34e436f2521c2cc0d3dcfd2ebddcdf41466c13ff43a3",
    "aj044.p1.out": "f8fa1da185b52f6bf45ef4d5a0d10e0c0bfd1be3f37df7e14dbf5d8637d6eb54",
    "aj044.p2.out": "9d4fcce8bc527707b63537674f7161340f77026b2ec579a23703509b14928b65",
    "aj045.p1.out": "3449d0e484b2b507dd3e541bbe1d48ddf2fa46195bfcfeab748c37144cf0fac1",
    "aj045.p2.out": "9e3c8301242092b54217a5e78df44e07f19c1014ce4ccc6bf42340bdae300cb9",
    "aj046.p1.out": "907db6eeb6637755d49521a1400a36040400c6e4392ae55b7c02f48c0f258eb9",
    "aj046.p2.out": "0da68bb4455fa1d421562cdd88ec5e7b866cca8010f4a190b4a6c5a69b7867a6",
    "aj047.p1.out": "bb5c805201b2344ff8bc93f09dd4cfbb39be3d827c5f6298c23022e2b3e57a4c",
    "aj047.p2.out": "ea2b3d61a57447ce78b74eb0d621163efd5b81bd4a7db1716757e956a797a345",
    "aj048.p1.out": "913c96d67ff9bf8b8cc923b1044cc3138eb0bdee3c30333259e4848aef6903ec",
    "aj048.p2.out": "179f96fd1e75a1788103dfccabc48103a8a3cb7ce6a630b54f7bd2d6f58b4d7e",
    "aj049.p1.out": "50a195f0a1348812bca31ba2279f123bd39cd6928cf4e022c775257771fa695e",
    "aj049.p2.out": "9b7c058feb4665546b4c05b53cd8363bd38c5b30bd9c5fd4ec7a0a701eb83b2d",
    "aj050.p1.out": "50e997dbc23df812f52f6ddcd57839ce447aa92425908b35f34077d47918def2",
    "aj050.p2.out": "8ea868801d44f8522e2ba481c4d8cfdebbf4a2b4cba75f9a0034f61d739cb9f8",
}

INPUT_CSV_SHAS = {
    "aj001": "2f6daea5ca3b3fe6b7713c8d450af3f3c9f203acacb8a1340255d8e8f656496c",
    "aj002": "f804e74ba3f313d330a7a75d991376f867ac3207f3c9b5d2028992dfe91f0dab",
    "aj003": "08cc4972915bc5386e7e3efb62de5c8c3f40be8da4c460d9edaa1ac14ce9456b",
    "aj004": "f2b260c55971daaf9e3bebc400fd8bac256f5471bc8abe3222401665d09e465c",
    "aj005": "533d9f9afa058bc56a76f879241e10886e9d22c9cd13a401e99b27325f266e35",
    "aj006": "868cefe37e286c8cf1b4da10f6eae8e877726de297bd7e548b606e6b4b94178a",
    "aj007": "a5903c5a952aa00cb21121e27da17e043615cc5131ec879d31b8f71b76d05ddf",
    "aj008": "c58df951b0febb47bc6c05b2bc67d7bc9d93b736d5e701019945f9a1d8432a76",
    "aj009": "73037561fc86cc46693ff55a725fb5f815cb3aa19527656260a4de9d38ad1e4e",
    "aj010": "b9f9479e7802a246e52037c1f01ac3fa9a288c2d401f7e9961ccda9c1f8d5323",
    "aj011": "4cd3fdfe7ef70718abe0146b69e0a3ab6766bc5a716ce259b6c710e94fa2474f",
    "aj012": "451007c8c7d9f33b145d017e979caae44b926fae5dec65e53150edcf38d13bed",
    "aj013": "2584f8d1ff75b45b49556d241021bf5a5aa073727f1379ad1c305ae7a36be94e",
    "aj014": "5cf314614a928631c80c08e5f01907943c41cb0f2d45a42433df83edda71331e",
    "aj015": "9e307ebbbc428b624871983b14bc21c196889fc53b16e622ca28d05d2456ab63",
    "aj016": "91e5864fd7b30db7b7f598d2586c34090fbf0bfe1cab5e43f445114be5e7fd63",
    "aj017": "5e3947de4127de7a2890b9ee8541c7d0e175cfe44c13727f44f0d036fd459cde",
    "aj018": "3bf675beaf450fa92b3cd1047fb9e945db690cdfb9a663758d3a58f629c6be23",
    "aj019": "549a30e5efd52ddb9fd6df991c5dc6501165d0ff223f13f6b2f7361df14d7d8a",
    "aj020": "b7e26d07ef6c6fa4a83729328c7cef2daf19f72525a3180fd2529d1f5bdb912c",
    "aj021": "7d80256513c5540bd287166b1181d0d51f24944a87686da13d3a09e7f126d85a",
    "aj022": "2dad418be7911b991b0bf8abada4541fc138340cd026ed37ee8dc0634226e1be",
    "aj023": "c5de8b68230f863ad7463e90ef3e1eb8e9ab3f3b8ad0c51984495429d5c5ca18",
    "aj024": "884a648cb1854c48029a04cfbd7fa1a1ade99ded4d824de8aeac0b471415e676",
    "aj025": "1095676f617fd85cb3288728ef83e37a7c7b319e751a47896ec6b731b6be09dd",
    "aj026": "6c66e97632d92188be33ae928e1a93ba0195bb28924808c0a024f6f9829a19dc",
    "aj027": "9b35ea30143bf93000e84963431512a2b6df1fca363acf5c26137e254105aa09",
    "aj028": "d43f053ec124148861256f0b0207c16b65bb95970194aed6ac190c90f2b358e6",
    "aj029": "9f6c8b211d3117418f071446a46ba62270cc020e151f3907789967fa25a28d5f",
    "aj031": "dff44ed0c0d8949d4df707382420bfb2ba6903801b4ce19e33e2cbd8f590778f",
    "aj032": "4a34284ef945ea3fd56c38da6659c9af842ebf946c5fcae80a0cc31025440166",
    "aj033": "d4b0480e4e05599926632ad6ecb709fce3ac6bc2cd65179884f0f104b79bb932",
    "aj034": "ccca4f4fbc5766f8a1ee06adbbc8b6171e2ba00b3497f516d6c422be0b021dd1",
    "aj035": "69b14f3570a5b347c6c36dfcfb144a20f7ebade21b2444c589d2825f31f402d1",
    "aj036": "801e9c928045191ccf01883199e2f941596b5978fd6466a61eaff2ec027d7dd6",
    "aj037": "9762d21a9a279f97397f37ec8c6b0e8423b92efe3e20c804293c194b41e7b5e7",
    "aj038": "6c0bbf2d725da84fb26b41b0ebc7996b54366a7327028daad2463a3c685fb726",
    "aj040": "4fb6ddd9e3d9124744b5c80ff4018ce61673a97b586f74d75ca5e7dfafcbbc56",
    "aj041": "4c4e9c1879cf1ed3e2ada1c69bedabc8db43645de245aaac2e757c7122a1d225",
    "aj042": "64998e91bae288fbe9b0302b52af6ba0acb2245b5d4dad0d124b1a5f9dcb2264",
    "aj043": "0b048b71a61935ccc777b803e9223ed5d27d92b87c7fed2367736037ff62c4be",
    "aj044": "d0ee8a5d5273db0b75d125413437958994191ee95ce835bb4c565efdf492df99",
    "aj045": "ad63dbcd4895cefaaf3ed734170b1295f44aafe26dc8b2cbcc0c860f4387a7f0",
    "aj046": "6d5c2d2a8f7b2d4ed4192361292090c5fa45e4c009da72e48a84610f5aa599d2",
    "aj047": "3a820574711e6f8e82e8234e49efd41b51bbf348b0fb40c853f1740c5aaf5867",
    "aj048": "0d2e1345396b1a4fc047e59e82835427a9e3831ce645badd76715129c1da83e4",
}

CLASS_30484_BASE_ROW = ("20", "30484", "1152922604135251968", "65536", "52", "24", "40", "4")
FRESHNESS_RANKS = {13: (12264, 0), 14: (5473, 0), 15: (16957, 0), 16: (2634, 0),
                  17: (8785, 0), 18: (1518, 0), 19: (8106, 0), 20: (30484, 52)}

ADOPTED_TABLE_DIGEST = "a7ef2336dd7a93f43619a58677de2c11b6126bb89c5c8cb7fef144dfc4b3d2db"
ADOPTED_INCREMENT_SHA = "a2b24baa0acb253f6b5a2901b601834b8dc50163ad500407192989efcc75e659"

INCREMENT_NAME = "increment-b39loss46-20261125.cache"
EI_SCHEMA = "b39loss46-increments-manifest-v1"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sys_exit(msg: str):
    print(f"ABORT {msg}", file=sys.stderr)
    raise SystemExit(1)


def parse_replay(path: Path):
    row = None
    rows_seen = 0
    for line in path.read_text().splitlines():
        if line.startswith("replay,"):
            parts = line.split(",")
            rows_seen += 1
            row = {
                "stones": int(parts[2]), "legal": int(parts[3]),
                "is_or": int(parts[4]),
                "budget": int(parts[5]), "result": int(parts[6]),
                "nodes": int(parts[7]),
                "lo": parts[9], "hi": parts[10],
            }
    if rows_seen != 1 or row is None:
        sys_exit(f"expected exactly one replay row in {path}")
    return row


def two_pass(kid: str, shas: dict):
    variants = {}
    for tag in ("p1", "p2"):
        p = B39_DIR / f"output/raw/{kid}.{tag}.out"
        if not p.is_file():
            sys_exit(f"missing raw {p}")
        psha = sha(p)
        if psha != shas[f"{kid}.{tag}.out"]:
            sys_exit(f"raw {kid}.{tag}.out sha drift vs the pinned published bytes")
        txt = p.read_text()
        if "# replay_done" not in txt:
            sys_exit(f"raw {kid}.{tag}.out lacks the '# replay_done' completeness guard")
        variants[tag] = parse_replay(p)
    ref = variants["p1"]
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
    for tag, r in variants.items():
        if tuple(r[f] for f in fields) != tuple(ref[f] for f in fields):
            sys_exit(f"{kid}: pass mismatch {tag} vs p1 (fresh two-pass node-exact gate)")
    return ref


def verify_kit(dirp: Path, manifest_sha: str, kit_files: int):
    if not dirp.is_dir():
        sys_exit(f"kit dir missing {dirp}")
    if sha(dirp / "MANIFEST-sha256.txt") != manifest_sha:
        sys_exit(f"kit {dirp.name} MANIFEST sha drift")
    verified = 0
    for line in (dirp / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split()
        want, rel = fields[0], fields[1]
        # the published batch-39 MANIFEST lists repo-root-relative paths
        prefix = "research/experiments/" + B39_EXP + "/"
        if not rel.startswith(prefix):
            sys_exit(f"kit {dirp.name} MANIFEST path outside the kit dir: {rel}")
        p = dirp / rel[len(prefix):]
        if not p.is_file():
            sys_exit(f"kit {dirp.name} file missing: {rel}")
        if sha(p) != want:
            sys_exit(f"kit {dirp.name} file sha drift: {rel}")
        verified += 1
    if verified != kit_files:
        sys_exit(f"kit {dirp.name} files verified {verified} != {kit_files}")
    return verified


def main() -> None:
    # --- anchors: base cache, merger, quarantine ----------------------------
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys_exit("base cache (Part EE canonical) sha drift")
    if sha(MERGER) != MERGER_SHA_EXPECTED:
        sys_exit("fail-closed union merger (scripts/s5_union_merge.py) sha drift: "
                 "this Part must use the pinned merger byte-for-byte")
    if sha(QUARANTINE) != QUARANTINE_SHA_EXPECTED:
        sys_exit("quarantine registry sha drift")
    base_keys = {}
    wins = losss = 0
    with BASE_CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].lstrip().startswith("#"):
                continue
            base_keys[(int(row[1]), int(row[2]))] = (int(row[4]), int(row[5]))
            if int(row[4]) == 1:
                wins += 1
            elif int(row[4]) == 2:
                losss += 1
    if len(base_keys) != BASE_CACHE_ROWS_EXPECTED:
        sys_exit(f"base cache rows {len(base_keys)} != {BASE_CACHE_ROWS_EXPECTED}")
    if wins != BASE_CACHE_WIN_EXPECTED or losss != BASE_CACHE_LOSS_EXPECTED:
        sys_exit(f"base cache WIN/LOSS {wins}/{losss} != pinned")
    q = json.loads(QUARANTINE.read_text())
    quarantined = {tuple(e["key"]) for e in q["entries"] if e.get("active")}

    # --- G-kit: the published batch-39 kit is verified file-by-file ---------
    kit_files = verify_kit(B39_DIR, B39_MANIFEST_SHA, B39_KIT_FILES)
    if sha(B39_DIR / "scripts/jsreplay.js") != SOURCE_PINS["jsreplay"]:
        sys_exit("jsreplay.js sha drift in the batch-39 kit (pinned solver image 8458...)")
    if sha(B39_DIR / "scripts/runbatch.sh") != SOURCE_PINS["runbatch"]:
        sys_exit("runbatch.sh sha drift in the batch-39 kit (pinned f591...)")
    for name, want in SOURCE_PINS.items():
        p = {"batch38_batch_keys": "sources/batch-keys-b38.json",
             "canonical_cache": "sources/canonical-cache-fc3e4ac9.cache",
             "closure_classes": "sources/closure-classes.csv",
             "freshness_ranks13to20": "sources/freshness-ranks13to20.csv",
             "jsreplay": "scripts/jsreplay.js",
             "prior_probe_universe": "sources/prior-probe-universe.csv",
             "quarantine": "sources/quarantine.json",
             "refresh_summary": "sources/refresh-summary.json",
             "runbatch": "scripts/runbatch.sh",
             "worklist_class30484_extract": "sources/worklist-class30484-extract.csv"}[name]
        if sha(B39_DIR / p) != want:
            sys_exit(f"batch-39 source pin drift: {name}")
    if sha(B39_DIR / "output/status.log") != B39_STATUS_SHA:
        sys_exit("batch-39 status.log sha drift")
    if sha(B39_DIR / "output/batch-audit.json") != B39_AUDIT_SHA:
        sys_exit("batch-39 batch-audit.json sha drift")
    if sha(B39_DIR / "input/batch-keys-b39.json") != B39_KEYS_SHA:
        sys_exit("batch-39 batch-keys-b39.json sha drift")

    # --- G-SSOT: batch-audit.json honesty pins --------------------------------
    audit = json.loads((B39_DIR / "output/batch-audit.json").read_text())
    if audit["schema"] != "n11-centralreply-closure-batch39-audit-v1":
        sys_exit("batch-39 audit schema drift")
    res = audit["results"]
    if (res["LOSS"], res["WIN"], res["EXHAUSTED"], res["MISMATCH"]) != (46, 2, 2, 0):
        sys_exit("batch-39 audit honest-label accounting drift (46/2/2/0)")
    if res["total_nodes_all_keys_single_pass"] != WHOLE_PACKET_NODES_PER_PASS:
        sys_exit("batch-39 whole-packet node total drift")
    if res["win_keys_unconsumed"] != WIN_IDS_UNCONSUMED:
        sys_exit("batch-39 audit unconsumed-WIN key set drift")
    if res["exhausted_keys_honest_unknown"] != EXHAUSTED_EXCLUDED_IDS:
        sys_exit("batch-39 audit exhausted-honest key set drift")
    if audit["verdicts_consumed_into_canonical_cache"] is not False:
        sys_exit("batch-39 audit verdicts_consumed must be false (probe-time honesty)")
    if audit["pins"] != SOURCE_PINS:
        sys_exit("batch-39 audit pins table drift vs the pinned batch-39 source pins")
    if audit["target_key_count"] != 50:
        sys_exit("batch-39 audit target count drift")
    audit_per = {e["key_id"]: e for e in audit["per_key"]}
    if len(audit_per) != 50:
        sys_exit("batch-39 audit per_key table must hold exactly the 50 targets")

    # --- G-keys: batch-39 registry (G-accounting) -----------------------------
    keys_doc = json.loads((B39_DIR / "input/batch-keys-b39.json").read_text())
    if keys_doc["schema"] != "n11-centralreply-closure-batch39-keys-v1":
        sys_exit("batch-39 keys schema drift")
    if keys_doc["target_key_count"] != 50 or len(keys_doc["keys"]) != 50:
        sys_exit("batch-39 keys accounting drift (50 targets)")
    if keys_doc["canonical_cache_s5verdict_rows"] != BASE_CACHE_ROWS_EXPECTED:
        sys_exit("batch-39 keys BASE row-count context drift")
    if keys_doc["consumed_into_canonical_cache"] is not False:
        sys_exit("batch-39 keys consumed flag must be false")
    reserved = keys_doc["claim_reserved_excluded"]
    if [e["key_id"] for e in reserved] != CLAIM_RESERVED_IDS:
        sys_exit("batch-39 claim-reserved excluded ids drift (Part EF in-flight)")
    for e in reserved:
        if (e["lo"], e["hi"]) != CLAIM_RESERVED_PAIRS[e["key_id"]]:
            sys_exit(f"claim-reserved pair drift for {e['key_id']}")
        if e["probe_order"] not in (585, 586):
            sys_exit(f"claim-reserved probe_order drift for {e['key_id']}")
    reg = {e["key_id"]: e for e in keys_doc["keys"]}
    if sorted(reg) != PACKET_IDS:
        sys_exit("batch-39 registry key ids != the 50 probed targets")
    for kid, e in reg.items():
        pins = KEY_PINS[kid]
        if e["serving_class"] != 30484 or e["class_unknown_now_at_selection"] != 52:
            sys_exit(f"{kid}: batch-39 registry selection-context drift")
        if (e["lo"], e["hi"], e["legal"]) != (pins["lo"], pins["hi"], pins["legal"]):
            sys_exit(f"{kid}: batch-39 registry lo/hi/legal key-field drift")
        if e["s5_index"] != pins["s5_index"] or e["probe_order"] != pins["probe_order"]:
            sys_exit(f"{kid}: batch-39 registry s5_index/probe_order drift")
    for kid in CLAIM_RESERVED_IDS:
        if kid in reg:
            sys_exit(f"claim-reserved in-flight key {kid} must NOT be a batch-39 target")

    # --- G-status: the 54-line honest history ---------------------------------
    lines = (B39_DIR / "output/status.log").read_text().splitlines()
    if len(lines) != STATUS_LINES:
        sys_exit(f"status lines {len(lines)} != {STATUS_LINES}")
    if lines[0] != STATUS_FIRST or lines[-1] != STATUS_FINAL:
        sys_exit("status first/final line drift")
    if [l for l in lines if "WIN-HALT" in l] != STATUS_WIN_HALT_LINES:
        sys_exit("status WIN-HALT lines != the pinned honest halt history")
    if [l for l in lines if " EXHAUSTED " in l] != STATUS_EXHAUSTED_LINES:
        sys_exit("status EXHAUSTED lines != the pinned honest-history pair")
    import re
    pat = re.compile(r"^(\S+) (aj\d{3}) PASS (\d+),(\d+),(\d+)$")
    got_pass = {}
    others = []
    for line in lines:
        m = pat.match(line)
        if m:
            kid = m.group(2)
            if kid in got_pass:
                sys_exit(f"duplicate status verdict row for {kid}")
            got_pass[kid] = (int(m.group(3)), int(m.group(4)), int(m.group(5)))
            continue
        if "WIN-HALT" in line or " EXHAUSTED " in line:
            continue
        others.append(line)
    if others:
        sys_exit(f"status has UNEXPECTED rows: {others[:3]}")
    if sorted(got_pass) != PACKET_IDS:
        sys_exit("status PASS keys != the 50 targets")
    for kid, (r, n) in LABEL_PINS.items():
        if got_pass[kid] != (BUDGET, r, n):
            sys_exit(f"{kid} status verdict vs pinned honest label drift")

    # --- G-SSOT: the 100 published raws (two-pass fresh-cold node-exact) -----
    raws = {}
    for kid in PACKET_IDS:
        ref = two_pass(kid, RAW_SHAS)
        if ref["stones"] != 5 or ref["is_or"] != 0:
            sys_exit(f"{kid}: wrong depth/or bit")
        if ref["budget"] != BUDGET:
            sys_exit(f"{kid}: budget drift (expected the pre-declared 15M)")
        e = KEY_PINS[kid]
        if ref["legal"] != e["legal"] or ref["lo"] != str(e["lo"]) or ref["hi"] != str(e["hi"]):
            sys_exit(f"{kid}: legal/key disagreement raw vs pinned key fields")
        if (ref["budget"], ref["result"], ref["nodes"]) != got_pass[kid]:
            sys_exit(f"{kid}: raw (budget,result,nodes) row != status verdict row")
        if (ref["result"], ref["nodes"]) != LABEL_PINS[kid]:
            sys_exit(f"{kid}: raw honest-label drift vs the pinned audit label")
        ap = audit_per[kid]
        if (ap["budget"], ap["result"], ap["nodes"], ap["probe_order"]) != (
                BUDGET, ref["result"], ref["nodes"], e["probe_order"]):
            sys_exit(f"{kid}: batch-audit per_key row drift vs the raw replay")
        raws[kid] = ref
    loss_set = sorted(k for k in PACKET_IDS if raws[k]["result"] == 2)
    win_set = sorted(k for k in PACKET_IDS if raws[k]["result"] == 1)
    exh_set = sorted(k for k in PACKET_IDS if raws[k]["result"] == 0)
    if loss_set != sorted(ADOPTED_IDS):
        sys_exit(f"15M decisive LOSS set != the adopted 46: {len(loss_set)}")
    if win_set != WIN_IDS_UNCONSUMED:
        sys_exit(f"15M probe-level WIN set != pinned unconsumed pair: {win_set}")
    if exh_set != EXHAUSTED_EXCLUDED_IDS:
        sys_exit(f"15M still-EXHAUSTED set != pinned honest-UNKNOWN pair: {exh_set}")
    n = sum(raws[k]["nodes"] for k in ADOPTED_IDS)
    if n != ADOPTED_NODES_PER_PASS:
        sys_exit(f"adopted node total drift {n} != {ADOPTED_NODES_PER_PASS}")
    p = sum(raws[k]["nodes"] for k in PACKET_IDS)
    if p != WHOLE_PACKET_NODES_PER_PASS:
        sys_exit(f"whole-packet node total drift {p} != {WHOLE_PACKET_NODES_PER_PASS}")

    # --- G-accounting: 52 == 2 claim-reserved + 50 targets -------------------
    if len(ADOPTED_IDS) + len(WIN_IDS_UNCONSUMED) + len(EXHAUSTED_EXCLUDED_IDS) \
            + len(CLAIM_RESERVED_IDS) != 52:
        sys_exit("class-30484 universe-fresh accounting 52 drift")

    # --- G-input: byte-pinned 1-line input rows of the 46 adopted keys ------
    for kid in ADOPTED_IDS:
        p_in = B39_DIR / f"input/{kid}.input.csv"
        if sha(p_in) != INPUT_CSV_SHAS[kid]:
            sys_exit(f"input csv {kid} sha drift vs the pinned published bytes")
        e = KEY_PINS[kid]
        want_line = f"target,0,5,{e['lo']},{e['hi']},{e['legal']},0,0,0,0,0"
        rows_in = [l for l in p_in.read_text().splitlines() if l.strip()]
        if rows_in != [want_line]:
            sys_exit(f"input csv {kid} body drift: {rows_in}")

    # --- G-worklist/G-closure/G-freshness: selection provenance -------------
    wl = {}
    for row in csv.DictReader((B39_DIR / "sources/worklist-class30484-extract.csv").open()):
        wl[int(row["probe_order"])] = row
    if len(wl) != 52:
        sys_exit("worklist class-30484 extract must hold the 52 universe-fresh rows")
    for kid in ADOPTED_IDS + WIN_IDS_UNCONSUMED + EXHAUSTED_EXCLUDED_IDS:
        e = KEY_PINS[kid]
        r = wl.get(e["probe_order"])
        if r is None:
            sys_exit(f"{kid}: worklist extract row missing at probe_order {e['probe_order']}")
        if (int(r["s5_index"]), r["lo"], r["hi"], int(r["legal"])) != (
                e["s5_index"], str(e["lo"]), str(e["hi"]), e["legal"]):
            sys_exit(f"{kid}: worklist extract field drift vs registry")
        if r["serving_class"] != "30484" or r["class_unknown_now"] != "52":
            sys_exit(f"{kid}: worklist extract selection-context drift")
        if r["closure_first"] != "24" or r["closure_third"] != "40":
            sys_exit(f"{kid}: worklist extract closure-column drift")
        if int(r["membership_class_count"]) != e["membership_class_count"]:
            sys_exit(f"{kid}: worklist extract membership-count drift")
    reserved_orders = {e["probe_order"] for e in reserved}
    for kid in CLAIM_RESERVED_IDS:
        e_pair = CLAIM_RESERVED_PAIRS[kid]
        found = [r for r in wl.values()
                 if (int(r["lo"]), int(r["hi"])) == e_pair]
        if len(found) != 1:
            sys_exit(f"claim-reserved {kid} must sit exactly once in the extract (untouched)")
    if reserved_orders != {585, 586}:
        sys_exit("claim-reserved probe-order drift in the extract")
    clo = list(csv.reader((B39_DIR / "sources/closure-classes.csv").open()))
    hdr, rows_clo = clo[0], clo[1:]
    if hdr != ["class_rank", "class_index", "class_lo", "class_hi", "unknown_now",
               "first_group_first", "first_group_third", "groups_served_count"]:
        sys_exit("closure-classes BASE header drift")
    row30484 = [r for r in rows_clo if r[1] == "30484"]
    if len(row30484) != 1:
        sys_exit("closure BASE must hold exactly one class-30484 row")
    if tuple(row30484[0]) != CLASS_30484_BASE_ROW:
        sys_exit(f"closure BASE class-30484 row drift: {row30484[0]}")
    fr = list(csv.DictReader((B39_DIR / "sources/freshness-ranks13to20.csv").open()))
    if len(fr) != 8:
        sys_exit("freshness ranks13to20 must hold 8 rows")
    for r in fr:
        want = FRESHNESS_RANKS[int(r["rank"])]
        if (int(r["class_index"]), int(r["fresh"])) != want:
            sys_exit(f"freshness-ranks row {r['rank']} drift (rank 20 must be the fresh frontier)")

    # --- G7: prior-probe-universe freshness of the adopted keys --------------
    prior_pairs = set()
    with (B39_DIR / "sources/prior-probe-universe.csv").open() as fh:
        for row in csv.reader(fh):
            prior_pairs.add((int(row[0]), int(row[1])))
    for kid in ADOPTED_IDS:
        e = KEY_PINS[kid]
        if (e["lo"], e["hi"]) in prior_pairs:
            sys_exit(f"{kid}: adopted key already prior-probed (freshness gate G7)")

    # --- freshness: BASE / quarantine / WIN-EXH unconsumed -------------------
    emitted = set()
    for kid in PACKET_IDS:
        e = KEY_PINS[kid]
        key = (e["lo"], e["hi"])
        if key in emitted:
            sys_exit(f"{kid}: duplicate key across the probed packet")
        emitted.add(key)
        if key in quarantined:
            sys_exit(f"{kid}: quarantined key {key}")
    for kid in ADOPTED_IDS:
        e = KEY_PINS[kid]
        if (e["lo"], e["hi"]) in base_keys:
            sys_exit(f"{kid}: key already in canonical BASE; fresh-increment gate")
    for kid in WIN_IDS_UNCONSUMED + EXHAUSTED_EXCLUDED_IDS:
        e = KEY_PINS[kid]
        if (e["lo"], e["hi"]) in base_keys:
            sys_exit(f"{kid}: unconsumed {kid} must sit in NO canonical cache (BASE)")
    for cid, key in CLAIM_RESERVED_PAIRS.items():
        if key in [ (KEY_PINS[k]["lo"], KEY_PINS[k]["hi"]) for k in ADOPTED_IDS ]:
            sys_exit(f"claim-reserved {cid} pair must not be adopted here (Part EF owner)")

    adopted_rows = [(KEY_PINS[k]["lo"], KEY_PINS[k]["hi"], KEY_PINS[k]["legal"],
                     LABEL_PINS[k][0], LABEL_PINS[k][1]) for k in ADOPTED_IDS]
    if len(adopted_rows) != 46 or any(r[3] != 2 for r in adopted_rows):
        sys_exit("adopted rows must be exactly the 46 fresh exact-LOSS rows")
    digest = hashlib.sha256("\n".join(
        f"{lo},{hi},{legal},{result},{nodes}"
        for lo, hi, legal, result, nodes in sorted(adopted_rows)).encode()).hexdigest()
    if digest != ADOPTED_TABLE_DIGEST:
        sys_exit(f"adopted-table digest drift {digest}")

    # --- emit increment + manifest -------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    hdr = HDR_LINES
    rows_for_sort = [(lo, hi, nodes) for lo, hi, legal, result, nodes in adopted_rows]
    rowlines = [f"s5verdict,{lo},{hi},5,2,{nodes}" for lo, hi, nodes in sorted(rows_for_sort)]
    blob = ("\n".join(hdr + rowlines) + "\n").encode("utf-8")
    incr_sha = hashlib.sha256(blob).hexdigest()
    if incr_sha != ADOPTED_INCREMENT_SHA:
        sys_exit(f"emitted increment sha drift {incr_sha} != pinned {ADOPTED_INCREMENT_SHA}")
    (OUT / INCREMENT_NAME).write_bytes(blob)

    adopted_table = [
        {"lo": lo, "hi": hi, "legal": legal, "result": 2, "nodes": nodes}
        for lo, hi, legal, result, nodes in sorted(adopted_rows)]

    manifest = {
        "schema": EI_SCHEMA,
        "batches": [
            {"pool": "b39loss46",
             "adopted_loss_ids": list(ADOPTED_IDS),
             "probed_ids": list(PACKET_IDS),
             "anchor_ids": [],
             "unadopted_win_ids": list(WIN_IDS_UNCONSUMED),
             "exhausted_excluded_ids": list(EXHAUSTED_EXCLUDED_IDS),
             "adopted_nodes_per_pool": ADOPTED_NODES_PER_PASS,
             "whole_packet_nodes": WHOLE_PACKET_NODES_PER_PASS,
             "status_log_sha256": B39_STATUS_SHA,
             "status_log_lines": STATUS_LINES,
             "status_log_first_line": STATUS_FIRST,
             "status_log_final_line": STATUS_FINAL,
             "status_log_win_halt_lines": list(STATUS_WIN_HALT_LINES),
             "status_log_exhausted_lines": list(STATUS_EXHAUSTED_LINES),
             "probed_budget": BUDGET,
             "claim_reserved_excluded_ids": list(CLAIM_RESERVED_IDS),
             "claim_reserved_pairs": {k: list(v) for k, v in CLAIM_RESERVED_PAIRS.items()},
             "kit_integrity": {
                 "kit_manifest_sha256": B39_MANIFEST_SHA,
                 "kit_files_verified": kit_files,
                 "raw_file_sha256_pins": RAW_SHAS,
                 "batch_audit_sha256": B39_AUDIT_SHA,
                 "batch_keys_sha256": B39_KEYS_SHA,
                 "note": "the Part EH batch-39 kit is PUBLISHED (178 files, "
                         "byte-pinned above; fetch-verified against the kit "
                         "MANIFEST-sha256 52b69c04...); the 46 adopted keys are "
                         "fresh at BASE (never probed before batch-39; never "
                         "adopted); 2 EXHAUSTED honest-UNKNOWN and 2 probe-level "
                         "WIN rows are NOT consumed",
             "source_pins": dict(SOURCE_PINS)}},
        ],
        "resolved_ids": list(ADOPTED_IDS),
        "loss_ids": list(ADOPTED_IDS),
        "win_ids": list(WIN_IDS_UNCONSUMED),
        "unadopted_win_ids": list(WIN_IDS_UNCONSUMED),
        "unadopted_win_rows": [
            {"lo": KEY_PINS[k]["lo"], "hi": KEY_PINS[k]["hi"], "legal": KEY_PINS[k]["legal"],
             "result": 1, "nodes": LABEL_PINS[k][1]} for k in WIN_IDS_UNCONSUMED],
        "exhausted_excluded_ids": list(EXHAUSTED_EXCLUDED_IDS),
        "exhausted_rows": [
            {"lo": KEY_PINS[k]["lo"], "hi": KEY_PINS[k]["hi"], "legal": KEY_PINS[k]["legal"],
             "result": 0, "nodes": LABEL_PINS[k][1]} for k in EXHAUSTED_EXCLUDED_IDS],
        "row_counts": {
            "adopted_loss_rows": 46,
            "wins_unconsumed": 2,
            "exhausted_excluded": 2,
            "claim_reserved_excluded": 2,
            "prior_adopted_loss_rows_base": 1,
        },
        "adopted_table": adopted_table,
        "adopted_table_digest_sha256": digest,
        "sha256": {"loss_increment": incr_sha},
        "full_packet_eq_loss_only": False,
        "win_scenario_exists": True,
        "win_scenario_note":
            "the re-probed batch-39 packet contains 2 probe-level WIN rows "
            "{aj049 s5 nodes 4998452, aj050 s5 nodes 1871594}: they are NOT "
            "consumed by this Part (adoption of WIN verdicts is scrutiny-owner "
            "C++ second-implementation gate 9193f5b6 exclusive) and 2 EXHAUSTED "
            "honest-UNKNOWN rows {aj030, aj039} stay excluded (same-condition "
            "re-probe prohibited); only the 46 exact-LOSS rows are adopted",
        "full_packet_eq_loss_only_rationale":
            "the batch-39 packet spans 50 fresh targets: 46 exact LOSS (adopted), "
            "2 EXHAUSTED honest UNKNOWN (excluded), 2 probe-level WIN "
            "(unconsumed); the increment is exactly the 46 LOSS rows; every "
            "emitted key is fresh at BASE (fresh-increment gate against "
            "fc3e4ac9...)",
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_sha256": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "base_cache_absent_hits_for_emitted": 0,
        "base_cache_prior_adoption_confirmed": 0,
        "quarantine_hits": 0,
        "interpretation_guard":
            "canonical 46-LOSS adoption increment: only the fresh batch-39 "
            "exact-LOSS rows (two-pass fresh-cold node-exact at the pre-declared "
            "15M budget/order 0 condition) are consumed into the canonical cache "
            "via the fail-closed union merger; nodes are bookkeeping, never "
            "verdicts; the standard 11x11 empty board stays UNKNOWN; no class "
            "freed or excluded claim is made by the maker (the reaudit refresh "
            "derives scheduling effects machine-only)",
        "provenance": {
            "b39_kit_files": kit_files,
            "status_lines": STATUS_LINES,
            "raws_published": True,
            "audit_per_key_rows": 50,
        },
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "increment_sha256": incr_sha,
        "rows": len(rowlines),
        "adopted_total_nodes_per_pass": ADOPTED_NODES_PER_PASS,
        "whole_packet_nodes_per_pass": WHOLE_PACKET_NODES_PER_PASS,
        "digest": digest,
        "manifest_sha256": hashlib.sha256(
            (OUT / "increments-manifest.json").read_bytes()).hexdigest(),
    }))


HDR_LINES = [
 "# n11 central-reply closure batch-39 (class 30484) 46-LOSS",
 "#   canonical-adoption increment (Part EI, 2026-11-25) - loss-only,",
 "#   fresh increment.  The 46 honest-label exact-LOSS rows aj001..aj050",
 "#   (minus aj030/aj039 EXHAUSTED honest-UNKNOWN, minus aj049/aj050",
 "#   probe-level WIN unconsumed) of the published Part EH batch-39 kit",
 "#   (178 files, MANIFEST-sha256 52b69c04...), two-pass fresh-cold",
 "#   node-exact at the pre-declared 15M budget, order 0; MISMATCH 0.",
 "#   Adopted per-pass node total 140,162,086 of the whole packet",
 "#   177,032,132; the 2 WIN rows and 2 EXHAUSTED rows are consumed",
 "#   NOWHERE (WIN: scrutiny-owner C++ gate 9193f5b6 exclusive; EXH:",
 "#   same-condition re-probe prohibited); the 2 claim-reserved dual-",
 "#   class batch-38 keys (ai044/ai048, Part EF in-flight) untouched.",
 "# Loss-only adoption asserts no root verdict, frees no class,",
 "#   excludes no class; scheduling effects are derived only by the",
 "#   reaudit refresh (Board fail-closed child verification) and the",
 "#   delta extractor.  11x11 stays UNKNOWN; nodes are bookkeeping,",
 "#   never verdicts."
]


if __name__ == "__main__":
    main()
