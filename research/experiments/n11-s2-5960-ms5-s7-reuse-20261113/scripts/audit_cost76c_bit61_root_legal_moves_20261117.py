#!/usr/bin/env python3
"""Independent exact-geometry audit of the cost76c bit-61 WIN7 root.

Re-derives the raw-root defense list in three ways:
  1. this file's pivoted Bareiss 4x4 determinant;
  2. a translated 3x3 determinant over (x, y, x^2+y^2);
  3. the repository's pinned legal_candidates.py implementation.
The result is a certificate-extraction preflight, not a game verdict.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

BASE_MAIN = "353cda65aa4550ff159ba760130371fccb9c474a"
CHILD_HEX = "00000000010000809002000001000000"
BIT = 61
ROOT_HEX = "0000000001000080b002000001000000"
LEGAL_CANDIDATES_BLOB_SHA = "8e97082c42838c7a4a4b6d2dd235276c8d43ab9a"
N = 121


def cells_from_hex(hex_text: str) -> list[int]:
    value = int(hex_text, 16)
    return [i for i in range(N) if (value >> i) & 1]


def xyq(cell: int) -> tuple[int, int, int]:
    x, y = cell % 11, cell // 11
    return x, y, x * x + y * y


def det4_bareiss(points: tuple[int, int, int, int] | list[int]) -> int:
    """Exact determinant of rows [x,y,x^2+y^2,1]."""
    matrix = [[*xyq(cell)[:2], xyq(cell)[2], 1] for cell in points]
    sign, previous = 1, 1
    for k in range(3):
        pivot_row = next((r for r in range(k, 4) if matrix[r][k] != 0), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            matrix[k], matrix[pivot_row] = matrix[pivot_row], matrix[k]
            sign = -sign
        pivot = matrix[k][k]
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                numerator = matrix[i][j] * pivot - matrix[i][k] * matrix[k][j]
                if numerator % previous:
                    raise ArithmeticError("Bareiss division was not exact")
                matrix[i][j] = numerator // previous
        for i in range(k + 1, 4):
            matrix[i][k] = 0
        previous = pivot
    return sign * matrix[3][3]


def det3_relative(points: tuple[int, int, int, int] | list[int]) -> int:
    """Translated determinant in 3D; equals -det4_bareiss above."""
    p1, p2, p3, p4 = [xyq(cell) for cell in points]
    a = tuple(p2[i] - p1[i] for i in range(3))
    b = tuple(p3[i] - p1[i] for i in range(3))
    c = tuple(p4[i] - p1[i] for i in range(3))
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def load_pinned_legal_candidates(script_path: Path):
    data = script_path.read_bytes()
    git_blob_sha = hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()
    if git_blob_sha != LEGAL_CANDIDATES_BLOB_SHA:
        raise RuntimeError(
            f"legal_candidates.py blob changed: {git_blob_sha} != {LEGAL_CANDIDATES_BLOB_SHA}"
        )
    spec = importlib.util.spec_from_file_location("pinned_legal_candidates", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load pinned legal_candidates.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, git_blob_sha


def audit(repo_script_dir: Path) -> dict:
    child = cells_from_hex(CHILD_HEX)
    root = cells_from_hex(ROOT_HEX)
    if len(child) != 6 or BIT in child:
        raise AssertionError("child must have exactly six stones and bit 61 must be empty")
    if root != sorted(child + [BIT]):
        raise AssertionError("root is not exactly child | (1 << 61)")
    if int(ROOT_HEX, 16) != (int(CHILD_HEX, 16) | (1 << BIT)):
        raise AssertionError("root hex mismatch")

    root_zero_quads = []
    root_quad_count = 0
    for quad in itertools.combinations(root, 4):
        root_quad_count += 1
        d4, d3 = det4_bareiss(quad), det3_relative(quad)
        if d4 != -d3:
            raise AssertionError(f"determinant implementations disagree on root quad {quad}")
        if d4 == 0:
            root_zero_quads.append(list(quad))
    if root_zero_quads:
        raise AssertionError(f"seven-stone root is unsafe: {root_zero_quads}")

    root_set = set(root)
    direct_legal: list[int] = []
    illegal_witnesses: dict[str, list[int]] = {}
    for candidate in range(N):
        if candidate in root_set:
            continue
        witness = None
        for triple in itertools.combinations(root, 3):
            d4 = det4_bareiss((*triple, candidate))
            d3 = det3_relative((*triple, candidate))
            if d4 != -d3:
                raise AssertionError(
                    f"determinant implementations disagree for triple {triple}, cell {candidate}"
                )
            if d4 == 0:
                witness = list(triple)
                break
        if witness is None:
            direct_legal.append(candidate)
        else:
            illegal_witnesses[str(candidate)] = witness

    # Triple-union enumeration mirrors the engine's forbidden-mask construction.
    forbidden = set(root)
    for triple in itertools.combinations(root, 3):
        for candidate in range(N):
            if candidate not in triple and det3_relative((*triple, candidate)) == 0:
                forbidden.add(candidate)
    mask_legal = [cell for cell in range(N) if cell not in forbidden]
    if mask_legal != direct_legal:
        raise AssertionError("direct candidate test and triple-union mask differ")

    legal_module, legal_blob_sha = load_pinned_legal_candidates(
        repo_script_dir / "legal_candidates.py"
    )
    pinned_stones, pinned_legal = legal_module.legal_candidates(ROOT_HEX)
    if pinned_stones != root or pinned_legal != direct_legal:
        raise AssertionError("pinned repository legal_candidates.py disagrees")

    for candidate in direct_legal:
        if any(
            det4_bareiss(quad) == 0
            for quad in itertools.combinations(sorted(root + [candidate]), 4)
        ):
            raise AssertionError(f"legal candidate {candidate} creates a forbidden quadruple")
    for candidate_text, triple in illegal_witnesses.items():
        if det4_bareiss((*triple, int(candidate_text))) != 0:
            raise AssertionError(f"illegal candidate {candidate_text} lacks a zero determinant witness")

    witness_bytes = json.dumps(
        illegal_witnesses, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return {
        "schema": "n11-cost76c-bit61-root-legal-defense-audit-v1",
        "base_main": BASE_MAIN,
        "child_hex": CHILD_HEX,
        "candidate_bit": BIT,
        "root_hex": ROOT_HEX,
        "child_stones": child,
        "root_stones": root,
        "root_four_subset_count": root_quad_count,
        "root_zero_determinants": len(root_zero_quads),
        "legal_defense_count": len(direct_legal),
        "legal_defenses": direct_legal,
        "illegal_defense_count": len(illegal_witnesses),
        "illegal_witnesses_sha256": hashlib.sha256(witness_bytes).hexdigest(),
        "illegal_witness_sample": dict(list(illegal_witnesses.items())[:5]),
        "det4_vs_translated_det3_agree": True,
        "direct_vs_triple_union_agree": True,
        "pinned_legal_candidates_agree": True,
        "legal_candidates_git_blob_sha": legal_blob_sha,
        "all_legal_extensions_safe": True,
        "all_illegal_extensions_have_witness": True,
        "extraction_preflight_only": True,
        "game_verdict_claimed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-script-dir", type=Path,
        default=Path(__file__).resolve().parent,
        help="directory containing the pinned legal_candidates.py",
    )
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    result = audit(args.repo_script_dir)
    rendered = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    print("sha256=" + hashlib.sha256(rendered.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
