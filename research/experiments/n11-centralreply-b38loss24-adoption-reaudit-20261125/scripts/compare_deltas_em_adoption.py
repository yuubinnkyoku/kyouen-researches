"""BASE (canonical chain through the Part EL aj039loss1 adoption)
vs SCENARIO (em-b38loss24 = Part EM loss-only batch-38 adoption).

Fail-closed machine recomputation of exactly what the Part EM loss-only
canonical adoption changed, from published bytes only:

* every published artifact sha-pinned (the published Part EL outputs -- the
  BASE canonical cache cf08e181... 6,713 rows WIN 158 / LOSS 6,555, the BASE
  reaudit outputs refresh-summary 4579a021... / closure-classes 880e1c37...
  / per-root-coverage bafc7b66... / probe-worklist regen pin ed289920... --
  the Part EM outputs -- increment 3c632661... (24 s5verdict exact-LOSS
  rows), increments manifest ac5649f8... (schema
  em-b38loss24-increments-manifest-v1), the 6,737-row scenario cache
  b5be64e6... WIN 158 / LOSS 6,579 (chain name
  merged-exact-s5-chain-plus-b38loss24-20261125.cache; the sha pin carries
  the identity), the merge-audits x3 (identical sha 4a877e17...), the
  byte-clones of the union merger 90711961... and both refresh forks (the
  published Part EL refresh c0debd18... and the published Part EM refresh
  baf9cbde...), the frozen graph/update8/board/policy/quarantine pins);
* the published Part EL refresh fork and the published Part EM refresh fork
  are RE-EXECUTED byte-verbatim in isolated scratch trees against their
  pinned inputs, and all eight outputs must be byte-identical to the
  published / regenerated pins before any delta is emitted (double-run
  determinism; this simultaneously re-proves the published Part EL reaudit
  outputs are regenerable from published bytes);
* the complete published Part EF batch-38 kit (181 files, MANIFEST
  4dbf8856...) is sha-verified file-by-file; its machine audit
  batch-audit.json 73652099... (schema n11-centralreply-closure-batch38-
  audit-v1) must report verdicts_consumed_into_canonical_cache false with
  24 LOSS / 19 WIN / 6 EXHAUSTED / MISMATCH 0 over the class-30345 target;
  every one of the 49 batch-38 keys is then re-verified from its two raw
  replay outputs (exactly one replay row each, '# replay_done' completeness
  guard, two-pass fresh-cold node-exact p1==p2, budget 15,000,000 order 0,
  stones 5, is_or 0, key/lo/hi/legal vs the sha-pinned batch-keys SSOT
  29807104...) against the manifest decomposition (adopted_table /
  unadopted_win_rows / exhausted_honest_unknown_rows); the 7 reported
  p2-truncation retry artifacts are the ONLY non-complete raw files and are
  accounted for by the audit;
* SCEN cache == BASE cache rows + exactly the 24 increment rows (verdict
  agreement everywhere; 6,737 rows, WIN 158 / LOSS 6,579); the adopted rows
  are ALL fresh exact-LOSS rows of the published Part EF batch-38 kit
  (ai001,004,008,009,011,012,015,016,018,019,020,021,022,025,026,027,029,
  031,032,033,037,042,044,045, adopted node total per pass 168,055,078,
  adopted-table digest a56b1cde...); the 19 batch-38 probe-level WIN rows
  (incl. ai048, the class-30484 dual-class sibling of the adopted ai044) and
  the 6 honest-EXHAUSTED keys are consumed NOWHERE (WIN canonical adoption
  is scrutiny-owner C++ second-implementation gate 9193f5b6...
  exclusive); the excluded prior batch-1 dual-class key b018 sits in NO
  cache; aj030 / aj049 / aj050 (Part EK/batch-39 probe-level WINs) sit in NO
  cache;
* the class-30484 arithmetic is recomputed from the frozen dependency graph
  with the integer-geometry Board: the 54-child canonical boundary is
  regenerated (entirely inside the s5 mask universe; ZERO non-s5 children;
  ZERO update8-receipt children); 49 children are known exact LOSS in BASE
  and exactly 5 are unknown in BASE and exactly 4 in SCEN == the pinned 4
  remaining unknown s5 keys {892576 aj030 probe-level WIN unconsumed,
  900718 ai048 probe-level WIN unconsumed, 902511 aj049 probe-level WIN
  unconsumed, 902512 aj050 probe-level WIN unconsumed}; the adopted ai044
  (s5 900354) is the ONLY adopted member and sits inside this boundary;
  class 30484 is NOT freed and NOT excluded (unknown 5 -> 4, rank 7 ->
  7, groups_served_count 4 static);
* the class-30345 arithmetic is recomputed the same way: the 51-child
  boundary (1 non-s5 child; 50 in-universe children) held ZERO known children
  in BASE and exactly 26 unknown in SCEN; all 24 adopted keys sit inside
  this boundary (unknown 50 -> 26, rank 13 -> 11, groups_served_count 4
  static); the class is NOT freed and NOT excluded;
* the class-30118 arithmetic is recomputed the same way: the 56-child
  boundary (all in-universe) holds exactly ONE adopted member (ai033;
  unknown 52 -> 51, rank 21 -> 17, groups_served_count 4 static); the
  in-flight Part EJ batch-40 owner of this class is untouched by this
  recomputation;
* witness classes 16371 / 20421 / 34908 are proven BYTE-STATIC across this
  Part (closure rows byte-identical before/after; ZERO adopted members
  inside their Board boundaries);
* every closure-classes.csv row is compared: ZERO unknown_now changes beside
  classes 30484/30345/30118; ZERO left/entered rows; exactly 6
  rank-churn-only rows (1518, 2634, 5343, 8106, 8785, 13342 each +1) and
  ZERO groups_served churn (798 fully stable rows);
* update8 refresh: ALL 24 adopted s5 indices sit OUTSIDE the frozen update8
  baseline requirement: resolved stays 259, remaining stays 31,600,
  groups_free_now stays 131, the newly-resolved/lost sets are both EMPTY,
  win_hit_groups stays [] and every per-root remaining is byte-identical;
* class_status counts: excluded 390 / excluded_now 23 / free_now 39 /
  unknown 34,497 IDENTICAL before and after (the loss-only adoption frees
  nothing and excludes nothing); Board verification 39/39 with zero
  rejections on both sides; root 27 stays 119/119;
* per-root coverage: free/uncovered thirds are IDENTICAL at every root; the
  individual greedy union changes only at 6 roots (0: 3001->3000,
  1: 6352->6351, 2: 6129->6134, 12: 2890->2866, 24: 2781->2780,
  36: 2997->2975 -- pure re-selection bookkeeping, no coverage claim);
* the frozen greedy scheduler deltas are recorded as bookkeeping (joint
  greedy 36,505 -> 36,460, worklist 64,365 -> 64,339, known universe
  892 -> 916, cache in universe 869 -> 893).

No unknown verdict is asserted anywhere.  The standard 11x11 empty board
and every one of the 19 central-reply roots stay UNKNOWN; free_now /
coverage quantities are scheduling bookkeeping derived from exact LOSS
verdicts, not root verdict claims.  The 19 batch-38 probe-level WIN rows,
the 6 honest-EXHAUSTED keys, the excluded b018 key and the batch-39
probe-level WINs aj030/aj049/aj050 are consumed NOWHERE by this Part
(scrutiny-owner C++ second-implementation gate pin 9193f5b6...); no WIN
verdict and no EXHAUSTED verdict enters the canonical cache; 11x11 stays
UNKNOWN.
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

BASE_EXP = ROOT / "research/experiments/n11-centralreply-aj039loss1-adoption-reaudit-20261125"
BASE_OUT = BASE_EXP / "reaudit/output"
BASE_CACHE = BASE_EXP / "output/merged-exact-s5-chain-plus-aj039loss1-20261125.cache"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-b38loss24-20261125.cache"
INCR = EXP / "output/increment-b38loss24-20261125.cache"
MANIFEST = EXP / "output/increments-manifest.json"
EF_KIT = ROOT / "research/experiments/n11-centralreply-closure-class30345-batch38-20261125"
BATCH_KEYS = EF_KIT / "input/batch-keys-b38.json"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_REFRESH_SCRIPT = BASE_EXP / "reaudit/scripts/refresh_adoption_el.py"
SCEN_REFRESH_SCRIPT = EXP / "reaudit/scripts/refresh_adoption_em.py"
MERGER = EXP / "scripts/s5_union_merge.py"

BASE_CACHE_SHA = "cf08e1817a369853747706872763046c4544e289eae6d847bfd27d7503d23e7d"
SCEN_CACHE_SHA = "b5be64e6b96af435ab589caced29273bab765085ba13c3033e897de13fab636c"
INCR_SHA = "3c6326618944b4c18d37e1fe6cad470b53e712592fe7a19d7190f44f5a26bed4"
MANIFEST_SHA = "ac5649f809eeaf373a0b064f9f2bf8ad025e4b8e5bd9a89a49d3c7c095abf394"
BASE_SUMMARY_SHA = "4579a0217d0b71301605337513cf92e98d7656b7d8ceffcbe27f10b4efac8a3c"
BASE_CLOSURE_SHA = "880e1c373d1944f458fcb34d6d314b86a9b374cad5c704c4d95108a163355f10"
BASE_PRC_SHA = "bafc7b669a486ca8afa2305e09021e36a4cb0e5c5a8c888095464eb9b8cd7af8"
BASE_WORKLIST_SHA = "ed289920f527ee551c4c29bbf5cf012c7bddf0f4acca2fd3ddae4b919d7fad7c"
SCEN_SUMMARY_SHA = "bacf6a6848aa7cd857ed708f8bd908942d68f6d1b9068e6996cfd3cf41838f29"
SCEN_CLOSURE_SHA = "93a6889772544bb26d2c1542e1c1487787c1d05934ca9d3a18f1c969f24241f1"
SCEN_PRC_SHA = "bce9f8f1ac2a3c2caa3e7534041f6825263626fa03822f991521c6000e06838d"
SCEN_WORKLIST_SHA = "b4d16b7f21b0f0bc92e6a1022211327f6d3e153f015630f40e9e1f9315cee488"
BASE_REFRESH_SHA = "c0debd185919fb9791fa0f9ca07883d682429e536c8f31c65548047032ab02b1"
SCEN_REFRESH_SHA = "baf9cbde6aa49949eb5a9668134dd3d6cfad7aee057ad61ea0a631b686a0ef78"
MERGE_AUDIT_SHA = "4a877e17881e0aac0ca46a6aa4124b428ee69e45016320e2762c41adcb3c4ad8"
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
BOARD_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
ADOPTED_TABLE_DIGEST = "a56b1cdef65f0b311b1ae04e90023204f8bb85e9f0a3852f6007a0b42f9b12dc"

EF_MANIFEST_SHA = "4dbf8856597709b3bd41d6f185a0502ebbdee447b1fc48d0caab586fdcc5ac02"
EF_KIT_FILES = 181
EF_AUDIT_JSON_SHA = "73652099bcc47ac86b89a790524fb78c353e01c91ddcdc3748b91cfea5b75fdc"
EF_AUDIT_PY_SHA = "f07a162f44452a6a3a529cdb9c38f55a0f0009ed597393e9645326b7ac3d717a"
EF_STATUS_SHA = "8ca390768e317b5fdf810767dbd6e7bc31790d58762701e71759b4883fd8e14f"
EF_STATUS_LINES = 81
EF_BATCH_KEYS_SHA = "298071046bfba8473c5b3d6e0b6a30108697eb0899aed7c70fcb4c5343f7cb8d"

BUDGET = 15000000
ADOPTED_ROWS = 24
ADOPTED_TOTAL_NODES = 168055078
BATCH_TOTAL_NODES = 396892270
ADOPTED_IDS = ["ai001", "ai004", "ai008", "ai009", "ai011", "ai012", "ai015",
               "ai016", "ai018", "ai019", "ai020", "ai021", "ai022", "ai025",
               "ai026", "ai027", "ai029", "ai031", "ai032", "ai033", "ai037",
               "ai042", "ai044", "ai045"]
EXHAUSTED_IDS = ["ai007", "ai024", "ai030", "ai038", "ai040", "ai041"]
WIN_IDS_UNCONSUMED = ["ai002", "ai003", "ai005", "ai006", "ai010", "ai013",
                      "ai014", "ai017", "ai023", "ai028", "ai034", "ai035",
                      "ai036", "ai039", "ai043", "ai046", "ai047", "ai048",
                      "ai049"]
B018_KEY = (1153204079095189504, 65536)
B018_S5 = 528497
# Part EK / batch-39 probe-level WINs: consumed NOWHERE by any Part so far
UNCONSUMED_WIN_NO_CACHE = {
    "aj030": (1152922604135251976, 65536),
    "aj049": (1152921574400065536, 1114112),
    "aj050": (1152921574400065536, 68157440),
}
# class 30484 (dual-class owner of the adopted ai044)
BOUNDARY_30484_RAW = 54
BASE_KNOWN_LOSS_30484 = 49
UNKNOWN_BASE_30484 = 5
UNKNOWN_SCEN_30484 = 4
ADOPTED_S5_AI044 = 900354
UNKNOWN_S5_REMAINING = [892576, 900718, 902511, 902512]
# class 30345 (the batch-38 target)
BOUNDARY_30345_RAW = 51
NON_S5_30345 = 1
UNKNOWN_BASE_30345 = 50
UNKNOWN_SCEN_30345 = 26
OWN_30345 = 24
# class 30118 (in-flight Part EJ batch-40 owner; exactly one adopted member)
BOUNDARY_30118_RAW = 56
UNKNOWN_BASE_30118 = 52
UNKNOWN_SCEN_30118 = 51
OWN_30118 = 1
OWN_30118_ID = "ai033"
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
JOINT_GREEDY_AFTER = 36460
WORKLIST_BEFORE = 64365
WORKLIST_AFTER = 64339
KNOWN_UNIVERSE_BEFORE = 892
KNOWN_UNIVERSE_AFTER = 916
CACHE_IN_UNIVERSE_BEFORE = 869
CACHE_IN_UNIVERSE_AFTER = 893
CACHE_VERDICTS_BEFORE = {"1": 158, "2": 6555}
CACHE_VERDICTS_AFTER = {"1": 158, "2": 6579}
UNIQUE_GROUPS_BEFORE = 2115
UNIQUE_GROUPS_AFTER = 2115
GROUP_BEST_NONFREE = 2115
PER_ROOT_REMAINING_DELTA = {}
PER_ROOT_COVERAGE_DELTA = {
    "0": {"free": [7, 7], "uncovered": [112, 112], "greedy": [3001, 3000]},
    "1": {"free": [4, 4], "uncovered": [115, 115], "greedy": [6352, 6351]},
    "2": {"free": [8, 8], "uncovered": [111, 111], "greedy": [6129, 6134]},
    "12": {"free": [6, 6], "uncovered": [113, 113], "greedy": [2890, 2866]},
    "24": {"free": [12, 12], "uncovered": [107, 107], "greedy": [2781, 2780]},
    "36": {"free": [4, 4], "uncovered": [115, 115], "greedy": [2997, 2975]},
}
CLOSURE_ROWS_BEFORE = 807
CLOSURE_ROWS_AFTER = 807
CLOSURE_LEFT = []
CLOSURE_ENTERED = []
CLASS_30484_ROW_BEFORE = {"class_rank": "7", "unknown_now": "5", "groups_served_count": "4"}
CLASS_30484_ROW_AFTER = {"class_rank": "7", "unknown_now": "4", "groups_served_count": "4"}
CLASS_30345_ROW_BEFORE = {"class_rank": "13", "unknown_now": "50", "groups_served_count": "4"}
CLASS_30345_ROW_AFTER = {"class_rank": "11", "unknown_now": "26", "groups_served_count": "4"}
CLASS_30118_ROW_BEFORE = {"class_rank": "21", "unknown_now": "52", "groups_served_count": "4"}
CLASS_30118_ROW_AFTER = {"class_rank": "17", "unknown_now": "51", "groups_served_count": "4"}
RANK_CHURN_DETAIL = [(1518, 19, 20), (2634, 17, 18), (5343, 11, 12),
                     (8106, 20, 21), (8785, 18, 19), (13342, 12, 13)]
GS_CHURN_DECREASE = []
RANK_CHURN_ROWS = 6
FULLY_STABLE_ROWS = 798
# the three dedicated classes (30484/30345/30118) are excluded from the
# generic changed-class loop; the generic set must stay EMPTY
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


def verify_ef_kit():
    if sha(EF_KIT / "MANIFEST-sha256.txt") != EF_MANIFEST_SHA:
        fail("Part EF kit MANIFEST sha drift")
    n = 0
    for line in (EF_KIT / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split()
        want, rel, want_size = fields[0], fields[2], int(fields[1])
        if rel.startswith("/") or ".." in rel.split("/"):
            fail(f"Part EF MANIFEST unsafe path: {rel}")
        p = EF_KIT / rel
        if not p.is_file():
            fail(f"Part EF kit file missing: {rel}")
        if sha(p) != want:
            fail(f"Part EF kit sha drift at {rel}")
        if p.stat().st_size != want_size:
            fail(f"Part EF kit size drift at {rel}: {p.stat().st_size} != {want_size}")
        n += 1
    if n != EF_KIT_FILES:
        fail(f"Part EF kit files {n} != {EF_KIT_FILES}")
    if sha(EF_KIT / "output/batch-audit.json") != EF_AUDIT_JSON_SHA:
        fail("batch-audit.json sha drift in the Part EF kit")
    if sha(EF_KIT / "scripts/audit_b38.py") != EF_AUDIT_PY_SHA:
        fail("audit_b38.py sha drift in the Part EF kit")
    if sha(EF_KIT / "output/status.log") != EF_STATUS_SHA:
        fail("status.log sha drift in the Part EF kit")
    if len((EF_KIT / "output/status.log").read_text().splitlines()) != EF_STATUS_LINES:
        fail(f"status.log line count drift (expected {EF_STATUS_LINES})")
    return n


def replay_row(raw_dir: Path, kid: str, tag: str, raw_pins: dict):
    p = raw_dir / f"{kid}.{tag}.out"
    if raw_pins is not None:
        fid = f"{kid}.{tag}.out"
        if fid not in raw_pins:
            fail(f"manifest raw_file_sha256_pins lacks the adopted raw {fid}")
        if sha(p) != raw_pins[fid]:
            fail(f"raw replay sha drift vs the pinned published bytes: {fid}")
    row = None
    seen = 0
    text = p.read_text()
    for line in text.splitlines():
        if line.startswith("replay,"):
            parts = line.split(",")
            seen += 1
            row = {"stones": int(parts[2]), "legal": int(parts[3]),
                   "is_or": int(parts[4]), "budget": int(parts[5]),
                   "result": int(parts[6]), "nodes": int(parts[7]),
                   "lo": parts[9], "hi": parts[10]}
    if seen != 1 or row is None:
        fail(f"expected exactly one replay row in {p}")
    if "# replay_done" not in text:
        fail(f"raw {kid}.{tag}.out lacks the '# replay_done' completeness guard")
    return row


def two_pass_raw(raw_dir: Path, kid: str, raw_pins):
    rows = {}
    for tag in ("p1", "p2"):
        rows[tag] = replay_row(raw_dir, kid, tag, raw_pins)
    ref = rows["p1"]
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
    for tag, r in rows.items():
        if tuple(r[f] for f in fields) != tuple(ref[f] for f in fields):
            fail(f"two-pass raw disagreement (fresh-cold node-exact gate): {kid}.{tag}")
    if ref["budget"] != BUDGET:
        fail(f"{kid}: raw budget drift (expected {BUDGET})")
    return ref


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
        ("ef kit batch-keys SSOT", BATCH_KEYS, EF_BATCH_KEYS_SHA),
        ("ef kit audit", EF_KIT / "output/batch-audit.json", EF_AUDIT_JSON_SHA),
        ("ef kit status", EF_KIT / "output/status.log", EF_STATUS_SHA),
    ]
    for name, p, want in pins:
        got = sha(p)
        if got != want:
            fail(f"{name} sha drift: {got} != {want}")
    kit_files = verify_ef_kit()

    # --- Part EF kit audit honesty pins --------------------------------------
    audit = json.loads((EF_KIT / "output/batch-audit.json").read_text())
    if audit["schema"] != "n11-centralreply-closure-batch38-audit-v1":
        fail("Part EF audit schema drift")
    if audit["class_index"] != 30345 or audit["batch"] != "batch-38":
        fail("Part EF audit class/batch drift")
    if audit["verdicts_consumed_into_canonical_cache"] is not False:
        fail("Part EF audit verdicts_consumed_into_canonical_cache must be false")
    if audit["target_key_count"] != 49:
        fail("Part EF audit target_key_count must be 49")
    res = audit["results"]
    if (res["LOSS"], res["WIN"], res["EXHAUSTED"], res["MISMATCH"]) != (24, 19, 6, 0):
        fail("Part EF audit 24/19/6/0 results accounting drift")
    if res["total_nodes_all_keys_single_pass"] != BATCH_TOTAL_NODES:
        fail("Part EF audit batch total node drift")
    if sorted(res["exhausted_keys_honest_unknown"]) != sorted(EXHAUSTED_IDS):
        fail("Part EF audit exhausted key set drift")
    if sorted(res["win_keys_unconsumed"]) != sorted(WIN_IDS_UNCONSUMED):
        fail("Part EF audit unconsumed WIN key set drift")
    if "9193f5b6" not in res["win_note"]:
        fail("Part EF audit win_note must pin the scrutiny-owner C++ gate 9193f5b6")
    if audit["truncation_retries_status_lines"] != 7 or \
            audit["reported_truncation_artifacts"] != res.get("reported_truncation_artifacts", audit["reported_truncation_artifacts"]):
        fail("Part EF audit truncation retry accounting drift")
    if len(audit["reported_truncation_artifacts"]) != 7:
        fail("Part EF audit must account for exactly 7 reported truncation artifacts")

    raw_extra = sorted(q.name for q in (EF_KIT / "output/raw").iterdir()
                       if "# replay_done" not in q.read_text())
    if raw_extra != sorted(audit["reported_truncation_artifacts"]):
        fail(f"the ONLY non-complete raw files must be the 7 reported truncation artifacts: {raw_extra}")

    # --- batch-keys SSOT ------------------------------------------------------
    bkeys = json.loads(BATCH_KEYS.read_text())
    key_by_id = {k["key_id"]: k for k in bkeys["keys"]}
    if len(key_by_id) != 49 or sorted(key_by_id) != sorted(
            ADOPTED_IDS + EXHAUSTED_IDS + WIN_IDS_UNCONSUMED):
        fail("batch-keys SSOT must hold exactly the 49 batch-38 keys")
    if bkeys.get("schema") is None or bkeys.get("consumed_into_canonical_cache") is not False:
        fail("batch-keys SSOT schema / consumed flag drift")
    if key_by_id["ai044"]["s5_index"] != ADOPTED_S5_AI044:
        fail("ai044 s5 index drift in the batch-keys SSOT")
    if key_by_id["ai048"]["s5_index"] != 900718:
        fail("ai048 s5 index drift in the batch-keys SSOT")

    # --- manifest decomposition ----------------------------------------------
    manifest = json.loads(MANIFEST.read_text())
    if manifest["schema"] != "em-b38loss24-increments-manifest-v1":
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
        fail("manifest adopted_table must hold 24 rows")
    if sum(r["nodes"] for r in manifest["adopted_table"]) != ADOPTED_TOTAL_NODES:
        fail("manifest adopted_table node sum drift")
    if manifest["base_cache_rows"] != 6713:
        fail("manifest base rows drift")
    if manifest["base_cache_absent_hits_for_emitted"] != 0:
        fail("manifest emitted rows must be absent from BASE")
    if manifest["quarantine_hits"] != 0:
        fail("manifest quarantine hits must be 0")
    if manifest["row_counts"] != {"adopted_loss_rows": 24,
                                  "excluded_prior_win": 1,
                                  "exhausted_honest_unknown": 6,
                                  "prior_canonical_rows_base": 6713,
                                  "wins_unconsumed_this_pool": 19}:
        fail("manifest row_counts drift")
    if manifest["loss_ids"] != ADOPTED_IDS or manifest["resolved_ids"] != ADOPTED_IDS:
        fail("manifest loss/resolved id sets drift")
    if manifest["win_ids"] != WIN_IDS_UNCONSUMED or \
            manifest["unadopted_win_ids"] != WIN_IDS_UNCONSUMED:
        fail("manifest unconsumed WIN id sets drift")
    if manifest["full_packet_eq_loss_only"] is not False:
        fail("manifest full_packet_eq_loss_only must be false (packet spans 24L/19W/6E)")
    if manifest["win_scenario_exists"] is not True:
        fail("manifest win_scenario_exists must be true (19 probe-level WIN rows in pool)")
    if manifest["provenance"]["audit_gates_all_pass"] is not True:
        fail("manifest provenance audit_gates_all_pass must be true")
    if manifest["provenance"]["ef_kit_files"] != EF_KIT_FILES or \
            manifest["provenance"]["status_lines"] != EF_STATUS_LINES:
        fail("manifest provenance kit/status accounting drift")
    if len(manifest["unadopted_win_rows"]) != 19:
        fail("manifest must hold 19 unconsumed WIN rows")
    if len(manifest["exhausted_honest_unknown_rows"]) != 6:
        fail("manifest must hold 6 honest-EXHAUSTED rows")
    if len(manifest["batches"]) != 1:
        fail("manifest must hold exactly one batch pool")
    b = manifest["batches"][0]
    if b["pool"] != "ef-b38loss24":
        fail("unexpected pool in the EM manifest")
    if b["adopted_loss_ids"] != ADOPTED_IDS:
        fail("pool adopted id set drift")
    if sorted(b["exhausted_honest_unknown_ids"]) != sorted(EXHAUSTED_IDS):
        fail("pool exhausted id set drift")
    if b["unadopted_win_ids"] != WIN_IDS_UNCONSUMED:
        fail("pool unconsumed WIN id set drift")
    if b["excluded_prior_ids"] != ["b018"]:
        fail("pool excluded prior id set drift")
    if b["adopted_nodes_per_pool"] != ADOPTED_TOTAL_NODES or \
            b["batch_total_nodes_per_pass"] != BATCH_TOTAL_NODES:
        fail("pool node accounting drift")
    if b["probed_budget"] != BUDGET:
        fail("pool budget pin drift (single 15M condition, no re-probe anywhere)")
    if b["status_log_lines"] != EF_STATUS_LINES or b["status_log_sha256"] != EF_STATUS_SHA:
        fail("pool status-log pin drift")
    ki_ = b["kit_integrity"]
    if ki_["kit_manifest_sha256"] != EF_MANIFEST_SHA or \
            ki_["kit_files_verified"] != EF_KIT_FILES:
        fail("pool kit integrity pins drift")
    if ki_["batch_keys_sha256"] != EF_BATCH_KEYS_SHA:
        fail("pool batch-keys SSOT pin drift")
    if ki_["audit_b38_json_sha256"] != EF_AUDIT_JSON_SHA or \
            ki_["audit_b38_py_sha256"] != EF_AUDIT_PY_SHA:
        fail("pool audit shas drift")
    if len(ki_["raw_file_sha256_pins"]) != 48 or \
            sorted(ki_["raw_file_sha256_pins"]) != sorted(
                f"{kid}.{tag}.out" for kid in ADOPTED_IDS for tag in ("p1", "p2")):
        fail("pool raw-file pin table must cover exactly the 48 adopted raws")
    if len(ki_["input_csv_sha256_pins"]) != 24 or \
            sorted(ki_["input_csv_sha256_pins"]) != sorted(ADOPTED_IDS):
        fail("pool input-csv pin table must cover exactly the 24 adopted keys")
    if (b["b018_prior_win_pin"]["lo"], b["b018_prior_win_pin"]["hi"]) != B018_KEY:
        fail("pool b018 pin key drift")
    if b["b018_prior_win_pin"]["s5_index"] != B018_S5:
        fail("pool b018 s5 index drift")

    # --- Part EF raws: ALL 49 keys two-pass fresh-cold node-exact ------------
    raw_pins = ki_["raw_file_sha256_pins"]
    adopted_tab = {(int(e["lo"]), int(e["hi"])): e for e in manifest["adopted_table"]}
    win_tab = {(int(e["lo"]), int(e["hi"])): e for e in manifest["unadopted_win_rows"]}
    exh_tab = {(int(e["lo"]), int(e["hi"])): e for e in manifest["exhausted_honest_unknown_rows"]}
    audit_by_id = {e["key_id"]: e for e in audit["per_key"]}
    for kid in ADOPTED_IDS + EXHAUSTED_IDS + WIN_IDS_UNCONSUMED:
        e = key_by_id[kid]
        ref = two_pass_raw(EF_KIT / "output/raw", kid,
                           raw_pins if kid in ADOPTED_IDS else None)
        if ref["stones"] != 5 or ref["is_or"] != 0:
            fail(f"{kid}: wrong depth/or bit")
        if ref["lo"] != str(e["lo"]) or ref["hi"] != str(e["hi"]) or \
                ref["legal"] != e["legal"]:
            fail(f"{kid}: raw key-field disagreement vs the batch-keys SSOT")
        key = (e["lo"], e["hi"])
        tab = adopted_tab.get(key) or win_tab.get(key) or exh_tab.get(key)
        if tab is None:
            fail(f"{kid}: key absent from the manifest decomposition tables")
        if (ref["result"], ref["nodes"]) != (tab["result"], tab["nodes"]):
            fail(f"{kid}: raw honest-label drift vs the manifest decomposition")
        ae = audit_by_id.get(kid)
        if ae is None or (ae["result"], ae["nodes"]) != (tab["result"], tab["nodes"]) \
                or ae["budget"] != BUDGET:
            fail(f"{kid}: batch-audit per-key label drift")
        if kid in ADOPTED_IDS:
            if tab["result"] != 2 or tab["legal"] != e["legal"]:
                fail(f"{kid}: adopted table LOSS/legal drift")
            p_in = EF_KIT / f"input/{kid}.input.csv"
            if sha(p_in) != ki_["input_csv_sha256_pins"][kid]:
                fail(f"input csv {kid} sha drift vs the pinned published bytes")
            want_line = f"target,0,5,{e['lo']},{e['hi']},{e['legal']},0,0,0,0,0"
            rows_in = [l for l in p_in.read_text().splitlines() if l.strip()]
            if rows_in != [want_line]:
                fail(f"input csv {kid} body drift: {rows_in}")
        elif kid in WIN_IDS_UNCONSUMED:
            if tab["result"] != 1:
                fail(f"{kid}: unconsumed WIN row result drift")
        else:
            if tab["result"] != 0 or tab["nodes"] != BUDGET:
                fail(f"{kid}: honest-EXHAUSTED row must be result 0 at the 15M budget")

    # --- refresh re-execution (double-run determinism) -----------------------
    base_tmp = rerun_refresh(BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA, ".emverify-base-el")
    scen_tmp = rerun_refresh(SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA, ".emverify-scen-em")
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
    shutil.rmtree(ROOT / "research/experiments/.emverify-base-el")
    shutil.rmtree(ROOT / "research/experiments/.emverify-scen-em")

    # --- cache relation: SCEN == BASE + exactly the 24 increment rows --------
    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    incr = load_cache(INCR)
    if len(base) != 6713 or len(scen) != 6737 or len(incr) != ADOPTED_ROWS:
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
    if (wins, losses) != (158, 6579):
        fail(f"scenario verdict counts {wins}/{losses} != 158/6,579")
    if set(incr) != set(adopted_tab):
        fail("increment key set != the manifest adopted_table key set")
    for key, row in incr.items():
        if row != (adopted_tab[key]["result"], adopted_tab[key]["nodes"]):
            fail(f"manifest adopted_table row != increment row: {key}")
    ai044_key = (key_by_id["ai044"]["lo"], key_by_id["ai044"]["hi"])
    if ai044_key not in incr or incr[ai044_key][0] != 2:
        fail("the class-30484 dual-class child ai044 must be adopted here as exact LOSS")
    for kid in WIN_IDS_UNCONSUMED:
        key = (key_by_id[kid]["lo"], key_by_id[kid]["hi"])
        if key in incr or key in base or key in scen:
            fail(f"the unconsumed WIN key {kid} must sit in NO cache (WIN scrutiny gate)")
    for kid in EXHAUSTED_IDS:
        key = (key_by_id[kid]["lo"], key_by_id[kid]["hi"])
        if key in incr or key in base or key in scen:
            fail(f"the honest-EXHAUSTED key {kid} must sit in NO cache")
    if B018_KEY in incr or B018_KEY in base or B018_KEY in scen:
        fail("the excluded prior batch-1 dual-class key b018 must sit in NO cache")
    for kid, key in UNCONSUMED_WIN_NO_CACHE.items():
        if key in incr or key in base or key in scen:
            fail(f"the unconsumed batch-39/EK WIN key {kid} must sit in NO cache")

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
    if mask_to_index[ai044_key] != ADOPTED_S5_AI044:
        fail("adopted ai044 s5 index != the pinned 900354")
    for key in incr:
        if key not in mask_to_index:
            fail(f"adopted key outside the s5 universe: {key}")
        if mask_to_index[key] in update8["required_new_s5"]:
            fail("an adopted s5 index sits inside the frozen update8 baseline requirement")
    if any(key in quarantined for key in incr):
        fail("a quarantined key sits inside the adopted increment")

    def boundary(cls):
        c_lo, c_hi = s4_masks[cls]
        return {(c & ((1 << 64) - 1), c >> 64) for c in board.children(c_lo | (c_hi << 64))}

    # --- class 30484 (the EL/EM dual-class owner) ---------------------------
    kids_30484 = boundary(30484)
    if len(kids_30484) != BOUNDARY_30484_RAW:
        fail(f"class-30484 Board child boundary {len(kids_30484)} != {BOUNDARY_30484_RAW}")
    if [k for k in kids_30484 if k not in mask_to_index]:
        fail("class-30484 boundary must have ZERO non-s5 children")
    if [k for k in kids_30484 if mask_to_index[k] in receipt_verdicts]:
        fail("class-30484 must have ZERO update8-receipt children")
    known_base_30484 = [k for k in kids_30484 if k in base]
    if len(known_base_30484) != BASE_KNOWN_LOSS_30484:
        fail(f"class-30484 BASE-known child count {len(known_base_30484)} != {BASE_KNOWN_LOSS_30484}")
    for k in known_base_30484:
        if base[k][0] != 2:
            fail("a BASE-known child of 30484 is not an exact LOSS")
    unknown_base_30484 = [k for k in kids_30484 if k not in base]
    if len(unknown_base_30484) != UNKNOWN_BASE_30484:
        fail(f"class-30484 BASE unknown {len(unknown_base_30484)} != {UNKNOWN_BASE_30484}")
    unknown_scen_30484 = [k for k in kids_30484 if k not in scen]
    if len(unknown_scen_30484) != UNKNOWN_SCEN_30484:
        fail(f"class-30484 SCEN unknown {len(unknown_scen_30484)} != {UNKNOWN_SCEN_30484} (NOT freed)")
    if sorted(mask_to_index[k] for k in unknown_scen_30484) != UNKNOWN_S5_REMAINING:
        fail("scenario unknown children of 30484 != the pinned 4 remaining s5 keys")
    own_30484 = set(kids_30484) & set(incr)
    if own_30484 != {ai044_key}:
        fail("class-30484 adopted-own set != exactly the adopted ai044 key")
    if any(k in quarantined for k in kids_30484):
        fail("a quarantined key sits inside the class-30484 child boundary")

    # --- class 30345 (the batch-38 target) -----------------------------------
    kids_30345 = boundary(30345)
    if len(kids_30345) != BOUNDARY_30345_RAW:
        fail(f"class-30345 Board child boundary {len(kids_30345)} != {BOUNDARY_30345_RAW}")
    non_s5_30345 = [k for k in kids_30345 if k not in mask_to_index]
    if len(non_s5_30345) != NON_S5_30345:
        fail(f"class-30345 boundary non-s5 child count drift ({len(non_s5_30345)})")
    unknown_base_30345 = [k for k in kids_30345 if k in mask_to_index and k not in base]
    if len(unknown_base_30345) != UNKNOWN_BASE_30345:
        fail(f"class-30345 BASE unknown {len(unknown_base_30345)} != {UNKNOWN_BASE_30345}")
    unknown_scen_30345 = [k for k in kids_30345 if k in mask_to_index and k not in scen]
    if len(unknown_scen_30345) != UNKNOWN_SCEN_30345:
        fail(f"class-30345 SCEN unknown {len(unknown_scen_30345)} != {UNKNOWN_SCEN_30345}")
    own_30345 = set(kids_30345) & set(incr)
    if len(own_30345) != OWN_30345:
        fail(f"class-30345 adopted membership {len(own_30345)} != {OWN_30345}")
    if [k for k in non_s5_30345 if k in incr]:
        fail("an adopted key claimed a non-s5 child slot of class-30345")
    ai045_key = (key_by_id["ai045"]["lo"], key_by_id["ai045"]["hi"])
    if ai045_key not in own_30345:
        fail("class-30345 membership must include ai045 (all 24 adopted rows)")

    # --- class 30118 (in-flight Part EJ batch-40 owner) ----------------------
    kids_30118 = boundary(30118)
    if len(kids_30118) != BOUNDARY_30118_RAW:
        fail(f"class-30118 Board child boundary {len(kids_30118)} != {BOUNDARY_30118_RAW}")
    if [k for k in kids_30118 if k not in mask_to_index]:
        fail("class-30118 boundary must have ZERO non-s5 children")
    own_30118 = set(kids_30118) & set(incr)
    if len(own_30118) != OWN_30118:
        fail(f"class-30118 adopted membership {len(own_30118)} != {OWN_30118}")
    ai033_key = (key_by_id["ai033"]["lo"], key_by_id["ai033"]["hi"])
    if own_30118 != {ai033_key}:
        fail("class-30118 adopted member != exactly ai033")
    unknown_base_30118 = [k for k in kids_30118 if k not in base]
    unknown_scen_30118 = [k for k in kids_30118 if k not in scen]
    if len(unknown_base_30118) != UNKNOWN_BASE_30118 or \
            len(unknown_scen_30118) != UNKNOWN_SCEN_30118:
        fail("class-30118 unknown counts drift vs pins (52 -> 51)")

    # --- byte-static witness classes -----------------------------------------
    for cls, raw in ((16371, BOUNDARY_16371_RAW),
                     (20421, BOUNDARY_20421_RAW),
                     (34908, BOUNDARY_34908_RAW)):
        kids = boundary(cls)
        if len(kids) != raw:
            fail(f"class-{cls} Board child boundary drift")
        if set(incr) & kids:
            fail(f"no adopted key may sit inside the class-{cls} boundary (byte-static witness)")
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
        fail("update8 newly-resolved/lost sets must BOTH be empty (all 24 sit outside)")
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
    if scen_summary["inputs"]["cache_rows"] != 6737 \
            or scen_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_AFTER \
            or scen_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_AFTER:
        fail("scenario inputs metrics drift")
    if base_summary["inputs"]["cache_rows_in_universe"] != CACHE_IN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["known_universe_indices"] != KNOWN_UNIVERSE_BEFORE \
            or base_summary["inputs"]["cache_rows"] != 6713:
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
    for cls, row_pins in ((30484, (CLASS_30484_ROW_BEFORE, CLASS_30484_ROW_AFTER)),
                          (30345, (CLASS_30345_ROW_BEFORE, CLASS_30345_ROW_AFTER)),
                          (30118, (CLASS_30118_ROW_BEFORE, CLASS_30118_ROW_AFTER))):
        before_pins, after_pins = row_pins
        for col, want in before_pins.items():
            if cb_t[cls][col] != want:
                fail(f"base class-{cls} row {col} drift: {cb_t[cls][col]} != {want}")
        for col, want in after_pins.items():
            if cs_t[cls][col] != want:
                fail(f"scenario class-{cls} row {col} drift: {cs_t[cls][col]} != {want}")
    if int(cb_t[30484]["unknown_now"]) - int(cs_t[30484]["unknown_now"]) != len(own_30484):
        fail("class-30484 unknown delta != its own adopted children (Board boundary)")
    if int(cb_t[30345]["unknown_now"]) - int(cs_t[30345]["unknown_now"]) != len(own_30345):
        fail("class-30345 unknown delta != its own adopted children (Board boundary)")
    if int(cb_t[30118]["unknown_now"]) - int(cs_t[30118]["unknown_now"]) != len(own_30118):
        fail("class-30118 unknown delta != its own adopted children (Board boundary)")
    for cls in (16371, 20421, 34908):
        if cb_t[cls] != cs_t[cls]:
            fail(f"class-{cls} closure row must be byte-identical before/after (witness)")
    changed, rank_churn, stable, gs_dec = [], 0, 0, []
    rank_churn_classes = []
    for ci, brow in sorted(cb_t.items()):
        if ci in (30484, 30345, 30118) or ci not in cs_t:
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
        kids = boundary(ci)
        own_c = len(kids & set(incr))
        if (b_unk - s_unk) != own_c or own_c == 0:
            fail(f"class {ci} unknown delta {b_unk}->{s_unk} != own adopted membership {own_c}")
        changed.append({"class_index": ci, "unknown_before": b_unk,
                        "unknown_after": s_unk, "own_adopted": own_c})
    if changed != CHANGED_CLASS_SET:
        fail(f"changed-class set must be EMPTY beside the dedicated "
             f"30484/30345/30118 sections: {changed}")
    if rank_churn_classes != RANK_CHURN_DETAIL:
        fail(f"rank-churn-only rows != the pinned 6-row churn detail: {rank_churn_classes}")
    if rank_churn != RANK_CHURN_ROWS or stable != FULLY_STABLE_ROWS:
        fail(f"rank churn {rank_churn}/stable {stable} != pinned {RANK_CHURN_ROWS}/{FULLY_STABLE_ROWS}")
    if gs_dec != GS_CHURN_DECREASE:
        fail(f"groups_served_count churn set != the pinned empty churn: {gs_dec}")
    scen_first = scen_summary["closure_classes_first"]
    c30484 = [e for e in scen_first if e["class_index"] == 30484]
    if len(c30484) != 1 or c30484[0]["unknown_now"] != 4 or len(c30484[0]["groups_served"]) != 4:
        fail("scenario closure_classes_first entry for class 30484 drift (rank-7 / 4-unknown / 4-group)")

    # --- emit decomp -------------------------------------------------------
    out = {
        "schema": "em-b38loss24-adoption-decomp-deltas-v1",
        "scenario": "ADOPTED-CANONICAL",
        "packet": {
            "batches": [{"pool": "ef-b38loss24", "class_index": 30345,
                         "probed_rows": 49, "adopted_loss_rows": 24,
                         "unadopted_win_rows": 19, "exhausted_honest_unknown_rows": 6,
                         "excluded_prior_win_rows": 1,
                         "adopted_nodes_per_pool": ADOPTED_TOTAL_NODES,
                         "batch_total_nodes_per_pass": BATCH_TOTAL_NODES}],
            "adopted_loss_rows": ADOPTED_ROWS,
            "unadopted_win_rows": 19,
            "exhausted_honest_unknown_rows": 6,
            "adopted_total_nodes_per_pass": ADOPTED_TOTAL_NODES,
            "batch_total_nodes_per_pass": BATCH_TOTAL_NODES,
            "adopted_loss_ids": ADOPTED_IDS,
            "decisive_labels": "24 fresh exact-LOSS rows of the published Part EF "
                              "batch-38 kit adopted (each a first-ever probe, two-pass "
                              "fresh-cold node-exact at the single 15M budget/order-0 "
                              "condition, solved within budget, MISMATCH 0, resolved by "
                              "its own single pass history - no re-probe, no exhaustion "
                              "conversion); the 19 probe-level WIN rows (incl. ai048 the "
                              "class-30484 dual-class sibling of the adopted ai044) are "
                              "unconsumed (scrutiny-owner C++ gate 9193f5b6 exclusive) "
                              "and sit in NO cache; the 6 honest-EXHAUSTED keys stay "
                              "honest UNKNOWN; b018 (prior batch-1 dual-class WIN) stays "
                              "excluded and unconsumed",
        },
        "cache": {
            "base_sha256": BASE_CACHE_SHA, "scenario_sha256": SCEN_CACHE_SHA,
            "base_rows": len(base), "scenario_rows": len(scen), "increment_rows": len(incr),
            "verdict_counts": {"WIN": 158, "LOSS": 6579},
            "relation": "scenario == base rows + the 24 increment rows verbatim (no other row changed)",
            "merge_audit_runs": 3, "merge_audit_sha256_each": MERGE_AUDIT_SHA,
            "adopted_s5_indices": sorted(mask_to_index[k] for k in incr),
            "naming_note": "chain name merged-exact-s5-chain-plus-b38loss24-20261125.cache "
                           "(short-form convention; the sha pin carries the identity)",
        },
        "class_30484": {
            "children_total_raw": len(kids_30484), "non_s5_children": 0,
            "unknown_before": 5, "unknown_after": 4,
            "adopted_own": 1, "adopted_own_id": "ai044",
            "unconsumed_win_children": 4,
            "base_known_loss_children": 49, "receipt_known_loss_children": 0,
            "status_before": "unknown", "status_after": "unknown",
            "class_rank": [7, 7],
            "groups_served_count": [4, 4],
            "unknown_s5_remaining": UNKNOWN_S5_REMAINING,
            "unknown_s5_remaining_ids": {"aj030": 892576, "ai048": 900718,
                                          "aj049": 902511, "aj050": 902512},
            "not_a_root_verdict": "the loss-only adoption of the 24 rows frees nothing "
                                  "and excludes nothing; free_now/coverage quantities are "
                                  "Board-derived scheduling bookkeeping; no root verdict "
                                  "and no coverage claim is made",
        },
        "class_30345": {
            "children_total_raw": len(kids_30345), "non_s5_children": NON_S5_30345,
            "unknown_before": 50, "unknown_after": 26,
            "adopted_own": OWN_30345,
            "status_before": "unknown", "status_after": "unknown",
            "class_rank": [13, 11],
            "groups_served_count": [4, 4],
            "note": "the batch-38 target class: all 24 adopted rows sit inside its "
                    "51-child Board boundary; NOT freed, NOT excluded (26 unknown "
                    "children remain)",
        },
        "class_30118": {
            "children_total_raw": len(kids_30118), "non_s5_children": 0,
            "unknown_before": 52, "unknown_after": 51,
            "adopted_own": OWN_30118, "adopted_own_id": OWN_30118_ID,
            "status_before": "unknown", "status_after": "unknown",
            "class_rank": [21, 17],
            "note": "exactly one adopted row (ai033) sits inside the in-flight Part EJ "
                    "batch-40 target class; recomputed here from the frozen graph, the "
                    "EJ owner lane is untouched",
        },
        "class_16371": {"status": "byte-static across Part EM (witness)"},
        "class_20421": {"status": "byte-static across Part EM (witness)"},
        "class_34908": {"status": "byte-static across Part EM (witness)"},
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
            "note": "ALL 24 adopted s5 indices sit OUTSIDE the frozen update8 baseline "
                    "requirement: resolved, remaining and every per-root remaining are "
                    "BYTE-STATIC",
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
            "note": "the joint greedy union moves 36,505 -> 36,460 and the worklist "
                    "shrinks 64,365 -> 64,339 with the class-30345 frontier cost 50 -> 26 "
                    "and class-30484's 5 -> 4; per-root free/uncovered thirds are "
                    "IDENTICAL at every root (nothing was freed); the 6 greedy shifts "
                    "(incl. root 2's 6,129 -> 6,134 re-selection increase) are pure "
                    "bookkeeping; root 27 stays 119/119",
        },
        "verification": {
            "kit_files_verified": {"ef": kit_files},
            "packet_pins": {"status_log": EF_STATUS_SHA, "audit_b38_json": EF_AUDIT_JSON_SHA,
                            "ef_manifest": EF_MANIFEST_SHA, "batch_keys": EF_BATCH_KEYS_SHA},
            "raws_two_pass_verified": 49,
            "truncation_retry_artifacts_accounted": 7,
            "refresh_scripts_reexecuted": [BASE_REFRESH_SHA, SCEN_REFRESH_SHA],
            "refresh_outputs_byte_identical": True,
            "board_child_regeneration": "class-30484 54-child / class-30345 51-child "
                                        "(1 non-s5) / class-30118 56-child / class-16371 "
                                        "52-child / class-20421 50-child / class-34908 "
                                        "56-child boundaries regenerated via Board(11).children",
        },
        "interpretation_guard":
            "only the 24 fresh Part EF batch-38 exact-LOSS rows (two-pass fresh-cold "
            "node-exact at the single 15M budget/order-0 condition) are consumed into the "
            "canonical cache by this Part; the 19 batch-38 probe-level WIN rows (incl. "
            "ai048) are consumed NOWHERE (WIN adoption is scrutiny-owner C++ "
            "second-implementation gate pin 9193f5b6... exclusive) and their keys sit in "
            "NO cache; the 6 honest-EXHAUSTED keys stay honest UNKNOWN; b018 stays "
            "excluded; class 30484 (4 children remaining: aj030/ai048/aj049/aj050, all "
            "unconsumed probe-level WINs) is NOT freed and NOT excluded; class 30345 "
            "(26 unknown children remain) is NOT freed; class 30118 (51 unknown children "
            "remain, Part EJ in-flight owner) is NOT freed; witnesses byte-static; class "
            "status stays unknown, free_now 39 static, closure table 807 rows static "
            "with NO left/entered exchange, the 6 rank-churn-only rows being pure "
            "bookkeeping; no root verdict and no coverage claim is made anywhere; the "
            "per-root/greedy/worklist quantities quoted here are bookkeeping, never "
            "verdicts; no update8 resolution changed (all 24 adopted s5 indices sit "
            "outside the frozen baseline requirement); 11x11 stays UNKNOWN",
    }
    (EXP / "output/decomp-deltas-b38loss24-adoption.json").write_text(
        json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("DECOMP OK changed=%d rank_churn=%d gs_dec=%d stable=%d left=%d entered=%d" % (
        len(changed), rank_churn, len(gs_dec), stable, len(left), len(entered)))
    print("class30345: unknown 50 -> 26 (all 24 adopted rows inside its boundary), NOT freed, rank 13 -> 11")
    print("class30484: unknown 5 -> 4 (1 adopted ai044; 4 unconsumed probe-WINs remain: aj030/ai048/aj049/aj050), NOT freed, rank 7 -> 7")
    print("class30118: unknown 52 -> 51 (1 adopted ai033), NOT freed, rank 21 -> 17")
    print("witnesses 16371/20421/34908: byte-static")


if __name__ == "__main__":
    main()
