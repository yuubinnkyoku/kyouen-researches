#!/usr/bin/env python3
# Independent raw-sweep audit for the class4-lane cost-87 child sweep (three open class-4 parents
# demand c1=0,c2=0,c4=3; the last unswept S6 row of the best class-4 blocker-candidate S5) (2026-11-16).
# Python standard library only; exact integer Bareiss determinants; no floating point,
# no repository solver/engine code. Re-derives the sweep aggregate from the thirteen raw
# artifacts (11 v16 raw batch JSONLs + v16 determinism rerun + v15 crosscheck JSONLs),
# re-enumerates the legal candidates from scratch, re-derives the one-stone-deletion demand
# against the head-1407 ranking CSV, cross-checks the completed claim, and verifies the
# duplicate-claim retirement of the 2026-11-15 cost-86d claim against the 2026-11-14 sweep.
import json, sys, os, hashlib

OUT = os.path.join(os.path.dirname(__file__), '..', 'output')
CLAIM = os.path.join(OUT, 'class4-lane-cost87-inflight-20261114.json')
CHILD = '00000000020000003800000080000004'
BLOCKER = '00000000020000003800000080000000'

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

def md5(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()


def main():
    claim = json.load(open(CLAIM))
    assert claim['s6_child'] == CHILD
    assert claim['s5'] == BLOCKER
    assert claim['s6_s7_edge_cost'] == 87
    assert claim['demand'] == 'c1=0,c2=0,c4=3'
    assert claim['status'] == 'completed'
    assert claim['result']['win7_d10_bits'] == [] and claim['result']['refuted_d10'] == 87 and claim['result']['capped'] == 0
    st, legal = enumerate_legal(CHILD)
    assert st == [2, 31, 59, 60, 61, 89], 'child stones mismatch: %r' % st
    child_safe = True
    for i in range(6):
        for j in range(i + 1, 6):
            for k in range(j + 1, 6):
                for l in range(k + 1, 6):
                    if det4([st[i], st[j], st[k], st[l]]) == 0:
                        child_safe = False
    assert child_safe, 'child must be safe'
    assert legal == claim['candidate_bits'], 'independent enumeration != claim list'
    assert len(legal) == 87

    batches = []
    verdicts = {}
    total_nodes = 0
    pilots = 0
    raw_files = []
    for n in range(1, 12):
        p = os.path.join(OUT, 'class4-lane-cost87-raw-batch%d-20261116.jsonl' % n)
        rows = load_jsonl(p)
        ctrl = [r for r in rows if 'control' in r]
        cand = [r for r in rows if 'bit' in r]
        assert len(ctrl) == len(cand), 'pilot control count != candidate count in batch %d' % n
        assert all(r['nodes'] == 3402 and r['loss'] is False for r in ctrl), 'bad pilot control in batch %d' % n
        pilots += len(ctrl)
        bits = [r['bit'] for r in cand]
        assert bits == claim['engine']['batch_bits']['batch%d' % n], 'batch %d bits != claim engine batch_bits' % n
        for r in cand:
            assert r['bit'] not in verdicts, 'duplicate bit'
            assert r['bit'] in legal, 'bit not in enumeration'
            assert r.get('andclose') is True, 'andclose not true on bit %r' % r['bit']
            verdicts[r['bit']] = r
            total_nodes += r['nodes']
            tsr = r['terminalStoneRange']
            assert tsr[0] >= 7 and tsr[1] <= 17, 'terminal stone range outside depth-10 bounds (7-stone root, 10 plies)'
        batches.append({'batch': n, 'file': os.path.basename(p),
                        'candidate_bits': bits, 'pilot_lines': len(ctrl),
                        'nodes': sum(r['nodes'] for r in cand)})
        raw_files.append({'file': os.path.basename(p), 'md5': md5(p)})
    assert set(verdicts.keys()) == set(legal), 'candidate set mismatch'
    win_bits = sorted(b for b, r in verdicts.items() if r['loss'])
    capped = sorted(b for b, r in verdicts.items() if r['capped'])
    refuted = sorted(b for b, r in verdicts.items() if (not r['loss']) and (not r['capped']))
    assert len(win_bits) + len(refuted) + len(capped) == 87
    assert not capped, 'capped candidates present: %r' % capped
    assert win_bits == [], 'unexpected win bits: %r' % win_bits
    assert total_nodes == claim['result']['candidate_nodes'] == 142614947, 'total nodes mismatch vs completed claim'

    # determinism rerun: batch 5 bits must agree (ignoring ms)
    det_path = os.path.join(OUT, 'class4-lane-cost87-v16-determinism-rerun-20261116.jsonl')
    det = load_jsonl(det_path)
    det_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'], tuple(r['terminalStoneRange'])) for r in det if 'bit' in r}
    b5_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'], tuple(r['terminalStoneRange']))
               for r in load_jsonl(os.path.join(OUT, 'class4-lane-cost87-raw-batch5-20261116.jsonl')) if 'bit' in r}
    assert det_bits == b5_bits, 'determinism rerun mismatch'
    det_pilots = [r for r in det if 'control' in r]
    assert len(det_pilots) == 8 and all(r['nodes'] == 3402 and r['loss'] is False for r in det_pilots)

    # v15 cross-engine agreement (3 heaviest REFUTED anchors)
    v15_path = os.path.join(OUT, 'class4-lane-cost87-v15-crosscheck-20261116.jsonl')
    v15 = load_jsonl(v15_path)
    v15_pilots = [r for r in v15 if 'control' in r]
    assert all(r['nodes'] == 5949 and r['loss'] is False for r in v15_pilots)
    v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
    assert sorted(v15_bits) == [6, 28, 110], 'unexpected v15 anchors: %r' % sorted(v15_bits)
    for b in v15_bits:
        assert v15_bits[b]['loss'] is False, 'v15 found a WIN the raw sweep missed'
        assert verdicts[b]['loss'] is False, 'raw verdict disagreement'
    assert all(r.get('andclose') is True for r in v15 if 'bit' in r), 'v15 anchors andclose not true'

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

    # head-1407 ranking CSV: open S5 set + parent rows
    ranking = {}
    with open(os.path.join(OUT, 'class-frontier-s5-ranking-after-cost75e-receipts-20261116.csv')) as f:
        f.readline()
        for line in f:
            parts = line.strip().split(',')
            ranking[parts[0]] = (int(parts[1]), int(parts[2]), int(parts[3]))
    assert len(ranking) == 174, 'ranking open count mismatch: %d' % len(ranking)

    # one-stone deletion D4 canonicalization
    lifted = {}
    for s in st:
        rest = sorted(x for x in st if x != s)
        v = 0
        for i in rest:
            v |= 1 << i
        lifted[s] = d4_canon(format(v, '032x'))
    assert lifted[2] == BLOCKER, 'del-2 must be parent1 (best class-4 blocker S5): %r' % lifted[2]
    assert lifted[31] == '00000000000000801002000000480000', 'del-31 mismatch: %r' % lifted[31]
    assert lifted[89] == '00000000000000003800000000800100', 'del-89 mismatch: %r' % lifted[89]
    for s in (59, 60, 61):
        assert lifted[s] not in ranking, 'deletion of stone %d expected closed but open: %r' % (s, lifted[s])
    assert ranking[BLOCKER] == (4, 18, 1460), 'parent1 row mismatch'
    assert ranking['00000000000000801002000000480000'] == (4, 89, 7577), 'parent2 row mismatch'
    assert ranking['00000000000000003800000000800100'] == (4, 90, 7775), 'parent3 row mismatch'

    # top-candidates CSV: the blocker S5's 18 rows incl. this child, demand row
    tc_lines = open(os.path.join(OUT, 'class-frontier-top-candidates-s6-after-cost75e-receipts-20261116.csv')).read().splitlines()
    blocker_rows = [l for l in tc_lines if l.startswith(BLOCKER + ',')]
    assert len(blocker_rows) == 18, 'blocker S5 must have 18 listed rows: %d' % len(blocker_rows)
    row = [l for l in blocker_rows if l.startswith(BLOCKER + ',' + CHILD + ',')]
    assert len(row) == 1, 'child row not unique in top-candidates CSV'
    assert row[0].endswith('"c1=0,c2=0,c4=3"'), 'demand mismatch: %r' % row[0]
    assert row[0].split(',')[2] == '87', 'edge cost mismatch: %r' % row[0]

    # duplicate-claim retirement check: 2026-11-15 cost-86d claim vs 2026-11-14 sweep
    s14 = json.load(open(os.path.join(OUT, 'class4-lane-cost86d-sweep-20261114.json')))
    c15 = json.load(open(os.path.join(OUT, 'class4-lane-cost86d-inflight-20261115.json')))
    assert s14['target']['s6_child_hex'] == c15['s6_child'] == '00000000020000003800100080000000'
    assert s14['target']['class4_lane_target_s5'] == BLOCKER
    assert s14['candidate_count'] == 86
    assert s14['summary']['win7_d10'] == [] and len(s14['summary']['refuted_d10']) == 86 and s14['summary']['capped'] == []
    assert s14['summary']['total_nodes'] == 315578134
    assert s14['summary']['refuted_d10'] == c15['legal_candidates'], '11-15 claim candidate list != 11-14 sweep candidate list'
    assert c15['status'] == 'superseded_duplicate'
    dup_st, dup_legal = enumerate_legal('00000000020000003800100080000000')
    assert dup_st == [31, 44, 59, 60, 61, 89] and dup_legal == s14['summary']['refuted_d10'], 'independent re-enumeration of the 86d child failed'

    audit = {
        'schema': 'n11-class4-lane-cost87-raw-sweep-audit-20261116-v1',
        'date': '2026-11-16',
        'independent_method': ('Python standard library; exact Bareiss integer determinants; D4 canonicalization and legal-candidate '
            'enumeration helpers reused verbatim from the published cost-70d/70e/84 audit scripts (same session series, published on main); '
            'raw-record parsing, aggregate re-derivation, batch-bit cross-check, determinism/v15 crosschecks, one-stone-deletion '
            're-derivation, head-1407 CSV cross-checks and the 86d duplicate-claim verification written fresh for cost-87; '
            'no repository engine/solver/cache, no floating point'),
        'target': {
            's5_hex': BLOCKER,
            's6_child_hex': CHILD,
            'edge_cost': 87,
            'legal_candidate_count': 87,
            'demand': {'c1': 0, 'c2': 0, 'c4': 3},
        },
        'source_claim': {
            'path': 'research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class4-lane-cost87-inflight-20261114.json',
            'status': 'completed',
            'chain_head_at_sweep': '1407/174/6441/509300/4711/373023 (class-frontier-cost75e-receipts-recompute-20261116.json, git blob sha 5cd93de7ee8943681549b8f97918f6112548b373, commit dd623408)',
        },
        'geometry': {
            'child_stones': 6,
            'child_stone_bits': st,
            'child_safe': True,
            'independent_legal_candidate_count': 87,
            'candidate_bits_exact_match': True,
            'lift_note': ('one-stone deletions re-derived independently: stone 2 deletion reproduces the best class-4 blocker-candidate '
                'S5 00000000020000003800000080000000 bit-exact (18 rows / 1460 at head 1407), stone 31 deletion D4-canonicalizes to the open '
                'class-4 S5 00000000000000801002000000480000 (89 rows / 7577 at head 1407) and stone 89 deletion to the open class-4 S5 '
                '00000000000000003800000000800100 (90 rows / 7775 at head 1407); the remaining three deletions (stones 59/60/61) are closed '
                'rows absent from the head-1407 ranking CSV; per-class demand c1=0,c2=0,c4=3 matches the published head-1407 top-candidates CSV row'),
        },
        'batches': batches,
        'raw_file_md5_pins': raw_files + [
            {'file': 'class4-lane-cost87-v16-determinism-rerun-20261116.jsonl', 'md5': md5(det_path)},
            {'file': 'class4-lane-cost87-v15-crosscheck-20261116.jsonl', 'md5': md5(v15_path)},
        ],
        'aggregate': {
            'candidates': 87,
            'win7_d10_bits': win_bits,
            'refuted_d10': len(refuted),
            'refuted_d10_bits': refuted,
            'capped': len(capped),
            'capped_bits': capped,
            'candidate_nodes': total_nodes,
            'pilots': pilots,
            'andclose_true_all': True,
        },
        'crosschecks': {
            'v16_determinism_rerun': {
                'file': 'class4-lane-cost87-v16-determinism-rerun-20261116.jsonl',
                'batch_rerun': 5,
                'identical_ignoring_ms': True,
            },
            'v15_cross_engine': {
                'file': 'class4-lane-cost87-v15-crosscheck-20261116.jsonl',
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
            'andclose_true_on_every_candidate': True,
            'pilot_3402_per_candidate_fresh_process': True,
            'determinism_rerun_node_exact': True,
            'v15_cross_engine_agreement': True,
            'independent_enumeration_matches_claim': True,
            'one_stone_deletion_d4_canonicalization_verified': True,
            'parent_rows_match_head1407_ranking_csv': True,
            'demand_matches_head1407_top_candidates_csv': True,
            'blocker_s5_listed_rows_18': True,
        },
        'duplicate_claim_retirement_check': {
            'retired_claim': 'class4-lane-cost86d-inflight-20261115.json',
            'status': 'superseded_duplicate',
            'prior_sweep': 'class4-lane-cost86d-sweep-20261114.json (86/86 REFUTED-D10, 315,578,134 nodes, STERILE, published 2026-11-14)',
            'child_hex_identical': True,
            'candidate_list_bit_exact_identical': True,
            'independent_reenumeration_86_matches': True,
            'no_conflicting_evidence': True,
            'note': ('the 2026-11-15 claim duplicated an already-published 2026-11-14 sweep; no raw batches ran under the duplicate claim, '
                'no computation was wasted, no evidence conflict; the claim is retired in the same push as this audit'),
        },
        'proof_boundary': {
            'raw_sweep_rederivation': 'closed by this audit (aggregate, batch bits, verdicts, nodes re-derived from the raw JSONLs)',
            'certificate_extraction': 'not required: the sweep is sterile (no WIN7-D10 bits)',
            'fold_material': 'none: no receipts, the canonical chain frontier is unchanged at head 1407/174/6441/509300/4711/373023 (the parallel cost-60c WIN7 fold and the cost-76d/77e folds are separate lanes and do not touch this child or its parents)',
            'interpretation_of_refuted_d10': ('all 87 candidates are REFUTED-D10: no first-player win within depth 10 from any of the 87 '
                'seven-stone roots. This is NOT a LOSS proof for those roots and does not close the child S6 row; closing this child row '
                'requires evidence beyond depth 10'),
        },
        'interpretation': ('win7_d10_bits is empty: the sweep is sterile. With it, all 18 open S6 rows of the best class-4 blocker-candidate '
            'S5 00000000020000003800000080000000 are swept REFUTED-D10 (73f,74f,74c,75,79,79b,80,80c,81,82,82b,84,86a,86b,86c,86d,86e,87): '
            'the S5 is unclosable by depth-10 WIN7 receipts - a negative structural fact only, NOT a LOSS proof; the row remains open on the '
            'class-4 frontier until closed by other evidence or deeper search. The next class-4 candidates by the head-1407 ranking are '
            '000000000000003800002000800000 (60 rows / 4216), 00000000020000003800000000080000 (61 rows / 4351) and '
            '00000000000000801802000000080000 (64 rows / 4390). REFUTED-D10 is NOT a LOSS proof. The standard 11x11 empty board, both '
            'two-stone roots {49,60}/{59,60}, S2 {59,60}, class 1, class 2 and class 4 all remain UNKNOWN.'),
    }
    out_path = os.path.join(OUT, 'class4-lane-cost87-raw-sweep-audit-20261116.json')
    with open(out_path, 'w') as f:
        f.write(json.dumps(audit, indent=1) + '\n')
    print('audit written:', out_path)
    print('win_bits:', win_bits, 'refuted:', len(refuted), 'capped:', len(capped), 'nodes:', total_nodes)

if __name__ == '__main__':
    main()
