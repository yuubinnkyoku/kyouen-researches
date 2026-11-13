#!/usr/bin/env python3
"""Verify every LOSS7 certificate for the next class-2 S6 candidate."""
import gzip
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE.parent/'n11-central-19-cover-20261031'))
import verify_five_terminal_loss7 as verifier


def main():
    paths=sorted((HERE/'output/class2-next-loss-certificates').glob('*-loss7.cert.gz'))
    assert len(paths)==72
    records=[]
    for index,path in enumerate(paths,1):
        root=path.name.split('-',1)[0]
        raw=gzip.decompress(path.read_bytes())
        strategy=verifier.parse(raw,root,header='n11-terminal-strategy-v1 original_first_LOSS7 second_to_move_WIN')
        stats=verifier.verify(int(root,16),strategy,winner_parity=0)
        records.append({'root':root,'verdict':'LOSS7','certificate_sha256':hashlib.sha256(raw).hexdigest(),
                        'compressed_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'verifier_stats':stats})
        if index%10==0:
            print(f'verified {index}/{len(paths)}',file=sys.stderr,flush=True)
    print(json.dumps({'certificates':records,'scope':'terminal strategies for listed S7 roots; S6 coverage checked separately'},indent=2))


if __name__ == '__main__':
    main()
