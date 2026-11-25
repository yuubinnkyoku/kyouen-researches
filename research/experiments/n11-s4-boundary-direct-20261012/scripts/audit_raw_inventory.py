#!/usr/bin/env python3
"""Recheck every unique solver raw referenced by the reply27 batch audits."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-s4-boundary-direct-20261012"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def expected_code(value):
    if isinstance(value, str):
        return {"UNKNOWN": 0, "WIN": 1, "LOSS": 2}.get(value)
    if isinstance(value, int):
        return value
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=EXP / "output/raw-sha256-audit.json")
    args = parser.parse_args()

    receipts = sorted((EXP / "output").glob("*batch-audit.json"))
    receipts.append(EXP / "output/raw-audit-before-merge.json")
    if len(receipts) != 23:
        raise ValueError(f"expected 9 S5 and 14 S6 batch audit receipts, found {len(receipts)}")
    records = {}
    reference_count = 0
    for receipt_path in receipts:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        for item in walk(receipt):
            if "raw_path" not in item or "raw_sha256" not in item:
                continue
            path_text = str(item["raw_path"]).replace("\\", "/")
            if path_text.startswith(".local/"):
                raise ValueError(f"audit still depends on an untracked .local raw: {path_text}")
            relative = Path(path_text)
            path = relative if relative.is_absolute() else ROOT / relative
            if not path.is_file():
                raise FileNotFoundError(path)
            actual_sha = sha(path)
            if actual_sha != item["raw_sha256"]:
                raise ValueError(f"raw SHA-256 mismatch: {path_text}")

            key = tuple(item["key"]) if isinstance(item.get("key"), list) else None
            replay_rows = []
            with path.open(encoding="utf-8-sig", newline="") as stream:
                for line_no, row in enumerate(csv.reader(stream), 1):
                    if row and row[0] == "replay" and len(row) == 11:
                        row_key = (int(row[9]), int(row[10]))
                        if key is None or row_key == key:
                            replay_rows.append((line_no, row))
            if len(replay_rows) != 1:
                raise ValueError(f"expected one matching replay row for {path_text}, found {len(replay_rows)}")
            line_no, row = replay_rows[0]
            parsed = {"key": [int(row[9]), int(row[10])], "stones": int(row[2]),
                      "legal": int(row[3]), "is_or": int(row[4]), "budget": int(row[5]),
                      "verdict_code": int(row[6]), "nodes": int(row[7]), "line": line_no}
            for name, actual in (("legal", parsed["legal"]), ("stones", parsed["stones"]),
                                 ("budget", parsed["budget"]), ("nodes", parsed["nodes"])):
                if name in item and int(item[name]) != actual:
                    raise ValueError(f"raw {name} mismatch for {path_text}: {actual} != {item[name]}")
            if key is not None and parsed["key"] != list(key):
                raise ValueError(f"raw key mismatch for {path_text}")
            code = expected_code(item.get("verdict", item.get("verdict_code")))
            if code is not None and parsed["verdict_code"] != code:
                raise ValueError(f"raw verdict mismatch for {path_text}")
            if "raw_line" in item and int(item["raw_line"]) != line_no:
                raise ValueError(f"raw line mismatch for {path_text}")

            normalized = path.resolve().relative_to(ROOT).as_posix()
            signature = (normalized, actual_sha)
            record = {"path": normalized, "sha256": actual_sha, "bytes": path.stat().st_size,
                      **parsed, "verdict": {0: "UNKNOWN", 1: "WIN", 2: "LOSS"}[parsed["verdict_code"]],
                      "referenced_by": []}
            prior = records.get(signature)
            if prior is None:
                records[signature] = record
            elif any(prior[name] != record[name] for name in ("key", "stones", "legal", "budget", "verdict_code", "nodes")):
                raise ValueError(f"conflicting audit metadata for {normalized}")
            records[signature]["referenced_by"].append(receipt_path.relative_to(ROOT).as_posix())
            reference_count += 1

    entries = sorted(records.values(), key=lambda row: row["path"])
    counts = Counter((row["stones"], row["verdict"]) for row in entries)
    output = args.output if args.output.is_absolute() else ROOT / args.output
    doc = {
        "schema": "n11-reply27-raw-sha256-audit-v1",
        "source_audit_receipt_count": len(receipts),
        "raw_reference_count": reference_count,
        "unique_raw_file_count": len(entries),
        "unique_raw_counts_by_stones_and_verdict": {
            str(stones): {verdict: counts[(stones, verdict)] for verdict in ("WIN", "LOSS", "UNKNOWN")
                          if counts[(stones, verdict)]}
            for stones in sorted({row["stones"] for row in entries})
        },
        "untracked_local_raw_references": 0,
        "saved_raw_relocation_manifest": "research/experiments/n11-s4-boundary-direct-20261012/input/saved-s6-raw-relocations.json",
        "saved_raw_relocation_manifest_sha256": sha(EXP / "input/saved-s6-raw-relocations.json"),
        "source_audits": [{"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)} for path in receipts],
        "raw_files": entries,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in doc.items() if k not in ("source_audits", "raw_files")},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
