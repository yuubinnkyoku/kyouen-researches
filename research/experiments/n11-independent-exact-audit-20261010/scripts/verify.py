"""Read-only hash, source-row, ranked DAG and independent frontier verification."""
import csv
import gzip
import json
from fractions import Fraction
from collections import Counter,defaultdict
from independent import Board,aggregate,verify_dag,mask_from_key
from audit import ROOT,OUT,digest,read_cache,dump,key

def main():
    manifest=json.loads((OUT/'source-manifest.json').read_text())
    for source in manifest['raw']+manifest['caches']:
        if digest(ROOT/source['path'])!=source['sha256']:
            raise ValueError(('source hash mismatch',source['path']))
    board=Board(11)
    forest=json.loads(gzip.decompress((OUT/'raw-rooted-proof.json.gz').read_bytes()))
    nodes, trusted = {},{}
    lines={}
    for ident,row in forest['nodes'].items():
        mask=int(row['mask'])
        node=dict(mask=str(mask),verdict=row['verdict'],children=row.get('children',[]))
        if row['kind']=='solver-replay':
            e=row['evidence']
            if e['path'] not in lines:
                with (ROOT/e['path']).open(encoding='utf-8-sig') as f: lines[e['path']]=list(csv.reader(f))
            r=lines[e['path']][e['row']-1]
            raw=mask_from_key(int(r[9]),int(r[10]))
            if (r[0]!='replay' or int(r[6])!=row['verdict'] or int(r[5])<=0 or
                int(r[2])!=mask.bit_count() or int(r[4])!=int(mask.bit_count()%2==0) or
                board.canonical(raw)!=mask or board.legal(raw).bit_count()!=int(r[3])):
                raise ValueError(('raw leaf mismatch',e))
            trusted[mask]=row['verdict']
            node['trusted']=True
        nodes[ident]=node
    verdicts=verify_dag(board,dict(roots=forest['roots'],nodes=nodes),trusted)
    cache=read_cache(ROOT/'research/experiments/n11-strategy-redesign-20261010/output/current-exact-s5.cache')
    for r,v in verdicts.items():
        if cache[int(r)]!=v: raise ValueError('reconstructed/cache conflict')
    # Regenerate the root-edge coverage and every complete S4 child set.
    root=(1<<60)|(1<<27)
    groups=defaultdict(list)
    for a in board.points(board.legal(root)):
        for b in board.points(board.legal(root|(1<<a))):
            if b>a: groups[board.canonical(root|(1<<a)|(1<<b))].append((a,b))
    frontier=json.loads(gzip.decompress((OUT/'frontier.json.gz').read_bytes()))
    if len(frontier)!=len(groups): raise ValueError('incomplete class list')
    hist=Counter(); secured=set(); third=defaultdict(list)
    for f in frontier:
        a,b=f['key']; m=a+(b<<64)
        ch=board.children(m)
        if ch!={a+(b<<64) for a,b in f['children']}: raise ValueError('incomplete S4 children')
        cov={p for edge in groups[m] for p in edge}
        if cov!=set(f['coverage']): raise ValueError('coverage mismatch')
        v=aggregate(4,[cache.get(c,0) for c in ch])
        if v!=f['verdict']: raise ValueError('S4 propagation mismatch')
        hist[v]+=1
        if v==2: secured.update(cov)
        for a,b in groups[m]: third[a].append(v); third[b].append(v)
    audit=json.loads((OUT/'audit.json').read_text())
    remaining=set(board.points(board.legal(root)))-secured
    if sorted(remaining)!=audit['remaining'] or len(secured)!=audit['secured']: raise ValueError('coverage totals')
    weights={int(k):Fraction(v) for k,v in audit['rational_dual']['weights'].items()}
    assert set(weights)<=remaining and all(v>=0 for v in weights.values())
    for f in frontier:
        if f['verdict']==0: assert sum(weights.get(p,0) for p in f['coverage'])<=1
    example=next(f for f in frontier if f['key']==audit['rational_dual']['primal_example'])
    assert example['verdict']==0 and remaining<=set(example['coverage']) and sum(weights.values())==1
    assert aggregate(2,[aggregate(3,values) for values in third.values()])==0
    # Verify the genuine terminal-leaf minimax certificates WITHOUT a trust map.
    certificates=[]
    for p in sorted(OUT.glob('minimax-*.json.gz')):
        n=int(p.name.split('-')[1][1:]) if p.name.startswith('minimax-n') else 11
        cert=json.loads(gzip.decompress(p.read_bytes()))
        v=verify_dag(Board(n),cert)
        certificates.append(dict(path=p.name,verdict=v,nodes=len(cert['nodes']),sha256=digest(p)))
    dump('verification.json',dict(hash_checked_sources=len(manifest['raw'])+len(manifest['caches']),
        raw_rooted_s5=len(verdicts),solver_trusted_leaves=len(trusted),raw_dependency_nodes=len(nodes),
        s4=dict(hist),secured=len(secured),remaining=sorted(remaining),rational_dual='1',root='UNKNOWN',
        minimax_certificates=certificates))
    print('INDEPENDENT_VERIFICATION_OK',len(verdicts),'raw-rooted S5',len(secured),'secured',len(certificates),'minimax certificates')

if __name__=='__main__': main()
