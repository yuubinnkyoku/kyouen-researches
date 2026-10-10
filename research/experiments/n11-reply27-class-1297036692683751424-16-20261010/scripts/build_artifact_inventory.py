"""Hash every experiment artifact except this self-referential inventory."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
INVENTORY = EXP / "output/artifact-sha256.json"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    files = []
    for path in sorted(EXP.rglob("*")):
        if not path.is_file() or path == INVENTORY or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        files.append({"path": path.resolve().relative_to(ROOT.resolve()).as_posix(),
                      "bytes": path.stat().st_size, "sha256": sha(path)})
    result = {
        "schema": "n11-reply27-experiment-artifact-sha256-v1",
        "algorithm": "SHA-256",
        "inventory_path": INVENTORY.resolve().relative_to(ROOT.resolve()).as_posix(),
        "inventory_excluded_from_its_own_entries": True,
        "file_count": len(files),
        "total_bytes": sum(row["bytes"] for row in files),
        "files": files,
    }
    INVENTORY.parent.mkdir(parents=True, exist_ok=True)
    INVENTORY.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"inventory": result["inventory_path"], "file_count": len(files),
                      "total_bytes": result["total_bytes"], "sha256": sha(INVENTORY)}, sort_keys=True))


if __name__ == "__main__":
    main()
