#!/usr/bin/env python3
"""Evaluate structural prediction of exact n=11 s5 solve cost.

Target: log(exact df-pn nodes).  The split is deterministic by the original
reply27 frontier sequence: first 80% train, last 20% holdout.  UNKNOWN 15M-cap
rows are excluded because their true solve cost is right-censored.

This is a scheduler model only; predicted costs are never proof evidence.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

FEATURES=[
    "legal","e2","e3","e4","components","isolated","max_component",
    "max_degree","max_d2","max_d3","max_d4","sum_degree","pair_max_degree",
    "occ_sum_d2","occ_min_d2","occ_max_d2","occ_radius2_sum",
]


def load_features(path:Path):
    out={}
    with path.open(newline="",encoding="utf-8") as fp:
        for r in csv.DictReader(fp):
            k=(int(r["lo"]),int(r["hi"]))
            out[k]=np.array([float(r[c]) for c in FEATURES],dtype=float)
    return out


def load_replay(root:Path):
    seq={}
    for p in root.rglob("*.csv"):
        try:
            with p.open(newline="",encoding="utf-8") as fp:
                for r in csv.reader(fp):
                    if not r or r[0].startswith("#") or len(r)<5: continue
                    if not r[0].startswith("reply27-"): continue
                    try:
                        n=int(r[1]); k=(int(r[3]),int(r[4]))
                    except ValueError:
                        continue
                    old=seq.get(k)
                    if old is not None and old!=n:
                        raise SystemExit(f"sequence conflict {k}: {old} vs {n}")
                    seq[k]=n
        except UnicodeDecodeError:
            pass

    exact={}
    censored=0
    for p in root.rglob("*.out"):
        with p.open(newline="",encoding="utf-8") as fp:
            for r in csv.reader(fp):
                if not r or r[0]!="replay": continue
                v=int(r[6]); nodes=int(r[7]); k=(int(r[9]),int(r[10]))
                if v==0:
                    censored+=1
                    continue
                if v not in (1,2):
                    continue
                old=exact.get(k)
                val=(v,nodes)
                if old is not None and old!=val:
                    raise SystemExit(f"replay conflict {k}: {old} vs {val}")
                exact[k]=val
    return seq,exact,censored


def metrics(y,p):
    err=p-y
    ae=np.abs(err)
    corr=float(np.corrcoef(y,p)[0,1]) if len(y)>1 else float("nan")
    return {
        "n":int(len(y)),
        "corr_log_nodes":corr,
        "rmse_log":float(np.sqrt(np.mean(err*err))),
        "mae_log":float(np.mean(ae)),
        "median_abs_log":float(np.median(ae)),
        "mean_multiplicative_error":float(np.exp(np.mean(ae))),
        "median_multiplicative_error":float(np.exp(np.median(ae))),
    }


def fit_linear(X,y,lam=1.0):
    mean=X.mean(axis=0)
    sd=X.std(axis=0); sd[sd==0]=1.0
    Z=(X-mean)/sd
    A=np.column_stack([np.ones(len(Z)),Z])
    reg=np.eye(A.shape[1])*lam
    reg[0,0]=0
    w=np.linalg.solve(A.T@A+reg,A.T@y)
    return w,mean,sd


def predict(X,w,mean,sd):
    Z=(X-mean)/sd
    return w[0]+Z@w[1:]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--features",type=Path,required=True)
    ap.add_argument("--replay-dir",type=Path,required=True)
    ap.add_argument("--out",type=Path)
    args=ap.parse_args()

    feat=load_features(args.features)
    seq,exact,censored=load_replay(args.replay_dir)
    keys=sorted(k for k in exact if k in feat and k in seq)
    if len(keys)<1000:
        raise SystemExit(f"too few joined rows: {len(keys)}")

    rows=sorted(
        [(seq[k],k,exact[k][0],exact[k][1],feat[k]) for k in keys],
        key=lambda r:r[0],
    )
    cutoff=int(math.floor(0.8*(max(r[0] for r in rows)+1)))
    tr=[r for r in rows if r[0]<cutoff]
    te=[r for r in rows if r[0]>=cutoff]
    if not tr or not te:
        raise SystemExit("empty split")

    X=np.stack([r[4] for r in tr]); y=np.log(np.array([r[3] for r in tr],dtype=float))
    Xt=np.stack([r[4] for r in te]); yt=np.log(np.array([r[3] for r in te],dtype=float))

    # Structural ridge model.
    w,mean,sd=fit_linear(X,y,lam=1.0)
    p=predict(Xt,w,mean,sd)

    # Legal-only OLS baseline.
    j=FEATURES.index("legal")
    xl=X[:,j]
    xb=np.column_stack([np.ones(len(xl)),xl])
    wb=np.linalg.lstsq(xb,y,rcond=None)[0]
    pb=wb[0]+wb[1]*Xt[:,j]

    coeff=[
        {"feature":name,"standardized_coefficient":float(w[i+1])}
        for i,name in enumerate(FEATURES)
    ]
    coeff.sort(key=lambda r:-abs(r["standardized_coefficient"]))

    out={
        "joined_exact_rows":len(rows),
        "censored_unknown_rows_seen":censored,
        "split":{
            "cutoff_global_seq":cutoff,
            "train":len(tr),"holdout":len(te),
            "train_seq_min":min(r[0] for r in tr),
            "train_seq_max":max(r[0] for r in tr),
            "holdout_seq_min":min(r[0] for r in te),
            "holdout_seq_max":max(r[0] for r in te),
        },
        "legal_only":{
            "intercept":float(wb[0]),"slope":float(wb[1]),
            "holdout":metrics(yt,pb),
        },
        "structural_ridge":{
            "lambda":1.0,
            "holdout":metrics(yt,p),
            "coefficients":coeff,
        },
        "claim":"scheduler cost model only; predictions are not proof evidence",
    }
    text=json.dumps(out,indent=2,sort_keys=True)+"\n"
    print(text,end="")
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(text,encoding="utf-8")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
