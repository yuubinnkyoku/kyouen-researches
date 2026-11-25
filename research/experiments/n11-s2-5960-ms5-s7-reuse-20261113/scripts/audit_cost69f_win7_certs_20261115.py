#!/usr/bin/env python3
"""Independent audit of all nine published cost-69f WIN7 certificates
(2026-11-15).

Independence: fresh Python implementation written for this audit from the
published game-rule description (verify_bit7_win7_cert.ts header); no
repository verifier import, no engine, no verdict cache, no solver. The
kyouen predicate is an exact integer Bareiss 4x4 determinant of
[x^2+y^2, x, y, 1] on arbitrary-precision Python integers (no floating point
anywhere); the forbidden-by-triple masks are recomputed from scratch and
cached.

Checks per certificate (bits 2/20/44/68/69/94/109/118/119 of the cost-69f
child 00000000000000809102000000000008):
1. file level: byte size, md5, sha256 and git blob sha against the two
   records files (bits 2/94/109/119 published as 2 parts each; each part is
   checked for bytes, md5, git blob sha, line counts and line-boundary
   split, and the joined bytes must reproduce the records-pinned whole
   md5/sha256/bytes);
2. certificate structure: exact header line, root line == child | 1<<bit,
   root popcount 7, rows sorted-unique, keys 32-hex within the 121-point
   board, integer moves in [0, 121);
3. game rules: root has no 4 cocircular stones (C(7,4)=35 exact determinants
   non-zero); loser mobility re-enumerated from the triple-ban rule and
   cross-checked against the records root_check and the set of one-bit
   strategy rows;
4. full strategy verification: every legal loser first move is a sub-root;
   from each sub-root the winner follows the published strategy (every
   strategy move legal), the loser expands ALL legal replies, terminals are
   loser-stuck positions with 13..17 stones, no strategy rows exist at
   loser or terminal states;
5. exact union: the consumed winner-state sets over all sub-roots equal the
   certificate row set (missing 0 / extra 0);
6. records cross-check: winner/loser state counts, loser reply edges,
   visited states, terminal count, sub_roots_pass/total, fbt_drops 0,
   fatal null, rows_sorted_unique, and the v15 cross-engine anchor
   (loss=true, node count) from class2-lane-cost69f-v15-crosscheck-20261115.jsonl.

Results: all nine certificates PASS every check; terminal range [13, 17]
on every certificate.
"""
import hashlib, json, time
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'
CERTDIR = OUT / 'class2-lane-cost69f-certificates'
N = 121
FULL = (1 << N) - 1


def git_blob_sha(raw):
    return hashlib.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()


def det4(points):
    a = []
    for p in points:
        x, y = p % 11, p // 11
        a.append([x * x + y * y, x, y, 1])
    sign, div = 1, 1
    for k in range(3):
        if a[k][k] == 0:
            for j in range(k + 1, 4):
                if a[j][k] != 0:
                    a[k], a[j] = a[j], a[k]
                    sign = -sign
                    break
            else:
                return 0
        piv = a[k][k]
        for i in range(k + 1, 4):
            aik = a[i][k]
            for j in range(k + 1, 4):
                v = a[i][j] * piv - aik * a[k][j]
                if v % div:
                    raise AssertionError('non-integral Bareiss step')
                a[i][j] = v // div
            a[i][k] = 0
        div = piv
    return sign * a[3][3]


@lru_cache(maxsize=None)
def fbt(a, b, c):
    m = 0
    for d in range(N):
        if d != a and d != b and d != c and det4((a, b, c, d)) == 0:
            m |= 1 << d
    return m


def points_of(v):
    pts = []
    while v:
        lsb = v & -v
        pts.append(lsb.bit_length() - 1)
        v ^= lsb
    return pts


def legal_of(pts):
    banned = 0
    for p in pts:
        banned |= 1 << p
    n = len(pts)
    f = fbt
    for i in range(n):
        a = pts[i]
        for j in range(i + 1, n):
            b = pts[j]
            for k in range(j + 1, n):
                banned |= f(a, b, pts[k])
    return FULL & ~banned


def parse_cert(text, expected_root):
    lines = [l for l in text.split('\n') if l.strip()]
    assert lines[0] == 'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS', 'header'
    assert lines[1] == 'root ' + expected_root, 'root line'
    strat = {}
    prev = ''
    for ln in lines[2:]:
        k, mv = ln.split(' ')
        assert len(k) == 32, 'bad row key length'
        assert k > prev, 'unsorted or duplicate row'
        prev = k
        mv = int(mv)
        assert 0 <= mv < N, 'move out of board'
        assert int(k, 16) <= FULL, 'row bit out of board'
        strat[k] = mv
    return strat, len(lines) - 2


