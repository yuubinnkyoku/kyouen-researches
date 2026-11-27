#!/usr/bin/env python3
"""split_piece.py — sound leftmost-column case split of a row-exact CNF piece.

Reads a DIMACS CNF produced by sat4.js --rspec for the three-row q=4 lane and
writes sub-pieces, one per column c of the deficient row Y (which the rspec
constrains to exactly k >= 1 stones):
  piece_c = base CNF + unit clauses:
      cell(Y, c) = 1        (leftmost stone at column c)
      cell(Y, c') = 0  for all c' < c
Completeness: every model of the base CNF has a unique leftmost stone column in
row Y, so it belongs to exactly one piece. Soundness: each piece only conjoins
unit literals on existing cell variables (cell[i] = i+1, row-major, per
encodeCore: cell vars are allocated first).
Usage: split_piece.py base.cnf m rowY outdir prefix
"""
import os
import sys

def main():
    base, m, rowY, outdir, prefix = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
    os.makedirs(outdir, exist_ok=True)
    with open(base) as f:
        lines = f.read().split('\n')
    hdr_i = next(i for i, l in enumerate(lines) if l.startswith('p cnf'))
    parts = lines[hdr_i].split()
    nv, nc = int(parts[2]), int(parts[3])
    body = lines[hdr_i + 1:]
    pieces = []
    for c in range(m):
        units = [str(rowY * m + c + 1)]
        for c2 in range(c):
            units.append(str(-(rowY * m + c2 + 1)))
        out = os.path.join(outdir, '%s_c%02d.cnf' % (prefix, c))
        with open(out, 'w') as g:
            g.write('p cnf %d %d\n' % (nv, nc + len(units)))
            g.write('\n'.join(body))
            if not '\n'.join(body).endswith('\n'):
                g.write('\n')
            for u in units:
                g.write('%s 0\n' % u)
        pieces.append(out)
    print('\n'.join(pieces))

if __name__ == '__main__':
    main()
