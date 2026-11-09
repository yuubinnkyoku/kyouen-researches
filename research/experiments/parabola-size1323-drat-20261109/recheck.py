"""Replay a qualified saved certificate into a fresh receipt, without SAT reruns."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from audit import bounded, CHECKER_SOURCE, CHECKER_SHA
from corrected import encode, dimacs, SHAPES

HERE = Path(__file__).resolve().parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shape", choices=SHAPES, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--timeout", type=float, default=300)
    args = ap.parse_args()
    if args.output.exists():
        raise FileExistsError("fresh receipt path required")
    key = args.shape
    location = HERE/"output"/("fixed" if key in ("000", "101") else "")/f"shape-{key}"
    init = json.loads((location/"solver.json").read_text())
    cnf = gzip.decompress((location/"input.cnf.gz").read_bytes())
    proof = gzip.decompress((location/"proof.drat.gz").read_bytes())
    edges_raw = gzip.decompress((HERE.parent/"parabola-hplus1-drat-20261109/input/verified_edges.txt.gz").read_bytes())
    edges = [tuple(map(int, row.split())) for row in edges_raw.decode("ascii").splitlines()[1:]]
    clauses, nv, _, _ = encode(2647, key, edges)
    assert dimacs(clauses, nv) == cnf
    assert sha(cnf) == init["input_sha256"] and sha(proof) == init["proof_sha256"]
    assert sha(CHECKER_SOURCE.read_bytes()) == CHECKER_SHA
    exe = Path(tempfile.gettempdir())/f"size1323-recheck-{CHECKER_SHA[:16]}-{os.getpid()}.exe"
    subprocess.run(["g++", "-O2", "-std=c++17", str(CHECKER_SOURCE), "-o", str(exe)], check=True, timeout=60)
    with tempfile.TemporaryDirectory(prefix="size1323-recheck-") as directory:
        directory = Path(directory)
        (directory/"input.cnf").write_bytes(cnf)
        (directory/"proof.drat").write_bytes(proof)
        receipt = bounded([str(exe), str(directory/"input.cnf"), str(directory/"proof.drat")], args.timeout)
    receipt.update(shape=key, p=2647, target_size=1323, input_sha256=sha(cnf), proof_sha256=sha(proof),
                   proof_lines=init["proof_lines"], checker_source_sha256=CHECKER_SHA,
                   checker_binary_sha256=sha(exe.read_bytes()),
                   verified=receipt["returncode"] == 0 and receipt["stdout"].splitlines()[-1:] == ["VERIFIED"])
    args.output.write_text(json.dumps(receipt, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
