#!/usr/bin/env python3
"""Losslessly archive explicitly listed historical private caches, with hashes."""
from pathlib import Path
import gzip
import hashlib
import json
import sys


def main():
    inventory = Path(sys.argv[1])
    records = json.loads(inventory.read_text()) if inventory.exists() else {}
    for name in sys.argv[2:]:
        source = Path(name)
        if not source.exists():
            assert name in records and Path(records[name]['gzip_path']).is_file()
            continue
        assert source.is_file() and not source.is_symlink() and source.suffix in {'.memo', '.hyb'}
        target = source.with_suffix(source.suffix+'.gz')
        assert not target.exists(), 'refusing to overwrite an archive'
        raw_hash = hashlib.sha256(); size = 0
        with source.open('rb') as inp, (Path(str(target)+'.new')).open('wb') as output:
            with gzip.GzipFile(fileobj=output, mode='wb', compresslevel=1, filename='', mtime=0) as zipped:
                while chunk := inp.read(1024*1024):
                    raw_hash.update(chunk);size += len(chunk);zipped.write(chunk)
        Path(str(target)+'.new').replace(target)
        restored_hash = hashlib.sha256(); restored_size = 0
        with gzip.open(target, 'rb') as restored:
            while chunk := restored.read(1024*1024):
                restored_hash.update(chunk);restored_size += len(chunk)
        assert restored_hash.digest() == raw_hash.digest() and restored_size == size
        with target.open('rb') as file: compressed_hash = hashlib.file_digest(file, 'sha256').hexdigest()
        records[name] = {'gzip_path': str(target), 'raw_sha256': raw_hash.hexdigest(),
                         'raw_bytes': size, 'gzip_sha256': compressed_hash,
                         'gzip_bytes': target.stat().st_size, 'round_trip_verified': True}
        tmp = inventory.with_suffix('.new');tmp.write_text(json.dumps(records, indent=2)+'\n');tmp.replace(inventory)
        source.unlink()
        print(json.dumps({'archived': name, 'bytes_reclaimed': size-target.stat().st_size}), flush=True)


if __name__ == '__main__':
    main()
