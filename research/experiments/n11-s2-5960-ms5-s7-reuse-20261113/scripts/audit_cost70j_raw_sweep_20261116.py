#!/usr/bin/env python3
# Independent raw-sweep audit for the class2-lane cost-70j child sweep (the cost-70
# child 00000000000000801282000000200000 of the best coverable class-2 target S5 at
# the post-cost-75e canonical head 1407, a dual class-1+class-2 demand row).
# Python standard library only; exact integer Bareiss determinants; no floating point,
# no repository solver/engine code. Re-derives the sweep aggregate from the eleven raw
# artifacts (9 v16 raw batches + v16 determinism rerun + v15 crosscheck JSONLs),
# re-enumerates the legal candidates from scratch, re-derives all six one-stone
# deletion lift parents by exact D4 canonicalization, verifies both open parents
# against the published head-1407 ranking CSV, and cross-checks the claim.
import json, sys, os, csv

OUT = os.path.join(os.path.dirname(__file__), '..', 'output')
CLAIM = os.path.join(OUT, 'class2-lane-cost70j-inflight-20261116.json')
CHILD = '00000000000000801282000000200000'
PARENT_CLASS2 = '00000000000000801202000000200000'  # best coverable class-2 target S5 (3 rows / 209)
PARENT_CLASS1 = '00000000000000801082000000200000'  # class-1 lift parent (75 rows / 5971)
RANKING_CSV = os.path.join(OUT, 'class-frontier-s5-ranking-after-cost75e-receipts-20261116.csv')
TOPCSV = os.path.join(OUT, 'class-frontier-top-candidates-s6-after-cost75e-receipts-20261116.csv')

