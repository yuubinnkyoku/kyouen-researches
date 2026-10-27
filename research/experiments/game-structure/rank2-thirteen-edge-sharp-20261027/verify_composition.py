"""Independent multiset-counting check from connected Grundy histograms.

Each (edge count e, Grundy z) category with c connected types contributes
C(c+k-1,k) multisets of k components, with xor z when k is odd.
"""
from math import comb

CONNECTED = {
    1: {1: 1},
    2: {2: 1},
    3: {0: 1, 1: 2},
    4: {0: 1, 2: 2, 3: 2},
    5: {0: 4, 1: 5, 2: 1, 3: 2},
    6: {0: 6, 1: 6, 2: 9, 3: 9},
    7: {0: 25, 1: 27, 2: 10, 3: 14, 4: 3},
    8: {0: 49, 1: 52, 2: 56, 3: 56, 4: 14},
    9: {0: 193, 1: 209, 2: 130, 3: 111, 4: 53, 5: 14},
    10: {0: 539, 1: 557, 2: 476, 3: 446, 4: 204, 5: 99, 6: 1},
    11: {0: 2022, 1: 2006, 2: 1364, 3: 1381, 4: 739, 5: 546, 6: 13},
    12: {0: 6773, 1: 6645, 2: 5233, 3: 5198, 4: 2887, 5: 2588, 6: 161, 7: 18},
    13: {0: 25596, 1: 25030, 2: 18747, 3: 18810, 4: 11429, 5: 11647, 6: 1318, 7: 245},
}
EXPECTED = [43796, 43505, 35095, 35257, 15685, 16100, 2485, 1444]
LIMIT = 13
ways = [[0] * 16 for _ in range(LIMIT + 1)]
ways[0][0] = 1
for e, histogram in CONNECTED.items():
    for z, count in histogram.items():
        nxt = [[0] * 16 for _ in range(LIMIT + 1)]
        for used in range(LIMIT + 1):
            for old_z, value in enumerate(ways[used]):
                if not value:
                    continue
                for k in range((LIMIT - used) // e + 1):
                    nxt[used + k * e][old_z ^ (z if k % 2 else 0)] += (
                        value * comb(count + k - 1, k)
                    )
        ways = nxt
assert ways[13][:8] == EXPECTED
assert all(v == 0 for v in ways[13][8:])
print("13-edge classes:", sum(ways[13]), "histogram:", ways[13][:8])
