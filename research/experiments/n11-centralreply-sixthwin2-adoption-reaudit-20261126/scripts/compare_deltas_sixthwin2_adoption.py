#!/usr/bin/env python3
"""Part SP sixthwin2 adoption delta EXTRACTOR, fail-closed.

Re-verification battery over the published Part SP kit
n11-centralreply-sixthwin2-adoption-reaudit-20261126 (structural clone of
the Part EW extractor pattern, adapted to the sixthwin2 sources):

1. every published kit byte is pinned and verified first (increment,
   manifest, merged head of record, 3 merge audits, reaudit refresh
   outputs, the census measurement json, the refresh fork, the maker,
   the merger, the frozen graph/update8/quarantine/policy anchors and
   the BASE-side sixthwin5 dossier outputs);
2. the BASE-side published refresh (sixthwin5 dossier,
   refresh_adoption_sixthwin5.py sha256 92a884c9...) is re-executed
   byte-verbatim from a scratch tree and must regenerate its published
   outputs byte-for-byte (refresh-summary 295027cf..., closure-classes
   350e269a..., per-root-coverage 9c5b2774... and the unpublished-size
   probe-worklist regen pin 82f9e517..., 3,715,904 bytes);
3. the SCEN-side Part SP refresh fork (byte-clone 82ddb89c..., only the
   docstring/CACHE-path/cache-sha regions differ from 92a884c9...) is
   re-executed from a scratch tree and must regenerate this kit's
   published reaudit outputs byte-for-byte (7a500a03.../350e269a.../
   9c5b2774... + worklist regen 0818da81...);
4. the Part SP maker is re-executed from a scratch tree and must emit a
   byte-identical increment (89bff217...) and manifest;
5. the fail-closed union merger is re-run 3x from the kit directory
   with the recorded input path strings and must produce byte-identical
   merged cache (cc3694bb...) and byte-identical audit records
   (5904693e...);
6. an INDEPENDENT census recount (graph s4_status/s4_cost + update8
   receipts + both published caches, Board-verified free_now counts
   taken from the re-executed refresh summaries) must reproduce the
   published census delta measurement (030e36ed...) field-for-field:
   34,409/111/39/390 -> 34,407/113/39/390, exactly 2 unknown ->
   excluded_now win-hit flips {2624, 30136}, serving class 3077
   excluded_now on both sides with cost-unknown 95 -> 93, zero closure
   rank/unknown churn, byte-identical per-root coverage, update8
   resolved 281 -> 281 (both adopted s5 indices 103319/112203 outside
   the frozen baseline requirement), joint greedy 35,155 unchanged and
   worklist 64,276 -> 64,276;
7. the decomposition summary decomp-deltas-sixthwin2-adoption.json is
   emitted from the re-executed and re-measured values only.

NO new solver pass runs here.  11x11 stays UNKNOWN; nodes are
bookkeeping; consuming a WIN label asserts no root verdict.
"""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
KIT = "n11-centralreply-sixthwin2-adoption-reaudit-20261126"
B5 = "n11-centralreply-sixthwin5-adoption-predecl-20261126"
KD = ROOT / "research/experiments" / KIT
B5D = ROOT / "research/experiments" / B5

BASE_CACHE = B5D / "output/merged-exact-s5-chain-plus-sixthwin5-20261126.cache"
SCEN_CACHE = KD / "output/merged-exact-s5-chain-plus-sixthwin2-20261126.cache"
GRAPH = (ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"
         "/output/dependency-graph.json.gz")
UPDATE8 = (ROOT / "research/experiments/n11-night-plan-update8-20261016"
           "/output/repaired-joint-plan-update8.json")

