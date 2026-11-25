"""Build a byte/hash inventory for this experiment, excluding the inventory."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
DEST = OUT / "artifact-sha256.json"


def main() -> None:
    entries = []
    for path in sorted(item for item in EXP.rglob("*") if item.is_file() and item != DEST):
        data = path.read_bytes()
        entries.append({"path": path.relative_to(ROOT).as_posix(), "bytes": len(data),
                        "sha256": hashlib.sha256(data).hexdigest()})
    document = {"schema": "n11-reply27-followup-artifact-inventory-v1",
                "inventory_excludes_itself": True,
                "artifact_count": len(entries),
                "total_bytes": sum(item["bytes"] for item in entries),
                "artifacts": entries}
    DEST.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(DEST.read_bytes()).hexdigest()
    print(json.dumps({"artifacts": len(entries), "bytes": document["total_bytes"],
                      "inventory_sha256": digest, "path": DEST.relative_to(ROOT).as_posix()}, sort_keys=True))


if __name__ == "__main__":
    main()
