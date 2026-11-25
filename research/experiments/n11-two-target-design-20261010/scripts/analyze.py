#!/usr/bin/env python3
"""Two remaining reply27 third moves: exact incidence + non-proof scheduling proxies.

Uses the independently audited, frozen 3,384-class geometry and latest tracked
exact S5 cache. The output rankings NEVER establish a game verdict.
"""
from __future__ import annotations

import argparse
import collections
import csv
import gzip
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-two-target-design-20261010"
OLD = ROOT / "research/experiments/n11-strategy-redesign-20261010/output"
CURRENT = ROOT / "research/experiments/n11-reply27-class-1297036692683751424-16-20261010/output"
GEOMETRY = OLD / "geometry.json.gz"
DEFAULT_CACHE = ROOT / "research/experiments/n11-reply27-next-class-1188950301626859520-536870912-20261010/output/current-exact-s5-after-probe-3.cache"
HISTORY = OLD / "history.json"
PROFILE = OLD / "historical-cost-profile.json"

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def keystr(k) -> str:
    return f"{k[0]}:{k[1]}"

def read_cache(path: Path):
    import sys
    sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
    from s5_evidence_policy import quarantined_cache_keys
    quarantine = quarantined_cache_keys()
    values = {}
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            if not row or row[0].startswith("#"):
                continue
            if row[0] != "s5verdict":
                raise ValueError(f"unexpected cache row: {row}")
            assert int(row[3]) == 5 and int(row[4]) in (1, 2)
            k, v = (int(row[1]), int(row[2])), int(row[4])
            if k in quarantine:
                raise ValueError(f"quarantined cache entry: {k}")
            if k in values and values[k] != v:
                raise ValueError(f"verdict conflict: {k}")
            values[k] = v
    return values

def stage(vals):
    if 1 in vals:
        return "WIN"
    if all(v == 2 for v in vals):  # vacuous truth: OR at even S4
        return "LOSS"
    return "UNKNOWN"

