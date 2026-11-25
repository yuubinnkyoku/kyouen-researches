#!/usr/bin/env python3
"""Independent geometry/terminal verification of 24 S8 neighbor certificates.
Only Python standard library; ignores C++ verdicts and all external caches.
"""
from pathlib import Path
from functools import lru_cache
from collections import Counter
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from verify_core import canonical,children,safe,points,next_player_wins_at_s10

def fail(msg): raise ValueError(msg)
def require(c,msg):
    if not c: fail(msg)

@lru_cache(None)
def eval_s10(h):
    b=int(h,16)
    require(b.bit_count()==10 and canonical(b)==b and safe(b),'unsafe or noncanonical S10 '+h)
    return next_player_wins_at_s10(b)

def parse(path):
    blocks=[]
    for line in Path(path).read_text().splitlines():
        x=line.split('\t')
        if x[0]=='ROOT':
            require(len(x)==5,'bad root row')
            blocks.append({'root':x[1],'result':x[2],'legal':int(x[3]),'hint':int(x[4]),'children':[]})
        else:
            require(blocks and x[0] in ('S9_WIN','S9_LOSS','S10_WIN'),'bad evidence row')
            blocks[-1]['children'].append(x)
    return blocks

def verify(path):
    blocks=parse(path)
    require(len(blocks)==22,'root count')
    seen=set();stat=Counter();all10=set()
    for row in blocks:
        h=row['root']; b=int(h,16)
        require(h==f'{b:032x}' and b.bit_count()==8 and canonical(b)==b and safe(b),'invalid S8 '+h)
        require(h not in seen,'duplicate S8 root')
        seen.add(h)
        c9=children(b)
        require(len(c9)==row['legal'],'incorrect S9 count')
        rows=row['children']
        if row['result']=='LOSS':
            require(all(len(x)==3 and x[0]=='S9_WIN' for x in rows),'bad S9 WIN rows')
            mapping={int(x[1],16):int(x[2],16) for x in rows}
            require(len(mapping)==len(rows) and set(mapping)==c9,'incomplete S9 obligations')
            for s9,s10 in mapping.items():
                require(s10 in children(s9),'S10 witness not a child')
                h10=f'{s10:032x}'
                require(not eval_s10(h10)[0],'claimed S10 LOSS is WIN '+h10)
                all10.add(h10)
            stat['loss']+=1
        elif row['result']=='WIN':
            require(rows and rows[0][0]=='S9_LOSS' and len(rows[0])==2,'missing S9 LOSS witness')
            s9=int(rows[0][1],16)
            require(s9 in c9,'S9 witness not child')
            h10=[x[1] for x in rows[1:]]
            require(all(len(x)==2 and x[0]=='S10_WIN' for x in rows[1:]),'invalid S10 WIN rows')
            require(set(h10)=={f'{x:032x}' for x in children(s9)},'incomplete S10 children')
            for h in set(h10):
                require(eval_s10(h)[0],'claimed S10 WIN is LOSS '+h)
                all10.add(h)
            stat['win']+=1
        else:fail('invalid root verdict')
    require(stat['win']+stat['loss']==22,'unexpected verdict totals')
    stats={'s8_win':stat['win'],'s8_loss':stat['loss'],'s8_roots':len(blocks),'s10_proof_leaves':len(all10),'s10_terminal_states':sum(eval_s10(h)[1] for h in all10), 's10_win':sum(eval_s10(h)[0] for h in all10)}
    require(stats['s10_proof_leaves']>0,'empty proof')
    print('PASS',stats)
    return stats
if __name__=='__main__':verify(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent/'proof24.tsv')
