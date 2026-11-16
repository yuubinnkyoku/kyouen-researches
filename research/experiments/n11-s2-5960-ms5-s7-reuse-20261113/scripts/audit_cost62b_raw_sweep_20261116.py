#!/usr/bin/env python3
# Independent raw-sweep audit for the class2-lane cost-62b child sweep (the cost-62
# child 00000000000000801282020000000000 at the post-cost-60c canonical head 1410,
# a dual class-1+class-2 demand row; the next cheapest unswept one-stone-replacement
# neighbor of the STERILE cost-70j child). Python standard library only; exact
# integer Bareiss determinants; no floating point, no repository solver/engine code.
# Re-derives the sweep aggregate from the raw artifacts (10 v16 raw batches + v16
# determinism rerun + v15 crosscheck JSONLs), re-enumerates the legal candidates
# from scratch, re-derives all six one-stone deletion lift parents by exact D4
# canonicalization, verifies both open parents against the published head-1410
# ranking CSV, cross-checks the claim, and re-derives the two bit-21/bit-109
# cross-cover relationships to the STERILE cost-70j child (the only candidate
# roots of this child that cover that row - both REFUTED-D10).
import json, sys, os, csv, glob

OUT = os.path.join(os.path.dirname(__file__), '..', 'output')
CLAIM = os.path.join(OUT, 'class2-lane-cost62b-inflight-20261116.json')
CHILD = '00000000000000801282020000000000'
PARENT_CLASS2 = '00000000000000801202020000000000'  # class-2 lift parent (49 rows / 3360)
PARENT_CLASS1 = '00000000000000801082020000000000'  # class-1 lift parent (73 rows / 5489)
TARGET_70J = '00000000000000801282000000200000'     # STERILE cost-70j child (cross-cover target)
RANKING_CSV = os.path.join(OUT, 'class-frontier-s5-ranking-after-cost60c-receipts-20261116.csv')
TOPCSV = os.path.join(OUT, 'class-frontier-top-candidates-s6-after-cost60c-receipts-20261116.csv')
BATCH_BITS = {
    1: [4, 0, 1, 3, 12, 15, 50],
    2: [32, 6, 8, 9, 10, 29, 73],
    3: [43, 11, 13, 14, 17, 18, 21],
    4: [45, 22, 26, 28, 31, 33, 67],
    5: [52, 54, 77, 78, 84, 86, 87],
    6: [72, 88, 89, 92, 94, 97, 98],
    7: [99, 100, 101, 102, 103, 105, 106],
    8: [108, 109, 110, 111, 112, 113, 114],
    9: [116, 117, 118, 119, 120],
    10: [42],
}
TOTAL_NODES = 34617690

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
    assert claim['s6_s7_edge_cost'] == 62
    assert claim['demand'] == {'c1': 1, 'c2': 1, 'c4': 0}
    assert claim['child_stones_bit_indices'] == [41, 49, 55, 57, 60, 71]
    st, legal = enumerate_legal(CHILD)
    assert st == [41, 49, 55, 57, 60, 71], 'unexpected child stones'
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
    assert len(legal) == 62

    batches = []
    verdicts = {}
    total_nodes = 0
    pilots = 0
    for n in sorted(BATCH_BITS):
        p = os.path.join(OUT, 'class2-lane-cost62b-raw-batch%d-20261116.jsonl' % n)
        rows = load_jsonl(p)
        ctrl = [r for r in rows if 'control' in r]
        cand = [r for r in rows if 'bit' in r]
        assert len(ctrl) == 1 and ctrl[0]['nodes'] == 3402 and ctrl[0]['loss'] is False
        pilots += 1
        bits = [r['bit'] for r in cand]
        assert bits == BATCH_BITS[n], 'batch %d bit list mismatch: %r' % (n, bits)
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
    assert len(win_bits) + len(refuted) + len(capped) == 62
    assert not capped, 'capped candidates would invalidate the sweep'
    assert win_bits == [], 'expected a STERILE sweep (no WIN7-D10 candidate)'
    assert total_nodes == TOTAL_NODES, 'unexpected total candidate nodes: %d' % total_nodes
    heaviest = sorted(verdicts.items(), key=lambda kv: -kv[1]['nodes'])[:6]
    heaviest = {str(b): r['nodes'] for b, r in heaviest}

    # determinism rerun: batch 5 bits must agree (ignoring ms)
    det = load_jsonl(os.path.join(OUT, 'class2-lane-cost62b-v16-determinism-rerun-20261116.jsonl'))
    det_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'], tuple(r['terminalStoneRange'])) for r in det if 'bit' in r}
    b5_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'], tuple(r['terminalStoneRange']))
               for r in load_jsonl(os.path.join(OUT, 'class2-lane-cost62b-raw-batch5-20261116.jsonl')) if 'bit' in r}
    assert det_bits == b5_bits, 'determinism rerun mismatch'
    det_pilot = [r for r in det if 'control' in r][0]
    assert det_pilot['nodes'] == 3402 and det_pilot['loss'] is False

    # v15 cross-engine agreement (single foreground invocation: both cross-cover
    # roots 21/109, the two heaviest candidates 114/105 and bit 0, plus one d6 pilot)
    v15 = load_jsonl(os.path.join(OUT, 'class2-lane-cost62b-v15-crosscheck-20261116.jsonl'))
    v15_pilots = [r for r in v15 if 'control' in r]
    assert len(v15_pilots) == 1
    assert v15_pilots[0]['nodes'] == 5949 and v15_pilots[0]['loss'] is False
    v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
    assert sorted(v15_bits) == [0, 21, 105, 109, 114], 'unexpected anchor selection'
    for b in (0, 21, 105, 109, 114):
        assert v15_bits[b]['loss'] is False, 'v15 found a WIN on a supposedly refuted anchor'
        assert verdicts[b]['loss'] is False, 'raw verdict disagreement'
        assert v15_bits[b]['capped'] is False
        assert b in legal, 'v15 anchor not a legal candidate: %r' % b
    anchors = sorted(v15_bits)

    # cross-cover re-derivation: exactly two candidate roots cover the STERILE
    # cost-70j child, namely bits 21 and 109, and both are REFUTED-D10
    target_v = int(TARGET_70J, 16)
    cover_bits = []
    for b in legal:
        root = st + [b]
        for s in root:
            v = 0
            for x in root:
                if x != s:
                    v |= 1 << x
            if int(d4_canon(format(v, '032x')), 16) == target_v:
                cover_bits.append(b)
                break
    assert cover_bits == [21, 109], cover_bits
    for b in (21, 109):
        assert verdicts[b]['loss'] is False and verdicts[b]['capped'] is False, \
            'the bit-%d cross-cover root must be REFUTED-D10 in this sweep' % b

    # independent one-stone-deletion demand re-derivation
    lifted = {}
    for s in st:
        rest = sorted(x for x in st if x != s)
        v = 0
        for i in rest: v |= 1 << i
        lifted[s] = d4_canon(format(v, '032x'))
    assert lifted == {
        41: '00000000000000003800000008000020',
        49: '00000000000000801280020000000000',
        55: '00000000000000801202020000000000',
        57: '00000000000000801082020000000000',
        60: '00000000000000800282020000000000',
        71: '00000000000000001282020000000000',
    }, 'one-stone deletion D4 canonicalization mismatch: %r' % lifted
    assert len(set(lifted.values())) == 6, 'deletion orbits must be distinct'
    assert lifted[55] == PARENT_CLASS2, 'lift-stone-55 deletion must reproduce the class-2 lift parent'
    assert lifted[57] == PARENT_CLASS1, 'lift-stone-57 deletion must reproduce the class-1 lift parent'

    # verify both open parents and the four closed deletions against the published
    # head-1410 ranking CSV (independently parsed here)
    rank = {}
    with open(RANKING_CSV) as f:
        for row in csv.DictReader(f):
            rank[row['s5_hex']] = (int(row['classes']), int(row['remaining_s6_orbits']), int(row['remaining_s7_edge_cost']))
    assert rank[PARENT_CLASS2] == (2, 49, 3360), 'class-2 parent ranking mismatch: %r' % rank.get(PARENT_CLASS2)
    assert rank[PARENT_CLASS1] == (1, 73, 5489), 'class-1 parent ranking mismatch: %r' % rank.get(PARENT_CLASS1)
    for s in (41, 49, 60, 71):
        assert lifted[s] not in rank, 'deletion stone %d must be a closed S5 orbit at head 1410' % s

    # verify the child row against the published MS5 S6 manifest (milestone5 parts,
    # blob-pinned inputs of the whole class-frontier chain): the child must be an
    # in-manifest row with edge cost 62 and class bitmask 3 (dual class-1+class-2)
    manifest_hits = []
    for mp in sorted(glob.glob(os.path.join(
            os.path.dirname(__file__), '..', '..',
            'n11-s2-5960-milestone5-20261112',
            'output', 'ms5_s6_manifest_part*.csv'))):
        with open(mp) as f:
            for line in f:
                if line.startswith('hex,'):
                    continue
                parts = line.strip().split(',')
                if parts and parts[0] == CHILD:
                    manifest_hits.append((int(parts[1]), int(parts[2])))
    assert manifest_hits == [(62, 3)], \
        'the child must appear exactly once in the published MS5 S6 manifest with cost 62 and class bitmask 3: %r' % manifest_hits
    # the curated head-1410 top-candidates CSV lists only the best class-4 S5 rows;
    # the child must not appear there (coordination consistency)
    with open(TOPCSV) as f:
        topcsv_text = f.read()
    assert CHILD not in topcsv_text, 'the child is not a best-class-4-S5 row and must be absent from the curated top-candidates CSV'

    audit = {
        'schema': 'n11-class2-lane-cost62b-raw-sweep-audit-20261116-v1',
        'date': '2026-11-16',
        'independent_method': 'Python standard library; exact Bareiss integer determinants; D4 canonicalization and CSV parsing implemented independently; no repository engine/solver/cache, no floating point',
        'target': {
            's5_parent_class2_hex': PARENT_CLASS2,
            's5_parent_class1_hex': PARENT_CLASS1,
            's6_child_hex': CHILD,
            'edge_cost': 62,
            'legal_candidate_count': 62,
            'demand': {'c1': 1, 'c2': 1, 'c4': 0},
        },
        'source_claim': {
            'path': 'research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost62b-inflight-20261116.json',
            'chain_head_at_claim': claim['chain_head_at_claim'],
        },
        'geometry': {
            'child_stones': 6,
            'child_safe': True,
            'independent_legal_candidate_count': 62,
            'candidate_bits_exact_match': True,
            'lift_note': 'one-stone deletions re-derived independently: stone 55 deletion reproduces the class-2 lift parent 00000000000000801202020000000000 bit-exact (49 rows / 3360, classes_bitmask 2 at the post-cost-60c head 1410) and stone 57 deletion reproduces the class-1 lift parent 00000000000000801082020000000000 bit-exact (73 rows / 5489, classes_bitmask 1); the other four deletions (stones 41, 49, 60, 71) canonicalize to 00000000000000003800000008000020, 00000000000000801280020000000000, 00000000000000800282020000000000, 00000000000000001282020000000000: six distinct orbits, all four closed and absent from the head-1410 ranking CSV; per-mask-bit demand is therefore c1=1, c2=1, c4=0 (a dual class-1+class-2 demand row), matching the claim and the MS5 S6 manifest row (cost 62, class bitmask 3)',
        },
        'batches': batches,
        'aggregate': {
            'candidates': 62,
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
                'file': 'class2-lane-cost62b-v16-determinism-rerun-20261116.jsonl',
                'batch_rerun': 5,
                'identical_ignoring_ms': True,
            },
            'v15_cross_engine': {
                'file': 'class2-lane-cost62b-v15-crosscheck-20261116.jsonl',
                'anchors': anchors,
                'anchor_nodes': {str(b): v15_bits[b]['nodes'] for b in anchors},
                'pilots_5949': len(v15_pilots),
                'run_note': 'single foreground invocation (both cross-cover roots 21/109, the two heaviest candidates 114/105 and bit 0), one d6 pilot at 5949 nodes; v15 confirms loss=false on all five anchors, agreeing with v16',
            },
        },
        'checks': {
            'all_bits_exactly_once': True,
            'all_terminal_ranges_within_depth10_bounds': True,
            'distinct_terminal_ranges': sorted({tuple(r['terminalStoneRange']) for r in verdicts.values()}),
            'pilot_3402_per_batch': True,
            'independent_enumeration_matches_claim': True,
            'one_stone_deletion_d4_canonicalization_verified': True,
            'parents_verified_against_head1410_ranking_csv': True,
            'total_nodes_match': total_nodes == TOTAL_NODES,
        },
        'cross_cover_consequence': 'the sweep tested the two candidate roots of this child that cover the STERILE cost-70j child 00000000000000801282000000200000 (a remaining row, edge 70, of the best coverable class-2 S5 00000000000000801202000000200000, 3 rows / 209, all three rows STERILE by their own-row sweeps): exactly bits 21 (root 00000000000000801282020000200000) and 109 (root 00002000000000801282020000000000), re-derived independently here by canonical covers over all 62 candidates x 7 deletions. Both are REFUTED-D10, so the 70j row is NOT closed by this neighbor either; its cross-cover route via this child is exhausted. Together with the cost-60c negative fact (bit 119 REFUTED), the 70j row now has its two cheapest one-stone-replacement neighbors exhausted; its closure depends on the remaining neighbors (65k-child and 74h-child neighborhoods), other cross-cover routes, or evidence beyond depth 10. A negative fact only; NOT a LOSS proof.',
        'structural_consequence': '62/62 REFUTED-D10 at cap 1e9 (0 capped): the cost-62b child is STERILE - no WIN7-D10 receipt can be produced from any of its 62 legal roots, so this S6 row is unclosable by depth-10 WIN7 receipts from its own row. This is NOT a LOSS proof. The canonical head 1410/174/6438/509109/4711/373023 is unchanged (no fold material): both open parents keep the child row (class-2 49/3360 and class-1 73/5489).',
        'interpretation': 'win7_d10_bits is []: the sweep is STERILE. refuted_d10 is NOT a LOSS proof; it records only the absence of a first-player win within depth 10 from each root. There were no capped candidates. The standard 11x11 empty board, both two-stone roots {49,60}/{59,60}, S2 {59,60}, class 1, class 2 and class 4 all remain UNKNOWN.',
    }
    out_path = os.path.join(OUT, 'class2-lane-cost62b-sweep-audit-20261116.json')
    with open(out_path, 'w') as f:
        f.write(json.dumps(audit, indent=1) + '\n')
    print('audit written:', out_path)
    print('win_bits:', win_bits, 'refuted:', len(refuted), 'capped:', len(capped), 'nodes:', total_nodes)

if __name__ == '__main__':
    main()
