#!/usr/bin/env python3
"""Closed-form A/B/C child-signature derivator for z=12, y>=6.

This is separate from the band table.  It transcribes only the already
published K1043 and K1055 anchors plus the proposed z=12 induction formula.
"""
from candidate import k1043_z12_y5, k1055_z11, value12


def child_values(y, d, R):
    x = y + d
    r = R - 1
    values = set()
    if y == 6:
        values.add(k1043_z12_y5(x, r))
    else:
        values.add(value12(x, y - 1, r))
    if d > 0:
        values.add(value12(x - 1, y, r))
    values.add(1 ^ k1055_z11(x, y, r))
    return tuple(sorted(values))


def child_signature(y, d, R):
    return "".join(str(v) for v in child_values(y, d, R))


def mex_of_signature(sig):
    values = {int(c) for c in sig}
    m = 0
    while m in values:
        m += 1
    return m
