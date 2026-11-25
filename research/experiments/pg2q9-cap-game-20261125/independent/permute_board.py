"""Write a point-permuted copy of a board file.

Used to check that the C enumerator's counts do not depend on the point order
(the DFS enumerates caps by increasing point index, so a permutation changes the
whole traversal order).
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"


def main() -> None:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        HERE.parent / "output" / "board_pg2q9.txt"
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else OUT / "board_pg2q9_perm.txt"
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 12345
    n, lines = [], []
    with open(src, "r", encoding="utf-8") as fh:
        head = fh.readline().split()
        n = int(head[0])
        for row in fh:
            f = row.split()
            if f:
                lines.append([int(x) for x in f[1:]])
    perm = list(range(n))
    random.Random(seed).shuffle(perm)
    assert sorted(perm) == list(range(n))
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(f"{n} {len(lines)}\n")
        for L in lines:
            fh.write(f"{len(L)} " + " ".join(str(perm[p]) for p in L) + "\n")
    print(f"wrote {dst} with seed {seed}")


if __name__ == "__main__":
    main()
