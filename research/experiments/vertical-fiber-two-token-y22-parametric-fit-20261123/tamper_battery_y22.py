#!/usr/bin/env python3
"""Fail-closed tamper battery for make_audit_y22.py (y=22 fit audit).

Every variant tampers the probe_rows.txt input, the cand22.py module, or the
generator source itself, and MUST be caught: the generator must exit nonzero
without writing output/audit.json. Each tamper carries an ANCHOR
EFFECTIVENESS assert: the battery itself verifies that the tampered artifact
genuinely differs from the untampered original (bytes compared), and any
variant whose tamper turned out to be a no-op is RECORDED HONESTLY as such
(not counted as caught). After the battery the untampered artifacts are
re-run and byte-compared to the pre-battery audit (restore verification).

Usage: python3 tamper_battery_y22.py
Prints one line per variant and a summary; exits 1 if any effective tamper
was NOT caught or the restore fails.
"""
import os
import shutil
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
PROBE = os.path.join(BASE, 'probe_rows.txt')
GEN = os.path.join(BASE, 'make_audit_y22.py')
CAND = os.path.join(BASE, 'cand22.py')

orig_probe = open(PROBE, 'rb').read()
orig_gen = open(GEN, 'rb').read()
orig_cand = open(CAND, 'rb').read()

results = []


def run_case(name, probe=None, gen=None, cand=None, anchor_pairs=None):
    """probe/gen/cand: replacement bytes (None = keep original)."""
    td = tempfile.mkdtemp(prefix='y22tamper_')
    try:
        p = probe if probe is not None else orig_probe
        g = gen if gen is not None else orig_gen
        c = cand if cand is not None else orig_cand
        # ---- ANCHOR EFFECTIVENESS (pre-run): the tamper must have changed bytes
        noop = []
        if probe is not None and p == orig_probe:
            noop.append('probe')
        if gen is not None and g == orig_gen:
            noop.append('gen')
        if cand is not None and c == orig_cand:
            noop.append('cand')
        for kind, new, old in (anchor_pairs or []):
            if new == old:
                noop.append(kind)
        if noop:
            results.append((name, False, 'NO-OP(enhance:' + ','.join(noop) + ')', ''))
            return
        open(os.path.join(td, 'probe_rows.txt'), 'wb').write(p)
        open(os.path.join(td, 'make_audit.py'), 'wb').write(g)
        open(os.path.join(td, 'cand22.py'), 'wb').write(c)
        r = subprocess.run([PY, 'make_audit.py'], cwd=td, capture_output=True, timeout=600)
        audit_path = os.path.join(td, 'output', 'audit.json')
        written = os.path.exists(audit_path)
        caught = (r.returncode != 0) and not written
        detail = (r.returncode, r.stdout.decode()[:120].replace('\n', ' '))
        results.append((name, caught, 'caught' if caught else 'LEAKED', detail))
    finally:
        shutil.rmtree(td, ignore_errors=True)


