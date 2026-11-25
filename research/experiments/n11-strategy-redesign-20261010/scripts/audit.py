"""Independent determinant/D4 audit, fixed-player propagation, exact-only merge.

Geometry and boundary completeness are independent of the C++ solver. Exact
leaf verdicts remain solver-trusted; this is NOT an independently replayed
whole-game AND/OR certificate.
"""
import csv
import gzip
import itertools
import json
import shutil
from collections import Counter
from pathlib import Path
from study import ROOT, EXP, OLD, BASE, A, SUSPECT, sha, dump, s5cache

def points(k):
    a,b=k
    assert 0<=a<2**64 and 0<=b<2**57
    return tuple(i for i in range(121) if ((a if i<64 else b)>>(i%64))&1)

def determinant(rows):
    # Independent Laplace expansion, not the solver's completion masks.
    if len(rows)==1:
        return rows[0][0]
    return sum((-1)**i*v*determinant([r[:i]+r[i+1:] for r in rows[1:]])
               for i,v in enumerate(rows[0]))

def safe(p):
    for four in itertools.combinations(p,4):
        if forbidden(four):
            return False
    return True

def forbidden(four):
    # Subtract the last row of [q,x,y,1] from the first three, then
    # expand in its final column. This is exactly the 4x4 determinant.
    x,y=four[3]%11,four[3]//11
    q=x*x+y*y
    rows=[]
    for v in four[:3]:
        xx,yy=v%11,v//11
        rows.append((xx*xx+yy*yy-q,xx-x,yy-y))
    a,b,c=rows
    return (a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])
            +a[2]*(b[0]*c[1]-b[1]*c[0]))==0

def canonical(p):
    images=[]
    for reflect in (False,True):
        for rotations in range(4):
            img=[]
            for v in p:
                x,y=v%11,v//11
                if reflect:
                    x=10-x
                for _ in range(rotations):
                    x,y=y,10-x
                img.append(y*11+x)
            mask=sum(1<<v for v in img)
            images.append((mask&((1<<64)-1),mask>>64))
    return min(images,key=lambda k:(k[1],k[0]))

def legal(p):
    assert safe(p)
    triples=list(itertools.combinations(p,3))
    return [m for m in range(121) if m not in p and not any(forbidden((*t,m)) for t in triples)]

def children(k):
    p=points(k)
    return {canonical((*p,m)) for m in legal(p)}

def aggregate(stones,ch,exact):
    vals=[exact.get((stones+1,*k),0) for k in ch]
    if stones%2==0:
        if 1 in vals:
            return 1
        return 2 if all(v==2 for v in vals) else 0
    if 2 in vals:
        return 2
    return 1 if all(v==1 for v in vals) else 0

