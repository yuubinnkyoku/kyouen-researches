#!/usr/bin/env python3
"""N11: independently audit the S7 WIN -> S6 WIN -> S5 edge lift.

Only S7 WIN -> S6 WIN (even OR) is a verdict implication.
S5 AND cannot be called WIN from a subset of S6 WIN children.
The historical 17-root list is a comparison baseline, not 17 newly
independently terminal-verified proofs.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
FROZEN = EXP / 'n11-targeted-terminal-lift-20261015' / 'data' / 'all_s7_win_17.txt'
FROZEN_SHA = '17282f84fd65ad20ac58ef794449a52bcc796d8129a1a3a58d726a305fbeb21e'
NEW_ROOT = int('00000000000100001000000042401008', 16)
KNOWN_S6_LOSS = int('00000000040004001004000004010000', 16)


def need(ok, why):
    if not ok:
        raise ValueError(why)


def load_proof():
    filename = HERE / 'verify.py'
    spec = importlib.util.spec_from_file_location('n11_s7_lift_proof', filename)
    proof = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(proof)
    return proof


def read_frozen(raw):
    need(hashlib.sha256(raw).hexdigest() == FROZEN_SHA,
         'historical S7 WIN baseline SHA-256 changed')
    lines = raw.decode('ascii').splitlines()
    need(len(lines) == 17 and lines == sorted(set(lines)),
         'historical S7 WIN baseline missing/duplicated/unsorted')
    need(all(len(x) == 32 and set(x) <= set('0123456789abcdef')
             for x in lines), 'invalid historical S7 key')
    return [int(x, 16) for x in lines]


def reverse(geometry, boards):
    return {geometry.canonical(b ^ (1 << p))
            for b in boards for p in geometry.points(b)}


def children(geometry, board):
    moves = geometry.legal(board)
    return {geometry.canonical(board | (1 << p))
            for p in geometry.points(moves)}


def audit_geometry(geometry, old_roots):
    for b in [*old_roots, NEW_ROOT]:
        need(b.bit_count() == 7 and geometry.safe(b) and
             geometry.canonical(b) == b, 'invalid S7 root')
    need(NEW_ROOT not in old_roots, 'new S7 root already in frozen baseline')
    old6 = reverse(geometry, old_roots)
    new6 = reverse(geometry, [NEW_ROOT])
    all6 = old6 | new6
    need(len(old6) == 103 and len(new6) == 7 and
         not (old6 & new6) and len(all6) == 110,
         'S6 WIN witness union changed')
    need(KNOWN_S6_LOSS not in all6, 'independent S6 LOSS conflict')
    for b in all6:
        need(b.bit_count() == 6 and geometry.safe(b) and
             geometry.canonical(b) == b, 'invalid S6 parent')
    for b in new6:
        need(NEW_ROOT in children(geometry, b),
             'S6 parent lacks legal S7 WIN witness')

    old5 = reverse(geometry, old6)
    new5 = reverse(geometry, new6)
    all5 = old5 | new5
    need(len(old5) == 277 and len(new5) == 21 and
         not (old5 & new5) and len(all5) == 298,
         'S5 parent union changed')

    def covered_edges(parents, known_win6):
        edges = set()
        gaps = {}
        for b in parents:
            need(b.bit_count() == 5 and geometry.safe(b) and
                 geometry.canonical(b) == b, 'invalid S5 parent')
            actual = children(geometry, b)
            covered = actual & known_win6
            gaps[b] = len(actual) - len(covered)
            edges.update((b, c) for c in covered)
        return edges, gaps

    old_edges, _ = covered_edges(old5, old6)
    all_edges, gaps = covered_edges(all5, all6)
    added_edges = all_edges - old_edges
    need(len(old_edges) == 612 and len(all_edges) == 654 and
         len(added_edges) == 42 and
         {a for a, _ in added_edges} == new5 and
         {b for _, b in added_edges} == new6 and
         all(b in new6 for _, b in added_edges),
         'certified S5->S6 edge increment changed')
    need(min(gaps.values()) == 14 and all(g > 0 for g in gaps.values()),
         'S5 gap regression: no all-child S5 WIN proof is claimed')
    return {
        'old_s6': old6, 'new_s6': new6, 'old_s5': old5, 'new_s5': new5,
        'added_edges': added_edges, 'minimum_s5_uncovered': min(gaps.values()),
    }


def audit(negative=False):
    proof = load_proof()
    need(proof.ROOT == NEW_ROOT, 'source S7 terminal root changed')
    rows, witnesses = proof.read_certificate()
    proof.boundary(rows, witnesses)  # all 34/17/360 structural obligations
    raw = FROZEN.read_bytes()
    frozen = read_frozen(raw)
    outcomes = [audit_geometry(geom, frozen) for geom in proof.GEOMETRIES]
    need(outcomes[0] == outcomes[1],
         '3x3 determinant / 4x4 Bareiss S6/S5 audit mismatch')
    if negative:
        tests = [raw[:-1], raw.replace(b'00000000000000821080000002001020',
                                       b'00000000000000821080000002001021')]
        for tampered in tests:
            try:
                read_frozen(tampered)
            except (ValueError, UnicodeDecodeError):
                continue
            raise ValueError('modified historical baseline accepted')
        for geom in proof.GEOMETRIES:
            try:
                audit_geometry(geom, [NEW_ROOT, *frozen[1:]])
            except ValueError:
                continue
            raise ValueError('overlapping S7 witness accepted')
    result = outcomes[0]
    return {
        'source': 'independently terminal-verified S7 WIN proof, 34/34 S8 children',
        'comparison': '2026-10-15 frozen S7 WIN list; historical verdict provenance',
        'frozen_s7_win_roots': len(frozen),
        'new_terminal_s7_win_roots': 1,
        'frozen_s6_win_witness_parents': len(result['old_s6']),
        'new_s6_win_witness_parents': len(result['new_s6']),
        'new_s6_vs_frozen_overlap': 0,
        's6_win_witness_parents_union': 110,
        'frozen_s5_incident_parents': len(result['old_s5']),
        'new_s5_incident_parents': len(result['new_s5']),
        's5_incident_parents_union': 298,
        'frozen_s5_to_s6_witness_class_edges': 612,
        'new_s5_to_s6_certified_win_edges': len(result['added_edges']),
        's5_to_s6_witness_class_edges_union': 654,
        'minimum_uncovered_s6_children_among_298_s5_parents':
            result['minimum_s5_uncovered'],
        'new_s6_keys': [f'{b:032x}' for b in sorted(result['new_s6'])],
        'new_s5_keys': [f'{b:032x}' for b in sorted(result['new_s5'])],
        'new_s5_win_proofs': 0,
        'new_two_stone_root_closures': 0,
        'empty_board': 'UNKNOWN',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--negative', action='store_true')
    print(json.dumps(audit(parser.parse_args().negative),
                     ensure_ascii=False, indent=2))
