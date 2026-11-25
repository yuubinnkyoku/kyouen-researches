"""Reconstruct the frozen main evidence corpus, never launch the existing solver.

Tracked n11 CSV replay rows with positive budget are solver-trusted roots.
Caches are compared to, rather than used as leaves in, the raw reconstruction.
"""
import csv
import gzip
import hashlib
import json
import subprocess
import time
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from independent import Board, aggregate, mask_from_key

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP/'output'
CURRENT = ROOT/'research/experiments/n11-strategy-redesign-20261010/output/current-exact-s5.cache'

@lru_cache(maxsize=None)
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def dump(name, obj):
    p = OUT/name
    p.parent.mkdir(parents=True,exist_ok=True)
    data = (json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()
    p.write_bytes(gzip.compress(data,mtime=0) if name.endswith('.gz') else data)

def key(mask):
    return [mask & ((1<<64)-1),mask >> 64]

def read_cache(p):
    result = {}
    for row in csv.reader(p.open(encoding='utf-8-sig')):
        if row and row[0] == 's5verdict':
            if len(row)!=6 or int(row[3])!=5 or int(row[4]) not in (1,2):
                raise ValueError(('bad cache',p,row))
            m = mask_from_key(int(row[1]),int(row[2]))
            if m in result and result[m]!=int(row[4]):
                raise ValueError(('cache conflict',p,key(m)))
            result[m] = int(row[4])
    return result

def main():
    started = time.perf_counter()
    board = Board(11)
    files = subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
    # Path scope is explicit: other board sizes and q variants are not evidence.
    files = sorted(p for p in files if p.startswith('research/experiments/n11-')
                   and not p.startswith(EXP.relative_to(ROOT).as_posix()+'/'))
    raw, observations, sources = {}, defaultdict(list), []
    cache_union, cache_sources, contaminated = {}, [], []
    cache_evidence = defaultdict(list)
    registry = json.loads((ROOT/'results/n11-s5-evidence-quarantine.json').read_text())
    quarantine = {a+(b<<64) for r in registry['entries'] if r['active'] for a,b in [r['key']]}
    for path in files:
        p = ROOT/path
        if path.endswith('.cache'):
            cache = read_cache(p)
            if cache:
                hits = sorted(set(cache)&quarantine)
                if hits:
                    contaminated.append(dict(path=path,keys=[key(m) for m in hits]))
                for m,v in cache.items():
                    if m in quarantine:
                        continue
                    if m.bit_count()!=5 or board.canonical(m)!=m:
                        raise ValueError(('cache geometry',path,key(m)))
                    board.legal(m)
                    if cache_union.get(m,v)!=v:
                        raise ValueError(('cache union conflict',path,key(m)))
                    cache_union[m]=v
                    cache_evidence[m].append(dict(path=path,cache_rows=len(cache),sha256=digest(p)))
                cache_sources.append(dict(path=path,sha256=digest(p),rows=len(cache)))
        if not path.endswith('.csv'):
            continue
        count = 0
        with p.open(encoding='utf-8-sig',newline='') as f:
            for line,row in enumerate(csv.reader(f),1):
                if not row or row[0]!='replay':
                    continue
                if len(row)!=11:
                    raise ValueError(('malformed replay',path,line))
                n,legal,is_or,budget,v,nodes = map(int,row[2:8])
                if budget == 0:
                    continue # cache projections are not solver executions
                if not 0<=n<=121 or v not in (0,1,2) or budget<0 or nodes<0 or is_or!=int(n%2==0):
                    raise ValueError(('bad replay',path,line))
                m = mask_from_key(int(row[9]),int(row[10]))
                if len(board.points(m))!=n or board.legal(m).bit_count()!=legal:
                    raise ValueError(('raw geometry/legal',path,line,key(m)))
                m = board.canonical(m)
                ev = dict(path=path,row=line,verdict=v,budget=budget,nodes=nodes)
                observations[m].append(ev)
                if v:
                    if raw.get(m,v)!=v:
                        raise ValueError(('raw exact conflict',path,line,key(m)))
                    raw[m]=v
                count += 1
        if count:
            sources.append(dict(path=path,sha256=digest(p),replay_rows=count))
    dump('source-manifest.json',dict(raw=sources,caches=cache_sources,
        registry_sha256=digest(ROOT/'results/n11-s5-evidence-quarantine.json'),
        baseline_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()))
    print('RAW',dict(Counter(m.bit_count() for m in raw)),'CACHE',len(cache_union),flush=True)
    exact = dict(raw)
    proof = {m:dict(kind='solver-replay',evidence=min((e for e in observations[m] if e['verdict']),key=lambda e:e['nodes'])) for m in raw}
    # Descending layers forbid cycles. Decisive reverse propagation first, then
    # full-boundary deductions for known parents and cache claims under audit.
    targets = defaultdict(set)
    targets[5].update(cache_union)
    targets[5].update(quarantine)
    for m in raw:
        targets[m.bit_count()].add(m)
    for n in range(max(targets),5,-1):
        decisive_parent = 2 if (n-1)%2 else 1
        for m,v in list(exact.items()):
            if m.bit_count()!=n:
                continue
            for parent in board.predecessors(m):
                if n==6 and v!=decisive_parent and parent not in targets[n-1]:
                    continue
                targets[n-1].add(parent)
                if v == decisive_parent:
                    if exact.get(parent,v)!=v:
                        raise ValueError(('reverse conflict',key(parent),key(m)))
                    if parent not in exact:
                        exact[parent]=v
                        proof[parent]=dict(kind='decisive-child',children=[str(m)])
        for parent in sorted(targets[n-1]):
            if parent in exact:
                continue
            ch = board.children(parent)
            v = aggregate(n-1,[exact.get(c,0) for c in ch])
            if v:
                exact[parent]=v
                proof[parent]=dict(kind='complete-boundary',children=[str(c) for c in sorted(ch)])
    current = read_cache(CURRENT)
    if quarantine & set(current):
        raise ValueError('current cache contains withdrawn evidence')
    if current != cache_union:
        raise ValueError(('current/union mismatch',len(current),len(cache_union)))
    supported = {m:exact[m] for m in current if m in exact}
    unsupported = sorted(set(current)-set(supported))
    conflicts = [key(m) for m in supported if supported[m]!=current[m]]
    if conflicts:
        raise ValueError(('current/raw proof conflict',conflicts))
    print('RECONSTRUCTED',len(supported),'UNSUPPORTED',len(unsupported),flush=True)
    dump('cache-only-claims.json',[dict(key=key(m),verdict=current[m],
        limitation='no matching positive-budget replay or complete raw-rooted derivation in tracked n11 corpus',
        evidence=min(cache_evidence[m],key=lambda e:(e['cache_rows'],e['path']))) for m in unsupported])
    # Frontier is recomputed from current cache only after its raw proof coverage
    # is reported. Unsupported claims must remain explicit trust assumptions.
    root = (1<<60)|(1<<27)
    groups = defaultdict(list)
    for a in board.points(board.legal(root)):
        for b in board.points(board.legal(root|(1<<a))):
            if b>a:
                groups[board.canonical(root|(1<<a)|(1<<b))].append((a,b))
    frontier, secured, s3 = [], set(), {}
    affected = []
    for m,edges in sorted(groups.items()):
        ch = board.children(m)
        v = aggregate(4,[current.get(c,0) for c in ch])
        cov = sorted({p for e in edges for p in e})
        if v==2:
            secured.update(cov)
        for a,b in edges:
            for third in (a,b):
                s3.setdefault(third,[]).append(v)
        hits = ch & quarantine
        if hits:
            old = aggregate(4,[1 if c in quarantine else current.get(c,0) for c in ch])
            affected.append(dict(key=key(m),withdrawn_children=[key(c) for c in sorted(hits)],
                previous_with_bad_evidence=old,current=v,coverage=cov,
                independent_win_witnesses=[key(c) for c in sorted(ch) if current.get(c)==1]))
        frontier.append(dict(key=key(m),verdict=v,coverage=cov,children=[key(c) for c in sorted(ch)],
                             raw_supported_children=sum(c in supported for c in ch)))
    remaining = set(board.points(board.legal(root)))-secured
    raw_only_secured = set()
    for f in frontier:
        if aggregate(4,[supported.get(a+(b<<64),0) for a,b in f['children']])==2:
            raw_only_secured.update(f['coverage'])
    unknown = [f for f in frontier if f['verdict']==0]
    examples = [f for f in unknown if remaining <= set(f['coverage'])]
    if not remaining or not examples:
        raise ValueError('single-class bound no longer applies; recompute optimization')
    weights = {min(remaining):Fraction(1)}
    dual_sum = sum(weights.values())
    max_weight = max(sum(weights.get(p,Fraction(0)) for p in f['coverage']) for f in unknown)
    assert max_weight<=1 and dual_sum==1
    root_verdict = aggregate(2,[aggregate(3,vs) for _,vs in sorted(s3.items())])
    assert len(s3)==board.legal(root).bit_count()
    dump('frontier.json.gz',frontier)
    third_certificate=[]
    for third,values in sorted(s3.items()):
        witnesses=[f for f in frontier if f['verdict']==2 and third in f['coverage']]
        third_certificate.append(dict(move=third,verdict=aggregate(3,values),
            loss_class_witness=witnesses[0]['key'] if witnesses else None))
    dump('third-move-certificate.json',dict(root=key(root),proposition='original first player wins',
        leaf_trust='solver replay or persisted cache verdict; not blanket independent minimax',
        complete_third_moves=third_certificate))
    dump('withdrawal-dependencies.json',dict(contaminated_cache_files=contaminated,affected_s4=affected,
        withdrawn=[dict(key=key(m),direct_exact=raw.get(m,0),correct_derivation=exact.get(m,0),
                       observations=observations[m]) for m in sorted(quarantine)]))
    # Persist the minimal raw-rooted dependency DAG for every current S5 claim.
    reachable = {}
    def collect(m):
        if str(m) in reachable:
            return
        reachable[str(m)] = dict(mask=str(m),verdict=exact[m],**proof[m])
        for c in proof[m].get('children',[]):
            if int(c).bit_count()!=m.bit_count()+1:
                raise ValueError('unranked evidence')
            collect(int(c))
    for m in supported:
        collect(m)
    dump('raw-rooted-proof.json.gz',dict(leaf_trust='solver exact replay',nodes=reachable,
                                      roots=[str(m) for m in sorted(supported)]))
    (OUT/'reconstructed-exact-s5.cache').write_text('# s5 verdict cache: n=11 schema=1 (independent raw-rooted reconstruction)\n'+
        ''.join(f's5verdict,{key(m)[0]},{key(m)[1]},5,{supported[m]},0\n' for m in sorted(supported)),encoding='utf-8')
    (OUT/'canonical-current-s5.cache').write_text('# s5 verdict cache: n=11 schema=1 (quarantine checked; mixed replay/cache trust, see audit.json)\n'+
        ''.join(f's5verdict,{key(m)[0]},{key(m)[1]},5,{current[m]},0\n' for m in sorted(current)),encoding='utf-8')
    report = dict(tracked_csv_scope='research/experiments/n11-*; positive-budget replay only',
        raw_sources=len(sources),raw_rows=sum(s['replay_rows'] for s in sources),
        raw_exact_by_layer=dict(Counter(m.bit_count() for m in raw)),cache_files=len(cache_sources),
        contaminated_cache_files=len(contaminated),quarantined_keys=len(quarantine),
        current_exact_s5=dict(rows=len(current),WIN=sum(v==1 for v in current.values()),LOSS=sum(v==2 for v in current.values())),
        raw_rooted_supported_s5=len(supported),cache_only_claims=len(unsupported),conflicts=conflicts,
        s4=dict(Counter({0:'UNKNOWN',1:'WIN',2:'LOSS'}[f['verdict']] for f in frontier)),
        loss_classes_raw_supported=sum(f['verdict']==2 and f['raw_supported_children']==len(f['children']) for f in frontier),
        raw_only_secured=len(raw_only_secured),
        canonical_s4=len(frontier),raw_s4_edges=sum(map(len,groups.values())),secured=len(secured),remaining=sorted(remaining),
        affected_s4=len(affected),changed_s4=sum(f['previous_with_bad_evidence']!=f['current'] for f in affected),
        minimum_additional_classes=1,rational_dual=dict(weights={str(k):str(v) for k,v in weights.items()},
                 value=str(dual_sum),max_class_weight=str(max_weight),primal_example=examples[0]['key']),
        root={0:'UNKNOWN',1:'WIN',2:'LOSS'}[root_verdict],empty='UNKNOWN',
        solver_trust='Every solver-replay proof leaf remains an unverified minimax assumption.',
        seconds=time.perf_counter()-started)
    dump('audit.json',report)
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':
    main()
