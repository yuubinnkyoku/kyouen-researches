"""Merge one audited direct S5 LOSS into the experiment's current cache."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board  # noqa: E402

PLAN = EXP / "input/followup-s5-probe15m-plan.json"
SUMMARY = EXP / "output/followup-s5-probe15m/summary.json"
RAW_DIR = EXP / "output/followup-s5-probe15m"
BASE_CACHE = EXP / "output/current-exact-s5-latest.cache"
PREFLIGHT = EXP / "output/followup-preflight.json"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_cache(path: Path) -> tuple[str, dict[tuple[int, int], int]]:
    rows = {}
    header = "# s5 verdict cache: n=11 schema=1 (merged exact evidence; see receipt)"
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line:
            continue
        if line.startswith("#"):
            header = line
            continue
        fields = line.split(",")
        if len(fields) != 6 or fields[0] != "s5verdict" or int(fields[3]) != 5:
            raise SystemExit(f"malformed cache row {path}:{line_no}: {line}")
        key, verdict = (int(fields[1]), int(fields[2])), int(fields[4])
        if verdict not in (1, 2) or key in rows and rows[key] != verdict:
            raise SystemExit(f"invalid/conflicting cache row {path}:{line_no}: {line}")
        rows[key] = verdict
    return header, rows


def main() -> None:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    preflight = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    if len(plan["targets"]) != 1 or len(summary["results"]) != 1:
        raise SystemExit("expected exactly one planned and completed probe")
    target, result = plan["targets"][0], summary["results"][0]
    key = tuple(target["key"])
    if tuple(result["key"]) != key or result["stones"] != 5 or result["verdict"] != 2:
        raise SystemExit(f"raw replay is not the expected direct S5 LOSS: {result}")
    if result["budget"] != 15_000_000 or not 0 <= result["nodes"] <= result["budget"]:
        raise SystemExit(f"invalid exact-probe budget/nodes: {result}")
    raw_path = ROOT / result["raw"]
    input_path = ROOT / result["input"]
    if sha(raw_path) != result["raw_sha256"] or sha(input_path) != result["input_sha256"]:
        raise SystemExit("raw/input hash does not match the completed probe receipt")
    replay_rows = [row for row in csv.reader(raw_path.open(newline="", encoding="utf-8-sig"))
                   if row and row[0] == "replay"]
    if len(replay_rows) != 1:
        raise SystemExit(f"expected one raw replay row, found {len(replay_rows)}")
    row = replay_rows[0]
    if len(row) != 11 or tuple(map(int, (row[9], row[10]))) != key:
        raise SystemExit(f"raw row key/shape mismatch: {row}")
    if tuple(map(int, row[2:8])) != (5, result["legal"], 0, 15_000_000, 2, result["nodes"]):
        raise SystemExit(f"raw row fields disagree with summary: {row}")
    board = Board(11)
    mask = key[0] | (key[1] << 64)
    if board.canonical(mask) != mask or mask.bit_count() != 5:
        raise SystemExit(f"S5 target is unsafe or noncanonical: {key}")
    if board.legal(mask).bit_count() != result["legal"]:
        raise SystemExit("independent geometry legal-count disagrees with raw solver")
    parent = tuple(preflight["class"]["key"])
    parent_mask = parent[0] | (parent[1] << 64)
    if mask not in board.children(parent_mask):
        raise SystemExit(f"S5 key is not a legal child of target S4: {key}")

    header, exact = read_cache(BASE_CACHE)
    old = exact.get(key)
    if old is not None and old != 2:
        raise SystemExit(f"cache verdict conflicts with direct LOSS at {key}: {old}")
    if old == 2:
        raise SystemExit("direct LOSS is already in base cache; refusing a duplicate merge")
    exact[key] = 2
    out_cache = EXP / "output/current-exact-s5-after-followup-loss.cache"
    with out_cache.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(header + "\n")
        for (lo, hi), verdict in sorted(exact.items()):
            stream.write(f"s5verdict,{lo},{hi},5,{verdict},0\n")
    counts = Counter(exact.values())
    receipt = {
        "schema": "n11-reply27-single-s5-raw-loss-merge-v1",
        "base_cache": {"path": BASE_CACHE.relative_to(ROOT).as_posix(), "sha256": sha(BASE_CACHE),
                       "exact_rows": len(exact) - 1},
        "source_plan": {"path": PLAN.relative_to(ROOT).as_posix(), "sha256": sha(PLAN)},
        "source_summary": {"path": SUMMARY.relative_to(ROOT).as_posix(), "sha256": sha(SUMMARY)},
        "source_input": {"path": result["input"], "sha256": sha(input_path)},
        "source_raw": {"path": result["raw"], "sha256": sha(raw_path)},
        "source_solver": {"path": summary["solver_path"], "sha256": summary["solver_sha256"],
                          "source_sha256": summary["solver_source_sha256"]},
        "independent_geometry": {"canonical": True, "legal_edge_from_s4": True,
                                 "legal_count": result["legal"]},
        "merged_key": list(key), "merged_verdict": "LOSS", "budget": result["budget"],
        "nodes": result["nodes"], "cache": {"path": out_cache.relative_to(ROOT).as_posix(),
                                             "sha256": sha(out_cache), "exact_rows": len(exact),
                                             "verdict_counts": {str(k): v for k, v in sorted(counts.items())}},
        "conflicts": 0,
    }
    out_receipt = EXP / "output/followup-s5-cache-merge.json"
    out_receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"key": list(key), "verdict": "LOSS", "nodes": result["nodes"],
                      "cache_rows": len(exact), "counts": dict(counts),
                      "cache_sha256": sha(out_cache), "receipt_sha256": sha(out_receipt)}, sort_keys=True))


if __name__ == "__main__":
    main()
