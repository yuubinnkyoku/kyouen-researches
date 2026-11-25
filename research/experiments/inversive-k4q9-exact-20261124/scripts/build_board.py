"""Build Miquelian inversive plane boards locally, with design checks.

Circles come from the published builder
``finite-field-kyouen-20261120/scripts/inversive_fast.py`` (SHA-256 recorded).
The 3-(q^2+1, q+1, 1) parameters are re-checked here (points, circle count,
every pair on exactly q+1 circles, every triple on exactly one circle).

Usage:
    python build_board.py --q 9 11 13 16
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
REPO = EXP.parents[2]
PUBLISHED = REPO / "research/experiments/finite-field-kyouen-20261120/scripts"
OUT = EXP / "output"

sys.path.insert(0, str(PUBLISHED))
from inversive_fast import build_circles  # noqa: E402
from inversive_all_q import build_field  # noqa: E402


def special_points(q: int) -> dict:
    """Indices of infinity, 0 and 1 in the builder's point order.

    The builder uses ``points = list(F.elements()) + [None]``, so infinity is
    the last index; 0 and 1 are located by field identity.
    """
    F, sub = build_field(q)
    elems = list(F.elements())
    zero = sub[0]
    one = F.pow(zero, 0)
    return {"inf": len(elems), "zero": elems.index(zero), "one": elems.index(one)}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def design_checks(blocks: list[tuple[int, ...]], n: int, q: int) -> dict:
    assert len(blocks) == q * (q * q + 1), (len(blocks), q * (q * q + 1))
    assert all(len(b) == q + 1 and len(set(b)) == q + 1 for b in blocks)
    pair = Counter()
    for b in blocks:
        for i in range(len(b)):
            for j in range(i + 1, len(b)):
                pair[(b[i], b[j])] += 1
    assert len(pair) == n * (n - 1) // 2
    assert set(pair.values()) == {q + 1}, set(pair.values())
    triple = Counter()
    for b in blocks:
        for i in range(len(b)):
            for j in range(i + 1, len(b)):
                for k in range(j + 1, len(b)):
                    triple[(b[i], b[j], b[k])] += 1
    assert max(triple.values()) == 1
    assert len(triple) == n * (n - 1) * (n - 2) // 6
    return {"pairs": len(pair), "pair_multiplicity": q + 1,
            "triples": len(triple), "triple_multiplicity": 1}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    args = ap.parse_args()
    builder_sha = sha256(PUBLISHED / "inversive_fast.py")
    OUT.mkdir(parents=True, exist_ok=True)
    for q in args.q:
        points, blocks = build_circles(q, check_orbit_size=True)
        n = len(points)
        assert n == q * q + 1
        row = {"q": q, "v": n, "b": len(blocks), "block_size": q + 1,
               "builder_sha256": builder_sha,
               "special": special_points(q),
               "checks": design_checks(blocks, n, q)}
        path = OUT / f"board_q{q}.json"
        path.write_text(json.dumps({**row, "blocks": [list(b) for b in blocks]}),
                        encoding="utf-8")
        print(f"q={q}: v={n} b={len(blocks)} special={row['special']} "
              f"-> {path.name}", flush=True)


if __name__ == "__main__":
    main()
