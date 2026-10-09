#!/usr/bin/env python3
"""Merge persisted n=11 exact s5 evidence without recomputing game verdicts.

UNKNOWN replay rows are recorded in the receipt but never enter the cache.
Every key is checked for board bounds, safety, stone count and D4 identity;
conflicting exact results fail before any output is written.
"""
from __future__ import annotations
import argparse
import csv
import glob
import hashlib
import json
from collections import Counter
from pathlib import Path
from derive_shared_s6_witness_cache import canonical_safe_key
from s5_evidence_policy import quarantined_cache_keys


def merge(cache_paths, replay_patterns):
    verdict={}
    quarantine=quarantined_cache_keys()
    origin={}
    receipt=[]
    def put(key,value,path):
        if value not in (0,1,2):
            raise SystemExit(f"bad verdict {value}: {path}")
        canonical=canonical_safe_key(key,5)
        if canonical!=key:
            raise SystemExit(f"noncanonical s5 evidence: {key} in {path}")
        if value==0:
            return
        old=verdict.get(key)
        if old is not None and old!=value:
            raise SystemExit(f"CONFLICT {key}: {old} from {origin[key]} vs {value} from {path}")
        verdict[key]=value
        origin.setdefault(key,str(path))
    replay_paths=[]
    for pattern in replay_patterns:
        found=glob.glob(pattern,recursive=True)
        if not found:
            raise SystemExit(f"no replay files matching {pattern}")
        replay_paths.extend(found)
    for path,is_replay in [(p,False) for p in cache_paths]+[(Path(p),True) for p in sorted(set(replay_paths))]:
        hist=Counter()
        excluded=0
        nodes=0
        keys=set()
        with path.open(newline="",encoding="utf-8") as fp:
            for row in csv.reader(fp):
                if not row or row[0].startswith("#"):
                    continue
                if is_replay:
                    if row[0]!="replay" or len(row)!=11 or int(row[2])!=5 or int(row[4])!=0:
                        raise SystemExit(f"not an s5 AND replay row: {path}: {row}")
                    key=(int(row[9]),int(row[10])); value=int(row[6]); nodes+=int(row[7])
                else:
                    if row[0]!="s5verdict" or len(row)!=6 or int(row[3])!=5 or int(row[4]) not in (1,2):
                        raise SystemExit(f"not an exact s5 cache row: {path}: {row}")
                    key=(int(row[1]),int(row[2])); value=int(row[4])
                    if key in quarantine:
                        excluded+=1
                        continue
                put(key,value,path)
                if key in keys:
                    raise SystemExit(f"duplicate row {key}: {path}")
                keys.add(key); hist[value]+=1
        receipt.append({"path":path.as_posix(),"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"rows":len(keys),"counts":dict(sorted(hist.items())),"nodes":nodes,"quarantined_cache_rows":excluded})
    hist=Counter(verdict.values())
    return verdict,{"unique_exact_s5":len(verdict),"win":hist[1],"loss":hist[2],"conflicts":0,"sources":receipt}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--cache",type=Path,action="append",default=[])
    ap.add_argument("--replay",action="append",default=[])
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--summary-out",type=Path,required=True)
    args=ap.parse_args()
    if not args.cache and not args.replay:
        raise SystemExit("no evidence sources")
    verdict,summary=merge(args.cache,args.replay)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text("# s5 verdict cache: n=11 schema=1 (merged exact evidence; see receipt)\n"+"".join(f"s5verdict,{lo},{hi},5,{v},0\n" for (lo,hi),v in sorted(verdict.items())),encoding="utf-8")
    args.summary_out.parent.mkdir(parents=True,exist_ok=True)
    args.summary_out.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(f"EXACT_S5_MERGE_OK unique={summary['unique_exact_s5']} WIN={summary['win']} LOSS={summary['loss']}")


if __name__=="__main__":
    main()
