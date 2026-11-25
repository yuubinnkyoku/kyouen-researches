"""Rebuild reply27 geometry and a deduplicated, hash-bound replay history.

Scores are descriptive scheduling proxies, never game verdicts.
"""
import csv
import gzip
import hashlib
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / 'research/experiments/n11-strategy-redesign-20261010'
OLD = ROOT / 'research/experiments/n11-boundary-recovery-20261006/output'
sys.path.insert(0, str(ROOT / 'research/experiments/n11-search-methods/scripts'))
sys.path.insert(0, str(OLD.parent / 'scripts'))
from dfpn_edge_classes import d4_canonical_key
from n11_integer_circle_geometry import legal_points

A = (1333065489702715392, 0)
SUSPECT = {(10448351135499552768,128), (1152925911243358208,536870912)}
BASE = OLD / 'post-23b52acf-after-round3-round4-completed-merged-s5.cache'

import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(_PolicyPath(__file__).resolve().parents[4] / 'research/experiments/n11-frontier-selection-20261005/scripts'))
from s5_evidence_policy import quarantined_cache_keys

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def pts(key):
    lo, hi = key
    assert 0 <= lo < 1 << 64 and 0 <= hi < 1 << 57
    return tuple(i for i in range(121) if ((lo if i < 64 else hi) >> (i % 64)) & 1)

def canon(p):
    return tuple(d4_canonical_key(p))

def children(key):
    p = pts(key)
    return {canon((*p, m)) for m in legal_points(p)}

