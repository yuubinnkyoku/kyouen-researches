#!/usr/bin/env python3
"""Materialize the optimizer's selected repair rows for the dual-tight ranker."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repair", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    repair = json.loads(args.repair.read_text(encoding="utf-8"))
    additive = repair.get("additive_optimum", {})
    selected = additive.get("selected")
    if not isinstance(selected, list) or not selected:
        raise SystemExit("repair input has no additive-optimum selected classes")
    if len(selected) != repair.get("minimum_additional_classes"):
        raise SystemExit("additive repair size disagrees with the structural minimum")
    if additive.get("mip_gap") != 0.0:
        raise SystemExit("refusing ranking adapter for a nonzero-gap additive repair")

    result = {
        "schema": "n11-dual-tight-repair-ranking-input-v1",
        "source_repair": {
            "path": args.repair.as_posix(),
            "sha256": sha256(args.repair),
        },
        "repair_selected": selected,
        "claim": "schema adapter only; selected classes and optimizer values are copied verbatim; no verdict or optimization is changed",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8", newline="\n")
    print(json.dumps({"selected": len(selected), "out": args.out.as_posix()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
