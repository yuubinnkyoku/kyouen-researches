#!/usr/bin/env python3
"""BASE (canonical chain through the Part EM emloss21 loss-only adoption,
head of record 6e49dd84... 6,792 rows WIN 192 / LOSS 6,600) vs SCENARIO
(sixthwin5 = Part EW WIN-only canonical adoption: the 5 UNCONSUMED
sixth-cost exclusive-probe exact-WIN rows k02/k03/k04/k05/k08).

Fork of the published Part EM extractor
`compare_deltas_em_adoption.py` (sha256
b9a74915d0aa5690898f64b6fae5eeba8c87ebcb761dd7cdc680bdeb8c8f228c;
structural clone, disclosed diff: the adopted-rows table, both refresh
sides, the manifest decomposition fields, the census flip expectations
(WIN-side win-hit flips replace the loss-only zero-flip assertion),
the serving-class status expectations, the dossier-supersession /
dossier-maker re-execution sections and the pinned expectations are
Part-EW specific).

Fail-closed machine recomputation of exactly what the Part EW
sixthwin5 canonical WIN adoption changed, from published bytes only:

* every artifact sha-pinned (BASE = the published Part EM pre-declaration
  dossier outputs -- the merged canonical cache 6e49dd84... 6,792 rows
  WIN 192 / LOSS 6,600, the reaudit outputs refresh-summary 7f379b71...
  / closure-classes 68628134... / per-root-coverage 9c5b2774... and
  worklist regen pin 147b62d6... 3,715,963 B; SCEN = the published
  sixthwin5 pre-declaration dossier outputs -- the scenario merged cache
  16a12390... 6,797 rows WIN 197 / LOSS 6,600, the dossier increment
  44c16a28... (pre-declaration header, superseded row-exactly by the
  Part-emitted increment efee7b9e...), the reaudit outputs
  refresh-summary 295027cf... / closure-classes 350e269a... /
  per-root-coverage 9c5b2774... and worklist regen pin 82f9e517...
  3,715,904 B; the Part EW kit outputs -- increment efee7b9e...,
  increments-manifest a7376780... (schema
  sixthwin5-adoption-increments-manifest-v1), merge-audits x3 (identical
  sha b404c248...), the maker (structural clone of the published
  dossier maker 424edee4...), the byte-clone of the union merger
  90711961... and both refresh forks (the published Part EM dossier
  refresh cc01b3d8... and the published sixthwin5 dossier refresh fork
  92a884c9..., itself a byte-clone of cc01b3d8... differing in EXACTLY
  the three declared regions: docstring, CACHE path, expected cache
  sha; the computation region is byte-identical), the frozen
  graph/update8/board/policy/quarantine pins, the published Part EM
  kit increment 3e6e9bf0... and the dossier census measurement
  census-deltas-sixthwin5-predecl.json fd684d83...); both
  probe-worklists are UNPUBLISHED per the size policy - they enter ONLY
  as regen pins re-verified by the byte-verbatim refresh re-execution;
* BOTH published refresh forks are RE-EXECUTED byte-verbatim in isolated
  scratch trees against their pinned inputs, and all eight outputs must
  be byte-identical to the published / regenerated pins before any
  delta is emitted (double determinism; this simultaneously re-proves
  the published reaudit outputs of both sides are regenerable from
  published bytes);
* the published dossier maker make_increments_sixthwin5.py
  (424edee4...) is RE-EXECUTED byte-verbatim in an isolated scratch
  tree: rc=0 and byte-identical reproduction of its pinned outputs
  (increment 44c16a28... and manifest 25defefa...) is required before
  any delta is emitted - this re-proves live, from published bytes
  only, the entire Part EW adopt-eligibility evidence chain the dossier
  maker encodes (probe-kit direct pins - README, selection JSON, the
  k08 win-finding JSON, status.log, 5 target input CSVs and all 20
  raw CSV files, Part SK gate kit MANIFEST 8d84b1a5... 46/46
  file-by-file with the 178-gate table and 11 GATE-PASS rows, the TI
  kit audit gates for k03/k04/k05/k08, the ea73c3e3 k02 4-run
  witness, the fresh-to-BASE / quarantine / canonical-safety gates and
  the adopted-table digest b6ea1bcc...);
* the Part-emitted increment efee7b9e... is row-for-row identical to
  the published dossier increment 44c16a28... (the superseded header
  comment block is the ONLY differing region); the recorded
  supersession: the canonical merged cache of record is the published
  dossier merged file 16a12390... and the Part merge audits
  (b404c248... x3, byte-identical) record exactly this output;
* SCEN cache == BASE cache rows + exactly the 5 Part increment rows
  (verdict agreement everywhere; 6,797 rows WIN 197 / LOSS 6,600); the
  adopted rows are ALL fresh exact-WIN rows (k02 15M 7,717,432, k03
  15M 9,255,414, k04 15M 9,433,024, k05 15M 13,397,611, k08 15M
  6,195,897; adopted node total 45,999,378; every row re-verified live
  against the published source bytes first by the Part maker and again
  here by the dossier-maker re-execution); NO adopted key intersects
  the Part EM kit increment 3e6e9bf0... (no re-adoption of any
  already-consumed row); the 3 standing unconsumed LOSS labels of the
  same ladder (k01 15M, k06 15M, k07 2M) are NOT consumed and the later
  third-impl batch WIN rows k13/k19 stay outside this Part;
* the independent full-class census (frozen graph s4_cost + update8
  receipts + cache verdicts, replicating the refresh status logic) must
  reproduce the published class status counts EXACTLY on both sides
  (BASE 34,417/103/39/390 -> SCEN 34,409/111/39/390) with EXACTLY 8
  status flips, ALL of them unknown -> excluded_now by the win-hit
  mechanism, and the flipped set must be EXACTLY the owner classes of
  the 5 adopted keys that were unknown at BASE (774, 1387, 2169, 2339,
  3077, 16734, 25845, 30329; measured set equality); NO class is freed
  and NO class moves in any other direction;
* serving-class Board arithmetic recomputed from the frozen graph:
  class 3077 (raw boundary 108, cost size 100) cost-unknown 100 -> 95
  (exactly the 5 adopted keys, all owned there; its status flips
  unknown -> excluded_now by the win-hit mechanism);
* per-key owner class sets recomputed from the frozen graph must equal
  the published dossier census measurement's owner_classes row-for-row
  (owner-class count histogram EXACTLY {2 owners: 2 keys, 3 owners: 3
  keys});
* closure-classes.csv: ZERO rows leave, ZERO rows enter (804 -> 804);
  the unknown_now churn is exactly {16734: 92 -> 91} (the other 7
  flipped owner classes are not ranked closure candidates) and the
  class_rank churn recomputed from the two published CSVs must be
  EMPTY (0 re-ranked rows; NO rank churn); NO groups_served churn
  anywhere; every other field of every common row is byte-identical;
* update8 refresh: resolved 280 -> 281 (the newly resolved set is
  EXACTLY the single adopted s5 index k02/64872, the only adopted key
  inside the frozen update8 baseline requirement; the other four
  adopted keys - 39127, 91506, 96472, 112201 - were first probed
  AFTER the baseline froze and are correctly not in it - measured,
  disclosed), remaining 31,445 unchanged, groups_free_now stays 131,
  union baseline stays 31,859, win_hit groups 25 -> 25 IDENTICAL sets
  (this WIN adoption adds no win_hit group and removes none);
* per-root coverage: free_now/uncovered third columns IDENTICAL at all
  20 roots (per-root-coverage.csv byte-identical on both sides);
  Board verification 39/39 with zero rejections on both sides; the
  individual greedy union is IDENTICAL at all 20 roots (zero
  greedy-union changes, matching the published dossier measurement);
* the frozen greedy scheduler deltas are recorded as bookkeeping (joint
  greedy 35,155 -> 35,155 UNCHANGED; unique groups 2,115 -> 2,115;
  group_best_options_nonfree 2,101 -> 2,101; worklist 64,277 -> 64,276
  (-1 = exactly the one newly resolved in-requirement key));
* the published dossier census measurement fd684d83... is machine
  cross-compared field-by-field against this independent recount
  (census counts on both sides, the 8-flip set, closure churn, joint
  greedy, worklist totals, update8 numbers incl. the single-key
  newly-resolved set and the 4 out-of-baseline keys, win_hit identity,
  serving-class records, owner histogram, the adopted table and both
  cache identities): agreement must be EXACT.  The dossier verdict
  scope fields (consumed NOTHING, part_declared false) describe the
  dossier-time status and are superseded by the Part EW declaration
  (disclosed, not asserted).

No unknown verdict is asserted anywhere.  The standard 11x11 empty board
and every central-reply root stay UNKNOWN; free_now / coverage
quantities are scheduling bookkeeping derived from exact verdicts, not
root verdict claims.  Consuming the 5 WIN labels transfers NO verdict to
any root: owner classes leave live status by the win-hit mechanism only.
The standard 11x11 empty board and every one of the 19 central-reply
roots stay UNKNOWN unless and until the required S5 children are all
exact LOSS; nodes are bookkeeping, never verdicts.
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

# BASE side = the published Part EM pre-declaration dossier kit (head of
# record = Part EM head merged-exact-s5-chain-plus-emloss21 6e49dd84...).
BASE_EXP = ROOT / "research/experiments/n11-centralreply-emloss21-adoption-predecl-20261126"
BASE_OUT = BASE_EXP / "reaudit/output"
BASE_CACHE = BASE_EXP / "output/merged-exact-s5-chain-plus-emloss21-20261126.cache"
# SCEN side = the published sixthwin5 pre-declaration dossier kit.
DOSSIER = ROOT / "research/experiments/n11-centralreply-sixthwin5-adoption-predecl-20261126"
SCEN_CACHE = DOSSIER / "output/merged-exact-s5-chain-plus-sixthwin5-20261126.cache"
INCR = EXP / "output/increment-sixthwin5-adoption-20261126.cache"
MANIFEST = EXP / "output/increments-manifest.json"
CENSUSJSON = DOSSIER / "output/census-deltas-sixthwin5-predecl.json"
DOSSIER_INCR = DOSSIER / "output/increment-sixthwin5-20261126.cache"
DOSSIER_MANIFEST = DOSSIER / "output/increments-manifest.json"
DOSSIER_MAKER = DOSSIER / "scripts/make_increments_sixthwin5.py"
EM_PART = ROOT / "research/experiments/n11-centralreply-emloss21-adoption-reaudit-20261126"
EM_INCREMENT = EM_PART / "output/increment-emloss21-adoption-20261126.cache"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_REFRESH_SCRIPT = BASE_EXP / "reaudit/scripts/refresh_adoption_emloss21.py"
SCEN_REFRESH_SCRIPT = DOSSIER / "reaudit/scripts/refresh_adoption_sixthwin5.py"
MERGER = EXP / "scripts/s5_union_merge.py"
MAKER = EXP / "scripts/make_increments_sixthwin5_adoption.py"
DECOMP_OUT = EXP / "output/decomp-deltas-sixthwin5-adoption.json"

# ---- pins ------------------------------------------------------------------
BASE_CACHE_SHA = "6e49dd841b7bfcb335d86ef2479c95f47ab7acbcf41ace389a8b8eb95c778c9d"
SCEN_CACHE_SHA = "16a12390c0c3f046f0ae537b2a9940e15661263fc5034ce1b155c138bb9043cd"
INCR_SHA = "efee7b9e3b377aabbd5cb3606b84739be7f87aff8ddd4bffafc9d22fa557e6be"
MANIFEST_SHA = "a7376780687fbacb0a9a958a94de0df4634d4512bb08d1631b36772a9c78ba86"
MAKER_SHA = None  # asserted at run (the maker bytes are pinned by the wave-B/C MANIFEST)
DOSSIER_INCR_SHA = "44c16a28f944e255d3968f49a16cc61e06f70269ada833fe976f1607b7d40b03"
DOSSIER_MANIFEST_SHA = "25defefac25a9a527b4de90408fe1dddcd13a19f29128a07afbab69f4e66e39f"
DOSSIER_MAKER_SHA = "424edee4116ab785376d5fe5d197599b1574b71a46cf847d90a291dd27f99558"
CENSUSJSON_SHA = "fd684d83c689452f0da7dca2ec2cb5b6501f03b9f5d2b30c30fbcf0590f5ba5f"
BASE_SUMMARY_SHA = "7f379b718e48330c5acbc3c9c79be3c4fb6d616c4dc7bedfe7691e6ebb225f0b"
BASE_CLOSURE_SHA = "6862813431dd1abbaba81ac2a720385be394ce774f259b8001ca49630fc4a8e2"
BASE_PRC_SHA = "9c5b277429f99157ff2e65323b5912b9ce957f1d2008f8ac8fc1e03b49f91ad1"
BASE_WORKLIST_SHA = "147b62d643ba9039e9e2b64363cec602405bf11210a3aa4cfd9084eb0df3a973"
SCEN_SUMMARY_SHA = "295027cf9a3fd7eb4e74b2008f4794cc146f0ee769901db056e7e176a38deb3a"
SCEN_CLOSURE_SHA = "350e269a9d4e0827274aff7c587cdb389f070eade0ff54c220c7c14f9197bc6d"
SCEN_PRC_SHA = "9c5b277429f99157ff2e65323b5912b9ce957f1d2008f8ac8fc1e03b49f91ad1"
SCEN_WORKLIST_SHA = "82f9e51798172d1e3a38cbc215b7230135bddd09d911ab672397264560e67cc7"
BASE_REFRESH_SHA = "cc01b3d8772a9e6fe0c5718ed0715b7c927c5ab149444690329c6e19c57e2131"
SCEN_REFRESH_SHA = "92a884c9b80f402a580c1545f7db882e26eaeb58becb5fe6686a8bbb7e70ec21"
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
MERGE_AUDIT_SHA = "b404c2483988daac71c88de54f29962cfea90ab5b4c85fbf81697d5dab4e720a"
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
BOARD_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
EM_INCREMENT_SHA = "3e6e9bf0a5f410a1d584889832f21352dd01a97aef5a899de06a28373fcaef82"
ADOPTED_TABLE_DIGEST = "b6ea1bcc10829498add9c87bb874b18dd95904ddf83f022ee67af06c06d93b0c"
MERGED_COMMENT = "# S5 solver-trusted exact; base=merged-exact-s5-after-js-probe-13.cache (sha256 60e0dc3476920d4e...); increment=101 fresh rows (99 canonical S5 children of S4 1297036692683752448:0 absent from the chain, 2 unclaimed backward-only rows, 1 S6-witness-derived TARGET_S5 row nodes=0); see merge-manifest.json"

# ---- adopted table (Part EW) -----------------------------------------------
# id -> (s5_index, lo, hi, nodes, serving_class); order = sorted (lo, hi),
# the manifest adopted_table / increment row order.
ADOPTED = {
    "k02": (64872, 1297036692683751424, 68157440, 7717432, 3077),
    "k03": (96472, 10376293541461626880, 65792, 9255414, 3077),
    "k04": (112201, 10376293541461626888, 65536, 9433024, 3077),
    "k05": (91506, 10376293541461757952, 65536, 13397611, 3077),
    "k08": (39127, 10376293610182148096, 68719476736, 6195897, 3077),
}
ADOPTED_IDS = sorted(ADOPTED, key=lambda k: (ADOPTED[k][1], ADOPTED[k][2]))
ADOPTED_NODES = 45999378
OUTSIDE_BASELINE_IDS = ["k08", "k05", "k03", "k04"]  # s5 39127/91506/96472/112201
IN_BASELINE_IDS = ["k02"]  # s5 64872
CENSUS_BASE = {"unknown": 34417, "excluded_now": 103, "free_now": 39, "excluded": 390}
CENSUS_SCEN = {"unknown": 34409, "excluded_now": 111, "free_now": 39, "excluded": 390}
STATUS_FLIPS = [774, 1387, 2169, 2339, 3077, 16734, 25845, 30329]
OWNER_HIST = {3: 3, 2: 2}
SERVING_CHECKS = {
    3077: {"raw_boundary": 108, "cost_size": 100, "unknown_base": 100,
           "unknown_scen": 95, "members": ["k02", "k03", "k04", "k05", "k08"]},
}
CLOSURE = {"rows": (804, 804), "left": [], "entered": []}
CLOSURE_UNKNOWN_CHURN = {16734: (92, 91)}
RANK_CHURN_EXPECTED = 0
UPD8 = {"resolved": (280, 281), "remaining": (31445, 31445), "free_groups": (131, 131)}
UNION_BASELINE = 31859
WIN_HIT = (25, 25)
GREEDY_DELTA = {}
JOINT_GREEDY = (35155, 35155)
UNIQUE_GROUPS = (2115, 2115)
GROUP_BEST_NONFREE = (2101, 2101)
WORKLIST_TOTAL = (64277, 64276)
BOARD_VERIFIED = (39, 39)


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


def rerun_dossier_maker(tmp_name: str):
    """Re-execute the published sixthwin5 dossier maker byte-verbatim in a
    scratch tree; require rc=0 and byte-identical reproduction of its
    pinned outputs (increment 44c16a28..., manifest 25defefa...).  This
    re-proves the entire sixthwin5 dossier adopt-eligibility evidence
    chain live."""
    if sha(DOSSIER_MAKER) != DOSSIER_MAKER_SHA:
        fail("dossier maker sha drift")
    scratch = ROOT / "research/experiments" / tmp_name
    if scratch.exists():
        shutil.rmtree(scratch)
    (scratch / "scripts").mkdir(parents=True)
    shutil.copyfile(DOSSIER_MAKER, scratch / "scripts" / DOSSIER_MAKER.name)
    if sha(scratch / "scripts" / DOSSIER_MAKER.name) != DOSSIER_MAKER_SHA:
        fail("scratch copy of dossier maker not byte-identical")
    merger_pin = DOSSIER / "scripts/s5_union_merge.py"
    if sha(merger_pin) != MERGER_SHA:
        fail("dossier merger pin drift")
    shutil.copyfile(merger_pin, scratch / "scripts" / "s5_union_merge.py")
    if sha(scratch / "scripts" / "s5_union_merge.py") != MERGER_SHA:
        fail("scratch copy of merger not byte-identical")
    proc = subprocess.run([sys.executable, str(scratch / "scripts" / DOSSIER_MAKER.name)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        fail(f"dossier maker re-execution failed: {proc.stderr[-400:]}")
    outs = {}
    for name, want in (("increment-sixthwin5-20261126.cache", DOSSIER_INCR_SHA),
                       ("increments-manifest.json", DOSSIER_MANIFEST_SHA)):
        p = scratch / "output" / name
        if not p.is_file():
            fail(f"dossier maker re-execution missing output {name}")
        if sha(p) != want:
            fail(f"dossier maker re-execution output drift: {name}")
        outs[name] = p
    return outs


def main() -> None:
    global MAKER_SHA
    MAKER_SHA = sha(MAKER)
    pins = [
        ("base cache", BASE_CACHE, BASE_CACHE_SHA),
        ("scenario cache", SCEN_CACHE, SCEN_CACHE_SHA),
        ("increment", INCR, INCR_SHA),
        ("manifest", MANIFEST, MANIFEST_SHA),
        ("maker", MAKER, MAKER_SHA if MAKER_SHA else sha(MAKER)),
        ("dossier increment (superseded)", DOSSIER_INCR, DOSSIER_INCR_SHA),
        ("dossier manifest", DOSSIER_MANIFEST, DOSSIER_MANIFEST_SHA),
        ("dossier maker", DOSSIER_MAKER, DOSSIER_MAKER_SHA),
        ("dossier census measurement", CENSUSJSON, CENSUSJSON_SHA),
        ("prior Part EM kit increment (re-adoption guard)", EM_INCREMENT, EM_INCREMENT_SHA),
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
    if manifest["schema"] != "sixthwin5-adoption-increments-manifest-v1":
        fail("manifest schema drift")
    if manifest["part"] != "EW" or manifest["date"] != "2026-11-26":
        fail("manifest part/date drift")
    if manifest["win_canonical_adoption"] is not True:
        fail("manifest win_canonical_adoption flag drift")
    if manifest["base_cache_sha256"] != BASE_CACHE_SHA:
        fail("manifest base cache pin drift")
    if manifest["sha256"]["win_increment"] != INCR_SHA:
        fail("manifest win_increment pin drift")
    if manifest["merger_sha256"] != MERGER_SHA:
        fail("manifest merger pin drift")
    if manifest["base_cache_rows"] != 6792:
        fail("manifest base rows drift")
    if manifest["base_cache_win_loss"] != [192, 6600]:
        fail("manifest base win/loss drift")
    if manifest["row_counts"] != {"adopted_win_rows": 5,
                                   "win_ties_consumed_elsewhere": 0,
                                   "standing_unconsumed_loss_rows": 3,
                                   "prior_canonical_rows_base": 6792}:
        fail("manifest row_counts drift")
    if manifest["resolved_ids"] != ADOPTED_IDS or manifest["win_ids"] != ADOPTED_IDS:
        fail("manifest adopted/target ids drift")
    if manifest["loss_ids"] != []:
        fail("manifest must adopt no LOSS row (WIN-only Part)")
    if manifest["adopted_nodes_total"] != ADOPTED_NODES:
        fail("manifest adopted node total drift")
    if manifest["adopted_table_digest_sha256"] != ADOPTED_TABLE_DIGEST:
        fail("manifest adopted-table digest drift")
    if manifest["quarantine_hits"] != 0:
        fail("manifest quarantine hits drift")
    if manifest["base_cache_absent_hits_for_emitted"] != 0:
        fail("manifest base-absent hits drift")
    if manifest["win_ties"] != [] or \
            "unlike emloss21" not in manifest["win_ties_note"]:
        fail("manifest win-ties record drift (must record the no-tie fact)")
    ds = manifest["dossier_supersession"]
    if ds["dossier_increment_sha256"] != DOSSIER_INCR_SHA or \
            ds["dossier_manifest_sha256"] != DOSSIER_MANIFEST_SHA or \
            ds["dossier_maker_sha256"] != DOSSIER_MAKER_SHA or \
            ds["row_region_byte_identical"] is not True or \
            ds["merged_cache_sha256_of_record"] != SCEN_CACHE_SHA or \
            not ds.get("note"):
        fail("manifest dossier supersession drift")
    prov = manifest["provenance"]
    if prov["part_maker_reverified_live"] is not True or \
            prov["dossier_bytes_repinned"] is not True or \
            prov["probe_kit_direct_pins"] is not True or \
            prov["sk_kit_files_verified"] != 46 or \
            prov["ti_kit_pins_verified"] != 8 or \
            prov["raws_published"] is not True or \
            not prov.get("probe_fetch_anchor_note"):
        fail("manifest provenance drift")
    pools = {p["pool"]: p for p in manifest["pools"]}
    if sorted(pools) != ["ea73c3e3-third-impl-k02", "sixthcost-exclusive-probe",
                          "sk-cpp-second-implementation-gate",
                          "ti-third-implementation-audits"]:
        fail("manifest pool set drift")
    pprobe = pools["sixthcost-exclusive-probe"]
    if pprobe["adopted_win_ids"] != ADOPTED_IDS or \
            pprobe["budget"] != 15000000 or \
            pprobe["first_stage_budget"] != 2000000 or \
            pprobe["adopted_nodes"] != ADOPTED_NODES or \
            pprobe["standing_loss_ids_not_adopted"] != ["k01", "k06", "k07"]:
        fail("manifest probe pool drift")
    if pprobe["standing_loss_labels"] != {"k01": [15000000, 2, 10369650],
                                           "k06": [15000000, 2, 8182231],
                                           "k07": [2000000, 2, 1419823]}:
        fail("manifest standing LOSS labels drift")
    if len(pprobe["kit_integrity"]["raw_file_sha256_pins"]) != 20 or \
            len(pprobe["kit_integrity"]["input_csv_sha256_pins"]) != 5:
        fail("manifest probe raw/input pin count drift")
    psk = pools["sk-cpp-second-implementation-gate"]
    sk_ki = psk["kit_integrity"]
    if sk_ki["kit_files_verified"] != 46 or sk_ki["gate_rows_all_pass"] != 178 or \
            sk_ki["gate_status_gate_pass_rows"] != 11 or \
            sk_ki["kit_manifest_sha256"] != "8d84b1a58348b86a3bf8ca4b2d54c957b3c39683a745e52c5e33d2db19b5562a" or \
            sk_ki["gate_rows_json_sha256"] != "11fb829c10d489f90d9a05f322356168089a80bf1d0128343a054e14221d52d1" or \
            sk_ki["audit_run1_run2_run3_sha256_identical"] != sk_ki["audit_gate_json_sha256"] or \
            "Part SK kit" not in sk_ki["note"]:
        fail("manifest SK pool drift")
    pti = pools["ti-third-implementation-audits"]
    ti_ki = pti["kit_integrity"]
    if pti["covered_ids"] != ["k03", "k04", "k05", "k08"] or \
            ti_ki["kit_manifest_sha256"] != "538f8ec7e2a5eba71a4a1c4368d76ac1f5f2b77927759c6a26d592fde9c5342c" or \
            ti_ki["kit_manifest_lines"] != 344 or \
            ti_ki["third_impl_js_sha256"] != "08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998":
        fail("manifest TI pool drift")
    for kid in pti["covered_ids"]:
        if any(t[0] != "1" for t in ti_ki["determinism_triplets"][kid]):
            fail(f"manifest TI pool non-WIN determinism triplet for {kid}")
        rep_rows = [list(r) for r in ti_ki["replica_unanimous_rows"][kid]]
        if rep_rows and rep_rows[0] == ["0", "2000000"]:
            # k08 records the first-stage 2M incomplete run of the same
            # ladder raw before the three full-budget WIN replays
            rep_rows = rep_rows[1:]
        elif kid == "k08":
            fail("manifest TI k08 replica table must record the first-stage "
                 "2M incomplete marker")
        if len(rep_rows) != 3 or any(r[0] != "1" for r in rep_rows):
            fail(f"manifest TI pool non-WIN replica verdict rows for {kid}")
        nodesset = {int(r[1]) for r in rep_rows}
        if nodesset != {ADOPTED[kid][3]}:
            fail(f"manifest TI replica node drift for {kid}: {nodesset}")
    pea = pools["ea73c3e3-third-impl-k02"]
    ea_ki = pea["kit_integrity"]
    if pea["covered_ids"] != ["k02"] or ea_ki["witness_runs"] != 4 or \
            len(ea_ki["witness_sha256_pins"]) != 4 or \
            sorted(ea_ki["witness_sha256_pins"]) != ["out/witness/out-k02-a.txt",
                                                     "out/witness/out-k02-b.txt",
                                                     "out/witness/out-k02-g.txt",
                                                     "out/witness/out-k02-v.txt"] or \
            ea_ki["third_impl_js_sha256"] != ti_ki["third_impl_js_sha256"] or \
            "verdict-level agreement" not in pea["verdict_agreement_note"]:
        fail("manifest ea73c3e3 pool drift")
    sc = manifest["source_class"]
    if sc["serving_class_index"] != 3077 or sc["class"] != "10376293541461626880:65536" or \
            sc["class_children_total"] != 108 or sc["s5_unknown_before"] != 101 or \
            sc["unknown_exclusive"] != 43:
        fail("manifest source-class drift")
    rows = manifest["adopted_table"]
    if len(rows) != 5:
        fail("manifest adopted row count drift")
    if sum(r["nodes"] for r in rows) != ADOPTED_NODES:
        fail("manifest adopted node sum drift")
    for r in rows:
        kid = None
        for k, v in ADOPTED.items():
            if (v[1], v[2]) == (r["lo"], r["hi"]):
                kid = k
                break
        if kid is None:
            fail(f"manifest adopted row not in the pinned table: {r}")
        if (r["s5_index"], r["lo"], r["hi"], r["nodes"], r["serving_class"]) != \
                (ADOPTED[kid][0], ADOPTED[kid][1], ADOPTED[kid][2],
                 ADOPTED[kid][3], ADOPTED[kid][4]):
            fail(f"manifest adopted row field drift: {kid}")
        if r["result"] != 1:
            fail(f"manifest adopted row must be exact WIN: {kid}")
    if "interpretation_guard" not in manifest or "UNKNOWN" not in manifest["interpretation_guard"]:
        fail("manifest interpretation guard drift")

    # --- dossier supersession: Part increment rows == dossier increment rows ---
    if cache_row_list(INCR) != cache_row_list(DOSSIER_INCR):
        fail("Part increment rows differ from the dossier increment rows")
    if cache_row_list(INCR) != [f"s5verdict,{ADOPTED[k][1]},{ADOPTED[k][2]},5,1,{ADOPTED[k][3]}"
                                for k in ADOPTED_IDS]:
        fail("increment rows differ from the pinned adopted table order/bytes")

    # --- merge-audit decomposition --------------------------------------------
    for rn in ("merge-audit-run1.json", "merge-audit-run2.json", "merge-audit-run3.json"):
        a = json.loads((EXP / "output" / rn).read_text())
        if a["unique_rows"] != 6797 or a["duplicate_rows_elided"] != 0:
            fail(f"merge-audit row accounting drift: {rn}")
        if a["verdict_counts"] != {"WIN(1)": 197, "LOSS(2)": 6600}:
            fail(f"merge-audit verdict counts drift: {rn}")
        if a["nodes_field_mismatches_recorded"] != []:
            fail(f"merge-audit nodes mismatch drift: {rn}")
        if a["output_sha256"] != SCEN_CACHE_SHA or a["output_bytes"] != 284024:
            fail(f"merge-audit output identity drift: {rn}")
        if a["comments_kept_from_first_input"] != [MERGED_COMMENT]:
            fail(f"merge-audit comment block drift: {rn}")
        ins = a["inputs"]
        if len(ins) != 2 or ins[0]["sha256"] != BASE_CACHE_SHA or \
                ins[0]["rows"] != 6792 or ins[0]["unique_new"] != 6792:
            fail(f"merge-audit BASE input entry drift: {rn}")
        if ins[1]["sha256"] != INCR_SHA or ins[1]["rows"] != 5 or ins[1]["unique_new"] != 5:
            fail(f"merge-audit increment input entry drift: {rn}")
        if ins[1]["file"] != "output/increment-sixthwin5-adoption-20261126.cache":
            fail(f"merge-audit increment path drift: {rn}")
        if not ins[0]["file"].endswith(
                "n11-centralreply-emloss21-adoption-predecl-20261126/output/"
                "merged-exact-s5-chain-plus-emloss21-20261126.cache"):
            fail(f"merge-audit BASE path drift: {rn}")

    # --- refresh re-execution (both sides, byte-verbatim) --------------------
    base_tmp = rerun_refresh(BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA, ".ew-verify-base-emloss21")
    scen_tmp = rerun_refresh(SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA, ".ew-verify-scen-sixthwin5")
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
    shutil.rmtree(ROOT / "research/experiments/.ew-verify-base-emloss21")
    shutil.rmtree(ROOT / "research/experiments/.ew-verify-scen-sixthwin5")

    # --- dossier maker re-execution (the sixthwin5 dossier chain, live) -----
    maker_outs = rerun_dossier_maker(".ew-verify-dossier-maker")
    if sha(maker_outs["increment-sixthwin5-20261126.cache"]) != DOSSIER_INCR_SHA:
        fail("dossier maker re-execution increment drift (unreachable re-check)")
    shutil.rmtree(ROOT / "research/experiments/.ew-verify-dossier-maker")

    # --- frozen dependency graph + cache relation ---------------------------
    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s5_masks = g["s5_masks"]
    m2i_probe = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}
    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    incr = load_cache(INCR)
    if len(base) != 6792 or len(scen) != 6797 or len(incr) != 5:
        fail(f"cache sizes drift: base {len(base)} scen {len(scen)} incr {len(incr)}")
    adopted_keys = {(ADOPTED[k][1], ADOPTED[k][2]): k for k in ADOPTED}
    em_keys = set(load_cache(EM_INCREMENT))
    for key, row in incr.items():
        if row[0] != 1:
            fail(f"increment contains a non-WIN row: {key}")
        if key in base:
            fail(f"increment key already in BASE: {key}")
        if key not in adopted_keys:
            fail(f"increment key not in the adopted set: {key}")
        if key in em_keys:
            fail(f"adopted key also sits in the prior Part EM kit increment "
                  f"(re-adoption): {key}")
        if scen.get(key) != row:
            fail(f"increment row not taken verbatim into scenario cache: {key}")
    merged = dict(base)
    for key, row in incr.items():
        merged[key] = row
    if merged != scen:
        fail("scenario cache != BASE rows + increment rows (set difference)")
    wins = sum(1 for v in scen.values() if v[0] == 1)
    losses = len(scen) - wins
    if (wins, losses) != (197, 6600):
        fail(f"scenario verdict counts {wins}/{losses} != 197/6,600")
    if sums_nodes(incr) != ADOPTED_NODES:
        fail("increment node total drift")

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
    if dict(Counter(v[0] for v in cb.values())) != CENSUS_BASE:
        fail("independent census BASE recount drift vs the published counts")
    if dict(Counter(v[0] for v in ca.values())) != CENSUS_SCEN:
        fail("independent census SCEN recount drift vs the published counts")
    changed = sorted(i for i in cb if cb[i][0] != ca[i][0])
    if changed != STATUS_FLIPS:
        fail(f"WIN-adoption status flips {changed} != the dossier-measured flip set")
    for i in changed:
        if (cb[i][0], ca[i][0]) != ("unknown", "excluded_now"):
            fail(f"status flip at class {i} is not unknown -> excluded_now")
        if ca[i][2] is not True:
            fail(f"status flip at class {i} is not win-hit driven")
    owners = {}
    for i in range(len(s4_masks)):
        for j in s4_cost[i]:
            if j in adopted_indices:
                owners.setdefault(adopted_indices[j], []).append(i)
    if sorted(owners) != sorted(ADOPTED_IDS):
        fail("owner recomputation id set drift")
    hist = Counter(len(owners[k]) for k in owners)
    if dict(hist) != OWNER_HIST:
        fail(f"owner-class count histogram drift: {dict(hist)} != {OWNER_HIST}")
    owner_classes = {c for k in owners for c in owners[k]}
    if set(STATUS_FLIPS) - owner_classes:
        fail("a flipped class is not an owner class of any adopted key")
    nonflip = owner_classes - set(STATUS_FLIPS)
    if nonflip != {30354}:
        fail(f"owner classes outside the flip set drift: {sorted(nonflip)}")
    for c in nonflip:
        if cb[c][0] != "excluded_now" or ca[c][0] != "excluded_now":
            fail(f"non-flipped owner class {c} must stay excluded_now on both sides")

    # --- serving-class Board boundary arithmetic ----------------------------
    board = Board(11)

    def boundary(cls):
        lo, hi = s4_masks[cls]
        return {(c & ((1 << 64) - 1), c >> 64) for c in board.children(lo | (hi << 64))}

    serving_records = {}
    for cls, want in SERVING_CHECKS.items():
        kids = boundary(cls)
        if len(kids) != want["raw_boundary"]:
            fail(f"class-{cls} Board boundary {len(kids)} != {want['raw_boundary']}")
        cost = s4_cost[cls]
        if len(cost) != want["cost_size"]:
            fail(f"class-{cls} cost size {len(cost)} != {want['cost_size']}")
        own = sorted(adopted_indices[j] for j in set(cost) & set(adopted_indices))
        if own != sorted(want["members"]):
            fail(f"class-{cls} adopted members {own} != {sorted(want['members'])}")
        ub = sum(1 for j in cost if known(j, base) is None)
        ua = sum(1 for j in cost if known(j, scen) is None)
        if (ub, ua) != (want["unknown_base"], want["unknown_scen"]):
            fail(f"class-{cls} cost-unknown {ub}->{ua} != "
                 f"{want['unknown_base']}->{want['unknown_scen']}")
        if any(k in quarantined for k in kids):
            fail(f"a quarantined key sits inside the class-{cls} boundary")
        if cb[cls][0] != "unknown" or ca[cls][0] != "excluded_now":
            fail(f"serving class {cls} must flip unknown -> excluded_now "
                 "(win-hit by the 5 adopted rows, the dossier-measured "
                 "serving transition)")
        serving_records[cls] = {"class": cls, "boundary_raw": len(kids),
                                "cost_size": len(cost),
                                "cost_unknown_base": ub, "cost_unknown_scen": ua,
                                "adopted_members": own,
                                "status_base": cb[cls][0], "status_scen": ca[cls][0]}
    if serving_records[3077]["adopted_members"] != sorted(ADOPTED_IDS):
        fail("serving-class member assignment drift")

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
    if len(common) != 804:
        fail(f"closure common-row count {len(common)} != 804")
    churn = {"unknown": {}, "rank": {}, "groups": {}}
    for c in sorted(common):
        b, a = c_before[c], c_after[c]
        if b["unknown_now"] != a["unknown_now"]:
            churn["unknown"][c] = (int(b["unknown_now"]), int(a["unknown_now"]))
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
    if len(churn["rank"]) != RANK_CHURN_EXPECTED:
        fail(f"closure rank churn count {len(churn['rank'])} != {RANK_CHURN_EXPECTED}")
    if churn["groups"] != {}:
        fail(f"closure groups_served churn drift: {churn['groups']}")

    # --- update8 refresh comparison -------------------------------------------
    sb = json.loads((BASE_OUT / "refresh-summary.json").read_text())
    sa = json.loads((DOSSIER / "reaudit/output/refresh-summary.json").read_text())
    ub_, ua_ = sb["frozen_update8_refresh"], sa["frozen_update8_refresh"]
    if ub_["union_size_baseline"] != UNION_BASELINE or ua_["union_size_baseline"] != UNION_BASELINE:
        fail("update8 baseline drift")
    if (ub_["resolved_count"], ua_["resolved_count"]) != UPD8["resolved"]:
        fail("update8 resolved drift")
    if (ub_["remaining_now"], ua_["remaining_now"]) != UPD8["remaining"]:
        fail("update8 remaining drift")
    if (ub_["groups_free_now"], ua_["groups_free_now"]) != UPD8["free_groups"]:
        fail("update8 free groups drift")
    # win_hit groups: identical sets on both sides (measured; the WIN-only
    # adoption adds no win_hit group and removes none at the group level)
    if (len(ub_["win_hit_groups"]), len(ua_["win_hit_groups"])) != WIN_HIT:
        fail(f"win_hit group counts drift {WIN_HIT}")
    base_scal = sorted((w["first"], w["third"], w["fourth"], w["reply"],
                        w["s4_class_index"], w["unknown_s5_children"])
                       for w in ub_["win_hit_groups"])
    scen_scal = sorted((w["first"], w["third"], w["fourth"], w["reply"],
                        w["s4_class_index"], w["unknown_s5_children"])
                       for w in ua_["win_hit_groups"])
    if base_scal != scen_scal:
        fail("win_hit group sets differ across the adoption (measured-identical required)")
    if (sb["class_status_counts"], sa["class_status_counts"]) != (CENSUS_BASE, CENSUS_SCEN):
        fail("published status counts mismatch the pinned censuses")
    # the newly resolved set must be exactly k02's s5 index 64872 (the only
    # adopted key inside the frozen update8 baseline requirement)
    new_resolved = sorted(set(ua_["resolved_among_baseline_requirement"]) -
                          set(ub_["resolved_among_baseline_requirement"]))
    in_baseline = sorted(ADOPTED[k][0] for k in IN_BASELINE_IDS)
    if new_resolved != in_baseline or in_baseline != [64872]:
        fail(f"newly resolved update8 set drift: {new_resolved}")
    un_resolved = sorted(set(ub_["resolved_among_baseline_requirement"]) -
                         set(ua_["resolved_among_baseline_requirement"]))
    if un_resolved != []:
        fail(f"update8 resolved rows disappeared: {un_resolved}")
    outside = sorted(ADOPTED[k][0] for k in OUTSIDE_BASELINE_IDS)
    if outside != [39127, 91506, 96472, 112201]:
        fail("outside-baseline adopted s5 index set drift")
    if any(j in ub_["resolved_among_baseline_requirement"] or
           j in ua_["resolved_among_baseline_requirement"] for j in outside):
        fail("an outside-baseline adopted s5 index sits inside the frozen "
             "update8 baseline requirement (it was first probed after the "
             "baseline froze)")

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
    if greedy_delta != GREEDY_DELTA:
        fail(f"greedy root deltas drift: {greedy_delta}")
    if (sb["joint_greedy"]["greedy_union_size"], sa["joint_greedy"]["greedy_union_size"]) != JOINT_GREEDY:
        fail("joint greedy drift")
    if (sb["joint_greedy"]["unique_groups"], sa["joint_greedy"]["unique_groups"]) != UNIQUE_GROUPS:
        fail("unique groups drift")
    if (sb["group_best_options_nonfree"], sa["group_best_options_nonfree"]) != GROUP_BEST_NONFREE:
        fail("group best options drift")
    if (sb["worklist_total"], sa["worklist_total"]) != WORKLIST_TOTAL:
        fail("worklist total drift")
    if sb["board_verification"]["board_verified_free"] != BOARD_VERIFIED[0] or \
            sa["board_verification"]["board_verified_free"] != BOARD_VERIFIED[1] or \
            sb["board_verification"]["rejected"] != {} or \
            sa["board_verification"]["rejected"] != {}:
        fail("Board verification drift")

    # --- dossier census measurement cross-comparison ---------------------------
    cj = json.loads(CENSUSJSON.read_text())
    if cj["base_cache"]["sha256"] != BASE_CACHE_SHA or cj["scen_cache"]["sha256"] != SCEN_CACHE_SHA:
        fail("census-deltas cache pin drift")
    if (cj["base_cache"]["rows"], cj["base_cache"]["win"], cj["base_cache"]["loss"]) != (6792, 192, 6600) or \
            (cj["scen_cache"]["rows"], cj["scen_cache"]["win"], cj["scen_cache"]["loss"]) != (6797, 197, 6600):
        fail("census-deltas cache accounting drift")
    if cj["increment"]["sha256"] != DOSSIER_INCR_SHA:
        fail("census-deltas increment pin drift (must be the superseded dossier increment)")
    if cj["base_summary"]["sha256"] != BASE_SUMMARY_SHA or cj["base_closure"]["sha256"] != BASE_CLOSURE_SHA or \
            cj["scen_summary"]["sha256"] != SCEN_SUMMARY_SHA or cj["scen_closure"]["sha256"] != SCEN_CLOSURE_SHA:
        fail("census-deltas input summary/closure pin drift")
    if cj["census_recount_base"] != CENSUS_BASE or cj["census_recount_scen"] != CENSUS_SCEN:
        fail("census-deltas recount drift")
    if cj["verdict"]["census_counts_identical_to_published_summaries"] is not True or \
            cj["per_root_free_and_uncovered_identical"] is not True or \
            cj["per_root_coverage_byte_identical"] is not True:
        fail("census-deltas identity flags drift")
    if cj["status_flips"] != STATUS_FLIPS or cj["status_flip_count"] != len(STATUS_FLIPS):
        fail("census-deltas status-flip table drift")
    cu = {e["class_index"]: (e["base"], e["scen"]) for e in cj["closure_churn"]["unknown_now_churn"]}
    if cu != CLOSURE_UNKNOWN_CHURN:
        fail("census-deltas closure unknown churn drift")
    cr = {e["class_index"]: (e["base"], e["scen"]) for e in cj["closure_churn"]["rank_churn_ranked"]}
    if cr != churn["rank"]:
        fail("census-deltas closure rank churn drift (published table vs recomputation)")
    if cj["closure_churn"]["rows_base"] != 804 or cj["closure_churn"]["rows_scen"] != 804 or \
            cj["closure_churn"]["left"] != [] or cj["closure_churn"]["entered"] != []:
        fail("census-deltas closure rows drift")
    if cj["per_root_greedy_delta"] != []:
        fail("census-deltas per-root greedy delta must be empty (measured)")
    if (cj["joint_greedy"]["base"], cj["joint_greedy"]["scen"]) != JOINT_GREEDY:
        fail("census-deltas joint greedy drift")
    if (cj["worklist_total"]["base"], cj["worklist_total"]["scen"]) != WORKLIST_TOTAL:
        fail("census-deltas worklist drift")
    if (cj["update8_refresh_base"]["resolved"], cj["update8_refresh_scen"]["resolved"]) != UPD8["resolved"] or \
            (cj["update8_refresh_base"]["remaining"], cj["update8_refresh_scen"]["remaining"]) != UPD8["remaining"] or \
            (cj["update8_refresh_base"]["groups_free_now"], cj["update8_refresh_scen"]["groups_free_now"]) != UPD8["free_groups"]:
        fail("census-deltas update8 drift")
    if cj["update8_refresh_base"]["win_hit_groups"] != 25 or \
            cj["update8_refresh_scen"]["win_hit_groups"] != 25:
        fail("census-deltas win_hit counts drift")
    if cj["win_hit_groups_identical"] is not True:
        fail("census-deltas must record identical win_hit groups")
    if cj["update8_new_resolved"] != [64872]:
        fail("census-deltas newly-resolved set drift")
    if sorted(cj["adopted_outside_baseline_requirement"]) != [39127, 91506, 96472, 112201]:
        fail("census-deltas adopted-outside-baseline set drift")
    if {int(k): v for k, v in cj["owner_class_count_hist"].items()} != OWNER_HIST:
        fail("census-deltas owner histogram drift")
    if cj["verdict"]["canonical_head_sha256"] != BASE_CACHE_SHA or \
            cj["verdict"]["part_declared"] is not False or \
            cj["verdict"]["consumed"] != "NOTHING" or \
            cj["verdict"]["status_flips"] != len(STATUS_FLIPS) or \
            "UNKNOWN" not in cj["verdict"]["note"]:
        fail("census-deltas verdict-scope fields drift (dossier-time scope)")
    wr = cj["worklist_regen_pins"]
    if wr["scen"]["sha256"] != SCEN_WORKLIST_SHA or wr["scen"]["size"] != 3715904:
        fail("census-deltas scen worklist regen pin drift")
    if not isinstance(wr["base"], list) or len(wr["base"]) != 1 or \
            wr["base"][0]["sha256"] != BASE_WORKLIST_SHA or wr["base"][0]["size"] != 3715963:
        fail("census-deltas base worklist regen pin drift (must carry over the "
             "Part EM dossier regen pin)")
    scr = cj["serving_class_rows"]
    for cls, want in SERVING_CHECKS.items():
        row = scr[str(cls)]
        if (row["unknown_before"], row["unknown_after"], row["adopted_owned_here"],
             row["base_status"], row["scen_status"]) != \
                (want["unknown_base"], want["unknown_scen"], len(want["members"]),
                 "unknown", "excluded_now"):
            fail(f"census-deltas serving-class row drift: {cls}")
    ak = cj["adopted"]
    if len(ak) != 5:
        fail("census-deltas adopted table size drift")
    for rec, kid in zip(ak, ADOPTED_IDS):
        s5i, lo, hi, nodes, cls = ADOPTED[kid]
        if (rec["lo"], rec["hi"], rec["nodes"], rec["s5_index"], rec["serving_class"]) != \
                (lo, hi, nodes, s5i, cls):
            fail(f"census-deltas adopted table order/field drift: {kid}")
        if sorted(rec["owner_classes"]) != sorted(owners[kid]) or \
                rec["owner_count"] != len(owners[kid]):
            fail(f"census-deltas adopted owner set drift: {kid}")
        for c in owners[kid]:
            if c in set(STATUS_FLIPS):
                if (cb[c][0], ca[c][0]) != ("unknown", "excluded_now"):
                    fail(f"owner class {c} of {kid} flip-direction violation")
            else:
                if cb[c][0] != "excluded_now" or ca[c][0] != "excluded_now":
                    fail(f"owner class {c} of {kid} must stay excluded_now on both sides")

    # --- decomposition emission -------------------------------------------------
    decomp = {
        "schema": "sixthwin5-decomp-deltas-v1",
        "part": "EW",
        "date": "2026-11-26",
        "base": {
            "cache_sha256": BASE_CACHE_SHA,
            "cache_path": "research/experiments/n11-centralreply-emloss21-adoption-predecl-20261126/output/merged-exact-s5-chain-plus-emloss21-20261126.cache",
            "rows": 6792, "win": 192, "loss": 6600,
            "refresh_summary_sha256": BASE_SUMMARY_SHA,
            "closure_classes_sha256": BASE_CLOSURE_SHA,
            "per_root_coverage_sha256": BASE_PRC_SHA,
            "probe_worklist_regen_pin_sha256": BASE_WORKLIST_SHA,
            "probe_worklist_not_published_size_policy_bytes": 3715963,
            "class_status_counts": CENSUS_BASE,
        },
        "scen": {
            "cache_sha256": SCEN_CACHE_SHA,
            "cache_path_of_record": "research/experiments/n11-centralreply-sixthwin5-adoption-predecl-20261126/output/merged-exact-s5-chain-plus-sixthwin5-20261126.cache",
            "rows": 6797, "win": 197, "loss": 6600,
            "increment_sha256": INCR_SHA,
            "manifest_sha256": MANIFEST_SHA,
            "merge_audit_sha256": MERGE_AUDIT_SHA,
            "refresh_summary_sha256": SCEN_SUMMARY_SHA,
            "closure_classes_sha256": SCEN_CLOSURE_SHA,
            "per_root_coverage_sha256": SCEN_PRC_SHA,
            "probe_worklist_regen_pin_sha256": SCEN_WORKLIST_SHA,
            "probe_worklist_not_published_size_policy_bytes": 3715904,
            "class_status_counts": CENSUS_SCEN,
        },
        "dossier_supersession": {
            "dossier_increment_sha256": DOSSIER_INCR_SHA,
            "dossier_manifest_sha256": DOSSIER_MANIFEST_SHA,
            "dossier_maker_sha256": DOSSIER_MAKER_SHA,
            "part_increment_sha256": INCR_SHA,
            "row_region_byte_identical": True,
            "merged_cache_byte_identical": True,
            "note": "the dossier increment header declared pre-declaration dossier status; the Part-emitted increment supersedes it with the Part EW adoption header; the 5 s5verdict rows are byte-identical and the merged cache of record carries the published dossier merged sha 16a12390...",
        },
        "adopted": {
            "ids": list(ADOPTED_IDS),
            "nodes_total": ADOPTED_NODES,
            "direction": "WIN (win-only canonical adoption)",
            "condition": "closure-batch two-pass fresh-cold node-exact 15M raws plus a voluntary third cold verify run each, C++-gated GATE-PASS by the Part SK kit, third-implementation-corroborated (k02 by the ea73c3e3 fixed-implementation kit's 4-run witness; k03/k04/k05/k08 by the TI kit audits' verdict-level WIN agreement); re-verified live TWICE (Part maker + the byte-verbatim dossier-maker re-execution inside this extractor; NO new solver pass ran)",
            "win_ties": [],
            "standing_unconsumed_loss_not_emitted": {"k01": [15000000, 10369650],
                                                     "k06": [15000000, 8182231],
                                                     "k07": [2000000, 1419823]},
        },
        "class_flips": {
            "count": len(STATUS_FLIPS),
            "direction": "unknown -> excluded_now, win-hit only: exactly the owner classes of the 5 adopted WIN keys that were status-unknown at BASE (the dossier census measured 8); NO class is freed",
            "per_key_owner_classes": {k: sorted(owners[k]) for k in sorted(owners)},
            "flipped_classes": list(STATUS_FLIPS),
            "owner_class_count_histogram": {str(k): v for k, v in sorted(OWNER_HIST.items())},
            "serving_classes": {str(cls): rec for cls, rec in sorted(serving_records.items())},
        },
        "closure_classes": {
            "rows_before_after": list(CLOSURE["rows"]),
            "left_rows": [],
            "entered_rows": [],
            "exit_note": "no closure class enters or leaves: the 8 win-hit flips turn classes unknown -> excluded_now, which do not change closure membership; class 16734 is the only unknown_now churn (92 -> 91) and the dense ranking is unchanged",
            "rank_churn_rows": len(churn["rank"]),
            "rank_churn_nature": "measured 0 re-ranked rows",
            "unknown_churn": {str(k): list(v) for k, v in sorted(CLOSURE_UNKNOWN_CHURN.items())},
            "groups_served_churn": {},
        },
        "frozen_update8": {
            "union_baseline": UNION_BASELINE,
            "resolved": list(UPD8["resolved"]),
            "remaining_now": list(UPD8["remaining"]),
            "groups_free_now": list(UPD8["free_groups"]),
            "win_hit_groups": "25 -> 25 IDENTICAL sets (measured; no group crosses the win_hit boundary)",
            "newly_resolved": [64872],
            "newly_resolved_note": "exactly k02's s5 index 64872; the other 4 adopted keys (s5 39127/91506/96472/112201) sit outside the frozen update8 baseline requirement and are correctly not counted (measured, disclosed)",
        },
        "per_root": {
            "free_now_uncovered": "identical at all 20 rows incl. baseline; no coverage claim",
            "greedy_union_changes": {},
            "joint_greedy": list(JOINT_GREEDY),
            "joint_greedy_delta": JOINT_GREEDY[1] - JOINT_GREEDY[0],
            "unique_groups": list(UNIQUE_GROUPS),
            "group_best_options_nonfree": list(GROUP_BEST_NONFREE),
            "worklist_total": list(WORKLIST_TOTAL),
        },
        "dossier_census_crosscheck": {
            "measurement_sha256": CENSUSJSON_SHA,
            "agreement": "EXACT on both cache identities, the census counts (34,417/103/39/390 -> 34,409/111/39/390), the exact 8-class flip set, closure churn incl. the zero rank table and the 16734 unknown churn, per-root greedy deltas (none), joint greedy, worklist totals, update8 numbers incl. the 1-key newly-resolved set and the 4 outside-baseline keys, win_hit identity, serving-class records, the owner histogram and the 5-row adopted table with owner sets",
            "superseded_scope_fields": "verdict.consumed=NOTHING / part_declared=false describe the dossier-time status and are superseded by this Part EW declaration; checked, not asserted as current",
        },
        "honesty": {
            "win_only_adoption": True,
            "no_root_verdict": "no root verdict is asserted or implied by consuming a WIN label; the win-hit mechanism only reclassifies owner classes as excluded_now",
            "no_class_freed": "no class flips to free_now; joint greedy and per-root coverage are byte-identical on both sides",
            "scheduling_effect": "joint greedy 35,155 -> 35,155 UNCHANGED, worklist 64,277 -> 64,276 (-1), update8 resolved 280 -> 281 (the k02 index only): scheduling bookkeeping only",
            "unknown_still": "34,409 S4 classes remain status-unknown after the adoption; 11x11 stays UNKNOWN",
            "unconsumed": "k01/k06/k07 LOSS rows stay unconsumed honest labels (not emitted, no cache); the later parked4 L50M WIN rows (k13/k19 etc.) are NOT adopted and stay in NO cache; no root, no root class and no closure class verdict is asserted",
        },
    }
    DECOMP_OUT.write_text(json.dumps(decomp, indent=1, ensure_ascii=False) + "\n",
                          encoding="utf-8")
    print("EW decomp OK: flips=8 (unknown->excluded_now win-hit) "
          "census 34417/103/39/390 -> 34409/111/39/390 caches=6792->6797 "
          "win=192->197 loss=6600->6600 closure_rows=804->804 enter/exit=none "
          "resolved=280->281 (new key 64872 only) greedy=35155->35155 "
          "worklist=64277->64276")
    print(f"decomp sha={sha(DECOMP_OUT)}")
    print(f"maker sha={MAKER_SHA}")

def sums_nodes(cache):
    return sum(v[1] for v in cache.values())


if __name__ == "__main__":
    main()
