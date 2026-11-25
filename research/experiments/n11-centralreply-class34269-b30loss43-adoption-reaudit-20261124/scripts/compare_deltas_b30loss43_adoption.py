#!/usr/bin/env python3
"""Part DN adoption delta extraction: BASE (Part DL, b31loss51) vs SCENARIO (b30loss43).

Fail-closed machine recomputation of exactly what the batch-30 (class 34269)
43-LOSS canonical adoption changed, from published bytes only:

* every published artifact sha-pinned (the Part DN experiment outputs, the
  Part DL BASE reaudit outputs, both chain caches, the increment, the
  increments manifest, the three published probe kits MANIFESTs verified
  file-by-file 199+34+15 files, graph/update8/board/policy/quarantine pins);
* the published Part DL refresh script (reaudit/scripts/refresh_adoption_
  b31loss51.py, sha e92fa80e...) and the published Part DN refresh fork
  (reaudit/scripts/refresh_adoption_b30loss43.py, sha d45832a6...) are
  RE-EXECUTED byte-verbatim in isolated scratch trees against their pinned
  inputs, and all eight outputs (two x refresh-summary/closure-classes/
  per-root-coverage/probe-worklist) must be byte-identical to the published /
  regenerated pins before any delta is emitted (double-run determinism);
* SCEN cache == BASE cache rows + exactly the 43 increment rows (verdict
  agreement everywhere; 6,448 rows, WIN 158 / LOSS 6,290);
* the class-34269 arithmetic is independently recomputed from the frozen
  dependency graph with the integer-geometry Board: the class's canonical
  5-stone children are regenerated, exactly 54 are unknown against BASE
  (== the batch-30 key set), exactly 43 resolve to LOSS in the scenario
  (== the adopted key set; node totals 346,729,500 per pass on the raws,
  pinned by the maker), and the remaining exactly-11 unknowns are the
  unconsumed WIN children (s5 indices pinned here);
* every closure-classes.csv row that changes unknown_now is asserted to be a
  Board-verified holder of adopted keys with exact own-membership arithmetic
  (delta == children-of-class intersect adopted set); rank churn is pure
  bookkeeping and counted;
* update8 refresh: resolved_among_baseline_requirement grows from 142 to 185
  and the newly resolved set is asserted to be exactly the 43 adopted s5
  indices; remaining 31,717 -> 31,674; known-universe 584 -> 627;
* class_status counts static (excluded 390 / excluded_now 23 / free_now 38
  board-verified / unknown 34,498), root 27 stays 119/119, no free/excluded
  flips anywhere;
* the frozen greedy scheduler deltas are recorded as bookkeeping
  (joint greedy 36,854 -> 36,902, worklist 64,711 -> 64,665, per-root
  remaining decreases only at roots 12 (-129) and 24 (-86)).

No unknown verdict is asserted anywhere.  The eleven probe-level WINs stay
UNCONSUMED (verdicts unconsumed by the adoption; consumed nowhere), class
34269 is NOT freed (11 unconsumed WIN children remain), and the standard
11x11 empty board stays UNKNOWN.
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

BASE_EXP = ROOT / "research/experiments/n11-centralreply-class5804-b31loss51-adoption-reaudit-20261124"
BASE_OUT = BASE_EXP / "reaudit/output"
BASE_CACHE = BASE_EXP / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-20261124.cache"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-20261124.cache"
INCR = EXP / "output/increment-b30loss43-20261124.cache"
MANIFEST = EXP / "output/increments-manifest.json"
KIT1 = ROOT / "research/experiments/n11-centralreply-closure-class34269-batch30-20261123"
KIT2 = ROOT / "research/experiments/n11-centralreply-closure-class34269-batch30-exh6-20m-20261124"
KIT3 = ROOT / "research/experiments/n11-centralreply-closure-class34269-batch30-exh1-25m-20261124"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_REFRESH_SCRIPT = BASE_EXP / "reaudit/scripts/refresh_adoption_b31loss51.py"
SCEN_REFRESH_SCRIPT = EXP / "reaudit/scripts/refresh_adoption_b30loss43.py"

BASE_CACHE_SHA = "60222707dd13902103fc8f7ef11c8487ec1be531ad0711e23e50c32154e30b84"
SCEN_CACHE_SHA = "7bdfa2366ef9c24b48a610d078104227555dd52ec18a566082cef2f906aab0f7"
INCR_SHA = "2dc3a15685c5df8a716a74729833cfb8cd1b19aba793213feebf53b32ea07740"
MANIFEST_SHA = "800d77e99680260fd89f7315ad6a4f19f1d5af98cae7693913f9c4eec5a39e6f"
BASE_SUMMARY_SHA = "fea0b0d4473b34447556f3a3e8b9ecc7c57c59221b18c4bb58222e0149b2e4bc"
BASE_CLOSURE_SHA = "50841fa47676be8af145f1f8f751b0d96f75e94417990418cbe1d2a52bd4d389"
BASE_PRC_SHA = "136e308a332c8ab6fe877f3ef3a3b361770931285d91a0d12a59a6dd9707b487"
BASE_WORKLIST_SHA = "006ccd78d061c22838b3cee7701a91649d35abf3c8d56cecbb05931b604846d5"
SCEN_SUMMARY_SHA = "8349371ca09556570f0f50f58eab4444d0e7e277a5a7e0900585f430aef3e756"
SCEN_CLOSURE_SHA = "8f68f594834ba6aa85a09cea9c45ae86866f3fa18cfa97e79643b66976a4743c"
SCEN_PRC_SHA = "1bc7a5e58462427333bdca95adab7470d0d3ac28bfff49866ba6efde6fd4f367"
SCEN_WORKLIST_SHA = "bac10aee9964bde0dbfa914e0d046b2f5380638ed20d3e3273823659f3abb708"
BASE_REFRESH_SHA = "e92fa80e7d8d9ac46f9dd66b90fab6cebab349948fdb14a916f180c2611b81e4"
SCEN_REFRESH_SHA = "d45832a6569267d7a8187cb9935acab177d73395af4485bf496ba2661ec29c5b"
KIT1_MANIFEST_SHA = "330128aa1bcff45b52dac46e7e8bf9bbf57836f90d8f342fa269ee85ae77d845"
KIT2_MANIFEST_SHA = "bb88fba3338a2e4188cd9a6a6fc8a1208507ccaa42fac36e9facb3fd0833a907"
KIT3_MANIFEST_SHA = "e05c4259cdc5b004fc340fb770044ba57e443de0591c7d57a4b6a3b349707375"
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
BOARD_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
CLASS_IDX = 34269
ADOPTED_ROWS = 43
WIN_S5 = [38891, 178184, 355050, 809575, 900276, 900687, 941211, 956329, 957713, 958080, 958143]
ADOPTED_TOTAL_NODES = 346729500
MERGE_AUDIT_SHA = "6c35b897262cc80b1374a7cf1e8fc0eb1ae7edfef1e1b2b92c48d9c613619041"
STATUS_TRANSITIONS = {"excluded": 390, "excluded_now": 23, "free_now": 38, "unknown": 34498}
UPD8_RESOLVED_BEFORE = 142
UPD8_RESOLVED_AFTER = 185
UPD8_REMAINING_BEFORE = 31717
UPD8_REMAINING_AFTER = 31674
JOINT_GREEDY_BEFORE = 36854
JOINT_GREEDY_AFTER = 36902
WORKLIST_BEFORE = 64711
WORKLIST_AFTER = 64665
KNOWN_UNIVERSE_BEFORE = 584
KNOWN_UNIVERSE_AFTER = 627
CACHE_IN_UNIVERSE_BEFORE = 561
CACHE_IN_UNIVERSE_AFTER = 604
PER_ROOT_REMAINING_DELTA = {"12": -129, "24": -86}
CLOSURE_ROWS = 808


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
    k1 = verify_kit(KIT1, KIT1_MANIFEST_SHA, 199)
    k2 = verify_kit(KIT2, KIT2_MANIFEST_SHA, 34)
    k3 = verify_kit(KIT3, KIT3_MANIFEST_SHA, 15)

    manifest = json.loads(MANIFEST.read_text())
    batch = manifest["batches"][0]
    adopted_ids = manifest["loss_ids"]
    win_ids = manifest["win_ids"]
    if len(adopted_ids) != ADOPTED_ROWS or len(win_ids) != len(WIN_S5):
        fail("manifest adopted/WIN id counts drift")
    if batch["class_index"] != CLASS_IDX:
        fail("manifest batch class drift")
    if [r["s5_index"] for r in manifest["unadopted_win_rows"]] != WIN_S5:
        fail("manifest unadopted WIN s5 index list drift")
    if batch["total_nodes_pass_one"] != ADOPTED_TOTAL_NODES or batch["total_nodes_pass_two"] != ADOPTED_TOTAL_NODES:
        fail("manifest node totals drift")

    # --- refresh re-execution (double-run determinism) ---------------------
    base_tmp = rerun_refresh(BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA, ".dnverify-base-b31loss51")
    scen_tmp = rerun_refresh(SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA, ".dnverify-scen-b30loss43")
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
    shutil.rmtree(ROOT / "research/experiments/.dnverify-base-b31loss51")
    shutil.rmtree(ROOT / "research/experiments/.dnverify-scen-b30loss43")

    # --- cache relation: SCEN == BASE + the 43 increment rows --------------
    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    incr = load_cache(INCR)
    if len(base) != 6405 or len(scen) != 6448 or len(incr) != 43:
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
    if (wins, losses) != (158, 6290):
        fail(f"scenario verdict counts {wins}/{losses} != 158/6,290")
    for key, row in incr.items():
        v, n = row
        nodes = scen[key][1]
        if n != nodes:
            fail(f"scenario nodes for {key} differ from increment: {nodes} != {n}")

    # --- Board arithmetic for class 34269 ----------------------------------
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
    if len(batch_keys) != 54 or batch_keys != child_keys:
        fail("batch-30 key set != the Board-regenerated class-34269 child boundary")
    unknown_base = {k for k in child_keys if k not in base}
    unknown_scen = {k for k in child_keys if k not in scen}
    if len(unknown_base) != 54 or unknown_base != batch_keys:
        fail("BASE unknown children of 34269 != the 54 batch keys")
    if len(unknown_scen) != len(WIN_S5):
        fail(f"scenario unknown children of 34269 = {len(unknown_scen)} != 11")
    scen_unknown_idx = sorted(mask_to_index[k] for k in unknown_scen)
    if scen_unknown_idx != WIN_S5:
        fail(f"scenario unknown children != the pinned WIN s5 set: {scen_unknown_idx}")
    adopted_keys = batch_keys - unknown_scen
    if len(adopted_keys) != ADOPTED_ROWS or {mask_to_index[k] for k in adopted_keys} != {mask_to_index[k] for k in incr}:
        fail("adopted key set != increment key set (child-boundary mismatch)")
    adopted_idx = sorted(mask_to_index[k] for k in adopted_keys)
    if any(k in scen for k in unknown_scen):
        fail("a WIN child appeared in the scenario cache (verdict consumed)")

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
    if newly != adopted_idx:
        fail(f"newly resolved update8 set != the adopted s5 set: {newly}")
    if lost:
        fail(f"update8 resolution LOST rows: {sorted(lost)}")
    if len(newly) != 43 or not set(newly) <= required:
        fail("newly resolved set not fully within the update8 baseline requirement")
    if rb["remaining_now"] - rs["remaining_now"] != 43:
        fail("update8 remaining delta != 43")

    # --- class status / universe metrics --------------------------------------
    cb, cs = base_summary["class_status_counts"], scen_summary["class_status_counts"]
    if cb != STATUS_TRANSITIONS or cs != STATUS_TRANSITIONS:
        fail(f"class status counts drift vs the static pin: {cb} {cs}")
    if scen_summary["board_verification"] != {"free_candidates": 38, "board_verified_free": 38, "rejected": {}}:
        fail("scenario board verification shape drift")
    if scen_summary["inputs"]["cache_rows"] != 6448 or scen_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_AFTER \
            or scen_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_AFTER:
        fail("scenario inputs metrics drift")
    if base_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["cache_rows"] != 6405:
        fail("base inputs metrics drift")
    bcv = base_summary["inputs"]["cache_verdicts"]
    scv = scen_summary["inputs"]["cache_verdicts"]
    if bcv != {"1": 158, "2": 6247} or scv != {"1": 158, "2": 6290}:
        fail("cache verdict counts drift")
    if rs["remaining_now"] != 31674 or rb["remaining_now"] != 31717:
        fail("update8 remaining recheck")

    # per-root coverage: identical free/uncovered thirds everywhere
    prc_pairs = list(zip(
        csv.DictReader(BASE_OUT.joinpath("per-root-coverage.csv").open()),
        csv.DictReader((EXP / "reaudit/output/per-root-coverage.csv").open())))
    for b, s in prc_pairs:
        if b["first"] != s["first"] or b["free_now"] != s["free_now"] or b["uncovered"] != s["uncovered"]:
            fail(f"per-root coverage changed at root {b['first']}: {b} -> {s}")
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
    if len(cb_t) != CLOSURE_ROWS or len(cs_t) != CLOSURE_ROWS:
        fail(f"closure table row counts {len(cb_t)}/{len(cs_t)} != {CLOSURE_ROWS}+entry lanes")
    left = sorted(set(cb_t) - set(cs_t))
    entered = sorted(set(cs_t) - set(cb_t))
    if left or entered:
        fail(f"closure table left/entered non-empty: {left} {entered}")
    changed, rank_churn, stable, gs_churn = [], 0, 0, []
    for ci, brow in sorted(cb_t.items()):
        srow = cs_t[ci]
        diff = {k: (brow[k], srow[k]) for k in brow if brow[k] != srow[k]}
        if not diff:
            stable += 1
            continue
        if set(diff) == {"class_rank"}:
            rank_churn += 1
            continue
        if "unknown_now" not in diff:
            # pure bookkeeping churn: rank plus a groups-served decrease (a
            # served group re-ranked to another class after the adoption;
            # decreases only, never increases, byte-reproduced by the double
            # refresh re-execution above)
            if set(diff) == {"class_rank", "groups_served_count"} and \
                    int(diff["groups_served_count"][1]) < int(diff["groups_served_count"][0]):
                gs_churn.append({"class_index": ci,
                                 "groups_served_count": [int(diff["groups_served_count"][0]),
                                                         int(diff["groups_served_count"][1])]})
                continue
            fail(f"class {ci} changed unexpected columns: {diff}")
        b_unk, s_unk = int(diff["unknown_now"][0]), int(diff["unknown_now"][1])
        clo, chi = s4_masks[ci]
        kids = board.children(clo | (chi << 64))
        kids_keys = {(c & ((1 << 64) - 1), c >> 64) for c in kids}
        own = len(kids_keys & set(adopted_keys))
        if (b_unk - s_unk) != own or own == 0:
            fail(f"class {ci} unknown delta {b_unk}->{s_unk} != own adopted membership {own}")
        if ci == CLASS_IDX and (b_unk, s_unk) != (54, 11):
            fail("class 34269 unknown transition != the pinned 54 -> 11")
        changed.append({"class_index": ci, "unknown_before": b_unk, "unknown_after": s_unk,
                        "own_adopted": own})
    if len(changed) < 1 or not any(c["class_index"] == CLASS_IDX and c["own_adopted"] == 43 for c in changed):
        fail("class 34269 not present in the changed-class set with own 43")
    # every changed class must be a Board-verified holder of at least one adopted key (checked above);
    # no class may become free or excluded: status counts are pinned static already
    scen_34269 = cs_t[CLASS_IDX]
    if int(scen_34269["unknown_now"]) != 11:
        fail("closure table 34269 unknown_now != 11")

    # --- metric deltas -------------------------------------------------------------
    jb, js = base_summary["joint_greedy"], scen_summary["joint_greedy"]
    if jb["greedy_union_size"] != JOINT_GREEDY_BEFORE or js["greedy_union_size"] != JOINT_GREEDY_AFTER:
        fail("joint greedy union size drift vs pins")
    if base_summary["worklist_total"] != WORKLIST_BEFORE or scen_summary["worklist_total"] != WORKLIST_AFTER:
        fail("worklist totals drift vs pins")
    if jb["unique_groups"] != 2119 or js["unique_groups"] != 2119:
        fail("greedy group universe changed")
    if rb["groups_free_now"] != rs["groups_free_now"]:
        fail("groups_free_now changed")
    if rs.get("win_hit_groups", rb.get("win_hit_groups")) not in ([], None):
        fail("win_hit_groups non-empty (a WIN was consumed)")

    # --- emit decomp -----------------------------------------------------------------
    out = {
        "schema": "b30loss43-adoption-decomp-deltas-v1",
        "scenario": "ADOPTED-CANONICAL",
        "batch": {"batch": 30, "class_index": CLASS_IDX, "probed_rows": 54,
                  "adopted_loss_rows": ADOPTED_ROWS, "unadopted_win_rows": len(WIN_S5),
                  "adopted_total_nodes_per_pass": ADOPTED_TOTAL_NODES,
                  "decisive_labels": "38 LOSS @15M (kit) + 4 LOSS @20M (DJ reprobe: ac032/ac036/ac044/ac047) "
                                     "+ 1 LOSS @25M (DK reprobe: ac013, superseding its 15M/20M exhaustions) "
                                     "+ 11 probe-level WINs (10 @15M, ac006 @20M DJ) left UNCONSUMED",
                  "adopted_loss_ids": adopted_ids, "unadopted_win_ids": win_ids},
        "cache": {"base_sha256": BASE_CACHE_SHA, "scenario_sha256": SCEN_CACHE_SHA,
                  "base_rows": len(base), "scenario_rows": len(scen), "increment_rows": len(incr),
                  "verdict_counts": {"WIN": 158, "LOSS": 6290},
                  "relation": "scenario == base rows + the 43 increment rows verbatim (no other row changed)",
                  "merge_audit_runs": 3, "merge_audit_sha256_each": MERGE_AUDIT_SHA},
        "class_34269": {"children_total": len(child_keys),
                        "unknown_before": 54, "unknown_after": 11,
                        "adopted_own": 43,
                        "unknown_after_s5": WIN_S5,
                        "status_after": "unknown",
                        "not_freed_because": "eleven probe-level WIN children remain verdict-unconsumed "
                                             "(scrutiny owner C++ second-implementation gate pin 9193f5b6...)",
                        "groups_served": [[int(scen_34269["first_group_first"]), int(scen_34269["first_group_third"])]]},
        "closure_table": {"rows": CLOSURE_ROWS, "left": [], "entered": [],
                          "unknown_changed_classes": changed,
                          "rank_churn_only_rows": rank_churn,
                          "groups_served_decrease_churn": gs_churn,
                          "fully_stable_rows": stable},
        "update8": {"resolved_before": UPD8_RESOLVED_BEFORE, "resolved_after": UPD8_RESOLVED_AFTER,
                    "newly_resolved_s5": adopted_idx,
                    "newly_resolved_equals_adopted": True,
                    "remaining_before": UPD8_REMAINING_BEFORE, "remaining_after": UPD8_REMAINING_AFTER,
                    "groups_free_now_static": 131},
        "class_status_counts": STATUS_TRANSITIONS,
        "metrics": {"joint_greedy_union_size": [JOINT_GREEDY_BEFORE, JOINT_GREEDY_AFTER],
                    "worklist_total": [WORKLIST_BEFORE, WORKLIST_AFTER],
                    "known_universe_indices": [KNOWN_UNIVERSE_BEFORE, KNOWN_UNIVERSE_AFTER],
                    "cache_rows_in_universe": [CACHE_IN_UNIVERSE_BEFORE, CACHE_IN_UNIVERSE_AFTER],
                    "per_root_remaining_delta": PER_ROOT_REMAINING_DELTA,
                    "note": "greedy/worklist deltas are frozen-scheduler bookkeeping after the 43 frontier "
                            "slots resolve (class 34269's members leave the nonfree best-option set); "
                            "per-root free/uncovered thirds are byte-identical everywhere; root 27 stays 119/119"},
        "verification": {"kit_files_verified": {"kit1": k1, "kit2": k2, "kit3": k3},
                         "refresh_scripts_reexecuted": [BASE_REFRESH_SHA, SCEN_REFRESH_SHA],
                         "refresh_outputs_byte_identical": True,
                         "board_child_regeneration": "class-34269 canonical 5-stone child boundary regenerated via Board(11).children"},
        "interpretation_guard":
            "only the 43 fresh LOSS rows are consumed into the canonical cache by this Part; "
            "the eleven probe-level WINs are consumed NOWHERE (no verdict claim, no exclusion "
            "claim); all 54 batch-30 keys stay UNKNOWN as verdicts; class 34269 is NOT freed "
            "(11 unconsumed WIN children remain); no update8 resolution was lost; no per-root "
            "coverage regressed (all free/uncovered thirds identical); 11x11 stays UNKNOWN; "
            "nodes are bookkeeping, never verdicts",
    }
    (EXP / "output/decomp-deltas-b30loss43-adoption.json").write_text(
        json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("DECOMP OK changed=%d rank_churn=%d gs_churn=%d stable=%d" % (len(changed), rank_churn, len(gs_churn), stable))
    print("class34269: unknown 54 -> 11, own adopted 43, WIN s5 pinned")


if __name__ == "__main__":
    main()
