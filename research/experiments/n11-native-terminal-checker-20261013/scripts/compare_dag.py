"""Compare C++'s portable DAG to prior Python exports and optionally recheck it."""
import argparse
import gzip
import json
from pathlib import Path
import sys
import time

EXP = Path(__file__).resolve().parents[1]
ROOT = EXP.parents[2]
sys.path.insert(0, str(ROOT / "research/experiments/n11-proof-dag-engine-20261011/scripts"))
from dag_verifier import verify_certificate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("index", type=int)
    parser.add_argument("--prior", type=Path)
    parser.add_argument("--rerun-python", action="store_true")
    args = parser.parse_args()
    if args.prior:
        args.prior = args.prior.resolve()
    dag = EXP / f"output/pilot-{args.index}-terminal-dag.json.gz"
    started = time.monotonic()
    with gzip.open(dag, "rt") as stream:
        cert = json.load(stream)
    result = dict(s5_index=args.index)
    if args.prior:
        with gzip.open(args.prior, "rt") as stream:
            prior = json.load(stream)
        # A proof edge set has no ordering semantics; normalize labels explicitly.
        for certificate in (cert, prior):
            for node in certificate["nodes"].values():
                node["edges"].sort(key=lambda e: e["move"])
        assert cert == prior, "C++ export differs from prior Python proof"
        result["prior_python_export_semantically_identical"] = True
        result["prior_certificate"] = str(args.prior.relative_to(ROOT))
        del prior
    if args.rerun_python:
        checked = verify_certificate(cert)
        native = json.loads((EXP / f"output/pilot-{args.index}-receipt.json").read_text())
        assert all(checked[k] == native[k] for k in checked)
        result["fresh_python_verification"] = checked
    result["wall_seconds"] = time.monotonic() - started
    (EXP / f"output/pilot-{args.index}-python-comparison.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
