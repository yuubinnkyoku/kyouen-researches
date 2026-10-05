#!/usr/bin/env python3
"""Validate reply-27 exact-replay outputs and classify the selected s4 classes.

Only completed replay rows (result WIN/LOSS) are exported to the s5 verdict
cache. UNKNOWN rows remain unresolved.  The selected s4 class is WIN if any
canonical s5 child is WIN, LOSS if every canonical s5 child is LOSS, otherwise
UNKNOWN.  This is the exact OR-node recurrence at four stones.
"""
from __future__ import annotations
import argparse, csv, json, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EDGE_DIR = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE_DIR))
from dfpn_edge_classes import d4_canonical_key, legal_after  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
WITNESS = HERE / "output/reply27-direct-union-cover.json"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("replay", nargs="+", type=Path)
    ap.add_argument("--cache-out", type=Path)
    ap.add_argument("--summary-out", type=Path)
    args=ap.parse_args()
    doc=json.loads(WITNESS.read_text(encoding="utf-8"))
    first,r2=doc["root"]; selected=[tuple(x) for x in doc["classes"]]
    base={first,r2}; groups=defaultdict(list)
    for a in legal_after(base):
        for b in legal_after(base|{a}):
            if b<=a: continue
            k=d4_canonical_key([first,r2,a,b])
            if k in selected: groups[k].append((a,b))
    assert set(groups)==set(selected)
    children={}
    for k in selected:
        ss=set()
        for a,b in groups[k]:
            occ=base|{a,b}
            for z in legal_after(occ):
                ss.add(d4_canonical_key(list(occ|{z})))
        children[k]=ss

    verdict={}; conflicts=[]
    for p in args.replay:
        with p.open(newline="",encoding="utf-8") as fp:
            for row in csv.reader(fp):
                if not row or row[0]!="replay": continue
                result=int(row[6])
                if result not in (1,2): continue
                key=(int(row[9]),int(row[10]))
                old=verdict.get(key)
                if old is not None and old!=result: conflicts.append((key,old,result))
                verdict[key]=result
    assert not conflicts, conflicts

    status={}; unresolved={}
    for k in selected:
        vals=[verdict.get(x,0) for x in children[k]]
        if 1 in vals: status[k]="WIN"
        elif vals and all(v==2 for v in vals): status[k]="LOSS"
        else:
            status[k]="UNKNOWN"
            unresolved[k]=sum(v==0 for v in vals)

    counts={s:sum(v==s for v in status.values()) for s in ("WIN","LOSS","UNKNOWN")}
    out={
        "completed_s5_verdicts":len(verdict),
        "s5_win":sum(v==1 for v in verdict.values()),
        "s5_loss":sum(v==2 for v in verdict.values()),
        "selected_s4_status_counts":counts,
        "selected_s4_loss":[list(k) for k,v in status.items() if v=="LOSS"],
        "selected_s4_win":[list(k) for k,v in status.items() if v=="WIN"],
        "unknown_children_by_s4":{"%d:%d"%k:n for k,n in unresolved.items()},
    }
    txt=json.dumps(out,indent=2,sort_keys=True)+"\n"
    print(txt,end="")
    if args.summary_out:
        args.summary_out.parent.mkdir(parents=True,exist_ok=True)
        args.summary_out.write_text(txt,encoding="utf-8")
    if args.cache_out:
        args.cache_out.parent.mkdir(parents=True,exist_ok=True)
        with args.cache_out.open("w",encoding="utf-8") as fp:
            fp.write("# s5 verdict cache: n=11 schema=1 (canonical key -> WIN/LOSS, UNKNOWN never stored)\n")
            for (lo,hi),v in sorted(verdict.items()):
                fp.write(f"s5verdict,{lo},{hi},5,{v},0\n")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
