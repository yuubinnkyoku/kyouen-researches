#!/usr/bin/env python3
"""BASE (canonical chain through the Part EM b38loss24 loss-only adoption)
vs SCENARIO (epwin10 = Part EP FIRST-EVER WIN canonical adoption).

Fail-closed machine recomputation of exactly what the Part EP win10
canonical adoption changed, from published bytes only:

* every artifact sha-pinned (BASE = the published Part EM outputs -- the
  merged canonical cache b5be64e6... 6,737 rows WIN 158 / LOSS 6,579, the
  reaudit outputs refresh-summary bacf6a68... / closure-classes 93a68897...
  / per-root-coverage bce9f8f1...; SCEN = the Part EP outputs -- increment
  c245bc4c... (10 s5verdict exact-WIN rows), increments-manifest 25d3abdf...
  (schema epwin10-increments-manifest-v1), the 6,747-row scenario cache
  fd29a337... WIN 168 / LOSS 6,579 (chain name
  merged-exact-s5-chain-plus-epwin10-20261125.cache; the sha pin carries the
  identity), the merge-audits x3 (identical sha efbe25bc...), the maker
  efc40a0b..., the byte-clones of the union merger 90711961... and both
  refresh forks (the published Part EM refresh baf9cbde... and the Part EP
  refresh fork 99d583c3...), the frozen graph/update8/board/policy/
  quarantine pins);
* the published Part EM refresh fork and the Part EP refresh fork are
  RE-EXECUTED byte-verbatim in isolated scratch trees against their pinned
  inputs, and all eight outputs must be byte-identical to the published /
  regenerated pins before any delta is emitted (double-run determinism; this
  simultaneously re-proves the published Part EM reaudit outputs are
  regenerable from published bytes);
* SCEN cache == BASE cache rows + exactly the 10 increment rows (verdict
  agreement everywhere; 6,747 rows, WIN 168 / LOSS 6,579); the adopted rows
  are ALL fresh exact-WIN rows: class 34908 af029/af047/af050/af053/af023/
  af048 and class 30484 aj030/aj049/aj050/ai048, adopted node total
  98,335,817.  Their eligibility was proven by the maker (gate kits EN/EO
  verified file-by-file against their pinned MANIFESTs; the manifest
  decomposition, every per-row pin MANIFEST-extracted, is re-verified here
  from the published EP manifest);
* the independent full-class census (frozen graph s4_cost + update8
  receipts + cache verdicts, replicating the refresh status logic) must
  reproduce the published class status counts EXACTLY on both sides (BASE
  34,497/23/39/390, SCEN 34,477/43/39/390) and identify EXACTLY 20 status
  flips, all UNKNOWN -> excluded_now, exactly the 20 classes whose s4_cost
  contains an adopted key: 25834, 25867, 27360, 29943, 29979, 30337, 30345,
  30354, 30469, 30483, 30484, 30493, 30542, 34765, 34771, 34799, 34867,
  34882, 34908, 34912 -- and ZERO other class changes;
* the class-30484 arithmetic is recomputed from the frozen dependency graph
  with the integer-geometry Board: the 54-child canonical boundary is
  regenerated (cost set == boundary, all in-universe); BASE held 50 known
  children and exactly 4 unknown (the probe-level WINs aj030/aj049/aj050/
  ai048); SCEN holds ZERO unknown (closure class FULLY KNOWN for the first
  time); the class flips to excluded_now (a known WIN cost child ends free
  all-LOSS coverage) - a scheduling-status fact, NOT a root verdict;
* the class-34908 arithmetic likewise: the 56-child boundary, 6 unknown in
  BASE (af029/af047/af050/af053/af023/af048), ZERO unknown in SCEN; the
  class flips to excluded_now;
* the class-30345 arithmetic: the 51-raw-child boundary (50 in-universe
  cost children) drops unknown 26 -> 25 (the dual-class sibling ai048 sits
  inside); the class flips to excluded_now; the in-flight Part EJ batch-40
  owner of this class is untouched by this recomputation;
* the class-30354 arithmetic: the 97-child boundary drops unknown 97 -> 96
  (ai048 dual-class sibling); the class flips to excluded_now;
* closure-classes.csv: exactly the two rows 30484 (rank 7, unknown 4) and
  34908 (rank 8, unknown 6) LEAVE the file; ZERO rows enter; among the 805
  common rows the only unknown_now change is 30345: 26 -> 25 and the only
  groups_served change is 16757: 5 -> 4; every other field of every common
  row is byte-identical except class_rank, which shifts by EXACTLY -2 for
  every row below the two departed (799 rows, a pure renumbering);
* update8 refresh: resolved 259 -> 260, remaining 31,600 -> 31,505,
  groups_free_now stays 131, union baseline stays 31,859, and exactly 10
  win_hit_groups ALL of s4 class 30354 -- the quartets (12,40,96,60),
  (12,80,96,60), (12,96,40,60), (24,40,108,60), (24,80,108,60),
  (24,108,40,60), (36,20,90,60), (36,30,100,60), (36,90,20,60),
  (36,100,30,60) -- all with unknown_s5_children 97 (their certificate
  option class lost one unknown child to a WIN);
* per-root coverage: free_now/uncovered thirds are IDENTICAL at every one
  of the 19 roots; Board verification 39/39 with zero rejections on both
  sides; the individual greedy union changes only at 5 roots
  (0: 3000->2981, 2: 6134->6133, 12: 2866->2868, 24: 2780->2776,
  36: 2975->3025 -- pure re-selection bookkeeping, no coverage claim);
* the frozen greedy scheduler deltas are recorded as bookkeeping (joint
  greedy 36,460 -> 36,643, group_best_options_nonfree 2,115 -> 2,105,
  worklist 64,339 -> 64,328).

No unknown verdict is asserted anywhere.  The standard 11x11 empty board
and every one of the 19 central-reply roots stay UNKNOWN; free_now /
coverage quantities are scheduling bookkeeping derived from exact verdicts,
not root verdict claims.  Consuming the 10 WIN labels transfers NO verdict
to any root: the two closure classes become excluded, which removes them
from the free-coverage option space and modestly ENLARGES the remaining
greedy union - recorded honestly below.  The k04 sixth-cost WIN (verified
by the Part EN gate but owned by another lane), the remaining batch-38
probe-level WIN rows, and every other unconsumed probe-level WIN stay in NO
cache; 11x11 stays UNKNOWN.
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

BASE_EXP = ROOT / "research/experiments/n11-centralreply-b38loss24-adoption-reaudit-20261125"
BASE_OUT = BASE_EXP / "reaudit/output"
BASE_CACHE = BASE_EXP / "output/merged-exact-s5-chain-plus-b38loss24-20261125.cache"
SCEN_CACHE = EXP / "output/merged-exact-s5-chain-plus-epwin10-20261125.cache"
INCR = EXP / "output/increment-epwin10-20261125.cache"
MANIFEST = EXP / "output/increments-manifest.json"
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_REFRESH_SCRIPT = BASE_EXP / "reaudit/scripts/refresh_adoption_em.py"
SCEN_REFRESH_SCRIPT = EXP / "reaudit/scripts/refresh_adoption_ep.py"
MERGER = EXP / "scripts/s5_union_merge.py"
MAKER = EXP / "scripts/make_increments_ep_win10_adoption.py"
DECOMP_OUT = EXP / "output/decomp-deltas-epwin10-adoption.json"

# ---- pins ------------------------------------------------------------------
BASE_CACHE_SHA = "b5be64e6b96af435ab589caced29273bab765085ba13c3033e897de13fab636c"
SCEN_CACHE_SHA = "fd29a33726e2e083998c67d83bf90822f84beebac30728ea79ea713e880cd1af"
INCR_SHA = "c245bc4c63fdd116f5d707736a4b06925c7e0c48df92993a21363a910e7de1f2"
MANIFEST_SHA = "25d3abdf4ab4b305d914e41739984bbc7f8dab2d7b83b1fc7fddcd0ca8e748be"
MAKER_SHA = "efc40a0bf7882bb7abc666a6d1c489a93938621d3e4ad1287a4818466e84e7a0"
BASE_SUMMARY_SHA = "bacf6a6848aa7cd857ed708f8bd908942d68f6d1b9068e6996cfd3cf41838f29"
BASE_CLOSURE_SHA = "93a6889772544bb26d2c1542e1c1487787c1d05934ca9d3a18f1c969f24241f1"
BASE_PRC_SHA = "bce9f8f1ac2a3c2caa3e7534041f6825263626fa03822f991521c6000e06838d"
BASE_WORKLIST_SHA = "b4d16b7f21b0f0bc92e6a1022211327f6d3e153f015630f40e9e1f9315cee488"
SCEN_SUMMARY_SHA = "5a1ff0c58acdb2bb96ae0eb0f2c5183fb9459afbacb3392ae08e005a313a3b01"
SCEN_CLOSURE_SHA = "fdd4e4b2ae08db14f2fe5f0d934a3f42a93cf687f348ef1f3074b677758ba38d"
SCEN_PRC_SHA = "487a95c48083b0626aba341e77eb80037be07104a3c7621ab2bac4e352816c57"
SCEN_WORKLIST_SHA = "7cd566bfa39a4211893156151ed976fa31e19ddfe0658de1afbf2b6757f0b004"
BASE_REFRESH_SHA = "baf9cbde6aa49949eb5a9668134dd3d6cfad7aee057ad61ea0a631b686a0ef78"
SCEN_REFRESH_SHA = "99d583c3e73657bb6bd2e6cfa55dfc73c83da3151c180c0252cccd464e2501aa"
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
MERGE_AUDIT_SHA = "efbe25bc7e09e8904281d10be06791203c3b0c33d73b3a99cd2bfce32b120754"
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
BOARD_SHA = "954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUARANTINE_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

ADOPTED = {
    "af023": (810351, 1152921504607895553, 68719478784),
    "af029": (900646, 1152921504607895553, 68720525312),
    "af047": (961976, 1152921504607895809, 68719476736),
    "af048": (962172, 1152921508902862849, 68719476736),
    "af050": (962386, 1152921504607899649, 68719476736),
    "af053": (962470, 1152921504606852096, 17660905521152),
    "ai048": (900718, 1152921573327372288, 68157440),
    "aj030": (892576, 1152922604135251976, 65536),
    "aj049": (902511, 1152921574400065536, 1114112),
    "aj050": (902512, 1152921574400065536, 68157440),
}
ADOPTED_NODES = 98335817
FLIP_CLASSES = [25834, 25867, 27360, 29943, 29979, 30337, 30345, 30354, 30469,
                30483, 30484, 30493, 30542, 34765, 34771, 34799, 34867, 34882,
                34908, 34912]
CENSUS_BEFORE = {"unknown": 34497, "excluded_now": 23, "free_now": 39, "excluded": 390}
CENSUS_AFTER = {"unknown": 34477, "excluded_now": 43, "free_now": 39, "excluded": 390}
WIN_HIT_QUARTETS = [(12, 40, 96, 60), (12, 80, 96, 60), (12, 96, 40, 60),
                    (24, 40, 108, 60), (24, 80, 108, 60), (24, 108, 40, 60),
                    (36, 20, 90, 60), (36, 30, 100, 60), (36, 90, 20, 60),
                    (36, 100, 30, 60)]
GREEDY_DELTA = {"0": (3000, 2981), "2": (6134, 6133), "12": (2866, 2868),
                "24": (2780, 2776), "36": (2975, 3025)}
JOINT_GREEDY = (36460, 36643)
GROUP_BEST_NONFREE = (2115, 2105)
WORKLIST_TOTAL = (64339, 64328)
UPD8 = {"resolved": (259, 260), "remaining": (31600, 31505), "free_groups": (131, 131)}
CLOSURE = {"rows": (807, 805), "left": [30484, 34908], "entered": []}


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
    if manifest["schema"] != "epwin10-increments-manifest-v1":
        fail("manifest schema drift")
    if manifest["win_canonical_adoption"] is not True:
        fail("manifest win_canonical_adoption flag drift")
    if manifest["base_cache_sha256"] != BASE_CACHE_SHA:
        fail("manifest base cache pin drift")
    if manifest["sha256"]["win_increment"] != INCR_SHA:
        fail("manifest win_increment pin drift")
    if manifest["merger_sha256"] != MERGER_SHA:
        fail("manifest merger pin drift")
    if manifest["base_cache_rows"] != 6737:
        fail("manifest base rows drift")
    rows = manifest["adopted_win_rows"]
    if len(rows) != 10 or manifest["adopted_ids"] != ["af029", "af047", "af050", "af053", "af023", "af048", "aj030", "aj049", "aj050", "ai048"]:
        fail("manifest adopted ids drift")
    if sum(r["nodes"] for r in rows) != ADOPTED_NODES:
        fail("manifest adopted node sum drift")
    for r in rows:
        kid = r["key_id"]
        ok = (kid in ADOPTED and
              (r["class"] == (34908 if kid.startswith("af") else 30484)) and
              (r["s5_index"], r["lo"], r["hi"]) == ADOPTED[kid] and
              r["result"] == 1 and r["nodes"] > 0)
        if not ok:
            fail(f"manifest adopted row drift: {kid}")
    if manifest["verdicts_out_of_scope_unconsumed"].get("k04_sixthcost_win") is None:
        fail("manifest must declare the k04 sixth-cost WIN out of scope")

    # --- cache relation: SCEN == BASE + exactly the 10 increment rows --------
    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    incr = load_cache(INCR)
    if len(base) != 6737 or len(scen) != 6747 or len(incr) != 10:
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
    if (wins, losses) != (168, 6579):
        fail(f"scenario verdict counts {wins}/{losses} != 168/6,579")
    if sum(v[1] for v in incr.values()) != ADOPTED_NODES:
        fail("increment node total drift")

    # --- refresh re-execution (double-run determinism) ----------------------
    base_tmp = rerun_refresh(BASE_REFRESH_SCRIPT, BASE_REFRESH_SHA, ".epverify-base-em")
    scen_tmp = rerun_refresh(SCEN_REFRESH_SCRIPT, SCEN_REFRESH_SHA, ".epverify-scen-ep")
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
    shutil.rmtree(ROOT / "research/experiments/.epverify-base-em")
    shutil.rmtree(ROOT / "research/experiments/.epverify-scen-ep")

    # --- independent full-class census --------------------------------------
    sys.path.insert(0, str(BOARD_SOURCE.parent))
    sys.path.insert(0, str(POLICY.parent))
    from independent import Board  # noqa: E402
    from s5_evidence_policy import quarantined_cache_keys, is_canonical_safe_s5_key  # noqa: E402
    quarantined = quarantined_cache_keys()
    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s4_masks, s4_status, s4_cost, s5_masks = g["s4_masks"], g["s4_status"], g["s4_cost"], g["s5_masks"]
    m2i = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}
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
    if sorted({c for v in owners.values() for c in v}) != sorted(FLIP_CLASSES):
        fail("adopted-key class membership != the 20 flipped classes")

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

    cls_30484 = check_class(30484, 54, 54, 4, 0,
                            ["ai048", "aj030", "aj049", "aj050"])
    cls_34908 = check_class(34908, 56, 56, 6, 0,
                            ["af023", "af029", "af047", "af048", "af050", "af053"])
    cls_30345 = check_class(30345, 51, 50, 26, 25, ["ai048"])
    cls_30354 = check_class(30354, 97, 97, 97, 96, ["ai048"])
    if cls_30484["status_scen"] != "excluded_now" or cls_34908["status_scen"] != "excluded_now":
        fail("the two closure classes must be excluded_now in SCEN")

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
    if {f: c_before[30484][f] for f in ("class_rank", "unknown_now", "groups_served_count")} != \
            {"class_rank": "7", "unknown_now": "4", "groups_served_count": "4"}:
        fail("closure 30484 BASE row drift")
    if {f: c_before[34908][f] for f in ("class_rank", "unknown_now", "groups_served_count")} != \
            {"class_rank": "8", "unknown_now": "6", "groups_served_count": "5"}:
        fail("closure 34908 BASE row drift")
    common = set(c_before) & set(c_after)
    rank_shift_rows = 0
    for c in sorted(common):
        b, a = c_before[c], c_after[c]
        ro, rn = int(b["class_rank"]), int(a["class_rank"])
        if ro <= 6:
            if rn != ro:
                fail(f"closure rank churn above the departed rows at class {c}")
        elif ro >= 9:
            if rn != ro - 2:
                fail(f"closure rank shift for class {c}: {ro}->{rn}")
            rank_shift_rows += 1
        else:
            fail(f"common row with a departed rank: class {c} rank {ro}")
        for f in ("class_lo", "class_hi"):
            if b[f] != a[f]:
                fail(f"closure field {f} churn at class {c}")
        if b["unknown_now"] != a["unknown_now"] and c != 30345:
            fail(f"closure unknown_now churn at class {c}")
        if b["groups_served_count"] != a["groups_served_count"] and c != 16757:
            fail(f"closure groups_served churn at class {c}")
    if c_before[30345]["unknown_now"] != "26" or c_after[30345]["unknown_now"] != "25":
        fail("closure 30345 unknown 26->25 drift")
    if c_after[30345]["groups_served_count"] != c_before[30345]["groups_served_count"]:
        fail("closure 30345 groups_served drift")
    if c_before[16757]["groups_served_count"] != "5" or c_after[16757]["groups_served_count"] != "4":
        fail("closure 16757 groups served 5->4 drift")
    if rank_shift_rows != 799:
        fail(f"closure common-row count {rank_shift_rows} != 799")

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
    if ub_["win_hit_groups"] != []:
        fail("BASE win_hit groups must be empty")
    got_q = sorted((w["first"], w["third"], w["fourth"], w["reply"]) for w in ua_["win_hit_groups"])
    if got_q != sorted(WIN_HIT_QUARTETS):
        fail(f"SCEN win_hit quartets drift: {got_q}")
    if any(w["s4_class_index"] != 30354 or w["unknown_s5_children"] != 97 for w in ua_["win_hit_groups"]):
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
        "schema": "epwin10-decomp-deltas-v1",
        "part": "EP",
        "date": "2026-11-25",
        "base": {
            "cache_sha256": BASE_CACHE_SHA,
            "rows": 6737, "win": 158, "loss": 6579,
            "refresh_summary_sha256": BASE_SUMMARY_SHA,
            "closure_classes_sha256": BASE_CLOSURE_SHA,
            "per_root_coverage_sha256": BASE_PRC_SHA,
            "class_status_counts": CENSUS_BEFORE,
        },
        "scen": {
            "cache_sha256": SCEN_CACHE_SHA,
            "rows": 6747, "win": 168, "loss": 6579,
            "increment_sha256": INCR_SHA,
            "manifest_sha256": MANIFEST_SHA,
            "refresh_summary_sha256": SCEN_SUMMARY_SHA,
            "closure_classes_sha256": SCEN_CLOSURE_SHA,
            "per_root_coverage_sha256": SCEN_PRC_SHA,
            "probe_worklist_regen_pin_sha256": SCEN_WORKLIST_SHA,
            "probe_worklist_not_published_size_policy_bytes": 3718981,
            "class_status_counts": CENSUS_AFTER,
        },
        "adopted": {
            "ids": list(ADOPTED),
            "nodes_total": ADOPTED_NODES,
            "classes": {"34908": 6, "30484": 4},
        },
        "class_flips": {
            "count": 20,
            "direction": "unknown->excluded_now",
            "classes": flipped,
            "per_key_owner_classes": {k: owners[k] for k in sorted(owners)},
        },
        "closure_classes": {
            "rows_before_after": list(CLOSURE["rows"]),
            "left_rows": {"30484": dict(c_before[30484]), "34908": dict(c_before[34908])},
            "entered_rows": [],
            "rank_shift": {"rows": 799, "delta": -2, "nature": "pure renumbering below the two departed rows"},
            "unknown_churn": {"30345": ["26", "25"]},
            "groups_served_churn": {"16757": ["5", "4"]},
            "class_30484": cls_30484,
            "class_34908": cls_34908,
            "class_30345": cls_30345,
            "class_30354": cls_30354,
        },
        "frozen_update8": {
            "union_baseline": 31859,
            "resolved": list(UPD8["resolved"]),
            "remaining_now": list(UPD8["remaining"]),
            "groups_free_now": list(UPD8["free_groups"]),
            "win_hit_groups_base": [],
            "win_hit_groups_scen": [{"first": w[0], "third": w[1], "fourth": w[2],
                                     "reply": w[3], "s4_class_index": 30354,
                                     "unknown_s5_children": 97} for w in WIN_HIT_QUARTETS],
        },
        "per_root": {
            "free_now_uncovered": "identical at all 19 central roots + root 27 baseline 119/119",
            "greedy_union_changes": {k: list(v) for k, v in sorted(GREEDY_DELTA.items(), key=lambda kv: int(kv[0]))},
            "joint_greedy": list(JOINT_GREEDY),
            "group_best_options_nonfree": list(GROUP_BEST_NONFREE),
            "worklist_total": list(WORKLIST_TOTAL),
        },
        "honesty": {
            "first_ever_win_adoption": True,
            "no_root_verdict": "no 19-root verdict is asserted or implied by any class flip",
            "exclusion_effect": "classes 30484/34908 become excluded (known WIN child ends free all-LOSS coverage): remaining greedy union grows 36,460 -> 36,643 (+183) and worklist shrinks 64,339 -> 64,328 (-11): scheduling bookkeeping only",
            "unknown_still": "34,477 S4 classes remain status-unknown; 11x11 stays UNKNOWN",
            "out_of_scope_unconsumed": ["k04 sixth-cost WIN", "remaining batch-38 probe WIN rows",
                                         "all other probe-level WINs"],
            "nodes_are_bookkeeping": True,
        },
    }
    DECOMP_OUT.write_text(json.dumps(decomp, indent=1, ensure_ascii=False, sort_keys=True) + "\n",
                          encoding="utf-8")
    print(f"EP decomp OK: flips=20 caches=6737->6747 win=158->168 "
          f"closure_left={CLOSURE['left']} greedy={JOINT_GREEDY[0]}->{JOINT_GREEDY[1]} "
          f"decomp_sha={sha(DECOMP_OUT)}")


if __name__ == "__main__":
    main()
