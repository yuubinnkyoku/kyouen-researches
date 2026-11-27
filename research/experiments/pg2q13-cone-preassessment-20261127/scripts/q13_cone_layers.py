#!/usr/bin/env python3
"""PG(2,13) s=2 cone pre-assessment + exact arc census layers m=4..7.

Method: fix a non-collinear triangle F (PGL(3,13) transitive on triangles).
Cone = all arcs containing F. Canonical DFS: added points (all indices < v-1,
excluding F members) enumerated in increasing order => each arc containing F
exactly once. T_m := #arcs of size m containing F. Double counting over triples:
  N_m = N_3 * T_m / C(m,3),  N_3 = C(v,3) - #lines*C(q+1,3).
Gates (fail-closed):
  G1 board: v=183, 183 lines x 14 points, pair->line unique, two lines meet once.
  G2 T_4 == v - 3 - 3*(q-1) (points off the 3 triangle sides).
  G3 divisibility N_3*T_m % C(m,3) == 0 for all m.
  G4 two different triangles give identical T_m (transitivity check).
Pre-assessment: layer growth => full cone (all sizes) too large for pure-Python
single-command runs; full s=2 spectrum needs a C/bitset port.

Depends on pg2q9_cone_spectrum.py (published at
research/experiments/pg2q-s2-cone-spectrum-family-20261127/scripts/) for the
PG(2,q) board builder with its internal axioms assertions.
Run: python3 q13_cone_layers.py   (rc=0 on all gates PASS)
"""
import sys, time, json
from math import comb
sys.path.insert(0, '.')
from pg2q9_cone_spectrum import Board

def layers(b, F, maxm, tlimit):
    v = b.v
    Fm = 0
    for i in F: Fm |= 1 << i
    pl = b.plm[F[0]][F[1]]
    assert not (pl >> F[2]) & 1, "F collinear"
    T0 = time.time()
    layer = {Fm: True}
    T = {3: 1}
    m = 3
    while layer and m < maxm:
        if time.time() - T0 > tlimit:
            return T, None
        nxt = {}
        for mask in layer:
            mm = mask & ~Fm & ((1 << (v-1)) - 1)
            last = mm.bit_length() - 1 if mm else -1
            for j in range(last+1, v-1):
                if mask >> j & 1: continue
                ok = True; pm = mask
                while pm:
                    lb = pm & -pm; pm ^= lb; p = lb.bit_length() - 1
                    lm = b.plm[p][j]
                    if (lm & mask) != lb: ok = False; break
                if ok:
                    nxt[mask | (1 << j)] = True
        T[m+1] = len(nxt)
        layer = nxt; m += 1
    return T, time.time() - T0

def main():
    q = 13
    b = Board(q)
    v = b.v
    gates = {}
    gates["G1_board"] = (v == 183 and len(b.lines) == 183
                         and all(len(l) == 14 for l in b.lines))
    gates["G1_pair_line_unique"] = len(b.pair_line) == comb(v, 2)
    N3 = comb(v, 3) - len(b.lines) * comb(q+1, 3)
    Fs = [[0, q*q, v-1], [5, q*q+3, v-1]]
    results = []
    for F in Fs:
        T, dt = layers(b, F, 7, 200.0)
        assert T is not None, "timeout"
        results.append((F, T, dt))
    T1, T2 = results[0][1], results[1][1]
    gates["G4_two_triangles"] = (T1 == T2)
    gates["G2_T4"] = (T1[4] == v - 3 - 3*(q-1))
    Nm = {}
    gates["G3_divisibility"] = True
    for m in range(4, 8):
        tm = T1[m]
        if (N3 * tm) % comb(m, 3) != 0:
            gates["G3_divisibility"] = False
        Nm[m] = N3 * tm // comb(m, 3)
    gates["all"] = all(gates.values())
    out = {
        "board": "PG(2,13)", "v": v, "q": q,
        "N_3": N3,
        "T_m_cone_layers": {str(k): T1[k] for k in sorted(T1)},
        "N_m_arcs": {str(k): Nm[k] for k in sorted(Nm)},
        "triangles": [str(F) for F, _, _ in results],
        "T_m_second_triangle": {str(k): T2[k] for k in sorted(T2)},
        "gates": gates,
        "timings_s": [round(r[2], 1) if r[2] else None for r in results],
        "layer_growth_6_to_7": T1[7] / T1[6],
        "note": ("layers m<=7 complete enumeration; m>=8 not attempted "
                 "(estimated >=10^7 states/layer; full cone ~10^7-10^8 => "
                 "pure-Python single-command infeasible; C/bitset port needed "
                 "for full PG(2,13) s=2 spectrum)"),
    }
    print(json.dumps(out, indent=1))
    assert gates["all"], "GATE FAIL"
    return 0

if __name__ == "__main__":
    sys.exit(main())
