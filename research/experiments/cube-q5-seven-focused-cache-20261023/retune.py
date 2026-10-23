#!/usr/bin/env python3
"""Change only the advisory prior and positive unknown PN/DN estimates."""
from pathlib import Path
import hashlib
import json
import struct
import sys


def retune(source, destination, prior):
    source, destination = Path(source), Path(destination)
    prior = int(prior)
    assert 1 <= prior <= 1000 and not destination.exists()
    infinity = 1 << 124
    with source.open('rb') as inp, destination.open('xb') as out:
        magic = inp.read(8);assert magic == b'Q5HYB2\n\0'
        header = list(struct.unpack('<9Q', inp.read(72)))
        side, old_prior = header[0], header[4]
        assert 3 <= side <= 7 and 1 <= old_prior <= 1000
        old_header = header.copy();header[4] = prior
        out.write(magic);out.write(struct.pack('<9Q', *header))
        left = 104*header[7];digest = hashlib.sha256()
        while left:
            chunk = inp.read(min(left, 1024*1024));assert chunk
            digest.update(chunk);out.write(chunk);left -= len(chunk)
        for _ in range(header[8]):
            raw = inp.read(136);assert len(raw) == 136
            row = list(struct.unpack('<17Q', raw))
            assert 0 < row[12]+(row[13] << 64) < infinity
            assert 0 < row[14]+(row[15] << 64) < infinity
            stones = sum(word.bit_count() for word in row[:6]);cost = 1
            for _ in range(stones, 17 if side == 7 else 9):
                if cost >= (infinity//2)//prior:
                    cost = infinity//2;break
                cost *= prior
            row[12:16] = [cost & ((1 << 64)-1), cost >> 64]*2
            out.write(struct.pack('<17Q', *row))
        trailer = inp.read(8)
        assert trailer == b'Q5END1\n\0' and not inp.read(1)
        out.write(trailer)
    with destination.open('rb') as stream:
        stream.seek(80);remaining = 104*header[7];check = hashlib.sha256()
        while remaining:
            chunk = stream.read(min(remaining, 1024*1024));assert chunk
            check.update(chunk);remaining -= len(chunk)
    assert digest.digest() == check.digest()
    result = {'source': str(source), 'destination': str(destination), 'old_prior': old_prior,
              'new_prior': prior, 'exact_rows_unchanged': header[7],
              'unknown_rows_reseeded': header[8], 'cumulative_nodes_unchanged': header[6],
              'exact_payload_sha256': digest.hexdigest(), 'old_header': old_header,
              'only_positive_advisory_estimates_changed': True}
    for label, path in [('source', source), ('destination', destination)]:
        with path.open('rb') as stream:result[label+'_sha256'] = hashlib.file_digest(stream, 'sha256').hexdigest()
    return result


if __name__ == '__main__':
    print(json.dumps(retune(*sys.argv[1:4]), indent=2))
