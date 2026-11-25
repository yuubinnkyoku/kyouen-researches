#!/usr/bin/env python3
"""Summarize exact-replay shards for the 2,262 reply-27 s5 targets.

Only result 1/2 is treated as a proved verdict. result 0 remains UNKNOWN.
The script rejects duplicate canonical roots with conflicting proved verdicts.
"""
import argparse,csv,glob,json
from collections import Counter

ap=argparse.ArgumentParser()
ap.add_argument("patterns",nargs="+")
ap.add_argument("--unknown-out")
args=ap.parse_args()
paths=[]
for pat in args.patterns: paths += glob.glob(pat)
assert paths, "no shard outputs"
seen={}
unknown=[]
hist=Counter()
nodes=Counter()
for path in sorted(set(paths)):
    with open(path,newline="") as f:
        for r in csv.reader(f):
            if not r or r[0]!="replay": continue
            # replay,id,stones,legal,is_or,budget,result,nodes,wall_s,key_lo,key_hi
            key=(int(r[9]),int(r[10]))
            result=int(r[6]); n=int(r[7])
            hist[result]+=1; nodes[result]+=n
            if result in (1,2):
                old=seen.get(key)
                if old is not None and old!=result:
                    raise SystemExit(f"CONFLICT key={key} old={old} new={result}")
                seen[key]=result
            else:
                unknown.append(r)
if args.unknown_out:
    with open(args.unknown_out,"w",newline="") as f:
        csv.writer(f).writerows(unknown)
out={"rows":sum(hist.values()),"unique_proved":len(seen),
     "result_counts":{"UNKNOWN":hist[0],"WIN":hist[1],"LOSS":hist[2]},
     "node_counts":{"UNKNOWN":nodes[0],"WIN":nodes[1],"LOSS":nodes[2]},
     "unknown_rows":len(unknown),"conflicts":0}
print(json.dumps(out,indent=2,sort_keys=True))
print("REPLY27_EXACT_SHARDS_SUMMARY_OK")
