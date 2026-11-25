"""Independent verifier for blocking-set witnesses (no SAT dependency).

A witness file is {"q": int, "n": int, "points": [...]}.
Checks every circle meets the set and prints the intersection profile.

Usage:
    python verify_blocking.py output/blocking_q7_n14.json [...]
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def verify(path: Path) -> dict:
    w = json.loads(path.read_text(encoding="utf-8"))
    board = json.loads((OUT / f"board_q{w['q']}.json").read_text(encoding="utf-8"))
    X = set(w["points"])
    assert len(X) == w["n"], (len(X), w["n"])
    prof = Counter(len(X.intersection(C)) for C in board["blocks"])
    assert 0 not in prof, "some circle is missed"
    return {"q": w["q"], "n": w["n"], "min_intersection": min(prof),
            "max_intersection": max(prof),
            "profile": dict(sorted(prof.items()))}


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: verify_blocking.py <witness.json> [...]")
    for arg in sys.argv[1:]:
        print(json.dumps(verify(Path(arg))), flush=True)


if __name__ == "__main__":
    main()
