#!/usr/bin/env python3
"""Independent standard-library exact-geometry terminal proof of one S6 WIN.
No preexisting verdict caches are used. Verdicts are fixed original-first perspective.
"""
from pathlib import Path
from functools import lru_cache
from collections import Counter
from verify_core import canonical,children,safe,next_player_wins_at_s10

S6=int("00000000000100001011010000001000",16)
S7=int("00000000100100009001010000001000",16)

def check(condition,msg):
    if not condition: raise ValueError(msg)

@lru_cache(None)
def evaluate(h):
    x=int(h,16)
    check(x.bit_count()==10 and canonical(x)==x and safe(x),"bad S10 position "+h)
    return next_player_wins_at_s10(x)

def verify(path=None):
    base=Path(__file__).resolve().parent
    lines=(Path(path) if path else base/'s8_38_win_proof.tsv').read_text().splitlines()
    check(S7 in children(S6),"S7 is not a legal S6 child")
    check(S6.bit_count()==6 and canonical(S6)==S6 and safe(S6),"invalid S6")
    check(S7.bit_count()==7 and canonical(S7)==S7 and safe(S7),"invalid S7")
    obligations=children(S7)
    check(len(obligations)==38,"S7 expected 38 distinct S8 children")
    declared=[int(x,16) for x in (base/'s8_38_children.txt').read_text().split()]
    check(len(declared)==38 and len(set(declared))==38 and set(declared)==obligations,"S8 boundary incomplete")
    blocks=[]
    for line in lines:
        cols=line.split('\t')
        if cols[0]=='ROOT':
            check(len(cols)==5,"bad ROOT row")
            blocks.append((cols,[]))
        else:
            check(blocks,"orphan child")
            blocks[-1][1].append(cols)
    check(len(blocks)==38,"wrong S8 root count")
    roots=set();leaves=set();states=0
    for row,proof in blocks:
        _,h,verdict,legal_count,hint=row
        root=int(h,16)
        check(root.bit_count()==8 and safe(root) and canonical(root)==root and h==f'{root:032x}',"bad S8 root")
        check(root in obligations and root not in roots,"unexpected/duplicate S8 root")
        roots.add(root)
        check(verdict=='WIN',"not a WIN root")
        c9=children(root)
        check(len(c9)==int(legal_count),"wrong S9 count")
        check(proof and proof[0][0]=='S9_LOSS' and len(proof[0])==2,"missing S9 witness")
        s9=int(proof[0][1],16)
        check(s9 in c9,"S9 not a legal child")
        check(all(len(c)==2 and c[0]=='S10_WIN' for c in proof[1:]),"bad S10 witness rows")
        expected={f'{x:032x}' for x in children(s9)}
        found=[c[1] for c in proof[1:]]
        check(len(found)==len(set(found)) and set(found)==expected,"S9 children not exhaustive")
        leaves.update(expected)
    check(roots==obligations,"S7 child not proved")
    rows=[]
    for h in sorted(leaves):
        win,used=evaluate(h)
        check(win,"claimed S10 WIN is LOSS: "+h)
        states+=used
        rows.append((h,used))
    cpp=base/'s10_cpp_results.tsv'
    if cpp.exists():
        other={}
        for line in cpp.read_text().splitlines():
            fields=line.split('\t')
            check(len(fields)==5 and fields[0] not in other,"invalid C++ row")
            other[fields[0]]=fields
        check(len(other)==len(rows),"C++ boundary incomplete")
        for h,used in rows:
            check(h in other and other[h][1]=='WIN' and int(other[h][2])==used,"C++/Python terminal mismatch: "+h)
        print('PASS independent C++/Python per-leaf agreement',len(rows))
    print('PASS S6 WIN',f'{S6:032x}','via S7',f'{S7:032x}')
    print('PASS S7 WIN all',len(roots),'S8 children WIN')
    print('PASS independent S10 terminal WIN leaves',len(leaves),'states',states)
    return len(leaves),states

if __name__=='__main__':
    import sys
    verify(sys.argv[1] if len(sys.argv)>1 else None)