def verify_subroot(strat, sub):
    seen = set()
    consumed = []
    terminals = []
    winner_states = 0
    loser_states = 0
    opp = 0
    stack = [(sub, 0)]
    sg = strat.get
    while stack:
        board, depth = stack.pop()
        hexs = format(board, '032x')
        if hexs in seen:
            continue
        seen.add(hexs)
        pts = points_of(board)
        options = legal_of(pts)
        if options == 0:
            assert depth % 2 != 0, 'winner stuck at ' + hexs
            assert hexs not in strat, 'terminal has strategy move ' + hexs
            terminals.append(len(pts))
            continue
        if depth % 2 == 0:
            mv = sg(hexs)
            assert mv is not None, 'missing winner move at ' + hexs
            assert (options >> mv) & 1, 'illegal winner move at ' + hexs
            consumed.append(hexs)
            winner_states += 1
            stack.append((board | (1 << mv), depth + 1))
        else:
            assert hexs not in strat, 'strategy on loser turn ' + hexs
            loser_states += 1
            o = options
            while o:
                bit = o & -o
                o ^= bit
                opp += 1
                stack.append((board | bit, depth + 1))
    return len(seen), consumed, terminals, opp, winner_states, loser_states


def audit(cert_path, root_hex):
    t0 = time.time()
    raw = Path(cert_path).read_bytes()
    strat, nlines = parse_cert(raw.decode(), root_hex)
    root = int(root_hex, 16)
    pts = points_of(root)
    assert len(pts) == 7, 'root must have 7 stones'
    for i in range(7):
        for j in range(i + 1, 7):
            for k in range(j + 1, 7):
                for q in range(k + 1, 7):
                    assert det4((pts[i], pts[j], pts[k], pts[q])) != 0, '4 cocircular in root'
    legal_first = legal_of(pts)
    legal_bits = []
    lb = legal_first
    while lb:
        bit = lb & -lb
        lb ^= bit
        legal_bits.append(bit.bit_length() - 1)
    mob = len(legal_bits)
    onebit_keys = [int(k, 16) for k in strat]
    onebit = sorted(v ^ root for v in onebit_keys if bin(v ^ root).count('1') == 1)
    assert onebit == [1 << b for b in sorted(legal_bits)], 'sub-root rows != legal first moves'
    total_seen = 0
    all_consumed = set()
    opp_total = 0
    winner_total = 0
    loser_total = 0
    terminal_total = 0
    tmin, tmax = 999, 0
    for b in sorted(legal_bits):
        seen, consumed, terminals, opp, ws, ls = verify_subroot(strat, root | (1 << b))
        total_seen += seen
        all_consumed.update(consumed)
        opp_total += opp
        winner_total += ws
        loser_total += ls
        terminal_total += len(terminals)
        if terminals:
            tmin = min(tmin, min(terminals))
            tmax = max(tmax, max(terminals))
    union_missing = len(set(strat) - all_consumed)
    union_extra = len(all_consumed - set(strat))
    assert tmax > 0, 'no terminal reached (strategy must terminate)'
    return {'root_hex': root_hex, 'rows': len(strat), 'lines': nlines,
            'loser_mobility': mob, 'subroots_verified': mob,
            'visited_states': total_seen, 'loser_reply_edges': opp_total,
            'winner_states': winner_total, 'loser_states': loser_total,
            'terminal_count': terminal_total,
            'terminals_range': [tmin, tmax],
            'union_missing': union_missing, 'union_extra': union_extra,
            'seconds': round(time.time() - t0, 1)}


