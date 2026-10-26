#!/usr/bin/env python3
"""Rank S5 AND obligations using only the certified S7->S6 WIN witness pool.

This is a *frontier*, not an S5 verdict. The 17 historical S7 WIN roots
are a frozen comparison baseline; their terminal proofs are not rerun here.
Run verify.py --negative before treating the new S7 root as terminal-proved.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

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

# Existing independent terminal-only S5 certificates (K0423). A proof-only
# S6-WIN coverage gap is NOT an undecided S5 verdict.
K0423_PILOTS = (
    (558600, (40, 48, 60, 72, 80), 2,
     'bbe374db319d9aeb95bbe540fbcae13005b5fa9351215a5ae1e732b87c553bce',
     270545, 426376, 28813),
    (209644, (49, 55, 60, 65, 71), 1,
     'e89bb8010597058607699590f0e30a9ad817012971c3265614c0ba09d70b08a4',
     349157, 518252, 50131),
)


def certified_s5_from_k0423(geometry, *, tamper=False):
    base = (Path(__file__).resolve().parent.parent /
            'n11-s5-s6-quotient-20261013' / 'output')
    known = {}
    for index, points, verdict, certificate_sha, nodes, edges, terminals in K0423_PILOTS:
        receipt = json.loads(
            (base / f'pilot-{index}-terminal-verification.json').read_text(
                encoding='utf-8'))
        if tamper and index == 558600:
            receipt['verdict'] = 1
        board = sum(1 << p for p in points)
        need(int(receipt['root_mask']) == board and
             receipt['s5_index'] == index and
             receipt['verdict'] == verdict and
             receipt['trusted_leaves'] == 0 and
             receipt['certificate_sha256'] == certificate_sha and
             (receipt['nodes'], receipt['edges'], receipt['terminal_nodes'])
             == (nodes, edges, terminals),
             'K0423 terminal certificate receipt mismatch')
        need(board.bit_count() == 5 and geometry.safe(board) and
             geometry.canonical(board) == board,
             'K0423 S5 root is not canonical and safe')
        known[f'{board:032x}'] = 'WIN' if verdict == 1 else 'LOSS'
    need(len(known) == 2, 'K0423 certified S5 roots duplicated')
    return known


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

    # The original 14-gap "best" root is already independently proved
    # original-first LOSS in K0423. Exclude it BEFORE scheduling work.
    certified = certified_s5_from_k0423(geometry)
    excluded = [(gap, key, certified[key]) for
                gap, _, key, _, _ in records if key in certified]
    need(excluded == [(14, EXPECTED_TOP, 'LOSS')],
         'K0423 certified verdict collision / excluded frontier changed')
    remaining = [row for row in records if row[2] not in certified]
    filtered_missing_frequency = Counter(
        int(key, 16) for row in remaining for key in row[4])
    filtered_legal = sum(row[3] for row in remaining)
    filtered_missing = sum(row[0] for row in remaining)
    filtered_secured = filtered_legal - filtered_missing
    need(len(remaining) == 297 and remaining[0][0] == 27 and
         filtered_legal == 26451 and filtered_secured == 651 and
         filtered_missing == 25800 and
         len(filtered_missing_frequency) == 25307,
         'K0423-filtered frontier regression')
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
            in enumerate(remaining[:5])
        ],
        'excluded_original_top': {
            's5': EXPECTED_TOP, 'verdict': 'LOSS',
            'prior_proof_only_gap': 14,
            'certificate': 'K0423 / pilot-558600-terminal-dag.json.gz',
            'trusted_leaves': 0,
            'prior_gap_children_unique_within_298': True,
        },
        'k0423_certified_s5_exclusions': len(excluded),
        'after_k0423_filter_parent_classes': len(remaining),
        'after_k0423_filter_legal_edges': filtered_legal,
        'after_k0423_filter_secured_edges': filtered_secured,
        'after_k0423_filter_uncovered_edges': filtered_missing,
        'after_k0423_filter_distinct_uncovered_s6':
            len(filtered_missing_frequency),
        'after_k0423_filter_minimum_gap': remaining[0][0],
        'filter_limit': 'Only K0423 independent S5 verdicts; other known '
                        'S5 certificates and caches not yet reconciled',
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
                certified_s5_from_k0423(geometry, tamper=True)
            except ValueError:
                pass
            else:
                raise ValueError('tampered K0423 S5 receipt accepted')
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
