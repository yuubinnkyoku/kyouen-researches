#!/usr/bin/env python3
"""Keep unknown nodes containing a symmetry image of a selected root.

Exact rows and counters are unchanged. Every child of a retained unknown node
also contains such an image, so this removes only unreachable search work.
The source snapshot is retained and destination must be a new file.
"""
from pathlib import Path
import hashlib
import itertools
import json
import mmap
import struct
import sys


def focus(source, destination, roots):
    source, destination, roots = map(Path, (source, destination, roots))
    assert source.resolve() != destination.resolve() and not destination.exists()
    with source.open('rb') as stream, mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ) as data:
        assert data[:8] == b'Q5HYB2\n\0'
        header = list(struct.unpack_from('<9Q', data, 8))
        side = header[0]
        assert 3 <= side <= 7
        images = set()
        selected = []
        for line in roots.read_text().splitlines():
            if not line.strip():
                continue
            points = list(map(int, line.split()))
            assert points and len(set(points)) == len(points) and all(0 <= p < side**3 for p in points)
            selected.append(points)
            for perm in itertools.permutations(range(3)):
                for flips in itertools.product((False, True), repeat=3):
                    image = 0
                    for point in points:
                        coords = (point//side**2, point//side % side, point % side)
                        mapped = [side-1-coords[perm[i]] if flips[i] else coords[perm[i]] for i in range(3)]
                        image |= 1 << ((mapped[0]*side+mapped[1])*side+mapped[2])
                    images.add(image)
        assert selected
        exact_end = 80+104*header[7]
        assert len(data) == exact_end+136*header[8]+8 and data[-8:] == b'Q5END1\n\0'
        kept = 0
        with destination.open('xb') as output:
            for start in range(0, exact_end, 1024*1024):
                output.write(data[start:min(start+1024*1024, exact_end)])
            for offset in range(exact_end, len(data)-8, 136):
                key = int.from_bytes(data[offset:offset+48], 'little')
                if any(key & image == image for image in images):
                    output.write(data[offset:offset+136])
                    kept += 1
            output.write(b'Q5END1\n\0')
            updated = header.copy();updated[8] = kept
            output.seek(8);output.write(struct.pack('<9Q', *updated))
        result = {
            'source': str(source), 'destination': str(destination), 'roots': selected,
            'root_images': len(images), 'exact_rows_preserved': header[7],
            'cumulative_nodes_preserved': header[6], 'unknown_before': header[8],
            'unknown_after': kept, 'only_unreachable_unknown_work_removed': True,
        }
    for label, path in [('source', source), ('destination', destination)]:
        with path.open('rb') as stream:
            result[label+'_sha256'] = hashlib.file_digest(stream, 'sha256').hexdigest()
    return result


if __name__ == '__main__':
    print(json.dumps(focus(*sys.argv[1:4]), indent=2))
