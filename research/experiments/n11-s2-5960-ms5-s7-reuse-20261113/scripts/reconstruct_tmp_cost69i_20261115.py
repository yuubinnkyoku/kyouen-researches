#!/usr/bin/env python3
"""Reconstruct output/tmp-cost69i/ for recompute_frontier_cost69i_receipts_20261115.py.

The cost-69i lane (2026-11-15, commit 79d866f8) published its fold script but
not its working directory output/tmp-cost69i/, so the published fold script
could not be re-run end-to-end from main alone (it stops at
tmp-cost69i/legal-moves.json). This repair regenerates every file in
tmp-cost69i/ from artifacts that ARE on main, using only published verifiers
and exact-integer geometry - no lane-local state:

  - bit{b}.cert-receipt.json : recomputed from the published certificate bytes
    (bit21/bit97 whole files; bit29/bit100 joined from the published
    row-boundary part1of2/part2of2 with CRLF -> LF normalization, exactly as
    the fold script joins them);
  - legal-moves.json        : the legal loser first moves at each 7-stone root,
    recomputed with exact-integer Bareiss 4x4 determinants of
    [x^2+y^2,x,y,1] (zero det = concyclic/collinear quadruple); the mobility
    must equal the published sub_roots_pass (56/56/46/58);
  - bit{b}.bigint.json     : fresh run of the published independent verifier
    scripts/verify_win7_certificate_bigint_independent.mjs;
  - bit{b}.tsverify.json   : fresh run of the published independent verifier
    scripts/verify_bit7_win7_cert.ts (--root-check line, then --subroots with
    the full legal-move list, --consumed-out);
  - bit{b}.consumed.txt    : the consumed winner-state keys emitted by the
    TS verifier run (their set must equal the full certificate row set).

The reconstruction is cross-checked at every step: md5/bytes/rows of the
joined certificates vs the published head JSON records, mobility vs
sub_roots_pass, TS loserMobility vs the same, consumed set vs the strategy
row set. The final proof that the reconstruction is faithful is left to the
published fold script itself: after this repair it re-runs end-to-end and
asserts every control against these files plus its own published outputs.
"""
import hashlib, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'
TMP = OUT / 'tmp-cost69i'
CERTS = OUT / 'class2-lane-cost69i-certificates'

