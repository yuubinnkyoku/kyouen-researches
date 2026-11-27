#!/usr/bin/env python3
"""Build the sixthwin5 (5 unconsumed sixth-cost WIN rows) canonical
WIN-adoption PREDECL-DOSSIER increment, fail-closed.

Dossier n11-centralreply-sixthwin5-adoption-predecl-20261126 (2026-11-26).
This is NOT a Part: no declaration, no adoption, no verdict consumption.
The canonical head stays merged-exact-s5-chain-plus-emloss21 (sha256
6e49dd84..., 6,792 rows WIN 192 / LOSS 6,600; the Part EM adoption head
of record, published by the Part EM pre-declaration dossier kit).  This
maker publishes, up front, the increment and manifest a future EV-pattern
WIN-adoption Part would pin, so that the declaring Part can reference
PUBLISHED bytes only (the Part EU declaration-pin lesson).

The pool of record is exactly the 5 UNCONSUMED sixth-cost exclusive-probe
WIN rows of the published probe kit
n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121
(class 10376293541461626880:65536, budget 15,000,000, order 0):

* k02 1297036692683751424:68157440 (legal 87, nodes 7,717,432)
* k03 10376293541461626880:65792 (legal 81, nodes 9,255,414)
* k04 10376293541461626888:65536 (legal 83, nodes 9,433,024)
* k05 10376293541461757952:65536 (legal 88, nodes 13,397,611)
* k08 10376293610182148096:68719476736 (legal 89, nodes 6,195,897)

Each adopted row is gated at FOUR independent implementations, all
re-verified here byte-for-byte or field-for-field:

1. the probe kit's jsreplay replica: two-pass fresh-cold node-exact
   (at15m-run1/2) PLUS a voluntary third cold verify run
   (at15m-run3-verify), identical (result, nodes) across all three;
2. the published Part SK C++ second-implementation gate kit
   n11-sixthcost-exclusive-cppgate-20261126 (MANIFEST-verified
   file-by-file, 46/46): every row GATE-PASS, 2-pass determinism and
   published-raw node-exact (the pre-registered adoption requirement of
   the probe kit's WIN rows, sha-pinned C++ solver);
3. the TI third-implementation kit
   n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122
   (audit-summary.json for k03, audit-k04/k05/k06k07k08-summary.json):
   verdict-level WIN agreement, determinism triplets identical, replica
   raws byte-identical to the probe kit's;
4. for k02, the ea73c3e3 fixed third implementation kit
   n11-sixthcost-third-implementation-verdict-reverification-20261121:
   WIN (1) with 9,106,337 expansions on all 4 witness runs (a/b/g/v),
   verdict-level agreement (expansions legitimately differ from the
   replica's node counts; different implementations).

Every gate is fail-closed: any drift aborts with rc=1 and NO output is
written.  The probe kit predates the repo MANIFEST convention and holds
no MANIFEST-sha256: every byte this maker consumes from it is pinned
directly by sha256 (README, selection JSON, win-finding JSON, status.log,
5 target input CSVs - each cross-checked byte-equal to the SK kit's
MANIFEST-pinned gate input - and all 20 raw CSV files).  The 5 adopted
(lo,hi) pairs are proven absent from BASE (fresh-increment gate), absent
from the active quarantine registry and canonical-safe per
s5_evidence_policy; the adopted-table digest and the emitted increment
sha are self-pinned.  The standing unconsumed LOSS labels of the same
ladder (k01 15M 10,369,650, k06 15M 8,182,231, k07 2M 1,419,823) are
recorded but NOT adopted and NOT emitted: this dossier adopts no LOSS row.

WIN-only adoption asserts no root verdict and frees no class; owner
classes of the adopted keys may be excluded_now by the win-hit mechanism,
and all scheduling effects remain to be derived only by the reaudit
refresh (Board fail-closed child verification).  The standard 11x11
empty board and every central-reply root stay UNKNOWN; nodes are
bookkeeping, never verdicts.
"""
import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
MERGER = EXP / "scripts/s5_union_merge.py"

EM_EXP = "n11-centralreply-emloss21-adoption-predecl-20261126"
PROBE_EXP = "n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121"
SK_EXP = "n11-sixthcost-exclusive-cppgate-20261126"
TI_EXP = "n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122"
THIRDIM_EXP = "n11-sixthcost-third-implementation-verdict-reverification-20261121"

BASE_CACHE = ROOT / "research/experiments" / EM_EXP / (
    "output/merged-exact-s5-chain-plus-emloss21-20261126.cache")
PROBE_DIR = ROOT / "research/experiments" / PROBE_EXP
SK_DIR = ROOT / "research/experiments" / SK_EXP
TI_DIR = ROOT / "research/experiments" / TI_EXP
THIRDIM_DIR = ROOT / "research/experiments" / THIRDIM_EXP
GRAPH = (ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"
         "/output/dependency-graph.json.gz")
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
POLICY = (ROOT / "research/experiments/n11-frontier-selection-20261005"
          "/scripts/s5_evidence_policy.py")

MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA_EXPECTED = "6e49dd841b7bfcb335d86ef2479c95f47ab7acbcf41ace389a8b8eb95c778c9d"
BASE_CACHE_ROWS_EXPECTED = 6792
BASE_CACHE_WIN_EXPECTED = 192
BASE_CACHE_LOSS_EXPECTED = 6600
QUARANTINE_SHA_EXPECTED = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
POLICY_SHA_EXPECTED = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
GRAPH_SHA_EXPECTED = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"

# probe kit direct pins (kit predates MANIFESTs; the 20261121 kit holds none)
PROBE_README_SHA = "95cc5399a5c04b8db95decc450379c7b4489edc107147328eec4b9cb2f41c113"
PROBE_SELECTION_SHA = "d5e9b059611849f7b7e69c7370a0e66cd7535c43b3a043ce9f5bfc0e5ff72e87"
PROBE_WINFINDING_K08_SHA = "be662d23e68dcc99731aa707b35b676893f949d8acf3bb2ba9de8d902fa5ce05"
PROBE_STATUS_SHA = "2a253d081bf439960089ffb39b1934f0b4696a78d4750155ea26e60207fbd7b8"
PROBE_BUDGET = 15000000
PROBE_2M_BUDGET = 2000000

# (lo, hi, legal, s5_index, order_position) - machine-derived from the
# published selection JSON exclusive_probe_order, cross-gated below
# against the raw replay rows and the frozen dependency graph.
PROBE_KEY_PINS = {
    "k02": (1297036692683751424, 68157440, 87, 64872, 1),
    "k03": (10376293541461626880, 65792, 81, 96472, 2),
    "k04": (10376293541461626888, 65536, 83, 112201, 3),
    "k05": (10376293541461757952, 65536, 88, 91506, 4),
    "k08": (10376293610182148096, 68719476736, 89, 39127, 7),
}