def load_cert_bytes(c):
    """Verify the published storage layout and return the whole cert bytes."""
    st = c['storage']
    if st['layout'] == 'single file':
        raw = (CERTDIR / st['path'].split('/')[-1]).read_bytes()
        assert len(raw) == c['bytes'] == st['bytes'], f"bytes mismatch bit {c['bit']}"
        assert hashlib.md5(raw).hexdigest() == c['md5'], f"md5 mismatch bit {c['bit']}"
        assert hashlib.sha256(raw).hexdigest() == c['sha256'], f"sha256 mismatch bit {c['bit']}"
        assert git_blob_sha(raw) == c['git_blob_sha'], f"git blob sha mismatch bit {c['bit']}"
        return raw, st['layout']
    assert 'part' in st['layout'] and len(st['parts']) == 2, f"layout bit {c['bit']}"
    parts = []
    for p in st['parts']:
        praw = (CERTDIR / p['path'].split('/')[-1]).read_bytes()
        assert len(praw) == p['bytes'], f"part bytes mismatch bit {c['bit']}"
        assert hashlib.md5(praw).hexdigest() == p['md5'], f"part md5 mismatch bit {c['bit']}"
        assert git_blob_sha(praw) == p['git_blob_sha'], f"part blob sha mismatch bit {c['bit']}"
        parts.append(praw)
    assert st['joined_md5_equals_whole_md5'] is True
    assert parts[0].endswith(b'\n') and not parts[0].endswith(b'\n\n'), 'split not at line boundary'
    first2 = parts[1].split(b'\n', 1)[0].decode()
    ks, _, ms = first2.partition(' ')
    assert len(ks) == 32 and int(ks, 16) <= FULL and ms.isdigit(), 'part2 must start with a strategy row'
    joined = parts[0] + parts[1]
    assert len(joined) == c['bytes'], f"joined bytes mismatch bit {c['bit']}"
    assert hashlib.md5(joined).hexdigest() == c['md5'], f"joined md5 mismatch bit {c['bit']}"
    assert hashlib.sha256(joined).hexdigest() == c['sha256'], f"joined sha256 mismatch bit {c['bit']}"
    return joined, st['layout']


