#!/usr/bin/env python3
"""Machine verification of the stretch-2 structure theorems (STR2-V/U),
the SIEVE3 corollaries, and the six weight-3 reductions (RED3 family).

Pot-form dynamics: deal `pot` stones one each from pointer (recipients +1,
wrapping); loser = position (ptr+pot) mod n, read AFTER the deal; the
loser's held count becomes the new pot; pointer = player after the loser.

Verified for every m in [lo, hi] (fresh simulation, compared against the
published pins pc_uv8000.json):

STR2-V (m >= 4): stretch-2 of V(m) has length ceil((m-1)/3); non-final
losers are labels 4, 7, 10, ... in order, each holding 2; final (breaking)
loser by m mod 3:  1 -> label 0 (holds 3),  0 -> label 2 (holds 3),
2 -> label 3 (holds 3).  End states:
  m=3q+1  -> W3(2q):  circle [2,3,5,6,...,m-2,m-1] all 3, pot 3
  m=3q    -> H3(2q-1): circle [3,5,6,8,...,m-1,0] with label 0 hot(4)
  m=3q+2  -> G3(2q):   circle [5,6,8,9,...,m-3,m-2,0,2] with 0,2 hot(4)
where W3(n)=[3]*n, H3(n)=[3]*(n-1)+[4], G3(n)=[3]*(n-2)+[4,4].

STR2-U (m >= 4): stretch-2 length ceil((m+1)/3); non-final losers labels
2, 5, 8, ... each holding 2; breaking loser by m mod 3:
  0 -> label 3 (and label m-1 died in the last block: SIEVE3-U)
  1 -> label 1 (label m-1 alive, 3 stones)
  2 -> label 0 (label m-1 alive, 3 stones)
End states:
  m=3q+2  -> W3(2q+1): circle [1,3,4,6,7,...,m-2,m-1] all 3
  m=3q+1  -> H3(2q):   circle [3,4,6,7,...,m-1,0] with label 0 hot(4)
  m=3q    -> G3(2q-1): circle [4,6,7,9,...,0,1] with labels 0,1 hot(4)

For each m: (a) exact stretch-2 loser sequence, (b) exact end state
(circle labels in pointer order with counts, next pot), (c) playing the
reduced weight-3 game and mapping the survivor position back through the
position->label map reproduces the pinned V(m)/U(m).
"""
import json
import sys


def v_endstate(m):
    """Play V(m) (pot 1, all 2) through stretch-2; return
    (order, pot_after, tr2) where order = [(label, count)] from new ptr and
    tr2 = list of (pot, loser_label, held) for the stretch-2 phases."""
    lab = list(range(m))
    cts = [2] * m
    k = m
    ptr = 0
    pot = 1
    tr2 = []
    while k > 1 and pot == 1:
        for i in range(pot):
            cts[(ptr + i) % k] += 1
        li = (ptr + pot) % k
        held = cts[li]
        assert lab[li] == 1 and held == 2, (m, lab[li], held)
        del cts[li]; del lab[li]
        ptr = li if li < k - 1 else 0
        pot = held
        k -= 1
    while k > 1 and pot == 2:
        for i in range(pot):
            cts[(ptr + i) % k] += 1
        li = (ptr + pot) % k
        held = cts[li]
        tr2.append((pot, lab[li], held))
        del cts[li]; del lab[li]
        ptr = li if li < k - 1 else 0
        pot = held
        k -= 1
    order = [(lab[(ptr + j) % k], cts[(ptr + j) % k]) for j in range(k)]
    return order, pot, tr2


def u_endstate(m):
    """Play U(m) (pot 2, all 2) through stretch-2."""
    lab = list(range(m))
    cts = [2] * m
    k = m
    ptr = 0
    pot = 2
    tr2 = []
    while k > 1 and pot == 2:
        for i in range(pot):
            cts[(ptr + i) % k] += 1
        li = (ptr + pot) % k
        held = cts[li]
        tr2.append((pot, lab[li], held))
        del cts[li]; del lab[li]
        ptr = li if li < k - 1 else 0
        pot = held
        k -= 1
    order = [(lab[(ptr + j) % k], cts[(ptr + j) % k]) for j in range(k)]
    return order, pot, tr2


def survivor_of(n, counts, pot):
    """Generic game: n players, counts (circle from ptr), pot, ptr=0.
    Returns survivor position (0-based original index)."""
    lab = list(range(n))
    cts = list(counts)
    k = n
    ptr = 0
    p = pot
    while k > 1:
        for i in range(p):
            cts[(ptr + i) % k] += 1
        li = (ptr + p) % k
        held = cts[li]
        del cts[li]; del lab[li]
        ptr = li if li < k - 1 else 0
        p = held
        k -= 1
    return lab[0]


