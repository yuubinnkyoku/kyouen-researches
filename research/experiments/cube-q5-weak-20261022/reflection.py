#!/usr/bin/env python3
"""Constructive strategy for the 3D coplanar/cospherical q=5 game.

Coordinates are zero based. The opponent must play legally from a safe,
reflection invariant position. No search or finite board-size limit is used.
"""
from __future__ import annotations

import argparse
import json


def reply(shape: tuple[int, int, int], point: tuple[int, int, int]):
    if len(shape) != 3 or any(n <= 0 for n in shape):
        raise ValueError("shape must have three positive side lengths")
    if len(point) != 3 or any(not 0 <= p < n for p, n in zip(point, shape)):
        raise ValueError("point is outside the board")
    axis = next((i for i, n in enumerate(shape) if n % 2 == 0), None)
    if axis is None:
        raise ValueError("fixed-point-free coordinate reflection needs an even side")
    result = list(point)
    result[axis] = shape[axis] - 1 - result[axis]
    return tuple(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("shape", nargs=3, type=int)
    parser.add_argument("point", nargs=3, type=int)
    args = parser.parse_args()
    try:
        response = reply(tuple(args.shape), tuple(args.point))
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps({"opponent": args.point, "reply": response}))
