"""Freeze a selected edge set and independently check every supplied quadruple."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time
from generate import save_gz

HERE = Path(__file__).resolve().parent
INCLUDED = HERE.parent/"parabola-local-repair-20261109/verify_subset.cpp"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", type=Path, required=True)
    args = ap.parse_args()
    destination = HERE/"input"
    destination.mkdir(exist_ok=False)
    cache = args.cache.read_bytes()
    p = 2647
    selected = []
    all_count = 0
    for line in cache.splitlines():
        edge = tuple(map(int, line.split()))
        assert len(edge) == 4
        all_count += 1
        nonzero = [t for t in edge if t]
        if len({min(t, p-t) for t in nonzero}) == len(nonzero):
            selected.append(edge)
    selected = sorted(set(selected))
    raw = (f"{p} {len(selected)}\n"+"".join(" ".join(map(str, q))+"\n" for q in selected)).encode("ascii")
    save_gz(destination/"verified_edges.txt.gz", raw)
    source = HERE/"verify_edges.cpp"
    wrapper_sha = hashlib.sha256(source.read_bytes()).hexdigest()
    included_sha = hashlib.sha256(INCLUDED.read_bytes()).hexdigest()
    exe = Path(tempfile.gettempdir())/f"upper-edge-{wrapper_sha[:8]}-{included_sha[:8]}.exe"
    subprocess.run(["g++", "-O2", "-std=c++17", str(source), "-o", str(exe)], check=True, timeout=60)
    with tempfile.TemporaryDirectory(prefix="upper-edges-") as temporary:
        plain = Path(temporary)/"edges.txt"
        plain.write_bytes(raw)
        started = time.monotonic()
        run = subprocess.run([str(exe), str(plain)], capture_output=True, text=True, timeout=60)
    receipt = {"p": p, "provided_edges": len(selected), "cache_edges": all_count,
               "cache_sha256": hashlib.sha256(cache).hexdigest(), "edge_input_sha256": hashlib.sha256(raw).hexdigest(),
               "wrapper_sha256": wrapper_sha, "included_verifier_sha256": included_sha,
               "verifier_binary_sha256": hashlib.sha256(exe.read_bytes()).hexdigest(),
               "returncode": run.returncode, "stdout": run.stdout, "stderr": run.stderr,
               "seconds": time.monotonic()-started,
               "scope": "Every supplied edge is forbidden by exact integer geometry. Completeness of the edge list is not required or claimed."}
    (destination/"geometry.json").write_text(json.dumps(receipt, indent=2)+"\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt, indent=2))
    assert run.returncode == 0 and run.stdout.strip() == f"VERIFIED_EDGES {p} {len(selected)}"


if __name__ == "__main__":
    main()
