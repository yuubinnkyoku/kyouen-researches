"""Build the em-b38loss24 (Part EM 24-row loss-only) canonical-adoption
increment, fail-closed.

Part EM (2026-11-25).  BASE = the published Part EL canonical merged chain
head merged-exact-s5-chain-plus-aj039loss1-20261125.cache (6,713 rows, sha
cf08e181...; WIN 158 / LOSS 6,555; the aj039loss1 canonical adoption of
Part EL).  The adopted pool is the published, COMPLETE Part EF batch-38
kit (closure class 30345 rank-12 fresh frontier, 49 fresh never-probed
keys solved two-pass fresh-cold node-exact at budget 15,000,000 order 0,
49/49 resolved, MISMATCH 0, kit MANIFEST-sha256 4dbf8856... fixed by repo
commit 17489a6b after an honestly-recorded transcription incident in
d08a493e, 181 kit files, machine audit batch-audit.json 73652099... all
gates PASS, verdicts_consumed false): exactly the 24 honest-label
exact-LOSS rows ai001..ai045 of that batch (incl. the class-30484
dual-class child ai044, the Part EF completion-log resume route (b),
adopted here for the first time).

NOT consumed by this Part (all sit in NO cache): the 19 probe-level WIN
rows of batch-38 (incl. ai048, the ai044 dual-class sibling, WIN
2,232,854 - WIN canonical adoption is scrutiny-owner C++
second-implementation gate 9193f5b6... exclusive; g++ is unavailable in
this environment and nothing about any WIN is decided here); the 6
EXHAUSTED keys (ai007/ai024/ai030/ai038/ai040/ai041, honest UNKNOWN at
the 15M condition, no same-condition re-probe); the excluded prior batch-1
dual-class key b018 (probe-level WIN 2026-11-22, unconsumable without the
scrutiny-owner C++ gate); the batch-39/EK probe-level WINs aj030/aj049/
aj050.  Every batch-38 key was probed exactly once at its own single 15M
condition (absent from the published prior-probe universe 6deee846...);
there is no exhaustion history and no re-probe anywhere in this pool.

Every gate is fail-closed: any drift aborts with rc=1 and no output is
written.  The published Part EF kit is verified file-by-file (181 byte
pins against the published MANIFEST-sha256), the machine audit
batch-audit.json honesty pins are verified (49 per-key labels/nodes/
timestamps, LOSS 24 / WIN 19 / EXHAUSTED 6 / MISMATCH 0, total nodes
396,892,270/pass), the 81-line status.log is pinned by sha and
line-class accounting, all 49 raw two-pass pairs are parsed and gated
(pass-identical per key, honest-label agreement with the audit), the 24
adopted keys are proven absent from BASE (fresh-increment gate) and from
the quarantine registry and from the published prior-probe universe, and
every unadopted key (19 WIN, 6 EXHAUSTED, b018) is proven absent from
BASE and never emitted.

Loss-only adoption consumes no WIN verdict, asserts no root verdict,
frees no class and excludes no class.  11x11 stays UNKNOWN; nodes are
bookkeeping, never verdicts.
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

EL_EXP = "n11-centralreply-aj039loss1-adoption-reaudit-20261125"
EF_EXP = "n11-centralreply-closure-class30345-batch38-20261125"
BASE_CACHE = ROOT / "research/experiments" / EL_EXP / (
    "output/merged-exact-s5-chain-plus-aj039loss1-20261125.cache")
EF_DIR = ROOT / "research/experiments" / EF_EXP
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"

MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA_EXPECTED = "cf08e1817a369853747706872763046c4544e289eae6d847bfd27d7503d23e7d"
BASE_CACHE_ROWS_EXPECTED = 6713
BASE_CACHE_WIN_EXPECTED = 158
BASE_CACHE_LOSS_EXPECTED = 6555
QUARANTINE_SHA_EXPECTED = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

EF_MANIFEST_SHA = "4dbf8856597709b3bd41d6f185a0502ebbdee447b1fc48d0caab586fdcc5ac02"
EF_KIT_FILES = 181
EF_STATUS_SHA = "8ca390768e317b5fdf810767dbd6e7bc31790d58762701e71759b4883fd8e14f"
EF_AUDIT_SHA = "73652099bcc47ac86b89a790524fb78c353e01c91ddcdc3748b91cfea5b75fdc"
EF_AUDIT_PY_SHA = "f07a162f44452a6a3a529cdb9c38f55a0f0009ed597393e9645326b7ac3d717a"
BATCH_KEYS_SHA = "298071046bfba8473c5b3d6e0b6a30108697eb0899aed7c70fcb4c5343f7cb8d"
PRIOR_UNIVERSE_SHA = "6deee846a4e67778437cd052502535f4839f3fbe76d5e1ec9bc9b6c0036e942b"
CLOSURE_CLASSES_SHA = "27e00b0dbf2f33603dfbed91b00153f73c7a2d05b1258133a39c9ec5bfd41364"
FRESHNESS_SHA = "e5f517177778102d2313da5bb6b46c3084c9a99c11323b750407b0f1919da148"
BUDGET = 15000000

STATUS_LINES = 81
ADOPTED_IDS = [
    "ai001", "ai004", "ai008", "ai009", "ai011", "ai012", "ai015", "ai016",
    "ai018", "ai019", "ai020", "ai021", "ai022", "ai025", "ai026", "ai027",
    "ai029", "ai031", "ai032", "ai033", "ai037", "ai042", "ai044", "ai045"]
WIN_IDS_UNCONSUMED = [
    "ai002", "ai003", "ai005", "ai006", "ai010", "ai013", "ai014", "ai017",
    "ai023", "ai028", "ai034", "ai035", "ai036", "ai039", "ai043", "ai046",
    "ai047", "ai048", "ai049"]
EXHAUSTED_IDS = ["ai007", "ai024", "ai030", "ai038", "ai040", "ai041"]
EXCLUDED_PRIOR_IDS = ["b018"]
ALL_PROBED_IDS = ["ai%03d" % i for i in range(1, 50)]

ADOPTED_NODES_PER_PASS = 168055078
BATCH_TOTAL_NODES_PER_PASS = 396892270

# key (lo, hi, legal, s5_index, probe_order) - machine-derived from the
# published batch-keys-b38.json, cross-gated below against the raw replay rows.
KEY_PINS = {
    "ai001": (1152922604252696576, 65536, 83, 39148, 132),
    "ai002": (1153485554071900160, 65536, 74, 151694, 133),
    "ai003": (3458765613332172800, 65536, 79, 195012, 134),
    "ai004": (5764608622545866752, 65536, 87, 298570, 135),
    "ai005": (1152922604118544384, 65536, 87, 355799, 136),
    "ai006": (1152922604118478848, 65537, 88, 391735, 137),
    "ai007": (1152922604118478880, 65536, 84, 441292, 138),
    "ai008": (1152922604118478848, 65538, 87, 473959, 139),
    "ai009": (1152922741557432320, 65536, 78, 604944, 141),
    "ai010": (1152923153874292736, 65536, 78, 624629, 142),
    "ai011": (1152922604118478848, 66048, 82, 657234, 143),
    "ai012": (1152922604185587712, 65536, 87, 716150, 144),
    "ai013": (1152922604386914304, 65536, 78, 731678, 145),
    "ai014": (1157426203745849344, 65536, 79, 753317, 146),
    "ai015": (1152922604118478848, 66560, 91, 754556, 147),
    "ai016": (1152922604118511616, 65536, 83, 800006, 148),
    "ai017": (1161929803373219840, 65536, 81, 826581, 149),
    "ai018": (1152922604118478848, 67584, 91, 827502, 150),
    "ai019": (1152922604118478912, 65536, 91, 866157, 151),
    "ai020": (1170937002627960832, 65536, 87, 878758, 152),
    "ai021": (1152922604118478848, 69632, 78, 879412, 153),
    "ai022": (1152922604118479360, 65536, 90, 888325, 154),
    "ai023": (1152922604120576000, 65536, 85, 888357, 155),
    "ai024": (1152922604118479104, 65536, 86, 889534, 156),
    "ai025": (1152922608413446144, 65536, 90, 889976, 157),
    "ai026": (1152922604118478976, 65536, 87, 891015, 158),
    "ai027": (1152931400211501056, 65536, 85, 891592, 159),
    "ai028": (1152921573327372288, 1056768, 76, 892997, 160),
    "ai029": (1152922604118478852, 65536, 89, 893644, 161),
    "ai030": (1152921573327372288, 17825792, 91, 894456, 162),
    "ai031": (1152922604118478850, 65536, 84, 894824, 163),
    "ai032": (1152921573327372288, 34360786944, 89, 895608, 164),
    "ai033": (1152922604118478849, 65536, 80, 895907, 165),
    "ai034": (1152921573326324736, 68720525312, 74, 896605, 166),
    "ai035": (1152922672837955584, 65536, 84, 897030, 167),
    "ai036": (1152922604119003136, 65536, 82, 897221, 168),
    "ai037": (1152922606265962496, 65536, 89, 897427, 169),
    "ai038": (1152927002164989952, 65536, 89, 898436, 170),
    "ai039": (1152921573327372288, 1064960, 87, 899303, 171),
    "ai040": (1152922604118487040, 65536, 85, 899584, 172),
    "ai041": (1152921573327372288, 34603008, 91, 900170, 173),
    "ai042": (1152922604655349760, 65536, 86, 900292, 174),
    "ai043": (1152922604152033280, 65536, 74, 900322, 175),
    "ai044": (1152922604135256064, 65536, 72, 900354, 176),
    "ai045": (1152924803141734400, 65536, 86, 900436, 177),
    "ai046": (1152921573327372288, 1081344, 80, 900561, 178),
    "ai047": (1152921573327372288, 1114112, 82, 900716, 179),
    "ai048": (1152921573327372288, 68157440, 68, 900718, 180),
    "ai049": (1152921573327372288, 68720525312, 72, 900719, 181),
}

# (result, nodes, ts) - machine-derived from the published batch-audit.json
# per_key array; cross-gated below against the raw replay pairs, the
# status.log verdict rows and the audit SSOT itself.
LABEL_PINS = {
    "ai001": (2, 10528977, "2026-11-25T07:13:18Z"),
    "ai002": (1, 3552766, "2026-11-25T07:11:52Z"),
    "ai003": (1, 5682652, "2026-11-25T07:15:11Z"),
    "ai004": (2, 4352970, "2026-11-25T07:14:55Z"),
    "ai005": (1, 11770537, "2026-11-25T07:19:06Z"),
    "ai006": (1, 8819998, "2026-11-25T07:18:25Z"),
    "ai007": (0, 15000000, "2026-11-25T07:22:45Z"),
    "ai008": (2, 3221447, "2026-11-25T07:20:32Z"),
    "ai009": (2, 7514829, "2026-11-25T07:26:06Z"),
    "ai010": (1, 13066796, "2026-11-25T07:27:07Z"),
    "ai011": (2, 6715814, "2026-11-25T07:29:29Z"),
    "ai012": (2, 4767152, "2026-11-25T07:29:04Z"),
    "ai013": (1, 10255279, "2026-11-25T07:33:40Z"),
    "ai014": (1, 14969659, "2026-11-25T07:36:10Z"),
    "ai015": (2, 3086764, "2026-11-25T07:35:20Z"),
    "ai016": (2, 3496190, "2026-11-25T07:37:29Z"),
    "ai017": (1, 8468415, "2026-11-25T07:38:24Z"),
    "ai018": (2, 6236845, "2026-11-25T07:49:04Z"),
    "ai019": (2, 4269857, "2026-11-25T07:48:43Z"),
    "ai020": (2, 9007508, "2026-11-25T07:52:10Z"),
    "ai021": (2, 6190420, "2026-11-25T07:51:36Z"),
    "ai022": (2, 7405631, "2026-11-25T07:55:32Z"),
    "ai023": (1, 13676098, "2026-11-25T07:56:45Z"),
    "ai024": (0, 15000000, "2026-11-25T08:04:29Z"),
    "ai025": (2, 9392986, "2026-11-25T08:00:41Z"),
    "ai026": (2, 9199731, "2026-11-25T08:04:50Z"),
    "ai027": (2, 10234914, "2026-11-25T08:07:51Z"),
    "ai028": (1, 4892185, "2026-11-25T08:06:48Z"),
    "ai029": (2, 12001061, "2026-11-25T08:15:12Z"),
    "ai030": (0, 15000000, "2026-11-25T08:15:33Z"),
    "ai031": (2, 4148336, "2026-11-25T08:17:18Z"),
    "ai032": (2, 11928171, "2026-11-25T08:18:51Z"),
    "ai033": (2, 4181137, "2026-11-25T08:20:53Z"),
    "ai034": (1, 3087464, "2026-11-25T08:20:38Z"),
    "ai035": (1, 4227036, "2026-11-25T08:22:30Z"),
    "ai036": (1, 8137160, "2026-11-25T08:23:16Z"),
    "ai037": (2, 7709821, "2026-11-25T08:26:44Z"),
    "ai038": (0, 15000000, "2026-11-25T08:31:24Z"),
    "ai039": (1, 13065437, "2026-11-25T08:32:25Z"),
    "ai040": (0, 15000000, "2026-11-25T08:40:16Z"),
    "ai041": (0, 15000000, "2026-11-25T08:40:16Z"),
    "ai042": (2, 9086966, "2026-11-25T08:43:00Z"),
    "ai043": (1, 3897909, "2026-11-25T08:41:55Z"),
    "ai044": (2, 5677449, "2026-11-25T15:19:27Z"),
    "ai045": (2, 7700102, "2026-11-25T15:19:49Z"),
    "ai046": (1, 5256793, "2026-11-25T15:21:18Z"),
    "ai047": (1, 2946085, "2026-11-25T15:20:51Z"),
    "ai048": (1, 2232854, "2026-11-25T15:21:51Z"),
    "ai049": (1, 832069, "2026-11-25T15:21:37Z"),
}

# the excluded prior batch-1 dual-class key (probe-level WIN 2026-11-22)
B018_PIN = {
    "lo": 1153204079095189504, "hi": 65536, "legal": 60, "s5_index": 528497,
    "probe_order": 140, "budget_result_nodes": "15000000,1,3549602"}

RAW_SHAS = {
    "ai001.p1.out": "be33d440a1a7123b13d7e772d3f3cd2360131619b8d48ef052c763b0806d6c83",
    "ai001.p2.out": "8835c1b8a49e952b2af73b15767f5083731b6d527abc6a553d9c3afccefa92f6",
    "ai004.p1.out": "bb2a29f2c3a32bf2663c2c100b361def934596faadcf699137e506d0eb3eb1dc",
    "ai004.p2.out": "d584b9bc5b8d710ad718e8fbfb8665b615a512f76ecd6e22cec13c1c4759f3d3",
    "ai008.p1.out": "02f2d83cf948eaf4656df0aa7ade1a7e217fea4b683ee531c749a4fe7e79b0a1",
    "ai008.p2.out": "02640ad870d260f603f683566db817ec381d1246233d898b76bba8ace7f6e80d",
    "ai009.p1.out": "b88e0253d1fcf669a366390b632a1174ff18346d7d1cf188c5ffaf2fd50b9e4f",
    "ai009.p2.out": "7be09faf7dd8a042b578dfd990f0a686977bb422cf6a8291f82c1542747ce8e7",
    "ai011.p1.out": "acb67399644bd2e289d646d2b8529885925f8708bd4bcc7fdfcbbee14d079c37",
    "ai011.p2.out": "d0a56512583ca2209961e07358a511fc33ad775d99133bce9330c684d043d69e",
    "ai012.p1.out": "4206753c451aa1c6ffeb122c8337788ccac230d454ca3c75b9a6ffcb66bbca24",
    "ai012.p2.out": "4206753c451aa1c6ffeb122c8337788ccac230d454ca3c75b9a6ffcb66bbca24",
    "ai015.p1.out": "149419ea25d4fc1cbc739a475ec4a4ba4c89fd8e4d2ee5b313ae95d5629e1b44",
    "ai015.p2.out": "67233a5d0609a3b1bd41e0897a382655586cfc1ce186763becf3074db29621ca",
    "ai016.p1.out": "c9483305afea9d5c2c93763ac458fee5c8dfc67520e416f84a845a0d8d8a24e5",
    "ai016.p2.out": "0f257bc75d5a7fa74d167e59a1e5edfd792a43ab6f5c0f48cdbd9cd2c0d1f807",
    "ai018.p1.out": "6e9fe01007595c45cb2efb05c6eeaf8ab77910da11a1dbc57d8cd5e6ead373e4",
    "ai018.p2.out": "8d5d89f3b5b46ebd6ce95accdb79a16d8a29b4b8a717d8ae69a7a048f24a1047",
    "ai019.p1.out": "dc4fbe6727732a9e35b04f0153451dad3b1e6c1d22f4577d1cecb5116bd215cd",
    "ai019.p2.out": "1432b02ea65f90c023c8af7a42deb801b20f3edb8bbb81e0ee54942c83c0fbc1",
    "ai020.p1.out": "6bbfee32a08a7b4b78b97e3af3e21e0d0ad00926cf644f2622c9e970e6d6056f",
    "ai020.p2.out": "0c9318bc9828d8d76d225779e6dc8f5e30a6bd497ad69f7d0b0837854df49c84",
    "ai021.p1.out": "d2addcbf44980467aa2b9961f0da83976ced54fafd6022c7d1d506df6d86691f",
    "ai021.p2.out": "ddc2d4a693ad82470464c5e1d409c1fdcbdf3eed4be1d11ba001d0a3aed2e4dc",
    "ai022.p1.out": "56f0d5990a76e1aad743cac43332d68faa8b5c03b8b14e148855bea7859ff334",
    "ai022.p2.out": "566d0879432b35312fb9bc2be620b6aae8c2074fb5c6582f989406fe2892c579",
    "ai025.p1.out": "f134444f510a18ddc46c2b2cbfdd89b83a5c8ba5ccb42cc6baa5f0f33323cb37",
    "ai025.p2.out": "bfe8da28b74f4ee79d5bb6915d7fb4e4ea3294906d97af836c8fc438c5bc3491",
    "ai026.p1.out": "037fbf9f7714a92c7e5451c05d2d6767b35953962381b2efffc67aef4955fec4",
    "ai026.p2.out": "37a07becbfb1ad46d9b919d1e49664852db48dc1e44ae0c9f1dd916b27e72db4",
    "ai027.p1.out": "88e425834649a3b1f3ab9ad7cee312ced210a5b45ee081807b7ca98c65bdf558",
    "ai027.p2.out": "7fee6064ccdc416b676dde4c21dc53f20269d1eae1b6eba7784a5e41ff2fc8d1",
    "ai029.p1.out": "a8a6140eb6f32bebad3fb406617e077ae9d9a08ab8312729e0b333e3e3299eaa",
    "ai029.p2.out": "a8a6140eb6f32bebad3fb406617e077ae9d9a08ab8312729e0b333e3e3299eaa",
    "ai031.p1.out": "27cc5c3d96ff58c6a77a72010861452faa6e094576adf32a8436a22e9ad69210",
    "ai031.p2.out": "27cc5c3d96ff58c6a77a72010861452faa6e094576adf32a8436a22e9ad69210",
    "ai032.p1.out": "f309b62e4c19a25fa404d5739c3b6b1a4918b94caea1078634fad663699ab4af",
    "ai032.p2.out": "e3318cbf0c6ec3496555e9c45b061fc7c2998d7f808d3713492a5420aee1e9ca",
    "ai033.p1.out": "c4fc1c2f510bcfe3d3e7b6b6ff394b1223dee06cd7f6588af33ddba270f597ca",
    "ai033.p2.out": "61b3b15296f6ecc3bf158fd57a52f3444f0c3fd670abb74b7a7b756734aef1ad",
    "ai037.p1.out": "132d6abb6730ef994fb603b332c9ace5536882e5a967fefb8f608e75890016e8",
    "ai037.p2.out": "132d6abb6730ef994fb603b332c9ace5536882e5a967fefb8f608e75890016e8",
    "ai042.p1.out": "ad99270756ba712e06510df60357f3ab789381fca3d5a1b1cd7190d338053a55",
    "ai042.p2.out": "b86925c97cbc014a3a4e15550546ed61be96f0e24500a72904bcbaac75f264b5",
    "ai044.p1.out": "e7454d4dc06c70d922a20f9777a17532c425c177868472a69868ba59d2de3b8e",
    "ai044.p2.out": "9bad79257e3419753799b2d7fb1246667f5c1db6717786428c998085b4d35682",
    "ai045.p1.out": "4c3b67f79a88ab99d723dec313fee39631856a061d5ed3a50798e8eadac26303",
    "ai045.p2.out": "2474c2095a6a6b79193977551de45c3ac87ed77c166c0e36bdad7775e2df4dd2",
}

INPUT_CSV_SHAS = {
    "ai001": "90a132fa72a4d357b6a4fb3137e3b6b09ecd5acd0ab36f43c0b6a5d2435d3fca",
    "ai004": "22df405ee0aeccc164b91dc5b467714ef4921434ecd6ad95605c283ba84102cd",
    "ai008": "c2e7455cb2a474dedcb5a21dc093badffafcfdc474e1ac1782281de87bd71ae5",
    "ai009": "71d6f6e206be8e143e9776d256ac57e46ad65bea07f4978c75c0aeff0e038188",
    "ai011": "c9516e730bbd979001ad4ee4168f57c4e6f37ad03ca78bd112cfb416a70a0ca6",
    "ai012": "c7f4ffb3b3d34b063c8d4678187ccdb58f705c2c7b733d2c0f13473d9db7c57b",
    "ai015": "27b1e678f0cd63489abd4fa4d4260c009ecf3a4e244686f802002af7d7701b64",
    "ai016": "f061e58c99f1839d15a27d15c9b00575527790b08c4303d3131f6e1fb8e444fd",
    "ai018": "2238776a8b8fd1f5202072bdc478b1affe86cf5227a7c1a852e785373441379b",
    "ai019": "69ebd32b8e1bee2c2ac57e06bdd46d705e74dec5afca8a8565a2a35a601a81d5",
    "ai020": "ea9a64c09a600d6e9be506241e42b06370ef52038e1f95bd9f0f78785ec1138e",
    "ai021": "345abf18dcc01b39bc00a06be5eed2253a2299d5cfce33b833844536f0c72785",
    "ai022": "432e47ab5443dcca621e3c121e0f22486277509609a9e61e676482ce2f812b56",
    "ai025": "ed5d0e9c432995e99d668031e765cd9158bdbc13b2488a315e6a2ec599c65ca1",
    "ai026": "beb9abed74dfddb902aff470e92b2dee8e8e0b4da6bdfc5b3524b3b4360b751e",
    "ai027": "a09e52e5cf64bbd1e65b83196d6e86ae3e5155a5dab030faf956c21b30fa8a29",
    "ai029": "ddca9b4260a7adfd68ef5351c45de3ddfc28f1c4dc389554854a18996aed8876",
    "ai031": "a5dacf1ff20f6f72f84c3645b9d187a3c8ee15e38b37c0d87b2d339a8205ccf4",
    "ai032": "644c8395a0868bdb23a7cfb17793d94060f588d0aa58d86fbee01c25f119d8bd",
    "ai033": "a68ea1e98bc63e219f5d757cb4b81f07a43756b0e473caa18fbddee17953c5ba",
    "ai037": "8cfe8d3dddf734c6ffb3fdb8b0837b98f3c4307e0b871f98bb3ce03edbc81236",
    "ai042": "e54332cab4916d49b5e65f68e31d7247e2efc2697bc936c99033254f78199a60",
    "ai044": "87fd94e0ef4108469df3a41d5cd28c6f3a26c5aacf1e9855942d2e8a8a4b7bf2",
    "ai045": "98f20b211c3dd31c8ca29b539445eeacd50084f9d653fe0676388aa86c5724b3",
}

ADOPTED_TABLE_DIGEST = "a56b1cdef65f0b311b1ae04e90023204f8bb85e9f0a3852f6007a0b42f9b12dc"
ADOPTED_INCREMENT_SHA = "3c6326618944b4c18d37e1fe6cad470b53e712592fe7a19d7190f44f5a26bed4"

INCREMENT_NAME = "increment-b38loss24-20261125.cache"
EM_SCHEMA = "em-b38loss24-increments-manifest-v1"

HDR_LINES = [
 "# n11 central-reply closure class 30345 b38loss24",
 "#   canonical-adoption increment (Part EM, 2026-11-25) - loss-only,",
 "#   fresh 24-row increment.  The 24 honest-label exact-LOSS rows of the",
 "#   published Part EF batch-38 kit (49 fresh never-probed keys of closure",
 "#   class 30345 solved two-pass fresh-cold node-exact at budget 15,000,000",
 "#   order 0, 49/49 resolved, MISMATCH 0, total nodes 396,892,270/pass;",
 "#   MANIFEST-sha256 4dbf8856..., 181 kit files, batch-audit.json",
 "#   73652099... all gates PASS): every first-ever probe resolved within",
 "#   its own 15M condition (no same-condition re-probe anywhere; the 6",
 "#   EXHAUSTED keys remain honest UNKNOWN, not adopted).  Included is the",
 "#   class-30484 dual-class claim-reserved child ai044 (key",
 "#   1152922604135256064,65536, legal 72, nodes 5,677,449), the EF",
 "#   measured-LOSS route to shrink class 30484's unknown children (the",
 "#   Part EF completion log resume note (b); its WIN sibling ai048 stays",
 "#   unconsumed, scrutiny-owner C++ second-implementation gate",
 "#   9193f5b6... exclusive).  The 19 probe-level WIN rows, the 6 EXHAUSTED",
 "#   rows and the excluded prior batch-1 dual-class key b018 are NOT",
 "#   consumed and sit in NO cache.",
 "# Loss-only adoption asserts no root verdict, frees no class,",
 "#   excludes no class; scheduling effects are derived only by the",
 "#   reaudit refresh (Board fail-closed child verification) and the",
 "#   delta extractor.  11x11 stays UNKNOWN; nodes are bookkeeping,",
 "#   never verdicts.",
]


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


def two_pass(raw_dir: Path, kid: str, budget: int, pins: dict):
    variants = {}
    for tag in ("p1", "p2"):
        p = raw_dir / f"{kid}.{tag}.out"
        if not p.is_file():
            sys_exit(f"missing raw {p}")
        if pins is not None:
            want = pins[f"{kid}.{tag}.out"]
            if sha(p) != want:
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
    if ref["budget"] != budget:
        sys_exit(f"{kid}: budget drift (expected {budget})")
    return ref


def verify_ef_kit():
    if not EF_DIR.is_dir():
        sys_exit(f"kit dir missing {EF_DIR}")
    if sha(EF_DIR / "MANIFEST-sha256.txt") != EF_MANIFEST_SHA:
        sys_exit("Part EF kit MANIFEST sha drift (expected the 17489a6b fixed bytes)")
    verified = 0
    for line in (EF_DIR / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split("  ")
        if len(fields) != 3:
            sys_exit(f"Part EF MANIFEST malformed line: {line}")
        want, size, rel = fields[0], int(fields[1]), fields[2]
        if rel.startswith("/") or ".." in rel.split("/"):
            sys_exit(f"Part EF MANIFEST unsafe path: {rel}")
        if ".." in rel or "\x00" in rel:
            sys_exit(f"Part EF MANIFEST unsafe path: {rel}")
        p = EF_DIR / rel
        if not p.is_file():
            sys_exit(f"Part EF kit file missing: {rel}")
        if p.stat().st_size != size:
            sys_exit(f"Part EF kit file size drift: {rel}")
        if sha(p) != want:
            sys_exit(f"Part EF kit file sha drift: {rel}")
        verified += 1
    if verified != EF_KIT_FILES:
        sys_exit(f"Part EF kit files verified {verified} != {EF_KIT_FILES}")
    return verified


def main() -> None:
    # --- anchors: base cache, merger, quarantine ----------------------------
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys_exit("base cache (Part EL canonical) sha drift")
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

    # --- G-kit: the published Part EF kit is verified file-by-file ----------
    kit_files = verify_ef_kit()
    if sha(EF_DIR / "input/batch-keys-b38.json") != BATCH_KEYS_SHA:
        sys_exit("batch-keys-b38.json sha drift")
    if sha(EF_DIR / "sources/prior-probe-universe.csv") != PRIOR_UNIVERSE_SHA:
        sys_exit("prior-probe-universe.csv sha drift")
    if sha(EF_DIR / "sources/closure-classes.csv") != CLOSURE_CLASSES_SHA:
        sys_exit("closure-classes.csv sha drift")
    if sha(EF_DIR / "sources/freshness-ranks1to12.csv") != FRESHNESS_SHA:
        sys_exit("freshness-ranks1to12.csv sha drift")
    if sha(EF_DIR / "output/status.log") != EF_STATUS_SHA:
        sys_exit("Part EF status.log sha drift")
    if sha(EF_DIR / "output/batch-audit.json") != EF_AUDIT_SHA:
        sys_exit("Part EF batch-audit.json sha drift")
    if sha(EF_DIR / "scripts/audit_b38.py") != EF_AUDIT_PY_SHA:
        sys_exit("Part EF audit_b38.py sha drift")

    # --- G-keys: batch-keys json vs pinned key fields ------------------------
    bk = json.loads((EF_DIR / "input/batch-keys-b38.json").read_text())
    if bk["schema"] != "n11-centralreply-closure-batch38-keys-v1":
        sys_exit("batch-keys schema drift")
    if bk["target_key_count"] != 49 or len(bk["keys"]) != 49:
        sys_exit("batch-keys target accounting drift")
    for k in bk["keys"]:
        kid = k["key_id"]
        lo, hi, legal, s5_index, probe_order = KEY_PINS[kid]
        if (k["hi"] != hi or k["legal"] != legal or k["s5_index"] != s5_index
                or k["probe_order"] != probe_order or k["lo"] != lo):
            sys_exit(f"batch-keys key field drift: {kid}")
        if k["class_mask"] != [1152922604118478848, 65536]:
            sys_exit(f"batch-keys class-mask drift: {kid}")
        if k["serving_class"] != 30345:
            sys_exit(f"batch-keys serving-class drift: {kid}")
    if sorted(KEY_PINS) != ALL_PROBED_IDS:
        sys_exit("batch-keys key-id set drift")
    if len(bk["prior_packeted_excluded"]) != 1:
        sys_exit("batch-keys prior_packeted_excluded accounting drift")
    b018 = bk["prior_packeted_excluded"][0]
    if (b018["key_id"] != "b018"
            or b018["lo"] != B018_PIN["lo"] or b018["hi"] != B018_PIN["hi"]
            or b018["legal"] != B018_PIN["legal"]
            or b018["s5_index"] != B018_PIN["s5_index"]
            or b018["probe_order"] != B018_PIN["probe_order"]
            or b018["budget_result_nodes"] != B018_PIN["budget_result_nodes"]):
        sys_exit("batch-keys prior_packeted_excluded b018 pin drift")

    # --- G-SSOT: batch-audit.json honesty pins ------------------------------
    audit = json.loads((EF_DIR / "output/batch-audit.json").read_text())
    if audit["schema"] != "n11-centralreply-closure-batch38-audit-v1":
        sys_exit("Part EF audit schema drift")
    if audit["batch_keys_b38_sha256"] != BATCH_KEYS_SHA:
        sys_exit("Part EF audit batch-keys pin drift")
    if audit["verdicts_consumed_into_canonical_cache"] is not False:
        sys_exit("Part EF audit verdicts_consumed must be false")
    res = audit["results"]
    if res["LOSS"] != 24 or res["WIN"] != 19 or res["EXHAUSTED"] != 6 or res["MISMATCH"] != 0:
        sys_exit("Part EF audit results accounting drift (expected 24/19/6/0)")
    if sorted(res["exhausted_keys_honest_unknown"]) != sorted(EXHAUSTED_IDS):
        sys_exit("Part EF audit exhausted-keys drift")
    if res["class_30484_dual_class_children"]["ai044"] != (
            "LOSS 5677449 (unconsumed honest label; future loss-only adoption candidate)"):
        sys_exit("Part EF audit ai044 dual-class label drift")
    if res["class_30484_dual_class_children"]["ai048"] != (
            "WIN 2232854 (unconsumed; scrutiny-owner C++ gate exclusive)"):
        sys_exit("Part EF audit ai048 dual-class label drift")
    per_key = {e["key_id"]: e for e in audit["per_key"]}
    if sorted(per_key) != ALL_PROBED_IDS:
        sys_exit("Part EF audit per_key set drift")
    total_nodes = 0
    for kid in ALL_PROBED_IDS:
        e = per_key[kid]
        r, n, ts = LABEL_PINS[kid]
        if e["result"] != r or e["nodes"] != n or e["ts"] != ts:
            sys_exit(f"Part EF audit per_key label drift: {kid}")
        if e["budget"] != BUDGET:
            sys_exit(f"Part EF audit per_key budget drift: {kid}")
        lo, hi, legal, s5_index, probe_order = KEY_PINS[kid]
        if e["probe_order"] != probe_order:
            sys_exit(f"Part EF audit per_key probe_order drift: {kid}")
        total_nodes += n
    if total_nodes != BATCH_TOTAL_NODES_PER_PASS:
        sys_exit(f"Part EF audit total nodes {total_nodes} != {BATCH_TOTAL_NODES_PER_PASS}")
    if sorted(k for k in per_key if per_key[k]["result"] == 2) != sorted(ADOPTED_IDS):
        sys_exit("Part EF audit LOSS set != the 24 adopted ids")
    if sorted(k for k in per_key if per_key[k]["result"] == 1) != sorted(WIN_IDS_UNCONSUMED):
        sys_exit("Part EF audit WIN set != the 19 unconsumed win ids")
    if sorted(k for k in per_key if per_key[k]["result"] == 0) != sorted(EXHAUSTED_IDS):
        sys_exit("Part EF audit EXHAUSTED set drift")

    # --- G-status: the 81-line honest status -------------------------------
    lines = (EF_DIR / "output/status.log").read_text().splitlines()
    if len(lines) != STATUS_LINES:
        sys_exit(f"status.log lines {len(lines)} != {STATUS_LINES}")
    pass_lines = [l for l in lines if " PASS " in l]
    halt_lines = [l for l in lines if "WIN-HALT" in l]
    exh_lines = [l for l in lines if " EXHAUSTED " in l]
    retr_lines = [l for l in lines if "P2-TRUNCATED-RETRY" in l]
    if len(pass_lines) != 49 or len(halt_lines) != 19 or len(exh_lines) != 6 or len(retr_lines) != 7:
        sys_exit(f"status line-class accounting drift "
                 f"{len(pass_lines)}/{len(halt_lines)}/{len(exh_lines)}/{len(retr_lines)}")
    got_pass = {}
    for line in pass_lines:
        parts = line.split()
        kid = parts[1]
        if kid in got_pass:
            sys_exit(f"duplicate status verdict row for {kid}")
        b, r, n = parts[3].split(",")
        got_pass[kid] = (int(b), int(r), int(n))
    if sorted(got_pass) != ALL_PROBED_IDS:
        sys_exit("status PASS keys != the 49 batch-38 targets")
    for kid in ALL_PROBED_IDS:
        r, n, ts = LABEL_PINS[kid]
        if got_pass[kid] != (BUDGET, r, n):
            sys_exit(f"{kid} status verdict vs pinned honest label drift")
        if f"{ts} {kid} PASS {BUDGET},{r},{n}" not in lines:
            sys_exit(f"{kid} status verdict row timestamp/label drift")
    for kid in ALL_PROBED_IDS:
        if per_key[kid]["ts"] != LABEL_PINS[kid][2]:
            sys_exit(f"{kid} audit-ts vs LABEL_PINS timestamp drift")
    if sorted(l.split()[1] for l in halt_lines) != sorted(WIN_IDS_UNCONSUMED):
        sys_exit("status WIN-HALT keys != the 19 probe-level WINs")
    if sorted(l.split()[1] for l in exh_lines) != sorted(EXHAUSTED_IDS):
        sys_exit("status EXHAUSTED keys drift")

    # --- G-raw: all 49 two-pass pairs (fresh-cold node-exact) ---------------
    raws = {}
    for kid in ALL_PROBED_IDS:
        pins = RAW_SHAS if kid in ADOPTED_IDS else None
        ref = two_pass(EF_DIR / "output/raw", kid, BUDGET, pins)
        lo, hi, legal, s5_index, probe_order = KEY_PINS[kid]
        if ref["stones"] != 5 or ref["is_or"] != 0:
            sys_exit(f"{kid}: wrong depth/or bit")
        if ref["legal"] != legal or ref["lo"] != str(lo) or ref["hi"] != str(hi):
            sys_exit(f"{kid}: legal/key disagreement raw vs pinned key fields")
        if (ref["budget"], ref["result"], ref["nodes"]) != got_pass[kid]:
            sys_exit(f"{kid}: raw (budget,result,nodes) row != status verdict row")
        if (ref["result"], ref["nodes"]) != (LABEL_PINS[kid][0], LABEL_PINS[kid][1]):
            sys_exit(f"{kid}: raw honest-label drift vs the pinned audit label")
        raws[kid] = ref
    loss_set = sorted(k for k in raws if raws[k]["result"] == 2)
    win_set = sorted(k for k in raws if raws[k]["result"] == 1)
    exh_set = sorted(k for k in raws if raws[k]["result"] == 0)
    if loss_set != sorted(ADOPTED_IDS):
        sys_exit(f"15M exact-LOSS set drift: {loss_set}")
    if win_set != sorted(WIN_IDS_UNCONSUMED):
        sys_exit(f"15M probe-level WIN set drift: {win_set}")
    if exh_set != sorted(EXHAUSTED_IDS):
        sys_exit(f"15M EXHAUSTED set drift: {exh_set}")
    n_total = sum(raws[k]["nodes"] for k in ALL_PROBED_IDS)
    if n_total != BATCH_TOTAL_NODES_PER_PASS:
        sys_exit(f"whole-batch node total drift {n_total} != {BATCH_TOTAL_NODES_PER_PASS}")
    n_adopted = sum(raws[k]["nodes"] for k in ADOPTED_IDS)
    if n_adopted != ADOPTED_NODES_PER_PASS:
        sys_exit(f"adopted node total drift {n_adopted} != {ADOPTED_NODES_PER_PASS}")

    # --- G-input: byte-pinned 1-line input rows for the adopted keys --------
    for kid in ADOPTED_IDS:
        p_in = EF_DIR / f"input/{kid}.input.csv"
        if sha(p_in) != INPUT_CSV_SHAS[kid]:
            sys_exit(f"input csv {kid} sha drift vs the pinned published bytes")
        lo, hi, legal, s5_index, probe_order = KEY_PINS[kid]
        want_line = f"target,0,5,{lo},{hi},{legal},0,0,0,0,0"
        rows_in = [l for l in p_in.read_text().splitlines() if l.strip()]
        if rows_in != [want_line]:
            sys_exit(f"input csv {kid} body drift: {rows_in}")

    # --- G-selection: closure table + freshness pins -----------------------
    cc = {}
    with (EF_DIR / "sources/closure-classes.csv").open(newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0] == "class_rank":
                continue
            cc[(int(row[2]), int(row[3]))] = row
    row30345 = cc[(1152922604118478848, 65536)]
    if int(row30345[0]) != 12 or int(row30345[1]) != 30345 or int(row30345[4]) != 50:
        sys_exit("closure-classes rank-12 class 30345 unknown_now 50 selection drift")

    # --- freshness: prior-probe universe / BASE / quarantine ----------------
    prior_pairs = set()
    with (EF_DIR / "sources/prior-probe-universe.csv").open(newline="") as stream:
        for row in csv.reader(stream):
            if not row or len(row) < 2 or row[0] in ("lo", "hi"):
                continue
            try:
                prior_pairs.add((int(row[0]), int(row[1])))
            except ValueError:
                continue
    if len(prior_pairs) != 2104:
        sys_exit(f"prior-probe universe pairs {len(prior_pairs)} != 2104")
    for kid in ALL_PROBED_IDS:
        lo, hi, legal, s5_index, probe_order = KEY_PINS[kid]
        key = (lo, hi)
        if key in quarantined:
            sys_exit(f"{kid}: quarantined key {key}")
        if key in base_keys:
            sys_exit(f"{kid}: key already in canonical BASE; fresh-increment gate")
        if kid in ADOPTED_IDS and key in prior_pairs:
            sys_exit(f"{kid}: adopted key IS in the published prior-probe universe "
                     f"(first-ever-probe gate)")
    if (B018_PIN["lo"], B018_PIN["hi"]) in base_keys:
        sys_exit("the excluded prior WIN key b018 must sit in NO cache (BASE)")
    if (B018_PIN["lo"], B018_PIN["hi"]) in quarantined:
        sys_exit("b018 quarantine drift")
    adopted_pairs = set()
    for kid in ADOPTED_IDS:
        lo, hi, legal, s5_index, probe_order = KEY_PINS[kid]
        adopted_pairs.add((lo, hi))
    for kid in WIN_IDS_UNCONSUMED + EXHAUSTED_IDS:
        lo, hi, legal, s5_index, probe_order = KEY_PINS[kid]
        if (lo, hi) in adopted_pairs:
            sys_exit(f"unadopted key {kid} collides with an adopted pair")
    if len(adopted_pairs) != 24:
        sys_exit("adopted pairs must be exactly 24 distinct keys")

    adopted_rows = []
    for kid in ADOPTED_IDS:
        lo, hi, legal, s5_index, probe_order = KEY_PINS[kid]
        adopted_rows.append((lo, hi, legal, 2, LABEL_PINS[kid][1]))
    if len(adopted_rows) != 24 or any(r[3] != 2 for r in adopted_rows):
        sys_exit("adopted rows must be exactly the 24 fresh exact-LOSS rows")
    digest = hashlib.sha256("\n".join(
        f"{lo},{hi},{legal},{result},{nodes}"
        for lo, hi, legal, result, nodes in sorted(adopted_rows)).encode()).hexdigest()
    if digest != ADOPTED_TABLE_DIGEST:
        sys_exit(f"adopted-table digest drift {digest}")

    # --- emit increment + manifest -------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    rowlines = [f"s5verdict,{r[0]},{r[1]},5,2,{r[2]}"
                for r in sorted((lo, hi, nodes)
                                 for lo, hi, legal, result, nodes in adopted_rows)]
    if len(rowlines) != 24:
        sys_exit("emitted row count drift")
    blob = ("\n".join(HDR_LINES + rowlines) + "\n").encode("utf-8")
    incr_sha = hashlib.sha256(blob).hexdigest()
    if incr_sha != ADOPTED_INCREMENT_SHA:
        sys_exit(f"emitted increment sha drift {incr_sha} != pinned {ADOPTED_INCREMENT_SHA}")
    (OUT / INCREMENT_NAME).write_bytes(blob)

    adopted_table = [
        {"lo": lo, "hi": hi, "legal": legal, "result": 2, "nodes": nodes}
        for lo, hi, legal, result, nodes in sorted(adopted_rows)]

    manifest = {
        "schema": EM_SCHEMA,
        "batches": [
            {"pool": "ef-b38loss24",
             "adopted_loss_ids": list(ADOPTED_IDS),
             "unadopted_win_ids": list(WIN_IDS_UNCONSUMED),
             "exhausted_honest_unknown_ids": list(EXHAUSTED_IDS),
             "excluded_prior_ids": list(EXCLUDED_PRIOR_IDS),
             "adopted_nodes_per_pool": ADOPTED_NODES_PER_PASS,
             "batch_total_nodes_per_pass": BATCH_TOTAL_NODES_PER_PASS,
             "status_log_sha256": EF_STATUS_SHA,
             "status_log_lines": STATUS_LINES,
             "status_log_first_line": (EF_DIR / "output/status.log")
                 .read_text().splitlines()[0],
             "status_log_final_line": (EF_DIR / "output/status.log")
                 .read_text().splitlines()[-1],
             "probed_budget": BUDGET,
             "b018_prior_win_pin": dict(B018_PIN),
             "kit_integrity": {
                 "kit_manifest_sha256": EF_MANIFEST_SHA,
                 "kit_files_verified": kit_files,
                 "raw_file_sha256_pins": RAW_SHAS,
                 "input_csv_sha256_pins": INPUT_CSV_SHAS,
                 "audit_b38_json_sha256": EF_AUDIT_SHA,
                 "audit_b38_py_sha256": EF_AUDIT_PY_SHA,
                 "batch_keys_sha256": BATCH_KEYS_SHA,
                 "prior_probe_universe_sha256": PRIOR_UNIVERSE_SHA,
                 "closure_classes_sha256": CLOSURE_CLASSES_SHA,
                 "freshness_sha256": FRESHNESS_SHA,
                 "note": "the Part EF kit is PUBLISHED (181 files, byte-pinned "
                         "above; MANIFEST-sha256 4dbf8856... as fixed by repo "
                         "commit 17489a6b); all 24 adopted keys are fresh at "
                         "BASE (first-ever probes, absent from the published "
                         "prior-probe universe) and absent from the "
                         "quarantine registry; the 19 probe-level WIN rows "
                         "(incl. the ai044 dual-class sibling ai048), the 6 "
                         "EXHAUSTED honest-UNKNOWN keys and the excluded "
                         "prior b018 are NOT consumed"},
             },
        ],
        "resolved_ids": list(ADOPTED_IDS),
        "loss_ids": list(ADOPTED_IDS),
        "win_ids": list(WIN_IDS_UNCONSUMED),
        "unadopted_win_ids": list(WIN_IDS_UNCONSUMED),
        "unadopted_win_rows": [
            {"lo": KEY_PINS[k][0], "hi": KEY_PINS[k][1],
             "legal": KEY_PINS[k][2], "result": 1, "nodes": LABEL_PINS[k][1]}
            for k in WIN_IDS_UNCONSUMED],
        "exhausted_honest_unknown_rows": [
            {"lo": KEY_PINS[k][0], "hi": KEY_PINS[k][1],
             "legal": KEY_PINS[k][2], "result": 0, "nodes": LABEL_PINS[k][1]}
            for k in EXHAUSTED_IDS],
        "row_counts": {
            "adopted_loss_rows": 24,
            "wins_unconsumed_this_pool": 19,
            "exhausted_honest_unknown": 6,
            "excluded_prior_win": 1,
            "prior_canonical_rows_base": BASE_CACHE_ROWS_EXPECTED,
        },
        "adopted_table": adopted_table,
        "adopted_table_digest_sha256": digest,
        "sha256": {"loss_increment": incr_sha},
        "full_packet_eq_loss_only": False,
        "win_scenario_exists": True,
        "win_scenario_note":
            "the batch-38 packet holds 19 probe-level WIN rows (incl. the "
            "class-30484 dual-class sibling ai048 of the adopted ai044): they "
            "are NOT consumed by this Part (adoption of WIN verdicts is "
            "scrutiny-owner C++ second-implementation gate 9193f5b6... "
            "exclusive) and every WIN key sits in NO cache",
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_sha256": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "base_cache_absent_hits_for_emitted": 0,
        "quarantine_hits": 0,
        "interpretation_guard":
            "canonical loss-only adoption increment: only the 24 fresh Part EF "
            "exact-LOSS rows (each a first-ever probe, two-pass fresh-cold "
            "node-exact at the single 15M budget/order-0 condition, solved "
            "within budget) are consumed into the canonical cache via the "
            "fail-closed union merger; nodes are bookkeeping, never verdicts; "
            "the standard 11x11 empty board stays UNKNOWN; no class freed or "
            "excluded claim is made by the maker (the reaudit refresh derives "
            "scheduling effects machine-only)",
        "provenance": {
            "ef_kit_files": kit_files,
            "status_lines": STATUS_LINES,
            "raws_published": True,
            "audit_gates_all_pass": True,
        },
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "increment_sha256": incr_sha,
        "rows": len(rowlines),
        "adopted_total_nodes_per_pass": ADOPTED_NODES_PER_PASS,
        "batch_total_nodes_per_pass": BATCH_TOTAL_NODES_PER_PASS,
        "digest": digest,
        "manifest_sha256": hashlib.sha256(
            (OUT / "increments-manifest.json").read_bytes()).hexdigest(),
    }))


if __name__ == "__main__":
    main()
