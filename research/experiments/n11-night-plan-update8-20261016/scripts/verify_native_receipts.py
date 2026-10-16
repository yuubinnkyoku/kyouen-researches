"""Fresh independent Python re-verification of the two native receipts that
lack a stored python-comparison (115540 LOSS, 144311 WIN); the 144193 LOSS
comparison is loaded and cross-checked instead of recomputed.

Uses only the K0372 standalone integer geometry plus the edge-DAG verifier of
n11-proof-dag-engine-20261011 (it never reads solver or cache verdicts).  The
same criteria as the stored pilot-144193-python-comparison.json apply:
verdict, trusted_leaves, nodes, edges and terminal_nodes must all reproduce.

Outputs (never overwriting existing files):
  output/native-115540-python-comparison.json
  output/native-144311-python-comparison.json
"""
from __future__ import annotations

import gzip
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
NATIVE = ROOT / "research/experiments/n11-native-terminal-checker-20261013/output"
sys.path.insert(0, str(ROOT / "research/experiments/n11-proof-dag-engine-20261011/scripts"))
from dag_verifier import verify_certificate  # noqa: E402

FRESH = (115540, 144311)
STORED = (144193,)


def main() -> None:
    results = {}
    for index in FRESH:
        started = time.monotonic()
        cert_path = NATIVE / f"pilot-{index}-terminal-dag.json.gz"
        receipt_path = NATIVE / f"pilot-{index}-receipt.json"
        receipt = json.loads(receipt_path.read_text())
        target = EXP / f"output/native-{index}-python-comparison.json"
        assert not target.exists(), "refusing to overwrite"
        with gzip.open(cert_path, "rt") as stream:
            cert = json.load(stream)
        checked = verify_certificate(cert)
        assert checked == {k: receipt[k] for k in checked}, (index, checked)
        comparison = {
            "s5_index": index,
            "fresh_python_verification": checked,
            "source_certificate": str(cert_path.relative_to(ROOT)),
            "source_receipt": str(receipt_path.relative_to(ROOT)),
            "wall_seconds": time.monotonic() - started,
        }
        target.write_text(json.dumps(comparison, indent=2, sort_keys=True) + "\n")
        results[str(index)] = checked
        print(f"{index}: {checked} in {comparison['wall_seconds']:.1f}s", flush=True)
    for index in STORED:
        receipt = json.loads((NATIVE / f"pilot-{index}-receipt.json").read_text())
        stored = json.loads((NATIVE / f"pilot-{index}-python-comparison.json").read_text())
        assert stored["s5_index"] == index
        assert stored["fresh_python_verification"] == \
            {k: receipt[k] for k in stored["fresh_python_verification"]}
        results[str(index)] = stored["fresh_python_verification"]
        print(f"{index}: stored comparison agrees with receipt", flush=True)
    print(json.dumps(results, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
