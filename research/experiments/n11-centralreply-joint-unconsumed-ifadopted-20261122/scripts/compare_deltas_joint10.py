#!/usr/bin/env python3
"""Joint unconsumed-rows IF-ADOPTED decomposition delta extractor (Part AJ).

Fail-closed, analysis-only. Reads the BASE refresh outputs (Part AH base
control, same canonical 95e868d6... cache) and the three Part AJ scenario
refresh outputs:

  * JWIN10   = base + the 10 unconsumed closure WIN rows only
               (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006)
  * JLOSS122 = base + the 122 probed exact-LOSS rows NOT already in BASE
  * JALL132  = base + all 132 unique-new probed rows (10 WIN + 122 LOSS)

Covers the nine WIN-HALT batches 1,3,4,5,6,8,9,11,12 (classes 16757, 20421,
16371, 12264, 5473, 2634, 1518, 8785, 8106).  Batch 13/14 are NOT in this
packet (Part AI / Part AF own them).  HONEST CORRECTION published by the
increments maker itself: the first maker run ABORTed at b001 already-in-BASE;
precise re-measurement found exactly 19 batch-1 LOSS rows (b001..b017, b019,
b020) pre-consumed into canonical BASE with identical verdicts AND nodes,
excluded from every increment here (151 probed -> 132 unique-new).

The refresh semantics of the published refresh scripts are re-executed
faithfully for the base and each scenario cache (graph + update8 receipt +
cache verdicts, per-class verdict-level status, Board fail-closed
verification for free candidates) and every recomputed class_status_count is
asserted byte-equal to the published summary before any delta is reported.

Emitted deltas (machine-identified, no hand annotation):
  * excluded_now flip sets vs base, cross-checked against the frozen-graph
    holder union of the 10 WIN S5 children restricted to classes that are
    not already excluded_now at base, plus the WIN-holder detail per batch
    with membership_class_count gates,
  * per-batch-class unknown_now deltas, gated to the scenario increments'
    cost-membership (cross-batch memberships handled by measuring the
    actual s4_cost membership, not by trusting batch ownership),
  * update8 newly-resolved baseline-requirement indices per scenario, gated
    to the increment rows actually present; counts are MEASURED (some
    increment rows may sit outside the frozen update8 requirement),
  * metric/additivity observations and per-root free-coverage gates:
    per-root (free_now, uncovered) and the full roots table must be
    unchanged in every scenario; root 27 (known-loss baseline) must stay
    119/119 free; the per-root individual_greedy_union scheduling sizes are
    MEASURED (they move; nonadditive roots are recorded, not gated).

The increments are read-only what-if analysis inputs; no verdict is consumed
and no class, root, coverage or closure claim is made. 11x11 stays UNKNOWN;
nodes are bookkeeping, never verdicts.
"""
import csv
import gzip
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]