def dump(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf-8')

def s5cache(path=BASE):
    _s5_quarantine = quarantined_cache_keys()
    out = {}
    for r in csv.reader(Path(path).open(encoding='utf-8-sig')):
        if r and r[0] == 's5verdict':
            k, v = (int(r[1]), int(r[2])), int(r[4])
            if k in _s5_quarantine:
                continue
            assert int(r[3]) == 5 and v in (1, 2)
            assert k not in out or out[k] == v
            out[k] = v
    return out

def status(keys, exact):
    vals = [exact.get(k, 0) for k in keys]
    if 1 in vals:
        return 'WIN'
    if all(v == 2 for v in vals):
        return 'LOSS'
    return 'UNKNOWN'

def prepare():
    out = EXP / 'output'
    out.mkdir(parents=True, exist_ok=True)
    cache = s5cache()
    # These two derived entries used the wrong fixed-player S7 polarity.
    # Retain the historical file, quarantine entries until direct revalidation.
    for k in SUSPECT:
        cache.pop(k, None)
    # Independent integer-circle geometry; compare boundaries for EVERY edge.
    groups = defaultdict(list)
    root = (60, 27)
    for a in legal_points(root):
        for b in legal_points((*root, a)):
            if b > a:
                groups[canon((*root, a, b))].append((a, b))
    assert len(groups) == 3384 and sum(map(len, groups.values())) == 6871
    geo, secured = [], set()
    for key, edges in sorted(groups.items()):
        ch = children(key)
        for a, b in edges:
            assert {canon((*root, a, b, z)) for z in legal_points((*root, a, b))} == ch
        cov = set(v for edge in edges for v in edge)
        st = status(ch, cache)
        if st == 'LOSS':
            secured |= cov
        geo.append(dict(key=key, coverage=sorted(cov), children=sorted(ch), status=st,
                        counts=dict(Counter({1:'WIN', 2:'LOSS', 0:'UNKNOWN'}[cache.get(c,0)] for c in ch))))
    (out / 'geometry.json.gz').write_bytes(gzip.compress(json.dumps(geo).encode(), mtime=0))
    remaining = set(legal_points(root)) - secured
    candidates = [g for g in geo if remaining.intersection(g['coverage'])]
    relevant_s5 = {tuple(k) for g in candidates for k in g['children']} | set(cache) | SUSPECT
    print('geometry', Counter(g['status'] for g in geo), 'remaining', sorted(remaining), flush=True)
    # All replay observations for S5 relevant to B and ALL S6/S7/S8/S9/S10.
    csv.field_size_limit(100_000_000)
    hist = defaultdict(dict)
    sources = []
    files = sorted(set((ROOT/'research/experiments').rglob('*.csv')) | set((ROOT/'.local').rglob('*.csv')))
    for file in files:
        if EXP in file.parents:
            continue
        matched = 0
        try:
            with file.open(encoding='utf-8-sig', newline='') as f:
                for line, r in enumerate(csv.reader(f), 1):
                    if len(r) != 11 or r[0] != 'replay' or not r[2].isdigit():
                        continue
                    n = int(r[2])
                    if not 5 <= n <= 10:
                        continue
                    raw = int(r[9]), int(r[10])
                    p = pts(raw)
                    assert len(p) == n and int(r[4]) == int(n % 2 == 0)
                    k = canon(p)
                    if n == 5 and k not in relevant_s5:
                        continue
                    v, budget, nodes, legal = int(r[6]), int(r[5]), int(r[7]), int(r[3])
                    if budget == 0:
                        continue  # derived cache projections are not raw solver runs
                    assert v in (0,1,2) and budget > 0 and nodes >= 0, (file,line,r)
                    # Validate geometry once per canonical key; copies are deduplicated.
                    hkey = (n, *k)
                    if hkey not in hist:
                        assert len(legal_points(p)) == legal
                    obs = (budget, v, nodes, legal)
                    hist[hkey].setdefault(obs, dict(budget=budget, verdict=v, nodes=nodes, legal=legal,
                                                  path=file.relative_to(ROOT).as_posix(), row=line))
                    matched += 1
        except (UnicodeError, csv.Error):
            continue
        if matched:
            sources.append(dict(path=file.relative_to(ROOT).as_posix(), sha256=sha(file), rows=matched))
    exact = {}
    history = []
    for k, obs in sorted(hist.items()):
        vs = {o['verdict'] for o in obs.values()} - {0}
        assert len(vs) <= 1, (k, vs)
        v = next(iter(vs), 0)
        exact[k] = v
        if k[0] == 5 and v:
            assert tuple(k[1:]) not in cache or cache[tuple(k[1:])] == v
        history.append(dict(stones=k[0], key=k[1:], verdict=v, observations=list(obs.values()),
                            max_unknown_budget=max((o['budget'] for o in obs.values() if o['verdict']==0), default=0)))
    dump(out/'history.json', history)
    dump(out/'history-sources.json', dict(scanned_files=len(files), matching_files=len(sources), sources=sources,
                                       conflicts=0, unknown_is_not_exact=True))
    # 15M historical truncated costs, one observation per canonical key.
    s5obs = []
    for k, obs in hist.items():
        if k[0] == 5:
            elig = [o for o in obs.values() if o['budget'] == 15_000_000]
            if elig:
                s5obs.append(min(elig, key=lambda x: (x['verdict']==0, x['nodes'])))
    buckets = defaultdict(list)
    for o in s5obs:
        buckets[o['legal']//10*10].append(o)
    profile = {}
    for b, obs in buckets.items():
        profile[b] = dict(n=len(obs), verdicts=dict(Counter(o['verdict'] for o in obs)),
                          mean_truncated_nodes=statistics.mean(o['nodes'] for o in obs),
                          median_nodes=statistics.median(o['nodes'] for o in obs))
    b_rows = []
    for g in candidates:
        if g['status'] != 'UNKNOWN':
            continue
        unknown = [tuple(c) for c in g['children'] if tuple(c) not in cache]
        legals = [len(legal_points(pts(k))) for k in unknown]
        empirical = sum(profile.get(l//10*10, {'mean_truncated_nodes':15_000_000})['mean_truncated_nodes'] for l in legals)
        hheld = sum(any(o['budget']>=2_000_000 for o in hist.get((5,*k),{}).values() if o['verdict']==0) for k in unknown)
        s6ch = {k:children(k) for k in unknown}
        s6union = set().union(*s6ch.values())
        derived_loss = [k for k,ch in s6ch.items() if any(exact.get((6,*c))==2 for c in ch)]
        derived_win = [k for k,ch in s6ch.items() if all(exact.get((6,*c))==1 for c in ch)]
        b_rows.append(dict(key=g['key'], coverage=g['coverage'], counts=g['counts'], unknown=len(unknown),
                           full_remaining_coverage=remaining.issubset(g['coverage']),
                           estimated_capped_15m_completion_nodes=empirical,
                           legal_min=min(legals), legal_max=max(legals), held_at_2m=hheld,
                           saved_s6_derived_loss=derived_loss, saved_s6_derived_win=derived_win,
                           s6_unique=len(s6union), s6_incidences=sum(map(len,s6ch.values())),
                           saved_exact_s6_overlap=sum(exact.get((6,*c),0)!=0 for c in s6union),
                           unknown_keys=unknown))
    b_rows.sort(key=lambda r:(not r['full_remaining_coverage'], r['estimated_capped_15m_completion_nodes'],r['key']))
    dump(out/'b-candidates.json', b_rows)
    dump(out/'historical-cost-profile.json', dict(profile=profile, unique_s5_15m=len(s5obs),
          caveat='selected surviving-class children; censored at 15M; no calibrated probability or upper bound'))
    a_s5 = [tuple(c) for g in geo if tuple(g['key'])==A for c in g['children'] if tuple(c) not in cache]
    a_s6 = {k:children(k) for k in a_s5}
    a_unknown = sorted({c for ch in a_s6.values() for c in ch if not exact.get((6,*c),0)})
    assert len(a_unknown)==6
    a_s7 = {k:children(k) for k in a_unknown}
    s7union = set().union(*a_s7.values())
    # One complete S6 LOSS child per S5, minimizing distinct S7 obligation count.
    choices = [[c for c in ch if c in a_unknown] for ch in a_s6.values()]
    pairs = sorted((len(a_s7[x]|a_s7[y]), x,y) for x in choices[0] for y in choices[1])
    dump(out/'a-boundary.json', dict(s5=[dict(key=k, children=sorted(ch)) for k,ch in a_s6.items()],
          s6=[dict(key=k, children=sorted(ch)) for k,ch in a_s7.items()],
          unique_s7=len(s7union), incidences=sum(map(len,a_s7.values())),
          loss_direction_min_complete_pair=pairs[0],
          exact_s7_overlap=sum(bool(exact.get((7,*c))) for c in s7union)))
    dump(out/'baseline.json',dict(root=root, cache_path=BASE.relative_to(ROOT).as_posix(), cache_sha256=sha(BASE),
          cache_counts=dict(Counter(cache.values())), class_counts=dict(Counter(g['status'] for g in geo)),
          secured=len(secured), remaining=sorted(remaining), all_covering_candidates=len(candidates),
          covering_win=sum(g['status']=='WIN' for g in candidates), candidate_unknown=len(b_rows),
          s5_raw_exact_extra=[k[1:] for k,v in exact.items() if k[0]==5 and v and tuple(k[1:]) not in cache]))
    print('candidate ranking', [(r['key'],r['unknown'],round(r['estimated_capped_15m_completion_nodes'])) for r in b_rows[:6]],flush=True)

if __name__ == '__main__':
    prepare()
