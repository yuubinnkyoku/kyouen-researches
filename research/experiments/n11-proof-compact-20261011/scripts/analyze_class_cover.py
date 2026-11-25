"""Reconstruct and minimize the frozen 11x11 third-move LOSS-class cover."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
EXPERIMENT = Path(__file__).resolve().parents[1]
INDEPENDENT = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"
sys.path.insert(0, str(INDEPENDENT))
from independent import Board  # noqa: E402


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _key(record: dict) -> tuple[int, int]:
    value = record["key"]
    if (not isinstance(value, list) or len(value) != 2
            or any(type(part) is not int or part < 0 for part in value)):
        raise ValueError("malformed S4 class key")
    return value[0], value[1]


def _oriented_masks(board: Board, mask: int) -> set[int]:
    points = board.points(mask)
    return {
        sum(mapping[point] for point in points)
        for mapping in board.maps
    }


def reconstruct(frontier: list[dict], third_move_certificate: dict,
                audit: dict) -> dict:
    """Re-derive class-to-move incidence from integer geometry and frozen rows."""
    if len(frontier) != 3384:
        raise ValueError(f"expected 3384 canonical S4 classes, found {len(frontier)}")
    if len({_key(row) for row in frontier}) != len(frontier):
        raise ValueError("duplicate canonical S4 class")

    board = Board(11)
    root = (1 << 60) | (1 << 27)
    legal_root = board.legal(root)
    legal_moves = tuple(board.points(legal_root))
    if len(legal_moves) != 119:
        raise ValueError("the frozen root does not have 119 legal third moves")

    loss_rows = [row for row in frontier if row.get("verdict") == 2]
    if len(loss_rows) != 31:
        raise ValueError(f"expected 31 current LOSS classes, found {len(loss_rows)}")

    # Reconstruct each class's coverage instead of trusting its stored coverage
    # field. A physical orientation must contain the fixed root and third move,
    # and its fourth stone must be a legal response to that third move.
    class_cover: dict[tuple[int, int], set[int]] = {}
    for row in loss_rows:
        key = _key(row)
        mask = key[0] | (key[1] << 64)
        if mask.bit_count() != 4 or board.canonical(mask) != mask:
            raise ValueError(f"LOSS class is not a canonical four-stone state: {key}")
        board.legal(mask)
        cover: set[int] = set()
        for move in legal_moves:
            predecessor = root | (1 << move)
            response_mask = board.legal(predecessor)
            for oriented in _oriented_masks(board, mask):
                if oriented & root != root or not (oriented >> move & 1):
                    continue
                response = oriented & ~(root | (1 << move))
                if response.bit_count() != 1:
                    continue
                point = response.bit_length() - 1
                if response_mask >> point & 1:
                    if board.canonical(predecessor | response) != mask:
                        raise ValueError("oriented class has a noncanonical transition")
                    cover.add(move)
                    break
        stored = row.get("coverage")
        if (not isinstance(stored, list)
                or any(type(point) is not int for point in stored)
                or set(stored) != cover):
            raise ValueError(f"stored incidence disagrees with geometry for {key}")
        class_cover[key] = cover

    incidence: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for key, points in class_cover.items():
        for point in points:
            incidence[point].append(key)
    if set(incidence) - set(legal_moves):
        raise ValueError("a class covers a point outside the root's legal moves")

    covered = set(incidence)
    uncovered = sorted(set(legal_moves) - covered)
    histogram = Counter(len(incidence[point]) for point in covered)
    unique_points = sorted(point for point in covered if len(incidence[point]) == 1)
    forced_classes = {incidence[point][0] for point in unique_points}
    if forced_classes != set(class_cover):
        raise ValueError("unique-incidence points do not force every known LOSS class")

    certificate_root = third_move_certificate.get("root")
    if certificate_root != [root & ((1 << 64) - 1), root >> 64]:
        raise ValueError("third-move certificate has the wrong root")
    entries = third_move_certificate.get("complete_third_moves")
    if not isinstance(entries, list) or len(entries) != len(legal_moves):
        raise ValueError("third-move certificate does not list all legal moves")
    by_move = {entry.get("move"): entry for entry in entries}
    if len(by_move) != len(entries) or set(by_move) != set(legal_moves):
        raise ValueError("third-move certificate move set disagrees with geometry")
    certificate_witnesses: set[tuple[int, int]] = set()
    for point in legal_moves:
        entry = by_move[point]
        witness = entry.get("loss_class_witness")
        if point in covered:
            if entry.get("verdict") != 2 or not isinstance(witness, list) or len(witness) != 2:
                raise ValueError(f"missing frozen LOSS witness for move {point}")
            witness_key = tuple(witness)
            if witness_key not in class_cover or point not in class_cover[witness_key]:
                raise ValueError(f"invalid class witness for move {point}")
            certificate_witnesses.add(witness_key)
        elif entry.get("verdict") != 0 or witness is not None:
            raise ValueError(f"uncovered move {point} has a frozen verdict witness")
    if certificate_witnesses != set(class_cover):
        raise ValueError("the saved third-move witness does not use exactly the 31 LOSS classes")
    if uncovered != [100, 108] or len(covered) != 117:
        raise ValueError("reconstructed coverage differs from the frozen 117/119 result")

    raw_supported = audit.get("loss_classes_raw_supported")
    if raw_supported != 1:
        raise ValueError("the independent-trust audit no longer reports one raw-supported LOSS class")

    return {
        "schema": "n11-third-move-loss-class-cover-v1",
        "root": {"lo": root & ((1 << 64) - 1), "hi": root >> 64},
        "board_size": 11,
        "legal_third_moves": len(legal_moves),
        "known_loss_classes": len(class_cover),
        "covered_third_moves": len(covered),
        "uncovered_third_moves": uncovered,
        "incidence_histogram": {str(k): histogram[k] for k in sorted(histogram)},
        "unique_incidence_moves": unique_points,
        "forced_class_count": len(forced_classes),
        "minimum_loss_classes_for_current_117_cover": len(forced_classes),
        "class_minimum_witness": "all 31 known LOSS classes cover exactly 117 moves; 112 moves have a unique covering class, and those unique witnesses include all 31 classes",
        "loss_classes": [
            {"key": [key[0], key[1]], "covered_moves": sorted(points)}
            for key, points in sorted(class_cover.items())
        ],
        "raw_supported_loss_classes": raw_supported,
        "independent_minimax_limit": "Only one of these 31 class verdicts is raw-supported in the frozen trust audit. This cover minimum does not independently prove the class verdicts and is not a minimum proof-DAG node count or verification cost.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path,
                        default=EXPERIMENT / "output/class-cover-minimization.json")
    args = parser.parse_args()
    audit_dir = ROOT / "research/experiments/n11-independent-exact-audit-20261010/output"
    frontier_path = audit_dir / "frontier.json.gz"
    third_path = audit_dir / "third-move-certificate.json"
    audit_path = audit_dir / "audit.json"
    with gzip.open(frontier_path, "rt", encoding="utf-8") as stream:
        frontier = json.load(stream)
    with third_path.open(encoding="utf-8") as stream:
        third = json.load(stream)
    with audit_path.open(encoding="utf-8") as stream:
        audit = json.load(stream)
    result = reconstruct(frontier, third, audit)
    result["sources"] = {
        path.relative_to(ROOT).as_posix(): sha256(path)
        for path in (frontier_path, third_path, audit_path,
                     INDEPENDENT / "independent.py")
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
                        encoding="utf-8")
    print(json.dumps({k: result[k] for k in (
        "legal_third_moves", "known_loss_classes", "covered_third_moves",
        "uncovered_third_moves", "incidence_histogram", "forced_class_count",
        "minimum_loss_classes_for_current_117_cover", "raw_supported_loss_classes")},
        sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