BASE_DIR = ROOT / "research/experiments/n11-class8106-n005n006-base-control-20261122/output"
SCEN = {
    "JWIN10": EXP / "wins10/output",
    "JLOSS122": EXP / "loss122/output",
    "JALL132": EXP / "all132/output",
}
INCR = {
    "JWIN10": EXP / "output/increment-joint-wins10-IFADOPTED-20261122.cache",
    "JLOSS122": EXP / "output/increment-joint-loss122-IFADOPTED-20261122.cache",
    "JALL132": EXP / "output/increment-joint-all132-IFADOPTED-20261122.cache",
}
INCR_SHA = {
    "JWIN10": "fe2c6f68f49195b44e21c8d43998fccd965c868e08e49d8a1b3233f5daa4c15e",
    "JLOSS122": "e5fe80af7321a9ea10715c419c2611e469c2470da7ebe26f7d5ee8f14681e8c8",
    "JALL132": "cc841d6e8af62558e2bd59600f6ffa55ed1c781996f085ead7c699237f4b1a1f",
}
SCEN_CACHE = {
    "JWIN10": ("merged-joint-wins10-scenario-20261122.cache",
               "7881724ac978bd4e7b8e089dc9467e770a44be5634051edccde46bc976f5a2b5"),
    "JLOSS122": ("merged-joint-loss122-scenario-20261122.cache",
                 "d80ee94b978243c0a2747acae2fe78f88c84c0a68f64b620af869988feaa27cd"),
    "JALL132": ("merged-joint-all132-scenario-20261122.cache",
                "13bfec6e819be2ecef6317cc28d0b1bbce87c1942dc268f7dd615769a2c9eda2"),
}
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_CACHE = ROOT / "research/experiments/n11-central-reply-8784-closure-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-20261122.cache"
BATCHES = {
    "b018": ("n11-centralreply-closure-class16757-batch-20261122", 16757),
    "d002": ("n11-centralreply-closure-class20421-batch-20261122", 20421),
    "e002": ("n11-centralreply-closure-class16371-batch4-20261122", 16371),
    "f017": ("n11-centralreply-closure-class12264-batch5-20261122", 12264),
    "g018": ("n11-centralreply-closure-class5473-batch6-20261122", 5473),
    "h045": ("n11-centralreply-closure-class2634-batch8-20261122", 2634),
    "j033": ("n11-centralreply-closure-class1518-batch9-20261122", 1518),
    "z003": ("n11-centralreply-closure-class8785-batch11-20261122", 8785),
    "n005": ("n11-centralreply-closure-class8106-batch12-20261122", 8106),
    "n006": ("n11-centralreply-closure-class8106-batch12-20261122", 8106),
}
BATCH_CLASSES = [16757, 20421, 16371, 12264, 5473, 2634, 1518, 8785, 8106]
OUT = EXP / "output/decomp-deltas-joint10.json"

METRICS = [
    ("excluded_now", lambda s: s["class_status_counts"]["excluded_now"]),
    ("free_now", lambda s: s["class_status_counts"]["free_now"]),
    ("unknown_classes", lambda s: s["class_status_counts"]["unknown"]),
    ("update8_remaining_now", lambda s: s["frozen_update8_refresh"]["remaining_now"]),
    ("update8_resolved_count", lambda s: s["frozen_update8_refresh"]["resolved_count"]),
    ("update8_win_hit_groups", lambda s: len(s["frozen_update8_refresh"]["win_hit_groups"])),
    ("joint_greedy_union_size", lambda s: s["joint_greedy"]["greedy_union_size"]),
    ("probe_worklist_total", lambda s: s["worklist_total"]),
    ("baseline_root27_free_thirds", lambda s: s["roots"][0]["free_thirds_now"]),
]


def fail(msg):
    print("GATE FAILED: " + msg, file=sys.stderr)
    raise SystemExit(1)


def sha(path):
    import hashlib
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


