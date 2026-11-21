#!/usr/bin/env python3
"""n11 S5 frontier closure census at a pinned merged cache (2026-11-21).

Secondary measurement over published first-order artifacts only:
  - the frozen 3,384-class geometry (independently audited, K0372),
  - one pinned byte-checked merged exact S5 cache,
  - the active S5 evidence quarantine registry,
  - the frozen historical cost profile used by the scheduler proxy.

It NEVER establishes a game verdict. It never writes a cache row.
Fail-closed: any pinned-input mismatch aborts with nonzero exit.

Outputs (JSON):
  chain-verify   : byte-chain verification of the published reply27 JS-replica
                   merged-cache increments (probe-1 .. probe-13, as pinned).
  class-census   : per-live-candidate-class closure distance at this cache:
                   unknown children, exclusive vs shared split, quarantined
                   blockers, completion proxy.
  supply-census  : active-unknown S5 keys by live-parent band, with the
                   unclaimed single-live-parent band (parent != focus class)
                   quantified and its cheapest keys listed.
  focus-xcheck   : machine cross-check of the focus-class exclusive band (35
                   keys declared by the 2026-11-21 13:38Z lane) plus its
                   two published proxy bands.
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
CHAIN = [
    ("probe-1", ROOT / "research/experiments/n11-reply27-s5-jsreplica-probe-1306114260682670080-20261121/output/merged-exact-s5-after-js-probe-1.cache"),
    ("probe-2", ROOT / "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461622788-20261121/output/merged-exact-s5-after-js-probe-2.cache"),
    ("probe-3", ROOT / "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461622788-77309411328-20261121/output/merged-exact-s5-after-js-probe-3.cache"),
    ("probe-4", ROOT / "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-12288-20261121/output/merged-exact-s5-after-js-probe-4.cache"),
    ("probe-5", ROOT / "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-134217744-20261121/output/merged-exact-s5-after-js-probe-5.cache"),
    ("probe-6", ROOT / "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-134225920-20261121/output/merged-exact-s5-after-js-probe-6.cache"),
    ("probe-7", ROOT / "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-150994944-20261121/output/merged-exact-s5-after-js-probe-7.cache"),
    ("probe-8", ROOT / "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-16777232-20261121/output/merged-exact-s5-after-js-probe-8.cache"),
    ("probe-9", ROOT / "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-16785408-20261121/output/merged-exact-s5-after-js-probe-9.cache"),
    ("probe-10", ROOT / "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-18874368-20261121/output/merged-exact-s5-after-js-probe-10.cache"),
    ("probe-11", ROOT / "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-25165824-20261121/output/merged-exact-s5-after-js-probe-11.cache"),
    ("probe-12", ROOT / "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-34359742464-20261121/output/merged-exact-s5-after-js-probe-12.cache"),
    ("probe-13", ROOT / "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/merged-exact-s5-after-js-probe-13.cache"),
]
PIN = {
    "geometry_json_gz": "146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54",
    "quarantine_registry": "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9",
    "probe13_cache": "60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6",
    "probe12_cache": "0e4016aea0feea2c1eaa6dbc8ba56af1e54c1d02d8cba5338ecd8ddd0804f3a8",
}
FOCUS_CLASS = (1188950301626859520, 536870912)
FOCUS_DECLARED_35 = [
    (1152921504606851072, 536870922), (1152921504606851072, 536870978), (1152921504606851072, 536936450), (1152921504606851072, 537001986), (1152921504606851072, 570425346), (1188950301626859520, 536870913), (1188950301626859520, 536870976), (1188950301626859520, 537133056), (1188950301626859520, 603979776), (1188950301626863616, 536870912), (1188950301626892288, 536870912), (1188950301643636736, 536870912), (1188950310216794112, 536870912), (1188950576504766464, 536870912), (1188951401138487296, 536870912), (1189091039115214848, 536870912), (1197957500881600512, 536870912), (1261007895664787456, 536870912), (1765411053930283008, 536870912), (5800636320054247424, 536870912), (10376293541461622816, 68719476737), (10412322338481635328, 536870912), (1152921504606851072, 553648130),
    (1152921504606851072, 603979778), (1152921504741064705, 68719476738), (1152921504741068800, 68719476738), (1188950301626859520, 537001984), (1188950301626859520, 805306368), (1188950301626867712, 536870912), (1188950302700601344, 536870912), (1188950305921826816, 536870912), (1188959097719881728, 536870912), (1189020670371037184, 536870912), (1193453901254230016, 536870912), (10376293545756590112, 68719476736),
]


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def die(msg: str) -> None:
    print(f"CENSUS FAIL-CLOSED ABORT: {msg}", file=sys.stderr)
    sys.exit(1)


def read_cache(path: Path, quarantine: set):
    values = {}
    n = 0
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            if not row or row[0].startswith("#"):
                continue
            if row[0] != "s5verdict":
                die(f"unexpected cache row in {path.name}: {row[:2]}")
            if len(row) != 6:
                die(f"bad row arity in {path.name}")
            k, v = (int(row[1]), int(row[2])), int(row[4])
            if int(row[3]) != 5 or v not in (1, 2):
                die(f"bad cache row in {path.name}: {row}")
            n += 1
            first = values.setdefault(k, v)
            if first != v:
                die(f"internal verdict conflict in {path.name}: {k}")
            if k in quarantine:
                die(f"quarantined key present in {path.name}: {k}")
    return values, n


def chain_verify(quarantine: set):
    out = []
    prev_rows = None
    for tag, path in CHAIN:
        if not path.exists():
            die(f"chain file missing: {path}")
        rows, n = read_cache(path, quarantine)
        sha = digest(path)
        if prev_rows is None:
            inserted = []
            rowset = rows
        else:
            new_keys = set(rows) - set(prev_rows)
            removed = set(prev_rows) - set(rows)
            if removed:
                die(f"chain {tag}: rows removed from previous cache: {sorted(removed)[:3]}")
            inserted = sorted(new_keys)
            # byte sortedness: verify file order is sorted by (lo, hi)
        oksort = True
        last = None
        with path.open() as f:
            for row in csv.reader(f):
                if not row or row[0].startswith("#"):
                    continue
                k = (int(row[1]), int(row[2]))
                if last is not None and k <= last:
                    oksort = False
                last = k
        if prev_rows is not None:
            for k, v in prev_rows.items():
                if rows.get(k) != v:
                    die(f"chain {tag}: verdict changed or dropped for {k}")
        verdicts = collections.Counter("WIN" if v == 1 else "LOSS" for v in rows.values())
        out.append({
            "stage": tag, "path": str(path.relative_to(ROOT)), "rows": n,
            "sha256": sha, "win": verdicts["WIN"], "loss": verdicts["LOSS"],
            "rows_inserted_vs_prev": len(inserted) if prev_rows is not None else None,
            "inserted_keys": [[k[0], k[1]] for k in inserted] if prev_rows is not None else None,
            "strictly_sorted": oksort,
        })
        prev_rows = rows
    last = out[-1]
    if last["sha256"] != PIN["probe13_cache"]:
        die("probe-13 cache sha256 pin mismatch")
    if out[-2]["sha256"] != PIN["probe12_cache"]:
        die("probe-12 cache sha256 pin mismatch")
    return out


def main():
    for name, p in (("geometry", GEOMETRY), ("quarantine", QUARANTINE), ("history", HISTORY), ("profile", PROFILE)):
        if not p.exists():
            die(f"missing pinned input: {p}")
    if digest(GEOMETRY) != PIN["geometry_json_gz"]:
        die("geometry sha256 mismatch")
    if digest(QUARANTINE) != PIN["quarantine_registry"]:
        die("quarantine registry sha256 mismatch")

    quarantine = {k for k in quarantined_cache_keys() if True}
    just_quarantine = quarantined_cache_keys()

    chain = chain_verify(just_quarantine)

    cache_path = CHAIN[-1][1]
    cache, rows_n = read_cache(cache_path, just_quarantine)

    geo = json.loads(gzip.open(GEOMETRY, "rt", encoding="utf-8").read())
    if len(geo) != 3384:
        die(f"geometry class count {len(geo)}")
    hist = {}
    for row in json.loads(HISTORY.read_text(encoding="utf-8")):
        if row["stones"] == 5:
            hist[tuple(row["key"])] = row
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))["profile"]

    def stage(vals):
        if 1 in vals:
            return "WIN"
        if all(v == 2 for v in vals):
            return "LOSS"
        return "UNKNOWN"

    def legal_count(k):
        pts = (k[0], k[1])
        legal = 0
        lo, hi = pts
        for i in range(121):
            if ((lo if i < 64 else hi) >> (i % 64)) & 1:
                continue
            legal += 1
        return legal

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

    classes = []
    for row in geo:
        k = tuple(row["key"])
        ch = {tuple(z) for z in row["children"]}
        v = [cache.get(z, 0) for z in ch]
        classes.append({
            "key": k, "coverage": row["coverage"], "children": ch,
            "status": stage(v), "win": v.count(1), "loss": v.count(2), "unknown": v.count(0),
        })
    byclass = {c["key"]: c for c in classes}
    required = {100, 108}
    candidates = [c for c in classes if required.intersection(c["coverage"])]
    if not all(required.issubset(c["coverage"]) for c in candidates):
        die("candidate class covering only one of {100,108}")
    cstat = collections.Counter(c["status"] for c in candidates)
    active = [c for c in candidates if c["status"] == "UNKNOWN"]
    if any(c["status"] == "LOSS" for c in candidates):
        die("a candidate class is already LOSS: census stale, root state moved")

    active_incidence = collections.defaultdict(list)
    for c in active:
        for ch in c["children"]:
            if ch not in cache:
                active_incidence[ch].append(c["key"])

    # closure-distance table
    closure = []
    for c in active:
        u = sorted(k for k in c["children"] if k not in cache)
        deg = {k: len(active_incidence[k]) for k in u}
        qblocked = [k for k in u if k in just_quarantine]
        closure.append({
            "class": f"{c['key'][0]}:{c['key'][1]}",
            "coverage": c["coverage"],
            "unknown": len(u),
            "unknown_exclusive": sum(deg[k] == 1 for k in u),
            "unknown_shared": sum(deg[k] >= 2 for k in u),
            "unknown_quarantine_blocked": len(qblocked),
            "quarantine_blocked_keys": [[k[0], k[1]] for k in qblocked],
            "children_total": len(c["children"]),
            "win_children": c["win"], "loss_children": c["loss"],
            "completion_15m_truncated_nodes_proxy": round(sum(proxy_of(k) for k in u)),
            "min_child_proxy": min((proxy_of(k) for k in u), default=None),
        })
    closure.sort(key=lambda r: (r["unknown"], r["class"]))

    # supply bands
    bands = collections.Counter(len(active_incidence[k]) for k in active_incidence)
    supply = []
    for k, parents in active_incidence.items():
        supply.append({
            "key": f"{k[0]}:{k[1]}", "legal": legal_of(k),
            "live_parents": sorted(f"{p[0]}:{p[1]}" for p in parents),
            "proxy": proxy_of(k), "quarantined": k in just_quarantine,
        })
    focus_band = [s for s in supply if s["live_parents"] == [f"{FOCUS_CLASS[0]}:{FOCUS_CLASS[1]}"] and not s["quarantined"]]
    unclaimed = [s for s in supply if len(s["live_parents"]) == 1 and s["live_parents"][0] != f"{FOCUS_CLASS[0]}:{FOCUS_CLASS[1]}" and not s["quarantined"]]
    unclaimed_quarantined = [s for s in supply if s["quarantined"]]
    two_plus = [s for s in supply if len(s["live_parents"]) >= 2 and not s["quarantined"]]
    unclaimed.sort(key=lambda s: (s["proxy"], s["key"]))
    two_plus.sort(key=lambda s: (s["proxy"], s["key"]))
    focus_sorted = sorted([s for s in supply if s["live_parents"] == [f"{FOCUS_CLASS[0]}:{FOCUS_CLASS[1]}"]], key=lambda s: (s["proxy"], s["key"]))

    got = {(int(s["key"].split(":")[0]), int(s["key"].split(":")[1])) for s in focus_band}
    want = set(FOCUS_DECLARED_35)
    xcheck = {
        "declared_35_found": len(want & got),
        "declared_35_missing": sorted([[k[0], k[1]] for k in want - got]),
        "extra_focus_band_keys": sorted([[k[0], k[1]] for k in got - want]),
        "focus_band_proxy_multiset": sorted(s["proxy"] for s in focus_band),
        "focus_band_unknown_children_of_focus_class": byclass[FOCUS_CLASS]["unknown"],
    }

    quarantined_in_supply = [s for s in supply if s["quarantined"]]

    result = {
        "schema": "n11-s5-frontier-census-20261121-v1",
        "pins": {
            "geometry_sha256": PIN["geometry_json_gz"],
            "quarantine_sha256": PIN["quarantine_registry"],
            "cache": str(cache_path.relative_to(ROOT)),
            "cache_sha256": PIN["probe13_cache"],
            "cache_rows": rows_n,
        },
        "chain_verify": chain,
        "candidate_counts": dict(cstat),
        "active_classes": len(active),
        "active_unknown_s5_unique": len(active_incidence),
        "active_unknown_s5_degree_distribution": dict(bands),
        "class_closure_table": closure,
        "supply": {
            "one_live_parent_focus_exclusive": len(focus_band),
            "one_live_parent_other_classes_claimable_pool": len(unclaimed),
            "two_plus_live_parents_reply27_band": len(two_plus),
            "quarantine_blocked_supply_keys": len(quarantined_in_supply),
            "quarantine_blocked_supply": quarantined_in_supply,
            "unclaimed_band_cheapest_20": [
                {"key": s["key"], "parent": s["live_parents"][0], "proxy": s["proxy"], "legal": s["legal"]}
                for s in unclaimed[:20]
            ],
            "two_plus_band_cheapest_20": [
                {"key": s["key"], "parents": s["live_parents"], "proxy": s["proxy"], "legal": s["legal"]}
                for s in two_plus[:20]
            ],
        },
        "focus_lane_xcheck": xcheck,
        "interpretation_guard": "Closure distance, proxies and node counts are scheduling measurements, never verdicts. Standard 11x11 empty board and the two-stone root {60,27} remain UNKNOWN.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
