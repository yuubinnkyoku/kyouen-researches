#!/usr/bin/env python3
"""Build the Part ST sixthloss30 (30 unconsumed fifth-resumption resolved
LOSS rows) canonical LOSS-adoption increment, fail-closed.

Part ST kit n11-centralreply-sixthloss30-adoption-reaudit-20261126
(2026-11-26).  This IS the adoption Part declared emission: the canonical
head of record advances from merged-exact-s5-chain-plus-sixthwin3 (sha256
02db5ab3..., 6,801 rows WIN 201 / LOSS 6,600; the Part SQ adoption head
of record) to merged-exact-s5-chain-plus-sixthloss30 (sha256 dade15780..., 6,831
rows WIN 201 / LOSS 6,630) by consuming exactly the 30 unconsumed
fifth-resumption resolved exact-LOSS rows of the sixth-cost class
10376293541461626880:65536 probe selection (k09..k43 minus the adopted
k13/k19/k20/k33 and the still-parked k38; exclusive_probe_order positions
9..43 minus 13/19/20/33/38).  The verdict scope of the Part is exactly
those 30 LOSS rows: NO root verdict, NO 11x11 outcome, NO class freed,
NO class excluded (loss-only adoption flips no status; the Part EM
precedent).

Structural clone of the published Part SQ maker
make_increments_sixthwin3_adoption.py (sha256 1a5f9b03...): the
computation region (source-kit byte gates, multi-pass payload gates,
gate-kit MANIFEST verification, third-impl gates, freshness/quarantine/
canonical-safety gates, adopted-table digest, self-publication gates,
increment emit) is identical logic; the disclosed diff regions are the
docstring, the source pools (the probe kit's published fifth-resumption
raws replace the parked4rest2 ladder; the Part SR C++ gate kit replaces
the Part SN kit; the k09..k43 resolved-32 third-impl addendum replaces
the k20/k33 addendum), the LOSS direction of the adopted rows, the
emitted increment header block, the output file names and the manifest
fields.

Each adopted row is gated at FOUR independent implementations, all
re-verified here byte-for-byte or field-for-field:

1. the probe kit's published fifth-resumption raws
   (n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121,
   direct sha pins): per key the 2,000,000 park-at-UNKNOWN baseline (26
   keys) or 2M-stage LOSS resolution with an at2m determinism pair
   (k17/k18/k28/k32) PLUS the primary cold two-pass node-exact resolution
   pair at 15,000,000 (28 keys; k28/k32 resolve at the 2,000,000 stage),
   every stage payload-gated against the pinned key/legal/budget/result/
   nodes table;
2. the published Part SR pinned C++ second-implementation scrutiny gate
   kit n11-sixthcost-fifthres30-cppgate-20261126 (MANIFEST-verified
   file-by-file, 112/112): GATE-PASS for every row (33/33 rows incl. 3
   anchors) with 2-pass determinism and published-raw node-exact (the
   parent batch's pre-registered consumption gate: any C++ disagreement
   fails closed in favor of discarding the row; sha-pinned C++ solver
   9193f5b6...); the kit's own audit_gate.py is re-run LIVE here
   (rc=0, PASS) and its tamper battery log is byte-gated;
3. the k09..k43 resolved-32 third-implementation verdict re-verification
   addendum (published inside the k01-k03 third-impl kit; auditor
   audit_k09k43.py re-run LIVE here twice, 850/850 gates): verdict-level
   LOSS(2) agreement per key, 2 identical cold runs each (expansions
   legitimately differ from replica node counts - different
   implementations), per-row replica-raw copies byte-equal to the probe
   kit raws (cross-registration gated);
4. the probe kit's published selection JSON (d5e9b059...): the 30 keys
   are exactly the exclusive_probe_order entries at their pinned
   positions of the same sixth-cost class selection of record.

The 30 adopted (lo,hi) pairs are proven absent from BASE (fresh-increment
gate), absent from the active quarantine registry and canonical-safe per
s5_evidence_policy; the adopted-table digest and the emitted increment
sha are self-pinned; this Part additionally re-verifies the published
merged head of record byte-for-byte (dade15780..., 6,831 rows) and its
three byte-identical merge audit records (84993a62...).  The standing
unconsumed row is recorded but NOT adopted and NOT emitted: the
still-parked key k38 of the same probe selection (first-implementation
L50M cold-pair LOSS row plus Part SS C++ GATE-PASS but NO
third-implementation corroboration - the coverage asymmetry the Part SS
completion log records).  This Part adopts no WIN row and no k38 row.

LOSS-only adoption asserts no root verdict, frees no class and excludes
no class (zero status flips measured; the Part EM precedent); the
serving class 3077 keeps its excluded_now status with cost-unknown 91
-> 61, and all scheduling effects are those derived by the reaudit
refresh (Board fail-closed child verification) and the census delta
measurer.  The standard 11x11 empty board and every central-reply root
stay UNKNOWN; nodes are bookkeeping, never verdicts.
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

SQ_EXP = "n11-centralreply-sixthwin3-adoption-reaudit-20261126"
PROBE_EXP = "n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121"
SR_EXP = "n11-sixthcost-fifthres30-cppgate-20261126"
TI_EXP = ("n11-sixthcost-k01-k03-thirdimpl-verdict-"
          "reverification-20261122")

BASE_CACHE = ROOT / "research/experiments" / SQ_EXP / (
    "output/merged-exact-s5-chain-plus-sixthwin3-20261126.cache")
PROBE_DIR = ROOT / "research/experiments" / PROBE_EXP
SR_DIR = ROOT / "research/experiments" / SR_EXP
TI_DIR = ROOT / "research/experiments" / TI_EXP
GRAPH = (ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"
         "/output/dependency-graph.json.gz")
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
POLICY = (ROOT / "research/experiments/n11-frontier-selection-20261005"
          "/scripts/s5_evidence_policy.py")

MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA_EXPECTED = "02db5ab35b8ad71dfd0699217756291c6bc896c78e9fd7c609b5e25177f6b25c"
BASE_CACHE_ROWS_EXPECTED = 6801
BASE_CACHE_WIN_EXPECTED = 201
BASE_CACHE_LOSS_EXPECTED = 6600
QUARANTINE_SHA_EXPECTED = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
POLICY_SHA_EXPECTED = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
GRAPH_SHA_EXPECTED = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"

PROBE_SELECTION_SHA = "d5e9b059611849f7b7e69c7370a0e66cd7535c43b3a043ce9f5bfc0e5ff72e87"

# --- Part SR pinned C++ second-implementation scrutiny gate kit -------
SR_MANIFEST_SHA = "374fa85cac3c30884c53e5ae6092c6148b20fb2852cd4d6f67c622246467db65"
SR_KIT_FILES = 112
SR_README_SHA = "1e07d3e9ae057bb63471a76ded66ab11051c9319556071ec368ab68dd69c9ec2"
SR_GATEROWS_SHA = "662502671ff478d61505038126f6928bd57126ca767cc18d658139796dfeaad2"
SR_STATUS_SHA = "57807343045a0805af89cdff134621202f519f36c59e1ac4708ce470bb39982e"
SR_AUDIT_SHA = "44358ce2b4dadfaad6ada4df60ef84f57d904eca4344685c34a0c2b7f7561352"
SR_GATES_TOTAL = 231
SR_GATE_STATUS_ROWS = 33
SR_AUDIT_PY_SHA = "e8a139a7e4b0c87e1d354b38bcd3f8487dabfc42da3f159f2c01e558f303c625"
SR_TAMPER_SHA = "2d3cb400d8449c6c7657b642c8f49defb3277c9cf057dd215c40b31cf66fbaad"
SR_T1_RESULT_SHA = "3b8c2b2639bd50e0aab53a0adbeaebabcc2a5f4990762d194d21dea8457074ac"
SR_CPP_SHA = "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e"
SR_CPP_COMMIT = "154f3b7a67b97e13acbaee8b04dc74ddca728d19"
SR_HEADER_PINS = {'kyouen_residual_micro.hpp': '5976935dcfccb9b5a26fa68f8de20868ce45363dd8c372dcd67d9b841167e7f5', 'n11_s5_quarantine.hpp': '2e36d69481fafcde7aede8ae4fedf3d5477f91ee9846bcd4ae2975f32a4ba1a5'}
SR_CANONICAL_HEAD = {'LOSS': 6600, 'WIN': 201, 'label': '02db5ab3', 'path': 'research/experiments/n11-centralreply-sixthwin3-adoption-reaudit-20261126/output/merged-exact-s5-chain-plus-sixthwin3-20261126.cache', 'rows': 6801, 'sha256': '02db5ab35b8ad71dfd0699217756291c6bc896c78e9fd7c609b5e25177f6b25c', 'targets_fresh_vs': '02db5ab3'}
SR_ANCHORS_RUNTIME = {'anchor-af039': ['30000000', '89,30000000,2,19234232'], 'anchor-aj001': ['30000000', '84,30000000,2,5156075'], 'anchor-at2m': ['2000000', '98,2000000,0,2000000']}
SR_THIRD_IMPL_BLOCK = {'all_pass': True, 'exists': True, 'rows_audited': 32, 'schema': 'n11-sixthcost-k09k43-thirdimpl-batch-audit-v2', 'source': 'research/experiments/n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122/out/audit-k09k43-summary.json', 'verdict_level_corroboration': True}
SR_ANCHOR_PINS = {
    "anchor-at2m": (98, 2000000, 0, 2000000),
    "anchor-aj001": (84, 30000000, 2, 5156075),
    "anchor-af039": (89, 30000000, 2, 19234232),
}

# --- k09..k43 resolved-32 third-implementation addendum ---------------
TI_AUDITOR_SHA = "978dd2c714bc45e03a2dc34cf52b24b9eb82e7d8c505dc7b0a52f862a830cc4e"
TI_THIRD_IMPL_SHA = "08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998"
TI_VERIFY_TBL_SHA = "c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251"
TI_SUMMARY_SHA = "300c8c0a61e4e5fe5fb1a8a5a1fe32aaebd391ec767dc2783f3b87cfd943728e"
TI_TAMPER_LOG_SHA = "1786e82609636c9751f90d92c4a9106422ad41490b1bb1f6ce23a32968559646"
TI_NEG_SHAS = {'neg-gate-k09-legal88.txt': 'cb5be18779dcb6c7ba65e674756193d13a6564a000de6c52ed1f4518c2ec65d4', 'neg-gate-k09-stones6.txt': '2f74943e77a8a83e272fef6e92f4b3dc02b40e860a2c4f8b625b8e0f5ff753d5', 'neg-gate-k10-legal85.txt': 'cd3e1335def9fc9cdee60f97ce7b31164be5b78e9657508af70efa52413b122a', 'neg-gate-k10-stones6.txt': 'd0a95734859a27867c7e5c1188794235b4a1ce7998890a93aeee39c5fdf71ae2', 'neg-gate-k11-legal87.txt': 'c343a33578d0f347ff37c77e94bd84cb34e53037e00ecd5256c7094e3cf334b4', 'neg-gate-k11-stones6.txt': '2604ff5b05338ddb2dc8d819f81138029b30fbb5376b2f0eff1b5af499f319b5', 'neg-gate-k12-legal84.txt': 'cf35f01e044ec4492aa2fccc0142626f41cdfa1d6ca005a99aa293331dda75f5', 'neg-gate-k12-stones6.txt': '037a0ef9dd9208ac4f8960180e0275b75ac29595dd05d43c0930fbcc0b6e9a03', 'neg-gate-k14-legal100.txt': 'e2ec66d4550a74d3f9954ab59a40e422e99a8aedde5fbdf856a2517a9c76938c', 'neg-gate-k14-stones6.txt': 'c77c74e5e615001e72681e52c61828b27d1ed734b4cd79121fc78cb29770036e', 'neg-gate-k15-legal100.txt': '40839a6a9c298648bc88394fbbbcf606f23329a1402ce4d2ad6928b05d047fbe', 'neg-gate-k15-stones6.txt': '15e4108a00547d8a66cd5d36eef900970b22250172e1e46d88ba162ac16c9ede', 'neg-gate-k16-legal96.txt': '80191ceb7a8437d0b1b3c94b4366d18c880852ed041f53874a46b54a15a7f1df', 'neg-gate-k16-stones6.txt': 'bf26d4845357e995709f8746ef0a1af3e9ea80b5d8d8e92085ca0c3888c56246', 'neg-gate-k17-legal97.txt': '5aa2694589c7991c434d1313a47677b62bdb0f159afc4ce9ef278c36f9ab0d68', 'neg-gate-k17-stones6.txt': '02a4b3e67ba8f2569f8bb3aa4fe8397138c21efc5c9becd97fbc837a23d58eb8', 'neg-gate-k18-legal92.txt': 'dae07082b796f4cca32b25592988f5f85ea25229f90daa20105be1d9df36afe3', 'neg-gate-k18-stones6.txt': 'b1992af390d21984189281db1a40a1879c35f57f3c099bceacae8c94cb3ef1cf', 'neg-gate-k21-legal91.txt': 'd3f9f9556aeddabc52984f2e1f837aabbaf9f5eeb586f0e85e4c1de426cf927b', 'neg-gate-k21-stones6.txt': '261538936278c0e388843be9cb1c6cd2b1ca2194b07dfb4e4228eee17036cdc1', 'neg-gate-k22-legal99.txt': '5dc59b768981fb79e02290ef2ccc280224de407c3ffca0cba18ac5727a033129', 'neg-gate-k22-stones6.txt': 'f57163df24f640ebf55b2dd890a346d1171ec6cd9a951be08aec8101e95088b8', 'neg-gate-k23-legal98.txt': 'f303c96ef6343d8a6ec0a104ac3f180eb148f7bc1856b75bbcd25ab18930092a', 'neg-gate-k23-stones6.txt': 'cca451100a376c3e62b35975f438de317a2ce615a36941301e1484c12d8f11c6', 'neg-gate-k24-legal94.txt': '58aaf5e2b40ef490605271865279fc31738f53991fb6b5955c2fd66836211691', 'neg-gate-k24-stones6.txt': 'bf57e3f637ea82a03dcebc445947e2142c65a83ec23107e852ae00d3a26bd99c', 'neg-gate-k25-legal92.txt': '12c7088926d945060da98a5207f6ece6f6527e41a821e4e3a39c357b01f72181', 'neg-gate-k25-stones6.txt': '68d59803282cf58dc028c0e597c621de1f009b2d1a48ac1dec74ca115547cef3', 'neg-gate-k26-legal96.txt': 'ee8333fa5c284401c6867fc0aeaa2707b2941a4dbe62d19355568283249c9928', 'neg-gate-k26-stones6.txt': 'f2b6c76c6bf6fe66431f15d0efc739298d5deb6639c87acd79e3182bf9f4ecc3', 'neg-gate-k27-legal94.txt': '4e0e0d50a6ae1773feb1c0e6f927bcd5cb677d6788eb7ca02d236f60874bcad0', 'neg-gate-k27-stones6.txt': '99e1c4fd316764cd7e8abf881e3760301d1664cf73a2e3cc28197a2233a0118d', 'neg-gate-k28-legal99.txt': '3133005f01c533daa5536f0c2b7ca7d7dc37d68a92c77402a5d3a4034ea473a0', 'neg-gate-k28-stones6.txt': 'cb92aa68df9fa76e0a0a2674bebb591dc3b58d60ae4e2cbb044995eb31535c38', 'neg-gate-k29-legal98.txt': 'b2fd103992d3584f7a274a0224801ebf740d7e9860d6ec658751784538e5313c', 'neg-gate-k29-stones6.txt': '61133386f5710633cda9d079fa2dd360213f792cff4e3a009967221c287e3c09', 'neg-gate-k30-legal96.txt': '53d1be5d98153c83b30f12674597bb028e8834bd048d671a5bcee29dd3ff37d7', 'neg-gate-k30-stones6.txt': 'c7c29d7c2b10f644c054654bfec885192339d4cf8a14d9782a7348974d02dc5f', 'neg-gate-k31-legal93.txt': 'c7b0ed201d2f7b9149c69ecc4329a0a9e8a47408e6f9aae3cc8482a58902bf4a', 'neg-gate-k31-stones6.txt': '750d2cb2274369f886bc4c934a7c1792f493afd3950d68d4c767a2d7c819acd5', 'neg-gate-k32-legal94.txt': '45f404d2d271c5759d09b31fbdc2e0c009c3acc479c545fe8ccabcaf57d38b05', 'neg-gate-k32-stones6.txt': '9737d9617f4bdf7e590e24e7574b06cf677de81f99802f13d9ea63b6d9716860', 'neg-gate-k34-legal97.txt': 'b043bcb60ebebcc1294be4db8e3ded87e45faa6ae0a6f98e500b66c47285a635', 'neg-gate-k34-stones6.txt': '0e72246de06c90039a8cfe0be3ef282afc5d11891160d5afc2fe8da1c7dedf0a', 'neg-gate-k35-legal101.txt': '7e4578dbb4f51c716f8416d4ebbf6774987e077deb39def494799cf971c94808', 'neg-gate-k35-stones6.txt': '2622798bd3117b405fb3241ec0b4036d7f8d82f6bf35920e60b4172d6666323f', 'neg-gate-k36-legal101.txt': 'd5229757466a7a69866f8e68562969dde315809ad86da8ddbaf2866d0fdc8cff', 'neg-gate-k36-stones6.txt': '070e0850f31e2eae8f7a4405b99c1e0408ed8836237615d6e67817a12968be9b', 'neg-gate-k37-legal104.txt': 'ef89c56f5800c98de51e11873460a6a1b3108e0f6e6885f1a8eff3f76d8a07af', 'neg-gate-k37-stones6.txt': 'd4e98c260fb4915e9312e47bb4eae4451bb1a2e312d557111a565426b9e229e1', 'neg-gate-k39-legal101.txt': '4c83f9d067d02b6e8e5a4fcfdffde15acf7599033f0575681479f39de9c2da7c', 'neg-gate-k39-stones6.txt': '76721f4e1f4e5127ee322a4b2a6af1bee0aa0507e506ecb8ae11dba6475f689d', 'neg-gate-k40-legal103.txt': 'bc6129cec44a55b6558d1ae9a7c688a540688639f4a535233999ef29dda84ebe', 'neg-gate-k40-stones6.txt': '53606dd303ed0e2799b7854679091e81edfd6c56fd5ea81d28fc0420fd4001d0', 'neg-gate-k41-legal101.txt': 'c7f23a5d39759cc757e025837bf6ae099181c683a512739c1c326f7da304c650', 'neg-gate-k41-stones6.txt': '7a68d1b0bd2d8ad206c083adb744f01d703a31ea370c82e48f547e1cd0c264cf', 'neg-gate-k42-legal102.txt': '0f2dc583e33e5d256d6164474ae635f64cd898b2c9658753238b7ba629278da9', 'neg-gate-k42-stones6.txt': '28ea53c585a502f6c9e5e8e2625ff678fe715332bb9af30d6d93660ec8e9ce5c', 'neg-gate-k43-legal104.txt': '3a3236a18265a21f6a6d336b03dc567a09705e9e6ff4e8b81227a8594583053f', 'neg-gate-k43-stones6.txt': '5db9388f31d05e73968f45b10c19178cb96f154c1d9f9f5241b2d79b33c3231f'}

# --- adopted keys -------------------------------------------------------
ADOPTED_IDS = [
    "k09",
    "k10",
    "k11",
    "k12",
    "k14",
    "k15",
    "k16",
    "k17",
    "k18",
    "k21",
    "k22",
    "k23",
    "k24",
    "k25",
    "k26",
    "k27",
    "k28",
    "k29",
    "k30",
    "k31",
    "k32",
    "k34",
    "k35",
    "k36",
    "k37",
    "k39",
    "k40",
    "k41",
    "k42",
    "k43"
]
ADOPTED_KEY_PINS = {
    "k09": [
        10377419441368469504,
        65536,
        87,
        97281,
        9,
        15000000,
        4018184
    ],
    "k10": [
        10378545341275312128,
        65536,
        84,
        85763,
        10,
        15000000,
        4295355
    ],
    "k11": [
        10412322338480590848,
        65536,
        86,
        112071,
        11,
        15000000,
        7012218
    ],
    "k12": [
        10952754293765050368,
        65536,
        83,
        109493,
        12,
        15000000,
        5688761
    ],
    "k14": [
        1152956757699461120,
        536870912,
        99,
        105775,
        14,
        15000000,
        6801611
    ],
    "k15": [
        1297036692683751424,
        1064960,
        99,
        48266,
        15,
        15000000,
        5947870
    ],
    "k16": [
        1297036761403228160,
        536870912,
        95,
        82565,
        16,
        15000000,
        10883904
    ],
    "k17": [
        10376293541461626880,
        65537,
        96,
        54808,
        17,
        15000000,
        1241921
    ],
    "k18": [
        10376293541461626880,
        65544,
        91,
        112020,
        18,
        15000000,
        1838655
    ],
    "k21": [
        10376293541461626880,
        67174400,
        90,
        111812,
        21,
        15000000,
        3649839
    ],
    "k22": [
        10376293541461626880,
        268500992,
        98,
        112202,
        22,
        15000000,
        7527812
    ],
    "k23": [
        10376293541461626912,
        65536,
        97,
        99496,
        23,
        15000000,
        10938326
    ],
    "k24": [
        10376293541461627904,
        65536,
        93,
        5901,
        24,
        15000000,
        4796315
    ],
    "k25": [
        10376293541461659648,
        65536,
        91,
        106275,
        25,
        15000000,
        5496449
    ],
    "k26": [
        10376293541462151168,
        65536,
        95,
        62164,
        26,
        15000000,
        14439424
    ],
    "k27": [
        10376293541478404096,
        65536,
        93,
        112206,
        27,
        15000000,
        2250306
    ],
    "k28": [
        10376293541528735744,
        65536,
        98,
        107317,
        28,
        2000000,
        1918850
    ],
    "k29": [
        10376293541595844608,
        65536,
        97,
        39140,
        29,
        15000000,
        4996919
    ],
    "k30": [
        10376293610181103616,
        65536,
        95,
        112207,
        30,
        15000000,
        3933511
    ],
    "k31": [
        10376856491415048192,
        65536,
        92,
        103952,
        31,
        15000000,
        4560796
    ],
    "k32": [
        10664523917613338624,
        65536,
        93,
        112058,
        32,
        2000000,
        1989908
    ],
    "k34": [
        14987979559889014784,
        65536,
        96,
        86700,
        34,
        15000000,
        8567123
    ],
    "k35": [
        1152921573327372288,
        553648128,
        100,
        57660,
        35,
        15000000,
        14273589
    ],
    "k36": [
        1224979167365300224,
        536870912,
        100,
        100161,
        36,
        15000000,
        3007021
    ],
    "k37": [
        1297036692683751424,
        17825792,
        103,
        16999,
        37,
        15000000,
        8083885
    ],
    "k39": [
        10376293541461626880,
        66560,
        100,
        71506,
        39,
        15000000,
        5725348
    ],
    "k40": [
        10376293541461626880,
        67584,
        102,
        52359,
        40,
        15000000,
        5926395
    ],
    "k41": [
        10376293541461626884,
        65536,
        100,
        112187,
        41,
        15000000,
        6536846
    ],
    "k42": [
        10376293541461627136,
        65536,
        101,
        58495,
        42,
        15000000,
        8486305
    ],
    "k43": [
        10376293541461692416,
        65536,
        103,
        100922,
        43,
        15000000,
        6916669
    ]
}
ADOPTED_RAW_SHAS = {
    "k09": {
        "at15m-run1-k09.out.csv": "8ad953baf0a3de2db492b6242d087a6eba3fe687c91d2e85dadf284d92f27b09",
        "at15m-run2-k09.out.csv": "3bbadffc78845e85086bdff8c926e6c2a43e295dc4e4c6a11d644649b66cb2da",
        "at2m-k09.out.csv": "830b870ffeb9e646e949eb669053797a7c4fcaf74982f27aa6e83a050c0ae8b4"
    },
    "k10": {
        "at15m-run1-k10.out.csv": "e29a71292f1e90d14e06adc83e91e508659c10d82fb44ecaaf98caa9c2faac96",
        "at15m-run2-k10.out.csv": "17e01019a008a2e6ffe5d3bc5371f0e437276ba50c0dc03a0658efbf6d5ac19f",
        "at2m-k10.out.csv": "289f227f74d043e94d01ff66fc0fb79d442366dd64df1c470341120f4247657c"
    },
    "k11": {
        "at15m-run1-k11.out.csv": "09945e30a02937e99ae20795d989d6035194cdaa0a5611fe5a9e837cdd7068f3",
        "at15m-run2-k11.out.csv": "a562d639db1e3fbbda72bb5181b3895a4597fd71a1989dbad0f1ee4fec439020",
        "at2m-k11.out.csv": "ad82b26860bce8873b302baa4f0479d895f27673e7b25b3270600d48cd604ccf"
    },
    "k12": {
        "at15m-run1-k12.out.csv": "43c4494ed5bcaea898640b8755325c1f2b27a9aeff6ce66f5202dfa3e190b897",
        "at15m-run2-k12.out.csv": "43c4494ed5bcaea898640b8755325c1f2b27a9aeff6ce66f5202dfa3e190b897",
        "at2m-k12.out.csv": "e7dd51a50bbf132c677d37f1e825c8a5ec05c5736d7c80c2aee5af984c0e0380"
    },
    "k14": {
        "at15m-run1-k14.out.csv": "db48c6fe5e314feeea1b6f60da2277a8eb23cbc6b3e7f20ceb093f9a16b9bf1f",
        "at15m-run2-k14.out.csv": "eab08cd4719ebf2c32bd61144a8ec86e22665a2adfc84134ca44274339fd38d3",
        "at2m-k14.out.csv": "5c651471e0cb48b5a69e0863eca442a7b61b3fdb4b719d16570dd175aa435846"
    },
    "k15": {
        "at15m-run1-k15.out.csv": "41ed7c0f35ae119dfd08714b2e04d63d4b836777dc6dff9254631c4070454a26",
        "at15m-run2-k15.out.csv": "c4e2f73508b326b43ab8f527656c5ffd47c3e903f2a2f8bbbfbbf719388cb2a6",
        "at2m-k15.out.csv": "8ddc4d2928e9a753a638553d0cc6ef14e2a8bfbcbba0e9aec4b26479b12201f1"
    },
    "k16": {
        "at15m-run1-k16.out.csv": "9446b88264791b9f0900e6c380179fad593c203e9c5e5f5c4fef182b94273956",
        "at15m-run2-k16.out.csv": "9446b88264791b9f0900e6c380179fad593c203e9c5e5f5c4fef182b94273956",
        "at2m-k16.out.csv": "1470c4fc82da1800d90e5cb0c4d723ffcf3ec51f5f1a957dbcff2ec9ff2c66b2"
    },
    "k17": {
        "at15m-run1-k17.out.csv": "f82e89fd68e227a95cb0602d610423210d6f1ac5ece72ed5a19a837eac183476",
        "at15m-run2-k17.out.csv": "f82e89fd68e227a95cb0602d610423210d6f1ac5ece72ed5a19a837eac183476",
        "at2m-k17.out.csv": "f2834fe5c2d7e37c1ab375277080f86ca05fc03b2b317d49229eb8a122905e9a",
        "at2m-run2-k17.out.csv": "f2834fe5c2d7e37c1ab375277080f86ca05fc03b2b317d49229eb8a122905e9a"
    },
    "k18": {
        "at15m-run1-k18.out.csv": "5ffe97ab364ef3c6a30fcf757304fa5a2641816094fd5be8ae58b0dfd29dbadf",
        "at15m-run2-k18.out.csv": "c411dbb19dc6bf6fac39827aa18d1df73d050ec3bf5520a53a422774d0fe2132",
        "at2m-k18.out.csv": "302da911d9923ef373acd6c5e5caea7d2a7a6dc584e538d1462db8c093b3713c",
        "at2m-run2-k18.out.csv": "302da911d9923ef373acd6c5e5caea7d2a7a6dc584e538d1462db8c093b3713c"
    },
    "k21": {
        "at15m-run1-k21.out.csv": "a8c70a5a5cb4d343603a1b8be86a13a10a91ea59a67d1fc806a152acdfe0ff4f",
        "at15m-run2-k21.out.csv": "934d60aa76cfad44c945c1509caff1c7604a73cd2b2dda002ae71008ab5f47c2",
        "at2m-k21.out.csv": "027bffe2cdec9fc03cce47a1cb7493472357a112d40fbe19f78259adf23ffef0"
    },
    "k22": {
        "at15m-run1-k22.out.csv": "c5ae72f9ec839e1a451e279705a743f383769105bc165c49f0fe8c0a32013538",
        "at15m-run2-k22.out.csv": "789c8d31bced36108f022a8157d3efd883b441fb86f4f330b0a61855c7a7f89e",
        "at2m-k22.out.csv": "a85953a759240f8f91726c16edc0568b8a0068c9666a0c2af55e9bbc90da4639"
    },
    "k23": {
        "at15m-run1-k23.out.csv": "4b1de3ccaf7e3bc4852f63ed6bb57409da994e9cac68ae90e3a8966d422846ca",
        "at15m-run2-k23.out.csv": "cd4f2f1f303e49e58c3e7d17c27b0eb50ecbb66f4a25ecb9254f6a2e9ab38085",
        "at2m-k23.out.csv": "57a9a999235292892dce3d0e8db6c3147cd91bcadb5711d854d7d9900de8b2de"
    },
    "k24": {
        "at15m-run1-k24.out.csv": "37d77c3762bc95e08a095d21d192b6e5bfa7cfad7b21282bce9807bf68aca464",
        "at15m-run2-k24.out.csv": "9866fabeddb14ab503166944acf61772501c80cbd801faaf1f3aec974f4697b6",
        "at2m-k24.out.csv": "a1f0b3b68645cb7b9c254f6254200cbea1cafc1c4fac229fd0e7578a2a81f6f1"
    },
    "k25": {
        "at15m-run1-k25.out.csv": "3bbb1dc2a8a6fd67ce9039a4c0a87fa9715a26bc567e0f23dabd5044d1d91227",
        "at15m-run2-k25.out.csv": "768b87150adfa3e87b134ee8f511f9851a58a1d0a571cff049dabef1ce443d2a",
        "at2m-k25.out.csv": "b10147cbe3930b57b571f3e98697fde16ad231d07655f00f932cb2feeb6ccf7a"
    },
    "k26": {
        "at15m-run1-k26.out.csv": "d53e0cb756dddc9e9d0a84a6a50b75cefd812f51337a2b3ef19752253d2b254e",
        "at15m-run2-k26.out.csv": "5530922e24a48f5b71a15c4fa3a9357b964b90c158c8bc7ee72d65b3a7964cdd",
        "at2m-k26.out.csv": "736209bbbc321d5202dfb5baa2539df68d298a2b5465801c4e18c7e7c485f817"
    },
    "k27": {
        "at15m-run1-k27.out.csv": "5bc995699e804475f107570b1c06fca903693d4bc2ef47340739fdc482eacd6c",
        "at15m-run2-k27.out.csv": "5bc995699e804475f107570b1c06fca903693d4bc2ef47340739fdc482eacd6c",
        "at2m-k27.out.csv": "dad5b085f1d80f0a7400dfb7792f90e63b4a6ce5c0ebb2d493147f262a93618b"
    },
    "k28": {
        "at2m-k28.out.csv": "189092ef700e69750ad9be96aaf9abf4fe8eda0559432cef8cd58bc50faa1ed1",
        "at2m-run2-k28.out.csv": "189092ef700e69750ad9be96aaf9abf4fe8eda0559432cef8cd58bc50faa1ed1"
    },
    "k29": {
        "at15m-run1-k29.out.csv": "b7e2d3c78ba07a94aefc3305a7ddeed136e95fd460530dfa3066a30abe391428",
        "at15m-run2-k29.out.csv": "b7e2d3c78ba07a94aefc3305a7ddeed136e95fd460530dfa3066a30abe391428",
        "at2m-k29.out.csv": "bf4d012246b6c830399f6f153610d8fe1edc77521cad33b7dfdd2c43ff7b76f0"
    },
    "k30": {
        "at15m-run1-k30.out.csv": "69a156a55a86e302f80bee81a36d144af7b48934402baaba315bf892689a550d",
        "at15m-run2-k30.out.csv": "43ddd5818ba82c09726e6780beefc5d35874482bf276d831805d253de579475a",
        "at2m-k30.out.csv": "8af30f012f8b28a267215f95aae3a78d761d27550fe74ab69fdc6d455938cca3"
    },
    "k31": {
        "at15m-run1-k31.out.csv": "6dddbe547438e9726e532bcddbd9c8e9327635418cf03697e95dfccdfda551b3",
        "at15m-run2-k31.out.csv": "6dddbe547438e9726e532bcddbd9c8e9327635418cf03697e95dfccdfda551b3",
        "at2m-k31.out.csv": "807d45296efddf7df344d27a9a5c6fe3762eda3c3ee47cd97ab47171d3cbd7d8"
    },
    "k32": {
        "at2m-k32.out.csv": "8c8ebb3eb42da60e57bde403cc0dfe15c72f256b526a6c4c73e42722bc668312",
        "at2m-run2-k32.out.csv": "8c8ebb3eb42da60e57bde403cc0dfe15c72f256b526a6c4c73e42722bc668312"
    },
    "k34": {
        "at15m-run1-k34.out.csv": "c0de8c6a0df4e6bb33eadcbc8bd7aa89f8df3ced8d65d12a34e8544a7233ffb2",
        "at15m-run2-k34.out.csv": "8021ec79348e2467ab0b5f9760089ab3ec2b91d0bfdb81dd95bab42e73737313",
        "at2m-k34.out.csv": "2ce58086b3bfc0b487bd6e170c0480257cf8cf8c7793d251eb39d89d2d170d15"
    },
    "k35": {
        "at15m-run1-k35.out.csv": "7722a6488ab33017f9da9ff947d906264d6432019d3cc9040d733169cd98c57f",
        "at15m-run2-k35.out.csv": "95b1014485c87666913a5266b182e6d514628ae477096c5a9989ee18b806e52c",
        "at2m-k35.out.csv": "0101327dced0f46d4087c4aa631d2917de30bbfe6215cc7ea104fe64d0199201"
    },
    "k36": {
        "at15m-run1-k36.out.csv": "562ba346acc6a4e3da8d3f80ab61aebfc5738192983ff3924a98cce89053276e",
        "at15m-run2-k36.out.csv": "562ba346acc6a4e3da8d3f80ab61aebfc5738192983ff3924a98cce89053276e",
        "at2m-k36.out.csv": "4d535300bcbc168b9478b9cde812ac0f581b19762bb1d17f969cdb2da3935c64"
    },
    "k37": {
        "at15m-run1-k37.out.csv": "eb00397435727be266f9783871e3932cd8c7a0ecd9a27585dbfa77b1411c2265",
        "at15m-run2-k37.out.csv": "c07990271dba7346c280fd6ed70bb8facb119916d5ab12fa3ae7933c7f0a325d",
        "at2m-k37.out.csv": "de8fcc1ed30fa40a319ec61dd9c01f657fb5e81ce617b0c6d8ab71534581762f"
    },
    "k39": {
        "at15m-run1-k39.out.csv": "af3bb4c3513561c1760c7aa774b9d2ee984930d3dd1e4ce7ba4ba2ae60f49ee0",
        "at15m-run2-k39.out.csv": "af3bb4c3513561c1760c7aa774b9d2ee984930d3dd1e4ce7ba4ba2ae60f49ee0",
        "at2m-k39.out.csv": "a7951d82df52cd7dc2aeabea6882f21a245e846281335d7c2740c0edba407130"
    },
    "k40": {
        "at15m-run1-k40.out.csv": "9dc4b27ecd03bcaeb0bd58475700a273a63d9b2a4ea47d33c4ce4542e6ea592b",
        "at15m-run2-k40.out.csv": "7a6d41d848ec2e32e28a30e387a93bbbbad426bb5670cf39a10d962e544084e6",
        "at2m-k40.out.csv": "643406dccb4b66c6b6e2153a2fef5b60120b5d49dc648066ddd9a8ed0865c44b"
    },
    "k41": {
        "at15m-run1-k41.out.csv": "542ca03402b81721f4a529d14dd240017d4fd81836f8ce458009c0bbbf6bddfd",
        "at15m-run2-k41.out.csv": "542ca03402b81721f4a529d14dd240017d4fd81836f8ce458009c0bbbf6bddfd",
        "at2m-k41.out.csv": "1b613c597a42a50a81beb6b2911f9b60493de64ab3b301b3db3f3a7ffe93ac80"
    },
    "k42": {
        "at15m-run1-k42.out.csv": "f1fab0ea787967329db92b3e9d81606ba5af7756ca7b195188599b0540313503",
        "at15m-run2-k42.out.csv": "a810cda5cb75e9cef92d8ec70a94e58c337a4f614a0e084c9d4beff8a12cac0c",
        "at2m-k42.out.csv": "61cf72b7071e4c4cc6a0d36f3d3d2660cdb0fc4b743b3afbe365ae4be92b61c9"
    },
    "k43": {
        "at15m-run1-k43.out.csv": "78668844f8c0b33d5baf5bac9d2cd49c7b047452a5b2464cf8024ed756f1c3dc",
        "at15m-run2-k43.out.csv": "78668844f8c0b33d5baf5bac9d2cd49c7b047452a5b2464cf8024ed756f1c3dc",
        "at2m-k43.out.csv": "7175fb05f2ffe544ff397b2288058934b4ecc381c33612d9ed23b7ee002cf434"
    }
}
AT2M_PINS = {
    "k09": [
        2000000,
        0,
        2000000
    ],
    "k10": [
        2000000,
        0,
        2000000
    ],
    "k11": [
        2000000,
        0,
        2000000
    ],
    "k12": [
        2000000,
        0,
        2000000
    ],
    "k14": [
        2000000,
        0,
        2000000
    ],
    "k15": [
        2000000,
        0,
        2000000
    ],
    "k16": [
        2000000,
        0,
        2000000
    ],
    "k17": [
        2000000,
        2,
        1241921
    ],
    "k18": [
        2000000,
        2,
        1838655
    ],
    "k21": [
        2000000,
        0,
        2000000
    ],
    "k22": [
        2000000,
        0,
        2000000
    ],
    "k23": [
        2000000,
        0,
        2000000
    ],
    "k24": [
        2000000,
        0,
        2000000
    ],
    "k25": [
        2000000,
        0,
        2000000
    ],
    "k26": [
        2000000,
        0,
        2000000
    ],
    "k27": [
        2000000,
        0,
        2000000
    ],
    "k28": [
        2000000,
        2,
        1918850
    ],
    "k29": [
        2000000,
        0,
        2000000
    ],
    "k30": [
        2000000,
        0,
        2000000
    ],
    "k31": [
        2000000,
        0,
        2000000
    ],
    "k32": [
        2000000,
        2,
        1989908
    ],
    "k34": [
        2000000,
        0,
        2000000
    ],
    "k35": [
        2000000,
        0,
        2000000
    ],
    "k36": [
        2000000,
        0,
        2000000
    ],
    "k37": [
        2000000,
        0,
        2000000
    ],
    "k39": [
        2000000,
        0,
        2000000
    ],
    "k40": [
        2000000,
        0,
        2000000
    ],
    "k41": [
        2000000,
        0,
        2000000
    ],
    "k42": [
        2000000,
        0,
        2000000
    ],
    "k43": [
        2000000,
        0,
        2000000
    ]
}
TI_COLD_PINS = {
    "k09": {
        "a": [
            "5ad35d7b60a1e4f9678d62ddca05640677ce68e1afd6bcb4834b9f36b83e18a2",
            4622038,
            2607830,
            652622
        ],
        "b": [
            "2c90f30d012967cba210499419744cc888a32ac6b3e3d0803fc702677ff0d2cf",
            4622038,
            2607830,
            652622
        ]
    },
    "k10": {
        "a": [
            "0b1060820db36b74571300c4c2c235f95f6f25da9bfa9bbd26acb3f8cd984ca8",
            4945820,
            2741107,
            888907
        ],
        "b": [
            "5a58a0fd16abd5398b30f173a09557acc3ce5bed851d9752160adc08145735f3",
            4945820,
            2741107,
            888907
        ]
    },
    "k11": {
        "a": [
            "8f43915dd613305198888ed4567fd87091c0ccfa8bb38756878534a1336abf0c",
            8105873,
            4437184,
            3911738
        ],
        "b": [
            "74a8e095b95b5fb51310221b90d84287b4713376aa024e9643db16629fb6e36c",
            8105873,
            4437184,
            3911738
        ]
    },
    "k12": {
        "a": [
            "1da376709160f66a561a4e7d5d05f2b1876ca3a61dfc4b1314e2d3ffcd9afb49",
            6593392,
            3638963,
            2404936
        ],
        "b": [
            "22ba7b24d027f4621dd94a57b3061cf6ff062756beca4f24e3dc7574b9fa43ac",
            6593392,
            3638963,
            2404936
        ]
    },
    "k14": {
        "a": [
            "cfc0d907618680c247dead5ee761f471e41b37d1c82775bfd0df33c941cf7383",
            7836133,
            4297914,
            3642312
        ],
        "b": [
            "1fa1ae612379bbb0f506e16135fd967dd3e7beedcedd3ef6723e39d81903a820",
            7836133,
            4297914,
            3642312
        ]
    },
    "k15": {
        "a": [
            "ee7b943e05cd4c751c9d5696ec752bcde068c5d36a7fbfd6f5f81372a0e5a5b1",
            6903671,
            3790763,
            2712282
        ],
        "b": [
            "117eeefc5726e220872df3f5271890c93432537ac99c435128bef966a8b2b962",
            6903671,
            3790763,
            2712282
        ]
    },
    "k16": {
        "a": [
            "d13eceaeeb74f023c0be6db586ea0eddd2aefda8c2a2171c0db7f8be12af1021",
            12650074,
            6857256,
            8455770
        ],
        "b": [
            "b380213b4a51b7e175f4f747b2ab3ad87030998d77f028f5c8523a3fc33127f2",
            12650074,
            6857256,
            8455770
        ]
    },
    "k17": {
        "a": [
            "f299b0daf31934056875292ecc7c9324a22c273b32d505a0e2457d5aacac4f44",
            1405334,
            826431,
            47
        ],
        "b": [
            "2c67b5815fe365ae3417a027746f883e095aff8f2caf269e6a064b3bb38c5a3e",
            1405334,
            826431,
            47
        ]
    },
    "k18": {
        "a": [
            "d68216a123bf0588714abe8ddd87921f24da6bdca83320dea253c6261b9d684f",
            2098799,
            1184660,
            2153
        ],
        "b": [
            "700efa7633e9e485845bd96e3dcdc5fe29438b4d22f6df1e7c22d084f332c145",
            2098799,
            1184660,
            2153
        ]
    },
    "k21": {
        "a": [
            "e4e2243334e1eb68432415ae818b04b9f441cd74f6823e4af6f5da4554d70f17",
            4202005,
            2326723,
            392033
        ],
        "b": [
            "744cbeb7f44b5d4bf2ba229b634aab8b7616f341da9e0cc8fabfee3b4ef2f4d5",
            4202005,
            2326723,
            392033
        ]
    },
    "k22": {
        "a": [
            "d10c79da6c5f71986cd33957f377a7f01ea46ee45c4283531fa0d33c89f70571",
            8820734,
            4653093,
            4626471
        ],
        "b": [
            "b9391f00b3961191e0a61071a619633e9faf7b95d2ff9984138ffcd97a9c9611",
            8820734,
            4653093,
            4626471
        ]
    },
    "k23": {
        "a": [
            "9235bf8fa6692bab30a3cbd487d3c2d7b983b7e18999655557ea3363b10d25eb",
            12654986,
            6739220,
            8460682
        ],
        "b": [
            "6f912c5f407a8ca9fe293f8b5448fd68f9eecd18e57502c8ee1b88569234a4fb",
            12654986,
            6739220,
            8460682
        ]
    },
    "k24": {
        "a": [
            "55b4e0da8764225da3d933de42246b2185fa4e0eae6373a98b185649a8e85f8a",
            5616289,
            3010163,
            1467038
        ],
        "b": [
            "9e9240c0e29fafe3335648fa70679b17c414af93cfe54f2ab312e53c3e210fa7",
            5616289,
            3010163,
            1467038
        ]
    },
    "k25": {
        "a": [
            "d7bd9e427203861828831f74a5af7affe8da422326500b7ce290d7a1ba71006f",
            6336310,
            3564228,
            2153523
        ],
        "b": [
            "7e888bf7d9f923ecf31afcc8f98107a9cc65da3211106ae5aeb48eda9a7d7cf5",
            6336310,
            3564228,
            2153523
        ]
    },
    "k26": {
        "a": [
            "34dc0c513e2bce7d63e3bcd8c44c5e71b5851c842644525ed2778076ca53fe20",
            16684962,
            8721684,
            12490658
        ],
        "b": [
            "72f2d0a30931e466de5cd5be0c6992b7694adb3391063407a18175e9697ec191",
            16684962,
            8721684,
            12490658
        ]
    },
    "k27": {
        "a": [
            "2e24b455b831924a37039d5315cf4f9ef431538ed0d0fe3b876414835ecc4018",
            2578044,
            1458498,
            10504
        ],
        "b": [
            "a6867369fde93aa460f626948732c2fc89e59638c1d0c657dfacd23e71a585f5",
            2578044,
            1458498,
            10504
        ]
    },
    "k28": {
        "a": [
            "ccbd590fe10505c00163c259d20d75f7f7241c6b1f0ab142b61b53cfc9d1c109",
            2177958,
            1274689,
            2777
        ],
        "b": [
            "abc2ac1dabe13083854374b6e1ce534d81cb66698a272dfa3d982043d730ac3a",
            2177958,
            1274689,
            2777
        ]
    },
    "k29": {
        "a": [
            "3ffa1bb2f336983ea96f02c6778d3fb2dcfbe84c40f8d6730beaf84fa0998e04",
            5797487,
            3237734,
            1635160
        ],
        "b": [
            "f86445df1e04680d6bcdcc20f50c3f4017e0ca9f982ea0cad1a1d08d405817b9",
            5797487,
            3237734,
            1635160
        ]
    },
    "k30": {
        "a": [
            "c370b6486bcc1b96b08eec82c3ddb78c53ea3b180ec7f6682302105981123574",
            4531296,
            2619620,
            597949
        ],
        "b": [
            "d86620f4d28736e22ff40d49608b21179f6cdbddb455982e7918a2b102213a4e",
            4531296,
            2619620,
            597949
        ]
    },
    "k31": {
        "a": [
            "1cd6994458d2158c97e4af57d8cf2b64aaaa31ab99c9643f7e86873fe8aa5b0d",
            5269285,
            2862847,
            1151374
        ],
        "b": [
            "9ceea6a9f5349da5c2765319ef63f8bdc3e34844f005c552dfe71fe48bffb562",
            5269285,
            2862847,
            1151374
        ]
    },
    "k32": {
        "a": [
            "6074ea72747ad8c7d5410227ac872d0a3acd7de355cb16414e23dfc2242dab45",
            2235267,
            1374600,
            3852
        ],
        "b": [
            "6ae42019969e8243a34858312ed7bfa87a8505a3044bad6b35d8dcd5432df62c",
            2235267,
            1374600,
            3852
        ]
    },
    "k34": {
        "a": [
            "ec9eed20fc1897ca0054abf1dbe8d866604948e591f5f82bcb66e9984362461f",
            9966873,
            5293840,
            5772570
        ],
        "b": [
            "735153a8738628384a31940d3a6ae47f132d2e9810100ab2e23ab9a19ccf08ba",
            9966873,
            5293840,
            5772570
        ]
    },
    "k35": {
        "a": [
            "5db2c5562b0e9eac0b0e56a78122e871a1aa96c3ccec447c8e30c2951d739e1c",
            16896018,
            8726341,
            12701714
        ],
        "b": [
            "476472923cb2e23238a90fdf0a7d9bea7a8e8e4682b9811fde786f54720fd512",
            16896018,
            8726341,
            12701714
        ]
    },
    "k36": {
        "a": [
            "92d701a8bf8745659787d1db152338d8189eb71703c74ed712ac267d1e8f41d8",
            3440325,
            1961576,
            107949
        ],
        "b": [
            "c9f8b0f30915841c2c4a8285b6dc9ae6536c01b853df6b16539a07c1d37762de",
            3440325,
            1961576,
            107949
        ]
    },
    "k37": {
        "a": [
            "918d1697a83706ddac0e411de93770733bf581e17e130b1c255e5cea58da9e92",
            9510402,
            4989499,
            5316103
        ],
        "b": [
            "2d9b9c8714c70c63756ea25b71ac4f8b50fd35900b6fdc4bf07db7b5cc4d6aae",
            9510402,
            4989499,
            5316103
        ]
    },
    "k39": {
        "a": [
            "41387f03460bf5cdf6eb339f10ce4a3445a6641f78f0bbf00651172c9a715636",
            6611082,
            3659270,
            2422272
        ],
        "b": [
            "043ff581d316d327f48f0f1b5627309320e4c1aff3dd05bc1b0e8cc253734286",
            6611082,
            3659270,
            2422272
        ]
    },
    "k40": {
        "a": [
            "d9cd4ecd68a0a5fb5f8ee09423225867982cb34615e7d5db57e4812f72ca3bee",
            6894081,
            3725971,
            2703506
        ],
        "b": [
            "012a494b1e2e71a97077c3492c9900d663dc0b8e91e1d244f268b712dacf3fd6",
            6894081,
            3725971,
            2703506
        ]
    },
    "k41": {
        "a": [
            "fff7655e11990baeb774e37431a8a7d9f96ee18ada33d56cdad75f4770046199",
            7704061,
            4018770,
            3510186
        ],
        "b": [
            "76f181bb9c0cf5335ace62c30216360731c79a1c4eccd94d906dea0f452294ae",
            7704061,
            4018770,
            3510186
        ]
    },
    "k42": {
        "a": [
            "38cd4bef3862ff2bbb0e8d60bd61f1908698e784c38cfaa083549a72d9b8e6ce",
            10223560,
            5244634,
            6029256
        ],
        "b": [
            "9ad6ed80b32b3255769c9d59b617bf2347c3138478d05a17a1b1ac37f3665157",
            10223560,
            5244634,
            6029256
        ]
    },
    "k43": {
        "a": [
            "c5a8939f9ba26a9733453f3101c45849a0e2c0e2f39de5731056de4bc3c2df37",
            8061097,
            4354662,
            3867018
        ],
        "b": [
            "17e2903113ff1d64fa3d0202caf7b5cd1642ef24102fd10a56a9514da1d1fedb",
            8061097,
            4354662,
            3867018
        ]
    }
}
TI_REPLICA_SHAS = {
    "k09": {
        "at15m-run1-k09.out.csv": "8ad953baf0a3de2db492b6242d087a6eba3fe687c91d2e85dadf284d92f27b09",
        "at15m-run2-k09.out.csv": "3bbadffc78845e85086bdff8c926e6c2a43e295dc4e4c6a11d644649b66cb2da",
        "at2m-k09.out.csv": "830b870ffeb9e646e949eb669053797a7c4fcaf74982f27aa6e83a050c0ae8b4"
    },
    "k10": {
        "at15m-run1-k10.out.csv": "e29a71292f1e90d14e06adc83e91e508659c10d82fb44ecaaf98caa9c2faac96",
        "at15m-run2-k10.out.csv": "17e01019a008a2e6ffe5d3bc5371f0e437276ba50c0dc03a0658efbf6d5ac19f",
        "at2m-k10.out.csv": "289f227f74d043e94d01ff66fc0fb79d442366dd64df1c470341120f4247657c"
    },
    "k11": {
        "at15m-run1-k11.out.csv": "09945e30a02937e99ae20795d989d6035194cdaa0a5611fe5a9e837cdd7068f3",
        "at15m-run2-k11.out.csv": "a562d639db1e3fbbda72bb5181b3895a4597fd71a1989dbad0f1ee4fec439020",
        "at2m-k11.out.csv": "ad82b26860bce8873b302baa4f0479d895f27673e7b25b3270600d48cd604ccf"
    },
    "k12": {
        "at15m-run1-k12.out.csv": "43c4494ed5bcaea898640b8755325c1f2b27a9aeff6ce66f5202dfa3e190b897",
        "at15m-run2-k12.out.csv": "43c4494ed5bcaea898640b8755325c1f2b27a9aeff6ce66f5202dfa3e190b897",
        "at2m-k12.out.csv": "e7dd51a50bbf132c677d37f1e825c8a5ec05c5736d7c80c2aee5af984c0e0380"
    },
    "k14": {
        "at15m-run1-k14.out.csv": "db48c6fe5e314feeea1b6f60da2277a8eb23cbc6b3e7f20ceb093f9a16b9bf1f",
        "at15m-run2-k14.out.csv": "eab08cd4719ebf2c32bd61144a8ec86e22665a2adfc84134ca44274339fd38d3",
        "at2m-k14.out.csv": "5c651471e0cb48b5a69e0863eca442a7b61b3fdb4b719d16570dd175aa435846"
    },
    "k15": {
        "at15m-run1-k15.out.csv": "41ed7c0f35ae119dfd08714b2e04d63d4b836777dc6dff9254631c4070454a26",
        "at15m-run2-k15.out.csv": "c4e2f73508b326b43ab8f527656c5ffd47c3e903f2a2f8bbbfbbf719388cb2a6",
        "at2m-k15.out.csv": "8ddc4d2928e9a753a638553d0cc6ef14e2a8bfbcbba0e9aec4b26479b12201f1"
    },
    "k16": {
        "at15m-run1-k16.out.csv": "9446b88264791b9f0900e6c380179fad593c203e9c5e5f5c4fef182b94273956",
        "at15m-run2-k16.out.csv": "9446b88264791b9f0900e6c380179fad593c203e9c5e5f5c4fef182b94273956",
        "at2m-k16.out.csv": "1470c4fc82da1800d90e5cb0c4d723ffcf3ec51f5f1a957dbcff2ec9ff2c66b2"
    },
    "k17": {
        "at15m-run1-k17.out.csv": "f82e89fd68e227a95cb0602d610423210d6f1ac5ece72ed5a19a837eac183476",
        "at15m-run2-k17.out.csv": "f82e89fd68e227a95cb0602d610423210d6f1ac5ece72ed5a19a837eac183476",
        "at2m-k17.out.csv": "f2834fe5c2d7e37c1ab375277080f86ca05fc03b2b317d49229eb8a122905e9a",
        "at2m-run2-k17.out.csv": "f2834fe5c2d7e37c1ab375277080f86ca05fc03b2b317d49229eb8a122905e9a"
    },
    "k18": {
        "at15m-run1-k18.out.csv": "5ffe97ab364ef3c6a30fcf757304fa5a2641816094fd5be8ae58b0dfd29dbadf",
        "at15m-run2-k18.out.csv": "c411dbb19dc6bf6fac39827aa18d1df73d050ec3bf5520a53a422774d0fe2132",
        "at2m-k18.out.csv": "302da911d9923ef373acd6c5e5caea7d2a7a6dc584e538d1462db8c093b3713c",
        "at2m-run2-k18.out.csv": "302da911d9923ef373acd6c5e5caea7d2a7a6dc584e538d1462db8c093b3713c"
    },
    "k21": {
        "at15m-run1-k21.out.csv": "a8c70a5a5cb4d343603a1b8be86a13a10a91ea59a67d1fc806a152acdfe0ff4f",
        "at15m-run2-k21.out.csv": "934d60aa76cfad44c945c1509caff1c7604a73cd2b2dda002ae71008ab5f47c2",
        "at2m-k21.out.csv": "027bffe2cdec9fc03cce47a1cb7493472357a112d40fbe19f78259adf23ffef0"
    },
    "k22": {
        "at15m-run1-k22.out.csv": "c5ae72f9ec839e1a451e279705a743f383769105bc165c49f0fe8c0a32013538",
        "at15m-run2-k22.out.csv": "789c8d31bced36108f022a8157d3efd883b441fb86f4f330b0a61855c7a7f89e",
        "at2m-k22.out.csv": "a85953a759240f8f91726c16edc0568b8a0068c9666a0c2af55e9bbc90da4639"
    },
    "k23": {
        "at15m-run1-k23.out.csv": "4b1de3ccaf7e3bc4852f63ed6bb57409da994e9cac68ae90e3a8966d422846ca",
        "at15m-run2-k23.out.csv": "cd4f2f1f303e49e58c3e7d17c27b0eb50ecbb66f4a25ecb9254f6a2e9ab38085",
        "at2m-k23.out.csv": "57a9a999235292892dce3d0e8db6c3147cd91bcadb5711d854d7d9900de8b2de"
    },
    "k24": {
        "at15m-run1-k24.out.csv": "37d77c3762bc95e08a095d21d192b6e5bfa7cfad7b21282bce9807bf68aca464",
        "at15m-run2-k24.out.csv": "9866fabeddb14ab503166944acf61772501c80cbd801faaf1f3aec974f4697b6",
        "at2m-k24.out.csv": "a1f0b3b68645cb7b9c254f6254200cbea1cafc1c4fac229fd0e7578a2a81f6f1"
    },
    "k25": {
        "at15m-run1-k25.out.csv": "3bbb1dc2a8a6fd67ce9039a4c0a87fa9715a26bc567e0f23dabd5044d1d91227",
        "at15m-run2-k25.out.csv": "768b87150adfa3e87b134ee8f511f9851a58a1d0a571cff049dabef1ce443d2a",
        "at2m-k25.out.csv": "b10147cbe3930b57b571f3e98697fde16ad231d07655f00f932cb2feeb6ccf7a"
    },
    "k26": {
        "at15m-run1-k26.out.csv": "d53e0cb756dddc9e9d0a84a6a50b75cefd812f51337a2b3ef19752253d2b254e",
        "at15m-run2-k26.out.csv": "5530922e24a48f5b71a15c4fa3a9357b964b90c158c8bc7ee72d65b3a7964cdd",
        "at2m-k26.out.csv": "736209bbbc321d5202dfb5baa2539df68d298a2b5465801c4e18c7e7c485f817"
    },
    "k27": {
        "at15m-run1-k27.out.csv": "5bc995699e804475f107570b1c06fca903693d4bc2ef47340739fdc482eacd6c",
        "at15m-run2-k27.out.csv": "5bc995699e804475f107570b1c06fca903693d4bc2ef47340739fdc482eacd6c",
        "at2m-k27.out.csv": "dad5b085f1d80f0a7400dfb7792f90e63b4a6ce5c0ebb2d493147f262a93618b"
    },
    "k28": {
        "at2m-k28.out.csv": "189092ef700e69750ad9be96aaf9abf4fe8eda0559432cef8cd58bc50faa1ed1",
        "at2m-run2-k28.out.csv": "189092ef700e69750ad9be96aaf9abf4fe8eda0559432cef8cd58bc50faa1ed1"
    },
    "k29": {
        "at15m-run1-k29.out.csv": "b7e2d3c78ba07a94aefc3305a7ddeed136e95fd460530dfa3066a30abe391428",
        "at15m-run2-k29.out.csv": "b7e2d3c78ba07a94aefc3305a7ddeed136e95fd460530dfa3066a30abe391428",
        "at2m-k29.out.csv": "bf4d012246b6c830399f6f153610d8fe1edc77521cad33b7dfdd2c43ff7b76f0"
    },
    "k30": {
        "at15m-run1-k30.out.csv": "69a156a55a86e302f80bee81a36d144af7b48934402baaba315bf892689a550d",
        "at15m-run2-k30.out.csv": "43ddd5818ba82c09726e6780beefc5d35874482bf276d831805d253de579475a",
        "at2m-k30.out.csv": "8af30f012f8b28a267215f95aae3a78d761d27550fe74ab69fdc6d455938cca3"
    },
    "k31": {
        "at15m-run1-k31.out.csv": "6dddbe547438e9726e532bcddbd9c8e9327635418cf03697e95dfccdfda551b3",
        "at15m-run2-k31.out.csv": "6dddbe547438e9726e532bcddbd9c8e9327635418cf03697e95dfccdfda551b3",
        "at2m-k31.out.csv": "807d45296efddf7df344d27a9a5c6fe3762eda3c3ee47cd97ab47171d3cbd7d8"
    },
    "k32": {
        "at2m-k32.out.csv": "8c8ebb3eb42da60e57bde403cc0dfe15c72f256b526a6c4c73e42722bc668312",
        "at2m-run2-k32.out.csv": "8c8ebb3eb42da60e57bde403cc0dfe15c72f256b526a6c4c73e42722bc668312"
    },
    "k34": {
        "at15m-run1-k34.out.csv": "c0de8c6a0df4e6bb33eadcbc8bd7aa89f8df3ced8d65d12a34e8544a7233ffb2",
        "at15m-run2-k34.out.csv": "8021ec79348e2467ab0b5f9760089ab3ec2b91d0bfdb81dd95bab42e73737313",
        "at2m-k34.out.csv": "2ce58086b3bfc0b487bd6e170c0480257cf8cf8c7793d251eb39d89d2d170d15"
    },
    "k35": {
        "at15m-run1-k35.out.csv": "7722a6488ab33017f9da9ff947d906264d6432019d3cc9040d733169cd98c57f",
        "at15m-run2-k35.out.csv": "95b1014485c87666913a5266b182e6d514628ae477096c5a9989ee18b806e52c",
        "at2m-k35.out.csv": "0101327dced0f46d4087c4aa631d2917de30bbfe6215cc7ea104fe64d0199201"
    },
    "k36": {
        "at15m-run1-k36.out.csv": "562ba346acc6a4e3da8d3f80ab61aebfc5738192983ff3924a98cce89053276e",
        "at15m-run2-k36.out.csv": "562ba346acc6a4e3da8d3f80ab61aebfc5738192983ff3924a98cce89053276e",
        "at2m-k36.out.csv": "4d535300bcbc168b9478b9cde812ac0f581b19762bb1d17f969cdb2da3935c64"
    },
    "k37": {
        "at15m-run1-k37.out.csv": "eb00397435727be266f9783871e3932cd8c7a0ecd9a27585dbfa77b1411c2265",
        "at15m-run2-k37.out.csv": "c07990271dba7346c280fd6ed70bb8facb119916d5ab12fa3ae7933c7f0a325d",
        "at2m-k37.out.csv": "de8fcc1ed30fa40a319ec61dd9c01f657fb5e81ce617b0c6d8ab71534581762f"
    },
    "k39": {
        "at15m-run1-k39.out.csv": "af3bb4c3513561c1760c7aa774b9d2ee984930d3dd1e4ce7ba4ba2ae60f49ee0",
        "at15m-run2-k39.out.csv": "af3bb4c3513561c1760c7aa774b9d2ee984930d3dd1e4ce7ba4ba2ae60f49ee0",
        "at2m-k39.out.csv": "a7951d82df52cd7dc2aeabea6882f21a245e846281335d7c2740c0edba407130"
    },
    "k40": {
        "at15m-run1-k40.out.csv": "9dc4b27ecd03bcaeb0bd58475700a273a63d9b2a4ea47d33c4ce4542e6ea592b",
        "at15m-run2-k40.out.csv": "7a6d41d848ec2e32e28a30e387a93bbbbad426bb5670cf39a10d962e544084e6",
        "at2m-k40.out.csv": "643406dccb4b66c6b6e2153a2fef5b60120b5d49dc648066ddd9a8ed0865c44b"
    },
    "k41": {
        "at15m-run1-k41.out.csv": "542ca03402b81721f4a529d14dd240017d4fd81836f8ce458009c0bbbf6bddfd",
        "at15m-run2-k41.out.csv": "542ca03402b81721f4a529d14dd240017d4fd81836f8ce458009c0bbbf6bddfd",
        "at2m-k41.out.csv": "1b613c597a42a50a81beb6b2911f9b60493de64ab3b301b3db3f3a7ffe93ac80"
    },
    "k42": {
        "at15m-run1-k42.out.csv": "f1fab0ea787967329db92b3e9d81606ba5af7756ca7b195188599b0540313503",
        "at15m-run2-k42.out.csv": "a810cda5cb75e9cef92d8ec70a94e58c337a4f614a0e084c9d4beff8a12cac0c",
        "at2m-k42.out.csv": "61cf72b7071e4c4cc6a0d36f3d3d2660cdb0fc4b743b3afbe365ae4be92b61c9"
    },
    "k43": {
        "at15m-run1-k43.out.csv": "78668844f8c0b33d5baf5bac9d2cd49c7b047452a5b2464cf8024ed756f1c3dc",
        "at15m-run2-k43.out.csv": "78668844f8c0b33d5baf5bac9d2cd49c7b047452a5b2464cf8024ed756f1c3dc",
        "at2m-k43.out.csv": "7175fb05f2ffe544ff397b2288058934b4ecc381c33612d9ed23b7ee002cf434"
    }
}
TI_SUMMARY_ROWS = 32

ADOPTED_NODES_TOTAL = 181750115
STANDING_PARKED_KEYS = ["k38"]

# --- published outputs of this Part (self-pinned) -----------------------
MERGED_NAME = "merged-exact-s5-chain-plus-sixthloss30-20261126.cache"
MERGED_SHA_EXPECTED = "dade15780ce6625cc70d93ba77b1560145dd2b9f096a53dce556d2fccf7e312b"
MERGED_BYTES_EXPECTED = 285726
MERGED_ROWS_EXPECTED = 6831
MERGED_WIN_EXPECTED = 201
MERGED_LOSS_EXPECTED = 6630
MERGE_AUDIT_SHA_EXPECTED = "49a1891b4a3d5177ba55e84f0e69ac558208282cc96a6ad63d99895293b71b5e"

ADOPTED_TABLE_DIGEST = "f7379d0c955687164743ed1573d3bb6087d19a040ae94047fff36f0b1210d712"
ADOPTED_INCREMENT_SHA = "aa54956f2c4b4466e917f9c13802e630dd110890055b9243da3f44bf184445d6"
SERVING_CLASS = 3077
CLASS_MASK = (10376293541461626880, 65536)
PARK_BUDGET = 2000000
RESOLUTION_BUDGET = 15000000

INCREMENT_NAME = "increment-sixthloss30-adoption-20261126.cache"
SIXTHLOSS30_SCHEMA = "sixthloss30-adoption-increments-manifest-v1"

HDR_LINES = HDR = [
 "# n11 central-reply closure sixthloss30 canonical-adoption increment",
 "#   (Part ST, n11-centralreply-sixthloss30-adoption-reaudit-20261126,",
 "#   2026-11-26) - LOSS-only, fresh 30-row increment.  Part ST declares",
 "#   the sixthloss30 canonical LOSS adoption: the canonical head of",
 "#   record advances from merged-exact-s5-chain-plus-sixthwin3 (sha256",
 "#   02db5ab3..., 6,801 rows WIN 201 / LOSS 6,600; the Part SQ adoption",
 "#   head of record) to merged-exact-s5-chain-plus-sixthloss30 (6,831",
 "#   rows WIN 201 / LOSS 6,630) by consuming exactly the 30 unconsumed",
 "#   fifth-resumption resolved exact-LOSS rows of the sixth-cost class",
 "#   10376293541461626880:65536 probe selection (k09..k43 minus the",
 "#   adopted k13/k19/k20/k33 and the still-parked k38;",
 "#   exclusive_probe_order positions 9..43 minus 13/19/20/33/38).",
 "# The sources of record (all re-verified live by the Part maker against",
 "#   published bytes): the probe kit's primary cold two-pass node-exact",
 "#   resolution pairs (26 keys at 15,000,000 over the pinned 2,000,000",
 "#   park-at-UNKNOWN baselines; k17/k18 additionally resolved LOSS at",
 "#   the 2,000,000 stage with an at2m determinism pair; k28/k32 resolved",
 "#   LOSS at the 2,000,000 stage with an at2m determinism pair), the",
 "#   Part SR pinned C++ second-implementation scrutiny gate (33/33",
 "#   GATE-PASS, two fresh-cold passes per row, node-exact vs the",
 "#   published probe raws), and the k09..k43 resolved-32 third-",
 "#   implementation verdict re-verification addendum (verdict-level",
 "#   LOSS(2) agreement, 2 identical cold runs per row, auditor",
 "#   audit_k09k43.py re-run live 850/850; expansions legitimately",
 "#   differ from replica node counts - different implementations).",
 "#   Adopted node total 181,750,115 (bookkeeping, never verdicts).",
 "# Coverage-asymmetry disclosure: the still-parked key k38",
 "#   (10376293541461626880:66048) has a first-implementation L50M",
 "#   cold-pair LOSS row and a Part SS C++ second-implementation",
 "#   GATE-PASS but NO third-implementation corroboration; it stays",
 "#   standing unconsumed and is NOT adopted by this Part.",
 "# Every adopted key is fresh to BASE 02db5ab3... (loss_ties = []; no",
 "#   consumed row is re-adopted), quarantine-free, canonical-safe per",
 "#   s5_evidence_policy, and owned by serving class 3077 at graph time.",
 "# LOSS-only adoption asserts NO root verdict, frees NO class and",
 "#   excludes NO class (loss-only adoption flips no status; the EM",
 "#   precedent); the measured census delta is zero status flips with",
 "#   the serving class 3077 cost-unknown arithmetic and closure rank",
 "#   churn derived machine-only by the reaudit refresh and the census",
 "#   delta measurer; nodes are bookkeeping, never verdicts.  The",
 "#   standard 11x11 empty board and every central-reply root stay",
 "#   UNKNOWN.",
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
    txt = path.read_text()
    line = None
    for cand in txt.strip().splitlines():
        if cand.startswith("third,") or "GATE_FAIL" in cand:
            if line is not None:
                sys_exit(f"multiple third-impl rows in {path}")
            line = cand
    if line is None:
        sys_exit(f"no third-impl raw row in {path}")
    parts = line.split(",")
    if parts[5] == "GATE_FAIL":
        return {"gate_fail": True, "text": txt}
    if len(parts) != 15 or parts[0] != "third":
        sys_exit(f"malformed third-impl raw row in {path}")
    kv = dict(x.split("=", 1) for x in parts[12:15])
    return {
        "gate_fail": False,
        "row": parts[1], "stones": int(parts[2]),
        "legal_in": int(parts[3]), "legal_derived": int(parts[4]),
        "result": int(parts[5]),
        "expansions": int(parts[6]),
        "tt_hits": int(parts[7]), "lo": parts[9], "hi": parts[10],
        "reason": parts[11], "quads": kv["quads"],
        "ttoverwrites": int(kv["ttOverwrites"]),
        "memopower": int(kv["memoPower"]),
    }


def payload_eq(a: dict, b: dict, what: str):
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes",
              "lo", "hi")
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
    # --- anchors: base cache, merger, quarantine, policy, graph ---------
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys_exit("base cache (Part SQ head of record) sha drift")
    if sha(ROOT / "research/experiments" / SQ_EXP
           / "scripts/s5_union_merge.py") != MERGER_SHA_EXPECTED:
        sys_exit("pinned union merger (Part SQ kit scripts/s5_union_merge.py) "
                 "sha drift")
    if sha(EXP / "scripts/s5_union_merge.py") != MERGER_SHA_EXPECTED:
        sys_exit("this kit's merger clone sha drift")
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
        sys_exit(f"base cache rows {len(base_keys)} != "
                 f"{BASE_CACHE_ROWS_EXPECTED}")
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

    # --- probe kit selection JSON (order positions of the keys) --------
    if not PROBE_DIR.is_dir():
        sys_exit(f"probe kit dir missing {PROBE_DIR}")
    sel_path = PROBE_DIR / "output/sixth-cost-exclusive-keys.json"
    if sha(sel_path) != PROBE_SELECTION_SHA:
        sys_exit("probe kit selection JSON sha drift")
    sel = json.loads(sel_path.read_text())
    if sel["schema"] != "n11-sixthcost-exclusive-selection-v1":
        sys_exit("probe selection schema drift")
    if sel["class"] != f"{CLASS_MASK[0]}:{CLASS_MASK[1]}":
        sys_exit("probe selection class drift")
    if sel["class_children_total"] != 108 or sel["s5_unknown_before"] != 101:
        sys_exit("probe selection class census drift")
    if sel["unknown_exclusive"] != 43 or len(sel["exclusive_probe_order"]) != 43:
        sys_exit("probe selection exclusive list drift")
    adopted_key_strs = [f"{ADOPTED_KEY_PINS[k][0]}:{ADOPTED_KEY_PINS[k][1]}"
                        for k in ADOPTED_IDS]
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, pos, _b, _n = ADOPTED_KEY_PINS[kid]
        entry = sel["exclusive_probe_order"][pos - 1]
        if entry["key"] != f"{lo}:{hi}" or entry["legal"] != legal:
            sys_exit(f"probe selection order-position disagreement: {kid}")

    # --- probe kit fifth-resumption raws (first implementation) --------
    praw = PROBE_DIR / "output/raw"
    probe_rows = {}
    at2m_loss_keys = []
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos, budget, nodes = ADOPTED_KEY_PINS[kid]
        p_budget, p_result, p_nodes = AT2M_PINS[kid]
        files = ADOPTED_RAW_SHAS[kid]
        for name, want in files.items():
            p = praw / name
            if not p.is_file():
                sys_exit(f"probe raw missing: {name}")
            if sha(p) != want:
                sys_exit(f"probe raw sha drift: {name}")
        at2m = parse_replay(praw / f"at2m-{kid}.out.csv")
        if (at2m["stones"], at2m["is_or"], at2m["budget"]) != (5, 0, PARK_BUDGET):
            sys_exit(f"{kid}: at2m stage depth/or/budget drift")
        if at2m["legal"] != legal or at2m["lo"] != str(lo) \
                or at2m["hi"] != str(hi):
            sys_exit(f"{kid}: at2m key/legal drift")
        if (at2m["result"], at2m["nodes"]) != (p_result, p_nodes):
            sys_exit(f"{kid}: at2m park/loss stage payload drift")
        if (p_result, p_nodes) == (0, PARK_BUDGET):
            # standard 26 keys: park baseline + cold two-pass 15M resolution
            if f"at2m-run2-{kid}.out.csv" in files:
                sys_exit(f"{kid}: park key must not carry an at2m determinism "
                         "pair")
            if budget != RESOLUTION_BUDGET:
                sys_exit(f"{kid}: resolution budget drift (park key)")
            r1 = parse_replay(praw / f"at15m-run1-{kid}.out.csv")
            r2 = parse_replay(praw / f"at15m-run2-{kid}.out.csv")
            for r, tag in ((r1, "run1"), (r2, "run2")):
                if (r["stones"], r["is_or"], r["budget"]) != (5, 0, budget):
                    sys_exit(f"{kid}: 15M stage depth/or/budget drift ({tag})")
                if r["legal"] != legal or r["lo"] != str(lo) \
                        or r["hi"] != str(hi):
                    sys_exit(f"{kid}: legal/key disagreement raw vs pinned "
                             f"({tag})")
                if (r["result"], r["nodes"]) != (2, nodes):
                    sys_exit(f"{kid}: honest-label drift vs pinned label "
                             f"({tag})")
            payload_eq(r1, r2, f"{kid} at15m")
            probe_rows[kid] = r1
        else:
            # k17/k18/k28/k32: LOSS resolved already at the 2M stage with
            # an at2m determinism pair
            at2m_run2 = parse_replay(praw / f"at2m-run2-{kid}.out.csv")
            payload_eq(at2m, at2m_run2, f"{kid} at2m pair")
            if (at2m["result"], at2m["nodes"]) != (2, p_nodes):
                sys_exit(f"{kid}: at2m LOSS stage drift")
            at2m_loss_keys.append(kid)
            if budget == PARK_BUDGET:
                # k28/k32: the 2M pair IS the resolution of record
                probe_rows[kid] = at2m
                if f"at15m-run1-{kid}.out.csv" in files:
                    sys_exit(f"{kid}: 2M-resolution key must not carry 15M "
                             "resolution raws")
            else:
                # k17/k18: additionally resolved at 15M (resolution of
                # record), gated like the standard keys
                r1 = parse_replay(praw / f"at15m-run1-{kid}.out.csv")
                r2 = parse_replay(praw / f"at15m-run2-{kid}.out.csv")
                for r, tag in ((r1, "run1"), (r2, "run2")):
                    if (r["stones"], r["is_or"], r["budget"]) != (5, 0, budget):
                        sys_exit(f"{kid}: 15M stage depth/or/budget drift "
                                 f"({tag})")
                    if r["legal"] != legal or r["lo"] != str(lo) \
                            or r["hi"] != str(hi):
                        sys_exit(f"{kid}: legal/key disagreement raw vs "
                                 f"pinned ({tag})")
                    if (r["result"], r["nodes"]) != (2, nodes):
                        sys_exit(f"{kid}: honest-label drift vs pinned label "
                                 f"({tag})")
                payload_eq(r1, r2, f"{kid} at15m")
                probe_rows[kid] = r1
    if sorted(at2m_loss_keys) != ["k17", "k18", "k28", "k32"]:
        sys_exit(f"at2m LOSS stage structure drift: {sorted(at2m_loss_keys)}")
    adopted_nodes = sum(ADOPTED_KEY_PINS[k][6] for k in ADOPTED_IDS)
    if adopted_nodes != ADOPTED_NODES_TOTAL:
        sys_exit(f"adopted node total drift {adopted_nodes} != "
                 f"{ADOPTED_NODES_TOTAL}")

    # --- Part SR pinned C++ second-implementation gate kit -------------
    if not SR_DIR.is_dir():
        sys_exit(f"Part SR kit dir missing {SR_DIR}")
    if sha(SR_DIR / "MANIFEST-sha256.txt") != SR_MANIFEST_SHA:
        sys_exit("Part SR kit MANIFEST sha drift")
    sr_manifest = load_manifest_2field(SR_DIR / "MANIFEST-sha256.txt",
                                       "Part SR")
    if len(sr_manifest) != SR_KIT_FILES:
        sys_exit(f"Part SR kit files verified {len(sr_manifest)} != "
                 f"{SR_KIT_FILES}")
    for rel, want in sr_manifest.items():
        p = SR_DIR / rel
        if not p.is_file():
            sys_exit(f"Part SR kit file missing: {rel}")
        if sha(p) != want:
            sys_exit(f"Part SR kit file sha drift: {rel}")
    if sr_manifest.get("README.md") != SR_README_SHA:
        sys_exit("Part SR kit README pin drift")
    if sr_manifest.get("input/gate-rows.json") != SR_GATEROWS_SHA:
        sys_exit("Part SR gate-rows manifest pin drift")
    if sr_manifest.get("output/gate-status.log") != SR_STATUS_SHA:
        sys_exit("Part SR gate-status manifest pin drift")
    for rel in ("output/audit_gate.json", "output/audit_gate.run1.json",
                "output/audit_gate.run2.json", "output/audit_gate.run3.json"):
        if sr_manifest.get(rel) != SR_AUDIT_SHA:
            sys_exit(f"Part SR audit json manifest pin drift: {rel}")
    if sr_manifest.get("scripts/audit_gate.py") != SR_AUDIT_PY_SHA:
        sys_exit("Part SR audit_gate.py manifest pin drift")
    if sr_manifest.get("tamper.log") != SR_TAMPER_SHA:
        sys_exit("Part SR tamper battery log manifest pin drift")
    if sr_manifest.get("t1_result.json") != SR_T1_RESULT_SHA:
        sys_exit("Part SR t1_result.json manifest pin drift")

    # gate-rows.json: the machine-derived pin table of the C++ gate
    if sha(SR_DIR / "input/gate-rows.json") != SR_GATEROWS_SHA:
        sys_exit("Part SR gate-rows.json sha drift")
    gr = json.loads((SR_DIR / "input/gate-rows.json").read_text())
    if gr["schema"] != "n11-sixthcost-fifthres30-cppgate-rows-v1":
        sys_exit("Part SR gate-rows schema drift")
    if gr["part"] != "SR":
        sys_exit("Part SR gate-rows part drift")
    gs = gr["gate_source"]
    if gs["path"] != "cpp/solvers/kyouen_dfpn_root.cpp" \
            or gs["sha256"] != SR_CPP_SHA or gs["commit"] != SR_CPP_COMMIT \
            or gs["header_pins"] != SR_HEADER_PINS:
        sys_exit("Part SR gate-rows gate-source block drift")
    ch = gr["canonical_head"]
    if (ch["label"] != "02db5ab3"
            or ch["sha256"] != BASE_CACHE_SHA_EXPECTED
            or ch["rows"] != BASE_CACHE_ROWS_EXPECTED
            or ch["WIN"] != BASE_CACHE_WIN_EXPECTED
            or ch["LOSS"] != BASE_CACHE_LOSS_EXPECTED
            or ch["targets_fresh_vs"] != "02db5ab3"
            or ch["path"] != "research/experiments/" + SQ_EXP
            + "/output/merged-exact-s5-chain-plus-sixthwin3-20261126.cache"):
        sys_exit("Part SR gate-rows canonical-head block drift")
    if gr["anchors"] != {k: f"{v[0]},{v[1]},{v[2]},{v[3]}"
                         for k, v in SR_ANCHOR_PINS.items()}:
        sys_exit("Part SR gate-rows anchor pin drift")
    if gr["anchors_runtime"] != SR_ANCHORS_RUNTIME:
        sys_exit("Part SR gate-rows anchors_runtime drift")
    tib = gr["third_impl"]
    if (tib["exists"] is not True or tib["all_pass"] is not True
            or tib["rows_audited"] != TI_SUMMARY_ROWS
            or tib["schema"] != "n11-sixthcost-k09k43-thirdimpl-batch-audit-v2"
            or tib["verdict_level_corroboration"] is not True):
        sys_exit("Part SR gate-rows third_impl block drift")
    if len(gr["gates"]) != SR_GATES_TOTAL or any(
            v["status"] != "PASS" for v in gr["gates"].values()):
        sys_exit("Part SR gate-rows gate table not all PASS")
    if sorted(gr["targets"]) != sorted(ADOPTED_IDS):
        sys_exit("Part SR gate-rows target set drift")
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos, budget, nodes = ADOPTED_KEY_PINS[kid]
        t = gr["targets"][kid]
        expected = f"{legal},{budget},2,{nodes}"
        if (t["lo"], t["hi"], t["budget"], t["expected"]) != \
                (str(lo), str(hi), str(budget), expected):
            sys_exit(f"Part SR gate-rows target drift: {kid}")
        if t["replica_verdict"] != 2 or t["third_impl_verdict"] != 2:
            sys_exit(f"Part SR gate-rows verdict flags drift: {kid}")
        # raw provenance must point at the probe kit's resolution raw
        if budget == RESOLUTION_BUDGET:
            want_prov = ("research/experiments/" + PROBE_EXP
                         + f"/output/raw/at15m-run1-{kid}.out.csv")
        else:
            want_prov = ("research/experiments/" + PROBE_EXP
                         + f"/output/raw/at2m-{kid}.out.csv")
        if t["raw_provenance"] != want_prov:
            sys_exit(f"Part SR gate-rows raw provenance drift: {kid}")
        # input CSV cross-registration vs the third-impl kit SSOT input
        inp = SR_DIR / f"input/{kid}.input.csv"
        if sha(inp) != t["input_sha256"]:
            sys_exit(f"Part SR gate input sha vs gate-rows pin drift: {kid}")
        if (TI_DIR / f"input/{kid}.input.csv").read_bytes() != \
                inp.read_bytes():
            sys_exit(f"{kid}: SR gate input CSV is not byte-equal to the "
                     "third-impl kit input (cross-registration)")
    for name in SR_ANCHOR_PINS:
        if f"input/{name}.input.csv" not in sr_manifest:
            sys_exit(f"Part SR anchor input manifest pin drift: {name}")

    # gate-status.log: 33 GATE-PASS rows (3 anchors + 30 targets)
    gk_map = {}
    for line in (SR_DIR / "output/gate-status.log").read_text().splitlines():
        parts = line.split()
        if len(parts) < 4 or parts[2] != "GATE-PASS" \
                or not parts[3].replace(",", "").isdigit():
            sys_exit(f"Part SR gate-status unexpected line: {line}")
        gk_map[parts[1]] = parts[3]
    if len(gk_map) != SR_GATE_STATUS_ROWS:
        sys_exit("Part SR gate-status must carry exactly 33 GATE-PASS rows")
    for name, (legal_v, budget_v, res_v, nodes_v) in SR_ANCHOR_PINS.items():
        if gk_map.get(name) != f"{legal_v},{budget_v},{res_v},{nodes_v}":
            sys_exit(f"Part SR gate-status anchor row drift: {name}")
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos, budget, nodes = ADOPTED_KEY_PINS[kid]
        if gk_map.get(kid) != f"{legal},{budget},2,{nodes}":
            sys_exit(f"Part SR gate-status row drift: {kid}")

    # audit_gate.json + run1/2/3: byte-identical, field-gated
    for i in ("", ".run1", ".run2", ".run3"):
        if sha(SR_DIR / f"output/audit_gate{i}.json") != SR_AUDIT_SHA:
            sys_exit(f"Part SR audit_gate{i}.json sha drift")
    ag = json.loads((SR_DIR / "output/audit_gate.json").read_text())
    if ag["overall"] != "PASS" or ag["part"] != "SR":
        sys_exit("Part SR audit_gate.json overall/part drift")
    if len(ag["rows"]) != SR_GATE_STATUS_ROWS:
        sys_exit("Part SR audit_gate rows census drift")
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos, budget, nodes = ADOPTED_KEY_PINS[kid]
        row = ag["rows"].get(kid)
        exp = f"{legal},{budget},2,{nodes}"
        if row is None or row["expected"] != exp \
                or row["observed_p1"] != exp or row["budget"] != str(budget):
            sys_exit(f"Part SR audit_gate row drift: {kid}")
    for name, (legal_v, budget_v, res_v, nodes_v) in SR_ANCHOR_PINS.items():
        row = ag["rows"].get(name)
        exp = f"{legal_v},{budget_v},{res_v},{nodes_v}"
        if row is None or row["expected"] != exp \
                or row["observed_p1"] != exp:
            sys_exit(f"Part SR audit_gate anchor row drift: {name}")

    # SR C++ gate raw payload gates (p1/p2 fresh-cold passes per row)
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos, budget, nodes = ADOPTED_KEY_PINS[kid]
        s1 = parse_replay(SR_DIR / f"output/raw/{kid}.p1.out")
        s2 = parse_replay(SR_DIR / f"output/raw/{kid}.p2.out")
        payload_eq(s1, s2, f"SR {kid}")
        if (s1["stones"], s1["is_or"], s1["budget"], s1["result"],
                s1["nodes"]) != (5, 0, budget, 2, nodes):
            sys_exit(f"{kid}: SR C++ gate honest-label drift")
        if s1["legal"] != legal or s1["lo"] != str(lo) or s1["hi"] != str(hi):
            sys_exit(f"{kid}: SR C++ gate legal/key drift")
        ref = probe_rows[kid]
        if (ref["result"], ref["nodes"]) != (s1["result"], s1["nodes"]):
            sys_exit(f"{kid}: SR C++ gate vs published raw node-exact drift")
    for name, (legal_v, budget_v, res_v, nodes_v) in SR_ANCHOR_PINS.items():
        a1 = parse_replay(SR_DIR / f"output/raw/{name}.p1.out")
        a2 = parse_replay(SR_DIR / f"output/raw/{name}.p2.out")
        payload_eq(a1, a2, f"SR {name}")
        if (a1["stones"], a1["is_or"], a1["legal"], a1["budget"],
                a1["result"], a1["nodes"]) != (5, 0, legal_v, budget_v,
                                               res_v, nodes_v):
            sys_exit(f"{name}: SR C++ gate anchor-label drift")

    # SR kit tamper battery + t1 fail-closed record
    tam = (SR_DIR / "tamper.log").read_text()
    for needle in ("T1-START", "T1 audit rc=1 (expected 1)",
                   "T2-START", "T2 audit rc=1 (expected 1)",
                   "T3-START", "T3 audit rc=1 (expected 1)",
                   "CLEAN-CONTROL audit rc=0 (expected 0)", "BATTERY-END"):
        if needle not in tam:
            sys_exit(f"Part SR tamper battery log missing: {needle}")
    t1 = json.loads((SR_DIR / "t1_result.json").read_text())
    if "t1" not in t1 or "g3_k09" not in t1["t1"] \
            or t1["t1"]["g3_k09"]["status"] != "FAIL":
        sys_exit("Part SR t1_result.json fail-closed record drift")
    # LIVE re-run of the kit's own audit (self-contained, PASS required)
    proc = subprocess.run([sys.executable, "audit_gate.py"],
                          cwd=str(SR_DIR / "scripts"),
                          capture_output=True, text=True)
    if proc.returncode != 0 or "audit_gate: PASS" not in proc.stdout:
        sys_exit("live Part SR audit_gate.py re-run failed closed "
                 f"rc={proc.returncode}: {proc.stdout[-400:]}")

    # --- k09..k43 resolved-32 third-impl verdict addendum --------------
    if not TI_DIR.is_dir():
        sys_exit(f"third-impl kit dir missing {TI_DIR}")
    if sha(TI_DIR / "audit_k09k43.py") != TI_AUDITOR_SHA:
        sys_exit("k09k43 third-impl auditor sha drift")
    if sha(TI_DIR / "third_impl.js") != TI_THIRD_IMPL_SHA:
        sys_exit("third_impl.js sha drift")
    if sha(TI_DIR / "verify_tbl.js") != TI_VERIFY_TBL_SHA:
        sys_exit("verify_tbl.js sha drift")
    if sha(TI_DIR / "out/audit-k09k43-summary.json") != TI_SUMMARY_SHA:
        sys_exit("k09k43 third-impl summary sha drift")
    if sha(TI_DIR / "out/audit-tamper-controls-k09k43.txt") != \
            TI_TAMPER_LOG_SHA:
        sys_exit("k09k43 third-impl tamper-controls log sha drift")
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos, _b, nodes = ADOPTED_KEY_PINS[kid]
        # cold a/b: verdict-level LOSS agreement + determinism pair
        cold = {}
        for tag, fname in (("a", f"{kid}-cold-a.txt"),
                           ("b", f"{kid}-cold-b.txt")):
            p = TI_DIR / f"out/{fname}"
            if sha(p) != TI_COLD_PINS[kid][tag][0]:
                sys_exit(f"third-impl cold raw sha drift: {fname}")
            cold[tag] = parse_third(p)
        qa = (cold["a"]["result"], cold["a"]["expansions"],
              cold["a"]["tt_hits"], cold["a"]["ttoverwrites"])
        qb = (cold["b"]["result"], cold["b"]["expansions"],
              cold["b"]["tt_hits"], cold["b"]["ttoverwrites"])
        if qa != qb:
            sys_exit(f"{kid}: third-impl determinism pair drift")
        want = (2, TI_COLD_PINS[kid]["a"][1], TI_COLD_PINS[kid]["a"][2],
                TI_COLD_PINS[kid]["a"][3])
        if qa != want:
            sys_exit(f"{kid}: third-impl honest-label drift vs pinned "
                     "quadruple")
        for t in ("a", "b"):
            d = cold[t]
            if d["gate_fail"] or d["reason"] != "clean" \
                    or d["stones"] != 5 or d["legal_in"] != legal \
                    or d["legal_derived"] != legal \
                    or d["lo"] != str(lo) or d["hi"] != str(hi) \
                    or d["quads"] != "95670" or d["memopower"] != 22:
                sys_exit(f"{kid}: third-impl cold run field drift ({t})")
            if d["expansions"] == nodes:
                sys_exit(f"{kid}: anti-copy gate (expansions == replica "
                         "nodes)")
        # replica-raw copies re-published inside the addendum must be
        # byte-equal to the probe kit raws (self-contained auditor)
        for stage_name, probe_name in ADOPTED_RAW_SHAS[kid].items():
            p = TI_DIR / f"out/{kid}-replica-raws/{stage_name}"
            if not p.is_file():
                sys_exit(f"{kid}: third-impl replica copy missing: "
                         f"{stage_name}")
            if sha(p) != TI_REPLICA_SHAS[kid][stage_name]:
                sys_exit(f"{kid}: third-impl replica pin drift: {stage_name}")
            if sha(p) != ADOPTED_RAW_SHAS[kid][stage_name]:
                sys_exit(f"{kid}: third-impl replica copy != probe kit raw "
                         f"(cross-registration): {stage_name}")
        # negative gates: 2 per key, fail-closed GATE_FAIL raws
        negs = [n for n in TI_NEG_SHAS if n.startswith(f"neg-gate-{kid}-")]
        if len(negs) != 2:
            sys_exit(f"{kid}: expected exactly 2 negative-gate raws")
        for n in negs:
            p = TI_DIR / f"out/{n}"
            if sha(p) != TI_NEG_SHAS[n]:
                sys_exit(f"third-impl negative-gate raw sha drift: {n}")
            d = parse_third(p)
            if not d["gate_fail"] or "mismatch" not in d["text"]:
                sys_exit(f"third-impl negative-gate payload drift: {n}")

    # published summary: 32 audited rows, all verdict-level agreements
    summ = json.loads((TI_DIR / "out/audit-k09k43-summary.json").read_text())
    if summ["schema"] != "n11-sixthcost-k09k43-thirdimpl-batch-audit-v2" \
            or summ["all_pass"] is not True \
            or summ["rows_audited"] != TI_SUMMARY_ROWS \
            or summ["rows_expected"] != TI_SUMMARY_ROWS \
            or summ["consumed"] is not False:
        sys_exit("k09k43 third-impl summary block drift")
    if len(summ["row_results"]) != TI_SUMMARY_ROWS:
        sys_exit("k09k43 third-impl summary row_results census drift")
    for kid in ADOPTED_IDS:
        lo, hi, legal, _s5, _pos, budget, nodes = ADOPTED_KEY_PINS[kid]
        rr = summ["row_results"][kid]
        if rr["key"] != f"{lo}:{hi}" or rr["legal"] != legal \
                or rr["replica_verdict"] != 2 or rr["third_impl_verdict"] != 2 \
                or rr["verdict_level_agreement"] is not True \
                or rr["determinism_identical"] is not True \
                or rr["third_impl_runs"] != 2 \
                or rr["replica_resolution_nodes"] != nodes \
                or rr["third_impl_expansions"] != TI_COLD_PINS[kid]["a"][1] \
                or rr["third_impl_tt_hits"] != TI_COLD_PINS[kid]["a"][2]:
            sys_exit(f"k09k43 third-impl summary row drift: {kid}")
        want_stage = ("loss2m" if budget == PARK_BUDGET
                      else ("loss2m15m" if kid in ("k17", "k18")
                            else "loss15"))
        if rr["replica_stage"] != want_stage:
            sys_exit(f"{kid}: third-impl summary replica_stage drift")

    # LIVE re-run of the published data-driven auditor (850/850 gates,
    # deterministic byte-identical stdout across two executions)
    audit_stdouts = []
    for _ in range(2):
        proc = subprocess.run([sys.executable, "audit_k09k43.py"],
                              cwd=str(TI_DIR), capture_output=True, text=True)
        if proc.returncode != 0:
            sys_exit("live audit_k09k43.py re-run failed closed "
                     f"rc={proc.returncode}: {proc.stdout[-400:]}")
        live = json.loads(proc.stdout)
        if live["all_pass"] is not True or len(live["gates"]) != 850 \
                or any(not gv["pass"] for gv in live["gates"].values()) \
                or live["rows_audited"] != TI_SUMMARY_ROWS:
            sys_exit("live audit_k09k43.py gate accounting drift")
        audit_stdouts.append(proc.stdout)
    if audit_stdouts[0] != audit_stdouts[1]:
        sys_exit("live audit_k09k43.py non-deterministic stdout")

    # --- freshness: BASE absence, quarantine, canonical safety ---------
    adopted_rows = []
    for kid in ADOPTED_IDS:
        ref = probe_rows[kid]
        if ref["result"] != 2:
            sys_exit(f"{kid}: adopted row must be exact LOSS")
        lo, hi, legal, s5_index, _pos, _b, _n = ADOPTED_KEY_PINS[kid]
        if (int(ref["lo"]), int(ref["hi"])) != (lo, hi):
            sys_exit(f"{kid}: raw key vs pinned key disagreement")
        if ref["legal"] != legal:
            sys_exit(f"{kid}: raw legal vs pinned legal disagreement")
        if mask_to_index.get((lo, hi)) != s5_index:
            sys_exit(f"{kid}: s5_index round-trip drift vs the frozen graph")
        owners = [ci for ci in range(len(s4_masks))
                  if s5_index in s4_cost[ci]]
        if SERVING_CLASS not in owners:
            sys_exit(f"{kid}: serving class must own the key at graph time")
        if ref["nodes"] != ADOPTED_KEY_PINS[kid][6]:
            sys_exit(f"{kid}: node drift")
        key = (lo, hi)
        if key in quarantined:
            sys_exit(f"{kid}: quarantined key {key}")
        if not is_canonical_safe_s5_key(key):
            sys_exit(f"{kid}: noncanonical/unsafe key {key}")
        if key in base_keys:
            sys_exit(f"{kid}: key already in canonical BASE; "
                     "fresh-increment gate")
        adopted_rows.append((lo, hi, legal, 2, ref["nodes"], s5_index,
                             SERVING_CLASS, owners))
    if len({(r[0], r[1]) for r in adopted_rows}) != 30:
        sys_exit("adopted pairs must be exactly 30 distinct keys")

    digest = hashlib.sha256("\n".join(
        f"{lo},{hi},{legal},{result},{nodes}"
        for lo, hi, legal, result, nodes, _s5, _cls, _own in
        sorted(adopted_rows)).encode()).hexdigest()
    if digest != ADOPTED_TABLE_DIGEST:
        sys_exit(f"adopted-table digest drift {digest}")

    # --- self-publication gates: merged head of record + merge audits ---
    if sha(OUT / MERGED_NAME) != MERGED_SHA_EXPECTED:
        sys_exit("published merged cache of record sha drift")
    if (OUT / MERGED_NAME).stat().st_size != MERGED_BYTES_EXPECTED:
        sys_exit("published merged cache of record byte-size drift")
    merged_rows = 0
    merged_wins = 0
    merged_loss = 0
    for line in (OUT / MERGED_NAME).read_text(encoding="utf-8-sig") \
            .splitlines():
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
    if (merged_rows, merged_wins, merged_loss) != (MERGED_ROWS_EXPECTED,
                                                   MERGED_WIN_EXPECTED,
                                                   MERGED_LOSS_EXPECTED):
        sys_exit(f"merged cache of record census drift {merged_rows}/"
                 f"{merged_wins}/{merged_loss}")
    if merged_loss - BASE_CACHE_LOSS_EXPECTED != 30 \
            or merged_wins != BASE_CACHE_WIN_EXPECTED:
        sys_exit("merged cache delta must be exactly the 30 adopted LOSS "
                 "rows (WIN unchanged)")
    for i in (1, 2, 3):
        if sha(OUT / f"merge-audit-run{i}.json") != \
                MERGE_AUDIT_SHA_EXPECTED:
            sys_exit(f"merge-audit-run{i}.json sha drift")
    ma = json.loads((OUT / "merge-audit-run1.json").read_text())
    if ma["tool"] != "s5_union_merge.py" \
            or ma["output_sha256"] != MERGED_SHA_EXPECTED \
            or ma["output_bytes"] != MERGED_BYTES_EXPECTED \
            or ma["unique_rows"] != MERGED_ROWS_EXPECTED \
            or ma["duplicate_rows_elided"] != 0 \
            or ma["verdict_counts"] != {"WIN(1)": MERGED_WIN_EXPECTED,
                                        "LOSS(2)": MERGED_LOSS_EXPECTED} \
            or ma["nodes_field_mismatches_recorded"] != []:
        sys_exit("merge-audit record field drift")
    if ma["inputs"][0]["sha256"] != BASE_CACHE_SHA_EXPECTED \
            or ma["inputs"][0]["rows"] != BASE_CACHE_ROWS_EXPECTED \
            or ma["inputs"][0]["unique_new"] != BASE_CACHE_ROWS_EXPECTED:
        sys_exit("merge-audit base input accounting drift")
    if ma["inputs"][1]["sha256"] != ADOPTED_INCREMENT_SHA \
            or ma["inputs"][1]["rows"] != 30 \
            or ma["inputs"][1]["unique_new"] != 30:
        sys_exit("merge-audit increment input accounting drift")
    if "11x11 root questions remain UNKNOWN" not in \
            ma["interpretation_guard"]:
        sys_exit("merge-audit interpretation guard drift")

    # --- emit increment + manifest --------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    rowlines = [f"s5verdict,{lo},{hi},5,2,{nodes}"
                for lo, hi, legal, result, nodes, _s5, _cls, _own
                in sorted(adopted_rows)]
    for line in rowlines:
        f = line.split(",")
        lo, hi, result, nodes = int(f[1]), int(f[2]), int(f[4]), int(f[5])
        if (lo, hi, nodes) not in {(r[0], r[1], r[4]) for r in adopted_rows}:
            sys_exit("emit-order row not in the gated adopted table")
    if len(rowlines) != 30:
        sys_exit("emitted row count drift")
    blob = ("\n".join(HDR_LINES + rowlines) + "\n").encode("utf-8")
    incr_sha = hashlib.sha256(blob).hexdigest()
    if incr_sha != ADOPTED_INCREMENT_SHA:
        sys_exit(f"emitted increment sha drift {incr_sha} != pinned "
                 f"{ADOPTED_INCREMENT_SHA}")
    existing = OUT / INCREMENT_NAME
    if existing.is_file() and existing.read_bytes() != blob:
        sys_exit("on-disk increment differs from the emitted blob")
    with (OUT / INCREMENT_NAME).open("wb") as f:
        f.write(blob)
        f.flush()
        import os as _os
        _os.fsync(f.fileno())
        _dfd = _os.open(str(OUT), _os.O_RDONLY)
        try:
            _os.fsync(_dfd)
        finally:
            _os.close(_dfd)

    adopted_table = [
        {"lo": lo, "hi": hi, "legal": legal, "result": 2, "nodes": nodes,
         "s5_index": s5_index, "serving_class": serving_class,
         "owner_classes_graph": owners}
        for lo, hi, legal, result, nodes, s5_index, serving_class, owners
        in sorted(adopted_rows)]

    manifest = {
        "schema": SIXTHLOSS30_SCHEMA,
        "part": "ST",
        "date": "2026-11-26",
        "loss_canonical_adoption": True,
        "canonical_head_published_by_this_part": {
            "merged_cache_name": MERGED_NAME,
            "merged_cache_sha256": MERGED_SHA_EXPECTED,
            "merged_cache_bytes": MERGED_BYTES_EXPECTED,
            "merged_cache_rows": MERGED_ROWS_EXPECTED,
            "merged_cache_win_loss": [MERGED_WIN_EXPECTED,
                                      MERGED_LOSS_EXPECTED],
            "merge_audit_runs": 3,
            "merge_audit_sha256_x3_identical": MERGE_AUDIT_SHA_EXPECTED,
            "merger": "pinned byte-clone of the published union merger "
                      "(sha256 90711961..., this kit scripts/s5_union_merge.py)",
            "note": "this Part ST publishes the merged head of record "
                    "itself at this kit's output/ directory; three "
                    "independent merge runs produced byte-identical "
                    "output and byte-identical audit records",
        },
        "source_class": {
            "class": f"{CLASS_MASK[0]}:{CLASS_MASK[1]}",
            "class_children_total": 108, "s5_unknown_before": 101,
            "unknown_exclusive": 43, "serving_class_index": SERVING_CLASS,
            "note": "the sixth-cost live candidate class (s4 class 3077, "
                    "coverage {80,84,100,108}); the 30 adopted keys are "
                    "positions 9..43 minus 13/19/20/33/38 of the same "
                    "published probe selection exclusive_probe_order of "
                    "record (d5e9b059...), resolved by the probe kit's "
                    "fifth-resumption runs over their pinned 2,000,000 "
                    "park-at-UNKNOWN baselines",
            "adoption_requirement_of_record":
                "the parent batch's pre-registered consumption gate: "
                "published C++ second-implementation verification "
                "(pinned cpp/solvers/kyouen_dfpn_root.cpp sha256 "
                "9193f5b6...) of every consumed raw row, satisfied for "
                "all 30 rows by the Part SR kit (GATE-PASS 33/33); any "
                "C++ disagreement fails closed in favor of discarding the "
                "row; third-implementation verdict-level corroboration "
                "(the k09..k43 resolved-32 addendum, auditor re-run live "
                "850/850) is additionally recorded for all 30 rows per "
                "the repo's adoption pattern; the still-parked k38 has NO "
                "third-impl corroboration and is NOT adopted",
        },
        "pools": [
            {"pool": "fifthres30-probe-raws",
             "kit": PROBE_EXP,
             "park_budget": PARK_BUDGET,
             "resolution_budget": RESOLUTION_BUDGET,
             "adopted_loss_ids": list(ADOPTED_IDS),
             "stage_structure": {
                 "park_at_2m_keys": 26,
                 "loss_at_2m_with_determinism_pair": ["k17", "k18",
                                                      "k28", "k32"],
                 "resolution_at_15m_keys": 28,
                 "resolution_at_2m_keys": ["k28", "k32"],
             },
             "adopted_nodes": ADOPTED_NODES_TOTAL,
             "kit_integrity": {
                 "note": "the probe kit's published fifth-resumption raws "
                         "are pinned directly per stage file (sha256 "
                         "pins in this maker; every stage payload-gated "
                         "against the pinned key/legal/budget/result/"
                         "nodes table with multi-pass determinism)",
                 "selection_json_sha256": PROBE_SELECTION_SHA,
                 "raw_file_sha256_pins": "in-maker (ADOPTED_RAW_SHAS)",
             }},
            {"pool": "sr-cpp-second-implementation-gate",
             "kit": SR_EXP,
             "kit_integrity": {
                 "note": "Part SR kit verified file-by-file against its "
                         "published MANIFEST-sha256 "
                         f"{SR_MANIFEST_SHA[:8]}... ({SR_KIT_FILES} files)",
                 "kit_manifest_sha256": SR_MANIFEST_SHA,
                 "kit_files_verified": SR_KIT_FILES,
                 "readme_sha256": SR_README_SHA,
                 "gate_rows_json_sha256": SR_GATEROWS_SHA,
                 "gate_rows_all_pass": SR_GATES_TOTAL,
                 "gate_status_log_sha256": SR_STATUS_SHA,
                 "gate_status_gate_pass_rows": SR_GATE_STATUS_ROWS,
                 "audit_gate_json_sha256": SR_AUDIT_SHA,
                 "audit_run1_run2_run3_sha256_identical": SR_AUDIT_SHA,
                 "audit_gate_py_sha256": SR_AUDIT_PY_SHA,
                 "audit_gate_py_live_rerun": "rc=0, PASS",
                 "tamper_battery_log_sha256": SR_TAMPER_SHA,
                 "t1_result_json_sha256": SR_T1_RESULT_SHA,
                 "cpp_solver_sha256": SR_CPP_SHA,
                 "cpp_solver_commit": SR_CPP_COMMIT,
             },
             "canonical_head_cross_gate":
                 "the SR gate-rows.json canonical_head block pins exactly "
                 "this Part's BASE 02db5ab3 (6,801 rows WIN 201 / LOSS "
                 "6600) and records the 30 targets fresh versus it; the "
                 "freshness vs BASE is re-gated by this Part directly"},
            {"pool": "k09k43-third-implementation-verdict-reverify",
             "kit": TI_EXP,
             "covered_ids": list(ADOPTED_IDS),
             "kit_integrity": {
                 "note": "the k09..k43 resolved-32 third-impl addendum "
                         "(published inside the k01-k03 third-impl kit) "
                         "is gated here directly on its published bytes "
                         "and re-verified LIVE: the data-driven auditor "
                         "audit_k09k43.py is re-run twice in this maker "
                         "with rc=0, 850/850 gates, byte-identical "
                         "stdout; the cold a/b witness raws, negative-gate "
                         "raws, tamper-controls log, published summary "
                         "and the per-row replica-raw copies (byte-equal "
                         "to the probe kit raws) are all sha-pinned and "
                         "field-gated",
                 "auditor_sha256": TI_AUDITOR_SHA,
                 "third_impl_js_sha256": TI_THIRD_IMPL_SHA,
                 "verify_tbl_js_sha256": TI_VERIFY_TBL_SHA,
                 "tamper_controls_log_sha256": TI_TAMPER_LOG_SHA,
                 "summary_json_sha256": TI_SUMMARY_SHA,
                 "cold_raw_sha256_pins": "in-maker (TI_COLD_PINS)",
                 "negative_gate_raw_sha256_pins": TI_NEG_SHAS,
                 "auditor_live_rerun": "rc=0, 850/850 gates, deterministic "
                                       "byte-identical stdout x2",
             },
             "verdict_agreement_note":
                 "third-impl LOSS(2) verdict-level agreement for all 30 "
                 "adopted rows with 2 identical cold runs each "
                 "(expansions legitimately differ from replica node "
                 "counts - different implementations); the addendum's "
                 "replica raw copies are byte-equal to the probe kit's "
                 "fifth-resumption raws",
             "standing_unconsumed_keys": STANDING_PARKED_KEYS,
             "coverage_asymmetry_disclosure":
                 "the still-parked key k38 (10376293541461626880:66048) "
                 "has a first-implementation L50M cold-pair LOSS row and "
                 "a Part SS C++ GATE-PASS but NO third-implementation "
                 "corroboration; it stays standing unconsumed and is NOT "
                 "adopted by this Part",
        },
        ],
        "resolved_ids": list(ADOPTED_IDS),
        "loss_ids": list(ADOPTED_IDS),
        "win_ids": [],
        "loss_ties": [],
        "loss_ties_note": "no consumed-LOSS regression ties: all 30 "
                          "adopted keys are fresh to BASE",
        "row_counts": {
            "adopted_loss_rows": 30,
            "loss_ties_consumed_elsewhere": 0,
            "standing_unconsumed_parked_keys": len(STANDING_PARKED_KEYS),
            "prior_canonical_rows_base": BASE_CACHE_ROWS_EXPECTED,
        },
        "adopted_table": adopted_table,
        "adopted_table_digest_sha256": digest,
        "adopted_nodes_total": ADOPTED_NODES_TOTAL,
        "sha256": {"loss_increment": incr_sha},
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_sha256": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "base_cache_win_loss": [BASE_CACHE_WIN_EXPECTED,
                                BASE_CACHE_LOSS_EXPECTED],
        "base_cache_absent_hits_for_emitted": 0,
        "quarantine_hits": 0,
        "interpretation_guard":
            "Part ST canonical LOSS-only adoption increment: the 30 fresh "
            "exact-LOSS rows (each cold two-pass node-exact at its "
            "pinned resolution budget over the pinned 2M park-at-UNKNOWN "
            "baseline, C++-gated by Part SR 33/33 GATE-PASS and third-"
            "implementation-corroborated by the k09..k43 addendum re-run "
            "live 850/850) are consumed into the canonical chain via the "
            "fail-closed union merger whose output this Part publishes "
            "as the merged head of record (dade15780..., 6,831 rows WIN "
            "201 / LOSS 6,630); LOSS-only adoption asserts no root "
            "verdict, frees no class and excludes no class (zero status "
            "flips; the Part EM precedent); the serving class 3077 keeps "
            "its excluded_now status with cost-unknown 91 -> 61, "
            "derived machine-only by the reaudit refresh and the census "
            "delta measurer; nodes are bookkeeping, never verdicts; the "
            "standard 11x11 empty board and every central-reply root "
            "stay UNKNOWN",
        "provenance": {
            "part_maker_reverified_live": True,
            "merged_cache_published_by_this_part": True,
            "sr_kit_files_verified": SR_KIT_FILES,
            "sr_audit_gate_live_rerun": True,
            "third_impl_auditor_live_rerun": True,
            "probe_kit_direct_pins": True,
            "raws_published": True,
        },
    }
    manifest_bytes = json.dumps(manifest, indent=1,
                                sort_keys=True).encode("utf-8")
    with (OUT / "increments-manifest.json").open("wb") as f:
        f.write(manifest_bytes)
        f.flush()
        import os as _os
        _os.fsync(f.fileno())
        _dfd = _os.open(str(OUT), _os.O_RDONLY)
        try:
            _os.fsync(_dfd)
        finally:
            _os.close(_dfd)
    print(json.dumps({
        "part": "ST",
        "head_of_record": "02db5ab3... -> dade15780... (6,831 rows "
                          "WIN 201 / LOSS 6,630)",
        "increment_sha256": incr_sha,
        "rows": len(rowlines),
        "adopted_nodes_total": ADOPTED_NODES_TOTAL,
        "digest": digest,
        "manifest_sha256": hashlib.sha256(
            (OUT / "increments-manifest.json").read_bytes()).hexdigest(),
    }))


if __name__ == "__main__":
    main()
