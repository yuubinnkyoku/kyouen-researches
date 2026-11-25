#!/usr/bin/env python3
"""Build the batch-30 (class 34269) 43-LOSS canonical-adoption increment, fail-closed.

Prepared for the Part DN adoption (declared 2026-11-24, publish-then-execute):
the published batch-30 cumulative evidence is byte-pinned through the three
published kits -- the single batch-30 kit (MANIFEST 330128aa1bcff45b52dac46e7e8bf9bbf57836f90d8f342fa269ee85ae77d845,
199 files: input 55 + output/raw 112 (108 primary two-pass raws + 4 pinned
truncated retry sidecars) + scripts 6 + val-gate 24 + README + the 79-line
honest-history status.log), the published Part DJ exh6-20M reprobe kit
(MANIFEST bb88fba3338a2e4188cd9a6a6fc8a1208507ccaa42fac36e9facb3fd0833a907, 34 files; its MANIFEST records the raws and
status under output/-relative names -- a documented quirk resolved here against
the published tree), and the published Part DK 25M reprobe kit (MANIFEST
e05c4259cdc5b004fc340fb770044ba57e443de0591c7d57a4b6a3b349707375, 15 files).  Every kit file is sha256-verified here
file-by-file.  jsreplay.js 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df is byte-identical in all three
kits.

The batch is FULLY probed: all 54 of 54 keys carry honest two-pass fresh-cold
labels.  38 keys are resolved LOSS at budget 15M (kit raws) plus 4 at budget
20M (the published Part DJ reprobe raws: ac032/ac036/ac044/ac047) plus
ac013 at budget 25M (the published Part DK reprobe raws, superseding its
pinned 15M and 20M EXHAUSTED pairs) = 43 LOSS rows adopted here.  11 keys are
probe-level WINs (10 at 15M in the kit, ac006 at the Part DJ 20M reprobe,
superseding its pinned 15M exhaustion) and ALL ELEVEN stay UNCONSUMED: none
is adopted here, none is emitted into any increment, none is written into any
canonical cache (WIN-row adoption is the separate scrutiny-owner C++
second-implementation lane, pin 9193f5b6...).  No batch-30 key was adopted
canonically before (the BASE carries none of them).

The adoption base is the canonical exact-S5 verdict chain head = the Part DL
merged 6,405-row cache sha256 60222707dd13902103fc8f7ef11c8487ec1be531ad0711e23e50c32154e30b84 (BASE through the Part DL
b31loss51 adoption), byte-pinned here; this maker ABORTS against anything
else.  Every adopted key is asserted fresh (absent from the BASE) and absent
from the quarantine registry (81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9).  Every unconsumed WIN key
is likewise asserted absent (its verdict is consumed nowhere).

The drive status.log is HONEST HISTORY (unlike Part DL's clean 59-line shape):
79 lines = 56 PASS rows (54 keys, with the pinned ac001/ac002 restart
duplicates each appearing exactly twice at the pinned rows) + exactly the 11
pinned WIN-HALT rows (ac002 twice with its two pinned PASS rows, 10 unique
15M WIN keys) + exactly the 6 pinned EXHAUSTED rows (ac006/ac013/ac032/
ac036/ac044/ac047 at 15M, all later superseded by the DJ/DK reprobes) +
exactly the 2 pinned MISMATCH rows (ac028/ac029: truncated second passes
retried and resolved, the retry PASS rows pinned node-exact against the
mismatch p1 triples) + exactly the 4 pinned TRUNCATED-RETRY markers.  All rows
of all five classes are pinned line-by-line; per-key PASS agreement with the
kit raws is machine-checked on (budget, result, nodes).

Fail-closed gates: three kit MANIFESTs sha-verified file-by-file (199+34+15
files, the DJ output/-relative name quirk resolved and pinned); 54+6+1 two-pass
fresh-cold raw re-verification with '# replay_done' on both passes and
(budget,result,nodes) agreement with all three status logs; the three-generation
ac013 supersede chain byte-pinned (15M EXHAUSTED pair in kit, DJ 20M EXHAUSTED
pair, DK 25M LOSS pair, nodes 21,954,135 two-pass node-exact); the DJ
frozen-snapshot chain tie (DJ kit batch-keys base_status_log_sha256 ==
sha256 of the first 2180 bytes of the published 79-line status.log, the state
frozen at the DJ selection; byte 2180 is the end of line 44, the pinned ac029
resolved retry row) and the DK kit batch-keys base_status_log prefix (8 hex
chars of the full 79-line status sha); val-gates node-exact across hosts
(4 gate patterns x 5 published hosts in kit + DJ first/second-20m-vgo @20M +
DK first/second-25m dkt/dkvv @25M, the two gate molecules identical across
kits by byte); the 43 adopted keys distinct, ABSENT from the canonical BASE
(6,405 rows) and from the quarantine registry; adopted-row per-pass node total
346729500 on both passes; the 11 WIN keys consumed nowhere.  Verdicts are
byte-taken from the raws.  The 43 LOSS rows ARE the only thing consumed into
the canonical cache by this Part; 11x11 stays UNKNOWN; nodes are bookkeeping,
never verdicts; class 34269 is NOT freed here (eleven unconsumed WIN children
remain, verdict-unconsumed).
"""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
KIT1_DIR = ROOT / "research/experiments/n11-centralreply-closure-class34269-batch30-20261123"
KIT2_DIR = ROOT / "research/experiments/n11-centralreply-closure-class34269-batch30-exh6-20m-20261124"
KIT3_DIR = ROOT / "research/experiments/n11-centralreply-closure-class34269-batch30-exh1-25m-20261124"
# kit1 raws live under output/raw, kit2 raws under output/raw too (the DJ kit
# MANIFEST records them without the output/ prefix, a documented quirk resolved
# in verify_kit), kit3 raws under output/raw.
KIT1_RAW = KIT1_DIR / "output/raw"
KIT2_RAW = KIT2_DIR / "output/raw"
KIT3_RAW = KIT3_DIR / "output/raw"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class5804-b31loss51-adoption-reaudit-20261124/output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-20261124.cache"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
MERGER = EXP / "scripts/s5_union_merge.py"

MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA_EXPECTED = "60222707dd13902103fc8f7ef11c8487ec1be531ad0711e23e50c32154e30b84"
BASE_CACHE_ROWS_EXPECTED = 6405
BASE_CACHE_WIN_EXPECTED = 158
BASE_CACHE_LOSS_EXPECTED = 6247
JSREPLAY_SHA_EXPECTED = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
QUARANTINE_SHA_EXPECTED = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

