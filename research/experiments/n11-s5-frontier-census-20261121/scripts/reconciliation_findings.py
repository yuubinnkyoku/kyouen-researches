#!/usr/bin/env python3
"""Cross-lane reconciliation findings at the pinned Nov 21 reply27 state.

Secondary measurement over published first-order artifacts. No verdict claim,
no cache write, no rehabilitation. Fail-closed.

Sections:
  A. proxy-vs-actual calibration for every published JS-replica probe raw
     (2M and 15M stages) plus the two two-target-design C++ published raws.
  B. Historical-backlog reconciliation for the current chain: the union-
     audit's "backward only" rows (exact/merged historical verdicts absent
     from the pinned chain and not quarantined) intersected with the active
     two-target supply:
       - per-live-class decrements if the historical rows were adopted,
       - overlap with the focus-class lane's 35 declared keys,
       - overlap with the reply27 JS-replica lane's 13 published targets,
       - if-adopted class status recomputation (measurement only).
"""
from __future__ import annotations

import collections
import csv
import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
from s5_evidence_policy import quarantined_cache_keys  # noqa: E402

GEOMETRY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
HISTORY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/history.json"
PROFILE = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/historical-cost-profile.json"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
CHAIN_CACHE = ROOT / "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/merged-exact-s5-after-js-probe-13.cache"
UNION_AUDIT = ROOT / "research/experiments/n11-s5-frontier-census-20261121/output/global-union-audit.json"
PROBE_DIRS = sorted((ROOT / "research/experiments").glob("n11-reply27-s5-jsreplica-probe-*-20261121"))
TWO_TARGET_RAW = ROOT / "research/experiments/n11-two-target-design-20261010/output/raw"

PIN = {
    "geometry_json_gz": "146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54",
    "quarantine_registry": "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9",
    "probe13_cache": "60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6",
}
FOCUS_CLASS = (1188950301626859520, 536870912)
FOCUS_DECLARED_35 = [
    (1152921504606851072, 536870922), (1152921504606851072, 536870978), (1152921504606851072, 536936450), (1152921504606851072, 537001986), (1152921504606851072, 570425346), (1188950301626859520, 536870913), (1188950301626859520, 536870976), (1188950301626859520, 537133056), (1188950301626859520, 603979776), (1188950301626863616, 536870912), (1188950301626892288, 536870912), (1188950301643636736, 536870912), (1188950310216794112, 536870912), (1188950576504766464, 536870912), (1188951401138487296, 536870912), (1189091039115214848, 536870912), (1197957500881600512, 536870912), (1261007895664787456, 536870912), (1765411053930283008, 536870912), (5800636320054247424, 536870912), (10376293541461622816, 68719476737), (10412322338481635328, 536870912), (1152921504606851072, 553648130),
    (1152921504606851072, 603979778), (1152921504741064705, 68719476738), (1152921504741068800, 68719476738), (1188950301626859520, 537001984), (1188950301626859520, 805306368), (1188950301626867712, 536870912), (1188950302700601344, 536870912), (1188950305921826816, 536870912), (1188959097719881728, 536870912), (1189020670371037184, 536870912), (1193453901254230016, 536870912), (10376293545756590112, 68719476736),
]


def die(msg: str) -> None:
    print(f"FINDINGS FAIL-CLOSED ABORT: {msg}", file=sys.stderr)
    sys.exit(1)


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def parse_replay_rows(paths):
    out = []
    for p in paths:
        with p.open() as f:
            for line in f:
                if not line.startswith("replay,"):
                    continue
                parts = line.strip().split(",")
                out.append({
                    "file": p.name, "stones": int(parts[2]), "legal": int(parts[3]),
                    "budget": int(parts[5]), "result": int(parts[6]),
                    "nodes": int(parts[7]), "wall_s": float(parts[8]),
                    "key": (int(parts[9]), int(parts[10])),
                })
    return out


