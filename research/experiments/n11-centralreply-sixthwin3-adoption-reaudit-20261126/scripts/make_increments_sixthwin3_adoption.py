#!/usr/bin/env python3
"""Build the Part SQ sixthwin3 (2 unconsumed parked4rest2 L50M ladder WIN rows)
canonical WIN-adoption increment, fail-closed.

Part SQ kit n11-centralreply-sixthwin3-adoption-reaudit-20261126
(2026-11-26).  This IS the adoption Part declared emission: the canonical
head of record advances from merged-exact-s5-chain-plus-sixthwin2 (sha256
cc3694bb..., 6,799 rows WIN 199 / LOSS 6,600; the Part SP adoption head of
record) to merged-exact-s5-chain-plus-sixthwin3 (sha256 02db5ab3..., 6,801
rows WIN 201 / LOSS 6,600) by consuming exactly the 2 unconsumed
parked4rest2 L50M ladder exact-WIN rows of the sixth-cost class
10376293541461626880:65536: k20 10376293541461626880:33619968 and k33
12682136550675320832:65536 (positions 20/33 of the published probe
selection exclusive_probe_order, budget 50,000,000 over the pinned
15,000,000 park-at-UNKNOWN baselines).  The verdict scope of the Part is
exactly those 2 WIN rows: NO root verdict, NO 11x11 outcome, NO class
freed (owner classes of the adopted keys are excluded_now by the win-hit
mechanism; the SQ census measurement against the current cc3694bb head
measures exactly 2 unknown -> excluded_now flips: 3054 owner of k20 and
2402 owner of k33, with the serving class 3077 already excluded_now and
its cost-unknown count 93 -> 91).

Structural clone of the published Part SP maker
`make_increments_sixthwin2_adoption.py` (sha256 6e95f467...): the
computation region (all source-kit byte gates, multi-pass payload gates,
gate-kit MANIFEST verification, third-impl gates, freshness/quarantine/
canonical-safety gates, adopted-table digest) is identical logic; the
disclosed diff regions are the docstring, the source pools (parked4rest2
L50M ladder replaces the parked4 ladder; the SN C++ gate kit replaces the
SM kit; the k20/k33 third-impl addendum replaces the SL batch summary),
the emitted increment header block, the output file names and the
manifest fields.

Each adopted row is gated at FOUR independent implementations, all
re-verified here byte-for-byte or field-for-field:

1. the parked4rest2 ladder kit's jsreplay replica
   (n11-sixthcost-class10376293541461626880-parked4rest2-s5-l50m-ladder-
   20261126, MANIFEST-verified file-by-file): 15,000,000 park-at-UNKNOWN
   baseline PLUS the 50M primary battery (cold run1/run2 two-pass
   node-exact), the 32,000,000 budget-margin re-proof and the voluntary
   third cold 50M verify run, identical (result, nodes) = (1, 16,196,331)
   / (1, 15,842,649) across all runs, plus 4 validation-anchor replays;
2. the published Part SN pinned C++ second-implementation scrutiny gate
   kit n11-sixthcost-parked4rest2-l50m-cppgate-20261126 (MANIFEST-verified
   file-by-file, 28/28): GATE-PASS for every row with 2-pass determinism
   and published-raw node-exact (the pre-registered adoption requirement
   the parked4rest2 halt-audit delegates, sha-pinned C++ solver
   9193f5b6...);
3. the k20/k33 third-implementation verdict re-verification addendum
   (n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122,
   auditor audit_k20k33.py re-run LIVE here, 49/49 gates): verdict-level
   WIN agreement per key, 3 identical cold third-impl runs each
   (expansions 19,455,330 / 18,829,006 with tt-hits 10,071,309 /
   10,066,094 and pinned tt-overwrites 15,261,026 / 14,634,702;
   expansions legitimately differ from replica node counts - different
   implementations), replica 4-run unanimity and park-baseline replica
   rows pinned, fail-closed negative battery (legal+1 / stones=6);
4. the probe kit's published selection JSON (d5e9b059...): k20/k33 are
   exactly the exclusive_probe_order entries at positions 20 and 33 of
   the same sixth-cost class selection of record.

The 2 adopted (lo,hi) pairs are proven absent from BASE (fresh-increment
gate), absent from the active quarantine registry and canonical-safe per
s5_evidence_policy; the adopted-table digest and the emitted increment
sha are self-pinned; this Part additionally re-verifies the published
merged head of record byte-for-byte (02db5ab3..., 6,801 rows) and its
three byte-identical merge audit records.  The standing unconsumed rows
are recorded but NOT adopted and NOT emitted: the still-parked key k38
of the same probe selection (15,000,000 park-at-UNKNOWN, NO L50M
follow-up claimed - the coverage asymmetry the third-impl completion
pre-registered) and the 30 fifth-resumption verified LOSS rows of the
Part SL batch (no delegated C++ gate).  This Part adopts no LOSS row.

WIN-only adoption asserts no root verdict and frees no class; owner
classes of the adopted keys are excluded_now by the win-hit mechanism,
and all scheduling effects are those derived by the reaudit refresh
(Board fail-closed child verification) and the census delta measurer.
The standard 11x11 empty board and every central-reply root stay
UNKNOWN; nodes are bookkeeping, never verdicts.
"""
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
MERGER = EXP / "scripts/s5_union_merge.py"

SP_EXP = "n11-centralreply-sixthwin2-adoption-reaudit-20261126"
P4R_EXP = ("n11-sixthcost-class10376293541461626880-"
           "parked4rest2-s5-l50m-ladder-20261126")
SN_EXP = "n11-sixthcost-parked4rest2-l50m-cppgate-20261126"
TI_EXP = ("n11-sixthcost-k01-k03-thirdimpl-verdict-"
          "reverification-20261122")
PROBE_EXP = "n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121"

BASE_CACHE = ROOT / "research/experiments" / SP_EXP / (
    "output/merged-exact-s5-chain-plus-sixthwin2-20261126.cache")
P4R_DIR = ROOT / "research/experiments" / P4R_EXP
SN_DIR = ROOT / "research/experiments" / SN_EXP
TI_DIR = ROOT / "research/experiments" / TI_EXP
PROBE_DIR = ROOT / "research/experiments" / PROBE_EXP
GRAPH = (ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"
         "/output/dependency-graph.json.gz")
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
POLICY = (ROOT / "research/experiments/n11-frontier-selection-20261005"
          "/scripts/s5_evidence_policy.py")

MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA_EXPECTED = "cc3694bbe871ccf27bdf4dbcf5e93586da440164fd75c02c15dc2a0ae46d11b8"
BASE_CACHE_ROWS_EXPECTED = 6799
BASE_CACHE_WIN_EXPECTED = 199
BASE_CACHE_LOSS_EXPECTED = 6600
QUARANTINE_SHA_EXPECTED = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
POLICY_SHA_EXPECTED = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
GRAPH_SHA_EXPECTED = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"

# parked4rest2 ladder kit (MANIFEST-verified file-by-file, 26 files)
P4R_MANIFEST_SHA = "fa4b2615c1edce655e94a4be7cdc765e2d68015b68f323a0df7f8c4169b76fed"
P4R_KIT_FILES = 26
P4R_README_SHA = "7ea14f684464ddea292cad0e8567f1334fa33ee4530d443bf988962fe60db26c"
P4R_JSREPLAY_SHA = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
P4R_HALTAUDIT_SHA = "544fc34fa28565118b5cc840ca0ce943ad4b9a44d904a23371ba325137b357c8"
P4R_STATUS_SHA = "8ef612a545950f7558d48158f65c591e28be13444549b4c41131064ab96556ec"
PARK_BUDGET = 15000000
L50M_BUDGET = 50000000
MARGIN_BUDGET = 32000000

ADOPTED_IDS = ["k20", "k33"]
# (lo, hi, legal, s5_index, order_position_1based) - machine-derived from
# the published selection JSON exclusive_probe_order (0-based index 19/32
# = positions 20/33), cross-gated below against the halt-audit, the raw
# replay rows and the frozen dependency graph.
ADOPTED_KEY_PINS = {
    "k20": (10376293541461626880, 33619968, 95, 111843, 20),
    "k33": (12682136550675320832, 65536, 91, 97791, 33),
}
# (result, nodes) of the resolving 50M condition per adopted key -
# machine-derived from the published raws, cross-gated below.
ADOPTED_LABEL_PINS = {
    "k20": (1, 16196331),
    "k33": (1, 15842649),
}
ADOPTED_NODES_TOTAL = 32038980

