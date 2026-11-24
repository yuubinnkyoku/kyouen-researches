"""SAT-free verification of an s-arc witness, rebuilding the circles itself.

The circle family is rebuilt from the published builder
(``finite-field-kyouen-20261120/scripts/inversive_fast.py``, pinned by SHA-256
in the board JSON) and the design parameters are re-checked, so a PASS here
does not rely on the board file the solver read.

Usage:
    python verify_arc.py --q 9 --s 4 --points 1 2 3 ... [--max-intersections]
    python verify_arc.py --q 9 --s 4 --file output/witness.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
REPO = EXP.parents[2]
PUBLISHED = REPO / "research/experiments/finite-field-kyouen-20261120/scripts"
BOARDS = EXP / "output"

sys.path.insert(0, str(PUBLISHED))
from inversive_fast import build_circles  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(q: int, s: int, points: list[int]) -> dict:
    board_meta = json.loads((BOARDS / f"board_q{q}.json").read_text(encoding="utf-8"))
    builder_sha = sha256(PUBLISHED / "inversive_fast.py")
    out: dict = {"q": q, "s": s, "n": len(points), "points": sorted(points),
                 "builder_sha256": builder_sha,
                 "builder_sha256_matches_board":
                     builder_sha == board_meta["builder_sha256"]}
    pts, blocks = build_circles(q, check_orbit_size=True)
    out["rebuilt_points"] = len(pts)
    out["rebuilt_circles"] = len(blocks)
    out["design_ok"] = (len(pts) == q * q + 1 and len(blocks) == q * (q * q + 1)
                        and all(len(b) == q + 1 for b in blocks))
    S = set(points)
    out["points_in_range"] = all(0 <= p < len(pts) for p in S)
    worst = 0
    dist: dict[int, int] = {}
    for b in blocks:
        r = len(S.intersection(b))
        dist[r] = dist.get(r, 0) + 1
        worst = max(worst, r)
    out["max_intersection"] = worst
    out["intersection_profile"] = {str(k): v for k, v in sorted(dist.items())}
    out["is_s_arc"] = worst <= s
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--s", type=int, required=True)
    ap.add_argument("--points", type=int, nargs="*", default=None)
    ap.add_argument("--file", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    if args.file is not None:
        data = json.loads(args.file.read_text(encoding="utf-8"))
        points = data["points"]
    else:
        points = args.points or []
    res = verify(args.q, args.s, points)
    print(json.dumps(res, indent=1))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(res, indent=1), encoding="utf-8")
    raise SystemExit(0 if res["is_s_arc"] and res["design_ok"] else 1)


if __name__ == "__main__":
    main()
