#!/usr/bin/env python3
"""Independently verify the class-2 terminal WIN7 strategy certificates."""
import gzip
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE.parent/'n11-central-19-cover-20261031'))
import verify_five_terminal_loss7 as verifier


def main():
    paths = sorted((HERE/'output/class2-certificates').glob('*-win7.cert.gz'))
    assert len(paths) == 14
    entries = []
    for path in paths:
        root = path.name.split('-',1)[0]
        raw = gzip.decompress(path.read_bytes())
        strategy = verifier.parse(raw,root,header='n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS')
        stats = verifier.verify(int(root,16),strategy,winner_parity=1)
        entries.append({'root':root,'verdict':'WIN7','certificate_sha256':hashlib.sha256(raw).hexdigest(),
                        'compressed_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'verifier_stats':stats})
    print(json.dumps({'certificates':entries,'scope':'terminal strategies for listed S7 roots; no root-board verdict'},indent=2))


if __name__ == '__main__':
    main()
