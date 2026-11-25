"""Part EE adoption delta extraction: BASE (Part EC, b33exh5loss2 merged 6,665 rows)
vs SCENARIO (af034loss1 = Part ED af034 single 60M LOSS).

Fail-closed machine recomputation of exactly what the Part EE 1-LOSS canonical
adoption changed, from published bytes only:

* every published artifact sha-pinned (the published Part EC outputs -- the
  BASE canonical cache cecc1a0f... 6,665 rows WIN 158 / LOSS 6,507, the BASE
  reaudit outputs refresh-summary 936373e6... / closure-classes 0ae9749c... /
  per-root-coverage 06cd6561... / probe-worklist regen pin 36bc6c6c... -- the
  Part EE outputs -- increment cc9c4746..., increments manifest 0ad3469e...,
  the 6,666-row scenario cache fc3e4ac9... WIN 158 / LOSS 6,508 (shortened
  chain name merged-exact-s5-chain-plus-af034loss1-20261125.cache: the
  additive BASE-name-plus convention exceeds the 255-byte filename component
  limit, honestly documented in the declaration; the sha pin carries the
  identity), the merge-audits x3 (identical sha 05381cea...), the byte-clone
  of the union merger 90711961..., the frozen graph/update8/board/policy/
  quarantine pins);
* the published Part EC refresh fork (reaudit/scripts/refresh_adoption_ec.py,
  sha 73186e63...) and the published Part EE refresh fork (reaudit/scripts/
  refresh_adoption_ee.py, sha 01937f23...) are RE-EXECUTED byte-verbatim in
  isolated scratch trees against their pinned inputs, and all eight outputs
  must be byte-identical to the published / regenerated pins before any delta
  is emitted (double-run determinism; this simultaneously re-proves the
  published Part EC reaudit outputs are regenerable from published bytes);
* SCEN cache == BASE cache rows + exactly the 1 increment row (verdict
  agreement everywhere; 6,666 rows, WIN 158 / LOSS 6,508); the adopted row is
  the Part ED af034 re-probe at the pre-declared 60M condition: published
  EXHAUSTED honest-UNKNOWN at BOTH the 15M (Part EA published raws) and 30M
  (Part ED kit sources) conditions, resolved exact LOSS only at 60M (fresh-cold
  two-pass node-exact, nodes 32,012,059, legal 95); the re-probed packet is
  LOSS-ONLY (full_packet_eq_loss_only=true); the 3 drive anchors are consumed
  NOWHERE (af001/af039 re-check BASE rows verbatim, af029 stays an unconsumed
  probe-level WIN - scrutiny-owner C++ gate);
* kit integrity: the published Part ED af034-reprobe60m kit (36 files,
  MANIFEST rev2 1dfe02ca...) verified file-by-file, including the pinned
  solver image jsreplay.js (84585617...), the 60M runner (b0c5f714...),
  audit_ed.py (6f76e8e5...), the 5-line honest-history status.log
  (26a97e02...: af001 anchor PASS 60000000,2,2952432 / af029 WIN-HALT /
  af034 PASS 60000000,2,32012059, zero retry, zero exhausted),
  af034.drive.out (d2d52ed6...), audit_ed.json (5473eafb...; 58/58 gates,
  verdict_consumed=false, main probe af034 LOSS 32,012,059, drive anchors
  af001/af029/af039 pinned), the canonical EC cache byte-clone and the
  batch-33/Part EA status byte-clones in sources/, the 8 byte-pinned 60M raw
  replay files with two-pass node-exact agreement, and BOTH published
  source-exhaustion raws of the adopted key (15M: Part EA kit sources/exh15m
  pins; 30M: Part ED kit sources/exh30m pins); the published Part EA kit
  (61 files, MANIFEST 42ba81bc...) verified file-by-file as the 15M raw owner;
* the class-34908 arithmetic is recomputed from the frozen dependency graph
  with the integer-geometry Board: the 56-child canonical boundary is
  regenerated (entirely inside the s5 mask universe; ZERO non-s5 children);
  49 children are known exact LOSS in BASE (47 chain rows + the 2 Part EC
  adopted rows af003/af039, both re-checked verbatim); exactly 7 children are
  unknown in BASE and exactly 6 in SCEN == the 6 unconsumed probe-level WIN
  keys {af029, af047, af050, af053, af023, af048}; class 34908 is NOT freed
  and NOT excluded (unknown 7 -> 6, rank 8 -> 7, groups_served 5 static);
* class 16371 is proven BYTE-STATIC across this Part and class 20421 shows
  ONLY the pinned rank churn 7 -> 8 (no EE adopted key sits inside either
  boundary; 16371's closure row is byte-identical before/after, 20421's row
  differs in the class_rank column ONLY);
* every closure-classes.csv row is compared: ZERO unknown_now changes beside
  class 34908; ZERO left/entered rows; exactly ONE rank-churn-only row
  (20421) and ZERO groups_served churn (805 fully stable rows);
* update8 refresh: the adopted s5 index (930660) sits OUTSIDE the frozen
  update8 baseline requirement: resolved stays 259, remaining stays 31,600,
  groups_free_now stays 131, the newly-resolved/lost sets are both EMPTY,
  win_hit_groups stays [] and every per-root remaining is byte-identical;
* class_status counts: excluded 390 / excluded_now 23 / free_now 39 /
  unknown 34,497 IDENTICAL before and after (the loss-only adoption frees
  nothing and excludes nothing); Board verification 39/39 with zero
  rejections on both sides; root 27 stays 119/119;
* per-root coverage: free/uncovered thirds are IDENTICAL at every root; the
  individual greedy union changes only at roots 0 and 12 (pure re-selection
  bookkeeping, no coverage claim);
* the frozen greedy scheduler deltas are recorded as bookkeeping (joint
  greedy 36,509 -> 36,508, worklist 64,415 -> 64,414, known universe
  844 -> 845, cache in universe 821 -> 822).

No unknown verdict is asserted anywhere.  The standard 11x11 empty board
and every one of the 19 central-reply roots stay UNKNOWN; free_now /
coverage quantities are scheduling bookkeeping derived from exact LOSS
verdicts, not root verdict claims.  The af029 probe-level WIN row is
consumed NOWHERE by this Part (scrutiny-owner C++ second-implementation
gate pin 9193f5b6...); no WIN verdict and no EXHAUSTED verdict enters the
canonical cache; 11x11 stays UNKNOWN.
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

BASE_EXP = ROOT / "research/experiments/n11-centralreply-b33exh5loss2-adoption-reaudit-20261125"
BASE_OUT = BASE_EXP / "reaudit/output"
BASE_CACHE = BASE_EXP / "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-plus-b35loss26-plus-b4loss1-plus-b36loss40-plus-b37loss46-plus-b3loss3-plus-b33exh5loss2-20261125.cache"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-af034loss1-20261125.cache"
INCR = EXP / "output/increment-af034loss1-20261125.cache"
MANIFEST = EXP / "output/increments-manifest.json"
ED_KIT = ROOT / "research/experiments/n11-centralreply-closure-class34908-af034-reprobe60m-20261125"
EA_KIT = ROOT / "research/experiments/n11-centralreply-closure-class34908-b33exh5-reprobe30m-20261125"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_REFRESH_SCRIPT = BASE_EXP / "reaudit/scripts/refresh_adoption_ec.py"
SCEN_REFRESH_SCRIPT = EXP / "reaudit/scripts/refresh_adoption_ee.py"
MERGER = EXP / "scripts/s5_union_merge.py"

BASE_CACHE_SHA = "cecc1a0fae126d98d8e5f23e041657b86e4d7128f80cc1182f4f9830ed1e8626"
SCEN_CACHE_SHA = "fc3e4ac9052447158202f09d5efe05468dba32fe95ec90beaaa0a0de9d2c020f"
INCR_SHA = "cc9c474627ec8f6fc98c0ebeb7600707021e8cd598b3be6799d39c104289e162"
MANIFEST_SHA = "0ad3469ede4bfbddaee21d12dbab97f7e0babdbe5cbaba8cc7a6f2f41d0d22c9"
BASE_SUMMARY_SHA = "936373e6f16cad2b5e0b08fe9177fc577a3f3a072397208aafd72f9ff0944651"
BASE_CLOSURE_SHA = "0ae9749c2ef1319938bc1219136b287d98e1c56051f8e34dde076e8611340d35"
BASE_PRC_SHA = "06cd656193b317c25cb1ec6dab4ea771ace93a43c74ce974c0e8897576acb389"
BASE_WORKLIST_SHA = "36bc6c6c047dff1fa2e21d4d4ceb05eb0248213b039257ea20da6fd0d8cef9cd"
SCEN_SUMMARY_SHA = "6af660a1e0ad8f0ad3b0ac6b32c1a24099aa8f1c3a2271496a9bfb99dc80b6bc"
SCEN_CLOSURE_SHA = "27e00b0dbf2f33603dfbed91b00153f73c7a2d05b1258133a39c9ec5bfd41364"
SCEN_PRC_SHA = "6974299b57a39f7fa6aa72d76bef83a647c637dce4b2fdf23d0db4380c04a5fb"
SCEN_WORKLIST_SHA = "b4933810ccd6229e43b89f6c08f3984288026925c2b44c6398a4afd0a83a183b"
BASE_REFRESH_SHA = "73186e63037cfc8ee7a1266cc0686e827abad1cd2b5ee7d8270a60ae52dbece7"
SCEN_REFRESH_SHA = "01937f237b922542cd0a33c6750c84f83e0be1589ed528c217e2b0e4ac2630f5"
MERGE_AUDIT_SHA = "05381cea4c65fcbcaf46d77fbdf3b1d307c41f6abeef0cc9636954e29f5cbcfd"
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
ADOPTED_TABLE_DIGEST = "aab6262a8cba4ecba4d82ccb197bb08c8a50dddb72931044a17b65f2f0ecf8dc"

ED_MANIFEST_SHA = "1dfe02cae61e9f410e24bbafe7386a0958da4deddd92456faad12b8f755546ac"
ED_KIT_FILES = 36
EA_MANIFEST_SHA = "42ba81bc79dd887074dbc9514b87f0c9d1a656d53a98ff3dfef29b9c4666601e"
EA_KIT_FILES = 61
ED_STATUS_SHA = "26a97e0297c9db720c8c051db1498508bd24c038b1b3c37e69ac28fe65be226c"
ED_DRIVE_SHA = "d2d52ed68ad026f9b9b3e6ffa42210e297c22700af41de10bba38e1c6a4f2584"
ED_AUDIT_SHA = "5473eafb277867344dbba851110c4d671b1fc04f906f3c12b9dc75cf7b15a533"
AUDIT_ED_SCRIPT_SHA = "6f76e8e51ca1ce4dfb6ac678802ec6d85d4530df9013f11df0b0769ac0c7e168"
JSREPLAY_SHA = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
RUNBATCH60M_SHA = "b0c5f714f926a923d35692672fbfc6aaf2da0081cdf4217c074e0f64d3a29f92"
EA_STATUS_SHA = "db7c7017d7bfeef2d0c17c646b22f77b8bfd52a66796433b86e88444741c0438"
B33_STATUS_SHA = "1f663fc802c03b27c2e39d6130cf6c1392d62dd99b5847d6af477cd823a94b52"
EXH15M_SHAS = {
    "af034.p1.out": "6041fdeed69907458ca68cb7b335793d3c172a017368da868345f98ac8b45af0",
    "af034.p2.out": "710a214bb5737b5011e8e7fe3377f6f85adc6fe3430c53c064b44eccc550d102",
}
EXH30M_SHAS = {
    "af034.p1.out": "9ecfdc770c0b8a6eab027c097051ae2731ee15f1ede0babbc619e38acf2fca74",
    "af034.p2.out": "3978990d5821850476e7b38d1de98fbe7a56738cfd48a8b03cf8ed3350d1b290",
}
ED_RAW_SHAS = {
    "af001.p1.out": "9124225f73963f40ace05e20b47ec1c5e6156fc82a7f677a2f4afded9f0c52e0",
    "af001.p2.out": "9124225f73963f40ace05e20b47ec1c5e6156fc82a7f677a2f4afded9f0c52e0",
    "af029.p1.out": "971a9b29888f0a86e48c4fde21f9a06255116d8917e5cb5e40bebbfcdee5472d",
    "af029.p2.out": "21c7b21853b67c99e5369434f4baf40831f32b590083cf09d70897a16739d457",
    "af034.p1.out": "63860f94341477e77429624891c7e9d39a5c122487aa85c1b6dbb59fa547a7ab",
    "af034.p2.out": "eb64725fa72a2ca66af1da74fcbf6a531fd279b90f151e76be08a94b7a6a9fdd",
    "af039.p1.out": "da227971f7fee97128920784cb12f24b343557b9cec762e68a602d187e9fff43",
    "af039.p2.out": "15abe72fafa95af72e56bfcbe090b423398cdcee87f829a10c5d82b6b16b94b9",
}
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
BOARD_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
ED_TARGET_INPUT_SHA = "a4bff56606cbb11107b77dac677b1e1151f59686174bddcf7e08c0558f590326"
ED_ANCHOR_INPUT_SHAS = {
    "af001": "b2ef3588267694aff51b5ec7aa9940064c5199db2b5f00644a9ed27fca2a127b",
    "af029": "b5500b8d98cd3cbef56f6177245d8e3c21c31081f2252c6454f1aee73ce30c10",
    "af039": "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691",
}

CLASS_34908 = 34908
CLASS_16371 = 16371
CLASS_20421 = 20421
ADOPTED_ROWS = 1
ADOPTED_TOTAL_NODES = 32012059
WHOLE_PACKET_NODES = ADOPTED_TOTAL_NODES  # loss-only: the probed packet IS the single adopted row

ADOPTED_IDS = ["af034"]
PACKET_IDS = ["af034"]
ANCHOR_IDS = ["af001", "af029", "af039"]

ADOPTED_S5 = [930660]
NEWLY_RESOLVED_UPD8_S5 = []

# class 34908 (the single EE target)
BOUNDARY_34908_RAW = 56
BOUNDARY_34908_S5 = 56
BASE_KNOWN_LOSS_34908 = 49
UNKNOWN_BASE_34908 = 7
UNKNOWN_SCEN_34908 = 6
WIN_S5_PINNED_34908 = {"af029": 900646, "af047": 961976, "af050": 962386,
                       "af053": 962470, "af023": 810351, "af048": 962172}
UNCONSUMED_WIN_IDS_34908 = ["af023", "af029", "af047", "af048", "af050", "af053"]
KEY_PINS = {
    "af001": (1152921504742113281, 68719476736),
    "af003": (3458764513821589505, 68719476736),
    "af023": (1152921504607895553, 68719478784),
    "af029": (1152921504607895553, 68720525312),
    "af034": (1152921504607911937, 68719476736),
    "af039": (1152921504607895681, 68719476736),
    "af047": (1152921504607895809, 68719476736),
    "af048": (1152921508902862849, 68719476736),
    "af050": (1152921504607899649, 68719476736),
    "af053": (1152921504606852096, 17660905521152),
}
LABEL_PINS_60M = {
    "af001": (2, 2952432),       # 60M drive anchor, node-exact vs published 15M/30M
    "af029": (1, 4862485),       # 60M drive anchor, node-exact; unconsumed WIN
    "af034": (2, 32012059),      # ADOPTED (the single EE increment row)
    "af039": (2, 19234232),      # 60M drive anchor, node-exact vs the 30M value
}
BASE_VERBATIM_34908 = {
    "af001": (2, 2952432),        # published batch-33 LOSS anchor row
    "af003": (2, 23126072),       # Part EC adopted row (s5 153030)
    "af039": (2, 19234232),       # Part EC adopted row (s5 950512)
}
ED_STATUS_LINES = 5
ED_STATUS_FIRST = "2026-11-25T05:07:10Z af001 PASS 60000000,2,2952432"
ED_STATUS_FINAL = "2026-11-25T05:18:47Z af034 PASS 60000000,2,32012059"
ED_STATUS_WIN_HALT_LINES = [
    "2026-11-25T05:07:58Z af029 WIN-HALT",
]
ED_STATUS_RETRY_LINES = []
ED_STATUS_EXHAUSTED_LINES = []

STATUS_EXPECTED = {"excluded": 390, "excluded_now": 23, "free_now": 39, "unknown": 34497}
UPD8_RESOLVED_BEFORE = 259
UPD8_RESOLVED_AFTER = 259
UPD8_REMAINING_BEFORE = 31600
UPD8_REMAINING_AFTER = 31600
JOINT_GREEDY_BEFORE = 36509
JOINT_GREEDY_AFTER = 36508
WORKLIST_BEFORE = 64415
WORKLIST_AFTER = 64414
KNOWN_UNIVERSE_BEFORE = 844
KNOWN_UNIVERSE_AFTER = 845
CACHE_IN_UNIVERSE_BEFORE = 821
CACHE_IN_UNIVERSE_AFTER = 822
CACHE_VERDICTS_BEFORE = {"1": 158, "2": 6507}
CACHE_VERDICTS_AFTER = {"1": 158, "2": 6508}
UNIQUE_GROUPS_BEFORE = 2115
UNIQUE_GROUPS_AFTER = 2115
GROUP_BEST_NONFREE = 2115
PER_ROOT_REMAINING_DELTA = {}
PER_ROOT_COVERAGE_DELTA = {
    "0": {"free": [7, 7], "uncovered": [112, 112], "greedy": [3004, 3003]},
    "12": {"free": [6, 6], "uncovered": [113, 113], "greedy": [2891, 2890]},
}
CLOSURE_ROWS_BEFORE = 807
CLOSURE_ROWS_AFTER = 807
CLOSURE_LEFT = []
CLOSURE_ENTERED = []
CLASS_34908_ROW_BEFORE = {"class_rank": "8", "unknown_now": "7", "groups_served_count": "5"}
CLASS_34908_ROW_AFTER = {"class_rank": "7", "unknown_now": "6", "groups_served_count": "5"}
CLASS_16371_ROW = {"class_rank": "4", "unknown_now": "2", "groups_served_count": "3"}
CLASS_20421_ROW_BEFORE = {"class_rank": "7", "unknown_now": "6", "groups_served_count": "4"}
CLASS_20421_ROW_AFTER = {"class_rank": "8", "unknown_now": "6", "groups_served_count": "4"}
RANK_CHURN_DETAIL = [(20421, 7, 8)]
GS_CHURN_DECREASE = []
RANK_CHURN_ROWS = 1
FULLY_STABLE_ROWS = 805
CHANGED_CLASS_SET = []


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


def verify_kit(dirp: Path, manifest_sha: str, files_expected: int):
    if sha(dirp / "MANIFEST-sha256.txt") != manifest_sha:
        fail(f"kit {dirp.name} MANIFEST sha drift")
    n = 0
    for line in (dirp / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split()
        if len(fields) >= 4:   # 4-column format: sha blobsha size relpath
            want, rel = fields[0], fields[3]
        elif len(fields) == 3:  # Part EA format: sha blobsha relpath
            want, rel = fields[0], fields[2]
        else:                   # Part ED rev2 format: sha relpath
            want, rel = fields[0], fields[1]
        p = dirp / rel
        if not p.is_file():
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


def two_pass_raw(p1: Path, p2: Path, shas: dict):
    """Parse a published two-pass raw replay pair and demand node-exact agreement."""
    rows = {}
    for p in (p1, p2):
        if sha(p) != shas[p.name]:
            fail(f"raw replay sha drift vs the pinned published bytes: {p.name}")
        row = None
        seen = 0
        for line in p.read_text().splitlines():
            if line.startswith("replay,"):
                parts = line.split(",")
                seen += 1
                row = {"stones": int(parts[2]), "legal": int(parts[3]),
                       "is_or": int(parts[4]), "budget": int(parts[5]),
                       "result": int(parts[6]), "nodes": int(parts[7])}
        if seen != 1 or row is None:
            fail(f"expected exactly one replay row in {p}")
        rows[p.name] = row
    ref = rows[p1.name]
    for name, r in rows.items():
        if r != ref:
            fail(f"two-pass raw disagreement (fresh-cold node-exact gate): {name}")
    return ref


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
        ("union merger byte-clone", MERGER, MERGER_SHA),
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
    ed_files = verify_kit(ED_KIT, ED_MANIFEST_SHA, ED_KIT_FILES)
    ea_files = verify_kit(EA_KIT, EA_MANIFEST_SHA, EA_KIT_FILES)
    if sha(ED_KIT / "scripts/jsreplay.js") != JSREPLAY_SHA:
        fail("jsreplay.js sha drift in the Part ED kit (pinned solver image 8458...)")
    if sha(ED_KIT / "scripts/runbatch_af034-60m.sh") != RUNBATCH60M_SHA:
        fail("60M runner sha drift in the Part ED kit (pinned b0c5...)")
    if sha(ED_KIT / "scripts/audit_ed.py") != AUDIT_ED_SCRIPT_SHA:
        fail("audit_ed.py sha drift in the Part ED kit (pinned 6f76...)")
    if sha(ED_KIT / "output/status.log") != ED_STATUS_SHA:
        fail("Part ED status.log sha drift")
    if sha(ED_KIT / "output/af034.drive.out") != ED_DRIVE_SHA:
        fail("Part ED af034.drive.out sha drift")
    if sha(ED_KIT / "output/audit_ed.json") != ED_AUDIT_SHA:
        fail("Part ED audit_ed.json sha drift")
    if sha(ED_KIT / "sources/canonical-cache-ec-merged-cecc1a0f-20261125.cache") != BASE_CACHE_SHA:
        fail("Part ED sources canonical-cache byte-clone sha drift vs the BASE pin")
    if sha(ED_KIT / "sources/n11-s5-evidence-quarantine.json") != QUARANTINE_SHA:
        fail("Part ED sources quarantine byte-clone sha drift")
    if sha(ED_KIT / "sources/b33-status.log") != B33_STATUS_SHA:
        fail("published batch-33 honest-history status sha drift (source 1f66...)")
    if sha(ED_KIT / "sources/ea-status.log") != EA_STATUS_SHA:
        fail("published Part EA honest-history status sha drift (source db7c...)")
    status_lines = (ED_KIT / "output/status.log").read_text().splitlines()
    if len(status_lines) != ED_STATUS_LINES \
            or status_lines[0] != ED_STATUS_FIRST or status_lines[-1] != ED_STATUS_FINAL \
            or [l for l in status_lines if "WIN-HALT" in l] != ED_STATUS_WIN_HALT_LINES \
            or [l for l in status_lines if "RETRY" in l] != ED_STATUS_RETRY_LINES \
            or [l for l in status_lines if "EXHAUSTED" in l] != ED_STATUS_EXHAUSTED_LINES:
        fail("Part ED status.log honest-history shape drift")
    for kid in ANCHOR_IDS + ADOPTED_IDS:
        two_pass_raw(ED_KIT / f"output/raw/{kid}.p1.out",
                     ED_KIT / f"output/raw/{kid}.p2.out", ED_RAW_SHAS)
    main_raw = two_pass_raw(ED_KIT / "output/raw/af034.p1.out",
                            ED_KIT / "output/raw/af034.p2.out", ED_RAW_SHAS)
    if (main_raw["result"], main_raw["nodes"], main_raw["budget"], main_raw["legal"]) \
            != (2, ADOPTED_TOTAL_NODES, 60000000, 95):
        fail("the adopted af034 60M raw pair must be exact LOSS 32,012,059 (budget 60,000,000, legal 95)")
    for kid in ANCHOR_IDS:
        r = two_pass_raw(ED_KIT / f"output/raw/{kid}.p1.out",
                         ED_KIT / f"output/raw/{kid}.p2.out", ED_RAW_SHAS)
        if (r["result"], r["nodes"], r["budget"]) != (LABEL_PINS_60M[kid] + (60000000,)):
            fail(f"60M drive anchor {kid} raw label drift")
    exh15 = two_pass_raw(EA_KIT / "sources/exh15m/af034.p1.out",
                         EA_KIT / "sources/exh15m/af034.p2.out", EXH15M_SHAS)
    if (exh15["result"], exh15["nodes"], exh15["budget"]) != (0, 15000000, 15000000):
        fail("the published 15M source exhaustion of af034 must be EXHAUSTED 15,000,000 (honest-UNKNOWN history)")
    exh30 = two_pass_raw(ED_KIT / "sources/exh30m/af034.p1.out",
                         ED_KIT / "sources/exh30m/af034.p2.out", EXH30M_SHAS)
    if (exh30["result"], exh30["nodes"], exh30["budget"]) != (0, 30000000, 30000000):
        fail("the published 30M source exhaustion of af034 must be EXHAUSTED 30,000,000 (honest-UNKNOWN history)")

    # --- audit_ed.json honesty pins ---------------------------------------
    audit = json.loads((ED_KIT / "output/audit_ed.json").read_text())
    if audit["schema"] != "n11-ed-af034-reprobe60m-audit-v1":
        fail("audit_ed.json schema drift")
    if audit["gates_total"] != 58 or not audit["all_gates_pass"] or audit["gates_failed"] != []:
        fail("audit_ed.json all-pass gate drift")
    if audit["verdict_consumed"]:
        fail("audit_ed.json verdict_consumed must be false")
    mp = audit["main_probe_af034"]
    if (mp["label"], mp["result"], mp["nodes"]) != ("LOSS", 2, ADOPTED_TOTAL_NODES):
        fail("audit_ed.json main_probe label/nodes drift")
    if audit["claims"]["target"] != "af034 (1152921504607911937, 68719476736)" \
            or audit["claims"]["label"] != "LOSS":
        fail("audit_ed.json claims target/label drift")
    for kid in ANCHOR_IDS:
        a = audit["anchors"][kid]
        if (a["result"], a["nodes"]) != LABEL_PINS_60M[kid] or a["budget"] != 60000000:
            fail(f"audit_ed.json drive anchor {kid} label drift")
    for name, v in audit["valgate"].items():
        if not v:
            fail(f"audit_ed.json valgate entry missing: {name}")

    # --- manifest decomposition ------------------------------------------
    manifest = json.loads(MANIFEST.read_text())
    if manifest["schema"] != "af034loss1-increments-manifest-v1":
        fail("manifest schema drift")
    if manifest["base_cache_sha256"] != BASE_CACHE_SHA:
        fail("manifest base cache pin drift")
    if manifest["sha256"]["loss_increment"] != INCR_SHA:
        fail("manifest loss_increment pin drift")
    if manifest["merger_sha256"] != MERGER_SHA:
        fail("manifest merger pin drift")
    if manifest["adopted_table_digest_sha256"] != ADOPTED_TABLE_DIGEST:
        fail("manifest adopted-table digest drift")
    if manifest["base_cache_rows"] != 6665:
        fail("manifest base rows drift")
    if manifest["base_cache_absent_hits_for_emitted"] != 0:
        fail("manifest emitted rows must be absent from BASE (fresh increment)")
    if manifest["base_cache_prior_adoption_confirmed"] != 0:
        fail("manifest prior-adoption count drift")
    if manifest["quarantine_hits"] != 0:
        fail("manifest quarantine hits must be 0")
    if manifest["row_counts"] != {"adopted_loss_rows": 1, "exhausted_excluded": 0,
                                  "prior_adopted_loss_rows_base": 2, "wins_unconsumed": 0}:
        fail("manifest row_counts drift")
    if manifest["provenance"] != {"b33_status_lines": 66, "ea_status_lines": 13,
                                 "ed_kit_files": ed_files,
                                 "ed_status_lines": ED_STATUS_LINES,
                                 "raws_published": True}:
        fail("manifest provenance drift")
    adopted_ids = manifest["loss_ids"]
    if adopted_ids != ADOPTED_IDS:
        fail(f"manifest adopted ids != the pinned adopted set: {adopted_ids}")
    if sorted(manifest["resolved_ids"]) != sorted(adopted_ids):
        fail("manifest resolved_ids != loss_ids")
    if manifest.get("full_packet_eq_loss_only") is not True:
        fail("the re-probed Part ED packet is LOSS-ONLY: manifest full_packet_eq_loss_only must be true")
    if manifest.get("win_scenario_exists") is not False:
        fail("manifest win_scenario_exists must be false (no probe-level WIN row in THIS packet)")
    if manifest["unadopted_win_ids"] != []:
        fail("manifest unconsumed WIN id set must be EMPTY for this Part")
    if manifest["unadopted_win_rows"] != []:
        fail("manifest unconsumed WIN rows must be EMPTY for this Part")
    if manifest["exhausted_excluded_ids"] != [] or manifest["exhausted_rows"] != []:
        fail("manifest exhausted-excluded rows must be EMPTY for this Part")
    if len(manifest["adopted_table"]) != ADOPTED_ROWS \
            or any(r["result"] != 2 for r in manifest["adopted_table"]):
        fail("manifest adopted_table must be 1 exact-LOSS row")
    if sum(r["nodes"] for r in manifest["adopted_table"]) != ADOPTED_TOTAL_NODES:
        fail("manifest adopted_table node sum drift")
    for b in manifest["batches"]:
        pool = b["pool"]
        if pool != "af034loss1":
            fail(f"unexpected pool {pool} in the EE manifest")
        if b["adopted_loss_ids"] != ADOPTED_IDS:
            fail(f"pool {pool} adopted id set drift")
        if b["unadopted_win_ids"] != [] or b["exhausted_excluded_ids"] != []:
            fail(f"pool {pool} unconsumed/excluded sets must be EMPTY")
        if b["probed_ids"] != PACKET_IDS:
            fail(f"pool {pool} probed != the single adopted target")
        if sorted(b["anchor_ids"]) != sorted(ANCHOR_IDS):
            fail(f"pool {pool} drive-anchor id set drift")
        if b["status_log_lines"] != ED_STATUS_LINES:
            fail(f"pool {pool} status-log honest-history line count drift")
        if b["status_log_first_line"] != ED_STATUS_FIRST \
                or b["status_log_final_line"] != ED_STATUS_FINAL:
            fail(f"pool {pool} status-log first/final line drift")
        if b["status_log_win_halt_lines"] != ED_STATUS_WIN_HALT_LINES:
            fail(f"pool {pool} status-log WIN-HALT drift")
        if b["status_log_retry_lines"] != ED_STATUS_RETRY_LINES:
            fail(f"pool {pool} status-log retry-history drift")
        if b["status_log_exhausted_lines"] != ED_STATUS_EXHAUSTED_LINES:
            fail(f"pool {pool} status-log EXHAUSTED drift")
        if b["adopted_nodes_per_pool"] != ADOPTED_TOTAL_NODES:
            fail(f"pool {pool} adopted node total drift")
        if b["whole_packet_nodes"] != ADOPTED_TOTAL_NODES:
            fail(f"pool {pool} whole-packet node total drift (the loss-only packet IS the adopted row)")
        if b["reprobe_budget"] != 60000000 or b["origin_budget_15m"] != 15000000 \
                or b["source_budget_30m"] != 30000000:
            fail(f"pool {pool} budget-condition pins drift")
        if b["status_log_sha256"] != ED_STATUS_SHA:
            fail(f"pool {pool} status-log sha pin drift")
        if b["target_input_sha256"] != ED_TARGET_INPUT_SHA:
            fail(f"pool {pool} target input pin drift")
        if b["anchor_input_sha256"] != ED_ANCHOR_INPUT_SHAS:
            fail(f"pool {pool} drive-anchor input pin table drift")
        ki = b["kit_integrity"]
        if ki["kit_manifest_sha256"] != ED_MANIFEST_SHA or ki["kit_files_verified"] != ED_KIT_FILES:
            fail(f"pool {pool} kit integrity pins drift")
        if ki["raw_file_sha256_pins"] != ED_RAW_SHAS:
            fail(f"pool {pool} raw-file pin table drift")
        if ki["b33_status_sha256"] != B33_STATUS_SHA or ki["ea_status_sha256"] != EA_STATUS_SHA:
            fail(f"pool {pool} source-status pin table drift")
        if ki["exh30m_source_sha256_pins"] != EXH30M_SHAS:
            fail(f"pool {pool} 30M source-exhaustion pin table drift")

    # --- refresh re-execution (double-run determinism) ---------------------
    base_tmp = rerun_refresh(BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA, ".eeverify-base-ec")
    scen_tmp = rerun_refresh(SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA, ".eeverify-scen")
    checks = [
        (base_tmp / "refresh-summary.json", BASE_OUT / "refresh-summary.json", BASE_SUMMARY_SHA),
        (base_tmp / "closure-classes.csv", BASE_OUT / "closure-classes.csv", BASE_CLOSURE_SHA),
        (base_tmp / "per-root-coverage.csv", BASE_OUT / "per-root-coverage.csv", BASE_PRC_SHA),
        (base_tmp / "probe-worklist.csv", None, BASE_WORKLIST_SHA),
        (scen_tmp / "refresh-summary.json", EXP / "reaudit/output/refresh-summary.json", SCEN_SUMMARY_SHA),
        (scen_tmp / "closure-classes.csv", EXP / "reaudit/output/closure-classes.csv", SCEN_CLOSURE_SHA),
        (scen_tmp / "per-root-coverage.csv", EXP / "reaudit/output/per-root-coverage.csv", SCEN_PRC_SHA),
        (scen_tmp / "probe-worklist.csv", None, SCEN_WORKLIST_SHA),
    ]
    for tmp_out, pub, want_sha in checks:
        if sha(tmp_out) != want_sha:
            fail(f"refresh re-execution output drift: {tmp_out.name} ({tmp_out.parent.parent.name})")
        if pub is not None and sha(pub) != want_sha:
            fail(f"published output drifted from pin: {pub}")
    shutil.rmtree(ROOT / "research/experiments/.eeverify-base-ec")
    shutil.rmtree(ROOT / "research/experiments/.eeverify-scen")

    # --- cache relation: SCEN == BASE + exactly the 1 increment row -------
    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    incr = load_cache(INCR)
    if len(base) != 6665 or len(scen) != 6666 or len(incr) != ADOPTED_ROWS:
        fail(f"cache sizes drift: base {len(base)} scen {len(scen)} incr {len(incr)}")
    for key, row in incr.items():
        if row[0] != 2:
            fail(f"increment contains a non-LOSS row: {key}")
        if key in base:
            fail(f"increment key already in BASE: {key}")
        if scen.get(key) != row:
            fail(f"increment row not taken verbatim into scenario cache: {key}")
        if row != (2, ADOPTED_TOTAL_NODES):
            fail(f"increment row verdict/nodes drift: {key} {row}")
    merged = dict(base)
    for key, row in incr.items():
        merged[key] = row
    if merged != scen:
        fail("scenario cache != BASE rows + increment rows (set difference)")
    wins = sum(1 for v in scen.values() if v[0] == 1)
    losses = len(scen) - wins
    if (wins, losses) != (158, 6508):
        fail(f"scenario verdict counts {wins}/{losses} != 158/6,508")
    # the adopted key must be exactly af034; the WIN keys sit in NO cache
    adopted_keys = {KEY_PINS[k] for k in ADOPTED_IDS}
    if set(incr) != adopted_keys or len(incr) != 1:
        fail("increment key set != the pinned af034 key")
    tab = {(int(e["lo"]), int(e["hi"])): (e["legal"], e["result"], e["nodes"])
           for e in manifest["adopted_table"]}
    if set(tab) != set(incr):
        fail("manifest adopted_table keys != increment keys")
    for key, row in incr.items():
        if row != (tab[key][1], tab[key][2]):
            fail(f"manifest adopted_table row != increment row: {key}")
        if tab[key][0] != 95:
            fail(f"manifest adopted_table legal-move count drift: {key}")
    for kid in UNCONSUMED_WIN_IDS_34908:
        if KEY_PINS[kid] in incr or KEY_PINS[kid] in base or KEY_PINS[kid] in scen:
            fail(f"the unconsumed WIN key {kid} must sit in NO cache (scrutiny gate owns it)")
    if KEY_PINS["af029"] in base or KEY_PINS["af029"] in scen or KEY_PINS["af029"] in incr:
        fail("the unconsumed 60M drive-anchor WIN key af029 must sit in NO cache")
    for kid, want in BASE_VERBATIM_34908.items():
        if base.get(KEY_PINS[kid]) != want or scen.get(KEY_PINS[kid]) != want:
            fail(f"the published anchor/adopted row {kid} must reproduce the BASE row verbatim in both caches")

    # --- Board arithmetic for classes 34908 / 16371 / 20421 -----------------
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
    board = Board(11)
    update8 = json.loads(UPDATE8.read_text())
    receipt_verdicts = {int(k): int(v) for k, v in update8["resolved_s5_verdicts"].items()}
    if {mask_to_index[k] for k in adopted_keys} != set(ADOPTED_S5):
        fail("adopted s5 index set != the pinned adopted list")

    # --- class 34908 (the single EE target) ----------------------------------
    lo, hi = s4_masks[CLASS_34908]
    children = board.children(lo | (hi << 64))
    child_keys_34908 = {(c & ((1 << 64) - 1), c >> 64) for c in children}
    if len(child_keys_34908) != BOUNDARY_34908_RAW:
        fail(f"class-34908 Board child boundary {len(child_keys_34908)} != {BOUNDARY_34908_RAW}")
    non_s5 = [k for k in child_keys_34908 if k not in mask_to_index]
    if non_s5:
        fail("class-34908 boundary must have ZERO non-s5 children")
    in_s5_34908 = child_keys_34908
    if len(in_s5_34908) != BOUNDARY_34908_S5:
        fail(f"class-34908 in-s5 boundary {len(in_s5_34908)} != {BOUNDARY_34908_S5}")
    if not adopted_keys <= child_keys_34908:
        fail("the adopted key must sit inside the class-34908 child boundary")
    receipt_child_34908 = {k for k in in_s5_34908 if mask_to_index[k] in receipt_verdicts}
    if receipt_child_34908:
        fail("class-34908 must have ZERO update8-receipt children")
    known_base_34908 = {k for k in in_s5_34908 if k in base}
    if len(known_base_34908) != BASE_KNOWN_LOSS_34908:
        fail(f"class-34908 BASE-known child count {len(known_base_34908)} != {BASE_KNOWN_LOSS_34908}")
    for k in known_base_34908:
        if base[k][0] != 2:
            fail("a BASE-known child of 34908 is not an exact LOSS")
    unknown_base_34908 = {k for k in in_s5_34908 if k not in base}
    if len(unknown_base_34908) != UNKNOWN_BASE_34908:
        fail(f"class-34908 BASE unknown count {len(unknown_base_34908)} != {UNKNOWN_BASE_34908}")
    want_base_unknown_s5 = sorted(list(WIN_S5_PINNED_34908.values()) + ADOPTED_S5)
    if sorted(mask_to_index[k] for k in unknown_base_34908) != want_base_unknown_s5:
        fail("BASE unknown children of 34908 != the pinned packet (6 unconsumed WIN + the af034 EXHAUSTED)")
    unknown_scen_34908 = {k for k in in_s5_34908 if k not in scen}
    if len(unknown_scen_34908) != UNKNOWN_SCEN_34908:
        fail(f"scenario unknown children of 34908 = {len(unknown_scen_34908)} != 6 (6 unconsumed WINs; class NOT freed)")
    if unknown_scen_34908 != unknown_base_34908 - adopted_keys:
        fail("scenario unknown children of 34908 != BASE unknowns minus the adopted set")
    want_scen_unknown_s5 = sorted(WIN_S5_PINNED_34908.values())
    if sorted(mask_to_index[k] for k in unknown_scen_34908) != want_scen_unknown_s5:
        fail("scenario unknown children of 34908 != the pinned unconsumed WIN s5 set")
    own_34908 = in_s5_34908 & adopted_keys
    if own_34908 != adopted_keys:
        fail("class-34908 adopted-own set != exactly the 1 EE re-probe row")
    for k in own_34908:
        if scen[k][0] != 2:
            fail(f"the adopted child of 34908 is not an exact LOSS in the scenario: {k}")
    if own_34908 & unknown_scen_34908:
        fail("adopted set collides with the unconsumed WIN set inside 34908")
    if any(k in quarantined for k in child_keys_34908):
        fail("a quarantined key sits inside the class-34908 child boundary")

    # --- classes 16371 and 20421 (NOT EE-owned; boundary checks) -------------
    for cls in (CLASS_16371, CLASS_20421):
        clo, chi = s4_masks[cls]
        kids = {(c & ((1 << 64) - 1), c >> 64) for c in board.children(clo | (chi << 64))}
        if adopted_keys & kids:
            fail(f"no adopted key may sit inside the class-{cls} boundary ({cls} is not EE-owned)")
        if any(k in quarantined for k in kids):
            fail(f"a quarantined key sits inside the class-{cls} boundary")
        for k in kids:
            if k in base and k in scen and base[k] != scen[k]:
                fail(f"class-{cls} child verdict drifted across EE")

    # --- update8 refresh deltas ---------------------------------------------
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
    if newly != NEWLY_RESOLVED_UPD8_S5 or lost:
        fail(f"update8 newly-resolved/lost sets must BOTH be empty (the adopted key sits "
             f"outside the frozen baseline requirement): newly {newly} lost {sorted(lost)}")
    if set(ADOPTED_S5) & set(update8["required_new_s5"]):
        fail("the adopted s5 index must sit OUTSIDE the frozen update8 baseline requirement")
    if rb["groups_free_now"] != 131 or rs["groups_free_now"] != 131:
        fail("update8 groups_free_now drift (must stay 131 static)")
    if rs.get("win_hit_groups", rb.get("win_hit_groups")) not in ([], None):
        fail("win_hit_groups non-empty (a WIN was consumed)")

    # --- class status / universe metrics --------------------------------------
    cb, cs = base_summary["class_status_counts"], scen_summary["class_status_counts"]
    if cb != STATUS_EXPECTED or cs != STATUS_EXPECTED:
        fail(f"class status counts drift vs the pinned static transition: {cb} {cs}")
    if scen_summary["board_verification"] != {"free_candidates": 39, "board_verified_free": 39, "rejected": {}}:
        fail("scenario board verification shape drift")
    if base_summary["board_verification"] != {"free_candidates": 39, "board_verified_free": 39, "rejected": {}}:
        fail("base board verification shape drift")
    if scen_summary["inputs"]["cache_rows"] != 6666 \
            or scen_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_AFTER \
            or scen_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_AFTER:
        fail("scenario inputs metrics drift")
    if base_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["cache_rows"] != 6665:
        fail("base inputs metrics drift")
    bcv = base_summary["inputs"]["cache_verdicts"]
    scv = scen_summary["inputs"]["cache_verdicts"]
    if bcv != CACHE_VERDICTS_BEFORE or scv != CACHE_VERDICTS_AFTER:
        fail("cache verdict counts drift")

    # per-root coverage: free/uncovered thirds identical at EVERY root
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
        fail(f"per-root coverage delta {prc_delta} != the pinned re-selection churn")
    for root, d in prc_delta.items():
        if d["free"][0] != d["free"][1] or d["uncovered"][0] != d["uncovered"][1]:
            fail(f"root {root} free/uncovered thirds changed although no class was freed")
    root27 = [s for b, s in prc_pairs if s["first"] == "27"][0]
    if root27["free_now"] != "119" or root27["uncovered"] != "0":
        fail("root 27 coverage regressed")
    rb_pr = rb["per_root_remaining"]
    rs_pr = rs["per_root_remaining"]
    deltas = {k: rs_pr[k] - rb_pr[k] for k in rb_pr if rs_pr[k] != rb_pr[k]}
    if deltas != PER_ROOT_REMAINING_DELTA:
        fail(f"per-root remaining delta {deltas} != pinned {PER_ROOT_REMAINING_DELTA}")
    if any(v > 0 for v in deltas.values()):
        fail("a per-root remaining INCREASED (coverage regression)")

    # --- joint greedy / worklist bookkeeping ---------------------------------
    jb, js = base_summary["joint_greedy"], scen_summary["joint_greedy"]
    if jb["greedy_union_size"] != JOINT_GREEDY_BEFORE or js["greedy_union_size"] != JOINT_GREEDY_AFTER:
        fail("joint greedy union size drift vs pins")
    if base_summary["worklist_total"] != WORKLIST_BEFORE or scen_summary["worklist_total"] != WORKLIST_AFTER:
        fail("worklist totals drift vs pins")
    if jb["unique_groups"] != UNIQUE_GROUPS_BEFORE or js["unique_groups"] != UNIQUE_GROUPS_AFTER:
        fail("greedy group universe must stay static (no class freed)")
    if base_summary["group_best_options_nonfree"] != GROUP_BEST_NONFREE \
            or scen_summary["group_best_options_nonfree"] != GROUP_BEST_NONFREE:
        fail("nonfree best-option count drift")

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
    if left != CLOSURE_LEFT or entered != CLOSURE_ENTERED:
        fail(f"closure table left/entered must be EMPTY (static 807-row table): {left} / {entered}")
    if CLASS_34908 not in cb_t or CLASS_34908 not in cs_t:
        fail("class 34908 must remain in BOTH closure tables (not freed, not excluded)")
    for col, want in CLASS_34908_ROW_BEFORE.items():
        if cb_t[CLASS_34908][col] != want:
            fail(f"base class-34908 row {col} drift: {cb_t[CLASS_34908][col]} != {want}")
    for col, want in CLASS_34908_ROW_AFTER.items():
        if cs_t[CLASS_34908][col] != want:
            fail(f"scenario class-34908 row {col} drift: {cs_t[CLASS_34908][col]} != {want}")
    if int(cb_t[CLASS_34908]["unknown_now"]) - int(cs_t[CLASS_34908]["unknown_now"]) != len(own_34908) or len(own_34908) != 1:
        fail("class-34908 unknown delta != its own adopted children (Board boundary)")
    if int(cb_t[CLASS_34908]["class_rank"]) - int(cs_t[CLASS_34908]["class_rank"]) != 1:
        fail("class-34908 rank must drop exactly 8 -> 7 (its frontier cost shrank)")
    if CLASS_16371 not in cb_t or CLASS_16371 not in cs_t:
        fail("class 16371 must remain in BOTH closure tables (not freed, not excluded)")
    if cb_t[CLASS_16371] != cs_t[CLASS_16371]:
        fail("class-16371 full row must be byte-identical before/after (not EE-owned)")
    for col, want in CLASS_16371_ROW.items():
        if cs_t[CLASS_16371][col] != want:
            fail(f"class-16371 row {col} drift: {cs_t[CLASS_16371][col]} != {want}")
    if CLASS_20421 not in cb_t or CLASS_20421 not in cs_t:
        fail("class 20421 must remain in BOTH closure tables (not freed, not excluded)")
    for col, want in CLASS_20421_ROW_BEFORE.items():
        if cb_t[CLASS_20421][col] != want:
            fail(f"base class-20421 row {col} drift: {cb_t[CLASS_20421][col]} != {want}")
    for col, want in CLASS_20421_ROW_AFTER.items():
        if cs_t[CLASS_20421][col] != want:
            fail(f"scenario class-20421 row {col} drift: {cs_t[CLASS_20421][col]} != {want}")
    diff_20421 = {k: (cb_t[CLASS_20421][k], cs_t[CLASS_20421][k])
                  for k in cb_t[CLASS_20421] if cb_t[CLASS_20421][k] != cs_t[CLASS_20421][k]}
    if set(diff_20421) != {"class_rank"} or diff_20421["class_rank"] != ("7", "8"):
        fail(f"class-20421 must differ in the class_rank column ONLY (7 -> 8): {diff_20421}")
    changed, rank_churn, stable, gs_dec, gs_bad = [], 0, 0, [], []
    rank_churn_classes = []
    for ci, brow in sorted(cb_t.items()):
        if ci == CLASS_34908 or ci not in cs_t:
            continue
        srow = cs_t[ci]
        diff = {k: (brow[k], srow[k]) for k in brow if brow[k] != srow[k]}
        if not diff:
            stable += 1
            continue
        if set(diff) == {"class_rank"}:
            rank_churn += 1
            rank_churn_classes.append((ci, int(brow["class_rank"]), int(srow["class_rank"])))
            continue
        if set(diff) == {"class_rank", "groups_served_count"}:
            gs_dec.append({
                "class_index": ci,
                "class_rank": [int(diff["class_rank"][0]), int(diff["class_rank"][1])],
                "groups_served_count": [int(diff["groups_served_count"][0]),
                                         int(diff["groups_served_count"][1])],
                "unknown_now": [int(brow["unknown_now"]), int(srow["unknown_now"])],
            })
            continue
        if "unknown_now" not in diff:
            fail(f"class {ci} changed unexpected columns: {diff}")
        b_unk, s_unk = int(diff["unknown_now"][0]), int(diff["unknown_now"][1])
        clo, chi = s4_masks[ci]
        kids = board.children(clo | (chi << 64))
        kids_keys = {(c & ((1 << 64) - 1), c >> 64) for c in kids}
        own = len(kids_keys & adopted_keys)
        if (b_unk - s_unk) != own or own == 0:
            fail(f"class {ci} unknown delta {b_unk}->{s_unk} != own adopted membership {own}")
        changed.append({"class_index": ci, "unknown_before": b_unk, "unknown_after": s_unk,
                        "own_adopted": own})
    if changed != CHANGED_CLASS_SET:
        fail(f"changed-class set != the pinned EMPTY set: {changed}")
    if rank_churn_classes != RANK_CHURN_DETAIL:
        fail(f"rank-churn-only rows != the pinned single 20421 churn: {rank_churn_classes}")
    if rank_churn != RANK_CHURN_ROWS or stable != FULLY_STABLE_ROWS:
        fail(f"rank churn {rank_churn}/stable {stable} != pinned {RANK_CHURN_ROWS}/{FULLY_STABLE_ROWS}")
    for e in gs_dec:
        if e["unknown_now"][0] != e["unknown_now"][1]:
            fail(f"groups_served_churn class {e['class_index']} changed unknown_now: {e}")
    if gs_dec != GS_CHURN_DECREASE:
        fail(f"groups_served_count churn set != the pinned empty churn: {gs_dec}")
    scen_first = scen_summary["closure_classes_first"]
    c34908 = [e for e in scen_first if e["class_index"] == CLASS_34908]
    if len(c34908) != 1 or c34908[0]["unknown_now"] != 6 or len(c34908[0]["groups_served"]) != 5:
        fail("scenario closure_classes_first entry for class 34908 drift (rank-7 / 6-unknown / 5-group)")

    # --- emit decomp -----------------------------------------------------------------
    out = {
        "schema": "af034loss1-adoption-decomp-deltas-v1",
        "scenario": "ADOPTED-CANONICAL",
        "packet": {"batches": [
            {"pool": "af034loss1", "class_index": 34908, "probed_rows": 1,
             "adopted_loss_rows": 1, "unadopted_win_rows": 0,
             "exhausted_excluded_rows": 0,
             "adopted_nodes_per_pool": ADOPTED_TOTAL_NODES, "whole_packet_nodes": WHOLE_PACKET_NODES},
        ],
            "adopted_loss_rows": ADOPTED_ROWS,
            "unadopted_win_rows": 0,
            "exhausted_excluded_rows": 0,
            "adopted_total_nodes_per_pass": ADOPTED_TOTAL_NODES,
            "adopted_loss_ids": adopted_ids,
            "drive_anchor_labels_60m": {k: list(v) for k, v in LABEL_PINS_60M.items()},
            "decisive_labels": "1 fresh LOSS @60M adopted (Part ED af034, two-pass fresh-cold "
                               "node-exact, published EXHAUSTED honest-UNKNOWN at 15M and 30M, "
                               "resolved only at the pre-declared 60M condition); packet is "
                               "loss-only; the 3 drive anchors are consumed NOWHERE (af001/af039 "
                               "re-check BASE rows verbatim, af029 unconsumed WIN); MISMATCH 0"},
        "cache": {"base_sha256": BASE_CACHE_SHA, "scenario_sha256": SCEN_CACHE_SHA,
                  "base_rows": len(base), "scenario_rows": len(scen), "increment_rows": len(incr),
                  "verdict_counts": {"WIN": 158, "LOSS": 6508},
                  "relation": "scenario == base rows + the 1 increment row verbatim (no other row changed)",
                  "merge_audit_runs": 3, "merge_audit_sha256_each": MERGE_AUDIT_SHA,
                  "adopted_s5_indices": ADOPTED_S5,
                  "naming_note": "shortened chain name merged-exact-s5-chain-plus-af034loss1-"
                                 "20261125.cache (the additive BASE-name-plus convention exceeds "
                                 "the 255-byte filename component limit, honestly documented in "
                                 "the declaration) - the sha pin carries the identity"},
        "class_34908": {"children_total_raw": len(child_keys_34908),
                        "children_total_s5": len(in_s5_34908),
                        "non_s5_children": 0,
                        "unknown_before": int(cb_t[CLASS_34908]["unknown_now"]),
                        "unknown_after": int(cs_t[CLASS_34908]["unknown_now"]),
                        "adopted_own": len(own_34908),
                        "unconsumed_win_children": 6,
                        "still_exhausted_children": 0,
                        "base_known_loss_children": len(known_base_34908),
                        "receipt_known_loss_children": len(receipt_child_34908),
                        "status_before": "unknown",
                        "status_after": "unknown (NOT freed, NOT excluded: 6 unconsumed "
                                        "probe-level WIN children {af029, af047, af050, af053, "
                                        "af023, af048} remain)",
                        "class_rank": [8, 7],
                        "groups_served_count": [5, 5],
                        "unknown_s5_remaining": sorted(WIN_S5_PINNED_34908.values()),
                        "not_a_root_verdict": "the loss-only adoption of the af034 row frees "
                                               "nothing and excludes nothing; free_now/coverage "
                                               "quantities are Board-derived scheduling "
                                               "bookkeeping; no root verdict and no coverage "
                                               "claim is made"},
        "class_16371": {"status": "byte-static across Part EE (not EE-owned; 2 unconsumed "
                                  "probe-level WIN children {e042, e002} remain)",
                        "class_rank": [4, 4], "groups_served_count": [3, 3], "unknown": [2, 2]},
        "class_20421": {"status": "rank churn ONLY (7 -> 8, pure frontier-cost bookkeeping; "
                                  "not EE-owned: no EE adopted key sits inside its boundary; "
                                  "6 unconsumed probe-level WIN children remain)",
                        "class_rank": [7, 8], "groups_served_count": [4, 4], "unknown": [6, 6]},
        "closure_table": {"rows_before": CLOSURE_ROWS_BEFORE, "rows_after": CLOSURE_ROWS_AFTER,
                          "left": left, "entered": entered,
                          "left_reason": "EMPTY: the 807-row frontier table is fully static "
                                         "across this Part (no left/entered exchange, no "
                                         "unknown churn beyond class 34908)",
                          "unknown_changed_classes": changed,
                          "rank_churn_only_rows": rank_churn,
                          "rank_churn_detail": [{"class_index": ci, "from": f, "to": t}
                                                for ci, f, t in rank_churn_classes],
                          "groups_served_decrease_churn": gs_dec,
                          "fully_stable_rows": stable},
        "update8": {"resolved_before": UPD8_RESOLVED_BEFORE, "resolved_after": UPD8_RESOLVED_AFTER,
                    "newly_resolved_s5": NEWLY_RESOLVED_UPD8_S5,
                    "newly_resolved_within_adopted": False,
                    "note": "the adopted s5 index (930660) sits OUTSIDE the frozen update8 "
                            "baseline requirement: the resolved count, the remaining count "
                            "and every per-root remaining are BYTE-STATIC",
                    "remaining_before": UPD8_REMAINING_BEFORE, "remaining_after": UPD8_REMAINING_AFTER,
                    "groups_free_now_static": 131},
        "class_status_counts_before": cb,
        "class_status_counts_after": cs,
        "metrics": {"joint_greedy_union_size": [JOINT_GREEDY_BEFORE, JOINT_GREEDY_AFTER],
                    "worklist_total": [WORKLIST_BEFORE, WORKLIST_AFTER],
                    "known_universe_indices": [KNOWN_UNIVERSE_BEFORE, KNOWN_UNIVERSE_AFTER],
                    "cache_rows_in_universe": [CACHE_IN_UNIVERSE_BEFORE, CACHE_IN_UNIVERSE_AFTER],
                    "unique_groups": [UNIQUE_GROUPS_BEFORE, UNIQUE_GROUPS_AFTER],
                    "per_root_remaining_delta": PER_ROOT_REMAINING_DELTA,
                    "per_root_coverage_delta": PER_ROOT_COVERAGE_DELTA,
                    "note": "the joint greedy union shrinks (36,509 -> 36,508) and the "
                            "worklist shrinks (64,415 -> 64,414) after class 34908's frontier "
                            "cost drops (unknown 7 -> 6); per-root free/uncovered thirds are "
                            "IDENTICAL at every root (nothing was freed); roots 0/12 "
                            "individual greedy unions shift as pure bookkeeping; root 27 "
                            "stays 119/119"},
        "verification": {"kit_files_verified": {"ed": ed_files, "ea": ea_files},
                         "packet_pins": {"status_log": ED_STATUS_SHA,
                                         "drive_out": ED_DRIVE_SHA,
                                         "audit_ed_json": ED_AUDIT_SHA,
                                         "ed_manifest": ED_MANIFEST_SHA},
                         "refresh_scripts_reexecuted": [BASE_REFRESH_SHA, SCEN_REFRESH_SHA],
                         "refresh_outputs_byte_identical": True,
                         "board_child_regeneration": "class-34908 56-child (all in the s5 "
                                                      "mask universe, ZERO non-s5) and "
                                                      "class-16371 / class-20421 boundaries "
                                                      "regenerated via Board(11).children"},
        "interpretation_guard":
            "only the 1 fresh af034 exact-LOSS row (published EXHAUSTED at the 15M and 30M "
            "conditions, resolved exact LOSS only at the pre-declared 60M condition) is "
            "consumed into the canonical cache by this Part; the re-probed packet is "
            "LOSS-ONLY; the af029 60M drive anchor is an unconsumed probe-level WIN consumed "
            "NOWHERE (scrutiny-owner C++ second-implementation gate pin 9193f5b6...); the 8 "
            "previously pooled unconsumed WIN rows stay unconsumed; class 34908 (6 children "
            "remaining: 6 unconsumed WIN) and classes 16371/20421 are NOT freed and NOT "
            "excluded; class status stays unknown, free_now 39 static, closure table 807 rows "
            "static with NO left/entered exchange, the single rank-churn row 20421 (7 -> 8) "
            "being pure bookkeeping; no root verdict and no coverage claim is made anywhere; "
            "the per-root/greedy/worklist quantities quoted here are bookkeeping, never "
            "verdicts; no update8 resolution changed (the adopted key sits outside the "
            "frozen baseline requirement); 11x11 stays UNKNOWN",
    }
    (EXP / "output/decomp-deltas-af034loss1-adoption.json").write_text(
        json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("DECOMP OK changed=%d rank_churn=%d gs_dec=%d stable=%d left=%d entered=%d" % (
        len(changed), rank_churn, len(gs_dec), stable, len(left), len(entered)))
    print("class34908: unknown 7 -> 6 (1 adopted, 6 unconsumed WINs remain), NOT freed, rank 8 -> 7")
    print("class16371: byte-static; class20421: rank churn only (7 -> 8), no EE key inside either boundary")
    print("update8: byte-static (af034 s5 930660 outside the frozen requirement)")


if __name__ == "__main__":
    main()
