"""Historical invalid helper, copied verbatim for counterexample reproduction.

Do not use this as a minimum-union lower bound.
"""

from __future__ import annotations

def _lp_relaxation_dual(inst: Instance) -> float:
    """Dual of  min sum x  s.t.  sum_{e in C(s)} x[e] >= 1  for every paid option.

    That relaxation is implied by any integral union plan (set x = 1_union), so
    its optimum is a valid lower bound.  Its dual packs (group, option) pairs
    under a per-element capacity of one; a greedy ascending |C(s)| packing is a
    feasible dual point.
    """
    best = 0.0
    orders = (
        sorted(((i, s) for i in inst.paid for s in inst.groups[i] if inst.cost[s]),
               key=lambda t: (len(inst.cost[t[1]]), t[0], t[1])),
        sorted(((i, s) for i in inst.paid for s in inst.groups[i] if inst.cost[s]),
               key=lambda t: (len(inst.cost[t[1]]), len(inst.pool[t[0]]), t[0], t[1])),
        sorted(((i, s) for i in inst.paid for s in inst.groups[i] if inst.cost[s]),
               key=lambda t: (len(inst.cost[t[1]]), -len(inst.cover[t[1]]), t[0], t[1])),
    )
    for order in orders:
        slack: dict[int, float] = {}
        value = 0.0
        for i, s in order:
            cs = inst.cost[s]
            limit = min(slack.get(e, 1.0) for e in cs)
            if limit <= 1e-12:
                continue
            value += limit
            for e in cs:
                slack[e] = slack.get(e, 1.0) - limit
        if value > best:
            best = value
    return best
