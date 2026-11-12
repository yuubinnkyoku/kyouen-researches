"""Audit a greedy/ruin-and-recreate safe set with independent integer geometry.

The construction (build_safe.cpp) only knows the forbidden-edge list, so a
reported set is checked twice here:

  1. against the edge list itself (no edge fully contained), and
  2. with the independent generic 4x4 Leibniz verifier
     (parabola-local-repair-20261109/verify_subset.cpp), which recomputes exact
     integer determinants and does not share code with the search.

Usage: audit_safe_set.py --input walk.json [--output out.json]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from probe_driver import run_gen  # noqa: E402

VERIFIER = ROOT / "research/experiments/parabola-local-repair-20261109/verify_subset.cpp"
VERIFIER_SHA = "c817e7808e5d853a6ca0b897e5a0f454944f38069c8c32b5a10ef7f97b32261c"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", default=None)
    ap.add_argument("--binary", default=None)
    args = ap.parse_args()
    src = Path(args.input)
    data = json.loads(src.read_text(encoding="utf-8"))
    p = data["p"]
    points = sorted(data["points"])
    if len(points) != len(set(points)) or any(not 0 <= t < p for t in points):
        raise SystemExit("invalid point list")
    edges = run_gen(str(Path(__import__("os").environ["TEMP"]) / "forbidden_edges.exe"), p)
    chosen = set(points)
    inside = [q for q in edges if set(q) <= chosen]
    h = (p - 1) // 2
    complete = [t for t in range(1, h + 1) if t in chosen and p - t in chosen]
    empty = [t for t in range(1, h + 1) if t not in chosen and p - t not in chosen]
    record = {
        "p": p, "size": len(points), "edges": len(edges),
        "edges_inside": len(inside), "first_edges_inside": inside[:5],
        "class": {"x": 1 if 0 in chosen else 0, "c": len(complete), "e": len(empty),
                  "complete": complete[:5], "empty": empty[:5]},
        "input": str(src), "input_sha256": sha(src),
        "verifier_sha256": sha(VERIFIER),
        "verifier_sha256_expected": VERIFIER_SHA,
    }
    binary = Path(args.binary) if args.binary else Path(__import__("os").environ["TEMP"]) / "verify_subset.exe"
    if not binary.exists():
        subprocess.run(["g++", "-O2", "-std=c++17", str(VERIFIER), "-o", str(binary)], check=True)
    payload = f"{p} {len(points)}\n" + " ".join(map(str, points)) + "\n"
    t0 = time.time()
    res = subprocess.run([str(binary), "--modular-filter"], input=payload.encode("ascii"),
                         capture_output=True)
    record.update({"verifier_rc": res.returncode,
                   "verifier_stdout": res.stdout.decode().strip(),
                   "verifier_stderr": res.stderr.decode().strip()[:300],
                   "verifier_seconds": round(time.time() - t0, 2),
                   "safe": res.returncode == 0 and not inside})
    out = Path(args.output) if args.output else src.with_name(src.stem + "_audit.json")
    out.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")
    print(json.dumps(record, indent=2, ensure_ascii=False))
    return 0 if record["safe"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
