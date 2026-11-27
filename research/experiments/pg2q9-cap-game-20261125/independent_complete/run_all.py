"""Run the whole independent verification in order.

Python standard library only.  From this directory:

    python run_all.py

Each step writes machine-readable results to out/ and prints a human-readable
summary.  The whole run takes about 2.5 minutes; the 4-cap orbit BFS and the
full 2-cap upset DPs dominate.
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

STEPS = [
    "t1_board.py",
    "t2_frame_census.py",
    "t3_group.py",
    "t4_grundy_samples.py",
    "t5_extra_layers.py",
    "t6_arithmetic.py",
    "t7_crosschecks.py",
    "t8_conic_mechanism.py",
    "t9_conic_orbits.py",
]


def main():
    t0 = time.time()
    for step in STEPS:
        print("=" * 70)
        print("RUN", step, flush=True)
        t = time.time()
        r = subprocess.run(
            [sys.executable, step],
            cwd=str(Path(__file__).resolve().parent),
        )
        if r.returncode != 0:
            raise SystemExit(f"{step} failed with exit code {r.returncode}")
        print(f"DONE {step} in {time.time() - t:.1f}s", flush=True)
    print("=" * 70)
    print(f"ALL OK in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
