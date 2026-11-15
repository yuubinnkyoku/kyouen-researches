#!/usr/bin/env python3
"""Second independent reconstruction of output/tmp-cost83d/ for
recompute_frontier_cost83d_receipts_20261115.py.

A first, simpler reconstruction script
(reconstruct_tmp_cost83d_20261115.py, git blob 591716b8, landed with the
cost-84a in-flight claim commit) already regenerates the fold script's
runtime inputs: it derives the legal loser first moves from the published
legal_candidates module and runs the published BigInt / TS-Bareiss
verifiers, but asserts nothing against the published head JSON records
and pins no certificate part. This second implementation (new file, the
first is unchanged on main, following the published chain-roots audit
v6/v7 dual-implementation pattern) regenerates the same 13 files the
fold script reads from artifacts that ARE on main, with fresh
exact-integer geometry and full cross-assertions - no lane-local state:

  - legal-moves.json         : regenerated from scratch: the legal loser
    first moves at each 7-stone root are recomputed with exact-integer
    Bareiss 4x4 determinants of [x^2+y^2,x,y,1] and asserted to number
    sub_roots_pass per root (62/58/68 == published sub_roots_pass);
  - bit{b}.cert-receipt.json : recomputed from the two published
    certificate parts joined with CRLF->LF normalization (the joined
    bytes must match the published head JSON records' md5/rows:
    class-frontier-cost83d-receipts-recompute-20261115.json,
    cost83d_addition); each part is pinned to its main git blob sha;
  - bit{b}.bigint.json     : fresh run of the published independent
    verifier scripts/verify_win7_certificate_bigint_independent.mjs;
  - bit{b}.tsverify.json   : fresh run of the published independent
    verifier scripts/verify_bit7_win7_cert.ts (--root-check line, then
    --subroots with the full legal-move list, --consumed-out);
  - bit{b}.consumed.txt    : the consumed winner-state keys emitted by the
    TS verifier run (their set must equal the full certificate row set).

The reconstruction is cross-checked at every step: md5/rows of the joined
certificates vs the published head JSON records, mobility vs
sub_roots_pass, TS loserMobility vs the same, consumed set vs the strategy
row set. The final proof that the reconstruction is faithful is left to
the published fold script itself: after this repair it re-runs end-to-end
and asserts every control against these files plus its own published
outputs (head 1314, head JSON blob 49cb8022..., ranking d8adfb7e...,
top-candidates 454568f2...). The fold script runs equally well from the
first implementation's outputs: legal-moves.json, the three consumed
files and the three joined certificate byte streams are byte-identical
between the two implementations, and the receipts / BigInt / TS-verify
JSONs agree field-by-field when parsed.
"""
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'
TMP = OUT / 'tmp-cost83d'
CERTS = OUT / 'class2-lane-cost83d-certificates'
TMP.mkdir(parents=True, exist_ok=True)

