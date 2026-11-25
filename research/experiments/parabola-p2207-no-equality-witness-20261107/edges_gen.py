"""Locate the forbidden-edge generator and run it for a prime.

The harness rewrites TEMP/TMP per process, so ``tempfile.gettempdir()`` no longer
points at the directory that holds the prebuilt generator.  Resolution order:

  1. KYOUEN_EDGES_EXE environment variable,
  2. D:/tmp/forbidden_edges.exe, D:/tmp/p2207_drat/forbidden_edges.exe,
  3. <tempdir>/forbidden_edges.exe (the old behaviour).

The generated edge list is cached under CACHE_DIR keyed by prime and by the
generator hash, so repeated runs do not pay the enumeration twice.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path

CANDIDATES = [
    Path("D:/tmp/forbidden_edges.exe"),
    Path("D:/tmp/p2207_drat/forbidden_edges.exe"),
]
CACHE_DIR = Path("D:/tmp/kyouen-edges")


def generator() -> Path:
    env = os.environ.get("KYOUEN_EDGES_EXE")
    if env:
        p = Path(env)
        if p.exists():
            return p
        raise SystemExit(f"KYOUEN_EDGES_EXE does not exist: {p}")
    for p in CANDIDATES:
        if p.exists():
            return p
    import tempfile
    p = Path(tempfile.gettempdir()) / "forbidden_edges.exe"
    if p.exists():
        return p
    raise SystemExit("cannot locate forbidden_edges.exe; set KYOUEN_EDGES_EXE")


def run_edges(p: int) -> list[tuple[int, int, int, int]]:
    gen = generator()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    tag = hashlib.sha256(gen.read_bytes()).hexdigest()[:16]
    cache = CACHE_DIR / f"edges_{p}_{tag}.txt"
    if not cache.exists() or cache.stat().st_size == 0:
        tmp = cache.with_suffix(".tmp")
        with tmp.open("w", encoding="ascii", newline="\n") as f:
            subprocess.run([str(gen), str(p)], stdout=f, stderr=subprocess.DEVNULL,
                           check=True, stdin=subprocess.DEVNULL)
        os.replace(tmp, cache)
    return [tuple(map(int, line.split())) for line in
            cache.read_text(encoding="ascii").splitlines()]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: edges_gen.py <p>")
    edges = run_edges(int(sys.argv[1]))
    print(len(edges))
