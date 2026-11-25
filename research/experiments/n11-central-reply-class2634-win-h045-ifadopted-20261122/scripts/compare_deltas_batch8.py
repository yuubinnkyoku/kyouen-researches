#!/usr/bin/env python3
"""Batch-8 (class 2634) WIN-vs-LOSS decomposition delta extractor.

Fail-closed, analysis-only. Reads the baseline re-audit refresh outputs and the
three batch-8 IF-ADOPTED scenario outputs:

  * PW045    = base + h045 WIN row only   (cache-pwinh045-IFADOPTED.cache)
  * PLOSS43  = base + 43 LOSS rows only   (cache-ploss43-IFADOPTED.cache)
  * PFULL44  = base + all 44 resolved rows(cache-pfull44-IFADOPTED.cache)

The refresh semantics of the published Part M script are re-executed faithfully
for the base and each scenario cache (graph + update8 receipt + cache verdicts,
per-class verdict-level status, Board fail-closed verification for free
candidates) and every recomputed class_status_count is asserted byte-equal to
the published summary before any delta is reported.

Emitted deltas (machine-identified, no hand annotation):
  * excluded_now flip sets vs base and win-only (PFULL44 minus PLOSS43),
    cross-checked against the frozen graph holders of the h045 S5 child
    103558 and the batch-keys membership_class_count (== 2),
  * update8 newly-resolved baseline-requirement indices per scenario,
    gated to the increment rows actually present,
  * metric/additivity observations and per-root free-coverage gates.

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

BASE_DIR = ROOT / "research/experiments/n11-class2634-base-control-20261122/output"
REAUDIT = ROOT / "research/experiments/n11-central-reply-10324-closure-reaudit-20261122/output"
SCEN = {
    "PW045": EXP / "pwinh045/output",
    "PLOSS43": EXP / "ploss43/output",
    "PFULL44": EXP / "pfull44/output",
}
INCR = {
    "PW045": EXP / "output/increment-batch8-winh045-only-IFADOPTED-20261122.cache",
    "PLOSS43": EXP / "output/increment-batch8-loss43-only-IFADOPTED-20261122.cache",
    "PFULL44": EXP / "output/increment-batch8-probed-44rows-IFADOPTED-20261122.cache",
}
INCR_SHA = {
    "PW045": "7a5e05499027efa76cf507e06f99f6b3adcbe2adbf450212a1cd92632a3217f2",
    "PLOSS43": "73f01e74b4cdf3fe5029c3a0011f323bf4ba35758c12c9755e2a628c8ef891f8",
    "PFULL44": "356b62a71d62ea77e4071d687eca794c835b9dbcea58143e18355e39203827f3",
}
SCEN_CACHE = {
    "PW045": ("cache-pwinh045-IFADOPTED.cache",
              "1b84db115bfc68fde9f9e9000ff3250d3ed2b279d508174f38e979a40ce9b2b1"),
    "PLOSS43": ("cache-ploss43-IFADOPTED.cache",
                "0020b89d8a77e2a5350fca78442eec3eea6969056c91177e4d87c661cbc8ecfe"),
    "PFULL44": ("cache-pfull44-IFADOPTED.cache",
                "9235e54786a895c37e42076089a675a93d27adc5af3c2aa326f698408ca0a6cd"),
}
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_CACHE = REAUDIT / "merged-exact-s5-chain-plus-closure-increment-plus-batch7-20261122.cache"
BATCH_KEYS = ROOT / "research/experiments/n11-centralreply-closure-class2634-batch8-20261122/input/batch-keys.json"
H045_S5_INDEX = 103558
H045_ROW = "s5verdict,4035225266258182144,64,5,1,6366900"
OUT = EXP / "output/decomp-deltas-batch8.json"

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
    win_row_text = [l for l in INCR["PW045"].read_text().splitlines()
                    if l.startswith("s5verdict")]
    if win_row_text != [H045_ROW]:
        fail(f"h045 increment row mismatch: {win_row_text}")
    if any(v[0] != 2 for v in incr_rows["PLOSS43"].values()):
        fail("loss43 increment contains a non-LOSS verdict")
    if (set(incr_rows["PLOSS43"]) | set(incr_rows["PW045"])) != set(incr_rows["PFULL44"]):
        fail("PFULL44 rows != PW045 + PLOSS43 rows")

    keys = json.loads(BATCH_KEYS.read_text())["keys"]
    win_key = [k for k in keys if k["key_id"] == "h045"][0]
    if win_key["s5_index"] != H045_S5_INDEX or win_key["membership_class_count"] != 2:
        fail("h045 batch-keys metadata mismatch")
    membership_expected = win_key["membership_class_count"]
    if (4035225266258182144, 64) not in incr_rows["PW045"]:
        fail("h045 increment key mismatch")

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

    # graph-side machine identification of the h045 cost-child holders
    holders = [i for i, c in enumerate(s4_cost) if H045_S5_INDEX in c]
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
    win_only = sorted(excluded_now_sets["PFULL44"] - excluded_now_sets["PLOSS43"])
    if flips["PW045"] != sorted(holders):
        fail(f"PW045 excluded_now flips {flips['PW045']} != graph holders {sorted(holders)}")
    if flips["PLOSS43"]:
        fail(f"PLOSS43 excluded_now flips non-empty: {flips['PLOSS43']}")
    if win_only != sorted(holders):
        fail(f"win-only excluded_now delta {win_only} != graph holders {sorted(holders)}")
    if flips["PFULL44"] != sorted(set(flips["PLOSS43"]) | set(holders)):
        fail(f"PFULL44 flips != union: {flips['PFULL44']}")

    # graph-level cross checks on the holders
    base_iv = verdicts_for(base_cache)
    batch_s5 = {k["s5_index"] for k in keys}
    rem_2634 = [j for j in s4_cost[2634] if base_iv.get(j) is None]
    if set(rem_2634) != batch_s5:
        fail(f"class 2634 base-remaining cost != batch-keys universe ({len(rem_2634)} rows)")
    holder_rem = {}
    for i in holders:
        if H045_S5_INDEX not in s4_cost[i]:
            fail(f"holder {i} does not contain h045 s5 index")
        if s4_status[i] not in (0, 1):
            fail(f"holder {i} unexpected base graph status {s4_status[i]}")
        holder_rem[i] = [j for j in s4_cost[i] if base_iv.get(j) is None]
        if H045_S5_INDEX not in holder_rem[i]:
            fail(f"holder {i} does not have h045 unresolved at base")

    table = {}
    for metric, fn in METRICS:
        table[metric] = {"base": fn(published["BASE"])}
        for name in SCEN:
            table[metric][name] = fn(published[name])

    # class 2634 unknown_now from the faithful recompute
    c2634 = {name: recomputed[name][1].get(2634) for name in ["BASE"] + list(SCEN)}
    if c2634["PW045"] != c2634["BASE"] - 1:
        fail(f"class 2634 PW045 unknown_now {c2634['PW045']} != base-1")
    if c2634["PLOSS43"] > c2634["BASE"] or c2634["PFULL44"] > c2634["PLOSS43"]:
        fail(f"class 2634 unknown_now monotonicity violated: {c2634}")
    additivity_class = {
        "base": c2634["BASE"], "PW045": c2634["PW045"],
        "PLOSS43": c2634["PLOSS43"], "PFULL44": c2634["PFULL44"],
        "full_equals_win_plus_loss":
            (c2634["BASE"] - c2634["PW045"]) + (c2634["BASE"] - c2634["PLOSS43"])
            == c2634["BASE"] - c2634["PFULL44"],
    }
    if not additivity_class["full_equals_win_plus_loss"]:
        fail(f"class 2634 unknown additivity violated: {additivity_class}")

    # update8 resolved-requirement delta, machine-identified
    base_resolved = set(published["BASE"]["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    loss_universe = {mask_to_index[(v_lo, v_hi)] for (v_lo, v_hi) in incr_rows["PLOSS43"]
                     if (v_lo, v_hi) in mask_to_index}
    win_universe = {mask_to_index[k] for k in incr_rows["PW045"] if k in mask_to_index}
    resolved_delta = {}
    for name in SCEN:
        s = published[name]["frozen_update8_refresh"]
        new = sorted(set(s["resolved_among_baseline_requirement"]) - base_resolved)
        lost = sorted(base_resolved - set(s["resolved_among_baseline_requirement"]))
        if lost:
            fail(f"{name}: resolved set shrank: {lost}")
        pool = win_universe if name == "PW045" else set(loss_universe) | (win_universe if name == "PFULL44" else set())
        for idx in new:
            if idx not in pool:
                fail(f"{name}: newly resolved s5 {idx} outside its increment universe")
        resolved_delta[name] = {"newly_resolved_s5": new, "count": len(new)}

    additivity = {}
    for metric, _ in METRICS:
        t = table[metric]
        w = t["PW045"] - t["base"]
        l = t["PLOSS43"] - t["base"]
        f = t["PFULL44"] - t["base"]
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

    out = {
        "schema": "n11-class2634-batch8-decomp-deltas-v1",
        "interpretation_guard": ("read-only what-if IF-ADOPTED planning deltas; "
                                 "verdicts NOT consumed; scheduling quantities only; "
                                 "11x11 empty board and all roots stay UNKNOWN"),
        "recompute_gates": ("class statuses, free-candidate board verification and all "
                            "class_status_counts re-executed from graph+update8+cache and "
                            "asserted equal to the published summaries for BASE and all "
                            "three scenarios before any delta was emitted"),
        "h045": {
            "s5_index": H045_S5_INDEX,
            "increment_row": H045_ROW,
            "graph_cost_child_holder_classes": sorted(holders),
            "holder_graph_statuses": {str(i): statuses[i] for i in sorted(holders)},
            "holder_base_remaining_unknown_sizes": {str(i): len(holder_rem[i]) for i in sorted(holders)},
            "peer_holder_remaining_s5": {str(i): sorted(holder_rem[i]) for i in sorted(holders) if i != 2634},
            "exclusion_note": ("per the published refresh semantics a baseline "
                               "UNKNOWN class with any WIN cost child becomes "
                               "excluded_now regardless of remaining unknown "
                               "children; the WIN-only flips therefore include "
                               "class 2634 itself (51 -> 50 unknown) and its "
                               "single peer holder"),
            "membership_class_count": membership_expected,
            "batch8_win_row": "h045 (probe_order 325, 2-pass node-exact, nodes 6366900, WIN-HALT pre-registered rule)",
        },
        "h002_note": ("budget-exhaustion UNKNOWN row (s5 11390, 15M, result 0) is excluded "
                      "from every increment; not a verdict; not re-searched here"),
        "excluded_now_flips": {
            "PW045": flips["PW045"], "PLOSS43": flips["PLOSS43"],
            "PFULL44": flips["PFULL44"],
            "win_only_pf44_minus_ploss43": win_only,
            "all_equal_membership_count_2": (len(flips["PW045"]) == membership_expected
                                             and win_only == sorted(holders)),
        },
        "class2634_unknown_now": additivity_class,
        "update8_resolved_delta": resolved_delta,
        "metrics": table,
        "additivity_measured": additivity,
        "per_root_free_coverage_gate": cov,
        "excluded_now_counts": {n: published[n]["class_status_counts"]["excluded_now"]
                                for n in ["BASE"] + list(SCEN)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    compact = {
        "metrics": {m: t for m, t in table.items()},
        "class2634_unknown_now": additivity_class,
        "update8_resolved_delta": resolved_delta,
        "excluded_now_flips": out["excluded_now_flips"],
    }
    print(json.dumps(compact, indent=1))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
