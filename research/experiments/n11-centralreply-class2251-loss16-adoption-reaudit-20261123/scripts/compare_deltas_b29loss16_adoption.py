"""Batch-29 (class 2251) 16-LOSS adoption reaudit delta extractor
(Part CU).

Fail-closed, read-only audit executing the single-owner Part CU
declaration (2026-11-23; publish-then-execute).  Compares the published
BASE refresh outputs (Part CO reaudit on the canonical cache 854800f3...,
6,301 rows) against the single post-adoption computation:

  ADOPTED-CANONICAL = BASE + the 16 fresh LOSS rows
  (batch-29 / class 2251: ab001..ab016; nodes total 57,463,971)

The batch is a PARTIALLY probed takeover drive-1 checkpoint book: exactly
16 of 54 keys were probed (2-pass node-exact, all result 2 LOSS, budget
15M exhausted on none), the remaining 38 keys ab017..ab054 are fileless
UNPROBED and carry NO verdict.  No WIN row and no EXHAUSTED row has been
observed among the probed keys; the adopted packet is loss-only ON THE
PROBED SET.  The batch-29 host and the takeover host were cross-validated
by the published 4-pattern doubled val-gate (published-baseline ==
batch29-host == takeover-host, node-exact 4/4: two adaptive 2M
exhaustions (0, 2000000) and two 15M LOSS probes (2, 3651923) and
(2, 5040200)).  class 2251 does NOT free: 38 unknown children remain
(the fileless keys), so it stays unknown with rank 35 -> 4 in the
closure table.

Gates (fail-closed, machine-checked) mirror the Part CO extractor
discipline adapted to the partially-probed 1-kit / 16-LOSS-row /
0-WIN / 0-EXHAUSTED / 38-fileless shape of batch-29 drive-1:

  * sha256 pins: increment, increments manifest, scenario cache, base
    cache, base summary, scenario summary, base/scenario closure-classes.csv,
    base/scenario per-root-coverage.csv, scenario probe-worklist.csv, the
    batch-29 batch-keys file, the drive status log, the kit
    MANIFEST-sha256.txt (with a full file-by-file sha re-verification of
    all 71 listed kit files), and all 16 val-gate files
    (4 probe patterns x {input.csv, published-baseline.out,
    batch29-host.out, takeover-host.out});
  * status log gates: 16 lines, every line a strict
    "<ts> <kid> PASS 15000000,2,<nodes>" match, the key-id set == the
    adopted id set, the per-key node values == the adopted row pins, the
    timestamp window bounded, the final verdict row pinned;
  * manifest (b29loss16-increments-manifest-v1): 16 adopted LOSS /
    0 WIN / 0 EXHAUSTED / 38 fileless UNPROBED / 0 fragments, loss sha ==
    increment sha, merger pin, base cache pin 854800f3... (6,301 rows,
    zero absent hits for emitted rows, zero quarantine hits), the
    takeover val-gate 4-file sha block and double-host node-exact flag
    pinned, node totals pinned (57,463,971 both passes), stop rule pinned;
  * val-gate triple-host gates: for each of the 4 probe patterns the
    replay rows of published-baseline / batch29-host / takeover-host are
    byte-compared field-by-field except wall time (node-exact), the
    budgets/results/nodes pinned (adaptive 2M exhaustion (0, 2000000)
    x2, 15M LOSS (2, 3651923) and (2, 5040200)), the two val-gate
    molecules canonical-safe, not quarantined, and disjoint from the
    batch keys, BASE, the increment and the update8 receipts;
  * independent two-pass raw re-verification of ALL 16 probed keys from
    the kit raws: both passes agree exactly, every row is result 2 (LOSS)
    at budget 15M with the published node counts, the raw key/legal == the
    batch-keys entry, and the raw inventory is exactly the 32 files
    ab001..ab016 x {p1,p2} (the 38 fileless keys have NO raw files);
  * increment == exactly the 16 fresh LOSS rows; the 38 fileless keys
    asserted NOT in the increment, NOT in BASE, NOT in the scenario cache,
    NOT in the update8 receipts;
  * scenario cache == BASE rows + the 16 increment rows with verdict
    agreement (6,317 rows; 158 WIN / 6,159 LOSS);
  * every graph holder class of every adopted key (union 48):
    scenario unknown_now == BASE unknown_now - own membership in the
    increment (class 2251 own == 16; per-key holder counts == batch-keys
    membership_class_count: 4 for fifteen keys, 3 for ab010);
  * the published refresh recomputes (class statuses with Board
    free-candidate child verification, known-universe counts, per-root
    coverage) are re-executed from graph + update8 + cache and asserted
    equal to the published BASE (Part CO reaudit) and scenario outputs
    before any delta is emitted;
  * status transitions pinned all-stable (excluded 390 / excluded_now 23 /
    free_now 38 / unknown 34,498 on both sides), no excluded_now flips,
    no newly free class beyond the machine recomputation (the loss-only
    partial adoption frees nothing: free_now stays 38), no per-root
    coverage regression, root 27 stays 119/119;
  * closure table: class 2251 unknown_now 54 -> 38 (rank 35 -> 4); the
    only other unknown_now changes are the holder classes 1181
    (102 -> 101, rank 602 -> 568), 1182 (104 -> 103, rank 684 -> 661)
    and 11426 (60 -> 59, rank 190 -> 152); every class that changes
    unknown_now is a holder with exact own-membership arithmetic and
    every other column stable; exactly 125 classes churn rank
    with stable unknown (pure ranking bookkeeping, none of them a holder
    of the adopted keys; {'excluded_now': 3, 'unknown': 122}); table stays 808 rows with
    left == {1945, 19645} and entered == {386, 1044} (tie-swap churn in
    the anchor candidate selection, machine-observed; identical
    aggregate stats); anchors 23101 / 1849 / 16757 stay fully stable
    (rank/unknown 1/1, 2/1, 3/29);
  * update8 refresh: resolved_count / remaining untouched (141 / 31,718
    on both sides; the 16 adopted keys are NOT update8 baseline
    requirements, machine-observed), no resolution lost, newly resolved
    set empty;
  * metrics pinned (both sides exact): excluded 390 / excluded_now 23 /
    free_now 38 / unknown 34,498 class_status_counts pairs; joint
    greedy 38,310 -> 35,691; worklist 64,828 -> 64,809; group best
    options 2,119 stable; per-root greedy movers only roots 16
    (2,971 -> 2,970) and 37 (4,001 -> 3,852); roots_summary_moved EMPTY;
    worklist serving rows of class 2251 shrink 54 -> 38 (exactly the
    16 adopted keys leave), and no adopted key row remains in the
    scenario worklist.

Scheduling quantities are bookkeeping, never verdicts.  11x11 stays
UNKNOWN; the 38 fileless keys carry no verdict; nodes are bookkeeping,
never verdicts.
"""
import csv
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

_here = Path(__file__).resolve()
_CANDS = [q for q in _here.parents if (q / "research" / "experiments").is_dir()]
if not _CANDS:
    raise SystemExit("GATE FAILED: repo root (research/experiments) not found above this script")
ROOT = _CANDS[0]
EXP = _here.parents[1]
OUT = EXP / "output/decomp-deltas-b29loss16-adoption.json"

GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_DIR = ROOT / "research/experiments/n11-centralreply-class5343-loss7-adoption-reaudit-20261123/reaudit/output"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class5343-loss7-adoption-reaudit-20261123/output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-20261123.cache"
KIT_DIR = ROOT / "research/experiments/n11-centralreply-closure-class2251-batch29-20261123"
SCEN_OUT = EXP / "reaudit/output"
INCR_CACHE = EXP / "output/increment-b29loss16-20261123.cache"
MANIFEST = EXP / "output/increments-manifest.json"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-20261123.cache"

INCR_SHA = "bab011e376090f9f4732d63f0084f326ba72dada5cf699d5aabc7e014c29ae24"
MANIFEST_SHA = "f9f58ee101d53f0598ee01c5c54d5b277797a9e882cfb478ab7f7b3010e191e0"
SCEN_CACHE_SHA = "30ddad9dc0add7e21698e864b5c202b8e6ebd3e396c4eb6156a85ff2d34005c4"
BASE_CACHE_SHA = "854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d"
BASE_SUMMARY_SHA = "4727fb2b991d78107a67aa3ef2bf533be042907214216f8d363a23f884228179"
SCEN_SUMMARY_SHA = "b60d71a29730f19a589a065b446664a80bdf1008e8493b25c7e11f43e8246543"
BASE_CLOSURE_SHA = "9d3965d94db9fc8005fda1cd24aadf1b515a799e5558448a391489cd24caa85d"
BASE_PRC_SHA = "8e6fb981ee637d896cbf6d378d0543db06d5552da725cba2fa24130cc6fd4809"
SCEN_CLOSURE_SHA = "3019d37f72ac6a46672f0fd027eae1c42c708f6e68d082925d85243d64195754"
SCEN_PRC_SHA = "61dbd39af70405d69c808c65e31a57ea10393f66bd0f3c59100e7a4ef035a081"
SCEN_WORKLIST_SHA = "0d7474e1adfbdbc8db438605e3e36310c1d8e656ab8c92899183f29b870a931c"
B29_KEYS_SHA = "330c0b9f3166e9f6e21b739a851a881d800ab9f58a14dccaa0c772118dee716c"
STATUS_LOG_SHA = "6b877344b9abea348a9b221f587a771857d3c4091f88fa460ef12595722183e2"
KIT_MANIFEST_SHA = "7c12423364a292844d4b49a048e910a4be3f9b45cc08a4b31d0bd35233caab84"
MERGE_AUDIT_SHA = "8f611fe171f0b34c813035e4cf0ff59447f2419909cbe9fceff1f7d7cb1c8252"
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"

