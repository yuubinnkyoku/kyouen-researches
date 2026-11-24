#!/usr/bin/env python3
"""Build the batch-31 (class 5804) 51-LOSS canonical-adoption increment, fail-closed.

Prepared for the Part DL adoption: the published batch-31 cumulative evidence
is byte-pinned through the published single batch-31 kit (Part CY scaffold +
takeover drives; kit MANIFEST 3481019545cc1ed6d86765130ea895915e5b18865dfd6ed29d673fdff2d98b9a, 194 files: README 1 + input
56 (55 per-key input csv + batch-keys.json) + scripts 6 + val-gate 20 (4 gates
x {input.csv, published-baseline.out, b31-host.out, d2-host.out,
tk-host.out})) plus the published Part DI reprobe kit (MANIFEST
31ac5acdc2fcacb58f1bf5e27ddcff3e6dd09be0885c434a084354a71de3a682, 40 files, adding the di-host val-gate outputs and the 30M
ad043 reprobe raws).  Every kit file is sha256-verified here file-by-file.

The batch is FULLY probed at probe level: all 55 of 55 keys carry honest
labels.  51 keys are resolved LOSS 2-pass fresh-cold at budget 15M; 3 keys
(ad024 / ad028 / ad055) are probe-level WINs at budget 15M and 1 key
(ad043) is a probe-level WIN at the higher 30M budget of the published
Part DI reprobe (its published 15M exhaustion (nodes 15,000,000) is
superseded by that resolution, recorded here byte-pinned).  All 4 WIN rows
stay UNCONSUMED: none is adopted here, none is emitted into any increment,
none is written into any canonical cache (WIN-row adoption is the separate
scrutiny-owner C++ second-implementation lane, pin 9193f5b6...).  The
adopted packet is the 51 fresh LOSS rows ad001..ad054 except
{ad024, ad028, ad043, ad055}; no batch-31 key was adopted canonically
before (BASE carries none of them).

The adoption base is the canonical exact-S5 verdict cache BASE = the Part
DB merged 6,354-row cache sha256 04b0a239... (the closure chain through the
Part DB batch-29 37-LOSS adoption), byte-pinned here; this maker ABORTS
against anything else.  Every adopted key is asserted fresh (absent from
BASE) and absent from the quarantine registry.  Every unconsumed WIN key
is likewise asserted absent from BASE (its verdict is consumed nowhere).

Fail-closed gates: batch-31 kit MANIFEST sha-verified file-by-file (194
files); Part DI kit MANIFEST sha-verified file-by-file (40 files); the
20 val-gate host files sha-verified and their (result, nodes) asserted
node-exact against the pinned expectations on all five hosts
(published-baseline / b31-host / d2-host / tk-host / di-host; wall_s
excluded); the raw replay rows of ALL 55 probed keys must be two-pass
node-exact with (stones, legal, is_or, budget, result, nodes, lo, hi)
identical on both passes and a completed "# replay_done" line on both
passes; the status.log (sha-pinned; 59 lines) must parse as exactly 55
PASS rows with (budget, result, nodes) agreement with the raws (each
key exactly once), exactly three pinned WIN-HALT rows (ad024 / ad028 /
ad055), exactly the one pinned ad043 EXHAUSTED row (the superseded 15M
exhaustion) and nothing else; the raw set must be exactly ad001..ad055 x
{p1,p2} (110 files; no sidecars, no fragments); ad043's 30M evidence in the
DI kit must be two-pass node-exact WIN (result 1, nodes 18,247,029, budget
30,000,000) and its 15M exhausted raw pair must be byte-pinned as the
superseded label; the DI kit sources/b31-status.log must byte-reproduce
the batch-31 kit status.log (chain cross-check); the DI kit
sources/canonical-cache-db-merged-b29loss37.cache must byte-reproduce the
BASE cache (chain cross-check); the DI anchor raws ad054/ad055 (30M) must
be node-exact against the published batch-31 15M raws; legal and (lo,hi)
must match the published batch-keys.json for every probed key; the 51
adopted keys are distinct, ABSENT from the canonical BASE cache and from
the quarantine registry; adopted-row node totals must agree on both
passes (237,596,711 per pass); the raw LOSS set over the 55 keys must be
exactly the 51 adopted candidates and the only non-LOSS raw labels of the
batch are the four pinned WIN rows (ad024/ad028/ad043/ad055).  Verdicts
are byte-taken from the raws.  The 51 LOSS rows ARE the only thing
consumed into the canonical cache by this Part; 11x11 stays UNKNOWN;
nodes are bookkeeping, never verdicts; class 5804 is NOT freed here
(four unconsumed WIN children remain, verdict-unconsumed).
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
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class2251-loss37-adoption-reaudit-20261124/output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-20261124.cache"
B31_DIR = ROOT / "research/experiments/n11-centralreply-closure-class5804-batch31-20261124"
DI_DIR = ROOT / "research/experiments/n11-centralreply-closure-class5804-b31ad043-reprobe30m-20261124"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"

MERGER = EXP / "scripts/s5_union_merge.py"
BASE_CACHE_SHA_EXPECTED = "04b0a23987a97518e276ea5ff966496facab22f93628cd5fbc682a04c3650556"
BASE_CACHE_ROWS_EXPECTED = 6354
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
JSREPLAY_SHA_EXPECTED = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
DB_MERGED_CACHE_CLONE_SHA_EXPECTED = "04b0a23987a97518e276ea5ff966496facab22f93628cd5fbc682a04c3650556"

# --- published batch-31 kit pins -------------------------------------------
B31_KEYS_SHA_EXPECTED = "d058fddc862c5f62b387eea7c7ac5b78f2c5063661371b388e5078772af4ff0e"
B31_MANIFEST_SHA_EXPECTED = "3481019545cc1ed6d86765130ea895915e5b18865dfd6ed29d673fdff2d98b9a"
B31_KIT_FILES_EXPECTED = 194
B31_STATUS_SHA_EXPECTED = "c69c2fec9d07e50dca6763fdb97acb5a05798b7852a1ab45be8e7a7a7889dd5b"
STATUS_LINES_EXPECTED = 59
STATUS_FINAL_LINE = "2026-11-24T06:57:11Z ad055 WIN-HALT"
WIN_HALT_LINES = [
    "2026-11-24T02:01:45Z ad024 WIN-HALT",
    "2026-11-24T02:05:32Z ad028 WIN-HALT",
    "2026-11-24T06:57:11Z ad055 WIN-HALT",
]
EXHAUSTED_LINES = [
    "2026-11-24T06:46:37Z ad043 EXHAUSTED 15000000,0,15000000",
]

# --- published Part DI reprobe kit pins -------------------------------------
DI_MANIFEST_SHA_EXPECTED = "31ac5acdc2fcacb58f1bf5e27ddcff3e6dd09be0885c434a084354a71de3a682"
DI_KIT_FILES_EXPECTED = 40
DI_STATUS_SHA_EXPECTED = "f681a3c47c00f2f14ba670162a3606903ebde246df6b8ea634888730a582c2c5"
DI_STATUS_FINAL_LINE = "2026-11-24T07:16:30Z ad043 WIN-HALT"
DI_AD043_P1_SHA = "a17572d9768cc341f2618e3a6c79b549acbe19c2b514e57662fc1386f22f8049"
DI_AD043_P2_SHA = "dd405f061a2c485cda4467752e3579cc897b1f421ee7b2117d9bda3e7ba7ee01"
DI_B31STATUS_CLONE_SHA = "c69c2fec9d07e50dca6763fdb97acb5a05798b7852a1ab45be8e7a7a7889dd5b"
DI_ANCHOR54_SHA = "c2d1500b831836c7791d96d3fab5f344c59bff506d96854c510a2c504e9ae1e0"
DI_ANCHOR55_SHA = "61704c55151f00db87c59285e40ba01180da5b762c9bb73ecf285fe93b9c34dd"
DI_EXH15M_P1_SHA = "5f3bf5bc6f6bc636c7aa6d7e72619530ce2a0b918558d635ac7191b27c729d11"
DI_EXH15M_P2_SHA = "1feacf0c91cfaa72e9f3965bc0be83beb6aebbba005a74f0fbbdcfffb4b4db15"

# --- adopted packet ----------------------------------------------------------
BUDGET = 15000000
ADOPTED_LOSS_IDS = [
    'ad001',
    'ad002',
    'ad003',
    'ad004',
    'ad005',
    'ad006',
    'ad007',
    'ad008',
    'ad009',
    'ad010',
    'ad011',
    'ad012',
    'ad013',
    'ad014',
    'ad015',
    'ad016',
    'ad017',
    'ad018',
    'ad019',
    'ad020',
    'ad021',
    'ad022',
    'ad023',
    'ad025',
    'ad026',
    'ad027',
    'ad029',
    'ad030',
    'ad031',
    'ad032',
    'ad033',
    'ad034',
    'ad035',
    'ad036',
    'ad037',
    'ad038',
    'ad039',
    'ad040',
    'ad041',
    'ad042',
    'ad044',
    'ad045',
    'ad046',
    'ad047',
    'ad048',
    'ad049',
    'ad050',
    'ad051',
    'ad052',
    'ad053',
    'ad054'
]
ADOPTED_NODES = {
    "ad001": 5609720,
    "ad002": 4555434,
    "ad003": 5940995,
    "ad004": 3434932,
    "ad005": 3420177,
    "ad006": 7296844,
    "ad007": 7840993,
    "ad008": 2362665,
    "ad009": 2479959,
    "ad010": 12273095,
    "ad011": 2914995,
    "ad012": 5968986,
    "ad013": 5270933,
    "ad014": 3337929,
    "ad015": 4271124,
    "ad016": 3479933,
    "ad017": 2805657,
    "ad018": 7948923,
    "ad019": 6567285,
    "ad020": 4663738,
    "ad021": 4826218,
    "ad022": 3183609,
    "ad023": 2795664,
    "ad025": 2750868,
    "ad026": 3940244,
    "ad027": 1624906,
    "ad029": 2936438,
    "ad030": 3146845,
    "ad031": 5946707,
    "ad032": 11268913,
    "ad033": 5883887,
    "ad034": 4885748,
    "ad035": 3582819,
    "ad036": 1675597,
    "ad037": 5417573,
    "ad038": 4503724,
    "ad039": 4962308,
    "ad040": 1723362,
    "ad041": 2168706,
    "ad042": 3179879,
    "ad044": 2251201,
    "ad045": 7781306,
    "ad046": 3560629,
    "ad047": 11064379,
    "ad048": 10316369,
    "ad049": 3146801,
    "ad050": 1897590,
    "ad051": 3580351,
    "ad052": 5410550,
    "ad053": 4094246,
    "ad054": 1644957,
}
ADOPTED_KEYS = {
    "ad001": (6053400849273585664, 0),
    "ad002": (6052837899320164352, 128),
    "ad003": (6053400849139367937, 0),
    "ad004": (6053400849139367938, 0),
    "ad005": (6053400849139367940, 0),
    "ad006": (6053400849139367944, 0),
    "ad007": (6053400849139367952, 0),
    "ad008": (6053400849139367968, 0),
    "ad009": (6053400849139369984, 0),
    "ad010": (6053400849139372032, 0),
    "ad011": (6053400849139376128, 0),
    "ad012": (6053400849139384320, 0),
    "ad013": (6053400849139400704, 0),
    "ad014": (6053400849143562240, 0),
    "ad015": (6053400849147756544, 0),
    "ad016": (6053400849156145152, 0),
    "ad017": (6053400849172922368, 0),
    "ad018": (6053400849206476800, 0),
    "ad019": (6053400857729302528, 0),
    "ad020": (6053400866319237120, 0),
    "ad021": (6053400883499106304, 0),
    "ad022": (6053400917858844672, 0),
    "ad023": (6053400986578321408, 0),
    "ad025": (6053418441325412352, 0),
    "ad026": (6053436033511456768, 0),
    "ad027": (6053471217883545600, 0),
    "ad029": (6053400849139367936, 4),
    "ad030": (6052837907775881216, 128),
    "ad031": (6052837899190140928, 128),
    "ad032": (6052837899185948672, 128),
    "ad033": (6052837899185946625, 128),
    "ad034": (6053400849139367936, 8),
    "ad035": (6052837916365815808, 128),
    "ad036": (6052837899194335232, 128),
    "ad037": (6052837899185950720, 128),
    "ad038": (6052837899185946626, 128),
    "ad039": (6053400849139367936, 16),
    "ad040": (6052837933545684992, 128),
    "ad041": (6052837899202723840, 128),
    "ad042": (6052837899185954816, 128),
    "ad044": (6053400849139367936, 32),
    "ad045": (6052837967905423360, 128),
    "ad046": (6052837899185963008, 128),
    "ad047": (6052837899185946632, 128),
    "ad048": (6053400849139367936, 64),
    "ad049": (6052838036624900096, 128),
    "ad050": (6052837899253055488, 128),
    "ad051": (6052837899185979392, 128),
    "ad052": (6052837899185946640, 128),
    "ad053": (6052837899185946656, 128),
    "ad054": (6052838174063853568, 128),
}
ADOPTED_LEGAL = {
    "ad001": 92,
    "ad002": 94,
    "ad003": 96,
    "ad004": 97,
    "ad005": 94,
    "ad006": 96,
    "ad007": 100,
    "ad008": 94,
    "ad009": 100,
    "ad010": 89,
    "ad011": 94,
    "ad012": 92,
    "ad013": 97,
    "ad014": 97,
    "ad015": 96,
    "ad016": 90,
    "ad017": 89,
    "ad018": 82,
    "ad019": 100,
    "ad020": 97,
    "ad021": 95,
    "ad022": 89,
    "ad023": 96,
    "ad025": 93,
    "ad026": 99,
    "ad027": 84,
    "ad029": 100,
    "ad030": 100,
    "ad031": 98,
    "ad032": 95,
    "ad033": 99,
    "ad034": 98,
    "ad035": 90,
    "ad036": 87,
    "ad037": 94,
    "ad038": 101,
    "ad039": 92,
    "ad040": 89,
    "ad041": 84,
    "ad042": 99,
    "ad044": 91,
    "ad045": 89,
    "ad046": 92,
    "ad047": 94,
    "ad048": 86,
    "ad049": 92,
    "ad050": 91,
    "ad051": 100,
    "ad052": 101,
    "ad053": 92,
    "ad054": 86,
}
ADOPTED_S5 = {
    "ad001": 97381,
    "ad002": 102238,
    "ad003": 119474,
    "ad004": 125125,
    "ad005": 130687,
    "ad006": 136105,
    "ad007": 141315,
    "ad008": 144458,
    "ad009": 148458,
    "ad010": 152721,
    "ad011": 156973,
    "ad012": 161166,
    "ad013": 165259,
    "ad014": 170887,
    "ad015": 174498,
    "ad016": 177679,
    "ad017": 180752,
    "ad018": 183816,
    "ad019": 186724,
    "ad020": 189532,
    "ad021": 192176,
    "ad022": 194523,
    "ad023": 196763,
    "ad025": 199913,
    "ad026": 201807,
    "ad027": 203738,
    "ad029": 211491,
    "ad030": 211529,
    "ad031": 211582,
    "ad032": 211655,
    "ad033": 211693,
    "ad034": 211744,
    "ad035": 211788,
    "ad036": 211830,
    "ad037": 211891,
    "ad038": 211921,
    "ad039": 211965,
    "ad040": 211996,
    "ad041": 212031,
    "ad042": 212087,
    "ad044": 212160,
    "ad045": 212175,
    "ad046": 212243,
    "ad047": 212273,
    "ad048": 212307,
    "ad049": 212340,
    "ad050": 212372,
    "ad051": 212404,
    "ad052": 212432,
    "ad053": 212464,
    "ad054": 212512,
}
MEMBERSHIP_EXPECT = {
    "ad001": 3,
    "ad002": 3,
    "ad003": 4,
    "ad004": 4,
    "ad005": 4,
    "ad006": 4,
    "ad007": 4,
    "ad008": 3,
    "ad009": 4,
    "ad010": 4,
    "ad011": 4,
    "ad012": 4,
    "ad013": 4,
    "ad014": 4,
    "ad015": 4,
    "ad016": 4,
    "ad017": 4,
    "ad018": 4,
    "ad019": 4,
    "ad020": 4,
    "ad021": 4,
    "ad022": 4,
    "ad023": 4,
    "ad025": 4,
    "ad026": 4,
    "ad027": 4,
    "ad029": 4,
    "ad030": 4,
    "ad031": 4,
    "ad032": 4,
    "ad033": 4,
    "ad034": 4,
    "ad035": 4,
    "ad036": 4,
    "ad037": 4,
    "ad038": 4,
    "ad039": 4,
    "ad040": 4,
    "ad041": 4,
    "ad042": 4,
    "ad044": 4,
    "ad045": 4,
    "ad046": 4,
    "ad047": 4,
    "ad048": 4,
    "ad049": 4,
    "ad050": 4,
    "ad051": 4,
    "ad052": 4,
    "ad053": 3,
    "ad054": 3,
}
ADOPTED_TOTAL_NODES = 237596711
PROBED_IDS = [
    'ad001',
    'ad002',
    'ad003',
    'ad004',
    'ad005',
    'ad006',
    'ad007',
    'ad008',
    'ad009',
    'ad010',
    'ad011',
    'ad012',
    'ad013',
    'ad014',
    'ad015',
    'ad016',
    'ad017',
    'ad018',
    'ad019',
    'ad020',
    'ad021',
    'ad022',
    'ad023',
    'ad024',
    'ad025',
    'ad026',
    'ad027',
    'ad028',
    'ad029',
    'ad030',
    'ad031',
    'ad032',
    'ad033',
    'ad034',
    'ad035',
    'ad036',
    'ad037',
    'ad038',
    'ad039',
    'ad040',
    'ad041',
    'ad042',
    'ad043',
    'ad044',
    'ad045',
    'ad046',
    'ad047',
    'ad048',
    'ad049',
    'ad050',
    'ad051',
    'ad052',
    'ad053',
    'ad054',
    'ad055'
]
WIN_UNCONSUMED_IDS = ["ad024", "ad028", "ad043", "ad055"]
WIN_UNCONSUMED = {
    "ad024": {
        "key_id": 'ad024',
        "result": 1,
        "nodes": 4360661,
        "legal": 86,
        "lo": 6053401124017274880,
        "hi": 0,
        "s5_index": 198576,
        "membership_class_count": 3,
        "decisive_budget": 15000000,
},
    "ad028": {
        "key_id": 'ad028',
        "result": 1,
        "nodes": 12803283,
        "legal": 82,
        "lo": 6053682324116078592,
        "hi": 0,
        "s5_index": 207094,
        "membership_class_count": 3,
        "decisive_budget": 15000000,
},
    "ad043": {
        "key_id": 'ad043',
        "result": 1,
        "nodes": 18247029,
        "legal": 87,
        "lo": 6052837899185946628,
        "hi": 128,
        "s5_index": 212115,
        "membership_class_count": 4,
        "decisive_budget": 30000000,
},
    "ad055": {
        "key_id": 'ad055',
        "result": 1,
        "nodes": 3364655,
        "legal": 92,
        "lo": 6053400849139367936,
        "hi": 128,
        "s5_index": 212536,
        "membership_class_count": 2,
        "decisive_budget": 15000000,
},
}

# --- val-gate five-host pins --------------------------------------------------
HOST_PINS = {
    "at2m-s5-1152921504606851072-536870946": {
        "input_csv": 'ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348',
        "published_baseline": '6e902ab147b117bb09216070f272969418247f5eb73870bf7705c8220fc9c35c',
        "b31_host": 'ff4dbb8344400c6cc629038e833110e4b5ada5bf24bfa70d07a525d159276a22',
        "d2_host": 'ff4dbb8344400c6cc629038e833110e4b5ada5bf24bfa70d07a525d159276a22',
        "tk_host": 'ff4dbb8344400c6cc629038e833110e4b5ada5bf24bfa70d07a525d159276a22',
        "di_host": 'ff4dbb8344400c6cc629038e833110e4b5ada5bf24bfa70d07a525d159276a22',
},
    "at2m-s5-1188950301626860544-536870912": {
        "input_csv": '56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62',
        "published_baseline": 'eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24',
        "b31_host": 'eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24',
        "d2_host": 'eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24',
        "tk_host": '661a2842573f3a92df28bc4fdaf2feace2ae63717a73e140384c64039666b551',
        "di_host": 'eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24',
},
    "first-15m-s5-1152921504606851072-536870946": {
        "input_csv": 'ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348',
        "published_baseline": '8035fe54f8c79dd44c4c80d6b38e4ad39d3d4660eaf57a32799969087b8a5591',
        "b31_host": '8035fe54f8c79dd44c4c80d6b38e4ad39d3d4660eaf57a32799969087b8a5591',
        "d2_host": '2e8c1dd59de4ed011684c877e2117dc992195015992647f1418370c1732ae21e',
        "tk_host": '2e8c1dd59de4ed011684c877e2117dc992195015992647f1418370c1732ae21e',
        "di_host": '8675ae4b4904485d5ffde72578342d69668a5c8bd39b82d93193177f515ebafb',
},
    "second-15m-s5-1188950301626860544-536870912": {
        "input_csv": '56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62',
        "published_baseline": '91dffdec33a409bc3e5f6eb50c0ea95313574ef74d0692c5912a0814946de1fb',
        "b31_host": 'c3d1577d0663f62ad04c370d1194f25ca2359de229c9fc72bd883abb28268f5f',
        "d2_host": '9d2ebcf15cb8c05ce5cd4e52cf34068ad5e71056339f38017ac034d41645d6ce',
        "tk_host": '45cb1348c0a805ddff4b7d7a9db39cf56cd91f0669dae8f385f0ee7c33d2e4e2',
        "di_host": '45cb1348c0a805ddff4b7d7a9db39cf56cd91f0669dae8f385f0ee7c33d2e4e2',
},
}
VAL_GATE_EXPECT = {
    "at2m-s5-1152921504606851072-536870946": (0, 2000000),
    "at2m-s5-1188950301626860544-536870912": (0, 2000000),
    "first-15m-s5-1152921504606851072-536870946": (2, 3651923),
    "second-15m-s5-1188950301626860544-536870912": (2, 5040200),
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
                "lo": int(parts[9]), "hi": int(parts[10]),
            }
    if rows_seen != 1 or row is None:
        sys_exit(f"expected exactly one replay row in {path}")
    return row


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
        # regenerated-maker fix (post-incident): the two published kit MANIFESTs
        # record work-tree-relative paths (rooted at the repo root), so resolve
        # against ROOT as well as the kit dir; sha content-check stays fail-closed.
        p = dirp / rel
        if not p.is_file():
            p = ROOT / rel
        if not p.is_file():
            sys_exit(f"kit {dirp.name} file missing: {rel}")
        if sha(p) != want:
            sys_exit(f"kit {dirp.name} file sha drift: {rel}")
        verified += 1
    if verified != kit_files:
        sys_exit(f"kit {dirp.name} files verified {verified} != {kit_files}")
    return verified


def two_pass(kid: str):
    variants = {}
    for tag in ("p1", "p2"):
        p = B31_DIR / f"output/raw/{kid}.{tag}.out"
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
            sys_exit(f"{kid}: pass mismatch {tag} {r} vs p1 {ref}")
    return ref


def parse_status(path: Path):
    lines = path.read_text().splitlines()
    if len(lines) != STATUS_LINES_EXPECTED:
        sys_exit(f"status lines {len(lines)} != {STATUS_LINES_EXPECTED}")
    if lines[-1] != STATUS_FINAL_LINE:
        sys_exit(f"status final line drift: {lines[-1]!r}")
    joined = "\n".join(lines)
    if re.search(r"\b(TRUNCATED|EXECUTION-COMPLETE|P1-FAIL|MISMATCH)\b", joined):
        sys_exit("status.log carries an out-of-scope record")
    for wl in WIN_HALT_LINES:
        if lines.count(wl) != 1:
            sys_exit(f"status.log must carry exactly the one pinned row: {wl!r}")
    for el in EXHAUSTED_LINES:
        if lines.count(el) != 1:
            sys_exit(f"status.log must carry exactly the one pinned row: {el!r}")
    halts = [l for l in lines if l.endswith(" WIN-HALT")]
    if sorted(halts) != sorted(WIN_HALT_LINES):
        sys_exit(f"status.log WIN-HALT rows {halts} != the three pinned rows")
    exhs = [l for l in lines if " EXHAUSTED " in l]
    if exhs != EXHAUSTED_LINES:
        sys_exit(f"status.log EXHAUSTED rows {exhs} != the one pinned ad043 row")
    got = {}
    for line in lines:
        if line in WIN_HALT_LINES or line in EXHAUSTED_LINES:
            continue
        m = re.match(r"^(\S+) (ad\d{3}) PASS (\d+),(\d+),(\d+)$", line)
        if not m:
            sys_exit(f"status line not a clean PASS row: {line!r}")
        kid, b, r, n = m.group(2), int(m.group(3)), int(m.group(4)), int(m.group(5))
        if kid in got:
            sys_exit(f"status key {kid} appears more than once (each-once gate)")
        if kid not in PROBED_IDS:
            sys_exit(f"status key {kid} is not one of the 55 probed keys")
        got[kid] = (b, r, n)
    if set(got) != set(PROBED_IDS) or len(got) != 55:
        sys_exit("status probed set != the 55 probed keys")
    return got, lines


def main() -> None:
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys_exit("base cache sha drift")
    merger = MERGER
    if sha(merger) != MERGER_SHA_EXPECTED:
        sys_exit("fail-closed union merger (scripts/s5_union_merge.py) sha drift: "
                 "this Part must use the pinned merger byte-for-byte")
    if sha(B31_DIR / "scripts/jsreplay.js") != JSREPLAY_SHA_EXPECTED:
        sys_exit("batch-31 kit jsreplay.js sha drift (pinned solver image)")

    base_keys = {}
    with BASE_CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].lstrip().startswith("#"):
                continue
            base_keys[(int(row[1]), int(row[2]))] = (int(row[4]), int(row[5]))
    if len(base_keys) != BASE_CACHE_ROWS_EXPECTED:
        sys_exit(f"base cache rows {len(base_keys)} != {BASE_CACHE_ROWS_EXPECTED}")
    q = json.loads(QUARANTINE.read_text())
    quarantined = {tuple(e["key"]) for e in q["entries"] if e.get("active")}

    # --- kit integrity: the published batch-31 kit, file-by-file -------------
    kit_verified = verify_kit(B31_DIR, B31_MANIFEST_SHA_EXPECTED, B31_KIT_FILES_EXPECTED)
    if sha(B31_DIR / "input/batch-keys.json") != B31_KEYS_SHA_EXPECTED:
        sys_exit("batch-keys.json sha drift")
    # --- kit integrity: the published Part DI reprobe kit, file-by-file ------
    di_verified = verify_kit(DI_DIR, DI_MANIFEST_SHA_EXPECTED, DI_KIT_FILES_EXPECTED)
    if sha(DI_DIR / "sources/b31-status.log") != DI_B31STATUS_CLONE_SHA or \
            DI_B31STATUS_CLONE_SHA != B31_STATUS_SHA_EXPECTED:
        sys_exit("DI kit sources/b31-status.log does not byte-reproduce the batch-31 status.log")
    if sha(DI_DIR / "sources/canonical-cache-db-merged-b29loss37.cache") != DB_MERGED_CACHE_CLONE_SHA_EXPECTED or \
            DB_MERGED_CACHE_CLONE_SHA_EXPECTED != BASE_CACHE_SHA_EXPECTED:
        sys_exit("DI kit canonical-cache clone does not byte-reproduce BASE (chain drift)")
    if sha(DI_DIR / "output/raw/ad043.p1.out") != DI_AD043_P1_SHA or \
            sha(DI_DIR / "output/raw/ad043.p2.out") != DI_AD043_P2_SHA:
        sys_exit("DI ad043 30M raw sha drift")
    if sha(DI_DIR / "output/status.log") != DI_STATUS_SHA_EXPECTED:
        sys_exit("DI status.log sha drift")

    # --- batch-keys -----------------------------------------------------------
    bk_all = json.loads((B31_DIR / "input/batch-keys.json").read_text())
    if bk_all["schema"] != "n11-centralreply-closure-class5804-batch31-input-v1":
        sys_exit(f"batch-keys schema drift: {bk_all['schema']}")
    if bk_all["class_index"] != 5804 or bk_all["budget"] != BUDGET:
        sys_exit("batch-keys class/budget drift")
    if bk_all["closure_class_rank_in_published_base"] != 38:
        sys_exit("batch-keys closure rank drift (kit frozen at selection)")
    if int(bk_all["published_base_canonical_rows"]) != 6317:
        sys_exit("batch-keys published_base_canonical_rows drift (kit frozen at selection)")
    if bk_all["class_mask"] != ["6053400849139367936", "0"]:
        sys_exit("batch-keys class mask drift")
    by_id = {k["key_id"]: k for k in bk_all["keys"]}
    if len(by_id) != 55:
        sys_exit(f"batch-keys key count {len(by_id)} != 55")

    # --- status.log picture ----------------------------------------------------
    if sha(B31_DIR / "output/status.log") != B31_STATUS_SHA_EXPECTED:
        sys_exit("status.log sha drift")
    status, slines = parse_status(B31_DIR / "output/status.log")

    # --- two-pass raw verification of all 55 probed keys ----------------------
    raws = {}
    for kid in PROBED_IDS:
        ref = two_pass(kid)
        if ref["budget"] != BUDGET or ref["stones"] != 5 or ref["is_or"] != 0:
            sys_exit(f"{kid}: wrong depth/budget {ref}")
        bk = by_id.get(kid)
        if bk is None:
            sys_exit(f"batch-keys.json missing {kid}")
        if ref["legal"] != int(bk["legal"]):
            sys_exit(f"{kid}: legal mismatch raw={ref['legal']} keys={bk['legal']}")
        if (ref["lo"], ref["hi"]) != (int(bk["lo"]), int(bk["hi"])):
            sys_exit(f"{kid}: key mismatch raw=({ref['lo']},{ref['hi']}) keys=({bk['lo']},{bk['hi']})")
        if status.get(kid) != (ref["budget"], ref["result"], ref["nodes"]):
            sys_exit(f"{kid}: status.log disagreement {status.get(kid)} vs raw {ref}")
        raws[kid] = ref
    loss_set = sorted(k for k, r in raws.items() if r["result"] == 2)
    win_set = sorted(k for k, r in raws.items() if r["result"] == 1)
    exh_set = sorted(k for k, r in raws.items() if r["result"] == 0)
    if win_set != ["ad024", "ad028", "ad055"]:
        sys_exit(f"the only 15M WINs over the probed batch must be [ad024, ad028, ad055], got {win_set}")
    if exh_set != ["ad043"]:
        sys_exit(f"the only 15M EXHAUSTED over the probed batch must be [ad043], got {exh_set}")
    if loss_set != sorted(ADOPTED_LOSS_IDS):
        sys_exit("the raw LOSS set != the 51 adopted candidates")

    # --- raw file inventory: exactly 110 pass files, no sidecars/fragments ----
    raw_dir = B31_DIR / "output/raw"
    present = sorted(p.name for p in raw_dir.iterdir() if p.is_file())
    expected_files = sorted(f"{kid}.{tag}.out" for kid in PROBED_IDS for tag in ("p1", "p2"))
    if present != expected_files:
        sys_exit(f"raw inventory drift: {sorted(set(present) ^ set(expected_files))}")

    # --- ad043 supersede chain: 15M exhausted pair + DI 30M WIN pair ----------
    if sha(B31_DIR / "output/raw/ad043.p1.out") != DI_EXH15M_P1_SHA or \
            sha(B31_DIR / "output/raw/ad043.p2.out") != DI_EXH15M_P2_SHA:
        sys_exit("batch-31 15M ad043 raw pair sha drift vs the DI kit exh15m clones")
    r43_15m = raws["ad043"]
    if (r43_15m["result"], r43_15m["nodes"]) != (0, 15000000):
        sys_exit("the superseded 15M ad043 label must be the pinned exhaustion")
    d1 = parse_replay(DI_DIR / "output/raw/ad043.p1.out")
    d2 = parse_replay(DI_DIR / "output/raw/ad043.p2.out")
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
    if tuple(d1[f] for f in fields) != tuple(d2[f] for f in fields):
        sys_exit("DI ad043 30M raw two-pass mismatch")
    if (d1["budget"], d1["result"], d1["nodes"]) != (30000000, 1, 18247029):
        sys_exit("DI ad043 30M raw must be the pinned WIN row (1, 18247029)")
    dstatus = (DI_DIR / "output/status.log").read_text().splitlines()
    if dstatus[-1] != DI_STATUS_FINAL_LINE or len(dstatus) != 5:
        sys_exit("DI status.log shape drift")
    if dstatus[0] != "2026-11-24T07:12:24Z ad054 PASS 30000000,2,1644957" or \
            dstatus[1] != "2026-11-24T07:12:58Z ad055 PASS 30000000,1,3364655":
        sys_exit("DI status anchor rows drift")
    a54 = parse_replay(DI_DIR / "sources/anchor-15m/ad054.p1.out")
    a55 = parse_replay(DI_DIR / "sources/anchor-15m/ad055.p1.out")
    if (a54["result"], a54["nodes"]) != (raws["ad054"]["result"], raws["ad054"]["nodes"]):
        sys_exit("DI anchor ad054 not node-exact vs the published 15M raw")
    if (a55["result"], a55["nodes"]) != (raws["ad055"]["result"], raws["ad055"]["nodes"]):
        sys_exit("DI anchor ad055 not node-exact vs the published 15M raw")
    if sha(DI_DIR / "sources/anchor-15m/ad054.p1.out") != DI_ANCHOR54_SHA or \
            sha(DI_DIR / "sources/anchor-15m/ad055.p1.out") != DI_ANCHOR55_SHA:
        sys_exit("DI anchor raw sha drift")

    # --- gate the adopted keys against BASE / quarantine -------------------------
    emitted_keys = set()
    for kid in ADOPTED_LOSS_IDS:
        key = (raws[kid]["lo"], raws[kid]["hi"])
        if key != ADOPTED_KEYS[kid]:
            sys_exit(f"{kid}: raw key != pinned adopted key")
        if int(by_id[kid]["s5_index"]) != ADOPTED_S5[kid]:
            sys_exit(f"{kid}: batch-keys s5 drift")
        if int(by_id[kid]["membership_class_count"]) != MEMBERSHIP_EXPECT[kid]:
            sys_exit(f"{kid}: batch-keys membership drift")
        if key in quarantined:
            sys_exit(f"{kid}: quarantined key {key}")
        if key in base_keys:
            sys_exit(f"{kid}: key already in canonical BASE cache {key} "
                     f"(base={base_keys[key]}, raw=(result {raws[kid]['result']}, "
                     f"nodes {raws[kid]['nodes']})); fresh-increment gate")
        if key in emitted_keys:
            sys_exit(f"{kid}: duplicate emitted key {key}")
        emitted_keys.add(key)

    # --- the unconsumed WIN keys (consumed nowhere) ---------------------------
    for kid in WIN_UNCONSUMED_IDS:
        w = WIN_UNCONSUMED[kid]
        wkey = (w["lo"], w["hi"])
        if kid == "ad043":
            src = d1
            exp_15m = (0, 15000000)
        else:
            src = raws[kid]
            exp_15m = (w["result"], w["nodes"])
        if (src["lo"], src["hi"]) != wkey or src["legal"] != w["legal"]:
            sys_exit(f"{kid}: raw key/legal != pinned WIN pin")
        if (src["result"], src["nodes"]) != (w["result"], w["nodes"]):
            sys_exit(f"{kid}: raw row != pinned WIN pin: {src}")
        if (raws[kid]["result"], raws[kid]["nodes"]) != exp_15m:
            sys_exit(f"{kid}: batch-kit 15M label disagree with the pinned basis")
        if int(by_id[kid]["s5_index"]) != w["s5_index"]:
            sys_exit(f"{kid}: batch-keys s5 drift")
        if int(by_id[kid]["membership_class_count"]) != w["membership_class_count"]:
            sys_exit(f"{kid}: batch-keys membership drift")
        if wkey in base_keys or wkey in quarantined or wkey in emitted_keys:
            sys_exit(f"the unconsumed WIN key {kid} must appear in no canonical cache/increment/quarantine here")

    # --- the 51 fresh adopted LOSS rows -----------------------------------------
    nodes_p1_total = 0
    nodes_p2_total = 0
    for kid in ADOPTED_LOSS_IDS:
        ref = raws[kid]
        if ref["result"] != 2:
            sys_exit(f"{kid}: adopted row must be result 2, got {ref['result']}")
        if ref["nodes"] != ADOPTED_NODES[kid]:
            sys_exit(f"{kid}: adopted-row nodes drift {ref['nodes']} != {ADOPTED_NODES[kid]}")
        if ref["legal"] != ADOPTED_LEGAL[kid]:
            sys_exit(f"{kid}: adopted-row legal drift")
        nodes_p1_total += ref["nodes"]
        n_p2 = sum(int(line.split(",")[7])
                   for line in (B31_DIR / f"output/raw/{kid}.p2.out").read_text().splitlines()
                   if line.startswith("replay,"))
        nodes_p2_total += n_p2
        if n_p2 != ref["nodes"]:
            sys_exit(f"{kid}: adopted-row pass node totals disagree: {n_p2} vs {ref['nodes']}")
    if nodes_p1_total != ADOPTED_TOTAL_NODES or nodes_p2_total != ADOPTED_TOTAL_NODES:
        sys_exit(f"adopted packet node totals drift p1={nodes_p1_total} p2={nodes_p2_total} "
                 f"!= {ADOPTED_TOTAL_NODES}")

    # --- val-gate five-host node-exact cross-check -----------------------------
    host_verified = 0
    for gate, pins in sorted(HOST_PINS.items()):
        if sha(B31_DIR / f"val-gate/{gate}.input.csv") != pins["input_csv"]:
            sys_exit(f"val-gate input csv sha drift for {gate}")
        exp_r, exp_n = VAL_GATE_EXPECT[gate]
        exp_b = 2000000 if exp_r == 0 else 15000000
        host_file_map = {
            "published_baseline": B31_DIR / f"val-gate/{gate}.published-baseline.out",
            "b31_host": B31_DIR / f"val-gate/{gate}.b31-host.out",
            "d2_host": B31_DIR / f"val-gate/{gate}.d2-host.out",
            "tk_host": B31_DIR / f"val-gate/{gate}.tk-host.out",
            "di_host": DI_DIR / f"val-gate/{gate}.di-host.out",
        }
        for host_key, p in sorted(host_file_map.items()):
            if not p.is_file():
                sys_exit(f"val-gate file missing for {gate} host {host_key}")
            if sha(p) != pins[host_key]:
                sys_exit(f"val-gate sha drift: {gate} host {host_key}")
            row = parse_replay(p)
            if (row["budget"], row["result"], row["nodes"]) != (exp_b, exp_r, exp_n):
                sys_exit(f"val-gate {gate} host {host_key} not node-exact "
                         f"({row['result']},{row['nodes']}) != ({exp_r},{exp_n})")
            host_verified += 1
    if host_verified != 20:
        sys_exit(f"val-gate host files verified {host_verified} != 20")

    # --- expected val-gate budgets match the raws (adaptive 2M / 15M) -----------
    for gate in ("first-15m-s5-1152921504606851072-536870946",
                 "second-15m-s5-1188950301626860544-536870912"):
        row = parse_replay(B31_DIR / f"val-gate/{gate}.b31-host.out")
        if row["budget"] != BUDGET:
            sys_exit("val-gate 15M pattern budget drift")

    # --- emit the increment + manifest ------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    hdr = [
        "# n11 central-reply closure batch-31 (class 5804) 51-LOSS",
        "#   canonical-adoption increment (Part DL, 2026-11-24)",
        "# published batch-31 kit (Part CY scaffold + takeover drives) +",
        "#   published Part DI reprobe kit: ALL 55 of 55 keys carry honest",
        "#   probe labels.  51 keys resolved LOSS at budget 15M and ARE",
        "#   this increment; their two-pass fresh-cold raws come from the",
        "#   cumulative batch-31 kit (Part CY drive-1 + drive-2 takeover +",
        "#   Part DI reprobe).  3 keys (ad024/ad028/ad055) are probe-level",
        "#   WINs at budget 15M and 1 key (ad043) is a probe-level WIN at",
        "#   the Part DI 30M budget (its published 15M exhaustion is",
        "#   superseded); all four stay UNCONSUMED: not adopted, not",
        "#   emitted, not in any canonical cache (WIN-row scrutiny is the",
        "#   separate C++ owner lane, pin 9193f5b6...; no completeness",
        "#   claim is made beyond the labels).",
        "# 2-pass node-exact exact-S5 verdicts at budget 15M, fresh cold,",
        "#   pinned jsreplay.js sha256",
        "#   845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# gates: batch-31 kit MANIFEST sha-verified file-by-file (194 files)",
        "#   + Part DI kit MANIFEST sha-verified file-by-file (40 files);",
        "#   20 val-gate host files pinned and node-exact on five hosts",
        "#   (published-baseline/b31-host/d2-host/tk-host/di-host); all 55",
        "#   probed keys two-pass node-exact with '# replay_done' on both",
        "#   passes; status.log (59 lines, sha-pinned, 55 PASS rows + three",
        "#   pinned WIN-HALT rows + the one pinned superseded 15M ad043",
        "#   EXHAUSTED row) each-once agreement on (b,r,n); raw inventory",
        "#   exactly ad001..ad055 x {p1,p2} (110 files; no sidecars);",
        "#   batch-keys legal/(lo,hi)/s5/membership agreement; adopted-row",
        "#   per-pass node total 237,596,711; adopted keys distinct and",
        "#   absent from BASE 04b0a239... (6,354 rows) while all four WIN",
        "#   keys are also absent (consumed nowhere); DI kit byte-clones",
        "#   reproduce the batch-31 status.log and the BASE cache; adopted",
        "#   keys absent from the quarantine registry.",
        "# ADOPTED set = ad001..ad054 except {ad024, ad028, ad043, ad055}",
        "#   (51 keys; 51 of them result 2 at budget 15M).  The batch is",
        "#   probe-complete; full != loss because four WIN rows exist at",
        "#   probe level and stay unconsumed.",
        "# The 51 LOSS rows ARE consumed into the canonical cache by the",
        "#   fail-closed union merger; 11x11 stays UNKNOWN; nodes are",
        "#   bookkeeping, never verdicts; class 5804 is NOT freed (its",
        "#   remaining unknown children are the four unconsumed WINs).",
    ]
    rows_for_sort = [(ADOPTED_KEYS[k][0], ADOPTED_KEYS[k][1], ADOPTED_NODES[k])
                     for k in ADOPTED_LOSS_IDS]
    rowlines = [f"s5verdict,{lo},{hi},5,2,{nodes}" for lo, hi, nodes in sorted(rows_for_sort)]
    blob = ("\n".join(hdr + rowlines) + "\n").encode("utf-8")
    incr_path = OUT / "increment-b31loss51-20261124.cache"
    incr_path.write_bytes(blob)
    incr_sha = hashlib.sha256(blob).hexdigest()

    manifest = {
        "schema": "b31loss51-increments-manifest-v1",
        "batches": [{
            "batch": 31,
            "class_index": 5804,
            "keys_total": 55,
            "adopted_loss_ids": list(ADOPTED_LOSS_IDS),
            "already_adopted_ids": [],
            "unadopted_win_ids": list(WIN_UNCONSUMED_IDS),
            "exhausted_excluded_ids": [],
            "probed_ids": list(PROBED_IDS),
            "fragment_ids": [],
            "fileless_unprobed_count": 0,
            "fileless_unprobed_ids": [],
            "input_sha256": B31_KEYS_SHA_EXPECTED,
            "status_log_sha256": B31_STATUS_SHA_EXPECTED,
            "status_log_lines": STATUS_LINES_EXPECTED,
            "status_log_final_line": STATUS_FINAL_LINE,
            "status_log_win_halt_lines": list(WIN_HALT_LINES),
            "status_log_exhausted_lines": list(EXHAUSTED_LINES),
            "ad043_supersede": {
                "superseded_15m_label": "EXHAUSTED (result 0, nodes 15,000,000)",
                "resolution": "Part DI 30M two-pass fresh-cold WIN "
                              "(result 1, nodes 18,247,029, p1==p2 node-exact)",
                "di_kit_manifest_sha256": DI_MANIFEST_SHA_EXPECTED,
                "di_kit_files_verified": di_verified,
                "di_status_sha256": DI_STATUS_SHA_EXPECTED,
                "di_ad043_p1_sha256": DI_AD043_P1_SHA,
                "di_ad043_p2_sha256": DI_AD043_P2_SHA,
                "di_b31_status_clone_sha256": DI_B31STATUS_CLONE_SHA,
                "di_base_cache_clone_sha256": DB_MERGED_CACHE_CLONE_SHA_EXPECTED,
            },
            "kit_integrity": {
                "manifest_sha256": B31_MANIFEST_SHA_EXPECTED,
                "files_verified": kit_verified,
            },
            "val_gate_multi_host_node_exact": True,
            "total_nodes_pass_one": nodes_p1_total,
            "total_nodes_pass_two": nodes_p2_total,
            "stop_rule": "batch-31 probe-complete (55/55 keys carry honest labels: "
                         "51 LOSS 2-pass fresh-cold budget 15M across Part CY drive-1 "
                         "+ drive-2 takeover + Part DI reprobe; loss-only adoption of "
                         "the 51 fresh rows; the four probe-level WINs ad024/ad028/"
                         "ad043/ad055 stay unconsumed pending the scrutiny-owner C++ "
                         "gate; verdict not consumed)",
            "fragment_state": {},
        }],
        "resolved_ids": list(ADOPTED_LOSS_IDS),
        "loss_ids": list(ADOPTED_LOSS_IDS),
        "win_ids": list(WIN_UNCONSUMED_IDS),
        "unadopted_win_ids": list(WIN_UNCONSUMED_IDS),
        "exhausted_excluded_ids": [],
        "row_counts": {
            "probed_rows": 55, "adopted_loss_rows": 51, "prior_adopted_loss_rows": 0,
            "wins": 4, "exhausted_excluded": 0, "fragments_unprobed": 0,
            "fileless_unprobed": 0,
        },
        "sha256": {"loss": incr_sha},
        "full_packet_eq_loss_only": False,
        "full_packet_eq_loss_only_rationale":
            "the batch is probe-complete (55/55 honest labels) but the packet is "
            "NOT loss-only: four probe-level WIN rows (ad024 4,360,661 and ad028 "
            "12,803,283 at 15M, ad043 18,247,029 at the Part DI 30M reprobe, ad055 "
            "3,364,655 at 15M) stay UNCONSUMED and are NOT adopted; the adopted "
            "packet is the 51 fresh LOSS rows plus nothing else; no batch-31 row was "
            "adopted before; class 5804 is NOT freed (four unconsumed WIN children "
            "remain and no LOSS-only adoption can consume them)",
        "win_scenario_exists": True,
        "win_scenario_note":
            "exactly four WIN rows (ad024/ad028 at 15M, ad043 at the Part DI 30M "
            "reprobe superseding its pinned 15M exhaustion, ad055 at 15M) exist and "
            "each stays unconsumed by this adoption (scrutiny owner C++ "
            "second-implementation gate pin 9193f5b6...); loss-only adoption NEVER "
            "frees class 5804 while any of the four WIN children remain "
            "verdict-unconsumed",
        "unadopted_win_rows": [
            {"key_id": kid, "result": WIN_UNCONSUMED[kid]["result"],
             "nodes": WIN_UNCONSUMED[kid]["nodes"], "legal": WIN_UNCONSUMED[kid]["legal"],
             "lo": WIN_UNCONSUMED[kid]["lo"], "hi": WIN_UNCONSUMED[kid]["hi"],
             "s5_index": WIN_UNCONSUMED[kid]["s5_index"],
             "decisive_budget": WIN_UNCONSUMED[kid]["decisive_budget"]}
            for kid in WIN_UNCONSUMED_IDS],
        "exhausted_rows": [],
        "fragment_rows_note":
            "batch-31 is probe-complete with NO fragment keys and NO truncated sidecars: "
            "the raw inventory is exactly ad001..ad055 x {p1,p2} (110 files)",
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_sha256": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "base_cache_absent_hits_for_emitted": 0,
        "base_cache_prior_adoption_confirmed": 0,
        "quarantine_hits": 0,
        "interpretation_guard":
            "canonical 51-LOSS adoption increment: only the 51 fresh LOSS rows "
            "(ad001..ad054 except {ad024, ad028, ad043, ad055}) are consumed into "
            "the canonical cache via the fail-closed union merger; the four "
            "probe-level WINs are consumed NOWHERE (no verdict claim, no "
            "exclusion claim); all 55 batch-31 keys stay UNKNOWN as verdicts; "
            "adopting 51 LOSS rows does NOT free class 5804 (four unconsumed WIN "
            "children remain); 11x11 stays UNKNOWN; nodes are bookkeeping, never "
            "verdicts",
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"INCREMENT rows=51 loss_nodes={ADOPTED_TOTAL_NODES} -> {incr_path}")


if __name__ == "__main__":
    main()