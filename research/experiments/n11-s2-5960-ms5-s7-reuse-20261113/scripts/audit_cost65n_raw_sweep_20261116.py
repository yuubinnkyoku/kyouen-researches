#!/usr/bin/env python3
# Independent raw-sweep audit for the class2-lane cost-65n child sweep (the
# cost-65n child 00000000000000801202010000800000 at the post-cost-64g
# canonical head 1441; the cheapest open row of the shared class-2 protocol
# parent, 59 open bits after 6 published-verbatim REFUTED-D10 transfers).
# Python standard library only; exact integer Bareiss determinants; no
# floating point, no repository solver/engine code.
# Re-derives the sweep aggregate from the raw artifacts (8 v16 raw batches +
# v16 determinism reruns batch5/batch7 + v15 crosscheck JSONLs), re-enumerates
# the legal candidates from scratch, re-derives all six one-stone deletion
# lift parents by exact D4 canonicalization, verifies the shared parent
# against the published head-1441 pre-sweep census family data (the second
# direct parent 00000000000000801202010000000000 is outside the two census
# protocol parents and is pinned to the published certificates manifest),
# cross-checks the completed claim v2 (NOT-STERILE: 2 WIN7-D10 bits 90/117 +
# 63 REFUTED-D10), verifies the 6 pre-sweep transfers against the published
# census bit table root canons, and confirms both WIN root D4 canons are
# distinct from every other candidate canon (no intra-sweep orbit collision).
import json, sys, os, hashlib

