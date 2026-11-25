#!/usr/bin/env python3
"""Read a certified q=5 cube strategy and return the next player's witness.

Points use index (x*side+y)*side+z, with zero-based coordinates. The occupied
position must occur in the certified strategy; arbitrary positions need not.
"""
from itertools import permutations, product
from pathlib import Path
import argparse
import gzip
import json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("occupied", nargs="+", type=int)
    args = parser.parse_args()
    opener = gzip.open if args.certificate.suffix == ".gz" else open
    with opener(args.certificate, "rt") as stream:
        magic, side, _, _ = stream.readline().split()
        if magic != "Q5CUBE1":
            parser.error("unsupported certificate")
        side = int(side)
        records = {}
        for line in stream:
            lo, hi, label, wlo, whi = map(int, line.split())
            records[lo | (hi << 64)] = (label, wlo | (whi << 64))
    if len(set(args.occupied)) != len(args.occupied) or any(
            p < 0 or p >= side**3 for p in args.occupied):
        parser.error("occupied indices must be distinct and inside the board")
    points = list(product(range(side), repeat=3))
    lookup = {p: i for i, p in enumerate(points)}
    transforms = []
    for axes in permutations(range(3)):
        for flips in product((False, True), repeat=3):
            transforms.append([lookup[tuple(side-1-p[axes[j]] if flips[j] else p[axes[j]]
                                            for j in range(3))] for p in points])

    def canonical(occupied):
        return min(sum(1 << t[p] for p in occupied) for t in transforms)

    mask = canonical(args.occupied)
    if mask not in records:
        parser.error("position is outside this certified strategy")
    label, witness = records[mask]
    if not label:
        parser.error("this is a losing position; no winning reply is certified")
    for p in range(side**3):
        if p not in args.occupied and canonical([*args.occupied, p]) == witness:
            print(json.dumps({"reply_index": p, "reply_coordinates": points[p],
                              "resulting_position": "P"}))
            return
    parser.error("certificate has no matching witness")


if __name__ == "__main__":
    main()