# --- published kit pins -------------------------------------------------------
KIT1_MANIFEST_SHA = "330128aa1bcff45b52dac46e7e8bf9bbf57836f90d8f342fa269ee85ae77d845"
KIT1_FILES = 199
KIT2_MANIFEST_SHA = "bb88fba3338a2e4188cd9a6a6fc8a1208507ccaa42fac36e9facb3fd0833a907"
KIT2_FILES = 34
KIT3_MANIFEST_SHA = "e05c4259cdc5b004fc340fb770044ba57e443de0591c7d57a4b6a3b349707375"
KIT3_FILES = 15
KIT1_KEYS_SHA = "79fbd1664f4ad66ea62d9c8a8aa5aaff5d16bcdaa397895119ce4d8f47961232"
KIT2_KEYS_SHA = "a80f402befaf2e8cf7b0484b4c51a125b525ccfd536a31ad7dea52b555011068"
KIT3_KEYS_SHA = "797467ec1009fc835c3fa9b92a29ebdbac6c3431777abbcde11a8a6fc1df88d5"
KIT1_STATUS_SHA = "88a474b5ef544ecb015f5a4058bc2dcb969afaca6f1b2816887307cd720c632c"
KIT2_STATUS_SHA = "62f66b6a76eef059f42c225353003de4d4f9c638b33438c8217ec411df4da3c9"
KIT3_STATUS_SHA = "6a345a8bb33bb1e4536a30cb4d7ff974ab06a74eeed520f7756b37f32653d569"
KIT2_SNAPSHOT_SHA = "07d839ab54a811b782cd79529c862c3827339e46e9942433012ae8378f790e2c"  # first 2180 bytes of the 79-line status
KIT2_SNAPSHOT_BYTES = 2180
KIT3_SNAPSHOT_PREFIX = "88a474b5"

# --- status.log honest-history pins -------------------------------------------
KIT1_STATUS_LINES = 79
KIT1_STATUS_FIRST_LINE = "2026-11-23T21:46:53Z ac001 PASS 15000000,2,5635468"
KIT1_STATUS_FINAL_LINE = "2026-11-24T07:26:04Z ac053 PASS 15000000,2,4251146"
WIN_HALT_LINES = [
        "2026-11-23T21:47:49Z ac002 WIN-HALT",
        "2026-11-23T21:48:06Z ac002 WIN-HALT",
        "2026-11-23T21:50:48Z ac003 WIN-HALT",
        "2026-11-24T02:08:58Z ac020 WIN-HALT",
        "2026-11-24T02:15:22Z ac027 WIN-HALT",
        "2026-11-24T02:15:26Z ac026 WIN-HALT",
        "2026-11-24T07:02:25Z ac034 WIN-HALT",
        "2026-11-24T07:11:14Z ac041 WIN-HALT",
        "2026-11-24T07:16:08Z ac045 WIN-HALT",
        "2026-11-24T07:18:16Z ac048 WIN-HALT",
        "2026-11-24T07:25:41Z ac054 WIN-HALT",
    ]
EXHAUSTED_LINES = [
        "2026-11-24T01:48:05Z ac006 EXHAUSTED 15000000,0,15000000",
        "2026-11-24T01:56:44Z ac013 EXHAUSTED 15000000,0,15000000",
        "2026-11-24T06:55:12Z ac032 EXHAUSTED 15000000,0,15000000",
        "2026-11-24T07:03:43Z ac036 EXHAUSTED 15000000,0,15000000",
        "2026-11-24T07:15:13Z ac044 EXHAUSTED 15000000,0,15000000",
        "2026-11-24T07:20:11Z ac047 EXHAUSTED 15000000,0,15000000",
    ]
MISMATCH_LINES = [
        "2026-11-24T02:17:46Z ac028 MISMATCH p1=15000000,2,5087946 p2=",
        "2026-11-24T02:19:25Z ac029 MISMATCH p1=15000000,2,9204933 p2=",
    ]
RETRY_LINES = [
        "2026-11-24T01:45:32Z ac006 P2-TRUNCATED-RETRY",
        "2026-11-24T02:16:52Z ac029 P1-TRUNCATED-RETRY",
        "2026-11-24T02:16:52Z ac028 P2-TRUNCATED-RETRY",
        "2026-11-24T06:59:37Z ac034 P2-TRUNCATED-RETRY",
    ]
KIT1_PASS_DUP = {"ac001": 2, "ac002": 2}
KIT1_PASS_DUP_ROWS = [
    ("ac001", (15000000, 2, 5635468)),
    ("ac002", (15000000, 1, 10752246)),
]
KIT2_STATUS_LINES = 14
KIT2_STATUS_FIRST_LINE = "2026-11-24T07:50:02Z ac013 P2-TRUNCATED-RETRY"
KIT2_STATUS_FINAL_LINE = "2026-11-24T08:09:36Z ac047 PASS 20000000,2,17394041"
DJ_RETRY_LINES = [
        "2026-11-24T07:50:02Z ac013 P2-TRUNCATED-RETRY",
        "2026-11-24T07:50:02Z ac006 P2-TRUNCATED-RETRY",
        "2026-11-24T07:58:25Z ac032 P2-TRUNCATED-RETRY",
        "2026-11-24T07:58:25Z ac036 P2-TRUNCATED-RETRY",
        "2026-11-24T08:06:17Z ac047 P2-TRUNCATED-RETRY",
        "2026-11-24T08:06:17Z ac044 P2-TRUNCATED-RETRY",
    ]
DJ_WIN_HALT_LINES = [
        "2026-11-24T07:53:38Z ac006 WIN-HALT",
    ]
DJ_EXHAUSTED_LINES = [
        "2026-11-24T07:53:43Z ac013 EXHAUSTED 20000000,0,20000000",
    ]
KIT3_STATUS_LINES = 1
KIT3_STATUS_FINAL_LINE = "2026-11-24T11:49:57Z ac013 PASS 25000000,2,21954135"

# --- raw inventory pins --------------------------------------------------------
KIT1_SIDECARS = [
    "ac006.p2.truncated.014532.out",
    "ac028.p2.truncated.021652.out",
    "ac029.p1.truncated.021652.out",
    "ac034.p2.truncated.065937.out",
]
KIT2_SIDECARS = [
    "ac006.p2.truncated.075002.out",
    "ac013.p2.truncated.075002.out",
    "ac032.p2.truncated.075825.out",
    "ac036.p2.truncated.075825.out",
    "ac044.p2.truncated.080617.out",
    "ac047.p2.truncated.080617.out",
]