OUT = os.path.join(os.path.dirname(__file__), '..', 'output')
CLAIM = os.path.join(OUT, 'class2-lane-cost65n-inflight-20261116.json')
CENSUS = os.path.join(OUT, 'class2-lane-next-target-presweep-1441-20261116.json')
CERTS = os.path.join(OUT, 'class2-lane-cost65n-win2-certificates-20261116.json')
CHILD = '00000000000000801202010000800000'
PARENT_SHARED = '00000000000000003800000008002000'   # class-2 shared protocol parent (29 rows / 2017)
PARENT_SECOND = '00000000000000801202010000000000'   # second class-2 direct parent (48 rows / 3498)
BATCH_BITS = {
    1: [1, 3, 6, 8, 9, 10, 11, 12],
    2: [14, 17, 18, 19, 20, 21, 22, 26],
    3: [29, 31, 32, 42, 43, 44, 53, 54],
    4: [56, 58, 61, 66, 67, 74, 75, 77],
    5: [79, 83, 85, 86, 87, 88, 90, 94],
    6: [97, 98, 99, 102, 103, 105, 106, 107],
    7: [108, 110, 111, 112, 113, 114, 116, 117],
    8: [118, 119, 120],
}
TRANSFERRED_BITS = [35, 50, 51, 55, 64, 109]
TOTAL_NODES = 92530349
TOTAL_MS = 187251
WIN_BITS = [90, 117]


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
    res = claim['results']
    assert claim['schema'] == 'n11-class2-lane-cost65n-completed-20261116-v2'
    assert claim['s6_child'] == CHILD
    assert claim['s6_s7_edge_cost'] == 65
    assert claim['demand'] == {'c1': 0, 'c2': 2, 'c4': 0}
    assert claim['child_stones_bit_indices'] == [23, 40, 49, 57, 60, 71]
    st, legal = enumerate_legal(CHILD)
    assert st == [23, 40, 49, 57, 60, 71], 'unexpected child stones'
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
    assert len(legal) == 65

    # census cross-check: bit table and family data of the published
    # head-1441 pre-sweep census v4
    census = json.load(open(CENSUS))
    assert census['schema'] == 'n11-class2-lane-next-target-presweep-1441-20261116-v1'
    bt = census['cheapest_row_bit_tables'][CHILD]
    census_open = sorted(e['bit'] for e in bt if e['status'] == 'open')
    census_tr = {e['bit']: e['root_canon'] for e in bt
                 if e['status'] == 'harvested_refuted'}
    assert sorted(census_tr) == TRANSFERRED_BITS
    assert census_open == sorted(res['refuted_d10_bits_swept_v16'] + WIN_BITS), \
        'census open bits != swept set (swept refuted + WIN)'
    fam = census['family_census'][PARENT_SHARED]
    assert fam['row_count'] == 29 and fam['occurrences'] == 2017

    batches = []
    verdicts = {}
    total_nodes = 0
    total_ms = 0
    pilots = 0
    for n in sorted(BATCH_BITS):
        p = os.path.join(OUT, 'class2-lane-cost65n-raw-batch%d-20261116.jsonl' % n)
        rows = load_jsonl(p)
        ctrl = [r for r in rows if 'control' in r]
        cand = [r for r in rows if 'bit' in r]
        assert len(ctrl) == 1 and ctrl[0]['nodes'] == 3402 and ctrl[0]['loss'] is False
        pilots += 1
        bits = [r['bit'] for r in cand]
        assert bits == BATCH_BITS[n], 'batch %d bit list mismatch: %r' % (n, bits)
        assert bits == res['batch_bit_lists'][str(n)], 'batch %d != claim list' % n
        for r in cand:
            assert r['bit'] not in verdicts, 'duplicate bit'
            assert r['bit'] in legal, 'bit not in enumeration'
            verdicts[r['bit']] = r
            total_nodes += r['nodes']
            total_ms += r['ms']
            tsr = r['terminalStoneRange']
            assert tsr[0] >= 7 and tsr[1] <= 17, 'terminal stone range outside depth-10 bounds'
            assert r['andclose'] is True
        batches.append({'batch': n, 'file': os.path.basename(p),
                        'candidate_bits': bits, 'pilot_nodes': 3402,
                        'nodes': sum(r['nodes'] for r in cand)})
    assert set(verdicts.keys()) == set(census_open), 'swept set != census open set'
    win_bits = sorted(b for b, r in verdicts.items() if r['loss'])
    capped = sorted(b for b, r in verdicts.items() if r['capped'])
    refuted = sorted(b for b, r in verdicts.items() if (not r['loss']) and (not r['capped']))
    assert len(win_bits) + len(refuted) + len(capped) == 59
    assert not capped, 'capped candidates would invalidate the sweep'
    assert win_bits == WIN_BITS == res['win7_d10_bits'], 'unexpected WIN set'
    assert refuted == res['refuted_d10_bits_swept_v16']
    assert total_nodes == TOTAL_NODES == res['candidate_nodes_excluding_pilots']
    assert total_ms == TOTAL_MS == res['candidate_ms_total']
    assert res['refuted_d10_count'] == len(refuted) + len(TRANSFERRED_BITS) == 63
    heaviest = sorted(verdicts.items(), key=lambda kv: -kv[1]['nodes'])[:3]
    heaviest = {str(b): r['nodes'] for b, r in heaviest}
    assert heaviest == res['heaviest_bits_nodes'], 'heaviest bits mismatch vs claim'

    # determinism reruns: batch5 (WIN bit 90) and batch7 (WIN bit 117)
    for n, blob_note in ((5, 'batch5'), (7, 'batch7')):
        det = load_jsonl(os.path.join(OUT,
                      'class2-lane-cost65n-v16-determinism-rerun-%s-20261116.jsonl' % blob_note))
        det_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'],
                               tuple(r['terminalStoneRange']))
                    for r in det if 'bit' in r}
        raw_bits = {r['bit']: (r['loss'], r['nodes'], r['capped'],
                               tuple(r['terminalStoneRange']))
                    for r in load_jsonl(os.path.join(
                        OUT, 'class2-lane-cost65n-raw-batch%d-20261116.jsonl' % n))
                    if 'bit' in r}
        assert det_bits == raw_bits, 'determinism rerun mismatch (%s)' % blob_note
        det_pilot = [r for r in det if 'control' in r][0]
        assert det_pilot['nodes'] == 3402 and det_pilot['loss'] is False

    # v15 cross-engine agreement (anchors 9/90/94/117 incl. both WIN bits)
    v15 = load_jsonl(os.path.join(OUT, 'class2-lane-cost65n-v15-crosscheck-20261116.jsonl'))
    v15_pilots = [r for r in v15 if 'control' in r]
    assert len(v15_pilots) == 1
    assert v15_pilots[0]['nodes'] == 5949 and v15_pilots[0]['loss'] is False
    v15_bits = {r['bit']: r for r in v15 if 'bit' in r}
    assert sorted(v15_bits) == [9, 90, 94, 117], 'unexpected anchor selection'
    for b in (9, 90, 94, 117):
        assert v15_bits[b]['loss'] == verdicts[b]['loss'], \
            'v15/v16 verdict disagreement on bit %d' % b
        assert v15_bits[b]['capped'] is False
        assert b in legal
    assert v15_bits[90]['loss'] is True and v15_bits[90]['nodes'] == 3204116
    assert v15_bits[117]['loss'] is True and v15_bits[117]['nodes'] == 865824

    # transfers: census root canon == d4_canon(child | 1<<bit)
    child_v = int(CHILD, 16)
    transfers = {}
    for b in TRANSFERRED_BITS:
        root_hex = '%032x' % (child_v | (1 << b))
        assert d4_canon(root_hex) == census_tr[b], \
            'transferred root canon mismatch on bit %d' % b
        assert not (b in verdicts), 'transferred bit was re-swept'
        transfers[str(b)] = {'root': root_hex, 'd4_canon': census_tr[b]}
    assert set(TRANSFERRED_BITS).isdisjoint(win_bits)
    assert set(TRANSFERRED_BITS).isdisjoint(refuted)

    # D4 orbit collision scan: all 65 candidate roots must be distinct
    # canons (swept 59 + transferred 6), and both WIN canons distinct
    canons = {}
    for b in legal:
        root_hex = '%032x' % (child_v | (1 << b))
        c = d4_canon(root_hex)
        assert c not in canons, 'intra-sweep D4 orbit collision at bit %d' % b
        canons[c] = b
    win_canons = {}
    for b in WIN_BITS:
        win_canon = d4_canon('%032x' % (child_v | (1 << b)))
        assert win_canon in canons and canons[win_canon] == b
        win_canons[str(b)] = win_canon

    # certificates manifest cross-check (published blob e2e4e3f5...)
    certs = json.load(open(CERTS))
    assert certs['schema'] == 'n11-class2-lane-cost65n-win2-certificates-20261116-v1'
    cert_bits = sorted(c['bit'] for c in certs['certificates'])
    assert cert_bits == WIN_BITS
    for c in certs['certificates']:
        expect_root = '%032x' % (child_v | (1 << c['bit']))
        assert c['root_hex'] == expect_root
        assert c['verdict'] == 'WIN7'
        assert c['root_mobility_matches_legal_candidates_py'] is True
        assert c['bigint_verify']['union_missing'] == 0
        assert c['bigint_verify']['union_extra'] == 0
        assert c['bareiss_verify']['all_subroots_pass'] is True
        assert c['fbt_drops'] == 0 and c['fatal'] is None

    # lift parents: all six one-stone deletions of the child, D4-canonical
    lifts = []
    for i in range(6):
        v = 0
        for j, c in enumerate(st):
            if j != i:
                v |= 1 << c
        lifts.append(d4_canon('%032x' % v))
    assert d4_canon(PARENT_SHARED) in lifts, 'shared parent is not a lift'
    assert d4_canon(PARENT_SECOND) in lifts, 'second parent is not a lift'
    assert len(set(lifts)) == 6

    audit = {
        'schema': 'n11-class2-lane-cost65n-raw-sweep-audit-20261116-v1',
        'date': '2026-11-16',
        'child': CHILD,
        'child_stones': st,
        'claim_schema_crosscheck': claim['schema'],
        'independent_enumeration': {
            'method': 'exact integer Bareiss 4x4 from scratch (stdlib only)',
            'legal_candidates': legal,
            'matches_claim': True,
        },
        'sweep_aggregate': {
            'batches': batches,
            'pilots_3402': pilots,
            'swept_candidates': 59,
            'win7_d10_bits': win_bits,
            'win7_d10_count': len(win_bits),
            'refuted_d10_swept': len(refuted),
            'refuted_d10_transferred': len(TRANSFERRED_BITS),
            'capped': 0,
            'total_candidate_nodes': total_nodes,
            'total_candidate_ms': total_ms,
            'heaviest_bits_nodes': heaviest,
        },
        'determinism_reruns': 'batch5 (WIN bit 90) and batch7 (WIN bit 117) node-exact vs raw, ms-only diff',
        'v15_crosscheck': {
            'pilot_nodes': 5949,
            'anchors': sorted(v15_bits),
            'two_directional_agreement': True,
            'win_bit_90_v15_nodes': 3204116,
            'win_bit_117_v15_nodes': 865824,
        },
        'transfers': transfers,
        'd4_orbit_collision_scan': {
            'candidate_canons_distinct': 65,
            'win_canons': win_canons,
            'intra_sweep_collisions': 0,
        },
        'certificates_manifest_crosscheck': {
            'manifest_schema': certs['schema'],
            'win_bits': cert_bits,
            'bigint_and_bareiss_all_pass': True,
            'root_hexes_match_child_or_bit': True,
        },
        'lift_parents': {
            'all_six_one_stone_deletion_canons': lifts,
            'shared_parent': {'hex': PARENT_SHARED, 'd4_canon': d4_canon(PARENT_SHARED),
                              'rows_at_head_1441': 29, 'edge_cost_at_head_1441': 2017,
                              'matches_census_family': True},
            'second_parent': {'hex': PARENT_SECOND, 'd4_canon': d4_canon(PARENT_SECOND),
                              'rows_at_head_1441': 48, 'edge_cost_at_head_1441': 3498,
                              'pinned_to': 'published certificates manifest direct_s5_parents (class2-lane-cost65n-win2-certificates-20261116.json, git blob e2e4e3f5d352e162f2d6e898b285462ff5b4d286)'},
            'note': ('both open class-2 parents of the row are one-stone '
                     'deletion lifts of the child; the shared parent is '
                     'cross-checked against the head-1441 census family '
                     '(29 rows / 2017 occurrences); the second parent is '
                     'outside the two census protocol parents and is pinned '
                     'to the certificates manifest; the remaining four lifts '
                     'are closed rows at head 1441 (verified by the fold '
                     'session when the receipts are folded)'),
        },
        'census_crosscheck': {
            'census_schema': census['schema'],
            'census_bit_table_open_59': True,
            'census_transferred_6': True,
            'family_shared_29_2017': True,
        },
        'interpretation_guard': ('REFUTED-D10 is not a LOSS proof; WIN7-D10 '
                                 'proves a first-player win within depth 10 '
                                 'from the single 7-stone root only; the row '
                                 'is NOT sterile; head 1441 unchanged until '
                                 'the fold; 11x11 empty board and classes '
                                 '1/2/4 remain UNKNOWN'),
    }
    op = os.path.join(OUT, 'class2-lane-cost65n-sweep-audit-20261116.json')
    with open(op, 'w') as f:
        json.dump(audit, f, indent=1)
        f.write('\n')
    d = open(op, 'rb').read()
    print('WROTE', op, len(d), 'bytes git blob',
          hashlib.sha1(b'blob %d\0' % len(d) + d).hexdigest())
    print('aggregate: win %s / refuted swept %d / transferred %d / capped 0 / nodes %d / ms %d'
          % (win_bits, len(refuted), len(TRANSFERRED_BITS), total_nodes, total_ms))
    print('ALL AUDIT CHECKS PASS')


if __name__ == '__main__':
    main()
