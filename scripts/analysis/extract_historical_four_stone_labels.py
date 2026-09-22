#!/usr/bin/env python3
"""Audit historical 4-stone outcome labels reachable from a frozen git commit.

This deliberately walks commits and their trees, rather than only the current
checkout or `git rev-list --objects`, so every detected label retains exact
(commit, path, blob) provenance. Blob contents are parsed once per blob SHA.

The extractor is conservative: it only accepts explicit 4-point states paired
with an explicit WIN/LOSS token in CSV or JSON/text-like records. Ambiguous
content is counted but not silently promoted to a known label.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import subprocess
from collections import defaultdict

STATE_RE = re.compile(r"(?<!\d)(\d{1,2})\s*,\s*(\d{1,2})\s*,\s*(\d{1,2})\s*,\s*(\d{1,2})(?!\d)")
OUTCOME_RE = re.compile(r"\b(WIN|LOSS)\b", re.I)
TEXT_EXT = {'.csv','.json','.jsonl','.md','.txt','.log','.tsv'}


def git(*args: str, binary: bool = False):
    p = subprocess.run(['git', *args], check=True, stdout=subprocess.PIPE)
    return p.stdout if binary else p.stdout.decode('utf-8', errors='strict')


def canonical(st):
    pts = tuple(sorted(st))
    best = None
    for t in range(8):
        q=[]
        for p in pts:
            x,y=p%10,p//10
            if t==0: a,b=x,y
            elif t==1: a,b=9-y,x
            elif t==2: a,b=9-x,9-y
            elif t==3: a,b=y,9-x
            elif t==4: a,b=9-x,y
            elif t==5: a,b=x,9-y
            elif t==6: a,b=y,x
            else: a,b=9-y,9-x
            q.append(b*10+a)
        z=tuple(sorted(q))
        best=z if best is None or z<best else best
    return ','.join(map(str,best))


def valid_state(xs):
    return len(set(xs))==4 and all(0 <= x < 100 for x in xs)


def parse_csv(text):
    out=[]
    try: rows=list(csv.DictReader(io.StringIO(text)))
    except csv.Error: return out
    for i,r in enumerate(rows,2):
        keys={str(k).lower():k for k in r if k is not None}
        sk=next((keys[k] for k in ('state','position','stones') if k in keys),None)
        ok=next((keys[k] for k in ('outcome','result','label') if k in keys),None)
        if sk is None or ok is None: continue
        m=STATE_RE.fullmatch((r.get(sk) or '').strip())
        val=(r.get(ok) or '').strip().upper()
        if m and val in {'WIN','LOSS'}:
            xs=tuple(map(int,m.groups()))
            if valid_state(xs): out.append((canonical(xs),val,f'row:{i}'))
    return out


def parse_lines(text):
    out=[]
    for i,line in enumerate(text.splitlines(),1):
        ms=list(STATE_RE.finditer(line)); os=list(OUTCOME_RE.finditer(line))
        if len(ms)==1 and len(os)==1:
            xs=tuple(map(int,ms[0].groups()))
            if valid_state(xs): out.append((canonical(xs),os[0].group(1).upper(),f'line:{i}'))
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('base', help='full frozen base commit SHA')
    ap.add_argument('--json-out')
    a=ap.parse_args()
    commits=git('rev-list',a.base).splitlines()
    blob_prov=defaultdict(list)
    for c in commits:
        raw=git('ls-tree','-r','-z',c,binary=True)
        for rec in raw.split(b'\0'):
            if not rec: continue
            meta,path=rec.split(b'\t',1); mode,typ,sha=meta.decode().split()
            if typ=='blob': blob_prov[sha].append((c,path.decode('utf-8','surrogateescape')))
    labels=defaultdict(lambda: {'WIN':[], 'LOSS':[]})
    stats={'commits':len(commits),'unique_blobs':len(blob_prov),'text_blobs':0,'decoded_blobs':0,'skipped_binary_or_nontext':0,'ambiguous_decode':0}
    parsed_cache={}
    for sha,prov in blob_prov.items():
        paths=[p for _,p in prov]
        if not any('.'+p.rsplit('.',1)[-1].lower() in TEXT_EXT for p in paths if '.' in p):
            stats['skipped_binary_or_nontext']+=1; continue
        stats['text_blobs']+=1
        data=git('cat-file','blob',sha,binary=True)
        try: text=data.decode('utf-8')
        except UnicodeDecodeError:
            stats['ambiguous_decode']+=1; continue
        stats['decoded_blobs']+=1
        parsed=parse_csv(text) if any(p.lower().endswith(('.csv','.tsv')) for p in paths) else parse_lines(text)
        parsed_cache[sha]=parsed
        for key,outcome,loc in parsed:
            for c,p in prov: labels[key][outcome].append({'commit':c,'path':p,'blob':sha,'location':loc})
    conflicts={k:v for k,v in labels.items() if v['WIN'] and v['LOSS']}
    report={'base':a.base,'stats':stats,'canonical_keys':len(labels),'conflict_keys':len(conflicts),'labels':dict(labels),'conflicts':conflicts}
    print(json.dumps({k:v for k,v in report.items() if k not in {'labels','conflicts'}},indent=2))
    if conflicts: print(f'WARNING: {len(conflicts)} canonical keys have both WIN and LOSS', flush=True)
    if a.json_out:
        with open(a.json_out,'w',encoding='utf-8') as f: json.dump(report,f,ensure_ascii=False,indent=2,sort_keys=True)

if __name__=='__main__': main()
