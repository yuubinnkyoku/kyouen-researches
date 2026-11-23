"""Export the AG(2,q) board (lines and circles as blocks) in the arc_census format.

K1058's AG(2,q) board forbids four collinear points and four concyclic points; its
blocks are the q lines' point sets (size q) and the circles (size q+1).  The
Grundy program and the arc census read the same simple format, so exporting it
lets the generalised kyouen game be compared across three boards of the same
order: Miquelian inversive, Suzuki-Tits inversive, and AG(2,q).

Run:  python ag_board_export.py --q 8 --out ../output/blocks_ag_q8.txt
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    pts, blocks, through, nc, nl = build_ag(args.q)
    # dedupe blocks as point sets
    unique = sorted({tuple(sorted(b)) for b in blocks})
    print(f"AG(2,{args.q}): {len(pts)} points, {nc} circles, {nl} lines, "
          f"{len(unique)} distinct blocks")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        fh.write(f"{len(pts)} {len(unique)}\n")
        for b in unique:
            fh.write(f"{len(b)} " + " ".join(str(i) for i in b) + "\n")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
