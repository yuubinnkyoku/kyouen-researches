#!/usr/bin/env python3
"""Choose reply=27 s5 probes using the chronological structural WIN model.

The model is trained only on the original exact reply27 frontier.  Candidate
roots are current UNKNOWN s5 children of the current repair classes.  Model
scores are used only for scheduling: no predicted verdict is ever promoted to
proof evidence.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import evaluate_s5_win_model as M  # noqa: E402


def load_feature_rows(path:Path):
    out={}
    with path.open(newline="",encoding="utf-8") as fp:
        for r in csv.DictReader(fp):
            key=(int(r["lo"]),int(r["hi"]))
            out[key]={
                "legal":int(r["legal"]),
                "x":np.array([float(r[c]) for c in M.FEATURES],dtype=float),
            }
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train",type=Path,required=True)
    ap.add_argument("--candidates",type=Path,required=True)
    ap.add_argument("--class-map",type=Path,required=True)
    ap.add_argument("--per-class",type=int,default=1)
    ap.add_argument("--out",type=Path)
    ap.add_argument("--probes-out",type=Path)
    args=ap.parse_args()
    if args.per_class<1:
        raise SystemExit("--per-class must be >=1")

    tr=M.load(args.train)
    X=np.stack([v[1] for v in tr.values()])
    y=np.array([v[0] for v in tr.values()],dtype=int)
    w,mean,sd=M.fit_logistic(X,y)

    cand=load_feature_rows(args.candidates)
    cmap=json.loads(args.class_map.read_text(encoding="utf-8"))
    keys=sorted(cand)
    Xt=np.stack([cand[k]["x"] for k in keys])
    score=M.score_model(Xt,w,mean,sd)
    scored={k:float(score[i]) for i,k in enumerate(keys)}

    selected=[]
    seen=set()
    classes=[]
    for row in cmap["classes"]:
        ck=tuple(row["key"])
        children=[tuple(ch) for ch in row["unknown_children"]]
        ranked=sorted(
            children,
            key=lambda k:(-scored[k],cand[k]["legal"],k[1],k[0]),
        )
        chosen=[]
        for k in ranked[:args.per_class]:
            chosen.append({
                "key":list(k),
                "score":scored[k],
                "legal":cand[k]["legal"],
            })
            if k not in seen:
                seen.add(k)
                selected.append(k)
        classes.append({
            "key":list(ck),
            "unknown_s5":len(children),
            "top_score":scored[ranked[0]] if ranked else None,
            "top_legal":cand[ranked[0]]["legal"] if ranked else None,
            "chosen":chosen,
        })

    # Most WIN-like predicted roots first.  Exact solver verdicts remain the
    # only source of truth.
    selected.sort(key=lambda k:(-scored[k],cand[k]["legal"],k[1],k[0]))
    result={
        "train_unique":len(tr),
        "train_win":int(y.sum()),
        "train_loss":int(len(y)-y.sum()),
        "repair_classes":len(classes),
        "per_class":args.per_class,
        "dedup_probes":len(selected),
        "classes":sorted(
            classes,
            key=lambda r:(-(r["top_score"] if r["top_score"] is not None else -1e300),
                          r["key"]),
        ),
        "claim":"scheduling only; model scores are not verdicts",
    }
    text=json.dumps(result,indent=2,sort_keys=True)+"\n"
    print(text,end="")
    print("REPLY27_MODEL_PROBES_OK")

    if args.probes_out:
        args.probes_out.parent.mkdir(parents=True,exist_ok=True)
        with args.probes_out.open("w",encoding="utf-8") as fp:
            for seq,k in enumerate(selected):
                fp.write(
                    f"reply27-model-probe,{seq},5,{k[0]},{k[1]},"
                    f"{cand[k]['legal']},0,0,0,0,0\n"
                )
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(text,encoding="utf-8")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
