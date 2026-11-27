#!/usr/bin/env python3
"""BASE (canonical chain through the Part EU euwin2 third WIN adoption)
vs SCENARIO (evwin4 = Part EV fourth WIN canonical adoption: the 4 EV
gate-verified unconsumed closure-batch WIN rows b018/d002/e002/f017).

Fork of the published Part EU extractor
`compare_deltas_eu_adoption.py` (sha256
9bc5f06aa01aed86fd48f5d17704f5a5c0b97b3c960a3b6795ddc47fb7741666;
structural clone, disclosed diff: the adopted-rows table, both refresh
sides, the manifest decomposition fields, the dossier-supersession
checks and the pinned expectations are Part-EV specific).

Fail-closed machine recomputation of exactly what the Part EV win4
canonical adoption changed, from published bytes only:

* every artifact sha-pinned (BASE = the published Part EU outputs -- the
  merged canonical cache 3ba48608... 6,767 rows WIN 188 / LOSS 6,579,
  the reaudit outputs refresh-summary 2b70bb55... / closure-classes
  59a4c85f... / per-root-coverage cfc2bfe1... and worklist regen pin
  397a4379...; SCEN = the published pre-declaration dossier outputs --
  the scenario merged cache 63f33c4f... 6,771 rows WIN 192 / LOSS 6,579,
  increment 8d0e43ed... (dossier predecl header, superseded row-exactly
  by the Part-emitted increment 7f125610...), the reaudit outputs
  refresh-summary 1fafd081... / closure-classes 6ba51faa... /
  per-root-coverage d9eee976... and worklist regen pin ca50cb68...;
  the Part kit outputs -- increment 7f125610..., increments-manifest
  f013a8f5... (schema evwin4-increments-manifest-v1), merge-audits x3
  (identical sha d9713aed...), the maker (structural clone of the Part
  EU maker f2ae97a1...), the byte-clone of the union merger 90711961...
  and both refresh forks (the published Part EU refresh 6dc24c15... and
  the published dossier refresh fork f2edac3e..., itself a byte-clone
  of 6dc24c15... differing in EXACTLY the three declared regions:
  docstring, CACHE path, expected cache sha; the computation region is
  byte-identical), the frozen graph/update8/board/policy/quarantine
  pins, the EV gate kit SSOT registry gate-rows-ev.json 3ba154f2...
  (re-checked against the EV kit MANIFEST 34d7768b... and audit
  0327dad8...), and the dossier census measurement
  census-deltas-evwin4-predecl.json ab97fba9...); both probe-worklists
  are UNPUBLISHED per the size policy - they enter ONLY as regen pins
  (BASE 397a4379... 3,717,712 B / SCEN ca50cb68... 3,717,416 B)
  re-verified by the byte-verbatim refresh re-execution;
* the published Part EU refresh fork and the published dossier EV
  refresh fork are RE-EXECUTED byte-verbatim in isolated scratch trees
  against their pinned inputs, and all eight outputs must be
  byte-identical to the published / regenerated pins before any delta
  is emitted (double determinism; this simultaneously re-proves the
  published reaudit outputs of both sides are regenerable from
  published bytes);
* the Part-emitted increment 7f125610... is row-for-row identical to
  the published dossier increment 8d0e43ed... (the superseded header
  comment block is the ONLY differing region); the recorded
  supersession: the canonical scenario merged cache of record is the
  published dossier merged file 63f33c4f... and the Part merge audits
  (d9713aed... x3, byte-identical) record exactly this output;
* SCEN cache == BASE cache rows + exactly the 4 Part increment rows
  (verdict agreement everywhere; 6,771 rows, WIN 192 / LOSS 6,579);
  the adopted rows are ALL fresh exact-WIN rows of the Part EV gate
  (b018 class 16757 batch-1 dual-class s5_index 528497 nodes 3,549,602,
  d002 class 20421 batch-3 s5_index 197253 nodes 5,359,994, e002 class
  16371 batch-4 s5_index 183566 nodes 14,112,632, f017 class 12264
  batch-5 s5_index 415095 nodes 3,522,635; adopted node total
  26,544,863; 15M two-pass fresh-cold node-exact batch raws + C++ gate
  raws + third-impl a/b corroboration, re-verified live by the Part
  maker).  Per-row provenance pins are re-verified here against the
  byte-pinned SSOT registry; the 2 Part-EU adopted rows must already
  sit WIN in BASE (regression tie, NOT re-adopted);
* the independent full-class census (frozen graph s4_cost + update8
  receipts + cache verdicts, replicating the refresh status logic)
  must reproduce the published class status counts EXACTLY on both
  sides (BASE 34,430/90/39/390, SCEN 34,417/103/39/390) and identify
  EXACTLY 13 status flips, all UNKNOWN -> excluded_now, exactly the
  BASE-unknown owner classes of the adopted keys (the further owner
  class 30345 was already excluded_now from the Part EP/EU chain and
  must NOT double-flip);
* the 13 flipped owner classes' Board arithmetic: per-class raw
  boundary / cost size / cost-unknown drop of each (the multi-class
  membership b018 in 15640/16757/30345 and d002 in 4 classes /
  e002 in 4 classes / f017 in 3 classes is recomputed from the frozen
  graph), plus the pre-excluded 30345 (51-raw-child boundary, unknown
  5 -> 4) and the no-member 30354 (97/97, unknown 96 static) classes;
* closure-classes.csv: ZERO rows leave, ZERO rows enter (805 -> 805);
  the unknown_now churn is exactly {16371: 2->1, 16757: 3->2,
  30345: 5->4, 20421: 6->5, 12264: 51->50} and the class_rank churn is
  exactly the 7-row set {16371: 4->1, 23101: 1->2, 1849: 2->3,
  2251: 3->4, 12264: 13->11, 13342: 11->12, 30118: 12->13}; NO
  groups_served churn anywhere; every other field of every row is
  byte-identical;
* update8 refresh: resolved 260 -> 263, remaining 31,505 -> 31,445,
  groups_free_now stays 131, union baseline stays 31,859, win_hit
  groups 10 -> 25 = the identical 10 class-30354 quartets of the BASE
  side (unknown_s5_children 97 on both sides) PLUS EXACTLY the 15 new
  quartets of the three hit owner classes {12264: 6, 16757: 5,
  20421: 4}; zero base quartets removed;
* per-root coverage: free_now/uncovered thirds IDENTICAL at all 20
  roots + baseline; Board verification 39/39 with zero rejections on
  both sides; the individual greedy union changes only at the 6 roots
  {0: 2980->2789, 5: 2884->2883, 12: 2848->2846, 36: 3005->2951,
  37: 3620->3619, 48: 2895->2893} (pure re-selection bookkeeping, no
  coverage claim);
* the frozen greedy scheduler deltas are recorded as bookkeeping (joint
  greedy 36,619 -> 36,618, group_best_options_nonfree stays 2,105,
  worklist 64,307 -> 64,302);
* the published dossier census measurement ab97fba9... is machine
  cross-compared field-by-field against this independent recount
  (census counts, flip set, closure churn, per-root greedy deltas,
  joint greedy, worklist totals, update8 numbers, the 15 new
  win_hit quartets and both cache identities): agreement must be
  EXACT.  The dossier verdict scope fields (consumed NOTHING,
  part_ev_declared false) describe the dossier-time status and are
  superseded by the Part EV declaration (disclosed, not asserted).

No unknown verdict is asserted anywhere.  The standard 11x11 empty board
and every central-reply root stay UNKNOWN; free_now / coverage
quantities are scheduling bookkeeping derived from exact verdicts, not
root verdict claims.  Consuming the 4 WIN labels transfers NO verdict to
any root: 13 classes become excluded (a known WIN cost child ends free
all-LOSS coverage), which removes them from the free-coverage option
space - recorded honestly below.  The 21 unconsumed closure-batch LOSS
rows, k04, and every other unconsumed probe-level WIN stay in NO
cache; 11x11 stays UNKNOWN.
"""
import csv
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]

