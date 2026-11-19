#!/usr/bin/env python3
"""Transcription of the published K1037 (z=11, y=5) closed form.
Exact code copied from research/experiments/vertical-fiber-two-token-z11-y5-boundary-20261119/verify_z11_y5.py
"""
def _odd_le(R, hi):
    return R % 2 == 1 and 1 <= R <= hi

def in_T(x, R):
    if x == 5:
        return _odd_le(R, 9)
    if x == 6:
        return _odd_le(R, 15)
    if not _odd_le(R, 11):
        if x == 8:
            return R == 17
        if x == 12:
            return R == 19
        if x == 16:
            return R == 21
        if x == 17:
            return 21 <= R <= 33 and R % 2 == 1
        if x >= 18:
            return R == 21
        return False
    return True

ROW_P = {
    5: (), 6: (12, 14, 16), 7: (12, 14, 16), 8: (12, 14, 16),
    9: (12, 14, 16), 10: (12, 14, 16), 11: (12, 14, 16, 18),
    12: (12, 14, 16, 18, 20), 13: (12, 14, 16, 18),
    14: (12, 14, 16, 18, 20), 15: (12, 14, 16, 18, 20),
    16: (12, 14, 16, 18, 20), 17: (12, 14, 16, 18, 20),
}
BASE_P = (12, 14, 16, 18, 20)
PIONEER_LO = {6: 17, 8: 18, 10: 18, 12: 21, 14: 20, 16: 22}

def in_P(x, R):
    if x <= 17:
        if R in ROW_P[x]:
            return True
        if x in PIONEER_LO:
            return R >= PIONEER_LO[x]
        return False
    if R in BASE_P:
        return True
    if x % 2 == 0:
        return (23 <= R <= x + 17 and R % 2 == 1) or R >= x + 18
    return 23 <= R <= x + 16 and R % 2 == 1

def candidate(x, R):
    if R == 0:
        return 0
    if in_T(x, R):
        return 2
    if in_P(x, R):
        return 1
    return 0
