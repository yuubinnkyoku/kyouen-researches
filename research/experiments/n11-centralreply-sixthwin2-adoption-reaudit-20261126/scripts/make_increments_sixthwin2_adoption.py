#!/usr/bin/env python3
"""Build the Part SP sixthwin2 (2 unconsumed parked4 L50M ladder WIN rows)
canonical WIN-adoption increment, fail-closed.

Part SP kit n11-centralreply-sixthwin2-adoption-reaudit-20261126
(2026-11-26).  This IS the adoption Part declared emission: the canonical
head of record advances from merged-exact-s5-chain-plus-sixthwin5 (sha256
16a12390..., 6,797 rows WIN 197 / LOSS 6,600; the Part EW adoption head
of record, published by the sixthwin5 dossier kit) to
merged-exact-s5-chain-plus-sixthwin2 (sha256 cc3694bb..., 6,799 rows
WIN 199 / LOSS 6,600) by consuming exactly the 2 unconsumed parked4
L50M ladder exact-WIN rows of the sixth-cost class
10376293541461626880:65536: k13 1152921573327376384:536870912 and
k19 10376293541461626880:65664 (positions 13/19 of the published probe
selection exclusive_probe_order, budget 50,000,000 over the pinned
15,000,000 park-at-UNKNOWN baselines).  The verdict scope of the Part is
exactly those 2 WIN rows: NO root verdict, NO 11x11 outcome, NO class
freed (owner classes of the adopted keys are excluded_now by the
win-hit mechanism; the pre-declaration halt-audit's lane-time if-adopted
prediction was computed against the older 6e49dd84 head and is NOT the
measurement of record; the SP census measurement against the current
16a12390 head measures exactly 2 unknown -> excluded_now flips:
2624 owner of k19 and 30136 owner of k13, with the serving class 3077
already excluded_now since Part EW and its cost-unknown count 95 -> 93).

Structural clone of the published Part EW maker `make_increments_
sixthwin5.py` (sha256 9e6bf992...): the computation region (all
source-kit byte gates, multi-pass payload gates, SM gate-kit MANIFEST
verification, SL batch audit gates, freshness/quarantine/canonical-
safety gates, adopted-table digest) is byte-identical logic; the
disclosed diff regions are the docstring, the source pools (parked4
L50M ladder replaces the 15M probe ladder; the SM C++ gate kit replaces
the SK kit; the SL third-implementation batch replaces the TI audits
and the ea73c3e3 witness), the emitted increment header block, the
output file name and the manifest fields (this Part also publishes the
merged cache of record itself: no pre-declaration dossier exists for
sixthwin2, so there is no dossier-supersession region and instead the
merged cache and its three byte-identical merge audits are pinned and
gated here).

Each adopted row is gated at FOUR independent implementations, all
re-verified here byte-for-byte or field-for-field:

1. the parked4 ladder kit's jsreplay replica
   (n11-sixthcost-class10376293541461626880-parked4-s5-l50m-ladder-20261126):
   15,000,000 park-at-UNKNOWN baseline PLUS the 50M primary battery
   (cold run1/run2 two-pass node-exact), the 32,000,000 budget-margin
   re-proof and the voluntary third cold 50M verify run, identical
   (result, nodes) = (1, 16,402,480) / (1, 15,379,062) across all runs,
   plus 4 validation-anchor replays (2M park-UNKNOWN and 15M honest
   LOSS rows of pinned anchor keys);
2. the published Part SM pinned C++ second-implementation scrutiny
   gate kit n11-sixthcost-parked4-l50m-cppgate-20261126 (MANIFEST-
   verified file-by-file, 28/28): GATE-PASS for every row with 2-pass
   determinism and published-raw node-exact (the pre-registered
   adoption requirement the halt-audit delegates, sha-pinned C++
   solver 9193f5b6...);
3. the Part SL third-implementation batch audit
   (n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122,
   out/audit-k09k43-summary.json): verdict-level WIN agreement per
   key, 3 identical cold third-impl runs each (expansions 19,433,195 /
   17,955,947 with tt-hits 10,181,270 / 9,504,863 and pinned
   tt-overwrites 15,238,891 / 13,761,643; expansions legitimately
   differ from replica node counts - different implementations),
   replica 4-run unanimity and park-baseline replica rows pinned;
4. the probe kit's published selection JSON (d5e9b059...): k13/k19
   are exactly the exclusive_probe_order entries at positions 13 and
   19 of the same sixth-cost class selection of record.

The 2 adopted (lo,hi) pairs are proven absent from BASE (fresh-increment
gate), absent from the active quarantine registry and canonical-safe
per s5_evidence_policy; the adopted-table digest and the emitted
increment sha are self-pinned; this Part additionally re-verifies the
published merged head of record byte-for-byte (cc3694bb..., 6,799 rows)
and its three byte-identical merge audit records.  The standing
unconsumed rows are recorded but NOT adopted and NOT emitted: the two
parked4rest2 L50M WIN rows k20/k33 (third-implementation corroboration
absent at Part SP build time; their C++ gate kit Part SN was in flight -
disclosed) and the 30 fifth-resumption verified LOSS rows of the Part
SL batch.  This Part adopts no LOSS row.

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
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
MERGER = EXP / "scripts/s5_union_merge.py"

B5_EXP = "n11-centralreply-sixthwin5-adoption-predecl-20261126"
PARKED4_EXP = ("n11-sixthcost-class10376293541461626880-"
               "parked4-s5-l50m-ladder-20261126")
SM_EXP = "n11-sixthcost-parked4-l50m-cppgate-20261126"
SL_EXP = ("n11-sixthcost-k01-k03-thirdimpl-verdict-"
          "reverification-20261122")
PROBE_EXP = "n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121"

BASE_CACHE = ROOT / "research/experiments" / B5_EXP / (
    "output/merged-exact-s5-chain-plus-sixthwin5-20261126.cache")
PARKED4_DIR = ROOT / "research/experiments" / PARKED4_EXP
SM_DIR = ROOT / "research/experiments" / SM_EXP
SL_DIR = ROOT / "research/experiments" / SL_EXP
PROBE_DIR = ROOT / "research/experiments" / PROBE_EXP
GRAPH = (ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"
         "/output/dependency-graph.json.gz")
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
POLICY = (ROOT / "research/experiments/n11-frontier-selection-20261005"
          "/scripts/s5_evidence_policy.py")

MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA_EXPECTED = "16a12390c0c3f046f0ae537b2a9940e15661263fc5034ce1b155c138bb9043cd"
BASE_CACHE_ROWS_EXPECTED = 6797
BASE_CACHE_WIN_EXPECTED = 197
BASE_CACHE_LOSS_EXPECTED = 6600
QUARANTINE_SHA_EXPECTED = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
POLICY_SHA_EXPECTED = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
GRAPH_SHA_EXPECTED = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"

# parked4 ladder kit direct pins (the kit holds no MANIFEST-sha256;
# every consumed byte is pinned directly here, as with the probe kit)
P4_README_SHA = "f021e14bd33bf3fc701473ec393ce96702c1ed3a9341b52bffdfdf13bda487ac"
P4_JSREPLAY_SHA = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
P4_HALTAUDIT_SHA = "9baeb8bebc09cbdb6812d5d3815e5ef00ff0fdfeead4ddb1a5b1f2dd3a5c5703"
P4_STATUS_SHA = "ea493ae9c886ebc38bb0355f2801c44e31109dc906b35f88254ef32c1d000be9"
PARK_BUDGET = 15000000
L50M_BUDGET = 50000000
MARGIN_BUDGET = 32000000

ADOPTED_IDS = ["k13", "k19"]
# (lo, hi, legal, s5_index, order_position_1based) - machine-derived from
# the published selection JSON exclusive_probe_order (0-based index 12/18
# = positions 13/19), cross-gated below against the halt-audit, the raw
# replay rows and the frozen dependency graph.
ADOPTED_KEY_PINS = {
    "k13": (1152921573327376384, 536870912, 95, 112203, 13),
    "k19": (10376293541461626880, 65664, 95, 103319, 19),
}
# (result, nodes) of the resolving 50M condition per adopted key -
# machine-derived from the published raws, cross-gated below.
ADOPTED_LABEL_PINS = {
    "k13": (1, 16402480),
    "k19": (1, 15379062),
}
ADOPTED_NODES_TOTAL = 31781542

# standing unconsumed rows outside this Part (recorded, NOT adopted,
# NOT emitted): k20/k33 parked then never started by this lane
# (later resolved WIN(1) by the parked4rest2 ladder; no third-impl
# corroboration at SP build time; their C++ gate kit Part SN was in
# flight - disclosed) and the 30 verified LOSS rows of the Part SL
# fifth-resumption batch.
PARKED_NEVER_STARTED_KEYS = [
    "10376293541461626880:33619968",   # k20
    "12682136550675320832:65536",      # k33
]

P4_INPUT_SHAS = {
    "batch-k13.input.csv": "298dd6e6b6655d12aefaae138a2e1d85388220546ff68e4d6b7081c6097b0526",
    "batch-k19.input.csv": "88c107d7d060ef756a394d722de3a80b4ee60bad5647785cbbb65eb088da6190",
    "batch-k20.input.csv": "0984400f8aa99735e11e2638f5bc9a9273ddd296e845f7b7118f3ada81adddad",
    "batch-k33.input.csv": "ca081b0f2f85e62b39cbbd1178a7be839c87e3446b2357657bbfe8681f82e2f4",
    "val-at2m-first.input.csv": "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
    "val-at2m-second.input.csv": "56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62",
    "val-first-15m.input.csv": "ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348",
    "val-second-15m.input.csv": "56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62",
}

P4_RAW_SHAS = {
    "base15m-1152921573327376384-536870912.out.csv": "c911a74041642a526584f4c0612908d0564d2595b1872aeffa1b57ec296d4f67",
    "l50m-run1-1152921573327376384-536870912.out.csv": "b14273ee1a2b2c60375041f979db13f37c4b0b0b77d51e561bdf8abbac683985",
    "l50m-run2-1152921573327376384-536870912.out.csv": "155ffe291e6d1c106bda6e31515ae481032b63fee8578bdde52d26101ab4ebe4",
    "l50m-run3-verify-1152921573327376384-536870912.out.csv": "979b11478c30b16c03630a1700e04421d25df7bf9437e981d2c0b35bf4799968",
    "l50m-margin-1152921573327376384-536870912.out.csv": "9b6a0026caf8781d268d9e9da16b2cc7389ffd1e23aae92dc136c1d2464c94eb",
    "base15m-10376293541461626880-65664.out.csv": "34e9a2b7aef6f5c60eb2dfbb2813cb663cf383af71e5852720529bfa01337539",
    "l50m-run1-10376293541461626880-65664.out.csv": "0e1287abba7d7f012f8e42bc9f774ec6cc093b46c54fb40f570f7c6d1c891abb",
    "l50m-run2-10376293541461626880-65664.out.csv": "0e1287abba7d7f012f8e42bc9f774ec6cc093b46c54fb40f570f7c6d1c891abb",
    "l50m-run3-verify-10376293541461626880-65664.out.csv": "eb624fcf4e753114ad708406b35683eedb3b1811be80fdb005c2eeed726ad3a5",
    "l50m-margin-10376293541461626880-65664.out.csv": "be8f4289607c24e1cba48b3bd4efac15e80874fec7987cef3c037d7de53a7517",
    "val-at2m-first.out.csv": "2bbfeba091014b8a38f54a1fee29f32ae610beaf02f9b1f5c92ae07cc00fa1de",
    "val-at2m-second.out.csv": "0af850c443c5574f5a806c760bc236f7937c109003e7bf6ca7e3b5b023646481",
    "val-first-15m.out.csv": "e5d33b954b81b6d766d870eff54a5425e6a0faf09cde049ce463920f8d4f9a25",
    "val-second-15m.out.csv": "5957bce29e5fa27fa3b67f0be6552ecac39e294c14cc3452cbc7711228cedc02",
}

# validation-anchor replay expectations (honesty ladder: 2M park-UNKNOWN
# then 15M honest LOSS, exact replays of pinned anchor keys)
P4_VAL_PINS = {
    "val-at2m-first": (98, 2000000, 0, 2000000, 1152921504606851072, 536870946),
    "val-at2m-second": (99, 2000000, 0, 2000000, 1188950301626860544, 536870912),
    "val-first-15m": (98, 15000000, 2, 3651923, 1152921504606851072, 536870946),
    "val-second-15m": (99, 15000000, 2, 5040200, 1188950301626860544, 536870912),
}

# Part SM pinned C++ second-implementation scrutiny gate kit
SM_MANIFEST_SHA = "976e079c069379d51efb2a36d3b7d8919ef30aae577764615d73468ebc6f4abe"
SM_KIT_FILES = 28
SM_README_SHA = "92a88c3e8d6607c094aa392f46afbec733070a80c9af749d2cd0750e4dc5a296"
SM_GATEROWS_SHA = "9818accccba39af567c6a5b9f5e32a5267838a4a0299c691cf4a2ede7f60581a"
SM_STATUS_SHA = "e0a1159e009b02d8a32ccb9c72a904055646f41ec5d2d60ce8bca44d7dc874e7"
SM_AUDIT_SHA = "a11983dda3b2279d530ccda5a8ed4ab00620648175568d99f92876000eb96f52"
SM_GATES_TOTAL = 66
SM_CPP_SHA = "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e"
SM_CPP_COMMIT = "154f3b7a67b97e13acbaee8b04dc74ddca728d19"
SM_ANCHOR_PINS = {
    "anchor-at2m": (98, 2000000, 0, 2000000),
    "anchor-aj001": (84, 30000000, 2, 5156075),
    "anchor-af039": (89, 30000000, 2, 19234232),
}

# Part SL third-implementation batch audit (single pinned summary file)
SL_SUMMARY_REL = "out/audit-k09k43-summary.json"
SL_SUMMARY_SHA = "300c8c0a61e4e5fe5fb1a8a5a1fe32aaebd391ec767dc2783f3b87cfd943728e"
SL_ROWS_AUDITED = 32
SL_STANDING_LOSS_ROWS = 30
SL_ROW_PINS = {
    "k13": {"key": "1152921573327376384:536870912", "legal": 95,
            "expansions": 19433195, "tt_hits": 10181270,
            "ttoverwrites": 15238891},
    "k19": {"key": "10376293541461626880:65664", "legal": 95,
            "expansions": 17955947, "tt_hits": 9504863,
            "ttoverwrites": 13761643},
}

# probe kit selection JSON (the selection of record for this class)
PROBE_SELECTION_SHA = "d5e9b059611849f7b7e69c7370a0e66cd7535c43b3a043ce9f5bfc0e5ff72e87"

# published outputs of this Part (self-pinned; the merged head of record
# is published BY this Part, so it is gated here byte-for-byte)
MERGED_NAME = "merged-exact-s5-chain-plus-sixthwin2-20261126.cache"
MERGED_SHA_EXPECTED = "cc3694bbe871ccf27bdf4dbcf5e93586da440164fd75c02c15dc2a0ae46d11b8"
MERGED_BYTES_EXPECTED = 284127
MERGE_AUDIT_SHA_EXPECTED = "5904693ec6836515c2523d5a5b8744e4f515e56400e3288a07dff30e6875f9cf"

ADOPTED_TABLE_DIGEST = "e7e2b30d5e5ee504f299ec1e64ecf2c252d9d3ca412299d38932628e8844bd83"
ADOPTED_INCREMENT_SHA = "89bff217885ef89ae7a86d9580657818bdf4c7619ef24da7efd6392169aa1694"
SERVING_CLASS = 3077
CLASS_MASK = (10376293541461626880, 65536)

INCREMENT_NAME = "increment-sixthwin2-adoption-20261126.cache"
SIXTHWIN2_SCHEMA = "sixthwin2-adoption-increments-manifest-v1"

HDR_LINES = [
 "# n11 central-reply closure sixthwin2 canonical-adoption increment",
 "#   (Part SP, n11-centralreply-sixthwin2-adoption-reaudit-20261126,",
 "#   2026-11-26) - WIN-only, fresh 2-row increment.  Part SP declares the",
 "#   sixthwin2 canonical WIN adoption: the canonical head of record advances",
 "#   to merged-exact-s5-chain-plus-sixthwin2 (6,799 rows WIN 199 / LOSS",
 "#   6,600) by consuming exactly the 2 unconsumed parked4 L50M ladder",
 "#   exact-WIN rows of the sixth-cost class 10376293541461626880:65536:",
 "#   k13 1152921573327376384:536870912 and k19 10376293541461626880:65664",
 "#   (budget 50,000,000 over the pinned 15,000,000 park-at-UNKNOWN",
 "#   baselines).",
 "# The sources of record (all re-verified live by the Part maker against",
 "#   published bytes): the parked4 ladder's four-run primary battery (50M",
 "#   cold two-pass node-exact, 32M budget-margin re-proof, voluntary third",
 "#   cold 50M verify; k13 nodes 16,402,480 / k19 nodes 15,379,062), the",
 "#   Part SM pinned C++ second-implementation scrutiny gate (GATE-PASS,",
 "#   two fresh-cold passes per row, node-exact 95,50000000,1,16402480 /",
 "#   95,50000000,1,15379062), and the Part SL third-implementation batch",
 "#   audit (verdict-level WIN agreement, 3 identical cold runs each,",
 "#   expansions 19,433,195 / 17,955,947; expansions legitimately differ",
 "#   from replica node counts - different implementations).  Adopted node",
 "#   total 31,781,542.",
 "# NOT consumed and NOT emitted (standing unconsumed rows, outside this",
 "#   Part): the two parked4rest2 L50M WIN rows k20/k33 (third-",
 "#   implementation corroboration absent at Part SP build time; their C++",
 "#   gate kit Part SN was in flight - disclosed) and the 30 fifth-",
 "#   resumption verified LOSS rows of the Part SL batch.",
 "# Every adopted key is fresh to BASE 16a12390..., quarantine-free,",
 "#   canonical-safe per s5_evidence_policy.",
 "# This Part publishes the merged cache of record itself (no pre-",
 "#   declaration dossier exists for sixthwin2): merger = the pinned",
 "#   byte-clone of s5_union_merge.py 90711961..., output pinned in this",
 "#   kit's MANIFEST; win_ties = [] (both keys are fresh to BASE).",
 "# WIN-only adoption asserts NO root verdict and frees no class; the",
 "#   measured census delta is exactly 2 unknown -> excluded_now win-hit",
 "#   flips: class 2624 (1297600742147751936:0, owner of k19) and class",
 "#   30136 (1152921573327376384:0, owner of k13); serving class 3077",
 "#   cost-unknown 95 -> 93 with status already excluded_now (Part EW);",
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
        sys_exit("base cache (Part EW head of record) sha drift")
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

    # --- parked4 ladder kit: direct byte pins (no MANIFEST) -------------
    if not PARKED4_DIR.is_dir():
        sys_exit(f"parked4 ladder kit dir missing {PARKED4_DIR}")
    if sha(PARKED4_DIR / "README.md") != P4_README_SHA:
        sys_exit("parked4 kit README sha drift")
    if sha(PARKED4_DIR / "scripts/jsreplay.js") != P4_JSREPLAY_SHA:
        sys_exit("parked4 kit jsreplay.js sha drift")
    if sha(PARKED4_DIR / "output/halt-audit.json") != P4_HALTAUDIT_SHA:
        sys_exit("parked4 kit halt-audit.json sha drift")
    if sha(PARKED4_DIR / "output/raw/status.log") != P4_STATUS_SHA:
        sys_exit("parked4 kit status.log sha drift")

    h = json.loads((PARKED4_DIR / "output/halt-audit.json").read_text())
    if h["schema"] != "n11-sixthcost-parked4-l50m-ladder-halt-audit-v1":
        sys_exit("parked4 halt-audit schema drift")
    if h["all_gates_pass_before_halt"] is not True \
            or h["gates_passed_count"] != 77:
        sys_exit("parked4 halt-audit gate accounting drift")
    adopted_key_strs = [f"{ADOPTED_KEY_PINS[k][0]}:{ADOPTED_KEY_PINS[k][1]}"
                        for k in ADOPTED_IDS]
    if h["halted_on_win_keys"] != adopted_key_strs:
        sys_exit("parked4 halt-audit halted_on_win_keys drift")
    pins = h["pins"]
    if pins["jsreplay_sha256"] != P4_JSREPLAY_SHA \
            or pins["parent_selection_json_sha256"] != PROBE_SELECTION_SHA \
            or pins["quarantine_sha256"] != QUARANTINE_SHA_EXPECTED \
            or pins["policy_sha256"] != POLICY_SHA_EXPECTED:
        sys_exit("parked4 halt-audit pins block drift")
    # the halt-audit pins the lane-time canonical head 6e49dd84 (pre-EW):
    # disclosed, NOT asserted equal to this Part's BASE (the lane ran
    # before Part EW merged; freshness vs the current head is gated below)
    probe = h["probe"]
    if probe["started_keys"] != adopted_key_strs:
        sys_exit("parked4 halt-audit started_keys drift")
    if sorted(probe["never_started_keys_stay_parked_15m"]) != \
            sorted(PARKED_NEVER_STARTED_KEYS):
        sys_exit("parked4 halt-audit never-started parked keys drift")
    if probe["resolved_loss_raw"] != []:
        sys_exit("parked4 halt-audit resolved_loss_raw drift")
    if sorted(probe["win_raws_needing_scrutiny"]) != sorted(adopted_key_strs):
        sys_exit("parked4 halt-audit win_raws_needing_scrutiny drift")
    for kid in ADOPTED_IDS:
        pk = probe["per_key"][kid]
        lo, hi, legal, _s5, pos = ADOPTED_KEY_PINS[kid]
        res, nodes = ADOPTED_LABEL_PINS[kid]
        if pk["key"] != f"{lo}:{hi}" or pk["legal"] != legal \
                or pk["position"] != pos or pk["verdict"] != "WIN":
            sys_exit(f"parked4 halt-audit per_key header drift: {kid}")
        stages = pk["stages"]
        if stages["base15m"] != {"result": 0, "nodes": PARK_BUDGET}:
            sys_exit(f"parked4 halt-audit base15m park stage drift: {kid}")
        if stages["at50m"] != {"result": res, "nodes": nodes} \
                or stages["at50m_run2"] != {"result": res, "nodes": nodes}:
            sys_exit(f"parked4 halt-audit 50M determinism pair drift: {kid}")
        if stages["margin_reproof"] != {"budget": MARGIN_BUDGET,
                                        "result": res, "nodes": nodes}:
            sys_exit(f"parked4 halt-audit margin re-proof drift: {kid}")
        if stages["voluntary_run3_verify"] != {"budget": L50M_BUDGET,
                                               "result": res, "nodes": nodes}:
            sys_exit(f"parked4 halt-audit voluntary verify drift: {kid}")
    if "NO verdict is consumed" not in h["status_guard"] or "remain UNKNOWN" not in h["status_guard"]:
        sys_exit("parked4 halt-audit status guard drift")

    # parked4 status.log: SSOT stage lines for the adopted keys
    slines = (PARKED4_DIR / "output/raw/status.log").read_text().splitlines()
    for kid in ADOPTED_IDS:
        res, nodes = ADOPTED_LABEL_PINS[kid]
        want = [
            f"start {kid} 07:38:31",
            f"done {kid} base15m rc=0 res=0 nodes={PARK_BUDGET}",
            f"done {kid} l50m-run1 rc=0 res={res} nodes={nodes}",
            f"done {kid} l50m-run2 rc=0 res={res} nodes={nodes}",
            f"done {kid} margin32m rc=0 res={res} nodes={nodes}",
            f"key {kid} status=WIN-halt res50m={res} nodes={nodes}",
            f"done {kid} run3-verify rc=0",
        ]
        for w in want:
            if w not in slines:
                sys_exit(f"parked4 status.log missing stage line: {kid}: {w}")
    sjoined = "\n".join(slines)
    if "lane halted on WIN stop rule 1: keys k13,k19 resolved WIN; k20,k33 " \
       "never started (remain parked@15M, claimable)" not in sjoined:
        sys_exit("parked4 status.log missing lane-halt line")
    if "voluntary run3-verify completed for both WIN keys (identical " \
       "result/nodes)" not in sjoined:
        sys_exit("parked4 status.log missing voluntary verify line")

    # parked4 input CSVs: direct pins (row-spec shape + never-started keys)
    for name, want in P4_INPUT_SHAS.items():
        p = PARKED4_DIR / f"input/{name}"
        if not p.is_file():
            sys_exit(f"parked4 kit input CSV missing: {name}")
        if sha(p) != want:
            sys_exit(f"parked4 kit input CSV sha drift: {name}")
        fields = p.read_text().strip().split(",")
        if len(fields) != 11 or fields[0] != "target" \
                or fields[1] != "0" or fields[2] != "5":
            sys_exit(f"parked4 kit input CSV row-spec drift: {name}")
    never_started_lo_hi = set()
    for name in ("batch-k20.input.csv", "batch-k33.input.csv"):
        fields = (PARKED4_DIR / f"input/{name}").read_text().strip().split(",")
        never_started_lo_hi.add(f"{fields[3]}:{fields[4]}")
    if never_started_lo_hi != set(PARKED_NEVER_STARTED_KEYS):
        sys_exit("parked4 never-started input CSV key drift (k20/k33)")
    # the val anchors replay the same target twice (2M then 15M): the two
    # val input CSVs per side must be byte-identical pairs
    if P4_INPUT_SHAS["val-at2m-first.input.csv"] != \
            P4_INPUT_SHAS["val-first-15m.input.csv"] \
            or P4_INPUT_SHAS["val-at2m-second.input.csv"] != \
            P4_INPUT_SHAS["val-second-15m.input.csv"]:
        sys_exit("parked4 val input pair drift")

    # parked4 raws: 15M park baseline + 50M two-pass + margin re-proof +
    # voluntary third verify, plus 4 validation-anchor replays, all
    # byte-pinned and payload-gated
    probe_rows = {}
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos = ADOPTED_KEY_PINS[kid]
        res, nodes = ADOPTED_LABEL_PINS[kid]
        base = f"{lo}-{hi}"
        raw_files = {
            "base15m": PARKED4_DIR / f"output/raw/base15m-{base}.out.csv",
            "run1": PARKED4_DIR / f"output/raw/l50m-run1-{base}.out.csv",
            "run2": PARKED4_DIR / f"output/raw/l50m-run2-{base}.out.csv",
            "run3": PARKED4_DIR / f"output/raw/l50m-run3-verify-{base}.out.csv",
            "margin": PARKED4_DIR / f"output/raw/l50m-margin-{base}.out.csv",
        }
        raw_names = {
            "base15m": f"base15m-{base}.out.csv",
            "run1": f"l50m-run1-{base}.out.csv",
            "run2": f"l50m-run2-{base}.out.csv",
            "run3": f"l50m-run3-verify-{base}.out.csv",
            "margin": f"l50m-margin-{base}.out.csv",
        }
        for tag, p in raw_files.items():
            if not p.is_file():
                sys_exit(f"parked4 raw missing: {p.name}")
            if sha(p) != P4_RAW_SHAS[raw_names[tag]]:
                sys_exit(f"parked4 raw sha drift ({tag}): {kid}")
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
        # the margin re-proof is a DIFFERENT budget by design (32M vs 50M):
        # node-exactness of (result, nodes, legal, key) is asserted in the
        # per-tag loop above; only the full payload (incl. budget) is not
        # required to match the 50M runs
        probe_rows[kid] = parsed["run1"]
    # validation anchors: honesty replays of pinned anchor keys
    for name, (legal_v, budget_v, res_v, nodes_v, lo_v, hi_v) in \
            P4_VAL_PINS.items():
        p = PARKED4_DIR / f"output/raw/{name}.out.csv"
        if not p.is_file():
            sys_exit(f"parked4 val raw missing: {name}")
        if sha(p) != P4_RAW_SHAS[f"{name}.out.csv"]:
            sys_exit(f"parked4 val raw sha drift: {name}")
        r = parse_replay(p)
        if (r["stones"], r["is_or"], r["legal"], r["budget"], r["result"],
                r["nodes"], r["lo"], r["hi"]) != \
                (5, 0, legal_v, budget_v, res_v, nodes_v, str(lo_v), str(hi_v)):
            sys_exit(f"parked4 val anchor replay drift: {name}")
    adopted_nodes = sum(ADOPTED_LABEL_PINS[kid][1] for kid in ADOPTED_IDS)
    if adopted_nodes != ADOPTED_NODES_TOTAL:
        sys_exit(f"adopted node total drift {adopted_nodes} "
                 f"!= {ADOPTED_NODES_TOTAL}")

    # --- Part SM pinned C++ second-implementation scrutiny gate kit ------
    if not SM_DIR.is_dir():
        sys_exit(f"Part SM kit dir missing {SM_DIR}")
    if sha(SM_DIR / "MANIFEST-sha256.txt") != SM_MANIFEST_SHA:
        sys_exit("Part SM kit MANIFEST sha drift")
    sm_manifest_shas = load_manifest_2field(SM_DIR / "MANIFEST-sha256.txt",
                                            "Part SM")
    if len(sm_manifest_shas) != SM_KIT_FILES:
        sys_exit(f"Part SM kit files verified {len(sm_manifest_shas)} "
                 f"!= {SM_KIT_FILES}")
    for rel, want in sm_manifest_shas.items():
        p = SM_DIR / rel
        if not p.is_file():
            sys_exit(f"Part SM kit file missing: {rel}")
        if sha(p) != want:
            sys_exit(f"Part SM kit file sha drift: {rel}")
    if sm_manifest_shas.get("README.md") != SM_README_SHA:
        sys_exit("Part SM kit README pin drift")
    for kid in ADOPTED_IDS:
        a = sm_manifest_shas.get(f"input/{kid}.input.csv")
        if a is None or a != P4_INPUT_SHAS[f"batch-{kid}.input.csv"]:
            sys_exit(f"{kid}: SM gate input CSV is not byte-equal to the "
                     "parked4 kit's batch input CSV (cross-registration)")
    if sha(SM_DIR / "input/gate-rows.json") != SM_GATEROWS_SHA:
        sys_exit("Part SM gate-rows.json sha drift")
    gr = json.loads((SM_DIR / "input/gate-rows.json").read_text())
    if gr["schema"] != "n11-sixthcost-parked4-cppgate-rows-v1":
        sys_exit("Part SM gate-rows schema drift")
    if gr["part"] != "SM":
        sys_exit("Part SM gate-rows part drift")
    gs = gr["gate_source"]
    if gs["path"] != "cpp/solvers/kyouen_dfpn_root.cpp" \
            or gs["sha256"] != SM_CPP_SHA or gs["commit"] != SM_CPP_COMMIT:
        sys_exit("Part SM gate-rows gate-source block drift")
    ch = gr["canonical_head"]
    if (ch["label"] != "16a12390" or ch["sha256"] != BASE_CACHE_SHA_EXPECTED
            or ch["rows"] != BASE_CACHE_ROWS_EXPECTED
            or ch["census"] != {"WIN": BASE_CACHE_WIN_EXPECTED,
                                "LOSS": BASE_CACHE_LOSS_EXPECTED}
            or ch["targets_fresh_vs"] != "16a12390"):
        sys_exit("Part SM gate-rows canonical-head block drift")
    if len(gr["gates"]) != SM_GATES_TOTAL or any(
            v["status"] != "PASS" for v in gr["gates"].values()):
        sys_exit("Part SM gate-rows 66-gate table not all PASS")
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos = ADOPTED_KEY_PINS[kid]
        res, nodes = ADOPTED_LABEL_PINS[kid]
        t = gr["targets"][kid]
        if (t["key_lo"], t["key_hi"], t["budget"], t["expected"]) != \
                (str(lo), str(hi), str(L50M_BUDGET),
                 f"{legal},{L50M_BUDGET},{res},{nodes}"):
            sys_exit(f"Part SM gate-rows target drift: {kid}")
        if t["input_sha256"] != P4_INPUT_SHAS[f"batch-{kid}.input.csv"]:
            sys_exit(f"Part SM gate-rows input pin drift: {kid}")
        base = f"{lo}-{hi}"
        if t["raw_p1_sha256"] != P4_RAW_SHAS[f"l50m-run1-{base}.out.csv"] \
                or t["raw_p2_sha256"] != P4_RAW_SHAS[f"l50m-run2-{base}.out.csv"] \
                or t["run3_verify_sha256"] != \
                P4_RAW_SHAS[f"l50m-run3-verify-{base}.out.csv"] \
                or t["margin_sha256"] != P4_RAW_SHAS[f"l50m-margin-{base}.out.csv"]:
            sys_exit(f"Part SM gate-rows raw pin cross-registration drift: {kid}")
        if t["third_impl_verdict_level_corroboration"] is not True:
            sys_exit(f"Part SM gate-rows corroboration flag drift: {kid}")
        if t["row_spec"] != f"target,0,5,{lo},{hi},{legal},0,0,0,0,0":
            sys_exit(f"Part SM gate-rows row spec drift: {kid}")
    if sha(SM_DIR / "output/gate-status.log") != SM_STATUS_SHA:
        sys_exit("Part SM gate-status.log sha drift")
    gk_map = {}
    for line in (SM_DIR / "output/gate-status.log").read_text().splitlines():
        parts = line.split()
        if len(parts) < 4 or " ".join(parts[2:3]) != "GATE-PASS" \
                or not parts[3].replace(",", "").isdigit():
            sys_exit(f"Part SM gate-status unexpected line: {line}")
        gk_map[parts[1]] = parts[3]
    if len(gk_map) != 5:
        sys_exit("Part SM gate-status must carry exactly 5 GATE-PASS rows")
    for name, (legal_v, budget_v, res_v, nodes_v) in SM_ANCHOR_PINS.items():
        if gk_map.get(name) != f"{legal_v},{budget_v},{res_v},{nodes_v}":
            sys_exit(f"Part SM gate-status anchor row drift: {name}")
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos = ADOPTED_KEY_PINS[kid]
        res, nodes = ADOPTED_LABEL_PINS[kid]
        if gk_map.get(kid) != f"{legal},{L50M_BUDGET},{res},{nodes}":
            sys_exit(f"Part SM gate-status row drift: {kid}")
    for rel in ("output/audit_gate.json", "output/audit_gate.run1.json",
                "output/audit_gate.run2.json", "output/audit_gate.run3.json"):
        if sm_manifest_shas.get(rel) != SM_AUDIT_SHA:
            sys_exit(f"Part SM audit json sha drift: {rel}")
    ag = json.loads((SM_DIR / "output/audit_gate.json").read_text())
    if ag["overall"] != "PASS" or ag["part"] != "SM":
        sys_exit("Part SM audit_gate.json overall/part drift")
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos = ADOPTED_KEY_PINS[kid]
        res, nodes = ADOPTED_LABEL_PINS[kid]
        row = ag["rows"].get(kid)
        if row is None or row["expected"] != f"{legal},{L50M_BUDGET},{res},{nodes}" \
                or row["observed_p1"] != row["expected"] \
                or row["budget"] != str(L50M_BUDGET):
            sys_exit(f"Part SM audit_gate row drift: {kid}")
    for name, (legal_v, budget_v, res_v, nodes_v) in SM_ANCHOR_PINS.items():
        row = ag["rows"].get(name)
        if row is None or row["expected"] != f"{legal_v},{budget_v},{res_v},{nodes_v}" \
                or row["observed_p1"] != row["expected"]:
            sys_exit(f"Part SM audit_gate anchor row drift: {name}")
    # SM raw payload gate (bytes already MANIFEST-verified; payload here)
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos = ADOPTED_KEY_PINS[kid]
        res, nodes = ADOPTED_LABEL_PINS[kid]
        s1 = parse_replay(SM_DIR / f"output/raw/{kid}.p1.out")
        s2 = parse_replay(SM_DIR / f"output/raw/{kid}.p2.out")
        payload_eq(s1, s2, f"SM {kid}")
        if (s1["stones"], s1["is_or"], s1["budget"], s1["result"],
                s1["nodes"]) != (5, 0, L50M_BUDGET, res, nodes):
            sys_exit(f"{kid}: SM C++ gate honest-label drift")
        if s1["legal"] != legal or s1["lo"] != str(lo) or s1["hi"] != str(hi):
            sys_exit(f"{kid}: SM C++ gate legal/key drift")
    for name, (legal_v, budget_v, res_v, nodes_v) in SM_ANCHOR_PINS.items():
        a1 = parse_replay(SM_DIR / f"output/raw/{name}.p1.out")
        a2 = parse_replay(SM_DIR / f"output/raw/{name}.p2.out")
        payload_eq(a1, a2, f"SM {name}")
        if (a1["stones"], a1["is_or"], a1["legal"], a1["budget"], a1["result"],
                a1["nodes"]) != (5, 0, legal_v, budget_v, res_v, nodes_v):
            sys_exit(f"{name}: SM C++ gate anchor-label drift")

    # --- Part SL third-implementation batch audit (pinned summary) -------
    if not SL_DIR.is_dir():
        sys_exit(f"SL kit dir missing {SL_DIR}")
    slp = SL_DIR / SL_SUMMARY_REL
    if sha(slp) != SL_SUMMARY_SHA:
        sys_exit("Part SL batch audit summary sha drift")
    a = json.loads(slp.read_text())
    if a["schema"] != "n11-sixthcost-k09k43-thirdimpl-batch-audit-v2":
        sys_exit("Part SL batch audit schema drift")
    if a["all_pass"] is not True or a["consumed"] is not False:
        sys_exit("Part SL batch audit all_pass/consumed drift")
    if a["rows_audited"] != SL_ROWS_AUDITED \
            or a["rows_expected"] != SL_ROWS_AUDITED:
        sys_exit("Part SL batch audit row accounting drift")
    if "remain UNKNOWN" not in a["claim"]:
        sys_exit("Part SL batch audit UNKNOWN-guard drift")
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos = ADOPTED_KEY_PINS[kid]
        res, nodes = ADOPTED_LABEL_PINS[kid]
        pins = SL_ROW_PINS[kid]
        rr = a["row_results"].get(kid)
        if rr is None:
            sys_exit(f"Part SL row_results missing: {kid}")
        if (rr["key"] != f"{lo}:{hi}" or rr["legal"] != legal
                or rr["replica_stage"] != "win"
                or rr["replica_verdict"] != 1 or rr["replica_resolution_nodes"] != nodes
                or rr["third_impl_verdict"] != 1
                or rr["third_impl_expansions"] != pins["expansions"]
                or rr["third_impl_tt_hits"] != pins["tt_hits"]
                or rr["third_impl_runs"] != 3
                or rr["determinism_identical"] is not True
                or rr["verdict_level_agreement"] is not True):
            sys_exit(f"Part SL row_results drift: {kid}")
    gates = a["gates"]
    for kid in ADOPTED_IDS:
        res, nodes = ADOPTED_LABEL_PINS[kid]
        pins = SL_ROW_PINS[kid]
        det = gates.get(f"C2_{kid}_determinism_3runs_identical")
        det_pin = (f"[('1', '{pins['expansions']}', '{pins['tt_hits']}'), "
                   f"('1', '{pins['expansions']}', '{pins['tt_hits']}'), "
                   f"('1', '{pins['expansions']}', '{pins['tt_hits']}')]")
        if det is None or det.get("pass") is not True \
                or det["detail"] != det_pin:
            sys_exit(f"Part SL determinism triplet drift: {kid}")
        una = gates.get(f"repl_{kid}_win_4runs_unanimous")
        una_pin = f"[('1', '{nodes}'), ('1', '{nodes}'), ('1', '{nodes}'), ('1', '{nodes}')]"
        if una is None or una.get("pass") is not True \
                or una["detail"] != una_pin:
            sys_exit(f"Part SL replica unanimity drift: {kid}")
        park = gates.get(f"repl_{kid}_base15m_parked_unknown")
        if park is None or park.get("pass") is not True \
                or park["detail"] != "[('0', '15000000')]":
            sys_exit(f"Part SL park-baseline drift: {kid}")
        agree = gates.get(f"C2_{kid}_win_verdict_level_vs_replica")
        if agree is None or agree.get("pass") is not True \
                or agree["detail"] != "third=['1'] replica=1":
            sys_exit(f"Part SL verdict-level agreement gate drift: {kid}")
        diff = gates.get(f"C2_{kid}_expansions_differ_from_replica_nodes_allowed")
        if diff is None or diff.get("pass") is not True:
            sys_exit(f"Part SL expansions-differ note gate drift: {kid}")
        tto = gates.get(f"C2_{kid}_ttoverwrites_pinned")
        if tto is None or tto.get("pass") is not True \
                or tto["detail"] != f"ttOverwrites={pins['ttoverwrites']}":
            sys_exit(f"Part SL tt-overwrites pin drift: {kid}")
        lo, hi, legal, _s5, _pos = ADOPTED_KEY_PINS[kid]
        base = f"{lo}-{hi}"
        for stage, (budget_v, res_v, nodes_v) in (
                ("base15m", (PARK_BUDGET, 0, PARK_BUDGET)),
                ("l50m-run1", (L50M_BUDGET, res, nodes)),
                ("l50m-run2", (L50M_BUDGET, res, nodes)),
                ("l50m-run3-verify", (L50M_BUDGET, res, nodes)),
                ("l50m-margin", (MARGIN_BUDGET, res, nodes))):
            gn = f"repl_row_{kid}_{stage}-{base}.out.csv"
            rowgate = gates.get(gn)
            if rowgate is None or rowgate.get("pass") is not True:
                sys_exit(f"Part SL replica raw pin gate missing: {kid} {gn}")
            fields = [x.strip() for x in rowgate["detail"]
                      .replace("|", ",").split(",") if x.strip()]
            if len(fields) != 11 or fields[0] != "replay":
                sys_exit(f"Part SL replica raw row malformed: {kid} {gn}")
            if (int(fields[2]), int(fields[3]), int(fields[4]), int(fields[5]),
                    int(fields[6]), int(fields[7]), fields[9], fields[10]) != \
                    (5, legal, 0, budget_v, res_v, nodes_v, str(lo), str(hi)):
                sys_exit(f"Part SL replica raw row payload drift: {kid} {gn}")
        # cold a/b/v third-impl witness rows (verdict-level WIN agreement)
        witness_rows = 0
        for wname in (f"{kid}-cold-a.txt", f"{kid}-cold-b.txt",
                      f"{kid}-cold-v-legal.txt"):
            tk = gates.get(f"third_key_{kid}_{wname}")
            if tk is None or tk.get("pass") is not True:
                sys_exit(f"Part SL third_key witness gate missing: {kid} {wname}")
            fields = [x.strip() for x in tk["detail"].split("|")]
            if len(fields) != 15 or fields[0] != "third" \
                    or int(fields[2]) != 5 or int(fields[3]) != legal \
                    or int(fields[4]) != legal or int(fields[5]) != 1 \
                    or int(fields[6]) != pins["expansions"] \
                    or int(fields[7]) != pins["tt_hits"] \
                    or fields[9] != str(lo) or fields[10] != str(hi) \
                    or fields[11] != "clean" \
                    or fields[13] != f"ttOverwrites={pins['ttoverwrites']}" \
                    or fields[14] != "memoPower=22" \
                    or fields[12] != "quads=95670":
                sys_exit(f"Part SL third_key witness row drift: {kid} {wname}")
            witness_rows += 1
        if witness_rows != 3:
            sys_exit(f"{kid} needs exactly 3 cold third-impl witness runs")
        # fail-closed negative battery (documented in the same summary)
        for gn in (f"C4_ng1_{kid}_legal96_gate_fail",
                   f"C4_ng2_{kid}_stones6_gate_fail"):
            ng = gates.get(gn)
            if ng is None or ng.get("pass") is not True:
                sys_exit(f"Part SL negative gate drift: {kid} {gn}")

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
    if (merged_rows, merged_wins, merged_loss) != (6799, 199, 6600):
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
            or ma["unique_rows"] != 6799 \
            or ma["duplicate_rows_elided"] != 0 \
            or ma["verdict_counts"] != {"WIN(1)": 199, "LOSS(2)": 6600} \
            or ma["nodes_field_mismatches_recorded"] != [] \
            or [inp["sha256"] for inp in ma["inputs"]] != \
            [BASE_CACHE_SHA_EXPECTED, ADOPTED_INCREMENT_SHA]:
        sys_exit("merge-audit record field drift")
    if ma["inputs"][0]["rows"] != 6797 or ma["inputs"][1]["rows"] != 2 \
            or ma["inputs"][0]["unique_new"] != 6797 \
            or ma["inputs"][1]["unique_new"] != 2:
        sys_exit("merge-audit input accounting drift")
    if "11x11 root questions remain UNKNOWN" not in ma["interpretation_guard"]:
        sys_exit("merge-audit interpretation guard drift")

    # --- emit increment + manifest ----------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    rowlines = [f"s5verdict,{r[0]},{r[1]},5,1,{r[2]}"
                for r in sorted((lo, hi, nodes)
                                 for lo, hi, legal, result, nodes, _s5, _cls,
                                 _own in adopted_rows)]
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
        "schema": SIXTHWIN2_SCHEMA,
        "part": "SP",
        "date": "2026-11-26",
        "win_canonical_adoption": True,
        "canonical_head_published_by_this_part": {
            "merged_cache_name": MERGED_NAME,
            "merged_cache_sha256": MERGED_SHA_EXPECTED,
            "merged_cache_bytes": MERGED_BYTES_EXPECTED,
            "merged_cache_rows": 6799,
            "merged_cache_win_loss": [199, 6600],
            "merge_audit_runs": 3,
            "merge_audit_sha256_x3_identical": MERGE_AUDIT_SHA_EXPECTED,
            "merger": "pinned byte-clone of the published union merger "
                      "(sha256 90711961..., this kit scripts/s5_union_merge.py)",
            "note": "no pre-declaration dossier exists for sixthwin2 "
                    "(unlike EW's sixthwin5); this Part SP publishes the "
                    "merged head of record itself at this kit's output/ "
                    "directory; three independent merge runs produced "
                    "byte-identical output and byte-identical audit records",
        },
        "source_class": {
            "class": f"{CLASS_MASK[0]}:{CLASS_MASK[1]}",
            "class_children_total": 108, "s5_unknown_before": 101,
            "unknown_exclusive": 43, "serving_class_index": SERVING_CLASS,
            "note": "the sixth-cost live candidate class (s4 class 3077, "
                    "coverage {80,84,100,108}); k13/k19 are positions 13/19 "
                    "of the same published probe selection exclusive_probe_"
                    "order of record (d5e9b059...), resolved by the parked4 "
                    "L50M ladder over their pinned 15,000,000 "
                    "park-at-UNKNOWN baselines",
            "adoption_requirement_of_record":
                "the parked4 halt-audit's pre-registered WIN-row "
                "requirement: published C++ second-implementation "
                "verification of the replica raw rows (pinned "
                "cpp/solvers/kyouen_dfpn_root.cpp sha256 9193f5b6...); "
                "satisfied for both rows by the Part SM kit (GATE-PASS); "
                "any C++ disagreement fails closed in favor of discarding "
                "the row; third-implementation verdict-level corroboration "
                "(Part SL batch audit) is additionally recorded for both "
                "rows per the repo's sixthwin5 adoption pattern",
        },
        "pools": [
            {"pool": "parked4-l50m-ladder",
             "kit": PARKED4_EXP,
             "budget": L50M_BUDGET,
             "park_budget": PARK_BUDGET,
             "margin_budget": MARGIN_BUDGET,
             "adopted_win_ids": list(ADOPTED_IDS),
             "standing_unconsumed_keys_not_adopted": {
                 "k20": "10376293541461626880:33619968 (never started by "
                        "this lane; resolved WIN(1) at 50M by the "
                        "parked4rest2 ladder - outside this Part; "
                        "third-implementation corroboration absent at SP "
                        "build time; C++ gate kit Part SN in flight - "
                        "disclosed)",
                 "k33": "12682136550675320832:65536 (same standing status "
                        "as k20)",
             },
             "adopted_nodes": ADOPTED_NODES_TOTAL,
             "kit_integrity": {
                 "note": "the parked4 ladder kit holds no MANIFEST-sha256; "
                         "every consumed byte is pinned directly in this "
                         "manifest: README, jsreplay.js, halt-audit.json, "
                         "status.log, the 8 input CSVs (batch-k13/k19/k20/"
                         "k33 and the 4 validation anchors) and all 14 raw "
                         "CSV files (raw_file_sha256_pins / "
                         "input_csv_sha256_pins below)",
                 "readme_sha256": P4_README_SHA,
                 "jsreplay_sha256": P4_JSREPLAY_SHA,
                 "halt_audit_sha256": P4_HALTAUDIT_SHA,
                 "halt_audit_pins": {
                     "gates_passed_count": 77,
                     "halted_on_win_keys": adopted_key_strs,
                     "lane_time_base_chain_sha256": "6e49dd84...",
                     "lane_time_base_note": "the halt-audit pins the "
                         "lane-time canonical head 6e49dd84 (pre-EW); the "
                         "lane's if-adopted prediction was computed against "
                         "that older head and is superseded by this Part's "
                         "census measurement against the current 16a12390 "
                         "head (Part EW already flipped serving class 3077; "
                         "the full recount measures the flip set exactly "
                         "{2624, 30136})",
                 },
                 "status_log_sha256": P4_STATUS_SHA,
                 "input_csv_sha256_pins": P4_INPUT_SHAS,
                 "raw_file_sha256_pins": P4_RAW_SHAS,
                 "validation_anchor_replays": {k: list(v) for k, v in
                                                P4_VAL_PINS.items()},
                 "input_csv_cross_registration":
                     "batch-k13/batch-k19 are byte-equal to the Part SM "
                     "kit's MANIFEST-pinned gate inputs; the val anchors "
                     "are byte-equal to the Part SM kit's pinned "
                     "anchor-at2m input family",
             }},
            {"pool": "sm-cpp-second-implementation-gate",
             "kit": SM_EXP,
             "kit_integrity": {
                 "note": "Part SM kit verified file-by-file against its "
                         f"published MANIFEST-sha256 {SM_MANIFEST_SHA[:8]}... "
                         f"({SM_KIT_FILES} files)",
                 "kit_manifest_sha256": SM_MANIFEST_SHA,
                 "kit_files_verified": SM_KIT_FILES,
                 "readme_sha256": SM_README_SHA,
                 "gate_rows_json_sha256": SM_GATEROWS_SHA,
                 "gate_rows_all_pass": SM_GATES_TOTAL,
                 "gate_status_log_sha256": SM_STATUS_SHA,
                 "gate_status_gate_pass_rows": 5,
                 "audit_gate_json_sha256": SM_AUDIT_SHA,
                 "audit_run1_run2_run3_sha256_identical": SM_AUDIT_SHA,
                 "cpp_solver_sha256": SM_CPP_SHA,
                 "cpp_solver_commit": SM_CPP_COMMIT,
             },
             "canonical_head_cross_gate":
                 "the SM gate-rows.json canonical_head block pins this "
                 "Part's BASE (16a12390, 6,797 rows, WIN 197 / LOSS 6600) "
                 "and records the 2 adopted targets as fresh versus exactly "
                 "that head, with raw/margin/run3 sha cross-registration "
                 "to the parked4 ladder raws (gated here)"},
            {"pool": "sl-third-implementation-batch",
             "kit": SL_EXP,
             "covered_ids": list(ADOPTED_IDS),
             "kit_integrity": {
                 "note": "Part SL batch audit summary pinned directly "
                         "(same published kit as the TI-era audits); "
                         "k13/k19 row_results, determinism triplets, "
                         "replica 4-run unanimity, park-baseline replica "
                         "rows, cold a/b/v witness rows, tt-overwrites and "
                         "the fail-closed negative battery (legal96/"
                         "stones6 GATE_FAIL) all field-gated here",
                 "summary_path": SL_SUMMARY_REL,
                 "summary_sha256": SL_SUMMARY_SHA,
                 "rows_audited": SL_ROWS_AUDITED,
                 "row_pins": SL_ROW_PINS,
             },
             "verdict_agreement_note":
                 "third-impl WIN(1) verdict-level agreement for k13/k19 "
                 "with 3 identical cold runs each (expansions 19,433,195 / "
                 "17,955,947, tt-hits 10,181,270 / 9,504,863, tt-overwrites "
                 "15,238,891 / 13,761,643); expansions legitimately differ "
                 "from replica node counts (different implementations); "
                 "the summary's replica raw rows are payload-equal to the "
                 "parked4 ladder raws",
             "standing_unconsumed_loss_rows":
                 "the 30 fifth-resumption verified LOSS rows of the same "
                 "batch are NOT adopted and NOT emitted by this Part; "
                 "they remain unconsumed honest LOSS labels"},
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
            "standing_unconsumed_parked4rest2_win_rows": 2,
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
            "Part SP canonical WIN-only adoption increment: the 2 fresh "
            "exact-WIN rows (each cold two-pass node-exact at 50M over the "
            "pinned 15M park-at-UNKNOWN baseline, plus a 32M budget-margin "
            "re-proof and a voluntary third cold 50M verify run, solved "
            "within budget, C++-gated by Part SM and third-implementation-"
            "corroborated by the Part SL batch) are consumed into the "
            "canonical chain via the fail-closed union merger whose output "
            "this Part publishes as the merged head of record (cc3694bb..., "
            "6,799 rows WIN 199 / LOSS 6,600); WIN-only adoption asserts "
            "no root verdict and frees no class; owner classes of the "
            "adopted keys are excluded_now by the win-hit mechanism, "
            "derived machine-only by the reaudit refresh (flip set exactly "
            "{2624, 30136}; serving class 3077 stays excluded_now since "
            "Part EW with cost-unknown 95 -> 93); nodes are bookkeeping, "
            "never verdicts; the standard 11x11 empty board and every "
            "central-reply root stay UNKNOWN",
        "provenance": {
            "part_maker_reverified_live": True,
            "merged_cache_published_by_this_part": True,
            "parked4_kit_direct_pins": True,
            "sm_kit_files_verified": SM_KIT_FILES,
            "sl_summary_sha_pinned": True,
            "probe_kit_direct_pins": True,
            "raws_published": True,
        },
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "part": "SP",
        "head_of_record": "16a12390... -> cc3694bb... (6,799 rows "
                          "WIN 199 / LOSS 6,600)",
        "increment_sha256": incr_sha,
        "rows": len(rowlines),
        "adopted_nodes_total": ADOPTED_NODES_TOTAL,
        "digest": digest,
        "manifest_sha256": hashlib.sha256(
            (OUT / "increments-manifest.json").read_bytes()).hexdigest(),
    }))


if __name__ == "__main__":
    main()