# (result, nodes) of the resolving 15M condition per adopted key -
# machine-derived from the published raws, cross-gated below.
PROBE_LABEL_PINS = {
    "k02": (1, 7717432),
    "k03": (1, 9255414),
    "k04": (1, 9433024),
    "k05": (1, 13397611),
    "k08": (1, 6195897),
}

# standing unconsumed LOSS labels of the same ladder - recorded, NOT
# adopted, NOT emitted (the raw honest labels of the probe kit SSOT).
LOSS_LABEL_PINS = {
    "k01": (15000000, 2, 10369650),
    "k06": (15000000, 2, 8182231),
    "k07": (2000000, 2, 1419823),
}

PROBE_INPUT_SHAS = {
    "k02": "b6174a3fa73687af2820fd3eee16d750ca0d43ac7c2a1ea063a392710ce73887",
    "k03": "9e40900a8df77e9ce139359ec289d664c08b8f9010d50e80149b4e9e624a3b40",
    "k04": "110776a29b4a9ce4fa0b61c47fc2a586e3475bdd94328db77b506ae8456a80a4",
    "k05": "7f30311de61973274163246fb9502b65922788da868b47165ef86646ebb3e750",
    "k08": "6fcbf158817f25e82ebb73010c49638949aa2f8ff9d48713d4806a2d4426c35f",
}

PROBE_RAW_SHAS = {
    "at2m-k02.out.csv": "ae2df9689268e1c61b9f814baad991d54ee4907779349ec4c7f07345d0ca2871",
    "at15m-run1-k02.out.csv": "29c9a80fdbcbe3b032b44d5c2763e8dd6c2d44abb293d067031a23c75779dfea",
    "at15m-run2-k02.out.csv": "29c9a80fdbcbe3b032b44d5c2763e8dd6c2d44abb293d067031a23c75779dfea",
    "at15m-run3-verify-k02.out.csv": "29c9a80fdbcbe3b032b44d5c2763e8dd6c2d44abb293d067031a23c75779dfea",
    "at2m-k03.out.csv": "ecd00db9ce475fda0adb57374c9c90624634387dd59eb51ccdca6b07713c3216",
    "at15m-run1-k03.out.csv": "a1c51cdf3b4a7601b5afabf3c558127f3b762f1f3c87785c695a7ffe5d6b7151",
    "at15m-run2-k03.out.csv": "b17652530797f7ecca37668ae22145ae538afc498c5795a58846c87902c5cd32",
    "at15m-run3-verify-k03.out.csv": "27169f87a60b7600967e413433dc6fee12ca555b7a20f098ba61f09523e3b924",
    "at2m-k04.out.csv": "e97fd079a6902287d992c68246b92817694f735f7273ef9f05e89b162b4a497e",
    "at15m-run1-k04.out.csv": "c10896543282f563deeddf31af994465c9f5fac465c734fa22339a47dc81ca61",
    "at15m-run2-k04.out.csv": "7c12138c13d8ff5f256a51d3a311994248e405e05f0780678e86a008daac1e8e",
    "at15m-run3-verify-k04.out.csv": "492f758e4b2a6e1eb1e7a48df697979b39a83f180ecc6d9aa124700c98e1a4ec",
    "at2m-k05.out.csv": "6be638e623dcd3275cfb9cce04bebe447fbf3fa93dad33f8c30508b635f87297",
    "at15m-run1-k05.out.csv": "dde1e4f0eae6a0557f0a6da7fd54f43f8ab4749c0321c16eba8f4586ee743df8",
    "at15m-run2-k05.out.csv": "562e2c9d3cfd7596e63a4f4d101c40ea6ea7dd66abfe5339cc095c6a0e408a2c",
    "at15m-run3-verify-k05.out.csv": "1305562baff3d171ff24df0befd6dc519147b77dc3648f78580b7e039d6f9381",
    "at2m-k08.out.csv": "274e02b011464194f397d5fda587aafe02b03d875d1c9e2f205438d9684f1c12",
    "at15m-run1-k08.out.csv": "b015a80c41c2aeb21c4c387c433d3a119569590c10907c8038d76e4e6c677044",
    "at15m-run2-k08.out.csv": "b015a80c41c2aeb21c4c387c433d3a119569590c10907c8038d76e4e6c677044",
    "at15m-run3-verify-k08.out.csv": "61d5379bccde66b43dc1bda2bf640a02152faeeeaa83cf982889ad4b8c732481",
}

# Part SK C++ second-implementation gate kit (MANIFEST-verified)
SK_MANIFEST_SHA = "8d84b1a58348b86a3bf8ca4b2d54c957b3c39683a745e52c5e33d2db19b5562a"
SK_KIT_FILES = 46
SK_GATEROWS_SHA = "11fb829c10d489f90d9a05f322356168089a80bf1d0128343a054e14221d52d1"
SK_STATUS_SHA = "f24f3766579c13f91addc12c277d201d2791bd2a2bef8e1985350e91b7421ba8"
SK_AUDIT_SHA = "ad139eceee6bd9e9c349410bf7e4b823a61dfaaf31b23df5b0438431f6bc3629"
SK_GATES_TOTAL = 178

# TI third-implementation kit (MANIFEST.sha256, repo-root-relative paths)
TI_MANIFEST_SHA = "538f8ec7e2a5eba71a4a1c4368d76ac1f5f2b77927759c6a26d592fde9c5342c"
TI_MANIFEST_LINES = 344
TI_KIT_PREFIX = ("research/experiments/"
                 "n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122/")
TI_AUDIT_FILE = {
    "k03": "out/audit-summary.json",
    "k04": "out/audit-k04-summary.json",
    "k05": "out/audit-k05-summary.json",
    "k08": "out/audit-k06k07k08-summary.json",
}
TI_AUDIT_SHAS = {
    "out/audit-summary.json": "c24da5cdef97717252f8152315b13087ff2a60fe5da66a944c5390aa7b7ad8de",
    "out/audit-k04-summary.json": "5116045c07686dda8bcf6067d3d9b305a247cf23a25234e2563efd1d8052d84b",
    "out/audit-k05-summary.json": "15373d0655ac1b17b0ac89b3a536dc5747e0b4451d25923beca47070fabb3daf",
    "out/audit-k06k07k08-summary.json": "6cb112f8b6e4232976c65b8e65205f9e87ee943ad88282c7ce28edba2100bf2f",
}
TI_THIRD_IMPL_SHA = "08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998"
TI_DETERMINISM_PINS = {
    "k03": [("1", "10896601", "5996958")] * 3,
    "k04": [("1", "11020407", "6092599")] * 3,
    "k05": [("1", "15949585", "8391212")] * 3,
    "k08": [("1", "7243596", "3873045")] * 3,
}
TI_UNANIMOUS_PINS = {
    "k03": [("1", "9255414")] * 3,
    "k04": [("1", "9433024")] * 3,
    "k05": [("1", "13397611")] * 3,
    "k08": [("0", "2000000"), ("1", "6195897"),
            ("1", "6195897"), ("1", "6195897")],
}

