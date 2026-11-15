#!/usr/bin/env python3
# Independent raw-sweep audit for the class2-lane cost-74h child sweep (the cheapest
# unswept child of the second coverable class-2 target S5 at the merged canonical
# head 1270, 2026-11-15).
# Python standard library only; exact integer Bareiss determinants; no floating point,
# no repository solver/engine code. Re-derives the sweep aggregate from the twelve raw
# artifacts (10 v16 raw batches + v16 determinism rerun + v15 crosscheck JSONLs),
# re-enumerates the legal candidates from scratch, re-derives all six one-stone
# deletion lift parents by exact D4 canonicalization, and cross-checks the claim.
import json, sys, os, glob, re

OUT = os.path.join(os.path.dirname(__file__), '..', 'output')
CLAIM = os.path.join(OUT, 'class2-lane-cost74h-inflight-20261115.json')
CHILD = '00000000000000889002000000000800'
PARENT1 = '00000000000000801222000000000000'  # class-2 lift parent (75 rows / 5705)
PARENT2 = '00000000000000801202000000200000'  # second coverable class-2 target S5 (17 rows / 1325)

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
    assert claim['s6_s7_edge_cost'] == 74
    assert claim['s5_parent1'] == PARENT1 and claim['s5_parent2'] == PARENT2
    st, legal = enumerate_legal(CHILD)
    assert st == [11, 49, 60, 63, 67, 71], 'unexpected child stones'
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
    assert len(legal) == 74

    batches = []
    verdicts = {}
    total_nodes = 0
    pilots = 0
    for n in range(1, 11):
        p = os.path.join(OUT, 'class2-lane-cost74h-raw-batch%d-20261115.jsonl' % n)
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
    assert len(win_bits) + len(refuted) + len(capped) == 74
    assert not capped, 'capped candidates would invalidate the sterile verdict'
    assert not win_bits, 'expected a sterile sweep for cost-74h'
    assert total_nodes == 72720136, 'unexpected total candidate nodes'
    heaviest = sorted(verdicts.items(), key=lambda kv: -kv[1]['nodes'])[:6]
    heaviest = {str(b): r['nodes'] for b, r in heaviest}

    # determinism rerun: batch 5 bits must agree (ignoring ms)
    det = load_jsonl(os.path.join(OUT, 'class2-lane-cost74h-v16-determinism-rerun-20261115.jsonl'))
    det_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'], tuple(r['terminalStoneRange'])) for r in det if 'bit' in r}
    b5_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'], tuple(r['terminalStoneRange']))
               for r in load_jsonl(os.path.join(OUT, 'class2-lane-cost74h-raw-batch5-20261115.jsonl')) if 'bit' in r}
    assert det_bits == b5_bits, 'determinism rerun mismatch'
    det_pilot = [r for r in det if 'control' in r][0]
    assert det_pilot['nodes'] == 3402 and det_pilot['loss'] is False

    # v15 cross-engine agreement (all crosschecked bits are REFUTED anchors; the
    # crosscheck was run as three foreground invocations after a sandbox environment
    # reset killed the first background attempt, so it carries three d6 pilots)
    v15 = load_jsonl(os.path.join(OUT, 'class2-lane-cost74h-v15-crosscheck-20261115.jsonl'))
    v15_pilots = [r for r in v15 if 'control' in r]
    assert len(v15_pilots) == 3
    assert all(r['nodes'] == 5949 and r['loss'] is False for r in v15_pilots)
    v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
    assert v15_bits, 'v15 crosscheck must contain candidate rows'
    for b in win_bits:
        assert b in v15_bits and v15_bits[b]['loss'] is True, 'v15 disagrees on WIN bit'
    for b in v15_bits:
        if b not in win_bits:
            assert v15_bits[b]['loss'] is False, 'v15 found extra WIN'
            assert verdicts[b]['loss'] is False, 'raw verdict disagreement'
    anchors = sorted(b for b in v15_bits if b not in win_bits)
    assert anchors == [0, 2, 62, 86, 87], 'unexpected anchor selection'
    # every v15 anchor must be a legal candidate of this child (bit 1 is NOT legal
    # for the 74h child and was excluded from the crosscheck on purpose)
    for b in anchors:
        assert b in legal, 'v15 anchor not a legal candidate: %r' % b

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
    pub_canon = set()
    manifests = sorted(glob.glob(os.path.join(OUT, '*win7-certificates*.json')))
    for f in manifests:
        if 'cost65k' in f or 'cost73f' in f:
            continue
        try:
            d = json.load(open(f))
        except Exception:
            continue
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
        11: '00000000000000801222000000000000',
        49: '00000000000000889000000000000800',
        60: '00000000000000888002000000000800',
        63: '00000000000000003800000000008200',
        67: '00000000000000801202000000200000',
        71: '00000000000000089002000000000800',
    }, 'one-stone deletion D4 canonicalization mismatch: %r' % lifted
    assert len(set(lifted.values())) == 6, 'deletion orbits must be distinct'
    assert lifted[11] == PARENT1, 'lift-stone-11 deletion must reproduce the class-2 lift parent'
    assert lifted[67] == PARENT2, 'lift-stone-67 deletion must reproduce the second coverable class-2 target S5'

    audit = {
        'schema': 'n11-class2-lane-cost74h-raw-sweep-audit-20261115-v1',
        'date': '2026-11-15',
        'independent_method': 'Python standard library; exact Bareiss integer determinants; D4 canonicalization implemented independently; no repository engine/solver/cache, no floating point',
        'target': {
            's5_parent1_hex': PARENT1,
            's5_parent2_hex': PARENT2,
            's6_child_hex': CHILD,
            'edge_cost': 74,
            'legal_candidate_count': 74,
        },
        'source_claim': {
            'path': 'research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74h-inflight-20261115.json',
            'chain_head_at_claim': claim['chain_head_at_claim'],
        },
        'geometry': {
            'child_stones': 6,
            'child_safe': True,
            'independent_legal_candidate_count': 74,
            'candidate_bits_exact_match': True,
            'lift_note': 'one-stone deletions re-derived independently: stone 11 deletion reproduces the class-2 lift parent 00000000000000801222000000000000 bit-exact (75 rows / 5705, classes_bitmask 2 at the merged head 1270); stone 67 deletion reproduces the second coverable class-2 target S5 00000000000000801202000000200000 bit-exact (17 rows / 1325, classes_bitmask 2); the other four deletions (stones 49, 60, 63, 71) canonicalize to 00000000000000889000000000000800, 00000000000000888002000000000800, 00000000000000003800000000008200, 00000000000000089002000000000800: six distinct orbits, the remaining four closed and absent from the merged-head ranking; per-mask-bit demand is therefore c1=0, c2=2, c4=0, matching the claim and the merged-head top-candidates CSV row s5=00000000000000801202000000200000,s6=00000000000000889002000000000800,cost=74',
        },
        'batches': batches,
        'aggregate': {
            'candidates': 74,
            'win7_d10_bits': win_bits,
            'win7_d10_nodes': {str(b): verdicts[b]['nodes'] for b in win_bits},
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
                'file': 'class2-lane-cost74h-v16-determinism-rerun-20261115.jsonl',
                'batch_rerun': 5,
                'identical_ignoring_ms': True,
                'post_reset_note': 'the sandbox environment reset mid-session and wiped the local mirror; all 10 raw batches and the determinism rerun were regenerated from scratch with the same v16 engine and reproduced the pre-reset aggregate node-exactly (74 candidates, 0 WIN7, 74 REFUTED, 0 capped, 72,720,136 nodes, 10 pilots at 3402), which doubles as an environment-reset determinism check',
            },
            'v15_cross_engine': {
                'file': 'class2-lane-cost74h-v15-crosscheck-20261115.jsonl',
                'win_bits_agree': True,
                'refuted_anchors': anchors,
                'anchor_nodes': {str(b): v15_bits[b]['nodes'] for b in anchors},
                'pilots_5949': len(v15_pilots),
                'run_note': 'three foreground invocations (bits 0/2, bits 62/86, bit 87), each with its own d6 pilot at 5949 nodes; the first background attempt was killed by the sandbox environment reset and is not part of this file; bit 1 is not a legal candidate of this child (Bareiss-unsafe, absent from the 74-candidate enumeration) and was excluded from the anchors',
            },
        },
        'd4_duplicate_scan': {
            'roots_compared': len(pub_canon),
            'manifest_files_scanned': len(manifests) - sum(1 for f in manifests if 'cost65k' in os.path.basename(f) or 'cost73f' in os.path.basename(f)),
            'duplicates': 0,
        },
        'checks': {
            'all_bits_exactly_once': True,
            'all_terminal_ranges_within_depth10_bounds': True,
            'distinct_terminal_ranges': sorted({tuple(r['terminalStoneRange']) for r in verdicts.values()}),
            'pilot_3402_per_batch': True,
            'independent_enumeration_matches_claim': True,
            'one_stone_deletion_d4_canonicalization_verified': True,
            'total_nodes_match': total_nodes == 72720136,
        },
        'proof_boundary': {
            'raw_sweep_rederivation': 'closed by this audit',
            'certificate_extraction': 'not required: the sweep is sterile (no WIN7-D10 bits)',
            'fold_material': 'none: no receipts, the canonical chain frontier is unchanged by this sweep',
            'interpretation_of_refuted_d10': 'all 74 candidates are REFUTED-D10: no first-player win within depth 10 from any of the 74 seven-stone roots. This is NOT a LOSS proof for those roots and does not close the child S6 row; closing this child row requires evidence beyond depth 10 (each candidate would need a refutation at depth > 10 or an equivalent invariant)',
        },
        'interpretation': 'win7_d10_bits is empty: the sweep is sterile. refuted_d10 is NOT a LOSS proof. capped proves nothing (and there were no capped candidates). The sweep alone closes no S6 orbit and changes no frontier count; the child 00000000000000889002000000000800 remains an open S6 row (a remaining row of both open parents: the class-2 lift parent 00000000000000801222000000000000 stays at 75 rows / 5705 and the second coverable class-2 target S5 00000000000000801202000000200000 stays at 17 rows / 1325 in the claim-baseline merged head 1270). Note: while this sweep was in flight a parallel lane landed the cost-69i fold on a 1266-based chain (head 1273), forking the canonical chain against the merged head 1270; that fork is a receipt-bookkeeping fork only and is unaffected by this sterile sweep, whose claim baseline remains the merged head 1270. The standard 11x11 empty board, both two-stone roots {49,60}/{59,60}, S2 {59,60}, class 2 and class 4 all remain UNKNOWN.',
    }
    out_path = os.path.join(OUT, 'class2-lane-cost74h-sweep-audit-20261115.json')
    with open(out_path, 'w') as f:
        f.write(json.dumps(audit, indent=1) + '\n')
    print('audit written:', out_path)
    print('win_bits:', win_bits, 'refuted:', len(refuted), 'capped:', len(capped), 'nodes:', total_nodes)

if __name__ == '__main__':
    main()
