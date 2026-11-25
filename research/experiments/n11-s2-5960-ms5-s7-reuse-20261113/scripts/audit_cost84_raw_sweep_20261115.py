#!/usr/bin/env python3
# Independent raw-sweep audit for the class4-lane cost-84 child sweep (three open class-4 parents
# demand c1=0,c2=0,c4=3; the cheapest unswept S6 child of the best class-4 blocker-candidate S5
# after the sterile cost-82b sweep) (2026-11-15).
# Python standard library only; exact integer Bareiss determinants; no floating point,
# no repository solver/engine code. Re-derives the sweep aggregate from the eleven raw
# artifacts (11 v16 raw batch JSONLs + v16 determinism rerun + v15 crosscheck JSONLs),
# re-enumerates the legal candidates from scratch, and cross-checks the claim.
import json, sys, os, glob, hashlib

OUT = os.path.join(os.path.dirname(__file__), '..', 'output')
CLAIM = os.path.join(OUT, 'class4-lane-cost84-inflight-20261115.json')
CHILD = '00000000020000003800000080000400'

def bareiss4(m):
    # exact integer Bareiss on a 4x4 matrix
    m = [row[:] for row in m]
    n = 4
    prev = 1
    for k in range(n - 1):
        if m[k][k] == 0:
            for r in range(k + 1, n):
                if m[r][k] != 0:
                    m[k], m[r] = m[r], m[k]
                    break
            else:
                return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                m[i][j] = (m[i][j] * m[k][k] - m[i][k] * m[k][j]) // prev
            m[i][k] = 0
        prev = m[k][k]
    return m[n - 1][n - 1]

def row_of(cell):
    x = cell % 11; y = cell // 11
    return [x * x + y * y, x, y, 1]

def det4(cells):
    return bareiss4([row_of(c) for c in cells])

def stones(hexstr):
    v = int(hexstr, 16)
    return [i for i in range(121) if (v >> i) & 1]

def enumerate_legal(hexstr):
    st = stones(hexstr)
    legal = []
    for p in range(121):
        if p in st:
            continue
        unsafe = False
        n = len(st)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if det4([st[i], st[j], st[k], p]) == 0:
                        unsafe = True
                        break
                if unsafe: break
            if unsafe: break
        if not unsafe:
            legal.append(p)
    return st, legal

def d4_canon(hexstr):
    st = stones(hexstr)
    best = None
    for swap in (0, 1):
        for fx in (0, 1):
            for fy in (0, 1):
                t = []
                for c in st:
                    x, y = c % 11, c // 11
                    a, b = (y, x) if swap else (x, y)
                    if fx: a = 10 - a
                    if fy: b = 10 - b
                    t.append(a + 11 * b)
                v = 0
                for i in t: v |= 1 << i
                h = format(v, '032x')
                if best is None or h < best: best = h
    return best

