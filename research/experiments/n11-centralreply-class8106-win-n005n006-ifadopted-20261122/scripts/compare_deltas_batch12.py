#!/usr/bin/env python3
"""Batch-12 (class 8106) n005/n006 WIN-vs-LOSS decomposition delta extractor.

Fail-closed, analysis-only. Reads the baseline (Part Y re-audit) refresh
outputs and the three batch-12 IF-ADOPTED scenario outputs:

  * PWIN2   = base + 2 WIN rows (n005/n006) only
  * PLOSS6  = base + 6 LOSS rows only (n001-n004/n007/n008)
  * PFULL8  = base + all 8 probed rows

The refresh semantics of the published Part Y scenario script are re-executed
faithfully for the base and each scenario cache (graph + update8 receipt +
cache verdicts, per-class verdict-level status, Board fail-closed
verification for free candidates) and every recomputed class_status_count is
asserted byte-equal to the published summary before any delta is reported.

Emitted deltas (machine-identified, no hand annotation):
  * excluded_now flip sets vs base and win-only (PFULL8 minus PLOSS6),
    cross-checked against the frozen graph holders of BOTH WIN S5 children
    (n005 s5 188395, n006 s5 219608, membership_class_count 3 each; the two
    holder triples share only class 8106 itself, so the expected union is 5),
  * update8 newly-resolved baseline-requirement indices per scenario, gated
    to the increment rows actually present (PWIN2 =2, PLOSS6 =6, PFULL8 =8),
  * metric/additivity observations and per-root free-coverage gates: per-root
    (free_now, uncovered) must be unchanged in every scenario; the
    per-root individual_greedy_union scheduling sizes are MEASURED (they do
    move: this is the first decomposition packet with a multi-WIN increment),
  * per-root greedy tables and win-hit-group details per scenario.

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

BASE_DIR = ROOT / "research/experiments/n11-class8106-n005n006-base-control-20261122/output"
REAUDIT = ROOT / "research/experiments/n11-central-reply-8784-closure-reaudit-20261122/output"
SCEN = {
    "PWIN2": EXP / "pwin2/output",
    "PLOSS6": EXP / "ploss6/output",
    "PFULL8": EXP / "pfull8/output",
}
INCR = {
    "PWIN2": EXP / "output/increment-batch12-winn005n006-only-IFADOPTED-20261122.cache",
    "PLOSS6": EXP / "output/increment-batch12-loss6-only-IFADOPTED-20261122.cache",
    "PFULL8": EXP / "output/increment-batch12-probed-8rows-IFADOPTED-20261122.cache",
}
INCR_SHA = {
    "PWIN2": "dd5fc998af17c3c3acdf89f3bbbbbf2d9e94280baff70ee6ff54d3b0759eef5d",
    "PLOSS6": "d18ddaf8d5f12b425591597faab3f728e6cea5478b69288ff295ce2cd5f166b6",
    "PFULL8": "d1954280f21b16bca20b4da42570e576e41b64cb3fe6e19de05c537658012def",
}
SCEN_CACHE = {
    "PWIN2": ("cache-pwin2-IFADOPTED.cache",
              "c13f81d75f3837b1331f05742d046fac9ae3b3821c24ec26a311833ae4bbf986"),
    "PLOSS6": ("cache-ploss6-IFADOPTED.cache",
               "898ca5f48d78f2eaf628e45bea8d1454278d95e54c34c7c5a68325cba7b6e883"),
    "PFULL8": ("cache-pfull8-IFADOPTED.cache",
               "21bbef33b8b8fa575217397d81a9366b9788b6c336337dae6f71e9ac6fe64c6f"),
}
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
UPDATE8 = ROOT / "research/experiments/n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"
POLICY = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BASE_CACHE = REAUDIT / "merged-exact-s5-chain-plus-closure-increment-plus-batch10-20261122.cache"
BATCH_KEYS = ROOT / "research/experiments/n11-centralreply-closure-class8106-batch12-20261122/input/batch-keys.json"
WIN_KEYS = {"n005": 188395, "n006": 219608}
WIN_ROWS = {
    "n006": "s5verdict,1152926194711134208,128,5,1,3695373",
    "n005": "s5verdict,1153489144664555520,0,5,1,12863268",
}
OUT = EXP / "output/decomp-deltas-batch12.json"

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
    win_row_text = [l for l in INCR["PWIN2"].read_text().splitlines()
                    if l.startswith("s5verdict")]
    if win_row_text != [WIN_ROWS["n006"], WIN_ROWS["n005"]]:
        fail(f"win increment rows mismatch: {win_row_text}")
    if any(v[0] != 2 for v in incr_rows["PLOSS6"].values()):
        fail("loss6 increment contains a non-LOSS verdict")
    if (set(incr_rows["PLOSS6"]) | set(incr_rows["PWIN2"])) != set(incr_rows["PFULL8"]):
        fail("PFULL8 rows != PWIN2 + PLOSS6 rows")
    if len(incr_rows["PWIN2"]) != 2 or len(incr_rows["PLOSS6"]) != 6 or len(incr_rows["PFULL8"]) != 8:
        fail("increment row counts not 2/6/8")

    keys = json.loads(BATCH_KEYS.read_text())["keys"]
    by_id = {k["key_id"]: k for k in keys}
    for kid, s5i in WIN_KEYS.items():
        wk = by_id[kid]
        if wk["s5_index"] != s5i:
            fail(f"{kid} batch-keys s5 mismatch")
    memberships = {kid: by_id[kid]["membership_class_count"] for kid in WIN_KEYS}
    if len(keys) != 52:
        fail(f"batch-keys universe is not 52 keys: {len(keys)}")
    win_universe_keys = [(int(by_id[k]["lo"]), int(by_id[k]["hi"])) for k in WIN_KEYS]
    for k in win_universe_keys:
        if k not in incr_rows["PWIN2"]:
            fail(f"win increment key mismatch {k}")

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

    # graph-side machine identification of the two WIN cost-child holder sets
    holders = {}
    for kid, s5i in WIN_KEYS.items():
        hs = [i for i, c in enumerate(s4_cost) if s5i in c]
        if len(hs) != memberships[kid]:
            fail(f"{kid} graph holders {hs} vs membership_class_count {memberships[kid]}")
        holders[kid] = sorted(hs)
    statuses = {i: s4_status[i] for h in holders.values() for i in h}
    holder_union = sorted(set().union(*[set(h) for h in holders.values()]))
    holder_overlap = sorted(set(holders["n005"]) & set(holders["n006"]))
    if len(holder_union) != sum(memberships.values()) - len(holder_overlap):
        fail("holder union size inconsistent with memberships minus pairwise overlap")
    if 8106 not in holder_overlap:
        fail("holder overlap does not contain batch class 8106 itself")

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
    win_only = sorted(excluded_now_sets["PFULL8"] - excluded_now_sets["PLOSS6"])
    if flips["PWIN2"] != holder_union:
        fail(f"PWIN2 excluded_now flips {flips['PWIN2']} != graph holder union {holder_union}")
    if flips["PLOSS6"]:
        fail(f"PLOSS6 excluded_now flips non-empty: {flips['PLOSS6']}")
    if win_only != holder_union:
        fail(f"win-only excluded_now delta {win_only} != graph holder union {holder_union}")
    if flips["PFULL8"] != sorted(set(flips["PLOSS6"]) | set(flips["PWIN2"])):
        fail(f"PFULL8 flips != union: {flips['PFULL8']}")

    # graph-level cross checks on the holders and the batch class
    base_iv = verdicts_for(base_cache)
    batch_s5 = {k["s5_index"] for k in keys}
    rem_8106 = [j for j in s4_cost[8106] if base_iv.get(j) is None]
    if set(rem_8106) != batch_s5:
        fail(f"class 8106 base-remaining cost != batch-keys universe ({len(rem_8106)} rows)")
    holder_rem = {}
    for kid, hs in holders.items():
        for i in hs:
            if WIN_KEYS[kid] not in s4_cost[i]:
                fail(f"holder {i} does not contain {kid} s5 index")
            if s4_status[i] not in (0, 1):
                fail(f"holder {i} unexpected base graph status {s4_status[i]}")
            holder_rem.setdefault(i, [j for j in s4_cost[i] if base_iv.get(j) is None])
            if WIN_KEYS[kid] not in holder_rem[i]:
                fail(f"holder {i} does not have {kid} unresolved at base")

    table = {}
    for metric, fn in METRICS:
        table[metric] = {"base": fn(published["BASE"])}
        for name in SCEN:
            table[metric][name] = fn(published[name])

    # class 8106 unknown_now from the faithful recompute
    c8106 = {name: recomputed[name][1].get(8106) for name in ["BASE"] + list(SCEN)}
    if c8106["PWIN2"] != c8106["BASE"] - 2:
        fail(f"class 8106 PWIN2 unknown_now {c8106['PWIN2']} != base-2")
    if c8106["PLOSS6"] != c8106["BASE"] - 6:
        fail(f"class 8106 PLOSS6 unknown_now {c8106['PLOSS6']} != base-6")
    if c8106["PFULL8"] != c8106["BASE"] - 8:
        fail(f"class 8106 PFULL8 unknown_now {c8106['PFULL8']} != base-8")
    additivity_class = {
        "base": c8106["BASE"], "PWIN2": c8106["PWIN2"],
        "PLOSS6": c8106["PLOSS6"], "PFULL8": c8106["PFULL8"],
        "full_equals_win_plus_loss":
            (c8106["BASE"] - c8106["PWIN2"]) + (c8106["BASE"] - c8106["PLOSS6"])
            == c8106["BASE"] - c8106["PFULL8"],
    }
    if not additivity_class["full_equals_win_plus_loss"]:
        fail(f"class 8106 unknown additivity violated: {additivity_class}")

    # update8 resolved-requirement delta, machine-identified
    base_resolved = set(published["BASE"]["frozen_update8_refresh"]["resolved_among_baseline_requirement"])
    loss_universe = {mask_to_index[(v_lo, v_hi)] for (v_lo, v_hi) in incr_rows["PLOSS6"]
                     if (v_lo, v_hi) in mask_to_index}
    win_universe = {mask_to_index[k] for k in incr_rows["PWIN2"] if k in mask_to_index}
    resolved_delta = {}
    for name in SCEN:
        s = published[name]["frozen_update8_refresh"]
        new = sorted(set(s["resolved_among_baseline_requirement"]) - base_resolved)
        lost = sorted(base_resolved - set(s["resolved_among_baseline_requirement"]))
        if lost:
            fail(f"{name}: resolved set shrank: {lost}")
        if name == "PWIN2":
            pool = win_universe
        elif name == "PLOSS6":
            pool = loss_universe
        else:
            pool = set(loss_universe) | win_universe
        for idx in new:
            if idx not in pool:
                fail(f"{name}: newly resolved s5 {idx} outside its increment universe")
        resolved_delta[name] = {"newly_resolved_s5": new, "count": len(new)}
    if resolved_delta["PWIN2"]["count"] != 2 or resolved_delta["PLOSS6"]["count"] != 6 \
            or resolved_delta["PFULL8"]["count"] != 8:
        fail(f"update8 newly-resolved counts not 2/6/8: {resolved_delta}")

    additivity = {}
    for metric, _ in METRICS:
        t = table[metric]
        w = t["PWIN2"] - t["base"]
        l = t["PLOSS6"] - t["base"]
        f = t["PFULL8"] - t["base"]
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
    greedy_root_deltas = {"PWIN2": {}, "PLOSS6": {}, "PFULL8": {}}
    for name, d in SCEN.items():
        prc = {}
        with (d / "per-root-coverage.csv").open() as fh:
            for r in csv.DictReader(fh):
                prc[(r["role"], r["first"])] = (r["free_now"], r["uncovered"], r["individual_greedy_union"])
        roots = {(r["role"], r.get("origin_first")): (r["free_thirds_now"], r["uncovered"])
                 for r in published[name]["roots"]}
        ok = roots == base_roots
        if not ok:
            fail(f"per-root roots free coverage gate broken in {name}")
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
            "individual_greedy_union_moved_roots": moved,
        }
    # greedy additivity per moved root
    greedy_additivity = {}
    for k in sorted(set(greedy_root_deltas["PWIN2"]) | set(greedy_root_deltas["PLOSS6"])
                    | set(greedy_root_deltas["PFULL8"])):
        d5 = greedy_root_deltas["PWIN2"].get(k, {}).get("delta", 0)
        d6 = greedy_root_deltas["PLOSS6"].get(k, {}).get("delta", 0)
        d8 = greedy_root_deltas["PFULL8"].get(k, {}).get("delta", 0)
        greedy_additivity[k] = {"win_delta": d5, "loss_delta": d6, "full_delta": d8,
                                "full_eq_win_plus_loss": d5 + d6 == d8}

    # per-root greedy + win-hit groups (scheduling quantities, measured to
    # document the joint interaction of this first multi-WIN packet)
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
                            if row["PFULL8_delta"] != row["PWIN2_delta"] + row["PLOSS6_delta"]}

    out = {
        "schema": "n11-class8106-batch12-decomp-deltas-v1",
        "interpretation_guard": ("read-only what-if IF-ADOPTED planning deltas; "
                                 "verdicts NOT consumed; scheduling quantities only; "
                                 "11x11 empty board and all roots stay UNKNOWN"),
        "recompute_gates": ("class statuses, free-candidate board verification and all "
                            "class_status_counts re-executed from graph+update8+cache and "
                            "asserted equal to the published summaries for BASE and all "
                            "three scenarios before any delta was emitted"),
        "win_keys": {
            "n005": {
                "s5_index": WIN_KEYS["n005"],
                "increment_row": WIN_ROWS["n005"],
                "graph_cost_child_holder_classes": holders["n005"],
                "membership_class_count": memberships["n005"],
            },
            "n006": {
                "s5_index": WIN_KEYS["n006"],
                "increment_row": WIN_ROWS["n006"],
                "graph_cost_child_holder_classes": holders["n006"],
                "membership_class_count": memberships["n006"],
            },
            "holder_union": holder_union,
            "holder_overlap": holder_overlap,
            "overlap_note": ("the two WIN holder triples (sizes 3+3) share exactly "
                             "one class: batch class 8106 itself, so the union is 5 "
                             "classes, all baseline UNKNOWN at the frozen graph"),
        },
        "holders_detail": {
            "holder_graph_statuses": {str(i): statuses[i] for i in sorted(holder_union)},
            "holder_base_remaining_unknown_sizes": {str(i): len(holder_rem[i]) for i in sorted(holder_union)},
            "peer_holder_remaining_s5": {str(i): sorted(holder_rem[i]) for i in sorted(holder_union) if i != 8106},
            "exclusion_note": ("per the published refresh semantics a baseline "
                               "UNKNOWN class with any WIN cost child becomes "
                               "excluded_now regardless of remaining unknown "
                               "children; the WIN-only flips are therefore the "
                               "5-class holder union: batch class 8106 itself "
                               "(52 -> 44 unknown after the full increment) plus "
                               "peer holders 5007/5011 (n005) and 6147/6166 (n006)"),
        },
        "probed_note": ("batch 12 probed 8/52 (two waves n001-n004 and n005-n008, "
                        "WIN-HALT x2 on n005/n006); no exhaustion rows exist in this "
                        "batch, hence every increment contains only 2-pass resolved rows"),
        "excluded_now_flips": {
            "PWIN2": flips["PWIN2"], "PLOSS6": flips["PLOSS6"],
            "PFULL8": flips["PFULL8"],
            "win_only_pf8_minus_ploss6": win_only,
            "all_equal_holder_union": (flips["PWIN2"] == holder_union
                                       and win_only == holder_union),
        },
        "class8106_unknown_now": additivity_class,
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
        "class8106_unknown_now": additivity_class,
        "update8_resolved_delta": resolved_delta,
        "excluded_now_flips": out["excluded_now_flips"],
        "per_root_free_coverage_gate": {n: {"identical": c["free_coverage_columns_identical_to_base"],
                                            "greedy_moved": len(c["individual_greedy_union_moved_roots"])}
                                        for n, c in cov.items()},
        "greedy_union_column_additivity": greedy_additivity,
        "greedy_nonadditive_roots": {r: {k: v for k, v in row.items() if k in ("base", "PWIN2", "PLOSS6", "PFULL8")}
                                     for r, row in greedy_anomaly_roots.items()},
    }
    print(json.dumps(compact, indent=1))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
