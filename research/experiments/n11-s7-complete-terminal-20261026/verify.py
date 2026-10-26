#!/usr/bin/env python3
"""Self-contained terminal minimax certificate for one N11 S7 first-WIN root.

Fixed original-first viewpoint: S7 is universal over S8; each S8 has
one S9 witness; each S9 is universal over its S10 children; each S10
is independently solved to terminal. Frozen outcome caches are NOT inputs.
"""
import argparse
import hashlib
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
ROOT = int('00000000000100001000000042401008', 16)
WITNESS_SHA = '86ecd320e36d2729b85110c30672d166f8b2db59d4f404811335f87242a33848'
S9_SHA = '4873850f91fe922203c9c1a92f5716145da69818887214bdd219652472cf8733'
S8_BOUNDARY_SHA = '1ffd660cb50315df4ca50c5c60ae97a7df1f4c9e7e7349ace4792f4a71c50a80'
S10_BOUNDARY_SHA = 'cb47d6e5b7428a9e3fd75f47822a7b5af4242bf2152897202f55d282a932e0eb'
LEAF_STATES_SHA = '72bc1ffc20b41db87645d01015e6ab9b2e7cff55960c8d5980d030dfb97eabd2'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SOURCE = load('n11_s7_complete_source',
              EXP / 'n11-s9-neighbor23-terminal-20261026' / 'verify.py')
GEOMETRIES = (SOURCE.THREE, SOURCE.FOUR)  # 3x3 and independent 4x4 Bareiss


def digest(values):
    return hashlib.sha256(''.join(f'{v:032x}\n' for v in sorted(values))
                          .encode('ascii')).hexdigest()


def read_certificate():
    witness_file = HERE / 's8-witness.tsv'
    s9_file = HERE / 's9-roots.keys'
    raw_rows, raw_s9 = witness_file.read_bytes(), s9_file.read_bytes()
    need(hashlib.sha256(raw_rows).hexdigest() == WITNESS_SHA,
         'S8 witness manifest SHA mismatch')
    need(hashlib.sha256(raw_s9).hexdigest() == S9_SHA,
         'S9 root manifest SHA mismatch')
    lines = raw_rows.decode('ascii').splitlines()
    s9_lines = raw_s9.decode('ascii').splitlines()
    need(len(lines) == 34 and len(s9_lines) == 17,
         'S7/S9 certificate manifest incomplete')
    rows = []
    for line in lines:
        fields = line.split()
        need(len(fields) == 2 and all(len(h) == 32 and
             set(h) <= set('0123456789abcdef') for h in fields),
             'invalid S8 witness row')
        rows.append(tuple(int(h, 16) for h in fields))
    need(all(len(h) == 32 and set(h) <= set('0123456789abcdef')
             for h in s9_lines), 'invalid S9 root key')
    need(lines == sorted(set(lines)) and
         s9_lines == sorted(set(s9_lines)), 'unsorted or duplicate manifest')
    return rows, [int(h, 16) for h in s9_lines]


def boundary(rows, s9_roots):
    """Geometry and full AND/OR boundaries, without trusting manifest sizes."""
    need(len(rows) == 34 and len(s9_roots) == 17,
         'missing S8 obligation or S9 witness')
    need(len({b for b, _ in rows}) == len(rows) and
         len(set(s9_roots)) == len(s9_roots), 'duplicate certificate node')
    need({w for _, w in rows} == set(s9_roots),
         'unused or missing S9 witness')
    need(digest(b for b, _ in rows) == S8_BOUNDARY_SHA,
         'changed S8 obligation boundary')
    for geom in GEOMETRIES:
        need(ROOT.bit_count() == 7 and geom.safe(ROOT) and
             geom.canonical(ROOT) == ROOT, 'invalid S7 root')
        actual8 = SOURCE.children(geom, ROOT)
        need(len(actual8) == 34 and actual8 == {b for b, _ in rows},
             'incomplete S7 universal S8 boundary')
        for s8, s9 in rows:
            need(s8.bit_count() == 8 and geom.safe(s8) and
                 geom.canonical(s8) == s8, 'invalid S8 child')
            need(s9.bit_count() == 9 and geom.safe(s9) and
                 geom.canonical(s9) == s9, 'invalid S9 witness')
            need(s9 in SOURCE.children(geom, s8),
                 'S8 witness is not a legal S9 child')
        leaves, edges = set(), 0
        for s9 in s9_roots:
            actual10 = SOURCE.children(geom, s9)
            edges += len(actual10)
            leaves.update(actual10)
        need(edges == 360 and len(leaves) == 360 and
             digest(leaves) == S10_BOUNDARY_SHA,
             'incomplete S9 universal S10 boundary')
        for s10 in leaves:
            need(s10.bit_count() == 10 and geom.safe(s10) and
                 geom.canonical(s10) == s10, 'invalid S10 terminal leaf')
        parents6 = {geom.canonical(ROOT ^ (1 << p))
                    for p in geom.points(ROOT)}
        need(len(parents6) == 7 and all(ROOT in SOURCE.children(geom, p)
            for p in parents6), 'invalid reverse S6 WIN witness boundary')
    return sorted(leaves)


def verify(negative=False):
    rows, s9_roots = read_certificate()
    leaves = boundary(rows, s9_roots)
    if negative:
        # Semantic rejections, independent of the raw manifest SHA checks.
        bad = [
            (rows[:-1], s9_roots),
            (rows + [rows[-1]], s9_roots),
            ([(rows[0][0], rows[0][0])] + rows[1:], s9_roots),
            ([(rows[0][0] ^ 1, rows[0][1])] + rows[1:], s9_roots),
            (rows, s9_roots[:-1]),
            (rows, s9_roots + [s9_roots[-1]]),
        ]
        for wrong_rows, wrong_s9 in bad:
            try:
                boundary(wrong_rows, wrong_s9)
            except ValueError:
                continue
            raise ValueError('tampered certificate boundary accepted')
    solvers = [SOURCE.terminal_solver(geom) for geom in GEOMETRIES]
    state_rows = []
    totals = [0, 0]
    for s10 in leaves:
        verdicts = [solver(s10) for solver in solvers]
        need(all(verdict for verdict, _ in verdicts),
             f'S10 terminal leaf not original-first WIN: {s10:032x}')
        need(verdicts[0][1] == verdicts[1][1],
             f'independent per-leaf state mismatch: {s10:032x}')
        legal = [geom.legal(s10) for geom in GEOMETRIES]
        need(legal[0] == legal[1],
             f'independent S10 legal moves mismatch: {s10:032x}')
        for i in range(2):
            totals[i] += verdicts[i][1]
        state_rows.append(f'{s10:032x} {verdicts[0][1]} '
                          f'{legal[0].bit_count()}\n')
    need(totals == [28029, 28029], 'independent terminal state regression')
    need(hashlib.sha256(''.join(state_rows).encode('ascii')).hexdigest()
         == LEAF_STATES_SHA, 'terminal per-leaf fingerprint mismatch')
    print('VERIFIED N11 S7 original-first WIN: 34/34 S8 obligations, '
          '17 distinct S9 witnesses, 360 S9->S10 incidences, '
          '360 distinct terminal S10 WIN leaves, '
          '28029 states per independent solver, 7 S6 WIN parents; '
          'two-stone root and empty board UNKNOWN')
    if negative:
        print('PASS six semantic boundary mutation rejections')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--negative', action='store_true')
    verify(parser.parse_args().negative)
