"""Independently rebuild the requested S4 class boundary and cache intersection."""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board  # noqa: E402

S4_KEY = (1297036692683751424, 16)
CURRENT_CACHE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/output/canonical-current-s5.cache"
STRATEGY_CACHE = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/current-exact-s5.cache"
AUDIT = ROOT / "research/experiments/n11-independent-exact-audit-20261010/output/audit.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_cache(path: Path) -> dict[tuple[int, int], int]:
    result: dict[tuple[int, int], int] = {}
    with path.open(newline="", encoding="utf-8") as stream:
        for row_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
                raise ValueError(f"invalid S5 exact-cache row at {path}:{row_no}: {row}")
            key, verdict = (int(row[1]), int(row[2])), int(row[4])
            if verdict not in (1, 2) or key in result and result[key] != verdict:
                raise ValueError(f"invalid or conflicting S5 cache result {key}: {verdict}")
            result[key] = verdict
    return result


def key_csv(key: tuple[int, int], legal: int) -> list[str]:
    # audit_s5_raw_history.py consumes layer/key/legal/status columns 2/3/4/5/7.
    return ["s5target", "0", "5", str(key[0]), str(key[1]), str(legal), "0", "0", "0", "0", "0"]


def write_targets(path: Path, rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        csv.writer(stream, lineterminator="\n").writerows(rows)


def main() -> None:
    if read_cache(CURRENT_CACHE) != read_cache(STRATEGY_CACHE):
        raise SystemExit("independent-audit cache differs from strategy cache")

    board = Board(11)
    parent = S4_KEY[0] | (S4_KEY[1] << 64)
    if board.canonical(parent) != parent or parent.bit_count() != 4:
        raise SystemExit("requested S4 key is not canonical")
    children = board.children(parent)
    cache = read_cache(CURRENT_CACHE)
    child_keys = sorted((child & ((1 << 64) - 1), child >> 64) for child in children)
    if len(child_keys) != 108 or len(set(child_keys)) != len(child_keys):
        raise SystemExit(f"unexpected canonical S5 boundary size: {len(child_keys)}")

    hits = {key: cache[key] for key in child_keys if key in cache}
    if len(hits) != 9 or any(value != 2 for value in hits.values()):
        raise SystemExit(f"current exact-cache intersection changed: {hits}")
    unknown = [key for key in child_keys if key not in cache]
    legal_counts = {key: board.legal(key[0] | (key[1] << 64)).bit_count() for key in child_keys}

    all_rows = [key_csv(key, legal_counts[key]) for key in child_keys]
    unknown_rows = [key_csv(key, legal_counts[key]) for key in unknown]
    write_targets(EXP / "input/target-s5-all.csv", all_rows)
    write_targets(EXP / "input/target-s5-cache-unknown.csv", unknown_rows)

    child_lines = "\n".join(f"{lo},{hi}" for lo, hi in child_keys) + "\n"
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    current_main = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()
    preflight = {
        "schema": "n11-reply27-s4-s5-boundary-preflight-v1",
        "main_commit": current_main,
        "s4_key": list(S4_KEY),
        "s4_canonical": True,
        "independent_geometry_source": "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py",
        "independent_geometry_source_sha256": sha(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"),
        "canonical_s5_child_count": len(child_keys),
        "canonical_s5_child_keys_sha256": hashlib.sha256(child_lines.encode()).hexdigest(),
        "current_cache": {
            "path": CURRENT_CACHE.relative_to(ROOT).as_posix(),
            "sha256": sha(CURRENT_CACHE),
            "rows": len(cache),
            "verdict_rows_identical_to_strategy_cache": True,
            "target_verdict_counts": {"WIN": sum(v == 1 for v in hits.values()), "LOSS": sum(v == 2 for v in hits.values())},
            "target_cache_hits": [[lo, hi, hits[(lo, hi)]] for lo, hi in sorted(hits)],
            "target_cache_unknown_or_absent": len(unknown),
        },
        "current_s4_frontier": {
            "audit_path": AUDIT.relative_to(ROOT).as_posix(),
            "audit_sha256": sha(AUDIT),
            "class_counts": audit["s4"],
            "secured_third_moves": audit["secured"],
            "remaining_third_moves": audit["remaining"],
            "integer_minimum_additional_classes": audit["minimum_additional_classes"],
            "rational_lp_dual": audit["rational_dual"],
        },
        "s5_children": [
            {"key": list(key), "legal_count": legal_counts[key], "cache_verdict": hits.get(key)}
            for key in child_keys
        ],
        "raw_history_target_csv": "research/experiments/n11-reply27-class-1297036692683751424-16-20261010/input/target-s5-all.csv",
        "unknown_cache_target_csv": "research/experiments/n11-reply27-class-1297036692683751424-16-20261010/input/target-s5-cache-unknown.csv",
    }
    out = EXP / "output/preflight.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(preflight, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"children": len(child_keys), "cache_hits": len(hits), "unknown": len(unknown),
                      "child_keys_sha256": preflight["canonical_s5_child_keys_sha256"],
                      "cache_sha256": preflight["current_cache"]["sha256"],
                      "preflight_sha256": sha(out)}, sort_keys=True))


if __name__ == "__main__":
    main()