def load_jsonl(path):
    out = []
    for line in open(path):
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def main():
    claim = json.load(open(CLAIM))
    assert claim['s6_child'] == CHILD
    assert claim['s6_s7_edge_cost'] == 84
    assert claim['demand'] == {'c1': 0, 'c2': 0, 'c4': 3}
    assert claim['status'] == 'completed'
    assert claim['result']['win7_d10_bits'] == [] and claim['result']['refuted_d10'] == 84 and claim['result']['capped'] == 0
    st, legal = enumerate_legal(CHILD)
    assert st == [10, 31, 59, 60, 61, 89], 'child stones mismatch: %r' % st
    child_safe = True
    for i in range(6):
        for j in range(i + 1, 6):
            for k in range(j + 1, 6):
                for l in range(k + 1, 6):
                    if det4([st[i], st[j], st[k], st[l]]) == 0:
                        child_safe = False
    assert child_safe, 'child must be safe'
    assert legal == claim['legal_candidates'], 'independent enumeration != claim list'
    assert len(legal) == 84

    batches = []
    verdicts = {}
    total_nodes = 0
    pilots = 0
    for n in range(1, 12):
        p = os.path.join(OUT, 'class4-lane-cost84-raw-batch%d-20261115.jsonl' % n)
        rows = load_jsonl(p)
        ctrl = [r for r in rows if 'control' in r]
        cand = [r for r in rows if 'bit' in r]
        assert len(ctrl) == 1 and ctrl[0]['nodes'] == 3402 and ctrl[0]['loss'] is False
        pilots += 1
        bits = [r['bit'] for r in cand]
        assert bits == claim['engine']['batch_bits']['batch%d' % n], 'batch %d bits != claim engine batch_bits' % n
        for r in cand:
            assert r['bit'] not in verdicts, 'duplicate bit'
            assert r['bit'] in legal, 'bit not in enumeration'
            verdicts[r['bit']] = r
            total_nodes += r['nodes']
            tsr = r['terminalStoneRange']
            assert tsr[0] >= 7 and tsr[1] <= 17, 'terminal stone range outside depth-10 bounds (7-stone root, 10 plies)'
        batches.append({'batch': n, 'file': os.path.basename(p),
                        'candidate_bits': bits, 'pilot_nodes': 3402,
                        'nodes': sum(r['nodes'] for r in cand)})
    assert set(verdicts.keys()) == set(legal), 'candidate set mismatch'
    win_bits = sorted(b for b, r in verdicts.items() if r['loss'])
    capped = sorted(b for b, r in verdicts.items() if r['capped'])
    refuted = sorted(b for b, r in verdicts.items() if (not r['loss']) and (not r['capped']))
    assert len(win_bits) + len(refuted) + len(capped) == 84
    assert not capped, 'capped candidates present: %r' % capped
    assert win_bits == [], 'unexpected win bits: %r' % win_bits
    assert total_nodes == claim['result']['candidate_nodes'], 'total nodes mismatch vs completed claim'

    # determinism rerun: batch 5 bits must agree (ignoring ms)
    det = load_jsonl(os.path.join(OUT, 'class4-lane-cost84-v16-determinism-rerun-20261115.jsonl'))
    det_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'], tuple(r['terminalStoneRange'])) for r in det if 'bit' in r}
    b5_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'], tuple(r['terminalStoneRange']))
               for r in load_jsonl(os.path.join(OUT, 'class4-lane-cost84-raw-batch5-20261115.jsonl')) if 'bit' in r}
    assert det_bits == b5_bits, 'determinism rerun mismatch'
    det_pilot = [r for r in det if 'control' in r][0]
    assert det_pilot['nodes'] == 3402 and det_pilot['loss'] is False

    # v15 cross-engine agreement (3 heaviest REFUTED anchors)
    v15 = load_jsonl(os.path.join(OUT, 'class4-lane-cost84-v15-crosscheck-20261115.jsonl'))
    v15_pilots = [r for r in v15 if 'control' in r]
    assert all(r['nodes'] == 5949 and r['loss'] is False for r in v15_pilots)
    v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
    assert sorted(v15_bits) == [34, 66, 86], 'unexpected v15 anchors: %r' % sorted(v15_bits)
    for b in v15_bits:
        assert v15_bits[b]['loss'] is False, 'v15 found a WIN the raw sweep missed'
        assert verdicts[b]['loss'] is False, 'raw verdict disagreement'

    # root identity + D4 canonical scan (vacuous for a sterile sweep, kept for structure)
    child_v = int(CHILD, 16)
    roots = {}
    for b in win_bits:
        rh = format(child_v | (1 << b), '032x')
        rst, rmob = enumerate_legal(rh)
        assert len(rst) == 7
        roots[b] = {'root_hex': rh, 'd4_canonical_hex': d4_canon(rh), 'root_mobility': len(rmob)}
    canon_list = [roots[b]['d4_canonical_hex'] for b in win_bits]
    assert len(set(canon_list)) == len(canon_list), 'WIN roots share a D4 orbit'

    # head-1227 ranking CSV: open S5 set + parent rows
    ranking = {}
    with open(os.path.join(OUT, 'class-frontier-s5-ranking-after-cost69h-receipts-20261115.csv')) as f:
        f.readline()
        for line in f:
            parts = line.strip().split(',')
            ranking[parts[0]] = (int(parts[1]), int(parts[2]), int(parts[3]))
    assert len(ranking) == 175, 'ranking open count mismatch: %d' % len(ranking)

    # one-stone deletion D4 canonicalization
    lifted = {}
    for s in st:
        rest = sorted(x for x in st if x != s)
        v = 0
        for i in rest:
            v |= 1 << i
        lifted[s] = d4_canon(format(v, '032x'))
    assert lifted[10] == '00000000020000003800000080000000', 'del-10 must be parent1 (best class-4 blocker S5): %r' % lifted[28]
    assert lifted[31] == '00000000020000003800000000000400', 'del-31 mismatch: %r' % lifted[31]
    assert lifted[89] == '00000000000000003800000000800001', 'del-89 mismatch: %r' % lifted[89]
    for s in (59, 60, 61):
        assert lifted[s] not in ranking, 'deletion of stone %d expected closed but open: %r' % (s, lifted[s])
    assert ranking['00000000020000003800000080000000'] == (4, 18, 1460), 'parent1 row mismatch'
    assert ranking['00000000020000003800000000000400'] == (4, 88, 7388), 'parent2 row mismatch'
    assert ranking['00000000000000003800000000800001'] == (4, 85, 7023), 'parent3 row mismatch'

    # top-candidates CSV demand row for the child
    tc_lines = open(os.path.join(OUT, 'class-frontier-top-candidates-s6-after-cost69h-receipts-20261115.csv')).read().splitlines()
    row = [l for l in tc_lines if l.startswith('00000000020000003800000080000000,00000000020000003800000080000400,')]
    assert len(row) == 1, 'child row not unique in top-candidates CSV'
    assert row[0].endswith('"c1=0,c2=0,c4=3"'), 'demand mismatch: %r' % row[0]
    assert row[0].split(',')[2] == '84', 'edge cost mismatch: %r' % row[0]

    audit = {
        'schema': 'n11-class4-lane-cost84-raw-sweep-audit-20261115-v1',
        'date': '2026-11-15',
        'independent_method': ('Python standard library; exact Bareiss integer determinants; D4 canonicalization and legal-candidate '
            'enumeration helpers reused verbatim from the published cost-70d/70e audit scripts (same session series, published on main); '
            'raw-record parsing, aggregate re-derivation, batch-bit cross-check, determinism/v15 crosschecks, one-stone-deletion '
            're-derivation and CSV cross-checks written fresh for cost-84 (adapted from the published cost-82b audit); no repository engine/solver/cache, no floating point'),
        'target': {
            's5_hex': claim['s5'],
            's6_child_hex': CHILD,
            'edge_cost': 84,
            'legal_candidate_count': 84,
            'demand': {'c1': 0, 'c2': 0, 'c4': 3},
        },
        'source_claim': {
            'path': 'research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class4-lane-cost84-inflight-20261115.json',
            'chain_head_at_claim': claim['chain_head_at_claim'],
        },
        'geometry': {
            'child_stones': 6,
            'child_stone_bits': st,
            'child_safe': True,
            'independent_legal_candidate_count': 84,
            'candidate_bits_exact_match': True,
            'lift_note': ('one-stone deletions re-derived independently: stone 10 deletion reproduces the best class-4 blocker-candidate '
                'S5 00000000020000003800000080000000 bit-exact (18 rows / 1460 at head 1227), stone 31 deletion D4-canonicalizes to the open '
                'class-4 S5 00000000020000003800000000000400 (88 rows / 7388 at head 1227) and stone 89 deletion to the open class-4 S5 '
                '00000000000000003800000000800001 (85 rows / 7023 at head 1227); the remaining three deletions (stones 59/60/61) are closed '
                'rows absent from the head-1227 ranking CSV; per-class demand c1=0,c2=0,c4=3 matches the published head-1227 top-candidates CSV row'),
        },
        'batches': batches,
        'aggregate': {
            'candidates': 84,
            'win7_d10_bits': win_bits,
            'refuted_d10': len(refuted),
            'refuted_d10_bits': refuted,
            'capped': len(capped),
            'capped_bits': capped,
            'candidate_nodes': total_nodes,
            'pilots': pilots,
        },
        'crosschecks': {
            'v16_determinism_rerun': {
                'file': 'class4-lane-cost84-v16-determinism-rerun-20261115.jsonl',
                'batch_rerun': 5,
                'identical_ignoring_ms': True,
            },
            'v15_cross_engine': {
                'file': 'class4-lane-cost84-v15-crosscheck-20261115.jsonl',
                'win_bits_agree': True,
                'refuted_anchors': sorted(v15_bits),
                'anchor_nodes': {str(b): v15_bits[b]['nodes'] for b in sorted(v15_bits)},
                'pilots_5949': len(v15_pilots),
            },
        },
        'checks': {
            'all_bits_exactly_once': True,
            'batch_bits_match_claim_engine_plan': True,
            'all_terminal_ranges_within_depth10_bounds': True,
            'distinct_terminal_ranges': sorted({tuple(r['terminalStoneRange']) for r in verdicts.values()}),
            'pilot_3402_per_batch': True,
            'determinism_rerun_node_exact': True,
            'v15_cross_engine_agreement': True,
            'independent_enumeration_matches_claim': True,
            'one_stone_deletion_d4_canonicalization_verified': True,
            'parent_rows_match_head1227_ranking_csv': True,
            'demand_matches_head1227_top_candidates_csv': True,
        },
        'proof_boundary': {
            'raw_sweep_rederivation': 'closed by this audit (aggregate, batch bits, verdicts, nodes re-derived from the raw JSONLs)',
            'certificate_extraction': 'not required: the sweep is sterile (no WIN7-D10 bits)',
            'fold_material': 'none: no receipts, the canonical chain frontier is unchanged at 1227/6620/522561/4890/386284',
            'interpretation_of_refuted_d10': ('all 84 candidates are REFUTED-D10: no first-player win within depth 10 from any of the 84 '
                'seven-stone roots. This is NOT a LOSS proof for those roots and does not close the child S6 row; closing this child row '
                'requires evidence beyond depth 10'),
        },
        'interpretation': ('win7_d10_bits is empty: the sweep is sterile. This extends the best class-4 blocker S5 00000000020000003800000080000000 '
            'consecutive-sterile record to 15 swept rows of its 18 open S6 rows (73f/74f/74c/75/79/79b/80/80c/81/82/86a/86b/86c/82b/84), leaving 3 '
            'unswept rows (two cost-86 rows 00000000020000003800100080000000 and '
            '00000000020000003840000080000000, and cost-87 00000000020000003800000080000004). REFUTED-D10 is NOT a LOSS proof. The standard '
            '11x11 empty board, both two-stone roots {49,60}/{59,60}, S2 {59,60}, class 1, class 2 and class 4 all remain UNKNOWN.'),
    }
    out_path = os.path.join(OUT, 'class4-lane-cost84-sweep-audit-20261115.json')
    with open(out_path, 'w') as f:
        f.write(json.dumps(audit, indent=1) + '\n')
    print('audit written:', out_path)
    print('win_bits:', win_bits, 'refuted:', len(refuted), 'capped:', len(capped), 'nodes:', total_nodes)

if __name__ == '__main__':
    main()
