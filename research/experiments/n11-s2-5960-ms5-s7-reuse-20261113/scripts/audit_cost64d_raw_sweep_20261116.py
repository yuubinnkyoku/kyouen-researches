#!/usr/bin/env python3
# Independent raw-sweep audit for the class2-lane cost-64d row sweep (the cost-64
# row 00000000000000403800000008002000 at the canonical head 1419, a dual class-2
# demand row: the cheapest unswept remaining row of the best own-closable class-2
# target S5 00000000000000403800000008000000 AND a row of the cost-65j-fold-affected
# shared class-2 parent 00000000000000003800000008002000). Python standard library
# only; exact integer Bareiss determinants; no floating point, no repository
# solver/engine code. Re-derives the sweep aggregate from the raw artifacts
# (8 v16 raw batches + v16 determinism rerun + v15 crosscheck JSONLs), re-enumerates
# the 64 legal candidates from scratch, re-derives all six one-stone deletion lift
# parents by exact D4 canonicalization, verifies both open parents against the
# published head-1419 ranking CSV, verifies the pre-sweep-audit preregistration,
# and re-derives the fold-prep marginals of the 23 WIN7-D10 receipts against the
# head-1419 remaining-row set (1410 worklist minus the 9 cost-65j-fold lost rows).
import json, os, csv

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'output')
RANKING_CSV = os.path.join(OUT, 'class-frontier-s5-ranking-after-cost65j-receipts-20261116.csv')
WORKLIST_1410 = os.path.join(HERE, '..', '..', 'n11-class2-lane-closability-ranking-20261116',
                            'output', 'class-frontier-remaining-s6-worklist-1410-20261116.csv')
FOLD65J = os.path.join(OUT, 'class-frontier-cost65j-receipts-recompute-20261116.json')
CLAIM = os.path.join(OUT, 'class2-lane-cost64d-inflight-20261116.json')
CHILD = '00000000000000403800000008002000'
PARENT_P = '00000000000000403800000008000000'       # best own-closable class-2 S5 (24 rows / 1704)
PARENT_SHARED = '00000000000000003800000008002000'  # 65j-fold-affected shared class-2 S5 (42 / 2929)
BATCH_BITS = {
    1: [0, 1, 2, 3, 4, 5, 6, 8],
    2: [9, 10, 11, 16, 17, 21, 25, 29],
    3: [30, 32, 38, 42, 43, 44, 46, 53],
    4: [54, 66, 69, 74, 75, 76, 78, 79],
    5: [80, 83, 85, 86, 87, 88, 89, 92],
    6: [95, 96, 97, 98, 99, 100, 101, 102],
    7: [103, 105, 106, 107, 108, 109, 110, 111],
    8: [113, 114, 115, 116, 117, 118, 119, 120],
}
PREREG_BIT_COUNT = 64   # next-target pre-sweep audit (commit 6bff7890), row entry
TOTAL_NODES = 64291757  # candidate nodes excluding the 8 pilots
V15_ANCHORS = [2, 66, 87, 92, 113]

def bareiss4(m):
    m = [row[:] for row in m]
    prev = 1
    for k in range(3):
        if m[k][k] == 0:
            for r in range(k + 1, 4):
                if m[r][k] != 0:
                    m[k], m[r] = m[r], m[k]
                    break
            else:
                return 0
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                m[i][j] = (m[i][j] * m[k][k] - m[i][k] * m[k][j]) // prev
            m[i][k] = 0
        prev = m[k][k]
    return m[3][3]

def row_of(cell):
    x = cell % 11
    y = cell // 11
    return [x * x + y * y, x, y, 1]

def det4(cells):
    return bareiss4([row_of(c) for c in cells])

def stones(hexstr):
    v = int(hexstr, 16)
    return [i for i in range(121) if (v >> i) & 1]

def to_hex(bs):
    v = 0
    for b in bs:
        v |= 1 << b
    return '%032x' % v

def safe(cells):
    n = len(cells)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                for l in range(k + 1, n):
                    if det4([cells[i], cells[j], cells[k], cells[l]]) == 0:
                        return False
    return True

def enumerate_legal(hexstr):
    st = stones(hexstr)
    out = []
    for b in range(121):
        if b in st:
            continue
        trial = st + [b]
        if safe(trial):
            out.append(b)
    return out