BASE_EXP = ROOT / "research/experiments/n11-centralreply-euwin2-adoption-reaudit-20261125"
BASE_OUT = BASE_EXP / "reaudit/output"
BASE_CACHE = BASE_EXP / "output/merged-exact-s5-chain-plus-euwin2-20261125.cache"
BASE_INCREMENT = BASE_EXP / "output/increment-euwin2-20261125.cache"
DOSSIER = ROOT / "research/experiments/n11-centralreply-evwin4-adoption-predecl-20261126"
SCEN_CACHE = DOSSIER / "output/merged-exact-s5-chain-plus-evwin4-20261126.cache"
INCR = EXP / "output/increment-evwin4-20261126.cache"
MANIFEST = EXP / "output/increments-manifest.json"
CENSUSJSON = DOSSIER / "output/census-deltas-evwin4-predecl.json"
DOSSIER_INCR = DOSSIER / "output/increment-evwin4-20261126.cache"
EV_KIT = ROOT / "research/experiments/n11-centralreply-closure-wins-b018d002e002f017-cppgate-20261125"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_REFRESH_SCRIPT = BASE_EXP / "reaudit/scripts/refresh_adoption_eu.py"
SCEN_REFRESH_SCRIPT = DOSSIER / "reaudit/scripts/refresh_adoption_evwin4.py"
MERGER = EXP / "scripts/s5_union_merge.py"
MAKER = EXP / "scripts/make_increments_ev_win4_adoption.py"
DECOMP_OUT = EXP / "output/decomp-deltas-evwin4-adoption.json"

# ---- pins ------------------------------------------------------------------
BASE_CACHE_SHA = "3ba486086703b9f44a0c685d7d5b45fab80f86760f2cd032a8dc18a2690233d6"
SCEN_CACHE_SHA = "63f33c4f620583449641102026b261c559ae5ecc29713cd6445d6fe9369858f0"
INCR_SHA = "7f1256108d697bd96d473e55a5509dea35f4c0b1be45893cac3f667c4b3f55c4"
MANIFEST_SHA = "f013a8f54807297c649538958bbc19b156eab7d469019a1d1dbf7bc31a4726b9"
MAKER_SHA = None  # asserted at run (the maker bytes are pinned by the wave-B MANIFEST)
DOSSIER_INCR_SHA = "8d0e43ed34b80142143f16d5fc4b1aa900473badc17341425ac517053552a7c7"
CENSUSJSON_SHA = "ab97fba9149991be00f3d4f35d1382a974ff4dcedb15443eb23206b5b416d7d1"
BASE_SUMMARY_SHA = "2b70bb55b25635f78e2cdd9559d8eab30d9c98640e5507ad280c6a510d958477"
BASE_CLOSURE_SHA = "59a4c85fdd25a8d161bfb46598a8f8c77a684c996d456ba85b125f840134bf0e"
BASE_PRC_SHA = "cfc2bfe15508c4d0c3455ca2f2abedd2a233d01118dbae95353bdc5b79f8e47f"
BASE_WORKLIST_SHA = "397a43794be60442725825371a5cfba9c2744a69b8f5d32cb3a3f313ced29ba6"
SCEN_SUMMARY_SHA = "1fafd0811d4b5e806a11cf610111967b9d6fdb741fa86b68688ef1cee4411e6e"
SCEN_CLOSURE_SHA = "6ba51faa9824ba5065a8e938cc6970ce2ace464f74d26f30582cbaa8334c930d"
SCEN_PRC_SHA = "d9eee976e52c38c71440a26cb6f9f14ae68439feaec21e17600b1052870dd502"
SCEN_WORKLIST_SHA = "ca50cb68c10827e7e24e02c02e0166813b57ad646eb169bf8bd2c827fcdd09df"
BASE_REFRESH_SHA = "6dc24c15e0ddfa9043d715dd09a794819ef0c393fe15d0491c5beb04042e9fad"
SCEN_REFRESH_SHA = "f2edac3e3e3c74ddd073a709a0ab521cf8c3db1048322e1f0347a1ea013aa885"
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
MERGE_AUDIT_SHA = "d9713aed5c0679605bb3e10e0198e1c15fd7b5b3867f3a253f5251b8a0dc667f"
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
BOARD_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
EV_KIT_MANIFEST_SHA = "34d7768bc68e0829ac725d33c91de0dea147dcc89239e3736dc4b1a06ddce9cb"
EV_REGISTRY_SHA = "3ba154f2f803a7a25de0133ac0fd0c3ed2df4c4ce7733bec4c8adc01e064659f"
EV_AUDIT_SHA = "0327dad83f7c33d475656d8d1f9ccd2e67c3b78f8f394b9a5daf74c2b96c91c4"
EU_INCREMENT_SHA = "d9365d80a90aff30cb451f8f2519ab2cc004c6d10ba4fb149a7ee340e0aa0b4f"
MERGED_COMMENT = "# S5 solver-trusted exact; base=merged-exact-s5-after-js-probe-13.cache (sha256 60e0dc3476920d4e...); increment=101 fresh rows (99 canonical S5 children of S4 1297036692683752448:0 absent from the chain, 2 unclaimed backward-only rows, 1 S6-witness-derived TARGET_S5 row nodes=0); see merge-manifest.json"

ADOPTED = {
    "b018": (528497, 1153204079095189504, 65536),
    "d002": (197253, 3461016313634230272, 131072),
    "e002": (183566, 1153765929805414400, 16),
    "f017": (415095, 1188950301625810945, 70368744177666),
}
ADOPTED_IDS = ["b018", "d002", "e002", "f017"]
ADOPTED_CLASS = {"b018": 16757, "d002": 20421, "e002": 16371, "f017": 12264}
ADOPTED_NODES = 26544863
ADOPTED_ROW_NODES = {"b018": 3549602, "d002": 5359994, "e002": 14112632, "f017": 3522635}
FLIP_CLASSES = [4864, 4903, 5255, 5282, 5613, 6030, 12264, 12327,
                14776, 15640, 16371, 16757, 20421]
PREV_EXCLUDED_OWNERS = [30345]
CENSUS_BEFORE = {"unknown": 34430, "excluded_now": 90, "free_now": 39, "excluded": 390}
CENSUS_AFTER = {"unknown": 34417, "excluded_now": 103, "free_now": 39, "excluded": 390}
OWNER_SETS = {
    "b018": [15640, 16757, 30345],
    "d002": [5255, 5282, 6030, 20421],
    "e002": [4864, 4903, 5613, 16371],
    "f017": [12264, 12327, 14776],
}
WIN_HIT_QUARTETS_BASE = [(12, 40, 96, 60), (12, 80, 96, 60), (12, 96, 40, 60),
                         (24, 40, 108, 60), (24, 80, 108, 60), (24, 108, 40, 60),
                         (36, 20, 90, 60), (36, 30, 100, 60), (36, 90, 20, 60),
                         (36, 100, 30, 60)]
# the 15 NEW win_hit groups of the SCEN side: (first, third, fourth, reply,
# s4_class_index, unknown_s5_children as recorded by the refresh)
WIN_HIT_NEW_15 = [
    (0, 5, 10, 60, 12264, 51), (0, 10, 5, 60, 12264, 51),
    (0, 55, 110, 60, 12264, 51), (0, 110, 55, 60, 12264, 51),
    (5, 0, 10, 60, 12264, 51), (5, 10, 0, 60, 12264, 51),
    (12, 51, 81, 60, 20421, 49), (12, 81, 51, 60, 20421, 49),
    (36, 50, 84, 60, 16757, 48), (36, 70, 84, 60, 16757, 48),
    (36, 84, 50, 60, 16757, 48),
    (37, 73, 100, 60, 20421, 49), (37, 100, 73, 60, 20421, 49),
    (48, 40, 80, 60, 16757, 48), (48, 80, 40, 60, 16757, 48),
]
GREEDY_DELTA = {0: (2980, 2789), 5: (2884, 2883), 12: (2848, 2846),
                36: (3005, 2951), 37: (3620, 3619), 48: (2895, 2893)}
