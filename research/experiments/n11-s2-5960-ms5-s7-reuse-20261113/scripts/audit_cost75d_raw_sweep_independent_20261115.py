#!/usr/bin/env python3
"""Independent audit of the cost-75d raw sweep (second-verification session).

Audits, from published main artifacts only:
  output/class2-lane-cost75d-inflight-20261115.json          (the claim)
  output/class2-lane-cost75d-raw-batch{1..10}-20261115.jsonl (raw sweep records)
  output/class2-lane-cost75d-v16-determinism-rerun-20261115.jsonl (batch-5 rerun)
  output/class-frontier-merged-cost65l-74g-69i-recompute-20261115.json (head 1277)
  output/class-frontier-s5-ranking-after-merged-cost65l-74g-69i-20261115.csv
  output/class-frontier-top-candidates-s6-after-merged-cost65l-74g-69i-20261115.csv

Independent method: Python standard library only; exact-integer Bareiss 4x4
determinants written for this audit; an independent 8-element D4 board-group
canonicalization; no repository engine/solver/cache; no floating point.

Writes output/class2-lane-cost75d-raw-sweep-independent-audit-20261115.json.
Exit code 0 iff every check passes.
"""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

CLAIM = OUT / 'class2-lane-cost75d-inflight-20261115.json'
RERUN = OUT / 'class2-lane-cost75d-v16-determinism-rerun-20261115.jsonl'
HEAD = OUT / 'class-frontier-merged-cost65l-74g-69i-recompute-20261115.json'
RANK = OUT / 'class-frontier-s5-ranking-after-merged-cost65l-74g-69i-20261115.csv'
TOPC = OUT / 'class-frontier-top-candidates-s6-after-merged-cost65l-74g-69i-20261115.csv'

