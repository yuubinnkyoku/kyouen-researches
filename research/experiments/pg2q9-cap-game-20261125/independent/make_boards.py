"""Write reference boards PG(2,q) for q in {3,5,7,8,9} as board files.

Independent construction (zero sets of normals over GF(q)); used to validate the
C enumerator against published cap-size distributions for q=3 and q=8.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pgcore as pc

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"


def write_board(path, n, lines):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"{n} {len(lines)}\n")
        for L in lines:
            fh.write(f"{len(L)} " + " ".join(map(str, L)) + "\n")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for q in (3, 5, 7, 8, 9):
        pts, lines = pc.pg(q)
        path = OUT / f"board_pg2q{q}.txt"
        write_board(path, len(pts), lines)
        print(f"PG(2,{q}): {len(pts)} points, {len(lines)} lines of {q+1} -> {path}")


if __name__ == "__main__":
    main()