JOINT_GREEDY = (36619, 36618)
GROUP_BEST_NONFREE = (2105, 2105)
WORKLIST_TOTAL = (64307, 64302)
UPD8 = {"resolved": (260, 263), "remaining": (31505, 31445), "free_groups": (131, 131)}
CLOSURE = {"rows": (805, 805), "left": [], "entered": []}
CLOSURE_UNKNOWN_CHURN = {16371: ("2", "1"), 16757: ("3", "2"), 30345: ("5", "4"),
                         20421: ("6", "5"), 12264: ("51", "50")}
CLOSURE_RANK_CHURN = {1849: (2, 3), 2251: (3, 4), 23101: (1, 2), 12264: (13, 11),
                      13342: (11, 12), 16371: (4, 1), 30118: (12, 13)}
# per-class boundary expectations: class -> (raw_boundary, cost_size,
#   unknown_before, unknown_after, adopted_members)
CLASS_CHECKS = {
    4864: (101, 101, 101, 100, ["e002"]),
    4903: (105, 103, 102, 101, ["e002"]),
    5255: (104, 104, 104, 103, ["d002"]),
    5282: (95, 95, 95, 94, ["d002"]),
    5613: (105, 105, 105, 104, ["e002"]),
    6030: (103, 102, 102, 101, ["d002"]),
    12264: (52, 52, 51, 50, ["f017"]),
    12327: (99, 99, 99, 98, ["f017"]),
    14776: (59, 59, 59, 58, ["f017"]),
    15640: (96, 93, 93, 92, ["b018"]),
    16371: (52, 52, 2, 1, ["e002"]),
    16757: (49, 49, 3, 2, ["b018"]),
    20421: (50, 49, 6, 5, ["d002"]),
    30345: (51, 50, 5, 4, ["b018"]),
    30354: (97, 97, 96, 96, []),
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fail(msg):
    print(f"ABORT {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_cache(path: Path):
    cache = {}
    for row in csv.reader(path.open(encoding="utf-8-sig", newline="")):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 6 or row[0] != "s5verdict":
            fail(f"invalid cache row: {row}")
        key = (int(row[1]), int(row[2]))
        if key in cache and cache[key] != (int(row[4]), int(row[5])):
            fail(f"cache conflict at {key}")
        cache[key] = (int(row[4]), int(row[5]))
    return cache


def cache_row_list(path: Path):
    return [ln for ln in path.read_text(encoding="utf-8-sig").splitlines() if ln.startswith("s5verdict,")]


def rerun_refresh(script: Path, script_sha: str, tmp_name: str):
    if sha(script) != script_sha:
        fail(f"refresh script sha drift: {script.name}")
    scratch = ROOT / "research/experiments" / tmp_name
    outdir = scratch / "reaudit"
    if scratch.exists():
        shutil.rmtree(scratch)
    (outdir / "scripts").mkdir(parents=True)
    (outdir / "output").mkdir()
    shutil.copyfile(script, outdir / "scripts" / script.name)
    if sha(outdir / "scripts" / script.name) != script_sha:
        fail("scratch copy of refresh script not byte-identical")
    proc = subprocess.run([sys.executable, str(outdir / "scripts" / script.name)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        fail(f"refresh re-execution failed ({script.name}): {proc.stderr[-400:]}")
    return outdir / "output"


def main() -> None:
    global MAKER_SHA
    MAKER_SHA = sha(MAKER)
    pins = [
        ("base cache", BASE_CACHE, BASE_CACHE_SHA),
        ("scenario cache", SCEN_CACHE, SCEN_CACHE_SHA),
        ("increment", INCR, INCR_SHA),
        ("manifest", MANIFEST, MANIFEST_SHA),
        ("maker", MAKER, MAKER_SHA if MAKER_SHA else sha(MAKER)),
        ("base (EU) increment", BASE_INCREMENT, EU_INCREMENT_SHA),
        ("dossier increment (superseded)", DOSSIER_INCR, DOSSIER_INCR_SHA),
        ("dossier census measurement", CENSUSJSON, CENSUSJSON_SHA),
        ("EV gate kit MANIFEST", EV_KIT / "MANIFEST-sha256.txt", EV_KIT_MANIFEST_SHA),
        ("EV gate SSOT registry", EV_KIT / "input/gate-rows-ev.json", EV_REGISTRY_SHA),
        ("EV gate audit", EV_KIT / "output/audit_gate.json", EV_AUDIT_SHA),
        ("base refresh-summary", BASE_OUT / "refresh-summary.json", BASE_SUMMARY_SHA),
        ("base closure-classes", BASE_OUT / "closure-classes.csv", BASE_CLOSURE_SHA),
        ("base per-root-coverage", BASE_OUT / "per-root-coverage.csv", BASE_PRC_SHA),
        ("scenario refresh-summary", DOSSIER / "reaudit/output/refresh-summary.json", SCEN_SUMMARY_SHA),
        ("scenario closure-classes", DOSSIER / "reaudit/output/closure-classes.csv", SCEN_CLOSURE_SHA),
        ("scenario per-root-coverage", DOSSIER / "reaudit/output/per-root-coverage.csv", SCEN_PRC_SHA),
        ("base refresh script", BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA),
        ("scenario refresh script", SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA),
        ("union merger byte-clone", MERGER, MERGER_SHA),
        ("merge-audit run1", EXP / "output/merge-audit-run1.json", MERGE_AUDIT_SHA),
        ("merge-audit run2", EXP / "output/merge-audit-run2.json", MERGE_AUDIT_SHA),
        ("merge-audit run3", EXP / "output/merge-audit-run3.json", MERGE_AUDIT_SHA),
        ("graph", GRAPH, GRAPH_SHA),
        ("update8", UPDATE8, UPDATE8_SHA),
        ("board source", BOARD_SOURCE, BOARD_SHA),
        ("policy", POLICY, POLICY_SHA),
        ("quarantine", QUARANTINE, QUARANTINE_SHA),
    ]
    for name, p, want in pins:
        got = sha(p)
        if got != want:
            fail(f"{name} sha drift: {got} != {want}")

    # --- manifest decomposition ----------------------------------------------
    manifest = json.loads(MANIFEST.read_text())
    if manifest["schema"] != "evwin4-increments-manifest-v1":
        fail("manifest schema drift")
    if manifest["part"] != "EV" or manifest["date"] != "2026-11-26":
        fail("manifest part/date drift")
    if manifest["win_canonical_adoption"] is not True:
        fail("manifest win_canonical_adoption flag drift")
    if manifest["base_cache_sha256"] != BASE_CACHE_SHA:
        fail("manifest base cache pin drift")
    if manifest["sha256"]["win_increment"] != INCR_SHA:
        fail("manifest win_increment pin drift")
    if manifest["merger_sha256"] != MERGER_SHA:
        fail("manifest merger pin drift")
    if manifest["base_cache_rows"] != 6767:
        fail("manifest base rows drift")
    if manifest["row_counts"] != {"adopted_win_rows": 4,
                                  "exhausted_honest_unknown_rows": 0,
                                  "prior_canonical_rows_base": 6767,
                                  "loss_rows_this_pool": 0}:
        fail("manifest row_counts drift")
    if manifest["adopted_ids"] != ADOPTED_IDS or manifest["targets"] != ADOPTED_IDS:
        fail("manifest adopted/target ids drift")
    if manifest["adopted_nodes_per_pool"] != ADOPTED_NODES:
        fail("manifest adopted node pool drift")
    ert = manifest["eu_regression_tie"]
    if ert["eu_increment_sha256"] != EU_INCREMENT_SHA or \
            ert["adopted_rows_win_in_base"] != 2 or not ert.get("note"):
        fail("manifest EU regression tie drift")
    if manifest["quarantine_hits"] != 0:
        fail("manifest quarantine hits drift")
    if manifest["base_cache_absent_hits_for_emitted"] != 4:
        fail("manifest base-absent hits drift")
    rows = manifest["adopted_win_rows"]
    if len(rows) != 4:
        fail("manifest adopted row count drift")
    if sum(r["nodes"] for r in rows) != ADOPTED_NODES:
        fail("manifest adopted node sum drift")
    # registry cross-SSOT + live re-hash of every per-row evidence file
    registry = json.loads((EV_KIT / "input/gate-rows-ev.json").read_text())
    regt = registry["targets"]
    if registry.get("part") != "EV":
        fail("EV registry part drift")
    audit = json.loads((EV_KIT / "output/audit_gate.json").read_text())
    if audit.get("overall") != "PASS" or audit.get("part") != "EV":
        fail("EV gate audit honesty drift (extractor side)")
    if audit.get("schema") != "n11-centralreply-cppgate-wins41164-audit-v1":
        fail("EV gate audit schema drift")
    if any(g["status"] != "PASS" for g in audit["gates"].values()):
        fail("an EV gate audit gate is not PASS")
    BATCH_KIT = {
        "b018": "n11-centralreply-closure-class16757-batch-20261122",
        "d002": "n11-centralreply-closure-class20421-batch-20261122",
        "e002": "n11-centralreply-closure-class16371-batch4-20261122",
        "f017": "n11-centralreply-closure-class12264-batch5-20261122",
    }
    THIRDIMPL = ROOT / "research/experiments/n11-centralreply-closure-wins-thirdimpl-reverify-20261122"
    for r in rows:
        kid = r["key_id"]
        reg = regt[kid]
        bb = r["batch_basis"]
        ok = (kid in ADOPTED and
              r["class"] == ADOPTED_CLASS[kid] == int(reg["class_index"]) and
              (r["s5_index"], r["lo"], r["hi"]) == ADOPTED[kid] and
              (int(reg["s5_index"]), int(reg["lo"]), int(reg["hi"])) == ADOPTED[kid] and
              r["result"] == 1 and
              r["budget"] == 15000000 and int(reg["budget"]) == 15000000 and
              r["nodes"] == ADOPTED_ROW_NODES[kid] and
              r["expect_third"] == 1 and
              reg["expected"] == f"{r['legal']},15000000,1,{ADOPTED_ROW_NODES[kid]}" and
              reg["result_label"] == "WIN" and
              r["gate_kit"] == "ev" and
              r["gate_input_sha256"] == reg["input_pin"] and
              bb["kit"] == BATCH_KIT[kid] and
              bb["batch_keys_sha256"] == reg["batch_source_pins"]["batch_keys_sha256"] and
              bb["input_sha256"] == reg["batch_source_pins"]["input_sha256"] and
              bb["status_log_sha256"] == reg["batch_source_pins"]["status_log_sha256"] and
              bb["raw_p1_sha256"] == reg["batch_source_pins"]["raw_p1_sha256"] and
              bb["raw_p2_sha256"] == reg["batch_source_pins"]["raw_p2_sha256"] and
              bb["win_halted_at"] and
              bb["thirdimpl_rows_json_sha256"] == "03048edb26d886ae8b0fd903be6b8aa7d066b8883b1441d25448f89f77109b40" and
              len(bb["thirdimpl_out_a_sha256"]) == 64 and
              len(bb["thirdimpl_out_b_sha256"]) == 64 and
              len(bb["thirdimpl_expansion_counts"]) == 2 and
              all(n > 0 for n in bb["thirdimpl_expansion_counts"]) and
              r.get("extra_provenance") is None)
        if not ok:
            fail(f"manifest adopted row drift: {kid}")
        # live re-hash: gate kit, batch kit, thirdimpl kit (all published bytes)
        bk = ROOT / "research/experiments" / BATCH_KIT[kid]
        pins_live = [
            (EV_KIT / "input" / f"{kid}.input.csv", r["gate_input_sha256"]),
            (EV_KIT / "output/raw" / f"{kid}.p1.out", r["gate_raw_p1_sha256"]),
            (EV_KIT / "output/raw" / f"{kid}.p2.out", r["gate_raw_p2_sha256"]),
            (bk / "input/batch-keys.json", bb["batch_keys_sha256"]),
            (bk / "input" / f"{kid}.input.csv", bb["input_sha256"]),
            (bk / "output/status.log", bb["status_log_sha256"]),
            (bk / "output/raw" / f"{kid}.p1.out", bb["raw_p1_sha256"]),
            (bk / "output/raw" / f"{kid}.p2.out", bb["raw_p2_sha256"]),
            (THIRDIMPL / "input/rows.json", bb["thirdimpl_rows_json_sha256"]),
            (THIRDIMPL / f"input/{kid}.input.csv", bb["input_sha256"]),
            (THIRDIMPL / "output/targets" / f"{kid}.a.out", bb["thirdimpl_out_a_sha256"]),
            (THIRDIMPL / "output/targets" / f"{kid}.b.out", bb["thirdimpl_out_b_sha256"]),
        ]
        for p, want in pins_live:
            if sha(p) != want:
                fail(f"adopted-row evidence re-hash drift: {kid} {p.name}")
    prov = manifest["provenance"]
    if prov["ev_kit_manifest_sha256"] != EV_KIT_MANIFEST_SHA or \
            prov["ev_registry_sha256"] != EV_REGISTRY_SHA or \
            prov["ev_audit_sha256"] != EV_AUDIT_SHA or \
            prov["ev_audit_schema"] != "n11-centralreply-cppgate-wins41164-audit-v1" or \
            prov["ev_audit_schema"] != audit["schema"] or \
            prov["ev_gate_status_pass"] != 7 or \
            prov["ev_audit_reruns_byte_identical"] != 4 or \
            prov["ev_gate_source_sha256"] != registry["gate_source"]["sha256"] or \
            prov["ev_gate_source_commit"] != registry["gate_source"]["commit"] or \
            prov["ev_gate_source_commit"] != "154f3b7a67b97e13acbaee8b04dc74ddca728d19" or \
            prov["thirdimpl_manifest_sha256"] != sha(
                ROOT / "research/experiments/n11-centralreply-closure-wins-thirdimpl-reverify-20261122/MANIFEST.sha256") or \
            prov["thirdimpl_rows_json_sha256"] != "03048edb26d886ae8b0fd903be6b8aa7d066b8883b1441d25448f89f77109b40" or \
            "20 files" not in prov["batch_kit_integrity"] or \
            "36/36" not in prov["batch_kit_integrity"] or \
            "96/96" not in prov["batch_kit_integrity"] or \
            not prov["pin_policy"]:
        fail("manifest provenance EV gate/batch pin drift")
    pool = manifest["pool_derivation"]
    if pool["targets_adopted_here"] != ADOPTED_IDS or \
            "no new solver pass" not in pool["resolution"]:
        fail("manifest pool derivation drift")
    oos = manifest["verdicts_out_of_scope_unconsumed"]
    for key in ("closure_batch_loss_rows", "k04_sixthcost_win", "b018_dual_class",
                "other_closure_wins", "no_reprobe"):
        if not oos.get(key):
            fail(f"manifest must declare the out-of-scope entry: {key}")
    if "UNKNOWN" not in manifest["interpretation_guard"]:
        fail("manifest interpretation guard drift")

    # --- dossier supersession: Part increment rows == dossier increment rows
    if cache_row_list(INCR) != cache_row_list(DOSSIER_INCR):
        fail("Part increment rows differ from the dossier increment rows")

    # --- merge-audit decomposition --------------------------------------------
    for rn in ("merge-audit-run1.json", "merge-audit-run2.json", "merge-audit-run3.json"):
        a = json.loads((EXP / "output" / rn).read_text())
        if a["unique_rows"] != 6771 or a["duplicate_rows_elided"] != 0:
            fail(f"merge-audit row accounting drift: {rn}")
        if a["verdict_counts"] != {"WIN(1)": 192, "LOSS(2)": 6579}:
            fail(f"merge-audit verdict counts drift: {rn}")
        if a["nodes_field_mismatches_recorded"] != []:
            fail(f"merge-audit nodes mismatch drift: {rn}")
        if a["output_sha256"] != SCEN_CACHE_SHA or a["output_bytes"] != 282733:
            fail(f"merge-audit output identity drift: {rn}")
        if a["comments_kept_from_first_input"] != [MERGED_COMMENT]:
            fail(f"merge-audit comment block drift: {rn}")
        ins = a["inputs"]
        if len(ins) != 2 or ins[0]["sha256"] != BASE_CACHE_SHA or \
                ins[0]["rows"] != 6767 or ins[0]["unique_new"] != 6767:
            fail(f"merge-audit BASE input entry drift: {rn}")
        if ins[1]["sha256"] != INCR_SHA or ins[1]["rows"] != 4 or ins[1]["unique_new"] != 4:
            fail(f"merge-audit increment input entry drift: {rn}")
        if not ins[1]["file"].endswith(
                "n11-centralreply-evwin4-adoption-reaudit-20261126/output/increment-evwin4-20261126.cache"):
            fail(f"merge-audit increment path drift: {rn}")

    # --- refresh re-execution (both sides, byte-verbatim) --------------------
    base_tmp = rerun_refresh(BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA, ".ev-verify-base-eu")
    scen_tmp = rerun_refresh(SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA, ".ev-verify-scen-evwin4")
    checks = [
        (base_tmp / "refresh-summary.json", BASE_OUT / "refresh-summary.json", BASE_SUMMARY_SHA),
        (base_tmp / "closure-classes.csv", BASE_OUT / "closure-classes.csv", BASE_CLOSURE_SHA),
        (base_tmp / "per-root-coverage.csv", BASE_OUT / "per-root-coverage.csv", BASE_PRC_SHA),
        (base_tmp / "probe-worklist.csv", None, BASE_WORKLIST_SHA),
        (scen_tmp / "refresh-summary.json", DOSSIER / "reaudit/output/refresh-summary.json", SCEN_SUMMARY_SHA),
        (scen_tmp / "closure-classes.csv", DOSSIER / "reaudit/output/closure-classes.csv", SCEN_CLOSURE_SHA),
        (scen_tmp / "per-root-coverage.csv", DOSSIER / "reaudit/output/per-root-coverage.csv", SCEN_PRC_SHA),
        (scen_tmp / "probe-worklist.csv", None, SCEN_WORKLIST_SHA),
    ]
    for tmp_out, pub, want_sha in checks:
        if sha(tmp_out) != want_sha:
            fail(f"refresh re-execution output drift: {tmp_out.name} ({tmp_out.parent.parent.name})")
        if pub is not None and sha(pub) != want_sha:
            fail(f"published output drifted from pin: {pub}")
    shutil.rmtree(ROOT / "research/experiments/.ev-verify-base-eu")
    shutil.rmtree(ROOT / "research/experiments/.ev-verify-scen-evwin4")

    # --- frozen dependency graph + cache relation ---------------------------
    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s5_masks = g["s5_masks"]
    m2i_probe = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}

    # --- cache relation: SCEN == BASE + exactly the 4 increment rows --------
    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    incr = load_cache(INCR)
    if len(base) != 6767 or len(scen) != 6771 or len(incr) != 4:
        fail(f"cache sizes drift: base {len(base)} scen {len(scen)} incr {len(incr)}")
    adopted_keys = {(ADOPTED[k][1], ADOPTED[k][2]): k for k in ADOPTED}
    for key, row in incr.items():
        if row[0] != 1:
            fail(f"increment contains a non-WIN row: {key}")
        if key in base:
            fail(f"increment key already in BASE: {key}")
        if key not in adopted_keys:
            fail(f"increment key not in the adopted set: {key}")
        if scen.get(key) != row:
            fail(f"increment row not taken verbatim into scenario cache: {key}")
    merged = dict(base)
    for key, row in incr.items():
        merged[key] = row
    if merged != scen:
        fail("scenario cache != BASE rows + increment rows (set difference)")
    wins = sum(1 for v in scen.values() if v[0] == 1)
    losses = len(scen) - wins
    if (wins, losses) != (192, 6579):
        fail(f"scenario verdict counts {wins}/{losses} != 192/6,579")
    if sum(v[1] for v in incr.values()) != ADOPTED_NODES:
        fail("increment node total drift")
    # EU regression tie: both Part-EU adopted rows already sit WIN in BASE
    eu_inc = load_cache(BASE_INCREMENT)
    if len(eu_inc) != 2:
        fail("EU increment row count drift")
    for key, row in eu_inc.items():
        if base.get(key) is None or base[key][0] != 1 or row[0] != 1:
            fail(f"EU regression tie broken: {key} not WIN in BASE")
        if base[key][1] != row[1]:
            fail(f"EU regression nodes tie broken: {key}")
        if key in incr:
            fail("a Part-EU row must NOT be re-adopted by EV")

    # --- independent full-class census --------------------------------------
    sys.path.insert(0, str(BOARD_SOURCE.parent))
    sys.path.insert(0, str(POLICY.parent))
    from independent import Board  # noqa: E402
    from s5_evidence_policy import quarantined_cache_keys, is_canonical_safe_s5_key  # noqa: E402
    quarantined = quarantined_cache_keys()
    s4_masks, s4_status, s4_cost = g["s4_masks"], g["s4_status"], g["s4_cost"]
    m2i = m2i_probe
    update8 = json.loads(UPDATE8.read_text())
    receipts = {int(k): int(v) for k, v in update8["resolved_s5_verdicts"].items()}
    adopted_indices = {m2i[(ADOPTED[k][1], ADOPTED[k][2])]: k for k in ADOPTED}
    for key in incr:
        if key not in m2i:
            fail("an adopted key sits outside the s5 universe")
        if not is_canonical_safe_s5_key(key):
            fail("an adopted key is not a canonical safe s5 key")
        if key in quarantined:
            fail("a quarantined key sits inside the adopted increment")

    def known(j, cache):
        lo, hi = s5_masks[j]
        if (lo, hi) in cache:
            return cache[(lo, hi)][0]
        if j in receipts:
            return 2 if receipts[j] == 2 else 1
        return None

    def census(cache):
        out = {}
        for i in range(len(s4_masks)):
            base_st = s4_status[i]
            if base_st == -1:
                out[i] = ("excluded", [], False)
                continue
            win_hit = False
            unknown = []
            for j in s4_cost[i]:
                v = known(j, cache)
                if v == 1:
                    win_hit = True
                elif v is None:
                    unknown.append(j)
            if base_st == 1:
                st = "excluded_now" if win_hit else ("free_now" if not unknown else "unknown")
            else:
                st = "excluded_now" if win_hit else "free_now"
            out[i] = (st, unknown, win_hit)
        return out

    cb, ca = census(base), census(scen)
    if dict(Counter(v[0] for v in cb.values())) != CENSUS_BEFORE:
        fail("independent census before-drift vs the published BASE counts")
    if dict(Counter(v[0] for v in ca.values())) != CENSUS_AFTER:
        fail("independent census after-drift vs the published SCEN counts")
    changed = sorted(i for i in cb if cb[i][0] != ca[i][0])
    if changed != sorted(FLIP_CLASSES):
        fail(f"census flip set drift: {changed}")
    if any(cb[i][0] != "unknown" or ca[i][0] != "excluded_now" for i in FLIP_CLASSES):
        fail("every flipped class must be UNKNOWN -> excluded_now")
    for i in FLIP_CLASSES:
        members = sorted(adopted_indices[j] for j in s4_cost[i] if j in adopted_indices)
        if not members:
            fail(f"flipped class {i} holds no adopted key")
    owners = {}
    for i in range(len(s4_masks)):
        for j in s4_cost[i]:
            if j in adopted_indices:
                owners.setdefault(adopted_indices[j], []).append(i)
    for k in owners:
        if sorted(owners[k]) != OWNER_SETS[k]:
            fail(f"per-key owner class set drift: {k}")
    owner_union = sorted({c for v in owners.values() for c in v})
    if owner_union != sorted(set(FLIP_CLASSES) | set(PREV_EXCLUDED_OWNERS)):
        fail(f"adopted-key owner union != 13 flips + the chain-pre-excluded 30345: {owner_union}")
    for i in PREV_EXCLUDED_OWNERS:
        if cb[i][0] != "excluded_now" or ca[i][0] != "excluded_now":
            fail(f"chain-pre-excluded owner class {i} must stay excluded_now on both sides")

    # --- Board boundary arithmetic --------------------------------------------
    board = Board(11)

    def boundary(cls):
        lo, hi = s4_masks[cls]
        return {(c & ((1 << 64) - 1), c >> 64) for c in board.children(lo | (hi << 64))}

    def check_class(cls, raw_boundary, cost_size, unknown_before, unknown_after,
                    adopted_members):
        kids = boundary(cls)
        if len(kids) != raw_boundary:
            fail(f"class-{cls} Board boundary {len(kids)} != {raw_boundary}")
        cost = s4_cost[cls]
        if len(cost) != cost_size:
            fail(f"class-{cls} cost size {len(cost)} != {cost_size}")
        own = sorted(adopted_indices[j] for j in set(cost) & set(adopted_indices))
        if own != sorted(adopted_members):
            fail(f"class-{cls} adopted members {own} != {sorted(adopted_members)}")
        ub = sum(1 for j in cost if known(j, base) is None)
        ua = sum(1 for j in cost if known(j, scen) is None)
        if (ub, ua) != (unknown_before, unknown_after):
            fail(f"class-{cls} cost-unknown {ub}->{ua} != {unknown_before}->{unknown_after}")
        if any(k in quarantined for k in kids):
            fail(f"a quarantined key sits inside the class-{cls} boundary")
        return {"class": cls, "boundary_raw": len(kids), "cost_size": cost_size,
                "cost_unknown_base": ub, "cost_unknown_scen": ua,
                "adopted_members": own,
                "status_base": cb[cls][0], "status_scen": ca[cls][0]}

    cls_records = {cls: check_class(cls, *CLASS_CHECKS[cls]) for cls in CLASS_CHECKS}
    if cls_records[30345]["status_base"] != "excluded_now" or \
            cls_records[30345]["status_scen"] != "excluded_now":
        fail("class 30345 must be excluded_now on both sides (EP/EU chain flipped it)")
    for cls in FLIP_CLASSES:
        if cls_records[cls]["status_base"] != "unknown" or \
                cls_records[cls]["status_scen"] != "excluded_now":
            fail(f"class {cls} must flip unknown -> excluded_now")
    if cls_records[30354]["status_base"] != "excluded_now" or \
            cls_records[30354]["status_scen"] != "excluded_now":
        fail("class 30354 must stay excluded_now (EP-flipped, no EV member)")

    # --- closure-classes.csv comparison ----------------------------------------
    def read_closure(p):
        return {int(r["class_index"]): r for r in csv.DictReader(open(p))}

    c_before, c_after = read_closure(BASE_OUT / "closure-classes.csv"), \
        read_closure(DOSSIER / "reaudit/output/closure-classes.csv")
    left = sorted(set(c_before) - set(c_after))
    entered = sorted(set(c_after) - set(c_before))
    if left != CLOSURE["left"] or entered != CLOSURE["entered"]:
        fail(f"closure left/entered drift: left {left} entered {entered}")
    if (len(c_before), len(c_after)) != CLOSURE["rows"]:
        fail("closure row counts drift")
    common = set(c_before) & set(c_after)
    if len(common) != 805:
        fail(f"closure common-row count {len(common)} != 805")
    churn = {"unknown": {}, "rank": {}, "groups": {}}
    for c in sorted(common):
        b, a = c_before[c], c_after[c]
        if b["unknown_now"] != a["unknown_now"]:
            churn["unknown"][c] = (b["unknown_now"], a["unknown_now"])
        if b["class_rank"] != a["class_rank"]:
            churn["rank"][c] = (int(b["class_rank"]), int(a["class_rank"]))
        if b["groups_served_count"] != a["groups_served_count"]:
            churn["groups"][c] = (b["groups_served_count"], a["groups_served_count"])
        for f in b:
            if f in ("class_rank", "unknown_now"):
                continue
            if b[f] != a[f]:
                fail(f"closure field {f} churn at class {c} (byte-identity required)")
    if churn["unknown"] != CLOSURE_UNKNOWN_CHURN:
        fail(f"closure unknown churn drift: {churn['unknown']}")
    if churn["rank"] != CLOSURE_RANK_CHURN:
        fail(f"closure rank churn drift: {churn['rank']}")
    if churn["groups"] != {}:
        fail(f"closure groups_served churn drift: {churn['groups']}")

    # --- update8 refresh comparison -------------------------------------------
    sb = json.loads((BASE_OUT / "refresh-summary.json").read_text())
    sa = json.loads((DOSSIER / "reaudit/output/refresh-summary.json").read_text())
    ub_, ua_ = sb["frozen_update8_refresh"], sa["frozen_update8_refresh"]
    if ub_["union_size_baseline"] != 31859 or ua_["union_size_baseline"] != 31859:
        fail("update8 baseline drift")
    if (ub_["resolved_count"], ua_["resolved_count"]) != UPD8["resolved"]:
        fail("update8 resolved drift")
    if (ub_["remaining_now"], ua_["remaining_now"]) != UPD8["remaining"]:
        fail("update8 remaining drift")
    if (ub_["groups_free_now"], ua_["groups_free_now"]) != UPD8["free_groups"]:
        fail("update8 free groups drift")
    # win_hit groups: the BASE 10 class-30354 quartets stay identical; the SCEN
    # side holds exactly those 10 PLUS the 15 new quartets of the 3 hit classes
    if len(ua_["win_hit_groups"]) != 25 or len(ub_["win_hit_groups"]) != 10:
        fail("win_hit group counts drift (10 base / 25 scen)")
    got_qb = sorted((w["first"], w["third"], w["fourth"], w["reply"]) for w in ub_["win_hit_groups"])
    base_scal = sorted((w["first"], w["third"], w["fourth"], w["reply"],
                        w["s4_class_index"], w["unknown_s5_children"])
                       for w in ub_["win_hit_groups"])
    scen_scal = sorted((w["first"], w["third"], w["fourth"], w["reply"],
                        w["s4_class_index"], w["unknown_s5_children"])
                       for w in ua_["win_hit_groups"])
    if got_qb != sorted(WIN_HIT_QUARTETS_BASE):
        fail(f"base win_hit quartets drift: {got_qb}")
    if any(w["s4_class_index"] != 30354 or w["unknown_s5_children"] != 97
           for w in ub_["win_hit_groups"]):
        fail("base win_hit groups must all be class 30354 with 97 recorded children")
    expected_scen = sorted(base_scal + WIN_HIT_NEW_15)
    if scen_scal != expected_scen:
        fail(f"scen win_hit group table drift: {scen_scal}")
    if (sb["class_status_counts"], sa["class_status_counts"]) != (CENSUS_BEFORE, CENSUS_AFTER):
        fail("published status counts mismatch the pinned censuses")

    # --- per-root coverage comparison ------------------------------------------
    def read_prc(p):
        return {r["first"]: r for r in csv.DictReader(open(p))}

    pb_, pa_ = read_prc(BASE_OUT / "per-root-coverage.csv"), \
        read_prc(DOSSIER / "reaudit/output/per-root-coverage.csv")
    if set(pb_) != set(pa_) or len(pb_) != 20:
        fail("per-root root set drift")
    greedy_delta = {}
    for rt in pb_:
        b, a = pb_[rt], pa_[rt]
        for f in ("role", "thirds", "free_now", "uncovered"):
            if b[f] != a[f]:
                fail(f"per-root {f} churn at root {rt}")
        if b["individual_greedy_union"] != a["individual_greedy_union"]:
            greedy_delta[int(rt)] = (int(b["individual_greedy_union"]),
                                     int(a["individual_greedy_union"]))
    if {k: v for k, v in sorted(greedy_delta.items())} != \
            {k: v for k, v in sorted(GREEDY_DELTA.items())}:
        fail(f"greedy root deltas drift: {greedy_delta}")
    if (sb["joint_greedy"]["greedy_union_size"], sa["joint_greedy"]["greedy_union_size"]) != JOINT_GREEDY:
        fail("joint greedy drift")
    if sb["joint_greedy"]["unique_groups"] != sa["joint_greedy"]["unique_groups"] != 2115:
        fail("unique groups drift")
    if (sb["group_best_options_nonfree"], sa["group_best_options_nonfree"]) != GROUP_BEST_NONFREE:
        fail("group best options drift")
    if (sb["worklist_total"], sa["worklist_total"]) != WORKLIST_TOTAL:
        fail("worklist total drift")
    if sb["board_verification"]["board_verified_free"] != 39 or \
            sa["board_verification"]["board_verified_free"] != 39 or \
            sb["board_verification"]["rejected"] != {} or \
            sa["board_verification"]["rejected"] != {}:
        fail("Board verification drift")

    # --- dossier census measurement cross-comparison ---------------------------
    cj = json.loads(CENSUSJSON.read_text())
    if cj["base_cache"]["sha256"] != BASE_CACHE_SHA or cj["scen_cache"]["sha256"] != SCEN_CACHE_SHA:
        fail("census-deltas cache pin drift")
    if (cj["base_cache"]["rows"], cj["base_cache"]["win"], cj["base_cache"]["loss"]) != (6767, 188, 6579) or \
            (cj["scen_cache"]["rows"], cj["scen_cache"]["win"], cj["scen_cache"]["loss"]) != (6771, 192, 6579):
        fail("census-deltas cache accounting drift")
    if cj["increment"]["sha256"] != DOSSIER_INCR_SHA:
        fail("census-deltas increment pin drift (must be the superseded dossier increment)")
    if cj["base_summary"]["sha256"] != BASE_SUMMARY_SHA or cj["base_closure"]["sha256"] != BASE_CLOSURE_SHA or \
            cj["scen_summary"]["sha256"] != SCEN_SUMMARY_SHA or cj["scen_closure"]["sha256"] != SCEN_CLOSURE_SHA:
        fail("census-deltas input summary/closure pin drift")
    if cj["census_recount_base"] != CENSUS_BEFORE or cj["census_recount_scen"] != CENSUS_AFTER:
        fail("census-deltas recount drift")
    if cj["verdict"]["census_counts_identical_to_published_summaries"] is not True or \
            cj["per_root_free_and_uncovered_identical"] is not True:
        fail("census-deltas identity flags drift")
    for f in cj["status_flips"]:
        if list(f["class_mask"]) != list(s4_masks[f["class_index"]]):
            fail(f"census-deltas flip class_mask drift at {f['class_index']}")
    if sorted(f["class_index"] for f in cj["status_flips"]) != sorted(FLIP_CLASSES) or \
            any(f["base"] != "unknown" or f["scen"] != "excluded_now" for f in cj["status_flips"]):
        fail("census-deltas flip set drift")
    cu = {e["class_index"]: (str(e["base"]), str(e["scen"])) for e in cj["closure_churn"]["unknown_now_churn"]}
    cr = {e["class_index"]: (int(e["base"]), int(e["scen"])) for e in cj["closure_churn"]["rank_churn"]}
    if cu != CLOSURE_UNKNOWN_CHURN or cr != CLOSURE_RANK_CHURN:
        fail("census-deltas closure churn drift")
    if cj["closure_churn"]["rows_base"] != 805 or cj["closure_churn"]["rows_scen"] != 805 or \
            cj["closure_churn"]["left"] != [] or cj["closure_churn"]["entered"] != []:
        fail("census-deltas closure rows drift")
    cgd = {e["first"]: (e["individual_greedy_union_base"], e["individual_greedy_union_scen"])
           for e in cj["per_root_greedy_delta"]}
    if cgd != GREEDY_DELTA:
        fail("census-deltas per-root greedy drift")
    if any(e["free_now"] != int(pb_[str(e["first"])]["free_now"]) or
           e["uncovered"] != int(pb_[str(e["first"])]["uncovered"])
           for e in cj["per_root_greedy_delta"]):
        fail("census-deltas per-root free/uncovered record drift")
    if (cj["joint_greedy"]["base"], cj["joint_greedy"]["scen"]) != JOINT_GREEDY:
        fail("census-deltas joint greedy drift")
    if (cj["worklist_total"]["base"], cj["worklist_total"]["scen"]) != WORKLIST_TOTAL:
        fail("census-deltas worklist drift")
    if (cj["update8_refresh_base"]["resolved"], cj["update8_refresh_scen"]["resolved"]) != UPD8["resolved"] or \
            (cj["update8_refresh_base"]["remaining"], cj["update8_refresh_scen"]["remaining"]) != UPD8["remaining"] or \
            (cj["update8_refresh_base"]["groups_free_now"], cj["update8_refresh_scen"]["groups_free_now"]) != UPD8["free_groups"]:
        fail("census-deltas update8 drift")
    if cj["update8_refresh_base"]["win_hit_groups"] != 10 or \
            cj["update8_refresh_scen"]["win_hit_groups"] != 25:
        fail("census-deltas win_hit counts drift")
    cnew = sorted(tuple(e) for e in cj["win_hit_groups_only_scen"])
    if cnew != sorted(tuple(q[:5]) for q in WIN_HIT_NEW_15):
        fail("census-deltas new win_hit quartets drift")
    if cj["win_hit_groups_identical"] is not False or cj["win_hit_groups_only_base"] != []:
        fail("census-deltas must record zero base-only win_hit groups")
    if cj["verdict"]["canonical_head_sha256"] != BASE_CACHE_SHA or \
            cj["verdict"]["part_ev_declared"] is not False or \
            cj["verdict"]["consumed"] != "NOTHING" or \
            "UNKNOWN" not in cj["verdict"]["note"]:
        fail("census-deltas verdict-scope fields drift (dossier-time scope)")
    wr = cj["worklist_regen_pins"]
    if wr["base"]["sha256"] != BASE_WORKLIST_SHA or wr["scen"]["sha256"] != SCEN_WORKLIST_SHA or \
            wr["base"]["size"] != 3717712 or wr["scen"]["size"] != 3717416:
        fail("census-deltas worklist regen pin drift")
    ak = cj["adopted"]
    if sorted(ak) != sorted(ADOPTED_IDS):
        fail("census-deltas adopted table ids drift")
    for kid in ADOPTED_IDS:
        rec = ak[kid]
        if (rec["lo"], rec["hi"], rec["nodes"]) != \
                (ADOPTED[kid][1], ADOPTED[kid][2], ADOPTED_ROW_NODES[kid]) or \
                rec["class_index"] != ADOPTED_CLASS[kid] or \
                rec["s5_index"] != ADOPTED[kid][0]:
            fail(f"census-deltas adopted table drift: {kid}")
        if sorted(rec["owner_classes"]) != OWNER_SETS[kid] or rec["owner_count"] != len(OWNER_SETS[kid]):
            fail(f"census-deltas adopted owner set drift: {kid}")
        if sum(1 for c in OWNER_SETS[kid] if cb[c][0] == "unknown") != rec["unknown_before"] or \
                sum(1 for c in OWNER_SETS[kid] if ca[c][0] == "unknown") != rec["unknown_after"]:
            fail(f"census-deltas adopted unknown owner count drift: {kid}")
        for orow in rec["owner_class_rows"]:
            c = orow["class_index"]
            if orow["cost_size"] != len(s4_cost[c]) or \
                    orow["base_status"] != cb[c][0] or orow["scen_status"] != ca[c][0]:
                fail(f"census-deltas adopted owner row drift: {kid} class {c}")

    # --- decomposition emission -------------------------------------------------
    flipped = {str(c): {"status_base": cb[c][0], "status_scen": ca[c][0],
                        "adopted_members": sorted(adopted_indices[j] for j in s4_cost[c]
                                                  if j in adopted_indices),
                        "cost_size": len(s4_cost[c]),
                        "cost_unknown_base": sum(1 for j in s4_cost[c] if known(j, base) is None),
                        "cost_unknown_scen": sum(1 for j in s4_cost[c] if known(j, scen) is None)}
               for c in FLIP_CLASSES}
    decomp = {
        "schema": "evwin4-decomp-deltas-v1",
        "part": "EV",
        "date": "2026-11-26",
        "base": {
            "cache_sha256": BASE_CACHE_SHA,
            "rows": 6767, "win": 188, "loss": 6579,
            "refresh_summary_sha256": BASE_SUMMARY_SHA,
            "closure_classes_sha256": BASE_CLOSURE_SHA,
            "per_root_coverage_sha256": BASE_PRC_SHA,
            "probe_worklist_sha256": BASE_WORKLIST_SHA,
            "class_status_counts": CENSUS_BEFORE,
        },
        "scen": {
            "cache_sha256": SCEN_CACHE_SHA,
            "cache_path_of_record": "research/experiments/n11-centralreply-evwin4-adoption-predecl-20261126/output/merged-exact-s5-chain-plus-evwin4-20261126.cache",
            "rows": 6771, "win": 192, "loss": 6579,
            "increment_sha256": INCR_SHA,
            "manifest_sha256": MANIFEST_SHA,
            "merge_audit_sha256": MERGE_AUDIT_SHA,
            "refresh_summary_sha256": SCEN_SUMMARY_SHA,
            "closure_classes_sha256": SCEN_CLOSURE_SHA,
            "per_root_coverage_sha256": SCEN_PRC_SHA,
            "probe_worklist_regen_pin_sha256": SCEN_WORKLIST_SHA,
            "probe_worklist_not_published_size_policy_bytes": 3717416,
            "class_status_counts": CENSUS_AFTER,
        },
        "dossier_supersession": {
            "dossier_increment_sha256": DOSSIER_INCR_SHA,
            "part_increment_sha256": INCR_SHA,
            "row_region_byte_identical": True,
            "merged_cache_byte_identical": True,
            "note": "the dossier increment header declared pre-declaration dossier status; the Part-emitted increment supersedes it with the Part EV adoption header; the 4 s5verdict rows are byte-identical and the merged scenario cache of record carries the published dossier sha 63f33c4f...",
        },
        "adopted": {
            "ids": list(ADOPTED),
            "nodes_total": ADOPTED_NODES,
            "classes": {"16757": 1, "20421": 1, "16371": 1, "12264": 1},
            "condition": "closure-batch 15M two-pass fresh-cold node-exact replica raws + EV C++ gate two-pass node-exact + third-impl a/b verdict-level corroboration (re-verified live by the Part maker; NO new solver pass ran)",
            "gate": "Part EV C++ second implementation, audit 0327dad8..., 7/7 GATE-PASS, 4/4 byte-identical audit re-runs",
        },
        "class_flips": {
            "count": 13,
            "direction": "unknown->excluded_now",
            "classes": flipped,
            "per_key_owner_classes": {k: sorted(owners[k]) for k in sorted(owners)},
            "owner_union_nonflip_classes": {"30345": "excluded_now (EP flip via ai048; EU chain carried)"},
        },
        "closure_classes": {
            "rows_before_after": list(CLOSURE["rows"]),
            "left_rows": [],
            "entered_rows": [],
            "rank_churn": {str(k): list(v) for k, v in sorted(CLOSURE_RANK_CHURN.items())},
            "rank_churn_nature": "16371 rises 4->1 (unknown_now 2->1, full 52-child class excluded); 12264 falls 13->11 displacing 30118/13342/23101/1849/2251 by one each; no renumbering elsewhere",
            "unknown_churn": {str(k): list(v) for k, v in sorted(CLOSURE_UNKNOWN_CHURN.items())},
            "groups_served_churn": {},
        },
        "frozen_update8": {
            "union_baseline": 31859,
            "resolved": list(UPD8["resolved"]),
            "remaining_now": list(UPD8["remaining"]),
            "groups_free_now": list(UPD8["free_groups"]),
            "win_hit_groups_base_identical": [
                {"first": w[0], "third": w[1], "fourth": w[2], "reply": w[3],
                 "s4_class_index": 30354, "unknown_s5_children": 97}
                for w in WIN_HIT_QUARTETS_BASE],
            "win_hit_groups_new_15": [
                {"first": q[0], "third": q[1], "fourth": q[2], "reply": q[3],
                 "s4_class_index": q[4], "unknown_s5_children": q[5]}
                for q in WIN_HIT_NEW_15],
            "win_hit_delta_note": "10 base groups (all class 30354, recorded unknown_s5_children 97) stay identical; EXACTLY 15 new groups join, all quartets of classes 12264 (6) / 16757 (5) / 20421 (4); zero groups removed",
        },
        "per_root": {
            "free_now_uncovered": "identical at all 20 rows incl. baseline; no coverage claim",
            "greedy_union_changes": {str(k): list(v) for k, v in sorted(GREEDY_DELTA.items(), key=lambda kv: int(kv[0]))},
            "joint_greedy": list(JOINT_GREEDY),
            "group_best_options_nonfree": list(GROUP_BEST_NONFREE),
            "worklist_total": list(WORKLIST_TOTAL),
        },
        "class_records": {str(cls): rec for cls, rec in sorted(cls_records.items())},
        "dossier_census_crosscheck": {
            "measurement_sha256": CENSUSJSON_SHA,
            "agreement": "EXACT on census counts, 13 flips, closure churn, per-root greedy deltas, joint greedy, worklist totals, update8 numbers, the 15 new win_hit quartets and both cache identities",
            "superseded_scope_fields": "verdict.consumed=NOTHING / part_ev_declared=false describe the dossier-time status and are superseded by this Part declaration; not asserted",
        },
        "honesty": {
            "fourth_win_adoption": True,
            "no_root_verdict": "no root verdict is asserted or implied by any class flip",
            "exclusion_effect": "13 classes become excluded (known WIN cost child ends free all-LOSS coverage): joint greedy 36,619 -> 36,618, worklist shrinks 64,307 -> 64,302 (-5), individual greedy shrinks at 6 roots (0: -191, 36: -54, 12: -2, 5: -1, 48: -2, 37: -1): scheduling bookkeeping only",
            "unknown_still": "34,417 S4 classes remain status-unknown; 11x11 stays UNKNOWN",
            "unconsumed": "the 21 closure-batch LOSS rows, k04 and every other unconsumed probe-level WIN stay in NO cache; no root, no root class and no closure class verdict is asserted",
        },
    }
    DECOMP_OUT.write_text(json.dumps(decomp, indent=1, ensure_ascii=False) + "\n",
                          encoding="utf-8")
    print("EV decomp OK: flips=13 caches=6767->6771 win=188->192 closure_left=[] "
          "greedy=36619->36618 worklist=64307->64302")
    print(f"decomp sha={sha(DECOMP_OUT)}")
    print(f"maker sha={MAKER_SHA}")


if __name__ == "__main__":
    main()
