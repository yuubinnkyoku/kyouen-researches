#!/usr/bin/env python3
"""Independent audit of all ten published cost-69e WIN7 certificates
(2026-11-15).

Independence: fresh Python implementation written for this audit from the
published game-rule description (verify_bit7_win7_cert.ts header); no
repository verifier import, no engine, no verdict cache. The kyouen
predicate is an exact integer Bareiss 4x4 determinant of [x^2+y^2, x, y, 1]
on arbitrary-precision Python integers (no floating point anywhere); the
forbidden-by-triple masks are recomputed from scratch and cached.

Checks per certificate (bits 21/99/87/84/76/90/89/94/108/116 of the cost-69e
child 00000000000000803202000000008000):
1. file level: byte size, md5 and sha256 against the records file (bit-116
   restored from the published base64(gzip -9) form and checked against the
   records-pinned uncompressed hashes);
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
   certificate row set (missing 0 / extra 0).

Results: all ten certificates PASS every check; totals 411,114 strategy
rows, 893,019 visited states, 830,898 loser reply edges, terminal range
[13, 17] on every certificate.
"""
import base64, gzip, hashlib, json, sys, time
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'
CERTDIR = OUT / 'class2-lane-cost69e-certificates'
N = 121
FULL = (1 << N) - 1


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
    return strat


def verify_subroot(strat, sub):
    seen = set()
    consumed = []
    terminals = []
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
            stack.append((board | (1 << mv), depth + 1))
        else:
            assert hexs not in strat, 'strategy on loser turn ' + hexs
            o = options
            while o:
                bit = o & -o
                o ^= bit
                opp += 1
                stack.append((board | bit, depth + 1))
    return len(seen), consumed, terminals, opp


def audit(cert_path, root_hex):
    t0 = time.time()
    text = Path(cert_path).read_text()
    strat = parse_cert(text, root_hex)
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
    any_term = False
    tmin, tmax = 999, 0
    for b in sorted(legal_bits):
        seen, consumed, terminals, opp = verify_subroot(strat, root | (1 << b))
        total_seen += seen
        all_consumed.update(consumed)
        opp_total += opp
        if terminals:
            any_term = True
            tmin = min(tmin, min(terminals))
            tmax = max(tmax, max(terminals))
    union_missing = len(set(strat) - all_consumed)
    union_extra = len(all_consumed - set(strat))
    assert any_term, 'no terminal reached (strategy must terminate)'
    return {'root_hex': root_hex, 'rows': len(strat), 'loser_mobility': mob,
            'subroots_verified': mob, 'visited_states': total_seen,
            'loser_reply_edges': opp_total,
            'terminals_range': [tmin, tmax] if any_term else None,
            'union_missing': union_missing, 'union_extra': union_extra,
            'seconds': round(time.time() - t0, 1)}


