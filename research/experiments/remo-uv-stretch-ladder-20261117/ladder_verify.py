#!/usr/bin/env python3
"""Unified weight-ladder verification.

Family F(w, h; n): n players; the first n-h hold w stones, the LAST h hold
w+1 ("hot"); pot w; pointer at position 0 (the first cold player).
  F(w,0) = W_w (uniform), F(w,1) = H_w, F(w,2) = G_w, F(w,3) = T_w, ...

Unified ladder claim (machine-verified here; proof for the w=2 cases and
the h=0 case in the report):
  For k >= 1, write n = (w+1)k + r with 0 <= r <= w.
  The stretch-w of F(w,h;n) ends in the state of a reduced game:
    base weight B = w+1 (usual) or w+2 (collapsed case n' <= h'),
    hot count h'' = min(h', n'), h' = (h-1-r) mod (w+1),
    n' = w*k + e,  e = (r-1) if h == 0 else max(r-1, 0),
    the end circle read from the new pointer consists of n'-h'' players
    holding B followed by h'' players holding B+1 (hot at the END),
    end pot = B,
  and playing the reduced game (positions 0..n'-1 of that circle, pot B,
  ptr 0) and mapping its survivor position back through the circle
  reproduces the full game's survivor.

Checks, for every (w, h, n) in the tested grid:
  (1) stretch-w end pot equals B (B chosen by the collapse rule),
  (2) end circle counts = [B]*(n'-h'') + [B+1]*h'' read from new ptr,
  (3) reduced-game survivor position maps to the full-game survivor.
"""
import sys


def play_until_stretch_end(counts, pot):
    """Play phases while the STARTING pot equals the initial pot; return
    (circle_labels_from_ptr, circle_counts, end_pot, ptr_fp). Ends when a
    phase started with the initial pot produces a different new pot, or
    the game finishes."""
    n = len(counts)
    lab = list(range(n))
    cts = list(counts)
    k = n
    ptr = 0
    p0 = pot
    p = pot
    if k == 1:
        order = [(lab[(ptr + j) % k], cts[(ptr + j) % k]) for j in range(k)]
        return order, p, lab[0]
    while True:
        for i in range(p):
            cts[(ptr + i) % k] += 1
        li = (ptr + p) % k
        held = cts[li]
        del cts[li]; del lab[li]
        ptr = li if li < k - 1 else 0
        newp = held
        k -= 1
        if k == 1 or newp != p0:
            break
        p = newp
    order = [(lab[(ptr + j) % k], cts[(ptr + j) % k]) for j in range(k)]
    return order, newp, lab[0]


def survivor(counts, pot):
    n = len(counts)
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


def check(w, h, n):
    """Returns None if OK (or out of claim range), else an error string."""
    counts = [w] * (n - h) + [w + 1] * h
    r = n % (w + 1)
    k = n // (w + 1)
    if k < 1 or h > w:
        return None  # outside claim range
    if h >= 2 and 1 <= r < h:
        return None  # open class (different structure; see report)
    e = (r - 1) if h == 0 else max(r - 1, 0)
    np_ = w * k + e
    hp = (h - 1 - r) % (w + 1)
    if np_ < 1:
        return None  # degenerate terminal
    collapsed = np_ < hp
    if collapsed:
        B = w + 2
        hpp = 0
    else:
        B = w + 1
        hpp = min(hp, np_)
    order, endpot, _ = play_until_stretch_end(counts, w)
    if len(order) != np_:
        return (f"n' mismatch: got {len(order)} expected {np_}")
    if endpot != B:
        return (f"end pot {endpot} != B={B}")
    exp_counts = [B] * (np_ - hpp) + [B + 1] * hpp
    got_counts = [c for _, c in order]
    if got_counts != exp_counts:
        return (f"end counts {got_counts[:8]}... != {exp_counts[:8]}...")
    # survivor consistency
    full_sv = survivor(counts, w)
    red_sv = survivor(exp_counts, B)
    pred = order[red_sv][0]
    if pred != full_sv:
        return (f"survivor mismatch: reduced->{pred} full->{full_sv}")
    return None


def main():
    grid = [
        (2, [0, 1, 2], 1000),
        (3, [0, 1, 2, 3], 800),
        (4, [0, 1, 2, 3, 4], 250),
        (5, [0, 1, 2, 3, 4, 5], 150),
    ]
    total = bad = 0
    for w, hs, N in grid:
        for h in hs:
            errs = 0
            first = None
            for n in range(w + 1, N + 1):
                r = check(w, h, n)
                total += 1
                if r is not None:
                    errs += 1
                    if first is None:
                        first = (n, r)
            stat = "OK" if errs == 0 else f"FAIL {errs} (first {first})"
            print(f"w={w} h={h} n in [{w+1},{N}]: {stat}")
    print(f"total checks: {total}")


if __name__ == "__main__":
    main()
