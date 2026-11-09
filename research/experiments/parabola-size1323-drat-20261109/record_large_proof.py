"""Record hashes of local pending evidence without publishing the large blob."""
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    directory = HERE/"output/shape-112"
    output = directory/"proof-manifest.json"
    if output.exists():
        raise FileExistsError("preserve the existing evidence manifest")
    proof = directory/"proof.drat.gz"
    solver = json.loads((directory/"solver.json").read_text())
    with proof.open("rb") as stream:
        compressed_sha = hashlib.file_digest(stream, "sha256").hexdigest()
    digest, lines = hashlib.sha256(), 0
    with gzip.open(proof, "rb") as stream:
        for block in iter(lambda: stream.read(8*1024*1024), b""):
            digest.update(block)
            lines += block.count(b"\n")
    assert digest.hexdigest() == solver["proof_sha256"] and lines == solver["proof_lines"]
    report = {"local_path": "proof.drat.gz", "compression": "gzip", "compressed_bytes": proof.stat().st_size,
              "compressed_sha256": compressed_sha, "raw_sha256": digest.hexdigest(), "raw_lines": lines,
              "cnf_sha256": solver["input_sha256"],
              "availability": "Local ignored evidence, not included in Git. Restore this exact file or regenerate the proof before resuming its audit.",
              "scope": "Content provenance only; no DRAT acceptance is implied."}
    output.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