def main():
    out=EXP/'output'
    history=json.loads((out/'history.json').read_text())
    hist_sources=json.loads((out/'history-sources.json').read_text())
    # Validate recorded historical raw hashes (no new computation).
    for s in hist_sources['sources']:
        assert sha(ROOT/s['path'])==s['sha256'],s['path']
    exact={}
    evidence={}
    for h in history:
        if h['verdict']:
            k=(h['stones'],*h['key'])
            exact[k]=h['verdict']
            obs=min((o for o in h['observations'] if o['verdict']),key=lambda o:o['nodes'])
            evidence[k]=dict(path=obs['path'],row=obs['row'],sha256=sha(ROOT/obs['path']),nodes=obs['nodes'])
    new=[]
    for summary in sorted(out.glob('*/summary.json')):
        run=json.loads(summary.read_text())
        assert sha(ROOT/run['plan'])==run['plan_sha256']
        assert sha(ROOT/run['solver_path'])==run['solver_sha256']
        assert sha(ROOT/'cpp/solvers/kyouen_dfpn_root.cpp')==run['solver_source_sha256']
        for r in run['results']:
            if r.get('verdict') is None:
                continue
            k=tuple(r['key'])
            n=r['stones']
            p=points(k)
            assert len(p)==n and canonical(p)==k and len(legal(p))==r['legal']
            for role in ('input','raw','log'):
                assert sha(ROOT/r[role])==r[role+'_sha256']
            raw=list(csv.reader((ROOT/r['raw']).open()))
            found=[(line+1,x) for line,x in enumerate(raw) if x and x[0]=='replay']
            assert len(found)==1
            line,x=found[0]
            assert [int(x[i]) for i in (2,3,4,5,6,7,9,10)]==[n,r['legal'],int(n%2==0),r['budget'],r['verdict'],r['nodes'],*k]
            hkey=(n,*k)
            if r['verdict']:
                assert exact.get(hkey,r['verdict'])==r['verdict'],('conflict',hkey)
                exact[hkey]=r['verdict']
                evidence[hkey]=dict(path=r['raw'],row=line,sha256=r['raw_sha256'],nodes=r['nodes'])
            new.append(r)
    # Historical erroneous S5 WIN deductions are quarantined unless there is
    # separate exact replay support. They are not inferred from an S7 LOSS.
    cache=s5cache()
    quarantine=[]
    for k in SUSPECT:
        if not exact.get((5,*k)):
            cache.pop(k,None)
            quarantine.append(k)
    a_boundary=json.loads((out/'a-boundary.json').read_text())
    derived6=[]
    for row in a_boundary['s6']:
        k=tuple(row['key'])
        ch=children(k)
        assert ch=={tuple(c) for c in row['children']}
        v=aggregate(6,ch,exact)
        if v:
            assert exact.get((6,*k),v)==v
            exact[6,*k]=v
            derived6.append(dict(key=k,verdict=v,children=sorted(ch)))
    # Bind complete A S5->S6 certificates, preserving reused raw evidence.
    reused=out/'reused-raw'
    reused.mkdir(exist_ok=True)
    cert=[]
    for row in a_boundary['s5']:
        k=tuple(row['key'])
        ch=children(k)
        assert ch=={tuple(c) for c in row['children']}
        leaves=[]
        for c in sorted(ch):
            hkey=(6,*c)
            ev=evidence.get(hkey)
            if ev and not (EXP in (ROOT/ev['path']).parents):
                src=ROOT/ev['path']
                dst=reused/(ev['sha256']+'.csv')
                if not dst.exists():
                    shutil.copyfile(src,dst)
                assert sha(dst)==ev['sha256']
                ev=ev|dict(original_path=ev['path'],path=dst.relative_to(ROOT).as_posix())
            if ev:
                raw=list(csv.reader((ROOT/ev['path']).open(encoding='utf-8-sig')))[ev['row']-1]
                assert raw[0]=='replay' and int(raw[2])==6 and int(raw[6])==exact[hkey]
                rp=points((int(raw[9]),int(raw[10])))
                assert canonical(rp)==c and safe(rp) and len(legal(rp))==int(raw[3])
            leaves.append(dict(key=c,verdict=exact.get(hkey,0),evidence=ev))
        v=aggregate(5,ch,exact)
        if v:
            assert cache.get(k,v)==v
            cache[k]=v
        cert.append(dict(key=k,verdict=v,complete_children=len(ch),leaves=leaves))
    # All newly found direct S6 LOSS witnesses are reusable for every safe S5
    # predecessor. Derive only after independent geometry and reverse incidence.
    reverse=[]
    for r in new:
        k=tuple(r['key'])
        if r['stones']==5 and r['verdict']:
            assert cache.get(k,r['verdict'])==r['verdict']
            cache[k]=r['verdict']
        if r['stones']==6 and r['verdict']==2:
            p=points(k)
            for removed in p:
                parent=canonical(tuple(v for v in p if v!=removed))
                assert safe(points(parent)) and k in children(parent)
                assert cache.get(parent,2)==2
                cache[parent]=2
                reverse.append(dict(s6=k,s5=parent))
    with (out/'current-exact-s5.cache').open('w',encoding='utf-8',newline='') as f:
        f.write('# fixed-player exact S5 cache; unsupported legacy S7 inversions quarantined\n')
        for k,v in sorted(cache.items()):
            f.write(f's5verdict,{k[0]},{k[1]},5,{v},0\n')
    # Recompute every S4 status against reconstructed complete geometry.
    geo=json.loads(gzip.decompress((out/'geometry.json.gz').read_bytes()))
    secured=set()
    status_counts=Counter()
    full_classes=[]
    for g in geo:
        k=tuple(g['key'])
        vals=[cache.get(tuple(c),0) for c in g['children']]
        v=1 if 1 in vals else 2 if all(x==2 for x in vals) else 0
        status_counts[{0:'UNKNOWN',1:'WIN',2:'LOSS'}[v]]+=1
        if v==2:
            secured.update(g['coverage'])
        if k==A or any(r.get('group')=='B-'+str(list(k)) for r in new):
            ch=children(k)
            assert ch=={tuple(c) for c in g['children']}
            full_classes.append(dict(key=k,verdict=v,coverage=g['coverage'],
                       counts=dict(Counter({0:'UNKNOWN',1:'WIN',2:'LOSS'}[cache.get(c,0)] for c in ch))))
    remaining=sorted(set(range(121))-{60,27}-secured)
    unk=[g for g in geo if not any(cache.get(tuple(c))==1 for c in g['children']) and
         any(tuple(c) not in cache for c in g['children'])]
    # With exactly two remaining vertices, the integer cardinality and rational
    # dual are elementary: one candidate covers both; weight 1 on one vertex.
    both=[g for g in unk if set(remaining).issubset(g['coverage'])]
    assert len(remaining)==2 and both
    dump(out/'upper-boundary-certificate.json',dict(schema='fixed-player-upper-boundary-v1',
          original_first_player=True,s5=cert,s6_from_complete_s7=derived6,
          leaf_trust='C++ exact solver; geometry does not verify recursive minimax verdict',
          root='UNKNOWN',empty='UNKNOWN'))
    report=dict(new_verdict_counts=dict(Counter(f'S{r["stones"]}_{r["verdict"]}' for r in new)),
        total_new_nodes=sum(r['nodes'] for r in new),conflicts=0,quarantined_s5=quarantine,
        exact_s5=dict(rows=len(cache),WIN=sum(v==1 for v in cache.values()),LOSS=sum(v==2 for v in cache.values()),
                      UNKNOWN_excluded=True,conflicts=0),
        s4=dict(status_counts),secured=len(secured),remaining=remaining,minimum_additional_classes=1,rational_dual='1',
        dual=dict(weights={str(remaining[0]):'1'},max_class_weight='1',primal_example=both[0]['key']),
        full_class_audits=full_classes,s6_reverse_propagations=reverse,
        a_s5_outcomes=[dict(key=r['key'],verdict=r['verdict']) for r in cert],
        geometry='independent exact determinant and independent D4; full S4 reconstruction in geometry.json.gz',
        trust='exact leaf outcomes are solver-trusted, not independently minimax-certified',root='UNKNOWN',empty='UNKNOWN')
    dump(out/'audit.json',report)
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':
    main()