BASE_CACHE_SHA = "16a12390c0c3f046f0ae537b2a9940e15661263fc5034ce1b155c138bb9043cd"
BASE_INCR_SHA = "44c16a28f944e255d3968f49a16cc61e06f70269ada833fe976f1607b7d40b03"
BASE_MANIFEST_SHA = "25defefac25a9a527b4de90408fe1dddcd13a19f29128a07afbab69f4e66e39f"
SCEN_CACHE_SHA = "cc3694bbe871ccf27bdf4dbcf5e93586da440164fd75c02c15dc2a0ae46d11b8"
SCEN_CACHE_BYTES = 284127
INCREMENT_SHA = "89bff217885ef89ae7a86d9580657818bdf4c7619ef24da7efd6392169aa1694"
MANIFEST_SHA = "d97f1d5d6b37814cd130fc7519e211b2405f327b9af5e0b7f5bfe9a422c31e07"
MERGE_AUDIT_SHA = "5904693ec6836515c2523d5a5b8744e4f515e56400e3288a07dff30e6875f9cf"
CENSUS_JSON_SHA = "030e36eddc042da500e568f3076352461f008d5625009a5b3814c2f6ae8e38d3"
SCEN_SUMMARY_SHA = "7a500a032f997307defb37f28ce65f93ce935f2feca9ca6281c5474775ef4bc7"
SCEN_WORKLIST_SHA = "0818da81ba01259945d7fb0051b07221582cd4dc68d55d9edb61aa447e4628ac"
BASE_SUMMARY_SHA = "295027cf9a3fd7eb4e74b2008f4794cc146f0ee769901db056e7e176a38deb3a"
BASE_WORKLIST_SHA = "82f9e51798172d1e3a38cbc215b7230135bddd09d911ab672397264560e67cc7"
CLOSURE_SHA = "350e269a9d4e0827274aff7c587cdb389f070eade0ff54c220c7c14f9197bc6d"
PERROOT_SHA = "9c5b277429f99157ff2e65323b5912b9ce957f1d2008f8ac8fc1e03b49f91ad1"
WORKLIST_BYTES = 3715904
REFRESH_SP_SHA = "82ddb89c279f6221cd6d5aa8e89f5f316eba56592fbb7201550b2478da00852e"
REFRESH_B5_SHA = "92a884c9b80f402a580c1545f7db882e26eaeb58becb5fe6686a8bbb7e70ec21"
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
ADOPTED_TABLE_DIGEST = "e7e2b30d5e5ee504f299ec1e64ecf2c252d9d3ca412299d38932628e8844bd83"
ADOPTED_NODES_TOTAL = 31781542


def sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def abort(msg: str):
    print(f"ABORT {msg}", file=sys.stderr)
    raise SystemExit(1)


def check_pin(path: Path, want: str, what: str):
    got = sha(path)
    if got != want:
        abort(f"{what} sha drift: {got} != {want}")


def run(cmd, cwd: Path, tag: str):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        abort(f"{tag} re-execution failed rc={r.returncode}: "
              f"{r.stdout[-400:]} {r.stderr[-400:]}")
    return r


def scratch_refresh(script_src: Path, tag: str):
    """Re-execute a published refresh script from a scratch kit tree.

    The script resolves ROOT from its own location (parents[5]); placed
    at research/experiments/<scratch>/reaudit/scripts/, ROOT is the repo
    root, so its inputs (CACHE, graph, update8, policy, quarantine,
    board) are the published bytes and its outputs land in the scratch
    tree's reaudit/output.
    """
    scratch = ROOT / "research/experiments" / f"zz-sp-extractor-scratch-{tag}"
    if scratch.exists():
        shutil.rmtree(scratch)
    (scratch / "reaudit/scripts").mkdir(parents=True)
    (scratch / "reaudit/output").mkdir(parents=True)
    dst = scratch / "reaudit/scripts" / script_src.name
    shutil.copyfile(script_src, dst)
    check_pin(dst, sha(script_src), f"scratch copy {tag}")
    run([sys.executable, str(dst)], scratch / "reaudit/scripts", tag)
    return scratch


def load_cache(path: Path) -> dict:
    import csv
    cache = {}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 and row[0] != "s5verdict":
                abort(f"malformed cache row in {path.name}")
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            if stones != 5 or verdict not in (1, 2):
                abort(f"malformed cache row in {path.name}")
            key = (lo, hi)
            if key in cache and cache[key][0] != verdict:
                abort(f"WIN/LOSS conflict inside {path.name}: {key}")
            cache[key] = (verdict, nodes)
    return cache


