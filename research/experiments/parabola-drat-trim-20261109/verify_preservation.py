"""Round-trip the local gzip and compare both hashes to the accepted proof."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import time


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    manifest = json.loads(args.manifest.read_text())
    proof = Path(manifest['local_gzip'])
    receipt = json.loads(Path(manifest['receipt_path']).read_text())
    assert hashlib.sha256(Path(manifest['receipt_path']).read_bytes()).hexdigest() == manifest['receipt_sha256']
    assert receipt['verified'] and receipt['returncode'] == 0
    start = time.monotonic()
    compressed = hashlib.sha256()
    with proof.open('rb') as stream:
        for block in iter(lambda: stream.read(8*1024*1024), b''):
            compressed.update(block)
    assert proof.stat().st_size == manifest['compressed_bytes']
    assert compressed.hexdigest() == manifest['compressed_sha256']
    raw, size, lines = hashlib.sha256(), 0, 0
    with gzip.open(proof, 'rb') as stream:
        for block in iter(lambda: stream.read(8*1024*1024), b''):
            raw.update(block)
            size += len(block)
            lines += block.count(b'\n')
    assert raw.hexdigest() == manifest['proof_raw_sha256'] == receipt['proof_raw_sha256']
    assert size == manifest['proof_raw_bytes'] == receipt['proof_raw_bytes']
    assert lines == manifest['proof_lines'] == receipt['proof_lines']
    result = dict(roundtrip_verified=True, compressed_sha256=compressed.hexdigest(),
                  raw_sha256=raw.hexdigest(), raw_bytes=size, raw_lines=lines,
                  seconds=time.monotonic()-start,
                  scope='Byte preservation and gzip CRC/hash checks, not a new LRAT proof replay.')
    with args.output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