def main():
    rec1 = json.loads((OUT / 'class2-lane-cost69f-win7-certificates-20261115.json').read_text())
    rec2 = json.loads((OUT / 'class2-lane-cost69f-win7-certificates-2-20261115.json').read_text())
    certs = rec1['certificates'] + rec2['certificates']
    assert [c['bit'] for c in certs] == [20, 44, 68, 69, 118, 2, 94, 109, 119]
    child = rec1['sweep_source']['s6_child_hex']
    assert rec2['sweep_source']['s6_child_hex'] == child
    assert rec2['sweep_source']['certified_bits_after'] == [2, 20, 44, 68, 69, 94, 109, 118, 119]
    assert rec2['sweep_source']['uncertified_bits_after'] == []
    v15rows = [json.loads(l) for l in
               (OUT / 'class2-lane-cost69f-v15-crosscheck-20261115.jsonl').read_text().splitlines()
               if l.strip()]
    v15 = {r['bit']: r for r in v15rows if 'bit' in r}
    pilots = [r for r in v15rows if r.get('control') == 'pilot_d6']
    assert len(pilots) == 3 and all(p['loss'] is False and p['nodes'] == 5949 for p in pilots)
    tmp = Path('/tmp/_audit69f_cert.txt')
    per = []
    for c in certs:
        bit = c['bit']
        assert c['verdict'] == 'WIN7' and c['child_hex'] == child
        assert int(c['root_hex'], 16) == int(child, 16) | (1 << bit), f'root != child|bit {bit}'
        assert c['fbt_drops'] == 0 and c.get('fatal') is None and c['rows_sorted_unique'] is True
        assert c['sub_roots_pass'] == c['sub_roots_total']
        assert c['union_missing'] == 0 and c['union_extra'] == 0
        assert c['terminal_range'] == [13, 17]
        assert c['root_check']['stones'] == 7 and c['root_check']['match'] is True
        raw, layout = load_cert_bytes(c)
        tmp.write_bytes(raw)
        r = audit(tmp, c['root_hex'])
        assert r['rows'] == c['rows'], f'rows mismatch bit {bit}'
        assert r['lines'] == c['rows'], f'line count mismatch bit {bit}'
        assert r['loser_mobility'] == c['root_check']['loser_mobility'], f'mobility mismatch bit {bit}'
        assert r['subroots_verified'] == c['sub_roots_pass'], f'sub-roots mismatch bit {bit}'
        assert r['union_missing'] == 0 and r['union_extra'] == 0, f'union mismatch bit {bit}'
        assert r['terminals_range'] == c['terminal_range'] == [13, 17], f'terminal range bit {bit}'
        assert r['terminal_count'] == c['terminal_count'], f'terminal count bit {bit}'
        assert r['winner_states'] == c['winner_states'], f'winner states bit {bit}'
        assert r['loser_states'] == c['loser_states'], f'loser states bit {bit}'
        assert r['loser_reply_edges'] == c['loser_reply_edges'], f'loser reply edges bit {bit}'
        assert r['visited_states'] == c['visited_states_across_subroots'], f'visited states bit {bit}'
        assert v15[bit]['loss'] is True and v15[bit]['nodes'] == c['v15_anchor_crosscheck']['nodes'], \
            f'v15 anchor mismatch bit {bit}'
        assert c['v15_anchor_crosscheck']['loss'] is True
        per.append({'bit': bit, 'root_hex': c['root_hex'], 'storage': layout,
                    'bytes': c['bytes'], 'rows': r['rows'],
                    'loser_mobility': r['loser_mobility'],
                    'subroots_verified': r['subroots_verified'],
                    'visited_states': r['visited_states'],
                    'winner_states': r['winner_states'],
                    'loser_states': r['loser_states'],
                    'loser_reply_edges': r['loser_reply_edges'],
                    'terminal_count': r['terminal_count'],
                    'terminals_range': r['terminals_range'],
                    'v15_anchor_nodes': v15[bit]['nodes'],
                    'union_missing': 0, 'union_extra': 0, 'seconds': r['seconds']})
        print(f"CONTROL bit {bit}: PASS rows={r['rows']} subs={r['subroots_verified']} "
              f"visited={r['visited_states']} loser_edges={r['loser_reply_edges']} "
              f"terminals={r['terminal_count']}@{r['terminals_range']} union=0/0 "
              f"v15anchor={v15[bit]['nodes']}")
    result = {
        'schema': 'n11-class2-lane-cost69f-9cert-python-independent-audit-20261115-v1',
        'date': '2026-11-15',
        'audited_scope': 'all nine WIN7 certificates of the class2-lane cost-69f sweep '
                         '(bits 2/20/44/68/69/94/109/118/119 of child '
                         '00000000000000809102000000000008, the folded chain head 1163 '
                         'receipt group)',
        'records_sources': [
            'class2-lane-cost69f-win7-certificates-20261115.json (bits 20/44/68/69/118)',
            'class2-lane-cost69f-win7-certificates-2-20261115.json (bits 2/94/109/119, 2-part storage)',
        ],
        'method': 'fresh Python implementation; no repository verifier import, no engine, '
                  'no verdict cache, no solver, no floating point; exact integer Bareiss '
                  '4x4 determinant of [x^2+y^2,x,y,1] on arbitrary-precision integers; '
                  'forbidden-by-triple masks recomputed from scratch; per certificate: '
                  'published storage verified first (single files and both parts of the '
                  'four 2-part certificates against bytes, md5, sha256 where published '
                  'and git blob sha, line-boundary split, joined md5/sha256/bytes equal '
                  'to the records whole-file hashes), then exact header/root lines, '
                  'root = child | 1<<bit with 7 stones and C(7,4)=35 non-zero '
                  'determinants (no 4 cocircular), loser mobility re-enumerated and '
                  'matched to the one-bit strategy rows, full sub-root decomposition '
                  'with every strategy move legal, all loser replies expanded, '
                  'terminals loser-stuck at 13..17 stones, no strategy rows at loser or '
                  'terminal states, the exact consumed/rows union (0 missing / 0 extra) '
                  'over all sub-roots, records cross-check of winner/loser state counts, '
                  'loser reply edges, visited states, terminal count, and the v15 '
                  'cross-engine anchor (loss=true, node count) from '
                  'class2-lane-cost69f-v15-crosscheck-20261115.jsonl',
        'totals': {
            'certificates': len(per),
            'strategy_rows': sum(p['rows'] for p in per),
            'visited_states': sum(p['visited_states'] for p in per),
            'winner_states': sum(p['winner_states'] for p in per),
            'loser_states': sum(p['loser_states'] for p in per),
            'loser_reply_edges': sum(p['loser_reply_edges'] for p in per),
            'terminal_count': sum(p['terminal_count'] for p in per),
            'subroots_verified': sum(p['subroots_verified'] for p in per),
            'all_pass': True,
            'terminal_range_all': [13, 17],
        },
        'certificates': per,
        'interpretation_guard': 'the audit reproduces the certificates game-legal '
                                'content exactly; WIN7 certificates prove a win within '
                                'the certified strategy from the individual 7-stone '
                                'roots only; they close receipt orbits in the s6 manifest '
                                'but do not by themselves close the six-stone child, '
                                'the S5 parent, the S2 {59,60} root, or the 11x11 empty '
                                'board; solved counts measure manifest bookkeeping, not '
                                'game-theoretic values; 11x11 empty root / {49,60} / '
                                'S2 {59,60} / class 2 / class 4 remain UNKNOWN',
    }
    (OUT / 'class2-lane-cost69f-9cert-python-independent-audit-20261115.json').write_text(
        json.dumps(result, indent=1) + '\n')
    print('written class2-lane-cost69f-9cert-python-independent-audit-20261115.json')


if __name__ == '__main__':
    main()
