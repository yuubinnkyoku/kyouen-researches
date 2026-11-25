#!/usr/bin/env python3
"""Train on the original reply27 exact frontier and test on later probes.

This is deliberately chronological, not random cross-validation:
  train = full 2262 replay + hard9 boundary exact cache
  test  = exact s5 verdicts learned later by adaptive/repair experiments,
          excluding any key already present in train.

The target is verdict==1 (a class-disqualifying WIN s5 in the current proof
convention).  The purpose is ranking future probes, not calibrated probability.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

FEATURES = [
    "legal","e2","e3","e4","components","isolated","max_component",
    "max_degree","max_d2","max_d3","max_d4","sum_degree","pair_max_degree",
    "occ_sum_d2","occ_min_d2","occ_max_d2","occ_radius2_sum",
]


def load(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        rows=list(csv.DictReader(f))
    out={}
    for r in rows:
        k=(int(r["lo"]),int(r["hi"]))
        y=1 if int(r["verdict"])==1 else 0
        x=np.array([float(r[c]) for c in FEATURES],dtype=float)
        old=out.get(k)
        if old is not None and old[0]!=y:
            raise SystemExit(f"conflicting feature verdict {k}")
        out[k]=(y,x)
    return out


def auc(y,score):
    pos=[i for i,v in enumerate(y) if v==1]
    neg=[i for i,v in enumerate(y) if v==0]
    if not pos or not neg:
        return float("nan")
    total=0.0
    for i in pos:
        for j in neg:
            if score[i]>score[j]: total+=1
            elif score[i]==score[j]: total+=0.5
    return total/(len(pos)*len(neg))


def fit_logistic(X,y):
    mean=X.mean(axis=0)
    sd=X.std(axis=0)
    sd[sd==0]=1.0
    Z=(X-mean)/sd
    npos=max(1,int(y.sum())); nneg=max(1,len(y)-npos)
    weights=np.where(y==1,0.5/npos,0.5/nneg)
    lam=0.5

    def fg(w):
        z=Z@w[1:]+w[0]
        # stable logistic loss
        loss=np.sum(weights*(np.maximum(z,0)-y*z+np.log1p(np.exp(-np.abs(z)))))
        loss += 0.5*lam*np.dot(w[1:],w[1:])
        p=1/(1+np.exp(-np.clip(z,-50,50)))
        d=weights*(p-y)
        grad=np.empty_like(w)
        grad[0]=d.sum()
        grad[1:]=Z.T@d+lam*w[1:]
        return loss,grad

    w0=np.zeros(X.shape[1]+1)
    res=minimize(lambda w: fg(w)[0],w0,jac=lambda w:fg(w)[1],
                 method="L-BFGS-B",options={"maxiter":2000,"ftol":1e-12})
    if not res.success:
        raise SystemExit(f"logistic fit failed: {res.message}")
    return res.x,mean,sd


def score_model(X,w,mean,sd):
    Z=(X-mean)/sd
    return Z@w[1:]+w[0]


def enrichment(y,score):
    order=np.argsort(-score)
    total_pos=int(y.sum())
    out={}
    for k in (5,10,20,40,80):
        kk=min(k,len(y))
        out[str(k)]={
            "k":kk,
            "win":int(y[order[:kk]].sum()),
            "precision":float(y[order[:kk]].mean()) if kk else 0.0,
            "recall":float(y[order[:kk]].sum()/total_pos) if total_pos else 0.0,
        }
    first=next((rank+1 for rank,i in enumerate(order) if y[i]==1),None)
    out["first_win_rank"]=first
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",type=Path,required=True)
    ap.add_argument("--test",type=Path,required=True)
    ap.add_argument("--out",type=Path)
    args=ap.parse_args()

    tr=load(args.train); te0=load(args.test)
    te={k:v for k,v in te0.items() if k not in tr}
    if not te: raise SystemExit("empty chronological holdout")
    X=np.stack([v[1] for v in tr.values()])
    y=np.array([v[0] for v in tr.values()],dtype=int)
    Xt=np.stack([v[1] for v in te.values()])
    yt=np.array([v[0] for v in te.values()],dtype=int)

    w,mean,sd=fit_logistic(X,y)
    train_score=score_model(X,w,mean,sd)
    test_score=score_model(Xt,w,mean,sd)

    single={}
    for j,name in enumerate(FEATURES):
        a=auc(yt,Xt[:,j])
        single[name]={
            "auc_win_high":a,
            "auc_best_orientation":max(a,1-a) if not math.isnan(a) else a,
            "direction":"high" if a>=0.5 else "low",
        }

    coeff=[
        {"feature":name,"standardized_coefficient":float(w[j+1])}
        for j,name in enumerate(FEATURES)
    ]
    coeff.sort(key=lambda r:-abs(r["standardized_coefficient"]))

    legal_j=FEATURES.index("legal")
    legal_auc=auc(yt,-Xt[:,legal_j])  # current scheduler favours lower legal
    model_auc=auc(yt,test_score)
    base_rate=float(yt.mean())

    result={
        "chronological_split":{
            "train_unique":len(tr),"train_win":int(y.sum()),
            "train_loss":int(len(y)-y.sum()),
            "test_unique_after_train_dedup":len(te),"test_win":int(yt.sum()),
            "test_loss":int(len(yt)-yt.sum()),
        },
        "baseline":{
            "holdout_win_rate":base_rate,
            "low_legal_auc_for_win":legal_auc,
            "low_legal_enrichment":enrichment(yt,-Xt[:,legal_j]),
        },
        "balanced_logistic":{
            "train_auc":auc(y,train_score),
            "holdout_auc":model_auc,
            "holdout_enrichment":enrichment(yt,test_score),
            "coefficients":coeff,
        },
        "single_feature_holdout_auc":single,
        "acceptance_note":(
            "Model is useful only if chronological holdout ranking materially "
            "beats legal-count baseline; training AUC alone is not evidence."
        ),
    }
    text=json.dumps(result,indent=2,sort_keys=True)+"\n"
    print(text,end="")
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(text,encoding="utf-8")


if __name__=="__main__":
    main()
