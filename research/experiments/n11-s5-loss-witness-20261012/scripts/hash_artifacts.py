"""Refresh the experiment's SHA-256 inventory without hashing itself."""
import hashlib
import json
from pathlib import Path

EXP = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


files = []
for path in sorted(p for p in EXP.rglob("*") if p.is_file() and p.name != "final-sha256.json"):
    if ".local" in path.parts or "__pycache__" in path.parts:
        continue
    files.append({"path": str(path.relative_to(EXP)).replace("\\", "/"),
                  "bytes": path.stat().st_size, "sha256": sha256(path)})
(EXP / "output").mkdir(exist_ok=True)
(EXP / "output/final-sha256.json").write_text(
    json.dumps({"schema": "n11-s5-loss-witness-sha256-v1", "files": files},
               sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
print(json.dumps({"files": len(files), "manifest": "output/final-sha256.json"}, sort_keys=True))
