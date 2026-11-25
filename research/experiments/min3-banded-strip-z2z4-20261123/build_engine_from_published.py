#!/usr/bin/env python3
"""build_engine_from_published.py -- provenance gate for the engine block
embedded in verify_min3_banded_strip.py.

The engine + closed-form block (mex / H_ordered / H_canonical / vC / vO /
q_odd / single_token, 2,508 bytes) is machine-compared (zero hand
transcription) against THREE published verifiers:
  src1: research/experiments/generalx-min-token-lowr-staircase-20261123/
        verify_min_token_staircase.py          (published K1264 verifier)
  src2: research/experiments/generalx-unified-window-sharpness-20261123/
        verify_unified_window_sharpness.py    (published K1268 machine)
  src3: research/experiments/ones-row-windowedge-frontier-20261123/
        verify_ones_row_frontier.py           (published K1271 machine)
Cuts: src1 between the lines 'def mex(values):' and the first line starting
with 'SELF_SHA = hashlib' (trailing blank lines stripped); src2, src3 and
this machine between their '# === ENGINE BLOCK' and
'# === END ENGINE BLOCK' markers (trailing blank lines stripped).
Exit 0 iff the three source sha256 pins match, all four blocks are
byte-identical, and the common block matches the published engine pin
bd5f22e4... (i.e., this machine's engine is byte-exact). Fail-closed:
PROVENANCE PASS is printed only on success; rc=1 otherwise.
"""
import hashlib, os, sys

SRC1_REL = os.path.join('..', 'generalx-min-token-lowr-staircase-20261123',
                        'verify_min_token_staircase.py')
SRC1_PIN = '108fdd65a96588b32cfd64503cf2a22f999d6e4eefded775bb6fda32568e69fa'
SRC2_REL = os.path.join('..', 'generalx-unified-window-sharpness-20261123',
                        'verify_unified_window_sharpness.py')
SRC2_PIN = '0ab66665dc9990f5399a661ccb2f9c3ba75f5a010c7e915f6a44e3d4fe6d3103'
SRC3_REL = os.path.join('..', 'ones-row-windowedge-frontier-20261123',
                        'verify_ones_row_frontier.py')
SRC3_PIN = '1ce7df23f15165180773fcfd45c9b789e0f22981a148fdc07e6708cbb5e43173'
ENGINE_PIN = ('bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12'
              'e3a92')
SELF_REL = 'verify_min3_banded_strip.py'


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
    if s is None:
        raise SystemExit('engine block markers not found')
    for j in range(s, len(lines)):
        if lines[j].startswith('# === END ENGINE BLOCK'):
            e = j
            break
    if e is None or e <= s:
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
    src3 = load_pinned(SRC3_REL, SRC3_PIN)
    self_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             SELF_REL)
    self_text = open(self_path, 'rb').read().decode('utf-8')
    b1 = cut_k1264(src1)
    b2 = cut_markers(src2)
    b3 = cut_markers(src3)
    bs = cut_markers(self_text)
    for name, b in (('k1264', b1), ('unified', b2), ('k1271', b3),
                    ('self', bs)):
        print(name, 'engine block bytes:', len(b.encode()),
              'sha256:', hashlib.sha256(b.encode()).hexdigest()[:16] + '...')
    four_way = (b1 == b2 == b3 == bs)
    engine_sha = hashlib.sha256(b1.encode()).hexdigest()
    pin_ok = (engine_sha == ENGINE_PIN)
    print('engine pin match:', pin_ok)
    print('four-way byte-identical:', four_way)
    if not (four_way and pin_ok):
        sys.exit(1)
    print('PROVENANCE PASS')
    sys.exit(0)


if __name__ == '__main__':
    main()
