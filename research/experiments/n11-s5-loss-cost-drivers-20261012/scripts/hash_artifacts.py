"""Hash the tracked experiment inputs, outputs, scripts, and solver source."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUTPUT = EXP / "output/final-sha256.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    files = []
    for path in sorted(p for p in EXP.rglob("*") if p.is_file()):
        relative = path.relative_to(EXP).as_posix()
        if path == OUTPUT or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if relative.startswith("output/profile-regression-v3/"):
            continue  # failed assertion-only development run; v4 is the audited receipt
        files.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)})
    solver = ROOT / "cpp/solvers/kyouen_dfpn_root.cpp"
    result = {
        "schema": "n11-s5-loss-cost-drivers-final-sha256-v1",
        "self_excluded": "output/final-sha256.json",
        "files": files,
        "solver_source": {"path": "cpp/solvers/kyouen_dfpn_root.cpp",
                          "bytes": solver.stat().st_size, "sha256": sha256(solver)},
    }
    OUTPUT.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
                      encoding="utf-8")
    print(json.dumps({"path": OUTPUT.relative_to(ROOT).as_posix(),
                      "sha256": sha256(OUTPUT), "file_count": len(files),
                      "solver_source_sha256": result["solver_source"]["sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
