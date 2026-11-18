#!/usr/bin/env python3
"""K0941 core: pure-arithmetic determination of V(m)/U(m) for composite N.

Composition of PUBLISHED theorems only:
  K0928 (pot dynamics / RED), K0931/K0933/K0934 (LAD-GEN stretch law,
  end-state census, watched criterion), K0935 (WATCH-MAP), K0937 (INV-TRACK,
  death congruence ladder death <=> (w+1)|N), K0939 (ENTRY-LOC family
  entry, END-INV/E-model transitions, SIEVE-PRIME).

New here (machine-derived, anchored in this experiment):
  THM-A  composite N never reaches the t=0 endgame (ladder-only death at
         stretch spf(N)-1)   [paper proof in report.md]
  THM-B  death dichotomy + post-death states:
         V: breaking death (r=h-1)  -> uniform Z(w+1, n-t)
         U: block death (r=h) -> breaking runs -> E(w+1; n-t-1-w, w)
              collapse (t=h=r=0) -> Z(w+2, w-1)
  THM-C  the post-death game is the E-model recursion (E-form is
         phase-self-preserving from ANY E/uniform state); the survivor
         frame position is the Josephus-type recursion sigma
  THM-D  the death-stretch frame->label map is the LAD-GEN composition
  =>  V(m)/U(m) for composite N = pure arithmetic, no engine.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sievegen_core import track_gen, isprime, spf


# ---------- THM-C: E-game / uniform-game survivor position --------------
def sigma_E(P, alpha, beta):
    """Survivor frame position of the E-game E(P;alpha,beta):
    k=alpha+beta players, ptr-frame circle [P]^alpha+[P+1]^beta, pot P.
    Phase rule of K0928 Lemma P; E-form self-preservation (THM-C).
    Returns position in [0, k-1] of the final survivor (frame at entry).
    """
    if alpha + beta <= 1:
        return 0
    frames = []
    k = alpha + beta
    while k > 1:
        q, r = divmod(P, k)
        frames.append((k, r))
        if r < alpha:
            P, alpha, beta = P + q, alpha - r - 1, beta + r
        else:
            P, alpha, beta = P + q + 1, beta + 2 * alpha - r - 1, r - alpha
        k -= 1
    sig = 0
    for (k, r) in reversed(frames):
        sig = (r + 1 + sig) % k
    return sig

def sigma_Z(M, K):
    """Survivor frame position of the uniform game Z(M,K):
    K players all holding M, pot M.  One phase -> E(M+q; K-1-r, r)."""
    if K <= 1:
        return 0
    q, r = divmod(M, K)
    # Z phase: loser at position r; new frame starts at r+1
    return (r + 1 + sigma_E(M + q, K - 1 - r, r)) % K

# ---------- THM-D: death-stretch frame -> label map ---------------------
def _walk(LS, origin, removed, n):
    """Labels in frame order: circle positions origin, origin+1, ... mod n,
    skipping removed positions."""
    out = []
    p = origin % n
    for _ in range(n):
        if p not in removed:
            out.append(LS[p])
        p = (p + 1) % n
    return out

def _stretch_removals(w, n, t, r, h):
    """Removals (fixed-frame positions) and new-frame origin of ONE
    surviving ladder stretch (LAD-GEN): blocks + breaking. Returns
    (removed_set, origin) with origin = bl+1."""
    J = t if r >= h else t - 1
    if r < h:
        bl = n - r - 1
    elif r >= 1:
        bl = w - r
    else:                      # r == 0, h == 0, t >= 2
        bl = w + 1
    removed = set(j * (w + 1) - 1 for j in range(1, J + 1))
    removed.add(bl)
    return removed, (bl + 1) % n

def death_frame(side, m, steps, death):
    """Label list (frame order) + post-death game entry for the composite
    game. steps: tracker steps; death: the death step (last).
    Returns (frame, entry) where entry is
      ('Z', M, K)                uniform state, or
      ('E', P, alpha, beta)     E-form state.
    """
    w, n = death['w'], death['n']
    t, r, h = death['t'], death['r'], death['h']
    # label map at the START of the death stretch (fixed frame)
    if side == 'V':
        LS = [(i + 2) % m for i in range(m - 1)]   # post phase-1 frame
    else:
        LS = list(range(m))                        # game start frame
    for st in steps[:-1]:
        rem, org = _stretch_removals(st['w'], st['n'], st['t'],
                                     st['r'], st['h'])
        LS = _walk(LS, org, rem, st['n'])
    if side == 'V':
        # breaking death: watch at n-h, blocks 1..t-1
        assert r == h - 1, ("V death not breaking", death)
        removed = set(j * (w + 1) - 1 for j in range(1, t))
        removed.add(n - h)
        frame = _walk(LS, (n - h + 1) % n, removed, n)
        return frame, ('Z', w + 1, n - t)
    # U: block death (r == h), then the stretch breaking still runs
    assert r == h, ("U death not block", death)
    if t == 1 and h == 0:
        # collapse: block 1 removes the watch (position w), the collapse
        # phase removes position 0; post state Z(w+2, w-1), frame from 1
        assert r == 0
        removed = {w, 0}
        frame = _walk(LS, 1, removed, n)
        return frame, ('Z', w + 2, w - 1)
    bl = w + 1 if r == 0 else w - r
    removed = set(j * (w + 1) - 1 for j in range(1, t + 1))
    removed.add(bl)
    frame = _walk(LS, (bl + 1) % n, removed, n)
    return frame, ('E', w + 1, n - t - 1 - w, w)

def predict_composite(side, m):
    """Pure-arithmetic V(m)/U(m) for composite N. Returns
    (value, info) or (None, info) if the tracker does not report a
    ladder death (should not happen for odd composite N)."""
    N = 2 * m + 1 if side == 'V' else 2 * m + 3
    tr = track_gen(side, m)
    info = {'N': N, 'status': tr['status'], 'steps': len(tr['steps'])}
    if tr['status'] != 'died':
        return None, info
    death = tr['steps'][-1]
    frame, entry = death_frame(side, m, tr['steps'], death)
    if entry[0] == 'Z':
        _, M, K = entry
        sig = sigma_Z(M, K)
    else:
        _, P, alpha, beta = entry
        sig = sigma_E(P, alpha, beta)
    info.update({'death': {k: death[k] for k in
                           ('w', 'n', 't', 'r', 'h', 'phase', 'held')},
                 'entry': entry, 'sigma': sig,
                 'frame_len': len(frame)})
    return frame[sig], info

def predict(side, m):
    """Pure-arithmetic V(m) (side 'V') / U(m) (side 'U') for ALL m >= 1.
    Prime N: SIEVE-PRIME (K0939). Composite N: this file. Base pins:
    V m=1 (N=3): 0; U m=1 (N=5): 0."""
    N = 2 * m + 1 if side == 'V' else 2 * m + 3
    if isprime(N):
        return 0 if side == 'V' else m - 1
    val, info = predict_composite(side, m)
    if val is None:
        raise RuntimeError(("no ladder death", side, m, N, info))
    return val
