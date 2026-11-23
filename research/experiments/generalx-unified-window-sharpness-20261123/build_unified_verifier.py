#!/usr/bin/env python3
"""build_unified_verifier.py -- provenance gate for the engine block embedded
in verify_unified_window_sharpness.py.

The engine + closed-form block (mex / H_ordered / H_canonical / vC / vO /
q_odd / single_token) is machine-extracted (zero hand transcription) from the
published K1264 verifier
  research/experiments/generalx-min-token-lowr-staircase-20261123/verify_min_token_staircase.py
(SHA-256 pin below), between the cut markers:
    start: first line equal to 'def mex(values):'
    end:   line before the first line starting with 'SELF_SHA = hashlib'
The same cut is applied to this verifier between its '# === ENGINE BLOCK' and
'# === END ENGINE BLOCK' markers, and the two blocks are compared
byte-for-byte. Exit 0 iff identical (and the source sha matches the pin).
"""
import hashlib, os, sys

SRC_REL = os.path.join('..', 'generalx-min-token-lowr-staircase-20261123',
                      'verify_min_token_staircase.py')
SRC_PIN = '108fdd65a96588b32cfd64503cf2a22f999d6e4eefded775bb6fda32568e69fa'
SELF_REL = 'verify_unified_window_sharpness.py'

def cut_k1264(text):
    lines = text.split('\n')
    s = None
    for i, ln in enumerate(lines):
        if ln == 'def mex(values):':
            s = i
            break
    if s is None:
        raise SystemExit('start marker not found in K1264 verifier')
    e = None
    for j in range(s, len(lines)):
        if lines[j].startswith('SELF_SHA = hashlib'):
            e = j
            break
    if e is None:
        raise SystemExit('end marker not found in K1264 verifier')
    # strip trailing blank lines of the block
    block = lines[s:e]
    while block and block[-1].strip() == '':
        block.pop()
    return '\n'.join(block) + '\n'

def cut_self(text):
    lines = text.split('\n')
    s = e = None
    for i, ln in enumerate(lines):
        if ln.startswith('# === ENGINE BLOCK'):
            s = i + 1
        if ln.startswith('# === END ENGINE BLOCK'):
            e = i
    if s is None or e is None or e <= s:
        raise SystemExit('engine block markers not found in this verifier')
    block = lines[s:e]
    while block and block[-1].strip() == '':
        block.pop()
    return '\n'.join(block) + '\n'

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.normpath(os.path.join(here, SRC_REL))
    self_path = os.path.join(here, SELF_REL)
    src_bytes = open(src_path, 'rb').read()
    src_sha = hashlib.sha256(src_bytes).hexdigest()
    if src_sha != SRC_PIN:
        print('K1264 verifier sha mismatch:', src_sha)
        sys.exit(1)
    print('K1264 verifier sha256 PIN OK:', src_sha)
    b1 = cut_k1264(src_bytes.decode('utf-8'))
    self_bytes = open(self_path, 'rb').read()
    b2 = cut_self(self_bytes.decode('utf-8'))
    same = b1 == b2
    print('engine block bytes:', len(b1.encode()), 'vs', len(b2.encode()))
    print('engine block sha256:',
          hashlib.sha256(b1.encode()).hexdigest())
    print('byte-identical:', same)
    if not same:
        sys.exit(1)
    print('PROVENANCE PASS')
    sys.exit(0)

if __name__ == '__main__':
    main()
