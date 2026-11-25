"""Task 2: enumerate every safe set (cap) of the s=2 game on this board and
classify all 6-caps by their 7/8 extensions.

Classification of a non-maximal 6-cap S:
  only8 : every addable point p gives a NON-maximal 7-cap S+p (so S extends to 8)
  only7 : every addable point p gives a MAXIMAL   7-cap S+p
  mixed : addable points of both kinds

The DFS enumerates each cap exactly once.  Safety is maintained with the
standard forbidden mask: p may be added to S iff p is on no line that already
contains two points of S.

Auxiliary cross-checks (incidence vs distinct counting):
  * every 6-subset of a maximal 7-cap must be class only7; count incidences;
  * every 6-subset of an 8-cap must be class only8; count incidences;
  * every 5-cap must have a maximal 6-child and the 5-caps with an only7 child
    are exactly the 5-subsets of maximal 7-caps (counted directly).

Outputs caps_by_size.bin (all caps, grouped by size) and summary_enum.json.
"""

import json
import struct
from array import array

from boardlib import Board, HERE, bits, read_board

N, M, BLOCKS = read_board()
brd = Board(N, BLOCKS)
FULL = brd.FULL
PAIR = brd.pair_line

caps = [[] for _ in range(N + 1)]
counts = [0] * (N + 1)
maximal = [0] * (N + 1)
maxsets = [set() for _ in range(N + 1)]
class6 = {}  # mask -> 0 maximal, 1 only8, 2 only7, 3 mixed

# ---------------------------------------------------------------- DFS enumeration
def dfs(S, forbidden, last):
    k = S.bit_count()
    counts[k] += 1
    caps[k].append(S)
    A = FULL & ~S & ~forbidden
    if A == 0:
        maximal[k] += 1
        maxsets[k].add(S)
        if k == 6:
            class6[S] = 0
        return
    if k == 6:
        has8 = False
        has_max7 = False
        m = A
        while m:
            b = m & -m
            p = b.bit_length() - 1
            f2 = forbidden
            s = S
            pl = PAIR[p]
            while s:
                bb = s & -s
                f2 |= pl[bb.bit_length() - 1]
                s ^= bb
            A2 = FULL & ~(S | b) & ~f2
            if A2:
                has8 = True
            else:
                has_max7 = True
            m ^= b
        if has8 and has_max7:
            class6[S] = 3
        elif has8:
            class6[S] = 1
        else:
            class6[S] = 2
    # canonical enumeration: only add points with index > last
    T = A & ~((1 << (last + 1)) - 1)
    while T:
        b = T & -T
        p = b.bit_length() - 1
        f2 = forbidden
        s = S
        pl = PAIR[p]
        while s:
            bb = s & -s
            f2 |= pl[bb.bit_length() - 1]
            s ^= bb
        dfs(S | b, f2, p)
        T ^= b


dfs(0, 0, -1)

max_size = max(k for k in range(N + 1) if counts[k])
assert max_size <= 8, f"unexpected cap of size {max_size}"

# ------------------------------------------------- 6-cap class counts / identities
c6_max = sum(1 for c in class6.values() if c == 0)
c6_only8 = sum(1 for c in class6.values() if c == 1)
c6_only7 = sum(1 for c in class6.values() if c == 2)
c6_mixed = sum(1 for c in class6.values() if c == 3)
assert len(class6) == counts[6], (len(class6), counts[6])
assert c6_max == maximal[6]
assert c6_max + c6_only8 + c6_only7 + c6_mixed == counts[6]

# ------------------------------------------------------ 6-subsets of maximal 7s
inc7 = 0
bad7 = []
for S in maxsets[7]:
    for a in bits(S):
        T = S ^ (1 << a)
        inc7 += 1
        if class6.get(T) != 2:
            bad7.append((S, T, class6.get(T)))
# incidences of 6-subsets of ALL 7-caps (maximal or not) for reference
inc7_all = counts[7] * 7

# ------------------------------------------------------------ 6-subsets of 8s
inc8 = 0
bad8 = []
for S in caps[8]:
    pts = list(bits(S))
    for i, a in enumerate(pts):
        for b in pts[i + 1:]:
            T = S ^ (1 << a) ^ (1 << b)
            inc8 += 1
            if class6.get(T) != 1:
                bad8.append((S, T, class6.get(T)))

distinct_only7_from8 = len({S ^ (1 << a) for S in maxsets[7] for a in bits(S)})
distinct_only8_from8 = len({
    S ^ (1 << a) ^ (1 << b)
    for S in caps[8]
    for i, a in enumerate(list(bits(S)))
    for b in list(bits(S))[i + 1:]
})

assert not bad7, f"{len(bad7)} 6-subsets of maximal 7-caps are not class only7"
assert not bad8, f"{len(bad8)} 6-subsets of 8-caps are not class only8"

