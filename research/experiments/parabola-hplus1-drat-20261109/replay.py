"""Replay frozen DRAT proofs into a fresh receipt directory; never regenerate SAT."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from audit import CHECKER_SOURCE, CHECKER_SHA, bounded

HERE = Path(__file__).resolve().parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--timeout", type=float, default=180)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    assert sha(CHECKER_SOURCE.read_bytes()) == CHECKER_SHA
    exe = Path(tempfile.gettempdir())/f"hplus1-replay-{CHECKER_SHA[:16]}.exe"
    subprocess.run(["g++", "-O2", "-std=c++17", str(CHECKER_SOURCE), "-o", str(exe)], check=True, timeout=60)
    binary_sha = sha(exe.read_bytes())
    receipts = []
    for shape in "abc":
        out = HERE/"output"/f"shape-{shape}"
        old = json.loads((out/"audit.json").read_text())
        cnf = gzip.decompress((out/"input.cnf.gz").read_bytes())
        proof = gzip.decompress((out/"proof.drat.gz").read_bytes())
        assert sha(cnf) == old["input_sha256"] and sha(proof) == old["proof_sha256"]
        with tempfile.TemporaryDirectory(prefix="hplus1-replay-") as temporary:
            temporary = Path(temporary)
            (temporary/"input.cnf").write_bytes(cnf)
            (temporary/"proof.drat").write_bytes(proof)
            receipt = bounded([str(exe), str(temporary/"input.cnf"), str(temporary/"proof.drat")], args.timeout)
        receipt.update(shape=shape, p=2647, target_size=1324,
                       input_sha256=sha(cnf), proof_sha256=sha(proof),
                       checker_source_sha256=CHECKER_SHA, checker_binary_sha256=binary_sha,
                       verified=receipt["returncode"] == 0 and receipt["stdout"].splitlines()[-1:] == ["VERIFIED"])
        receipts.append(receipt)
        (args.output/f"shape-{shape}.json").write_text(json.dumps(receipt, indent=2)+"\n", encoding="utf-8", newline="\n")
        print(f"shape={shape} verified={receipt['verified']} seconds={receipt['seconds']:.1f}", flush=True)
    result = {"all_three_verified": all(r["verified"] for r in receipts),
              "p": 2647, "excluded_size": 1324, "implied_upper_bound": 1323,
              "receipts": receipts,
              "scope": "Actual DRAT replay only. Use the class-coverage proof and separately checked edge soundness to infer the geometric upper bound."}
    (args.output/"summary.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8", newline="\n")
    if not result["all_three_verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
