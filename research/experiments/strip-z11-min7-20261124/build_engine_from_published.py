#!/usr/bin/env python3
"""build_engine_from_published.py -- provenance gate for the engine block
embedded in verify_strip_z11.py.

The engine + closed-form block (mex / H_ordered / H_canonical / vC / vO /
q_odd / single_token, 2,508 bytes) is machine-compared (zero hand
transcription) against TEN published verifiers:
  src1: research/experiments/generalx-min-token-lowr-staircase-20261123/
        verify_min_token_staircase.py          (published K1264 verifier)
  src2: research/experiments/generalx-unified-window-sharpness-20261123/
        verify_unified_window_sharpness.py    (published K1268 machine)
  src3: research/experiments/ones-row-windowedge-frontier-20261123/
        verify_ones_row_frontier.py           (published K1271 machine)
  src4: research/experiments/min3-banded-strip-z2z4-20261123/
        verify_min3_banded_strip.py           (published K1272 machine)
  src5: research/experiments/strip-z5-min4-20261123/
        verify_strip_z5.py                    (published K1273 machine)
  src6: research/experiments/strip-z6-min5-20261123/
        verify_strip_z6.py                    (published K1274 machine)
  src7: research/experiments/strip-z7-min5-20261123/
        verify_strip_z7.py                   (published K1275 machine)
  src8: research/experiments/strip-z8-min5-20261124/
        verify_strip_z8.py                    (published K1276 machine)
  src9: research/experiments/strip-z9-min6-20261124/
        verify_strip_z9.py                    (published K1277 machine)
  src10: research/experiments/strip-z10-min7-20261124/
        verify_strip_z10.py                   (published K1279 machine)
Cuts: src1 between the lines 'def mex(values):' and the first line starting
with 'SELF_SHA = hashlib' (trailing blank lines stripped); src2..src10 and
this machine between their '# === ENGINE BLOCK' and
'# === END ENGINE BLOCK' markers (trailing blank lines stripped).
Exit 0 iff the ten source sha256 pins match, all eleven blocks are
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
SRC4_REL = os.path.join('..', 'min3-banded-strip-z2z4-20261123',
                        'verify_min3_banded_strip.py')
SRC4_PIN = '009184eff1accbaa82cdea9eea5e81253252e6d3681e893b1fd30506d6acad9c'
SRC5_REL = os.path.join('..', 'strip-z5-min4-20261123', 'verify_strip_z5.py')
SRC5_PIN = ('314e176b4229486ff60672b63095397daa786fb1e4affe90ac20b5c060b72'
            '4f4')
SRC6_REL = os.path.join('..', 'strip-z6-min5-20261123', 'verify_strip_z6.py')
SRC6_PIN = ('61cb0b60b9012320e2146f4b49566a3b6fc5cee4cfb42c8911db9dc5321'
            'cb134')
SRC7_REL = os.path.join('..', 'strip-z7-min5-20261123', 'verify_strip_z7.py')
SRC7_PIN = ('0c400f32e78b7a8848a6bdaa40a2f29ff73fe1b0f667abb187b961508f53a'
            '1c9')
SRC8_REL = os.path.join('..', 'strip-z8-min5-20261124', 'verify_strip_z8.py')
SRC8_PIN = ('cdc472198c905233215b2c717986b77c5194b0588cdfa2f50e37376f3e5ed3a'
            'd')
SRC9_REL = os.path.join('..', 'strip-z9-min6-20261124', 'verify_strip_z9.py')
SRC9_PIN = ('bf3c0c1c1b38a32bbcb7cf83129d4c5842a39aa99587cb342301ee66adab5cd'
            '2')
ENGINE_PIN = ('bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb1'
              '2e3a92')
SRC10_REL = os.path.join('..', 'strip-z10-min7-20261124',
                        'verify_strip_z10.py')
SRC10_PIN = ('8f29faf7263943f983e5589f16259d02c8c1d7761bea97d13676bed6d30ea'
            '768')
SELF_REL = 'verify_strip_z11.py'


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
    src4 = load_pinned(SRC4_REL, SRC4_PIN)
    src5 = load_pinned(SRC5_REL, SRC5_PIN)
    src6 = load_pinned(SRC6_REL, SRC6_PIN)
    src7 = load_pinned(SRC7_REL, SRC7_PIN)
    src8 = load_pinned(SRC8_REL, SRC8_PIN)
    src9 = load_pinned(SRC9_REL, SRC9_PIN)
    src10 = load_pinned(SRC10_REL, SRC10_PIN)
    self_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             SELF_REL)
    self_text = open(self_path, 'rb').read().decode('utf-8')
    blocks = [cut_k1264(src1), cut_markers(src2), cut_markers(src3),
              cut_markers(src4), cut_markers(src5), cut_markers(src6),
              cut_markers(src7), cut_markers(src8), cut_markers(src9),
              cut_markers(src10),
              cut_markers(self_text)]
    shas = [hashlib.sha256(b.encode('utf-8')).hexdigest() for b in blocks]
    if len(set(shas)) != 1:
        print('blocks differ:', shas)
        sys.exit(1)
    if shas[0] != ENGINE_PIN:
        print('engine pin mismatch:', shas[0])
        sys.exit(1)
    print('ten published sources + this machine: eleven-way byte-identical')
    print('engine block sha256:', shas[0])
    print('engine block bytes:', len(blocks[0].encode('utf-8')))
    print('PROVENANCE PASS')


if __name__ == '__main__':
    main()