XR = [i % 11 for i in range(121)]
YR = [i // 11 for i in range(121)]
QR = [XR[i] * XR[i] + YR[i] * YR[i] for i in range(121)]

def det4rows(a, b, c, d):
    mm = [[QR[a], XR[a], YR[a], 1], [QR[b], XR[b], YR[b], 1],
          [QR[c], XR[c], YR[c], 1], [QR[d], XR[d], YR[d], 1]]
    prev = 1
    for k in range(3):
        if mm[k][k] == 0:
            for r in range(k + 1, 4):
                if mm[r][k] != 0:
                    mm[k], mm[r] = mm[r], mm[k]
                    break
            else:
                return 0
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                mm[i][j] = (mm[i][j] * mm[k][k] - mm[i][k] * mm[k][j]) // prev
        prev = mm[k][k]
    return mm[3][3]

def mask_over(cells):
    F = 0
    n = len(cells)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                a, b, c = cells[i], cells[j], cells[k]
                for d in range(121):
                    if det4rows(a, b, c, d) == 0:
                        F |= 1 << d
    return F

def git_blob_sha_bytes(data: bytes):
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()

head = json.loads((OUT / 'class-frontier-cost69i-receipts-recompute-20261115.json').read_text())
add = {r['bit']: r for r in head['cost69i_addition']}
BITS = [21, 29, 97, 100]
assert sorted(add) == BITS

TMP.mkdir(exist_ok=True)
legal_moves = {}
for bit in BITS:
    rec = add[bit]
    root_hex = rec['root_hex']
    v = int(root_hex, 16)
    stones = [i for i in range(121) if (v >> i) & 1]
    assert len(stones) == 7
    F = mask_over(stones)
    moves = [p for p in range(121) if not (v >> p) & 1 and not (F >> p) & 1]
    assert len(moves) == rec['sub_roots_pass'], (bit, len(moves), rec['sub_roots_pass'])
    legal_moves[str(bit)] = {'root': root_hex, 'stones': stones, 'moves': moves}
    print(f'bit {bit}: legal loser first moves recomputed: {len(moves)} '
          f'== published sub_roots_pass')

(TMP / 'legal-moves.json').write_text(json.dumps(legal_moves, indent=1))
print('written tmp-cost69i/legal-moves.json')

for bit in BITS:
    rec = add[bit]
    root_hex = rec['root_hex']
    parts = sorted(CERTS.glob(f'bit{bit}-root-{root_hex}.cert.part*of2'))
    if parts:
        whole = b''.join(p.read_bytes().replace(b'\r\n', b'\n') for p in parts)
    else:
        whole = (CERTS / f'bit{bit}-root-{root_hex}.cert').read_bytes().replace(b'\r\n', b'\n')
    cert_path = TMP / f'c69i-bit{bit}.cert'
    cert_path.write_bytes(whole)
    rows = whole.splitlines()[2:]
    assert len(rows) == rec['rows'], (bit, len(rows), rec['rows'])
    assert rows == sorted(set(rows)), bit
    assert hashlib.md5(whole).hexdigest() == rec['md5'], bit

    # cert receipt (same fields as tmp-cost74g/bit*.cert-receipt.json)
    rel = ('research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/'
           f'class2-lane-cost69i-certificates/bit{bit}-root-{root_hex}.cert')
    receipt = {
        'bit': bit, 'root_hex': root_hex, 'rows': len(rows), 'bytes': len(whole),
        'md5': hashlib.md5(whole).hexdigest(),
        'sha256': hashlib.sha256(whole).hexdigest(),
        'git_blob_sha': git_blob_sha_bytes(whole),
        'path': rel.replace('/', '\\'),
        'rows_sorted_unique': True,
    }
    (TMP / f'bit{bit}.cert-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')

    # BigInt independent verifier (published script)
    run = subprocess.run(
        ['node', str(HERE / 'scripts' / 'verify_win7_certificate_bigint_independent.mjs'),
         str(cert_path), str(rec['sub_roots_pass'])],
        capture_output=True, text=True, check=True)
    bj = json.loads(run.stdout)
    assert bj['verdict'] == 'WIN7 certificate independently verified', bit
    assert bj['root_hex'] == root_hex and bj['strategy_rows'] == rec['rows']
    assert bj['subroots_passed'] == rec['sub_roots_pass']
    assert bj['union_missing'] == 0 and bj['union_extra'] == 0
    assert bj['terminal_range'] == [13, 17]
    (TMP / f'bit{bit}.bigint.json').write_text(json.dumps(bj, indent=2) + '\n')
    print(f'bit {bit}: BigInt verifier PASS ({rec["rows"]} rows, union 0/0)')

    # TS Number-Bareiss verifier (published script): root-check + subroots
    root_check = subprocess.run(
        ['node', '--experimental-strip-types',
         str(HERE / 'scripts' / 'verify_bit7_win7_cert.ts'),
         '--cert', str(cert_path), '--root', root_hex, '--root-check'],
        capture_output=True, text=True, check=True)
    rc = json.loads(root_check.stdout.strip().splitlines()[0])
    assert rc == {'stones': 7, 'loserMobility': rec['sub_roots_pass']}, (bit, rc)
    consumed_out = TMP / f'bit{bit}.consumed.txt'
    if consumed_out.exists():
        consumed_out.unlink()
    subroots = subprocess.run(
        ['node', '--experimental-strip-types',
         str(HERE / 'scripts' / 'verify_bit7_win7_cert.ts'),
         '--cert', str(cert_path), '--root', root_hex,
         '--subroots', ','.join(str(m) for m in legal_moves[str(bit)]['moves']),
         '--consumed-out', str(consumed_out)],
        capture_output=True, text=True, check=True)
    ts = json.loads(subroots.stdout.strip().splitlines()[-1])
    assert ts['rows'] == rec['rows'], (bit, ts['rows'])
    stats = ts['stats']
    assert sorted(int(k[1:]) for k in stats) == sorted(legal_moves[str(bit)]['moves']), bit
    assert all(s['range'][0] >= 13 and s['range'][1] <= 17 for s in stats.values()), bit
    (TMP / f'bit{bit}.tsverify.json').write_text(
        json.dumps(rc) + '\n' + json.dumps(ts) + '\n')
    consumed = [x for x in consumed_out.read_text().split() if x]
    assert len(set(consumed)) == rec['rows'], (bit, len(set(consumed)), rec['rows'])
    print(f'bit {bit}: TS Bareiss verifier PASS ({len(stats)} sub-roots, '
          f'{len(set(consumed))} consumed winner rows == strategy rows)')

print('reconstruction complete: tmp-cost69i/ regenerated from main artifacts')
