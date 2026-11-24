"""Part DP adoption delta extraction: BASE (Part DN, b30loss43) vs SCENARIO (b32loss54).

Fail-closed machine recomputation of exactly what the batch-32 (class 8730)
54-LOSS canonical adoption changed, from published bytes only:

* every published artifact sha-pinned (the Part DP experiment outputs, the
  Part DN BASE reaudit outputs, both chain caches, the increment, the
  increments manifest, the published batch-32 kit MANIFEST verified
  file-by-file 193 files, graph/update8/board/policy/quarantine pins);
* the published Part DN refresh script (reaudit/scripts/
  refresh_adoption_b30loss43.py, sha d45832a6...) and the published Part DP
  refresh fork (reaudit/scripts/refresh_adoption_b32loss54.py, sha
  41bf706f...) are RE-EXECUTED byte-verbatim in isolated scratch trees
  against their pinned inputs, and all eight outputs (two x
  refresh-summary/closure-classes/per-root-coverage/probe-worklist) must be
  byte-identical to the published / regenerated pins before any delta is
  emitted (double-run determinism);
* SCEN cache == BASE cache rows + exactly the 54 increment rows (verdict
  agreement everywhere; 6,502 rows, WIN 158 / LOSS 6,344);
* the class-8730 arithmetic is independently recomputed from the frozen
  dependency graph with the integer-geometry Board: the class's canonical
  5-stone child boundary is regenerated (58 children), exactly 54 are
  unknown against BASE (== the batch-32 key set), and exactly 58 resolve to
  LOSS in the scenario (54 adopted + the 4 base-known s5
  144458/212464/310606/311726), so class 8730 becomes free_now with zero
  remaining unknown children (Board-verified by the reaudit refresh:
  free_now 39, board_verified 39/39);
* every closure-classes.csv row that changes unknown_now is asserted to be a
  Board-verified holder of adopted keys with exact own-membership arithmetic
  (delta == children-of-class intersect adopted set); rank churn is pure
  bookkeeping and counted; class 8730 LEAVES the closure table (left
  exactly [8730], entered empty) because it turns free_now;
* update8 refresh: resolved_among_baseline_requirement grows from 185 to
  187 (+2 == the adopted s5 indices that lie in the frozen baseline
  requirement: {285539, 311727}); remaining 31,674 -> 31,672;
  known-universe 627 -> 681; no resolution is lost;
* class_status counts: excluded 390 / excluded_now 23 static, free_now
  38 -> 39 (the class-8730 Board-verified flip), unknown 34,498 -> 34,497,
  no free/excluded flips anywhere else; root 27 stays 119/119;
* per-root coverage: free/uncovered thirds improve exactly at the four
  groups class 8730 serves (root 38: 13/106 -> 15/104, root 5: 8/111 ->
  10/109); every other root byte-identical;
* the frozen greedy scheduler deltas are recorded as bookkeeping
  (joint greedy 36,902 -> 36,968, worklist 64,665 -> 64,609, per-root
  remaining decreases at roots 5 (-5), 25 (-2), 38 (-4)).

No unknown verdict is asserted anywhere.  The standard 11x11 empty board
and every one of the 19 central-reply roots stay UNKNOWN; free_now /
coverage quantities are scheduling bookkeeping derived from exact LOSS
verdicts, not root verdict claims.
"""

import csv
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]

BASE_EXP = ROOT / "research/experiments/n11-centralreply-class34269-b30loss43-adoption-reaudit-20261124"
BASE_OUT = BASE_EXP / "reaudit/output"
BASE_CACHE = BASE_EXP / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-20261124.cache"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-20261124.cache"
INCR = EXP / "output/increment-b32loss54-20261124.cache"
MANIFEST = EXP / "output/increments-manifest.json"
KIT1 = ROOT / "research/experiments/n11-centralreply-closure-class8730-batch32-20261124"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_REFRESH_SCRIPT = BASE_EXP / "reaudit/scripts/refresh_adoption_b30loss43.py"
SCEN_REFRESH_SCRIPT = EXP / "reaudit/scripts/refresh_adoption_b32loss54.py"

