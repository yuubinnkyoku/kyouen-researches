#!/usr/bin/env python3
"""n11 reply27 S5 class-closure priority: certificate-oriented scheduling metrics.

Reads the frozen 3,384-class geometry (independently audited upstream), the
reply27 JS-replica merged exact S5 cache at probe-13, and the probe-13
post-probe supply table, and computes, per live candidate class:

  - closure distance (remaining UNKNOWN S5 children), split into
    exclusive (single live parent class) and shared children,
  - the frozen-profile truncated-cost proxy sums of those children,
  - a bin-implied remaining-WIN index (reference only, biased evidence,
    NOT a probability and NOT calibrated),
  - the class's first-completion position under a global
    cheapest-first supply order (static all-LOSS scenario), and
  - the coordinator comparison: global cheapest-first vs class-targeted
    completion, in probes and in cumulative truncated proxy nodes.

None of these numbers establish any game verdict. Output rankings are
scheduling measurements only. 11x11 root questions remain UNKNOWN.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

GEOMETRY_SHA = "146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54"
# reply27 JS-replica probe-13 merged exact S5 cache (main a423c2f0):
CACHE_SHA = "60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6"
# probe-13 post-probe supply table (published in full with the probe-13 README):
SUPPLY_SHA = "31f0d29b820a69508af0c352c22f09b244bff5b9ae79476679047cdb160ea954"
# probe-13 post-probe candidate ledger (published):
CANDIDATE_LEDGER_SHA = "2a4c2382d812102f8132339c871b07ee998e933c80da876759e51e84f64fda80"
# frozen historical legal-decile truncated-cost profile (analyze.py input):
PROFILE_SHA = "6b2971e53059ac36af7bf161a61d90d65f85e604e27b93d013e7a2853fdceddc"

FOCUS_CLASS = "1188950301626859520:536870912"
CERT_CLASS = "1297036692683752448:0"

# focus-class lane single-owner declaration (research/log/2026-11-21-
# n11-focusclass-s5-exclusive1parent-js-replica-single-owner.md, commit
# aa33434c) enumerated 35 exclusive keys; machine gate equality is asserted.
FOCUS_LANE_35 = [
    "10376293541461622816:68719476737", "10376293545756590112:68719476736",
    "10412322338481635328:536870912", "1152921504606851072:536870922",
    "1152921504606851072:536870978", "1152921504606851072:536936450",
    "1152921504606851072:537001986", "1152921504606851072:553648130",
    "1152921504606851072:570425346", "1152921504606851072:603979778",
    "1152921504741064705:68719476738", "1152921504741068800:68719476738",
    "1188950301626859520:536870913", "1188950301626859520:536870976",
    "1188950301626859520:537001984", "1188950301626859520:537133056",
    "1188950301626859520:603979776", "1188950301626859520:805306368",
    "1188950301626863616:536870912", "1188950301626867712:536870912",
    "1188950301626892288:536870912", "1188950301643636736:536870912",
    "1188950302700601344:536870912", "1188950305921826816:536870912",
    "1188950310216794112:536870912", "1188950576504766464:536870912",
    "1188951401138487296:536870912", "1188959097719881728:536870912",
    "1189020670371037184:536870912", "1189091039115214848:536870912",
    "1193453901254230016:536870912", "1197957500881600512:536870912",
    "1261007895664787456:536870912", "1765411053930283008:536870912",
    "5800636320054247424:536870912",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(msg: str):
    print(f"GATE FAILED: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--geometry", required=True)
    ap.add_argument("--cache", required=True)
    ap.add_argument("--supply", required=True)
    ap.add_argument("--candidate-ledger", required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out_dir = Path(a.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # ---- pins (fail closed) -------------------------------------------------
    if digest(Path(a.geometry)) != GEOMETRY_SHA:
        fail("geometry sha mismatch")
    if digest(Path(a.cache)) != CACHE_SHA:
        fail("cache sha mismatch")
    if digest(Path(a.supply)) != SUPPLY_SHA:
        fail("supply sha mismatch")
    if digest(Path(a.candidate_ledger)) != CANDIDATE_LEDGER_SHA:
        fail("candidate ledger sha mismatch")
    if digest(Path(a.profile)) != PROFILE_SHA:
        fail("profile sha mismatch")

    # ---- inputs --------------------------------------------------------------
    geo = json.loads(gzip.open(a.geometry, "rt", encoding="utf-8").read())
    if len(geo) != 3384:
        fail("geometry class count")
    cache = {}
    for row in csv.reader(Path(a.cache).open(encoding="utf-8-sig", newline="")):
        if not row or row[0].startswith("#"):
            continue
        if row[0] != "s5verdict" or int(row[3]) != 5 or int(row[4]) not in (1, 2):
            fail(f"unexpected cache row {row}")
        k = (int(row[1]), int(row[2]))
        v = int(row[4])
        if k in cache and cache[k] != v:
            fail(f"verdict conflict in cache {k}")
        cache[k] = v

    def stage(vals):
        if 1 in vals:
            return "WIN"
        if all(v == 2 for v in vals):
            return "LOSS"
        return "UNKNOWN"

    required = {100, 108}
    secured = set()
    candidates = []
    counts = defaultdict(int)
    for g in geo:
        ch = {tuple(z) for z in g["children"]}
        vals = [cache.get(z, 0) for z in ch]
        st = stage(vals)
        counts[st] += 1
        if st == "LOSS":
            secured.update(g["coverage"])
        if required.intersection(g["coverage"]):
            candidates.append((tuple(g["key"]), g["coverage"], ch, st))
    third_moves = {v for _, cov, _, _ in candidates for v in cov}
    if len(third_moves) != 119 or third_moves - secured != required:
        fail("third-move/coverage invariants")
    if not all(required.issubset(cov) for _, cov, _, _ in candidates):
        fail("candidate coverage split invariant")
    if len(candidates) != 115:
        fail("candidate count")
    active = [c for c in candidates if c[3] == "UNKNOWN"]
    if len(active) != 62 or counts["WIN"] != 272 or counts["LOSS"] != 31:
        fail("ledger invariants")
    if sum(1 for c in candidates if c[3] == "WIN") != 53:
        fail("candidate WIN count")

    # live incidence over active classes only
    live_par = defaultdict(set)
    for k, cov, ch, st in active:
        for child in ch:
            if child not in cache:
                live_par[child].add(k)
    supply = {}
    for row in csv.DictReader(Path(a.supply).open(newline="")):
        supply[(int(row["key"].split(":")[0]), int(row["key"].split(":")[1]))] = row
    profile = json.loads(Path(a.profile).read_text(encoding="utf-8"))["profile"]
    def bin_mean(legal):
        h = profile.get(str(int(legal) // 10 * 10))
        return h["mean_truncated_nodes"] if h else 15_000_000
    fproxy = {c: bin_mean(int(supply[c]["legal"])) for c in supply}
    if set(supply) != set(live_par) or len(supply) != 4562:
        fail("supply/live-incidence mismatch")
    deg = defaultdict(int)
    for child in live_par:
        deg[len(live_par[child])] += 1
    if deg != {1: 2688, 2: 1874}:
        fail(f"supply degree distribution {dict(deg)}")

    dpool = {c: len(live_par[c]) for c in live_par}
    if sum(1 for c in dpool if dpool[c] == 1) - 35 != 2653:
        fail("claimable pool count")

    # LEDGER cross-check against the published candidate ledger
    ledger = {r["key"]: r for r in csv.DictReader(Path(a.candidate_ledger).open(newline=""))}
    if len(ledger) != 115:
        fail("candidate ledger size")

    # ---- per-class metrics ---------------------------------------------------
    rows = []
    for k, cov, ch, st in active:
        unk = sorted(c for c in ch if c not in cache)
        ks = f"{k[0]}:{k[1]}"
        ex = [c for c in unk if len(live_par[c]) == 1]
        sh = [c for c in unk if len(live_par[c]) > 1]
        assert len(unk) == len(ex) + len(sh)
        def proxy(c):
            return int(supply[c]["truncated_cost_proxy_nodes"])
        def bin_win_rate(c):
            r = supply[c]
            n = int(r["bin_sample_size"])
            if n <= 0:
                fail(f"zero bin sample for {c}")
            return int(r["bin_win_count"]) / n
        prior = 1.0
        for c in unk:
            prior *= (1.0 - bin_win_rate(c))
        lr = ledger.get(ks)
        if lr is None:
            fail(f"missing ledger row {ks}")
        if int(lr["s5_unknown"]) != len(unk):
            fail(f"ledger unknown mismatch {ks}")
        if int(lr["s5_unknown_shared_with_other_live_classes"]) != len(sh):
            fail(f"ledger shared mismatch {ks}")
        if int(lr["completion_15m_truncated_nodes_proxy"]) != round(sum(fproxy[c] for c in unk)):
            fail(f"ledger proxy mismatch {ks}")
        rows.append({
            "key": ks,
            "coverage": " ".join(str(x) for x in sorted(cov)),
            "s5_children": len(ch),
            "s5_unknown": len(unk),
            "unknown_exclusive": len(ex),
            "unknown_shared": len(sh),
            "proxy_exclusive_sum": sum(proxy(c) for c in ex),
            "proxy_shared_sum": sum(proxy(c) for c in sh),
            "proxy_total": sum(proxy(c) for c in unk),
            "bin_prior_all_loss_index": round(prior, 6),
            "min_child_proxy": min(proxy(c) for c in unk),
            "max_child_proxy": max(proxy(c) for c in unk),
        })

    # ---- global cheapest-first queue (static all-LOSS scenario) ----------------
    order = sorted(supply, key=lambda c: (fproxy[c], c))
    qrank = {c: i + 1 for i, c in enumerate(order)}
    for r in rows:
        child_keys = supply and None  # placeholder, filled below
    # children per class set (again, deterministically)
    class_children = {r["key"]: set() for r in rows}
    for k, cov, ch, st in active:
        ks = f"{k[0]}:{k[1]}"
        class_children[ks] = {c for c in ch if c not in cache}
    for r in rows:
        ch = class_children[r["key"]]
        r["complete_at_queue_rank"] = max(qrank[c] for c in ch)
        r["queue_cum_proxy_to_completion"] = round(sum(fproxy[c] for c in order[: r["complete_at_queue_rank"]]))
    by_rank = sorted(rows, key=lambda r: (r["complete_at_queue_rank"], r["key"]))
    first = by_rank[0]

    # targeted completions
    def targeted(ks):
        for r in rows:
            if r["key"] == ks:
                return r
        fail(f"missing class {ks}")

    focus = targeted(FOCUS_CLASS)
    cert = targeted(CERT_CLASS)
    if focus["s5_unknown"] != 93 or focus["unknown_shared"] != 58 or focus["unknown_exclusive"] != 35:
        fail("focus-class closure split")
    if cert["s5_unknown"] != 99 or cert["unknown_shared"] != 61 or cert["unknown_exclusive"] != 38:
        fail("certificate-class closure split")
    my_focus_excl = sorted(
        f"{c[0]}:{c[1]}" for c in class_children[FOCUS_CLASS] if len(live_par[c]) == 1
    )
    if my_focus_excl != sorted(FOCUS_LANE_35):
        fail("focus-lane 35-key gate")

    # bin prior ranking
    by_prior = sorted(rows, key=lambda r: (-r["bin_prior_all_loss_index"], r["proxy_total"], r["key"]))
    by_cost = sorted(rows, key=lambda r: (r["proxy_total"], r["key"]))

    # certificate class exclusive probe order (ascending proxy, then key)
    cert_excl = sorted(
        (c for c in class_children[CERT_CLASS] if len(live_par[c]) == 1),
        key=lambda c: (int(supply[c]["truncated_cost_proxy_nodes"]), c),
    )
    focus_excl = sorted(
        (c for c in class_children[FOCUS_CLASS] if len(live_par[c]) == 1),
        key=lambda c: (int(supply[c]["truncated_cost_proxy_nodes"]), c),
    )
    overlap = set(f"{c[0]}:{c[1]}" for c in cert_excl) & set(FOCUS_LANE_35)
    if overlap:
        fail(f"certificate-class exclusive keys overlap focus-lane claims {sorted(overlap)}")
    # all certificate-class exclusive keys sit in the census claimable pool
    if not all(len(live_par[c]) == 1 for c in cert_excl) or len(cert_excl) != 38:
        fail("certificate-class exclusive set")

    # ---- outputs ----------------------------------------------------------------
    cols = list(rows[0].keys())
    with (out_dir / "class-closure-priority.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for r in sorted(rows, key=lambda r: (r["proxy_total"], r["key"])):
            w.writerow(r)

    summary = {
        "input_pins": {
            "geometry_sha256": GEOMETRY_SHA,
            "cache_sha256": CACHE_SHA,
            "cache": "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/merged-exact-s5-after-js-probe-13.cache",
            "main_at_snapshot": "a423c2f01c4e23874a2bf668cfa019bc244d188d",
            "supply_sha256": SUPPLY_SHA,
            "candidate_ledger_sha256": CANDIDATE_LEDGER_SHA,
        },
        "gates": "3384 classes; 119 third moves; 115 candidates; 62 UNKNOWN/53 WIN/0 LOSS; secured 117; remaining {100,108}; supply 4562 (deg 1:2688 2:1874); claimable pool 2653; ledger cross-check 62/62; focus-lane 35-key equality; certificate-class 38-key non-overlap",
        "status_guard": "scheduling measurement only; no verdict; {60,27}, third moves 100/108 and the 11x11 empty board remain UNKNOWN",
        "queue_static_all_loss": {
            "scenario": "IF every remaining unknown S5 child of the 62 live classes is decided LOSS; static combinatorial statement, no probability used",
            "order": "global ascending truncated_cost_proxy_nodes then key",
            "supply_size": len(supply),
            "first_class_completion": {
                "class": first["key"],
                "probe_index_queue": first["complete_at_queue_rank"],
                "cumulative_proxy_nodes_to_that_point": first["queue_cum_proxy_to_completion"],
                "s5_unknown": first["s5_unknown"],
            },
            "next_five_classes": [
                {"class": r["key"], "probe_index_queue": r["complete_at_queue_rank"],
                 "cumulative_proxy_to_completion": r["queue_cum_proxy_to_completion"]}
                for r in by_rank[1:6]
            ],
            "class_targeted": {
                "focus_class": {
                    "class": FOCUS_CLASS, "probes": focus["s5_unknown"],
                    "proxy_sum": focus["proxy_total"], "exclusive_keys_claimed_by_focus_lane": 35,
                },
                "certificate_class": {
                    "class": CERT_CLASS, "probes": cert["s5_unknown"],
                    "proxy_sum": cert["proxy_total"],
                    "exclusive_keys": len(cert_excl),
                    "shared_keys": cert["unknown_shared"],
                    "note": "the census/reconciliation lane (commit e4aae3b4) identified 99 backward-only published rows exactly covering this class's unknowns (7+99=106 children); fresh re-solving is an alternative to adoption, decision left to evidence owners",
                },
            },
            "interpretation": "under the static all-LOSS scenario a class-targeted completion of the cheapest class needs 93 probes / 530,074,017 proxy nodes, while the global cheapest-first order first completes a class at queue position 3,927 with cumulative 21,911.9M proxy nodes; the ratio is a scheduling fact of the two orders, not a proof-cost bound (truncated proxies are biased, censored, uncalibrated)",
        },
        "bin_prior_ranking_top5": [
            {"class": r["key"], "index": r["bin_prior_all_loss_index"],
             "s5_unknown": r["s5_unknown"], "proxy_total": r["proxy_total"]}
            for r in by_prior[:5]
        ],
        "cost_ranking_top5": [
            {"class": r["key"], "s5_unknown": r["s5_unknown"], "proxy_total": r["proxy_total"],
             "bin_prior": r["bin_prior_all_loss_index"]}
            for r in by_cost[:5]
        ],
        "certificate_class_exclusive_probe_order": [
            {"order": i + 1, "key": f"{c[0]}:{c[1]}",
             "legal": int(supply[c]["legal"]),
             "truncated_cost_proxy_nodes": int(supply[c]["truncated_cost_proxy_nodes"]),
             "bin_win_count": int(supply[c]["bin_win_count"]),
             "bin_sample_size": int(supply[c]["bin_sample_size"])}
            for i, c in enumerate(cert_excl)
        ],
        "focus_class_exclusive_reference": [
            {"order": i + 1, "key": f"{c[0]}:{c[1]}",
             "truncated_cost_proxy_nodes": int(supply[c]["truncated_cost_proxy_nodes"])}
            for i, c in enumerate(focus_excl)
        ],
    }
    (out_dir / "class-closure-priority.json").write_text(
        json.dumps(summary, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print("ALL GATES PASS")
    print(f"rows={len(rows)} first-under-cheapest-first={first['key']}@{first['complete_at_queue_rank']}")
    print(f"focus: probes={focus['s5_unknown']} proxy={focus['proxy_total']} prior={focus['bin_prior_all_loss_index']}")
    print(f"cert:  probes={cert['s5_unknown']} proxy={cert['proxy_total']} excl={len(cert_excl)}")


if __name__ == "__main__":
    main()
