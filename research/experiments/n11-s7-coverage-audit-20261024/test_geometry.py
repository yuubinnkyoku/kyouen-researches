#!/usr/bin/env python3
"""Cross-check the gap auditor's independent integer geometry against the terminal checker."""
from itertools import combinations
from pathlib import Path
import importlib.util
import sys

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
spec = importlib.util.spec_from_file_location("coverage_audit", HERE / "analyze.py")
audit = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = audit
spec.loader.exec_module(audit)
sys.path.insert(0, str(EXP / "n11-four-s8-joint-terminal52-20261023"))
from terminal_geometry import canonical, circle, legal, points, safe  # noqa: E402


def main():
    roots = set().union(*(audit.read_keys(p, n) for p, n in
                          zip(audit.S9_FILES, (29, 27, 2, 10))))
    targets = [
        int("00000000100000021081000020000020", 16),
        int("00000000000001121800020000000020", 16),
    ]
    # Both geometry implementations must agree on every legal move of 68 S9
    # roots and the two closest not-yet-classified S7 candidates.
    for board in sorted(roots | set(targets)):
        assert safe(board)
        assert audit.canonical(board) == canonical(board)
        assert audit.legal_points(board) == legal(board)
        for p in points(board):
            child = board ^ (1 << p)
            assert audit.canonical(child) == canonical(child)
    # The exact circle equation includes degenerate collinear triples.
    # Test every point for a sample of triples, not only positive examples.
    for board in targets:
        for a, b, c in combinations(points(board), 3):
            mask = audit.forbidden_by_triple(a, b, c)
            for p in range(121):
                assert bool(mask >> p & 1) == circle(a, b, c, p)
    print("PASS 70 S7/S9 legal boundaries, D4 parents, and 70*121 exact triple checks")


if __name__ == "__main__":
    main()