XR = [i % 11 for i in range(121)]
YR = [i // 11 for i in range(121)]
QR = [XR[i] * XR[i] + YR[i] * YR[i] for i in range(121)]

# blob pins of the published (raw-CDN-verified) inputs used here
PIN_HEAD_JSON = ('49cb8022bc715fa22d7c2d483160083478676caa', 7407)
PIN_PARTS = {
    16: [('44176845d520a7feb3d1d18d3b1912a388c13623', 1226499),
         ('adb6daf529884d729731d45afa6c72b3dc7d2016', 1226472)],
    51: [('6a00807a4b47372df118b4dc4d6f80cf10d4be3b', 1049949),
         ('08378253032b6cb56d7ba914c9c6036aeaf2a96b', 1049928)],
    82: [('14559e5787772a4bd65f982181e8b05770d2d24b', 1638728),
         ('126b0a5f56c3ae7ed6ff94f6049225c9f30355cc', 1638684)],
}


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


def blob_of(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest(), len(data)


sha, blen = blob_of(OUT / 'class-frontier-cost83d-receipts-recompute-20261115.json')
assert (sha, blen) == PIN_HEAD_JSON, (sha, blen)
head = json.loads((OUT / 'class-frontier-cost83d-receipts-recompute-20261115.json').read_text())
add = {r['bit']: r for r in head['cost83d_addition']}
BITS = [16, 51, 82]
assert sorted(add) == BITS

# ---------- 1. legal-moves.json: regenerate from exact-integer geometry ----------
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
(TMP / 'legal-moves.json').write_text(json.dumps(legal_moves, indent=1) + '\n')
print('tmp-cost83d/legal-moves.json regenerated (fresh Bareiss geometry, '
      'independent of the legal_candidates module used by the first '
      'implementation)')

# ---------- 2. per-bit: joined certificate, receipt, BigInt, TS, consumed ----------
sums = {'rows': 0, 'bytes': 0, 'sub_roots': 0}
for bit in BITS:
    rec = add[bit]
    root_hex = rec['root_hex']
    parts = sorted(CERTS.glob(f'bit{bit}-root-{root_hex}.cert.part*of2'))
    assert len(parts) == 2, (bit, parts)  # all 3 83d certificates are split pushes
    for p, pin in zip(parts, PIN_PARTS[bit]):
        assert blob_of(p) == pin, (bit, p.name, blob_of(p))
    whole = b''.join(p.read_bytes().replace(b'\r\n', b'\n') for p in parts)
    cert_path = TMP / f'c83d-bit{bit}.cert'
    cert_path.write_bytes(whole)
    lines = whole.splitlines()
    assert lines[0] == b'n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS'
    assert lines[1] == b'root ' + root_hex.encode(), bit
    rows = lines[2:]
    assert len(rows) == rec['rows'], (bit, len(rows), rec['rows'])
    assert rows == sorted(set(rows)), bit
    assert hashlib.md5(whole).hexdigest() == rec['md5'], bit

    # cert receipt (same core fields as the first implementation's receipts,
    # plus the split-part pins so the join is fully determined)
    rel = ('research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/'
           f'class2-lane-cost83d-certificates/')
    receipt = {
        'bit': bit, 'root_hex': root_hex, 'rows': len(rows), 'bytes': len(whole),
        'md5': hashlib.md5(whole).hexdigest(),
        'sha256': hashlib.sha256(whole).hexdigest(),
        'git_blob_sha': git_blob_sha_bytes(whole),
        'parts': [
            {'name': p.name, 'bytes': p.stat().st_size,
             'git_blob_sha': blob_of(p)[0]} for p in parts],
        'join': 'concat part1of2 + part2of2 with CRLF->LF normalization',
        'path': rel,
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
    assert bj['root_hex'] == root_hex and bj['strategy_rows'] == rec['rows'], bit
    assert bj['subroots_passed'] == rec['sub_roots_pass'], bit
    assert bj['union_missing'] == 0 and bj['union_extra'] == 0, bit
    assert bj['terminal_range'] == [13, 17], bit
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
    assert ts['rows'] == rec['rows'], (bit, ts['rows'], rec['rows'])
    stats = ts['stats']
    assert sorted(int(k[1:]) for k in stats) == sorted(legal_moves[str(bit)]['moves']), bit
    assert all(s['range'][0] >= 13 and s['range'][1] <= 17 for s in stats.values()), bit
    (TMP / f'bit{bit}.tsverify.json').write_text(
        json.dumps(rc) + '\n' + json.dumps(ts) + '\n')
    consumed = [x for x in consumed_out.read_text().split() if x]
    assert len(set(consumed)) == rec['rows'], (bit, len(set(consumed)), rec['rows'])
    assert set(consumed) == {r.decode().split()[0] for r in rows}, bit
    print(f'bit {bit}: TS Bareiss verifier PASS ({len(stats)} sub-roots, '
          f'{len(set(consumed))} consumed winner rows == strategy rows)')

    sums['rows'] += len(rows)
    sums['bytes'] += len(whole)
    sums['sub_roots'] += rec['sub_roots_pass']

assert sums == {'rows': 216638, 'bytes': 7830260, 'sub_roots': 188}, sums
print('reconstruction complete: tmp-cost83d/ 13 files regenerated '
      'from main artifacts; totals 216,638 rows / 7,830,260 bytes / 188 '
      'sub-roots == the published head JSON totals')
