#!/usr/bin/env python3
"""Rank S5 AND obligations using only the certified S7->S6 WIN witness pool.

This is a *frontier*, not an S5 verdict. The 17 historical S7 WIN roots
are a frozen comparison baseline; their terminal proofs are not rerun here.
Run verify.py --negative before treating the new S7 root as terminal-proved.
"""
import argparse
from collections import Counter
import json

import s6_win_lift_audit as lift

EXPECTED_TOP = '00000000000101001001010000000000'
EXPECTED_MISSING = (
    '00000000000101001001010000000002',
    '00000000000101001001010000000004',
    '00000000000101001001010000000020',
    '00000000000101001001010000000040',
    '00000000000101001001010000000080',
    '00000000000101001001010000000200',
    '00000000000101001001010000002000',
    '00000000000101001001010000008000',
    '00000000000101001001010000010000',
    '00000000000101001001010000040000',
    '00000000000101001001010000080000',
    '00000000000101001001010004000000',
    '00000000000101001001010020000000',
    '00000000000101001001014000000000',
)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def enumerate_frontier(geometry, old_roots, *, tamper=False):
    lift_result = lift.audit_geometry(geometry, old_roots)
    known6 = lift_result['old_s6'] | lift_result['new_s6']
    parents5 = lift_result['old_s5'] | lift_result['new_s5']
    if tamper:
        # A missing certified S6 witness must invalidate the fixed census.
        known6 = known6 - {min(lift_result['new_s6'])}
    records = []
    missing_frequency = Counter()
    for parent in parents5:
        legal6 = lift.children(geometry, parent)
        secured = legal6 & known6
        missing = legal6 - known6
        missing_frequency.update(missing)
        records.append((len(missing), -len(secured), f'{parent:032x}',
                        len(legal6), tuple(f'{v:032x}' for v in sorted(missing))))
    records.sort()
    total_legal = sum(row[3] for row in records)
    total_missing = sum(row[0] for row in records)
    total_secured = total_legal - total_missing
    top = records[0]
    top_missing = top[4]
    need(len(records) == 298 and total_legal == 26468 and
         total_secured == 654 and total_missing == 25814,
         'S5 legal / secured / missing incidence regression')
    need(len(missing_frequency) == 25321 and
         max(missing_frequency.values()) == 2,
         'S5 missing-S6 sharing regression')
    need(top[:4] == (14, -3, EXPECTED_TOP, 17) and
         top_missing == EXPECTED_MISSING and
         records[1][0] == 27 and
         all(missing_frequency[int(key, 16)] == 1 for key in top_missing),
         'S5 near-closure priority regression')
    need(all(row[0] > 0 for row in records),
         'S5 all-child proof must not be inferred from partial coverage')
    return {
        'parent_classes': len(records),
        'legal_s5_to_s6_class_edges': total_legal,
        'secured_s5_to_s6_win_witness_edges': total_secured,
        'uncovered_s5_to_s6_class_edges': total_missing,
        'distinct_uncovered_s6_classes': len(missing_frequency),
        'maximum_missing_s6_parent_reuse': max(missing_frequency.values()),
        'top': [
            {'s5': key, 'legal_s6': legal, 'secured_s6': -neg_secured,
             'uncovered_s6': gap,
             'missing_s6': list(missing) if i == 0 else []}
            for i, (gap, neg_secured, key, legal, missing)
            in enumerate(records[:5])
        ],
        'top_missing_s6_shared_with_other_297_parents': 0,
        'new_s5_win_proofs': 0,
        'two_stone_root_new_closures': 0,
        'empty_board': 'UNKNOWN',
    }


def main(negative=False):
    proof = lift.load_proof()
    need(proof.ROOT == lift.NEW_ROOT, 'S7 proof root changed')
    rows, witnesses = proof.read_certificate()
    proof.boundary(rows, witnesses)
    old_roots = lift.read_frozen(lift.FROZEN.read_bytes())
    reports = [enumerate_frontier(geometry, old_roots)
               for geometry in proof.GEOMETRIES]
    need(reports[0] == reports[1],
         '3x3 determinant / independent 4x4 Bareiss frontier mismatch')
    if negative:
        for geometry in proof.GEOMETRIES:
            try:
                enumerate_frontier(geometry, old_roots, tamper=True)
            except ValueError:
                continue
            raise ValueError('removed certified S6 WIN witness was accepted')
    print(json.dumps(reports[0], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--negative', action='store_true')
    main(parser.parse_args().negative)
