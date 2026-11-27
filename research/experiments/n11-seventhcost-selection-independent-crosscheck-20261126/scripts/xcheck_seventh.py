#!/usr/bin/env python3
"""Independent cross-check of the seventh-cost exclusive selection (fresh logic,
selector source NOT consulted beyond its published output). Recomputes from the
published head cache + geometry + supply + priority table: live classes under
head, rank-7 unclaimed class, unknown/exclusive/shared children, proxy order,
bands, proxy sum; compares to the published selection JSON."""
import csv, gzip, json
from collections import defaultdict
from pathlib import Path

R = Path(__file__).resolve().parent
HEAD = R / "research/experiments/n11-centralreply-sixthlossk38-adoption-reaudit-20261126/output/merged-exact-s5-chain-plus-sixthlossk38-20261126.cache"
GEO = R / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
SUP = R / "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/post-probe/shared-s5-tasks.csv"
CCP = R / "research/experiments/n11-s5-class-closure-priority-20261121/output/class-closure-priority.csv"
PUB = R / "published-keys.json"

head = {}
for row in csv.reader(HEAD.open(encoding="utf-8-sig", newline="")):
    if not row or row[0].startswith("#"):
        continue
    assert row[0] == "s5verdict" and int(row[3]) == 5
    head[(int(row[1]), int(row[2]))] = int(row[4])
assert len(head) == 6832

geo = json.loads(gzip.open(GEO, "rt", encoding="utf-8").read())
assert len(geo) == 3384
live = []
for g in geo:
    ch = {tuple(z) for z in g["children"]}
    if not ({100, 108} & set(g["coverage"])):
        continue
    vals = [head.get(z, 0) for z in ch]
    if 1 in vals:
        continue
    if all(v == 2 for v in vals):
        continue
    live.append((tuple(g["key"]), g["coverage"], ch))

live_par = defaultdict(set)
for k, cov, ch in live:
    for c in ch:
        if c not in head:
            live_par[c].add(k)

supply = {}
for row in csv.DictReader(SUP.open(newline="")):
    lo, hi = row["key"].split(":")
    supply[(int(lo), int(hi))] = row

pub = list(csv.DictReader(CCP.open(newline="")))
ranked = sorted(pub, key=lambda r: (int(r["proxy_total"]), r["key"]))
claimed = {"1188950301626859520:536870912", "1297036692683752448:0",
           "1297036830122704896:0", "1297107061427929088:0",
           "1152921504612089856:536870912", "10376293541461626880:65536"}
# next unclaimed live class with exclusive unknown children
sel = None
for r in ranked:
    if r["key"] in claimed:
        continue
    cand = next((c for c in live if f"{c[0][0]}:{c[0][1]}" == r["key"]), None)
    if cand is None:
        continue
    unk = sorted(c for c in cand[2] if c not in head)
    excl = [c for c in unk if live_par[c] == {cand[0]}]
    if excl:
        sel = (r, cand, unk, excl)
        break
r, cand, unk, excl = sel
def proxy(c): return int(supply[c]["truncated_cost_proxy_nodes"])
order = sorted(excl, key=lambda c: (proxy(c), c))

pubj = json.loads(PUB.read_text())
mine = [f"{c[0]}:{c[1]}" for c in order]
pubkeys = [e["key"] for e in pubj["exclusive_probe_order"]]
checks = {
  "rank_index_in_ranked": ranked.index(r),
  "class_match": pubj["class"] == f"{cand[0][0]}:{cand[0][1]}",
  "coverage_match": pubj["coverage"] == sorted(cand[1]),
  "children_total_match": pubj["class_children_total"] == len(cand[2]),
  "unknown_head_match": pubj["s5_unknown_before_head"] == len(unk),
  "exclusive_match": pubj["unknown_exclusive_head"] == len(excl) == len(pubkeys),
  "shared_match": pubj["unknown_shared_head"] == len(unk) - len(excl),
  "proxy_sum_match": pubj["proxy_exclusive_sum_head"] == sum(proxy(c) for c in excl),
  "order_match": mine == pubkeys,
  "proxy_values_match": all(pubj["exclusive_probe_order"][i]["proxy"] == proxy(order[i]) for i in range(len(order))),
  "legal_values_match": all(pubj["exclusive_probe_order"][i]["legal"] == int(supply[order[i]]["legal"]) for i in range(len(order))),
  "head_absent": not (set(mine) & {f"{k[0]}:{k[1]}" for k in head}),
  "live_classes_count": len(live),
}
bands = defaultdict(int)
for c in order: bands[proxy(c)] += 1
checks["bands_match"] = {str(k): v for k, v in sorted(bands.items())} == pubj["bands_proxy_to_count"]
print(json.dumps(checks, indent=1))
bad = [k for k, v in checks.items() if v is False]
print("ALL-CHECKS-PASS" if not bad else f"FAILED: {bad}")
