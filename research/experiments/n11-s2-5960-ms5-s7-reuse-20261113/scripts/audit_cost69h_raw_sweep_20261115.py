#!/usr/bin/env python3
# Independent raw-sweep audit for the class2-lane cost-69h child sweep (2026-11-15).
# Python standard library only; exact integer Bareiss determinants; no floating point,
# no repository solver/engine code. Re-derives the sweep aggregate from the eleven raw
# artifacts (9 v16 raw batches + v16 determinism rerun + v15 crosscheck JSONLs),
# re-enumerates the legal candidates from scratch, and cross-checks the claim.
# WIN7-D10 roots are identity-checked (root == child | 1<<bit), D4-canonicalized and
# mobility-checked by the same independent Bareiss enumeration.
import json, sys, os, glob, hashlib, re

OUT = os.path.join(os.path.dirname(__file__), '..', 'output')
CLAIM = os.path.join(OUT, 'class2-lane-cost69h-inflight-20261115.json')
CHILD = '0000000000000080120a000000200000'
N_BATCHES = 9

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
    assert claim['s6_s7_edge_cost'] == 69
    assert claim['demand'] == {'c1': 0, 'c2': 2, 'c4': 0}
    st, legal = enumerate_legal(CHILD)
    assert len(st) == 6, 'child must have 6 stones'
    # child safety
    child_safe = True
    for i in range(6):
        for j in range(i + 1, 6):
            for k in range(j + 1, 6):
                for l in range(k + 1, 6):
                    if det4([st[i], st[j], st[k], st[l]]) == 0:
                        child_safe = False
    assert child_safe, 'child must be safe'
    assert legal == claim['legal_candidates'], 'independent enumeration != claim list'
    assert len(legal) == 69

    batches = []
    verdicts = {}
    total_nodes = 0
    pilots = 0
    for n in range(1, N_BATCHES + 1):
        p = os.path.join(OUT, 'class2-lane-cost69h-raw-batch%d-20261115.jsonl' % n)
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
    assert len(win_bits) + len(refuted) + len(capped) == 69
    assert not capped, 'capped candidates present'
    assert win_bits == [58, 96], win_bits

    # determinism rerun: batch 5 bits must agree (ignoring ms)
    det = load_jsonl(os.path.join(OUT, 'class2-lane-cost69h-v16-determinism-rerun-20261115.jsonl'))
    det_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'], tuple(r['terminalStoneRange'])) for r in det if 'bit' in r}
    b5_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'], tuple(r['terminalStoneRange']))
               for r in load_jsonl(os.path.join(OUT, 'class2-lane-cost69h-raw-batch5-20261115.jsonl')) if 'bit' in r}
    assert det_bits == b5_bits, 'determinism rerun mismatch'
    det_pilot = [r for r in det if 'control' in r][0]
    assert det_pilot['nodes'] == 3402 and det_pilot['loss'] is False

    # v15 cross-engine agreement
    v15 = load_jsonl(os.path.join(OUT, 'class2-lane-cost69h-v15-crosscheck-20261115.jsonl'))
    v15_pilots = [r for r in v15 if 'control' in r]
    assert all(r['nodes'] == 5949 and r['loss'] is False for r in v15_pilots)
    v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
    for b in win_bits:
        assert b in v15_bits and v15_bits[b]['loss'] is True, 'v15 disagrees on WIN bit'
    for b in v15_bits:
        if b not in win_bits:
            assert v15_bits[b]['loss'] is False, 'v15 found extra WIN'
            assert verdicts[b]['loss'] is False, 'raw verdict disagreement'

    # root identity + D4 canonical + independent Bareiss mobility
    child_v = int(CHILD, 16)
    roots = {}
    for b in win_bits:
        rh = format(child_v | (1 << b), '032x')
        rst, rmob = enumerate_legal(rh)
        assert len(rst) == 7
        roots[b] = {'root_hex': rh, 'd4_canonical_hex': d4_canon(rh), 'root_mobility': len(rmob)}
    assert roots[58]['d4_canonical_hex'] == '0000000000000080160a000000200000'
    assert roots[96]['d4_canonical_hex'] == '00000000040000809002800000000800'
    assert roots[58]['root_mobility'] == 60 and roots[96]['root_mobility'] == 53
    canon_list = [roots[b]['d4_canonical_hex'] for b in win_bits]
    assert len(set(canon_list)) == len(canon_list), 'WIN roots share a D4 orbit'
    pub_canon = set()
    manifests = sorted(glob.glob(os.path.join(OUT, '*win7-certificates*.json')))
    scanned = 0
    for f in manifests:
        if 'cost65k' in f or 'cost73f' in f or 'cost69h' in f:
            continue
        try:
            d = json.load(open(f))
        except Exception:
            continue
        scanned += 1
        s = json.dumps(d)
        for m in re.findall(r'"(?:root_hex|d4_canonical_hex)"\s*:\s*"([0-9a-f]{32})"', s):
            pub_canon.add(d4_canon(m))
    dups_vs_pub = [c for c in canon_list if c in pub_canon]
    assert not dups_vs_pub, 'D4 duplicate vs published manifests: %r' % dups_vs_pub

    # independent one-stone-deletion demand re-derivation
    lifted = {}
    for s in st:
        rest = sorted(x for x in st if x != s)
        v = 0
        for i in rest: v |= 1 << i
        lifted[s] = d4_canon(format(v, '032x'))
    assert lifted == {
        21: '0000000000000080120a000000000000',
        49: '00000000000000801208000000200000',
        51: '00000000000000801202000000200000',
        57: '00000000000000003800002000000002',
        60: '0000000000000080020a000000200000',
        71: '0000000000000000120a000000200000',
    }, 'one-stone deletion D4 canonicalization mismatch: %r' % lifted
    op = {p['s5_hex']: p for p in claim['open_parents_at_head_1219']}
    assert op['00000000000000801202000000200000']['lift_stone'] == 51
    assert op['0000000000000080120a000000000000']['lift_stone'] == 21
    for closed_stone in (49, 57, 60, 71):
        assert lifted[closed_stone] not in op, 'closed lift unexpectedly open'

    audit = {
        'schema': 'n11-class2-lane-cost69h-raw-sweep-audit-20261115-v1',
        'date': '2026-11-15',
        'independent_method': 'Python standard library; exact Bareiss integer determinants; D4 canonicalization implemented independently; no repository engine/solver/cache, no floating point',
        'target': {
            's5_hex': claim['s5'],
            's6_child_hex': CHILD,
            'edge_cost': 69,
            'legal_candidate_count': 69,
        },
        'source_claim': {
            'path': 'research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69h-inflight-20261115.json',
            'chain_head_at_claim': claim['chain_head_at_claim'],
        },
        'geometry': {
            'child_stones': 6,
            'child_safe': True,
            'independent_legal_candidate_count': 69,
            'candidate_bits_exact_match': True,
            'lift_note': 'one-stone deletions re-derived independently: stone 51 deletion reproduces the second coverable class-2 target S5 00000000000000801202000000200000 bit-exact (32 rows / 2403 at head 1219); stone 21 deletion reproduces the open class-2 S5 0000000000000080120a000000000000 bit-exact (49 rows / 3593); the remaining four deletions (stones 49/57/60/71) canonicalize to S5 hexes absent from the open-parent set of this child at head 1219 (closed rows); demand c1=0,c2=2,c4=0 confirmed',
        },
        'batches': batches,
        'aggregate': {
            'candidates': 69,
            'win7_d10_bits': win_bits,
            'win7_d10_nodes': {str(b): verdicts[b]['nodes'] for b in win_bits},
            'refuted_d10': len(refuted),
            'refuted_d10_bits': refuted,
            'capped': len(capped),
            'capped_bits': capped,
            'candidate_nodes': total_nodes,
            'pilots': pilots,
        },
        'crosschecks': {
            'v16_determinism_rerun': {
                'file': 'class2-lane-cost69h-v16-determinism-rerun-20261115.jsonl',
                'batch_rerun': 5,
                'identical_ignoring_ms': True,
            },
            'v15_cross_engine': {
                'file': 'class2-lane-cost69h-v15-crosscheck-20261115.jsonl',
                'win_bits_agree': True,
                'win_anchor_nodes': {str(b): v15_bits[b]['nodes'] for b in win_bits},
                'refuted_anchors': sorted(b for b in v15_bits if b not in win_bits),
                'anchor_nodes': {str(b): v15_bits[b]['nodes'] for b in sorted(v15_bits) if b not in win_bits},
                'pilots_5949': len(v15_pilots),
            },
        },
        'win7_roots': {str(b): roots[b] for b in win_bits},
        'd4_duplicate_scan': {
            'roots_compared': len(pub_canon),
            'manifest_files_scanned': scanned,
            'duplicates': 0,
        },
        'checks': {
            'all_bits_exactly_once': True,
            'all_terminal_ranges_within_depth10_bounds': True,
            'distinct_terminal_ranges': sorted({tuple(r['terminalStoneRange']) for r in verdicts.values()}),
            'pilot_3402_per_batch': True,
            'independent_enumeration_matches_claim': True,
            'one_stone_deletion_d4_canonicalization_verified': True,
            'root_identity_child_or_bit': True,
        },
        'proof_boundary': {
            'raw_sweep_rederivation': 'closed by this audit',
            'certificate_extraction': 'completed this session: blind kill-table extraction of both WIN7 roots (bits 58/96) with fbt_drops=0, BigInt independent verification PASS; manifest published immediately after this audit',
            'fold_material': 'pending: the fold of the 2 WIN7-D10 receipts onto the canonical chain head 1219/6628/523173/4898/386896 is executed by recompute_frontier_cost69h_receipts_20261115.py (published after the certificates)',
            'interpretation_of_refuted_d10': 'all 67 REFUTED candidates have no first-player win within depth 10 from their 7-stone roots. This is NOT a LOSS proof for those roots and does not close the child S6 row by itself',
        },
        'interpretation': 'win7_d10_bits = [58, 96]: the child 0000000000000080120a000000200000 has two first-player wins within depth 10 (root = child | 1<<bit), each certified by an n11-terminal-strategy-v1 certificate (second-to-move LOSS) independently verified by the BigInt exact-geometry verifier. refuted_d10 is NOT a LOSS proof. The sweep alone changes no frontier count; the fold removes the child row from both open class-2 parents (the second coverable class-2 target 00000000000000801202000000200000 32 rows / 2403 and the open class-2 S5 0000000000000080120a000000000000 49 rows / 3593, both at head 1219). The standard 11x11 empty board, both two-stone roots {49,60}/{59,60}, S2 {59,60}, class 2 and class 4 all remain UNKNOWN.',
    }
    out_path = os.path.join(OUT, 'class2-lane-cost69h-sweep-audit-20261115.json')
    with open(out_path, 'w') as f:
        f.write(json.dumps(audit, indent=1) + '\n')
    print('audit written:', out_path)
    print('win_bits:', win_bits, 'refuted:', len(refuted), 'capped:', len(capped), 'nodes:', total_nodes)

if __name__ == '__main__':
    main()