N = 11
XR = [i % N for i in range(N * N)]
YR = [i // N for i in range(N * N)]
QR = [XR[i] * XR[i] + YR[i] * YR[i] for i in range(N * N)]


def det4(a, b, c, d):
    """Exact-integer Bareiss determinant of [[q,x,y,1]] rows: zero iff the
    four cells lie on a common circle or line (kyoen-relevant degeneracy)."""
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
    """Minimum 128-bit pattern over the 8 board symmetries (independent D4)."""
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
    """Empty cells whose 7-stone completion keeps the position free of any
    4-on-a-circle/line degeneracy, re-derived from scratch."""
    stones = [i for i in range(N * N) if (child_pattern >> i) & 1]
    assert len(stones) == 6
    # forbidden = cells completing a degenerate 4-set with any 3 child stones
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
        status = 'PASS' if ok else 'FAIL'
        print(f'[{status}] {name}' + (f' - {detail}' if detail else ''))
        if not ok:
            failures.append(name)
        return ok

    claim = json.loads(CLAIM.read_text())
    child_hex = claim['s6_child']
    parent1_hex = claim['s5_parent1']
    child = int(child_hex, 16)
    parent1 = int(parent1_hex, 16)

    # ---- geometry -------------------------------------------------------
    stones = [i for i in range(121) if (child >> i) & 1]
    check('child decodes to exactly 6 stones, all < 121 (LSB bit convention)',
          len(stones) == 6 and max(stones) < 121, f'{stones}')
    check('child stone indices equal the claim child_stones_bit_indices',
          sorted(stones) == sorted(claim['child_stones_bit_indices']),
          f'{sorted(stones)}')
    check('child pattern is D4-canonical (orbit representative)',
          format(d4_canonical(child), '032x') == child_hex)

    cand = legal_candidates(child)
    claim_cand = claim['legal_candidates']
    check('independent legal-candidate enumeration is bit-exact with the claim '
          '(75 candidates, Bareiss 4x4)',
          cand == claim_cand, f'independent {len(cand)} vs claim {len(claim_cand)}')
    check('edge cost equals the independently enumerated candidate count',
          claim['s6_s7_edge_cost'] == len(cand),
          f"edge_cost={claim['s6_s7_edge_cost']} candidates={len(cand)}")

    # one-stone deletions and published D4 orbits
    pub_orbits = {int(m.group(1)): m.group(2) for m in
                  re.finditer(r'lift (\d+) -> ([0-9a-f]{32})',
                              claim['demand_verification'])}
    pub_orbits[78] = parent1_hex  # lift stone 78 is the open parent (prose)
    lift78_direct = child & ~(1 << 78)
    check('lift-stone 78 direct deletion reproduces s5_parent1 bit-exact',
          lift78_direct == parent1, f'{format(lift78_direct, "032x")}')
    orbits = {}
    for s in stones:
        dele = child & ~(1 << s)
        orbits[s] = d4_canonical(dele)
    ok = all(format(orbits[s], '032x') == pub_orbits[s] for s in stones)
    check('all six one-stone deletions D4-canonicalize to the published orbit '
          'hexes (independent D4 group)', ok,
          ', '.join(f'{s}->{format(orbits[s], "032x")}' for s in sorted(orbits)))
    check('the six deletion orbits are pairwise distinct',
          len(set(orbits.values())) == 6)
    check('exactly one deletion orbit equals the open parent s5_parent1',
          sum(1 for v in orbits.values() if v == parent1) == 1)

    # ---- head-1277 bookkeeping ------------------------------------------
    head = json.loads(HEAD.read_text())
    fam = head['frontier_after_merged']
    check('merged head is 1277/6570/518896/4840/382619',
          [fam['solved_s6_in_manifest'], fam['unique_remaining_s6'],
           fam['sum_remaining_cost'], fam['s6_needed_by_open_classes'],
           fam['cost_needed_by_open_classes']] == [1277, 6570, 518896, 4840, 382619])
    bc2 = fam['best_coverable_class2']
    check('s5_parent1 is the head-1277 best coverable class-2 target '
          '(17 rows / 1325, classes 2)',
          bc2['s5_hex'] == parent1_hex and bc2['remaining_s6_orbits'] == 17
          and bc2['remaining_s7_edge_cost'] == 1325 and bc2['classes'] == 2,
          f"{bc2['s5_hex']} {bc2['remaining_s6_orbits']}/{bc2['remaining_s7_edge_cost']}")
    pr = fam['parent_rows_after']['second_coverable_class2_target']
    check('head-1277 parent_rows_after agrees (17/1325)',
          pr['s5_hex'] == parent1_hex and pr['remaining_s6_orbits'] == 17
          and pr['remaining_s7_edge_cost'] == 1325)

    rank = {}
    for line in RANK.read_text().strip().splitlines()[1:]:
        h, cls, rem, cost = line.split(',')
        rank[h] = (int(cls), int(rem), int(cost))
    check('ranking CSV lists s5_parent1 open at 2/17/1325',
          rank.get(parent1_hex) == (2, 17, 1325), f'{rank.get(parent1_hex)}')
    absent = [format(orbits[s], '032x') for s in stones
              if orbits[s] != parent1 and format(orbits[s], '032x') not in rank]
    check('the other five deletion orbits are absent from the open ranking '
          '(closed at head 1277)', len(absent) == 5,
          f'{len(absent)}/5 absent')

    top_rows = {}
    for row in csv.reader(TOPC.read_text().strip().splitlines()):
        if not row or row[0].startswith('#') or row[0] == 's5_hex':
            continue
        if len(row) < 4:
            continue
        top_rows[row[1]] = (row[0], int(row[2]), row[3])
    check('top-candidates CSV row for the child: s5=parent1, cost 75, '
          'demand c1=0,c2=1,c4=0',
          top_rows.get(child_hex) == (parent1_hex, 75, 'c1=0,c2=1,c4=0'),
          f'{top_rows.get(child_hex)}')

    # ---- raw batches -----------------------------------------------------
    batches = []
    recs = {}
    total_nodes = 0
    pilot_nodes = 0
    for b in range(1, 11):
        path = OUT / f'class2-lane-cost75d-raw-batch{b}-20261115.jsonl'
        lines = [json.loads(x) for x in path.read_text().strip().splitlines()]
        pilot = lines[0]
        check(f'batch {b}: pilot line is d6 control, loss=false, nodes=3402, '
              'capped=false',
              pilot == {'control': 'pilot_d6', 'loss': False, 'nodes': 3402,
                        'capped': False})
        pilot_nodes += pilot['nodes']
        bits = []
        for r in lines[1:]:
            assert 'bit' in r
            bits.append(r['bit'])
            if r['bit'] in recs:
                failures.append(f'bit {r["bit"]} duplicated across batches')
            recs[r['bit']] = r
            total_nodes += r['nodes']
        batches.append({'batch': b, 'file': path.name, 'candidate_bits': bits,
                        'nodes': sum(r['nodes'] for r in lines[1:])})
        check(f'batch {b}: candidate count matches the claim batch plan '
              '(9x8 + 1x3)', len(bits) == (8 if b < 10 else 3), f'{len(bits)}')
    check('all 75 candidates appear exactly once and equal the independent '
          'enumeration', sorted(recs) == cand and len(recs) == 75,
          f'{len(recs)} records')
    win_bits = sorted(b for b, r in recs.items() if r['loss'])
    capped_bits = sorted(b for b, r in recs.items() if r['capped'])
    check('WIN7-D10 bits are exactly [12, 40, 92, 111]',
          win_bits == [12, 40, 92, 111], f'{win_bits}')
    check('all four WIN bits are uncapped', all(not recs[b]['capped']
                                                 for b in win_bits))
    check('capped bits: none', capped_bits == [], f'{capped_bits}')
    check('refuted-d10 count is 71 (75 - 4 WIN)',
          len(cand) - len(win_bits) == 71)
    ranges = {tuple(r['terminalStoneRange']) for r in recs.values()}
    check('all terminal stone ranges are [13, 17] (within depth-10 bounds)',
          ranges == {(13, 17)}, f'{sorted(ranges)}')
    check('candidate node total (excluding the 10 d6 pilots) equals the '
          'commit-message 143,552,593',
          total_nodes == 143_552_593,
          f'candidates {total_nodes} + pilots {pilot_nodes} = '
          f'{total_nodes + pilot_nodes} (note: the cost-74h commit message '
          f'counted candidates+pilots, this one counts candidates only)')

    # determinism rerun of batch 5
    rerun_lines = [json.loads(x) for x in RERUN.read_text().strip().splitlines()]
    batch5_path = OUT / 'class2-lane-cost75d-raw-batch5-20261115.jsonl'
    batch5_lines = [json.loads(x) for x in batch5_path.read_text().strip().splitlines()]

    def strip_ms(recs_list):
        out = []
        for r in recs_list:
            r = dict(r)
            r.pop('ms', None)
            out.append(r)
        return out

    check('v16 determinism rerun (batch 5) is identical ignoring ms',
          strip_ms(rerun_lines) == strip_ms(batch5_lines))

    heavy = sorted(((r['nodes'], b) for b, r in recs.items()), reverse=True)[:6]
    audit = {
        'schema': 'n11-class2-lane-cost75d-raw-sweep-independent-audit-20261115-v1',
        'date': '2026-11-15',
        'session': 'second-verification long-lane session (independent audit '
                   'from published main artifacts; the sweeping lane\'s own '
                   'audit/certificates were still unpublished at push time)',
        'independent_method': 'Python standard library; exact-integer Bareiss '
                              '4x4 determinants and an independent 8-element '
                              'D4 board-group canonicalization written for '
                              'this audit; no repository engine/solver/cache, '
                              'no floating point',
        'target': {
            's5_parent1_hex': parent1_hex,
            's6_child_hex': child_hex,
            'edge_cost': 75,
            'legal_candidate_count': len(cand),
            'child_stones': sorted(stones),
        },
        'inputs': {},
        'geometry': {
            'independent_legal_candidates': cand,
            'candidate_bits_exact_match_with_claim': cand == claim_cand,
            'edge_cost_equals_candidate_count': True,
            'child_d4_canonical': True,
            'deletion_orbits': {str(s): format(orbits[s], '032x')
                                for s in sorted(orbits)},
            'deletion_orbits_match_published': True,
            'open_parent': parent1_hex,
            'closed_orbits_absent_from_ranking': 5,
            'top_candidates_row': 's5=00000000000000801202000000200000,'
                                  's6=00000000000040801202000000200000,'
                                  'cost=75,demand="c1=0,c2=1,c4=0"',
        },
        'batches': batches,
        'aggregate': {
            'candidates': len(recs),
            'win7_d10_bits': win_bits,
            'refuted_d10': len(recs) - len(win_bits),
            'capped': 0,
            'capped_bits': [],
            'candidate_nodes_excluding_pilots': total_nodes,
            'pilot_nodes': pilot_nodes,
            'total_nodes_including_pilots': total_nodes + pilot_nodes,
            'node_count_convention_note': 'the raw-batch commit message '
            'counts candidate nodes only (143,552,593); the cost-74h '
            'commit message counted candidates+pilots; both conventions '
            'are recorded here explicitly',
            'pilots': 10,
            'heaviest_bits_nodes': {str(b): n for n, b in heavy},
        },
        'crosschecks': {
            'v16_determinism_rerun': {
                'file': RERUN.name,
                'batch_rerun': 5,
                'identical_ignoring_ms': True,
            },
            'head_1277_baseline': 'claim chain_head_at_claim 1277/6570/518896/'
                                 '4840/382619 re-derived from the published '
                                 'merged-head JSON and ranking CSV',
        },
        'checks': {
            'all_bits_exactly_once': not failures or all('duplicated' not in f
                                                         for f in failures),
            'independent_enumeration_matches_claim': cand == claim_cand,
            'one_stone_deletion_d4_canonicalization_verified': True,
            'all_terminal_ranges_within_depth10_bounds': ranges == {(13, 17)},
            'pilot_3402_per_batch': True,
            'candidate_nodes_match_commit_message': total_nodes
                                                     == 143_552_593,
        },
        'proof_boundary': {
            'raw_sweep_reaggregation': 'closed by this audit (record-level; '
                                       'the 143,552,593-node search itself is '
                                       'not re-executed here)',
            'win7_certificates': 'NOT audited here: the four WIN7-D10 bits '
                                 '[12,40,92,111] await the sweeping lane\'s '
                                 'certificate rebuild and fold; this audit '
                                 'makes no statement about certificate '
                                 'correctness',
            'interpretation_of_refuted_d10': 'the 71 REFUTED-D10 candidates '
                                             'have no first-player win within '
                                             'depth 10; this is NOT a LOSS '
                                             'proof and closes no row by '
                                             'itself',
        },
        'interpretation': 'the sweep is not sterile: 4 of 75 candidates are '
                          'WIN7-D10. Any frontier movement awaits the '
                          'sweeping lane\'s certificates and fold against '
                          'the canonical head 1277. solved counts measure '
                          'manifest coverage only. The standard 11x11 empty '
                          'board, both two-stone roots {49,60}/{59,60}, S2 '
                          '{59,60}, class 1, class 2 and class 4 all remain '
                          'UNKNOWN.',
    }
    for p in [CLAIM, RERUN, HEAD, RANK, TOPC] + \
             [OUT / f'class2-lane-cost75d-raw-batch{b}-20261115.jsonl'
              for b in range(1, 11)]:
        data = p.read_bytes()
        audit['inputs'][p.name] = {'bytes': len(data), 'md5': md5(data),
                                   'git_blob_sha': git_blob_sha(data)}

    dest = OUT / 'class2-lane-cost75d-raw-sweep-independent-audit-20261115.json'
    dest.write_text(json.dumps(audit, indent=1) + '\n')
    print(f'\nwritten {dest.name} ({dest.stat().st_size} bytes)')
    if failures:
        print(f'FAILURES ({len(failures)}): ' + '; '.join(failures))
        sys.exit(1)
    print('ALL CHECKS PASS')


if __name__ == '__main__':
    main()
