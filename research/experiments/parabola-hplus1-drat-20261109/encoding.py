"""One-hot pair states and an explicitly supplied forbidden-edge relaxation."""
from pysat.card import CardEnc, EncType

SHAPES = {"a": (1, 0, 0), "b": (0, 1, 0), "c": (1, 1, 1)}


def state_var(i, state):
    return 4*(i-1)+{"B": 1, "N": 2, "L": 3, "H": 4}[state]


def encode(p, shape, edges):
    h = (p-1)//2
    origin, both_count, none_count = SHAPES[shape]
    clauses = []
    for i in range(1, h+1):
        states = [state_var(i, state) for state in ("B", "N", "L", "H")]
        clauses.append(states)
        clauses.extend([[-states[a], -states[b]] for a in range(4) for b in range(a)])
    top = 4*h
    for state, count in (("B", both_count), ("N", none_count)):
        card = CardEnc.equals([state_var(i, state) for i in range(1, h+1)],
                              bound=count, top_id=top, encoding=EncType.seqcounter)
        clauses.extend(card.clauses)
        top = max(top, card.nv)
    point_base = top
    for t in range(1, p):
        i = min(t, p-t)
        side = state_var(i, "L" if t <= h else "H")
        both = state_var(i, "B")
        point = point_base+t
        clauses.extend([[-point, side, both], [point, -side], [point, -both]])
    used = 0
    for edge in edges:
        if not origin and 0 in edge:
            continue
        clauses.append([-point_base-t for t in edge if t != 0])
        used += 1
    return clauses, point_base+p-1, point_base, used


def dimacs(clauses, nv):
    return (f"p cnf {nv} {len(clauses)}\n"+"".join(
        " ".join(map(str, clause))+" 0\n" for clause in clauses)).encode("ascii")
