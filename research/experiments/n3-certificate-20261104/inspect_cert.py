#!/usr/bin/env python3
"""Decode the KYOENC3 3x3 empty-board certificate and check its header.

Usage: python3 inspect_cert.py kyouen-3x3.cert
"""
import struct
import sys

def main():
    data = open(sys.argv[1], 'rb').read()
    magic = data[:8]
    assert magic.rstrip(b'\x00') == b'KYOENC3', magic
    version, boardSize, nodeCount, rootLo, rootHi, forbiddenCount = struct.unpack_from('<IIQQII', data, 8)
    assert version == 3, version
    assert boardSize == 3, boardSize
    nodeCount = int(nodeCount)
    offset = 40
    print(f'magic          {magic.rstrip(bytes([0]))!r}')
    print(f'version        {version}')
    print(f'boardSize      {boardSize}')
    print(f'nodeCount      {nodeCount}')
    print(f'rootLo         {rootLo:#x}')
    print(f'rootHi         {rootHi}')
    print(f'forbiddenCount {forbiddenCount}')
    print('nodes:')
    for i in range(int(nodeCount)):
        lo, hi, outcome, witness, rank, reserved = struct.unpack_from('<QIBBBB', data, offset)
        offset += 16
        mask = lo | (hi << 64)
        pts = [p for p in range(mask.bit_length()) if (mask >> p) & 1]
        wname = {1: 'losing', 2: 'winning'}[outcome]
        print(f'  mask={mask:#05x} points={pts} outcome={wname} witness={witness if witness != 255 else None} rank={rank}')
    assert offset == len(data)

if __name__ == '__main__':
    main()
