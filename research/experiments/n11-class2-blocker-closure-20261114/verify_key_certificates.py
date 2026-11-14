#!/usr/bin/env python3
"""Replay the two decisive cost-68 strategies with the Python verifier."""
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
EXP=HERE.parent
sys.path.insert(0,str(EXP/'n11-central-19-cover-20261031'))
import verify_five_terminal_loss7 as verifier


def main():
    base=EXP/'n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost68-certificates'
    roots=('00000000000000801a02000080000001','00000000000000801a02040080000000')
    records=[]
    for root in roots:
        raw=(base/f'n11_s7_{root}.cert').read_bytes()
        strategy=verifier.parse(raw,root,header='n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS')
        stats=verifier.verify(int(root,16),strategy,winner_parity=1)
        records.append({'root':root,'sha256':hashlib.sha256(raw).hexdigest(),'verifier_stats':stats})
    print(json.dumps({'certificates':records,'scope':'two cost-68 WIN7 strategies; other receipts not replayed'},indent=2))


if __name__=='__main__':
    main()
