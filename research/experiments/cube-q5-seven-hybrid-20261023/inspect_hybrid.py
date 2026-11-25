#!/usr/bin/env python3
"""Inspect advisory PN/DN for shallow unknown nodes, without trusting labels."""
from pathlib import Path
import collections
import json
import mmap
import struct
import sys

with Path(sys.argv[1]).open('rb') as stream:
    data = mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ)
    assert data[:8] in [b'Q5HYB1\n\0', b'Q5HYB2\n\0']
    compact = data[:8] == b'Q5HYB2\n\0'
    header = struct.unpack_from('<9Q', data, 8)
    offset = 80+104*header[7]
    layers = collections.Counter()
    shallow = []
    for _ in range(header[8]):
        row = struct.unpack_from('<17Q', data, offset)
        stones = sum(x.bit_count() for x in row[:6]); layers[stones] += 1
        if stones <= 6:
            points = [i for i in range(header[0]**3) if row[i//64] >> (i%64) & 1]
            shallow.append({'root': points, 'live': sum(x.bit_count() for x in row[6:12]),
                            'advisory_pn': row[12]+(row[13]<<64),
                            'advisory_dn': row[14]+(row[15]<<64)})
        offset += 136+(0 if compact else 64*row[16])
    assert data[offset:offset+8] == b'Q5END1\n\0' and offset+8 == len(data)
    print(json.dumps({'base_rows': header[2], 'cumulative_nodes': header[6],
                      'delta_rows': header[7], 'unknown_rows': header[8],
                      'unknown_layers': dict(sorted(layers.items())),
                      'small_advisory_dn': sorted(shallow, key=lambda x: x['advisory_dn'])[:12],
                      'small_advisory_pn': sorted(shallow, key=lambda x: x['advisory_pn'])[:12],
                      'all_work_estimates_are_not_verdicts': True}, indent=2))