def bareiss4(m):
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
    assert claim['s6_s7_edge_cost'] == 70
    assert claim['s5_parent_class2'] == PARENT_CLASS2
    assert claim['s5_parent_class1'] == PARENT_CLASS1
    assert claim['demand'] == {'c1': 1, 'c2': 1, 'c4': 0}
    assert claim['child_stones_bit_indices'] == [21, 49, 55, 57, 60, 71]
    st, legal = enumerate_legal(CHILD)
    assert st == [21, 49, 55, 57, 60, 71], 'unexpected child stones'
    assert len(st) == 6, 'child must have 6 stones'
    child_safe = True
    for i in range(6):
        for j in range(i + 1, 6):
            for k in range(j + 1, 6):
                for l in range(k + 1, 6):
                    if det4([st[i], st[j], st[k], st[l]]) == 0:
                        child_safe = False
    assert child_safe, 'child must be safe'
    assert legal == claim['legal_candidates'], 'independent enumeration != claim list'
    assert len(legal) == 70

    batches = []
    verdicts = {}
    total_nodes = 0
    pilots = 0
    for n in range(1, 10):
        p = os.path.join(OUT, 'class2-lane-cost70j-raw-batch%d-20261116.jsonl' % n)
        rows = load_jsonl(p)
        ctrl = [r for r in rows if 'control' in r]
        cand = [r for r in rows if 'bit' in r]
        assert len(ctrl) == 1 and ctrl[0]['nodes'] == 3402 and ctrl[0]['loss'] is False
        pilots += 1
        bits = [r['bit'] for r in cand]
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
    assert len(win_bits) + len(refuted) + len(capped) == 70
    assert not capped, 'capped candidates would invalidate the sterile verdict'
    assert not win_bits, 'expected a sterile sweep for cost-70j'
    assert total_nodes == 53890941, 'unexpected total candidate nodes: %d' % total_nodes
    heaviest = sorted(verdicts.items(), key=lambda kv: -kv[1]['nodes'])[:6]
    heaviest = {str(b): r['nodes'] for b, r in heaviest}

    # determinism rerun: batch 5 bits must agree (ignoring ms)
    det = load_jsonl(os.path.join(OUT, 'class2-lane-cost70j-v16-determinism-rerun-20261116.jsonl'))
    det_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'], tuple(r['terminalStoneRange'])) for r in det if 'bit' in r}
    b5_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'], tuple(r['terminalStoneRange']))
               for r in load_jsonl(os.path.join(OUT, 'class2-lane-cost70j-raw-batch5-20261116.jsonl')) if 'bit' in r}
    assert det_bits == b5_bits, 'determinism rerun mismatch'
    det_pilot = [r for r in det if 'control' in r][0]
    assert det_pilot['nodes'] == 3402 and det_pilot['loss'] is False

    # v15 cross-engine agreement (single foreground invocation: 3 heaviest REFUTED
    # anchors bits 9/92/114 plus one d6 pilot)
    v15 = load_jsonl(os.path.join(OUT, 'class2-lane-cost70j-v15-crosscheck-20261116.jsonl'))
    v15_pilots = [r for r in v15 if 'control' in r]
    assert len(v15_pilots) == 1
    assert v15_pilots[0]['nodes'] == 5949 and v15_pilots[0]['loss'] is False
    v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
    assert sorted(v15_bits) == [9, 92, 114], 'unexpected anchor selection'
    for b in v15_bits:
        assert v15_bits[b]['loss'] is False, 'v15 found a WIN on a supposedly refuted anchor'
        assert verdicts[b]['loss'] is False, 'raw verdict disagreement'
        assert v15_bits[b]['capped'] is False
        assert b in legal, 'v15 anchor not a legal candidate: %r' % b
    anchors = sorted(v15_bits)

    # root identity scan (vacuous for a sterile sweep, kept for structure)
    child_v = int(CHILD, 16)
    assert win_bits == [], 'sterile sweep must have no WIN roots'

    # independent one-stone-deletion demand re-derivation
    lifted = {}
    for s in st:
        rest = sorted(x for x in st if x != s)
        v = 0
        for i in rest: v |= 1 << i
        lifted[s] = d4_canon(format(v, '032x'))
    assert lifted == {
        21: '00000000000000003800000008000020',
        49: '00000000000000801280000000200000',
        55: '00000000000000801202000000200000',
        57: '00000000000000801082000000200000',
        60: '00000000000000800282000000200000',
        71: '00000000000000001282000000200000',
    }, 'one-stone deletion D4 canonicalization mismatch: %r' % lifted
    assert len(set(lifted.values())) == 6, 'deletion orbits must be distinct'
    assert lifted[55] == PARENT_CLASS2, 'lift-stone-55 deletion must reproduce the best coverable class-2 target S5'
    assert lifted[57] == PARENT_CLASS1, 'lift-stone-57 deletion must reproduce the class-1 lift parent'

    # verify both open parents and the four closed deletions against the published
    # head-1407 ranking CSV (independently parsed here)
    rank = {}
    with open(RANKING_CSV) as f:
        for row in csv.DictReader(f):
            rank[row['s5_hex']] = (int(row['classes']), int(row['remaining_s6_orbits']), int(row['remaining_s7_edge_cost']))
    assert rank[PARENT_CLASS2] == (2, 3, 209), 'class-2 parent ranking mismatch: %r' % rank.get(PARENT_CLASS2)
    assert rank[PARENT_CLASS1] == (1, 75, 5971), 'class-1 parent ranking mismatch: %r' % rank.get(PARENT_CLASS1)
    for s in (21, 49, 60, 71):
        assert lifted[s] not in rank, 'deletion stone %d must be a closed S5 orbit at head 1407' % s

    # verify the class-2 parent's three remaining rows against the published
    # head-1407 top-candidates CSV: they are exactly the cost-65k (STERILE),
    # cost-70j (this sweep) and cost-74h (STERILE) children
    top = []
    with open(TOPCSV) as f:
        lines = [l for l in f if not l.startswith('#')]
        for row in csv.DictReader(lines):
            if row['s5_hex'] == PARENT_CLASS2:
                top.append((row['s6_hex'], int(row['s6_s7_edge_cost']), row['demand']))
    assert top == [
        ('00000000020000801202000000200000', 65, 'c1=0,c2=2,c4=0'),
        (CHILD, 70, 'c1=1,c2=1,c4=0'),
        ('00000000000000889002000000000800', 74, 'c1=0,c2=2,c4=0'),
    ], 'class-2 parent remaining rows mismatch: %r' % top

    audit = {
        'schema': 'n11-class2-lane-cost70j-raw-sweep-audit-20261116-v1',
        'date': '2026-11-16',
        'independent_method': 'Python standard library; exact Bareiss integer determinants; D4 canonicalization and CSV parsing implemented independently; no repository engine/solver/cache, no floating point',
        'target': {
            's5_parent_class2_hex': PARENT_CLASS2,
            's5_parent_class1_hex': PARENT_CLASS1,
            's6_child_hex': CHILD,
            'edge_cost': 70,
            'legal_candidate_count': 70,
            'demand': {'c1': 1, 'c2': 1, 'c4': 0},
        },
        'source_claim': {
            'path': 'research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70j-inflight-20261116.json',
            'chain_head_at_claim': claim['chain_head_at_claim'],
        },
        'geometry': {
            'child_stones': 6,
            'child_safe': True,
            'independent_legal_candidate_count': 70,
            'candidate_bits_exact_match': True,
            'lift_note': 'one-stone deletions re-derived independently: stone 55 deletion reproduces the best coverable class-2 target S5 00000000000000801202000000200000 bit-exact (3 rows / 209, classes_bitmask 2 at the post-cost-75e head 1407) and stone 57 deletion reproduces the class-1 lift parent 00000000000000801082000000200000 bit-exact (75 rows / 5971, classes_bitmask 1); the other four deletions (stones 21, 49, 60, 71) canonicalize to 00000000000000003800000008000020, 00000000000000801280000000200000, 00000000000000800282000000200000, 00000000000000001282000000200000: six distinct orbits, all four closed and absent from the head-1407 ranking CSV; per-mask-bit demand is therefore c1=1, c2=1, c4=0 (a dual class-1+class-2 demand row), matching the claim and the head-1407 top-candidates CSV row s5=00000000000000801202000000200000,s6=00000000000000801282000000200000,cost=70',
        },
        'batches': batches,
        'aggregate': {
            'candidates': 70,
            'win7_d10_bits': win_bits,
            'refuted_d10': len(refuted),
            'refuted_d10_bits': refuted,
            'capped': len(capped),
            'capped_bits': capped,
            'candidate_nodes': total_nodes,
            'pilots': pilots,
            'heaviest_bits_nodes': heaviest,
        },
        'crosschecks': {
            'v16_determinism_rerun': {
                'file': 'class2-lane-cost70j-v16-determinism-rerun-20261116.jsonl',
                'batch_rerun': 5,
                'identical_ignoring_ms': True,
            },
            'v15_cross_engine': {
                'file': 'class2-lane-cost70j-v15-crosscheck-20261116.jsonl',
                'win_bits_agree': True,
                'refuted_anchors': anchors,
                'anchor_nodes': {str(b): v15_bits[b]['nodes'] for b in anchors},
                'pilots_5949': len(v15_pilots),
                'run_note': 'single foreground invocation (bits 9,92,114 - the three heaviest refuted candidates of the sweep), one d6 pilot at 5949 nodes; all three anchors REFUTED in v15, agreeing with v16',
            },
        },
        'checks': {
            'all_bits_exactly_once': True,
            'all_terminal_ranges_within_depth10_bounds': True,
            'distinct_terminal_ranges': sorted({tuple(r['terminalStoneRange']) for r in verdicts.values()}),
            'pilot_3402_per_batch': True,
            'independent_enumeration_matches_claim': True,
            'one_stone_deletion_d4_canonicalization_verified': True,
            'parents_verified_against_head1407_ranking_csv': True,
            'total_nodes_match': total_nodes == 53890941,
        },
        'proof_boundary': {
            'raw_sweep_rederivation': 'closed by this audit',
            'certificate_extraction': 'not required: the sweep is sterile (no WIN7-D10 bits)',
            'fold_material': 'none: no receipts, the canonical chain frontier is unchanged by this sweep',
            'interpretation_of_refuted_d10': 'all 70 candidates are REFUTED-D10: no first-player win within depth 10 from any of the 70 seven-stone roots. This is NOT a LOSS proof for those roots and does not close the child S6 row; closing this child row requires evidence beyond depth 10 (each candidate would need a refutation at depth > 10 or an equivalent invariant)',
        },
        'structural_consequence': 'with this sweep sterile, ALL THREE remaining rows of the best coverable class-2 target S5 00000000000000801202000000200000 at head 1407 are STERILE from their own sweeps: the cost-65 row 00000000020000801202000000200000 (cost-65k sweep, 65/65 REFUTED-D10), the cost-70 row 00000000000000801282000000200000 (this cost-70j sweep, 70/70 REFUTED-D10) and the cost-74 row 00000000000000889002000000000800 (cost-74h sweep, 74/74 REFUTED-D10). Consequently this S5 is receipt-unclosable from its OWN rows: no sweep of any of its own rows can ever produce a WIN7-D10 receipt, so the S5 leaves the own-row-coverable category (in that respect joining the audit-blocked S5 00000000000000809082000000000000, 10/698). IMPORTANT LIMIT (erratum of the first version of this field, corrected in-session): its rows are NOT permanently unreachable by the receipt mechanism - each row can still be closed by cross-covers (marginals) from WIN7 receipts of OTHER children\'s sweeps, the standard marginal mechanism with multiple precedents (e.g., the cost-70g child was closed at head 1249 by the cost-70f bit-84 cross-cover; the cost-75e bit-10 in-manifest marginal closed a row held by two parents simultaneously). Closure of this S5 now depends entirely on cross-covers or on evidence beyond depth 10. This is a negative structural fact about the own-row receipt mechanism, NOT a LOSS proof for any position; the S5 remains an open row of the class-2 frontier. The next own-row-coverable class-2 candidate at head 1407 is the second-candidate S5 00000000000000801202000040000000 (5 rows / 364: the cost-64 and cost-71 rows are STERILE, the cost-76c row is in-flight under another claim, and the 76d/77e fold-pending rows are claimed by parallel lanes).',
        'interpretation': 'win7_d10_bits is empty: the sweep is sterile. refuted_d10 is NOT a LOSS proof. capped proves nothing (and there were no capped candidates). The sweep alone closes no S6 orbit and changes no frontier count; the child 00000000000000801282000000200000 remains an open S6 row of both open parents: the best coverable class-2 target S5 00000000000000801202000000200000 stays at 3 rows / 209 and the class-1 lift parent 00000000000000801082000000200000 stays at 75 rows / 5971 in the claim-baseline head 1407. The standard 11x11 empty board, both two-stone roots {49,60}/{59,60}, S2 {59,60}, class 1, class 2 and class 4 all remain UNKNOWN.',
    }
    out_path = os.path.join(OUT, 'class2-lane-cost70j-sweep-audit-20261116.json')
    with open(out_path, 'w') as f:
        f.write(json.dumps(audit, indent=1) + '\n')
    print('audit written:', out_path)
    print('win_bits:', win_bits, 'refuted:', len(refuted), 'capped:', len(capped), 'nodes:', total_nodes)

if __name__ == '__main__':
    main()
