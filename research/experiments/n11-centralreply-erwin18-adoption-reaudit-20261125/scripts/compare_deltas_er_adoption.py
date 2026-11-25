#!/usr/bin/env python3
"""BASE (canonical chain through the Part EP epwin10 first WIN adoption)
vs SCENARIO (erwin18 = Part ER second WIN canonical adoption: the remaining
18 batch-38 class-30345 exact-WIN rows, EQ-C++-gate-verified).

Fail-closed machine recomputation of exactly what the Part ER win18
canonical adoption changed, from published bytes only:

* every artifact sha-pinned (BASE = the published Part EP outputs -- the
  merged canonical cache fd29a337... 6,747 rows WIN 168 / LOSS 6,579, the
  reaudit outputs refresh-summary 5a1ff0c5... / closure-classes fdd4e4b2...
  / per-root-coverage 487a95c4... and worklist regen pin 7cd566bf...;
  SCEN = the Part ER outputs -- increment 4f6b7797... (18 s5verdict
  exact-WIN rows), increments-manifest 48b71d6a... (schema
  erwin18-increments-manifest-v1), the 6,765-row scenario cache 9c4dd94e...
  WIN 186 / LOSS 6,579 (chain name
  merged-exact-s5-chain-plus-erwin18-20261125.cache; the sha pin carries the
  identity), the merge-audits x3 (identical sha d55f578f...), the maker
  39f6c86a..., the byte-clones of the union merger 90711961... and both
  refresh forks (the published Part EP refresh 99d583c3... and the Part ER
  refresh fork 6c91e0ce...), the frozen graph/update8/board/policy/
  quarantine pins, and the batch-38 SSOT batch-keys 29807104...);
  both probe-worklists are UNPUBLISHED per the size policy - they enter ONLY
  as regen pins (BASE 7cd566bf... 3,718,981 B / SCEN 78e499dd... 3,717,828 B)
  re-verified by the byte-verbatim refresh re-execution; every published
  output is additionally fetch-back-checked at its wave head);
* the published Part EP refresh fork and the Part ER refresh fork are
  RE-EXECUTED byte-verbatim in isolated scratch trees against their pinned
  inputs, and all eight outputs must be byte-identical to the published /
  regenerated pins before any delta is emitted (double-run determinism; this
  simultaneously re-proves the published Part EP reaudit outputs are
  regenerable from published bytes);
* SCEN cache == BASE cache rows + exactly the 18 increment rows (verdict
  agreement everywhere; 6,765 rows, WIN 186 / LOSS 6,579); the adopted rows
  are ALL fresh exact-WIN rows of closure class 30345 (ai002 ai003 ai005
  ai006 ai010 ai013 ai014 ai017 ai023 ai028 ai034 ai035 ai036 ai039 ai043
  ai046 ai047 ai049, adopted node total 136,604,338 -- the Part EQ
  declaration prose figure 136,539,338 was a mis-sum, disclosed here; per-row
  registry/audit/raw data is SSOT and agrees on 136,604,338).  Their
  eligibility was proven by the maker against the byte-verified EQ C++ gate
  kit (74 entries, audit schema
  n11-centralreply-cppgate-30345win18-audit-v1, 21/21 GATE-PASS, 4
  byte-identical runs) and the batch-38 kit (181 entries): every manifest
  row is re-verified here against the b38 SSOT (lo/hi/s5_index per key),
  and the adopted set must equal the 19 raw-derived b38 WIN rows minus the
  EP-consumed ai048, exactly;
* the independent full-class census (frozen graph s4_cost + update8
  receipts + cache verdicts, replicating the refresh status logic) must
  reproduce the published class status counts EXACTLY on both sides (BASE
  34,477/43/39/390, SCEN 34,436/84/39/390) and identify EXACTLY 41 status
  flips, all UNKNOWN -> excluded_now, exactly the owner classes of the
  adopted keys that were still unknown (the three further owner classes
  29979/30345/30542 were already excluded_now from the Part EP adoption
  and must NOT double-flip);
* the class-30345 arithmetic is recomputed from the frozen dependency graph
  with the integer-geometry Board: the 51-raw-child boundary (50 in-universe
  cost children) drops unknown 25 -> 7 (18 members consumed here; the class
  already flipped to excluded_now at Part EP via ai048 and stays
  excluded_now - a scheduling-status fact, NOT a root verdict);
* the class-30118 arithmetic: the 56-child boundary, 56 cost children,
  adopted member ai034 only, unknown 51 -> 50; flips to excluded_now;
* the class-30354 arithmetic (no adopted member): 97-child boundary, 97
  cost children, unknown stays 96 -> 96 (its one WIN child ai048 was already
  EP-consumed; the class stays excluded_now);
* closure-classes.csv: ZERO rows leave, ZERO rows enter (805 -> 805); the
  only unknown_now churn is 30118: 51 -> 50 and 30345: 25 -> 7; NO
  groups_served churn anywhere; the only class_rank churn is the exact
  six-row swap-set {30345: 9->8, 34269: 8->9, 30118: 15->12, 12264: 12->13,
  5473: 13->14, 16957: 14->15}; every other field of every row is
  byte-identical;
* update8 refresh: resolved stays 260, remaining stays 31,505,
  groups_free_now stays 131, union baseline stays 31,859, and the win_hit
  groups are UNCHANGED: exactly 10 groups ALL of s4 class 30354 -- the
  quartets (12,40,96,60), (12,80,96,60), (12,96,40,60), (24,40,108,60),
  (24,80,108,60), (24,108,40,60), (36,20,90,60), (36,30,100,60),
  (36,90,20,60), (36,100,30,60) -- all with unknown_s5_children 97 on BOTH
  sides (the ER adoption consumes no child of 30354);
* per-root coverage: free_now/uncovered thirds are IDENTICAL at every one
  of the roots; Board verification 39/39 with zero rejections on both
  sides; the individual greedy union changes only at 3 roots
  (0: 2981->2980, 12: 2868->2850, 36: 3025->3007 -- pure re-selection
  bookkeeping, no coverage claim);
* the frozen greedy scheduler deltas are recorded as bookkeeping (joint
  greedy 36,643 -> 36,619, group_best_options_nonfree stays 2,105,
  worklist 64,328 -> 64,309).

No unknown verdict is asserted anywhere.  The standard 11x11 empty board
and every central-reply root stay UNKNOWN; free_now / coverage quantities
are scheduling bookkeeping derived from exact verdicts, not root verdict
claims.  Consuming the 18 WIN labels transfers NO verdict to any root: 41
classes become excluded (a known WIN cost child ends free all-LOSS
coverage), which removes them from the free-coverage option space and
shrinks the remaining greedy union - recorded honestly below.  The 6
batch-38 EXHAUSTED rows (ai007/ai024/ai030/ai038/ai040/ai041) stay honest
UNKNOWN at the 15M condition; b018, the k04 sixth-cost WIN, and every other
unconsumed probe-level WIN stay in NO cache; 11x11 stays UNKNOWN.
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

BASE_EXP = ROOT / "research/experiments/n11-centralreply-epwin10-adoption-reaudit-20261125"
BASE_OUT = BASE_EXP / "reaudit/output"
BASE_CACHE = BASE_EXP / "output/merged-exact-s5-chain-plus-epwin10-20261125.cache"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-erwin18-20261125.cache"
INCR = EXP / "output/increment-erwin18-20261125.cache"
MANIFEST = EXP / "output/increments-manifest.json"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
B38_KEYS = ROOT / "research/experiments/n11-centralreply-closure-class30345-batch38-20261125/input/batch-keys-b38.json"
BASE_REFRESH_SCRIPT = BASE_EXP / "reaudit/scripts/refresh_adoption_ep.py"
SCEN_REFRESH_SCRIPT = EXP / "reaudit/scripts/refresh_adoption_er.py"
MERGER = EXP / "scripts/s5_union_merge.py"
MAKER = EXP / "scripts/make_increments_er_win18_adoption.py"
DECOMP_OUT = EXP / "output/decomp-deltas-erwin18-adoption.json"

# ---- pins ------------------------------------------------------------------
BASE_CACHE_SHA = "fd29a33726e2e083998c67d83bf90822f84beebac30728ea79ea713e880cd1af"
SCEN_CACHE_SHA = "9c4dd94e61b6ee724a966ecc9552e527ba5a7107de732f0e9c5ced33bdad4a5a"
INCR_SHA = "4f6b7797df3bb950703f95e7ec72f288a447434da5b4ccf3d6d94ee8d8d6ffc1"
MANIFEST_SHA = "48b71d6af77306a94bd561f625838cff70cd94f12d702bcda0e945b67237450a"
MAKER_SHA = "39f6c86ab7d7772e608b23549500ac808a8f3298bdd0a744102dbb0cabed1e39"
BASE_SUMMARY_SHA = "5a1ff0c58acdb2bb96ae0eb0f2c5183fb9459afbacb3392ae08e005a313a3b01"
BASE_CLOSURE_SHA = "fdd4e4b2ae08db14f2fe5f0d934a3f42a93cf687f348ef1f3074b677758ba38d"
BASE_PRC_SHA = "487a95c48083b0626aba341e77eb80037be07104a3c7621ab2bac4e352816c57"
BASE_WORKLIST_SHA = "7cd566bfa39a4211893156151ed976fa31e19ddfe0658de1afbf2b6757f0b004"
SCEN_SUMMARY_SHA = "a6b8d0824e21e3d4f37bdd32a26dd8146234afb5a83f67f2734c1a83b99e1317"
SCEN_CLOSURE_SHA = "4c03f965a717a80cf2ce9980de8d2658c316891ae8fb83e8d9e62d84b14b4c14"
SCEN_PRC_SHA = "1bf6c25a2bdd7506bc5762acddc2f86aac2faf333e3d41d7b9c9fe4afb1c644a"
SCEN_WORKLIST_SHA = "78e499dd5553c99b2c1ec09ba3d8071ea72cc5ed065ba4578316bddfe8084996"
BASE_REFRESH_SHA = "99d583c3e73657bb6bd2e6cfa55dfc73c83da3151c180c0252cccd464e2501aa"
SCEN_REFRESH_SHA = "6c91e0ceaee03592f18ca1c36130d868cc7221bbe1819b803c4ba12b917a6061"
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
MERGE_AUDIT_SHA = "d55f578f65be6ce3cb379dbdd56f80e08e69348e519137991660bac3362444b1"
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
BOARD_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
B38_KEYS_SHA = "298071046bfba8473c5b3d6e0b6a30108697eb0899aed7c70fcb4c5343f7cb8d"

EQ_KIT_MANIFEST_SHA = "786315f35e73cc322f0746c68e5cb7d93369628933e46d45ff77f4f247cd304d"
EQ_REGISTRY_SHA = "85736edf3a1b049afc3476c7cb78d1980415888a42c10037e632d393c79cb09c"
EQ_AUDIT_SHA = "c2ff2232271d87459fd6954b5076e3a6462c849a15cd891fe51f343c931f0174"
EQ_AUDIT_SCHEMA = "n11-centralreply-cppgate-30345win18-audit-v1"
EQ_GATE_SOURCE_SHA = "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e"
EQ_GATE_STATUS_PASS = 21
B38_MANIFEST_SHA = "4dbf8856597709b3bd41d6f185a0502ebbdee447b1fc48d0caab586fdcc5ac02"
EP_INCREMENT_SHA = "c245bc4c63fdd116f5d707736a4b06925c7e0c48df92993a21363a910e7de1f2"

ADOPTED = {
    "ai002": (151694, 1153485554071900160, 65536),
    "ai003": (195012, 3458765613332172800, 65536),
    "ai005": (355799, 1152922604118544384, 65536),
    "ai006": (391735, 1152922604118478848, 65537),
    "ai010": (624629, 1152923153874292736, 65536),
    "ai013": (731678, 1152922604386914304, 65536),
    "ai014": (753317, 1157426203745849344, 65536),
    "ai017": (826581, 1161929803373219840, 65536),
    "ai023": (888357, 1152922604120576000, 65536),
    "ai028": (892997, 1152921573327372288, 1056768),
    "ai034": (896605, 1152921573326324736, 68720525312),
    "ai035": (897030, 1152922672837955584, 65536),
    "ai036": (897221, 1152922604119003136, 65536),
    "ai039": (899303, 1152921573327372288, 1064960),
    "ai043": (900322, 1152922604152033280, 65536),
    "ai046": (900561, 1152921573327372288, 1081344),
    "ai047": (900716, 1152921573327372288, 1114112),
    "ai049": (900719, 1152921573327372288, 68720525312),
}
ADOPTED_IDS = ["ai002", "ai003", "ai005", "ai006", "ai010", "ai013", "ai014",
               "ai017", "ai023", "ai028", "ai034", "ai035", "ai036", "ai039",
               "ai043", "ai046", "ai047", "ai049"]
ADOPTED_NODES = 136604338
EQ_PROSE_NODES = 136539338
FLIP_CLASSES = [4099, 4133, 5184, 5220, 6233, 10165, 10197, 11127, 11162, 11979,
                18652, 18684, 19683, 22617, 22642, 23424, 23452, 24199, 26520,
                26543, 27071, 29779, 29806, 29957, 30118, 30130, 30146, 30156,
                30189, 30257, 30278, 30324, 30330, 30333, 30338, 30340, 30344,
                30349, 30350, 30351, 30463]
PREV_EXCLUDED_OWNERS = [29979, 30345, 30542]
CENSUS_BEFORE = {"unknown": 34477, "excluded_now": 43, "free_now": 39, "excluded": 390}
CENSUS_AFTER = {"unknown": 34436, "excluded_now": 84, "free_now": 39, "excluded": 390}
WIN_HIT_QUARTETS = [(12, 40, 96, 60), (12, 80, 96, 60), (12, 96, 40, 60),
                    (24, 40, 108, 60), (24, 80, 108, 60), (24, 108, 40, 60),
                    (36, 20, 90, 60), (36, 30, 100, 60), (36, 90, 20, 60),
                    (36, 100, 30, 60)]
GREEDY_DELTA = {"0": (2981, 2980), "12": (2868, 2850), "36": (3025, 3007)}
JOINT_GREEDY = (36643, 36619)
GROUP_BEST_NONFREE = (2105, 2105)
WORKLIST_TOTAL = (64328, 64309)
UPD8 = {"resolved": (260, 260), "remaining": (31505, 31505), "free_groups": (131, 131)}
CLOSURE = {"rows": (805, 805), "left": [], "entered": []}
CLOSURE_UNKNOWN_CHURN = {30118: ("51", "50"), 30345: ("25", "7")}
CLOSURE_RANK_CHURN = {34269: (8, 9), 30345: (9, 8), 12264: (12, 13),
                      5473: (13, 14), 16957: (14, 15), 30118: (15, 12)}


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
        ("maker", MAKER, MAKER_SHA),
        ("b38 batch-keys SSOT", B38_KEYS, B38_KEYS_SHA),
        ("base refresh-summary", BASE_OUT / "refresh-summary.json", BASE_SUMMARY_SHA),
        ("base closure-classes", BASE_OUT / "closure-classes.csv", BASE_CLOSURE_SHA),
        ("base per-root-coverage", BASE_OUT / "per-root-coverage.csv", BASE_PRC_SHA),
        ("scenario refresh-summary", EXP / "reaudit/output/refresh-summary.json", SCEN_SUMMARY_SHA),
        ("scenario closure-classes", EXP / "reaudit/output/closure-classes.csv", SCEN_CLOSURE_SHA),
        ("scenario per-root-coverage", EXP / "reaudit/output/per-root-coverage.csv", SCEN_PRC_SHA),
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
    if manifest["schema"] != "erwin18-increments-manifest-v1":
        fail("manifest schema drift")
    if manifest["part"] != "ER" or manifest["date"] != "2026-11-25":
        fail("manifest part/date drift")
    if manifest["win_canonical_adoption"] is not True:
        fail("manifest win_canonical_adoption flag drift")
    if manifest["base_cache_sha256"] != BASE_CACHE_SHA:
        fail("manifest base cache pin drift")
    if manifest["sha256"]["win_increment"] != INCR_SHA:
        fail("manifest win_increment pin drift")
    if manifest["merger_sha256"] != MERGER_SHA:
        fail("manifest merger pin drift")
    if manifest["base_cache_rows"] != 6747:
        fail("manifest base rows drift")
    if manifest["row_counts"] != {"adopted_win_rows": 18,
                                  "exhausted_honest_unknown_rows": 0,
                                  "prior_canonical_rows_base": 6747,
                                  "loss_rows_this_pool": 0}:
        fail("manifest row_counts drift")
    if manifest["adopted_ids"] != ADOPTED_IDS or manifest["resolved_ids"] != ADOPTED_IDS:
        fail("manifest adopted ids drift")
    if manifest["adopted_nodes_per_pool"] != ADOPTED_NODES:
        fail("manifest adopted node pool drift")
    if manifest["adopted_nodes_declared_in_eq_prose"]["value"] != EQ_PROSE_NODES:
        fail("manifest EQ prose mis-sum record drift")
    if manifest["quarantine_hits"] != 0:
        fail("manifest quarantine hits drift")
    if manifest["base_cache_absent_hits_for_emitted"] != 18:
        fail("manifest base-absent hits drift")
    if manifest["full_packet_eq_win_only"] is not True or manifest["loss_scenario_exists"] is not False:
        fail("manifest full-packet flags drift")
    rows = manifest["adopted_win_rows"]
    if len(rows) != 18:
        fail("manifest adopted row count drift")
    if sum(r["nodes"] for r in rows) != ADOPTED_NODES:
        fail("manifest adopted node sum drift")
    for r in rows:
        kid = r["key_id"]
        ok = (kid in ADOPTED and
              r["class"] == 30345 and
              (r["s5_index"], r["lo"], r["hi"]) == ADOPTED[kid] and
              r["result"] == 1 and
              r["budget"] == 15000000 and
              r["nodes"] > 0 and
              r["nodes"] < r["budget"] and
              r["gate_kit"] == "eq" and
              r["source_kit"] == "b38" and
              r["gate_input_sha256"] and
              r["gate_raw_p1_sha256"] and
              r["gate_raw_p2_sha256"] and
              r["source_raw_p1_sha256"] and
              r["source_raw_p2_sha256"])
        if not ok:
            fail(f"manifest adopted row drift: {kid}")
    prov = manifest["provenance"]
    if prov["eq_kit_manifest_sha256"] != EQ_KIT_MANIFEST_SHA or \
            prov["eq_registry_sha256"] != EQ_REGISTRY_SHA or \
            prov["eq_audit_sha256"] != EQ_AUDIT_SHA or \
            prov["eq_audit_schema"] != EQ_AUDIT_SCHEMA or \
            prov["eq_gate_status_pass"] != EQ_GATE_STATUS_PASS or \
            prov["eq_gate_source_sha256"] != EQ_GATE_SOURCE_SHA or \
            prov["b38_manifest_sha256"] != B38_MANIFEST_SHA or \
            prov["b38_keys_sha256"] != B38_KEYS_SHA or \
            prov["ep_increment_sha256"] != EP_INCREMENT_SHA:
        fail("manifest provenance EQ/b38/EP pin drift")
    dispo = manifest["batch38_disposition_derivation"]
    if dispo["counts"] != {"WIN": 19, "LOSS": 24, "EXHAUSTED": 6}:
        fail("manifest b38 disposition counts drift")
    if dispo["consumed_by_ep"] != ["ai048"] or dispo["targets_adopted_here"] != ADOPTED_IDS:
        fail("manifest b38 disposition target drift")
    # cross-verify every adopted row against the batch-38 SSOT
    b38 = json.loads(B38_KEYS.read_text())["keys"]
    ssot = {k["key_id"]: k for k in b38}
    for kid in ADOPTED_IDS:
        k = ssot[kid]
        if (int(k["s5_index"]), int(k["lo"]), int(k["hi"])) != ADOPTED[kid]:
            fail(f"b38 SSOT lo/hi/s5_index drift for {kid}")
    if sorted(dispo["published_raw_derived"]["WIN"]) != sorted(ADOPTED_IDS + ["ai048"]):
        fail("b38 WIN set != adopted 18 + EP-consumed ai048")
    oos = manifest["verdicts_out_of_scope_unconsumed"]
    for key in ("batch38_6_exhausted", "batch38_loss_rows", "ai048", "ai044",
                "b018", "k04_sixthcost_win", "other_closure_wins"):
        if not oos.get(key):
            fail(f"manifest must declare the out-of-scope entry: {key}")
    if "UNKNOWN" not in manifest["interpretation_guard"]:
        fail("manifest interpretation guard drift")

    # --- refresh re-execution (double-run determinism; runs BEFORE the heavy
    # graph load in the parent so the two processes never co-resident the
    # graph -- only the verify guarantees differ in no way) -----------------
    # --- refresh re-execution (double-run determinism) ----------------------
    base_tmp = rerun_refresh(BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA, ".erverify-base-ep")
    scen_tmp = rerun_refresh(SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA, ".erverify-scen-er")
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
    shutil.rmtree(ROOT / "research/experiments/.erverify-base-ep")
    shutil.rmtree(ROOT / "research/experiments/.erverify-scen-er")

    # --- frozen dependency graph + cache relation ---------------------------
    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s5_masks = g["s5_masks"]
    m2i_probe = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}

    # --- cache relation: SCEN == BASE + exactly the 18 increment rows --------
    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    incr = load_cache(INCR)
    if len(base) != 6747 or len(scen) != 6765 or len(incr) != 18:
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
    if (wins, losses) != (186, 6579):
        fail(f"scenario verdict counts {wins}/{losses} != 186/6,579")
    if sum(v[1] for v in incr.values()) != ADOPTED_NODES:
        fail("increment node total drift")
    # EP regression tie: the EP-consumed ai048 must already sit WIN in BASE
    # ai048 (EP-adopted) = s5_index 900718, lo 1152921573327372288, hi 68157440
    ai048_key = (1152921573327372288, 68157440)
    if m2i_probe.get(ai048_key) != 900718:
        fail("ai048 s5 index drift")
    if base.get(ai048_key) is None or base[ai048_key][0] != 1:
        fail("the EP-consumed ai048 WIN must already sit in the BASE cache")
    if ai048_key in incr:
        fail("ai048 must NOT be re-adopted by ER")

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
    owner_union = sorted({c for v in owners.values() for c in v})
    if owner_union != sorted(set(FLIP_CLASSES) | set(PREV_EXCLUDED_OWNERS)):
        fail(f"adopted-key owner union != 41 flips + the 3 EP-pre-excluded: {owner_union}")
    for i in PREV_EXCLUDED_OWNERS:
        if cb[i][0] != "excluded_now" or ca[i][0] != "excluded_now":
            fail(f"EP-pre-excluded owner class {i} must stay excluded_now on both sides")

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

    cls_30345 = check_class(30345, 51, 50, 25, 7, list(ADOPTED))
    cls_30118 = check_class(30118, 56, 56, 51, 50, ["ai034"])
    cls_30354 = check_class(30354, 97, 97, 96, 96, [])
    if cls_30345["status_base"] != "excluded_now" or cls_30345["status_scen"] != "excluded_now":
        fail("class 30345 must be excluded_now on both sides (EP flipped it)")
    if cls_30118["status_base"] != "unknown" or cls_30118["status_scen"] != "excluded_now":
        fail("class 30118 must flip unknown -> excluded_now")
    if cls_30354["status_base"] != "excluded_now" or cls_30354["status_scen"] != "excluded_now":
        fail("class 30354 must stay excluded_now (EP-flipped, no ER member)")

    # --- closure-classes.csv comparison ----------------------------------------
    def read_closure(p):
        return {int(r["class_index"]): r for r in csv.DictReader(open(p))}

    c_before, c_after = read_closure(BASE_OUT / "closure-classes.csv"), \
        read_closure(EXP / "reaudit/output/closure-classes.csv")
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
    sa = json.loads((EXP / "reaudit/output/refresh-summary.json").read_text())
    ub_, ua_ = sb["frozen_update8_refresh"], sa["frozen_update8_refresh"]
    if ub_["union_size_baseline"] != 31859 or ua_["union_size_baseline"] != 31859:
        fail("update8 baseline drift")
    if (ub_["resolved_count"], ua_["resolved_count"]) != UPD8["resolved"]:
        fail("update8 resolved drift")
    if (ub_["remaining_now"], ua_["remaining_now"]) != UPD8["remaining"]:
        fail("update8 remaining drift")
    if (ub_["groups_free_now"], ua_["groups_free_now"]) != UPD8["free_groups"]:
        fail("update8 free groups drift")
    # win_hit groups unchanged EP -> ER: both sides hold the same 10 groups
    if len(ua_["win_hit_groups"]) != 10 or len(ub_["win_hit_groups"]) != 10:
        fail("win_hit group counts drift (both sides must hold 10)")
    got_qb = sorted((w["first"], w["third"], w["fourth"], w["reply"]) for w in ub_["win_hit_groups"])
    got_qa = sorted((w["first"], w["third"], w["fourth"], w["reply"]) for w in ua_["win_hit_groups"])
    if got_qb != sorted(WIN_HIT_QUARTETS) or got_qa != sorted(WIN_HIT_QUARTETS):
        fail(f"win_hit quartets drift: base {got_qb} scen {got_qa}")
    if any(w["s4_class_index"] != 30354 or w["unknown_s5_children"] != 97
           for w in ub_["win_hit_groups"] + ua_["win_hit_groups"]):
        fail("win_hit groups must all be class 30354 with 97 unknown children")
    if (sb["class_status_counts"], sa["class_status_counts"]) != (CENSUS_BEFORE, CENSUS_AFTER):
        fail("published status counts mismatch the pinned censuses")

    # --- per-root coverage comparison ------------------------------------------
    def read_prc(p):
        return {r["first"]: r for r in csv.DictReader(open(p))}

    pb_, pa_ = read_prc(BASE_OUT / "per-root-coverage.csv"), \
        read_prc(EXP / "reaudit/output/per-root-coverage.csv")
    if set(pb_) != set(pa_) or len(pb_) != 20:
        fail("per-root root set drift")
    greedy_delta = {}
    for rt in pb_:
        b, a = pb_[rt], pa_[rt]
        for f in ("role", "thirds", "free_now", "uncovered"):
            if b[f] != a[f]:
                fail(f"per-root {f} churn at root {rt}")
        if b["individual_greedy_union"] != a["individual_greedy_union"]:
            greedy_delta[rt] = (int(b["individual_greedy_union"]), int(a["individual_greedy_union"]))
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
            sb["board_verification"]["rejected"] != {} or sa["board_verification"]["rejected"] != {}:
        fail("Board verification drift")

    # --- decomposition emission -------------------------------------------------
    flipped = {str(c): {"status_base": cb[c][0], "status_scen": ca[c][0],
                        "adopted_members": sorted(adopted_indices[j] for j in s4_cost[c]
                                                  if j in adopted_indices),
                        "cost_size": len(s4_cost[c]),
                        "cost_unknown_base": sum(1 for j in s4_cost[c] if known(j, base) is None),
                        "cost_unknown_scen": sum(1 for j in s4_cost[c] if known(j, scen) is None)}
               for c in FLIP_CLASSES}
    decomp = {
        "schema": "erwin18-decomp-deltas-v1",
        "part": "ER",
        "date": "2026-11-25",
        "base": {
            "cache_sha256": BASE_CACHE_SHA,
            "rows": 6747, "win": 168, "loss": 6579,
            "refresh_summary_sha256": BASE_SUMMARY_SHA,
            "closure_classes_sha256": BASE_CLOSURE_SHA,
            "per_root_coverage_sha256": BASE_PRC_SHA,
            "probe_worklist_sha256": BASE_WORKLIST_SHA,
            "class_status_counts": CENSUS_BEFORE,
        },
        "scen": {
            "cache_sha256": SCEN_CACHE_SHA,
            "rows": 6765, "win": 186, "loss": 6579,
            "increment_sha256": INCR_SHA,
            "manifest_sha256": MANIFEST_SHA,
            "refresh_summary_sha256": SCEN_SUMMARY_SHA,
            "closure_classes_sha256": SCEN_CLOSURE_SHA,
            "per_root_coverage_sha256": SCEN_PRC_SHA,
            "probe_worklist_regen_pin_sha256": SCEN_WORKLIST_SHA,
            "probe_worklist_not_published_size_policy_bytes": 3717828,
            "class_status_counts": CENSUS_AFTER,
        },
        "adopted": {
            "ids": list(ADOPTED),
            "nodes_total": ADOPTED_NODES,
            "classes": {"30345": 18},
            "eq_prose_nodes_mis_sum_disclosed": EQ_PROSE_NODES,
            "eq_prose_correction": "Part EQ declaration prose summed 136,539,338 (mis-sum); per-row registry/audit/raw agree on 136,604,338 (SSOT = per-row data)",
        },
        "class_flips": {
            "count": 41,
            "direction": "unknown->excluded_now",
            "classes": flipped,
            "per_key_owner_classes": {k: sorted(owners[k]) for k in sorted(owners)},
            "owner_union_nonflip_classes": {"29979": "excluded_now (EP flip)",
                                           "30345": "excluded_now (EP flip via ai048)",
                                           "30542": "excluded_now (EP flip)"},
        },
        "closure_classes": {
            "rows_before_after": list(CLOSURE["rows"]),
            "left_rows": [],
            "entered_rows": [],
            "rank_churn": {str(k): list(v) for k, v in sorted(CLOSURE_RANK_CHURN.items())},
            "rank_churn_nature": "30345 rises 9->8 and 30118 rises 15->12 (unknown_now drops); the displaced rows shift down by one; no renumbering elsewhere",
            "unknown_churn": {"30118": ["51", "50"], "30345": ["25", "7"]},
            "groups_served_churn": {},
            "class_30345": cls_30345,
            "class_30118": cls_30118,
            "class_30354": cls_30354,
        },
        "frozen_update8": {
            "union_baseline": 31859,
            "resolved": list(UPD8["resolved"]),
            "remaining_now": list(UPD8["remaining"]),
            "groups_free_now": list(UPD8["free_groups"]),
            "win_hit_groups_base_and_scen_identical": [{"first": w[0], "third": w[1], "fourth": w[2],
                                                        "reply": w[3], "s4_class_index": 30354,
                                                        "unknown_s5_children": 97} for w in WIN_HIT_QUARTETS],
        },
        "per_root": {
            "free_now_uncovered": "identical at all central roots + baseline; no coverage claim",
            "greedy_union_changes": {k: list(v) for k, v in sorted(GREEDY_DELTA.items(), key=lambda kv: int(kv[0]))},
            "joint_greedy": list(JOINT_GREEDY),
            "group_best_options_nonfree": list(GROUP_BEST_NONFREE),
            "worklist_total": list(WORKLIST_TOTAL),
        },
        "honesty": {
            "second_win_adoption": True,
            "no_root_verdict": "no root verdict is asserted or implied by any class flip",
            "exclusion_effect": "41 classes become excluded (known WIN cost child ends free all-LOSS coverage): remaining greedy union shrinks 36,643 -> 36,619 (-24) and worklist shrinks 64,328 -> 64,309 (-19): scheduling bookkeeping only",
            "unknown_still": "34,436 S4 classes remain status-unknown; 11x11 stays UNKNOWN",
            "out_of_scope_unconsumed": ["batch-38 6 EXHAUSTED rows (honest UNKNOWN at the 15M condition)",
                                        "b38 LOSS rows (Part EM territory)", "b018 probe-level WIN",
                                        "k04 sixth-cost WIN", "all other probe-level WINs"],
            "nodes_are_bookkeeping": True,
        },
    }
    DECOMP_OUT.write_text(json.dumps(decomp, indent=1, ensure_ascii=False, sort_keys=True) + "\n",
                          encoding="utf-8")
    print(f"ER decomp OK: flips=41 caches=6747->6765 win=168->186 "
          f"closure_left={CLOSURE['left']} greedy={JOINT_GREEDY[0]}->{JOINT_GREEDY[1]} "
          f"decomp_sha={sha(DECOMP_OUT)}")


if __name__ == "__main__":
    main()
