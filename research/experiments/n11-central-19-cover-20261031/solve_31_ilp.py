#!/usr/bin/env python3
"""Constrained 31-class cover search for the four unrepaired central n11 roots.

A feasible result is a geometric certificate plan, NOT a proof of S4 LOSS.
The script pins saved solver-trusted S5 verdicts and never infers a game winner.
"""
import argparse
import base64
import gzip
import hashlib
import json
from itertools import combinations
from pathlib import Path
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCES = [
    ("research/experiments/n11-s4-boundary-direct-20261012/output/current-exact-s5.cache",
     "2dccf42b92337cbcbfb62ea5c77db487b1ad8ead"),
    ("research/experiments/n11-boundary-recovery-20261006/output/post-23b52acf-after-round4-s6-escalation-s5-cache-corpus-union.cache",
     "9887a18c0788d26507be7e8e191c26817634a6b6"),
]
REPS = [16, 49, 24, 12]
TRANS = []
for j in range(8):
    t = []
    for i in range(121):
        x, y = i % 11, i // 11
        u, v = ((x,y),(10-y,x),(10-x,10-y),(y,10-x),
                (10-x,y),(10-y,10-x),(x,10-y),(y,x))[j]
        t.append(11*v+u)
    TRANS.append(t)


def points(mask):
    return [i for i in range(121) if (mask >> i) & 1]


def canonical(p):
    return min(sum(1 << t[i] for i in p) for t in TRANS)


def det4(p):
    rows = []
    for i in p:
        x, y = i % 11, i // 11
        rows.append((x*x+y*y,x,y))
    a = [[rows[i][j]-rows[0][j] for j in range(3)] for i in range(1,4)]
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def cover(p, a):
    mask = 0
    for t in TRANS:
        q = [t[i] for i in p]
        if a in q and 60 in q:
            for x in q:
                if x != a and x != 60:
                    mask |= 1 << x
    return mask


def win4_set():
    merged = {}
    for rel, expected in SOURCES:
        raw = (ROOT / rel).read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        assert digest == expected, (rel, digest)
        current = {}
        for line in raw.decode().splitlines():
            if not line or line.startswith("#"):
                continue
            f = line.split(",")
            assert len(f) == 6 and f[0] == "s5verdict" and f[3] == "5"
            key = int(f[1]) + (int(f[2]) << 64)
            verdict = int(f[4])
            assert verdict in (1,2) and key not in current
            current[key] = verdict
            if key in merged:
                assert merged[key] == verdict, "WIN/LOSS CONFLICT"
            merged[key] = verdict
    assert len(merged) == 5853
    wins = [k for k,v in merged.items() if v == 1]
    assert len(wins) == 161
    blocked = set()
    for k in wins:
        p = points(k)
        assert len(p) == 5 and canonical(p) == k
        for x in p:
            blocked.add(canonical([y for y in p if y != x]))
    assert len(blocked) == 555
    return blocked


def solve_root(a, row, blocked, seconds):
    dual = sorted(map(int, row["dual_numerators"]))
    assert row["minimum_classes"] == 31 and len(dual) == 62
    thirds = [x for x in range(121) if x not in (a,60)]
    nond = [x for x in thirds if x not in dual]
    assert len(nond) == 57
    dual_mask = sum(1 << x for x in dual)
    classes = {}
    for c in thirds:
        for d in thirds:
            if d <= c:
                continue
            p = [a,60,c,d]
            if det4(p) == 0:
                continue
            key = canonical(p)
            if key not in classes:
                classes[key] = cover(p,a)
    assert len(classes) == row["legal_s4_classes"]
    candidates = [(k,m) for k,m in classes.items()
                  if k not in blocked and (m & dual_mask).bit_count() == 2]
    original = set(int(k,16) for k in row["primal_s4_classes"])
    index = {x:i for i,x in enumerate(dual+nond)}
    rr, cc = [], []
    for j,(_,m) in enumerate(candidates):
        for x in points(m):
            if x in index:
                rr.append(index[x])
                cc.append(j)
    A = coo_matrix((np.ones(len(rr)),(rr,cc)),
                   shape=(119,len(candidates))).tocsr()
    lb = np.r_[np.ones(62),np.ones(57)]
    ub = np.r_[np.ones(62),np.full(57,np.inf)]
    costs = np.array([0.0 if k in original else 1.0 for k,_ in candidates])
    start = time.monotonic()
    res = milp(costs,integrality=np.ones(len(candidates)),
               bounds=Bounds(np.zeros(len(candidates)),np.ones(len(candidates))),
               constraints=LinearConstraint(A,lb,ub),
               options={"time_limit":seconds,"presolve":True})
    elapsed = round(time.monotonic()-start,3)
    out = dict(first=a,status=int(res.status),message=str(res.message),
               elapsedSeconds=elapsed,candidates=len(candidates),
               geometricLowerBound=31,found=False)
    if res.x is not None:
        chosen = [k for (k,_),v in zip(candidates,res.x) if v > 0.5]
        cov = 0
        for k in chosen:
            assert k not in blocked
            cov |= classes[k]
        full = sum(1 << x for x in thirds)
        if len(chosen) == 31 and cov == full:
            new = set(chosen)
            out.update(found=True,removed=sorted(f"{k:032x}" for k in original-new),
                       added=sorted(f"{k:032x}" for k in new-original),
                       chosenClasses=31,thirdMovesCovered=119)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds",type=float,default=50.0)
    args = parser.parse_args()
    cert = json.loads(gzip.decompress(base64.b64decode(
        (HERE/"certificate.json.gz.b64").read_text().strip())))
    assert cert["schema"] == "n11-central-19-geometric-s4-cover-v1"
    blocked = win4_set()
    for a in REPS:
        row = next(r for r in cert["roots"] if r["first"] == a)
        result = solve_root(a,row,blocked,args.seconds)
        print(json.dumps({"schema":"n11-central-31-ilp-v1",
                          "outcome":"UNKNOWN","result":result},
                         ensure_ascii=False),flush=True)


if __name__ == "__main__":
    main()
