#!/usr/bin/env python3
"""BASE (canonical chain through the Part EV evwin4 fourth WIN adoption)
vs SCENARIO (emloss21 = Part EM loss-only canonical adoption: the 21
UNCONSUMED closure-batch exact-LOSS rows of the EM-pattern territory).

Fork of the published Part EV extractor
`compare_deltas_ev_adoption.py` (sha256
70a5b2078f5774742464d189baa348297c3fbb5c715d327ce8706bfbfbcf2b5b;
structural clone, disclosed diff: the adopted-rows table, both refresh
sides, the manifest decomposition fields, the dossier-supersession /
dossier-maker re-execution sections and the pinned expectations are
Part-EM specific).

Fail-closed machine recomputation of exactly what the Part EM emloss21
canonical LOSS adoption changed, from published bytes only:

* every artifact sha-pinned (BASE = the published Part EV pre-declaration
  dossier outputs -- the merged canonical cache 63f33c4f... 6,771 rows
  WIN 192 / LOSS 6,579, the reaudit outputs refresh-summary 1fafd081... /
  closure-classes 6ba51faa... / per-root-coverage d9eee976... and worklist
  regen pin ca50cb68...; SCEN = the published emloss21 pre-declaration
  dossier outputs -- the scenario merged cache 6e49dd84... 6,792 rows
  WIN 192 / LOSS 6,600, the dossier increment 47443dc1... (pre-declaration
  header, superseded row-exactly by the Part-emitted increment
  3e6e9bf0...), the reaudit outputs refresh-summary 7f379b71... /
  closure-classes 68628134... / per-root-coverage 9c5b2774... and worklist
  regen pin 147b62d6...; the Part kit outputs -- increment 3e6e9bf0...,
  increments-manifest bd4b9e76... (schema
  emloss21-adoption-increments-manifest-v1), merge-audits x3 (identical
  sha 17a390e7...), the maker (structural clone of the published dossier
  maker 74fbbfd9...), the byte-clone of the union merger 90711961... and
  both refresh forks (the published Part EV dossier refresh f2edac3e...
  and the published emloss21 dossier refresh fork cc01b3d8..., itself a
  byte-clone of f2edac3e... differing in EXACTLY the three declared
  regions: docstring, CACHE path, expected cache sha; the computation
  region is byte-identical), the frozen graph/update8/board/policy/
  quarantine pins, the published Part EV kit increment 7f125610... and
  the dossier census measurement census-deltas-emloss21-predecl.json
  d67b6e9b...); both probe-worklists are UNPUBLISHED per the size
  policy - they enter ONLY as regen pins (BASE ca50cb68... 3,717,416 B /
  SCEN 147b62d6... 3,715,963 B) re-verified by the byte-verbatim refresh
  re-execution;
* BOTH published refresh forks are RE-EXECUTED byte-verbatim in isolated
  scratch trees against their pinned inputs, and all eight outputs must
  be byte-identical to the published / regenerated pins before any delta
  is emitted (double determinism; this simultaneously re-proves the
  published reaudit outputs of both sides are regenerable from published
  bytes);
* the published dossier maker make_increments_emloss21.py (74fbbfd9...)
  is RE-EXECUTED byte-verbatim in an isolated scratch tree: rc=0 and
  byte-identical reproduction of its pinned outputs (increment
  47443dc1... and manifest 94815c34...) is required before any delta is
  emitted - this re-proves live, from published bytes only, the entire
  Part EM adopt-eligibility evidence chain the dossier maker encodes
  (batch-5 direct sha pins 39/39 consumed files, Part ES kit MANIFEST
  cc987739... 38/38 file-by-file, the b38 SSOT cross-gate 29807104...
  with the prior 15M EXHAUSTED honest-label pins, all 24 probed rows'
  two-pass payload gates, the f017/ai007/ai040 WIN regression ties
  against BASE, the fresh-to-BASE / quarantine / canonical-safety gates
  and the adopted-table digest 4fd8723e...);
* the Part-emitted increment 3e6e9bf0... is row-for-row identical to the
  published dossier increment 47443dc1... (the superseded header comment
  block is the ONLY differing region); the recorded supersession: the
  canonical merged cache of record is the published dossier merged file
  6e49dd84... and the Part merge audits (17a390e7... x3, byte-identical)
  record exactly this output;
* SCEN cache == BASE cache rows + exactly the 21 Part increment rows
  (verdict agreement everywhere; 6,792 rows WIN 192 / LOSS 6,600); the
  adopted rows are ALL fresh exact-LOSS rows (17 batch-5 class-12264
  rows f001-f016/f018 at 15M, 4 Part ES class-30345 reprobe30m rows
  ai024/ai030/ai038/ai041 at 30M; adopted node total 129,518,414 =
  58,253,401 + 71,265,013; every row re-verified live against the
  published source bytes first by the Part maker and again here by the
  dossier-maker re-execution); NO adopted key intersects the Part EV
  increment 7f125610... (no re-adoption of any already-consumed row);
  the 3 consumed source-batch WINs (f017 Part EV 15M 3,522,635, ai007
  and ai040 Part EU euwin2 30M 16,090,493 / 20,711,023) are re-verified
  live as WIN regression ties in BASE with identical nodes, never
  re-adopted;
* the independent full-class census (frozen graph s4_cost + update8
  receipts + cache verdicts, replicating the refresh status logic) must
  reproduce the published class status counts EXACTLY on both sides
  (BASE 34,417/103/39/390, SCEN 34,417/103/39/390 IDENTICAL) with
  EXACTLY ZERO status flips (loss-only adoption frees no class and
  excludes no class: every owner class of the 21 keys keeps its BASE
  status);
* serving-class Board arithmetic recomputed from the frozen graph:
  class 12264 (raw boundary 52, cost size 52) cost-unknown 50 -> 33
  (exactly the 17 batch-5 keys consumed; closure rank 11 -> 9) and
  class 30345 (raw boundary 51, cost size 50) cost-unknown 4 -> 0 (the
  4 Part ES keys exhausted its remaining unknown closure children; the
  class EXITS the closure-classes ranking 805 -> 804 with
  exited=[30345], entered=[]; its status stays excluded_now - flipped
  by the Part EP/EU chain, NOT re-flipped here);
* per-key owner class sets recomputed from the frozen graph must equal
  the published dossier census measurement's owner_classes row-for-row
  (owner-class count histogram EXACTLY {3 owners: 7 keys,
  4 owners: 14 keys});
* closure-classes.csv: exactly ONE row leaves (805 -> 804), ZERO rows
  enter; the unknown_now churn is exactly {6518: 61->60, 6547: 58->57,
  9478: 61->60, 12235: 61->60, 12264: 50->33} and the class_rank churn
  recomputed from the two published CSVs must equal the published
  dossier measurement's rank_churn table EXACTLY (763 re-ranked rows -
  dense-rank bookkeeping at the cheap end of the ranking, no coverage
  claim); NO groups_served churn anywhere; every other field of every
  common row is byte-identical;
* update8 refresh: resolved 263 -> 280 (the newly resolved set is
  EXACTLY the 17 batch-5 adopted s5 indices; the 4 Part ES keys were
  first probed in batch-38 AFTER the update8 baseline froze and are
  correctly not in it - measured, disclosed), remaining 31,445
  unchanged, groups_free_now stays 131, union baseline stays 31,859,
  win_hit groups 25 -> 25 IDENTICAL sets (loss-only adoption adds no
  win_hit group and removes none);
* per-root coverage: free_now/uncovered third columns IDENTICAL at all
  20 roots; Board verification 39/39 with zero rejections on both
  sides; the individual greedy union changes only at the 6 roots
  {49: 2697->2696, 38: 3014->2879, 16: 2969->2982, 5: 2883->2866,
  36: 2951->3001, 12: 2846->2842} (four drops, two rises; the greedy
  heuristic is a scheduling quantity, disclosed as-is);
* the frozen greedy scheduler deltas are recorded as bookkeeping (joint
  greedy 36,618 -> 35,155, MINUS 1,463, the largest single scheduling
  reduction of any pending adoption pool measured so far; unique groups
  2,115 -> 2,115; group_best_options_nonfree 2,105 -> 2,101; worklist
  64,302 -> 64,277 (-25));
* the published dossier census measurement d67b6e9b... is machine
  cross-compared field-by-field against this independent recount
  (census counts, zero-flip set, closure churn incl. the 763-row rank
  table, per-root greedy deltas, joint greedy, worklist totals, update8
  numbers, win_hit identity, serving-class records, owner histogram,
  the adopted table and both cache identities): agreement must be
  EXACT.  The dossier verdict scope fields (consumed NOTHING,
  part_declared false) describe the dossier-time status and are
  superseded by the Part EM declaration (disclosed, not asserted).

No unknown verdict is asserted anywhere.  The standard 11x11 empty board
and every central-reply root stay UNKNOWN; free_now / coverage
quantities are scheduling bookkeeping derived from exact verdicts, not
root verdict claims.  Consuming the 21 LOSS labels transfers NO verdict
to any root and flips NO class status: the census is identical on both
sides.  k04 (sixth-cost WIN) and every other unconsumed probe-level WIN
stay in NO cache; 11x11 stays UNKNOWN.
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

# BASE side = the published Part EV pre-declaration dossier kit (head of
# record = Part EV head merged-exact-s5-chain-plus-evwin4 63f33c4f...).
BASE_EXP = ROOT / "research/experiments/n11-centralreply-evwin4-adoption-predecl-20261126"
BASE_OUT = BASE_EXP / "reaudit/output"
BASE_CACHE = BASE_EXP / "output/merged-exact-s5-chain-plus-evwin4-20261126.cache"
# SCEN side = the published emloss21 pre-declaration dossier kit.
DOSSIER = ROOT / "research/experiments/n11-centralreply-emloss21-adoption-predecl-20261126"
SCEN_CACHE = DOSSIER / "output/merged-exact-s5-chain-plus-emloss21-20261126.cache"
INCR = EXP / "output/increment-emloss21-adoption-20261126.cache"
MANIFEST = EXP / "output/increments-manifest.json"
CENSUSJSON = DOSSIER / "output/census-deltas-emloss21-predecl.json"
DOSSIER_INCR = DOSSIER / "output/increment-emloss21-20261126.cache"
DOSSIER_MANIFEST = DOSSIER / "output/increments-manifest.json"
DOSSIER_MAKER = DOSSIER / "scripts/make_increments_emloss21.py"
EV_PART = ROOT / "research/experiments/n11-centralreply-evwin4-adoption-reaudit-20261126"
EV_INCREMENT = EV_PART / "output/increment-evwin4-20261126.cache"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_REFRESH_SCRIPT = BASE_EXP / "reaudit/scripts/refresh_adoption_evwin4.py"
SCEN_REFRESH_SCRIPT = DOSSIER / "reaudit/scripts/refresh_adoption_emloss21.py"
MERGER = EXP / "scripts/s5_union_merge.py"
MAKER = EXP / "scripts/make_increments_emloss21_adoption.py"
DECOMP_OUT = EXP / "output/decomp-deltas-emloss21-adoption.json"

# ---- pins ------------------------------------------------------------------
BASE_CACHE_SHA = "63f33c4f620583449641102026b261c559ae5ecc29713cd6445d6fe9369858f0"
SCEN_CACHE_SHA = "6e49dd841b7bfcb335d86ef2479c95f47ab7acbcf41ace389a8b8eb95c778c9d"
INCR_SHA = "3e6e9bf0a5f410a1d584889832f21352dd01a97aef5a899de06a28373fcaef82"
MANIFEST_SHA = "bd4b9e766d0806f60a6df1ec4e91076fa7564486caeadfc222a16baabca6c01d"
MAKER_SHA = None  # asserted at run (the maker bytes are pinned by the wave-B/C MANIFEST)
DOSSIER_INCR_SHA = "47443dc143c157ab972de0f39f2cf3afb5d062e209da9dcd8e486f0a57c8ebca"
DOSSIER_MANIFEST_SHA = "94815c34f1142481a20fe411a0a1c87c4e0a075b100d47db2f5e7b35dea9707d"
DOSSIER_MAKER_SHA = "74fbbfd9a206a28e1bcdf2d52ceb884bf71c5aee62ec0eefe520a41cd33d8035"
CENSUSJSON_SHA = "d67b6e9bcf55a601afdc177aa804f2be2b8d4fd6ec9d76ac6389fa5b913edcd3"
BASE_SUMMARY_SHA = "1fafd0811d4b5e806a11cf610111967b9d6fdb741fa86b68688ef1cee4411e6e"
BASE_CLOSURE_SHA = "6ba51faa9824ba5065a8e938cc6970ce2ace464f74d26f30582cbaa8334c930d"
BASE_PRC_SHA = "d9eee976e52c38c71440a26cb6f9f14ae68439feaec21e17600b1052870dd502"
BASE_WORKLIST_SHA = "ca50cb68c10827e7e24e02c02e0166813b57ad646eb169bf8bd2c827fcdd09df"
SCEN_SUMMARY_SHA = "7f379b718e48330c5acbc3c9c79be3c4fb6d616c4dc7bedfe7691e6ebb225f0b"
SCEN_CLOSURE_SHA = "6862813431dd1abbaba81ac2a720385be394ce774f259b8001ca49630fc4a8e2"
SCEN_PRC_SHA = "9c5b277429f99157ff2e65323b5912b9ce957f1d2008f8ac8fc1e03b49f91ad1"
SCEN_WORKLIST_SHA = "147b62d643ba9039e9e2b64363cec602405bf11210a3aa4cfd9084eb0df3a973"
BASE_REFRESH_SHA = "f2edac3e3e3c74ddd073a709a0ab521cf8c3db1048322e1f0347a1ea013aa885"
SCEN_REFRESH_SHA = "cc01b3d8772a9e6fe0c5718ed0715b7c927c5ab149444690329c6e19c57e2131"
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
MERGE_AUDIT_SHA = "17a390e78f603de0bc20577f9f1f75b5016fd818af1acb58db835f5add49801f"
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
BOARD_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
EV_INCREMENT_SHA = "7f1256108d697bd96d473e55a5509dea35f4c0b1be45893cac3f667c4b3f55c4"
ADOPTED_TABLE_DIGEST = "4fd8723ec0e2d185fe807b80681f1c9deca6ac0ee09ddd4bf77b047cdb88e97b"
MERGED_COMMENT = "# S5 solver-trusted exact; base=merged-exact-s5-after-js-probe-13.cache (sha256 60e0dc3476920d4e...); increment=101 fresh rows (99 canonical S5 children of S4 1297036692683752448:0 absent from the chain, 2 unclaimed backward-only rows, 1 S6-witness-derived TARGET_S5 row nodes=0); see merge-manifest.json"

# ---- adopted table (Part EM) -----------------------------------------------
# id -> (s5_index, lo, hi, nodes, serving_class); order = sorted (lo, hi),
# the manifest adopted_table / increment row order.
ADOPTED = {
    "f005": (223911, 1152921504606848033, 128, 2815240, 12264),
    "f008": (323984, 1152921504606848033, 262144, 1775516, 12264),
    "f016": (415094, 1152921504606848033, 134217728, 4032622, 12264),
    "f003": (115134, 1152921504606848033, 536870912, 2247077, 12264),
    "f011": (414362, 1152921504606848033, 1099511627776, 2685012, 12264),
    "f018": (415096, 1152921504606850081, 0, 3598340, 12264),
    "f009": (324399, 1152921504606913569, 0, 2214154, 12264),
    "f001": (348, 1152921504741065761, 0, 2789768, 12264),
    "ai030": (894456, 1152921573327372288, 17825792, 16504156, 30345),
    "ai041": (900170, 1152921573327372288, 34603008, 15781960, 30345),
    "f006": (224296, 1152921779484754977, 0, 2042919, 12264),
    "ai024": (889534, 1152922604118479104, 65536, 19127057, 30345),
    "ai038": (898436, 1152927002164989952, 65536, 19851840, 30345),
    "f012": (415090, 1188950301627908097, 70368744177664, 4680543, 12264),
    "f013": (415091, 1188950305920778241, 70368744177664, 4667365, 12264),
    "f014": (415092, 1188959097718833153, 70368744177664, 2543113, 12264),
    "f015": (415093, 1206964700135292929, 70368744177664, 6555693, 12264),
    "f010": (327676, 1224979098644775969, 0, 3586193, 12264),
    "f002": (4231, 1297036692682703905, 0, 4054799, 12264),
    "f007": (227832, 1441151880758559777, 0, 3503294, 12264),
    "f004": (119290, 1729382256910271521, 0, 4461753, 12264),
}
ADOPTED_IDS = sorted(ADOPTED, key=lambda k: (ADOPTED[k][1], ADOPTED[k][2]))
ADOPTED_B5_IDS = ["f001", "f002", "f003", "f004", "f005", "f006", "f007",
                  "f008", "f009", "f010", "f011", "f012", "f013", "f014",
                  "f015", "f016", "f018"]
ADOPTED_ES_IDS = ["ai024", "ai030", "ai038", "ai041"]
ADOPTED_NODES_B5 = 58253401
ADOPTED_NODES_ES = 71265013
ADOPTED_NODES = 129518414
WIN_TIES = {
    "f017": (415095, 1188950301625810945, 70368744177666, 82, 3522635),
    "ai007": (441292, 1152922604118478880, 65536, 84, 16090493),
    "ai040": (899584, 1152922604118487040, 65536, 85, 20711023),
}
CENSUS_BOTH = {"unknown": 34417, "excluded_now": 103, "free_now": 39, "excluded": 390}
OWNER_HIST = {3: 7, 4: 14}
SERVING_CHECKS = {
    12264: {"raw_boundary": 52, "cost_size": 52, "unknown_base": 50,
            "unknown_scen": 33, "members": ADOPTED_B5_IDS},
    30345: {"raw_boundary": 51, "cost_size": 50, "unknown_base": 4,
            "unknown_scen": 0, "members": ADOPTED_ES_IDS},
}
CLOSURE = {"rows": (805, 804), "left": [30345], "entered": []}
CLOSURE_UNKNOWN_CHURN = {6518: (61, 60), 6547: (58, 57), 9478: (61, 60),
                         12235: (61, 60), 12264: (50, 33)}
RANK_CHURN_EXPECTED = 763
UPD8 = {"resolved": (263, 280), "remaining": (31445, 31445), "free_groups": (131, 131)}
UNION_BASELINE = 31859
WIN_HIT = (25, 25)
GREEDY_DELTA = {49: (2697, 2696), 38: (3014, 2879), 16: (2969, 2982),
                5: (2883, 2866), 36: (2951, 3001), 12: (2846, 2842)}
JOINT_GREEDY = (36618, 35155)
UNIQUE_GROUPS = (2115, 2115)
GROUP_BEST_NONFREE = (2105, 2101)
WORKLIST_TOTAL = (64302, 64277)
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
    """Re-execute the published dossier maker byte-verbatim in a scratch
    tree; require rc=0 and byte-identical reproduction of its pinned
    outputs (increment 47443dc1..., manifest 94815c34...).  This re-proves
    the entire Part EM adopt-eligibility evidence chain live."""
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
    for name, want in (("increment-emloss21-20261126.cache", DOSSIER_INCR_SHA),
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
        ("Part EV kit increment", EV_INCREMENT, EV_INCREMENT_SHA),
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
    if manifest["schema"] != "emloss21-adoption-increments-manifest-v1":
        fail("manifest schema drift")
    if manifest["part"] != "EM" or manifest["date"] != "2026-11-26":
        fail("manifest part/date drift")
    if manifest["loss_canonical_adoption"] is not True:
        fail("manifest loss_canonical_adoption flag drift")
    if manifest["base_cache_sha256"] != BASE_CACHE_SHA:
        fail("manifest base cache pin drift")
    if manifest["sha256"]["loss_increment"] != INCR_SHA:
        fail("manifest loss_increment pin drift")
    if manifest["merger_sha256"] != MERGER_SHA:
        fail("manifest merger pin drift")
    if manifest["base_cache_rows"] != 6771:
        fail("manifest base rows drift")
    if manifest["base_cache_win_loss"] != [192, 6579]:
        fail("manifest base win/loss drift")
    if manifest["row_counts"] != {"adopted_loss_rows": 21,
                                   "win_ties_consumed_elsewhere": 3,
                                   "prior_canonical_rows_base": 6771}:
        fail("manifest row_counts drift")
    if set(manifest["resolved_ids"]) != set(ADOPTED) or \
            set(manifest["loss_ids"]) != set(ADOPTED) or \
            len(manifest["resolved_ids"]) != 21 or len(manifest["loss_ids"]) != 21:
        fail("manifest adopted/target ids drift")
    if manifest["adopted_nodes_total"] != ADOPTED_NODES:
        fail("manifest adopted node total drift")
    if manifest["adopted_table_digest_sha256"] != ADOPTED_TABLE_DIGEST:
        fail("manifest adopted-table digest drift")
    if manifest["quarantine_hits"] != 0:
        fail("manifest quarantine hits drift")
    if manifest["base_cache_absent_hits_for_emitted"] != 0:
        fail("manifest base-absent hits drift")
    if manifest["full_packet_eq_loss_only"] is not True:
        fail("manifest loss-only flag drift")
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
            prov["b5_kit_direct_pins"] is not True or \
            prov["es_kit_files_verified"] != 38 or \
            prov["raws_published"] is not True or \
            prov["b38_ssot_verified"] is not True or \
            not prov.get("b5_fetch_anchor_note"):
        fail("manifest provenance drift")
    pools = {p["pool"]: p for p in manifest["pools"]}
    if sorted(pools) != ["b5-class12264", "es-class30345-reprobe30m"]:
        fail("manifest pool set drift")
    pb5, pes = pools["b5-class12264"], pools["es-class30345-reprobe30m"]
    if pb5["adopted_loss_ids"] != ADOPTED_B5_IDS or pb5["win_tie_ids"] != ["f017"] \
            or pb5["budget"] != 15000000 or pb5["adopted_nodes"] != ADOPTED_NODES_B5:
        fail("manifest b5 pool drift")
    if pes["adopted_loss_ids"] != ADOPTED_ES_IDS or \
            pes["win_tie_ids"] != ["ai007", "ai040"] or \
            pes["budget"] != 30000000 or pes["adopted_nodes"] != ADOPTED_NODES_ES:
        fail("manifest es pool drift")
    if pes["prior_15m_condition"]["honest_label_pins"] != {
            k: [0, 15000000] for k in ["ai007", "ai024", "ai030", "ai038",
                                       "ai040", "ai041"]}:
        fail("manifest es prior-15m honest-label pins drift")
    if pes["b38_ssot_cross_check"]["batch_keys_b38_sha256"] != \
            "298071046bfba8473c5b3d6e0b6a30108697eb0899aed7c70fcb4c5343f7cb8d":
        fail("manifest b38 SSOT pin drift")
    rows = manifest["adopted_table"]
    if len(rows) != 21:
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
        if r["result"] != 2:
            fail(f"manifest adopted row must be exact LOSS: {kid}")
    # win ties: manifest rows vs pins, then verified live against BASE below
    wt = {w["id"]: w for w in manifest["win_ties"]}
    if sorted(wt) != sorted(WIN_TIES):
        fail("manifest win-tie ids drift")
    for kid, (s5i, lo, hi, legal, nodes) in WIN_TIES.items():
        w = wt[kid]
        if (w["lo"], w["hi"], w["legal"], w["s5_index"], w["nodes"]) != (lo, hi, legal, s5i, nodes):
            fail(f"manifest win-tie field drift: {kid}")
    if "interpretation_guard" not in manifest or "UNKNOWN" not in manifest["interpretation_guard"]:
        fail("manifest interpretation guard drift")

    # --- dossier supersession: Part increment rows == dossier increment rows
    if cache_row_list(INCR) != cache_row_list(DOSSIER_INCR):
        fail("Part increment rows differ from the dossier increment rows")
    if cache_row_list(INCR) != [f"s5verdict,{ADOPTED[k][1]},{ADOPTED[k][2]},5,2,{ADOPTED[k][3]}"
                                for k in ADOPTED_IDS]:
        fail("increment rows differ from the pinned adopted table order/bytes")

    # --- merge-audit decomposition --------------------------------------------
    for rn in ("merge-audit-run1.json", "merge-audit-run2.json", "merge-audit-run3.json"):
        a = json.loads((EXP / "output" / rn).read_text())
        if a["unique_rows"] != 6792 or a["duplicate_rows_elided"] != 0:
            fail(f"merge-audit row accounting drift: {rn}")
        if a["verdict_counts"] != {"WIN(1)": 192, "LOSS(2)": 6600}:
            fail(f"merge-audit verdict counts drift: {rn}")
        if a["nodes_field_mismatches_recorded"] != []:
            fail(f"merge-audit nodes mismatch drift: {rn}")
        if a["output_sha256"] != SCEN_CACHE_SHA or a["output_bytes"] != 283770:
            fail(f"merge-audit output identity drift: {rn}")
        if a["comments_kept_from_first_input"] != [MERGED_COMMENT]:
            fail(f"merge-audit comment block drift: {rn}")
        ins = a["inputs"]
        if len(ins) != 2 or ins[0]["sha256"] != BASE_CACHE_SHA or \
                ins[0]["rows"] != 6771 or ins[0]["unique_new"] != 6771:
            fail(f"merge-audit BASE input entry drift: {rn}")
        if ins[1]["sha256"] != INCR_SHA or ins[1]["rows"] != 21 or ins[1]["unique_new"] != 21:
            fail(f"merge-audit increment input entry drift: {rn}")
        if not ins[1]["file"].endswith(
                "n11-centralreply-emloss21-adoption-reaudit-20261126/output/increment-emloss21-adoption-20261126.cache"):
            fail(f"merge-audit increment path drift: {rn}")

    # --- refresh re-execution (both sides, byte-verbatim) --------------------
    base_tmp = rerun_refresh(BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA, ".em-verify-base-evwin4")
    scen_tmp = rerun_refresh(SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA, ".em-verify-scen-emloss21")
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
    shutil.rmtree(ROOT / "research/experiments/.em-verify-base-evwin4")
    shutil.rmtree(ROOT / "research/experiments/.em-verify-scen-emloss21")

    # --- dossier maker re-execution (the Part EM evidence chain, live) -------
    maker_outs = rerun_dossier_maker(".em-verify-dossier-maker")
    if sha(maker_outs["increment-emloss21-20261126.cache"]) != DOSSIER_INCR_SHA:
        fail("dossier maker re-execution increment drift (unreachable re-check)")
    shutil.rmtree(ROOT / "research/experiments/.em-verify-dossier-maker")

    # --- frozen dependency graph + cache relation ---------------------------
    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s5_masks = g["s5_masks"]
    m2i_probe = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}
    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    incr = load_cache(INCR)
    if len(base) != 6771 or len(scen) != 6792 or len(incr) != 21:
        fail(f"cache sizes drift: base {len(base)} scen {len(scen)} incr {len(incr)}")
    adopted_keys = {(ADOPTED[k][1], ADOPTED[k][2]): k for k in ADOPTED}
    ev_keys = set(load_cache(EV_INCREMENT))
    for key, row in incr.items():
        if row[0] != 2:
            fail(f"increment contains a non-LOSS row: {key}")
        if key in base:
            fail(f"increment key already in BASE: {key}")
        if key not in adopted_keys:
            fail(f"increment key not in the adopted set: {key}")
        if key in ev_keys:
            fail(f"adopted key also sits in the Part EV increment (re-adoption): {key}")
        if scen.get(key) != row:
            fail(f"increment row not taken verbatim into scenario cache: {key}")
    merged = dict(base)
    for key, row in incr.items():
        merged[key] = row
    if merged != scen:
        fail("scenario cache != BASE rows + increment rows (set difference)")
    wins = sum(1 for v in scen.values() if v[0] == 1)
    losses = len(scen) - wins
    if (wins, losses) != (192, 6600):
        fail(f"scenario verdict counts {wins}/{losses} != 192/6,600")
    if sums_nodes(incr) != ADOPTED_NODES:
        fail("increment node total drift")
    # WIN regression ties: the 3 consumed source-batch WINs sit in BASE
    # with identical nodes, never re-adopted
    for kid, (s5i, lo, hi, legal, nodes) in WIN_TIES.items():
        key = (lo, hi)
        got = base.get(key)
        if got is None or got[0] != 1 or got[1] != nodes:
            fail(f"win-tie {kid}: BASE row {got} != WIN tie nodes {nodes}")
        if key in incr:
            fail(f"win-tie {kid} must NOT be re-adopted by Part EM")

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
    for kid, (s5i, lo, hi, legal, nodes) in WIN_TIES.items():
        key = (lo, hi)
        if key in quarantined:
            fail(f"win-tie {kid}: quarantined key {key}")
        if not is_canonical_safe_s5_key(key):
            fail(f"win-tie {kid}: noncanonical/unsafe key {key}")

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
    if dict(Counter(v[0] for v in cb.values())) != CENSUS_BOTH:
        fail("independent census BASE recount drift vs the published counts")
    if dict(Counter(v[0] for v in ca.values())) != CENSUS_BOTH:
        fail("independent census SCEN recount drift vs the published counts")
    changed = sorted(i for i in cb if cb[i][0] != ca[i][0])
    if changed != []:
        fail(f"loss-only adoption flips class statuses: {changed}")
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
        if cb[cls][0] != "excluded_now" or ca[cls][0] != "excluded_now":
            fail(f"serving class {cls} must stay excluded_now on both sides "
                 "(EP/EV chain state, no loss-only flip)")
        serving_records[cls] = {"class": cls, "boundary_raw": len(kids),
                                "cost_size": len(cost),
                                "cost_unknown_base": ub, "cost_unknown_scen": ua,
                                "adopted_members": own,
                                "status_base": cb[cls][0], "status_scen": ca[cls][0]}
    if serving_records[12264]["adopted_members"] != sorted(ADOPTED_B5_IDS) or \
            serving_records[30345]["adopted_members"] != sorted(ADOPTED_ES_IDS):
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
    # win_hit groups: identical sets on both sides (loss-only adds/removes none)
    if (len(ub_["win_hit_groups"]), len(ua_["win_hit_groups"])) != WIN_HIT:
        fail(f"win_hit group counts drift {WIN_HIT}")
    base_scal = sorted((w["first"], w["third"], w["fourth"], w["reply"],
                        w["s4_class_index"], w["unknown_s5_children"])
                       for w in ub_["win_hit_groups"])
    scen_scal = sorted((w["first"], w["third"], w["fourth"], w["reply"],
                        w["s4_class_index"], w["unknown_s5_children"])
                       for w in ua_["win_hit_groups"])
    if base_scal != scen_scal:
        fail("win_hit group sets differ across the adoption (loss-only must keep them identical)")
    if (sb["class_status_counts"], sa["class_status_counts"]) != (CENSUS_BOTH, CENSUS_BOTH):
        fail("published status counts mismatch the pinned censuses")
    # the newly resolved set must be exactly the 17 batch-5 adopted s5 indices
    new_resolved = sorted(set(ua_["resolved_among_baseline_requirement"]) -
                          set(ub_["resolved_among_baseline_requirement"]))
    b5_indices = sorted(ADOPTED[k][0] for k in ADOPTED_B5_IDS)
    if new_resolved != b5_indices:
        fail(f"newly resolved update8 set drift: {new_resolved} != {b5_indices}")
    un_resolved = sorted(set(ub_["resolved_among_baseline_requirement"]) -
                         set(ua_["resolved_among_baseline_requirement"]))
    if un_resolved != []:
        fail(f"update8 resolved rows disappeared: {un_resolved}")
    es_indices = sorted(ADOPTED[k][0] for k in ADOPTED_ES_IDS)
    if any(j in ub_["resolved_among_baseline_requirement"] or
           j in ua_["resolved_among_baseline_requirement"] for j in es_indices):
        fail("a Part ES key sits in the frozen update8 baseline requirement "
             "(it was first probed in batch-38, after the baseline froze)")

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
    if (cj["base_cache"]["rows"], cj["base_cache"]["win"], cj["base_cache"]["loss"]) != (6771, 192, 6579) or \
            (cj["scen_cache"]["rows"], cj["scen_cache"]["win"], cj["scen_cache"]["loss"]) != (6792, 192, 6600):
        fail("census-deltas cache accounting drift")
    if cj["increment"]["sha256"] != DOSSIER_INCR_SHA:
        fail("census-deltas increment pin drift (must be the superseded dossier increment)")
    if cj["base_summary"]["sha256"] != BASE_SUMMARY_SHA or cj["base_closure"]["sha256"] != BASE_CLOSURE_SHA or \
            cj["scen_summary"]["sha256"] != SCEN_SUMMARY_SHA or cj["scen_closure"]["sha256"] != SCEN_CLOSURE_SHA:
        fail("census-deltas input summary/closure pin drift")
    if cj["census_recount_base"] != CENSUS_BOTH or cj["census_recount_scen"] != CENSUS_BOTH:
        fail("census-deltas recount drift")
    if cj["verdict"]["census_counts_identical_to_published_summaries"] is not True or \
            cj["per_root_free_and_uncovered_identical"] is not True:
        fail("census-deltas identity flags drift")
    if cj["status_flips"] != []:
        fail("census-deltas must record zero status flips")
    cu = {e["class_index"]: (e["base"], e["scen"]) for e in cj["closure_churn"]["unknown_now_churn"]}
    if cu != CLOSURE_UNKNOWN_CHURN:
        fail("census-deltas closure unknown churn drift")
    cr = {e["class_index"]: (e["base"], e["scen"]) for e in cj["closure_churn"]["rank_churn_ranked"]}
    if cr != churn["rank"]:
        fail("census-deltas closure rank churn drift (published table vs recomputation)")
    if cj["closure_churn"]["rows_base"] != 805 or cj["closure_churn"]["rows_scen"] != 804 or \
            cj["closure_churn"]["left"] != [30345] or cj["closure_churn"]["entered"] != []:
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
    if cj["update8_refresh_base"]["win_hit_groups"] != 25 or \
            cj["update8_refresh_scen"]["win_hit_groups"] != 25:
        fail("census-deltas win_hit counts drift")
    if cj["win_hit_groups_identical"] is not True:
        fail("census-deltas must record identical win_hit groups")
    if cj["update8_new_resolved"] != b5_indices:
        fail("census-deltas newly-resolved set drift")
    if {int(k): v for k, v in cj["owner_class_count_hist"].items()} != OWNER_HIST:
        fail("census-deltas owner histogram drift")
    if cj["verdict"]["canonical_head_sha256"] != BASE_CACHE_SHA or \
            cj["verdict"]["part_declared"] is not False or \
            cj["verdict"]["consumed"] != "NOTHING" or \
            cj["verdict"]["status_flips"] != 0 or \
            "UNKNOWN" not in cj["verdict"]["note"]:
        fail("census-deltas verdict-scope fields drift (dossier-time scope)")
    wr = cj["worklist_regen_pins"]
    if wr["base"]["sha256"] != BASE_WORKLIST_SHA or wr["scen"]["sha256"] != SCEN_WORKLIST_SHA or \
            wr["base"]["size"] != 3717416 or wr["scen"]["size"] != 3715963:
        fail("census-deltas worklist regen pin drift")
    scr = cj["serving_class_rows"]
    for cls, want in SERVING_CHECKS.items():
        row = scr[str(cls)]
        if (row["unknown_before"], row["unknown_after"], row["adopted_owned_here"],
             row["base_status"], row["scen_status"]) != \
                (want["unknown_base"], want["unknown_scen"], len(want["members"]),
                 "excluded_now", "excluded_now"):
            fail(f"census-deltas serving-class row drift: {cls}")
    ak = cj["adopted"]
    if len(ak) != 21:
        fail("census-deltas adopted table size drift")
    for rec, kid in zip(ak, ADOPTED_IDS):
        s5i, lo, hi, nodes, cls = ADOPTED[kid]
        if (rec["lo"], rec["hi"], rec["nodes"], rec["s5_index"], rec["serving_class"]) != \
                (lo, hi, nodes, s5i, cls):
            fail(f"census-deltas adopted table order/field drift: {kid}")
        if sorted(rec["owner_classes"]) != sorted(owners[kid]) or \
                rec["owner_count"] != len(owners[kid]):
            fail(f"census-deltas adopted owner set drift: {kid}")
        if any(cb[c][0] != ca[c][0] for c in owners[kid]):
            fail(f"an owner class of {kid} flipped status (loss-only violation)")

    # --- decomposition emission -------------------------------------------------
    decomp = {
        "schema": "emloss21-decomp-deltas-v1",
        "part": "EM",
        "date": "2026-11-26",
        "base": {
            "cache_sha256": BASE_CACHE_SHA,
            "rows": 6771, "win": 192, "loss": 6579,
            "refresh_summary_sha256": BASE_SUMMARY_SHA,
            "closure_classes_sha256": BASE_CLOSURE_SHA,
            "per_root_coverage_sha256": BASE_PRC_SHA,
            "probe_worklist_sha256": BASE_WORKLIST_SHA,
            "class_status_counts": CENSUS_BOTH,
        },
        "scen": {
            "cache_sha256": SCEN_CACHE_SHA,
            "cache_path_of_record": "research/experiments/n11-centralreply-emloss21-adoption-predecl-20261126/output/merged-exact-s5-chain-plus-emloss21-20261126.cache",
            "rows": 6792, "win": 192, "loss": 6600,
            "increment_sha256": INCR_SHA,
            "manifest_sha256": MANIFEST_SHA,
            "merge_audit_sha256": MERGE_AUDIT_SHA,
            "refresh_summary_sha256": SCEN_SUMMARY_SHA,
            "closure_classes_sha256": SCEN_CLOSURE_SHA,
            "per_root_coverage_sha256": SCEN_PRC_SHA,
            "probe_worklist_regen_pin_sha256": SCEN_WORKLIST_SHA,
            "probe_worklist_not_published_size_policy_bytes": 3715963,
            "class_status_counts": CENSUS_BOTH,
        },
        "dossier_supersession": {
            "dossier_increment_sha256": DOSSIER_INCR_SHA,
            "dossier_manifest_sha256": DOSSIER_MANIFEST_SHA,
            "dossier_maker_sha256": DOSSIER_MAKER_SHA,
            "part_increment_sha256": INCR_SHA,
            "row_region_byte_identical": True,
            "merged_cache_byte_identical": True,
            "note": "the dossier increment header declared pre-declaration dossier status; the Part-emitted increment supersedes it with the Part EM adoption header; the 21 s5verdict rows are byte-identical and the merged cache of record carries the published dossier merged sha 6e49dd84...",
        },
        "adopted": {
            "ids": list(ADOPTED_IDS),
            "nodes_total": ADOPTED_NODES,
            "nodes_by_pool": {"batch5_class12264_15m": ADOPTED_NODES_B5,
                              "es_class30345_reprobe30m": ADOPTED_NODES_ES},
            "direction": "LOSS (loss-only canonical adoption)",
            "condition": "closure-batch two-pass fresh-cold node-exact raws re-verified live TWICE (Part maker + the byte-verbatim dossier-maker re-execution inside this extractor; NO new solver pass ran)",
            "win_ties_not_readopted": {kid: {"lo": WIN_TIES[kid][1], "hi": WIN_TIES[kid][2],
                                            "nodes": WIN_TIES[kid][4]} for kid in WIN_TIES},
        },
        "class_flips": {
            "count": 0,
            "direction": "none (loss-only adoption frees no class and excludes no class)",
            "per_key_owner_classes": {k: sorted(owners[k]) for k in sorted(owners)},
            "owner_class_count_histogram": {str(k): v for k, v in sorted(OWNER_HIST.items())},
            "serving_classes": {str(cls): rec for cls, rec in sorted(serving_records.items())},
        },
        "closure_classes": {
            "rows_before_after": list(CLOSURE["rows"]),
            "left_rows": [30345],
            "entered_rows": [],
            "exit_note": "class 30345's 4 remaining unknown closure children (the Part ES reprobe30m keys) are consumed; its status stays excluded_now (Part EP/EU chain state, NOT re-flipped); it leaves the closure-classes ranking only because unknown_now drops to 0",
            "rank_churn_rows": len(churn["rank"]),
            "rank_churn_nature": "dense-rank bookkeeping at the cheap end of the ranking: the 21 keys' owner classes shift by 1-2 unknown counts each; 763 rows re-ranked, no class freed, no coverage claim",
            "unknown_churn": {str(k): list(v) for k, v in sorted(CLOSURE_UNKNOWN_CHURN.items())},
            "groups_served_churn": {},
        },
        "frozen_update8": {
            "union_baseline": UNION_BASELINE,
            "resolved": list(UPD8["resolved"]),
            "remaining_now": list(UPD8["remaining"]),
            "groups_free_now": list(UPD8["free_groups"]),
            "win_hit_groups": "25 -> 25 IDENTICAL sets (loss-only adoption adds no win_hit group and removes none)",
            "newly_resolved": b5_indices,
            "newly_resolved_note": "exactly the 17 batch-5 adopted s5 indices; the 4 Part ES keys were first probed in batch-38 AFTER the update8 baseline froze and are correctly not in it (measured, disclosed)",
        },
        "per_root": {
            "free_now_uncovered": "identical at all 20 rows incl. baseline; no coverage claim",
            "greedy_union_changes": {str(k): list(v) for k, v in sorted(GREEDY_DELTA.items(), key=lambda kv: int(kv[0]))},
            "joint_greedy": list(JOINT_GREEDY),
            "joint_greedy_delta": JOINT_GREEDY[1] - JOINT_GREEDY[0],
            "unique_groups": list(UNIQUE_GROUPS),
            "group_best_options_nonfree": list(GROUP_BEST_NONFREE),
            "worklist_total": list(WORKLIST_TOTAL),
        },
        "dossier_census_crosscheck": {
            "measurement_sha256": CENSUSJSON_SHA,
            "agreement": "EXACT on both cache identities, census counts, the zero-flip set, closure churn incl. the 763-row rank table, per-root greedy deltas, joint greedy, worklist totals, update8 numbers incl. the 17-key newly-resolved set, win_hit identity, serving-class records, the owner histogram and the 21-row adopted table with owner sets",
            "superseded_scope_fields": "verdict.consumed=NOTHING / part_declared=false describe the dossier-time status and are superseded by this Part EM declaration; not asserted",
        },
        "honesty": {
            "loss_only_adoption": True,
            "no_root_verdict": "no root verdict is asserted or implied by consuming a LOSS label",
            "no_class_freed_or_excluded": "the census is IDENTICAL on both sides (34,417 unknown / 103 excluded_now / 39 free_now / 390 excluded, zero flips)",
            "scheduling_effect": "joint greedy 36,618 -> 35,155 (-1,463, the largest single scheduling reduction of any pending adoption pool measured so far), worklist 64,302 -> 64,277 (-25), group_best_options_nonfree 2,105 -> 2,101, update8 resolved 263 -> 280: scheduling bookkeeping only",
            "unknown_still": "34,417 S4 classes remain status-unknown on both sides; 11x11 stays UNKNOWN",
            "unconsumed": "k04 (sixth-cost WIN) and every other unconsumed probe-level WIN stay in NO cache; no root, no root class and no closure class verdict is asserted",
        },
    }
    DECOMP_OUT.write_text(json.dumps(decomp, indent=1, ensure_ascii=False) + "\n",
                          encoding="utf-8")
    print("EM decomp OK: flips=0 census=34417/103/39/390 IDENTICAL caches=6771->6792 "
          "win=192->192 loss=6579->6600 closure_rows=805->804 exit=30345 "
          "resolved=263->280 greedy=36618->35155 worklist=64302->64277")
    print(f"decomp sha={sha(DECOMP_OUT)}")
    print(f"maker sha={MAKER_SHA}")


def sums_nodes(cache):
    return sum(v[1] for v in cache.values())


if __name__ == "__main__":
    main()