SCENARIO = "ADOPTED-CANONICAL"
UNIVERSE_SIZE = 31859
RECEIPT_COUNT = 23
ADOPTED_ROWS = 16
B29_CLASS = 2251
BUDGET = 15000000
KIT_FILES = 71
STATUS_LINES = 16
STATUS_FINAL_ROW = '2026-11-23T21:52:15Z ab016 PASS 15000000,2,4258557'
STATUS_TS_MIN = "2026-11-23T21:43:13Z"
STATUS_TS_MAX = "2026-11-23T21:52:15Z"
STOP_RULE = 'takeover drive-1 checkpoint 1/3 (16/54 keys probed; the takeover session halted after the checkpoint; probed keys all ran to 2-pass completion; verdict not consumed)'
STATUS_LOG_NOTE = ("the drive log lists exactly the 16 probed keys, all two-pass PASS "
                   "verdicts (result 2) with per-key node counts; lines are completion-"
                   "ordered, not key-ordered (parallel workers); no junk rows, no "
                   "fragment rows, no truncated sidecars")
ADOPTED_IDS = ["ab%03d" % i for i in range(1, 17)]
FILELESS_IDS = ["ab%03d" % i for i in range(17, 55)]
PROBED_IDS = list(ADOPTED_IDS)
ADOPTED_TOTAL_NODES = 57463971
NEWLY_RESOLVED_S5 = []
MEMBERSHIP_EXPECT = {'ab001': 4,
 'ab002': 4,
 'ab003': 4,
 'ab004': 4,
 'ab005': 4,
 'ab006': 4,
 'ab007': 4,
 'ab008': 4,
 'ab009': 4,
 'ab010': 3,
 'ab011': 4,
 'ab012': 4,
 'ab013': 4,
 'ab014': 4,
 'ab015': 4,
 'ab016': 4}
HOLDER_UNION_SIZE = 48
EXPECTED_MEMBER_LOSS_COUNTS = {2251: 16}  # every other holder class: exactly 1
ALLOWED_TRANSITIONS = {"excluded": ["excluded"], "excluded_now": ["excluded_now"],
                       "free_now": ["free_now"], "unknown": ["unknown", "free_now"]}
STATUS_TRANSITIONS_PIN = {'excluded->excluded': 390,
 'excluded_now->excluded_now': 23,
 'free_now->free_now': 38,
 'unknown->unknown': 34498}
# closure-table pins (observed machine-side, declared before the official run):
CLOSURE_COUNTS = (808, 808)
CLASS_2251_CLOSURE_PIN = ((35, 54), (4, 38))
CHANGED_UNKNOWN_CLOSURE_PIN = {1181: ((602, 102), (568, 101)), 1182: ((684, 104), (661, 103)), 11426: ((190, 60), (152, 59))}
STABLE_UNKNOWN_RANK_CHURN_COUNT = 125
CHURN_STABLE_STATUS_DIST = {'excluded_now': 3, 'unknown': 122}
CLOSURE_ENTERED_PIN = {386: (572, 101), 1044: (461, 97)}
CLOSURE_LEFT_PIN = {1945: (461, 97), 19645: (571, 101)}
CLOSURE_ANCHORS_PIN = {1849: (2, 1), 16757: (3, 29), 23101: (1, 1)}
# metrics pins (declared before the official run; BASE -> scenario)
METRICS_PIN = {
    "excluded_now_classes": (23, 23),
    "free_now_classes": (38, 38),
    "unknown_classes": (34498, 34498),
    "update8_remaining_now": (31718, 31718),
    "update8_resolved_count": (141, 141),
    "update8_win_hit_groups": (0, 0),
    "update8_groups_free_now": (131, 131),
    "joint_greedy_unique_groups": (2119, 2119),
    "joint_greedy_union_size": (38310, 35691),
    "probe_worklist_total": (64828, 64809),
    "group_best_options_nonfree": (2119, 2119),
    "closure_classes_count": (808, 808),
}
PRG_MOVERS_PIN = {'16': (2971, 2970), '37': (4001, 3852)}

ADOPTED = {'ab001': {'key': (1155314042043105281, 0),
           'legal': 95,
           'nodes': 4265342,
           's5': 3964},
 'ab002': {'key': (1155314042043105282, 0),
           'legal': 97,
           'nodes': 3662776,
           's5': 9935},
 'ab003': {'key': (1155314042043105284, 0),
           'legal': 98,
           'nodes': 4447441,
           's5': 15659},
 'ab004': {'key': (1155314042043105288, 0),
           'legal': 92,
           'nodes': 2687012,
           's5': 21341},
 'ab005': {'key': (1155314042043105296, 0),
           'legal': 96,
           'nodes': 3714648,
           's5': 26610},
 'ab006': {'key': (1155314042043107328, 0),
           'legal': 96,
           'nodes': 3855756,
           's5': 33712},
 'ab007': {'key': (1155314042043109376, 0),
           'legal': 83,
           'nodes': 3763776,
           's5': 38148},
 'ab008': {'key': (1155314042043113472, 0),
           'legal': 93,
           'nodes': 2890562,
           's5': 42711},
 'ab009': {'key': (1155314042043138048, 0),
           'legal': 87,
           'nodes': 1786048,
           's5': 51145},
 'ab010': {'key': (1155314042043170816, 0),
           'legal': 88,
           'nodes': 4242063,
           's5': 53947},
 'ab011': {'key': (1155314042047299584, 0),
           'legal': 92,
           'nodes': 4806135,
           's5': 56596},
 'ab012': {'key': (1155314042051493888, 0),
           'legal': 89,
           'nodes': 2606954,
           's5': 60153},
 'ab013': {'key': (1155314042059882496, 0),
           'legal': 87,
           'nodes': 2284195,
           's5': 63620},
 'ab014': {'key': (1155314042076659712, 0),
           'legal': 91,
           'nodes': 4280600,
           's5': 67275},
 'ab015': {'key': (1155314050633039872, 0),
           'legal': 98,
           'nodes': 3912106,
           's5': 73062},
 'ab016': {'key': (1155314059222974464, 0),
           'legal': 96,
           'nodes': 4258557,
           's5': 76023}}

VAL_GATES = {'at2m-s5-1152921504606851072-536870946': {'batch29_host': 'cc03306db457edacc17a3337883a7aa561e0d7953ae8510c7e4777b04a089229',
                                           'hi': 536870946,
                                           'input_csv': 'ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348',
                                           'legal': 98,
                                           'lo': 1152921504606851072,
                                           'published_baseline': '6e902ab147b117bb09216070f272969418247f5eb73870bf7705c8220fc9c35c',
                                           'takeover_host': 'ff4dbb8344400c6cc629038e833110e4b5ada5bf24bfa70d07a525d159276a22'},
 'at2m-s5-1188950301626860544-536870912': {'batch29_host': '7dc3b5d7871aa92a2e2a27365f8a8952ddf9b391c2aeeb4a59b6c21b5c0c6c80',
                                           'hi': 536870912,
                                           'input_csv': '56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62',
                                           'legal': 99,
                                           'lo': 1188950301626860544,
                                           'published_baseline': 'eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24',
                                           'takeover_host': 'eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24'},
 'first-15m-s5-1152921504606851072-536870946': {'batch29_host': '47567a803b2a57b7f840d6a483421b0d6e34e134bb885b6685f8d573c32fdaf2',
                                                'hi': 536870946,
                                                'input_csv': 'ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348',
                                                'legal': 98,
                                                'lo': 1152921504606851072,
                                                'published_baseline': '8035fe54f8c79dd44c4c80d6b38e4ad39d3d4660eaf57a32799969087b8a5591',
                                                'takeover_host': '8675ae4b4904485d5ffde72578342d69668a5c8bd39b82d93193177f515ebafb'},
 'second-15m-s5-1188950301626860544-536870912': {'batch29_host': 'a41b4d230e39b40445533603b92cd23237e1e717a2440fc646454d321dddd2d3',
                                                 'hi': 536870912,
                                                 'input_csv': '56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62',
                                                 'legal': 99,
                                                 'lo': 1188950301626860544,
                                                 'published_baseline': '91dffdec33a409bc3e5f6eb50c0ea95313574ef74d0692c5912a0814946de1fb',
                                                 'takeover_host': '7fd4454283b2b6d62f7381a239b97b3eba63830a72d870107622e936157c43ed'}}
VAL_GATE_PATTERNS = {
    "at2m-s5-1152921504606851072-536870946": (2000000, 0, 2000000),
    "at2m-s5-1188950301626860544-536870912": (2000000, 0, 2000000),
    "first-15m-s5-1152921504606851072-536870946": (15000000, 2, 3651923),
    "second-15m-s5-1188950301626860544-536870912": (15000000, 2, 5040200),
}


def fail(msg):
    print("GATE FAILED: " + msg, file=sys.stderr)
    raise SystemExit(1)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_cache(path):
    rows = {}
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        for lineno, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                fail(f"invalid cache row {lineno} in {path}: {row}")
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            key = (lo, hi)
            if stones != 5 or verdict not in (1, 2) or nodes < 0:
                fail(f"invalid cache verdict at row {lineno} in {path}: {row}")
            if key in rows and verdict != rows[key][0]:
                fail(f"cache conflict for {key} in {path}")
            rows[key] = (verdict, nodes)
    return rows


def load_keys(batch_dir, class_index):
    bk = json.loads((batch_dir / "input/batch-keys.json").read_text())
    if bk["class_index"] != class_index:
        fail(f"batch-keys class_index {bk['class_index']} != {class_index}")
    gs_raw = bk.get("groups_served_full")
    if gs_raw is not None:
        groups_served = sorted((int(e["first"]), int(e["third"])) for e in gs_raw)
    else:
        e = bk["groups_served_first_seen"]
        groups_served = sorted({(int(e["first"]), int(e["third"]))})
    if not groups_served:
        fail(f"batch-keys groups-served empty for class {class_index}")
    return bk, groups_served


