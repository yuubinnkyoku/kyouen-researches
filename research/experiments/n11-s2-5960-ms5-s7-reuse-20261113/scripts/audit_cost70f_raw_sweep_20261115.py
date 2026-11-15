#!/usr/bin/env python3
# Independent raw-sweep audit for the class2-lane cost-70f child sweep (2026-11-15).
# Child 00000000000000801202000002200000 (second coverable class-2 target S5,
# both open parents class 2, demand c1=0,c2=2,c4=0, edge cost 70).
# Python standard library only; exact integer Bareiss determinants; no floating
# point, no repository solver/engine code.  Re-derives the sweep aggregate from
# the nine v16 raw batch JSONLs, re-enumerates the legal candidates from
# scratch, and cross-checks the claim, the determinism rerun and the v15
# cross-engine anchors.
import glob
import json
import os
import re

OUT = os.path.join(os.path.dirname(__file__), '..', 'output')
CLAIM = os.path.join(OUT, 'class2-lane-cost70f-inflight-20261115.json')
CHILD = '00000000000000801202000002200000'
WIN_BITS = [9, 64, 72, 84]
REFUTED_ANCHORS = [1, 32, 116]


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
    x = cell % 11
    y = cell // 11
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
                if unsafe:
                    break
            if unsafe:
                break
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
                    if fx:
                        a = 10 - a
                    if fy:
                        b = 10 - b
                    t.append(a + 11 * b)
                v = 0
                for i in t:
                    v |= 1 << i
                h = format(v, '032x')
                if best is None or h < best:
                    best = h
    return best


def load_jsonl(path):
    return [json.loads(line) for line in open(path) if line.strip()]