def main():
    for name, (fname, want) in SCEN_CACHE.items():
        if sha(EXP / "output" / fname) != want:
            fail(f"{name} cache sha drift")
    for name, p in INCR.items():
        if sha(p) != INCR_SHA[name]:
            fail(f"{name} increment sha drift")
    if sha(BASE_DIR / "refresh-summary.json") != "25987addd9bfdb901b341288ca1543ab5f893e77471da636a345c1edfd2acb96":
        fail("BASE control refresh-summary sha drift")
    if sha(BASE_CACHE) != "95e868d6762925b9a27ad963a825a9ad4fd5131a864eb82fac0db77d7acdb326":
        fail("BASE cache sha drift")

    incr_rows = {}
    for name, p in INCR.items():
        incr_rows[name] = read_cache(p)
    if len(incr_rows["JWIN10"]) != 10 or len(incr_rows["JLOSS122"]) != 122 or len(incr_rows["JALL132"]) != 132:
        fail("increment row counts not 10/122/132")
    if any(v[0] != 1 for v in incr_rows["JWIN10"].values()):
        fail("JWIN10 increment contains a non-WIN verdict")
    if any(v[0] != 2 for v in incr_rows["JLOSS122"].values()):
        fail("JLOSS122 increment contains a non-LOSS verdict")
    if (set(incr_rows["JWIN10"]) | set(incr_rows["JLOSS122"])) != set(incr_rows["JALL132"]):
        fail("JALL132 rows != JWIN10 + JLOSS122 rows")
    for k, v in incr_rows["JWIN10"].items():
        if incr_rows["JALL132"][k] != v:
            fail(f"JALL132 WIN row mismatch {k}")
    for k, v in incr_rows["JLOSS122"].items():
        if incr_rows["JALL132"][k] != v:
            fail(f"JALL132 LOSS row mismatch {k}")

    # WIN/LOSS ids against their published batch-keys.json (lo,hi)
    win_key_lohi = {}
    for kid, (dirname, klass) in BATCHES.items():
        keys = json.loads((ROOT / "research/experiments" / dirname / "input/batch-keys.json").read_text())["keys"]
        by_id = {k["key_id"]: k for k in keys}
        if kid not in by_id:
            fail(f"{kid} missing from its batch-keys.json")
        bk = by_id[kid]
        win_key_lohi[kid] = (int(bk["lo"]), int(bk["hi"]), bk["s5_index"], bk["membership_class_count"], klass)
        if (int(bk["lo"]), int(bk["hi"])) not in incr_rows["JWIN10"]:
            fail(f"{kid} (lo,hi) not present in the JWIN10 increment")
        if incr_rows["JWIN10"][(int(bk["lo"]), int(bk["hi"]))][0] != 1:
            fail(f"{kid} increment row is not WIN")
    if set(win_key_lohi) != {"b018", "d002", "e002", "f017", "g018", "h045", "j033", "z003", "n005", "n006"}:
        fail("WIN id set mismatch")

    sys.path.insert(0, str(BOARD_SOURCE.parent))
    sys.path.insert(0, str(POLICY.parent))
    from independent import Board
    from s5_evidence_policy import quarantined_cache_keys, is_canonical_safe_s5_key

    quarantined = quarantined_cache_keys()
    board = Board(11)

    with gzip.open(GRAPH, "rt", encoding="utf-8") as stream:
        g = json.load(stream)
    s4_masks, s4_status, s4_cost = g["s4_masks"], g["s4_status"], g["s4_cost"]
    s5_masks = g["s5_masks"]
    mask_to_index = {(lo, hi): i for i, (lo, hi) in enumerate(s5_masks)}

    update8 = json.loads(UPDATE8.read_text(encoding="utf-8"))
    if update8["union_size"] != 31859 or len(update8["required_new_s5"]) != 31859:
        fail("update8 baseline drift")
    receipt_verdicts = {int(k): int(v) for k, v in update8["resolved_s5_verdicts"].items()}

    base_cache = read_cache(BASE_CACHE)
    scenarios_cache = {name: read_cache(EXP / "output" / fname)
                       for name, (fname, _) in SCEN_CACHE.items()}

    # graph-side machine identification of the 10 WIN cost-child holder sets
    holders = {}
    win_s5 = {}
    for kid, (lo, hi, s5i, memb, klass) in win_key_lohi.items():
        win_s5[kid] = s5i
        if (lo, hi) not in mask_to_index or mask_to_index[(lo, hi)] != s5i:
            fail(f"{kid} lo/hi does not map to its published s5 index")
        hs = sorted(i for i, c in enumerate(s4_cost) if s5i in c)
        if len(hs) != memb:
            fail(f"{kid} graph holders {hs} vs membership_class_count {memb}")
        for i in hs:
            if s4_status[i] not in (0, 1):
                fail(f"{kid} holder {i} unexpected graph status {s4_status[i]}")
        holders[kid] = hs
    holder_union = sorted(set().union(*[set(h) for h in holders.values()]))
    for kid, (lo, hi, s5i, memb, klass) in win_key_lohi.items():
        if klass not in holders[kid]:
            fail(f"{kid} own batch class {klass} not among its holders {holders[kid]}")
    member_win_counts = Counter()
    for kid, hs in holders.items():
        for i in hs:
            member_win_counts[i] += 1

    def verdicts_for(cache):
        index_verdict = {}
        for (lo, hi), (verdict, _nodes) in cache.items():
            i = mask_to_index.get((lo, hi))
            if i is None:
                continue
            index_verdict[i] = verdict
        for i, v in receipt_verdicts.items():
            index_verdict[i] = v
        return index_verdict

    def refresh_statuses(cache):
        """Faithful re-execution of the published refresh class pass."""
        index_verdict = verdicts_for(cache)
        for (lo, hi) in cache:
            if (lo, hi) in quarantined:
                fail(f"quarantined key inside cache: {(lo, hi)}")
            if not is_canonical_safe_s5_key((lo, hi)):
                fail(f"noncanonical cache key {(lo, hi)}")
        LOSS, UNKNOWN, EXCLUDED = 0, 1, -1
        st, unknown_counts, win_hits = {}, {}, {}
        for i in range(len(s4_masks)):
            base = s4_status[i]
            cost = s4_cost[i]
            if base == EXCLUDED:
                st[i] = "excluded"
                unknown_counts[i] = 0
                continue
            unknown, win_hit = [], False
            for j in cost:
                v = index_verdict.get(j)
                if v == 1:
                    win_hit = True
                elif v is None:
                    unknown.append(j)
            win_hits[i] = win_hit
            unknown_counts[i] = len(unknown)
            if base == UNKNOWN:
                st[i] = "excluded_now" if win_hit else ("free_candidate" if not unknown else "unknown")
            else:
                st[i] = "excluded_now" if win_hit else "free_candidate"
        for i, s in list(st.items()):
            if s != "free_candidate":
                continue
            lo, hi = s4_masks[i]
            if not is_canonical_safe_s5_key((lo, hi)):
                try:
                    board.legal(lo | (hi << 64))
                except ValueError:
                    st[i] = "free_now_unverified"
                    continue
            missing = False
            for child in board.children(lo | (hi << 64)):
                key = (child & ((1 << 64) - 1), child >> 64)
                have = cache.get(key)
                if have is None:
                    ci = mask_to_index.get(key)
                    rv = receipt_verdicts.get(ci) if ci is not None else None
                    have = (rv, 0) if rv is not None else None
                if have is None or have[0] != 2:
                    missing = True
                    break
            st[i] = "free_now" if not missing else "free_now_unverified"
        counts = Counter(st.values())
        return st, unknown_counts, win_hits, counts

    base_summary = json.loads((BASE_DIR / "refresh-summary.json").read_text())
    published = {"BASE": base_summary}
    for name, d in SCEN.items():
        published[name] = json.loads((d / "refresh-summary.json").read_text())

    recomputed = {"BASE": refresh_statuses(base_cache)}
    for name in SCEN:
        recomputed[name] = refresh_statuses(scenarios_cache[name])

    for name in ["BASE"] + list(SCEN):
        st, _, _, counts = recomputed[name]
        pub = published[name]["class_status_counts"]
        want = dict(pub)
        if counts.get("free_now", 0) != want.get("free_now", 0):
            fail(f"{name}: recomputed free {counts.get('free_now',0)} != published free_now {want.get('free_now',0)}")
        for k in ("excluded", "excluded_now", "unknown"):
            if counts.get(k, 0) != want.get(k, 0):
                fail(f"{name}: recomputed {k} {counts.get(k,0)} != published {k} {want.get(k,0)}")
        if counts.get("free_now_unverified", 0):
            fail(f"{name}: unverified free candidates appeared: {counts.get('free_now_unverified')}")

    excluded_now_sets = {}
    for name in ["BASE"] + list(SCEN):
        st = recomputed[name][0]
        excluded_now_sets[name] = {i for i, s in st.items() if s == "excluded_now"}

    base_ex = excluded_now_sets["BASE"]
    flips = {name: sorted(excluded_now_sets[name] - base_ex) for name in SCEN}
    win_only = sorted(excluded_now_sets["JALL132"] - excluded_now_sets["JLOSS122"])
    eligible_union = sorted(i for i in holder_union
                            if recomputed["BASE"][0].get(i) != "excluded_now"
                            and s4_status[i] != -1)
    already_excluded_now = sorted(i for i in holder_union if i in base_ex)
    graph_excluded = sorted(i for i in holder_union if s4_status[i] == -1)
    if flips["JWIN10"] != eligible_union:
        fail(f"JWIN10 excluded_now flips {flips['JWIN10']} != eligible holder union {eligible_union}")
    if flips["JLOSS122"]:
        fail(f"JLOSS122 excluded_now flips non-empty: {flips['JLOSS122']}")
    if win_only != eligible_union:
        fail(f"win-only excluded_now delta {win_only} != eligible holder union {eligible_union}")
    if flips["JALL132"] != sorted(set(flips["JLOSS122"]) | set(flips["JWIN10"])):
        fail(f"JALL132 flips != union: {flips['JALL132']}")
    if len(eligible_union) != len(holder_union) - len(already_excluded_now) - len(graph_excluded):
        fail("eligible union arithmetic inconsistent")

    # per-batch-class unknown_now deltas, gated to actual s4_cost membership
    def incr_costs(rows):
        out = {}
        for (lo, hi) in rows:
            i = mask_to_index.get((lo, hi))
            if i is None:
                fail(f"increment key outside the s5 universe: {(lo, hi)}")
            out[i] = rows[(lo, hi)][0]
        return out
    scen_membership_delta = {}
    for name in SCEN:
        iv = incr_costs(incr_rows[name])
        per_class = {}
        for c in BATCH_CLASSES:
            per_class[c] = sorted(j for j in s4_cost[c] if j in iv)
        scen_membership_delta[name] = per_class
    class_table = {}
    for c in BATCH_CLASSES:
        row = {"base_unknown_now": recomputed["BASE"][1].get(c)}
        for name in SCEN:
            u = recomputed[name][1].get(c)
            exp = row["base_unknown_now"] - len(scen_membership_delta[name][c])
            if u != exp:
                fail(f"class {c} {name} unknown_now {u} != base - membership-delta {exp}")
            row[name + "_unknown_now"] = u
            row[name + "_own_delta"] = len(scen_membership_delta[name][c])
        row["full_eq_win_plus_loss"] = (row["JALL132_own_delta"]
                                        == row["JWIN10_own_delta"] + row["JLOSS122_own_delta"])
        if not row["full_eq_win_plus_loss"]:
            fail(f"class {c} membership additivity violated: {row}")
        class_table[c] = row

    table = {}
    for metric, fn in METRICS:
        table[metric] = {"base": fn(published["BASE"])}
        for name in SCEN:
            table[metric][name] = fn(published[name])

    # update8 resolved-requirement delta, machine-identified
    base_resolved = set(published["BASE"]["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    resolved_delta = {}
    for name in SCEN:
        s = published[name]["frozen_update8_refresh"]
        new = sorted(set(s["resolved_among_baseline_requirement"]) - base_resolved)
        lost = sorted(base_resolved - set(s["resolved_among_baseline_requirement"]))
        if lost:
            fail(f"{name}: resolved set shrank: {lost}")
        if set(new) - set(incr_costs(incr_rows[name])):
            fail(f"{name}: newly resolved s5 outside its increment universe")
        resolved_delta[name] = {"newly_resolved_s5": new, "count": len(new),
                                "increment_rows_in_universe": len(incr_costs(incr_rows[name]))}
    rd = table["update8_resolved_count"]
    if rd["JALL132"] - rd["base"] != resolved_delta["JALL132"]["count"]:
        fail("JALL132 update8 resolved count arithmetic inconsistent")

    additivity = {}
    for metric, _ in METRICS:
        t = table[metric]
        w = t["JWIN10"] - t["base"]
        l = t["JLOSS122"] - t["base"]
        f = t["JALL132"] - t["base"]
        additivity[metric] = {"win_delta": w, "loss_delta": l, "full_delta": f,
                              "full_eq_win_plus_loss": (w + l == f)}

    # per-root free coverage equality gates (coverage columns only);
    # the per-root individual_greedy_union scheduling sizes ARE allowed to
    # move and are measured below instead of gated.
    cov = {}
    base_prc = {}
    with (BASE_DIR / "per-root-coverage.csv").open() as fh:
        for r in csv.DictReader(fh):
            base_prc[(r["role"], r["first"])] = (r["free_now"], r["uncovered"], r["individual_greedy_union"])
    base_roots = {(r["role"], r.get("origin_first")): (r["free_thirds_now"], r["uncovered"])
                  for r in published["BASE"]["roots"]}
    root27 = published["BASE"]["roots"][0]
    if root27["role"] != "known-loss-baseline" or root27.get("origin_first") != 27 \
            or root27["free_thirds_now"] != 119 or root27["thirds"] != 119 or root27["uncovered"] != 0:
        fail(f"root27 baseline row not 119/119: {root27}")
    greedy_root_deltas = {"JWIN10": {}, "JLOSS122": {}, "JALL132": {}}
    for name, d in SCEN.items():
        prc = {}
        with (d / "per-root-coverage.csv").open() as fh:
            for r in csv.DictReader(fh):
                prc[(r["role"], r["first"])] = (r["free_now"], r["uncovered"], r["individual_greedy_union"])
        roots = {(r["role"], r.get("origin_first")): (r["free_thirds_now"], r["uncovered"])
                 for r in published[name]["roots"]}
        if roots != base_roots:
            fail(f"per-root roots free coverage gate broken in {name}")
        r27 = published[name]["roots"][0]
        if (r27["role"], r27.get("origin_first"), r27["free_thirds_now"], r27["thirds"], r27["uncovered"]) \
                != ("known-loss-baseline", 27, 119, 119, 0):
            fail(f"root27 not 119/119 in {name}: {r27}")
        moved = {}
        for k, (_f, _u, gu) in base_prc.items():
            f2, u2, gu2 = prc[k]
            if (f2, u2) != (_f, _u):
                fail(f"per-root free coverage columns changed in {name} at {k}")
            if gu2 != gu:
                moved["|".join(map(str, k))] = {"base": int(gu), "scenario": int(gu2),
                                                "delta": int(gu2) - int(gu)}
        for k, m in moved.items():
            greedy_root_deltas[name][k] = m
        cov[name] = {
            "free_coverage_columns_identical_to_base": True,
            "roots_identical_to_base": True,
            "root27_119_of_119": True,
            "individual_greedy_union_moved_roots": moved,
        }
    greedy_additivity = {}
    for k in sorted(set(greedy_root_deltas["JWIN10"]) | set(greedy_root_deltas["JLOSS122"])
                    | set(greedy_root_deltas["JALL132"])):
        d5 = greedy_root_deltas["JWIN10"].get(k, {}).get("delta", 0)
        d6 = greedy_root_deltas["JLOSS122"].get(k, {}).get("delta", 0)
        d8 = greedy_root_deltas["JALL132"].get(k, {}).get("delta", 0)
        greedy_additivity[k] = {"win_delta": d5, "loss_delta": d6, "full_delta": d8,
                               "full_eq_win_plus_loss": d5 + d6 == d8}

    per_root_greedy = {name: published[name]["per_root_greedy"] for name in ["BASE"] + list(SCEN)}
    group_best_nonfree = {"BASE": published["BASE"]["group_best_options_nonfree"]}
    for name in SCEN:
        group_best_nonfree[name] = published[name]["group_best_options_nonfree"]
    win_hit_detail = {name: published[name]["frozen_update8_refresh"]["win_hit_groups"]
                      for name in ["BASE"] + list(SCEN)}
    greedy_movers = {}
    for root, b in published["BASE"]["per_root_greedy"].items():
        bsz = b["greedy_union_size"]
        row = {"base": bsz}
        for name in SCEN:
            row[name] = published[name]["per_root_greedy"][root]["greedy_union_size"]
            row[name + "_delta"] = row[name] - bsz
        greedy_movers[root] = row
    greedy_anomaly_roots = {root: {k: v for k, v in row.items()}
                            for root, row in greedy_movers.items()
                            if row["JALL132_delta"] != row["JWIN10_delta"] + row["JLOSS122_delta"]}

    out = {
        "schema": "n11-joint10-unconsumed-decomp-deltas-v1",
        "interpretation_guard": ("read-only what-if IF-ADOPTED planning deltas; "
                                 "verdicts NOT consumed; scheduling quantities only; "
                                 "the 10 WIN rows are HYPOTHETICAL adoptions, the 122 LOSS rows "
                                 "are unconsumed published evidence; 11x11 empty board and all "
                                 "roots stay UNKNOWN"),
        "recompute_gates": ("class statuses, free-candidate board verification and all "
                            "class_status_counts re-executed from graph+update8+cache and "
                            "asserted equal to the published summaries for BASE and all "
                            "three scenarios before any delta was emitted"),
        "honest_correction_note": ("the increments maker's first run ABORTed fail-closed at "
                                   "b001 already-in-canonical-BASE; re-measurement showed "
                                   "exactly 19 batch-1 LOSS rows (b001..b017,b019,b020) "
                                   "already inside BASE with identical verdicts AND nodes; "
                                   "they are excluded from every increment (151 probed -> "
                                   "132 unique-new); no verdict conflicts were found"),
        "win_keys": {
            kid: {
                "s5_index": win_key_lohi[kid][2],
                "batch_class": win_key_lohi[kid][4],
                "graph_cost_child_holder_classes": holders[kid],
                "membership_class_count": win_key_lohi[kid][3],
            } for kid in sorted(win_key_lohi)
        },
        "holders_summary": {
            "holder_union": holder_union,
            "holder_union_size": len(holder_union),
            "eligible_flip_union": eligible_union,
            "already_excluded_now_at_base": already_excluded_now,
            "graph_excluded": graph_excluded,
            "multi_win_holder_classes": {str(i): member_win_counts[i]
                                         for i in sorted(member_win_counts) if member_win_counts[i] > 1},
            "exclusion_note": ("per the published refresh semantics a baseline UNKNOWN class "
                               "with any WIN cost child becomes excluded_now; all 30 holders "
                               "are baseline UNKNOWN at the frozen graph and none is "
                               "excluded_now at BASE, so the eligible union is the full "
                               "30-class holder union"),
        },
        "excluded_now_flips": {
            "JWIN10": flips["JWIN10"], "JLOSS122": flips["JLOSS122"],
            "JALL132": flips["JALL132"],
            "win_only_jall132_minus_jloss122": win_only,
            "all_equal_eligible_holder_union": (flips["JWIN10"] == eligible_union
                                                and win_only == eligible_union),
        },
        "per_batch_class_unknown_now": class_table,
        "update8_resolved_delta": resolved_delta,
        "metrics": table,
        "additivity_measured": additivity,
        "per_root_free_coverage_gate": cov,
        "per_root_greedy_union_column_additivity": greedy_additivity,
        "per_root_greedy": per_root_greedy,
        "group_best_options_nonfree": group_best_nonfree,
        "win_hit_groups_detail": win_hit_detail,
        "greedy_nonadditive_roots": greedy_anomaly_roots,
        "excluded_now_counts": {n: published[n]["class_status_counts"]["excluded_now"]
                               for n in ["BASE"] + list(SCEN)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    compact = {
        "metrics": {m: t for m, t in table.items()},
        "per_batch_class_unknown_now": class_table,
        "update8_resolved_delta": resolved_delta,
        "excluded_now_flips": out["excluded_now_flips"],
        "holder_union_size": len(holder_union),
        "eligible_flip_union_size": len(eligible_union),
        "multi_win_holder_classes": out["holders_summary"]["multi_win_holder_classes"],
        "per_root_free_coverage_gate": {n: {"identical": c["free_coverage_columns_identical_to_base"],
                                            "root27_119": c["root27_119_of_119"],
                                            "greedy_moved": len(c["individual_greedy_union_moved_roots"])}
                                        for n, c in cov.items()},
        "greedy_union_column_additivity": greedy_additivity,
        "greedy_nonadditive_roots": {r: {k: v for k, v in row.items()
                                         if k in ("base", "JWIN10", "JLOSS122", "JALL132")}
                                     for r, row in greedy_anomaly_roots.items()},
    }
    print(json.dumps(compact, indent=1))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
