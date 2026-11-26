#!/usr/bin/env python3
"""Part SQ sixthwin3 adoption delta EXTRACTOR, fail-closed.

Re-verification battery over the published Part SQ kit
n11-centralreply-sixthwin3-adoption-reaudit-20261126 (structural clone of
the Part SP extractor pattern, adapted to the sixthwin3 sources):

1. every published kit byte is pinned and verified first (increment,
   manifest, merged head of record, 3 merge audits, reaudit refresh
   outputs, the census measurement json, the refresh fork, the maker,
   the merger, the frozen graph/update8/quarantine/policy anchors and
   the BASE-side sixthwin2 dossier outputs);
2. the BASE-side published refresh (sixthwin2 dossier,
   refresh_adoption_sixthwin2.py sha256 82ddb89c...) is re-executed
   byte-verbatim from a scratch tree and must regenerate its published
   outputs byte-for-byte (refresh-summary 7a500a03..., closure-classes
   350e269a..., per-root-coverage 9c5b2774... and the unpublished-size
   probe-worklist regen pin 0818da81..., 3,715,904 bytes);
3. the SCEN-side Part SQ refresh fork (byte-clone 60dfb1a1..., only the
   docstring/CACHE-path/cache-sha regions differ from 82ddb89c...) is
   re-executed from a scratch tree and must regenerate this kit's
   published reaudit outputs byte-for-byte (de205c31.../350e269a.../
   9c5b2774... + worklist regen 24301312...);
4. the Part SQ maker is re-executed from a scratch tree and must emit a
   byte-identical increment (47f7dfb0...) and manifest (07181de7...);
5. the fail-closed union merger is re-run 3x from the kit directory
   with the recorded input path strings and must produce byte-identical
   merged cache (02db5ab3...) and byte-identical audit records
   (622ac17f...);
6. an INDEPENDENT census recount (graph s4_status/s4_cost + update8
   receipts + both published caches, Board-verified free_now counts
   taken from the re-executed refresh summaries) must reproduce the
   published census delta measurement (8d8329d0...) field-for-field:
   34,407/113/39/390 -> 34,405/115/39/390, exactly 2 unknown ->
   excluded_now win-hit flips {2402, 3054}, serving class 3077
   excluded_now on both sides with cost-unknown 93 -> 91, zero closure
   rank/unknown churn, byte-identical per-root coverage, update8
   resolved 281 -> 281 (both adopted s5 indices 97791/111843 outside
   the frozen baseline requirement), joint greedy 35,155 unchanged and
   worklist 64,276 -> 64,276;
7. the decomposition summary decomp-deltas-sixthwin3-adoption.json is
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
KIT = "n11-centralreply-sixthwin3-adoption-reaudit-20261126"
B2 = "n11-centralreply-sixthwin2-adoption-reaudit-20261126"
KD = ROOT / "research/experiments" / KIT
B2D = ROOT / "research/experiments" / B2

BASE_CACHE = B2D / "output/merged-exact-s5-chain-plus-sixthwin2-20261126.cache"
SCEN_CACHE = KD / "output/merged-exact-s5-chain-plus-sixthwin3-20261126.cache"
GRAPH = (ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"
         "/output/dependency-graph.json.gz")
UPDATE8 = (ROOT / "research/experiments/n11-night-plan-update8-20261016"
           "/output/repaired-joint-plan-update8.json")

BASE_CACHE_SHA = "cc3694bbe871ccf27bdf4dbcf5e93586da440164fd75c02c15dc2a0ae46d11b8"
BASE_INCR_SHA = "89bff217885ef89ae7a86d9580657818bdf4c7619ef24da7efd6392169aa1694"
BASE_MANIFEST_SHA = "d97f1d5d6b37814cd130fc7519e211b2405f327b9af5e0b7f5bfe9a422c31e07"
SCEN_CACHE_SHA = "02db5ab35b8ad71dfd0699217756291c6bc896c78e9fd7c609b5e25177f6b25c"
SCEN_CACHE_BYTES = 284230
INCREMENT_SHA = "47f7dfb02489a960184b5c83bd3ed36e33936bd40067c7cc97299ab1f740ecc6"
MANIFEST_SHA = "07181de7e74b619be876fdfff907f452a294cec20705258314560327e12eeb27"
MERGE_AUDIT_SHA = "622ac17f72c9ad2a7b9e9714b3274c6bcba1df34910365268db16f3c76e0c368"
CENSUS_JSON_SHA = "8d8329d092557933300c3b7297c3fe532ce157a62b7694308aadf716a56e6fcc"
SCEN_SUMMARY_SHA = "de205c31e59aeeb22e4d040578d1d0d89ec55a074020d4f3a244815964e4eafd"
SCEN_WORKLIST_SHA = "24301312e1e7cfd904da085723144bbbaef15e272c2d430979410520672dcd33"
BASE_SUMMARY_SHA = "7a500a032f997307defb37f28ce65f93ce935f2feca9ca6281c5474775ef4bc7"
BASE_WORKLIST_SHA = "0818da81ba01259945d7fb0051b07221582cd4dc68d55d9edb61aa447e4628ac"
CLOSURE_SHA = "350e269a9d4e0827274aff7c587cdb389f070eade0ff54c220c7c14f9197bc6d"
PERROOT_SHA = "9c5b277429f99157ff2e65323b5912b9ce957f1d2008f8ac8fc1e03b49f91ad1"
WORKLIST_BYTES = 3715904
REFRESH_SP_SHA = "60dfb1a199743529b61e8da6a330e5f5b333c19b063c60804b3ce16a341f2fda"
REFRESH_B2_SHA = "82ddb89c279f6221cd6d5aa8e89f5f316eba56592fbb7201550b2478da00852e"
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
GRAPH_SHA = "54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024bbf192ec0d408c00b"
UPDATE8_SHA = "b658290aa941c105035aa3b9b13741cd95b5032b9b7fb7d61b2aed0d0cea6719"
ADOPTED_TABLE_DIGEST = "d89ccfbb53078359fb650b2ac7fec5d94fe2b7bfb0038b54ce476d7b01f6dd28"
ADOPTED_NODES_TOTAL = 32038980


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
    scratch = ROOT / "research/experiments" / f"zz-sq-extractor-scratch-{tag}"
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
    check_pin(BASE_CACHE, BASE_CACHE_SHA, "BASE cache (sixthwin2 head)")
    check_pin(B2D / "output/increment-sixthwin2-adoption-20261126.cache",
              BASE_INCR_SHA, "BASE increment (sixthwin2 dossier)")
    check_pin(B2D / "output/increments-manifest.json",
              BASE_MANIFEST_SHA, "BASE manifest (sixthwin2 dossier)")
    check_pin(SCEN_CACHE, SCEN_CACHE_SHA, "SCEN merged cache of record")
    if SCEN_CACHE.stat().st_size != SCEN_CACHE_BYTES:
        abort("SCEN merged cache byte-size drift")
    check_pin(KD / "output/increment-sixthwin3-adoption-20261126.cache",
              INCREMENT_SHA, "Part SQ increment")
    check_pin(KD / "output/increments-manifest.json", MANIFEST_SHA,
              "Part SQ manifest")
    for i in (1, 2, 3):
        check_pin(KD / f"output/merge-audit-run{i}.json", MERGE_AUDIT_SHA,
                  f"merge-audit-run{i}")
    check_pin(KD / "output/census-deltas-sixthwin3-adoption.json",
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
    check_pin(B2D / "reaudit/output/refresh-summary.json", BASE_SUMMARY_SHA,
              "BASE refresh summary")
    check_pin(B2D / "reaudit/output/closure-classes.csv", CLOSURE_SHA,
              "BASE closure classes")
    check_pin(B2D / "reaudit/output/per-root-coverage.csv", PERROOT_SHA,
              "BASE per-root coverage")
    check_pin(KD / "reaudit/scripts/refresh_adoption_sixthwin3.py",
              REFRESH_SP_SHA, "SCEN refresh fork")
    check_pin(B2D / "reaudit/scripts/refresh_adoption_sixthwin2.py",
              REFRESH_B2_SHA, "BASE refresh script")
    check_pin(KD / "scripts/s5_union_merge.py", MERGER_SHA, "union merger")
    check_pin(GRAPH, GRAPH_SHA, "frozen dependency graph")
    check_pin(UPDATE8, UPDATE8_SHA, "frozen update8 plan")

    manifest = json.loads((KD / "output/increments-manifest.json").read_text())
    if manifest["schema"] != "sixthwin3-adoption-increments-manifest-v1" \
            or manifest["part"] != "SQ" \
            or manifest["win_canonical_adoption"] is not True \
            or manifest["sha256"]["win_increment"] != INCREMENT_SHA \
            or manifest["base_cache_sha256"] != BASE_CACHE_SHA \
            or manifest["adopted_nodes_total"] != ADOPTED_NODES_TOTAL \
            or manifest["adopted_table_digest_sha256"] != ADOPTED_TABLE_DIGEST \
            or manifest["loss_ids"] != [] or manifest["win_ties"] != []:
        abort("manifest field drift")
    if len(manifest["adopted_table"]) != 2 \
            or manifest["adopted_table"][0]["lo"] != 10376293541461626880 \
            or manifest["adopted_table"][0]["hi"] != 33619968 \
            or manifest["adopted_table"][0]["nodes"] != 16196331 \
            or manifest["adopted_table"][0]["s5_index"] != 111843 \
            or manifest["adopted_table"][1]["lo"] != 12682136550675320832 \
            or manifest["adopted_table"][1]["hi"] != 65536 \
            or manifest["adopted_table"][1]["nodes"] != 15842649 \
            or manifest["adopted_table"][1]["s5_index"] != 97791:
        abort("manifest adopted-table drift")
    chp = manifest["canonical_head_published_by_this_part"]
    if chp["merged_cache_sha256"] != SCEN_CACHE_SHA \
            or chp["merged_cache_rows"] != 6801 \
            or chp["merged_cache_win_loss"] != [201, 6600] \
            or chp["merge_audit_sha256_x3_identical"] != MERGE_AUDIT_SHA:
        abort("manifest canonical-head publication block drift")

    # --- 2./3. re-execute both refreshes from scratch ----------------------
    base_scratch = scratch_refresh(
        B2D / "reaudit/scripts/refresh_adoption_sixthwin2.py", "base")
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
        KD / "reaudit/scripts/refresh_adoption_sixthwin3.py", "scen")
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
    maker_scratch = ROOT / "research/experiments/zz-sq-extractor-scratch-maker"
    if maker_scratch.exists():
        shutil.rmtree(maker_scratch)
    (maker_scratch / "scripts").mkdir(parents=True)
    (maker_scratch / "output").mkdir(parents=True)
    src = KD / "scripts/make_increments_sixthwin3_adoption.py"
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
    for name in ("merged-exact-s5-chain-plus-sixthwin3-20261126.cache",
                 "merge-audit-run1.json", "merge-audit-run2.json",
                 "merge-audit-run3.json",
                 "increment-sixthwin3-adoption-20261126.cache"):
        shutil.copyfile(KD / "output" / name, maker_scratch / "output" / name)
    run([sys.executable, str(dst)], maker_scratch / "scripts", "maker rerun")
    check_pin(maker_scratch / "output/increment-sixthwin3-adoption-20261126.cache",
              INCREMENT_SHA, "regen increment")
    check_pin(maker_scratch / "output/increments-manifest.json",
              MANIFEST_SHA, "regen manifest")

    # --- 5. re-run the merger 3x from the kit directory --------------------
    for i in (1, 2, 3):
        outp = maker_scratch / f"merged-r{i}.cache"
        auditp = maker_scratch / f"merge-audit-r{i}.json"
        run([sys.executable, "scripts/s5_union_merge.py", "merge",
             "--out", str(outp), "--audit", str(auditp),
             "../n11-centralreply-sixthwin2-adoption-reaudit-20261126/"
             "output/merged-exact-s5-chain-plus-sixthwin2-20261126.cache",
             "output/increment-sixthwin3-adoption-20261126.cache"],
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
            sum(1 for v in base.values() if v[0] == 2)) != (6799, 199, 6600):
        abort("BASE cache census drift")
    if (len(scen), sum(1 for v in scen.values() if v[0] == 1),
            sum(1 for v in scen.values() if v[0] == 2)) != (6801, 201, 6600):
        abort("SCEN cache census drift")
    if set(scen) - set(base) != {(10376293541461626880, 33619968),
                               (12682136550675320832, 65536)}:
        abort("SCEN minus BASE must be exactly the 2 adopted keys")
    for k in base:
        if scen[k] != base[k]:
            abort(f"crossover drift at {k}")

    adopted_indices = {111843, 97791}
    if mask_to_index[(10376293541461626880, 33619968)] != 111843 \
            or mask_to_index[(12682136550675320832, 65536)] != 97791:
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
    if cb != {"unknown": 34407, "excluded_now": 113, "free_now": 39,
              "excluded": 390}:
        abort(f"independent BASE recount drift {cb}")
    if cs != {"unknown": 34405, "excluded_now": 115, "free_now": 39,
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
    if flips != [2402, 3054]:
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
    if (len(unknown_b), len(unknown_s)) != (93, 91):
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
        (KD / "output/census-deltas-sixthwin3-adoption.json").read_text())
    if cj["census_recount_base"] != cb or cj["census_recount_scen"] != cs:
        abort("census json recount fields disagree with the extractor")
    if cj["status_flips"] != flips or cj["status_flip_count"] != 2:
        abort("census json flip fields disagree")
    if cj["serving_class_rows"]["3077"]["unknown_before"] != 93 \
            or cj["serving_class_rows"]["3077"]["unknown_after"] != 91 \
            or cj["serving_class_rows"]["3077"]["base_status"] != "excluded_now" \
            or cj["serving_class_rows"]["3077"]["scen_status"] != "excluded_now":
        abort("census json serving-class fields disagree")
    if cj["closure_churn"] != {"rows_base": 804, "rows_scen": 804,
                               "entered": [], "left": [],
                               "unknown_now_churn": [],
                               "rank_churn_ranked": []}:
        abort("census json closure-churn fields disagree")
    if cj["update8_new_resolved"] != [] \
            or cj["adopted_outside_baseline_requirement"] != [97791, 111843]:
        abort("census json update8 fields disagree")
    if cj["joint_greedy"] != {"base": 35155, "scen": 35155} \
            or cj["worklist_total"] != {"base": 64276, "scen": 64276}:
        abort("census json scheduling fields disagree")
    if cj["verdict"]["part_declared"] is not True \
            or cj["verdict"]["canonical_head_sha256"] != SCEN_CACHE_SHA:
        abort("census json verdict fields disagree")
    if (cj["base_cache"]["sha256"], cj["base_cache"]["rows"],
            cj["base_cache"]["win"], cj["base_cache"]["loss"]) != \
            (BASE_CACHE_SHA, 6799, 199, 6600):
        abort("census json base identity fields disagree")
    if (cj["scen_cache"]["sha256"], cj["scen_cache"]["rows"],
            cj["scen_cache"]["win"], cj["scen_cache"]["loss"]) != \
            (SCEN_CACHE_SHA, 6801, 201, 6600):
        abort("census json scen identity fields disagree")
    if cj["owner_class_count_hist"] != {"3": 2}:
        abort("census json owner histogram disagrees")
    cadopted = {tuple((r["lo"], r["hi"])): r for r in cj["adopted"]}
    for idx, ocs in owners.items():
        key = tuple(s5_masks[idx])
        if cadopted[key]["s5_index"] != idx \
                or cadopted[key]["owner_classes"] != ocs:
            abort("census json adopted-owner fields disagree")

    # --- 7. emit the decomp deltas json -----------------------------------
    decomp = {
        "schema": "sixthwin3-decomp-deltas-v1",
        "part": "SQ",
        "date": "2026-11-26",
        "base": {
            "cache_sha256": BASE_CACHE_SHA,
            "cache_path": ("research/experiments/"
                           "n11-centralreply-sixthwin2-adoption-reaudit-"
                           "20261126/output/merged-exact-s5-chain-plus-"
                           "sixthwin2-20261126.cache"),
            "rows": 6799, "win": 199, "loss": 6600,
            "refresh_summary_sha256": BASE_SUMMARY_SHA,
            "closure_classes_sha256": CLOSURE_SHA,
            "per_root_coverage_sha256": PERROOT_SHA,
            "probe_worklist_regen_pin_sha256": BASE_WORKLIST_SHA,
            "probe_worklist_not_published_size_policy_bytes": WORKLIST_BYTES,
            "class_status_counts": {"unknown": 34407, "excluded_now": 113,
                                    "free_now": 39, "excluded": 390},
        },
        "scen": {
            "cache_sha256": SCEN_CACHE_SHA,
            "cache_path_of_record": (f"research/experiments/{KIT}/"
                                     "output/merged-exact-s5-chain-plus-"
                                     "sixthwin3-20261126.cache"),
            "rows": 6801, "win": 201, "loss": 6600,
            "increment_sha256": INCREMENT_SHA,
            "manifest_sha256": MANIFEST_SHA,
            "merge_audit_sha256": MERGE_AUDIT_SHA,
            "refresh_summary_sha256": SCEN_SUMMARY_SHA,
            "closure_classes_sha256": CLOSURE_SHA,
            "per_root_coverage_sha256": PERROOT_SHA,
            "probe_worklist_regen_pin_sha256": SCEN_WORKLIST_SHA,
            "probe_worklist_not_published_size_policy_bytes": WORKLIST_BYTES,
            "class_status_counts": {"unknown": 34405, "excluded_now": 115,
                                    "free_now": 39, "excluded": 390},
        },
        "canonical_head_publication": {
            "merged_cache_name": "merged-exact-s5-chain-plus-"
                                 "sixthwin3-20261126.cache",
            "merged_cache_sha256": SCEN_CACHE_SHA,
            "merged_cache_bytes": SCEN_CACHE_BYTES,
            "merged_cache_rows": 6801,
            "merged_cache_win_loss": [201, 6600],
            "merge_audit_runs": 3,
            "merge_audit_sha256_x3_identical": MERGE_AUDIT_SHA,
            "merger_sha256": MERGER_SHA,
            "note": "no pre-declaration dossier exists for sixthwin3; the "
                    "Part SQ kit publishes the merged head of record at its "
                    "own output/ directory; the extractor re-ran the "
                    "merger 3x from the kit directory with the recorded "
                    "input path strings and reproduced the cache and all "
                    "three audit records byte-identically",
        },
        "adopted": {
            "ids": ["k20", "k33"],
            "nodes_total": ADOPTED_NODES_TOTAL,
            "direction": "WIN (win-only canonical adoption)",
            "condition": ("parked4rest2 L50M ladder four-run battery (15M "
                          "park-at-UNKNOWN baseline, 50M cold two-pass "
                          "node-exact, 32M budget-margin re-proof, "
                          "voluntary third cold 50M verify), C++-gated "
                          "GATE-PASS by the Part SN scrutiny kit, "
                          "third-implementation-corroborated by the k20/k33 "
                          "third-impl verdict re-verification addendum "
                          "(3 identical cold runs each, auditor re-run live "
                          "by the Part maker); re-verified live by this "
                          "extractor (both refresh forks re-executed "
                          "byte-verbatim, the Part maker re-executed "
                          "byte-verbatim and the merger 3x; NO new solver "
                          "pass ran)"),
            "win_ties": [],
            "standing_unconsumed_win_not_emitted": {
                "k38": "the still-parked key k38 of the same probe "
                       "selection (15,000,000 park-at-UNKNOWN, NO L50M "
                       "follow-up claimed - the coverage asymmetry the "
                       "k20/k33 third-impl completion pre-registered)",
            },
            "standing_unconsumed_loss_not_emitted": {
                "count": 30,
                "note": "the 30 fifth-resumption verified LOSS rows of the "
                        "Part SL batch stay unconsumed honest labels "
                        "WITHOUT a delegated C++ second-implementation "
                        "gate (coverage asymmetry disclosed)",
            },
        },
        "class_flips": {
            "count": 2,
            "direction": ("unknown -> excluded_now, win-hit only: exactly "
                          "the owner classes of the adopted keys that were "
                          "status-unknown at BASE (3054 owner of k20, "
                          "2402 owner of k33); the serving owner class 3077 "
                          "was already excluded_now (Part EW); NO class "
                          "is freed"),
            "per_key_owner_classes": {
                "k20": owners[111843],
                "k33": owners[97791],
            },
            "flipped_classes": flips,
            "owner_class_count_histogram": {"3": 2},
            "serving_classes": {
                "3077": {
                    "class": 3077,
                    "boundary_raw": None,
                    "cost_unknown_base": 93,
                    "cost_unknown_scen": 91,
                    "adopted_members": ["k20", "k33"],
                    "status_base": "excluded_now",
                    "status_scen": "excluded_now",
                    "status_note": "already flipped by Part EW; measured "
                                   "cost-unknown 95 -> 93 by Part SP and "
                                   "93 -> 91 by this Part",
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
                          "counts (34,407/113/39/390 -> "
                          "34,405/115/39/390), the exact 2-class flip set "
                          "{2402, 3054}, zero closure churn incl. the "
                          "zero rank and unknown_now tables, per-root "
                          "greedy deltas (none, byte-identical), joint "
                          "greedy, worklist totals, update8 numbers "
                          "(281 -> 281, both adopted indices 97791/111843 "
                          "outside the frozen baseline requirement), "
                          "win_hit identity, serving-class records, the "
                          "owner histogram and the 2-row adopted table "
                          "with owner sets"),
            "verdict_fields_current": ("verdict.part_declared=true and "
                                       "canonical_head_sha256=02db5ab3... "
                                       "describe the ADOPTED head declared "
                                       "by Part SQ; checked, current"),
        },
        "frozen_update8": {
            "union_baseline": 31859,
            "resolved": [281, 281],
            "remaining_now": [31445, 31445],
            "groups_free_now": [131, 131],
            "win_hit_groups": ("25 -> 25 IDENTICAL sets (measured; no "
                               "group crosses the win_hit boundary)"),
            "newly_resolved": [],
            "newly_resolved_note": ("both adopted s5 indices (k20 111843, "
                                    "k33 97791) sit outside the frozen "
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
                                  "cost-unknown 93 -> 91"),
            "unknown_still": ("34,405 S4 classes remain status-unknown "
                              "after the adoption; 11x11 stays UNKNOWN"),
            "unconsumed": ("the still-parked key k38 and the 30 SL batch "
                           "LOSS rows stay unconsumed honest labels "
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
    outp = KD / "output/decomp-deltas-sixthwin3-adoption.json"
    outp.write_text(json.dumps(decomp, indent=1, sort_keys=True),
                    encoding="utf-8")
    print(json.dumps({
        "part": "SQ",
        "verdict": "EXTRACTor PASS: both refreshes re-executed byte-verbatim, "
                   "maker re-executed byte-verbatim, merger 3x byte-identical, "
                   "independent census recount EXACT (34,407/113/39/390 -> "
                   "34,405/115/39/390, flips {2402, 3054}, serving "
                   "excluded_now x2 with cost-unknown 93 -> 91, zero closure "
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