BASE_CACHE_SHA = "7bdfa2366ef9c24b48a610d078104227555dd52ec18a566082cef2f906aab0f7"
SCEN_CACHE_SHA = "1ded9a083feabc095dd998c92002b47efc05b8666adf030501bcffc2873a9dd6"
INCR_SHA = "ca4af3e7704f2a72649b8386c83916ea129152bfc85c1363a30f4be54590dadb"
MANIFEST_SHA = "3f906dc81e1eb74a2f0a74113e474e215673755eee7d719e42ce42424e86a2f4"
BASE_SUMMARY_SHA = "8349371ca09556570f0f50f58eab4444d0e7e277a5a7e0900585f430aef3e756"
BASE_CLOSURE_SHA = "8f68f594834ba6aa85a09cea9c45ae86866f3fa18cfa97e79643b66976a4743c"
BASE_PRC_SHA = "1bc7a5e58462427333bdca95adab7470d0d3ac28bfff49866ba6efde6fd4f367"
BASE_WORKLIST_SHA = "bac10aee9964bde0dbfa914e0d046b2f5380638ed20d3e3273823659f3abb708"
SCEN_SUMMARY_SHA = "74f5dd9b6d8752964ca622ebb40388694aac1bd787d615e184a06e25693a5179"
SCEN_CLOSURE_SHA = "284bb069d7c0efb7bb04addd7e1947716dfd2db5f0caf47ca3942bfa5cfa493f"
SCEN_PRC_SHA = "096a9c37c1e6624ec1d17eaed957ceaf331f4ed7c5787a0c88fd5bdc6075e9c0"
SCEN_WORKLIST_SHA = "87c2ebd63015ca399a13e0ef561796bce655003ff69cb01b8f8177818f1bf368"
BASE_REFRESH_SHA = "d45832a6569267d7a8187cb9935acab177d73395af4485bf496ba2661ec29c5b"
SCEN_REFRESH_SHA = "41bf706fd0e2d0eb831ecfdf35eb52bf448dece8107b792856fb2d65fe93a366"
KIT1_MANIFEST_SHA = "7c2c159ae24bab8836e23a8e2502615d62650eb4fb555979513ca55f71e7dec8"
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
BOARD_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
CLASS_IDX = 8730
ADOPTED_ROWS = 54
ADOPTED_TOTAL_NODES = 223769637
BASE_KNOWN_LOSS_S5 = [144458, 212464, 310606, 311726]
NEWLY_RESOLVED_UPD8_S5 = [285539, 311727]
MERGE_AUDIT_SHA = "5ebfdbfb4aefefb2cd1d6c020f1bbe946f60c1196ee2bd2b63a998fe0305ae52"
STATUS_BEFORE = {"excluded": 390, "excluded_now": 23, "free_now": 38, "unknown": 34498}
STATUS_AFTER = {"excluded": 390, "excluded_now": 23, "free_now": 39, "unknown": 34497}
UPD8_RESOLVED_BEFORE = 185
UPD8_RESOLVED_AFTER = 187
UPD8_REMAINING_BEFORE = 31674
UPD8_REMAINING_AFTER = 31672
JOINT_GREEDY_BEFORE = 36902
JOINT_GREEDY_AFTER = 36968
WORKLIST_BEFORE = 64665
WORKLIST_AFTER = 64609
KNOWN_UNIVERSE_BEFORE = 627
KNOWN_UNIVERSE_AFTER = 681
CACHE_IN_UNIVERSE_BEFORE = 604
CACHE_IN_UNIVERSE_AFTER = 658
UNIQUE_GROUPS_BEFORE = 2119
UNIQUE_GROUPS_AFTER = 2115
PER_ROOT_REMAINING_DELTA = {"5": -5, "25": -2, "38": -4}
PER_ROOT_COVERAGE_DELTA = {
    "38": {"free": [13, 15], "uncovered": [106, 104], "greedy": [3068, 3014]},
    "5": {"free": [8, 10], "uncovered": [111, 109], "greedy": [2938, 2884]},
}
CLOSURE_ROWS_BEFORE = 808
CLOSURE_ROWS_AFTER = 807


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fail(msg: str):
    print(f"ABORT {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_cache(path: Path):
    cache = {}
    for row in csv.reader(path.open(encoding="utf-8-sig", newline="")):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 6 or row[0] != "s5verdict":
            fail(f"invalid cache row: {row}")
        cache[(int(row[1]), int(row[2]))] = (int(row[4]), int(row[5]))
    return cache


def _kit_candidates(kit_dir: Path, rel: str):
    cands = [kit_dir / rel, ROOT / rel]
    stripped = rel.split("research/experiments/", 1)[-1]
    if stripped.startswith("n11"):
        stripped = stripped[stripped.index("/") + 1:]
    cands.append(kit_dir / stripped)
    cands.append(kit_dir / "output" / stripped)
    return cands


def verify_kit(dirp: Path, manifest_sha: str, files_expected: int):
    if sha(dirp / "MANIFEST-sha256.txt") != manifest_sha:
        fail(f"kit {dirp.name} MANIFEST sha drift")
    n = 0
    for line in (dirp / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        want, rel = line.split(None, 1)
        p = next((c for c in _kit_candidates(dirp, rel) if c.is_file()), None)
        if p is None:
            fail(f"kit {dirp.name} file missing: {rel}")
        if sha(p) != want:
            fail(f"kit {dirp.name} sha drift at {rel}")
        n += 1
    if n != files_expected:
        fail(f"kit {dirp.name} files {n} != {files_expected}")
    return n


def rerun_refresh(script: Path, script_sha: str, tmp_name: str):
    """Re-execute a published refresh script byte-verbatim in a scratch tree."""
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
    # --- sha pins over every published artifact ---------------------------
    pins = [
        ("base cache", BASE_CACHE, BASE_CACHE_SHA),
        ("scenario cache", SCEN_CACHE, SCEN_CACHE_SHA),
        ("increment", INCR, INCR_SHA),
        ("manifest", MANIFEST, MANIFEST_SHA),
        ("base refresh-summary", BASE_OUT / "refresh-summary.json", BASE_SUMMARY_SHA),
        ("base closure-classes", BASE_OUT / "closure-classes.csv", BASE_CLOSURE_SHA),
        ("base per-root-coverage", BASE_OUT / "per-root-coverage.csv", BASE_PRC_SHA),
        ("scenario refresh-summary", EXP / "reaudit/output/refresh-summary.json", SCEN_SUMMARY_SHA),
        ("scenario closure-classes", EXP / "reaudit/output/closure-classes.csv", SCEN_CLOSURE_SHA),
        ("scenario per-root-coverage", EXP / "reaudit/output/per-root-coverage.csv", SCEN_PRC_SHA),
        ("base refresh script", BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA),
        ("scenario refresh script", SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA),
        ("graph", GRAPH, GRAPH_SHA),
        ("update8", UPDATE8, UPDATE8_SHA),
        ("board source", BOARD_SOURCE, BOARD_SHA),
        ("policy", POLICY, POLICY_SHA),
        ("quarantine", QUARANTINE, QUARANTINE_SHA),
        ("merge-audit run1", EXP / "output/merge-audit-run1.json", MERGE_AUDIT_SHA),
        ("merge-audit run2", EXP / "output/merge-audit-run2.json", MERGE_AUDIT_SHA),
        ("merge-audit run3", EXP / "output/merge-audit-run3.json", MERGE_AUDIT_SHA),
    ]
    for name, p, want in pins:
        got = sha(p)
        if got != want:
            fail(f"{name} sha drift: {got} != {want}")
    k1 = verify_kit(KIT1, KIT1_MANIFEST_SHA, 193)

    manifest = json.loads(MANIFEST.read_text())
    batch = manifest["batches"][0]
    adopted_ids = manifest["loss_ids"]
    win_ids = manifest["win_ids"]
    if len(adopted_ids) != ADOPTED_ROWS or win_ids:
        fail("manifest adopted/WIN id counts drift (batch-32 must be loss-only)")
    if batch["class_index"] != CLASS_IDX:
        fail("manifest batch class drift")
    if manifest.get("full_packet_eq_loss_only") is not True:
        fail("manifest full_packet_eq_loss_only must be true for batch-32")
    if batch["total_nodes_pass_one"] != ADOPTED_TOTAL_NODES or batch["total_nodes_pass_two"] != ADOPTED_TOTAL_NODES:
        fail("manifest node totals drift")

    # --- refresh re-execution (double-run determinism) ---------------------
    base_tmp = rerun_refresh(BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA, ".dpverify-base-b30loss43")
    scen_tmp = rerun_refresh(SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA, ".dpverify-scen-b32loss54")
    checks = [
        (base_tmp / "refresh-summary.json", BASE_OUT / "refresh-summary.json", BASE_SUMMARY_SHA),
        (base_tmp / "closure-classes.csv", BASE_OUT / "closure-classes.csv", BASE_CLOSURE_SHA),
        (base_tmp / "per-root-coverage.csv", BASE_OUT / "per-root-coverage.csv", BASE_PRC_SHA),
        (base_tmp / "probe-worklist.csv", None, BASE_WORKLIST_SHA),
        (scen_tmp / "refresh-summary.json", EXP / "reaudit/output/refresh-summary.json", SCEN_SUMMARY_SHA),
        (scen_tmp / "closure-classes.csv", EXP / "reaudit/output/closure-classes.csv", SCEN_CLOSURE_SHA),
        (scen_tmp / "per-root-coverage.csv", EXP / "reaudit/output/per-root-coverage.csv", SCEN_PRC_SHA),
        (scen_tmp / "probe-worklist.csv", EXP / "reaudit/output/probe-worklist.csv", SCEN_WORKLIST_SHA),
    ]
    for tmp_out, pub, want_sha in checks:
        if sha(tmp_out) != want_sha:
            fail(f"refresh re-execution output drift: {tmp_out.name} ({tmp_out.parent.parent.name})")
        if pub is not None and sha(pub) != want_sha:
            fail(f"published output drifted from pin: {pub}")
    shutil.rmtree(ROOT / "research/experiments/.dpverify-base-b30loss43")
    shutil.rmtree(ROOT / "research/experiments/.dpverify-scen-b32loss54")

    # --- cache relation: SCEN == BASE + the 43 increment rows --------------
    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    incr = load_cache(INCR)
    if len(base) != 6448 or len(scen) != 6502 or len(incr) != 54:
        fail(f"cache sizes drift: base {len(base)} scen {len(scen)} incr {len(incr)}")
    for key, row in incr.items():
        if row[0] != 2:
            fail(f"increment contains a non-LOSS row: {key}")
        if key in base:
            fail(f"increment key already in BASE: {key}")
        if scen.get(key) != row:
            fail(f"increment row not taken verbatim into scenario cache: {key}")
    merged = dict(base)
    for key, row in incr.items():
        merged[key] = row
    if merged != scen:
        fail("scenario cache != BASE rows + increment rows (set difference)")
    wins = sum(1 for v in scen.values() if v[0] == 1)
    losses = len(scen) - wins
    if (wins, losses) != (158, 6344):
        fail(f"scenario verdict counts {wins}/{losses} != 158/6,344")
    for key, row in incr.items():
        v, n = row
        nodes = scen[key][1]
        if n != nodes:
            fail(f"scenario nodes for {key} differ from increment: {nodes} != {n}")

    # --- Board arithmetic for class 8730 ----------------------------------
    sys.path.insert(0, str(BOARD_SOURCE.parent))
    sys.path.insert(0, str(POLICY.parent))
    from independent import Board  # noqa: E402
    from s5_evidence_policy import quarantined_cache_keys  # noqa: E402
    quarantined = quarantined_cache_keys()
    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s4_masks = g["s4_masks"]
    s5_masks = g["s5_masks"]
    mask_to_index = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}
    lo, hi = s4_masks[CLASS_IDX]
    board = Board(11)
    children = board.children(lo | (hi << 64))
    child_keys = {(c & ((1 << 64) - 1), c >> 64) for c in children}
    bkeys = json.loads((KIT1 / "input/batch-keys.json").read_text())["keys"]
    batch_keys = {(int(e["lo"]), int(e["hi"])) for e in bkeys}
    if len(batch_keys) != 54 or not batch_keys <= child_keys:
        fail("batch-32 key set not inside the Board-regenerated class-8730 child boundary")
    unknown_base = {k for k in child_keys if k not in base}
    unknown_scen = {k for k in child_keys if k not in scen}
    if len(unknown_base) != 54 or unknown_base != batch_keys:
        fail("BASE unknown children of 8730 != the 54 batch keys")
    if unknown_scen:
        fail(f"scenario unknown children of 8730 = {len(unknown_scen)} != 0 (class must be fully LOSS)")
    adopted_keys = batch_keys - unknown_scen
    if len(adopted_keys) != ADOPTED_ROWS or {mask_to_index[k] for k in adopted_keys} != {mask_to_index[k] for k in incr}:
        fail("adopted key set != increment key set (child-boundary mismatch)")
    adopted_idx = sorted(mask_to_index[k] for k in adopted_keys)
    base_known = child_keys - batch_keys
    if len(base_known) != 4 or sorted(mask_to_index[k] for k in base_known) != BASE_KNOWN_LOSS_S5:
        fail("the 4 base-known LOSS children of 8730 != the pinned s5 indices")
    if all(base.get(k, (0, 0))[0] == 2 for k in base_known) is False:
        fail("a base-known child of 8730 is not an exact LOSS in BASE")
    for k in child_keys:
        if scen[k][0] != 2:
            fail(f"class 8730 child not LOSS in scenario: {k}")
    if any(k in quarantined for k in child_keys):
        fail("a quarantined key sits inside the class-8730 child boundary")

    # --- update8 refresh deltas ---------------------------------------------
    update8 = json.loads(UPDATE8.read_text())
    required = set(update8["required_new_s5"])
    base_summary = json.loads(BASE_OUT.joinpath("refresh-summary.json").read_text())
    scen_summary = json.loads((EXP / "reaudit/output/refresh-summary.json").read_text())
    rb = base_summary["frozen_update8_refresh"]
    rs = scen_summary["frozen_update8_refresh"]
    if rb["resolved_count"] != UPD8_RESOLVED_BEFORE or rs["resolved_count"] != UPD8_RESOLVED_AFTER:
        fail("update8 resolved_count drift vs pins")
    if rb["remaining_now"] != UPD8_REMAINING_BEFORE or rs["remaining_now"] != UPD8_REMAINING_AFTER:
        fail("update8 remaining_now drift vs pins")
    newly = sorted(set(rs["resolved_among_baseline_requirement"]) - set(rb["resolved_among_baseline_requirement"]))
    lost = set(rb["resolved_among_baseline_requirement"]) - set(rs["resolved_among_baseline_requirement"])
    if newly != NEWLY_RESOLVED_UPD8_S5:
        fail(f"newly resolved update8 set != the pinned adopted-in-requirement set: {newly}")
    if lost:
        fail(f"update8 resolution LOST rows: {sorted(lost)}")
    if not set(newly) <= set(adopted_idx):
        fail("newly resolved update8 set is not a subset of the adopted s5 set")
    if rb["remaining_now"] - rs["remaining_now"] != len(NEWLY_RESOLVED_UPD8_S5):
        fail("update8 remaining delta != the pinned newly-resolved count")

    # --- class status / universe metrics --------------------------------------
    cb, cs = base_summary["class_status_counts"], scen_summary["class_status_counts"]
    if cb != STATUS_BEFORE or cs != STATUS_AFTER:
        fail(f"class status counts drift vs the pinned transition: {cb} {cs}")
    if scen_summary["board_verification"] != {"free_candidates": 39, "board_verified_free": 39, "rejected": {}}:
        fail("scenario board verification shape drift")
    if base_summary["board_verification"] != {"free_candidates": 38, "board_verified_free": 38, "rejected": {}}:
        fail("base board verification shape drift")
    if scen_summary["inputs"]["cache_rows"] != 6502 or scen_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_AFTER \
            or scen_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_AFTER:
        fail("scenario inputs metrics drift")
    if base_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["cache_rows"] != 6448:
        fail("base inputs metrics drift")
    bcv = base_summary["inputs"]["cache_verdicts"]
    scv = scen_summary["inputs"]["cache_verdicts"]
    if bcv != {"1": 158, "2": 6290} or scv != {"1": 158, "2": 6344}:
        fail("cache verdict counts drift")
    if rs["remaining_now"] != UPD8_REMAINING_AFTER or rb["remaining_now"] != UPD8_REMAINING_BEFORE:
        fail("update8 remaining recheck")

    # per-root coverage: identical free/uncovered thirds everywhere
    prc_pairs = list(zip(
        csv.DictReader(BASE_OUT.joinpath("per-root-coverage.csv").open()),
        csv.DictReader((EXP / "reaudit/output/per-root-coverage.csv").open())))
    prc_delta = {}
    for b, s in prc_pairs:
        if b["first"] != s["first"]:
            fail("per-root rows misaligned")
        if b["free_now"] != s["free_now"] or b["uncovered"] != s["uncovered"] \
                or b["individual_greedy_union"] != s["individual_greedy_union"]:
            prc_delta[s["first"]] = {
                "free": [int(b["free_now"]), int(s["free_now"])],
                "uncovered": [int(b["uncovered"]), int(s["uncovered"])],
                "greedy": [int(b["individual_greedy_union"]), int(s["individual_greedy_union"])],
            }
    if prc_delta != PER_ROOT_COVERAGE_DELTA:
        fail(f"per-root coverage delta {prc_delta} != the pinned class-8730 effect {PER_ROOT_COVERAGE_DELTA}")
    for root, d in prc_delta.items():
        if d["free"][1] - d["free"][0] != 2 or d["uncovered"][0] - d["uncovered"][1] != 2:
            fail(f"root {root} did not gain exactly the two class-8730 thirds it serves")
    root27 = [s for b, s in prc_pairs if s["first"] == "27"][0]
    if root27["free_now"] != "119" or root27["uncovered"] != "0":
        fail("root 27 coverage regressed")
    # per-root greedy remaining decreases only at roots 12 / 24
    rb_pr = rb["per_root_remaining"]
    rs_pr = rs["per_root_remaining"]
    deltas = {k: rs_pr[k] - rb_pr[k] for k in rb_pr if rs_pr[k] != rb_pr[k]}
    if deltas != PER_ROOT_REMAINING_DELTA:
        fail(f"per-root remaining delta {deltas} != pinned {PER_ROOT_REMAINING_DELTA}")
    if any(v > 0 for v in deltas.values()):
        fail("a per-root remaining INCREASED (coverage regression)")

    # --- closure-classes table diff --------------------------------------------
    def read_closure(p: Path):
        rows = {}
        for r in csv.DictReader(p.open()):
            rows[int(r["class_index"])] = r
        return rows

    cb_t = read_closure(BASE_OUT / "closure-classes.csv")
    cs_t = read_closure(EXP / "reaudit/output/closure-classes.csv")
    if len(cb_t) != CLOSURE_ROWS_BEFORE or len(cs_t) != CLOSURE_ROWS_AFTER:
        fail(f"closure table row counts {len(cb_t)}/{len(cs_t)} != {CLOSURE_ROWS_BEFORE}/{CLOSURE_ROWS_AFTER}")
    left = sorted(set(cb_t) - set(cs_t))
    entered = sorted(set(cs_t) - set(cb_t))
    if left != [CLASS_IDX]:
        fail(f"closure table left != exactly the freed class [8730]: {left}")
    if entered:
        fail(f"closure table entered non-empty: {entered}")
    if int(cb_t[CLASS_IDX]["unknown_now"]) != 54 or int(cb_t[CLASS_IDX]["groups_served_count"]) != 4:
        fail("the left class-8730 row is not the pinned 54-unknown / 4-group base row")
    changed, rank_churn, stable, gs_churn = [], 0, 0, []
    for ci, brow in sorted(cb_t.items()):
        if ci == CLASS_IDX:
            continue
        srow = cs_t[ci]
        diff = {k: (brow[k], srow[k]) for k in brow if brow[k] != srow[k]}
        if not diff:
            stable += 1
            continue
        if set(diff) == {"class_rank"}:
            rank_churn += 1
            continue
        if set(diff) == {"class_rank", "groups_served_count"} and \
                int(diff["groups_served_count"][1]) < int(diff["groups_served_count"][0]):
            gs_churn.append({"class_index": ci,
                             "groups_served_count": [int(diff["groups_served_count"][0]),
                                                     int(diff["groups_served_count"][1])]})
            continue
        if "unknown_now" not in diff:
            fail(f"class {ci} changed unexpected columns: {diff}")
        b_unk, s_unk = int(diff["unknown_now"][0]), int(diff["unknown_now"][1])
        clo, chi = s4_masks[ci]
        kids = board.children(clo | (chi << 64))
        kids_keys = {(c & ((1 << 64) - 1), c >> 64) for c in kids}
        own = len(kids_keys & set(adopted_keys))
        if (b_unk - s_unk) != own or own == 0:
            fail(f"class {ci} unknown delta {b_unk}->{s_unk} != own adopted membership {own}")
        changed.append({"class_index": ci, "unknown_before": b_unk, "unknown_after": s_unk,
                        "own_adopted": own})
    if changed != [{"class_index": 8811, "unknown_before": 54, "unknown_after": 52,
                    "own_adopted": 2}]:
        fail(f"changed-class set != exactly the pinned class-8811 own-2 delta: {changed}")
    # the freed class must not appear in the scenario closure table via any
    # served group (it is board-verified free; its four groups left the
    # nonfree universe entirely)
    if CLASS_IDX in cs_t:
        fail("class 8730 still present in the scenario closure table")

    # --- metric deltas -------------------------------------------------------------
    jb, js = base_summary["joint_greedy"], scen_summary["joint_greedy"]
    if jb["greedy_union_size"] != JOINT_GREEDY_BEFORE or js["greedy_union_size"] != JOINT_GREEDY_AFTER:
        fail("joint greedy union size drift vs pins")
    if base_summary["worklist_total"] != WORKLIST_BEFORE or scen_summary["worklist_total"] != WORKLIST_AFTER:
        fail("worklist totals drift vs pins")
    if jb["unique_groups"] != UNIQUE_GROUPS_BEFORE or js["unique_groups"] != UNIQUE_GROUPS_AFTER:
        fail("greedy group universe delta != the pinned -4 (the class-8730 groups became free)")
    if rb["groups_free_now"] != rs["groups_free_now"]:
        fail("groups_free_now changed")
    if rs.get("win_hit_groups", rb.get("win_hit_groups")) not in ([], None):
        fail("win_hit_groups non-empty (a WIN was consumed)")

    # --- emit decomp -----------------------------------------------------------------
    out = {
        "schema": "b32loss54-adoption-decomp-deltas-v1",
        "scenario": "ADOPTED-CANONICAL",
        "batch": {"batch": 32, "class_index": CLASS_IDX, "probed_rows": 54,
                  "adopted_loss_rows": ADOPTED_ROWS, "unadopted_win_rows": 0,
                  "adopted_total_nodes_per_pass": ADOPTED_TOTAL_NODES,
                  "decisive_labels": "54 LOSS @15M (Part DM drive-1 kit raws, 2-pass fresh-cold; "
                                     "WIN 0 / EXHAUSTED 0 / MISMATCH 0 / TRUNCATED 0)",
                  "adopted_loss_ids": adopted_ids, "unadopted_win_ids": win_ids},
        "cache": {"base_sha256": BASE_CACHE_SHA, "scenario_sha256": SCEN_CACHE_SHA,
                  "base_rows": len(base), "scenario_rows": len(scen), "increment_rows": len(incr),
                  "verdict_counts": {"WIN": 158, "LOSS": 6344},
                  "relation": "scenario == base rows + the 54 increment rows verbatim (no other row changed)",
                  "merge_audit_runs": 3, "merge_audit_sha256_each": MERGE_AUDIT_SHA},
        "class_8730": {"children_total": len(child_keys),
                       "unknown_before": 54, "unknown_after": 0,
                       "adopted_own": 54,
                       "base_known_loss_s5": BASE_KNOWN_LOSS_S5,
                       "status_before": "unknown",
                       "status_after": "free_now (Board-verified by the reaudit refresh: "
                                       "free_now 38 -> 39, board_verified 39/39, rejected 0)",
                       "groups_served": [[5, 58], [5, 62], [38, 55], [38, 65]],
                       "per_root_coverage_effect": {"first 5": "free 8 -> 10, uncovered 111 -> 109",
                                                    "first 38": "free 13 -> 15, uncovered 106 -> 104"},
                       "not_a_root_verdict": "free_now is Board-derived scheduling bookkeeping over exact "
                                             "LOSS verdicts; no root verdict and no coverage claim is made"},
        "closure_table": {"rows_before": CLOSURE_ROWS_BEFORE, "rows_after": CLOSURE_ROWS_AFTER,
                          "left": [CLASS_IDX], "entered": [],
                          "left_reason": "class 8730 turned free_now (all 58 children exact LOSS in the "
                                         "scenario cache) and leaves the nonfree closure ranking",
                          "unknown_changed_classes": changed,
                          "rank_churn_only_rows": rank_churn,
                          "groups_served_decrease_churn": gs_churn,
                          "fully_stable_rows": stable},
        "update8": {"resolved_before": UPD8_RESOLVED_BEFORE, "resolved_after": UPD8_RESOLVED_AFTER,
                    "newly_resolved_s5": NEWLY_RESOLVED_UPD8_S5,
                    "newly_resolved_within_adopted": True,
                    "remaining_before": UPD8_REMAINING_BEFORE, "remaining_after": UPD8_REMAINING_AFTER,
                    "groups_free_now_static": 131},
        "class_status_counts_before": STATUS_BEFORE,
        "class_status_counts_after": STATUS_AFTER,
        "metrics": {"joint_greedy_union_size": [JOINT_GREEDY_BEFORE, JOINT_GREEDY_AFTER],
                    "worklist_total": [WORKLIST_BEFORE, WORKLIST_AFTER],
                    "known_universe_indices": [KNOWN_UNIVERSE_BEFORE, KNOWN_UNIVERSE_AFTER],
                    "cache_rows_in_universe": [CACHE_IN_UNIVERSE_BEFORE, CACHE_IN_UNIVERSE_AFTER],
                    "unique_groups": [UNIQUE_GROUPS_BEFORE, UNIQUE_GROUPS_AFTER],
                    "per_root_remaining_delta": PER_ROOT_REMAINING_DELTA,
                    "per_root_coverage_delta": PER_ROOT_COVERAGE_DELTA,
                    "note": "greedy/worklist deltas are frozen-scheduler bookkeeping after the 54 frontier "
                            "slots resolve; the joint greedy union INCREASES (36,902 -> 36,968) because "
                            "class-8730's members leave the nonfree best-option set and re-selection churns "
                            "the greedy choice; per-root free/uncovered thirds improve exactly at the four "
                            "class-8730 groups; root 27 stays 119/119"},
        "verification": {"kit_files_verified": {"kit1": k1},
                         "refresh_scripts_reexecuted": [BASE_REFRESH_SHA, SCEN_REFRESH_SHA],
                         "refresh_outputs_byte_identical": True,
                         "board_child_regeneration": "class-8730 canonical 58-child 5-stone boundary regenerated via Board(11).children"},
        "interpretation_guard":
            "only the 54 fresh LOSS rows are consumed into the canonical cache by this Part; "
            "batch-32 has no WIN row, so no verdict stays unconsumed and no scrutiny gate is "
            "in scope; class 8730 turns free_now ONLY as Board-derived scheduling bookkeeping "
            "over exact LOSS verdicts (no root verdict, no coverage claim); the 508 rows and "
            "coverage quantities quoted here are bookkeeping, never verdicts; no update8 "
            "resolution was lost; per-root coverage improved exactly at the four class-8730 "
            "groups and regressed nowhere (root 27 stays 119/119); 11x11 stays UNKNOWN",
    }
    (EXP / "output/decomp-deltas-b32loss54-adoption.json").write_text(
        json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("DECOMP OK changed=%d rank_churn=%d gs_churn=%d stable=%d" % (len(changed), rank_churn, len(gs_churn), stable))
    print("class8730: unknown 54 -> 0, own adopted 54, free_now board-verified; left=[8730]")


if __name__ == "__main__":
    main()