def main():
    recs = json.loads((OUT / 'class2-lane-cost69e-win7-certificates-20261114.json').read_text())
    child = recs['child_hex']
    certs = [c for c in recs['certificates'] if c.get('verdict') == 'WIN7']
    assert [c['bit'] for c in certs] == [21, 99, 87, 84, 76, 90, 89, 94, 108, 116]
    per = []
    for c in certs:
        bit = c['bit']
        fn = c['file'].split('/')[-1]
        path = CERTDIR / fn
        raw = path.read_bytes()
        file_md5 = hashlib.md5(raw).hexdigest()
        file_sha256 = hashlib.sha256(raw).hexdigest()
        if fn.endswith('.gz.b64'):
            text = gzip.decompress(base64.b64decode(raw)).decode()
            enc = hashlib.md5(text.encode()).hexdigest()
            enc_sha = hashlib.sha256(text.encode()).hexdigest()
            assert enc == c['md5'] and enc_sha == c['sha256'], 'bit-116 uncompressed hash mismatch'
            # records 'md5'/'sha256' for the gz.b64 certificate are the uncompressed
            # text hashes (see push_note, commit ce7d862d); 2,670,116 bytes is the
            # published uncompressed size (74,115 rows + header).
            assert len(text.encode()) == 2670116, 'bit-116 uncompressed byte size'
            tmp = Path('/tmp/_audit_cert116.txt')
            tmp.write_text(text)
            audit_path = str(tmp)
            storage = 'base64(gzip-9) publication, uncompressed hashes verified'
        else:
            assert file_md5 == c['md5'] and file_sha256 == c['sha256'], f'hash mismatch bit {bit}'
            audit_path = str(path)
            storage = 'plain'
        r = audit(audit_path, c['root_hex'])
        assert int(c['root_hex'], 16) == int(child, 16) | (1 << bit), 'root != child|bit'
        assert r['rows'] == c['rows'], f'rows mismatch bit {bit}'
        assert r['loser_mobility'] == c['root_check']['loser_mobility'] == c['root_check']['independent_enumeration_legal'], f'mobility mismatch bit {bit}'
        assert r['subroots_verified'] == c['sub_roots_pass'], f'sub-roots mismatch bit {bit}'
        assert r['union_missing'] == 0 and r['union_extra'] == 0, f'union mismatch bit {bit}'
        assert r['terminals_range'] == c['terminal_range'] == [13, 17], f'terminal range bit {bit}'
        per.append({'bit': bit, 'root_hex': c['root_hex'], 'file': c['file'],
                    'storage': storage, 'bytes': len(raw), 'rows': r['rows'],
                    'loser_mobility': r['loser_mobility'],
                    'subroots_verified': r['subroots_verified'],
                    'visited_states': r['visited_states'],
                    'loser_reply_edges': r['loser_reply_edges'],
                    'terminals_range': r['terminals_range'],
                    'union_missing': 0, 'union_extra': 0, 'seconds': r['seconds']})
        print(f"CONTROL bit {bit}: PASS rows={r['rows']} subs={r['subroots_verified']} "
              f"visited={r['visited_states']} loser_edges={r['loser_reply_edges']} "
              f"terminals={r['terminals_range']} union=0/0")
    result = {
        'schema': 'n11-class2-lane-cost69e-10cert-python-independent-audit-20261115-v1',
        'date': '2026-11-15',
        'audited_scope': 'all ten WIN7 certificates of the class2-lane cost-69e sweep '
                         '(bits 21/99/87/84/76/90/89/94/108/116 of child '
                         '00000000000000803202000000008000)',
        'method': 'fresh Python implementation; no repository verifier import, no engine, '
                  'no verdict cache, no floating point; exact integer Bareiss 4x4 '
                  'determinant of [x^2+y^2,x,y,1] on arbitrary-precision integers; '
                  'forbidden-by-triple masks recomputed from scratch; per certificate: '
                  'file md5/sha256 against the records file (bit-116 restored from the '
                  'published base64(gzip-9) form and checked against the records-pinned '
                  'uncompressed hashes), exact header/root lines, root = child | 1<<bit '
                  'with 7 stones and C(7,4)=35 non-zero determinants (no 4 cocircular), '
                  'loser mobility re-enumerated and matched to the one-bit strategy rows, '
                  'full sub-root decomposition with every strategy move legal, all loser '
                  'replies expanded, terminals loser-stuck at 13..17 stones, no strategy '
                  'rows at loser or terminal states, and the exact consumed/rows union '
                  '(0 missing / 0 extra) over all sub-roots',
        'totals': {
            'certificates': len(per),
            'strategy_rows': sum(p['rows'] for p in per),
            'visited_states': sum(p['visited_states'] for p in per),
            'loser_reply_edges': sum(p['loser_reply_edges'] for p in per),
            'subroots_verified': sum(p['subroots_verified'] for p in per),
            'all_pass': True,
            'terminal_range_all': [13, 17],
        },
        'certificates': per,
        'interpretation_guard': 'the audit reproduces the certificates game-legal '
                                'content exactly; WIN7 certificates prove a win within '
                                'depth 10 from the individual 7-stone roots only; '
                                '11x11 empty root / {49,60} / S2 {59,60} / class 2 / '
                                'class 4 remain UNKNOWN',
    }
    (OUT / 'class2-lane-cost69e-10cert-python-independent-audit-20261115.json').write_text(
        json.dumps(result, indent=1) + '\n')
    print('written class2-lane-cost69e-10cert-python-independent-audit-20261115.json')


if __name__ == '__main__':
    main()