# standing unconsumed rows outside this Part (recorded, NOT adopted,
# NOT emitted): the still-parked key k38 of the same probe selection
# (15,000,000 park-at-UNKNOWN, NO L50M follow-up claimed - the coverage
# asymmetry the k20/k33 third-impl completion pre-registered) and the 30
# verified LOSS rows of the Part SL fifth-resumption batch (no delegated
# C++ gate).
STANDING_PARKED_KEYS = ["k38"]
SL_STANDING_LOSS_ROWS = 30

P4R_INPUT_SHAS = {
    "batch-k20.input.csv": "0984400f8aa99735e11e2638f5bc9a9273ddd296e845f7b7118f3ada81adddad",
    "batch-k33.input.csv": "ca081b0f2f85e62b39cbbd1178a7be839c87e3446b2357657bbfe8681f82e2f4",
    "val-at2m-first.input.csv": "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
    "val-at2m-second.input.csv": "56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62",
    "val-first-15m.input.csv": "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
    "val-second-15m.input.csv": "56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62",
}

P4R_RAW_SHAS = {
    "base15m-10376293541461626880-33619968.out.csv": "64a069a2a66f677ffd01c4eb03eb6b43aa07ac041319c3fb5ecce5b853c21774",
    "l50m-run1-10376293541461626880-33619968.out.csv": "f852cd55f7f80bdf57ccbe753e78a0b09deb5f7c552af51caed5f4d583aa2c73",
    "l50m-run2-10376293541461626880-33619968.out.csv": "86db668a0288aeb3695f0fb0c3285f128d906ca8dbbf240d6d17b566303601e3",
    "l50m-run3-verify-10376293541461626880-33619968.out.csv": "bf2b12fffb194540205b4eb2c80e98b907059701a36969035824f3b0a339efff",
    "l50m-margin-10376293541461626880-33619968.out.csv": "e5525aab03eb0e272dd44dbe04a0c0c98bddcd2afc3c14c0e474e7055fbafa55",
    "base15m-12682136550675320832-65536.out.csv": "4fb1067184f15036cea90c496c6ebb160ffacd18395adff327c104da71356af8",
    "l50m-run1-12682136550675320832-65536.out.csv": "664ebc3a88ed14cb5a8f418df213368ab8501533c13a60f50261d93d841fc54f",
    "l50m-run2-12682136550675320832-65536.out.csv": "c08cdd7854c9a1c177428e86d08039edfeafe79e340001dc7f386ca0c706a3d2",
    "l50m-run3-verify-12682136550675320832-65536.out.csv": "598538dce0cadc2be4752a6276fe3a8de0f5d3d873d4e7d214063924ebd7b530",
    "l50m-margin-12682136550675320832-65536.out.csv": "39154465a07ee7c97bebab517b284c77866d42374ba6ca5a446a5b502676526e",
    "val-at2m-first.out.csv": "918659ce721241b5956f44c287a0ea4c39b25fa176d03806adba90f540671195",
    "val-at2m-second.out.csv": "b61bf0f8f4700054a28134b803c11077a6c338cf3565a275b70bfbf4ad75b55f",
    "val-first-15m.out.csv": "bf6114f4b5cb8d54fe55dd36250165e5a636c1559ee1d2e20867d668b4cae0db",
    "val-second-15m.out.csv": "5ba4f3f0122855f014397cb50679a884bfac2426fd6467cc9312f3c058a2310f",
}

# validation-anchor replay expectations (honesty ladder: 2M park-UNKNOWN
# then 15M honest LOSS, exact replays of pinned anchor keys)
P4R_VAL_PINS = {
    "val-at2m-first": (98, 2000000, 0, 2000000, 1152921504606851072, 536870946),
    "val-at2m-second": (99, 2000000, 0, 2000000, 1188950301626860544, 536870912),
    "val-first-15m": (98, 15000000, 2, 3651923, 1152921504606851072, 536870946),
    "val-second-15m": (99, 15000000, 2, 5040200, 1188950301626860544, 536870912),
}

# Part SN pinned C++ second-implementation scrutiny gate kit
SN_MANIFEST_SHA = "9853b8616949cbfb9b64b23ce7b97e053303a0d9183ddb0873a36d2fd35a853d"
SN_KIT_FILES = 28
SN_README_SHA = "61cacfef2a395fbea56c4fdf6a96721f1e1db4d5e207588b7c2413d6e48170bc"
SN_GATEROWS_SHA = "b72105bca125354456161469f4bf5bb218b6d155e4ac91045291bab813affec8"
SN_STATUS_SHA = "70b0ee89d6c6c4a1f0a611702227d34be94aeb4e98ee07c296b993240bee7e83"
SN_AUDIT_SHA = "3fbb449df2fd60b4f0075528799c7da369a105eaef601b565eda56a4c86b616e"
SN_GATES_TOTAL = 67
SN_CPP_SHA = "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e"
SN_CPP_COMMIT = "154f3b7a67b97e13acbaee8b04dc74ddca728d19"
SN_ANCHOR_PINS = {
    "anchor-at2m": (98, 2000000, 0, 2000000),
    "anchor-aj001": (84, 30000000, 2, 5156075),
    "anchor-af039": (89, 30000000, 2, 19234232),
}

# k20/k33 third-implementation verdict re-verification addendum (published
# inside the k01-k03 third-impl kit; auditor re-run LIVE below)
TI_AUDITOR_SHA = "32893172386f002b551b6380b71d44ba0bc18ef8f2ab6bbcaf78228e4de2c172"
TI_THIRD_IMPL_SHA = "08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998"
TI_VERIFY_TBL_SHA = "c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251"
TI_TAMPER_LOG_SHA = "3e12204989a6c53e70233829a115d2ee99d7176499266df9b4f85b8f3703183c"
TI_ROW_PINS = {
    "k20": {"key": "10376293541461626880:33619968", "legal": 95,
            "expansions": 19455330, "tt_hits": 10071309,
            "ttoverwrites": 15261026},
    "k33": {"key": "12682136550675320832:65536", "legal": 91,
            "expansions": 18829006, "tt_hits": 10066094,
            "ttoverwrites": 14634702},
}
TI_COLD_SHAS = {
    "k20-cold-a.txt": "2153540d32f80d122dba5ef812b3e2809298103a399c4d121f2996a8bc831907",
    "k20-cold-b.txt": "38daf3dc04160d350ea2de6640d0520b0a301a76da04c121d28e0aa07018900f",
    "k20-cold-v-legal.txt": "5d2cb0c47ccc4da97743d6abefae2812971e3ab64709403bd6d4fa2fa17a5e23",
    "k33-cold-a.txt": "6cf45221fe382896dbceedf03d3c20d23711ea41b8802767faeff78d69a11cd4",
    "k33-cold-b.txt": "5f4db70e54eab2e177244065eeacd3868122377b8cedadeafb1318093a797e4e",
    "k33-cold-v-legal.txt": "4243b74245fbd3118672439ed7c7605818b6652d1f6f538521871a04c91be2b1",
    "neg-gate-k20-ng1.txt": "3683cc1b8037a082596d3efad7dee28df53de49cb9dd121bda1d4153b49909a4",
    "neg-gate-k20-ng2.txt": "de3012e5bc2f8ab9553288b288871ae1e634f9d12d51cdc02454b2c5b1c03c51",
    "neg-gate-k33-ng1.txt": "83c200c5f87d6340b149f914aa3652e77ae7259900a84b596da91faf8f50d305",
    "neg-gate-k33-ng2.txt": "4ea2e13acae6aedb8d6a096656fb73097fd3f4bffeacf49a7f050fa26af7da37",
    "calib-verify-tbl.txt": "88c0b78b2251ea799dbe3a91df0fb56f532ec95e991290ff179ebb918466c863",
    "calib-anchor-w2-a.txt": "3812a557a01367165ed52a2a5ca3f9bdda2eb3c87fec21218bffd17bbfb690db",
    "calib-anchor-w2-b.txt": "800d2698beea89632c993343e46297248430b0f0f218f1565a333e418ef2579f",
}
TI_NEG_MSGS = {
    "neg-gate-k20-ng1.txt": "legal count mismatch: derived=95 declared=96",
    "neg-gate-k20-ng2.txt": "stone count mismatch: bits=5 declared=6",
    "neg-gate-k33-ng1.txt": "legal count mismatch: derived=91 declared=92",
    "neg-gate-k33-ng2.txt": "stone count mismatch: bits=5 declared=6",
}

# probe kit selection JSON (the selection of record for this class)
PROBE_SELECTION_SHA = "d5e9b059611849f7b7e69c7370a0e66cd7535c43b3a043ce9f5bfc0e5ff72e87"

