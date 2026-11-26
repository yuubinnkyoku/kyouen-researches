"""Build the Part EM emloss21 (21 unconsumed closure-batch LOSS rows)
canonical LOSS-adoption increment, fail-closed.

Part EM kit n11-centralreply-emloss21-adoption-reaudit-20261126
(2026-11-26).  This IS the adoption Part declared emission: the canonical
head of record advances from merged-exact-s5-chain-plus-evwin4 (sha256
63f33c4f..., 6,771 rows WIN 192 / LOSS 6,579) to merged-exact-s5-chain-
plus-emloss21 (sha256 6e49dd84..., 6,792 rows WIN 192 / LOSS 6,600) by
consuming exactly the 21 unconsumed closure-batch exact-LOSS rows of the
EM-pattern loss-adoption territory (the published Part EV adoption
README).  The verdict scope of the Part is exactly those 21 LOSS rows:
NO root verdict, NO 11x11 outcome, NO class freed or excluded (the
pre-declaration dossier census measured the scenario deltas IDENTICAL on
both sides with zero status flips).

Structural clone of the published pre-declaration dossier maker
`make_increments_emloss21.py` (sha256
74fbbfd9a206a28e1bcdf2d52ceb884bf71c5aee62ec0eefe520a41cd33d8035):
the computation region (all source-kit byte gates, two-pass payload
gates, b38 SSOT cross-gate, WIN regression ties, freshness/quarantine/
canonical-safety gates, adopted-table digest) is byte-identical logic;
the disclosed diff regions are the docstring, the emitted increment
header block, the output file name, the manifest Part/supersession
fields and the added dossier-supersession byte gates.  The Part
executor additionally machine-asserts that the emitted increment rows
are row-for-row identical to the published dossier increment rows (the
header comment block is the only differing region).

The pool of record is exactly the 21 UNCONSUMED closure-batch exact-LOSS
rows named by the published Part EV adoption README/declaration territory:

* batch-5 (class 12264, kit n11-centralreply-closure-class12264-batch5,
  2026-11-22, budget 15,000,000, order 0, two-pass fresh-cold node-exact):
  the 17 exact-LOSS rows f001-f016 and f018 (f018 published as-is after
  the f017 WIN-HALT, per the kit README).  The 18th probed row f017 is the
  WIN-HALT verdict, consumed by Part EV as WIN and already sitting in BASE
  with identical nodes (regression tie, NOT re-adopted, NOT emitted).
  The batch-5 kit predates the repo MANIFEST convention and holds no
  MANIFEST-sha256: every byte this maker consumes from it is pinned
  directly by sha256 (README, batch-keys.json, status.log and all 36 raw
  files; the batch-5 jsreplay.js replica sha 845856175d... is the same pin
  the ES kit MANIFEST carries).
* Part ES reprobe30m (class 30345, kit
  n11-centralreply-closure-class30345-reprobe30m, 2026-11-25, budget
  30,000,000, order 0, two-pass fresh-cold node-exact, kit MANIFEST
  cc987739...): the 4 exact-LOSS rows ai024/ai030/ai038/ai041 (the
  batch-38 honest-EXHAUSTED keys resolved exact at the FIRST next-highest
  condition 30M, no 15M same-condition re-probe).  The 2 WIN rows
  ai007/ai040 were consumed by Part EU (euwin2) and sit in BASE as WIN
  with identical nodes (regression ties, NOT re-adopted, NOT emitted).

Every gate is fail-closed: any drift aborts with rc=1 and NO output is
written.  Both source kits are verified byte-for-byte (batch-5 by direct
sha pins, ES through its published MANIFEST file-by-file), all 24 probed
rows' two-pass pairs are payload-gated (stones/legal/is_or/budget/result/
nodes/lo/hi identical across passes; '# replay_done' completeness guard),
both status logs are pinned and line-class accounted, the ES targets-30m
SSOT is cross-gated against the published batch-38 batch-keys-b38.json
(29807104...) with the prior 15M EXHAUSTED honest-label pins, and the
f017/ai007/ai040 WIN regression ties are machine-verified against BASE
(identical nodes, WIN).  All 21 adopted (lo,hi) pairs are proven absent
from BASE (fresh-increment gate), absent from the active quarantine
registry and canonical-safe per s5_evidence_policy; the adopted-table
digest and the emitted increment sha are self-pinned; the published
dossier kit bytes (increment 47443dc1..., manifest 94815c34..., maker
74fbbfd9...) are re-pinned and the emitted rows cross-gated row-for-row.

Loss-only adoption asserts no root verdict, frees no class and excludes
no class; scheduling effects remain those derived by the reaudit refresh
(Board fail-closed child verification) and the census delta extractor.
The standard 11x11 empty board and every central-reply root stay
UNKNOWN; nodes are bookkeeping, never verdicts.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
MERGER = EXP / "scripts/s5_union_merge.py"

EV_EXP = "n11-centralreply-evwin4-adoption-predecl-20261126"
B5_EXP = "n11-centralreply-closure-class12264-batch5-20261122"
ES_EXP = "n11-centralreply-closure-class30345-reprobe30m-20261125"
B38_EXP = "n11-centralreply-closure-class30345-batch38-20261125"
BASE_CACHE = ROOT / "research/experiments" / EV_EXP / (
    "output/merged-exact-s5-chain-plus-evwin4-20261126.cache")
B5_DIR = ROOT / "research/experiments" / B5_EXP
ES_DIR = ROOT / "research/experiments" / ES_EXP
B38_DIR = ROOT / "research/experiments" / B38_EXP
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"

MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA_EXPECTED = "63f33c4f620583449641102026b261c559ae5ecc29713cd6445d6fe9369858f0"
BASE_CACHE_ROWS_EXPECTED = 6771
BASE_CACHE_WIN_EXPECTED = 192
BASE_CACHE_LOSS_EXPECTED = 6579
QUARANTINE_SHA_EXPECTED = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
POLICY_SHA_EXPECTED = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"

B5_README_SHA = "1f69bfb1ff8c98e38d4c2219c792ba8225dadc2c7a25b0cfd394208e02eed7a6"
B5_KEYS_SHA = "57da4702161ab781350ebf4236791266b31bdcd78b017eaa6e4a9391ecf5451d"
B5_STATUS_SHA = "c473e32c7f1a3b2e15517ce4d5e684d3b09295b07ac314c7f0d93ecab49b2229"
B5_STATUS_LINES = 19
B5_BUDGET = 15000000
B5_REPLICA_SHA = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"

ES_MANIFEST_SHA = "cc9877399ab18dddad1250a359d13d834849aceb4ff6d54612a79bf72a615819"
ES_KIT_FILES = 38
ES_README_SHA = "67ab379ddf5325d264fe094fce101d16ca94be2fe44ad3d14d606c4d56607299"
ES_TARGETS_SHA = "1c27a238d8e39d1c17e6e93e85c94c229d603e6ea09d3b642ec00fd6474dc3a5"
ES_STATUS_SHA = "4b59732019a2ef2adc80e1e2bd058e1923301bad443849200f66a131d6ab03d8"
ES_BUDGET = 30000000
B38_KEYS_SHA = "298071046bfba8473c5b3d6e0b6a30108697eb0899aed7c70fcb4c5343f7cb8d"

ADOPTED_F_IDS = ["f%03d" % i for i in list(range(1, 17)) + [18]]
ADOPTED_ES_IDS = ["ai024", "ai030", "ai038", "ai041"]
WIN_TIE_IDS = ["f017", "ai007", "ai040"]
B5_PROBED_IDS = ["f%03d" % i for i in range(1, 19)]
ES_PROBED_IDS = ["ai007", "ai024", "ai030", "ai038", "ai040", "ai041"]
ADOPTED_IDS = ADOPTED_F_IDS + ADOPTED_ES_IDS
ALL_PROBED_IDS = B5_PROBED_IDS + ES_PROBED_IDS
assert len(ADOPTED_IDS) == 21

ADOPTED_NODES_B5 = 58253401
ADOPTED_NODES_ES = 71265013
ADOPTED_NODES_TOTAL = 129518414
B5_WHOLE_NODES = 61776036          # 18 probed rows incl. the f017 WIN-HALT
ES_WHOLE_NODES = 108066529          # 6 probed rows incl. the 2 consumed WINs

# (lo, hi, legal, s5_index) - machine-derived from the published
# batch-5 batch-keys.json, cross-gated below against the raw replay rows.
B5_KEY_PINS = {
    "f001": (1152921504741065761, 0, 80, 348),
    "f002": (1297036692682703905, 0, 86, 4231),
    "f003": (1152921504606848033, 536870912, 84, 115134),
    "f004": (1729382256910271521, 0, 86, 119290),
    "f005": (1152921504606848033, 128, 84, 223911),
    "f006": (1152921779484754977, 0, 76, 224296),
    "f007": (1441151880758559777, 0, 90, 227832),
    "f008": (1152921504606848033, 262144, 80, 323984),
    "f009": (1152921504606913569, 0, 76, 324399),
    "f010": (1224979098644775969, 0, 90, 327676),
    "f011": (1152921504606848033, 1099511627776, 80, 414362),
    "f012": (1188950301627908097, 70368744177664, 92, 415090),
    "f013": (1188950305920778241, 70368744177664, 92, 415091),
    "f014": (1188959097718833153, 70368744177664, 92, 415092),
    "f015": (1206964700135292929, 70368744177664, 91, 415093),
    "f016": (1152921504606848033, 134217728, 92, 415094),
    "f017": (1188950301625810945, 70368744177666, 82, 415095),
    "f018": (1152921504606850081, 0, 87, 415096),
}

# (result, nodes, ts) per probed key - machine-derived from the published
# status logs, cross-gated below against the raw two-pass pairs.
B5_LABEL_PINS = {
    "f001": (2, 2789768, "2026-11-22T03:31:16Z"),
    "f002": (2, 4054799, "2026-11-22T03:31:28Z"),
    "f003": (2, 2247077, "2026-11-22T03:32:16Z"),
    "f004": (2, 4461753, "2026-11-22T03:32:39Z"),
    "f005": (2, 2815240, "2026-11-22T03:33:31Z"),
    "f006": (2, 2042919, "2026-11-22T03:33:24Z"),
    "f007": (2, 3503294, "2026-11-22T03:34:27Z"),
    "f008": (2, 1775516, "2026-11-22T03:34:10Z"),
    "f009": (2, 2214154, "2026-11-22T03:35:31Z"),
    "f010": (2, 3586193, "2026-11-22T03:35:44Z"),
    "f011": (2, 2685012, "2026-11-22T03:36:39Z"),
    "f012": (2, 4680543, "2026-11-22T03:37:00Z"),
    "f013": (2, 4667365, "2026-11-22T03:38:16Z"),
    "f014": (2, 2543113, "2026-11-22T03:37:54Z"),
    "f015": (2, 6555693, "2026-11-22T03:40:06Z"),
    "f016": (2, 4032622, "2026-11-22T03:39:41Z"),
    "f017": (1, 3522635, "2026-11-22T03:41:36Z"),
    "f018": (2, 3598340, "2026-11-22T03:41:37Z"),
}

B5_RAW_SHAS = {
    "f001.p1.out": "cd48311178a57c7187f19ffbffd7eb3c7412f960a300abeb692fb058c0df4775",
    "f001.p2.out": "cd48311178a57c7187f19ffbffd7eb3c7412f960a300abeb692fb058c0df4775",
    "f002.p1.out": "6acf23c5885c7c711c5b2109d7dbcd442712a023a45fa27f49e80ea19279716d",
    "f002.p2.out": "14cfd1833ede4156b439cf9d32f81ec6c6d3e0c2e918fb0772cc9d87bec831a8",
    "f003.p1.out": "a1de5b14da0755da7251ecf186765280d9123a1fc97086fab8a20af050075bc0",
    "f003.p2.out": "799c46fb3abd0a942d116a43666f79e6f30052aca1c87f6090b0dca8b7c67a66",
    "f004.p1.out": "8b3a5578b2d29deba036e3e17ea5f3b3db2c6b35fb1e4ce40c7a09cc4b2f01da",
    "f004.p2.out": "b57572d89e3a3bffedab21d312d556d2e66e013327ffe6f87c36f1d3ce5a7ef3",
    "f005.p1.out": "10ec6a25608ad55924271be7d28d09c5c0c278a3b1bf394dfeddd69a32d38965",
    "f005.p2.out": "9c31c912bbf1b796adcec2af4091d1d0ebb242c248ade41c1c5a2a72a89c86c4",
    "f006.p1.out": "81aa7c8c47bf57c7ab2e3cd98fef29dad0bcbb207301e297a2722d91ddb1658b",
    "f006.p2.out": "c52cb36f7f4cdbe71bedcda92bb6a1da9d85acc1701cddfaaf4cc2ffe121a8d1",
    "f007.p1.out": "f6946df443faa33af65e6aa67ec724b8d3ac0e584d84039cb1c5dcc865036877",
    "f007.p2.out": "fbc5d70205e10d12617d5a1db70e453cb2e109e2e7083467173392cc4f707435",
    "f008.p1.out": "dd182f1520632d591027a0f9b9328ec52b321f4ff5c04826421bee22b0cd2097",
    "f008.p2.out": "dd182f1520632d591027a0f9b9328ec52b321f4ff5c04826421bee22b0cd2097",
    "f009.p1.out": "2a16076a648442f194f833a0c5eb79004494cea4b5ad2170043ecf301e5151a9",
    "f009.p2.out": "3d764238e45d08e0bdbe0c0d475ad5c76ab4511de79b44d7e3c7be596786f538",
    "f010.p1.out": "71c851afaf675a30e92e809969155c52158ba5b8e16d53fed8001819b7c589a7",
    "f010.p2.out": "82358395214e0f9564f37323599abde1e4d0811822087368f55fb1a74de6a8df",
    "f011.p1.out": "9887535c7a792d34135753bbc76974468df9c5cefa0a973c54473120fd4cb091",
    "f011.p2.out": "b66ae0b835fee5c4e003cc0db389b62f87d20315ef0df0f388455880aa9fef4b",
    "f012.p1.out": "56df93b45a0b7e302f9ed33bbc6a19a7f0e37f5a0c884470b4f905e8106ebe21",
    "f012.p2.out": "692ce4664e5a0a39ead73cc56f9500e65f4c21fbde9fefe3afb657dda01cafdf",
    "f013.p1.out": "3f149f870203bbeda195651acaebc5f2b96eb1f7a99cbfef90939db61b107fe7",
    "f013.p2.out": "5a5f34bac3b1977e8e0dc6dd23918ec48881f87217d2d5a3fcba01a0a82885e5",
    "f014.p1.out": "8658d68d680ef9afed1a4a17e97a02bc3b766f4842656241706101d7d46ea072",
    "f014.p2.out": "5dedf836afbbd62e26baca1537cc7c843d824f9ba63eb5c80455b52197c980f6",
    "f015.p1.out": "a57639c2dcaeef24176a6894dfbb17f578cb0f8db1fdb976d93553d34e4370a3",
    "f015.p2.out": "808d6d14e1f4cbda8c866083cd04da1947073d68e6b7503b3695a6107a62341b",
    "f016.p1.out": "0b17e454843d07cdf6a038becd9ec86d3da873e8a238cde41e3c440fff97268d",
    "f016.p2.out": "bf2b0a0fcbb69356591177d38c53ce628093be395a4c65bc6ae5604f702a4758",
    "f017.p1.out": "807a00df449ec05e8ed51df2c3834267f92017445b12afb9a80b362cd0c18e5e",
    "f017.p2.out": "fff3029a21a1621e5c39303ef42981d7aa8b711a8ae9b9a7c3f43698e36a15bc",
    "f018.p1.out": "614c1f6f5d3da629f5e40f7501aa39f942a863ee04174b1099a86fc54dc1f48a",
    "f018.p2.out": "60b95137d9c617ed58c9721ebf9624eb89584c0a92dffbbeed2aac76b9b168a5",
}

# (lo, hi, legal, s5_index, probe_order) for the 6 Part ES targets -
# machine-derived from the published targets-30m.json, cross-gated
# below against the b38 batch-keys SSOT and the raw replay rows.
ES_KEY_PINS = {
    "ai007": (1152922604118478880, 65536, 84, 441292, 138),
    "ai024": (1152922604118479104, 65536, 86, 889534, 156),
    "ai030": (1152921573327372288, 17825792, 91, 894456, 162),
    "ai038": (1152927002164989952, 65536, 89, 898436, 170),
    "ai040": (1152922604118487040, 65536, 85, 899584, 172),
    "ai041": (1152921573327372288, 34603008, 91, 900170, 173),
}

ES_LABEL_PINS = {
    "ai007": (1, 16090493, "2026-11-25T21:51:00Z"),
    "ai024": (2, 19127057, "2026-11-25T21:54:40Z"),
    "ai030": (2, 16504156, "2026-11-25T21:57:44Z"),
    "ai038": (2, 19851840, "2026-11-25T22:01:42Z"),
    "ai040": (1, 20711023, "2026-11-25T22:05:59Z"),
    "ai041": (2, 15781960, "2026-11-25T22:09:01Z"),
}

# the honest prior 15M condition of the 6 Part ES targets (Part EF
# batch-audit 73652099... per the published Part EM maker LABEL pins):
# all six EXHAUSTED at budget 15,000,000 (honest UNKNOWN, result 0).
B38_PRIOR_LABEL_PINS = {
    "ai007": (0, 15000000), "ai024": (0, 15000000), "ai030": (0, 15000000),
    "ai038": (0, 15000000), "ai040": (0, 15000000), "ai041": (0, 15000000),
}

DOSSIER_INCR_SHA_EXPECTED = "47443dc143c157ab972de0f39f2cf3afb5d062e209da9dcd8e486f0a57c8ebca"
DOSSIER_MANIFEST_SHA_EXPECTED = "94815c34f1142481a20fe411a0a1c87c4e0a075b100d47db2f5e7b35dea9707d"
DOSSIER_MAKER_SHA_EXPECTED = "74fbbfd9a206a28e1bcdf2d52ceb884bf71c5aee62ec0eefe520a41cd33d8035"
DOSSIER_MERGED_SHA_EXPECTED = "6e49dd841b7bfcb335d86ef2479c95f47ab7acbcf41ace389a8b8eb95c778c9d"
ADOPTED_TABLE_DIGEST = "4fd8723ec0e2d185fe807b80681f1c9deca6ac0ee09ddd4bf77b047cdb88e97b"
ADOPTED_INCREMENT_SHA = "3e6e9bf0a5f410a1d584889832f21352dd01a97aef5a899de06a28373fcaef82"

INCREMENT_NAME = "increment-emloss21-adoption-20261126.cache"
EMLOSS21_SCHEMA = "emloss21-adoption-increments-manifest-v1"

HDR_LINES = [
 "# n11 central-reply closure emloss21 canonical-adoption increment",
 "#   (Part EM, n11-centralreply-emloss21-adoption-reaudit-20261126,",
 "#   2026-11-26) - loss-only, fresh 21-row increment.  Part EM declares",
 "#   the emloss21 canonical LOSS adoption: the canonical head of record",
 "#   advances to merged-exact-s5-chain-plus-emloss21 (6,792 rows",
 "#   WIN 192 / LOSS 6,600) by consuming exactly the 21 unconsumed",
 "#   closure-batch exact-LOSS rows of the EM-pattern territory.",
 "# The sources of record (re-verified live by this Part maker against",
 "#   published bytes): 17 rows f001-f016,f018 of the published batch-5",
 "#   kit (closure class 12264, 2026-11-22, budget 15,000,000 order 0,",
 "#   two-pass fresh-cold node-exact; f018 published as-is after the",
 "#   f017 WIN-HALT) and 4 rows ai024/ai030/ai038/ai041 of the published",
 "#   Part ES reprobe30m kit (closure class 30345, 2026-11-25, budget",
 "#   30,000,000 order 0, two-pass fresh-cold node-exact; the batch-38",
 "#   honest-EXHAUSTED keys resolved exact at the first next-highest",
 "#   condition).  Adopted node total 129,518,414 (batch-5 58,253,401 +",
 "#   Part ES 71,265,013).",
 "# NOT re-adopted here (each sits in BASE already as a consumed WIN with",
 "#   identical nodes, machine-verified regression ties): f017 (Part EV,",
 "#   15M, nodes 3,522,635), ai007 and ai040 (Part EU euwin2, 30M, nodes",
 "#   16,090,493 / 20,711,023).  Every adopted row is fresh to BASE",
 "#   63f33c4f..., quarantine-free, canonical-safe per",
 "#   s5_evidence_policy.",
 "# This Part-emitted increment supersedes the pre-declaration dossier",
 "#   increment 47443dc1... row-for-row (the header comment block is the",
 "#   only differing region; the merged cache of record carries the",
 "#   published dossier merged sha 6e49dd84...).",
 "# Loss-only adoption asserts NO root verdict, frees no class and",
 "#   excludes no class; the scheduling effects are derived only by the",
 "#   reaudit refresh (Board fail-closed child verification) and the",
 "#   census delta extractor.  The standard 11x11 empty board and every",
 "#   central-reply root stay UNKNOWN; nodes are bookkeeping, never",
 "#   verdicts.",
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


def verify_es_kit():
    if not ES_DIR.is_dir():
        sys_exit(f"kit dir missing {ES_DIR}")
    if sha(ES_DIR / "MANIFEST-sha256.txt") != ES_MANIFEST_SHA:
        sys_exit("Part ES kit MANIFEST sha drift")
    verified = 0
    for line in (ES_DIR / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split("  ")
        if len(fields) != 3:
            sys_exit(f"Part ES MANIFEST malformed line: {line}")
        want, size, rel = fields[0], int(fields[1]), fields[2]
        if rel.startswith("/") or ".." in rel.split("/") or "\x00" in rel:
            sys_exit(f"Part ES MANIFEST unsafe path: {rel}")
        p = ES_DIR / rel
        if not p.is_file():
            sys_exit(f"Part ES kit file missing: {rel}")
        if p.stat().st_size != size:
            sys_exit(f"Part ES kit file size drift: {rel}")
        if sha(p) != want:
            sys_exit(f"Part ES kit file sha drift: {rel}")
        verified += 1
    if verified != ES_KIT_FILES:
        sys_exit(f"Part ES kit files verified {verified} != {ES_KIT_FILES}")
    return verified


def main() -> None:
    # --- anchors: base cache, merger, quarantine, policy --------------------
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys_exit("base cache (Part EV head) sha drift")
    if sha(MERGER) != MERGER_SHA_EXPECTED:
        sys_exit("fail-closed union merger (scripts/s5_union_merge.py) sha drift: "
                 "this dossier must use the pinned merger byte-for-byte")
    if sha(QUARANTINE) != QUARANTINE_SHA_EXPECTED:
        sys_exit("quarantine registry sha drift")
    if sha(POLICY) != POLICY_SHA_EXPECTED:
        sys_exit("evidence policy sha drift")
    base_keys = {}
    wins = losss = 0
    for line in BASE_CACHE.read_text(encoding="utf-8-sig").splitlines():
        if not line or line.lstrip().startswith("#"):
            continue
        f = line.split(",")
        if len(f) != 6 or f[0] != "s5verdict":
            sys_exit(f"invalid base cache row: {line}")
        base_keys[(int(f[1]), int(f[2]))] = (int(f[4]), int(f[5]))
        if int(f[4]) == 1:
            wins += 1
        elif int(f[4]) == 2:
            losss += 1
    if len(base_keys) != BASE_CACHE_ROWS_EXPECTED:
        sys_exit(f"base cache rows {len(base_keys)} != {BASE_CACHE_ROWS_EXPECTED}")
    if wins != BASE_CACHE_WIN_EXPECTED or losss != BASE_CACHE_LOSS_EXPECTED:
        sys_exit(f"base cache WIN/LOSS {wins}/{losss} != pinned")
    q = json.loads(QUARANTINE.read_text())
    quarantined = {tuple(e["key"]) for e in q["entries"] if e.get("active")}

    sys.path.insert(0, str(POLICY.parent))
    from s5_evidence_policy import is_canonical_safe_s5_key  # noqa: E402

    # --- batch-5 kit: direct byte pins (kit predates MANIFESTs) ------------
    if not B5_DIR.is_dir():
        sys_exit(f"batch-5 kit dir missing {B5_DIR}")
    if sha(B5_DIR / "README.md") != B5_README_SHA:
        sys_exit("batch-5 kit README sha drift")
    if sha(B5_DIR / "input/batch-keys.json") != B5_KEYS_SHA:
        sys_exit("batch-5 batch-keys.json sha drift")
    if sha(B5_DIR / "output/status.log") != B5_STATUS_SHA:
        sys_exit("batch-5 status.log sha drift")
    bk = json.loads((B5_DIR / "input/batch-keys.json").read_text())
    if bk["schema"] != "n11-centralreply-closure-class12264-batch-input-v1":
        sys_exit("batch-5 keys schema drift")
    if bk["class_index"] != 12264 or bk["class_mask"] != [1152921504606848033, 0]:
        sys_exit("batch-5 keys class drift")
    if bk["budget"] != B5_BUDGET:
        sys_exit("batch-5 keys budget drift")
    if len(bk["keys"]) != 51 or [k["key_id"] for k in bk["keys"]] != [
            "f%03d" % i for i in range(1, 52)]:
        sys_exit("batch-5 keys 51-key accounting drift")
    b5k = {k["key_id"]: k for k in bk["keys"]}
    for kid in B5_PROBED_IDS:
        k = b5k[kid]
        lo, hi, legal, s5_index = B5_KEY_PINS[kid]
        if (k["lo"] != lo or k["hi"] != hi or k["legal"] != legal
                or k["s5_index"] != s5_index):
            sys_exit(f"batch-5 keys key field drift: {kid}")
    # batch-5 status.log: exactly 19 lines, 18 PASS + 1 WIN-HALT row
    blines = (B5_DIR / "output/status.log").read_text().splitlines()
    if len(blines) != B5_STATUS_LINES:
        sys_exit(f"batch-5 status lines {len(blines)} != {B5_STATUS_LINES}")
    pass_rows = {}
    halt_rows = []
    for line in blines:
        parts = line.split()
        if len(parts) == 4 and parts[2] == "PASS":
            pass_rows[parts[1]] = (parts[0], tuple(int(x) for x in parts[3].split(",")))
        elif len(parts) == 3 and parts[2] == "WIN-HALT":
            halt_rows.append((parts[0], True))
        else:
            sys_exit(f"batch-5 status unexpected line: {line}")
    if sorted(pass_rows) != sorted(B5_PROBED_IDS):
        sys_exit("batch-5 status PASS keys != the 18 probed targets")
    if halt_rows != [("2026-11-22T03:41:36Z", True)]:
        sys_exit("batch-5 status WIN-HALT row drift")
    for kid in B5_PROBED_IDS:
        r, n, ts = B5_LABEL_PINS[kid]
        if pass_rows[kid] != (ts, (B5_BUDGET, r, n)):
            sys_exit(f"batch-5 status verdict row drift: {kid}")
    # batch-5 raws: all 18 two-pass pairs, byte-pinned
    b5_raws = {}
    for kid in B5_PROBED_IDS:
        ref = two_pass(B5_DIR / "output/raw", kid, B5_BUDGET, B5_RAW_SHAS)
        lo, hi, legal, s5_index = B5_KEY_PINS[kid]
        if ref["stones"] != 5 or ref["is_or"] != 0:
            sys_exit(f"{kid}: wrong depth/or bit")
        if ref["legal"] != legal or ref["lo"] != str(lo) or ref["hi"] != str(hi):
            sys_exit(f"{kid}: legal/key disagreement raw vs pinned key fields")
        if (ref["budget"], ref["result"], ref["nodes"]) != (
                B5_BUDGET, B5_LABEL_PINS[kid][0], B5_LABEL_PINS[kid][1]):
            sys_exit(f"{kid}: raw honest-label drift vs the pinned status row")
        b5_raws[kid] = ref
    if sorted(k for k in b5_raws if b5_raws[k]["result"] == 2) != sorted(ADOPTED_F_IDS):
        sys_exit("batch-5 exact-LOSS set != the 17 adopted f-ids")
    if sorted(k for k in b5_raws if b5_raws[k]["result"] == 1) != ["f017"]:
        sys_exit("batch-5 probed WIN set drift")
    n_b5_whole = sum(b5_raws[k]["nodes"] for k in B5_PROBED_IDS)
    if n_b5_whole != B5_WHOLE_NODES:
        sys_exit(f"batch-5 whole-batch node total drift {n_b5_whole} != {B5_WHOLE_NODES}")
    n_b5_adopted = sum(b5_raws[k]["nodes"] for k in ADOPTED_F_IDS)
    if n_b5_adopted != ADOPTED_NODES_B5:
        sys_exit(f"batch-5 adopted node total drift {n_b5_adopted} != {ADOPTED_NODES_B5}")

    # --- Part ES kit: MANIFEST-verified bytes --------------------------------
    kit_files = verify_es_kit()
    if sha(ES_DIR / "README.md") != ES_README_SHA:
        sys_exit("Part ES kit README sha drift")
    if sha(ES_DIR / "input/targets-30m.json") != ES_TARGETS_SHA:
        sys_exit("Part ES targets-30m.json sha drift")
    if sha(ES_DIR / "output/status.log") != ES_STATUS_SHA:
        sys_exit("Part ES status.log sha drift")
    tg = json.loads((ES_DIR / "input/targets-30m.json").read_text())
    if tg["schema"] != "class30345-reprobe30m-targets-v1":
        sys_exit("Part ES targets schema drift")
    if tg["part"] != "ES" or tg["condition"]["budget"] != ES_BUDGET:
        sys_exit("Part ES targets condition drift")
    if tg["condition"]["order"] != 0:
        sys_exit("Part ES targets order drift")
    if sorted(t["key_id"] for t in tg["targets"]) != sorted(ES_PROBED_IDS):
        sys_exit("Part ES targets key-id set drift")
    for t in tg["targets"]:
        kid = t["key_id"]
        lo, hi, legal, s5_index, probe_order = ES_KEY_PINS[kid]
        if (t["lo"] != lo or t["hi"] != hi or t["legal"] != legal
                or t["s5_index"] != s5_index or t["probe_order"] != probe_order):
            sys_exit(f"Part ES target key field drift: {kid}")
        if t["serving_class"] != 30345 or t["class_mask"] != [1152922604118478848, 65536]:
            sys_exit(f"Part ES target class drift: {kid}")
    # Part ES status.log: 8 lines, 6 PASS + 2 WIN echo rows
    eslines = (ES_DIR / "output/status.log").read_text().splitlines()
    es_pass = {}
    es_win_rows = []
    for line in eslines:
        parts = line.split()
        if len(parts) == 4 and parts[2] == "PASS":
            if parts[1] in es_pass:
                sys_exit(f"Part ES status duplicate PASS row for {parts[1]}")
            es_pass[parts[1]] = (parts[0], tuple(int(x) for x in parts[3].split(",")))
        elif len(parts) == 4 and parts[2] == "WIN":
            es_win_rows.append((parts[0], parts[1],
                                tuple(int(x) for x in parts[3].split(","))))
        else:
            sys_exit(f"Part ES status unexpected line: {line}")
    if sorted(es_pass) != sorted(ES_PROBED_IDS):
        sys_exit("Part ES status PASS keys != the 6 targets")
    for kid in ES_PROBED_IDS:
        r, n, ts = ES_LABEL_PINS[kid]
        if es_pass[kid] != (ts, (ES_BUDGET, r, n)):
            sys_exit(f"Part ES status verdict row drift: {kid}")
    if sorted(es_win_rows) != sorted(
            [(ES_LABEL_PINS[k][2], k, (ES_BUDGET, ES_LABEL_PINS[k][0], ES_LABEL_PINS[k][1]))
             for k in ("ai007", "ai040")]):
        sys_exit("Part ES status WIN echo rows drift")
    # b38 SSOT cross-gate + prior 15M EXHAUSTED honest-label pins
    if sha(B38_DIR / "input/batch-keys-b38.json") != B38_KEYS_SHA:
        sys_exit("batch-keys-b38.json (b38 SSOT) sha drift")
    b38k = {k["key_id"]: k for k in
            json.loads((B38_DIR / "input/batch-keys-b38.json").read_text())["keys"]}
    for kid in ES_PROBED_IDS:
        lo, hi, legal, s5_index, probe_order = ES_KEY_PINS[kid]
        k = b38k.get(kid)
        if k is None:
            sys_exit(f"{kid}: missing from the b38 SSOT")
        if (k["lo"] != lo or k["hi"] != hi or k["legal"] != legal
                or k["s5_index"] != s5_index or k["probe_order"] != probe_order):
            sys_exit(f"{kid}: b38 SSOT key-field disagreement")
        if k["serving_class"] != 30345:
            sys_exit(f"{kid}: b38 SSOT serving class drift")
        if B38_PRIOR_LABEL_PINS[kid] != (0, B5_BUDGET):
            sys_exit(f"{kid}: prior 15M EXHAUSTED label pin drift")
    # Part ES raws: all 6 two-pass pairs (already byte-pinned by the
    # ES MANIFEST verification; payload-gated here)
    es_raws = {}
    es_manifest_shas = {}
    for line in (ES_DIR / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        f0, _sz, rel = line.split("  ")
        if rel.startswith("output/raw/"):
            es_manifest_shas[rel.split("/", 2)[2]] = f0
    for kid in ES_PROBED_IDS:
        ref = two_pass(ES_DIR / "output/raw", kid, ES_BUDGET, es_manifest_shas)
        lo, hi, legal, s5_index, probe_order = ES_KEY_PINS[kid]
        if ref["stones"] != 5 or ref["is_or"] != 0:
            sys_exit(f"{kid}: wrong depth/or bit")
        if ref["legal"] != legal or ref["lo"] != str(lo) or ref["hi"] != str(hi):
            sys_exit(f"{kid}: legal/key disagreement raw vs pinned key fields")
        if (ref["budget"], ref["result"], ref["nodes"]) != (
                ES_BUDGET, ES_LABEL_PINS[kid][0], ES_LABEL_PINS[kid][1]):
            sys_exit(f"{kid}: raw honest-label drift vs the pinned status row")
        es_raws[kid] = ref
    if sorted(k for k in es_raws if es_raws[k]["result"] == 2) != sorted(ADOPTED_ES_IDS):
        sys_exit("Part ES 30M exact-LOSS set != the 4 adopted ids")
    n_es_whole = sum(es_raws[k]["nodes"] for k in ES_PROBED_IDS)
    if n_es_whole != ES_WHOLE_NODES:
        sys_exit(f"Part ES whole-batch node total drift {n_es_whole} != {ES_WHOLE_NODES}")
    n_es_adopted = sum(es_raws[k]["nodes"] for k in ADOPTED_ES_IDS)
    if n_es_adopted != ADOPTED_NODES_ES:
        sys_exit(f"Part ES adopted node total drift {n_es_adopted} != {ADOPTED_NODES_ES}")

    # --- WIN regression ties (consumed WINs, never re-adopted) -------------
    for kid in WIN_TIE_IDS:
        if kid in B5_PROBED_IDS:
            ref = b5_raws[kid]
        else:
            ref = es_raws[kid]
        key = (int(ref["lo"]), int(ref["hi"]))
        if ref["result"] != 1:
            sys_exit(f"win-tie {kid}: raw result drift")
        got = base_keys.get(key)
        if got is None or got[0] != 1 or got[1] != ref["nodes"]:
            sys_exit(f"win-tie {kid}: BASE row {got} != in-cache WIN tie nodes {ref['nodes']}")

    # --- freshness: BASE absence, quarantine absence, canonical safety -----
    adopted_rows = []
    for kid in ADOPTED_IDS:
        if kid in B5_PROBED_IDS:
            ref = b5_raws[kid]
            key_pin, serving_class = B5_KEY_PINS[kid][3], 12264
        else:
            ref = es_raws[kid]
            key_pin, serving_class = ES_KEY_PINS[kid][3], 30345
        if ref["result"] != 2:
            sys_exit(f"{kid}: adopted row must be exact LOSS")
        key = (int(ref["lo"]), int(ref["hi"]))
        if key in quarantined:
            sys_exit(f"{kid}: quarantined key {key}")
        if not is_canonical_safe_s5_key(key):
            sys_exit(f"{kid}: noncanonical/unsafe key {key}")
        if key in base_keys:
            sys_exit(f"{kid}: key already in canonical BASE; fresh-increment gate")
        adopted_rows.append((key[0], key[1], ref["legal"], 2, ref["nodes"],
                             key_pin, serving_class))
    if len({(r[0], r[1]) for r in adopted_rows}) != 21:
        sys_exit("adopted pairs must be exactly 21 distinct keys")
    # the 3 consumed WINs must also be quarantine-clear and canonical-safe
    for kid in WIN_TIE_IDS:
        if kid in B5_PROBED_IDS:
            ref = b5_raws[kid]
        else:
            ref = es_raws[kid]
        key = (int(ref["lo"]), int(ref["hi"]))
        if key in quarantined:
            sys_exit(f"win-tie {kid}: quarantined key {key}")
        if not is_canonical_safe_s5_key(key):
            sys_exit(f"win-tie {kid}: noncanonical/unsafe key {key}")

    digest = hashlib.sha256("\n".join(
        f"{lo},{hi},{legal},{result},{nodes}"
        for lo, hi, legal, result, nodes, _s5, _cls in
        sorted(adopted_rows)).encode()).hexdigest()
    if digest != ADOPTED_TABLE_DIGEST:
        sys_exit(f"adopted-table digest drift {digest}")

    # --- Part EM dossier-supersession gates ----------------------------------
    DOSSIER = ROOT / "research/experiments/n11-centralreply-emloss21-adoption-predecl-20261126"
    if sha(DOSSIER / "output/increment-emloss21-20261126.cache") != DOSSIER_INCR_SHA_EXPECTED:
        sys_exit("published dossier increment sha drift")
    if sha(DOSSIER / "output/increments-manifest.json") != DOSSIER_MANIFEST_SHA_EXPECTED:
        sys_exit("published dossier manifest sha drift")
    if sha(DOSSIER / "scripts/make_increments_emloss21.py") != DOSSIER_MAKER_SHA_EXPECTED:
        sys_exit("published dossier maker sha drift")
    if sha(DOSSIER / "output/merged-exact-s5-chain-plus-emloss21-20261126.cache") \
            != DOSSIER_MERGED_SHA_EXPECTED:
        sys_exit("published dossier merged cache sha drift")
    dm = json.loads((DOSSIER / "output/increments-manifest.json").read_text())
    if dm["adopted_table_digest_sha256"] != ADOPTED_TABLE_DIGEST \
            or dm["adopted_nodes_total"] != ADOPTED_NODES_TOTAL \
            or dm["sha256"]["loss_increment"] != DOSSIER_INCR_SHA_EXPECTED:
        sys_exit("published dossier manifest adopted-table accounting drift")
    dossier_rows = [ln for ln in
                    (DOSSIER / "output/increment-emloss21-20261126.cache")
                    .read_text().splitlines() if ln.startswith("s5verdict,")]
    if len(dossier_rows) != 21:
        sys_exit("published dossier increment row count drift")

    # --- emit increment + manifest -------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    rowlines = [f"s5verdict,{r[0]},{r[1]},5,2,{r[2]}"
                for r in sorted((lo, hi, nodes)
                                 for lo, hi, legal, result, nodes, _s5, _cls
                                 in adopted_rows)]
    if len(rowlines) != 21:
        sys_exit("emitted row count drift")
    if rowlines != dossier_rows:
        sys_exit("emitted increment rows differ from the published dossier rows")
    blob = ("\n".join(HDR_LINES + rowlines) + "\n").encode("utf-8")
    incr_sha = hashlib.sha256(blob).hexdigest()
    if incr_sha != ADOPTED_INCREMENT_SHA:
        sys_exit(f"emitted increment sha drift {incr_sha} != pinned {ADOPTED_INCREMENT_SHA}")
    (OUT / INCREMENT_NAME).write_bytes(blob)

    adopted_table = [
        {"lo": lo, "hi": hi, "legal": legal, "result": 2, "nodes": nodes,
         "s5_index": s5_index, "serving_class": serving_class}
        for lo, hi, legal, result, nodes, s5_index, serving_class
        in sorted(adopted_rows)]

    manifest = {
        "schema": EMLOSS21_SCHEMA,
        "part": "EM",
        "date": "2026-11-26",
        "loss_canonical_adoption": True,
        "dossier_supersession": {
            "dossier_increment_sha256": DOSSIER_INCR_SHA_EXPECTED,
            "dossier_manifest_sha256": DOSSIER_MANIFEST_SHA_EXPECTED,
            "dossier_maker_sha256": DOSSIER_MAKER_SHA_EXPECTED,
            "row_region_byte_identical": True,
            "merged_cache_sha256_of_record": DOSSIER_MERGED_SHA_EXPECTED,
            "note": "the dossier increment header declared pre-declaration "
                    "dossier status; this Part-emitted increment supersedes "
                    "it with the Part EM adoption header; the 21 s5verdict "
                    "rows are byte-identical and the merged cache of record "
                    "carries the published dossier merged sha 6e49dd84...",
        },
        "pools": [
            {"pool": "b5-class12264",
             "kit": B5_EXP,
             "budget": B5_BUDGET,
             "adopted_loss_ids": list(ADOPTED_F_IDS),
             "win_tie_ids": ["f017"],
             "win_tie_note": "f017 (batch-5 WIN-HALT, 15M, nodes 3,522,635) "
                             "consumed by Part EV as WIN; in BASE 63f33c4f "
                             "with identical nodes; regression tie, NOT "
                             "re-adopted",
             "adopted_nodes": ADOPTED_NODES_B5,
             "whole_probed_nodes": B5_WHOLE_NODES,
             "probed_ids": list(B5_PROBED_IDS),
             "kit_integrity": {
                 "note": "the batch-5 kit (2026-11-22) predates the repo "
                         "MANIFEST convention and holds no MANIFEST-sha256; "
                         "every consumed byte is pinned directly: README "
                         f"{B5_README_SHA[:8]}..., batch-keys.json "
                         f"{B5_KEYS_SHA[:8]}..., status.log "
                         f"{B5_STATUS_SHA[:8]}... and all 36 raw files "
                         "(raw_file_sha256_pins below)",
                 "solver_replica_sha256": B5_REPLICA_SHA,
                 "raw_file_sha256_pins": B5_RAW_SHAS,
             }},
            {"pool": "es-class30345-reprobe30m",
             "kit": ES_EXP,
             "budget": ES_BUDGET,
             "adopted_loss_ids": list(ADOPTED_ES_IDS),
             "win_tie_ids": ["ai007", "ai040"],
             "win_tie_note": "ai007/ai040 (30M WIN) consumed by Part EU "
                             "euwin2; in BASE 63f33c4f with identical nodes; "
                             "regression ties, NOT re-adopted",
             "adopted_nodes": ADOPTED_NODES_ES,
             "whole_probed_nodes": ES_WHOLE_NODES,
             "probed_ids": list(ES_PROBED_IDS),
             "prior_15m_condition": {
                 "note": "all 6 targets were EXHAUSTED (honest UNKNOWN) at "
                         "budget 15M in batch-38, first-ever probes per the "
                         "published prior-probe universe; Part ES resolved "
                         "them at the first next-highest condition 30M with "
                         "no 15M same-condition re-probe",
                 "honest_label_pins": {k: list(v) for k, v in B38_PRIOR_LABEL_PINS.items()},
             },
             "kit_integrity": {
                 "note": "Part ES kit verified file-by-file against its "
                         f"published MANIFEST-sha256 {ES_MANIFEST_SHA[:8]}... "
                         f"({ES_KIT_FILES} files)",
                 "kit_manifest_sha256": ES_MANIFEST_SHA,
                 "kit_files_verified": ES_KIT_FILES,
                 "readme_sha256": ES_README_SHA,
                 "targets_30m_sha256": ES_TARGETS_SHA,
                 "status_log_sha256": ES_STATUS_SHA,
             },
             "b38_ssot_cross_check": {
                 "batch_keys_b38_sha256": B38_KEYS_SHA,
                 "note": "all 6 targets cross-gated field-by-field against "
                         "the published b38 batch-keys SSOT (lo/hi/legal/"
                         "s5_index/probe_order, serving_class 30345)",
             }},
        ],
        "resolved_ids": list(ADOPTED_IDS),
        "loss_ids": list(ADOPTED_IDS),
        "win_ties": [
            {"id": kid,
             "lo": (B5_KEY_PINS if kid in B5_KEY_PINS else ES_KEY_PINS)[kid][0],
             "hi": (B5_KEY_PINS if kid in B5_KEY_PINS else ES_KEY_PINS)[kid][1],
             "legal": (B5_KEY_PINS if kid in B5_KEY_PINS else ES_KEY_PINS)[kid][2],
             "s5_index": (B5_KEY_PINS if kid in B5_KEY_PINS else ES_KEY_PINS)[kid][3],
             "nodes": (B5_LABEL_PINS if kid in B5_LABEL_PINS else ES_LABEL_PINS)[kid][1]}
            for kid in WIN_TIE_IDS],
        "row_counts": {
            "adopted_loss_rows": 21,
            "win_ties_consumed_elsewhere": 3,
            "prior_canonical_rows_base": BASE_CACHE_ROWS_EXPECTED,
        },
        "adopted_table": adopted_table,
        "adopted_table_digest_sha256": digest,
        "adopted_nodes_total": ADOPTED_NODES_TOTAL,
        "sha256": {"loss_increment": incr_sha},
        "full_packet_eq_loss_only": True,
        "win_scenario_note":
            "there is NO WIN scenario in this dossier: the increment is "
            "loss-only (21 exact-LOSS rows) and the 3 WIN rows of the source "
            "batches (f017, ai007, ai040) are already consumed by Parts "
            "EV/EU and sit in BASE with identical nodes (regression ties)",
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_sha256": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "base_cache_win_loss": [BASE_CACHE_WIN_EXPECTED, BASE_CACHE_LOSS_EXPECTED],
        "base_cache_absent_hits_for_emitted": 0,
        "quarantine_hits": 0,
        "interpretation_guard":
            "Part EM canonical loss-only adoption increment: the 21 fresh "
            "exact-LOSS rows (each two-pass fresh-cold node-exact at its own "
            "single published condition, batch-5 15M / Part ES 30M, solved "
            "within budget) are consumed into the canonical chain via the "
            "fail-closed union merger; nodes are bookkeeping, never "
            "verdicts; consuming a LOSS label asserts no root verdict; "
            "the standard 11x11 empty board and every central-reply root "
            "stay UNKNOWN; no class freed or excluded claim is made by the "
            "Part (the reaudit refresh derives scheduling effects "
            "machine-only)",
        "provenance": {
            "part_maker_reverified_live": True,
            "dossier_bytes_repinned": True,
            "b5_kit_direct_pins": True,
            "b5_fetch_anchor_note":
                "the batch-5 kit bytes were re-anchored to the published "
                "repo tree at the point of dossier construction (39/39 "
                "consumed files byte-identical to the repo copies); the "
                "pins above are the anchor of record",
            "es_kit_files_verified": kit_files,
            "raws_published": True,
            "b38_ssot_verified": True,
        },
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "part": "EM",
        "supersession": "dossier increment 47443dc1... superseded "
                        "row-for-row; merged cache of record 6e49dd84...",
        "increment_sha256": incr_sha,
        "rows": len(rowlines),
        "adopted_nodes_total": ADOPTED_NODES_TOTAL,
        "adopted_nodes_b5": ADOPTED_NODES_B5,
        "adopted_nodes_es": ADOPTED_NODES_ES,
        "digest": digest,
        "manifest_sha256": hashlib.sha256(
            (OUT / "increments-manifest.json").read_bytes()).hexdigest(),
    }))


if __name__ == "__main__":
    main()
