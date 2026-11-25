#!/usr/bin/env python3
"""Build focused bases from raw or gzip sources, restoring one source at a time."""
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import struct
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('side', type=int)
    parser.add_argument('roots', type=Path)
    parser.add_argument('prefix', type=Path)
    parser.add_argument('inputs', type=Path, nargs='+')
    parser.add_argument('--filter', type=Path, required=True)
    parser.add_argument('--inventory', type=Path)
    args = parser.parse_args()
    count = len([line for line in args.roots.read_text().splitlines() if line.strip()])
    targets = [Path(str(args.prefix)+f'-{i}.memo') for i in range(count)]
    assert count and all(not path.exists() for path in targets)
    inventory = json.loads(args.inventory.read_text()) if args.inventory else None
    args.prefix.parent.mkdir(parents=True, exist_ok=True)
    records = []
    with tempfile.TemporaryDirectory(dir=args.prefix.parent) as directory:
        work = Path(directory)
        previous = []
        for i, source in enumerate(args.inputs):
            actual = source
            if source.suffix == '.gz':
                actual = work/'restored.raw'
                digest = hashlib.sha256()
                with gzip.open(source, 'rb') as inp, actual.open('xb') as output:
                    while chunk := inp.read(1024*1024):
                        digest.update(chunk);output.write(chunk)
                if inventory is not None:
                    expected = inventory[str(source)[:-3]]
                    assert digest.hexdigest() == expected['raw_sha256']
                    assert actual.stat().st_size == expected['raw_bytes']
            with actual.open('rb') as stream:
                header = stream.read(80)
            if header[:8] == b'Q5MEMO2\n':
                source_rows = struct.unpack_from('<Q', header, 24)[0]
            else:
                assert header[:8] in [b'Q5HYB1\n\0', b'Q5HYB2\n\0']
                source_rows = struct.unpack_from('<Q', header, 64)[0]
            prefix = work/f'step-{i}'
            command = [str(args.filter), str(args.side), str(args.roots), str(prefix),
                       *map(str, previous), str(actual)]
            run = subprocess.run(command, text=True, capture_output=True, check=True)
            reports = [json.loads(line) for line in run.stdout.splitlines()]
            assert len(reports) == count
            for path in previous:
                assert path.parent == work;path.unlink()
            previous = [Path(report['output']) for report in reports]
            if actual != source:
                actual.unlink()
            records.append({'input': str(source), 'source_rows': source_rows,
                            'retained_rows': [report['rows'] for report in reports]})
        for source, target in zip(previous, targets):
            assert not target.exists();source.replace(target)
    print(json.dumps({'outputs': list(map(str, targets)), 'steps': records,
                      'original_source_rows': sum(row['source_rows'] for row in records),
                      'all_original_archives_retained': True}, indent=2))


if __name__ == '__main__':
    main()
