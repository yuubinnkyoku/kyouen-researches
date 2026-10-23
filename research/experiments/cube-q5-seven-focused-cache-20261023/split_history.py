#!/usr/bin/env python3
"""Keep immutable exact rows raw, and losslessly archive old unknown-tree tails."""
from pathlib import Path
import fcntl
import gzip
import hashlib
import json
import struct
import sys

END = b'Q5END1\n\0'


def write_json(path, value):
    temporary = path.with_name(path.name+'.new')
    temporary.write_text(json.dumps(value, indent=2)+'\n');temporary.replace(path)


def split_one(source, index):
    source, index = Path(source), Path(index)
    table = source.with_name(source.stem+'-table.hyb')
    tail = source.with_name(source.stem+'-unknown.gz')
    new_index = Path(str(table)+'.idx')
    assert all(not path.exists() for path in [table, tail, new_index])
    original_stat, index_stat = source.stat(), index.stat()
    with source.open('rb') as inp:
        original_header = inp.read(80)
        assert original_header[:8] == b'Q5HYB2\n\0'
        header = list(struct.unpack_from('<9Q', original_header, 8))
        payload_bytes, unknown_bytes = 104*header[7], 136*header[8]+8
        assert header[8] and original_stat.st_size == 80+payload_bytes+unknown_bytes
        updated = header.copy();updated[8] = 0
        digest = hashlib.sha256(original_header)
        with table.open('xb') as output:
            output.write(original_header[:8]);output.write(struct.pack('<9Q', *updated))
            left = payload_bytes
            while left:
                chunk = inp.read(min(left, 1024*1024));assert chunk
                digest.update(chunk);output.write(chunk);left -= len(chunk)
            output.write(END)
        with tail.open('xb') as output:
            with gzip.GzipFile(fileobj=output, mode='wb', filename='', mtime=0, compresslevel=1) as zipped:
                left = unknown_bytes;trailer = b''
                while left:
                    chunk = inp.read(min(left, 1024*1024));assert chunk
                    digest.update(chunk);zipped.write(chunk);left -= len(chunk);trailer = (trailer+chunk)[-8:]
                assert trailer == END and not inp.read(1)
    # Reconstruct every original byte before changing the state or removing data.
    reconstructed = hashlib.sha256(original_header)
    with table.open('rb') as inp:
        inp.seek(80);left = payload_bytes
        while left:
            chunk = inp.read(min(left, 1024*1024));assert chunk
            reconstructed.update(chunk);left -= len(chunk)
        assert inp.read() == END
    with gzip.open(tail, 'rb') as inp:
        while chunk := inp.read(1024*1024):reconstructed.update(chunk)
    assert digest.digest() == reconstructed.digest()
    with index.open('rb') as inp:
        index_header = inp.read(64)
        assert index_header[:8] in [b'Q5IDX2\n\0', b'Q5IDX3\n\0']
        fields = list(struct.unpack_from('<7Q', index_header, 8))
        assert fields[:3] == [header[0], header[6], header[7]] and fields[4] == original_stat.st_size
        fields[4] = table.stat().st_size
        index_digest = hashlib.sha256(index_header)
        with new_index.open('xb') as output:
            output.write(index_header[:8]);output.write(struct.pack('<7Q', *fields))
            while chunk := inp.read(1024*1024):index_digest.update(chunk);output.write(chunk)
    check = hashlib.sha256(index_header)
    with new_index.open('rb') as inp:
        inp.seek(64)
        while chunk := inp.read(1024*1024):check.update(chunk)
    assert check.digest() == index_digest.digest()
    assert (source.stat().st_ino, source.stat().st_mtime_ns) == (original_stat.st_ino, original_stat.st_mtime_ns)
    assert (index.stat().st_ino, index.stat().st_mtime_ns) == (index_stat.st_ino, index_stat.st_mtime_ns)
    return {'original': str(source), 'original_index': str(index), 'table': str(table),
            'tail': str(tail), 'index': str(new_index), 'original_header_hex': original_header.hex(),
            'original_index_header_hex': index_header.hex(), 'original_sha256': digest.hexdigest(),
            'original_index_sha256': index_digest.hexdigest(), 'exact_rows_unchanged': header[7],
            'unknown_rows_preserved': header[8], 'original_bytes': original_stat.st_size,
            'table_bytes': table.stat().st_size, 'tail_gzip_bytes': tail.stat().st_size,
            'bytes_reclaimed': original_stat.st_size-table.stat().st_size-tail.stat().st_size,
            'full_reconstruction_verified': True}


def compact(workspace, inventory_path):
    workspace, inventory_path = Path(workspace), Path(inventory_path)
    lock = (workspace/'.campaign.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    state_path = workspace/'run-state.json'
    state = json.loads(state_path.read_text())
    assert state['status'] in ['paused', 'blocked-storage', 'stage-budget-completed', 'stage-saved']
    records = json.loads(inventory_path.read_text()) if inventory_path.exists() else {}
    for i in range(len(state['bases'])):
        source, index = Path(state['bases'][i]), Path(state['indices'][i])
        # Leave the latest full tree available for the normal --promote path.
        if i == len(state['bases'])-1:continue
        with source.open('rb') as inp:header = inp.read(80)
        if header[:8] != b'Q5HYB2\n\0' or not struct.unpack_from('<Q', header, 72)[0]:continue
        result = split_one(source, index)
        records[str(source)] = result;write_json(inventory_path, records)
        state['bases'][i] = result['table'];state['indices'][i] = result['index']
        state['history_inventory'] = str(inventory_path);write_json(state_path, state)
        source.unlink();index.unlink()
    return records


if __name__ == '__main__':
    records = compact(*sys.argv[1:3])
    print(json.dumps({'layers': len(records),
                      'bytes_reclaimed': sum(row['bytes_reclaimed'] for row in records.values()),
                      'all_unknown_history_preserved': True}, indent=2))
