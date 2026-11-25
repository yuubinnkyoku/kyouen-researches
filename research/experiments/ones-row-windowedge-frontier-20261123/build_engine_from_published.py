#!/usr/bin/env python3
"""build_engine_from_published.py -- provenance gate for the engine block
embedded in verify_ones_row_frontier.py.

The engine + closed-form block (mex / H_ordered / H_canonical / vC / vO /
q_odd / single_token) is machine-compared (zero hand transcription) against
TWO published verifiers:
  src1 (older): research/experiments/generalx-min-token-lowr-staircase-20261123/
               verify_min_token_staircase.py   (published K1264 verifier)
  src2 (newer): research/experiments/generalx-unified-window-sharpness-20261123/
               verify_unified_window_sharpness.py (published K1268 machine,
               whose own build gate extracts byte-exactly from src1)
Cuts: src1 between the lines 'def mex(values):' and the first line starting
with 'SELF_SHA = hashlib'; src2 and this machine between their
'# === ENGINE BLOCK' and '# === END ENGINE BLOCK' markers. Trailing blank
lines are stripped in all cuts. Exit 0 iff both sha pins match and all three
blocks are byte-identical.
"""
import hashlib, os, sys

SRC1_REL = os.path.join('..', 'generalx-min-token-lowr-staircase-20261123',
                        'verify_min_token_staircase.py')
SRC1_PIN = '108fdd65a96588b32cfd64503cf2a22f999d6e4eefded775bb6fda32568e69fa'
SRC2_REL = os.path.join('..', 'generalx-unified-window-sharpness-20261123',
                        'verify_unified_window_sharpness.py')
SRC2_PIN = '0ab66665dc9990f5399a661ccb2f9c3ba75f5a010c7e915f6a44e3d4fe6d3103'
SELF_REL = 'verify_ones_row_frontier.py'


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
    block = lines[s:e]
    while block and block[-1].strip() == '':
        block.pop()
    return '\n'.join(block) + '\n'


def cut_markers(text):
    lines = text.split('\n')
    s = e = None
    for i, ln in enumerate(lines):
        if ln.startswith('# === ENGINE BLOCK'):
            s = i + 1
            break
    for j in range(s, len(lines)):
        if lines[j].startswith('# === END ENGINE BLOCK'):
            e = j
            break
    if s is None or e is None or e <= s:
        raise SystemExit('engine block markers not found')
    block = lines[s:e]
    while block and block[-1].strip() == '':
        block.pop()
    return '\n'.join(block) + '\n'


def load_pinned(rel, pin):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), rel)
    data = open(path, 'rb').read()
    sha = hashlib.sha256(data).hexdigest()
    if sha != pin:
        print('sha mismatch for', rel, ':', sha)
        sys.exit(1)
    print('pin OK:', os.path.basename(path), sha)
    return data.decode('utf-8')


def main():
    src1 = load_pinned(SRC1_REL, SRC1_PIN)
    src2 = load_pinned(SRC2_REL, SRC2_PIN)
    self_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), SELF_REL)
    self_bytes = open(self_path, 'rb').read()
    b1 = cut_k1264(src1)
    b2 = cut_markers(src2)
    b3 = cut_markers(self_bytes.decode('utf-8'))
    for name, b in (('k1264', b1), ('unified', b2), ('self', b3)):
        print(name, 'engine block bytes:', len(b.encode()),
              'sha256:', hashlib.sha256(b.encode()).hexdigest())
    three_way = (b1 == b2 == b3)
    print('three-way byte-identical:', three_way)
    if not three_way:
        sys.exit(1)
    print('PROVENANCE PASS')
    sys.exit(0)


if __name__ == '__main__':
    main()
