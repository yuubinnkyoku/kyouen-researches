#!/usr/bin/env python3
"""Fail-closed, atomic merge of canonical S10 WIN/LOSS worker shards."""
import argparse
import os
import pathlib
import tempfile
import sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from fifth_verify_standalone import canonical,safe


def read_shard(path, *, geometry=False):
    entries={}
    with open(path,encoding='utf-8') as f:
        for i,line in enumerate(f,1):
            cols=line.strip().split()
            if len(cols)!=2:raise ValueError(f'{path}:{i}: expected two columns')
            key,verdict=cols
            if len(key)!=32 or any(c not in '0123456789abcdef' for c in key):
                raise ValueError(f'{path}:{i}: invalid canonical hex mask')
            if verdict not in ('WIN','LOSS'):
                raise ValueError(f'{path}:{i}: invalid verdict')
            if key in entries:raise ValueError(f'{path}:{i}: duplicate key')
            x=int(key,16)
            if x.bit_count()!=10 or x>>121:
                raise ValueError(f'{path}:{i}: not a ten-stone 11x11 position')
            if geometry and (canonical(x)!=x or not safe(x)):
                raise ValueError(f'{path}:{i}: unsafe/noncanonical position')
            entries[key]=verdict
    return entries


def merge(baseline,shards,output,*,geometry=False):
    dest=pathlib.Path(output)
    if dest.resolve() in {pathlib.Path(x).resolve() for x in [baseline,*shards]}:
        raise ValueError('output cannot overwrite any input')
    combined=read_shard(baseline,geometry=geometry)
    old=len(combined);overlap=0;new=0
    for shard in shards:
        current=read_shard(shard,geometry=geometry)
        for key,verdict in current.items():
            prior=combined.get(key)
            if prior is not None:
                if prior!=verdict:raise ValueError(f'WIN/LOSS CONFLICT key={key} old={prior} new={verdict} shard={shard}')
                overlap+=1
            else:combined[key]=verdict;new+=1
    dest.parent.mkdir(parents=True,exist_ok=True)
    tmp=None
    try:
        with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=dest.parent,prefix='.'+dest.name+'.',suffix='.tmp',delete=False) as f:
            tmp=pathlib.Path(f.name)
            for key,verdict in sorted(combined.items()):f.write(f'{key}\t{verdict}\n')
            f.flush();os.fsync(f.fileno())
        os.replace(tmp,dest)
        # Best-effort directory durability on POSIX.
        if hasattr(os,'O_DIRECTORY'):
            fd=os.open(dest.parent,os.O_RDONLY|os.O_DIRECTORY)
            try:os.fsync(fd)
            finally:os.close(fd)
    finally:
        if tmp is not None and tmp.exists():tmp.unlink()
    return dict(old=old,new=new,overlap=overlap,total=len(combined))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('baseline');p.add_argument('output');p.add_argument('shards',nargs='+')
    p.add_argument('--geometry',action='store_true',help='independently check S10 geometry and D4 canonicality')
    a=p.parse_args()
    print(merge(a.baseline,a.shards,a.output,geometry=a.geometry))
