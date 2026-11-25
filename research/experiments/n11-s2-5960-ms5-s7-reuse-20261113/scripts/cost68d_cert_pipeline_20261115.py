#!/usr/bin/env python3
"""cost-68d WIN7 certificate extraction pipeline (class2-lane long-term lane, 2026-11-15).

Reuses the repo-verbatim warm rebuild pipeline process() (blind extraction,
FBS=1<<20, fbt_drops==0, BigInt independent verification) for the 7 WIN7-D10
roots of the cost-68d sweep (S6 child 00000000000000809122000000000000 of the
third class-2 target S5 00000000000000809102000000000000).

Usage: cost68d_cert_pipeline_20261115.py <targets.json> <out_records.json>
  targets.json: list of [band, child_hex, bit, root_hex]
"""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    'warmpipe', HERE / 'warm_rebuild_pipeline_20261115.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

targets = json.loads(Path(sys.argv[1]).read_text())
records = []
for band, child, bit, root in targets:
    print(f'processing {band} bit-{bit} root {root} ...', flush=True)
    entry = mod.process(band, child, bit, root)
    records.append(entry)
    print(f"  OK rows={entry['rows']} nodes={entry['extraction_nodes']} "
          f"mobility={entry['root_check']['loser_mobility']} md5={entry['md5']}",
          flush=True)
Path(sys.argv[2]).write_text(json.dumps(records, indent=1) + '\n')
print(f'written {sys.argv[2]} with {len(records)} entries')
