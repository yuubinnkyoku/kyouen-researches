"""Gzip solver traces losslessly and refresh the run's hashes."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n",
                    encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("run_dir", type=Path)
    args = ap.parse_args()
    run_dir = args.run_dir.resolve()
    trace_dir = run_dir / "solver-traces"
    if not run_dir.is_dir() or not trace_dir.is_dir():
        ap.error("run directory must contain solver-traces")
    traces = sorted(trace_dir.glob("*.csv"))
    if not traces:
        ap.error("no uncompressed solver traces found")
    records = []
    for source in traces:
        target = source.with_suffix(source.suffix + ".gz")
        if target.exists():
            ap.error(f"refusing to overwrite {target}")
        raw_size, raw_hash = source.stat().st_size, sha256(source)
        with source.open("rb") as src, target.open("xb") as dst:
            with gzip.GzipFile(filename="", mode="wb", fileobj=dst, mtime=0) as zipped:
                while True:
                    block = src.read(1024 * 1024)
                    if not block:
                        break
                    zipped.write(block)
        with gzip.open(target, "rb") as zipped:
            decoded_hash = hashlib.sha256()
            decoded_size = 0
            while True:
                block = zipped.read(1024 * 1024)
                if not block:
                    break
                decoded_hash.update(block)
                decoded_size += len(block)
        if decoded_size != raw_size or decoded_hash.hexdigest() != raw_hash:
            target.unlink()
            raise ValueError(f"gzip round-trip mismatch for {source.name}")
        record = {"raw_path": source.name, "raw_bytes": raw_size,
                  "raw_sha256": raw_hash, "gzip_path": target.name,
                  "gzip_bytes": target.stat().st_size, "gzip_sha256": sha256(target)}
        source.unlink()
        records.append(record)

    archive = {"schema": "n11-solver-trace-gzip-archive-v1", "files": records}
    archive_path = trace_dir / "trace-archive-manifest.json"
    dump(archive_path, archive)
    summary_path = run_dir / "summary.json"
    if summary_path.is_file() and len(records) == 1:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        item = records[0]
        old_path = summary.get("trace_path")
        summary["trace_raw_path"] = old_path
        summary["trace_raw_bytes"] = item["raw_bytes"]
        summary["trace_raw_sha256"] = item["raw_sha256"]
        summary["trace_path"] = (Path("solver-traces") / item["gzip_path"]).as_posix()
        summary["trace_bytes"] = item["gzip_bytes"]
        summary["trace_sha256"] = item["gzip_sha256"]
        dump(summary_path, summary)
    manifest_path = run_dir / "artifact-manifest.json"
    if manifest_path.is_file():
        artifacts = []
        for path in sorted(p for p in run_dir.rglob("*")
                           if p.is_file() and p != manifest_path):
            artifacts.append({"path": str(path.relative_to(run_dir)).replace("\\", "/"),
                              "bytes": path.stat().st_size, "sha256": sha256(path)})
        dump(manifest_path, {"schema": "n11-shared-s5-proof-bundle-files-v1",
                             "files": artifacts})
    print(json.dumps(archive, sort_keys=True))


if __name__ == "__main__":
    main()
