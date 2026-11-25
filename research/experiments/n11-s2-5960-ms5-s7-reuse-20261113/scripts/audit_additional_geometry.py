#!/usr/bin/env python3
"""Independently audit the extra candidates with a lifted determinant."""
import csv
import gzip
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]


def det3(a,b,c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0]))


def safe(mask):
    points = [(i % 11, i // 11) for i in range(121) if mask >> i & 1]
    for quad in combinations(points,4):
        x,y = quad[0]
        rows = [(a-x,b-y,a*a+b*b-x*x-y*y) for a,b in quad[1:]]
        if det3(*rows) == 0:
            return False
    return True


def main():
    path = HERE/'output/additional-candidates.csv.gz'
    with gzip.open(path,'rt',newline='') as source:
        rows = list(csv.DictReader(source))
    assert len(rows) == 6309
    for row in rows:
        parent = int(row['s6_hex'],16)
        move = int(row['move_in_s6_coordinates'])
        assert parent.bit_count() == 6 and 0 <= move < 121 and not parent >> move & 1
        assert safe(parent | (1 << move))
    print(f'{len(rows)} extra moves: independent determinant geometry passed')


if __name__ == '__main__':
    main()
