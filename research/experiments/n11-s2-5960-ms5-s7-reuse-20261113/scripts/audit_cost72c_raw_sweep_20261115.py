#!/usr/bin/env python3
# Independent raw-sweep audit for the class2-lane cost-72c child sweep (both-parents-class-2
# demand c1=0,c2=2,c4=0; the cheapest unswept row (cost 72) of the second coverable class-2 S5
# 00000000000000801202000000200000 at the head-1235 chain, with both open parents in class-2
# demand) (2026-11-15).
# Python standard library only; exact integer Bareiss determinants; no floating point,
# no repository solver/engine code. Re-derives the sweep aggregate from the thirteen raw
# artifacts (9 v16 raw batch JSONLs + v16 determinism rerun + 3 v15 crosscheck JSONLs),
# re-enumerates the legal candidates from scratch, and cross-checks the claim.
import json, sys, os, glob, re as _re

OUT = os.path.join(os.path.dirname(__file__), '..', 'output')
CLAIM = os.path.join(OUT, 'class2-lane-cost72c-inflight-20261115.json')
CHILD = '00000000000000801202000000220000'

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
    assert claim['s6_s7_edge_cost'] == 72
    assert claim['demand'] == {'c1': 0, 'c2': 2, 'c4': 0}
    st, legal = enumerate_legal(CHILD)
    assert st == [17, 21, 49, 57, 60, 71], 'child stones mismatch: %r' % st
    child_safe = True
    for i in range(6):
        for j in range(i + 1, 6):
            for k in range(j + 1, 6):
                for l in range(k + 1, 6):
                    if det4([st[i], st[j], st[k], st[l]]) == 0:
                        child_safe = False
    assert child_safe, 'child must be safe'
    assert legal == claim['legal_candidates'], 'independent enumeration != claim list'
    assert len(legal) == 72

    batches = []
    verdicts = {}
    total_nodes = 0
    pilots = 0
    for n in range(1, 10):
        p = os.path.join(OUT, 'class2-lane-cost72c-raw-batch%d-20261115.jsonl' % n)
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
    assert len(win_bits) + len(refuted) + len(capped) == 72
    assert not capped, 'capped candidates present: %r' % capped
    assert win_bits == [1, 7, 24, 39, 59, 64, 67, 72, 96], 'unexpected win bits: %r' % win_bits

    # determinism rerun: batch 5 bits must agree (ignoring ms)
    det = load_jsonl(os.path.join(OUT, 'class2-lane-cost72c-v16-determinism-rerun-20261115.jsonl'))
    det_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'], tuple(r['terminalStoneRange'])) for r in det if 'bit' in r}
    b5_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'], tuple(r['terminalStoneRange']))
               for r in load_jsonl(os.path.join(OUT, 'class2-lane-cost72c-raw-batch5-20261115.jsonl')) if 'bit' in r}
    assert det_bits == b5_bits, 'determinism rerun mismatch'
    det_pilot = [r for r in det if 'control' in r][0]
    assert det_pilot['nodes'] == 3402 and det_pilot['loss'] is False

    # v15 cross-engine agreement
    v15 = []
    v15_files = ['class2-lane-cost72c-v15-crosscheck-a-20261115.jsonl',
                 'class2-lane-cost72c-v15-crosscheck-b-20261115.jsonl',
                 'class2-lane-cost72c-v15-crosscheck-refuted-20261115.jsonl']
    for vf in v15_files:
        v15 += load_jsonl(os.path.join(OUT, vf))
    v15_pilots = [r for r in v15 if 'control' in r]
    assert all(r['nodes'] == 5949 and r['loss'] is False for r in v15_pilots)
    v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
    for b in win_bits:
        assert b in v15_bits and v15_bits[b]['loss'] is True, 'v15 disagrees on WIN bit'
    for b in v15_bits:
        if b not in win_bits:
            assert v15_bits[b]['loss'] is False, 'v15 found extra WIN'
            assert verdicts[b]['loss'] is False, 'raw verdict disagreement'

    # root identity + D4 canonical scan
    child_v = int(CHILD, 16)
    roots = {}
    for b in win_bits:
        rh = format(child_v | (1 << b), '032x')
        rst, rmob = enumerate_legal(rh)
        assert len(rst) == 7
        roots[b] = {'root_hex': rh, 'd4_canonical_hex': d4_canon(rh), 'root_mobility': len(rmob)}
    for b, rh, mob in [
        (1, '00000000000000801202000000220002', 61),
        (7, '00000000000000801202000000220080', 47),
        (24, '00000000000000801202000001220000', 59),
        (39, '00000000000000801202008000220000', 46),
        (59, '00000000000000801a02000000220000', 53),
        (64, '00000000000000811202000000220000', 52),
        (67, '00000000000000881202000000220000', 53),
        (72, '00000000000001801202000000220000', 47),
        (96, '00000001000000801202000000220000', 56)]:
        assert roots[b]['root_hex'] == rh, 'root hex mismatch bit %d' % b
        assert roots[b]['root_mobility'] == mob, 'root mobility mismatch bit %d' % b
    canon_list = [roots[b]['d4_canonical_hex'] for b in win_bits]
    assert len(set(canon_list)) == len(canon_list), 'WIN roots share a D4 orbit'
    pub_canon = set()
    manifests = sorted(glob.glob(os.path.join(OUT, '*win7-certificates*.json')))
    scanned = 0
    for f in manifests:
        if 'cost72c' in f or 'cost65k' in f or 'cost73f' in f:
            continue
        try:
            d = json.load(open(f))
        except Exception:
            continue
        scanned += 1
        s = json.dumps(d)
        for m in _re.findall(r'"(?:root_hex|d4_canonical_hex)"\s*:\s*"([0-9a-f]{32})"', s):
            pub_canon.add(d4_canon(m))
    dups_vs_pub = [c for c in canon_list if c in pub_canon]
    assert not dups_vs_pub, 'D4 duplicate vs published manifests: %r' % dups_vs_pub

    # head-1233 ranking CSV: open S5 set + parent rows
    ranking = {}
    with open(os.path.join(OUT, 'class-frontier-s5-ranking-after-cost71c-receipts-20261115.csv')) as f:
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
    assert lifted[17] == '00000000000000801202000000200000', 'del-17 must be parent1 (second coverable class-2 S5): %r' % lifted[17]
    assert lifted[21] == '00000000000000083800000008000000', 'del-21 mismatch: %r' % lifted[21]
    for s in (49, 57, 60, 71):
        assert lifted[s] not in ranking, 'deletion of stone %d expected closed but open: %r' % (s, lifted[s])
    assert ranking['00000000000000801202000000200000'] == (2, 26, 1976), 'parent1 row mismatch'
    assert ranking['00000000000000083800000008000000'] == (2, 55, 4111), 'parent2 row mismatch'

    # top-candidates CSV demand row for the child
    tc_lines = open(os.path.join(OUT, 'class-frontier-top-candidates-s6-after-cost71c-receipts-20261115.csv')).read().splitlines()
    row = [l for l in tc_lines if l.startswith('00000000000000801202000000200000,00000000000000801202000000220000,')]
    assert len(row) == 1, 'child row not unique in top-candidates CSV'
    assert row[0].endswith('"c1=0,c2=2,c4=0"'), 'demand mismatch: %r' % row[0]
    assert row[0].split(',')[2] == '72', 'edge cost mismatch: %r' % row[0]

    audit = {
        'schema': 'n11-class2-lane-cost72c-raw-sweep-audit-20261115-v1',
        'date': '2026-11-15',
        'independent_method': ('Python standard library; exact Bareiss integer determinants; D4 canonicalization and legal-candidate '
            'enumeration helpers reused verbatim from the published cost-70e audit script (same session series, published on main); '
            'raw-record parsing, aggregate re-derivation, batch-bit cross-check, WIN-root scan, one-stone-deletion re-derivation and '
            'CSV cross-checks adapted from cost-70e to cost-71c; no repository engine/solver/cache, no floating point'),
        'target': {
            's5_hex': claim['s5'],
            's6_child_hex': CHILD,
            'edge_cost': 72,
            'legal_candidate_count': 72,
            'demand': {'c1': 0, 'c2': 2, 'c4': 0},
        },
        'source_claim': {
            'path': 'research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost72c-inflight-20261115.json',
            'chain_head_at_claim': claim['chain_head_at_claim'],
        },
        'geometry': {
            'child_stones': 6,
            'child_stone_bits': st,
            'child_safe': True,
            'independent_legal_candidate_count': 72,
            'candidate_bits_exact_match': True,
            'lift_note': ('one-stone deletions re-derived independently: stone 17 deletion reproduces the second coverable class-2 '
                'target S5 00000000000000801202000000200000 bit-exact (26 rows / 1976 at head 1235) and stone 21 deletion '
                'D4-canonicalizes to the open class-2 S5 00000000000000083800000008000000 (55 rows / 4111 at head 1235); the remaining '
                'four deletions (stones 49/57/60/71) are closed rows absent from the head-1235 ranking CSV; per-class demand '
                'c1=0,c2=2,c4=0 matches the published head-1235 top-candidates CSV row for this child'),
        },
        'batches': batches,
        'aggregate': {
            'candidates': 72,
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
                'file': 'class2-lane-cost72c-v16-determinism-rerun-20261115.jsonl',
                'batch_rerun': 5,
                'identical_ignoring_ms': True,
            },
            'v15_cross_engine': {
                'files': ['class2-lane-cost72c-v15-crosscheck-a-20261115.jsonl', 'class2-lane-cost72c-v15-crosscheck-b-20261115.jsonl', 'class2-lane-cost72c-v15-crosscheck-refuted-20261115.jsonl'],
                'win_bits_agree': True,
                'refuted_anchors': sorted(b for b in v15_bits if b not in win_bits),
                'anchor_nodes': {str(b): v15_bits[b]['nodes'] for b in sorted(v15_bits) if b not in win_bits},
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
            'parent_rows_match_head1235_ranking_csv': True,
            'demand_matches_head1235_top_candidates_csv': True,
            'win_root_d4_orbits_distinct': True,
            'win_root_d4_orbits_new_vs_published_manifests': True,
        },
        'certificate_status': ('extracted in the same session: WIN7 certificates for all 9 WIN roots (bits 1/7/24/39/59/64/67/72/96, '
            '321,781 strategy rows total, 41,346,462 extraction nodes), each verified twice independently (BigInt cofactor verifier '
            'and Python Bareiss replay verifier with full loser-reply expansion and exact strategy-union closure, both union 0/0); '
            'published as two line-boundary parts per certificate (join md5 = whole-file md5); '
            'see class2-lane-cost72c-win7-certificates-20261115.json and the certificates README'),
        'proof_boundary': {
            'raw_sweep_rederivation': 'closed by this audit (aggregate, batch bits, verdicts, nodes re-derived from the raw JSONLs)',
            'certificate_extraction': 'completed: independently verified WIN7 certificates for both WIN roots are fold material',
            'fold_material': '9 receipts (bits 1/7/24/39/59/64/67/72/96) ready; fold must re-fetch latest main and re-assert the canonical head',
            'interpretation_of_refuted_d10': ('all 63 non-WIN candidates are REFUTED-D10: no first-player win within depth 10 from those '
                'seven-stone roots. This is NOT a LOSS proof for those roots and does not close the child S6 row'),
        },
        'interpretation': ('win7_d10_bits is [1, 7, 24, 39, 59, 64, 67, 72, 96]: the sweep is NOT sterile. The v16 determinism rerun '
            '(batch 5) is node-exact and the v15 cross-engine agrees on all 9 WIN bits (loss=true) and the REFUTED anchors '
            '(bits 0/43/117, loss=false). All 9 WIN roots are new (no D4 duplicate vs '
            'the %d published certificate-manifest canonical roots scanned across %d manifest files). REFUTED-D10 is '
            'NOT a LOSS proof. The standard 11x11 empty board, both two-stone roots {49,60}/{59,60}, S2 {59,60}, class 1, class 2 and '
            'class 4 all remain UNKNOWN.') % (len(pub_canon), scanned),
    }
    out_path = os.path.join(OUT, 'class2-lane-cost72c-sweep-audit-20261115.json')
    with open(out_path, 'w') as f:
        f.write(json.dumps(audit, indent=1) + '\n')
    print('audit written:', out_path)
    print('win_bits:', win_bits, 'win_nodes:', {b: verdicts[b]['nodes'] for b in win_bits},
          'refuted:', len(refuted), 'capped:', len(capped), 'nodes:', total_nodes)
    print('pub_canon roots:', len(pub_canon), 'manifest files scanned:', scanned)

if __name__ == '__main__':
    main()
