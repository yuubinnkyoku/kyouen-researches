#!/usr/bin/env python3
"""Batch-11 (class 8785) z003 WIN-vs-LOSS decomposition delta extractor.

Fail-closed, analysis-only. Reads the baseline (Part Y re-audit) refresh
outputs and the three batch-11 IF-ADOPTED scenario outputs:

  * PWINZ003 = base + z003 WIN row only      (cache-pwinz003-IFADOPTED.cache)
  * PLOSS3   = base + 3 LOSS rows only       (cache-ploss3-IFADOPTED.cache)
  * PFULL4   = base + all 4 probed rows      (cache-pfull4-IFADOPTED.cache)

The refresh semantics of the published Part Y scenario script are re-executed
faithfully for the base and each scenario cache (graph + update8 receipt +
cache verdicts, per-class verdict-level status, Board fail-closed
verification for free candidates) and every recomputed class_status_count is
asserted byte-equal to the published summary before any delta is reported.

Emitted deltas (machine-identified, no hand annotation):
  * excluded_now flip sets vs base and win-only (PFULL4 minus PLOSS3),
    cross-checked against the frozen graph holders of the z003 S5 child
    198530 and the batch-keys membership_class_count (== 3),
  * update8 newly-resolved baseline-requirement indices per scenario,
    gated to the increment rows actually present,
  * metric/additivity observations and per-root free-coverage gates,
  * per-root greedy tables per scenario (scheduling quantities; measured to
    document the non-additive joint-greedy interaction of this packet).

The increments are read-only what-if analysis inputs; no verdict is consumed
and no class, root, coverage or closure claim is made. 11x11 stays UNKNOWN.
"""
import csv
import gzip
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]

