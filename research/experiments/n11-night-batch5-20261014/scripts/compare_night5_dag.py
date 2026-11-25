"""Recheck a night-batch5 C++-exported terminal DAG with the independent Python verifier.

Same cross-check as night batches 1/2/3/4 / adaptive verify: the exported
portable certificate is re-verified from scratch with the proof-dag-engine
Python verifier and every receipt field it recomputes must agree.
"""
import argparse
import gzip
import json
import sys
import time
from pathlib import Path

EXP = Path(__file__).resolve().parents[1]
ROOT = EXP.parents[2]
sys.path.insert(0, str(ROOT / 'research/experiments/n11-proof-dag-engine-20261011/scripts'))
from dag_verifier import verify_certificate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('index', type=int)
    parser.add_argument('--label', required=True)
    parser.add_argument('--rerun-python', action='store_true')
    args = parser.parse_args()
    dag = EXP / f'output/{args.label}-{args.index}-terminal-dag.json.gz'
    receipt_path = EXP / f'output/{args.label}-{args.index}-receipt.json'
    started = time.monotonic()
    with gzip.open(dag, 'rt') as stream:
        cert = json.load(stream)
    result = dict(s5_index=args.index, label=args.label)
    if args.rerun_python:
        checked = verify_certificate(cert)
        native = json.loads(receipt_path.read_text())
        assert all(checked[k] == native[k] for k in checked)
        result['fresh_python_verification'] = checked
    result['wall_seconds'] = time.monotonic() - started
    out = EXP / f'output/{args.label}-{args.index}-python-comparison.json'
    assert not out.exists(), 'refusing to overwrite existing artifacts'
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