def v_expected(m):
    """Expected stretch-2 outcome of V(m):
    (circle, next_pot, breaking_loser, length, pos2label)."""
    r = m % 3
    if r == 1:
        q = (m - 1) // 3
        n = 2 * q
        labs = [2 + 3 * j // 2 if j % 2 == 0 else 3 + 3 * (j - 1) // 2
                for j in range(n)]
        circle = [(l, 3) for l in labs]
        return circle, 3, 0, q, labs
    if r == 0:
        q = m // 3
        n = 2 * q - 1
        # fps 1,3,4,6,7,...,3q-3,3q-2 ; fp i -> label i+2 (i<=m-3), fp m-2 -> 0
        fps = [f for f in range(1, m - 1) if f % 3 in (0, 1)]
        labs = [0 if f == m - 2 else f + 2 for f in fps]
        assert len(labs) == n and labs[-1] == 0, (m, labs)
        circle = [(l, 4 if l == 0 else 3) for l in labs]
        return circle, 3, 2, q, labs
    q = (m - 2) // 3
    n = 2 * q
    # fps 3,4,6,7,...,3q-2 (labels f+2), then fp m-2 (label 0), fp 0 (label 2)
    fps = [f for f in range(3, m - 2) if f % 3 in (0, 1)]
    labs = [f + 2 for f in fps] + [0, 2]
    assert len(labs) == n, (m, labs)
    circle = [(l, 4 if l in (0, 2) else 3) for l in labs]
    return circle, 3, 3, q + 1, labs


def u_expected(m):
    r = m % 3
    if r == 2:
        q = (m - 2) // 3
        n = 2 * q + 1
        # fps 1, then 3,4,6,7,...,3q-2, 3q(=m-2), 3q+1(=m-1)  (identity labels)
        labs = [1] + [f for f in range(3, m) if f % 3 in (0, 1)]
        assert len(labs) == n, (m, len(labs), n)
        circle = [(l, 3) for l in labs]
        return circle, 3, 0, q + 1, labs
    if r == 1:
        q = (m - 1) // 3
        n = 2 * q
        # fps 3,4,6,7,...,3q-2, then fp 3q(=m-1), fp 0 (label 0)
        labs = [f for f in range(3, m - 1) if f % 3 in (0, 1)] + [m - 1, 0]
        assert len(labs) == n, (m, len(labs), n)
        circle = [(l, 4 if l == 0 else 3) for l in labs]
        return circle, 3, 1, q + 1, labs
    q = m // 3
    n = 2 * q - 1
    # fps 4,6,7,9,10,... then 0, 1
    labs = [f for f in range(4, m) if f % 3 in (0, 1)] + [0, 1]
    assert len(labs) == n, (m, len(labs), n)
    circle = [(l, 4 if l in (0, 1) else 3) for l in labs]
    return circle, 3, 3, q + 1, labs


def main():
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    uv = json.load(open("../remo-pc-twin-laws-20261117/data/pc_uv8000.json"))
    Up, Vp = uv["U"], uv["V"]
    bad = 0
    checks = 0
    for m in range(lo, hi + 1):
        # ---------------- V ----------------
        order, pot_after, tr2 = v_endstate(m)
        exp_circle, exp_pot, exp_break, exp_len, labs = v_expected(m)
        if len(tr2) != exp_len:
            bad += 1; print(f"V{m}: stretch2 len {len(tr2)} != {exp_len}"); continue
        if any(tr2[i][1] != 4 + 3 * i or tr2[i][2] != 2
               for i in range(len(tr2) - 1)):
            bad += 1; print(f"V{m}: block seq bad {tr2}"); continue
        if tr2[-1][1] != exp_break or tr2[-1][2] != 3:
            bad += 1
            print(f"V{m}: breaking loser {tr2[-1][1]}!={exp_break} "
                  f"or held {tr2[-1][2]}!=3")
            continue
        if [(l, c) for l, c in order] != exp_circle or pot_after != exp_pot:
            bad += 1
            print(f"V{m}: end state mismatch")
            print("  got:", order[:14], "pot", pot_after)
            print("  exp:", exp_circle[:14], "pot", exp_pot)
            continue
        checks += 1
        n = len(exp_circle)
        sv = survivor_of(n, [c for _, c in exp_circle], 3)
        if labs[sv] != Vp[m - 1]:
            bad += 1
            print(f"V{m}: reduction survivor {labs[sv]} != pin {Vp[m-1]}")
        checks += 1
        # ---------------- U ----------------
        order, pot_after, tr2 = u_endstate(m)
        exp_circle, exp_pot, exp_break, exp_len, labs = u_expected(m)
        if len(tr2) != exp_len:
            bad += 1; print(f"U{m}: stretch2 len {len(tr2)} != {exp_len}"); continue
        if any(tr2[i][1] != 2 + 3 * i or tr2[i][2] != 2
               for i in range(len(tr2) - 1)):
            bad += 1; print(f"U{m}: block seq bad {tr2}"); continue
        if tr2[-1][1] != exp_break or tr2[-1][2] != 3:
            bad += 1
            print(f"U{m}: breaking loser {tr2[-1][1]}!={exp_break} "
                  f"or held {tr2[-1][2]}!=3")
            continue
        died = any(t[1] == m - 1 for t in tr2)
        if died != (m % 3 == 0):
            bad += 1; print(f"U{m}: SIEVE3-U violation (died={died})"); continue
        if [(l, c) for l, c in order] != exp_circle or pot_after != exp_pot:
            bad += 1
            print(f"U{m}: end state mismatch")
            print("  got:", order[:14], "pot", pot_after)
            print("  exp:", exp_circle[:14], "pot", exp_pot)
            continue
        checks += 1
        n = len(exp_circle)
        sv = survivor_of(n, [c for _, c in exp_circle], 3)
        if labs[sv] != Up[m - 1]:
            bad += 1
            print(f"U{m}: reduction survivor {labs[sv]} != pin {Up[m-1]}")
        checks += 1
    print(f"m in [{lo},{hi}]: checks={checks} failures={bad}")


if __name__ == "__main__":
    main()
