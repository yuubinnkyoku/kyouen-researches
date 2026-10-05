#!/usr/bin/env python3
"""Size skeleton for a stateless QBF encoding of normal-play Kyouen.

A safe position has at most three stones in each row, since four collinear
points are forbidden. Therefore every n x n game ends within d=3n moves.

For a fixed move sequence m_1,...,m_d, prefix legality is stateless:
  * m_t is an in-board point,
  * m_t differs from all earlier moves,
  * every four selected moves have nonzero circle/line determinant.

The game value can be encoded recursively with alternating move quantifiers:
  existential turn: exists a legal move continuing a win;
  universal turn:  every legal opponent move must continue a win.
If the universal player has no legal move, the guarded universal formula is
vacuously true; if the existential player has no legal move, it is false.
Thus early terminals need no ad-hoc winner rule.

This script only counts the structural predicates. It does not emit a concrete
bit-blasted determinant circuit/QCIR.
"""
from __future__ import annotations
import argparse, json
from math import comb
from pathlib import Path

def row(n):
    d=3*n
    coord_bits=(n-1).bit_length()
    return {
        "n":n,
        "sound_full_game_depth_bound":d,
        "quantifier_blocks":d,
        "coordinate_bits_per_move":2*coord_bits,
        "quantified_move_bits":d*2*coord_bits,
        "pairwise_distinctness_predicates":comb(d,2),
        "four_move_determinant_predicates":comb(d,4),
        "minimum_known_required_depth_lower_bound":21 if n==11 else None,
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",type=Path); args=ap.parse_args()
    out={
      "scope":"stateless full-game QBF skeleton for standard Kyouen",
      "n11_empty_root_outcome":"UNKNOWN",
      "rows":[row(n) for n in range(4,12)],
      "limitations":[
        "Counts treat one determinant test as one high-level predicate; bit-blasting it requires many Boolean gates.",
        "The QBF paper benchmarks maker-breaker games, while Kyouen is a normal-play impartial avoidance game; the guarded recursion is a new adaptation.",
        "No generic QBF solver benchmark is claimed here."
      ]
    }
    text=json.dumps(out,ensure_ascii=False,indent=2)+"\n"
    if args.out:
      args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(text,encoding="utf-8")
    else: print(text,end="")

if __name__=="__main__": main()
