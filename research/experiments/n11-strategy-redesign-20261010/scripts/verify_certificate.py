"""Portable upper-certificate/full-coverage audit, requiring no .local binary.

Exact leaf verdicts are trusted input, not independently re-solved minimax.
"""
import csv
import gzip
import json
from collections import Counter, defaultdict
from audit import ROOT, EXP, points, safe, canonical, children, aggregate, legal
from study import sha, dump, s5cache

def main():
    out=EXP/'output'
    cert=json.loads((out/'upper-boundary-certificate.json').read_text())
    assert cert['original_first_player'] is True and cert['root']=='UNKNOWN'
    supported={}
    for parent in cert['s5']:
        pk=tuple(parent['key'])
        ch=children(pk)
        assert ch=={tuple(r['key']) for r in parent['leaves']}
        assert len(ch)==parent['complete_children']
        for leaf in parent['leaves']:
            k=tuple(leaf['key'])
            e=leaf['evidence']
            assert e is not None
            p=ROOT/e['path']
            assert '.local' not in p.parts and sha(p)==e['sha256']
            raw=list(csv.reader(p.open(encoding='utf-8-sig')))[e['row']-1]
            assert len(raw)==11 and raw[0]=='replay'
            rp=points((int(raw[9]),int(raw[10])))
            v=int(raw[6])
            assert int(raw[2])==6 and int(raw[4])==1 and v in (1,2)
            assert canonical(rp)==k and len(legal(rp))==int(raw[3])
            assert v==leaf['verdict'] and supported.get((6,*k),v)==v
            supported[6,*k]=v
        assert aggregate(5,ch,supported)==parent['verdict']
    cache=s5cache(out/'current-exact-s5.cache')
    for k in cache:
        assert safe(points(k)) and canonical(points(k))==k
    for p in cert['s5']:
        assert cache[tuple(p['key'])]==p['verdict']
    # Reconstruct ALL raw root edges with this verifier's D4, not the generator.
    raw=defaultdict(list)
    root=(60,27)
    for a in legal(root):
        for b in legal((*root,a)):
            if b>a:
                raw[canonical((*root,a,b))].append((a,b))
    geo=json.loads(gzip.decompress((out/'geometry.json.gz').read_bytes()))
    assert len(raw)==len(geo)==3384 and sum(map(len,raw.values()))==6871
    hist=Counter()
    class_status={}
    secured=set()
    for g in geo:
        k=tuple(g['key'])
        cov={v for edge in raw[k] for v in edge}
        assert cov==set(g['coverage'])
        ch=children(k)
        assert ch=={tuple(c) for c in g['children']}
        vals=[cache.get(c,0) for c in ch]
        st='WIN' if 1 in vals else 'LOSS' if all(v==2 for v in vals) else 'UNKNOWN'
        hist[st]+=1
        class_status[k]=st
        if st=='LOSS':
            secured.update(cov)
    audit=json.loads((out/'audit.json').read_text())
    assert dict(hist)==audit['s4'] and len(secured)==audit['secured']
    remaining=set(legal(root))-secured
    assert sorted(remaining)==audit['remaining']==[100,108]
    example=tuple(audit['dual']['primal_example'])
    assert class_status[example]=='UNKNOWN'
    assert remaining.issubset({v for edge in raw[example] for v in edge})
    # Single weight 1 on 100: every candidate's weight is 0 or 1, and a
    # feasible single UNKNOWN class exists. Hence integer minimum = dual = 1.
    assert audit['dual']['weights']=={'100':'1'}
    print('PORTABLE_CERTIFICATE_GEOMETRY_OK',len(supported),'S6 leaves; S4',dict(hist),'secured',len(secured),flush=True)
    dump(out/'portable-verification.json',dict(verified_s6_leaves=len(supported),raw_edges=6871,canonical_s4=3384,
         s4=dict(hist),secured=len(secured),remaining=sorted(remaining),minimum_additional_classes=1,rational_dual='1',
         local_binary_required=False,leaf_minimax_independently_verified=False,
         certificate_sha256=sha(out/'upper-boundary-certificate.json'),cache_sha256=sha(out/'current-exact-s5.cache')))

if __name__=='__main__':
    main()
