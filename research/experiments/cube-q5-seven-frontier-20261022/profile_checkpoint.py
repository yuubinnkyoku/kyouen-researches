#!/usr/bin/env python3
"""Stream a little-endian exact checkpoint; summarize without trusting labels."""
from collections import Counter
from pathlib import Path
import json
import struct
import sys

path = Path(sys.argv[1])
hist = Counter()
best = {}
by_layer = {}
with path.open('rb') as stream:
    assert stream.read(8) == b'Q5MEMO2\n'
    side, nodes, count = struct.unpack('<3Q', stream.read(24))
    seen = 0
    while chunk := stream.read(104*10000):
        for row in struct.iter_unpack('<13Q', chunk):
            mask = sum(v << (64*j) for j, v in enumerate(row[:6]))
            label = row[6]
            stones = mask.bit_count()
            hist[stones, label] += 1
            key = stones, mask
            if label not in best or key < best[label]:
                best[label] = key
            layer = stones, label
            if layer not in by_layer or mask < by_layer[layer]:
                by_layer[layer] = mask
            seen += 1
    assert seen == count
print(json.dumps({'side': side, 'cumulative_expansions': nodes, 'rows': count,
                  'unverified_label_histogram': {str(k): {'P': hist[k, 0], 'N': hist[k, 1]}
                                               for k in sorted({k for k, _ in hist})},
                  'candidate_roots': {('P' if label == 0 else 'N'):
                                      [i for i in range(side**3) if (mask >> i) & 1]
                                      for label, (_, mask) in best.items()},
                  'candidates_by_layer': {str(stones)+('P' if label == 0 else 'N'):
                                          [i for i in range(side**3) if (mask >> i) & 1]
                                          for (stones,label),mask in sorted(by_layer.items())}}, indent=2))
