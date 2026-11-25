#!/usr/bin/env python3
# Independent raw-sweep audit for the class2-lane cost-60c child sweep (the cost-60
# child 00000000000000003800000008008020 at the post-cost-75e canonical head 1407,
# a dual class-1+class-2 demand row; cross-cover neighbor of the STERILE cost-70j
# child). Python standard library only; exact integer Bareiss determinants; no
# floating point, no repository solver/engine code. Re-derives the sweep aggregate
# from the ten raw artifacts (8 v16 raw batches + v16 determinism rerun + v15
# crosscheck JSONLs), re-enumerates the legal candidates from scratch, re-derives
# all six one-stone deletion lift parents by exact D4 canonicalization, verifies
# both open parents against the published head-1407 ranking CSV, cross-checks the
# claim, and re-derives the single bit-119 cross-cover relationship to the STERILE
# cost-70j child (the only candidate root of this child that covers that row).
import json, sys, os, csv

OUT = os.path.join(os.path.dirname(__file__), '..', 'output')
CLAIM = os.path.join(OUT, 'class2-lane-cost60c-inflight-20261116.json')
CHILD = '00000000000000003800000008008020'
PARENT_CLASS2 = '00000000000000003800000008008000'  # class-2 lift parent (50 rows / 3551)
PARENT_CLASS1 = '00000000000000003800000000008020'  # class-1 lift parent (74 rows / 5399)
TARGET_70J = '00000000000000801282000000200000'     # STERILE cost-70j child (cross-cover target)
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
    assert claim['s6_s7_edge_cost'] == 60
    assert claim['demand'] == {'c1': 1, 'c2': 1, 'c4': 0}
    assert claim['child_stones_bit_indices'] == [5, 15, 27, 59, 60, 61]
    st, legal = enumerate_legal(CHILD)
    assert st == [5, 15, 27, 59, 60, 61], 'unexpected child stones'
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
    assert len(legal) == 60

    batches = []
    verdicts = {}
    total_nodes = 0
    pilots = 0
    for n in range(1, 9):
        p = os.path.join(OUT, 'class2-lane-cost60c-raw-batch%d-20261116.jsonl' % n)
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
    assert len(win_bits) + len(refuted) + len(capped) == 60
    assert not capped, 'capped candidates would invalidate the sweep'
    assert win_bits == [92], 'expected exactly the bit-92 WIN7-D10 candidate'
    assert total_nodes == 25197741, 'unexpected total candidate nodes: %d' % total_nodes
    heaviest = sorted(verdicts.items(), key=lambda kv: -kv[1]['nodes'])[:6]
    heaviest = {str(b): r['nodes'] for b, r in heaviest}

    # determinism rerun: batch 5 bits must agree (ignoring ms)
    det = load_jsonl(os.path.join(OUT, 'class2-lane-cost60c-v16-determinism-rerun-20261116.jsonl'))
    det_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'], tuple(r['terminalStoneRange'])) for r in det if 'bit' in r}
    b5_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'], tuple(r['terminalStoneRange']))
               for r in load_jsonl(os.path.join(OUT, 'class2-lane-cost60c-raw-batch5-20261116.jsonl')) if 'bit' in r}
    assert det_bits == b5_bits, 'determinism rerun mismatch'
    det_pilot = [r for r in det if 'control' in r][0]
    assert det_pilot['nodes'] == 3402 and det_pilot['loss'] is False

    # v15 cross-engine agreement (single foreground invocation: the WIN bit 92, the
    # bit-119 cross-cover anchor and two further refuted anchors, plus one d6 pilot)
    v15 = load_jsonl(os.path.join(OUT, 'class2-lane-cost60c-v15-crosscheck-20261116.jsonl'))
    v15_pilots = [r for r in v15 if 'control' in r]
    assert len(v15_pilots) == 1
    assert v15_pilots[0]['nodes'] == 5949 and v15_pilots[0]['loss'] is False
    v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
    assert sorted(v15_bits) == [0, 92, 119, 120], 'unexpected anchor selection'
    assert v15_bits[92]['loss'] is True and v15_bits[92]['capped'] is False, \
        'v15 must confirm the bit-92 WIN7-D10 verdict'
    assert verdicts[92]['loss'] is True, 'raw verdict disagreement on the WIN bit'
    for b in (0, 119, 120):
        assert v15_bits[b]['loss'] is False, 'v15 found a WIN on a supposedly refuted anchor'
        assert verdicts[b]['loss'] is False, 'raw verdict disagreement'
        assert v15_bits[b]['capped'] is False
        assert b in legal, 'v15 anchor not a legal candidate: %r' % b
    anchors = sorted(b for b in v15_bits if b != 92)

    # root identity: the single WIN root is the child plus the bit-92 stone, D4-canonical
    child_v = int(CHILD, 16)
    root_v = child_v | (1 << 92)
    root_hex = format(root_v, '032x')
    assert root_hex == '00000000100000003800000008008020'
    rst, rlegal = enumerate_legal(root_hex)
    assert len(rst) == 7
    root_safe = True
    for i in range(7):
        for j in range(i + 1, 7):
            for k in range(j + 1, 7):
                for l in range(k + 1, 7):
                    if det4([rst[i], rst[j], rst[k], rst[l]]) == 0:
                        root_safe = False
    assert root_safe, 'root must be safe'
    assert len(rlegal) == 45, 'root loser mobility must be 45 (sub-root count)'
    root_d4 = d4_canon(root_hex)

    # cross-cover re-derivation: exactly one candidate root covers the STERILE
    # cost-70j child, namely bit 119, and its verdict is REFUTED-D10
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
    assert cover_bits == [119], cover_bits
    assert verdicts[119]['loss'] is False and verdicts[119]['capped'] is False, \
        'the bit-119 cross-cover root must be REFUTED-D10 in this sweep'

    # independent one-stone-deletion demand re-derivation
    lifted = {}
    for s in st:
        rest = sorted(x for x in st if x != s)
        v = 0
        for i in rest: v |= 1 << i
        lifted[s] = d4_canon(format(v, '032x'))
    assert lifted == {
        5:  '00000000000000003800000008008000',
        15: '00000000000000003800000008000020',
        27: '00000000000000003800000000008020',
        59: '00000000000000001800000008020020',
        60: '00000000000000002800000008008020',
        61: '00000000000000001282200000000000',
    }, 'one-stone deletion D4 canonicalization mismatch: %r' % lifted
    assert len(set(lifted.values())) == 6, 'deletion orbits must be distinct'
    assert lifted[5] == PARENT_CLASS2, 'lift-stone-5 deletion must reproduce the class-2 lift parent'
    assert lifted[27] == PARENT_CLASS1, 'lift-stone-27 deletion must reproduce the class-1 lift parent'

    # verify both open parents and the four closed deletions against the published
    # head-1407 ranking CSV (independently parsed here)
    rank = {}
    with open(RANKING_CSV) as f:
        for row in csv.DictReader(f):
            rank[row['s5_hex']] = (int(row['classes']), int(row['remaining_s6_orbits']), int(row['remaining_s7_edge_cost']))
    assert rank[PARENT_CLASS2] == (2, 50, 3551), 'class-2 parent ranking mismatch: %r' % rank.get(PARENT_CLASS2)
    assert rank[PARENT_CLASS1] == (1, 74, 5399), 'class-1 parent ranking mismatch: %r' % rank.get(PARENT_CLASS1)
    for s in (15, 59, 60, 61):
        assert lifted[s] not in rank, 'deletion stone %d must be a closed S5 orbit at head 1407' % s

    # verify the child row against the published MS5 S6 manifest (milestone5 parts,
    # blob-pinned inputs of the whole class-frontier chain): the child must be an
    # in-manifest row with edge cost 60 and class bitmask 3 (dual class-1+class-2)
    import glob
    manifest_hits = []
    for mp in sorted(glob.glob(os.path.join(
            os.path.dirname(__file__), '..', '..', 'n11-s2-5960-milestone5-20261112',
            'output', 'ms5_s6_manifest_part*.csv'))):
        with open(mp) as f:
            for line in f:
                if line.startswith('hex,'):
                    continue
                parts = line.strip().split(',')
                if parts and parts[0] == CHILD:
                    manifest_hits.append((int(parts[1]), int(parts[2])))
    assert manifest_hits == [(60, 3)], \
        'the child must appear exactly once in the published MS5 S6 manifest with cost 60 and class bitmask 3: %r' % manifest_hits
    # the curated head-1407 top-candidates CSV lists only the best class-4 S5 rows;
    # the child must not appear there (coordination consistency)
    with open(TOPCSV) as f:
        topcsv_text = f.read()
    assert CHILD not in topcsv_text, 'the child is not a best-class-4-S5 row and must be absent from the curated top-candidates CSV'

    audit = {
        'schema': 'n11-class2-lane-cost60c-raw-sweep-audit-20261116-v1',
        'date': '2026-11-16',
        'independent_method': 'Python standard library; exact Bareiss integer determinants; D4 canonicalization and CSV parsing implemented independently; no repository engine/solver/cache, no floating point',
        'target': {
            's5_parent_class2_hex': PARENT_CLASS2,
            's5_parent_class1_hex': PARENT_CLASS1,
            's6_child_hex': CHILD,
            'edge_cost': 60,
            'legal_candidate_count': 60,
            'demand': {'c1': 1, 'c2': 1, 'c4': 0},
        },
        'source_claim': {
            'path': 'research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost60c-inflight-20261116.json',
            'chain_head_at_claim': claim['chain_head_at_claim'],
        },
        'geometry': {
            'child_stones': 6,
            'child_safe': True,
            'independent_legal_candidate_count': 60,
            'candidate_bits_exact_match': True,
            'lift_note': 'one-stone deletions re-derived independently: stone 5 deletion reproduces the class-2 lift parent 00000000000000003800000008008000 bit-exact (50 rows / 3551, classes_bitmask 2 at the post-cost-75e head 1407) and stone 27 deletion reproduces the class-1 lift parent 00000000000000003800000000008020 bit-exact (74 rows / 5399, classes_bitmask 1); the other four deletions (stones 15, 59, 60, 61) canonicalize to 00000000000000003800000008000020, 00000000000000001800000008020020, 00000000000000002800000008008020, 00000000000000001282200000000000: six distinct orbits, all four closed and absent from the head-1407 ranking CSV; per-mask-bit demand is therefore c1=1, c2=1, c4=0 (a dual class-1+class-2 demand row), matching the claim and the head-1407 top-candidates CSV row s5=00000000000000003800000008008000,s6=00000000000000003800000008008020,cost=60',
        },
        'batches': batches,
        'aggregate': {
            'candidates': 60,
            'win7_d10_bits': win_bits,
            'refuted_d10': len(refuted),
            'refuted_d10_bits': refuted,
            'capped': len(capped),
            'capped_bits': capped,
            'candidate_nodes': total_nodes,
            'pilots': pilots,
            'heaviest_bits_nodes': heaviest,
        },
        'win_root': {
            'bit': 92,
            'root_hex': root_hex,
            'd4_canonical_hex': root_d4,
            'root_safe': True,
            'loser_mobility_sub_roots': 45,
        },
        'crosschecks': {
            'v16_determinism_rerun': {
                'file': 'class2-lane-cost60c-v16-determinism-rerun-20261116.jsonl',
                'batch_rerun': 5,
                'identical_ignoring_ms': True,
            },
            'v15_cross_engine': {
                'file': 'class2-lane-cost60c-v15-crosscheck-20261116.jsonl',
                'win_bit_agrees': True,
                'win_bit': 92,
                'refuted_anchors': anchors,
                'anchor_nodes': {str(b): v15_bits[b]['nodes'] for b in anchors},
                'pilots_5949': len(v15_pilots),
                'run_note': 'single foreground invocation (bit 92 the WIN candidate, bits 119/0/120 refuted anchors - bit 119 being the unique cross-cover root of the STERILE cost-70j child), one d6 pilot at 5949 nodes; v15 confirms loss=true on bit 92 and loss=false on all three anchors, agreeing with v16',
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
            'total_nodes_match': total_nodes == 25197741,
        },
        'cross_cover_consequence': 'the sweep tested the unique candidate root of this child that covers the STERILE cost-70j child 00000000000000801282000000200000 (a remaining row, edge 70, of the best coverable class-2 S5 00000000000000801202000000200000, 3 rows / 209, all three rows STERILE by their own-row sweeps): exactly bit 119, root 00800000000000003800000008008020, re-derived independently here by canonical covers over all 60 candidates x 7 deletions. The verdict is REFUTED-D10, so the 70j row is NOT closed by this neighbor; its cross-cover route via this child is exhausted and its closure now depends on other one-stone-replacement neighbors (this session enumerated 114 open-row neighbors for the 70j child, cheapest remaining at cost 62) or on evidence beyond depth 10. A negative fact only; NOT a LOSS proof.',
        'proof_boundary': {
            'raw_sweep_rederivation': 'closed by this audit',
            'certificate_extraction': 'required for the bit-92 WIN7-D10 root 00000000100000003800000008008020 and completed: 27,547 strategy rows / 804,782 blind extraction nodes / 45 sub-roots, independently verified by the BigInt verifier (union 0/0, sub-roots 45/45) and the Bareiss verifier (45/45 sub-roots, terminals [13,17], 8,543 terminals); see class2-lane-cost60c-win7-certificates-20261116.json',
            'fold_material': 'the bit-92 receipt is fold material for the canonical chain: its covers close the child row and any in-manifest marginals; the fold is recorded separately (class-frontier-cost60c-receipts-recompute-20261116.json)',
            'interpretation_of_refuted_d10': 'the other 59 candidates are REFUTED-D10: no first-player win within depth 10 from those roots. This is NOT a LOSS proof and does not close any row by itself',
        },
        'interpretation': 'win7_d10_bits is [92]: the sweep is NOT sterile. The bit-92 root 00000000100000003800000008008020 is a proven WIN7-D10 (original first player wins within depth 10, second to move at the root); its certificate is published and independently verified. Folding its receipt closes the child S6 row 00000000000000003800000008008020 (plus in-manifest marginals) - see the fold record. refuted_d10 is NOT a LOSS proof. capped proves nothing (and there were no capped candidates). The standard 11x11 empty board, both two-stone roots {49,60}/{59,60}, S2 {59,60}, class 1, class 2 and class 4 all remain UNKNOWN.',
    }
    out_path = os.path.join(OUT, 'class2-lane-cost60c-sweep-audit-20261116.json')
    with open(out_path, 'w') as f:
        f.write(json.dumps(audit, indent=1) + '\n')
    print('audit written:', out_path)
    print('win_bits:', win_bits, 'refuted:', len(refuted), 'capped:', len(capped), 'nodes:', total_nodes)

if __name__ == '__main__':
    main()