# ea73c3e3 fixed third-implementation kit (k02, 4 witness runs)
THIRDIM_README_SHA = "1a3ddd07f6907524f7ea1562ac58f4e7d9ae210e3279b4b9ecbe643ca6196ce4"
THIRDIM_THIRD_IMPL_SHA = TI_THIRD_IMPL_SHA
THIRDIM_WITNESS_SHAS = {
    "out/witness/out-k02-a.txt": "bbce3433c184738052f078ffc0e83dd563de79bda0aba054b0b35b1e1602b50d",
    "out/witness/out-k02-b.txt": "a0eec80f2f6c47f815469a2146b8f18055b163f8e95ff964114fb2956fcef7ea",
    "out/witness/out-k02-g.txt": "98e9427fe73e2b48cda5b082396851b3a5b3066d30398be3a4b1ed26186079f0",
    "out/witness/out-k02-v.txt": "7a490ad4046a422c06dfffd206ff75ecc191d43b6e60e768b2d42beadd0a1300",
}
K02_THIRD_IMPL_EXPANSIONS = 9106337

ADOPTED_IDS = ["k02", "k03", "k04", "k05", "k08"]
ADOPTED_NODES_TOTAL = 45999378
ADOPTED_TABLE_DIGEST = "b6ea1bcc10829498add9c87bb874b18dd95904ddf83f022ee67af06c06d93b0c"
ADOPTED_INCREMENT_SHA = "44c16a28f944e255d3968f49a16cc61e06f70269ada833fe976f1607b7d40b03"
SERVING_CLASS = 3077
CLASS_MASK = (10376293541461626880, 65536)

INCREMENT_NAME = "increment-sixthwin5-20261126.cache"
SIXTHWIN5_SCHEMA = "sixthwin5-increments-manifest-v1"

