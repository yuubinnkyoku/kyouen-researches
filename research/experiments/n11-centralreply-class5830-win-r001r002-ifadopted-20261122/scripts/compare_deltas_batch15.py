#!/usr/bin/env python3
"""Batch-15 (class 5830) r001/r002 IF-ADOPTED decomposition delta extractor (Part AN).

Fail-closed, analysis-only. Executes the published single-owner Part AN
declaration (note amendment pushed 2026-11-22 after the Part AI status
update).  Reads the BASE refresh outputs (Part AH base control, canonical
95e868d6... cache) and the single scenario refresh output:

  * PWIN2 = base + the 2 unconsumed closure WIN rows only (r001/r002)

Batch 15 (class 5830) has ZERO resolved LOSS rows (r003/r004 are 15M budget
EXHAUSTION rows, result 0, nodes==budget - honest UNKNOWN, excluded from
every increment by the type gate), so there is NO PLOSS2/PFULL4 scenario:
adopting every resolved row of batch-15 equals adopting {r001, r002}.  That
identity is machine-asserted here from the published increments manifest
(row_counts.losses == 0, full_packet_eq_win_only true, exhaustion rows
recorded as excluded).

The refresh semantics of the published refresh scripts are re-executed
faithfully for the base and the scenario cache (graph + update8 receipt +
cache verdicts, per-class verdict-level status, Board fail-closed
verification for free candidates) and every recomputed class_status_count is
asserted byte-equal to the published summary before any delta is reported.

Emitted deltas (machine-identified, no hand annotation):
  * excluded_now flip set vs base, cross-checked against the frozen-graph
    cost-child holder classes of the 2 WIN S5 children.  Note: the published
    batch-keys membership_class_count is a closure-scoped count (r001/r002
    both report 1: only their batch class 5830 among the closure classes),
    while the frozen-graph s4_cost holder sets are authoritative for the
    refresh semantics and are larger here (they include non-closure side
    classes); both are recorded per WIN key and the batch class must be
    among the graph holders (gated).  Every holder class's own unknown_now
    delta is measured and gated to its per-class membership delta,
  * per-batch-class unknown_now delta, gated to the scenario increment's
    cost-membership,
  * update8 newly-resolved baseline-requirement indices, gated to the
    increment rows actually present; counts are MEASURED,
  * metric observations and per-root free-coverage gates: per-root
    (free_now, uncovered) and the full roots table must be unchanged;
    root 27 (known-loss baseline) must stay 119/119 free; the per-root
    individual_greedy_union scheduling sizes are MEASURED (they move;
    nonadditive roots are recorded, not gated).

The increment is a read-only what-if analysis input; no verdict is consumed
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
SCEN = {"PWIN2": EXP / "win2/output"}
INCR = {"PWIN2": EXP / "output/increment-batch15-wins2-IFADOPTED-20261122.cache"}
INCR_SHA = {"PWIN2": "05c10e1ff17c2601b1fb4a0782af2543d302187ce6344df97d3c763947262b7d"}
MANIFEST = EXP / "output/increments-manifest.json"
SCEN_CACHE = {
    "PWIN2": ("merged-batch15-wins2-scenario-20261122.cache",
              "516933010c8e2033602110aaafacd182de7e8affbd897248ba54f6058e2d282e"),
}
SCEN_SUMMARY_SHA = {
    "PWIN2": "496f37610f01daa4e67e3a3652fac6817d0f8fa43838d03a4010f8d5ac6f4c48",
}
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_CACHE = ROOT / "research/experiments/n11-central-reply-8784-closure-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-20261122.cache"
BATCHES = {
    "r001": ("n11-centralreply-closure-class5830-batch15-20261122", 5830),
    "r002": ("n11-centralreply-closure-class5830-batch15-20261122", 5830),
}
BATCH_CLASSES = [5830]
OUT = EXP / "output/decomp-deltas-batch15.json"

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
    if SCEN_SUMMARY_SHA["PWIN2"] != sha(SCEN["PWIN2"] / "refresh-summary.json"):
        fail("PWIN2 refresh-summary sha drift")
    if sha(BASE_DIR / "refresh-summary.json") != "25987addd9bfdb901b341288ca1543ab5f893e77471da636a345c1edfd2acb96":
        fail("BASE control refresh-summary sha drift")
    if sha(BASE_CACHE) != "95e868d6762925b9a27ad963a825a9ad4fd5131a864eb82fac0db77d7acdb326":
        fail("BASE cache sha drift")

    # single-scenario type gates from the published increments manifest
    manifest = json.loads(MANIFEST.read_text())
    if manifest["row_counts"]["losses"] != 0 or manifest["row_counts"]["resolved_rows"] != 2:
        fail(f"manifest row_counts not (2 resolved / 0 losses): {manifest['row_counts']}")
    if sorted(manifest["win_ids"]) != ["r001", "r002"]:
        fail(f"manifest win_ids mismatch: {manifest['win_ids']}")
    if sorted(manifest["exhausted_excluded_ids"]) != ["r003", "r004"]:
        fail(f"manifest exhausted ids mismatch: {manifest['exhausted_excluded_ids']}")
    if len(manifest["exhausted_rows"]) != 2:
        fail("manifest exhaustion rows != 2")
    for e in manifest["exhausted_rows"]:
        if e["verdict"] is not None or e["nodes"] != e["budget"] or e["nodes"] != 15000000:
            fail(f"exhaustion row carries a verdict or wrong nodes: {e}")
    if manifest["full_packet_eq_win_only"] is not True or manifest["loss_scenario_exists"] is not False:
        fail("manifest full==win identity not asserted")
    if manifest["sha256"]["win"] != INCR_SHA["PWIN2"]:
        fail("manifest win sha mismatch")

    incr_rows = {"PWIN2": read_cache(INCR["PWIN2"])}
    if len(incr_rows["PWIN2"]) != 2:
        fail("PWIN2 increment row count != 2")
    if any(v[0] != 1 for v in incr_rows["PWIN2"].values()):
        fail("PWIN2 increment contains a non-WIN verdict")

    # WIN/LOSS ids against their published batch-keys.json (lo,hi)
    win_key_lohi = {}
    for kid, (dirname, klass) in BATCHES.items():
        keys = json.loads((ROOT / "research/experiments" / dirname / "input/batch-keys.json").read_text())["keys"]
        by_id = {k["key_id"]: k for k in keys}
        if kid not in by_id:
            fail(f"{kid} missing from its batch-keys.json")
        bk = by_id[kid]
        win_key_lohi[kid] = (int(bk["lo"]), int(bk["hi"]), bk["s5_index"], bk["membership_class_count"], klass)
        if (int(bk["lo"]), int(bk["hi"])) not in incr_rows["PWIN2"]:
            fail(f"{kid} (lo,hi) not present in the PWIN2 increment")
        if incr_rows["PWIN2"][(int(bk["lo"]), int(bk["hi"]))][0] != 1:
            fail(f"{kid} increment row is not WIN")
    if set(win_key_lohi) != {"r001", "r002"}:
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

    # graph-side machine identification of the 2 WIN cost-child holder sets
    holders = {}
    win_s5 = {}
    for kid, (lo, hi, s5i, memb, klass) in win_key_lohi.items():
        win_s5[kid] = s5i
        if (lo, hi) not in mask_to_index or mask_to_index[(lo, hi)] != s5i:
            fail(f"{kid} lo/hi does not map to its published s5 index")
        hs = sorted(i for i, c in enumerate(s4_cost) if s5i in c)
        if memb > len(hs):
            fail(f"{kid} membership_class_count {memb} exceeds graph holders {hs}")
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
    eligible_union = sorted(i for i in holder_union
                            if recomputed["BASE"][0].get(i) != "excluded_now"
                            and s4_status[i] != -1)
    already_excluded_now = sorted(i for i in holder_union if i in base_ex)
    graph_excluded = sorted(i for i in holder_union if s4_status[i] == -1)
    if flips["PWIN2"] != eligible_union:
        fail(f"PWIN2 excluded_now flips {flips['PWIN2']} != eligible holder union {eligible_union}")
    if len(eligible_union) != len(holder_union) - len(already_excluded_now) - len(graph_excluded):
        fail("eligible union arithmetic inconsistent")

    # per-batch-class unknown_now delta, gated to actual s4_cost membership
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
        class_table[c] = row

    # every graph holder class's own unknown_now delta, gated to per-class
    # membership in the scenario increment (measured for non-batch classes)
    holder_classes_table = {}
    for c in holder_union:
        row = {"base_unknown_now": recomputed["BASE"][1].get(c),
               "base_status": recomputed["BASE"][0].get(c) if c not in base_ex else "excluded_now",
               "in_batch_classes": c in BATCH_CLASSES}
        for name in SCEN:
            own = sorted(j for j in s4_cost[c] if j in incr_costs(incr_rows[name]))
            u = recomputed[name][1].get(c)
            exp = row["base_unknown_now"] - len(own)
            if u != exp:
                fail(f"holder class {c} {name} unknown_now {u} != base - own membership {exp}")
            row[name + "_unknown_now"] = u
            row[name + "_own_membership"] = len(own)
            row[name + "_status"] = recomputed[name][0].get(c)
        holder_classes_table[c] = row

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
    if rd["PWIN2"] - rd["base"] != resolved_delta["PWIN2"]["count"]:
        fail("PWIN2 update8 resolved count arithmetic inconsistent")

    deltas = {}
    for metric, _ in METRICS:
        t = table[metric]
        deltas[metric] = {"win_delta": t["PWIN2"] - t["base"]}

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
        cov[name] = {
            "free_coverage_columns_identical_to_base": True,
            "roots_identical_to_base": True,
            "root27_119_of_119": True,
            "individual_greedy_union_moved_roots": moved,
        }

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

    out = {
        "schema": "n11-batch15-ifadopted-decomp-deltas-v1",
        "interpretation_guard": ("read-only what-if IF-ADOPTED planning deltas; "
                                 "verdicts NOT consumed; scheduling quantities only; "
                                 "the 2 WIN rows are HYPOTHETICAL adoptions; 11x11 "
                                 "empty board and all roots stay UNKNOWN"),
        "recompute_gates": ("class statuses, free-candidate board verification and all "
                            "class_status_counts re-executed from graph+update8+cache and "
                            "asserted equal to the published summaries for BASE and the "
                            "PWIN2 scenario before any delta was emitted"),
        "single_scenario_note": ("batch-15 has zero resolved LOSS rows; r003/r004 are "
                                 "budget-exhaustion rows (result 0, nodes==budget, honest "
                                 "UNKNOWN) excluded by the type gate, so PWIN2 is also the "
                                 "full-packet scenario (full==win machine-asserted from the "
                                 "increments manifest)"),
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
                               "with any WIN cost child becomes excluded_now; holders that "
                               "are baseline UNKNOWN at the frozen graph and not already "
                               "excluded_now at BASE form the eligible union"),
            "membership_scope_note": ("batch-keys membership_class_count is a closure-scoped "
                                      "count over the closure classes only; the frozen-graph "
                                      "s4_cost holder sets (which drive the refresh and the "
                                      "flip sets) can and here do additionally contain "
                                      "non-closure side classes (e.g. the class-5830 batch "
                                      "keys are also cost children of side class 2634)"),
        },
        "excluded_now_flips": {
            "PWIN2": flips["PWIN2"],
            "equal_eligible_holder_union": flips["PWIN2"] == eligible_union,
        },
        "per_batch_class_unknown_now": class_table,
        "holder_classes_unknown_now": holder_classes_table,
        "update8_resolved_delta": resolved_delta,
        "metrics": table,
        "metric_deltas_vs_base": deltas,
        "per_root_free_coverage_gate": cov,
        "per_root_greedy": per_root_greedy,
        "group_best_options_nonfree": group_best_nonfree,
        "win_hit_groups_detail": win_hit_detail,
        "per_root_greedy_scheduling_movers": greedy_movers,
        "excluded_now_counts": {n: published[n]["class_status_counts"]["excluded_now"]
                               for n in ["BASE"] + list(SCEN)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    compact = {
        "metrics": {m: t for m, t in table.items()},
        "per_batch_class_unknown_now": class_table,
        "holder_classes_unknown_now": holder_classes_table,
        "update8_resolved_delta": resolved_delta,
        "excluded_now_flips": out["excluded_now_flips"],
        "holder_union_size": len(holder_union),
        "eligible_flip_union_size": len(eligible_union),
        "multi_win_holder_classes": out["holders_summary"]["multi_win_holder_classes"],
        "per_root_free_coverage_gate": {n: {"identical": c["free_coverage_columns_identical_to_base"],
                                            "root27_119": c["root27_119_of_119"],
                                            "greedy_moved": len(c["individual_greedy_union_moved_roots"])}
                                        for n, c in cov.items()},
        "greedy_scheduling_movers": {r: {k: v for k, v in row.items() if k.endswith("delta") or k == "base"}
                                     for r, row in greedy_movers.items() if row["PWIN2_delta"] != 0},
    }
    print(json.dumps(compact, indent=1))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
