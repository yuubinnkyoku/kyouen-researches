"""Audit untracked local raw separately; preserve byte copies of new exact support.

Only .local/n11 is accepted as the board/rule scope. Original files are retained.
"""
import csv
import json
import shutil
from collections import Counter
from independent import Board,mask_from_key
from audit import ROOT,EXP,OUT,dump,digest,key

def main():
    missing={a+(b<<64) for r in json.loads((OUT/'cache-only-claims.json').read_text()) for a,b in [r['key']]}
    banned={a+(b<<64) for r in json.loads((ROOT/'results/n11-s5-evidence-quarantine.json').read_text())['entries'] if r['active'] for a,b in [r['key']]}
    board=Board(11)
    sources, hits, recovered, observed = [],[],{},Counter()
    files=sorted((ROOT/'.local/n11').rglob('*.csv'))
    for p in files:
        observations=[]
        with p.open(encoding='utf-8-sig',newline='') as f:
            for line,r in enumerate(csv.reader(f),1):
                if not r or r[0]!='replay' or len(r)!=11 or int(r[2])!=5 or int(r[5])<=0:
                    continue
                mask=mask_from_key(int(r[9]),int(r[10]))
                mask=board.canonical(mask)
                if mask not in missing|banned:
                    continue
                if mask.bit_count()!=5 or board.legal(mask).bit_count()!=int(r[3]) or int(r[4])!=0:
                    raise ValueError(('bad local raw',p,line))
                v=int(r[6]); assert v in (0,1,2)
                observations.append(dict(key=key(mask),row=line,verdict=v,budget=int(r[5])))
                observed[v]+=1
                if mask in banned:
                    hits.append(dict(path=p.relative_to(ROOT).as_posix(),sha256=digest(p),row=line,key=key(mask),verdict=v))
                if mask in missing and v:
                    target=EXP/'input/recovered-raw'/f'{digest(p)}.csv'
                    target.parent.mkdir(parents=True,exist_ok=True)
                    if not target.exists(): shutil.copyfile(p,target)
                    assert digest(p)==digest(target)
                    recovered[mask]=v
                    sources.append(dict(path=target.relative_to(ROOT).as_posix(),original_path=p.relative_to(ROOT).as_posix(),sha256=digest(p)))
        if observations:
            print(p.name,observations[:2],flush=True)
    dump('local-recovery.json',dict(scanned_csv=len(files),quarantined_observations=hits,
        newly_supported_s5=len(recovered),sources=list({r['path']:r for r in sources}.values()),verdict_counts=dict(observed)))

if __name__=='__main__': main()
