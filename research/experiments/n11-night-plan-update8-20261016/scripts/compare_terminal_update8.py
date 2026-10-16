"""Recheck the update8 terminal DAG 150871 with the independent Python verifier.

Mirrors n11-adaptive-verify-20261013/scripts/compare_dag.py for the update8
artifact layout: the C++ check_trace receipt in output/receipt-<index>.json is
compared field-by-field with a fresh independent Python re-derivation of the
exported terminal DAG.
"""
from __future__ import annotations

import argparse
import gzip
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research/experiments/n11-proof-dag-engine-20261011/scripts"))
from dag_verifier import verify_certificate  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("index", type=int, default=150871, nargs="?")
    args = p.parse_args()
    dag = EXP / f"output/terminal-{args.index}-dag.json.gz"
    started = time.monotonic()
    with gzip.open(dag, "rt") as stream:
        cert = json.load(stream)
    checked = verify_certificate(cert)
    receipt = json.loads((EXP / f"output/receipt-{args.index}.json").read_text())
    assert all(checked[k] == receipt[k] for k in checked), (checked, receipt)
    result = dict(schema="n11-night-update8-python-comparison-v1", s5_index=args.index,
                  fresh_python_verification=checked, wall_seconds=time.monotonic() - started,
                  native_receipt=(EXP / f"output/receipt-{args.index}.json").relative_to(ROOT).as_posix(),
                  certificate_sha256=receipt["certificate_sha256"])
    out = EXP / f"output/terminal-verify-{args.index}.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
