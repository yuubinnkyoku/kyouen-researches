#!/usr/bin/env python3
"""Check immutable inputs and UNKNOWN receipts for the d=1323, target=1322 slice."""
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent / 'parabola-ternary-selection-20261109'
NAMES = ['target1322-d1323-20261109', 'target1322-d1323-1m-20261109']
EXPECTED = '8cbd404a7e01bcc3ea0d32fe770d105c38b6c8ee241c018cf8a070a0dcb9f48a'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    for name, budget in zip(NAMES, (100000, 1000000)):
        path = EXP / 'output' / name
        init = json.loads((path/'init.json').read_text())
        result = json.loads((path/'result.json').read_text())
        run = json.loads((path/'run.json').read_text())
        assert all(result[k] == v for k, v in init.items())
        assert (result['p'], result['d'], result['target'], result['empty_bound']) == (2647, 1323, 1322, 3)
        assert result['conflict_budget'] == budget
        assert result['status'] == 'UNKNOWN' and result['statistics']['conflicts'] >= budget
        assert run['status'] == 'FINISHED' and run['returncode'] == 0 and run['result_exists']
        raw = gzip.decompress((path/'input.cnf.gz').read_bytes())
        assert sha(raw) == EXPECTED == result['encoded_cnf_sha256']
        assert result['worker_source_sha256'] == sha((EXP/'ternary.py').read_bytes())
        assert raw.splitlines()[0] == b'p cnf 7926 68404'
        assert len(raw.splitlines()) == 68405
        print(f'PASS: budget={budget}, UNKNOWN, input_sha256={EXPECTED}')


if __name__ == '__main__':
    main()
