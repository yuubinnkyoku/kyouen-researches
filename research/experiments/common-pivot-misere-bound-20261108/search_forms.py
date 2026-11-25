#!/usr/bin/env python3
"""Bounded graph sums/joins; a miss is not a bound or nonexistence proof."""
from functools import lru_cache
import argparse
import json
from pathlib import Path

OPTIONS=[];VALUES=[];INTERN={};LIMIT=300000


def mex(values):
    answer=0
    while answer in values:answer+=1
    return answer


def form(options):
    key=tuple(sorted(set(options)))
    if key in INTERN:return INTERN[key]
    if len(OPTIONS)>=LIMIT:raise RuntimeError('bounded form limit')
    identifier=len(OPTIONS);INTERN[key]=identifier;OPTIONS.append(key)
    g=mex({VALUES[x][0] for x in key})
    h=mex({VALUES[x][1] for x in key}) if key else 1
    t=mex({VALUES[x][2] for x in key if VALUES[x][1]<2}) if h<2 else None
    VALUES.append((g,h,t,2+t if h==1 else 1,2+t if h==0 else 0))
    return identifier


@lru_cache(None)
def add(a,b):
    if a>b:return add(b,a)
    if a==0:return b
    return form([add(x,b) for x in OPTIONS[a]]+[add(a,y) for y in OPTIONS[b]])


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--with-petersen',action='store_true')
    args=parser.parse_args()
    zero=form([]);star=form([zero]);two=form([zero,star]);wild=form([two])
    cores=[(star,1,'free'),(two,3,'P3'),(wild,6,'C6')]
    best={zero:(0,'empty'),star:(1,'free'),two:(3,'P3'),wild:(6,'C6')}
    if args.with_petersen:
        petersen=form([wild]);cores.append((petersen,10,'Petersen'));best[petersen]=(10,'Petersen')
    frontier=list(best);history=[];limit_reached=False
    try:
        for depth in range(1,10):
            candidates=set()
            for current in frontier:
                n,expression=best[current]
                for other,size,name in cores:
                    for operation in ('sum','join'):
                        identifier=add(current,other) if operation=='sum' else form(OPTIONS[current]+OPTIONS[other])
                        if n+size>50:continue
                        if identifier not in best or n+size<best[identifier][0]:
                            best[identifier]=(n+size,[operation,expression,name]);candidates.add(identifier)
            # Keep representatives across all low h and g classes, favoring large t/F.
            grouped={}
            for identifier in candidates:
                g,h,t,f0,f1=VALUES[identifier]
                grouped.setdefault((min(g,10),min(h,10)),[]).append(identifier)
            frontier=[]
            for group in grouped.values():
                frontier.extend(sorted(group,key=lambda x:(max(VALUES[x][3:]),-best[x][0]),reverse=True)[:40])
            leaders=sorted(best,key=lambda x:(max(VALUES[x][3:]),-best[x][0]),reverse=True)[:10]
            row=dict(depth=depth,root_forms=len(best),internal_forms=len(OPTIONS),frontier=len(frontier),
                     highest_poison_transform=max(max(VALUES[x][3:]) for x in best))
            history.append(row);print(row,flush=True)
            if row['highest_poison_transform']>=10:break
    except RuntimeError as error:
        if str(error)!='bounded form limit':raise
        limit_reached=True
    leaders=sorted(best,key=lambda x:(max(VALUES[x][3:]),-best[x][0]),reverse=True)[:20]
    output=dict(scope='bounded sums and joins of the stated graph cores; no exhaustive graph claim',
                cores=[name for identifier,size,name in cores],
                history=history,internal_form_limit=LIMIT,form_limit_reached=limit_reached,
                leaders=[dict(vertices=best[x][0],expression=best[x][1],
                              normal=VALUES[x][0],misere_aux=VALUES[x][1],restricted=VALUES[x][2],
                              poison_even=VALUES[x][3],poison_odd=VALUES[x][4]) for x in leaders])
    target=Path(__file__).with_name('output')/('form_search_petersen.json' if args.with_petersen else 'form_search.json')
    target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output['leaders'][:2],indent=2),flush=True)


if __name__=='__main__':main()