def main():
    claim = json.load(open(CLAIM))
    assert claim['s6_child'] == CHILD
    assert claim['s6_s7_edge_cost'] == 70
    assert claim['demand'] == {'c1': 0, 'c2': 2, 'c4': 0}
    st, legal = enumerate_legal(CHILD)
    assert st == [21, 25, 49, 57, 60, 71], 'child stones mismatch: %r' % st
    for i in range(6):
        for j in range(i + 1, 6):
            for k in range(j + 1, 6):
                for l in range(k + 1, 6):
                    assert det4([st[i], st[j], st[k], st[l]]) != 0, 'child unsafe'
    assert legal == claim['legal_candidates'], 'independent enumeration != claim'
    assert len(legal) == 70

    batches = []
    verdicts = {}
    total_nodes = 0
    pilots = 0
    for n in range(1, 10):
        p = os.path.join(OUT, 'class2-lane-cost70f-raw-batch%d-20261115.jsonl' % n)
        rows = load_jsonl(p)
        ctrl = [r for r in rows if 'control' in r]
        cand = [r for r in rows if 'bit' in r]
        assert len(ctrl) == 1 and ctrl[0]['nodes'] == 3402 and ctrl[0]['loss'] is False
        pilots += 1
        bits = [r['bit'] for r in cand]
        assert bits == claim['engine']['batch_bits']['batch%d' % n], 'batch %d bits' % n
        for r in cand:
            assert r['bit'] not in verdicts, 'duplicate bit'
            assert r['bit'] in legal, 'bit not in enumeration'
            verdicts[r['bit']] = r
            total_nodes += r['nodes']
            tsr = r['terminalStoneRange']
            assert tsr[0] >= 7 and tsr[1] <= 17, 'terminal range outside depth-10 bounds'
        batches.append({'batch': n, 'file': os.path.basename(p),
                        'candidate_bits': bits, 'pilot_nodes': 3402,
                        'nodes': sum(r['nodes'] for r in cand)})
    assert set(verdicts) == set(legal), 'candidate set mismatch'
    win_bits = sorted(b for b, r in verdicts.items() if r['loss'])
    capped = sorted(b for b, r in verdicts.items() if r['capped'])
    refuted = sorted(b for b, r in verdicts.items() if (not r['loss']) and (not r['capped']))
    assert len(win_bits) + len(refuted) + len(capped) == 70
    assert not capped, 'capped candidates: %r' % capped
    assert win_bits == WIN_BITS, 'unexpected win bits: %r' % win_bits

    det = load_jsonl(os.path.join(OUT, 'class2-lane-cost70f-v16-determinism-rerun-20261115.jsonl'))
    det_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'], tuple(r['terminalStoneRange']))
                for r in det if 'bit' in r}
    b5_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'], tuple(r['terminalStoneRange']))
               for r in load_jsonl(os.path.join(OUT, 'class2-lane-cost70f-raw-batch5-20261115.jsonl'))
               if 'bit' in r}
    assert det_bits == b5_bits, 'determinism rerun mismatch'
    det_pilot = [r for r in det if 'control' in r][0]
    assert det_pilot['nodes'] == 3402 and det_pilot['loss'] is False

    v15 = load_jsonl(os.path.join(OUT, 'class2-lane-cost70f-v15-crosscheck-20261115.jsonl'))
    v15_pilots = [r for r in v15 if 'control' in r]
    assert all(r['nodes'] == 5949 and r['loss'] is False for r in v15_pilots)
    v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
    for b in win_bits:
        assert b in v15_bits and v15_bits[b]['loss'] is True, 'v15 disagrees on WIN bit'
    for b in REFUTED_ANCHORS:
        assert b in v15_bits and v15_bits[b]['loss'] is False, 'v15 anchor disagreement'
    assert set(v15_bits) == set(win_bits) | set(REFUTED_ANCHORS)

    child_v = int(CHILD, 16)
    roots = {}
    for b in win_bits:
        rh = format(child_v | (1 << b), '032x')
        rst, rmob = enumerate_legal(rh)
        assert len(rst) == 7
        roots[b] = {'root_hex': rh, 'd4_canonical_hex': d4_canon(rh),
                    'root_mobility': len(rmob)}
    canon_list = [roots[b]['d4_canonical_hex'] for b in win_bits]
    assert len(set(canon_list)) == len(canon_list), 'WIN roots share a D4 orbit'

    pub_canon = set()
    manifests = sorted(glob.glob(os.path.join(OUT, '*win7-certificates*.json')))
    scanned = 0
    for f in manifests:
        if 'cost65k' in f or 'cost73f' in f:
            continue
        try:
            d = json.load(open(f))
        except Exception:
            continue
        scanned += 1
        s = json.dumps(d)
        for m in re.findall(r'"(?:root_hex|d4_canonical_hex)"\s*:\s*"([0-9a-f]{32})"', s):
            pub_canon.add(d4_canon(m))
    assert not [c for c in canon_list if c in pub_canon], 'D4 duplicate vs published manifests'

    ranking = {}
    with open(os.path.join(OUT, 'class-frontier-s5-ranking-after-cost70e-receipts-20261115.csv')) as f:
        f.readline()
        for line in f:
            parts = line.strip().split(',')
            ranking[parts[0]] = (int(parts[1]), int(parts[2]), int(parts[3]))
    assert len(ranking) == 175, 'ranking open count mismatch: %d' % len(ranking)

    lifted = {}
    for s in st:
        rest = sorted(x for x in st if x != s)
        v = 0
        for i in rest:
            v |= 1 << i
        lifted[s] = d4_canon(format(v, '032x'))
    assert lifted[25] == '00000000000000801202000000200000', 'del-25 parent1: %r' % lifted[25]
    assert lifted[21] == '00000000000000003800000808000000', 'del-21 parent2: %r' % lifted[21]
    for s in (49, 57, 60, 71):
        assert lifted[s] not in ranking, 'deletion %d expected closed but open' % s
    assert ranking['00000000000000801202000000200000'] == (2, 28, 2119), 'parent1 row'
    assert ranking['00000000000000003800000808000000'] == (2, 57, 4272), 'parent2 row'

    tc_lines = open(os.path.join(OUT, 'class-frontier-top-candidates-s6-after-cost70e-receipts-20261115.csv')).read().splitlines()
    row = [l for l in tc_lines
           if l.startswith('00000000000000801202000000200000,00000000000000801202000002200000,')]
    assert len(row) == 1, 'child row not unique in top-candidates CSV'
    assert row[0].endswith('"c1=0,c2=2,c4=0"'), 'demand mismatch: %r' % row[0]
    assert row[0].split(',')[2] == '70', 'edge cost mismatch: %r' % row[0]

    audit = {
        'schema': 'n11-class2-lane-cost70f-raw-sweep-audit-20261115-v1',
        'date': '2026-11-15',
        'independent_method': ('Python standard library; exact Bareiss integer determinants; '
                               'D4 canonicalization and legal-candidate enumeration helpers reused '
                               'from the published cost-70d/70e audit scripts (same session series); '
                               'raw parsing, aggregate re-derivation, batch-bit cross-check, WIN-root '
                               'scan, one-stone-deletion re-derivation and CSV cross-checks written '
                               'for cost-70f; no repository engine/solver/cache, no floating point'),
        'target': {
            's5_hex': claim['s5'],
            's6_child_hex': CHILD,
            'edge_cost': 70,
            'legal_candidate_count': 70,
            'demand': {'c1': 0, 'c2': 2, 'c4': 0},
        },
        'source_claim': {
            'path': 'research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost70f-inflight-20261115.json',
            'chain_head_at_claim': claim['chain_head_at_claim'],
        },
        'geometry': {
            'child_stones': 6,
            'child_stone_bits': st,
            'child_safe': True,
            'independent_legal_candidate_count': 70,
            'candidate_bits_exact_match': True,
            'lift_note': ('one-stone deletions re-derived independently: stone 25 deletion '
                          'reproduces the second coverable class-2 target S5 '
                          '00000000000000801202000000200000 bit-exact (28 rows / 2119 at head '
                          '1233) and stone 21 deletion D4-canonicalizes to the open class-2 S5 '
                          '00000000000000003800000808000000 (57 rows / 4272 at head 1233); the '
                          'remaining four deletions (stones 49/57/60/71) are closed rows absent '
                          'from the head-1233 ranking CSV; per-class demand c1=0,c2=2,c4=0 '
                          'matches the published head-1233 top-candidates CSV row'),
        },
        'batches': batches,
        'aggregate': {
            'candidates': 70,
            'win7_d10_bits': win_bits,
            'win7_d10_nodes': {str(b): verdicts[b]['nodes'] for b in win_bits},
            'refuted_d10': len(refuted),
            'refuted_d10_bits': refuted,
            'capped': len(capped),
            'capped_bits': capped,
            'candidate_nodes': total_nodes,
            'pilots': pilots,
        },
        'win_roots': {str(b): roots[b] for b in win_bits},
        'd4_duplicate_scan': {
            'roots_compared': len(pub_canon),
            'manifest_files_scanned': scanned,
            'duplicates': 0,
        },
        'crosschecks': {
            'v16_determinism_rerun': {
                'file': 'class2-lane-cost70f-v16-determinism-rerun-20261115.jsonl',
                'batch_rerun': 5,
                'identical_ignoring_ms': True,
            },
            'v15_cross_engine': {
                'file': 'class2-lane-cost70f-v15-crosscheck-20261115.jsonl',
                'win_bits_agree': True,
                'refuted_anchors': sorted(REFUTED_ANCHORS),
                'anchor_nodes': {str(b): v15_bits[b]['nodes'] for b in REFUTED_ANCHORS},
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
            'parent_rows_match_head1233_ranking_csv': True,
            'demand_matches_head1233_top_candidates_csv': True,
            'win_root_d4_orbits_distinct': True,
            'win_root_d4_orbits_new_vs_published_manifests': True,
        },
        'proof_boundary': {
            'raw_sweep_rederivation': 'closed by this audit',
            'certificate_extraction': ('pending: 4 WIN7-D10 roots (bits 9/64/72/84) are fold '
                                       'material candidates; folding requires published, '
                                       'independently verified WIN7 certificates first'),
            'fold_material': 'none usable yet: certificates not published at audit time; the '
                             'canonical chain frontier stays at 1233/6614/522131/4884/385854',
            'interpretation_of_refuted_d10': ('all 66 non-WIN candidates are REFUTED-D10: no '
                                              'first-player win within depth 10 from those '
                                              'seven-stone roots. This is NOT a LOSS proof and '
                                              'does not close the child S6 row'),
        },
        'interpretation': ('win7_d10_bits is [9, 64, 72, 84]: the sweep is NOT sterile. The v16 '
                           'determinism rerun (batch 5) is node-exact and the v15 cross-engine '
                           'agrees on all 4 WIN bits (loss=true) and the 3 REFUTED anchors '
                           '(bits 1/32/116, loss=false). The 4 WIN roots are new (no D4 duplicate '
                           'vs the %d published certificate-manifest canonical roots scanned), so '
                           'certificate extraction for these 4 roots would add new fold material; '
                           'until verified certificates are published, no fold may be run and the '
                           'frontier is unchanged. REFUTED-D10 is NOT a LOSS proof. The standard '
                           '11x11 empty board, both two-stone roots {49,60}/{59,60}, S2 {59,60}, '
                           'class 1, class 2 and class 4 all remain UNKNOWN.') % len(pub_canon),
    }
    out_path = os.path.join(OUT, 'class2-lane-cost70f-sweep-audit-20261115.json')
    with open(out_path, 'w', newline='\n') as f:
        f.write(json.dumps(audit, indent=1) + '\n')
    print('audit written:', out_path)
    print('win_bits:', win_bits, 'refuted:', len(refuted), 'capped:', len(capped),
          'nodes:', total_nodes)
    print('pub_canon roots:', len(pub_canon), 'manifest files scanned:', scanned)


if __name__ == '__main__':
    main()
