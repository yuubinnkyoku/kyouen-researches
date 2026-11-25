#!/usr/bin/env python3
"""Independent chord-equation census, cross-checking the C++ circle census."""
import csv
import math
import sys
from pathlib import Path

def chord_count(h,m):
    count=0
    for d0 in range(1,m):
        for d1 in range(1,m):
            if (d0-d1)%2: continue
            d2sq=2*d1*d1-d0*d0-8*h*h
            if d2sq<=0: continue
            d2=math.isqrt(d2sq)
            if d2*d2!=d2sq or d2>=m or (d1-d2)%2: continue
            count+=m-max(d0,d1,d2)
    return count

def r2(n):
    ans=0
    for a in range(-math.isqrt(n),math.isqrt(n)+1):
        b2=n-a*a
        b=math.isqrt(b2)
        if b*b==b2: ans+=1 if b==0 else 2
    return ans

def main(path):
    rows=list(csv.DictReader(Path(path).open(encoding="utf-8")))
    assert len(rows)==60
    for i,row in enumerate(rows,1):
        h=int(row["h"])
        assert h==i
        below=2*h+1
        assert int(row["width_below"])==below
        assert int(row["threshold_width"])==below+1
        assert chord_count(h,below)==int(row["below_count"])==0
        assert chord_count(h,below+1)==int(row["threshold_count"])==int(row["r2_over_4"])==r2(4*h+1)//4
    print("PASS: 60 spacings / 120 boards")

if __name__=="__main__":
    path=Path(__file__).resolve().parent.parent/"output"/"q36_three_row_onset_audit_20261020.csv"
    main(sys.argv[1] if len(sys.argv)>1 else path)
