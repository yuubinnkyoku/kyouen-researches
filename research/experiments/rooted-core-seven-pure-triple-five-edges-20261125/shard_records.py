#!/usr/bin/env python3
"""Shard the canonical combined official records file into balanced parts.

The canonical file byte format (matching emit_records of solve_core.py) is:
  head pretty-printed with json.dumps(head, indent=2) with the final '}' opened
  for the compact one-line records array.
Usage: python3 shard_records.py [canonical.json]
Writes output/shards/partNN.json: {"shard":i,"of":N,"head":{...},
"records_count":k,"records":[...]} fully compact, records split at record
boundaries with balanced byte sizes, in canonical record order.
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'output'
NSHARDS = 6


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else OUT / 'official_records_run1.json'
    data = json.loads(src.read_text(encoding='utf-8'))
    records = data['records']
    head = {k: v for k, v in data.items() if k != 'records'}
    sizes = [len(json.dumps(r, separators=(',', ':'))) for r in records]
    per_shard = sum(sizes) / NSHARDS
    cum = 0
    bounds = []
    for i, s in enumerate(sizes):
        cum += s
        if len(bounds) < NSHARDS - 1 and cum >= per_shard * (len(bounds) + 1):
            bounds.append(i + 1)
    bounds = [0] + bounds + [len(records)]
    shards_dir = OUT / 'shards'
    shards_dir.mkdir(parents=True, exist_ok=True)
    for si in range(NSHARDS):
        lo, hi = bounds[si], bounds[si + 1]
        shard = dict(shard=si, of=NSHARDS, head=head, records_count=hi - lo,
                     records=records[lo:hi])
        text = json.dumps(shard, separators=(',', ':')) + '\n'
        (shards_dir / ('part%02d.json' % si)).write_text(text, encoding='utf-8')
        print('shard %02d: %d records, %d bytes' % (si, hi - lo,
              os.path.getsize(shards_dir / ('part%02d.json' % si))))


if __name__ == '__main__':
    main()