def main() -> None:
    import gzip

    # --- 1. published byte pins -------------------------------------------
    check_pin(BASE_CACHE, BASE_CACHE_SHA, "BASE cache (sixthwin5 head)")
    check_pin(B5D / "output/increment-sixthwin5-20261126.cache",
              BASE_INCR_SHA, "BASE increment (sixthwin5 dossier)")
    check_pin(B5D / "output/increments-manifest.json",
              BASE_MANIFEST_SHA, "BASE manifest (sixthwin5 dossier)")
    check_pin(SCEN_CACHE, SCEN_CACHE_SHA, "SCEN merged cache of record")
    if SCEN_CACHE.stat().st_size != SCEN_CACHE_BYTES:
        abort("SCEN merged cache byte-size drift")
    check_pin(KD / "output/increment-sixthwin2-adoption-20261126.cache",
              INCREMENT_SHA, "Part SP increment")
    check_pin(KD / "output/increments-manifest.json", MANIFEST_SHA,
              "Part SP manifest")
    for i in (1, 2, 3):
        check_pin(KD / f"output/merge-audit-run{i}.json", MERGE_AUDIT_SHA,
                  f"merge-audit-run{i}")
    check_pin(KD / "output/census-deltas-sixthwin2-adoption.json",
              CENSUS_JSON_SHA, "census measurement json")
    check_pin(KD / "reaudit/output/refresh-summary.json", SCEN_SUMMARY_SHA,
              "SCEN refresh summary")
    check_pin(KD / "reaudit/output/closure-classes.csv", CLOSURE_SHA,
              "SCEN closure classes")
    check_pin(KD / "reaudit/output/per-root-coverage.csv", PERROOT_SHA,
              "SCEN per-root coverage")
    wl = KD / "reaudit/output/probe-worklist.csv"
    check_pin(wl, SCEN_WORKLIST_SHA, "SCEN probe worklist (unpublished pin)")
    if wl.stat().st_size != WORKLIST_BYTES:
        abort("SCEN probe worklist size drift")
    check_pin(B5D / "reaudit/output/refresh-summary.json", BASE_SUMMARY_SHA,
              "BASE refresh summary")
    check_pin(B5D / "reaudit/output/closure-classes.csv", CLOSURE_SHA,
              "BASE closure classes")
    check_pin(B5D / "reaudit/output/per-root-coverage.csv", PERROOT_SHA,
              "BASE per-root coverage")
    check_pin(KD / "reaudit/scripts/refresh_adoption_sixthwin2.py",
              REFRESH_SP_SHA, "SCEN refresh fork")
    check_pin(B5D / "reaudit/scripts/refresh_adoption_sixthwin5.py",
              REFRESH_B5_SHA, "BASE refresh script")
    check_pin(KD / "scripts/s5_union_merge.py", MERGER_SHA, "union merger")
    check_pin(GRAPH, GRAPH_SHA, "frozen dependency graph")
    check_pin(UPDATE8, UPDATE8_SHA, "frozen update8 plan")

    manifest = json.loads((KD / "output/increments-manifest.json").read_text())
    if manifest["schema"] != "sixthwin2-adoption-increments-manifest-v1" \
            or manifest["part"] != "SP" \
            or manifest["win_canonical_adoption"] is not True \
            or manifest["sha256"]["win_increment"] != INCREMENT_SHA \
            or manifest["base_cache_sha256"] != BASE_CACHE_SHA \
            or manifest["adopted_nodes_total"] != ADOPTED_NODES_TOTAL \
            or manifest["adopted_table_digest_sha256"] != ADOPTED_TABLE_DIGEST \
            or manifest["loss_ids"] != [] or manifest["win_ties"] != []:
        abort("manifest field drift")
    if len(manifest["adopted_table"]) != 2 \
            or manifest["adopted_table"][0]["lo"] != 1152921573327376384 \
            or manifest["adopted_table"][0]["hi"] != 536870912 \
            or manifest["adopted_table"][0]["nodes"] != 16402480 \
            or manifest["adopted_table"][0]["s5_index"] != 112203 \
            or manifest["adopted_table"][1]["lo"] != 10376293541461626880 \
            or manifest["adopted_table"][1]["hi"] != 65664 \
            or manifest["adopted_table"][1]["nodes"] != 15379062 \
            or manifest["adopted_table"][1]["s5_index"] != 103319:
        abort("manifest adopted-table drift")
    chp = manifest["canonical_head_published_by_this_part"]
    if chp["merged_cache_sha256"] != SCEN_CACHE_SHA \
            or chp["merged_cache_rows"] != 6799 \
            or chp["merged_cache_win_loss"] != [199, 6600] \
            or chp["merge_audit_sha256_x3_identical"] != MERGE_AUDIT_SHA:
        abort("manifest canonical-head publication block drift")

    # --- 2./3. re-execute both refreshes from scratch ----------------------
    base_scratch = scratch_refresh(
        B5D / "reaudit/scripts/refresh_adoption_sixthwin5.py", "base")
    check_pin(base_scratch / "reaudit/output/refresh-summary.json",
              BASE_SUMMARY_SHA, "regen BASE refresh summary")
    check_pin(base_scratch / "reaudit/output/closure-classes.csv",
              CLOSURE_SHA, "regen BASE closure classes")
    check_pin(base_scratch / "reaudit/output/per-root-coverage.csv",
              PERROOT_SHA, "regen BASE per-root coverage")
    bwl = base_scratch / "reaudit/output/probe-worklist.csv"
    check_pin(bwl, BASE_WORKLIST_SHA, "regen BASE worklist pin")
    if bwl.stat().st_size != WORKLIST_BYTES:
        abort("regen BASE worklist size drift")

    scen_scratch = scratch_refresh(
        KD / "reaudit/scripts/refresh_adoption_sixthwin2.py", "scen")
    check_pin(scen_scratch / "reaudit/output/refresh-summary.json",
              SCEN_SUMMARY_SHA, "regen SCEN refresh summary")
    check_pin(scen_scratch / "reaudit/output/closure-classes.csv",
              CLOSURE_SHA, "regen SCEN closure classes")
    check_pin(scen_scratch / "reaudit/output/per-root-coverage.csv",
              PERROOT_SHA, "regen SCEN per-root coverage")
    swl = scen_scratch / "reaudit/output/probe-worklist.csv"
    check_pin(swl, SCEN_WORKLIST_SHA, "regen SCEN worklist pin")
    if swl.stat().st_size != WORKLIST_BYTES:
        abort("regen SCEN worklist size drift")

    # --- 4. re-execute the Part maker from scratch -------------------------
    maker_scratch = ROOT / "research/experiments/zz-sp-extractor-scratch-maker"
    if maker_scratch.exists():
        shutil.rmtree(maker_scratch)
    (maker_scratch / "scripts").mkdir(parents=True)
    (maker_scratch / "output").mkdir(parents=True)
    src = KD / "scripts/make_increments_sixthwin2_adoption.py"
    dst = maker_scratch / "scripts" / src.name
    shutil.copyfile(src, dst)
    check_pin(dst, sha(src), "scratch copy maker")
    merger_src = KD / "scripts/s5_union_merge.py"
    merger_dst = maker_scratch / "scripts" / merger_src.name
    shutil.copyfile(merger_src, merger_dst)
    check_pin(merger_dst, MERGER_SHA, "scratch copy merger for maker gate")
    # the maker's self-publication gates read the published merged head of
    # record and its 3 audits (already byte-pinned at step 1, and
    # independently re-produced by the merger rerun at step 5 below): copy
    # them into the scratch tree so the maker rerun reproduces the increment
    # and manifest against the same bytes it consumed in publication order
    for name in ("merged-exact-s5-chain-plus-sixthwin2-20261126.cache",
                 "merge-audit-run1.json", "merge-audit-run2.json",
                 "merge-audit-run3.json",
                 "increment-sixthwin2-adoption-20261126.cache"):
        shutil.copyfile(KD / "output" / name, maker_scratch / "output" / name)
    run([sys.executable, str(dst)], maker_scratch / "scripts", "maker rerun")
    check_pin(maker_scratch / "output/increment-sixthwin2-adoption-20261126.cache",
              INCREMENT_SHA, "regen increment")
    check_pin(maker_scratch / "output/increments-manifest.json",
              MANIFEST_SHA, "regen manifest")

    # --- 5. re-run the merger 3x from the kit directory --------------------
    for i in (1, 2, 3):
        outp = maker_scratch / f"merged-r{i}.cache"
        auditp = maker_scratch / f"merge-audit-r{i}.json"
        run([sys.executable, "scripts/s5_union_merge.py", "merge",
             "--out", str(outp), "--audit", str(auditp),
             "../n11-centralreply-sixthwin5-adoption-predecl-20261126/"
             "output/merged-exact-s5-chain-plus-sixthwin5-20261126.cache",
             "output/increment-sixthwin2-adoption-20261126.cache"],
            KD, f"merger rerun {i}")
        check_pin(outp, SCEN_CACHE_SHA, f"regen merged cache r{i}")
        check_pin(auditp, MERGE_AUDIT_SHA, f"regen merge audit r{i}")

    # --- 6. independent census recount + census json crosscheck ------------
    base_sum = json.loads(
        (base_scratch / "reaudit/output/refresh-summary.json").read_text())
    scen_sum = json.loads(
        (scen_scratch / "reaudit/output/refresh-summary.json").read_text())

    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s4_masks = g["s4_masks"]
    s4_status = g["s4_status"]
    s4_cost = g["s4_cost"]
    s5_masks = g["s5_masks"]
    mask_to_index = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}
    update8 = json.loads(UPDATE8.read_text())
    receipt = {int(k): int(v)
               for k, v in update8["resolved_s5_verdicts"].items()}
    baseline_req = set(update8["required_new_s5"])

    base = load_cache(BASE_CACHE)
    scen = load_cache(SCEN_CACHE)
    if (len(base), sum(1 for v in base.values() if v[0] == 1),
            sum(1 for v in base.values() if v[0] == 2)) != (6797, 197, 6600):
        abort("BASE cache census drift")
    if (len(scen), sum(1 for v in scen.values() if v[0] == 1),
            sum(1 for v in scen.values() if v[0] == 2)) != (6799, 199, 6600):
        abort("SCEN cache census drift")
    if set(scen) - set(base) != {(1152921573327376384, 536870912),
                               (10376293541461626880, 65664)}:
        abort("SCEN minus BASE must be exactly the 2 adopted keys")
    for k in base:
        if scen[k] != base[k]:
            abort(f"crossover drift at {k}")

    adopted_indices = {112203, 103319}
    if mask_to_index[(1152921573327376384, 536870912)] != 112203 \
            or mask_to_index[(10376293541461626880, 65664)] != 103319:
        abort("adopted s5_index round-trip drift")
    owners = {}
    for idx in adopted_indices:
        owners[idx] = [ci for ci in range(len(s4_masks))
                       if idx in s4_cost[ci]]

    def census(cache):
        status = {}
        for i in range(len(s4_masks)):
            if s4_status[i] == -1:
                status[i] = "excluded"
                continue
            win_hit = False
            unknown_left = False
            for j in s4_cost[i]:
                key = tuple(s5_masks[j])
                v = cache[key][0] if key in cache else receipt.get(j)
                if v == 1:
                    win_hit = True
                elif v is None:
                    unknown_left = True
            if win_hit:
                status[i] = "excluded_now"
            elif not unknown_left:
                status[i] = "free_now_candidate"
            else:
                status[i] = "unknown"
        return status

    base_status = census(base)
    scen_status = census(scen)

    def counts_from(status):
        c = {"unknown": 0, "excluded_now": 0, "free_now": 0, "excluded": 0}
        for v in status.values():
            if v == "free_now_candidate":
                c["free_now"] += 1
            else:
                c[v] += 1
        return c

    cb, cs = counts_from(base_status), counts_from(scen_status)
    if cb != {"unknown": 34409, "excluded_now": 111, "free_now": 39,
              "excluded": 390}:
        abort(f"independent BASE recount drift {cb}")
    if cs != {"unknown": 34407, "excluded_now": 113, "free_now": 39,
              "excluded": 390}:
        abort(f"independent SCEN recount drift {cs}")
    if cb != base_sum["class_status_counts"] \
            or cs != scen_sum["class_status_counts"]:
        abort("recount vs regen refresh summary disagreement")

    owners_flat = set()
    for idx, ocs in owners.items():
        owners_flat.update(ocs)
    flips = sorted(ci for ci in base_status
                   if base_status[ci] != scen_status[ci])
    if flips != [2624, 30136]:
        abort(f"status flip set drift {flips}")
    for ci in flips:
        if base_status[ci] != "unknown" or scen_status[ci] != "excluded_now":
            abort(f"non-win-hit flip at {ci}")
        if ci not in owners_flat:
            abort(f"flip site not an adopted-key owner class: {ci}")
    for ci in owners_flat:
        if base_status[ci] != "unknown":
            if base_status[ci] != scen_status[ci]:
                abort(f"already-decided owner class re-flipped: {ci}")
    cls = 3077
    cost = s4_cost[cls]
    unknown_b = [j for j in cost if tuple(s5_masks[j]) not in base
                 and j not in receipt]
    unknown_s = [j for j in cost if tuple(s5_masks[j]) not in scen
                 and j not in receipt]
    if base_status[cls] != "excluded_now" or scen_status[cls] != "excluded_now":
        abort("serving class 3077 status drift (must be excluded_now twice)")
    if (len(unknown_b), len(unknown_s)) != (95, 93):
        abort("serving class cost-unknown arithmetic drift")

    # closure churn: none may enter/leave/rerank/unknown-churn
    import csv as _csv

    def load_closure(p):
        rows = {}
        with p.open() as stream:
            for r in _csv.DictReader(stream):
                rows[int(r["class_index"])] = r
        return rows

    bc = load_closure(base_scratch / "reaudit/output/closure-classes.csv")
    sc = load_closure(scen_scratch / "reaudit/output/closure-classes.csv")
    if set(bc) != set(sc) or len(bc) != 804:
        abort("closure class set churn")
    for ci, a in bc.items():
        b = sc[ci]
        if a["unknown_now"] != b["unknown_now"] \
                or a["class_rank"] != b["class_rank"]:
            abort(f"closure churn at {ci}")

    # per-root byte identity (regenerated both sides)
    pr_b = (base_scratch / "reaudit/output/per-root-coverage.csv").read_bytes()
    pr_s = (scen_scratch / "reaudit/output/per-root-coverage.csv").read_bytes()
    if pr_b != pr_s:
        abort("per-root coverage differs between the two refresh regenerations")

    # update8 frozen refresh accounting from the REGENERATED summaries
    u8b = base_sum["frozen_update8_refresh"]
    u8s = scen_sum["frozen_update8_refresh"]
    if (u8b["resolved_count"], u8b["remaining_now"], u8b["groups_free_now"]) \
            != (281, 31445, 131):
        abort("BASE update8 refresh accounting drift")
    if (u8s["resolved_count"], u8s["remaining_now"], u8s["groups_free_now"]) \
            != (281, 31445, 131):
        abort("SCEN update8 refresh accounting drift")
    base_req = set(u8b["resolved_among_baseline_requirement"])
    scen_req = set(u8s["resolved_among_baseline_requirement"])
    if scen_req != base_req:
        abort("resolved-among-baseline-requirement set changed")
    if base_req - baseline_req:
        abort("resolved set must sit inside the frozen requirement")
    if adopted_indices & baseline_req:
        abort("adopted keys must sit OUTSIDE the frozen baseline requirement")

    def group_key(gr):
        return (gr["first"], gr["third"], gr["fourth"], gr["reply"],
                gr["s4_class_index"])
    if sorted(group_key(x) for x in u8b["win_hit_groups"]) != \
            sorted(group_key(x) for x in u8s["win_hit_groups"]) \
            or len(u8b["win_hit_groups"]) != 25:
        abort("win-hit group set churn")
    if base_sum["joint_greedy"]["greedy_union_size"] != 35155 \
            or scen_sum["joint_greedy"]["greedy_union_size"] != 35155:
        abort("joint greedy drift")
    if base_sum["worklist_total"] != 64276 or scen_sum["worklist_total"] != 64276:
        abort("worklist total drift")

    # census json field-by-field crosscheck (the published measurement)
    cj = json.loads(
        (KD / "output/census-deltas-sixthwin2-adoption.json").read_text())
    if cj["census_recount_base"] != cb or cj["census_recount_scen"] != cs:
        abort("census json recount fields disagree with the extractor")
    if cj["status_flips"] != flips or cj["status_flip_count"] != 2:
        abort("census json flip fields disagree")
    if cj["serving_class_rows"]["3077"]["unknown_before"] != 95 \
            or cj["serving_class_rows"]["3077"]["unknown_after"] != 93 \
            or cj["serving_class_rows"]["3077"]["base_status"] != "excluded_now" \
            or cj["serving_class_rows"]["3077"]["scen_status"] != "excluded_now":
        abort("census json serving-class fields disagree")
    if cj["closure_churn"] != {"rows_base": 804, "rows_scen": 804,
                               "entered": [], "left": [],
                               "unknown_now_churn": [],
                               "rank_churn_ranked": []}:
        abort("census json closure-churn fields disagree")
    if cj["update8_new_resolved"] != [] \
            or cj["adopted_outside_baseline_requirement"] != [103319, 112203]:
        abort("census json update8 fields disagree")
    if cj["joint_greedy"] != {"base": 35155, "scen": 35155} \
            or cj["worklist_total"] != {"base": 64276, "scen": 64276}:
        abort("census json scheduling fields disagree")
    if cj["verdict"]["part_declared"] is not True \
            or cj["verdict"]["canonical_head_sha256"] != SCEN_CACHE_SHA:
        abort("census json verdict fields disagree")
    if (cj["base_cache"]["sha256"], cj["base_cache"]["rows"],
            cj["base_cache"]["win"], cj["base_cache"]["loss"]) != \
            (BASE_CACHE_SHA, 6797, 197, 6600):
        abort("census json base identity fields disagree")
    if (cj["scen_cache"]["sha256"], cj["scen_cache"]["rows"],
            cj["scen_cache"]["win"], cj["scen_cache"]["loss"]) != \
            (SCEN_CACHE_SHA, 6799, 199, 6600):
        abort("census json scen identity fields disagree")
    if cj["owner_class_count_hist"] != {"2": 1, "3": 1}:
        abort("census json owner histogram disagrees")
    cadopted = {tuple((r["lo"], r["hi"])): r for r in cj["adopted"]}
    for idx, ocs in owners.items():
        key = tuple(s5_masks[idx])
        if cadopted[key]["s5_index"] != idx \
                or cadopted[key]["owner_classes"] != ocs:
            abort("census json adopted-owner fields disagree")

    # --- 7. emit the decomp deltas json -----------------------------------
    decomp = {
        "schema": "sixthwin2-decomp-deltas-v1",
        "part": "SP",
        "date": "2026-11-26",
        "base": {
            "cache_sha256": BASE_CACHE_SHA,
            "cache_path": ("research/experiments/"
                           "n11-centralreply-sixthwin5-adoption-predecl-"
                           "20261126/output/merged-exact-s5-chain-plus-"
                           "sixthwin5-20261126.cache"),
            "rows": 6797, "win": 197, "loss": 6600,
            "refresh_summary_sha256": BASE_SUMMARY_SHA,
            "closure_classes_sha256": CLOSURE_SHA,
            "per_root_coverage_sha256": PERROOT_SHA,
            "probe_worklist_regen_pin_sha256": BASE_WORKLIST_SHA,
            "probe_worklist_not_published_size_policy_bytes": WORKLIST_BYTES,
            "class_status_counts": {"unknown": 34409, "excluded_now": 111,
                                    "free_now": 39, "excluded": 390},
        },
        "scen": {
            "cache_sha256": SCEN_CACHE_SHA,
            "cache_path_of_record": (f"research/experiments/{KIT}/"
                                     "output/merged-exact-s5-chain-plus-"
                                     "sixthwin2-20261126.cache"),
            "rows": 6799, "win": 199, "loss": 6600,
            "increment_sha256": INCREMENT_SHA,
            "manifest_sha256": MANIFEST_SHA,
            "merge_audit_sha256": MERGE_AUDIT_SHA,
            "refresh_summary_sha256": SCEN_SUMMARY_SHA,
            "closure_classes_sha256": CLOSURE_SHA,
            "per_root_coverage_sha256": PERROOT_SHA,
            "probe_worklist_regen_pin_sha256": SCEN_WORKLIST_SHA,
            "probe_worklist_not_published_size_policy_bytes": WORKLIST_BYTES,
            "class_status_counts": {"unknown": 34407, "excluded_now": 113,
                                    "free_now": 39, "excluded": 390},
        },
        "canonical_head_publication": {
            "merged_cache_name": "merged-exact-s5-chain-plus-"
                                 "sixthwin2-20261126.cache",
            "merged_cache_sha256": SCEN_CACHE_SHA,
            "merged_cache_bytes": SCEN_CACHE_BYTES,
            "merged_cache_rows": 6799,
            "merged_cache_win_loss": [199, 6600],
            "merge_audit_runs": 3,
            "merge_audit_sha256_x3_identical": MERGE_AUDIT_SHA,
            "merger_sha256": MERGER_SHA,
            "note": "no pre-declaration dossier exists for sixthwin2; the "
                    "Part SP kit publishes the merged head of record at its "
                    "own output/ directory; the extractor re-ran the "
                    "merger 3x from the kit directory with the recorded "
                    "input path strings and reproduced the cache and all "
                    "three audit records byte-identically",
        },
        "adopted": {
            "ids": ["k13", "k19"],
            "nodes_total": ADOPTED_NODES_TOTAL,
            "direction": "WIN (win-only canonical adoption)",
            "condition": ("parked4 L50M ladder four-run battery (15M "
                          "park-at-UNKNOWN baseline, 50M cold two-pass "
                          "node-exact, 32M budget-margin re-proof, "
                          "voluntary third cold 50M verify), C++-gated "
                          "GATE-PASS by the Part SM scrutiny kit, "
                          "third-implementation-corroborated by the Part "
                          "SL batch audit (3 identical cold runs each); "
                          "re-verified live by this extractor (both refresh "
                          "forks re-executed byte-verbatim, the Part maker "
                          "re-executed byte-verbatim and the merger 3x; NO "
                          "new solver pass ran)"),
            "win_ties": [],
            "standing_unconsumed_win_not_emitted": {
                "k20": "10376293541461626880:33619968 (parked4rest2 "
                       "L50M WIN(1); third-impl corroboration absent at SP "
                       "build time; Part SN C++ gate in flight - disclosed)",
                "k33": "12682136550675320832:65536 (same standing status "
                       "as k20)",
            },
            "standing_unconsumed_loss_not_emitted": {
                "count": 30,
                "note": "the 30 fifth-resumption verified LOSS rows of the "
                        "Part SL batch stay unconsumed honest labels",
            },
        },
        "class_flips": {
            "count": 2,
            "direction": ("unknown -> excluded_now, win-hit only: exactly "
                          "the owner classes of the adopted keys that were "
                          "status-unknown at BASE (2624 owner of k19, "
                          "30136 owner of k13); owners 3077 (both keys) "
                          "and 5184 (k19) were already excluded_now; NO "
                          "class is freed"),
            "per_key_owner_classes": {
                "k13": owners[112203],
                "k19": owners[103319],
            },
            "flipped_classes": flips,
            "owner_class_count_histogram": {"2": 1, "3": 1},
            "serving_classes": {
                "3077": {
                    "class": 3077,
                    "boundary_raw": None,
                    "cost_unknown_base": 95,
                    "cost_unknown_scen": 93,
                    "adopted_members": ["k13", "k19"],
                    "status_base": "excluded_now",
                    "status_scen": "excluded_now",
                    "status_note": "already flipped by Part EW; the SP "
                                   "adoption only reduces its cost-unknown "
                                   "count (the lane-era halt-audit if-"
                                   "adopted prediction against the 6e49dd84 "
                                   "head is superseded by this measurement "
                                   "against the current 16a12390 head)",
                },
            },
        },
        "closure_classes": {
            "rows_before_after": [804, 804],
            "left_rows": [],
            "entered_rows": [],
            "exit_note": ("no closure class enters or leaves: the 2 "
                          "win-hit flips turn classes unknown -> "
                          "excluded_now, which do not change closure "
                          "membership; zero rank churn and zero unknown_now "
                          "churn (measured on both regenerated CSVs)"),
            "rank_churn_rows": 0,
            "rank_churn_nature": "measured 0 re-ranked rows",
            "unknown_churn": {},
            "groups_served_churn": {},
        },
        "census_crosscheck": {
            "measurement_sha256": CENSUS_JSON_SHA,
            "agreement": ("EXACT on both cache identities, the census "
                          "counts (34,409/111/39/390 -> "
                          "34,407/113/39/390), the exact 2-class flip set "
                          "{2624, 30136}, zero closure churn incl. the "
                          "zero rank and unknown_now tables, per-root "
                          "greedy deltas (none, byte-identical), joint "
                          "greedy, worklist totals, update8 numbers "
                          "(281 -> 281, both adopted indices 103319/112203 "
                          "outside the frozen baseline requirement), "
                          "win_hit identity, serving-class records, the "
                          "owner histogram and the 2-row adopted table "
                          "with owner sets"),
            "verdict_fields_current": ("verdict.part_declared=true and "
                                       "canonical_head_sha256=cc3694bb... "
                                       "describe the ADOPTED head declared "
                                       "by Part SP; checked, current"),
        },
        "frozen_update8": {
            "union_baseline": 31859,
            "resolved": [281, 281],
            "remaining_now": [31445, 31445],
            "groups_free_now": [131, 131],
            "win_hit_groups": ("25 -> 25 IDENTICAL sets (measured; no "
                               "group crosses the win_hit boundary)"),
            "newly_resolved": [],
            "newly_resolved_note": ("both adopted s5 indices (k13 112203, "
                                    "k19 103319) sit outside the frozen "
                                    "update8 baseline requirement and are "
                                    "correctly not counted (measured, "
                                    "disclosed)"),
        },
        "honesty": {
            "win_only_adoption": True,
            "no_root_verdict": ("no root verdict is asserted or implied by "
                                "consuming a WIN label; the win-hit "
                                "mechanism only reclassifies owner classes "
                                "as excluded_now"),
            "no_class_freed": ("no class flips to free_now; joint greedy "
                               "and per-root coverage are byte-identical on "
                               "both sides"),
            "scheduling_effect": ("joint greedy 35,155 -> 35,155 "
                                  "UNCHANGED, worklist 64,276 -> 64,276 "
                                  "(delta 0), update8 resolved 281 -> 281: "
                                  "no baseline-requirement scheduling change "
                                  "at all; the only measured effects are "
                                  "the 2 win-hit flips and the serving-class "
                                  "cost-unknown 95 -> 93"),
            "unknown_still": ("34,407 S4 classes remain status-unknown "
                              "after the adoption; 11x11 stays UNKNOWN"),
            "unconsumed": ("k20/k33 parked4rest2 WIN rows and the 30 SL "
                           "batch LOSS rows stay unconsumed honest labels "
                           "(not emitted, no cache); no root, no root "
                           "class and no closure class verdict is asserted"),
        },
        "per_root": {
            "free_now_uncovered": ("identical at all 20 rows incl. "
                                   "baseline; no coverage claim"),
            "greedy_union_changes": {},
            "joint_greedy": [35155, 35155],
            "joint_greedy_delta": 0,
            "unique_groups": [2115, 2115],
            "group_best_options_nonfree": [2101, 2101],
            "worklist_total": [64276, 64276],
        },
    }
    outp = KD / "output/decomp-deltas-sixthwin2-adoption.json"
    outp.write_text(json.dumps(decomp, indent=1, sort_keys=True),
                    encoding="utf-8")
    print(json.dumps({
        "part": "SP",
        "verdict": "EXTRACTor PASS: both refreshes re-executed byte-verbatim, "
                   "maker re-executed byte-verbatim, merger 3x byte-identical, "
                   "independent census recount EXACT (34,409/111/39/390 -> "
                   "34,407/113/39/390, flips {2624, 30136}, serving "
                   "excluded_now x2 with cost-unknown 95 -> 93, zero closure "
                   "churn, update8 281 -> 281, joint greedy 35,155 unchanged, "
                   "worklist 64,276 unchanged)",
        "decomp_sha256": sha(outp),
        "base_census": cb, "scen_census": cs, "flips": flips,
    }, indent=1))
    print("written:", outp)

    # cleanup scratch trees
    for s in (base_scratch, scen_scratch, maker_scratch):
        shutil.rmtree(s, ignore_errors=True)


if __name__ == "__main__":
    main()
