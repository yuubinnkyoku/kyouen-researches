"""Create/check a SHA-256 inventory of this experiment's persisted artifacts."""
import argparse
import hashlib
import json
from pathlib import Path

EXPERIMENT = Path(__file__).resolve().parents[1]
MANIFEST = EXPERIMENT / "output" / "final-sha256.json"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def current_inventory():
    files = []
    for path in sorted(EXPERIMENT.rglob("*")):
        if not path.is_file() or path == MANIFEST:
            continue
        relative = path.relative_to(EXPERIMENT)
        if "__pycache__" in relative.parts or path.suffix in {".pyc", ".pyo"}:
            continue
        files.append({"path": relative.as_posix(), "bytes": path.stat().st_size,
                      "sha256": sha256(path)})
    return {"schema": "n11-proof-dag-followup-sha256-v1", "files": files}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="check the existing inventory without rewriting it")
    args = parser.parse_args()
    actual = current_inventory()
    if args.check:
        if not MANIFEST.is_file():
            parser.error(f"missing manifest: {MANIFEST}")
        expected = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if expected != actual:
            expected_paths = {item["path"] for item in expected.get("files", [])}
            actual_paths = {item["path"] for item in actual["files"]}
            raise SystemExit("artifact inventory mismatch: "
                             f"missing={sorted(expected_paths - actual_paths)} "
                             f"added={sorted(actual_paths - expected_paths)} "
                             "or a size/hash changed")
    else:
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(json.dumps(actual, sort_keys=True, separators=(",", ":")) + "\n",
                            encoding="utf-8")
    print(json.dumps({"files": len(actual["files"]), "manifest": str(MANIFEST),
                      "checked": args.check}, sort_keys=True))


if __name__ == "__main__":
    main()