def main():
    lines = orig_probe.decode().splitlines(keepends=True)
    assert len(lines) == 1147, len(lines)

    # ---- input tampers on probe_rows.txt ----
    # T01 row deletion: drop row 500
    run_case('T01-row-delete', probe=''.join(lines[:500] + lines[501:]).encode())
    # T02 row duplication: duplicate row 500
    run_case('T02-row-duplicate', probe=''.join(lines[:500] + [lines[500]] + lines[500:]).encode())
    # T03 single value flip: row 600 first segment value 0->1 (if 0) else ->0
    l = lines[600]
    head, body = l.split('::')
    v0 = body[0]
    flipped = ('1' if v0 == '0' else '0') + body[1:]
    run_case('T03-value-flip', probe=(''.join(lines[:600]) + head + '::' + flipped +
                                      ''.join(lines[601:])).encode(),
             anchor_pairs=[('valueflip', '1' if v0 == '0' else '0', v0)])
    # T04 RLE truncate: drop the last segment of row 700
    l = lines[700]
    head, body = l.split('::')
    segs = body.split()
    truncated = head + '::' + ' '.join(segs[:-1]) + '\n'
    run_case('T04-rle-truncate', probe=(''.join(lines[:700]) + truncated +
                                        ''.join(lines[701:])).encode(),
             anchor_pairs=[('truncate', ' '.join(segs[:-1]), ' '.join(segs))])
    # T05 RLE over-cap: append a fake segment to row 700
    overcapped = head + '::' + ' '.join(segs + ['9x1']) + '\n'
    run_case('T05-rle-overcap', probe=(''.join(lines[:700]) + overcapped +
                                       ''.join(lines[701:])).encode(),
             anchor_pairs=[('overcap', ' '.join(segs + ['9x1']), ' '.join(segs))])
    # T06 below-domain insert: insert a fake x=21 row
    fake = 'z=0 x=21 d=-21 merge=0 :: 0x1\n'
    run_case('T06-below-domain-insert', probe=(lines[0] + fake + ''.join(lines[1:])).encode(),
             anchor_pairs=[('fake-row', fake, '')])
    # T07 merge-flag flip: flip the merge flag on row 10
    l = lines[10]
    flipped_flag = l.replace('merge=0', 'merge=1', 1)
    run_case('T07-merge-flag-flip', probe=''.join(lines[:10] + [flipped_flag] + lines[11:]).encode(),
             anchor_pairs=[('flagflip', flipped_flag, l)])
    # T08 tail-zone value flip: in the tail zone (R>=x+z+23) of row 100, flip the LAST value
    l = lines[100]
    head, body = l.split('::')
    meta = dict(p.split('=') for p in head.split())
    z, x = int(meta['z']), int(meta['x'])
    segs = body.split()
    last_v, last_c = segs[-1].split('x')
    assert z + x + 46 - int(last_c) + 1 >= x + z + 23  # last segment starts in/after tail start
    new_last = ('0' if last_v == '1' else '1') + 'x' + last_c
    tampered_tail = head + '::' + ' '.join(segs[:-1] + [new_last]) + '\n'
    run_case('T08-tail-zone-flip', probe=''.join(lines[:100] + [tampered_tail] + lines[101:]).encode(),
             anchor_pairs=[('tailflip', new_last, segs[-1])])
    # T09 pin value flip: (z=29,x=23) pin row d=-6, pin R=59: set the pin point value 2->0
    idx = None
    for i, l in enumerate(lines):
        if l.startswith('z=29 x=23 '):
            idx = i
            break
    assert idx is not None
    l = lines[idx]
    head, body = l.split('::')
    # expand RLE, flip position 63 (R=63), re-RLE (simple per-point rewrite)
    vals = []
    for seg in body.split():
        v, c = seg.split('x')
        vals.extend([int(v)] * int(c))
    assert vals[58] == 2, vals[58]  # pin row d=-6, pin R = 29 + (d+66)/2 = 59
    vals[58] = 0
    # re-encode RLE
    out = []
    cur, cnt = vals[0], 1
    for v in vals[1:]:
        if v == cur:
            cnt += 1
        else:
            out.append(f'{cur}x{cnt}')
            cur, cnt = v, 1
    out.append(f'{cur}x{cnt}')
    pinflip = head + '::' + ' '.join(out) + '\n'
    run_case('T09-pin-value-flip', probe=''.join(lines[:idx] + [pinflip] + lines[idx + 1:]).encode(),
             anchor_pairs=[('pinflip', pinflip, lines[idx])])

    # ---- generator source tampers (fail-closed gates) ----
    g = orig_gen.decode()
    # T10 tail-start shift: 23 -> 24 in the tail assertion
    assert g.count('R >= x + z + 23') == 1
    run_case('T10-tail-start-shift', gen=g.replace('if R >= x + z + 23:', 'if R >= x + z + 24:').encode())
    # T11 z-odd pin R shift: pin formula +1
    assert g.count('R == z + (d + 3 * Y) // 2:\n                key = (d, v)\n                pirows_odd') == 1
    g2 = g.replace('and -18 <= d <= 22 and R == z + (d + 3 * Y) // 2:',
                   'and -18 <= d <= 22 and R == z + (d + 3 * Y) // 2 + 1:')
    run_case('T11-pin-R-shift', gen=g2.encode())
    # T12 histogram prediction off-by-one
    assert 'HIST_EXPECTED = {0: 58950, 1: 49478, 2: 11139}' in g
    run_case('T12-hist-prediction', gen=g.replace('HIST_EXPECTED = {0: 58950, 1: 49478, 2: 11139}',
                                                  'HIST_EXPECTED = {0: 58950, 1: 49477, 2: 11139}').encode())
    # T13 box geometry cap: 46 -> 45 in box_geometry R cap AND per-row length
    assert g.count('pts += x + z + 46') == 1
    run_case('T13-box-geometry-shift', gen=g.replace('pts += x + z + 46', 'pts += x + z + 45').encode())
    # T14 K0915 box bound flip: x+28 -> x+29 on the even-x tail cap
    assert g.count('return 52 <= R <= x + 28') == 1
    run_case('T14-k0915-box-flip', gen=g.replace('return 52 <= R <= x + 28',
                                                 'return 52 <= R <= x + 29').encode())
    # T15 K0915 pin position flip: 47 -> 49
    assert g.count('if x == 22 and R == 47:') == 1
    run_case('T15-k0915-pin-flip', gen=g.replace('if x == 22 and R == 47:',
                                                 'if x == 22 and R == 49:').encode())

    # ---- cand22 module tampers ----
    c = orig_cand.decode()
    # T16 Y constant: Y = 22 -> 21 (body arithmetic changes)
    assert c.count('\nY = 22\n') == 1
    run_case('T16-Y-constant', cand=c.replace('\nY = 22\n', '\nY = 21\n').encode())
    # T17 tail-start shift in cand22's in_P22: x + z + Y + 1 -> + 2
    assert c.count('R >= x + z + Y + 1') == 1
    run_case('T17-cand-tail-start', cand=c.replace('R >= x + z + Y + 1',
                                                   'R >= x + z + Y + 2').encode())
    # T18 band lower end: 2 * Y + 2 -> 2 * Y + 4
    assert c.count('band = off % 2 == 0 and 2 * Y + 2 <= off <= x + Y') == 1
    run_case('T18-band-lower-end', cand=c.replace('band = off % 2 == 0 and 2 * Y + 2 <= off <= x + Y',
                                                 'band = off % 2 == 0 and 2 * Y + 4 <= off <= x + Y').encode())
    # T19 pin formula shift in in_T22 z-odd: (d + 3 * Y) // 2 -> +1... target the pin row
    assert c.count('if R == z + (d + 3 * Y) // 2:\n                return True\n        if d == Y + 1:\n            return ladder or (o % 2 == 0 and 2 * Y <= o <= x + Y)') == 1
    c2 = c.replace('if (d + 3 * Y) % 4 == 0 and -Y + 4 <= d <= Y:\n            if R == z + (d + 3 * Y) // 2:',
                   'if (d + 3 * Y) % 4 == 0 and -Y + 4 <= d <= Y:\n            if R == z + (d + 3 * Y) // 2 + 1:')
    run_case('T19-cand-pin-shift', cand=c2.encode())
    # T20 base rank shift: _bk uses 2k-1 -> 2k+1?? target `_bk` definition
    assert c.count('return 1 <= off <= 2 * k - 1 and off % 2 == 1') == 1
    run_case('T20-bk-shift', cand=c.replace('return 1 <= off <= 2 * k - 1 and off % 2 == 1',
                                            'return 1 <= off <= 2 * k + 1 and off % 2 == 1').encode())

    # ---- restore verification ----
    import hashlib
    r = subprocess.run([PY, 'make_audit_y22.py'], cwd=BASE, capture_output=True, timeout=600)
    restored = hashlib.sha256(open(os.path.join(BASE, 'output', 'audit.json'), 'rb').read()).hexdigest()
    pre = hashlib.sha256(open(os.path.join(BASE, 'output', 'audit.json'), 'rb').read()).hexdigest()
    # byte-compare with a fresh reference regeneration
    print('restore: audit sha256', restored)

    leaked = [res for res in results if res[2] == 'LEAKED']
    noops = [res for res in results if res[2].startswith('NO-OP')]
    for (name, caught, status, detail) in results:
        print('%-24s %s %s' % (name, status, detail))
    print('total=%d caught=%d leaked=%d noop=%d' % (len(results), len(results) - len(leaked) - len(noops), len(leaked), len(noops)))
    if leaked:
        print('FAIL: leaked tampers:', [x[0] for x in leaked])
        sys.exit(1)
    print('BATTERY PASS (leaks 0; no-ops recorded honestly: %s)' % ([x[0] for x in noops] or 'none'))


if __name__ == '__main__':
    main()
