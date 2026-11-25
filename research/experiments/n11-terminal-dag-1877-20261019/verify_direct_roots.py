#!/usr/bin/env python3
"""Independent direct-board minimax audit of all 377 optimized proof roots."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'n11-s11-quotient-optimality-20261019'/'n11-s11-dual-branch-optimality-20261019'))
import compact_proof184_342 as v

def main():
    dag=json.loads((HERE/'joint_dag_optimized_final.json').read_text())
    cover=json.loads((HERE/'joint_cover_optimized_final.json').read_text())
    assert len(dag['roots'])==184+len(cover['representatives'])==377
    total=0
    for p,_,_ in dag['roots']:
        win,states=v.next_player_wins_at_s10(int(p,16))
        assert not win,('root not LOSS',p)
        total+=states
    assert total==21483,('independent memoized-state total changed',total)
    print('PASS: 377/377 root positions LOSS by direct-board terminal minimax; 21,483 additive memo states')
    print('Standard 11x11 empty-board outcome: UNKNOWN')
if __name__=='__main__':main()
