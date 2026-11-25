#!/usr/bin/env python3
"""Chronological Expected-Work evaluation for exact n=11 s5 scheduling.

Train on the first 80% of the original reply=27 frontier sequence and evaluate
on the final 20%.  Two models are fit from structural features:

- balanced logistic score for P(WIN)-ranking;
- ridge regression for log(exact nodes).

The Expected-Work score is
    win_logit - predicted_log_nodes,
which is the log of odds/cost up to an additive prior constant.  This script is
only a scheduler evaluation; no predicted value is proof evidence.
"""
from __future__ import annotations

import argparse,csv,json,math,re
from pathlib import Path
import numpy as np
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import evaluate_s5_win_model as W  # noqa:E402
import evaluate_s5_cost_model as C  # noqa:E402


def load_rows(features:Path,replay_dir:Path):
    feat={}
    with features.open(newline="",encoding="utf-8") as fp:
        for r in csv.DictReader(fp):
            k=(int(r["lo"]),int(r["hi"]))
            feat[k]=np.array([float(r[c]) for c in W.FEATURES],dtype=float)

    seq={}
    for p in replay_dir.rglob("*.csv"):
        if re.fullmatch(r"reply27-\d+\.csv",p.name) is None:
            continue
        with p.open(newline="",encoding="utf-8") as fp:
            for r in csv.reader(fp):
                if not r or r[0].startswith("#"): continue
                if not r[0].startswith("reply27-"): continue
                n=int(r[1]); k=(int(r[3]),int(r[4]))
                old=seq.get(k)
                if old is not None and old!=n:
                    raise SystemExit(f"seq conflict {k}: {old} vs {n}")
                seq[k]=n

    exact={}
    for p in replay_dir.rglob("*.out"):
        with p.open(newline="",encoding="utf-8") as fp:
            for r in csv.reader(fp):
                if not r or r[0]!="replay": continue
                v=int(r[6]); nodes=int(r[7]); k=(int(r[9]),int(r[10]))
                if v not in (1,2): continue
                old=exact.get(k)
                val=(1 if v==1 else 0,nodes)
                if old is not None and old!=val:
                    raise SystemExit(f"replay conflict {k}: {old} vs {val}")
                exact[k]=val

    rows=[]
    for k,(y,nodes) in exact.items():
        if k in feat and k in seq:
            rows.append((seq[k],k,y,nodes,feat[k]))
    rows.sort(key=lambda r:r[0])
    return rows


def policy_stats(rows,order):
    total_win=sum(r[2] for r in rows)
    cum_nodes=0
    wins=0
    first=None
    milestones={}
    top={}
    for rank,i in enumerate(order,1):
        r=rows[i]
        cum_nodes+=r[3]
        wins+=r[2]
        if r[2] and first is None:
            first={"rank":rank,"nodes":cum_nodes}
        for target in (1,3,5,10):
            if wins>=target and str(target) not in milestones:
                milestones[str(target)]={"rank":rank,"nodes":cum_nodes}
        if rank in (10,20,40,80,160):
            top[str(rank)]={
                "roots":rank,
                "wins":wins,
                "nodes":cum_nodes,
                "wins_per_million_nodes":wins/(cum_nodes/1e6) if cum_nodes else 0.0,
            }
    return {
        "total_roots":len(rows),
        "total_wins":total_win,
        "first_win":first,
        "win_milestones":milestones,
        "top_prefix":top,
        "all_nodes":cum_nodes,
    }


def auc(y,score):
    return W.auc(y,score)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--features",type=Path,required=True)
    ap.add_argument("--replay-dir",type=Path,required=True)
    ap.add_argument("--out",type=Path)
    args=ap.parse_args()

    rows=load_rows(args.features,args.replay_dir)
    if len(rows)<1000:
        raise SystemExit(f"too few rows {len(rows)}")
    maxseq=max(r[0] for r in rows)
    cutoff=int(math.floor(0.8*(maxseq+1)))
    tr=[r for r in rows if r[0]<cutoff]
    te=[r for r in rows if r[0]>=cutoff]
    X=np.stack([r[4] for r in tr])
    y=np.array([r[2] for r in tr],dtype=int)
    logn=np.log(np.array([r[3] for r in tr],dtype=float))
    Xt=np.stack([r[4] for r in te])
    yt=np.array([r[2] for r in te],dtype=int)

    # Balanced WIN ranking model.
    ww,wmean,wsd=W.fit_logistic(X,y)
    win_score=W.score_model(Xt,ww,wmean,wsd)

    # Structural exact-cost model.
    cw,cmean,csd=C.fit_linear(X,logn,lam=1.0)
    pred_log_nodes=C.predict(Xt,cw,cmean,csd)

    legal_j=W.FEATURES.index("legal")
    legal=Xt[:,legal_j]
    ew=win_score-pred_log_nodes

    policies={
        "legal_low":np.lexsort((np.arange(len(te)),legal)),
        "predicted_cost_low":np.argsort(pred_log_nodes,kind="stable"),
        "win_score_high":np.argsort(-win_score,kind="stable"),
        "expected_work_odds_per_cost":np.argsort(-ew,kind="stable"),
    }
    actual_nodes=np.array([r[3] for r in te],dtype=float)
    oracle_ew=np.where(yt==1,1.0/actual_nodes,0.0)

    out={
        "split":{
            "joined_exact":len(rows),"cutoff_global_seq":cutoff,
            "train":len(tr),"train_win":int(y.sum()),
            "holdout":len(te),"holdout_win":int(yt.sum()),
            "holdout_loss":int(len(yt)-yt.sum()),
        },
        "ranking_quality":{
            "legal_low_auc_for_win":auc(yt,-legal),
            "structural_win_auc":auc(yt,win_score),
            "cost_corr_log_nodes":float(np.corrcoef(np.log(actual_nodes),pred_log_nodes)[0,1]),
        },
        "policies":{
            name:policy_stats(te,order)
            for name,order in policies.items()
        },
        "oracle_reference":{
            "actual_win_per_node_order":policy_stats(te,np.argsort(-oracle_ew,kind="stable"))
        },
        "definition":{
            "expected_work_score":"balanced_WIN_logit - predicted_log_exact_nodes",
            "interpretation":"ranking equivalent to estimated WIN odds per unit solve cost up to a prior constant",
        },
        "claim":"scheduler evaluation only; exact replay remains the sole verdict source",
    }
    text=json.dumps(out,indent=2,sort_keys=True)+"\n"
    print(text,end="")
    print("S5_EXPECTED_WORK_EVAL_OK")
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(text,encoding="utf-8")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
