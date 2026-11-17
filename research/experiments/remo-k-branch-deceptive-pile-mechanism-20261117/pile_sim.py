"""(1,1,p)|0 pile-game simulator (v2, fixed succ: true r passed explicitly).

Reduction (from the region/mask game semantics):
profile atoms (1,1,0,p,0,0,0): a=star1-only(size1), b=star2-only(size1),
c=star3-only(size p). Occupied atoms always lie in a single star; when
the c pile is the only occupied atom only c is legal (forced); when the
board is empty any pile may be opened. Opening a or b (size 1) completes
its star instantly and the elimination cascade leaves the opener as the
sole survivor (win-now). The c pile forces a deterministic stretch until
the board re-empties (decision point) or one player remains (terminal).
"""
import sys

def succ(x, A, r):
    for d in range(1, r + 1):
        q = (x + d) % r
        if q in A:
            return q
    raise AssertionError("no active player after %d" % x)

def forced_stretch(p, A, mu, r):
    """Deterministic c-pile stretch from empty board, mover mu.
    Returns ('end', survivor) or ('decision', A', mu')."""
    A = set(A)
    m = {j: 0 for j in A}
    count = 0
    mover = mu
    while True:
        if count == p:
            mm = m[mover]
            A.discard(mover)
            if len(A) == 1:
                return ('end', next(iter(A)))
            nm = succ(mover, A, r)
            count -= mm
            mover = nm
            if count == 0:
                return ('decision', frozenset(A), nm)
        else:
            m[mover] += 1
            count += 1
            mover = succ(mover, A, r)

def sv_set(p, r):
    """All possible survivors over all plays, (1,1,p)|0, r players."""
    survivors = set()
    A, mu = frozenset(range(r)), 0
    seen = set()
    while True:
        survivors.add(mu)          # win-now option at the decision point
        if (A, mu) in seen:
            raise AssertionError("cycle in decision path p=%d r=%d" % (p, r))
        seen.add((A, mu))
        res = forced_stretch(p, A, mu, r)
        if res[0] == 'end':
            survivors.add(res[1])
            return survivors
        A, mu = res[1], res[2]

if __name__ == "__main__":
    p = int(sys.argv[1]); r = int(sys.argv[2])
    print(p, r, sorted(sv_set(p, r)))
