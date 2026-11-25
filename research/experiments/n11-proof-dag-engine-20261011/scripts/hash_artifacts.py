"""Create/check a SHA-256 inventory for this experiment and solver inputs."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-proof-dag-engine-20261011"
MANIFEST = EXP / "output/final-sha256.json"
EXTERNAL = [
    ROOT / "cpp/solvers/kyouen_dfpn_root.cpp",
    ROOT / "cpp/solvers/kyouen_residual_micro.hpp",
    ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py",
]


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def inventory():
    paths = [p for p in EXP.rglob("*") if p.is_file() and
             "__pycache__" not in p.parts and p.suffix != ".pyc" and p != MANIFEST]
    paths += EXTERNAL
    rows = []
    for p in sorted(set(paths), key=lambda x: str(x).lower()):
        rows.append(dict(path=p.relative_to(ROOT).as_posix(), bytes=p.stat().st_size,
                         sha256=digest(p)))
    return dict(schema="n11-proof-dag-engine-sha256-v1", files=rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        failures = []
        for row in data["files"]:
            path = ROOT / Path(row["path"])
            if not path.is_file() or path.stat().st_size != row["bytes"] or digest(path) != row["sha256"]:
                failures.append(row["path"])
        if failures:
            raise SystemExit("SHA-256 mismatch: " + ", ".join(failures))
        print(f"sha256_check=passed files={len(data['files'])}")
        return
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    data = inventory()
    MANIFEST.write_text(json.dumps(data, sort_keys=True,
                                   separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST.relative_to(ROOT)} files={len(data['files'])}")


if __name__ == "__main__":
    main()
