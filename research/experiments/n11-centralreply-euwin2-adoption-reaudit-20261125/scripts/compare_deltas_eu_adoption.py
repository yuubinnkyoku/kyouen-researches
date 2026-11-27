#!/usr/bin/env python3
"""BASE (canonical chain through the Part ER erwin18 second WIN adoption)
vs SCENARIO (euwin2 = Part EU third WIN canonical adoption: the 2 ES-30M-
resolved closure-class-30345 exact-WIN rows, ET-C++-gate-verified).

Fork of the published Part ER extractor
`compare_deltas_er_adoption.py` (sha256 c3e82eaa...; structural clone,
disclosed diff: the adopted-rows table, both refresh sides, the manifest
decomposition fields and the pinned expectations are Part-EU specific).

Fail-closed machine recomputation of exactly what the Part EU win2
canonical adoption changed, from published bytes only:

* every artifact sha-pinned (BASE = the published Part ER outputs -- the
  merged canonical cache 9c4dd94e... 6,765 rows WIN 186 / LOSS 6,579, the
  reaudit outputs refresh-summary a6b8d082... / closure-classes 4c03f965...
  / per-root-coverage 1bf6c25a... and worklist regen pin 78e499dd...;
  SCEN = the Part EU outputs -- increment d9365d80... (2 s5verdict
  exact-WIN rows), increments-manifest 793f68c5... (schema
  euwin2-increments-manifest-v1), the 6,767-row scenario cache 3ba48608...
  WIN 188 / LOSS 6,579 (chain name
  merged-exact-s5-chain-plus-euwin2-20261125.cache; the sha pin carries the
  identity), the merge-audits x3 (identical sha 9f807c95...), the maker
  f2ae97a1..., the byte-clone of the union merger 90711961... and both
  refresh forks (the published Part ER refresh 6c91e0ce... and the
  disclosed-repair Part EU refresh fork 6dc24c15... - the declaration's
  original a377eea0... pin pointed at never-published bytes and was
  superseded 2026-11-26 by the disclosed 3-region-diff repair fork),
  the frozen graph/update8/board/policy/quarantine pins, and the batch-38 SSOT batch-keys 29807104...);
  both probe-worklists are UNPUBLISHED per the size policy - they enter ONLY
  as regen pins (BASE 78e499dd... 3,717,828 B / SCEN 397a4379... 3,717,712 B)
  re-verified by the byte-verbatim refresh re-execution;
* the published Part ER refresh fork and the Part EU refresh fork are
  RE-EXECUTED byte-verbatim in isolated scratch trees against their pinned
  inputs, and all eight outputs must be byte-identical to the published /
  regenerated pins before any delta is emitted (double-run determinism;
  this simultaneously re-proves the published Part ER reaudit outputs are
  regenerable from published bytes);
* SCEN cache == BASE cache rows + exactly the 2 increment rows (verdict
  agreement everywhere; 6,767 rows, WIN 188 / LOSS 6,579); the adopted rows
  are ALL fresh exact-WIN rows of closure class 30345 (ai007 ai040,
  adopted node total 36,801,516 -- the two of the six batch-38
  honest-EXHAUSTED keys that the Part ES 30M re-probe resolved as WIN,
  re-verified node-identical by the Part ET C++ scrutiny gate, audit
  2c6d7441..., 9/9 GATE-PASS, 4 byte-identical runs).  Their eligibility
  was proven by the maker against the byte-verified Part ES (38 entries),
  Part ET (38 entries) and batch-38 (181 entries) kits: every manifest row
  is re-verified here against the b38 SSOT (lo/hi/s5_index per key), and
  the adopted set must equal the ES-30M raw-derived WIN disposition of the
  re-derived 6-key honest-EXHAUSTED pool, exactly; the 18 Part-ER adopted
  rows must already sit WIN in BASE (regression tie, NOT re-adopted);
* the independent full-class census (frozen graph s4_cost + update8
  receipts + cache verdicts, replicating the refresh status logic) must
  reproduce the published class status counts EXACTLY on both sides (BASE
  34,436/84/39/390, SCEN 34,430/90/39/390) and identify EXACTLY 6 status
  flips, all UNKNOWN -> excluded_now, exactly the owner classes of the
  adopted keys that were still unknown (the further owner class 30345 was
  already excluded_now from the Part EP adoption via ai048 and must NOT
  double-flip);
* the class-30345 arithmetic is recomputed from the frozen dependency graph
  with the integer-geometry Board: the 51-raw-child boundary (50
  in-universe cost children) drops unknown 7 -> 5 (both members consumed
  here; the class already flipped to excluded_now at Part EP via ai048 and
  stays excluded_now - a scheduling-status fact, NOT a root verdict);
* the six flipped owner classes' arithmetic: the Board boundary / cost
  size / cost-unknown drop of each (exactly one adopted member each:
  ai007 in 12846/12875/13801, ai040 in 30282/30308/30326), from
  unknown -> excluded_now;
* the class-30354 arithmetic (no adopted member): 97-child boundary, 97
  cost children, unknown stays 96 -> 96 (its one WIN child ai048 was
  already EP-consumed; the class stays excluded_now);
* closure-classes.csv: ZERO rows leave, ZERO rows enter (805 -> 805); the
  only unknown_now churn is 30345: 7 -> 5; NO groups_served churn
  anywhere; the only class_rank churn is the exact two-row swap-set
  {30345: 8->7, 20421: 7->8}; every other field of every row is
  byte-identical;
* update8 refresh: resolved stays 260, remaining stays 31,505,
  groups_free_now stays 131, union baseline stays 31,859, and the win_hit
  groups are UNCHANGED: exactly 10 groups ALL of s4 class 30354 -- the
  quartets (12,40,96,60), (12,80,96,60), (12,96,40,60), (24,40,108,60),
  (24,80,108,60), (24,108,40,60), (36,20,90,60), (36,30,100,60),
  (36,90,20,60), (36,100,30,60) -- all with unknown_s5_children 97 on BOTH
  sides (the EU adoption consumes no child of 30354);
* per-root coverage: free_now/uncovered thirds are IDENTICAL at every one
  of the roots; Board verification 39/39 with zero rejections on both
  sides; the individual greedy union changes only at 2 roots
  (12: 2850->2848, 36: 3007->3005 -- pure re-selection bookkeeping, no
  coverage claim);
* the frozen greedy scheduler deltas are recorded as bookkeeping (joint
  greedy stays 36,619, group_best_options_nonfree stays 2,105, worklist
  64,309 -> 64,307).

No unknown verdict is asserted anywhere.  The standard 11x11 empty board
and every central-reply root stay UNKNOWN; free_now / coverage quantities
are scheduling bookkeeping derived from exact verdicts, not root verdict
claims.  Consuming the 2 WIN labels transfers NO verdict to any root: 6
classes become excluded (a known WIN cost child ends free all-LOSS
coverage), which removes them from the free-coverage option space -
recorded honestly below.  The 4 ES-30M-resolved LOSS rows
(ai024/ai030/ai038/ai041) stay unconsumed (EM-pattern territory); the b38
15M honest-EXHAUSTED label of every pool key stays honest UNKNOWN at 15M;
b018, the k04 sixth-cost WIN, and every other unconsumed probe-level WIN
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

BASE_EXP = ROOT / "research/experiments/n11-centralreply-erwin18-adoption-reaudit-20261125"
BASE_OUT = BASE_EXP / "reaudit/output"
BASE_CACHE = BASE_EXP / "output/merged-exact-s5-chain-plus-erwin18-20261125.cache"
BASE_INCREMENT = BASE_EXP / "output/increment-erwin18-20261125.cache"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-euwin2-20261125.cache"
INCR = EXP / "output/increment-euwin2-20261125.cache"
MANIFEST = EXP / "output/increments-manifest.json"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
B38_KEYS = ROOT / "research/experiments/n11-centralreply-closure-class30345-batch38-20261125/input/batch-keys-b38.json"
BASE_REFRESH_SCRIPT = BASE_EXP / "reaudit/scripts/refresh_adoption_er.py"
SCEN_REFRESH_SCRIPT = EXP / "reaudit/scripts/refresh_adoption_eu.py"
MERGER = EXP / "scripts/s5_union_merge.py"
MAKER = EXP / "scripts/make_increments_eu_win2_adoption.py"
DECOMP_OUT = EXP / "output/decomp-deltas-euwin2-adoption.json"

# ---- pins ------------------------------------------------------------------
BASE_CACHE_SHA = "9c4dd94e61b6ee724a966ecc9552e527ba5a7107de732f0e9c5ced33bdad4a5a"
SCEN_CACHE_SHA = "3ba486086703b9f44a0c685d7d5b45fab80f86760f2cd032a8dc18a2690233d6"
INCR_SHA = "d9365d80a90aff30cb451f8f2519ab2cc004c6d10ba4fb149a7ee340e0aa0b4f"
MANIFEST_SHA = "793f68c5651f3bc94f58acce753cd55c3c8e2cd33f4abea9dabbe9702715e82f"
MAKER_SHA = "f2ae97a135af1d7f14b376e5c9d41142025b6a2b4b161ce907cca9cb0356f498"
BASE_SUMMARY_SHA = "a6b8d0824e21e3d4f37bdd32a26dd8146234afb5a83f67f2734c1a83b99e1317"
BASE_CLOSURE_SHA = "4c03f965a717a80cf2ce9980de8d2658c316891ae8fb83e8d9e62d84b14b4c14"
BASE_PRC_SHA = "1bf6c25a2bdd7506bc5762acddc2f86aac2faf333e3d41d7b9c9fe4afb1c644a"
BASE_WORKLIST_SHA = "78e499dd5553c99b2c1ec09ba3d8071ea72cc5ed065ba4578316bddfe8084996"
SCEN_SUMMARY_SHA = "2b70bb55b25635f78e2cdd9559d8eab30d9c98640e5507ad280c6a510d958477"
SCEN_CLOSURE_SHA = "59a4c85fdd25a8d161bfb46598a8f8c77a684c996d456ba85b125f840134bf0e"
SCEN_PRC_SHA = "cfc2bfe15508c4d0c3455ca2f2abedd2a233d01118dbae95353bdc5b79f8e47f"
SCEN_WORKLIST_SHA = "397a43794be60442725825371a5cfba9c2744a69b8f5d32cb3a3f313ced29ba6"
BASE_REFRESH_SHA = "6c91e0ceaee03592f18ca1c36130d868cc7221bbe1819b803c4ba12b917a6061"
SCEN_REFRESH_SHA = "6dc24c15e0ddfa9043d715dd09a794819ef0c393fe15d0491c5beb04042e9fad"
# REPAIR (2026-11-26, disclosed decision log
# research/log/2026-11-26-part-eu-scen-refresh-pin-repair.md): the Part EU
# declaration (7136d22c) pre-registered SCEN_REFRESH_SHA =
# a377eea0cf5fac65fc248a7d50b5b8672c442dd9f26a80d3cd2cb08954ba067c
# (the declaring session's pre-declaration exploration fork).  Those bytes
# were never published (wave B carried only the three kit scripts) and are
# unrecoverable (declaring environment gone; repo-wide search finds only
# this pin).  Superseded by the published disclosed-repair fork
# reaudit/scripts/refresh_adoption_eu.py: a byte-clone of the published
# Part ER refresh 6c91e0ce... differing in EXACTLY the three declared
# regions (CACHE path, expected cache sha, docstring); all computation
# bytes identical.  All four refresh output pins pre-registered by the
# declaration are docstring-insensitive and unchanged; the declared
# post-conditions remain authoritative.
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
MERGE_AUDIT_SHA = "9f807c95e71a3da1f4d3d958cdf87f5f31f2bd1c961a1b105b63368fa0b159ce"
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
BOARD_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
B38_KEYS_SHA = "298071046bfba8473c5b3d6e0b6a30108697eb0899aed7c70fcb4c5343f7cb8d"
ER_INCREMENT_SHA = "4f6b7797df3bb950703f95e7ec72f288a447434da5b4ccf3d6d94ee8d8d6ffc1"
ER_MANIFEST_SHA = "48b71d6af77306a94bd561f625838cff70cd94f12d702bcda0e945b67237450a"

ES_KIT_MANIFEST_SHA = "cc9877399ab18dddad1250a359d13d834849aceb4ff6d54612a79bf72a615819"
ET_KIT_MANIFEST_SHA = "f0c1c27a830448dca3cd9c17cfb0f225293bc19f402e7c16710bd32572b449c8"
ET_REGISTRY_SHA = "6cf057ba2320a9d7be55e53edd9be2b65e41f552af206010899793a5b6a659c5"
ET_AUDIT_SHA = "2c6d7441d6f752f160efbe7e275b807ff174d8cd70ece3c85aed135ead11c0d0"
ET_AUDIT_SCHEMA = "n11-centralreply-cppgate-30345es6-audit-v1"
ET_GATE_SOURCE_SHA = "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e"
ET_GATE_STATUS_PASS = 9
ET_BUDGET = 30000000
B38_MANIFEST_SHA = "4dbf8856597709b3bd41d6f185a0502ebbdee447b1fc48d0caab586fdcc5ac02"

ADOPTED = {
    "ai007": (441292, 1152922604118478880, 65536),
    "ai040": (899584, 1152922604118487040, 65536),
}
ADOPTED_IDS = ["ai007", "ai040"]
POOL_IDS = ["ai007", "ai024", "ai030", "ai038", "ai040", "ai041"]
LOSS_IDS = ["ai024", "ai030", "ai038", "ai041"]
ADOPTED_NODES = 36801516
ADOPTED_ROW_NODES = {"ai007": 16090493, "ai040": 20711023}
FLIP_CLASSES = [12846, 12875, 13801, 30282, 30308, 30326]
PREV_EXCLUDED_OWNERS = [30345]
CENSUS_BEFORE = {"unknown": 34436, "excluded_now": 84, "free_now": 39, "excluded": 390}
CENSUS_AFTER = {"unknown": 34430, "excluded_now": 90, "free_now": 39, "excluded": 390}
WIN_HIT_QUARTETS = [(12, 40, 96, 60), (12, 80, 96, 60), (12, 96, 40, 60),
                    (24, 40, 108, 60), (24, 80, 108, 60), (24, 108, 40, 60),
                    (36, 20, 90, 60), (36, 30, 100, 60), (36, 90, 20, 60),
                    (36, 100, 30, 60)]
GREEDY_DELTA = {"12": (2850, 2848), "36": (3007, 3005)}
JOINT_GREEDY = (36619, 36619)
GROUP_BEST_NONFREE = (2105, 2105)
WORKLIST_TOTAL = (64309, 64307)
UPD8 = {"resolved": (260, 260), "remaining": (31505, 31505), "free_groups": (131, 131)}
CLOSURE = {"rows": (805, 805), "left": [], "entered": []}
CLOSURE_UNKNOWN_CHURN = {30345: ("7", "5")}
CLOSURE_RANK_CHURN = {30345: (8, 7), 20421: (7, 8)}
# per-class boundary expectations: class -> (raw_boundary, cost_size,
#   unknown_before, unknown_after, adopted_members)
CLASS_CHECKS = {
    30345: (51, 50, 7, 5, ["ai007", "ai040"]),
    12846: (103, 102, 102, 101, ["ai007"]),
    12875: (109, 109, 109, 108, ["ai007"]),
    13801: (103, 103, 99, 98, ["ai007"]),
    30282: (105, 105, 105, 104, ["ai040"]),
    30308: (107, 107, 103, 102, ["ai040"]),
    30326: (108, 108, 108, 107, ["ai040"]),
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
        ("base (ER) increment", BASE_INCREMENT, ER_INCREMENT_SHA),
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
    if manifest["schema"] != "euwin2-increments-manifest-v1":
        fail("manifest schema drift")
    if manifest["part"] != "EU" or manifest["date"] != "2026-11-25":
        fail("manifest part/date drift")
    if manifest["win_canonical_adoption"] is not True:
        fail("manifest win_canonical_adoption flag drift")
    if manifest["base_cache_sha256"] != BASE_CACHE_SHA:
        fail("manifest base cache pin drift")
    if manifest["sha256"]["win_increment"] != INCR_SHA:
        fail("manifest win_increment pin drift")
    if manifest["merger_sha256"] != MERGER_SHA:
        fail("manifest merger pin drift")
    if manifest["base_cache_rows"] != 6765:
        fail("manifest base rows drift")
    if manifest["row_counts"] != {"adopted_win_rows": 2,
                                  "exhausted_honest_unknown_rows": 0,
                                  "prior_canonical_rows_base": 6765,
                                  "loss_rows_this_pool": 4}:
        fail("manifest row_counts drift")
    if manifest["adopted_ids"] != ADOPTED_IDS or manifest["resolved_ids"] != POOL_IDS:
        fail("manifest adopted/resolved ids drift")
    if manifest["adopted_nodes_per_pool"] != ADOPTED_NODES:
        fail("manifest adopted node pool drift")
    ert = manifest["er_regression_tie"]
    if ert["er_increment_sha256"] != ER_INCREMENT_SHA or \
            ert["er_manifest_sha256"] != ER_MANIFEST_SHA or \
            ert["adopted_rows_win_in_base"] != 18 or not ert.get("note"):
        fail("manifest ER regression tie drift")
    if manifest["quarantine_hits"] != 0:
        fail("manifest quarantine hits drift")
    if manifest["base_cache_absent_hits_for_emitted"] != 2:
        fail("manifest base-absent hits drift")
    rows = manifest["adopted_win_rows"]
    if len(rows) != 2:
        fail("manifest adopted row count drift")
    if sum(r["nodes"] for r in rows) != ADOPTED_NODES:
        fail("manifest adopted node sum drift")
    for r in rows:
        kid = r["key_id"]
        ok = (kid in ADOPTED and
              r["class"] == 30345 and
              (r["s5_index"], r["lo"], r["hi"]) == ADOPTED[kid] and
              r["result"] == 1 and
              r["budget"] == ET_BUDGET and
              r["nodes"] == ADOPTED_ROW_NODES[kid] and
              r["gate_kit"] == "et" and
              r["source_kit"] == "es" and
              r["source_dir"] == "output/raw" and
              r["gate_input_sha256"] and
              r["gate_raw_p1_sha256"] and
              r["gate_raw_p2_sha256"] and
              r["source_input_sha256"] and
              r["source_raw_p1_sha256"] and
              r["source_raw_p2_sha256"] and
              r["b38_basis"]["kit"] == "b38" and
              r["b38_basis"]["condition_budget"] == 15000000 and
              r["b38_basis"]["honest_disposition"].startswith("EXHAUSTED") and
              r["b38_basis"]["raw_p1_sha256"] and
              r["b38_basis"]["raw_p2_sha256"])
        if not ok:
            fail(f"manifest adopted row drift: {kid}")
    prov = manifest["provenance"]
    if prov["es_kit_manifest_sha256"] != ES_KIT_MANIFEST_SHA or \
            prov["et_kit_manifest_sha256"] != ET_KIT_MANIFEST_SHA or \
            prov["et_registry_sha256"] != ET_REGISTRY_SHA or \
            prov["et_audit_sha256"] != ET_AUDIT_SHA or \
            prov["et_audit_schema"] != ET_AUDIT_SCHEMA or \
            prov["et_gate_status_pass"] != ET_GATE_STATUS_PASS or \
            prov["et_gate_source_sha256"] != ET_GATE_SOURCE_SHA or \
            prov["et_audit_reruns_byte_identical"] != 3 or \
            prov["b38_manifest_sha256"] != B38_MANIFEST_SHA or \
            prov["b38_keys_sha256"] != B38_KEYS_SHA:
        fail("manifest provenance ES/ET/b38 pin drift")
    if "38 + 38 + 181" not in prov["kit_integrity"]:
        fail("manifest kit integrity note drift")
    dispo = manifest["pool_derivation"]
    if dispo["win_derived"] != ADOPTED_IDS or dispo["loss_derived"] != LOSS_IDS:
        fail("manifest ES-30M disposition drift")
    if dispo["targets_adopted_here"] != ADOPTED_IDS:
        fail("manifest targets drift")
    if "same-condition ban untouched" not in dispo["resolution"]:
        fail("manifest resolution disclosure drift")
    # cross-verify every adopted row against the batch-38 SSOT
    b38 = json.loads(B38_KEYS.read_text())["keys"]
    ssot = {k["key_id"]: k for k in b38}
    for kid in POOL_IDS:
        k = ssot[kid]
        if int(k["serving_class"]) != 30345:
            fail(f"b38 SSOT serving_class drift for {kid}")
    for kid in ADOPTED_IDS:
        k = ssot[kid]
        if (int(k["s5_index"]), int(k["lo"]), int(k["hi"])) != ADOPTED[kid]:
            fail(f"b38 SSOT lo/hi/s5_index drift for {kid}")
    oos = manifest["verdicts_out_of_scope_unconsumed"]
    for key in ("es6_30m_resolved_loss_rows", "b38_15m_exhausted_labels", "b018",
                "k04_sixthcost_win", "other_closure_wins"):
        if not oos.get(key):
            fail(f"manifest must declare the out-of-scope entry: {key}")
    if "UNKNOWN" not in manifest["interpretation_guard"]:
        fail("manifest interpretation guard drift")

    # --- refresh re-execution (double-run determinism; runs BEFORE the heavy
    # graph load in the parent so the two processes never co-resident the
    # graph - only the verify guarantees differ in no way) -------------------
    base_tmp = rerun_refresh(BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA, ".eu-verify-base-er")
    scen_tmp = rerun_refresh(SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA, ".eu-verify-scen-eu")
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
    shutil.rmtree(ROOT / "research/experiments/.eu-verify-base-er")
    shutil.rmtree(ROOT / "research/experiments/.eu-verify-scen-eu")

    # --- frozen dependency graph + cache relation ---------------------------
    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s5_masks = g["s5_masks"]
    m2i_probe = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}

    # --- cache relation: SCEN == BASE + exactly the 2 increment rows --------
    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    incr = load_cache(INCR)
    if len(base) != 6765 or len(scen) != 6767 or len(incr) != 2:
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
    if (wins, losses) != (188, 6579):
        fail(f"scenario verdict counts {wins}/{losses} != 188/6,579")
    if sum(v[1] for v in incr.values()) != ADOPTED_NODES:
        fail("increment node total drift")
    # ER regression tie: all 18 Part-ER adopted rows must already sit WIN in
    # BASE with identical nodes; none may be re-adopted here
    er_inc = load_cache(BASE_INCREMENT)
    if len(er_inc) != 18:
        fail("ER increment row count drift")
    for key, row in er_inc.items():
        if base.get(key) is None or base[key][0] != 1 or row[0] != 1:
            fail(f"ER regression tie broken: {key} not WIN in BASE")
        if base[key][1] != row[1]:
            fail(f"ER regression nodes tie broken: {key}")
        if key in incr:
            fail("a Part-ER row must NOT be re-adopted by EU")

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
        fail(f"adopted-key owner union != 6 flips + the EP-pre-excluded 30345: {owner_union}")
    for i in PREV_EXCLUDED_OWNERS:
        if cb[i][0] != "excluded_now" or ca[i][0] != "excluded_now":
            fail(f"EP-pre-excluded owner class {i} must stay excluded_now on both sides")
    if sorted(owners["ai007"]) != [12846, 12875, 13801, 30345] or \
            sorted(owners["ai040"]) != [30282, 30308, 30326, 30345]:
        fail("per-key owner class sets drift")

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
        fail("class 30345 must be excluded_now on both sides (EP flipped it)")
    for cls in FLIP_CLASSES:
        if cls_records[cls]["status_base"] != "unknown" or \
                cls_records[cls]["status_scen"] != "excluded_now":
            fail(f"class {cls} must flip unknown -> excluded_now")
    if cls_records[30354]["status_base"] != "excluded_now" or \
            cls_records[30354]["status_scen"] != "excluded_now":
        fail("class 30354 must stay excluded_now (EP-flipped, no EU member)")

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
    # win_hit groups unchanged ER -> EU: both sides hold the same 10 groups
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
        "schema": "euwin2-decomp-deltas-v1",
        "part": "EU",
        "date": "2026-11-25",
        "base": {
            "cache_sha256": BASE_CACHE_SHA,
            "rows": 6765, "win": 186, "loss": 6579,
            "refresh_summary_sha256": BASE_SUMMARY_SHA,
            "closure_classes_sha256": BASE_CLOSURE_SHA,
            "per_root_coverage_sha256": BASE_PRC_SHA,
            "probe_worklist_sha256": BASE_WORKLIST_SHA,
            "class_status_counts": CENSUS_BEFORE,
        },
        "scen": {
            "cache_sha256": SCEN_CACHE_SHA,
            "rows": 6767, "win": 188, "loss": 6579,
            "increment_sha256": INCR_SHA,
            "manifest_sha256": MANIFEST_SHA,
            "refresh_summary_sha256": SCEN_SUMMARY_SHA,
            "closure_classes_sha256": SCEN_CLOSURE_SHA,
            "per_root_coverage_sha256": SCEN_PRC_SHA,
            "probe_worklist_regen_pin_sha256": SCEN_WORKLIST_SHA,
            "probe_worklist_not_published_size_policy_bytes": 3717712,
            "class_status_counts": CENSUS_AFTER,
        },
        "adopted": {
            "ids": list(ADOPTED),
            "nodes_total": ADOPTED_NODES,
            "classes": {"30345": 2},
            "condition": "ES 30M re-probe resolution (b38 15M honest-EXHAUSTED basis; same-condition ban untouched)",
            "gate": "Part ET C++ second implementation, audit 2c6d7441..., 9/9 GATE-PASS, 4/4 byte-identical runs",
        },
        "class_flips": {
            "count": 6,
            "direction": "unknown->excluded_now",
            "classes": flipped,
            "per_key_owner_classes": {k: sorted(owners[k]) for k in sorted(owners)},
            "owner_union_nonflip_classes": {"30345": "excluded_now (EP flip via ai048)"},
        },
        "closure_classes": {
            "rows_before_after": list(CLOSURE["rows"]),
            "left_rows": [],
            "entered_rows": [],
            "rank_churn": {str(k): list(v) for k, v in sorted(CLOSURE_RANK_CHURN.items())},
            "rank_churn_nature": "30345 rises 8->7 (unknown_now 7->5) displacing 20421 down 7->8; no renumbering elsewhere",
            "unknown_churn": {"30345": ["7", "5"]},
            "groups_served_churn": {},
            "class_30345": cls_records[30345],
            "class_12846": cls_records[12846],
            "class_12875": cls_records[12875],
            "class_13801": cls_records[13801],
            "class_30282": cls_records[30282],
            "class_30308": cls_records[30308],
            "class_30326": cls_records[30326],
            "class_30354": cls_records[30354],
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
            "third_win_adoption": True,
            "no_root_verdict": "no root verdict is asserted or implied by any class flip",
            "exclusion_effect": "6 classes become excluded (known WIN cost child ends free all-LOSS coverage): joint greedy stays 36,619 (the 6 flipped classes serve no closure group), worklist shrinks 64,309 -> 64,307 (-2), individual greedy shrinks -2 at each of roots 12 and 36: scheduling bookkeeping only",
            "unknown_still": "34,430 S4 classes remain status-unknown; 11x11 stays UNKNOWN",
            "out_of_scope_unconsumed": ["the 4 ES-30M-resolved LOSS rows (ai024/ai030/ai038/ai041; EM-pattern territory)",
                                        "b38 15M honest-EXHAUSTED labels (honest UNKNOWN at the 15M condition, untouched)",
                                        "b018 probe-level WIN (dual-class, scrutiny-owner pending)",
                                        "k04 sixth-cost WIN", "all other probe-level WINs"],
            "nodes_are_bookkeeping": True,
        },
    }
    DECOMP_OUT.write_text(json.dumps(decomp, indent=1, ensure_ascii=False, sort_keys=True) + "\n",
                          encoding="utf-8")
    print(f"EU decomp OK: flips=6 caches=6765->6767 win=186->188 "
          f"closure_left={CLOSURE['left']} greedy={JOINT_GREEDY[0]}->{JOINT_GREEDY[1]} "
          f"decomp_sha={sha(DECOMP_OUT)}")


if __name__ == "__main__":
    main()