# --- adopted packet ------------------------------------------------------------
ADOPTED_LOSS_IDS = ['ac001', 'ac004', 'ac005', 'ac007', 'ac008', 'ac009', 'ac010', 'ac011', 'ac012', 'ac013', 'ac014', 'ac015', 'ac016', 'ac017', 'ac018', 'ac019', 'ac021', 'ac022', 'ac023', 'ac024', 'ac025', 'ac028', 'ac029', 'ac030', 'ac031', 'ac032', 'ac033', 'ac035', 'ac036', 'ac037', 'ac038', 'ac039', 'ac040', 'ac042', 'ac043', 'ac044', 'ac046', 'ac047', 'ac049', 'ac050', 'ac051', 'ac052', 'ac053']
WIN_UNCONSUMED_IDS = ['ac002', 'ac003', 'ac006', 'ac020', 'ac026', 'ac027', 'ac034', 'ac041', 'ac045', 'ac048', 'ac054']
EXH15_IDS = ['ac006', 'ac013', 'ac032', 'ac036', 'ac044', 'ac047']
PROBED_IDS = [f"ac{i:03d}" for i in range(1, 55)]
ADOPTED_KEYS = {
    'ac001': {'key': (1152921504758890496, 68719476736), 'legal': 88, 'nodes': 5635468, 's5': 36668, 'mcc': 2, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac004': {'key': (1152921779502579712, 68719476736), 'legal': 89, 'nodes': 5816333, 's5': 257581, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac005': {'key': (5764607523052060672, 68719476736), 'legal': 92, 'nodes': 7941333, 's5': 259840, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac007': {'key': (1152921504624672768, 68719476737), 'legal': 95, 'nodes': 6320372, 's5': 357255, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac008': {'key': (1152921504624672800, 68719476736), 'legal': 87, 'nodes': 3722379, 's5': 440522, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac009': {'key': (1152921504624672768, 68719476738), 'legal': 92, 'nodes': 14494291, 's5': 442454, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac010': {'key': (1153202979601383424, 68719476736), 'legal': 80, 'nodes': 4730437, 's5': 542960, 'mcc': 2, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac011': {'key': (1152921504624672768, 68719476992), 'legal': 80, 'nodes': 3413023, 's5': 544425, 'mcc': 2, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac012': {'key': (1152922054380486656, 68719476736), 'legal': 93, 'nodes': 6067761, 's5': 604378, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac013': {'key': (1155173304438358016, 68719476736), 'legal': 93, 'nodes': 21954135, 's5': 605817, 'mcc': 4, 'decisive_budget': 25000000, 'raw_kit': 'KIT3'},
    'ac014': {'key': (1152921504624672768, 68719477248), 'legal': 88, 'nodes': 8535077, 's5': 625811, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac015': {'key': (1152921504893108224, 68719476736), 'legal': 87, 'nodes': 6725969, 's5': 715677, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac016': {'key': (1152921504691781632, 68719476736), 'legal': 91, 'nodes': 3000128, 's5': 731067, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac017': {'key': (1152921504624672768, 68719477760), 'legal': 95, 'nodes': 10672726, 's5': 732474, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac018': {'key': (1152921504624803840, 68719476736), 'legal': 91, 'nodes': 6927463, 's5': 799572, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac019': {'key': (1161928703879413760, 68719476736), 'legal': 91, 'nodes': 10173232, 's5': 800491, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac021': {'key': (1152921504624672768, 68719478784), 'legal': 91, 'nodes': 9916865, 's5': 810549, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac022': {'key': (1152921504624672832, 68719476736), 'legal': 88, 'nodes': 3441401, 's5': 858406, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac023': {'key': (1170935903134154752, 68719476736), 'legal': 96, 'nodes': 8979741, 's5': 859149, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac024': {'key': (1152921504624672784, 68719476736), 'legal': 81, 'nodes': 9826442, 's5': 865769, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac025': {'key': (1152921504624672768, 68719480832), 'legal': 78, 'nodes': 3428856, 's5': 866494, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac028': {'key': (1152921505161543680, 68719476736), 'legal': 87, 'nodes': 5087946, 's5': 916195, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac029': {'key': (1152923703647928320, 68719476736), 'legal': 93, 'nodes': 9204933, 's5': 916640, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac030': {'key': (1152921504658227200, 68719476736), 'legal': 92, 'nodes': 7072780, 's5': 920775, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac031': {'key': (1152921504624672768, 68721573888), 'legal': 97, 'nodes': 10125646, 's5': 921287, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac032': {'key': (1152921504624934912, 68719476736), 'legal': 92, 'nodes': 19707272, 's5': 939058, 'mcc': 4, 'decisive_budget': 20000000, 'raw_kit': 'KIT2'},
    'ac033': {'key': (1152925902671183872, 68719476736), 'legal': 86, 'nodes': 5912106, 's5': 939315, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac035': {'key': (1152921504624672768, 68723671040), 'legal': 93, 'nodes': 8904715, 's5': 941466, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac036': {'key': (1152921504624672896, 68719476736), 'legal': 90, 'nodes': 16605302, 's5': 951686, 'mcc': 4, 'decisive_budget': 20000000, 'raw_kit': 'KIT2'},
    'ac037': {'key': (1152930300717694976, 68719476736), 'legal': 86, 'nodes': 3818788, 's5': 951830, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac038': {'key': (1152921504624672776, 68719476736), 'legal': 95, 'nodes': 5018863, 's5': 952950, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac039': {'key': (1152921504624672768, 68727865344), 'legal': 97, 'nodes': 11367923, 's5': 953103, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac040': {'key': (1152921504624672769, 68719476736), 'legal': 84, 'nodes': 3119506, 's5': 955954, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac042': {'key': (1152921504624672772, 68719476736), 'legal': 95, 'nodes': 3007885, 's5': 956625, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac043': {'key': (1152921504624673024, 68719476736), 'legal': 82, 'nodes': 6210354, 's5': 956972, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac044': {'key': (1152921504624673280, 68719476736), 'legal': 92, 'nodes': 16323488, 's5': 957287, 'mcc': 4, 'decisive_budget': 20000000, 'raw_kit': 'KIT2'},
    'ac046': {'key': (1152921504625197056, 68719476736), 'legal': 92, 'nodes': 5216563, 's5': 957935, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac047': {'key': (1152921504626769920, 68719476736), 'legal': 94, 'nodes': 17394041, 's5': 958064, 'mcc': 4, 'decisive_budget': 20000000, 'raw_kit': 'KIT2'},
    'ac049': {'key': (1152921504607895556, 73014444032), 'legal': 90, 'nodes': 3095290, 's5': 958082, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac050': {'key': (1152921504607903744, 73014444032), 'legal': 82, 'nodes': 8586185, 's5': 958097, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac051': {'key': (1152921504607895554, 73014444032), 'legal': 89, 'nodes': 9625374, 's5': 958105, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac052': {'key': (1152921504607895553, 73014444032), 'legal': 86, 'nodes': 5349962, 's5': 958114, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac053': {'key': (1152921504624672768, 73014444032), 'legal': 80, 'nodes': 4251146, 's5': 958125, 'mcc': 2, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
}
WIN_UNCONSUMED = {
    'ac002': {'key': (10376293541479448576, 68719476736), 'legal': 87, 'nodes': 10752246, 's5': 38891, 'mcc': 2, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac003': {'key': (1153484454578094080, 68719476736), 'legal': 85, 'nodes': 8036766, 's5': 178184, 'mcc': 2, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac006': {'key': (1152921504624738304, 68719476736), 'legal': 85, 'nodes': 18182847, 's5': 355050, 'mcc': 3, 'decisive_budget': 20000000, 'raw_kit': 'KIT2'},
    'ac020': {'key': (1152921504624705536, 68719476736), 'legal': 90, 'nodes': 9765071, 's5': 809575, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac026': {'key': (1152921573344149504, 68719476736), 'legal': 82, 'nodes': 3036572, 's5': 900276, 'mcc': 2, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac027': {'key': (1152921504624672768, 68720525312), 'legal': 80, 'nodes': 2593751, 's5': 900687, 'mcc': 2, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac034': {'key': (1152921504624689152, 68719476736), 'legal': 83, 'nodes': 14853857, 's5': 941211, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac041': {'key': (1152921504624672770, 68719476736), 'legal': 84, 'nodes': 10959413, 's5': 956329, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac045': {'key': (1152921504624676864, 68719476736), 'legal': 88, 'nodes': 2530544, 's5': 957713, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac048': {'key': (1152921508919640064, 68719476736), 'legal': 76, 'nodes': 4701704, 's5': 958080, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ac054': {'key': (1152921504607899648, 73014444032), 'legal': 76, 'nodes': 2236690, 's5': 958143, 'mcc': 2, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
}
ADOPTED_TOTAL_NODES = 346729500

# --- supersede pins -------------------------------------------------------------
DJ20_NODES = {"ac006": 18182847, "ac032": 19707272, "ac036": 16605302, "ac044": 16323488, "ac047": 17394041}
DJ20_EXH_NODES = 20000000
DK25_LOSS_NODES = 21954135
BUDGET_KIT1 = 15000000
BUDGET_KIT2 = 20000000
BUDGET_KIT3 = 25000000

# --- val-gate pins ---------------------------------------------------------------
VAL_GATES = {
    "at2m-s5-1152921504606851072-536870946": (2000000, 0, 2000000),
    "at2m-s5-1188950301626860544-536870912": (2000000, 0, 2000000),
    "first-15m-s5-1152921504606851072-536870946": (15000000, 2, 3651923),
    "second-15m-s5-1188950301626860544-536870912": (15000000, 2, 5040200),
}
VAL_HOSTS = ["published-baseline", "b30-host", "d2t-host", "d3t-host", "d3u-host"]
KIT2_VG = {
    "first-20m-vgo.djvg1-host.out": (20000000, 2, 3651923),
    "second-20m-vgo.djvg2-host.out": (20000000, 2, 5040200),
}
KIT3_VG = {
    "first-25m.dkt-vg1-host.out": (25000000, 2, 3651923),
    "first-25m.dkvvg1-host.out": (25000000, 2, 3651923),
    "second-25m.dkt-vg2-host.out": (25000000, 2, 5040200),
    "second-25m.dkvvg2-host.out": (25000000, 2, 5040200),
}


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


def norm_key(row):
    return (int(row["lo"]), int(row["hi"]))


def _kit_candidates(kit_dir: Path, rel: str) -> list:
    """Resolve a MANIFEST-recorded path against the published tree.

    Three recorded path styles occur across the published kits:
      * repo-prefixed (KIT1 and KIT2 for scripts/input/val-gate/README),
      * work-tree-relative (KIT3: README.md, input/, output/, scripts/...),
      * the KIT2 quirk: raws and status.log recorded without the output/
        component that exists in the published tree.
    Resolution is content sha-checked regardless; nothing is trusted on name.
    """
    cands = []
    cands.append(kit_dir / rel)
    cands.append(ROOT / rel)
    stripped = rel.split("research/experiments/", 1)[-1]
    stripped = stripped[stripped.index("/") + 1:] if stripped.startswith("n11") else stripped
    cands.append(kit_dir / stripped)
    cands.append(kit_dir / "output" / stripped)
    return cands


def verify_kit(dirp: Path, manifest_sha: str, kit_files: int):
    if not dirp.is_dir():
        sys_exit(f"kit dir missing {dirp}")
    if sha(dirp / "MANIFEST-sha256.txt") != manifest_sha:
        sys_exit(f"kit {dirp.name} MANIFEST sha drift")
    verified = 0
    for line in (dirp / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        want, rel = line.split(None, 1)
        p = None
        for cand in _kit_candidates(dirp, rel):
            if cand.is_file():
                p = cand
                break
        if p is None:
            sys_exit(f"kit {dirp.name} file missing: {rel} (resolved candidates tried)")
        if sha(p) != want:
            sys_exit(f"kit {dirp.name} file sha drift: {rel}")
        verified += 1
    if verified != kit_files:
        sys_exit(f"kit {dirp.name} files verified {verified} != {kit_files}")
    return verified


def two_pass(rawdir: Path, kid: str):
    variants = {}
    for tag in ("p1", "p2"):
        p = rawdir / f"{kid}.{tag}.out"
        if not p.is_file():
            sys_exit(f"missing raw {p}")
        txt = p.read_text()
        if "# replay_done" not in txt:
            sys_exit(f"raw {p} lacks the '# replay_done' completeness guard")
        variants[tag] = parse_replay(p)
    ref = variants["p1"]
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
    for tag, r in variants.items():
        if tuple(r[f] for f in fields) != tuple(ref[f] for f in fields):
            sys_exit(f"{kid}: pass mismatch {tag} vs p1")
    return ref


def parse_status1(path: Path):
    lines = path.read_text().splitlines()
    if len(lines) != KIT1_STATUS_LINES:
        sys_exit(f"kit1 status lines {len(lines)} != {KIT1_STATUS_LINES}")
    if lines[0] != KIT1_STATUS_FIRST_LINE or lines[-1] != KIT1_STATUS_FINAL_LINE:
        sys_exit("kit1 status first/final line drift")
    # all five row classes pinned line-by-line
    for pin_list, marker in ((WIN_HALT_LINES, lambda l: l.endswith(" WIN-HALT")),
                             (EXHAUSTED_LINES, lambda l: " EXHAUSTED " in l),
                             (MISMATCH_LINES, lambda l: " MISMATCH " in l),
                             (RETRY_LINES, lambda l: l.endswith("TRUNCATED-RETRY"))):
        got = [l for l in lines if marker(l)]
        if sorted(got, key=lines.index) != pin_list:
            sys_exit(f"kit1 status row-class drift ({len(pin_list)} pinned rows)")
    got_pass = {}
    for line in lines:
        m = re.match(r"^(\S+) (ac\d{3}) PASS (\d+),(\d+),(\d+)$", line)
        if m:
            kid = m.group(2)
            got_pass.setdefault(kid, []).append((int(m.group(3)), int(m.group(4)), int(m.group(5))))
    if len([x for v in got_pass.values() for x in v]) != 56:
        sys_exit("kit1 status PASS count != 56 (54 keys + 2 pinned restart duplicates)")
    # every key exactly its pinned PASS multiplicity
    counts = {k: len(v) for k, v in got_pass.items()}
    for kid in PROBED_IDS:
        want = KIT1_PASS_DUP.get(kid, 1)
        if counts.get(kid, 0) != want:
            sys_exit(f"kit1 status: {kid} has {counts.get(kid, 0)} PASS rows != pinned {want}")
    if set(counts) != set(PROBED_IDS):
        sys_exit("kit1 status PASS keys != the 54 probed keys")
    return got_pass


def assert_final_pass_row(kid, triple, rows):
    if triple not in rows:
        sys_exit(f"{kid}: decisive PASS row {triple} not in status rows {rows}")


def main() -> None:
    # --- base cache, merger, quarantine anchors -------------------------------
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys_exit("base cache sha drift")
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

    # --- kit integrity: three published kits, file-by-file ---------------------
    k1 = verify_kit(KIT1_DIR, KIT1_MANIFEST_SHA, KIT1_FILES)
    k2 = verify_kit(KIT2_DIR, KIT2_MANIFEST_SHA, KIT2_FILES)
    k3 = verify_kit(KIT3_DIR, KIT3_MANIFEST_SHA, KIT3_FILES)
    if sha(KIT1_DIR / "scripts/jsreplay.js") != JSREPLAY_SHA_EXPECTED or \
            sha(KIT2_DIR / "scripts/jsreplay.js") != JSREPLAY_SHA_EXPECTED or \
            sha(KIT3_DIR / "scripts/jsreplay.js") != JSREPLAY_SHA_EXPECTED:
        sys_exit("jsreplay.js sha drift in a kit (pinned solver image 8458...)")
    if sha(KIT1_DIR / "input/batch-keys.json") != KIT1_KEYS_SHA or \
            sha(KIT2_DIR / "input/batch-keys.json") != KIT2_KEYS_SHA or \
            sha(KIT3_DIR / "input/batch-keys.json") != KIT3_KEYS_SHA:
        sys_exit("batch-keys sha drift in a kit")
    if sha(KIT1_DIR / "output/status.log") != KIT1_STATUS_SHA or \
            sha(KIT2_DIR / "output/status.log") != KIT2_STATUS_SHA or \
            sha(KIT3_DIR / "output/status.log") != KIT3_STATUS_SHA:
        sys_exit("status.log sha drift in a kit")

    # --- chain ties: DJ frozen snapshot + DK prefix + input csv byte identity ---
    stat1_bytes = (KIT1_DIR / "output/status.log").read_bytes()
    if hashlib.sha256(stat1_bytes[:KIT2_SNAPSHOT_BYTES]).hexdigest() != KIT2_SNAPSHOT_SHA:
        sys_exit("DJ kit base_status_log_sha256 does not reproduce the frozen "
                 "2180-byte snapshot prefix of the published 79-line status.log")
    if hashlib.sha256(stat1_bytes).hexdigest()[:8] != KIT3_SNAPSHOT_PREFIX:
        sys_exit("DK kit base_status_log prefix drift vs the published 79-line status")
    dkkeys = json.loads((KIT3_DIR / "input/batch-keys.json").read_text())
    if dkkeys.get("base_status_log_sha256") != KIT3_SNAPSHOT_PREFIX:
        sys_exit("DK kit batch-keys base_status_log prefix drift")
    for kid in EXH15_IDS:
        if (KIT1_DIR / f"input/{kid}.input.csv").read_bytes() != (KIT2_DIR / f"input/{kid}.input.csv").read_bytes():
            sys_exit(f"KIT2 input csv for {kid} not byte-identical to KIT1")
    if (KIT1_DIR / "input/ac013.input.csv").read_bytes() != (KIT3_DIR / "input/ac013.input.csv").read_bytes():
        sys_exit("KIT3 ac013 input csv not byte-identical to KIT1")
    for gate, name in (("first", "first-15m-s5-1152921504606851072-536870946"),
                        ("second", "second-15m-s5-1188950301626860544-536870912")):
        b1 = (KIT1_DIR / f"val-gate/{name}.input.csv").read_bytes()
        b2 = (KIT2_DIR / f"val-gate/{name}.input.csv").read_bytes()
        b3 = (KIT3_DIR / f"val-gate/{name}.input.csv").read_bytes()
        if not (b1 == b2 == b3):
            sys_exit(f"val-gate input csv for {gate} not byte-identical across kits")

    # --- batch-keys gates --------------------------------------------------------
    bk_all = json.loads((KIT1_DIR / "input/batch-keys.json").read_text())
    if bk_all["schema"] != "n11-centralreply-closure-class34269-batch30-input-v1":
        sys_exit("KIT1 batch-keys schema drift")
    if bk_all["class_index"] != 34269 or bk_all["budget"] != BUDGET_KIT1:
        sys_exit("KIT1 batch-keys class/budget drift")
    if len(bk_all["keys"]) != 54:
        sys_exit("KIT1 batch-keys key count != 54")
    if bk_all["closure_class_rank_in_published_base"] != 36:
        sys_exit("KIT1 batch-keys closure rank drift (kit frozen at selection)")
    if int(bk_all["published_base_canonical_rows"]) != 6301:
        sys_exit("KIT1 batch-keys published_base_canonical_rows drift (kit frozen at selection)")
    if bk_all["class_mask"] != ["1152921504624672768", "68719476736"]:
        sys_exit("KIT1 batch-keys class mask drift")
    by_id = {k["key_id"]: k for k in bk_all["keys"]}
    djkeys2 = json.loads((KIT2_DIR / "input/batch-keys.json").read_text())
    if djkeys2["schema"] != "n11-centralreply-closure-class34269-batch30-exh6-20m-input-v1":
        sys_exit("KIT2 batch-keys schema drift")
    if djkeys2["class_index"] != 34269 or djkeys2["budget"] != BUDGET_KIT2 or len(djkeys2["keys"]) != 6:
        sys_exit("KIT2 batch-keys class/budget/keys drift")
    if djkeys2["reprobe_of"] != EXH15_IDS or djkeys2["budget"] != BUDGET_KIT2:
        sys_exit("KIT2 reprobe_of drift")
    if djkeys2["base_status_log_sha256"] != KIT2_SNAPSHOT_SHA:
        sys_exit("KIT2 batch-keys snapshot sha drift")
    if dkkeys["schema"] != "n11-centralreply-closure-class34269-batch30-exh1-25m-input-v1":
        sys_exit("KIT3 batch-keys schema drift")
    if dkkeys["class_index"] != 34269 or dkkeys["budget"] != BUDGET_KIT3 or dkkeys["reprobe_of"] != ["ac013"] or len(dkkeys["keys"]) != 1:
        sys_exit("KIT3 batch-keys class/budget/reprobe drift")

    # --- status logs --------------------------------------------------------------
    got_pass = parse_status1(KIT1_DIR / "output/status.log")
    sdj = (KIT2_DIR / "output/status.log").read_text().splitlines()
    if len(sdj) != KIT2_STATUS_LINES or sdj[0] != KIT2_STATUS_FIRST_LINE or sdj[-1] != KIT2_STATUS_FINAL_LINE:
        sys_exit("KIT2 status shape drift")
    if [l for l in sdj if l.endswith("TRUNCATED-RETRY")] != DJ_RETRY_LINES:
        sys_exit("KIT2 status retry rows drift")
    if [l for l in sdj if l.endswith(" WIN-HALT")] != DJ_WIN_HALT_LINES:
        sys_exit("KIT2 status WIN-HALT rows drift")
    if [l for l in sdj if " EXHAUSTED " in l] != DJ_EXHAUSTED_LINES:
        sys_exit("KIT2 status EXHAUSTED rows drift")
    dkstat = (KIT3_DIR / "output/status.log").read_text().splitlines()
    if len(dkstat) != KIT3_STATUS_LINES or dkstat[-1] != KIT3_STATUS_FINAL_LINE:
        sys_exit("KIT3 status shape drift")

    # --- two-pass raw verification -----------------------------------------------
    raws15 = {}
    for kid in PROBED_IDS:
        ref = two_pass(KIT1_RAW, kid)
        if ref["stones"] != 5 or ref["is_or"] != 0:
            sys_exit(f"{kid}: wrong depth/or bit")
        if ref["budget"] != BUDGET_KIT1:
            sys_exit(f"{kid}: kit1 budget drift")
        e = by_id.get(kid)
        if e is None:
            sys_exit(f"batch-keys missing {kid}")
        if ref["legal"] != int(e["legal"]) or ref["lo"] != e["lo"] or ref["hi"] != e["hi"]:
            sys_exit(f"{kid}: legal/key disagreement raw vs batch-keys")
        assert_final_pass_row(kid, (ref["budget"], ref["result"], ref["nodes"]), got_pass[kid])
        raws15[kid] = ref
    raws20 = {}
    for kid in EXH15_IDS:
        ref = two_pass(KIT2_RAW, kid)
        if ref["stones"] != 5 or ref["is_or"] != 0 or ref["budget"] != BUDGET_KIT2:
            sys_exit(f"{kid}: kit2 depth/budget drift")
        e = by_id.get(kid)
        if ref["legal"] != int(e["legal"]) or ref["lo"] != e["lo"] or ref["hi"] != e["hi"]:
            sys_exit(f"{kid}: kit2 raw/batch-keys disagreement")
        raws20[kid] = ref
        if kid == "ac006":
            if (ref["result"], ref["nodes"]) != (1, 18182847):
                sys_exit("ac006 decisive 20M WIN row drift")
        elif kid == "ac013":
            if (ref["result"], ref["nodes"]) != (0, DJ20_EXH_NODES):
                sys_exit("ac013 superseded 20M exhaustion row drift")
        else:
            if (ref["result"], ref["nodes"]) != (2, DJ20_NODES[kid]):
                sys_exit(f"{kid} decisive 20M LOSS row drift")
    r25 = two_pass(KIT3_RAW, "ac013")
    if (r25["budget"], r25["result"], r25["nodes"]) != (BUDGET_KIT3, 2, DK25_LOSS_NODES):
        sys_exit("ac013 decisive 25M LOSS row drift")
    if (r25["lo"], r25["hi"], r25["legal"]) != (raws15["ac013"]["lo"], raws15["ac013"]["hi"], raws15["ac013"]["legal"]):
        sys_exit("ac013 key/legal drift across generations")

    # --- supersede chain labels ----------------------------------------------------
    for kid in EXH15_IDS:
        if (raws15[kid]["result"], raws15[kid]["nodes"]) != (0, 15000000):
            sys_exit(f"{kid}: kit1 pair must be the pinned 15M exhaustion")
    if raws20["ac013"]["result"] != 0:
        sys_exit("ac013: DJ pair must remain exhausted at 20M (superseded by DK 25M)")

    # --- decisive labels -------------------------------------------------------------
    dec = {}
    for kid in PROBED_IDS:
        if kid in EXH15_IDS:
            dec[kid] = raws20[kid] if kid != "ac013" else r25
        else:
            dec[kid] = raws15[kid]
    loss_set = sorted(k for k in PROBED_IDS if dec[k]["result"] == 2)
    win_set = sorted(k for k in PROBED_IDS if dec[k]["result"] == 1)
    exh_set = sorted(k for k in PROBED_IDS if dec[k]["result"] == 0)
    if loss_set != sorted(ADOPTED_LOSS_IDS):
        sys_exit("decisive LOSS set != the 43 adopted candidates")
    if win_set != sorted(WIN_UNCONSUMED_IDS):
        sys_exit("decisive WIN set != the 11 unconsumed WIN keys")
    if exh_set:
        sys_exit(f"decisive EXHAUSTED non-empty: {exh_set}")

    # --- raw inventory: primaries + pinned sidecars ------------------------------------
    prim1 = sorted(p.name for p in KIT1_RAW.iterdir() if p.is_file())
    exp1 = sorted([f"{kid}.{tag}.out" for kid in PROBED_IDS for tag in ("p1", "p2")] + KIT1_SIDECARS)
    if prim1 != exp1:
        sys_exit(f"kit1 raw inventory drift: {sorted(set(prim1) ^ set(exp1))}")
    prim2 = sorted(p.name for p in KIT2_RAW.iterdir() if p.is_file())
    exp2 = sorted([f"{kid}.{tag}.out" for kid in EXH15_IDS for tag in ("p1", "p2")] + KIT2_SIDECARS)
    if prim2 != exp2:
        sys_exit(f"kit2 raw inventory drift: {sorted(set(prim2) ^ set(exp2))}")
    prim3 = sorted(p.name for p in KIT3_RAW.iterdir() if p.is_file())
    if prim3 != ["ac013.p1.out", "ac013.p2.out"]:
        sys_exit(f"kit3 raw inventory drift: {prim3}")

    # --- val-gates node-exact across hosts ----------------------------------------------
    for gate, (exp_b, exp_r, exp_n) in sorted(VAL_GATES.items()):
        for host in VAL_HOSTS:
            p = KIT1_DIR / f"val-gate/{gate}.{host}.out"
            if not p.is_file():
                sys_exit(f"kit1 val-gate file missing: {gate} {host}")
            row = parse_replay(p)
            if (row["budget"], row["result"], row["nodes"]) != (exp_b, exp_r, exp_n):
                sys_exit(f"kit1 val-gate {gate} {host} not node-exact")
    for gate, (exp_b, exp_r, exp_n) in sorted(KIT2_VG.items()):
        row = parse_replay(KIT2_DIR / f"val-gate/{gate}")
        if (row["budget"], row["result"], row["nodes"]) != (exp_b, exp_r, exp_n):
            sys_exit(f"kit2 val-gate {gate} not node-exact")
    for gate, (exp_b, exp_r, exp_n) in sorted(KIT3_VG.items()):
        row = parse_replay(KIT3_DIR / f"val-gate/{gate}")
        if (row["budget"], row["result"], row["nodes"]) != (exp_b, exp_r, exp_n):
            sys_exit(f"kit3 val-gate {gate} not node-exact")

    # --- gate the adopted keys against BASE / quarantine ---------------------------------
    emitted = set()
    for kid in ADOPTED_LOSS_IDS:
        key = norm_key(dec[kid])
        pins = ADOPTED_KEYS[kid]
        if key != pins["key"]:
            sys_exit(f"{kid}: raw key != pinned adopted key")
        if int(dec[kid]["nodes"]) != pins["nodes"] or int(dec[kid]["legal"]) != pins["legal"]:
            sys_exit(f"{kid}: adopted nodes/legal drift vs pins")
        if pins["decisive_budget"] != dec[kid]["budget"]:
            sys_exit(f"{kid}: decisive budget drift")
        e = by_id[kid]
        if int(e["s5_index"]) != pins["s5"] or int(e["membership_class_count"]) != pins["mcc"]:
            sys_exit(f"{kid}: batch-keys s5/mcc drift vs pins")
        if key in quarantined:
            sys_exit(f"{kid}: quarantined key {key}")
        if key in base_keys:
            sys_exit(f"{kid}: key already in canonical BASE {key}; fresh-increment gate")
        if key in emitted:
            sys_exit(f"{kid}: duplicate emitted key {key}")
        emitted.add(key)
    for kid in WIN_UNCONSUMED_IDS:
        w = WIN_UNCONSUMED[kid]
        key = w["key"]
        src = dec[kid]
        if key != norm_key(src):
            sys_exit(f"{kid}: WIN raw key != pin")
        if (src["result"], int(src["nodes"])) != (1, w["nodes"]):
            sys_exit(f"{kid}: WIN raw row != pin")
        e = by_id[kid]
        if int(e["s5_index"]) != w["s5"] or int(e["membership_class_count"]) != w["mcc"]:
            sys_exit(f"{kid}: WIN batch-keys s5/mcc drift")
        if key in base_keys or key in quarantined or key in emitted:
            sys_exit(f"unconsumed WIN key {kid} must appear in no cache/increment/quarantine here")

    # --- node totals per pass ------------------------------------------------------------
    n1 = n2 = 0
    for kid in ADOPTED_LOSS_IDS:
        rawdir = KIT1_RAW if ADOPTED_KEYS[kid]["raw_kit"] == "KIT1" else (KIT2_RAW if ADOPTED_KEYS[kid]["raw_kit"] == "KIT2" else KIT3_RAW)
        a = parse_replay(rawdir / f"{kid}.p1.out")
        b = parse_replay(rawdir / f"{kid}.p2.out")
        if (a["result"], a["nodes"]) != (2, ADOPTED_KEYS[kid]["nodes"]) or a["nodes"] != b["nodes"]:
            sys_exit(f"{kid}: adopted-row pass node disagreement")
        n1 += a["nodes"]; n2 += b["nodes"]
    if n1 != ADOPTED_TOTAL_NODES or n2 != ADOPTED_TOTAL_NODES:
        sys_exit(f"adopted packet node totals drift p1={n1} p2={n2} != {ADOPTED_TOTAL_NODES}")

    # --- emit increment + manifest ----------------------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    hdr = [
        "# n11 central-reply closure batch-30 (class 34269) 43-LOSS",
        "#   canonical-adoption increment (Part DN, 2026-11-24)",
        "# published batch-30 kit + Part DJ exh6-20M reprobe kit + Part",
        "#   DK 25M reprobe kit: ALL 54 of 54 keys carry honest two-pass",
        "#   probe labels.  43 keys resolved LOSS (38 at budget 15M kit",
        "#   raws, ac032/ac036/ac044/ac047 at the Part DJ 20M reprobe,",
        "#   ac013 at the Part DK 25M reprobe superseding its pinned 15M",
        "#   and 20M exhaustion pairs, nodes 21,954,135) and ARE this",
        "#   increment.  11 keys (ac002/ac003/ac020/ac026/ac027/ac034/",
        "#   ac041/ac045/ac048/ac054 at 15M and ac006 at the Part DJ",
        "#   20M reprobe) are probe-level WINs and stay UNCONSUMED: not",
        "#   adopted, not emitted, not in any canonical cache (WIN-row",
        "#   scrutiny is the separate C++ owner lane, pin 9193f5b6...;",
        "#   no completeness claim is made beyond the labels).",
        "# 2-pass node-exact exact-S5 verdicts, fresh cold, pinned",
        "#   jsreplay.js sha256",
        "#   845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# gates: three kit MANIFESTs sha-verified file-by-file (199+34+15",
        "#   files, the KIT2 output/-relative name quirk resolved against",
        "#   the published tree); 54+6+1 two-pass fresh-cold raw",
        "#   re-verification with '# replay_done' on both passes;",
        "#   honest-history status pins (79-line kit1 log: 56 PASS rows",
        "#   with the pinned ac001/ac002 restart duplicates, 11 pinned",
        "#   WIN-HALT rows, 6 pinned EXHAUSTED rows, 2 pinned MISMATCH",
        "#   rows resolved by pinned retries, 4 pinned TRUNCATED-RETRY",
        "#   markers; 14-line DJ log; 1-line DK log); the three-generation",
        "#   ac013 supersede chain byte-pinned; the DJ frozen-snapshot",
        "#   chain tie (base_status_log_sha256 == sha256 of the first",
        "#   2180 bytes of the 79-line status) and the DK prefix tie;",
        "#   val-gate node-exact across all published hosts (4 x 5 hosts",
        "#   at 15M + DJ 20M pair + DK 25M dkt/dkvv pair); adopted keys",
        "#   distinct, absent from BASE 60222707... (6,405 rows,",
        "#   WIN 158 / LOSS 6,247) and from the quarantine registry;",
        "#   the 11 WIN keys likewise absent everywhere (consumed",
        "#   nowhere); adopted per-pass node total {}".format(ADOPTED_TOTAL_NODES) + ",",
        "# ADOPTED set = the 43 decisive-LOSS keys; full != loss because",
        "#   eleven probe-level WIN rows exist and stay unconsumed.",
        "# The 43 LOSS rows ARE consumed into the canonical cache by the",
        "#   fail-closed union merger; 11x11 stays UNKNOWN; nodes are",
        "#   bookkeeping, never verdicts; class 34269 is NOT freed (its",
        "#   remaining unknown children are the eleven unconsumed WINs).",
    ]
    rows_for_sort = [(ADOPTED_KEYS[k]["key"][0], ADOPTED_KEYS[k]["key"][1], ADOPTED_KEYS[k]["nodes"]) for k in ADOPTED_LOSS_IDS]
    rowlines = [f"s5verdict,{lo},{hi},5,2,{nodes}" for lo, hi, nodes in sorted(rows_for_sort)]
    blob = ("\n".join(hdr + rowlines) + "\n").encode("utf-8")
    incr_path = OUT / "increment-b30loss43-20261124.cache"
    incr_path.write_bytes(blob)
    incr_sha = hashlib.sha256(blob).hexdigest()

    manifest = {
        "schema": "b30loss43-increments-manifest-v1",
        "batches": [{
            "batch": 30,
            "class_index": 34269,
            "keys_total": 54,
            "adopted_loss_ids": list(ADOPTED_LOSS_IDS),
            "already_adopted_ids": [],
            "unadopted_win_ids": list(WIN_UNCONSUMED_IDS),
            "exhausted_excluded_ids": [],
            "probed_ids": list(PROBED_IDS),
            "fragment_ids": [],
            "fileless_unprobed_count": 0,
            "fileless_unprobed_ids": [],
            "input_sha256": KIT1_KEYS_SHA,
            "status_log_sha256": KIT1_STATUS_SHA,
            "status_log_lines": KIT1_STATUS_LINES,
            "status_log_first_line": KIT1_STATUS_FIRST_LINE,
            "status_log_final_line": KIT1_STATUS_FINAL_LINE,
            "status_log_win_halt_lines": list(WIN_HALT_LINES),
            "status_log_exhausted_lines": list(EXHAUSTED_LINES),
            "status_log_mismatch_lines": list(MISMATCH_LINES),
            "status_log_retry_lines": list(RETRY_LINES),
            "kit_integrity": {"kit1_manifest_sha256": KIT1_MANIFEST_SHA, "kit1_files_verified": k1,
                                "kit2_manifest_sha256": KIT2_MANIFEST_SHA, "kit2_files_verified": k2,
                                "kit3_manifest_sha256": KIT3_MANIFEST_SHA, "kit3_files_verified": k3},
            "dj_reprobe": {
                "budget": BUDGET_KIT2, "keys": list(EXH15_IDS),
                "status_sha256": KIT2_STATUS_SHA, "status_lines": KIT2_STATUS_LINES,
                "resolved_loss_ids": ["ac032", "ac036", "ac044", "ac047"],
                "resolved_win_ids": ["ac006"], "remained_exhausted_ids": ["ac013"],
                "base_status_snapshot_sha256": KIT2_SNAPSHOT_SHA,
                "base_status_snapshot_bytes": KIT2_SNAPSHOT_BYTES,
            },
            "dk_reprobe": {
                "budget": BUDGET_KIT3, "keys": ["ac013"],
                "status_sha256": KIT3_STATUS_SHA, "status_lines": KIT3_STATUS_LINES,
                "resolved_loss_ids": ["ac013"],
                "superseded_15m_label": "EXHAUSTED (0, 15000000, kit1 pair)",
                "superseded_20m_label": "EXHAUSTED (0, 20000000, DJ pair)",
                "base_status_prefix8": KIT3_SNAPSHOT_PREFIX,
            },
            "val_gate_multi_host_node_exact": True,
            "total_nodes_pass_one": n1,
            "total_nodes_pass_two": n2,
            "stop_rule": "batch-30 probe-complete (54/54 keys carry honest two-pass labels: 38 LOSS @15M kit raws + 4 LOSS @20M DJ reprobe + 1 LOSS @25M DK reprobe = 43 adopted; the eleven probe-level WINs (10 @15M, ac006 @20M DJ) stay unconsumed pending the scrutiny-owner C++ gate; verdict not consumed)",
            "fragment_state": {},
        }],
        "resolved_ids": list(ADOPTED_LOSS_IDS),
        "loss_ids": list(ADOPTED_LOSS_IDS),
        "win_ids": list(WIN_UNCONSUMED_IDS),
        "unadopted_win_ids": list(WIN_UNCONSUMED_IDS),
        "exhausted_excluded_ids": [],
        "row_counts": {"probed_rows": 54, "adopted_loss_rows": 43, "prior_adopted_loss_rows": 0,
                        "wins": 11, "exhausted_excluded": 0, "fragments_unprobed": 0, "fileless_unprobed": 0},
        "sha256": {"loss": incr_sha},
        "full_packet_eq_loss_only": False,
        "full_packet_eq_loss_only_rationale":
            "the batch is probe-complete (54/54 honest labels) but the packet is "
            "NOT loss-only: eleven probe-level WIN rows stay UNCONSUMED and are NOT "
            "adopted; the adopted packet is the 43 fresh LOSS rows plus nothing "
            "else; no batch-30 row was adopted before; class 34269 is NOT freed "
            "(eleven unconsumed WIN children remain)",
        "win_scenario_exists": True,
        "win_scenario_note":
            "exactly eleven WIN rows exist (ac002/ac003/ac020/ac026/ac027/ac034/"
            "ac041/ac045/ac048/ac054 at 15M and ac006 at the Part DJ 20M reprobe "
            "superseding its pinned 15M exhaustion) and each stays unconsumed by "
            "this adoption (scrutiny owner C++ second-implementation gate pin "
            "9193f5b6...); loss-only adoption NEVER frees class 34269 while any "
            "of the eleven WIN children remain verdict-unconsumed",
        "unadopted_win_rows": [
            {"key_id": kid, "result": 1, "nodes": WIN_UNCONSUMED[kid]["nodes"],
              "legal": WIN_UNCONSUMED[kid]["legal"], "lo": WIN_UNCONSUMED[kid]["key"][0],
              "hi": WIN_UNCONSUMED[kid]["key"][1], "s5_index": WIN_UNCONSUMED[kid]["s5"],
              "decisive_budget": WIN_UNCONSUMED[kid]["decisive_budget"],
              "decisive_kit": WIN_UNCONSUMED[kid]["raw_kit"]}
            for kid in WIN_UNCONSUMED_IDS],
        "exhausted_rows": [],
        "fragment_rows_note":
            "batch-30 is probe-complete with NO fragment keys: the raw inventory is "
            "exactly 54 x {p1,p2} primary pairs across three generations plus the "
            "pinned truncated retry sidecars (4 in kit1, 6 in kit2), which are retry "
            "artifacts and not verdict rows",
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_sha256": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "base_cache_absent_hits_for_emitted": 0,
        "base_cache_prior_adoption_confirmed": 0,
        "quarantine_hits": 0,
        "interpretation_guard":
            "canonical 43-LOSS adoption increment: only the 43 fresh LOSS rows are "
            "consumed into the canonical cache via the fail-closed union merger; the "
            "eleven probe-level WINs are consumed NOWHERE (no verdict claim, no "
            "exclusion claim); all 54 batch-30 keys stay UNKNOWN as verdicts; "
            "adopting 43 LOSS rows does NOT free class 34269 (eleven unconsumed WIN "
            "children remain); 11x11 stays UNKNOWN; nodes are bookkeeping, never "
            "verdicts",
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"INCREMENT rows=43 loss_nodes={ADOPTED_TOTAL_NODES} -> {incr_path}")


if __name__ == "__main__":
    main()
