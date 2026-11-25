#!/usr/bin/env python3
"""Reassemble the canonical combined official records file from output/shards/.

The canonical file byte format (matching emit_records of solve_core.py) is:
  head pretty-printed with json.dumps(head, indent=2) with the final '}' opened
  and the compact one-line records appended, ending with ']\\n}\\n'.
Shard files are fully compact JSON:
  {"shard":i,"of":N,"head":{...},"records_count":k,"records":[...]}.
Records concatenate to the canonical records array in shard order.
Usage: python3 combine_records.py [dest.json]
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'output'


def main():
    shards_dir = OUT / 'shards'
    parts = sorted(shards_dir.glob('part*.json'))
    assert parts, 'no shards found'
    heads = []
    records = []
    for i, path in enumerate(parts):
        shard = json.loads(path.read_text(encoding='utf-8'))
        assert shard['shard'] == i, (i, shard['shard'])
        assert shard['of'] == len(parts)
        assert shard['records_count'] == len(shard['records'])
        heads.append(shard['head'])
        records.extend(shard['records'])
    head = heads[0]
    assert all(h == head for h in heads), 'shard heads differ'
    text = json.dumps(head, indent=2)
    text = text[:-2] + ',\n  "records": [\n' + ',\n'.join(
        '    ' + json.dumps(row, separators=(',', ':')) for row in records) + '\n  ]\n}\n'
    json.loads(text)
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else OUT / 'official_records.json'
    dest.write_text(text, encoding='utf-8')
    print('recombined %d records -> %s (%d bytes)' % (len(records), dest, len(text.encode('utf-8'))))


if __name__ == '__main__':
    main()
