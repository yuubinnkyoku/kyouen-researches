"""BASE (canonical chain through the Part EI b39loss46 adoption)
vs SCENARIO (ek-aj039loss1 = Part EL single-row aj039loss1 adoption).

Fail-closed machine recomputation of exactly what the Part EL single-LOSS
canonical adoption changed, from published bytes only:

* every published artifact sha-pinned (the published Part EI outputs -- the
  BASE canonical cache 73482be0... 6,712 rows WIN 158 / LOSS 6,554, the BASE
  reaudit outputs refresh-summary 414314eb... / closure-classes e12bf328... /
  per-root-coverage 2525f306... / probe-worklist regen pin 98529a8d... -- the
  Part EL outputs -- increment 7838b081..., increments manifest 34439f4d...
  (schema ek-aj039loss1-increments-manifest-v1), the 6,713-row scenario
  cache cf08e181... WIN 158 / LOSS 6,555 (chain name
  merged-exact-s5-chain-plus-aj039loss1-20261125.cache; the sha pin carries
  the identity), the merge-audits x3 (identical sha 0ab05a15...), the
  byte-clones of the union merger 90711961... and both refresh forks (the
  published Part EI refresh 1bcf1972... and the published Part EL refresh
  c0debd18...), the frozen graph/update8/board/policy/quarantine pins);
* the published Part EI refresh fork and the published Part EL refresh fork
  are RE-EXECUTED byte-verbatim in isolated scratch trees against their
  pinned inputs, and all eight outputs must be byte-identical to the
  published / regenerated pins before any delta is emitted (double-run
  determinism; this simultaneously re-proves the published Part EI reaudit
  outputs are regenerable from published bytes);
* SCEN cache == BASE cache rows + exactly the 1 increment row (verdict
  agreement everywhere; 6,713 rows, WIN 158 / LOSS 6,555); the adopted row is
  the aj039 fresh exact-LOSS row of the published Part EK 30M re-probe kit
  (42 published files, MANIFEST rev2 97574401..., audit_ek.json d9aa8aab...
  79/79 gates PASS: two-pass fresh-cold node-exact at the pre-declared 30M
  budget, order 0, nodes 16,549,916 per pass, MISMATCH 0, resolved in
  (15M, 30M] beyond the honest EXHAUSTED 15M history of batch-39 - not a
  same-condition re-probe; the aj030 probe-level WIN row 15,284,699 and the
  batch-39 probe-level WIN rows aj049/aj050 are consumed NOWHERE; the 2
  claim-reserved dual-class batch-38 keys ai044/ai048 are Part EF in-flight
  owner and untouched);
* the class-30484 arithmetic is recomputed from the frozen dependency graph
  with the integer-geometry Board: the 54-child canonical boundary is
  regenerated (entirely inside the s5 mask universe; ZERO non-s5 children;
  ZERO update8-receipt children); 48 children are known exact LOSS in BASE
  and exactly 6 are unknown in BASE and exactly 5 in SCEN == the pinned 5
  remaining unknown s5 keys {892576 aj030 probe-level WIN unconsumed,
  900354 ai044 claim-reserved, 900718 ai048 claim-reserved, 902511 aj049
  probe-level WIN unconsumed, 902512 aj050 probe-level WIN unconsumed}; the
  adopted aj039 (s5_index 897668) is the ONLY adopted row and sits inside
  this boundary; class 30484 is NOT freed and NOT excluded (unknown 6 -> 5,
  rank 9 -> 7, groups_served_count 4 static);
* classes 30118 / 16371 are proven BYTE-STATIC across this Part (closure
  rows byte-identical before/after; the adopted key sits outside both Board
  boundaries; 30118 keeps unknown 52 / rank 21); classes 20421 / 34908 are
  rank-churn-only (rank 8 -> 9 / 7 -> 8; unknown_now static; the adopted key
  sits outside both Board boundaries);
* every closure-classes.csv row is compared: ZERO unknown_now changes beside
  class 30484; ZERO left/entered rows; exactly 2 rank-churn-only rows and
  ZERO groups_served churn (804 fully stable rows);
* update8 refresh: the adopted aj039 s5 index 897668 sits OUTSIDE the frozen
  update8 baseline requirement: resolved stays 259, remaining stays 31,600,
  groups_free_now stays 131, the newly-resolved/lost sets are both EMPTY,
  win_hit_groups stays [] and every per-root remaining is byte-identical;
* class_status counts: excluded 390 / excluded_now 23 / free_now 39 /
  unknown 34,497 IDENTICAL before and after (the loss-only adoption frees
  nothing and excludes nothing); Board verification 39/39 with zero
  rejections on both sides; root 27 stays 119/119;
* per-root coverage: free/uncovered thirds are IDENTICAL at every root; the
  individual greedy union changes only at root 24 (2,782 -> 2,781 pure
  re-selection bookkeeping, no coverage claim);
* the frozen greedy scheduler deltas are recorded as bookkeeping (joint
  greedy 36,505 static, worklist 64,366 -> 64,365, known universe 891 -> 892,
  cache in universe 868 -> 869).

No unknown verdict is asserted anywhere.  The standard 11x11 empty board
and every one of the 19 central-reply roots stay UNKNOWN; free_now /
coverage quantities are scheduling bookkeeping derived from exact LOSS
verdicts, not root verdict claims.  The aj030/aj049/aj050 probe-level WIN
rows and the 2 claim-reserved batch-38 keys are consumed NOWHERE by this
Part (scrutiny-owner C++ second-implementation gate pin 9193f5b6...); no
WIN verdict and no EXHAUSTED verdict enters the canonical cache; 11x11
stays UNKNOWN.
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

BASE_EXP = ROOT / "research/experiments/n11-centralreply-b39loss46-adoption-reaudit-20261125"
BASE_OUT = BASE_EXP / "reaudit/output"
BASE_CACHE = BASE_EXP / "output/merged-exact-s5-chain-plus-b39loss46-20261125.cache"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-aj039loss1-20261125.cache"
INCR = EXP / "output/increment-aj039loss1-20261125.cache"
MANIFEST = EXP / "output/increments-manifest.json"
EK_KIT = ROOT / "research/experiments/n11-centralreply-closure-class30484-aj030aj039-reprobe30m-20261125"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_REFRESH_SCRIPT = BASE_EXP / "reaudit/scripts/refresh_adoption_ei.py"
SCEN_REFRESH_SCRIPT = EXP / "reaudit/scripts/refresh_adoption_el.py"
MERGER = EXP / "scripts/s5_union_merge.py"

BASE_CACHE_SHA = "73482be0cf0201b2d812f9205b0315e91527234e02196691279753853feddc70"
SCEN_CACHE_SHA = "cf08e1817a369853747706872763046c4544e289eae6d847bfd27d7503d23e7d"
INCR_SHA = "7838b08131c5ee5bd8a2819ee8e3bcb4fb9733034f495e7da24b2758890ad36a"
MANIFEST_SHA = "34439f4d86d5fd9b064600af2201311eac54c074580c8e94c965933c9daec703"
BASE_SUMMARY_SHA = "414314eb38776f7fee69b3f6d1b894ab24b8e4fac4ea578bc109fce82863329f"
BASE_CLOSURE_SHA = "e12bf3280c77e31fc91e30e6806d2828b141af565bfa5e565a2aa3410d974673"
BASE_PRC_SHA = "2525f3069826a055bf9bf4343c08ac217722beefdce054138a68a0976c875b8d"
BASE_WORKLIST_SHA = "98529a8ddd457c09506a80ce2f7a6344fee3c3fcc0d63969aa391e67ad6c8e79"
SCEN_SUMMARY_SHA = "4579a0217d0b71301605337513cf92e98d7656b7d8ceffcbe27f10b4efac8a3c"
SCEN_CLOSURE_SHA = "880e1c373d1944f458fcb34d6d314b86a9b374cad5c704c4d95108a163355f10"
SCEN_PRC_SHA = "bafc7b669a486ca8afa2305e09021e36a4cb0e5c5a8c888095464eb9b8cd7af8"
SCEN_WORKLIST_SHA = "ed289920f527ee551c4c29bbf5cf012c7bddf0f4acca2fd3ddae4b919d7fad7c"
BASE_REFRESH_SHA = "1bcf1972be102781d056f6caae15bfc239c145d79700b74b6bac3919f03da2d6"
SCEN_REFRESH_SHA = "c0debd185919fb9791fa0f9ca07883d682429e536c8f31c65548047032ab02b1"
MERGE_AUDIT_SHA = "0ab05a15e3f31f35011dac2e729c1fdb134912f23af926ba0233a837dac202b5"
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
BOARD_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
ADOPTED_TABLE_DIGEST = "cd77a0d107b99ef7515b3e1f95a0913cfc514a4c2240a8e003743d8db06ebc52"

EK_MANIFEST_SHA = "97574401309964806a8eed4968496dcd222aecaf029aa9b1115dcaaa2ec78a68"
EK_KIT_FILES = 42
EK_STATUS_SHA = "868bfbff196343d074c909b0290739a0111f2b3dcfc04967f459528dbab6c01c"
EK_AUDIT_JSON_SHA = "d9aa8aab971ca0975caea7e52156bea86b3c183d843a40a8cea44a8dcf54691b"
EK_AUDIT_PY_SHA = "7636def1cc7ca87171a0716e8eb76386ea9965485f28a942a53137439ac4bcfb"
JSREPLAY_SHA = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
RUNNER_SHA = "3b5083b47c043f93bbe01a5f3335baba6be6d1d6929885f4ab5b28b1778cf7b4"
B39_STATUS_SHA = "08d70bb77c08e7a37b77005b3b2dca1a759f56b4146e1623eef4eb69759a3cea"
B39_EXHAUSTED_LINES = [
    "2026-11-25T09:56:39Z aj030 EXHAUSTED 15000000,0,15000000",
    "2026-11-25T10:06:11Z aj039 EXHAUSTED 15000000,0,15000000",
]

CLASS_30484 = 30484
CLASS_30118 = 30118
CLASS_16371 = 16371
CLASS_20421 = 20421
CLASS_34908 = 34908
ADOPTED_ROWS = 1
ADOPTED_TOTAL_NODES = 16549916
WHOLE_PACKET_NODES = 31834615

ADOPTED_IDS = ["aj039"]
WIN_IDS_UNCONSUMED = ["aj030"]
ANCHOR_IDS = ["aj001", "aj049", "af039"]
PROBED_IDS = ["aj030", "aj039"]
CLAIM_RESERVED_IDS = ["ai044", "ai048"]
CLAIM_RESERVED_PAIRS = {
    "ai044": (1152922604135256064, 65536),
    "ai048": (1152921573327372288, 68157440),
}
UNCONSUMED_WIN_NO_CACHE = {
    "aj049": (1152921574400065536, 1114112),
    "aj050": (1152921574400065536, 68157440),
}
KEY_PINS = {
    "aj039": {"lo": 1152922606282735616, "hi": 65536, "legal": 88,
              "s5_index": 897668, "probe_order": 578,
              "membership_class_count": 4},
    "aj030": {"lo": 1152922604135251976, "hi": 65536, "legal": 83,
              "s5_index": 892576, "probe_order": 569,
              "membership_class_count": 4},
    "aj001": {"lo": 1152922604269469696, "hi": 65536, "legal": 84,
              "s5_index": 63021},
    "aj049": {"lo": 1152921574400065536, "hi": 1114112, "legal": 80,
              "s5_index": 902511},
    "af039": {"lo": 1152921504607895681, "hi": 68719476736, "legal": 89},
}
LABEL_PINS = {
    "aj039": (2, 16549916),
    "aj030": (1, 15284699),
    "aj001": (2, 5156075),
    "aj049": (1, 4998452),
    "af039": (2, 19234232),
}
EXH_LABEL_PINS = {"aj030": (0, 15000000), "aj039": (0, 15000000)}
BUDGET = 30000000
EXH_BUDGET = 15000000
STATUS_ALL_LINES = [
    "2026-11-25T14:06:22Z aj049 PASS 30000000,1,4998452",
    "2026-11-25T14:06:22Z aj049 WIN-HALT",
    "2026-11-25T14:06:25Z aj001 PASS 30000000,2,5156075",
    "2026-11-25T14:12:54Z aj030 PASS 30000000,1,15284699",
    "2026-11-25T14:12:54Z aj030 WIN-HALT",
    "2026-11-25T14:13:33Z af039 PASS 30000000,2,19234232",
    "2026-11-25T14:17:28Z aj039 PASS 30000000,2,16549916",
]

RAW_SHAS = {
    "aj039.p1.out": "529b3efeefd4c3d2c12988c9254b4a39931405708b707dece56dc9a508863238",
    "aj039.p2.out": "930d0b48063c1b0f18381beaa16d038c1129406539da579b68a8224fa9274dd8",
    "aj030.p1.out": "a0c88b3511d551fec1efa3069a7df59b1291bce2ae4bcb24cdb2bcda70573c7b",
    "aj030.p2.out": "f0eb149af394f79f795186bf714d7da23a22c0df07d7bc2f1e35d6d661613062",
    "aj001.p1.out": "41a6b129005bd360741d89b48be2b3e35bba38d26fa9c08228e4519f2747ade1",
    "aj001.p2.out": "0348aa062d7a488f8d802fcaec18c43dd87faa41089c63f0f78ee9a9922dd5ab",
    "aj049.p1.out": "741f62f999d6944dc5d6151850f9f1960051b56c476ee53fd5b611dae8c49af5",
    "aj049.p2.out": "850df2ae34a0f3e437a83f557e57b8ccca59ab418de54c64fd06beea212b9257",
    "af039.p1.out": "2ba27ad40d2b344491f52e6efc724312ee3f597b9a9d7a8d194c60c6740a2fb4",
    "af039.p2.out": "93b3a25d25b96af4cc27eb6994ece201be6befa1b40722d61b5cf18303019a7e",
}
EXH_RAW_SHAS = {
    "aj030.p1.out": "843a0a0c976699d937391377455504797f5bece24222eef74d4452f20e20178c",
    "aj030.p2.out": "661c8e410f8e3f93227ac635233556fec5069ccf115117255a38b3b19f551757",
    "aj039.p1.out": "60ae21db0e099b22403b8ce64ba97e15de3987acfafb218d79c11aae6c3b4906",
    "aj039.p2.out": "c51899d50649444c3ee8cbb43f3318392131cc3add8b54cbe77d3f600a59dfbb",
}
INPUT_CSV_SHAS = {
    "aj039": "82f8dff3136ce54e33203f69f3589b72891a41129b11f7b0811b4053e9858394",
    "aj030": "520ee52abefaec80b800245dd1913489cd511923732e14d3315f4806aec83595",
    "aj001": "2f6daea5ca3b3fe6b7713c8d450af3f3c9f203acacb8a1340255d8e8f656496c",
    "aj049": "46349391b3aa212cf7ffffbeae94d01b5202f25ca24a6c5294b75ced6184951a",
    "af039": "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691",
}

# class 30484 (the EL target): Board 54-child boundary, all in the s5 universe
BOUNDARY_30484_RAW = 54
BASE_KNOWN_LOSS_30484 = 48
UNKNOWN_BASE_30484 = 6
UNKNOWN_SCEN_30484 = 5
WIN_S5_PINNED = {"aj030": 892576, "aj049": 902511, "aj050": 902512}
RESERVED_S5_PINNED = {"ai044": 900354, "ai048": 900718}
UNKNOWN_S5_REMAINING = [892576, 900354, 900718, 902511, 902512]
ADOPTED_S5 = 897668
# secondary dual-class owner 30118: BYTE-STATIC (aj039 outside its boundary)
BOUNDARY_30118_RAW = 56
OWN_ADOPTED_30118 = 0
UNKNOWN_30118_STATIC = 52
# byte-static witness classes
BOUNDARY_16371_RAW = 52
BOUNDARY_20421_RAW = 50
BOUNDARY_34908_RAW = 56

STATUS_EXPECTED = {"excluded": 390, "excluded_now": 23, "free_now": 39, "unknown": 34497}
UPD8_RESOLVED_BEFORE = 259
UPD8_RESOLVED_AFTER = 259
UPD8_REMAINING_BEFORE = 31600
UPD8_REMAINING_AFTER = 31600
JOINT_GREEDY_BEFORE = 36505
JOINT_GREEDY_AFTER = 36505
WORKLIST_BEFORE = 64366
WORKLIST_AFTER = 64365
KNOWN_UNIVERSE_BEFORE = 891
KNOWN_UNIVERSE_AFTER = 892
CACHE_IN_UNIVERSE_BEFORE = 868
CACHE_IN_UNIVERSE_AFTER = 869
CACHE_VERDICTS_BEFORE = {"1": 158, "2": 6554}
CACHE_VERDICTS_AFTER = {"1": 158, "2": 6555}
UNIQUE_GROUPS_BEFORE = 2115
UNIQUE_GROUPS_AFTER = 2115
GROUP_BEST_NONFREE = 2115
PER_ROOT_REMAINING_DELTA = {}
PER_ROOT_COVERAGE_DELTA = {
    "24": {"free": [12, 12], "uncovered": [107, 107], "greedy": [2782, 2781]},
}
CLOSURE_ROWS_BEFORE = 807
CLOSURE_ROWS_AFTER = 807
CLOSURE_LEFT = []
CLOSURE_ENTERED = []
CLASS_30484_ROW_BEFORE = {"class_rank": "9", "unknown_now": "6", "groups_served_count": "4"}
CLASS_30484_ROW_AFTER = {"class_rank": "7", "unknown_now": "5", "groups_served_count": "4"}
RANK_CHURN_DETAIL = [(20421, 8, 9), (34908, 7, 8)]
GS_CHURN_DECREASE = []
RANK_CHURN_ROWS = 2
FULLY_STABLE_ROWS = 804
CHANGED_CLASS_SET = []


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
        cache[(int(row[1]), int(row[2]))] = (int(row[4]), int(row[5]))
    return cache


def verify_ek_kit():
    if sha(EK_KIT / "MANIFEST-sha256.txt") != EK_MANIFEST_SHA:
        fail("Part EK kit MANIFEST rev2 sha drift")
    n = 0
    for line in (EK_KIT / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split()
        want, rel = fields[0], fields[1]
        if rel.startswith("/") or ".." in rel.split("/"):
            fail(f"Part EK MANIFEST unsafe path: {rel}")
        p = EK_KIT / rel
        if not p.is_file():
            fail(f"Part EK kit file missing: {rel}")
        if sha(p) != want:
            fail(f"Part EK kit sha drift at {rel}")
        n += 1
    if n != EK_KIT_FILES:
        fail(f"Part EK kit files {n} != {EK_KIT_FILES}")
    if sha(EK_KIT / "scripts/jsreplay.js") != JSREPLAY_SHA:
        fail("jsreplay.js sha drift in the Part EK kit (pinned solver image 8458...)")
    if sha(EK_KIT / "scripts/runbatch_ek-30m.sh") != RUNNER_SHA:
        fail("runbatch_ek-30m.sh sha drift in the Part EK kit (pinned 3b50...)")
    if sha(EK_KIT / "scripts/audit_ek.py") != EK_AUDIT_PY_SHA:
        fail("audit_ek.py sha drift in the Part EK kit (CORRECTION sha 7636def1)")
    return n


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


def two_pass_raw(raw_dir: Path, kid: str, shas: dict, budget: int):
    rows = {}
    for tag in ("p1", "p2"):
        p = raw_dir / f"{kid}.{tag}.out"
        if sha(p) != shas[f"{kid}.{tag}.out"]:
            fail(f"raw replay sha drift vs the pinned published bytes: {kid}.{tag}.out")
        row = None
        seen = 0
        for line in p.read_text().splitlines():
            if line.startswith("replay,"):
                parts = line.split(",")
                seen += 1
                row = {"stones": int(parts[2]), "legal": int(parts[3]),
                       "is_or": int(parts[4]), "budget": int(parts[5]),
                       "result": int(parts[6]), "nodes": int(parts[7]),
                       "lo": parts[9], "hi": parts[10]}
        if seen != 1 or row is None:
            fail(f"expected exactly one replay row in {p}")
        if "# replay_done" not in p.read_text():
            fail(f"raw {kid}.{tag}.out lacks the '# replay_done' completeness guard")
        rows[tag] = row
    ref = rows["p1"]
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
    for tag, r in rows.items():
        if tuple(r[f] for f in fields) != tuple(ref[f] for f in fields):
            fail(f"two-pass raw disagreement (fresh-cold node-exact gate): {kid}.{tag}")
    if ref["budget"] != budget:
        fail(f"{kid}: raw budget drift (expected {budget})")
    return ref


def main() -> None:
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
        ("ek kit status", EK_KIT / "output/status.log", EK_STATUS_SHA),
        ("ek kit audit", EK_KIT / "output/audit_ek.json", EK_AUDIT_JSON_SHA),
        ("ek kit b39-status", EK_KIT / "sources/b39-status.log", B39_STATUS_SHA),
    ]
    for name, p, want in pins:
        got = sha(p)
        if got != want:
            fail(f"{name} sha drift: {got} != {want}")
    kit_files = verify_ek_kit()

    # --- Part EK audit honesty pins -----------------------------------------
    audit = json.loads((EK_KIT / "output/audit_ek.json").read_text())
    if audit["schema"] != "n11-ek-aj030aj039-reprobe30m-audit-v1":
        fail("Part EK audit schema drift")
    if audit["gates_total"] != 79 or audit["gates_failed"] != []:
        fail("Part EK audit gates 79/79 accounting drift")
    if audit["all_gates_pass"] is not True:
        fail("Part EK audit all_gates_pass must be true")
    if audit["verdict_consumed"] is not False:
        fail("Part EK audit verdict_consumed must be false (probe-time honesty)")
    if audit["main_probes"]["aj039"]["result"] != 2 or \
            audit["main_probes"]["aj039"]["nodes"] != 16549916:
        fail("Part EK audit aj039 honest-label drift")
    if audit["main_probes"]["aj030"]["result"] != 1 or \
            audit["main_probes"]["aj030"]["nodes"] != 15284699:
        fail("Part EK audit aj030 honest-label drift")
    lines = (EK_KIT / "output/status.log").read_text().splitlines()
    if lines != STATUS_ALL_LINES:
        fail("Part EK status.log != the pinned 7-line honest history")
    b39_lines = (EK_KIT / "sources/b39-status.log").read_text().splitlines()
    exhausted_now = [l for l in b39_lines if " EXHAUSTED " in l and
                     ("aj030" in l or "aj039" in l)]
    if exhausted_now != B39_EXHAUSTED_LINES:
        fail("b39-status honest EXHAUSTED history lines drift")

    # --- Part EK raws: adopted aj039, unconsumed aj030, anchors -------------
    for kid in PROBED_IDS + ANCHOR_IDS:
        e = KEY_PINS[kid]
        ref = two_pass_raw(EK_KIT / "output/raw", kid, RAW_SHAS, BUDGET)
        if ref["stones"] != 5 or ref["is_or"] != 0:
            fail(f"{kid}: wrong depth/or bit")
        if ref["legal"] != e["legal"] or ref["lo"] != str(e["lo"]) or ref["hi"] != str(e["hi"]):
            fail(f"{kid}: raw key-field disagreement vs the pinned key fields")
        if (ref["result"], ref["nodes"]) != LABEL_PINS[kid]:
            fail(f"{kid}: raw honest-label drift vs the pinned audit label")
        p_in = EK_KIT / f"input/{kid}.input.csv"
        if sha(p_in) != INPUT_CSV_SHAS[kid]:
            fail(f"input csv {kid} sha drift vs the pinned published bytes")
        want_line = f"target,0,5,{e['lo']},{e['hi']},{e['legal']},0,0,0,0,0"
        rows_in = [l for l in p_in.read_text().splitlines() if l.strip()]
        if rows_in != [want_line]:
            fail(f"input csv {kid} body drift: {rows_in}")
    for kid in ("aj030", "aj039"):
        e = KEY_PINS[kid]
        ref = two_pass_raw(EK_KIT / "sources/exh15m", kid, EXH_RAW_SHAS, EXH_BUDGET)
        if (ref["result"], ref["nodes"]) != EXH_LABEL_PINS[kid]:
            fail(f"{kid}: exh15m honest-history label drift")
        if ref["lo"] != str(e["lo"]) or ref["hi"] != str(e["hi"]):
            fail(f"{kid}: exh15m key disagreement vs the pinned key fields")

    # --- manifest decomposition ---------------------------------------------
    manifest = json.loads(MANIFEST.read_text())
    if manifest["schema"] != "ek-aj039loss1-increments-manifest-v1":
        fail("manifest schema drift")
    if manifest["base_cache_sha256"] != BASE_CACHE_SHA:
        fail("manifest base cache pin drift")
    if manifest["sha256"]["loss_increment"] != INCR_SHA:
        fail("manifest loss_increment pin drift")
    if manifest["merger_sha256"] != MERGER_SHA:
        fail("manifest merger pin drift")
    if manifest["adopted_table_digest_sha256"] != ADOPTED_TABLE_DIGEST:
        fail("manifest adopted-table digest drift")
    if len(manifest["adopted_table"]) != ADOPTED_ROWS:
        fail("manifest adopted_table must hold 1 row")
    if sum(r["nodes"] for r in manifest["adopted_table"]) != ADOPTED_TOTAL_NODES:
        fail("manifest adopted_table node sum drift")
    if manifest["base_cache_rows"] != 6712:
        fail("manifest base rows drift")
    if manifest["base_cache_absent_hits_for_emitted"] != 0:
        fail("manifest emitted row must be absent from BASE")
    if manifest["quarantine_hits"] != 0:
        fail("manifest quarantine hits must be 0")
    if manifest["row_counts"] != {"adopted_loss_rows": 1,
                                  "wins_unconsumed_this_pool": 1,
                                  "exhausted_history_prior": 2,
                                  "claim_reserved_excluded": 2,
                                  "prior_canonical_rows_base": 6712}:
        fail("manifest row_counts drift")
    if manifest["loss_ids"] != ADOPTED_IDS or manifest["resolved_ids"] != ADOPTED_IDS:
        fail("manifest loss/resolved id sets drift")
    if manifest["unadopted_win_ids"] != WIN_IDS_UNCONSUMED:
        fail("manifest unconsumed WIN id set drift")
    if manifest["full_packet_eq_loss_only"] is not False:
        fail("manifest full_packet_eq_loss_only must be false (packet spans 1 LOSS + 1 WIN)")
    if manifest["win_scenario_exists"] is not True:
        fail("manifest win_scenario_exists must be true (aj030 probe-level WIN in pool)")
    wr = manifest["unadopted_win_rows"]
    if len(wr) != 1:
        fail("manifest must hold exactly one unconsumed WIN row (aj030)")
    if (wr[0]["lo"], wr[0]["hi"], wr[0]["legal"], wr[0]["result"], wr[0]["nodes"]) != (
            KEY_PINS["aj030"]["lo"], KEY_PINS["aj030"]["hi"], KEY_PINS["aj030"]["legal"],
            1, LABEL_PINS["aj030"][1]):
        fail("manifest unconsumed aj030 WIN row pin drift")
    eh = manifest["exhausted_history_15m"]
    for kid in ("aj030", "aj039"):
        if (eh[kid]["result"], eh[kid]["nodes"]) != EXH_LABEL_PINS[kid]:
            fail(f"manifest exhausted_history_15m {kid} drift")
        if eh[kid]["key"] != [KEY_PINS[kid]["lo"], KEY_PINS[kid]["hi"]]:
            fail(f"manifest exhausted_history_15m {kid} key drift")
    if len(manifest["batches"]) != 1:
        fail("manifest must hold exactly one batch pool")
    b = manifest["batches"][0]
    if b["pool"] != "ek-aj039loss1":
        fail("unexpected pool in the EL manifest")
    if b["adopted_loss_ids"] != ADOPTED_IDS:
        fail("pool adopted id set drift")
    if sorted(b["probed_ids"]) != sorted(PROBED_IDS):
        fail("pool probed id set drift")
    if sorted(b["anchor_ids"]) != sorted(ANCHOR_IDS):
        fail("pool anchor id set drift")
    if b["unadopted_win_ids"] != WIN_IDS_UNCONSUMED:
        fail("pool unconsumed WIN id set drift")
    if b["claim_reserved_excluded_ids"] != CLAIM_RESERVED_IDS:
        fail("pool claim-reserved id set drift")
    if b["adopted_nodes_per_pool"] != ADOPTED_TOTAL_NODES or \
            b["whole_packet_nodes"] != WHOLE_PACKET_NODES:
        fail("pool node accounting drift")
    if b["status_log_sha256"] != EK_STATUS_SHA or b["status_log_lines"] != 7:
        fail("pool status-log pin drift")
    if b["probed_budget"] != 30000000 or b["exhausted_history_budget"] != 15000000:
        fail("pool budget pins drift (30M condition vs 15M honest exhaustion)")
    if b["b39_exhausted_history_lines"] != B39_EXHAUSTED_LINES:
        fail("pool honest-exhaustion history lines drift")
    ki_ = b["kit_integrity"]
    if ki_["kit_manifest_sha256"] != EK_MANIFEST_SHA or ki_["kit_files_verified"] != EK_KIT_FILES:
        fail("pool kit integrity pins drift")
    if ki_["raw_file_sha256_pins"] != RAW_SHAS:
        fail("pool raw-file pin table drift")
    if ki_["audit_ek_json_sha256"] != EK_AUDIT_JSON_SHA:
        fail("pool audit_ek.json pin drift")
    for cid, key in CLAIM_RESERVED_PAIRS.items():
        if tuple(b["claim_reserved_pairs"][cid]) != key:
            fail(f"pool claim-reserved pair drift for {cid}")
    for cid, key in UNCONSUMED_WIN_NO_CACHE.items():
        if tuple(b["unconsumed_win_no_cache_pairs"][cid]) != key:
            fail(f"pool unconsumed no-cache pair drift for {cid}")

    # --- refresh re-execution (double-run determinism) -----------------------
    base_tmp = rerun_refresh(BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA, ".elverify-base-ei")
    scen_tmp = rerun_refresh(SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA, ".elverify-scen-el")
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
    shutil.rmtree(ROOT / "research/experiments/.elverify-base-ei")
    shutil.rmtree(ROOT / "research/experiments/.elverify-scen-el")

    # --- cache relation: SCEN == BASE + exactly the 1 increment row ----------
    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    incr = load_cache(INCR)
    if len(base) != 6712 or len(scen) != 6713 or len(incr) != ADOPTED_ROWS:
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
        fail("scenario cache != BASE rows + increment row (set difference)")
    wins = sum(1 for v in scen.values() if v[0] == 1)
    losses = len(scen) - wins
    if (wins, losses) != (158, 6555):
        fail(f"scenario verdict counts {wins}/{losses} != 158/6,555")
    adopted_key = (KEY_PINS["aj039"]["lo"], KEY_PINS["aj039"]["hi"])
    if set(incr) != {adopted_key}:
        fail("increment key set != the pinned adopted aj039 key")
    tab = {(int(e["lo"]), int(e["hi"])): e for e in manifest["adopted_table"]}
    if set(tab) != set(incr):
        fail("manifest adopted_table keys != increment keys")
    for key, row in incr.items():
        if row != (tab[key]["result"], tab[key]["nodes"]):
            fail(f"manifest adopted_table row != increment row: {key}")
        if tab[key]["legal"] != KEY_PINS["aj039"]["legal"]:
            fail("manifest adopted_table legal drift")
    for kid in WIN_IDS_UNCONSUMED:
        key = (KEY_PINS[kid]["lo"], KEY_PINS[kid]["hi"])
        if key in incr or key in base or key in scen:
            fail(f"the unconsumed key {kid} must sit in NO cache (WIN scrutiny gate)")
    for kid, key in UNCONSUMED_WIN_NO_CACHE.items():
        if key in incr or key in base or key in scen:
            fail(f"the unconsumed batch-39 WIN key {kid} must sit in NO cache")
    for cid, key in CLAIM_RESERVED_PAIRS.items():
        if key in incr or key in base or key in scen:
            fail(f"the claim-reserved batch-38 key {cid} must sit in NO cache (Part EF owner)")

    # --- Board arithmetic ------------------------------------------------------
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
    if mask_to_index[adopted_key] != ADOPTED_S5:
        fail("adopted aj039 s5 index != the pinned 897668")
    if ADOPTED_S5 in update8["required_new_s5"]:
        fail("the adopted aj039 s5 index sits inside the frozen update8 baseline requirement")

    # --- class 30484 (the EL target) -----------------------------------------
    lo, hi = s4_masks[CLASS_30484]
    children = board.children(lo | (hi << 64))
    child_keys = {(c & ((1 << 64) - 1), c >> 64) for c in children}
    if len(child_keys) != BOUNDARY_30484_RAW:
        fail(f"class-30484 Board child boundary {len(child_keys)} != {BOUNDARY_30484_RAW}")
    non_s5 = [k for k in child_keys if k not in mask_to_index]
    if non_s5:
        fail("class-30484 boundary must have ZERO non-s5 children")
    in_s5 = list(child_keys)
    receipt_child = [k for k in in_s5 if mask_to_index[k] in receipt_verdicts]
    if receipt_child:
        fail("class-30484 must have ZERO update8-receipt children")
    known_base = [k for k in in_s5 if k in base]
    if len(known_base) != BASE_KNOWN_LOSS_30484:
        fail(f"class-30484 BASE-known child count {len(known_base)} != {BASE_KNOWN_LOSS_30484}")
    for k in known_base:
        if base[k][0] != 2:
            fail("a BASE-known child of 30484 is not an exact LOSS")
    unknown_base = [k for k in in_s5 if k not in base]
    if len(unknown_base) != UNKNOWN_BASE_30484:
        fail(f"class-30484 BASE unknown {len(unknown_base)} != {UNKNOWN_BASE_30484}")
    unknown_scen = [k for k in in_s5 if k not in scen]
    if len(unknown_scen) != UNKNOWN_SCEN_30484:
        fail(f"class-30484 SCEN unknown {len(unknown_scen)} != {UNKNOWN_SCEN_30484} (NOT freed)")
    if sorted(mask_to_index[k] for k in unknown_scen) != UNKNOWN_S5_REMAINING:
        fail("scenario unknown children of 30484 != the pinned 5 remaining s5 keys")
    own = set(in_s5) & set(incr)
    if own != set(incr):
        fail("class-30484 adopted-own set != exactly the 1 EL row")
    if any(k in quarantined for k in child_keys):
        fail("a quarantined key sits inside the class-30484 child boundary")

    # --- secondary dual-class owner 30118 + witness classes -------------------
    lo2, hi2 = s4_masks[CLASS_30118]
    kids2 = {(c & ((1 << 64) - 1), c >> 64) for c in board.children(lo2 | (hi2 << 64))}
    if len(kids2) != BOUNDARY_30118_RAW:
        fail(f"class-30118 Board child boundary {len(kids2)} != {BOUNDARY_30118_RAW}")
    own2 = kids2 & set(incr)
    if len(own2) != OWN_ADOPTED_30118:
        fail("class-30118 must hold ZERO adopted members (aj039 outside its boundary)")
    unk2b = [k for k in kids2 if k not in base]
    unk2s = [k for k in kids2 if k not in scen]
    if len(unk2b) != UNKNOWN_30118_STATIC or len(unk2s) != UNKNOWN_30118_STATIC:
        fail(f"class-30118 unknown must stay {UNKNOWN_30118_STATIC}/{UNKNOWN_30118_STATIC} (byte-static)")
    for cls, boundary in ((CLASS_16371, BOUNDARY_16371_RAW),
                          (CLASS_20421, BOUNDARY_20421_RAW),
                          (CLASS_34908, BOUNDARY_34908_RAW)):
        clo, chi = s4_masks[cls]
        kids = {(c & ((1 << 64) - 1), c >> 64) for c in board.children(clo | (chi << 64))}
        if len(kids) != boundary:
            fail(f"class-{cls} Board child boundary drift")
        if set(incr) & kids:
            fail(f"no adopted key may sit inside the class-{cls} boundary (not EL-owned)")
        if any(k in quarantined for k in kids):
            fail(f"a quarantined key sits inside the class-{cls} boundary")

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
    if newly or lost:
        fail("update8 newly-resolved/lost sets must BOTH be empty (aj039 sits outside)")
    if rb["groups_free_now"] != 131 or rs["groups_free_now"] != 131:
        fail("update8 groups_free_now drift (must stay 131 static)")
    if rs.get("win_hit_groups", rb.get("win_hit_groups")) not in ([], None):
        fail("win_hit_groups non-empty (a WIN was consumed)")

    # --- class status / universe metrics ------------------------------------
    cb, cs = base_summary["class_status_counts"], scen_summary["class_status_counts"]
    if cb != STATUS_EXPECTED or cs != STATUS_EXPECTED:
        fail(f"class status counts drift vs the pinned static transition: {cb} {cs}")
    if scen_summary["board_verification"] != {"free_candidates": 39, "board_verified_free": 39, "rejected": {}}:
        fail("scenario board verification shape drift")
    if base_summary["board_verification"] != {"free_candidates": 39, "board_verified_free": 39, "rejected": {}}:
        fail("base board verification shape drift")
    if scen_summary["inputs"]["cache_rows"] != 6713 \
            or scen_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_AFTER \
            or scen_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_AFTER:
        fail("scenario inputs metrics drift")
    if base_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["cache_rows"] != 6712:
        fail("base inputs metrics drift")
    bcv, scv = base_summary["inputs"]["cache_verdicts"], scen_summary["inputs"]["cache_verdicts"]
    if bcv != CACHE_VERDICTS_BEFORE or scv != CACHE_VERDICTS_AFTER:
        fail("cache verdict counts drift")

    # per-root coverage: free/uncovered thirds identical at EVERY root
    prc_pairs = list(zip(
        csv.DictReader(BASE_OUT.joinpath("per-root-coverage.csv").open()),
        csv.DictReader((EXP / "reaudit/output/per-root-coverage.csv").open())))
    prc_delta = {}
    for bb, srow in prc_pairs:
        if bb["first"] != srow["first"]:
            fail("per-root rows misaligned")
        if bb["free_now"] != srow["free_now"] or bb["uncovered"] != srow["uncovered"] \
                or bb["individual_greedy_union"] != srow["individual_greedy_union"]:
            prc_delta[srow["first"]] = {
                "free": [int(bb["free_now"]), int(srow["free_now"])],
                "uncovered": [int(bb["uncovered"]), int(srow["uncovered"])],
                "greedy": [int(bb["individual_greedy_union"]), int(srow["individual_greedy_union"])],
            }
    if prc_delta != PER_ROOT_COVERAGE_DELTA:
        fail(f"per-root coverage delta {prc_delta} != the pinned re-selection churn")
    for root, d in prc_delta.items():
        if d["free"][0] != d["free"][1] or d["uncovered"][0] != d["uncovered"][1]:
            fail(f"root {root} free/uncovered thirds changed although no class was freed")
    root27 = [srow for bb, srow in prc_pairs if srow["first"] == "27"][0]
    if root27["free_now"] != "119" or root27["uncovered"] != "0":
        fail("root 27 coverage regressed")
    rb_pr, rs_pr = rb["per_root_remaining"], rs["per_root_remaining"]
    deltas = {k: rs_pr[k] - rb_pr[k] for k in rb_pr if rs_pr[k] != rb_pr[k]}
    if deltas != PER_ROOT_REMAINING_DELTA:
        fail(f"per-root remaining delta {deltas} != pinned")
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

    # --- closure-classes table diff -------------------------------------------
    def read_closure(p: Path):
        return {int(r["class_index"]): r for r in csv.DictReader(p.open())}

    cb_t = read_closure(BASE_OUT / "closure-classes.csv")
    cs_t = read_closure(EXP / "reaudit/output/closure-classes.csv")
    if len(cb_t) != CLOSURE_ROWS_BEFORE or len(cs_t) != CLOSURE_ROWS_AFTER:
        fail(f"closure table row counts {len(cb_t)}/{len(cs_t)} != 807/807")
    left = sorted(set(cb_t) - set(cs_t))
    entered = sorted(set(cs_t) - set(cb_t))
    if left != CLOSURE_LEFT or entered != CLOSURE_ENTERED:
        fail(f"closure table left/entered must be EMPTY: {left} / {entered}")
    for col, want in CLASS_30484_ROW_BEFORE.items():
        if cb_t[CLASS_30484][col] != want:
            fail(f"base class-30484 row {col} drift: {cb_t[CLASS_30484][col]} != {want}")
    for col, want in CLASS_30484_ROW_AFTER.items():
        if cs_t[CLASS_30484][col] != want:
            fail(f"scenario class-30484 row {col} drift: {cs_t[CLASS_30484][col]} != {want}")
    if int(cb_t[CLASS_30484]["unknown_now"]) - int(cs_t[CLASS_30484]["unknown_now"]) != len(own):
        fail("class-30484 unknown delta != its own adopted children (Board boundary)")
    if cb_t[CLASS_30118] != cs_t[CLASS_30118]:
        fail("class-30118 closure row must be byte-identical before/after (not EL-owned)")
    if cb_t[CLASS_16371] != cs_t[CLASS_16371]:
        fail("class-16371 closure row must be byte-identical before/after (not EL-owned)")
    changed, rank_churn, stable, gs_dec = [], 0, 0, []
    rank_churn_classes = []
    for ci, brow in sorted(cb_t.items()):
        if ci in (CLASS_30484,) or ci not in cs_t:
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
            gs_dec.append({"class_index": ci,
                           "class_rank": [int(diff["class_rank"][0]), int(diff["class_rank"][1])],
                           "groups_served_count": [int(diff["groups_served_count"][0]),
                                                    int(diff["groups_served_count"][1])],
                           "unknown_now": [int(brow["unknown_now"]), int(srow["unknown_now"])]})
            continue
        if "unknown_now" not in diff:
            fail(f"class {ci} changed unexpected columns: {diff}")
        b_unk, s_unk = int(diff["unknown_now"][0]), int(diff["unknown_now"][1])
        clo, chi = s4_masks[ci]
        kids = {(c & ((1 << 64) - 1), c >> 64) for c in board.children(clo | (chi << 64))}
        own_c = len(kids & set(incr))
        if (b_unk - s_unk) != own_c or own_c == 0:
            fail(f"class {ci} unknown delta {b_unk}->{s_unk} != own adopted membership {own_c}")
        changed.append({"class_index": ci, "unknown_before": b_unk,
                        "unknown_after": s_unk, "own_adopted": own_c})
    if changed != CHANGED_CLASS_SET:
        fail(f"changed-class set must be EMPTY beside the dedicated 30484 sections: {changed}")
    if rank_churn_classes != RANK_CHURN_DETAIL:
        fail(f"rank-churn-only rows != the pinned 2-row churn detail: {rank_churn_classes}")
    if rank_churn != RANK_CHURN_ROWS or stable != FULLY_STABLE_ROWS:
        fail(f"rank churn {rank_churn}/stable {stable} != pinned {RANK_CHURN_ROWS}/{FULLY_STABLE_ROWS}")
    if gs_dec != GS_CHURN_DECREASE:
        fail(f"groups_served_count churn set != the pinned empty churn: {gs_dec}")
    scen_first = scen_summary["closure_classes_first"]
    c30484 = [e for e in scen_first if e["class_index"] == CLASS_30484]
    if len(c30484) != 1 or c30484[0]["unknown_now"] != 5 or len(c30484[0]["groups_served"]) != 4:
        fail("scenario closure_classes_first entry for class 30484 drift (rank-7 / 5-unknown / 4-group)")

    # --- emit decomp -------------------------------------------------------
    out = {
        "schema": "ek-aj039loss1-adoption-decomp-deltas-v1",
        "scenario": "ADOPTED-CANONICAL",
        "packet": {
            "batches": [{"pool": "ek-aj039loss1", "class_index": 30484,
                         "probed_rows": 2, "adopted_loss_rows": 1,
                         "unadopted_win_rows": 1, "anchor_rows": 3,
                         "adopted_nodes_per_pool": ADOPTED_TOTAL_NODES,
                         "whole_packet_nodes": WHOLE_PACKET_NODES}],
            "adopted_loss_rows": ADOPTED_ROWS,
            "unadopted_win_rows": 1,
            "claim_reserved_untouched": 2,
            "adopted_total_nodes_per_pass": ADOPTED_TOTAL_NODES,
            "whole_packet_nodes_per_pass": WHOLE_PACKET_NODES,
            "adopted_loss_ids": ADOPTED_IDS,
            "decisive_labels": "1 fresh LOSS @30M order 0 adopted (Part EK aj030/aj039 "
                               "30M re-probe, two-pass fresh-cold node-exact, MISMATCH 0, "
                               "resolved in (15M,30M] beyond the honest EXHAUSTED 15M "
                               "history - not a same-condition re-probe); the probe-level "
                               "WIN row aj030 (15,284,699, WIN-HALT) is unconsumed "
                               "(scrutiny-owner C++ gate 9193f5b6 exclusive) and sits in "
                               "NO cache; the 2 claim-reserved dual-class batch-38 keys "
                               "ai044/ai048 untouched (Part EF in-flight owner); the "
                               "batch-39 WINs aj049/aj050 stay unconsumed",
        },
        "cache": {
            "base_sha256": BASE_CACHE_SHA, "scenario_sha256": SCEN_CACHE_SHA,
            "base_rows": len(base), "scenario_rows": len(scen), "increment_rows": len(incr),
            "verdict_counts": {"WIN": 158, "LOSS": 6555},
            "relation": "scenario == base rows + the 1 increment row verbatim (no other row changed)",
            "merge_audit_runs": 3, "merge_audit_sha256_each": MERGE_AUDIT_SHA,
            "adopted_s5_indices": [ADOPTED_S5],
            "naming_note": "chain name merged-exact-s5-chain-plus-aj039loss1-20261125.cache "
                           "(short-form convention; the sha pin carries the identity)",
        },
        "class_30484": {
            "children_total_raw": len(child_keys), "non_s5_children": 0,
            "unknown_before": 6, "unknown_after": 5,
            "adopted_own": 1,
            "unconsumed_win_children": 3,
            "claim_reserved_children": 2,
            "base_known_loss_children": 48, "receipt_known_loss_children": 0,
            "status_before": "unknown", "status_after": "unknown",
            "class_rank": [9, 7],
            "groups_served_count": [4, 4],
            "unknown_s5_remaining": UNKNOWN_S5_REMAINING,
            "unknown_s5_remaining_ids": {"aj030": 892576, "ai044": 900354,
                                          "ai048": 900718, "aj049": 902511,
                                          "aj050": 902512},
            "not_a_root_verdict": "the loss-only adoption of the 1 row frees nothing and "
                                  "excludes nothing; free_now/coverage quantities are "
                                  "Board-derived scheduling bookkeeping; no root verdict and "
                                  "no coverage claim is made",
        },
        "class_30118": {
            "status": "byte-static across Part EL: the adopted aj039 sits OUTSIDE its "
                      "56-child Board boundary; closure row byte-identical, unknown 52 "
                      "/ rank 21 unchanged",
        },
        "class_16371": {"status": "byte-static across Part EL (not EL-owned; closure row "
                                   "byte-identical, no adopted key inside its Board boundary)"},
        "class_20421": {"status": "rank-churn-only across Part EL (8 -> 9; unknown_now "
                                   "static; no adopted key inside its Board boundary)"},
        "class_34908": {"status": "rank-churn-only across Part EL (7 -> 8; unknown_now "
                                   "static; no adopted key inside its Board boundary)"},
        "closure_table": {
            "rows_before": CLOSURE_ROWS_BEFORE, "rows_after": CLOSURE_ROWS_AFTER,
            "left": left, "entered": entered,
            "left_reason": "EMPTY: the 807-row frontier table is fully static across this "
                           "Part (no left/entered exchange)",
            "unknown_changed_classes": changed,
            "rank_churn_only_rows": rank_churn,
            "rank_churn_detail": [{"class_index": ci, "from": f, "to": t}
                                  for ci, f, t in rank_churn_classes],
            "groups_served_decrease_churn": gs_dec,
            "fully_stable_rows": stable,
        },
        "update8": {
            "resolved_before": UPD8_RESOLVED_BEFORE, "resolved_after": UPD8_RESOLVED_AFTER,
            "newly_resolved_s5": [],
            "newly_resolved_within_adopted": False,
            "note": "the adopted aj039 s5 index 897668 sits OUTSIDE the frozen update8 "
                    "baseline requirement: resolved, remaining and every per-root "
                    "remaining are BYTE-STATIC",
            "remaining_before": UPD8_REMAINING_BEFORE, "remaining_after": UPD8_REMAINING_AFTER,
            "groups_free_now_static": 131,
        },
        "class_status_counts_before": cb,
        "class_status_counts_after": cs,
        "metrics": {
            "joint_greedy_union_size": [JOINT_GREEDY_BEFORE, JOINT_GREEDY_AFTER],
            "worklist_total": [WORKLIST_BEFORE, WORKLIST_AFTER],
            "known_universe_indices": [KNOWN_UNIVERSE_BEFORE, KNOWN_UNIVERSE_AFTER],
            "cache_rows_in_universe": [CACHE_IN_UNIVERSE_BEFORE, CACHE_IN_UNIVERSE_AFTER],
            "unique_groups": [UNIQUE_GROUPS_BEFORE, UNIQUE_GROUPS_AFTER],
            "per_root_remaining_delta": PER_ROOT_REMAINING_DELTA,
            "per_root_coverage_delta": PER_ROOT_COVERAGE_DELTA,
            "note": "the joint greedy union stays 36,505 (the single adoption does not "
                    "move the greedy choice) and the worklist shrinks by exactly 1 "
                    "(64,366 -> 64,365) with class 30484's frontier cost 6 -> 5; "
                    "per-root free/uncovered thirds are IDENTICAL at every root "
                    "(nothing was freed); root 24's individual greedy union shifts "
                    "2,782 -> 2,781 as pure bookkeeping; root 27 stays 119/119",
        },
        "verification": {
            "kit_files_verified": {"ek": kit_files},
            "packet_pins": {"status_log": EK_STATUS_SHA, "audit_ek_json": EK_AUDIT_JSON_SHA,
                            "ek_manifest": EK_MANIFEST_SHA},
            "refresh_scripts_reexecuted": [BASE_REFRESH_SHA, SCEN_REFRESH_SHA],
            "refresh_outputs_byte_identical": True,
            "board_child_regeneration": "class-30484 54-child / class-30118 56-child / "
                                        "class-16371 52-child / class-20421 50-child / "
                                        "class-34908 56-child boundaries regenerated via "
                                        "Board(11).children",
        },
        "interpretation_guard":
            "only the fresh Part EK exact-LOSS row aj039 (two-pass fresh-cold node-exact "
            "at the pre-declared 30M condition, resolved in (15M,30M] beyond the honest "
            "EXHAUSTED 15M history - not a same-condition re-probe) is consumed into the "
            "canonical cache by this Part; the probe-level WIN rows (aj030 of this pool "
            "and aj049/aj050 of batch-39) are consumed NOWHERE (WIN adoption is "
            "scrutiny-owner C++ second-implementation gate pin 9193f5b6 exclusive) and "
            "their keys sit in NO cache; the 2 claim-reserved dual-class batch-38 keys "
            "(ai044/ai048) are the Part EF in-flight owner and untouched; class 30484 "
            "(5 children remaining: 1 probe-level WIN aj030, 2 claim-reserved, 2 "
            "unconsumed WINs aj049/aj050) is NOT freed and NOT excluded; classes "
            "30118/16371 are byte-static and 20421/34908 rank-churn-only; class status "
            "stays unknown, free_now 39 static, closure table 807 rows static with NO "
            "left/entered exchange, the 2 rank-churn-only rows being pure bookkeeping; "
            "no root verdict and no coverage claim is made anywhere; the per-root/"
            "greedy/worklist quantities quoted here are bookkeeping, never verdicts; no "
            "update8 resolution changed (aj039 sits outside the frozen baseline "
            "requirement); 11x11 stays UNKNOWN",
    }
    (EXP / "output/decomp-deltas-aj039loss1-adoption.json").write_text(
        json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("DECOMP OK changed=%d rank_churn=%d gs_dec=%d stable=%d left=%d entered=%d" % (
        len(changed), rank_churn, len(gs_dec), stable, len(left), len(entered)))
    print("class30484: unknown 6 -> 5 (1 adopted; 1 unconsumed WIN aj030 + 2 reserved + 2 unconsumed WINs remain), NOT freed, rank 9 -> 7")
    print("30118/16371: byte-static; 20421/34908: rank-churn-only")


if __name__ == "__main__":
    main()