# published outputs of this Part (self-pinned; the merged head of record
# is published BY this Part, so it is gated here byte-for-byte)
MERGED_NAME = "merged-exact-s5-chain-plus-sixthwin3-20261126.cache"
MERGED_SHA_EXPECTED = "02db5ab35b8ad71dfd0699217756291c6bc896c78e9fd7c609b5e25177f6b25c"
MERGED_BYTES_EXPECTED = 284230
MERGE_AUDIT_SHA_EXPECTED = "622ac17f72c9ad2a7b9e9714b3274c6bcba1df34910365268db16f3c76e0c368"

ADOPTED_TABLE_DIGEST = "d89ccfbb53078359fb650b2ac7fec5d94fe2b7bfb0038b54ce476d7b01f6dd28"
ADOPTED_INCREMENT_SHA = "47f7dfb02489a960184b5c83bd3ed36e33936bd40067c7cc97299ab1f740ecc6"
SERVING_CLASS = 3077
CLASS_MASK = (10376293541461626880, 65536)

INCREMENT_NAME = "increment-sixthwin3-adoption-20261126.cache"
SIXTHWIN3_SCHEMA = "sixthwin3-adoption-increments-manifest-v1"

HDR_LINES = [
 "# n11 central-reply closure sixthwin3 canonical-adoption increment",
 "#   (Part SQ, n11-centralreply-sixthwin3-adoption-reaudit-20261126,",
 "#   2026-11-26) - WIN-only, fresh 2-row increment.  Part SQ declares the",
 "#   sixthwin3 canonical WIN adoption: the canonical head of record advances",
 "#   from merged-exact-s5-chain-plus-sixthwin2 (sha256 cc3694bb..., 6,799",
 "#   rows WIN 199 / LOSS 6,600; the Part SP adoption head of record) to",
 "#   merged-exact-s5-chain-plus-sixthwin3 (6,801 rows WIN 201 / LOSS 6,600)",
 "#   by consuming exactly the 2 unconsumed parked4rest2 L50M ladder",
 "#   exact-WIN rows of the sixth-cost class 10376293541461626880:65536:",
 "#   k20 10376293541461626880:33619968 and k33 12682136550675320832:65536",
 "#   (budget 50,000,000 over the pinned 15,000,000 park-at-UNKNOWN",
 "#   baselines; exclusive_probe_order positions 20/33).",
 "# The sources of record (all re-verified live by the Part maker against",
 "#   published bytes): the parked4rest2 ladder's four-run primary battery",
 "#   (50M cold two-pass node-exact, 32M budget-margin re-proof, voluntary",
 "#   third cold 50M verify; k20 nodes 16,196,331 / k33 nodes 15,842,649),",
 "#   the Part SN pinned C++ second-implementation scrutiny gate",
 "#   (GATE-PASS, two fresh-cold passes per row, node-exact 95,50000000,1,",
 "#   16196331 / 91,50000000,1,15842649), and the k20/k33 third-",
 "#   implementation verdict re-verification addendum (verdict-level WIN",
 "#   agreement, 3 identical cold runs each, k20 expansions 19,455,330 /",
 "#   k33 expansions 18,829,006; expansions legitimately differ from",
 "#   replica node counts - different implementations).  Adopted node",
 "#   total 32,038,980.",
 "# Coverage-asymmetry disclosure (weighed per the third-impl completion",
 "#   pre-registration): the 30 fifth-resumption verified LOSS rows of the",
 "#   Part SL batch remain WITHOUT a delegated C++ second-implementation",
 "#   gate (no LOSS row is adopted by this Part); the still-parked key k38",
 "#   of the same probe selection remains at 15,000,000 with NO L50M",
 "#   follow-up claimed; both remain standing unconsumed, outside this",
 "#   Part.",
 "# Every adopted key is fresh to BASE cc3694bb... (win_ties = []),",
 "#   quarantine-free, canonical-safe per s5_evidence_policy.",
 "# This Part publishes the merged cache of record itself (no pre-",
 "#   declaration dossier exists for sixthwin3): merger = the pinned",
 "#   byte-clone of s5_union_merge.py 90711961..., output pinned in this",
 "#   kit's MANIFEST; win_ties = [] (both keys are fresh to BASE).",
 "# WIN-only adoption asserts NO root verdict and frees no class; the",
 "#   measured census delta is exactly 2 unknown -> excluded_now win-hit",
 "#   flips: class 3054 (1297037794341814272:0, owner of k20) and class",
 "#   2402 (1873498544497754112:0, owner of k33); serving class 3077",
 "#   cost-unknown 93 -> 91 with status already excluded_now (Part EW);",
 "#   nodes are bookkeeping, never verdicts.  The standard 11x11 empty",
 "#   board and every central-reply root stay UNKNOWN.",
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


def parse_third(path: Path):
    line = path.read_text().strip().splitlines()[-1]
    parts = line.split(",")
    if len(parts) >= 6 and parts[5] == "GATE_FAIL":
        return {"gate_fail": True, "text": path.read_text()}
    if len(parts) != 15 or parts[0] != "third":
        sys_exit(f"malformed third-impl raw row in {path}")
    kv = dict(x.split("=", 1) for x in parts[12:15])
    return {
        "gate_fail": False,
        "row": parts[1], "stones": int(parts[2]),
        "legal_in": int(parts[3]), "legal_derived": int(parts[4]),
        "result": int(parts[5]), "expansions": int(parts[6]),
        "tt_hits": int(parts[7]), "lo": parts[9], "hi": parts[10],
        "reason": parts[11], "quads": kv["quads"],
        "ttoverwrites": int(kv["ttOverwrites"]),
        "memopower": int(kv["memoPower"]),
    }


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
        sys_exit("base cache (Part SP head of record) sha drift")
    if sha(MERGER) != MERGER_SHA_EXPECTED:
        sys_exit("fail-closed union merger (scripts/s5_union_merge.py) sha "
                 "drift: this Part must use the pinned merger byte-for-byte")
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

    # --- probe kit selection JSON (order positions of the adopted keys) -
    if not PROBE_DIR.is_dir():
        sys_exit(f"probe kit dir missing {PROBE_DIR}")
    if sha(PROBE_DIR / "output/sixth-cost-exclusive-keys.json") != \
            PROBE_SELECTION_SHA:
        sys_exit("probe kit selection JSON sha drift")
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
        lo, hi, legal, _s5, pos = ADOPTED_KEY_PINS[kid]
        entry = sel["exclusive_probe_order"][pos - 1]
        if entry["key"] != f"{lo}:{hi}" or entry["legal"] != legal:
            sys_exit(f"probe selection order-position disagreement: {kid}")

    # --- parked4rest2 ladder kit: MANIFEST-verified file-by-file ---------
    if not P4R_DIR.is_dir():
        sys_exit(f"parked4rest2 ladder kit dir missing {P4R_DIR}")
    if sha(P4R_DIR / "MANIFEST-sha256.txt") != P4R_MANIFEST_SHA:
        sys_exit("parked4rest2 kit MANIFEST sha drift")
    p4r_manifest_shas = load_manifest_2field(P4R_DIR / "MANIFEST-sha256.txt",
                                             "parked4rest2")
    if len(p4r_manifest_shas) != P4R_KIT_FILES:
        sys_exit(f"parked4rest2 kit files verified {len(p4r_manifest_shas)} "
                 f"!= {P4R_KIT_FILES}")
    for rel, want in p4r_manifest_shas.items():
        p = P4R_DIR / rel
        if not p.is_file():
            sys_exit(f"parked4rest2 kit file missing: {rel}")
        if sha(p) != want:
            sys_exit(f"parked4rest2 kit file sha drift: {rel}")
    if p4r_manifest_shas.get("README.md") != P4R_README_SHA:
        sys_exit("parked4rest2 kit README pin drift")
    if p4r_manifest_shas.get("scripts/jsreplay.js") != P4R_JSREPLAY_SHA:
        sys_exit("parked4rest2 kit jsreplay pin drift")
    if p4r_manifest_shas.get("output/halt-audit.json") != P4R_HALTAUDIT_SHA:
        sys_exit("parked4rest2 kit halt-audit pin drift")
    if p4r_manifest_shas.get("status.log") != P4R_STATUS_SHA:
        sys_exit("parked4rest2 kit status.log pin drift")
    for name, want in P4R_INPUT_SHAS.items():
        if p4r_manifest_shas.get(f"input/{name}") != want:
            sys_exit(f"parked4rest2 input CSV manifest pin drift: {name}")
    for name, want in P4R_RAW_SHAS.items():
        if p4r_manifest_shas.get(f"output/raw/{name}") != want:
            sys_exit(f"parked4rest2 raw manifest pin drift: {name}")

    h = json.loads((P4R_DIR / "output/halt-audit.json").read_text())
    if h["schema"] != "n11-sixthcost-parked4rest2-l50m-ladder-halt-audit-v1":
        sys_exit("parked4rest2 halt-audit schema drift")
    if h["all_gates_pass_before_halt"] is not True \
            or h["gates_passed_count"] != 75:
        sys_exit("parked4rest2 halt-audit gate accounting drift")
    adopted_key_strs = [f"{ADOPTED_KEY_PINS[k][0]}:{ADOPTED_KEY_PINS[k][1]}"
                        for k in ADOPTED_IDS]
    if h["halted_on_win_keys"] != adopted_key_strs:
        sys_exit("parked4rest2 halt-audit halted_on_win_keys drift")
    pins = h["pins"]
    if pins["jsreplay_sha256"] != P4R_JSREPLAY_SHA \
            or pins["parent_selection_json_sha256"] != PROBE_SELECTION_SHA \
            or pins["quarantine_sha256"] != QUARANTINE_SHA_EXPECTED \
            or pins["policy_sha256"] != POLICY_SHA_EXPECTED:
        sys_exit("parked4rest2 halt-audit pins block drift")
    # the halt-audit pins the lane-time canonical head 16a12390 (pre-SP):
    # disclosed, NOT asserted equal to this Part's BASE (the ladder ran
    # before Part SP merged; freshness vs the current head is gated below)
    if pins["base_chain_cache_sha256"] != \
            "16a12390c0c3f046f0ae537b2a9940e15661263fc5034ce1b155c138bb9043cd":
        sys_exit("parked4rest2 halt-audit lane-time base pin drift")
    probe = h["probe"]
    if probe["claimed_keys"] != adopted_key_strs \
            or probe["started_keys"] != adopted_key_strs:
        sys_exit("parked4rest2 halt-audit claimed/started keys drift")
    if probe["never_started_keys_stay_parked_15m"] != []:
        sys_exit("parked4rest2 halt-audit never-started drift (this lane "
                 "started both adopted keys)")
    if probe["resolved_loss_raw"] != []:
        sys_exit("parked4rest2 halt-audit resolved_loss_raw drift")
    if sorted(probe["win_raws_needing_scrutiny"]) != sorted(adopted_key_strs):
        sys_exit("parked4rest2 halt-audit win_raws_needing_scrutiny drift")
    for kid in ADOPTED_IDS:
        pk = probe["per_key"][kid]
        lo, hi, legal, _s5, pos = ADOPTED_KEY_PINS[kid]
        res, nodes = ADOPTED_LABEL_PINS[kid]
        if pk["key"] != f"{lo}:{hi}" or pk["legal"] != legal \
                or pk["position"] != pos or pk["verdict"] != "WIN":
            sys_exit(f"parked4rest2 halt-audit per_key header drift: {kid}")
        stages = pk["stages"]
        if stages["base15m"] != {"result": 0, "nodes": PARK_BUDGET}:
            sys_exit(f"parked4rest2 halt-audit base15m park stage drift: {kid}")
        if stages["at50m"] != {"result": res, "nodes": nodes} \
                or stages["at50m_run2"] != {"result": res, "nodes": nodes}:
            sys_exit(f"parked4rest2 halt-audit 50M determinism pair drift: {kid}")
        if stages["margin_reproof"] != {"budget": MARGIN_BUDGET,
                                        "result": res, "nodes": nodes}:
            sys_exit(f"parked4rest2 halt-audit margin re-proof drift: {kid}")
        if stages["voluntary_run3_verify"] != {"budget": L50M_BUDGET,
                                               "result": res, "nodes": nodes}:
            sys_exit(f"parked4rest2 halt-audit voluntary verify drift: {kid}")
    for tgt in probe["delegated_cpp_gate_targets"]:
        lo, hi, legal, _s5, _pos = ADOPTED_KEY_PINS[
            "k20" if tgt["key"].startswith("10376293541461626880") else "k33"]
        res, nodes = ADOPTED_LABEL_PINS[
            "k20" if tgt["key"].startswith("10376293541461626880") else "k33"]
        if tgt["key"] != f"{lo}:{hi}" or tgt["budget"] != L50M_BUDGET \
                or tgt["expected_result"] != res \
                or tgt["expected_nodes"] != nodes \
                or tgt["target"] != f"target,0,5,{lo},{hi},{legal},0,0,0,0,0":
            sys_exit(f"parked4rest2 delegated C++ gate target drift: {tgt['key']}")
    if "NO verdict is consumed" not in h["status_guard"] \
            or "remain UNKNOWN" not in h["status_guard"]:
        sys_exit("parked4rest2 halt-audit status guard drift")

    # parked4rest2 status.log: SSOT stage lines for the adopted keys
    slines = (P4R_DIR / "status.log").read_text().splitlines()
    sjoined = "\n".join(slines)
    want_lines = [
        "gate2 base15m reproduced k20 0/15000000 wall 185 s; "
        "k33 0/15000000 wall 188 s",
        "l50m-run1 results k20 WIN(1) nodes 16196331 wall 200s; "
        "k33 WIN(1) nodes 15842649 wall 194s",
        "l50m-run2 determinism pair CONFIRMED k20 (1,16196331) "
        "k33 (1,15842649) identical to run1",
        "l50m-margin re-proof PASS k20 (1,16196331) k33 (1,15842649) at 32M",
        "run3-verify results k20 (1,16196331) k33 (1,15842649) identical "
        "to the declared pair and margin",
        "ALL 75 PRE-WIN GATES PASS -> HALTED ON WIN k20/k33",
    ]
    for w in want_lines:
        if w not in sjoined:
            sys_exit(f"parked4rest2 status.log missing stage line: {w}")

    # parked4rest2 input CSVs: direct pins (row-spec shape)
    for name, want in P4R_INPUT_SHAS.items():
        p = P4R_DIR / f"input/{name}"
        fields = p.read_text().strip().split(",")
        if len(fields) != 11 or fields[0] != "target" \
                or fields[1] != "0" or fields[2] != "5":
            sys_exit(f"parked4rest2 kit input CSV row-spec drift: {name}")
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos = ADOPTED_KEY_PINS[kid]
        fields = (P4R_DIR / f"input/batch-{kid}.input.csv").read_text() \
            .strip().split(",")
        if fields[3] != str(lo) or fields[4] != str(hi) \
                or fields[5] != str(legal):
            sys_exit(f"parked4rest2 batch input key/legal drift: {kid}")
    # the val anchors replay the same target twice (2M then 15M): the two
    # val input CSVs per side must be byte-identical pairs
    if P4R_INPUT_SHAS["val-at2m-first.input.csv"] != \
            P4R_INPUT_SHAS["val-first-15m.input.csv"] \
            or P4R_INPUT_SHAS["val-at2m-second.input.csv"] != \
            P4R_INPUT_SHAS["val-second-15m.input.csv"]:
        sys_exit("parked4rest2 val input pair drift")

    # parked4rest2 raws: 15M park baseline + 50M two-pass + margin re-proof
    # + voluntary third verify, plus 4 validation-anchor replays, all
    # byte-pinned and payload-gated
    probe_rows = {}
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos = ADOPTED_KEY_PINS[kid]
        res, nodes = ADOPTED_LABEL_PINS[kid]
        base = f"{lo}-{hi}"
        raw_files = {
            "base15m": P4R_DIR / f"output/raw/base15m-{base}.out.csv",
            "run1": P4R_DIR / f"output/raw/l50m-run1-{base}.out.csv",
            "run2": P4R_DIR / f"output/raw/l50m-run2-{base}.out.csv",
            "run3": P4R_DIR / f"output/raw/l50m-run3-verify-{base}.out.csv",
            "margin": P4R_DIR / f"output/raw/l50m-margin-{base}.out.csv",
        }
        for tag, p in raw_files.items():
            if not p.is_file():
                sys_exit(f"parked4rest2 raw missing: {p.name}")
            if sha(p) != P4R_RAW_SHAS[p.name]:
                sys_exit(f"parked4rest2 raw sha drift ({tag}): {kid}")
        parsed = {tag: parse_replay(p) for tag, p in raw_files.items()}
        b = parsed["base15m"]
        if (b["stones"], b["is_or"], b["budget"], b["result"], b["nodes"]) \
                != (5, 0, PARK_BUDGET, 0, PARK_BUDGET):
            sys_exit(f"{kid}: 15M park-at-UNKNOWN baseline stage drift")
        if b["legal"] != legal or b["lo"] != str(lo) or b["hi"] != str(hi):
            sys_exit(f"{kid}: base15m key/legal drift")
        for tag, budget in (("run1", L50M_BUDGET), ("run2", L50M_BUDGET),
                            ("run3", L50M_BUDGET), ("margin", MARGIN_BUDGET)):
            r = parsed[tag]
            if (r["stones"], r["is_or"], r["budget"]) != (5, 0, budget):
                sys_exit(f"{kid}: wrong depth/or/budget ({tag})")
            if r["legal"] != legal or r["lo"] != str(lo) or r["hi"] != str(hi):
                sys_exit(f"{kid}: legal/key disagreement raw vs pinned ({tag})")
            if (r["result"], r["nodes"]) != (res, nodes):
                sys_exit(f"{kid}: honest-label drift vs pinned label ({tag})")
        payload_eq(parsed["run1"], parsed["run2"], f"{kid} 50m")
        payload_eq(parsed["run1"], parsed["run3"], f"{kid} 50m-run3-verify")
        probe_rows[kid] = parsed["run1"]
    # validation anchors: honesty replays of pinned anchor keys
    for name, (legal_v, budget_v, res_v, nodes_v, lo_v, hi_v) in \
            P4R_VAL_PINS.items():
        p = P4R_DIR / f"output/raw/{name}.out.csv"
        if sha(p) != P4R_RAW_SHAS[f"{name}.out.csv"]:
            sys_exit(f"parked4rest2 val raw sha drift: {name}")
        r = parse_replay(p)
        if (r["stones"], r["is_or"], r["legal"], r["budget"], r["result"],
                r["nodes"], r["lo"], r["hi"]) != \
                (5, 0, legal_v, budget_v, res_v, nodes_v, str(lo_v), str(hi_v)):
            sys_exit(f"parked4rest2 val anchor replay drift: {name}")
    adopted_nodes = sum(ADOPTED_LABEL_PINS[kid][1] for kid in ADOPTED_IDS)
    if adopted_nodes != ADOPTED_NODES_TOTAL:
        sys_exit(f"adopted node total drift {adopted_nodes} "
                 f"!= {ADOPTED_NODES_TOTAL}")

    # --- Part SN pinned C++ second-implementation scrutiny gate kit ------
    if not SN_DIR.is_dir():
        sys_exit(f"Part SN kit dir missing {SN_DIR}")
    if sha(SN_DIR / "MANIFEST-sha256.txt") != SN_MANIFEST_SHA:
        sys_exit("Part SN kit MANIFEST sha drift")
    sn_manifest_shas = load_manifest_2field(SN_DIR / "MANIFEST-sha256.txt",
                                            "Part SN")
    if len(sn_manifest_shas) != SN_KIT_FILES:
        sys_exit(f"Part SN kit files verified {len(sn_manifest_shas)} "
                 f"!= {SN_KIT_FILES}")
    for rel, want in sn_manifest_shas.items():
        p = SN_DIR / rel
        if not p.is_file():
            sys_exit(f"Part SN kit file missing: {rel}")
        if sha(p) != want:
            sys_exit(f"Part SN kit file sha drift: {rel}")
    if sn_manifest_shas.get("README.md") != SN_README_SHA:
        sys_exit("Part SN kit README pin drift")
    for kid in ADOPTED_IDS:
        a = sn_manifest_shas.get(f"input/{kid}.input.csv")
        if a is None or a != P4R_INPUT_SHAS[f"batch-{kid}.input.csv"]:
            sys_exit(f"{kid}: SN gate input CSV is not byte-equal to the "
                      "parked4rest2 kit's batch input CSV (cross-registration)")
    if sha(SN_DIR / "input/gate-rows.json") != SN_GATEROWS_SHA:
        sys_exit("Part SN gate-rows.json sha drift")
    gr = json.loads((SN_DIR / "input/gate-rows.json").read_text())
    if gr["schema"] != "n11-sixthcost-parked4rest2-cppgate-rows-v1":
        sys_exit("Part SN gate-rows schema drift")
    if gr["part"] != "SN":
        sys_exit("Part SN gate-rows part drift")
    gs = gr["gate_source"]
    if gs["path"] != "cpp/solvers/kyouen_dfpn_root.cpp" \
            or gs["sha256"] != SN_CPP_SHA or gs["commit"] != SN_CPP_COMMIT:
        sys_exit("Part SN gate-rows gate-source block drift")
    ch = gr["canonical_head"]
    # the SN gate-rows canonical_head block pins the lane-time head
    # 16a12390 (the SN gate ran before Part SP merged): disclosed; the
    # freshness that matters for THIS Part is vs BASE cc3694bb, gated in
    # the freshness section below (both keys absent from cc3694bb)
    if (ch["label"] != "16a12390"
            or ch["sha256"] != "16a12390c0c3f046f0ae537b2a9940e15661263fc"
                               "5034ce1b155c138bb9043cd"
            or ch["rows"] != 6797
            or ch["census"] != {"WIN": 197, "LOSS": 6600}
            or ch["targets_fresh_vs"] != "16a12390"):
        sys_exit("Part SN gate-rows canonical-head block drift")
    if len(gr["gates"]) != SN_GATES_TOTAL or any(
            v["status"] != "PASS" for v in gr["gates"].values()):
        sys_exit("Part SN gate-rows 67-gate table not all PASS")
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos = ADOPTED_KEY_PINS[kid]
        res, nodes = ADOPTED_LABEL_PINS[kid]
        t = gr["targets"][kid]
        if (t["key_lo"], t["key_hi"], t["budget"], t["expected"]) != \
                (str(lo), str(hi), str(L50M_BUDGET),
                 f"{legal},{L50M_BUDGET},{res},{nodes}"):
            sys_exit(f"Part SN gate-rows target drift: {kid}")
        if t["input_sha256"] != P4R_INPUT_SHAS[f"batch-{kid}.input.csv"]:
            sys_exit(f"Part SN gate-rows input pin drift: {kid}")
        base = f"{lo}-{hi}"
        if t["raw_p1_sha256"] != P4R_RAW_SHAS[f"l50m-run1-{base}.out.csv"] \
                or t["raw_p2_sha256"] != P4R_RAW_SHAS[f"l50m-run2-{base}.out.csv"] \
                or t["run3_verify_sha256"] != \
                P4R_RAW_SHAS[f"l50m-run3-verify-{base}.out.csv"] \
                or t["margin_sha256"] != P4R_RAW_SHAS[f"l50m-margin-{base}.out.csv"]:
            sys_exit(f"Part SN gate-rows raw pin cross-registration drift: {kid}")
        if t["third_impl_verdict_level_corroboration"] is not False:
            sys_exit(f"Part SN gate-rows corroboration flag drift (the SN "
                     f"gate ran before the third-impl addendum existed and "
                     f"records false; the corroboration this Part relies on "
                     f"is gated directly below): {kid}")
        if t["row_spec"] != f"target,0,5,{lo},{hi},{legal},0,0,0,0,0":
            sys_exit(f"Part SN gate-rows row spec drift: {kid}")
    if sha(SN_DIR / "output/gate-status.log") != SN_STATUS_SHA:
        sys_exit("Part SN gate-status.log sha drift")
    gk_map = {}
    for line in (SN_DIR / "output/gate-status.log").read_text().splitlines():
        parts = line.split()
        if len(parts) < 4 or " ".join(parts[2:3]) != "GATE-PASS" \
                or not parts[3].replace(",", "").isdigit():
            sys_exit(f"Part SN gate-status unexpected line: {line}")
        gk_map[parts[1]] = parts[3]
    if len(gk_map) != 5:
        sys_exit("Part SN gate-status must carry exactly 5 GATE-PASS rows")
    for name, (legal_v, budget_v, res_v, nodes_v) in SN_ANCHOR_PINS.items():
        if gk_map.get(name) != f"{legal_v},{budget_v},{res_v},{nodes_v}":
            sys_exit(f"Part SN gate-status anchor row drift: {name}")
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos = ADOPTED_KEY_PINS[kid]
        res, nodes = ADOPTED_LABEL_PINS[kid]
        if gk_map.get(kid) != f"{legal},{L50M_BUDGET},{res},{nodes}":
            sys_exit(f"Part SN gate-status row drift: {kid}")
    for rel in ("output/audit_gate.json", "output/audit_gate.run1.json",
                "output/audit_gate.run2.json", "output/audit_gate.run3.json"):
        if sn_manifest_shas.get(rel) != SN_AUDIT_SHA:
            sys_exit(f"Part SN audit json sha drift: {rel}")
    ag = json.loads((SN_DIR / "output/audit_gate.json").read_text())
    if ag["overall"] != "PASS" or ag["part"] != "SN":
        sys_exit("Part SN audit_gate.json overall/part drift")
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos = ADOPTED_KEY_PINS[kid]
        res, nodes = ADOPTED_LABEL_PINS[kid]
        row = ag["rows"].get(kid)
        if row is None or row["expected"] != f"{legal},{L50M_BUDGET},{res},{nodes}" \
                or row["observed_p1"] != row["expected"] \
                or row["budget"] != str(L50M_BUDGET):
            sys_exit(f"Part SN audit_gate row drift: {kid}")
    for name, (legal_v, budget_v, res_v, nodes_v) in SN_ANCHOR_PINS.items():
        row = ag["rows"].get(name)
        if row is None or row["expected"] != f"{legal_v},{budget_v},{res_v},{nodes_v}" \
                or row["observed_p1"] != row["expected"]:
            sys_exit(f"Part SN audit_gate anchor row drift: {name}")
    # SN raw payload gate (bytes already MANIFEST-verified; payload here)
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos = ADOPTED_KEY_PINS[kid]
        res, nodes = ADOPTED_LABEL_PINS[kid]
        s1 = parse_replay(SN_DIR / f"output/raw/{kid}.p1.out")
        s2 = parse_replay(SN_DIR / f"output/raw/{kid}.p2.out")
        payload_eq(s1, s2, f"SN {kid}")
        if (s1["stones"], s1["is_or"], s1["budget"], s1["result"],
                s1["nodes"]) != (5, 0, L50M_BUDGET, res, nodes):
            sys_exit(f"{kid}: SN C++ gate honest-label drift")
        if s1["legal"] != legal or s1["lo"] != str(lo) or s1["hi"] != str(hi):
            sys_exit(f"{kid}: SN C++ gate legal/key drift")
    for name, (legal_v, budget_v, res_v, nodes_v) in SN_ANCHOR_PINS.items():
        a1 = parse_replay(SN_DIR / f"output/raw/{name}.p1.out")
        a2 = parse_replay(SN_DIR / f"output/raw/{name}.p2.out")
        payload_eq(a1, a2, f"SN {name}")
        if (a1["stones"], a1["is_or"], a1["legal"], a1["budget"], a1["result"],
                a1["nodes"]) != (5, 0, legal_v, budget_v, res_v, nodes_v):
            sys_exit(f"{name}: SN C++ gate anchor-label drift")

    # --- k20/k33 third-implementation verdict re-verification addendum --
    if not TI_DIR.is_dir():
        sys_exit(f"third-impl kit dir missing {TI_DIR}")
    if sha(TI_DIR / "audit_k20k33.py") != TI_AUDITOR_SHA:
        sys_exit("k20/k33 third-impl auditor sha drift")
    if sha(TI_DIR / "third_impl.js") != TI_THIRD_IMPL_SHA:
        sys_exit("third_impl.js sha drift")
    if sha(TI_DIR / "verify_tbl.js") != TI_VERIFY_TBL_SHA:
        sys_exit("verify_tbl.js sha drift")
    if sha(TI_DIR / "out/audit-tamper-controls-k20k33.txt") != TI_TAMPER_LOG_SHA:
        sys_exit("k20/k33 third-impl tamper-controls log sha drift")
    for kid in ADOPTED_IDS:
        a = sha(TI_DIR / f"input/batch-{kid}.input.csv")
        if a != P4R_INPUT_SHAS[f"batch-{kid}.input.csv"]:
            sys_exit(f"{kid}: third-impl row-spec input is not byte-equal to "
                     "the parked4rest2 batch input (cross-registration)")
    # per-row cold third-impl runs (a, b, verify-legal): verdict-level WIN
    # agreement, determinism quadruple, anti-copy expansions
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos = ADOPTED_KEY_PINS[kid]
        res, nodes = ADOPTED_LABEL_PINS[kid]
        pins = TI_ROW_PINS[kid]
        cold = {}
        for tag, fname in (("a", f"{kid}-cold-a.txt"),
                           ("b", f"{kid}-cold-b.txt"),
                           ("v", f"{kid}-cold-v-legal.txt")):
            p = TI_DIR / f"out/{fname}"
            if sha(p) != TI_COLD_SHAS[fname]:
                sys_exit(f"third-impl cold raw sha drift: {fname}")
            cold[tag] = parse_third(p)
        quad = {t: (cold[t]["result"], cold[t]["expansions"],
                    cold[t]["tt_hits"], cold[t]["ttoverwrites"])
                for t in ("a", "b", "v")}
        if not (quad["a"] == quad["b"] == quad["v"]):
            sys_exit(f"{kid}: third-impl determinism quadruple drift")
        if quad["a"] != (1, pins["expansions"], pins["tt_hits"],
                          pins["ttoverwrites"]):
            sys_exit(f"{kid}: third-impl honest-label drift vs pinned "
                     "quadruple")
        for t in ("a", "b", "v"):
            d = cold[t]
            if d["gate_fail"] or d["reason"] != "clean" \
                    or d["stones"] != 5 or d["legal_in"] != legal \
                    or d["legal_derived"] != legal \
                    or d["lo"] != str(lo) or d["hi"] != str(hi) \
                    or d["quads"] != "95670" or d["memopower"] != 22:
                sys_exit(f"{kid}: third-impl cold run field drift ({t})")
            if d["expansions"] == nodes:
                sys_exit(f"{kid}: anti-copy gate (expansions == replica nodes)")
        if (cold["v"]["result"], cold["v"]["expansions"]) != \
                (cold["a"]["result"], cold["a"]["expansions"]):
            sys_exit(f"{kid}: third-impl verify-legal equality drift")
        # replica copies re-published inside the third-impl dir must be
        # byte-equal to the ladder raws (self-contained auditor)
        base = f"{lo}-{hi}"
        for stage, ladder_name in (
                ("base15m", f"base15m-{base}.out.csv"),
                ("l50m-run1", f"l50m-run1-{base}.out.csv"),
                ("l50m-run2", f"l50m-run2-{base}.out.csv"),
                ("l50m-margin", f"l50m-margin-{base}.out.csv"),
                ("l50m-run3-verify", f"l50m-run3-verify-{base}.out.csv")):
            p = TI_DIR / f"out/{kid}-replica-raws/{stage}-{kid}.out.csv"
            if sha(p) != P4R_RAW_SHAS[ladder_name]:
                sys_exit(f"{kid}: third-impl replica copy drift: {stage}")
    # C1 fresh calibration raws
    vt = (TI_DIR / "out/calib-verify-tbl.txt").read_text().strip().splitlines()
    if len(vt) != 2 or vt[0] != "replica quads 95670 mine quads 95670" \
            or vt[1] != "triples checked 195044 mismatches 0":
        sys_exit("third-impl C1 verify-tbl calibration raw drift")
    ca = parse_third(TI_DIR / "out/calib-anchor-w2-a.txt")
    cb = parse_third(TI_DIR / "out/calib-anchor-w2-b.txt")
    for d in (ca, cb):
        if d["gate_fail"] or d["result"] != 1 or d["expansions"] != 7583990 \
                or d["lo"] != "10376293541461626880" or d["hi"] != "131328" \
                or d["reason"] != "clean":
            sys_exit("third-impl C1 anchor-w2 calibration drift")
    if (ca["result"], ca["expansions"], ca["tt_hits"], ca["ttoverwrites"]) != \
            (cb["result"], cb["expansions"], cb["tt_hits"], cb["ttoverwrites"]):
        sys_exit("third-impl C1 anchor-w2 determinism drift")
    # C4 fail-closed negative gates
    for fname, msg in TI_NEG_MSGS.items():
        p = TI_DIR / f"out/{fname}"
        if sha(p) != TI_COLD_SHAS[fname]:
            sys_exit(f"third-impl negative-gate raw sha drift: {fname}")
        d = parse_third(p)
        if not d["gate_fail"] or json.dumps(msg) not in d["text"]:
            sys_exit(f"third-impl negative-gate payload drift: {fname}")
    # LIVE re-run of the published data-driven auditor (49/49 gates,
    # deterministic byte-identical stdout across two executions)
    audit_stdouts = []
    for _ in range(2):
        proc = subprocess.run([sys.executable, "audit_k20k33.py"],
                              cwd=TI_DIR, capture_output=True, text=True)
        if proc.returncode != 0:
            sys_exit("live audit_k20k33.py re-run failed closed "
                     f"rc={proc.returncode}: {proc.stdout[-400:]}")
        if "gates 49 fails 0" not in proc.stdout or "ALL PASS" not in proc.stdout:
            sys_exit("live audit_k20k33.py gate accounting drift")
        audit_stdouts.append(proc.stdout)
    if audit_stdouts[0] != audit_stdouts[1]:
        sys_exit("live audit_k20k33.py non-deterministic stdout")

    # --- freshness: BASE absence, quarantine, canonical safety -----------
    adopted_rows = []
    for kid in ADOPTED_IDS:
        ref = probe_rows[kid]
        if ref["result"] != 1:
            sys_exit(f"{kid}: adopted row must be exact WIN")
        (lo, hi, legal, s5_index, _pos) = ADOPTED_KEY_PINS[kid]
        if (int(ref["lo"]), int(ref["hi"])) != (lo, hi):
            sys_exit(f"{kid}: raw key vs pinned key disagreement")
        if ref["legal"] != legal:
            sys_exit(f"{kid}: raw legal vs pinned legal disagreement")
        if mask_to_index.get((lo, hi)) != s5_index:
            sys_exit(f"{kid}: s5_index round-trip drift vs the frozen graph")
        owners = [ci for ci in range(len(s4_masks)) if s5_index in s4_cost[ci]]
        if SERVING_CLASS not in owners:
            sys_exit(f"{kid}: serving class must own the key at graph time")
        if ref["nodes"] != ADOPTED_LABEL_PINS[kid][1]:
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
    if len({(r[0], r[1]) for r in adopted_rows}) != 2:
        sys_exit("adopted pairs must be exactly 2 distinct keys")

    digest = hashlib.sha256("\n".join(
        f"{lo},{hi},{legal},{result},{nodes}"
        for lo, hi, legal, result, nodes, _s5, _cls, _own in
        sorted(adopted_rows)).encode()).hexdigest()
    if digest != ADOPTED_TABLE_DIGEST:
        sys_exit(f"adopted-table digest drift {digest}")

    # --- self-publication gates: merged head of record + merge audits ----
    if sha(OUT / MERGED_NAME) != MERGED_SHA_EXPECTED:
        sys_exit("published merged cache of record sha drift")
    if (OUT / MERGED_NAME).stat().st_size != MERGED_BYTES_EXPECTED:
        sys_exit("published merged cache of record byte-size drift")
    merged_rows = 0
    merged_wins = 0
    merged_loss = 0
    for line in (OUT / MERGED_NAME).read_text(encoding="utf-8-sig").splitlines():
        if not line or line.lstrip().startswith("#"):
            continue
        f = line.split(",")
        if len(f) != 6 or f[0] != "s5verdict":
            sys_exit(f"invalid merged cache row: {line}")
        merged_rows += 1
        if int(f[4]) == 1:
            merged_wins += 1
        elif int(f[4]) == 2:
            merged_loss += 1
    if (merged_rows, merged_wins, merged_loss) != (6801, 201, 6600):
        sys_exit(f"merged cache of record census drift {merged_rows}/"
                 f"{merged_wins}/{merged_loss}")
    if merged_wins - BASE_CACHE_WIN_EXPECTED != 2:
        sys_exit("merged cache WIN delta must be exactly the 2 adopted rows")
    for i in (1, 2, 3):
        if sha(OUT / f"merge-audit-run{i}.json") != \
                MERGE_AUDIT_SHA_EXPECTED:
            sys_exit(f"merge-audit-run{i}.json sha drift")
    ma = json.loads((OUT / "merge-audit-run1.json").read_text())
    if ma["tool"] != "s5_union_merge.py" \
            or ma["output_sha256"] != MERGED_SHA_EXPECTED \
            or ma["output_bytes"] != MERGED_BYTES_EXPECTED \
            or ma["unique_rows"] != 6801 \
            or ma["duplicate_rows_elided"] != 0 \
            or ma["verdict_counts"] != {"WIN(1)": 201, "LOSS(2)": 6600} \
            or ma["nodes_field_mismatches_recorded"] != [] \
            or [inp["sha256"] for inp in ma["inputs"]] != \
            [BASE_CACHE_SHA_EXPECTED, ADOPTED_INCREMENT_SHA]:
        sys_exit("merge-audit record field drift")
    if ma["inputs"][0]["rows"] != 6799 or ma["inputs"][1]["rows"] != 2 \
            or ma["inputs"][0]["unique_new"] != 6799 \
            or ma["inputs"][1]["unique_new"] != 2:
        sys_exit("merge-audit input accounting drift")
    if "11x11 root questions remain UNKNOWN" not in ma["interpretation_guard"]:
        sys_exit("merge-audit interpretation guard drift")

    # --- emit increment + manifest ----------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    # byte-stable emit order of the pinned increment of record (k33 then
    # k20, i.e. ascending key_hi; kept fixed so the emitted bytes and the
    # already-pinned increment sha / merge-audit input pin stay identical)
    rowlines = [f"s5verdict,{r[0]},{r[1]},5,1,{r[2]}"
                for r in ((12682136550675320832, 65536, 15842649),
                          (10376293541461626880, 33619968, 16196331))]
    for line in rowlines:
        f = line.split(",")
        lo, hi, legal, result, nodes = int(f[1]), int(f[2]), int(f[3]), \
            int(f[4]), int(f[5])
        if (lo, hi, nodes) not in {(r[0], r[1], r[4]) for r in adopted_rows}:
            sys_exit("emit-order row not in the gated adopted table")
    if len(rowlines) != 2:
        sys_exit("emitted row count drift")
    blob = ("\n".join(HDR_LINES + rowlines) + "\n").encode("utf-8")
    incr_sha = hashlib.sha256(blob).hexdigest()
    if incr_sha != ADOPTED_INCREMENT_SHA:
        sys_exit(f"emitted increment sha drift {incr_sha} "
                 f"!= pinned {ADOPTED_INCREMENT_SHA}")
    existing = (OUT / INCREMENT_NAME)
    if existing.is_file() and existing.read_bytes() != blob:
        sys_exit("on-disk increment differs from the emitted blob")
    (OUT / INCREMENT_NAME).write_bytes(blob)

    adopted_table = [
        {"lo": lo, "hi": hi, "legal": legal, "result": 1, "nodes": nodes,
         "s5_index": s5_index, "serving_class": serving_class,
         "owner_classes_graph": owners}
        for lo, hi, legal, result, nodes, s5_index, serving_class, owners
        in sorted(adopted_rows)]

    manifest = {
        "schema": SIXTHWIN3_SCHEMA,
        "part": "SQ",
        "date": "2026-11-26",
        "win_canonical_adoption": True,
        "canonical_head_published_by_this_part": {
            "merged_cache_name": MERGED_NAME,
            "merged_cache_sha256": MERGED_SHA_EXPECTED,
            "merged_cache_bytes": MERGED_BYTES_EXPECTED,
            "merged_cache_rows": 6801,
            "merged_cache_win_loss": [201, 6600],
            "merge_audit_runs": 3,
            "merge_audit_sha256_x3_identical": MERGE_AUDIT_SHA_EXPECTED,
            "merger": "pinned byte-clone of the published union merger "
                      "(sha256 90711961..., this kit scripts/s5_union_merge.py)",
            "note": "no pre-declaration dossier exists for sixthwin3 "
                    "(unlike EW's sixthwin5); this Part SQ publishes the "
                    "merged head of record itself at this kit's output/ "
                    "directory; three independent merge runs produced "
                    "byte-identical output and byte-identical audit records",
        },
        "source_class": {
            "class": f"{CLASS_MASK[0]}:{CLASS_MASK[1]}",
            "class_children_total": 108, "s5_unknown_before": 101,
            "unknown_exclusive": 43, "serving_class_index": SERVING_CLASS,
            "note": "the sixth-cost live candidate class (s4 class 3077, "
                    "coverage {80,84,100,108}); k20/k33 are positions 20/33 "
                    "of the same published probe selection exclusive_probe_"
                    "order of record (d5e9b059...), resolved by the "
                    "parked4rest2 L50M ladder over their pinned 15,000,000 "
                    "park-at-UNKNOWN baselines",
            "adoption_requirement_of_record":
                "the parked4rest2 halt-audit's pre-registered WIN-row "
                "requirement: published C++ second-implementation "
                "verification of the replica raw rows (pinned "
                "cpp/solvers/kyouen_dfpn_root.cpp sha256 9193f5b6...); "
                "satisfied for both rows by the Part SN kit (GATE-PASS); "
                "any C++ disagreement fails closed in favor of discarding "
                "the row; third-implementation verdict-level corroboration "
                "(the k20/k33 third-impl addendum, auditor re-run live) is "
                "additionally recorded for both rows per the repo's "
                "sixthwin5/sixthwin2 adoption pattern",
        },
        "pools": [
            {"pool": "parked4rest2-l50m-ladder",
             "kit": P4R_EXP,
             "budget": L50M_BUDGET,
             "park_budget": PARK_BUDGET,
             "margin_budget": MARGIN_BUDGET,
             "adopted_win_ids": list(ADOPTED_IDS),
             "standing_unconsumed_keys_not_adopted": {
                 "k38": "the still-parked key k38 of the same probe "
                        "selection (15,000,000 park-at-UNKNOWN, NO L50M "
                        "follow-up claimed - the coverage asymmetry the "
                        "k20/k33 third-impl completion pre-registered)",
             },
             "adopted_nodes": ADOPTED_NODES_TOTAL,
             "kit_integrity": {
                 "note": "the parked4rest2 ladder kit is MANIFEST-verified "
                         "file-by-file here (26/26); the consumed bytes "
                         "are additionally pinned directly: README, "
                         "jsreplay.js, halt-audit.json, status.log, the 6 "
                         "input CSVs (batch-k20/k33 and the 4 validation "
                         "anchors) and all 14 raw CSV files "
                         "(raw_file_sha256_pins / input_csv_sha256_pins "
                         "below)",
                 "kit_manifest_sha256": P4R_MANIFEST_SHA,
                 "kit_files_verified": P4R_KIT_FILES,
                 "readme_sha256": P4R_README_SHA,
                 "jsreplay_sha256": P4R_JSREPLAY_SHA,
                 "halt_audit_sha256": P4R_HALTAUDIT_SHA,
                 "halt_audit_pins": {
                     "gates_passed_count": 75,
                     "halted_on_win_keys": adopted_key_strs,
                     "lane_time_base_chain_sha256": "16a12390...",
                     "lane_time_base_note": "the halt-audit and the Part SN "
                         "gate-rows pin the lane-time canonical head "
                         "16a12390 (pre-SP); freshness vs the current "
                         "cc3694bb head (this Part's BASE) is gated "
                         "directly below and measured by the census "
                         "measurer (flip set exactly {2402, 3054})",
                 },
                 "status_log_sha256": P4R_STATUS_SHA,
                 "input_csv_sha256_pins": P4R_INPUT_SHAS,
                 "raw_file_sha256_pins": P4R_RAW_SHAS,
                 "validation_anchor_replays": {k: list(v) for k, v in
                                                P4R_VAL_PINS.items()},
                 "input_csv_cross_registration":
                     "batch-k20/batch-k33 are byte-equal to the Part SN "
                     "kit's MANIFEST-pinned gate inputs and to the "
                     "third-impl addendum's row-spec inputs; the val "
                     "anchors are byte-equal to the Part SN kit's pinned "
                     "anchor-at2m input family",
             }},
            {"pool": "sn-cpp-second-implementation-gate",
             "kit": SN_EXP,
             "kit_integrity": {
                 "note": "Part SN kit verified file-by-file against its "
                         f"published MANIFEST-sha256 {SN_MANIFEST_SHA[:8]}... "
                         f"({SN_KIT_FILES} files)",
                 "kit_manifest_sha256": SN_MANIFEST_SHA,
                 "kit_files_verified": SN_KIT_FILES,
                 "readme_sha256": SN_README_SHA,
                 "gate_rows_json_sha256": SN_GATEROWS_SHA,
                 "gate_rows_all_pass": SN_GATES_TOTAL,
                 "gate_status_log_sha256": SN_STATUS_SHA,
                 "gate_status_gate_pass_rows": 5,
                 "audit_gate_json_sha256": SN_AUDIT_SHA,
                 "audit_run1_run2_run3_sha256_identical": SN_AUDIT_SHA,
                 "cpp_solver_sha256": SN_CPP_SHA,
                 "cpp_solver_commit": SN_CPP_COMMIT,
             },
             "canonical_head_cross_gate":
                 "the SN gate-rows.json canonical_head block pins the "
                 "lane-time head 16a12390 (6,797 rows, WIN 197 / LOSS 6600; "
                 "the SN gate ran before Part SP merged) and records the 2 "
                 "adopted targets as fresh versus exactly that head, with "
                 "raw/margin/run3 sha cross-registration to the "
                 "parked4rest2 ladder raws (gated here); freshness vs the "
                 "current cc3694bb head is re-gated by this Part directly"},
            {"pool": "k20k33-third-implementation-verdict-reverify",
             "kit": TI_EXP,
             "covered_ids": list(ADOPTED_IDS),
             "kit_integrity": {
                 "note": "the k20/k33 third-impl addendum (published inside "
                         "the k01-k03 third-impl kit) is gated here "
                         "directly on its published bytes and re-verified "
                         "LIVE: the data-driven auditor audit_k20k33.py is "
                         "re-run twice in this maker with rc=0, 49/49 "
                         "gates, byte-identical stdout; the cold a/b/v "
                         "witness raws, C1 fresh-calibration raws, C4 "
                         "negative-gate raws, tamper-controls log and the "
                         "per-row replica-raw copies (byte-equal to the "
                         "ladder raws) are all sha-pinned and field-gated",
                 "auditor_sha256": TI_AUDITOR_SHA,
                 "third_impl_js_sha256": TI_THIRD_IMPL_SHA,
                 "verify_tbl_js_sha256": TI_VERIFY_TBL_SHA,
                 "tamper_controls_log_sha256": TI_TAMPER_LOG_SHA,
                 "cold_raw_sha256_pins": TI_COLD_SHAS,
                 "row_pins": TI_ROW_PINS,
                 "auditor_live_rerun": "rc=0, 49/49 gates, deterministic "
                                       "byte-identical stdout x2",
             },
             "verdict_agreement_note":
                 "third-impl WIN(1) verdict-level agreement for k20/k33 "
                 "with 3 identical cold runs each (expansions 19,455,330 / "
                 "18,829,006, tt-hits 10,071,309 / 10,066,094, tt-overwrites "
                 "15,261,026 / 14,634,702); expansions legitimately differ "
                 "from replica node counts (different implementations); "
                 "the addendum's replica raw copies are byte-equal to the "
                 "parked4rest2 ladder raws",
             "standing_unconsumed_loss_rows":
                 "the 30 fifth-resumption verified LOSS rows of the Part "
                 "SL batch are NOT adopted and NOT emitted by this Part; "
                 "they remain unconsumed honest LOSS labels WITHOUT a "
                 "delegated C++ second-implementation gate (coverage "
                 "asymmetry disclosed)",
             "standing_parked_keys": STANDING_PARKED_KEYS,
        },
        ],
        "resolved_ids": list(ADOPTED_IDS),
        "win_ids": list(ADOPTED_IDS),
        "loss_ids": [],
        "win_ties": [],
        "win_ties_note": "no consumed-WIN regression ties: both adopted "
                         "keys are fresh to BASE",
        "row_counts": {
            "adopted_win_rows": 2,
            "win_ties_consumed_elsewhere": 0,
            "standing_unconsumed_loss_rows": SL_STANDING_LOSS_ROWS,
            "standing_unconsumed_parked_keys": len(STANDING_PARKED_KEYS),
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
            "Part SQ canonical WIN-only adoption increment: the 2 fresh "
            "exact-WIN rows (each cold two-pass node-exact at 50M over the "
            "pinned 15M park-at-UNKNOWN baseline, plus a 32M budget-margin "
            "re-proof and a voluntary third cold 50M verify run, solved "
            "within budget, C++-gated by Part SN and third-implementation-"
            "corroborated by the k20/k33 third-impl addendum re-run live) "
            "are consumed into the canonical chain via the fail-closed "
            "union merger whose output this Part publishes as the merged "
            "head of record (02db5ab3..., 6,801 rows WIN 201 / LOSS 6,600); "
            "WIN-only adoption asserts no root verdict and frees no class; "
            "owner classes of the adopted keys are excluded_now by the "
            "win-hit mechanism, derived machine-only by the reaudit refresh "
            "(flip set exactly {2402, 3054}; serving class 3077 stays "
            "excluded_now with cost-unknown 93 -> 91); nodes are "
            "bookkeeping, never verdicts; the standard 11x11 empty board "
            "and every central-reply root stay UNKNOWN",
        "provenance": {
            "part_maker_reverified_live": True,
            "merged_cache_published_by_this_part": True,
            "parked4rest2_kit_files_verified": P4R_KIT_FILES,
            "sn_kit_files_verified": SN_KIT_FILES,
            "third_impl_auditor_live_rerun": True,
            "probe_kit_direct_pins": True,
            "raws_published": True,
        },
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "part": "SQ",
        "head_of_record": "cc3694bb... -> 02db5ab3... (6,801 rows "
                          "WIN 201 / LOSS 6,600)",
        "increment_sha256": incr_sha,
        "rows": len(rowlines),
        "adopted_nodes_total": ADOPTED_NODES_TOTAL,
        "digest": digest,
        "manifest_sha256": hashlib.sha256(
            (OUT / "increments-manifest.json").read_bytes()).hexdigest(),
    }))


if __name__ == "__main__":
    main()
