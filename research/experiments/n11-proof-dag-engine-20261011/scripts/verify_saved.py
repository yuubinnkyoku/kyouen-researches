"""Verify a saved proof DAG without launching or importing the solver."""
import argparse
import gzip
import json
from pathlib import Path

from dag_verifier import verify_certificate


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("certificate", type=Path)
    ap.add_argument("--out", type=Path, help="write the verification receipt as JSON")
    args = ap.parse_args()
    opener = gzip.open if args.certificate.suffix == ".gz" else open
    with opener(args.certificate, "rt", encoding="utf-8") as f:
        certificate = json.load(f)
    result = verify_certificate(certificate)
    result["certificate"] = str(args.certificate)
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
    if args.out:
        args.out.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
