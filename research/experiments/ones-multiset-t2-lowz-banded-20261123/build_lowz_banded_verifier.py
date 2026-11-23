#!/usr/bin/env python3
"""build_lowz_banded_verifier.py -- provenance gate for the engine block
embedded in verify_ones_multiset_t2_lowz_banded.py.

The engine + closed-form block (mex / H_ordered / H_canonical / vC / vO /
q_odd / single_token) is machine-extracted (zero hand transcription) from the
published unified-window verifier
  research/experiments/generalx-unified-window-sharpness-20261123/verify_unified_window_sharpness.py
(SHA-256 pin below), between the cut markers:
    start: line starting with '# === ENGINE BLOCK' (block = lines after it)
    end:   line starting with '# === END ENGINE BLOCK' (exclusive)
The published extraction of that same source was pinned in the published
unified-window report as engine block 2,508 bytes / SHA-256 bd5f22e4...
(provenance chain K1138 -> y22 K1257 -> K1264 108fdd65... -> unified window
0ab66665...). The same cut is applied to this verifier, and the two blocks
are compared byte-for-byte plus a sha256 pin. Exit 0 iff identical (and the
source sha matches its pin and the block sha matches its pin).
"""
import hashlib, os, sys

SRC_REL = os.path.join('..', 'generalx-unified-window-sharpness-20261123',
                       'verify_unified_window_sharpness.py')
SRC_PIN = '0ab66665dc9990f5399a661ccb2f9c3ba75f5a010c7e915f6a44e3d4fe6d3103'
BLK_PIN = 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'
SELF_REL = 'verify_ones_multiset_t2_lowz_banded.py'

def cut_marker(text):
    lines = text.split('\n')
    s = e = None
    for i, ln in enumerate(lines):
        if ln.startswith('# === ENGINE BLOCK') and s is None:
            s = i + 1
        if ln.startswith('# === END ENGINE BLOCK'):
            e = i
    if s is None or e is None or e <= s:
        raise SystemExit('engine block markers not found')
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
        print('unified-window verifier sha mismatch:', src_sha)
        sys.exit(1)
    print('unified-window verifier sha256 PIN OK:', src_sha)
    b1 = cut_marker(src_bytes.decode('utf-8'))
    self_bytes = open(self_path, 'rb').read()
    b2 = cut_marker(self_bytes.decode('utf-8'))
    h1 = hashlib.sha256(b1.encode()).hexdigest()
    h2 = hashlib.sha256(b2.encode()).hexdigest()
    print('engine block bytes:', len(b1.encode()), 'vs', len(b2.encode()))
    print('engine block sha256:', h1)
    if h1 != BLK_PIN:
        print('engine block sha does not match published block pin')
        sys.exit(1)
    print('published engine block sha256 PIN OK:', h1)
    same = b1 == b2
    print('byte-identical:', same)
    if not same:
        print('self block sha256:', h2)
        sys.exit(1)
    print('PROVENANCE PASS')
    sys.exit(0)

if __name__ == '__main__':
    main()