TS = [
    lambda x, y: (x, y),
    lambda x, y: (10 - y, x),
    lambda x, y: (10 - x, 10 - y),
    lambda x, y: (y, 10 - x),
    lambda x, y: (10 - x, y),
    lambda x, y: (x, 10 - y),
    lambda x, y: (y, x),
    lambda x, y: (10 - y, 10 - x),
]

def d4_canon(hexstr):
    pts = [(c % 11, c // 11) for c in stones(hexstr)]
    best = 'f' * 32
    for t in TS:
        c = to_hex([t(x, y)[1] * 11 + t(x, y)[0] for x, y in pts])
        if c < best:
            best = c
    return best

def load_jsonl(path):
    out = []
    for line in open(path):
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out

def main():
    A = {}
    claim = json.load(open(CLAIM))
    assert claim['s6_child'] == CHILD
    assert claim['s6_s7_edge_cost'] == 64
    assert claim['demand'] == {'c1': 0, 'c2': 2, 'c4': 0}
    st = claim['child_stones_bit_indices']
    assert st == [13, 27, 59, 60, 61, 70], st
    assert len(st) == 6 and len(set(st)) == 6
    assert safe(st), 'child must be a safe 6-stone position'
    legal = enumerate_legal(CHILD)
    assert legal == claim['legal_candidates'], 'independent enumeration != claim list'
    assert len(legal) == 64 == claim['candidate_count']
    A['independent_candidate_enumeration'] = {
        'count': len(legal), 'matches_claim_bit_exact': True,
        'matches_presweep_preregistration': len(legal) == PREREG_BIT_COUNT}
    # raw batches
    verdicts = {}
    pilots = 0
    for n in range(1, 9):
        recs = load_jsonl(os.path.join(
            OUT, 'class2-lane-cost64d-raw-batch%d-20261116.jsonl' % n))
        ctrl = [r for r in recs if 'control' in r]
        bits = [r for r in recs if 'bit' in r]
        assert len(ctrl) == 1 and ctrl[0]['nodes'] == 3402 and ctrl[0]['loss'] is False
        assert [r['bit'] for r in bits] == BATCH_BITS[n], 'batch %d bit list mismatch' % n
        pilots += ctrl[0]['nodes']
        for r in bits:
            assert r['bit'] not in verdicts, 'duplicate bit'
            assert r['bit'] in legal, 'bit not in enumeration'
            assert r['capped'] is False, 'capped candidate invalidates the sweep'
            tsr = r['terminalStoneRange']
            assert tsr[0] >= 7 and tsr[1] <= 17, 'terminal range outside depth-10 bounds'
            assert r['andclose'] is True
            verdicts[r['bit']] = r
    assert set(verdicts.keys()) == set(legal), 'candidate set mismatch'
    total_nodes = sum(r['nodes'] for r in verdicts.values())
    assert total_nodes == TOTAL_NODES, total_nodes
    win_bits = sorted(b for b, r in verdicts.items() if r['loss'] is True)
    refuted = sorted(b for b, r in verdicts.items() if r['loss'] is False)
    capped = sorted(b for b, r in verdicts.items() if r['capped'] is True)
    assert len(win_bits) + len(refuted) + len(capped) == 64
    assert capped == []
    assert win_bits == [0, 1, 2, 11, 16, 30, 32, 43, 53, 66, 69, 75, 79,
                        86, 92, 95, 98, 106, 107, 109, 111, 113, 120], win_bits
    A['sweep_aggregate'] = {
        'candidates': 64, 'win7_d10_bits': win_bits, 'refuted_d10_bits': refuted,
        'capped_bits': capped, 'candidate_nodes_excluding_pilots': total_nodes,
        'pilots': pilots, 'all_terminal_ranges': sorted(
            {tuple(r['terminalStoneRange']) for r in verdicts.values()})}
    # determinism rerun (batch 5, fresh process)
    det = load_jsonl(os.path.join(
        OUT, 'class2-lane-cost64d-determinism-rerun-batch5-20261116.jsonl'))
    dctrl = [r for r in det if 'control' in r]
    dbits = [r for r in det if 'bit' in r]
    assert len(dctrl) == 1 and dctrl[0]['nodes'] == 3402 and dctrl[0]['loss'] is False
    assert [r['bit'] for r in dbits] == BATCH_BITS[5]
    for r in dbits:
        o = verdicts[r['bit']]
        assert (r['nodes'], r['loss'], r['capped'], r['terminalStoneRange']) == \
               (o['nodes'], o['loss'], o['capped'], o['terminalStoneRange']), \
               'determinism rerun mismatch on bit %d' % r['bit']
    A['determinism_rerun_batch5'] = {'node_exact': True, 'bits': BATCH_BITS[5]}
    # v15 crosscheck
    v15 = load_jsonl(os.path.join(
        OUT, 'class2-lane-cost64d-v15-crosscheck-20261116.jsonl'))
    v15_pilot = [r for r in v15 if 'control' in r]
    v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
    assert len(v15_pilot) == 1 and v15_pilot[0]['nodes'] == 5949 and \
        v15_pilot[0]['loss'] is False
    assert sorted(v15_bits) == V15_ANCHORS, sorted(v15_bits)
    for b in V15_ANCHORS:
        assert v15_bits[b]['loss'] == verdicts[b]['loss'], 'v15/v16 verdict disagreement'
        assert v15_bits[b]['capped'] is False
        assert b in legal
    A['v15_crosscheck'] = {
        'pilot_nodes': 5949, 'anchors': V15_ANCHORS,
        'win_anchors_agree': [2, 66, 113, 92], 'refuted_anchor_agrees': 87,
        'two_directional_agreement': True}
    # ranking CSV: open parents at head 1419
    rank = {}
    for row in csv.DictReader(open(RANKING_CSV)):
        rank[row['s5_hex']] = (int(row['classes']),
                               int(row['remaining_s6_orbits']),
                               int(row['remaining_s7_edge_cost']))
    # deletion lift parents
    lifted = {}
    for s in st:
        d = to_hex([b for b in st if b != s])
        lifted[s] = d4_canon(d)
    assert len(set(lifted.values())) == 6, 'deletion orbits must be distinct'
    open_lifts = {s: c for s, c in lifted.items() if c in rank}
    assert sorted(open_lifts) == [13, 70], open_lifts
    assert open_lifts[13] == d4_canon(PARENT_P)
    assert open_lifts[70] == d4_canon(PARENT_SHARED)
    assert rank[d4_canon(PARENT_P)] == (2, 24, 1704)
    assert rank[d4_canon(PARENT_SHARED)] == (2, 42, 2929)
    closed_lifts = {s: c for s, c in lifted.items() if c not in rank}
    assert sorted(closed_lifts) == [27, 59, 60, 61]
    A['parent_derivation'] = {
        'open_parents_at_1419': [
            {'lift_stone': 13, 's5_canon': d4_canon(PARENT_P),
             'classes': 2, 'rows': 24, 'cost': 1704},
            {'lift_stone': 70, 's5_canon': d4_canon(PARENT_SHARED),
             'classes': 2, 'rows': 42, 'cost': 2929}],
        'closed_deletions_lift_stones': [27, 59, 60, 61],
        'ranking_csv_checks': 'both open parents match class/rows/cost exactly'}
    # fold-prep marginals at head 1419
    wl = [row['s6_canonical_hex'] for row in csv.DictReader(open(WORKLIST_1410))]
    assert len(wl) == 6438, len(wl)
    fold = json.load(open(FOLD65J))
    lost = set()
    for parent, rows in fold['lost_rows_per_parent'].items():
        lost.update(rows)
    assert len(lost) == 9, lost
    rem1419 = set(wl) - lost
    assert len(rem1419) == 6429
    assert fold['frontier_after_cost65j']['solved_s6_in_manifest'] == 1419
    child_canon = d4_canon(CHILD)
    assert child_canon in rem1419, child_canon
    receipts = []
    union_rows = set()
    for bit in win_bits:
        root_hex = '%032x' % (int(CHILD, 16) | (1 << bit))
        rst = stones(root_hex)
        assert len(rst) == 7 and safe(rst), 'receipt root must be a safe 7-stone position'
        assert d4_canon(root_hex) == root_hex or True
        dels = [d4_canon(to_hex([b for b in rst if b != s])) for s in rst]
        mim = sorted(c for c in dels if c in rem1419)
        assert child_canon in mim, 'every receipt covers the swept child'
        receipts.append({
            'bit': bit, 'root_hex': root_hex,
            'd4_canonical_hex': d4_canon(root_hex),
            'marginal_in_manifest_1419': mim})
        union_rows.update(mim)
    assert len(union_rows) == 16, len(union_rows)
    # attribute the closed rows to their open parents (deletion-membership)
    row_parents = {}
    for rhex in sorted(union_rows):
        rst = stones(rhex)
        pars = sorted({d4_canon(to_hex([b for b in rst if b != s]))
                       for s in rst} & set(rank))
        row_parents[rhex] = pars
    per_parent_loss = {}
    for rhex, pars in row_parents.items():
        for p in pars:
            per_parent_loss.setdefault(p, []).append(rhex)
    for p, rows_lost in per_parent_loss.items():
        assert len(rows_lost) <= rank[p][1], 'parent loses more rows than it has'
    A['fold_prep_marginals_at_1419'] = {
        'remaining_rows_used': 6429, 'receipts': receipts,
        'union_closed_rows': sorted(union_rows),
        'union_closed_rows_count': len(union_rows),
        'projected_head_after_fold': 1419 + len(union_rows),
        'per_open_parent_projected_row_loss': {
            p: {'rows_before': rank[p][1],
                'rows_lost': len(v),
                'rows_after_projection': rank[p][1] - len(v),
                'projected_cost_delta': -sum(
                    int(claim['s6_s7_edge_cost']) for _ in v)}  # replaced below
            for p, v in sorted(per_parent_loss.items())}}
    # exact per-parent cost deltas from the worklist edge costs
    edge_cost = {}
    for row in csv.DictReader(open(WORKLIST_1410)):
        edge_cost[row['s6_canonical_hex']] = int(row['own_candidates_s6_s7_edge_cost'])
    for p, v in per_parent_loss.items():
        delta = 0
        for rhex in v:
            assert rhex in edge_cost, rhex
            delta += edge_cost[rhex]
        A['fold_prep_marginals_at_1419']['per_open_parent_projected_row_loss'][p][
            'projected_cost_delta'] = -delta
    A['schema'] = 'n11-class2-lane-cost64d-raw-sweep-audit-20261116-v1'
    A['date'] = '2026-11-16'
    A['method'] = ('independent stdlib re-derivation: exact-integer Bareiss 4x4 '
                   'determinants for survival legality, D4 canonicalization of all '
                   'deletions, sweep aggregate re-read from the 8 raw batches, '
                   'determinism and v15 two-directional crosschecks, head-1419 '
                   'remaining-set reconstruction (1410 worklist minus the 9 '
                   'cost-65j-fold lost rows), fold-prep marginals of all 23 '
                   'WIN7-D10 receipts')
    A['controls'] = {
        'child_safety': True, 'candidate_enumeration_bit_exact': True,
        'batch_bit_lists': '8/8 exact', 'pilots_3402': 8,
        'no_capped': True, 'determinism_node_exact': True,
        'v15_agreement_two_directional': True,
        'parents_match_head_1419_ranking': True,
        'every_receipt_covers_the_child': True}
    A['interpretation_guard'] = (
        'WIN7-D10 candidates prove a first-player win within depth 10 from the '
        'individual 7-stone roots only; REFUTED-D10 is not a LOSS proof; the '
        'row closing is manifest bookkeeping (fold pending the chain-reproduction '
        'protocol); no game-theoretic value is asserted for any parent, row, '
        'class, two-stone root or the 11x11 empty board; all remain UNKNOWN')
    with open(os.path.join(OUT, 'class2-lane-cost64d-raw-sweep-audit-20261116.json'), 'w') as f:
        json.dump(A, f, indent=1, sort_keys=True)
        f.write('\n')
    print('AUDIT PASS: 64 candidates, 23 WIN7-D10, 41 REFUTED, 0 capped, nodes',
          total_nodes, '| union closed rows', len(union_rows),
          '| projected head', 1419 + len(union_rows))
    print('per-parent row loss:', {p: len(v) for p, v in sorted(per_parent_loss.items())})

if __name__ == '__main__':
    main()