def main():
    if digest(GEOMETRY) != PIN["geometry_json_gz"]:
        die("geometry pin")
    if digest(QUARANTINE) != PIN["quarantine_registry"]:
        die("quarantine pin")
    if digest(CHAIN_CACHE) != PIN["probe13_cache"]:
        die("chain pin")
    audit = json.loads(UNION_AUDIT.read_text())
    if audit["global_conflict_count"] != 0:
        die("upstream union audit reports conflicts; findings refuse to run on inconsistent corpus")

    hist = {}
    for row in json.loads(HISTORY.read_text(encoding="utf-8")):
        if row["stones"] == 5:
            hist[tuple(row["key"])] = row
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))["profile"]

    sys.path.insert(0, str(ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts"))
    from n11_integer_circle_geometry import legal_points  # noqa: E402

    def points(k):
        return tuple(i for i in range(121) if ((k[0] if i < 64 else k[1]) >> (i % 64)) & 1)

    def legal_of(k):
        h = hist.get(k)
        obs = h.get("observations", []) if h else []
        if obs:
            return obs[0]["legal"]
        return len(legal_points(points(k)))

    def proxy_of(k):
        b = str(legal_of(k) // 10 * 10)
        h = profile.get(b)
        return h["mean_truncated_nodes"] if h else 15000000

    # --- A. proxy calibration over published probe raws
    calib = []
    for d in PROBE_DIRS:
        rd = d / "output/raw"
        rows = parse_replay_rows(sorted(rd.glob("at*.out.csv")))
        # validation gate rows excluded: only at2m/at15m target rows
        for r in rows:
            if r["stones"] != 5:
                die("non-5-stone row in probe raw")
            calib.append({
                "key": f"{r['key'][0]}:{r['key'][1]}", "stage_budget": r["budget"],
                "result": r["result"], "nodes": r["nodes"], "wall_s": r["wall_s"],
                "legal": r["legal"], "proxy": round(proxy_of(r["key"]), 1),
                "nodes_over_proxy": round(r["nodes"] / proxy_of(r["key"]), 4),
                "probe_dir": d.name,
            })
    rows2 = parse_replay_rows(sorted(TWO_TARGET_RAW.glob("*.out.csv")))
    for r in rows2:
        calib.append({
            "key": f"{r['key'][0]}:{r['key'][1]}", "stage_budget": r["budget"],
            "result": r["result"], "nodes": r["nodes"], "wall_s": r["wall_s"],
            "legal": r["legal"], "proxy": round(proxy_of(r["key"]), 1),
            "nodes_over_proxy": round(r["nodes"] / proxy_of(r["key"]), 4),
            "probe_dir": "n11-two-target-design-20261010 (published C++ raws)",
        })
    calib.sort(key=lambda c: (c["probe_dir"], c["key"], c["stage_budget"]))
    resolved15 = [c for c in calib if c["stage_budget"] == 15000000 and c["result"] in (1, 2)]
    two_m_unknown = [c for c in calib if c["stage_budget"] == 2000000 and c["result"] == 0]

    # --- B. backlog reconciliation
    geo = json.loads(gzip.open(GEOMETRY, "rt", encoding="utf-8").read())
    chain = {}
    with CHAIN_CACHE.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            if not row or row[0].startswith("#"):
                continue
            if row[0] != "s5verdict":
                die("chain row")
            chain[(int(row[1]), int(row[2]))] = int(row[4])
    quarantine = quarantined_cache_keys()

    def stage(vals):
        if 1 in vals: return "WIN"
        if all(v == 2 for v in vals): return "LOSS"
        return "UNKNOWN"

    classes = []
    for row in geo:
        k = tuple(row["key"])
        ch = {tuple(z) for z in row["children"]}
        classes.append((k, row["coverage"], ch))
    required = {100, 108}
    candidates = [(k, cov, ch) for k, cov, ch in classes if required & set(cov)]

    # active classes at the pinned chain
    active = []
    for k, cov, ch in candidates:
        v = [chain.get(z, 0) for z in ch]
        if stage(v) == "UNKNOWN":
            active.append((k, cov, ch))
    active_keys = {k for k, _, _ in active}
    active_incidence = collections.defaultdict(list)
    for k, cov, ch in active:
        for z in ch:
            if z not in chain:
                active_incidence[z].append(k)

    backlog = [(r["key"][0], r["key"][1]) for r in audit["backward_only_exact_or_merged_rows"]]
    backvals = {(r["key"][0], r["key"][1]): r["verdict_values"] for r in audit["backward_only_exact_or_merged_rows"]}
    in_supply = [k for k in backlog if k in active_incidence]

    per_class = collections.Counter()
    per_class_win = collections.defaultdict(list)
    for k in in_supply:
        v = backvals[k]
        for parent in active_incidence[k]:
            per_class[parent] += 1
            if 1 in v:
                per_class_win[parent].append(k)

    focus35 = set(FOCUS_DECLARED_35)
    overlap_focus = [k for k in in_supply if k in focus35]
    reply27_targets = set()
    for d in PROBE_DIRS:
        for p in (d / "output/raw").glob("at15m-s5-*.out.csv"):
            pass
        for p in (d / "output/raw").glob("at15m-s5-*.out.csv"):
            rows = parse_replay_rows([p])
            for r in rows:
                reply27_targets.add(r["key"])
    overlap_reply27 = [k for k in in_supply if k in reply27_targets]

    # if-adopted recompute (measurement only: what the class statuses would be)
    adopted = dict(chain)
    for k in in_supply:
        v = backvals[k]
        if v == [2]:
            adopted[k] = 2
        elif v == [1]:
            adopted[k] = 1
    statuses_ad = collections.Counter()
    eliminated_ad = []
    for k, cov, ch in candidates:
        v = [adopted.get(z, 0) for z in ch]
        st = stage(v)
        statuses_ad[st] += 1
        if st == "WIN":
            # count classes that moved UNKNOWN -> WIN under adoption
            v0 = [chain.get(z, 0) for z in ch]
            if v0.count(1) == 0:
                eliminated_ad.append(f"{k[0]}:{k[1]}")
    # supply after adoption
    active_incidence_ad = collections.defaultdict(list)
    for k, cov, ch in candidates:
        v = [adopted.get(z, 0) for z in ch]
        if stage(v) != "UNKNOWN":
            continue
        for z in ch:
            if z not in adopted:
                active_incidence_ad[z].append(k)
    deg_ad = collections.Counter(len(v) for v in active_incidence_ad.values())
    deg_now = collections.Counter(len(v) for v in active_incidence.values())

    closure_delta = []
    for k, cov, ch in active:
        kids_unknown_now = [z for z in ch if z not in chain]
        kids_unknown_ad = [z for z in ch if z not in adopted]
        closure_delta.append({
            "class": f"{k[0]}:{k[1]}",
            "unknown_now": len(kids_unknown_now),
            "unknown_if_backlog_adopted": len(kids_unknown_ad),
            "delta": len(kids_unknown_now) - len(kids_unknown_ad),
        })
    closure_delta.sort(key=lambda r: (r["unknown_if_backlog_adopted"], r["class"]))
    eliminated_by_win = sorted(per_class_win.keys())
    backlog_proxy_sum = sum(proxy_of(k) for k in in_supply)

    result = {
        "schema": "n11-s5-findings-reconciliation-20261121-v1",
        "pins": {"chain_cache_sha256": PIN["probe13_cache"],
                 "union_audit": str(UNION_AUDIT.relative_to(ROOT)),
                 "union_audit_sha256": digest(UNION_AUDIT)},
        "proxy_calibration": {
            "resolved_15m_rows": len(resolved15),
            "unknown_2m_rows": len(two_m_unknown),
            "rows": calib,
            "note": "proxy = frozen legal-decile mean truncated nodes; ratio is an observation on 20 resolution runs, not a calibrated estimator; selection bias is documented upstream.",
        },
        "backlog_reconciliation": {
            "backward_only_total": len(backlog),
            "backward_only_in_active_supply": len(in_supply),
            "overlap_with_focus_lane_35": [[k[0], k[1]] for k in overlap_focus],
            "overlap_with_reply27_published_targets": [[k[0], k[1]] for k in overlap_reply27],
            "per_live_class_decrements_if_adopted": [
                {"class": f"{k[0]}:{k[1]}", "decrement": v,
                 "win_rows_would_eliminate": [[x[0], x[1]] for x in per_class_win.get(k, [])]}
                for k, v in sorted(per_class.items(), key=lambda kv: (-kv[1], kv[0]))[:25]
            ],
            "live_classes_touched": len(per_class),
            "historical_win_row_keys": [[k[0], k[1]] for k in in_supply if 1 in backvals[k]],
            "would_eliminate_classes_unknown_to_win": eliminated_by_win and sorted(f"{k[0]}:{k[1]}" for k in eliminated_by_win) or [],
            "if_adopted_candidate_status_counts": dict(statuses_ad),
            "if_adopted_new_win_classes": eliminated_ad,
            "degree_distribution_now": dict(deg_now),
            "degree_distribution_if_adopted": dict(deg_ad),
            "backlog_completion_proxy_sum_nodes_est": round(backlog_proxy_sum),
            "guard": "Adoption is NOT claimed or performed by this measurement. Historical rows carry their own trust labels (K0374/K0379 raw reconstructions for the S6-split WIN; reply27-20more / ten-loss / s4-boundary-direct batches for the LOSS rows). Reconciliation belongs to the evidence owners; nothing here changes any verdict, cache, or class status.",
        },
        "closure_delta_table": closure_delta,
        "status_guard": "Standard 11x11 empty board, the two-stone root {60,27}, and third moves 100/108 remain UNKNOWN. Node counts and proxies are never verdicts.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
