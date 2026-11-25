#!/usr/bin/env python3
"""Verify a local DRAT proof with the incremental checker and a negative control."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    folder = parser.parse_args().directory
    checker = Path(__file__).resolve().parent.parent / 'parabola-p2207-no-equality-witness-20261107/drat_check_incremental.cpp'
    cnf = gzip.decompress((folder / 'input.cnf.gz').read_bytes())
    proof = gzip.decompress((folder / 'local-proof.drat.gz').read_bytes())
    metadata = json.loads((folder / 'proof-generation.json').read_text())
    assert digest(cnf) == metadata['cnf_sha256'] and digest(proof) == metadata['proof_sha256']
    with tempfile.TemporaryDirectory(prefix='q2647-incremental-') as tmp:
        root = Path(tmp)
        (root / 'input.cnf').write_bytes(cnf)
        (root / 'proof.drat').write_bytes(proof)
        (root / 'truncated.drat').write_bytes(b'\n'.join(proof.splitlines()[:100]) + b'\n')
        binary = root / 'checker'
        subprocess.run(['c++', '-O2', '-std=c++17', str(checker), '-o', str(binary)], check=True)
        result = subprocess.run([str(binary), str(root / 'input.cnf'), str(root / 'proof.drat')], capture_output=True, text=True, timeout=1200)
        assert result.returncode == 0 and result.stdout.strip().splitlines()[-1] == 'VERIFIED'
        control = subprocess.run([str(binary), str(root / 'input.cnf'), str(root / 'truncated.drat')], capture_output=True, text=True, timeout=60)
        assert control.returncode != 0 and 'VERIFIED' not in control.stdout
        receipt = {'cnf_sha256': digest(cnf), 'proof_sha256': digest(proof),
                   'checker_source_sha256': digest(checker.read_bytes()),
                   'checker_returncode': result.returncode, 'checker_stdout': result.stdout.strip(),
                   'truncated_proof_returncode': control.returncode,
                   'scope': 'fixed-pair bounded-deletion CNF, not a global upper bound'}
    (folder / 'incremental-check.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