HDR_LINES = [
 "# n11 central-reply closure sixthwin5 PREDECL DOSSIER increment",
 "#   (dossier n11-centralreply-sixthwin5-adoption-predecl-20261126,",
 "#   2026-11-26) - WIN-only, fresh 5-row increment.  This is NOT a",
 "#   Part: no declaration, no adoption, no verdict consumption.  The",
 "#   canonical head stays merged-exact-s5-chain-plus-emloss21",
 "#   (6e49dd84..., 6,792 rows WIN 192 / LOSS 6,600).",
 "# The 5 unconsumed sixth-cost exclusive-probe WIN rows of record (the",
 "#   probe kit n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-",
 "#   20261121 ladder, class 10376293541461626880:65536, budget 15,000,000",
 "#   order 0, two-pass fresh-cold node-exact plus a voluntary third",
 "#   cold verify run, all identical in (result, nodes)): k02, k03,",
 "#   k04, k05 and k08 - each corroborated verdict-level by the",
 "#   published C++ second-implementation gate (Part SK kit, all rows",
 "#   GATE-PASS, 2-pass node-exact) and by an independent third",
 "#   implementation (k02: the ea73c3e3 fixed-implementation kit's",
 "#   4-run witness; k03/k04/k05/k08: the TI kit audits' verdict-level",
 "#   WIN agreement).",
 "# NOT consumed by this dossier and NOT emitted (each remains an",
 "#   unconsumed honest standing label, no LOSS adoption is declared",
 "#   here): k01 (LOSS, 15M, 10,369,650), k06 (LOSS, 15M, 8,182,231)",
 "#   and k07 (LOSS, 2M, 1,419,823).",
 "# WIN-only adoption, if a future Part declares it, asserts no root",
 "#   verdict and frees no class; owner classes of the adopted keys may",
 "#   be excluded_now by the win-hit mechanism, and all scheduling",
 "#   effects are derived only by the reaudit refresh (Board fail-closed",
 "#   child verification) and the census delta extractor.  The standard",
 "#   11x11 empty board and every central-reply root stay UNKNOWN;",
 "#   nodes are bookkeeping, never verdicts.",
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sys_exit(msg: str):
    print(f"ABORT {msg}", file=sys.stderr)
    raise SystemExit(1)


def parse_replay(path: Path):
    row = None
    rows_seen = 0
    txt = path.read_text()
    for line in txt.splitlines():
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
    if "# replay_done" not in txt:
        sys_exit(f"{path} lacks the '# replay_done' completeness guard")
    return row


def payload_eq(a: dict, b: dict, what: str):
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
    if tuple(a[f] for f in fields) != tuple(b[f] for f in fields):
        sys_exit(f"{what}: payload mismatch (fresh multi-pass node-exact gate)")


def load_manifest_2field(path: Path, what: str):
    entries = {}
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split(None, 1)
        if len(fields) != 2:
            sys_exit(f"{what} MANIFEST malformed line: {line}")
        want, rel = fields
        if rel.startswith("/") or ".." in rel.split("/") or "\x00" in rel:
            sys_exit(f"{what} MANIFEST unsafe path: {rel}")
        if rel in entries:
            sys_exit(f"{what} MANIFEST duplicate path: {rel}")
        entries[rel] = want
    return entries


def main() -> None:
    # --- anchors: base cache, merger, quarantine, policy, graph -----------
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys_exit("base cache (Part EM head) sha drift")
    if sha(MERGER) != MERGER_SHA_EXPECTED:
        sys_exit("fail-closed union merger (scripts/s5_union_merge.py) sha "
                 "drift: this dossier must use the pinned merger byte-for-byte")
    if sha(QUARANTINE) != QUARANTINE_SHA_EXPECTED:
        sys_exit("quarantine registry sha drift")
    if sha(POLICY) != POLICY_SHA_EXPECTED:
        sys_exit("evidence policy sha drift")
    if sha(GRAPH) != GRAPH_SHA_EXPECTED:
        sys_exit("frozen dependency graph sha drift")
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

    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s4_masks = g["s4_masks"]
    s5_masks = g["s5_masks"]
    s4_cost = g["s4_cost"]
    mask_to_index = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}
    serving_mask_classes = [ci for ci, m in enumerate(s4_masks)
                            if tuple(m) == CLASS_MASK]
    if serving_mask_classes != [SERVING_CLASS]:
        sys_exit(f"serving-class mask lookup drift: {serving_mask_classes}")

    # --- probe kit: direct byte pins (no MANIFEST; pin everything) -------
    if not PROBE_DIR.is_dir():
        sys_exit(f"probe kit dir missing {PROBE_DIR}")
    if sha(PROBE_DIR / "README.md") != PROBE_README_SHA:
        sys_exit("probe kit README sha drift")
    if sha(PROBE_DIR / "output/sixth-cost-exclusive-keys.json") != PROBE_SELECTION_SHA:
        sys_exit("probe kit selection JSON sha drift")
    if sha(PROBE_DIR / "output/win-finding-ifadopted-k08.json") != \
            PROBE_WINFINDING_K08_SHA:
        sys_exit("probe kit win-finding-ifadopted-k08.json sha drift")
    sel = json.loads((PROBE_DIR / "output/sixth-cost-exclusive-keys.json")
                     .read_text())
    if sel["schema"] != "n11-sixthcost-exclusive-selection-v1":
        sys_exit("probe selection schema drift")
    if sel["class"] != f"{CLASS_MASK[0]}:{CLASS_MASK[1]}":
        sys_exit("probe selection class drift")
    if sel["class_children_total"] != 108 or sel["s5_unknown_before"] != 101:
        sys_exit("probe selection class census drift")
    if sel["unknown_exclusive"] != 43 or len(sel["exclusive_probe_order"]) != 43:
        sys_exit("probe selection exclusive list drift")
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, pos = PROBE_KEY_PINS[kid]
        entry = sel["exclusive_probe_order"][pos]
        if entry["key"] != f"{lo}:{hi}" or entry["legal"] != legal:
            sys_exit(f"probe selection order-position disagreement: {kid}")
    wf = json.loads((PROBE_DIR / "output/win-finding-ifadopted-k08.json")
                    .read_text())
    fnd = wf["finding"]
    if fnd["win_child_key"] != f"{PROBE_KEY_PINS['k08'][0]}:{PROBE_KEY_PINS['k08'][1]}":
        sys_exit("win-finding k08 json child key drift")
    if [(r["budget"], r["result"], r["nodes"]) for r in fnd["win_runs"]] != [
            (PROBE_2M_BUDGET, 0, 2000000),
            (PROBE_BUDGET, 1, 6195897), (PROBE_BUDGET, 1, 6195897),
            (PROBE_BUDGET, 1, 6195897)]:
        sys_exit("win-finding k08 json win_runs ladder drift")
    if fnd["verdict_consumed"] is not False:
        sys_exit("win-finding k08 json verdict_consumed drift")
    if "expected result 1, nodes 6,195,897" not in fnd["adoption_requirement"]:
        sys_exit("win-finding k08 json adoption requirement drift")

    # probe kit status.log: SSOT stage lines for the adopted keys
    if sha(PROBE_DIR / "output/raw/status.log") != PROBE_STATUS_SHA:
        sys_exit("probe kit status.log sha drift")
    slines = (PROBE_DIR / "output/raw/status.log").read_text().splitlines()
    for line in slines:
        parts = line.split()
        if parts and parts[0] == "note":
            continue
        if not (parts and (parts[0] in ("done", "start", "key"))):
            sys_exit(f"probe status.log unexpected line: {line}")
    want_stage_lines = {
        "k02": ["done 2 2m rc=0", "done 2 15m-run1 rc=0",
                "done 2 15m-run2 rc=0"],
        "k03": ["done 03 2m rc=0 res=0", "done 03 15m-run1 rc=0",
                "done 03 15m-run2 rc=0", "done 03 15m-run3-verify rc=0"],
        "k04": ["done 04 2m rc=0 res=0", "done 04 15m-run1 rc=0",
                "done 04 15m-run2 rc=0", "done 04 15m-run3-verify rc=0"],
        "k05": ["done 05 2m rc=0 res=0", "done 05 15m-run1 rc=0",
                "done 05 15m-run2 rc=0", "done 05 15m-run3-verify rc=0"],
        "k08": ["done 08 2m rc=0 res=0", "done 08 15m-run1 rc=0",
                "done 08 15m-run2 rc=0", "done 08 15m-run3-verify rc=0"],
    }
    for kid, wanted in want_stage_lines.items():
        for w in wanted:
            if w not in slines:
                sys_exit(f"probe status.log missing stage line: {kid}: {w}")
    if "key 02 status=done res2m=0" not in slines:
        sys_exit("probe status.log missing key 02 status line")
    if "key 03 status=WIN-halt res2m=0" not in slines or \
       "key 04 status=WIN-halt res2m=0" not in slines or \
       "key 05 status=WIN-halt res2m=0" not in slines or \
       "key 08 status=WIN-halt res2m=0" not in slines:
        sys_exit("probe status.log missing WIN-halt status line(s)")

    # probe kit target input CSVs: direct pins (byte-equality with the SK
    # kit's MANIFEST-pinned gate inputs asserted after the SK verification)
    for kid in ADOPTED_IDS:
        p = PROBE_DIR / f"input/{kid}.input.csv"
        if not p.is_file():
            sys_exit(f"probe kit input CSV missing: {p.name}")
        if sha(p) != PROBE_INPUT_SHAS[kid]:
            sys_exit(f"probe kit input CSV sha drift: {kid}")
        lo, hi, legal, _s5, _pos = PROBE_KEY_PINS[kid]
        fields = p.read_text().strip().split(",")
        if fields != ["target", "0", "5", str(lo), str(hi), str(legal),
                      "0", "0", "0", "0", "0"]:
            sys_exit(f"probe kit input CSV target drift: {kid}")

    # probe kit raws: 2M honest-UNKNOWN first stage + resolving 15M
    # two-pass + voluntary third verify run, all byte-pinned
    probe_rows = {}
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos = PROBE_KEY_PINS[kid]
        raw_files = {
            "at2m": PROBE_DIR / f"output/raw/at2m-{kid}.out.csv",
            "run1": PROBE_DIR / f"output/raw/at15m-run1-{kid}.out.csv",
            "run2": PROBE_DIR / f"output/raw/at15m-run2-{kid}.out.csv",
            "run3": PROBE_DIR / f"output/raw/at15m-run3-verify-{kid}.out.csv",
        }
        raw_names = {"at2m": f"at2m-{kid}.out.csv",
                     "run1": f"at15m-run1-{kid}.out.csv",
                     "run2": f"at15m-run2-{kid}.out.csv",
                     "run3": f"at15m-run3-verify-{kid}.out.csv"}
        for tag, p in raw_files.items():
            if not p.is_file():
                sys_exit(f"probe raw missing: {p.name}")
            if sha(p) != PROBE_RAW_SHAS[raw_names[tag]]:
                sys_exit(f"probe raw sha drift ({tag}): {kid}")
        parsed = {tag: parse_replay(p) for tag, p in raw_files.items()}
        r2m = parsed["at2m"]
        if (r2m["stones"], r2m["is_or"], r2m["budget"], r2m["result"],
                r2m["nodes"]) != (5, 0, PROBE_2M_BUDGET, 0, PROBE_2M_BUDGET):
            sys_exit(f"{kid}: 2M honest-UNKNOWN ladder stage drift")
        for tag in ("run1", "run2", "run3"):
            r = parsed[tag]
            if (r["stones"], r["is_or"], r["budget"]) != (5, 0, PROBE_BUDGET):
                sys_exit(f"{kid}: wrong depth/or/budget ({tag})")
            if r["legal"] != legal or r["lo"] != str(lo) or r["hi"] != str(hi):
                sys_exit(f"{kid}: legal/key disagreement raw vs pinned ({tag})")
        payload_eq(parsed["run1"], parsed["run2"], f"{kid} 15m")
        payload_eq(parsed["run1"], parsed["run3"], f"{kid} 15m-run3-verify")
        if (parsed["run1"]["result"], parsed["run1"]["nodes"]) != \
                PROBE_LABEL_PINS[kid]:
            sys_exit(f"{kid}: 15M honest-label drift vs pinned label")
        probe_rows[kid] = parsed["run1"]
    if set(LOSS_LABEL_PINS) & set(ADOPTED_IDS):
        sys_exit("internal pin collision")
    adopted_nodes = sum(PROBE_LABEL_PINS[kid][1] for kid in ADOPTED_IDS)
    if adopted_nodes != ADOPTED_NODES_TOTAL:
        sys_exit(f"adopted node total drift {adopted_nodes} "
                 f"!= {ADOPTED_NODES_TOTAL}")

    # --- Part SK C++ second-implementation gate kit, file-by-file -------
    if not SK_DIR.is_dir():
        sys_exit(f"Part SK kit dir missing {SK_DIR}")
    if sha(SK_DIR / "MANIFEST-sha256.txt") != SK_MANIFEST_SHA:
        sys_exit("Part SK kit MANIFEST sha drift")
    sk_manifest_shas = load_manifest_2field(SK_DIR / "MANIFEST-sha256.txt",
                                             "Part SK")
    if len(sk_manifest_shas) != SK_KIT_FILES:
        sys_exit(f"Part SK kit files verified {len(sk_manifest_shas)} "
                 f"!= {SK_KIT_FILES}")
    for rel, want in sk_manifest_shas.items():
        p = SK_DIR / rel
        if not p.is_file():
            sys_exit(f"Part SK kit file missing: {rel}")
        if sha(p) != want:
            sys_exit(f"Part SK kit file sha drift: {rel}")
    for kid in ADOPTED_IDS:
        a = sk_manifest_shas.get(f"input/{kid}.input.csv")
        if a is None or a != PROBE_INPUT_SHAS[kid]:
            sys_exit(f"{kid}: SK gate input CSV is not byte-equal to the "
                     "probe kit's target CSV (cross-registration)")
    if sha(SK_DIR / "input/gate-rows.json") != SK_GATEROWS_SHA:
        sys_exit("Part SK gate-rows.json sha drift")
    gr = json.loads((SK_DIR / "input/gate-rows.json").read_text())
    if gr["schema"] != "n11-sixthcost-exclusive-cppgate-rows-v1":
        sys_exit("Part SK gate-rows schema drift")
    if gr["part"] != "SK":
        sys_exit("Part SK gate-rows part drift")
    ch = gr["canonical_head"]
    if (ch["label"] != "6e49dd84" or ch["sha256"] != BASE_CACHE_SHA_EXPECTED
            or ch["rows"] != BASE_CACHE_ROWS_EXPECTED
            or ch["census"] != {"WIN": BASE_CACHE_WIN_EXPECTED,
                                "LOSS": BASE_CACHE_LOSS_EXPECTED}):
        sys_exit("Part SK gate-rows canonical-head block drift")
    if len(gr["gates"]) != SK_GATES_TOTAL or any(
            v["status"] != "PASS" for v in gr["gates"].values()):
        sys_exit("Part SK gate-rows 178-gate table not all PASS")
    if sha(SK_DIR / "output/gate-status.log") != SK_STATUS_SHA:
        sys_exit("Part SK gate-status.log sha drift")
    gk_map = {}
    for line in (SK_DIR / "output/gate-status.log").read_text().splitlines():
        parts = line.split()
        if len(parts) < 4 or " ".join(parts[2:3]) != "GATE-PASS" \
                or not parts[3].replace(",", "").isdigit():
            sys_exit(f"Part SK gate-status unexpected line: {line}")
        gk_map[parts[1]] = parts[3]
    if len(gk_map) != 11:
        sys_exit("Part SK gate-status must carry exactly 11 GATE-PASS rows")
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos = PROBE_KEY_PINS[kid]
        res, nodes = PROBE_LABEL_PINS[kid]
        if gk_map.get(kid) != f"{legal},{PROBE_BUDGET},{res},{nodes}":
            sys_exit(f"Part SK gate-status row drift: {kid}")
    for rel in ("output/audit_gate.json", "output/audit_gate.run1.json",
                "output/audit_gate.run2.json", "output/audit_gate.run3.json"):
        if sk_manifest_shas.get(rel) != SK_AUDIT_SHA:
            sys_exit(f"Part SK audit json sha drift: {rel}")
    ag = json.loads((SK_DIR / "output/audit_gate.json").read_text())
    if ag["overall"] != "PASS":
        sys_exit("Part SK audit_gate.json overall drift")
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos = PROBE_KEY_PINS[kid]
        res, nodes = PROBE_LABEL_PINS[kid]
        row = ag["rows"].get(kid)
        if row is None or row["expected"] != f"{legal},{PROBE_BUDGET},{res},{nodes}" \
                or row["observed_p1"] != row["expected"]:
            sys_exit(f"Part SK audit_gate row drift: {kid}")
    # SK raw payload gate (bytes already MANIFEST-verified; payload here)
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos = PROBE_KEY_PINS[kid]
        res, nodes = PROBE_LABEL_PINS[kid]
        s1 = parse_replay(SK_DIR / f"output/raw/{kid}.p1.out")
        s2 = parse_replay(SK_DIR / f"output/raw/{kid}.p2.out")
        payload_eq(s1, s2, f"SK {kid}")
        if (s1["stones"], s1["is_or"], s1["budget"], s1["result"],
                s1["nodes"]) != (5, 0, PROBE_BUDGET, res, nodes):
            sys_exit(f"{kid}: SK C++ gate honest-label drift")
        if s1["legal"] != legal or s1["lo"] != str(lo) or s1["hi"] != str(hi):
            sys_exit(f"{kid}: SK C++ gate legal/key drift")

    # --- TI third-implementation kit: MANIFEST + 4 audit summaries -------
    if not TI_DIR.is_dir():
        sys_exit(f"TI kit dir missing {TI_DIR}")
    if sha(TI_DIR / "MANIFEST.sha256") != TI_MANIFEST_SHA:
        sys_exit("TI kit MANIFEST.sha256 drift")
    ti_lines = [l for l in (TI_DIR / "MANIFEST.sha256").read_text().splitlines()
                if l.strip()]
    if len(ti_lines) != TI_MANIFEST_LINES:
        sys_exit(f"TI MANIFEST line count {len(ti_lines)} != {TI_MANIFEST_LINES}")
    ti_map = {}
    for line in ti_lines:
        fields = line.split(None, 1)
        if len(fields) != 2:
            sys_exit(f"TI MANIFEST malformed line: {line}")
        want, rel = fields
        if not rel.startswith("research/experiments/"):
            sys_exit(f"TI MANIFEST unexpected repo-root-relative path: {rel}")
        if rel in ti_map:
            sys_exit(f"TI MANIFEST duplicate path: {rel}")
        ti_map[rel] = want
    # the TI kit covers k03/k04/k05/k08 inputs (k02's third-impl kit is the
    # ea73c3e3 one; its witness rows pin the target inline)
    for kid in ("k03", "k04", "k05", "k08"):
        rel = f"{TI_KIT_PREFIX}input/{kid}.input.csv"
        if rel not in ti_map:
            sys_exit(f"TI kit pin missing for {kid} input CSV")
        if ti_map[rel] != PROBE_INPUT_SHAS[kid]:
            sys_exit(f"{kid}: TI input CSV pin drift (not byte-equal to the "
                     "probe kit's target CSV)")
    for kid in ("k03", "k04", "k05", "k08"):
        audit_file = TI_AUDIT_FILE[kid]
        rel = TI_KIT_PREFIX + audit_file
        if ti_map.get(rel) != TI_AUDIT_SHAS[audit_file]:
            sys_exit(f"TI MANIFEST pin drift: {audit_file}")
        p = TI_DIR / audit_file
        if sha(p) != TI_AUDIT_SHAS[audit_file]:
            sys_exit(f"TI audit summary sha drift: {audit_file}")
        a = json.loads(p.read_text())
        if a["all_pass"] is not True or a["consumed"] is not False:
            sys_exit(f"TI audit summary all_pass/consumed drift: {kid}")
        if "remain UNKNOWN" not in a["claim"]:
            sys_exit(f"TI audit summary UNKNOWN-guard drift: {kid}")
        gates = a["gates"]
        det = gates.get(f"C2_{kid}_determinism_3runs_identical")
        if det is None or det.get("pass") is not True \
                or det["detail"] != str(TI_DETERMINISM_PINS[kid]):
            sys_exit(f"TI determinism triplet drift: {kid} ({det})")
        una = gates.get(f"repl_{kid}_win_3runs_unanimous")
        if una is None or una.get("pass") is not True \
                or una["detail"] != str(TI_UNANIMOUS_PINS[kid]):
            sys_exit(f"TI replica unanimity drift: {kid} ({una})")
        agree = gates.get(f"C2_{kid}_win_verdict_level_vs_replica")
        if agree is None or agree.get("pass") is not True:
            sys_exit(f"TI verdict-level agreement gate drift: {kid}")
        lo, hi, legal, _s5, _pos = PROBE_KEY_PINS[kid]
        res, nodes = PROBE_LABEL_PINS[kid]
        # replica raw rows inside the TI audit must equal the probe pins
        # (detail separator varies by audit: ',' or ' | ')
        for stage, (budget, sres, snodes) in (
                ("at2m", (PROBE_2M_BUDGET, 0, PROBE_2M_BUDGET)),
                ("at15m-run1", (PROBE_BUDGET, res, nodes)),
                ("at15m-run3-verify", (PROBE_BUDGET, res, nodes))):
            gn = f"repl_row_{stage}-{kid}.out.csv"
            rowgate = gates.get(gn)
            if rowgate is None or rowgate.get("pass") is not True:
                sys_exit(f"TI replica raw pin gate missing: {kid} {gn}")
            fields = [x.strip() for x in rowgate["detail"]
                      .replace("|", ",").split(",") if x.strip()]
            if len(fields) != 11 or fields[0] != "replay":
                sys_exit(f"TI replica raw row malformed: {kid} {gn}")
            if (int(fields[2]), int(fields[3]), int(fields[4]), int(fields[5]),
                    int(fields[6]), int(fields[7]), fields[9], fields[10]) != \
                    (5, legal, 0, budget, sres, snodes, str(lo), str(hi)):
                sys_exit(f"TI replica raw row payload drift: {kid} {gn}")

    # --- ea73c3e3 fixed third-implementation kit (k02, 4 witness runs) ---
    if not THIRDIM_DIR.is_dir():
        sys_exit(f"third-impl kit dir missing {THIRDIM_DIR}")
    if sha(THIRDIM_DIR / "README.md") != THIRDIM_README_SHA:
        sys_exit("ea73c3e3 kit README sha drift")
    tim_manifest = load_manifest_2field(THIRDIM_DIR / "MANIFEST.sha256",
                                         "ea73c3e3")
    if sha(THIRDIM_DIR / "third_impl.js") != THIRDIM_THIRD_IMPL_SHA:
        sys_exit("ea73c3e3 third_impl.js sha drift")
    if tim_manifest.get("third_impl.js") != THIRDIM_THIRD_IMPL_SHA:
        sys_exit("ea73c3e3 MANIFEST third_impl.js pin drift")
    k02_lo, k02_hi, k02_legal, _s5, _pos = PROBE_KEY_PINS["k02"]
    witness_rows = 0
    for rel, want in THIRDIM_WITNESS_SHAS.items():
        p = THIRDIM_DIR / rel
        if not p.is_file():
            sys_exit(f"ea73c3e3 witness file missing: {rel}")
        if sha(p) != want:
            sys_exit(f"ea73c3e3 witness file sha drift: {rel}")
        if tim_manifest.get(rel) != want:
            sys_exit(f"ea73c3e3 MANIFEST witness pin drift: {rel}")
        line = p.read_text().strip()
        parts = line.split(",")
        # third,k02*,5,-1,87,1,9106337,4991527,27.12,<lo>,<hi>,clean,...
        if parts[0] != "third" or int(parts[2]) != 5 \
                or int(parts[4]) != k02_legal \
                or int(parts[5]) != 1 \
                or int(parts[6]) != K02_THIRD_IMPL_EXPANSIONS \
                or parts[9] != str(k02_lo) or parts[10] != str(k02_hi) \
                or parts[11] != "clean":
            sys_exit(f"ea73c3e3 witness row drift: {rel}: {line}")
        witness_rows += 1
    if witness_rows != 4:
        sys_exit("k02 needs exactly 4 third-impl witness runs (a/b/g/v)")

    # --- freshness: BASE absence, quarantine, canonical safety ----------
    adopted_rows = []
    for kid in ADOPTED_IDS:
        ref = probe_rows[kid]
        if ref["result"] != 1:
            sys_exit(f"{kid}: adopted row must be exact WIN")
        (lo, hi, legal, s5_index, _pos) = PROBE_KEY_PINS[kid]
        if (int(ref["lo"]), int(ref["hi"])) != (lo, hi):
            sys_exit(f"{kid}: raw key vs pinned key disagreement")
        if ref["legal"] != legal:
            sys_exit(f"{kid}: raw legal vs pinned legal disagreement")
        if mask_to_index.get((lo, hi)) != s5_index:
            sys_exit(f"{kid}: s5_index round-trip drift vs the frozen graph")
        owners = [ci for ci in range(len(s4_masks)) if s5_index in s4_cost[ci]]
        if SERVING_CLASS not in owners:
            sys_exit(f"{kid}: serving class must own the key at graph time")
        if ref["nodes"] != PROBE_LABEL_PINS[kid][1]:
            sys_exit(f"{kid}: node drift")
        key = (lo, hi)
        if key in quarantined:
            sys_exit(f"{kid}: quarantined key {key}")
        if not is_canonical_safe_s5_key(key):
            sys_exit(f"{kid}: noncanonical/unsafe key {key}")
        if key in base_keys:
            sys_exit(f"{kid}: key already in canonical BASE; "
                     "fresh-increment gate")
        adopted_rows.append((lo, hi, legal, 1, ref["nodes"], s5_index,
                             SERVING_CLASS, owners))
    if len({(r[0], r[1]) for r in adopted_rows}) != 5:
        sys_exit("adopted pairs must be exactly 5 distinct keys")

    digest = hashlib.sha256("\n".join(
        f"{lo},{hi},{legal},{result},{nodes}"
        for lo, hi, legal, result, nodes, _s5, _cls, _own in
        sorted(adopted_rows)).encode()).hexdigest()
    if digest != ADOPTED_TABLE_DIGEST:
        sys_exit(f"adopted-table digest drift {digest}")

    # --- emit increment + manifest ---------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    rowlines = [f"s5verdict,{r[0]},{r[1]},5,1,{r[2]}"
                for r in sorted((lo, hi, nodes)
                                 for lo, hi, legal, result, nodes, _s5, _cls,
                                 _own in adopted_rows)]
    if len(rowlines) != 5:
        sys_exit("emitted row count drift")
    blob = ("\n".join(HDR_LINES + rowlines) + "\n").encode("utf-8")
    incr_sha = hashlib.sha256(blob).hexdigest()
    if incr_sha != ADOPTED_INCREMENT_SHA:
        sys_exit(f"emitted increment sha drift {incr_sha} "
                 f"!= pinned {ADOPTED_INCREMENT_SHA}")
    (OUT / INCREMENT_NAME).write_bytes(blob)

    adopted_table = [
        {"lo": lo, "hi": hi, "legal": legal, "result": 1, "nodes": nodes,
         "s5_index": s5_index, "serving_class": serving_class,
         "owner_classes_graph": owners}
        for lo, hi, legal, result, nodes, s5_index, serving_class, owners
        in sorted(adopted_rows)]

    manifest = {
        "schema": SIXTHWIN5_SCHEMA,
        "dossier_status": "PREDECL DOSSIER - NOT a Part: no declaration, no "
                          "adoption, no verdict consumption; the canonical head "
                          "stays merged-exact-s5-chain-plus-emloss21 6e49dd84... "
                          "and every sixthwin5 row of this increment stays an "
                          "unconsumed honest WIN label until a future "
                          "EV-pattern WIN-adoption Part says otherwise",
        "source_class": {
            "class": f"{CLASS_MASK[0]}:{CLASS_MASK[1]}",
            "class_children_total": 108, "s5_unknown_before": 101,
            "unknown_exclusive": 43, "serving_class_index": SERVING_CLASS,
            "note": "the sixth-cost live candidate class (s4 class 3077, "
                    "coverage {80,84,100,108}); WIN-elimination as a "
                    "LOSS-completion route for third moves {100,108} is the "
                    "documented motivation of the exclusive probe batch",
            "adoption_requirement_of_record":
                "the probe kit's pre-registered WIN-row requirement: published "
                "C++ second-implementation verification of the replica raw "
                "rows (pinned cpp/solvers/kyouen_dfpn_root.cpp sha256 "
                "9193f5b6...); satisfied for all 5 rows by the Part SK kit "
                "(all GATE-PASS); any C++ disagreement fails closed in favor "
                "of discarding the row",
        },
        "pools": [
            {"pool": "sixthcost-exclusive-probe",
             "kit": PROBE_EXP,
             "budget": PROBE_BUDGET,
             "first_stage_budget": PROBE_2M_BUDGET,
             "adopted_win_ids": list(ADOPTED_IDS),
             "standing_loss_ids_not_adopted": list(LOSS_LABEL_PINS),
             "standing_loss_labels": {k: list(v) for k, v in
                                      LOSS_LABEL_PINS.items()},
             "loss_adoption_note": "the 3 standing LOSS rows of the same "
                                   "ladder are NOT adopted and NOT emitted by "
                                   "this dossier; they remain unconsumed "
                                   "honest LOSS labels",
             "adopted_nodes": ADOPTED_NODES_TOTAL,
             "kit_integrity": {
                 "note": "the probe kit (2026-11-21) predates the repo "
                         "MANIFEST convention and holds no MANIFEST-sha256; "
                         "every consumed byte is pinned directly in this "
                         "manifest: README, the selection JSON, the k08 "
                         "win-finding JSON, status.log, the 5 target input "
                         "CSVs and all 20 raw CSV files "
                         "(raw_file_sha256_pins / input_csv_sha256_pins below)",
                 "readme_sha256": PROBE_README_SHA,
                 "selection_json_sha256": PROBE_SELECTION_SHA,
                 "win_finding_k08_json_sha256": PROBE_WINFINDING_K08_SHA,
                 "status_log_sha256": PROBE_STATUS_SHA,
                 "input_csv_sha256_pins": PROBE_INPUT_SHAS,
                 "raw_file_sha256_pins": PROBE_RAW_SHAS,
                 "input_csv_cross_registration":
                     "each of the 5 target input CSVs is byte-equal to the "
                     "Part SK kit's MANIFEST-pinned gate input and to the TI "
                     "kit's MANIFEST-pinned input",
             }},
            {"pool": "sk-cpp-second-implementation-gate",
             "kit": SK_EXP,
             "kit_integrity": {
                 "note": "Part SK kit verified file-by-file against its "
                         f"published MANIFEST-sha256 {SK_MANIFEST_SHA[:8]}... "
                         f"({SK_KIT_FILES} files)",
                 "kit_manifest_sha256": SK_MANIFEST_SHA,
                 "kit_files_verified": SK_KIT_FILES,
                 "gate_rows_json_sha256": SK_GATEROWS_SHA,
                 "gate_rows_all_pass": SK_GATES_TOTAL,
                 "gate_status_log_sha256": SK_STATUS_SHA,
                 "gate_status_gate_pass_rows": 11,
                 "audit_gate_json_sha256": SK_AUDIT_SHA,
                 "audit_run1_run2_run3_sha256_identical": SK_AUDIT_SHA,
             },
             "canonical_head_cross_gate":
                 "the SK gate-rows.json canonical_head block pins this "
                 "dossier's BASE (6e49dd84, 6,792 rows, WIN 192 / LOSS 6600) "
                 "and records the 5 adopted targets as fresh versus exactly "
                 "that head"},
            {"pool": "ti-third-implementation-audits",
             "kit": TI_EXP,
             "covered_ids": ["k03", "k04", "k05", "k08"],
             "kit_integrity": {
                 "note": "TI kit MANIFEST.sha256 (repo-root-relative paths) "
                         "pinned; the 4 consumed audit summaries and the "
                         "input CSV pins verified",
                 "kit_manifest_sha256": TI_MANIFEST_SHA,
                 "kit_manifest_lines": TI_MANIFEST_LINES,
                 "audit_summary_sha256_pins": TI_AUDIT_SHAS,
                 "third_impl_js_sha256": TI_THIRD_IMPL_SHA,
                 "determinism_triplets": TI_DETERMINISM_PINS,
                 "replica_unanimous_rows": TI_UNANIMOUS_PINS,
             },
             "verdict_agreement_note":
                 "third-impl WIN(1) verdict-level agreement for k03/k04/k05/"
                 "k08; expansions legitimately differ from replica node "
                 "counts (different implementations); the TI audits' replica "
                 "raws are byte-identical to the probe kit's"},
            {"pool": "ea73c3e3-third-impl-k02",
             "kit": THIRDIM_EXP,
             "covered_ids": ["k02"],
             "kit_integrity": {
                 "readme_sha256": THIRDIM_README_SHA,
                 "third_impl_js_sha256": THIRDIM_THIRD_IMPL_SHA,
                 "witness_sha256_pins": THIRDIM_WITNESS_SHAS,
                 "witness_runs": 4,
             },
             "verdict_agreement_note":
                 "k02 WIN(1) reproduced by the fixed third implementation "
                 "on 4 witness runs (a/b/g/v) with 9,106,337 expansions "
                 "each; expansions legitimately differ from the replica's "
                 "7,717,432 nodes; verdict-level agreement (the same rule "
                 "the TI audits apply)"},
        ],
        "resolved_ids": list(ADOPTED_IDS),
        "win_ids": list(ADOPTED_IDS),
        "loss_ids": [],
        "win_ties": [],
        "win_ties_note": "no consumed-WIN regression ties this time: all 5 "
                         "adopted keys are fresh to BASE (unlike emloss21's "
                         "f017/ai007/ai040 ties)",
        "row_counts": {
            "adopted_win_rows": 5,
            "win_ties_consumed_elsewhere": 0,
            "standing_unconsumed_loss_rows": 3,
            "prior_canonical_rows_base": BASE_CACHE_ROWS_EXPECTED,
        },
        "adopted_table": adopted_table,
        "adopted_table_digest_sha256": digest,
        "adopted_nodes_total": ADOPTED_NODES_TOTAL,
        "sha256": {"win_increment": incr_sha},
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_sha256": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "base_cache_win_loss": [BASE_CACHE_WIN_EXPECTED,
                                BASE_CACHE_LOSS_EXPECTED],
        "base_cache_absent_hits_for_emitted": 0,
        "quarantine_hits": 0,
        "interpretation_guard":
            "PREDECL DOSSIER canonical WIN-only adoption increment: if a "
            "future Part declares the sixthwin5 adoption, the 5 fresh "
            "exact-WIN rows (each two-pass fresh-cold node-exact at the "
            "single published condition 15M plus a voluntary third cold "
            "verify run, solved within budget, C++-gated by Part SK and "
            "third-implementation-corroborated) would be consumed into the "
            "canonical chain via the fail-closed union merger; WIN-only "
            "adoption asserts no root verdict and frees no class; owner "
            "classes of the adopted keys may be excluded_now by the "
            "win-hit mechanism, derived machine-only by the reaudit "
            "refresh; nodes are bookkeeping, never verdicts; the standard "
            "11x11 empty board and every central-reply root stay UNKNOWN",
        "provenance": {
            "probe_kit_direct_pins": True,
            "probe_fetch_anchor_note":
                "the probe kit bytes were re-anchored to the published repo "
                "tree at dossier construction; the pins above are the anchor "
                "of record",
            "sk_kit_files_verified": SK_KIT_FILES,
            "ti_kit_pins_verified": 4 + len(TI_AUDIT_FILE),
            "raws_published": True,
        },
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "increment_sha256": incr_sha,
        "rows": len(rowlines),
        "adopted_nodes_total": ADOPTED_NODES_TOTAL,
        "digest": digest,
        "manifest_sha256": hashlib.sha256(
            (OUT / "increments-manifest.json").read_bytes()).hexdigest(),
    }))


if __name__ == "__main__":
    main()
