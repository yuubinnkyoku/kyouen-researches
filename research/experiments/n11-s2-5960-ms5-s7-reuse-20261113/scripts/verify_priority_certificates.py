#!/usr/bin/env python3
"""Recheck locally stored terminal strategies with the independent verifier."""
import gzip
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE.parent/'n11-central-19-cover-20261031'))
import verify_five_terminal_loss7 as verifier


def main():
    entries = []
    paths = sorted((HERE/'output/priority-certificates').glob('*.cert.gz'))
    assert len(paths) == 15
    for path in paths:
        root, verdict = path.name.split('-',1)
        assert verdict in ('win7.cert.gz','loss7.cert.gz')
        win = verdict.startswith('win7')
        header = 'n11-terminal-strategy-v1 original_first_'+('WIN7 second_to_move_LOSS' if win else 'LOSS7 second_to_move_WIN')
        raw = gzip.decompress(path.read_bytes())
        strategy = verifier.parse(raw,root,header=header)
        stats = verifier.verify(int(root,16),strategy,winner_parity=int(win))
        entries.append({'root':root,'verdict':'WIN7' if win else 'LOSS7',
                        'certificate_sha256':hashlib.sha256(raw).hexdigest(),
                        'compressed_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                        'verifier_stats':stats})
    print(json.dumps({'certificates':entries,'scope':'terminal strategies for listed S7 roots; no root-board verdict'},indent=2))


if __name__ == '__main__':
    main()
