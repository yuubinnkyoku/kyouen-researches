#!/usr/bin/env python3
"""Build fold_win8_root00901010_preverified.py from the PUBLISHED fold18 machine.

Adopted rerun-gate redesign (research/log/2026-11-20-n11-fold-machine-rerun-gate-scaling-note.md
+ research/log/2026-11-20-n11-fold19-preverified-chain-adoption.md):
the preverified copy of the published fold18 machine skips ONLY its seven recursive
rerun gate blocks (fold11..fold17 machine re-execution) when the environment variable
FOLD_PREVERIFIED_CHAIN=1 is set.  All input SHA pins, the full frontier chain
recomputation, the K1120 certificate 19-gate block, the K1097 refsolve crosscheck,
the two-method coverage geometry, and the receipt application are unchanged and
always execute; default (env unset) behavior is byte-for-byte the published machine's
semantics (full chain).

Every inserted line carries the marker FOLD_PREVERIFIED_CHAIN_GUARD so that the
patch is exactly reversible: dropping the marked lines and restoring the 4-space
indentation inside the guarded blocks reproduces the published machine byte-exactly
(checked at the end of this script and re-checked by the fold19 machine gate).

Usage:  python3 make_preverified_patch.py [W_root]   (default /home/user/work/W19)
Input:  <W>/fold_win8_root00901010.py   (published fold18 machine, sha-pinned below)
Output: <W>/fold_win8_root00901010_preverified.py
"""
import hashlib, os, sys, py_compile

W = os.environ.get('PATCH_W', sys.argv[1] if len(sys.argv) > 1 else '/home/user/work/W19')
SRC = f'{W}/fold_win8_root00901010.py'
DST = f'{W}/fold_win8_root00901010_preverified.py'
PIN_PUB = 'dcdfbf92d62409cc3a92f9f16f319e1328180622660b39751921b5de72800091'  # published fold18 machine

MARK = 'FOLD_PREVERIFIED_CHAIN_GUARD'
PREV_LINE = "PREVERIFIED = os.environ.get('FOLD_PREVERIFIED_CHAIN', '') == '1'  # " + MARK + " NOTE"

# (block header line, block last line) for the seven rerun gate blocks
BLOCKS = [
    ("# ---------- fold11 machine byte-identical rerun (published scripts source) ----------",
     "print('fold11 machine rerun verified: stdout ends ' + _rr.stdout.strip().splitlines()[-1][:80])"),
    ("# ---------- fold12 machine byte-identical rerun (published scripts source) ----------",
     "print('fold12 machine rerun verified: stdout ends ' + _rr12.stdout.strip().splitlines()[-1][:80])"),
    ("# ---------- fold13 machine byte-identical rerun (published scripts source) ----------",
     "print('fold13 machine rerun verified: stdout ends ' + _rr13.stdout.strip().splitlines()[-1][:80])"),
    ("# ---------- fold14 machine byte-identical rerun (published scripts source) ----------",
     "print('fold14 machine rerun verified: stdout ends ' + _rr14.stdout.strip().splitlines()[-1][:80])"),
    ("# ---------- fold15 machine byte-identical rerun (published scripts source) ----------",
     "print('fold15 machine rerun verified: stdout ends ' + _rr15.stdout.strip().splitlines()[-1][:80])"),
    ("# ---------- fold16 machine byte-identical rerun (published scripts source) ----------",
     "print('fold16 machine rerun verified: stdout ends ' + _rr16.stdout.strip().splitlines()[-1][:80])"),
    ("# ---------- fold17 machine byte-identical rerun (published scripts source) ----------",
     "print('fold17 machine rerun verified: stdout ends ' + _rr17.stdout.strip().splitlines()[-1][:80])"),
]

def die(m):
    print('PATCH FAILED:', m); sys.exit(1)

src = open(SRC, 'rb').read()
if hashlib.sha256(src).hexdigest() != PIN_PUB:
    die('pristine fold18 machine sha256 mismatch (expected published ' + PIN_PUB + ')')
text = src.decode()
lines = text.split('\n')

# insert PREVERIFIED definition right after the imports line
imp = "from itertools import combinations"
if lines.count(imp) != 1:
    die('import anchor count != 1')
idx = lines.index(imp)
lines = lines[:idx + 1] + [PREV_LINE, ''] + lines[idx + 1:]

for header, last in BLOCKS:
    if lines.count(header) != 1: die('block header count != 1: ' + header)
    if lines.count(last) != 1: die('block end count != 1: ' + last)
    i = lines.index(header)
    j = lines.index(last)
    if j < i: die('block end before header')
    block = lines[i:j + 1]
    guarded = ['if not PREVERIFIED:  # ' + MARK + ' BEGIN']
    for l in block:
        guarded.append(('    ' + l) if l else l)
    guarded.append('# ' + MARK + ' END')
    lines = lines[:i] + guarded + lines[j + 1:]

out = '\n'.join(lines)
open(DST, 'w').write(out)
py_compile.compile(DST, doraise=True)

# exact reverse patch check: marked lines dropped, guarded blocks dedented -> published bytes
rev = []
i = 0
guarded_in_block = False
for l in lines:
    if MARK in l:
        if l.strip() == 'if not PREVERIFIED:  # ' + MARK + ' BEGIN':
            guarded_in_block = True
        elif l.strip() == '# ' + MARK + ' END':
            guarded_in_block = False
        elif l == PREV_LINE:
            pass
        else:
            die('unexpected guard marker line: ' + l)
        continue
    if guarded_in_block and l:
        if not l.startswith('    '): die('reverse: line inside guard lacks indent: ' + l)
        rev.append(l[4:])
    else:
        rev.append(l)
rev_text = '\n'.join(rev)
if hashlib.sha256(rev_text.encode()).hexdigest() != PIN_PUB:
    die('reverse patch does not reproduce published machine')
print('patch OK: %s' % DST)
print('patched sha256: %s' % hashlib.sha256(out.encode()).hexdigest())
print('reverse patch reproduces published machine byte-exactly')
print('guard marker lines: %d' % sum(1 for l in lines if MARK in l))
