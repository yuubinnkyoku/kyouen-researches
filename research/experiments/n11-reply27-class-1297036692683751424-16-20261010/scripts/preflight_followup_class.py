"""Prepare an independently regenerated, unprobed follow-up cover candidate."""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board  # noqa: E402

RECLASS = EXP / "output/frontier-reclassification-from-start-final.json"
GEOMETRY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
CACHE = EXP / "output/current-exact-s5-latest.cache"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reclassification", type=Path, default=RECLASS)
    parser.add_argument("--cache", type=Path, default=CACHE)
    parser.add_argument("--out-csv", type=Path, default=EXP / "input/followup-s5-all.csv")
    parser.add_argument("--out", type=Path, default=EXP / "output/followup-preflight.json")
    args = parser.parse_args()
    reclass_path = args.reclassification if args.reclassification.is_absolute() else ROOT / args.reclassification
    cache_path = args.cache if args.cache.is_absolute() else ROOT / args.cache
    out_csv = args.out_csv if args.out_csv.is_absolute() else ROOT / args.out_csv
    out_path = args.out if args.out.is_absolute() else ROOT / args.out
    reclass = json.loads(reclass_path.read_text(encoding="utf-8"))
    candidate = reclass["best_unresolved_class_covering_all_remaining"]
    key = tuple(candidate["key"])
    mask = key[0] | (key[1] << 64)
    geo = json.loads(gzip.decompress(GEOMETRY.read_bytes()))
    row = next(g for g in geo if tuple(g["key"]) == key)
    board = Board(11)
    if board.canonical(mask) != mask:
        raise SystemExit("follow-up S4 key is not canonical")
    children = sorted((c & ((1 << 64) - 1), c >> 64) for c in board.children(mask))
    if set(children) != {tuple(c) for c in row["children"]}:
        raise SystemExit("independent follow-up geometry differs from frozen complete boundary")

    exact = {}
    for line in cache_path.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            f = line.split(",")
            exact[(int(f[1]), int(f[2]))] = int(f[4])
    records = []
    for child in children:
        child_mask = child[0] | (child[1] << 64)
        if board.canonical(child_mask) != child_mask or child_mask.bit_count() != 5:
            raise SystemExit(f"unsafe/noncanonical follow-up S5: {child}")
        records.append({"key": list(child), "legal_count": board.legal(child_mask).bit_count(),
                        "cache_verdict": exact.get(child, 0)})
    counts = {name: sum(("UNKNOWN" if r["cache_verdict"] == 0 else "WIN" if r["cache_verdict"] == 1 else "LOSS") == name for r in records)
              for name in ("LOSS", "WIN", "UNKNOWN")}
    if candidate["verdict"] != "UNKNOWN" or len(children) != candidate["s5_children"]:
        raise SystemExit("follow-up candidate status/boundary changed")
    expected = {name: candidate["boundary"].get(name, 0) for name in counts}
    if counts != expected:
        raise SystemExit(f"candidate/cache boundary mismatch: {counts} != {expected}")

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        for r in records:
            writer.writerow(["s5target", 0, 5, *r["key"], r["legal_count"], 0, 0, 0, 0, 0])
    unresolved = sorted((r["legal_count"], tuple(r["key"])) for r in records if r["cache_verdict"] == 0)
    result = {"schema": "n11-reply27-followup-class-preflight-v1",
              "class": {"key": list(key), "coverage": sorted(row["coverage"]),
                        "children": len(children), "cache_boundary": counts, "status": "UNKNOWN"},
              "independent_geometry": {"implementation": "n11-independent-exact-audit Board",
                                       "source_sha256": sha(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"),
                                       "complete_geometry_path": GEOMETRY.relative_to(ROOT).as_posix(),
                                       "complete_geometry_sha256": sha(GEOMETRY), "full_boundary_match": True},
              "current_s5_cache": {"path": cache_path.relative_to(ROOT).as_posix(), "sha256": sha(cache_path),
                                   "exact_rows": len(exact)},
              "s5_children": records,
              "raw_audit_targets_csv": {"path": out_csv.relative_to(ROOT).as_posix(),
                                        "rows": len(records), "sha256": sha(out_csv)},
              "lowest_legal_unknown_s5": [{"legal_count": n, "key": list(k)} for n, k in unresolved[:10]],
              "note": "No raw-history/S6/S7 preflight has been run for these children yet; the list is not dispatch approval."}
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"class": list(key), "boundary": counts,
                      "lowest_legal_unknown_s5": result["lowest_legal_unknown_s5"][:4],
                      "preflight_sha256": sha(out_path)}, sort_keys=True))


if __name__ == "__main__":
    main()
