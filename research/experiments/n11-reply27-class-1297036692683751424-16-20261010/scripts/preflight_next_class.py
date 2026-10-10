"""Independently regenerate the lowest-unknown cover candidate S5 boundary."""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board  # noqa: E402

RECLASS = EXP / "output/frontier-reclassification.json"
GEOMETRY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
CACHE = EXP / "output/current-exact-s5.cache"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_cache() -> dict[tuple[int, int], int]:
    result = {}
    for line in CACHE.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        fields = line.split(",")
        result[(int(fields[1]), int(fields[2]))] = int(fields[4])
    return result


def csv_target(key: tuple[int, int], legal_count: int) -> list[int | str]:
    return ["s5target", 0, 5, key[0], key[1], legal_count, 0, 0, 0, 0, 0]


def main() -> None:
    reclass = json.loads(RECLASS.read_text(encoding="utf-8"))
    candidate = reclass["best_unresolved_class_covering_all_remaining"]
    parent_key = tuple(candidate["key"])
    parent = parent_key[0] | (parent_key[1] << 64)
    geometry = json.loads(gzip.decompress(GEOMETRY.read_bytes()))
    row = next((g for g in geometry if tuple(g["key"]) == parent_key), None)
    if row is None:
        raise SystemExit(f"candidate missing from complete S4 geometry: {parent_key}")

    board = Board(11)
    if board.canonical(parent) != parent:
        raise SystemExit("candidate S4 is not canonical")
    legal_parent = board.legal(parent).bit_count()
    children = sorted((child & ((1 << 64) - 1), child >> 64) for child in board.children(parent))
    if set(children) != {tuple(c) for c in row["children"]} or len(children) != candidate["s5_children"]:
        raise SystemExit("independently generated candidate S5 boundary disagrees with frozen geometry")

    exact = read_cache()
    records = []
    for key in children:
        mask = key[0] | (key[1] << 64)
        if board.canonical(mask) != mask or mask.bit_count() != 5:
            raise SystemExit(f"unsafe/noncanonical S5 child: {key}")
        legal = board.legal(mask).bit_count()
        records.append({"key": list(key), "legal_count": legal,
                        "cache_verdict": exact.get(key, 0)})
    statuses = {1: "WIN", 2: "LOSS", 0: "UNKNOWN"}
    counts = {name: sum(statuses[r["cache_verdict"]] == name for r in records)
              for name in ("LOSS", "WIN", "UNKNOWN")}
    expected_counts = {name: candidate["boundary"].get(name, 0) for name in ("LOSS", "WIN", "UNKNOWN")}
    if counts != expected_counts:
        raise SystemExit(f"candidate boundary/cache mismatch: {counts} != {candidate['boundary']}")
    unknown = [r for r in records if r["cache_verdict"] == 0]

    all_path = EXP / "input/candidate-s5-all.csv"
    unknown_path = EXP / "input/candidate-s5-cache-unknown.csv"
    for path, values in ((all_path, records), (unknown_path, unknown)):
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream, lineterminator="\n")
            for item in values:
                writer.writerow(csv_target(tuple(item["key"]), item["legal_count"]))

    result = {
        "schema": "n11-reply27-next-class-geometric-preflight-v1",
        "main_commit": "154f3b7a67b97e13acbaee8b04dc74ddca728d19",
        "candidate_s4": {"key": list(parent_key), "coverage": sorted(row["coverage"]),
                         "legal_s5_moves": legal_parent, "children": len(children),
                         "cache_boundary": counts, "status": "UNKNOWN"},
        "independent_geometry": {"implementation": "Board from n11-independent-exact-audit-20261010/scripts/independent.py",
                                 "source_sha256": sha(Path(__file__).resolve().parents[4] / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"),
                                 "geometry_path": GEOMETRY.relative_to(ROOT).as_posix(),
                                 "geometry_sha256": sha(GEOMETRY), "canonical_boundary_match": True},
        "s5_cache": {"path": CACHE.relative_to(ROOT).as_posix(), "sha256": sha(CACHE),
                     "exact_rows": len(exact)},
        "target_files": {"all": {"path": all_path.relative_to(ROOT).as_posix(), "rows": len(records), "sha256": sha(all_path)},
                         "cache_unknown": {"path": unknown_path.relative_to(ROOT).as_posix(), "rows": len(unknown), "sha256": sha(unknown_path)}},
        "s5_children": records,
    }
    out = EXP / "output/candidate-preflight.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"candidate_s4": list(parent_key), "children": len(children),
                      "cache_counts": counts, "unknown": len(unknown),
                      "lowest_legal_unknowns": sorted((r["legal_count"], tuple(r["key"])) for r in unknown)[:10],
                      "report_sha256": sha(out)}, sort_keys=True))


if __name__ == "__main__":
    main()
