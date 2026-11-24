"""Detail for the q=4 size-9 complement-profile discrepancy.

The experiment's structure.json / report give a single complement profile
{2:10, 3:6, 4:3, 5:2} for the 11,480 maximal safe sets of size 9.  This script
prints one representative of every distinct profile that actually occurs and
hand-checkable per-line loads for it.
"""

from __future__ import annotations

import os

from common import Board, bits, read_board

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)


def main():
    n, blocks = read_board(os.path.join(BASE, "output", "board_pg2q4.txt"))
    board = Board(n, blocks, cap=3)
    _sizes, _by_size, maximal = board.enumerate_safe(collect=False)

    classes = {}
    for s in maximal:
        if s.bit_count() != 9:
            continue
        complement = ((1 << n) - 1) ^ s
        hist = {}
        for bm in board.block_masks:
            c = (complement & bm).bit_count()
            hist[c] = hist.get(c, 0) + 1
        classes.setdefault(tuple(sorted(hist.items())), []).append((s, complement))

    total = sum(len(v) for v in classes.values())
    print(f"maximal safe sets of size 9: {total}, distinct complement profiles: "
          f"{len(classes)}")
    for profile, members in sorted(classes.items(), key=lambda kv: -len(kv[1])):
        s, complement = members[0]
        print()
        print(f"profile {profile}  count {len(members)}")
        print(f"  S = {list(bits(s))}")
        print(f"  X = {list(bits(complement))}")
        loads = [(i + 1, (complement & bm).bit_count())
                 for i, bm in enumerate(board.block_masks)]
        print(f"  line loads |X & line_i| (1-based lines): {loads}")
        print(f"  safe(S)={board.safe(s)}  max load over lines = "
              f"{board.max_block_load(s)}  |S|={s.bit_count()}")
        print(f"  any safe extension? "
              f"{any(board.safe(s | (1 << p)) for p in bits(complement))}")


if __name__ == "__main__":
    main()