# --------------------------------------------------------- direct 5-cap analysis
five_total = 0
five_with_max6 = 0
five_with_only7child = 0
five_with_only8child = 0
five_with_mixed_child = 0
five_no_child = 0
five_with_8child = 0
for S in caps[5]:
    five_total += 1
    f = brd.forbidden(S)
    A = FULL & ~S & ~f
    if A == 0:
        five_no_child += 1
        continue
    has_max6 = False
    has_only7 = False
    has_only8 = False
    has_mixed = False
    has8 = False
    m = A
    while m:
        b = m & -m
        code = class6[S | b]
        if code == 0:
            has_max6 = True
        elif code == 1:
            has_only8 = True
            has8 = True
        elif code == 2:
            has_only7 = True
        else:
            has_mixed = True
            has8 = True
        m ^= b
    five_with_max6 += has_max6
    five_with_only7child += has_only7
    five_with_only8child += has_only8
    five_with_mixed_child += has_mixed
    five_with_8child += has8

# distinct 5-subsets of maximal 7-caps (direct independent count)
five_from_max7 = set()
for S in maxsets[7]:
    pts = list(bits(S))
    for i in range(7):
        for j in range(i + 1, 7):
            for k in range(j + 1, 7):
                for l in range(k + 1, 7):
                    for mm in range(l + 1, 7):
                        T = (1 << pts[i]) | (1 << pts[j]) | (1 << pts[k]) | (1 << pts[l]) | (1 << pts[mm])
                        five_from_max7.add(T)

# 5-subsets of 8-caps, for reference (with multiplicity and distinct)
inc5_in_8 = len(caps[8]) * 56
five_from_8 = set()
for S in caps[8]:
    pts = list(bits(S))
    for i in range(8):
        for j in range(i + 1, 8):
            for k in range(j + 1, 8):
                for l in range(k + 1, 8):
                    for mm in range(l + 1, 8):
                        T = ((1 << pts[i]) | (1 << pts[j]) | (1 << pts[k])
                             | (1 << pts[l]) | (1 << pts[mm]))
                        five_from_8.add(T)

# ------------------------------------------------------- validate safety primitive
# For a deterministic sample of caps, compare the incremental forbidden mask with
# the direct line definition and the addable mask with direct single-point tests.
import random
rng = random.Random(20261125)
sample_masks = []
for k in range(1, 9):
    if caps[k]:
        sample_masks.extend(rng.sample(caps[k], min(40, len(caps[k]))))
val_bad = 0
for S in sample_masks:
    if not brd.is_safe(S):
        val_bad += 1
    f = brd.forbidden(S)
    A = FULL & ~S & ~f
    direct = 0
    rest = FULL & ~S
    while rest:
        b = rest & -rest
        if brd.is_safe(S | b):
            direct |= b
        rest ^= b
    if A != direct:
        val_bad += 1
assert val_bad == 0, f"{val_bad} safety-primitive mismatches"

# ------------------------------------------------------------------ write output
caps_path = HERE / "caps_by_size.bin"
with open(caps_path, "wb") as f:
    f.write(b"CAPS1\n")
    f.write(struct.pack("<I", N))
    for k in range(N + 1):
        arr = array("Q", caps[k])
        f.write(struct.pack("<Q", len(arr)))
        if arr:
            arr.tofile(f)

summary = {
    "n": N,
    "m": M,
    "max_cap_size": max_size,
    "counts_by_size": {str(k): counts[k] for k in range(max_size + 1)},
    "maximal_by_size": {str(k): maximal[k] for k in range(max_size + 1)},
    "six_cap_classes": {
        "maximal": c6_max,
        "only8": c6_only8,
        "only7": c6_only7,
        "mixed": c6_mixed,
        "total": counts[6],
    },
    "seven_caps": {
        "total": counts[7],
        "maximal": maximal[7],
        "nonmaximal": counts[7] - maximal[7],
        "incidence_6subsets": inc7,
        "incidence_6subsets_all7": inc7_all,
        "distinct_6subsets_of_maximal": distinct_only7_from8,
    },
    "eight_caps": {
        "total": counts[8],
        "maximal": maximal[8],
        "incidence_6subsets": inc8,
        "distinct_6subsets": distinct_only8_from8,
    },
    "six_subset_checks": {
        "max7_subsets_all_only7": not bad7,
        "eight_subsets_all_only8": not bad8,
        "bad7": len(bad7),
        "bad8": len(bad8),
    },
    "five_caps": {
        "total": five_total,
        "with_maximal_6_child": five_with_max6,
        "with_only7_child": five_with_only7child,
        "without_only7_child": five_total - five_with_only7child,
        "with_only8_child": five_with_only8child,
        "with_mixed_child": five_with_mixed_child,
        "with_any_8_child": five_with_8child,
        "no_child": five_no_child,
        "distinct_5subsets_of_maximal7": len(five_from_max7),
        "incidence_5subsets_of_8": inc5_in_8,
        "distinct_5subsets_of_8": len(five_from_8),
    },
    "safety_primitive_sample": len(sample_masks),
    "safety_primitive_mismatches": val_bad,
}
(HERE / "summary_enum.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps(summary, indent=2))
