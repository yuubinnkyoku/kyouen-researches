#!/usr/bin/env python3
"""Conflict-checked atomic merge of independently verified S10 terminal verdicts.

Requires the main repo's tracked 51,571-row S10 cache. Does not modify it;
produces a new file. Full Python terminal proof is rerun before writing.
"""
import argparse
import json
import os
import tempfile
from pathlib import Path
from verify_core import canonical, safe
from verify_gap6_terminal import verify

HERE=Path(__file__).resolve().parent

def parse_cache(text):
    out={}
    for line in text.splitlines():
        if not line.strip(): continue
        fields=line.split()
        if len(fields)<2 or fields[1] not in ('WIN','LOSS'):
            raise ValueError('bad S10 row '+line)
        h,v=fields[:2]
        if len(h)!=32 or any(c not in '0123456789abcdef' for c in h):
            raise ValueError('bad S10 key '+h)
        if h in out: raise ValueError('duplicate S10 key '+h)
        out[h]=v
    return out

def merge(old,new):
    merged=dict(old)
    overlap=0
    for h,v in new.items():
        if h in merged:
            if merged[h]!=v: raise ValueError(f'WIN/LOSS conflict: {h}: {merged[h]} vs {v}')
            overlap+=1
        else: merged[h]=v
    return merged,overlap

def new_verified_rows():
    cert=json.loads((HERE/'gap6-terminal-cert.json').read_text())
    win={h:'WIN' for r in cert['s8_win_roots'] for h in r['s10_win_children']}
    boundary=parse_cache((HERE/'s8-new-all-s10-results.tsv').read_text())
    merged,overlap=merge(win,boundary)
    if len(win)!=337 or len(boundary)!=243 or overlap!=0 or len(merged)!=580:
        raise ValueError('wrong certificate leaf universe')
    for h in merged:
        m=int(h,16)
        if m.bit_count()!=10 or canonical(m)!=m or not safe(m):
            raise ValueError('invalid canonical S10 key '+h)
    return merged

def atomic_write(path, content):
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.'+path.name+'.',suffix='.tmp',dir=path.parent)
    try:
        with os.fdopen(fd,'w',encoding='ascii',newline='\n') as f:
            f.write(content)
            f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('source',type=Path,help='tracked s10_merged_51571.tsv')
    p.add_argument('output',type=Path,help='NEW destination path, not the source')
    a=p.parse_args()
    if a.source.resolve()==a.output.resolve(): raise ValueError('refusing in-place overwrite')
    verify(verbose=False)  # independent Python proof before any write
    old=parse_cache(a.source.read_text())
    if len(old)!=51571: raise ValueError(f'expected 51571 old cache entries, got {len(old)}')
    new=new_verified_rows()
    merged,overlap=merge(old,new)
    if (overlap,len(merged))!=(29,52122):
        raise ValueError(f'unexpected overlap/size {(overlap,len(merged))}')
    payload=''.join(f'{h}\t{v}\n' for h,v in sorted(merged.items()))
    if a.output.exists():raise ValueError('destination already exists; refusing overwrite')
    atomic_write(a.output,payload)
    print(f'PASS old={len(old)} independent={len(new)} overlap={overlap} added={len(new)-overlap} merged={len(merged)} conflicts=0')

if __name__=='__main__':main()
