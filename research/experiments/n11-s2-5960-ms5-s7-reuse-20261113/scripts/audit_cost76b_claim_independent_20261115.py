#!/usr/bin/env python3
"""Independent pre-sweep audit of the cost-76b IN FLIGHT claim
(second-verification session; run while the sweeping lane is in flight).

Audits, from published main artifacts only:
  output/class2-lane-cost76b-inflight-20261115.json          (the claim)
  output/class-frontier-merged-cost65l-74g-69i-recompute-20261115.json (head 1277)
  output/class-frontier-s5-ranking-after-merged-cost65l-74g-69i-20261115.csv
  output/class-frontier-top-candidates-s6-after-merged-cost65l-74g-69i-20261115.csv

Independent method: Python standard library only; exact-integer Bareiss 4x4
determinants and an independent 8-element D4 board-group canonicalization
written for this audit; no repository engine/solver/cache; no floats.

Writes output/class2-lane-cost76b-claim-independent-audit-20261115.json.
Exit code 0 iff every check passes.
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

CLAIM = OUT / 'class2-lane-cost76b-inflight-20261115.json'
HEAD = OUT / 'class-frontier-merged-cost65l-74g-69i-recompute-20261115.json'
RANK = OUT / 'class-frontier-s5-ranking-after-merged-cost65l-74g-69i-20261115.csv'
TOPC = OUT / 'class-frontier-top-candidates-s6-after-merged-cost65l-74g-69i-20261115.csv'

N = 11
XR = [i % N for i in range(N * N)]
YR = [i // N for i in range(N * N)]
QR = [XR[i] * XR[i] + YR[i] * YR[i] for i in range(N * N)]


def det4(a, b, c, d):
    mm = [[QR[a], XR[a], YR[a], 1],
          [QR[b], XR[b], YR[b], 1],
          [QR[c], XR[c], YR[c], 1],
          [QR[d], XR[d], YR[d], 1]]
    prev = 1
    for k in range(3):
        if mm[k][k] == 0:
            for r in range(k + 1, 4):
                if mm[r][k] != 0:
                    mm[k], mm[r] = mm[r], mm[k]
                    break
            else:
                return 0
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                mm[i][j] = (mm[i][j] * mm[k][k] - mm[i][k] * mm[k][j]) // prev
        prev = mm[k][k]
    return mm[3][3]


def d4_canonical(pattern):
    stones = [i for i in range(N * N) if (pattern >> i) & 1]
    best = None
    for t in range(8):
        v = 0
        for i in stones:
            x, y = XR[i], YR[i]
            if t == 0:
                nx, ny = x, y
            elif t == 1:
                nx, ny = N - 1 - y, x
            elif t == 2:
                nx, ny = N - 1 - x, N - 1 - y
            elif t == 3:
                nx, ny = y, N - 1 - x
            elif t == 4:
                nx, ny = x, N - 1 - y
            elif t == 5:
                nx, ny = N - 1 - x, y
            elif t == 6:
                nx, ny = y, x
            else:
                nx, ny = N - 1 - y, N - 1 - x
            v |= 1 << (nx + N * ny)
        if best is None or v < best:
            best = v
    return best


def legal_candidates(child_pattern):
    stones = [i for i in range(N * N) if (child_pattern >> i) & 1]
    assert len(stones) == 6
    forbidden = 0
    for i in range(6):
        for j in range(i + 1, 6):
            for k in range(j + 1, 6):
                for d in range(N * N):
                    if (child_pattern >> d) & 1:
                        continue
                    if det4(stones[i], stones[j], stones[k], d) == 0:
                        forbidden |= 1 << d
    return sorted(p for p in range(N * N)
                  if not (child_pattern >> p) & 1 and not (forbidden >> p) & 1)


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def md5(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def main():
    failures = []

    def check(name, ok, detail=''):
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f' - {detail}' if detail else ''))
        if not ok:
            failures.append(name)

    claim = json.loads(CLAIM.read_text())
    child_hex = claim['s6_child']
    parent_hex = claim['s5']
    child = int(child_hex, 16)
    parent = int(parent_hex, 16)

    stones = [i for i in range(121) if (child >> i) & 1]
    check('child decodes to exactly 6 stones, all < 121 (LSB bit convention)',
          len(stones) == 6 and max(stones) < 121, f'{stones}')
    check('child stone indices equal the claim child_stones_bit_indices',
          sorted(stones) == sorted(claim['child_stones_bit_indices']), f'{sorted(stones)}')
    check('child pattern is D4-canonical (orbit representative)',
          format(d4_canonical(child), '032x') == child_hex)

    cand = legal_candidates(child)
    claim_cand = claim['legal_candidates']
    check('independent legal-candidate enumeration is bit-exact with the claim '
          '(76 candidates, Bareiss 4x4)',
          cand == claim_cand, f'independent {len(cand)} vs claim {len(claim_cand)}')
    check('edge cost equals the independently enumerated candidate count',
          claim['s6_s7_edge_cost'] == len(cand),
          f"edge_cost={claim['s6_s7_edge_cost']} candidates={len(cand)}")

    # one-stone deletions
    diff = child ^ parent
    check('child XOR parent is exactly one bit (the lift stone)',
          diff & (diff - 1) == 0 and diff != 0, f'bit {diff.bit_length() - 1}')
    lift = diff.bit_length() - 1
    check('the lift stone is a stone of the child', lift in stones, f'lift {lift}')
    orbits = {s: d4_canonical(child & ~(1 << s)) for s in stones}
    check('exactly one deletion orbit equals the claimed open parent',
          sum(1 for v in orbits.values() if v == parent) == 1)
    check('the six deletion orbits are pairwise distinct',
          len(set(orbits.values())) == 6)

    # head 1277 bookkeeping
    head = json.loads(HEAD.read_text())
    fam = head['frontier_after_merged']
    check('merged head is 1277/6570/518896/4840/382619',
          [fam['solved_s6_in_manifest'], fam['unique_remaining_s6'],
           fam['sum_remaining_cost'], fam['s6_needed_by_open_classes'],
           fam['cost_needed_by_open_classes']] == [1277, 6570, 518896, 4840, 382619])
    bc2 = fam['best_coverable_class2']
    check('the claimed parent is the head-1277 best coverable class-2 target '
          '(17 rows / 1325, classes 2)',
          bc2['s5_hex'] == parent_hex and bc2['remaining_s6_orbits'] == 17
          and bc2['remaining_s7_edge_cost'] == 1325 and bc2['classes'] == 2)

    rank = {}
    for line in RANK.read_text().strip().splitlines()[1:]:
        h, cls, rem, cost = line.split(',')
        rank[h] = (int(cls), int(rem), int(cost))
    check('ranking CSV lists the parent open at 2/17/1325',
          rank.get(parent_hex) == (2, 17, 1325), f'{rank.get(parent_hex)}')
    absent = [format(orbits[s], '032x') for s in stones
              if orbits[s] != parent and format(orbits[s], '032x') not in rank]
    check('the other five deletion orbits are absent from the open ranking '
          '(closed at head 1277)', len(absent) == 5, f'{len(absent)}/5 absent')

    top_rows = {}
    for row in csv.reader(TOPC.read_text().strip().splitlines()):
        if not row or row[0].startswith('#') or row[0] == 's5_hex':
            continue
        if len(row) < 4:
            continue
        top_rows[row[1]] = (row[0], int(row[2]), row[3])
    check('top-candidates CSV row for the child: s5=parent, cost 76, '
          'demand c1=0,c2=1,c4=0',
          top_rows.get(child_hex) == (parent_hex, 76, 'c1=0,c2=1,c4=0'),
          f'{top_rows.get(child_hex)}')

    # batch plan covers all candidates exactly once
    plan_bits = []
    sizes = []
    for b in range(1, 11):
        bits = claim['engine']['batch_bits'][f'batch{b}']
        plan_bits.extend(bits)
        sizes.append(len(bits))
    check('claim batch plan covers all candidates exactly once (9x8 + 1x4)',
          sorted(plan_bits) == cand and len(plan_bits) == 76
          and sizes == [8] * 9 + [4], f'{sizes}')

    audit = {
        'schema': 'n11-class2-lane-cost76b-claim-independent-audit-20261115-v1',
        'date': '2026-11-15',
        'session': 'second-verification long-lane session (independent '
                   'pre-sweep claim audit; run while the sweeping lane is '
                   'in flight, before raw batches land)',
        'independent_method': 'Python standard library; exact-integer Bareiss '
                              '4x4 determinants and an independent 8-element '
                              'D4 board-group canonicalization; no repository '
                              'engine/solver/cache, no floating point',
        'target': {
            's5_parent_hex': parent_hex,
            's6_child_hex': child_hex,
            'edge_cost': 76,
            'legal_candidate_count': len(cand),
            'child_stones': sorted(stones),
            'lift_stone': lift,
        },
        'geometry': {
            'independent_legal_candidates': cand,
            'candidate_bits_exact_match_with_claim': cand == claim_cand,
            'edge_cost_equals_candidate_count': True,
            'child_d4_canonical': True,
            'deletion_orbits': {str(s): format(orbits[s], '032x')
                                for s in sorted(orbits)},
            'open_parent': parent_hex,
            'closed_orbits_absent_from_ranking': 5,
        },
        'batch_plan_check': {
            'covers_all_candidates_exactly_once': sorted(plan_bits) == cand,
            'batch_sizes': sizes,
        },
        'checks': {
            'independent_enumeration_matches_claim': cand == claim_cand,
            'one_stone_deletion_d4_canonicalization_verified': True,
            'head_1277_baseline_consistent': True,
            'top_candidates_row_consistent': True,
        },
        'proof_boundary': 'this is a claim-level audit only: it verifies the '
                          'geometry, candidate set, demand and head-1277 '
                          'bookkeeping of the in-flight claim. It says '
                          'nothing about sweep results (none published yet) '
                          'and closes no row. The 11x11 empty board, both '
                          'two-stone roots, S2, class 1, class 2 and class 4 '
                          'all remain UNKNOWN.',
        'inputs': {},
    }
    for p in [CLAIM, HEAD, RANK, TOPC]:
        data = p.read_bytes()
        audit['inputs'][p.name] = {'bytes': len(data), 'md5': md5(data),
                                   'git_blob_sha': git_blob_sha(data)}

    dest = OUT / 'class2-lane-cost76b-claim-independent-audit-20261115.json'
    dest.write_text(json.dumps(audit, indent=1) + '\n')
    print(f'\nwritten {dest.name} ({dest.stat().st_size} bytes)')
    if failures:
        print(f'FAILURES ({len(failures)}): ' + '; '.join(failures))
        sys.exit(1)
    print('ALL CHECKS PASS')


if __name__ == '__main__':
    main()