def build(cache_path: Path, out_dir: Path):
    geo = json.loads(gzip.open(GEOMETRY, "rt", encoding="utf-8").read())
    cache = read_cache(cache_path)
    old_hist = json.loads(HISTORY.read_text(encoding="utf-8"))
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))["profile"]
    assert len(geo) == 3384
    hist = {}
    for row in old_hist:
        if row["stones"] == 5:
            hist[tuple(row["key"])] = row
    classes, byclass = [], {}
    required_moves = {100, 108}
    secured = set()
    overall = collections.Counter()
    for row in geo:
        k = tuple(row["key"])
        ch = {tuple(z) for z in row["children"]}
        v = [cache.get(z, 0) for z in ch]
        st = stage(v)
        overall[st] += 1
        if st == "LOSS":
            secured.update(row["coverage"])
        a = {
            "key": k, "coverage": row["coverage"], "children": ch,
            "status": st, "s5_win": v.count(1), "s5_loss": v.count(2),
            "s5_unknown": v.count(0),
        }
        classes.append(a)
        byclass[k] = a

    # D4 stabilizer of the fixed ordered root (60,27): vertical reflection
    # fixes each root stone; 100=9*11+1, 108=9*11+9.
    reflect = lambda v: (v // 11) * 11 + 10 - v % 11
    assert reflect(60) == 60 and reflect(27) == 27
    assert reflect(100) == 108 and reflect(108) == 100
    assert (100 in secured) == (108 in secured)
    third_moves = {v for c in classes for v in c["coverage"]}
    assert len(third_moves) == 119
    assert third_moves - secured == required_moves, (third_moves-secured)

    # ALL class boundaries containing either remaining move are equivalent
    # for the target-coverage question. Status from complete S5 boundaries.
    candidates = [c for c in classes if required_moves.intersection(c["coverage"])]
    assert candidates
    assert all(required_moves.issubset(c["coverage"]) for c in candidates)
    active = [c for c in candidates if c["status"] == "UNKNOWN"]
    assert not any(c["status"] == "LOSS" for c in candidates)

    incidence = collections.defaultdict(list)
    active_incidence = collections.defaultdict(list)
    for c in candidates:
        for ch in c["children"]:
            incidence[ch].append(c["key"])
            if c["status"] == "UNKNOWN" and ch not in cache:
                active_incidence[ch].append(c["key"])

    # Source history is a frozen pre-checkpoint replay corpus; labels are
    # observational/truncated. Do NOT interpret a missing row as no past work.
    costs = {}
    for k in active_incidence:
        h = hist.get(k)
        observations = h.get("observations", []) if h else []
        legal_values = [o["legal"] for o in observations]
        if len(set(legal_values)) > 1:
            raise ValueError(f"inconsistent legal count: {k}")
        cost_history = [o["nodes"] for o in observations]
        costs[k] = {
            "history_observations": len(observations),
            "history_nodes_observed_sum": sum(cost_history),
            "history_max_unknown_budget": max((o["budget"] for o in observations if o["verdict"] == 0), default=0),
            "legal": legal_values[0] if legal_values else None
        }

    # The legal-count proxy is not calibrated for remaining S5 children:
    # historical ranks were adaptive and 15M UNKNOWN is right-censored.
    # Compute legal() only for previously unobserved keys.
    import sys
    sys.path.insert(0, str(ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts"))
    from n11_integer_circle_geometry import legal_points
    def points(k):
        return tuple(i for i in range(121) if ((k[0] if i < 64 else k[1]) >> (i % 64)) & 1)
    for k, d in costs.items():
        if d["legal"] is None:
            d["legal"] = len(legal_points(points(k)))
    def profile_for(k):
        bin_key = str(costs[k]["legal"] // 10 * 10)
        h = profile.get(bin_key)
        return (h["mean_truncated_nodes"] if h else 15_000_000,
                h["n"] if h else 0,
                (int(h["verdicts"].get("1",0)), int(h["verdicts"].get("2",0)), int(h["verdicts"].get("0",0))) if h else (0,0,0))

    # Exact all-class incidence is reused in the prospective scheduler.
    rankings = []
    for c in candidates:
        u = sorted(k for k in c["children"] if k not in cache) if c["status"] == "UNKNOWN" else []
        h = [costs[k] for k in u] if c["status"] == "UNKNOWN" else []
        proxy = sum(profile_for(k)[0] for k in u)
        shared_active = sum(len(active_incidence[k]) > 1 for k in u)
        # Existing class-boundary evidence is already absorbed by the cache,
        # while the frozen S5 history can still signal budget-exhausted replays.
        ranks = {
            "key": keystr(c["key"]),
            "coverage": c["coverage"], "status": c["status"],
            "s5_children": len(c["children"]),
            "s5_loss": c["s5_loss"], "s5_win": c["s5_win"],
            "s5_unknown": c["s5_unknown"],
            "s5_unknown_shared_with_other_live_classes": shared_active,
            "s5_unknown_active_incidence_sum": sum(len(active_incidence[k]) for k in u),
            "frozen_history_observations": sum(d["history_observations"] for d in h),
            "frozen_history_nodes_sum": sum(d["history_nodes_observed_sum"] for d in h),
            "frozen_history_15m_unknown_targets": sum(d["history_max_unknown_budget"]>=15_000_000 for d in h),
            "completion_15m_truncated_nodes_proxy": round(proxy),
            "legal_min": min((d["legal"] for d in h), default=None),
            "legal_max": max((d["legal"] for d in h), default=None),
        }
        rankings.append(ranks)
    rankable = [r for r in rankings if r["status"]=="UNKNOWN"]
    by_unknown = sorted(rankable,key=lambda r:(r["s5_unknown"],r["key"]))
    by_proxy = sorted(rankable,key=lambda r:(r["completion_15m_truncated_nodes_proxy"],r["s5_unknown"],r["key"]))
    by_shared = sorted(rankable,key=lambda r:(-r["s5_unknown_shared_with_other_live_classes"],r["completion_15m_truncated_nodes_proxy"],r["key"]))
    def top(rows,n=10):
        return [{**r,"rank":i+1} for i,r in enumerate(rows[:n])]

    # Probe is a conditional investment: whether the node becomes LOSS or
    # WIN matters differently to each candidate. Keep both parent counts.
    tasks = []
    for k, parents in active_incidence.items():
        v,n,w = profile_for(k)
        live = [byclass[c] for c in parents]
        raw = costs[k]
        tasks.append({
            "key":keystr(k), "legal":raw["legal"], "live_parents":len(parents),
            "live_parent_keys":[keystr(c) for c in parents],
            "parent_unknown_min":min(c["s5_unknown"] for c in live),
            "parent_unknown_inverse_sum":round(sum(1/c["s5_unknown"] for c in live),9),
            "if_loss_progress":len(parents),
            "if_win_classes_eliminated":len(parents),
            "history_max_unknown_budget":raw["history_max_unknown_budget"],
            "historical_observations":raw["history_observations"],
            "historical_nodes":raw["history_nodes_observed_sum"],
            "bin_sample_size":n,"bin_win_count":w[0],
            "bin_loss_count":w[1],"bin_unknown_count":w[2],
            "truncated_cost_proxy_nodes":round(v),
        })
    # Do not restart any S5 that has >=2M UNKNOWN history at 2M.
    ready2 = [t for t in tasks if t["history_max_unknown_budget"] < 2_000_000]
    ready2.sort(key=lambda t:(-t["live_parents"],t["truncated_cost_proxy_nodes"],t["parent_unknown_min"],t["legal"],t["key"]))

    # Pairwise sharing is a diagnostic, NOT proof of a successful strategy.
    pair_shared = collections.Counter()
    for k, parents in active_incidence.items():
        for a,b in itertools.combinations(sorted(parents),2):
            pair_shared[(a,b)] += 1
    pairs = [
        {"class_a":keystr(a),"class_b":keystr(b),"shared_unknown_s5":n}
        for (a,b),n in sorted(pair_shared.items(),key=lambda z:(-z[1],z[0]))[:20]
    ]
    cstat = collections.Counter(c["status"] for c in candidates)
    summary = {
        "source": {
            "geometry":str(GEOMETRY.relative_to(ROOT)),"geometry_sha256":digest(GEOMETRY),
            "cache":str(cache_path.relative_to(ROOT)) if cache_path.is_relative_to(ROOT) else str(cache_path),
            "cache_sha256":digest(cache_path),
            "history":str(HISTORY.relative_to(ROOT)),"history_sha256":digest(HISTORY),
            "profile":str(PROFILE.relative_to(ROOT)),"profile_sha256":digest(PROFILE),
        },
        "cache_rows":len(cache),"cache_verdicts":dict(collections.Counter("WIN" if v==1 else "LOSS" for v in cache.values())),
        "s4_counts":dict(overall),"secured":len(secured),"total_legal_third_moves":len(third_moves),
        "remaining":sorted(third_moves-secured),
        "symmetry": {"axis":"vertical reflection (row,column) -> (row,10-column)",
          "fixes_ordered_root":[60,27],"swaps":[100,108],
          "candidate_100_only":0,"candidate_108_only":0,
          "implication":"any LOSS S4 class covering 100 also covers 108; 2-class split provides no distinct coverage"},
        "candidates":len(candidates),"candidate_status":dict(cstat),
        "active":len(active),"unknown_s5_incidence":sum(len(c["children"]-{z for z in c["children"] if z in cache}) for c in active),
        "active_unknown_s5_unique":len(active_incidence),
        "active_unknown_s5_degree_distribution":dict(collections.Counter(map(len,active_incidence.values()))),
        "all_candidate_s5_unique":len(incidence),
        "all_candidate_s5_degree_distribution":dict(collections.Counter(map(len,incidence.values()))),
        "top_unknown":top(by_unknown), "top_completion_proxy":top(by_proxy),
        "top_shared":top(by_shared), "top_pairs":pairs,
        "top_joint_tasks_ready_2m":ready2[:20],
        "ranking_model": {
          "completion":"Sum of frozen historical 15M-truncated legal-decile mean nodes over UNKNOWN S5; not an upper bound or an unbiased estimate.",
          "early_rejection":"ONE exact S5 WIN rejects all containing S4 classes; frozen bin WIN/LOSS/UNKNOWN counts supplied only as biased evidence, NOT a probability.",
          "joint":"Rank new S5 by number of live parent classes, then capped observed cost; useful for exploration only, no guaranteed gain.",
          "selection_bias":"Prior probed children were selected by earlier rankings, censored at budget, and run on different hardware.",
          "no_independent_terminal_proof":"S5 outcomes are solver/cache-trusted; geometry is a separately audited frozen input."
        }
    }
    out_dir.mkdir(parents=True,exist_ok=True)
    cols=list(rankings[0])
    with (out_dir/"candidate-classes.csv").open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=cols);writer.writeheader();writer.writerows(sorted(rankings,key=lambda r:(r["status"]!="UNKNOWN",r["s5_unknown"],r["key"])))
    cols=list(tasks[0])
    with (out_dir/"shared-s5-tasks.csv").open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=cols);writer.writeheader();writer.writerows(sorted(tasks,key=lambda t:(-t["live_parents"],t["truncated_cost_proxy_nodes"],t["key"])))
    (out_dir/"strategy-analysis.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
        "cache_rows":len(cache),"s4_counts":dict(overall),"candidates":len(candidates),
        "candidate_status":dict(cstat),"active_s5_keys":len(active_incidence),
        "live_degree_distribution":summary["active_unknown_s5_degree_distribution"],
        "unknown_best":top(by_unknown,3),"proxy_best":top(by_proxy,3),
        "shared_best":top(by_shared,3),
        "joint_task_head":ready2[:3],
        "top_pair":pairs[:3],
    },ensure_ascii=False,indent=2))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--cache",type=Path,default=DEFAULT_CACHE)
    ap.add_argument("--out",type=Path,default=EXP/"output")
    a=ap.parse_args()
    build(a.cache,a.out)
