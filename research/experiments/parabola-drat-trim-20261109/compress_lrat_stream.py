"""Preserve a verified raw LRAT in bounded-memory level-1 gzip, with manifest."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import time


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--proof', type=Path, required=True)
    ap.add_argument('--receipt', type=Path, required=True)
    ap.add_argument('--gzip', type=Path, required=True)
    ap.add_argument('--manifest', type=Path, required=True)
    args = ap.parse_args()
    if args.gzip.exists() or args.manifest.exists():
        raise FileExistsError('fresh output paths required')
    receipt = json.loads(args.receipt.read_text())
    assert receipt['verified'] is True and receipt['returncode'] == 0
    assert 'c VERIFIED' in receipt['stdout'].splitlines()
    digest, size, lines = hashlib.sha256(), 0, 0
    start = time.monotonic()
    with args.proof.open('rb') as src, args.gzip.open('xb') as destination:
        with gzip.GzipFile(filename='', fileobj=destination, mode='wb', compresslevel=1, mtime=0) as dst:
            for block in iter(lambda: src.read(8*1024*1024), b''):
                digest.update(block)
                size += len(block)
                lines += block.count(b'\n')
                dst.write(block)
    assert digest.hexdigest() == receipt['proof_raw_sha256']
    assert size == receipt['proof_raw_bytes'] and lines == receipt['proof_lines']
    compressed_digest = hashlib.sha256()
    with args.gzip.open('rb') as stream:
        for block in iter(lambda: stream.read(8*1024*1024), b''):
            compressed_digest.update(block)
    manifest = dict(local_raw_pin=str(args.proof.resolve()), local_gzip=args.gzip.as_posix(),
                    proof_raw_sha256=digest.hexdigest(), proof_raw_bytes=size, proof_lines=lines,
                    compressed_sha256=compressed_digest.hexdigest(), compressed_bytes=args.gzip.stat().st_size,
                    compresslevel=1, seconds=time.monotonic()-start,
                    receipt_path=args.receipt.as_posix(), receipt_sha256=hashlib.sha256(args.receipt.read_bytes()).hexdigest(),
                    availability='Raw pin and gzip are local evidence, not distributed in Git. Restore either exact file to replay.',
                    scope='Streamed provenance and preservation of an independently accepted LRAT; not a new proof replay.')
    with args.manifest.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(manifest, stream, indent=2)
        stream.write('\n')
    print(json.dumps(manifest, indent=2), flush=True)


if __name__ == '__main__':
    main()
