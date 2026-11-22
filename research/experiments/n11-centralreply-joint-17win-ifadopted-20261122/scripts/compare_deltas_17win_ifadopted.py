#!/usr/bin/env python3
"""Joint 17-WIN if-adopted delta extractor (Part BB, 2026-11-22).

Fail-closed, read-only audit executing the two-owner Part BB declaration
(note amendment, declaration commit dafe9651, observed HEAD-before-push
53e7fae9).  Compares the published BASE refresh outputs (the Part AS
canonical reaudit on the 6,120-row canonical cache be9cb24e..., scenario
= the canonical classification) against the JOINT 17-WIN if-adopted
computation:

  IF-ADOPTED = canonical 6,120 rows + ALL seventeen unconsumed closure
  WIN rows of the repo history, adopted TOGETHER in one projection:

    b018 d002 e002 f017 g018 h045 j033 z003 n005 n006   (Part AJ wins10)
    p002 p003                                          (batch-13, Part AI)
    r001 r002                                          (batch-15, Part AN)
    q042                                               (batch-14, Part AT)
    v001 v002                                          (batch-18, Part BA)

  (17 unique WIN keys; joint increment 04003820..., if-adopted cache
  f8c2fd97..., canonical BASE be9cb24e... untouched.)

This is a projection for the scrutiny owner's adoption-decision
precomputation (k04 / q042 / v001+v002 precedent).  NO WIN verdict is
consumed anywhere by this Part: the canonical cache stays byte-identical
(machine-asserted against the published BASE sha), and the if-adopted
cache is NOT the repo canonical chain.  This Part neither recommends nor
rejects adoption.  Node counts are bookkeeping, never verdicts.

Byte chain: the 17 WIN rows are NOT re-derived from raws here.  Each row
was machine-verified against its own 2-pass raw passes, batch status
logs and quarantine registry at its own publication (Part AJ / AI / AN /
AT / BA extractors); this audit re-verifies the five PUBLISHED source
increments by sha256 at their upstream repo paths, cross-checks their
published manifests, REBUILDS the joint 17-row increment from those
source bytes and asserts byte identity with the published joint
increment, then asserts the merged if-adopted cache == BASE + 17 rows.

Gates (all fail-closed):
  * sha256 pins: joint increment, joint manifest, if-adopted cache,
    canonical BASE cache, BASE summary, scenario summary, BASE
    closure-classes.csv, BASE per-root-coverage.csv, scenario
    closure-classes.csv, scenario per-root-coverage.csv, batch-18
    batch-keys, both merge-audit runs, and the five upstream source
    increments + five source manifests (10 files, upstream paths),
  * joint manifest: 17 rows / 17 WINs / 0 LOSS, ifadopted_only, 17
    unique keys, course-bookkeeping (key, s5 index, nodes) per row
    machine-cross-checked against the graph mapping and the rebuilt
    packet; win_s5_in_update8_baseline_requirement recomputed,
  * the five source increments: every WIN row of every source is unique
    across sources, BASE-absent, quarantine-free, canonical-safe, in
    the pinned s5 universe; the 17-row joint packet rebuilt from them
    (sorted by (lo,hi)) is BYTE-IDENTICAL to the published joint
    increment; q042/b13/b15/b18 manifests machine cross-checked,
  * if-adopted cache == BASE rows + the 17 WIN rows (row count base+17,
    no verdict drift on shared rows, scenario-only rows == the 17 WIN
    keys), WIN counts 158 -> 175, LOSS 5,962 -> 5,962,
  * NONE of the 17 WIN s5 indices is resolved in the BASE known
    universe (all 17 verdicts stay unconsumed on main; 17/17 gate),
  * every recomputed status transition is one of
    excluded->excluded, excluded_now->excluded_now, free_now->free_now,
    unknown->{unknown, free_now, excluded_now},
  * flips (newly excluded_now) == exactly the machine-computed set of
    BASE-unknown graph holder classes of any of the 17 WIN s5 indices
    (per-WIN holder ledger + union computed from the pinned graph cost
    sets, never hardcoded); each transition is unknown->excluded_now;
    no regression,
  * source-class ledger (13 pinned batch classes, provenance = the
    upstream per-batch experiment dirs): collectively their BASE-unknown
    boundaries cover every one of the 17 adopted WIN s5 indices; 12 of
    the 13 are in flips; class 5830 (batch-15) is machine-asserted to be
    the documented exception: already excluded_now in BASE via a
    pre-existing WIN child (recorded), so r001/r002 add no new flip
    there; the batch-15 shared-cost effect lands on class 2634 instead,
  * class 16131: BASE-unknown children == exactly the 53 published
    batch-18 key s5 indices; scenario-unknown == 53 - 2 (v001/v002
    consumed by the projection only),
  * no newly free class and no newly free third (a WIN adoption can
    only flip classes to excluded_now, never free one - gated),
  * update8: no resolution lost; newly-resolved == exactly
    required_new_s5 (31,859) intersected with the 17 WIN s5 indices
    (machine-recomputed, recorded); resolved-count arithmetic
    consistent; BASE win_hit_groups == 0; every scenario win-hit group
    serves a class inside the machine-computed flip set,
  * per-root coverage recomputed from the graph matches the published
    per-root-coverage.csv for BASE and scenario; root 27 stays 119/119;
    a pure WIN adoption must not move any per-root free/uncovered count
    (gated),
  * canonical cache byte-pinned untouched (be9cb24e..., 6,120 rows).

Measured (recorded, not gated, scheduling quantities only): closure
table churn (left/entered classes), the scenario closure rows of the 13
source classes, per-root and joint greedy sizes, probe worklist size,
per-root greedy movers.

Interpretation guard: the IF-ADOPTED projection shows the scrutiny
owner what adopting all 17 unconsumed closure WINs TOGETHER would do to
the classification ledger: the BASE-unknown holder classes of those
children flip to excluded_now (a one-way door - the all-LOSS closure
route of every flipped class is permanently refuted by a verified WIN
child).  It is NOT a verdict consumption, NOT a closure claim, NOT a
19-root or 11x11 result, and neither an adoption recommendation nor a
rejection.  The standard 11x11 empty board, the 19 central-reply roots
and every class stay UNKNOWN.
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
OUT = EXP / "output/decomp-deltas-joint17win-ifadopted.json"

GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_DIR = ROOT / "research/experiments/n11-centralreply-class23101-loss41-adoption-reaudit-20261122/reaudit/output"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class23101-loss41-adoption-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-20261122.cache"
BATCH_DIR = ROOT / "research/experiments/n11-centralreply-closure-class16131-batch18-20261122"
SCEN_OUT = EXP / "reaudit/output"
INCR_CACHE = EXP / "output/increment-17win-joint-IFADOPTED-20261122.cache"
MANIFEST = EXP / "output/increment-manifest.json"
SCEN_CACHE = EXP / "output/merged-joint17win-IFADOPTED-20261122.cache"

# --- upstream published source increments (byte chains to their own
#     publication-time machine verifications; paths on main) -----------
SOURCES = [
    {"name": "part-aj-wins10", "rows": 10,
     "win_ids": ["b018", "d002", "e002", "f017", "g018", "h045", "j033",
                 "z003", "n005", "n006"],
     "incr": ROOT / "research/experiments/n11-centralreply-joint-unconsumed-ifadopted-20261122/output/increment-joint-wins10-IFADOPTED-20261122.cache",
     "manifest": ROOT / "research/experiments/n11-centralreply-joint-unconsumed-ifadopted-20261122/output/increments-manifest.json",
     "incr_sha": "fe2c6f68f49195b44e21c8d43998fccd965c868e08e49d8a1b3233f5daa4c15e",
     "manifest_sha": "74fb877dba862bb8d8ecaa28d4741fbc97f533087e1779fe49a3062af2600b88"},
    {"name": "batch13-wins2", "rows": 2,
     "win_ids": ["p002", "p003"],
     "incr": ROOT / "research/experiments/n11-centralreply-class16930-win-p002p003-ifadopted-20261122/output/increment-batch13-wins2-IFADOPTED-20261122.cache",
     "manifest": ROOT / "research/experiments/n11-centralreply-class16930-win-p002p003-ifadopted-20261122/output/increments-manifest.json",
     "incr_sha": "bb238f67dbfcc3b9a05ac5542f783107366777f17149f7a5a5af64d4864b0f7c",
     "manifest_sha": "43143fd51bb02ddf65d912018f063e631a70517d607c2a73a626b76bd8e5957c"},
    {"name": "batch15-wins2", "rows": 2,
     "win_ids": ["r001", "r002"],
     "incr": ROOT / "research/experiments/n11-centralreply-class5830-win-r001r002-ifadopted-20261122/output/increment-batch15-wins2-IFADOPTED-20261122.cache",
     "manifest": ROOT / "research/experiments/n11-centralreply-class5830-win-r001r002-ifadopted-20261122/output/increments-manifest.json",
     "incr_sha": "05c10e1ff17c2601b1fb4a0782af2543d302187ce6344df97d3c763947262b7d",
     "manifest_sha": "d6ed7b931fb3418ceb8879073b2668b184e3dfcc7a2d24230267fdb7da67777e"},
    {"name": "batch14-q042", "rows": 1,
     "win_ids": ["q042"],
     "incr": ROOT / "research/experiments/n11-centralreply-class23101-q042-ifadopted-20261122/output/increment-q042-win-ifadopted-20261122.cache",
     "manifest": ROOT / "research/experiments/n11-centralreply-class23101-q042-ifadopted-20261122/output/increment-manifest.json",
     "incr_sha": "b4958328270f11b24d3a638e1099a0c6047dbebb242e3116217b0473ef63f9b6",
     "manifest_sha": "894e9420b043e12543920bb63c49f00530e45ad5b29c95c65e3dadf3047fc02e"},
    {"name": "batch18-v001v002", "rows": 2,
     "win_ids": ["v001", "v002"],
     "incr": ROOT / "research/experiments/n11-centralreply-class16131-win-v001v002-ifadopted-20261122/output/increment-b18win-v001v002-ifadopted-20261122.cache",
     "manifest": ROOT / "research/experiments/n11-centralreply-class16131-win-v001v002-ifadopted-20261122/output/increment-manifest.json",
     "incr_sha": "4f8fc29bfd00492aa9a983f20a121737d395b8f80d53e2b04c271fec068bc1ee",
     "manifest_sha": "13736030ea484a0496da7f929b9c6892a2e9ebf6522f96d1c87d2c21000945f1"},
]

INCR_SHA = "04003820756b72bc3b35ac67746d9f6dd3dffd7315dbd2f36d50d497485cbe87"
MANIFEST_SHA = "509cc941fb77b6efccde23b64b7cc38c48814153d457c27a7b3576c47be9866d"
SCEN_CACHE_SHA = "f8c2fd970e836eaf17f955b139b18e2e81c0e899c4652edfb0bc05d0790bf7e9"
MERGE_AUDIT_SHA = "ae19b239cb4db449c3a5cd571e6f6447f2eddb9962d6c2d8b7d1cac701bac435"
BASE_CACHE_SHA = "be9cb24e899fbe93db51e415320c50fa733e378748bb7a41fe13fd7b22f06685"
BASE_SUMMARY_SHA = "f2008e70b31f23724d9bd8d605f7ab6f1de20f1802e65bd5b955420a2f50a744"
SCEN_SUMMARY_SHA = "5cee40860f5350ed758f8f4b266b9334aedfff7e9f36a76c22b2b18cae31795b"
BASE_CLOSURE_SHA = "3ee1dbb6db7a5fc8858f5bbdd5cae7ca754589f376ebb99727535806f917bc9e"
BASE_PRC_SHA = "527c7e9a3f6350f638b5e2e2a70c3115e50533eeca651e38e32329a04ab225d4"
SCEN_CLOSURE_SHA = "0c3c31f37b5e159cb4da63f9af41623c5bebc7c16ed4969c37447670033a99dd"
SCEN_PRC_SHA = "5ead108d55e8736af308ec5c702f14d7e7a62d3138fecaa94306c85c7dff5747"
BATCH_KEYS_SHA = "1bb3ed41b26af92491ed579a7c05471f271ed1394d8b5f817b5110794d926667"

SCENARIO = "IF-ADOPTED"
BATCH_CLASS = 16131
BATCH_KEY_COUNT = 53
UNIVERSE_SIZE = 31859
RECEIPT_COUNT = 23
ALLOWED_TRANSITIONS = {"excluded": ["excluded"], "excluded_now": ["excluded_now"],
                       "free_now": ["free_now"],
                       "unknown": ["unknown", "free_now", "excluded_now"]}

# 13 source classes of the 17 WINs (provenance: upstream per-batch
# experiment dirs + the batch manifests machine-pinned below).  The
# per-id key correspondence inside a batch is cosmetic bookkeeping for
# this joint Part; the gates below verify the LEDGER structurally.
SOURCE_CLASSES = {
    16757: "AJ b1 / b018", 20421: "AJ b3 / d002", 16371: "AJ b4 / e002",
    12264: "AJ b5 / f017", 5473: "AJ b6 / g018", 2634: "AJ b8 / h045",
    1518: "AJ b9 / j033", 8785: "AJ b11 / z003", 8106: "AJ b12 / n005+n006",
    16930: "batch13 / p002+p003", 5830: "batch15 / r001+r002",
    23101: "batch14 / q042", 16131: "batch18 / v001+v002",
}
MANIFEST_CLASS_PINS = {  # class_index fields machine-pinned by the source manifests
    "batch13-wins2": 16930, "batch15-wins2": 5830,
    "batch14-q042": 23101, "batch18-v001v002": 16131,
}
CLASS_5830 = 5830  # documented BASE-exception (see docstring gates)


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


def read_win_rows(path, name):
    rows = []
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        for lineno, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                fail(f"invalid row {lineno} in {name}: {row}")
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            if stones != 5 or verdict != 1 or nodes <= 0:
                fail(f"non-WIN row in {name} increment: {row}")
            rows.append((lo, hi, verdict, nodes))
    return rows


def main():
    # --- pins ------------------------------------------------------------------
    for name, p, want in (("joint increment", INCR_CACHE, INCR_SHA),
                          ("joint manifest", MANIFEST, MANIFEST_SHA),
                          ("if-adopted cache", SCEN_CACHE, SCEN_CACHE_SHA),
                          ("merge-audit run1", EXP / "output/merge-audit-run1.json", MERGE_AUDIT_SHA),
                          ("merge-audit run2", EXP / "output/merge-audit-run2.json", MERGE_AUDIT_SHA),
                          ("canonical BASE cache", BASE_CACHE, BASE_CACHE_SHA),
                          ("base summary", BASE_DIR / "refresh-summary.json", BASE_SUMMARY_SHA),
                          ("scenario summary", SCEN_OUT / "refresh-summary.json", SCEN_SUMMARY_SHA),
                          ("base closure-classes", BASE_DIR / "closure-classes.csv", BASE_CLOSURE_SHA),
                          ("base per-root-coverage", BASE_DIR / "per-root-coverage.csv", BASE_PRC_SHA),
                          ("scenario closure-classes", SCEN_OUT / "closure-classes.csv", SCEN_CLOSURE_SHA),
                          ("scenario per-root-coverage", SCEN_OUT / "per-root-coverage.csv", SCEN_PRC_SHA),
                          ("batch-keys", BATCH_DIR / "input/batch-keys.json", BATCH_KEYS_SHA)):
        got = sha(p)
        if got != want:
            fail(f"{name} sha256 drift: {got} != {want}")
    for src in SOURCES:
        got = sha(src["incr"])
        if got != src["incr_sha"]:
            fail(f"{src['name']} source increment sha drift: {got} != {src['incr_sha']}")
        got = sha(src["manifest"])
        if got != src["manifest_sha"]:
            fail(f"{src['name']} source manifest sha drift: {got} != {src['manifest_sha']}")

    manifest = json.loads(MANIFEST.read_text())
    if manifest["schema"] != "joint17win-ifadopted-increment-manifest-v1":
        fail("joint manifest schema drift")
    if manifest["part"] != "BB":
        fail("manifest part is not BB")
    rc = manifest["row_counts"]
    if not (rc["rows"] == 17 and rc["wins"] == 17 and rc["losses"] == 0):
        fail(f"manifest row_counts not the seventeen WIN rows: {rc}")
    if manifest["ifadopted_only"] is not True:
        fail("manifest ifadopted_only not asserted")
    if manifest["canonical_cache_untouched"] != BASE_CACHE_SHA:
        fail("manifest canonical pin does not match the published BASE sha")
    if manifest["sha256"]["win"] != INCR_SHA:
        fail("manifest win sha does not match the pinned joint increment")
    if manifest["base_cache_absent_hits"] != 0 or manifest["quarantine_hits"] != 0:
        fail("manifest BASE-absent / quarantine hit counters nonzero")
    if len(manifest["sources"]) != len(SOURCES):
        fail("manifest sources list length drift")
    for i, ms in enumerate(manifest["sources"]):
        if ms["name"] != SOURCES[i]["name"] or ms["rows"] != SOURCES[i]["rows"]:
            fail(f"manifest source[{i}] name/rows drift: {ms}")
        if ms["increment_sha256"] != SOURCES[i]["incr_sha"]:
            fail(f"manifest source {ms['name']} increment sha drift")
        if ms["manifest_sha256"] != SOURCES[i]["manifest_sha"]:
            fail(f"manifest source {ms['name']} manifest sha drift")
        if ms["win_ids"] != SOURCES[i]["win_ids"]:
            fail(f"manifest source {ms['name']} win_ids drift")

    WIN_IDS = [wid for src in SOURCES for wid in src["win_ids"]]
    if manifest["win_ids"] != WIN_IDS or len(WIN_IDS) != 17:
        fail("manifest win_ids bookkeeping drift")
    WIN_KEYS = [tuple(k) for k in manifest["win_keys"]]
    WIN_S5S = list(manifest["win_s5_index"])
    WIN_NODES = list(manifest["win_nodes"])
    if not (len(WIN_KEYS) == len(WIN_S5S) == len(WIN_NODES) == 17):
        fail("manifest win bookkeeping lists not 17 entries")
    # id -> key correspondence is cosmetic for the joint packet EXCEPT
    # where a pinned upstream manifest machine-pins it (q042, b18):

    sys.path.insert(0, str(BOARD_SOURCE.parent))
    sys.path.insert(0, str(POLICY.parent))
    from independent import Board
    from s5_evidence_policy import quarantined_cache_keys, is_canonical_safe_s5_key

    quarantined = quarantined_cache_keys()
    board = Board(11)

    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s4_masks, s4_status, s4_cost = g["s4_masks"], g["s4_status"], g["s4_cost"]
    roots = g["roots"]
    s5_masks = g["s5_masks"]
    mask_to_index = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}

    update8 = json.loads(UPDATE8.read_text(encoding="utf-8"))
    if update8["schema"] != "n11-night-repaired-joint-plan-update8-v1":
        fail("update8 schema drift")
    baseline_req = set(update8["required_new_s5"])
    if update8["union_size"] != UNIVERSE_SIZE or len(baseline_req) != UNIVERSE_SIZE:
        fail("update8 baseline drift")
    if not update8["verification"]["passed"]:
        fail("update8 verification flag not passed")
    receipt_verdicts = {int(k): int(v) for k, v in update8["resolved_s5_verdicts"].items()}
    if len(receipt_verdicts) != RECEIPT_COUNT:
        fail(f"receipt verdict count {len(receipt_verdicts)} != {RECEIPT_COUNT}")

    # --- rebuild the joint packet from the five source increments ---------------
    src_rows = {}
    packet = []
    for src in SOURCES:
        rows = read_win_rows(src["incr"], src["name"])
        if len(rows) != src["rows"]:
            fail(f"{src['name']}: source increment holds {len(rows)} WIN rows, expected {src['rows']}")
        for lo, hi, v, n in rows:
            if (lo, hi) in src_rows:
                fail(f"duplicate WIN key across sources: {(lo, hi)}")
            src_rows[(lo, hi)] = {"source": src["name"], "nodes": n}
            packet.append((lo, hi, v, n))
        mjson = json.loads(src["manifest"].read_text())
        if mjson.get("sha256", {}).get("win") != src["incr_sha"]:
            fail(f"{src['name']} manifest sha256.win does not chain to its increment")
        if mjson.get("base_cache_absent_hits") != 0 or mjson.get("quarantine_hits") != 0:
            fail(f"{src['name']} manifest BASE-absent / quarantine counters nonzero")
        flat = json.dumps(mjson.get("win_ids", "")).replace(" ", "")
        for wid in src["win_ids"]:
            if wid not in flat:
                fail(f"{src['name']} manifest lacks win id {wid}")
        if src["name"] in MANIFEST_CLASS_PINS:
            if int(mjson.get("class_index")) != MANIFEST_CLASS_PINS[src["name"]]:
                fail(f"{src['name']} manifest class_index != pinned ledger class")
    if len(packet) != 17:
        fail(f"rebuilt packet holds {len(packet)} rows, expected 17")
    ordered = sorted(packet, key=lambda r: (r[0], r[1]))
    rebuilt_keys = [(lo, hi) for lo, hi, _v, _n in ordered]
    if rebuilt_keys != WIN_KEYS:
        fail("rebuilt packet keys != joint manifest win_keys")
    if [r[3] for r in ordered] != WIN_NODES:
        fail("rebuilt packet nodes != joint manifest win_nodes")
    rebuilt_text = INCR_CACHE.read_text(encoding="utf-8-sig")
    body = rebuilt_text.splitlines()
    rows_text = [l for l in body if l and not l.lstrip().startswith("#")]
    want_rows = [f"s5verdict,{lo},{hi},5,1,{nodes}" for lo, hi, _v, nodes in ordered]
    if rows_text != want_rows:
        fail("published joint increment rows != rows rebuilt from the five source increments")

    # WIN/s5/nodes chain checks
    for (lo, hi), s5, nodes in zip(WIN_KEYS, WIN_S5S, WIN_NODES):
        key = (lo, hi)
        if mask_to_index.get(key) != s5:
            fail(f"key {key} does not map to manifest s5 index {s5}")
        if src_rows[key]["nodes"] != nodes:
            fail(f"key {key} nodes disagreement source/joint manifest")
    in_req = [s5 for s5 in WIN_S5S if s5 in baseline_req]
    if manifest["win_s5_in_update8_baseline_requirement"] != len(in_req):
        fail("manifest win_s5_in_update8_baseline_requirement drift")

    # q042 / b18 explicit manifest cross-checks
    q_man = json.loads(SOURCES[3]["manifest"].read_text())
    q_key = tuple(q_man["win_key"])
    if q_key not in src_rows:
        fail("q042 manifest key not present in the packet")
    if mask_to_index.get(q_key) != q_man["win_s5_index"]:
        fail("q042 manifest s5 index != graph mapping of its key")
    if src_rows[q_key]["nodes"] != q_man["win_nodes"]:
        fail("q042 nodes disagreement joint packet / q042 manifest")
    b_man = json.loads(SOURCES[4]["manifest"].read_text())
    for k, n, s5 in zip(b_man["win_keys"], b_man["win_nodes"], b_man["win_s5_index"]):
        key = tuple(k)
        if key not in src_rows:
            fail("b18 manifest key not present in the packet")
        if src_rows[key]["nodes"] != n:
            fail("b18 nodes disagreement joint packet / b18 manifest")
        if mask_to_index.get(key) != s5:
            fail("b18 manifest s5 index != graph mapping of its key")

    # --- batch keys against the pinned graph -----------------------------------
    bk = json.loads((BATCH_DIR / "input/batch-keys.json").read_text())
    if bk["class_index"] != BATCH_CLASS:
        fail(f"batch-keys class_index {bk['class_index']} != {BATCH_CLASS}")
    if [int(x) for x in bk["class_mask"]] != list(s4_masks[BATCH_CLASS]):
        fail("batch-keys class_mask != graph mask of the batch class")
    batch_s5s = sorted(int(k["s5_index"]) for k in bk["keys"])
    if len(batch_s5s) != BATCH_KEY_COUNT or len(set(batch_s5s)) != BATCH_KEY_COUNT:
        fail(f"batch-keys s5 index set is not {BATCH_KEY_COUNT} unique indices")

    # --- increment / quarantine / canonical safety -------------------------------
    incr = read_cache(INCR_CACHE)
    if len(incr) != 17 or set(incr) != set(WIN_KEYS):
        fail("joint increment is not exactly the seventeen pinned WIN keys")
    for (lo, hi), s5, nodes in zip(WIN_KEYS, WIN_S5S, WIN_NODES):
        if incr[(lo, hi)] != (1, nodes):
            fail(f"joint increment row {(lo, hi)} != (WIN, {nodes})")
        if (lo, hi) in quarantined or not is_canonical_safe_s5_key((lo, hi)):
            fail(f"WIN key {(lo, hi)} quarantined or noncanonical")

    # --- caches -------------------------------------------------------------------
    base_cache = read_cache(BASE_CACHE)
    scen_cache = read_cache(SCEN_CACHE)
    if len(base_cache) != 6120:
        fail(f"BASE cache rows {len(base_cache)} != 6120")
    for key in WIN_KEYS:
        if key in base_cache:
            fail(f"WIN row {key} already inside the canonical BASE cache "
                 "(would not be if-adopted)")
        if scen_cache.get(key) != (1, dict(zip(WIN_KEYS, WIN_NODES))[key]):
            fail(f"scenario cache does not adopt exactly the WIN row {key}")
    if len(scen_cache) != len(base_cache) + 17:
        fail("scenario cache row count != BASE + 17")
    for key, (v, _n) in scen_cache.items():
        b = base_cache.get(key)
        if b is None:
            if key not in set(WIN_KEYS):
                fail(f"scenario-only row outside the increment: {key}")
        elif b[0] != v:
            fail(f"scenario verdict drift on shared key {key}")
    base_votes = Counter(v for v, _ in base_cache.values())
    scen_votes = Counter(v for v, _ in scen_cache.values())
    if base_votes.get(1, 0) != 158 or scen_votes.get(1, 0) != 175:
        fail("WIN counts not 158 -> 175")
    if base_votes.get(2, 0) != 5962 or scen_votes.get(2, 0) != 5962:
        fail("LOSS counts not 5,962 -> 5,962")
    for key in scen_cache:
        if key in quarantined:
            fail(f"quarantined key inside scenario cache: {key}")
        if not is_canonical_safe_s5_key(key):
            fail(f"noncanonical scenario key {key}")

    # --- faithful re-execution of the published refresh class pass --------------
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
            fail(f"{name}: recomputed known universe {len(iv)} != published")
        if pub_in["cache_rows_in_universe"] != iu:
            fail(f"{name}: recomputed cache rows in universe {iu} != published")

    win_nodes_by_key = dict(zip(WIN_KEYS, WIN_NODES))
    s5_by_key = dict(zip(WIN_KEYS, WIN_S5S))
    for key in WIN_KEYS:
        if base_iv.get(s5_by_key[key]) is not None:
            fail(f"WIN s5 {s5_by_key[key]} ({key}) resolved in BASE "
                 "(verdict would be consumed on main)")

    # --- transitions + flips --------------------------------------------------------
    transitions = Counter()
    for i in range(len(s4_masks)):
        b, s = base_st[i], scen_st[i]
        transitions[f"{b}->{s}"] += 1
        if s not in ALLOWED_TRANSITIONS.get(b, []):
            fail(f"class {i} forbidden transition {b} -> {s}")
    base_excluded_now = {i for i, s in base_st.items() if s == "excluded_now"}
    flips = sorted(i for i, s in scen_st.items()
                   if s == "excluded_now" and i not in base_excluded_now)
    flipped_out = sorted(i for i, s in scen_st.items()
                         if s != "excluded_now" and i in base_excluded_now)
    if flipped_out:
        fail(f"excluded_now regressions {flipped_out} must be EMPTY")
    win_set = set(WIN_S5S)
    holders = {s5: sorted(i for i in range(len(s4_masks))
                          if s5 in s4_cost[i]) for s5 in WIN_S5S}
    holder_union = sorted(set().union(*[set(v) for v in holders.values()]))
    expected_flips = sorted(i for i in holder_union if base_st[i] == "unknown")
    if flips != expected_flips:
        fail(f"flips {flips} != machine-computed BASE-unknown holder union "
             f"{expected_flips}")
    for i in flips:
        if base_st[i] != "unknown" or scen_st[i] != "excluded_now":
            fail(f"flip class {i} is not unknown->excluded_now")
    new_free = sorted(i for i, s in scen_st.items()
                      if s == "free_now" and base_st[i] != "free_now")
    if new_free:
        fail(f"a WIN adoption created newly free classes {new_free} (must be impossible)")

    # --- source-class ledger ----------------------------------------------------------
    ledger = {}
    ledger_covers = set()
    for c, name in sorted(SOURCE_CLASSES.items()):
        held = sorted(set(base_unknown[c]) & win_set)
        if not held:
            fail(f"source class {c} ({name}) holds none of the 17 adopted WIN children")
        if c not in flips:
            if c != CLASS_5830:
                fail(f"source class {c} ({name}) not in flips without the documented "
                     "5830 exception")
            if base_st[c] != "excluded_now":
                fail("class 5830 exception is not BASE-excluded_now (ledger broken)")
        ledger_covers |= set(held)
        scen_expected = sorted(set(base_unknown[c]) - set(held))
        if sorted(scen_unknown[c]) != scen_expected:
            fail(f"source class {c} scenario-unknown boundary != BASE minus its "
                 "adopted WIN children")
        pre_win_children = sorted(j for j in s4_cost[c] if base_iv.get(j) == 1)
        ledger[str(c)] = {
            "provenance": name,
            "base_status": base_st[c],
            "scenario_status": scen_st[c],
            "in_flips": c in flips,
            "base_unknown_children": len(base_unknown[c]),
            "scenario_unknown_children": len(scen_unknown[c]),
            "adopted_win_children_held": held,
            "preexisting_base_win_children": pre_win_children,
        }
    if ledger_covers != win_set:
        fail(f"the 13-class ledger covers {len(ledger_covers)} of the 17 WIN children "
             "(must cover all 17)")

    # --- class 16131 strong gate -------------------------------------------------------
    base_class_unknown = sorted(base_unknown[BATCH_CLASS])
    if base_class_unknown != batch_s5s:
        fail("BASE-unknown children of class 16131 != the 53 batch-18 key s5 indices")
    scen_class = sorted(scen_unknown[BATCH_CLASS])
    v_s5s = [s5_by_key[tuple(k)] for k in json.loads(SOURCES[4]["manifest"].read_text())["win_keys"]]
    if sorted(set(base_class_unknown) - set(v_s5s)) != scen_class:
        fail("scenario-unknown children of 16131 != BASE-unknown minus v001/v002 "
             "(machine mismatch)")
    if len(scen_class) != BATCH_KEY_COUNT - 2:
        fail(f"class 16131 scenario-unknown children count {len(scen_class)} != 51")

    # --- metric table ------------------------------------------------------------------
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
    if metrics["excluded_now_classes"]["base"] != 23:
        fail("BASE excluded_now baseline drift (expected 23)")
    if metrics["unknown_classes"]["base"] != 34500:
        fail("BASE unknown baseline drift (expected 34,500)")
    if metrics["excluded_now_classes"]["scenario"] != 23 + len(flips):
        fail("excluded_now arithmetic inconsistent with the flip count")
    if metrics["unknown_classes"]["scenario"] != 34500 - len(flips):
        fail("unknown arithmetic inconsistent with the flip count")

    # --- update8 ------------------------------------------------------------------------
    base_resolved = set(base_summary["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    scen_resolved = set(scen_summary["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    lost = sorted(base_resolved - scen_resolved)
    if lost:
        fail(f"update8 resolutions lost: {lost}")
    newly_resolved = sorted(scen_resolved - base_resolved)
    want_newly = sorted(baseline_req & win_set)
    if newly_resolved != want_newly:
        fail(f"update8 newly-resolved {newly_resolved} != baseline requirement "
             f"intersected with the 17 WIN s5 indices {want_newly}")
    if len(newly_resolved) != metrics["update8_resolved_count"]["delta"]:
        fail("update8 resolved-count arithmetic inconsistent")
    if len(newly_resolved) != len(in_req):
        fail("newly-resolved count != recomputed in-baseline-requirement count")
    if metrics["update8_win_hit_groups"]["base"] != 0:
        fail("BASE win_hit_groups baseline drift (expected 0)")
    flip_set = set(flips)
    for grp in scen_summary["frozen_update8_refresh"]["win_hit_groups"]:
        if int(grp["s4_class_index"]) not in flip_set:
            fail(f"scenario win_hit group outside the flip set: {grp}")

    # --- per-root coverage ----------------------------------------------------------------
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
    if set(base_prc) != set(scen_prc) or len(base_prc) != len(roots):
        fail("per-root row set changed or count mismatch")
    for prc, by_root, name in ((base_prc, base_by_root, "BASE"),
                               (scen_prc, scen_by_root, SCENARIO)):
        for (role, first), (thirds, free, uncov, _ig) in prc.items():
            rr, rt, rf = by_root[first]
            if rr != role or rt != thirds or rf != free:
                fail(f"{name}: recomputed root {first} ({rr},{rt},{rf}) != "
                     f"published ({role},{thirds},{free})")
    for name, pub in published.items():
        r0 = pub["roots"][0]
        if (r0["role"], r0["origin_first"], r0["thirds"], r0["free_thirds_now"],
                r0["uncovered"]) != ("known-loss-baseline", 27, 119, 119, 0):
            fail(f"{name}: roots[0] not the 119/119 known-loss baseline")
    newly_free_thirds = [{"first": f, "third": t}
                         for (f, t), base_free in sorted(base_by_third.items())
                         if not base_free and scen_by_third[(f, t)]]
    if newly_free_thirds:
        fail(f"a WIN adoption created newly free thirds {newly_free_thirds} "
             "(must be impossible)")
    for (role, first), (thirds, bfree, buncov, big) in base_prc.items():
        sthirds, sfree, suncov, sig = scen_prc[(role, first)]
        del sthirds
        if (bfree, buncov) != (sfree, suncov):
            fail(f"root {first}: per-root free/uncovered moved under a pure WIN "
                 f"adoption ({bfree},{buncov})->({sfree},{suncov}) - impossible")
    prg_base = base_summary["per_root_greedy"]
    prg_scen = scen_summary["per_root_greedy"]
    per_root_greedy_movers = {}
    for first in sorted(prg_base, key=lambda x: int(x)):
        b, s = prg_base[first], prg_scen[first]
        per_root_greedy_movers[first] = {
            "base_greedy_union_size": b["greedy_union_size"],
            "scenario_greedy_union_size": s["greedy_union_size"],
            "delta": s["greedy_union_size"] - b["greedy_union_size"],
            "free_thirds": [b["free_thirds"], s["free_thirds"]],
            "uncovered_thirds": [b["uncovered_thirds"], s["uncovered_thirds"]],
        }

    # --- closure table observations ------------------------------------------------------
    def load_closure(path):
        with Path(path).open() as fh:
            return list(csv.DictReader(fh))

    base_cc = load_closure(BASE_DIR / "closure-classes.csv")
    scen_cc = load_closure(SCEN_OUT / "closure-classes.csv")
    base_idx = {int(r["class_index"]): r for r in base_cc}
    scen_idx = {int(r["class_index"]): r for r in scen_cc}
    closure_rows_ledger = {}
    for c in sorted(SOURCE_CLASSES):
        entry = {"base_in_table": c in base_idx, "scenario_in_table": c in scen_idx}
        if c in base_idx:
            entry["base_rank"] = int(base_idx[c]["class_rank"])
            entry["base_unknown_now"] = int(base_idx[c]["unknown_now"])
        if c in scen_idx:
            entry["scenario_rank"] = int(scen_idx[c]["class_rank"])
            entry["scenario_unknown_now"] = int(scen_idx[c]["unknown_now"])
        if c in base_idx and c in scen_idx:
            delta = (int(scen_idx[c]["unknown_now"])
                     - int(base_idx[c]["unknown_now"]))
            if delta != -len(ledger[str(c)]["adopted_win_children_held"]):
                fail(f"closure row for source class {c} unknown_now delta {delta} "
                     "!= its consumed WIN children")
            entry["unknown_now_delta"] = delta
        closure_rows_ledger[str(c)] = entry
    s_base = [r for r in base_cc if int(r["class_index"]) == BATCH_CLASS]
    s_scen = [r for r in scen_cc if int(r["class_index"]) == BATCH_CLASS]
    if len(s_base) != 1 or len(s_scen) != 1:
        fail(f"class {BATCH_CLASS} not exactly once in base ({len(s_base)}) "
             f"and scenario ({len(s_scen)}) closure-candidate tables")
    if int(s_base[0]["unknown_now"]) != 53:
        fail(f"base closure row for {BATCH_CLASS} unknown_now != 53")
    if int(s_scen[0]["unknown_now"]) != 51:
        fail(f"scenario closure row for {BATCH_CLASS} unknown_now != 51")
    closure_rows = {
        "base_class_16131_rank": int(s_base[0]["class_rank"]),
        "base_class_16131_unknown_now": int(s_base[0]["unknown_now"]),
        "scenario_class_16131_rank": int(s_scen[0]["class_rank"]),
        "scenario_class_16131_unknown_now": int(s_scen[0]["unknown_now"]),
        "left_table_classes": sorted(set(base_idx) - set(scen_idx)),
        "entered_table_classes": sorted(set(scen_idx) - set(base_idx)),
        "flipped_classes_in_table": sorted(set(flips) & set(scen_idx)),
        "source_class_rows": closure_rows_ledger,
        "note": ("the closure-candidate table is a probing-worklist view keyed to "
                 "unknown cost children; the win-flips are recorded by "
                 "class_status_counts and the transitions ledger, not by this table"),
    }

    # --- holder rows ------------------------------------------------------------------------
    holder_rows = {}
    for c in holder_union:
        held_here = sorted(s5 for s5 in WIN_S5S if c in holders[s5])
        holder_rows[str(c)] = {
            "base_status": base_st[c],
            "scenario_status": scen_st[c],
            "in_flips": c in flips,
            "adopted_wins_held": held_here,
            "base_unknown_now": len(base_unknown[c]),
            "scenario_unknown_now": len(scen_unknown[c]),
        }

    out = {
        "schema": "n11-joint17win-ifadopted-decomp-deltas-v1",
        "scenario": ("IF-ADOPTED = canonical 6,120 rows (be9cb24e..., Part AS) + "
                     "the十七 unconsumed closure WIN rows (b018 d002 e002 f017 g018 "
                     "h045 j033 z003 n005 n006 p002 p003 r001 r002 q042 v001 v002) "
                     "adopted TOGETHER as a what-if; the joint increment is "
                     "byte-rebuilt from the five sha-pinned published source "
                     "increments; a scrutiny-owner precomputation projection, NOT "
                     "the canonical chain").replace("十七", "seventeen "),
        "interpretation_guard": ("if-adopted projection deltas only: NO WIN verdict "
                                 "is consumed, the canonical cache is byte-pinned "
                                 "untouched, the BASE-unknown holder classes of the "
                                 "17 WIN children flip to excluded_now (one-way: "
                                 "their all-LOSS closure routes are permanently "
                                 "refuted by the verified WIN children); no "
                                 "coverage change; this Part neither recommends "
                                 "nor rejects adoption; the 11x11 empty board and "
                                 "all 19 central-reply roots stay UNKNOWN; nodes "
                                 "are bookkeeping"),
        "recompute_gates": ("class statuses with Board free-candidate child "
                            "verification, known-universe counts and per-root free "
                            "coverage were recomputed from graph + update8 + caches "
                            "and asserted equal to the published BASE (Part AS "
                            "reaudit) and if-adopted outputs before any delta was "
                            "emitted; the joint increment was byte-rebuilt from the "
                            "five sha-pinned upstream source increments; the "
                            "class-16131 BASE-unknown boundary was asserted equal to "
                            "the 53 batch-18 key s5 indices; none of the 17 WIN "
                            "s5 indices is resolved in the BASE known universe "
                            "(17/17 verdict non-consumption gate)"),
        "pins": {
            "increment_sha256": INCR_SHA,
            "manifest_sha256": MANIFEST_SHA,
            "ifadopted_cache_sha256": SCEN_CACHE_SHA,
            "merge_audit_sha256": MERGE_AUDIT_SHA,
            "canonical_base_cache_sha256": BASE_CACHE_SHA,
            "base_summary_sha256": BASE_SUMMARY_SHA,
            "ifadopted_summary_sha256": SCEN_SUMMARY_SHA,
            "base_closure_classes_sha256": BASE_CLOSURE_SHA,
            "base_per_root_coverage_sha256": BASE_PRC_SHA,
            "ifadopted_closure_classes_sha256": SCEN_CLOSURE_SHA,
            "ifadopted_per_root_coverage_sha256": SCEN_PRC_SHA,
            "batch_keys_sha256": BATCH_KEYS_SHA,
            "source_increments": {src["name"]: {"increment_sha256": src["incr_sha"],
                                                "manifest_sha256": src["manifest_sha"],
                                                "increment_path": str(src["incr"].relative_to(ROOT))}
                                  for src in SOURCES},
        },
        "win_rows": [
            {"key": [lo, hi], "s5_index": s5_by_key[(lo, hi)], "result": 1,
             "nodes": win_nodes_by_key[(lo, hi)], "source": src_rows[(lo, hi)]["source"]}
            for (lo, hi) in WIN_KEYS
        ],
        "win_id_bookkeeping": {
            "win_ids": WIN_IDS,
            "note": ("per-id key correspondence is cosmetic inside a batch for "
                     "this joint Part except where machine-pinned (q042, v001, "
                     "v002); the joint manifest stores keys sorted by (lo,hi) "
                     "independent of the id order"),
        },
        "flips_excluded_now": flips,
        "flips_gate": ("flips == the machine-computed BASE-unknown graph holder "
                       "classes of any of the 17 WIN s5 indices (per-WIN holder "
                       "ledger + union computed from the pinned graph cost sets, "
                       "not hardcoded); each transitions unknown -> excluded_now; "
                       "no regression; a WIN adoption can never free a class or "
                       "move per-root coverage (all gated)"),
        "status_transitions": dict(sorted(transitions.items())),
        "newly_free_now_classes": new_free,
        "win_holders": {
            "per_s5": {str(s5): holders[s5] for s5 in WIN_S5S},
            "holder_union": holder_union,
            "rows": holder_rows,
        },
        "source_class_ledger": ledger,
        "source_class_ledger_gate": ("the 13 pinned batch classes "
                                     "collectively cover all 17 adopted WIN "
                                     "children in their BASE-unknown boundaries; "
                                     "12 of 13 are in flips; class 5830 "
                                     "(batch-15) is the machine-verified BASE "
                                     "exception: already excluded_now via a "
                                     "pre-existing WIN child, so adopting "
                                     "r001/r002 flips no new class there (its "
                                     "shared-cost effect lands on class 2634, "
                                     "which holds 103558/103560/103561)"),
        "class_16131": {
            "base_status": base_st[BATCH_CLASS],
            "scenario_status": scen_st[BATCH_CLASS],
            "base_unknown_children": len(base_unknown[BATCH_CLASS]),
            "scenario_unknown_children": len(scen_unknown[BATCH_CLASS]),
            "base_unknown_equals_batch_keys": True,
            "scenario_unknown_indices": sorted(scen_unknown[BATCH_CLASS]),
        },
        "update8": {
            "newly_resolved_s5": newly_resolved,
            "in_baseline_requirement_count": len(in_req),
            "lost_resolved": lost,
            "win_hit_groups_base": base_summary["frozen_update8_refresh"]["win_hit_groups"],
            "win_hit_groups_scenario": scen_summary["frozen_update8_refresh"]["win_hit_groups"],
            "groups_free_now": [base_summary["frozen_update8_refresh"]["groups_free_now"],
                                scen_summary["frozen_update8_refresh"]["groups_free_now"]],
        },
        "newly_free_thirds": newly_free_thirds,
        "per_root_greedy": per_root_greedy_movers,
        "metrics": metrics,
        "closure_candidate_rows": closure_rows,
    }
    OUT.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("OK decomp-deltas-joint17win-ifadopted.json: "
          f"flips={len(flips)} new_free={new_free} "
          f"excluded_now {metrics['excluded_now_classes']['base']}->"
          f"{metrics['excluded_now_classes']['scenario']} "
          f"class16131 unknown {len(base_unknown[BATCH_CLASS])}->"
          f"{len(scen_unknown[BATCH_CLASS])} "
          f"free_now {metrics['free_now_classes']['base']}->"
          f"{metrics['free_now_classes']['scenario']} "
          f"update8_resolved +{len(newly_resolved)} "
          f"win_hit_groups {metrics['update8_win_hit_groups']['base']}->"
          f"{metrics['update8_win_hit_groups']['scenario']} "
          f"joint_greedy {metrics['joint_greedy_union_size']['base']}->"
          f"{metrics['joint_greedy_union_size']['scenario']} "
          f"worklist {metrics['probe_worklist_total']['base']}->"
          f"{metrics['probe_worklist_total']['scenario']}")


if __name__ == "__main__":
    main()