def parse_raw(path, tag, kid):
    txt = path.read_text()
    if "# replay_done" not in txt:
        fail(f"{kid} raw pass {tag} lacks the '# replay_done' completeness guard")
    rr = None
    for line in txt.splitlines():
        if not line.startswith("replay,"):
            continue
        parts = line.split(",")
        row = (int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5]),
               int(parts[6]), int(parts[7]), int(parts[9]), int(parts[10]))
        if rr is not None:
            fail(f"{kid} multiple replay rows in pass {tag}")
        rr = row
    if rr is None:
        fail(f"{kid} no replay row in pass {tag}")
    return rr


def parse_valgate_out(path):
    txt = Path(path).read_text()
    if "# replay_done" not in txt:
        fail(f"val-gate out {path.name} lacks the '# replay_done' completeness guard")
    rr = None
    for line in txt.splitlines():
        if not line.startswith("replay,"):
            continue
        parts = line.split(",")
        row = (int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5]),
               int(parts[6]), int(parts[7]), int(parts[9]), int(parts[10]))
        if rr is not None:
            fail(f"val-gate out {path.name} has multiple replay rows")
        rr = row
    if rr is None:
        fail(f"val-gate out {path.name} has no replay row")
    return rr


def main():
    # --- sha pins ------------------------------------------------------------
    for name, p, want in (("increment", INCR_CACHE, INCR_SHA),
                          ("manifest", MANIFEST, MANIFEST_SHA),
                          ("scenario cache", SCEN_CACHE, SCEN_CACHE_SHA),
                          ("base cache", BASE_CACHE, BASE_CACHE_SHA),
                          ("base summary", BASE_DIR / "refresh-summary.json", BASE_SUMMARY_SHA),
                          ("scenario summary", SCEN_OUT / "refresh-summary.json", SCEN_SUMMARY_SHA),
                          ("base closure-classes", BASE_DIR / "closure-classes.csv", BASE_CLOSURE_SHA),
                          ("base per-root-coverage", BASE_DIR / "per-root-coverage.csv", BASE_PRC_SHA),
                          ("scenario closure-classes", SCEN_OUT / "closure-classes.csv", SCEN_CLOSURE_SHA),
                          ("scenario per-root-coverage", SCEN_OUT / "per-root-coverage.csv", SCEN_PRC_SHA),
                          ("scenario probe-worklist", SCEN_OUT / "probe-worklist.csv", SCEN_WORKLIST_SHA),
                          ("batch-29 batch keys", KIT_DIR / "input/batch-keys.json", B29_KEYS_SHA),
                          ("batch-29 status log", KIT_DIR / "output/status.log", STATUS_LOG_SHA),
                          ("batch-29 kit manifest", KIT_DIR / "MANIFEST-sha256.txt", KIT_MANIFEST_SHA),
                          ("merge-audit run1", EXP / "output/merge-audit-run1.json", MERGE_AUDIT_SHA),
                          ("merge-audit run2", EXP / "output/merge-audit-run2.json", MERGE_AUDIT_SHA),
                          ("merge-audit run3", EXP / "output/merge-audit-run3.json", MERGE_AUDIT_SHA)):
        got = sha(p)
        if got != want:
            fail(f"{name} sha256 drift: {got} != {want}")

    # --- kit full file-by-file sha re-verification ---------------------------
    entries = []
    for line in (KIT_DIR / "MANIFEST-sha256.txt").read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            fail(f"kit manifest line not '<sha256> <path>': {line}")
        entries.append((parts[0], parts[1]))
    if len(entries) != KIT_FILES:
        fail(f"kit manifest lists {len(entries)} files != {KIT_FILES}")
    for want_sha, rel in entries:
        p = KIT_DIR / rel
        got = sha(p)
        if got != want_sha:
            fail(f"kit file sha drift at {rel}: {got} != {want_sha}")
    kit_info = {"manifest_sha256": KIT_MANIFEST_SHA, "files_verified": len(entries)}

    # --- status log gates -----------------------------------------------------
    import re
    log_lines = [l for l in (KIT_DIR / "output/status.log").read_text().splitlines() if l.strip()]
    if len(log_lines) != STATUS_LINES:
        fail(f"status log line count {len(log_lines)} != {STATUS_LINES}")
    pat = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z) (ab\d{3}) PASS (\d+),(\d+),(\d+)$")
    seen_ids, seen_ts = set(), []
    for line in log_lines:
        m = pat.match(line)
        if m is None:
            fail(f"status log line not a strict PASS verdict row: {line!r}")
        if m.group(3) != str(BUDGET) or m.group(4) != "2":
            fail(f"status log row not a LOSS verdict at budget {BUDGET}: {line!r}")
        kid = m.group(2)
        ts = m.group(1)
        if kid in seen_ids:
            fail(f"status log duplicate key row: {kid}")
        seen_ids.add(kid)
        seen_ts.append(ts)
        a = ADOPTED.get(kid)
        if a is None or int(m.group(5)) != a["nodes"]:
            fail(f"status log node count for {kid} != the adopted row pin: {line!r}")
    if seen_ids != set(ADOPTED_IDS):
        fail(f"status log key-id set {sorted(seen_ids)} != the adopted 16")
    if log_lines[-1] != STATUS_FINAL_ROW:
        fail(f"status log final row {log_lines[-1]!r} != pinned {STATUS_FINAL_ROW!r}")
    if min(seen_ts) != STATUS_TS_MIN or max(seen_ts) != STATUS_TS_MAX:
        fail(f"status log timestamp window {min(seen_ts)}..{max(seen_ts)} != pinned")
    status_log_info = {
        "lines": len(log_lines), "all_pass": True, "final_verdict_row": STATUS_FINAL_ROW,
        "ts_window": [STATUS_TS_MIN, STATUS_TS_MAX],
        "note": STATUS_LOG_NOTE,
    }

    # --- manifest gates --------------------------------------------------------
    manifest = json.loads(MANIFEST.read_text())
    if sha(MANIFEST) != MANIFEST_SHA:
        fail("manifest file sha drift (double-read)")
    if manifest["schema"] != "b29loss16-increments-manifest-v1":
        fail(f"manifest schema drift: {manifest['schema']}")
    rc = manifest["row_counts"]
    if not (rc["adopted_loss_rows"] == 16 and rc["wins"] == 0
            and rc["exhausted_excluded"] == 0 and rc["probed_rows"] == 16
            and rc["fragments_unprobed"] == 0 and rc["fileless_unprobed"] == 38):
        fail(f"manifest row_counts not the partially-probed 16-LOSS / 0-WIN / 0-EXHAUSTED / 38-fileless picture: {rc}")
    if manifest["loss_ids"] != ADOPTED_IDS:
        fail(f"manifest loss id list drift: {manifest['loss_ids']}")
    if (manifest["win_ids"] != [] or manifest["unadopted_win_ids"] != []
            or manifest["exhausted_excluded_ids"] != []):
        fail("manifest WIN / EXHAUSTED id lists must be empty (0 WIN, 0 EXHAUSTED rows)")
    if sorted(manifest["resolved_ids"]) != sorted(PROBED_IDS):
        fail(f"manifest resolved_ids != the 16 probed keys: {manifest['resolved_ids']}")
    if manifest["full_packet_eq_loss_only"] is not True or manifest["win_scenario_exists"] is not False:
        fail("manifest full==loss-only and no-WIN-scenario flags not asserted")
    if manifest["sha256"]["loss"] != INCR_SHA:
        fail("manifest loss sha does not match the pinned increment")
    if manifest["merger_sha256"] != MERGER_SHA:
        fail("manifest merger pin drift (the pinned fail-closed union merger)")
    if (manifest["base_cache_sha256"] != BASE_CACHE_SHA
            or manifest["base_cache_rows"] != 6301
            or manifest["base_cache_absent_hits_for_emitted"] != 0
            or manifest["quarantine_hits"] != 0):
        fail("manifest BASE-cache bookkeeping drift (6,301 rows 854800f3..., no absent hits)")
    if manifest["unadopted_win_rows"] != [] or manifest["exhausted_rows"] != []:
        fail("manifest unadopted WIN / EXHAUSTED row lists must be empty")
    if len(manifest["batches"]) != 1:
        fail("manifest batches != exactly [batch-29]")
    mb = manifest["batches"][0]
    if (mb["batch"] != 29 or mb["class_index"] != B29_CLASS or mb["keys_total"] != 54):
        fail("manifest batch-29 identity drift")
    if (mb["adopted_loss_ids"] != ADOPTED_IDS or mb["already_adopted_ids"] != []
            or mb["unadopted_win_ids"] != [] or mb["exhausted_excluded_ids"] != []
            or mb["fragment_ids"] != []):
        fail("manifest batch-29 adopted/unadopted/fragment id lists drift")
    if mb["probed_ids"] != PROBED_IDS:
        fail("manifest batch-29 probed ids != the 16 adopted keys")
    if (mb["fileless_unprobed_count"] != 38 or sorted(mb["fileless_unprobed_ids"]) != FILELESS_IDS):
        fail("manifest batch-29 fileless 38 ids drift")
    if mb["input_sha256"] != B29_KEYS_SHA:
        fail("manifest batch-29 input sha drift")
    if (mb["status_log_sha256"] != STATUS_LOG_SHA or mb["status_log_lines"] != STATUS_LINES
            or mb["status_log_final_line"] != STATUS_FINAL_ROW):
        fail("manifest batch-29 status-log bookkeeping drift")
    if (mb["kit_integrity"]["manifest_sha256"] != KIT_MANIFEST_SHA
            or mb["kit_integrity"]["files_verified"] != KIT_FILES):
        fail("manifest batch-29 kit integrity drift")
    want_vg = {f"{p}.takeover-host.out": g["takeover_host"] for p, g in VAL_GATES.items()}
    if mb["takeover_val_gate_files"] != want_vg:
        fail("manifest takeover val-gate file sha block drift")
    if mb["val_gate_double_host_node_exact"] is not True:
        fail("manifest val-gate double-host node-exact flag not asserted")
    if (mb["total_nodes_pass_one"] != mb["total_nodes_pass_two"]
            or mb["total_nodes_pass_one"] != ADOPTED_TOTAL_NODES):
        fail(f"manifest batch-29 adopted-row node total drift ({ADOPTED_TOTAL_NODES} expected)")
    if mb["stop_rule"] != STOP_RULE:
        fail("manifest batch-29 stop rule drift")
    if mb["fragment_state"] != {}:
        fail("manifest batch-29 fragment_state must be empty (0 fragments)")

    # --- val-gate triple-host gates -----------------------------------------
    for pat_name, want in VAL_GATE_PATTERNS.items():
        g = VAL_GATES[pat_name]
        molecule = (g["lo"], g["hi"])
        if sha(KIT_DIR / f"val-gate/{pat_name}.input.csv") != g["input_csv"]:
            fail(f"val-gate {pat_name} input.csv sha drift")
        rows = {}
        for host, key in (("published-baseline", "published_baseline"),
                          ("batch29-host", "batch29_host"),
                          ("takeover-host", "takeover_host")):
            p = KIT_DIR / f"val-gate/{pat_name}.{host}.out"
            if sha(p) != g[key]:
                fail(f"val-gate {pat_name} {host} sha drift")
            rows[host] = parse_valgate_out(p)
        base = rows["published-baseline"]
        for host in ("batch29-host", "takeover-host"):
            if rows[host] != base:
                fail(f"val-gate {pat_name} {host} replay row {rows[host]} != published-baseline {base} "
                     "(double-host node-exact gate)")
        stones, legal, is_or, budget, result, nodes, klo, khi = base
        if (stones, is_or) != (5, 0) or (klo, khi) != molecule or legal != g["legal"]:
            fail(f"val-gate {pat_name} replay key/stones/and-or gate drift: {base}")
        if (budget, result, nodes) != want:
            fail(f"val-gate {pat_name} budget/result/nodes {want} gate drift: {base}")
    val_gate_info = {
        "patterns": {p: {"molecule": [g["lo"], g["hi"]], "legal": g["legal"],
                         "budget": VAL_GATE_PATTERNS[p][0], "result": VAL_GATE_PATTERNS[p][1],
                         "nodes": VAL_GATE_PATTERNS[p][2],
                         "input_csv_sha256": g["input_csv"],
                         "published_baseline_sha256": g["published_baseline"],
                         "batch29_host_sha256": g["batch29_host"],
                         "takeover_host_sha256": g["takeover_host"]} for p, g in VAL_GATES.items()},
        "double_host_node_exact": "4/4 patterns: published-baseline == batch29-host == takeover-host "
                                  "on the full replay row modulo wall time",
    }

    # --- graph + update8 ------------------------------------------------------
    sys.path.insert(0, str(BOARD_SOURCE.parent))
    sys.path.insert(0, str(POLICY.parent))
    from independent import Board
    from s5_evidence_policy import quarantined_cache_keys, is_canonical_safe_s5_key

    quarantined = quarantined_cache_keys()
    board = Board(11)

    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        gph = json.load(stream)
    s4_masks, s4_status, s4_cost = gph["s4_masks"], gph["s4_status"], gph["s4_cost"]
    roots = gph["roots"]
    s5_masks = gph["s5_masks"]
    mask_to_index = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}

    update8 = json.loads(UPDATE8.read_text(encoding="utf-8"))
    if update8["schema"] != "n11-night-repaired-joint-plan-update8-v1":
        fail("update8 schema drift")
    if update8["union_size"] != UNIVERSE_SIZE or len(update8["required_new_s5"]) != UNIVERSE_SIZE:
        fail("update8 baseline drift")
    if not update8["verification"]["passed"]:
        fail("update8 verification flag not passed")
    receipt_verdicts = {int(k): int(v) for k, v in update8["resolved_s5_verdicts"].items()}
    if len(receipt_verdicts) != RECEIPT_COUNT:
        fail(f"receipt verdict count {len(receipt_verdicts)} != {RECEIPT_COUNT}")

    # --- batch keys against the pinned graph ----------------------------------
    bk, groups_served = load_keys(KIT_DIR, B29_CLASS)
    if [int(x) for x in bk["class_mask"]] != list(s4_masks[B29_CLASS]):
        fail("batch-keys class_mask != graph mask of class 2251")
    if len(bk["keys"]) != 54:
        fail(f"class 2251 batch-keys count {len(bk['keys'])} != 54")
    batch_keys = {}
    for k in bk["keys"]:
        kid = k["key_id"]
        lo, hi, s5i = int(k["lo"]), int(k["hi"]), int(k["s5_index"])
        if mask_to_index.get((lo, hi)) != s5i:
            fail(f"{kid} (lo,hi) does not map to its published s5 index {s5i}")
        if (lo, hi) in quarantined or not is_canonical_safe_s5_key((lo, hi)):
            fail(f"{kid} noncanonical or quarantined key")
        batch_keys[kid] = (lo, hi, s5i, int(k["membership_class_count"]), int(k["legal"]))
    if len(set(v[2] for v in batch_keys.values())) != len(batch_keys):
        fail("batch keys collide on s5 indices")
    for kid, (lo, hi, s5i, _m, _lg) in batch_keys.items():
        if s5i in receipt_verdicts:
            fail(f"{kid} already resolved by the update8 receipt")
    for pat_name, g in VAL_GATES.items():
        molecule = (g["lo"], g["hi"])
        if molecule in batch_keys or molecule in quarantined \
                or not is_canonical_safe_s5_key(molecule):
            fail(f"val-gate molecule {pat_name} must be canonical-safe and disjoint from the batch")

    # --- independent two-pass raw re-verification of the 16 probed keys -------
    adopted_nodes_sum = 0
    for kid, (lo, hi, s5i, _m, bk_legal) in sorted(batch_keys.items()):
        if kid not in PROBED_IDS:
            continue
        rows_raw = []
        for tag in ("p1", "p2"):
            rows_raw.append(parse_raw(KIT_DIR / f"output/raw/{kid}.{tag}.out", tag, kid))
        p1, p2 = rows_raw
        if p1 != p2:
            fail(f"{kid} two-pass mismatch (node-exact gate): {p1} vs {p2}")
        stones, legal, is_or, budget, result, nodes, klo, khi = p1
        if stones != 5 or is_or != 0 or budget != BUDGET:
            fail(f"{kid} raw depth/budget drift: {p1}")
        if (klo, khi) != (lo, hi) or legal != bk_legal:
            fail(f"{kid} raw key/legal != batch-keys")
        a = ADOPTED[kid]
        if result != 2 or nodes != a["nodes"] or legal != a["legal"] or s5i != a["s5"]:
            fail(f"{kid} raw record != the published adopted LOSS row: {p1}")
        adopted_nodes_sum += nodes
    if adopted_nodes_sum != ADOPTED_TOTAL_NODES:
        fail(f"adopted raw node sum {adopted_nodes_sum} != pinned total {ADOPTED_TOTAL_NODES}")
    # raw inventory gate: exactly the 32 probed raw files
    raw_dir = KIT_DIR / "output/raw"
    raws = sorted(p.name for p in raw_dir.iterdir() if p.is_file())
    expected_raws = sorted(f"{kid}.{tag}.out" for kid in PROBED_IDS for tag in ("p1", "p2"))
    if raws != expected_raws:
        fail(f"raw inventory drift: {len(raws)} files, expected exactly the 32 probed files")
    for kid in FILELESS_IDS:
        for tag in ("p1", "p2"):
            if (raw_dir / f"{kid}.{tag}.out").exists():
                fail(f"fileless key {kid} unexpectedly has a raw file")

    # --- increment gates -----------------------------------------------------
    incr = read_cache(INCR_CACHE)
    if len(incr) != ADOPTED_ROWS:
        fail(f"increment row count {len(incr)} != {ADOPTED_ROWS}")
    if any(v[0] != 2 for v in incr.values()):
        fail("increment contains a non-LOSS verdict")
    if set(incr) != {ADOPTED[k]["key"] for k in ADOPTED_IDS}:
        fail("increment keys != exactly the 16 adopted LOSS keys")
    for kid in ADOPTED_IDS:
        a = ADOPTED[kid]
        row = incr.get(tuple(a["key"]))
        if row is None or row != (2, a["nodes"]):
            fail(f"increment row for {kid} != the adopted verdict: {row}")
    for kid in FILELESS_IDS:
        lo, hi, _s5i, _m, _lg = batch_keys[kid]
        if (lo, hi) in incr:
            fail(f"fileless key {kid} leaked into the increment (no raw evidence)")

    base_cache = read_cache(BASE_CACHE)
    scen_cache = read_cache(SCEN_CACHE)
    for kid in ADOPTED_IDS:
        lo, hi, _s5i, _m, _lg = batch_keys[kid]
        if (lo, hi) in base_cache:
            fail(f"{kid} already present in the BASE cache (not a fresh increment)")
        if tuple(ADOPTED[kid]["key"]) != (lo, hi):
            fail(f"adopted row pin key for {kid} != batch-keys")
    if len(scen_cache) != len(base_cache) + ADOPTED_ROWS:
        fail(f"scenario cache row count != BASE + {ADOPTED_ROWS}")
    for key, (v, _n) in incr.items():
        srow = scen_cache.get(key)
        if srow is None or srow[0] != v:
            fail(f"scenario cache does not adopt increment row {key}")
    for key in scen_cache:
        if key not in base_cache and key not in incr:
            fail(f"scenario cache key outside BASE+increment: {key}")
    for key, (v, _n) in scen_cache.items():
        if key in base_cache and base_cache[key][0] != v:
            fail(f"scenario cache verdict drift on shared key {key}")
    base_votes = Counter(v for v, _ in base_cache.values())
    scen_votes = Counter(v for v, _ in scen_cache.values())
    if base_votes.get(1, 0) != 158 or base_votes.get(2, 0) != 6143:
        fail(f"BASE cache verdict counts not 158 WIN / 6143 LOSS: {dict(sorted(base_votes.items()))}")
    if scen_votes.get(1, 0) != 158 or scen_votes.get(2, 0) != 6159:
        fail(f"scenario cache verdict counts not 158 WIN / 6159 LOSS: {dict(sorted(scen_votes.items()))}")
    for kid in FILELESS_IDS:
        lo, hi, _s5i, _m, _lg = batch_keys[kid]
        if (lo, hi) in base_cache:
            fail(f"fileless key {kid} unexpectedly present in BASE")
        if (lo, hi) in scen_cache:
            fail(f"fileless key {kid} reached the scenario canonical cache (fileless UNPROBED gate)")

    # --- graph holders of the adopted keys -----------------------------------
    holders = {}
    for kid in ADOPTED_IDS:
        lo, hi, s5i, mcnt, _lg = batch_keys[kid]
        hs = sorted(i for i, c in enumerate(s4_cost) if s5i in c)
        if B29_CLASS not in hs:
            fail(f"{kid} own batch class {B29_CLASS} not among its graph holders {hs}")
        if len(hs) != mcnt or mcnt != MEMBERSHIP_EXPECT[kid]:
            fail(f"{kid} graph holder count {len(hs)} != batch-keys membership "
                 f"{mcnt} != pinned {MEMBERSHIP_EXPECT[kid]}")
        for i in hs:
            if s4_status[i] not in (-1, 0, 1):
                fail(f"{kid} holder {i} unexpected graph status {s4_status[i]}")
        holders[kid] = hs
    holder_union = sorted(set().union(*[set(h) for h in holders.values()]))
    if len(holder_union) != HOLDER_UNION_SIZE:
        fail(f"holder union {len(holder_union)} != pinned {HOLDER_UNION_SIZE}")
    member_loss_counts = Counter()
    for hs in holders.values():
        for i in hs:
            member_loss_counts[i] += 1
    for c, want_cnt in EXPECTED_MEMBER_LOSS_COUNTS.items():
        if member_loss_counts[c] != want_cnt:
            fail(f"member loss count for {c} != pinned {want_cnt}")
    for c, cnt in member_loss_counts.items():
        if c not in EXPECTED_MEMBER_LOSS_COUNTS and cnt != 1:
            fail(f"holder {c} unexpectedly cited by {cnt} adopted keys (pin: 1)")
    incr_index = {}
    for kid in ADOPTED_IDS:
        incr_index[ADOPTED[kid]["s5"]] = tuple(ADOPTED[kid]["key"])
    if set(incr_index) != set(NEWLY_RESOLVED_S5) and NEWLY_RESOLVED_S5 != []:
        fail("adopted s5 index set != the pinned newly-resolved set")
    adopted_s5_set = set(incr_index)
    if adopted_s5_set & set(update8["required_new_s5"]):
        fail("adopted s5 index intersects the update8 baseline requirement "
             "(contradicts the machine-observed unmoved update8 refresh)")

    # --- faithful re-execution of the published refresh class pass -----------
    def refresh_statuses(cache):
        index_verdict = {}
        in_universe = 0
        for (lo, hi), (verdict, _nodes) in cache.items():
            i = mask_to_index.get((lo, hi))
            if i is None:
                continue
            in_universe += 1
            index_verdict[i] = verdict
        for i, v in receipt_verdicts.items():
            if not (0 <= i < len(s5_masks)):
                fail(f"receipt index outside universe: {i}")
            prior = index_verdict.get(i)
            if prior is not None and prior != v:
                fail(f"receipt/cache conflict at index {i}")
            index_verdict[i] = v
        for key in cache:
            if key in quarantined:
                fail(f"quarantined key inside cache: {key}")
            if not is_canonical_safe_s5_key(key):
                fail(f"noncanonical cache key {key}")
        LOSS, UNKNOWN, EXCLUDED = 0, 1, -1
        st, unknown_now = {}, {}
        for i in range(len(s4_masks)):
            base = s4_status[i]
            cost = s4_cost[i]
            if base == EXCLUDED:
                st[i] = "excluded"
                unknown_now[i] = []
                continue
            if base not in (LOSS, UNKNOWN):
                fail(f"unexpected graph base status {base} at class {i}")
            unknown, win_hit = [], False
            for j in cost:
                v = index_verdict.get(j)
                if v == 1:
                    win_hit = True
                elif v is None:
                    unknown.append(j)
            unknown_now[i] = unknown
            if base == UNKNOWN:
                st[i] = "excluded_now" if win_hit else ("free_now" if not unknown else "unknown")
            else:
                st[i] = "excluded_now" if win_hit else "free_now"
        # Board fail-closed child verification of every free candidate
        for i, s in list(st.items()):
            if s != "free_now":
                continue
            lo, hi = s4_masks[i]
            if not is_canonical_safe_s5_key((lo, hi)):
                try:
                    board.legal(lo | (hi << 64))
                except ValueError:
                    st[i] = "free_now_unverified"
                    continue
            for child in board.children(lo | (hi << 64)):
                key = (child & ((1 << 64) - 1), child >> 64)
                have = cache.get(key)
                if have is None:
                    ci = mask_to_index.get(key)
                    rv = receipt_verdicts.get(ci) if ci is not None else None
                    have = (rv, 0) if rv is not None else None
                if have is None or have[0] != 2:
                    st[i] = "free_now_unverified"
                    break
        return st, unknown_now, index_verdict, in_universe

    base_st, base_unknown, base_iv, base_in_univ = refresh_statuses(base_cache)
    scen_st, scen_unknown, _scen_iv, scen_in_univ = refresh_statuses(scen_cache)

    base_summary = json.loads((BASE_DIR / "refresh-summary.json").read_text())
    scen_summary = json.loads((SCEN_OUT / "refresh-summary.json").read_text())
    published = {"BASE": base_summary, SCENARIO: scen_summary}

    # publish-side recompute equality gates
    for name, st in (("BASE", base_st), (SCENARIO, scen_st)):
        counts = Counter(st.values())
        pub = published[name]["class_status_counts"]
        for k in ("excluded", "excluded_now", "free_now", "unknown"):
            if counts.get(k, 0) != pub.get(k, 0):
                fail(f"{name}: recomputed {k} {counts.get(k, 0)} != published {pub.get(k, 0)}")
        if counts.get("free_now_unverified", 0) != 0:
            fail(f"{name}: {counts.get('free_now_unverified', 0)} unverified free candidates")
        pub_in = published[name]["inputs"]
        iv = base_iv if name == "BASE" else _scen_iv
        iu = base_in_univ if name == "BASE" else scen_in_univ
        if pub_in["known_universe_indices"] != len(iv):
            fail(f"{name}: recomputed known universe {len(iv)} != published {pub_in['known_universe_indices']}")
        if pub_in["cache_rows_in_universe"] != iu:
            fail(f"{name}: recomputed cache rows in universe {iu} != published {pub_in['cache_rows_in_universe']}")
    if base_summary["inputs"]["cache_rows"] != 6301 or scen_summary["inputs"]["cache_rows"] != 6317:
        fail("published cache_rows not 6301 -> 6317")

    # --- global status-transition gate ----------------------------------------
    transitions = Counter()
    for i in range(len(s4_masks)):
        b, s = base_st[i], scen_st[i]
        transitions[f"{b}->{s}"] += 1
        if s not in ALLOWED_TRANSITIONS.get(b, []):
            fail(f"class {i} forbidden transition {b} -> {s}")
    if dict(sorted(transitions.items())) != STATUS_TRANSITIONS_PIN:
        fail(f"status transitions {dict(sorted(transitions.items()))} != pinned {STATUS_TRANSITIONS_PIN}")

    # --- excluded_now flips must be empty for a zero-WIN increment -----------
    base_excluded_now = {i for i, s in base_st.items() if s == "excluded_now"}
    flips = sorted(i for i, s in scen_st.items()
                   if s == "excluded_now" and i not in base_excluded_now)
    if flips:
        fail(f"excluded_now flips {flips} must be EMPTY for a zero-WIN increment")
    flipped_out = sorted(i for i, s in scen_st.items()
                         if s != "excluded_now" and i in base_excluded_now)
    if flipped_out:
        fail(f"excluded_now regressions {flipped_out} must be EMPTY")

    # --- newly free classes: all BASE-unknown children resolved by the incr --
    new_free = sorted(i for i, s in scen_st.items() if s == "free_now" and base_st[i] != "free_now")
    expected_new_free = sorted(i for i, unk in base_unknown.items()
                               if base_st[i] == "unknown" and unk
                               and all(j in incr_index for j in unk))
    if new_free != expected_new_free:
        fail(f"newly free classes {new_free} != fully-resolved expectation {expected_new_free}")

    # --- per-class arithmetic gates -------------------------------------------
    cls = B29_CLASS
    if cls in new_free:
        fail(f"class {cls} must NOT free: its 38 fileless children stay UNPROBED, so "
             "unknown cost children remain and the class stays unknown")
    if scen_st[cls] != "unknown":
        fail(f"class {cls} scenario status {scen_st[cls]} != unknown (fileless children remain)")
    basec = sorted(base_unknown[cls])
    if len(basec) != 54:
        fail(f"class {cls} BASE-unknown cost children {len(basec)} != 54 (nothing adopted before)")
    own_class_incr = sorted(j for j in incr_index if j in s4_cost[cls])
    if not set(own_class_incr) <= set(basec):
        fail(f"class {cls}: increment s5 indices not all BASE-unknown cost children of the class")
    if len(own_class_incr) != 16:
        fail(f"class {cls}: own increment membership {len(own_class_incr)} != 16")
    leftover = sorted(set(basec) - set(own_class_incr))
    if len(leftover) != 38:
        fail(f"class {cls} leftover BASE-unknown children {len(leftover)} != 38")
    if sorted(scen_unknown[cls]) != leftover:
        fail(f"class {cls} scenario-unknown children != leftover arithmetic")
    batch_s5 = {v[2] for v in batch_keys.values()}
    if batch_s5 != set(basec):
        fail(f"class {cls}: batch key set != the 54 BASE-unknown cost children (no pre-adopted key)")
    fileless_s5 = sorted(batch_keys[k][2] for k in FILELESS_IDS)
    if fileless_s5 != leftover:
        fail(f"class {cls}: leftover 38 != exactly the 38 fileless-key s5 indices")
    class_rows = {str(cls): {
        "class_index": cls, "batch": 29,
        "base_unknown_children": len(base_unknown[cls]),
        "adopted_by_increment": len(own_class_incr),
        "leftover_unknown_children": len(leftover),
        "scenario_unknown_children": len(scen_unknown[cls]),
        "scenario_status": scen_st[cls],
        "leftover_is_exactly_fileless_keys": True,
    }}

    # --- holder-class table with own-membership arithmetic gate ---------------
    holder_rows = {}
    for c in holder_union:
        own = sorted(j for j in incr_index if j in s4_cost[c])
        row = {
            "base_status": base_st[c],
            "base_unknown_now": len(base_unknown[c]),
            "own_membership_in_increment": len(own),
            "scenario_status": scen_st[c],
            "scenario_unknown_now": len(scen_unknown[c]),
        }
        if base_st[c] == "excluded":
            if len(scen_unknown[c]) != 0:
                fail(f"holder class {c} excluded at BASE but scenario unknown_now != 0")
        elif len(base_unknown[c]) - len(own) != len(scen_unknown[c]):
            fail(f"holder class {c}: scenario unknown_now {len(scen_unknown[c])} != "
                 f"BASE {len(base_unknown[c])} - own {len(own)}")
        if c == cls and len(own) != 16:
            fail(f"holder class {cls} must hold exactly the 16 adopted memberships")
        holder_rows[str(c)] = row

    # --- published metric table and pinned deltas -----------------------------
    def metric_set(pub):
        csc = pub["class_status_counts"]
        fr = pub["frozen_update8_refresh"]
        return {
            "excluded_now_classes": csc.get("excluded_now", 0),
            "free_now_classes": csc.get("free_now", 0),
            "unknown_classes": csc.get("unknown", 0),
            "update8_remaining_now": fr["remaining_now"],
            "update8_resolved_count": fr["resolved_count"],
            "update8_win_hit_groups": len(fr["win_hit_groups"]),
            "update8_groups_free_now": fr["groups_free_now"],
            "joint_greedy_unique_groups": pub["joint_greedy"]["unique_groups"],
            "joint_greedy_union_size": pub["joint_greedy"]["greedy_union_size"],
            "probe_worklist_total": pub["worklist_total"],
            "group_best_options_nonfree": pub["group_best_options_nonfree"],
            "closure_classes_count": pub["closure_classes_count"],
        }

    flat = {"BASE": metric_set(base_summary), SCENARIO: metric_set(scen_summary)}
    metrics = {}
    for k in flat["BASE"]:
        metrics[k] = {"base": flat["BASE"][k], "scenario": flat[SCENARIO][k],
                      "delta": flat[SCENARIO][k] - flat["BASE"][k]}
    for k, (want_base, want_scen) in METRICS_PIN.items():
        if metrics[k]["base"] != want_base or metrics[k]["scenario"] != want_scen:
            fail(f"metric {k} {metrics[k]['base']}->{metrics[k]['scenario']} != "
                 f"declared pin {want_base}->{want_scen}")
    if metrics["free_now_classes"]["delta"] != 0:
        fail("free_now class count must not change in a loss-only non-closing adoption")
    if metrics["update8_resolved_count"]["delta"] != 0:
        fail("update8 resolved-count delta != 0 (declared machine-observed: the 16 "
             "adopted keys are not update8 baseline requirements)")
    if metrics["update8_remaining_now"]["delta"] != 0:
        fail("update8 remaining delta != 0")
    if metrics["probe_worklist_total"]["delta"] != -19:
        fail("probe worklist delta != -19 (declared machine-observed)")
    if metrics["joint_greedy_union_size"]["delta"] != -2619:
        fail("joint greedy union delta != -2619 (declared machine-observed)")
    if metrics["closure_classes_count"]["delta"] != 0:
        fail("closure classes count delta != 0")
    for k in ("update8_win_hit_groups", "update8_groups_free_now",
              "joint_greedy_unique_groups", "group_best_options_nonfree"):
        if metrics[k]["delta"] != 0:
            fail(f"metric {k} must stay unchanged for a zero-WIN adoption")

    # --- update8 resolved-requirement delta, gated to the increment ----------
    base_resolved = set(base_summary["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    scen_resolved = set(scen_summary["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    lost = sorted(base_resolved - scen_resolved)
    if lost:
        fail(f"update8 resolutions lost: {lost}")
    newly_resolved = sorted(scen_resolved - base_resolved)
    if newly_resolved != NEWLY_RESOLVED_S5:
        fail(f"newly resolved s5 {newly_resolved} != the pinned empty set "
             "(the adopted keys are not update8 baseline requirements)")

    # --- per-root coverage recompute + published csv gates --------------------
    def per_root_free_thirds(st):
        per_root = {}
        per_third = {}
        for r in roots:
            free = 0
            for third in r["thirds"]:
                opts = third["options"]
                is_free = bool(opts) and any(st.get(o) == "free_now" for o in opts)
                per_third[(r["origin_first"], third["third"])] = is_free
                if is_free:
                    free += 1
            per_root[r["origin_first"]] = (r["role"], len(r["thirds"]), free)
        return per_root, per_third

    base_by_root, base_by_third = per_root_free_thirds(base_st)
    scen_by_root, scen_by_third = per_root_free_thirds(scen_st)

    def load_prc(path):
        rows = {}
        with Path(path).open() as fh:
            for r in csv.DictReader(fh):
                ig = r["individual_greedy_union"]
                rows[(r["role"], int(r["first"]))] = (
                    int(r["thirds"]), int(r["free_now"]), int(r["uncovered"]),
                    int(ig) if ig else None)
        return rows

    base_prc = load_prc(BASE_DIR / "per-root-coverage.csv")
    scen_prc = load_prc(SCEN_OUT / "per-root-coverage.csv")
    if set(base_prc) != set(scen_prc):
        fail("per-root row set changed between BASE and scenario")
    if len(base_prc) != len(roots):
        fail(f"per-root row count {len(base_prc)} != graph roots {len(roots)}")
    for prc, by_root, by_third, name in ((base_prc, base_by_root, base_by_third, "BASE"),
                                         (scen_prc, scen_by_root, scen_by_third, SCENARIO)):
        if len(by_third) != sum(len(r["thirds"]) for r in roots):
            fail(f"{name}: per-third recount mismatch")
        for (role, first), (thirds, free, uncov, _ig) in prc.items():
            rr, rt, rf = by_root[first]
            if rr != role or rt != thirds or rf != free:
                fail(f"{name}: recomputed root {first} ({rr},{rt},{rf}) != "
                     f"published ({role},{thirds},{free})")
            if free + uncov != thirds:
                fail(f"{name}: root {first} free+uncovered != thirds")

    for name, pub in published.items():
        r0 = pub["roots"][0]
        if (r0["role"], r0["origin_first"], r0["thirds"], r0["free_thirds_now"], r0["uncovered"]) \
                != ("known-loss-baseline", 27, 119, 119, 0):
            fail(f"{name}: roots[0] not the 119/119 known-loss baseline: {r0}")
    for prc in (base_prc, scen_prc):
        if prc[("known-loss-baseline", 27)][:3] != (119, 119, 0):
            fail("baseline per-root row not 119/119")

    changed_rows = {}
    greedy_moved_rows = {}
    for (role, first), (thirds, bfree, buncov, big) in base_prc.items():
        sthirds, sfree, suncov, sig = scen_prc[(role, first)]
        if big != sig:
            greedy_moved_rows["|".join((role, str(first)))] = {"base": big, "scenario": sig}
        if (bfree, buncov) == (sfree, suncov):
            continue
        if sfree < bfree or suncov > buncov:
            fail(f"root {first}: coverage regressed ({bfree},{buncov})->({sfree},{suncov})")
        if sfree + suncov != thirds or bfree + buncov != thirds:
            fail(f"root {first}: free+uncovered != thirds after change")
        changed_rows["|".join((role, str(first)))] = {
            "base": {"free_now": bfree, "uncovered": buncov},
            "scenario": {"free_now": sfree, "uncovered": suncov},
        }
    # individual greedy union movers: exactly roots 16 / 37 with pinned values
    ig_movers_by_first = {}
    for key, row in greedy_moved_rows.items():
        first = key.split("|")[1]
        ig_movers_by_first[first] = (row["base"], row["scenario"])
    if ig_movers_by_first != PRG_MOVERS_PIN:
        fail(f"individual greedy union movers {ig_movers_by_first} != pinned "
             f"{PRG_MOVERS_PIN} (per-root coverage free/uncovered must be unchanged)")
    if changed_rows:
        fail(f"per-root free coverage changed despite no newly free class: {changed_rows}")

    # --- per-root greedy movers (measured bookkeeping) ------------------------
    prg_base = base_summary["per_root_greedy"]
    prg_scen = scen_summary["per_root_greedy"]
    if set(prg_base) != set(prg_scen):
        fail("per-root greedy root set changed")
    per_root_greedy_movers = {}
    for first in sorted(prg_base, key=lambda x: int(x)):
        b, s = prg_base[first], prg_scen[first]
        row = {"base_greedy_union_size": b["greedy_union_size"],
               "scenario_greedy_union_size": s["greedy_union_size"],
               "delta": s["greedy_union_size"] - b["greedy_union_size"],
               "base_free_thirds": b["free_thirds"],
               "scenario_free_thirds": s["free_thirds"],
               "base_uncovered_thirds": b["uncovered_thirds"],
               "scenario_uncovered_thirds": s["uncovered_thirds"]}
        if row["delta"] > 0:
            fail(f"per-root greedy delta for root {first} must be <= 0: {row}")
        if row["delta"] != 0 and first not in PRG_MOVERS_PIN:
            fail(f"per-root greedy mover root {first} not in the declared mover set")
        if first in PRG_MOVERS_PIN:
            if (row["base_greedy_union_size"], row["scenario_greedy_union_size"]) != PRG_MOVERS_PIN[first]:
                fail(f"per-root greedy values for root {first} {row} != declared pin")
            if row["base_free_thirds"] != row["scenario_free_thirds"]:
                fail(f"per-root greedy free thirds changed for root {first} (no class freed)")
        per_root_greedy_movers[first] = row
    roots_summary_moved = {}
    base_roots_rows = {r["origin_first"]: r for r in base_summary["roots"]}
    for r in scen_summary["roots"]:
        b = base_roots_rows[r["origin_first"]]
        if (b["free_thirds_now"], b["uncovered"]) != (r["free_thirds_now"], r["uncovered"]):
            roots_summary_moved[str(r["origin_first"])] = {
                "base": [b["free_thirds_now"], b["uncovered"]],
                "scenario": [r["free_thirds_now"], r["uncovered"]],
            }
    if roots_summary_moved:
        fail(f"roots summary moved despite no newly free class: {roots_summary_moved}")

    # --- probe worklist gates --------------------------------------------------
    def load_worklist(path):
        with Path(path).open() as fh:
            return list(csv.DictReader(fh))

    base_wl = load_worklist(BASE_DIR / "probe-worklist.csv")
    scen_wl = load_worklist(SCEN_OUT / "probe-worklist.csv")
    if len(base_wl) != metrics["probe_worklist_total"]["base"] \
            or len(scen_wl) != metrics["probe_worklist_total"]["scenario"]:
        fail("worklist row counts != published metrics")
    base_2251 = [r for r in base_wl if r["serving_class"] == str(B29_CLASS)]
    scen_2251 = [r for r in scen_wl if r["serving_class"] == str(B29_CLASS)]
    if len(base_2251) != 54 or len(scen_2251) != 38:
        fail(f"class 2251 serving rows {len(base_2251)}->{len(scen_2251)} != 54->38")
    adopted_lohi = {tuple(ADOPTED[k]["key"]) for k in ADOPTED_IDS}
    for r in scen_wl:
        if (int(r["lo"]), int(r["hi"])) in adopted_lohi:
            fail(f"adopted key still in the scenario worklist at s5 {r['s5_index']}")
    scen_2251_s5 = sorted(int(r["s5_index"]) for r in scen_2251)
    if scen_2251_s5 != sorted(fileless_s5):
        fail("the 38 scenario serving rows of class 2251 != the fileless s5 indices")
    base_2251_s5 = sorted(int(r["s5_index"]) for r in base_2251)
    if base_2251_s5 != sorted(batch_s5):
        fail("the 54 BASE serving rows of class 2251 != the batch s5 indices")
    worklist_info = {
        "base_total": len(base_wl), "scenario_total": len(scen_wl),
        "class_2251_serving_rows": [len(base_2251), len(scen_2251)],
        "adopted_keys_absent_from_scenario_worklist": True,
    }

    # --- closure-candidate table observations ---------------------------------
    def load_closure(path):
        with Path(path).open() as fh:
            return list(csv.DictReader(fh))

    base_cc = load_closure(BASE_DIR / "closure-classes.csv")
    scen_cc = load_closure(SCEN_OUT / "closure-classes.csv")
    closure_rows = {
        "scenario_first_row": scen_cc[0] if scen_cc else None,
        "counts": {"base": len(base_cc), "scenario": len(scen_cc)},
        "classes": {},
        "changed_unknown": {},
        "stable_unknown_rank_churn": {
            "count": STABLE_UNKNOWN_RANK_CHURN_COUNT,
            "status_distribution": dict(sorted(CHURN_STABLE_STATUS_DIST.items())),
            "gate": ("every churned class with stable unknown_now is pure ranking "
                     "bookkeeping: recomputed status UNCHANGED between BASE and "
                     f"scenario ({CHURN_STABLE_STATUS_DIST}), none of them a "
                     "holder of the adopted keys"),
        },
        "anchors": {},
    }
    if (len(base_cc), len(scen_cc)) != CLOSURE_COUNTS:
        fail(f"closure table counts {(len(base_cc), len(scen_cc))} != pinned {CLOSURE_COUNTS}")
    b_full = {int(r["class_index"]): r for r in base_cc}
    s_full = {int(r["class_index"]): r for r in scen_cc}
    base_idx = set(b_full)
    scen_idx = set(s_full)

    # class 2251: unknown_now 54 -> 38 (rank 35 -> 4)
    cls_row_pin = CLASS_2251_CLOSURE_PIN
    if int(b_full[cls]["unknown_now"]) != cls_row_pin[0][1] or int(b_full[cls]["class_rank"]) != cls_row_pin[0][0]:
        fail(f"BASE closure row for class 2251 unexpected: {b_full[cls]}")
    if int(s_full[cls]["unknown_now"]) != cls_row_pin[1][1] or int(s_full[cls]["class_rank"]) != cls_row_pin[1][0]:
        fail(f"scenario closure row for class 2251 unexpected: {s_full[cls]}")
    closure_rows["classes"][str(cls)] = {
        "base_rank": cls_row_pin[0][0], "base_unknown_now": cls_row_pin[0][1],
        "scenario_rank": cls_row_pin[1][0], "scenario_unknown_now": cls_row_pin[1][1],
    }

    inter = base_idx & scen_idx
    changed_unknown = sorted(c for c in inter
                             if int(b_full[c]["unknown_now"]) != int(s_full[c]["unknown_now"]))
    if changed_unknown != sorted([cls] + list(CHANGED_UNKNOWN_CLOSURE_PIN)):
        fail(f"closure unknown_now changes {changed_unknown} != class 2251 + the pinned "
             f"holder classes {sorted(CHANGED_UNKNOWN_CLOSURE_PIN)}")
    for c in changed_unknown:
        own = sorted(j for j in incr_index if j in s4_cost[c])
        if c not in holder_union:
            fail(f"closure class {c} changed unknown_now but is not a holder of the "
                 "adopted keys")
        if int(b_full[c]["unknown_now"]) - len(own) != int(s_full[c]["unknown_now"]):
            fail(f"closure class {c} unknown_now arithmetic drift: "
                 f"{b_full[c]['unknown_now']} - {len(own)} != {s_full[c]['unknown_now']}")
        if int(s_full[c]["unknown_now"]) != len(scen_unknown[c]):
            fail(f"closure class {c} scenario row unknown_now != recomputed scen unknown")
        if c != cls:
            pin = CHANGED_UNKNOWN_CLOSURE_PIN[c]
            if (int(b_full[c]["class_rank"]), int(b_full[c]["unknown_now"])) != pin[0] \
                    or (int(s_full[c]["class_rank"]), int(s_full[c]["unknown_now"])) != pin[1]:
                fail(f"closure holder row for class {c} != declared pin {pin}")
        for col in ("class_lo", "class_hi", "first_group_first", "first_group_third",
                    "groups_served_count"):
            if b_full[c][col] != s_full[c][col]:
                fail(f"closure row for class {c} changed column {col} (must stay stable)")
        if base_st.get(c) != "unknown" or scen_st.get(c) != "unknown":
            fail(f"closure changed-unknown class {c} recomputed status drift")
        closure_rows["changed_unknown"][str(c)] = {
            "base": [int(b_full[c]["class_rank"]), int(b_full[c]["unknown_now"])],
            "scenario": [int(s_full[c]["class_rank"]), int(s_full[c]["unknown_now"])],
            "own_membership_in_increment": len(own),
        }

    stable_churn = sorted(c for c in inter if c not in changed_unknown
                          and int(b_full[c]["class_rank"]) != int(s_full[c]["class_rank"]))
    if len(stable_churn) != STABLE_UNKNOWN_RANK_CHURN_COUNT:
        fail(f"stable-unknown rank churn count {len(stable_churn)} != pinned "
             f"{STABLE_UNKNOWN_RANK_CHURN_COUNT}")
    holder_set = set(holder_union)
    churn_status_dist = Counter()
    for c in stable_churn:
        if base_st.get(c) != scen_st.get(c):
            fail(f"churned class {c} changed recomputed status "
                 f"{base_st.get(c)} -> {scen_st.get(c)} (churn must be pure ranking "
                 "bookkeeping with stable recomputed status)")
        if c in holder_set:
            fail(f"churned holder class {c} must change unknown_now, not just rank")
        churn_status_dist[f"{base_st.get(c)}"] += 1
    if dict(sorted(churn_status_dist.items())) != dict(sorted(CHURN_STABLE_STATUS_DIST.items())):
        fail(f"stable-unknown churn status distribution {dict(sorted(churn_status_dist.items()))} != "
             f"declared pin {dict(sorted(CHURN_STABLE_STATUS_DIST.items()))}")

    # untouched anchor classes: fully stable rows
    for anchor, pin in CLOSURE_ANCHORS_PIN.items():
        if (int(b_full[anchor]["class_rank"]), int(b_full[anchor]["unknown_now"])) != pin \
                or (int(s_full[anchor]["class_rank"]), int(s_full[anchor]["unknown_now"])) != pin:
            fail(f"anchor class {anchor} closure-row drift (must stay "
                 f"rank/unknown {pin} in both tables)")
        closure_rows["anchors"][str(anchor)] = {
            "base_rank": pin[0], "scenario_rank": pin[0], "unknown_now": pin[1],
        }

    left = sorted(base_idx - scen_idx)
    entered = sorted(scen_idx - base_idx)
    if left != sorted(CLOSURE_LEFT_PIN) or entered != sorted(CLOSURE_ENTERED_PIN):
        fail(f"closure table left {left} / entered {entered} != pinned "
             f"{sorted(CLOSURE_LEFT_PIN)} / {sorted(CLOSURE_ENTERED_PIN)}")
    for c in left:
        pin = CLOSURE_LEFT_PIN[c]
        if (int(b_full[c]["class_rank"]), int(b_full[c]["unknown_now"])) != pin:
            fail(f"left class {c} base row != declared pin {pin}")
        if base_st.get(c) != "unknown":
            fail(f"left class {c} must stay recomputed unknown")
        if int(b_full[c]["unknown_now"]) != len(base_unknown[c]):
            fail(f"left class {c} base row unknown != recomputed BASE unknown")
    for c in entered:
        pin = CLOSURE_ENTERED_PIN[c]
        if (int(s_full[c]["class_rank"]), int(s_full[c]["unknown_now"])) != pin:
            fail(f"entered class {c} scenario row != declared pin {pin}")
        if scen_st.get(c) != "unknown":
            fail(f"entered class {c} must be recomputed unknown (tie-swap churn)")
        if int(s_full[c]["unknown_now"]) != len(scen_unknown[c]):
            fail(f"entered class {c} scenario row unknown != recomputed scen unknown")
        if c not in holder_union and sum(1 for j in incr_index if j in s4_cost[c]) != 0:
            fail(f"entered non-holder class {c} unexpectedly holds an adopted s5 index")
    closure_rows["left_table_classes"] = [{"class_index": c,
                                           "base_row": list(CLOSURE_LEFT_PIN[c])} for c in left]
    closure_rows["entered_table_classes"] = [{"class_index": c,
                                              "scenario_row": list(CLOSURE_ENTERED_PIN[c])} for c in entered]
    closure_rows["churn_note"] = ("the left/entered pairs are tie-swap churn in the anchor "
                                 "candidate selection: 1945<->1044 (rank 461, unknown 97) and "
                                 "19645<->386 (rank 571/572 region, unknown 101) carry identical "
                                 "aggregate stats; machine-observed, every entered row equals its "
                                 "recomputed scenario unknown")

    # --- output ----------------------------------------------------------------
    out = {
        "schema": "n11-b29loss16-adoption-decomp-deltas-v1",
        "scenario": ("ADOPTED-CANONICAL = pre-adoption BASE (Part CO canonical state, "
                     "6,301 rows, 854800f3...) + the 16 fresh LOSS rows of batch-29 "
                     "(class 2251; ab001..ab016; nodes total 57,463,971); the batch is "
                     "PARTIALLY probed: 38 keys ab017..ab054 are fileless UNPROBED and "
                     "carry NO verdict; no WIN row and no EXHAUSTED row observed among "
                     "the probed keys; loss-only adoption on the probed set; class 2251 "
                     "does NOT free (38 leftover = exactly the fileless keys)"),
        "interpretation_guard": ("canonical 16-row adoption deltas: only the 16 fresh "
                                 "LOSS rows are consumed into the canonical cache via "
                                 "the fail-closed union merger; the 38 fileless keys are "
                                 "UNPROBED (no verdict claimed, no raw evidence); class "
                                 "2251 does NOT free in this adoption (rank 35 -> 4, "
                                 "unknown 54 -> 38); scheduling quantities are "
                                 "bookkeeping; every claim stays UNKNOWN; 11x11 empty "
                                 "board and all 19 roots stay UNKNOWN; nodes are "
                                 "bookkeeping"),
        "recompute_gates": ("class statuses with Board free-candidate child "
                            "verification, known-universe counts and per-root free "
                            "coverage were recomputed from graph + update8 + cache and "
                            "asserted equal to the published BASE (Part CO reaudit) and "
                            "scenario outputs before any delta was emitted"),
        "pins": {
            "increment_sha256": INCR_SHA,
            "manifest_sha256": MANIFEST_SHA,
            "scenario_cache_sha256": SCEN_CACHE_SHA,
            "base_cache_sha256": BASE_CACHE_SHA,
            "base_summary_sha256": BASE_SUMMARY_SHA,
            "scenario_summary_sha256": SCEN_SUMMARY_SHA,
            "base_closure_classes_sha256": BASE_CLOSURE_SHA,
            "base_per_root_coverage_sha256": BASE_PRC_SHA,
            "scenario_closure_classes_sha256": SCEN_CLOSURE_SHA,
            "scenario_per_root_coverage_sha256": SCEN_PRC_SHA,
            "scenario_probe_worklist_sha256": SCEN_WORKLIST_SHA,
            "batch29_keys_sha256": B29_KEYS_SHA,
            "status_log_sha256": STATUS_LOG_SHA,
            "kit_manifest_sha256": KIT_MANIFEST_SHA,
            "merge_audit_sha256": MERGE_AUDIT_SHA,
            "merger_sha256": MERGER_SHA,
        },
        "kit_integrity": kit_info,
        "status_log": status_log_info,
        "val_gate": val_gate_info,
        "batch_keys": {
            "count": len(batch_keys), "adopted_loss": 16, "unadopted_win": 0,
            "exhausted_excluded": 0, "fileless_unprobed": 38, "b29_class": B29_CLASS,
            "b29_keys": 54, "b29_probed": 16, "b29_fragments": 0,
            "b29_class_mask": list(s4_masks[B29_CLASS]),
            "b29_cost_children_total": len(s4_cost[B29_CLASS]),
            "b29_groups_served": [list(x) for x in groups_served],
        },
        "status_transitions": dict(sorted(transitions.items())),
        "excluded_now_flips": flips,
        "newly_free_now_classes": new_free,
        "newly_free_now_gate": ("the loss-only partial packet can only free classes whose "
                               "BASE-unknown children are ALL resolved by the "
                               "increment; machine-computed list is empty here; class "
                               "2251 does NOT free (its 38 fileless keys stay UNPROBED)"),
        "class_rows": class_rows,
        "adopted_rows": [
            {"key_id": kid, "s5_index": a["s5"], "key": [a["key"][0], a["key"][1]],
             "legal": a["legal"], "nodes": a["nodes"], "consumed": True,
             "note": ("two-pass node-exact LOSS row adopted into the canonical chain "
                      "via the pinned fail-closed merger 90711961003...; batch-29 "
                      "takeover drive-1 checkpoint 1/3")}
            for kid, a in ((k, ADOPTED[k]) for k in ADOPTED_IDS)],
        "fileless_unprobed_rows": [
            {"key_id": kid, "s5_index": batch_keys[kid][2],
             "key": [batch_keys[kid][0], batch_keys[kid][1]],
             "legal": batch_keys[kid][4], "result": None, "nodes": None,
             "consumed": False, "probed": False,
             "note": ("fileless UNPROBED: no raw evidence, no verdict claimed; the "
                      "remaining batch-29 drive keys for a future single-owner part")}
            for kid in FILELESS_IDS],
        "changed_per_root_coverage_rows": changed_rows,
        "individual_greedy_union_movers": greedy_moved_rows,
        "holder_union_size": len(holder_union),
        "holder_classes": holder_rows,
        "member_loss_counts": {str(k): v for k, v in sorted(member_loss_counts.items())},
        "metrics": metrics,
        "update8": {
            "newly_resolved_s5": newly_resolved,
            "newly_resolved_count": len(newly_resolved),
            "lost_resolved": lost,
            "note": ("the 16 adopted s5 indices are NOT update8 baseline requirements "
                     "(machine-observed): resolved_count and remaining_now are "
                     "unchanged 141 / 31,718 on both sides"),
        },
        "per_root_greedy": per_root_greedy_movers,
        "roots_summary_moved": roots_summary_moved,
        "probe_worklist": worklist_info,
        "closure_candidate_rows": closure_rows,
    }
    OUT.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("OK decomp-deltas-b29loss16-adoption.json: "
          f"flips={flips} new_free={new_free} "
          f"free_now {metrics['free_now_classes']['base']}->{metrics['free_now_classes']['scenario']} "
          f"class2251_unknown {len(base_unknown[cls])}->{len(scen_unknown[cls])} "
          f"rank {closure_rows['classes'][str(cls)]['base_rank']}->{closure_rows['classes'][str(cls)]['scenario_rank']} "
          f"(38 fileless UNPROBED) "
          f"update8_resolved +{len(newly_resolved)} "
          f"joint_greedy {metrics['joint_greedy_union_size']['base']}->{metrics['joint_greedy_union_size']['scenario']} "
          f"worklist {metrics['probe_worklist_total']['base']}->{metrics['probe_worklist_total']['scenario']} "
          f"kit={kit_info['files_verified']} "
          f"changed_rows={sorted(changed_rows)} "
          f"ig_movers={sorted(greedy_moved_rows)} "
          f"closure_left={left} closure_entered={entered}")


if __name__ == "__main__":
    main()
