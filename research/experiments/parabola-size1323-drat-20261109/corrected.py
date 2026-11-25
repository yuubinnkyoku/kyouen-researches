"""Four size-h classes with the complete selector range reserved."""
from encoding_fixed import build

SHAPES = {"000": (0, 0, 0), "011": (0, 1, 1), "101": (1, 0, 1), "112": (1, 1, 2)}


def encode(p, shape, edges):
    x, c, e = SHAPES[shape]
    h = (p-1)//2
    if c+e > h:
        return [[]], 4*h+p-1, 4*h, 0
    clauses, nv, used = build(p, edges, x, c, e)
    return clauses, nv, nv-(p-1), used


def dimacs(clauses, nv):
    return (f"p cnf {nv} {len(clauses)}\n"+"".join(
        " ".join(map(str, clause))+" 0\n" for clause in clauses)).encode("ascii")
