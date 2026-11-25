#!/usr/bin/env python3
"""Build the Part DZ canonical-adoption increments (fail-closed).

Part DZ (declared 2026-11-25, publish-then-execute) adopts ONLY the fresh
exact-LOSS rows carried by three published probe-kit drives into the
canonical exact-S5 verdict chain:

* increment-b4loss1-20261125.cache  : 1 row  (batch-4  e001, class 16371,
  2026-11-22 kit, nodes 882,800 @ budget 15M, two-pass fresh-cold),
* increment-b36loss40-20261125.cache: 40 rows (batch-36 d005..d049 minus the
  5 probe-level WIN rows {d008,d009,d021,d026,d029}, class 20421),
* increment-b37loss46-20261125.cache: 46 rows (batch-37 e003..e050 minus
  e022 (already canonical, batch-14 q007 dual-class) and the probe-level WIN
  e042, class 16371).

87 rows total.  NOTHING ELSE is consumed by this Part:

* the probe-level WIN rows (batch-36 d008/d009/d021/d026/d029, batch-37
  e042, batch-4 e002) are consumed NOWHERE (scrutiny-owner C++ second
  implementation gate pin 9193f5b6...),
* batch-3 (2026-11-22) honest-labeled unconsumed rows d001/d003 (LOSS) and
  d002 (WIN) of class 20421 are NOT adopted here: the 2026-11-22 batch-3
  declaration-only kit publishes NO two-pass raws, so their adoption needs
  its own raw publication first (recorded as the next candidate),
* e022 (s5 546606) is already canonical (BASE row
  s5verdict,1153202979868770304,16,5,2,1494975, adopted earlier as the
  batch-14 q007 dual-class packet row) and is excluded from the batch-37
  target set.

The adoption base is the canonical chain head = the Part DW merged
6,573-row cache sha256
23d40e36ed1730ace4986461995dfc0ee606a380da9b156cdddaf09ef8a29822
(WIN 158 / LOSS 6,415), byte-pinned here; this maker ABORTS against
anything else.  Every adopted key is asserted fresh (absent from the
BASE) and absent from the quarantine registry (81d23160...).

Fail-closed gates: batch-36 and batch-37 kit MANIFEST files sha-verified
file-by-file (160 / 166 entries, the 4-column sha256+git-blob+size form
accepted for batch-36); the batch-4 kit (declaration-only, 2026-11-22)
pinned file-by-file (status.log 63c2d969..., batch-keys 70b8a4c8..., the
four val-gate host outputs, both e001 passes 84a3c287... byte-identical,
e002 passes field-equal 8108953x/1914d048) AND cross-verified byte-equal
against the batch-37 kit's published batch4-packet source clones; 92
two-pass fresh-cold raw re-verification ('# replay_done' on both passes,
(budget,result,nodes) agreement with the pinned honest-history status
rows row-by-row); raw/batch-keys agreement on (legal, lo, hi) and pins on
(s5_index, membership_class_count); raw inventories exactly
45x{p1,p2} / 47x{p1,p2} / {e001,e002}x{p1,p2} and nothing else;
val-gate node-exact across every host output per molecule (published
baselines + dx-host / dy-host / batch-4 this-host); the 87 adopted keys
distinct, absent from the BASE (6,573 rows) and from the quarantine
registry; adopted per-pass node totals pinned per batch (159,499,387 /
96,295,019 / 882,800; all-probed totals 183,921,575 / 99,204,059 /
14,995,432).  Verdicts are byte-taken from the raws.

Loss-only adoption asserts NO root verdict; class 16371 / class 20421
scheduling effects are derived only later by the reaudit refresh +
fail-closed delta extractor.  11x11 stays UNKNOWN; nodes are bookkeeping,
never verdicts.
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
KIT_B36 = ROOT / "research/experiments/n11-centralreply-closure-class20421-batch36-20261124"
KIT_B37 = ROOT / "research/experiments/n11-centralreply-closure-class16371-batch37-20261125"
KIT_B4 = ROOT / "research/experiments/n11-centralreply-closure-class16371-batch4-20261122"
B36_RAW = KIT_B36 / "output/raw"
B37_RAW = KIT_B37 / "output/raw"
B4_RAW = KIT_B4 / "output/raw"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class16757-b35loss26-adoption-reaudit-20261124/output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-plus-b35loss26-20261124.cache"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
MERGER = EXP / "scripts/s5_union_merge.py"

MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA_EXPECTED = "23d40e36ed1730ace4986461995dfc0ee606a380da9b156cdddaf09ef8a29822"
BASE_CACHE_ROWS_EXPECTED = 6573
BASE_CACHE_WIN_EXPECTED = 158
BASE_CACHE_LOSS_EXPECTED = 6415
JSREPLAY_SHA_EXPECTED = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
QUARANTINE_SHA_EXPECTED = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

# --- published kit pins ------------------------------------------------------
KIT_B36_MANIFEST_SHA = "f4a6d53f65694b1393767d562a14266d8bc91b3f255ba23c5d828414adcd0826"
KIT_B36_FILES = 160
KIT_B36_KEYS_SHA = "d59182030ce1ade5ad02c8db3836291e2feadfa84325fd4729001e80bfc0c815"
KIT_B36_STATUS_SHA = "dd8c180b9ad19937634d6ad7d0b0964a08f637d9d3d24dbbeabf198e6f6d74fb"
KIT_B37_MANIFEST_SHA = "e4a9d32691bc045e296f6a64f7d277086ce02b1c5bb02f4e71badb9fa6c0a455"
KIT_B37_FILES = 166
KIT_B37_KEYS_SHA = "25b9388e9f855f30bf334bc825f483dbe66becc5c49b918bd1aaa74d3f3765a8"
KIT_B37_STATUS_SHA = "8ce0b9fb646fc811d55ce2b7b1a874c048efe56fdad09b78a97bbae2a24132e1"
KIT_B4_STATUS_SHA = "63c2d9693a374453bea604b85e1b69ac41c06a214675ea63100a675b1f064ac0"
KIT_B4_KEYS_SHA = "70b8a4c89f7cea454bfd2b52f720245b6d9c5d7311878bf8aac637940825ecdf"
KIT_B4_E001_P1_SHA = "84a3c2877fe928dc013eebe70706927178be30085b6a02e489574691c88228a4"
KIT_B4_E001_P2_SHA = "84a3c2877fe928dc013eebe70706927178be30085b6a02e489574691c88228a4"
KIT_B4_E002_P1_SHA = "8108953223410bcb73e1c66fad48f52af8437ad03a164688fea0d97db93eb5e7"
KIT_B4_E002_P2_SHA = "1914d0485d66327e28bd938d25d812bea8de28d4986d3324067dcd5d10d5aaa2"
KIT_B4_RUNBATCH_SHA = "4e47fd12234e9d9cc4f94bbd3e80d8c06805836a6f0ac4285d16e1f0d966b05f"

# --- status.log honest-history pins ------------------------------------------
B36_STATUS_LINES = 50
B36_STATUS_FIRST = "2026-11-24T23:40:23Z d005 PASS 15000000,2,2497042"
B36_STATUS_FINAL = "2026-11-25T00:13:41Z d049 PASS 15000000,2,4633293"
B36_WIN_HALT_LINES = [
    "2026-11-24T23:42:13Z d008 WIN-HALT",
    "2026-11-24T23:43:06Z d009 WIN-HALT",
    "2026-11-24T23:53:24Z d021 WIN-HALT",
    "2026-11-24T23:57:59Z d026 WIN-HALT",
    "2026-11-24T23:59:30Z d029 WIN-HALT",
]
B37_STATUS_LINES = 48
B37_STATUS_FIRST = "2026-11-25T00:06:08Z e003 PASS 15000000,2,872116"
B37_STATUS_FINAL = "2026-11-25T00:24:44Z e042 WIN-HALT"
B37_WIN_HALT_LINES = [
    "2026-11-25T00:24:44Z e042 WIN-HALT",
]
B4_STATUS_LINES = 3
B4_STATUS_FIRST = "2026-11-22T03:23:43Z e001 PASS 15000000,2,882800"
B4_STATUS_FINAL = "2026-11-22T03:26:03Z e002 WIN-HALT"
B4_WIN_HALT_LINES = [
    "2026-11-22T03:26:03Z e002 WIN-HALT",
]
EXHAUSTED_LINES = []
RETRY_LINES = []
TRUNCATED_SIDECARS = []
BUDGET = 15000000

# --- adopted packets ---------------------------------------------------------
B36_PROBED_IDS = [f"d{i:03d}" for i in range(5, 50)]
B36_WIN_IDS = ["d008", "d009", "d021", "d026", "d029"]
B36_WIN_PINS = {
    "d008": {"key": (1155454779397246976, 131072), "s5": 528689, "nodes": 5273778},
    "d009": {"key": (1156299204327378944, 131072), "s5": 543795, "nodes": 4997146},
    "d021": {"key": (1155173441859489792, 131072), "s5": 605961, "nodes": 5266012},
    "d026": {"key": (1153062242096250880, 540672), "s5": 620742, "nodes": 6877739},
    "d029": {"key": (1152921642046849024, 68719477248), "s5": 625899, "nodes": 2007513},
}
B37_PROBED_IDS = [f"e{i:03d}" for i in range(3, 51) if i != 22]
B37_WIN_IDS = ["e042"]
B37_WIN_PINS = {
    "e042": {"key": (1153202979851993088, 272), "s5": 550879, "nodes": 2909040},
}
B4_PROBED_IDS = ["e001", "e002"]
B4_WIN_IDS = ["e002"]
B4_WIN_PINS = {
    "e002": {"key": (1153765929805414400, 16), "s5": 183566, "nodes": 14112632},
}
B37_EXCLUDED_CANONICAL_IDS = ["e022"]
B37_E022_CACHE_ROW = "s5verdict,1153202979868770304,16,5,2,1494975"
B37_E022_S5 = 546606

B36_ADOPTED_NODES = 159499387
B36_ALL45_NODES = 183921575
B37_ADOPTED_NODES = 96295019
B37_ALL47_NODES = 99204059
B4_ADOPTED_NODES = 882800
B4_ALL2_NODES = 14995432

# --- val-gate pins ------------------------------------------------------------
VAL_GATES = {
    "at2m-s5-1152921504606851072-536870946": (2000000, 0, 2000000),
    "at2m-s5-1188950301626860544-536870912": (2000000, 0, 2000000),
    "first-15m-s5-1152921504606851072-536870946": (15000000, 2, 3651923),
    "second-15m-s5-1188950301626860544-536870912": (15000000, 2, 5040200),
}
VAL_HOSTS_B36 = ["published-baseline", "dx-host"]
VAL_HOSTS_B37 = ["published-baseline", "dy-host"]
VAL_HOSTS_B4 = {  # batch-4 kit val-gate molecule -> filename
    "at2m-s5-1152921504606851072-536870946": "at2m-1.this-host.out",
    "at2m-s5-1188950301626860544-536870912": "at2m-2.this-host.out",
    "first-15m-s5-1152921504606851072-536870946": "15m-1.this-host.out",
    "second-15m-s5-1188950301626860544-536870912": "15m-2.this-host.out",
}

B36_ADOPTED_KEYS = {
    'd005': {'key': (1155173304420601856, 131072), 'legal': 87, 'nodes': 2497042, 's5': 356378, 'mcc': 4, 'decisive_budget': 15000000},
    'd006': {'key': (1155173304420536320, 131073), 'legal': 85, 'nodes': 2448235, 's5': 393798, 'mcc': 4, 'decisive_budget': 15000000},
    'd007': {'key': (1155173304420536352, 131072), 'legal': 82, 'nodes': 2835651, 's5': 441775, 'mcc': 4, 'decisive_budget': 15000000},
    'd010': {'key': (1155173304420537344, 131072), 'legal': 86, 'nodes': 4464813, 's5': 565995, 'mcc': 4, 'decisive_budget': 15000000},
    'd011': {'key': (1155173304422633472, 131072), 'legal': 79, 'nodes': 9671556, 's5': 570139, 'mcc': 4, 'decisive_budget': 15000000},
    'd012': {'key': (1155173308715503616, 131072), 'legal': 91, 'nodes': 3794414, 's5': 574236, 'mcc': 4, 'decisive_budget': 15000000},
    'd013': {'key': (1155182100513558528, 131072), 'legal': 89, 'nodes': 5818726, 's5': 578232, 'mcc': 4, 'decisive_budget': 15000000},
    'd014': {'key': (1173187702930018304, 131072), 'legal': 83, 'nodes': 3545649, 's5': 582153, 'mcc': 4, 'decisive_budget': 15000000},
    'd015': {'key': (1155173304420536320, 135168), 'legal': 91, 'nodes': 4654637, 's5': 585861, 'mcc': 4, 'decisive_budget': 15000000},
    'd016': {'key': (1153062242096250880, 532480), 'legal': 89, 'nodes': 3825579, 's5': 589727, 'mcc': 4, 'decisive_budget': 15000000},
    'd017': {'key': (1153062242096250880, 17301504), 'legal': 89, 'nodes': 1966996, 's5': 593275, 'mcc': 4, 'decisive_budget': 15000000},
    'd018': {'key': (1153062242096250880, 34360262656), 'legal': 88, 'nodes': 4747380, 's5': 596738, 'mcc': 4, 'decisive_budget': 15000000},
    'd019': {'key': (1155173304420536832, 131072), 'legal': 88, 'nodes': 5262509, 's5': 602640, 'mcc': 4, 'decisive_budget': 15000000},
    'd020': {'key': (1155173304421584896, 131072), 'legal': 85, 'nodes': 2907985, 's5': 605690, 'mcc': 4, 'decisive_budget': 15000000},
    'd022': {'key': (1155173306568019968, 131072), 'legal': 80, 'nodes': 6359951, 's5': 608779, 'mcc': 4, 'decisive_budget': 15000000},
    'd023': {'key': (1155177702467047424, 131072), 'legal': 89, 'nodes': 3080674, 's5': 611801, 'mcc': 4, 'decisive_budget': 15000000},
    'd024': {'key': (1164180503675277312, 131072), 'legal': 91, 'nodes': 5763753, 's5': 614833, 'mcc': 4, 'decisive_budget': 15000000},
    'd025': {'key': (1155173304420536320, 133120), 'legal': 86, 'nodes': 3676924, 's5': 617672, 'mcc': 4, 'decisive_budget': 15000000},
    'd027': {'key': (1153062242096250880, 34078720), 'legal': 88, 'nodes': 3664311, 's5': 623364, 'mcc': 4, 'decisive_budget': 15000000},
    'd028': {'key': (1155173854176350208, 131072), 'legal': 82, 'nodes': 1533976, 's5': 625189, 'mcc': 4, 'decisive_budget': 15000000},
    'd030': {'key': (1155173304420536576, 131072), 'legal': 89, 'nodes': 4904993, 's5': 630432, 'mcc': 4, 'decisive_budget': 15000000},
    'd031': {'key': (1155175503443791872, 131072), 'legal': 80, 'nodes': 4682372, 's5': 636913, 'mcc': 4, 'decisive_budget': 15000000},
    'd032': {'key': (1155173304420536320, 132096), 'legal': 86, 'nodes': 3604850, 's5': 641189, 'mcc': 4, 'decisive_budget': 15000000},
    'd033': {'key': (1153062242096250880, 557056), 'legal': 85, 'nodes': 2780990, 's5': 643424, 'mcc': 4, 'decisive_budget': 15000000},
    'd034': {'key': (1153062242096250880, 67633152), 'legal': 80, 'nodes': 2430527, 's5': 645317, 'mcc': 3, 'decisive_budget': 15000000},
    'd035': {'key': (1155173304420536448, 131072), 'legal': 90, 'nodes': 6414338, 's5': 650304, 'mcc': 4, 'decisive_budget': 15000000},
    'd036': {'key': (1155173304420798464, 131072), 'legal': 83, 'nodes': 6935869, 's5': 651925, 'mcc': 4, 'decisive_budget': 15000000},
    'd037': {'key': (1155173304957407232, 131072), 'legal': 89, 'nodes': 4395429, 's5': 653505, 'mcc': 4, 'decisive_budget': 15000000},
    'd038': {'key': (1155173304420536320, 131584), 'legal': 81, 'nodes': 2879174, 's5': 655969, 'mcc': 4, 'decisive_budget': 15000000},
    'd039': {'key': (1153062242096250880, 589824), 'legal': 70, 'nodes': 968369, 's5': 657407, 'mcc': 3, 'decisive_budget': 15000000},
    'd040': {'key': (1155173304420536384, 131072), 'legal': 90, 'nodes': 3483061, 's5': 662182, 'mcc': 4, 'decisive_budget': 15000000},
    'd041': {'key': (1155173304688971776, 131072), 'legal': 85, 'nodes': 4830084, 's5': 664455, 'mcc': 4, 'decisive_budget': 15000000},
    'd042': {'key': (1155173304420569088, 131072), 'legal': 81, 'nodes': 5099461, 's5': 669726, 'mcc': 4, 'decisive_budget': 15000000},
    'd043': {'key': (1155173304420552704, 131072), 'legal': 84, 'nodes': 1536412, 's5': 671112, 'mcc': 4, 'decisive_budget': 15000000},
    'd044': {'key': (1155173304454090752, 131072), 'legal': 85, 'nodes': 2213835, 's5': 671120, 'mcc': 4, 'decisive_budget': 15000000},
    'd045': {'key': (1155173373140013056, 131072), 'legal': 80, 'nodes': 2928981, 's5': 671129, 'mcc': 3, 'decisive_budget': 15000000},
    'd046': {'key': (1155173304420536321, 131072), 'legal': 84, 'nodes': 2953291, 's5': 671133, 'mcc': 3, 'decisive_budget': 15000000},
    'd047': {'key': (1155173304420536322, 131072), 'legal': 82, 'nodes': 2289816, 's5': 671137, 'mcc': 4, 'decisive_budget': 15000000},
    'd048': {'key': (1155173304420536324, 131072), 'legal': 85, 'nodes': 7013481, 's5': 671143, 'mcc': 4, 'decisive_budget': 15000000},
    'd049': {'key': (1155173304437313536, 131072), 'legal': 86, 'nodes': 4633293, 's5': 671146, 'mcc': 3, 'decisive_budget': 15000000},
}
B37_ADOPTED_KEYS = {
    'e003': {'key': (5764888998279380992, 16), 'legal': 88, 'nodes': 872116, 's5': 306951, 'mcc': 4, 'decisive_budget': 15000000},
    'e004': {'key': (1153202979851993088, 17), 'legal': 75, 'nodes': 2444351, 's5': 399422, 'mcc': 4, 'decisive_budget': 15000000},
    'e005': {'key': (1153202979851993088, 18), 'legal': 92, 'nodes': 1436764, 's5': 480806, 'mcc': 4, 'decisive_budget': 15000000},
    'e006': {'key': (1153202979851993090, 16), 'legal': 93, 'nodes': 2044730, 's5': 498207, 'mcc': 4, 'decisive_budget': 15000000},
    'e007': {'key': (1153202979851993092, 16), 'legal': 86, 'nodes': 1274455, 's5': 502385, 'mcc': 4, 'decisive_budget': 15000000},
    'e008': {'key': (1153202979851993096, 16), 'legal': 92, 'nodes': 2246752, 's5': 505442, 'mcc': 4, 'decisive_budget': 15000000},
    'e009': {'key': (1153202979851993104, 16), 'legal': 85, 'nodes': 2701133, 's5': 509234, 'mcc': 4, 'decisive_budget': 15000000},
    'e010': {'key': (1153202979851993152, 16), 'legal': 90, 'nodes': 1323011, 's5': 512923, 'mcc': 4, 'decisive_budget': 15000000},
    'e011': {'key': (1153202979851993216, 16), 'legal': 93, 'nodes': 1926841, 's5': 516385, 'mcc': 4, 'decisive_budget': 15000000},
    'e012': {'key': (1153202979851993600, 16), 'legal': 93, 'nodes': 1755039, 's5': 522643, 'mcc': 4, 'decisive_budget': 15000000},
    'e013': {'key': (1153202979851994112, 16), 'legal': 87, 'nodes': 1292880, 's5': 525693, 'mcc': 4, 'decisive_budget': 15000000},
    'e014': {'key': (1153202979851997184, 16), 'legal': 82, 'nodes': 2504820, 's5': 528188, 'mcc': 3, 'decisive_budget': 15000000},
    'e015': {'key': (1153202979852001280, 16), 'legal': 88, 'nodes': 3397717, 's5': 530117, 'mcc': 4, 'decisive_budget': 15000000},
    'e016': {'key': (1153202979852009472, 16), 'legal': 89, 'nodes': 1681334, 's5': 532225, 'mcc': 4, 'decisive_budget': 15000000},
    'e017': {'key': (1153202979852025856, 16), 'legal': 87, 'nodes': 1254583, 's5': 534675, 'mcc': 4, 'decisive_budget': 15000000},
    'e018': {'key': (1153202979852124160, 16), 'legal': 91, 'nodes': 2163651, 's5': 537035, 'mcc': 4, 'decisive_budget': 15000000},
    'e019': {'key': (1153202979852517376, 16), 'legal': 89, 'nodes': 5473304, 's5': 541141, 'mcc': 4, 'decisive_budget': 15000000},
    'e020': {'key': (1153202979853041664, 16), 'legal': 84, 'nodes': 3070360, 's5': 543110, 'mcc': 4, 'decisive_budget': 15000000},
    'e021': {'key': (1153202979854090240, 16), 'legal': 92, 'nodes': 2032926, 's5': 544907, 'mcc': 4, 'decisive_budget': 15000000},
    'e023': {'key': (1153202979885547520, 16), 'legal': 86, 'nodes': 1261430, 's5': 547319, 'mcc': 4, 'decisive_budget': 15000000},
    'e024': {'key': (1153202979919101952, 16), 'legal': 80, 'nodes': 2080409, 's5': 548819, 'mcc': 4, 'decisive_budget': 15000000},
    'e025': {'key': (1154328879758835712, 16), 'legal': 80, 'nodes': 2180425, 's5': 549855, 'mcc': 4, 'decisive_budget': 15000000},
    'e026': {'key': (1153202980388864000, 16), 'legal': 87, 'nodes': 1270547, 's5': 550280, 'mcc': 4, 'decisive_budget': 15000000},
    'e027': {'key': (1153202980925734912, 16), 'legal': 79, 'nodes': 2851789, 's5': 550330, 'mcc': 4, 'decisive_budget': 15000000},
    'e028': {'key': (1153202981999476736, 16), 'legal': 89, 'nodes': 1392689, 's5': 550357, 'mcc': 4, 'decisive_budget': 15000000},
    'e029': {'key': (1153202984146960384, 16), 'legal': 91, 'nodes': 2604085, 's5': 550403, 'mcc': 4, 'decisive_budget': 15000000},
    'e030': {'key': (1153203048571469824, 16), 'legal': 74, 'nodes': 1651408, 's5': 550446, 'mcc': 3, 'decisive_budget': 15000000},
    'e031': {'key': (1153205178875248640, 16), 'legal': 84, 'nodes': 2186798, 's5': 550549, 'mcc': 4, 'decisive_budget': 15000000},
    'e032': {'key': (1153207377898504192, 16), 'legal': 88, 'nodes': 1591928, 's5': 550593, 'mcc': 4, 'decisive_budget': 15000000},
    'e033': {'key': (1153211775945015296, 16), 'legal': 93, 'nodes': 1887012, 's5': 550622, 'mcc': 4, 'decisive_budget': 15000000},
    'e034': {'key': (1171217378361475072, 16), 'legal': 86, 'nodes': 1896242, 's5': 550719, 'mcc': 4, 'decisive_budget': 15000000},
    'e035': {'key': (1162210179106734080, 16), 'legal': 86, 'nodes': 4309181, 's5': 550757, 'mcc': 4, 'decisive_budget': 15000000},
    'e036': {'key': (1157706579479363584, 16), 'legal': 83, 'nodes': 2017628, 's5': 550795, 'mcc': 4, 'decisive_budget': 15000000},
    'e037': {'key': (1154047404580798464, 1028), 'legal': 82, 'nodes': 2061203, 's5': 550839, 'mcc': 4, 'decisive_budget': 15000000},
    'e038': {'key': (1154047404580798464, 1032), 'legal': 84, 'nodes': 4704883, 's5': 550868, 'mcc': 4, 'decisive_budget': 15000000},
    'e039': {'key': (1153202979851993088, 528), 'legal': 80, 'nodes': 1990057, 's5': 550876, 'mcc': 4, 'decisive_budget': 15000000},
    'e040': {'key': (1153202979851993088, 1040), 'legal': 77, 'nodes': 2079262, 's5': 550877, 'mcc': 4, 'decisive_budget': 15000000},
    'e041': {'key': (1157425104234221568, 268435712), 'legal': 84, 'nodes': 3166673, 's5': 550878, 'mcc': 3, 'decisive_budget': 15000000},
    'e043': {'key': (1157425104234217473, 268435712), 'legal': 76, 'nodes': 1348152, 's5': 550880, 'mcc': 3, 'decisive_budget': 15000000},
    'e044': {'key': (1154047404580798464, 33555456), 'legal': 87, 'nodes': 1391767, 's5': 550882, 'mcc': 4, 'decisive_budget': 15000000},
    'e045': {'key': (1154047404580798464, 16778240), 'legal': 94, 'nodes': 1792096, 's5': 550883, 'mcc': 4, 'decisive_budget': 15000000},
    'e046': {'key': (1154047404580798464, 17408), 'legal': 90, 'nodes': 1777014, 's5': 550884, 'mcc': 4, 'decisive_budget': 15000000},
    'e047': {'key': (1157425104234217474, 268435712), 'legal': 94, 'nodes': 1693883, 's5': 550885, 'mcc': 4, 'decisive_budget': 15000000},
    'e048': {'key': (1154047404580798464, 9216), 'legal': 92, 'nodes': 1657429, 's5': 550886, 'mcc': 4, 'decisive_budget': 15000000},
    'e049': {'key': (1154047404580798464, 33792), 'legal': 91, 'nodes': 1143085, 's5': 550887, 'mcc': 4, 'decisive_budget': 15000000},
    'e050': {'key': (1154047404580798464, 66560), 'legal': 76, 'nodes': 1411177, 's5': 550888, 'mcc': 3, 'decisive_budget': 15000000},
}
B4_ADOPTED_KEYS = {
    'e001': {'key': (10376575016706768896, 16), 'legal': 88, 'nodes': 882800, 's5': 93170, 'mcc': 4, 'decisive_budget': 15000000},
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
    cands = []
    cands.append(kit_dir / rel)
    cands.append(ROOT / rel)
    stripped = rel.split("research/experiments/", 1)[-1]
    stripped = stripped[stripped.index("/") + 1:] if stripped.startswith("n11") else stripped
    cands.append(kit_dir / stripped)
    cands.append(kit_dir / "output" / stripped)
    return cands


def verify_kit(dirp: Path, manifest_sha: str, kit_files: int):
    """MANIFEST sha-verify file-by-file; accepts both the 2-column
    'sha256 path' form (batch-37) and the 4-column
    'sha256 git-blob-sha1 size path' form (batch-36); paths repo-relative
    or kit-relative."""
    if not dirp.is_dir():
        sys_exit(f"kit dir missing {dirp}")
    manifest = dirp / "MANIFEST-sha256.txt"
    if sha(manifest) != manifest_sha:
        sys_exit(f"kit {dirp.name} MANIFEST sha drift")
    verified = 0
    for line in manifest.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split()
        want, rel = parts[0], parts[-1]
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


def parse_status(path: Path, n_lines: int, first: str, final: str,
                 win_halt_lines: list, idpat: str):
    lines = path.read_text().splitlines()
    if len(lines) != n_lines:
        sys_exit(f"status lines {len(lines)} != {n_lines}")
    if lines[0] != first or lines[-1] != final:
        sys_exit("status first/final line drift")
    got_pass = {}
    win_halt, exh, retry = [], [], []
    mismatch = []
    for line in lines:
        m = re.match(rf"^(\S+) ({idpat}) PASS (\d+),(\d+),(\d+)$", line)
        if m:
            kid = m.group(2)
            if kid in got_pass:
                sys_exit(f"status duplicate verdict row for {kid}")
            got_pass[kid] = (int(m.group(3)), int(m.group(4)), int(m.group(5)))
            continue
        m = re.match(rf"^(\S+) ({idpat}) WIN-HALT$", line)
        if m:
            win_halt.append(line)
            continue
        m = re.match(rf"^(\S+) ({idpat}) EXHAUSTED (\d+),(\d+),(\d+)$", line)
        if m:
            exh.append(line)
            continue
        m = re.match(rf"^(\S+) ({idpat}) P2-TRUNCATED-RETRY$", line)
        if m:
            retry.append(line)
            continue
        mismatch.append(line)
    if mismatch:
        sys_exit(f"status has unmatched/MISMATCH rows: {mismatch[:3]}")
    if win_halt != win_halt_lines:
        sys_exit("status WIN-HALT lines != the pinned pre-registered halt history")
    if exh != EXHAUSTED_LINES:
        sys_exit("status EXHAUSTED lines != the pinned empty history")
    if retry != RETRY_LINES:
        sys_exit("status TRUNCATED-RETRY lines != the pinned empty history")
    return got_pass


def batch_keys_gates(kit_dir: Path, keys_sha: str, schema: str, batch_name: str,
                     keys_filename: str, target_key_count: int, serving_class: int):
    keys_path = kit_dir / "input" / keys_filename
    if sha(keys_path) != keys_sha:
        sys_exit(f"batch-keys sha drift in kit {batch_name}")
    bk = json.loads(keys_path.read_text())
    if bk["schema"] != schema:
        sys_exit(f"batch-keys schema drift ({batch_name})")
    if bk["batch"] != batch_name:
        sys_exit(f"batch-keys batch label drift ({batch_name})")
    if int(bk["target_key_count"]) != target_key_count or len(bk["keys"]) != target_key_count:
        sys_exit(f"batch-keys target count drift ({batch_name})")
    if int(bk["canonical_cache_s5verdict_rows"]) != BASE_CACHE_ROWS_EXPECTED:
        sys_exit(f"batch-keys canonical cache rows drift ({batch_name})")
    if bk["consumed_into_canonical_cache"] is not False:
        sys_exit(f"batch-keys consumption flag drift ({batch_name})")
    if bk["pins"]["canonical_cache"] != BASE_CACHE_SHA_EXPECTED:
        sys_exit(f"batch-keys canonical cache pin drift ({batch_name})")
    if bk["pins"]["closure_classes"] != "b7241eb046e32f4900c9f9a976ada326c5124ad18c01de6b4eb40b97a8a7f24e":
        sys_exit(f"batch-keys closure-classes pin drift ({batch_name})")
    if bk["pins"]["refresh_summary"] != "5fe3e5ab176df05ef30894d6e0df6ceb292d3ac2280ff543e94bbee69e549de4":
        sys_exit(f"batch-keys refresh-summary pin drift ({batch_name})")
    if bk["pins"]["jsreplay"] != JSREPLAY_SHA_EXPECTED or bk["pins"]["quarantine"] != QUARANTINE_SHA_EXPECTED:
        sys_exit(f"batch-keys jsreplay/quarantine pin drift ({batch_name})")
    for e in bk["keys"]:
        if e["serving_class"] != serving_class or e["class_unknown_now_at_selection"] != 49:
            sys_exit(f"batch-keys serving class / selection-time unknown drift ({batch_name})")
    return bk


def val_gate_check(kit_dir: Path, hosts: list, subdir: str):
    for gate, (exp_b, exp_r, exp_n) in sorted(VAL_GATES.items()):
        for host in hosts:
            p = kit_dir / subdir / f"{gate}.{host}.out"
            if not p.is_file():
                sys_exit(f"val-gate file missing: {gate} {host}")
            row = parse_replay(p)
            if (row["budget"], row["result"], row["nodes"]) != (exp_b, exp_r, exp_n):
                sys_exit(f"val-gate {gate} {host} not node-exact")


def main() -> None:
    # --- base cache, merger, quarantine anchors ------------------------------
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
    if B37_E022_CACHE_ROW not in BASE_CACHE.read_text():
        sys_exit("BASE lacks the pinned e022 canonical row (batch-14 q007 dual-class)")
    q = json.loads(QUARANTINE.read_text())
    quarantined = {tuple(e["key"]) for e in q["entries"] if e.get("active")}

    # --- kit integrity ----------------------------------------------------------
    k36 = verify_kit(KIT_B36, KIT_B36_MANIFEST_SHA, KIT_B36_FILES)
    k37 = verify_kit(KIT_B37, KIT_B37_MANIFEST_SHA, KIT_B37_FILES)
    for kd, name in ((KIT_B36, "batch-36"), (KIT_B37, "batch-37")):
        if sha(kd / "scripts/jsreplay.js") != JSREPLAY_SHA_EXPECTED:
            sys_exit(f"jsreplay.js sha drift in the {name} kit (pinned solver image 8458...)")
    if sha(KIT_B4 / "output/status.log") != KIT_B4_STATUS_SHA:
        sys_exit("batch-4 status.log sha drift")
    if sha(KIT_B4 / "input/batch-keys.json") != KIT_B4_KEYS_SHA:
        sys_exit("batch-4 batch-keys.json sha drift")
    if sha(KIT_B4 / "output/raw/e001.p1.out") != KIT_B4_E001_P1_SHA:
        sys_exit("batch-4 e001.p1.raw sha drift")
    if sha(KIT_B4 / "output/raw/e001.p2.out") != KIT_B4_E001_P2_SHA:
        sys_exit("batch-4 e001.p2.raw sha drift")
    if sha(KIT_B4 / "output/raw/e002.p1.out") != KIT_B4_E002_P1_SHA:
        sys_exit("batch-4 e002.p1.raw sha drift")
    if sha(KIT_B4 / "output/raw/e002.p2.out") != KIT_B4_E002_P2_SHA:
        sys_exit("batch-4 e002.p2.raw sha drift")
    if sha(KIT_B4 / "scripts/jsreplay.js") != JSREPLAY_SHA_EXPECTED:
        sys_exit("batch-4 jsreplay.js sha drift (pinned solver image 8458...)")
    if sha(KIT_B4 / "scripts/runbatch.sh") != KIT_B4_RUNBATCH_SHA:
        sys_exit("batch-4 runbatch.sh sha drift")
    # batch-4 packet cross-verification against the published batch-37 kit clones
    b37_clone_keys = KIT_B37 / "sources/batch4-packet/batch-keys.json"
    b37_clone_status = KIT_B37 / "sources/batch4-packet/status.log"
    if sha(b37_clone_keys) != KIT_B4_KEYS_SHA or sha(b37_clone_status) != KIT_B4_STATUS_SHA:
        sys_exit("batch-37 kit batch4-packet clones do not match the batch-4 originals")

    # --- batch-keys gates (b36/b37 selection packets, frozen at kit selection) --
    bk36 = batch_keys_gates(KIT_B36, KIT_B36_KEYS_SHA,
                            "n11-centralreply-closure-batch36-keys-v1", "batch-36",
                            "batch-keys-b36.json", 45, 20421)
    bk37 = batch_keys_gates(KIT_B37, KIT_B37_KEYS_SHA,
                            "n11-centralreply-closure-batch37-keys-v1", "batch-37",
                            "batch-keys-b37.json", 47, 16371)
    if bk37["pins"]["batch4_batch_keys"] != KIT_B4_KEYS_SHA or bk37["pins"]["batch4_status"] != KIT_B4_STATUS_SHA:
        sys_exit("batch-37 batch-keys batch4 packet pins drift")
    consumed_dual = bk37.get("consumed_dual_class_excluded") or []
    if [e["key_id"] for e in consumed_dual] != B37_EXCLUDED_CANONICAL_IDS \
            or consumed_dual[0]["cache_row"] != B37_E022_CACHE_ROW \
            or int(consumed_dual[0].get("s5_index", consumed_dual[0].get("s5", B37_E022_S5))) != B37_E022_S5:
        sys_exit("batch-37 consumed_dual_class_excluded set drift (e022 pinned)")
    unconsumed37 = bk37.get("probed_unconsumed_same_class") or []
    if [e["key_id"] for e in unconsumed37] != ["e001", "e002"] \
            or unconsumed37[0]["budget_result_nodes"] != "15000000,2,882800" \
            or unconsumed37[1]["budget_result_nodes"] != "15000000,1,14112632":
        sys_exit("batch-37 probed_unconsumed_same_class drift (batch-4 e001/e002 pinned)")
    b4_all = json.loads((KIT_B4 / "input/batch-keys.json").read_text())
    if b4_all["schema"] != "n11-centralreply-closure-class16371-batch-input-v1":
        sys_exit("batch-4 batch-keys schema drift")
    if int(b4_all["class_index"]) != 16371 or b4_all["class_mask"] != [1153202979851993088, 16]:
        sys_exit("batch-4 batch-keys class identity drift")
    by36 = {k["key_id"]: k for k in bk36["keys"]}
    by37 = {k["key_id"]: k for k in bk37["keys"]}
    by4 = {k["key_id"]: k for k in b4_all["keys"]}
    if set(by36) != set(B36_PROBED_IDS):
        sys_exit("batch-36 key ids != the 45 probed keys")
    if set(by37) != set(B37_PROBED_IDS):
        sys_exit("batch-37 key ids != the 47 probed keys")
    if not {"e001", "e002"} <= set(by4) or len(by4) != 50:
        sys_exit("batch-4 key ids drift")

    # --- status logs (honest histories) -----------------------------------------
    got36 = parse_status(KIT_B36 / "output/status.log", B36_STATUS_LINES,
                        B36_STATUS_FIRST, B36_STATUS_FINAL, B36_WIN_HALT_LINES, r"d\d{3}")
    got37 = parse_status(KIT_B37 / "output/status.log", B37_STATUS_LINES,
                        B37_STATUS_FIRST, B37_STATUS_FINAL, B37_WIN_HALT_LINES, r"e\d{3}")
    got4 = parse_status(KIT_B4 / "output/status.log", B4_STATUS_LINES,
                        B4_STATUS_FIRST, B4_STATUS_FINAL, B4_WIN_HALT_LINES, r"e\d{3}")
    if set(got36) != set(B36_PROBED_IDS):
        sys_exit("batch-36 status verdict keys != the 45 probed keys")
    if set(got37) != set(B37_PROBED_IDS):
        sys_exit("batch-37 status verdict keys != the 47 probed keys")
    if set(got4) != set(B4_PROBED_IDS):
        sys_exit("batch-4 status verdict keys != the 2 probed keys")

    # --- two-pass raw verification ----------------------------------------------
    probed_specs = [
        ("batch-36", B36_RAW, B36_PROBED_IDS, by36, got36),
        ("batch-37", B37_RAW, B37_PROBED_IDS, by37, got37),
        ("batch-4", B4_RAW, B4_PROBED_IDS, by4, got4),
    ]
    raws = {}
    for name, rawdir, ids, keyset, statusrows in probed_specs:
        for kid in ids:
            ref = two_pass(rawdir, kid)
            if ref["stones"] != 5 or ref["is_or"] != 0:
                sys_exit(f"{kid}: wrong depth/or bit")
            if ref["budget"] != BUDGET:
                sys_exit(f"{kid}: kit budget drift")
            e = keyset.get(kid)
            if e is None:
                sys_exit(f"batch-keys missing {kid}")
            if ref["legal"] != int(e["legal"]) or ref["lo"] != str(e["lo"]) or ref["hi"] != str(e["hi"]):
                sys_exit(f"{kid}: legal/key disagreement raw vs batch-keys")
            if (ref["budget"], ref["result"], ref["nodes"]) != statusrows[kid]:
                sys_exit(f"{kid}: raw (budget,result,nodes) row != status verdict row")
            raws[(name, kid)] = ref

    # --- val-gates node-exact across hosts --------------------------------------
    val_gate_check(KIT_B36, VAL_HOSTS_B36, "val-gate")
    val_gate_check(KIT_B37, VAL_HOSTS_B37, "val-gate")
    for gate, fname in VAL_HOSTS_B4.items():
        p = KIT_B4 / "output/val-gate" / fname
        row = parse_replay(p)
        exp_b, exp_r, exp_n = VAL_GATES[gate]
        if (row["budget"], row["result"], row["nodes"]) != (exp_b, exp_r, exp_n):
            sys_exit(f"batch-4 val-gate {fname} not node-exact")

    # --- derive and gate the verdict sets ---------------------------------------
    def loss_win_exh(name, ids):
        loss_set = sorted(k for k in ids if raws[(name, k)]["result"] == 2)
        win_set = sorted(k for k in ids if raws[(name, k)]["result"] == 1)
        exh_set = sorted(k for k in ids if raws[(name, k)]["result"] == 0)
        if exh_set:
            sys_exit(f"{name}: probe-level EXHAUSTED set non-empty: {exh_set}")
        return loss_set, win_set
    loss36, win36 = loss_win_exh("batch-36", B36_PROBED_IDS)
    loss37, win37 = loss_win_exh("batch-37", B37_PROBED_IDS)
    loss4, win4 = loss_win_exh("batch-4", B4_PROBED_IDS)
    if loss36 != sorted(k for k in B36_PROBED_IDS if k not in B36_WIN_IDS):
        sys_exit("batch-36 decisive LOSS set != the 40 adopted candidates")
    if win36 != sorted(B36_WIN_IDS):
        sys_exit(f"batch-36 probe-level WIN set != the pinned 5 unconsumed WIN keys: {win36}")
    if loss37 != sorted(k for k in B37_PROBED_IDS if k not in B37_WIN_IDS):
        sys_exit("batch-37 decisive LOSS set != the 46 adopted candidates")
    if win37 != sorted(B37_WIN_IDS):
        sys_exit(f"batch-37 probe-level WIN set != the pinned unconsumed WIN key: {win37}")
    if loss4 != ["e001"] or win4 != ["e002"]:
        sys_exit("batch-4 packet decomposition 1 LOSS + 1 WIN drift")

    # --- raw inventories ----------------------------------------------------------
    for name, rawdir, ids, pat in (("batch-36", B36_RAW, B36_PROBED_IDS, r"^d\d{3}\.p[12]\.out$"),
                                   ("batch-37", B37_RAW, B37_PROBED_IDS, r"^e\d{3}\.p[12]\.out$"),
                                   ("batch-4", B4_RAW, B4_PROBED_IDS, r"^e\d{3}\.p[12]\.out$")):
        prim = sorted(p.name for p in rawdir.iterdir() if p.is_file() and re.match(pat, p.name))
        side = sorted(p.name for p in rawdir.iterdir() if p.is_file() and not re.match(pat, p.name))
        if prim != sorted(f"{kid}.{tag}.out" for kid in ids for tag in ("p1", "p2")):
            sys_exit(f"{name} raw primary inventory drift")
        if side != sorted(TRUNCATED_SIDECARS):
            sys_exit(f"{name} raw sidecar inventory drift: {side}")

    # --- gate the adopted keys against BASE / quarantine ------------------------
    emitted = set()
    batch_pins = {
        "batch-36": B36_ADOPTED_KEYS, "batch-37": B37_ADOPTED_KEYS, "batch-4": B4_ADOPTED_KEYS,
    }
    for name, ids in(("batch-36", loss36), ("batch-37", loss37), ("batch-4", loss4)):
        keypins = batch_pins[name]
        for kid in ids:
            key = norm_key(raws[(name, kid)])
            pins = keypins[kid]
            if key != pins["key"]:
                sys_exit(f"{kid}: raw key != pinned adopted key")
            if int(raws[(name, kid)]["nodes"]) != pins["nodes"] or int(raws[(name, kid)]["legal"]) != pins["legal"]:
                sys_exit(f"{kid}: adopted nodes/legal drift vs pins")
            if raws[(name, kid)]["budget"] != BUDGET:
                sys_exit(f"{kid}: decisive budget drift")
            e = {"batch-36": by36, "batch-37": by37, "batch-4": by4}[name][kid]
            if int(e["s5_index"]) != pins["s5"] or int(e["membership_class_count"]) != pins["mcc"]:
                sys_exit(f"{kid}: batch-keys s5/mcc drift vs pins")
            if key in quarantined:
                sys_exit(f"{kid}: quarantined key {key}")
            if key in base_keys:
                sys_exit(f"{kid}: key already in canonical BASE {key}; fresh-increment gate")
            if key in emitted:
                sys_exit(f"{kid}: duplicate emitted key {key}")
            emitted.add(key)
    if len(emitted) != 87:
        sys_exit(f"emitted keys {len(emitted)} != 87")

    # --- the unconsumed WIN keys must also be fresh (never adopted) ---------------
    for name, win_ids, winpins in (("batch-36", B36_WIN_IDS, B36_WIN_PINS),
                                   ("batch-37", B37_WIN_IDS, B37_WIN_PINS),
                                   ("batch-4", B4_WIN_IDS, B4_WIN_PINS)):
        for kid in win_ids:
            ref = raws[(name, kid)]
            key = norm_key(ref)
            if key != winpins[kid]["key"] or ref["nodes"] != winpins[kid]["nodes"]:
                sys_exit(f"{kid} (unconsumed WIN): raw vs pin drift")
            e = {"batch-36": by36, "batch-37": by37, "batch-4": by4}[name][kid]
            if int(e["s5_index"]) != winpins[kid]["s5"]:
                sys_exit(f"{kid} (unconsumed WIN): s5 drift vs pin")
            if key in base_keys:
                sys_exit(f"{kid} (unconsumed WIN): key already in canonical BASE {key}")
            if key in emitted:
                sys_exit(f"{kid} (unconsumed WIN): key collides with an adopted key")

    # --- node totals per pass -----------------------------------------------------
    totals = {}
    for name, ids, expected_adopted, expected_all, probed_ids in (
            ("batch-36", loss36, B36_ADOPTED_NODES, B36_ALL45_NODES, B36_PROBED_IDS),
            ("batch-37", loss37, B37_ADOPTED_NODES, B37_ALL47_NODES, B37_PROBED_IDS),
            ("batch-4", loss4, B4_ADOPTED_NODES, B4_ALL2_NODES, B4_PROBED_IDS)):
        n1 = sum(raws[(name, k)]["nodes"] for k in ids)
        nall = sum(raws[(name, k)]["nodes"] for k in probed_ids)
        if n1 != expected_adopted or nall != expected_all:
            sys_exit(f"{name}: node totals drift p1={n1} all={nall}")

    # --- emit the three increments + manifest --------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    def emit_increment(fname, hdr, adopted_ids, keypins):
        rows = [(keypins[k]["key"][0], keypins[k]["key"][1], keypins[k]["nodes"]) for k in adopted_ids]
        rowlines = [f"s5verdict,{lo},{hi},5,2,{nodes}" for lo, hi, nodes in sorted(rows)]
        blob = ("\n".join(hdr + rowlines) + "\n").encode("utf-8")
        path = OUT / fname
        path.write_bytes(blob)
        return hashlib.sha256(blob).hexdigest()

    hdr_b4 = [
        "# n11 central-reply closure batch-4 (class 16371) 1-LOSS",
        "#   canonical-adoption increment (Part DZ, 2026-11-25).",
        "# The published batch-4 kit (2026-11-22 declaration-only drive)",
        "#   halted at the second WIN (e002): only e001/e002 carry honest",
        "# two-pass fresh-cold labels at budget 15M (e001 LOSS adopted",
        "# here; the probe-level WIN e002 stays unconsumed, scrutiny-",
        "# owner C++ gate 9193f5b6...).  The batch-4 kit is byte-pinned",
        "#   file-by-file here and cross-verified against the published",
        "#   batch-37 kit batch4-packet clones.  ONLY the 1 fresh LOSS",
        "#   row is consumed into the canonical cache by this increment.",
        "# 2-pass node-exact exact-S5 verdicts, fresh cold, pinned",
        "#   jsreplay.js sha256",
        "#   845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
    ]
    hdr_b36 = [
        "# n11 central-reply closure batch-36 (class 20421) 40-LOSS",
        "#   canonical-adoption increment (Part DZ, 2026-11-25).",
        "# The published batch-36 kit (Part DX probe drive) probed",
        "#   ALL 45 of 45 clean keys honest two-pass fresh-cold at budget",
        "#   15M: 40 LOSS (adopted here), 5 probe-level WIN",
        "#   {d008,d009,d021,d026,d029}, pre-registered WIN-HALT",
        "#   markers, consumed NOWHERE by this Part (scrutiny-owner C++",
        "#   gate 9193f5b6...), 0 EXHAUSTED, MISMATCH 0.  The batch-3",
        "#   (2026-11-22) honest-labeled unconsumed rows d001/d003 (LOSS)",
        "#   and d002 (WIN) of class 20421 stay unconsumed: their kit",
        "#   publishes no two-pass raws (adoption candidate for a later",
        "#   Part).  ONLY the 40 fresh LOSS rows are consumed into the",
        "#   canonical cache by this increment.",
        "# gates: kit MANIFEST sha-verified file-by-file (160 files);",
        "#   45 two-pass fresh-cold raw re-verification with",
        "#   '# replay_done' on both passes; (budget,result,nodes)",
        "#   agreement with the 50-line honest-history status pins;",
        "#   raw/batch-keys agreement on (legal,lo,hi) and",
        "#   (s5_index, membership_class_count); raw inventory == 90",
        "#   primaries and nothing else; val-gate node-exact across the",
        "#   published-baseline and dx-host outputs per molecule;",
        "#   adopted keys distinct, absent from BASE 23d40e36... (6,573",
        "#   rows, WIN 158 / LOSS 6,415) and from the quarantine",
        "#   registry; adopted per-pass node total 159499387 (all-45",
        "#   total 183921575).",
        "# Loss-only adoption asserts no root verdict; any class-20421",
        "#   scheduling effect is derived only by the reaudit refresh",
        "#   (Board fail-closed child verification).  11x11 stays",
        "#   UNKNOWN; nodes are bookkeeping, never verdicts.",
    ]
    hdr_b37 = [
        "# n11 central-reply closure batch-37 (class 16371) 46-LOSS",
        "#   canonical-adoption increment (Part DZ, 2026-11-25).",
        "# The published batch-37 kit (Part DY probe drive) probed",
        "#   ALL 47 of 47 clean keys honest two-pass fresh-cold at",
        "#   budget 15M: 46 LOSS (adopted here), 1 probe-level WIN (e042",
        "#   = batch-13 p028 dual-class packet key, pre-registered",
        "#   WIN-HALT marker, consumed NOWHERE by this Part, scrutiny-",
        "#   owner C++ gate 9193f5b6...), 0 EXHAUSTED, MISMATCH 0.  The",
        "#   already-canonical dual-class child e022 (s5 546606,",
        "#   batch-14 q007, BASE row s5verdict,1153202979868770304,16,",
        "#   5,2,1494975) is excluded from the batch-37 target set.",
        "# gates: kit MANIFEST sha-verified file-by-file (166 files);",
        "#   47 two-pass fresh-cold raw re-verification with",
        "#   '# replay_done' on both passes; (budget,result,nodes)",
        "#   agreement with the 48-line honest-history status pins;",
        "#   raw/batch-keys agreement on (legal,lo,hi) and",
        "#   (s5_index, membership_class_count); raw inventory == 94",
        "#   primaries and nothing else; val-gate node-exact across the",
        "#   published-baseline and dy-host outputs per molecule;",
        "#   adopted keys distinct, absent from BASE 23d40e36... (6,573",
        "#   rows, WIN 158 / LOSS 6,415) and from the quarantine",
        "#   registry; adopted per-pass node total 96295019 (all-47",
        "#   total 99204059).",
        "# Loss-only adoption asserts no root verdict; any class-16371",
        "#   scheduling effect is derived only by the reaudit refresh",
        "#   (Board fail-closed child verification).  11x11 stays",
        "#   UNKNOWN; nodes are bookkeeping, never verdicts.",
    ]
    sha_b4 = emit_increment("increment-b4loss1-20261125.cache", hdr_b4, ["e001"], B4_ADOPTED_KEYS)
    sha_b36 = emit_increment("increment-b36loss40-20261125.cache", hdr_b36, loss36, B36_ADOPTED_KEYS)
    sha_b37 = emit_increment("increment-b37loss46-20261125.cache", hdr_b37, loss37, B37_ADOPTED_KEYS)

    manifest = {
        "schema": "dz-adoption-increments-manifest-v1",
        "batches": [
            {"batch": "batch-4", "class_index": 16371, "keys_total": 2,
             "adopted_loss_ids": list(loss4), "already_adopted_ids": [],
             "unadopted_win_ids": list(win4), "exhausted_excluded_ids": [],
             "probed_ids": list(B4_PROBED_IDS),
             "status_log_sha256": KIT_B4_STATUS_SHA, "status_log_lines": B4_STATUS_LINES,
             "status_log_first_line": B4_STATUS_FIRST, "status_log_final_line": B4_STATUS_FINAL,
             "status_log_win_halt_lines": list(B4_WIN_HALT_LINES),
             "kit_integrity": "file-level pins (no 2026-11-22 kit MANIFEST): status "
                               "63c2d969..., batch-keys 70b8a4c8..., raws 84a3c287.../"
                               "81089532.../1914d048..., val-gate 4 molecules node-exact, "
                               "byte-cross-verified against the published batch-37 kit "
                               "batch4-packet clones",
             "val_gate_multi_host_node_exact": True,
             "total_nodes_pass_one": B4_ADOPTED_NODES, "total_nodes_pass_two": B4_ADOPTED_NODES,
             "stop_rule": "WIN-HALT at the second key e002 (2 of 2 packet keys honest-"
                          "labeled; e002 verdict not consumed)"},
            {"batch": "batch-36", "class_index": 20421, "keys_total": 45,
             "adopted_loss_ids": list(loss36), "already_adopted_ids": [],
             "unadopted_win_ids": list(win36), "exhausted_excluded_ids": [],
             "probed_ids": list(B36_PROBED_IDS),
             "input_sha256": KIT_B36_KEYS_SHA,
             "status_log_sha256": KIT_B36_STATUS_SHA, "status_log_lines": B36_STATUS_LINES,
             "status_log_first_line": B36_STATUS_FIRST, "status_log_final_line": B36_STATUS_FINAL,
             "status_log_win_halt_lines": list(B36_WIN_HALT_LINES),
             "status_log_mismatch_lines": [], "status_log_retry_lines": [],
             "kit_integrity": {"kit_manifest_sha256": KIT_B36_MANIFEST_SHA,
                               "kit_files_verified": k36},
             "val_gate_multi_host_node_exact": True,
             "total_nodes_pass_one": B36_ADOPTED_NODES, "total_nodes_pass_two": B36_ADOPTED_NODES,
             "stop_rule": "batch-36 probe-complete (45/45 clean keys carry honest "
                          "two-pass labels: 40 LOSS @15M adopted + 5 probe-level WIN "
                          "unconsumed pending the scrutiny-owner C++ gate + 0 EXHAUSTED; "
                          "the batch-3 unconsumed rows d001/d003 (LOSS, raws unpublished) "
                          "and d002 (WIN) stay unconsumed; verdict not consumed)"},
            {"batch": "batch-37", "class_index": 16371, "keys_total": 47,
             "adopted_loss_ids": list(loss37),
             "already_adopted_ids": list(B37_EXCLUDED_CANONICAL_IDS),
             "unadopted_win_ids": list(win37), "exhausted_excluded_ids": [],
             "probed_ids": list(B37_PROBED_IDS),
             "input_sha256": KIT_B37_KEYS_SHA,
             "status_log_sha256": KIT_B37_STATUS_SHA, "status_log_lines": B37_STATUS_LINES,
             "status_log_first_line": B37_STATUS_FIRST, "status_log_final_line": B37_STATUS_FINAL,
             "status_log_win_halt_lines": list(B37_WIN_HALT_LINES),
             "status_log_mismatch_lines": [], "status_log_retry_lines": [],
             "kit_integrity": {"kit_manifest_sha256": KIT_B37_MANIFEST_SHA,
                               "kit_files_verified": k37},
             "val_gate_multi_host_node_exact": True,
             "total_nodes_pass_one": B37_ADOPTED_NODES, "total_nodes_pass_two": B37_ADOPTED_NODES,
             "stop_rule": "batch-37 probe-complete (47/47 clean keys carry honest "
                          "two-pass labels: 46 LOSS @15M adopted + 1 probe-level WIN "
                          "(e042, batch-13 p028 dual-class packet key) unconsumed pending "
                          "the scrutiny-owner C++ gate; the already-canonical dual-class "
                          "child e022 was excluded at selection; verdict not consumed)"},
        ],
        "resolved_ids": sorted(loss4 + loss36 + loss37),
        "loss_ids": sorted(loss4 + loss36 + loss37),
        "win_ids": sorted(win4 + win36 + win37),
        "unadopted_win_ids": sorted(win4 + win36 + win37),
        "exhausted_excluded_ids": [],
        "exhausted_rows": [],
        "row_counts": {"probed_rows": 2 + 45 + 47,
                        "adopted_loss_rows": 87, "prior_adopted_loss_rows": 0,
                        "wins": 7, "exhausted_excluded": 0, "fragments_unprobed": 0,
                        "fileless_unprobed": 0},
        "sha256": {"loss_b4loss1": sha_b4, "loss_b36loss40": sha_b36,
                   "loss_b37loss46": sha_b37},
        "full_packet_eq_loss_only": False,
        "win_scenario_exists": True,
        "win_scenario_note": "seven probe-level WIN rows stay unconsumed (batch-36 "
                             "d008/d009/d021/d026/d029, batch-37 e042, batch-4 e002): each "
                             "belongs to the scrutiny-owner C++ second-implementation "
                             "gate pin 9193f5b6...; loss-only adoption NEVER frees a class "
                             "while any unconsumed WIN child remains",
        "full_packet_eq_loss_only_rationale":
            "the three packets together are NOT loss-only: seven probe-level WIN rows "
            "stay unconsumed and NOT adopted; e022 was already canonical before this "
            "Part; the adopted packet is the 87 fresh LOSS rows plus nothing else; "
            "classes 16371 and 20421 are NOT freed",
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_sha256": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "base_cache_absent_hits_for_emitted": 0,
        "quarantine_hits": 0,
        "interpretation_guard":
            "canonical 87-LOSS adoption increment set: only the 87 fresh LOSS rows are "
            "consumed into the canonical cache via the fail-closed union merger; the "
            "seven probe-level WINs are consumed NOWHERE (no verdict claim, no "
            "exclusion claim) and belong to the scrutiny owner; the batch-3 "
            "honest-labeled unconsumed rows (d001/d003 LOSS raws unpublished, d002 WIN) "
            "stay unconsumed outside this Part; adopting 87 LOSS rows does NOT free "
            "classes 16371/20421 (unconsumed WIN children remain); loss-only adoption "
            "asserts no root verdict and no coverage claim; any scheduling effect is "
            "derived only by the reaudit refresh (Board fail-closed child "
            "verification); 11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts",
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"INCREMENTS rows=87 b4={sha_b4[:12]} b36={sha_b36[:12]} b37={sha_b37[:12]}")


if __name__ == "__main__":
    main()