BASE_DIR = ROOT / "research/experiments/n11-class8785-z003-base-control-20261122/output"
REAUDIT = ROOT / "research/experiments/n11-central-reply-8784-closure-reaudit-20261122/output"
SCEN = {
    "PWINZ003": EXP / "pwinz003/output",
    "PLOSS3": EXP / "ploss3/output",
    "PFULL4": EXP / "pfull4/output",
}
INCR = {
    "PWINZ003": EXP / "output/increment-batch11-winz003-only-IFADOPTED-20261122.cache",
    "PLOSS3": EXP / "output/increment-batch11-loss3-only-IFADOPTED-20261122.cache",
    "PFULL4": EXP / "output/increment-batch11-probed-4rows-IFADOPTED-20261122.cache",
}
INCR_SHA = {
    "PWINZ003": "32c582c1c476ba5d737686f4d261b79612363ed13c39a7c3afc6753437a34377",
    "PLOSS3": "939f8deba2389fcf0cbd69a0c8e27f212ab967416770e3f5d0366ecf2bcb3096",
    "PFULL4": "2778d392255827ec9705ba0dcf241baba12d4662ef369cd0c50e698ce31b7a46",
}
SCEN_CACHE = {
    "PWINZ003": ("cache-pwinz003-IFADOPTED.cache",
                 "3fcdbfd090e64144f458d3eb5f28086e6026e000c5f24aecca4a34f38173a882"),
    "PLOSS3": ("cache-ploss3-IFADOPTED.cache",
               "ba08f924153f19275b03137c943dde9edeb4b0a3afa45a9ef2755875d376ef75"),
    "PFULL4": ("cache-pfull4-IFADOPTED.cache",
               "c5044be884211755c8b06cbc1b699fa51b5f7710192174f306e6b21550b88cae"),
}
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_CACHE = REAUDIT / "merged-exact-s5-chain-plus-closure-increment-plus-batch10-20261122.cache"
BATCH_KEYS = ROOT / "research/experiments/n11-centralreply-closure-class8785-batch11-20261122/input/batch-keys.json"
Z003_S5_INDEX = 198530
Z003_ROW = "s5verdict,1225542323476103168,1,5,1,11601265"
OUT = EXP / "output/decomp-deltas-batch11.json"

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
        if sha(SCEN[name] / fname) != want:
            fail(f"{name} cache sha drift")
    for name, p in INCR.items():
        if sha(p) != INCR_SHA[name]:
            fail(f"{name} increment sha drift")

    incr_rows = {}
    for name, p in INCR.items():
        rows = read_cache(p)
        incr_rows[name] = rows
    win_row_text = [l for l in INCR["PWINZ003"].read_text().splitlines()
                    if l.startswith("s5verdict")]
    if win_row_text != [Z003_ROW]:
        fail(f"z003 increment row mismatch: {win_row_text}")
    if any(v[0] != 2 for v in incr_rows["PLOSS3"].values()):
        fail("loss3 increment contains a non-LOSS verdict")
    if (set(incr_rows["PLOSS3"]) | set(incr_rows["PWINZ003"])) != set(incr_rows["PFULL4"]):
        fail("PFULL4 rows != PWINZ003 + PLOSS3 rows")
    if len(incr_rows["PWINZ003"]) != 1 or len(incr_rows["PLOSS3"]) != 3 or len(incr_rows["PFULL4"]) != 4:
        fail("increment row counts not 1/3/4")

    keys = json.loads(BATCH_KEYS.read_text())["keys"]
    win_key = [k for k in keys if k["key_id"] == "z003"][0]
    if win_key["s5_index"] != Z003_S5_INDEX or win_key["membership_class_count"] != 3:
        fail("z003 batch-keys metadata mismatch")
    membership_expected = win_key["membership_class_count"]
    if (1225542323476103168, 1) not in incr_rows["PWINZ003"]:
        fail("z003 increment key mismatch")
    if len(keys) != 51:
        fail(f"batch-keys universe is not 51 keys: {len(keys)}")

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
    receipt_verdicts = {int(k): int(v) for k, v in update8["resolved_s5_verdicts"].items()}

    base_cache = read_cache(BASE_CACHE)
    scenarios_cache = {name: read_cache(SCEN[name] / fname)
                        for name, (fname, _) in SCEN_CACHE.items()}

    # graph-side machine identification of the z003 cost-child holders
    holders = [i for i, c in enumerate(s4_cost) if Z003_S5_INDEX in c]
    statuses = {i: s4_status[i] for i in holders}
    if len(holders) != membership_expected:
        fail(f"graph holders {holders} vs membership_class_count {membership_expected}")

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
        # Board fail-closed verification for free candidates
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

    # recomputed counts must equal published counts exactly
    for name in ["BASE"] + list(SCEN):
        st, _, _, counts = recomputed[name]
        pub = published[name]["class_status_counts"]
        want = dict(pub)
        # after the board pass, verified candidates are renamed 'free_now'
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
    win_only = sorted(excluded_now_sets["PFULL4"] - excluded_now_sets["PLOSS3"])
    if flips["PWINZ003"] != sorted(holders):
        fail(f"PWINZ003 excluded_now flips {flips['PWINZ003']} != graph holders {sorted(holders)}")
    if flips["PLOSS3"]:
        fail(f"PLOSS3 excluded_now flips non-empty: {flips['PLOSS3']}")
    if win_only != sorted(holders):
        fail(f"win-only excluded_now delta {win_only} != graph holders {sorted(holders)}")
    if flips["PFULL4"] != sorted(set(flips["PLOSS3"]) | set(holders)):
        fail(f"PFULL4 flips != union: {flips['PFULL4']}")

    # graph-level cross checks on the holders
    base_iv = verdicts_for(base_cache)
    batch_s5 = {k["s5_index"] for k in keys}
    rem_8785 = [j for j in s4_cost[8785] if base_iv.get(j) is None]
    if set(rem_8785) != batch_s5:
        fail(f"class 8785 base-remaining cost != batch-keys universe ({len(rem_8785)} rows)")
    holder_rem = {}
    for i in holders:
        if Z003_S5_INDEX not in s4_cost[i]:
            fail(f"holder {i} does not contain z003 s5 index")
        if s4_status[i] not in (0, 1):
            fail(f"holder {i} unexpected base graph status {s4_status[i]}")
        holder_rem[i] = [j for j in s4_cost[i] if base_iv.get(j) is None]
        if Z003_S5_INDEX not in holder_rem[i]:
            fail(f"holder {i} does not have z003 unresolved at base")

    table = {}
    for metric, fn in METRICS:
        table[metric] = {"base": fn(published["BASE"])}
        for name in SCEN:
            table[metric][name] = fn(published[name])

    # class 8785 unknown_now from the faithful recompute
    c8785 = {name: recomputed[name][1].get(8785) for name in ["BASE"] + list(SCEN)}
    if c8785["PWINZ003"] != c8785["BASE"] - 1:
        fail(f"class 8785 PWINZ003 unknown_now {c8785['PWINZ003']} != base-1")
    if c8785["PLOSS3"] != c8785["BASE"] - 3:
        fail(f"class 8785 PLOSS3 unknown_now {c8785['PLOSS3']} != base-3")
    if c8785["PFULL4"] != c8785["BASE"] - 4:
        fail(f"class 8785 PFULL4 unknown_now {c8785['PFULL4']} != base-4")
    additivity_class = {
        "base": c8785["BASE"], "PWINZ003": c8785["PWINZ003"],
        "PLOSS3": c8785["PLOSS3"], "PFULL4": c8785["PFULL4"],
        "full_equals_win_plus_loss":
            (c8785["BASE"] - c8785["PWINZ003"]) + (c8785["BASE"] - c8785["PLOSS3"])
            == c8785["BASE"] - c8785["PFULL4"],
    }
    if not additivity_class["full_equals_win_plus_loss"]:
        fail(f"class 8785 unknown additivity violated: {additivity_class}")

    # update8 resolved-requirement delta, machine-identified
    base_resolved = set(published["BASE"]["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    loss_universe = {mask_to_index[(v_lo, v_hi)] for (v_lo, v_hi) in incr_rows["PLOSS3"]
                     if (v_lo, v_hi) in mask_to_index}
    win_universe = {mask_to_index[k] for k in incr_rows["PWINZ003"] if k in mask_to_index}
    resolved_delta = {}
    for name in SCEN:
        s = published[name]["frozen_update8_refresh"]
        new = sorted(set(s["resolved_among_baseline_requirement"]) - base_resolved)
        lost = sorted(base_resolved - set(s["resolved_among_baseline_requirement"]))
        if lost:
            fail(f"{name}: resolved set shrank: {lost}")
        pool = win_universe if name == "PWINZ003" else set(loss_universe) | (win_universe if name == "PFULL4" else set())
        for idx in new:
            if idx not in pool:
                fail(f"{name}: newly resolved s5 {idx} outside its increment universe")
        resolved_delta[name] = {"newly_resolved_s5": new, "count": len(new)}

    additivity = {}
    for metric, _ in METRICS:
        t = table[metric]
        w = t["PWINZ003"] - t["base"]
        l = t["PLOSS3"] - t["base"]
        f = t["PFULL4"] - t["base"]
        additivity[metric] = {"win_delta": w, "loss_delta": l, "full_delta": f,
                              "full_eq_win_plus_loss": (w + l == f)}

    # per-root free coverage equality gates
    cov = {}
    base_prc = {}
    with (BASE_DIR / "per-root-coverage.csv").open() as fh:
        for r in csv.DictReader(fh):
            base_prc[(r["role"], r["first"])] = (r["free_now"], r["uncovered"])
    base_roots = {(r["role"], r.get("origin_first")): (r["free_thirds_now"], r["uncovered"])
                  for r in published["BASE"]["roots"]}
    for name, d in SCEN.items():
        prc = {}
        with (d / "per-root-coverage.csv").open() as fh:
            for r in csv.DictReader(fh):
                prc[(r["role"], r["first"])] = (r["free_now"], r["uncovered"])
        roots = {(r["role"], r.get("origin_first")): (r["free_thirds_now"], r["uncovered"])
                 for r in published[name]["roots"]}
        ok = roots == base_roots and prc == base_prc
        cov[name] = {"identical_to_base": ok}
        if not ok:
            fail(f"per-root free coverage gate broken in {name}")

    # per-root greedy + win-hit groups (scheduling quantities, measured to
    # document the non-additive joint-greedy interaction of this packet)
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
                            if row["PFULL4_delta"] != row["PWINZ003_delta"] + row["PLOSS3_delta"]}

    out = {
        "schema": "n11-class8785-batch11-decomp-deltas-v1",
        "interpretation_guard": ("read-only what-if IF-ADOPTED planning deltas; "
                                 "verdicts NOT consumed; scheduling quantities only; "
                                 "11x11 empty board and all roots stay UNKNOWN"),
        "recompute_gates": ("class statuses, free-candidate board verification and all "
                            "class_status_counts re-executed from graph+update8+cache and "
                            "asserted equal to the published summaries for BASE and all "
                            "three scenarios before any delta was emitted"),
        "z003": {
            "s5_index": Z003_S5_INDEX,
            "increment_row": Z003_ROW,
            "graph_cost_child_holder_classes": sorted(holders),
            "holder_graph_statuses": {str(i): statuses[i] for i in sorted(holders)},
            "holder_base_remaining_unknown_sizes": {str(i): len(holder_rem[i]) for i in sorted(holders)},
            "peer_holder_remaining_s5": {str(i): sorted(holder_rem[i]) for i in sorted(holders) if i != 8785},
            "exclusion_note": ("per the published refresh semantics a baseline "
                               "UNKNOWN class with any WIN cost child becomes "
                               "excluded_now regardless of remaining unknown "
                               "children; the WIN-only flips therefore include "
                               "class 8785 itself (51 -> 50 unknown) and its two "
                               "peer holders 5307 and 5748"),
            "membership_class_count": membership_expected,
            "batch11_win_row": "z003 (probe_order 334, 2-pass node-exact + 4-way cross-host agreement, nodes 11601265, WIN-HALT pre-registered rule)",
        },
        "probed_note": ("batch 11 probed 4/51 (first wave z001-z004; z005-z051 "
                        "untouched); no exhaustion rows exist in this batch, "
                        "hence every increment contains only 2-pass resolved rows"),
        "excluded_now_flips": {
            "PWINZ003": flips["PWINZ003"], "PLOSS3": flips["PLOSS3"],
            "PFULL4": flips["PFULL4"],
            "win_only_pf4_minus_ploss3": win_only,
            "all_equal_membership_count_3": (len(flips["PWINZ003"]) == membership_expected
                                             and win_only == sorted(holders)),
        },
        "class8785_unknown_now": additivity_class,
        "update8_resolved_delta": resolved_delta,
        "metrics": table,
        "additivity_measured": additivity,
        "per_root_free_coverage_gate": cov,
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
        "class8785_unknown_now": additivity_class,
        "update8_resolved_delta": resolved_delta,
        "excluded_now_flips": out["excluded_now_flips"],
        "greedy_nonadditive_roots": {r: {"base": v["base"], "PWINZ003": v["PWINZ003"], "PLOSS3": v["PLOSS3"], "PFULL4": v["PFULL4"]} for r, v in greedy_anomaly_roots.items()},
    }
    print(json.dumps(compact, indent=1))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
